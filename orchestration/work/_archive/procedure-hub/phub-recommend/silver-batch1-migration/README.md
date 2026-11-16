# Batch1 inactive candidate migration

Python standard library only. No install, model, network, DB, service, canonical write,
commit, or publication option is present. DATA-001/2, WORK-013, approved manifest v2,
84 field transforms and the original 247-field baseline are fixed inputs.

Run from the profile repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/build.py --inputs orchestration/work/phub-recommend/silver-data-contract-batch1/contract-fix/input-manifest.v2.json --field-contract orchestration/work/phub-recommend/silver-data-contract-batch1/field-contract.json --output orchestration/work/phub-recommend/silver-batch1-candidate
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/validate.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate --independent-source
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/test_contract.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate
PYTHONDONTWRITEBYTECODE=1 python3 orchestration/work/phub-recommend/silver-batch1-migration/check_reproducible.py --candidate orchestration/work/phub-recommend/silver-batch1-candidate --trials 2 --relocate-inputs
```

The build command intentionally rejects an existing records.json. To reproduce the
existing candidate, use check_reproducible.py or a fresh candidate/tmp/run-N output.
The top-level candidate stays inactive and existing canonical stepN files remain inputs.
During implementation, explicitly reviewed development runs were built under candidate/tmp
and their exports copied into the inactive candidate; this is not an automatic overwrite
or source rebaseline path. Temporary files are removed after successful checks.

`--locator-root ROOT` reads each approved member at
`ROOT/<domain>/<logical_file_key>` while retaining the original manifest bytes,
logical identity and locator declaration in deterministic outputs. Actual read paths
are recorded separately in run-metadata.json. Hash or bytes mismatch fails closed;
a different input manifest or field contract fails before building.

`type-contract.json` is the declarative exact nested type contract for all 84 fields;
schema.json includes it verbatim alongside the original proposed type/required/empty
semantics, explicit DATA-001 exceptions, transforms, selectors and independent oracles.
`expected-inputs.json` pins contracts/oracles. `expected-rules.json` pins the actual new
builder/rules/transport/machine-schema bytes independently of candidate output. The
validator imports transport utilities only; it never imports builder/rules or uses
builder transformations as source truth. It reads source files and fixed rules directly.

Snapshots are per fixed collection. Audit-only design/coverage/legacy scripts have their
own snapshot and audit sidecar; they never enter semantic source_refs. A normalized ID
hashes `[schema_version, mapping_rule_revision, payload_without_id_and_type]`. Raw source
refs are retained in the payload. Native entity IDs retain namespace+original native ID.
No source entity key is guessed from a display name or an ID's appearance.

All 63 non-audit file roots are preserved, including UTF-8 text roots with source line
range and original byte hash. Exact-ID historical rows retain their own occurrences.
Containment parent links are actual same-file JSON parents. No historical continuity or
approval is synthesized. Collection versions stay null+reason; file version metadata
retains integer/string/null/missing distinctions from the immutable manifest.

Safety/aftercare has one claim per original raw field, including multiple raw fields
sharing a normalized predicate. Values, duplicate/order/empty/null/false semantics remain
unchanged. normalized_value is null. Existing override projections retain all raw metadata
and before values, with separate original-field arrays for the after projection.
Source owner verification requires an explicit existing product or a single unit with
matching ledger source evidence. Candidate, ownerless, multiple-owner and out-of-batch
claims stay preserved without attachment. Attachments use batch1-source-preservation/2,
subject=target, same source scope, unknown application, no witness, no resolution.

`decisions=[]` is deliberate: historical approval/gate/open/name-basis artifacts and
citations are preserved as original roots/claims, while no new approval authority record
is synthesized. decision field coverage is `source_preserved_no_approval`, with zero typed
instances. Family subfamilies stays []+needs_design; technique/unit registries retain only
referenced IDs and are not full migrations. No purpose/subfamily IDs are issued.

output-manifest.json covers the deterministic build exports. validation.json,
counterexamples.json, reproducibility.json, protected manifests and run-metadata.json are
verification/execution sidecars, outside the normalized data-ID payload. The completed
report and verification-manifest identify their final bytes. Coverage has independent
baseline_status and batch_status. A pending_independent_validation result in a build
export refers to validation.json for the executed result; the builder never self-approves.

The counterexample harness recalculates normalized IDs before source/meaning checks and
requires a specific semantic diagnostic with zero normalized-ID failures. Identity trials
separately exercise actual repeated builds/physical reads and in-memory source/audit/schema
lifetime perturbations. No changed-source manifest is approved by a probe. Immutable pilot
regressions use regression-inputs.json (13 referenced source artifacts) and existing fixture
bytes; their case/146-combo/7-note/5-language/duration counts are not new migration counts.

Implementation P0-P4 results do not perform P5 independent candidate review, canonical
transition, clinical review, Gold publication or application activation.
