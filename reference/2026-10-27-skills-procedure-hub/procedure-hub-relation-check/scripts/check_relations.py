"""Procedure Hub 실버 8단계 관계 원장(step8-relations) 점검 — 읽기만 · 표준 라이브러리.

하는 일
1. step8-apply.py 를 임시 폴더로 다시 돌려 원장과 바이트 비교(원장 낡음 · 결정론)
2. 원장 불변식 검사(errors) — 사람 확인 게이트 상태 없음(U8-1) · 간격 숫자 칸(first a|b · days 하한 ≤ 상한 · 원문 간격 낱말마다 사전 갈래) ·
   「같은 날 불가」 = same_day false · 「대체(택 1)」 = 간격 비움 · 끝점 단위 시술 = 5단계 키 · 엣지 ↔ 주장 · 충돌 표시 ↔ 충돌 표 ·
   피함 엣지 출발 = 7단계 고민 노드 · 확인 조건 id = 결정 사전 · 원천 질문 걸린 행 존재 · summary 재셈 · open 0
3. --selftest: 원장 사본에 틀린 값을 넣어(뒤집은 days · 게이트 상태 · 엣지 빠진 주장 · 없는 고민 · 같은 날 불가인데 true · 사전 밖 간격 낱말 ·
   없는 단위 시술 · summary) 각각 errors 로 잡히는지 본다

사용
  python3 check_relations.py --work orchestration/work/phub-recommend --out <scratchpad>/relation-check.json   # 새 스냅샷은 --source <폴더>
  python3 check_relations.py --work orchestration/work/phub-recommend --selftest
종료 코드: errors 0 · open 0(· selftest 전부 잡힘) 이면 0, 아니면 1.
"""
import argparse
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # 작업 폴더에 __pycache__ 를 남기지 않는다


