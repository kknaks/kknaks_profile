# 결정 카드 아티팩트 구현·검증 보고

Task `task_5a08eb7c41eb` · Dispatch `ctx_f9de64debc75` · 2026-11-03

**미부착 원문 62행 / 152필드의 오프라인 결정 UI와 JSON 수출입 형식을 작성했습니다. 원장·실버·candidate 변경 및 결정 반영은 0건입니다. P5 최종 FAIL을 반영해 candidate 미승인·검증기 보완 중으로 표시했습니다.**

## 결과와 분모

| 이유 | 원문 행 | 원문 필드 | UI 처리 권고 |
|---|---:|---:|---|
| candidate_only | 19 | 49 | 원장 관계와 범위를 확인 |
| out_of_batch_entity | 37 | 83 | 후속 이관 묶음 유지 |
| owner_unresolved | 6 | 20 | 단일 대상·원천 관계 확인 |
| 합계 | 62 | 152 | 각 필드는 개별 결정·재설정 |

`DATA-001`, `WORK-013`, 구현 보고와 실제 records/source-row-index/mapping-ledger/identity-ledger/coverage/input/output manifest를 근거로 삼았습니다. records의 안전·사후관리 claim 1,394개에서 attachment의 claim 집합을 빼도 정확히 이 152개이며 subject=null 집합도 같습니다. 미부착 source-row의 occurrence와 field claim/scope는 보존하고 행별 표시만 묶었습니다. 목록 누락·중복 0개입니다.

원문 파일 2개의 bytes hash 및 pointer 값을 직접 읽어 source record 311개와 대조했습니다. 각 필드에는 원문 값, 행 전체 문맥, 실제 출처 file/pointer/hash, 현재 실버 source_text와 존재 여부, candidate 미부착/원문 보존 상태, 기존 매핑과 제한 registry 후보의 이름·출처, claim/scope/raw hash가 있습니다. 모든 필드는 미선택으로 시작합니다. 권고는 이관·원천 관계 처리에 한정하며 새 임상 판단이나 자동 대상 확정을 만들지 않습니다.

## UI와 JSON

검색·이유/작성상태 필터·진행률·필드별 북마크·원문 배열 구조와 접기·모바일/키보드 조작을 구현했습니다. 공통 처리는 명시된 필터 범위의 미선택 수를 확인창에 표시한 뒤 입력하며, 기존 선택·메모를 덮지 않고 작성 중으로 남깁니다.

브라우저 임시 저장은 best-effort로 표시하고 저장 불가도 안내합니다. 명시 JSON 내보내기·불러오기가 있으며 다른 schema/artifact/candidate 판·중복/미등록 카드·원문/claim/scope/source/hash 불일치·허용되지 않은 enum/대상·잘못된 시각/자료형을 거부합니다. 기존 편집과 충돌하면 전체 import를 취소하므로 부분 덮어쓰기하지 않습니다. 원문/source/fingerprint와 카드별 허용 target은 schema에도 고정했고, 중복 ID·기존 편집 충돌은 runtime에서 추가 검사합니다.

작성 중인 선택 없는 메모는 `choice=""`, `decided_at=null`로 백업할 수 있습니다. 선택이 생기면 실제 시각을 기록하고 과거 원장 결정으로 소급하지 않습니다. 연결 제안은 실제 후보에 한정하며 target·근거가 모두 있어야 UI 검토 완료로 표시할 수 있습니다. 새 entity·제품선택·clinical 승인·DB 쓰기는 없습니다.

## 검증 결과

| 검사 | 결과 | 증거 |
|---|---|---|
| 정확한 152집합, 49/83/20, 원문/source/provenance·각 ref·candidate fingerprint | PASS · 5,436검사 | `results/data-validation.json` |
| 실제 file:// Chromium 130 UI | PASS · 21항목 | `results/browser-validation.json` |
| 잘못된 import와 기존 편집 충돌 | 20종 모두 원자적 거부 | 위 JSON의 `negative_imports` |
| JSON Schema 2020-12와 실제 UI export의 일치 | 정상 678 / 변조 거부 16 | `results/schema-validation.json` |
| 원문 한글·구조·390px 모바일/데스크톱 | 화면 직접 확인 | `results/mobile.png`, `desktop.png` |
| 후보 파일 시작/종료 SHA256 | 변경 0 | `results/candidate-start.json`, `candidate-end.json` |
| 외부 요청 / 브라우저 page error | 0 / 0 | `results/browser-validation.json` |

브라우저에서 검색, 이유49/83/20, 미결/작성/검토완료, 개별 선택·실제 시각·이유/메모, 북마크, 저장 복원, 실제 JSON 다운로드·file input 불러오기, 깨끗한 상태 재수입, 공통 처리 취소/확인, 미완성 제안 복원, 실제 후보 선택과 근거 필수, 개별 재설정, 저장 불가 안내를 실행했습니다. UI 변조 검사는 판2종·candidate hash2종·알 수 없는/중복 카드·enum·target·raw/source hash·claim/scope/source refs·시각·이유·자료형·추가 필드·기존 편집 충돌·목록형식·null 결정의 20종입니다.

이 검증은 카드 아티팩트의 원문 대조·목록·동작에 대한 것입니다. candidate 전체 의미 정확성·임상 정확성·원장 승인·P5 PASS를 증명하지 않습니다. 코디네이터가 전달한 [P5 최종 FAIL](../silver-batch1-review/report.md)을 직접 읽고, scope 원문 의미 검증(BR-H1)과 line_memberships 삭제 검출(BR-M1) 공백에 따른 미승인·검증기 보완 중 상태를 화면과 metadata에 반영했습니다. P5는 현재 scope/line 값과 이 152필드의 49/83/20 분류 자체는 정상으로 확인했으며 분류 정정은 없다고 보고했습니다. 이 원문 분류 확인과 데이터판 적용 승인을 구분하며 candidate를 수정하지 않았습니다. P5 보고서의 SHA256도 카드 metadata에 고정했습니다.

## 범위와 인계

작성한 파일은 `silver-decision-cards/` 안에만 있습니다. 외부 CDN/font/library/fetch/import·서버·설치·네트워크·모델 호출·업로드·하위 worker·commit/push/PR은 실행하지 않았습니다. 검증에는 기설치 Playwright/Chromium 및 Ajv를 사용했고 배포 HTML 자체에는 외부 의존성이 없습니다.

인계물은 `index.html`, `cards.json`, `decision-schema.json`, `README.md`, 재생성·검증 스크립트 및 `results/`입니다. `results/ui-export.json`과 거부용 JSON은 테스트가 작성한 자료이며 사용자 결정으로 인계하면 안 됩니다. 실제 사용자 결정은 화면에서 새로 내보내야 합니다.

후속 반영은 사용자 결정 JSON을 고정 candidate 판·카드·schema와 함께 받고, 유일성/refs/hash/후보 범위 및 원장 근거를 별도 검증한 다음 승인된 원장 관계 수정·이관 규칙 수정·clinical 원천 확인·후속 이관 작업으로 나눠 수행해야 합니다. P5 결함 보완 후 독립 재검수 및 후보판 변경 여부를 먼저 확인하며 이 JSON을 selected/subject/attachment/clinical 승인으로 자동 변환하면 안 됩니다. 구체적 절차와 재실행 명령은 [README](README.md)에 있습니다.
