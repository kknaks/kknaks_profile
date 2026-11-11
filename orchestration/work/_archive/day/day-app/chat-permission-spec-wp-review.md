# 리뷰 리포트 — day-app 채팅 진입 권한 문장(SPEC-003 · 004) + WP v8 W1 / doc · 좁은 검수 (2026-11-10)

- 대상:
  - 스펙 트리 HEAD `b1260dd2` 위 미커밋 — M `spec-003-mobile-app.md`(U-1 · §3 SSE · 케이스 매트릭스 403 · A-1) · M `spec-004-internal-chat.md`(C-A1)
  - profile `delivery-request-v8.json`(deps[2] · deps[17])
- 근거:
  - `chat-permission-spec-wp-fix-report.md` · `chat-mobile-code-report.md` §3 · §7
  - 사용자 확정 「채팅 상대는 같은 병원 활성 직원」 · `board` 무관(`chat-decisions-20261110.md`) · SPEC-004 §3 「권한 · 격리」 · OQ-C1
  - 앞 리뷰 `notification-wp-review.md` W1
  - SPEC-001 `:142` · `:316-320` · `:393`
  - DAY 코드 `b6c034bf` `backend/day/services/sessions.py` `me()` · `still_allowed()`(읽기만)
- 방법:
  - diff 전수 대조 · 서버 `/me` 실제 판정 확인
  - 이전 v8을 복원해 경로 diff · schema/모델 1회 · lint 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 1)

방향은 맞다. 이미 확정된 SPEC-004 정책(board와 묶지 않는 같은 병원 활성 직원 채팅)에 SPEC-003의 「권한 없음」 문장을 맞췄고, 새 정책 · 사용자 승인 요구는 없다.
- U-1 · §3 SSE · 매트릭스 403 · A-1 · C-A1: board 권한만 없는 `/me` 200 세션 → 「시술현황」 메뉴 본문 자리에만 기존 원문 안내를 띄우고, 셸 · 채팅 · 설정 진입은 유지한다.
- 권한 확대 · 우회는 0이다:
  - board API · 판 스트림 · 고객 정보 · 통역(U-15 · A-14b = board view 그대로)은 열지 않는다.
  - 권한 키 · auth code · API · 새 글자는 0이다.
  - 세션 401 처리 · 세션 묶음 지우는 때는 무변경이다.
- WP v8 W1은 해소됐다. 다른 v8 내용은 회귀가 없다.

WARN 1건은 새 문장이 `/me` 401/403 사례로 든 예가 지금 서버 동작과 맞지 않는 것이다.

## FAIL

없음.

## WARN

### W1. U-1 새 문장의 「`/me` 자체가 401 · 403인 경우(… **직원 비활성 · 병원 멤버십 상실** 등)」 — 세션 도중의 비활성/멤버십 상실은 지금 `/me`가 막지 않는다
- 위치: `spec-003-mobile-app.md` U-1 「권한 없음」 줄(새 문장 끝) 「`/me` 자체가 401 · 403인 경우(인증 불가 · 직원 비활성 · 병원 멤버십 상실 등)는 … 기존 인증 실패 · 권한 없음 처리 그대로다(셸 없음 · 채팅 포함 진입 없음)」
- 근거:
  - DAY `sessions.py` `me()`는 세션의 account · hospital · staff 행이 **없을 때만** 401(`session owner is gone`)이다. `staff.is_active` · 멤버십을 다시 보지 않고 200 + `permissions`를 돌려준다.
  - 직원 비활성 403은 SPEC-001 **로그인 때만**이다(`:320` `staff_inactive` · 규칙 12 `:393`).
  - 세션 도중 비활성 직원의 채팅 차단은 SPEC-004 §3 `:272` 「내 staff가 비활성이면 채팅 요청 전부 403」 · 케이스 매트릭스 `:429` 「403 → 토스트 · 채팅 목록 비움」이 맡는다.
