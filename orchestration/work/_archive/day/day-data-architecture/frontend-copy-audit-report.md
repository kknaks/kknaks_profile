# F21 — 시안 · SPEC 에 없는 화면 문구 걷기(전수) 결과 보고

- 작성: day frontend 워커 · 2026-11-08 · task_ca5e4982b4e0
- 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** api 만 다시 빌드했다.
- 백엔드 로직 파일은 건드리지 않았다.

## 상태: done

기준(사용자 · `roles/day/frontend/rules.md` 「문구」): 시안 · SPEC · 원천에 없는 글자는 뺀다. 대신할 문구를 새로 넣지 않는다. 빈 자리는 비워 둔다. 동작에 꼭 필요한 글자에 근거가 없으면 빼지 않고 「사용자 확인」으로 올린다. dev 견본(`/dev/kit`) 설명 글은 제외다.

## 뺀 것 (근거 없음)

| 문구 | 자리 | 처리 |
|---|---|---|
| 「시술 완료 고객이 없어요」 | 인박스 시술 완료 탭 — 고객이 하나도 없을 때 | 뺐다(빈 탭은 비움). 찾기 결과 0건의 「조건에 맞는 고객이 없어요 · 조건 지우기」는 시안 L1447 이라 그대로 |
| 「이름 · 발음 검색」 | 시술 완료 탭 검색 placeholder | 시안 L1446 의 **「고객 이름」** 으로(aria 「고객 이름으로 찾기」도 시안). 지어낸 말이 아니라 시안 글자로 바꾼 것이다 |
| 「KOS 계정으로 로그인합니다.」 | 로그인 카드 설명 | 뺐다 |
| 「로그인할 병원을 고르세요. 다른 병원으로 바꾸려면 다시 로그인합니다.」 | 병원 고르기 카드 설명 | 뺐다 |
| 「의사를 선택하세요」(선택됨 칸 안의 빈 글) | 의사 호출 · 재호출 · 수락 창의 「선택됨」 자리 | 뺐다. 원천 L99 의 「의사를 선택하세요」는 **꺼진 아래 버튼** 글자라 버튼에는 그대로 둔다. 선택됨 칸은 고르기 전엔 비운다. 재호출 · 수락(한 칸)은 시안 `recallPopHtml` 처럼 고르기 전엔 「선택됨」 머리째 숨긴다 |
| 「원장」(목록 머리) | 의사 호출 창(두 칸) 원장 줄 위 | 근거 없음. 같은 창 모양의 시안 라벨 **「전체」**(시안 L1088)로 바꿨다. 시안에 있는 글자다 |
| 「의사 검색」(placeholder) | 의사 호출 창 검색 칸 | 시안 L1085 placeholder **「검색」** 으로(aria 「의사 검색」은 시안 그대로) |
| 「입력 지우기」(aria) | 검색 칸 지우기 X | 시안 L1446 aria **「입력 삭제」** 로 |

앞 회차에 뺀 「지금 판에 앉은 고객이 없어요」(F15) · 「아직 열린 화면이 없어요」(빈 홈 — 삭제)도 다시 들어오지 않게 테스트로 막았다.

## 사용자 확인 (근거 없음 · 빼면 뜻이 사라져 남김)

