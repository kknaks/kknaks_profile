"""실버 3단계(부위) 반영 — 결정론 · v5 범위 바로잡기(부위 = 「어디에 맞냐」 · 원천은 이름 칸만 — _RESUME §2 10-28).

입력: step3-decisions.json(결정 — 원천 경로 · 노드 추가 · 노드 속성 · 문자열 행선지 · 트리 밖 · 질문)
      step3-lexicon.json(사전 · 이름 칸 · 셈 밖 칸 · 잔여 형태소 · 허용 목록)
      procedure-master-v3.json site_tree(DEC-002 트리) · 원천(결정 source 키)
      step3-research.json — 근거로만(근거 약 대조 가드)
출력: step3-sites.json · step3-sites.md · step3-source-fix.md

rows 는 원천에서 이 스크립트가 만든다. 사전에 잡혔는데 결정에 없는 문자열 · 사전 밖 부위 형태소 잔여 → open[].
결정 파일에 행선지(또는 사전 · 허용 목록)를 더하면 닫힌다. 숫자는 이 파일에 적지 않는다.
"""
import argparse
import collections
import glob
import json
import os
import re
import unicodedata
from pathlib import Path

W = Path(__file__).resolve().parent
AP = argparse.ArgumentParser()
AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
AP.add_argument('--decisions', default=str(W / 'step3-decisions.json'))
AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
AP.add_argument('--trace', help='문자열마다 사전 매치 · 잔여 낱말을 이 파일로(경계 전수 시험용)')
ARGS = AP.parse_args()
OUT = Path(ARGS.out)
DEC = json.load(open(ARGS.decisions))
LEX = json.load(open(W / DEC['lexicon']))
TREE = json.load(open(W / DEC['tree_source']['file']))[DEC['tree_source']['key']]
RES = json.load(open(W / 'step3-research.json'))
SRC = Path(ARGS.source or DEC['source']['path'])


def fail(msg):
    raise SystemExit(f'검사 실패: {msg}')


def norm(s):
    k = re.sub(r'\s+', '', s)
    return k.lower() if re.match(r'^[A-Za-z]', k) else k


def fold(s):
    """라틴 글자의 악센트만 지운다(NFKD 후 결합 부호 제거 · 글자 수 보존). 한글 · 한자 · 가나는 그대로."""
    out = []
    for ch in s:
        if '\u00c0' <= ch <= '\u024f':
            b = ''.join(c for c in unicodedata.normalize('NFKD', ch) if not unicodedata.combining(c))
            out.append(b if len(b) == 1 else ch)
        else:
            out.append(ch)
    return ''.join(out)


# ───────── 1. 원천 → 문자열 행 ─────────
def walk(x, path, f, out):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(v, path + [k], f, out)
    elif isinstance(x, list):
        for v in x:
            walk(v, path + [None], f, out)
    elif isinstance(x, str):
        out.append((f, '.'.join('[]' if p is None else p for p in path), fold(x)))


src = []
for fp in sorted(glob.glob(str(SRC / DEC['source']['glob']))):
    walk(json.load(open(fp)), [], os.path.basename(fp), src)
n_fields_all = len(src)
name_fields = {(x['file'], x['key']) for x in DEC['name_fields']['fields']}
src = [r for r in src if (r[0], r[1]) in name_fields]  # v5 — 부위 원천은 이름 칸만(설명 문장 칸은 셈 밖)
compiled = [((i - 100000 if e['first'] else i), e, re.compile(e['pattern'], 0 if e['case_sensitive'] else re.I))
            for i, e in enumerate(LEX['entries'])]

# 「앞 낱말이 노드 이름 · 동의어(+과/와)면 허용 안 함」(W-C) — 노드 이름 + 노드로 가는 결정 문자열 정규형
node_terms = {re.sub(r'\(묶음\)$', '', n) for n in DEC['nodes']} | {x['key'][0] for x in DEC['strings'] if x['destination'] == 'node'}


