# 화면 피드백 1차분 — F1 · F9 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_fcecac921150
- 워크트리: 같은 워크트리 · 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** api 만 다시 빌드했다(`/login` 200).
- 백엔드 소스는 고치지 않았다. 다만 #230 테스트 두 줄을 고쳤다(아래 「알림」 1).

## 상태: done

## F1 — 의사 호출 · 재호출 · 수락 창 = 누른 버튼 아래 팝오버

내용과 두 칸 구성은 그대로다. 왼쪽은 검색 · 추천 「모든 의사」 · 원장 줄 + 상태, 오른쪽은 선택됨 · 호출할 시술, 아래는 버튼이다. **위치와 여는 방식만 바꿨다.**

- **`ui.doctor_call_modal(as_popover=true)`**: 같은 몸체를 #229 **`ui.popover`** 매크로 안에 그린다.
  - 클래스는 이미 있는 `day-pop day-modal day-modal--call` 만 쓴다(폭 = 의사 호출 창 토큰 640px · 모서리 · 그림자). **손 CSS 0 · 새 토큰 0.**
  - `ui.popover` 에 인자 둘을 더했다: `extra`(이미 있는 클래스) · `align`(`start` = 트리거 왼쪽 맞춤).
  - X 는 `data-day-pop-close`(팝오버 닫기) 다. 모달 모드(견본 `/dev/kit` 미리보기 · 서버 모달)는 그대로 `<dialog>` 다.
- **판 조립(`board_parts`)**: 여는 버튼 네 곳을 `ui.pop_trigger` 로 바꿨다.
  - 카드 [의사 호출 · N건]
  - 인박스 확인 필요 [재호출]
  - 시술 줄 [수락]
  - 호출 탭 [수락]
- **day.js 위치**:
  - 누른 버튼 **바로 아래**, 왼쪽 맞춤.
  - 오른쪽이 넘치면 왼쪽으로 당긴다.
  - 아래 공간이 없으면 **위**로.
  - 위아래 모두 모자라면(창 높이 약 500px · 버튼이 화면 가운데) 넓은 쪽에 두고 화면 안으로 당긴다. 이때는 버튼과 겹칠 수 있다.
- **덮개 없음**(판이 보인다). 닫는 방법은 **바깥 클릭 · Esc · X** 이다.
- 열 때 「호출할 시술 · N개」를 카드 체크로 채우고, 검색 칸에 포커스를 준다.
- 열려 있는 동안 판 다시 받기는 미룬다(닫으면 바로 받는다 · fix1 W3).
- **차트 창(E55)은 모달 그대로**다.
- 테스트:
  - `test_의사_호출_재호출_수락_창은_팝오버_차트는_모달`
  - 기존 창 테스트(기본 선택 · 상태 글자 · `hx-params` · 권한 숨김)는 팝오버 마크업으로 갱신했다.

### 브라우저 실물 (1440×900 · 데모 계정 · 저장 버튼은 누르지 않음 — 쓰기 요청 0)

- **실제 `/board`(데모 지점)는 지금 판에 열린 호출 · 준비중 시술 · [수락] 이 없다**(`f0-real-board-now.png`). 그래서 여는 버튼이 없어 팝오버를 실물로 열 수 없었다.
- 같은 템플릿 · 같은 매크로인 견본 `/dev/kit/board` 에서 열었다.

| 연 곳 | 위치(트리거 → 팝오버) | 결과 |
|---|---|---|
| 인박스 [재호출] | (67, 268–296) → (67, 303) 640×502 | 바로 아래 · 왼쪽 맞춤 · 모달 0 · Esc 로 닫힘 |
| 카드 [의사 호출 · 1건] | (620, 439–475) → (620, 12) | 아래 공간 없음 → 위 · 바깥 클릭으로 닫힘 · 「호출할 시술 · 1개」 |
| 시술 줄 [수락] | (832, 386–410) → (788, 386) | 오른쪽 넘침 → 왼쪽으로 당김 · 위아래 모두 모자라 넓은 쪽 · X 로 닫힘 |
| 호출 탭 [수락] | (67, 264–292) → (67, 299) | 바로 아래 |
| 시술 줄 누름 → 차트 | — | 모달 그대로(`dialog[open]` 1) |

## F9 — 방 카드 머리 끌기 손잡이

- **확인 결과: 이미 시안 아이콘 그대로 그려지고 있다.**
  - `icons.html` 의 `grip` 은 시안 `ICON.grip`(lucide grip-vertical · viewBox 24 · 점 6 · stroke 2)과 path 가 같다.
  - `ui.grip` 이 그 아이콘을 그린다.
  - 실제 `/board` DOM: 카드 2장 모두 손잡이 + svg(circle 6) · 16px · 색 `#cfcfcf`.
  - 시안 파일을 같은 브라우저로 열어도 16px · `#cfcfcf` · stroke 2 · 머리 면 `#f7f7f8` 로 **같다**(`f9-grip-board.png` ↔ `f9-grip-prototype.png` · 2배율).
- 「아이콘이 없다」로 보였던 까닭은 둘 중 하나로 본다.
  1. **조작 권한이 없을 때는 손잡이를 일부러 그리지 않는다**(#231 fix1 W2 — board edit 이 없으면 끌기 · 손잡이 없음). `DAY_ADMIN_EMAILS` 를 넣기 전, 또는 백엔드가 `is_admin` 을 넘기기 전 화면이면 손잡이가 없다.
  2. 시안 색 그대로(gray-500 on `#f7f7f8`)라 **아주 옅다.** 더 진하게 할지는 디자인 결정이다(바꾸면 시안과 달라진다).
- 그래서 코드는 바꾸지 않았다. 지금 전체 권한 계정으로 열면 보인다.

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **282 passed** |
| `scripts/test.sh -q backend/tests/day/board backend/tests/day/web` | **111 passed** |
| ruff(내 파일 · 테스트) | 통과 |
| 스크린샷 `frontend-feedback-shots/` | `f0-real-board-now` · `f1-1-recall-popover` · `f1-2-call-popover-from-card` · `f1-3-accept-popover-from-row` · `f1-4-accept-popover-from-inbox` · `f1-5-chart-still-modal` · `f9-grip-board` · `f9-grip-prototype` |

## 바꾼 파일

- `templates/ui.html`: `popover(extra, align)` · `doctor_call_modal(as_popover)` · 몸체를 `_call_body` 로 나눔
- `templates/partials/board_parts.html`: 창 4곳 팝오버 · 여는 버튼 `pop_trigger`
- `static/day.js`: `align=start` · 위아래 고르기 · 열 때 시술 채움 · 검색 포커스 · `data-day-pop-close`
- `tests/day/web/test_board_page.py`

## 알림

1. **#230 테스트 두 줄을 고쳤다**: `tests/day/board/test_board_api.py:630 · 646` 의 `data-day-open-dialog="accept-` → `data-day-pop="accept-`(F1 로 여는 버튼 속성이 바뀜).
   - 630 은 「수락 버튼이 없어야 한다」 단언이다. 예전 속성으로는 늘 거짓이라 의미 없이 통과했는데, 이제 실제로 검사한다(통과).
   - 백엔드 워커가 같은 파일을 만지면 겹칠 수 있다.
2. 팝오버 높이(약 500px)는 900px 화면 가운데의 버튼 아래위에 다 들어가지 않는다. 그때는 넓은 쪽에 두므로 **버튼과 겹칠 수 있다**(창 안 원장 목록은 높이 고정 · 스크롤). 더 줄일지는 디자인 결정이다.