| 문구 | 자리 | 왜 남겼나 |
|---|---|---|
| 「병원 선택」 | 병원 고르기 카드 제목 | 병원이 여럿일 때만 나오는 화면의 이름이다. 빼면 무엇을 고르는 화면인지 사라진다 |
| 「처음으로」 | 병원 고르기 → 로그인으로 돌아가는 링크 | 링크 글자 |
| 「MediSolve AI」 · 「DAY」 | 로그인 카드 위 · 제목 | SPEC-001 은 「centurion 로그인 화면 모양」만 정했다(그 화면의 회사 · 앱 이름 자리). 문구 자체의 근거는 없다 |
| 조작 오류 토스트 16줄 · 「KOS 반영 실패 — 데스크에서 KOS 를 확인하세요」 | 판 조작 409 등 · SSE `kos_failed` 토스트 | **백엔드 파일**(`routers/board.py` `MESSAGES` · `KOS_FAILED_MESSAGE` — #230 이 「자리 값」이라 적음). SPEC-002 는 「실패 토스트만」이고 글자는 정하지 않았다. 빼면 토스트가 빈다. 고칠지 · 무엇으로 할지는 사용자 결정이다. 화면 워커는 백엔드 로직 금지라 손대지 않았다 |
| 마취 · 시간 글자 「+mm:ss」 · 「n분」 · 「n초」 | 칩 · 시간 칸 | 시안 L943-947 · L1168(근거 있음 — 참고로 적음) |

로그인 오류 문구 13줄(`routers/login.py`)과 권한 없음 · CSRF 문구(`web_errors.py`)는 SPEC-001 대응표와 글자까지 같다(근거 있음).

## 막는 장치

- 새 테스트 `tests/architecture/test_screen_copy.py`:
  - **화면 템플릿 · day.js 의 한글을 모두 뽑아** 근거 표(`VISIBLE` · `HIDDEN`)에 있는지 본다. 표의 값이 근거다.
  - 표에 없는 글자가 생기면 실패한다. 근거가 없으면 넣지 않는다.
  - `test_지어_넣었던_문구는_없다`: 뺀 문구 여섯이 다시 들어오면 실패한다.

## 검증

- `uv run pytest -q -m "not infra"`: **309 passed**
- ruff 통과 · CSS 다시 빌드(선택됨 숨김 한 줄)
- 브라우저:
  - 로그인 카드 글자 = 「MediSolve AI · DAY · 이메일 · 비밀번호 · 로그인」
  - 실제 `/board` 시술 완료 탭: 고객 없음 → 빈 탭(문구 없음) · placeholder 「고객 이름」
  - 견본: 수락 창은 고르기 전 머리 「전체」 만 → 고르면 「선택됨/전체」 · 의사 호출 창은 「추천/전체/선택됨/호출할 시술 · 1개」 · 선택됨 칸 빈 글
- 스크린샷(`frontend-feedback-shots/`): `f21-login.png` · `f21-board-done-tab.png` · `f21-accept-before-pick.png` · `f21-call-window.png`

## 바꾼 파일

- `templates/partials/board_main.html`
- `templates/partials/login_card.html`
- `templates/ui.html`
- `styles/app.css` + `static/day.css`
- `tests/architecture/test_screen_copy.py`(새)

## 문구 전수 표 (화면 템플릿 · day.js — dev 견본 제외)

「보임」 = 화면 글자 · placeholder · 툴팁. 「aria · title」 = 스크린 리더 이름 · 대체 글(화면에 안 보임). 근거의 L 번호는 시안 줄이다.

| 문구 | 종류 | 파일 | 근거 |
|---|---|---|---|
| 간호 관리 차트 | 보임 | ui.html | 시안 L1265 · SPEC-002 E55 |
| 간호관리차트 | aria · title | ui.html | 시안 L1466 툴팁 |
| 개 | 보임 | ui.html | 원천 L98 「호출할 시술 · N개」 |
| 건 | 보임 | board_parts.html | SPEC-002 U-3 「의사 호출 · N건」 |
| 검색 | 보임 | ui.html | 시안 L1085 placeholder |
| 고객 검색 | 보임 | base.html | 시안 L726 · SPEC-002 E06 |
| 고객 이름 | 보임 | board_main.html | 시안 L1446 완료 탭 검색 placeholder |
| 고객 이름으로 찾기 | aria · title | board_main.html | 시안 L1446 aria-label |
| 권한 없음 | 보임 | forbidden.html | SPEC-001 대응표 「권한 없음 화면」 |
| 권한 없음 · DAY | 보임 | forbidden_page.html | 탭 제목 = 권한 없음(SPEC-001) + 제품 이름 |
| 귀가 | 보임 | board_parts.html | 시안 L1438 배지 · SPEC-002 U-12 |
| 귀가 대기 | 보임 | board_parts.html | 시안 L1228 · SPEC-002 E46 |
| 끌거나 화살표 키 | aria · title | ui.html | 시안 L1214 aria-label |
| 남 | 보임 | board_parts.html | 성별(시안 L1219 c.sex 앞 글자) |
| 다음 날 | 보임 | ui.html | 시안 L734(날짜 이동 · 이 화면엔 안 씀) |
| 닫기 | aria · title | ui.html | 시안 L1084 aria-label |
| 더보기 | aria · title | board_parts.html · ui.html | 시안 L1143 aria-label |
| 로그아웃 | 보임 | base.html | SPEC-001 U-3 |
| 로그인 | 보임 | login.html · login_card.html | SPEC-001 U-1 |
| 로그인 · DAY | 보임 | login_card.html | 탭 제목 = 로그인(SPEC-001) + 제품 이름 |
| 마취 | 보임 | board_parts.html | 시안 L1184 「마취 +mm:ss」 |
| 마취 시작 | 보임 | board_parts.html | 시안 L1187 · SPEC-002 U-8 |
| 마취 완료 | 보임 | board_parts.html | 시안 L1190 「마취 완료 nn분」 |
| 마취 재시작 | 보임 | board_parts.html | 시안 L1186 툴팁 |
| 마취 종료 | 보임 | board_parts.html | 시안 L1184 툴팁 |
| 메뉴 | aria · title | base.html | 시안 L722 nav aria-label |
| 메모 | aria · title | ui.html | 시안 L1221 aria-label 「메모 접기/크게 보기」 |
| 메모 접기 | aria · title | day.js | 시안 L1221 aria-label |
| 메모 크게 보기 | aria · title | day.js | 시안 L1221 aria-label |
| 모든 의사 | 보임 | ui.html | 원천 L97 · SPEC-002 U-4 |
| 병원 선택 | 보임 | login_card.html | 사용자 확인 — 근거 없음(병원 고르기 화면 제목 · 빼면 화면 뜻이 사라짐) |
| 분 | 보임 | board_parts.html · day.js | 시안 L1168 「nn분」 |
| 비밀번호 | 보임 | login_card.html | SPEC-001 U-1 입력 |
| 비어 있음 | 보임 | board_parts.html | 시안 L900 · SPEC-002 규칙 19 |
| 선택 | aria · title | ui.html | 시안 L1139 aria-label 「… 선택」 |
| 선택됨 | 보임 | ui.html | 원천 L98 · 시안 L1087 |
| 선택한 시술 | aria · title | board_parts.html | 보이지 않음 — 호출 바 region aria-label |
| 수납 필요 | 보임 | ui.html | SPEC-002 U9 · 원천 L20 |
| 수락 | 보임 | board_parts.html · ui.html | 시안 L1158 · SPEC-002 U-3 |
| 수락 대기 | 보임 | board_main.html | 시안 L1061 · SPEC-002 U-11 |
| 수락할 원장 | 보임 | ui.html | 시안 L1084 머리 |
| 수락함 | 보임 | board_main.html | 시안 L1061 · SPEC-002 U-11 |
| 순서 바꾸기 | aria · title | ui.html | 시안 L1214 aria-label |
| 시술 대기 | 보임 | board_main.html | 시안 L1006 · SPEC-002 U-10 |
| 시술 완료 | 보임 | board_main.html | 시안 L982 인박스 탭 · SPEC-002 E16 |
| 시술 중 | 보임 | board_parts.html | 시안 L897 · SPEC-002 규칙 19 |
| 시술 현황 | 보임 | board.html · board_main.html | 시안 L720 헤더 탭 · SPEC-002 E07 |
| 시술 현황 · DAY | 보임 | board_main.html | 탭 제목 = 시술 현황(시안) + 제품 이름 |
| 시작 | 보임 | board_parts.html · ui.html | 시안 L1157 · SPEC-002 U-3 |
| 시작 가능 | 보임 | board_main.html | 시안 L1006 · SPEC-002 U-10 |
| 시작 대기 | 보임 | board_parts.html | 시안 L899 · SPEC-002 규칙 19 |
| 시작 취소 | 보임 | board_parts.html | 시안 L1233 · SPEC-002 U-7 |
| 없음 | aria · title | ui.html | 보이지 않음 — 차트 아이콘 aria-label(간호관리차트 없음) |
| 여 | 보임 | board_parts.html | 성별(시안 L1219 c.sex 앞 글자) |
| 오늘 | 보임 | ui.html | 시안 L735(날짜 이동 · 이 화면엔 안 씀) |
| 완료 | aria · title | ui.html | 시안 L1140 alt 「완료」 |
| 완료 취소 | 보임 | board_parts.html | 시안 L1233 · SPEC-002 U-7 |
| 응답 없음 | 보임 | board_parts.html | 시안 L957 · SPEC-002 E21 |
| 의사 검색 | aria · title | ui.html | 시안 L1085 aria-label |
| 의사 차트 | 보임 | ui.html | 시안 L1265 · SPEC-002 E55 |
| 의사 호출 | 보임 | ui.html | 원천 L95 「의사 호출」 머리 · SPEC-002 U-4 |
| 의사 호출 · | 보임 | board_parts.html | SPEC-002 U-3 「의사 호출 · N건」 · 원천 L100 |
| 의사를 선택하세요 | 보임 | ui.html | 원천 L99 꺼진 버튼 |
| 의사차트 | aria · title | ui.html | 시안 L1466 툴팁 |
| 이 화면을 볼 권한이 없습니다. 관리자에게 문의해 주세요 | 보임 | board.html | SPEC-001 대응표 forbidden |
| 이메일 | 보임 | login_card.html | SPEC-001 U-1 입력 |
| 이전 날 | 보임 | ui.html | 시안 L732(날짜 이동 · 이 화면엔 안 씀) |
| 인박스 | aria · title | board_main.html | 시안 L251 · SPEC-002 E15(aria-label) |
| 입력 삭제 | aria · title | ui.html | 시안 L1446 aria-label |
| 있음 | aria · title | ui.html | 보이지 않음 — 차트 아이콘 aria-label(간호관리차트 있음) |
| 재호출 | 보임 | board_parts.html · ui.html | 시안 L974 · SPEC-002 E22 |
| 전체 | 보임 | board_parts.html · ui.html | 시안 L1152 「전체 호출」 줄 · L1088 「전체」 라벨 |
| 전체 선택 | 보임 | ui.html | 시안 L1197 · SPEC-002 E40 |
| 전체 의사 | 보임 | board_parts.html | 시안 L956 |
| 전체 호출 | 보임 | board_parts.html | 시안 L957 |
| 접기 | aria · title | ui.html | 시안 L1221 aria-label |
| 조건 지우기 | 보임 | board_main.html | 시안 L1447 · SPEC-002 E27 |
| 조건에 맞는 고객이 없어요 | 보임 | board_main.html | 시안 L1447 · SPEC-002 E27 |
| 종료 | 보임 | board_parts.html · ui.html | 시안 L1156 · SPEC-002 U-3 |
| 준비중 | 보임 | ui.html | 시안 L1155 · SPEC-002 E41 |
| 진행중 | 보임 | ui.html | 시안 L1153 · SPEC-002 E41 |
| 차트 열기 | aria · title | ui.html | 시안 L1218 aria-label |
| 차트 종류 | aria · title | ui.html | 보이지 않음 — 차트 탭 tablist aria-label |
| 처음 호출 | 보임 | board_main.html | 시안 L1073 꼬리표 |
| 처음으로 | 보임 | login_card.html | 사용자 확인 — 근거 없음(병원 고르기에서 로그인으로 돌아가는 링크) |
| 초 | 보임 | day.js | 시안 L1168 「30초」 |
| 추천 | 보임 | ui.html | 원천 L97 「추천」 묶음 · 시안 L1064 |
| 콜 잡은 원장이 집도 | 보임 | ui.html | 원천 L97 |
| 크게 보기 | aria · title | ui.html | 시안 L1221 aria-label |
| 판 | aria · title | board_main.html | 보이지 않음 — 판 main aria-label |
| 현황 | 보임 | board_main.html | 시안 L982 인박스 탭 · SPEC-002 E16 |
| 호출 | 보임 | board_main.html · board_parts.html · ui.html | 시안 L982 인박스 탭 · E41 줄 상태 |
| 호출할 시술 · | 보임 | ui.html | 원천 L98 「호출할 시술 · N개」 |
| 화면 | aria · title | base.html | 보이지 않음 — 헤더 탭 nav aria-label |
| 확인 필요 | 보임 | board_main.html · board_parts.html | 시안 L1005 · SPEC-002 U-10 |