def node_list_end(t):
    """「등」 앞이 노드 이름 · 동의어인데 나열 끝이 아니면 True(W-C).
    나열 끝 = 앞 낱말 앞에 나열 기호(, · / 、) · 여는 괄호가 있다(「부위(눈가 등)」)(「복부, 엉덩이, 팔, 다리 등의」 · 「코·이마 등은」).
    「가슴과 등」(+과/와) · 「팔 등 제모」(낱말 하나)는 부위 「등」일 수 있어 허용하지 않는다."""
    m = re.search(r'([가-힣A-Za-z]+)\s*$', t)
    if not m:
        return False
    w = m.group(1)
    conj = re.search(r'(?<=[가-힣])[과와]$', w)
    if conj:
        w = w[:-1]
    if w not in node_terms:
        return False
    return bool(conj) or not re.search(r'[,·/、(]\s*$', t[:m.start()])


found = {}
covered = []
trace = []
for f, p, s in src:
    ms = []
    for pr, e, rx in compiled:
        for m in rx.finditer(s):
            if m.end() > m.start():
                ms.append((m.start(), pr, m.end(), e))
    ms.sort(key=lambda t: (t[0], t[1]))
    pos, cv = 0, []
    for st, pr, en, e in ms:
        if st < pos:
            continue
        pos = en
        cv.append((st, en))
        if ARGS.trace:
            trace.append(dict(text=s, file=f, start=st, span=s[st:en], expr=e['expr']))
        if e['expr'].startswith('#skip'):
            continue
        k = (norm(s[st:en]), e['expr'])
        c = found.setdefault(k, dict(count=0, count_name_fields=0, variants=collections.Counter(), by_file=collections.Counter(),
                                     name_field_samples=[], prose_samples=[]))
        c['count'] += 1
        c['variants'][s[st:en]] += 1
        c['by_file'][f] += 1
        ctx = dict(file=f, key=p, text=s[max(0, st - 20):en + 20].replace('\n', ' '))
        if (f, p) in name_fields:
            c['count_name_fields'] += 1
            if len(c['name_field_samples']) < 3 and ctx['text'] not in [x['text'] for x in c['name_field_samples']]:
                c['name_field_samples'].append(ctx)
        elif len(c['prose_samples']) < 2 and ctx['text'] not in [x['text'] for x in c['prose_samples']]:
            c['prose_samples'].append(ctx)
    covered.append(cv)

# ───────── 2. 잔여 검사(사전 밖 부위 형태소) ─────────
RS = LEX['residual']
allowed = {a.lower() for g in RS['allowed'] for a in g['tokens']}
allowed_pat = [(re.compile(p['token']), re.compile(p['before']), p.get('not_after_node_term', False)) for p in RS.get('allowed_patterns', [])]
morph = ([(m, re.compile(re.escape(m))) for m in RS['morphemes_ko']]
         + [(m['label'], re.compile(m['pattern'])) for m in RS.get('morpheme_patterns_ko', [])]
         + [(m, re.compile(re.escape(m), re.I)) for m in RS['stems_en']])  # 영문 어간은 단어 안에서도(F-B) — 소음은 허용 목록
reviewed = DEC.get('residual_reviewed', [])  # 사람이 문맥을 보고 닫은 잔여(결정 한 줄 — W-C)
residual = collections.OrderedDict()
for (f, p, s), cv in zip(src, covered):
    seen = set()
    for m, rx in morph:
        for mm in rx.finditer(s):
            if any(a <= mm.start() < b for a, b in cv):
                continue
            a, b = mm.start(), mm.end()
            while a > 0 and re.match('[가-힣A-Za-z]', s[a - 1]):
                a -= 1
            while b < len(s) and re.match('[가-힣A-Za-z]', s[b]):
                b += 1
            if (a, b) in seen:  # 한 낱말에 형태소 여럿 — 한 번만 센다
                continue
            seen.add((a, b))
            t = s[a:b]
            if t.lower() in allowed or any(tp.fullmatch(t) and bp.search(s[:a]) and not (na and node_list_end(s[:a]))
                                           for tp, bp, na in allowed_pat):
                continue
            if any(rv['token'] == t and rv['file'] == f and rv['context'] in s for rv in reviewed):
                continue
            if ARGS.trace:
                trace.append(dict(text=s, file=f, start=a, span=t, expr='#residual'))
            r = residual.setdefault(t, dict(token=t, morpheme=m, count=0, sample=f'{f}:{p} …{s[max(0, a - 20):b + 20]}…'))
            r['count'] += 1
