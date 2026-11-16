"""실버 6단계(패키지) 반영 — 결정론(3 · 4 · 5단계와 같은 구조).

입력: step6-decisions.json(결정 — 패키지 · 구성 · 묶음 이름 · 넘겨받은 것 · 원천 질문 · 원천 수정 후보)
      원천(결정 source.path) taxonomy · market-pricing · synergy
      step5-units.json(읽기만 — 단위 시술 키 · 원장 행선지 · 시장가 kind · handoffs)
출력: step6-packages.json · step6-packages.md · step6-origin-questions.md · step6-source-fix.md

패키지 원천 행 = 5단계 원장 「6단계 패키지」 행 + 5단계 시장가 「6단계 패키지」 행. 원천 행인데 결정에 없으면 open[].
구성은 단위 시술 키(5단계) 또는 슬롯(원문 · 후보 · 원천 질문). 키도 질문도 없는 구성 · 구성 없는 패키지 = open.
묶음 이름(taxonomy 하위)은 노드 · 엣지를 만들지 않는다 — 7단계 목적 원문 / 패키지 속성.
synergy 대조는 8단계 메모(step6-to-step8-notes)만 — 엣지를 만들지 않는다. 숫자는 이 파일에 적지 않는다(고정 assert 없음).
"""
import argparse
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
AP = argparse.ArgumentParser()
AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
AP.add_argument('--decisions', default=str(W / 'step6-decisions.json'))
AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
ARGS = AP.parse_args()
OUT = Path(ARGS.out)
DEC = json.load(open(ARGS.decisions))
SRC = Path(ARGS.source or DEC['source']['path'])
J = lambda p: json.load(open(p))
S5 = J(W / DEC['canon']['step5'])
TAX = J(SRC / 'taxonomy.json')
MKT = J(SRC / 'market-pricing.json')
SYN = J(SRC / 'synergy.json')['links']

OPEN, STALE = [], []


def op(t, **kw):
    OPEN.append(dict(type=t, **kw))


# ───────── 0. 정본 · 원천 ─────────
UNITS = {u['id']: u for u in S5['units']}
ITEMS = {i['id']: (m['id'], s['id'], i) for m in TAX['modality'] for s in m['subcategories'] for i in s['items']}
SUBS = {s['id']: (m['id'], s) for m in TAX['modality'] for s in m['subcategories']}
MROWS = {i['name']: (c['id'], i) for c in MKT['categories'] for i in c['items']}
OQ = {q['id']: q for q in DEC['origin_questions']}
KINDS = set(DEC['kinds'])

# 패키지 원천 행 — 5단계가 6단계로 넘긴 원장 행 · 시장가 행
src_ledger = [r for r in S5['ledger'] if r['dest'] == '6단계 패키지']
src_market = [r for r in S5['market'] if r['kind'] == '6단계 패키지']
for b in DEC['backport_step5']:  # U1 · U2 — 5단계 단위 시술로 돌린 행은 6단계 원천이 아님
    r = next((x for x in S5['ledger'] if x['id'] == b['ledger_id']), None)
    if r is None or r['dest'] == '6단계 패키지' or b['to'] not in r['units']:
        op('5단계 보강 안 됨', id=b['ledger_id'], name=b['name'], to=b['to'])

