# chat-permission-spec-final-fix 결과 보고 — /me 실제 행동 W1 + v8 execution 에 v7 배선 마감 보존

## 상태: done (SPEC working tree 미커밋 · v8 JSON 제자리 · source 코드 · GitHub · 커밋 0)

## SPEC-003 (W1 — 사실만 · 새 정책/서버 변경 0)
| 위치 | before → after |
|---|---|
| U-1 권한 없음 줄 끝 | 「`/me` 자체가 401 · 403 인 경우(인증 불가 · **직원 비활성 · 병원 멤버십 상실** 등)…」 → 「(인증 불가 · 세션 주인 없음(401) · 기존 규칙상 403)…」 + 「세션 도중 직원 비활성 · 병원 멤버십 상실은 `/me` 가 아니라 채팅 서버가 403 으로 막는다(DAY-SPEC-004 §3 「권한 · 격리」 · 케이스 매트릭스 — 앱은 토스트 · 채팅 목록 비움)」 |
| 케이스 매트릭스 403 줄 | 「`/me` 자체 403 이면 기존 안내(셸 없음)」 → 「`/me` 자체 403(기존 규칙상) …」 + 「세션 도중 비활성 · 멤버십 상실은 채팅 403(DAY-SPEC-004)」 |

근거: DAY `sessions.py me()` = 세션 행 없을 때만 401(staff 활성 · 멤버십 재확인 없음) · 비활성 403 = SPEC-001 로그인 때만 · 세션 도중 = SPEC-004 :272 「내가 활성 직원이 아님 → 채팅 요청 전부 403」 · :429 「403 → 토스트 · 채팅 목록 비움」.
불변: board 없음(/me 200) = 셸 · 채팅 · 설정 진입 유지 · board API/SSE/고객/통역 0 · 안내 원문 · 로그아웃 · 권한 키 · API · `/me` 동작 · 새 UI 문구 0 · SPEC-004 C-A1 보존 · 000/001/002/005 = b1260dd2(4/4).

## v8 JSON execution (contract_version 8 · baseline · target · v7 digest 불변 · v8 알림 내용 유지)
코디 `delivery-request-v7-execution.json`(v7 contract 불변 · execution 만 — v7 backend 리뷰 W2 · W3)의 추가 3 항목을 같은 문장으로 보존:
| key | 변경 |
|---|---|
| `execution.code_surface[5]` | v7 원문(= v8 이 가져온 원문) → v7-execution 원문(+ scripts/deploy/day_vm.py 선택 APNs/Blob 비밀 2개 app.env 연결 · Git 금지 키 · backend/Dockerfile 첨부 디렉터리 소유권 · compose.local 영속 볼륨/권한) |
| `execution.verification[13]` 추가 | v7 배선 마감 검증(선택 비밀 없어도 기존 배포 계약 유지 · Key Vault → app.env 만 · Git 설정이면 거부 · 가짜값 unit/dry-run · disk 영속 마운트 계약 · 실 Vault/배포/기동 0) |
| `execution.rollback[8]` 추가 | 선택 비밀 · disk 지원은 설정 없으면 기존 동작 · migration 0006/0007 forward-only |
| `execution.dependencies[18]` 추가 | 위 3 항목의 출처 · 위치 연결(새 정책 · API 0) |
경로 diff 실측 = 위 4개만(수정 전 사본 scratchpad `v8-before-finalfix.json`).

## 검증 (최종 1회)
- jsonschema **0 errors** · `DeliveryRequest.model_validate` OK(v8 · L3 · target 5)
- lint --strict exit 0 · **0 error, 263 warning** · products/day 0건 · `git diff --check` OK · status = M 003 · M 004
- 코드 · 서버 · 앱 실행 0

## 다음
코디: 재검수 → SPEC 커밋 → v8 SPEC 원천 sha 갱신(deps[17]) → mobile 워커 안내.
