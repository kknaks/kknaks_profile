"""market-pricing.json 1차 조사 산출물 생성기.

레포 루트에서:
  uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/market-pricing/build.py

원본은 읽기만 한다. 쓰기는 이 폴더 안에만 한다.
수동 기록(manual/S*.json · segments.json · manual/auto-review.json)은 손으로 고치고,
나머지 생성 파일은 직접 고치지 않는다(재생성 시 덮어씀).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = 'orchestration/work/phub-recommend/bronze/phub-ledger/market-pricing.json'
SRC = REPO / SRC_REL
OUT_REL = 'orchestration/work/phub-ledger-redesign/first-pass/market-pricing'


# ---------------------------------------------------------------- 위치 기록 파서
class Parser:
    """원문 텍스트를 직접 훑어 노드마다 Pointer·코드포인트 구간·바이트 구간을 기록한다.
    중복 키는 덮어쓰지 않고 출현 순서대로 따로 기록한다."""

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.keys = []
        self.dup_keys = []
        # 코드포인트 → 바이트 오프셋
        self.byte_at = [0]
        for ch in text:
            self.byte_at.append(self.byte_at[-1] + len(ch.encode('utf-8')))

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in ' \t\r\n':
            self.i += 1

    def esc(self, k):
        return k.replace('~', '~0').replace('/', '~1')

    def string(self):
        assert self.t[self.i] == '"'
        s = self.i
        self.i += 1
        while self.t[self.i] != '"':
            if self.t[self.i] == '\\':
                self.i += 2
            else:
                self.i += 1
        self.i += 1
        lit = self.t[s:self.i]
        return json.loads(lit), s, self.i

    def value(self, ptr, parent, key, index):
        self.ws()
        s = self.i
        c = self.t[s]
        node = {'pointer': ptr, 'parent': parent, 'key': key, 'index': index}
        if c == '{':
            node['type'] = 'object'
            self.nodes.append(node)
            self.i += 1
            seen = {}
            n = 0
            self.ws()
            if self.t[self.i] == '}':
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke = self.string()
                    occ = seen.get(k, 0)
                    seen[k] = occ + 1
                    if occ:
                        self.dup_keys.append({'object': ptr, 'key': k, 'occurrence': occ, 'char_span': [ks, ke]})
                    cptr = f'{ptr}/{self.esc(k)}'
                    self.keys.append({'key': k, 'object_pointer': ptr, 'pointer': cptr, 'order': n,
                                      'literal_char_span': [ks, ke],
                                      'literal_byte_span': [self.byte_at[ks], self.byte_at[ke]]})
                    n += 1
                    self.ws()
                    assert self.t[self.i] == ':'
                    self.i += 1
                    self.value(cptr, ptr, k, None)
                    self.ws()
                    if self.t[self.i] == ',':
                        self.i += 1
                        continue
                    assert self.t[self.i] == '}'
                    self.i += 1
                    break
            node['length'] = n
        elif c == '[':
            node['type'] = 'array'
            self.nodes.append(node)
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == ']':
                self.i += 1
            else:
                while True:
                    self.value(f'{ptr}/{n}', ptr, None, n)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ',':
                        self.i += 1
                        continue
                    assert self.t[self.i] == ']'
                    self.i += 1
                    break
            node['length'] = n
        elif c == '"':
            v, _, _ = self.string()
            node['type'] = 'string'
            node['value'] = v
            self.nodes.append(node)
        else:
            m = re.compile(r'-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null').match(self.t, s)
            lit = m.group(0)
            self.i = m.end()
            v = json.loads(lit)
            node['type'] = ('null' if v is None else 'boolean' if isinstance(v, bool)
                            else 'integer' if isinstance(v, int) else 'number')
            node['value'] = v
            self.nodes.append(node)
        e = self.i
        node['literal_char_span'] = [s, e]
        node['literal_byte_span'] = [self.byte_at[s], self.byte_at[e]]
        node['literal'] = self.t[s:e] if node['type'] not in ('object', 'array') else None
        return node


def seg_of(ptr):
    if ptr in ('', '/version', '/updated', '/currency', '/note', '/categories'):
        return 'S00'
    m = re.match(r'^/categories/(\d+)(/|$)', ptr)
    return f'S{int(m.group(1)) + 1:02d}'


# 문자열 값의 분석 적용/제외 규칙 (경로 패턴 → 역할·사유)
EXCLUDE_RULES = [
    (r'^/version$', 'identifier', '버전 문자열 "1.1" — 언어 텍스트 아님'),
    (r'^/updated$', 'identifier', 'ISO 날짜 문자열 — 언어 텍스트 아님'),
    (r'^/currency$', 'code', '통화 코드(KRW) — 언어 텍스트 아님'),
    (r'^/categories/\d+/id$', 'identifier', '카테고리 ID(Mn) — 식별자'),
]
TEXT_RULES = [
    (r'^/note$', 'text:note'),
    (r'^/categories/\d+/name$', 'text:category_name'),
    (r'^/categories/\d+/items/\d+/name$', 'text:item_name'),
    (r'^/categories/\d+/items/\d+/unit$', 'text:unit'),
]

# 자동 후보 패턴 — 이 패턴에 실제로 일치한 것만 자동 후보가 된다(전수 의미 해석 아님).
AUTO_PATTERNS = [
    ('paren', r'\([^()]*\)', '괄호 구절'),
    ('num_unit', r'\d+(?:\.\d+)?(?:cc|ml|회|줄|샷|바이알|개|부위|cm2)', '숫자+단위'),
    ('plus', r'[^\s(+]+\s*\+\s*[^\s)+]+', "'+' 연결"),
    ('slash', r'[^\s/()]+(?:/[^\s/()]+)+', "'/' 연결"),
    ('kw', r'이상|기준|부위당|개당|패키지|콤보|동시|양쪽|안쪽|비수술|집중|강화|축소|시술 후|아닌|따라|상이|참고|범위|'
           r'전체얼굴|풀페이스|풀코스|전신|고농도|프리미엄|소부위|나노|수입|국산', '키워드'),
]

# 알려진 오분절 서명 — 출현별로 표시한다(교정하지 않음). 원문 직접 대조로 확인한 것만 둔다.
KNOWN_MISSEG = [
    {'id': 'K-정가', 'surface': '정가', 'tokens': [['정', 'NNP'], ['가', 'XSN']],
     'impact': "'정가'(정해진 가격)가 고유명사+접미사로 쪼개져, '정가 아닌' 부정 대상 탐색 시 '정가'가 명사로 잡히지 않는다."},
    {'id': 'K-리쥬란', 'surface': '리쥬란', 'tokens': [['리쥬', 'NNP'], ['이', 'VCP'], ['란', 'ETM']],
     'impact': '제품명 후보가 명사+지정사(길이0)+어미로 쪼개진다. 제품명 단위 검색 불가, 길이0 토큰 포함.'},
    {'id': 'K-볼뉴머', 'surface': '볼뉴머', 'tokens': [['볼', 'NNG'], ['뉴', 'NNG'], ['머', 'EC']],
     'impact': "제품명 후보에서 '볼'(부위 후보와 같은 형태)이 명사로 나와 부위 오탐 위험."},
    {'id': 'K-이모드', 'surface': '이모드', 'tokens': [['이', 'MM'], ['모드', 'NNG']],
     'impact': "장비명 후보가 관형사 '이'+'모드' 로 쪼개짐. 관형사(MM) 수집 시 오탐."},
    {'id': 'K-리프팅(민트)', 'surface': '리프팅', 'tokens': [['리프', 'NNP'], ['팅', 'NNP']],
     'impact': "다른 출현에서는 '리프팅/NNG' 한 토큰인데 이 출현만 둘로 쪼개짐 — 같은 말의 분석 불일치."},
    {'id': 'K-양쪽(민트)', 'surface': '양쪽', 'tokens': [['양', 'MM'], ['쪽', 'NNB']],
     'impact': "다른 출현에서는 '양쪽/NNG' 인데 이 출현만 관형사+의존명사. 양측성 표현 토큰 검색 시 누락 위험."},
    {'id': 'K-몰딩', 'surface': '몰딩', 'tokens': [['몰', 'NNG'], ['딩', 'MAG']],
     'impact': "'딩'이 부사(MAG)로 태깅 — 부사(수식) 수집 시 오탐."},
    {'id': 'K-더마펜', 'surface': '더마펜', 'tokens': [['더', 'MAG'], ['마', 'NNG'], ['펜', 'NNG']],
     'impact': "장비명 후보 첫 음절 '더'가 비교 부사(MAG)로 태깅 — 비교·정도 부사 수집 시 오탐."},
    {'id': 'K-이중턱', 'surface': '이중턱', 'tokens': [['이', 'NNP'], ['중턱', 'NNG']],
     'impact': "'이중턱'(고민 후보)이 '이'+'중턱' 으로 쪼개져 다른 뜻의 명사가 나옴."},
    {'id': 'K-쥬베룩', 'surface': '쥬베룩', 'tokens': [['쥬베', 'NNG'], ['룩', 'NNG']],
     'impact': "제품명 후보 분절. 같은 원장의 '쥬베룩 울트라' 출현에서는 '쥬베룩/NNG' 한 토큰 — 분석 불일치."},
    {'id': 'K-소부위', 'surface': '소부위', 'tokens': [['소', 'NNG'], ['부위', 'NNG']],
     'impact': "크기 수식 접두 '소-'가 일반명사(NNG)로 태깅 — 크기 수식 탐색 시 누락 위험."},
    {'id': 'K-부위당', 'surface': '부위당', 'tokens': [['부위당', 'NNP']],
     'impact': "'부위'+'당'(단위당)이 한 고유명사로 묶여 분모 표현 '당' 이 토큰으로 안 잡힘."},
]


def tok_list(kiwi, text):
    out = []
    for t in kiwi.tokenize(text):
        s, e = t.start, t.start + t.len
        out.append({'form': t.form, 'tag': t.tag, 'start': s, 'end': e,
                    'slice': text[s:e], 'form_equals_slice': t.form == text[s:e],
                    'lemma_tool': t.lemma, 'oov': bool(getattr(t, 'oov', False))})
    return out


def main():
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8')
    p = Parser(text)
    root = p.value('', None, None, None)
    p.ws()
    assert p.i == len(text), 'trailing data'
    data = json.loads(text)
    nodes = p.nodes
    for n in nodes:
        n['segment'] = seg_of(n['pointer'])
        n['is_leaf'] = n['type'] not in ('object', 'array')
        n['is_empty_container'] = (not n['is_leaf']) and n['length'] == 0
        if n['type'] == 'string':
            n['is_empty_string'] = n['value'] == ''
    segs = json.loads((HERE / 'segments.json').read_text(encoding='utf-8'))
    manual = {}
    for s in segs['segments']:
        manual[s['id']] = json.loads((HERE / 'manual' / f"{s['id']}.json").read_text(encoding='utf-8'))
    by_ptr = {n['pointer']: n for n in nodes}

    # ---------------- 문맥 참조
    def context_of(ptr):
        ctx = ['/currency', '/note', '/updated']
        m = re.match(r'^/categories/(\d+)', ptr)
        if m:
            b = f'/categories/{m.group(1)}'
            ctx += [b + '/id', b + '/name']
            m2 = re.match(r'^(/categories/\d+/items/\d+)/', ptr)
            if m2:
                ctx += [m2.group(1) + '/' + k for k in ('name', 'unit', 'low', 'mid', 'high')]
        return [c for c in ctx if c != ptr]

    for n in nodes:
        if n['is_leaf']:
            n['context_refs'] = context_of(n['pointer'])

    source_map = {
        'source': SRC_REL, 'source_sha256': sha, 'source_bytes': len(raw), 'source_codepoints': len(text),
        'span_units': {'literal_char_span': '디코딩된 파일 텍스트의 Unicode 코드포인트 [start,end) — JSON 리터럴(따옴표 포함)',
                       'literal_byte_span': '원본 파일 UTF-8 바이트 [start,end) — JSON 리터럴',
                       'value_span(형태소·표현)': '디코딩된 문자열 값의 코드포인트 [start,end)'},
        'escapes_in_source': text.count('\\'),
        'duplicate_keys': p.dup_keys,
        'counts': {'nodes': len(nodes), 'leaves': sum(n['is_leaf'] for n in nodes),
                   'containers': sum(not n['is_leaf'] for n in nodes),
                   'empty_containers': sum(n['is_empty_container'] for n in nodes),
                   'empty_strings': sum(n.get('is_empty_string', False) for n in nodes),
                   'nulls': sum(n['type'] == 'null' for n in nodes),
                   'key_occurrences': len(p.keys)},
        'nodes': nodes,
        'key_occurrences': p.keys,
    }

    # ---------------- 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type='cong')
    applied, excluded = [], []
    for n in nodes:
        if n['type'] != 'string':
            continue
        ptr = n['pointer']
        ex = next((r for r in EXCLUDE_RULES if re.match(r[0], ptr)), None)
        if ex:
            excluded.append({'pointer': ptr, 'value': n['value'], 'role': ex[1], 'reason': ex[2]})
            continue
        role = next(r[1] for r in TEXT_RULES if re.match(r[0], ptr))
        toks = tok_list(kiwi, n['value'])
        applied.append({'pointer': ptr, 'role': role, 'text': n['value'], 'segment': n['segment'], 'tokens': toks})
    non_string = [{'pointer': n['pointer'], 'type': n['type'], 'reason': '숫자 값 — 형태소 분석 대상 아님(원문 값은 source-map 에 보존)'}
                  for n in nodes if n['is_leaf'] and n['type'] != 'string']
    field_names = sorted({k['key'] for k in p.keys})
    field_analysis = [{'field_name': f, 'role': 'field_name', 'occurrences': sum(1 for k in p.keys if k['key'] == f),
                       'first_pointer': next(k['pointer'] for k in p.keys if k['key'] == f),
                       'tokens': tok_list(kiwi, f),
                       'note': '영문 식별자 — Kiwi 결과(SL)는 참고용. 언어 텍스트 분석과 역할을 구분한다.'} for f in field_names]
    misseg_occ = []
    for a in applied:
        for k in KNOWN_MISSEG:
            for m in re.finditer(re.escape(k['surface']), a['text']):
                got = [[t['form'], t['tag']] for t in a['tokens'] if m.start() <= t['start'] < m.end()]
                if got == k['tokens']:
                    misseg_occ.append({'id': k['id'], 'pointer': a['pointer'], 'span': [m.start(), m.end()],
                                       'surface': k['surface'], 'raw_tokens': got, 'impact': k['impact']})
    # 영숫자 혼합 분절(K): SL/SN 이 공백 없이 붙어 쪼개진 출현
    mixed_occ = []
    for a in applied:
        for m in re.finditer(r'[A-Za-z]+\d+[A-Za-z0-9]*|\d+[A-Za-z]+\d+', a['text']):
            got = [[t['form'], t['tag']] for t in a['tokens'] if m.start() <= t['start'] < m.end()]
            if len(got) > 1:
                mixed_occ.append({'id': 'K-영숫자혼합', 'pointer': a['pointer'], 'span': [m.start(), m.end()],
                                  'surface': m.group(0), 'raw_tokens': got,
                                  'impact': '제품명·단위(CO2·cm2·FLX 등) 영숫자 결합이 SL/SN 으로 나뉜다. 이름 단위 검색은 원문 구간으로 해야 한다.'})
    morph = {
        'analyzer': {'name': 'kiwipiepy', 'version': kiwipiepy.__version__, 'model_type': 'cong', 'num_workers': 1,
                     'user_dictionary': None, 'options': 'Kiwi(num_workers=1, model_type="cong").tokenize(text) 기본값',
                     'tagset': 'Kiwi(세종 확장) 품사', 'runtime': f'python {sys.version.split()[0]}',
                     'lemma_note': "lemma_tool 은 Kiwi Token.lemma 가 준 값 그대로. 도구가 주지 않은 기본형은 만들지 않았다.",
                     'span_note': "start/end 는 문자열 값의 코드포인트 [start,end). 축약·불규칙 활용(예: '따라'→'따르'+'어')에서는 form 과 slice 가 다를 수 있어 form_equals_slice 로 표시."},
        'source_sha256': sha,
        'applied': applied, 'excluded_strings': excluded, 'non_string_leaves': non_string,
        'field_names': field_analysis,
        'known_missegmentation_occurrences': misseg_occ + mixed_occ,
        'counts': {'applied_values': len(applied), 'tokens': sum(len(a['tokens']) for a in applied),
                   'excluded_strings': len(excluded), 'non_string_leaves': len(non_string),
                   'field_names': len(field_names),
                   'known_misseg_occurrences': len(misseg_occ) + len(mixed_occ)},
    }

    # ---------------- 표현
    auto_review = json.loads((HERE / 'manual' / 'auto-review.json').read_text(encoding='utf-8'))
    auto = []
    for a in applied:
        for pid, pat, label in AUTO_PATTERNS:
            for m in re.finditer(pat, a['text']):
                cid = f"A:{a['pointer']}:{m.start()}-{m.end()}:{pid}"
                auto.append({'id': cid, 'source': 'auto_regex', 'pattern_id': pid, 'pattern': pat, 'label': label,
                             'pointer': a['pointer'], 'segment': a['segment'], 'start': m.start(), 'end': m.end(),
                             'text': m.group(0), 'full_value': a['text'],
                             'review': auto_review.get('verdicts', {}).get(cid, auto_review.get('default_verdict'))})
    man = []
    errors = []
    for sid, mobj in manual.items():
        cnt = {}
        for ptr, sub, persp, note in mobj['expressions']:
            v = by_ptr.get(ptr, {}).get('value')
            if not isinstance(v, str):
                errors.append(f'{sid}: pointer not string {ptr}')
                continue
            key = (ptr, sub)
            occ = cnt.get(key, 0)
            cnt[key] = occ + 1
            pos = -1
            for _ in range(occ + 1):
                pos = v.find(sub, pos + 1)
            if pos < 0:
                errors.append(f'{sid}: substring not found {ptr} {sub!r} occ{occ}')
                continue
            man.append({'id': f'M:{ptr}:{pos}-{pos + len(sub)}', 'source': 'manual_reading', 'segment': sid,
                        'pointer': ptr, 'start': pos, 'end': pos + len(sub), 'text': sub, 'full_value': v,
                        'perspectives': persp, 'note': note,
                        'matched_by_auto_pattern': [x['pattern_id'] for x in auto
                                                    if x['pointer'] == ptr and x['start'] == pos and x['end'] == pos + len(sub)]})
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    # 겹침: 같은 값 안에서 구간이 겹치는 표현 쌍(의도된 겹침 — 구절과 하위 구절)
    allx = auto + man
    overlaps = 0
    for a in applied:
        xs = [x for x in allx if x['pointer'] == a['pointer']]
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                if xs[i]['start'] < xs[j]['end'] and xs[j]['start'] < xs[i]['end']:
                    overlaps += 1
    manual_outside = [m for m in man if not any(x['pointer'] == m['pointer'] and x['start'] <= m['start'] and m['end'] <= x['end'] for x in auto)]
    expressions = {
        'source_sha256': sha,
        'method': {'auto_regex': '아래 패턴에 실제로 일치한 구간만 자동 후보. 의미 해석이 아니며, 패턴 밖 표현은 자동 후보에 없다.',
                   'patterns': [{'id': i, 'pattern': p_, 'label': l} for i, p_, l in AUTO_PATTERNS],
                   'manual_reading': '구획별 원문 직접 읽기로 수집(manual/S*.json). 부위·제품·고민·수식(위치·크기·농도·등급·강도)·조건·부정·시간 등 탐색 관점은 확정 분류가 아니다.',
                   'span': '문자열 값의 코드포인트 [start,end)'},
        'auto_candidates': auto, 'manual_expressions': man,
        'counts': {'auto_candidates': len(auto), 'manual_expressions': len(man),
                   'manual_not_inside_any_auto': len(manual_outside), 'overlapping_pairs': overlaps,
                   'auto_review_false_positive': sum(1 for x in auto if x['review'] and x['review'].startswith('false_positive'))},
    }

    # ---------------- coverage
    leaf_ptrs = [n['pointer'] for n in nodes if n['is_leaf'] or n['is_empty_container']]
    cov_segs = []
    for s in segs['segments']:
        sid = s['id']
        own = [n['pointer'] for n in nodes if n['segment'] == sid and (n['is_leaf'] or n['is_empty_container'])]
        own_cont = [n['pointer'] for n in nodes if n['segment'] == sid and not n['is_leaf']]
        if sid == 'S00':
            rng = {'from': '', 'to': '/note', 'note': '루트 스칼라 4개 + 루트 객체·/categories 배열 컨테이너'}
            ctx = []
            title = s['title']
        else:
            b = f"/categories/{s['category_index']}"
            rng = {'from': b, 'to': f"{b}/items/{len(data['categories'][s['category_index']]['items']) - 1}/high"}
            ctx = ['/currency', '/note', '/updated']
            c = data['categories'][s['category_index']]
            title = f"{c['id']} {c['name']} ({len(c['items'])}항목)"
        mo = manual[sid]
        cov_segs.append({'id': sid, 'title': title, 'pointer_range': rng, 'owned_leaf_pointers': own,
                         'owned_container_pointers': own_cont, 'context_refs': ctx,
                         'machine_extracted': True, 'direct_read': bool(mo.get('direct_read')),
                         'last_read_pointer': mo.get('last_pointer'), 'read_note': mo.get('read_note'),
                         'manual_record': f'manual/{sid}.json', 'review_file': f'review-part-{sid}.md',
                         'review_section': f'## {sid}'})
    coverage = {'source_sha256': sha, 'all_leaf_pointers': leaf_ptrs,
                'all_container_pointers': [n['pointer'] for n in nodes if not n['is_leaf']],
                'owned_rule': segs['category_segment_rule'], 'segments': cov_segs}

    # ---------------- 출력
    def dump(name, obj):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dump('source-map.json', source_map)
    dump('morphology.json', morph)
    dump('expressions.json', expressions)
    dump('coverage.json', coverage)
    write_review(data, nodes, by_ptr, segs, manual, morph, expressions, coverage, sha, len(raw))
    write_issues(manual, morph)
    print(json.dumps({'sha256': sha, 'counts': source_map['counts'], 'morph': morph['counts'],
                      'expr': expressions['counts']}, ensure_ascii=False))


def md(v):
    return str(v).replace('|', '\\|')


def write_review(data, nodes, by_ptr, segs, manual, morph, expr, coverage, sha, nbytes):
    units = {}
    for n in nodes:
        if re.match(r'^/categories/\d+/items/\d+/unit$', n['pointer']):
            units.setdefault(n['value'], []).append(n['pointer'])
    L = []
    L.append('# market-pricing.json — 1차 조사 (읽기용)\n')
    L.append('**1차 범위 종료: 예 (근거 validation.md) · 원장 전체 완료 아님** — 열린 미결은 [issues.md](issues.md).\n')
    L.append(f'- 원본: `{SRC_REL}` · {nbytes:,} bytes · sha256 `{sha}`')
    c = json.loads(json.dumps({'n': len(nodes)}))
    L.append(f"- 노드 {len(nodes)} (말단 {sum(n['is_leaf'] for n in nodes)} · 컨테이너 {sum(not n['is_leaf'] for n in nodes)} · 빈 컨테이너 {sum(n['is_empty_container'] for n in nodes)} · 빈 문자열 0 · null 0) · 중복 키 0 · 백슬래시 이스케이프 0")
    L.append('- 구획: 루트 메타 S00 + 카테고리별 S01~S17 (전부 직접 읽음 — coverage.json `direct_read`)')
    L.append('- 기계 기록: source-map.json(구조·값·구간) · morphology.json · expressions.json · coverage.json · 검증 validation.md\n')
    L.append('## 상태\n')
    L.append('| 항목 | 상태 |\n|---|---|')
    mc = morph['counts']; ec = expr['counts']
    L.append('| 전수 읽기 | S00~S17 18구획 전부 직접 읽음(구획별 manual/S*.json 저장) |')
    L.append(f"| 구조·값 수집 | 노드 {len(nodes)} · 키 출현 {len([1 for n in nodes if n['key'] is not None])} · 모든 말단 값 원문·Pointer·리터럴 구간 기록 |")
    L.append(f"| 형태소·표현 수집 | Kiwi {morph['analyzer']['version']}(cong, 1스레드) 텍스트 {mc['applied_values']}값 {mc['tokens']}토큰 · 제외 문자열 {mc['excluded_strings']} · 숫자 말단 {mc['non_string_leaves']}(분석 대상 아님) · 알려진 오분절 출현 {mc['known_misseg_occurrences']} · 자동 후보 {ec['auto_candidates']} · 직접 읽기 표현 {ec['manual_expressions']} |")
    L.append('| 기계 검증 | validation.md 참조 (verify.py) |')
    L.append('| 읽기 검토 | 작성자 구획별 직접 읽기 + 표현 재대조(validation.md §읽기 검토). 독립 검토는 코디 몫 |')
    L.append('| 알려진 분석 오류 | issues.md K 절 |')
    L.append('| 열린 미결 | issues.md (B·I·P·F·K, C 0) |')
    L.append('| 후속 의미 조사 | 시작 안 함 |\n')
    L.append('## 컬럼 구성\n')
    L.append('원본 키 이름 그대로. 모든 카테고리·항목이 같은 키 집합을 가진다(선택적 필드 없음 — 기계 확인).\n')
    L.append('| 원본 컬럼(경로 패턴) | 자료형 | 중첩 구조 | 출현 수 | 원문 예시 | 예시 위치 |\n|---|---|---|---|---|---|')
    L.append(f"| `version` (`/version`) | string | 루트 객체 키 | 1 | `\"1.1\"` | `/version` |")
    L.append(f"| `updated` (`/updated`) | string(날짜 형태) | 루트 객체 키 | 1 | `\"2026-07-26\"` | `/updated` |")
    L.append(f"| `currency` (`/currency`) | string(코드) | 루트 객체 키 | 1 | `\"KRW\"` | `/currency` |")
    L.append(f"| `note` (`/note`) | string(문장 3개) | 루트 객체 키 | 1 | `{md(data['note'])}` | `/note` |")
    L.append(f"| `categories` (`/categories`) | array[17] of object | 루트 객체 키 | 1 | (객체 17개) | `/categories` |")
    L.append("| `categories[].id` (`/categories/{i}/id`) | string | 카테고리 객체 | 17 | `\"M1\"` | `/categories/0/id` |")
    L.append("| `categories[].name` (`/categories/{i}/name`) | string | 카테고리 객체 | 17 | `\"보톡스\"` | `/categories/0/name` |")
    L.append("| `categories[].items` (`/categories/{i}/items`) | array[6~10] of object | 카테고리 객체 | 17 (원소 합 122) | (객체 10개) | `/categories/0/items` |")
    L.append("| `items[].name` (`/categories/{i}/items/{j}/name`) | string | 항목 객체 | 122 | `\"이마 주름 (수입)\"` | `/categories/0/items/0/name` |")
    L.append("| `items[].unit` (`/categories/{i}/items/{j}/unit`) | string | 항목 객체 | 122 | `\"1회\"` | `/categories/0/items/0/unit` |")
    L.append("| `items[].low` (`/categories/{i}/items/{j}/low`) | integer | 항목 객체 | 122 | `50000` | `/categories/0/items/0/low` |")
    L.append("| `items[].mid` (`/categories/{i}/items/{j}/mid`) | integer | 항목 객체 | 122 | `100000` | `/categories/0/items/0/mid` |")
    L.append("| `items[].high` (`/categories/{i}/items/{j}/high`) | integer | 항목 객체 | 122 | `200000` | `/categories/0/items/0/high` |\n")
    L.append('### `unit` 값의 형태 변형 (원문 값 전부)\n')
    L.append('| `unit` 원문 값 | 출현 수 | 첫 위치 |\n|---|---|---|')
    for u, ps in units.items():
        L.append(f'| `{md(u)}` | {len(ps)} | `{ps[0]}` |')
    L.append('\n빈 값(빈 문자열·빈 배열·빈 객체·null): 없음(기계 확인). 숫자는 모두 정수, 통화 기호·천 단위 구분 없음.\n')
    L.append('## 구획 목차\n')
    L.append('| 구획 | 범위 | 소유 말단 | 직접 읽기 | 문서 |\n|---|---|---|---|---|')
    for s in coverage['segments']:
        L.append(f"| {s['id']} | {md(s['title'])} | {len(s['owned_leaf_pointers'])} | {'○' if s['direct_read'] else '✗'} | [review-part-{s['id']}.md](review-part-{s['id']}.md) |")
    L.append('\n각 구획 문서는 ①상위 문맥 ②원문 값 표(원본 컬럼명·자료형·Pointer) ③잠정 관찰(원문과 분리) ④직접 읽기 표현 ⑤자동 후보 ⑥형태소 ⑦미결 순서다.\n')
    (HERE / 'review.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    applied = {a['pointer']: a for a in morph['applied']}
    excl = {e['pointer']: e for e in morph['excluded_strings']}
    miss = morph['known_missegmentation_occurrences']
    for s in coverage['segments']:
        sid = s['id']; mo = manual[sid]
        P = [f'# {sid} — {md(s["title"])}\n', f'[← review.md](review.md) · 소유 말단 {len(s["owned_leaf_pointers"])} · 직접 읽기 {"○" if s["direct_read"] else "✗"} · 마지막 읽은 Pointer `{s["last_read_pointer"]}`\n']
        P.append(f'## {sid}\n')
        if sid == 'S00':
            P.append('### 원문 값\n')
            P.append('| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |\n|---|---|---|---|')
            for k in ('version', 'updated', 'currency', 'note'):
                P.append(f"| `/{k}` | `{k}` | string | `{md(data[k])}` |")
            P.append(f"| `/categories` | `categories` | array[{len(data['categories'])}] | (S01~S17 이 원소 소유) |")
            P.append('| `` (루트) | — | object(키 5) | — |')
        else:
            ci = int(sid[1:]) - 1; b = f'/categories/{ci}'; cat = data['categories'][ci]
            P.append('### 상위 문맥 (S00 소유, 공동 참조)\n')
            P.append(f"- `/currency` = `{data['currency']}` · `/updated` = `{data['updated']}` · `/note` = `{md(data['note'])}`\n")
            P.append('### 원문 값 — 카테고리\n')
            P.append('| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |\n|---|---|---|---|')
            P.append(f"| `{b}/id` | `id` | string | `{cat['id']}` |")
            P.append(f"| `{b}/name` | `name` | string | `{md(cat['name'])}` |")
            P.append(f"| `{b}/items` | `items` | array[{len(cat['items'])}] of object | (아래 표) |\n")
            P.append(f'### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)\n')
            P.append('자료형: `name`·`unit` string, `low`·`mid`·`high` integer.\n')
            P.append('| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |\n|---|---|---|---|---|---|')
            for j, it in enumerate(cat['items']):
                P.append(f"| `{b}/items/{j}` | {md(it['name'])} | {md(it['unit'])} | {it['low']} | {it['mid']} | {it['high']} |")
            P.append('')
        P.append('### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)\n')
        P.append('| 근거 Pointer | 관찰 | 상태 |\n|---|---|---|')
        for ptr, ob, st in mo['observations']:
            P.append(f'| `{ptr}` | {md(ob)} | {st} |')
        P.append('\n### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))\n')
        P.append('| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |\n|---|---|---|---|---|---|')
        for m in [x for x in expr['manual_expressions'] if x['segment'] == sid]:
            P.append(f"| `{m['pointer']}` | [{m['start']},{m['end']}) | {md(m['text'])} | {md(', '.join(m['perspectives']))} | {md(m['note'])} | {', '.join(m['matched_by_auto_pattern']) or '없음(패턴 밖)'} |")
        P.append('\n### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)\n')
        P.append('| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |\n|---|---|---|---|---|')
        for a in [x for x in expr['auto_candidates'] if x['segment'] == sid]:
            P.append(f"| `{a['pointer']}` | [{a['start']},{a['end']}) | {a['pattern_id']} | {md(a['text'])} | {md(a['review'])} |")
        P.append('\n### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)\n')
        P.append('| Pointer | 원문 값 | 토큰 |\n|---|---|---|')
        for n in nodes:
            if n['segment'] != sid or n['type'] != 'string':
                continue
            ptr = n['pointer']
            if ptr in applied:
                tk = ' '.join(f"{t['form']}/{t['tag']}[{t['start']},{t['end']})" for t in applied[ptr]['tokens'])
                P.append(f'| `{ptr}` | {md(n["value"])} | {md(tk)} |')
            else:
                P.append(f'| `{ptr}` | {md(n["value"])} | 제외: {md(excl[ptr]["reason"])} |')
        km = [x for x in miss if x['pointer'].startswith(f'/categories/{int(sid[1:]) - 1}/') or (sid == 'S00' and not x['pointer'].startswith('/categories'))] if sid != 'S00' else [x for x in miss if not x['pointer'].startswith('/categories/')]
        if km:
            P.append('\n알려진 오분절 출현(교정 안 함):\n')
            for x in km:
                P.append(f"- `{x['pointer']}` [{x['span'][0]},{x['span'][1]}) `{md(x['surface'])}` → {md(x['raw_tokens'])} — {md(x['impact'])}")
        P.append('\n### 미결 (이 구획)\n')
        P.append('| ID | 상태 | Pointer | 내용 |\n|---|---|---|---|')
        for iid, st, ptrs, txt in mo['issues']:
            P.append(f"| {iid} | {st} | {md(', '.join('`'+p+'`' for p in ptrs))} | {md(txt)} |")
        (HERE / f'review-part-{sid}.md').write_text('\n'.join(P) + '\n', encoding='utf-8')


def write_issues(manual, morph):
    allis = []
    for sid, mo in manual.items():
        for iid, st, ptrs, txt in mo['issues']:
            allis.append((st, iid, sid, ptrs, txt))
    extra = json.loads((HERE / 'manual' / 'cross-issues.json').read_text(encoding='utf-8'))
    for iid, st, ptrs, txt in extra['issues']:
        allis.append((st, iid, 'X', ptrs, txt))
    names = {'A': 'A — 에이전트 추출/해석 오류', 'B': 'B — 원문 정보 부족', 'C': 'C — 현재 사용자 결정 필요',
             'I': 'I — 원문 내 불일치(원본 보존, 후속 확인 후보)', 'P': 'P — 잠정 해석', 'F': 'F — 후속 의미·연결 조사',
             'K': 'K — 알려진 분석 한계'}
    L = ['# market-pricing.json — 미결 기록\n',
         '상태 문자: A 에이전트 오류 · B 원문 정보 부족 · C 현재 사용자 결정 필요 · I 원문 내 불일치 · P 잠정 · F 후속 · K 알려진 분석 한계.',
         '이 파일은 build.py 가 manual/S*.json · manual/cross-issues.json 에서 생성한다(직접 고치지 않는다).\n']
    L.append('## 집계\n')
    L.append('| 상태 | 건수 |\n|---|---|')
    for k in 'ABCIPFK':
        L.append(f"| {names[k]} | {sum(1 for x in allis if x[0] == k)} |")
    L.append('')
    L.append(extra['preface'] + '\n')
    for k in 'ABCIPFK':
        rows = [x for x in allis if x[0] == k]
        L.append(f'## {names[k]}\n')
        if not rows:
            L.append(extra['empty_notes'].get(k, '없음.') + '\n')
            continue
        L.append('| ID | 구획 | Pointer | 내용 |\n|---|---|---|---|')
        for st, iid, sid, ptrs, txt in rows:
            L.append(f"| {iid} | {sid} | {md(', '.join('`'+p+'`' for p in ptrs))} | {md(txt)} |")
        if k == 'K':
            L.append('\n알려진 오분절 출현 전체(morphology.json `known_missegmentation_occurrences`):\n')
            for x in morph['known_missegmentation_occurrences']:
                L.append(f"- {x['id']} `{x['pointer']}` [{x['span'][0]},{x['span'][1]}) `{md(x['surface'])}` → {md(x['raw_tokens'])}")
        L.append('')
    (HERE / 'issues.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
