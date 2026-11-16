# [backend] 화면 피드백 2차분 — F3 · F4 · F5 · F7 · F10 (백엔드)

너는 #230 backend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지. 템플릿 · day.js 는 frontend 가 동시에 — 건드리지 마라(조각에 넘기는 값이 바뀌면 리포트 맨 위 「#231 영향」).
정본: SPEC-002 ⑥⑦ `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md`(PR #909 `6386f746`) · SPEC-000 `sender_staff_id` · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` · cc `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/kos/ops.py`(귀가 대기 · 되돌리기 요청).
1. **F3** 다시 호출 = cc D-25 ~ D-27(대기면 호출 · 수락돼도 다시 · 유효 호출 = 가장 최근 · 앞 수락 무효 · KOS `call-tasks-doctors` 다시 보냄).
2. **F4** 카드 안 줄 순서 = 진행중(시작 순) → 대기(오더 순) → 완료(완료 시각 순).
3. **F5** 귀가 대기 방문은 판 카드에서 빠지고 인박스 「시술 완료」에만.
4. **F7** 스냅샷에 `customer.nationality`(그대로 · 없으면 null) · 입실 시각은 고객 줄에 안 씀.
5. **F10** KOS 쓰기 = **누른 사람 토큰** — migration `external_outbox.sender_staff_id` · 수락도 누른 사람(대리 수락 = 간호사) · KOS 엔 수락한 의사 doctorIds · 귀가 대기 · 시작 취소 · 완료 취소 쓰기 열기(cc 요청 · 내부 경로 · 데모 실물 확인 전 운영 연결엔 막는 설정).
6. **멈춘 로컬 outbox 행 정리**(새 규칙으로 다시 보내거나 failed — 로컬 dev 데이터).
7. **실물(데모 지점 · 사용자 허락됨 — 화면에서 직접 쓰기 중)**: 호출 → 수락 → 시작 → 종료 → 귀가 대기 · 시작 취소 1회씩 KOS 반영 confirmed 확인(값 · 개인정보 없이 상태 · 건수만).
검증: `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · compose down 금지 · api/worker/scheduler 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-feedback-b-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
