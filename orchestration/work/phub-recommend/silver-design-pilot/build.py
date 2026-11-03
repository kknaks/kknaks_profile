"""Build only this pilot directory from immutable on-disk source snapshots."""
from common import *
from collections import Counter,defaultdict
import copy
inv=read(A/'inventory.json');raw=Path(inv['roots']['raw']);design=read(D/'design.json');issues=read(A/'issues.json')['issues']
p={'schema_version':'silver-design-pilot/1','basis':{'file':str(D/'design.json'),'sha256':sha(D/'design.json'),'status':'proposal_only'},'snapshots':[],'source_records':[],'entities':[],'scopes':[],'claims':[],'relation_claims':[],'mappings':[],'decisions':[],'resolutions':[],'attachments':[],'legacy_aliases':[],'notes':[],'cases':[],'coverage':{}}
files={};sources={};entities={}
def src(file,ptr):
 file=str(Path(file).resolve());key=(file,ptr)
 if key in sources:return sources[key]
 if file not in files:
  sid='snap:'+sha(file);files[file]=sid
  obj=read(file)
  p['snapshots'].append({'id':sid,'source_version':str(obj.get('version')) if isinstance(obj,dict) and 'version' in obj else None,'files':[{'file':file,'sha256':sha(file),'bytes':Path(file).stat().st_size}],'captured_at':None,'source_kind':'raw_snapshot' if Path(file).parent==raw else 'generated' if 'decisions' not in file else 'decision'})
 v=get(read(file),ptr);sid='src:'+digest([files[file],file,ptr]);sources[key]=sid
 p['source_records'].append({'id':sid,'snapshot_ref':files[file],'file':file,'pointer':ptr,'native_id':str(v.get('id',v.get('ledger_id'))) if isinstance(v,dict) and (v.get('id') or v.get('ledger_id')) else None,'raw_value':copy.deepcopy(v),'parent_ref':None,'continuity_ref':None})
 return sid
# Existing entity identity registry; no naming/array-order based identity minting.
catalog={}
for filename,ns,root,key in [('step1-products.json','product','items','ledger_id'),('step2-families.json','family','families','id'),('step3-sites.json','site','nodes','id'),('step5-units.json','unit_procedure','units','id'),('step8-relations.json','evidence_statement','evidence/statements','id')]:
 obj=read(B/filename)
 for i,x in enumerate(get(obj,'/'+root)):
  if key in x:catalog[ns+':'+x[key]]=(B/filename,'/'+root+'/'+str(i))
s7=read(B/'step7-concerns.json');s8=read(B/'step8-relations.json');s5=read(B/'step5-units.json')
for root in ['categories','subcategories','items','extra_items']:
 for i,x in enumerate(s7['concerns'][root]):catalog['concern:'+x['id']]=(B/'step7-concerns.json','/concerns/'+root+'/'+str(i))
def ent(ref):
 if ref not in entities:
  file,ptr=catalog[ref];sr=src(file,ptr);ns,native=ref.split(':',1)
  p['entities'].append({'id':ref,'type':ns,'native_id':native,'source_refs':[sr]});entities[ref]=True
 return ref
def scope(token,axes=None,container=None,qual=None,conflicts=None,state='unknown'):
 sid='scope:'+digest([p['basis']['sha256'],token,axes,container,qual,conflicts,state]);p['scopes'].append({'id':sid,'axes':axes or {},'container_scope_ref':container,'statement_qualifiers':qual or [],'conflicts':conflicts or [],'application_state':state});return sid
def axis(knowledge='unknown',included=None,refs=None):return {'knowledge':knowledge,'included':included or [],'excluded':[],'raw_refs':refs or []}
def claim(token,sr,sc,pred,kind='explanation',subject=None,field=None,language=None,review='unreviewed',rawvalue=None):
 cid='clm:'+digest([p['basis']['sha256'],token,sr,sc,pred]);r=next(x for x in p['source_records'] if x['id']==sr)
 p['claims'].append({'id':cid,'kind':kind,'subject_ref':subject,'predicate':pred,'raw_field':field or r['pointer'],'raw_value':copy.deepcopy(r['raw_value'] if rawvalue is None else rawvalue),'normalized_value':None,'source_refs':[sr],'scope_ref':sc,'mapping_refs':[],'language':language,'variant':{'of':None,'equivalence':'unreviewed'},'override':None,'review_state':review});return cid
