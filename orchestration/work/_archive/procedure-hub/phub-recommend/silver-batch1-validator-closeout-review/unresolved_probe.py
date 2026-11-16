"""Erase an unresolved line mapping and its ledger row; retain no stale export refs."""
from pathlib import Path
import ast
# Reuse only test serialization/rehashing infrastructure, never an expectation oracle.
p=Path(__file__).with_name('review.py'); tree=ast.parse(p.read_text())
keep=[]
for node in tree.body:
 if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)):keep.append(node)
 elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='sys.path.insert':keep.append(node)
 elif isinstance(node,ast.Assign):
  names={n.id for n in ast.walk(node.targets[0]) if isinstance(n,ast.Name)}
  if names & {'R','B','C','M','base'}:keep.append(node)
exec(compile(ast.Module(body=keep,type_ignores=[]),str(p),'exec'))
# Semicolon assignments in the R statement also initialize B/C/M.
g=copy.deepcopy(base);sources={s['id']:s for s in g['source_records']}
m=next(m for m in g['mappings'] if m['purpose']=='membership' and any(sources[x]['logical_file_key']=='step1-products.json' and sources[x]['pointer'].endswith('/line') for x in m['source_refs']))
removed=m['id'];g['mappings'].remove(m)
# No graph ID changed: deletion alone, remaining normalized payloads identical.
out=R/'cli-line-unresolved-erasure';out.mkdir(exist_ok=False)
for f in C.iterdir():
 if not f.is_file() or f.name in {'validation.json','counterexamples.json','output-manifest.json'}:continue
 if f.name=='records.json':write(out/f.name,g)
 elif f.name=='mapping-ledger.json':write(out/f.name,[x for x in load(f) if x['mapping_ref']!=removed])
 else:(out/f.name).symlink_to(f)
om=load(C/'output-manifest.json')
for x in om['files']:x.update(sha256=sha(out/x['file']),bytes=(out/x['file']).stat().st_size)
write(out/'output-manifest.json',om)
proc=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
v=load(out/'validation.json');codes=Counter(d['code'] for d in v['diagnostics'])
noise={k:n for k,n in codes.items() if k=='NORMALIZED_ID' or k=='OUTPUT_HASH' or k.startswith('SIDECAR') or k.startswith('EXPORT') or k.startswith('MAPPING_LEDGER')}
r={'name':'line_unresolved_erasure','removed_id':removed,'exit_code':proc.returncode,'codes':dict(codes),'noise':noise,'diagnostics':v['diagnostics'],'passed':proc.returncode==1 and codes['PRODUCT_LINE_UNRESOLVED']>0 and not noise}
write(R/'unresolved-erasure.json',r);print(r['passed'],dict(codes));assert r['passed']
