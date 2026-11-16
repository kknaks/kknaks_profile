from pathlib import Path
import ast
p=Path(__file__).with_name('review.py');tree=ast.parse(p.read_text());keep=[]
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)):keep.append(n)
 elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='sys.path.insert':keep.append(n)
 elif isinstance(n,ast.Assign) and {x.id for x in ast.walk(n.targets[0]) if isinstance(x,ast.Name)} & {'R','B','C','M','base'}:keep.append(n)
exec(compile(ast.Module(body=keep,type_ignores=[]),str(p),'exec'))
initial=load(R/'initial-harness-results.json');results=[x for x in initial if x['passed']]
sources={s['id']:s for s in base['source_records']};uid=load(R/'source-direct.json')['unresolved_ids'][0]
for name,code in [('line_reason_loss','PRODUCT_LINE_SOURCE'),('line_unresolved_state_retry','PRODUCT_LINE_UNRESOLVED')]:
 g=copy.deepcopy(base)
 if name=='line_reason_loss':product(g)['line_memberships'][0].pop('reason')
 else:next(m for m in g['mappings'] if m['id']==uid)['state']='exact'
 out,n=materialize('cli-'+name,g);proc=subprocess.run([sys.executable,str(M/'validate.py'),'--candidate',str(out),'--independent-source'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 v=load(out/'validation.json');codes=Counter(d['code'] for d in v['diagnostics']);noise={k:n for k,n in codes.items() if k=='NORMALIZED_ID' or k=='OUTPUT_HASH' or k.startswith('SIDECAR') or k.startswith('EXPORT') or k.startswith('MAPPING_LEDGER')}
 results.append({'name':name,'expected_code':code,'passed':proc.returncode==1 and codes[code]>0 and not noise,'exit_code':proc.returncode,'normalized_ids_remapped':n,'codes':dict(codes),'consistency_noise':noise,'diagnostics':v['diagnostics']});write(R/'full-cli-probes.json',results);print(name,results[-1]['passed'],dict(codes),flush=True)
assert len(results)==12 and all(x['passed'] for x in results)
