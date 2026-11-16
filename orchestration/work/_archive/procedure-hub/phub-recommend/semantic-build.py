#!/usr/bin/env python3
"""시맨틱 정본 — 실버 1~8단계 위에 노드 · 엣지 종류 · 용어 · 사전 하나 · id 대응 · 읽는 규칙 · 표시 · 상속 규칙을 한 정본으로.

입력: step1-products · step2-families · step3-sites · step4-techniques · step5-units · step6-packages · step7-concerns · step8-relations(정본 json)
      step7-decisions · step8-decisions(사전 · 규칙 원문) · step3-lexicon(정규화) — 전부 읽기만
출력: semantic.json · semantic.md
결정: 사용자 10-30 「시맨틱 조사 반영 — 추천대로」(B1~B12 · U1~U3 · _RESUME §2) — 조사 semantic-research.json · .md
결정론: 시각 · 무작위 없음 · 모든 목록 정렬 — 두 번 실행해 cmp 같음. 실버 id 는 바꾸지 않는다(정본 id ↔ 실버 id 대응표만 둔다).
셈은 이 파일에 적지 않는다 — 전부 실버 파일에서 센다.
"""
import collections
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

W = Path(__file__).resolve().parent
C_ = collections.Counter
FILES = ['step1-products.json', 'step2-families.json', 'step3-sites.json', 'step4-techniques.json',
         'step5-units.json', 'step6-packages.json', 'step7-concerns.json', 'step8-relations.json']
J = lambda f: json.load(open(W / f, encoding='utf-8'))
S1, S2, S3, S4, S5, S6, S7, S8 = [J(f) for f in FILES]
D7, D8, L3 = J('step7-decisions.json'), J('step8-decisions.json'), J('step3-lexicon.json')
S9 = J('step9-explanations.json')  # 9단계 설명 사실(11-01 · D9-7 값 사전 · 속성 — 노드 · 엣지 종류는 늘지 않음)
CC, SF, EV, CN = S7['concerns'], S8['safety'], S8['evidence'], S8['conditions']
OPEN = []


def op(t, **kw):
    OPEN.append(dict(type=t, **kw))


def cnt(it):
    return dict(sorted(C_(it).items(), key=lambda kv: str(kv[0])))


def idpat(ids):
    return cnt(re.sub(r'\d+', '9', re.sub(r'[가-힣]+', '가', str(i))) for i in ids)


# 사전 정규화 · 찾기 규칙(품질 M · H · G — 10-30) — 문서(semantic.json dictionary.resolve_rules) = 이 코드. 측정 · 골드 resolve 는 이 칸을 읽는다
RESOLVE_RULES = dict(
    normalize=['NFKC', '라틴 악센트 접기(NFKD 결합 부호 제거 · NFC)', '입력 접기 fold(「쳐짐」 → 「처짐」 — 10-27 원천 수정 결정과 같은 방향 · 사전 · 질의 양쪽)', '공백 제거', '괄호 ( ) [ ] 지움(안 글자는 남김 — 「코그(Cog)」 = 「코그 Cog」)', '전부 소문자'],
    fold={'쳐짐': '처짐'},
    strip_chars='()[]',
    split=r'[\s/·,()\[\]+]+',
    order=['완전(정규화 뒤 같음)', '낱말 나눔(split 으로 나눠 낱말마다 완전)', '끝말 떼기(tails — 질의 끝 「주사 · 시술」을 떼고 완전)', '접두(질의 2자 이상이 사전 표현 앞부분 · 대상 계열 · 고민 대분류가 하나로 모일 때만 — 여럿이면 못 찾음)'],
    tails=['주사', '시술'],
    prefix_min=2,
    prefix_rule='대상의 계열(제품 · 단위 시술 · 계열 · 패키지 → 계열 코드) · 고민 대분류(P{n}) · 부위 · 목적을 모아 하나일 때만 접두 일치를 쓴다(품질 G — 다른 계열 · 고민으로 찾는 것 막음)',
    note='3단계 lexicon normalize 문구(「영문으로 시작하면 소문자」)는 3단계 매칭 설명 — 사전은 이 규칙 하나(품질 M)')


def norm(s):
    """사전 정규화 — RESOLVE_RULES.normalize 그대로(문서 = 코드)."""
    t = unicodedata.normalize('NFKC', str(s))
    t = unicodedata.normalize('NFC', ''.join(ch for ch in unicodedata.normalize('NFKD', t) if not unicodedata.combining(ch)))
    for a, b in RESOLVE_RULES['fold'].items():
        t = t.replace(a, b)
    t = re.sub(r'\s+', '', t)
    t = re.sub('[' + re.escape(RESOLVE_RULES['strip_chars']) + ']', '', t)
    return t.lower()


# ───────── 0. 실버 개체 ─────────
act = [i for i in S1['items'] if i.get('active')]
units = S5['units']
special = S5['rules']['special_sites']
con_cat = [c for c in CC['categories'] if c.get('node')]
con_sub = [c for c in CC['subcategories'] if c.get('node')]
con_item = [c for c in CC['items'] if c.get('kind') == '고민']
con_extra = CC['extra_items']
con_all = con_cat + con_sub + con_item + con_extra
pur_nodes = [p for p in S7['purposes'] if p.get('node')]
cx = SF['complications']
ses = SF['side_effects']
stmts = EV['statements']
evs = EV['literature'] + EV['web'] + EV['guides']

# ───────── 1. id 규칙(B6) — 정본 id = {종류}:{안정 키} · 실버 id 는 그대로 ─────────
PURPOSE_ID = {p['name']: f'PU-{i + 1:02d}' for i, p in enumerate(pur_nodes)}  # 실버 purposes[] 순서(결정 J4 순서) 그대로
KINDS = [
    # (정본 종류, 실버 목록, 실버 id 칸, 정본 키 함수, id 규칙 설명)
    ('product', act, 'ledger_id', lambda x: x['ledger_id'], '원장 ledger_id 그대로(원천 추적) — 꼴이 여럿이라 접두로만 구분'),
    ('family', S2['families'], 'id', lambda x: x['id'], 'M{n} · N{n} 그대로'),
    ('site', S3['nodes'], 'id', lambda x: x['id'], 'site.{영문} 그대로'),
    ('technique', S4['nodes'], 'id', lambda x: x['id'], 'K{nn}[a-c] 그대로'),
    ('unit_procedure', units, 'id', lambda x: x['id'], 'U5-{nnn} 그대로'),
    ('package', S6['packages'], 'id', lambda x: x['id'], 'P6-{nn} 그대로'),
    ('concern', con_all, 'id', lambda x: re.sub(r'^(J\d+)-.*$', r'\1', x['id']), 'P{n} · P{n}-{n} · auto-{n}-{ts} 그대로 · 결정 노드 J{n}-{한글} → J{n}(이름은 name 칸)'),
    ('purpose', pur_nodes, 'name', lambda x: PURPOSE_ID[x['name']], '실버는 id 없음(이름 · 「목적:{이름}」 문자열) → PU-{nn}(purposes[] 순서)'),
    ('combo', S7['combos'], 'id', lambda x: x['id'], 'RC-… 그대로'),
    ('check_condition', CN['nodes'], 'id', lambda x: x['id'], 'C-{약어} 그대로'),
    ('complication', cx, 'id', lambda x: x['id'], 'CX-{계열}-{원천 번호} · U1 원문 serious = CX-{계열}-T{n}'),
    ('evidence_statement', stmts, 'id', lambda x: x['id'], 'ST-{계열}-{field}-{nn} 그대로'),
    ('evidence_source', evs, 'id', lambda x: x['id'], 'EV-LIT · EV-WEB · EV-GD 그대로'),
]
ID_MAP = []          # 정본 id ↔ 실버 id
CANON = {}           # (종류, 실버 id) → 정본 id
SILVER_FORMS = {}    # 실버 안 문자열 꼴 → 정본 id
for kind, rows, fld, key, _ in KINDS:
    seen = set()
    for x in rows:
        sid = x[fld]
        cid = f'{kind}:{key(x)}'
        if cid in seen:
            op('정본 id 겹침', kind=kind, id=cid)
        seen.add(cid)
        CANON[(kind, sid)] = cid
        ID_MAP.append({'canonical': cid, 'kind': kind, 'silver_id': sid, 'name': x.get('name') or (x.get('2_names') or {}).get('display_name') or x.get('label') or x.get('title') or x.get('concern') or x.get('source_label') or x.get('statement', '')[:60] or x.get('url')})
for p in pur_nodes:
    SILVER_FORMS['목적:' + p['name']] = CANON[('purpose', p['name'])]
for p in S7['purposes']:  # 고민에 붙은 목적 이름(R6) — 실버 엣지가 「목적:{이름}」으로 부르면 그 고민
    if not p.get('node') and p.get('same_as_concern') and ('concern', p['same_as_concern']) in CANON:
        SILVER_FORMS['목적:' + p['name']] = CANON[('concern', p['same_as_concern'])]
for p in S7['purposes']:  # 목적 별칭(aliases[].text)으로 부르는 「목적:{별칭}」(엣지 purpose_nodes 와 같은 대상)
    tgt = SILVER_FORMS.get('목적:' + p['name'])
    for a in p.get('aliases') or []:
        if tgt and ('목적:' + a['text']) not in SILVER_FORMS:
            SILVER_FORMS['목적:' + a['text']] = tgt
STRING_FORMS = [
    dict(form="family:{계열}", where='step8 edges[].a|b · conditions.claims[].target · safety.timelines[].attach', to='family:{계열}', note="「family:M9#HIFU」 꼴은 endpoints.a|b.qualifier(B3)"),
    dict(form="units:{U5,…}", where='step8 edges[].a|b', to='unit_procedure:{U5} 하나 · 둘 이상이면 endpoints.candidates[](B3 — 노드 아님)', note=''),
    dict(form="bundle:{M|M}", where='step8 edges[].a|b', to='endpoints.candidates[] 계열', note=''),
    dict(form="all · 「모든 시술(공통)」", where='step8 edges · conditions.claims[].target', to='대상 「모든 시술」(노드 아님)', note=''),
    dict(form="ledger:{원장 id} · product:{원장 id}", where='step8 conditions.claims[].target', to='product:{원장 id}', note='행선지 없는 원장 항목이면 대상 없음 표시'),
    dict(form="unit:{U5}", where='step8 safety.timelines[].attach · pih', to='unit_procedure:{U5}', note=''),
    dict(form="목적:{이름}", where='step7 edges[].from · from_concerns · correspondence[].target', to='purpose:PU-{nn} · 고민에 붙은 목적은 concern:{P}', note='purpose_nodes[] 는 「:」 없는 이름'),
    dict(form="J{n}-{한글}", where='step7 concerns.extra_items[].id · edges[].from_concerns', to='concern:J{n}', note=''),
]
for e in S7['edges']:  # 실버 「목적:」 문자열이 다 풀리는지
    for f in [e['from']] + (e.get('from_concerns') or []):
        if f.startswith('목적:') and f not in SILVER_FORMS:
            op('「목적:」 문자열이 목적 · 고민에 안 풀림', text=f)


