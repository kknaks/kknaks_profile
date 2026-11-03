"""Offline actual-builder metamorphic tests; all copies stay under v2 scratch."""
import copy,contextlib,io,os,runpy,shutil
from common import *
import common
from identity import SourceRegistry
raw=Path(read(A/'inventory.json')['roots']['raw'])
checks=[]
def ck(name,ok,**detail):checks.append({'check':name,'pass':bool(ok),**detail})
def build(root=None,schema=None,rule=None,editorial=False):
 oldwrite=common.write;oldsha=common.sha;captured={};before=dict(os.environ)
 common.write=lambda name,obj:captured.update({name:copy.deepcopy(obj)})
 if editorial:common.sha=lambda path:'f'*64 if Path(path)==D/'design.json' else oldsha(path)
 for key,val in [('V2_RAW_ROOT',root),('V2_SCHEMA_VERSION',schema),('V2_RULE_REVISION',rule)]:
  if val:os.environ[key]=str(val)
  else:os.environ.pop(key,None)
 try:
  with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(O/'build.py'))
  return captured['pilot.json']
 finally:
  common.write=oldwrite;common.sha=oldsha
  os.environ.clear();os.environ.update(before)
def ids(p,g):return [x['id'] for x in p[g]]
def sources(p):return {(x['logical_file_key'],x['pointer']):x['id'] for x in p['source_records'] if x['file'].endswith('.json')}
start={str(f):sha(f) for f in raw.rglob('*.json')}
scratch=O/'_identity_scratch';scratch.mkdir(exist_ok=False)
try:
 base=build();ck('actual_builder_reproduces_artifact',__import__('json').loads(__import__('json').dumps(base))==read(O/'pilot.json'))
 moved=scratch/'moved'
 shutil.copytree(raw,moved)
 relocated=build(moved)
 ck('relocation_snapshot_ids',ids(base,'snapshots')==ids(relocated,'snapshots'))
 ck('relocation_occurrence_ids',sources(base)==sources(relocated))
 ck('relocation_entity_ids',ids(base,'entities')==ids(relocated,'entities'))
 from validate import safe_validate
 from project import project
 relocated_checks=safe_validate(__import__('json').loads(__import__('json').dumps(relocated)),project(relocated))
 ck('relocated_artifact_validator_accepts',all(row['pass'] for row in relocated_checks),failures=[row for row in relocated_checks if not row['pass']][:5])
 ck('relocation_normalized_ids',all(ids(base,g)==ids(relocated,g) for g in ['scopes','claims','mappings','relation_claims','attachments','decisions','resolutions','notes']))
 # Reorder existing source rows using actual full builder, no invented clinical content.
 path=moved/'anatomy-danger-zones.json';original=path.read_bytes();obj=read(path);obj['zones'].reverse();path.write_text(__import__('json').dumps(obj,ensure_ascii=False))
 reordered=build(moved)
 ck('row_reorder_new_snapshot',ids(base,'snapshots')[0]!=ids(reordered,'snapshots')[0])
 ck('row_reorder_new_occurrences',all(sources(base)[k]!=v for k,v in sources(reordered).items() if k[0] in {f.name for f in raw.glob('*.json')}))
 ck('row_reorder_entity_ids_preserved',ids(base,'entities')==ids(reordered,'entities'))
 path.write_bytes(original)
 # Change display label only; native IDs stay exactly as the source supplies.
 path=moved/'taxonomy.json';original=path.read_bytes();obj=read(path);obj['modality'][0]['name']=obj['modality'][0].get('name','')+' [display-label-test]';path.write_text(__import__('json').dumps(obj,ensure_ascii=False))
 renamed=build(moved)
 ck('display_name_entity_ids_preserved',ids(base,'entities')==ids(renamed,'entities'))
 ck('display_name_new_source_snapshot',ids(base,'snapshots')[0]!=ids(renamed,'snapshots')[0]);path.write_bytes(original)
 # A logical file rename is a new identity even if basename/bytes are equal.
 path=moved/'anatomy-danger-zones.json';(moved/'nested').mkdir();path.rename(moved/'nested'/path.name)
 file_renamed=build(moved)
 ck('logical_file_rename_new_snapshot',ids(base,'snapshots')[0]!=ids(file_renamed,'snapshots')[0])
 ck('logical_file_rename_entity_ids_preserved',ids(base,'entities')==ids(file_renamed,'entities'))
 (moved/'nested'/path.name).rename(path)
 physical=[]
 for name in ['a','b','generated']:
  folder=scratch/name;folder.mkdir();target=folder/'same.json';shutil.copyfile(raw/'anatomy-danger-zones.json',target);physical.append(target)
 reg=SourceRegistry([('raw21','test/raw',[('a/same.json',physical[0]),('b/same.json',physical[1])]),('generated-silver','test/generated',[('a/same.json',physical[2])])])
 a=reg.src(physical[0],'');b=reg.src(physical[1],'');c=reg.src(physical[2],'')
 ck('same_bytes_different_full_logical_key',a!=b)
 ck('same_bytes_different_domain',a!=c and reg.snapshots[0]['id']!=reg.snapshots[1]['id'])
 ck('same_basename_multi_manifest',len(reg.snapshots[0]['files'])==2 and len({f['logical_file_key'] for f in reg.snapshots[0]['files']})==2)
 # Validate revision propagation through actual complete builder, not a formula-only toy.
 for name,kw in [('schema_revision',{'schema':'silver-design-pilot/3-test'}),('rule_revision',{'rule':'pilot-preserve-source/3-test'})]:
  revised=build(**kw)
  ck(name+'_source_immutable',sources(base)==sources(revised) and ids(base,'snapshots')==ids(revised,'snapshots'))
  ck(name+'_entity_immutable',ids(base,'entities')==ids(revised,'entities'))
  ck(name+'_normalized_revised',all(set(ids(base,g)).isdisjoint(ids(revised,g)) for g in ['scopes','claims','mappings','relation_claims','attachments','decisions','resolutions','notes']))
 editorial=build(editorial=True)
 ck('unrelated_design_hash_does_not_rekey',base['basis']['sha256']!=editorial['basis']['sha256'] and all(ids(base,g)==ids(editorial,g) for g in ['snapshots','source_records','entities','scopes','claims','mappings','relation_claims','attachments','decisions','resolutions','notes']))
finally:shutil.rmtree(scratch)
ck('original_raw21_unchanged',start=={str(f):sha(f) for f in raw.rglob('*.json')})
write('identity-tests.json',{'checks':checks,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'scope':'Actual builder and its SourceRegistry; revision test versions are unpublished incompatible fixtures.'})
print(__import__('json').dumps({'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'failures':[x for x in checks if not x['pass']]}))
assert all(x['pass'] for x in checks)
