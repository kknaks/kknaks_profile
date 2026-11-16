"""게이트 페이지의 유효 상태(미리 체크 + 사용자 답)를 gate-answers/*.json 으로 합친다. 사용자 답 원본은 gate-answers/<이름>/ 아래(ArtifactData 로 내려받음)."""
import json, re, glob, os
W = os.path.dirname(os.path.abspath(__file__))
G = f'{W}/gate-answers'
def load_dir(d):
    out = {}
    for f in glob.glob(f'{d}/**/*.json', recursive=True):
        j = json.load(open(f)); out[j.get('id') or os.path.basename(f)[:-5]] = j.get('data', j)
    return out
# 1) 제품 매칭
h = open(f'{W}/product-match-review.html').read()
D = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', h, re.S).group(1).replace('<\\/', '</'))
ans = load_dir(f'{G}/product-match')
items = []
for p in D['products']:
    a = ans.get(p['id'])
    if a and a.get('decision'):
        st = {'pick': 'approved', 'none': 'no_license', 'na': 'not_applicable'}.get(a['decision'], a['decision']); picks = a.get('picks') or []; src = 'user'
    elif p.get('autoKeys'):
        st, picks, src = 'auto', p['autoKeys'], 'auto'
    elif p['st'] == 'na':
        st, picks, src = 'not_applicable', [], 'auto'
    elif p['st'] == 'unknown':
        st, picks, src = 'unconfirmed', [], 'auto'
    else:
        st, picks, src = 'pending', [], 'none'
    items.append({'ledger_id': p['id'], 'name': p['name'], 'status': st, 'license_keys': picks, 'source': src, 'note': (a or {}).get('note', '')})
news = [{'id': n['id'], 'name': n['name'], 'decision': (ans.get(n['id']) or {}).get('decision'), 'license_keys': (ans.get(n['id']) or {}).get('picks', []), 'note': (ans.get(n['id']) or {}).get('note', '')} for n in D.get('news', [])]
json.dump({'items': items, 'new_devices': news}, open(f'{G}/product-match.json', 'w'), ensure_ascii=False, indent=1)
# 2) 분류표 2차 · 3) 원천 수정
json.dump(load_dir(f'{G}/classify-v2'), open(f'{G}/classify-v2.json', 'w'), ensure_ascii=False, indent=1)
json.dump(load_dir(f'{G}/classify-v1'), open(f'{G}/classify-v1.json', 'w'), ensure_ascii=False, indent=1)
json.dump(load_dir(f'{G}/source-fix'), open(f'{G}/source-fix.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('product-match', dict(Counter(i['status'] for i in items)), 'new', len(news))
