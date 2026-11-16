# 1단계 원장 반영 — 사용자 결정 전부를 step1-products 에 (2026-10-28)
#
# 입력(고정): step1-products-v1-frozen.json(10-27 합본 390행) · 조사 결과 step1-d*.json · step1-cancel-recheck.json
#            · step1-export-check.json(emedi 수출용 조회) · step1-kpic.json(KPIC 의약품 보강)
# 결정 정본: _RESUME.md §2 10-27 · 10-28 행 · gate-answers/step1-decisions-db-2026-10-28.md
# 5단계 추가 조사 반영(10-29): step1-step5-decisions.json(U8 되살림 · U9 새 행)
# 출력: step1-products.json · .md · step1-source-fix.json · .md · step1-origin-questions.md · step1-apply-log.md
#
# 결정론: 같은 입력이면 같은 출력. 추정 금지 — 결정에 없는 변경은 하지 않고 open[] 에 남긴다.
import json, re, copy, collections

W = '.'
J = lambda f: json.load(open(f'{W}/{f}'))
SRC = J('step1-products-v1-frozen.json')
D09, D12, D15, D16 = J('step1-d09-web.json'), J('step1-d12-web.json'), J('step1-d15-web.json'), J('step1-d16-web.json')
D17, D172, D18, D19 = J('step1-d17.json'), J('step1-d17-2.json'), J('step1-d18.json'), J('step1-d19.json')
D2031, CR = J('step1-d20-31.json'), J('step1-cancel-recheck.json')
EXPORT = J('step1-export-check.json')
KPIC = J('step1-kpic.json')

H = re.compile('[가-힣]')
items = copy.deepcopy(SRC['items'])
EXTRA_Q = {}
SRC_IDS_WITH_3LINE = {it['ledger_id'] for it in SRC['items'] if it.get('3_line') is not None}
idx = {it['ledger_id']: it for it in items}
LOG = []          # (결정, ledger_id, 이름, 무엇을)
SFIX = []         # 원천 수정
OPEN = []         # 전역 open
RES = lambda f, lid: next(x for x in f['items'] if x.get('ledger_id') == lid)


def log(dec, lid, what):
    nm = idx[lid]['2_names'].get('display_name') or idx[lid]['2_names'].get('ledger_name') if lid in idx else ''
    LOG.append({'decision': dec, 'ledger_id': lid, 'name': nm, 'change': what})


def norm_no(no):
    return re.sub(r'[\s호]', '', str(no or ''))


def row_open(lid, text, dec=None):
    it = idx[lid]
    it.setdefault('open', [])
    if text not in it['open']:
        it['open'].append(text)
    OPEN.append({'ledger_id': lid, 'name': it['2_names'].get('display_name') or it['2_names'].get('ledger_name'), 'open': text, 'decision': dec})


def sfix(sid, lid, field, now, fix, why, dec, src=None):
    LOG.append({'decision': dec, 'ledger_id': lid, 'name': idx[lid]['2_names'].get('ledger_name') if lid in idx else '', 'change': f'원천 수정 목록 {sid} — {field} {now} → {fix}'})
    SFIX.append({'id': sid, 'ledger_id': lid, 'name': idx[lid]['2_names'].get('ledger_name') if lid in idx else None,
                 'field': field, 'now': now, 'fix': fix, 'why': why, 'decision': dec, 'source': src})


# ───────────────────────── 0. 공통 정규화 ─────────────────────────

def is_domestic(no):
    return bool(re.match(r'^\s*(서울|경인|대구|부산|광주|대전)?\s*제', str(no or '')))


def lic_state(l):
    return (l.get('state') or '').strip()


def mk_lic(no, kind, state, holder, item=None, official_name=None, models=None, manufacturer=None, date=None,
           source=None, **extra):
    d = {'key': f'{"drug" if kind == "의약품" else "device"}:{norm_no(no)}', 'license_no': no, 'kind': kind,
         'state': state, 'item': item, 'official_name': official_name, 'models': models or [], 'holder': holder,
         'manufacturer': manufacturer, 'date': date, 'source': source}
    d.update(extra)
    return d


for it in items:
    L = it['4_license']
    L.setdefault('licenses', [])
    L.setdefault('history', [])
    L.setdefault('reference', [])
    # 10-27 데이터에 따로 있던 후보 칸은 reference 로 합친다(연결 안 함)
    for c in L.pop('candidates_not_linked', []) or []:
        c = dict(c); c['why'] = '후보 · 연결 안 함(10-27 기록)'
        L['reference'].append(c)
    for k in ('recommendable', 'rule'):
        L.pop(k, None)
    it.setdefault('open', [])
    co = it['6_companies']
    for r in ('manufacturer', 'importer', 'seller'):
        for e in co.get(r) or []:
            if not e.get('name'):
                e['name'] = '근거 없음'
    co.setdefault('license_holder', [])
    co.setdefault('other', [])
    co.setdefault('conflicts', [])


# 0-1. 수출용 허가 → 연결 안 함 · 참고 (10-27 규칙). emedi xprtppYn=예 · KPIC 제품명 「(수출용)」
EXP = {norm_no(x['license_no']): x for x in EXPORT['items'] if x.get('export') is True}
# 의약품: 식약처 의약품 허가 품목명(ITEM_NAME · ITEM_ENG_NAME)의 「(수출용)」 · 「for export」로만 판단(재판정 10-28 · KPIC 제품명은 낡을 수 있음 — 202107200)
RECHECK = J('step1-export-recheck.json')
for it_ in SRC['items']:
    for l_ in it_['4_license'].get('licenses') or []:
        if l_.get('kind') == '의약품' and ('수출용' in (l_.get('official_name') or '') or 'for export' in (l_.get('official_name_en') or '').lower()):
            EXP.setdefault(norm_no(l_['license_no']), {'license_no': l_['license_no'], 'source': f'식약처 의약품 허가 품목명 「{l_["official_name"]}」 · 영문 「{l_.get("official_name_en")}」'})


def export_filter(stage):
    for it in items:
        L = it['4_license']
        keep = []
        for l in L['licenses']:
            x = EXP.get(norm_no(l['license_no']))
            if x:
                l = dict(l); l['why'] = f'수출용에 한함 — 국내 허가로 치지 않음(10-27 규칙) · 근거 {x["source"]}'
                L['reference'].append(l)
                log('규칙 1 수출용', it['ledger_id'], f'{l["license_no"]} 연결 → 참고(수출용){stage}')
            elif '재제조' in json.dumps(l, ensure_ascii=False) or norm_no(l['license_no']) == '수허26-194':
                l = dict(l); l['state'] = '재제조(정품 아님)'
                L['history'].append(l)
                log('규칙 1 재제조', it['ledger_id'], f'{l["license_no"]} 연결 → 이력(재제조){stage}')
            else:
                keep.append(l)
        L['licenses'] = keep


export_filter('')


# ───────────────────────── 1. 결정별 반영 ─────────────────────────

def set_status(lid, status, reason, dec):
    L = idx[lid]['4_license']
    old = L['status']
    L['status'] = status
    L['reason'] = reason
    log(dec, lid, f'상태 {old} → {status}' if old != status else f'상태 {status} 유지(결정 확인)')


def unlink_to_ref(lid, why, dec, only=None):
    L = idx[lid]['4_license']
    keep = []
    for l in L['licenses']:
        if only is None or norm_no(l['license_no']) in {norm_no(x) for x in only}:
            l = dict(l); l['why'] = why
            L['reference'].append(l)
            log(dec, lid, f'{l["license_no"]} 연결 해제 → 참고')
        else:
            keep.append(l)
    L['licenses'] = keep


def add_lic(lid, l, dec):
    L = idx[lid]['4_license']
    if norm_no(l['license_no']) not in {norm_no(x['license_no']) for x in L['licenses']}:
        L['licenses'].append(l)
        log(dec, lid, f'허가 연결 {l["license_no"]}')
    L['history'] = [h for h in L['history'] if norm_no(h['license_no']) != norm_no(l['license_no'])]


def add_hist(lid, l, dec):
    L = idx[lid]['4_license']
    old = [x for x in L['history'] if norm_no(x['license_no']) == norm_no(l['license_no'])]
    if not old:
        L['history'].append(l)
        log(dec, lid, f'이력 추가 {l["license_no"]}({l["state"]})')
    elif old[0].get('state') != l['state']:
        log(dec, lid, f'이력 {l["license_no"]} 상태 {old[0].get("state")} → {l["state"]}(조사 결과)')
        old[0]['state'] = l['state']


def add_ref(lid, l, dec):
    L = idx[lid]['4_license']
    if norm_no(l['license_no']) not in {norm_no(x.get('license_no')) for x in L['reference']}:
        L['reference'].append(l)
        log(dec, lid, f'참고 기록 {l["license_no"]}')


def set_co(lid, role, entries, dec, replace=True):
    co = idx[lid]['6_companies']
    if replace:
        co[role] = entries
    else:
        names = {e['name'] for e in co[role]}
        co[role] = [e for e in co[role] if not e['name'].startswith('근거 없음')] + [e for e in entries if e['name'] not in names]
    log(dec, lid, f'{ {"manufacturer": "제조사", "importer": "수입사", "seller": "판매사", "license_holder": "허가권자", "other": "기타 역할"}[role] } = ' + ' · '.join(e['name'] for e in co[role]))


def conflict(lid, field, a, b, src, note='덮어쓰지 않음'):
    idx[lid]['6_companies']['conflicts'].append({'field': field, 'license': a, 'other': b, 'source': src, 'note': note})


def E(name, role, source, period=None):
    e = {'name': name, 'role': role, 'basis': source}
    if period:
        e['period'] = period
    return e


NAME_OVERRIDE = {}   # lid → (대표 이름, 근거)
EXTRA_SEARCH = collections.defaultdict(list)   # lid → [(이름, 근거)]
LINES = {}           # line_name → {...}
MERGED = {}          # dup → rep
MOVED = {}           # lid → (moved_to, note)


def line(name, rep_lid, items_, maker=None, undetermined_rows=(), basis=None, dec=None, parent=None):
    LINES[name] = {'line_name': name, 'parent_line': parent, 'line_row': rep_lid, 'items': items_,
                   'item_undetermined_rows': list(undetermined_rows), 'company': maker, 'basis': basis, 'decision': dec}


def lic_from_row(lid, no):
    for l in idx[lid]['4_license']['licenses'] + idx[lid]['4_license']['history']:
        if norm_no(l['license_no']) == norm_no(no):
            return copy.deepcopy(l)
    raise KeyError((lid, no))


EM = 'emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item'
EL = 'emedi 품목 검색 POST https://emedi.mfds.go.kr/search/data/list'

# D01 · D03 — 허가 규칙(디클래씨 11-1324 정상 연결 · 23-60 이력)은 10-27 반영됨. 젠틀레이즈 → 아래 취소 재조사
log('D01', 'auto-12-1774737181584', '확인 — 제허 11-1324 정상 연결 · 23-60(취소) 이력 유지')

# D02 텐쎄라
lid = 'M9-1-10'
set_co(lid, 'manufacturer', [E('(주)아스테라시스', '제조(허가권자 · 「제」 허가)', '식약처 의료기기 허가 제허 19-237 · 20-492')], 'D02')
conflict(lid, '제조사', '(주)아스테라시스(식약처)', 'TENTECH(해외 보도) · 원장 「원텍」', 'company-relation-check.json 텐쎄라')
sfix('SF-D02-1', lid, '원장 업체', '원텍', '(주)아스테라시스 — 업체 표기 확인', '식약처 허가권자(국내 제조)는 (주)아스테라시스 · 원텍과의 관계 근거 0', 'D02', 'company-relation-check.json')

# D04 에이비오톡신 → 디스포트
MERGED['auto-M1-1775364775100'] = 'M1-2-3'
EXTRA_SEARCH['M1-2-3'] += [('에이비오톡신', '한글 약칭 — 공식 근거 없음 · 사용자 판단(10-27 D04)'),
                           ('abobotulinumtoxinA', '성분명 — FDA Purple Book BLA 125274 Proper Name(10-27 D04)')]
sfix('SF-D04-1', 'auto-M1-1775364775100', '설명', '「에이비오에서 제조」', '디스포트(입센) 성분 abobotulinumtoxinA 를 부르는 이름 — 제조사 설명 고침', '설명 오류 후보 — 에이비오라는 제조사 근거 없음', 'D04')

# D05 온다 라인
lid = 'M9-3-1'
set_co(lid, 'manufacturer', [E('EL.EN. S.p.A.', '제조원', '식약처 허가 수인 22-4482 · 24-369 · 수허 26-28 제조원')], 'D05')
set_co(lid, 'importer', [E('(주)에코라', '수입(허가권자)', '식약처 허가 수인 22-4482 · 24-369 · 수허 26-28')], 'D05')
line('온다', lid, [{'license_no': '수인22-4482호', 'name': 'ONDA'}, {'license_no': '수인24-369호', 'name': 'ONDA SMART'},
                  {'license_no': '수허26-28호', 'name': 'ONDA PRO(품목 범용 전기 수술기 그대로)'}], '수입 에코라 · 제조 EL.EN.', dec='D05')

# D06 · D07 더채움
line('더채움', 'M2-1-2', [{'license_no': '제허20-527호', 'name': '더채움 프리미엄', 'ledger_id': 'auto-M2-1775364775108'},
                        {'license_no': '제허17-809호'}, {'license_no': '제허14-1762호'}, {'license_no': '제허14-860호'}],
     '(주)아크로스', dec='D07')
NAME_OVERRIDE['auto-M2-1775364775108'] = ('더채움 프리미엄', '허가 제품명 「the 채움 프리미엄」 · 원장 「프리미어」는 오기(D06)')
sfix('SF-D06-1', 'auto-M2-1775364775108', '제품 이름', '더채움프리미어', '더채움 프리미엄', '허가 제허 20-527 제품명 「더채움 프리미엄」 · 보도 라인명도 「더채움 프리미엄」', 'D06')
EXTRA_SEARCH['M2-1-2'] += [('채움', 'taxonomy M2-P-5 이름 — 허가 제품명 「더 채움」에 그대로 있음(D30)')]

# D08 확정 4
for lid in ['auto-M8-1775362921273', 'auto-M8-1775362936434', 'auto-M11-1775360510687', 'new-DEV-068']:
    log('D08', lid, '확정(재조사 연결 그대로)')

# D09 일치 14 받기 · 리레이저 · 더마큐어 확인 불가
for x in D09['items']:
    lid = x['ledger_id']
    if x['link'] == '일치':
        log('D09', lid, '받기(이름 일치 허가 연결 확정)')
for lid in ['auto-M8-1775362951135', 'new-DEV-042']:
    unlink_to_ref(lid, '이름 든 허가지만 원장 제품과 같다는 출처 없음(D09 웹 확인) — 연결 안 함', 'D09')
    set_status(lid, '확인 불가', '이름 든 허가는 있으나 같은 제품이라는 국내 웹 출처 없음(step1-d09-web) — D09 사용자 결정 확인 불가', 'D09')
lid = 'auto-M1-1775362462896'   # 톡스온 — 허가권자 칸 분리
co = idx[lid]['6_companies']
co['license_holder'] = [E('(주)에이티지씨', '허가권자(품목허가 획득)', '식약처 의약품 허가 202500353 · step1-d09-web')]
co['seller'] = [E('근거 없음', None, '국내 판매·유통사 기사 0 — 보도된 판권은 해외뿐(step1-d09-web)')]
log('D09', lid, '판매사 칸의 (주)에이티지씨 → 허가권자 칸(웹 출처상 허가권자) · 판매사 근거 없음')
lid = 'M2-2-5'
set_co(lid, 'seller', [E('디엔컴퍼니', '유통 · 출시(「‘퍼펙타’ 유통 DN컴퍼니」)', 'https://www.hkn24.com/news/articleView.html?idxno=138645', '2014-11 보도 — 현재 유통 출처 없음')], 'D09')
conflict(lid, '제조사', 'Sinclair France SAS(허가 제조원)', '프랑스 오비라인(Obvieline) 개발·제조(2015 보도)', 'https://www.dailypharm.com/user/news/119408')
lid = 'M2-2-6'
set_co(lid, 'seller', [E('대화제약(주)', '국내 판매 · 독점 유통(허가 수입사와 같은 회사 · 2017 S&V 인수)', 'https://www.monews.co.kr/news/articleView.html?idxno=102232', '2014~')], 'D09')

# D10 받기 7 · 캐번실 해제
for lid in ['M2-1-4', 'M2-1-6', 'M3-3-2', 'auto-M7-1775361076707', 'auto-M7-1775362571755', 'auto-M15-1775360527416', 'auto-M15-1775361179297']:
    log('D10', lid, '받기(음역 대응 허가 연결 확정)')
lid = 'auto-M7-1775362729861'
unlink_to_ref(lid, '비알팜 「Vita-lifts Cavern」은 이름 일부만 같은 다른 회사 제품(step1-d09-web) — D10 연결 해제', 'D10')
set_status(lid, '확인 불가', '캐번 = 네오닥터(잼버 이전 모델) · 허가 특정 불가 — 네오닥터 허가 18건 모델명이 코드라 어느 허가인지 이름으로 특정 못 함(D10 사용자 결정)', 'D10')
set_co(lid, 'manufacturer', [E('(주)네오닥터', '개발 · 출시(2017 · 2021 잼버로 업그레이드)', 'http://www.bosa.co.kr/news/articleView.html?idxno=2146454')], 'D10')
conflict(lid, '제조사', '(주)비알팜(해제한 허가)', '(주)네오닥터(캐번 개발·출시)', 'http://www.bosa.co.kr/news/articleView.html?idxno=2146454')
row_open(lid, '캐번(2017)이 2021 잼버로 바뀌어 지금도 「캐번」으로 유통되는지 출처 없음 — 「허가번호 미확인」 규칙 대상인지 사용자 판단 · 잼버실(auto-M7-1775361076707)과 라인인지 정할 것', 'D10')

