"""post-procedure-timeline.json 1차 조사 산출물 재생성.

실행(레포 루트에서):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/post-procedure-timeline/build.py

원본은 읽기만 한다. 쓰기는 이 스크립트가 있는 폴더 안의 생성 파일뿐이다.
수동 기록(manual/*.txt)은 직접 읽기 결과이며 이 스크립트는 그것을 읽어 위치(구간)만 계산한다.
validation.md 는 생성하지 않는다(verify 실행 결과를 사람이 적는다).
"""
import hashlib, json, os, re, sys, unicodedata
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
SRC_REL = 'orchestration/work/phub-recommend/bronze/phub-ledger/post-procedure-timeline.json'
SRC = os.path.join(ROOT, SRC_REL)
OUT_REL = os.path.relpath(HERE, ROOT)

ID_CODE_FIELDS = {'id', 'category', 'version', 'updated'}
LEVEL_KEYS = ['normal', 'abnormal', 'caution', 'emergency']


# ---------------------------------------------------------------- 원본 고정
raw = open(SRC, 'rb').read()
SHA = hashlib.sha256(raw).hexdigest()
text = raw.decode('utf-8')

def cp_to_byte(i, _cache={}):
    return len(text[:i].encode('utf-8'))

# 작은 재귀 하강 파서: 모든 값·키의 원문 리터럴 구간(코드포인트·바이트)을 잡고 중복 키를 감지한다.
class P:
    def __init__(s, t): s.t, s.i = t, 0
    def ws(s):
        while s.i < len(s.t) and s.t[s.i] in ' \t\r\n': s.i += 1
    def string(s):
        st = s.i; assert s.t[s.i] == '"'; s.i += 1
        while True:
            c = s.t[s.i]
            if c == '\\': s.i += 2; continue
            if c == '"': s.i += 1; break
            s.i += 1
        lit = s.t[st:s.i]
        return json.loads(lit), (st, s.i), ('\\' in lit)
    def value(s, ptr, out, dups):
        s.ws(); st = s.i; c = s.t[s.i]
        if c == '{':
            s.i += 1; s.ws(); keys = []; members = []
            if s.t[s.i] == '}': s.i += 1
            else:
                while True:
                    s.ws(); k, kspan, kesc = s.string(); s.ws(); assert s.t[s.i] == ':'; s.i += 1
                    if k in keys: dups.append({'object': ptr, 'key': k, 'key_literal_cp': list(kspan)})
                    keys.append(k)
                    cptr = ptr + '/' + k.replace('~', '~0').replace('/', '~1')
                    members.append((k, kspan, kesc, cptr))
                    s.value(cptr, out, dups); s.ws()
                    if s.t[s.i] == ',': s.i += 1; continue
                    assert s.t[s.i] == '}'; s.i += 1; break
            out[ptr] = {'type': 'object', 'literal_cp': (st, s.i), 'members': members}
        elif c == '[':
            s.i += 1; s.ws(); n = 0
            if s.t[s.i] == ']': s.i += 1
            else:
                while True:
                    s.value(f'{ptr}/{n}', out, dups); n += 1; s.ws()
                    if s.t[s.i] == ',': s.i += 1; continue
                    assert s.t[s.i] == ']'; s.i += 1; break
            out[ptr] = {'type': 'array', 'literal_cp': (st, s.i), 'length': n}
        elif c == '"':
            v, span, esc = s.string()
            out[ptr] = {'type': 'string', 'literal_cp': span, 'value': v, 'escaped': esc}
        else:
            m = re.compile(r'-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null').match(s.t, s.i)
            s.i = m.end(); v = json.loads(m.group(0))
            typ = 'null' if v is None else 'boolean' if isinstance(v, bool) else 'number'
            out[ptr] = {'type': typ, 'literal_cp': (st, s.i), 'value': v}

nodes_raw, dups = {}, []
p = P(text); p.value('', nodes_raw, dups); p.ws(); assert p.i == len(text)
data = json.loads(text)

