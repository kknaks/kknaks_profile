"""Independent artifact/source-set and provenance checks. No migration imports."""
import pathlib,json,hashlib,collections,re
P=pathlib.Path(__file__).resolve().parent; C=P.parent/'silver-batch1-candidate'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def at(d,p):
 for s in p.lstrip('/').split('/') if p else []:
  s=s.replace('~1','/').replace('~0','~');d=d[int(s)] if isinstance(d,list) else d[s]
 return d
D=load(P/'cards.json');R=load(C/'records.json');S=load(C/'safety-claims.json');cards=D['cards'];src={x['id']:x for x in R['source_records']};claims={x['id']:x for x in R['claims']};maps={x['id']:x for x in R['mappings']};scope={x['id']:x for x in R['scopes']};index=load(C/'source-row-index.json');registry={x['id']:x for k in ['products','families','registry'] for x in R[k]};ledger=load(C/'mapping-ledger.json'); identity=load(C/'identity-ledger.json');checks=collections.Counter()
def check(ok,label):
 assert ok,label
 checks[label]+=1
expected={x['claim_ref']:x for x in S['fields'] if x['attachment_state']=='not_created'}
# derive the same denominator from claims/attachments directly, not just safety-claims.
safety_claims={x['id'] for x in R['claims'] if x['predicate'].startswith('safety.') or x['predicate']=='aftercare'}
# operational sources can contain other safety predicates; limit to raw safety field occurrences.
attached={ref for a in R['attachments'] for ref in a['claim_refs']}
check(len(cards)==152 and len({c['id'] for c in cards})==152,'152 unique card IDs')
check({c['claim_ref'] for c in cards}==set(expected),'exact omitted field set')
check(not set(expected)&attached,'no omitted attachment')
check(len(safety_claims)==1394 and safety_claims-attached==set(expected),'records-derived 1394 minus attachments equals omitted set')
check({x['id'] for x in R['claims'] if x['id'] in safety_claims and x['subject_ref'] is None}==set(expected),'records-derived owner-null set')
check(collections.Counter(c['attachment_reason'] for c in cards)=={'candidate_only':49,'out_of_batch_entity':83,'owner_unresolved':20},'reason denominator')
check(len(D['groups'])==62,'62 row groups')
check(collections.Counter(cid for g in D['groups'] for cid in g['card_ids'])==collections.Counter(c['id'] for c in cards),'group field partition')
check(D['meta']['candidate_input_fingerprint']==sha(C/'input-manifest.json') and D['meta']['candidate_output_fingerprint']==sha(C/'output-manifest.json'),'candidate fingerprints')
for entry in load(C/'output-manifest.json')['files']:check(sha(C/entry['file'])==entry['sha256'],'manifest output bytes')
check(D['meta']['p5_status']=='FAIL_미승인_검증기보완중' and D['meta']['p5_review_report_sha256']==sha(P.parent/'silver-batch1-review/report.md'),'P5 FAIL and report hash')
cache={}
for ref,s in D['sources'].items():
 check(s==src[ref],'source record exact')
 p=pathlib.Path(s['file'])
 if str(p) not in cache:check(sha(p)==s['source_sha256'],'source bytes');cache[str(p)]=load(p)
 check(at(cache[str(p)],s['pointer'])==s['raw_value'],'source pointer value')
for c in cards:
 f=expected[c['claim_ref']]
 for k,v in f.items():check(c[k]==v,'safety field exact')
 check(c['claim']==claims[c['claim_ref']] and c['scope']==scope[c['scope_ref']],'claim and scope exact')
 check(c['mappings']==[maps[x] for x in f['mapping_refs']],'mapping exact')
 check(c['mapping_ledger']==[x for x in ledger if x['mapping_ref'] in c['mapping_refs']],'mapping ledger exact')
 check(c['raw_hash']==hashlib.sha256(json.dumps(f['raw_value'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'raw value hash')
 check(c['source_hashes']=={s:src[s]['source_sha256'] for s in c['source_refs']},'raw source hashes')
 allowed={x['target_ref'] for m in c['mappings'] if m['purpose']=='identity' for x in m['candidates'] if x['target_ref'] in registry}
 check({x['id'] for x in c['targets']}==allowed,'candidate target exact set')
 for t in c['targets']:
  check(t['source_refs']==registry[t['id']]['source_refs'],'target provenance')
  for s in t['source_refs']:check(s in D['sources'],'target source embedded')
 for m in c['mappings']:
  for s in m['source_refs']+[s for x in m['candidates'] for s in x['raw_refs']]:check(s in D['sources'],'mapping source embedded')
 for s in c['source_refs']:check(s in D['sources'],'field source embedded')
 g=next(g for g in D['groups'] if g['id']==c['group_id'])
 check(g['row_source_ref']==c['row_source_ref'],'group occurrence')
 ix=next(x for x in index if x['category']=='safety' and c['row_source_ref'] in x['source_refs'])
 check(g['source_index']==ix and c['claim_ref'] in ix['claim_refs'],'source row index exact')
 for v in c['current_values']:
  raw=src[v['source_ref']]['raw_value'].get('source_text',{});check(v['present']==(c['raw_field'] in raw) and v['value']==raw.get(c['raw_field']),'current silver exact')
check(all(x in identity for x in D['identity_ledger']),'identity ledger exact')
html=(P/'index.html').read_text();match=re.search(r'<script>const DATA=(.*?);\nconst \$=',html,re.S)
check(match is not None and json.loads(match[1])==load(P/'review.json'),'issue-first inline data exact')
check('<' not in match[1] and '&' not in match[1],'script end escaping')
check(not re.search(r'(?:https?:)?//[^\s]+\.(?:js|css)|<script[^>]+src=|<link|\bfetch\s*\(|\bimport\s*\(',html),'offline dependencies')
schema=load(P/'decision-schema.json');check(schema['properties']['decisions']['items']['properties']['card_id']['enum']==[c['id'] for c in cards],'schema card IDs')
start=load(P/'results/candidate-start.json');end={p.name:sha(p) for p in sorted(C.rglob('*')) if p.is_file()};check(start==end,'candidate unchanged')
(P/'results/candidate-end.json').write_text(json.dumps(end,indent=2)+'\n')
result={'result':'PASS','checks':sum(checks.values()),'by_check':dict(checks),'fields':152,'groups':62,'source_records_directly_checked':len(D['sources']),'source_files':len(cache),'candidate_unchanged':True,'clinical_approval':0,'decisions_applied':0};(P/'results/data-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
