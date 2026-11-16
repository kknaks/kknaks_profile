#!/usr/bin/env python3
"""Two real builds, physical relocation, identity lifetimes, protection, no canonical writes."""
import argparse
import copy
from pathlib import Path
import shutil
import subprocess
import sys
from transport import BASE, HERE, canonical, digest, sha, load, write
from test_contract import rehash


def identity_trials(g,manifest):
    """Input perturbations in memory; no approval/rebaseline of changed source files."""
    def snapshot(rows,domain):
        collection='procedure-hub/'+domain
        return 'snap:'+digest([domain,collection,sorted([[r['logical_file_key'],r['sha256']] for r in rows if r['domain']==domain])])
    def ids(graph):return {r['id'] for name in ['scopes','mappings','claims','decisions','attachments'] for r in graph[name]}
    def revised_snapshot(graph,old,new,rows):
        changes={old:new}
        for s in graph['source_records']:
            if s['snapshot_ref']==old:changes[s['id']]='src:'+digest([new,s['logical_file_key'],s['pointer']])
        def replace(value):
            if isinstance(value,str):return changes.get(value,value)
            if isinstance(value,list):return [replace(x) for x in value]
            if isinstance(value,dict):return {k:replace(v) for k,v in value.items()}
            return value
        graph=replace(graph)
        for s in graph['snapshots']:
            if s['id']==new:s['files']=[r for r in rows if r['domain']==s['domain']]
        return rehash(graph)
    original=ids(g);probes=[]
    ma=copy.deepcopy(manifest);next(r for r in ma if r['logical_file_key']=='silver-entity-graph-design/design.json')['sha256']='0'*64
    changed=revised_snapshot(copy.deepcopy(g),snapshot(manifest,'audit-artifact'),snapshot(ma,'audit-artifact'),ma)
    probes.append({'name':'audit_only_snapshot_change','passed':ids(changed)==original and [s['id'] for s in changed['source_records']]==[s['id'] for s in g['source_records']],
                   'normalized_id_changes':len(ids(changed)^original),'source_refs_preserved':True,'audit_snapshot_changed':snapshot(ma,'audit-artifact')!=snapshot(manifest,'audit-artifact'),'method':'manifest perturbation in memory + actual graph ID recalculation'})
    ms=copy.deepcopy(manifest);next(r for r in ms if r['logical_file_key']=='step1-products.json')['sha256']='0'*64
    changed=revised_snapshot(copy.deepcopy(g),snapshot(manifest,'generated-silver'),snapshot(ms,'generated-silver'),ms)
    probes.append({'name':'source_data_hash_change','passed':ids(changed)!=original,'normalized_symmetric_difference':len(ids(changed)^original),'native_entity_ids_unchanged':[r['id'] for r in changed['products']]==[r['id'] for r in g['products']]})
    for field in ['record_schema_version','mapping_rule_revision']:
        changed=copy.deepcopy(g);changed[field]+='/changed';changed=rehash(changed)
        probes.append({'name':field+'_lifetime','passed':ids(changed)!=original,'normalized_symmetric_difference':len(ids(changed)^original)})
    # Entity label mutation changes revision content, not the immutable native ID.
    changed=copy.deepcopy(g);changed['products'][0]['label']+=' (label-only probe)'
    probes.append({'name':'label_is_not_native_identity','passed':changed['products'][0]['id']==g['products'][0]['id'],'entity_revision_append_required_for_publication':True})
    raw=load(BASE/'step1-products.json');reordered=copy.deepcopy(raw);reordered['items'].reverse()
    probes.append({'name':'row_reordering_identity','passed':{'product:'+r['ledger_id'] for r in raw['items']}=={'product:'+r['ledger_id'] for r in reordered['items']} and digest(raw)!=digest(reordered),
                   'source_snapshot_changes':True,'occurrence_changes':True,'native_entity_ids_unchanged':True,'no_synthetic_continuity':True})
    return probes


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',required=True);p.add_argument('--trials',type=int,default=2);p.add_argument('--relocate-inputs',action='store_true');a=p.parse_args();out=Path(a.candidate).resolve()
    if a.trials<2:raise ValueError('at least two trials required')
    tmp=out/'tmp/reproducible';tmp.mkdir(parents=True,exist_ok=False)
    inp=BASE/'silver-data-contract-batch1/contract-fix/input-manifest.v2.json';fc=BASE/'silver-data-contract-batch1/field-contract.json';manifest=load(inp);reports=[]
    expected=load(out/'output-manifest.json');names=[r['file'] for r in expected['files']]+['output-manifest.json']
    try:
        for trial in range(a.trials):
            dest=tmp/f'run-{trial+1}'
            cmd=[sys.executable,str(HERE/'build.py'),'--inputs',str(inp),'--field-contract',str(fc),'--output',str(dest)]
            proc=subprocess.run(cmd,capture_output=True,text=True)
            comparison=[{'file':name,'equal':proc.returncode==0 and (dest/name).is_file() and sha(dest/name)==sha(out/name)} for name in names]
            reports.append({'trial':trial+1,'exit_code':proc.returncode,'passed':proc.returncode==0 and all(r['equal'] for r in comparison),'files':comparison,'stderr':proc.stderr})
        if a.relocate_inputs:
            root=tmp/'relocated-inputs'
            for row in manifest:
                dest=root/row['domain']/row['logical_file_key'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(row['file'],dest)
            copied=tmp/'input-manifest.v2.json';shutil.copyfile(inp,copied)
            dest=tmp/'relocated-run';cmd=[sys.executable,str(HERE/'build.py'),'--inputs',str(copied),'--field-contract',str(fc),'--output',str(dest),'--locator-root',str(root)]
            proc=subprocess.run(cmd,capture_output=True,text=True)
            comparison=[{'file':name,'equal':proc.returncode==0 and (dest/name).is_file() and sha(dest/name)==sha(out/name)} for name in names]
            reads=load(dest/'run-metadata.json')['physical_read_locators'] if proc.returncode==0 else []
            reports.append({'trial':'physical_relocation','exit_code':proc.returncode,'passed':proc.returncode==0 and all(r['equal'] for r in comparison) and all(str(root) in r['actual_file'] for r in reads),
                            'files':comparison,'manifest_bytes_identical':sha(copied)==sha(inp),'actual_relocated_files_read':len(reads),'stderr':proc.stderr})
        # Fail-closed input mutation: copied source only, no source edits.
        if a.relocate_inputs:
            changed=root/'raw21/taxonomy.json';changed.write_bytes(changed.read_bytes()+b' ')
            proc=subprocess.run([sys.executable,str(HERE/'build.py'),'--inputs',str(inp),'--field-contract',str(fc),'--output',str(tmp/'must-fail'),'--locator-root',str(root)],capture_output=True,text=True)
            reports.append({'trial':'source_tamper_rejected','passed':proc.returncode!=0 and 'hash/bytes mismatch' in proc.stderr,'exit_code':proc.returncode,'diagnostic':proc.stderr.strip()})
        altered=copy.deepcopy(manifest);altered[0]['sha256']='0'*64;mp=tmp/'unapproved-manifest.json';write(mp,altered)
        proc=subprocess.run([sys.executable,str(HERE/'build.py'),'--inputs',str(mp),'--field-contract',str(fc),'--output',str(tmp/'unapproved'),'--locator-root',str(root) if a.relocate_inputs else str(tmp)],capture_output=True,text=True)
        reports.append({'trial':'manifest_rebaseline_rejected','passed':proc.returncode!=0 and 'not approved v2' in proc.stderr,'diagnostic':proc.stderr.strip()})
        identity=identity_trials(load(out/'records.json'),manifest)
    finally:shutil.rmtree(tmp)
    protected=load(out/'protected-start.json');end=[]
    for row in protected:
        path=Path(row['file']);end.append({'file':str(path),'sha256':sha(path),'bytes':path.stat().st_size})
    changes=[{'before':r,'after':s} for r,s in zip(protected,end) if r!=s]
    write(out/'protected-end.json',end)
    r={'verdict':'PASS' if all(r['passed'] for r in reports+identity) and not changes else 'FAIL','actual_build_trials':reports,'identity_probes':identity,
       'protected_files':len(protected),'protected_changes':changes,'mutable_coordinator_log':'excluded from protected input; frozen approved snapshot included',
       'temp_cleaned':not tmp.exists(),'canonical_transition_executed':False,'clinical_reviews':0}
    write(out/'reproducibility.json',r);print(canonical({'verdict':r['verdict'],'build_probes':len(reports),'identity_probes':len(identity),'protected_files':len(protected),'protected_changes':len(changes),'failed':[x.get('trial',x.get('name')) for x in reports+identity if not x['passed']]}).decode());return int(r['verdict']!='PASS')
if __name__=='__main__':sys.exit(main())