def mapping(token,refs,sc,candidates=None,state='unresolved',purpose='identity',selected=None,rule=None):
 mid='map:'+digest([p['basis']['sha256'],token,refs,sc]);p['mappings'].append({'id':mid,'source_refs':refs,'purpose':purpose,'state':state,'candidates':[{'target_ref':ent(t),'role':'candidate','basis':'existing Silver source record; not application approval','exclusion':None,'scope_ref':sc} for t in candidates or []],'selected_refs':[ent(t) for t in selected or []],'rule':rule,'scope_ref':sc,'decision_refs':[],'reason':'No clinical mapping rule applied; preserve source/candidates without inventing an approval' if rule is None else 'Existing rule preserved'});return mid
def attach(token,cids,target,sc,witness=None,res=None,state='unknown',reasons=None):
 aid='att:'+digest([p['basis']['sha256'],token,cids,target,sc]);p['attachments'].append({'id':aid,'claim_refs':cids,'target_ref':ent(target),'rule':{'id':'pilot-preserve-source','version':'1'},'witness':witness or [],'scope_ref':sc,'application_state':state,'resolution_ref':res,'unknown_reasons':reasons or ['application unreviewed']});return aid
def case(cid,claims=None,rels=None,maps=None,scopes=None,att=None,notes=None):
 cs=next(x for x in design['cases'] if x['id']==cid)
 p['cases'].append({'id':cid,'group':cs['group'],'evidence_refs':cs['evidence'],'source_refs':[src(r['file'],pointer(r['locator'])) for r in cs['source']],'silver_refs':[src(cs['silver']['file'],pointer(cs['silver']['locator']))],'claim_refs':claims or [],'relation_refs':rels or [],'mapping_refs':maps or [],'scope_refs':scopes or [],'attachment_refs':att or [],'note_refs':notes or [],'status':'represented_unreviewed'})
# 1. Every safety field and leaf, including surviving lists: never content-deduplicate.
for c in read(A/'normalization-collisions.json'):
 ref=ent('unit_procedure:U5-016' if c['record_id']=='auto-2-1774737181584' else 'product:'+c['record_id']);modptr='/'+('/'.join(pointer(c['raw_path']).split('/')[1:3]));family_ref=ent('family:'+get(read(c['raw_file']),modptr)['id']);family_sr=src(c['raw_file'],modptr+'/id');sc=scope(['safety',ref],{ref.split(':',1)[0]:axis('explicit',[ref]),'family':axis('explicit',[family_ref],[family_sr])},state='explicit');cids=[]
 for field in c['sources']:
  ptr=pointer(c['raw_path'])+'/'+field['source_field'].replace('.','/')
  sr=src(c['raw_file'],ptr);cid=claim(['safety',sr],sr,sc,'safety.common','safety',ref,field['source_field']);cids.append(cid)
  # Preserve field-list provenance AND distinct leaf occurrence identities.
  for suffix,v in leaves(get(read(c['raw_file']),ptr)):src(c['raw_file'],ptr+suffix)
 aid=attach(['safety',ref],cids,ref,sc)
 case('LOSS-0'+str(len([x for x in p['cases'] if x['group']=='normalize-overwrite'])+1),cids,scopes=[sc],att=[aid])
