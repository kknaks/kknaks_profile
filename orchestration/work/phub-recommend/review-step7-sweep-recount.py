"""검수 review-step7-sweep 의 이상함 · 확인 필요 항목을 지금 step7-concerns.json 에 다시 대 보고 원인이 남았는지 셈"""
import json, sys, collections
W = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else W
r = json.load(open(f'{W}/review-step7-sweep.json'))
d = json.load(open(f'{OUT}/step7-concerns.json'))
U = {u['id']: u for u in json.load(open(f'{W}/step5-units.json'))['units']}
s3 = json.load(open(f'{W}/step3-sites.json')); P = {n['name']: n['parent'] for n in s3['nodes']}
def reg(s):
    if s not in P: return None
    while P[s]: s = P[s]
    return s
def parts(c):
    for x in (c.get('components') or []) + (c.get('members') or []) + (c.get('upgrade') or []): yield x
    for m in c.get('schedule') or []: yield from m['items']
CB = {c['id']: c for c in d['combos']}
def find(it):
    k = it['key'].split(':')
    if it['kind'] == '엣지':
        cand = [e for e in d['edges'] if e['source'] == it['source'] and any(it['key'] == f"E:{e['from']}:{x}" for x in (e.get('source_ids') or [e['source_id']]))]
        cand = [e for e in cand if e['to_family'] == it['to_family']] or cand
        return cand, [(e['to_units'], e['lowering']) for e in cand]
    c = CB.get(k[1]); ps = list(parts(c)); x = ps[int(k[2])]
    return [x], [(x['units'], x.get('status') or '')]
def words_of(it):
    return ' '.join(it['concerns'])
still = collections.Counter(); left = []
for it in r['items']:
    if it['verdict'] == '정상': continue
    objs, got = find(it)
    if not objs:
        left.append((it['key'], 'NOT FOUND')); continue
    rem = []
    for c in it['causes']:
        cc = c['cause']
        for units, st in got:
            bad = False
            if cc in ('C1', 'C2'):
                fam = {U[u]['key']['family'] for u in units}
                bad = len(units) > 1 and any(U[u]['purposes'] and not any(p in words_of(it) for p in U[u]['purposes']) for u in units)
            elif cc == 'C3': bad = any(reg(U[u]['key']['site']) == '두피' for u in units)
            elif cc == 'C3b': bad = 'U5-111' in units
            elif cc == 'C5': bad = any(U[u]['key']['family'] == 'M2' for u in units)
            elif cc == 'C5b': bad = '후보 여럿' not in st
            elif cc == 'C6': bad = any(reg(U[u]['key']['site']) != '바디' and U[u]['key']['site'] not in ('해당 없음', '병변 단위') for u in units)
            elif cc == 'C7': bad = len(units) > 1 and '후보 전부' in st and '이름' not in st
            elif cc == 'C8': bad = units != ['U5-141']
            elif cc == 'C9': bad = 'U5-138' not in units
            if bad: rem.append((cc, c['level'])); break
    if rem:
        lv = '이상함' if any(l == '이상함' for _, l in rem) else '확인 필요'
        still[lv] += 1; left.append((it['key'], it['verdict'], '→', lv, rem, [U[u]['name'] for u in got[0][0]][:6]))
before = collections.Counter(i['verdict'] for i in r['items'])
print(json.dumps({'이상함': [before['이상함'], still['이상함']], '확인 필요': [before['확인 필요'], still['확인 필요']]}, ensure_ascii=False))
for x in left: print(x)
