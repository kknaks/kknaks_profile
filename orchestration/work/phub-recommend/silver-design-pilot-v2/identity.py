"""Builder identity implementation; validator independently recomputes its formulas."""
from common import *
import copy
SCHEMA_VERSION='silver-design-pilot/2'
RULE_REVISION='pilot-preserve-source/2'
NORMALIZED=['scopes','mappings','claims','relation_claims','notes','decisions','resolutions','attachments']
class SourceRegistry:
 def __init__(self,collections):
  self.snapshots=[];self.records=[];self.files={};self.cache={}
  for domain,collection,entries in collections:
   if len({key for key,path in entries})!=len(entries):raise ValueError('Duplicate logical file key in collection')
   manifest=sorted([[key,sha(path)] for key,path in entries])
   sid='snap:'+digest([domain,collection,manifest])
   self.snapshots.append({'id':sid,'domain':domain,'collection':collection,'source_kind':{'raw21':'raw_snapshot','generated-silver':'generated','decision-artifact':'decision'}[domain], 'source_version':None,'captured_at':None,'files':[{'logical_file_key':key,'file':str(Path(path).resolve()),'sha256':sha(path),'bytes':Path(path).stat().st_size} for key,path in sorted(entries)]})
   for key,path in entries:
    locator=str(Path(path).resolve())
    if locator in self.files:raise ValueError('Ambiguous physical locator; use distinct locators for distinct logical bindings: '+locator)
    self.files[locator]=(sid,key)
 def src(self,path,ptr):
  path=str(Path(path).resolve());sid,key=self.files[path];rid='src:'+digest([sid,key,ptr])
  if rid not in self.cache:
   val=get(read(path),ptr)
   self.records.append({'id':rid,'snapshot_ref':sid,'logical_file_key':key,'file':path,'pointer':ptr,'native_id':str(val.get('id',val.get('ledger_id'))) if isinstance(val,dict) and (val.get('id') or val.get('ledger_id')) else None,'raw_value':copy.deepcopy(val),'parent_ref':None,'continuity_ref':None});self.cache[rid]=True
  return rid

def revise(p,schema_version=SCHEMA_VERSION,rule_revision=RULE_REVISION):
 """Topological normalized revision IDs; never alters source or entity identity."""
 p['schema_version']=schema_version;p['mapping_rule_revision']=rule_revision
 for group in NORMALIZED:
  for record in p[group]:
   old=record['id'];record['record_schema_version']=schema_version;record['mapping_rule_revision']=rule_revision
   new=old.split(':')[0]+':'+digest([schema_version,rule_revision,{k:v for k,v in record.items() if k!='id'}])
   def replace(obj):
    if isinstance(obj,dict):
     for k,v in obj.items():
      if isinstance(v,str) and v==old:obj[k]=new
      else:replace(v)
    elif isinstance(obj,list):
     for i,v in enumerate(obj):
      if isinstance(v,str) and v==old:obj[i]=new
      else:replace(v)
   replace(p)
 return p
