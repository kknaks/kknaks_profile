# prod-deploy-re1 frontend-1 결과 보고 — 차트 모달(E55) · 담당자 셀렉터 medikit 맞추기 (W1 · W2)

## 상태: done (커밋 · push 안 함 — 워크트리에 변경만)

## 수행 — 바뀐 파일

| 파일 | 줄 | 내용 |
|---|---|---|
| `backend/day/templates/ui.html` | :116 ~ :130 | `combobox` 매크로에 `label=""` 인자 추가 → 트리거 · 목록 `aria-label`(접근성 이름만 · 보이는 글자 아님). 기존 호출(kit_page)은 그대로 |
| `backend/day/templates/partials/board_chart_parts.html` | :24 ~ :28 | `author_span` 매크로 신설(작성자 자리 · OOB 겸용) |
| 〃 | :36 ~ :58 | `row` — `<select>` → `ui.combobox("chart-staff-<task>-<kind>", "staffId", …)` · 작성자 = `ms-hint day-chart__author` · 글 칸에 `day-textarea--chart` |
| `backend/day/templates/partials/board_chart_saved.html` | :13 | 저장 응답의 작성자 OOB 를 `charts.author_span(…, oob=true)` 로(같은 id · 같은 자리) |
| `backend/day/static/day.js` | :674 · :682 | 자동 저장이 `select[name=staffId]` 대신 `[name=staffId]`(콤보 hidden input)를 읽음 |
| 〃 | :837 ~ :839 | 담당자 고르면 바로 저장 — hidden input `change`(pickOption 이 이미 보냄)로 받음 |
| 〃 | :882 ~ :887 | 닫힌 콤보 트리거에서 ↑↓ = 목록 열기(예전 select 키보드와 맞춤 · 모든 콤보에 적용) |
| `backend/day/styles/app.css` | :150 ~ :155 | 토큰: 표 폭 760→880 · 시술명 열 150→200 · 담당자 열 170→180 · `--day-chart-field-h 36` · `--day-chart-hint-h 18` |
| 〃 | :509 ~ :527 | 표 · 머리 줄 · 행 · 시술명 · 작성자 · `day-textarea--chart` |
| `backend/day/static/day.css` | — | `scripts/build-css.sh` 로만 다시 빌드(손 수정 없음) |
| `backend/tests/day/web/test_board_page.py` | :705 ~ :745 | 차트 조각 시험을 콤보 마크업 기준으로 고침 · 읽기 전용 트리거 disabled · 작성자 hint · day.js 선택자 확인 |

## 쓴 medikit 컴포넌트

- **담당자 = `ui.combobox`(ComboBox m — `day-combo`, kit_page 견본 :129 ~ :132)**. 같은 화면의 G16 팝오버 체계(`data-day-pop` · fixed · 바깥 클릭 · Esc · ↑↓ · 포커스 복귀)를 그대로 쓴다. 고른 줄 = 파랑 배경 + ✓.
- 작성자 글 = **medikit `ms-hint`**(필드 보조 글 12px · gray-700).
- 표 = **medikit 표 모양**(`.ms-table-wrap` 테두리 gray-200 · 모서리 12 / `.ms-table th` = primary-100 바탕 · 600 · 12px · gray-300 아랫선 · 10px 16px 여백 / td = 위 선 gray-200 · 12px 16px). 줄마다 `<form>` 이라 `<table>` 대신 grid 에 같은 토큰 값을 줌.
- 글 칸 = 기존 `ui.textarea`(day-textarea) + 차트용 크기 수식 `day-textarea--chart`(ComboBox m 과 같은 테두리 · 모서리 6 · 가로 여백 16).

## 어긋남 1 ~ 6

1. **브라우저 기본 select** → medikit ComboBox(위). 읽기 전용 = 트리거 `disabled`. 자동 저장 트리거(고르면 바로 · 칸에서 나갈 때) 그대로.
2. **글자 줄 안 맞음** → 기준 = 36 칸 글자 줄. 시술명 `padding-top 8` · 콤보 36 가운데 · 글 칸 `padding 7px 16px`(1+7 = 8). 세 칸 첫 줄이 같은 높이(캡처 확인).
3. **이메일 줄로 행 높이 들쭉날쭉** → 작성자를 담당자 아래 `ms-hint` 자리로 두고 **비어도 한 줄(18px) 자리 유지 · 넘치면 말줄임(title 에 전체)**. 글 칸 처음 높이 = 36 + 4 + 18 = 58(두 줄) → 작성자 있든 없든 행 높이 같음. 글이 길면 글 칸만 늘어남(최대 150 · 기존 토큰).
4. **드롭다운 · 글 칸 크기 · 테두리 다름** → 둘 다 gray-300 1px · 모서리 6 · 가로 여백 16 · 첫 줄 높이 36 기준.
5. **열 너비** → 모달 760 → 880, 시술명 200(「바디보톡스 하이톡스 100unit」 한 줄) · 담당자 180 · 차트 나머지(약 450).
6. **머리 줄 약함** → medikit 표 머리(옅은 파랑 바탕 · 600 · 아랫선) + 표 테두리 · 모서리. 머리 줄은 본문 스크롤 때 위에 붙음(sticky — ms-table th 와 같게).