if ARGS.trace:
    json.dump(trace, open(ARGS.trace, 'w'), ensure_ascii=False)

# ───────── 3. 노드 = 트리 + 추가 ─────────
parent = {t['name']: t['parent'] for t in TREE}
status = {t['name']: ('added_oq206' if t['added_oq206'] else 'tree') for t in TREE}
order = [t['name'] for t in TREE]
for a in DEC['node_additions']:
    if a['name'] in parent or a['parent'] not in parent:
        fail(f'추가 노드 {a["name"]} — 이미 있거나 상위 {a["parent"]} 없음')
    parent[a['name']], status[a['name']] = a['parent'], 'added_step3'
    order.append(a['name'])
if set(DEC['node_ids']) != set(parent) or set(DEC['nodes']) != set(parent):
    fail('node_ids · nodes 와 트리 + 추가가 다름')
if len(set(DEC['node_ids'].values())) != len(parent):
    fail('node_ids 겹침')

# ───────── 4. 문자열 행선지 ─────────
oot = {o['name']: o for o in DEC['out_of_tree']}
oos_keys = [x['key'] for x in DEC.get('strings_out_of_scope', {}).get('strings', [])]  # v5 — 설명 문장 칸에만 있던 결정(셈 밖)
route = {}
for s in DEC['strings']:
    k = tuple(s['key'])
    if k in route:
        fail(f'결정 문자열 중복 {k}')
    route[k] = s
strings, deferred, opened = [], [], []
for k in sorted(found, key=lambda k: (k[1], k[0])):
    c = found[k]
    s = route.get(k)
    row = dict(string=c['variants'].most_common(1)[0][0], normalized=k[0], group=k[1], count=c['count'],
               count_name_fields=c['count_name_fields'], variants=dict(c['variants']), by_file=dict(c['by_file']),
               name_field_samples=c['name_field_samples'], prose_samples=c['prose_samples'])
    if s is None:
        row.update(destination='open')
        opened.append(dict(type='결정 없는 문자열', key=list(k), string=row['string'], count=row['count'], sample=(c['name_field_samples'] + c['prose_samples'])[:1]))
        strings.append(row)
        continue
    row.update({x: s.get(x) for x in ('destination', 'nodes', 'kind', 'synonym_type', 'handoff', 'deferred_stage', 'weak', 'out_of_tree', 'decided_by', 'note', 'question')})
    bad = None
    if s['destination'] == 'node':
        if not s['nodes'] or any(n not in parent for n in s['nodes']):
            bad = f"노드 {s['nodes']} 없음"
    elif s['destination'] == 'deferred':
        if not s['deferred_stage']:
            bad = 'deferred 단계 없음'
    else:
        bad = f"destination {s['destination']}"
    if s['destination'] == 'node' and bool(s['handoff']) != (s['kind'] == '부위+다른 축(D-07)'):
        bad = f"kind {s['kind']} ↔ handoff {'있음' if s['handoff'] else '없음'} 불일치"
    if s.get('out_of_tree'):
        o = oot.get(s['out_of_tree'])
        if o is None or list(k) not in o['strings']:
            bad = f"트리 밖 결정 {s['out_of_tree']} 와 안 맞음"
        elif o['resolution_type'] == 'not_site' and s['destination'] != 'deferred':
            bad = '트리 밖 부위 아님 결정인데 노드로 감'
        elif o['resolution_type'] != 'not_site' and s['nodes'] != [o['node']]:
            bad = f"트리 밖 결정 노드 {o['node']} ≠ {s['nodes']}"
    if bad:
        row['destination'] = 'open'
        opened.append(dict(type='행선지 오류', key=list(k), string=row['string'], reason=bad))
    strings.append(row)
    if row['destination'] == 'deferred':
        deferred.append(dict(string=row['string'], key=list(k), count=row['count'], stage=row['deferred_stage'], parts=row['handoff'], decided_by=row['decided_by']))
for t in residual.values():
    opened.append(dict(type='사전 밖 부위 형태소', **t))