- 영향: 문장대로 읽으면 「로그인 중 비활성이 되면 `/me`가 403 → 셸 없음」을 기대하게 된다. 실제로는 `/me` 200 → 셸 · 채팅 탭은 보이고, 채팅 서버가 403으로 막는다. 서버 차단은 있으므로 보안 우회는 아니다. 다만 앱 테스트 · 리뷰가 없는 서버 동작(`/me` 403)을 전제로 판정할 수 있다(검증 불가 문장).
- 최소 정정(새 정책 · 서버 변경 없이 사실만):
  - 괄호 예를 「인증 불가 · 세션 주인 없음(401) · 기존 규칙상 403」으로 줄인다.
  - 「세션 도중 직원 비활성 · 멤버십 상실은 `/me`가 아니라 채팅 서버가 403으로 막는다(DAY-SPEC-004 §3 「내가 활성 직원이 아님」 · 케이스 매트릭스 — 앱은 토스트 · 채팅 목록 비움)」 한 구절을 단다.
  - 매트릭스 403 줄의 「`/me` 자체 403」도 같은 뜻으로 읽히게 둔다.

## 확인 (실측)

| 점검 | 결과 |
|---|---|
| 정책 정합 | SPEC-004 §3 「채팅 쓰기 · 읽기 = 세션만 · board 권한과 묶지 않음」 · C-A1 · OQ-C1(사용자 확정)과 같다. v7 앱이 U-1을 「셸 전체 없음」으로 읽은 것(`chat-mobile-code-report` §3 · §7)을 막는 명확화일 뿐 결과 계약 · 권한 표 변화가 아니다 |
| 범위 | 바뀐 줄 = 003 U-1 · SSE `session_expired` `forbidden` 처리 · 매트릭스 403 · A-1 / 004 C-A1 끝 괄호. 안내 글자 원문(「이 화면을 볼 권한이 없습니다. 관리자에게 문의해 주세요」) · 로그아웃 버튼 · 통역 권한 · 시술현황 동작 · 세션 · API 무변경 |
| SSE `forbidden` | 판 스트림이 `forbidden`이면 시술현황 영역 안내 · 셸 유지 — 서버 `still_allowed`의 권한 회수 → `forbidden`(`sessions.py`)과 맞는 소비 · 세션을 지우지 않는 기존 규칙(`:493`) 그대로 |
| 동결 | spec-000 · 001 · 002 · 005 = git `b1260dd2` blob **4/4 동일** · `git status` = M 003 · M 004만 |
| WP v8 W1 | `$.execution.dependencies[2]` → 「board backend **업무 규칙 · 스냅샷 · 응답**을 고치거나 … (v8 예외 = 호출 · 재호출 커밋 뒤 알림 훅 최소 연결 — code_surface[9] · [10])」 — 앞 리뷰 W1 해소 · 다른 자리와 같은 한정 |
| deps[17] | 「SPEC 원천 갱신 예정 — 권한 문장 명확화가 b1260dd2 위 미커밋 · 코디 커밋 뒤 그 sha로 scope_delta · review_surface[0] · dependencies[15] 갱신 · 미래 hash 미기재」 — 정직 표기(결과 계약 · 권한 키 · API 0) |
| v8 회귀 | 이전 v8(앞 리뷰 복원본) 대비 바뀐 경로 = **deps[2] · deps[17] 2개뿐** · contract_version 8 · L3 · target 5 · baseline 그대로 |
| schema · 모델 | `delivery-request.schema.json` **0 errors** · `DeliveryRequest.model_validate` OK(v8 · L3 · target 5) |

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` → 출력 없음 · exit 0

## 남은 것

- planner: W1 한 구절(U-1 괄호 예 · 세션 도중 비활성 = 채팅 서버 403) → 좁은 재검수.
- 코디: SPEC 커밋 → v8 SPEC 원천 sha 갱신(deps[17]대로) → mobile 워커에 「시술현황 영역만 권한 없음 · 셸/채팅/설정 유지 · 세션 도중 비활성은 채팅 서버 403 처리」 전달. 코드 · 실기기는 미실행(pending)이다.