# D11 받기 4 · 젠틀맥스프로/프로+
for lid in ['M9-2-1', 'auto-M9-1775364775131', 'M8-5-5', 'M9-1-9']:
    log('D11', lid, '받기(모델명 표기 다른 허가 연결 확정)')
gmp = mk_lic('수허 18-338 호', '의료기기', '정상', '시너론켄델라코리아 유한회사', item='알렉산드라이트레이저수술기',
             official_name='Gentle Max Pro, Gentle Max Pro Plus', models=['9914-00-9035', '9914-CE-9036'],
             manufacturer='NPA de Mexico S. de R.L. de C.V.(제조의뢰 Candela Corporation)', date='2018-11-22',
             source=f'{EL} query2=9914-00-9035 · Gentle Max (step1-d09-web · step1-cancel-recheck)')
h13466 = mk_lic('수허 13-466 호', '의료기기', '취하', '(주)신한씨스텍', official_name='GentleMax Pro', date='2019-09-17(취하)', source='step1-d09-web')
h09142 = mk_lic('수허 09-142 호', '의료기기', '취하', '(주)신한씨스텍', official_name='Candela Family of Multiple-Wavelength Laser Systems: GentleMax', date='2019-11-28(취하)', source='step1-d09-web')
h26194 = mk_lic('수허 26-194 호', '의료기기', '재제조(정품 아님)', '주식회사 밴스로컬', official_name='GentleMaxi Pro Plus', date='2026-08-21',
                manufacturer='재제조원 LUCENTRA LIMITED(원제조의뢰 CANDELA CORPORATION · 원제조 NPA de Mexico)', source='step1-d09-web')
for lid in ['M8-5-3', 'auto-M8-1775362612108']:
    add_lic(lid, copy.deepcopy(gmp), 'D11')
    for h in (h13466, h09142, h26194):
        add_hist(lid, copy.deepcopy(h), 'D11')
    set_status(lid, '정상', '현재 정품 허가 수허 18-338(시너론켄델라코리아 · 정상) 연결 · 재제조 26-194 · 취하 13-466 · 09-142 는 이력(D11 · 취소 재조사)', 'D11')
    set_co(lid, 'manufacturer', [E('NPA de Mexico S. de R.L. de C.V.', '제조원(제조의뢰 Candela Corporation)', '식약처 허가 수허 18-338')], 'D11')
    set_co(lid, 'importer', [E('시너론켄델라코리아 유한회사', '수입(허가권자)', '식약처 허가 수허 18-338')], 'D11')
    set_co(lid, 'seller', [E('켄델라 코리아(시너론켄델라코리아 유한회사)', '판매 · 공식 사이트 표기(수입사와 같은 회사)', 'https://gentlemaxproplus.co.kr/find')], 'D11')
conflict('M8-5-3', '수입사', '주식회사 밴스로컬(재제조 허가 26-194)', '시너론켄델라코리아(정품 18-338)', 'https://gentlemaxproplus.co.kr/find', '재제조 ↔ 정품 — 덮어쓰지 않음')
row_open('M8-5-3', '젠틀맥스프로 · 젠틀맥스프로+ 두 행이 같은 허가 18-338(모델 두 개)을 가리킴 — 라인+품목(10-27 「같은 허가 원장 중복은 라인+품목」)으로 묶을지 사용자 판단', 'D11')

# D12 업체
D12_SAME = {  # lid: (원장 표기, 허가 업체 정식)
    'auto-10-1774737181584': ('PRP사이언스', '(주)피알피사이언스'),
    'auto-M2-1775362477273': ('비비안비', '(주)에코라 · 제조 Laboratoires VIVACY'),
    'auto-M2-1775362470502': ('크로마비전', '엠엔엘 · 제조 CROMA-PHARMA GmbH'),
    'auto-19-1774737181584': ('한스바이오파마', '한스바이오메드(주)'),
    'auto-16-1774737181584': ('삼양홀딩스', '(주)삼양바이오팜'),
}
for lid, (ledger_co, official) in D12_SAME.items():
    co = idx[lid]['6_companies']
    co['company_search_names'] = [{'name': ledger_co, 'basis': '원장 업체 표기 — 허가 업체와 같은 회사(업체관계 결정 · D12 ①)'}]
    log('D12', lid, f'업체 = 허가 업체명 {official} · 원장 표기 「{ledger_co}」 업체 검색 이름')
    sfix(f'SF-D12-{lid}', lid, '원장 업체', ledger_co, official, '같은 회사 표기 차이 — 허가 업체명이 정식(D12 ①)', 'D12', 'company-relation-check.json')
lid = 'auto-8-1774737181584'  # 셀레스텔라
set_co(lid, 'seller', [E('(주)더에쓰씨', '브랜드 운영 · 유통(「HA필러 브랜드 ‘셀레스텔라’」 운영)', 'http://www.sisunnews.co.kr/news/articleView.html?idxno=239067', '2026-05 보도 시점')], 'D12')
row_open(lid, '알에프바이오(허가 · 제조) ↔ 더에쓰씨(판매) 공급 관계 출처 없음(step1-d12-web)', 'D12')
lid = 'auto-23-1774737181584'  # 힐로웨이브
set_co(lid, 'seller', [E('(주)네오팜', '국내 판권 · 독점 유통', 'https://www.smarttoday.co.kr/ko-kr/articles/79173', '2025-05-01~')], 'D12')
set_co(lid, 'other', [E('(주)하이어코퍼레이션', '개발 · 브랜드(판권 공여자)', 'https://www.higherlink.kr/article/higher-news-24120901', '2024-12 출시')], 'D12')
conflict(lid, '제조사', '(주)에스씨엘(제허 14-1193 허가 · 제조)', '하이어코퍼레이션 「개발」', 'https://www.smarttoday.co.kr/ko-kr/articles/79173', '에스씨엘 ↔ 하이어 위탁 관계 출처 없음 — 덮어쓰지 않음')
lid = 'M7-3-3'  # 테스리프트
set_co(lid, 'seller', [E('대한뉴팜', '독점판매(「‘TESSLIFT SOFT’ 독점판매 계약」)', 'https://www.medicaltimes.com/Main/view.html?ID=1120074', '2018-07 보도 — 현재 판매 출처 없음')], 'D12')
conflict(lid, '독점판매 계약 상대', '주식회사 테스(허가 · 제조)', '2018-07 「TESSLIFT社」 ↔ 2019-03 「지쉘그룹」', 'https://www.medicaltimes.com/Main/view.html?ID=1124809')
sfix('SF-D12-tess', lid, '원장 업체', '리젠바이오텍', '주식회사 테스(제조) · 판매 대한뉴팜', '리젠바이오텍 ↔ 테스리프트 연결 출처 0 — 국내 판매사 출처는 대한뉴팜(D12 웹 확인)', 'D12', 'step1-d12-web.json')
lid = 'auto-M7-1775362555891'  # 블루로즈클레어
set_co(lid, 'manufacturer', [E('(주)제이월드', '제조(허가권자 · 휴젤 자회사 지분 80%)', '식약처 허가 제허 21-1025 · https://www.etoday.co.kr (2020-11-03 인수)')], 'D12')
set_co(lid, 'seller', [E('(주)휴젤', '브랜드 보유 · 영업·마케팅(제이월드 모회사)', 'https://www.smarttoday.co.kr/ko-kr/articles/81359', '2020-11~ 현재')], 'D12')
lid = 'new-DEV-063'  # 큐라스토닝
set_co(lid, 'manufacturer', [E('(주)클래시스', '제조(허가권자 · 이루다 흡수합병 2024-10)', '식약처 허가 제허 15-629 · https://classys.co.kr/product/curas-hybrid/')], 'D12')
set_co(lid, 'seller', [E('(주)클래시스', '제조 · 판매(공식 제품 페이지)', 'https://classys.co.kr/product/curas-hybrid/', '2024-10 합병 후')], 'D12')
set_co(lid, 'other', [E('(주)이루다(합병 전)', '개발 · FDA 510(k) 신청자', 'https://fda.innolitics.com/device/K173038', '2017-12 ~ 2024-10')], 'D12')
conflict(lid, '제조사', '(주)클래시스(제허 15-629 · 2015)', '(주)이루다(FDA K173038 · 2017)', 'https://fda.innolitics.com/device/K173038', '합병으로 허가가 넘어갔는지 출처 없음 — 덮어쓰지 않음')
conflict(lid, '제조원 칸', '클래시스 · LaserPair Co., Limited · 유리드알앤디', 'LaserPair = 레이저 보호안경 제조사(검색)', 'https://freshdi.com/supplier/LaserPair-Co-Limited')
lid = 'M15-2-1'  # 아쿠아필
set_co(lid, 'seller', [E('(주)네오메드', '판매(「미용기기 아쿠아필 판매 개시」)', 'https://m.jobkorea.co.kr/company/44611675', '2011-03~ · 2026 신품 판매 출처 없음')], 'D12')
conflict(lid, '제조사', '엠아이테크(제인 11-712)', '새서울메디칼 쇼핑몰 「제조사 자체제작」', 'https://ssmedi.com/product/%EC%95%84%EC%BF%A0%EC%95%84%ED%95%84-aqua-peel/44')
# 아포지플러스는 아래 D16 합침 — 관계는 대표 행에
lid = 'auto-36-1774737181584'
set_co(lid, 'other', [E('Cynosure, Inc.(사이노슈어)', '브랜드 · 제조의뢰(FDA K034030 Applicant)', 'https://fda.innolitics.com/device/K034030'),
                      E('사이노슈어 루트로닉', '수입사 루트로닉과 2024 합병', 'https://www.medipana.com/news/articleView.html?idxno=324858')], 'D12')
conflict(lid, '제조사', 'Cogmedix Inc.(수허 05-546 제조원)', '미국 사이노슈어社(보도 · FDA)', 'https://fda.innolitics.com/device/K034030', 'Cogmedix ↔ Cynosure 위탁 관계 원문 열람 실패 — 덮어쓰지 않음')

# D13 원장 오기 3
for lid, wrong, right in [('M1-1-7', '리즈톡신', '리즈톡스'), ('auto-49-1774737181584', '아스트로더', '아스트로돔'), ('new-DEV-074', '스캐나', '스케나')]:
    NAME_OVERRIDE[lid] = (right, f'원장 「{wrong}」은 오기 — 허가 · 사진 라벨 · 공식 표기 「{right}」(D13)')
    sfix(f'SF-D13-{right}', lid, '제품 이름', wrong, right, '허가 · 사진 라벨 · 공식 표기로 오기 확인', 'D13')

# D14
lid = 'auto-M2-1775364775107'  # 엘라비에프라임 → 엘라비에 프리미어 라인
for no in ['제허 22-434 호', '제허 20-867 호', '제허 20-206 호', '제허 19-21 호']:
    add_lic(lid, lic_from_row('M2-1-8', no), 'D14')
set_status(lid, '정상', '엘라비에 프리미어(휴메딕스) 라인에 연결 · 품목 미정 — 근거 사용자 판단(「프라임」 별칭 공식 근거 없음, D14)', 'D14')
set_co(lid, 'manufacturer', [E('(주)휴메딕스', '제조(허가권자 · 「제」 허가)', '식약처 허가 제허 22-434 · 20-867 · 20-206 · 19-21')], 'D14')
NAME_OVERRIDE[lid] = ('엘라비에 프리미어', '원장 「엘라비에프라임」 → 엘라비에 프리미어 라인(사용자 판단 · D14)')
line('엘라비에 프리미어', lid, [{'license_no': n} for n in ['제허 22-434 호', '제허 20-867 호', '제허 20-206 호', '제허 19-21 호']], '(주)휴메딕스',
     undetermined_rows=[lid], basis='M2-1-8 gate 「프리미어 라인(22-434 · 20-867 · 20-206 · 19-21)」', dec='D14', parent='엘라비에')
MERGED['auto-M9-1775363051791'] = 'M9-1-8'
sfix('SF-D14-lifsera', 'auto-M9-1775363051791', '원장 행', '리프세라(별도 행)', '리프테라(M9-1-8)와 같은 제품 — 행 합침', '원장 자동 병합 때 중복 생성(사용자 확인 D14)', 'D14')
for lid in ['auto-M8-1775364775128', 'auto-M1-1775364775101']:
    set_status(lid, '확인 불가', '비슷한 이름 후보는 있으나 같은 제품 근거 없음 — 원천 확인(D14 사용자 결정 확인 불가 유지)', 'D14')
row_open('auto-M1-1775364775101', '업체 「메디콕스」는 실제 별도 회사(메디톡스 오기 아님 · 사용자 D14) — 실제 제품명 · 제조사는 원천 질문', 'D14')

# D15
lid = 'auto-M9-1775364775134'  # 더블로골드S
dl = idx[lid]['3_line']['other_line_items']
for x in dl:
    add_lic(lid, mk_lic(x['license_no'], '의료기기', x['state'], '(주)하이로닉', models=[x['model']],
                        source='식약처 의료기기 품목허가 API TYPE_NAME=DOUBLO(구간 B other_line_items)'), 'D15')
set_status(lid, '정상', '더블로 라인(하이로닉) 전체에 연결 · 품목 미정(D15 사용자 결정 「라인 전체에 붙임」)', 'D15')
set_co(lid, 'manufacturer', [E('(주)하이로닉', '제조(라인 허가권자)', '식약처 허가 제허 11-238 · 13-291 · 18-195')], 'D15')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D15')
line('더블로', 'M9-1-5', [{'license_no': x['license_no'], 'name': x['model']} for x in dl], '(주)하이로닉', undetermined_rows=[lid], dec='D15')
lid = 'auto-M4-1775360463217'  # 벨피엔 프로 → 밸피엔 라인
NAME_OVERRIDE[lid] = ('밸피엔', '허가 이름 「밸피엔」 라인(휴메딕스 26-757) · 원장 「벨피엔 프로」 · taxonomy 「벨피엔」은 검색 이름(D15 · D30)')
EXTRA_SEARCH[lid] += [('벨피엔', 'taxonomy M4-P-4 이름(D30)')]
line('밸피엔', lid, [{'license_no': '제허26-757호'}], '(주)휴메딕스', undetermined_rows=[lid], dec='D15')
row_open(lid, '원장 「프로」가 리도카인 신허가(26-757)를 가리키는지 출처 없음 — 원천 질문(D30)', 'D30')
lid = 'auto-M7-1775364775158'  # 울트라V
x = RES(D15, lid)
unlink_to_ref(lid, '「수출용에 한함」(emedi xprtppYn=예) — 국내 허가 아님(10-27 수출용 규칙 · D15)', 'D15')
for c in x['candidates']:
    if '수출용' in c['state'] and norm_no(c['no']) != '제허13-1398':
        add_ref(lid, {'license_no': c['no'], 'holder': c['entp'], 'official_name': c['brand'], 'item': c['item'], 'state': c['state'], 'source': c['src'], 'why': '수출용에 한함 — 연결 안 함'}, 'D15')
    if '취하' in c['state']:
        add_hist(lid, {'license_no': c['no'], 'kind': '의료기기', 'holder': c['entp'], 'official_name': c['brand'], 'item': c['item'], 'state': '취하', 'date': c['state'], 'source': c['src']}, 'D15')
set_status(lid, '허가 취소(이력)', '국내 허가 없음(수출용만) — 내수 실 허가(울트라브이 14-182 등)는 전부 취하(D15 · step1-d15-web)', 'D15')
set_co(lid, 'seller', [E('(주)종근당', 'PDO 독점공급계약(2014-05) · 「종근당의 울트라V」 보도', 'https://www.ultrav.co.kr/about/history.php', '2014-05 ~ 2015 보도 — 현재 판매 출처 없음'),
                       E('주식회사 울트라브이', '제조의뢰 · 공급(회사 소개)', 'https://www.ultrav.co.kr/about/history.php', '2013~')], 'D15')
row_open(lid, '상태 — 결정 문구 「국내 허가 없음(수출용만)」을 정상 없이 취하 이력만 있는 경우로 보고 「허가 취소(이력)」로 둠. 「미허가」로 볼지 사용자 확인 · 연결 해제한 미스코 13-1398 ↔ 울트라브이 관계 출처 없음', 'D15')
lid = 'auto-M7-1775362513156'  # 해피리프트 → 시술 이름
MOVED[lid] = ('5단계 시술 이름', '해피리프트 = 압토스 실 리프트 시술 이름(의협신문 2006-01-31) — 제품은 압토스(수허 25-219) 새 행')
lid = 'auto-M7-1775362579841'  # 오메가리프트 → 오메가브이 라인
x = RES(D15, lid)
for c in x['candidates']:
    if '내수' in c['state']:
        add_lic(lid, mk_lic(c['no'], '의료기기', '정상', c['entp'], item=c['item'], official_name=c['brand'], date=c['state'], source=c['src']), 'D15')
    elif '수출용' in c['state']:
        add_ref(lid, {'license_no': c['no'], 'holder': c['entp'], 'official_name': c['brand'], 'state': c['state'], 'source': c['src'], 'why': '수출용에 한함 — 연결 안 함'}, 'D15')
set_status(lid, '정상', '오메가브이 라인(오브이메디 내수 정상 13-151 · 13-150 · 15-188) 전체에 연결 · 품목 미정(D15)', 'D15')
set_co(lid, 'manufacturer', [E('주식회사 오브이메디', '제조(라인 허가권자)', '식약처 허가 제허 13-151 · 13-150 · 15-188')], 'D15')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D15')
line('오메가브이', lid, [{'license_no': c['no'], 'name': c['brand']} for c in x['candidates'] if '내수' in c['state']], '주식회사 오브이메디', undetermined_rows=[lid], dec='D15')
row_open(lid, '옛 업체 오브이코리아(12-516 · 12-419 취하)와 오브이메디가 같은 회사라는 출처 없음', 'D15')

