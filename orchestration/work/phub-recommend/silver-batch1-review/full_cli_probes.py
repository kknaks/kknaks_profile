from pathlib import Path
import json,sys,copy,subprocess,hashlib
B=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parent;C=R/'execution-copy';sys.path.insert(0,str(B/'silver-batch1-migration'))
from test_contract import rehash
from transport import load,write,sha
base=load(C/'records.json')
def replace(v,changes):
 if isinstance(v,str):return changes.get(v,v)
 if isinstance(v,list):return [replace(x,changes) for x in v]
 if isinstance(v,dict):return {k:replace(x,changes) for k,x in v.items()}
 return v
results=[]
for name in ['scope_exclusion','line_erasure']:
 out=R/('cli-'+name);out.mkdir(exist_ok=False)
 g=copy.deepcopy(base)
 if name=='scope_exclusion':
  s=next(s for s in g['scopes'] if s['axes']['product']['included']);before=copy.deepcopy(s);owner=s['axes']['product']['included'][0];other=next(p['id'] for p in g['products'] if p['id']!=owner);s['axes']['product']['excluded']=[other];changed={'scope_id':s['id'],'owner':owner,'invented_exclusion':other,'source_refs':s['source_refs']}
 else:
  p=next(p for p in g['products'] if p['line_memberships']);before=copy.deepcopy(p);changed={'product_id':p['id'],'removed_line_memberships':p['line_memberships'],'source_refs':p['source_refs']};p['line_memberships']=[]
 g=rehash(g);changes={a['id']:b['id'] for group in ['scopes','mappings','claims','attachments','decisions'] for a,b in zip(base[group],g[group]) if a['id']!=b['id']}
 # Repoint every derived export to the recomputed graph IDs. This removes stale sidecar noise.
 for f in C.iterdir():
  if not f.is_file():continue
  if f.name=='records.json':write(out/f.name,g)
  elif f.name=='output-manifest.json':continue
  elif f.suffix=='.json':
   v=load(f);v2=replace(v,changes)
   if v2!=v:write(out/f.name,v2)
   else:(out/f.name).symlink_to(f)
  else:(out/f.name).symlink_to(f)
 om=load(C/'output-manifest.json')
 for row in om['files']:
  row['sha256']=sha(out/row['file']);row['bytes']=(out/row['file']).stat().st_size
 write(out/'output-manifest.json',om)
 # validator output must be a local file, not a symlink to execution-copy.
 (out/'validation.json').unlink(missing_ok=True)
 proc=subprocess.run([sys.executable,str(B/'silver-batch1-migration/validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True)
 validation=load(out/'validation.json');results.append({'name':name,'changed':changed,'before':before,'remapped_normalized_ids':len(changes),'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'verdict':validation['verdict'],'failure_count':validation.get('failure_count'),'diagnostics':validation.get('diagnostics')})
 write(R/'full-cli-probes.json',results);print(name,proc.returncode,validation['verdict'],flush=True)