# ───────── 1. 패키지 ─────────
packages, edges, slots, notes8 = [], [], [], []
covered_l, covered_m = collections.Counter(), collections.Counter()
for d in DEC['packages']:
    if d['kind'] not in KINDS:
        op('패키지 kind 값 밖', id=d['id'], kind=d['kind'])
    p = dict(id=d['id'], name=d['name'], kind=d['kind'], shape=d['shape'], menu_group=d.get('menu_group'), same_day_raw=d['same_day_raw'],
             recommendable=d['recommendable'], synonyms=[], price=[], description=None, notes=d.get('notes') or [], decided_by=d['decided_by'],
             source_fix=d.get('source_fix'), research_id=d.get('research_id'))
    if d['kind'] == '병원 시그니처' and d['recommendable']:
        op('병원 시그니처인데 추천 노출', id=d['id'])
    if d['source'] == 'ledger':
        lid = d['ledger_id']
        covered_l[lid] += 1
        if lid not in ITEMS:
            op('패키지 원장 항목이 원천에 없음', id=lid)
            continue
        fam, sub, it = ITEMS[lid]
        if it['name'] != d['name']:
            op('패키지 원장 이름 바뀜', id=lid, decision=d['name'], source=it['name'])
        p.update(ledger_id=lid, source_family=fam, source_sub=sub, detail_raw=it.get('detail'))
        p['synonyms'].append(dict(text=it['name'], type='원장 이름', src=lid))
        if d.get('price_raw'):
            if d['price_raw'] not in (it.get('detail') or ''):
                op('패키지 가격 원문이 원천 detail 에 없음', id=lid, price=d['price_raw'])
            p['price'].append(dict(src='원장 detail', raw=d['price_raw']))
        ex = it.get('extracted') or {}
        p['description'] = {k: ex.get(k) for k in ('overview', 'mechanism', 'onset_duration') if ex.get(k)}
    else:
        for n in d['market_names']:
            covered_m[n] += 1
            if n not in MROWS:
                op('패키지 시장가 행이 원천에 없음', name=n)
                continue
            cat, it = MROWS[n]
            p['synonyms'].append(dict(text=n, type='시장가 이름', src=f'market-pricing {cat}'))
            p['price'].append(dict(src=f'market-pricing {cat}', name=n, unit_raw=it.get('unit'), low=it.get('low'), mid=it.get('mid'), high=it.get('high'), currency=MKT.get('currency')))
        p['source_family'] = MROWS[d['market_names'][0]][0] if d['market_names'][0] in MROWS else None
    if not d['components']:
        op('패키지인데 구성 없음', id=d['id'], name=d['name'])
    for i, c in enumerate(d['components']):
        base = dict(package=d['id'], package_name=d['name'], order=i + 1, text=c['text'], basis=c['basis'], quantity_raw=c.get('quantity_raw'), sessions=c.get('sessions'))
        for u in [c.get('unit')] + (c.get('candidates') or []):
            if u and u not in UNITS:
                op('결정이 가리키는 키 없음', where=d['id'], unit=u)
        q = c.get('origin_question')
        if q and q not in OQ:
            op('결정이 가리키는 원천 질문 없음', where=d['id'], question=q)
            q = None  # 없는 질문은 질문 없음으로 센다
        if c.get('unit'):
            if c.get('evidence_level') == '약' and not q:
                op('근거 약 구성인데 원천 질문 없음', id=d['id'], text=c['text'])
            edges.append(dict(base, unit=c['unit'], unit_name=UNITS.get(c['unit'], {}).get('name'), evidence_level=c.get('evidence_level'),
                              candidates=c.get('candidates'), origin_question=q))
        else:
            if not q:
                op('구성 키도 질문도 없음', id=d['id'], text=c['text'])
            slots.append(dict(base, candidates=c.get('candidates') or [], candidate_names=[UNITS[u]['name'] for u in c.get('candidates') or [] if u in UNITS],
                              origin_question=q, missing_unit=c.get('missing_unit')))
    for s in d.get('step8_notes') or []:
        for li in s['links']:
            if li >= len(SYN):
                op('synergy 링크 번호 없음', id=d['id'], link=li)
        notes8.append(dict(package=d['id'], name=d['name'], pair=s['pair'], verdict=s['verdict'],
                           links=[dict(i=li, **{k: SYN[li][k] for k in ('from', 'to', 'type', 'timing')}) for li in s['links'] if li < len(SYN)]))
    p['components'] = sum(1 for e in edges if e['package'] == d['id']) + sum(1 for s in slots if s['package'] == d['id'])
    packages.append(p)
for r in src_ledger:
    if covered_l[r['id']] == 0:
        op('결정 없는 패키지 원천 행', id=r['id'], name=r['name'])
