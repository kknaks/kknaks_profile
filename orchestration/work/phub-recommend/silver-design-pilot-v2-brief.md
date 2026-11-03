# 데이터 실물 설계 검증 v2 — ID·typed refs·scope 불변식 보완

## 범위·근거

사용자 승인 reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md 단계3을 계속한다. silver-design-pilot-review/report.md의 H1/H2/H3/M1/M2 및 추가24 probes가 수정 계약이다. pilot 원문보존은 확인됐으나 전체수용 FAIL이다. 기존 v1 pilot/검수/HTML/design는 증거로 보존한다. **새 silver-design-pilot-v2/만** 작성한다. 원장·실버정본·골드·앱 수정과 전체이관 금지.

## 먼저 확정하여 문서화할 v2 계약

contract.md에 아래 정합 규칙과 필드/판 경계를 먼저 작성한 후 구현한다. 원문에서 정할 수 없는 임상판정은 기존 미정 유지. 표현상 불가피한 결정만 근거로 제안하고 막히면 ask한다.

1. H1/M2: 물리경로를 identity에서 제거한다. source domain/collection의 안정적 논리식별자와 논리 file key, 정렬 manifest의 logical file key+full content hash 기반 collection snapshot을 구분한다. raw21 collection과 generated/decision artifact 판은 다른 domain으로 둔다. source occurrence는 collection snapshot+logical file key+pointer에 결합하고 물리경로는 별도 locator다. 같은 bytes라도 다른 logical file/domain은 다른 identity이며 basename/content-only 키로 합치지 않는다. 같은 collection의 단순 디렉터리 이동은 snapshot/occurrence/entity ID 불변이다. 행재정렬은 새 snapshot/occurrence이며 기존 entity ID는 유지한다. record schema_version과 mapping rule 판, immutable source identity, normalized record revision의 수명을 명시한다. 무관 design 문구 변경으로 전체 ID가 바뀌지 않게 한다. 알고리즘 ID를 주장하면 validator도 독립 재계산한다.
2. H2: 모든 ref 경로에 target type/도달성/허용 cardinality를 선언하고 전수 검사한다. scope axes는 entity refs/원문 literal/관계 조건 enum을 축별로 구분하며 임의 string[]로 섞지 않는다. decision target/supersedes, override claim/scope, attachment witness의 mapping/source/edge/component refs 및 source/target 정합을 검사한다. 미지원 witness는 근거가 없으면 unknown이며 가짜 ref로 채우지 않는다. approved_rule/human authority는 실제 원문 evidence와 결합하고 reviewer 없는 가짜 human승인을 거부한다.
3. H3: raw가 맞는 것과 normalized scope/predicate/variant/기간/방향이 맞는 것을 독립 검사한다. 언어 family/container scope 삭제·unknown→explicit·무관 variant parent·predicate변조·원문없는0일 interval·nary directed승격을 거부한다. 같은 의미의 중복 필드가 있으면 단일 정본/파생 관계를 정하고 서로 모순되지 않게 한다. 원문 미기재/unknown/null/explicit_no_required_order 상태를 보존한다.
4. M1: 원문에 확정된 identity mapping 선택은 보존하고 clinical application 승인과 분리한다. exact selected 삭제와 rule id/version/hash 변경을 실제 correspondence/생성기 판 증거에 대조한다. native_id/source_kind도 검증한다. 후보만 exact로 만들거나 exact identity를 모두 hold로 만들어 통과시키지 않는다.

## 구현·검증

v1 실제42사례/combos146/LOSS16잎과 원천미정을 동일하게 포함하는 v2 data/schema/builder/validator/검증용projection을 만든다. v1→v2 ID/field 대응과 기존 pilot refinement/LOSS02 정정을 기록한다. 본 HTML/design 정본은 바꾸지 않는다. 보호입력 manifest는 immutable 원장/실버/설계 입력과 mutable 진행기록을 분리한다. v1 WORK hash 불일치를 소급 수정하지 말고 알려진 코디 진행기록 변경으로 기록한다.

- 원문 snapshot 독립 대조 및 v1 안전16잎·올바른 P9-4·arity146·note7·조건/후보/override/언어/resolution 보존을 재검증한다.
- 기존31 변조와 리뷰 추가24를 v2에서 동등 의미로 재현한다. 모두 관련 진단으로 거부되고 정상 positive가 통과해야 한다. broad KeyError 하나로 참조 실패를 숨기지 말고 ref type/path/target/reason을 구조화한다. 보고에 중복 변조 분모를 구분한다.
- 실제 builder로 원문 디렉터리 이동, 동일 bytes 다른 logical file/domain, 행재정렬·이름변경, schema/rule revision을 시험한다. relocation은 임시 v2 내부 복사본만 쓰며 원본 불변 확인한다.
- 확정된 identity mapping8개는 유지되고 candidate selected0 및 미승인 clinical edge0이 유지되는 positive controls를 둔다. graph가 전부 withheld라는 사실을 usable Gold 검증 완료로 주장하지 않는다. 조회 가능 원문 fact/identity와 적용 승인상태를 별도로 투영한다.
- validator는 builder의 기대출력만 비교하지 않고 원천값·명시 규칙·typed contract를 독립 검사한다. 가짜 임상값/검토자/승인일/새resolution 금지.

## 결과·경계

silver-design-pilot-v2/contract.md, report.md, data/schema/검증코드·결과, migration-map과 보호입력 manifest를 작성한다. scope 밖 원문/실버/decisions/apply/스킬/semantic/HTML/design/v1 pilot/리뷰/스펙/WP/Hub·앱/환경·DB·서버 변경 금지. 네트워크/모델/패키지설치/하위worker/commit/push/PR 금지. 실행은 offline이고 파일복사는 검증용 경로 안에서만 수행한다.

완료 판정은 단계3의 명시범위 검사이며 전체이관/전수임상/Gol d활성화 승인이 아니다. 결과는 H1~H3/M1~M2별 근거와 추가반례 결과, 아직미정·이관전제조건을 보고한다. live Orca preamble대로 inbox/heartbeat를 처리하고 세문장 요약·report-path/files-modified로 worker_done 한 번 후 멈춘다.
