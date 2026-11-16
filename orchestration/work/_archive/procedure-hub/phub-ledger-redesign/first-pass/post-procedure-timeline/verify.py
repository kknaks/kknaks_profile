"""post-procedure-timeline 1차 조사 결과 독립 검증. 읽기 전용 — 어떤 파일도 쓰지 않는다.
레포 루트에서: python3 orchestration/work/phub-ledger-redesign/first-pass/post-procedure-timeline/verify.py
실패가 하나라도 있으면 exit 1.
"""
import hashlib, json, os, re, sys
from collections import Counter

_SELF = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_SELF, '../../../../..'))
# 변이 시험용: 결과 폴더 사본을 검증할 때만 VERIFY_RESULTS_DIR 로 바꾼다(기본은 이 파일의 폴더).
HERE = os.environ.get('VERIFY_RESULTS_DIR', _SELF)
SRC = os.path.join(ROOT, 'orchestration/work/phub-recommend/bronze/phub-ledger/post-procedure-timeline.json')
EXPECTED_SHA = 'd04c9fe494acd318d656f6dea6d19e33cb944a20440e312ca9bad41309c9742e'
fails, checks = [], Counter()

def ok(cond, name, detail=''):
    checks[name] += 1
    if not cond: fails.append(f'{name}: {detail}')

def load(n): return json.load(open(os.path.join(HERE, n), encoding='utf-8'))

raw0 = open(SRC, 'rb').read(); sha0 = hashlib.sha256(raw0).hexdigest()
ok(sha0 == EXPECTED_SHA, 'source_sha_start', sha0)
text = raw0.decode('utf-8')

# 1. 독립 파싱 — 중복 키
dups = []
def hook(pairs):
    c = Counter(k for k, _ in pairs)
    dups.extend(k for k, v in c.items() if v > 1)
    return dict(pairs)
data = json.loads(text, object_pairs_hook=hook)

sm, mo, ex, cov = load('source-map.json'), load('morphology.json'), load('expressions.json'), load('coverage.json')
for name, d in [('source-map', sm['source']), ('morphology', mo['source']), ('expressions', ex['source']), ('coverage', cov['source'])]:
    ok(d['sha256'] == sha0, 'recorded_sha', name)
ok(sm['source']['bytes'] == len(raw0), 'recorded_bytes')
ok(sm['source']['codepoints'] == len(text), 'recorded_codepoints')
ok(len(dups) == 0 and sm['source']['duplicate_keys'] == [], 'duplicate_keys', dups)

# 2. 독립 순회 — 전체 경로 집합
def esc(k): return k.replace('~', '~0').replace('/', '~1')
truth = {}
def walk(o, p):
    if isinstance(o, dict):
        truth[p] = ('object', list(o.keys()))
        for k, v in o.items(): walk(v, p + '/' + esc(k))
    elif isinstance(o, list):
        truth[p] = ('array', len(o))
        for i, v in enumerate(o): walk(v, f'{p}/{i}')
    else:
        t = 'null' if o is None else 'boolean' if isinstance(o, bool) else 'number' if isinstance(o, (int, float)) else 'string'
        truth[p] = (t, o)
walk(data, '')
nodes = sm['nodes']; NODE = {n['pointer']: n for n in nodes}
ok(len(NODE) == len(nodes), 'node_pointer_unique')
ok(set(NODE) == set(truth), 'pointer_set_bidirectional', f'missing={sorted(set(truth)-set(NODE))[:5]} extra={sorted(set(NODE)-set(truth))[:5]}')
for p, (t, v) in truth.items():
    n = NODE.get(p)
    if not n: continue
    ok(n['type'] == t, 'node_type', p)
    if t == 'object': ok(n['keys'] == v, 'object_keys_order', p)
    elif t == 'array': ok(n['length'] == v, 'array_length', p)
    else: ok(n['value'] == v and type(n['value']) == type(v), 'leaf_value', p)