# 2. Duplicate legacy CC keys: aliases resolve to sets of occurrences/entities.
dups=read(A/'duplicate-cc-evidence.json');alias=defaultdict(list)
for c in dups:
 sr=src(c['raw_file'],pointer(c['raw_path']));grp='concern:'+c['correspondence_item_parent'][0];target='concern:'+c['correspondence_targets'][0]
 sc=scope(['cc',sr],{'concern':axis('explicit',[ent(grp)],[sr])},state='explicit')
 corr_i=next(i for i,v in enumerate(s7['correspondence']) if v.get('target')==c['correspondence_targets']);corr_ref=src(B/'step7-concerns.json','/correspondence/'+str(corr_i))
 mid=mapping(['cc',sr],[sr,corr_ref],sc,[target],state='exact',selected=[target],rule={'id':'step7-apply.py','version':s7['version'],'code_sha256':sha(B/'step7-apply.py')})
 alias[c['legacy_key']].append({'source_record_ref':sr,'target_ref':ent(target),'scope_ref':sc})
 if grp=='concern:P9-4':
  cid='ANCHOR-'+('10' if c['original']['cc']=='프락셔널레이저' else '11');r=next(x for x in issues if x['id']==cid)
  cl=claim(['cc-scope',sr],sr,sc,'source_container_concern','recommendation',target)
  case(cid,[cl],maps=[mid],scopes=[sc])
for key,targets in alias.items():p['legacy_aliases'].append({'namespace':'problem-packages.cc','snapshot_ref':files[str(raw/'problem-packages.json')],'alias':key,'state':'ambiguous','selected_refs':[],'targets':targets})
# 3. Full CC combos 146. Source relation identity is independent of existing R8 pair expansion.
rawcc=read(raw/'problem-packages.json')
combo_rel={};arity=Counter();combo_candidates=defaultdict(list)
for pi,prob in enumerate(rawcc['problems']):
 for ci,cc in enumerate(prob['complaints']):
  for ki,co in enumerate(cc.get('combos',[])):combo_candidates[f"{prob['problem_id']}:{cc['cc']}#{ki}"].append(f'/problems/{pi}/complaints/{ci}/combos/{ki}')
for pi,prob in enumerate(rawcc['problems']):
 for ci,cc in enumerate(prob['complaints']):
  for ki,co in enumerate(cc.get('combos',[])):
   ptr=f'/problems/{pi}/complaints/{ci}/combos/{ki}';sr=src(raw/'problem-packages.json',ptr);ccsr=src(raw/'problem-packages.json',f'/problems/{pi}/complaints/{ci}');arity[len(co['combo'])]+=1
   conflict=pi==1 and ci==3 and ki==2
   sc=scope(['combo',sr],{'container':axis('explicit',[cc['cc'],cc.get('cc_group','')],[ccsr]),'statement_site':axis('unknown',refs=[sr])},qual=[{'axis':'site','raw':co['reason'],'operator':'verbatim','value':None,'source_ref':sr}] if conflict else [],conflicts=[{'axis':'site','container':cc['cc'],'statement':'목주름','source_ref':sr}] if conflict else [],state='unknown')
   cl=claim(['combo',sr],sr,sc,'combo_source_statement','recommendation',review='source_conflict' if conflict else 'unreviewed');members=[]
   for mi,name in enumerate(co['combo']):
    msr=src(raw/'problem-packages.json',ptr+'/combo/'+str(mi));mid=mapping(['member',msr],[msr],sc)
    members.append({'role':'component','mapping_ref':mid,'source_ref':msr})
   rr='rel:'+digest(sr);existing=[]
   key=f"{prob['problem_id']}:{cc['cc']}#{ki}"
   for ri,row in enumerate(s8['claims']):
    if row.get('source')=='problem-packages.complaints[].combos' and row.get('source_index')==key:
     ss=src(B/'step8-relations.json','/claims/'+str(ri));candidates=combo_candidates[key]
     existing.append({'id':row['id'],'source_record_ref':ss,'origin_state':'exact' if len(candidates)==1 else 'ambiguous','source_occurrence_refs':[src(raw/'problem-packages.json',v) for v in candidates],'rule_text':row['rule'],'lowering_text':row.get('lowering'),'source_index':row['source_index'],'endpoints_raw':{'a':row['a'],'b':row['b']},'source_arity':row['combo_size']})
   p['relation_claims'].append({'id':rr,'claim_ref':cl,'members':members,'arity':len(members),'relation_kind':'single_procedure_attribute' if len(members)==1 else 'source_combo','direction':'not_applicable' if len(members)==1 else 'unknown','field_conditions':{},'interval':{'raw':None,'min':None,'max':None,'unit':None,'open_high':None,'repeat':None},'parent_claim_ref':None,'derivation':None,'existing_expansions':existing,'source_record_ref':sr,'expansion_policy':'no_new_pairs; existing R8 expansion retained as evidence only'})
   combo_rel[ptr]=(rr,cl,sc)