def resolve(ptr):
    o = data
    if ptr == '': return o
    for part in ptr[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        o = o[int(part)] if isinstance(o, list) else o[part]
    return o

# 문서 순서(원문 리터럴 시작 위치)로 정렬
order = sorted(nodes_raw, key=lambda k: (nodes_raw[k]['literal_cp'][0], -nodes_raw[k]['literal_cp'][1]))

def field_name(ptr):
    last = ptr.rsplit('/', 1)[-1] if ptr else ''
    return None if (ptr == '' or last.isdigit()) else last

def column_path(ptr):
    """원본 컬럼 경로 패턴: 배열 인덱스를 * 로."""
    return '/'.join('*' if x.isdigit() else x for x in ptr.split('/')) if ptr else ''


# ---------------------------------------------------------------- 구획
SEGMENTS = [OrderedDict(id='S00', title='상위 메타데이터 (version·updated·consensus_method·reaction_levels) + 루트·timelines 배열 컨테이너',
                        owns_prefixes=['/version', '/updated', '/consensus_method', '/reaction_levels'], owns_exact=['', '/timelines'])]
for i, t in enumerate(data['timelines']):
    SEGMENTS.append(OrderedDict(id=f'S{i+1:02d}', title=f"/timelines/{i} {t['id']} ({t['name']})",
                                owns_prefixes=[f'/timelines/{i}'], owns_exact=[]))

def owner_of(ptr):
    hits = []
    for s in SEGMENTS:
        if ptr in s['owns_exact'] or any(ptr == pre or ptr.startswith(pre + '/') for pre in s['owns_prefixes']):
            hits.append(s['id'])
    return hits

SEG_BASE = {s['id']: ('' if s['id'] == 'S00' else s['owns_prefixes'][0]) for s in SEGMENTS}


# ---------------------------------------------------------------- 노드 기록
nodes = []
for ord_i, ptr in enumerate(order):
    n = nodes_raw[ptr]; s, e = n['literal_cp']
    rec = OrderedDict(order=ord_i, pointer=ptr, parent=(None if ptr == '' else ptr.rsplit('/', 1)[0]),
                      field=field_name(ptr), column_path=column_path(ptr), type=n['type'],
                      literal_cp=[s, e], literal_byte=[cp_to_byte(s), cp_to_byte(e)])
    if ptr != '':
        last = ptr.rsplit('/', 1)[-1]
        if last.isdigit() and isinstance(resolve(rec['parent']), list): rec['index'] = int(last)
    if n['type'] == 'object':
        rec['keys'] = [m[0] for m in n['members']]
        rec['key_literals'] = [OrderedDict(key=m[0], literal_cp=list(m[1]), literal_byte=[cp_to_byte(m[1][0]), cp_to_byte(m[1][1])], escaped=m[2]) for m in n['members']]
        rec['empty'] = not n['members']
    elif n['type'] == 'array':
        rec['length'] = n['length']; rec['empty'] = n['length'] == 0
    else:
        rec['value'] = n['value']
        if n['type'] == 'string':
            rec['escaped'] = n['escaped']
            rec['value_cp_len'] = len(n['value'])
            rec['empty'] = n['value'] == ''
    ow = owner_of(ptr); rec['segment'] = ow[0] if len(ow) == 1 else ow
    nodes.append(rec)
NODE = {n['pointer']: n for n in nodes}
leaves = [n for n in nodes if n['type'] not in ('object', 'array')]
strings = [n for n in leaves if n['type'] == 'string']

# 공유 문맥: 각 timeline 구획은 /reaction_levels 정의와 /consensus_method 를 문맥으로 참조한다(소유 아님).
for s in SEGMENTS:
    s['owned_pointers'] = [n['pointer'] for n in nodes if n['segment'] == s['id']]
    s['owned_leaf_pointers'] = [n['pointer'] for n in nodes if n['segment'] == s['id'] and n['type'] not in ('object', 'array')]
    s['context_refs'] = [] if s['id'] == 'S00' else ['', '/timelines', '/consensus_method', '/reaction_levels'] + [f'/reaction_levels/{k}' for k in LEVEL_KEYS]


# ---------------------------------------------------------------- 수동 기록(직접 읽기) 파싱
def parse_manual(seg):
    path = os.path.join(HERE, 'manual', f'{seg}.txt')
    exprs, obs, issues = [], [], []
    base = SEG_BASE[seg]
    for ln, line in enumerate(open(path, encoding='utf-8').read().split('\n'), 1):
        if not line.strip() or line.startswith('#'): continue
        parts = [x.strip() for x in line.split(' | ')]
        if parts[0] == 'O':
            obs.append(OrderedDict(id=f'{seg}-O{len(obs)+1}', text=' | '.join(parts[1:]), manual_line=ln))
        elif parts[0] == 'Q':
            cls, ptrs, body = parts[1], parts[2], ' | '.join(parts[3:])
            refs = [(base + '/' + x) if not x.startswith('/') else x for x in ptrs.split()]
            issues.append(OrderedDict(id=f'{seg}-Q{len(issues)+1}', cls=cls, refs=refs, text=body, manual_line=ln))
        else:
            key, phrase, kinds = parts[0], parts[1], parts[2]
            note = parts[3] if len(parts) > 3 else ''
            ptr = key if key.startswith('/') else base + '/' + key
            occ = 1
            m = re.match(r'^(.*)#(\d+)$', phrase)
            if m: phrase, occ = m.group(1), int(m.group(2))
            exprs.append(OrderedDict(pointer=ptr, phrase=phrase, occurrence=occ, kinds=[k for k in kinds.split(',') if k], note=note, manual_line=ln))
    return exprs, obs, issues

MANUAL = {s['id']: parse_manual(s['id']) for s in SEGMENTS}

def find_occ(hay, needle, occ):
    i = -1
    for _ in range(occ):
        i = hay.find(needle, i + 1)
        if i < 0: return None
    return i


# ---------------------------------------------------------------- 형태소 분석
from kiwipiepy import Kiwi
import kiwipiepy
kiwi = Kiwi(num_workers=1, model_type='cong')

def classify(n):
    f = n['field']
    if f in ID_CODE_FIELDS: return 'excluded', 'ID/코드/버전/날짜 값 — 언어 텍스트가 아님(원문 보존, 형태소 분석 제외)'
    if n['value'] == '': return 'excluded', '빈 문자열'
    return 'applied', None

applied, excluded = [], []
for n in strings:
    st, reason = classify(n)
    if st == 'excluded':
        excluded.append(OrderedDict(pointer=n['pointer'], field=n['field'], value=n['value'], reason=reason)); continue
    toks = []
    for j, t in enumerate(kiwi.tokenize(n['value'])):
        s, e = t.start, t.start + t.len
        toks.append(OrderedDict(i=j, form=t.form, tag=str(t.tag), lemma=t.lemma, start=s, end=e,
                                source_slice=n['value'][s:e], surface_match=(n['value'][s:e] == t.form)))
    applied.append(OrderedDict(pointer=n['pointer'], field=n['field'], segment=n['segment'], text=n['value'], tokens=toks))

field_name_occ = Counter()
field_name_ptrs = {}
for n in nodes:
    if n['type'] == 'object':
        for k in n['keys']:
            field_name_occ[k] += 1
            field_name_ptrs.setdefault(k, []).append(n['pointer'] + '/' + k)

# 알려진 오분절 규칙: 직접 읽기에서 문맥과 대조해 확인한 서명. 서명에 맞는 모든 출현을 기록하며 교정하지 않는다.
# (rule, 토큰 서열[(form, {tags})], 원문 표면, 설명, 영향, 영향 정도)
SEQ_RULES = [
    ('K-NAE', [('나', {'NP'}), ('의', {'JKG'})], '내', '「내」(이내, 의존명사)가 나/NP+의/JKG 로 분석', '기간 한정(이내) 의미가 대명사+조사로 바뀜 — 시간 범위 손실', 'high'),
    ('K-JISOK', [('지', {'NP'}), ('속', {'NNG'})], '지속', '「지속」 이 지/NP+속/NNG 로 분할', '지속(경과) 단서 손실', 'high'),
    ('K-DAEBUBUN', [('대', {'XPN'}), ('부분', {'NNG'})], '대부분', '「대부분」 이 대/XPN+부분/NNG 로 분할', '근사·비율 단서 「대부분」 손실', 'medium'),
    ('K-SISA', [('시', {'NNB'}), ('사', {'NNG'})], '시사', '「시사」(추정) 가 시/NNB+사/NNG 로 분할', '조건 「시」 오탐 위험, 추정 표현 손실', 'medium'),
    ('K-SAMCHUL', [('삼', {'NR'}), ('출', {'NNG'})], '삼출', '「삼출」 이 삼/NR(수사)+출 로 분할', '수량 오탐(삼=3) 위험', 'medium'),
    ('K-SUPO', [('수', {'NNB', 'NNG'}), ('포', {'NNG'})], '수포', '「수포」 가 수+포 로 분할', '「수」(가능·수량) 오탐 위험, 사건명 손실', 'medium'),
    ('K-YUSA', [('유', {'NNG'}), ('사', {'NNG'})], '유사', '「유사」 가 유+사 로 분할', '비유·유사 단서 손실', 'medium'),
    ('K-SEONBEON', [('선', {'NNG'}), ('번', {'NNB'})], '선번', '외래어 「선번」 이 선+번(의존명사) 로 분할', '외래어 사건명 손실', 'low'),
    ('K-DOLGI', [('돌', {'VV'}), ('기', {'ETN'})], '돌기', '명사 「돌기」 가 돌/VV+기/ETN(동사 명사형)', '사건 명사 손실', 'medium'),
    ('K-IJUNGTEOK', [('이', {'MM'}), ('중턱', {'NNG'})], '이중턱', '「이중턱」 이 이/MM+중턱 으로 분할', '비교 기준 부위 손실', 'medium'),
    ('K-ANDONGMAEK', [('안', {'NNG'}), ('동맥', {'NNG'})], '안동맥', '「안동맥」 이 안+동맥 으로 분할', '「안」 부정 오탐 위험, 해부 명칭 손실', 'medium'),
    ('K-GYEOLJEOL', [('결', {'NNG'}), ('절', {'NNG'})], '결절', '「결절」 이 결+절 로 분할', '사건 명사 손실', 'low'),
    ('K-GYEONGGYEOL', [('경', {'NNG'}), ('결', {'NNG'})], '경결', '「경결」 이 경+결 로 분할', '사건 명사 손실', 'low'),
    ('K-BALJEOK', [('발', {'NNG'}), ('적', {'XSN'})], '발적', '「발적」 이 발/NNG+적/XSN 으로 분할', '사건 명사 손실(「-적」 접미 오인)', 'low'),
    ('K-GAPI', [('가', {'NNG'}), ('피', {'NNG', 'XPN'})], '가피', '「가피」 가 가+피 로 분할', '사건 명사 손실', 'low'),
    ('K-CHOKJI', [('촉', {'NNG'}), ('지', {'NNG'})], '촉지', '「촉지」 가 촉+지 로 분할', '감지 방식 단서 손실', 'low'),
    ('K-APTONG', [('압', {'NNG'}), ('통', {'NNG'})], '압통', '「압통」 이 압+통 으로 분할', '사건 명사 손실', 'low'),
    ('K-YUKAJONG', [('육아', {'NNG'}), ('종', {'NNG'})], '육아종', '「육아종」 이 육아+종 으로 분할', '사건 명사 손실(「육아」 오의미)', 'low'),
    ('K-NONGYANG', [('농', {'NNG'}), ('양', {'NNG'})], '농양', '「농양」 이 농+양 으로 분할', '사건 명사 손실', 'low'),
    ('K-HWANGSAEK', [('황', {'NNG'}), ('색', {'NNG'})], '황색', '「황색」 이 황+색 으로 분할', '색 표현 분할', 'low'),
    ('K-CHIMJA', [('침', {'NNG'}), ('자', {'NNG'})], '침자', '「침자」 가 침+자 로 분할', '부위 표현 분할', 'low'),
    ('K-ULTUNG', [('울', {'NNG'}), ('퉁', {'MAG'})], '울퉁', '「울퉁」 이 울/NNG+퉁/MAG 로 분할', '질감 표현 분할', 'low'),
    ('K-SMOOTHING', [('스무', {'MM'}), ('딩', {'MAG'})], '스무딩', '외래어 「스무딩」 이 스무/MM(수 관형사)+딩/MAG', '수량(스무=20) 오탐 위험, 관리 행위명 손실', 'medium'),
    ('K-MISECHIM', [('미', {'NNP'}), ('세침', {'NNG'})], '미세침', '「미세침」 이 미/NNP+세침 으로 분할', '「미세」 정도 단서 손실', 'low'),
    ('K-GWA-NNG', [('과', {'NNG'}), ('교정', {'NNG'})], '과교정', '접두 「과」 가 NNG 로 분석(다른 출현은 XPN)', '과도 단서 품사 불일치', 'low'),
    ('K-GWA-NNG', [('과', {'NNG'}), ('색소', {'NNG'})], '과색소', '접두 「과」 가 NNG 로 분석', '과도 단서 품사 불일치', 'low'),
    ('K-LOANSPLIT', [('골든', {'NNG'}), ('타임', {'NNG'})], '골든타임', '외래어 복합어 분할(다른 출현은 NNP 한 토큰)', '대응 시한 표현이 두 토큰', 'low'),
    ('K-LOANSPLIT', [('터치', {'NNG'}), ('업', {'NNG'})], '터치업', '외래어 「터치업」 분할', '재시술 표현 분할', 'low'),
    ('K-ANGEOMHASU', [('안검', {'NNG'}), ('하수', {'NNG'})], '안검하수', '「안검하수」 분할(다른 출현은 NNP 한 토큰)', '「하수」 오의미', 'low'),
    ('K-MAG-NOUN', [('멍', {'MAG'})], '멍', '명사 「멍」 이 MAG(부사)', '사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락', 'medium'),
    ('K-MAG-NOUN', [('젤', {'MAG'})], '젤', '명사 「젤」 이 MAG', '물질 명사 오태깅', 'low'),
    ('K-MAG-NOUN', [('깊이', {'MAG'})], '깊이', '명사 「깊이」 가 MAG(부사 「깊이」)', '깊이(대상 속성) 를 부사로 오태깅', 'medium'),
]

def collect_known(applied):
    out = []
    for a in applied:
        toks = a['tokens']
        for k in range(len(toks)):
            for rid, seq, surface, desc, impact, sev in SEQ_RULES:
                w = len(seq)
                if k + w > len(toks): continue
                if not all(toks[k+j]['form'] == f and toks[k+j]['tag'] in tags for j, (f, tags) in enumerate(seq)): continue
                s, e = toks[k]['start'], toks[k+w-1]['end']
                if not a['text'][s:].startswith(surface): continue
                out.append(OrderedDict(rule=rid, pointer=a['pointer'], token_index=list(range(k, k + w)),
                                       span=[s, s + len(surface)], surface=surface,
                                       raw=[f"{toks[x]['form']}/{toks[x]['tag']}" for x in range(k, k + w)],
                                       description=desc, impact=impact, severity=sev))
    return out

def collect_tag_variants(applied):
    """같은 표면 명사가 NNG 와 NNP 로 갈린 출현(분절 오류 아님, 품사 불일치)."""
    tags = {}
    for a in applied:
        for t in a['tokens']:
            if t['tag'] in ('NNG', 'NNP'): tags.setdefault(t['form'], set()).add(t['tag'])
    both = {f for f, ts in tags.items() if ts == {'NNG', 'NNP'}}
    out = []
    for a in applied:
        for t in a['tokens']:
            if t['form'] in both and t['tag'] == 'NNP':
                out.append(OrderedDict(pointer=a['pointer'], token_index=t['i'], span=[t['start'], t['end']], token=f"{t['form']}/NNP"))
    return sorted(both), out

# 출현별 수동 판정(manual/segmentation.txt): 포인터 | 구간 시작 | 원시 | 판정 | 영향
def load_seg_manual():
    path = os.path.join(HERE, 'manual', 'segmentation.txt')
    out = []
    if not os.path.exists(path): return out
    for ln, line in enumerate(open(path, encoding='utf-8').read().split('\n'), 1):
        if not line.strip() or line.startswith('#'): continue
        ptr, surface, occ, raw_t, verdict, impact = [x.strip() for x in line.split(' | ')]
        out.append(OrderedDict(pointer=ptr, surface=surface, occurrence=int(occ), raw=raw_t, verdict=verdict, impact=impact, manual_line=ln))
    return out

known = collect_known(applied)
tag_variant_forms, tag_variants = collect_tag_variants(applied)
seg_manual = load_seg_manual()
APPLIED = {a['pointer']: a for a in applied}
for r in seg_manual:
    v = APPLIED[r['pointer']]['text']; i = find_occ(v, r['surface'], r['occurrence'])
    assert i is not None, ('segmentation manual phrase not found', r)
    r['span'] = [i, i + len(r['surface'])]
    r['tokens_overlapping'] = [f"{t['form']}/{t['tag']}" for t in APPLIED[r['pointer']]['tokens'] if t['start'] < r['span'][1] and t['end'] > r['span'][0]]


# ---------------------------------------------------------------- 표현: 자동 후보(정규식) + 수동(직접 읽기)
AUTO_PATTERNS = OrderedDict([
    ('P-DAY', r'Day\s*\d+(?:\s*-\s*\d+)?'),
    ('P-NUMUNIT', r'\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)?\s*(?:분|시간|일|주|개월|도)(?:\s*(?:이상|이하|미만|초과|내|후|전|소요))?'),
    ('P-APPROXTIME', r'수\s?(?:분|시간|일|주|개월)(?:\s*-\s*수\s?(?:분|시간|일|주|개월))?(?:\s*(?:내|후에도|후|소요|지속))?'),
    ('P-SCALE', r'(?:통증 스케일|피부 타입)\s*[0-9IVX]+(?:\s*-\s*[0-9IVX]+)?(?:\s*이상)?'),
    ('P-COND-SI', r'[가-힣A-Za-z0-9·]+\s시(?=[\s,)]|$)'),
    ('P-AFTER', r'[가-힣A-Za-z0-9)]+\s?후(?:에도)?(?=[\s,)]|$)'),
    ('P-BEFORE', r'[가-힣]+\s전(?=[\s,)]|$)'),
    ('P-DURING', r'(?:시술|필링|진행)\s?중|직후|당일|즉시'),
    ('P-IF', r'[가-힣]+(?:으면|면)(?=\s)'),
    ('P-FREQ', r'극히 드묾|드묾|드물[게다]?|흔함|흔히|대개|간헐적'),
    ('P-DEGREE', r'경미한|심한|심함|심화|약간의?|가벼운|뚜렷한|미세한?|강한|강함|작은|큰|광범위한?|비정상적(?:으로)?|과도한?|과다|급격한?|본격적으로|완전(?:히)?'),
    ('P-SPEED', r'점차|서서히|점진적|즉각적(?:인)?|느린 편|느림|조기'),
    ('P-TEMPORAL', r'아직|여전히|오히려|특히|본격적으로'),
    ('P-COURSE', r'지속(?:적|되는)?|잔존|잔여|소실|완화|감소|증가|악화|진행(?:성)?|재발|만성|영구|지연(?:성)?|시작|확대|확산|형성|정상화|개선|흡수|탈락|노출|돌출|이동'),
    ('P-NEG', r'안 |않|없음|없이|아닌|아님|미반응|미흡|미미|미입증|불량|불필요|불균일|무감각|부자연'),
    ('P-POSSIB', r'가능(?:성)?|수 있|우려|시사|고려'),
    ('P-ADVICE', r'필요|필수|주의|금지|금기|문의|연락|위험|선택|권장|자제|피하|삼가|모니터링|관찰|확인|판단'),
    ('P-DEPTH', r'깊이|깊은|깊게|얕|얇|두께|심부'),
    ('P-APPROX', r'거의|대부분|상당 부분|일부|약 \d|모든|가장|최대|최저점|가까운'),
    ('P-COMPARE', r'예상보다|[가-힣]+보다|더 |이상|이하|미만|초과'),
    ('P-SYMBOL', r'→|~|--|—|\+|\*\*'),
    ('P-ALT', r'[^\s/()+,:]+(?:/[^\s/()+,:]+)+'),
    ('P-LATIN', r'[A-Za-z][A-Za-z0-9]*(?:[ -][A-Za-z0-9]+)*'),
    ('P-SITE', r'주사 부위|시술 부위|침자 부위|실 삽입 부위|부위|주위|전신|안면(?: 전체)?|눈가|이마|목|가슴|턱선|입꼬리|눈꺼풀|가장자리|아래|밖|체내'),
    ('P-PAREN', r'\([^()]*\)'),
])
AUTO_RE = {k: re.compile(v) for k, v in AUTO_PATTERNS.items()}

expressions = []
def add_expr(ptr, s, e, source, kinds, note='', extra=None):
    v = NODE[ptr]['value']
    rec = OrderedDict(id=f'E{len(expressions)+1:05d}', pointer=ptr, segment=NODE[ptr]['segment'], span=[s, e], text=v[s:e],
                      source=source, kinds=kinds, note=note)
    if extra: rec.update(extra)
    expressions.append(rec)

# 값 전체(문맥 단위): 모든 문자열 말단
for n in strings:
    if n['value'] != '':
        add_expr(n['pointer'], 0, len(n['value']), 'value-whole', ['value_context'], '값 전체 — 문맥 단위')
# 자동 후보: 형태소 적용 대상 언어 텍스트에만
for a in applied:
    for pid, rx in AUTO_RE.items():
        for m in rx.finditer(a['text']):
            if m.end() > m.start():
                add_expr(a['pointer'], m.start(), m.end(), 'auto:' + pid, [pid], '정규식 후보(일치분만, 의미 판정 아님)')
# 수동
manual_errors = []
for seg, (mexprs, _, _) in MANUAL.items():
    for me in mexprs:
        if me['pointer'] not in NODE or NODE[me['pointer']]['type'] != 'string':
            manual_errors.append(('bad pointer', seg, me)); continue
        v = NODE[me['pointer']]['value']; i = find_occ(v, me['phrase'], me['occurrence'])
        if i is None: manual_errors.append(('phrase not found', seg, me)); continue
        add_expr(me['pointer'], i, i + len(me['phrase']), 'manual', me['kinds'], me['note'],
                 {'manual_file': f'manual/{seg}.txt', 'manual_line': me['manual_line']})
if manual_errors:
    for x in manual_errors: print('MANUAL ERROR', x, file=sys.stderr)
    sys.exit(2)

# 패턴 밖 잔여 점검: 수식·부정·조건 성격 품사 토큰 중 어떤 자동/수동 표현과도 겹치지 않는 것
RESID_TAGS = {'MAG', 'MAJ', 'MM', 'VA', 'XSA', 'VX', 'XPN', 'NR', 'SN'}
def covered(ptr, s, e, sources):
    return any(x['pointer'] == ptr and x['source'] != 'value-whole' and (x['source'] in sources or any(x['source'].startswith(p) for p in sources))
               and x['span'][0] < e and x['span'][1] > s for x in expressions)
residual = []
for a in applied:
    for t in a['tokens']:
        if t['tag'] in RESID_TAGS or t['form'] in ('안', '못', '않', '없', '미', '불', '무', '비'):
            ra = covered(a['pointer'], t['start'], t['end'], ['auto:'])
            rm = covered(a['pointer'], t['start'], t['end'], ['manual'])
            if not (ra and rm):
                residual.append(OrderedDict(pointer=a['pointer'], token=f"{t['form']}/{t['tag']}", span=[t['start'], t['end']],
                                            covered_auto=ra, covered_manual=rm))


# ---------------------------------------------------------------- 미결
GLOBAL_ISSUES_PATH = os.path.join(HERE, 'manual', 'global-issues.txt')
global_issues = []
for ln, line in enumerate(open(GLOBAL_ISSUES_PATH, encoding='utf-8').read().split('\n'), 1):
    if not line.strip() or line.startswith('#'): continue
    gid, cls, refs, body = [x.strip() for x in line.split(' | ', 3)]
    global_issues.append(OrderedDict(id=gid, cls=cls, refs=refs.split(), text=body, manual_line=ln))


# ---------------------------------------------------------------- 쓰기
def dump(name, obj):
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1); f.write('\n')

