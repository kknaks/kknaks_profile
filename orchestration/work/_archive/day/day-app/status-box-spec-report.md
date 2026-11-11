# status-box-spec 결과 보고 — 카드 상태 박스 2줄 SPEC · WP v4 입력

## 상태: done (코드 · 서버 · 다른 SPEC · 20-spec.md · 30-work.md · GitHub · 커밋 없음)

## 변경

| 파일 | 내용 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | +35 / −16 (HEAD `cdde456a` 위 미커밋) — 머리 「2026-11-10 개정 ③ — 카드 상태 박스 2줄」(사용자 원문 4개 · 대체 계약 · 범위 밖 · 코드 미반영) |
| profile `delivery-request-v4.json` | v3(승인본과 같은 파일)에서 최소 변경 · contract_version **4** |
| profile `status-box-spec-report.md` | 이 보고서 |
| profile `delivery-request-v3.json` | **보존**(무수정 · v3) |

### SPEC-003 자리

| 자리 | 바꾼 것 |
|---|---|
| 문구 원칙 | 사용자 글자에 「시술 중」 · 「외 {N}개」 추가 |
| Wireframe | 시술 대기 카드 상자를 2줄로 + 상태 예 3개(「시술 중 · 05:24 / KOS-DEMO」 · 「마취 중 · 12:34 / 담당의 미정」 · 「시술 대기 · 마취 완료 20분 / 담당의 미정」 — 값은 예시) |
| U-3 4번 줄 | 「한 줄 상자」 → **모든 상태 2줄**: 1줄 상태(· 시간) / 담당의 · 2줄 시술명. 상태별 1줄 = 「시술 대기」 · 「마취 중 · mm:ss」 · 「시술 대기 · 마취 완료 {N}분」 · 「시술 중 · mm:ss」(진행중 첫 줄 `startedAt` 부터). 시간 = 초 단위 mm:ss · 분 60 넘어도 누적 · 형식 변환만. 담당의 = 기존 규칙(첫 담당의 · 없으면 「담당의 미정」). 시술명 = 그 상태 시술만 · 서버 순서 첫 `title` · 「외 N개」(1개면 생략) · 없으면 2줄 비움 |
| U-3 호출 뒤 카드 | 호출 상태 박스도 같은 2줄 — 1줄 「수락 대기 · mm:ss」 / 호출 대상(담당의 자리 · 「전체 의사」/원장 이름 · OQ-A8) · 2줄 그 호출 시술명. 호출 줄 · 수락 버튼은 그대로 |
| U-8 | 마취 중 한 줄(「HH:MM 시작 · 기준 N분」 + 오른쪽 분) → 상태 박스 1줄 「마취 중 · mm:ss」 · 마취 완료 「시술 대기 · 마취 완료 {N}분」(` - ` → ` · `) · 룸 상세 마취 칸은 범위 밖(OQ-A31) |
| A-28 · A-29 · A-30 | 2줄 · mm:ss · 시술명 외 N개 · 호출 박스 반영(A-29 실물 칸 로컬 day-local 유지) |
| OQ-A21 | 「시술 중 카드 상자」 해소(취소선) · 시술명 집계 대상 기본값 추가 · 담당의/겹침 기본값 그대로 |
| OQ-A30 | 마취 표시 = 상태 박스 2줄(웹 칩 「마취중 mm:ss」 글자는 가져오지 않음) |
| OQ-A31 신규 | 룸 상세 마취 칸 글자 · 룸 머리 방 이름 가운데 정렬(사용자 「기록해」) — 지금 그대로 · 구현 안 함 |

색(연보라 · `long` 빨강 · 시술 중 DAY 주색) · 서버 판정 · `needs` · `canRecall` · 수락 버튼 · 귀가 대기 자리 · 상세 시술 줄 · 룸 머리 · API 변경 없음.

### WP v4 (`delivery-request-v4.json`)

| 칸 | 값 |
|---|---|
| 같음 | idempotency `day/day-app` · #235 · L3 · targets DAY-SPEC-003/001 · baseline `3f57c1af09afa7ce185cd754244c714bf1ec11e5` pending · app/ 만 · 코드 PR #237 · 의존 · 권한 |
| contract_version | 4(v3 승인 + 1) |
| scope_delta | v3 contract `sha256:e688d8a7…` · plan_digest `sha256:701c2a2a…` → v4 사유 · 사용자 원문 4개 결속 · 대체 범위 · 범위 밖 |
| 바뀐 곳 | title · scope_delta · review_surface[0](원천 = cdde456a + 개정 ③ 미커밋) + 1개 · target_delta[9] 대체 표시 + [v4] 1개 · acceptance[0] · A16 · A17 · A18 · phases[3] · verification[0] · open_questions[0] |
| 항목 수 | target_delta 16 · acceptance 27 · review_surface 11 |

## 검증

- `git diff --check` 통과 · `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` **0건**
- v4 JSON: 파싱 OK · jsonschema(delivery-request + delivery-issue execution ref) **0 errors** · `DeliveryRequest.model_validate` **OK**(v4 · L3)
- 옛 글자 잔존: v4 의 「HH:MM 시작」은 scope_delta · A17 의 「대체」 설명에만 · 「마취 한 줄」 0

## 구현 메모 (mobile 용)

- 기존 app/ 미커밋(fix1)의 한 줄 상자 · 「마취 중 · HH:MM 시작 · 기준 N분」 · 「시술 대기 - 마취 완료」를 이 2줄로 바꾼다. 2줄은 상태가 비어도 높이 유지.
- mm:ss = `floor(초/60)` 두 자리 이상 · 초 두 자리 · 시(hour) 단위로 바꾸지 않음(예 75:03). 서버 `now` 보정(U-12).
- 시술명 집계: doing 줄 / 그 호출 `called` 줄 / `done` 아닌 줄 — 서버 순서 첫 값 + 「외 N개」.
- 호출 박스 오른쪽 = 호출 대상 글자(기존 「전체 의사」 · 원장 이름).
- 룸 상세 마취 칸 · 룸 머리 정렬은 손대지 않음.

## 미결

- 시술명 집계 대상 · 호출 박스 오른쪽 = 호출 대상은 사용자 합의를 레이아웃에 옮긴 planner 기본값(OQ-A21) — 리뷰 · 사용자 확인 대상.
- SPEC 개정 ③ 미커밋 — v4 원천 표기 「cdde456a + 개정 ③」 · 코디가 커밋한 exact head 로 결속.
- 다음: 독립 리뷰 → 코디 v4 plan(L3 새 plan_digest 승인 — 사용자 「응 일단 이거 부터 바꾸고 오자」 결속은 코디 몫) → apply → mobile 코드 발주.