탭 · 「최근 저장 : HH:MM」 · 닫기 · flash(줄 깜빡임) · 409 충돌(줄 OOB 통째 교체 + 토스트) 마크업 · 동작 그대로. 문구 추가 · 변경 없음(콤보 placeholder 도 빈 글자 — 예전 빈 option 과 같음).

## 이메일 줄 원인 (코드)

- 그 회색 줄은 **담당자가 아니라 「작성자」**(SPEC-002 :325 · 규칙 32 — 줄마다 마지막 저장 계정 · KOS 면 「KOS」 · 「자리 · 모양은 디자인」). `board_chart_parts.html` `author_text` ← `services/board_rules.py:666 chart_cell` 의 `author = {"name": s.name}` (`self.w.staff[log.author_staff_id].name`).
- 저장 이력이 있는 줄에만 나온다(이력 없는 줄 = 빈칸 · 그래서 행마다 있다/없다).
- 이메일로 보이는 이유 = **그 직원 행의 `name` 값 자체가 이메일**(서비스는 이름 칸을 그대로 쓸 뿐, 이메일로 대신 채우는 코드는 없음). W2 의 「닫힌 칸엔 이름 · 열린 목록엔 이메일」도 같은 원인으로 보임 — 담당자 목록도 `chart_options` 가 같은 `s.name` 을 씀 → 이름이 이메일인 직원 행이 따로 하나 있을 가능성(데이터 확인 필요 · 프론트 범위 밖).
- 이번 변경: 글자는 그대로 · 자리만 medikit 보조 글 자리(높이 고정 · 말줄임)로.

## 검증

- `uv run pytest -q backend/tests/day/web/test_board_page.py -k 차트` → **6 passed**
- 겸사 `uv run pytest -q -m "not infra" backend/tests/day/web backend/tests/architecture` → **113 passed**
- `scripts/build-css.sh` 1회 → `day.css 53.2KB (tailwindcss 4.3.4 · medikit 1.4.0)`
- `uv run ruff check backend` → All checks passed (테스트 파일 ruff format 적용)
- 인라인 스크립트 · style 속성 · eval: 바뀐 템플릿 · day.js diff 에서 **0건**(grep). day.css 는 빌드 산출물만.
- 캡처(가짜 값 · 템플릿 렌더 → headless Chrome · 사용자 포트/프로세스 안 건드림): `fe-captures/fe1-chart-nurse.png` · `fe1-chart-doctor.png` · `fe1-chart-doctor-list-open.png`(목록 연 모습 — 캡처용으로 목록을 흐름 안에 그림 · 실제는 트리거 아래 떠서 행을 밀지 않음)
- **pending**: 실제 브라우저에서 클릭으로 고르기 → 자동 저장 POST · 409 충돌 줄 교체 뒤 콤보 동작 · 모달 안 스크롤 때 목록 따라가기 — e2e/격리 스택 확인 필요(코드상 기존 popover 처리 그대로 탐).

## 계약 대조

- 라우트 · 폼 필드 이름(`chart` · `body` · `staffId` · `baseLogId`) · `hx-post` · `hx-trigger="day:chart-save"` · `hx-params` · OOB id(`chart-base-*` · `chart-author-*` · `chart-saved-*` · `chart-row-*`) · 읽기 전용(edit 없으면 hx 없음 · disabled · readonly) — **같음**.
- 서버 · 서비스 · 스펙 변경 없음.

## 이슈 · 코디가 확인할 것 (정할 것)