SPAN_UNITS = OrderedDict(
    literal_cp='원본 파일을 UTF-8 로 디코딩한 전체 문자열의 Unicode 코드포인트 인덱스 [start,end). 문자열은 따옴표 포함 JSON 리터럴',
    literal_byte='원본 파일 바이트 오프셋 [start,end). literal_cp 와 같은 리터럴',
    value_span='디코딩된 값 문자열(JSON 리터럴이 아님)의 코드포인트 [start,end). 이 원장은 이스케이프 0 이므로 값 시작 = literal_cp[0]+1',
    kiwi_offset='kiwipiepy Token.start/len 을 [start,start+len) 으로 기록. 분석 입력 = 디코딩 값 문자열 그대로(정규화 없음). source_slice 로 원문 대조')
SOURCE = OrderedDict(path=SRC_REL, sha256=SHA, bytes=len(raw), codepoints=len(text), newline_count=text.count('\n'),
                     backslash_escapes_in_strings=sum(1 for n in strings if n['escaped']), duplicate_keys=dups,
                     non_ascii=not raw.isascii(), nfc_normalized=(unicodedata.normalize('NFC', text) == text))

dump('source-map.json', OrderedDict(source=SOURCE, span_units=SPAN_UNITS,
     counts=OrderedDict(nodes=len(nodes), objects=sum(n['type'] == 'object' for n in nodes), arrays=sum(n['type'] == 'array' for n in nodes),
                        leaves=len(leaves), strings=len(strings), empty_containers=sum(1 for n in nodes if n['type'] in ('object', 'array') and n['empty']),
                        empty_strings=sum(1 for n in strings if n['empty'])),
     field_names=[OrderedDict(name=k, occurrences=field_name_occ[k], pointers=field_name_ptrs[k]) for k in sorted(field_name_occ, key=lambda x: (-field_name_occ[x], x))],
     nodes=nodes))

