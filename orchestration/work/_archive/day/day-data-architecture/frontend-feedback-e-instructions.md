# [frontend] 화면 피드백 F17 · F18 · F19

너는 #231 frontend 워커다. 같은 워크트리 · 마지막 커밋 `292d0996` 위 · 커밋 금지 · 백엔드 로직 파일은 꼭 필요할 때만(필요하면 리포트 맨 위에 적어라 — 지금 다른 워커 없음).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` F17 · F18 · F19.
- **F17** 호출(재호출 포함)이 나가면 그 카드의 선택 해제 · [의사 호출 · N건] 바 사라짐.
- **F18** [종료] 뒤 완료 줄 더보기가 저절로 열리는 원인을 찾아 막는다(같은 자리 버튼이 바뀌며 클릭/포커스가 이어지는지) · 줄이 바뀌는 모습은 짧고 부드럽게(모션은 토큰 · day.js — 손 CSS 0).
- **F19** 카드 D&D 를 cc-prototype 처럼: 끄는 카드가 손을 따라옴 · 놓일 자리 미리보기(다른 카드가 비켜남) · 놓으면 부드럽게 자리 잡음 · SSE 다시 받기와 안 부딪힘. 본: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/front/components/procedures/OrderCard.tsx` · 판 `procedure/front/app/**/live*` · 시안 FLIP(L1491-1558). 순서 저장은 지금 `PUT /board/order` 그대로.
검증: `uv run pytest -m "not infra"` · ruff · **브라우저 실물 /board**(데모 카드 2장 이상이 판에 있어야 F19 확인 — 없으면 견본 /dev/kit/board 로) · 스크린샷 · 가능하면 짧은 화면 녹화(gif 또는 연속 스크린샷) `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-shots/` · compose down 금지 · api 만 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-e-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
