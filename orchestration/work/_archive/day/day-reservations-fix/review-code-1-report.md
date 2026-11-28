# 리뷰 리포트 — day-reservations-fix / code (2026-11-27)

대상: `CENTURION_DAY/day-reservations-fix` 미커밋 변경 전체(base `origin/dev` `65506f35` · 추적 50 파일 +1378 −536 · 새 파일 11) — #300 BE · #301 웹 · #302 앱 묶음. read-only(파일 수정 · stash · KOS · dev/prod 접속 없음).

## 판정: FAIL

FAIL 2(하나는 SPEC 빈칸 — 코디 결정 필요) · WARN 6 · 나머지 계약은 한 글자씩 맞음. 검증 재실행은 전부 초록(앱 1건 = base 기존 실패 · 확인함). **브리프의 「mypy 기존 실패」는 기존 실패가 아니다** — 워크트리 `.mypy_cache` 가 낡아서 생긴 것(아래 §검증).

---

## FAIL

### F-1 · 앱 [문진 QR] 이 `opened` 요청을 다시 쓰면 QR 화면이 1.5초 뒤 닫힘 — 담당 BE(+ 앱)
- 위치: `backend/day/services/displays.py:282-287`(D44 다시 쓰기 · `_open_link` 이 `rules.OPEN` = pending **·opened**) · `backend/day/routers/api/displays.py:102`(앱도 같은 `displays.create`) · `app/lib/ui/display_flows.dart:100-112` → `app/lib/ui/qr_screen.dart:126-131`(`status != 'pending'` 이면 `qrClosedLine` → 1.5초 뒤 `maybePop`).
- 재현 흐름: 웹에서 「링크 열기」(또는 고객이 링크를 열어 `questionnaire_public.py:257` → `opened`) → 같은 방문을 앱 [문진 QR] → 서버가 그 opened 행을 그대로 돌려줌(`qrUrl` 도 이제 opened 에 실림 — 주의 3) → 앱 QR 화면이 첫 폴링 · 신호에서 opened 를 읽고 「고객 폰에서 열렸어요」 뒤 닫힘. F6 처럼 **QR 이 떴다가 사라지는** 증상이 앱에서 새로 생김.
- 근거: D44(`_RESUME.md` §2 · 검수 1차 OQ) = 「링크 복사 · 열기는 **그 링크** 다시 씀」 — 웹 팝오버 두 줄 범위. 앱 「이 기기 QR」까지 바꾸는 결정은 없다. BE 보고 주의 3 이 「앱도 같은 service 라 다시 씀」이라고 적었지만 QR 화면의 닫힘 판정은 보지 않았다. 테스트는 이 경우를 덮지 않는다(`test_reservation_display_popover.py:62` 는 웹 form 경로 · pending).
- 고칠 방향(택1 · 코디): ⓐ 다시 쓰기는 `pending` 만(웹 「링크 열기」 뒤 「링크 복사하기」는 새 링크 — D44 문구와 조금 어긋남) ⓑ 앱 JSON 경로(`routers/api/displays.py`)는 다시 쓰지 않음(service 에 `reuse` 인자) ⓒ 앱 QR 화면이 「처음 받은 상태」 기준으로 닫힘을 판정(앱 고침). 가장 작은 고침은 ⓑ.

### F-2 · Rule 15 ⓖ — 다섯 자리가 모두 「행 넘는 첫 줄 카드」로 덮이면 다음 카드가 그 위에 겹쳐 그려짐 — 담당 SPEC 결정 → BE
- 위치: `backend/day/policies/reservation_layout.py:190`(`for strict in (True, False)` — 엄격 자리를 못 찾으면 `covered` 를 무시하고 다시 찾음) · `:169`(`covered` 는 strict 에서만) · `:218`(주석 「엄격하지 않은 빈 줄은 늘 있다」).
- 재현(스크래치에서 순수 함수 실행 · 파일 안 고침): 한 열에 12:30 ~ 13:30 카드 6장 + 12:40 ~ 12:50 1장, 오픈 12:00 →
  `lane 0~4 line 0`(5장 · 13:00 행으로 넘어감 → 12:00 행 아래 줄 0~4 자리 전부 `covered`) · 6번째 `lane 0 line 1` · 7번째 `lane 1 line 1` · 12:00 행 `lines = 2`.
  그림(웹 `resSpan` · 앱 `span` 둘 다): lane 0 첫 줄 카드는 12:00 행 아래 줄 띠(top+140 ~ 280)를 덮고 13:00 행으로 이어짐 → 같은 lane 0 · line 1 에 놓인 6번째 카드와 **겹침**.