dump('morphology.json', OrderedDict(
    source=OrderedDict(path=SRC_REL, sha256=SHA),
    analyzer=OrderedDict(name='kiwipiepy', version=kiwipiepy.__version__, constructor="Kiwi(num_workers=1, model_type='cong')",
                         model_type='cong', num_workers=1, user_dictionary=None, load_default_dict='기본값(None → 라이브러리 기본)',
                         call='kiwi.tokenize(text) — 모든 옵션 기본값(normalize_coda=False, split_complex=False, match_options=Match.ALL, typos=None)',
                         tagset='Kiwi 품사 태그(세종 품사 체계 기반 + W_SERIAL 등 Kiwi 확장)', lemma='Token.lemma 를 도구 출력 그대로 기록. 도구에 없는 기본형을 만들지 않음',
                         runtime='uv run --python 3.12 --with kiwipiepy==0.24.1'),
    span_unit=SPAN_UNITS['kiwi_offset'],
    applied=applied, excluded_values=excluded,
    field_names=OrderedDict(status='excluded', reason='필드명은 전부 영문 식별자(snake/lower). 한국어 형태소 분석 대상이 아니다. 이름·출현 위치는 source-map.json field_names 에 전부 보존',
                            names=sorted(field_name_occ)),
    known_errors_rule=known, segmentation_manual=seg_manual,
    tag_variants=OrderedDict(definition='같은 표면 명사가 출현에 따라 NNG/NNP 로 갈림. 분절 오류는 아니며 품사 기준 집계 시 주의', forms=tag_variant_forms, nnp_occurrences=tag_variants),
    surface_mismatch_note='surface_match=false 는 Kiwi 가 어간·어미 결합을 풀어 낸 정상 출력(예: 심한 → 심하/VA+ᆫ/ETM)이 대부분이다. 원문 구간은 source_slice 로 보존',
    limits=['형태소 출력은 교정하지 않았다. 알려진 오분절은 known_errors_rule(규칙 서명)·segmentation_manual(출현별 직접 판정)에만 기록한다.',
            '영문 약어·혼합 표기(CO2·HIFU/RF·blanching·frost·TCA·PIH·papule·dimpling·III-V)는 Kiwi 가 SL/SN/W_SERIAL 등으로 출력하며 언어별 분석은 하지 않았다.',
            '기록된 판정 밖 토큰의 정확성은 보장하지 않는다.']))

