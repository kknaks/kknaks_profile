#!/usr/bin/env python3
"""Independent source validator. Does not import builder or its transformation functions."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys
from transport import BASE, HERE, canonical, digest, sha, load, write, pointer, escape, leaves

VERSION='silver-batch1/1'
NORM={'onset_duration.peak_effect':'onset_duration.peak','safety.common_adverse_effects':'safety.common',
      'safety.serious_adverse_effects':'safety.serious','safety.common_side_effects':'safety.common'}
PREFIX={'scope':'scp','mapping':'map','claim':'clm','decision':'dec','attachment':'att'}
MISSING=object()

def equal(a,b):return canonical(a)==canonical(b)

def evaluate(candidate, records=None, check_exports=True):
    """Return diagnostics; source and fixed expectations are read independently each call."""
    out=Path(candidate);g=records if records is not None else load(out/'records.json')
    errors=[];checks=Counter()
    def check(ok,code,locator,field,reason):
        checks[code]+=1
        if not ok:errors.append({'code':code,'source_locator':locator,'field':field,'reason':reason})
    def eq(a,b,code,locator,field,reason='Independent original value/contract mismatch'):
        check(equal(a,b),code,locator,field,reason)
    # Input gate uses fixed approved v2, never a current log or self-generated baseline.
    fixed=load(HERE/'expected-inputs.json')
    for name,h in fixed.items():check(sha(BASE/name)==h,'FIXED_INPUT',str(BASE/name),'sha256','Approved contract/oracle bytes changed')
    manifest=load(BASE/'silver-data-contract-batch1/contract-fix/input-manifest.v2.json')
    docs={};filemeta={}
    for row in manifest:
        p=Path(row['file']); key=(row['domain'],row['logical_file_key']);filemeta[key]=row
        check(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'INPUT_HASH',str(p),'sha256/bytes','Immutable input changed')
        docs[key]=load(p) if p.suffix=='.json' else p.read_text(encoding='utf-8')
    eq(load(out/'input-manifest.json'),manifest,'MANIFEST',str(out),'input-manifest')
    collections=load(BASE/'silver-data-contract-batch1/contract-fix/collections.json');snapshots={r['domain']:r for r in g['snapshots']}
    check(len(snapshots)==5 and len(g['snapshots'])==5,'SNAPSHOT_COUNT','manifest','snapshots','Exactly five fixed collections')
    for col in collections:
        domain=col['domain'];rows=[r for r in manifest if r['domain']==domain];s=snapshots.get(domain,{})
        eq(sorted(r['logical_file_key'] for r in rows),sorted(col['members']),'MEMBERSHIP',domain,'files')
        sid='snap:'+digest([domain,col['collection'],sorted([[r['logical_file_key'],r['sha256']] for r in rows])])
        eq(s.get('id'),sid,'SNAPSHOT_ID',domain,'id');eq(s.get('files'),rows,'SNAPSHOT_META',domain,'files')
        eq(s.get('source_kind'),col['source_kind'],'SNAPSHOT_META',domain,'source_kind')
        check(s.get('source_version') is None and bool(s.get('source_version_reason')),'VERSION_NULL',domain,'source_version','Collection has no separately declared version')
        check(s.get('captured_at') is None,'TIME',domain,'captured_at','No collection capture time evidence')
    allrecords=[r for name in ['snapshots','source_records','products','families','registry','scopes','mappings','claims','decisions','attachments'] for r in g[name]]
    byid={r['id']:r for r in allrecords}
    check(len(byid)==len(allrecords),'UNIQUE_ID','records','id','Record IDs must be globally unique')
    source={};sourcedict={}
    for r in g['source_records']:
        key=(r.get('domain'),r.get('logical_file_key'));ptr=r.get('pointer');loc=str(r.get('file'))+'#'+str(ptr)
        check(key in docs and key[0]!='audit-artifact','SOURCE_DOMAIN',loc,'domain','Semantic source must belong to fixed non-audit membership')
        if key not in docs:continue
        try:v=pointer(docs[key],ptr)
        except (ValueError,KeyError,TypeError,IndexError):check(False,'POINTER',loc,'pointer','Unreachable actual source');continue
        eq(r['raw_value'],v,'SOURCE_RAW',loc,'raw_value')
        eq(r.get('snapshot_ref'),snapshots[key[0]]['id'],'SOURCE_SNAPSHOT',loc,'snapshot_ref')
        eq(r.get('id'),'src:'+digest([snapshots[key[0]]['id'],key[1],ptr]),'SOURCE_ID',loc,'id')
        eq(r.get('file'),filemeta[key]['file'],'PHYSICAL_LOCATOR',loc,'file')
        eq(r.get('collection'),filemeta[key]['collection'],'SOURCE_DOMAIN',loc,'collection')
        eq(r.get('source_sha256'),filemeta[key]['sha256'],'SOURCE_HASH',loc,'source_sha256')
        eq(r.get('continuity_ref'),None,'CONTINUITY',loc,'continuity_ref','No prior snapshot evidence exists')
        if r.get('parent_ref'):
            parent=byid.get(r['parent_ref'],{})
            check(parent.get('pointer')==ptr.rsplit('/',1)[0] and parent.get('snapshot_ref')==r['snapshot_ref'] and parent.get('logical_file_key')==key[1],
                  'SOURCE_PARENT',loc,'parent_ref','Parent must be actual same-file JSON containment')
        else:check(ptr=='','SOURCE_PARENT',loc,'parent_ref','Only root has no containment parent')
        if isinstance(docs[key],str):
            check(ptr=='' and r.get('media_type')=='text/plain','TEXT_ROOT',loc,'media_type/pointer','Text has root transport only')
            eq(r.get('source_lines'),[1,len(v.splitlines())],'TEXT_LINES',loc,'source_lines')
            check(r['raw_value'].encode('utf-8')==Path(filemeta[key]['file']).read_bytes(),'TEXT_BYTES',loc,'raw_value','Decoded text round-trip must equal original bytes')
        else:eq(r.get('media_type'),'application/json','MEDIA',loc,'media_type')
        native=v.get('ledger_id',v.get('id')) if isinstance(v,dict) else None
        if isinstance(native,str):eq(r.get('native_id'),native,'NATIVE_ID',loc,'native_id')
        source[r['id']]=r;sourcedict[key+(ptr,)]=r
    def sr(key,ptr,domain='generated-silver'):
        return sourcedict.get((domain,key,ptr),{})
    def refs(value,allowed,loc,field,minimum=0,nullable=False):
        if value is None:
            check(nullable,'NULL_REF',loc,field,'Unexpected null reference');return
        vals=value if isinstance(value,list) else [value]
        check(len(vals)>=minimum,'REF_CARDINALITY',loc,field,'Too few references')
        check(len(vals)==len(set(vals)),'REF_DUPLICATE',loc,field,'Duplicate graph reference')
        for ref in vals:check(ref in byid and byid[ref].get('type') in allowed,'REF_TYPE',loc,field,'Unreachable or wrong target type: '+str(ref))
    # Rule truth is checked against independently pinned code hashes, actual source values and authority.
    rule=load(out/'rule-manifest.json');lockpath=HERE/'expected-rules.json'
    if lockpath.exists():
        lock=load(lockpath)
        for n,h in lock['implementation'].items():
            check(sha(HERE/n)==h,'RULE_CODE',str(HERE/n),'sha256','Actual code differs from reviewed lock')
            eq(rule.get('implementation',{}).get(n),h,'RULE_FINGERPRINT',str(out/'rule-manifest.json'),n)
    else:check(False,'RULE_LOCK',str(lockpath),'exists','Independent rule expectation missing')
    eq(rule.get('id'),'batch1-source-preservation','RULE_ID','rule-manifest','id')
    eq(rule.get('version'),'2','RULE_VERSION','rule-manifest','version')
    eq(rule.get('schema_version'),VERSION,'RULE_VERSION','rule-manifest','schema_version')
    eq(rule.get('authority'),'DATA-001/2 §5; WORK-013 P0-P4 candidate only','RULE_AUTHORITY','rule-manifest','authority')
    eq(rule.get('data_contract_sha256'),fixed['DATA-001.md'],'RULE_AUTHORITY','rule-manifest','data_contract_sha256')
    eq(rule.get('field_contract_sha256'),fixed['silver-data-contract-batch1/field-contract.json'],'RULE_AUTHORITY','rule-manifest','field_contract_sha256')
    eq(rule.get('key_normalize'),NORM,'NORMALIZER','rule-manifest','key_normalize')
    source_rule=docs['generated-silver','step5-units.json']['rules']['extracted']['key_normalize']
    eq(source_rule,NORM,'NORMALIZER_SOURCE','step5-units.json#/rules/extracted/key_normalize','value')
    eq(rule.get('source_rule'),{'domain':'generated-silver','logical_file_key':'step5-units.json','pointer':'/rules/extracted/key_normalize','value':NORM},'RULE_SOURCE','rule-manifest','source_rule')
    revision='batch1-rules:'+digest({k:v for k,v in rule.items() if k!='mapping_rule_revision'})
    eq(g.get('record_schema_version'),VERSION,'SCHEMA_VERSION','records','record_schema_version')
    eq(g.get('mapping_rule_revision'),revision,'RULE_REVISION','records','mapping_rule_revision')
    eq(rule.get('mapping_rule_revision'),revision,'RULE_REVISION','rule-manifest','mapping_rule_revision')
    for r in allrecords:
        loc=r['id'];typ=r['type']
        if typ in PREFIX:
            check(not any('audit' in key.lower() or 'design' in key.lower() for key in r), 'AUDIT_ID_CONTAMINATION',loc,'normalized_payload','Audit/design basis must stay outside normalized ID payload')
            payload={k:v for k,v in r.items() if k not in ['id','type']}
            eq(r['id'],PREFIX[typ]+':'+digest([VERSION,g['mapping_rule_revision'],payload]),'NORMALIZED_ID',loc,'id')
        if 'source_refs' in r:refs(r['source_refs'],['source_record'],loc,'source_refs',1)
        if typ in ['product','family']:
            refs(r['decision_refs'],['decision'],loc,'decision_refs');check(type(r['revision']) is int and r['revision']==1,'ENTITY_REVISION',loc,'revision','First candidate content revision is one')
            check(isinstance(r['label'],str) and bool(r['label']),'LABEL_TYPE',loc,'label','Required nonempty source label')
            check(r['status'] in ['active','pending','retired','merged','split'],'STATUS_ENUM',loc,'status','Invalid lifecycle enum')
        if typ=='product':
            for k in ['license_claim_refs','spec_claim_refs']:refs(r[k],['claim'],loc,k,1)
            refs(r['family_mapping_refs'],['mapping'],loc,'family_mapping_refs')
            for role in r['company_roles']:refs(role['claim_ref'],['claim'],loc,'company_roles.claim_ref',1)
            for lm in r['line_memberships']:refs(lm['parent_product_ref'],['product'],loc,'line_memberships.parent_product_ref',1);refs(lm['decision_ref'],['decision'],loc,'line_memberships.decision_ref',nullable=True)
            for k in ['merged_from','split_from']:refs(r['continuity'][k],['product'],loc,'continuity.'+k)
            refs(r['continuity']['merged_into'],['product'],loc,'continuity.merged_into',nullable=True)
        if typ=='family':
            refs(r['definition_claim_refs'],['claim'],loc,'definition_claim_refs',1);refs(r['deferred_refs'],['mapping'],loc,'deferred_refs')
            for v in r['technique_defaults']:
                refs(v['technique_ref'],['technique'],loc,'technique_defaults.technique_ref',1);refs(v['claim_ref'],['claim'],loc,'technique_defaults.claim_ref',1);refs(v['decision_ref'],['decision'],loc,'technique_defaults.decision_ref',nullable=True)
        if typ=='scope':
            check(r['application_state']=='unknown','CLINICAL_STATE',loc,'application_state','Source preservation is not clinical approval')
            check(r['container_scope_ref'] is None,'SCOPE_PARENT',loc,'container_scope_ref','Batch has no new context parent synthesis')
            eq(sorted(r['axes']),sorted(['product','family','site','unit_procedure','concern','target','container','site_relation','statement_site','patient_conditions']),'SCOPE_AXES',loc,'axes')
            for axis,a in r['axes'].items():
                check(a['knowledge'] in ['explicit','unknown','not_declared','not_applicable'],'AXIS_ENUM',loc,axis,'Invalid knowledge')
                inc=a['included'];exc=a['excluded'];check(len(inc)==len(set(inc)) and len(exc)==len(set(exc)) and not set(inc)&set(exc),'SCOPE_SET',loc,axis,'Duplicate or intersecting included/excluded values')
                check(bool(a['raw_refs']),'SCOPE_EVIDENCE',loc,axis,'Axis requires actual evidence');refs(a['raw_refs'],['source_record'],loc,axis+'.raw_refs',1)
                if a['knowledge']=='explicit':check(bool(inc or exc),'SCOPE_EXPLICIT',loc,axis,'Explicit needs a value')
                if a['knowledge'] in ['not_declared','not_applicable'] or a['value_kind']=='none':check(not inc and not exc,'SCOPE_EMPTY',loc,axis,'State/value-kind requires empty set')
                if a['value_kind']=='entity_refs':refs(inc+exc,[axis],loc,axis+'.included/excluded')
            for q in r['statement_qualifiers']:
                refs(q['source_ref'],['source_record'],loc,'statement_qualifiers.source_ref',1)
                check(q.get('operator') is None and q.get('value') is None,'QUALIFIER',loc,'statement_qualifiers','Uninterpreted context not promoted')
        if typ=='mapping':
            check(r['purpose'] in ['identity','membership','unit_compatibility','normalization','attachment','classification'],'MAPPING_PURPOSE',loc,'purpose','Invalid purpose')
            check(r['state'] in ['exact','rule_mapped','ambiguous','unresolved','excluded','compatible_candidate','selected'],'MAPPING_STATE',loc,'state','Invalid state')
            refs(r['scope_ref'],['scope'],loc,'scope_ref',1);refs(r['selected_refs'],['product','family','unit_procedure'],loc,'selected_refs');refs(r['decision_refs'],['decision'],loc,'decision_refs')
            if r['rule'] is None:check(bool(r.get('reason')),'NULL_RULE_REASON',loc,'reason','Null rule requires real reason')
            else:eq(r['rule'],{'id':'batch1-key-normalize','version':'1','code_sha256':sha(HERE/'rules.py')},'MAPPING_RULE',loc,'rule','Only exact original dotted-key normalization is authorized')
            if r['state'] in ['unresolved','compatible_candidate','ambiguous','excluded']:eq(r['selected_refs'],[],'CANDIDATE_SELECTION',loc,'selected_refs')
            for c in r['candidates']:
                check(all(k in c for k in ['target_ref','role','basis','exclusion','scope_ref']),'CANDIDATE_SHAPE',loc,'candidates','Required candidate object')
                refs(c['target_ref'],['product','family','unit_procedure'],loc,'candidates.target_ref',nullable=True);refs(c['scope_ref'],['scope'],loc,'candidates.scope_ref',1)
                if c['target_ref'] is None:check(bool(c.get('raw_refs')) and bool(c.get('reason')),'CANDIDATE_NULL',loc,'candidates','Null candidate needs raw refs/reason')
        if typ=='claim':
            refs(r['subject_ref'],['product','family','unit_procedure'],loc,'subject_ref',nullable=True);refs(r['scope_ref'],['scope'],loc,'scope_ref',1);refs(r['mapping_refs'],['mapping'],loc,'mapping_refs',1)
            check(r['normalized_value'] is None,'NORMALIZED_VALUE',loc,'normalized_value','New clinical normalization forbidden')
            eq(r['variant'],{'of':None,'equivalence':'unreviewed'},'VARIANT',loc,'variant')
            check(r['review_state'] in ['unreviewed','source_conflict'],'CLINICAL_STATE',loc,'review_state','No new staff or clinical confirmation')
            check(r['override'] is None,'CLAIM_OVERRIDE',loc,'override','No approval-backed normalized override decision issued; original preserved in projection')
            check(r['language'] is None,'LANGUAGE',loc,'language','No explicit source language for these claims')
            check(r['kind'] in ['explanation','safety','risk','check','preparation','counseling','license','definition','recommendation','operational','price','evidence'],'CLAIM_KIND',loc,'kind','Invalid claim enum')
            for ref in r['source_refs']:
                if ref in source:eq(r['raw_value'],source[ref]['raw_value'],'CLAIM_RAW',source[ref]['file']+'#'+source[ref]['pointer'],r['raw_field'])
        if typ=='attachment':
            refs(r['claim_refs'],['claim'],loc,'claim_refs',1);refs(r['target_ref'],['product','family','unit_procedure'],loc,'target_ref',1);refs(r['scope_ref'],['scope'],loc,'scope_ref',1)
            eq(r['rule'],{'id':'batch1-source-preservation','version':'2'},'ATTACHMENT_RULE',loc,'rule')
            eq(r['witness'],[],'ATTACHMENT_WITNESS',loc,'witness');eq(r['resolution_ref'],None,'ATTACHMENT_RESOLUTION',loc,'resolution_ref')
            check(r['application_state']=='unknown' and bool(r['unknown_reasons']) and 'source_preservation_only' in r['unknown_reasons'],'CLINICAL_STATE',loc,'application_state','Unknown preservation only')
            for ref in r['claim_refs']:
                cl=byid.get(ref,{})
                check(cl.get('subject_ref')==r['target_ref'] and cl.get('scope_ref')==r['scope_ref'],'ATTACHMENT_OWNER',loc,'target_ref/scope_ref','Same verified source owner and scope only')
    # No invented approval/clinical result rows.
    eq(g['decisions'],[],'DECISION_AUTHORITY','records','decisions','No newly verified approval authority available; roots retain historical decisions')
    eq(g['relations'],[],'NEW_RELATION','records','relations');eq(g['resolutions'],[],'NEW_RESOLUTION','records','resolutions')
    pdoc=docs['generated-silver','step1-products.json'];fdoc=docs['generated-silver','step2-families.json'];sdoc=docs['generated-silver','step5-units.json'];tdoc=docs['generated-silver','step4-techniques.json']
    entities={r['id']:r for r in g['products']+g['families']};unitmap={r['id']:(i,r) for i,r in enumerate(sdoc['units'])}
    eq(sorted(r['id'] for r in g['products']),sorted('product:'+r['ledger_id'] for r in pdoc['items']),'PRODUCT_CENSUS','step1-products.json#/items','ids')
    eq(sorted(r['id'] for r in g['families']),sorted('family:'+r['id'] for r in fdoc['families']),'FAMILY_CENSUS','step2-families.json#/families','ids')
    index=load(out/'source-row-index.json');ic=Counter(r['category'] for r in index)
    eq(dict(ic),{'product':395,'family':27,'product_family':354,'safety':580},'ROW_CENSUS','source-row-index','category')
    for category,expected in [('product',[r['ledger_id'] for r in pdoc['items']]),('family',[r['id'] for r in fdoc['families']]),('product_family',[r['ledger_id'] for r in fdoc['product_family']])]:
        eq(sorted(r['native_id'] for r in index if r['category']==category),sorted(expected),'ROW_ID_SET','source-row-index',category)
    eq(sorted(r['ledger_id'] for r in fdoc['product_family']),sorted(r['ledger_id'] for r in pdoc['items'] if r['active']),'ACTIVE_JOIN','step2-families.json#/product_family','ledger_id')
    claims_by_source=defaultdict(list)
    for c in g['claims']:
        for ref in c['source_refs']:claims_by_source[ref].append(c)
    def fieldclaim(key,ptr,owner,field,kind=None):
        ss=sr(key,ptr);rows=claims_by_source.get(ss.get('id'),[])
        rows=[r for r in rows if r['subject_ref']==owner and r['raw_field']==field]
        check(len(rows)==1,'FIELD_CLAIM',key+'#'+ptr,field,'Exactly one original field claim required')
        if rows and kind:eq(rows[0]['kind'],kind,'FIELD_KIND',key+'#'+ptr,field)
        return rows[0] if rows else {}
    for i,row in enumerate(pdoc['items']):
        ref='product:'+row['ledger_id'];e=entities.get(ref,{});ptr='/items/'+str(i);loc='step1-products.json#'+ptr
        eq(e.get('native_id'),row['ledger_id'],'PRODUCT_IDENTITY',loc,'native_id')
        status='merged' if row.get('merged_into') else 'retired' if row.get('moved_to') else 'active' if row.get('active') is True else 'pending'
        eq(e.get('status'),status,'PRODUCT_STATUS',loc,'status');eq(e.get('label'),row['2_names']['display_name'],'PRODUCT_LABEL',loc,'label');eq(e.get('identity_kind'),row['1_identity']['kind'],'PRODUCT_KIND',loc,'identity_kind')
        eq(e.get('revision'),1,'PRODUCT_REVISION',loc,'revision')
        expected_alias=[]
        for j,a in enumerate(row['2_names'].get('search_names',[])):
            expected_alias.append({'text':a['name'],'lang':{'한':'ko','영':'en'}.get(a.get('lang'),a.get('lang')),'source_ref':sr('step1-products.json',ptr+'/2_names/search_names/'+str(j)).get('id'),'state':'unreviewed','original_lang':a.get('lang')})
        eq(e.get('aliases'),expected_alias,'PRODUCT_ALIAS',loc,'aliases')
        eq(e.get('continuity'),{'merged_from':['product:'+v for v in row.get('merged_from',[])],'merged_into':'product:'+row['merged_into'] if row.get('merged_into') else None,'moved_to':row.get('moved_to'),'split_from':['product:'+v for v in row.get('split_from',[])]},'PRODUCT_CONTINUITY',loc,'continuity','Merge/move/split must originate in exact native source field')
        for key in row:fieldclaim('step1-products.json',ptr+'/'+escape(key),ref,key,'license' if key=='4_license' else 'operational')
        expected_license=[]
        lc=fieldclaim('step1-products.json',ptr+'/4_license',ref,'4_license','license')
        if lc:expected_license.append(lc['id'])
        for k,v in row['4_license'].items():
            lc=fieldclaim('step1-products.json',ptr+'/4_license/'+escape(k),ref,'4_license.'+k,'license')
            if lc:expected_license.append(lc['id'])
            if k in ['licenses','history','reference']:
                for j,_ in enumerate(v):
                    lc=fieldclaim('step1-products.json',ptr+'/4_license/'+k+'/'+str(j),ref,'4_license.'+k+'.'+str(j),'license')
                    if lc:expected_license.append(lc['id'])
        eq(e.get('license_claim_refs'),expected_license,'PRODUCT_LICENSE',loc,'license_claim_refs')
        sp=fieldclaim('step1-products.json',ptr+'/5_spec',ref,'5_spec','operational')
        eq(e.get('spec_claim_refs'),[sp['id']] if sp else [],'PRODUCT_SPEC',loc,'spec_claim_refs')
        roles=[]
        for role in ['manufacturer','importer','seller','license_holder','other']:
            for j,value in enumerate(row['6_companies'].get(role,[])):
                c=fieldclaim('step1-products.json',ptr+'/6_companies/'+role+'/'+str(j),ref,'6_companies.'+role+'.'+str(j),'operational')
                if value.get('name')!='근거 없음':roles.append({'role':role,'name':value.get('name'),'original':value.get('original'),'claim_ref':c.get('id')})
        eq(e.get('company_roles'),roles,'PRODUCT_COMPANY',loc,'company_roles')
        allowedparents=set()
        if row.get('line',{}).get('line_row'):allowedparents.add('product:'+row['line']['line_row'])
        for master in pdoc['lines'].values():
            if master.get('line_row') and any(v.get('ledger_id')==row['ledger_id'] for v in master.get('items',[])):allowedparents.add('product:'+master['line_row'])
        for lm in e.get('line_memberships',[]):check(lm['parent_product_ref'] in allowedparents and lm['parent_product_ref']!=ref,'PRODUCT_LINE',loc,'line_memberships','Only explicit line_row/ledger_id association can establish parent')
        eq(e.get('decision_refs'),[],'DECISION_AUTHORITY',loc,'decision_refs')
    membermaps=[r for r in g['mappings'] if r['purpose']=='membership' and 'legacy' in r]
    check(len(membermaps)==354,'MEMBERSHIP_CENSUS','step2-families.json#/product_family','mappings','Each source row exactly once')
    for i,row in enumerate(fdoc['product_family']):
        ss=sr('step2-families.json','/product_family/'+str(i));matches=[m for m in membermaps if m['source_refs']==[ss.get('id')]]
        check(len(matches)==1,'MEMBERSHIP_JOIN','step2-families.json#/product_family/'+str(i),'ledger_id','Exactly one source-specific membership mapping')
        if not matches:continue
        m=matches[0];eq(m['legacy'],row,'MEMBERSHIP_RAW',ss.get('file'),'legacy')
        expected='excluded' if row.get('family')=='계열 밖' else 'unresolved' if not row.get('family') or row.get('pending_director') or row.get('conflict') else 'exact'
        eq(m['state'],expected,'MEMBERSHIP_STATE',ss.get('file'),'state')
        targets=['family:'+v for v in [row.get('family')]+row.get('also_families',[]) if v and v!='계열 밖']
        eq([c['target_ref'] for c in m['candidates']],targets,'MEMBERSHIP_CANDIDATE',ss.get('file'),'candidates')
        eq(m['selected_refs'],targets if expected=='exact' else [],'MEMBERSHIP_SELECTED',ss.get('file'),'selected_refs')
        owner=entities.get('product:'+row['ledger_id'],{})
        check(m['id'] in owner.get('family_mapping_refs',[]),'MEMBERSHIP_ENTITY',ss.get('file'),'family_mapping_refs','Membership mapping must join exact ledger ID')
    for i,row in enumerate(fdoc['families']):
        ref='family:'+row['id'];e=entities.get(ref,{});ptr='/families/'+str(i);loc='step2-families.json#'+ptr
        eq(e.get('label'),row['name'],'FAMILY_LABEL',loc,'label');eq(e.get('native_id'),row['id'],'FAMILY_IDENTITY',loc,'native_id');eq(e.get('status'),'pending','FAMILY_STATUS',loc,'status')
        eq(e.get('aliases'),[{'text':v,'lang':None,'source_ref':sr('step2-families.json',ptr+'/synonyms/'+str(j)).get('id'),'state':'unreviewed'} for j,v in enumerate(row.get('synonyms',[]))],'FAMILY_ALIAS',loc,'aliases')
        defs=[]
        for k in row:
            c=fieldclaim('step2-families.json',ptr+'/'+escape(k),ref,k,'definition' if k in ['definition','literature_evidence'] else 'operational')
            if k in ['definition','literature_evidence'] and c:defs.append(c['id'])
        eq(e.get('definition_claim_refs'),defs,'FAMILY_DEFINITION',loc,'definition_claim_refs');eq(e.get('subfamilies'),[],'SUBFAMILY_DESIGN',loc,'subfamilies')
        check(any(v['owner_ref']==ref and v['field']=='subfamilies' and v['state']=='needs_design' and bool(v['raw_refs']) for v in g['field_states']),'SUBFAMILY_DESIGN',loc,'field_states','Stable subfamily key/axis remains unissued')
        expected=[]
        for j,default in enumerate(tdoc['family_defaults']):
            if default['family']!=row['id']:continue
            cr=fieldclaim('step4-techniques.json','/family_defaults/'+str(j),ref,'technique_defaults','operational')
            for role,tids in [('default',[default['default']]),('also',default.get('also',[]))]:
                for tid in tids:expected.append({'technique_ref':'technique:'+tid,'role':role,'layer':default.get('default_layer'),'claim_ref':cr.get('id'),'decision_ref':None,'reason':'Historical default reference only; no new clinical approval'})
        eq(e.get('technique_defaults'),expected,'TECHNIQUE_DEFAULT',loc,'technique_defaults')
        eq(e.get('decision_refs'),[],'DECISION_AUTHORITY',loc,'decision_refs')
        check(len(e.get('deferred_refs',[]))==len(row.get('deferred',[])),'DEFERRED',loc,'deferred_refs','Every deferred source remains unresolved classification mapping')
    # Registry must point to actual original ID; no new typed unit/technique migration claim.
    for r in g['registry']:
        original=source.get(r['source_refs'][0],{}).get('raw_value',{})
        check(original.get('id')==r['native_id'] and r['id']==r['type']+':'+r['native_id'] and r.get('limited_registry') is True,'REGISTRY',r['id'],'native_id','Limited registry must reach actual source row')
    # Raw taxonomy census is independent of builder source-row list and safety export.
    raw=docs['raw21','taxonomy.json'];rawrows=[]
    for i,mod in enumerate(raw['modality']):
        for j,sub in enumerate(mod.get('subcategories',[])):
            for k,r in enumerate(sub.get('items',[])):rawrows.append((f'/modality/{i}/subcategories/{j}/items/{k}',r,'extracted'))
        for j,r in enumerate(mod.get('products',[])):rawrows.append((f'/modality/{i}/products/{j}',r,'taxonomy_products'))
    eq(dict(Counter(k for _,_,k in rawrows)),{'extracted':521,'taxonomy_products':59},'SAFETY_ROWS','taxonomy.json#/modality','rows')
    origin=load(BASE/'silver-data-contract-batch1/results/safety-origin-locators.json');oracle=load(BASE/'silver-data-contract-batch1/results/safety-field-oracle.json')
    origin_by_ptr={r['raw_pointer']:r for r in origin};oracle_by_ptr={r['raw_pointer']:r for r in oracle}
    safetyclaims=[];attachments=defaultdict(list)
    for att in g['attachments']:
        for ref in att['claim_refs']:attachments[ref].append(att)
    actual_fields=[];owners={};elig=0;notcreated=0;all_leaves=0;rows56=0;fields56=0;collisions=[];rename=Counter();notreason=Counter()
    row_by_cp={};claims_by_current={};safetyindex={r['raw_pointer']:r for r in index if r['category']=='safety'}
    for rawptr,rawrow,key in rawrows:
        matches=[(i,r) for i,r in enumerate(sdoc[key]) if r['id']==rawrow['id']]
        check(len(matches)==1,'SAFETY_JOIN','taxonomy.json#'+rawptr,'id','Exact source-ID join must be unique')
        if len(matches)!=1:continue
        idx,current=matches[0];cp='/'+key+'/'+str(idx);row_by_cp[cp]=current
        o=origin_by_ptr.get(rawptr,{})
        eq(o.get('legacy_id'),rawrow['id'],'ORIGIN_ORACLE','taxonomy.json#'+rawptr,'id');eq(o.get('current_pointer'),cp,'ORIGIN_ORACLE','taxonomy.json#'+rawptr,'current_pointer')
        owner=None;why=None
        if current['attach']=='단위 시술 후보':why='candidate_only'
        elif current['attach'].startswith('원문 보관'):why='out_of_batch_entity'
        elif current.get('product'):
            if 'product:'+current['product'] in entities:owner='product:'+current['product']
            else:why='owner_unresolved'
        elif current['attach']=='단위 시술' and len(current.get('units',[]))==1:
            uid=current['units'][0];u=unitmap.get(uid,(None,{}))[1]
            if any(s.get('id')==current['id'] and s.get('src')=='ledger' and s.get('role')!='후보' for s in u.get('sources',[])):owner='unit_procedure:'+uid
            else:why='owner_unresolved'
        else:why='owner_unresolved'
        owners[cp]=(owner,why);ri=safetyindex.get(rawptr,{})
        eq(ri.get('native_id'),rawrow['id'],'SAFETY_INDEX','taxonomy.json#'+rawptr,'native_id')
        eq(ri.get('entity_refs'),[owner] if owner else [],'OWNER_INDEX','taxonomy.json#'+rawptr,'entity_refs')
        eq(ri.get('attachment_state'),'eligible' if owner else 'not_created','ATTACHMENT_PARTITION','taxonomy.json#'+rawptr,'attachment_state')
        eq(ri.get('attachment_reason'),why,'ATTACHMENT_REASON','taxonomy.json#'+rawptr,'attachment_reason')
        if why in ['candidate_only','out_of_batch_entity']:rows56+=1
        ex=rawrow.get('extracted',{});rawfields=[('safety.'+k,rawptr+'/extracted/safety/'+escape(k),v) for k,v in ex.get('safety',{}).items()]
        if 'aftercare' in ex:rawfields.append(('aftercare',rawptr+'/extracted/aftercare',ex['aftercare']))
        predcounts=Counter(NORM.get(k,k) for k,_,_ in rawfields);current_claims=[]
        expected_before={}
        for k,_,v in rawfields:expected_before[NORM.get(k,k)]=v
        eq(current['source_text'],expected_before,'LEGACY_SOURCE_TEXT','step5-units.json#'+cp,'source_text','Original last-write view must match its historical source (collision is restored separately)')
        # all keys also verify normal onset rename independent of safety-only denominator
        for field in current['keys']:
            check(field==NORM.get(field,field),'NORMAL_RENAME','step5-units.json#'+cp,'keys','Legacy normalized key spelling preserved')
        for field,ptr,value in rawfields:
            all_leaves+=leaves(value);actual_fields.append(ptr);loc='taxonomy.json#'+ptr;os=oracle_by_ptr.get(ptr,{})
            eq(os.get('raw_value'),value,'FIELD_ORACLE',loc,'raw_value');eq(os.get('raw_field'),field,'FIELD_ORACLE',loc,'raw_field');eq(os.get('normalized_predicate'),NORM.get(field,field),'FIELD_ORACLE',loc,'predicate')
            ss=sr('taxonomy.json',ptr,'raw21');cs=[c for c in claims_by_source.get(ss.get('id'),[]) if c['kind'] in ['safety','preparation']]
            check(len(cs)==1,'SAFETY_CLAIM',loc,field,'Exactly one separate source claim for every raw field')
            if not cs:continue
            c=cs[0];current_claims.append(c);safetyclaims.append(c)
            eq(c['raw_field'],field,'RAW_FIELD',loc,'raw_field');eq(c['raw_value'],value,'SAFETY_RAW',loc,'raw_value');eq(c['predicate'],NORM.get(field,field),'PREDICATE',loc,'predicate');eq(c['subject_ref'],owner,'OWNER_SEMANTIC',loc,'subject_ref','Owner is independently checked against explicit legacy source/registry')
            eq(c['kind'],'preparation' if field=='aftercare' else 'safety','FIELD_KIND',loc,'kind');eq(c['review_state'],'source_conflict' if predcounts[NORM.get(field,field)]>1 else 'unreviewed','CONFLICT_STATE',loc,'review_state')
            scope=byid.get(c['scope_ref'],{});axis=owner.split(':')[0] if owner else None
            if owner:
                check(scope.get('axes',{}).get(axis,{}).get('knowledge')=='explicit' and scope['axes'][axis]['included']==[owner],'OWNER_SCOPE',loc,'axes','Explicit owner cannot be hidden as unknown')
            scfam=current.get('family')
            if scfam and 'family:'+scfam in entities:
                eq(scope['axes']['family']['included'],['family:'+scfam],'FAMILY_SCOPE',loc,'family');eq(scope['axes']['family']['knowledge'],'explicit','FAMILY_SCOPE',loc,'family.knowledge')
            maps=[byid[m] for m in c['mapping_refs'] if m in byid]
            im=[m for m in maps if m.get('purpose')=='identity'];nm=[m for m in maps if m.get('purpose')=='normalization']
            check(len(im)==1 and len(nm)==1,'SAFETY_MAPPING',loc,'mapping_refs','Separate identity and normalization mappings required')
            if im:
                eq(im[0]['selected_refs'],[owner] if owner else [],'OWNER_MAPPING',loc,'selected_refs');eq(im[0].get('attachment_reason'),why,'OWNER_MAPPING',loc,'attachment_reason')
                if why=='candidate_only':eq(im[0]['state'],'compatible_candidate','CANDIDATE_SELECTION',loc,'state')
            if nm:
                eq(nm[0].get('raw_field'),field,'NORMALIZATION_FIELD',loc,'raw_field');eq(nm[0].get('normalized_predicate'),NORM.get(field,field),'NORMALIZATION_FIELD',loc,'normalized_predicate')
            ats=attachments.get(c['id'],[])
            if owner:
                elig+=1;check(len(ats)==1,'ELIGIBLE_ATTACHMENT',loc,'attachments','Eligible field needs exactly one same-owner preservation attachment')
            else:
                notcreated+=1;notreason[why]+=1;check(not ats,'NOT_CREATED_ATTACHMENT',loc,'attachments','Candidate/ownerless/out-of-batch field must not attach')
            if why in ['candidate_only','out_of_batch_entity']:fields56+=1
            if field in NORM:rename[field]+=1
        claims_by_current[cp]=current_claims
        eq(sorted(ri.get('claim_refs',[])),sorted(c['id'] for c in current_claims),'SAFETY_INDEX_CLAIMS','taxonomy.json#'+rawptr,'claim_refs')
        for pred,n in predcounts.items():
            if n>1:collisions.append({'legacy_id':rawrow['id'],'fields':n,'before_leaves':leaves(current['source_text'][pred]),'after_leaves':sum(leaves(v) for k,_,v in rawfields if NORM.get(k,k)==pred)})
    eq(len(actual_fields),1394,'FIELD_CENSUS','taxonomy.json','safety/aftercare');eq(all_leaves,4170,'LEAF_CENSUS','taxonomy.json','safety/aftercare')
    eq(sorted(actual_fields),sorted(oracle_by_ptr),'FIELD_ORACLE_CENSUS','safety-field-oracle.json','pointers')
    eq([rows56,fields56],[56,132],'CANDIDATE_POSITIVE','step5-units.json','candidate/raw-only preserved, attachment not created')
    eq([elig,notcreated,elig+notcreated],[1242,152,1394],'ATTACHMENT_CENSUS','records','eligible+not_created')
    eq([len(collisions),sum(r['fields'] for r in collisions),sum(r['before_leaves'] for r in collisions),sum(r['after_leaves'] for r in collisions)],[3,6,6,16],'COLLISION_RESTORE','taxonomy.json','collision denominator')
    loss=[c for c in claims_by_current.get('/extracted/25',[]) if c['raw_field'].startswith('safety.')]
    check(bool(loss) and all(c['subject_ref']=='unit_procedure:U5-016' for c in loss),'LOSS02','step5-units.json#/extracted/25','subject_ref','LOSS02 is unit U5-016, never a product')
    # Projection is independently reconstructed from original override rows and separately retained raw fields.
    projections=load(out/'override-projection.json');pmap={r['source_pointer']:r for r in projections};overcounts=Counter();actualptr=[]
    for group in ['units','product_links']:
        for i,row in enumerate(sdoc[group]):
            for j,ov in enumerate(row.get('side_effect_override',[])):
                ptr=f'/{group}/{i}/side_effect_override/{j}';actualptr.append(ptr);overcounts[group]+=1;pr=pmap.get(ptr,{})
                eq(pr.get('legacy'),ov,'OVERRIDE_RAW','step5-units.json#'+ptr,'legacy');eq(pr.get('before'),ov['values'],'OVERRIDE_BEFORE','step5-units.json#'+ptr,'before')
                kind='taxonomy_products' if ov['source']=='taxonomy products extracted' else 'extracted'
                cp=next(('/'+kind+'/'+str(k) for k,r in enumerate(sdoc[kind]) if r['id']==ov['id']),None)
                cs=[c for c in claims_by_current.get(cp,[]) if c['raw_field'].startswith('safety.')]
                eq(pr.get('claim_refs'),[c['id'] for c in cs],'OVERRIDE_CLAIMS','step5-units.json#'+ptr,'claim_refs')
                after=defaultdict(list)
                for c in cs:
                    s=source[c['source_refs'][0]];after[c['predicate'][7:]].append({'claim_ref':c['id'],'source_refs':c['source_refs'],'raw_field':c['raw_field'],'raw_pointer':s['pointer'],'raw_value':c['raw_value']})
                eq(pr.get('after'),dict(after),'OVERRIDE_AFTER','step5-units.json#'+ptr,'after')
                eq(pr.get('application_state'),'unknown','CLINICAL_STATE','step5-units.json#'+ptr,'application_state')
    eq(dict(overcounts),{'units':248,'product_links':376},'OVERRIDE_CENSUS','step5-units.json','side_effect_override');eq(sorted(pmap),sorted(actualptr),'OVERRIDE_CENSUS','override-projection','pointers')
    from independent_source import source_semantics
    source_semantics(g, docs, manifest, collections, eq, check)
    # Coverage preserves all baseline contracts; direct locators independently reach original values.
    machine=load(HERE/'type-contract.json')['fields']
    eq(load(out/'schema.json').get('field_types'),machine,'MACHINE_SCHEMA','schema.json','field_types')
    fc=load(BASE/'silver-data-contract-batch1/field-contract.json')['fields'];baseline=load(BASE/'silver-pilot-closeout-review/coverage.json')['fields'];cov=load(out/'coverage.json')['fields'];cm={r['proposed']:r for r in cov};fm={r['proposed']:r for r in fc}
    eq(sorted(cm),sorted(r['proposed'] for r in baseline),'COVERAGE_247','coverage','proposed');eq(len(fc),84,'FIELDS_84','field-contract','fields')
    locators=0
    physical_docs={r['file']:docs[k] for k,r in filemeta.items()}
    source_files={r['file'] for r in source.values() if r['pointer']==''}
    for bf in baseline:
        key=bf['proposed'];cf=cm.get(key,{})
        eq(cf.get('baseline_status'),bf['status'],'BASELINE_STATUS','coverage',key);eq(cf.get('proposed_contract'),bf['proposed_contract'],'BASELINE_CONTRACT','coverage',key)
        if key not in fm:
            eq(cf.get('batch_status'),'out_of_batch','OUT_OF_BATCH','coverage',key)
            eq([cf.get('typed_count'),cf.get('raw_count'),cf.get('source_count')],[0,0,0],'OUT_OF_BATCH','coverage',key)
        else:
            typ,field=key.split('.',1);group={'product':'products','family':'families','snapshot':'snapshots','source_record':'source_records','scope':'scopes','claim':'claims','mapping':'mappings','decision':'decisions','attachment':'attachments'}[typ]
            values=[r.get(field,MISSING) for r in g[group]]
            check(all(v is not MISSING for v in values),'REQUIRED_FIELD','records',key,'Field contract requires present transport key')
            for r in g[group]:
                value=r.get(field,MISSING);spec=fm[key]['proposed_contract']['type'];ok=machine_type(value,machine[key])
                check(ok,'EXACT_TYPE',r['id'],key,'Expected '+spec+' including declared nullable exceptions')
            for loc in fm[key].get('exact_current_locators',[]):
                p=Path(loc['file']);d=physical_docs.get(str(p));ptr=loc['pointer']
                try:v=pointer(d,ptr);locators+=1
                except (KeyError,ValueError,TypeError,IndexError):check(False,'FIELD_LOCATOR',str(p)+'#'+ptr,key,'Current contract locator missing');continue
                check(str(p) in source_files,'FIELD_RAW_COVERAGE',str(p)+'#'+ptr,key,'Original field reachable in preserved root/field source')
            check(cf.get('transform')==fm[key]['transform'] and cf.get('oracle')==fm[key]['oracle'],'FIELD_CONTRACT','coverage',key,'Actual coverage must retain precise transform/oracle')
    eq(locators,4576,'FIELD_LOCATOR_CENSUS','field-contract','exact_current_locators')
    # Export duplicates must be exact, not merely counts.
    if check_exports:
        exported=load(out/'safety-claims.json')['fields'];eq(len(exported),1394,'EXPORT_CENSUS','safety-claims','fields')
        for row in exported:
            c=byid.get(row['claim_ref'],{})
            for field in ['raw_field','raw_value','scope_ref','mapping_refs','source_refs']:
                eq(row.get(field),c.get(field),'EXPORT_DEEP_EQUAL','safety-claims',field)
            eq(row.get('predicate'),c.get('predicate'),'EXPORT_DEEP_EQUAL','safety-claims','predicate')
        om=load(out/'output-manifest.json')
        for r in om['files']:check(sha(out/r['file'])==r['sha256'] and (out/r['file']).stat().st_size==r['bytes'],'OUTPUT_HASH',str(out/r['file']),'sha256/bytes','Deterministic export changed')
    counts={'products':len(g['products']),'families':len(g['families']),'product_family':354,'safety_rows':len(rawrows),'safety_fields':len(actual_fields),'safety_leaves':all_leaves,'eligible_fields':elig,'not_created_fields':notcreated,'not_created_reasons':dict(notreason),'candidate_raw_only_rows':rows56,'candidate_raw_only_fields':fields56,'overrides':dict(overcounts),'collision_rows':collisions,'normal_renames':dict(rename),'field_locator_inspections':locators,'clinical_reviews':0}
    return {'verdict':'PASS' if not errors else 'FAIL','independent_source':True,'checks':dict(checks),'check_count':sum(checks.values()),'failure_count':len(errors),'diagnostics':errors,'counts':counts,'skips':[]}

def machine_type(value,schema):
    """Standard JSON Schema subset interpreted independently of transformations."""
    import re
    if value is MISSING:return False
    if 'anyOf' in schema and not any(machine_type(value,x) for x in schema['anyOf']):return False
    if 'enum' in schema and not any(equal(value,x) for x in schema['enum']):return False
    typ=schema.get('type')
    if typ=='string':
        if not isinstance(value,str):return False
        if 'pattern' in schema and re.fullmatch(schema['pattern'],value) is None:return False
    if typ=='null' and value is not None:return False
    if typ=='boolean' and type(value) is not bool:return False
    if typ=='integer' and (type(value) is not int or value<schema.get('minimum',value)):return False
    if typ=='array':
        if not isinstance(value,list) or len(value)<schema.get('minItems',0) or len(value)>schema.get('maxItems',len(value)):return False
        if not all(machine_type(x,schema.get('items',{})) for x in value):return False
    if typ=='object':
        if not isinstance(value,dict) or any(k not in value for k in schema.get('required',[])):return False
        for key,sub in schema.get('properties',{}).items():
            if key in value and not machine_type(value[key],sub):return False
        extra=schema.get('additionalProperties')
        if isinstance(extra,dict):
            if not all(machine_type(v,extra) for k,v in value.items() if k not in schema.get('properties',{})):return False
    return True

def sidecar_checks(out,g):
    """Independent consistency and typed reachability of all export/ledger sidecars."""
    out=Path(out);errors=[];checks=Counter()
    byid={r['id']:r for group in ['snapshots','source_records','products','families','registry','scopes','mappings','claims','decisions','attachments'] for r in g[group]}
    def check(ok,code,loc,field,reason):
        checks[code]+=1
        if not ok:errors.append({'code':code,'source_locator':loc,'field':field,'reason':reason})
    def ref(value,types,loc,field,nullable=False):
        if value is None:
            check(nullable,'SIDECAR_REF',loc,field,'Unexpected null');return
        vals=value if isinstance(value,list) else [value]
        check(len(vals)==len(set(vals)),'SIDECAR_REF',loc,field,'Duplicate graph refs')
        for v in vals:check(v in byid and byid[v].get('type') in types,'SIDECAR_REF',loc,field,'Target missing or wrong type: '+str(v))
    index=load(out/'source-row-index.json')
    for i,r in enumerate(index):
        loc='source-row-index.json#/'+str(i)
        for field,types in [('source_refs',['source_record']),('entity_refs',['product','family','unit_procedure']),('mapping_refs',['mapping']),('claim_refs',['claim'])]:ref(r[field],types,loc,field)
        for v in r['source_refs']:
            source=byid.get(v,{})
            if source.get('domain')=='generated-silver' and isinstance(source.get('raw_value'),dict):
                actual=source['raw_value'].get('ledger_id',source['raw_value'].get('id'))
                check(actual==r['native_id'],'SIDECAR_NATIVE',loc,'native_id','Source row ID must equal exported native ID')
    ledger=load(out/'mapping-ledger.json');maps={m['id']:m for m in g['mappings']}
    check(sorted(m['mapping_ref'] for m in ledger)==sorted(maps),'MAPPING_LEDGER_CENSUS','mapping-ledger.json','mapping_ref','Every purpose/field mapping occurs once')
    for i,r in enumerate(ledger):
        m=maps.get(r['mapping_ref'],{});loc='mapping-ledger.json#/'+str(i)
        for k in ['source_refs','purpose','state','candidates','selected_refs','rule','reason','scope_ref','decision_refs']:
            check(equal(r.get(k),m.get(k)),'MAPPING_LEDGER_RAW',loc,k,'Ledger must exactly retain source-specific mapping')
        expected=[c['id'] for c in g['claims'] if r['mapping_ref'] in c['mapping_refs']]
        check(r['claim_refs']==expected,'MAPPING_LEDGER_CLAIMS',loc,'claim_refs','All reverse field claim links required')
    identity=load(out/'identity-ledger.json');expected={e['id'] for e in g['products']+g['families']}
    check({v for r in identity for v in r['new_refs']}==expected and len(identity)==422,'IDENTITY_LEDGER_CENSUS','identity-ledger.json','new_refs','395 product and 27 family native identities')
    for i,r in enumerate(identity):
        loc='identity-ledger.json#/'+str(i);ref(r['source_refs'],['source_record'],loc,'source_refs');ref(r['new_refs'],[r['namespace']],loc,'new_refs')
        check(r['new_refs']==[r['namespace']+':'+r['old_id']] and r['state']=='exact','IDENTITY_LEDGER_NATIVE',loc,'new_refs','No name/first-match reissue')
    for i,r in enumerate(g['field_states']):
        loc='records.json#/field_states/'+str(i)
        ref(r['owner_ref'],['product','family','snapshot','source_record','scope','mapping','claim','attachment'],loc,'owner_ref');ref(r['raw_refs'],['source_record'],loc,'raw_refs')
        check(r['state'] in ['value','not_declared','unresolved','needs_design','not_applicable'] and bool(r['reason']) and bool(r['raw_refs']),'FIELD_STATE',loc,'state/reason/raw_refs','Explicit reason and actual source evidence')
    for i,r in enumerate(load(out/'override-projection.json')):
        loc='override-projection.json#/'+str(i);ref(r['source_ref'],['source_record'],loc,'source_ref');ref(r['target_ref'],['product','unit_procedure'],loc,'target_ref');ref(r['claim_refs'],['claim'],loc,'claim_refs');ref(r['scope_refs'],['scope'],loc,'scope_refs');ref(r['decision_ref'],['decision'],loc,'decision_ref',True)
        check(r['legacy']['override_of'] in byid and byid[r['legacy']['override_of']]['type']=='family','OVERRIDE_FAMILY',loc,'override_of','Legacy override family must reach original family')
    fields=load(BASE/'silver-data-contract-batch1/field-contract.json')['fields'];schema=load(out/'schema.json')
    expectedfields=[{k:f[k] for k in ['proposed','proposed_contract','transform','oracle','source_selectors','field_state_contract']} for f in fields]
    check(equal(schema['fields'],expectedfields),'SCHEMA_84_CONTRACT','schema.json','fields','Exact approved required/empty/meaning/transform/source/oracle retained')
    return dict(checks),errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',required=True);p.add_argument('--independent-source',action='store_true');a=p.parse_args()
    try:
        r=evaluate(a.candidate)
        counts,errors=sidecar_checks(a.candidate,load(Path(a.candidate)/'records.json'))
        r['checks'].update(counts);r['check_count']+=sum(counts.values());r['diagnostics'].extend(errors);r['failure_count']+=len(errors);r['verdict']='FAIL' if r['failure_count'] else 'PASS'
        write(Path(a.candidate)/'validation.json',r);print(canonical({'verdict':r['verdict'],'checks':r['check_count'],'failures':r['failure_count'],'first':r['diagnostics'][:8]}).decode());return int(r['failure_count']>0)
    except (OSError,ValueError,KeyError,TypeError,IndexError) as e:
        r={'verdict':'FAIL','diagnostics':[{'code':'STRUCTURAL','source_locator':a.candidate,'field':'records','reason':str(e)}]};write(Path(a.candidate)/'validation.json',r);print(str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
