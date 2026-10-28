# frontend WORK-008 추가 지시 1 (코디 · 2026-10-27) — review-doc r5 처분

`procedure-review-doc-r5-dispositions.md` 의 frontend 몫:
- W1: 판 = 흰 판(스크롤 컨테이너) 전체 — 가장자리 12px 에 놓아도 저장(지금 `onDrop` 이 흰 판이면 그대로)
- W2: FE3 예시 값에 필요하면 `procedure/back/app/service/fake_board.py` **예시 값만** 고쳐도 된다(back 의 다른 파일 금지) · **카드 수 5 유지 · 있는 카드 값만 바꿈** · 고쳤으면 `cd procedure/back && uv run pytest -q` 통과 수치를 보고에
- W5: 대기 줄 오른쪽 칸(호출함 · 칩 · 아이콘 · 버튼)이 한 줄로 남게 · 시술 이름 줄바꿈은 허용
