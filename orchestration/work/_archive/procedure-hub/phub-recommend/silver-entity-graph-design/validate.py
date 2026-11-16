"""Artifact/source checks only; no source mutation, generators, network or packages."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib,subprocess
O=Path(__file__).resolve().parent;J=lambda p:json.loads(Path(p).read_text());d=J(O/'design.json');checks=[]
def check(name,ok,**detail):checks.append({'check':name,'pass':bool(ok),**detail})
def at(file,path):
 v=J(file)
 assert path.startswith('$')
 for dot,b in re.findall(r'\.([^\.\[\]]+)|\[(\d+|\x27[^\x27]*\x27|"[^"]*")\]',path[1:]):v=v[dot if dot else int(b) if b.isdigit() else b[1:-1]]
 return v
for m in d['source_manifest']:
 p=Path(m['file']);check('source_hash_unchanged',p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],file=str(p))
for group in ['types','nodes','edges','cases','evidence','current_records']:
 xs=d[group];check('unique_'+group,len(xs)==len({x['id'] for x in xs}),count=len(xs))
types={t['id'] for t in d['types']};evs={e['id'] for e in d['evidence']}
keys={'name','type','required','default','empty_unknown','meaning','ref','normalization','locator','invariant','evidence'}
for t in d['types']:
 check('type_full_contract',all(k in t for k in ['purpose','storage','identity','lifecycle','legacy','source_path','gold_node','evidence']),type=t['id'])
 check('field_names_unique',len(t['fields'])==len({f['name'] for f in t['fields']}),type=t['id'])
 for f in t['fields']:
  check('field_contract',keys<=f.keys() and all(f[k] for k in ['name','type','meaning','default','empty_unknown','normalization','locator','invariant']),type=t['id'],field=f['name'])
  check('field_ref',not f['ref'] or f['ref'] in types,type=t['id'],field=f['name'])
for group in ['types','nodes','edges','cases','current_records']:
 for x in d[group]:check('evidence_refs',bool(x['evidence']) and set(x['evidence'])<=evs,group=group,id=x['id'])
for e in d['edges']:
 check('edge_endpoint_types',set(e['from_types']+e['to_types'])<=types,edge=e['id'])
 check('edge_contract',all(k in e and e[k] is not None for k in ['directed','cardinality','inverse_meaning','action','parallel_edges','uniqueness_key','required_attributes','source_claim_refs','scope','certainty','derivation','attachment','forbidden','example']),edge=e['id'])
 check('nonempty_edge_contract',all(e[k] for k in ['cardinality','inverse_meaning','required_attributes','source_claim_refs','scope','certainty','forbidden','example']),edge=e['id'])
sem=J(O.parent/'semantic.json')
check('all_current_stored_edges_mapped',{e['kind'] for e in sem['edge_kinds']}<={e['id'] for e in d['edges']})
check('all_node_kinds_mapped',{n['kind'] for n in sem['node_kinds']}=={n['id'] for n in d['nodes']})
check('migration_full_scalar_paths',len(d['migration'])==len(d['current_fields']) and {(x['stage'],x['path']) for x in d['migration']}=={(x['stage'],x['path']) for x in d['current_fields']})
# Compare every referenced original/silver value independently to the prior audit evidence.
issues=J(O.parent/'silver-origin-structure-audit/issues.json')['issues']
for i in issues:
 refs=(i['origin'] if isinstance(i['origin'],list) else [i['origin']])+[i['silver']]
 for r in refs:
  try:check('case_source_value',at(r['file'],r['jsonpath'])==r['value'],case=i['id'],locator=r['jsonpath'])
  except Exception as ex:check('case_source_value',False,case=i['id'],error=str(ex))
for e in d['evidence']:
 p=Path(e['file']);check('evidence_file_exists',p.is_file(),id=e['id'])
 if e['locator'].startswith('$'):
  try:at(p,e['locator']);check('evidence_locator_resolves',True,id=e['id'])
  except Exception as ex:check('evidence_locator_resolves',False,id=e['id'],error=str(ex))
 if e.get('lines'):check('evidence_lines_in_range',min(e['lines'])>=1 and max(e['lines'])<=len(p.read_text().splitlines()),id=e['id'])
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.hrefs=[];self.remote=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.hrefs.append(a['href'])
  if tag in ['script','link','iframe','img','source'] and any(a.get(k,'').startswith(('http:','https:','//')) for k in ['src','href']):self.remote.append(a)
h=(O/'index.html').read_text();parser=Parser();parser.feed(h)
check('static_ids_unique',len(parser.ids)==len(set(parser.ids)))
inline=re.search(r'<script id="design-data" type="application/json">(.*?)</script>',h,re.S).group(1)
check('inline_data_identical',json.loads(inline)==d)
check('inline_json_termination_escaped','<' not in inline)
check('offline_no_remote_assets',not parser.remote and not re.search(r'\b(fetch\(|import\s|XMLHttpRequest|@import|https?://[^\s]+\.(?:js|css))',h))
for href in parser.hrefs:
 if href.startswith('#'):check('static_anchor_resolves',href[1:] in parser.ids,href=href)
 elif href!='validation.json' and not href.startswith(('file:','http:','https:')):check('local_artifact_link_exists',(O/href).is_file(),href=href)
js=re.findall(r'<script>(.*?)</script>',h,re.S)[0];tmp=O/'.syntax-check.js';tmp.write_text(js)
try:
 r=subprocess.run(['node','--check',str(tmp)],capture_output=True,text=True);check('javascript_syntax',r.returncode==0,error=r.stderr)
finally:tmp.unlink()
check('known_case_denominators',sum(c['group']=='singleton-pair-label' for c in d['cases'])==21 and sum(c['group']=='note-claim-lineage' for c in d['cases'])==7 and sum(c['group']=='normalize-overwrite' for c in d['cases'])==3 and sum(c['group']=='duplicate-cc-first-match' for c in d['cases'])==2)
result={'scope':'설계 artifact·출처·구조 검증. 임상 정확성/활성 DB/허가 최신성 검증 아님','passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks}
previous=O/'validation.json'
if previous.exists() and J(previous).get('browser'):result['browser']=J(previous)['browser']
(O/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failures':[c for c in checks if not c['pass']]},ensure_ascii=False));raise SystemExit(bool(result['failed']))