# 3. 리터럴 구간 재현 (코드포인트 / 바이트)
prev = -1
for n in nodes:
    s, e = n['literal_cp']; bs, be = n['literal_byte']
    lit = text[s:e]
    ok(raw0[bs:be].decode('utf-8') == lit, 'byte_span_equals_cp_span', n['pointer'])
    if n['type'] not in ('object', 'array'):
        ok(json.loads(lit) == truth[n['pointer']][1], 'literal_reparse', n['pointer'])
    if n['type'] in ('object', 'array'):
        o = json.loads(lit)
        ok((list(o.keys()) if n['type'] == 'object' else len(o)) == truth[n['pointer']][1], 'container_literal_reparse', n['pointer'])
        for kl in n.get('key_literals', []):
            ks, ke = kl['literal_cp']
            ok(json.loads(text[ks:ke]) == kl['key'], 'key_literal', n['pointer'] + ' ' + kl['key'])
    ok(s >= prev, 'document_order', n['pointer']); prev = s
    if n['type'] == 'string' and not n['escaped']:
        ok(text[s+1:e-1] == n['value'], 'value_span_no_escape', n['pointer'])

strings = [n for n in nodes if n['type'] == 'string']
leaves = [n for n in nodes if n['type'] not in ('object', 'array')]
ok(sm['counts']['nodes'] == len(truth) and sm['counts']['leaves'] == len(leaves), 'counts_consistent')

# 4. 구획 소유 — 양방향·중복
owned = Counter()
for seg in cov['segments']:
    for p in seg['owned_pointers']: owned[p] += 1
    ok(seg['direct_read'] == 'done', 'segment_direct_read', seg['id'])
    ok(seg['machine_extracted'] is True, 'segment_machine', seg['id'])
    ok(os.path.exists(os.path.join(HERE, seg['manual_file'])), 'segment_manual_exists', seg['id'])
    ok(os.path.exists(os.path.join(HERE, seg['review_file'])), 'segment_review_exists', seg['id'])
    ok(set(seg['owned_leaf_pointers']) <= set(seg['owned_pointers']), 'segment_leaf_subset', seg['id'])
    ok(all(p in NODE and NODE[p]['segment'] == seg['id'] for p in seg['owned_pointers']), 'segment_matches_node', seg['id'])
    for r in seg['context_refs']:
        ok(r in NODE and r not in seg['owned_pointers'], 'context_ref_valid_not_owned', f"{seg['id']} {r}")
    ok(seg['last_pointer_read'] == seg['owned_leaf_pointers'][-1], 'segment_last_pointer', seg['id'])
ok(set(owned) == set(truth), 'ownership_union_equals_all', f'missing={sorted(set(truth)-set(owned))[:5]} extra={sorted(set(owned)-set(truth))[:5]}')
ok(all(v == 1 for v in owned.values()), 'ownership_no_duplicates', [p for p, v in owned.items() if v > 1][:5])
ok(all(p in owned for p, (t, v) in truth.items() if (t == 'object' and v == []) or (t == 'array' and v == 0)), 'empty_containers_owned')

# 5. 형태소 적용/제외
ap = {a['pointer']: a for a in mo['applied']}; exc = {x['pointer']: x for x in mo['excluded_values']}
ok(not (set(ap) & set(exc)), 'morph_applied_excluded_disjoint')
ok(set(ap) | set(exc) == {n['pointer'] for n in strings}, 'morph_covers_all_strings')
ok(all(x['reason'] for x in exc.values()), 'morph_exclusion_reason')
for p, a in ap.items():
    ok(p in NODE and a['text'] == NODE[p]['value'], 'morph_text_equals_source', p)
    for t in a['tokens']:
        ok(0 <= t['start'] <= t['end'] <= len(a['text']), 'token_span_range', p)
        ok(t['source_slice'] == a['text'][t['start']:t['end']], 'token_source_slice', p)
        ok(t['surface_match'] == (t['source_slice'] == t['form']), 'token_surface_flag', p)
        ok(t['lemma'] is None or isinstance(t['lemma'], str), 'token_lemma_tool_value', p)
