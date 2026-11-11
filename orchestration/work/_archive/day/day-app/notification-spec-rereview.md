# 리뷰 리포트 — day-app 알림 SPEC-005 W1 · W2 정정 · stable 재검수 / doc (2026-11-10)

- 대상: 스펙 트리 `53adbd49` 위 미커밋 — ?? `spec-005-notifications.md`(draft → stable) · M `20-spec.md`(List stable) · M `30-work.md`(Coverage 1행 · 이번 무변경)
- 근거:
  - 앞 리뷰 `notification-spec-review.md` W1 · W2 · 참고 1 · 2
  - `notification-spec-fix-report.md`
  - 프로토 `77173cf8` `repository/repo.py:388-415` · `service/notifications.py:45-52`(앞 리뷰 실측)
  - DAY `b6c034bf` `backend/day/services/board.py:540-560`(read-only)
- 방법:
  - 수정 문장 직접 대조 · 동결 blob 5개 비교
  - lint 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

| 지적 | 수정 실물 | 결과 |
|---|---|---|
| W1 중복 vs migration | `spec-005:187` 「중복」 = 관찰 결과 (호출 id, 받는 계정) 한 번(커밋 뒤 훅 재시도 · 동시 실행) · **기본 수단 = 기존 테이블 · migration 없이 호출 단위 잠금(그 `doctor_call` 행 잠금 등) 안에서 조회 뒤 쓰기를 같은 tx** · 유일 색인은 SPEC-000 개정 + migration 선행(동결 해제 뒤 후속 · 기본 아님) · DAY 적응으로 표기(프로토 `repo.py:388-389` 막지 않음). `:284` Backend · `:346` OQ-N3 · N-A1 `:323` · 차이 표 `:307`이 같은 문장이다 | PASS — 「migration 필요 없다」 단정과 보장의 모순이 풀렸다 · 잠금 수단이 검증 가능(N-A1 재시도 · 동시 실행) |
| W1 재호출 근거 | S-2 `:154` 재호출 = 새 `DoctorCall`(`reassigned_from_call_id` = 앞 호출) → 새 행 · 앞 행 유지 · 중복 방지 대상 아님 | PASS — DAY `board.py:540-560` `recall`이 `DoctorCall(…, reassigned_from_call_id=old.id)`를 만드는 것을 실측 |
| W2 빈 `ids` | API #2 `:200` `ids`가 있으면 그것만(`ids: []` = **0건**) · `callId`면 그 호출만 · 둘 다 = AND · 모두 읽음 = 두 칸이 아예 없을 때만 · 내 병원 + 내 계정 · **전체 날짜** · N-A4 `:326` 같은 뜻 | PASS — 프로토 `mark_read`(`IN (NULL)` 0건 · AND · 날짜 조건 없음)와 일치 · 앞 리뷰 참고 2(모두 읽음 날짜 범위)까지 반영 · 병원 조건만 DAY 추가로 표기 |
| W2 읽음 뒤 SSE | 실시간 `:220` 읽음/모두 읽음으로 실제 바뀐 행이 있을 때(`read > 0`)만 · **DAY 적응**(원천 `read`는 SSE 없음 · `announce`는 새 행 때만) · 차이 표 `:306` · N-A6 `:328` 「0건이면 안 보냄」 | PASS — 원천 차이를 명시 · 새 글자 · 정책 아닌 데이터 동기화로 한정 |
| 참고 1 순서 | `:361` **선행 조건** — SPEC-003 연결 패치는 지금 고치지 않고, 채팅 동결 해제 뒤 · 알림 코드 착수(#235 v8) **전에** 적용 + 독립 검수 | PASS |
| stable · index | frontmatter `status: stable` · 머리 「상태」 문단(계약 확정 · 코드 없음 · 제안 계약 · 키/Apple/실기기 pending) · 「지금 상태 — 정직 표기」(테이블만 · API/훅/발송 없음) 유지 · `20-spec.md:74` List stable | PASS — 구현 완료 주장 없음 |

## 동결 · 경계 · 회귀

- spec-000 · 001 · 002 · 003 · 004 = `53adbd49` blob과 **5/5 동일**(`git hash-object` 대조).
- `git status` = M `20-spec.md` · M `30-work.md` · ?? `spec-005-notifications.md` — 허용 3경로 안.
- 앞 리뷰에서 PASS였던 받는 사람 정책(원장 목록 / 지정 · 관리자 추가 · 호출자 제외 없음) · 채팅 분리 · v7 기기/APNs 공유 · `skipped_no_key` 분리 · 원형 글자 · 격리 · 인수 조건 구성은 그대로다. 새 OQ · 사용자 질문 · 새 글자 · 새 정책은 없다.

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` → 출력 없음 · exit 0

## 남은 것 (결함 아님)

- 앞 리뷰 참고 4(받는 계정 계산에서 활성 · 계정 있음 필터)는 SPEC 문장(`:180` 「활성 직원 · 계정 있음」)대로 구현하면 된다 — 코드 리뷰 확인 대상.
- 다음: 채팅 동결 해제 뒤 SPEC-003 연결 패치 + 검수 → #235 v8 WP → 리뷰 → 알림 코드(같은 PR #237). 코드 · APNs 키 · Apple · 실기기 수신은 미실행(pending)이다.
