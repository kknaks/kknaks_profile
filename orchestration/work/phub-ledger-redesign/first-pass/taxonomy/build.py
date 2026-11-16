#!/usr/bin/env python3
"""taxonomy.json 1차 조사 산출물 재현 빌드.

실행(레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/taxonomy/build.py
  (--no-morph : kiwi 없이 구조·구획·읽기 렌더만 갱신)

입력: 원본 taxonomy.json (읽기 전용), manual/*.json (직접 읽기 기록)
출력: 이 폴더 안의 source-map.json, coverage.json, morphology.json + morphology/*.json,
      expressions.json, review.md, review-part-*.md, issues.md, reading/*.txt, build-output.txt
원본은 열기만 하고 쓰지 않는다.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
SRC_REL = 'orchestration/work/phub-recommend/bronze/phub-ledger/taxonomy.json'
SRC = os.path.join(ROOT, SRC_REL)
OUT_REL = 'orchestration/work/phub-ledger-redesign/first-pass/taxonomy'
TARGET_CHARS = 9000  # 구획 하나의 대략적 렌더 분량(값 경계에서만 자른다)
NO_MORPH = '--no-morph' in sys.argv


def jp_escape(k):
    return str(k).replace('~', '~0').replace('/', '~1')


# ---------------------------------------------------------------- 원문 스캐너
class Scanner:
    """원본 바이트를 직접 훑어 모든 값·키 리터럴의 바이트 구간과 출현 순서를 얻는다.
    중복 키는 덮어쓰지 않고 출현 순서로 기록한다."""

    WS = b' \t\r\n'

    def __init__(self, raw):
        self.raw = raw
        self.i = 0
        self.nodes = []  # dict(pointer, kind, bs, be, key_bs, key_be, parent, key, index, order)
        self.dups = []

    def ws(self):
        r = self.raw
        while self.i < len(r) and r[self.i] in self.WS:
            self.i += 1

    def string_end(self, s):
        r = self.raw
        j = s + 1
        while True:
            c = r[j]
            if c == 0x5C:
                j += 2
                continue
            if c == 0x22:
                return j + 1
            j += 1

    def value(self, pointer, parent, key, index, key_span):
        self.ws()
        r = self.raw
        s = self.i
        c = r[s]
        node = {'pointer': pointer, 'parent': parent, 'key': key, 'index': index,
                'key_bs': key_span[0] if key_span else None,
                'key_be': key_span[1] if key_span else None, 'order': len(self.nodes)}
        self.nodes.append(node)
        if c == 0x7B:  # {
            node['kind'] = 'object'
            self.i += 1
            self.ws()
            seen = Counter()
            if r[self.i] == 0x7D:
                self.i += 1
            else:
                while True:
                    self.ws()
                    ks = self.i
                    ke = self.string_end(ks)
                    k = json.loads(r[ks:ke].decode('utf-8'))
                    seen[k] += 1
                    if seen[k] > 1:
                        self.dups.append({'object': pointer, 'key': k, 'occurrence': seen[k], 'key_byte_span': [ks, ke]})
                    self.i = ke
                    self.ws()
                    assert r[self.i] == 0x3A
                    self.i += 1
                    cp = pointer + '/' + jp_escape(k)
                    if seen[k] > 1:
                        cp += '#dup%d' % seen[k]
                    self.value(cp, pointer, k, None, (ks, ke))
                    self.ws()
                    if r[self.i] == 0x2C:
                        self.i += 1
                        continue
                    assert r[self.i] == 0x7D
                    self.i += 1
                    break
        elif c == 0x5B:  # [
            node['kind'] = 'array'
            self.i += 1
            self.ws()
            n = 0
            if r[self.i] == 0x5D:
                self.i += 1
            else:
                while True:
                    self.value(pointer + '/' + str(n), pointer, None, n, None)
                    n += 1
                    self.ws()
                    if r[self.i] == 0x2C:
                        self.i += 1
                        continue
                    assert r[self.i] == 0x5D
                    self.i += 1
                    break
        elif c == 0x22:
            node['kind'] = 'string'
            self.i = self.string_end(s)
        else:
            m = re.compile(rb'-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null').match(r, s)
            assert m, s
            lit = m.group(0)
            node['kind'] = {b'true': 'boolean', b'false': 'boolean', b'null': 'null'}.get(lit, 'number')
            self.i = m.end()
        node['bs'] = s
        node['be'] = self.i
        return node


def load_source():
    raw = open(SRC, 'rb').read()
    text = raw.decode('utf-8')
    sc = Scanner(raw)
    sc.value('', None, None, None, None)
    sc.ws()
    assert sc.i == len(raw), 'trailing data'
    # 바이트 → 코드포인트 오프셋 표
    b2c = {}
    ci = 0
    bi = 0
    for ch in text:
        b2c[bi] = ci
        bi += len(ch.encode('utf-8'))
        ci += 1
    b2c[bi] = ci
    return raw, text, sc.nodes, sc.dups, b2c


def get_value(raw, n):
    return json.loads(raw[n['bs']:n['be']].decode('utf-8'))


# ---------------------------------------------------------------- 구획 계획
def plan_sections(nodes_by_ptr, children, data):
    """문맥 단위(상위 객체·하위분류·항목 범위)로 구획을 만든다. 값 중간을 자르지 않는다."""
    def subtree(p):
        out = [p]
        for c in children.get(p, []):
            out.extend(subtree(c))
        return out

    def size(ptrs):
        s = 0
        for p in ptrs:
            n = nodes_by_ptr[p]
            s += 6 + (len(n['value']) if n['kind'] == 'string' else 8)
        return s

    sections = []

    def ctx_of(p):
        return ancestors_ctx(p, nodes_by_ptr)

    sections.append({'units': [('root', ['', '/modality', '/problem'])], 'scope': '루트 컨테이너'})

    def pack(top_ptr, units, label_prefix):
        cur = []
        cur_size = 0
        for name, ptrs in units:
            s = size(ptrs)
            if cur and cur_size + s > TARGET_CHARS:
                sections.append({'units': cur, 'scope': label_prefix})
                cur, cur_size = [], 0
            cur.append((name, ptrs))
            cur_size += s
        if cur:
            sections.append({'units': cur, 'scope': label_prefix})

    for top in ('modality', 'problem'):
        punits = []
        for i, ent in enumerate(data[top]):
            ep = '/%s/%d' % (top, i)
            units = []
            for k in ent.keys():
                kp = ep + '/' + jp_escape(k)
                if k == 'subcategories':
                    units.append(('%s 컨테이너' % k, [ep, kp] if not units else [kp]))
                    for si, sc in enumerate(ent[k]):
                        sp = kp + '/' + str(si)
                        head = [sp] + [sp + '/' + jp_escape(kk) for kk in sc.keys() if kk != 'items']
                        ip = sp + '/items'
                        head.append(ip)
                        item_units = [('%s items/%d' % (sc['id'], ii), subtree(ip + '/' + str(ii))) for ii in range(len(sc['items']))]
                        if item_units:
                            item_units[0] = (item_units[0][0], head + item_units[0][1])
                        else:
                            item_units = [('%s (items 비어 있음)' % sc['id'], head)]
                        units.extend(item_units)
                elif k == 'products':
                    units.append(('products 컨테이너', [kp]))
                    for pi in range(len(ent[k])):
                        units.append(('%s' % ent[k][pi]['id'], subtree(kp + '/' + str(pi))))
                else:
                    sub = subtree(kp)
                    if not units:
                        sub = [ep] + sub
                    units.append((k, sub))
            if top == 'modality':
                pack(ep, units, '%s %s' % (ent['id'], ent['category']))
            else:
                punits.extend(units)
        if punits:
            pack('/problem', punits, 'problem')
    for n, s in enumerate(sections):
        s['id'] = 'S%03d' % n
        s['owned'] = [p for _, ptrs in s['units'] for p in ptrs]
        s['unit_names'] = [u for u, _ in s['units']]
        del s['units']
    return sections


def ancestors_ctx(p, nodes_by_ptr):
    """조상 객체 중 id/category/label/name 이 있는 것의 Pointer·이름."""
    out = []
    parts = p.split('/')
    for k in range(1, len(parts)):
        ap = '/'.join(parts[:k])
        n = nodes_by_ptr.get(ap)
        if not n or n['kind'] != 'object':
            continue
        info = {'pointer': ap}
        for f in ('id', 'category', 'label', 'name'):
            fp = ap + '/' + f
            if fp in nodes_by_ptr and nodes_by_ptr[fp]['kind'] == 'string':
                info[f] = nodes_by_ptr[fp]['value']
        if len(info) > 1:
            out.append(info)
    return out


def rel(p, base):
    return p[len(base):] if base and p.startswith(base) else p


def main():
    raw, text, nodes, dups, b2c = load_source()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(text)
    nodes_by_ptr = OrderedDict()
    children = defaultdict(list)
    for n in nodes:
        v = get_value(raw, n)
        if n['kind'] in ('object', 'array'):
            n['child_count'] = len(v)
            n['empty'] = len(v) == 0
        else:
            n['value'] = v
            n['empty'] = (v == '')
        nodes_by_ptr[n['pointer']] = n
        if n['parent'] is not None:
            children[n['parent']].append(n['pointer'])

    sections = plan_sections(nodes_by_ptr, children, data)
    owner = {}
    for s in sections:
        for p in s['owned']:
            assert p not in owner, ('dup owner', p)
            owner[p] = s['id']
    assert set(owner) == set(nodes_by_ptr), 'section ownership mismatch'

    # ------------------------------------------------ source-map.json
    def gen_pattern(p):
        return re.sub(r'/\d+(?=/|$)', '/*', p)

    sm_nodes = []
    for p, n in nodes_by_ptr.items():
        rec = OrderedDict()
        rec['pointer'] = p
        rec['order'] = n['order']
        rec['parent'] = n['parent']
        rec['key'] = n['key']
        rec['index'] = n['index']
        rec['path_pattern'] = gen_pattern(p)
        rec['type'] = n['kind']
        if n['kind'] in ('object', 'array'):
            rec['child_count'] = n['child_count']
            if n['kind'] == 'object':
                rec['keys_in_order'] = [nodes_by_ptr[c]['key'] for c in children.get(p, [])]
        else:
            rec['value'] = n['value']
            if n['kind'] == 'string':
                rec['value_codepoints'] = len(n['value'])
        rec['empty'] = n['empty']
        rec['literal_byte_span'] = [n['bs'], n['be']]
        rec['literal_codepoint_span'] = [b2c[n['bs']], b2c[n['be']]]
        if n['key_bs'] is not None:
            rec['key_literal_byte_span'] = [n['key_bs'], n['key_be']]
        rec['section'] = owner[p]
        rec['context'] = ancestors_ctx(p, nodes_by_ptr)
        sm_nodes.append(rec)
    source_map = OrderedDict([
        ('source', SRC_REL), ('sha256', sha), ('bytes', len(raw)), ('codepoints', len(text)),
        ('encoding', 'utf-8 (BOM 없음)'),
        ('span_units', {
            'literal_byte_span': '원본 파일 UTF-8 바이트 오프셋 [start,end) — JSON 리터럴(문자열이면 따옴표 포함)',
            'literal_codepoint_span': '원본 파일 전체를 UTF-8 디코딩한 문자열의 코드포인트 오프셋 [start,end) — JSON 리터럴',
            'key_literal_byte_span': '객체 멤버 키 리터럴(따옴표 포함)의 바이트 [start,end)',
            'value': 'JSON 디코딩된 값. 형태소·표현 구간은 이 디코딩 문자열의 코드포인트 [start,end)',
        }),
        ('escape_check', {'note': '문자열 리터럴 내 백슬래시 이스케이프 출현 수(바이트 0x5C)', 'count': raw.count(b'\\')}),
        ('duplicate_keys', dups),
        ('pointer_note', 'RFC 6901 JSON Pointer. 중복 키가 있으면 #dupN 접미사(이 원본에는 없음)'),
        ('node_count', len(sm_nodes)),
        ('nodes', sm_nodes),
    ])
    json.dump(source_map, open(os.path.join(HERE, 'source-map.json'), 'w'), ensure_ascii=False, separators=(',', ':'))

    # ------------------------------------------------ 직접 읽기 기록 불러오기
    manual = {}
    mdir = os.path.join(HERE, 'manual')
    for fn in sorted(os.listdir(mdir)):
        if fn.endswith('.json'):
            m = json.load(open(os.path.join(mdir, fn)))
            manual[m['section']] = m
    global_issues = manual.pop('GLOBAL', None)

    # ------------------------------------------------ 읽기 렌더
    rdir = os.path.join(HERE, 'reading')
    for s in sections:
        lines = ['# %s  scope=%s  units=%s' % (s['id'], s['scope'], ' | '.join(s['unit_names']))]
        first = s['owned'][0]
        lines.append('# 상위 문맥: ' + json.dumps(ancestors_ctx(first, nodes_by_ptr), ensure_ascii=False))
        base = None
        owned_set = set(s['owned'])
        done = set()
        for p in s['owned']:
            if p in done:
                continue
            n = nodes_by_ptr[p]
            m_ = re.match(r'^(/\w+/\d+(?:/subcategories/\d+)?(?:/(?:items|products)/\d+)?)', p)
            b = m_.group(1) if m_ else ''
            if b != base:
                base = b
                info = ancestors_ctx(b + '/x', nodes_by_ptr)[-1:] if b else []
                lines.append('@ %s %s' % (b or '(root)', ' '.join(str(info[0].get(f)) for f in ('id', 'label', 'name', 'category') if info and info[0].get(f))))
            r = p[len(b):] or '.'
            if n['kind'] == 'object':
                ks = [nodes_by_ptr[c]['key'] for c in children.get(p, [])]
                lines.append('  %s {%s}' % (r, ','.join(ks)))
            elif n['kind'] == 'array':
                ch = children.get(p, [])
                if ch and all(c in owned_set and nodes_by_ptr[c]['kind'] not in ('object', 'array') for c in ch):
                    lines.append('  %s [%d] = %s' % (r, len(ch), ' ‖ '.join('%d:%s' % (i, json.dumps(nodes_by_ptr[c]['value'], ensure_ascii=False)) for i, c in enumerate(ch))))
                    done.update(ch)
                else:
                    lines.append('  %s [%d]' % (r, n['child_count']))
            else:
                lines.append('  %s = %s' % (r, json.dumps(n['value'], ensure_ascii=False)))
        open(os.path.join(rdir, s['id'] + '.txt'), 'w').write('\n'.join(lines) + '\n')

    # ------------------------------------------------ 형태소
    text_leaves = [n for n in nodes_by_ptr.values() if n['kind'] == 'string']
    morph_index = None
    if not NO_MORPH:
        seg_src = dict(manual)
        if global_issues:
            seg_src['GLOBAL'] = global_issues
        morph_index = build_morphology(text_leaves, nodes_by_ptr, owner, sections, seg_src)

    # ------------------------------------------------ 표현
    expr = build_expressions(text_leaves, owner, manual, nodes_by_ptr)

    # ------------------------------------------------ coverage
    cov_secs = []
    for s in sections:
        m = manual.get(s['id'])
        leaves = [p for p in s['owned'] if nodes_by_ptr[p]['kind'] not in ('object', 'array') or nodes_by_ptr[p]['empty']]
        cov_secs.append(OrderedDict([
            ('id', s['id']), ('scope', s['scope']), ('units', s['unit_names']),
            ('pointer_first', s['owned'][0]), ('pointer_last', s['owned'][-1]),
            ('context_refs', ancestors_ctx(s['owned'][0], nodes_by_ptr)),
            ('owned_pointers', s['owned']),
            ('owned_leaf_or_empty_container_count', len(leaves)),
            ('owned_node_count', len(s['owned'])),
            ('machine_extracted', True),
            ('read_state', m['state'] if m else 'unread'),
            ('read_last_pointer', m.get('last_pointer') if m else None),
            ('reading_render', 'reading/%s.txt' % s['id']),
            ('manual_record', ('manual/%s.json' % s['id']) if m else None),
            ('review_file', 'review-part-%s.md' % s['id']),
        ]))
    coverage = OrderedDict([
        ('source', SRC_REL), ('sha256', sha),
        ('ownership_rule', '각 노드(컨테이너·말단·빈 컨테이너)는 정확히 한 구획이 소유한다. context_refs 는 공동 참조(소유 아님).'),
        ('read_state_values', {'unread': '계획·기계 추출만 됨(미독)', 'read': '읽기 렌더를 직접 읽고 manual 기록 저장'}),
        ('section_count', len(sections)),
        ('sections', cov_secs),
    ])
    json.dump(coverage, open(os.path.join(HERE, 'coverage.json'), 'w'), ensure_ascii=False, indent=1)

    # ------------------------------------------------ review
    build_review(sections, nodes_by_ptr, children, manual, sha, len(raw), expr, morph_index)
    build_issues(sections, manual, global_issues, morph_index)

    out = ['sha256=%s bytes=%d nodes=%d sections=%d text_leaves=%d dups=%d' % (sha, len(raw), len(nodes_by_ptr), len(sections), len(text_leaves), len(dups)),
           'read_sections=%d/%d' % (sum(1 for s in sections if manual.get(s['id'], {}).get('state') == 'read'), len(sections)),
           'expressions auto=%d manual=%d' % (expr['auto_count'], expr['manual_count'])]
    if morph_index:
        out.append('morph applied=%d excluded=%d tokens=%d' % (morph_index['applied_count'], morph_index['excluded_count'], morph_index['token_count']))
    open(os.path.join(HERE, 'build-output.txt'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))


# ---------------------------------------------------------------- 형태소
ID_KEYS = {'id'}


def morph_decision(n):
    """값 하나의 형태소 적용/제외와 사유."""
    k = n['key']
    parent_key = None
    if n['index'] is not None:
        parent_key = n['parent'].rsplit('/', 1)[-1]
    if k in ID_KEYS:
        return False, 'ID/코드값(id 필드) — 언어 텍스트 아님'
    if parent_key == 'modality_ref':
        return False, 'ID/코드값(modality_ref 배열 원소) — 다른 항목 id 참조'
    if k == 'reclassified_to':
        return False, 'ID/코드값(reclassified_to) — 카테고리 id 참조'
    if n['value'] == '':
        return False, '빈 문자열 — 분석할 텍스트 없음'
    return True, None


def build_morphology(text_leaves, nodes_by_ptr, owner, sections, manual):
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type='cong')
    seg_rules = []
    for sid, m in manual.items():
        for e in m.get('seg_errors', []):
            e = dict(e)
            e['from_section'] = sid
            seg_rules.append(e)
    parts = defaultdict(list)
    excluded = []
    token_count = 0
    applied = 0
    for n in text_leaves:
        ok, reason = morph_decision(n)
        if not ok:
            excluded.append({'pointer': n['pointer'], 'key': n['key'], 'value': n['value'], 'reason': reason, 'section': owner[n['pointer']]})
            continue
        v = n['value']
        toks = kiwi.tokenize(v)
        arr = []
        for t in toks:
            arr.append([t.form, t.tag, t.start, t.start + t.len, v[t.start:t.start + t.len], t.lemma if t.lemma != t.form else None])
        token_count += len(arr)
        applied += 1
        parts[owner[n['pointer']]].append({'pointer': n['pointer'], 'role': 'text_value', 'text': v, 'tokens': arr})
    # 필드명: 고유 키마다 분석, 출현 위치 목록
    key_occ = defaultdict(list)
    for n in nodes_by_ptr.values():
        if n['key'] is not None:
            key_occ[n['key']].append(n['pointer'])
    field_names = []
    for k in sorted(key_occ):
        toks = kiwi.tokenize(k)
        field_names.append({'field_name': k, 'role': 'field_name', 'tokens': [[t.form, t.tag, t.start, t.start + t.len, k[t.start:t.start + t.len], t.lemma if t.lemma != t.form else None] for t in toks],
                            'note': '스키마 키(영문 snake_case). 분석은 적용했으나 언어 텍스트와 역할이 다르다 — 키 이름 자체는 의미 단서가 아니라 원본 컬럼명으로 보존',
                            'occurrences': key_occ[k]})
    # 알려진 오분절 — 출현별 표시
    flagged = []
    for sec, lst in parts.items():
        for rec in lst:
            for r in seg_rules:
                if r.get('tag'):
                    for t in rec['tokens']:
                        if t[1] == r['tag']:
                            flagged.append({'pointer': rec['pointer'], 'section': sec, 'span': [t[2], t[3]], 'surface': t[4],
                                            'raw_tokens': [[t[0], t[1]]], 'issue': r['issue'], 'impact': r.get('impact'),
                                            'rule_from': r.get('from_section'), 'status': 'K'})
                    continue
                if r.get('scope') == 'all' or r.get('pointer') == rec['pointer']:
                    surf = r['surface']
                    start = 0
                    while True:
                        i = rec['text'].find(surf, start)
                        if i < 0:
                            break
                        toks = [t for t in rec['tokens'] if t[2] < i + len(surf) and t[3] > i]
                        flagged.append({'pointer': rec['pointer'], 'section': sec, 'span': [i, i + len(surf)], 'surface': surf,
                                        'raw_tokens': [[t[0], t[1]] for t in toks], 'issue': r['issue'], 'impact': r.get('impact'),
                                        'rule_from': r.get('from_section'), 'status': 'K'})
                        start = i + len(surf)
    os.makedirs(os.path.join(HERE, 'morphology'), exist_ok=True)
    part_files = []
    for s in sections:
        lst = parts.get(s['id'], [])
        fn = 'morphology/%s.json' % s['id']
        body = json.dumps({'section': s['id'], 'records': lst}, ensure_ascii=False, separators=(',', ':'))
        open(os.path.join(HERE, fn), 'w').write(body)
        part_files.append({'section': s['id'], 'file': fn, 'records': len(lst), 'sha256': hashlib.sha256(body.encode()).hexdigest()})
    idx = OrderedDict([
        ('analyzer', {'name': 'kiwipiepy', 'version': kiwipiepy.__version__, 'model_type': kiwi.model_type,
                      'num_workers': 1, 'load_default_dict': '기본값(True)', 'typos': None, 'user_dictionary': None,
                      'tokenize_options': '기본값(match_options=ALL, normalize_coda=False, split_complex=False, saisiot=None)',
                      'run': 'uv run --python 3.12 --with kiwipiepy==0.24.1', 'tagset': 'Kiwi 세종 확장 품사 (NNG/NNP/NNB/VV/VA/XSV/ETM/EC/EF/JK*/SL/SN/SW/SO/SSO/SSC/SP/SF/W_* 등)'}),
        ('token_schema', ['form(분석기 형태소형)', 'tag', 'start', 'end', 'surface=text[start:end]', 'lemma(분석기 제공 lemma가 form 과 다를 때만, 아니면 null)']),
        ('span_unit', '디코딩된 값 문자열의 코드포인트 [start,end). 축약 형태소(예: 하+ᆯ)는 같은 구간을 겹쳐 가리킬 수 있고 form 은 표면형과 다를 수 있다(분석기 출력 그대로). 생략된 서술격 조사 등은 분석기가 길이 0 토큰(start==end, surface \"\")으로 내며 그대로 보존했다.'),
        ('base_form_note', 'lemma 는 kiwipiepy Token.lemma 값 그대로. 분석기가 주지 않은 기본형을 만들지 않았다.'),
        ('normalization', '원문 정규화 없음 — 디코딩 값 그대로 분석'),
        ('applied_count', applied), ('excluded_count', len(excluded)), ('token_count', token_count),
        ('excluded', excluded),
        ('non_text_values', '숫자·불리언·null 값은 형태소 대상 아님(source-map 에 원값 보존). 이 원본의 불리언/null: mfds, is_marketing_name'),
        ('field_names', field_names),
        ('known_segmentation_errors', flagged),
        ('parts', part_files),
    ])
    json.dump(idx, open(os.path.join(HERE, 'morphology.json'), 'w'), ensure_ascii=False, indent=1)
    return idx


# ---------------------------------------------------------------- 표현
PATTERNS = [
    ('수량·단위', r'\d+(?:[.,]\d+)?\s*(?:[~\-–]\s*\d+(?:[.,]\d+)?\s*)?(?:%|mm|cm|nm|µm|μm|㎛|ml|mL|cc|cm²|cm2|mg|g|kg|U|IU|유닛|단위|J|mJ|W|MHz|kHz|Hz|°C|℃|도|회|번|차|일|주|개월|달|년|시간|분|초|세|샷|라인|줄|개|종|배|층|ms|ns|ps)'),
    ('시간·시점', r'(?:즉시|당일|직후|이후|이전|이내|동안|후부터|부터|까지|매일|매주|매월|간격|주기|유지|지속|단기|장기|평생|영구|일시적)'),
    ('부정·금지', r'(?:않|없|금지|불가|금기|피해야|피하|삼가|아님|아니|못하|지양|불법|제외)'),
    ('가능성·빈도', r'(?:수 있|가능|우려|위험|드물|흔히|흔한|종종|간혹|때때로|일부|대부분|대체로|보통|주로|일반적)'),
    ('조건', r'(?:경우|때|시에|이면|라면|하면|되면|조건|단,|만약|따라|여부)'),
    ('정도·범위', r'(?:약간|경미|가벼운|심한|심하|매우|다소|최대|최소|이상|이하|미만|초과|정도|내외|사이|이내|범위|고용량|저용량|깊은|얕은|넓은|좁은)'),
    ('비교', r'(?:보다|대비|비해|달리|차이|동일|유사|더 |덜 )'),
    ('기호 결합', r'(?:[^\s,]+\+[^\s,]+|[^\s,]+/[^\s,]+|→|↑|↓|>|<|≥)'),
    ('괄호 병기', r'\([^()]*\)|\[[^\[\]]*\]'),
    ('참조·분류 언급', r'(?:M\d+(?:-[\w가-힣]+)*|참고|참조|통합|재분류|분류|카테고리|섹션|엔트리|cross-reference)'),
]


def sentence_spans(v):
    spans = []
    start = 0
    for m in re.finditer(r'(?<=[.!?])\s+|(?<=다\.)$', v):
        spans.append([start, m.start()])
        start = m.end()
    if start < len(v):
        spans.append([start, len(v)])
    return [s for s in spans if s[1] > s[0]] or [[0, len(v)]]


def build_expressions(text_leaves, owner, manual, nodes_by_ptr):
    auto = []
    for n in text_leaves:
        ok, _ = morph_decision(n)
        if not ok:
            continue
        v = n['value']
        sents = sentence_spans(v)
        for cat, pat in PATTERNS:
            for m in re.finditer(pat, v):
                s, e = m.start(), m.end()
                sent = next((x for x in sents if x[0] <= s < x[1]), [0, len(v)])
                auto.append({'pointer': n['pointer'], 'section': owner[n['pointer']], 'category_hint': cat,
                             'span': [s, e], 'text': v[s:e], 'sentence_span': sent, 'sentence': v[sent[0]:sent[1]]})
    man = []
    for sid, m in sorted(manual.items()):
        for x in m.get('expressions', []):
            n = nodes_by_ptr.get(x['pointer'])
            v = n['value'] if n and n['kind'] == 'string' else None
            occ = x.get('occurrence', 1)
            i = -1
            if v is not None:
                pos = -1
                for _ in range(occ):
                    pos = v.find(x['text'], pos + 1)
                    if pos < 0:
                        break
                i = pos
            rec = {'pointer': x['pointer'], 'section': sid, 'text': x['text'], 'occurrence': occ,
                   'span': [i, i + len(x['text'])] if i >= 0 else None, 'kinds': x.get('kinds', []),
                   'note': x.get('note', ''), 'status': x.get('status', 'P')}
            man.append(rec)
    out = OrderedDict([
        ('method', {'auto': '정규식 후보 추출(아래 패턴). 의미 해석이 아니라 수집 보조 — 오탐·누락 있음. 문장 구간은 마침표 뒤 공백 기준 단순 분할.',
                    'manual': '구획별 직접 읽기에서 수집한 복합 표현(manual/S###.json). span 은 값 문자열 코드포인트 [start,end).',
                    'patterns': [{'category_hint': c, 'regex': p} for c, p in PATTERNS],
                    'overlap': '같은 구간이 여러 category_hint 에 걸리는 겹침은 의도된 것(후보 관점이 다름). 같은 pointer·span·category_hint 중복은 생성 오류로 검증한다.'}),
        ('auto_count', len(auto)), ('manual_count', len(man)),
        ('manual', man),
        ('auto', auto),
    ])
    json.dump(out, open(os.path.join(HERE, 'expressions.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    return out


# ---------------------------------------------------------------- review
def md(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s.replace('|', '\\|') if s != '' else '`""` (빈 문자열)'


def build_review(sections, nodes_by_ptr, children, manual, sha, nbytes, expr, morph_index):
    # 컬럼 구성 표
    pat = OrderedDict()
    for p, n in nodes_by_ptr.items():
        g = re.sub(r'/\d+(?=/|$)', '/*', p)
        d = pat.setdefault(g, {'types': Counter(), 'first': p, 'n': 0, 'empty': [], 'parents': set()})
        d['types'][n['kind']] += 1
        d['n'] += 1
        if n['empty']:
            d['empty'].append(p)
        if n['parent'] is not None:
            d['parents'].add(re.sub(r'/\d+(?=/|$)', '/*', n['parent']))
    parent_count = Counter()
    for p, n in nodes_by_ptr.items():
        parent_count[re.sub(r'/\d+(?=/|$)', '/*', p)] += 1
    L = []
    L.append('# taxonomy.json — 1차 조사 (읽기용 목차)')
    L.append('')
    nread = sum(1 for s in sections if manual.get(s['id'], {}).get('state') == 'read')
    L.append('## 상태')
    L.append('')
    L.append('- 원본: `%s` · sha256 `%s` · %d bytes' % (SRC_REL, sha, nbytes))
    L.append('- 구획 %d개 중 직접 읽기 완료 %d개 (구획별 상태는 아래 목차와 `coverage.json`)' % (len(sections), nread))
    L.append('- 상세 상태·미결: [`validation.md`](validation.md) · [`issues.md`](issues.md) · 진행: [`progress.md`](progress.md)')
    L.append('- 이 문서와 review-part 는 원문 값(원본 컬럼명 그대로)과 잠정 관찰을 다른 칸·절로 분리한다. 관찰은 의미 확정이 아니다.')
    L.append('')
    L.append('| 항목 | 값 |')
    L.append('|---|---|')
    L.append('| 1차 범위 종료 | 예 — 전 구획 직접 읽기·구조/값·형태소/표현 수집·기계 검증·읽기 검토 완료(근거 `validation.md`) |')
    L.append('| 원장 전체 완료 | **아니오** — 원문 부족(B)·원문 내 불일치(I)·후속 의미 조사(F)·알려진 분석 한계(K)가 남아 있다(`issues.md`) |')
    L.append('| 원문 노드 | %d (말단·빈 컨테이너 %d) |' % (len(nodes_by_ptr), sum(1 for n in nodes_by_ptr.values() if n['kind'] not in ('object', 'array') or n['empty'])))
    L.append('| 구조 | modality 17 · subcategories 74 · items 523 · products 59 · problem 14 · problem subcategories 53 · problem items 117 |')
    if morph_index:
        L.append('| 형태소 | 적용 %d · 제외 %d(사유 기록) · 토큰 %d · 필드명 %d · 알려진 오분절 표시 %d |' % (morph_index['applied_count'], morph_index['excluded_count'], morph_index['token_count'], len(morph_index['field_names']), len(morph_index['known_segmentation_errors'])))
    L.append('| 표현 | 정규식 후보 %d · 직접 읽기 수집 %d |' % (expr['auto_count'], expr['manual_count']))
    L.append('| 사용자 결정 필요(C) | 0 — 원본 변경 후보는 후속 확인 후보(F/I)로 기록, 지금 선택 요청 없음 |')
    L.append('')
    L.append('## 컬럼 구성 표')
    L.append('')
    L.append('경로 패턴의 `*` 는 배열 인덱스. 출현 수는 원문 노드 수. 「선택적」은 같은 부모 패턴 출현 수보다 적게 나오는 필드. 예시는 첫 출현 원문 값과 Pointer.')
    L.append('')
    L.append('| 원본 컬럼명/경로 패턴 | 자료형 | 중첩 구조 | 출현 수 | 선택적 | 빈 값 출현 | 원문 예시 | 예시 Pointer |')
    L.append('|---|---|---|---|---|---|---|---|')
    for g, dd in pat.items():
        n = nodes_by_ptr[dd['first']]
        if n['kind'] == 'object':
            ks = [nodes_by_ptr[c]['key'] for c in children.get(dd['first'], [])]
            nest = 'object{%s}' % ', '.join(ks)
            ex = '(객체)'
        elif n['kind'] == 'array':
            nest = 'array[%d]' % n['child_count']
            ex = '(배열)'
        else:
            nest = '말단'
            ex = md(n['value'])
            if len(ex) > 80:
                ex = ex[:80] + '…(전체는 해당 Pointer)'
        par = None
        if n['parent'] is not None:
            par = re.sub(r'/\d+(?=/|$)', '/*', n['parent'])
        opt = ''
        if par and nodes_by_ptr[n['parent']]['kind'] == 'object' and dd['n'] < parent_count[par]:
            opt = '예 (%d/%d)' % (dd['n'], parent_count[par])
        emp = '%d (예: `%s`)' % (len(dd['empty']), dd['empty'][0]) if dd['empty'] else '0'
        types = ', '.join('%s %d' % (t, c) for t, c in dd['types'].items())
        L.append('| `%s` | %s | %s | %d | %s | %s | %s | `%s` |' % (g or '(루트)', types, nest, dd['n'], opt, emp, ex, dd['first'] or '(루트)'))
    L.append('')
    L.append('## 구획 목차')
    L.append('')
    L.append('| 구획 | 범위 | 단위 | 소유 노드 | 읽기 상태 | 값 문서 |')
    L.append('|---|---|---|---|---|---|')
    for s in sections:
        st = manual.get(s['id'], {}).get('state', 'unread')
        u = s['unit_names']
        us = ', '.join(u) if len(u) <= 4 else '%s … %s (%d단위)' % (u[0], u[-1], len(u))
        L.append('| %s | %s | %s | %d | %s | [review-part-%s.md](review-part-%s.md) |' % (s['id'], s['scope'], us.replace('|', '\\|'), len(s['owned']), st, s['id'], s['id']))
    L.append('')
    open(os.path.join(HERE, 'review.md'), 'w').write('\n'.join(L) + '\n')

    man_by_sec = defaultdict(list)
    for x in expr['manual']:
        man_by_sec[x['section']].append(x)
    for s in sections:
        m = manual.get(s['id'], {})
        P = ['# %s — %s' % (s['id'], s['scope']), '']
        P.append('- 읽기 상태: **%s**%s' % (m.get('state', 'unread'), (' · 마지막 읽은 Pointer `%s`' % m.get('last_pointer')) if m.get('last_pointer') else ''))
        P.append('- 단위: %s' % ', '.join(s['unit_names']).replace('|', '\\|'))
        ctx = ancestors_ctx(s['owned'][0], nodes_by_ptr)
        P.append('- 상위 문맥(공동 참조·소유 아님): ' + ('; '.join('`%s` %s' % (c['pointer'], ' / '.join(str(c.get(f)) for f in ('id', 'category', 'label', 'name') if c.get(f))) for c in ctx) or '없음'))
        P.append('- 기계 기록: `source-map.json`(section=%s) · `morphology/%s.json` · `expressions.json`(section=%s) · 읽기 렌더 `reading/%s.txt`' % (s['id'], s['id'], s['id'], s['id']))
        P.append('')
        P.append('## 원문 값 (원본 컬럼명 그대로, 원본 순서)')
        P.append('')
        P.append('| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |')
        P.append('|---|---|---|---|')
        for p in s['owned']:
            n = nodes_by_ptr[p]
            col = n['key'] if n['key'] is not None else ('[%d]' % n['index'] if n['index'] is not None else '(루트)')
            if n['index'] is not None:
                col = '%s[%d]' % (n['parent'].rsplit('/', 1)[-1], n['index'])
            if n['kind'] == 'object':
                val = '{object, 키 %d: %s}' % (n['child_count'], ', '.join(nodes_by_ptr[c]['key'] for c in children.get(p, []))) if n['child_count'] else '`{}` (빈 객체)'
            elif n['kind'] == 'array':
                val = '[array, 원소 %d]' % n['child_count'] if n['child_count'] else '`[]` (빈 배열)'
            else:
                val = md(n['value'])
            P.append('| `%s` | %s | %s | %s |' % (p or '(루트)', col, n['kind'], val))
        P.append('')
        P.append('## 잠정 관찰 (원문 아님 · 직접 읽기 기록)')
        P.append('')
        obs = m.get('observations', [])
        if obs:
            P.append('| 상태 | 근거 Pointer | 관찰 |')
            P.append('|---|---|---|')
            for o in obs:
                P.append('| %s | %s | %s |' % (o.get('status', 'P'), ', '.join('`%s`' % x for x in (o['pointers'] if 'pointers' in o else [o.get('pointer', '')])), o['note'].replace('|', '\\|')))
        else:
            P.append('(기록 없음)' if m else '(미독 — 아직 직접 읽지 않음)')
        P.append('')
        P.append('## 수동 복합 표현 (원문 구간)')
        P.append('')
        ex = man_by_sec.get(s['id'], [])
        if ex:
            P.append('| Pointer | 구간 | 원문 표현 | 관점 | 메모 |')
            P.append('|---|---|---|---|---|')
            for x in ex:
                P.append('| `%s` | %s | %s | %s | %s |' % (x['pointer'], x['span'], x['text'].replace('|', '\\|'), ', '.join(x['kinds']), x['note'].replace('|', '\\|')))
        else:
            P.append('(없음)')
        P.append('')
        segs = m.get('seg_errors', [])
        P.append('## 형태소 분석 확인 (알려진 오분절 K)')
        P.append('')
        if segs:
            P.append('| 범위 | 표면형 | 문제 | 영향 |')
            P.append('|---|---|---|---|')
            for x in segs:
                P.append('| %s | %s | %s | %s |' % (x.get('scope', x.get('pointer')), x['surface'], x['issue'].replace('|', '\\|'), (x.get('impact') or '').replace('|', '\\|')))
        else:
            P.append('(없음)')
        P.append('')
        P.append('## 미결')
        P.append('')
        iss = m.get('issues', [])
        if iss:
            P.append('| ID | 상태 | Pointer | 내용 | 영향·후속 |')
            P.append('|---|---|---|---|---|')
            for x in iss:
                P.append('| %s | %s | %s | %s | %s |' % (x['id'], x['status'], ', '.join('`%s`' % y for y in x['pointers']), x['note'].replace('|', '\\|'), x.get('impact', '').replace('|', '\\|')))
        else:
            P.append('(없음)')
        P.append('')
        open(os.path.join(HERE, 'review-part-%s.md' % s['id']), 'w').write('\n'.join(P) + '\n')


def build_issues(sections, manual, global_issues, morph_index=None):
    L = ['# taxonomy.json — 미결 기록', '',
         '상태 문자: A=에이전트 추출/해석 오류(에이전트가 고칠 것) · B=원문 정보 부족 · C=현재 사용자 결정 필요 · K=알려진 분석 한계 · P=잠정 해석 · F=후속 의미 조사 · I=원문 내 불일치.',
         '원본 변경 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 선택 대기(C)로 올리지 않는다.', '']
    allis = []
    if global_issues:
        allis.extend(('GLOBAL', x) for x in global_issues.get('issues', []))
    for s in sections:
        for x in manual.get(s['id'], {}).get('issues', []):
            allis.append((s['id'], x))
    cnt = Counter(x['status'] for _, x in allis)
    L.append('## 집계')
    L.append('')
    L.append('| 상태 | 건수 |')
    L.append('|---|---|')
    for k in 'ABCKPFI':
        L.append('| %s | %d |' % (k, cnt.get(k, 0)))
    L.append('')
    if global_issues and global_issues.get('preamble'):
        L.append(global_issues['preamble'])
        L.append('')
    L.append('## 전체 목록')
    L.append('')
    L.append('| ID | 구획 | 상태 | Pointer | 내용 | 영향·후속 |')
    L.append('|---|---|---|---|---|---|')
    for sid, x in allis:
        L.append('| %s | %s | %s | %s | %s | %s |' % (x['id'], sid, x['status'], ', '.join('`%s`' % y for y in x['pointers']), x['note'].replace('|', '\\|'), x.get('impact', '').replace('|', '\\|')))
    L.append('')
    # 알려진 형태소 분석 한계(K) — 규칙별 출현 수
    L.append('## 알려진 형태소 분석 한계 (K · 규칙별)')
    L.append('')
    L.append('출현별 위치·원시 토큰은 `morphology.json` 의 `known_segmentation_errors`. 교정하지 않고 기본 분석 결과를 보존했다.')
    L.append('')
    L.append('| 기록 구획 | 표면형/태그 | 문제 | 영향 | 표시된 출현 수 |')
    L.append('|---|---|---|---|---|')
    cnt_rule = Counter()
    if morph_index:
        for f in morph_index['known_segmentation_errors']:
            cnt_rule[(f['rule_from'], f['surface'] if not f['issue'].startswith('kiwi 가') else '(tag W_SERIAL)')] += 1
    srcs = [('GLOBAL', global_issues)] if global_issues else []
    srcs += [(s['id'], manual.get(s['id'], {})) for s in sections]
    for sid, m in srcs:
        for e in (m or {}).get('seg_errors', []):
            key = (sid, e['surface'])
            n = cnt_rule.get(key, 0)
            if e.get('tag'):
                n = sum(v for (a, b), v in cnt_rule.items() if b == '(tag W_SERIAL)')
            L.append('| %s | %s | %s | %s | %d |' % (sid, e['surface'].replace('|', '\\|'), e['issue'].replace('|', '\\|'), (e.get('impact') or '').replace('|', '\\|'), n))
    L.append('')
    open(os.path.join(HERE, 'issues.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