# 고민 트리 항목 중 노드가 아닌 것(시술 이름 항목 · 부위 · 목적 갈래 · P1 쁘띠시술 메뉴) → 가장 가까운 고민 노드(그 항목 엣지가 나가는 곳) + qualifier
TREE_PARENT = {c['id']: c.get('parent') for c in CC['subcategories']}
TREE_PARENT.update({c['id']: c.get('subcategory') or c.get('category') for c in CC['items']})
TREE_IDS = {c['id'] for k in ('categories', 'subcategories', 'items') for c in CC[k]}


def tree_anchor(cid):
    x = TREE_PARENT.get(cid)
    while x:
        if ('concern', x) in CANON:
            return x
        x = TREE_PARENT.get(x)
    return None


def canon_target(kind, sid):
    return CANON.get((kind, sid))


# ───────── 2. 노드 종류 13 ─────────
NODES = [
    dict(kind='product', name='제품', internal='product', meaning='허가 · 업체 · 규격을 가진 제품 · 장비(라인이면 상위 제품) — 시술에 「쓰는 것」',
         required=['ledger_id', '2_names.display_name', '4_license.status', '4_license.recommendable', 'active'], optional=['2_names.search_names[]', '1_identity.kind', '4_license.licenses[] · history[]', '5_spec', '6_companies', 'line', 'evidence', 'open'],
         canon='step1-products.json', path='items[] (active)', count=len(act), detail=f"items {len(S1['items'])} 중 active {len(act)} · 추천 {sum(1 for i in act if i['4_license']['recommendable'])}"),
    dict(kind='family', name='계열', internal='family', meaning='무엇을 — 공식 일반명 약제 · 장비 계열(문헌 M1~M17 + 늘린 N1~N10)',
         required=['id', 'name', 'definition', 'name_status'], optional=['synonyms[]', 'literature_name', 'literature_evidence[]', 'sub_families[]', 'new_family'],
         canon='step2-families.json', path='families[]', count=len(S2['families']), detail=f"새 계열 {sum(1 for f in S2['families'] if f.get('new_family'))}"),
    dict(kind='site', name='부위', internal='site', meaning='어디에 — 몸 겉에서 가리킬 수 있는 자리(일반인 이름 + 전문의 이름)',
         required=['id', 'name', 'parent', 'status'], optional=['synonyms[]', 'anatomical_name', 'danger_zone', 'compound_strings[]'],
         canon='step3-sites.json', path='nodes[]', count=len(S3['nodes']), detail=f"최상위 영역 {sum(1 for n in S3['nodes'] if not n.get('parent'))}"),
    dict(kind='technique', name='기법', internal='technique', meaning='어떻게 — 큰 기법 + 세부 기법',
         required=['id', 'name', 'level', 'parent'], optional=['medical_name', 'family_default[]', 'source_expressions[]'],
         canon='step4-techniques.json', path='nodes[]', count=len(S4['nodes']), detail=json.dumps(cnt(n['level'] for n in S4['nodes']), ensure_ascii=False)),
    dict(kind='unit_procedure', name='단위 시술', internal='unit_procedure', meaning='제일 작은 단위 행위 = 계열 × [하위 · 성분] × 부위 × 기법(원천에 있는 조합만)',
         required=['id', 'key{family,sub_family,ingredient,site,technique}', 'name', 'site_basis'], optional=['synonyms[]', 'candidate_of[]', 'uses_product[]', 'market[]', 'route_status', 'ops', 'step4_attrs', 'pih_not_applicable'],
         canon='step5-units.json', path='units[]', count=len(units), detail=f"특수 부위(노드 없음) {sum(1 for u in units if u['key']['site'] in special)}"),
    dict(kind='package', name='패키지', internal='package', meaning='이름 있는 단위 시술 묶음(일반 · 회차 · 병원 시그니처)',
         required=['id', 'name', 'kind', 'recommendable'], optional=['shape', 'synonyms[]', 'price[]', 'same_day_raw', 'detail_raw'],
         canon='step6-packages.json', path='packages[]', count=len(S6['packages']), detail=json.dumps(cnt(p['kind'] for p in S6['packages']), ensure_ascii=False)),
    dict(kind='concern', name='고민', internal='concern', meaning='상태 이름 — taxonomy problem 「고민」 갈래 3층 + 결정 노드',
         required=['id', 'name'], optional=['sites[]', 'parent', 'related[]', 'kind', 'en', 'basis'],
         canon='step7-concerns.json', path='concerns.categories[node] · subcategories[node] · items[kind=고민] · extra_items[]', count=len(con_all),
         detail=f"대분류 {len(con_cat)} · 중분류 {len(con_sub)} · 항목 {len(con_item)} · 결정 노드 {len(con_extra)}"),
    dict(kind='purpose', name='목적', internal='purpose', meaning='시술이 하는 일 — 고민과 같은 말이면 노드 없이 그 고민에 붙음(R6)',
         required=['name', 'kind'], optional=['aliases[]', 'from[]'], canon='step7-concerns.json', path='purposes[] (node)', count=len(pur_nodes),
         detail=f"고민에 붙은 목적 이름 {sum(1 for p in S7['purposes'] if p.get('same_as_concern'))}"),
    dict(kind='combo', name='추천 조합(사이트 「추천 패키지」)', internal='recommend_combo', meaning='원천이 고민 · 목적별로 적은 시술 조합(원천별 · 합치지 않음)',
         required=['id', 'kind', 'source', 'name', 'anchor'], optional=['components[]', 'tier', 'price', 'effect', 'sales_copy'], canon='step7-concerns.json', path='combos[]', count=len(S7['combos']),
         detail=json.dumps(cnt(c['kind'] for c in S7['combos']), ensure_ascii=False)),
    dict(kind='check_condition', name='확인 조건', internal='check_condition', meaning='사람 쪽 조건(임신 · 약물 · 체질 …)',
         required=['id', 'name', 'match_pattern'], optional=['n_claims', 'sources[]'], canon='step8-relations.json', path='conditions.nodes[]', count=len(CN['nodes']), detail=''),
    dict(kind='complication', name='합병증', internal='complication', meaning='예상 밖 이상 결과(혈관 폐색 · 감염 …) — severity moderate 이상 + U1 원문 serious. 흔한 예상 반응(부작용)은 노드 아님(계열 속성)',
         required=['id', 'name', 'family', 'severity|severity_site'], optional=['incidence', 'onset', 'mechanism', 'management', 'prevention', 'risk_factors', 'evidence[]', 'source'],
         canon='step8-relations.json', path='safety.complications[]', count=len(cx), detail=json.dumps(cnt(x['severity'] or x['severity_site'] for x in cx), ensure_ascii=False)),
    dict(kind='evidence_statement', name='근거 문장', internal='evidence_statement', meaning='계열 단위 문헌 문장(기전 · 효과 · 이상 반응) + 환자용 4개 언어',
         required=['id', 'family', 'field', 'statement', 'evidence[]'], optional=['accuracy_score', 'patient{}', 'class(B2 — 이 정본)'], canon='step8-relations.json', path='evidence.statements[]', count=len(stmts),
         detail=json.dumps(cnt(x['field'] for x in stmts), ensure_ascii=False)),
    dict(kind='evidence_source', name='근거 출처', internal='evidence_source', meaning='문헌 · 웹 · 가이드(원천 출처 문자열)',
         required=['id', 'kind'], optional=['pmid · doi · title · journal · year', 'url · urls[] · multi_url', 'label', 'used_by[]'], canon='step8-relations.json', path='evidence.literature[] · web[] · guides[]', count=len(evs),
         detail=f"문헌 {len(EV['literature'])} · 웹 {len(EV['web'])} · 가이드 {len(EV['guides'])}"),
]
for n, (kind, rows, fld, key, rule) in zip(NODES, KINDS):
    assert n['kind'] == kind
    n['id_rule'] = rule
    n['silver_id_patterns'] = idpat(x[fld] for x in rows)
    n['canonical_id'] = f'{kind}:{{키}}'

ATTRS_NOT_NODES = [
    dict(what='부작용(흔한 예상 반응)', where='step8 safety.side_effects[]', count=len(ses), rule=SF['side_effect_rule'],
         detail=f"원천 {json.dumps(cnt(x['source'].split('(')[0].split('[')[0] for x in ses), ensure_ascii=False)} · 의료진 질문 예외 {sum(1 for x in ses if x.get('staff_question'))} · 부작용 없는 계열 {len(SF['side_effect_gap_families'])}",
         decided='U2 · B1(10-30)'),
    dict(what='끝점 묶음', where='step8 edges[].endpoints.a|b.candidates[]', count=sum(1 for e in S8['edges'] for ep in e['endpoints'].values() if len(ep['candidates']) > 1),
         rule=D8['semantic_apply']['endpoint_candidates'], detail=json.dumps(cnt(ep['kind'] for e in S8['edges'] for ep in e['endpoints'].values()), ensure_ascii=False), decided='U3 · B3(10-30)'),
    dict(what='확인 조건 아닌 문장', where='step8 conditions.not_condition[]', count=len(CN['not_condition']), rule=CN['not_condition_rule'],
         detail=json.dumps(cnt(k['kind'][:12] for k in CN['not_condition']), ensure_ascii=False), decided='B8(10-30)'),
    dict(what='허가 · 업체 · 규격', where='step1 items[].4_license · 6_companies · 5_spec', count=sum(len(i['4_license']['licenses']) for i in act), rule='제품 속성(1단계 「제품 ↔ 허가만」). 업체는 DEC-003 「제조사 원장」 — 노드 세우기는 적재(B9) · 지금 실버엔 업체 id 없음',
         detail='', decided='B9'),
    dict(what='시장가', where='step5 market[] · units[].market[]', count=len(S5['market']), rule='단위 시술 × 제품 × 규격의 원문 가격', detail='', decided='10-27'),
    dict(what='경과 타임라인 · PIH · 운영 속성 · 계열 원문', where='step8 safety.timelines · pih · family_text · step5 units[].ops · pih', count=len(SF['timelines']), rule='붙는 수준(계열 · 하위 · 단위 · 제품)에 속성 — 상속 I8', detail='', decided='G11~G13'),
]

