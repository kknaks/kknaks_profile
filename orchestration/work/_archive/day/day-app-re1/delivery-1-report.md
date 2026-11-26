# delivery-1 결과 보고 — SPEC-003 ㉑ · SPEC-002 ㉚ → Delivery 2개

## 상태: done (Issue 2개 발행 · 둘 다 승인 대기 — 승인 receipt 는 만들지 않음 · 사용자 몫)

## Delivery Issue (MediSolveAIDev/CENTURION_DAY)

| request | Issue | 위험 | status | baseline | next_action | plan_digest |
|---|---|---|---|---|---|---|
| p1-backend | #281 | L3 | created | **ready** | review-delivery-plan | `sha256:3da6d383a548c526f3b79bee382fcf1dcef980c769f85085c1a7d5887cae2608` |
| p2-mobile | #282 | L2 | created | **ready** | review-delivery-plan | `sha256:3ff9a0e141d44eaf87ffb1045b067685090118928d020d43bf9e9ee66011babe` |

- 라벨 = `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready`. 승인 receipt(`{"decision":"approved","reviewer_type":"human","reviewer":"<사람>","plan_digest":"<위 값>"}`)는 사용자 몫이라 적용하지 않았다.
- 파일: `delivery/request-p1-backend.json` · `request-p2-mobile.json` · `plan-*.json` · `apply-*.json` · `*.err`(비어 있거나 uv 설치 줄만) · 생성 스크립트 `delivery/gen/make.py`

## baseline — 브리프와 다른 점 (꼭 읽어 주세요)