dump('expressions.json', OrderedDict(
    source=OrderedDict(path=SRC_REL, sha256=SHA), span_unit=SPAN_UNITS['value_span'],
    method=OrderedDict(
        value_whole='모든 비어있지 않은 문자열 말단의 값 전체를 문맥 단위로 1건씩 둔다(ID/코드 포함 — 원문 보존 목적).',
        auto='형태소 적용 대상 값에 아래 정규식을 적용한 일치분만. 의미 판정·전수 수집이 아니다. 패턴 밖 표현은 auto 에 없다.',
        manual='직접 읽기에서 적은 구절(manual/S*.txt). 패턴 밖 형용사·부사·회피/권고·깊이·속도·근사·수치단위·「후/시」·「있으면」 조건 포함. kinds 는 탐색 관점 이름이며 확정 분류가 아니다.',
        patterns=AUTO_PATTERNS, overlap='구간 겹침은 의도된 것(값 전체 ⊃ 수동 구절 ⊃ 자동 후보 등). 같은 (pointer,span,source,kinds) 의 중복만 오류로 본다.'),
    counts=OrderedDict(total=len(expressions), by_source=dict(Counter(x['source'].split(':')[0] for x in expressions)),
                       auto_by_pattern=dict(Counter(x['source'][5:] for x in expressions if x['source'].startswith('auto:')))),
    residual_tokens=OrderedDict(definition='수식·부정·수량 성격 품사(MAG MAJ MM VA XSA VX XPN NR SN)와 부정 접두 토큰 중 auto 또는 manual 어느 한쪽에 덮이지 않은 것. 읽기 검토 점검표',
                                items=residual),
    expressions=expressions))