COMBO_FIELDS = ('components', 'members', 'upgrade')  # 추천 조합 구성 칸(7단계 combos) — combo_component 셈(골드 빈틈 ② · 10-30)
# ───────── 3. 엣지 종류 21(B4) ─────────
eps = [ep for e in S8['edges'] for ep in e['endpoints'].values()]
s7_target = cnt(e['target_kind'] for e in S7['edges'])
EDGES = [
    dict(kind='product_family', name='계열 판정', meaning='제품이 어느 계열 제품인가(주 1 + 보조)', frm='product', to='family', directed=True,
         attrs=['role(주 · 보조)', 'sub_family · also_sub_families', 'verdict', 'evidence_level', 'conflict', 'confirm_question'], canon='step2-families.json', path='product_family[].family · also_families[]',
         count=sum(1 for r in S2['product_family'] if r.get('family')) + sum(len(r.get('also_families') or []) for r in S2['product_family']), inherit=False, page=['prod_fam', 'prod_fam_also']),
    dict(kind='key_family', name='단위 시술 키 — 계열', meaning='단위 시술 정체 첫 칸(무엇을)', frm='unit_procedure', to='family', directed=True, attrs=['sub_family', 'ingredient'],
         canon='step5-units.json', path='units[].key.family', count=len(units), inherit=False, page=['unit_fam']),
    dict(kind='key_site', name='단위 시술 키 — 부위', meaning='어디에(특수 부위 「해당 없음」 · 「병변 단위」는 엣지 없음 — 값만)', frm='unit_procedure', to='site', directed=True, attrs=['site_basis'],
         canon='step5-units.json', path='units[].key.site', count=sum(1 for u in units if u['key']['site'] not in special), inherit=False, page=['unit_site']),
    dict(kind='key_technique', name='단위 시술 키 — 기법', meaning='어떻게', frm='unit_procedure', to='technique', directed=True, attrs=['step4_attrs'],
         canon='step5-units.json', path='units[].key.technique', count=sum(1 for u in units if u['key']['technique']), inherit=False, page=['unit_tech']),
    dict(kind='child_of', name='상위', meaning='같은 종류 트리의 상하(부위 · 기법 · 고민)', frm='site · technique · concern', to='같은 종류', directed=True, attrs=[],
         canon='step3-sites.json · step4-techniques.json · step7-concerns.json', path='nodes[].parent · nodes[].parent · subcategories[].parent · items[].subcategory · extra_items[].parent',
         count=sum(1 for n in S3['nodes'] if n.get('parent')) + sum(1 for n in S4['nodes'] if n.get('parent')) + sum(1 for c in con_sub if c.get('parent')) + len(con_item) + sum(1 for c in con_extra if c.get('parent')),
         inherit=False, page=['site_parent', 'tech_parent', 'con_parent(상위)']),
    dict(kind='concern_related', name='관련 고민', meaning='상위 없는 결정 노드가 걸친 고민(J10 피부결)', frm='concern', to='concern', directed=False, attrs=[],
         canon='step7-concerns.json', path='concerns.extra_items[].related[]', count=sum(len(c.get('related') or []) for c in con_extra), inherit=False, page=['con_parent(관련)']),
    dict(kind='family_technique', name='계열 기법', meaning='계열 기본 기법 · 함께 쓰는 기법', frm='family', to='technique', directed=True, attrs=['role(기본 · 함께)', 'default_layer'],
         canon='step4-techniques.json', path='family_defaults[].default · also[]', count=sum(1 for r in S4['family_defaults'] if r.get('default')) + sum(len(r.get('also') or []) for r in S4['family_defaults']),
         inherit=False, page=['fam_tech', 'fam_tech_also']),
    dict(kind='uses_product', name='쓰는 제품(저장)', meaning='원천 이름이 제품을 부를 때만 저장', frm='unit_procedure', to='product', directed=True, attrs=['basis'],
         canon='step5-units.json', path='units[].uses_product[]', count=sum(len(u.get('uses_product') or []) for u in units), inherit=False, page=['unit_prod']),
    dict(kind='contains', name='패키지 구성', meaning='패키지가 담은 단위 시술(확정 · 슬롯 후보)', frm='package', to='unit_procedure', directed=True, attrs=['order', 'status(확정 · 슬롯 후보)', 'quantity_raw', 'sessions', 'evidence_level', 'origin_question'],
         canon='step6-packages.json', path='contains[] · slots[].candidates[]', count=len(S6['contains']) + sum(len(s.get('candidates') or []) for s in S6['slots']), inherit=False, page=['pkg_unit', 'pkg_slot']),
    dict(kind='treats', name='추천(고민 · 목적 → 시술)', meaning='원천 구조가 고민 · 목적에 적은 시술', frm='concern · purpose', to='unit_procedure · family', directed=True,
         attrs=['source', 'target_kind', 'lowering', 'resolve_flag', 'site_check', 'concern_region_check', 'severity', 'basis'], canon='step7-concerns.json', path='edges[]',
         count=len(S7['edges']), inherit=True, page=['con_unit', 'con_fam'], detail=json.dumps(s7_target, ensure_ascii=False)),
    dict(kind='concern_site', name='고민 부위', meaning='부위가 붙은 고민의 부위', frm='concern', to='site', directed=True, attrs=[],
         canon='step7-concerns.json', path='concerns.*.sites[]', count=sum(len(c.get('sites') or []) for c in con_all), inherit=False, page=['con_site']),
    dict(kind='anchors_combo', name='추천 조합 앵커', meaning='추천 조합이 걸린 고민', frm='concern', to='combo', directed=True, attrs=['kind'],
         canon='step7-concerns.json', path='combos[].anchor.concern · concerns', count=sum(len((c.get('anchor') or {}).get('concerns') or ([c['anchor']['concern']] if isinstance((c.get('anchor') or {}).get('concern'), str) else ((c.get('anchor') or {}).get('concern') or []))) for c in S7['combos']),
         inherit=False, page=['con_combo']),
    dict(kind='combo_component', name='조합 구성', meaning='추천 조합의 구성 시술 — 구성 칸 components(구성) · members(비교 대상) · upgrade(연령 플랜 업그레이드)(골드 빈틈 ② · 사용자 10-30)', frm='combo', to='unit_procedure', directed=True, attrs=['field(구성 칸 이름 그대로)', 'order', 'status', 'flag'],
         canon='step7-concerns.json', path='combos[].components|members|upgrade[].units[]', count=sum(len(x.get('units') or []) for c in S7['combos'] for f_ in COMBO_FIELDS for x in c.get(f_) or []), inherit=False, page=['combo_unit'],
         detail=' · '.join(f"{f_} {sum(len(x.get('units') or []) for c in S7['combos'] for x in c.get(f_) or [])}" for f_ in COMBO_FIELDS)),
    dict(kind='procedure_relation', name='시술 ↔ 시술 관계', meaning='시너지 · 순서 · 간격 · 같은 날 · 대체 · 금기 — 쌍 하나에 엣지 하나 · 주장 칸', frm='unit_procedure · family · 묶음(candidates)', to='같음', directed='주장마다',
         attrs=['endpoints.a|b{kind,id,qualifier,candidates[]}', 'claims[]{kind, interval{days,first,same_day,open_high,by_sub_condition,options}, level_site, reason, evidence_kind, gate_status, review_status}', 'conditional_claims', 'review_status'],
         canon='step8-relations.json', path='edges[] · claims[]', count=len(S8['edges']), inherit=True, page=['rel', 'rel_fam'], detail=f"주장 {len(S8['claims'])} · 끝점 {json.dumps(cnt(ep['kind'] for ep in eps), ensure_ascii=False)}"),
    dict(kind='concern_avoid', name='피함(금기 조합)', meaning='고민 조건 금기', frm='concern', to='unit_procedure · family', directed=True, attrs=['qualifier', 'scope', 'default_apply', 'grade_original'],
         canon='step8-relations.json', path='avoid_edges[]', count=len(S8['avoid_edges']), inherit=True, page=['avoid', 'avoid_fam']),
    dict(kind='requires_check', name='확인 조건', meaning='시술 → 사람 조건 · 등급(금기 · 주의 · 확인만)', frm='family · product · unit_procedure · 모든 시술', to='check_condition', directed=True,
         attrs=['grade_original', 'grade3', 'kind', 'where', 'strength_original', 'scope_conditional'], canon='step8-relations.json', path='conditions.claims[] (B8 — not_condition 뺌)',
         count=sum(len(k['conditions']) or 0 for k in CN['claims']), inherit=True, page=['cond', 'cond_fam'], detail=f"주장 {len(CN['claims'])} · 등급 {json.dumps(cnt(k['grade3'] for k in CN['claims']), ensure_ascii=False)}"),
    dict(kind='has_complication', name='합병증', meaning='계열 → 합병증(중대 반응만 — B1)', frm='family', to='complication', directed=True, attrs=['severity_site'],
         canon='step8-relations.json', path='safety.complications[].family', count=len(cx), inherit=True, page=['fam_cx']),
    dict(kind='site_caution', name='위험지대 주의', meaning='부위 × 계열 위험지대', frm='site', to='family', directed=True, attrs=['zone', 'danger_level', 'vessels', 'nerves', 'safe_injection_depth', 'units_affected'],
         canon='step8-relations.json', path='safety.site_caution[]', count=len(SF['site_caution']), inherit=True, page=['site_caution']),
    dict(kind='has_statement', name='근거 문장', meaning='계열 → 근거 문장', frm='family', to='evidence_statement', directed=True, attrs=['field', 'class(B2)'],
         canon='step8-relations.json', path='evidence.statements[].family', count=len(stmts), inherit=True, page=['fam_stmt']),
    dict(kind='cites', name='출처', meaning='근거 문장 · 합병증이 기댄 출처(관계 주장 출처는 주장 칸 claims[].evidence)', frm='evidence_statement · complication', to='evidence_source', directed=True, attrs=[],
         canon='step8-relations.json', path='evidence.statements[].evidence[] · safety.complications[].evidence[]',
         count=sum(len(x.get('evidence') or []) for x in stmts) + sum(len(x.get('evidence') or []) for x in cx), inherit=False, page=['stmt_ev', 'cx_ev', 'ev_claim']),
    dict(kind='line_item', name='라인 품목', meaning='라인(상위 제품) → 품목(하위 제품) — 결정 10-27 ④', frm='product', to='product', directed=True, attrs=['decision'],
         canon='step1-products.json', path='lines{}.items[] (ledger_id 있는 것)', count=sum(1 for v in S1['lines'].values() for it in v.get('items') or [] if it.get('ledger_id')),
         inherit=False, page=[], detail=f"라인 {len(S1['lines'])} · 품목 칸 {sum(len(v.get('items') or []) for v in S1['lines'].values())}(허가번호만 있는 품목은 엣지 아님 — 라인 속성)"),
]
NOT_EDGES = [
    dict(page='prod_unit_inh', why='상속 후보 = 상속 I4 계산 결과 — 저장 안 함(B7 · 골드)'),
    dict(page='set_member', why='끝점 묶음 = endpoints.candidates[] 칸(U3 · B3)'),
]