# 새 행 — 압토스(D15 「제품 APTOS 수허 25-219」)
APTOS = {
    'ledger_id': 'step1-new-APTOS', 'segment': '결정 반영', 'source': 'decision', 'family': copy.deepcopy(idx['auto-M7-1775362513156']['family']),
    '1_identity': {'kind': '제품(의료기기)', 'basis': 'D15 사용자 결정 「해피리프트 = 시술 이름 · 제품 APTOS 수허 25-219」 · step1-d15-web', 'basis_type': '사용자 결정'},
    '2_names': {'ledger_name': None, 'product_name': 'Aptos', 'synonyms': [{'name': 'Aptos', 'type': '허가 제품명'}, {'name': '아프토스', 'type': '해피리프트 행 동의어(web4)'}]},
    '3_line': None,
    '4_license': {'status': '정상', 'kind': '의료기기', 'reason': '수허 25-219(인터케어사이언스 · 정상 · 내수) 연결(D15)', 'licenses': [
        mk_lic('수허 25-219 호', '의료기기', '정상', '주식회사 인터케어사이언스', item='안면조직 고정용 실', official_name='Aptos',
               manufacturer='Aptos LLC', date='2025-12-17', source=f'{EM} meddevItemSeq=2025003907')], 'history': [], 'reference': []},
    '5_spec': None, '6_companies': {'manufacturer': [E('Aptos LLC', '제조원', '식약처 허가 수허 25-219')],
                                    'importer': [E('주식회사 인터케어사이언스', '수입(허가권자)', '식약처 허가 수허 25-219')],
                                    'seller': [E('주식회사 인터케어사이언스', 'APTOS 국내 독점유통', 'https://www.hinews.co.kr/view.php?ud=2024111115172032486aa9cc43d0_48', '계약 2023-08 ~ 2026-07 보도')],
                                    'license_holder': [], 'other': [], 'conflicts': []},
    '7_site_use': None, 'gate': None, 'change_vs_draft': None, 'note': '해피리프트(auto-M7-1775362513156) 행이 시술 이름으로 빠지며 생긴 제품 행', 'evidence': ['step1-d15-web.json 해피리프트 candidates'],
    'open': [],
}
items.append(APTOS); idx[APTOS['ledger_id']] = APTOS
log('D15', 'step1-new-APTOS', '새 행 — 압토스(수허 25-219) · 해피리프트에서 분리')
row_open('step1-new-APTOS', '현장이 지금 쓰는 실이 APTOS 인지 · 2006 압토스 실과 25-219 제품이 같은지 출처 없음(step1-d15-web)', 'D15')

# D16 14쌍 · PHA필 · 물톡스 · 라라
for dup, rep in [('auto-M3-1775364775147', 'auto-M2-1775360655397'), ('auto-M3-1775364775145', 'M3-1-1'), ('auto-M4-1775362490962', 'M9-2-3'),
                 ('auto-24-1774737181584', 'M4-2-2'), ('auto-M4-1775364775150', 'auto-M4-1775361364993'), ('new-DEV-005', 'auto-36-1774737181584'),
                 ('auto-M10-1775364775187', 'M10-2-2'), ('auto-M10-1775364775186', 'M10-1-1'), ('auto-35-1774737181584', 'M8-5-4'),
                 ('M1-P-10', 'M1-1-1'), ('auto-M15-1775362985090', 'M15-3-1'), ('auto-52-1774737181584', 'auto-48-1774737181584'),
                 ('auto-M16-DCA-1775404043061', 'auto-M16-1775403024925'), ('auto-M16-1775363074847', 'M15-4-1')]:
    MERGED[dup] = rep
row_open('M8-5-4', '「클라리티2 (혈관)」의 「혈관」은 5단계 단위 시술로(D16) — 제품은 클라리티2 하나', 'D16')
EXTRA_SEARCH['M1-1-1'] += [('Letybo', '해외 판매명 — 비즈워치 「국내 제품명: 보툴렉스」(D29)')]
for lid in ['auto-M15-1775401670325', 'auto-M15-1775402148301']:
    MOVED[lid] = ('5단계 시술 이름', '시술 이름 「PHA 필링」(검색 이름 물톡스) — 병원마다 쓰는 제품이 다름(step1-d16-web)')
line('라라', 'M15-1-7', [{'name': '라라필', 'ledger_id': 'M15-1-7'}, {'name': '라라닥터', 'ledger_id': 'auto-M15-1775401788467'}],
     '(주)에이치투메디', basis='같은 라인 다른 제품 2(step1-d16-web)', dec='D16')
x = D16['items'][1]
for lid in ['M15-1-7', 'auto-M15-1775401788467']:
    set_co(lid, 'manufacturer', [E('(주)에이치투메디(H2MEDI)', '개발 · 출시', 'https://www.ajunews.com/view/20250113163746036')], 'D16')
set_co('auto-M15-1775401788467', 'seller', [E('동구바이오제약', '국내 · 몽골 독점 유통 계약', 'https://www.hitnews.co.kr/news/articleView.html?idxno=74953', '2026-03 보도'),
                                            E('유벤타헬스케어', '동구바이오제약과 공동 유통', 'https://www.hitnews.co.kr/news/articleView.html?idxno=74953', '2026-03 보도')], 'D16')
set_co('M15-1-7', 'seller', [E('(주)에이치투메디', '라라필 본사(공급)', 'https://www.ajunews.com/view/20250113163746036', '2025-01 보도')], 'D16')
conflict('M15-1-7', '성분', '원천 「호박 추출물 프로테아제 효소」', '보도 「LHA, H2sol, Lipid, INCUBE 504」', 'https://www.ajunews.com/view/20250113163746036')
row_open('M15-1-7', '라라필 · 라라닥터 화장품/의료기기 여부 확인 불가(step1-d16-web) — 상태 「허가 대상 아님」은 10-27 게이트 기록(출처 URL 없음)', 'D16')

# D17
lid = 'auto-31-1774737181584'  # BBL히어로
set_co(lid, 'seller', [E('(주)아이맥', '판매(사용자 결정 D17) · 수입사와 같은 회사', 'https://emedi.mfds.go.kr/search/data/list query2=mJoule')], 'D17')
lid = 'auto-M14-1775363067062'  # 쿨미니
set_co(lid, 'seller', [E('한국애브비(주)', '현 수입사(허가 18-96 · 21-4556)', 'https://emedi.mfds.go.kr/search/data/list query2=CoolSculpting'),
                       E('일동에스테틱', '쿨미니 국내 출시(2016 보도) — 현재 판매 출처 없음', 'http://www.monews.co.kr/news/articleView.html?idxno=89871', '2016')], 'D17')
lid = 'new-DEV-053'  # AUTO MTS → DB FNS 라인
add_lic(lid, mk_lic('제인 12-1425 호', '의료기기', '정상', '(주)동방메디컬분당지점', item='의료용체내표시기(조합 — 약물흡수유도용피부자극기)',
                    official_name='DB MEDI TOUCH CUBE외 4건(모델 DB FNS · DB FNS CUBE · DB MEDI TOUCH …)', date='2012-11-07',
                    source=f'{EL} query2=DB FNS · emedi 상세(대표 모델 Crystal Premium) — step1-d17-2'), 'D17')
set_status(lid, '정상', '본체 제인 12-1425(DB FNS) · 니들 제인 10-343 — 동방메디컬 DB FNS 라인(D17 재조사)', 'D17')
set_co(lid, 'manufacturer', [E('(주)동방메디컬(동방메디컬분당지점)', '제조(허가권자 · 「제」 허가)', '식약처 허가 제인 12-1425 · 10-343')], 'D17')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D17')
set_co(lid, 'seller', [E('(주)동방메디컬', '제조 · 판매', 'https://emedi.mfds.go.kr/search/data/list query2=DB FNS'),
                       E('더미통상(서울종로의료기)', '온라인 판매', 'https://jongromedi.com/product/%EB%8F%99%EB%B0%A9%EB%A9%94%EB%94%94%EC%BB%AC-%EA%B5%AD%EC%82%B0-db-fns-%EC%98%A4%ED%86%A0mts-%EB%8B%88%EB%93%A4%EC%A1%B0%EC%A0%88-mts%EB%A8%B8%EC%8B%A0/1588/'),
                       E('하니메드', '온라인 판매(품절 표기)', 'https://hanimed.net/product/db-fns-%EB%8F%99%EB%B0%A9mts-dbfns-%EC%9D%98%EB%A3%8C%EC%9A%A9-%EC%B2%B4%EB%82%B4-%ED%91%9C%EC%8B%9C%EA%B8%B0-%EB%8B%88%EB%93%A4%EB%AF%B8%ED%8F%AC%ED%95%A8/349/')], 'D17')
line('DB FNS', lid, [{'license_no': '제인 12-1425 호', 'name': '본체(DB FNS)'}, {'license_no': '제인10-343호', 'name': '니들(DB FNS MICRO NEEDLE)'}], '(주)동방메디컬', dec='D17')
NAME_OVERRIDE[lid] = ('오토 MTS', '원장 「AUTO MTS」 · 판매 페이지 「오토MTS」(step1-d17-2)')
# 허가번호 미확인(10-28 규칙)
UNSPEC = {
    'auto-29-1774737181584': ('BBL(Sciton) / 세대 미확인 — Sciton BBL 실제 제품 · 국내 수입 아이맥 · 현행 장비 허가는 mJoule 21-192 뿐, 본체 모델 · HERO 표시 미확인(D17)', 'D17'),
    'M11-1-4': ('제품 정체 · 인모드 RF 핸드피스 관계 확인(inmode.co.kr · FDA K200947) · 국내 허가번호 연결 미확인(19-352 · 21-205 첨부 구성품)(D17)', 'D17'),
    'auto-M15-1775402654237': ('제품 확인(루메니스코리아 2024-07 국내 출시) · 국내 본체 허가 · 구성 미확인 · 젤 신고는 본체 허가 아님 — 비침습 ≠ 허가 대상 아님(D17)', 'D17'),
    'auto-M4-1775361371619': ('실제 제품(프로스테믹스 제조 · 휴메딕스 국내 공동 판매) · 국내 허가 못 찾음(D22)', 'D22'),
    'new-DEV-020': ('실제 제품 엔파인더스 N-Gine · 국내 허가 못 찾음 — 현장 명판 확인 전(D23 · 10-28 규칙으로 추천 포함)', 'D23'),
    'auto-M4-1775361364993': ('유럽 CE 의료기기 FILLMED NCTF 135HA · 아이더마바이오 국내 독점 수입·유통 보도 · 국내 허가 못 찾음(D20)', 'D20'),
}
for lid, (why, dec) in UNSPEC.items():
    set_status(lid, '허가번호 미확인', why + ' — 10-28 허가번호 미특정 규칙: 「허가번호 미확인」 표시 · 추천 포함', '10-28 허가번호 미특정 규칙')
lid = 'auto-29-1774737181584'
set_co(lid, 'importer', [E('(주)아이맥', 'Sciton 국내 수입사(허가 18-144 · 21-192)', 'https://emedi.mfds.go.kr/search/data/list')], 'D17')
for no, why in [('수허 18-144 호', 'Joule — IPL 미포함(사용목적) · 원장 BBL 이 Joule 본체인지 미확인'), ('수허 21-192 호', 'mJoule — IPL 포함(BBL HERO) · 원장 BBL 이 mJoule 인지 미확인')]:
    add_ref(lid, {'license_no': no, 'holder': '(주)아이맥', 'state': '정상', 'source': 'step1-d17 · step1-d17-2', 'why': why + ' — 연결 안 함'}, 'D17')
line('BBL(Sciton)', lid, [{'name': 'BBL HERO(mJoule)', 'ledger_id': 'auto-31-1774737181584', 'license_no': '수허 21-192 호'},
                          {'name': 'BBL 스킨타이트(이력)', 'ledger_id': 'auto-32-1774737181584'}], 'Sciton · 수입 (주)아이맥',
     basis='JOULE · mJOULE 본체 · BBL 기술 · HERO 세대 · Forever 프로그램(5단계 시술)로 구분 — 사용자 조사 · Sciton 공식 브로슈어(D17)', dec='D17')
row_open(lid, '본체 모델(JOULE · mJOULE) · HERO 표시 · 국내 허가번호 확인 후 시술 연결 — 파장으로 HERO 판정 금지(D17)', 'D17')
lid = 'M11-1-4'
set_co(lid, 'importer', [E('(주)신한네트웍스', 'InMode 수입사(허가 3건) — Morpheus8 판매 근거 없음', 'https://emedi.mfds.go.kr/search/data/list query2=InMode')], 'D17')
for no in ['수허 19-352 호', '수허 21-205 호']:
    add_ref(lid, {'license_no': no, 'holder': '(주)신한네트웍스', 'state': '정상', 'source': 'step1-d17-2', 'why': '첨부 구성품에 Morpheus8 이 드는지 미확인(첨부 내려받기 실패 · 21-205 비공개) — 연결 안 함'}, 'D17')
lid = 'auto-M15-1775402654237'
set_co(lid, 'seller', [E('루메니스코리아(루메니스비코리아 유한회사)', '국내 출시 · 론치 행사', 'https://www.mt.co.kr/thebio/2024/07/18/2024071810574226894', '2024-07')], 'D17')
add_ref(lid, {'license_no': '수신 26-898 호', 'holder': '루메니스비코리아 유한회사', 'official_name': 'Geneo Tripollar Preparation Gel', 'state': '정상', 'source': 'step1-d17', 'why': '소모품(겔) 신고 — 본체 허가 아님'}, 'D17')
row_open(lid, '국내 본체 허가 여부 · 국내 구성(OxyGeneo · LUX · LIFT) 확인 필요 · 미국 Geneo X Elite Class II(K233766)', 'D17')

# D18
lid = 'auto-37-1774737181584'
log('D18', lid, '확인 — 제허 25-78 연결 유지(허가 상세 모델명 CoolSoniq)')
lid = 'auto-M15-1775364775178'  # 헤어셀
add_lic(lid, mk_lic('제인 12-1201 호', '의료기기', '정상', '(주)트리비스', item='의료용전자기발생기', official_name='H-Cell ST', date='2012-09-19',
                    source='식약처 의료기기 품목허가 · step1-d18(헤어셀 S2 = H-cell ST 국내 브랜드)'), 'D18')
set_status(lid, '정상', '제인 12-1201(트리비스 H-Cell ST · 정상) 연결 — 헤어셀(S2)은 H-cell ST 의 국내 브랜드(D18)', 'D18')
set_co(lid, 'manufacturer', [E('(주)트리비스', '제조(허가권자 · 「제」 허가)', '식약처 허가 제인 12-1201')], 'D18')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D18')
sfix('SF-D18-haircell', lid, '설명(원리)', '「LED헬멧」', '미세자기장 헬멧(허가 품목 의료용전자기발생기)', '웹 헤어셀 S2 「미세자기장」 · 허가 H-Cell ST 의료용전자기발생기(D18)', 'D18', 'step1-d18.json')
row_open(lid, '허가 사용목적 「근육통 완화」 — 탈모 사용목적 아님(허가 범위는 5단계에서) · 신제품 헤어셀 Mark1(자기장+레이저·LED) 허가는 찾지 않음', 'D18')
lid = 'new-DEV-069'  # 아톰레이저
add_lic(lid, mk_lic('제허 21-712 호', '의료기기', '정상', '(주)대주메디테크엔지니어링', item='의료용 레이저 조사기', official_name='TINEA외 1건', models=['ATOM Laser'],
                    date='2021-08-24', source='emedi 상세 모델 「ATOM Laser」 · step1-d18'), 'D18')
set_status(lid, '정상', '제허 21-712(대주메디테크 · emedi 모델 ATOM Laser · 발톱 진균증) 연결(D18)', 'D18')
set_co(lid, 'manufacturer', [E('(주)대주메디테크엔지니어링', '제조(허가권자)', '식약처 허가 제허 21-712')], 'D18')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D18')
set_co(lid, 'seller', [E('(주)바디코스', '국내 총판', 'https://www.biotimes.co.kr/news/articleView.html?idxno=34708', '2026-09 보도'),
                       E('(주)메디뷰랩', '제품 소개 · 자사몰(판매 형태 표기 없음)', 'http://medi-beau.com/page/product/atom.html')], 'D18')
conflict(lid, '제조사', '(주)대주메디테크엔지니어링(허가)', '사진 로고 「LCI」', 'step1-d18.json', 'LCI 관계 출처 없음 — 덮어쓰지 않음')
for x in D18['items']:
    if x['verdict'] in ('다름', '확인 불가') and x['ledger_id'] != 'new-DEV-043':
        lid = x['ledger_id']
        set_status(lid, '확인 불가', f'후보 허가와 같은 제품 출처 없음(step1-d18 「{x["verdict"]}」) — D18 사용자 결정 확인 불가', 'D18')
        add_ref(lid, {'license_no': None, 'candidate': x['candidate'], 'source': 'step1-d18', 'why': f'후보 — {x["one_line"]}'}, 'D18')
