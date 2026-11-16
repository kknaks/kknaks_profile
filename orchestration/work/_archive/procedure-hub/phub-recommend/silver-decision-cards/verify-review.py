import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
D=json.loads((H/'cards.json').read_text());R=json.loads((H/'review.json').read_text());C={c['id']:c for c in D['cards']}
assert len(R['issues'])==26
seen_rows=set();seen_fields=set()
for x in R['issues']:
 assert all(x[k] for k in ['problem','facts','unknown','impact','plan','question','options','rows'])
 assert len({o['id'] for o in x['options']})==len(x['options'])
 for r in x['rows']:
  seen_rows.add(r['id'])
  for f in r['fields']:
   c=C[f['id']];seen_fields.add(f['id'])
   assert f['value']==c['raw_value'] and f['raw_hash']==c['raw_hash']
   assert (f['claim_ref'],f['scope_ref'])==(c['claim_ref'],c['scope_ref'])
 assert x['field_ids']==sorted({f['id'] for r in x['rows'] for f in r['fields']})
assert len(seen_rows)==62 and seen_fields==set(C)
shared=next(x for x in R['issues'] if x['id']=='shared-owner')
assert len(shared['rows'])==5 and len(shared['field_ids'])==17
for r in shared['rows']:
 for t in r['targets']:
  assert any(any(e['id']==r['native_id'] for e in p['matching_ledger_entries']) for p in t['proofs'])
skin=next(x for x in R['issues'] if x['id']=='skin-lineage')
assert all(not p['matching_ledger_entries'] for r in skin['rows'] for t in r['targets'] for p in t['proofs'])
# Highlighted suspicious expressions must actually occur in the selected source fields.
for issue_id,term in [('scope-hyperhidrosis','교근'),('scope-wrinkle','1.5%'),('scope-neck','교근'),('scope-plla','비가교HA')]:
 x=next(x for x in R['issues'] if x['id']==issue_id)
 assert any(term in json.dumps(f['value'],ensure_ascii=False) for r in x['rows'] for f in r['fields'] if f['field'] in x['focus'])
fingerprint=R.pop('review_fingerprint');assert hashlib.sha256(json.dumps(R,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==fingerprint
html=(H/'index.html').read_text();assert fingerprint in html and '/*REVIEW_DATA*/' not in html
# Candidate must remain byte-for-byte unchanged from the prior artifact snapshot.
start=json.loads((H/'results/candidate-start.json').read_text());cand=H.parent/'silver-batch1-candidate'
now={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(cand.rglob('*')) if p.is_file()}
assert now==start,'Candidate changed; do not reuse review decisions'
print('PASS: 26 issue topics; all 62 rows / 152 raw fields preserved; multi-owner evidence and wording anchors verified; candidate unchanged')