# ───────── 4. 용어집 47 ─────────
GLOSS = [
    ('단위 시술', '제일 작은 단위 행위 = 무엇을(계열) × 어디에(부위) × 어떻게(기법). 키 = 계열 × [하위 · 성분(J1 안 C)] × 부위 × 기법 · 원천에 있는 조합만', '_RESUME §2 10-27 · 10-29 「5단계 시작」 · 로그 step5 §3-1'),
    ('계열', '무엇을 — 공식 일반명 약제 · 장비 계열. 기준 = 교과서 · 임상 · 학회 문헌. 계열이 없으면 시술을 빼지 않고 계열을 늘림(N1~N10)', '_RESUME §2 10-27 · 10-28 · 10-29'),
    ('하위 계열', '계열 안 매질 · 재료 축 · 주 1 + 보조. 단위 시술 키에는 「무엇을」을 바꾸는 계열만(M5 · M8 · M9 · M13 · M16 성분)', '_RESUME §2 10-28 · 로그 step5 §3-1'),
    ('기법', '어떻게 — 큰 기법 + 세부 기법(K01~K13). 층 · 깊이 · 대상 근육 · 도구는 단위 시술 속성 · 펄스 · 박피 · 방식은 장비 속성', '_RESUME §2 10-28 J1 안 1'),
    ('계열 기본 기법', '계열이 따로 말하지 않을 때 쓰는 기법(default) · 함께 쓰는 기법(also)', 'step4 family_defaults'),
    ('부위', '몸 겉에서 가리킬 수 있는 자리. 쪼개는 규칙 = ① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다. 뼈 · 근육 · 혈관 · 층은 부위 아님', '_RESUME §2 10-27 · 10-28'),
    ('부위 이름(일반인)', '노드 이름 = 상담 용어', '_RESUME §2 10-28 「부위 노드 이름 2벌」'),
    ('부위 이름(전문의)', 'anatomical_name — 같은 겉자리의 의학 이름만', '_RESUME §2 10-28'),
    ('묶음 부위', '하위를 묶는 부위 노드 — 동의어 없음 · 단위 시술 키를 만들지 않음 · 부위 올라가기(R21)에서 통과', '로그 step5 §3-2 · step7 site_rules.climb'),
    ('최상위 영역', '3단계 트리에서 부모 없는 노드(얼굴 · 목(묶음) · 두피 · 바디 …) — 부위 올라가기 · 고민 영역의 경계', 'step7-decisions site_rules.climb.regions · R21 · R22'),
    ('특수 부위 「해당 없음」 · 「병변 단위」', '해당 없음 = 전신 투여 · 병변 단위 = 병변 수 · 면적으로 매기는 시술. 부위 노드 없음 · 영역 검사 밖', 'step5 rules.special_sites'),
    ('기본값 부위', '부위 이름 없는 얼굴 계열 항목 = 얼굴 전체 + site_basis 「기본값」 표시(J2)', '로그 step5 §3-4'),
    ('제품', '허가 · 업체 · 규격을 가진 제품 · 장비. 이름 3칸(대표 한글 1 · 허가 이름은 허가 쪽에만 · 검색 이름[])', '_RESUME §2 10-27'),
    ('라인 · 품목', '라인 = 상위 제품 · 개별 품목 = 하위 제품', '_RESUME §2 10-27 ④'),
    ('허가 상태', '정상 · 허가번호 미확인(추천 포함) · 확인 불가 · 미허가 · 허가 취소(이력) · 허가 대상 아님(출처 있을 때만)', '_RESUME §2 10-27 · 10-28'),
    ('장비 이름 = 시술 동의어', '장비 이름이 시술 이름으로 쓰이면 장비 노드는 두고 그 이름을 단위 시술 동의어로도', '_RESUME §2 10-27'),
    ('패키지', '이름 있는 단위 시술 묶음 — 일반 · 회차 · 병원 시그니처(추천 기본 제외). 구성은 원천에 적힌 만큼', '로그 step6 §3'),
    ('슬롯', '패키지 구성 중 못 푼 자리 — 후보 전부 + 원천 질문', '로그 step6 §3-2'),
    ('추천 조합', '원천이 고민 · 목적별로 적은 시술 조합(원천별 · 합치지 않음) — 사이트 「추천 패키지」', '_RESUME §2 10-28 U3 · 10-29'),
    ('영업 문구', 'salesPitch · upsellHook — 보관 · 기본 응답 제외', 'step7 rules R9'),
    ('고민', '상태 이름 — taxonomy problem 「고민」 갈래 + 결정 노드(J8 · J10 · J14)', '로그 step7 §3-1'),
    ('목적', '시술이 하는 일 — 고민과 같은 말이면 그 고민에 붙음(R6)', 'step7 rules R6'),
    ('중증도', '고민의 정도 — 하위 고민이 있으면 하위로(주름) · 없으면 상위 + severity', 'step7 rules R18'),
    ('고민 영역', '고민(과 하위 고민 · 항목)의 앵커 부위들의 최상위 영역 합집합 — 앵커 부위 없는 엣지 · 조합 구성의 영역 밖 단위 시술을 뺌(목적 갈래 중분류는 안 넣음)', 'step7 rules R22 · site_rules.concern_region · 사용자 10-30'),
    ('확인 조건', '사람 쪽 조건 원장 · 시술 → 조건 엣지에 등급', '_RESUME §2 10-28 · 로그 step8 §3-10'),
    ('등급 3분류', '금기 · 주의 · 확인만(+ 확인만(고지)) — 원문 등급은 그대로 두고 덧붙임', 'step8-decisions labels.grade3'),
    ('조건 아닌 문장', '상담 · 시술 준비 · 고지 · 효과 · 근거 수준 문장 — 확인 조건 엣지가 아니라 원문 보관(계열 대상은 계열 원문 속성)', 'step8 conditions.not_condition_rule · B8'),
    ('피함(금기 조합)', '고민 조건 금기 = 고민 → 단위 시술 엣지(concern_avoid)', 'step8-decisions U8-2'),
    ('관계 주장', '시술↔시술 엣지 안에 쌓는 원천 주장 한 줄', '로그 step8 §3-1'),
    ('시너지 · 순서 · 간격 · 금기', '시술↔시술 엣지 하나의 주장 종류 — 「대신」은 대체(택 1)', '_RESUME §2 10-26 · 로그 step8 §3-2'),
    ('간격', 'days [하한, 상한](일) · first(a|b|null) · same_day · open_high — 추천 · AI 는 edges[].resolved 의 이 칸만 읽음(10-30 · 원문 claims[].interval 은 근거)', 'step8 reading_contract'),
    ('합병증', '예상 밖 이상 결과(혈관 폐색 · 감염 …) — complications.json severity moderate 이상 + U1 원문 serious · 원천 없는 계열은 gap', '사용자 10-29 · U1 · U2 · B1(10-30)'),
    ('부작용', '흔한 예상 반응(멍 · 부기 · 홍반 …) — 계열 속성(safety.side_effects) · 제품 × 계열 · 단위 시술 값이 있으면 덮어씀(골드 계산)', '사용자 10-29 · U2 · B1(10-30) · step8 side_effect_rule'),
    ('위험지대', '부위 × 계열의 혈관 · 신경 · 안전 층 위험 — 위험지대 주의 엣지 속성', '로그 step8 §3-11'),
    ('필수 고지', '원문 그대로 보관(쪼개지 않음) · 계열 원문 속성', '_RESUME §2 10-28'),
    ('근거 문장', '계열 단위 문헌 문장 · field(moa · effects · adverse_effects) + class(B2 · 이 정본)', 'step8 evidence.statements · B2'),
    ('근거 출처', '문헌 · 웹 · 가이드. URL 없는 출처 문자열 = 웹 아님 · 「;」 URL 여럿 = multi_url', 'step8-decisions web_evidence_rule'),
    ('근거 강도', '원문 등급만(숫자를 만들지 않음)', '로그 step8 §3-12'),
    ('근거 약 · 중', '판정 근거가 약하면 값을 넣고 「약」 + 확인 질문(open 아님)', '_RESUME §2 10-28'),
    ('충돌', '원천끼리 다른 말 — 10-30 부터 하나로: 조건 다르면 나눔(R1 · 방향 포함) · 등급 더 엄격(R2) · 간격 더 긴 쪽(R3) · 같은 날 불가(R4) · 순서 반대만 순서 단정 안 함 + 의료진(R5) · 대기 더 긴 쪽(R6) · 원문은 alternatives', 'step8-decisions conflict_resolution · user_decisions 「충돌(10-30)」(D-13b 바꿈)'),
    ('조건부(단위 시술 미특정)', '한정어 붙은 끝점이 묶음으로 열림 → default_apply false · 기본 상속 · 응답에서 뺌', 'step8-decisions scope_rule'),
    ('하위 조건별 값', '겉 칸을 비우고 options[].sub_condition 별 값을 읽음', 'step8 F2 · reading_contract'),
    ('gap', '원천이 없어 비운 것 — 「없음 = 안전」 아님(합병증 gap 계열 · PIH gap · 이 부위 단위 시술 없음)', '로그 step8 §6 · step5 pih_gap_units'),
    ('끝점 묶음', '끝점이 하나로 안 좁혀진 것 — 노드가 아니라 엣지 endpoints.candidates[]', 'U3 · B3(10-30)'),
    ('후보 전부', '이름이 여럿을 가리키면 고르지 않고 후보 전부 + 표시 — 외부 LLM 이 고르거나 되묻기', '_RESUME §2 10-27 W-1'),
    ('부위로 내림 · 올라가기', '부위가 있으면 그 부위(또는 하위)의 단위 시술 · 없으면 R21 상위 노드 자신으로 올라가며(영역 경계 안 · 영역 「전체」 노드까지) · 그래도 없으면 계열만 + 「이 부위 단위 시술 없음」', 'step7 rules R21 · site_rules.climb'),
    ('원천 질문', '규칙으로 하나로 안 정해지는 것만 병원 · 의료진 · 원장님에게 — 값은 추천값 · 답 오면 그 행만', 'step8 U8-1 · _RESUME §2 10-29'),
]
GLOSSARY = [dict(term=t, definition=d, source=s) for t, d, s in GLOSS]

# ───────── 5. 사전 하나(B5) ─────────
TG = collections.defaultdict(lambda: {'targets': {}, 'sources': set(), 'raw': set()})


def put(text, kind, sid, qualifier=None, reason='', source=''):
    if not text:
        return
    if kind == 'scope':  # 「모든 시술」 = 범위(노드 아님 · G16 와일드카드) — 사전 대상은 scope:모든 시술
        cid = 'scope:모든 시술'
    else:
        cid = canon_target(kind, sid) if kind != 'none' else ('none:고민 노드 아님(트리 항목)' if (qualifier or {}).get('taxonomy_entry') else 'none:시술 아님')
    if cid is None:
        op('사전 대상이 정본에 없음', text=text, kind=kind, id=sid, source=source)
        return
    e = TG[norm(text)]
    k = cid + (('#' + json.dumps(qualifier, ensure_ascii=False, sort_keys=True)) if qualifier else '')
    t = e['targets'].setdefault(k, {'id': cid, 'qualifier': qualifier or None, 'reasons': set()})
    t['reasons'].add(reason)
    e['sources'].add(source)
    e['raw'].add(text)


for it in act:
    put(it['2_names']['display_name'], 'product', it['ledger_id'], reason='대표 이름', source='step1 items[].2_names.display_name')
    for s in it['2_names'].get('search_names') or []:
        put(s['name'], 'product', it['ledger_id'], reason='검색 이름', source='step1 items[].2_names.search_names[]')
for f in S2['families']:
    put(f['name'], 'family', f['id'], reason='이름', source='step2 families[].name')
    for s in f.get('synonyms') or []:
        put(s, 'family', f['id'], reason='동의어', source='step2 families[].synonyms[]')
for n in S3['nodes']:
    put(n['name'], 'site', n['id'], reason='이름', source='step3 nodes[].name')
    for s in n.get('synonyms') or []:
        put(s['text'], 'site', n['id'], reason='동의어 · ' + s['type'], source='step3 nodes[].synonyms[]')
for n in S4['nodes']:
    put(n['name'], 'technique', n['id'], reason='이름', source='step4 nodes[].name')
    if n.get('medical_name'):
        put(n['medical_name'], 'technique', n['id'], reason='의학 이름', source='step4 nodes[].medical_name')
for u in units:
    put(u['name'], 'unit_procedure', u['id'], reason='이름', source='step5 units[].name')
    for s in u.get('synonyms') or []:
        put(s['text'], 'unit_procedure', u['id'], reason=s['type'] + (' · 모호' if s.get('ambiguous') else ''), source='step5 units[].synonyms[]')
