# [frontend] 버그 F11 (+ F12) — 의사 호출 창 위치 · 0개 · 판 사라짐

너는 #231 frontend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지 · 백엔드 파일 금지(backend 가 F10 실물 확인을 기다리는 중 — api 재빌드만 하고 worker/scheduler 는 건드리지 마라).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md` F11 · F12.
- **F11** 실제 /board 에서 카드 체크 → [의사 호출 · N건] → 창이 **화면 왼쪽 위**에 뜨고 · 「호출할 시술 · 0개」 · 창 열린 동안 **판 카드가 사라진다**. F1 대로 그 버튼 바로 아래(공간 없으면 위) · 고른 시술 목록 · 판 그대로. 견본(/dev/kit/board)에선 됐다면 실제 판 조각 · SSE 다시 받기와 어긋나는 자리 — 원인을 찾아라. 카드 줄 [수락] · 인박스에서 연 창도 같이 확인.
- **F12** 카드 · 인박스 선택은 다시 누르면 해제.
검증: `uv run pytest -m "not infra"` · ruff · **브라우저 실물 /board**(데모 카드로 체크 → 호출 창 위치 · 개수 · 판 유지) 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-shots/` · compose down 금지 · api 만 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-feedback-c-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