lid = 'new-DEV-043'  # 오메가라이트
add_hist(lid, {'license_no': '경인 제신 15-332 호', 'kind': '의료기기', 'holder': '(주)오멜론', 'official_name': '오메가라이트외 1건', 'item': '이동형조명기', 'state': '취하', 'date': '2018-11-30', 'source': 'step1-d18'}, 'D18')
add_ref(lid, {'license_no': '제인 16-4726 호 · 경인 제신 13-402 호', 'candidate': '다오닉 「오메가라이트 듀얼」(2020 취하) · 혼콘코리아 「오메가 라이트」(2014 취소)', 'source': 'step1-d18', 'why': '제조 · 허가 업체가 오멜론과 다름 — 같은 제품 출처 없음'}, 'D18')
set_status(lid, '허가 취소(이력)', '오멜론 OMEGA light 허가(경인 제신 15-332) 2018 취하 · 현행 허가 0(D18)', 'D18')
set_co(lid, 'manufacturer', [E('(주)오멜론(O\'melon)', '제조(사진 표기 · 보도 · 공식몰)', 'step1-d18.json')], 'D18')

# D19
x = RES(D19, 'M15-6-4')
lid = 'M15-6-4'
add_lic(lid, mk_lic('제인 16-4317 호', '의료기기', '정상', '(주)엘트라글로벌', item='초음파자극기', official_name='BELLA SONIC 2X', models=['RMVS-1000'],
                    date='2016-04-08', source=f'{EM} meddevItemSeq=2016002383 · 수출용 아님(xprtppYn 아니오)'), 'D19')
add_ref(lid, {'license_no': '제인 17-4558 호', 'holder': '(주)로보맥스', 'official_name': 'RMVS-2000 (BELLA SONIC)', 'state': '정상 · 수출용에 한함', 'source': f'{EM} meddevItemSeq=2017004737', 'why': '수출용에 한함 — 연결 안 함'}, 'D19')
add_ref(lid, {'license_no': '제인 16-4263 호', 'holder': '(주)미젠', 'official_name': 'BELLA SONIC 2X', 'state': '취하 2023-07-14', 'source': 'step1-d19', 'why': '다른 업체 같은 브랜드 — 이 제품 이력인지 출처 없음'}, 'D19')
set_status(lid, '정상', '제인 16-4317 「BELLA SONIC 2X」(엘트라글로벌 · 정상 · 내수) 연결(D19)', 'D19')
set_co(lid, 'manufacturer', [E('(주)엘트라글로벌', '제조(허가권자)', 'http://ltraglobal.com/38 · 식약처 허가 제인 16-4317')], 'D19')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조')], 'D19')
row_open(lid, '허가 브랜드 「2X」와 시판 이름이 같은 모델인지 출처 없음(step1-d19)', 'D19')
for lid in ['auto-M16-1775403024925', 'auto-M10-1775363005172', 'auto-M10-1775363019549', 'auto-M12-1775363026852', 'auto-M8-1775362594611']:
    x = RES(D19, lid)
    set_status(lid, '미허가', f'{x["one_line"]}(D19 사용자 결정 미허가)', 'D19')
for lid in ['new-DEV-071', 'auto-M8-1775362619619', 'auto-M9-1775363058909', 'auto-M16-DCA-1775404043067']:
    x = RES(D19, lid)
    set_status(lid, '확인 불가', f'{x["one_line"]}(D19 사용자 결정 확인 불가)', 'D19')
add_ref('auto-M9-1775363058909', {'license_no': '제허 24-342 호', 'holder': '(주)클래시스', 'official_name': 'QUADESSY', 'state': '정상', 'source': 'step1-d19', 'why': '허가일 · 설명만 겹침 — 같은 제품 출처 없음 · 붙이지 않음(D19)'}, 'D19')
set_co('auto-M16-DCA-1775404043067', 'seller', [E('삼익제약(주)', '허가권자(보도)', 'https://www.hkn24.com/news/articleView.html?idxno=346548', '2025-09 보도')], 'D19')
row_open('auto-M16-DCA-1775404043067', 'KPIC 제품명 검색도 리포린 0(글리포린만) — 보도(2025-08 허가) ↔ 식약처 · KPIC 0 충돌 그대로', 'D19')

# D20
lid = 'auto-20-1774737181584'
set_status(lid, '허가 대상 아님', '인체조직(무세포 동종진피 hADM) — 인체조직법 적용 · 의료기기 품목허가 대상 아님(서울경제 2026-04-02 https://v.daum.net/v/20260402070323518 · D20)', 'D20')
set_co(lid, 'manufacturer', [E('주식회사 도프(DOF Inc.)', '조직은행', 'https://www.koreaclinicguide.com/de/blog/juveacell-korea')], 'D20')
set_co(lid, 'seller', [E('바임글로벌', '출시 주체', 'https://v.daum.net/v/20260402070323518', '2026-04 보도')], 'D20')
lid = 'auto-M4-1775361364993'
set_co(lid, 'manufacturer', [E('Fillmed Laboratories(구 Filorga Medical)', '제조', 'https://www.ddgroup.com/facial-aesthetics/mesotherapy/600706--fillmed-nctf-135ha--ce')], 'D20')
set_co(lid, 'importer', [E('(주)아이더마바이오', '국내 독점 수입·유통(보도) — 이 제품 허가는 없음', 'https://medigatenews.com/news/2391991345', '2019-12 보도')], 'D20')
for lid in ['auto-M15-1775401645338', 'auto-M1-1775360538524', 'auto-M15-1775362958625', 'auto-M4-1775361749536', 'auto-M3-hADM-1775404146754']:
    x = RES(D2031, lid)
    set_status(lid, '확인 불가', f'{x["one_line"]} — D20 사용자 결정 확인 불가', 'D20')
set_co('auto-M15-1775401645338', 'manufacturer', [E('WiQo / GPQ srl', '제조(PRX-T33 · 이탈리아)', 'step1-d20-31.json')], 'D20')
lid = 'auto-M17-1775364775191'  # AAPE
set_status(lid, '허가 대상 아님', '병원용 화장품 앰플(프로스테믹스 · 「병원용 앰플」 데일리안 2019-04-30 https://m.dailian.co.kr/news/view/791757) — 규칙 5 · 사용자 승인(10-28)', '규칙 5 AAPE')
add_hist(lid, {'license_no': '제허 19-756 호', 'kind': '의료기기', 'holder': '(주)프로스테믹스', 'official_name': 'AAPE Progen', 'item': '조직수복용생체재료', 'state': '취하', 'date': '2023-07-31', 'source': 'em.py query2=AAPE · step1-d20-31'}, '규칙 5 AAPE')
idx[lid]['4_license']['history'] = [h for h in idx[lid]['4_license']['history'] if not (norm_no(h['license_no']) == '제허19-756' and h.get('state') == '취소')]
set_co(lid, 'manufacturer', [E('(주)프로스테믹스(PROSTEMICS)', '제조', 'https://m.dailian.co.kr/news/view/791757')], '규칙 5 AAPE')
sfix('SF-AAPE-1', lid, '적응증', '「심부주름 개선」', '병원용 화장품 앰플 설명으로(주름 개선 주입재 AAPE Progen 은 2023 취하)', '적응증 문구만 의료기기 쪽과 겹침(규칙 5)', '10-28 승인 33', 'step1-d20-31.json')
sfix('SF-dabox-1', 'auto-M1-1775360538524', '적응증 글자', '「눈\\ufffd리」(깨진 글자)', '깨진 글자 바로잡기(원문 확인)', '원천 깨진 글자 1건 — _RESUME §1 「원천 수정 목록에 추가할 것」', '_RESUME §1')

# 바넥스 계열(2단계 점검 메모 10-27 · D18 확인 불가)
sfix('SF-vanquish-1', 'auto-M14-1775361047443', '계열 · 설명', 'M14 냉각지방분해 · 설명 「RF+석션」 · 사후관리에 냉각 PAH 문구 섞임', '설명 ↔ 계열 대조 후 바로잡기(2단계)', '자동 추가(auto-) 항목 계열 오배치 의심 — 실제 제품은 확인 불가(D18)', '_RESUME §2 10-27 2단계 메모 · D18', 'step1-d18.json')
sfix('SF-vanquish-2', 'auto-M10-1775361916636', '계열 · 설명', 'M10 · 설명 「RF+EMS+석션」', '설명 ↔ 계열 대조 후 바로잡기(2단계)', '바넥스와 같은 계열 문제 — Vanquish Me 와 기전 다름(D18)', '_RESUME §2 10-27 2단계 메모 · D18', 'step1-d18.json')

# D21 · D24 → 시술 이름
dec_json = J('step1-decisions.json')
DEC = {g['decision_id']: g for g in dec_json['decisions']}
for m in DEC['D21']['members']:
    MOVED[m['ledger_id']] = ('5단계 시술 이름', '실(M7) 메뉴성 이름 — 제품 원장에서 빼고 5단계 단위 시술(메뉴)로(D21)')
for m in DEC['D24']['members']:
    MOVED[m['ledger_id']] = ('5단계 시술 이름', '병원 메뉴명 · 장비 유형 일반명 — 제품 원장에서 빼고 5단계 시술 이름으로(D24)')
MOVED['auto-54-1774737181584'] = ('5단계 시술 이름', '여러 병원이 쓰는 냉각 진정 메뉴 이름 — 장비 이름 아님(D23 추천)')
# 5단계 추가 조사 반영(_RESUME §2 10-29 U8 · U9) — 결정 파일 step1-step5-decisions.json
S5 = J('step1-step5-decisions.json')
for r_ in S5['revive']:   # U8 장비 행 되살림 — moved_to 를 풀고 장비로
    lid = r_['ledger_id']
    MOVED.pop(lid, None)
    idx[lid]['1_identity'] = {'kind': r_['kind'], 'basis': r_['identity_basis'], 'basis_type': 'URL'}
    set_co(lid, 'seller', [E(e['name'], e['role'], e['basis']) for e in r_['seller']], r_['decision'])
    idx[lid]['4_license']['reason'] += ' · ' + r_['license_recheck']
    EXTRA_Q[lid] = r_['origin_question']
    log(r_['decision'], lid, '장비 행 되살림(시술 이름으로 빠짐 철회) — ' + r_['basis'])
for r_ in S5['new_rows']:  # U9 새 제품 행 — 허가 못 찾음 = 확인 불가(1단계 규칙 · 허가 대상 아님 출처 없음)
    row_ = {
        'ledger_id': r_['ledger_id'], 'segment': '결정 반영', 'source': 'decision', 'family': dict(r_['family']),
        '1_identity': {'kind': r_['kind'], 'basis': r_['identity_basis'], 'basis_type': 'URL'},
        '2_names': {'ledger_name': None, 'product_name': r_['display_name'], 'synonyms': [dict(x) for x in r_['synonyms']]},
        '3_line': None,
        '4_license': {'status': '확인 불가', 'kind': None, 'reason': '허가 못 찾음 — ' + r_['license_recheck'], 'licenses': [], 'history': [], 'reference': []},
        '5_spec': None, '6_companies': {'manufacturer': [E('근거 없음', None, '제조사 출처 못 찾음(' + r_['license_recheck'] + ')')],
                                        'importer': [E('근거 없음', None, '허가 없음 · 수입 여부 출처 없음')],
                                        'seller': [E('근거 없음', None, '판매사 출처 없음')],
                                        'license_holder': [], 'other': [], 'conflicts': []},
        '7_site_use': None, 'gate': None, 'change_vs_draft': None,
        'note': f"taxonomy 항목 {r_['source_item']} 의 정체로 밝힌 장비 — 5단계 단위 시술은 그 항목 이름을 동의어로 둔다({r_['decision']})",
        'evidence': ['step5-research2.json identities 파셀라 메디컬 경락'], 'open': [],
    }
    items.append(row_); idx[row_['ledger_id']] = row_
    EXTRA_Q[row_['ledger_id']] = r_['origin_question']
    log(r_['decision'], row_['ledger_id'], f"새 행 — {r_['display_name']}({r_['product_name']}) · 허가 못 찾음 → 확인 불가")
add_hist('auto-M15-1775360919010', {'license_no': '제인 05-914 호', 'kind': '의료기기', 'holder': '(주)현대메디텍', 'official_name': 'Meso Pri', 'item': '의약품직접주입기구', 'state': '만료(유효기간)', 'date': '2026-01-01', 'source': 'em.py query2=Meso-Pri · step1-d20-31'}, 'D31')

# D22 · D23 확인 불가 유지(원천 질문)
for g in ('D22', 'D23'):
    for m in DEC[g]['members']:
        lid = m['ledger_id']
        if lid in MOVED or lid in UNSPEC:
            continue
        set_status(lid, '확인 불가', f'식약처 · emedi · 웹 근거 0 — 원천 확인 전까지 보류({g} 추천 · 사용자 승인 10-28)', g)
        log(g, lid, '확인 불가 유지 · 원천 질문으로')
# D26 현장 기기 35 = 원장 행
for m in DEC['D26']['members']:
    log('D26', m['ledger_id'], '현장 기기 → 제품 원장 행 확정(진단 장비 4 는 kind 「진단 장비」)')
for lic in RES(D2031, 'auto-M9-1775364775137')['license_found']:
    add_ref('auto-M9-1775364775137', {'license_no': lic['no'], 'holder': lic['holder'], 'official_name': lic['model'], 'state': lic['state'], 'source': lic['query'], 'why': '후보 둘(위로 Apollo · Pollogen Apollo) — 원천 확인 전 연결 안 함'}, 'D23')
set_co('new-DEV-020', 'manufacturer', [E('엔파인더스(주)(N-Finders Co., Ltd.)', '제조(N-Gine)', 'https://nfinders.com/eng/product_n-gine/')], 'D23')
row_open('new-DEV-020', '현장 명판이 엔파인더스 「N-Gine」인지 직접 확인(사용자 · 직접 확인 7)', 'D23')

# D25 받기 29 + 갱신
for m in DEC['D25']['members']:
    log('D25', m['ledger_id'], '받기(초안 대비 바뀐 연결 확정)')
lid = 'M2-2-4'  # 테오시알
for no in ['수허 18-330 호', '수허 18-329 호']:
    add_hist(lid, {'license_no': no, 'kind': '의료기기', 'holder': None, 'official_name': 'TEOSYAL RHA', 'state': '취하', 'date': '2026-05-13', 'source': f'{EL} query2=Teosyal · step1-d20-31'}, 'D25')
for h in idx[lid]['4_license']['history']:
    if norm_no(h['license_no']) == '수허20-225':
        h['state'] = '만료(유효기간)'; h['date_note'] = '2025-11-03'
        log('D25', lid, '수허 20-225 이력 상태 취소 → 만료(유효기간)')
sfix('SF-D25-tune', 'auto-M9-1775360627229', '원장 업체', '클래시스', '알마(수입 알마코리아 · 수허 17-350)', '원천 taxonomy 업체 표기 틀림(D25 추천)', 'D25', 'step1-d20-31.json')
row_open('auto-M2-1775361463441', '15-1616 Cutegel Hydro 가 큐젤 라인 품목인지 따로 확인(D25 추천 메모)', 'D25')
row_open('M11-1-3', '24-257 「X PRO」를 실펌X 품목으로 둘지 — 라인+품목 규칙(D25 추천 메모)', 'D25')

# 취소(이력) 재조사 — 현재 허가 복귀
for x in CR['items']:
    if x['result'] == '현재 허가 있음' and x['ledger_id'] != 'M1-P-8':
        c = x['current_license'][0]
        lid = x['ledger_id']
        if lid != 'auto-M8-1775362612108':   # 젠틀맥스프로는 D11 에서
            add_lic(lid, mk_lic(c['no'], '의료기기', '정상', c['entp'].replace('(수입)', ''), official_name=c['name'], models=[m.strip() for m in c.get('model', '').split('·')],
                                manufacturer=c.get('manuf'), date=c['state'], source=c['src']), '취소 재조사')
            set_status(lid, '정상', f'현재 허가 {c["no"]}(정상) 복귀 — 옛 허가만 취하(취소 재조사 · D25)', '취소 재조사')
            set_co(lid, 'importer', [E('시너론켄델라코리아 유한회사', '수입(허가권자)', c['src'])], '취소 재조사')
            if c.get('manuf'):
                set_co(lid, 'manufacturer', [E(c['manuf'], '제조원', c['src'])], '취소 재조사')
            set_co(lid, 'seller', [E(s['name'], s['role'], s['url']) for s in x['sellers'] if s['name'] != '근거 없음'], '취소 재조사')
add_hist('auto-M8-1775362912344', {'license_no': '수허 99-1506 호', 'kind': '의료기기', 'holder': '(주)신한씨스텍', 'state': '취하', 'date': '2019-11-28', 'source': 'step1-cancel-recheck'}, '취소 재조사')
row_open('auto-M8-1775362912344', '허가는 있으나 국내 현재 유통 웹 근거 없음(step1-cancel-recheck)', '취소 재조사')
# 타임버스 = 티엠버스주
lid = 'M1-P-8'
for k in KPIC['items']:
    if k['ledger_id'] == lid and k['license_no'] is None:
        for h in k['hits']:
            add_lic(lid, mk_lic(h['kfda_code'], '의약품', '정상', '(주)종근당바이오', item=h['drug_class'] + '의약품', official_name=h['drug_name'],
                                manufacturer='(주)종근당바이오', date=h['permit_date'], source=f'KPIC drugcode {h["drug_code"]} · 식약처 품목기준코드 {h["kfda_code"]}',
                                official_name_en=h['drug_enm']), '10-28 타임버스')
for h in idx[lid]['4_license']['history']:
    if norm_no(h['license_no']) == '202301026':
        h['note'] = '타임버스엘주(수출용) — 2024-02-01 취소(KPIC)'
