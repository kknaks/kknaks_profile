from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parent;F=B/'silver-batch1-validator-fix'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,v):(R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
code=[{**r,'matches_current':sha(r['file'])==r['sha256']} for r in load(F/'code-hashes.json')]
reg=load(F/'positive-copy/counterexamples.json')
probes=load(F/'full-cli-probes.json')
cli_files=[]
for row in probes:
 out=F/('cli-'+row['name']);om=load(out/'output-manifest.json')
 cli_files.append({'case':row['name'],'files_match_manifest':all(sha(out/f['file'])==f['sha256'] and (out/f['file']).stat().st_size==f['bytes'] for f in om['files']), 'validation_matches_recorded_codes':sorted({d['code'] for d in load(out/'validation.json')['diagnostics']})==sorted(row['diagnostic_codes'])})
rebuilt=load(F/'rebuilt-comparison.json')
repro=load(B/'silver-batch1-review/reproducibility.json')
prior=load(F/'protected-end.json');prior_matches=[r['file'] for r in prior if not Path(r['file']).is_file() or sha(r['file'])!=r['sha256']]
result={'code_hashes':code,'regression':{'verdict':reg['verdict'],'negative':len(reg['counterexamples']),'positive':len(reg['positive_controls']),'all_passed':all(x['passed'] for x in reg['counterexamples']+reg['positive_controls'])},'fix_full_cli':{'count':len(probes),'all_passed':all(x['passed'] for x in probes),'materialized_evidence':cli_files},'prior_end_drift':prior_matches,'rebuilt_files_byte_equal_now':all((F/'rebuilt'/x['file']).read_bytes()==(B/'silver-batch1-candidate'/x['file']).read_bytes() for x in rebuilt['files']),'prior_repro_hash_matches':sha(B/'silver-batch1-review/reproducibility.json')==rebuilt['prior_reproducibility_sha256'],'prior_repro_verdict':repro['verdict'],'prior_repro_trials':repro['actual_build_trials']}
write('reused-evidence.json',result)
assert all(x['matches_current'] for x in code) and not prior_matches
assert result['regression']['all_passed'] and all(x['files_match_manifest'] and x['validation_matches_recorded_codes'] for x in cli_files)
assert result['rebuilt_files_byte_equal_now'] and result['prior_repro_hash_matches']
print('reused evidence PASS')
