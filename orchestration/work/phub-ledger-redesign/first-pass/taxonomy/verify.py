#!/usr/bin/env python3
"""taxonomy.json 1차 조사 산출물 독립 검증. 읽기만 하고 어떤 파일도 쓰지 않는다.

실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/verify.py
실패가 하나라도 있으면 종료 코드 1.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'orchestration/work/phub-recommend/bronze/phub-ledger/taxonomy.json')
EXPECTED_SHA = '5492d0d4354406477206cb46f1bb735ca684d2d4a218c11d31e7889b20f4e8fe'  # 작업 시작 시 고정한 원본 해시
STATUS = set('ABCKPFI')

fails = []
stats = {}


def fail(msg):
    fails.append(msg)


def esc(k):
    return str(k).replace('~', '~0').replace('/', '~1')


def load(name):
    return json.load(open(os.path.join(HERE, name)))


# ---------------------------------------------------------------- 1. 원본 해시(시작)
raw = open(SRC, 'rb').read()
sha_start = hashlib.sha256(raw).hexdigest()
if sha_start != EXPECTED_SHA:
    fail('원본 해시 불일치(시작): %s' % sha_start)
text = raw.decode('utf-8')

# ---------------------------------------------------------------- 2. 독립 파싱·전수 열거
dups = []


def hook(pairs):
    seen = Counter(k for k, _ in pairs)
    for k, c in seen.items():
        if c > 1:
            dups.append(k)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
truth = {}  # pointer -> (kind, value or len)


def kind_of(v):
    if isinstance(v, dict):
        return 'object'
    if isinstance(v, list):
        return 'array'
    if isinstance(v, bool):
        return 'boolean'
    if v is None:
        return 'null'
    if isinstance(v, str):
        return 'string'
    return 'number'


def walk(v, p):
    truth[p] = (kind_of(v), v if not isinstance(v, (dict, list)) else len(v))
    if isinstance(v, dict):
        for k, c in v.items():
            walk(c, p + '/' + esc(k))
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, p + '/' + str(i))


walk(data, '')
stats['source_nodes'] = len(truth)
stats['source_leaves_or_empty'] = sum(1 for p, (k, v) in truth.items() if k not in ('object', 'array') or v == 0)
stats['duplicate_keys'] = len(dups)
if dups:
    fail('원본 중복 키 %d (source-map 은 #dupN 처리 필요)' % len(dups))

# ---------------------------------------------------------------- 3. source-map 양방향·값·구간
sm = load('source-map.json')
if sm['sha256'] != EXPECTED_SHA:
    fail('source-map sha256 기록 불일치')
smn = {n['pointer']: n for n in sm['nodes']}
if len(smn) != len(sm['nodes']):
    fail('source-map Pointer 중복')
miss = set(truth) - set(smn)
extra = set(smn) - set(truth)
if miss:
    fail('source-map 누락 %d (예: %s)' % (len(miss), sorted(miss)[:3]))
if extra:
    fail('source-map 불필요 %d (예: %s)' % (len(extra), sorted(extra)[:3]))
b2c = {}
ci = bi = 0
for ch in text:
    b2c[bi] = ci
    bi += len(ch.encode('utf-8'))
    ci += 1
b2c[bi] = ci
bad_val = bad_span = 0
for p, (k, v) in truth.items():
    n = smn.get(p)
    if not n:
        continue
    if n['type'] != k:
        bad_val += 1
        continue
    if k in ('object', 'array'):
        if n['child_count'] != v:
            bad_val += 1
    elif n.get('value') != v or (k == 'number' and type(n.get('value')) != type(v)):
        bad_val += 1
    bs, be = n['literal_byte_span']
    lit = raw[bs:be]
    try:
        if k in ('object', 'array'):
            ok = lit[:1] == (b'{' if k == 'object' else b'[') and json.loads(lit.decode('utf-8')) is not None
            ok = ok and kind_of(json.loads(lit.decode('utf-8'))) == k
        else:
            ok = json.loads(lit.decode('utf-8')) == v
    except Exception:
        ok = False
    cs, ce = n['literal_codepoint_span']
    if not ok or text[cs:ce].encode('utf-8') != lit or b2c.get(bs) != cs or b2c.get(be) != ce:
        bad_span += 1
    if 'key_literal_byte_span' in n:
        ks, ke = n['key_literal_byte_span']
        if json.loads(raw[ks:ke].decode('utf-8')) != n['key']:
            bad_span += 1
if bad_val:
    fail('source-map 값/자료형 불일치 %d' % bad_val)
if bad_span:
    fail('source-map 리터럴/코드포인트/키 구간 불일치 %d' % bad_span)
stats['source_map_nodes'] = len(smn)

# ---------------------------------------------------------------- 4. coverage 소유 대조·상태·파일 실재
cov = load('coverage.json')
own = Counter()
sec_of = {}
for s in cov['sections']:
    for p in s['owned_pointers']:
        own[p] += 1
        sec_of[p] = s['id']
    if s['read_state'] != 'read':
        fail('미독 구획 %s' % s['id'])
    for key in ('reading_render', 'manual_record', 'review_file'):
        if not s.get(key) or not os.path.exists(os.path.join(HERE, s[key])):
            fail('%s %s 파일 없음' % (s['id'], key))
    if s.get('manual_record'):
        m = json.load(open(os.path.join(HERE, s['manual_record'])))
        if m.get('state') != 'read' or m.get('section') != s['id']:
            fail('%s manual 상태/구획 불일치' % s['id'])
        if m.get('last_pointer') not in truth:
            fail('%s last_pointer 원문에 없음' % s['id'])
        if m.get('last_pointer') not in set(s['owned_pointers']):
            fail('%s last_pointer 가 구획 소유 범위 밖' % s['id'])
    if s['owned_pointers'][0] != s['pointer_first'] or s['owned_pointers'][-1] != s['pointer_last']:
        fail('%s 범위 경계 기록 불일치' % s['id'])
dup_own = [p for p, c in own.items() if c > 1]
if dup_own:
    fail('구획 중복 소유 %d' % len(dup_own))
if set(own) != set(truth):
    fail('구획 소유 합집합 ≠ 원문 전체 (누락 %d, 불필요 %d)' % (len(set(truth) - set(own)), len(set(own) - set(truth))))
for p, n in smn.items():
    if sec_of.get(p) != n['section']:
        fail('source-map section 표기 불일치 %s' % p)
        break
stats['sections'] = len(cov['sections'])
stats['sections_read'] = sum(1 for s in cov['sections'] if s['read_state'] == 'read')

# ---------------------------------------------------------------- 5. review 문서 대조(분할 포함)
def md(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s.replace('|', '\\|') if s != '' else '`""` (빈 문자열)'


review_missing = 0
for s in cov['sections']:
    body = open(os.path.join(HERE, s['review_file'])).read()
    lines = {}
    value_part = body.split('## 원문 값', 1)[-1].split('## 잠정 관찰', 1)[0]  # 값 표 영역만
    for line in value_part.splitlines():
        m = re.match(r'^\| `([^`]*)` \| ', line)
        if m:
            lines[m.group(1)] = line
    for p in s['owned_pointers']:
        key = p or '(루트)'
        line = lines.get(key)
        if line is None:
            review_missing += 1
            continue
        k, v = truth[p]
        if k not in ('object', 'array') and md(v) not in line:
            review_missing += 1
        if '원본 컬럼명' not in body or '잠정 관찰' not in body:
            review_missing += 1
if review_missing:
    fail('review-part 값/Pointer 누락 %d' % review_missing)
rv = open(os.path.join(HERE, 'review.md')).read()
for s in cov['sections']:
    if s['review_file'] not in rv:
        fail('review.md 목차에 %s 없음' % s['review_file'])
if '컬럼 구성 표' not in rv:
    fail('review.md 컬럼 구성 표 없음')

# ---------------------------------------------------------------- 6. 형태소 적용·제외 대응
mi = load('morphology.json')
strings = {p for p, (k, v) in truth.items() if k == 'string'}
applied = {}
for part in mi['parts']:
    body = open(os.path.join(HERE, part['file']), 'rb').read()
    if hashlib.sha256(body).hexdigest() != part['sha256']:
        fail('형태소 파트 해시 불일치 %s' % part['file'])
    d = json.loads(body)
    for rec in d['records']:
        if rec['pointer'] in applied:
            fail('형태소 중복 레코드 %s' % rec['pointer'])
        applied[rec['pointer']] = rec
        if sec_of.get(rec['pointer']) != d['section']:
            fail('형태소 레코드 구획 불일치 %s' % rec['pointer'])
excluded = {e['pointer']: e for e in mi['excluded']}
both = set(applied) & set(excluded)
if both:
    fail('형태소 적용·제외 중복 %d' % len(both))
none = strings - set(applied) - set(excluded)
if none:
    fail('형태소 미처리 문자열 %d' % len(none))
if (set(applied) | set(excluded)) - strings:
    fail('형태소 대상이 문자열 값이 아님')
for p, e in excluded.items():
    if not e.get('reason') or e['value'] != truth[p][1]:
        fail('제외 사유/값 누락 %s' % p)
        break
bad_tok = 0
ntok = 0
zero_len = 0
for p, rec in applied.items():
    v = truth[p][1]
    if rec['text'] != v:
        bad_tok += 1
        continue
    for t in rec['tokens']:
        ntok += 1
        form, tag, st, en, surf, lemma = t
        if not (0 <= st <= en <= len(v)) or v[st:en] != surf or not tag:
            bad_tok += 1
        if st == en:
            zero_len += 1
if bad_tok:
    fail('형태소 토큰 구간/표면형 불일치 %d' % bad_tok)
if ntok != mi['token_count'] or len(applied) != mi['applied_count'] or len(excluded) != mi['excluded_count']:
    fail('형태소 집계 기록 불일치')
key_ptrs = defaultdict(list)
for p, n in smn.items():
    if n['key'] is not None:
        key_ptrs[n['key']].append(p)
fn = {f['field_name']: f for f in mi['field_names']}
if set(fn) != set(key_ptrs):
    fail('필드명 분석 대상 불일치')
for k, f in fn.items():
    if sorted(f['occurrences']) != sorted(key_ptrs.get(k, [])):
        fail('필드명 출현 위치 불일치 %s' % k)
    for t in f['tokens']:
        if k[t[2]:t[3]] != t[4]:
            fail('필드명 토큰 구간 불일치 %s' % k)
for f in mi['known_segmentation_errors']:
    v = truth.get(f['pointer'], (None, None))[1]
    if not isinstance(v, str) or v[f['span'][0]:f['span'][1]] != f['surface'] or f['status'] != 'K':
        fail('알려진 오분절 구간 불일치 %s' % f['pointer'])
        break
stats.update({'zero_length_tokens': zero_len, 'morph_applied': len(applied), 'morph_excluded': len(excluded), 'tokens': ntok,
              'field_names': len(fn), 'known_seg_flags': len(mi['known_segmentation_errors'])})

# ---------------------------------------------------------------- 7. 표현 구간
ex = load('expressions.json')
seen = set()
bad_ex = 0
for a in ex['auto']:
    v = truth.get(a['pointer'], (None, None))[1]
    s0, e0 = a['span']
    ss, se = a['sentence_span']
    if not isinstance(v, str) or v[s0:e0] != a['text'] or v[ss:se] != a['sentence'] or not (ss <= s0 < se):
        bad_ex += 1
    key = (a['pointer'], s0, e0, a['category_hint'])
    if key in seen:
        bad_ex += 1
    seen.add(key)
    if sec_of.get(a['pointer']) != a['section']:
        bad_ex += 1
for m in ex['manual']:
    v = truth.get(m['pointer'], (None, None))[1]
    if not m['span'] or not isinstance(v, str) or v[m['span'][0]:m['span'][1]] != m['text']:
        bad_ex += 1
    if m['status'] not in STATUS:
        bad_ex += 1
if bad_ex:
    fail('표현 구간/중복/구획 불일치 %d' % bad_ex)
if ex['auto_count'] != len(ex['auto']) or ex['manual_count'] != len(ex['manual']):
    fail('표현 집계 기록 불일치')
stats.update({'expr_auto': len(ex['auto']), 'expr_manual': len(ex['manual'])})

# ---------------------------------------------------------------- 8. 수동 기록 무결성
mdir = os.path.join(HERE, 'manual')
status_cnt = Counter()
ids = Counter()
for fnm in sorted(os.listdir(mdir)):
    m = json.load(open(os.path.join(mdir, fnm)))
    for o in m.get('observations', []):
        if o.get('status', 'P') not in STATUS:
            fail('관찰 상태 문자 오류 %s' % fnm)
        for p in o.get('pointers', []):
            if p not in truth:
                fail('관찰 Pointer 원문에 없음 %s %s' % (fnm, p))
    for x in m.get('issues', []):
        if x['status'] not in STATUS:
            fail('미결 상태 문자 오류 %s' % x['id'])
        status_cnt[x['status']] += 1
        ids[x['id']] += 1
        for p in x['pointers']:
            if p not in truth:
                fail('미결 Pointer 원문에 없음 %s %s' % (x['id'], p))
    for e in m.get('seg_errors', []):
        if e.get('scope') == 'pointer' and e.get('pointer') not in truth:
            fail('오분절 Pointer 원문에 없음 %s' % fnm)
dup_ids = [i for i, c in ids.items() if c > 1]
if dup_ids:
    fail('미결 ID 중복 %s' % dup_ids)
stats['issues_by_status'] = dict(sorted(status_cnt.items()))

# ---------------------------------------------------------------- 9. 원본 해시(끝)
sha_end = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()
if sha_end != sha_start:
    fail('원본 해시가 검증 중 바뀜')
stats['sha_start'] = sha_start
stats['sha_end'] = sha_end

stats['failure_count'] = len(fails)
print(json.dumps(stats, ensure_ascii=False, indent=1))
for f in fails[:50]:
    print('FAIL:', f)
sys.exit(1 if fails else 0)
