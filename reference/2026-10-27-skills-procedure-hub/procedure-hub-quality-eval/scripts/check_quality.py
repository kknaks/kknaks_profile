#!/usr/bin/env python3
"""허브 품질 측정 점검 — quality-eval.py 를 임시 폴더에서 두 번 돌려(결정론 · 정본 낡음) 목표 6 을 판정하고,
문항 · 정답 · 채점 식이 1차(고정본)와 같은지 · 규칙으로 계산되는 정답 칸은 무엇이 바뀌었는지 · 판끼리(v1 · v2 · v3 · 지금) 지표를 나란히 본다.

읽기만 한다. 측정 스크립트(quality-eval.py) · 리포트 · 문항 파일 · 실버 · 보관 판(quality-v*)은 고치지 않는다.
quality-eval.py 를 그대로 부른다(감싸기만) — 측정 로직을 여기서 다시 짜지 않는다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \\
        --work orchestration/work/phub-recommend \\
        --out <scratchpad>/quality-check.json --selftest

본다
- 결정론 — quality-eval.py --out <임시 A> · <임시 B> 두 번 · 산출 3개(quality-eval-set.json · quality-report.json · .md) 바이트 같음
- 정본 낡음 — 작업 폴더의 산출 3개 = 재실행 결과(다르면 「실버가 바뀌었는데 측정을 다시 안 돌림」)
- 문항 · 정답 고정 — 문항 파일을 1차 고정본(references/baseline.json fixed_set — 지금 quality-v1/quality-eval-set.json)과 문항마다 대조
  · 문항 수 · id · 의도 · 출처 · 문장 · 슬롯 · 정답 상태 · 근거 · 정답 칸(규칙 칸 밖) 다르면 오류
  · 규칙으로 계산되는 정답 칸(baseline rule_fields — 정답 하위 계열 · 부위 낱말)은 오류가 아니라 「무엇이 바뀌었나」 목록으로 보고
- 채점 식 고정 — quality-eval.py 의 채점 함수 · 상수(baseline scoring)의 소스 지문이 기준과 같은가(다르면 오류) ·
  측정 경로 함수(baseline path)는 바뀌면 경고(사람이 diff 확인 — 2차에서 resolve · I-01 경로가 바뀐 것처럼 의도된 변경일 수 있음)
- 목표 제외 문항 — 리포트 goal_excluded = baseline goal_excluded(1차 의료진 질문 5 · 정답 미정 1)
- 목표 6 — CC 슬롯 · CC 없음 두 경로. 묶음 6 = (재현율 · 정밀도) · (I-01 재현율 · 정밀도) · 문항 안전 누락 · 원천 안전 원문 누락(M4) · 말 → 노드 찾기 · 엣지 표본 오류율
  · 필수 경로(--require · 기본 cc)가 6/6 이 아니면 오류 「목표 미달」 · 다른 경로는 보고만
- 판끼리 — 보관 판(baseline versions)의 리포트 지표 · 목표를 지금과 나란히 · 문항별 상태가 바뀐 문항 id

숫자는 이 파일에 적지 않는다(고정 assert 없음) — 기준은 references/baseline.json, 셈은 출력이다.
종료 코드: errors 0 이고 selftest(요청 시) 전부 잡히면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import ast
import copy
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, '..', 'references', 'baseline.json')
OUTS = ('quality-eval-set.json', 'quality-report.json', 'quality-report.md')
GROUPS = [  # 목표 6 묶음(사용자 10-30 품질 목표) — quality-eval.py write_v2_head six() 와 같은 묶음
    ('질문 세트 재현율 · 정밀도(전체) ≥ 0.95', ('recall', 'precision')),
    ('I-01 재현율 · 정밀도 ≥ 0.95', ('i01_recall', 'i01_precision')),
    ('문항 안전 누락 = 0', ('safety_missing',)),
    ('원천 안전 원문 실버 누락(M4) = 0', ('m4_missing',)),
    ('말 → 노드 찾기 ≥ 97%', ('m2_found_pct',)),
    ('엣지 표본 오류율 ≤ 1%', ('m3_error_pct',)),
]


def L(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


# ───────────────────────── 실행 ─────────────────────────
def run_eval(work, script, out_dir):
    r = subprocess.run([sys.executable, script, '--out', out_dir], cwd=work, capture_output=True, text=True)
    return r.returncode, (r.stderr or '')[-2000:]


def same_bytes(a, b):
    return os.path.exists(a) and os.path.exists(b) and filecmp.cmp(a, b, shallow=False)


# ───────────────────────── 지문 ─────────────────────────
def fingerprints(src):
    """최상위 함수 · 대입문의 소스 지문(sha256 앞 12자). 이름 → 지문."""
    t = ast.parse(src)
    out = {}
    for n in t.body:
        if isinstance(n, ast.FunctionDef):
            out[n.name] = hashlib.sha256(ast.get_source_segment(src, n).encode()).hexdigest()[:12]
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            out[n.targets[0].id] = hashlib.sha256(ast.get_source_segment(src, n).encode()).hexdigest()[:12]
    return out


def check_scoring(src, base, err, warn):
    fp = fingerprints(src)
    for name, h in sorted(base['scoring'].items()):
        if fp.get(name) != h:
            err('채점 식 바뀜 — 채점 함수 · 상수 지문이 기준과 다름', f"{name}: 기준 {h} ↔ 지금 {fp.get(name)}")
    changed = sorted(n for n, h in base['path'].items() if fp.get(n) != h)
    for n in changed:
        warn('측정 경로 바뀜 — 사람이 diff 확인(의도된 경로 변경인가)', f"{n}: 기준 {base['path'][n]} ↔ 지금 {fp.get(n)}")
    return {'scoring_checked': sorted(base['scoring']), 'path_changed': changed}


# ───────────────────────── 문항 · 정답 고정 ─────────────────────────
def get_path(d, dotted):
    cur = d
    for k in dotted.split('.'):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def check_fixed(cur_set, fixed_set, base, err):
    rule_fields = base['rule_fields']  # 「answer.sub_families」 같은 점 경로
    rule_keys = {f.split('.', 1)[1] for f in rule_fields if f.startswith('answer.')}
    A = {q['id']: q for q in fixed_set['questions']}
    B = {q['id']: q for q in cur_set['questions']}
    if len(A) != len(B) or set(A) != set(B):
        err('문항 수 · id 다름 — 문항 세트가 1차와 다름', f"1차 {len(A)} · 지금 {len(B)} · 빠짐 {sorted(set(A) - set(B))} · 더함 {sorted(set(B) - set(A))}")
    rule_changes = []
    for qid in sorted(set(A) & set(B)):
        a, b = A[qid], B[qid]
        for k in sorted(set(a) | set(b)):
            if k == 'answer':
                continue
            if a.get(k) != b.get(k):
                err('문항 바뀜 — 문항 · 슬롯 · 의도 · 출처 · 근거 · 정답 상태가 1차와 다름', f"{qid} {k}: {json.dumps(a.get(k), ensure_ascii=False)[:80]} → {json.dumps(b.get(k), ensure_ascii=False)[:80]}")
        aa, ba = a.get('answer') or {}, b.get('answer') or {}
        if (a.get('answer') is None) != (b.get('answer') is None):
            err('정답 바뀜 — 정답 있음 ↔ 정답 미정', qid)
        for k in sorted(set(aa) | set(ba)):
            if aa.get(k) == ba.get(k):
                continue
            if k in rule_keys:
                rule_changes.append({'id': qid, 'text': b.get('text'), 'field': f'answer.{k}', 'before': aa.get(k), 'after': ba.get(k),
                                     'delta': rule_delta(aa.get(k), ba.get(k))})
            else:
                err('정답 바뀜 — 원천 근거 정답 칸이 1차와 다름(규칙 칸 밖)', f"{qid} answer.{k}: {json.dumps(aa.get(k), ensure_ascii=False)[:80]} → {json.dumps(ba.get(k), ensure_ascii=False)[:80]}")
    return rule_changes


def rule_delta(a, b):
    """규칙 칸 전 → 후 차이를 사람이 읽게 — dict(계열 → 목록) · 목록."""
    if isinstance(a, dict) or isinstance(b, dict):
        a, b = a or {}, b or {}
        out = {}
        for k in sorted(set(a) | set(b)):
            sa, sb = set(a.get(k) or []), set(b.get(k) or [])
            if sa != sb:
                out[k] = {'더함': sorted(sb - sa), '뺌': sorted(sa - sb)}
        return out
    sa, sb = set(a or []), set(b or [])
    return {'더함': sorted(sb - sa), '뺌': sorted(sa - sb)}


# ───────────────────────── 목표 ─────────────────────────
def judge(goal):
    p = goal.get('pass') or {}
    rows = []
    for name, keys in GROUPS:
        rows.append({'goal': name, 'values': {k: goal.get(k) for k in keys}, 'pass': all(p.get(k) for k in keys)})
    return {'n_pass': sum(r['pass'] for r in rows), 'of': len(rows), 'rows': rows, 'right': goal.get('right'), 'scored': goal.get('scored'),
            'wrong': goal.get('wrong'), 'path': goal.get('path')}


def check_goals(rep, base, require, err):
    if sorted(rep.get('goal_excluded') or []) != sorted(base['goal_excluded']):
        err('목표 제외 문항 바뀜 — 1차 의료진 질문 · 정답 미정 목록(고정)과 다름', f"기준 {base['goal_excluded']} ↔ 리포트 {rep.get('goal_excluded')}")
    goals = (rep.get('headline') or {}).get('goal') or {}
    out = {m: judge(g) for m, g in goals.items()}
    for m in require:
        if m not in out:
            err('목표 판정 없음 — 리포트에 그 경로가 없음', m)
        elif out[m]['n_pass'] != out[m]['of']:
            miss = [r['goal'] for r in out[m]['rows'] if not r['pass']]
            err('목표 미달 — 필수 경로', f"{m} {out[m]['n_pass']}/{out[m]['of']} · 못 넘은 것 {miss}")
    return out


# ───────────────────────── 판끼리 ─────────────────────────
def version_row(rep, label):
    h = rep.get('headline') or {}
    row = {'label': label, 'version': rep.get('version'),
           'M1': {k: (h.get('M1') or {}).get(k) for k in ('questions', 'scored', 'right', 'recall', 'precision', 'safety_missing', 'i01_recall')},
           'M2_found_pct': (h.get('M2') or {}).get('found_pct'), 'M3_error_pct': (h.get('M3') or {}).get('error_rate_pct'),
           'M4_missing': (h.get('M4') or {}).get('missing'), 'causes': h.get('causes')}
    g = h.get('goal')
    if g:
        row['goal'] = {m: {'n_pass': judge(x)['n_pass'], 'right': x.get('right'), 'recall': x.get('recall'), 'precision': x.get('precision'),
                           'i01_recall': x.get('i01_recall'), 'i01_precision': x.get('i01_precision')} for m, x in g.items()}
    elif rep.get('_v1_goal'):
        x = rep['_v1_goal']
        row['goal'] = {'1차 정의': {'n_pass': judge(x)['n_pass'], 'right': x.get('right'), 'recall': x.get('recall'), 'precision': x.get('precision'),
                                   'i01_recall': x.get('i01_recall'), 'i01_precision': x.get('i01_precision')}}
    return row


def status_changes(prev, cur):
    a = {r['id']: r['status'] for r in prev.get('m1') or []}
    return [{'id': r['id'], 'text': r.get('text'), 'from': a.get(r['id']), 'to': r['status']} for r in cur.get('m1') or [] if a.get(r['id']) != r['status']]


def compare_versions(work, base, cur_rep):
    rows, changes, prev, prev_label = [], [], None, None
    for v in base['versions']:
        p = os.path.join(work, v['report'])
        if not os.path.exists(p):
            rows.append({'label': v['label'], 'missing': v['report']})
            continue
        r = L(p)
        if v.get('goal_from_current_v1_compare') and cur_rep.get('v1_compare'):
            r = dict(r, _v1_goal=cur_rep['v1_compare']['goal'])  # 1차 리포트는 목표 정의 전 — 지금 리포트가 1차를 목표 정의로 다시 센 값
        rows.append(version_row(r, v['label']) | {'note': v.get('note')})
        if prev is not None:
            changes.append({'from': prev_label, 'to': v['label'], 'questions': status_changes(prev, r)})
        prev, prev_label = r, v['label']
    rows.append(version_row(cur_rep, '지금'))
    if prev is not None:
        changes.append({'from': prev_label, 'to': '지금', 'questions': status_changes(prev, cur_rep)})
    return rows, changes


# ───────────────────────── 본체 ─────────────────────────
def check(work, base, require, ran):
    errors, warnings = [], []
    err = lambda kind, detail='': errors.append({'kind': kind, 'detail': detail})
    warn = lambda kind, detail='': warnings.append({'kind': kind, 'detail': detail})
    if ran['exit'] != [0, 0]:
        err('quality-eval.py 종료 코드 ≠ 0', f"{ran['exit']} {ran['stderr'][-300:]}")
    for f in OUTS:
        if not ran['same_ab'].get(f):
            err('결정론 아님 — 두 번 실행 바이트 다름', f)
        if not ran['same_work'].get(f):
            err('정본 낡음 — 작업 폴더 산출이 재실행 결과와 바이트 다름(측정을 다시 안 돌림)', f)
    scoring = check_scoring(ran['src'], base, err, warn)
    rule_changes = check_fixed(ran['set'], ran['fixed_set'], base, err)
    goals = check_goals(ran['rep'], base, require, err)
    rows, changes = compare_versions(work, base, ran['rep'])
    return {'errors': errors, 'warnings': warnings, 'scoring': scoring, 'rule_field_changes': rule_changes,
            'goals': goals, 'versions': rows, 'version_changes': changes}


def load_run(work, script, tmp):
    a, b = os.path.join(tmp, 'a'), os.path.join(tmp, 'b')
    os.makedirs(a), os.makedirs(b)
    ea, sa = run_eval(work, script, a)
    eb, sb = run_eval(work, script, b)
    base = L(BASELINE)
    ran = {'exit': [ea, eb], 'stderr': sa + sb,
           'same_ab': {f: same_bytes(os.path.join(a, f), os.path.join(b, f)) for f in OUTS},
           'same_work': {f: same_bytes(os.path.join(a, f), os.path.join(work, f)) for f in OUTS},
           'src': open(script, encoding='utf-8').read(),
           'fixed_set': L(os.path.join(work, base['fixed_set']))}
    ran['set'] = L(os.path.join(a, 'quality-eval-set.json')) if ea == 0 else {'questions': []}
    ran['rep'] = L(os.path.join(a, 'quality-report.json')) if ea == 0 else {}
    return ran


# ───────────────────────── selftest ─────────────────────────
def selftest(work, base, require, ran):
    """틀린 값을 넣어 잡히는지 — 사본(메모리)만 바꾼다. quality-eval.py 를 다시 돌리지 않는다."""
    cases = []

    def case(name, expect, mutate, in_rule=False):
        r = copy.deepcopy(ran)
        mutate(r)
        got = check(work, base, require, r)
        kinds = sorted({e['kind'] for e in got['errors']})
        if in_rule:
            caught = any(c['id'] == expect for c in got['rule_field_changes'])
        else:
            caught = any(k.startswith(expect) for k in kinds)
        cases.append({'tamper': name, 'expect': expect, 'caught': caught, 'got': kinds if not in_rule else [c['id'] + ' ' + c['field'] for c in got['rule_field_changes']][:5]})

    q0 = lambda r: r['set']['questions'][0]
    qi = lambda r, f: next(q for q in r['set']['questions'] if f(q))

    case('문항 문장 바꾸기(Q001 「이마 주름」 → 「이마 주름 고민」)', '문항 바뀜', lambda r: q0(r).__setitem__('text', q0(r)['text'] + ' 고민'))
    case('정답 계열 바꾸기(I-01 문항 families 에 M99 더함)', '정답 바뀜 — 원천 근거', lambda r: qi(r, lambda q: q['intent'] == 'I-01' and q.get('answer'))['answer']['families'].append('M99'))
    case('슬롯 바꾸기(cc 지움)', '문항 바뀜', lambda r: qi(r, lambda q: (q.get('slots') or {}).get('cc')).__setitem__('slots', {k: v for k, v in qi(r, lambda q: (q.get('slots') or {}).get('cc'))['slots'].items() if k != 'cc'}))
    case('문항 하나 빼기', '문항 수 · id 다름', lambda r: r['set']['questions'].pop())
    case('정답 있음 → 정답 미정(answer None)', '정답 바뀜 — 정답 있음', lambda r: qi(r, lambda q: q.get('answer') and q['intent'] == 'I-02').__setitem__('answer', None))

    rq = next((q['id'] for q in ran['set']['questions'] if (q.get('answer') or {}).get('sub_families')), None)

    def m_rule(r):
        q = qi(r, lambda q: q['id'] == rq)
        q['answer']['sub_families'] = {k: v + ['가짜 하위'] for k, v in q['answer']['sub_families'].items()}
    if rq:
        case(f'규칙 칸 바꾸기({rq} 정답 하위에 「가짜 하위」 — 오류 아님 · 바뀜 목록에 나와야)', rq, m_rule, in_rule=True)

    case('채점 상수 바꾸기(GOALS 0.95 → 0.90)', '채점 식 바뀜', lambda r: r.__setitem__('src', r['src'].replace("('recall', '질문 세트 재현율(전체)', 0.95", "('recall', '질문 세트 재현율(전체)', 0.90", 1)))
    case('채점 함수 바꾸기(goal_pass 비교 >= → >)', '채점 식 바뀜', lambda r: r.__setitem__('src', r['src'].replace("out[k] = v is not None and ((v >= t)", "out[k] = v is not None and ((v > t)", 1)))
    case('목표 제외 문항 바꾸기(Q042 빼기)', '목표 제외 문항 바뀜', lambda r: r['rep'].__setitem__('goal_excluded', [x for x in r['rep']['goal_excluded'] if x != 'Q042']))

    def m_goal(r):
        g = r['rep']['headline']['goal'][require[0]]
        g['i01_precision'] = 0.9
        g['pass'] = dict(g['pass'], i01_precision=False)
    case(f'필수 경로({require[0]}) I-01 정밀도 0.9', '목표 미달', m_goal)
    case('작업 폴더 리포트가 재실행과 다름', '정본 낡음', lambda r: r['same_work'].__setitem__('quality-report.json', False))
    case('두 번 실행 결과 다름', '결정론 아님', lambda r: r['same_ab'].__setitem__('quality-eval-set.json', False))
    case('quality-eval.py 실패', 'quality-eval.py 종료 코드', lambda r: r.__setitem__('exit', [1, 0]))
    return cases


def write_baseline(work, script, path):
    """지금 quality-eval.py 의 지문으로 기준을 다시 쓴다 — 채점 식을 일부러 바꾸는 결정(사용자)이 있을 때만."""
    base = L(path)
    fp = fingerprints(open(script, encoding='utf-8').read())
    base['scoring'] = {k: fp[k] for k in base['scoring']}
    base['path'] = {k: fp[k] for k in base['path'] if k in fp}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(base, f, ensure_ascii=False, indent=1)
        f.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', default='orchestration/work/phub-recommend')
    ap.add_argument('--out', required=True)
    ap.add_argument('--require', default='cc', help='목표 6/6 이어야 하는 경로(쉼표) — cc · nocc · v1')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--write-baseline', action='store_true', help='채점 지문 기준을 지금 스크립트로 다시 씀(결정 있을 때만)')
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    script = os.path.join(work, 'quality-eval.py')
    if a.write_baseline:
        write_baseline(work, script, BASELINE)
        print('기준 다시 씀 →', os.path.abspath(BASELINE))
        return 0
    base = L(BASELINE)
    require = [x for x in a.require.split(',') if x]
    tmp = tempfile.mkdtemp(prefix='quality-check-')
    try:
        ran = load_run(work, script, tmp)
        res = check(work, base, require, ran)
        st = selftest(work, base, require, ran) if a.selftest else []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    res = {'work': work, 'baseline': os.path.abspath(BASELINE), 'require': require,
           'run': {'exit': ran['exit'], 'same_ab': ran['same_ab'], 'same_work': ran['same_work']}} | res | {'selftest': st}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    g = res['goals']
    gl = ' · '.join(f"{m} {x['n_pass']}/{x['of']}(맞음 {x['right']}/{x['scored']})" for m, x in g.items())
    rc = res['rule_field_changes']
    print(f"목표 {gl} · 규칙 칸 바뀐 문항 {len({c['id'] for c in rc})} · 측정 경로 바뀐 함수 {len(res['scoring']['path_changed'])} · "
          f"판 {len(res['versions'])} · errors {len(res['errors'])} · warnings {len(res['warnings'])}"
          + (f" · selftest {sum(c['caught'] for c in st)}/{len(st)} 잡힘" if st else '') + f" → {os.path.abspath(a.out)}")
    bad = len(res['errors']) > 0 or (st and not all(c['caught'] for c in st))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