# 미결 묶음
all_issues = []
for seg, (_, _, iss) in MANUAL.items():
    for q in iss: q2 = OrderedDict(q); q2['segment'] = seg; all_issues.append(q2)
for g in global_issues: g2 = OrderedDict(g); g2['segment'] = 'GLOBAL'; all_issues.append(g2)

# coverage
coverage = OrderedDict(source=OrderedDict(path=SRC_REL, sha256=SHA),
    status_legend=OrderedDict(machine_extracted='build.py 가 구조·값·형태소·자동 후보를 생성함', direct_read='에이전트가 read_segment.py 출력으로 구획 원문을 위에서 아래로 읽고 manual/<구획>.txt 에 관찰·표현·미결을 적음',
                              planned='계획만 — 미독'),
    segments=[])
for s in SEGMENTS:
    mexprs, mobs, miss = MANUAL[s['id']]
    coverage['segments'].append(OrderedDict(
        id=s['id'], title=s['title'], pointer_range=OrderedDict(owns_prefixes=s['owns_prefixes'], owns_exact=s['owns_exact']),
        owned_pointers=s['owned_pointers'], owned_leaf_pointers=s['owned_leaf_pointers'], context_refs=s['context_refs'],
        machine_extracted=True, direct_read='done', direct_read_date='2026-11-09', manual_file=f'manual/{s["id"]}.txt',
        review_file=f'review-part-{s["id"]}.md', manual_expression_count=len(mexprs), observation_count=len(mobs), issue_count=len(miss),
        last_pointer_read=s['owned_leaf_pointers'][-1]))
dump('coverage.json', coverage)