all_keys = sorted({k for n in nodes if n['type'] == 'object' for k in n['keys']})
ok(mo['field_names']['names'] == all_keys, 'field_names_all_recorded')
ok(sorted(f['name'] for f in sm['field_names']) == all_keys, 'field_name_occurrences_recorded')
for f in sm['field_names']:
    ok(all(p in NODE for p in f['pointers']) and len(f['pointers']) == f['occurrences'], 'field_name_pointers', f['name'])
for k in mo['known_errors_rule']:
    a = ap.get(k['pointer']); ok(a is not None, 'known_error_pointer', k['pointer'])
    if a:
        ok(a['text'][k['span'][0]:k['span'][1]] == k['surface'], 'known_error_span', k['pointer'])
        ok([f"{a['tokens'][i]['form']}/{a['tokens'][i]['tag']}" for i in k['token_index']] == k['raw'], 'known_error_tokens', k['pointer'])
for v in mo['tag_variants']['nnp_occurrences']:
    a = ap[v['pointer']]; t = a['tokens'][v['token_index']]
    ok(f"{t['form']}/{t['tag']}" == v['token'] and [t['start'], t['end']] == v['span'], 'tag_variant_occurrence', v['pointer'])

# 6. 표현
E = ex['expressions']
ok(len({x['id'] for x in E}) == len(E), 'expr_id_unique')
ok(max(Counter((x['pointer'], tuple(x['span']), x['source'], tuple(x['kinds'])) for x in E).values()) == 1, 'expr_no_duplicate')
for x in E:
    n = NODE.get(x['pointer'])
    ok(n is not None and n['type'] == 'string', 'expr_pointer_string', x['id'])
    if n: ok(n['value'][x['span'][0]:x['span'][1]] == x['text'] and x['span'][0] < x['span'][1], 'expr_span_text', x['id'])
    ok(x['segment'] == (n['segment'] if n else None), 'expr_segment', x['id'])
whole = {x['pointer'] for x in E if x['source'] == 'value-whole'}
ok(whole == {n['pointer'] for n in strings if n['value'] != ''}, 'expr_value_whole_all')
manual_ptrs = {x['pointer'] for x in E if x['source'] == 'manual'}
ok(manual_ptrs >= {n['pointer'] for n in strings}, 'expr_manual_every_value', sorted({n['pointer'] for n in strings} - manual_ptrs)[:5])
# 자동 후보 독립 재계산
auto_rec = {(x['pointer'], tuple(x['span']), x['source'][5:]) for x in E if x['source'].startswith('auto:')}
auto_re = set()
for pid, pat in ex['method']['patterns'].items():
    rx = re.compile(pat)
    for p, a in ap.items():
        for m in rx.finditer(a['text']):
            if m.end() > m.start(): auto_re.add((p, (m.start(), m.end()), pid))
ok(auto_rec == auto_re, 'auto_candidates_recomputed', f'missing={len(auto_re-auto_rec)} extra={len(auto_rec-auto_re)}')
# 직접 읽기 단서 덮임: 수식·조건·부정·시간·기호 단서의 모든 출현이 manual 구절 안에 있어야 한다
CUES = r'(?<=\s)시(?=[\s,)]|$)|후(?=[\s,)에]|$)|(?<=\s)전(?=[\s,)]|$)|(?<=\s)중(?=[\s~,)]|$)|직후|(?<=\s)내(?=\s)|이상|이하|미만|지속|드묾|흔함|대개|간헐|가능|수 있|우려|시사|고려|필요|필수|주의|금지|금기|문의|연락|즉시|깊|얇|얕|서서히|점차|점진|급격|즉각|조기|지연|만성|영구|안 |없|아닌|아님|미반응|미입증|미흡|미미|불필요|불량|불균일|보다|거의|대부분|상당|일부|모든|가장|최대|최저|약간|경미|심한|심함|심화|뚜렷|미세|가벼운|강한|강함|광범위|과도|과다|비정상|있으면|특히|아직|여전히|오히려|완전|본격|임의|선택|위험|→|~|\+|—|--|\*\*|Day|\d+'
mspans = {}
for x in E:
    if x['source'] == 'manual': mspans.setdefault(x['pointer'], []).append(x['span'])