set_status(lid, '정상', '티엠버스주 100 · 200단위(종근당바이오 · 2025-03-31 · 2025-09-16) 연결 — 사용자 결정 10-28 「타임버스 = 티엠버스주」', '10-28 타임버스')
NAME_OVERRIDE[lid] = ('티엠버스', '국내 허가 「티엠버스주」(종근당바이오) · 원장 「타임버스」는 검색 이름(10-28)')
EXTRA_SEARCH[lid] += [('TYEMVERS', '허가 영문명')]
set_co(lid, 'manufacturer', [E('(주)종근당바이오', '제조(허가권자)', 'KPIC drugcode 2025040100014 · 2025091700003')], '10-28 타임버스')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 의약품')], '10-28 타임버스')
# 라라젯
for lid in ['auto-48-1774737181584']:
    L = idx[lid]['4_license']
    L['reason'] = '의료기기 허가(제인 18-4662 다오닉) 2024-09-30 취하 · 현재 유통(2026-09 보도) · 비의료기기 여부 미확인 — 추천 제외(D13 정정 · 10-27)'
    set_co(lid, 'seller', [E('(주)에이치투메디', '기기 공급(공급사 · 무상 사후관리)', 'https://www.socialvalue.kr/news/view/1065576656108660'),
                           E('비즈마켓렌탈', '유통 · 판매채널(렌탈)', 'https://www.socialvalue.kr/news/view/1065576656108660'),
                           E('펜타르코', '구조화 · 채널 전략', 'https://www.socialvalue.kr/news/view/1065576656108660')], 'D13')
    row_open(lid, '미용기기 전환은 사용자 추정 — 비의료기기 출처 나오면 「허가 대상 아님」 검토(직접 확인 7)', 'D13')
for lid, cand in [('auto-32-1774737181584', 'Joule 플랫폼 수허 18-144 안인지'), ('auto-M8-1775361417735', '같은 수입사 elos Plus 수허 15-1663 인지')]:
    x = RES(CR, lid)
    for c in x['candidates']:
        add_ref(lid, {'license_no': c['no'], 'holder': c['entp'], 'official_name': c['name'], 'state': c['state'], 'source': c['src'], 'why': f'후보 — {cand} 출처 없음 · 연결 안 함'}, '취소 재조사')
    row_open(lid, f'허가 취소(이력) 유지 — {cand}는 직접 확인 7 에 남김', '취소 재조사')

# 규칙 5
lid = 'M8-4-1'  # 브이빔 라인
add_lic(lid, mk_lic('수허 21-34 호', '의료기기', '정상', '시너론켄델라코리아 유한회사', official_name='Vbeam Prima Basic', models=['9914-00-9081'], date='2021-02-02',
                    source='https://emedi.mfds.go.kr/search/data/list query2=Vbeam · step1-cancel-recheck'), '규칙 5 브이빔')
add_lic(lid, lic_from_row('auto-M8-1775364775121', '수허 18-276 호'), '규칙 5 브이빔')
set_status(lid, '정상', '브이빔 = 라인 · 품목 Perfecta(수허 18-276) · Prima(수허 21-34) · 옛 Vbeam(00-1160) 이력 — 규칙 5 사용자 승인(10-28)', '규칙 5 브이빔')
set_co(lid, 'importer', [E('시너론켄델라코리아 유한회사', '수입(허가권자)', '식약처 허가 수허 18-276 · 21-34')], '규칙 5 브이빔')
set_co(lid, 'seller', [E('시너론켄델라코리아 유한회사(시너론-켄델라 코리아)', '2018-10-01부터 한국 직접 판매(수입사와 같은 회사)', 'https://www.dt.co.kr/article/11193561')], '규칙 5 브이빔')
add_ref(lid, {'license_no': '수허 20-108 호', 'holder': '시너론켄델라코리아 유한회사', 'official_name': '9914-00-9084', 'state': '취하 2025-03-12', 'source': 'step1-cancel-recheck', 'why': '후속 모델 취하 — 이력 참고'}, '규칙 5 브이빔')
line('브이빔', lid, [{'name': 'Vbeam Perfecta', 'license_no': '수허 18-276 호', 'ledger_id': 'auto-M8-1775364775121'}, {'name': 'Vbeam Prima', 'license_no': '수허 21-34 호'}],
     '시너론켄델라코리아(수입) · Candela', dec='규칙 5')
lid = 'M15-2-2'  # 하이드라페이셜 허가 2
add_lic(lid, mk_lic('수허 18-215 호', '의료기기', '정상', '(주)인터엠디', official_name='HydraFacial MD ELITE', models=['70290-03-01-KOR'], manufacturer='Hydrafacial, LLC.',
                    source=f'{EL} query2=HydraFacial · step1-d20-31'), '규칙 5 하이드라페이셜')
add_hist(lid, {'license_no': '수허 18-283 호', 'kind': '의료기기', 'holder': '(주)제이스메디컬', 'state': '취소', 'date': '2023-01-13', 'source': f'{EL} query2=HydraFacial'}, '규칙 5 하이드라페이셜')
set_co(lid, 'importer', [E('주식회사메디뷰랩', '수입(허가권자)', '식약처 허가 수허 22-213'), E('(주)인터엠디', '수입(허가권자)', 'emedi 수허 18-215')], '규칙 5 하이드라페이셜')
set_co(lid, 'manufacturer', [E('Hydrafacial, LLC.', '제조원', '식약처 허가 수허 22-213 · 18-215')], '규칙 5 하이드라페이셜')
lid = 'auto-M4-1775361378128'  # 바이리즌 라인
add_lic(lid, lic_from_row('M4-1-7', '제허23-784호'), '규칙 5 바이리즌')
set_co(lid, 'manufacturer', [E('(주)아크로스', '제조(HA · 제허 20-527)', '식약처 허가 제허 20-527'), E('(주)비알팜', '제조(PN · 제허 23-784)', '식약처 허가 제허 23-784')], '규칙 5 바이리즌')
line('바이리즌', lid, [{'name': 'BYRYZN Skinbooster HA', 'license_no': '제허20-527호'}, {'name': 'BYRYZN PN(바이리즌 피엔)', 'license_no': '제허23-784호'}],
     '휴젤 브랜드(제조 아크로스 · 비알팜)', basis='라인 = 상위 제품 규칙 · 휴젤 브랜드(규칙 5)', dec='규칙 5')
set_status(lid, '정상', '바이리즌 = 라인 · 품목 HA(20-527) · PN(23-784) — 규칙 5 사용자 승인(10-28)', '규칙 5 바이리즌')

# D27 사용목적 불일치 — 연결 안 함 유지
for m in DEC['D27']['members']:
    lid = m['ledger_id']
    um = idx[lid].get('use_mismatch')
    if um:
        add_ref(lid, {'license_no': ' · '.join(re.findall(r'제허\s?\d+-\d+호', um)), 'source': 'step1-products v1 use_mismatch', 'why': '사용목적 불일치 — 연결 안 함(D27)'}, 'D27')
    log('D27', lid, '사용목적 불일치 허가 연결 안 함 확정')

# D28 유지
for lid in ['auto-M2-1775364775109', 'M4-1-7']:
    log('D28', lid, '유지(허가 제품명 · 모델명에 이름 직접 있음)')
    idx[lid].pop('weak_link', None)

# D29 taxonomy
lid = 'M1-P-9'  # 뉴럭스
idx[lid]['6_companies']['license_holder'] = [E('(주)뉴메코', '허가권자', '식약처 의약품 허가 202302604 · 202601737')]
set_co(lid, 'manufacturer', [E('(주)메디톡스', '위탁 제조원', '의약품 허가 CNSGN_MANUF')], 'D29')
EXTRA_SEARCH[lid] += [('NEWLUX', '허가 영문명(D29 — 「Neurox」 대신)')]
idx[lid]['2_names']['synonyms'] = [s for s in idx[lid]['2_names'].get('synonyms', []) if s['name'] != 'Neurox']
log('D29', lid, '검색 이름 Neurox → NEWLUX · 허가권자 뉴메코 / 제조 메디톡스 칸 분리')
lid = 'M5-P-1'  # 리젠ACR
for h in RES(D2031, lid)['license_history']:
    add_hist(lid, {'license_no': h['no'], 'kind': '의료기기', 'holder': h['holder'], 'official_name': h['model'], 'state': h['state'], 'date': h['date'], 'source': h['query']}, 'D29')
set_status(lid, '허가 취소(이력)', '국내 현행 허가 없음 — 리젠코리아 Regen ACR-C 신고 2011 취하 등 이력만(D29)', 'D29')
set_co(lid, 'manufacturer', [E('REGEN LAB SA(스위스)', '제조 · 상표권자(「RegenACR® … REGEN LAB SA」)', 'https://www.regenlab.com/patents/')], 'D29')
sfix('SF-D29-regen', lid, '업체', '리젠바이오텍', 'REGEN LAB SA(국내 이력 리젠코리아)', 'taxonomy 업체 「리젠바이오텍」 틀림 — 리젠바이오텍 허가 5건에 ACR 없음(D29)', 'D29', 'step1-d20-31.json')
lid = 'M8-P-1'  # 피코웨이
set_co(lid, 'importer', [E('시너론켄델라코리아 유한회사', '수입(허가권자)', '식약처 허가 수허 18-304')], 'D29')
set_co(lid, 'manufacturer', [E('NPA de Mexico S. de R.L. de C.V.', '제조원', '식약처 허가 수허 18-304')], 'D29')
set_co(lid, 'other', [E('Candela(캔델라)', '브랜드', 'https://practicaldermatology.com/news/20141008-syneron_launches_picoway_picosecond_device_for_pigmented_lesion_treatment_and_tattoo_removal/2459094/')], 'D29')
for h in idx[lid]['4_license']['history']:
    if norm_no(h['license_no']) == '수허15-1312':
        h['state'] = '취하'; log('D29', lid, '수허 15-1312 이력 상태 취소 → 취하(emedi)')
lid = 'M11-P-1'  # 인트라셀
for l in RES(D2031, lid)['license_found']:
    for no in l['no'].split(' · '):
        add_lic(lid, mk_lic(no, '의료기기', '정상', l['holder'], official_name=l['model'], date=l['date'], source=l['query']), 'D29')
for h in RES(D2031, lid)['license_history']:
    add_hist(lid, {'license_no': h['no'], 'kind': '의료기기', 'holder': h['holder'], 'official_name': h['model'], 'state': h['state'], 'date': h['date'], 'source': h['query']}, 'D29')
set_status(lid, '정상', 'INTRAcel 계열 현행 허가(대표 제허 17-689 INTRAcel PRO · 제이시스메디칼) — D29', 'D29')
set_co(lid, 'manufacturer', [E('(주)제이시스메디칼', '제조(허가권자)', '식약처 허가 제허 17-689 등')], 'D29')
set_co(lid, 'importer', [E('해당 없음', None, '국내 제조 허가(「제」)')], 'D29')
for m in DEC['D29']['members']:
    lid = m['ledger_id']
    if idx[lid]['4_license']['status'] == '확인 불가' and lid not in MERGED:
        log('D29', lid, '확인 불가 유지 · 원천 질문')

# D30
EXTRA_SEARCH['M8-2-4'] += [('프락셀', 'taxonomy M8-P-5 이름 — 수허 10-500 제품명 「프락셀, 프락셀 듀얼」(D30)')]
# D31
lid = 'auto-M15-1775360904089'
set_status(lid, '확인 불가', '같은 회사(바즈바이오메딕) 미용 적응증 분사식주사기 허가 CRJ-001CD(정상)가 있어 「허가 대상 아님」으로 닫을 수 없음 — 원천 질문(D31)', 'D31')
add_ref(lid, {'license_no': None, 'candidate': '바즈바이오메딕 CRJ-001CD(제품명 공란 · 정상)', 'source': 'step1-d20-31', 'why': '노보젯 모델인지 출처 없음 — 연결 안 함'}, 'D31')
set_co(lid, 'manufacturer', [E('바즈바이오메딕 주식회사', '제조', 'step1-d20-31.json')], 'D31')
lid = 'new-DEV-049'
idx[lid]['4_license']['reason'] = '「…미용기기이다」 — 스포츠서울 2019 기사 인용(제조사 자료 아님) · 트리시스 의료기기 허가에 없음(D31)'
log('D31', lid, '허가 대상 아님 확정 · 근거를 2019 기사 인용으로 교체')
lid = 'new-DEV-034'
set_co(lid, 'seller', [E('(주)벨레브(브랜드 벨루미에)', '판매(벨루미에몰)', 'step1-d20-31.json')], 'D31')
log('D31', lid, '확인 불가 유지 — 실물 라벨 · 판매처 문의')

# D32 의약품 3 새 행
def kp(lid):
    return [k for k in KPIC['items'] if k['ledger_id'] == lid and k['license_no'] is None][0]


def drug_row(lid, ledger_name, fam, licenses, status, reason, mf, note, refs=()):
    r = {'ledger_id': lid, 'segment': 'D32(분류표 · 원장 밖)', 'source': 'taxonomy_unit', 'family': {'code': fam, 'name': fam},
         '1_identity': {'kind': '제품(의약품)', 'basis': 'D32 사용자 결정 — 분류표 other · 단위 시술 행 안의 의약품 브랜드 · KPIC 조회', 'basis_type': '사용자 결정'},
         '2_names': {'ledger_name': ledger_name, 'product_name': None, 'synonyms': [{'name': ledger_name, 'type': '분류표 이름'}]},
         '3_line': None, '4_license': {'status': status, 'kind': '의약품', 'reason': reason, 'licenses': licenses, 'history': [], 'reference': list(refs)},
         '5_spec': None, '6_companies': {'manufacturer': mf, 'importer': [E('해당 없음', None, '국내 제조 의약품')] if licenses else [E('근거 없음', None, '허가 없음')],
                                         'seller': [E('근거 없음', None, '판매사 출처 없음')], 'license_holder': [], 'other': [], 'conflicts': []},
         '7_site_use': None, 'gate': None, 'change_vs_draft': None, 'note': note, 'evidence': [], 'open': []}
    items.append(r); idx[lid] = r
    log('D32', lid, f'새 행 — {ledger_name} · {status}')


def kp_lic(h, holder):
    return mk_lic(h['kfda_code'], '의약품', '정상', holder, item=f'{h["drug_class"]}의약품 · {h["cls"]}', official_name=h['drug_name'], official_name_en=h['drug_enm'],
                  date=h['permit_date'], source=f'KPIC drugcode {h["drug_code"]} · 식약처 품목기준코드 {h["kfda_code"]}')


k = kp('auto-M15-1775364775171')
drug_row('auto-M15-1775364775171', '컨트라투벡스', 'M15', [kp_lic(h, '메디팁') for h in k['hits']], '정상',
         '콘투락투벡스겔(메디팁 · 2001-04-06) — KPIC 제품명 검색(D32)', [E('메디팁', '허가권자(KPIC 업체)', 'KPIC drugcode A11AOOOOO9487')], '원장 이름 「컨트라투벡스」 → 허가 「콘투락투벡스겔」')
NAME_OVERRIDE['auto-M15-1775364775171'] = ('콘투락투벡스', '허가 「콘투락투벡스겔」(메디팁) — 원장 「컨트라투벡스」는 검색 이름(D32)')
EXTRA_SEARCH['auto-M15-1775364775171'] += [('Contractubex', 'KPIC 영문명')]
sfix('SF-D32-contra', 'auto-M15-1775364775171', '제품 이름', '컨트라투벡스', '콘투락투벡스겔(메디팁)', '식약처 · KPIC 한글 표기(D32)', 'D32', 'KPIC drugcode A11AOOOOO9487')
k = kp('M16-3-1')
dom = [h for h in k['hits'] if h['drug_name'].startswith('라이넥주')]
exp = [h for h in k['hits'] if '수출용' in h['drug_name']]
drug_row('M16-3-1', '라엔넥', 'M16', [kp_lic(h, '녹십자웰빙') for h in dom], '정상',
         '라이넥주 · 라이넥주바이알(녹십자웰빙) — 같은 성분 · 함량(Human Placenta Hydrolysate 1mL/mL)이라 한 제품(10-27 규칙) · KPIC(D32)',
         [E('녹십자웰빙', '허가권자(KPIC 업체)', 'KPIC drugcode A11AOOOOO6804')], '원장 이름 「라엔넥」 → 허가 「라이넥주」',
         refs=[{'license_no': h['kfda_code'], 'official_name': h['drug_name'], 'state': f'취소 {h["cancel_date"]}', 'source': f'KPIC drugcode {h["drug_code"]}', 'why': f'취소({h["cancel_date"]}) · KPIC 제품명 「수출용」 표기 — 연결 안 함'} for h in exp])
NAME_OVERRIDE['M16-3-1'] = ('라이넥', '허가 「라이넥주」(녹십자웰빙) — 원장 「라엔넥」은 검색 이름(D32)')
EXTRA_SEARCH['M16-3-1'] += [('Laennec', 'KPIC 영문명')]
sfix('SF-D32-laennec', 'M16-3-1', '제품 이름', '라엔넥', '라이넥주(녹십자웰빙)', '식약처 · KPIC 한글 표기(D32)', 'D32', 'KPIC drugcode A11AOOOOO6804')
row_open('M16-3-1', '허가 적응증 「만성 간질환 간기능 개선」 — 미용 적응증 없음(KPIC) · 시술 쓰임은 5단계', 'D32')
row_open('M16-3-1', '라이넥주바이알(201100874)을 같은 제품 규격으로 묶음 — 10-27 「같은 성분 · 용량만 다른 허가는 한 제품」 적용', 'D32')
drug_row('auto-M15-1775361951923', '아큐탄', 'M15', [], '확인 불가',
         'KPIC 제품명 검색 아큐탄 · 로아큐탄 · Roaccutane 0(오리지널 국내 미유통) · 같은 성분 이소트레티노인 국내 제품 49건(NOTES 10-28) — 이름만으로 어느 제품인지 특정 못 함(D32)',
         [E('근거 없음', None, '국내 허가 없음')], '이소트레티노인 브랜드(분류표)')