stale = [s['key'] for s in DEC['strings'] if tuple(s['key']) not in found]
stale += [['residual_reviewed', rv['context']] for rv in DEC.get('residual_reviewed', [])
          if not any(rv['file'] == f and rv['context'] in s for f, p, s in src)]
for o in DEC['out_of_tree']:
    for k in o['strings']:
        if tuple(k) not in route and k not in oos_keys:
            opened.append(dict(type='트리 밖 결정 문자열에 행선지 없음', key=k, string=k[0]))

# ───────── 5. 노드 속성 ─────────
by_node = collections.defaultdict(list)
for s in strings:
    if s['destination'] == 'node':
        for n in s['nodes']:
            by_node[n].append(s)
out_nodes = []
for name in order:
    a = DEC['nodes'][name]
    ss = by_node.get(name, [])
    if not a['anatomical_en'] or not a['anatomical_level']:
        opened.append(dict(type='해부학 이름 후보 없음', string=name))
    if not ss and not a.get('name_field_exception'):
        opened.append(dict(type='원천 문자열 0', string=name))
    syn = lambda s: dict(text=s['string'], key=[s['normalized'], s['group']], type=s['kind'] + (f" · {s['synonym_type']}" if s['synonym_type'] else ''),
                         count=s['count'], count_name_fields=s['count_name_fields'], weak=s['weak'])
    out_nodes.append(dict(
        id=DEC['node_ids'][name], name=name, parent=parent[name], status=status[name],
        synonyms=[syn(s) for s in ss if not s['handoff']],
        compound_strings=[dict(syn(s), handoff=[h['part'] + ' → ' + h['stage'] for h in s['handoff']]) for s in ss if s['handoff']],
        name_field_exception=a.get('name_field_exception'), handoff_note=a.get('handoff_note'),
        anatomical_before_v5=a.get('anatomical_before_v5'),
        anatomical_name=dict(en=a['anatomical_en'], ko=a['anatomical_ko'], basis=a['anatomical_basis'], level=a['anatomical_level']),
        danger_zone=dict(zone=a['danger_zone'], relation=a['danger_zone_relation'], basis=a['danger_zone_basis']),
        source=dict(strings=len(ss), count=sum(s['count'] for s in ss), count_name_fields=sum(s['count_name_fields'] for s in ss)),
        weak_strings=sum(1 for s in ss if s['weak']), note=a['note']))
node_by_name = {n['name']: n for n in out_nodes}
for z in DEC['danger_zone_mapping']:  # W3: 결정 대응을 노드가 실제로 갖는지
    if node_by_name.get(z['node'], {}).get('danger_zone', {}).get('zone') != z['zone']:
        opened.append(dict(type='위험 부위 대응 불일치', string=f"{z['zone']} → {z['node']}"))

# ───────── 6. 근거 약 대조(W3) — 조사 판 weak 문자열이 결정에서 약인지 ─────────
weak_by_norm = collections.defaultdict(set)
for s in DEC['strings']:
    weak_by_norm[s['key'][0]].add(bool(s['weak']))
for r in RES['rows']:
    if r['weak'] and r['normalized'] in weak_by_norm and True not in weak_by_norm[r['normalized']]:
        opened.append(dict(type='조사 판 근거 약이 결정에서 빠짐', string=r['string'], key=[r['normalized'], r['group']]))

# ───────── 7. 의료진 질문 ─────────
dq = []
for s in strings:
    if s.get('weak'):
        dq.append(dict(id=f"{s['normalized']}|{s['group']}", kind='근거 약 문자열(B4)', string=s['string'], value=' · '.join(s['nodes']),
                       question=s.get('question') or DEC['weak_string_question_template'].format(string=s['string'], nodes=' · '.join(s['nodes']))))
WA = DEC['doctor_questions_weak_anatomical']
for n in out_nodes:
    if n['anatomical_name']['level'] == WA['level']:
        dq.append(dict(id=n['id'], kind=WA['kind'], string=n['name'], value=f"{n['anatomical_name']['en']} · {n['anatomical_name']['ko']}",
                       question=WA['template'].format(name=n['name'], en=n['anatomical_name']['en'], ko=n['anatomical_name']['ko'])))
