"""실버 8단계(관계 · 확인 조건 · 안전 · 근거) 반영 — 결정론(3~7단계와 같은 구조).

입력: step8-decisions.json(결정 — 이름 풀이 사전 · 간격 낱말 사전 · 문장 패턴 · 확인 조건 사전 · 고민 조건 금기(피함) · 원천 질문 · 경과표 붙는 곳 · 사용자 판단)
      원천(결정 source.path) contraindications · synergy · treatment-sequence · treatment-optimization · problem-packages · problem-combos ·
      combo-recipes · pre-procedure-checklist · consent-checklist · patient-education · post-procedure-timeline · complications ·
      anatomy-danger-zones · pih-risk · literature-evidence · procedure-profiles · taxonomy · extracted
      1~7단계 정본(step1-products · step2-families · step3-sites · step4-techniques · step5-units · step6-packages · step7-concerns) · source-map(읽기만)
출력: step8-relations.json · step8-relations.md · step8-origin-questions.md

조사(step8-research · scratchpad s8_resolve · s8_build)의 계산을 옮기되, 조사 안에 박혀 있던 행별 대응표(원칙 · 규칙 · 위험 문장 → 쌍)는
U8-1 (나)대로 문장 패턴 규칙(decisions.sentence.patterns)으로 바꿨다. 사람 확인 게이트는 없다 — 규칙으로 하나로 안 정해지는 것만 원천 질문.
간격은 간격 낱말 사전(decisions.interval_lexicon)으로 숫자 칸(interval.days · first · same_day)을 채운다 — 원문 간격 낱말이 있는데 숫자 칸 · 표시가 비면 open.
원천 행 · 8단계 칸(source-map)이 행선지 없이 남으면 open · 원천 질문이 필요한데 결정에 없으면 open · 7단계 끝점(고민 · 조합 · CC 엣지)이 지금 7단계에 없으면 open.
숫자는 이 파일에 적지 않는다(고정 assert 없음).
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
C_ = collections.Counter


# ───────── 간격 낱말 사전(사용자 10-29) — 원문 → 숫자 칸 · 표시 ─────────
def _num_ranges(t, lex):
    units = lex['units_days']
    pat = next(b['pattern'] for b in lex['branches'] if b['id'] == 'L-NUM')
    out = []
    for m in re.finditer(pat, t):
        a, u1, b, u2 = m.group(1), m.group(2), m.group(3), m.group(4)
        lo = float(a) * units[u1 or u2]
        hi = float(b) * units[u2] if b else float(a) * units[u2]
        if not b and u1 and u1 != u2:  # 「3일 1주」 같은 이음 없는 두 단위는 앞만
            hi = lo
        after = t[m.end():]
        before = t[:m.start()]
        oh = bool(re.search(lex['open_high_after'], after)) or bool(re.search(lex['open_high_before'], before))
        out.append((round(lo, 3), round(hi, 3), oh, m.group(0)))
    return out


def parse_interval(text, lex, ctx_same_day=None):
    """원문 간격 문장 → {days · open_high · same_day · marks · condition · options · repeat · kind · first_from_source_order}.
    값을 새로 만들지 않고 원문 낱말 · 숫자만 사전대로 읽는다. 하위 조건(「A: … / B: …」) · 「또는」 은 options 로 두고 겉 칸은 감싼 범위."""
    if text is None or not str(text).strip():
        return None
    t = str(text).strip()
    pieces = [p for p in re.split(lex['option_split'], t) if p.strip()]
    if len(pieces) > 1:
        opts = []
        for p in pieces:
            sub = None
            m = re.match(lex['sub_condition_head'], p)
            if m and not re.search(r'\d+\s*(일|주|개월)', m.group(1)):
                sub = m.group(1).strip()
                p2 = p[m.end():]
            else:
                p2 = p
            o = _parse_one(p2, lex)
            if sub:
                o['sub_condition'] = sub
            o['text'] = p.strip()
            opts.append(o)
        r = {'text': t, 'days': None, 'open_high': any(o['open_high'] for o in opts), 'same_day': None, 'marks': [], 'condition': None,
             'repeat': any(o['repeat'] for o in opts), 'kind': next((o['kind'] for o in opts if o['kind']), None),
             'first_from_source_order': any(o['first_from_source_order'] for o in opts), 'options': opts, 'branches': sorted({b for o in opts for b in o['branches']})}
        lows = [0.0 if o['same_day'] else (o['days'][0] if o['days'] else None) for o in opts]
        highs = [0.0 if (o['same_day'] and not o['days']) else (o['days'][1] if o['days'] else None) for o in opts]
        lows = [x for x in lows if x is not None]
        highs = [x for x in highs if x is not None]
        if lows:
            r['days'] = [min(lows), max(highs or lows)]
        sds = [o['same_day'] for o in opts if o['same_day'] is not None]
        r['same_day'] = True if True in sds else (False if sds else None)
        r['condition'] = next((o['condition'] for o in opts if o['condition']), None)
        r['marks'] = ['하위 조건 · 「또는」 별 값(options)'] + sorted({mk for o in opts for mk in o['marks']})
        subs = {o.get('sub_condition') for o in opts if o.get('sub_condition')}
        r['by_sub_condition'] = len(subs) > 1
        if r['by_sub_condition']:  # 하위 조건이 갈리면 겉 칸을 섞지 않는다 — options[].sub_condition 별 값을 읽는다
            r['days'], r['same_day'], r['open_high'] = None, None, False
            r['marks'][0] = '하위 조건별 값(by_sub_condition — options[].sub_condition 별로 읽음)'
    else:
        r = _parse_one(t, lex)
        r['text'] = t
        r['options'] = None
    if ctx_same_day is not None and r['same_day'] is None:
        r['same_day'] = ctx_same_day
        r['marks'].append('같은 날 · 별도 세션 문맥(문장 머리)')
    return r


def _parse_one(t, lex):
    r = {'days': None, 'open_high': False, 'same_day': None, 'marks': [], 'condition': None, 'repeat': False, 'kind': None,
         'first_from_source_order': False, 'branches': []}
    force_none = False
    days_if_none = None
    for b in lex['branches']:
        if not re.search(b['pattern'], t):
            continue
        s = b['set']
        if b['id'] == 'L-NUM':
            rs = _num_ranges(t, lex)
            if rs:
                r['branches'].append(b['id'])
                r['days'] = [min(x[0] for x in rs), max(x[1] for x in rs)]
                r['open_high'] = any(x[2] for x in rs)
            continue
        r['branches'].append(b['id'])
        if 'kind' in s:
            r['kind'] = s['kind']
        if s.get('days', 'x') is None:
            force_none = True
        if 'same_day' in s and r['same_day'] is None:
            r['same_day'] = s['same_day']
        if s.get('mark'):
            r['marks'].append(s['mark'])
        if s.get('condition'):
            r['condition'] = s['condition']
        if s.get('repeat'):
            r['repeat'] = True
        if s.get('first_from_source_order'):
            r['first_from_source_order'] = True
        if s.get('days_if_none'):
            days_if_none = s['days_if_none']
    if force_none:
        r['days'] = None
        r['open_high'] = False
    elif r['days'] is None and days_if_none is not None:
        r['days'] = list(days_if_none)
    return r


def interval_empty(iv, lex):
    """원문에 간격 낱말이 있는데 숫자 칸 · 표시가 다 비었나."""
    if not iv or not iv.get('text'):
        return False
    if not re.search(lex['interval_words'], iv['text']):
        return False
    return iv['days'] is None and iv['same_day'] is None and not iv['marks'] and not iv.get('kind') and not iv.get('first_from_source_order')


def interval_unread(iv, lex):
    """원문 간격 낱말마다 그 낱말을 읽는 사전 갈래가 돌았나(word_branches) — 안 돈 낱말 목록."""
    if not iv or not iv.get('text'):
        return []
    fired = set(iv.get('branches') or [])
    return [w['word'] for w in lex['word_branches'] if re.search(w['word'], iv['text']) and not fired & set(w['branches'])]


# ───────── 충돌 하나로(사용자 10-30 · D-13b 바꿈) — 보수적 기본값 · 진짜 반대만 의료진 ─────────
# 규칙 문장은 decisions.conflict_resolution.rules(R1~R6). 여기는 그 규칙을 그대로 계산한다 — 행별 결정 없음.
def ep_keys(e):
    """끝점 → 엣지 키(엣지 만들 때와 같은 규칙)."""
    if e['level'] in ('해석 안 됨', '시술 아님'):
        return []
    if e['level'] == '복합(나눔)':
        return sorted({k for pp in e['parts'] for k in ep_keys(pp)})
    if e['level'] == '모든 시술':
        return ['all']
    if e['level'] == '계열 묶음':
        return ['bundle:' + '|'.join(e['families'])]
    if e['units']:
        return ['units:' + ','.join(e['units'])]
    return ['family:' + ','.join(e['families']) + (('#' + e['sub_family']) if e.get('sub_family') else '') + (('#' + e['technique']) if e.get('technique') else '')]


class UnitSets:
    """엣지 키 → 그 키가 닿는 단위 시술 집합(상속 I1 · I2 · I3 과 같은 범위). 단위 시술 후보 키는 후보 전부."""
    def __init__(self, units):
        self.K = {u['id']: u['key'] for u in units}
        self.UF = collections.defaultdict(set)
        for i, k in self.K.items():
            self.UF[k['family']].add(i)
        self.ALL = set(self.K)
        self.cache = {}

    def of(self, key):
        if key not in self.cache:
            if key == 'all':
                s = set(self.ALL)
            elif key.startswith('bundle:'):
                s = set().union(*[self.UF[f] for f in key[7:].split('|')])
            elif key.startswith('units:'):
                s = set(key[6:].split(','))
            elif key.startswith('family:'):
                body, *qs = key[7:].split('#')
                s = set().union(*[self.UF[f] for f in body.split(',')])
                for q in qs:
                    want = [x.strip() for x in q.split('|')]
                    hit = {x for x in s if any((self.K[x].get('sub_family') or '') == w or (self.K[x].get('technique') or '').startswith(w) for w in want)}
                    s = hit or s  # I2 — 키에 그 하위 · 기법 없는 계열은 계열 후보 전부
            else:
                s = set()  # 제품 · 원장 항목 키 — 단위 시술로 안 풀림(그 키 자신만)
            self.cache[key] = s
        return self.cache[key]

    def side(self, e):
        ks = ep_keys(e)
        return set().union(*[self.of(k) for k in ks]) if ks else set()


def cr_axes(texts, axes):
    """원문(간격 원문 · 끝점 원문 · 수식 · 하위 조건 원문) → 하위 조건 축 값(R1). 축마다 첫 갈래."""
    t = ' '.join(x for x in texts if x)
    out = {}
    for ax in axes:
        for v in ax['values']:
            if re.search(v['pattern'], t):
                out[ax['axis']] = v['value']
                break
    return out


def cr_units_of_claim(c, CR):
    """주장 → 비교 단위(간격 옵션이 있으면 옵션마다 — 원천이 하위 조건을 적은 것)."""
    iv = c.get('interval') or {}
    base = [iv.get('text'), c['a'].get('text'), c['b'].get('text'), c['a'].get('qualifier'), c['b'].get('qualifier'),
            ' '.join(c['a'].get('stripped_prefix') or []), ' '.join(c['b'].get('stripped_prefix') or [])]
    rows = ([(f"{c['id']}#{k}", o, [o.get('sub_condition'), o.get('text')]) for k, o in enumerate(iv.get('options') or [])]
            if iv.get('by_sub_condition') else [(c['id'], iv, [])])
    out = []
    for vid, o, extra in rows:
        ax = cr_axes(base + extra, CR['axes'])
        sd = o.get('same_day')
        marks = (o.get('marks') or []) + (iv.get('marks') or [])
        sep_label = sd is False and (any(m in CR['session_label_marks'] for m in marks) or 'L-SEP' in (o.get('branches') or []))
        days = o.get('days')
        if sd is True:
            ax.setdefault('세션', '같은 날')
        elif sep_label or (days and days[0] and days[0] > 0):
            ax.setdefault('세션', '별도 세션')
        out.append({'vid': vid, 'claim': c['id'], 'first': o.get('first'), 'days': days, 'open_high': bool(o.get('open_high')),
                    'same_day': None if sep_label else sd, 'axes': ax, 'sep_label': sep_label})
    return out


def cr_flip(x):
    return {'a': 'b', 'b': 'a'}.get(x, x)


def cr_fold(field, vals):
    """한 묶음(같은 하위 조건) 안 값 → (값, 규칙, 상태). R3 간격 더 긴 쪽 · R4 같은 날 불가 · R5 순서 반대 = 순서 단정 안 함 + 의료진."""
    if field == 'first':
        s = sorted({v for v in vals if v})
        if not s:
            return None, None, '정보 없음'
        if len(s) == 1:
            return s[0], None, '하나'
        return None, 'R5', '의료진 확인'
    if field == 'same_day':
        s = {v for v in vals if v is not None}
        if not s:
            return None, None, '정보 없음'
        if len(s) == 1:
            return s.pop(), None, '하나'
        return False, 'R4', '보수적 선택'
    ds = [v for v in vals if v]
    if not ds:
        return None, None, '정보 없음'
    v = ([max(d[0][0] for d in ds), max(d[0][1] for d in ds)], any(d[1] for d in ds))
    return v, (None if len({(tuple(d[0]), d[1]) for d in ds}) == 1 else 'R3'), ('하나' if len({(tuple(d[0]), d[1]) for d in ds}) == 1 else '보수적 선택')


def cr_put(o, field, v):
    if field == 'days':
        o['days'], o['open_high'] = (v[0], v[1]) if v else (None, False)
    else:
        o[field] = v


def cr_resolve(items, CR):
    """items = [(비교 단위, 그 엣지 · 쌍 방향으로 돌린 first)] → resolved 하나.
    필드마다: 비교 축(CR.field_axes) 값이 같은(또는 한쪽이 빈) 것끼리만 비교 → 묶음 값이 다 같으면 하나 · 다르면 by_sub_condition(R1) + 「조건 모름」 옵션(전부 접음)."""
    res = {'first': None, 'days': None, 'open_high': False, 'same_day': None, 'by_sub_condition': False, 'options': [],
           'field_status': {}, 'rules': [], 'alternatives': [], 'from_claims': sorted({vc['claim'] for vc, _ in items}), 'trace': {}}
    for field in ('first', 'same_day', 'days'):
        keys = CR['field_axes'][field]
        voters = []
        for vc, fo in items:
            if field == 'first':
                v = fo
            elif field == 'same_day':
                v = vc['same_day']
            else:
                v = (vc['days'], vc['open_high']) if vc['days'] and vc['days'] != [0, 0] and vc['same_day'] is not True and vc['days'][0] is not None else None
            if v is None:
                continue
            ax = {k: vc['axes'][k] for k in keys if vc['axes'].get(k)}
            if '순서' in keys and fo:
                ax['순서'] = fo
            voters.append((ax, v, vc['vid'], vc['claim']))
        if field == 'same_day' and any(ax.get('순서') for ax, *_ in voters):
            # R1 방향 축 — 먼저 하는 쪽(first)별 같은 날 값을 따로 남김(by_direction). 방향 안 적은 원문은 두 방향 모두에 들어감 · 방향 안 같은 묶음은 R4
            bd = {}
            for d_ in ('a', 'b'):
                mem = [(v, c) for ax, v, i, c in voters if ax.get('순서') in (d_, None)]
                v, rule, st = cr_fold('same_day', [m[0] for m in mem])
                bd[d_] = {'same_day': v, 'status': st, 'rule': rule, 'from': sorted({m[1] for m in mem})}
            res['by_direction'] = bd
        sigs = sorted({json.dumps(ax, ensure_ascii=False, sort_keys=True) for ax, *_ in voters if ax})
        groups = []
        for s in sigs or ['{}']:
            sg = json.loads(s)
            mem = [(v, i, c) for ax, v, i, c in voters if all(sg.get(k) == x for k, x in ax.items())]
            groups.append((sg, mem))
        outs = []
        for sg, mem in groups:
            v, rule, st = cr_fold(field, [m[0] for m in mem])
            outs.append((sg, v, rule, st, mem))
        distinct = {json.dumps(o[1], sort_keys=True) for o in outs}
        trace = []
        if len(outs) == 1 or len(distinct) == 1:
            v = outs[0][1]
            rules = sorted({o[2] for o in outs if o[2]})
            cr_put(res, field, v)
            res['field_status'][field] = '의료진 확인' if 'R5' in rules else ('보수적 선택' if rules else outs[0][3] if len(outs) == 1 else '하나')
            res['rules'] += rules
            for sg, v2, rule, st, mem in outs:
                trace.append({'sub_condition': sg, 'status': st, 'rule': rule, 'claims': sorted({m[2] for m in mem})})
                if rule:
                    res['alternatives'] += [{'field': field, 'claim': m[1], 'value': m[0] if field != 'days' else {'days': m[0][0], 'open_high': m[0][1]}, 'sub_condition': sg}
                                            for m in mem if m[0] != v2]
        else:
            res['by_sub_condition'] = True
            cr_put(res, field, None)
            res['rules'].append('R1')
            sts = [o[3] for o in outs]
            res['field_status'][field] = '조건 분리' + ('(+의료진 확인)' if '의료진 확인' in sts else '(+보수적 선택)' if '보수적 선택' in sts else '')
            for sg, v2, rule, st, mem in outs:
                o = {'sub_condition': sg, 'field': field, 'status': st, 'rule': rule, 'from': sorted({m[1] for m in mem})}
                cr_put(o, field, v2)
                res['options'].append(o)
                trace.append({'sub_condition': sg, 'status': st, 'rule': rule, 'claims': sorted({m[2] for m in mem})})
                if rule:
                    res['rules'].append(rule)
                    res['alternatives'] += [{'field': field, 'claim': m[1], 'value': m[0] if field != 'days' else {'days': m[0][0], 'open_high': m[0][1]}, 'sub_condition': sg}
                                            for m in mem if m[0] != v2]
            # 조건을 모를 때 = 전부 접음(가장 보수적) — 앱엔 이것 하나
            v, rule, st = cr_fold(field, [m[0] for _, mem in groups for m in mem])
            o = {'sub_condition': {CR['unknown_condition_key']: CR['unknown_condition_label']}, 'field': field,
                 'status': '조건 모름 → 전부 접음', 'rule': 'R1', 'from': sorted({m[1] for _, mem in groups for m in mem})}
            cr_put(o, field, v)
            res['options'].append(o)
        res['trace'][field] = trace
    res['rules'] = sorted(set(res['rules']))
    fs = res['field_status'].values()
    res['status'] = '의료진 확인' if any('의료진' in s for s in fs) else ('보수적 선택' if any('보수적' in s for s in fs) else ('조건 분리' if any(s.startswith('조건 분리') for s in fs) else '하나'))
    return res


def cr_view(r, straight):
    """앱이 읽는 값(방향 맞춤) — 전수 가드 비교용."""
    f = (lambda x: x) if straight else cr_flip
    bd = {f(k): v['same_day'] for k, v in (r.get('by_direction') or {}).items()}
    return json.dumps({'by_direction': bd, 'first': f(r['first']), 'days': r['days'], 'open_high': r['open_high'], 'same_day': r['same_day'],
                       'options': sorted(json.dumps({'sub_condition': o['sub_condition'], 'field': o['field'], 'first': f(o.get('first')),
                                                     'days': o.get('days'), 'open_high': o.get('open_high'), 'same_day': o.get('same_day')},
                                                    ensure_ascii=False, sort_keys=True) for o in r['options'])}, ensure_ascii=False, sort_keys=True)


GRADE_RANK = None  # decisions.conflict_resolution.grade_order 에서


def cr_wait_segments(text, CR):
    """대기 기간 원문 → [(깊이 축 값 | None, [개월 …])]. 문장 조각(, . ;)마다 개월 숫자 하나하나에 그 조각 안 가장 가까운 깊이 낱말(앞쪽 우선 · 없으면 뒤쪽)을 붙인다(R6 + R1)."""
    out = []
    ax = CR['wait_axes'][0]
    for seg in re.split(r'[,.;]', text or ''):
        hits = sorted((m.start(), v['value']) for v in ax['values'] for m in re.finditer(v['pattern'], seg))
        for m in re.finditer(r'(\d+)\s*(?:[~\-]\s*(\d+))?\s*개월', seg):
            before = [h for h in hits if h[0] < m.start()]
            after = [h for h in hits if h[0] >= m.end()]
            depth = before[-1][1] if before else (after[0][1] if after else None)
            out.append((depth, sorted({int(x) for x in m.groups() if x})))
    return out


def main(argv=None):
    AP = argparse.ArgumentParser()
    AP.add_argument('--source', help='원천 경로 덮어쓰기(고정 시험용)')
    AP.add_argument('--decisions', default=str(W / 'step8-decisions.json'))
    AP.add_argument('--step7', help='7단계 정본 덮어쓰기(고정 시험 — 끝점 어긋남)')
    AP.add_argument('--out', default=str(W), help='산출 폴더(고정 시험은 임시 폴더)')
    ARGS = AP.parse_args(argv)
    OUT = Path(ARGS.out)
    OUT.mkdir(parents=True, exist_ok=True)
    DEC = json.load(open(ARGS.decisions))
    SRCP = Path(ARGS.source or DEC['source']['path'])
    J = lambda p: json.load(open(p))
    CAN = DEC['canon']
    U = J(W / CAN['step5'])
    F = J(W / CAN['step2'])
    S3 = J(W / CAN['step3'])
    T4 = J(W / CAN['step4'])
    P1 = J(W / CAN['step1'])
    S6 = J(W / CAN['step6'])
    S7 = J(ARGS.step7 or (W / CAN['step7']))
    SMAP = J(W / CAN['source_map'])
    SRC_FILES = ['contraindications', 'synergy', 'treatment-sequence', 'treatment-optimization', 'problem-packages', 'pre-procedure-checklist',
                 'consent-checklist', 'patient-education', 'post-procedure-timeline', 'complications', 'anatomy-danger-zones', 'pih-risk',
                 'literature-evidence', 'procedure-profiles', 'taxonomy', 'extracted', 'combo-recipes', 'problem-combos']
    SRC = {f: J(SRCP / (f + '.json')) for f in SRC_FILES}
    LEX = DEC['interval_lexicon']
    LB = DEC['labels']
    OPEN, STALE = [], []

    def op(t, **kw):
        OPEN.append(dict(type=t, **kw))

    # ───────── 0. 이름 풀이(5단계 정본 · 장비 · 제품 · 계열 · 하위 · 기법 · 조사 사전) ─────────
    def norm(s):
        return re.sub(r'[\s\-_·]', '', (s or '').lower())

    UNITS = {u['id']: u for u in U['units']}
    FAM = {f['id']: f for f in F['families']}
    SITE_PARENT = {n['name']: n['parent'] for n in S3['nodes']}
    SITE_SYN = {}
    for n in S3['nodes']:
        SITE_SYN[norm(n['name'])] = n['name']
        for s in n.get('synonyms') or []:
            SITE_SYN.setdefault(norm(s['text']), n['name'])
    for nm in list(SITE_PARENT):
        if nm.endswith('(묶음)'):
            SITE_SYN.setdefault(norm(nm[:-4]), nm)

    def site_desc(site):
        out = {site}
        ch = True
        while ch:
            ch = False
            for k, p in SITE_PARENT.items():
                if p in out and k not in out:
                    out.add(k)
                    ch = True
        return out

    # 부위 올라가기(decisions.resolver.site_climb · 7단계 R21 과 같은 규칙 · 사용자 10-29) — 이름으로 잡은 단위 시술이 그 부위(또는 하위)에 없으면
    # 3단계 트리 상위 노드 자신 → 최상위 영역 「전체」 노드까지 올라가 그 층에 있는 것만 · 영역 경계 안 넘음 · 끝까지 없으면 계열만
    SITE_ROOT_WHOLE = {}
    for nm, par in SITE_PARENT.items():
        if not par:
            SITE_ROOT_WHOLE[nm] = (nm + ' 전체') if SITE_PARENT.get(nm + ' 전체') == nm else (None if nm.endswith('(묶음)') else nm)
    CLIMB_LOG = []

    def site_layers(site):
        out, a = [], SITE_PARENT.get(site)
        while a and SITE_PARENT.get(a):
            out.append(a)
            a = SITE_PARENT[a]
        root = site
        while SITE_PARENT.get(root):
            root = SITE_PARENT[root]
        w = SITE_ROOT_WHOLE.get(root)
        if w and w != site:
            out.append(w)
        return out

    def site_pick(us, site, where):
        """us(이름으로 잡은 단위 시술) → (그 부위 · 올라간 층의 단위 시술, 층) · 부위 없으면 그대로 · 끝까지 없으면 ([], None)"""
        us = sorted(us)
        if not us or not site or site not in SITE_PARENT:
            return us, '그대로'
        at = [x for x in us if UNITS[x]['key']['site'] in site_desc(site)]
        if at:
            return at, '부위 안'
        for lay in site_layers(site):
            r = [x for x in us if UNITS[x]['key']['site'] == lay]
            if r:
                CLIMB_LOG.append({'where': where, 'site': site, 'layer': lay, 'units': r})
                return r, lay
        CLIMB_LOG.append({'where': where, 'site': site, 'layer': None, 'units': [], 'dropped': us})
        return [], None

    def site_ep(level, via, us, site, where, basis=None, families=None):
        fams = sorted(set(families or []) | {UNITS[x]['key']['family'] for x in us})
        got, lay = site_pick(us, site, where)
        if lay is None:
            return ep('계열', via, families=fams, flag=f'이 부위 단위 시술 없음 · 계열만(부위 {site} · 상위 부위 · 영역 「전체」 노드까지 없음 · R21)', basis=basis)
        d = ep(level, via, units=got, families=families, basis=basis)
        if lay not in ('그대로', '부위 안'):
            d['site_layer'] = lay
            d['flag'] = (d.get('flag') or '') + f' · 상위 부위 {lay}(R21)'
        return d

    U_TEXT = collections.defaultdict(set)
    for u in U['units']:
        U_TEXT[norm(u['name'])].add(u['id'])
        for s in u['synonyms']:
            U_TEXT[norm(s['text'])].add(u['id'])
    DEV = collections.defaultdict(set)
    for d in U['device_name_synonyms']:
        DEV[norm(d['name'])].update(d['units'])
    F_TEXT = collections.defaultdict(set)
    for f in F['families']:
        F_TEXT[norm(f['name'])].add(f['id'])
        for s in f.get('synonyms') or []:
            F_TEXT[norm(re.sub(r'\(.*?\)', '', s).strip())].add(f['id'])
    for code, term in U['rules']['name']['family_term'].items():
        F_TEXT[norm(term)].add(code)
    SUB_TEXT = collections.defaultdict(set)
    for k, term in U['rules']['name']['sub_term'].items():
        fam, sub = k.split('|')
        SUB_TEXT[norm(term)].add((fam, sub))
    for k, term in U['rules']['name']['medium_term'].items():
        SUB_TEXT[norm(term)].add(('M8', k))
    for f in F['families']:
        for sub in f.get('sub_families') or []:
            SUB_TEXT[norm(re.sub(r'\(.*?\)', '', sub))].add((f['id'], sub))
            for mm in re.findall(r'\((.*?)\)', sub):
                for part in re.split(r'[·,]', mm):
                    SUB_TEXT[norm(part)].add((f['id'], sub))
    TECH_TEXT = collections.defaultdict(set)
    for k, term in U['rules']['name']['technique_term'].items():
        if term:
            TECH_TEXT[norm(term)].add(k)
    for n in T4['nodes']:
        TECH_TEXT[norm(n['name'])].add(n['id'])
    PL = {x['product']: x for x in U['product_links']}
    P_TEXT = collections.defaultdict(set)
    for it in P1['items']:
        if not it.get('active'):
            continue
        n = it['2_names']
        for t in [n['display_name']] + [s['name'] for s in n.get('search_names') or []]:
            P_TEXT[norm(t)].add(it['ledger_id'])
    RES = DEC['resolver']
    ALIAS = {}
    USED_ALIAS = set()
    for a in RES['alias']:
        ALIAS[norm(a['text'])] = a
        for i in a['target'].get('units') or []:
            if i not in UNITS:
                op('결정이 가리키는 단위 시술 없음', where=f"resolver.alias {a['text']}", unit=i)
        for f in [a['target'].get('family')] + (a['target'].get('family_set') or []):
            if f and f not in FAM:
                op('결정이 가리키는 계열 없음', where=f"resolver.alias {a['text']}", family=f)
    NOTE_F = RES['note_filters']

    def units_where(family=None, sub=None, technique=None, site=None, note=None):
        out = []
        for u in U['units']:
            k = u['key']
            if family and k['family'] != family:
                continue
            if sub and k.get('sub_family') != sub:
                continue
            if technique:
                t = k['technique']
                if not (t == technique or (t or '').startswith(technique)):
                    continue
            if site and k['site'] not in site_desc(site):
                continue
            if note in NOTE_F:
                nf = NOTE_F[note]
                ok_name = any(w in u['name'] for w in nf.get('name_contains') or [])
                ok_syn = any(w in s['text'] for s in u['synonyms'] for w in nf.get('synonym_contains') or [])
                if not (ok_name or ok_syn):
                    continue
            out.append(u['id'])
        return out

    def ep(level, via, units=None, family=None, sub=None, technique=None, flag=None, basis=None, qualifier=None, families=None):
        units = sorted(set(units or []))
        fams = set(families or ([family] if family else []))
        fams |= {UNITS[x]['key']['family'] for x in units}
        d = {'level': level, 'via': via, 'families': sorted(fams), 'sub_family': sub, 'technique': technique, 'units': units, 'n_units': len(units),
             'flag': flag or ('이름 일치' if len(units) == 1 and level == '단위 시술' else ('하나로 좁힘' if len(units) == 1 else ('후보 전부' if len(units) > 1 else None)))}
        if basis:
            d['basis'] = basis
        if qualifier:
            d['qualifier'] = qualifier
        return d

    def from_alias(a, site=None):
        tg, basis = a['target'], a['basis']
        if 'none' in tg:
            return ep('시술 아님', '조사 사전(결정)', flag='시술 아님 · 원장 밖 — 엣지 끝점 안 됨', basis=tg['none'])
        if tg.get('wildcard'):
            return ep('모든 시술', '조사 사전(결정)', flag='와일드카드', basis=basis)
        if 'units' in tg:
            return site_ep('단위 시술', '조사 사전(결정)', tg['units'], site, 'alias', basis=basis)
        if 'family_set' in tg:
            return ep('계열 묶음', '조사 사전(결정)', families=tg['family_set'], flag='묶음 낱말 · 후보 계열 전부', basis=basis, qualifier=tg.get('note'))
        fam, sub, tech, st, note = tg['family'], tg.get('sub'), tg.get('technique'), tg.get('site') or site, tg.get('note')
        if sub or tech or st or note in NOTE_F:
            lvl = '하위 계열' if sub else ('기법 조건' if tech else ('부위 조건' if st else '용도 조건'))
            us = units_where(fam, sub, tech, st, note)
            if not us and sub:
                us = units_where(fam, None, tech, st, note)
                if us:
                    return ep(lvl, '조사 사전(결정)', units=us, family=fam, sub=sub, technique=tech, basis=basis, qualifier=note,
                              flag='단위 시술 키에 이 하위 계열 없음 — 계열(+조건) 단위 시술 후보 전부 · 하위 원문 보관')
            if not us:
                return ep(lvl, '조사 사전(결정)', family=fam, sub=sub, technique=tech, basis=basis, qualifier=note, flag='조건에 맞는 단위 시술 없음 — 계열에서 멈춤')
            return ep(lvl, '조사 사전(결정)', units=us, family=fam, sub=sub, technique=tech, basis=basis, qualifier=note)
        return ep('계열', '조사 사전(결정)', family=fam, basis=basis, qualifier=note)

    def resolve_base(t, site):
        n = norm(t)
        if not n:
            return None
        if n in U_TEXT:
            return site_ep('단위 시술', '단위 시술 이름 · 동의어', U_TEXT[n], site, 'U_TEXT')
        if n in DEV:
            return site_ep('단위 시술', '장비 이름 동의어(10-27)', DEV[n], site, 'DEV')
        if n in ALIAS:
            USED_ALIAS.add(n)
            return from_alias(ALIAS[n], site)
        if n in P_TEXT:
            ids = sorted(P_TEXT[n])
            us, fams = set(), set()
            for i in ids:
                x = PL.get(i)
                if not x:
                    continue
                fams.add(x['family'])
                us.update(x['stored_units'] or x['inherited_candidates'])
            return site_ep('제품 → 단위 시술', '제품 이름(1단계) → 5단계 product_links', us, site, 'P_TEXT', basis='제품 ' + ','.join(ids), families=sorted(fams))
        if n in F_TEXT:
            fams = sorted(F_TEXT[n])
            if len(fams) == 1:
                if site:
                    us = units_where(fams[0], site=site)
                    if us:
                        return ep('부위 조건', '계열 + 부위', units=us, family=fams[0])
                return ep('계열', '계열 이름 · 동의어', family=fams[0])
            return ep('계열', '계열 이름 · 동의어', families=fams, flag='후보 계열 여럿')
        if n in SUB_TEXT:
            subs = sorted(SUB_TEXT[n])
            us = sorted({u for f, s in subs for u in units_where(f, s, site=site)})
            return ep('하위 계열', '하위 계열 낱말', units=us, families=sorted({f for f, s in subs}), sub=' | '.join(s for f, s in subs),
                      flag=None if us else '조건에 맞는 단위 시술 없음 — 계열에서 멈춤')
        if n in TECH_TEXT:
            ts = sorted(TECH_TEXT[n])
            us = sorted({u for tt in ts for u in units_where(technique=tt, site=site)})
            return ep('기법 조건', '기법 낱말', units=us, technique=' | '.join(ts))
        return None

    def clean_tail(t):
        prev = None
        while prev != t:
            prev = t
            for rx in RES['tail_regex']:
                t = re.sub(rx, '', t).strip()
            for w in sorted(RES['tail_words'], key=len, reverse=True):
                if t.endswith(' ' + w):
                    t = t[:-len(w)].strip()
        return t

    def intersect(base, site, strict):
        toks = [x for x in re.split(r'\s+', base) if x]
        if len(toks) < 2:
            return None
        cons = []
        for tk in toks:
            a = ALIAS.get(norm(tk))
            if a and 'family' in a['target']:
                cons.append(a['target'])
                USED_ALIAS.add(norm(tk))
            elif a and 'family_set' in a['target']:
                USED_ALIAS.add(norm(tk))  # 묶음 낱말(「RF 열시술」의 열시술) = 수식 — 앞 낱말이 이름
            elif norm(tk) in SUB_TEXT and len(SUB_TEXT[norm(tk)]) == 1:
                f, s = list(SUB_TEXT[norm(tk)])[0]
                cons.append({'family': f, 'sub': s})
            elif norm(tk) in TECH_TEXT:
                cons.append({'technique': sorted(TECH_TEXT[norm(tk)])[0]})
            elif norm(tk) in SITE_SYN:
                site = site or SITE_SYN[norm(tk)]
            elif norm(tk) in U_TEXT or norm(tk) in DEV:
                us = sorted(U_TEXT.get(norm(tk)) or DEV.get(norm(tk)))
                cons.append({'units': us})
            elif strict:
                return None
        if not cons:
            return None
        ucons = [c for c in cons if 'units' in c]
        if ucons:
            us = sorted(set.intersection(*[set(c['units']) for c in ucons]))
            if us:
                return ep('조건 일치(낱말 교집합)', '낱말 교집합', units=us, basis='낱말: ' + ' · '.join(toks))
            return None
        fams_ = [c['family'] for c in cons if c.get('family')]
        fam = fams_[-1] if fams_ else None
        sub = next((c['sub'] for c in cons if c.get('sub') and c.get('family') == fam), None)
        tech = next((c['technique'] for c in cons if c.get('technique')), None)
        us = units_where(fam, sub, tech, site)
        if us:
            return ep('조건 일치(낱말 교집합)', '낱말 교집합', units=us, family=fam, sub=sub, technique=tech, basis='낱말: ' + ' · '.join(toks))
        return None

    def bad_ep(e):
        return e['level'] == '해석 안 됨' or any(p.get('level') == '해석 안 됨' for p in e.get('parts', []))

    # 끝점 부위 낱말(품질 E · 10-30) — 끝점 원문에 3단계 부위 이름 · 강한 동의어(2자 이상 · 묶음 아님)가 있으면 그 부위를 site_hint 로(그 부위 · 올라간 층 단위 시술만)
    EP_SITE_KEYS = sorted({n['name'] for n in S3['nodes'] if not n['name'].endswith('(묶음)') and len(n['name']) >= 2 and n['name'] not in DEC['resolver']['endpoint_site_word_skip']}
                          | {x['text'] for n in S3['nodes'] for x in n.get('synonyms') or [] if not x.get('weak') and len(x['text']) >= 2 and re.search(r'[가-힣]', x['text']) and not n['name'].endswith('(묶음)')},
                          key=lambda x: (-len(x), x))
    EP_SITE_OF = {}
    for n in S3['nodes']:
        EP_SITE_OF[n['name']] = n['name']
        for x in n.get('synonyms') or []:
            EP_SITE_OF.setdefault(x['text'], n['name'])
    EP_SITE_LOG = []

    def ep_site_word(text):
        found = []
        t = text or ''
        for k in EP_SITE_KEYS:
            if k in t:
                nm = EP_SITE_OF[k]
                if nm not in found:
                    found.append(nm)
                t = t.replace(k, ' ')
        return found[0] if len(found) == 1 else None

    def resolve(text, code_hint=None, site_hint=None, mode='mixed'):
        """원천 이름 하나 → 끝점. 고르지 않는다(후보 전부 + 표시). mode=order 면 끝 낱말을 하나씩 떼며 푼다(순서 칸)."""
        raw = text
        t = (text or '').strip()
        if site_hint is None:
            sw = ep_site_word(t)
            if sw:
                site_hint = sw
                EP_SITE_LOG.append({'text': t, 'site': sw})
        stripped = []
        for p in RES['strip_prefix']:
            if re.match(r'^' + re.escape(p) + r'\s+', t):
                stripped.append(p)
                t = re.sub(r'^' + re.escape(p) + r'\s+', '', t)
        for rx in RES['cut_regex']:
            t = re.sub(rx, '', t).strip()
        m = re.match(r'^(M\d+|N\d+)-(.+)$', t)
        if m:
            code_hint = code_hint or m.group(1)
            t = m.group(2)
        t = re.sub(r'[.。]+$', '', t).strip()
        paren = re.findall(r'\((.*?)\)', t)
        base0 = re.sub(r'\(.*?\)', '', t).strip()
        base = base0 if resolve_base(base0, None) is not None else clean_tail(base0)
        site = site_hint
        qual = []
        for p in paren:
            if norm(p) in SITE_SYN:
                site = SITE_SYN[norm(p)]
            else:
                qual.append(p)
        r = resolve_base(base, site)
        if r is not None and r['level'] == '계열 묶음':
            for q in qual:  # 묶음 낱말 + 괄호 안 시술 이름 = 괄호(bundle_paren_rule)
                rq = resolve_base(clean_tail(q), site)
                if rq is not None and rq['level'] not in ('계열 묶음', '시술 아님'):
                    rq['qualifier_from_base'] = base
                    qual = [x for x in qual if x != q]
                    r = rq
                    break
        if r is None and paren:
            r = resolve_base(t, site)
        if r is None and qual:
            for q in qual:
                r = resolve_base(clean_tail(q), site)
                if r is None and re.search(r'/|\+|,| or | 또는 ', q):
                    r = resolve(q, None, site, mode)
                    if bad_ep(r):
                        r = None
                if r is not None:
                    r['qualifier_from_base'] = base
                    qual = [x for x in qual if x != q]
                    break
        if r is None:
            parts = [x.strip() for x in re.split(r'\s*(?:/|\+|,| or | 또는 )\s*', base) if x.strip()]
            if len(parts) > 1:
                subs = [resolve(x, None, site, mode) for x in parts]
                bad = [s for s in subs if s['level'] == '해석 안 됨']
                r = {'level': '복합(나눔)', 'via': '「/ + , or 또는」로 나눔', 'parts': [dict(s, text=x) for x, s in zip(parts, subs)],
                     'families': sorted({f for s in subs for f in s['families']}), 'units': sorted({u for s in subs for u in s['units']}),
                     'sub_family': None, 'technique': None, 'flag': '복합 — 원소마다 끝점' + (' · 못 푼 원소 있음' if bad else '')}
                r['n_units'] = len(r['units'])
        if r is None:
            r = intersect(base, site, strict=(mode != 'order'))
        if r is None and mode == 'order':
            toks = base.split()
            while len(toks) > 1 and r is None:
                toks = toks[:-1]
                r = resolve_base(' '.join(toks), site) or intersect(' '.join(toks), site, strict=False)
                if r is not None:
                    r['dropped_tail'] = base[len(' '.join(toks)):].strip()
        if r is None:
            r = ep('해석 안 됨', '없음', flag='unresolved_name_ref')
        if qual:
            r['qualifier'] = ' · '.join(filter(None, [r.get('qualifier')] + qual))
        if code_hint:
            r['source_code'] = code_hint
            if r['families'] and code_hint not in r['families'] and r['level'] not in ('복합(나눔)', '계열 묶음'):
                r['code_mismatch'] = f'원천 코드 {code_hint} ↔ 해석 계열 {",".join(r["families"])}'
        if stripped:
            r['stripped_prefix'] = stripped
        r['text'] = raw
        return r

    # 사람 조건 사전(B04)
    CONDS = DEC['conditions']

    def cond_match(text):
        return [c['id'] for c in CONDS if re.search(c['pattern'], text or '')]

    # 7단계 고민 노드(U8-2 — 고민 낱말은 7단계 고민 노드 하나만)
    CON7 = S7['concerns']
    CONCERN_BY_WORD = {}
    for grp in ('categories', 'subcategories', 'extra_items'):
        for x in CON7.get(grp) or []:
            if grp != 'categories' and not x.get('node', True):
                continue
            for w in [x.get('concern'), x.get('source_label'), x.get('name'), x.get('title')]:
                if w and (x.get('kind') in (None, '고민', '고민(원천 밖 · 결정)') or grp == 'categories'):
                    CONCERN_BY_WORD.setdefault(norm(w), x['id'])
    COMBO7 = {(c['source'], c['source_id']): c for c in S7['combos']}
    CC7 = collections.defaultdict(dict)
    for e in S7['edges']:
        if e['source'].startswith('③'):  # 7단계 R27 — 합친 엣지는 source_ids 의 CC 마다
            for sid_ in e.get('source_ids') or [e['source_id']]:
                CC7[sid_][(e.get('evidence') or {}).get('name')] = e

    def concern_of_word(w):
        return CONCERN_BY_WORD.get(norm(w))

    # ───────── A. 시술↔시술 주장 ─────────
    claims, attrs, cond_claims, avoids, landed = [], [], [], [], collections.defaultdict(list)
    seq_texts = collections.defaultdict(list)  # 7단계 메모 대조용(원천 칸 → 처리한 원문)

    def land(source, idx, what):
        landed[(source, str(idx))].append(what)

    def Cl(**kw):
        kw['id'] = f'R8-{len(claims) + 1:04d}'
        kw.setdefault('gate_status', '자동(규칙)')
        kw.setdefault('evidence', [])
        claims.append(kw)
        land(kw['source'], kw['source_index'], kw['id'])
        return kw

    def side_first(head, a, b):
        """원문 머리말(「X 먼저」 · 「X N주 후」 · 「X →」)의 X 가 어느 쪽인가 — 글자 포함 또는 이름 풀이 계열 교집합. 둘 다 · 아무도 아니면 None."""
        if not head:
            return None
        h = norm(re.sub(r'\(.*?\)', '', head))
        if not h:
            return None
        def txt(e):
            return norm(re.sub(r'\(.*?\)', '', re.sub(r'^(M\d+|N\d+)-', '', e.get('text') or '')))
        ta, tb = txt(a), txt(b)
        fa = bool(ta) and (h in ta or ta in h)
        fb = bool(tb) and (h in tb or tb in h)
        if fa != fb:
            return 'a' if fa else 'b'
        hr = resolve(head, mode='order')
        hf = set(hr['families'])
        if not hf:
            return None
        ia, ib = bool(hf & set(a['families'])), bool(hf & set(b['families']))
        if ia != ib:
            return 'a' if ia else 'b'
        return None

    def mk_iv(text, first=None, basis=None, ctx=None, extra=None):
        iv = parse_interval(text, LEX, ctx) if text else ({'text': None, 'days': None, 'open_high': False, 'same_day': ctx, 'marks': [], 'condition': None,
                                                             'repeat': False, 'kind': None, 'first_from_source_order': False, 'options': None, 'branches': []}
                                                            if ctx is not None else None)
        if iv is None and (first or extra):
            iv = {'text': None, 'days': None, 'open_high': False, 'same_day': None, 'marks': [], 'condition': None, 'repeat': False, 'kind': None,
                  'first_from_source_order': False, 'options': None, 'branches': []}
        if iv is not None:
            iv['first'] = first
            iv['first_basis'] = basis
            if iv.get('by_sub_condition') and first is not None:
                iv['first'], iv['first_basis'] = None, None  # 겉 first 도 비움 — 옵션별 first 는 그 옵션 원문 머리말에서
            if extra:
                for k, v in extra.items():
                    if k == 'marks':
                        iv['marks'] += v
                    elif v is not None:
                        iv[k] = v
        return iv

    # A1 contraindications.rules — 계열 코드 그대로(C4 상속)
    for i, r in enumerate(SRC['contraindications']['rules']):
        a = ep('계열', '원천 시술군 코드', family=r['from'])
        b = ep('계열', '원천 시술군 코드', family=r['to'])
        a['text'] = r['from_name']
        b['text'] = r['to_name']
        for code in (r['from'], r['to']):
            if code not in FAM:
                op('원천 시술군 코드가 2단계 계열에 없음', where=f'contraindications.rules[{i}]', family=code)
        txt = r['interval'] + ' ' + r['note']
        heads = re.findall(r'([^\s,.():/]+)\s*먼저', txt) + [x for x in re.findall(r'(?:^|[\s(:])([^\s,.():/→]+)\s*→', txt)]
        sides = {side_first(h, a, b) for h in heads} - {None}
        first = sides.pop() if len(sides) == 1 else None
        extra = {'marks': ['순서 원문 갈림(양쪽)']} if len(sides) > 1 else None
        civ = mk_iv(r['interval'], first, ('원문 「' + ' · '.join(heads) + '」') if first else None, extra=extra)
        for o in (civ or {}).get('options') or []:
            oh = re.findall(r'([^\s,.():/]+)\s*먼저', o['text']) + re.findall(r'(?:^|[\s(:])([^\s,.():/→]+)\s*→', o['text'])
            osd = {side_first(h, a, b) for h in oh} - {None}
            o['first'] = osd.pop() if len(osd) == 1 else None
            o['first_basis'] = ('원문 「' + ' · '.join(oh) + '」') if o['first'] else None
        Cl(source='contraindications.rules', source_index=i, text=f"{r['from']}↔{r['to']} {r['interval']}", kind='병행 · 간격', a=a, b=b, directed=False,
           interval=civ,
           level_original=r['level'], level_site=LB['contra_level_site'][r['level']], reason=r['note'], rule='구조 칸(from · to · level · interval · note)',
           lowering='계열(원천 시술군 코드 — 단위 시술은 조회 때 상속 · C4)', evidence_kind='원천 표기 없음')

    # A2 synergy.links
    for i, l in enumerate(SRC['synergy']['links']):
        a = resolve(l['from'], l['from_category'])
        b = resolve(l['to'], l['to_category'])
        tm = l.get('timing') or ''
        iv = parse_interval(tm, LEX)
        first, basis = None, None
        if l['type'] == '다음에':
            m = re.match(r'^(.+?)\s*(?:직후|\d)', tm) or re.match(r'^(.+?)\s*후\s', tm)
            if m:
                first = side_first(m.group(1), a, b)
                basis = f'원문 머리말 「{m.group(1).strip()}」' if first else None
            if first is None and iv and iv['first_from_source_order']:
                first, basis = 'a', '원문 「순차」 — from → to'
        kind = (iv or {}).get('kind') or LB['synergy_type'][l['type']]
        Cl(source='synergy.links', source_index=i, text=f"{l['from']} {l['type']} {l['to']} · {tm}", kind=kind, a=a, b=b, directed=(l['type'] == '다음에'),
           interval=mk_iv(tm, first, basis), type_original=l['type'], reason=l.get('reason'), target=l.get('target'), rule='구조 칸(from · to · type · timing)',
           lowering='이름 해석(5단계 정본) — 원천 코드는 source_code', evidence_kind='원천 표기 없음')

    TS = SRC['treatment-sequence']
    OPT = SRC['treatment-optimization']
    moved_to_conditions = []

    def person_side(e, text):
        """끝점이 시술로 안 풀리고 사람 조건 사전에 걸리면 조건(C10)."""
        return e['level'] == '해석 안 됨' and cond_match(text)

    # A3 incompatible_same_day
    for i, x in enumerate(TS['incompatible_same_day']):
        pr = x['pair']
        if len(pr) == 1:
            m = re.match(r'^(.+?)\s*주입 후\s*(.+)$', pr[0])
            if not m:
                op('원천 쌍 칸 꼴 밖', where=f'treatment-sequence.incompatible_same_day[{i}]', text=pr[0])
                continue
            at, bt, first = m.group(1), m.group(2), 'a'
        else:
            at, bt, first = pr[0], pr[1], None
        a, b = resolve(at), resolve(bt)
        if person_side(a, at) or person_side(b, bt):
            moved_to_conditions.append({'source': 'treatment-sequence.incompatible_same_day', 'source_index': i, 'pair': pr, 'reason': x['reason'],
                                        'person': at if person_side(a, at) else bt, 'proc': bt if person_side(a, at) else at, 'grade': 'iso_same_day'})
            continue
        Cl(source='treatment-sequence.incompatible_same_day', source_index=i, text=' ↔ '.join(pr), kind='같은 날 불가', a=a, b=b, directed=(len(pr) == 1),
           interval=mk_iv(None, first, '원문 「주입 후」' if first else None, extra={'same_day': False, 'marks': ['같은 날 불가(구조 칸)']}),
           reason=x['reason'], rule='구조 칸(pair)', lowering='이름 해석', evidence_kind='원천 표기 없음(reason 안 인용 표기는 원문)', pair_original=pr)

    # A4 minimum_intervals
    for i, x in enumerate(TS['minimum_intervals']):
        a, b = resolve(x['from']), resolve(x['to'])
        if person_side(a, x['from']) or person_side(b, x['to']):
            moved_to_conditions.append({'source': 'treatment-sequence.minimum_intervals', 'source_index': i, 'pair': [x['from'], x['to']], 'reason': x['reason'],
                                        'person': x['from'], 'proc': x['to'], 'min_months': x.get('min_months'), 'evidence_text': x['source'], 'grade': 'iso_wait'})
            continue
        ivt = f"{x['min_days']}일 이상" if 'min_days' in x else f"{x['min_months']}개월 이상"
        same_self = set(a['families']) == set(b['families']) and bool(re.search(r'재시술', x['to']))
        extra = {'same_day': True} if x.get('min_days') == 0 else None
        Cl(source='treatment-sequence.minimum_intervals', source_index=i, text=f"{x['from']} → {x['to']}", kind=('재시술 간격(자기 쌍)' if same_self else '간격'),
           a=a, b=b, directed=True, interval=mk_iv(ivt, 'a', '원문 from → to', extra=extra), min_days=x.get('min_days'), min_months=x.get('min_months'),
           reason=x['reason'], evidence_text=x['source'], rule='구조 칸(from · to · min_days)', lowering='이름 해석', evidence_kind='원천 source 칸',
           self_pair=('자기 쌍 — SPEC-004 self_relation_skipped 대상 · 계열 「재시술 간격」 속성 후보' if same_self else None))

    # A5 sequence_order(쌍 아님 — 같은 날 순위 표)
    sequence_rank = []
    for x in TS['sequence_order']:
        sequence_rank.append({'order': x['order'], 'phase': x['phase'], 'categories': [dict(resolve(c, mode='order'), text=c) for c in x['categories']], 'reason': x['reason']})
        land('treatment-sequence.sequence_order', x['order'], 'sequence_rank')

    # ───────── 문장 패턴(U8-1 — 행별 대응표 대신) ─────────
    SENT = DEC['sentence']
    PATS = [dict(p, rx=re.compile(p['regex'])) for p in SENT['patterns']]
    QW = r'(?:' + '|'.join(sorted(map(re.escape, SENT['qualifier_words']), key=len, reverse=True)) + r')'

    def split_qual(t):
        q = re.findall(QW, t)
        t2 = re.sub(QW + r'[·\s]*', ' ', t).strip()
        return t2, ('·'.join(q) if q else None)

    def chain_elems(text):
        """화살표 문장 → 원소 [{name, iv, paren_iv, carry}] (원천 순서 그대로)."""
        segs = [s.strip() for s in re.split(r'→', text) if s.strip()]
        out, carry = [], None
        for s in segs:
            s1 = re.sub(r'\.\s.*$', '', s).strip()
            if re.fullmatch(r'(\d+(?:\s*[\-~]\s*\d+)?\s*(주|개월|일|회)\s*(간격|후|회복)?\s*(반복|유지|회복)?|유지|반복)', s1):
                carry = s1
                continue
            iv = None
            m = re.match(r'^(?P<IV>\d+(?:\s*[\-~]\s*\d+)?\s*(?:주|개월|일)\s*(?:후부터|후|간격)|같은\s*날|같은날|직후|사이사이|이후)\s*(?P<REST>.*)$', s1)
            if m:
                iv, s1 = m.group('IV'), m.group('REST')
            piv = ' · '.join(p for p in re.findall(r'\(([^()]*)\)', s1) if re.search(LEX['interval_words'], p))
            trail = re.search(r'\s(동시|즉시)\s*도포', s1)
            if trail:
                iv = ' · '.join(filter(None, [iv, trail.group(1)]))
            name = s1
            out.append({'seg': s, 'name': name, 'iv': ' · '.join(filter(None, [iv, piv])) or None, 'carry': carry})
            carry = None
        return out, carry

    def narrow(e, fam):
        """후보 계열이 여럿인 하위 계열 낱말 + 행의 계열(제품 칸) = 그 계열만(family_hint_rule)."""
        if fam and e['level'] == '하위 계열' and len(e['families']) > 1 and fam in e['families']:
            e = dict(e, families=[fam], units=[u for u in e['units'] if UNITS[u]['key']['family'] == fam], flag=(e.get('flag') or '') + f' · 행 계열 {fam} 로 좁힘')
            e['n_units'] = len(e['units'])
        return e

    def emit_pair(src, idx, row_text, pid, at, bt, ivt, first_side, kind, ctx_sd, extra_ctx, mode, F_word=None, site_hint=None, strength=None, cond=None, fam_hint=None):
        a = narrow(resolve(at, site_hint=site_hint, mode=mode), fam_hint)
        b = resolve(bt, site_hint=site_hint, mode=mode)
        # 사람 조건이 주어인 「A 후 N 내 B 금지」 = 확인 조건(선탠 · 활성 여드름)
        if person_side(a, at):
            CC(source=src, source_index=idx, target=b, target_level=b['level'], text=row_text, detail=ivt, grade_original='금지', grade_site='금기 조합',
               grade3=LB['grade3']['forbid'], conditions=cond_match(at), kind='사람 조건', wait=mk_iv(ivt + ' 금지' if ivt else None), rule=pid, where=cond)
            return 'cond'
        first, basis = None, None
        if first_side == 'A':
            first, basis = 'a', f'원문 패턴 {pid}'
        elif first_side == 'F' and F_word:
            first = side_first(F_word, a, b)
            basis = f'원문 「{F_word} 먼저」' if first else None
        iv_text = ivt
        if ivt and kind in ('간격 금기', '같은 날 불가') and not re.search(r'금지|불가', ivt):
            iv_text = ivt + ' 금지'
        iv = mk_iv(iv_text, first, basis, ctx_sd, extra=extra_ctx)
        k = (iv or {}).get('kind') or kind or '순서 · 간격(문장)'
        Cl(source=src, source_index=idx, text=row_text, kind=k, a=a, b=b, directed=first is not None, interval=iv, rule=pid, condition=cond,
           strength_original=strength, lowering='문장 패턴 규칙(U8-1)', evidence_kind=EKIND.get(src, '원천 표기 없음'))
        return 'claim'

    def emit_chain(src, idx, row_text, text, ctx_sd, mode, pid, strength=None, cond=None, site_hint=None):
        els, tail_carry = chain_elems(text)
        made = 0
        for x, y in zip(els, els[1:]):
            a = resolve(x['name'], site_hint=site_hint, mode=mode)
            b = resolve(y['name'], site_hint=site_hint, mode=mode)
            extra = {'marks': []}
            if y['carry']:
                if re.search(r'반복|유지', y['carry']):
                    extra['marks'].append(f"앞 시술 반복(원문 「{y['carry']}」)")
                    extra['repeat_text'] = y['carry']
            ivt = ' · '.join(filter(None, [y['iv'], (y['carry'] if y['carry'] and not re.search(r'반복|유지', y['carry']) else None)])) or None
            iv = mk_iv(ivt, 'a', '원문 화살표 순서', ctx_sd, extra=extra if extra['marks'] or extra.get('repeat_text') else None)
            Cl(source=src, source_index=idx, text=row_text, kind=(iv or {}).get('kind') or '순서(문장 화살표)', a=a, b=b, directed=True, interval=iv,
               rule=pid, segs=[x['seg'], y['seg']], condition=cond, strength_original=strength, lowering='문장 분해(화살표) — 원문 보관',
               evidence_kind=EKIND.get(src, '원천 표기 없음'))
            made += 1
        return made, els, tail_carry

    def chain_all_resolved(text):
        els, _ = chain_elems(text)
        return len(els) >= 2 and all(not bad_ep(resolve(e['name'], mode='mixed')) for e in els)

    def parse_sentence(src, idx, row_text, sent, mode, ctx=None):
        """문장 하나 → 패턴 매칭 · 남은 꼬리로 다시(절 단위). 반환 = 만든 수 · 마지막 쌍 B(생략 상대용)."""
        ctx = ctx or {}
        made = 0
        last_b = ctx.get('last_b')
        rest = sent.strip()
        guard = 0
        while rest and guard < 12:
            guard += 1
            hit = None
            for p in PATS:
                if p.get('only_order_mode') and mode != 'order':
                    continue
                m = p['rx'].search(rest)
                if not m:
                    continue
                g = m.groupdict()
                e = p['emit']
                if e == 'concern_avoid':
                    cid = concern_of_word(g['C'])
                    if not cid:
                        continue
                    bt, q = split_qual(g['B'])
                    AV(src, idx, row_text, [cid], bt, q, p['id'], f"원문 고민 낱말 「{g['C']}」 → 7단계 {cid}", ctx)
                elif e == 'row_concern_avoid':
                    if not ctx.get('row_concerns'):
                        continue
                    bt, q = split_qual(g['B'])
                    if not q and not bad_ep(resolve(bt)):
                        pass
                    AV(src, idx, row_text, ctx['row_concerns'], bt, q, p['id'], ctx.get('row_concern_basis'), ctx)
                elif e == 'condition_forbid':
                    ks = cond_match(g['K'])
                    if not ks:
                        continue
                    b = resolve(g['B'])
                    CC(source=src, source_index=idx, target=b, target_level=b['level'], text=row_text, grade_original='금지', grade_site='금기 조합',
                       grade3=LB['grade3']['forbid'], conditions=ks, kind='사람 조건', rule=p['id'], where=ctx.get('where'), strength_original=ctx.get('strength'))
                elif e == 'chain':
                    sd = None
                    if re.search(r'같은\s*날|같은날', g['CTX']):
                        sd = True
                    elif re.search(r'별도\s*세션', g['CTX']):
                        sd = False
                    n, els, _ = emit_chain(src, idx, row_text, g['REST'], sd, mode, p['id'], ctx.get('strength'), ctx.get('cond'))
                    if els:
                        last_b = els[-1]['name']
                elif e == 'pair':
                    if p['id'] == 'S-AFTERGENERIC' and '→' in rest:
                        continue
                    site = (g.get('SITE') or '').strip()
                    ivt = ' '.join(filter(None, [g.get('IV'), site and '같은 부위'])) or None
                    r = emit_pair(src, idx, row_text, p['id'], g['A'], g['B'], ivt, p.get('first'), p.get('kind'), ctx.get('same_day'), None, mode,
                                  F_word=g.get('F'), site_hint=ctx.get('site'), strength=ctx.get('strength'), cond=ctx.get('cond'), fam_hint=ctx.get('family'))
                    last_b = g['B']
                elif e == 'first_or_gap':
                    emit_pair(src, idx, row_text, p['id'] + '#순서', g['A'], g['B'], None, 'F', '순서(문장)', None, None, mode, F_word=g['F'],
                              strength=ctx.get('strength'), cond=ctx.get('cond'))
                    # 반대 방향 간격 — F 가 아닌 쪽이 먼저일 때 N 이상
                    other = g['B'] if side_first(g['F'], resolve(g['A']), resolve(g['B'])) == 'a' else g['A']
                    fw = g['A'] if other == g['B'] else g['B']
                    emit_pair(src, idx, row_text, p['id'] + '#간격', other, fw, g['IV'], 'A', '간격', None, None, mode, strength=ctx.get('strength'), cond=ctx.get('cond'))
                    last_b = g['B']
                elif e == 'gap_or_first':
                    emit_pair(src, idx, row_text, p['id'] + '#간격', g['A'], g['B'], g['IV'], 'A', '간격', None, None, mode, strength=ctx.get('strength'), cond=ctx.get('cond'))
                    emit_pair(src, idx, row_text, p['id'] + '#순서', g['A'], g['B'], None, 'F', '순서(문장)', None, None, mode, F_word=g['F'],
                              strength=ctx.get('strength'), cond=ctx.get('cond'))
                    last_b = g['B']
                elif e in ('list_pair', 'list_ellipsis'):
                    partner = g.get('B') or last_b
                    if not partner:
                        continue
                    for it in [x.strip() for x in re.split(r'[·,]', g['LIST']) if x.strip()]:
                        emit_pair(src, idx, row_text, p['id'], it, partner, g['IV'], None, '병행 · 간격(문장)', None,
                                  {'marks': ['생략 상대 = 앞 절 대상(ellipsis_rule)']} if e == 'list_ellipsis' else None, mode,
                                  strength=ctx.get('strength'), cond=ctx.get('cond'))
                hit = (p, m)
                made += 1
                break
            if hit is None:
                # 화살표만 있는 문장(괄호 안 화살표 우선)
                pc = re.search(SENT['paren_chain'], rest)
                ctext = pc.group(1) if pc else (rest if '→' in rest else None)
                if ctext and (mode == 'order' or chain_all_resolved(ctext)):
                    n, els, _ = emit_chain(src, idx, row_text, ctext, ctx.get('same_day'), mode, 'S-ARROW', ctx.get('strength'), ctx.get('cond'), ctx.get('site'))
                    made += n
                    if els:
                        last_b = els[-1]['name']
                break
            rest = rest[hit[1].end():]
            mm = re.search(r',\s*', rest)
            if not mm:
                break
            rest = rest[mm.end():]
        return made, last_b

    def sentences(text):
        return [s for s in re.split(SENT['split_sentence'], text or '') if s.strip()]

    EKIND = {'treatment-optimization.by_concern.sequence': '3-AI 합의(consensus_method)', 'treatment-optimization.by_concern.contraindicated_combos': '3-AI 합의(consensus_method)',
             'treatment-optimization.combination_rules': '원천 evidence 칸'}

    def AV(src, idx, row_text, cids, bt, q, pid, basis, ctx):
        b = resolve(bt)
        av = {'id': f'AV8-{len(avoids) + 1:03d}', 'edge_type': DEC['avoid_edge_type']['name'], 'label': DEC['avoid_edge_type']['label_ko'],
              'from_concerns': cids, 'to': b, 'qualifier': q, 'text': row_text, 'source': src, 'source_index': idx, 'rule': pid, 'concern_basis': basis,
              'grade_original': '금지', 'where': ctx.get('where'), 'strength_original': ctx.get('strength'), 'evidence_text': ctx.get('evidence_text')}
        for c in cids:
            if not any(x['id'] == c for g in ('categories', 'subcategories', 'extra_items') for x in CON7.get(g) or []):
                op('7단계 끝점 어긋남 — 고민 노드 없음', where=f'{src}[{idx}]', concern=c)
        avoids.append(av)
        land(src, idx, av['id'])

    def CC(**kw):
        kw['id'] = f'K8-{len(cond_claims) + 1:04d}'
        cond_claims.append(kw)
        land(kw['source'], kw['source_index'], kw['id'])
        return kw

    def attr(source, idx, attach, text, **kw):
        a = dict(source=source, source_index=idx, attach=attach, text=text, **kw)
        iv = parse_interval(text, LEX) if re.search(LEX['interval_words'], text or '') else None
        if iv:
            a['interval'] = iv
        attrs.append(a)
        land(source, idx, 'attr')
        return a

    # A6 principles(원문 문장 — 패턴 규칙)
    principles_text_only = []
    for idx, ptxt in enumerate(TS['principles']):
        made = 0
        for s in sentences(ptxt):
            n, _ = parse_sentence('treatment-sequence.principles', idx, ptxt, s, 'mixed')
            made += n
        if not made:
            principles_text_only.append({'index': idx, 'text': ptxt, 'why': '패턴 · 시술 쌍 없음 — 원문만(B06 ⑥ 파생 계산 안 함)'})
            land('treatment-sequence.principles', idx, 'text_only')

    # A7 combination_rules — detail 문장 → (없으면) rule 제목 → 이름 없는 간격 문장은 앞 주장에 붙임 → 이름 하나면 계열 원문 속성
    def row_rules(src, idx, title, detail, strength, evidence_text, ctx_extra=None):
        start = len(claims)
        n_av, n_cc = len(avoids), len(cond_claims)
        ctx = dict(strength=strength, evidence_text=evidence_text, **(ctx_extra or {}))
        made = 0
        orphan = []
        for s in sentences(detail):
            n, _ = parse_sentence(src, idx, detail, s, 'mixed', ctx)
            if n:
                made += n
            elif re.fullmatch(SENT['orphan_interval_regex'], s.strip().rstrip('.').strip()):
                orphan.append(s)
        if not made and title:
            for s in sentences(title):
                n, _ = parse_sentence(src, idx, title, s, 'mixed', ctx)
                made += n
        new = claims[start:]
        for c in new:
            c['evidence_text'] = evidence_text
            c['rule_title'] = title
        if orphan and new:
            for s in orphan:
                tgt = new[-1]
                merged = ' · '.join(filter(None, [(tgt['interval'] or {}).get('text'), s]))
                old = tgt['interval'] or {}
                tgt['interval'] = mk_iv(merged, old.get('first'), old.get('first_basis'))
                tgt['interval_merged_from'] = s
        return made, len(avoids) - n_av, len(cond_claims) - n_cc

    for i, r in enumerate(OPT['combination_rules']):
        st = {'priority': r['priority'], 'priority_site': LB['opt_priority_site'].get(r['priority']), 'consensus': r['consensus']}
        made, nav, ncc = row_rules('treatment-optimization.combination_rules', i, r['rule'], r['detail'], st, r['evidence'])
        if not made:
            names = [resolve(clean := x, mode='mixed') for x in re.split(r'\s*(?:=|\(|\s)\s*', r['rule'])[:2]]
            fam = next((e['families'] for e in names if e['level'] not in ('해석 안 됨',) and len(e['families']) == 1), None)
            if fam:
                attr('treatment-optimization.combination_rules', i, f'family:{fam[0]}', r['detail'], what='계열 안전 원문(쌍 없음 · 이름 하나 — title_rule)',
                     rule_title=r['rule'], evidence_text=r['evidence'], priority=r['priority'])
            else:
                op('규칙 행에서 쌍 · 속성 행선지가 안 나옴', where=f'treatment-optimization.combination_rules[{i}]', text=r['rule'])

    # A8 by_concern(sequence · contraindicated_combos) — 행 = 고민 × 중증도 · 앵커 = 7단계 조합(RC-OP)
    for ci, c in enumerate(OPT['by_concern']):
        for si, s in enumerate(c['severity_levels']):
            where = f"{c['concern']} · {s['level']}"
            combo = COMBO7.get(('treatment-optimization.by_concern', f"{c['concern']}|{s['level']}"))
            if combo is None:
                op('7단계 끝점 어긋남 — 최적화 행 조합 없음', where=f'treatment-optimization.by_concern[{ci}].severity_levels[{si}]', text=where)
                anchor = []
            else:
                anchor = combo['anchor']['concern'] if isinstance(combo['anchor']['concern'], list) else combo['anchor'].get('concerns') or []
            st = {'evidence_level': s['evidence_level'], 'site': LB['opt_evidence_site'].get(s['evidence_level'])}
            cond = {'concern_ids': anchor, 'severity': s['level'], 'combo': combo['id'] if combo else None, 'source_label': where}
            seq = s.get('sequence') or ''
            idx = f'{ci}.{si}'
            parts = [p for p in re.split(r'\.\s*또는\s*', seq) if p.strip()]
            made = 0
            for part in parts:
                sd = None
                m = re.match(r'^(같은\s*날|같은날|별도\s*세션)\s*:\s*', part)
                if m:
                    sd = not re.search('별도', m.group(1))
                    part = part[m.end():]
                if '→' in part:
                    n, els, tail = emit_chain('treatment-optimization.by_concern.sequence', idx, seq, part, sd, 'order', 'S-ARROW', st, cond)
                    made += n
                    if n == 0:
                        attr('treatment-optimization.by_concern.sequence', idx, f"7단계 추천 조합 {cond['combo']} 속성(시술 하나 · 반복 간격 원문)", part)
                        made += 1
                else:
                    attr('treatment-optimization.by_concern.sequence', idx, f"7단계 추천 조합 {cond['combo']} 속성", part)
                    made += 1
            seq_texts['treatment-optimization.sequence'].append(seq)
            # 금기 조합 — 행 고민 = 중증도 이름 안 고민 낱말(없으면 앵커 전부)
            sev_words = [w for w in re.findall(r'[가-힣A-Za-z]+', s['level']) if concern_of_word(w)]
            row_concerns = sorted({concern_of_word(w) for w in sev_words}) or anchor
            rbasis = (f"중증도 이름 낱말 「{'·'.join(sev_words)}」 → 7단계 " + ','.join(row_concerns)) if sev_words else f"행 고민 앵커 전부({cond['combo']})"
            for k, txt in enumerate(s.get('contraindicated_combos') or []):
                kidx = f'{ci}.{si}.{k}'
                n0 = len(landed[('treatment-optimization.by_concern.contraindicated_combos', kidx)])
                parse_sentence('treatment-optimization.by_concern.contraindicated_combos', kidx, txt, re.split(r'\s+—\s+', txt)[0], 'mixed',
                               {'strength': st, 'cond': cond, 'where': where, 'row_concerns': row_concerns, 'row_concern_basis': rbasis})
                seq_texts['treatment-optimization.contraindicated_combos'].append(txt)
                if len(landed[('treatment-optimization.by_concern.contraindicated_combos', kidx)]) == n0:
                    op('금기 조합 문장이 패턴 밖', where=f'treatment-optimization.by_concern[{ci}].severity_levels[{si}].contraindicated_combos[{k}]', text=txt)

    # A9 common_combos note
    for i, x in enumerate(TS['common_combos']):
        if not x.get('note'):
            continue
        combo = COMBO7.get(('treatment-sequence.common_combos', x['name']))
        if combo is None:
            op('7단계 끝점 어긋남 — 세션 조합 없음', where=f'treatment-sequence.common_combos[{i}]', text=x['name'])
        cond = {'combo': combo['id'] if combo else None, 'concern_ids': (combo or {}).get('anchor', {}).get('concern') or [], 'source_label': x['name']}
        n, _ = parse_sentence('treatment-sequence.common_combos.note', i, x['note'], x['note'], 'order', {'cond': cond})
        seq_texts['treatment-sequence.common_combos.note'].append(x['note'])
        if not n:
            op('세션 조합 note 가 패턴 밖', where=f'treatment-sequence.common_combos[{i}].note', text=x['note'])

    # A10 problem-combos riskBenefit — 순서 문장만 쌍 · 나머지 = 7단계 조합 effect 원문(기본 행선지)
    for cb in [pk for pb in SRC['problem-combos']['combos'] for pk in pb.get('packages') or []]:
        rb = cb.get('riskBenefit')
        if not rb:
            continue
        w = cb['id']
        combo = COMBO7.get(('problem-combos', w))
        if combo is None:
            op('7단계 끝점 어긋남 — 추천 패키지 조합 없음', where=f'problem-combos[{w}]', text=cb.get('name'))
        cond = {'combo': combo['id'] if combo else None, 'concern_ids': (combo or {}).get('anchor', {}).get('concerns') or [], 'source_label': w}
        made = 0
        for s in sentences(rb):
            n, _ = parse_sentence('problem-combos.riskBenefit', w, rb, s, 'mixed', {'cond': cond})
            made += n
        seq_texts['problem-combos.riskBenefit'].append(rb)
        if not made:
            land('problem-combos.riskBenefit', w, f"7단계 추천 조합 {cond['combo']} effect.riskBenefit 원문 그대로(8단계 쌍 없음 · 다시 저장 안 함)")

    # A11 problem-packages combos(CC — 7단계 ③ 엣지 재사용) · alternatives(간격 낱말 있는 칸)
    for p in SRC['problem-packages']['problems']:
        for c in p['complaints']:
            key = f"{p['problem_id']}:{c['cc']}"
            e7 = CC7.get(key, {})
            anchor = next((e.get('anchor_sites') for e in e7.values() if e.get('anchor_sites')), None)
            site = anchor[0] if anchor and len(anchor) == 1 else None
            from7 = sorted({e['from'] for e in e7.values()})

            def proc_of(nm):
                for pr in c['procedures']:
                    words = [pr['name']] + [x.strip() for x in re.split(r'[/()]', pr['name']) if x.strip()]
                    if norm(nm) in {norm(w) for w in words}:
                        return pr['name']
                return None

            def side(nm):
                pn = proc_of(nm)
                e = e7.get(pn) if pn else None
                if pn is None:
                    r = resolve(nm, site_hint=site)
                    r['flag'] = (r.get('flag') or '') + ' · 조합 원소가 CC 추천 시술 밖 — 이름 해석(CC 앵커 부위)'
                    return r
                if e:
                    d = ep('단위 시술' if e['to_units'] else '계열', '7단계 CC 추천 시술 엣지(③) 재사용', units=e['to_units'], family=e.get('to_family'), flag='7단계 ' + e['lowering'])
                    d['text'] = nm
                    return d
                op('7단계 끝점 어긋남 — CC 추천 시술 엣지 없음', where=f'problem-packages {key}', text=pn)
                return resolve(nm, site_hint=site)
            for k, cb in enumerate(c.get('combos') or []):
                els = cb['combo']
                idx = f'{key}#{k}'
                if len(els) < 2:
                    attr('problem-packages.combos', idx, f'CC {key} 속성(원소 1개 — 쌍 아님)', cb['name'])
                    continue
                prs = [(els[0], els[1])] if len(els) == 2 else [(els[i], els[j]) for i in range(len(els)) for j in range(i + 1, len(els))]
                for x, y in prs:
                    Cl(source='problem-packages.complaints[].combos', source_index=idx, text=cb['name'], kind='시너지(CC 조합)', a=side(x), b=side(y), directed=False,
                       interval=None, reason=cb['reason'], evidence_text=cb.get('evidence'),
                       condition={'cc': c['cc'], 'problem': p['problem_id'], 'concern_ids': from7}, combo_name=cb['name'], combo_size=len(els),
                       rule='구조 칸(combo)', lowering='CC 앵커 부위로 내림(7단계 ③ 재사용)', evidence_kind='원천 evidence 칸(설명 문장)')
            for k, alt in enumerate(c.get('alternatives') or []):
                if not re.search(LEX['interval_words'], alt):
                    continue
                idx = f'{key}#{k}'
                n, _ = parse_sentence('problem-packages.complaints[].alternatives', idx, alt, alt, 'mixed', {'cond': {'cc': c['cc'], 'problem': p['problem_id']}, 'site': site})
                if not n:
                    tgt = sorted({u for nm in [x['name'] for x in c['procedures']] for u in (e7.get(nm) or {}).get('to_units', [])})
                    attr('problem-packages.complaints[].alternatives', idx, f"단위 시술 {','.join(tgt) or '(CC 엣지 없음)'} 재시술(터치업) 간격 원문", alt)
                seq_texts['problem-packages.complaints[].alternatives'].append(alt)

    # A12 combo-recipes followUp — 7단계 추천 조합(목적 레시피) 후속 일정 속성(쌍 아님)
    for r in SRC['combo-recipes']['recipes']:
        for k, f in enumerate(r.get('followUp') or []):
            attr('combo-recipes.followUp', f"{r.get('id')}#{k}", '7단계 추천 조합(목적 레시피) 후속 일정 원문', f"{f.get('week')}주 · {f.get('action')}",
                 week=f.get('week'), days_after=(f.get('week') or 0) * 7)

    # A13 taxonomy 제품 extracted 금기(쌍)
    for m in SRC['taxonomy']['modality']:
        for pr in m.get('products') or []:
            sf = (pr.get('extracted') or {}).get('safety') or {}
            for k, t in enumerate(sf.get('contraindications') or []):
                idx = f"{pr.get('id')}#{k}"
                n, _ = parse_sentence('taxonomy.modality[].products[].extracted.safety.contraindications', idx, t, t, 'mixed', {'family': m['id']})
                for c in claims:
                    if c['source_index'] == idx and c['source'].startswith('taxonomy.modality[].products'):
                        c['product'] = pr.get('id')
                if not n:
                    # 제품 문장 — 주어 = 그 제품(구조 칸) · 상대 = 문장 안 시술 이름(사전 낱말 최장 일치)
                    names = [a['text'] for a in RES['alias'] if a['text'] in t and norm(a['text']) != norm(pr.get('name'))]
                    names = sorted(names, key=len, reverse=True)[:1]
                    if names:
                        Cl(source='taxonomy.modality[].products[].extracted.safety.contraindications', source_index=idx, text=t, kind='같은 날 불가',
                           a=resolve(pr.get('name'), m['id']), b=resolve(names[0]), directed=False,
                           interval=mk_iv(t), rule='제품 문장(주어 = 제품 칸 · 상대 = 문장 안 사전 낱말 최장 일치)', lowering='제품 → 단위 시술', evidence_kind='원천 표기 없음', product=pr.get('id'))
                    else:
                        op('제품 금기 문장 상대 시술 못 찾음', where=idx, text=t)

    # 이름 없는 원천 질문 판정 · 간격 빈칸 · 끝점 표시
    for c in claims:
        c['not_procedure'] = any(c[s]['level'] == '시술 아님' for s in 'ab') or any(p.get('level') == '시술 아님' for s in 'ab' for p in c[s].get('parts', []))
        c['bundle_word'] = any(c[s]['level'] in ('계열 묶음', '모든 시술') for s in 'ab')
        c['resolved'] = not (bad_ep(c['a']) or bad_ep(c['b']))
        c['endpoint_levels'] = [c['a']['level'], c['b']['level']]
        if interval_empty(c.get('interval'), LEX):
            op('간격 원문 낱말이 있는데 숫자 칸 · 표시 비어 있음', where=c['id'], text=c['interval']['text'])
        for w in interval_unread(c.get('interval'), LEX):
            op('간격 원문 낱말을 읽는 사전 갈래 없음', where=c['id'], word=w, text=c['interval']['text'])

    # 6단계 메모 37 → 시너지 근거(함께 판매)
    pkg_evidence = []
    for n in S6['step6-to-step8-notes']:
        hit = [c['id'] for c in claims if c['source'] == 'synergy.links' and c['source_index'] in [l['i'] for l in n['links']]]
        pkg_evidence.append({'package': n['package'], 'name': n['name'], 'pair': n['pair'], 'verdict': n['verdict'], 'synergy_links': [l['i'] for l in n['links']],
                             'matched_claims': hit, 'use': '시너지의 「함께 판매 사례」 근거(10-29 6단계 결정) — 엣지를 새로 세우지 않음', 'conflict': n['verdict'].startswith('다름')})
    profile_attrs = []
    for p in SRC['procedure-profiles']['profiles']:
        profile_attrs.append({'family': p['id'], 'phase': p['phase'], 'phaseOrder': p['phaseOrder'],
                              'flags': {k: p.get(k) for k in ['hasProtein', 'hasHA', 'usesGel', 'createsWound', 'createsChannel', 'thermalLoad', 'bleedingRisk', 'swellingRisk']},
                              'practicalNotes': p.get('practicalNotes'), 'use': '계열 원문 속성 — 파생 엣지 계산 안 함(B06 ⑥)'})
        if p['id'] not in FAM:
            op('procedure-profiles 계열 코드가 2단계에 없음', family=p['id'])

    # ───────── 충돌(계열 쌍 · D-13b) ─────────
    def fams_of(e):
        if e['level'] in ('해석 안 됨', '시술 아님', '계열 묶음'):
            return []
        if e['level'] == '모든 시술':
            return ['*']
        if e['level'] == '복합(나눔)':
            return sorted({f for pp in e['parts'] for f in fams_of(pp)})
        return e['families']

    pairs = collections.defaultdict(list)
    for c in claims:
        for fa in fams_of(c['a']):
            for fb in fams_of(c['b']):
                if fa == fb or '*' in (fa, fb):
                    continue
                pairs[tuple(sorted([fa, fb]))].append(c)

    def first_family(c, k):
        f = ((c.get('interval') or {}).get('first'))
        if f not in ('a', 'b'):
            return None
        x = [y for y in fams_of(c[f]) if y in k]
        return x[0] if len(x) == 1 else None

    conflicts = []
    for k, cs in sorted(pairs.items()):
        firsts = collections.defaultdict(list)
        for c in cs:
            ff = first_family(c, k)
            if ff and c['id'] not in firsts[ff]:
                firsts[ff].append(c['id'])
        if len(firsts) > 1:
            conflicts.append({'pair': list(k), 'type': '순서(먼저 하는 쪽)', 'sides': dict(sorted(firsts.items())),
                              'note': '방향마다 다른 문맥(같은 날 · 별도 세션 · 하위 조건)일 수 있음 — 원문 둘 다 남김(D-13b)'})
        yes = sorted({c['id'] for c in cs if (c.get('interval') or {}).get('same_day') is True})
        no = sorted({c['id'] for c in cs if (c.get('interval') or {}).get('same_day') is False})
        if yes and no:
            conflicts.append({'pair': list(k), 'type': '같은 날 가능 ↔ 불가', 'sides': {'가능': yes, '불가': no}, 'note': '방향 · 하위 조건(박리 · 부위) 차이로 설명되는지 의료진 확인'})
        by_dir = collections.defaultdict(list)
        for c in cs:
            iv = c.get('interval') or {}
            if not iv.get('days') or iv.get('same_day') or iv['days'] == [0, 0]:
                continue
            by_dir[first_family(c, k) or '방향 없음'].append((c['id'], iv['days'], iv.get('open_high'), iv['text']))
        for d, lst in sorted(by_dir.items()):
            uniq = {x[0]: x for x in lst}
            lst = list(uniq.values())
            if len(lst) > 1:
                lo = max(r[1][0] for r in lst)
                hi = min((float('inf') if r[2] else r[1][1]) for r in lst)
                if lo > hi:
                    conflicts.append({'pair': list(k), 'type': '간격 수치', 'first': d, 'sides': {x[0]: x[3] for x in lst},
                                      'note': '간격 원문 범위가 겹치지 않음(「이상」은 위로 열림)'})
    # 10-30 전수 가드 — 묶음 낱말 끝점(「열 시술」 · 「주입 시술」)도 계열로 펴서 순서 반대를 다시 셈. 기존 X8 은 id 유지 · 묶음 몫은 sides_from_bundle 로 더함 · 새 쌍은 뒤에 붙임
    def fams_of_b(e):
        if e['level'] == '계열 묶음':
            return e['families']
        if e['level'] == '복합(나눔)':
            return sorted({f for pp in e['parts'] for f in fams_of_b(pp)})
        return fams_of(e)
    bpairs = collections.defaultdict(list)
    for c in claims:
        if not any(c[s]['level'] == '계열 묶음' or any(pp.get('level') == '계열 묶음' for pp in c[s].get('parts', [])) for s in 'ab'):
            continue
        for fa in fams_of_b(c['a']):
            for fb in fams_of_b(c['b']):
                if fa != fb and '*' not in (fa, fb):
                    bpairs[tuple(sorted([fa, fb]))].append(c)

    def first_family_b(c, k):
        f = ((c.get('interval') or {}).get('first'))
        if f not in ('a', 'b'):
            return None
        x = [y for y in fams_of_b(c[f]) if y in k]
        return x[0] if len(x) == 1 else None
    new_conf = []
    for k, bcs in sorted(bpairs.items()):
        firsts = collections.defaultdict(list)
        for c in pairs.get(k, []):
            ff = first_family(c, k)
            if ff and c['id'] not in firsts[ff]:
                firsts[ff].append(c['id'])
        bf = collections.defaultdict(list)
        for c in bcs:
            ff = first_family_b(c, k)
            if ff and c['id'] not in bf[ff]:
                bf[ff].append(c['id'])
        sides = {f: sorted(set(firsts.get(f, [])) | set(bf.get(f, []))) for f in set(firsts) | set(bf)}
        if len(sides) < 2 or not bf:
            continue
        base = next((x for x in conflicts if x['pair'] == list(k) and x['type'] == '순서(먼저 하는 쪽)'), None)
        if base:
            base['sides_from_bundle'] = dict(sorted(bf.items()))
        else:
            new_conf.append({'pair': list(k), 'type': '순서(먼저 하는 쪽)', 'sides': dict(sorted(sides.items())), 'from_bundle': True,
                             'note': '묶음 낱말 끝점(계열로 폄)이 들어간 순서 반대 — 10-30 전수 가드에서 드러남(그 전 셈은 묶음 끝점을 뺐음)'})
    for i, x in enumerate(conflicts):
        x['id'] = f'X8-{i + 1:03d}'
    for x in new_conf:
        x['id'] = f'X8-{len(conflicts) + 1:03d}'
        conflicts.append(x)
    conflict_claims = {cid for x in conflicts for side in x['sides'].values() for cid in (side if isinstance(side, list) else [])} | \
                      {cid for x in conflicts if x['type'] == '간격 수치' for cid in x['sides']}
    for c in claims:
        c['review_status'] = 'conflict' if c['id'] in conflict_claims else 'ok'

    # ───────── 출력 · 깊이 한정어 = 조건부(검수 F1 · scope_rule) ─────────
    SCOPE = DEC['scope_rule']
    scoped = []

    def scope_mark(e, owner, extra_q=None):
        """끝점 앞 한정어(고출력 · 고에너지 · 박리성 · 심부 …)를 떼고 묶음(계열 · 기법 · 하위 · 용도 · 낱말 교집합)으로 연 끝점 = 조건부 · 기본 상속 · 기본 적용에서 뺌."""
        hit = False
        for p in ([e] if e['level'] != '복합(나눔)' else e['parts']):
            src = ' '.join(filter(None, [p.get('text'), p.get('qualifier'), ' '.join(p.get('stripped_prefix') or []), extra_q if p is e or e['level'] != '복합(나눔)' else None]))
            words = sorted(set(re.findall(SCOPE['words'], src)))
            if words and p['level'] in SCOPE['group_levels']:
                p['scope'] = SCOPE['label']
                p['default_apply'] = False
                p['scope_words'] = words
                scoped.append((owner, p.get('text'), words))
                hit = True
        return hit
    for c in claims:
        if c['kind'] in SCOPE['kinds']:
            c['scope_conditional'] = any([scope_mark(c['a'], c['id']), scope_mark(c['b'], c['id'])])
    for av in avoids:
        av['scope_conditional'] = scope_mark(av['to'], av['id'], av.get('qualifier'))
        if av['scope_conditional']:
            av['scope'] = SCOPE['label']
            av['default_apply'] = False

    # ───────── 엣지(끝점 쌍마다 하나 · D-03) ─────────
    def ekeys(e):
        if e['level'] in ('해석 안 됨', '시술 아님'):
            return []
        if e['level'] == '복합(나눔)':
            return sorted({k for pp in e['parts'] for k in ekeys(pp)})
        if e['level'] == '모든 시술':
            return ['all']
        if e['level'] == '계열 묶음':
            return ['bundle:' + '|'.join(e['families'])]
        if e['units']:
            return ['units:' + ','.join(e['units'])]
        return ['family:' + ','.join(e['families']) + (('#' + e['sub_family']) if e.get('sub_family') else '') + (('#' + e['technique']) if e.get('technique') else '')]

    def ep_struct(key):
        """U3 · B3 — 끝점 문자열 → 칸(kind · id · qualifier · candidates[]). 묶음은 노드가 아니라 candidates[]."""
        if key == 'all':
            return {'kind': '모든 시술', 'id': None, 'qualifier': None, 'candidates': []}
        if key.startswith('bundle:'):
            fs = key[7:].split('|')
            return {'kind': '계열 묶음', 'id': None, 'qualifier': None, 'candidates': [{'kind': 'family', 'id': f} for f in fs]}
        if key.startswith('units:'):
            us = key[6:].split(',')
            if len(us) == 1:
                return {'kind': '단위 시술', 'id': us[0], 'qualifier': None, 'candidates': []}
            return {'kind': '단위 시술 후보', 'id': None, 'qualifier': None, 'candidates': [{'kind': 'unit_procedure', 'id': u} for u in us]}
        body, *qs = key[7:].split('#')
        fs = body.split(',')
        q = {}
        for x in qs:
            q['technique' if x in TECH_IDS else 'sub_family'] = x
        if len(fs) == 1:
            return {'kind': '계열' + (' + 조건' if q else ''), 'id': fs[0], 'qualifier': q or None, 'candidates': []}
        return {'kind': '계열 후보', 'id': None, 'qualifier': q or None, 'candidates': [{'kind': 'family', 'id': f} for f in fs]}
    TECH_IDS = {n['id'] for n in T4['nodes']}

    edge_map = collections.defaultdict(list)
    for c in claims:
        for ka in ekeys(c['a']):
            for kb in ekeys(c['b']):
                k = tuple(sorted([ka, kb]))
                edge_map[k].append(c['id'])
    CLAIM = {c['id']: c for c in claims}
    edges = []
    for i, (k, ids) in enumerate(sorted(edge_map.items())):
        ids = sorted(set(ids))
        edges.append({'id': f'E8-{i + 1:04d}', 'a': k[0], 'b': k[1], 'endpoints': {'a': ep_struct(k[0]), 'b': ep_struct(k[1])}, 'self_pair': k[0] == k[1], 'claims': ids,
                      'conditional_claims': [x for x in ids if CLAIM[x].get('scope_conditional')],
                      'kinds': sorted({CLAIM[x]['kind'] for x in ids}), 'review_status': 'conflict' if any(CLAIM[x]['review_status'] == 'conflict' for x in ids) else 'ok'})

    # ───────── B. 확인 조건 ─────────
    pre = SRC['pre-procedure-checklist']
    PT = LB['precheck_type_site']
    for x in pre['universal_checks']:
        hits = cond_match(x['label'] + ' ' + x['description'])
        CC(source='pre-procedure-checklist.universal_checks', source_index=x['id'], target='모든 시술(공통)', target_level='공통', text=x['label'], detail=x['description'],
           grade_original=x['type'], grade_site=PT[x['type']], grade3=LB['grade3'].get(x['type'], '조건 아님(' + PT[x['type']] + ')'), conditions=hits,
           kind=('사람 조건' if x['type'] not in ('counseling', 'safety_protocol') else PT[x['type']] + ' 항목'))
    for cs in pre['category_specific']:
        for j, x in enumerate(cs['checks']):
            hits = cond_match(x['label'])
            kind = '사람 조건' if x['type'] not in ('counseling', 'safety_protocol') else PT[x['type']] + ' 항목'
            if x['type'] == 'inform' and not hits:
                kind = '고지 항목'
            CC(source='pre-procedure-checklist.category_specific', source_index=f"{cs['id']}#{j}", target=f"family:{cs['id']}", target_level='계열', text=x['label'],
               grade_original=x['type'], grade_site=PT[x['type']], grade3=LB['grade3'].get(x['type'], '조건 아님(' + PT[x['type']] + ')'), conditions=hits, kind=kind)
    for cat in SRC['consent-checklist']['categories']:
        for j, t in enumerate(cat['contraindications']):
            CC(source='consent-checklist.contraindications', source_index=f"{cat['id']}#{j}", target=f"family:{cat['id']}", target_level='계열', text=t,
               grade_original='contraindications(동의서 금기 목록 · 등급 칸 없음)', grade_site='금기사항', grade3=LB['grade3']['consent'], conditions=cond_match(t), kind='사람 조건')
    for m in SRC['taxonomy']['modality']:
        ci = m['extracted'].get('contraindications') or {}
        for g in ('absolute', 'relative'):
            for j, t in enumerate(ci.get(g) or []):
                CC(source=f'taxonomy.modality[].extracted.contraindications.{g}', source_index=f"{m['id']}#{j}", target=f"family:{m['id']}", target_level='계열', text=t,
                   grade_original=g, grade_site={'absolute': '절대', 'relative': '상대'}[g], grade3=LB['grade3'][g], conditions=cond_match(t), kind='사람 조건')
    LEDGER = {x['id']: x for x in U['ledger']}
    for m in SRC['taxonomy']['modality']:
        for s in m.get('subcategories', []):
            for it in s.get('items', []):
                sf = (it.get('extracted') or {}).get('safety') or {}
                for j, t in enumerate(sf.get('contraindications') or []):
                    lg = LEDGER.get(it['id'], {})
                    if not lg:
                        op('원장 항목이 5단계 ledger 에 없음', where=it['id'])
                    tgt = lg.get('units') or ([f"product:{lg['product']}"] if lg.get('product') else [])
                    CC(source='taxonomy.items[].extracted.safety.contraindications', source_index=f"{it['id']}#{j}", target=tgt or f"ledger:{it['id']}",
                       target_level=('단위 시술' if lg.get('units') else ('제품' if lg.get('product') else '원장 항목(행선지 없음)')), ledger_dest=lg.get('dest'),
                       text=t, item_name=it['name'], grade_original='contraindications(원장 항목 · 등급 칸 없음)', grade_site='금기', grade3=LB['grade3']['item'],
                       conditions=cond_match(t), kind='사람 조건')
    for x in moved_to_conditions:
        r = resolve(x['proc'])
        CC(source=x['source'], source_index=x['source_index'], target=r, target_level=r['level'], text=' ↔ '.join(x['pair']), detail=x['reason'],
           wait=mk_iv(f"{x['min_months']}개월 이상" if x.get('min_months') is not None else None), evidence_text=x.get('evidence_text'),
           grade_original=('같은 날 불가(복용 중)' if x['grade'] == 'iso_same_day' else '대기 기간'),
           grade_site=('동일 세션 금기' if x['grade'] == 'iso_same_day' else '최소 간격'), grade3=LB['grade3'][x['grade']],
           conditions=cond_match(x['person']), kind='사람 조건(시술 쌍에서 옮김 · C10)')
    AGE = DEC['age_avoid_patterns']
    for a in OPT['by_age_group']:
        for j, t in enumerate(a['avoid']):
            tgt, q = None, None
            for pt in AGE:
                m = re.search(pt['regex'], t)
                if m:
                    q = m.group('Q')
                    tgt = ep('모든 시술', '연령 avoid 패턴(빈도 문장)', flag='와일드카드(빈도 · 양 문장)') if pt['target'] == 'all' else resolve(m.group('B'))
                    break
            if tgt is None:
                op('연령 avoid 문장이 패턴 밖', where=f"by_age_group {a['age']}#{j}", text=t)
                tgt = ep('해석 안 됨', '없음', flag='unresolved_name_ref')
            CC(source='treatment-optimization.by_age_group.avoid', source_index=f"{a['age']}#{j}", target=tgt, target_level=tgt['level'], text=t, age=a['age'],
               grade_original='avoid', grade_site='주의', grade3=LB['grade3']['avoid'], conditions=['C-AGE'], kind='연령대 조건', qualifier=q)
    for c in cond_claims:
        if not c['conditions'] and c['kind'] == '사람 조건':
            for rr in DEC['not_person_rules']:
                if re.search(rr['pattern'], c['text']):
                    c['kind'] = rr['kind']
                    break
    for x in [k for k in cond_claims if k.get('wait')] + [a for a in attrs if a.get('interval')]:
        iv = x.get('wait') or x.get('interval')
        if interval_empty(iv, LEX):
            op('간격 원문 낱말이 있는데 숫자 칸 · 표시 비어 있음', where=x.get('id') or f"attr {x['source']}[{x['source_index']}]", text=iv['text'])
        for w in interval_unread(iv, LEX):
            op('간격 원문 낱말을 읽는 사전 갈래 없음', where=x.get('id') or f"attr {x['source']}[{x['source_index']}]", word=w, text=iv['text'])
    unmatched = [c for c in cond_claims if not c['conditions'] and c['kind'].startswith('사람 조건')]
    for c in unmatched:
        op('사람 조건인데 조건 사전에 안 걸림', where=c['id'], text=c['text'])
    ext_check = []
    for code, e in SRC['extracted'].items():
        m = next((m for m in SRC['taxonomy']['modality'] if m['id'] == code), None)
        a = e.get('contraindications') or {}
        b = (m['extracted'].get('contraindications') or {}) if m else {}
        same = json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True)
        ext_check.append({'family': code, 'contraindications_same': same, 'aftercare_same': e.get('aftercare') == (m['extracted'].get('aftercare') if m else None)})
        if not same:
            op('extracted.json ↔ taxonomy 금기 다름(C6 — taxonomy 정본)', family=code)
    def is_condition(c):
        return not (c['kind'].endswith('항목') or not c['kind'].startswith(('사람 조건', '연령대')))
    cond_edges = [c for c in cond_claims if is_condition(c)]
    not_condition = [c for c in cond_claims if not is_condition(c)]
    cond_nodes = []
    for cd in CONDS:
        cs = [c for c in cond_edges if cd['id'] in c['conditions']]
        if cs:
            cond_nodes.append({'id': cd['id'], 'name': cd['name'], 'match_pattern': cd['pattern'], 'n_claims': len(cs), 'sources': sorted({c['source'].split('.')[0] for c in cs})})
        else:
            STALE.append({'type': '조건 사전 항목에 걸린 주장 없음', 'id': cd['id']})
    fam_cond = collections.defaultdict(list)
    for c in cond_claims:
        tg = c['target'] if isinstance(c['target'], str) else None
        if not tg or not tg.startswith('family:'):
            continue
        for cid in c['conditions']:
            fam_cond[(tg, cid)].append(c)
    grade_conflicts = []
    for (f, cid), cs in sorted(fam_cond.items()):
        g = sorted({c['grade3'] for c in cs if c['kind'] == '사람 조건'})
        if len([x for x in g if x in ('금기', '주의', '확인만', '확인만(고지)')]) > 1:
            grade_conflicts.append({'id': f'XK-{len(grade_conflicts) + 1:03d}', 'family': f, 'condition': cid, 'grades': g,
                                    'claims': [[c['id'], c['source'].split('.')[0], c['grade_original'], c['text']] for c in cs]})
    # 대기 기간 충돌 — 같은 조건 · 원천마다 기간 숫자(개월) 다름
    wait_conflicts = []
    for cd in CONDS:
        per = collections.defaultdict(set)
        for c in cond_claims:
            if cd['id'] not in c['conditions']:
                continue
            txt = ' '.join(filter(None, [c['text'], c.get('detail')]))
            ms = re.findall(r'(\d+)\s*(?:[~\-]\s*(\d+))?\s*개월', txt)
            if ms:
                per[c['source']] |= {int(x) for m in ms for x in m if x}
        vals = {k: tuple(sorted(v)) for k, v in per.items()}
        if len(set(vals.values())) > 1:
            wait_conflicts.append({'id': f'XW-{cd["id"]}', 'condition': cd['id'], 'what': f'{cd["name"]} 대기 기간', 'by_source': {k: list(v) for k, v in sorted(vals.items())},
                                   'note': '같은 조건 · 원천마다 기간 숫자(개월)가 다름 — 둘 다 보존 · 충돌 표시(D-13b)'})

    # ───────── C. 안전 ─────────
    comp = SRC['complications']
    SA = DEC['semantic_apply']
    comp_nodes, side_effects, se_exceptions, ev_web = [], [], [], {}
    for cat in comp['categories']:
        if cat['id'] not in FAM:
            op('합병증 계열 코드가 2단계에 없음', family=cat['id'])
        for j, x in enumerate(cat['complications']):
            if x['severity'] not in SA['complication_severities'] + SA['side_effect_severities']:
                op('합병증 원천 severity 가 결정에 없음', family=cat['id'], name=x['name'], severity=x['severity'])
            is_se = x['severity'] in SA['side_effect_severities']
            nid = f"{'SE' if is_se else 'CX'}-{cat['id']}-{j + 1:02d}"
            url = x.get('evidence')
            if url:
                urls = re.findall(DEC['web_evidence_rule']['url_regex'], url)
                ev_web.setdefault(url, {'id': f'EV-WEB-{len(ev_web) + 1:03d}', 'url': url,
                                        'kind': '웹' if urls else DEC['web_evidence_rule']['no_url_kind'],
                                        'multi_url': len(urls) > 1, 'urls': urls, 'used_by': []})['used_by'].append(nid)
            comp_nodes.append({'id': nid, 'name': x['name'], 'family': cat['id'], 'family_source_name': cat['name'], 'severity': x['severity'],
                               'severity_site': LB['complication_severity_site'][x['severity']], 'incidence': x.get('incidence'), 'onset': x.get('onset'),
                               'duration': x.get('duration'), 'mechanism': x.get('mechanism'), 'risk_factors': x.get('risk_factors'), 'management': x.get('management'),
                               'prevention': x.get('prevention'), 'evidence': [ev_web[url]['id']] if url else [], 'edge': f"has_complication family:{cat['id']} → {nid}",
                               'units_inherit': [u['id'] for u in U['units'] if u['key']['family'] == cat['id']]})
            if is_se:
                se = comp_nodes.pop()
                se.pop('units_inherit')
                se.pop('edge')
                se.update(source='complications.json categories[].complications[](severity mild — U2 · B1)', attach=f"family:{cat['id']}")
                if not re.search(SA['side_effect_common_incidence'], x.get('incidence') or ''):
                    se['staff_question'] = 'Q8-19'
                    se_exceptions.append(se['id'])
                side_effects.append(se)
    # U1 — complications.json 에 없는 계열은 taxonomy modality extracted.safety 원문으로(serious → 합병증 · common · uncommon → 부작용)
    comp_src_fams = {c['id'] for c in comp['categories']}
    GF = SA['gap_fill']
    gap_filled = {}
    for m in SRC['taxonomy']['modality']:
        if m['id'] in comp_src_fams or m['id'] not in FAM:
            continue
        sf_ = (m['extracted'].get('safety') or {})
        for g in ('serious', 'common', 'uncommon'):
            for j, t in enumerate(sf_.get(g) or []):
                if GF[g] == '합병증':
                    nid = f"CX-{m['id']}-T{j + 1:02d}"
                    comp_nodes.append({'id': nid, 'name': t, 'family': m['id'], 'family_source_name': m.get('name'), 'severity': None, 'severity_site': '원문 serious(taxonomy)',
                                       'incidence': None, 'onset': None, 'duration': None, 'mechanism': None, 'risk_factors': None, 'management': None, 'prevention': None, 'evidence': [],
                                       'edge': f"has_complication family:{m['id']} → {nid}", 'units_inherit': [u['id'] for u in U['units'] if u['key']['family'] == m['id']],
                                       'source': f"taxonomy modality[{m['id']}].extracted.safety.serious[{j}](U1)"})
                else:
                    side_effects.append({'id': f"SE-{m['id']}-{g[0].upper()}{j + 1:02d}", 'name': t, 'family': m['id'], 'family_source_name': m.get('name'), 'severity': None,
                                         'severity_site': f'원문 {g}(taxonomy)', 'incidence': None, 'source': f"taxonomy modality[{m['id']}].extracted.safety.{g}[{j}](U1)", 'attach': f"family:{m['id']}"})
                gap_filled.setdefault(m['id'], collections.Counter())[GF[g]] += 1
    # gap = 합병증 원천 없음(「없음 = 안전」 아님) · 원천은 있는데 중대 반응이 없는 계열(전부 mild → 부작용)은 따로
    comp_gap = sorted(f for f in FAM if f not in comp_src_fams and not any(c['family'] == f for c in comp_nodes))
    comp_none_mild_only = sorted(f for f in comp_src_fams if f in FAM and not any(c['family'] == f for c in comp_nodes))
    se_gap = sorted(f for f in FAM if not any(x['family'] == f for x in side_effects))
    name_multi = {k: v for k, v in sorted(C_(c['name'] for c in comp_nodes).items()) if v > 1}
    AZ = SRC['anatomy-danger-zones']
    zmap = {z['zone']: z for z in S3['danger_zone_mapping']}
    sl = {x['zone']: x for x in T4['unit_procedure_attrs']['safe_layers']}
    site_caution = []
    for z in AZ['zones']:
        if z['id'] not in zmap:
            op('위험지대 zone 이 3단계 대응표에 없음', zone=z['id'])
            continue
        site = zmap[z['id']]['node']
        for fam, keyname in (('M1', 'botox_specific'), ('M2', 'filler_specific')):
            spec = z.get(keyname)
            if not spec:
                continue
            us = [u['id'] for u in U['units'] if u['key']['family'] == fam and u['key']['site'] in site_desc(site)]
            site_caution.append({'id': f"SC-{z['id']}-{fam}", 'edge': f'site_caution site:{site} → family:{fam}', 'zone': z['id'], 'zone_name': z['name_ko'], 'site': site,
                                 'site_mapping': zmap[z['id']]['verdict'], 'family': fam, 'danger_level': z['danger_level'], 'danger_color': z['danger_color'],
                                 'vessels': z.get('vessels'), 'nerves': z.get('nerves'), 'tissue_data': z.get('tissue_data'), 'clinical_pearls': z.get('clinical_pearls'),
                                 'spec': spec, 'safe_layers_ref': ('4단계 unit_procedure_attrs.safe_layers zone=' + z['id']) if z['id'] in sl and fam == 'M2' else None,
                                 'safe_injection_depth': z.get('safe_injection_depth'), 'units_affected': us,
                                 'units_note': ('그 부위 · 하위 부위 단위 시술 — 조회 때 상속' if us else '이 부위 · 하위에 이 계열 단위 시술 없음(엣지는 둠 — 「없음 = 안전」 아님)'),
                                 'evidence_kind': '3-AI 합의(consensus_method)'})
    crit = {'attach': 'family:M2', 'what': 'critical_safety_facts 원문(숫자 그대로)', 'facts': AZ['critical_safety_facts']}
    family_text = collections.defaultdict(dict)
    for cat in SRC['consent-checklist']['categories']:
        family_text[cat['id']]['필수 고지(consent mandatory_disclosures)'] = cat['mandatory_disclosures']
        family_text[cat['id']]['즉시 내원이 필요한 징후(consent emergency_signs)'] = cat['emergency_signs']
    for cat in SRC['patient-education']['categories']:
        family_text[cat['id']]['환자 설명 가이드(patient-education)'] = [{k: cat.get(k) for k in ['patient_name', 'simple_explanation', 'how_it_works', 'duration_simple', 'pain_level', 'downtime', 'common_concerns']}]
    for m in SRC['taxonomy']['modality']:
        ex = m['extracted']
        family_text[m['id']]['사후관리(taxonomy modality extracted.aftercare)'] = ex.get('aftercare') or []
        for g in ('common', 'uncommon', 'serious'):
            family_text[m['id']][f'부작용 문장 {g}(근거 — 합병증 노드 아님 · B13)'] = (ex.get('safety') or {}).get(g) or []
    for code, e in SRC['extracted'].items():
        if (e.get('safety') or {}).get('emergency'):
            family_text[code]['응급(extracted.json safety.emergency)'] = e['safety']['emergency']
        if e.get('aftercare'):  # 품질 J(10-30) — extracted.json 사후관리 원문도 계열 원문 칸에 그대로
            family_text[code]['사후관리(extracted.json aftercare)'] = e['aftercare']
    for p in SRC['procedure-profiles']['profiles']:
        family_text[p['id']]['사후관리(procedure-profiles aftercare)'] = p.get('aftercare') or []
    family_text['M2']['critical_safety_facts(anatomy)'] = [AZ['critical_safety_facts']]
    for a in attrs:
        if a['attach'].startswith('family:'):
            family_text[a['attach'][7:]].setdefault('안전 원문(규칙 행 · 쌍 없음)', []).append(a['text'])
    for c in cond_claims:
        if c['kind'].endswith('항목') or not c['kind'].startswith(('사람 조건', '연령대')):
            tg = c['target'] if isinstance(c['target'], str) else None
            if tg and tg.startswith('family:'):
                family_text[tg[7:]].setdefault('상담 · 준비 · 고지 · 조건 아닌 문장(확인 조건 엣지 아님)', []).append(f"[{c['kind']}] {c['text']}")
    for k in family_text:
        if k not in FAM:
            op('안전 원문 계열 코드가 2단계에 없음', family=k)
    TLA = DEC['timeline_attach']
    timelines = []
    for t in SRC['post-procedure-timeline']['timelines']:
        a = TLA.get(t['id'])
        if a is None:
            op('결정 없는 경과표', id=t['id'])
            continue
        us = a.get('units') or sorted({u for w in a.get('units_where') or [] for u in units_where(w['family'], w.get('sub'))}) or None
        for u in us or []:
            if u not in UNITS:
                op('결정이 가리키는 단위 시술 없음', where=f"timeline_attach {t['id']}", unit=u)
        timelines.append({'id': t['id'], 'source_category': t['category'], 'name': t['name'], 'attach_level': a['level'], 'attach': a['attach'], 'units': us,
                          'phases': t['phases'], 'labels_site': LB['timeline_label_site']})
    for k in TLA:
        if k not in {t['id'] for t in SRC['post-procedure-timeline']['timelines']}:
            STALE.append({'type': '원천에 없는 경과표 결정', 'id': k})
    pih_attach = []
    for x in U['pih']:
        src = SRC['pih-risk']['procedures'][x['index']]
        pih_attach.append({'index': x['index'], 'name': x['name'], 'units': x['units'], 'attach': x['attach'], 'risk_factors': src.get('risk_factors'), 'prevention': src.get('prevention')})
    # 단위 시술 안전 상태(품질 K · G10 · 10-30) — 칸마다 값 있음 · 해당 없음(원천) · 정보 없음(gap). 모든 칸이 gap 인 단위 시술은 unit_gaps 로 따로(「없음 = 안전」 아님)
    def ctarget(c):
        t = c.get('target')
        fs, us, ps = set(), set(), set()
        for x in (t if isinstance(t, list) else [t]):
            if isinstance(x, str):
                k_, _, v_ = x.partition(':')
                if k_ == 'family':
                    fs.add(v_)
                elif k_ in ('unit', 'units'):
                    us |= set(v_.split(','))
                elif k_ in ('product', 'ledger'):
                    ps.add(v_)
            elif isinstance(x, dict):
                us |= set(x.get('units') or [])
                fs |= set(x.get('families') or []) if not x.get('units') else set()
        return fs, us, ps
    CT = [(c, ctarget(c)) for c in cond_edges if c.get('target_level') not in ('공통', '모든 시술')]
    unit_safety_status, unit_gaps = [], []
    for u in U['units']:
        uid, fam, site = u['id'], u['key']['family'], u['key']['site']
        prods = {p['product'] for p in u.get('uses_product') or []}
        st = {
            'complications': any(c['family'] == fam for c in comp_nodes),
            'side_effects': any(x.get('attach') == f'family:{fam}' for x in side_effects),
            'checks': any(fam in f_ or uid in u_ or (p_ & prods) for _, (f_, u_, p_) in CT),
            'site_caution': any(x['family'] == fam and uid in (x.get('units_affected') or []) for x in site_caution),
            'timelines': any((x.get('attach') == f'family:{fam}' and not x.get('units')) or uid in (x.get('units') or []) for x in timelines),
            'pih': ('해당 없음(원천)' if u.get('pih_not_applicable') else any(uid in (x.get('units') or []) for x in pih_attach)),
        }
        fields = {k_: ('값 있음' if v_ is True else (v_ if isinstance(v_, str) else '정보 없음(gap)')) for k_, v_ in st.items()}
        row = {'unit': uid, 'family': fam, 'fields': fields}
        unit_safety_status.append(row)
        if all(v_ != '값 있음' for v_ in fields.values()):
            unit_gaps.append({'unit': uid, 'name': u['name'], 'family': fam, 'status': '정보 없음(gap)',
                              'why': f"계열 {fam} 이 안전 원천(complications · consent · pre-procedure · timeline · pih) 밖 — 안전 정보 0 을 「안전」으로 말하지 않게 상태를 그대로 낸다(G10)",
                              'family_gap': {'complications': fam in comp_gap, 'side_effects': fam in se_gap}})
    item_text = C_()
    item_dest = C_()
    for m in SRC['taxonomy']['modality']:
        for s in m.get('subcategories', []):
            for it in s.get('items', []):
                ex = it.get('extracted') or {}
                lg = LEDGER.get(it['id'], {})
                d = '단위 시술' if lg.get('units') else ('제품(→ 5단계 「이 제품으로 했을 때」 extracted)' if lg.get('product') else ('행선지 ' + str(lg.get('dest'))))
                if ex.get('aftercare'):
                    item_text['aftercare'] += 1
                    item_dest[d] += 1
                for k in ('common', 'serious', 'note', 'long_term'):
                    if (ex.get('safety') or {}).get(k):
                        item_text['safety.' + k] += 1

    # ───────── D. 근거 ─────────
    LE = SRC['literature-evidence']
    ev_lit, statements = {}, []
    for code, cat in LE['categories'].items():
        for field in ('moa', 'adverse_effects', 'effects'):
            for j, s in enumerate(cat.get(field) or []):
                sid = f'ST-{code}-{field}-{j + 1:02d}'
                refs = []
                for cit in s.get('citations') or []:
                    key = ('pmid:' + str(cit['pmid'])) if cit.get('pmid') else (('doi:' + cit['doi']) if cit.get('doi') else 'title:' + (cit.get('title') or '')[:60])
                    ev = ev_lit.setdefault(key, {'id': f'EV-LIT-{len(ev_lit) + 1:03d}', 'key': key, 'kind': '문헌', 'pmid': cit.get('pmid'), 'doi': cit.get('doi'), 'pmc': cit.get('pmc'),
                                                 'title': cit.get('title'), 'journal': cit.get('journal'), 'year': cit.get('year'), 'authors': cit.get('authors'), 'oa_url': cit.get('oa_url'), 'used_by': []})
                    ev['used_by'].append(sid)
                    refs.append(ev['id'])
                statements.append({'id': sid, 'family': code, 'field': field, 'statement': s['statement'], 'accuracy_score': s.get('accuracy_score'),
                                   'accuracy_note': s.get('accuracy_note'), 'patient': {l: s.get('patient_' + l) for l in ('ko', 'en', 'zh', 'ja')}, 'evidence': refs,
                                   'added_at': s.get('added_at'), 'edge': f'family:{code} —근거 문장→ {sid}'})
    ev_guide = {}
    GNS = DEC['guide_not_source_rule']

    def guide_refs(text, used):
        out = []
        for part in [p.strip() for p in re.split(r';\s*', text or '') if p.strip()]:
            pmc = re.findall(r'PMC\d+', part)
            hit = next((e for pm in pmc for e in ev_lit.values() if e.get('pmc') == pm), None)
            if hit:
                hit['used_by'].append(used)
                out.append(hit['id'])
                continue
            g = ev_guide.setdefault(part, {'id': f'EV-GD-{len(ev_guide) + 1:03d}', 'label': part,
                                           'kind': ('가이드 · 표기 출처' if re.search(GNS['source_words'], part) else '출처 아님(이유 문장)'), 'pmc': pmc or None, 'used_by': []})
            g['used_by'].append(used)
            out.append(g['id'])
        return out
    for c in claims:
        if c.get('evidence_text') and c['source'] in ('treatment-sequence.minimum_intervals', 'treatment-optimization.combination_rules'):
            c['evidence'] = guide_refs(c['evidence_text'], c['id'])
    for c in cond_claims:
        if c.get('evidence_text'):
            c['evidence'] = guide_refs(c['evidence_text'], c['id'])
    evidence_kind_by_file = {'anatomy-danger-zones': AZ['consensus_method'], 'literature-evidence': LE['source_method'],
                             'post-procedure-timeline': SRC['post-procedure-timeline']['consensus_method'], 'treatment-optimization': OPT['consensus_method'],
                             '그 밖': '파일에 방법 표기 없음 → evidence_kind 「원천 표기 없음」'}

    for k in cond_claims:
        if isinstance(k['target'], dict):
            k['scope_conditional'] = scope_mark(k['target'], k['id'])

    # ───────── 충돌 하나로(사용자 10-30 · D-13b 바꿈 · conflict_resolution) ─────────
    CR = DEC['conflict_resolution']
    CR_RULES = {r['id'] for r in CR['rules']}

    def cr_need(rule, where):
        if rule and rule not in CR_RULES:
            op('충돌 해결 규칙이 결정에 없음', rule=rule, where=where)
    USETS = UnitSets(U['units'])
    ESET = {e['id']: (USETS.of(e['a']), USETS.of(e['b'])) for e in edges}
    EBY = {e['id']: e for e in edges}
    CSIDE = {c['id']: (USETS.side(c['a']), USETS.side(c['b'])) for c in claims}
    CVU = {c['id']: cr_units_of_claim(c, CR) for c in claims}

    def covers(f, e):
        a1, b1 = ESET[f['id']]
        a2, b2 = ESET[e['id']]
        return (a2 <= a1 and b2 <= b1) or (a2 <= b1 and b2 <= a1)

    def straight_for(cid, A, B):
        sa, sb = CSIDE[cid]
        if A <= sa and B <= sb:
            return True
        if A <= sb and B <= sa:
            return False
        return bool(A & sa and B & sb)

    def cr_items(cids, A, B):
        it = []
        for cid in cids:
            if CLAIM[cid].get('scope_conditional'):
                continue  # 조건부(단위 시술 미특정) = 기본 응답 밖 — 값 접기에서도 뺌(조회 옵션으로만)
            st = straight_for(cid, A, B)
            for vc in CVU[cid]:
                it.append((vc, vc['first'] if st else cr_flip(vc['first'])))
        return it

    def cr_check(owner, r):
        for rr in r['rules']:
            cr_need(rr, owner)
        for f in ('first', 'same_day', 'days'):
            opts = [o for o in r['options'] if o['field'] == f]
            if opts and r[f] is not None:
                op('두 값 — 겉 칸과 하위 조건 옵션이 같이 있음', where=owner, field=f)
            if opts and sum(1 for o in opts if CR['unknown_condition_key'] in o['sub_condition']) != 1:
                op('두 값 — 조건 모름 옵션이 하나가 아님', where=owner, field=f)
            if f == 'same_day' and r.get('by_direction') and r['same_day'] is not None and len({v['same_day'] for v in r['by_direction'].values() if v['same_day'] is not None}) > 1:
                op('두 값 — 방향별 같은 날 값이 다른데 겉 칸을 채움', where=owner)
            if f == 'first' and r['field_status'].get(f) == '의료진 확인' and r[f] is not None:
                op('두 값 — 순서 반대인데 순서를 단정함', where=owner)
    ANC = {e['id']: [f['id'] for f in edges if covers(f, e)] for e in edges}
    TRACES = []
    for e in edges:
        cids = sorted({x for fid in ANC[e['id']] for x in EBY[fid]['claims']})
        r = cr_resolve(cr_items(cids, *ESET[e['id']]), CR)
        TRACES.append((e['id'], r.pop('trace')))
        r['inherited_claims'] = sorted(set(cids) - set(e['claims']))
        r['inherited_from_edges'] = sorted(set(ANC[e['id']]) - {e['id']})
        e['resolved'] = r
        cr_check(e['id'], r)
    # 전수 가드 — 단위 시술 쌍마다 앱이 읽는 값(가장 구체적인 엣지의 resolved)이 하나인가 · 형제 엣지가 겹쳐 둘이면 쌍 하나로 접어 둔다(resolved_pairs)
    PE = collections.defaultdict(dict)
    for e in edges:
        A, B = ESET[e['id']]
        for u in A:
            for v in B:
                if u != v:
                    PE[(u, v) if u < v else (v, u)].setdefault(e['id'], u < v)
    resolved_pairs, two_value = [], []
    for k, m in sorted(PE.items()):
        ids = sorted(m)
        ms = [i for i in ids if not any(j != i and covers(EBY[i], EBY[j]) and not covers(EBY[j], EBY[i]) for j in ids)]
        if len({cr_view(EBY[i]['resolved'], m[i]) for i in ms}) <= 1:
            continue
        cids = sorted({x for i in ids for x in EBY[i]['claims']})
        r = cr_resolve(cr_items(cids, {k[0]}, {k[1]}), CR)
        pid = f'RP8-{len(resolved_pairs) + 1:04d}'
        TRACES.append((pid, r.pop('trace')))
        resolved_pairs.append({'id': pid, 'a': f'unit:{k[0]}', 'b': f'unit:{k[1]}', 'most_specific_edges': ms, 'applicable_edges': ids, 'resolved': r})
        cr_check(pid, r)
    RPK = {(p['a'][5:], p['b'][5:]) for p in resolved_pairs}
    for k, m in PE.items():
        ids = sorted(m)
        ms = [i for i in ids if not any(j != i and covers(EBY[i], EBY[j]) and not covers(EBY[j], EBY[i]) for j in ids)]
        if k not in RPK and len({cr_view(EBY[i]['resolved'], m[i]) for i in ms}) > 1:
            two_value.append(k)
            op('두 값 — 단위 시술 쌍에 가장 구체적인 엣지 값이 둘 이상', pair=list(k), edges=ms)
    # 계열 쌍 충돌(X8) 처분 — 앱이 읽는 값(엣지 · 쌍 resolved)의 묶음 기록에서 셈
    REV = CR['review_status']
    for x in conflicts:
        if x['type'] == '간격 수치':
            side_of, field = {cid: cid for cid in x['sides']}, 'days'
        else:
            side_of = {cid: s for sd in (x['sides'], x.get('sides_from_bundle') or {}) for s, lst in sd.items() for cid in lst}
            field = 'first' if x['type'].startswith('순서') else 'same_day'
        hits = []
        for owner, tr in TRACES:
            for g in tr.get(field, []):
                if len({side_of[c] for c in g['claims'] if c in side_of}) > 1:
                    hits.append((owner, g))
        if any(g['status'] == '의료진 확인' for _, g in hits):
            st, rule = '의료진 확인', 'R5'
        elif any(g['rule'] in ('R3', 'R4') for _, g in hits):
            st, rule = '보수적 선택', ('R3' if field == 'days' else 'R4')
        else:
            st, rule = '조건 분리(가짜 충돌)', 'R1'
        cr_need(rule, x['id'])
        x['resolution'] = {'status': st, 'rule': rule, 'review_status': REV[st], 'rule_text': next((r['text'] for r in CR['rules'] if r['id'] == rule), None),
                           'where': sorted({o for o, g in hits if (st == '의료진 확인' and g['status'] == '의료진 확인') or (st != '의료진 확인' and g['rule'])}),
                           'why': (CR['x8_why'][rule])}
    X8_STAFF = {x['id'] for x in conflicts if x['resolution']['status'] == '의료진 확인'}
    # 의료진 확인 묶음은 전부 원천 질문에 걸린 X8 에서 나와야 한다(계열 쌍 셈 밖의 순서 반대가 있으면 open)
    staff_groups = [(o, g) for o, tr in TRACES for g in tr.get('first', []) if g['status'] == '의료진 확인']
    for o, g in staff_groups:
        cs = set(g['claims'])
        if not any(len({s for sd in (x['sides'], x.get('sides_from_bundle') or {}) for s, lst in sd.items() if cs & set(lst)}) > 1 for x in conflicts if x['id'] in X8_STAFF):
            op('의료진 확인(순서 반대)인데 계열 쌍 충돌 · 원천 질문에 안 걸림', where=o, claims=sorted(cs))
    # 엣지 · 주장 표시 — 「충돌」 → 해제는 표시 없음 · 「보수적 선택」 · 진짜 반대만 「의료진 확인」(키 review_status 유지 · 값 바꿈 · 이전 값은 conflict_before)
    staff_claims = {c for o, g in staff_groups for c in g['claims']}
    alt_claims = {a['claim'].split('#')[0] for e in edges for a in e['resolved']['alternatives']} | {a['claim'].split('#')[0] for p in resolved_pairs for a in p['resolved']['alternatives']}
    for e in edges:
        e['conflict_before'] = e['review_status'] == 'conflict'
        e['review_status'] = REV[e['resolved']['status']]
        e['review_label'] = CR['review_label'][e['review_status']]
    for c in claims:
        c['conflict_before'] = c['review_status'] == 'conflict'
        c['review_status'] = REV['의료진 확인'] if c['id'] in staff_claims else (REV['보수적 선택'] if c['id'] in alt_claims else REV['하나'])
        c['review_label'] = CR['review_label'][c['review_status']]

    # 확인 조건 등급(R2) — 대상 키(공통 · 계열 · 단위 시술 · 제품 · 원장 항목) × 조건마다 하나 · 위 키(상속)까지 접어 더 엄격한 쪽
    GO = CR['grade_order']

    def tkeys(t):
        if isinstance(t, str):
            return ['all'] if t == '모든 시술(공통)' else [t]
        if isinstance(t, list):
            return [('units:' + x) if x.startswith('U5-') else x for x in t]
        return ep_keys(t)

    def key_covers(k1, k2):
        if k1 == k2 or k1 == 'all':
            return True
        s1, s2 = USETS.of(k1), USETS.of(k2)
        return bool(s1) and bool(s2) and s2 <= s1
    by_kc = collections.defaultdict(list)
    for k in cond_edges:
        if k.get('scope_conditional') or k['grade3'] not in GO:
            continue
        for tk in tkeys(k['target']):
            for cid in k['conditions']:
                by_kc[(tk, cid)].append(k)

    def grade_entry(tk, cid, rows, eid):
        g = min((r['grade3'] for r in rows), key=GO.index)
        diff = len({r['grade3'] for r in rows}) > 1
        if diff:
            cr_need('R2', eid)
        return {'id': eid, 'target': tk, 'condition': cid, 'grade3': g, 'rule': 'R2' if diff else None, 'status': '보수적 선택' if diff else '하나',
                'from': sorted({r['id'] for r in rows}), 'inherited': sorted({r['id'] for r in rows} - {r['id'] for r in by_kc.get((tk, cid), [])}),
                'alternatives': [{'claim': r['id'], 'grade3': r['grade3'], 'grade_original': r['grade_original'], 'source': r['source'].split('.')[0], 'text': r['text']}
                                 for r in rows if r['grade3'] != g]}
    cond_resolved = []
    for (tk, cid) in sorted(by_kc):
        rows = {r['id']: r for (k2, c2), rs in by_kc.items() if c2 == cid and key_covers(k2, tk) for r in rs}
        cond_resolved.append(grade_entry(tk, cid, list(rows.values()), f'KR8-{len(cond_resolved) + 1:04d}'))
    KRI = {(x['target'], x['condition']): x for x in cond_resolved}
    # 전수 가드 — 단위 시술 × 조건마다 가장 구체적인 키 값이 하나인가 · 형제 키가 겹쳐 둘이면 단위 시술 키로 하나 더 접어 둔다
    for u in sorted(USETS.ALL):
        for cid in sorted({c for _, c in KRI}):
            app = [tk for (tk, c2) in KRI if c2 == cid and key_covers(tk, 'units:' + u)]
            ms = [a for a in app if not any(b != a and key_covers(a, b) and not key_covers(b, a) for b in app)]
            if len({KRI[(a, cid)]['grade3'] for a in ms}) > 1:
                rows = {r['id']: r for a in app for r in by_kc.get((a, cid), [])}
                x = grade_entry('units:' + u, cid, list(rows.values()), f'KR8-{len(cond_resolved) + 1:04d}')
                x['why'] = '형제 키(' + ' · '.join(ms) + ') 값이 달라 단위 시술 키로 접음'
                cond_resolved.append(x)
                KRI[('units:' + u, cid)] = x
    for u in sorted(USETS.ALL):
        for cid in sorted({c for _, c in KRI}):
            app = [tk for (tk, c2) in KRI if c2 == cid and key_covers(tk, 'units:' + u)]
            ms = [a for a in app if not any(b != a and key_covers(a, b) and not key_covers(b, a) for b in app)]
            if len({KRI[(a, cid)]['grade3'] for a in ms}) > 1:
                op('두 값 — 단위 시술 × 조건 등급이 둘 이상', unit=u, condition=cid, keys=ms)
    for k in cond_edges:
        gr = {cid: KRI[(tk, cid)]['grade3'] for tk in tkeys(k['target']) for cid in k['conditions'] if (tk, cid) in KRI}
        k['grade3_resolved'] = gr
        k['resolution_rule'] = 'R2' if any(g != k['grade3'] for g in gr.values()) else None
    for x in grade_conflicts:
        e = KRI.get((x['family'], x['condition']))
        if not e:
            op('등급 충돌인데 해결 값 없음', where=x['id'])
            continue
        x['resolution'] = {'status': '보수적 선택', 'rule': 'R2', 'grade3': e['grade3'], 'resolved_id': e['id'], 'review_status': REV['보수적 선택'],
                           'alternatives': e['alternatives']}
    # 대기 기간(R6 = R3 더 긴 쪽 · 원문이 깊이 · 박리를 적었으면 R1 로 나눔)
    wait_resolved = []
    XW_CONDS = {x['condition'] for x in wait_conflicts}
    for cd in CONDS:
        if cd['id'] not in XW_CONDS:
            continue  # 대기 기간이 원천끼리 안 다른 조건은 주장 하나 그대로(두 값 없음)
        segs = []
        for c in cond_claims:
            if cd['id'] in c['conditions']:
                for depth, ms_ in cr_wait_segments(' '.join(filter(None, [c['text'], c.get('detail')])), CR):
                    segs.append((depth, max(ms_), c['id']))
        if not segs:
            continue
        depths = sorted({d for d, _, _ in segs if d})
        groups = [(d, [s for s in segs if s[0] in (d, None)]) for d in depths] or [(None, segs)]
        vals = {d: max(s[1] for s in g) for d, g in groups}
        allmax = max(s[1] for s in segs)
        diff_src = len({s[1] for s in segs}) > 1
        split = len(set(vals.values())) > 1
        rules = (['R1'] if split else []) + (['R6'] if diff_src else [])
        for rr in rules:
            cr_need(rr, f'WR8-{cd["id"]}')
        ud = LEX['units_days']['개월']
        wr = {'id': f'WR8-{cd["id"]}', 'condition': cd['id'], 'what': f'{cd["name"]} 대기 기간',
              'months': None if split else allmax, 'days': None if split else [allmax * ud, allmax * ud], 'open_high': True,
              'by_sub_condition': split, 'options': ([{'sub_condition': {CR['wait_axes'][0]['axis']: d}, 'months': v, 'days': [v * ud, v * ud],
                                                       'from': sorted({s[2] for s in g})} for (d, g), v in zip(groups, [vals[d] for d, _ in groups])]
                                                     + [{'sub_condition': {CR['unknown_condition_key']: CR['unknown_condition_label']}, 'months': allmax, 'days': [allmax * ud, allmax * ud],
                                                         'from': sorted({s[2] for s in segs})}]) if split else [],
              'rules': rules, 'status': '보수적 선택' if diff_src else '하나',
              'alternatives': [{'claim': cid_, 'depth': d, 'months': m} for d, m, cid_ in segs if m != (vals.get(d) if d else (allmax if not split else None))]}
        wait_resolved.append(wr)
        for c in cond_claims:
            if cd['id'] in c['conditions'] and any(s[2] == c['id'] for s in segs):
                c.setdefault('wait_resolved', []).append(wr['id'])
    WRI = {w['condition']: w for w in wait_resolved}
    for x in wait_conflicts:
        w = WRI.get(x['condition'])
        if not w:
            op('대기 기간 충돌인데 해결 값 없음', where=x['id'])
            continue
        x['resolution'] = {'status': '보수적 선택', 'rule': 'R6', 'rules': w['rules'], 'resolved_id': w['id'], 'review_status': REV['보수적 선택'],
                           'options': w['options'], 'months': w['months']}

    # ───────── 원천 질문(규칙으로 하나로 안 정해지는 것만) ─────────
    QS = DEC.get('origin_questions') or []
    need = []
    for c in claims:
        for s in 'ab':
            e = c[s]
            for pp in [e] + e.get('parts', []):
                if pp.get('level') == '해석 안 됨':
                    need.append(('unresolved_name', pp.get('text'), c['id']))
                if pp.get('level') == '용도 조건' and pp.get('qualifier') not in {x['note'] for x in DEC['purpose_ok']}:
                    need.append(('purpose_word', pp.get('text'), c['id']))
                if pp.get('level') in DEC['wide_candidates_levels'] and pp.get('n_units', 0) > DEC['wide_candidates_threshold']:
                    need.append(('wide_candidates', pp.get('text'), c['id']))
            if e.get('code_mismatch'):
                need.append(('code_mismatch', e.get('text'), c['id']))
    for av in avoids:
        if bad_ep(av['to']):
            need.append(('unresolved_name', av['to'].get('text'), av['id']))
    for k in cond_claims:
        if isinstance(k['target'], dict) and bad_ep(k['target']):
            need.append(('unresolved_name', k['target'].get('text'), k['id']))
    for x in conflicts:
        if x['resolution']['status'] == '의료진 확인':  # 10-30 — 진짜 반대만 질문(조건 분리 · 보수적 선택은 규칙으로 정함 · 등급 R2 · 대기 R6 도 질문 없음)
            need.append(('conflict', '↔'.join(x['pair']) + ' ' + x['type'], x['id']))
    for g in ev_guide.values():
        if g['kind'].startswith('출처 아님'):
            need.append(('guide_not_source', g['label'], g['id']))
    for owner, text, words in scoped:
        need.append(('scope_conditional', text, owner))
    for sid in se_exceptions:
        need.append(('side_effect_exception', sid, sid))

    def q_covers(q, typ, text):
        m = q['match']
        if m['type'] != typ:
            return False
        if 'texts' in m:
            return text in m['texts']
        if 'pairs' in m:
            return any(text.startswith(p) for p in m['pairs'])
        if 'conditions' in m:
            return text in m['conditions']
        return m.get('all', False)
    origin_q = {q['id']: dict(q, refs=[]) for q in QS}
    for typ, text, ref in need:
        hit = [q for q in QS if q_covers(q, typ, text)]
        if not hit:
            op('원천 질문이 필요한데 결정에 없음', kind=typ, text=text, ref=ref)
        for q in hit:
            if ref not in origin_q[q['id']]['refs']:
                origin_q[q['id']]['refs'].append(ref)
    for q in origin_q.values():
        if not q['refs']:
            STALE.append({'type': '걸리는 행 없는 원천 질문', 'id': q['id']})

    # 원천 수정 후보(규칙으로 계산)
    source_fix = []
    for c in claims:
        for s in 'ab':
            if c[s].get('code_mismatch'):
                source_fix.append({'what': '원천 시술군 코드 ↔ 정본 계열 어긋남', 'claim': c['id'], 'source': c['source'], 'source_index': c['source_index'], 'text': c[s]['text'], 'note': c[s]['code_mismatch']})
    for g in ev_guide.values():
        if g['kind'].startswith('출처 아님'):
            source_fix.append({'what': '출처 칸이 출처가 아님', 'evidence': g['id'], 'text': g['label'], 'used_by': g['used_by']})

    # ───────── 같은 성격 전수 — 원천 행 · 8단계 칸 · 7단계 메모 ─────────
    def walk(o, path):
        """source-map 칸 경로(a[].b · {code}) → 값 수(None · 빈 값 뺌)."""
        parts = path.split('.')
        vals = [o]
        for p in parts:
            nxt = []
            arr = p.endswith('[]')
            key = p[:-2] if arr else p
            for v in vals:
                if key == '{code}':
                    if isinstance(v, dict):
                        nxt += [x for k, x in v.items() if re.match(r'^(M|N)\d+', k)]
                    continue
                if not isinstance(v, dict) or key not in v:
                    continue
                x = v[key]
                if arr:
                    if isinstance(x, list):
                        nxt += x
                else:
                    nxt.append(x)
            vals = nxt
        return sum(1 for v in vals if v is not None)
    FH = DEC['field_handlers']
    coverage = []
    for f in SMAP['fields']:
        if not any(str(d['stage']) == '8' for d in f['destinations']):
            continue
        fn = f['file'].replace('.json', '')
        if fn not in SRC:
            op('8단계 칸 원천 파일을 안 읽음', file=f['file'], path=f['path'])
            continue
        n = walk(SRC[fn], f['path'])
        h = next((x for x in FH if x['file'] == fn and (f['path'] == x['prefix'] or f['path'].startswith(x['prefix'] + '.') or f['path'].startswith(x['prefix'] + '[]'))), None)
        coverage.append({'file': fn, 'path': f['path'], 'n_map': f['n_values'], 'n_now': n, 'handler': h['section'] if h else None})
        if h is None:
            op('8단계 칸인데 반영 규칙 없음(field_handlers)', file=fn, path=f['path'])
        if n != f['n_values']:
            op('8단계 칸 값 수가 source-map 과 다름', file=fn, path=f['path'], n_map=f['n_values'], n_now=n)
    # 원천 행 → 행선지(관계 칸)
    rows = []
    rows += [('contraindications.rules', i) for i in range(len(SRC['contraindications']['rules']))]
    rows += [('synergy.links', i) for i in range(len(SRC['synergy']['links']))]
    rows += [('treatment-sequence.incompatible_same_day', i) for i in range(len(TS['incompatible_same_day']))]
    rows += [('treatment-sequence.minimum_intervals', i) for i in range(len(TS['minimum_intervals']))]
    rows += [('treatment-sequence.principles', i) for i in range(len(TS['principles']))]
    rows += [('treatment-sequence.sequence_order', x['order']) for x in TS['sequence_order']]
    rows += [('treatment-sequence.common_combos.note', i) for i, x in enumerate(TS['common_combos']) if x.get('note')]
    rows += [('treatment-optimization.combination_rules', i) for i in range(len(OPT['combination_rules']))]
    rows += [('treatment-optimization.by_concern.sequence', f'{ci}.{si}') for ci, c in enumerate(OPT['by_concern']) for si, s in enumerate(c['severity_levels']) if s.get('sequence')]
    rows += [('treatment-optimization.by_concern.contraindicated_combos', f'{ci}.{si}.{k}') for ci, c in enumerate(OPT['by_concern']) for si, s in enumerate(c['severity_levels'])
             for k in range(len(s.get('contraindicated_combos') or []))]
    rows += [('treatment-optimization.by_age_group.avoid', f"{a['age']}#{j}") for a in OPT['by_age_group'] for j in range(len(a['avoid']))]
    rows += [('problem-combos.riskBenefit', pk['id']) for pb in SRC['problem-combos']['combos'] for pk in pb.get('packages') or [] if pk.get('riskBenefit')]
    rows += [(('problem-packages.complaints[].combos' if len(cb['combo']) > 1 else 'problem-packages.combos'), f"{p['problem_id']}:{c['cc']}#{k}")
             for p in SRC['problem-packages']['problems'] for c in p['complaints'] for k, cb in enumerate(c.get('combos') or [])]
    rows += [('problem-packages.complaints[].alternatives', f"{p['problem_id']}:{c['cc']}#{k}") for p in SRC['problem-packages']['problems'] for c in p['complaints']
             for k, alt in enumerate(c.get('alternatives') or []) if re.search(LEX['interval_words'], alt)]
    rows += [('combo-recipes.followUp', f"{r.get('id')}#{k}") for r in SRC['combo-recipes']['recipes'] for k in range(len(r.get('followUp') or []))]
    row_missing = [r for r in rows if not landed.get((r[0], str(r[1])))]
    # 원천 행 1:1 착지표(품질 I · 10-30) — 행마다 어디로 갔는지(주장 · 확인 조건 · 피함 id / 원문만 text_only · 계열 원문 attr · 순위 sequence_rank). 빠진 행은 위 open
    row_landing = [{'source': r[0], 'index': str(r[1]), 'landed': sorted(set(landed.get((r[0], str(r[1]))) or [])),
                    'how': ('구조(주장 · 조건 · 피함)' if any(str(x).startswith(('R8-', 'K8-', 'AV8-')) for x in landed.get((r[0], str(r[1]))) or [])
                            else ('원문만(규칙 — 쌍 없는 원칙 · 계열 원문 · 순위)' if landed.get((r[0], str(r[1]))) else '없음'))} for r in rows]
    for r in row_missing:
        op('원천 행 행선지 없음', source=r[0], source_index=str(r[1]))
    # 7단계 메모 245 대조 — 원천 칸별 수 · 원문
    recon = []
    NS = DEC['step7_note_sources']
    for src7, cnt in sorted(C_(x['source'] for x in S7['step8_notes']).items()):
        mine = NS.get(src7)
        if mine is None:
            op('7단계 메모 원천이 8단계 결정에 없음', source=src7)
            continue
        n_rows = sum(1 for r in rows if r[0] in mine)
        n_claim = sum(1 for c in claims if c['source'] in mine)
        n_attr = sum(1 for a in attrs if a['source'] in mine)
        n_cond = sum(1 for k in cond_claims if k['source'] in mine)
        n_av = sum(1 for a in avoids if a['source'] in mine)
        recon.append({'note_source': src7, 'notes': cnt, 'source_rows': n_rows, 'claims': n_claim, 'attrs': n_attr, 'conditions': n_cond, 'avoids': n_av})
        if src7 in seq_texts:
            for x in S7['step8_notes']:
                if x['source'] == src7 and x['text'] not in seq_texts[src7]:
                    op('7단계 메모 원문이 8단계 처리 원문에 없음', source=src7, text=x['text'])
        elif n_rows != cnt:
            op('7단계 메모 수 ≠ 8단계 원천 행 수', source=src7, notes=cnt, rows=n_rows)
    # 결정이 가리키는데 안 쓰인 사전 낱말
    for a in RES['alias']:
        if norm(a['text']) not in USED_ALIAS:
            STALE.append({'type': '안 쓰인 이름 풀이 사전 항목', 'text': a['text']})

    # 조사 판 대비(정보 — open 아님)
    R = json.load(open(W / DEC['research'][0]))
    res_by = C_(c['source'] for c in R['A_relations']['claims'])
    now_by = C_(c['source'] for c in claims)
    RS = DEC['research_diff_reasons']
    rows_d = [('claims.' + s, res_by.get(s, 0), now_by.get(s, 0)) for s in sorted(set(res_by) | set(now_by))]
    for t in sorted(set(C_(x['type'] for x in R['A_relations']['conflicts'])) | set(C_(x['type'] for x in conflicts))):
        rows_d.append(('conflicts.' + t, sum(1 for x in R['A_relations']['conflicts'] if x['type'] == t), sum(1 for x in conflicts if x['type'] == t)))
    rows_d.append(('condition_claims', len(R['B_conditions']['claims']), len(cond_claims)))
    rows_d.append(('avoid_edges', 0, len(avoids)))
    rows_d.append(('bundle_claims', sum(1 for c in R['A_relations']['claims'] if c.get('bundle_word')), sum(1 for c in claims if c['bundle_word'])))
    rk, nk = dict(C_(c['kind'] for c in R['A_relations']['claims'])), dict(C_(c['kind'] for c in claims))
    rows_d.append(('claim_kinds', json.dumps(dict(sorted(rk.items())), ensure_ascii=False), json.dumps(dict(sorted(nk.items())), ensure_ascii=False)))
    research_diff = []
    for item, rv, nv in rows_d:
        why = RS.get(item)
        if rv != nv and not why:
            op('조사 판 대비 셈 차이 이유 없음(research_diff_reasons)', item=item, research=rv, now=nv)
        research_diff.append({'item': item, 'research': rv, 'now': nv, 'reason': why if rv != nv else '같음'})

    # ───────── 저장 ─────────
    person = [k for k in cond_claims if k['kind'].startswith('사람 조건')]
    summary = {
        'claims': len(claims), 'claims_by_kind': dict(sorted(C_(c['kind'] for c in claims).items())), 'claims_by_source': dict(sorted(now_by.items())),
        'edges': len(edges), 'edges_conflict': sum(1 for e in edges if e['review_status'] == 'conflict'),
        'conflicts': len(conflicts), 'conflicts_by_type': dict(sorted(C_(x['type'] for x in conflicts).items())),
        'grade_conflicts': len(grade_conflicts), 'wait_conflicts': len(wait_conflicts),
        'not_procedure_claims': sum(c['not_procedure'] for c in claims), 'bundle_claims': sum(c['bundle_word'] for c in claims),
        'unresolved_claims': sum(not c['resolved'] for c in claims),
        'interval_filled': sum(1 for c in claims if c.get('interval') and (c['interval']['days'] is not None or c['interval']['same_day'] is not None or c['interval'].get('first'))),
        'condition_nodes': len(cond_nodes), 'condition_claims': len(cond_edges), 'not_condition_claims': len(not_condition),
        'not_condition_by_kind': dict(sorted(C_(k['kind'] for k in not_condition).items())), 'person_condition_claims': len(person),
        'grade3': dict(sorted(C_(k['grade3'] for k in person).items())), 'avoid_edges': len(avoids),
        'complications': len(comp_nodes), 'complications_by_source': dict(sorted(C_('U1 taxonomy' if c.get('source') else 'complications.json' for c in comp_nodes).items())),
        'side_effects': len(side_effects), 'side_effect_exceptions': len(se_exceptions), 'side_effect_gap_families': len(se_gap),
        'gap_filled_families': {k: dict(sorted(v.items())) for k, v in sorted(gap_filled.items())},
        'complication_gap_families': len(comp_gap), 'complication_mild_only_families': comp_none_mild_only, 'site_caution': len(site_caution), 'timelines': len(timelines), 'pih': len(pih_attach),
        'evidence': {'literature': len(ev_lit), 'statements': len(statements), 'web': len(ev_web), 'guides': len(ev_guide)},
        'scope_conditional': {'claims': sum(1 for c in claims if c.get('scope_conditional')), 'avoid_edges': sum(1 for a in avoids if a.get('scope_conditional')),
                              'condition_claims': sum(1 for k in cond_claims if k.get('scope_conditional'))},
        'by_sub_condition': sum(1 for c in claims if (c.get('interval') or {}).get('by_sub_condition')),
        'web_evidence': dict(sorted(C_(w['kind'] for w in ev_web.values()).items()), multi_url=sum(1 for w in ev_web.values() if w['multi_url'])),
        'attrs': len(attrs), 'origin_questions': sum(1 for q in origin_q.values() if q['refs']), 'source_fix_candidates': len(source_fix),
        'coverage_fields': len(coverage), 'source_rows': len(rows), 'open': len(OPEN), 'stale_decisions': len(STALE),
        'conflict_resolution': {
            'x8': dict(sorted(C_(x['resolution']['status'] for x in conflicts).items())),
            'x8_from_bundle_new': sum(1 for x in conflicts if x.get('from_bundle')), 'x8_with_bundle_sides': sum(1 for x in conflicts if x.get('sides_from_bundle')),
            'grade_conflicts_conservative': sum(1 for x in grade_conflicts if x.get('resolution')),
            'wait_conflicts_conservative': sum(1 for x in wait_conflicts if x.get('resolution')),
            'fake_released': sum(1 for x in conflicts if x['resolution']['rule'] == 'R1'),
            'conservative': sum(1 for x in conflicts if x['resolution']['rule'] in ('R3', 'R4')) + sum(1 for x in grade_conflicts if x.get('resolution')) + sum(1 for x in wait_conflicts if x.get('resolution')),
            'staff_true_opposition': sum(1 for x in conflicts if x['resolution']['rule'] == 'R5'),
            'edges_by_status': dict(sorted(C_(e['resolved']['status'] for e in edges).items())),
            'edges_by_review_status': dict(sorted(C_(e['review_status'] for e in edges).items())),
            'edges_by_sub_condition': sum(1 for e in edges if e['resolved']['by_sub_condition']),
            'edges_by_direction_split': sum(1 for e in edges if e['resolved'].get('by_direction') and len({v['same_day'] for v in e['resolved']['by_direction'].values() if v['same_day'] is not None}) > 1),
            'edges_rules': dict(sorted(C_(r for e in edges for r in e['resolved']['rules']).items())),
            'claims_by_review_status': dict(sorted(C_(c['review_status'] for c in claims).items())),
            'resolved_pairs': len(resolved_pairs), 'resolved_pairs_by_status': dict(sorted(C_(p['resolved']['status'] for p in resolved_pairs).items())),
            'unit_pairs_checked': len(PE), 'two_value_unit_pairs': len(two_value),
            'condition_resolved': len(cond_resolved), 'condition_resolved_conservative': sum(1 for x in cond_resolved if x['rule']),
            'condition_resolved_unit_fold': sum(1 for x in cond_resolved if x.get('why')),
            'wait_resolved': len(wait_resolved), 'origin_questions_retired': [q['id'] for q in DEC.get('origin_questions_retired') or []],
        },
    }
    out = {
        'version': 'step8-v1', 'generated_by': 'step8-apply.py', 'decision_ref': DEC['decision_ref'],
        'inputs': {'source': str(SRCP), 'canon': CAN, 'decisions': Path(ARGS.decisions).name},
        'reading_contract': DEC['reading_contract'],
        'summary': summary,
        'edges': edges, 'resolved_pairs': resolved_pairs, 'claims': claims, 'conflicts': conflicts, 'avoid_edges': avoids,
        'sequence_rank': sequence_rank, 'principles_text_only': principles_text_only, 'optimization_principles': OPT['optimization_principles'],
        'package_evidence': pkg_evidence, 'profile_attrs': profile_attrs, 'attrs': attrs,
        'conditions': {'nodes': cond_nodes, 'claims': cond_edges, 'not_condition': not_condition, 'not_condition_rule': DEC['semantic_apply']['not_condition_rule'], 'grade_conflicts': grade_conflicts, 'wait_conflicts': wait_conflicts, 'extracted_vs_taxonomy': ext_check,
                       'resolved': cond_resolved, 'wait_resolved': wait_resolved},
        'safety': {'complications': comp_nodes, 'side_effects': side_effects, 'side_effect_rule': DEC['semantic_apply']['side_effect_rule'],
                   'side_effect_gap_families': se_gap, 'complication_gap_families': comp_gap,
                   'complication_mild_only_families': {'families': comp_none_mild_only, 'note': '합병증 원천은 있으나 전부 severity mild → 부작용으로 감(gap 아님 — 원천이 중대 반응을 안 적음)'}, 'complication_names_multi_family': name_multi, 'site_caution': site_caution,
                   'critical_safety_facts': crit, 'timelines': timelines, 'pih': pih_attach, 'unit_safety_status': unit_safety_status, 'unit_gaps': unit_gaps, 'family_text': {k: family_text[k] for k in sorted(family_text)},
                   'item_text_counts': dict(sorted(item_text.items())), 'item_aftercare_dest': dict(sorted(item_dest.items()))},
        'evidence': {'literature': list(ev_lit.values()), 'statements': statements, 'web': list(ev_web.values()), 'guides': list(ev_guide.values()), 'evidence_kind_by_file': evidence_kind_by_file},
        'origin_questions': [q for q in origin_q.values() if q['refs']], 'origin_questions_retired': DEC.get('origin_questions_retired') or [],
        'conflict_resolution_rules': DEC['conflict_resolution']['rules'], 'source_fix_candidates': source_fix,
        'step7_reconcile': recon, 'coverage': coverage, 'row_landing': row_landing, 'research_diff': research_diff,
        'site_climb': {'rule': DEC['resolver']['site_climb']['rule'], 'events': sorted({json.dumps(x, ensure_ascii=False, sort_keys=True) for x in CLIMB_LOG})},
        'open': OPEN, 'stale_decisions': STALE,
    }
    json.dump(out, open(OUT / 'step8-relations.json', 'w'), ensure_ascii=False, indent=1)
    write_md(out, OUT, DEC)
    print(json.dumps(summary, ensure_ascii=False))
    return out


def write_md(o, OUT, DEC):
    s = o['summary']
    L = ['# 실버 8단계 — 관계 · 확인 조건 · 안전 · 근거 (반영)', '',
         f"`step8-apply.py` 결정론 산출 · 결정 `step8-decisions.json` · 정본 `step8-relations.json`. 원천 `{Path(o['inputs']['source']).name}` 은 읽기만.", '',
         '- 사람 확인 게이트 없음(U8-1 (나)) — 원칙 · 규칙 · 위험 문장 · 화살표 문장 모두 문장 패턴 규칙(`sentence.patterns`)으로 쌍을 만든다 · 규칙으로 하나로 안 정해지는 것만 원천 질문',
         '- 간격은 간격 낱말 사전(`interval_lexicon`) — **추천 · AI 는 `interval.days` · `interval.first` · `interval.same_day` 만 읽는다** · 원문은 `interval.text` 보관',
         f"- 고민 조건 금기 = 7단계 고민 노드 → 「{DEC['avoid_edge_type']['label_ko']}」 엣지(`{DEC['avoid_edge_type']['name']}` · SPEC-004 개정은 빌드 때 · U8-2 (가))",
         '- **충돌은 하나로(10-30 · D-13b 바꿈)** — 조건 다르면 나눔(R1) · 등급 더 엄격(R2) · 간격 더 긴 쪽(R3) · 같은 날 불가(R4) · 순서 반대 = 순서 단정 안 함 + 의료진(R5) · 대기 더 긴 쪽(R6). 원문은 alternatives · **앱은 `edges[].resolved` · `resolved_pairs` · `conditions.resolved` · `conditions.wait_resolved` 만 읽는다**', '',
         '## 셈', '', '| 항목 | 셈 |', '|---|---|',
         f"| 관계 주장 | {s['claims']} — " + ' · '.join(f'{k} {v}' for k, v in s['claims_by_kind'].items()) + ' |',
         f"| 관계 엣지(끝점 쌍) | {s['edges']} (충돌 표시 {s['edges_conflict']}) |",
         f"| 충돌 | 계열 쌍 {s['conflicts']} (" + ' · '.join(f'{k} {v}' for k, v in s['conflicts_by_type'].items()) + f") · 조건 등급 {s['grade_conflicts']} · 대기 기간 {s['wait_conflicts']} |",
         f"| 간격 숫자 칸 채운 주장 | {s['interval_filled']} / {s['claims']} |",
         f"| 시술 아님 끝점 주장 · 묶음 낱말 주장 · 못 푼 이름 주장 | {s['not_procedure_claims']} · {s['bundle_claims']} · {s['unresolved_claims']} |",
         f"| 확인 조건 | 노드 {s['condition_nodes']} · 주장 {s['condition_claims']}(사람 조건 {s['person_condition_claims']} — " + ' · '.join(f'{k} {v}' for k, v in s['grade3'].items()) + ') |',
         f"| 피함(고민 조건 금기) | {s['avoid_edges']} |",
         f"| 합병증 · 주의(site_caution) | {s['complications']} {s['complications_by_source']} (원천 없는 계열 {s['complication_gap_families']}) · {s['site_caution']} |",
         f"| 부작용(계열 속성 · U2 · B1) | {s['side_effects']}(의료진 질문 예외 {s['side_effect_exceptions']} · 없는 계열 {s['side_effect_gap_families']}) · U1 채운 계열 {s['gap_filled_families']} |",
         f"| 확인 조건 아님(B8 · 원문 보관) | {s['not_condition_claims']} {s['not_condition_by_kind']} |",
         f"| 경과표 · PIH | {s['timelines']} · {s['pih']} |",
         f"| 근거 | 문헌 {s['evidence']['literature']} · 문장 {s['evidence']['statements']} · 웹 {s['evidence']['web']} · 가이드 · 표기 {s['evidence']['guides']} |",
         f"| 조건부(한정어 · 단위 시술 미특정 · 기본 적용 제외) | 주장 {s['scope_conditional']['claims']} · 피함 {s['scope_conditional']['avoid_edges']} · 조건 {s['scope_conditional']['condition_claims']} |",
         f"| 하위 조건별 값(by_sub_condition — 겉 칸 비움) | {s['by_sub_condition']} |",
         f"| 웹 근거 종류 | " + ' · '.join(f'{k} {v}' for k, v in s['web_evidence'].items()) + ' |',
         f"| 속성(쌍 아님) | {s['attrs']} |",
         f"| 원천 질문 · 원천 수정 후보 | {s['origin_questions']} · {s['source_fix_candidates']} |",
         f"| 전수 — 8단계 칸 · 원천 행 | {s['coverage_fields']} · {s['source_rows']} |",
         f"| **open** · 낡은 결정 | **{s['open']}** · {s['stale_decisions']} |", '']
    cr = s['conflict_resolution']
    L += ['## 충돌 하나로(10-30)', '', '| 항목 | 셈 |', '|---|---|',
          f"| 계열 쌍 충돌 X8 처분 | {cr['x8']} (묶음 끝점으로 새로 드러난 쌍 {cr['x8_from_bundle_new']} · 기존 쌍에 묶음 몫 더함 {cr['x8_with_bundle_sides']}) |",
          f"| **가짜 충돌 해제(R1) · 보수 선택(R3 · R4 + 등급 R2 + 대기 R6) · 진짜 반대 → 의료진(R5)** | **{cr['fake_released']} · {cr['conservative']} · {cr['staff_true_opposition']}** |",
          f"| 등급 충돌 → 더 엄격 · 대기 기간 → 더 긴 쪽 | {cr['grade_conflicts_conservative']} · {cr['wait_conflicts_conservative']} |",
          f"| 엣지 resolved 상태 · 표시 | {cr['edges_by_status']} · {cr['edges_by_review_status']} |",
          f"| 엣지 규칙 쓰임 · 하위 조건으로 나뉜 엣지 · 방향별 같은 날 값이 갈리는 엣지(by_direction) | {cr['edges_rules']} · {cr['edges_by_sub_condition']} · {cr['edges_by_direction_split']} |",
          f"| 주장 표시 | {cr['claims_by_review_status']} |",
          f"| 단위 시술 쌍 전수 · 형제 엣지 겹쳐 쌍으로 접음 · **두 값 나가는 쌍** | {cr['unit_pairs_checked']} · {cr['resolved_pairs']} {cr['resolved_pairs_by_status']} · **{cr['two_value_unit_pairs']}** |",
          f"| 확인 조건 등급 표(대상 키 × 조건) · 그중 R2 · 단위 시술 키로 접음 | {cr['condition_resolved']} · {cr['condition_resolved_conservative']} · {cr['condition_resolved_unit_fold']} |",
          f"| 대기 기간 표 · 질문 내림 | {cr['wait_resolved']} · {', '.join(cr['origin_questions_retired'])} |", '',
          '규칙(결정 `conflict_resolution.rules`):', ''] + [f"- **{r['id']} {r['name']}** — {r['text']}" for r in o['conflict_resolution_rules']] + ['',
          '| X8 | 쌍 | 종류 | 처분 | 규칙 | 걸린 엣지 · 쌍 |', '|---|---|---|---|---|---|']
    L += [f"| {x['id']} | {' ↔ '.join(x['pair'])} | {x['type']}{' (묶음)' if x.get('from_bundle') else ''} | {x['resolution']['status']} | {x['resolution']['rule']} | {', '.join(x['resolution']['where'][:6])}{' …' if len(x['resolution']['where']) > 6 else ''} |" for x in o['conflicts']]
    L += ['', '| 대기 기간 | 조건 | 값 | 규칙 |', '|---|---|---|---|']
    L += [f"| {w['id']} | {w['what']} | " + (' / '.join(f"{list(op_['sub_condition'].values())[0]}: {op_['months']}개월" for op_ in w['options']) if w['by_sub_condition'] else f"{w['months']}개월") + f" | {' · '.join(w['rules']) or '하나'} |" for w in o['conditions']['wait_resolved']]
    L += ['']
    L += ['## 조사 판 대비(항목별 이유)', '', '| 항목 | 조사 | 지금 | 이유 |', '|---|---|---|---|']
    L += [f"| `{x['item']}` | {x['research'] if x['item'] != 'claim_kinds' else '(json)'} | {x['now'] if x['item'] != 'claim_kinds' else '(json)'} | {x['reason']} |" for x in o['research_diff']]
    L += ['']
    L += ['## 관계 주장', '', '| id | 원천 | 종류 | A | B | first | days | same_day | 표시 | 규칙 | 충돌 처분 |', '|---|---|---|---|---|---|---|---|---|---|---|']

    def eps(e):
        if e['level'] == '복합(나눔)':
            return ' + '.join(eps(p) for p in e['parts'])
        u = ','.join(e['units'][:4]) + ('…' if len(e['units']) > 4 else '')
        return f"{e.get('text')}→{e['level']}:{u or ','.join(e['families'])}"
    for c in o['claims']:
        iv = c.get('interval') or {}
        L.append(f"| {c['id']} | `{c['source']}`[{c['source_index']}] | {c['kind']} | {eps(c['a'])} | {eps(c['b'])} | {iv.get('first') or ''} | {iv.get('days') or ''}{'+' if iv.get('open_high') else ''} | "
                 f"{'' if iv.get('same_day') is None else iv.get('same_day')} | {' · '.join(iv.get('marks') or [])} | {c.get('rule')} | {c.get('review_label') or ''} |")
    L += ['', '## 충돌(원문 쪽별 · 처분은 위 「충돌 하나로」)', '', '| id | 쌍 | 종류 | 쪽별 | 처분 |', '|---|---|---|---|---|']
    for x in o['conflicts']:
        L.append(f"| {x['id']} | {' ↔ '.join(x['pair'])} | {x['type']} | " + ' / '.join(f"{k}: {v if isinstance(v, str) else ', '.join(v)}" for k, v in x['sides'].items())
                 + (' / 묶음 ' + ' / '.join(f"{k}: {', '.join(v)}" for k, v in x['sides_from_bundle'].items()) if x.get('sides_from_bundle') else '') + f" | {x['resolution']['status']} |")
    L += ['', '## 피함(고민 조건 금기 · U8-2)', '', '| id | 고민(7단계) | → 시술 | 수식 | 범위 | 원문 | 근거 |', '|---|---|---|---|---|---|---|']
    for a in o['avoid_edges']:
        L.append(f"| {a['id']} | {', '.join(a['from_concerns'])} | {eps(a['to'])} | {a['qualifier'] or ''} | {a.get('scope') or '기본 적용'} | {a['text']} | {a['concern_basis']} |")
    cnd = o['conditions']
    L += ['', '## 확인 조건 노드', '', '| id | 이름 | 주장 | 원천 |', '|---|---|---|---|']
    L += [f"| {n['id']} | {n['name']} | {n['n_claims']} | {' · '.join(n['sources'])} |" for n in cnd['nodes']]
    L += ['', f"등급 충돌 {len(cnd['grade_conflicts'])}(전부 R2 더 엄격 — conditions.resolved) · 대기 기간 충돌(R6 — conditions.wait_resolved) " + ' · '.join(f"{w['id']} " + ' / '.join(f'{k}: {v}' for k, v in w['by_source'].items()) for w in cnd['wait_conflicts']), '']
    sf = o['safety']
    L += ['## 안전', '', f"합병증 {len(sf['complications'])} · 원천 없는 계열(gap — 「없음 = 안전」 아님) {', '.join(sf['complication_gap_families'])} · 같은 이름 여러 계열 {sf['complication_names_multi_family']}", '',
          f"부작용 {len(sf['side_effects'])}(계열 속성 — {sf['side_effect_rule']}) · 부작용 없는 계열 {', '.join(sf['side_effect_gap_families'])}", '',
          '| 부작용 | 계열 | 이름 | 원천 등급 | 의료진 질문 |', '|---|---|---|---|---|'] + [f"| {x['id']} | {x['family']} | {x['name']} | {x['severity_site']} | {x.get('staff_question') or ''} |" for x in sf['side_effects']] + ['',
          '| site_caution | 부위 | 위험도 | 그 부위 단위 시술 |', '|---|---|---|---|']
    L += [f"| {x['id']} | {x['site']} | {x['danger_level']} | {len(x['units_affected'])} |" for x in sf['site_caution']]
    L += ['', '| 경과표 | 붙는 곳 | 단위 시술 |', '|---|---|---|'] + [f"| {t['id']} | {t['attach']} | {','.join(t['units'] or [])} |" for t in sf['timelines']]
    L += ['', '## 7단계 메모 대조', '', '| 7단계 메모 원천 | 메모 | 원천 행 | 주장 | 속성 | 조건 | 피함 |', '|---|---|---|---|---|---|---|']
    L += [f"| `{x['note_source']}` | {x['notes']} | {x['source_rows']} | {x['claims']} | {x['attrs']} | {x['conditions']} | {x['avoids']} |" for x in o['step7_reconcile']]
    L += ['', '## 전수 — source-map 8단계 칸', '', '| 원천 · 칸 | 지도 값 수 | 지금 | 반영 |', '|---|---|---|---|']
    L += [f"| `{x['file']}` {x['path']} | {x['n_map']} | {x['n_now']} | {x['handler']} |" for x in o['coverage']]
    L += ['', '## 원천 수정 후보', ''] + [f"- {x['what']} — {x.get('text')} ({x.get('note') or ''}{x.get('claim') or x.get('evidence')})" for x in o['source_fix_candidates']]
    L += ['', '## open', ''] + ([f"- {json.dumps(x, ensure_ascii=False)}" for x in o['open']] or ['없음'])
    L += ['', '## 낡은 결정(stale)', ''] + ([f"- {json.dumps(x, ensure_ascii=False)}" for x in o['stale_decisions']] or ['없음'])
    fx = W / 'step8-fixtures' / 'result.json'
    if fx.exists():
        r = json.load(open(fx))
        L += ['', f"## 고정 시험 {r['passed']}/{r['total']}", ''] + [f"- {'PASS' if c['pass'] else 'FAIL'} {c['id']} — {c['note']}" for c in r['cases']]
    open(OUT / 'step8-relations.md', 'w').write('\n'.join(L) + '\n')
    Q = ['# 8단계 원천 질문', '', '규칙(사전 · 패턴)으로 하나로 안 정해지는 것만. 충돌은 10-30 부터 진짜 반대(R5 순서 반대)만 — 등급(R2) · 대기(R6) · 간격(R3) · 같은 날(R4) · 조건 분리(R1)는 규칙으로 정함. 답이 오면 결정 파일 그 줄만 고치고 `step8-apply.py` 재실행.', '',
         '| id | 받는 사람 | 질문 | 걸린 행 |', '|---|---|---|---|']
    Q += [f"| {q['id']} | {q['to']} | {q['q']} | {', '.join(q['refs'][:12])}{' …' if len(q['refs']) > 12 else ''} ({len(q['refs'])}) |" for q in o['origin_questions']]
    Q += ['', '## 내린 질문(10-30 충돌 하나로 — 규칙으로 정함 · id 는 다시 안 씀)', '', '| id | 질문 | 처분 |', '|---|---|---|']
    Q += [f"| {q['id']} | {q['q']} | {q['resolution']} |" for q in o['origin_questions_retired']]
    open(OUT / 'step8-origin-questions.md', 'w').write('\n'.join(Q) + '\n')


if __name__ == '__main__':
    main()