for c in design['cases']:
 if c['group']=='singleton-pair-label':
  rr,cl,sc=combo_rel[pointer(c['source'][0]['locator'])];case(c['id'],[cl],[rr],scopes=[sc])
 if c['group']=='note-claim-lineage':
  x=c['proposed_record']['note_origin'];ptr=pointer(x['source_path']);rr,cl,sc=combo_rel[ptr];ss=src(B/'step7-concerns.json',pointer(c['silver']['locator']));r8sr=src(B/'step8-relations.json',pointer(x['silver_path']));nid='note:'+digest(ss)
  p['notes'].append({'id':nid,'source_record_ref':ss,'source_refs':[src(x['source_file'],ptr)],'claim_refs':[cl],'existing_claim_refs':[{'id':x['id'],'source_record_ref':r8sr}],'relation_ref':rr,'application_state':'unknown'})
  case(c['id'],[cl],[rr],scopes=[sc],notes=[nid])
# Container/statement disagreement kept unresolved; no solitary palja treatment edge.
ccsr=src(raw/'problem-packages.json','/problems/1/complaints/3');rr,cl,sc=combo_rel['/problems/1/complaints/3/combos/2'];case('ORIGIN-CC-01',[cl],[rr],scopes=[sc])
# 4. Field-level order branches; clinical review remains staff_check.
rs=src(raw/'contraindications.json','/rules/0');ss=src(B/'step8-relations.json','/claims/0');row=s8['claims'][0]
base=scope('order-common',{'site_relation':axis('unknown',refs=[rs])},state='conditional')
same=scope('order-same',{'site_relation':axis('explicit',['same_site'],[rs])},state='conditional');diff=scope('order-diff',{'site_relation':axis('explicit',['different_site'],[rs])},state='conditional')
cl=claim('order-claim',rs,base,'interval','recommendation',review='staff_check');members=[]
for name in ['from','to']:
 msr=src(raw/'contraindications.json','/rules/0/'+name);mid=mapping(['order',name],[msr],base,['family:'+get(read(raw/'contraindications.json'),'/rules/0/'+name)],state='exact',selected=['family:'+get(read(raw/'contraindications.json'),'/rules/0/'+name)]);members.append({'role':'a' if name=='from' else 'b','mapping_ref':mid,'source_ref':msr})
