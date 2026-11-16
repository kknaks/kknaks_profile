#!/usr/bin/env python3
"""시맨틱 사전 고정 시험(품질 수정 10-30) — 원인 F · G · H · M · L 마다 1건 이상. semantic.json 을 읽기만 한다.

찾기(resolve)는 semantic.json dictionary.resolve_rules 만 보고 짠다(문서 = 코드 · 품질 M) — 완전 → 낱말 나눔 → 끝말 → 접두(대상 계열 · 고민 대분류 하나일 때만).
입력: semantic.json · semantic-build.py(RESOLVE_RULES 비교) · 출력: semantic-fixtures/result.json. 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

W = Path(__file__).resolve().parent
SEM = json.load(open(W / 'semantic.json', encoding='utf-8'))
RR = SEM['dictionary']['resolve_rules']
DICT = {e['norm']: e for e in SEM['dictionary']['expressions']}
KEYS = sorted(DICT)
U5 = {u['id']: u for u in json.load(open(W / 'step5-units.json', encoding='utf-8'))['units']}


def norm(s):
    t = unicodedata.normalize('NFKC', str(s or ''))
    t = unicodedata.normalize('NFC', ''.join(ch for ch in unicodedata.normalize('NFKD', t) if not unicodedata.combining(ch)))
    for a, b in RR['fold'].items():
        t = t.replace(a, b)
    t = re.sub(r'\s+', '', t)
    t = re.sub('[' + re.escape(RR['strip_chars']) + ']', '', t)
    return t.lower()


def group(tid):
    k, _, v = tid.partition(':')
    if k == 'family':
        return 'family:' + v
    if k == 'unit_procedure' and v in U5:
        return 'family:' + str(U5[v]['key']['family'])
    if k == 'concern':
        m = re.match(r'(P\d+)', v)
        return 'concern:' + (m.group(1) if m else v)
    return tid


def resolve(text):
    q = norm(text)
    if q in DICT:
        return '완전', sorted({t['id'] for t in DICT[q]['targets']})
    toks = [t for t in re.split(RR['split'], text) if t]
    if len(toks) > 1:
        hit = [norm(t) for t in toks if norm(t) in DICT]
        if hit:
            return '낱말', sorted({t['id'] for h in hit for t in DICT[h]['targets']})
    for tl in RR['tails']:
        if q.endswith(tl) and len(q) - len(tl) >= 2 and q[:-len(tl)] in DICT:
            return '끝말', sorted({t['id'] for t in DICT[q[:-len(tl)]]['targets']})
    if len(q) >= RR['prefix_min']:
        tg = sorted({t['id'] for k in KEYS if k.startswith(q) for t in DICT[k]['targets']})
        if tg:
            return ('접두', tg) if len({group(t) for t in tg}) == 1 else ('접두 거절(대상 여럿)', [])
    return '없음', []


def has(text, tid):
    return tid in resolve(text)[1]


SRC = (W / 'semantic-build.py').read_text(encoding='utf-8')
m_ = re.search(r'RESOLVE_RULES = dict\((.*?)\)\n\n\ndef norm', SRC, re.S)
CODE_RULES = eval('dict(' + m_.group(1) + ')') if m_ else None  # 빌드 코드의 규칙 표 그대로(문서와 같은지)

CASES = [
    ('M1', 'M', '문서 = 코드 — semantic.json resolve_rules = semantic-build.py RESOLVE_RULES', lambda: CODE_RULES == RR),
    ('M2', 'M', '악센트 접기 — 「Juvéderm」 = 「juvederm」', lambda: norm('Juvéderm') == 'juvederm'),
    ('M3', 'M', '사전 행 norm = 정규화(expr) 전부', lambda: all(e['norm'] == norm(e['expr']) for e in SEM['dictionary']['expressions'])),
    ('F1', 'F', '원장 이름(값) 「하이드로퀴논」 → family:M15', lambda: has('하이드로퀴논', 'family:M15')),
    ('F2', 'F', '원장 이름(단위 시술) 「V라인주사」 → unit_procedure:U5-070', lambda: has('V라인주사', 'unit_procedure:U5-070')),
    ('F3', 'F', '고민 갈래 이름 「주사치료」(노드 아님) → concern:P13', lambda: has('주사치료', 'concern:P13')),
    ('F4', 'F', '환자용 이름 「콜라겐 재생 주사」 → family:M3', lambda: has('콜라겐 재생 주사', 'family:M3')),
    ('F5', 'F', '원천 CC 「케미컬필링」 → concern:P6-2(CC 앵커)', lambda: has('케미컬필링', 'concern:P6-2')),
    ('G1', 'G', '접두 — 대상 계열 · 고민 대분류가 여럿이면 거절(「리프」 → 리프팅 M9 · M7 · 목적)', lambda: resolve('리프')[0] == '접두 거절(대상 여럿)'),
    ('G2', 'G', '접두 — 하나로 모이면 씀(「쥬비」 → 쥬비덤 제품 M2)', lambda: resolve('쥬비')[0] == '접두' and {group(t) for t in resolve('쥬비')[1]} == {'family:M2'} or resolve('쥬비')[1] == ['product:M2-2-1']),
    ('H1', 'H', '입력 접기 — 「볼쳐짐/불독살」 = 「볼처짐/불독살」', lambda: norm('볼쳐짐/불독살') == norm('볼처짐/불독살') and resolve('볼쳐짐/불독살')[1] != []),
    ('H2', 'H', '괄호 지움 — 「코그 Cog」 = 「코그(Cog)」', lambda: resolve('코그 Cog') == resolve('코그(Cog)') and resolve('코그(Cog)')[1] != []),
    ('H3', 'H', '끝말 떼기 — 「쿨스컬프팅시술」 → 「쿨스컬프팅」 대상', lambda: resolve('쿨스컬프팅시술')[0] == '끝말' and resolve('쿨스컬프팅시술')[1] == resolve('쿨스컬프팅')[1]),
    ('L1', 'L', '「모든 시술」 → scope:모든 시술(와일드카드 · 노드 아님)', lambda: resolve('모든 시술')[1] == ['scope:모든 시술']),
    ('L2', 'L', '쌍 이름 「HA 필러」 · 「RF/HIFU」 · 「CO2 프락셔널」 찾음', lambda: all(resolve(t)[1] for t in ('HA 필러', 'RF/HIFU', 'CO2 프락셔널'))),
]

results = []
for cid, cause, what, fn in CASES:
    try:
        ok = bool(fn())
        err = None
    except Exception as e:  # 시험 자체가 깨지면 FAIL
        ok, err = False, repr(e)[:200]
    results.append(dict(id=cid, cause=cause, what=what, pass_=ok, error=err))
    print(('PASS' if ok else 'FAIL'), cid, what, err or '')
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
(W / 'semantic-fixtures').mkdir(exist_ok=True)
json.dump(res, open(W / 'semantic-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