for x in S5['device_name_synonyms']:
    for uid in x['units']:
        put(x['name'], 'unit_procedure', uid, reason='장비 · 제품 이름 = 시술 동의어(10-27)', source='step5 device_name_synonyms[]')
for p in S6['packages']:
    put(p['name'], 'package', p['id'], reason='이름', source='step6 packages[].name')
    for s in p.get('synonyms') or []:
        put(s['text'], 'package', p['id'], reason='동의어', source='step6 packages[].synonyms[]')
for c in con_cat + con_item + con_extra:
    put(c['name'], 'concern', c['id'], reason='이름', source='step7 concerns.*.name')
for c in con_sub:
    put(c.get('concern') or c['source_label'], 'concern', c['id'], reason='이름', source='step7 concerns.subcategories[].concern')
for s in D7['concern_synonyms']:
    for t in s['synonyms']:
        put(t, 'concern', s['id'], reason='고민 동의어(' + s['decided_by'] + ')', source='step7-decisions concern_synonyms[]')
for p in pur_nodes:
    put(p['name'], 'purpose', p['name'], reason='이름', source='step7 purposes[].name')
    for a in p.get('aliases') or []:
        put(a['text'], 'purpose', p['name'], reason='별칭', source='step7 purposes[].aliases[]')


def corr_target(t):
    if t.startswith('목적:'):
        cid = SILVER_FORMS.get(t)
        return ('purpose', t[3:]) if cid and cid.startswith('purpose:') else ('concern', next((p['same_as_concern'] for p in S7['purposes'] if p['name'] == t[3:]), None))
    return ('concern', t)


TREE_ENTRY_TARGETS = []
for r in S7['correspondence']:
    for t in r.get('target') or []:
        k, sid = corr_target(t)
        if k == 'concern' and ('concern', sid) not in CANON and sid in TREE_IDS:
            anc = tree_anchor(sid)
            TREE_ENTRY_TARGETS.append({'text': r['text'], 'entry': sid, 'anchor': anc})
            if anc:
                put(r['text'], 'concern', anc, qualifier={'taxonomy_entry': sid}, reason='고민 대응표 · 노드 아닌 트리 항목 → 상위 고민 노드 · ' + r['match_class'], source='step7 correspondence[]')
            else:
                put(r['text'], 'none', None, qualifier={'taxonomy_entry': sid}, reason='위로 고민 노드 없는 트리 항목(P1 쁘띠시술 메뉴 · 그 항목 · P14 기타 — J5 · J14 메뉴 앵커) — 항목 id 보관', source='step7 correspondence[]')
            continue
        put(r['text'], k, sid, reason='고민 대응표 · ' + r['match_class'], source='step7 correspondence[]')
D8ALIAS = {norm(a['text']): a for a in D8['resolver']['alias']}
F_LEVEL = []
for r in D7['resolver']['fam_kw']:
    a = D8ALIAS.get(norm(r['kw']))
    if a is not None:  # 7 · 8단계 같은 낱말 — 8단계 수준(계열 + 조건)을 정본으로 · 7단계 단위 시술은 상속 I2 · I3 로 나옴(B5)
        F_LEVEL.append({'text': r['kw'], 'step7': {'families': r.get('families'), 'units': r.get('units')}, 'step8': a['target']})
        continue
    for f in r.get('families') or []:
        put(r['kw'], 'family', f, reason='계열 낱말(7단계 resolver)', source='step7-decisions resolver.fam_kw[]')
    for uid in r.get('units') or []:
        put(r['kw'], 'unit_procedure', uid, reason='시술 낱말(7단계 resolver)', source='step7-decisions resolver.fam_kw[]')
for a in D8['resolver']['alias']:
    t = a['target']
    if t.get('units'):
        for uid in t['units']:
            put(a['text'], 'unit_procedure', uid, reason='이름 풀이(8단계 alias)', source='step8-decisions resolver.alias[]')
    elif t.get('family'):
        q = {k: t[k] for k in ('sub', 'site', 'technique', 'note') if t.get(k)}
        put(a['text'], 'family', t['family'], qualifier=q or None, reason='이름 풀이(8단계 alias)', source='step8-decisions resolver.alias[]')
    elif t.get('wildcard'):
        put(a['text'], 'scope', None, reason='와일드카드(8단계 alias · G16 — 전역 행)', source='step8-decisions resolver.alias[]')
    else:
        put(a['text'], 'none', None, reason='시술 아님(8단계 alias)', source='step8-decisions resolver.alias[]')
for n in CN['nodes']:
    put(n['name'], 'check_condition', n['id'], reason='이름', source='step8 conditions.nodes[].name')

# 원천 이름 칸 사전 출처(품질 F · 10-30) — 원천에 있는 이름이 사전에 없어 못 찾던 것. 대상은 실버가 이미 정한 자리만(새 판정 없음)
SRC_DIR = Path(D7['source']['path'])
B_PE = json.load(open(SRC_DIR / 'patient-education.json', encoding='utf-8'))
LED_DEST = []
for l in S5['ledger']:  # ① 원장 이름(5단계 ledger) → 행선지: 단위 시술 · 제품 · (없으면) 원천 계열 + 행선지 표시
    q = {'ledger': l['id'], 'dest': l['dest']}
    if l.get('units'):
        for uid in l['units']:
            put(l['name'], 'unit_procedure', uid, qualifier=q, reason='원장 이름 → 5단계 행선지 단위 시술', source='step5 ledger[].name')
    elif l.get('product') and ('product', l['product']) in CANON:
        put(l['name'], 'product', l['product'], qualifier=q, reason='원장 이름 → 5단계 행선지 제품', source='step5 ledger[].name')
    elif l.get('source_family') and ('family', l['source_family']) in CANON:
        put(l['name'], 'family', l['source_family'], qualifier=dict(q, to=l.get('to')), reason='원장 이름 · 행선지가 단위 시술 · 제품 아님(값 · 다른 단계 · 시술 아님) → 원천 계열 + 행선지 표시', source='step5 ledger[].name')
        LED_DEST.append(l['id'])
for m in S5['market']:  # ② 시장가 이름 → 5단계 시장가 행 단위 시술(이름 · 후보)
    for uid in m.get('units') or []:
        put(m['name'], 'unit_procedure', uid, qualifier={'market_role': m.get('role')}, reason='시장가 이름 → 5단계 시장가 행 단위 시술', source='step5 market[].name')
for c in B_PE['categories']:  # ③ 환자용 이름 → 그 계열(원천 categories[].id)
    if ('family', c['id']) in CANON:
        put(c['patient_name'], 'family', c['id'], reason='환자용 이름(patient-education) → 원천 계열', source='patient-education categories[].patient_name')
for e in S7['edges']:  # ④ 원천 CC 이름 → CC 의 고민 앵커(R28 · ③ 엣지 from) + qualifier cc
    if not e['source'].startswith('③') or ('concern', e['from']) not in CANON:
        continue
    for cc in e.get('ccs') or []:
        put(cc, 'concern', e['from'], qualifier={'cc': cc}, reason='원천 CC 이름 → CC 고민 앵커(R28)', source='step7 edges[③].ccs[]')
for c in CC['subcategories']:  # ⑤ 고민 갈래 이름(taxonomy problem subcategories label) → 노드면 그 노드 · 아니면 가장 가까운 고민 노드 + taxonomy_entry
    if ('concern', c['id']) in CANON:
        put(c['source_label'], 'concern', c['id'], reason='고민 갈래 원천 이름', source='step7 concerns.subcategories[].source_label')
    elif tree_anchor(c['id']):
        put(c['source_label'], 'concern', tree_anchor(c['id']), qualifier={'taxonomy_entry': c['id']}, reason='고민 갈래 원천 이름 · 노드 아님(' + (c.get('kind') or '') + ') → 상위 고민 노드', source='step7 concerns.subcategories[].source_label')

F_CONFLICT = []
for x in F_LEVEL:
    s7u, s8 = x['step7'].get('units') or [], x['step8']
    if 'none' in s8 and s7u:
        F_CONFLICT.append(dict(x, verdict='7단계 = 단위 시술 · 8단계 = 시술 아님 — 정본은 8단계(시술 아님) 따르고 7단계 결정 고칠 거리로 보고(이번에 안 바꿈)'))


def ctype(kinds, reasons):
    ks = tuple(sorted(kinds))
    if set(ks) <= {'concern', 'purpose'}:
        return 'A'
    if any('장비 · 제품 이름' in r for r in reasons) or ks == ('product', 'unit_procedure'):
        return 'B'
    if ks == ('family', 'product'):
        return 'C'
    if ks == ('product',):
        return 'D'
    if ks == ('unit_procedure',):
        return 'E'
    if ks == ('site', 'unit_procedure'):
        return 'G'
    if ks == ('technique', 'unit_procedure'):
        return 'H'
    if ks == ('site',):
        return 'I'
    return 'J'


MODE = {'A': ('전부', '묶음 이름 → 고민 · 목적 여럿(R12) — 대상 전부에 적용'),
        'B': ('후보', '장비 · 제품 이름 = 단위 시술 동의어(10-27) — 제품 · 시술 후보 전부 + 모호'),
        'C': ('후보', '브랜드 이름이 계열 낱말로도 — 「보톡스」 = 계열 · 제품 둘 다(10-27) · 나머지 같은 처리'),
        'D': ('후보', '같은 검색 이름이 제품 둘(라인 · 같은 허가) — 후보 전부'),
        'E': ('후보', '같은 말이 단위 시술 여럿 — 후보 전부(모호 표시)'),
        'G': ('후보', '부위 이름 = 단위 시술 원장 이름(「사각턱」 …) — 부위 · 시술 후보'),
        'H': ('후보', '기법 이름 = 단위 시술 이름(서브시전 · 펀치 · 압출) — 기법 · 시술 후보'),
        'I': ('전부', '나열 문자열(「볼/관자놀이」)이 부위 둘 — 대상 전부'),
        'J': ('후보', '종류가 다른 노드끼리(고민 · 계열 · 목적 · 부위 · 시술) — 후보 전부 · 고민 이름이 시술 동의어 칸에 든 것은 7단계 W3 교훈대로 고민 우선 표시')}
DICT = []
for k in sorted(TG):
    e = TG[k]
    tg = [dict(id=t['id'], qualifier=t['qualifier'], reasons=sorted(t['reasons'])) for _, t in sorted(e['targets'].items())]
    ids = sorted({t['id'] for t in tg})
    row = {'expr': sorted(e['raw'])[0], 'norm': k, 'variants': sorted(e['raw']), 'targets': tg, 'sources': sorted(e['sources'])}
    if len(ids) > 1:
        kinds = {i.split(':')[0] for i in ids}
        c = ctype(kinds, [r for t in tg for r in t['reasons']])
        row.update(collision=c, mode=MODE[c][0], ambiguous=MODE[c][0] == '후보')
        if c == 'J' and 'concern' in kinds and 'unit_procedure' in kinds:
            row['prefer'] = 'concern'
    else:
        row.update(collision=None, mode='하나', ambiguous=False)
    DICT.append(row)
f_rows = {norm(x['text']) for x in F_LEVEL}
for row in DICT:
    if row['norm'] in f_rows:
        row['level_merged'] = 'F — 7 · 8단계 수준 차이를 8단계(계열 + qualifier)로 합침 · 단위 시술은 상속 I2 · I3'
