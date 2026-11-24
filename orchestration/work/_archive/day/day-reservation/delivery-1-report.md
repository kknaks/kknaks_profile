# delivery-1 결과 보고 — SPEC-006 → WP 나누기 · Delivery Issue 발행

## 상태: blocked (Delivery Issue 발행 안 됨 — harness 가 baseline = 머지된 origin/main 을 요구)

## 막힌 것

`start-delivery --plan` 이 세 request 모두에서 거절했다. 우회하지 않았다.

```
$ uv run --project tools/harness mediness start-delivery \
    --request delivery/request-be-read.json \
    --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec \
    --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation \
    --github-repo MediSolveAIDev/CENTURION_DAY --plan --json
exit=2
{"error": "requested SPEC baseline is not the fetched latest origin/main revision", "status": "conflict"}
```

- 요청한 baseline = `1870f68cd23633776a228d4c28e78f68a593cbca`(SPEC PR #958 커밋 · 머지 전)
- fetch 한 `origin/main` = `8aef9206036d076798242ca66abd30d644762180` · `1870f68c` 는 main 의 조상이 아님
- 규칙 근거: `tools/harness/references/requests.md` 첫 줄 「`spec_baseline_revision`은 command가 fetch한 Mediness `origin/main`과 같아야 합니다」 · `rules/delivery-workflow.md` 「SPEC은 … fetch한 latest origin/main의 exact Git object에서 읽습니다」
- `be-refresh` · `fe` 도 같은 오류(exit 2) — 출력은 `delivery/plan-*.json`
- **풀기**: PR #958 머지 → 새 `origin/main` SHA 로 세 request 의 `spec_baseline_revision` 만 바꿔 `--plan` → `--apply`. 세 Delivery 모두 `risk_level: L2` 라 첫 apply 는 `delivery-plan:review` 를 돌려준다 — 승인 receipt 는 사용자 몫(만들지 않음)
- 다른 길(main SHA + `spec-baseline:pending` 으로 시작)은 SPEC 이 이미 승인 · 작성돼 있어 사실과 맞지 않아 쓰지 않았다

## 남긴 파일 (`orchestration/work/day-reservation/delivery/`)

| 파일 | 내용 |
|---|---|
| `request-be-read.json` · `request-be-refresh.json` · `request-fe.json` | start-delivery request(결과 계약 + execution) — 머지 뒤 baseline SHA 만 바꿔 재사용 |
| `plan-be-read.json` · `plan-be-refresh.json` · `plan-fe.json` | `--plan` 출력(위 conflict) |
| apply json | 없음 — plan 이 막혀 apply 를 하지 않음 |

## WP(= Delivery Issue) 나누기 — 3개

harness 규칙상 별도 WP 원장은 두지 않고 `1 Delivery Issue = 1 Code PR` 이 단위다(`rules/delivery-workflow.md` 「원장과 evidence」). 그래서 WP 하나 = Delivery Issue 하나로 잡았다. SPEC-002 때의 #230(백엔드) · #231(화면) 나누기를 따르되, **백엔드를 둘로 나눴다** — 이유: 다른 날짜 최신화(②)는 지금 동기화 함수(`run_schedules` · `emr_kos_keys.apply_isolated` · `emr_sale_sync`)의 「오늘」 가정을 건드려 C1 ~ C3 를 지켜야 하는 위험한 쪽이고, 조회 · 권한(①)은 읽기만이라 리뷰 축이 다르다. 둘은 「요청 입구(task name · 인자)」 계약만 맞추면 병렬로 간다.

| # | Delivery(제목) | 범위 | 의존(실제 순서만) | 완료 조건 | migration | 되돌리기 |
|---|---|---|---|---|---|---|
| ① | 백엔드 — 조회 라우트 · 화면 값 · 권한 키 | `GET /reservations`(전체 · HX 조각 · 10초 폴링도 같은 경로 — DB 만 · KOS 안 부름) · view model(SPEC-006 「화면이 읽는 칸」) · 오늘 아닌 날짜를 열거나 바꿀 때 최신화 요청 1회 넣기(폴링은 안 넣음) · 권한 키 `reservation` view 모든 직무 기본값 행(R31 · `policies/permissions.py` · `services/default_permissions.py`) · `menu.py` 링크 | ② 의 요청 입구 **계약만** 먼저(구현은 병렬) | A1 ~ A4(조각 / 페이지 값 · KOS 호출 0 · 요청 넣기 횟수 · 권한 403 · 케이스 매트릭스 테스트) + 실물 e2e 1회 | 없음(권한은 행 · 새 칸 없음) | Code PR revert |
| ② | 백엔드 — 다른 날짜 최신화 중앙 작업 | worker task — (병원, 날짜) 요청 → 그 날 창으로 일정 → KOS 키 보충 → 구매 · 시술권 · 카드(R26 · R40) · 같은 (병원, 날짜) 잠금 · 주기 재최신화 없음 · 오늘은 안 씀 · 조건 C1 · C2 · C3 | ① 이 넣는 입구 계약(병렬) | A1 ~ A5(그 날짜 저장 · C1 중간 상태 안 보임 · C2 오늘 잠금에 안 건너뜀 · C3 구매 안 버려짐 · 동시 요청 한 번 · 오늘 회차 회귀 없음) + 실물 e2e 1회 | 없음(잠금 = Redis 키) | Code PR revert |
| ③ | 화면 — Jinja2 + HTMX 템플릿 · day.js | 시안 정본 · RV-01 ~ RV-41 · U-1 ~ U-7 · 날짜 바꾸기 조각 · `hx-push-url` · 10초 조각 폴링 · 필터(화면 안) · 툴팁 · 좌우 넘김 · 현재 시각 선 1분 · 오른쪽 패널(공지 / 「예약 요청」 제목만) · 문구 짓기 금지 · 인라인 스크립트 0 · 손 CSS 0 | ① 의 값 계약(가짜 값으로 병렬 · 마지막 e2e 만 ① 뒤) | A1 ~ A3(시안과 같은 모양 · 문구 · CSP · medikit 만 · 동작) + 실물 e2e 1회 | 없음 | Code PR revert |

- 병렬: ① · ② · ③ 동시에 시작 가능. 직렬인 것은 **실물 e2e** 뿐 — 세 PR 이 모두 있어야 「다른 날짜 열기」 e2e 가 의미 있음(③ e2e 는 ① 뒤 · 「다른 날짜」 e2e 는 ② 뒤).
- 공통 실물 e2e(각 Delivery acceptance 에 같은 문장): 로컬 · KOS 데모 지점에서 오늘 열기 · 다른 날짜 열기 · 같은 날짜를 두 창에서 동시에 열기.
- 위험: 셋 다 `L2`(넓은 behavior · 독립 review 가치) — ② 는 동기화 함수를 건드리지만 KOS 쓰기 · migration · 배포가 없어 L3 로 올리지 않았다(리뷰 시 L3 로 올릴지 사용자 판단 가능).

## BE ↔ FE 계약 (① ↔ ③ · ① ↔ ②)

이름은 모두 제안 — 각 Delivery 의 Code PR 에서 확정하고 서로 맞춘다. SPEC-006 계약을 바꾸지 않는다.

**경로(① 제공 · ③ 소비)**

| 경로 | 언제 | 응답 |
|---|---|---|
| `GET /reservations` | 첫 열기 · 새로고침 | 전체 페이지 |
| `GET /reservations?date=YYYY-MM-DD` + `HX-Request` | 꺾쇠 · [오늘] · 달력 · 10초 폴링 | 조각 `#reservation-main`(페이지 머리 날짜 · 표 · 오른쪽 패널) |

- 폴링과 날짜 바꾸기가 같은 경로라 **최신화 요청을 넣을지 구분이 필요** — 제안: 폴링 요청에 `HX-Trigger` 값(또는 쿼리 `poll=1`)을 실어 ① 이 요청 넣기를 건너뛴다. ① · ③ 가 같이 정한다(SPEC 은 「폴링은 요청을 넣지 않는다」만 정함 — R40 · R41).
- 400 `invalid_request`(날짜 형식) · 401 · 403(권한 행 없음) = DAY-SPEC-001 · 002 공통 오류 화면.

**view model(① → ③ 템플릿 값 · 제안 이름)**

| 값 | 내용(SPEC-006 근거) |
|---|---|
| `date` · `weekday` · `is_today` · `now`(오늘만) | 페이지 머리 · 현재 시각 선(U-4) |
| `axis` {start, end}(30분 · 08:00 ~ 24:00 · 축 밖 예약이면 늘림) | U-1 |
| `columns[]` {group_id, title, capacity_text(구역 1개만 숫자 · 0 / 2+ = 빈 값), interval_minutes, gray_spans[](운영 전 · 지난 시간 · 쉬는 시간 · 꺼짐 · 휴무)} | U-1 ~ U-3 · R33 |
| `cards[]` {visit_id, group_id, start_min, end_min, stack_index, name(발음 ∥ 이름), nationality(값 그대로 · 없으면 빈 값), is_new, state(reserved · reception · consultation_waiting · consultation · procedure_waiting · procedure · procedure_done · completed · canceled · no_show), payment_due(귀가 대기 ∧ 열린 구매), tooltip(시안 S5 글자)} | U-5 |
| `filter` {total(취소 · 노쇼 제외), counts{예약 · 접수 · 상담 중 · 시술 중 · 귀가 대기 · 귀가 · 취소}} | U-6 |
| `notice` {date_text, items[] {content}}(`released_at` 순 · null 안 보임) | U-7 |
| `reservation_request_title` = 「예약 요청」(제목만) | R32 |

- 색 · 문구는 템플릿(③)이 시안 토큰으로 그린다 — ① 은 상태 키만 넘긴다.

**최신화 요청 입구(① 넣음 · ② 받음 · 제안)**

- taskiq task `sync_reservation_date_hospital(hospital_id: str, date: "YYYY-MM-DD")`(이름 제안 · 기존 `tasks/emr.py` 꼴) · ① 은 `kiq` 만 하고 기다리지 않는다 · 잠금 · 중복 제거는 ② 안에서(같은 (병원, 날짜) 한 번).

## baseline

- SPEC = DAY-SPEC-006(stable) · 커밋 `1870f68cd23633776a228d4c28e78f68a593cbca` · PR MediSolveAIDev/mediness#958(머지 전) — harness 가 받지 않음(위)
- 코드 = CENTURION_DAY `origin/dev` `5ece25ea`(읽기만)

## 문서 변경

- `30-work.md` · `log.md` — **바꾸지 않았다**. Delivery 번호가 없어서(발행 안 됨) Spec Coverage 를 Delivery 로 바꿀 수 없다. 머지 · 발행 뒤 Coverage 행 = `[Delivery #A](…) · [#B](…) · [#C](…) | proposed`(lint 값 · 구현 시작 전) + log.md 에 Delivery 발행 기록 한 줄을 넣는다.

## 미결 · 주의

- PR #958 머지가 선행 조건 — 그 뒤 같은 request 로 재실행하면 된다(idempotency key `day/day-spec-006/be-read` · `be-refresh` · `fe`).
- 세 Delivery 모두 L2 → 첫 apply 뒤 사용자 결과 계약 승인(receipt) 필요.
- ② 의 위험 수준(L2 vs L3) — 동기화 함수 변경이라 사용자 판단으로 올릴 수 있음.
- 폴링 / 날짜 바꾸기 구분 방식(위 「경로」 아래 줄) — ① · ③ Code PR 에서 맞출 것.