# ---------------------------------------------------------------- Markdown
def md_cell(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s.replace('|', '\\|').replace('\n', ' ')

def jtype(n):
    return {'string': 'string', 'number': 'number', 'boolean': 'boolean', 'null': 'null', 'object': 'object', 'array': 'array'}[n['type']]

# 컬럼 구성 표
col_rows = OrderedDict()
for n in nodes:
    cp = n['column_path'] or '(root)'
    r = col_rows.setdefault(cp, OrderedDict(types=Counter(), count=0, example=None, lengths=Counter(), empties=0))
    r['types'][jtype(n)] += 1; r['count'] += 1
    if n['type'] == 'array': r['lengths'][n['length']] += 1
    if n.get('empty'): r['empties'] += 1
    if r['example'] is None: r['example'] = n

def nest_desc(n):
    if n['type'] == 'object': return 'object{' + ', '.join(n['keys']) + '}'
    if n['type'] == 'array':
        return 'array'
    return n['type']

def example_text(n):
    if n['type'] in ('object', 'array'): return '(컨테이너)'
    return md_cell(n['value'])

# 선택적 필드 판정: 같은 부모 패턴 아래 모든 객체에 있는지
parent_pattern_count = Counter(n['column_path'] or '(root)' for n in nodes if n['type'] == 'object')

head = []
head.append('# post-procedure-timeline.json — 1차 조사 (읽기용 목차)\n')
head.append('> 생성: build.py (재생성 시 이 파일도 다시 만들어진다). 수동 보완은 manual/ 에만 적는다.\n')
head.append('## 상태\n')
head.append('| 항목 | 상태 |\n|---|---|')
head.append('| **1차 범위 종료** | validation.md 참조(기계 검증 + 별도 읽기 검토 결과가 거기 있다) |')
head.append('| **원장 전체 완료** | **아님** — 원문 부족 B·잠정 P·후속 F·원문 불일치 I 가 열려 있다(issues.md) |')
head.append(f'| 전수 읽기 | 구획 {len(SEGMENTS)}/{len(SEGMENTS)} 직접 읽기(coverage.json direct_read=done) |')
head.append(f'| 구조·값 수집 | 노드 {len(nodes)} · 말단 {len(leaves)} (문자열 {len(strings)}) · 중복 키 {len(dups)} · 이스케이프 {SOURCE["backslash_escapes_in_strings"]} · 빈 컨테이너 {sum(1 for n in nodes if n["type"] in ("object","array") and n["empty"])} |')
head.append(f'| 형태소 | Kiwi {kiwipiepy.__version__} cong · 적용 {len(applied)}값 {sum(len(a["tokens"]) for a in applied)}토큰 · 제외 {len(excluded)}값(ID/코드) · 필드명 {len(field_name_occ)}종 제외(영문 식별자) · 알려진 오분절 서명 {len(SEQ_RULES)}개(규칙 ID {len({r[0] for r in SEQ_RULES})}종, 문맥 대조 후 등록) {len(known)}출현 · 출현별 추가 판정 {len(seg_manual)} · NNG/NNP 갈림 {len(tag_variants)}출현 |')
c = Counter(x['source'].split(':')[0] for x in expressions)
head.append(f'| 표현 | 값 전체 {c["value-whole"]} · 수동 {c["manual"]} · 자동 후보 {c["auto"]}(정규식 일치분만) |')
head.append(f'| 원본 | `{SRC_REL}` · sha256 `{SHA}` · {len(raw)} bytes · {len(text)} codepoints · 줄바꿈 {SOURCE["newline_count"]} |')
head.append('')
head.append('## 파일\n')
head.append('| 파일 | 내용 |\n|---|---|')
for f, d in [('review-part-S00.md … S10.md', '구획별 모든 값(원본 컬럼명·자료형·원문 값·Pointer)과 분리된 잠정 관찰·수동 표현·미결'),
             ('source-map.json', '원본 식별·해시, 모든 노드(컨테이너 포함)의 Pointer·자료형·값·리터럴 구간(코드포인트/바이트)·키 리터럴 구간·소유 구획, 필드명 출현'),
             ('morphology.json', '분석기 설정, 적용 값별 토큰(표면형·품사·도구 lemma·구간·원문 대조), 제외 값과 사유, 필드명 제외, 알려진 오분절'),
             ('expressions.json', '값 전체 문맥 단위 + 수동 구절 + 정규식 후보(패턴 목록 포함), 잔여 토큰 점검표'),
             ('coverage.json', '구획 계획·소유 Pointer 집합·공유 문맥·읽기 상태·대응 문서'),
             ('issues.md', '미결(A·B·C·K·P·F·I)'), ('validation.md', '검증 명령·결과·별도 읽기 검토'), ('progress.md', '재개 위치'),
             ('manual/', '직접 읽기 기록(구획별 S*.txt, segmentation.txt, global-issues.txt)'), ('build.py · verify.py · read_segment.py', '재생성 · 독립 검증 · 구획 원문 출력')]:
    head.append(f'| {f} | {d} |')
head.append('')
head.append('## 컬럼 구성\n')
head.append('원본 컬럼명(경로 패턴, 배열 인덱스 = `*`) 그대로. 예시는 첫 출현의 원문 값과 Pointer.\n')
head.append('| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 구조 | 출현 수 | 배열 길이 분포 | 빈 값 | 필수/선택 | 원문 예시 | 예시 위치 |\n|---|---|---|---|---|---|---|---|')
for cp, r in col_rows.items():
    ex = r['example']
    types = ', '.join(f'{k}×{v}' for k, v in r['types'].items())
    nest = nest_desc(ex)
    lens = ', '.join(f'{k}:{v}' for k, v in sorted(r['lengths'].items())) if r['lengths'] else ''
    parent_cp = cp.rsplit('/', 1)[0] if '/' in cp else '(root)'
    parent_cp = parent_cp or '(root)'
    if cp == '(root)': req = '루트'
    elif cp.endswith('/*'): req = '배열 원소'
    else: req = '모든 부모에 있음' if r['count'] == parent_pattern_count.get(parent_cp, 0) else f'선택({r["count"]}/{parent_pattern_count.get(parent_cp,0)})'
    head.append(f'| `{cp}` | {types} · {md_cell(nest)} | {r["count"]} | {lens} | {r["empties"]} | {req} | {example_text(ex)} | `{ex["pointer"] or "(root)"}` |')
head.append('')
head.append('## 구획 목차\n')
head.append('| 구획 | 범위 | 소유 노드 / 말단 | 직접 읽기 | 문서 |\n|---|---|---|---|---|')
for s in SEGMENTS:
    head.append(f'| {s["id"]} | {md_cell(s["title"])} | {len(s["owned_pointers"])} / {len(s["owned_leaf_pointers"])} | done | [review-part-{s["id"]}.md](./review-part-{s["id"]}.md) |')
head.append('')
TIME_KINDS = {'period','reference_point','time_range','approx_time','onset','onset_time','onset_speed','peak','peak_time','duration','duration_threshold','persistence','resolution','recovery','delay','delayed_onset','chronicity','permanence','action_time','action_window','time_anchor','temporal','evaluation_time','retreatment','retreatment_decision','management','activity','avoidance','caution_period','obligation','sequence','speed','recurrence','condition','trough','completion'}
head.append('## 시간·경과·관리·대응·재시술 표현 색인 (직접 읽기 구절, 역할은 잠정)\n')
head.append('기준 시점·발현·피크·지속·소실/회복·지연·관리·응급 대응 시한·재시술 관련 수동 구절 전부. 「소속 period」 는 원문 구조상 그 값이 들어 있는 기간이며, 값 속 시간의 기준 시점은 대부분 원문에 없다(issues G-B2). 역할 이름은 탐색 관점이지 확정 분류가 아니다.\n')
head.append('| Pointer | 소속 period | 원본 컬럼명 | 원문 구절 | 잠정 역할 |\n|---|---|---|---|---|')
for x in expressions:
    if x['source'] != 'manual' or not (set(x['kinds']) & TIME_KINDS): continue
    m = re.match(r'^(/timelines/\d+/phases/\d+)', x['pointer'])
    per = md_cell(NODE[m.group(1) + '/period']['value']) if m else '-'
    head.append(f"| `{x['pointer']}` | {per} | `{NODE[x['pointer']]['field'] or NODE[x['pointer']]['parent'].rsplit('/',1)[-1]}` | {md_cell(x['text'])} | {', '.join(sorted(set(x['kinds']) & TIME_KINDS))} |")
head.append('')
head.append('## 원장 전체에 걸친 관찰(잠정)\n')
head.append('원문 값은 각 구획 문서에 있다. 아래는 근거 위치를 붙인 잠정 관찰이며 의미 확정이 아니다.\n')
for g in global_issues:
    if g['cls'] == 'O':
        head.append(f'- **{g["id"]}** {g["text"]} — 근거: {", ".join("`"+r+"`" for r in g["refs"])}')
head.append('')
open(os.path.join(HERE, 'review.md'), 'w', encoding='utf-8').write('\n'.join(head) + '\n')

# 구획 문서
EXPR_BY_PTR = {}
for x in expressions: EXPR_BY_PTR.setdefault(x['pointer'], []).append(x)
for s in SEGMENTS:
    mexprs, mobs, miss = MANUAL[s['id']]
    L = [f'# {s["id"]} — {s["title"]}\n', '> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.\n',
         f'- 소유 범위: prefix {s["owns_prefixes"]} · exact {s["owns_exact"]}', f'- 공유 문맥(소유 아님): {s["context_refs"] or "없음"}',
         f'- 직접 읽기: done (manual/{s["id"]}.txt) · 마지막 읽은 Pointer `{s["owned_leaf_pointers"][-1]}`', '']
    L.append('## 1. 원문 — 모든 노드 (문서 순서)\n')
    L.append('| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |\n|---|---|---|---|---|---|')
    k = 0
    for n in nodes:
        if n['segment'] != s['id']: continue
        k += 1
        if n['type'] == 'object': val = '{' + ', '.join(n['keys']) + '}' + (' (빈 객체)' if n['empty'] else '')
        elif n['type'] == 'array': val = f'[길이 {n["length"]}]' + (' (빈 배열)' if n['empty'] else '')
        else: val = md_cell(n['value'])
        L.append(f'| {k} | `{n["pointer"] or "(root)"}` | `{n["field"] if n["field"] is not None else ("[" + str(n.get("index")) + "]" if n.get("index") is not None else "(root)")}` | {jtype(n)} | {val} | {n["literal_cp"][0]}–{n["literal_cp"][1]} |')
    L.append('')
    if s['id'] != 'S00':
        L.append('## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)\n')
        t = resolve(s['owns_prefixes'][0])
        L.append(f'`id` = {md_cell(t["id"])} · `category` = {md_cell(t["category"])} · `name` = {md_cell(t["name"])}\n')
        for pi, ph in enumerate(t['phases']):
            base = f'{s["owns_prefixes"][0]}/phases/{pi}'
            L.append(f'### phases/{pi} — `period` = {md_cell(ph["period"])} · `label` = {md_cell(ph["label"])}\n')
            L.append('| 원본 컬럼명 | 순서 | 원문 값 | Pointer |\n|---|---|---|---|')
            for lv in LEVEL_KEYS:
                for vi, v in enumerate(ph[lv]):
                    L.append(f'| `{lv}` | {vi} | {md_cell(v)} | `{base}/{lv}/{vi}` |')
            L.append('')
    L.append('## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리\n')
    L.append('| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |\n|---|---|---|---|---|')
    for x in expressions:
        if x['segment'] == s['id'] and x['source'] == 'manual':
            L.append(f'| `{x["pointer"]}` | [{x["span"][0]},{x["span"][1]}) | {md_cell(x["text"])} | {", ".join(x["kinds"])} | {md_cell(x["note"])} |')
    L.append('')
    L.append('## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)\n')
    cc = Counter(x['source'][5:] for x in expressions if x['segment'] == s['id'] and x['source'].startswith('auto:'))
    L.append(', '.join(f'{k} {v}' for k, v in sorted(cc.items())) or '없음')
    L.append('\n전체 목록은 expressions.json (segment 필터).\n')
    L.append('## 5. 잠정 관찰\n')
    for o in mobs: L.append(f'- **{o["id"]}** {o["text"]}')
    L.append('')
    L.append('## 6. 미결 (이 구획)\n')
    L.append('| ID | 분류 | 위치 | 내용 |\n|---|---|---|---|')
    for q in miss: L.append(f'| {q["id"]} | {q["cls"]} | {" ".join("`"+r+"`" for r in q["refs"])} | {md_cell(q["text"])} |')
    L.append('')
    kn = [r for r in known if NODE[r['pointer']]['segment'] == s['id']]
    sm = [r for r in seg_manual if NODE[r['pointer']]['segment'] == s['id']]
    L.append('## 7. 형태소 — 알려진 오분절 (교정 안 함)\n')
    L.append('| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |\n|---|---|---|---|---|')
    for r in kn: L.append(f'| `{r["pointer"]}` | [{r["span"][0]},{r["span"][1]}) | {" + ".join(r["raw"])} | {r["rule"]} {r["description"]} | {r["impact"]} |')
    for r in sm: L.append(f'| `{r["pointer"]}` | [{r["span"][0]},{r["span"][1]}) | {md_cell(r["raw"])} | {md_cell(r["verdict"])} | {md_cell(r["impact"])} |')
    L.append('')
    open(os.path.join(HERE, f'review-part-{s["id"]}.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# issues.md
cls_name = OrderedDict(A='에이전트 추출/해석 오류', B='원문 정보 부족', C='현재 사용자 결정 필요', K='알려진 분석 한계', P='잠정', F='후속 의미 조사', I='원문 내 불일치', O='전체 관찰(잠정)')
I = ['# 미결 — post-procedure-timeline.json\n', '> build.py 생성. 원천은 manual/S*.txt 의 Q 줄과 manual/global-issues.txt.\n',
     '분류: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · K=알려진 분석 한계 · P=잠정 · F=후속 의미 조사 · I=원문 내 불일치. 원문 내 불일치는 C 가 아니다.\n']
cnt = Counter(q['cls'] for q in all_issues if q['cls'] != 'O')
I.append('## 집계\n\n| 분류 | 건수 |\n|---|---|')
for k in 'ABCKPFI': I.append(f'| {k} {cls_name[k]} | {cnt.get(k, 0)} |')
I.append('')
I.append('**C(사용자 결정 필요) 0건의 근거:** 아래 B 는 원문에 정보가 없는 것이라 사용자 추측으로 채울 대상이 아니고, P·F 는 21개 원장 비교 후 의미 설계 단계에서 묶어 다룰 과제이며, I 는 원본 보존 지시 아래 후속 확인 후보다. 도구 선택(형태소 설정)은 에이전트가 정해 기록했다. 따라서 현재 사용자에게 선택을 요청할 항목은 없다. 이것은 미결이 닫혔다는 뜻이 아니다.\n')
for k in 'ABCKPFI':
    rows = [q for q in all_issues if q['cls'] == k]
    I.append(f'## {k} — {cls_name[k]} ({len(rows)})\n')
    if not rows: I.append('없음.\n'); continue
    I.append('| ID | 구획 | 위치 | 내용 | 상태 |\n|---|---|---|---|---|')
    for q in rows:
        st = {'A': '해결됨(아래 validation 참조)', 'B': '열림', 'C': '-', 'K': '기록됨(교정 안 함)', 'P': '열림(잠정)', 'F': '열림(후속)', 'I': '열림(원본 보존, 후속 확인 후보)'}[k]
        I.append(f'| {q["id"]} | {q["segment"]} | {" ".join("`"+r+"`" for r in q["refs"])} | {md_cell(q["text"])} | {st} |')
    I.append('')
I.append(f'## K 상세 — 알려진 형태소 오분절 출현\n\n규칙 서명 {len(known)}출현 + 출현별 직접 판정 {len(seg_manual)}건. 위치·원시 토큰은 morphology.json known_errors_rule / segmentation_manual, 구획별로는 review-part 7절.\n')
I.append('| 규칙/판정 | 출현 수 |\n|---|---|')
for k2, v in Counter(r['rule'] for r in known).items(): I.append(f'| {k2} | {v} |')
for k2, v in Counter(r['verdict'].split(' ')[0] for r in seg_manual).items(): I.append(f'| 직접 판정 {md_cell(k2)} | {v} |')
I.append('')
open(os.path.join(HERE, 'issues.md'), 'w', encoding='utf-8').write('\n'.join(I) + '\n')

print(json.dumps(OrderedDict(sha256=SHA, nodes=len(nodes), leaves=len(leaves), strings=len(strings), applied=len(applied), excluded=len(excluded),
                             tokens=sum(len(a['tokens']) for a in applied), expressions=len(expressions), by_source=dict(c),
                             known=len(known), seg_manual=len(seg_manual), residual=len(residual), issues=dict(cnt), dups=len(dups)), ensure_ascii=False))
