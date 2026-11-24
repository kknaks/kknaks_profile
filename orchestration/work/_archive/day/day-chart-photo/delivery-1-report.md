# delivery-1 결과 보고 — SPEC-002 개정 ㉘ → WP 나누기 · Delivery Issue 발행

## 상태: blocked (Delivery Issue 발행 안 됨 — harness 가 baseline = fetch 한 origin/main 을 요구)

## 막힌 것

세 request 모두 `--plan` 에서 거절됐다. 우회하지 않았다 · apply 하지 않았다 · 승인 receipt 만들지 않았다.

```
$ uv run --project tools/harness mediness start-delivery \
    --request delivery/request-be-chart.json \
    --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec \
    --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo \
    --github-repo MediSolveAIDev/CENTURION_DAY --plan --json
exit=2
{"error": "requested SPEC baseline is not the fetched latest origin/main revision", "status": "conflict"}
```

- 요청 baseline = `a896cda0b9cfcc920b7c76ea1c278e8f697f9d28`(PR #960 · 머지 전) · fetch 한 `origin/main` = `c43633be698e1ebbc06ac9617a16262dacd1fac7` · `a896cda0` 는 main 의 조상 아님.
- 규칙: `tools/harness/references/requests.md` 첫 줄 「`spec_baseline_revision`은 command가 fetch한 Mediness `origin/main`과 같아야 합니다」.
- `be-photo` · `fe` 도 같은 오류(exit 2) — 출력 `delivery/plan-*.json`.

**지난번(SPEC-006)과 다른 점** — 그때는 target SPEC(SPEC-006)이 main 에 없어 main SHA + `spec-baseline:pending` 으로 시작할 수 있었다. 이번 target DAY-SPEC-002 · 001 은 **main 에 이미 stable 로 있다**(개정 ㉗ 까지). 그래서 main SHA 로 돌리면 pending 이 아니라 **ready — 개정 ㉘ 이 없는 옛 SPEC-002** 에 결속된다. 그 길은 규칙상 「Stable SPEC 이 있는 기능 고도화 = 지금 계약을 baseline 으로 고정하고 변화는 Target Delta 에 · 구현으로 확인된 변화만 merge 후 SPEC 에 반영」(`rules/delivery-workflow.md` :29)이지만, 이미 검수 PASS 한 개정 ㉘ 이 PR #960 에 따로 있어 「SPEC 이 둘」이 된다. 사용자 판단 몫이라 쓰지 않았다.

**풀기(둘 중 하나 — 사용자 · 코디 결정)**
1. **PR #960 머지** → 새 `origin/main` SHA 로 세 request 의 `spec_baseline_revision` 만 바꿔 `--plan` → `--apply`(만들어 둔 스크립트 `make_requests.py <새 SHA>` 와 같은 꼴 — 아래 「남긴 파일」). 셋 다 `L2` 라 첫 apply = `delivery-plan:review` → 승인 receipt = 사용자.
2. **PR #960 을 두고 main(`c43633be`) baseline 으로 시작** — ready · 옛 SPEC-002 + Target Delta(= 개정 ㉘ 내용 · 이미 request 에 다 있음). 구현 뒤 spec-sync 에서 #960 을 어떻게 합칠지 정해야 한다.

## WP(= Delivery Issue) 나누기 — 3개

`1 Delivery Issue = 1 Code PR`(별도 WP 원장 없음 — `rules/delivery-workflow.md`). SPEC-006 때처럼 백엔드를 둘로 나눴다 — 이유: 탭 저장(①)은 기존 차트 쓰기 · outbox · KOS 확인(C17)의 정합이 리뷰 축이고, 사진(②)은 새 외부 쓰기 경로(KOS 내부 이미지 · 직원 토큰 · 쓰기 큐 밖 직접 호출)라 축이 다르며 서로 코드가 겹치지 않는다. 헤더 로그인 표시(SPEC-001 ⑫)는 렌더 공통 값 한 줄 + 템플릿이라 ③ 에 넣었다.

| # | idempotency key | 범위 | 의존(실제 순서만) | 완료 조건 | migration | 되돌리기 |
|---|---|---|---|---|---|---|
| ① 백엔드 — 탭 저장 · C17 · 옛 경로 정리 | `day/day-spec-002-r28/be-chart` | `POST /board/visits/{id}/chart`(방문 잠금 · transaction 1) · 검사 순서 400 → 404 → KOS 읽기(transaction 밖 · `fetch_visit_tasks` · 시스템 계정) → 충돌(`baseLogId` · `base`) → 담당자 → 저장 · C17 탭 전체 거절 · 이어 붙인 칸 · `visit.chart_save` 1행 + outbox 묶음 + `task.doctor_change` 줄마다 · 열기 값 `base` · 옛 `POST /board/tasks/{id}/chart` · `/api/tasks/{id}/chart` 지움 | ③ 와 계약 K1 · K2 · K3 · K5 만(병렬) | A1 ~ A5(응답 모양 · C17 판정 · KOS 읽기 1회 transaction 밖 · event/outbox · 옛 경로 없음) + A6 실물 e2e | 없음 | Code PR revert(③ 과 같이 — 옛 경로를 지우므로) |
| ② 백엔드 — 시술전후사진 | `day/day-spec-002-r28/be-photo` | 목록 · 올리기 · 삭제 · 원본(계약 K4) · KOS 내부 이미지 7단계 · 직원 토큰 · 이름 매칭(`photo_code_missing`) · 썸네일 목록 때 서명 1회 → `data:` · 삭제 = 목록 → 삭제 → 목록 · 토큰 없음 / KOS 401 = `session_expired` · 그 밖 503 · KOS 호출 동안 transaction 없음 → `event_log` 따로 | ③ 와 계약 K4 만(병렬) · ① 과 독립 | A1 ~ A5(경로 · 권한 · KOS 호출 순서 · 칸 · 매트릭스 · transaction · event payload · DAY 저장 0) + A6 실물 e2e | 없음 | Code PR revert(KOS 시험 사진은 남음) |
| ③ 화면 — 모달 · 사진 탭 · 헤더 | `day/day-spec-002-r28/fe` | 탭 셋 · [저장](E57) · 「최근 저장」(E58) · 자동 저장 JS 걷어냄 · 탭 저장 폼(바뀐 줄만) · 미저장 확인 창(E59 · 기획 4-2 글자) · 충돌 그리기 · 사진 탭(구조만 · 글자 OQ-88 비움) · 헤더 로그인 표시(OQ-K21 답대로) · `board_chart_saved.html` 지움 · `verify-day-web/features/clinical-chart.md` 갱신 | ① · ② 계약(가짜 응답으로 병렬) | A1 ~ A7(모달 · 자동 저장 0 · 확인 창 · 충돌 · 사진 탭 · CSP · 헤더 · 문서) + A8 실물 e2e | 없음 | Code PR revert(① 과 같이) |

- 셋 다 `risk_level: L2` · `contract_version: 1` · Execution(code_surface · phases · verification · rollback) 채움(L2 의 `execution-plan:ready` 조건).
- **공통 실물 e2e**(세 Issue acceptance 같은 문장): 로컬 · KOS 데모 지점 · 시험 고객 — ⓐ 간호관리차트 여러 줄 [저장] → 「최근 저장」 · KOS 메모 확인 · 의사차트 따로 저장 ⓑ **충돌**: 창을 연 뒤 KOS 웹에서 같은 줄 메모를 먼저 고치고 [저장] → 409 · 저장 0 · KOS 글 + 줄바꿈 + 내 글 → 다시 [저장] → 저장 ⓒ **사진**: 「시술 전」 · 「시술 후」 1장씩 → KOS 웹 그 일정 사진 탭에 보임(분류 · 「태블릿」 · 메모) · 1장 삭제 → 사라짐 ⓓ 미저장 ✕ → 확인 창 → 「버리고 닫기」 → 요청 0. **순서**: ① · ② · ③ 이 모두 들어간 로컬에서 마지막으로 머지되는 Issue 가 1회.
- ② predeploy: 직원 토큰 + DAY 서버 UA 로 내부 이미지 경로가 받아지는지 데모 실물 1회(SPEC OQ-89 ⓐ).

## BE ↔ FE 계약(이름은 제안 — 두 PR 이 같은 글자로 맞춘다 · SPEC 계약은 바꾸지 않음)

| 계약 | 제공 → 소비 | 내용 |
|---|---|---|
| K1 차트 열기 | ① → ③ | `GET /board/visits/{visit_id}/chart` 그대로 · `tasks[].assignee` · `tasks[].doctor` 에 `base = {body, doctorStaffId}`(열 때 DAY 사본) · 탭 「최근 저장」 = `tasks[].{chart}.savedAt` 최댓값(템플릿 · 새 칸 없음) |
| K2 탭 저장 요청 | ③ → ① | `POST /board/visits/{visit_id}/chart` · `chart` + 줄마다 같은 이름 칸 반복(`taskId` · `body` · `staffId` · `baseLogId` · `baseBody` · `baseDoctorStaffId`) · 바뀐 줄만(안 바뀐 줄 칸 disabled) · 칸 수 다르면 400 · `X-CSRF-Token` |
| K3 탭 저장 응답 | ① → ③ | 200 = `partials/board_chart_tab.html`(값 `chart` · `tab` · `saved_at` · 줄마다 `base` · `baseLogId`) + 집도의 바뀌면 카드 · 원장 상태 OOB(+ `X-Day-Version`) / 409 `chart_conflict` = 저장 0 · 같은 조각 — 걸린 줄 이어 붙인 글 · KOS 담당자 · 새 `base` · `baseLogId` / 안 걸린 보낸 줄 = 요청 그대로 / 안 보낸 줄 = 지금 DAY 값 + 토스트 조각(글자 OQ-90) / 그 밖 = 지금 오류 토스트 |
| K4 사진 | ② → ③ | `GET …/photos` → `partials/board_photos.html` · `photos = {visit_id, edit, groups: [{category: before\|after, title, items: [{image_id, thumb(data: URI), shot_at}]}]}` · `POST …/photos`(multipart `category` · `file`) · `POST …/photos/{image_id}/delete` → 같은 조각 · `GET …/photos/{image_id}/original` → 바이트(`no-store`) · 오류 = 토스트(400 · 404 · 409 `photo_code_missing` · 401 `session_expired` · 503) |
| K5 옛 경로 | ① · ③ | 옛 `POST /board/tasks/{task_id}/chart` · `POST /api/tasks/{task_id}/chart`(라우트 · 서비스 — ①) · `partials/board_chart_saved.html` · day.js 줄 저장(③) 지움 |

주의(코디): ① · ② 의 화면 라우트(`routers/board.py` · 새 `routers/board_photos.py`)는 backend 브리프 템플릿의 allowed_paths(「routers/(api 제외) = frontend 몫」)와 부딪힌다 — SPEC-006 ①(#267)이 `routers/reservations.py` 를 backend 로 둔 선례를 따랐다. 브리프에서 정해 줄 것.

## baseline

- SPEC = DAY-SPEC-002 개정 ㉘ · DAY-SPEC-001 개정 ⑫ · 커밋 `a896cda0b9cfcc920b7c76ea1c278e8f697f9d28`(PR #960 · 머지 전) — harness 가 받지 않음(위). 세 request 의 Review Surface 첫 줄에 원천 · 커밋을 적어 둠.
- 코드 = CENTURION_DAY `origin/dev` `4bf0b4a1`(읽기만 · 경로 확인).

## 문서 변경

- `30-work.md` · `log.md` — **바꾸지 않았다**. Delivery 번호가 없어 Spec Coverage 를 이을 수 없다(SPEC-006 delivery-1 과 같음). 발행 뒤: SPEC-002 행에 `[#A] · [#B] · [#C](개정 ㉘)` · SPEC-001 행에 `[#C](개정 ⑫)` 를 더하고(구현 상태는 그 행의 기존 WP 와 함께 derive — 지금 `in_dev`) log.md 에 Delivery 발행 한 줄.

## 남긴 파일 (`day-chart-photo/delivery/`)

| 파일 | 내용 |
|---|---|
| `request-be-chart.json` · `request-be-photo.json` · `request-fe.json` | start-delivery request(결과 계약 + execution · 계약 K1 ~ K5 · e2e) — 풀기 1 이면 baseline SHA 만 바꿔 재사용 |
| `plan-be-chart.json` · `plan-be-photo.json` · `plan-fe.json` (+ `.err`) | `--plan` 출력(위 conflict) |
| apply json | 없음 — plan 이 막혀 apply 안 함 |
| `make_requests.py` | request 를 만든 스크립트 — 인자로 새 baseline SHA 를 받는다 |

## 미결 · 주의

- 풀기 1 / 2 결정(사용자).
- 셋 다 L2 → 첫 apply 뒤 사용자 승인 receipt.
- K3 충돌 토스트 · 사진 탭 글자(OQ-90 · 88)가 비어 있다 — FE 는 짓지 않고 비워 두거나 코디에 묻는다. 헤더 표시 모양(OQ-K21)도 답 전엔 자리만.
