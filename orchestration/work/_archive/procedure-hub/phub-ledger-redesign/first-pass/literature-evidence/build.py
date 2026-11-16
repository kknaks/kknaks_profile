#!/usr/bin/env python3
"""literature-evidence.json 1차 수집 재현 스크립트.

실행(레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/build.py

원본은 읽기만 한다. 쓰기는 이 폴더 안(OUT)뿐이다.
manual/S??.json (직접 읽기 기록)을 읽어 review-part·expressions·coverage 에 반영한다.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
SRC_REL = 'orchestration/work/phub-recommend/bronze/phub-ledger/literature-evidence.json'
SRC = os.path.join(REPO, SRC_REL)
MANUAL = os.path.join(HERE, 'manual')


# ---------------------------------------------------------------- 원문 스캐너
class Scanner:
    """JSON 원문을 직접 훑어 모든 노드의 위치·리터럴·중복 키를 기록한다.

    위치 단위: file_cp = 디코딩한 파일 텍스트(UTF-8)의 코드포인트 [start,end),
    file_byte = 파일 바이트 [start,end). 문자열 노드의 값 구간은 따옴표 포함 리터럴.
    """

    def __init__(self, text, raw):
        self.t = text
        self.i = 0
        self.nodes = []
        self.dup_keys = []
        # 코드포인트 → 바이트 오프셋 누적표
        self.cp2b = [0] * (len(text) + 1)
        b = 0
        for k, ch in enumerate(text):
            self.cp2b[k] = b
            b += len(ch.encode('utf-8'))
        self.cp2b[len(text)] = b
        assert b == len(raw)

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in ' \t\r\n':
            self.i += 1

    def string(self):
        t = self.t
        assert t[self.i] == '"', self.i
        s = self.i
        self.i += 1
        out = []
        cmap = []  # 디코딩 문자 k → 원문 리터럴 내 cp [a,b)
        while True:
            ch = t[self.i]
            if ch == '"':
                self.i += 1
                break
            if ch == '\\':
                a = self.i
                e = t[self.i + 1]
                if e == 'u':
                    code = int(t[self.i + 2:self.i + 6], 16)
                    self.i += 6
                    if 0xD800 <= code < 0xDC00 and t[self.i:self.i + 2] == '\\u':
                        lo = int(t[self.i + 2:self.i + 6], 16)
                        self.i += 6
                        code = 0x10000 + ((code - 0xD800) << 10) + (lo - 0xDC00)
                    out.append(chr(code))
                else:
                    out.append({'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f',
                                'n': '\n', 'r': '\r', 't': '\t'}[e])
                    self.i += 2
                cmap.append([a, self.i])
            else:
                out.append(ch)
                cmap.append([self.i, self.i + 1])
                self.i += 1
        return ''.join(out), s, self.i, cmap

    def value(self, ptr, parent, key_info, order):
        self.ws()
        t = self.t
        s = self.i
        node = {'pointer': ptr, 'parent': parent, **key_info, 'order': order}
        self.nodes.append(node)
        ch = t[self.i]
        if ch == '{':
            node['type'] = 'object'
            self.i += 1
            self.ws()
            seen = {}
            n = 0
            if t[self.i] == '}':
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke, _ = self.string()
                    if k in seen:
                        self.dup_keys.append({'object': ptr, 'key': k, 'first_cp': seen[k], 'dup_cp': [ks, ke]})
                    seen[k] = [ks, ke]
                    self.ws()
                    assert t[self.i] == ':'
                    self.i += 1
                    cp = ptr + '/' + k.replace('~', '~0').replace('/', '~1')
                    self.value(cp, ptr, {'key': k, 'key_literal': t[ks:ke], 'key_file_cp': [ks, ke],
                                         'index': None}, n)
                    n += 1
                    self.ws()
                    if t[self.i] == ',':
                        self.i += 1
                        continue
                    assert t[self.i] == '}'
                    self.i += 1
                    break
            node['child_count'] = n
        elif ch == '[':
            node['type'] = 'array'
            self.i += 1
            self.ws()
            n = 0
            if t[self.i] == ']':
                self.i += 1
            else:
                while True:
                    self.value(ptr + '/' + str(n), ptr, {'key': None, 'key_literal': None, 'key_file_cp': None,
                                                         'index': n}, n)
                    n += 1
                    self.ws()
                    if t[self.i] == ',':
                        self.i += 1
                        continue
                    assert t[self.i] == ']'
                    self.i += 1
                    break
            node['child_count'] = n
        elif ch == '"':
            v, a, b, cmap = self.string()
            node['type'] = 'string'
            node['value'] = v
            node['decoded_len_cp'] = len(v)
            node['literal_equals_decoded'] = (t[a + 1:b - 1] == v)
            # 디코딩 문자 k → 파일 cp. 이스케이프가 있을 때만 표를 남긴다.
            node['_cmap'] = cmap
        else:
            m = re.compile(r'-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null').match(t, self.i)
            lit = m.group(0)
            self.i = m.end()
            if lit in ('true', 'false'):
                node['type'], node['value'] = 'boolean', lit == 'true'
            elif lit == 'null':
                node['type'], node['value'] = 'null', None
            elif m.group(1) or m.group(2):
                node['type'], node['value'] = 'number_float', float(lit)
            else:
                node['type'], node['value'] = 'number_int', int(lit)
        e = self.i
        node['file_cp'] = [s, e]
        node['file_byte'] = [self.cp2b[s], self.cp2b[e]]
        node['literal'] = t[s:e] if node['type'] not in ('object', 'array') else None
        node['is_leaf'] = node['type'] not in ('object', 'array') or node.get('child_count') == 0
        return node


def scan(raw):
    text = raw.decode('utf-8')
    sc = Scanner(text, raw)
    sc.value('', None, {'key': None, 'key_literal': None, 'key_file_cp': None, 'index': None}, 0)
    sc.ws()
    assert sc.i == len(text), 'trailing data'
    return text, sc


# ---------------------------------------------------------------- 구획
def segment_of(ptr):
    m = re.match(r'^/categories/(M\d+)(/|$)', ptr)
    if m:
        return 'S%02d' % int(m.group(1)[1:])
    return 'S00'


SEG_TITLE = {'S00': '상위 메타데이터 · /version · /updated · /source_method · /accuracy_summary · /categories 컨테이너'}
for _i in range(1, 18):
    SEG_TITLE['S%02d' % _i] = '/categories/M%d' % _i


# ---------------------------------------------------------------- 형태소 적용/제외
KO_FIELDS = {'patient_ko', 'accuracy_note'}
HANGUL = re.compile('[\uac00-\ud7a3\u1100-\u11ff\u3131-\u318e]+')


def field_of(node):
    return node['key'] if node['key'] is not None else None


def morph_policy(node):
    """string 노드마다 (applied, kind, reason). 숫자 노드는 non_string 으로 기록."""
    p = node['pointer']
    f = field_of(node)
    if node['type'] != 'string':
        return False, 'non_string', '%s 값(%s). 언어 텍스트 아님' % (node['type'], node['literal'])
    if p == '/accuracy_summary/rubric':
        return True, 'ko_text', '한국어 혼합 텍스트(채점 기준 설명)'
    if f in KO_FIELDS:
        return True, 'ko_text', '한국어 텍스트 필드(%s)' % f
    if f in ('patient_en', 'statement', 'name', 'source_method', 'scored_by'):
        return False, 'en_text', '영어 텍스트. Kiwi 는 한국어 분석기라 적용하지 않음. 원문은 source-map·직접 읽기·수동 표현으로 보존(K-ENG)'
    if f in ('patient_zh',):
        return False, 'zh_text', '중국어 텍스트. Kiwi 적용 범위 밖(K-ZHJA). 직접 읽기·혼입 문자 검사로 보존'
    if f in ('patient_ja',):
        return False, 'ja_text', '일본어 텍스트. Kiwi 적용 범위 밖(K-ZHJA). 한글 혼입은 expressions 에 I 로 기록'
    if f in ('title', 'journal', 'authors'):
        return False, 'bibliographic', '서지 정보(영어 논문 제목·저널·저자). 언어 분석 대상 아님. 원문 보존'
    if f in ('pmid', 'doi', 'pmc', 'oa_url'):
        return False, 'id_code', '외부 식별자·URL(%s)' % f
    if f in ('version', 'updated', 'added_at'):
        return False, 'version_date', '버전·날짜 문자열'
    if f in ('patient_ko_coverage', 'ko', 'en', 'zh', 'ja'):
        return False, 'ratio_code', '"n/m" 형식 집계 문자열'
    raise SystemExit('정책 없는 string 노드: ' + p)


# ---------------------------------------------------------------- 보조 정규식(후보)
REGEX = [
    ('ko_possibility', re.compile(r'(?:[가-힣]+[ㄹ을를]?\s?)?수\s?(?:있|없)[가-힣]*')),
    ('ko_negation', re.compile(r'[가-힣]*(?:않|없|못|아니|비[가-힣]|무[가-힣]|불[가-힣])[가-힣]*')),
    ('ko_degree', re.compile(r'(?:더|덜|매우|약간|가장|크게|작게|심해|강한|가벼운|경미|드물|흔[히하])[가-힣]*')),
    ('citation_marker', re.compile(r'(?:\[\d+\])+')),
    ('number_unit', re.compile(r'\d+(?:\.\d+)?\s?(?:%|nm|mm|cm|mL|ml|mg|J|W|MHz|Hz|weeks?|months?|days?|years?|주|개월|일|년|회)?')),
    ('en_hedge', re.compile(r'\b(?:may|might|can|could|rarely|rare|often|commonly|common|usually|typically|generally|frequently|occasionally|possibly|potential(?:ly)?|likely|unlikely|suggest(?:s|ed)?)\b', re.I)),
    ('en_negation', re.compile(r'\b(?:no|not|non-?\w+|without|never|neither|nor|un\w+|in(?:effective|sufficient))\b', re.I)),
    ('en_compare', re.compile(r'\b(?:more|less|greater|lower|higher|than|compared|versus|vs\.?|superior|inferior|similar|comparable|better|worse)\b', re.I)),
    ('en_condition', re.compile(r'\b(?:if|when|unless|after|before|during|following|in patients with|in combination|combined with)\b', re.I)),
    ('mixed_hangul', HANGUL),
]
REGEX_FIELDS = {'statement', 'patient_ko', 'patient_en', 'accuracy_note', 'patient_zh', 'patient_ja', 'name',
                'source_method', 'scored_by', 'rubric'}


def main():
    raw = open(SRC, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    text, sc = scan(raw)
    nodes = sc.nodes
    by_ptr = {}
    for n in nodes:
        assert n['pointer'] not in by_ptr, 'pointer 중복 ' + n['pointer']
        by_ptr[n['pointer']] = n

    # 원문 재현 자기점검
    py = json.loads(raw)
    for n in nodes:
        if n['type'] not in ('object', 'array'):
            cur = py
            for part in n['pointer'].split('/')[1:]:
                part = part.replace('~1', '/').replace('~0', '~')
                cur = cur[int(part)] if isinstance(cur, list) else cur[part]
            assert cur == n['value'] and type(cur) is type(n['value']), n['pointer']

    # ------------------------------------------------ source-map
    sm_nodes = []
    for n in nodes:
        rec = {k: v for k, v in n.items() if not k.startswith('_')}
        rec['segment'] = segment_of(n['pointer'])
        if n['type'] == 'string' and not n['literal_equals_decoded']:
            rec['decoded_to_file_cp'] = n['_cmap']
        sm_nodes.append(rec)
    source_map = {
        'source': {'path': SRC_REL, 'sha256': sha, 'bytes': len(raw), 'codepoints': len(text),
                   'lines': raw.count(b'\n'), 'encoding': 'utf-8', 'bom': raw.startswith(b'\xef\xbb\xbf')},
        'units': {
            'file_cp': '디코딩한 파일 텍스트의 Unicode 코드포인트 [start,end). 문자열은 따옴표 포함 JSON 리터럴 구간',
            'file_byte': '파일 UTF-8 바이트 [start,end)',
            'key_file_cp': '키 리터럴(따옴표 포함) 파일 코드포인트 구간',
            'value': '디코딩 값(JSON 이스케이프 해제)',
            'literal': 'JSON 리터럴 원문 그대로(이스케이프 포함). 컨테이너는 null',
            'decoded_to_file_cp': '이스케이프가 있는 문자열만: 디코딩 문자 k 의 원문 파일 cp [a,b)',
            'order': '부모 안에서의 출현 순서(0부터). 배열은 index 와 같다',
        },
        'parse': {'parser': 'build.py Scanner(직접 구현) + json.loads 값 대조', 'duplicate_keys': sc.dup_keys,
                  'node_count': len(nodes), 'leaf_count': sum(1 for n in nodes if n['is_leaf']),
                  'escaped_strings': [n['pointer'] for n in nodes if n['type'] == 'string' and not n['literal_equals_decoded']]},
        'nodes': sm_nodes,
    }

    # ------------------------------------------------ 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type='cong')
    tok_opts = dict(normalize_coda=False, z_coda=True, split_complex=False, compatible_jamo=False, saisiot=None)
    seg_review = json.load(open(os.path.join(HERE, 'segmentation-review.json'), encoding='utf-8'))
    SEG_RULES = seg_review['rules']
    seg_occ = []
    morph_values = []
    applied_ptrs = []
    excluded = []
    for n in nodes:
        if not n['is_leaf'] or n['type'] in ('object', 'array'):
            continue
        ok, kind, reason = morph_policy(n)
        if not ok:
            excluded.append({'pointer': n['pointer'], 'field': n['key'], 'kind': kind, 'reason': reason})
            continue
        v = n['value']
        toks = kiwi.tokenize(v, **tok_opts)
        tl = []
        for k, t in enumerate(toks):
            s, e = t.start, t.start + t.len
            tl.append({'i': k, 'form': t.form, 'tag': t.tag, 'lemma': t.lemma, 'start': s, 'end': e,
                       'surface': v[s:e], 'word_position': t.word_position, 'sent_position': t.sent_position,
                       'oov': bool(t.oov) if hasattr(t, 'oov') else None,
                       'file_cp': [n['file_cp'][0] + 1 + s, n['file_cp'][0] + 1 + e]})
        applied_ptrs.append(n['pointer'])
        for rule in SEG_RULES:
            sig = rule['signature']
            for a in range(len(tl) - len(sig) + 1):
                if all(tl[a + j]['form'] == sig[j][0] and tl[a + j]['tag'] == sig[j][1] for j in range(len(sig))):
                    s0, e0 = tl[a]['start'], tl[a + len(sig) - 1]['end']
                    for j in range(len(sig)):
                        tl[a + j].setdefault('known_issue', []).append(rule['id'])
                    seg_occ.append({'rule': rule['id'], 'pointer': n['pointer'], 'token_index': [a, a + len(sig)],
                                    'span_in_value': [s0, e0], 'surface': v[s0:e0],
                                    'raw_tokens': [[tl[a + j]['form'], tl[a + j]['tag']] for j in range(len(sig))],
                                    'file_cp': [n['file_cp'][0] + 1 + s0, n['file_cp'][0] + 1 + e0]})
        morph_values.append({'pointer': n['pointer'], 'field': n['key'], 'segment': segment_of(n['pointer']),
                             'text': v, 'token_count': len(tl), 'tokens': tl})
    # 필드명(키) 분석: 모든 키는 영어 snake_case/코드 → 적용 제외, 출현 위치 기록
    key_occ = {}
    for n in nodes:
        if n['key'] is not None:
            key_occ.setdefault(n['key'], []).append(n['pointer'])
    field_names = [{'key': k, 'occurrences': len(v), 'first_pointer': v[0],
                    'morph': 'excluded',
                    'reason': ('카테고리 ID 키(Mxx). 식별자' if re.fullmatch(r'M\d+', k) else
                               '언어 코드 키' if k in ('ko', 'en', 'zh', 'ja') else
                               '영어 snake_case 필드명. Kiwi 대상 아님. 원본 컬럼명은 review 에 그대로 보존')}
                   for k, v in key_occ.items()]
    morphology = {
        'source_sha256': sha,
        'analyzer': {'name': 'kiwipiepy', 'version': kiwipiepy.__version__, 'model_type': 'cong',
                     'num_workers': 1, 'user_dictionary': None,
                     'builtin_dictionary': 'kiwipiepy_model 기본(load_default_dict 기본값, typo 사전 미사용)',
                     'tokenize_options': tok_opts, 'match_options': 'Match.ALL(기본)',
                     'tagset': 'Kiwi 품사 태그(세종 기반 + SL/SN/SH/SW/W_* 등)',
                     'run': 'uv run --python 3.12 --with kiwipiepy==0.24.1'},
        'lemma': 'Kiwi Token.lemma 를 그대로 기록. 도구가 주지 않은 기본형을 만들지 않았다',
        'offsets': 'start/end = 분석에 넣은 디코딩 값의 코드포인트 [start,end). file_cp = 리터럴 시작+1+start (적용 값은 모두 이스케이프 없음 — verify 가 확인)',
        'surface': '디코딩 값[start:end]. form 과 다를 수 있다(ᆫ·ᆯ·ᆷ 어미는 앞 글자 구간을 공유하거나 길이 1 로 겹친다)',
        'policy_note': '적용 = patient_ko · accuracy_note · /accuracy_summary/rubric. 그 밖의 string 은 excluded 에 사유와 함께. 숫자 노드도 excluded(non_string)',
        'segmentation_review': {'source': 'segmentation-review.json', 'rules': SEG_RULES, 'notes': seg_review['notes'],
                                'method': seg_review['note'], 'occurrences': seg_occ,
                                'counts': {r['id']: sum(1 for o in seg_occ if o['rule'] == r['id']) for r in SEG_RULES}},
        'values': morph_values,
        'excluded': excluded,
        'field_names': field_names,
    }

    for r in SEG_RULES:
        if not any(o['rule'] == r['id'] for o in seg_occ):
            raise SystemExit('분절 규칙이 한 번도 맞지 않음: ' + r['id'])

    # ------------------------------------------------ 수동 기록
    manual = {}
    for fn in sorted(os.listdir(MANUAL)) if os.path.isdir(MANUAL) else []:
        if re.fullmatch(r'S\d\d\.json', fn):
            manual[fn[:3]] = json.load(open(os.path.join(MANUAL, fn), encoding='utf-8'))

    # ------------------------------------------------ 표현
    exprs = []

    def add_expr(ptr, s, e, facets, origin, status, note=None, src_id=None):
        n = by_ptr[ptr]
        v = n['value']
        rec = {'pointer': ptr, 'field': n['key'], 'segment': segment_of(ptr), 'span_in_value': [s, e],
               'text': v[s:e], 'facets': facets, 'origin': origin, 'status': status}
        cm = n['_cmap']
        rec['file_cp'] = [cm[s][0], cm[e - 1][1]] if e > s else None
        rec['file_byte'] = [sc.cp2b[rec['file_cp'][0]], sc.cp2b[rec['file_cp'][1]]]
        if note:
            rec['note'] = note
        if src_id:
            rec['manual_id'] = src_id
        exprs.append(rec)
        return rec

    manual_errors = []
    for seg, m in manual.items():
        for x in m.get('expressions', []):
            ptr = x['pointer']
            v = by_ptr[ptr]['value']
            occ = x.get('occurrence', 0)
            pos = -1
            for _ in range(occ + 1):
                pos = v.find(x['text'], pos + 1)
            if pos < 0:
                manual_errors.append({'segment': seg, 'id': x.get('id'), 'pointer': ptr, 'text': x['text']})
                continue
            add_expr(ptr, pos, pos + len(x['text']), x['facets'], 'manual', x.get('status', 'P'),
                     x.get('note'), x.get('id'))
    if manual_errors:
        print('MANUAL TEXT NOT FOUND', json.dumps(manual_errors, ensure_ascii=False, indent=1))
        sys.exit(2)
    rr = json.load(open(os.path.join(HERE, 'regex-review.json'), encoding='utf-8'))
    REGEX_VERDICTS = {(x['pointer'], x['span_in_value'][0], x['span_in_value'][1], x['regex']): x['reason'] for x in rr['verdicts']}
    manual_spans = {(e['pointer'], tuple(e['span_in_value'])) for e in exprs}
    manual_by_ptr = {}
    for e in exprs:
        manual_by_ptr.setdefault(e['pointer'], []).append(tuple(e['span_in_value']))
    for n in nodes:
        if n['type'] != 'string' or (n['key'] not in REGEX_FIELDS):
            continue
        for name, rx in REGEX:
            for mm in rx.finditer(n['value']):
                if mm.end() == mm.start():
                    continue
                if name == 'number_unit' and not re.search(r'\d', mm.group(0)):
                    continue
                if name == 'number_unit' and n['key'] in ('patient_ko',) and re.fullmatch(r'\d', mm.group(0)) \
                        and n['value'][max(0, mm.start() - 1)] == '[':
                    continue  # 인용 표지 내부 숫자는 citation_marker 가 담당
                s, e = mm.start(), mm.end()
                cov = any(a <= s and e <= b for a, b in manual_by_ptr.get(n['pointer'], []))
                st = 'I' if name == 'mixed_hangul' and n['key'] not in ('patient_ko', 'accuracy_note', 'rubric') else 'P'
                if name == 'mixed_hangul' and st == 'P':
                    continue  # 한국어 필드의 한글은 표현 후보 아님
                vd = REGEX_VERDICTS.get((n['pointer'], s, e, name))
                r = add_expr(n['pointer'], s, e, [name], 'regex', 'K' if vd else st)
                r['covered_by_manual'] = cov
                if vd:
                    r['regex_verdict'] = 'false_positive'
                    r['note'] = vd
    hit = {(e['pointer'], e['span_in_value'][0], e['span_in_value'][1], e['facets'][0]) for e in exprs if e.get('regex_verdict')}
    if hit != set(REGEX_VERDICTS):
        raise SystemExit('regex-review 판정이 현재 후보와 맞지 않음')
    exprs.sort(key=lambda e: (e['file_cp'][0], -e['file_cp'][1], e['origin']))
    for k, e in enumerate(exprs):
        e['id'] = 'E%04d' % (k + 1)
    expr_by_ptr = {}
    for e in exprs:
        expr_by_ptr.setdefault(e['pointer'], []).append(e['id'])
    expressions = {
        'source_sha256': sha,
        'method': {
            'manual': '구획별 직접 읽기 중 manual/S??.json 에 적은 구절. 텍스트를 값 안에서 찾아 구간을 계산(occurrence 로 n번째 출현 지정)',
            'regex': '보조 정규식 후보(REGEX 표). 의미 판정 아님. covered_by_manual = 같은 값의 수동 구절이 구간을 포함하는지',
            'span_in_value': '디코딩 값 코드포인트 [start,end)', 'file_cp': '원문 파일 코드포인트 [start,end)',
            'file_byte': '원문 파일 바이트 [start,end)',
            'overlap': '구절과 내부 수식어의 겹침은 의도된 것. 같은 (pointer, span, facets, origin) 중복은 verify 가 오류로 검사',
            'status': 'P=잠정 관찰 · F=후속 의미 조사 · B=원문 정보 부족 · I=원문 내 불일치 · K=알려진 분석 한계 · A=에이전트 추출/해석 오류',
            'facets': '탐색 관점(확정 분류 아님)',
        },
        'regex_table': [{'name': n, 'pattern': r.pattern} for n, r in REGEX],
        'regex_fields': sorted(REGEX_FIELDS),
        'expressions': exprs,
    }

    # ------------------------------------------------ coverage
    segs = {}
    for n in nodes:
        sg = segment_of(n['pointer'])
        segs.setdefault(sg, {'owned': [], 'leaf': []})
        segs[sg]['owned'].append(n['pointer'])
        if n['is_leaf']:
            segs[sg]['leaf'].append(n['pointer'])
    coverage = {'source_sha256': sha, 'all_leaf_pointers': [n['pointer'] for n in nodes if n['is_leaf']],
                'all_node_pointers': [n['pointer'] for n in nodes],
                'ownership_rule': 'S00 = 루트·상위 메타·/categories 컨테이너. Sxx = /categories/Mxx 와 그 아래 전부. 공동 참조(context_refs)는 소유가 아니다',
                'reading_states': {'unread': '계획만 있음', 'machine_extracted': 'source-map 등 기계 추출만',
                                   'read_direct': '원문을 구획 단위로 직접 읽고 manual 기록 작성'},
                'segments': []}
    for sg in sorted(segs):
        m = manual.get(sg)
        coverage['segments'].append({
            'id': sg, 'title': SEG_TITLE[sg],
            'pointer_range': segs[sg]['owned'][0] + (' 와 하위 전부' if sg != 'S00' else ' (S00 소유 목록 참조)'),
            'owned_pointers': segs[sg]['owned'], 'owned_leaf_pointers': segs[sg]['leaf'],
            'context_refs': ['/source_method', '/accuracy_summary'] + ([] if sg == 'S00' else ['/categories/M%d/name' % int(sg[1:])]),
            'machine_extracted': True,
            'reading_state': m['reading_state'] if m else 'unread',
            'last_read_pointer': m.get('last_read_pointer') if m else None,
            'manual_file': 'manual/%s.json' % sg if m else None,
            'review_file': 'review-part-%s.md' % sg,
        })

    # ------------------------------------------------ review parts
    def cell(s):
        return str(s).replace('|', '\\|').replace('\n', '\\n')

    issues_all = []
    for sg in sorted(segs):
        m = manual.get(sg, {})
        L = ['# %s — %s' % (sg, SEG_TITLE[sg]), '', '[← review.md 목차](./review.md)', '']
        L.append('- 읽기 상태: %s · 마지막 읽은 Pointer `%s`' % (m.get('reading_state', 'unread'), m.get('last_read_pointer')))
        L.append('- 공동 참조 문맥(소유 아님): ' + ', '.join('`%s`' % c for c in coverage['segments'][sorted(segs).index(sg)]['context_refs']))
        L.append('')
        L.append('## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)')
        L.append('')
        L.append('원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.')
        L.append('')
        L.append('| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |')
        L.append('|---|---|---|---|---|---|---|')
        for p in segs[sg]['owned']:
            n = by_ptr[p]
            col = n['key'] if n['key'] is not None else ('[%d]' % n['index'] if n['index'] is not None else '(root)')
            if n['type'] in ('object', 'array'):
                val = '(%s, 자식 %d)' % (n['type'], n['child_count'])
            else:
                val = n['literal']
            mo = ''
            if n['is_leaf'] and n['type'] not in ('object', 'array'):
                mo = 'applied' if p in applied_ptrs else 'excluded'
            L.append('| `%s` | %s | %s | %s | %d–%d | %s | %s |' % (
                p or '(root)', cell(col), n['type'], cell(val), n['file_cp'][0], n['file_cp'][1], mo,
                ', '.join(expr_by_ptr.get(p, []))))
        L.append('')
        L.append('## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)')
        L.append('')
        obs = m.get('observations', [])
        if not obs:
            L.append('(직접 읽기 기록 없음 — 미독)' if not m else '(관찰 없음)')
        for o in obs:
            L.append('- **%s** [%s] `%s` — %s' % (o['id'], o.get('status', 'P'), '`, `'.join(o['pointers']), o['text']))
        L.append('')
        L.append('## 3. 수동 표현 (직접 읽기에서 수집)')
        L.append('')
        me = [e for e in exprs if e['segment'] == sg and e['origin'] == 'manual']
        if me:
            L.append('| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |')
            L.append('|---|---|---|---|---|---|---|')
            for e in me:
                L.append('| %s | `%s` | %d–%d | %s | %s | %s | %s |' % (
                    e['id'], e['pointer'], e['span_in_value'][0], e['span_in_value'][1], cell(e['text']),
                    ', '.join(e['facets']), e['status'], cell(e.get('note', ''))))
        else:
            L.append('(없음)')
        L.append('')
        L.append('## 4. 미결')
        L.append('')
        iss = m.get('issues', [])
        if not iss:
            L.append('(없음)' if m else '(미독)')
        for x in iss:
            issues_all.append(dict(x, segment=sg))
            L.append('- **%s** [%s] `%s` — %s' % (x['id'], x['class'], '`, `'.join(x['pointers']), x['text']))
        L.append('')
        open(os.path.join(OUT, 'review-part-%s.md' % sg), 'w', encoding='utf-8').write('\n'.join(L))

    write_review_index(nodes, by_ptr, coverage, manual, morphology, exprs, sha, raw, text)
    write_issues(issues_all, morphology, sha)
    json.dump(source_map, open(os.path.join(OUT, 'source-map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(morphology, open(os.path.join(OUT, 'morphology.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(expressions, open(os.path.join(OUT, 'expressions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(coverage, open(os.path.join(OUT, 'coverage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({'source_sha256': sha, 'issues': issues_all},
              open(os.path.join(OUT, 'issues-index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({'sha256': sha, 'nodes': len(nodes), 'leaves': source_map['parse']['leaf_count'],
                      'dup_keys': len(sc.dup_keys), 'escaped_strings': len(source_map['parse']['escaped_strings']),
                      'morph_applied': len(applied_ptrs), 'morph_tokens': sum(v['token_count'] for v in morph_values),
                      'morph_excluded': len(excluded), 'expressions': len(exprs),
                      'manual_expressions': sum(1 for e in exprs if e['origin'] == 'manual'),
                      'segments_read': sum(1 for s in coverage['segments'] if s['reading_state'] == 'read_direct'),
                      'segments': len(coverage['segments'])}, ensure_ascii=False))


def pattern_of(ptr):
    p = re.sub(r'^/categories/M\d+', '/categories/{Mxx}', ptr)
    p = re.sub(r'^/accuracy_summary/by_category_average/M\d+$', '/accuracy_summary/by_category_average/{Mxx}', p)
    p = re.sub(r'/\d+(?=/|$)', '/{i}', p)
    return p or '(root)'


def _cell(s):
    return str(s).replace('|', '\\|').replace('\n', '\\n')


def write_review_index(nodes, by_ptr, coverage, manual, morphology, exprs, sha, raw, text):
    pats = {}
    for n in nodes:
        pt = pattern_of(n['pointer'])
        d = pats.setdefault(pt, {'types': {}, 'count': 0, 'first': n, 'empty': [], 'parents': set()})
        d['count'] += 1
        d['types'][n['type']] = d['types'].get(n['type'], 0) + 1
        if n['parent'] is not None:
            d['parents'].add(n['parent'])
        if (n['type'] in ('object', 'array') and n['child_count'] == 0) or (n['type'] == 'string' and n['value'] == ''):
            d['empty'].append(n['pointer'])
    parent_pat_count = {}
    for n in nodes:
        parent_pat_count[pattern_of(n['pointer'])] = parent_pat_count.get(pattern_of(n['pointer']), 0) + 1
    L = ['# literature-evidence.json — 1차 조사 review', '']
    L += ['## 상태', '',
          '- **1차 범위 종료: 예(아래 기준 충족, validation.md 근거)** · **원장 전체 완료 아님** — 의미 조사·정규화·관계 확정은 시작하지 않았다',
          '- 전수 읽기: 구획 18/18 직접 읽음(coverage.json · manual/S00~S17.json). 진술 119개 × statement·citations·점수·patient_ko/en/zh/ja·added_at 전부',
          '- 구조·값 수집: 노드 %d · 말단(빈 컨테이너 포함) %d · 중복 키 %d · 이스케이프 문자열 %d (source-map.json)' % (
              len(nodes), sum(1 for n in nodes if n['is_leaf']), 0, sum(1 for n in nodes if n['type'] == 'string' and not n['literal_equals_decoded'])),
          '- 형태소: Kiwi %s(cong) 적용 %d값 %d토큰 · 제외 %d(사유별 morphology.json excluded) · 알려진 분석 오류 %d규칙 %d출현 표시(교정 아님)' % (
              morphology['analyzer']['version'], len(morphology['values']), sum(v['token_count'] for v in morphology['values']),
              len(morphology['excluded']), len(morphology['segmentation_review']['rules']), len(morphology['segmentation_review']['occurrences'])),
          '- 표현: 수동 %d · 정규식 보조 %d (expressions.json)' % (sum(1 for e in exprs if e['origin'] == 'manual'), sum(1 for e in exprs if e['origin'] == 'regex')),
          '- 기계 검증·읽기 검토·미결: [validation.md](./validation.md) · [issues.md](./issues.md) · 진행 기록 [progress.md](./progress.md)',
          '- 원본: `%s` sha256 `%s` · %d bytes · %d codepoints · 줄바꿈 0(한 줄 JSON)' % (SRC_REL, sha, len(raw), len(text)), '']
    L += ['## 읽는 법', '',
          '- 각 review-part 의 §1 표는 원본 컬럼명(키 그대로)·자료형·원문 값(JSON 리터럴)·파일 cp 구간만 담는다. 잠정 관찰은 §2, 수동 표현은 §3, 미결은 §4 로 분리했다.',
          '- 미결 문자: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · 보조 K=알려진 분석 한계 · P=잠정 · F=후속 · I=원문 불일치.',
          '- 관찰·표현의 facets 는 탐색 관점이며 확정 분류가 아니다. 형태소 기본형은 도메인 표준명이 아니다.', '']
    L += ['## 컬럼 구성 표 (경로 패턴 · 자료형 · 중첩 · 원문 예시와 위치)', '',
          '`{Mxx}`=카테고리 키, `{i}`=배열 인덱스. 출현 수는 노드 수. 선택 필드 = 같은 부모 패턴 중 일부에만 있는 키.', '',
          '| 경로 패턴 | 자료형(출현) | 출현 수 | 원문 예시(리터럴) | 예시 Pointer | 빈 값 출현 |', '|---|---|---|---|---|---|']
    for pt, d in pats.items():
        ex = d['first']
        exv = ('(%s, 자식 %d)' % (ex['type'], ex['child_count'])) if ex['type'] in ('object', 'array') else ex['literal']
        if len(exv) > 160:
            exv = exv[:157] + '…'
        types = ', '.join('%s×%d' % kv for kv in d['types'].items())
        emp = ('%d (예: `%s`)' % (len(d['empty']), d['empty'][0])) if d['empty'] else '0'
        L.append('| `%s` | %s | %d | %s | `%s` | %s |' % (pt, types, d['count'], _cell(exv), ex['pointer'] or '(root)', emp))
    # optional fields
    L += ['', '### 선택 필드·형태 변형', '']
    stmt_parents = [n for n in nodes if re.fullmatch(r'/categories/M\d+/(moa|adverse_effects|effects)/\d+', n['pointer'])]
    cit_parents = [n for n in nodes if re.fullmatch(r'.*/citations/\d+', n['pointer'])]
    for label, plist in (('진술 객체 `/categories/{Mxx}/{moa|adverse_effects|effects}/{i}`', stmt_parents), ('인용 객체 `…/citations/{i}`', cit_parents)):
        shapes = {}
        for n in plist:
            ks = tuple(c['key'] for c in nodes if c['parent'] == n['pointer'])
            shapes.setdefault(ks, []).append(n['pointer'])
        L.append('- %s: 키 구성 %d종' % (label, len(shapes)))
        for ks, ps in shapes.items():
            L.append('  - %d개 — `%s` (예: `%s`)' % (len(ps), ', '.join(ks), ps[0]))
    L += ['- 빈 배열 20개: M3·M15·M17 effects, M9 adverse_effects, M17 moa, M6·M10·M11·M13·M14 의 세 배열 전부. 빈 문자열·null·불리언 0.',
          '- 숫자: `accuracy_score` int, `year` int, `/accuracy_summary` 의 평균값 float(리터럴 `95.0` 등 소수점 보존), `n_scored` int.', '']
    L += ['## 구획 목차', '', '| 구획 | 범위 | 소유 노드 | 소유 말단 | 진술 수 | 읽기 상태 | 문서 |', '|---|---|---|---|---|---|---|']
    for sg in coverage['segments']:
        nst = sum(1 for p in sg['owned_pointers'] if re.fullmatch(r'/categories/M\d+/(moa|adverse_effects|effects)/\d+', p))
        L.append('| %s | %s | %d | %d | %d | %s | [review-part-%s.md](./review-part-%s.md) |' % (
            sg['id'], sg['title'], len(sg['owned_pointers']), len(sg['owned_leaf_pointers']), nst, sg['reading_state'], sg['id'], sg['id']))
    L += ['', '## 산출물', '',
          '| 파일 | 내용 |', '|---|---|',
          '| source-map.json | 모든 노드: Pointer·부모·키 리터럴/구간·순서·자료형·디코딩 값·JSON 리터럴·파일 cp/byte 구간·이스케이프 대응표·구획 |',
          '| coverage.json | 구획별 소유 노드/말단 Pointer·공동 참조·읽기 상태·manual/review 파일 |',
          '| morphology.json | 분석기 설정·적용 값별 토큰(표면형·form·tag·lemma·구간·파일 cp)·제외 목록·필드명 처리·알려진 분석 오류 출현 |',
          '| expressions.json | 수동·정규식 표현(구간·파일 cp/byte·facets·상태) |',
          '| issues.md · issues-index.json | 미결 묶음·구획별 미결 원본 |',
          '| segmentation-review.json | 형태소 출력 직접 대조로 찾은 오류 서명(교정 아님) |',
          '| manual/S??.json | 구획별 직접 읽기 기록(관찰·표현·미결) |',
          '| build.py · verify.py · read_segment.py | 재현 생성 · 독립 검증 · 읽기 출력 도우미 |', '']
    open(os.path.join(OUT, 'review.md'), 'w', encoding='utf-8').write('\n'.join(L))


def write_issues(issues_all, morphology, sha):
    by = {}
    for x in issues_all:
        by.setdefault(x['class'], []).append(x)
    L = ['# issues — literature-evidence.json', '',
         '원본 sha256 `%s`. 구획별 원본 미결은 각 review-part §4 와 issues-index.json. 아래는 같은 원인 묶음과 처리 상태.' % sha, '',
         '## 상태 요약', '',
         '| 문자 | 뜻 | 건수(구획 기록) | 처리 상태 |', '|---|---|---|---|',
         '| A | 에이전트 추출/해석 오류 | 0 열림 | 작업 중 발견·수정 기록은 validation.md §5. 현재 열린 A 없음 |',
         '| B | 원문 정보 부족 | %d | 열림 — 부족한 정보와 제한되는 활용을 각 항목에 적음. 사용자에게 사실을 묻지 않음 |' % len(by.get('B', [])),
         '| C | 현재 사용자 결정 필요 | 0 | 아래 「사용자 결정 0의 근거」 |',
         '| I | 원문 내 불일치 | %d | 열림 — 원문 그대로 보존, 원본 변경은 후속 확인 후보(선택 대기 아님) |' % len(by.get('I', [])),
         '| F | 후속 의미 조사 | %d | 열림 — 2단계(공통 의미·ERD) 과제 |' % len(by.get('F', [])),
         '| K | 알려진 분석 한계 | %d + 형태소 규칙 %d(출현 %d) | 기록 완료, 교정 안 함 |' % (
             len(by.get('K', [])), len(morphology['segmentation_review']['rules']), len(morphology['segmentation_review']['occurrences'])), '']
    L += ['## 같은 원인 묶음', '',
          '### I-CITE — patient_ko 인용 표지와 citations 불일치',
          '- 모든 진술의 citations 배열은 정확히 1개다. 그런데 patient_ko 끝에 `[1][2][4][5]`·`[3][9]` 같은 표지가 붙은 값이 있고, 그 번호가 가리킬 문헌 목록이 원장 안에 없다. 출현 위치는 expressions.json facet `citation_marker`(정규식 전수)와 각 구획 I 항목.',
          '- 영향: 표지 숫자(SN)를 수량·근거 개수로 쓰면 오류. 이후 단계에서 표지를 근거 연결로 쓰지 못한다.',
          '- 원본 변경 제안(표지 제거 등)은 원본 보존 지시 아래 후속 확인 후보이며 선택 대기로 올리지 않는다.', '',
          '### I-SCRIPT — 언어 필드의 다른 문자 혼입',
          '- patient_ja 5곳 한글(`伝달`·`ボツ리ヌ`·`狙い通리의`·`HIFU는`·`毛穴의`), patient_ja 1곳 중국어 간체(`视黄醇类`), patient_en 1곳 한글(`natural성분`), patient_zh 1곳 `的同事`(문맥상 다른 글자 후보). expressions.json facet `mixed_script`(정규식)·수동 표현.',
          '', '### I-LANG — 같은 진술의 언어별 수식·조건·극성 차이',
          '- statement(영어 원 주장)와 patient_ko/en/zh/ja, accuracy_note 사이에 빈도(`드물게`·`rarely`), 가능성(`may`·`수 있습니다`), 경과(`Temporary`·`일시적`), 조건(부위·피부형·pH·사후관리), 비교 대상, 고유명(성분·장비·질환)이 추가·탈락·변형된다. 가장 큰 사례: M16 effects/0 의 불승인·근거 부족 진술이 patient_en/zh/ja 에서 긍정 효과 문장으로 반전, M5 adverse_effects/1 감염 위험이 en/zh/ja 에서 탈락하고 ko 에 「매우 안전」 추가.',
          '- 영향: 언어별 문장을 같은 사실의 번역으로 취급해 수식·조건을 합치면 뜻이 바뀐다. 어느 필드가 기준인지 원문이 밝히지 않는다(source_method 는 statement 를 검증 대상으로 언급).',
          '', '### K-ENG / K-ZHJA — 형태소 분석 미적용 언어',
          '- statement·patient_en·name·source_method·scored_by(영어), patient_zh, patient_ja 는 Kiwi(한국어) 적용 범위 밖이라 제외했다. 이 값들의 수식·조건·부정은 직접 읽기·수동 표현·영어 보조 정규식으로만 수집했다. 영어 형태소(품사·기본형)는 없다.', '',
          '### K-MORPH — 알려진 형태소 오분절(교정 안 함)', '']
    for r in morphology['segmentation_review']['rules']:
        occ = [o for o in morphology['segmentation_review']['occurrences'] if o['rule'] == r['id']]
        L.append('- **%s** `%s` %s — %d출현 (예: `%s` [%d,%d)) — %s' % (r['id'], r['surface'], r['kind'], len(occ), occ[0]['pointer'], occ[0]['span_in_value'][0], occ[0]['span_in_value'][1], r['impact']))
    L += ['', '## 사용자 결정 0의 근거', '',
          '- 남은 항목은 B(원문 부족)·I(원문 불일치)·F(후속 의미 조사)·K(분석 한계)로, 1차 수집 범위 안에서 사용자가 지금 골라야 바뀌는 결과가 없다. 형태소 도구·제외 범위는 에이전트 판단으로 정해 기록했다.',
          '- I 항목의 원본 수정 여부, 언어 필드 기준 결정, 근접 중복 진술 병합 여부는 2단계 설계 때 영향 검토 후 사용자 확인 대상이 될 수 있다(지금은 선택 대기로 올리지 않음).', '']
    for cl in ('B', 'I', 'F', 'K'):
        L += ['## 구획별 %s 목록' % cl, '']
        for x in by.get(cl, []):
            L.append('- **%s** (%s) `%s` — %s' % (x['id'], x['segment'], '`, `'.join(x['pointers'][:4]) + (' …' if len(x['pointers']) > 4 else ''), x['text']))
        L.append('')
    open(os.path.join(OUT, 'issues.md'), 'w', encoding='utf-8').write('\n'.join(L))

if __name__ == '__main__':
    main()
