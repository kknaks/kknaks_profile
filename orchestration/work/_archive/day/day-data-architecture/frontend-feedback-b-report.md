# 화면 피드백 2차분 — F3 · F5 · F6 · F7 (화면) 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_075dce16e3eb
- 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** api 만 다시 빌드했다(`/login` 200).
- 백엔드 파일은 건드리지 않았다.
- `backend-feedback-b-report.md` 는 작업을 끝낼 때까지 없었다. 그래서 화면이 **서버 값만 따르도록** 만들었다. 백엔드가 바뀌면 화면이 저절로 맞는다(아래 「백엔드 반영 전후」).

## 상태: done

| # | 바꾼 것 | 파일 |
|---|---|---|
| F3 | 시술 줄의 체크를 **대기 줄(준비중 · 호출 · 수락)** 에 그린다. 진행중 · 완료는 체크가 꺼진다. 켤지 끌지는 서버 `pickable`(+ 조작 권한)이 정한다 | `ui.html` `proc_row`(조건 `status in wait · called · accepted`) |
| F5 | 방 카드의 귀가 대기 흐림(`is-going`)을 걷었다. 판에서 빼는 것은 서버 판 조건이다. 시술 완료 탭(귀가 대기 · 귀가 배지)은 그대로다 | `board_parts.room_card` |
| F6 | 페이지 머리의 [필터](E09) · 「의사별 · 구역」(E10)을 뺐다. 이제 「시술 현황 \| 날짜」 만 있다 | `board_main.html` |
| F7 | 바이탈 줄 = **성별 \| 만 나이 \| 국적**이다. 국적은 `customer.nationality` 값 그대로 쓰고, 없으면 칸을 그리지 않는다. 「입실 HH:MM」 은 뺐다. 인박스 · 시술 완료 카드에는 원래 이 줄이 없다. 시술 완료 카드 머리의 「입실-귀가」 시각(E28)은 다른 요소라 그대로 둔다 | `board_parts.customer` |

## 백엔드 반영 전후

지금 백엔드 상태:
- `board_rules.pickable` = `ready_wait` 만
- 판 조건 = `PROCEDURE_DONE` 포함
- 스냅샷에 `nationality` 없음

그래서 실제 화면에서 다음은 백엔드가 바뀐 뒤에야 보인다.
- 호출 · 수락 줄의 체크 켜짐(F3)
- 귀가 대기 카드가 판에서 사라짐(F5)
- 국적 글자(F7)

지금 보이는 것: F6 와 「입실」 빠짐. 귀가 대기 카드가 있다면 흐리지 않게 보인다.

테스트도 양쪽을 다 받는다. 견본 판 순서는 V5(귀가 대기)가 「없거나 맨 뒤」이고, 끌기 잠금은 V5 가 있을 때만 본다.

## 검증

- `uv run pytest -q -m "not infra"`: **285 passed**
- `scripts/test.sh -q backend/tests/day/board backend/tests/day/web`: **114 passed**
- ruff(테스트) 통과
- 새 테스트(`tests/day/web/test_board_page.py`):
  - 바이탈 줄에 입실 없음
  - 국적 값 그대로 · 없으면 칸 없음
  - 대기 줄(준비중 · 호출 · 수락) 체크 켜짐 · 진행중 꺼짐 · locked 면 꺼짐
  - E09 · E10 없음
  - 흐림 표시 없음
- 브라우저 실물 `/board`(데모 계정 · 1440×900): 필터 · 세그먼트 0개 · 바이탈 「여」(입실 없음 · 국적 값 없음) · `is-going` 0개 · 카드 1장(진행중 줄 2 — 체크 꺼짐이 맞다)
- 스크린샷 `frontend-feedback-shots/`: `fb-real-board.png` · `fb-sample-board.png`
