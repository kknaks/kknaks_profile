# [backend] #236 리뷰 반영 1차 — 테스트 보강 · event_log 인덱스 migration

같은 워크트리 · 같은 규칙(`be-236-brief.md`). 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-236-be-report.md`.

## 할 것
- **W3**: `outbox.touched()` 칸 묶음 변경이 [종료] → 「완료 취소」 superseded 판정에도 영향 — 그 경우를 막는 테스트 추가(맞는 방향인지 확인)
- **W4**: 원장 바꾸기의 「KOS 외부 id 없음 → skipped」 경로 테스트 추가
- **W2 (사용자 2026-11-10 「마이그레이션 적용」)**: `event_log (visit_id, type)` 인덱스 — 새 alembic revision(head 0005_outbox_sender 다음 · forward-only · 레포 migration 규칙대로 · 소프트 딜리트 부분 인덱스 관례가 있으면 따른다). `doctor_changed_at` 조회가 이 인덱스를 타는지 확인
- **W5**: `routers/board.py` docstring 의 옛 `need.overSec` 가 남았으면 고친다
- W1(수락 기록 덮어쓰기)은 그대로(사용자 결정)

## 검증
관련 테스트 · migration 테스트(`backend/tests/migrations`) · 끝에 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q` 1회 · ruff check · format. 커밋 · push 금지.

## 완료 보고
원 브리프와 같은 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`) · subject "backend 리뷰 반영 1차". 변경 파일 · migration revision · 테스트 수.
