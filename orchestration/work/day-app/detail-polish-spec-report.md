# detail-polish-spec 결과 보고 — 룸 상세 다듬기 SPEC 개정 ④ · WP v5 입력

## 상태: done (코드 · 서버 · GitHub · 커밋 · 다른 SPEC · 20-spec.md · 30-work.md 변경 없음)

## 변경

| 파일 | 내용 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | +32 / −12 (HEAD `d6d961e9` 위 미커밋) |
| profile `delivery-request-v5.json` | v4(승인본과 같은 파일)에서 최소 변경 · contract_version **5** |
| profile `detail-polish-spec-report.md` | 이 보고서 |
| `delivery-request-v4.json` | 보존(무수정) |

### SPEC-003 개정 ④

| 자리 | 바꾼 것 |
|---|---|
| 머리 개정 ④ | 사용자 원문 · 범위(룸 상세만) · 바꾸지 않는 것 · 코드 미반영(47be2cb0 = 개정 ③ 까지) |
| Wireframe | 룸 상세 머리 「< 시술현황 {방}(가운데)」 |
| U-4 내비게이션 줄 | 방 이름 = **헤더 전체 폭 정가운데**(왼쪽 버튼 뺀 영역 가운데 아님) · 긴 이름 말줄임 · 뒤로 버튼 영역/접근성 그대로 · 다른 머리 무변경 |
| U-4 1번 호출 강조 상자 | **미수락 `called` 줄이 남은 호출만** · 전부 수락된 호출 상자 숨김 · 부분 수락 · 여러 호출 중 미수락 남은 상자 유지 |
| U-4 4번 · U-7 | 시술 행 5상태 + ASCII(준비중 · 호출 중 · 수락 뒤 · 진행중 · 완료) — 상태 배지 · 행 [수락] · 호출 대상/경과 글자 없음 · 호출 중 비활성 [시작] · 진행중 연한 DAY 배경 · 큰 mm:ss · 담당의 · HH:MM 시작 / [종료] [⋮] · 완료 회색 「완료 N분」(시각 없으면 「완료」) / [⋮] · 그 행 값만 |
| U-7 활성 | 와이어 「기본 비활성」은 예시 · **서버 `canStart` 그대로**(준비중 KOS 담당의 있으면 true 가능 — 막지 않음) · 수락 뒤 false 면 비활성 · ⋮ = `canUndoStart` / `canUndoFinish` · 확인 창 · 원문 그대로 · `board` edit 일 때만 |
| U-6 들어오는 곳 | 「시술 카드 [수락]」 제거 · 상단 호출 강조 상자로 모음 문장 |
| A-31 | 머리 가운데 · 호출 상자 미수락만 · 시술 행 5상태 |
| A-39 신규 | 회귀 — 수락 경로 · 부분 수락 상자 유지 · can* 활성 그대로 · 보기만 직무 새 조작 없음 · 목록 카드 · 4메뉴 · 상세 마취 칸 · 통역 · 토스트 · API 무변경 |
| OQ-A31 | 룸 머리 부분 해소(취소선) · 상세 마취 칸만 남음(지금 그대로) |

목록 카드 2줄 · 4메뉴 · DAY 색 · 통역 · TW · 토스트 · 세션 · 환경 · API · needs · canRecall · 마취(상세 마취 칸 포함) 무변경.

### WP v5

| 칸 | 값 |
|---|---|
| 같음 | `day/day-app` · #235 · L3 누적 · targets · baseline `3f57c1af09afa7ce185cd754244c714bf1ec11e5` pending · app/ 만 · 코드 PR #237 하나 · 머지 마지막 지시 |
| contract_version | 5 |
| scope_delta | v4 contract `sha256:775e4f0a…` · plan_digest `sha256:60de61f5…` · 코드 head 47be2cb0 → v5 · 사용자 원문 2개 · 바뀐 계약 ①②③ · 무변경 목록 |
| 바뀐 곳 | title · scope_delta · review_surface[0](원천 = d6d961e9 + 개정 ④ 미커밋) + 1개 · target_delta + [v5] 1개 · acceptance[0] · A19 · **A27 신규** · phases[4] · verification[0] · open_questions[0] |
| 항목 수 | target_delta 17 · acceptance 28 · review_surface 12 |

## 검증 (각 1회)

- `git diff --check` 통과 · `lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` 0건
- v5 JSON parse · jsonschema **0 errors** · `DeliveryRequest.model_validate` OK(v5 · L3)

## 구현 메모 (mobile 용 · 코드 읽기만 근거)

- 머리: `DetailHeader(trailing: roomTitle)` 를 전체 폭 가운데 정렬로(뒤로 버튼과 겹치면 말줄임).
- 호출 상자: `_body` 의 `openCalls(card)` 중 `oc.waiting` 만 `_callBox`.
- `_taskCard`: `called` 분기의 [수락] 제거 → `called` 도 [시작](서버 `canStart` · 실제 false) · `sub` 의 호출 대상/경과 제거 · 상태 칩 제거 · 진행중 큰 경과 = `elapsedMmss`(분 누적 · 기존 `Ticking`) — 기존 `clock`(h:mm:ss) 아님 · 완료 「완료 {spanMin}」(빈 값이면 「완료」).

## 미결

- 개정 ④ 미커밋 — v5 원천 「d6d961e9 + 개정 ④」 · 코디 커밋 head 로 결속.
- 다음: 독립 문서 리뷰 → v5 plan · L3 승인 → apply → mobile 발주.
