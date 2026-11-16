"""Well-typed follow-ups to isolate inclusion and conflict semantic checks."""
from pathlib import Path
import ast
p=Path(__file__).with_name('review.py');tree=ast.parse(p.read_text());keep=[]
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)):keep.append(n)
 elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='sys.path.insert':keep.append(n)
 elif isinstance(n,ast.Assign) and {x.id for x in ast.walk(n.targets[0]) if isinstance(x,ast.Name)} & {'R','B','C','M','base'}:keep.append(n)
exec(compile(ast.Module(body=keep,type_ignores=[]),str(p),'exec'))
results=[]
for name,code in [('axis_inclusion_typed','SCOPE_AXIS_SOURCE'),('conflict_typed','SCOPE_CONFLICT_SOURCE')]:
 g=copy.deepcopy(base);s=scope(g)
 if name=='axis_inclusion_typed':s['axes']['product'].update(knowledge='explicit',included=[next(x['id'] for x in g['products'] if x['id'] not in s['axes']['product']['included'])])
 else:s['conflicts'].append({'axis':'site','container':'invented','statement':'invented','source_ref':s['source_refs'][0]})
 out,n=materialize('cli-'+name,g);p2=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 v=load(out/'validation.json');codes=Counter(d['code'] for d in v['diagnostics'])
 ok=p2.returncode==1 and codes[code]>0 and not any(k in {'NORMALIZED_ID','OUTPUT_HASH','STRUCTURAL','EXACT_TYPE'} or k.startswith(('SIDECAR','MAPPING_LEDGER','EXPORT')) for k in codes)
 results.append({'name':name,'passed':ok,'exit_code':p2.returncode,'codes':dict(codes),'diagnostics':v['diagnostics'],'ids_remapped':n});write(R/'refined-probes.json',results);print(name,ok,dict(codes),flush=True)
assert all(x['passed'] for x in results)