- 근거: DAY-SPEC-006 Functional Rule 15 ⓖ 「그 사이 아래 줄 띠도 덮는다 — 그 자리는 아래 줄 자리 셈에서도 찬 자리」. 그런데 다섯 자리가 다 덮이면 그 행 아래 줄에는 놓을 자리가 **없다** — SPEC 이 답을 안 줌(빈칸). 구현은 조용히 찬 자리에 놓는다(「조용히 통과하는 자리」). 30분 어긋난 60분 예약 6장 = 사용자가 든 예(12:30 ~ 13:30)라 실제로 생길 수 있다. 테스트 `test_동시_6장이면_6번째는…`(`test_reservation_layout.py:100`)은 정각 시작이라 행을 넘지 않아 이 경우를 못 잡는다.
- 고칠 방향(코디 결정 뒤): ⓐ 덮인 자리가 다 차면 그 카드는 다음 행 첫 줄 셈으로 넘김 ⓑ 아래 줄 카드를 덮인 자리 오른쪽 6번째 칸(열 폭 +1)에 둠 ⓒ 「덮는다」를 그리기만으로 두고(아래 줄 카드가 위에 그려짐 · z-index) 받아들임. 어느 쪽이든 경우 테스트 1개를 더하고 `:218` 주석을 고친다.

---

## WARN

### W-1 · 회색 면 · 현재 시각 선 · [+] 칸의 y 매핑이 `lines ≥ 2` 행에서 카드 분 위치와 다름 — 웹 · 앱 **같은 식**(서로는 일치) — 담당 SPEC 결정 → 웹 · 앱
- 웹 `backend/day/static/day.js:2223`(`resYOf` = 행 top + 분 비율 × **행 전체 높이**(lines 포함)) · 앱 `app/lib/ui/reservation_table.dart:227`(`y()` 같은 식). 카드 · 띠는 ⓓ 대로 **첫 줄 띠** 안 분 비례(`resSpan` · `span`).
- 숫자: 12:00 행 `lines = 2`(280px) → 12:30 카드 top = +70 · 현재 시각 선 12:30 = +140 · 회색 면 12:00 ~ 12:30 = 0 ~ 140(첫 줄 띠 전체). [+] (`day.js:3077` · `:3792`): 첫 줄 띠 +70 ~ 140(카드로 치면 12:30 자리)을 누르면 **12:00** 칸 · 툴팁 「… | 12:00 ~」 · 12:30 [+] 는 아래 줄 띠 +140 에 그려짐.
- 근거: SPEC-006 U 절(`spec-006:185`) 「시간 칸 글자 · 회색 면 · 현재 시각 선 · 카드 세로 자리는 이 행 높이를 따라 계산」 — 카드만 ⓓ 로 정해지고 나머지는 모호. 6장 넘게 겹친 행에서만 생김. 앱 워커가 짚은 점과 같음 — **웹 · 앱 둘이 다르지는 않다**.
- 방향: 코디가 「분 → 첫 줄 띠」(회색 면은 그 행 모든 줄 띠에 같은 분 구간으로)로 정하면 두 화면을 같이 고친다.

### W-2 · 웹 열 바탕 격자 = 140px 반복 — `lines ≥ 2` 행 안에 이름 없는 가로선이 생김(앱은 행 경계에만 선) — 담당 웹
- `backend/day/styles/app.css:3354`(`.day-res-col::before` `background-size: 100% var(--day-res-slot)`) vs 앱 `reservation_table.dart` 행 경계 선(행마다 `Positioned` 1px). 12:00 행 lines 2 면 웹은 +140 에 선 → 시간 글자 없는 1시간 행처럼 보임. ⓙ 정각 아닌 오픈은 마지막 짧은 행만이라 괜찮음. 같은 그림(ⓗ 「픽셀만 화면마다」) 기준으로 보면 작은 어긋남.

### W-3 · 「링크 복사하기」 클립보드 — 실패해도 아무 표시 없음 · Safari 에서는 거의 늘 실패 — 담당 웹
- `day.js:5986` `navigator.clipboard?.writeText(url).catch(() => {})` 를 `htmx:afterRequest`(XHR 끝난 뒤)에서 부름.
- 위험도: Chrome · Edge(데스크 PC 기본) = 포커스된 탭이면 활성화 없이 됨 → 낮음. Firefox = 사용자 활성화 5초 안이면 됨 → XHR 이 빠르면 낮음. **Safari = 사용자 동작 안에서만** → 비동기 뒤라 `NotAllowedError` → 조용히 삼킴 → 직원은 복사된 줄 앎. 알림 글자 없음(OQ-D43)이라 실패를 알릴 길도 없음.
- 방향: 누를 때 `navigator.clipboard.write([new ClipboardItem({"text/plain": 응답 Promise})])`(Safari 가 받는 꼴) 또는 「지원 브라우저 = Chromium」을 운영 전제로 적어 둠. 코디 판단.