coll = [r for r in DICT if r['collision']]
DICT_SUMMARY = dict(expressions=len(DICT), targets=sum(len(r['targets']) for r in DICT), collisions=len(coll),
                    collisions_by_class={c: dict(n=n, mode=MODE[c][0], how=MODE[c][1]) for c, n in sorted(C_(r['collision'] for r in coll).items())},
                    level_merged_F=len(F_LEVEL), conflict_reported=F_CONFLICT,
                    tree_entries=dict(n=len(TREE_ENTRY_TARGETS), to_anchor=sum(1 for x in TREE_ENTRY_TARGETS if x['anchor']), no_anchor=sorted({x['entry'] for x in TREE_ENTRY_TARGETS if not x['anchor']}),
                                      rule='고민 대응표가 노드 아닌 taxonomy 항목(시술 이름 · 부위 · 목적 갈래)을 가리키면 가장 가까운 고민 노드 + qualifier.taxonomy_entry · 위로 노드가 없으면(P1 쁘띠시술 · P14 기타 — J5 · J14) none:고민 노드 아님(트리 항목) + 항목 id'),
                    research_collisions_note='조사(semantic-research)의 겹침 147 은 F 갈래 21 을 겹침으로 셌음 — 정본은 F 를 qualifier 로 합쳐 겹침에서 빠짐 · 셈은 이 파일에서 다시 셈',
                    by_source=cnt(s for r in DICT for s in r['sources']), normalize=' → '.join(RESOLVE_RULES['normalize']), normalize_step3_text=L3['normalize'])
INTERPRET_RULES = dict(
    note='이름 → 노드가 아니라 원문 → 칸 규칙(사전 행이 아님)',
    concern_rules={k: D7['concern_rules'][k] for k in ['split_separators', 'tails', 'state_tails', 'lead_words', 'anti_prefix', 'purpose_verb_tails', 'severity_words']},
    concern_rule_ids=[r['id'] for r in D7['rules'] if re.match(r'R1[2-9]|R2[0-2]', r['id'])],
    step8_resolver={k: D8['resolver'][k] for k in ['strip_prefix', 'tail_words', 'tail_regex', 'cut_regex', 'bundle_paren_rule']},
    step3_lexicon=dict(patterns=len(L3['entries']), normalize=L3['normalize']),
    interval_lexicon='§ reading.interval_lexicon', sentence_patterns=len(D8['sentence']['patterns']), condition_patterns=len(D8['conditions']))

# ───────── 6. 근거 문장 종류(B2 — 조사 분류 · 추천대로) ─────────
ST_CLASS_TABLE = {
    '부작용(흔한 예상 반응)': ['ST-M5-adverse_effects-01', 'ST-M7-adverse_effects-02', 'ST-M7-adverse_effects-04', 'ST-M8-adverse_effects-02', 'ST-M8-adverse_effects-03', 'ST-M8-adverse_effects-04', 'ST-M12-adverse_effects-05', 'ST-M15-adverse_effects-01', 'ST-M15-adverse_effects-02'],
    '색소 반응(PIH)': ['ST-M8-adverse_effects-01', 'ST-M8-adverse_effects-05', 'ST-M12-adverse_effects-01', 'ST-M12-adverse_effects-04'],
    '드문 · 중대 반응(합병증 성격)': ['ST-M1-adverse_effects-01', 'ST-M1-adverse_effects-02', 'ST-M1-adverse_effects-03', 'ST-M2-adverse_effects-03', 'ST-M4-adverse_effects-02', 'ST-M5-adverse_effects-02', 'ST-M12-adverse_effects-02', 'ST-M16-adverse_effects-01', 'ST-M17-adverse_effects-01'],
    '안전성 총평': ['ST-M2-adverse_effects-01', 'ST-M7-adverse_effects-01', 'ST-M7-adverse_effects-03', 'ST-M7-adverse_effects-05', 'ST-M7-adverse_effects-06', 'ST-M12-adverse_effects-03'],
    '기전 · 효과 한계(이상 반응 칸)': ['ST-M1-adverse_effects-04', 'ST-M2-adverse_effects-02', 'ST-M3-adverse_effects-01', 'ST-M4-adverse_effects-01'],
    '효과(기전 칸)': ['ST-M2-moa-02', 'ST-M8-moa-03', 'ST-M8-moa-08'],
    '적응증(기전 칸)': ['ST-M15-moa-03', 'ST-M15-moa-04'],
    '안전성 비교(기전 칸)': ['ST-M15-moa-05'],
    '근거 수준 · 규제(효과 칸)': ['ST-M16-effects-01', 'ST-M16-effects-02'],
}
ST_IDS = {x['id']: x for x in stmts}
ST_CLASS = {}
for c, ids in ST_CLASS_TABLE.items():
    for i in ids:
        if i not in ST_IDS:
            op('근거 문장 분류표 id 가 실버에 없음', id=i)
        ST_CLASS[i] = c
for i, x in ST_IDS.items():
    ST_CLASS.setdefault(i, {'moa': '기전', 'effects': '효과', 'adverse_effects': None}[x['field']])
    if ST_CLASS[i] is None:
        op('이상 반응 칸 근거 문장이 분류표에 없음(B2)', id=i)
STATEMENTS = dict(total=len(stmts), by_field=cnt(x['field'] for x in stmts), by_class=cnt(ST_CLASS.values()),
                  table=[{'statement': CANON[('evidence_statement', i)], 'field': ST_IDS[i]['field'], 'class': ST_CLASS[i]} for i in sorted(ST_IDS)],
                  source_fix=sorted(i for i, c in ST_CLASS.items() if '칸)' in c),
                  rule='field(원천 칸)는 그대로 · class 는 이 정본(B2). 칸과 뜻이 다른 문장 = 원천 수정 후보')

# ───────── 7. 읽는 규칙 · 표시 12 · gate_status 3값 ─────────
iv = lambda c: c.get('interval') or {}
FLAGS = [
    ('conflict', '충돌 처분(보수적 선택 · 의료진 확인)', ['step8 claims[] · edges[].review_status=conservative|staff_check · review_label', 'edges[].resolved · resolved_pairs[]', 'conflicts[].resolution', 'conditions.resolved · wait_resolved', 'step2 product_family[].conflict'],
     sum(1 for c in S8['claims'] if c['review_status'] in ('conservative', 'staff_check')), '앱엔 resolved 하나(10-30) — 보수적 선택은 값 하나 + 원문 alternatives · 의료진 확인(순서 반대)은 순서 단정 안 함 + 원천 질문'),
    ('conditional', '조건부(단위 시술 미특정)', ['claims[].a|b.default_apply=false', 'avoid_edges[].default_apply=false', 'conditions.claims[].scope_conditional'],
     sum(1 for c in S8['claims'] for x in 'ab' if c[x].get('default_apply') is False) + sum(1 for v in S8['avoid_edges'] if v.get('default_apply') is False) + sum(1 for k in CN['claims'] if k.get('scope_conditional')),
     '기본 응답 · 계열 상속에서 뺌(조회 옵션으로만)'),
    ('candidates', '후보 여럿', ['edges[].endpoints.*.candidates[](2 이상)', 'units[].synonyms[].ambiguous', 'units[].candidate_of', 'step7 edges[].resolve_flag=ambiguous', 'step6 slots[]', '사전 mode 후보'],
     sum(1 for ep in eps if len(ep['candidates']) > 1) + sum(1 for e in S7['edges'] if 'ambiguous' in (e.get('resolve_flag') or '')) + len(S6['slots']), '고르지 않고 후보 전부 · 외부 LLM 이 고르거나 되묻기'),
    ('weak', '근거 약', ['evidence_level 약 · 중', 'step3 synonyms[].weak', 'anatomical_name.level 약'],
     sum(1 for r in S2['product_family'] if r.get('evidence_level') == '약') + sum(1 for u in units if u.get('evidence_level') in ('약', '중')) + sum(1 for c in S6['contains'] if c.get('evidence_level') == '약'),
     '값은 쓰되 약함 표시'),
    ('question', '원천 질문(병원 · 의료진 · 원장님)', ['origin_question · staff_question · doctor_questions · pending_director · confirm_question · origin_questions[]'],
     len(S8['origin_questions']) + len(S7['origin_questions']) + len(S6['origin_questions']) + len(S5['origin_questions']) + len(S5['staff_questions']) + len(S3['doctor_questions']) + len(S2['pending_director']),
     '추천값으로 쓰되 표시 · 답 오면 그 행만'),
    ('not_recommended', '추천 제외', ['step1 4_license.recommendable=false', 'step6 recommendable=false', 'combos sales_copy.default_response=false'],
     sum(1 for i in act if not i['4_license']['recommendable']) + sum(1 for p in S6['packages'] if not p['recommendable']), '기본 응답에서 뺌 · 노드는 남김'),
    ('gap', 'gap(원천 없음)', ['safety.complication_gap_families', 'safety.side_effect_gap_families', 'step5 pih_gap_units', 'step7 resolve_flag=no_unit_at_site'],
     len(SF['complication_gap_families']) + len(S5['pih_gap_units']) + sum(1 for e in S7['edges'] if 'no_unit_at_site' in (e.get('resolve_flag') or '')), '「없음 = 안전」 아님'),
    ('default_value', '기본값(규칙으로 채움)', ['step5 units[].site_basis 기본값', 'route_status 허가 용법 미확인', 'family_defaults'],
     sum(1 for u in units if '기본값' in (u.get('site_basis') or '')) + sum(1 for u in units if (u.get('route_status') or '').startswith('허가 용법 미확인')), '원천 값과 구분해 표시'),
    ('unresolved', '못 풂', ['step7 resolve_flag=unresolved', 'step8 claims[].resolved=false', '끝점 「해석 안 됨」'],
     sum(1 for e in S7['edges'] if 'unresolved' in (e.get('resolve_flag') or '')) + sum(1 for c in S8['claims'] if not c.get('resolved')), '원문 보관 · 끝 없음'),
    ('not_procedure', '시술 아님', ['step7 resolve_flag=not_procedure', 'step8 claims[].not_procedure', '사전 none:시술 아님'],
     sum(1 for e in S7['edges'] if 'not_procedure' in (e.get('resolve_flag') or '')) + sum(1 for c in S8['claims'] if c.get('not_procedure')), '엣지 끝 아님'),
    ('by_sub_condition', '하위 조건별 값', ['claims[].interval.by_sub_condition · options[]'], sum(1 for c in S8['claims'] if iv(c).get('by_sub_condition')), '겉 칸이 비면 options[].sub_condition 별로'),
    ('license_unconfirmed', '허가번호 미확인', ['step1 4_license.status'], sum(1 for i in act if i['4_license']['status'] == '허가번호 미확인'), '추천 포함 · 표시'),
]
FLAG_LIST = [dict(flag=f, ko=k, fields=fs, count=n, read=r) for f, k, fs, n, r in FLAGS]
GATE = dict(
    values=[dict(value='자동(완전 일치)', meaning='원천 말과 대상 이름이 정규화 뒤 같음'), dict(value='자동(규칙)', meaning='결정 파일의 규칙 · 사전 · 패턴으로 결정론'),
            dict(value='결정', meaning='사람이 정한 값 — decided_by 에 사용자 결정 id(_RESUME §2)')],
    rule='모든 노드 · 엣지 · 주장 공통 3값. 「미확인」은 상태가 아니라 표시(question · weak · gap). 실버 칸 → 값: gate_status 칸이 있으면 그대로(7단계 correspondence · 8단계 claims) · 없으면 decided_by 가 사용자 결정 id 면 「결정」 · 나머지 「자동(규칙)」',
    now={'step7 correspondence': cnt(r['gate_status'] for r in S7['correspondence']), 'step8 claims': cnt(c['gate_status'] for c in S8['claims']),
         'step5 units decided_by 있음': sum(1 for u in units if u.get('decided_by'))},
    decided='B12(10-30)')
