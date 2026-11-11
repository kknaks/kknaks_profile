# tabs-removal-spec 결과 보고 — 시술현황 상단 인박스 탭 제거 SPEC 개정 ⑤ · WP v6 입력

## 상태: done (코드 · 서버 · GitHub 쓰기 · 커밋 · 다른 SPEC · 20-spec.md · 30-work.md 변경 없음)

## 변경
| 파일 | 내용 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | +31 / −30 (HEAD `4a5d4a47` 위 미커밋) |
| profile `delivery-request-v6.json` | v5(승인본과 같은 파일)에서 최소 변경 · contract_version **6** |
| profile `tabs-removal-spec-report.md` | 이 보고서 |
| `delivery-request-v5.json` | 보존(무수정) |

### SPEC-003 개정 ⑤
| 자리 | 바꾼 것 |
|---|---|
| 머리 개정 ⑤ | 사용자 원문 3개 · 결과 계약(본문 = 연결 상태 줄 + 칩 4개 + `cards[]` 만) · 빠진 것 · 수락 경로 · 무변경 목록 · 코드 미반영(4ee33f95 = 개정 ④ 까지) |
| §1 범위 | 넣음 행 「호출 탭에서」 → 「푸시에서」 · 「호출 · 시술 완료 목록」 삭제 / 뺌 행 추가(인박스 탭 · 호출 탭 목록 · 시술 완료 목록 · 검색 — 다른 메뉴 · 숨은 화면 없음 · 서버 계약 그대로) |
| Wireframe | 폰 · 아이패드의 `[현황][호출 n][시술 완료 n]` 줄 삭제 |
| U-2 | 본문 = 연결 상태 줄 · 칩 · 카드만 · 「탭 셋」 문단 삭제 · 웹 인박스 대응 문장은 칩만 가져온다로 · 「「현황」 탭의 거르기 칩」 → 「거르기 칩」 |
| U-3 제목 | 「(「현황」 탭)」 → 「(시술현황 본문)」 |
| U-6 | 들어오는 곳에서 「호출 탭 카드(U-10)」 제거 · 공통 범위 = 목록 · 상세 |
| U-9 | 「「시술 완료」 탭에 「귀가 대기」로 보인다」 → 카드가 목록에서 빠짐 · 시술 완료 목록 없음 · `doneTab` 서버 계약 그대로 |
| U-10 · U-11 | 「1차 앱에서 뺌」 절로 교체 — 옮기지 않음 · 수락은 카드 호출 줄 · 상세 호출 상자 · 푸시 · `calls[]` · `doneTab[]` 정의는 DAY-SPEC-002 소유 그대로(doneTab 은 KOS 실패 토스트 방 · 고객 찾기에만) |
| UX 목록 · S-2 · S-3 · 스냅샷 표 `calls[]` · `doneTab[]` · 화면 목록 · 프로토 차이표 2행 · 닫은 것(수락 동선) | 호출 탭 · 시술 완료 탭 언급을 현재 계약으로 최소 정정(닫은 것 행은 기록 보존 + 「이후 개정 ⑤ 로 없음」) |
| A-1 · A-2 · A-25 · A-33 · A-39 | 호출 · 시술 완료 탭 표현 정정 |
| A-40 신규 | 칩 4개 + 카드만 · 탭/목록/검색 어디에도 없음 · 수락 경로 유지 · 나머지 무변경 |
| OQ-A2 · OQ-A30 | 「현황」 탭 칩 → 시술현황 칩 · 완료 탭 검색은 개정 ⑤ 로 뺌 |

### WP v6
| 칸 | 값 |
|---|---|
| 같음 | `day/day-app` · #235 · L3 누적 · targets · baseline `3f57c1af09afa7ce185cd754244c714bf1ec11e5` pending · app/ 만 · 코드 PR #237 하나 · 머지 마지막 지시 |
| contract_version | 6 |
| scope_delta | v5 contract `sha256:7327938e…` · plan_digest `sha256:fad1184b…` · 코드 head 4ee33f95 → v6 · 사용자 원문 · 코디 확정 안내 결속 · 바뀐/무변경 |
| 바뀐 곳 | title · scope_delta · review_surface[0](원천 4a5d4a47 + 개정 ⑤ 미커밋) · [11] + 1개 · target_delta[1] · [8] · [10] + [v6] 1개 · acceptance[0] · A1 · A2 · A14 · A21 · A27 + **A28 신규** · non_goals[6] · phases[3] · verification[0] |
| 항목 수 | target_delta 18 · acceptance 29 · review_surface 13 |

## 검증 (각 1회)
- `git diff --check` 통과 · `lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` 0건
- v6 JSON parse · jsonschema **0 errors** · `DeliveryRequest.model_validate` OK(v6 · L3)

## 구현 메모 (mobile 용)
- `board_screen.dart` 상단 인박스 탭 · 탭 상태 · 호출 탭 · 시술 완료 탭 본문을 제거하고 칩 + 카드 목록만. 스냅샷 파싱(`calls` · `doneTab`)은 그대로(KOS 실패 토스트 · 카드 호출 줄 순서).

## 미결
- 개정 ⑤ 미커밋 — v6 원천 「4a5d4a47 + 개정 ⑤」 · 코디 커밋 head 로 결속.
- 다음: 독립 문서 리뷰 → v6 plan · L3 승인 → apply → mobile 발주.