### W-4 · 죽은 코드(팝오버로 바꾸며 남음) — 담당 웹(+ BE)
- `backend/day/presentation/qr.py`(`qr_svg`) · `backend/day/web.py:28,184`(템플릿 전역) — 쓰는 템플릿 0(grep). `backend/day/styles/app.css:7387` `.day-res-dp__qr` (빌드된 `day.css:7259` 에도) — 쓰는 곳 0. `backend/tests/architecture/test_screen_copy.py:286` 「접속 중」 허용 줄 — 그 글자는 이제 안 그림(`reservations_display_targets.html` 이 「연결」/「미연결」로 바뀜).
- 방향: 지우거나(QR 그림을 이번에 안 쓰면) 다음 시안 때 다시 쓴다고 적음.

### W-5 · API 설명 글자가 바뀐 계약과 다름 — 담당 BE
- `backend/day/schemas/reservation_detail.py:139-141` `DisplayProgress.qrUrl` 설명 「열린(**pending**) 문진 요청…」 — 실제는 pending · opened(`services/displays.py:228` · `:546`). OpenAPI 에 나가는 계약 글자라 맞춘다.

### W-6 · 「6개월 경과」 글자는 고정 · 기간은 env — 담당 SPEC(참고) / 웹 · 앱
- `DAY_QUESTIONNAIRE_VALID_MONTHS`(`common/config.py:221` · 1 ~ 120)를 6 밖으로 바꾸면 화면은 여전히 「6개월 경과」(`reservations_display.html` `questionnaire_value` · `app/lib/core/reservation_copy.dart:82`). 결정 글자라 FAIL 아님 — env 를 바꿀 계획이 있으면 글자를 값에서 만들지 정한다.

---

## 직원이 실물에서 만날 자리
1. (F-1) 웹에서 「링크 열기」 한 뒤 앱 [문진 QR] → QR 이 잠깐 떴다 닫힘.
2. (F-2) 같은 그룹에 12:30 ~ 13:30 예약 6장 이상 → 카드 두 장이 겹쳐 보임 · 아래 카드 누르기 어려움.
3. (W-1) 줄이 접힌 행(6장 넘음)에서 빨간 현재 시각 선 · 회색 면이 카드 시각과 반 행쯤 어긋남 · [+] 툴팁 시각이 누른 자리와 다름.
4. 태블릿에 띄워 둔 상태에서 「링크 복사하기」를 누르면 태블릿 요청이 **닫힌다**(규칙 2 「같은 종류 새 요청이 열린 앞 요청을 닫음」 그대로 — 기기 없는 열린 요청이 없으면 새로 만들기 때문). SPEC 대로지만 직원은 「복사만 했는데 태블릿이 꺼짐」으로 느낄 수 있음 — e2e 때 확인 권함.
5. (W-3) Safari 데스크에서 「링크 복사하기」 → 아무 일 없음.
6. 다시 쓴 링크의 시한은 처음 만든 때 기준(10분) — 9분째 복사한 링크는 곧 만료.

## 참고(기존 부채 · 확인 결과)
- **mypy 「기존 실패」 = 낡은 캐시**: 워크트리 `.mypy_cache` 그대로 돌리면 `test_reservation_request_rules.py:191` 1 error. 새 캐시(`--cache-dir` 스크래치)로 돌리면 **현재 트리 742 파일 0 error** · base(`git archive origin/dev` 스크래치) 734 파일 0 error. 파일은 base 와 같음(diff 0). → `check.sh` 전에 `.mypy_cache` 를 지우면 통과할 것(코디 몫 · 나는 안 지움).
- 앱 `board_messages_contract_test` 실패 = **base 기존**: 웹 `routers/board_messages.py:51` 의 `memo_too_long` 이 앱 `core/copy.dart` 에 없음 — 두 파일 다 이 diff 에서 안 바뀜(`git diff --quiet` 확인).
- KOS 문진 읽기 호출 수: 제출 없는 · 기간 지난 연결 고객은 10초마다 1호출 · 상한 없음(사용자 받아들임 · BE 주의 5). 회차가 잠금 TTL(`sync_sales_lock_ttl_seconds`)을 넘기면 다음 회차와 겹칠 수 있으나 `apply_read` savepoint + 살아 있는 유일 인덱스가 중복을 막음.
- 제출 id 위치 미확인(BE 주의 2) 영향: 못 읽으면 DAY 제출 행이 기간 안인 동안은 읽기 자체를 건너뜀 → 기간이 지난 뒤 첫 회차에 같은 제출이 `read` 행 **1개** 더 생기고(그때 `external_ref` 를 남겨) 그 뒤는 없음. 최악 = 기간 지난 중복 1행. A7 e2e 로 확인할 항목 그대로.
- 띠 `end_min` 없을 때: 웹 `day.js:2295` = 시작 + 60 으로 그림 · 앱 `reservation_table.dart:413` = 안 그림. 서버는 늘 실으므로(옛 조각만) 영향 없음.
- `scripts/frontend/node_modules` 는 `.gitignore:29` 로 무시됨(커밋 위험 없음). 이 워크트리엔 설치돼 있지 않아 `node --test` 를 그대로 돌리면 모듈 없음으로 16 실패 — 스크래치 복사본에 `npm ci` 해서 돌림(아래).
- 활성 Python 700줄 이하: 바뀐 큰 파일 최대 `services/displays.py` 567줄.

