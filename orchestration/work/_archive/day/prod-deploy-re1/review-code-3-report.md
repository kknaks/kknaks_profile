# 리뷰 리포트 — prod-deploy-re1 / code 3 · 웹 차트 모달 E55 (2026-11-11)

대상: 같은 워크트리 미커밋(HEAD `5f7806d3` 위) — `dtos/board.py` · `queries/board.py` · `services/board_rules.py` · `templates/ui.html` ·
`partials/board_chart_parts.html` · `partials/board_chart_saved.html` · `static/day.js` · `styles/app.css` · `static/day.css`(빌드) ·
`tests/architecture/test_screen_copy.py` · `tests/day/board/test_board_rules.py` · `tests/day/web/test_board_page.py`.
근거: fe-1-report.md 본문 + 「수정 1」 · e2e-feedback.md W1 · W2 · SPEC-002 U-14(:316-330) · :526(차트 JSON) · 레포 AGENTS.md 「웹 화면」.

## 판정: WARN

FAIL 0 · WARN 2 · 참고 4. 자동 저장 · 409 · 읽기 전용 · flash · 의사 호출은 그대로다. WARN 은 「목록에서 ←→ 키 = 바로 저장」 하나와
「사용자 결정이 스펙(SPEC-002)에 아직 없음」 하나.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/web backend/tests/day/board backend/tests/architecture` | **172 passed**, 87 deselected |
| `uv run ruff check backend` | All checks passed |
| 바뀐 템플릿 · day.js diff 의 `+` 줄에서 `<script` · `style=` · `eval(` · `on*=` · `http(s)://` | 0건 |

- infra(`test_board_chart_api.py` — 실제 PostgreSQL)는 사용자 포트 · 프로세스 금지라 안 돌림. `day.css` 는 다시 빌드하지 않았다(read-only — 파일을 다시 쓰게 됨). 클래스-CSS 대조 시험(architecture)은 통과.

## FAIL

없음.

## WARN

### W1. 담당자 목록에서 ←/→ 키를 누르면 옆 사람이 골라지고 바로 저장된다
- `templates/ui.html:403-411` 목록이 `name="staffId"` 라디오 묶음이다. `static/day.js:902-907` 은 ↑↓ 만 `preventDefault` 하고 ←→ 는 막지 않는다 → 브라우저 기본 라디오 동작이 옆 라디오를 **checked + change** 로 바꾼다 → `day.js:839-848` change 처리가 칸 글자를 바꾸고 닫고 `chartSave`.
- 의사차트에서는 집도의 저장이 수락 뒤면 곧바로 KOS 로 간다(SPEC-002 :320 「그 뒤에 고치면 바로 KOS」 · 집도의를 고르면 KOS 가 수락 → 진행 중). 키 하나로 의도 없는 KOS 쓰기가 생길 수 있다.
- 의사 호출 창은 같은 라디오지만 [호출] 버튼으로 보내므로 영향이 없다 — 차트에서 새로 생긴 자리.
- 고칠 방향: `[data-day-staff-list]` 안 라디오에서 ArrowLeft/Right 도 `preventDefault`(↑↓ 와 같은 줄 이동으로 돌리거나 무시). 시험은 day.js 선택자 확인 수준이면 충분(기존 방식).

### W2. 사용자 결정 둘이 SPEC-002 와 아직 어긋난다 — 스펙 개정 필요
- **작성자 안 보임**: SPEC-002 U-14 :325 「**작성자** — 줄마다 마지막 저장의 작성자(저장한 계정)를 보인다 · KOS 에서 바뀐 글이면 「KOS」(규칙 32)」. 이번 변경은 `board_chart_parts.html:1-5` · `board_chart_saved.html:12` 에서 화면 작성자를 지웠다(사용자 2026-11-11 「보여 줄 필요 없다」 — fe-1 수정 1 보충 1). 서버 · 이력 · API 의 `author` 는 그대로(맞음).
- **차트 JSON 모양이 늘었다**(웹 모달과 앱 `GET /api/board/visits/{id}/chart` 가 같은 dict — `routers/api/board.py:158-166` · `services/board_rules.py:959-986`): `staffOptions[].job`(`board_rules.py:686-703`) · `customer.gender` · `customer.birthDate`(`:971-973`). SPEC-002 :526 은 `staffOptions: {assignee: [{staffId, name}], doctor: [{staffId, name}]}`. 더한 칸뿐이라 앱(`app/lib/ui/chart_sheet.dart` 는 이름 · 발음만 씀)이 깨지지는 않지만, API 는 외부 계약(AGENTS.md 「작업 규칙」)이므로 스펙에 적어야 한다.
- 고칠 방향: 코디가 SPEC-002 개정 — U-14 「작성자」 줄을 「화면에 보이지 않음(데이터 · API 는 그대로)」으로 · U-14 「담당자」 줄에 직군 표시(간호 · 피부관리 · 원장 · 둘 다면 안 붙임 = 미결) · 머리 = 판 카드 고객 줄 · :526 에 `job` · `customer{gender, birthDate}`. 코드는 그대로 둬도 된다.

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 자동 저장 | PASS | 폼 값 이름 `staffId` 그대로(라디오) · `hx-params="chart,body,staffId,baseLogId"` 그대로(`board_chart_parts.html:38`) — 검색 칸(`chart-staff-…-q`)은 hx-params 밖. `chartStaff`(`day.js:674`)가 고른 라디오를 읽고, 비면 저장 안 함(`:684` · 필수 규칙 :321). 고르면 change → 바로 저장(OQ-41 기본값 그대로). 글 칸 blur · 2초 쉼 경로는 손대지 않음 |
| 409 충돌 | PASS | `board_chart_saved.html` 은 충돌이면 `charts.row(…, oob=true)` 로 줄 통째 교체(그대로). 교체된 줄의 picker 는 같은 id · 이벤트 위임이라 다시 동작. 작성자 OOB 한 줄만 빠짐(W2 와 같은 결정) |
| 읽기 전용 | PASS | edit 없으면 form 에 `data-day-chart-row` · `hx-post` 없음(그대로) · 트리거 `disabled`(`ui.html:405`) → 팝오버가 안 열림 · 글 칸 `readonly`. ↑↓ 열기도 `!comboTrigger.disabled` 확인(`day.js:899`) |
| flash | PASS | `data-day-flash` · `data-day-sec` 그대로(`board_chart_parts.html:38`) |
| 의사 호출 회귀 | PASS | `_call_body` 의 사람 줄을 `ui.person_opt` 로 뽑았다(`ui.html:387-395` · `:460-463`) — 라디오 name `pick` · `data-filter-text` · 아바타 · `data-day-pick-name` · 태그 · 상태가 caller 로 같은 자리에. `job` 기본 "" 이라 의사 호출엔 직군 글자 없음. ↑↓ 줄 이동 선택자 추가분은 `[data-day-staff-list]` 한정이라 의사 호출 목록에 안 걸림. 웹 시험(의사 호출 포함) 통과 |
| BStaff `tags` 번짐 | PASS | 끝자리 기본값 `frozenset()`(`dtos/board.py:24`) — 위치 인자 생성(`routers/kit_board.py:60-63`)은 그대로. BStaff 를 직렬화(`asdict` 등)하는 곳 없음 · 판 스냅샷 · 다른 API 에 tags 가 나가지 않음 |
| `chart_options` `job` 번짐 | WARN(W2) | 호출처 = 차트 dict 하나 · 웹 모달 + 앱 차트 API. `JobRoleTag` 는 StrEnum 이라 `str()` = 코드값(`nurse` 등). 정렬 · 범위(`is_nurse`/`is_doctor`) · `chart_staff_listed` 그대로 |
| customer `gender` · `birthDate` 번짐 | WARN(W2) | 차트 dict 에만. 판 스냅샷 customer 와 같은 값 처리. 앱 `Customer` 모델은 이미 두 칸을 읽을 수 있으나 차트 시트는 쓰지 않음 |
| 지어 넣은 문구 | PASS | 보이는 새 글자 = 「간호」 · 「피부관리」 · 「원장」(사용자 2026-11-11 · `test_screen_copy.py:103-105` 근거 등록) · 성별 「남」 · 「여」(판 카드 GENDER 와 같음) · 검색 placeholder 「검색」(기존 `ui.search` 기본값). aria 이름 「… 담당자 검색」 은 기존 aria 글자 조합 |
| 인라인 스크립트 · style · CDN | PASS | diff `+` 줄 0건. `pop.style.*` 는 기존 placePop(JS) |
| medikit 모양 · 세 칸 2줄 고정 · 칸 안 스크롤 | PASS(코드 · 시험) | `app.css` 토큰 `--day-chart-row-h` · `max-height` + `overflow-y: auto`(시험 `test_board_page.py` 가 규칙 문자열 확인). 실제 브라우저 확인은 fe-1 pending 그대로 |

## 「조용히 통과하는 자리」

- 차트 API(앱 JSON)의 새 칸(`job` · `gender` · `birthDate`)은 규칙 단위 시험(`test_board_rules.py`)과 웹 조각 시험(가짜 dict)만 있고, 실제 API 시험(`test_board_chart_api.py:98-99`)은 `staffId` · `name` 만 본다 — 앱 쪽 모양이 바뀐 것을 API 시험이 모른다. W2 스펙 개정 때 `:98` 근처에 키 집합 단언 한 줄을 권한다(infra).
- day.js 동작(고르면 닫힘 · ↑↓ · Enter)은 시험이 선택자 문자열 존재만 본다 — 실제 클릭 · 키 동작은 e2e pending(fe-1 리포트와 같음).

## 직원이 실물에서 만날 자리

- W1: 목록에서 ←→ 를 누르면 옆 사람으로 바로 저장.
- 이미 고른 사람을 다시 누르면 change 가 없어 목록이 닫히지 않는다(Enter 도 같음 · `day.js:892-895` `t.click()`) — Esc · 바깥 클릭으로 닫힘. 작은 불편.
- 직군 둘 다(nurse + skincare)인 직원은 직군 글자 없이 이름만(fe-1 정할 것 1 · 미결).
- 이름 칸이 이메일인 직원 행은 목록 · 닫힌 칸 모두 이메일로 보인다(데이터 문제 · e2e W2 원인 · 화면 범위 밖).
- 닫힌 콤보 트리거 ↑↓ = 열기가 다른 화면 콤보에도 적용(키보드 보강 · 모양 · 문구 변화 없음 · fe-1 이슈 5).

## 참고

- 의사 호출 창과 차트 고르기의 아바타 톤 규칙(이름 순 % 3)은 같지만, 의사 호출 창은 목록 자리가 다르면 같은 원장도 다른 톤일 수 있다(기존 규칙 · 이번 변경 아님).