for r in src_market:
    if covered_m[r['name']] == 0:
        op('결정 없는 패키지 원천 행', name=r['name'])
for k, v in list(covered_l.items()) + list(covered_m.items()):
    if v > 1:
        op('패키지 원천 행 겹침', id=k)
STALE += [['packages', k] for k in covered_l if k not in {r['id'] for r in src_ledger}]
STALE += [['packages', k] for k in covered_m if k not in {r['name'] for r in src_market}]

# ───────── 2. 묶음 이름(노드 · 엣지 없음) ─────────
NP = {n['id']: n for n in DEC['non_packages']}
non_packages = []
for n in DEC['non_packages']:
    if n['id'] not in SUBS:
        STALE.append(['non_packages', n['id']])
        continue
    fam, s = SUBS[n['id']]
    if s['label'] != n['label']:
        op('묶음 이름 바뀜', id=n['id'], decision=n['label'], source=s['label'])
    non_packages.append(dict(n, family=fam, items=len(s['items'])))
mg = {p['menu_group'] for p in packages if p['menu_group']}
# 묶음 이름의 menu_group 행선지 번호 ↔ packages[].menu_group 「라벨」 대조
for n in non_packages:
    if 'menu_group' not in n['to']:
        continue
    named = set()
    for a, b in re.findall(r'P6-(\d+)(?:~(\d+))?', n['to']):
        named |= {f'P6-{i:02d}' for i in range(int(a), int(b or a) + 1)}
    actual = {p['id'] for p in packages if p['menu_group'] and p['menu_group'].endswith(f"「{n['label']}」")}
    if named != actual:
        op('묶음 이름 행선지 번호 어긋남', id=n['id'], to=sorted(named), menu_group=sorted(actual))

# 5단계가 6단계로 넘긴 것(handoffs) — 행선지 있어야
HD = {h['source']: h for h in DEC['handoffs']}
handoffs = []
for h in S5['handoffs']['2단계 deferred']:
    if h['deferred_to'] != '6단계':
        continue
    d = HD.get(h['source'])
    if d is None:
        op('넘겨받은 것 행선지 없음', source='5단계 handoffs', id=h['source'])
        continue
    for c in d['covered_by']:
        if c not in NP:
            op('넘겨받은 것 행선지 키 없음', source=h['source'], id=c)
    handoffs.append(dict(source=h['source'], family=h['family'], covered_by=d['covered_by'], note=d.get('note')))
STALE += [['handoffs', k] for k in HD if k not in {h['source'] for h in S5['handoffs']['2단계 deferred'] if h['deferred_to'] == '6단계'}]

# 원천 질문 — 쓰이지 않는 질문 = stale
used = {e['origin_question'] for e in edges + slots if e.get('origin_question')}
for q in DEC['origin_questions']:
    if q['id'] not in used and not q.get('target') and not q.get('packages'):
        STALE.append(['origin_questions', q['id']])

# ───────── 3. 셈 · 쓰기 ─────────
by_kind = collections.Counter(p['kind'] for p in packages)
summary = dict(source=str(SRC), packages=len(packages), by_kind=dict(by_kind), recommendable=sum(p['recommendable'] for p in packages),
               source_rows=dict(ledger=len(src_ledger), market=len(src_market)),
               edges=len(edges), edges_weak=sum(1 for e in edges if e.get('evidence_level') == '약'), slots=len(slots),
               slots_missing_unit=sum(1 for s in slots if s.get('missing_unit')),
               packages_full=sum(1 for p in packages if p['components'] and all(e['package'] != p['id'] for e in slots)),
               packages_no_edge=[p['id'] for p in packages if not any(e['package'] == p['id'] for e in edges)],
               non_packages=len(non_packages), non_packages_by_to=dict(collections.Counter(n['to'].split('(')[0] for n in non_packages)),
               handoffs=len(handoffs), step8_notes=len(notes8),
               step8_verdicts=dict(collections.Counter(n['verdict'].split(' — ')[0].split('(')[0].strip() for n in notes8)),
               origin_questions=len(DEC['origin_questions']), source_fix=len(DEC['source_fix']),
               open=len(OPEN), open_by_type=dict(collections.Counter(o['type'] for o in OPEN)), stale_decisions=len(STALE))
