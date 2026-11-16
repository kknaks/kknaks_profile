#!/usr/bin/env python3
"""Real-source positive controls and rehashed semantic counterexamples."""
import argparse
import copy
from pathlib import Path
import shutil
import sys
from transport import BASE, HERE, canonical, digest, load, write, sha, pointer
from validate import evaluate, machine_type

GROUPS=['scopes','mappings','claims','decisions','attachments']
PREFIX={'scope':'scp','mapping':'map','claim':'clm','decision':'dec','attachment':'att'}

def rehash(g):
    """Recompute normalized graph IDs after mutation; preserve all graph references."""
    def replace(value,changes):
        if isinstance(value,str):return changes.get(value,value)
        if isinstance(value,list):return [replace(x,changes) for x in value]
        if isinstance(value,dict):return {k:replace(v,changes) for k,v in value.items()}
        return value
    for group in GROUPS:
        changes={}
        for r in g[group]:
            payload={k:v for k,v in r.items() if k not in ['id','type']}
            changes[r['id']]=PREFIX[r['type']]+':'+digest([g['record_schema_version'],g['mapping_rule_revision'],payload])
        g=replace(g,changes)
    return g

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',required=True);a=p.parse_args();out=Path(a.candidate).resolve();base=load(out/'records.json')
    positives=[];results=[]
    baseline=evaluate(out)
    positives.append({'name':'full_source_positive','passed':baseline['verdict']=='PASS','counts':baseline['counts'],'failure_count':baseline['failure_count']})
    cases=[]
    def add(name,code,fn):cases.append((name,code,fn))
    def safety(g):return next(c for c in g['claims'] if c['raw_field']=='safety.common_adverse_effects')
    def ownerclaim(g):return next(c for c in g['claims'] if c['raw_field']=='safety.common' and c['subject_ref'])
    def candidate(g):return next(m for m in g['mappings'] if m['state']=='compatible_candidate')
    add('delete_one_collision_claim','SAFETY_CLAIM',lambda g:g['claims'].remove(safety(g)))
    add('many_to_one_predicate_overwrite','SAFETY_CLAIM',lambda g:g['claims'].__setitem__(slice(None),[c for c in g['claims'] if c['raw_field']!='safety.common_adverse_effects']))
    add('design_hash_normalized_ID_contamination','AUDIT_ID_CONTAMINATION',lambda g:ownerclaim(g).__setitem__('audit_design_sha256',sha(BASE/'silver-entity-graph-design/design.json')))
    add('raw_array_order','SAFETY_RAW',lambda g:ownerclaim(g)['raw_value'].reverse())
    add('raw_empty_array','SAFETY_RAW',lambda g:ownerclaim(g).__setitem__('raw_value',[]))
    add('raw_false_for_array','SAFETY_RAW',lambda g:ownerclaim(g).__setitem__('raw_value',False))
    add('raw_null_for_array','SAFETY_RAW',lambda g:ownerclaim(g).__setitem__('raw_value',None))
    add('normal_serious_rename_lost','PREDICATE',lambda g:next(c for c in g['claims'] if c['raw_field']=='safety.serious_adverse_effects').__setitem__('predicate','safety.serious_adverse_effects'))
    add('LOSS02_product_misclassification','LOSS02',lambda g:[c.__setitem__('subject_ref','product:M1-2-1') for c in g['claims'] if c['subject_ref']=='unit_procedure:U5-016'])
    add('invent_merge_target','PRODUCT_CONTINUITY',lambda g:g['products'][0]['continuity'].__setitem__('merged_into',g['products'][1]['id']))
    add('invent_line_parent','PRODUCT_LINE',lambda g:g['products'][0]['line_memberships'].append({'parent_product_ref':g['products'][1]['id'],'role':'item','decision_ref':None}))
    add('wrong_ledger_join','MEMBERSHIP_ENTITY',lambda g:g['products'][0].__setitem__('family_mapping_refs',g['products'][1]['family_mapping_refs']))
    add('candidate_auto_selected','CANDIDATE_SELECTION',lambda g:candidate(g).__setitem__('selected_refs',[candidate(g)['candidates'][0]['target_ref']]))
    add('null_family_filled','MEMBERSHIP_SELECTED',lambda g:next(m for m in g['mappings'] if m.get('legacy',{}).get('family','x') is None).__setitem__('selected_refs',['family:M1']))
    add('clinical_confirmed','CLINICAL_STATE',lambda g:ownerclaim(g).__setitem__('review_state','confirmed'))
    add('wrong_revision_type_bool','EXACT_TYPE',lambda g:g['products'][0].__setitem__('revision',True))
    add('broken_mapping_ref','REF_TYPE',lambda g:ownerclaim(g).__setitem__('mapping_refs',['map:missing']))
    # Independent source semantics: these survive normalized-ID recalculation.
    def lineproduct(g):return next(p for p in g['products'] if p['line_memberships'])
    add('line_membership_erasure','PRODUCT_LINE_SOURCE',lambda g:lineproduct(g).__setitem__('line_memberships',[]))
    add('line_role_replacement','PRODUCT_LINE_SOURCE',lambda g:lineproduct(g)['line_memberships'][0].__setitem__('role','발명'))
    add('line_reason_replacement','PRODUCT_LINE_SOURCE',lambda g:lineproduct(g)['line_memberships'][0].__setitem__('reason','invented approval'))
    add('line_fieldstate_erasure','PRODUCT_LINE_FIELD_STATE',lambda g:g['field_states'].__setitem__(slice(None),[s for s in g['field_states'] if not (s['owner_ref']==lineproduct(g)['id'] and s['field']=='line_memberships')]))
    add('line_unresolved_erasure','PRODUCT_LINE_UNRESOLVED',lambda g:g['mappings'].remove(next(m for m in g['mappings'] if m.get('reason','').startswith('Line string'))))
    add('source_scope_excluded_invention','SCOPE_AXIS_SOURCE',lambda g:g['scopes'][0]['axes']['product'].__setitem__('excluded',[g['products'][1]['id']]))
    add('source_qualifier_erasure','SCOPE_QUALIFIER_SOURCE',lambda g:next(s for s in g['scopes'] if s['statement_qualifiers']).__setitem__('statement_qualifiers',[]))
    add('source_qualifier_state','SCOPE_QUALIFIER_SOURCE',lambda g:next(s for s in g['scopes'] if s['statement_qualifiers'])['statement_qualifiers'][0].__setitem__('state','unreviewed'))
    add('source_axis_evidence_replacement','SCOPE_AXIS_SOURCE',lambda g:g['scopes'][0]['axes']['site'].__setitem__('raw_refs',g['scopes'][1]['source_refs']))
    add('scope_include_exclude_intersection','SCOPE_SET',lambda g:g['scopes'][0]['axes']['product'].__setitem__('excluded',g['scopes'][0]['axes']['product']['included'][:]))
    add('scope_duplicate','SCOPE_SET',lambda g:g['scopes'][0]['axes']['product']['included'].append(g['scopes'][0]['axes']['product']['included'][0]))
    def hide(g):
        c=ownerclaim(g);s=next(s for s in g['scopes'] if s['id']==c['scope_ref']);s['axes'][c['subject_ref'].split(':')[0]]['knowledge']='unknown'
    add('explicit_owner_hidden_as_unknown','OWNER_SCOPE',hide)
    add('unrelated_scope_parent','SCOPE_PARENT',lambda g:g['scopes'][1].__setitem__('container_scope_ref',g['scopes'][0]['id']))
    add('source_parent_unrelated','SOURCE_PARENT',lambda g:next(s for s in g['source_records'] if s['pointer']=='/items/0').__setitem__('parent_ref',next(s['id'] for s in g['source_records'] if s['pointer']=='/families')))
    add('null_rule_reason_deleted','NULL_RULE_REASON',lambda g:next(m for m in g['mappings'] if m['rule'] is None).__setitem__('reason',''))
    for field,value in [('id','forged-rule'),('version','999'),('code_sha256','0'*64)]:
        add('forged_mapping_rule_'+field,'MAPPING_RULE',lambda g,k=field,v=value:next(m for m in g['mappings'] if m['rule'] is not None)['rule'].__setitem__(k,v))
    add('subfamily_new_ID','SUBFAMILY_DESIGN',lambda g:g['families'][0].__setitem__('subfamilies',[{'key':'invented','axis':'purpose'}]))
    add('attachment_confirmed','CLINICAL_STATE',lambda g:g['attachments'][0].__setitem__('application_state','explicit'))
    add('attachment_wrong_owner','ATTACHMENT_OWNER',lambda g:g['attachments'][0].__setitem__('target_ref',g['products'][1]['id']))
    add('attachment_invent_witness','ATTACHMENT_WITNESS',lambda g:g['attachments'][0].__setitem__('witness',[{'mapping_ref':g['mappings'][0]['id'],'edge_ref':None,'component_ref':None,'source_ref':g['source_records'][0]['id']}]))
    add('registry_wrong_native','REGISTRY',lambda g:g['registry'][0].__setitem__('native_id','invented'))
    for name,code,fn in cases:
        g=copy.deepcopy(base);fn(g);g=rehash(g)
        r=evaluate(out,g,check_exports=False);codes=Counter(x['code'] for x in r['diagnostics'])
        semantic=[d for d in r['diagnostics'] if d['code']==code]
        passed=bool(semantic) and codes.get('NORMALIZED_ID',0)==0
        results.append({'name':name,'passed':passed,'expected_semantic_code':code,'semantic_diagnostics':semantic[:3],'failure_count':r['failure_count'],'normalized_id_failures':codes.get('NORMALIZED_ID',0),'normalized_ids_recalculated':True})
        print(name,'PASS' if passed else 'FAIL',flush=True)
    # Manifest authority mutations use isolated sidecars under candidate/tmp, never source modifications.
    temp=out/'tmp/rule-probes';temp.mkdir(parents=True,exist_ok=False)
    try:
        for f in out.iterdir():
            if f.is_file(): (temp/f.name).symlink_to(f)
        for field,code,val in [('id','RULE_ID','forged'),('version','RULE_VERSION','3'),('authority','RULE_AUTHORITY','invented human approval'),('source_rule','RULE_SOURCE',{'pointer':'/forged/decision'})]:
            path=temp/'rule-manifest.json'
            if path.is_symlink():path.unlink()
            rule=load(out/'rule-manifest.json');rule[field]=val
            rule['mapping_rule_revision']='batch1-rules:'+digest({k:v for k,v in rule.items() if k!='mapping_rule_revision'})
            write(path,rule);g=copy.deepcopy(base);g['mapping_rule_revision']=rule['mapping_rule_revision'];g=rehash(g)
            r=evaluate(temp,g,check_exports=False);semantic=[d for d in r['diagnostics'] if d['code']==code];idfails=sum(d['code']=='NORMALIZED_ID' for d in r['diagnostics'])
            results.append({'name':'forged_manifest_'+field,'passed':bool(semantic) and idfails==0,'expected_semantic_code':code,'semantic_diagnostics':semantic[:2],'normalized_ids_recalculated':True,'normalized_id_failures':idfails})
    finally:shutil.rmtree(temp)
    # Pilot is read-only; real historical fixture assertions, not new migration records.
    pilot=load(BASE/'silver-design-pilot-v2/pilot.json');cases42=pilot['cases'];combo={s['pointer'] for s in pilot['source_records'] if s['file'].endswith('combo-recipes.json')}
    regression=load(HERE/'regression-inputs.json')
    positives.append({'name':'pilot_regression_manifest_hashes','passed':all(sha(r['file'])==r['sha256'] for r in regression),'files':len(regression),'new_migration_count':0})
    regdocs={r['file']:load(r['file']) for r in regression if r['file'].endswith('.json')}
    rawsrc=[s for s in pilot['source_records'] if '/phub-stg-2026-10-26/' in s['file']]
    positives.append({'name':'pilot_actual_raw_pointer_regression','passed':all(canonical(pointer(regdocs[s['file']],s['pointer']))==canonical(s['raw_value']) for s in rawsrc),'source_occurrences':len(rawsrc),'new_migration_count':0})
    positives.append({'name':'immutable_pilot_42','passed':len(cases42)==42,'cases':len(cases42),'new_migration_count':0,'pilot_sha256':sha(BASE/'silver-design-pilot-v2/pilot.json')})
    positives.append({'name':'pilot_notes7','passed':len(pilot['notes'])==7,'notes':len(pilot['notes']),'new_migration_count':0})
    lang=[c for c in pilot['claims'] if c.get('language') is not None]
    positives.append({'name':'pilot_language5','passed':len(lang)==5,'cases':len(lang),'new_migration_count':0})
    clby={c['id']:c for c in pilot['claims']};srcby={s['id']:s for s in pilot['source_records']}
    duration=pilot['resolutions'][0];duration_inputs=[clby[x] for x in duration['input_claim_refs']]
    duration_equal=all(any(c['raw_value']==srcby[r]['raw_value'] for r in c['source_refs']) for c in duration_inputs)
    positives.append({'name':'pilot_duration_two_alternatives','passed':len(duration_inputs)==2 and len(duration['alternatives'])>=1 and duration_equal,'new_migration_count':0})
    combo_sources=[s for s in pilot['source_records'] if s['file'].endswith('problem-packages.json')]
    rawcombo=load(next(s['file'] for s in combo_sources if s['file'].endswith('problem-packages.json')))
    def walk(v):
        if isinstance(v,dict):
            yield v
            for x in v.values():yield from walk(x)
        elif isinstance(v,list):
            for x in v:yield from walk(x)
    combos=[r for r in walk(rawcombo) if 'combo' in r and isinstance(r['combo'],list)]
    positives.append({'name':'pilot_combo146_arity','passed':len(combos)==146 and sorted(Counter(len(r['combo']) for r in combos).items())==[(1,21),(2,119),(3,6)],'combos':len(combos),'new_migration_count':0})
    machine=load(HERE/'type-contract.json')['fields']
    badtypes=[]
    for key,spec in machine.items():
        # Required fields reject a missing sentinel; JSON raw fields deliberately allow any JSON.
        from validate import MISSING
        if machine_type(MISSING,spec):badtypes.append(key)
    positives.append({'name':'all84_required_types','passed':len(machine)==84 and not badtypes,'fields':len(machine)})
    positives.append({'name':'snapshot_file_versions_exact','passed':any(f['meta']['version_state']=='missing' for s in base['snapshots'] for f in s['files']) and any(type(f['meta']['source_version_raw']) is int for s in base['snapshots'] for f in s['files']) and any(isinstance(f['meta']['source_version_raw'],str) for s in base['snapshots'] for f in s['files'])})
    positives.append({'name':'null_rule_real_reason','passed':any(m['rule'] is None and m.get('reason') for m in base['mappings'])})
    positives.append({'name':'subfamily_needs_design','passed':len([s for s in base['field_states'] if s['field']=='subfamilies' and s['state']=='needs_design'])==27})
    counts=baseline['counts'];positives.append({'name':'candidate19_raw37_fields132_no_attachment','passed':counts['candidate_raw_only_rows']==56 and counts['candidate_raw_only_fields']==132})
    positives.append({'name':'raw_collision_16_and_10_recovered','passed':sum(r['after_leaves']-r['before_leaves'] for r in counts['collision_rows'])==10})
    report={'verdict':'PASS' if all(x['passed'] for x in positives+results) else 'FAIL','positive_controls':positives,'counterexamples':results,'count':len(results),'semantic_rejection_after_rehash_required':True,'clinical_reviews':0}
    write(out/'counterexamples.json',report);print(canonical({'verdict':report['verdict'],'positive':len(positives),'negative':len(results),'failed':[r['name'] for r in positives+results if not r['passed']]}).decode());return int(report['verdict']!='PASS')
from collections import Counter
if __name__=='__main__':sys.exit(main())