1. **이메일이 이름 칸에 들어간 직원 행** — 데이터(직원 동기화 · 로그인 계정 생성) 쪽 확인이 필요. 화면은 받은 이름을 그대로 보임.
2. **빈 담당자 고르기 없음** — 예전 select 의 빈 option(담당자 비우기)은 콤보에 넣지 않음. 비우면 저장이 안 되는(필수) 값이라 동작 차이는 없음. 필요하면 말해 달라.
3. 담당자 값이 목록 밖(퇴사 · 직무 바뀜)이면 비운 채 그림 — 예전 select 도 같은 결과(빈 option 선택)라 맞춤.
4. 모달 폭 880 · 열 너비는 시안이 없어 정한 값(토큰 3개 · app.css :150 ~ :155) — 바꾸기 쉬움.
5. ↑↓ 로 닫힌 콤보 열기는 다른 화면 콤보에도 적용됨(키보드 보강 · 문구 · 모양 변화 없음).

---

## 수정 1 (코디 수정 1 + 보충 1 ~ 4 · 사용자 2026-11-11) — 상태: done

### 무엇을 바꿨나
| 지시 | 결과 | 파일:줄 |
|---|---|---|
| 수정 1 — 세 칸 높이 = 글 2줄 · 넘치면 칸 안 스크롤 | 시술명 · 담당자 · 글 칸 모두 `--day-chart-row-h`(36 + 22 = 58 = 글 2줄) 고정 · 시술명 · 글 칸 `overflow-y: auto` · 글 칸 자동 늘어남(field-sizing content · 최대 150) 끔 | `styles/app.css` :153 ~ :156 · :523 ~ :533 |
| 보충 1 — 작성자 회색 글 뺌 | 줄의 작성자 자리 · 저장 응답 작성자 OOB 를 지움. 서버 `author` 값 · 이력 데이터는 그대로(화면만) | `partials/board_chart_parts.html`(author_text · author_span 매크로 삭제) · `partials/board_chart_saved.html` :12 |
| 보충 2 — 이름 앞 직군 | `staffOptions[].job` 추가: 원장 목록 = `doctor` · 간호관리 = 태그 `nurse` 하나 → `nurse` · `skincare` 하나 → `skincare` · **둘 다 → None(안 붙임)**. 화면 글자 = 「간호」 · 「피부관리」 · 「원장」(옅은 보조 글 `.day-opt__job`) — 목록 줄 · 닫힌 칸 둘 다. 정렬 · 범위 · 저장 계약 그대로 | `dtos/board.py` :24(BStaff.tags) · `queries/board.py` :320 · `services/board_rules.py` :685 ~ :704 · `partials/board_chart_parts.html` :14 · :36 ~ :45 |
| 보충 3 — 의사 호출 고르기 목록과 통일 | 의사 호출 창의 사람 줄을 공통 매크로 `ui.person_opt`(라디오 + 원형 이니셜 아바타 + 이름 · caller = 줄 끝)로 뽑아 의사 호출(_call_body)도 그대로 그걸 씀(출력 · 동작 같음). 새 `ui.staff_picker` = 닫힌 칸(ComboBox m 트리거) → G16 팝오버(모달 안 모달 아님 · `day-pick day-pick--single`): 검색(`ui.search` · medikit 필터) + 사람 목록(스크롤) + 고른 줄 파랑. 상태 글자(추천 · 모든 의사 · 비어 있음 · 시술 중) 없음. 아바타 톤 = 목록 이름 순 % 3(판 원장 톤 규칙과 같음) | `templates/ui.html` :386 ~ :418 · :438 ~ :441 |
| 〃 동작(day.js) | 라디오 name = `staffId`(폼 값 그대로). 고르면 닫힌 칸 글자(직군 + 이름) 바꾸고 → 닫고 → 자동 저장. 열면 검색 칸에 포커스 · ↑↓ = 줄 이동(보이는 줄만) · Enter / Space = 고르기 · Esc · 바깥 클릭 = 닫기 · 닫힌 칸에서 ↑↓ = 열기. 저장 값 읽기 = 고른 라디오(`chartStaff`) | `static/day.js` :143 · :672 ~ :683 · :838 ~ :847 · :880 ~ :905 |
| 보충 4 — 머리 = 판 카드 고객 줄 | `ui.customer_line(button=false)`(E37 이름 · 한글 발음) + `ui.vital`(E38 성별 \| 만 나이 \| 국적) — 판 카드와 같은 매크로 · 같은 값 처리(성별 male/female → 남/여 · 만 나이 = 차트 `visitDate` 기준 · 국적 그대로 · 값 없으면 안 보임). 차트 JSON customer 에 `gender` · `birthDate` 추가(판 스냅샷 :801 과 같은 방식) | `services/board_rules.py` :967 ~ :975 · `partials/board_chart_parts.html` :57 ~ :63 · `styles/app.css` :513 ~ :515 |
| 문구 근거 표 | 「간호」 · 「피부관리」 · 「원장」 근거(사용자 2026-11-11) 등록 | `tests/architecture/test_screen_copy.py` :103 ~ :105 |