out = {'version': DEC['version'].replace('decisions', 'packages'), 'generated_by': 'step6-apply.py', 'decision_ref': DEC['decision_ref'],
       'rules': DEC['rules'], 'summary': summary, 'packages': packages, 'contains': edges, 'slots': slots,
       'non_packages': non_packages, 'menu_groups_used': sorted(mg), 'handoffs': handoffs,
       'step6-to-step8-notes': notes8, 'origin_questions': DEC['origin_questions'], 'source_fix': DEC['source_fix'],
       'open': OPEN, 'stale_decisions': STALE}
json.dump(out, open(OUT / 'step6-packages.json', 'w'), ensure_ascii=False, indent=1)

esc = lambda s: str(s if s is not None else '').replace('|', '\\|').replace('\n', ' ')
L = []
P = L.append
s = summary
P('# 실버 6단계 — 패키지 원장\n')
P(f"정본 · `step6-apply.py` 가 `step6-decisions.json` + 원천 + `step5-units.json` 에서 만든다(손으로 고치지 않는다). 결정 근거: {DEC['decision_ref']}\n")
P(f"**패키지 {s['packages']}**(" + ' · '.join(f"{k} {v}" for k, v in s['by_kind'].items()) + f" · 추천 노출 {s['recommendable']}) · "
  f"원천 행 원장 {s['source_rows']['ledger']} · 시장가 {s['source_rows']['market']} · **구성 엣지 {s['edges']}**(근거 약 {s['edges_weak']}) · **슬롯 {s['slots']}**(5단계에 키 없음 {s['slots_missing_unit']}) · "
  f"구성 다 풀린 패키지 {s['packages_full']} · 엣지 0 패키지 {len(s['packages_no_edge'])}({', '.join(s['packages_no_edge'])} — 전부 슬롯 + 원천 질문) · "
  f"묶음 이름 {s['non_packages']}(" + ' · '.join(f"{k} {v}" for k, v in s['non_packages_by_to'].items()) + f") · 넘겨받은 것 {s['handoffs']} · "
  f"8단계 메모 {s['step8_notes']}(" + ' · '.join(f"{k} {v}" for k, v in s['step8_verdicts'].items()) + f") · 원천 질문 {s['origin_questions']} · 원천 수정 후보 {s['source_fix']} · "
  f"**open {s['open']}** · stale {s['stale_decisions']}\n")
fx = W / 'step6-fixtures' / 'result.json'
if fx.exists():
    r = J(fx)
    P(f"고정 시험 {r['passed']}/{r['total']}(결정 빼면 open — `step6-fixture-test.py`)\n")
P('## 1. 패키지\n')
P('| id | 이름 | kind | 꼴 | 메뉴 묶음 | 동의어 | 가격 원문 | 같은 날(원천 문구) | 추천 노출 |')
P('|---|---|---|---|---|---|---|---|---|')
for p in packages:
    pr = ' / '.join(x['raw'] if 'raw' in x else f"{x['name']} {x['low']:,}~{x['high']:,}({x['unit_raw']})" for x in p['price']) or '—'
    P(f"| {p['id']} | {esc(p['name'])} | {p['kind']} | {esc(p['shape'])} | {esc(p['menu_group'] or '—')} | {esc(' · '.join(x['text'] for x in p['synonyms']))} | {esc(pr)} | {esc(p['same_day_raw'])} | {'○' if p['recommendable'] else '✗(기본 제외)'} |")
P('\n## 2. 구성 엣지 — 패키지 → 단위 시술\n')
P('| 패키지 | # | 원문 | 단위 시술 | 수량 · 회차 | 근거 | 원천 질문 |')
P('|---|---|---|---|---|---|---|')
for e in edges:
    P(f"| {e['package']} {esc(e['package_name'])} | {e['order']} | {esc(e['text'])} | {e['unit']} {esc(e['unit_name'])}{' · 근거 약' if e.get('evidence_level') else ''} | {esc(e.get('quantity_raw') or '')} | {esc(e['basis'])} | {e.get('origin_question') or ''} |")
