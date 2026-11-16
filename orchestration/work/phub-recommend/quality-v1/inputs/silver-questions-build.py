#!/usr/bin/env python3
"""실버 질문 페이지 v3 — 지금 파일에서 질문을 다시 뽑아 silver-questions.json · .html 를 고친다(결정론 · 두 번 실행해도 같음).

python3 silver-questions-build.py
- 있던 항목(v2): 원 id 가 지금 판 원천 질문 파일에 남아 있으면 그대로(id 같음 — db answers/<id> 가 이어짐) · 없으면 removed_ids 로
- 8단계 항목은 질문 문구 · 걸린 행을 지금 판 step8-relations.json origin_questions 로 다시 씀
- 새 항목: step8 Q8-19(부작용 예외 9 · semantic.json U2) · step7 Q7-03(흉터 필러 · R26) · step7 R27 원천 수정 후보(갈래 목록 복사 · 갈래마다 1)
- 스타일 · 저장 방식은 html 그대로 — <script id="data"> 만 바꾼다. 실버 · 시맨틱 json 은 읽기만.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f), encoding='utf-8'))
T = lambda f: open(os.path.join(HERE, f), encoding='utf-8').read()
QJ, QH = os.path.join(HERE, 'silver-questions.json'), os.path.join(HERE, 'silver-questions.html')

Q = J('silver-questions.json')
S3, S7, S8, SEM = J('step3-sites.json'), J('step7-concerns.json'), J('step8-relations.json'), J('semantic.json')
MD = {1: T('step1-origin-questions.md'), 2: T('step2-origin-questions.md'), 5: T('step5-origin-questions.md'), 6: T('step6-origin-questions.md')}
Q7 = {q['id']: q for q in S7['origin_questions']}
Q8 = {q['id']: q for q in S8['origin_questions']}
S3Q = json.dumps(S3.get('doctor_questions') or [], ensure_ascii=False)
SE = {x['id']: x for x in S8['safety']['side_effects']}
FAMN = {f['id']: f['name'] for f in J('step2-families.json')['families']}
CLM = {c['id']: c for c in S8['claims']}
X8 = {x['id']: x for x in S8['conflicts']}
EDG = {e['id']: e for e in S8['edges']}


def x8_block(xid):
    """10-30 충돌 하나로 — 진짜 반대(R5) X8 하나 → 원문 나란히 + 지금 앱 값(순서 단정 안 함 · 간격 더 긴 쪽)."""
    x = X8[xid]
    nm = lambda f: f"{FAMN.get(f, f)}({f})"
    sides = {}
    for sd in (x['sides'], x.get('sides_from_bundle') or {}):
        for k, lst in sd.items():
            sides.setdefault(k, [])
            sides[k] += [c for c in lst if c not in sides[k]]
    out = []
    for i, (k, lst) in enumerate(sorted(sides.items())):
        out.append({'k': chr(65 + i), 'label': f"{nm(k)} 먼저", 'lines': [f"[{CLM[c]['source']}] {short(CLM[c]['text'], 300)}" for c in lst]})
    fam_edge = next((e for e in S8['edges'] if sorted([e['a'], e['b']]) == sorted([f'family:{p}' for p in x['pair']])), None)
    r = (fam_edge or {}).get('resolved') or {}
    d = r.get('days') or next((o.get('days') for o in r.get('options') or [] if o['field'] == 'days' and o.get('days')), None)
    now = '지금 앱 값: 순서 단정 안 함(R5)' + (f" · 간격 {d[0]:g}~{d[1]:g}일(더 긴 쪽 · R3)" if d else '') + f" · 걸린 엣지 · 쌍 {len(x['resolution']['where'])}"
    return {'id': xid, 'title': f"순서 — {nm(x['pair'][0])} ↔ {nm(x['pair'][1])} 어느 쪽이 먼저" + (' (묶음 원칙 포함)' if x.get('sides_from_bundle') or x.get('from_bundle') else ''),
            'sides': out, 'now': now}

V3_GROUPS = {'s8-Q8-19', 's7-oq-Q7-03', 's8-Q8-20'}       # 이 빌드가 만드는 항목(다시 돌리면 새로 씀) · s7-Q7-03 은 v1 게이트 항목이 쓴 id(빠짐) — 옛 답이 붙지 않게 새 id
is_v3 = lambda i: i['id'] in V3_GROUPS or i['id'].startswith('s7-R27-')


def still_open(it):
    """원 id 가 지금 판 원천 질문에 남아 있나 — (열림?, 근거)."""
    for o in it['orig_ids']:
        for s in it['stages']:
            if s in MD and o in MD[s]:
                return True, f"{s}단계 원천 질문 md 에 {o} 남음"
            if s == 3 and o.split('|')[0] in S3Q:
                return True, f"step3-sites.json doctor_questions 에 {o} 남음"
            if s == 7 and o in Q7:
                return True, f"step7-concerns.json origin_questions 에 {o} 남음"
            if s == 8 and o in Q8:
                return True, f"step8-relations.json origin_questions 에 {o} 남음"
    ret = [r for r in S8.get('origin_questions_retired') or [] if r['id'] in it['orig_ids']]
    if ret:
        return False, f"원 id {ret[0]['id']} — 10-30 충돌 하나로 규칙으로 정함(진짜 반대 아님): {ret[0]['resolution']}"
    return False, f"원 id {' · '.join(it['orig_ids'])} 가 지금 판 {' · '.join(str(s) for s in it['stages'])}단계 원천 질문에 없음 — 닫힘"


def short(s, n=200):
    s = re.sub(r'\s+', ' ', str(s or '')).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def refs_txt(q):
    r = q.get('refs') or []
    return ', '.join(r[:6]) + (' …' if len(r) > 6 else '') + f" ({len(r)})"


# ───────── 있던 항목 — 닫힌 것 빼기 · 8단계 문구 갱신
tabs = {t['key']: t for t in Q['tabs']}
removed = {r['id']: r for r in Q.get('removed') or []}
kept_basis = []
n_prev = 0
for key, t in tabs.items():
    keep = []
    for it in t['items']:
        if is_v3(it):
            continue
        n_prev += 1
        ok, why = still_open(it)
        if not ok:
            removed[it['id']] = {'id': it['id'], 'why': why, 'when': 'v3 2026-10-30'}
            continue
        if it['stages'] == [8] and it['orig_ids'][0] in Q8:
            q = Q8[it['orig_ids'][0]]
            it['q'] = q['q']
            it['where'] = [f"step8-origin-questions.md · {q['id']} · 걸린 행 {refs_txt(q)}"]
            if q['match']['type'] == 'conflict':  # 10-30 — 진짜 반대(R5)만 남김 · 조건 분리(R1) · 보수적 선택(R3 · R4)은 규칙으로 정해 빠짐
                it['blocks'] = [x8_block(r) for r in q['refs']]
                it['basis'] = [f"진짜 반대 {len(q['refs'])}개 — 지금은 순서 단정 안 함 + 간격 더 긴 쪽(충돌 하나로 10-30 · R5 · R3) · 원문은 alternatives 보관 · 답이 오면 결정 파일 그 줄만 고치고 step8-apply.py 재실행"]
        keep.append(it)
    t['items'] = keep

# ───────── 새 항목
new = []
# Q8-19 — 부작용 예외 9(의료진 · 충돌 꼴: 부작용 / 합병증)
q = Q8['Q8-19']
blocks = []
for r in q['refs']:
    x = SE[r]
    blocks.append({'id': r, 'title': f"{x.get('family_source_name') or x['family']} ({x['family']}) — {x['name']} · 발생률 {x.get('incidence') or '원문 없음'}",
                   'sides': [{'k': 'A', 'label': '부작용(흔한 예상 반응) — 지금 값', 'lines': [f"원천 severity {x.get('severity')}({x.get('severity_site')}) · {x.get('source')}",
                                                                                     f"발생 {x.get('onset') or '-'} · 지속 {x.get('duration') or '-'}", f"대처: {short(x.get('management'), 160)}"]},
                             {'k': 'B', 'label': '합병증(드문 이상 결과)', 'lines': [f"기전: {short(x.get('mechanism'), 200)}", f"위험 요인: {' · '.join(x.get('risk_factors') or []) or '원문 없음'}",
                                                                              '고르면 합병증 노드(계열 → 합병증 엣지)로 올림 — 원천 severity 는 바꾸지 않음']}]})
new.append({'tab': 'doctor', 'id': 's8-Q8-19', 'orig_ids': ['Q8-19'], 'stages': [8], 'stage_label': '8단계 · 시맨틱', 'status': '확인 대기', 'kind': 'conflict',
            'group': '8단계 — 부작용 · 합병증 경계(시맨틱 U2 예외)',
            'where': [f"step8-origin-questions.md · Q8-19 · 걸린 행 {refs_txt(q)}", 'semantic.json attributes_not_nodes 부작용 · 의료진 질문 예외 9'],
            'q': q['q'], 'blocks': blocks,
            'basis': [SEM['reading']['side_effects'], '지금은 9개 모두 부작용(계열 속성 safety.side_effects) — 답이 오면 그 행만 고치고 step8-apply.py 재실행']})
# Q8-20 — 묶음 원칙 「열 시술 후 주입 시술」 ↔ 개별 순서(10-30 충돌 하나로 전수 가드에서 드러남 · 진짜 반대)
q = Q8['Q8-20']
new.append({'tab': 'doctor', 'id': 's8-Q8-20', 'orig_ids': ['Q8-20'], 'stages': [8], 'stage_label': '8단계', 'status': '확인 대기', 'kind': 'conflict',
            'group': '8단계 — 순서 · 같은 날 · 간격 충돌(원문 나란히)', 'where': [f"step8-origin-questions.md · Q8-20 · 걸린 행 {refs_txt(q)}"],
            'q': q['q'], 'blocks': [x8_block(r) for r in q['refs']],
            'basis': ['10-30 충돌 하나로 — 묶음 낱말 끝점을 계열로 펴 다시 센 순서 반대(X8 뒤에 더함 · 기존 X8 id 유지) · 지금은 순서 단정 안 함 + 간격 더 긴 쪽']})
# Q7-03 — 흉터 필러(R26 = 계열만)
q = Q7['Q7-03']
new.append({'tab': 'hospital', 'id': 's7-oq-Q7-03', 'orig_ids': ['Q7-03'], 'stages': [7], 'stage_label': '7단계', 'status': '확인 대기',
            'group': '7단계 — 흉터 필러(R26)', 'where': ['step7-origin-questions.md · Q7-03 · ' + q['to']],
            'q': q['question'], 'also': [], 'now': 'R26 — 흉터 필러 = 계열만(필러 M2 계열 추천 · 단위 시술 없음) · 튼살도 같음',
            'ctx': [f"받는 사람: {q['to']}"] + [f"걸린 곳: {w}" for w in q['where']]})
# R27 — 갈래 목록 복사(원천 수정 후보 · 갈래마다 1)
r27 = {}
for r in S7['source_fix_candidates']:
    if 'R27' in r['kind']:
        r27.setdefault(r['from'], []).append(r)
cname = {}
for c in S7['concerns']['categories'] + S7['concerns']['subcategories'] + S7['concerns']['extra_items']:
    cname[c['id']] = c.get('name') or c.get('concern') or c.get('source_label')
for anc in sorted(r27, key=lambda a: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', a)]):
    rs = r27[anc]
    nm = cname.get(anc) or anc
    slug = re.sub(r'[^0-9A-Za-z가-힣]+', '_', anc).strip('_')
    fams = ' · '.join(dict.fromkeys(f"{r['source_family']}" for r in rs))
    new.append({'tab': 'hospital', 'id': f's7-R27-{slug}', 'orig_ids': [anc], 'stages': [7], 'stage_label': '7단계', 'status': '원천 수정 후보',
                'group': '7단계 — 원천 수정 후보(R27 갈래 목록 복사)', 'where': [f"step7-source-fix.md · 갈래 목록 복사(R27) · {anc} {len(rs)}줄"],
                'q': f"갈래 「{nm}」 의 추천 시술 목록({fams})이 추천 조합 여러 개에 똑같이 복사돼 있습니다 — 조합마다 목록이 달랐어야 하나요, 같은 목록이 맞나요?",
                'also': [], 'now': 'R27 — 겹친 엣지는 하나로 합침(같은 목록이면 한 번만) · 원천 수정 후보로만 적음',
                'ctx': [short(r['basis'], 300) for r in rs]})
for it in new:
    if it['id'] in removed:
        raise SystemExit(f"새 항목 id 가 빠진 id 와 겹침(옛 답이 붙음): {it['id']}")
    tabs[it['tab']]['items'].append(it)

# ───────── 묶기
counts = {k: len(t['items']) for k, t in tabs.items()}
added = {k: sum(1 for i in new if i['tab'] == k) for k in tabs}
removed_now = [r for r in removed.values() if r.get('when') == 'v3 2026-10-30']
Q['version'] = 'silver-questions v3.1 2026-10-30'
Q['note'] = '1~8단계 질문 — v2 뒤 더함: 8단계 Q8-19(부작용 예외 9 · 시맨틱 U2) · 7단계 Q7-03(흉터 필러 · R26) · 7단계 R27 원천 수정 후보(갈래 목록 복사) · 닫힌 것 뺌 · 10-30 충돌 하나로: 8단계 충돌 질문은 진짜 반대(R5)만(Q8-1 대기 · Q8-7 등급은 규칙으로 정해 뺌 · Q8-20 묶음 원칙 더함)'
Q['inputs'] = list(dict.fromkeys(Q['inputs'] + ['step7-concerns.json origin_questions · source_fix_candidates(R27)', 'step7-source-fix.md', 'semantic.json attributes_not_nodes · reading.side_effects']))
Q['counts'] = {'doctor': counts['doctor'], 'hospital': counts['hospital'], 'added_v3': added, 'removed_v3': len(removed_now), 'removed_total': len(removed),
               'added_step8': Q['counts'].get('added_step8')}
Q['removed'] = sorted(removed.values(), key=lambda r: r['id'])
Q['removed_ids'] = [r['id'] for r in Q['removed']]
Q['kept_check'] = {'what': f"v2 항목 {n_prev}(의료진 · 병원)을 지금 판 원천 질문 파일과 대조 — 닫힌 것 {len(removed_now)}",
                   'basis': ['항목마다 원 id 가 지금 판 1 · 2 · 5 · 6단계 원천 질문 md · step3-sites.json doctor_questions · step7-concerns.json · step8-relations.json origin_questions 에 남아 있으면 열림(남은 항목 id 그대로)',
                             '5 · 7 · 8단계 원천 질문 파일 10-30 갱신 — 5단계 24 id 전부 v2 항목에 있음 · 7단계 Q7-03 새로 · 8단계 Q8-19 새로(Q8-1~18 문구 · 걸린 행은 지금 판으로 다시 씀)',
                             '_RESUME §2 10-30 「R26 흉터 필러 · 튼살 = 계열만」은 추천값만 정함 — step7 Q7-03 은 지금 판에 남아 질문 유지',
                             '_RESUME §2 10-30 「엑셀V 동의어 + U5-138 KTP」 — step8 Q8-10(M8-혈관레이저 = 엑셀V · 브이빔)은 지금 판 origin_questions 에 남아 유지',
                             'step7-source-fix.md 「계열 코드 어긋남」 13 은 R7(이름 따름)으로 이미 정한 원천 수정 기록 — 질문으로 더하지 않음 · R27 갈래 목록 복사 60줄만 갈래마다 1 질문']}
js = json.dumps(Q, ensure_ascii=False, indent=1)
open(QJ, 'w', encoding='utf-8').write(js + '\n')
h = open(QH, encoding='utf-8').read()
pre, rest = h.split('<script id="data" type="application/json">', 1)
_, post = rest.split('</script>', 1)
emb = json.dumps(Q, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
open(QH, 'w', encoding='utf-8').write(pre + '<script id="data" type="application/json">' + emb + '</script>' + post)
print(f"의료진 {counts['doctor']} · 병원 {counts['hospital']} · 더한 {sum(added.values())} {added} · 뺀 {len(removed_now)} · 빠진 id 누계 {len(removed)}")