### 검증
- `uv run pytest -q backend/tests/day/web/test_board_page.py backend/tests/day/board/test_board_rules.py -k 차트` → **9 passed**(조각: 고르기 목록 · 직군 · 아바타 · 2줄 CSS · 작성자 없음 · 머리 바이탈 / 값 없음 · 저장 OOB 에 작성자 없음 / 규칙: chart_options job — nurse · skincare · 둘 다 None · doctor)
- `uv run pytest -q -m "not infra" backend/tests` → **879 passed**(architecture 경계 · 문구 근거 · 클래스-CSS 대조 포함)
- `scripts/build-css.sh` → `day.css 53.5KB` · `uv run ruff check backend` · `ruff format --check` 통과 · 인라인 스크립트 · style 속성 · eval 0
- **pending**: infra 시험(`scripts/test.sh` — 실제 PostgreSQL · chart API 의 staffOptions · customer 새 칸)은 사용자 포트 · 프로세스를 건드리지 않으려 안 돌림. 실제 브라우저에서 고르기 → 자동 저장 POST · 409 뒤 다시 그린 줄의 고르기 동작도 e2e pending.
- 캡처(가짜 값 · 템플릿 렌더 → headless Chrome): `fe-captures/fe1b-chart-nurse.png` · `fe1b-chart-doctor.png` · `fe1b-chart-doctor-picker-open.png`(목록 연 모습). 목록 연 캡처는 headless 가 캡처 때 창 크기를 바꿔(day.js 는 resize 에 팝오버를 닫음) 캡처 하네스가 열린 상태 · 위치(트리거 아래 6px — placePop 과 같은 값)를 강제로 그렸다 — 하네스 전용, 저장소 코드 아님.

### 정할 것 (수정 1)
1. **직군이 둘 다(nurse + skincare)인 직원** — 지금은 직군 글자 없이 이름만(`job: None`). 「간호」 · 「피부관리」 중 하나 / 둘 다 표시 / 다른 글자 중 정해 달라.
2. 간호관리 목록에서 nurse · skincare 어느 것도 아닌 직원은 목록에 안 들어온다(범위 그대로) — 해당 없음.
3. 글이 2줄을 넘는 글 칸은 셋째 줄 윗부분이 아래 여백으로 살짝 보인다(칸 안 스크롤의 보통 모양) — 그대로 둠.
4. 「이름이 이메일인 직원」(위 이메일 줄 원인)은 고르기 목록에서도 이메일로 보인다(w02b 그림과 같음) — 데이터 쪽.
5. 직군 매핑(태그 → 글자)은 화면(JOBS)에 있음 · API 는 코드값(`nurse` · `skincare` · `doctor`)만 — 앱이 쓸 때도 같은 매핑 필요.

---

## 수정 2 (코디 수정 2 · 코드 리뷰 review-code-3 W1) — 상태: done

### 무엇을 바꿨나 (`backend/day/static/day.js` 만 + 시험)
| 항목 | 결과 | 줄 |
|---|---|---|
| ←→ 로 옆 사람 저장(W1) | 담당자 목록(`[data-day-staff-list]`) 라디오에서 ArrowLeft/Right 를 `preventDefault` 하고 ↑↓ 와 같은 **줄 이동(포커스만)** 으로 돌림 → 키 하나로 고르기 · 저장 · KOS 쓰기가 생기지 않음. ↑↓ 는 원래부터 막혀 있음 | :904 ~ |
| 줄 이동 공통 | 메뉴 · 콤보 · 담당자 목록 ↑↓ 처리를 `moveInPop(step)` 하나로(동작 같음) | :166 ~ |
| Enter · Space | 고르기 = `click()` · **이미 고른 사람이면 저장 없이 닫기** | :904 ~ |
| 이미 고른 사람 다시 누르기 | 줄(label)을 누를 때 그 라디오가 이미 checked 면 저장 없이 닫기(change 없음). 라벨이 라디오에 보내는 두 번째 click(target = input)은 보지 않음 | :760 ~ |
| 의사 호출 목록 | 선택자를 `[data-day-staff-list]` 로 좁혀 영향 없음(의사 호출 목록엔 이 속성 없음 · ↑↓ 처리 결과 같음) | — |

