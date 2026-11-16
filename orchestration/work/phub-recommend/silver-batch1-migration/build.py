#!/usr/bin/env python3
"""Build an inactive, fully traceable batch1 candidate; never writes canonical data."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys
from transport import BASE, HERE, SCHEMA, canonical, digest, sha, load, write, escape, pointer, leaves, read_inputs, verify_fixed_inputs
import rules

PREFIX = {'scope':'scp','mapping':'map','claim':'clm','decision':'dec','attachment':'att'}

def build(inputs, field_contract, output, locator_root=None):
    verify_fixed_inputs()
    out=Path(output).resolve()
    permitted=(BASE/'silver-batch1-candidate').resolve()
    if out != permitted and permitted/'tmp' not in out.parents:
        raise ValueError('output must be candidate or candidate/tmp descendant')
    if (out/'records.json').exists():
        raise ValueError('candidate already exists; use a fresh candidate/tmp/run-N')
    if sha(inputs) != load(HERE/'expected-inputs.json')['silver-data-contract-batch1/contract-fix/input-manifest.v2.json']:
        raise ValueError('manifest is not approved v2; no silent rebaseline')
    if sha(field_contract) != load(HERE/'expected-inputs.json')['silver-data-contract-batch1/field-contract.json']:
        raise ValueError('field contract differs from approved version')
    manifest, docs, locators=read_inputs(inputs, locator_root)
    collections=load(BASE/'silver-data-contract-batch1/contract-fix/collections.json')
    fields=load(field_contract)['fields']
    if len(fields)!=84:
        raise ValueError('84-field contract required')
    code_files=['build.py','rules.py','transport.py','type-contract.json']
    implementation={n:sha(HERE/n) for n in code_files}
    rule_payload={'id':'batch1-source-preservation','version':'2','schema_version':SCHEMA,
                  'implementation':implementation,'data_contract_sha256':sha(BASE/'DATA-001.md'),
                  'field_contract_sha256':sha(field_contract),'key_normalize':rules.KEY_NORMALIZE,
                  'authority':'DATA-001/2 §5; WORK-013 P0-P4 candidate only',
                  'source_rule':{'domain':'generated-silver','logical_file_key':'step5-units.json','pointer':'/rules/extracted/key_normalize','value':rules.KEY_NORMALIZE}}
    revision='batch1-rules:'+digest(rule_payload)
    graph={k:[] for k in ['snapshots','source_records','products','families','registry','scopes','claims','mappings','decisions','attachments','field_states','relations','resolutions']}
    graph.update(record_schema_version=SCHEMA,mapping_rule_revision=revision)
    snap_by_domain={}; source_by_key={}; files_by_key={(x['domain'],x['logical_file_key']):x for x in manifest}
    audit_sidecar=[]
    for col in collections:
        rows=[x for x in manifest if x['domain']==col['domain']]
        if sorted(x['logical_file_key'] for x in rows)!=sorted(col['members']):
            raise ValueError('fixed collection membership mismatch: '+col['domain'])
        sid='snap:'+digest([col['domain'],col['collection'],sorted([[x['logical_file_key'],x['sha256']] for x in rows])])
        snapshot={'id':sid,'type':'snapshot','domain':col['domain'],'collection':col['collection'],
                  'source_kind':col['source_kind'],'source_version':None,'source_version_reason':col['source_version_reason'],
                  'captured_at':None,'files':rows}
        graph['snapshots'].append(snapshot);snap_by_domain[col['domain']]=sid
        if not col['semantic_source']:
            audit_sidecar.append({'snapshot_ref':sid,'reason':'audit basis only; not a semantic source ref'})
    def src(domain, key, ptr='', native=None):
        ident=(domain,key,ptr)
        if ident in source_by_key:
            return source_by_key[ident]['id']
        if domain=='audit-artifact':
            raise ValueError('audit record cannot be semantic source')
        value=pointer(docs[domain,key],ptr)
        parent=src(domain,key,ptr.rsplit('/',1)[0]) if ptr else None
        rid='src:'+digest([snap_by_domain[domain],key,ptr])
        raw_native=(value.get('ledger_id',value.get('id')) if isinstance(value,dict) else None)
        record={'id':rid,'type':'source_record','snapshot_ref':snap_by_domain[domain],
                'domain':domain,'collection':files_by_key[domain,key]['collection'],'logical_file_key':key,
                'file':files_by_key[domain,key]['file'],'pointer':ptr,'native_id':raw_native if isinstance(raw_native,str) else native,
                'raw_value':value,'parent_ref':parent,'continuity_ref':None,
                'media_type':'application/json' if key.endswith('.json') else 'text/plain',
                'source_sha256':files_by_key[domain,key]['sha256']}
        if isinstance(docs[domain,key],str):
            if ptr: raise ValueError('text root only')
            record['source_lines']=[1,len(value.splitlines())]
        source_by_key[ident]=record;graph['source_records'].append(record)
        return rid
    # Full immutable roots preserve additional fields and history without inventing clinical claims.
    for x in manifest:
        if x['domain']!='audit-artifact':src(x['domain'],x['logical_file_key'])
    def gs(key,ptr='',native=None):return src('generated-silver',key,ptr,native)
    def norm(kind,payload):
        record={'id':PREFIX[kind]+':'+digest([SCHEMA,revision,payload]),'type':kind,**payload}
        graph[{'scope':'scopes','claim':'claims','mapping':'mappings','decision':'decisions','attachment':'attachments'}[kind]].append(record)
        return record['id']
    def scope(refs, owner_ref=None, family=None, qualifiers=None):
        axes={a:{'knowledge':'not_declared','included':[],'excluded':[],'raw_refs':refs,'value_kind':'none' if a in ['statement_site','patient_conditions'] else 'entity_refs'} for a in rules.AXES}
        if owner_ref:
            axis=owner_ref.split(':')[0]
            axes[axis].update(knowledge='explicit',included=[owner_ref],value_kind='entity_refs')
        if family:
            axes['family'].update(knowledge='explicit',included=['family:'+family])
        return norm('scope',{'axes':axes,'container_scope_ref':None,'statement_qualifiers':qualifiers or [],'conflicts':[],
                              'application_state':'unknown','source_refs':refs})
    def mapping(refs,purpose,state,scope_ref,candidates=None,selected=None,reason=None,rule=None,**extra):
        return norm('mapping',{'source_refs':refs,'purpose':purpose,'state':state,'candidates':candidates or [],
                              'selected_refs':selected or [],'rule':rule,'reason':reason or 'Explicit historical source identity; no separate approved mapping rule',
                              'scope_ref':scope_ref,'decision_refs':[],**extra})
    def candidate(target,scope_ref,rawrefs,reason='source identity only'):
        return {'target_ref':target,'role':'source_owner','basis':'explicit source field','exclusion':None,
                'scope_ref':scope_ref,'raw_refs':rawrefs,'reason':reason}
    def claim(owner_ref,field,value,refs,scope_ref,maprefs,kind='operational',conflict=False):
        return norm('claim',{'kind':kind,'subject_ref':owner_ref,'predicate':rules.KEY_NORMALIZE.get(field,field),
                             'raw_field':field,'raw_value':value,'normalized_value':None,'source_refs':refs,'scope_ref':scope_ref,
                             'mapping_refs':maprefs,'language':None,'variant':{'of':None,'equivalence':'unreviewed'},
                             'override':None,'review_state':'source_conflict' if conflict else 'unreviewed'})
    def state(owner_ref,field,rawrefs,status,reason,raw_state='value'):
        graph['field_states'].append({'owner_ref':owner_ref,'field':field,'state':status,'raw_refs':rawrefs,'reason':reason,'raw_state':raw_state})
    products=docs['generated-silver','step1-products.json'];families=docs['generated-silver','step2-families.json']; step5=docs['generated-silver','step5-units.json']; step4=docs['generated-silver','step4-techniques.json']
    if step5['rules']['extracted']['key_normalize'] != rules.KEY_NORMALIZE:raise ValueError('source normalizer rule mismatch')
    pids={'product:'+x['ledger_id'] for x in products['items']};fids={'family:'+x['id'] for x in families['families']};units={x['id']:x for x in step5['units']}
    # Historical refs are linked only on exact explicit native keys; all occurrences retained.
    historical=defaultdict(list)
    frozen_ref=src('decision-artifact','frozen-inputs/coordinator-progress-2026-11-03.md')
    def scan(domain,key,value,ptr=''):
        if isinstance(value,dict):
            ident=value.get('ledger_id',value.get('id'))
            if isinstance(ident,str) and 'product:'+ident in pids:historical[ident].append(src(domain,key,ptr))
            for k,v in value.items():scan(domain,key,v,ptr+'/'+escape(k))
        elif isinstance(value,list):
            for i,v in enumerate(value):scan(domain,key,v,ptr+'/'+str(i))
    for domain,key in docs:
        if domain in ['research-artifact','decision-artifact'] or key=='step1-apply-log.json':scan(domain,key,docs[domain,key])
    rowindex=[];identity=[];mapledger=[];entity_by_id={}
    pscopes={};pmaps={}
    for i,row in enumerate(products['items']):
        ref='product:'+row['ledger_id'];ptr='/items/'+str(i);s=gs('step1-products.json',ptr);sc=scope([s],ref); pscopes[ref]=sc
        mi=mapping([s],'identity','exact',sc,[candidate(ref,sc,[s])],[ref]);pmaps[ref]=mi
        e={'id':ref,'type':'product','native_id':row['ledger_id'],'revision':1,'status':rules.product_status(row),
           'label':row['2_names']['display_name'],'aliases':[], 'source_refs':sorted(set([s]+historical[row['ledger_id']])),
           'decision_refs':[],'identity_kind':row['1_identity']['kind'],'license_claim_refs':[],'spec_claim_refs':[],
           'company_roles':[],'family_mapping_refs':[],'line_memberships':[],
           'continuity':{'merged_from':['product:'+v for v in row.get('merged_from',[])],
                         'merged_into':'product:'+row['merged_into'] if row.get('merged_into') else None,
                         'moved_to':row.get('moved_to'),'split_from':['product:'+v for v in row.get('split_from',[])]}}
        for j,a in enumerate(row['2_names'].get('search_names',[])):
            ar=gs('step1-products.json',ptr+'/2_names/search_names/'+str(j))
            e['aliases'].append({'text':a['name'],'lang':rules.LANGUAGE.get(a.get('lang'),a.get('lang')),'source_ref':ar,'state':'unreviewed','original_lang':a.get('lang')})
        # Every original direct field is a claim; full license and its historical lists/status each retain occurrences.
        direct_claims={}
        for key,value in row.items():
            sr=gs('step1-products.json',ptr+'/'+escape(key));kind='license' if key=='4_license' else 'operational'
            cr=claim(ref,key,value,[sr],sc,[mi],kind);direct_claims[key]=cr
            if key=='4_license':
                e['license_claim_refs'].append(cr)
                for sub,val in value.items():
                    rr=gs('step1-products.json',ptr+'/4_license/'+escape(sub));e['license_claim_refs'].append(claim(ref,'4_license.'+sub,val,[rr],sc,[mi],'license'))
                    if sub in ['licenses','history','reference']:
                        for j,v in enumerate(val):
                            rr=gs('step1-products.json',ptr+'/4_license/'+sub+'/'+str(j));e['license_claim_refs'].append(claim(ref,'4_license.'+sub+'.'+str(j),v,[rr],sc,[mi],'license'))
            if key=='5_spec':e['spec_claim_refs'].append(cr)
        for role in ['manufacturer','importer','seller','license_holder','other']:
            for j,v in enumerate(row['6_companies'].get(role,[])):
                sr=gs('step1-products.json',ptr+'/6_companies/'+role+'/'+str(j));cr=claim(ref,'6_companies.'+role+'.'+str(j),v,[sr],sc,[mi])
                if v.get('name')=='근거 없음':
                    state(ref,'company_roles.'+role,[sr],'not_declared',v.get('basis') or 'No company named in original')
                else:e['company_roles'].append({'role':role,'name':v.get('name'),'original':v.get('original'),'claim_ref':cr})
        for proposed in [f for f in fields if f['logical_type']=='product']:
            field=proposed['proposed'].split('.',1)[1]
            sourcekey={'label':'2_names','aliases':'2_names','identity_kind':'1_identity','license_claim_refs':'4_license','spec_claim_refs':'5_spec','company_roles':'6_companies','line_memberships':'line','continuity':'active'}.get(field)
            if sourcekey and sourcekey in row:
                rv=row[sourcekey];rs='null' if rv is None else 'empty_array' if rv==[] else 'empty_object' if rv=={} else 'false' if rv is False else 'empty_string' if rv=='' else 'value'
                state(ref,field,[gs('step1-products.json',ptr+'/'+sourcekey)],'value','Typed field from original occurrence; historical/clinical status retained',rs)
            else:state(ref,field,[s],'unresolved' if field in ['decision_refs','line_memberships'] else 'value','Derived transport/ID or later exact membership join; no clinical default', 'missing' if sourcekey else 'derived')
        for key in ['merged_from','merged_into','moved_to','split_from']:
            if key not in row:state(ref,'continuity.'+key,[s],'not_declared','Absent in original; empty transport default is not a historical event','missing')
        line=row.get('line')
        if line:
            sr=gs('step1-products.json',ptr+'/line');parent=line.get('line_row')
            if parent and 'product:'+parent in pids and parent!=row['ledger_id']:
                e['line_memberships'].append({'parent_product_ref':'product:'+parent,'role':line.get('role'),'decision_ref':None,'reason':'Explicit line_row; no separately verified approval decision'})
            else:
                lm=mapping([sr,gs('step1-products.json','/lines')],'membership','unresolved',sc,reason='Line string/license number does not establish a parent native ID')
                mapledger.append({'source_ref':sr,'mapping_refs':[lm],'purpose':'membership','state':'unresolved'})
        for name,master in products['lines'].items():
            parent=master.get('line_row')
            if parent and 'product:'+parent in pids and parent!=row['ledger_id'] and any(v.get('ledger_id')==row['ledger_id'] for v in master.get('items',[])):
                lm={'parent_product_ref':'product:'+parent,'role':(line or {}).get('role','품목'),'decision_ref':None,'reason':'Explicit line_row; no separately verified approval decision'}
                if lm not in e['line_memberships']:e['line_memberships'].append(lm)
        state(ref,'decision_refs',[s],'unresolved','Historical gate/open/change and decision artifacts preserved; no approval synthesized')
        if e['status']=='pending':state(ref,'status',[s],'unresolved','Inactive without explicit merge/move remains pending')
        graph['products'].append(e);entity_by_id[ref]=e
        rowindex.append({'category':'product','source_refs':[s],'native_id':row['ledger_id'],'entity_refs':[ref],'mapping_refs':[mi],'claim_refs':list(direct_claims.values())})
        identity.append({'namespace':'product','old_id':row['ledger_id'],'new_refs':[ref],'source_refs':[s],'snapshot_ref':snap_by_domain['generated-silver'],'state':'exact','legacy_aliases':row.get('taxonomy_product_ids',[]),'continuity_raw':{k:row[k] for k in ['merged_from','merged_into','moved_to','line','dedup','merged_ledger_ids','line_children'] if k in row},'reason':'Native ledger ID preserved; no name matching'})
    techniques={x['id']:(i,x) for i,x in enumerate(step4['nodes'])};used_tech=set(); used_units=set()
    for i,row in enumerate(families['families']):
        ref='family:'+row['id'];ptr='/families/'+str(i);s=gs('step2-families.json',ptr);sc=scope([s],ref);mi=mapping([s],'identity','exact',sc,[candidate(ref,sc,[s])],[ref])
        e={'id':ref,'type':'family','native_id':row['id'],'revision':1,'status':'pending','label':row['name'],'aliases':[],
           'source_refs':[s,frozen_ref],'decision_refs':[],'definition_claim_refs':[],'subfamilies':[],'technique_defaults':[],'deferred_refs':[]}
        for j,a in enumerate(row.get('synonyms',[])):
            sr=gs('step2-families.json',ptr+'/synonyms/'+str(j));e['aliases'].append({'text':a,'lang':None,'source_ref':sr,'state':'unreviewed'})
        for key,val in row.items():
            sr=gs('step2-families.json',ptr+'/'+escape(key));cr=claim(ref,key,val,[sr],sc,[mi],'definition' if key in ['definition','literature_evidence'] else 'operational')
            if key in ['definition','literature_evidence']:e['definition_claim_refs'].append(cr)
        # Dotted historical literature paths are converted only if real containment is reachable.
        for j,ev in enumerate(row.get('literature_evidence',[])):
            path=ev.get('path','')
            if '#' in path:
                import re
                key,tail=path.split('#',1);parts=re.findall(r'[^.\[\]]+',tail);p='/'+ '/'.join(escape(x) for x in parts)
                if ('raw21',key) in docs:
                    try:
                        actual=pointer(docs['raw21',key],p)
                        if 'value' not in ev or actual==ev['value']:e['source_refs'].append(src('raw21',key,p))
                    except (KeyError,IndexError,TypeError,ValueError):pass
        rawrefs=[gs('step2-families.json',ptr+'/'+k) for k in ['sub_families','sub_family_handling'] if k in row]
        state(ref,'subfamilies',rawrefs or [s],'needs_design','Stable subfamily key/axis not issued; complete legacy raw preserved')
        state(ref,'decision_refs',[s],'unresolved','Historical name_basis/frozen attribution preserved; no new approval record')
        for j,de in enumerate(row.get('deferred',[])):
            sr=gs('step2-families.json',ptr+'/deferred/'+str(j));m=mapping([sr],'classification','unresolved',sc,reason='deferred_to is a historical destination, not an issued entity ID');e['deferred_refs'].append(m)
        for j,default in enumerate(step4['family_defaults']):
            if default['family']!=row['id']:continue
            sr=gs('step4-techniques.json','/family_defaults/'+str(j));cr=claim(ref,'technique_defaults',default,[sr],sc,[mi]);
            for role,ids in [('default',[default['default']]),('also',default.get('also',[]))]:
                for tid in ids:
                    if tid not in techniques:raise ValueError('technique target missing: '+tid)
                    used_tech.add(tid);e['technique_defaults'].append({'technique_ref':'technique:'+tid,'role':role,'layer':default.get('default_layer'),'claim_ref':cr,'decision_ref':None,'reason':'Historical default reference only; no new clinical approval'})
        state(ref,'technique_defaults',[s],'value','Limited registry references only; technique semantics not migrated')
        for proposed in [f for f in fields if f['logical_type']=='family']:
            field=proposed['proposed'].split('.',1)[1]
            if field in ['subfamilies','technique_defaults','decision_refs']:continue
            sourcekey={'label':'name','aliases':'synonyms','definition_claim_refs':'definition','deferred_refs':'deferred'}.get(field)
            rv=row.get(sourcekey) if sourcekey else None
            rr=[gs('step2-families.json',ptr+'/'+sourcekey)] if sourcekey in row else [s]
            rs='derived' if not sourcekey else 'missing' if sourcekey not in row else 'null' if rv is None else 'empty_array' if rv==[] else 'value'
            state(ref,field,rr,'value','Source-preserved typed transport; no clinical approval',rs)
        graph['families'].append(e);entity_by_id[ref]=e
        rowindex.append({'category':'family','source_refs':[s],'native_id':row['id'],'entity_refs':[ref],'mapping_refs':[mi],'claim_refs':e['definition_claim_refs']})
        identity.append({'namespace':'family','old_id':row['id'],'new_refs':[ref],'source_refs':[s],'snapshot_ref':snap_by_domain['generated-silver'],'state':'exact','reason':'Existing native family ID, no new subfamily or purpose ID'})
    for i,row in enumerate(families['product_family']):
        ref='product:'+row['ledger_id'];sr=gs('step2-families.json','/product_family/'+str(i));sc=pscopes[ref]
        targets=['family:'+v for v in [row.get('family')]+row.get('also_families',[]) if v and v!='계열 밖']
        if any(t not in fids for t in targets):raise ValueError('unknown membership family')
        st='excluded' if row.get('family')=='계열 밖' else 'unresolved' if not row.get('family') or row.get('pending_director') or row.get('conflict') else 'exact'
        cs=[candidate(t,sc,[sr],'Historical family membership; not product selection') for t in targets]
        mr=mapping([sr],'membership',st,sc,cs,targets if st=='exact' else [],reason='Historical family membership; pending/conflict/null retained',legacy=row)
        entity_by_id[ref]['family_mapping_refs'].append(mr)
        rowindex.append({'category':'product_family','source_refs':[sr],'native_id':row['ledger_id'],'entity_refs':[ref],'mapping_refs':[mr],'claim_refs':[]})
        mapledger.append({'source_ref':sr,'mapping_refs':[mr],'purpose':'membership','state':st,'legacy':row})
    for i,row in enumerate(families['out_of_family']):
        ref='product:'+row['ledger_id'];sr=gs('step2-families.json','/out_of_family/'+str(i));mr=mapping([sr],'membership','excluded',pscopes[ref],reason=row['basis']);entity_by_id[ref]['family_mapping_refs'].append(mr)
    safety=[];source_safety={};collision=[];normalizer={'id':'batch1-key-normalize','version':'1','code_sha256':sha(HERE/'rules.py')}
    raw_tax=docs['raw21','taxonomy.json']
    # Census from actual raw containment, then exact legacy-ID alignment in approved oracle.
    rawrows=[]
    for i,mod in enumerate(raw_tax['modality']):
        for j,sub in enumerate(mod.get('subcategories',[])):
            for k,row in enumerate(sub.get('items',[])):rawrows.append((f'/modality/{i}/subcategories/{j}/items/{k}',row,'extracted'))
        for j,row in enumerate(mod.get('products',[])):rawrows.append((f'/modality/{i}/products/{j}',row,'taxonomy_products'))
    current_lookup={(key,row['id']):(i,row) for key in ['extracted','taxonomy_products'] for i,row in enumerate(step5[key])}
    for rawptr,rawrow,kind in rawrows:
        i,row=current_lookup[kind,rawrow['id']];cp='/'+kind+'/'+str(i)
        rawsr=src('raw21','taxonomy.json',rawptr);cursr=gs('step5-units.json',cp);refs=[rawsr,cursr]
        own,reason=rules.owner(row,pids,units)
        if own and own.startswith('unit_procedure:'):used_units.add(own.split(':',1)[1])
        qs=[{'axis':'legacy_context','raw':{k:row[k] for k in ['attach','family','sub_family','shown_on','units'] if k in row},'operator':None,'value':None,'source_ref':cursr,'state':'needs_source'}]
        fam=row.get('family') if 'family:'+str(row.get('family')) in fids else None
        sc=scope(refs,own,fam,qs)
        candidates=[]
        if row.get('product') and 'product:'+row['product'] in pids:candidates.append(candidate('product:'+row['product'],sc,[cursr]))
        for uid in row.get('units',[]):
            if uid in units:
                used_units.add(uid);candidates.append(candidate('unit_procedure:'+uid,sc,[cursr],'Historical candidate or multi-owner; never promoted to selected'))
        st='exact' if own else ('compatible_candidate' if reason=='candidate_only' else 'unresolved')
        mi=mapping(refs,'identity',st,sc,candidates,[own] if own else [],reason=reason or 'Explicit single owner verified against product/unit source registry',attachment_state='eligible' if own else 'not_created',attachment_reason=reason)
        rawfields=[];ex=rawrow.get('extracted',{})
        for key,val in ex.get('safety',{}).items():rawfields.append(('safety.'+key,rawptr+'/extracted/safety/'+escape(key),val))
        if 'aftercare' in ex:rawfields.append(('aftercare',rawptr+'/extracted/aftercare',ex['aftercare']))
        counts=Counter(rules.KEY_NORMALIZE.get(k,k) for k,_,_ in rawfields)
        crs=[]
        for field,ptr,val in rawfields:
            sr=src('raw21','taxonomy.json',ptr);pred=rules.KEY_NORMALIZE.get(field,field)
            nm=mapping([sr],'normalization','rule_mapped',sc,reason='Exact dotted-key rename only; raw occurrence and value remain separate',rule=normalizer,raw_field=field,normalized_predicate=pred)
            cr=claim(own,field,val,[sr],sc,[mi,nm],'preparation' if field=='aftercare' else 'safety',counts[pred]>1);crs.append(cr)
            safety.append({'claim_ref':cr,'row_source_ref':rawsr,'legacy_id':rawrow['id'],'raw_pointer':ptr,'raw_field':field,'predicate':pred,'raw_value':val,'leaf_count':leaves(val),'source_refs':[sr],'scope_ref':sc,'mapping_refs':[mi,nm],'attachment_state':'eligible' if own else 'not_created','attachment_reason':reason})
            if own:
                norm('attachment',{'claim_refs':[cr],'target_ref':own,'rule':{'id':'batch1-source-preservation','version':'2'},'witness':[],
                                   'scope_ref':sc,'application_state':'unknown','resolution_ref':None,'unknown_reasons':['source_preservation_only','clinical_application_unreviewed']})
        source_safety[kind,row['id']]=[v for v in safety if v['row_source_ref']==rawsr]
        entry={'category':'safety','source_refs':refs,'native_id':rawrow['id'],'raw_pointer':rawptr,'current_pointer':cp,
               'entity_refs':[own] if own else [],'mapping_refs':[mi],'claim_refs':crs,'attachment_state':'eligible' if own else 'not_created','attachment_reason':reason}
        rowindex.append(entry)
        mapledger.append({'source_ref':cursr,'mapping_refs':[mi],'purpose':'identity','state':st,'attachment_state':entry['attachment_state'],'attachment_reason':reason,'claim_refs':crs,'source_refs':refs})
        for pred,n in counts.items():
            if n>1:
                fs=[v for v in source_safety[kind,row['id']] if v['predicate']==pred]
                before=row['source_text'][pred]
                collision.append({'legacy_id':row['id'],'current_pointer':cp,'predicate':pred,'before':before,'before_leaves':leaves(before),'after_fields':fs,'after_leaves':sum(v['leaf_count'] for v in fs),'recovered_leaves':sum(v['leaf_count'] for v in fs)-leaves(before)})
    for tid in sorted(used_tech):
        i,node=techniques[tid];sr=gs('step4-techniques.json','/nodes/'+str(i));graph['registry'].append({'id':'technique:'+tid,'type':'technique','native_id':tid,'source_refs':[sr],'limited_registry':True})
    for uid in sorted(used_units):
        i=next(i for i,u in enumerate(step5['units']) if u['id']==uid);sr=gs('step5-units.json','/units/'+str(i));graph['registry'].append({'id':'unit_procedure:'+uid,'type':'unit_procedure','native_id':uid,'source_refs':[sr],'limited_registry':True})
    overrides=[]
    for group in ['units','product_links']:
        for i,row in enumerate(step5[group]):
            for j,ov in enumerate(row.get('side_effect_override',[])):
                ptr=f'/{group}/{i}/side_effect_override/{j}';sr=gs('step5-units.json',ptr)
                kind='taxonomy_products' if ov['source']=='taxonomy products extracted' else 'extracted'
                fs=[f for f in source_safety.get((kind,ov['id']),[]) if f['raw_field'].startswith('safety.')]
                if not fs:raise ValueError('override without raw safety: '+ptr)
                after=defaultdict(list)
                for f in fs:after[f['predicate'][7:]].append({'claim_ref':f['claim_ref'],'source_refs':f['source_refs'],'raw_field':f['raw_field'],'raw_pointer':f['raw_pointer'],'raw_value':f['raw_value']})
                overrides.append({'source_ref':sr,'source_pointer':ptr,'group':group,'target_ref':('unit_procedure:'+row['id']) if group=='units' else 'product:'+row['product'],
                                  'legacy':ov,'before':ov['values'],'after':dict(after),'claim_refs':[f['claim_ref'] for f in fs],
                                  'scope_refs':sorted({f['scope_ref'] for f in fs}),'application_state':'unknown',
                                  'decision_ref':None,'decision_reason':'Historical raw provenance retained; no new approval'})
    baseline=load(BASE/'silver-pilot-closeout-review/coverage.json'); coverage=[]
    graph_types={'product':'products','family':'families','snapshot':'snapshots','source_record':'source_records','scope':'scopes','claim':'claims','mapping':'mappings','decision':'decisions','attachment':'attachments'}
    for bf in baseline['fields']:
        key=bf['proposed'];typ,field=key.split('.',1);contract=next((x for x in fields if x['proposed']==key),None)
        instances=graph.get(graph_types.get(typ,''),[]) if contract else []
        vals=[r[field] for r in instances if field in r]
        batch='out_of_batch' if not contract else ('needs_design' if key=='family.subfamilies' else 'limited_registry' if key=='family.technique_defaults' else 'source_preserved_no_approval' if typ=='decision' else 'implemented')
        locs=contract.get('exact_current_locators',[]) if contract else []
        coverage.append({'proposed':key,'baseline_status':bf['status'],'batch_status':batch,'proposed_contract':bf['proposed_contract'],
                         'source_count':len(locs),'typed_count':0 if batch in ['out_of_batch','needs_design'] else len(vals),
                         'raw_count':len(locs),'empty_count':sum(v is None or v==[] or v=={} or v=='' for v in vals),
                         'oracle':contract['oracle'] if contract else None,'result':'pending_independent_validation' if contract else 'unchanged',
                         'transform':contract['transform'] if contract else None})
    def raw_census(value):
        c=Counter()
        if isinstance(value,dict):
            if not value:c['empty_object']+=1
            for v in value.values():c.update(raw_census(v))
        elif isinstance(value,list):
            if not value:c['empty_array']+=1
            for v in value:c.update(raw_census(v))
        elif value is None:c['null']+=1
        elif value is False:c['false']+=1
        elif value=='':c['empty_string']+=1
        else:c['scalar_value']+=1
        return c
    actual_counts={'products':len(graph['products']),'active':sum(x['active'] is True for x in products['items']),
                   'inactive':sum(x['active'] is False for x in products['items']),'families':len(graph['families']),
                   'product_family':len(families['product_family']),'safety_rows':len(rawrows),'safety_fields':len(safety),
                   'safety_leaves':sum(x['leaf_count'] for x in safety),'override_items':len(overrides),
                   'eligible_fields':sum(x['attachment_state']=='eligible' for x in safety),'not_created_fields':sum(x['attachment_state']=='not_created' for x in safety),
                   'not_created_reasons':dict(Counter(x['attachment_reason'] for x in safety if x['attachment_state']=='not_created')),
                   'registry_units':len(used_units),'registry_techniques':len(used_tech),
                   'raw_state_census':dict(raw_census({'products':products['items'],'families':families['families'],'mapping_rows':families['product_family'],'safety_raw':[x[1].get('extracted',{}) for x in rawrows]})),
                   'missing_fields':dict(Counter(f['field'] for f in graph['field_states'] if f['raw_state']=='missing'))}
    schema={'version':SCHEMA,'field_contract_sha256':sha(field_contract),'fields':[{k:f[k] for k in ['proposed','proposed_contract','transform','oracle','source_selectors','field_state_contract']} for f in fields],
            'field_types':load(HERE/'type-contract.json')['fields'],
            'extensions':{'snapshot.source_kind':['raw_snapshot','research','decision','generated','audit'],
                          'text_source':{'media_type':'text/plain','pointer':'','source_lines':'inclusive decoded UTF-8 lines; full byte hash'},
                          'source_record':['domain','collection','logical_file_key','media_type','source_sha256'],
                          'exceptions':['family.subfamilies=[]+needs_design','nullable mapping.rule+reason','nullable claim.subject_ref+mapping','collection version null+reason','decision approval never synthesized','unit/technique limited registry']},
            'normalized_id':'prefix+sha256([record_schema_version,mapping_rule_revision,payload_without_id_and_type])',
            'dependency_order':['snapshot','source_record','entity/registry','scope','mapping','claim','decision','attachment'],
            'clinical_approval':False}
    refs={'version':SCHEMA,'contracts':{
        'entity.aliases.source_ref':{'target':['source_record'],'nullable':False,'min':1,'max':1},
        'product.company_roles.claim_ref':{'target':['claim'],'nullable':False,'min':1,'max':1},
        'product.line_memberships.parent_product_ref':{'target':['product'],'nullable':False,'min':1,'max':1},
        'product.line_memberships.decision_ref':{'target':['decision'],'nullable':True},
        'product.continuity.merged_from':{'target':['product'],'min':0,'unique':True},
        'product.continuity.merged_into':{'target':['product'],'nullable':True},
        'product.continuity.split_from':{'target':['product'],'min':0,'unique':True},
        'family.technique_defaults.claim_ref':{'target':['claim'],'nullable':False},
        'family.technique_defaults.decision_ref':{'target':['decision'],'nullable':True},
        'scope.axes.*.raw_refs':{'target':['source_record'],'min':1,'unique':True},
        'scope.axes.*.included/excluded':{'target':'axis-typed entity refs when value_kind=entity_refs','min':0,'unique':True},
        'scope.statement_qualifiers.source_ref':{'target':['source_record'],'nullable':False},
        'scope.conflicts.source_ref':{'target':['source_record'],'nullable':False},
        'mapping.candidates.scope_ref':{'target':['scope'],'nullable':False},
        'mapping.candidates.raw_refs':{'target':['source_record'],'min':1,'unique':True},
        'mapping.decision_refs':{'target':['decision'],'min':0,'unique':True},
        'field_states.owner_ref':{'target':['product','family','source_record','claim','mapping','scope','attachment','snapshot'],'nullable':False},
        'field_states.raw_refs':{'target':['source_record'],'min':1,'unique':True},
        'source_record.snapshot_ref':{'target':['snapshot'],'nullable':False,'min':1,'max':1},
        'source_record.parent_ref':{'target':['source_record'],'nullable':True,'min':0,'max':1},
        'source_record.continuity_ref':{'target':['source_record'],'nullable':True,'min':0,'max':1},
        '*.source_refs':{'target':['source_record'],'nullable':False,'min':1,'unique':True},
        'entity.decision_refs':{'target':['decision'],'min':0,'unique':True},
        'product.family_mapping_refs':{'target':['mapping'],'min':0,'unique':True},
        'family.deferred_refs':{'target':['mapping'],'min':0,'unique':True},
        'entity.*claim_refs':{'target':['claim'],'min':0,'unique':True},
        'claim.subject_ref':{'target':['product','family','unit_procedure'],'nullable':True,'min':0,'max':1},
        'claim.scope_ref':{'target':['scope'],'nullable':False,'min':1,'max':1},
        'claim.mapping_refs':{'target':['mapping'],'min':1,'unique':True},
        'claim.variant.of':{'target':['claim'],'nullable':True},
        'mapping.scope_ref':{'target':['scope'],'nullable':False},
        'mapping.candidates.target_ref':{'target':['product','family','unit_procedure'],'nullable':True,'null_requires':['raw_refs','reason']},
        'mapping.selected_refs':{'target':['product','family','unit_procedure'],'min':0,'unique':True},
        'decision.target_refs':{'target':['product','family'],'min':1,'unique':True},
        'decision.supersedes':{'target':['decision'],'min':0,'unique':True},
        'attachment.claim_refs':{'target':['claim'],'min':1,'unique':True},
        'attachment.target_ref':{'target':['product','family','unit_procedure'],'nullable':False},
        'attachment.scope_ref':{'target':['scope'],'nullable':False},
        'attachment.resolution_ref':{'target':['resolution'],'nullable':True},
        'scope.container_scope_ref':{'target':['scope'],'nullable':True},
        'family.technique_defaults.technique_ref':{'target':['technique'],'nullable':False}}}
    mapledger=[{'mapping_ref':m['id'],'mapping_refs':[m['id']],'source_refs':m['source_refs'],'purpose':m['purpose'],'state':m['state'],'candidates':m['candidates'],'selected_refs':m['selected_refs'],'rule':m['rule'],'reason':m['reason'],'scope_ref':m['scope_ref'],'decision_refs':m['decision_refs'],'attachment_state':m.get('attachment_state'),'attachment_reason':m.get('attachment_reason'),'claim_refs':[c['id'] for c in graph['claims'] if m['id'] in c['mapping_refs']]} for m in graph['mappings']]
    exports={'input-manifest.json':manifest,'schema.json':schema,'ref-contract.json':refs,'rule-manifest.json':{**rule_payload,'mapping_rule_revision':revision},
             'records.json':graph,'source-row-index.json':rowindex,'identity-ledger.json':identity,'mapping-ledger.json':mapledger,
             'safety-claims.json':{'derived_from':'records.json#/claims; safety/aftercare subset','fields':safety},
             'override-projection.json':overrides,'coverage.json':{'denominator':247,'in_scope':84,'fields':coverage,'core_extensions_separate':True},
             'source-diff.json':{'counts':actual_counts,'collisions':collision,'source_mutations':0,'clinical_approvals':0,'audit_basis':audit_sidecar},
             'audit-sidecar.json':audit_sidecar}
    for name,value in exports.items():write(out/name,value)
    output_manifest={'schema_version':SCHEMA,'mapping_rule_revision':revision,'input_manifest_sha256':sha(inputs),
                     'command':'python3 silver-batch1-migration/build.py --inputs contract-fix/input-manifest.v2.json --field-contract field-contract.json --output silver-batch1-candidate',
                     'files':[{'file':name,'sha256':sha(out/name),'bytes':(out/name).stat().st_size} for name in sorted(exports)]}
    write(out/'output-manifest.json',output_manifest)
    write(out/'run-metadata.json',{'deterministic_payload':False,'physical_read_locators':[{'domain':d,'logical_file_key':k,'actual_file':v} for (d,k),v in sorted(locators.items())],'source_of_manifest':str(Path(inputs).resolve())})
    return actual_counts

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',required=True);p.add_argument('--field-contract',required=True);p.add_argument('--output',required=True);p.add_argument('--locator-root')
    a=p.parse_args()
    try:print(canonical(build(a.inputs,a.field_contract,a.output,a.locator_root)).decode())
    except (ValueError,KeyError,TypeError,OSError) as e:print('BUILD FAILED: '+str(e),file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
