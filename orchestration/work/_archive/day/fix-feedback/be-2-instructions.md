# [backend] be-2 — 2루프: 호출 취소(F-5) · 시스템 계정 집도의 표시 칸(E3)

너는 앞 맥락이 없다. 먼저 읽어라:
1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-be-brief.md` — 역할 · allowed_paths · 범위 제약 · 검증 · 완료 보고가 그대로 적용(작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` — 1루프 미커밋 위에 이어서).
2. 1루프 결과 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/be-1-report.md` · 코드 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-code-1-report.md`.
3. 스펙(미커밋 · 절대경로): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec/products/day/20-spec/spec-002-procedure-board.md` **개정 ㉒**(머리 :42 · U-3 :225-229 · U-7 :275 · 호출 상태 :541-547 · API :578 · 응답 :595 · 스냅샷 :660 `systemDoctor` · 매트릭스 :740-743 · 검사 순서 :756 · 토스트 :782 · 규칙 38 :953) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/_RESUME.md` §2.

⚠ **frontend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라.

## 고정 — 사용자 결정(스펙 어느 줄과 달라도 이것이 우선)

- **호출 취소 알림 · 새 알림 종류 · 앱 푸시 · migration 없음.** (SPEC-005 :444 「모델 대조」에 migration 문장이 남아 있으나 옛 문장이다 — 따르지 마라.)
- **호출 취소는 KOS 쓰기 없음**(KOS 에 호출 취소 명령 없음 — 사용자). DAY 만.

## 할 일

1. **호출 취소 서비스** `services/board.py` `cancel_call(session, current, task_id: uuid.UUID, now=None) -> ActionResult`(1루프 `undo_home` 과 같은 모양) — 규칙 38 · 검사 순서 :756 그대로: 401/403/404 → 409 `visit_home` → 수락된 호출이면 `call_already_accepted` → 호출(수락 전) 아니면 `task_not_called` → 취소 = 그 줄이 든 **열린 호출 전부**의 `doctor_call_task.deleted_at` + 받을 시술이 남지 않은 호출은 `closed_at` · `event_log` 1행(이름은 스펙대로 · 없으면 `call.cancel` 로 제안하고 리포트에) · 한 transaction. migration 없음(기존 칸).
2. **E3 `systemDoctor`** — 스냅샷 줄에 `systemDoctor: bool`(:660 — 담당 원장 없음 + KOS 집도의 = 병원 시스템 계정). 웹 · 앱 스냅샷 모두 더한 칸뿐(앱은 무시). 원장 변경(`doctor_change`)이 그 줄에서 원장 줄과 똑같이 되는지 확인 · 막히면 고쳐라(스펙 U-3 :228).
3. 거절 코드 글자는 `MESSAGES` 에 넣지 않는다(→ 일반 글자로 떨어짐 · 스펙 「비워 둠」).
4. 테스트 — 호출 취소: 성공(줄 준비중 · 남은 줄 없으면 호출 닫힘 · 남으면 열림) · `call_already_accepted` · `task_not_called` · `visit_home` · KOS outbox 0 건 · 알림 행 0 건. `systemDoctor` 참/거짓.

## 검증

- `cd backend && uv run pytest -q <만든·고친 테스트>` · ruff — 각 1회. **infra 테스트도 이번엔 돌린다**: `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q <네 infra 테스트 파일>`(스키마 `day_test` · 사용자 데이터 안 건드림 · Docker 는 켜져 있음 · 컨테이너를 띄우거나 내리지 마라).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/be-2-report.md` — 변경 파일 · 계약(함수 이름 · 시그니처 · 칸 이름) · 테스트 수치 · fe 몫 · E2E 에서 만날 자리. 완료 보고는 preamble 의 worker_done.
