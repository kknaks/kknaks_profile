"""Exhaustive record-reference paths. * traverses arrays or axis/condition objects.
Cardinalities are in schema.json; optional means nullable, not dangling.
"""
REFS={
'source_records':{'snapshot_ref':'snapshots','parent_ref':'source_records','continuity_ref':'source_records'},
'entities':{'source_refs.*':'source_records'},
'scopes':{'container_scope_ref':'scopes','axes.*.raw_refs.*':'source_records','statement_qualifiers.*.source_ref':'source_records','conflicts.*.source_ref':'source_records'},
'claims':{'subject_ref':'entities','source_refs.*':'source_records','scope_ref':'scopes','mapping_refs.*':'mappings','variant.of':'claims','override.claim_refs.*':'claims','override.scope_ref':'scopes','override.decision_ref':'decisions','override.source_record_ref':'source_records','override.override_of':'entities'},
'mappings':{'source_refs.*':'source_records','scope_ref':'scopes','candidates.*.target_ref':'entities','candidates.*.scope_ref':'scopes','selected_refs.*':'entities','decision_refs.*':'decisions'},
'relation_claims':{'claim_ref':'claims','members.*.mapping_ref':'mappings','members.*.source_ref':'source_records','parent_claim_ref':'claims','derivation.input_refs.*':'claims','field_conditions.*.scope_ref':'scopes','field_conditions.*.raw_ref':'source_records','field_conditions.*.options.*.scope_ref':'scopes','field_conditions.*.options.*.raw_ref':'source_records','existing_expansions.*.source_record_ref':'source_records','existing_expansions.*.source_occurrence_refs.*':'source_records','source_record_ref':'source_records'},
'notes':{'source_record_ref':'source_records','source_refs.*':'source_records','claim_refs.*':'claims','existing_claim_refs.*.source_record_ref':'source_records','relation_ref':'relation_claims'},
'decisions':{'target_refs.*':'claims','supersedes.*':'decisions','source_refs.*':'source_records'},
'resolutions':{'input_claim_refs.*':'claims','scope_ref':'scopes','policy.decision_ref':'decisions','output.selected_claim_ref':'claims','output.existing_slot_ref':'source_records','alternatives.*':'claims'},
'attachments':{'claim_refs.*':'claims','target_ref':'entities','witness.*.mapping_ref':'mappings','witness.*.edge_ref':'relation_claims','witness.*.component_ref':'source_records','witness.*.source_ref':'source_records','scope_ref':'scopes','resolution_ref':'resolutions'},
'legacy_aliases':{'snapshot_ref':'snapshots','selected_refs.*':'entities','targets.*.source_record_ref':'source_records','targets.*.target_ref':'entities','targets.*.scope_ref':'scopes'},
'cases':{**{k+'.*':v for k,v in [('source_refs','source_records'),('silver_refs','source_records'),('claim_refs','claims'),('relation_refs','relation_claims'),('mapping_refs','mappings'),('scope_refs','scopes'),('attachment_refs','attachments'),('note_refs','notes')]}}}

# Reviewed declaration; never derive expected values from builder output.
ATTACHMENT_RULE={'id': 'pilot-preserve-source', 'version': '1', 'implementation_file': 'build.py', 'implementation_sha256': '6ac8f07c83c4a069f031c7f89788626e01c621cbad13d854e3c62599eb924028', 'contract_file': 'contract.md', 'contract_sha256': 'a191739b17fe4d6b5809aa6d1d565f60c14d1436d2828bb8228d89dae4af47a4', 'semantics': 'source_subject_same_scope_unknown_empty_witness_duration_resolution_only'}