P('\n## 3. 슬롯 — 키로 못 푼 구성\n')
P('| 패키지 | # | 원문 | 후보 키 | 5단계에 없는 키 | 근거 | 원천 질문 |')
P('|---|---|---|---|---|---|---|')
for e in slots:
    P(f"| {e['package']} {esc(e['package_name'])} | {e['order']} | {esc(e['text'])} | {esc(' · '.join(e['candidates']) or '—')} | {esc(e.get('missing_unit') or '')} | {esc(e['basis'])} | {e['origin_question']} |")
P('\n## 4. 묶음 이름 — 노드 · 엣지 없음\n')
P('| taxonomy 하위 | 이름 | 판정 | 행선지 |')
P('|---|---|---|---|')
for n in non_packages:
    P(f"| `{n['id']}` | {esc(n['label'])} | {esc(n['verdict'])} | {esc(n['to'])} |")
P('\n## 5. 넘겨받은 것(5단계 handoffs → 6단계)\n')
for h in handoffs:
    P(f"- {esc(h['source'])} → {', '.join(h['covered_by'])}{' · ' + h['note'] if h.get('note') else ''}")
P('\n## 6. 8단계 메모 — synergy 대조(엣지 아님)\n')
P('| 패키지 | 쌍 | synergy | 판정 |')
P('|---|---|---|---|')
for n in notes8:
    ls = '<br>'.join(f"#{x['i']} {x['from']}→{x['to']} {x['type']} 「{x['timing']}」" for x in n['links']) or '—'
    P(f"| {n['package']} {esc(n['name'])} | {esc(' × '.join(n['pair']))} | {esc(ls)} | {esc(n['verdict'])} |")
P('\n## 7. 원천 설명 · 메모\n')
for p in packages:
    ds = p['description'] or {}
    extra = ' · '.join(p['notes'])
    if ds or extra or p.get('source_fix'):
        P(f"- **{p['id']} {esc(p['name'])}** — {esc(ds.get('overview') or '')}{(' · 메모: ' + esc(extra)) if extra else ''}{(' · 원천 수정 후보: ' + esc(p['source_fix'])) if p.get('source_fix') else ''}")
P(f"\n## 8. open {len(OPEN)} · stale {len(STALE)}\n")
for o in OPEN:
    P(f"- {esc(json.dumps(o, ensure_ascii=False))}")
for x in STALE:
    P(f"- stale {esc(x)}")
open(OUT / 'step6-packages.md', 'w').write('\n'.join(L) + '\n')

Q = ['# 실버 6단계 — 원천 질문(병원)\n', '지금 값(추천)은 넣어 두었다. 답이 오면 그 구성(슬롯 · 엣지)만 다시 판정한다. `step6-apply.py` 산출.\n',
     '| id | 질문 | 패키지 · 대상 |', '|---|---|---|']
for q in DEC['origin_questions']:
    Q.append(f"| {q['id']} | {esc(q['question'])} | {esc(', '.join(q.get('packages') or []) or q.get('target') or '')}{(' · ' + esc(q['target'])) if q.get('target') and q.get('packages') else ''} |")
open(OUT / 'step6-origin-questions.md', 'w').write('\n'.join(Q) + '\n')
F = ['# 실버 6단계 — 원천 수정 후보\n', '원천은 고치지 않는다. 후보만 적는다. `step6-apply.py` 산출.\n', '| 원장 id | 이름 | 칸 | 지금 | 제안 |', '|---|---|---|---|---|']
for f in DEC['source_fix']:
    F.append(f"| `{f['ledger_id']}` | {esc(f['name'])} | {f['field']} | {esc(f['now'])} | {esc(f['proposal'])} |")
open(OUT / 'step6-source-fix.md', 'w').write('\n'.join(F) + '\n')
print(json.dumps(summary, ensure_ascii=False))