READING = dict(
    reading_contract=S8['reading_contract'],
    interval_fields={'days': '[하한, 상한](일)', 'open_high': '위로 열림(이상)', 'first': 'a | b | null(순서 단정 안 함)', 'same_day': 'true · false · null', 'by_sub_condition': '겉 칸 비움 → options[]', 'options[]': 'sub_condition 별 days · same_day · first(+ 조건 모름 = 전부 접음)', 'by_direction': '먼저 하는 쪽별 same_day(a | b)', 'marks[]': '원문 낱말 갈래 표시', 'text': '원문(보관만)', 'resolved': '10-30 — 앱이 읽는 칸(edges[].resolved · resolved_pairs[].resolved)'},
    interval_lexicon=[dict(id=b['id'], pattern=b['pattern'], set=b['set'], note=b['note']) for b in D8['interval_lexicon']['branches']],
    units_days=D8['interval_lexicon']['units_days'],
    scope_rule=D8['scope_rule'], labels=D8['labels'],
    endpoints='엣지 끝 = endpoints.a|b{kind, id, qualifier, candidates[]} — kind 「단위 시술」 · 「계열」 · 「계열 + 조건」 은 id 하나 · 「단위 시술 후보」 · 「계열 묶음」 · 「계열 후보」 는 candidates[] 전부(후보 표시) · 「모든 시술」(B3)',
    side_effects=SF['side_effect_rule'],
    not_condition=CN['not_condition_rule'],
    default_response=['recommendable false · active false · 시그니처 · 영업 문구(default_response false) · default_apply false 는 기본 응답에서 뺌', '충돌은 resolved 하나(순서 반대는 순서 단정 안 함 + 의료진) · 후보는 전부 · gap 은 「정보 없음」으로'],
    counts=dict(claims=len(S8['claims']), with_interval=sum(1 for c in S8['claims'] if c.get('interval')), days=sum(1 for c in S8['claims'] if iv(c).get('days')),
                first=cnt(str(iv(c).get('first')) for c in S8['claims']), same_day=cnt(str(iv(c).get('same_day')) for c in S8['claims'])),
    flags=FLAG_LIST, gate_status=GATE)

# ───────── 8. 상속 규칙 9(B7 — 저장 안 함 · 골드 계산) ─────────
climb = D7['site_rules']['climb']
creg = D7['site_rules']['concern_region']
lv8 = cnt(c[x]['level'] for c in S8['claims'] for x in 'ab')
INHERIT = [
    dict(id='I1', name='계열 → 단위 시술', rule='계열 끝 엣지(관계 · 피함 · 확인 조건 · 합병증 · 근거 문장 · 위험지대 · 추천 계열만)는 key.family 가 그 계열인 단위 시술 전부에. default_apply false 는 상속 안 함',
         fields=['step5 units[].key.family', "step8 edges[].endpoints kind 계열", 'conditions.claims[].target_level 계열', 'step7 edges[].target_kind 계열만'],
         count=dict(relation_family_endpoints=lv8.get('계열', 0), condition_family_claims=sum(1 for k in CN['claims'] if k['target_level'] == '계열'), treats_family_only=s7_target.get('계열만', 0)),
         stored_now='safety.complications[].units_inherit(합병증만 미리 펼침) — 정본은 계산(B7) · 칸은 실버에 남아도 골드는 다시 셈'),
    dict(id='I2', name='하위 계열', rule='하위 끝(qualifier.sub_family)은 key.sub_family 같은 단위 시술로 · 키에 그 하위 없는 계열은 계열(+조건) 후보 전부 · 하위 원문 보관',
         fields=['edges[].endpoints.*.qualifier.sub_family', 'claims[].a|b.sub_family · flag', 'step8-decisions timeline_attach.units_where', 'step5 rules.product_link.inherit'],
         count=dict(sub_family_endpoints=lv8.get('하위 계열', 0)), stored_now=''),
    dict(id='I3', name='기법 조건', rule='기법 끝(qualifier.technique)은 key.technique 가 그 기법(또는 하위)인 단위 시술로 · 사전 「토닝 = M8 + K04a」 도 이 규칙으로 단위 시술이 나옴(B5)',
         fields=['edges[].endpoints.*.qualifier.technique', 'claims[].a|b.technique', 'conditions.claims[].target.technique', 'step5 rules.product_link.technique_compat'],
         count=dict(technique_endpoints=lv8.get('기법 조건', 0)), stored_now=''),
    dict(id='I4', name='제품 → 단위 시술', rule=S5['rules']['product_link']['inherit'], fields=['step5 units[].uses_product(저장)', 'product_links[].inherited_candidates · technique_excluded · guard', 'rules.product_link'],
         count=dict(link=cnt(p['link'] for p in S5['product_links'])), stored_now='product_links[].inherited_candidates(5단계 계산 기록) — 정본은 계산(B7)'),
    dict(id='I5', name='부위 — 내림 · 올라가기(R21) · 고민 영역(R22)',
         rule='내림: ' + D7['site_rules']['lowering'] + ' · R21: ' + climb['rule'] + ' · 영역: ' + climb['regions'] + ' · 전체 노드: ' + climb['whole_node'] + ' · 없으면: ' + climb['none'] + ' · R22: ' + creg['rule'] + ' · 고민 영역: ' + creg['region'] + ' · 영역 없음: ' + creg['none'],
         fields=['step7-decisions site_rules{lowering, climb, concern_region}', 'step7 edges[].lowering · site_layer · site_check · concern_region_check · concern_region_dropped', 'step3 nodes[].parent'],
         count=dict(site_check=cnt(e.get('site_check') for e in S7['edges']), concern_region_check=cnt(re.sub(r'\d+', 'N', e.get('concern_region_check') or '없음') for e in S7['edges'])), stored_now='7단계가 엣지에 적용해 저장(엣지 값) — 상속 아님'),
    dict(id='I6', name='끝점 묶음', rule='candidates[] 는 원문 이름이 가리킨 후보 전부(OR · 고르지 않음) — 각 후보에 「후보」 표시로 적용 · 계열 묶음은 그 계열 전부 · 모든 시술은 전부',
         fields=['edges[].endpoints.*.candidates[]', 'avoid_edges[].to.units', 'conditions.claims[].target.units'], count=dict(endpoints=cnt(ep['kind'] for ep in eps)), stored_now=''),
    dict(id='I7', name='조건부 제외', rule='default_apply false 는 기본 상속 · 기본 응답에서 뺌', fields=['claims[].a|b.default_apply', 'avoid_edges[].default_apply', 'conditions.claims[].scope_conditional'],
         count=dict(conditional=FLAG_LIST[1]['count']), stored_now=''),
    dict(id='I8', name='안전 · 운영 원문 붙는 수준 · 부작용 덮어쓰기', rule='경과 타임라인 · PIH · 운영 속성 · 부작용은 원천이 가리킨 수준(계열 · 하위 · 단위 · 제품)에 붙고 아래로 상속 · 아래 수준 값(제품 × 계열 · 단위 시술 extracted safety.common)이 있으면 위 값을 덮어씀',
         fields=['step8 safety.timelines[].attach_level', 'step8-decisions timeline_attach', 'step5 pih[].attach', 'step8 safety.pih', 'step5 units[].ops.inherit', 'step8 safety.side_effects[].attach', 'step5 extracted[](safety.common 키)'],
         count=dict(timelines=cnt(x['attach_level'][:12] for x in SF['timelines']), pih=cnt(p['attach'] for p in S5['pih']), side_effects=len(ses),
                    side_effect_override_keys=sum(1 for e in S5['extracted'] if 'safety.common' in e['keys'])), stored_now=''),
    dict(id='I9', name='해당 없음 ≠ gap', rule='PIH 해당 없음 계열은 「해당 없음」 · 원천 없음은 gap · 합병증 원천은 있으나 전부 mild 인 계열은 「중대 반응 없음(원천)」 — 셋을 나눠 표시',
         fields=['step5 rules.pih_not_applicable · pih_not_applicable_units · pih_gap_units', 'step8 safety.complication_gap_families · complication_mild_only_families'],
         count=dict(pih_not_applicable=len(S5['pih_not_applicable_units']), pih_gap=len(S5['pih_gap_units']), complication_gap=len(SF['complication_gap_families']),
                    complication_mild_only=len(SF['complication_mild_only_families']['families'])), stored_now=''),
]

# ───────── 8-1. 9단계 설명 사실 · 값 사전(D9-7 · 11-01) ─────────
ATTRS_NOT_NODES.append(dict(what='설명 사실(9단계)', where='step9 node_slots[] · records[]', count=sum(len(e['emit']) for e in S9['node_slots']),
                            rule='D9-1~D9-9(11-01) — 효과 시작 · 지속 · 작용 원리 · 개요 · 적응증 · 제품 메모 · 대안 · 관련 기법 · 고민 상세 = 붙는 노드(단위 시술 · 제품 · 계열 · 고민)의 속성 원문(section recovery · method · overview · disclosure). 같은 노드 · 같은 칸 충돌은 D9-3(① 긴 쪽 · ② resolved 하나 + alternatives · ③ 둘 다)',
                            detail=json.dumps(S9['summary']['d93'], ensure_ascii=False), decided='D9-1~D9-9(11-01)'))
VALUE_DICT = [dict(dictionary=x['dictionary'], key=x['key'], text=x['text'], source=x['source']['file'] + ':' + x['source']['path']) for x in S9['value_dictionary']]
for x in VALUE_DICT:
    if not x['text'].strip():
        op('값 사전 빈 값', key=x['key'])

# ───────── 9. 저장 ─────────
inputs = {f: dict(version=J(f).get('version'), sha256=hashlib.sha256((W / f).read_bytes()).hexdigest()[:16])
          for f in FILES + ['step7-decisions.json', 'step8-decisions.json', 'step3-lexicon.json', 'step9-explanations.json']}
summary = dict(node_kinds=len(NODES), edge_kinds=len(EDGES), glossary=len(GLOSSARY), flags=len(FLAG_LIST), gate_values=len(GATE['values']), inherit_rules=len(INHERIT),
               dictionary_expressions=DICT_SUMMARY['expressions'], dictionary_targets=DICT_SUMMARY['targets'], dictionary_collisions=DICT_SUMMARY['collisions'],
               id_map=len(ID_MAP), complications=len(cx), side_effects=len(ses), complication_gap_families=len(SF['complication_gap_families']),
               statements_by_class=STATEMENTS['by_class'], value_dictionary=len(VALUE_DICT), explanation_facts=sum(len(e['emit']) for e in S9['node_slots']), open=len(OPEN))
