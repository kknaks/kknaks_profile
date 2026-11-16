"""One unchanged-builder reproduction, only the output-location guard redirected locally.
Prior two-build/relocation evidence is retained without rerunning that large suite.
"""
from pathlib import Path
import sys,time
B=Path(__file__).resolve().parent.parent
R=Path(__file__).resolve().parent
M=B/'silver-batch1-migration';sys.path.insert(0,str(M))
from transport import load,write,sha
from validate import evaluate,sidecar_checks
original=M/'build.py';code=original.read_text()
old="permitted=(BASE/'silver-batch1-candidate').resolve()"
new='permitted=Path('+repr(str(R/'rebuilt'))+').resolve()'
assert code.count(old)==1
namespace={'__file__':str(original),'__name__':'fix_reproduction'}
exec(compile(code.replace(old,new),str(original),'exec'),namespace)
namespace['build'](B/'silver-data-contract-batch1/contract-fix/input-manifest.v2.json',B/'silver-data-contract-batch1/field-contract.json',R/'rebuilt')
manifest=load(B/'silver-batch1-candidate/output-manifest.json')
comparison=[{'file':name,'equal':sha(R/'rebuilt'/name)==sha(B/'silver-batch1-candidate'/name)} for name in [r['file'] for r in manifest['files']]+['output-manifest.json']]
r=evaluate(R/'rebuilt');counts,errors=sidecar_checks(R/'rebuilt',load(R/'rebuilt/records.json'))
write(R/'rebuilt-validation.json',r)
write(R/'rebuilt-comparison.json',{'builder_sha256':sha(original),'guard_only_memory_patch':{'old':old,'new':new},'files':comparison,'validator_verdict':r['verdict'],'sidecar_errors':errors,'prior_reproducibility_sha256':sha(B/'silver-batch1-review/reproducibility.json')})
assert all(r['equal'] for r in comparison) and r['verdict']=='PASS' and not errors
print('PASS unchanged builder reproduction, byte-identical outputs, independent validator')
