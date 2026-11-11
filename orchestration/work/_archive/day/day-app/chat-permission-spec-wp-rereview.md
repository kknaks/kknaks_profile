# 리뷰 리포트 — day-app 채팅 진입 권한 `/me` 사실 W1 + v8 execution v7 배선 마감 보존 / doc · 최종 재검수 (2026-11-10)

- 대상:
  - 스펙 트리 HEAD `b1260dd2` 위 미커밋 — M `spec-003-mobile-app.md` · M `spec-004-internal-chat.md`(C-A1 · 앞 검수 그대로)
  - profile `delivery-request-v8.json`
- 근거:
  - 앞 리뷰 `chat-permission-spec-wp-review.md` W1
  - `chat-permission-spec-final-fix-report.md`
  - 코디 `delivery-request-v7-execution.json` · `delivery-v7-execution-result.json`(v7 contract 7 · digest `00d8e577…` · plan `22f86376…` 유지 · execution만 갱신)
  - DAY `sessions.py me()`(앞 리뷰 실측)
- 방법:
  - 수정 문장 대조
  - 이전 v8(앞 리뷰 상태)을 복원해 경로 diff · v7-execution 원문과 byte 비교
  - schema/모델 · lint 각 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

| 지적 · 항목 | 실물 | 결과 |
|---|---|---|
| W1 `/me` 사실 | U-1 `:182` 끝 「`/me` 자체가 401 · 403인 경우(인증 불가 · 세션 주인 없음(401) · 기존 규칙상 403)는 … 기존 인증 실패 · 권한 없음 처리 그대로다(셸 없음 · 채팅 포함 진입 없음). **세션 도중 직원 비활성 · 병원 멤버십 상실은 `/me`가 아니라 채팅 서버가 403으로 막는다**(DAY-SPEC-004 §3 「권한 · 격리」 · 케이스 매트릭스 — 앱은 토스트 · 채팅 목록 비움)」 · 매트릭스 `:569` 「`/me` 자체 403(기존 규칙상) … — 세션 도중 비활성 · 멤버십 상실은 채팅 403(DAY-SPEC-004)」 | PASS — DAY `me()`(행 없음만 401 · 활성 재확인 없음) · SPEC-001 `staff_inactive` = 로그인 때 · SPEC-004 `:272` · `:429`와 일치. 새 정책 · 서버 변경 · `/me` 동작 변경 없음 |
| 보존 | board 없음(`/me` 200) = 「시술현황」 본문만 권한 없음 · 셸 · 채팅 · 설정 유지 · board API/SSE · 고객 정보 · 통역 확대 0 · 안내 원문 · 로그아웃 · 권한 키 · API · 새 글자 0 · SPEC-004 C-A1 그대로 | PASS |
| v8 execution 마감 보존 | 이전 v8 대비 바뀐 경로 = **4개뿐**: `code_surface[5]` · `verification[13]`(추가) · `rollback[8]`(추가) · `dependencies[18]`(추가). `code_surface[5]` = v7-execution `code_surface[5]`와 **완전히 같다**. `verification[13]` = v7-execution `verification[9]` · `rollback[8]` = v7-execution `rollback[6]` — **byte 일치** · deps[18]이 출처를 연결한다 | PASS — 코디 v7 execution 갱신(W2 · W3 배선: day_vm.py 선택 APNs/Blob 비밀 2개 → app.env · Git 금지 키 · Dockerfile 첨부 디렉터리 소유권 · compose.local 영속 볼륨)이 v8로 넘어갈 때 빠지지 않는다 |
| 그 밖 v8 회귀 | contract_version 8 · L3 · target 5 · baseline `9692e1fb` · v7 digest 인용 · A41 ~ A52 · deps[2](W1 해소분) · deps[17] 무변경 · 실설정/배포/Vault/기동 0 문장 유지(verification[13] · rollback[8] fail-closed · migration forward-only) | PASS |
| schema · 모델 | `delivery-request.schema.json` **0 errors** · `DeliveryRequest.model_validate` OK(v8 · L3 · target 5 · baseline `9692e1fb`) | PASS |

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` → 출력 없음 · exit 0 · `git status` = M 003 · M 004만 · 003/004 diff +5/−5
- spec-000 · 001 · 002 · 005 = git `b1260dd2` blob **4/4 동일**

## 남은 것

- 코디: SPEC 커밋 → v8 SPEC 원천 sha 갱신(deps[17]대로) → CLI plan · #235 v8 · 사용자 승인 → mobile 워커에 「시술현황 영역만 권한 없음 · 셸/채팅/설정 유지 · 세션 도중 비활성 = 채팅 서버 403 처리」 전달.
- 코드 · 서버 · 앱 · 실 Vault/배포 · 실기기는 미실행(pending)이다.
