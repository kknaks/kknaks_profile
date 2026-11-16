# F15 · F5 정리 — 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_e6e7c40b4761
- 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** api 만 다시 빌드했다.
- 백엔드 파일은 건드리지 않았다.

## 상태: done

| 항목 | 바꾼 것 |
|---|---|
| F15 빈 판 | `board_main.html` 에서 판 빈 상태 「지금 판에 앉은 고객이 없어요」 를 뺐다. 카드가 없으면 판은 비워 둔다. 인박스 시술 완료 탭의 빈 상태는 그대로다 |
| F5 흐린 귀가 대기 분기 | `board_parts.room_card` 에서 `card.state == "home"` 분기를 모두 지웠다: 손잡이 숨김 · 끌기 잠금 · 마취 칩 배지 · 호출 바 숨김. 귀가 대기 방문은 서버가 판에서 빼고 `doneTab` 에만 싣는다. 끌기 잠금과 버튼 숨김은 이제 조작 권한(`EDIT`)만 본다 |
| 줄 순서(F4) | 서버 배열 순서 그대로 그린다(진행 → 대기 → 완료). 완료 줄은 아래 칸에 두는데, 서버가 이미 맨 뒤에 두므로 순서가 바뀌지 않는다 |
| 체크(F3) · 국적(F7) | 앞 2차분에서 이미 서버 `pickable` · `customer.nationality` 를 따른다. 「입실」 은 쓰지 않는다. 이번에 바꾼 것 없음 |

## 검증

- `uv run pytest -q -m "not infra"`: **296 passed**
- `scripts/test.sh -q backend/tests/day/board backend/tests/day/web`: **124 passed**
- ruff 통과
- 새 테스트:
  - `test_빈_판은_비워_둔다`(판에 빈 상태 · 문구 없음)
  - `test_시술_줄은_서버_배열_순서_그대로`
- 브라우저 실물 `/board`(데모 계정):
  - 판 카드 0 — 데모 두 방문이 모두 귀가 대기라 판에서 빠지고 「시술 완료 2」
  - 판 빈 상태 0 · 흐림 0
  - 스크린샷 `frontend-feedback-shots/fd-real-board.png`
- 카드가 있을 때의 모습은 견본 `/dev/kit/board` 에서 본다(같은 템플릿).

## 바꾼 파일

`templates/partials/board_main.html` · `templates/partials/board_parts.html` · `tests/day/web/test_board_page.py`