### 검증
- `uv run pytest -q backend/tests/day/web/test_board_page.py -k 차트` → **6 passed**(day.js 선택자 확인 — ←→ 막기 · 줄 이동 · checked 면 닫기 · 다시 누르기 닫기)
- `uv run ruff check backend` 통과 · `node --check day.js` 통과 · CSS 변경 없음(빌드 안 함)
- 동작 확인(headless Chrome · 가짜 값 · 렌더된 모달에 실제 이벤트): 열면 검색 칸 포커스 → 고른 줄에서 ArrowRight = `defaultPrevented=true` · 고른 값 그대로(d2) · 포커스만 다음 줄(d3) → 고른 사람 다시 누름 = 닫힘 · 값 그대로 → 다른 사람 누름 = 닫힘 · 값 바뀜 · 칸 글자 「원장 김도윤」 → 고른 줄에서 Enter = 닫힘
- pending: 실브라우저 e2e(실제 저장 POST)

### 정할 것 (수정 2)
- 없음. 리뷰 W2(SPEC-002 개정 — 작성자 안 보임 · `job` · `customer{gender, birthDate}`)는 코디 몫.

---

## 수정 3 (코디 수정 3 · 사용자 지시 — 줄 배치 「아이콘 · 이름 · 직군」) — 상태: done

### 무엇을 바꿨나
| 항목 | 결과 | 파일:줄 |
|---|---|---|
| 목록 줄 | 아바타 → 이름 → **직군 오른쪽 끝**. 직군 = 의사 호출 상태 글자(「비어 있음」)와 같은 자리 · 같은 클래스 `.day-opt__status`(옅은 10/500 · 줄 끝). 이름 앞 직군은 뺌. 의사 호출 줄은 job 을 안 넘겨 출력 그대로 | `templates/ui.html` :390 ~ |
| 닫힌 칸(고른 값) | 이름 → 직군(`.day-opt__job` — 옅은 12/500 · 이름과 6px) | `templates/ui.html` :407 · `styles/app.css` :591 |
| 고를 때 칸 글자 | day.js 가 「이름 + 직군」 순으로 다시 씀(목록 줄의 `data-day-pick-job` 글자) | `static/day.js` :861 ~ |
| 직군 둘 다 | 그대로 글자 없음(`job: None`) | — |

### 검증
- `uv run pytest -q backend/tests/day/web/test_board_page.py -k 차트` → **6 passed**(줄 = 이름 뒤 `day-opt__status` 직군 · 둘 다 = 없음 · 닫힌 칸 이름 뒤 직군 · day.js 순서)
- `uv run pytest -q -m "not infra" backend/tests` → **879 passed** · `scripts/build-css.sh` → 53.5KB · `ruff check` · `node --check` 통과
- headless 동작: 다른 사람 고르면 칸 글자 「김도윤」+「원장」(이름 뒤) · 수정 2 키 동작(←→ 막기 · 다시 누르기/Enter 닫기) 그대로
- 캡처: `fe-captures/fe1c-chart-nurse-picker-open.png`(간호 · 피부관리 · 둘 다=글자 없음 줄 · 닫힌 칸 「가나다 간호」) · `fe1c-chart-doctor-picker-open.png` — 열린 상태는 하네스가 강제(수정 1 과 같은 방식)
- pending: 실브라우저 저장 e2e · infra 시험

### 정할 것 (수정 3)
- 없음(직군 둘 다 = 글자 없음은 수정 1 「정할 것」 1 그대로).

---

## 수정 4 (코디 — infra 시험 1건) — 상태: done
- `backend/tests/day/board/test_board_chart_api.py` :328 — `test_웹_차트_저장은_OOB_충돌이면_그_줄과_토스트_담당자_없음은_토스트_없음` 이 작성자 OOB(`chart-author-…`)를 찾던 줄을 사용자 결정(작성자 안 보임 · SPEC-002 개정 ⑱)에 맞게 바꿈: 저장 응답에 `chart-author-` 없음 + 이력 행 `author_staff_id` = 저장한 직원(데이터는 그대로). 코드 변경 없음.
- 검증: 격리 스택(compose 프로젝트 `day-fe-iso` · 127.0.0.1:11142 / 11143 · 새 비번 · 끝나고 `down -v` 로 지움 — 사용자 `day-local` 11040 ~ 11043 안 건드림)에서 `DAY_ENV_FILE=<격리 env> scripts/test.sh -q backend/tests/day/board/test_board_chart_api.py` → **11 passed** · ruff check · format 통과.
