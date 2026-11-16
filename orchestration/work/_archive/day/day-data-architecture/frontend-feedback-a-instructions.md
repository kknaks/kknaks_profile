# [frontend] 화면 피드백 1차분 — F1 · F9 (SPEC 변경 없는 것)

너는 #231 frontend 워커다. 같은 워크트리 · 미커밋(로그인 뒤 /board 수정 포함) · 커밋 금지 · 백엔드 파일 금지(backend 가 F8 을 동시에 본다). 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` F1 · F9 · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`.
- **F1** 사이드바 · 카드에서 여는 창 전부(의사 호출 E51 · 재호출 · 수락 「수락할 원장」) — **내용 · 두 칸 그대로, 위치만 누른 버튼 바로 아래 팝오버**(아래 공간 없으면 위 · 오른쪽 넘치면 왼쪽 · 덮개 없음 · 바깥 클릭 / Esc / X 로 닫힘 · 폭 약 640px). 차트 창(E55)은 모달 그대로. #229 popover 매크로를 쓰고 손 CSS 0.
- **F9** 방 카드 머리 끌기 손잡이 아이콘(시안 `.drag-handle svg`) — 아이콘 세트(G8)에 넣고 `ui.grip` 이 그리게.
검증: `uv run pytest -m "not infra"` · ruff · 브라우저 실물(/board — 사용자가 DAY_ADMIN_EMAILS 넣어 둠) 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-shots/` · compose down 금지 · api 만 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-a-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