dq += [dict(q) for q in DEC['doctor_questions_extra']]

# ───────── 8. 셈 ─────────
dest = collections.Counter(s['destination'] for s in strings)
summary = dict(
    source=dict(path=str(SRC), files=len(glob.glob(str(SRC / DEC['source']['glob']))), string_fields=n_fields_all, string_fields_counted=len(src)),
    nodes=len(out_nodes), nodes_by_status=dict(collections.Counter(n['status'] for n in out_nodes)),
    strings=len(strings), occurrences=sum(s['count'] for s in strings),
    to_node=dict(strings=dest['node'], occurrences=sum(s['count'] for s in strings if s['destination'] == 'node'),
                 synonyms=sum(len(n['synonyms']) for n in out_nodes), compound=sum(len(n['compound_strings']) for n in out_nodes)),
    deferred=dict(strings=dest['deferred'], occurrences=sum(d['count'] for d in deferred),
                  by_stage=dict(sorted(collections.Counter(d['stage'] for d in deferred).items(), key=lambda kv: -kv[1]))),
    open=len(opened), open_by_type=dict(collections.Counter(o['type'] for o in opened)), stale_decisions=len(stale),
    residual_tokens_allowed=len(allowed),
    weak_strings=sum(1 for s in strings if s.get('weak')),
    anatomical_level=dict(collections.Counter(n['anatomical_name']['level'] for n in out_nodes)),
    doctor_questions=len(dq), doctor_questions_by_kind=dict(collections.Counter(q['kind'] for q in dq)),
    changed=len(DEC.get('changes', [])))
J = dict(version=DEC['version'], decision_ref=DEC['decision_ref'], revision=DEC.get('revision'),
         inputs=['step3-decisions.json', DEC['lexicon'], f"{DEC['tree_source']['file']} {DEC['tree_source']['key']}", str(SRC), 'step3-research.json(근거 약 대조만)'],
         summary=summary, nodes=out_nodes, strings=strings, deferred=deferred, open=opened, stale_decisions=stale,
         doctor_questions=dq, changes=DEC.get('changes', []), boundary_rules=DEC['boundary_rules'], danger_zone_mapping=DEC['danger_zone_mapping'])
json.dump(J, open(OUT / 'step3-sites.json', 'w'), ensure_ascii=False, indent=1)

# ───────── 9. md ─────────
S = summary
L = []
P = L.append
P('---\ntype: silver\nid: step3-sites\ntitle: "실버 3단계 — 부위 원장"\nproduct: procedure-hub\nfeature: phub-recommend\n'
  f"decision: \"{DEC['decision_ref']}\"\nrevision: \"{DEC.get('revision', '')}\"\ngenerated_by: step3-apply.py\ndata: step3-sites.json\n---\n")
P('# 실버 3단계 — 부위 원장\n')
P(f"> **기준(v5)**: 부위 = 「어디에 맞냐」 — 시술 받는 사람이 말하는 자리, 사람 몸 겉(체표)에서 가리킬 수 있는 자리. 뼈 · 근육 · 혈관 · 조직층은 부위가 아니다. **원천은 이름 칸 {len(name_fields)}개만**(`step3-decisions.json` name_fields) — 설명 문장 칸의 해부 낱말은 세지 않는다. 노드 이름 2벌: 일반인 용어 = 노드 이름 · 전문의 용어 = 겉자리 이름(근육 · 뼈 이름은 4단계 넘김 메모).\n")
P('## 셈\n')
st_ko = {'tree': 'DEC-002 트리', 'added_oq206': 'OQ-206 추가', 'added_step3': '3단계 추가'}
P(f"- 원천: `{S['source']['path']}` JSON {S['source']['files']}개 · 문자열 칸 {S['source']['string_fields']:,} 중 **이름 칸 {len(name_fields)}종의 {S['source']['string_fields_counted']:,}칸만** 셈")
B = DEC.get('rescope_before')
if B:
    P(f"- **범위 바로잡기 전 → 후**: 문자열 {B['strings']} → {S['strings']} · 등장 {B['occurrences']:,} → {S['occurrences']:,}회 · 노드로 {B['to_node']['strings']} → {S['to_node']['strings']} · 넘김 {B['deferred']['strings']} → {S['deferred']['strings']} · 근거 약 {B['weak_strings']} → {S['weak_strings']} · 의료진 질문 {B['doctor_questions']} → {S['doctor_questions']}. "
      f"설명 문장 칸에만 나오던 결정 {len(oos_keys)}행은 `strings_out_of_scope`(셈 밖 · 기록만)")
