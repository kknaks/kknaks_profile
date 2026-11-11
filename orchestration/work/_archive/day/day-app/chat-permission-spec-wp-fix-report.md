# chat-permission-spec-wp-fix 결과 보고 — 채팅 진입 권한 문장 명확화 + WP v8 W1

## 상태: done (SPEC working tree 미커밋 · v8 JSON 제자리 · 코드 · GitHub · 커밋 0)

배경: SPEC-003 U-1 「board 권한 없으면 시술 현황 대신 권한 없음」을 앱이 「셸 전체 없음」으로 해석 → board 권한 없는 활성 직원이 채팅 탭에 못 들어감(chat-mobile-code-report §3 · §7 질문 1). 정본 = 사용자 「채팅 상대는 같은 병원 활성 직원」(board 권한과 묶지 않음) · SPEC-004 §3 · C-A1 · OQ-C1. 정책을 새로 정하지 않고 003 적용 범위만 명확화(v7 구현 권한 해석 정정 · 새 결과 계약 아님).

## SPEC 변경 (base b1260dd2)
| 위치 | before → after |
|---|---|
| 003 U-1 :182 권한 없음 | 「시술 현황 대신 권한 없음 안내 + 로그아웃」 → **「시술현황」 메뉴 본문 자리에** 같은 안내(문구 원문 그대로) · 시술현황 영역에만 적용 · `/me` 200 활성 직원 세션 = 셸(4메뉴 · 머리) · 채팅(SPEC-004) · 설정 진입 유지 · board API · 판 스트림 · 고객 정보 · 통역은 안 엶 · `/me` 자체 401/403(인증 불가 · 비활성 · 멤버십 상실)은 기존 인증 실패 · 권한 없음 처리 그대로(셸 없음) |
| 003 §3 SSE :326 | `forbidden` = 권한 없음 안내 → **시술현황 영역** 권한 없음 안내(셸 · 채팅 · 설정 유지) |
| 003 케이스 매트릭스 403 :569 | 「/me · SSE 면 권한 없음 안내」 → 판 SSE · board 조회 = 시술현황 영역 안내 · `/me` 자체 403 = 기존 안내(셸 없음) |
| 003 A-1 :697 | 「권한 행 없는 직무는 권한 없음 안내」 → 시술현황 영역에 안내 · 셸 · 채팅 · 설정 진입 유지(`/me` 200 활성 직원 · SPEC-004 C-A1) |
| 004 C-A1 :530 | 「board 권한 없는 직원도 채팅 가능」 + (앱 셸 · 「채팅」 탭 진입 포함 — SPEC-003 U-1 권한 없음은 시술현황 영역만) |

불변: 권한 없음 글자 원문 · 권한 표/키 · board 권한 확대 0 · 통역 = board view(U-15 · A-14b 무변경) · 시술현황 동작 · 세션/인증(U-1 다른 줄 · :493 지우는 때) · API/서버 code 0 · 새 UI 문구 0 · 새 OQ 0. SPEC-000/001/002/005 · index/coverage 무변경(hash = b1260dd2 확인).

## WP v8 JSON (version 8 유지 · scope 확대 0 · v7 입력 무변경)
- `execution.dependencies[2]` (W1): 「board backend 를 고치거나 …」 → 「board backend **업무 규칙 · 스냅샷 · 응답**을 고치거나 … (v8 예외 = 호출 · 재호출 커밋 뒤 알림 훅 최소 연결 — code_surface[9] · [10])」.
- `execution.dependencies[17]` 추가(정직 연결): 위 SPEC 권한 문장 명확화가 b1260dd2 위 미커밋 → 코디 커밋 뒤 그 sha 로 SPEC 원천 표기(scope_delta · review_surface[0] · dependencies[15]) 갱신 대상 · 미래 hash 미기재.
- 경로 diff 실측: 위 2곳만(수정 전 사본 scratchpad `v8-before-permfix.json`).

## 검증 (최종 1회)
- jsonschema **0 errors** · `DeliveryRequest.model_validate` OK(v8 · L3 · target 5)
- `lint-pipeline.py --strict` exit 0 · **0 error, 263 warning** · products/day 0건 · `git diff --check` OK · status = M 003 · M 004
- 코드 · 앱 · 서버 실행 0

## 다음
코디: 독립 검수 → SPEC 커밋 → v8 JSON SPEC 원천 sha 갱신 → 승인된 patch 를 mobile 워커에 알림(셸 · 채팅 진입 유지 · 시술현황 영역만 권한 없음).