rr='rel:'+digest([cl,rs,'order-claim']);p['relation_claims'].append({'id':rr,'claim_ref':cl,'members':members,'arity':2,'relation_kind':'timing','direction':'unknown','field_conditions':{'same_day':{'scope_ref':base,'value':True,'options':None,'raw_ref':src(raw/'contraindications.json','/rules/0/interval')},'first':{'scope_ref':base,'value':None,'options':[{'scope_ref':same,'value':'a','raw_ref':src(raw/'contraindications.json','/rules/0/note')},{'scope_ref':diff,'value':'explicit_no_required_order','raw_ref':src(raw/'contraindications.json','/rules/0/note')}],'raw_ref':src(raw/'contraindications.json','/rules/0/note')},'days':{'scope_ref':base,'value':None,'options':None,'raw_ref':src(raw/'contraindications.json','/rules/0/interval')}},'interval':{'raw':'같은 날 가능','min':None,'max':None,'unit':None,'open_high':None,'repeat':None},'parent_claim_ref':None,'derivation':None,'existing_expansions':[{'id':'R8-0001','source_record_ref':ss,'origin_state':'exact','source_occurrence_refs':[rs],'rule_text':row['rule'],'lowering_text':row.get('lowering'),'source_index':str(row['source_index']),'endpoints_raw':{'a':row['a'],'b':row['b']},'source_arity':2}],'source_record_ref':rs,'expansion_policy':'field_conditions required; unknown site never selects first'})
case('SCOPE-ORDER-01',[cl],[rr],scopes=[base,same,diff])
# 5. Comparison member candidates, product compatibility and M4-only override.
for cid,ci,mi in [('CAND-volume',2,0),('CAND-wrinkle',1,1)]:
 c=next(x for x in design['cases'] if x['id']==cid);sr=src(raw/'procedure-comparison.json',f'/comparisons/{ci}');ss=src(c['silver']['file'],pointer(c['silver']['locator']));member=get(s7,pointer(c['silver']['locator']));msr=src(raw/'procedure-comparison.json',f'/comparisons/{ci}/procedures/{mi}')
 ctx=scope([cid,'context'],{'container':axis('explicit',[read(raw/'procedure-comparison.json')['comparisons'][ci]['subtitle']],[sr])},state='unknown');sc=scope([cid,'member'],{'site':axis('unknown',refs=[msr])},container=ctx)
 mid=mapping(cid,[msr,ss],sc,['unit_procedure:'+u for u in member['units']],state='ambiguous',purpose='unit_compatibility',rule={'id':'step7-apply.py','version':s7['version'],'code_sha256':sha(B/'step7-apply.py')});cl=claim(cid,msr,sc,'comparison_member','recommendation',field='procedures');p['claims'][-1]['mapping_refs']=[mid]
 case(cid,[cl],maps=[mid],scopes=[ctx,sc])
c=next(x for x in design['cases'] if x['id']=='PRODUCT-SCOPE-01');sr=src(c['source'][0]['file'],pointer(c['source'][0]['locator']));ss=src(c['silver']['file'],pointer(c['silver']['locator']));product=s5['product_links'][243];pref=ent('product:'+product['product']);sc=scope('product-override',{'product':axis('explicit',[pref],[sr]),'family':axis('explicit',[ent('family:M4')],[sr])},state='explicit');mid=mapping('product-compatible',[sr,ss],sc,['unit_procedure:'+u for u in product['inherited_candidates']],state='compatible_candidate',purpose='unit_compatibility',rule={'id':'step5-apply.py','version':s5['version'],'code_sha256':sha(B/'step5-apply.py')})
rawsafety=src(c['source'][0]['file'],pointer(c['source'][0]['locator'])+'/extracted/safety/common');cl=claim('product-override',rawsafety,sc,'safety.common','safety',pref,'safety.common');p['claims'][-1]['mapping_refs']=[mid]
p['claims'][-1]['override']={'claim_refs':[],'predicate':'safety.common','scope_ref':sc,'priority':product['side_effect_override'][0]['priority'],'decision_ref':None,'override_of':product['side_effect_override'][0]['override_of'],'level':product['side_effect_override'][0]['level'],'source_record_ref':ss}
aid=attach('product-override',[cl],pref,sc,state='unknown',reasons=['M4 source claim; M2 application unknown; compatibility does not select product']);case('PRODUCT-SCOPE-01',[cl],maps=[mid],scopes=[sc],att=[aid])
for idx in [2,3]:
 row=s8['conditions']['not_condition'][idx];cid='PROJECTION-'+row['id'];c=next(x for x in design['cases'] if x['id']==cid);rs=src(c['source'][0]['file'],pointer(c['source'][0]['locator']));ss=src(c['silver']['file'],pointer(c['silver']['locator']));sc=scope(row['id'],{'target':axis('explicit',[ent(row['target'])],[ss]),'patient_conditions':axis('not_applicable',refs=[ss])},state='not_applicable');cl=claim(row['id'],rs,sc,'preparation' if idx==2 else 'counseling','preparation' if idx==2 else 'counseling',ent(row['target']));aid=attach(row['id'],[cl],row['target'],sc,reasons=['empty conditions are not a safety approval']);case(cid,[cl],scopes=[sc],att=[aid])