def load_apply(work):
    spec = importlib.util.spec_from_file_location('step8_apply', work / 'step8-apply.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ekeys(e):
    if e['level'] in ('해석 안 됨', '시술 아님'):
        return []
    if e['level'] == '복합(나눔)':
        return sorted({k for p in e['parts'] for k in ekeys(p)})
    if e['level'] == '모든 시술':
        return ['all']
    if e['level'] == '계열 묶음':
        return ['bundle:' + '|'.join(e['families'])]
    if e['units']:
        return ['units:' + ','.join(e['units'])]
    return ['family:' + ','.join(e['families']) + (('#' + e['sub_family']) if e.get('sub_family') else '') + (('#' + e['technique']) if e.get('technique') else '')]


def units_of(e):
    out = list(e.get('units') or [])
    for p in e.get('parts') or []:
        out += units_of(p)
    return out


def validate(rel, dec, s5, s7, A):
    errors = []

    def err(t, **kw):
        errors.append(dict(type=t, **kw))
    lex = dec['interval_lexicon']
    UNITS = {u['id'] for u in s5['units']}
    CON7 = {x['id'] for g in ('categories', 'subcategories', 'extra_items') for x in s7['concerns'].get(g) or []}
    CONDS = {c['id'] for c in dec['conditions']}
    claims = {c['id']: c for c in rel['claims']}
    SCOPE = dec['scope_rule']
    import re

    def scope_leaks(e, extra_q=None):
        out = []
        for p in ([e] if e['level'] != '복합(나눔)' else e['parts']):
            src = ' '.join(filter(None, [p.get('text'), p.get('qualifier'), ' '.join(p.get('stripped_prefix') or []), extra_q]))
            if re.search(SCOPE['words'], src) and p['level'] in SCOPE['group_levels'] and p.get('default_apply') is not False:
                out.append(p.get('text'))
        return out
    if rel['open']:
        err('open 남음', n=len(rel['open']))
    for c in rel['claims']:
        if c.get('gate_status') != '자동(규칙)':
            err('사람 확인 게이트 상태(U8-1 위반 — 규칙으로만)', claim=c['id'], gate_status=c.get('gate_status'))
        iv = c.get('interval')
        if iv:
            if iv.get('first') not in ('a', 'b', None):
                err('interval.first 가 a · b · null 밖', claim=c['id'], first=iv.get('first'))
            d = iv.get('days')
            if d is not None and (len(d) != 2 or d[0] < 0 or d[0] > d[1]):
                err('interval.days 하한 > 상한 · 음수', claim=c['id'], days=d)
            if A.interval_empty(iv, lex):
                err('간격 원문 낱말이 있는데 숫자 칸 · 표시 비어 있음', claim=c['id'], text=iv.get('text'))
            for w in A.interval_unread(iv, lex):
                err('간격 원문 낱말을 읽는 사전 갈래 없음', claim=c['id'], word=w)
        if iv and iv.get('options'):
            subs = {o.get('sub_condition') for o in iv['options'] if o.get('sub_condition')}
            if len(subs) > 1 and (not iv.get('by_sub_condition') or iv.get('days') is not None or iv.get('same_day') is not None or iv.get('first') is not None):
                err('하위 조건이 갈리는데 겉 칸을 섞음(by_sub_condition)', claim=c['id'])
        if c['kind'] in SCOPE['kinds']:
            for s_ in 'ab':
                for p in scope_leaks(c[s_]):
                    err('한정어를 떼고 묶음으로 연 끝점이 기본 적용(scope_rule)', claim=c['id'], text=p)
        if c['kind'] == '같은 날 불가' and (iv or {}).get('same_day') is not False:
            err('「같은 날 불가」인데 same_day 가 false 아님', claim=c['id'])
        if c['kind'] == '대체(택 1)' and (iv or {}).get('days') is not None:
            err('「대체(택 1)」인데 간격 숫자 있음', claim=c['id'])
        for s in 'ab':
            for u in units_of(c[s]):
                if u not in UNITS:
                    err('끝점 단위 시술이 5단계에 없음', claim=c['id'], unit=u)
    in_edge = {}
    for e in rel['edges']:
        for i in e['claims']:
            if i not in claims:
                err('엣지가 없는 주장을 가리킴', edge=e['id'], claim=i)
            in_edge.setdefault(i, []).append(e['id'])
    for c in rel['claims']:
        if any(ekeys(c['a'])) and any(ekeys(c['b'])) and c['id'] not in in_edge:
            err('끝점이 풀린 주장인데 엣지에 없음', claim=c['id'])
    conf_ids = set()
    for x in rel['conflicts']:
        for side in x['sides'].values():
            conf_ids |= set(side if isinstance(side, list) else [])
        if x['type'] == '간격 수치':
            conf_ids |= set(x['sides'])
    for c in rel['claims']:
        if (c['id'] in conf_ids) != (c.get('review_status') == 'conflict'):
            err('충돌 표시 ↔ 충돌 표 어긋남', claim=c['id'], review_status=c.get('review_status'))
    for a in rel['avoid_edges']:
        for p in scope_leaks(a['to'], a.get('qualifier')):
            err('한정어를 떼고 묶음으로 연 끝점이 기본 적용(scope_rule)', avoid=a['id'], text=p)
        for k in a['from_concerns']:
            if k not in CON7:
                err('피함 엣지 출발이 7단계 고민 노드 아님', avoid=a['id'], concern=k)
        if a['to']['level'] == '해석 안 됨' and not any(a['id'] in q['refs'] for q in rel['origin_questions']):
            err('피함 엣지 끝점 못 풂 · 원천 질문 없음', avoid=a['id'])
    for k in rel['conditions']['claims']:
        for cid in k['conditions']:
            if cid not in CONDS:
                err('확인 조건 id 가 결정 사전에 없음', claim=k['id'], condition=cid)
        if k['kind'] == '사람 조건' and not k['conditions']:
            err('사람 조건인데 조건 없음', claim=k['id'])
    known = set(claims) | {x['id'] for x in rel['conflicts']} | {x['id'] for x in rel['conditions']['claims']} | \
        {x['id'] for x in rel['conditions']['grade_conflicts']} | {x['id'] for x in rel['conditions']['wait_conflicts']} | \
        {x['id'] for x in rel['evidence']['guides']} | {x['id'] for x in rel['avoid_edges']}
    for q in rel['origin_questions']:
        for r in q['refs']:
            if r not in known:
                err('원천 질문이 없는 행을 가리킴', question=q['id'], ref=r)
    s = rel['summary']
    for k, n in (('claims', len(rel['claims'])), ('edges', len(rel['edges'])), ('conflicts', len(rel['conflicts'])), ('avoid_edges', len(rel['avoid_edges'])),
                 ('condition_claims', len(rel['conditions']['claims'])), ('open', len(rel['open'])), ('complications', len(rel['safety']['complications'])),
                 ('site_caution', len(rel['safety']['site_caution']))):
        if s.get(k) != n:
            err('summary 불일치', key=k, summary=s.get(k), recount=n)
    return errors


TAMPER = [
    ('days 뒤집음', 'interval.days 하한 > 상한 · 음수', lambda r: next(c for c in r['claims'] if (c.get('interval') or {}).get('days') and c['interval']['days'][0] < c['interval']['days'][1])['interval'].update(days=[30, 10])),
    ('게이트 상태 넣음', '사람 확인 게이트 상태(U8-1 위반 — 규칙으로만)', lambda r: r['claims'][0].update(gate_status='unconfirmed')),
    ('엣지에서 주장 뺌', '끝점이 풀린 주장인데 엣지에 없음', lambda r: [e['claims'].remove(r['claims'][0]['id']) for e in r['edges'] if r['claims'][0]['id'] in e['claims']]),
    ('없는 고민에서 피함', '피함 엣지 출발이 7단계 고민 노드 아님', lambda r: r['avoid_edges'][0].update(from_concerns=['P99-9'])),
    ('같은 날 불가인데 true', '「같은 날 불가」인데 same_day 가 false 아님', lambda r: next(c for c in r['claims'] if c['kind'] == '같은 날 불가')['interval'].update(same_day=True)),
    ('사전 밖 간격 낱말(택 1 갈래 지움)', '간격 원문 낱말을 읽는 사전 갈래 없음',
     lambda r: next(c for c in r['claims'] if c['kind'] == '대체(택 1)')['interval'].update(kind=None, marks=[], branches=[])),
    ('없는 단위 시술', '끝점 단위 시술이 5단계에 없음', lambda r: next(c for c in r['claims'] if c['a'].get('units'))['a']['units'].append('U5-999')),
    ('피함 조건부를 기본 적용으로', '한정어를 떼고 묶음으로 연 끝점이 기본 적용(scope_rule)',
     lambda r: [x['to'].update(default_apply=True) for x in r['avoid_edges'] if x['to'].get('default_apply') is False]),
    ('하위 조건 갈리는데 겉 same_day 채움', '하위 조건이 갈리는데 겉 칸을 섞음(by_sub_condition)',
     lambda r: next(c for c in r['claims'] if (c.get('interval') or {}).get('by_sub_condition'))['interval'].update(same_day=True)),
    ('summary 셈 틀림', 'summary 불일치', lambda r: r['summary'].update(claims=r['summary']['claims'] + 1)),
    ('충돌 표시 지움', '충돌 표시 ↔ 충돌 표 어긋남', lambda r: next(c for c in r['claims'] if c.get('review_status') == 'conflict').update(review_status='ok')),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--work', required=True, help='orchestration/work/phub-recommend')
    ap.add_argument('--source', help='원천 폴더(없으면 결정 source.path)')
    ap.add_argument('--out', help='결과 JSON 경로(없으면 stdout)')
    ap.add_argument('--selftest', action='store_true', help='틀린 값을 넣어 잡히는지')
    a = ap.parse_args()
    work = Path(a.work).resolve()
    A = load_apply(work)
    dec = json.load(open(work / 'step8-decisions.json'))
    s5 = json.load(open(work / dec['canon']['step5']))
    s7 = json.load(open(work / dec['canon']['step7']))
    rel = json.load(open(work / 'step8-relations.json'))
    errors = validate(rel, dec, s5, s7, A)
    with tempfile.TemporaryDirectory() as td:
        cmd = [sys.executable, str(work / 'step8-apply.py'), '--out', td] + (['--source', a.source] if a.source else [])
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0:
            errors.append(dict(type='step8-apply 재실행 실패', stderr=p.stderr[-300:]))
            fresh = None
        else:
            fresh = json.load(open(Path(td) / 'step8-relations.json'))
            if (Path(td) / 'step8-relations.json').read_bytes() != (work / 'step8-relations.json').read_bytes():
                errors.append(dict(type='원장 낡음(apply 재실행과 바이트 다름)', claims_now=len(fresh['claims']), claims_ledger=len(rel['claims'])))
    selftest = []
    if a.selftest:
        for name, want, f in TAMPER:
            r = copy.deepcopy(rel)
            f(r)
            got = {e['type'] for e in validate(r, dec, s5, s7, A)}
            selftest.append(dict(tamper=name, expect=want, caught=want in got, got=sorted(got)))
    out = dict(ledger='step8-relations.json', totals=dict(errors=len(errors), open=len(rel['open']), stale=len(rel['stale_decisions']),
               claims=len(rel['claims']), edges=len(rel['edges']), avoid_edges=len(rel['avoid_edges']), condition_claims=len(rel['conditions']['claims']),
               origin_questions=len(rel['origin_questions'])),
               open=rel['open'], stale_decisions=rel['stale_decisions'], errors=errors, selftest=selftest,
               fresh_open=(fresh or {}).get('open'))
    txt = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, 'w').write(txt)
    else:
        print(txt)
    st = (f" · selftest {sum(x['caught'] for x in selftest)}/{len(selftest)} 잡힘" if selftest else '')
    print(f"claims {len(rel['claims'])} · edges {len(rel['edges'])} · 피함 {len(rel['avoid_edges'])} · 조건 {len(rel['conditions']['claims'])} · errors {len(errors)} · open {len(rel['open'])}{st}"
          + (f" → {a.out}" if a.out else ''), file=sys.stderr)
    bad = errors or rel['open'] or (selftest and not all(x['caught'] for x in selftest))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