row_open('auto-M15-1775361951923', '「미허가」(오리지널 국내 미유통)로 둘지, 병원이 「아큐탄」으로 부르는 국내 이소트레티노인 제품을 붙일지 사용자 판단', 'D32')

# 의약품 행 KPIC 보강(규칙 7)
for k in KPIC['items']:
    if k['license_no'] is None:
        continue
    lid = k['ledger_id']
    for l in idx[lid]['4_license']['licenses'] + idx[lid]['4_license']['history'] + idx[lid]['4_license']['reference']:
        if norm_no(l.get('license_no')) == norm_no(k['license_no']) and k['hits']:
            h = k['hits'][0]
            l['kpic'] = {'drug_code': h['drug_code'], 'drug_name': h['drug_name'], 'ingredient': h['ingredient'], 'company': h['company'],
                         'class': h['cls'], 'atc': h['atc'], 'kpic_class': h['kpic_atc'], 'insurance': h['boh'], 'hira_code': h['boh_hiracode'],
                         'insurance_code_search': h['boh_code_search'], 'source': f'KPIC drugcode {h["drug_code"]}'}
for lid in [k['ledger_id'] for k in KPIC['items'] if k['license_no'] is None and k['hits']]:
    for l in idx[lid]['4_license']['licenses'] + idx[lid]['4_license']['reference']:
        for k in KPIC['items']:
            if k['ledger_id'] == lid:
                for h in k['hits']:
                    if str(h['kfda_code']) == str(l.get('license_no')):
                        l['kpic'] = {'drug_code': h['drug_code'], 'drug_name': h['drug_name'], 'ingredient': h['ingredient'], 'company': h['company'],
                                     'class': h['cls'], 'atc': h['atc'], 'kpic_class': h['kpic_atc'], 'insurance': h['boh'], 'hira_code': h['boh_hiracode'],
                                     'insurance_code_search': h['boh_code_search'], 'source': f'KPIC drugcode {h["drug_code"]}'}
n_kpic = sum(1 for it in items for l in it['4_license']['licenses'] + it['4_license']['history'] + it['4_license']['reference'] if l.get('kpic'))
LOG.append({'decision': '규칙 7 KPIC', 'ledger_id': '(의약품 행 전체)', 'name': '', 'change': f'의약품 허가 {n_kpic}건에 성분 · 업체 · 식약처 분류 · ATC · KPIC 약효 · 보험(급여가 · 심평원 코드/비급여) 보강'})
for k in KPIC['items']:
    if k['license_no'] is None and k['ledger_id'] in ('auto-M16-1775403024925',):
        row_open(k['ledger_id'], 'KPIC 제품명 검색 벨카이라 0 · 데옥시콜산 성분 제품 11건에도 없음 — 미허가 그대로', '규칙 7 KPIC')

# 더톡신 수출용 의약품(KPIC 제품명 「(수출용)」)은 0-1 에서 EXPORT 로 처리됨


export_filter(' — 결정으로 붙인 허가')
# 인트라셀: 본체 허가 6건이 수출용 → 남은 국내 허가는 일회용 팁(제인 09-1033)뿐. 소모품은 본체 허가 아님(D17 제네오X 「젤 신고는 본체 허가 아님」)
if [norm_no(l['license_no']) for l in idx['M11-P-1']['4_license']['licenses']] == ['제인09-1033']:
    unlink_to_ref('M11-P-1', '일회용 전극 팁(소모품) — 본체 허가 아님(D17 「젤 신고는 본체 허가 아님」과 같은 기준)', '규칙 1 수출용')
    row_open('M11-P-1', 'INTRAcel 본체 허가 6건이 전부 수출용 — 국내 본체 허가 없음 · 남은 국내 허가는 팁뿐이라 연결 안 함. D29 「현행 허가 찾음」과 달라짐 — 사용자 확인', '규칙 1 수출용')
# ── 수출용 재판정(코디 반려 10-28): 수출 전용 허가만 남은 행 → 같은 업체 · 같은 브랜드 내수 허가(xprtppYn 아니오 · 정상 · 이름이 제품명/모델명에 있음) 연결
RC = RECHECK['candidates']
def rc(lid, no):
    c = [x for x in RC[lid] if norm_no(x['license_no']) == norm_no(no)][0]
    assert c['xprtppYn'] == '아니오', (lid, no)
    return c
def rc_lic(lid, no, holder=None):
    c = rc(lid, no)
    return mk_lic(c['license_no_detail'], '의료기기', '정상' if c['cancel'] == '아니오' else '취하', holder or c['entp'], item=c['item'], official_name=c['product_names'] or c['brand_detail'],
                  models=c['models'], date=c['permit_date'], source=c['source'] + ' · xprtppYn 아니오(내수)')
DOM = [('M9-1-3', ['제허14-1422호'], 'SHURINK · SHURINK-A 모델'), ('M9-1-5', ['제허11-946호', '제허21-690호'], 'DOUBLO Lifting(모델 DOUBLO · DOUBLO-S) · NEW DOUBLO'),
       ('auto-M9-1775364775134', ['제허11-946호', '제허21-690호'], '더블로 라인 내수 허가(품목 미정)'), ('M2-1-1', ['제허13-871호', '제허14-2923호'], 'Neuramis Deep · Neuramis lidocaine 계열'),
       ('M11-1-2', ['제허11-1071호'], '제품명 Secret RF'), ('auto-39-1774737181584', ['제허22-679호'], '10THERMA 본체')]
for lid, nos, why in DOM:
    src_lid = 'M9-1-5' if lid == 'auto-M9-1775364775134' else lid
    for no in nos:
        add_lic(lid, rc_lic(src_lid, no), '수출용 재판정')
    set_status(lid, '정상', f'수출 전용 허가 대신 같은 업체 내수 허가 연결 — {why}(규칙 A: 이름 + 업체 일치 · 수출용 재판정 10-28) · 코디 승인(검수 v3 G1 · _RESUME §2 10-28 — 정상만 연결 · 수출용 규칙의 직접 귀결 · 같은 업체 · 이름 일치)', '수출용 재판정')
    idx[lid]['4_license']['approval'] = {'by': '코디', 'date': '2026-10-28', 'basis': '검수 v3 G1 승인 — 정상 · 내수 허가만 연결 · 수출용 규칙의 직접 귀결 · 같은 업체 · 이름 일치(_RESUME §2 10-28)'}
    log('검수 v3', lid, 'G1 승인 — 내수 허가 연결 그대로 정상 · 추천 · open 「사용자 확인」 지움 · 승인 근거 기록')
row_open('M2-1-1', '제허 14-2923 은 아띠에르(M2-1-6) 행과 같은 허가(제품명에 Neuramis · 아띠에르 둘 다) — 라인+품목 여부 판단', '수출용 재판정')
idx['M9-1-5']['shared_license_with'] = sorted(set((idx['M9-1-5'].get('shared_license_with') or []) + ['auto-M9-1775364775134']))
LINES['더블로']['items'] = [{'license_no': '제허11-946호', 'name': 'DOUBLO Lifting(DOUBLO · ULTRA VERA · DOUBLO-S)'}, {'license_no': '제허21-690호', 'name': 'NEW DOUBLO · V-RO'}]
LINES['더블로']['note'] = '10-27 라인 허가 3건(11-238 · 13-291 · 18-195)은 「수출용에 한함」 — 내수 허가 11-946 · 21-690 으로 교체(수출용 재판정)'
log('수출용 재판정', 'auto-M9-1775364775134', '라인 「더블로」 품목을 내수 허가 11-946 · 21-690 으로 교체')
add_hist('auto-M11-1775361447933', mk_lic('제허 14-1620 호', '의료기기', '취하', '(주)쉬엔비', models=['VIVACE'], date='2024-01-25(취하)', source=rc('auto-M11-1775361447933', '제허14-1620호')['source'] + ' · 내수'), '수출용 재판정')
set_status('auto-M11-1775361447933', '허가 취소(이력)', '현행 VIVACE · VIVACE PRO 허가는 「수출용에 한함」 · 내수 허가 14-1620 은 2024-01-25 취하(수출용 재판정)', '수출용 재판정')
row_open('auto-M11-1775361447933', '결정에 없는 상태 변경 — 정상 → 허가 취소(이력): 현행 VIVACE 24-117 · VIVACE PRO 25-404 가 「수출용에 한함」 · 내수 14-1620 은 2024-01-25 취하(수출용 규칙 적용 · 검수 v3 G2)', '검수 v3')
log('검수 v3', 'auto-M11-1775361447933', 'G2 — open 에 상태 변경 사유 기록')
row_open('M9-1-10', 'D02 결정은 「19-237 · 20-492 연결」 — 19-237 이 「수출용에 한함」이라 참고로 내리고 20-492 만 연결(수출용 규칙 우선 · 결정과 달라짐 · 검수 v3 F1)', '검수 v3')
log('검수 v3', 'M9-1-10', 'F1 — open 에 D02 와 달라진 사유 기록')
for lid in ['auto-M7-1775361076707', 'auto-M7-1775362571755', 'auto-M8-1775364775119', 'new-DEV-039', 'M3-3-2', 'M11-P-1', 'M9-1-6']:
    log('수출용 재판정', lid, '같은 업체 · 같은 브랜드 허가가 전부 「수출용에 한함」(또는 팁 소모품뿐) — 내수 허가 없음 확인')
# ── 1단계 마지막 반영(_RESUME §2 10-28 마지막 행) ① domestic7
D7 = {r['ledger_id']: r for r in J('step1-domestic7.json')['rows']}
def d7_lic(lid):
    x = D7[lid]['domestic_license'][0]
    return mk_lic(x['license_no'], '의료기기', '정상', D7[lid]['company'], item=x['item'], official_name=x.get('product_names') or x.get('brand'),
                  models=x.get('models') or [], date=x['permit_date'], source=x['source'] + ' · xprtppYn 아니오(내수)', valid=x.get('valid'))
for lid, why in [('M3-3-2', '제허 25-634 「G.O.U.R.I.」(덱스레보 · 내수 · 정상) — 제품명 표기만 점 차이'), ('M9-1-6', '제허 11-946 모델 목록에 DOUBLO-GOLD(하이로닉 · 내수 · 정상)'),
                 ('auto-M7-1775361076707', '제허 13-1507 제품명에 JAMBER 계열(네오닥터 · 내수 · 정상)')]:
    add_lic(lid, d7_lic(lid), '마지막 반영 domestic7')
    set_status(lid, '정상', f'{why} 연결 — 사용자 결정(_RESUME §2 10-28 마지막 행 · step1-domestic7)', '마지막 반영 domestic7')
idx['M3-3-2']['6_companies']['seller'] = [E('근거 없음', None, '판매사 출처 없음 — 국내 유통은 병원 이벤트로 확인(데이뷰의원 안양범계점 https://daybeauclinic06.com/branch/event.php?uid=1327)')]
EXTRA_SEARCH['M3-3-2'] += [('G.O.U.R.I.', '내수 허가 제허 25-634 제품명 표기')]
lid = 'auto-M7-1775362571755'
set_status(lid, '허가번호 미확인', '국내 유통 확인(평촌고운세상피부과의원 비급여 고지 「N-COG」 https://pcgowoonss.com/data/editor/2603/78448188b39c1e09e49755ce5e148c59_1773644563_533.png · 메디게이트뉴스 2015 「엔파인더스의 엔코그」 https://medigatenews.com/news/3272101004) · 이름 든 허가는 수출용 17-914 뿐 · 내수 13-2038 · 14-152 는 제품명 칸이 비어 특정 못 함 — 허가번호 미특정 규칙(사용자 10-28)', '마지막 반영 domestic7')
for c in D7[lid]['candidates_not_linked']:
    add_ref(lid, {'license_no': c['license_no'], 'item': c['item'], 'state': '정상 · 내수', 'source': c['source'], 'why': '같은 업체 내수 PDO 허가 — 제품명 칸이 비어 N-Cog 인지 근거 없음 · 연결 안 함'}, '마지막 반영 domestic7')
set_co(lid, 'manufacturer', [E('엔파인더스(주)', '제조', 'https://medigatenews.com/news/3272101004')], '마지막 반영 domestic7')
lid = 'M11-P-1'
for h in idx[lid]['4_license']['history']:
    if norm_no(h['license_no']) == '제허09-682':
        h['state'] = '만료(유효기간)'; h['note'] = '내수(xprtppYn 아니오) · 유효 2020-10-08 ~ 2026-08-31(step1-domestic7)'
set_status(lid, '허가 취소(이력)', '내수 허가 제허 09-682 는 2026-08-31 유효기간 만료 · 이름 든 정상 허가는 전부 수출용 · 국내 유통 근거 못 찾음 — 사용자 결정(_RESUME §2 10-28 마지막 행)', '마지막 반영 domestic7')
for lid, why in [('auto-M8-1775364775119', '「eCO2 EVOLUTION」 모델은 수출용 19-716 하나 · 국내 유통 근거 없음'),
                 ('new-DEV-039', 'StellarDuo 허가는 수출용 23-602 하나 · 현장 사진만으로는 국내 사용 근거로 보지 않음(사용자)')]:
    set_status(lid, '확인 불가', f'{why} — 사용자 결정 확인 불가(_RESUME §2 10-28 마지막 행)', '마지막 반영 domestic7')
EXTRA_Q['auto-M8-1775364775119'] = '현장에서 「에코2 에볼루션」이라 부르는 장비는 루트로닉 eCO2 어느 모델인가요? (EVOLUTION 은 수출용 허가뿐)'
EXTRA_Q['new-DEV-039'] = '현장 스텔라듀오(엘림텍)는 어디서 들여왔나요? 국내 허가번호가 붙어 있나요? (StellarDuo 허가는 수출용뿐)'
D7_DONE = {'M3-3-2', 'M9-1-6', 'auto-M7-1775361076707', 'auto-M7-1775362571755', 'M11-P-1', 'auto-M8-1775364775119', 'new-DEV-039'}
# ② 「허가 대상 아님」 출처 없는 행 — 국내 유통 출처
N45 = J('step1-n45-check.json')['items']
N45_OK, N45_NO = [], []
for x in N45:
    lid = x['ledger_id']; L = idx[lid]['4_license']
    if x['result'] == '국내 유통 확인':
        L['license_basis'] = '국내 유통 확인 · 허가 대상 여부 출처 없음'
        L['distribution_sources'] = x['sources']
        L['reason'] = '허가 대상 아님 유지 — 국내 유통 확인 · 허가 대상 여부 출처 없음(사용자 10-28) · 출처 ' + ' · '.join(s_['url'] for s_ in x['sources'])
        idx[lid]['evidence'] = (idx[lid].get('evidence') or []) + [f'{s_["text"]} — {s_["url"]}' for s_ in x['sources']]
        if x['sellers']:
            co = idx[lid]['6_companies']
            names = {e['name'] for e in co['seller']}
            co['seller'] = [e for e in co['seller'] if not e['name'].startswith('근거 없음')] + [E(z['name'], z['role'], z['url']) for z in x['sellers'] if z['name'] not in names]
        if x.get('note'):
            row_open(lid, x['note'], '마지막 반영 45행')
        log('마지막 반영 45행', lid, f'국내 유통 확인({x["via"]}) — 허가 대상 아님 유지 · license_basis 표시 · 추천' + (' · 판매사 ' + ', '.join(z['name'] for z in x['sellers']) if x['sellers'] else ''))
        N45_OK.append(lid)
    else:
        set_status(lid, '확인 불가', '「허가 대상 아님」 근거가 10-27 게이트(「허가 DB 없음」)뿐 · 국내 유통 출처 못 찾음(data-anyang 0 · 웹 · step1-n45-check) — 사용자 결정 확인 불가(10-28)' + (f' · 참고: {x["note"]}' if x.get('note') else ''), '마지막 반영 45행')
        EXTRA_Q[lid] = f'「{idx[lid]["2_names"]["ledger_name"]}」 필링은 어느 회사 제품인가요? 병원에서 실제로 쓰나요? (국내 병원 · 제조사 출처를 못 찾음)' if '필' in (idx[lid]['2_names']['ledger_name'] or '') else f'「{idx[lid]["2_names"]["ledger_name"]}」의 실제 제품명 · 회사는?'
        N45_NO.append(lid)

for n_, l_ in LINES.items():
    for x_ in l_['items']:
        if x_.get('license_no') and norm_no(x_['license_no']) in EXP:
            x_['export_only'] = True
    if l_['items'] and all(x_.get('export_only') for x_ in l_['items'] if x_.get('license_no')) and any(x_.get('license_no') for x_ in l_['items']):
        l_['note'] = '라인 허가가 전부 수출용 — 국내 허가 없음(10-27 수출용 규칙)'
        row_open(l_['line_row'], f'라인 「{n_}」 허가가 전부 「수출용에 한함」 — 국내 라인 허가 없음. 결정(라인 전체에 붙임) 당시엔 수출용 여부 미확인 — 사용자 확인', '규칙 1 수출용')