---

## 계약 대조 표

| 계약 | BE(내는 쪽) | 웹(읽는 쪽) | 앱(읽는 쪽) | 결과 |
|---|---|---|---|---|
| ① `rows[] {start_min,end_min,lines}` / `startMin·endMin·lines` | `presentation/reservations.py:62` · `schemas/reservations.py:60-64` | `reservations_parts.html` `data-day-res-rows` · 시간 글자 `r.start_min`/`r.end_min` · `day.js resRows` | `model/reservation.dart` `ResvRow` · `ResvRows.of` | 같음 |
| ① `cards[] lane·line·start_min·end_min` | 기존 칸 + 길이 비례(`policies/reservations.py:_card_span` 최소 30분 없앰) | `data-day-res-lane/line/start/end` → `resSpan` | `c.lane·c.line·c.startMin·c.endMin` → `span` | 같음 · 화면 재계산 없음(ⓕ) |
| ① `bands[] … end_min` / Band `endMin`(새 칸) | `dtos:205` · `presentation:70` · `schemas:72,194` | `data-day-res-end` → `resSpan` | `_v(b,'end_min')`(snake·camel) → `span` | 같음(없을 때만 다름 — 참고) |
| ① 놓는 순서 · R73 · 동행 이웃 · 5 자리 · 아래 줄 · ⓖ | `reservation_layout.py` `seat/_units/_place_run` | — | — | ⓖ 다 덮인 경우 겹침(**F-2**) · 그 밖 같음 |
| ① R71 30분 분리 | `COMPANION_SLOT_MINUTES = 30` · `companion_slot` · `ROW_MINUTES = 60` 따로 | 누르기 단위 `RES_SLOT_MIN = 30`(배치 아님 · 주석 맞음) | — | 같음 |
| ①ⓔ 열 폭 + 오른쪽 70 | — | `--day-res-col-pad-r: 70px` · `day.js` `padR` | `resColRight = resCardW / 2` | 같음 |
| ①ⓗ 1시간 기본 높이 웹 140 · 앱 70×2 | — | `--day-res-slot: 140px` | `resHour = resSlot * 2` | 같음 |
| y 매핑(회색 면 · 현재 시각 · [+]) | — | `resYOf` 행 전체 높이 비례 | `y()` 같은 식 | 웹 = 앱 · 카드와는 어긋남(**W-1**) |
| ② [+] 툴팁 `title` · `interval_minutes` | 기존 | `data-day-res-col-title` · `data-day-res-interval` → 「{그룹} \| {시작} ~ {끝}」 | (앱 [+] 없음) | 같음 |
| ③ `questionnaire.expired` | `questionnaire_reads.summary` · `schemas/reservation_detail.py:48` | `qv.expired` → 「6개월 경과」 | `m['expired'] == true` → `resQuestionnaireExpired` | 같음 |
| ③ [문진 QR] 보이기 같은 조건 | `reservation_detail.py` `questionnaire_done = 행 ∧ 기간 안` | `ed.qr` | `actions.questionnaireQr` | 같음 |
| ③ KST 달력 · 말일 · env | `policies/questionnaire.py add_months/is_expired` · env 기본 6 | 서버 값만 | 서버 값만 | 같음(테스트 5) |
| ③ 다시 보내기 = 제출 행만 | `last_of(..., submitted_only=True)` | — | — | 같음 |
| ④ `GET …/display-targets?kind=` 요청 0 | 라우트 그대로 · 테스트 `test_버튼_누름_기기_목록만_요청_0` | `_pop_button` `hx-get` | (앱 기존 흐름) | 같음 |
| ④ `POST …/display-requests` form `kind` · `device_id` | `services/displays.create` | `_link_row`(kind) · 기기 줄 form(kind · device_id) | JSON `kind` · `deviceId`(기존) | 같음 |
| ④ D44 링크 다시 씀 · 기기 줄 취소 → 새 | `_open_link`(pending·opened) · `closing_on_new` | `[data-day-res-dp-link]` ← `q.qrUrl`(pending·opened ∧ 기기 없음) | 같은 service 를 앱 QR 도 탐 | 웹 같음 · 앱 QR 닫힘(**F-1**) |
| ④ 기기 줄 모양 · 미연결도 누름 | — | `{name} [점] {연결/미연결}` · `.is-on` 초록 · 기본 빨강 | — | 같음 |
| ④ D45 다시 그리기가 팝오버 안 닫음 | — | `resDetailRun` 팝오버 열림이면 미룸 · `day:pop-closed` 뒤 한 번 · 줄 고르면 미룬 것 버림 | — | 같음(e2e 확인 항목) |
| ⑤ F6 origin 하나 · `displays[].qrUrl` | `session.public_origin` 하나 · `detail_view(origin)` 필수 · 호출 8곳(웹 GET 상세 · 동행 저장 · 신분확인 · 웹 띄우기 2 · 앱 상세 · 앱 띄우기 · 앱 대기) | — | `DisplayProgress.qrUrl` 새 칸 | 같음(grep 전수 · 로컬 정의 0) |
| KOS 읽기 내부 경로만 · 공개 새 호출 0 | `PATH_Q_READ = visitor/questionnaire/v1/…/legacy` → `client.internal` · 공개는 기존 3개(양식 · 동의 · 제출)만 | — | — | 같음 |
| 400 = 없음 · 실패 격리 · 중복 `external_ref` | `identity.py:180-185` · `_read` 고객만 건너뜀 · `apply_read` 확인 + savepoint | — | — | 같음 |
| 별도 태스크 · 일정 결과 영향 0 | `tasks/emr.py` `.kiq` try/except · `day.emr.sync_questionnaires_hospital` · 주기 없음 | — | — | 같음 |
| migration 0032 인덱스만 · downgrade | `create_index` / `drop_index` · head 테스트 갱신 | — | — | 같음 |
| 화면 문구 새 글자 5개만 | — | 「링크 복사하기」 「링크 열기」 「연결」 「미연결」 「6개월 경과」 + 툴팁 꼴(결정) | 「6개월 경과」 | 같음 · 인라인 스크립트 · style 속성 0 · CSS 빌드 재현 통과 |
| 옛 30분 잔재 | `SLOT_MINUTES` · `_axis` 없앰 | `RES_SLOT_MIN = 30` = 누르기 단위만 · 66 = CSS 기본(인라인으로 덮음) | `resCardH = 66` = 폰 목록 · 짧은 카드 판정만 | 잔재 없음(죽은 QR 코드는 W-4) |