P(f"- **노드 {S['nodes']}** = " + ' · '.join(f"{st_ko[k]} {v}" for k, v in S['nodes_by_status'].items()))
P(f"- **원천 부위 문자열 {S['strings']} · 등장 {S['occurrences']:,}회** — 노드로 {S['to_node']['strings']}({S['to_node']['occurrences']:,}회 · 동의어 칸 {S['to_node']['synonyms']} · 부위+다른 축 칸 {S['to_node']['compound']}) · 단계로 넘김 {S['deferred']['strings']}({S['deferred']['occurrences']:,}회)")
P('  - 넘김 단계별: ' + ' · '.join(f"{k} {v}" for k, v in S['deferred']['by_stage'].items()))
P(f"- **open {S['open']}**" + (f" — {S['open_by_type']}" if S['open'] else f' — 결정 없는 문자열 0 · 사전 밖 부위 형태소 잔여 0(허용 목록 대조) · 행선지 오류 0 · 위험 부위 대응 {len(DEC['danger_zone_mapping'])} 일치 · 조사 판 근거 약 누락 0'))
P(f"- **근거 약 {S['weak_strings']}문자열** · 해부학 이름 수준 " + ' · '.join(f"{k} {v}" for k, v in S['anatomical_level'].items()))
P(f"- **의료진 질문 {S['doctor_questions']}** = " + ' + '.join(f"{k} {v}" for k, v in S['doctor_questions_by_kind'].items()))
P(f"- 이번 판에서 바뀐 것 {S['changed']}건(아래 「바뀐 행」) · 원천에 없는 결정 문자열 {S['stale_decisions']}\n")
P(f"> 결정 `step3-decisions.json`(행선지 · 노드 속성) · 사전 `{DEC['lexicon']}` · 재현 `python3 step3-apply.py`. 새 원천이 들어오면 사전에 잡혔는데 결정에 없는 문자열 · 사전 밖 부위 형태소가 open 으로 나온다 — 결정 · 사전 · 허용 목록에 더하면 닫힌다.\n")
P('## 바뀐 행(검수 반영)\n')
P('| 판 | 문자열(키) | 바뀐 것 |\n|---|---|---|')
for c in DEC.get('changes', []):
    P(f"| {c['version']} | {' · '.join(c['key'])} | {c['change']} |")
P('\n## 노드\n')
P('| id | 일반인 용어(노드 이름) | 상위 | 상태 | 동의어(등장) | 부위+다른 축 → 넘김 | 전문의 용어 — 겉자리 이름(수준) | 위험 부위 | 이름 칸 근거(문자열 · 등장) |\n|---|---|---|---|---|---|---|---|---|')
for n in out_nodes:
    syn = ' · '.join(f"{'⚠' if s['weak'] else ''}{s['text']}({s['count']})" for s in n['synonyms']) or '—'
    cmp_ = ' · '.join(f"{'⚠' if s['weak'] else ''}{s['text']}({s['count']}) → {' / '.join(s['handoff'])}" for s in n['compound_strings']) or '—'
    a = n['anatomical_name']
    z = f"`{n['danger_zone']['zone']}` {n['danger_zone']['relation']}" if n['danger_zone']['zone'] else (n['danger_zone']['relation'] or '—')
    P(f"| `{n['id']}` | {n['name']} | {n['parent'] or '—'} | {st_ko[n['status']]} | {syn} | {cmp_} | {a['en']} · {a['ko']} (**{a['level']}**) | {z} | {n['source']['strings']} · {n['source']['count']}{' — 예외: ' + n['name_field_exception'] if n['name_field_exception'] else ''} |")