# 6. Language qualifiers are separate immutable variants, no equivalence assertion.
c=next(x for x in design['cases'] if x['id']=='PATIENT-LANG-01');root=pointer(c['source'][0]['locator']);ref=ent('evidence_statement:ST-M2-adverse_effects-03');sc=scope('language',{'family':axis('explicit',[ent('family:M2')])});cids=[]
for suffix,lang in [('/statement','en')]+[('/patient_'+l,l) for l in ['ko','en','zh','ja']]:
 sr=src(c['source'][0]['file'],root+suffix);cids.append(claim(['language',sr],sr,sc,'statement' if suffix=='/statement' else 'patient_explanation','evidence',ref,suffix,lang))
 if len(cids)>1:p['claims'][-1]['variant']['of']=cids[0]
aid=attach('language',cids,ref,sc);case('PATIENT-LANG-01',cids,scopes=[sc],att=[aid])
# Existing policy is preserved separately from its two original claims.
c=next(x for x in design['cases'] if x['id']=='RESOLUTION-01');sc=scope('duration',{'product':axis('explicit',[ent('product:M10-1-1')])});cids=[]
s9=read(B/'step9-explanations.json')
for r in c['source']:
 sr=src(r['file'],pointer(r['locator']));existing_record_i=next(i for i,v in enumerate(s9['records']) if v['source']['path']==r['locator'].replace('$.','taxonomy.',1));existing_record_ref=src(B/'step9-explanations.json','/records/'+str(existing_record_i));mid=mapping(['duration-identity',sr],[sr,existing_record_ref],sc,['product:M10-1-1'],state='exact',selected=['product:M10-1-1'],rule={'id':'step9-apply.py','version':s9['version'],'code_sha256':sha(B/'step9-apply.py')});cids.append(claim(['duration',sr],sr,sc,'onset_duration.duration','explanation',ent('product:M10-1-1')));p['claims'][-1]['mapping_refs']=[mid]
decfile=B/'step9-decisions.json';dec=read(decfile);ds=src(decfile,'');src(decfile,'/conflict_resolution');did='dec:'+digest([sha(decfile),'D9-3'])
p['decisions'].append({'id':did,'target_refs':cids,'status':'approved','authority':{'kind':'approved_rule','reviewer':None},'reason':dec['decision_ref'],'source_refs':[ds],'decided_at':dec['decided_at'],'supersedes':[]})
rid='res:'+digest([cids,sha(decfile),'duration']);p['resolutions'].append({'id':rid,'input_claim_refs':cids,'scope_ref':sc,'policy':{'id':'D9-3','version':str(dec['version']),'code_sha256':sha(B/'step9-apply.py'),'decision_ref':did},'output':{'selected_claim_ref':cids[0],'value':get(read(c['source'][0]['file']),pointer(c['source'][0]['locator'])),'existing_slot_ref':src(c['silver']['file'],pointer(c['silver']['locator']))},'alternatives':[cids[1]],'state':'conservative','clinical_consensus':False,'unknown_branch':{'conditions':'unknown','clinical_approval':None}})
aid=attach('duration',cids,'product:M10-1-1',sc,res=rid);case('RESOLUTION-01',cids,scopes=[sc],att=[aid])
p['coverage']={'raw_files_inventory':21,'case_evidence_rows':len(p['cases']),'safety_collision_rows':3,'safety_original_fields':6,'safety_leaves':16,'previously_lost_leaves':10,'duplicate_cc_occurrences':4,'duplicate_cc_keys':2,'cc_combos':sum(arity.values()),'cc_combos_arity':dict(sorted(arity.items())),'note_links':7,'comparison_members':2,'language_variants':5,'duration_source_claims':2,'unstarted':'Full Silver migration, 1277 semantic-pending field cells, clinical revalidation, production Gold/API/DB and traversal implementation'}
assert len(p['cases'])==42
write('pilot.json',p)
print(json.dumps({k:len(v) for k,v in p.items() if isinstance(v,list)},ensure_ascii=False))