OUT = dict(
    version='semantic-v1', generated_by='semantic-build.py',
    decision_ref='_RESUME.md §2 2026-10-30 「시맨틱 조사 반영 — 추천대로」(B1~B12 · U1~U3) · 조사 semantic-research.json',
    inputs=inputs, summary=summary,
    node_kinds=NODES, attributes_not_nodes=ATTRS_NOT_NODES, edge_kinds=EDGES, not_edges=NOT_EDGES,
    glossary=GLOSSARY,
    dictionary=dict(summary=DICT_SUMMARY, resolve_rules=RESOLVE_RULES, interpret_rules=INTERPRET_RULES, level_merged=F_LEVEL, expressions=DICT),
    ids=dict(rule='정본 id = {종류}:{키} — 실버 id 는 바꾸지 않음(B6). 골드 · 적재는 map 으로 실버 id → 정본 id', kinds=[dict(kind=k, rule=r) for k, _, _, _, r in KINDS],
             string_forms=STRING_FORMS, silver_string_map=dict(sorted(SILVER_FORMS.items())), map=ID_MAP),
    reading=READING, inheritance=INHERIT, statements=STATEMENTS,
    value_dictionary=dict(rule='D9-7(11-01) — 반응 단계 · 중증도 단계 정의 = 값 사전(노드 아님 · B02). 골드 globals 로 나감(다음 허브 발주)', items=VALUE_DICT),
    open=OPEN,
)
js = json.dumps(OUT, ensure_ascii=False, indent=1, default=sorted)
open(W / 'semantic.json', 'w', encoding='utf-8').write(js + '\n')


# ───────── md ─────────
def esc(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def jj(x):
    return esc(json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)


L = ['# 시맨틱 정본 — 노드 · 엣지 · 용어 · 사전 · id · 읽는 규칙 · 표시 · 상속', '',
     f"정본 데이터 `semantic.json`(이 문서는 그 json 에서 만든 것) · 결정론 `semantic-build.py`(실버 파일에서 계산 · 시각 없음) · 결정 {OUT['decision_ref']}", '',
     '입력: ' + ' · '.join(f"`{f}` {v['version']} {v['sha256']}" for f, v in inputs.items()), '',
     '## 0. 요약', '',
     f"노드 종류 **{summary['node_kinds']}** · 엣지 종류 **{summary['edge_kinds']}** · 용어 **{summary['glossary']}** · 표시 **{summary['flags']}** · gate_status **{summary['gate_values']}값** · 상속 규칙 **{summary['inherit_rules']}** · "
     f"사전 표현 **{summary['dictionary_expressions']}**(대상 {summary['dictionary_targets']} · 겹침 {summary['dictionary_collisions']}) · id 대응 **{summary['id_map']}** · 합병증 {summary['complications']} · 부작용 {summary['side_effects']} · 합병증 gap {summary['complication_gap_families']} · open **{summary['open']}**", '',
     '## 1. 노드 종류', '', '| # | 정본 종류 | 이름 | 뜻 | 정본 id · 실버 id 규칙 | 필수 | 선택 | 정본 파일 · 칸 | 셈 |', '|---|---|---|---|---|---|---|---|---|']
for i, n in enumerate(NODES, 1):
    L.append(f"| {i} | `{n['kind']}` | {esc(n['name'])} | {esc(n['meaning'])} | `{n['canonical_id']}` — {esc(n['id_rule'])}<br>실버 꼴 {jj(n['silver_id_patterns'])} | {esc(' · '.join(n['required']))} | {esc(' · '.join(n['optional']))} | `{n['canon']}` {esc(n['path'])} | **{n['count']}** {esc(n['detail'])} |")
L += ['', '### 1-1. 노드가 아닌 것(속성 · 칸)', '', '| 무엇 | 자리 | 셈 | 규칙 | 결정 |', '|---|---|---|---|---|']
L += [f"| {esc(x['what'])} | `{esc(x['where'])}` | {x['count']} {esc(x['detail'])} | {esc(x['rule'])} | {esc(x['decided'])} |" for x in ATTRS_NOT_NODES]
L += ['', '## 2. 엣지 종류', '', '| # | 정본 종류 | 이름 | 뜻 | 시작 → 끝 | 방향 | 속성 | 정본 파일 · 칸 | 셈 | 상속 | 페이지 종류 |', '|---|---|---|---|---|---|---|---|---|---|---|']
for i, e in enumerate(EDGES, 1):
    L.append(f"| {i} | `{e['kind']}` | {esc(e['name'])} | {esc(e['meaning'])} | {esc(e['frm'])} → {esc(e['to'])} | {esc(e['directed'])} | {esc(' · '.join(e['attrs']))} | `{e['canon']}` {esc(e['path'])} | **{e['count']}** {esc(e.get('detail', ''))} | {'계열 단위' if e['inherit'] else ''} | {esc(', '.join(e['page']) or '(새로)')} |")
L += [''] + [f"- 저장 엣지 아님: `{x['page']}` — {esc(x['why'])}" for x in NOT_EDGES]
L += ['', '## 3. 용어집', '', '| 용어 | 정의 | 출처 |', '|---|---|---|'] + [f"| **{esc(g['term'])}** | {esc(g['definition'])} | {esc(g['source'])} |" for g in GLOSSARY]
ds = DICT_SUMMARY
L += ['', '## 4. 사전 하나(B5)', '', f"표현 **{ds['expressions']}** · 대상 {ds['targets']} · 겹침 {ds['collisions']} · 7↔8단계 수준 합침(F) {ds['level_merged_F']} · 정규화 「{ds['normalize']}」", '',
      f"- 행 = `expr` · `norm` · `variants[]` · `targets[{{id, qualifier, reasons[]}}]` · `sources[]` · `mode`(하나 · 전부 · 후보) · `ambiguous` · `collision` · `prefer`", f"- {ds['research_collisions_note']}", '',
      '| 겹침 갈래 | 셈 | 처리 | 뜻 |', '|---|---|---|---|'] + [f"| {c} | {v['n']} | {v['mode']} | {esc(v['how'])} |" for c, v in ds['collisions_by_class'].items()]
L += ['', '출처별 원소: ' + ' · '.join(f"{k} {v}" for k, v in ds['by_source'].items()), '', '**7 · 8단계 같은 낱말 → 8단계 수준(계열 + qualifier)으로 합침**', '', '| 낱말 | 7단계 | 8단계(정본) |', '|---|---|---|']
L += [f"| {esc(x['text'])} | {jj(x['step7'])} | {jj(x['step8'])} |" for x in F_LEVEL]
L += ['', '**보고(7단계 결정은 이번에 안 바꿈)**', ''] + ([f"- {esc(x['text'])}: {esc(x['verdict'])}" for x in F_CONFLICT] or ['- 없음'])
L += ['', '**겹침 행**', '', '| 표현 | 대상 | 갈래 | 처리 |', '|---|---|---|---|'] + [f"| {esc(r['expr'])} | {esc(' · '.join(t['id'] + ('+' + json.dumps(t['qualifier'], ensure_ascii=False) if t['qualifier'] else '') for t in r['targets']))} | {r['collision']} | {r['mode']}{(' · ' + r['prefer'] + ' 우선') if r.get('prefer') else ''} |" for r in coll]
L += ['', f"해석 규칙(사전 행 아님): 고민 규칙 {', '.join(INTERPRET_RULES['concern_rule_ids'])} · 8단계 꼬리 낱말 {len(INTERPRET_RULES['step8_resolver']['tail_words'])} · 3단계 패턴 {INTERPRET_RULES['step3_lexicon']['patterns']} · 문장 패턴 {INTERPRET_RULES['sentence_patterns']} · 조건 패턴 {INTERPRET_RULES['condition_patterns']}"]
L += ['', '## 5. id 규칙(B6) — 정본 id ↔ 실버 id', '', OUT['ids']['rule'], '', '| 종류 | 규칙 |', '|---|---|'] + [f"| `{k['kind']}` | {esc(k['rule'])} |" for k in OUT['ids']['kinds']]
L += ['', '| 실버 안 문자열 꼴 | 자리 | → 정본 | 메모 |', '|---|---|---|---|'] + [f"| `{esc(x['form'])}` | {esc(x['where'])} | {esc(x['to'])} | {esc(x['note'])} |" for x in STRING_FORMS]
L += ['', '「목적:」 · 결정 노드 문자열 대응: ' + ' · '.join(f"`{k}` → `{v}`" for k, v in sorted(SILVER_FORMS.items())), '',
      f"전체 대응표 {len(ID_MAP)}행은 `semantic.json` ids.map(정본 id · 종류 · 실버 id · 이름) — 실버 id 와 다른 것만:", '']
L += [f"- `{m['silver_id']}` → `{m['canonical']}`" for m in ID_MAP if m['canonical'].split(':', 1)[1] != str(m['silver_id'])]
L += ['', '## 6. 읽는 규칙', '', f"**reading_contract**: {READING['reading_contract']}", '', '| 칸 | 뜻 |', '|---|---|'] + [f"| `{k}` | {esc(v)} |" for k, v in READING['interval_fields'].items()]
L += ['', f"- 끝점: {READING['endpoints']}", f"- 부작용: {READING['side_effects']}", f"- 조건 아님: {READING['not_condition']}"] + [f"- {x}" for x in READING['default_response']]
L += ['', f"셈: {jj(READING['counts'])}", '', '### 6-1. 간격 낱말 사전', '', '| id | 패턴 | 칸 | 메모 |', '|---|---|---|---|'] + [f"| {b['id']} | `{esc(b['pattern'])}` | {jj(b['set'])} | {esc(b['note'])} |" for b in READING['interval_lexicon']]
L += ['', f"단위 환산 {jj(READING['units_days'])} · 조건부 한정어 `{esc(READING['scope_rule']['words'])}`", '', '### 6-2. 표시 12', '', '| 표시 | 뜻 | 실버 칸 | 셈 | 읽는 법 |', '|---|---|---|---|---|']
L += [f"| `{f['flag']}` | {esc(f['ko'])} | {esc(' · '.join(f['fields']))} | {f['count']} | {esc(f['read'])} |" for f in FLAG_LIST]
L += ['', '### 6-3. gate_status 3값', '', '| 값 | 뜻 |', '|---|---|'] + [f"| {g['value']} | {esc(g['meaning'])} |" for g in GATE['values']] + ['', f"- {GATE['rule']}", f"- 지금: {jj(GATE['now'])}"]
L += ['', '## 7. 상속 규칙(B7 — 저장 안 함 · 골드 계산)', '', '| id | 이름 | 규칙 | 실버 칸 | 셈 | 지금 저장된 것 |', '|---|---|---|---|---|---|']
L += [f"| {x['id']} | {esc(x['name'])} | {esc(x['rule'])} | {esc(' · '.join(x['fields']))} | {jj(x['count'])} | {esc(x['stored_now'])} |" for x in INHERIT]
L += ['', '## 8. 근거 문장 종류(B2)', '', f"field {jj(STATEMENTS['by_field'])} → class {jj(STATEMENTS['by_class'])}", '', f"- {STATEMENTS['rule']}", f"- 원천 수정 후보(칸과 뜻이 다름) {len(STATEMENTS['source_fix'])}: {', '.join(STATEMENTS['source_fix'])}"]
L += ['', '## open', ''] + ([f"- {jj(x)}" for x in OPEN] or ['없음'])
open(W / 'semantic.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(json.dumps(summary, ensure_ascii=False))
sys.exit(1 if OPEN else 0)