P('\n⚠ = 근거 약(B4). 해부학 이름 근거 원문은 json `nodes[].anatomical_name.basis`. 수준 강 = 레포 파일에 그 이름이 있음(위험 부위 파일은 AI 합의본 — 의학 확정 아님) · 중 = 레포 일부 · 약 = 레포 밖 표준 용어집만. 확정은 의료진(OQ-202).\n')
P('## 전문의 용어에서 뺀 근육 · 뼈 이름 → 4단계 넘김 메모(추가 지시 7)\n')
P('| 노드 | 이전 전문의 용어 | 지금(겉자리) | 넘김 메모 |\n|---|---|---|---|')
for n in out_nodes:
    if n['handoff_note']:
        b = n['anatomical_before_v5'] or {}
        P(f"| {n['name']} | {b.get('ko', '')} · {b.get('en', '')} ({b.get('level', '')}) | {n['anatomical_name']['ko']} · {n['anatomical_name']['en']} (**{n['anatomical_name']['level']}**) | {n['handoff_note']} |")
P('\n' + DEC['node_naming']['kept_note'] + '\n')
P('## 트리 밖 결정이 보낸 문자열\n')
P('| 이름 | 결정 | 행선지 | 문자열(등장) |\n|---|---|---|---|')
for o in DEC['out_of_tree']:
    ss = [s for s in strings if [s['normalized'], s['group']] in o['strings']]
    to = o['node'] if o['resolution_type'] != 'not_site' else o['deferred_stage']
    P(f"| {o['name']} | {o['bundle']} {o['resolution']} | {to} | " + ' · '.join(f"{s['string']}({s['count']})" for s in ss) + ' |')
P('\n## 단계로 넘김(deferred)\n')
P('| 단계 | 문자열(등장) |\n|---|---|')
for stg in S['deferred']['by_stage']:
    ds = sorted([d for d in deferred if d['stage'] == stg], key=lambda d: (-d['count'], d['string']))
    P(f"| {stg} ({len(ds)}) | " + ' · '.join(f"{d['string']}({d['count']})" for d in ds) + ' |')
P('\n## 경계 규칙(B8 · W7)\n')
P('| 경계 | 원천 문자열이 가는 곳 |\n|---|---|')
for b in DEC['boundary_rules']:
    P(f"| {b['rule']} | {b['decision']} |")
P('\n## 위험 부위 대응(B9 — 최종 의료진)\n')
P('| zone | 노드 | 판정 | 근거 |\n|---|---|---|---|')
for z in DEC['danger_zone_mapping']:
    P(f"| `{z['zone']}` | {z['node']} | {z['verdict']} | {z['basis']} |")
P(f"\n## 의료진 질문 {len(dq)}\n")
P('| 종류 | 문자열 · 노드 | 둔 값 | 질문 |\n|---|---|---|---|')
for q in dq:
    P(f"| {q['kind']} | {q['string']} | {q['value']} | {q['question']} |")
FX = W / 'step3-fixtures' / 'result.json'
if FX.exists() and not ARGS.source:
    fx = json.load(open(FX))
    P(f"\n## 고정 시험(fixture) — {fx['passed']}/{fx['total']} 통과\n")
    P(f"`python3 step3-fixture-test.py` — 원천 사본에 문장 파일 하나씩 붙이거나 결정 한 줄을 빼고 돌려 open 이 기대와 같은지 본다. 사례 `step3-fixtures/cases.json`.\n")
    P('| 사례 | 종류 | 넣은 것 | 기대 open | 실제 open | 결과 |\n|---|---|---|---|---|---|')
    for c in fx['cases']:
        P(f"| {c['id']} | {c['type']} | {c['input']} | {' · '.join(c['expect']) or '없음'} | {' · '.join(c['actual']) or '없음'} | {'PASS' if c['pass'] else 'FAIL'} |")