# ───────────────────────── 2. 합침 · 빠짐 ─────────────────────────
# 검수 v3 ⑩ 같은 허가 활성 2쌍(코디 판단 _RESUME §2 10-28)
MERGED['auto-M9-1775361909628'] = 'M9-1-4'   # 울트라포머MPT → 슈링크 유니버스(같은 허가 21-831 · 26-208)
MERGED['auto-M9-1775364775138'] = 'M9-2-3'   # 볼뉴머RF → 볼뉴머(같은 허가 22-512)
for dup, rep in MERGED.items():
    d_ = idx[dup]
    d_['merged_into'] = rep
    r = idx[rep]
    r.setdefault('merged_from', [])
    if dup not in r['merged_from']:
        r['merged_from'].append(dup)
    nm = d_['2_names'].get('ledger_name')
    EXTRA_SEARCH[rep].append((nm, f'원장 이름(합쳐진 행 {dup})'))
    for s in d_['2_names'].get('synonyms', []):
        EXTRA_SEARCH[rep].append((s['name'], f'합쳐진 행 {dup} 의 이름 — {s.get("type") or "원장"}'))
    dec = {'auto-M1-1775364775100': 'D04', 'auto-M9-1775363051791': 'D14', 'auto-M9-1775361909628': '검수 v3', 'auto-M9-1775364775138': '검수 v3'}.get(dup, 'D16' if dup != 'M1-P-10' else 'D16 · D29')
    log(dec, dup, f'{rep} 에 합침(merged_into) — 행은 남김')
    log(dec, rep, f'대표 행 — {dup}({nm}) 을 합침 · 그 이름을 검색 이름으로')
for lid, (to, why) in MOVED.items():
    idx[lid]['moved_to'] = to
    idx[lid]['moved_note'] = why
    dec = 'D21' if '(D21)' in why else 'D24' if '(D24)' in why else 'D16' if 'PHA' in why else 'D15' if '해피' in why else 'D23'
    log(dec, lid, f'제품 원장에서 빠짐 → {to} (행은 남김)')


# ───────────────────────── 3. 이름 규칙(전체) ─────────────────────────
NAME_OVERRIDE['auto-M7-1775364775158'] = ('울트라V', '원장 이름 — 10-27 제품 이름 「울트라V-lift」는 수출용 허가(미스코 13-1398) 제품명이라 연결 해제와 함께 내림')
NAME_OVERRIDE['step1-new-APTOS'] = ('압토스', '국내 보도 표기 「압토스(Aptos)란 실」(의협신문 2006-01-31 · step1-d15-web)')
for lid_, nm_ in [('M15-4-1', 'LDM'), ('auto-29-1774737181584', 'BBL'), ('auto-M17-1775364775191', 'AAPE'), ('M5-P-4', 'EXOSOME SKIN')]:
    NAME_OVERRIDE[lid_] = (nm_, '부르는 그대로(영문) 대표 이름 — 한글 이름 출처 없음 · 코디 판단(_RESUME §2 10-28 검수 v3)')
TAXID = re.compile(r'\s*\((M\d+-P-\d+)\)\s*$')
CO_TYPES = ('업체 표기', '제조사 표기(오기', '원천 products.json 제조사')


def lang(n):
    return '한' if H.search(n) else '영'


for it in items:
    n = it['2_names']
    lid = it['ledger_id']
    ln, pn = n.get('ledger_name'), n.get('product_name')
    if lid in NAME_OVERRIDE:
        disp, why = NAME_OVERRIDE[lid]
    elif pn and H.search(pn):
        disp, why = TAXID.sub('', pn), '제품 이름(10-27 정규화)'
    elif ln and H.search(ln):
        disp, why = TAXID.sub('', ln), '원장 이름(국문)'
    else:
        han = [TAXID.sub('', s['name']) for s in n.get('synonyms', []) if H.search(s['name']) and not any(t in (s.get('type') or '') for t in CO_TYPES)]
        if han:
            disp, why = han[0], '국문 이름(검색 이름 중)'
        else:
            disp, why = (ln or pn), '한글 이름 출처 없음 — 원장 표기 그대로'
            row_open(lid, '대표 이름 — 국내에서 부르는 한글 이름 출처 없음(원장 표기 그대로 둠)', '이름 규칙')
    seen, search, basis = set(), [], [f'대표 이름 「{disp}」: {why}']
    co_alias = []

    def add(name, reason):
        if not name:
            return
        name = TAXID.sub('', str(name)).strip()
        if not name or name == disp or name.lower() in seen:
            return
        seen.add(name.lower())
        search.append({'name': name, 'lang': lang(name)})
        basis.append(f'「{name}」: {reason}')

    seen.add(disp.lower())
    add(ln, '원장 이름')
    if pn and pn != ln:
        add(pn, '10-27 제품 이름(정규화)')
    for s in n.get('synonyms', []):
        t = s.get('type') or ''
        if any(x in t for x in CO_TYPES):
            co_alias.append({'name': s['name'], 'basis': t})
            continue
        add(s['name'], t or '원장 이름')
    for nm, why2 in EXTRA_SEARCH.get(lid, []):
        before = len(search)
        add(nm, why2)
        if len(search) > before and '합쳐진 행' not in why2:
            m_ = re.search(r'(D\d\d|10-28)', why2)
            LOG.append({'decision': m_.group(1) if m_ else '이름 규칙(10-27)', 'ledger_id': lid, 'name': disp, 'change': f'검색 이름 추가 「{nm}」 — {why2}'})
    if lid in NAME_OVERRIDE:
        m_ = re.search(r'(D\d\d|10-28)', why)
        LOG.append({'decision': m_.group(1) if m_ else '이름 규칙(10-27)', 'ledger_id': lid, 'name': disp, 'change': f'대표 이름 「{disp}」 — {why}'})
    if co_alias:
        it['6_companies'].setdefault('company_search_names', []).extend(co_alias)
    it['2_names'] = {'display_name': disp, 'ledger_name': ln, 'search_names': search, 'name_basis': basis,
                     'ledger_maker_texts': n.get('ledger_maker_texts')}
    if not n.get('ledger_maker_texts'):
        it['2_names'].pop('ledger_maker_texts')
for lid_, nm_ in [('M2-1-2', '채움'), ('M8-2-4', '프락셀'), ('auto-M4-1775360463217', '벨피엔')]:
    LOG.append({'decision': 'D30', 'ledger_id': lid_, 'name': idx[lid_]['2_names']['display_name'], 'change': f'taxonomy 이름 「{nm_}」 = 같은 제품 — 검색 이름 확정'})
LOG.append({'decision': '이름 규칙(10-27)', 'ledger_id': f'(전체 {len(items)}행)', 'name': '', 'change': '이름 칸 3개로 — 대표 이름(한글 1) · 허가 이름(허가 쪽에만) · 검색 이름[](한/영) · 이유는 name_basis 에만'})


# ───────────────────────── 4. 업체 규칙 · 상태 · 추천 ─────────────────────────
EXPORT_LOST = set()
REC = {'정상': True, '허가 대상 아님': True, '허가번호 미확인': True, '허가 취소(이력)': False, '미허가': False, '확인 불가': False}
for it in items:
    L = it['4_license']
    lid = it['ledger_id']
    # 국내 제조(「제」)는 수입사 「해당 없음」
    nos = [l['license_no'] for l in L['licenses'] if l.get('kind') != '의약품']
    co = it['6_companies']
    if nos and all(is_domestic(x) for x in nos):
        imp = co.get('importer') or []
        if not imp or all(e['name'].startswith('근거 없음') for e in imp):
            co['importer'] = [E('해당 없음', None, '국내 제조 허가(「제」) — 수입 허가 없음')]
            log('규칙 5 업체', lid, '수입사 근거 없음 → 해당 없음(국내 제조 「제」 허가)')
    # 상태 일관성
    if L['status'] == '정상' and not L['licenses']:
        prev = L['status']
        if any(x.get('why', '').startswith('수출용') for x in L['reference']):
            L['status'] = '허가 취소(이력)' if L['history'] else '확인 불가'
            L['reason'] = f'연결 허가가 전부 수출용(국내 허가 아님) → {L["status"]}(10-27 수출용 규칙)'
            log('규칙 1 수출용', lid, f'상태 {prev} → {L["status"]}(남은 국내 허가 0)')
            row_open(lid, f'연결 허가가 전부 「수출용에 한함」 — 같은 업체 · 같은 브랜드 내수 허가도 없음(수출용 재판정 step1-export-recheck) · 국내 유통이 출처로 확인되면 「허가번호 미확인」 검토 · 상태 「{L["status"]}」로 둠', '규칙 1 수출용')
            EXPORT_LOST.add(lid)
        else:
            raise SystemExit(f'정상인데 연결 허가 없음: {lid}')
    if L['status'] not in REC:
        raise SystemExit(f'상태 값 밖: {lid} {L["status"]}')
    if L['status'] != '정상' and L['licenses']:
        raise SystemExit(f'정상 아닌데 연결 허가 있음: {lid} {L["status"]}')
    active = not it.get('merged_into') and not it.get('moved_to')
    it['active'] = active
    L['recommendable'] = REC[L['status']] and active
    if L['status'] == '허가 대상 아님' and active and lid not in ('new-DEV-049',):   # 오투덤은 D31 에서 기사 근거로 확정
        r = (L.get('reason') or '') + ' '.join(it.get('evidence') or [])
        if not re.search(r'https?://', r):
            row_open(lid, '「허가 대상 아님」 근거가 10-27 게이트 기록(「허가 DB 없음」)뿐 · 출처 URL 없음 — 새 규칙 「출처 있을 때만」에 맞는지 사용자 판단(바꾸지 않음)', '규칙 2')

# 라인 · 품목 표시
for name, ln_ in LINES.items():
    rep = ln_['line_row']
    idx[rep]['line'] = {'line_name': name, 'role': '라인', 'parent_line': ln_['parent_line'], 'items': ln_['items'], 'company': ln_['company'],
                        'item_undetermined': rep in ln_['item_undetermined_rows'], 'basis': ln_['basis'], 'decision': ln_['decision']}
    if rep in ln_['item_undetermined_rows']:
        idx[rep]['line']['item'] = '미정'
    for x in ln_['items']:
        if x.get('ledger_id') and x['ledger_id'] != rep:
            idx[x['ledger_id']]['line'] = {'line_name': name, 'role': '품목', 'line_row': rep, 'decision': ln_['decision']}
    for r_ in ln_['item_undetermined_rows']:
        if r_ != rep:
            idx[r_]['line'] = {'line_name': name, 'role': '품목', 'line_row': rep, 'item': '미정', 'decision': ln_['decision']}
    log(ln_['decision'] or '라인', rep, f'라인 「{name}」 · 품목 {len(ln_["items"])}' + (' · 품목 미정' if rep in ln_['item_undetermined_rows'] else ''))
# 10-27 A 구간 라인(members) — 이미 결정된 라인+품목
for it in items:
    l3 = it.get('3_line')
    if it.get('line') or not isinstance(l3, dict) or 'members' not in l3:
        continue
    name = l3['line_name']
    if name in LINES or all(m in MERGED or m in MERGED.values() for m in l3['members']) and name in ('하모니카', '스컬트라', 'NCTF'):
        continue
    it['line'] = {'line_name': name, 'role': '라인 구성', 'members': l3['members'], 'decision': '10-27 같은 허가 원장 중복은 라인+품목'}


# ───────────────────────── 4-1. 검수 v3 정리(코디 판단 _RESUME §2 10-28) ─────────────────────────
OK_LIC = {}
for it in items:
    for l in it['4_license']['licenses']:
        OK_LIC.setdefault(norm_no(l['license_no']), set()).add(it['ledger_id'])
n_r1 = n_r2 = n_r3 = n_f4 = n_line_drop = 0
for it in items:
    lid = it['ledger_id']
    if it.pop('3_line', None) is not None or True:
        n_r1 += 1 if lid in SRC_IDS_WITH_3LINE else 0
    # R2 검색 이름의 「(오기)」
    sn = it['2_names']['search_names']
    keep = [x for x in sn if '(오기)' not in x['name']]
    if len(keep) != len(sn):
        n_r2 += len(sn) - len(keep)
        it['2_names']['name_basis'] = [b_ for b_ in it['2_names']['name_basis'] if '(오기)」' not in b_]
        log('검수 v3', lid, 'R2 검색 이름에서 「(오기)」 붙은 항목 제거: ' + ', '.join(x['name'] for x in sn if '(오기)' in x['name']))
        it['2_names']['search_names'] = keep
    L = it['4_license']
    # R3 국내 제조 의약품 수입사 「해당 없음」
    dl = [l for l in L['licenses'] if l.get('kind') == '의약품']
    co = it['6_companies']
    if dl and len(dl) == len(L['licenses']) and not any('수입' in (l.get('holder_biz') or l.get('induty_type') or '') for l in dl):
        if not co['importer'] or all(e['name'] != '해당 없음' for e in co['importer']):
            co['importer'] = [E('해당 없음', None, '국내 허가 업체 업종이 의약품 제조/위탁제조판매(수입업 아님) — 국내 제조 의약품(검수 v3 R3)')]
            n_r3 += 1
            log('검수 v3', lid, 'R3 국내 제조 의약품 — 수입사 해당 없음')
    # F4 연결과 같은 허가가 참고에 있으면 참고 쪽 제거
    linked = {norm_no(l['license_no']) for l in L['licenses']}
    ref = [r for r in L['reference'] if not (r.get('license_no') and norm_no(r['license_no']) in linked)]
    if len(ref) != len(L['reference']):
        n_f4 += 1
        log('검수 v3', lid, 'F4 연결과 중복된 참고 허가 제거: ' + ', '.join(str(r['license_no']) for r in L['reference'] if r not in ref))
        L['reference'] = ref
# F3 라라젯 18-4662 취하
for lid in ['auto-48-1774737181584', 'auto-52-1774737181584']:
    for h in idx[lid]['4_license']['history']:
        if norm_no(h['license_no']) == '제인18-4662' and h.get('state') != '취하':
            h['state'] = '취하'; h['date_note'] = '2024-09-30'
            log('검수 v3', lid, 'F3 이력 제인 18-4662 상태 취소 → 취하(2024-09-30)')
# F7 울킨
it = idx['new-DEV-047']
it['evidence'] = (it.get('evidence') or []) + ['https://www.ulkin.net/ — 제조사 공식 사이트 「본 기기는 피부 미용 기기로 의료 기기가 아니며」(WebFetch 2026-10-27)']
it['open'] = [o for o in it['open'] if '출처 URL 없음' not in o]
OPEN[:] = [o for o in OPEN if not (o['ledger_id'] == 'new-DEV-047' and '출처 URL 없음' in o['open'])]
log('검수 v3', 'new-DEV-047', 'F7 evidence 에 제조사 공식 사이트 URL · open 「출처 URL 없음」 제거')
# ① 라인 품목 = 정상 · 내수 허가만(수출용 · 취소 · 재제조 · 이력 제품은 품목 아님)
for n_, l_ in LINES.items():
    keep = []
    for x_ in l_['items']:
        if x_.get('license_no'):
            ok = norm_no(x_['license_no']) in OK_LIC and norm_no(x_['license_no']) not in EXP
        else:
            r_ = idx.get(x_.get('ledger_id'))
            ok = bool(r_) and r_['active'] and r_['4_license']['status'] in ('정상', '허가 대상 아님', '허가번호 미확인')
        if ok:
            keep.append(x_)
        else:
            n_line_drop += 1
            log('검수 v3', l_['line_row'], f'① 라인 「{n_}」 품목에서 뺌 — {x_.get("license_no") or x_.get("name")}(정상 · 내수 허가 아님)')
    l_['items'] = keep
    for x_ in keep:
        x_.pop('export_only', None)
    l_.pop('note', None) if n_ != '더블로' else None
LOG.append({'decision': '검수 v3', 'ledger_id': '(전체)', 'name': '', 'change': f'① 옛 3_line 칸 삭제 {n_r1}행 — 라인은 line · lines 만'})
# domestic7 결정이 난 행은 수출용 · 재조사 대기 open 을 닫는다
for lid in D7_DONE:
    drop = [o for o in idx[lid]['open'] if '수출용' in o or '사용자 확인' in o]
    if drop:
        idx[lid]['open'] = [o for o in idx[lid]['open'] if o not in drop]
        OPEN[:] = [o for o in OPEN if not (o['ledger_id'] == lid and o['open'] in drop)]
        log('마지막 반영 domestic7', lid, f'open {len(drop)}건 닫음 — 사용자 결정(_RESUME §2 10-28 마지막 행)')
V3_COUNTS = {'R1_3line_removed': n_r1, 'R1_line_items_dropped': n_line_drop, 'R2_typo_search_removed': n_r2, 'R3_drug_importer_na': n_r3, 'F4_ref_dupes_rows': n_f4}

# ───────────────────────── 5. 요약 · 출력 ─────────────────────────
for o in OPEN:
    o['name'] = idx[o['ledger_id']]['2_names']['display_name']
act = [it for it in items if it['active']]
st = collections.Counter(it['4_license']['status'] for it in act)
line_names = sorted({it['line']['line_name'] for it in items if it.get('line') and it['active']})


def filled(role):
    return sum(1 for it in act if any(not e['name'].startswith('근거 없음') for e in it['6_companies'].get(role) or []))