- `spec_baseline_revision` = Mediness `origin/main` **`b152d46325423848fb6682a4c18d3269748d6cb1`**. requests.md 첫 줄 규칙대로 fetch 한 origin/main 이어야 해서, 브리프의 「baseline = e7c51875」는 review_surface 에 SPEC 원천으로 적었다(앞 작업 #275 ~ #278 과 같은 방식). SPEC 원천 = PR #964(`e7c51875` + 이번 커밋 `319dd82e`).
- **harness 는 `spec-baseline:pending` 이 아니라 `ready` 로 판정했다.** `surfaces.py:99-123` 은 target SPEC 의 main 쪽 frontmatter `status` 만 본다. DAY-SPEC-002 · 003 은 main 에서 이미 `stable` 이라 ready 가 된다(앞 작업 SPEC-007 은 main 에 없어서 pending 이었다). request 에는 baseline 상태를 직접 지정하는 칸이 없다. 그래서 우회하지 않고 이 판정을 그대로 두었다.
  - 뜻: delivery-workflow 「Stable SPEC 이 이미 있는 고도화 = main 의 계약을 baseline 으로 묶고 바뀌는 내용은 Target Delta 에」 갈래다. 개정 ㉑ · ㉚ 내용은 각 Issue 의 Target Delta · Acceptance · 계약 C0 ~ C3 에 문장으로 들어 있다.
  - 승인이 나면 next_action 은 바로 `implement-and-open-code-pr` 가 된다(pending 단계가 없음). PR #964 를 머지한 뒤 새 main 으로 묶고 싶으면, 같은 idempotency key · contract_version 2 · 새 SHA 로 다시 실행하면 된다(결과 계약이 같으면 재승인 없음). 꼭 해야 하는 단계는 아니다.
  - 정말 pending 이어야 한다면 그 판단은 코디 · 사용자가 내려야 한다. 이 경우 harness 를 바꾸거나, PR #964 머지 전까지 승인을 미뤄야 한다.

## WP(= Delivery) 나누기

브리프에서 기대한 모양 그대로다(backend · mobile 둘). 판단 근거는 두 가지다. ① 코드 워크트리 하나(`kknaksss/day-app-re1`)에서 BE 는 `backend/` · `deploy/` 를, APP 은 `app/` 을 맡아 서로 겹치지 않는다. ② 앞 작업처럼(#275 ~ #278 → #280) Code PR 하나에 두 Delivery 를 함께 연결할 수 있다. 개발은 아래 계약 C 를 기준으로 병렬로 한다(APP 은 테스트 더블 사용). 실제로 순서가 걸리는 것은 APP 완료 조건의 시뮬레이터 실물 1회뿐이고, 이건 BE 구현이 끝난 뒤에 한다.

| WP | Issue | 범위 | 완료 조건 | migration | 되돌리기 | 의존 |
|---|---|---|---|---|---|---|
| BE | #281 | 앱 `/api` JSON 짝 6(차트 탭 저장 · 사진 목록 · 올리기 · 삭제 · 다시 시도 · 파일) · Bearer · 웹 경로와 같은 service · 규칙 · 오류 코드 · Caddy `/api/visits/*/photos` 100MiB · 머리 주석 정리 · 테스트(웹 경로 회귀 포함) | A1 계약 pytest · A2 웹 회귀 · ruff · A3 Caddy · **A4 로컬 BE + KOS 데모 지점 실물 호출 1회**(차트 GET → 탭 저장 → 사진 2장 → 목록 → 파일 → 삭제 → 다시 시도) | 없음 | Code PR revert | 없음(mobile 과 병렬) |
| APP | #282 | U-23 차트 화면(값 원천 차트 GET · 탭 셋 · 탭별 저장 · 충돌 · 거절 글자 · 담당자 고르기 · 닫기 표 D6′ · D12 · 사진 탭 · 10초 tick) · 세션 Navigator(D4 · D14 — 차트 · 원장 고르기 · 확인 시트 / 팝오버 · 창) · 까만 줄 테마(D9) · iOS 권한 문구(D15) · 폰 전체 화면 / 아이패드 가운데 창 · 테스트 | A1 A-51 ~ A-60 · A-17 · A-38 위젯 / 단위 테스트 · A2 테마 · 겹침 · Info.plist · 계약 시험 · A3 analyze · test · build ios --no-codesign · **A4 시뮬레이터 + 로컬 BE 로 저장 · 사진 1회** | 없음 | Code PR revert | A4 만 BE 구현 뒤 |

- 위험 등급: BE = **L3**(새 공개 API 가 KOS 외부 쓰기(차트 outbox · 사진 등록 · 삭제)를 부르고, 앞단 배포 설정도 바뀜). APP = **L2**(화면 · 동작이 넓게 바뀌지만 KOS 쓰기는 BE 를 거쳐서만 함). 둘 다 첫 apply 결과가 `delivery-plan:review` 다.
- 옛 `POST /api/tasks/{task_id}/chart` 는 SPEC-002 에 「지우는 대상」으로 적혀 있다. dev `55e60aa4` 의 `routers/api/board.py` 에는 이미 없다(grep 0건). 그래서 BE 할 일에는 「확인만」으로 넣었다.

## BE ↔ APP 계약 전문 (두 Issue 의 Target Delta 에 같은 문장 · DAY-SPEC-002 개정 ㉚ §3 「차트 · 사진 JSON 짝」 · DAY-SPEC-003 §3 「차트 · 사진 — 앱이 쓰는 칸」 인용 · 이름 제안)

**C0 공통** — 인증 = /api 공통(Bearer · CSRF 안 봄 · DAY-SPEC-001) · 권한 = 보기 `board` view(차트 GET · 사진 목록 · 파일) / 쓰기 `board` edit(탭 저장 · 올리기 · 삭제 · 다시 시도) · `is_admin` = 전부(C7) · 같은 service(board.save_chart_tab · visit_photos.list_photos · upload · delete · retry · open_file · open_tab · visit_photo_import.request_import · wait_imported) · 같은 규칙(규칙 23 대상 방문 · 31 검사 순서 · 충돌 · 39 사진) · 대상 방문 넓히지 않음(D8) · 오류 본문 = /api 공용 `{detail, code, field}`(+ `details`) · 코드 = 웹과 같은 코드: 400 `invalid_request` · `photo_type` · `chart_too_long`(자리만 — 지금 서버는 안 보냄) · 401 `session_expired`(직원 KOS 토큰 없음 포함) · 403 `forbidden` · 404 `not_found`(규칙 23 대상 밖 · 그 방문 줄 · 사진 아님) · 409 `chart_conflict` · `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · 413 `photo_too_large`(본문 상한 — 장당 초과는 `rejected`) · 409 · 503 `photo_disabled` · `photo_id` = DAY 행 id(`visit_photo.id` · KOS id 안 실음)

**C1 값 원천(이미 있음 · 바꾸지 않음)** — `GET /api/visits/{visit_id}/chart`(`board` view · routers/api/board.py:149-161) — 앱이 쓰는 칸 = `customer`{name, phoneticName, gender, birthDate, nationality} · `firstTab` · `tasks[]`{id, title, assignee|doctor: {body, staffId, logId, base{body, doctorStaffId}, savedAt, author}} · `staffOptions`{assignee|doctor: [{staffId, name, job}]}

**C2 차트 탭 저장(새)** — `POST /api/visits/{visit_id}/chart` · `board` edit · 요청 JSON `{chart: "assignee"|"doctor", rows: [{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}]}` — 그 탭 바뀐 줄만(1개 이상 · 그 방문 줄 · 같은 taskId 두 번 안 됨) · 빈 값 = `staffId` · `baseLogId` · `baseDoctorStaffId` 는 uuid 또는 `null` · `body` · `baseBody` = 문자열(빈 문자열 허용) · 칸 생략 · 모르는 칸 = 400 `invalid_request`(extra=forbid) · **`staffId = null` 은 400 이 아니라 서비스까지 가 409 `chart_staff_required`** · 응답 200 `{saved: [taskId], lastSavedAt, tasks: [{id, title, assignee|doctor: {body, staffId, author, savedAt, logId, base}}]}`(그 방문 줄 전부의 요청한 차트 종류 칸 · 저장된 줄은 새 logId · base · 안 보낸 줄은 지금 DAY 값) · 409 `chart_conflict` = 공용 오류 본문 + `details.conflicts: [{taskId, body, staffId, base: {body, doctorStaffId}, baseLogId}]`(아무것도 저장 안 됨 · body = KOS 글 + 줄바꿈 + 내 글 — 서버가 만듦) · 그 밖 거절 = 공용 오류 본문만 · 집도의를 바꾼 저장 = 판 바뀜 → 앱은 SSE `board` 로 받음

**C3 사진(새 다섯)** — ① 목록 `GET /api/visits/{visit_id}/photos?poll=&tick=`(`board` view · 없음 = 가져오기 작업 + 최대 3초 · `poll=1` = 다시 읽기만 · `tick=1` = 작업만 넣고 안 기다림) → `{visitId, reread, groups: [{category: "before"|"after", title, items: [{photoId, shotAt, kosSynced}]}]}`(묶음 둘은 빈 묶음도 늘 · title = 「시술 전」 · 「시술 후」 서버 TITLES · 순서 shot_at 오름차순 · `edit` 칸 안 실음 — 앱은 /me 권한) · ② 올리기 `POST /api/visits/{visit_id}/photos`(`board` edit · multipart `category` + `file` 여러 개 · 장당 5MB · JPEG · PNG · 장 수 한도 없음 · 본문 100MiB = 앞단 Caddy + 서버 BODY_MAX_BYTES) → 200 = 목록 모양 + `kosError`(없으면 null) + `rejected: [code]` · ③ 삭제 `POST /api/visits/{visit_id}/photos/{photo_id}/delete`(`board` edit) → 200 = 목록 모양 + `kosError` · ④ 다시 시도 `POST /api/visits/{visit_id}/photos/{photo_id}/kos-retry`(`board` edit) → 200 = 목록 모양 + `kosError` · ⑤ 파일 `GET /api/visits/{visit_id}/photos/{photo_id}/file`(`board` view · Bearer) → 웹과 같은 바이트 · 머리 `Cache-Control: no-store` · `Content-Disposition: inline` · `X-Content-Type-Options: nosniff` — 웹 사진 GET 둘의 쿠키 전용(`required_web_view`)은 그대로

**남은 선택(이름 제안)** — BE 가 코드를 확인한 뒤 확정한다. 이름 제안과 달라지면 두 워커와 코디에 먼저 알리고, spec-sync 때 DAY-SPEC-002 · 003 을 고친다. 대상은 DAY-SPEC-002 OQ-99(탭 저장 200 의 `tasks` 칸 · 409 걸린 줄을 `details.conflicts` 에 둘지 최상위에 둘지 · 사진 목록 `title`)와 OQ-100(PhotoError 413 · photo_type · photo_disabled 가 /api 공용 모양으로 나가는지 — 기본값 = 공용 모양 · 같은 코드)이다.

## 같은 커밋(`319dd82e`)으로 PR #964 에 얹은 것

- `30-work.md` Spec Coverage: DAY-SPEC-002 행에 「개정 ㉚ = #281 · #282」, DAY-SPEC-003 행에 「개정 ㉑ = #281 · #282」 추가(구현 상태 in_dev 그대로)
- `log.md` wp-add 한 줄
- SPEC 본문 변경 없음 · lint `--strict` = **0 error** · products/day 줄 0(WARN 263 은 전부 다른 제품 — 무관)
- PR #964 head = `319dd82e7f152dd31080d4b73faef8892340c955`(draft 유지 · 머지 안 함)

## 막힌 것 · 주의

- 막힌 것 없음.
- **baseline ready ↔ 브리프 pending 차이**(위 절) — 코디 확인 필요.
- 코드 워크트리는 깨끗했다(`55e60aa4` · 변경 없음).
- `40-architecture/deployment.md` 「앞단 본문 상한」 문장 갱신(SPEC-002 ㉚ DB 절에 「그 문서 갱신은 WORK」로 적혀 있음)은 mediness 문서라 Code PR 에서 하지 않는다. spec-sync 때 문서 PR 에서 한다.
- 브리프 §9 (2) 직접 주입(`orca terminal send`)은 dispatch preamble 이 「Slack · GitHub · 다른 채널에 올리지 말 것 · 보고는 orchestration 명령으로」라고 해서, preamble 의 worker_done 과 함께 코디 터미널 핸들로 보냈다.