P(f"\n## 알려진 한계 — 사람이 찾는 몫\n")
P("이 원장이 기계로 보장하는 것은 **이름 칸 · 사전 · 잔여 형태소 · 허용 목록 안**에서다. 아래는 open 으로 나오지 않을 수 있어 새 원천 때 사람이 본다.\n")
P("- **이름 칸 밖의 부위 표현** — 설명 문장 칸(작용기전 · 적응증 설명 · 부작용 · 문헌 · 안전 본문 · 사후관리)은 세지 않는다(기준). 새 원천에서 이름 칸이 늘거나(새 파일 · 새 키) 부위가 설명 칸에만 적힌 시술이 생기면 `step3-decisions.json` name_fields 에 칸을 더해야 잡힌다.")
P("- **사전 · 잔여 형태소 밖 신조어 · 구어** — 이름 칸 안이라도 사전 패턴 · 잔여 형태소와 글자가 겹치지 않으면 조용히 빠진다.")
P("- **같은 표면 다른 뜻** — 행선지는 키(정규형 · 사전 무리) 단위라 같은 글자는 같은 곳으로 간다.")
P(f"\n## open {len(opened)}\n")
P('없음.' if not opened else '\n'.join(f"- {o}" for o in opened))
P(f"\n## 잔여 검사 허용 목록\n\n사전 밖 부위 형태소 {len(RS['morphemes_ko'])}(한글) · 패턴 {len(RS.get('morpheme_patterns_ko', []))} · {len(RS['stems_en'])}(영문 어간)로 **이름 칸만** 다시 훑는다. 아래는 글자만 겹치는 낱말(허용 · {len(allowed)}개) — 무리별 이유는 `{DEC['lexicon']}` residual.allowed.\n")
for g in RS['allowed']:
    P(f"- **{g['reason']}** ({len(g['tokens'])})")
P(f"\n사람이 문맥을 보고 닫은 잔여(`step3-decisions.json` residual_reviewed) {len(reviewed)}: " + (' · '.join(f"「{r['context']}」 — {r['verdict']}" for r in reviewed) or '없음'))
open(OUT / 'step3-sites.md', 'w').write('\n'.join(L) + '\n')

# ───────── 10. 원천 · 문서 수정 목록(직접 고치지 않음) ─────────
F = DEC['source_fix']
L = ['---\ntype: fix-list\nid: step3-source-fix\ntitle: "3단계 — DEC-002 근거 표 정정 · 원천 수정 후보"\ngenerated_by: step3-apply.py\n---\n',
     '# 3단계 — DEC-002 근거 표 정정 · 원천 수정 후보\n',
     f"> 결정: {DEC['decision_ref']} (B11 · B12). 이 목록만 낸다 — DEC-002.md · 원천은 고치지 않았다.\n",
     f"## B11 DEC-002 근거 표 정정 {len(F['B11'])}\n", '| # | 대상 | 지금 | 고칠 것 |', '|---|---|---|---|']
L += [f"| {i} | {x['target']} | {x['now']} | {x['fix']} |" for i, x in enumerate(F['B11'], 1)]
L += [f"\n## B12 원천 수정 후보 {len(F['B12'])}\n", '| # | 파일 | 키 | 지금 | 고칠 것 | 근거 수준 |', '|---|---|---|---|---|---|']
L += [f"| {i} | `{x['file']}` | {x['key']} | {x['now']} | {x['fix']} | {x['level']} |" for i, x in enumerate(F['B12'], 1)]
if F['B12'] and F['B12'][0].get('scope_note'):
    L += [f"\n> B12 는 {F['B12'][0]['scope_note']}."]
if F.get('withdrawn_v5'):
    L += [f"\n## 철회 {len(F['withdrawn_v5'])} (v5 범위 바로잡기)\n", '| 대상 | 그때 고칠 것 | 철회 이유 |', '|---|---|---|']
    L += [f"| {x['target']} | {x['fix']} | {x['reason']} |" for x in F['withdrawn_v5']]
k = F['known']
L += [f"\n참고(이미 목록에 있음): `{k['file']}` {k['key']} — {k['now']} · {k['note']}"]
open(OUT / 'step3-source-fix.md', 'w').write('\n'.join(L) + '\n')
print(json.dumps({k: summary[k] for k in ('nodes', 'strings', 'occurrences', 'to_node', 'deferred', 'open', 'open_by_type', 'stale_decisions', 'weak_strings', 'doctor_questions', 'doctor_questions_by_kind')}, ensure_ascii=False))
