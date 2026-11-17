# [planner] spec-2 — 검수 WARN 반영 · 착수 막는 OQ 에 임시 기본값 박기

너는 앞 맥락이 없다. 먼저 읽어라:

1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-spec-brief.md` — 역할 · 결정 표 · allowed_paths(`products/day/`) · 범위 제약 · 검증이 그대로 적용된다.
2. 앞 판 리포트 `…/fix-feedback/spec-report.md`
3. 검수 `…/fix-feedback/review-doc-1-report.md` — WARN W1 ~ W12 · §6 「착수 막는 OQ」 표

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` (앞 판의 미커밋 변경 위에 이어서). 커밋 · push · PR · 승인 금지.

## 할 일

### A. 착수 막는 OQ — 아래 값을 **「기본값(코디 2026-11-17 · 사용자 E2E 에서 확인)」**으로 스펙에 박는다

OQ 는 지우지 말고 열린 채로 두되, 코드가 따를 기본값을 각 OQ 와 본문 규칙 · 계약에 적는다.

| OQ | 기본값 |
|---|---|
| OQ-61 ⓐ | N = 0 이면 「바로 시작」 버튼 꺼짐(disabled). 액션바는 지금처럼 체크가 있을 때만 |
| OQ-61 ⓑ | 수락 줄이 요청에 오면 그 줄 거절 `task_not_waiting` |
| OQ-63 ⓐ | 일부 거절 = 거절 코드마다 토스트 1장 · 기존 코드 글자 |
| OQ-63 ⓒ | `event_log` = `task.quick_start` 1행(규칙 21) |
| OQ-65 ⓐ | 시스템 계정 집도의 그대로 · 시술 전 의사차트 글만 보냄(지금 코드 경로 `board.py:829-834`) |
| OQ-66 ⓑ | KOS 확인 조건 = `doctors_equal = [시스템 계정]` · `status` 안 봄 |
| OQ-58 ⓑ | KOS `change-flow-step(PROCEDURE_DONE → PROCEDURE)` 를 **보낸다** — 데모 실물은 E2E 에서 확인(안 보내면 다음 동기화에 카드가 다시 빠짐) |
| OQ-58 ⓔ | 확인 창 없음 · 성공 토스트 없음 · `visit_not_home` 글자는 비워 둠(기존 일반 거절 처리) |
| OQ-58 ⓕ | 방 없는 귀가 대기 방문 = 409 `visit_not_home` |
| OQ-59 ⓑ | 처음 탭 = 시술순 · 기억 안 함 |
| OQ-59 ⓓ | 방 이름(`room.title`) 문자열 오름차순 · 같은 이름은 시술순 순서 |
| OQ-59 ⓔ | **서버 정렬** — `GET /board?view=room` 같은 보기 값(이름은 코드 사실에 맞춰 네가 적는다). SSE 로 다시 받을 때 같은 보기 값을 실어 탭 유지 |
| OQ-59 ⓕ | 다시 그릴 때 탭 유지 |
| OQ-N8 | 권한은 첫 사용자 동작(클릭) 때 묻기 · 거절이면 안내 없음 |
| OQ-N9 | `document.hidden` 일 때만 OS 알림 |
| OQ-N10 | 누르면 탭 앞으로 + `/board` · 읽음 처리 안 함 |
| OQ-N11 | ㉠ 서버 변경 없음 — 기존 `notification` 이벤트 + `GET /api/notifications` (웹 쿠키 세션). 공통 틀(`base.html`)에서 스트림을 붙인다 |
| OQ-N12 | Notification `tag` = 알림 행 id |

### B. 문서 고침

- W3 `room.order` → 실제 칸 `sort_order`(스냅샷에 없음) — 이번 기본값(OQ-59 ⓓ)은 `room.title` 이라 스냅샷 칸 추가 없음으로 정리.
- W6 KOS 쓰기 1행 확인 조건을 위 OQ-66 ⓑ 대로.
- W10 `visit_home` 을 「묶음 전체 409(줄 판정 전)」로 :583 · :742 · :922 통일.
- W11 S-4 제목 「호출 없이 바로 시작」.
- W12 :342 아이콘 문장 「(작성된 것만 · :343)」 정리.
- W9 는 고치지 않는다(사용자 확인 대기 — F-4 받는 계정 규칙 그대로).

### C. 검증 · 보고

- `python3 scripts/lint-pipeline.py --strict` → products/day/ ERROR 0.
- Delivery #254 는 건드리지 마라(스펙 PR 머지 뒤 v2 재결속은 코디 몫).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-2-report.md` — 고친 곳 파일:줄 · 기본값 박은 위치 표.
- 완료 보고는 dispatch preamble 의 `worker_done` 명령으로.