## 검증 수치(각 1회 · 이 리뷰에서 다시 돌림)

| 명령 | 결과 |
|---|---|
| `./scripts/test.sh --pure -q` | **2454 passed** · 890 deselected · 0 failed(124s) |
| `node --test scripts/frontend/tests`(워크트리 그대로) | 22 파일 중 16 실패 — **전부 `ERR_MODULE_NOT_FOUND`**(node_modules 미설치 · 코드 문제 아님) |
| 같은 테스트 · 스크래치 복사본 + `npm ci`(`npm run test`) | **135 / 135 pass** |
| `build.mjs --check`(CSS 재현) · `npm run lint`(ESLint · Stylelint) · `format:check`(Prettier) | 통과 · 통과 · 통과 |
| `ruff check backend scripts` · `ruff format --check` | 통과 · 777 파일 그대로 |
| `mypy`(워크트리 캐시) | 1 error `test_reservation_request_rules.py:191` |
| `mypy --cache-dir <새>`(현재 트리) / base(`origin/dev` 압축 풀기) | **0 error / 742 파일** · 0 error / 734 파일 → 낡은 캐시 탓 |
| `cd app && flutter analyze`(fvm 3.44.8) | No issues found |
| `cd app && flutter test` | **549 pass** · 81 skip · **1 fail** = `board_messages_contract_test`(base 기존 — `memo_too_long` · 이 diff 안 닿음) |
| Rule 15 경우 재현(스크래치 순수 실행) | F-2 겹침 확인 |

taut audit/check · infra 전체(`test.sh -q`)는 이번에 다시 안 돌림(BE 보고: taut 0 · 전체 3344 passed).