for p in ap:
    for m in re.finditer(CUES, ap[p]['text']):
        ok(any(a <= m.start() and m.end() <= b for a, b in mspans.get(p, [])), 'cue_covered_by_manual', f'{p} {m.group(0)}@{m.start()}')
for r in ex['residual_tokens']['items']:
    ok(r['covered_manual'], 'residual_token_covered_manual', f"{r['pointer']} {r['token']}")

# 7. 읽기 문서 대조
def md(v): return v.replace('|', '\\|').replace('\n', ' ')
review = open(os.path.join(HERE, 'review.md'), encoding='utf-8').read()
parts = {}
for seg in cov['segments']:
    parts[seg['id']] = open(os.path.join(HERE, seg['review_file']), encoding='utf-8').read()
    ok(f"review-part-{seg['id']}.md" in review, 'review_toc_lists_part', seg['id'])
for n in nodes:
    doc = parts.get(n['segment'], '')
    ok(f"`{n['pointer'] or '(root)'}`" in doc, 'review_part_has_pointer', n['pointer'])
    if n['type'] == 'string':
        ok(f"| {md(n['value'])} |" in doc, 'review_part_has_value', n['pointer'])
for cp in {n['column_path'] or '(root)' for n in nodes}:
    ok(f'| `{cp}` |' in review, 'review_column_table', cp)
for x in E:
    if x['source'] == 'manual':
        ok(f"`{x['pointer']}` | [{x['span'][0]},{x['span'][1]}) |" in parts.get(x['segment'], ''), 'review_part_manual_expr', x['id'])

# 8. 미결 참조 유효
issues_md = open(os.path.join(HERE, 'issues.md'), encoding='utf-8').read()
def ref_ok(r):
    if '*' in r:
        rx = re.compile('^' + re.escape(r).replace('\\*', '[^/]+') + '$')
        return any(rx.match(p) for p in NODE)
    return r in NODE
for fn in sorted(os.listdir(os.path.join(HERE, 'manual'))):
    if not fn.endswith('.txt'): continue
    for line in open(os.path.join(HERE, 'manual', fn), encoding='utf-8'):
        if line.startswith('Q | '):
            seg = fn[:-4]; base = '' if seg == 'S00' else f'/timelines/{int(seg[1:]) - 1}'
            for r in line.split(' | ')[2].split():
                rr = r if r.startswith('/') else base + '/' + r
                ok(ref_ok(rr), 'issue_ref_valid', f'{fn} {rr}')
        elif fn == 'global-issues.txt' and line.strip() and not line.startswith('#'):
            gid, cls, refs, _ = line.split(' | ', 3)
            ok(cls in 'ABCKPFIO' and len(cls) == 1, 'global_issue_class', gid)
            for r in refs.split(): ok(ref_ok(r), 'global_issue_ref_valid', f'{gid} {r}')
            if cls != 'O': ok(gid in issues_md, 'global_issue_in_issues_md', gid)
ok('C 현재 사용자 결정 필요 | 0 |' in issues_md, 'issues_c_zero_recorded')

# 9. 산출물 실재
for f in ['review.md', 'source-map.json', 'morphology.json', 'expressions.json', 'issues.md', 'validation.md', 'coverage.json', 'progress.md', 'build.py']:
    ok(os.path.exists(os.path.join(HERE, f)), 'artifact_exists', f)

sha1 = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()
ok(sha1 == sha0, 'source_sha_end', sha1)
summary = {'source_sha256': sha1, 'pointers': len(truth), 'leaves': len(leaves), 'segments': len(cov['segments']),
           'checks': sum(checks.values()), 'check_kinds': len(checks), 'failure_count': len(fails)}
print(json.dumps(summary, ensure_ascii=False))
for f in fails[:50]: print('FAIL', f)
sys.exit(1 if fails else 0)
