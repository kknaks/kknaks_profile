# notification-spec-fix 결과 보고 — SPEC-005 리뷰 W1 · W2 정정 · stable

## 상태: done (SPEC-005 · index 만 · 코드 · WP · GitHub · 커밋 없음 · 동결 5 SPEC 무변경)

## 변경
| 파일 | before → after |
|---|---|
| `spec-005-notifications.md` | `status: draft` → **stable** + 머리 「상태」 문단(계약 확정 · 코드 없음 · 제안 계약 · 키/실기기 pending) |
| 〃 W1 「중복」 행 | 「(호출 id, 계정) 하나 — 방법은 구현」 → 관찰 결과 = (호출 id, 받는 계정) 한 번 · **기본 수단 = 기존 테이블 · migration 없이 호출 단위 잠금 안 조회 뒤 쓰기(같은 tx)** · 유일 색인은 SPEC-000 개정 + migration 선행(동결 해제 뒤 후속 · 기본 아님) · DAY 적응(프로토는 막지 않음 — `repo.py:388-389`) |
| 〃 W1 Backend 줄 | 「migration 이 필요 없다」 절대 단정 → 「기본 = migration 없음 · 유일 색인 고르면 SPEC-000 개정 + migration 먼저」 |
| 〃 W1 OQ-N3 · 모델 대조 제목 · N-A1 | 같은 문장으로 맞춤(「(기본 = 새 schema 없음)」) · N-A1 = 커밋 뒤 훅 재시도 · 동시 실행에도 한 번 · 재호출은 새 call id 라 새 행 · 앞 행 유지 |
| 〃 W1 S-2 | 재호출 = 새 `DoctorCall`(`reassigned_from_call_id`) — CENTURION_DAY b6c034bf `backend/day/services/board.py:540-560` `recall` · 중복 방지 대상 아님 · 앞 행 유지 |
| 〃 W2 API #2 | 「둘 다 없으면 모두 읽음」 → `ids` 있으면 그것만(`ids: []` = 0건) · `callId` 있으면 그 호출만 · 둘 다 = AND · **모두 읽음 = 두 칸이 아예 없을 때만 · 내 병원 + 내 계정 · 전체 날짜**(오늘 목록으로 줄이지 않음) — 원천 `repo.py:401-415` `mark_read` 그대로(병원 조건만 DAY 추가) |
| 〃 W2 실시간 | 읽음 뒤 SSE = 실제 바뀐 행이 있을 때(`read > 0`)만 · **DAY 적응**(원천 `read` 는 SSE 없음 · `announce` 는 새 행 때만 `:45-52`) · 데이터 동기화 보완 |
| 〃 W2 차이 표 | +3행: 읽음 뒤 실시간 · 알림 행 중복 · 읽음 범위(계정 + 병원 · 빈 ids 0건 · 모두 읽음 전체 날짜) |
| 〃 N-A4 · N-A6 | AND · 빈 ids 0건 · 모두 읽음 전체 날짜 · 다른 병원 id 무시 / 0건이면 SSE 안 보냄 |
| 〃 다른 SPEC 후속 | **선행 조건**: SPEC-003 연결 패치는 지금 고치지 않고, 채팅 동결 해제 뒤 · 알림 코드 착수(#235 v8) 전에 적용 + 독립 검수 |
| `20-spec.md` | SPEC List DAY-SPEC-005 draft → stable |
| `30-work.md` | 이번 무변경(앞 Coverage 1행 그대로) |

새 OQ · 사용자 확인 질문 0 · 새 글자 · 정책 0.

## 원천 · AC 매핑
- 프로토 `repository/repo.py:388-389` add_notification(중복 방지 없음) · `:401-415` mark_read(ids IN · 빈 배열 → IN(NULL) 0건 · ids/callId AND · 날짜 조건 없음) · `service/notifications.py:45-52` announce(새 행 때만 SSE).
- DAY `backend/day/services/board.py:540-560` recall = 새 DoctorCall.
- N-A1 ↔ 「알림 행 만들기 · 중복」 · S-2 / N-A4 ↔ API #2 / N-A6 ↔ 실시간 · 차이 표.

## 검증 (최종 1회)
- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` 0건
- `git diff --check` 통과 · `git status` = M 20-spec.md · M 30-work.md · ?? spec-005 — 경계 안
- 53adbd49 대비 spec-000 · 001 · 002 · 003 · 004 hash **동일**(동결)

## 남은 것
- 코드 미구현(제안 계약) · APNs 키 · Apple · 실기기 pending.
- 다음: SPEC-005 재검수 → (채팅 동결 해제 뒤) SPEC-003 연결 패치 + 검수 → #235 v8 WP → 리뷰 → 코드.
