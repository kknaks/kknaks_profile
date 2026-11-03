"""Check coverage locator evidence and capture immutable inputs after review."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
c=json.loads((R/'coverage.json').read_text());cache={};checks=[]
def get(file,ptr):
 if file not in cache:cache[file]=json.loads(Path(file).read_text())
 x=cache[file]
 for bit in ptr.split('/')[1:]:
  k=bit.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
for f in c['fields']:
 assert f['status'] in c['status_definitions']
 for e in f['origin_current_paths']+f['evidence']:
  get(e['file'],e['pointer'])
  checks.append({'field':f['proposed'],'file':e['file'],'pointer':e['pointer'],'exists':True})
 if f['status']=='원문raw보존만':assert f['pilot_typed_path'] is None and f['pilot_raw_preserved_matches']>0
 if f['status']=='pilot검증':assert f['pilot_typed_path'] is not None and f['evidence']
assert sum(x['fields'] for x in c['types'])==247
start=json.loads((R/'results/start.json').read_text());end=[]
for row in start['files']:
 f=Path(row['file']);end.append({'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
changed=[{'before':a,'after':b} for a,b in zip(start['files'],end) if a!=b]
(R/'results/end.json').write_text(json.dumps({'files':end,'count':len(end)},ensure_ascii=False,indent=2)+'\n')
result={'protected_files':len(end),'changed':changed,'all_unchanged':not changed,'start_protected_rows_sha256':hashlib.sha256(json.dumps(start['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'end_protected_rows_sha256':hashlib.sha256(json.dumps(end,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'coverage_locator_checks':len(checks),'coverage_field_count':len(c['fields']),'coverage_type_count':len(c['types']),'coverage_summary':c['summary'],'review_code_hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in (R/'probes').glob('*.py')},'start_manifest_sha256':hashlib.sha256((R/'results/start.json').read_bytes()).hexdigest(),'end_manifest_sha256':hashlib.sha256((R/'results/end.json').read_bytes()).hexdigest()}
(R/'results/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(R/'results/coverage-locators.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False));assert not changed