summary = {
    'rows_total': len(items), 'rows_v1': len(SRC['items']), 'rows_new': len(items) - len(SRC['items']),
    'active_products': len(act), 'merged': sum(1 for it in items if it.get('merged_into')), 'moved_to_procedure_name': sum(1 for it in items if it.get('moved_to')),
    'status': dict(st.most_common()), 'recommendable': {'true': sum(1 for it in act if it['4_license']['recommendable']), 'false': sum(1 for it in act if not it['4_license']['recommendable'])},
    'lines': {'count': len(line_names), 'names': line_names, 'item_undetermined': sorted(n for n, l in LINES.items() if l['item_undetermined_rows'])},
    'companies_filled': {r: filled(r) for r in ('manufacturer', 'importer', 'seller')},
    'seller_filled': filled('seller'),
    'export_only_unlinked': sum(1 for it in items for x in it['4_license']['reference'] if str(x.get('why', '')).startswith('수출용')),
    'kpic_enriched_licenses': sum(1 for it in items for l in it['4_license']['licenses'] + it['4_license']['history'] + it['4_license']['reference'] if l.get('kpic')), 'kpic_enriched_note': '연결 · 이력 · 참고 허가 중 kpic 이 붙은 수', 'kpic_linked': sum(1 for it in items for l in it['4_license']['licenses'] if l.get('kpic')), 'review_v3': V3_COUNTS, 'final_10_28': {'domestic7': len(D7_DONE), 'n45_rows': len(N45), 'n45_distribution_confirmed': len(N45_OK), 'n45_confirmed_by_source': 0, 'n45_unconfirmed': len(N45_NO)},
    'source_fix': len(SFIX), 'open_rows': sum(1 for it in items if it['open']), 'open_items': len(OPEN),
}
out = {'version': 2, 'generated_at': '2026-10-28',
       'scope': '1단계 제품 원장 — 사용자 결정 전부 반영(10-27 · 10-28) · 원장 390행 + 새 행',
       'basis': {'frozen_input': 'step1-products-v1-frozen.json(v1 · 390행)', 'decisions': ['_RESUME.md §2 10-27 · 10-28', 'gate-answers/step1-decisions-db-2026-10-28.md', '_RESUME.md §2 10-29 U8 · U9(step1-step5-decisions.json)'],
                 'research': ['step1-d09-web', 'step1-d12-web', 'step1-d15-web', 'step1-d16-web', 'step1-d17', 'step1-d17-2', 'step1-d18', 'step1-d19', 'step1-d20-31', 'step1-cancel-recheck'],
                 'export_check': 'step1-export-check.json(emedi 품목 상세 xprtppYn) · step1-export-recheck.json(내수 허가 재탐색 · 의약품 품목명 판정)', 'kpic': 'step1-kpic.json(KPIC MCP reference/2026-10-28-kpic-mcp)',
                 'script': 'step1-apply.py',
                 'fields': {'2_names': 'display_name(대표 한글 1) · search_names[{name, lang 한/영}] · name_basis(이유) — 허가 이름은 4_license.licenses[].official_name 에만',
                            '4_license': 'status 6값 · recommendable · licenses(정상만) · history(취소 · 취하 · 만료 · 재제조) · reference(수출용 · 후보 · 연결 안 함)',
                            '6_companies': 'manufacturer · importer · seller · license_holder · other(개발 · 브랜드) — 각 {name, role, basis, period?} · conflicts(덮지 않고 기록) · company_search_names',
                            'line': '라인 = 상위 제품 / 품목 · item 「미정」', 'merged_into · merged_from': '합친 행(지우지 않음)', 'moved_to': '「5단계 시술 이름」(지우지 않음)',
                            'active': '합침 · 빠짐이 아닌 제품 행', 'open[]': '결정에 없어 바꾸지 않은 것'}},
       'summary': summary, 'shared_license': SRC.get('shared_license'), 'lines': LINES, 'open': OPEN, 'items': items}
json.dump(out, open(f'{W}/step1-products.json', 'w'), ensure_ascii=False, indent=1)
OLD_SF = J('source-fix-list.json')['items']
for f in SFIX:
    hit = [o['id'] for o in OLD_SF if f['ledger_id'] and f['ledger_id'] in json.dumps(o, ensure_ascii=False) and str(f['now']).strip('「」') in json.dumps(o, ensure_ascii=False)]
    f['also_in_source_fix_list'] = hit or None
json.dump({'generated_at': '2026-10-28', 'scope': '1단계 원장 반영에서 새로 생긴 원천 수정(기존 source-fix-list 와 별도)', 'count': len(SFIX), 'items': SFIX},
          open(f'{W}/step1-source-fix.json', 'w'), ensure_ascii=False, indent=1)
open(f'{W}/step1-apply-log.json', 'w').write(json.dumps(LOG, ensure_ascii=False, indent=1))
print(json.dumps(summary, ensure_ascii=False, indent=1))


# ───────────────────────── 6. md ─────────────────────────
def esc(x):
    return str(x if x is not None else '').replace('|', '／').replace('\n', ' ')


def lic_short(L):
    return ', '.join(esc(l['license_no']) for l in L['licenses']) or '—'


DEC_ORDER = ['D01', 'D02', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19',
             'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32']
md = ['# 1단계 제품 원장 — 결정 반영본 (2026-10-28)', '',
      '정본은 `step1-products.json`(v2). 이 표는 읽기용 요약. 반영 스크립트 `step1-apply.py`(입력 고정 `step1-products-v1-frozen.json`) · 결정마다 무엇을 바꿨는지는 `step1-apply-log.md`.', '',
      '## 요약', '',
      f'- 행 {summary["rows_total"]} = v1 {summary["rows_v1"]} + 새 행 {summary["rows_new"]}(압토스 · 콘투락투벡스 · 라이넥 · 아큐탄)',
      f'- 제품(합침 · 빠짐 제외) **{summary["active_products"]}** · 합침 {summary["merged"]} · 시술 이름으로 빠짐 {summary["moved_to_procedure_name"]}',
      '- 상태별(제품 행): ' + ' · '.join(f'{k} {v}' for k, v in summary['status'].items()),
      f'- 추천 가능(recommendable) **{summary["recommendable"]["true"]}** / 제외 {summary["recommendable"]["false"]} — 정상 · 허가 대상 아님 · 허가번호 미확인 = 추천',
      f'- 라인 {summary["lines"]["count"]}: ' + ' · '.join(summary['lines']['names']) + ' — 품목 미정: ' + ' · '.join(summary['lines']['item_undetermined']),
      f'- 업체 채움(근거 있는 이름 · 「해당 없음」 포함, 제품 행 기준): 제조 {summary["companies_filled"]["manufacturer"]} · 수입 {summary["companies_filled"]["importer"]} · **판매 {summary["seller_filled"]}**',
      f'- 수출용 허가 연결 해제(참고로만) {summary["export_only_unlinked"]} · KPIC 보강 의약품 허가 {summary["kpic_enriched_licenses"]}',
      '- **수출용 재판정(10-28 코디 반려)**: emedi xprtppYn = 품목(허가) 단위 「수출용에 한함」(상세 화면 표 캡션 「품목의 수출용에한함여부」 https://emedi.mfds.go.kr/search/data/MNU20237). 예 105건 전부 허가 단위 비고 「수출용에 한함」 · 일부 모델만 수출용 0건 → 의료기기 수출 전용 판정은 유지. 국내 판매 제품은 **같은 업체의 다른 내수 허가**로 연결(슈링크 14-1422 · 더블로 11-946 · 21-690 · 뉴라미스 13-871 · 14-2923 · 시크릿RF 11-1071 · 텐써마 22-679) · 의약품은 식약처 품목명 기준으로 바꿔 더톡신 202107200 복구(KPIC 「수출용」 표기는 2025-11 제품명 변경 전 이름). 근거 `step1-export-recheck.json`',
      f'- **마지막 반영(10-28)**: domestic7 — 고우리 25-634 · 더블로 골드 11-946 · 잼버실 13-1507 연결 · N코그 허가번호 미확인 · 인트라셀 허가 취소(이력) · 에코2 에볼루션 · 스텔라듀오 확인 불가 / 출처 없던 「허가 대상 아님」 {len(N45)}행 — 국내 유통 확인 {len(N45_OK)}(유지 · `license_basis` 「국내 유통 확인 · 허가 대상 여부 출처 없음」) · 출처로 확정 0 · 확인 불가 {len(N45_NO)}(원천 질문) · 근거 `step1-n45-check.json` · `step1-domestic7.json`',
      f'- 원천 수정 {summary["source_fix"]}(`step1-source-fix.md`) · open {summary["open_items"]}건 / {summary["open_rows"]}행(아래 §3)', '',
      '## 1. 제품 행', '', '| ledger_id | 대표 이름 | 상태 | 추천 | 라인 | 연결 허가 | 제조 | 수입 | 판매 |', '|---|---|---|---|---|---|---|---|---|']
for it in items:
    if not it['active']:
        continue
    L = it['4_license']; co = it['6_companies']; ln_ = it.get('line')
    md.append(f'| `{it["ledger_id"]}` | {esc(it["2_names"]["display_name"])} | {L["status"]} | {"○" if L["recommendable"] else "✗"} | '
              f'{esc((ln_["line_name"] + (" · 품목 미정" if ln_.get("item") == "미정" else "") + (" (품목)" if ln_["role"] == "품목" else "")) if ln_ else "")} | {lic_short(L)} | '
              + ' | '.join(esc(' · '.join(e['name'] for e in co.get(r) or [])) for r in ('manufacturer', 'importer', 'seller')) + ' |')
md += ['', '## 2. 합침 · 시술 이름으로 빠짐 (행은 남김)', '', '| ledger_id | 원장 이름 | 어디로 | 근거 |', '|---|---|---|---|']
for it in items:
    if it.get('merged_into'):
        md.append(f'| `{it["ledger_id"]}` | {esc(it["2_names"]["ledger_name"])} | 합침 → `{it["merged_into"]}` {esc(idx[it["merged_into"]]["2_names"]["display_name"])} | 대표 행 검색 이름으로 |')
for it in items:
    if it.get('moved_to'):
        md.append(f'| `{it["ledger_id"]}` | {esc(it["2_names"]["ledger_name"])} | {it["moved_to"]} | {esc(it["moved_note"])} |')
md += ['', '## 3. open — 결정에 없어 바꾸지 않은 것', '', '| ledger_id | 이름 | 무엇 | 관련 |', '|---|---|---|---|']
for o in OPEN:
    md.append(f'| `{o["ledger_id"]}` | {esc(o["name"])} | {esc(o["open"])} | {esc(o["decision"])} |')
open(f'{W}/step1-products.md', 'w').write('\n'.join(md) + '\n')

# 원천 수정
sm = ['# 1단계 원천 수정 목록 — 이번 반영에서 생긴 것 (2026-10-28)', '',
      '기존 `source-fix-list.*` 와 별도. 원천(taxonomy · 원장 · 원천 products.json)에서 고칠 값 — 고치는 것은 원천 쪽 일이고 여기선 목록만. 정본 `step1-source-fix.json`.', '',
      f'{len(SFIX)}건', '', '| id | ledger_id | 원장 이름 | 칸 | 지금 | 고칠 값 | 왜 | 결정 | 기존 목록 |', '|---|---|---|---|---|---|---|---|---|']
for f in SFIX:
    sm.append(f'| {f["id"]} | `{f["ledger_id"]}` | {esc(f["name"])} | {esc(f["field"])} | {esc(f["now"])} | {esc(f["fix"])} | {esc(f["why"])} | {esc(f["decision"])} | {esc(", ".join(f["also_in_source_fix_list"] or []) or "—")} |')
open(f'{W}/step1-source-fix.md', 'w').write('\n'.join(sm) + '\n')

# 반영 기록
by = collections.OrderedDict()
for x in LOG:
    by.setdefault(x['decision'], []).append(x)
al = ['# 1단계 원장 반영 기록 (2026-10-28)', '', '결정마다 「어느 행에 무엇을 바꿨나」 한 줄. 스크립트 `step1-apply.py` 가 남긴 그대로.', '']
for k in sorted(by, key=lambda d: (DEC_ORDER.index(d[:3]) if d[:3] in DEC_ORDER else 99, d)):
    al.append(f'## {k}'); al.append('')
    for x in by[k]:
        al.append(f'- `{x["ledger_id"]}` {esc(x["name"])} — {esc(x["change"])}')
    al.append('')
open(f'{W}/step1-apply-log.md', 'w').write('\n'.join(al))

# 원천 질문
hh = open(f'{W}/step1-open.html').read()
OPN = json.loads([x for x in re.findall(r'<script[^>]*>(.*?)</script>', hh, re.S) if x.strip().startswith('{')][0])
EXTRA_Q.update({  # 새로 확인 불가가 됐거나 질문이 없던 것 — 결정 · 조사 근거에서 나온 쉬운 질문
    'auto-M1-1775360538524': '「다복스」는 어떤 톡신 제품인가요? 제품명 · 회사를 알려 주세요.',
    'auto-M15-1775401645338': 'PRX필은 WiQo 「PRX-T33」인가요? 국내 수입사는 어디인가요?',
    'auto-M15-1775362958625': '「옥시덤」은 어떤 장비인가요? 제품명 · 회사를 알려 주세요.',
    'auto-M8-1775362951135': '「리레이저」는 르키드 「RELASER」(제허 19-69)인가요?',
    'new-DEV-042': '현장 「더마큐어」 장비는 피글 「Dermacure」(제허 22-692)인가요?',
    'auto-M7-1775362729861': '「캐번실」은 네오닥터 캐번(지금은 잼버)인가요? 지금 쓰는 제품명은?',
    'auto-M8-1775362619619': '「슬렌더엑스」는 어느 회사의 어떤 장비인가요?',
    'auto-M9-1775363058909': '「시크릿맥스」는 클래시스 「QUADESSY」(제허 24-342)와 같은 장비인가요?',
    'auto-M16-DCA-1775404043067': '「리포린주」 허가번호를 알 수 있나요? (보도는 2025-08 허가, 식약처 조회는 0건)',
    'auto-49-1774737181584': '「아스트로돔」의 제조사 · 수입사는 어디인가요?',
    'new-DEV-074': '「스케나」의 제조사 · 수입사는 어디인가요?',
    'auto-M15-1775361951923': '「아큐탄」으로 쓰는 약은 어느 회사 이소트레티노인 제품인가요?',
    'auto-14-1774737181584': '병원이 쓰는 「레티젠」은 어느 회사 제품인가요? (같은 이름 허가는 인대·건 보충용이라 다름)',
    'auto-15-1774737181584': '병원이 쓰는 「미라콜」은 어느 회사 제품인가요? (같은 이름 허가는 인대·근육 보충용이라 다름)',
    'M4-2-3': '병원이 쓰는 「릴리이드M」은 어느 회사 제품인가요? (같은 이름 허가는 내시경 점막 융기용이라 다름)',
    'new-DEV-034': '「벨르업」 실물 라벨에 의료기기 표시(허가번호)가 있나요? 만든 회사는?',
})
ask_rows = {}
qm = ['# 1단계 원천(병원)에 물을 것 (2026-10-28)', '',
      '「확인 불가」로 남은 제품 중 병원 · 원천에 물어야 닫히는 것. 질문 한 줄씩. 답이 오면 그 행만 다시 판정한다.', '']
for g in OPN['ask']:
    qm += [f'## {g["t"]}', '']
    for q in g['items']:
        lids = [x.strip() for x in q['c'].split('·')]
        alive = [l for l in lids if l in idx and idx[l]['active'] and idx[l]['4_license']['status'] == '확인 불가']
        for l in lids:
            ask_rows[l] = q['q']
        mark = '' if alive else ' *(이번 반영으로 상태가 바뀜 — 그래도 질문은 남김)*'
        qm.append(f'- {q["q"]} — `{q["c"]}`{mark}')
    qm.append('')
left = [it for it in items if it['active'] and it['4_license']['status'] == '확인 불가' and it['ledger_id'] not in ask_rows and it['ledger_id'] not in EXPORT_LOST]
qm += ['## 그 밖의 확인 불가 — 이번 반영에서 질문을 붙인 것', '']
n_extra = 0
for it in left:
    q = EXTRA_Q.get(it['ledger_id']) or f'「{it["2_names"]["display_name"]}」의 실제 제품명 · 만든 회사는 어디인가요?'
    qm.append(f'- {q} — `{it["ledger_id"]}`'); n_extra += 1
qm += (['', '## 병원에 물을 것 아님 — 같은 업체 · 같은 브랜드 허가를 다시 찾아도(수출용 재판정 10-28) 전부 「수출용에 한함」인 것(참고)', ''] if EXPORT_LOST else [])
for lid in sorted(EXPORT_LOST):
    it = idx[lid]
    qm.append(f'- {it["2_names"]["display_name"]} — 수출용 허가 ' + ', '.join(str(x['license_no']) for x in it['4_license']['reference'] if str(x.get('why', '')).startswith('수출용')) + f' · 지금 {it["4_license"]["status"]} — `{lid}`')
qm += ['', '## 참고 — 라인에는 붙였지만 품목이 미정인 것(추천은 됨)', '']
for n, l in LINES.items():
    for r in l['item_undetermined_rows']:
        if not idx[r]['4_license']['recommendable']:
            continue
        qm.append(f'- 「{idx[r]["2_names"]["ledger_name"]}」은 {n} 라인 중 어느 제품인가요? — `{r}`')
n_ask = sum(len(g['items']) for g in OPN['ask'])
qm.insert(3, f'질문 {n_ask + n_extra}개 = 결정 페이지 「원천에 물어볼 것」 {n_ask} + 그 밖의 확인 불가 {n_extra}. ' + (f'수출용 허가만 남은 {len(EXPORT_LOST)}행은 식약처 재조사 대상이라 질문에서 뺌(맨 아래 참고). ' if EXPORT_LOST else '') + f'출처 없던 「허가 대상 아님」 중 국내 유통 출처를 못 찾은 {len(N45_NO)}행 포함(10-28). 직접 확인 6(엔진리프팅 명판 · BBL 본체 · 모르페우스8 허가번호 · 제네오X · 라라젯 · 취소 후보 2 — 타임버스는 10-28 티엠버스주로 결정)은 사용자 몫이라 여기 넣지 않음.\n')
open(f'{W}/step1-origin-questions.md', 'w').write('\n'.join(qm) + '\n')
summary['origin_questions'] = n_ask + n_extra
summary['export_only_rows_need_recheck'] = sorted(EXPORT_LOST)
out['summary'] = summary
json.dump(out, open(f'{W}/step1-products.json', 'w'), ensure_ascii=False, indent=1)
print('origin questions', n_ask + n_extra)
