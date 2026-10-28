# 되돌리기 구현 — WORK-006 WP-BE ∥ WP-FE

계약 **SPEC-003 0.5.1**(§5.13 · §6.3 · §7.2 · §7.3 · §8 · §9 「0.5.0 더함」) · 빌드 계획 **WORK-006** — 둘 다 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/` 아래(코디 커밋 08581e4). 결정 `_RESUME.md` §2 10-26 줄. KOS 확인 리포트 `kos-undo-probe-report.md`(OQ-529 · 530 받음).

- **backend** = WORK-006 **WP-BE 행 그대로**. `schemas/board.py` 두 필드(`canUndoStart` · `canUndoFinish`)를 **먼저** 넣는다(FE 고정점). `procedure/back/` 만. 검증 = WP-BE 검증 명령 + 마지막 전체 `uv run pytest -q` 1회.
- **frontend** = WORK-006 **WP-FE 행 그대로**(가짜 보드 `canUndo*` 예시는 back `service/fake_board.py` 하나 허용 — r6 W2). medikit `ConfirmModal` · `Tooltip` · `ResetIcon`. 아이콘 위치 = 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 · 대기 줄 없음. 스크린샷 → `orchestration/work/overall-board/fe-shots/undo-*.png`. 검증 = WP-FE 검증 명령.
- 같은 코드 워크트리(`/Users/kknaks/orca/workspaces/cc-prototype/overall-board`, 브랜치 `kknaksss/overall-board` — PR #6 위에 이어 쌓는다). 반대쪽 폴더 건드리지 마라(FE 의 fake_board.py 예외 하나). 커밋 · push 금지. 사용자 포트(3700 · 8700) 금지 — 가짜 보드는 임시 포트로 띄우고 내려라.
- public: 실명 · KOS id · 키 0.
- 결과는 각자 `backend-r1-report.md` / `frontend-r1-report.md` 끝에 「되돌리기」 절로. 보고는 §9 두 채널.
