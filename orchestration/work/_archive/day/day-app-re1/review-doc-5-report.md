# review-doc-5 — spec-sync-2 검수(SPEC ↔ 머지된 구현)

## 판정: **WARN**(FAIL 0 · WARN 7 · 참고 3)

- 대상: 스펙 워크트리 `day-app-re1-spec` 의 미커밋 변경(`git diff HEAD` · HEAD `538befe4`) 중 `products/day/`. 11개 파일, +83 −71.
- 정본: CENTURION_DAY `a76496c4`. `git show` · `git grep` 로만 읽었다(checkout 안 함).
- 결론: 처분표 1 ~ 8 은 모두 SPEC 에 들어갔다. D1 ~ D17 이름 · 코드 · 응답 칸은 코드와 글자까지 같다.
- 바꾼 hunk 마다 인용한 코드 줄을 전수로 대조했다. 뜻이 틀린 문장은 없다. 발명한 규칙 · 글자도 없다. main 쪽(#965 · #966 · #967) 줄도 건드리지 않았다.
- 남은 것은 작은 것들이다: 근거 줄 번호 하나가 낡음 · 칸 목록 하나 빠짐 · OQ 하나가 반만 닫힘 · 열린 OQ 요약 줄 하나가 낡음 · 조건 하나가 넓게 적힘.

## 검증

| 항목 | 결과 |
|---|---|
| `python3 scripts/lint-pipeline.py --strict` | exit 0 · 0 error · 263 warning · **`products/day` 줄 0**(warning 은 전부 다른 제품의 기존 것 — 무관) |
| 번호 참조(추가된 글에 나온 ID 전수) | OQ-119 · 120 · A83 · A84 · A90 · C7 · D06 · D29 ~ D31 · D39 ~ D42 · N25 · N26 · U-3 · U-26 · U-28 · U-30 · 개정 ㉒ · ㉜ · 고침 6 — 모두 정의가 있다. U-26 = 상세 · U-28 = 여권 스캔 · U-30 = 띄우기 받기로 문맥도 맞다. **끊김 0** |
| N22 → N26 고침 3곳 | SPEC-005 `:530` OQ-N26 = 띄우기 알림 채널(우리 것) · `:521` N22 = main 「KOS 에서 건 호출」. 고친 것이 맞다 |
| main 쪽 줄을 건드렸나 | 지운 줄마다 `ae8cec61`(main) · `a018f4fa`(우리 merge 전) 판과 대조했다. **main 에만 있는 줄 0.** 고친 줄은 모두 우리 줄이거나 merge 때 번호를 바꾼 우리 줄이다. 30-work 칸은 우리 Delivery 링크 뒤에 붙이기만 했다 |
| frontmatter `last_updated` | 바꾼 SPEC 7개 · 10-decision · 20-spec · 30-work · log 모두 2026-11-26 |

## 1. 처분표 1 ~ 8 반영 + 코드 대조(전수)

모든 줄 번호는 `a76496c4` 기준이다. ✓ = 글자 · 뜻이 코드와 같다.

### 1-1. be-2 D1 ~ D17

| # | SPEC 자리 | 코드 대조 | 결과 |
|---|---|---|---|
| D1 | SPEC-000 `:47` · `:51` · `:1203` · `:1242` 표 · SPEC-007 `:594` · `:773` · SPEC-003 `:1297` | `models/reception.py:34`(enum `questionnaire_crm_status`) · `:119-121`(`crm_status` · `crm_error` · `crm_sent_at`) · migration `:35-49` · `tests/day/test_models.py:90` `VENDOR_COLUMNS` 에 `kos_status` 있음 | ✓ |
| D2 | SPEC-003 `:645` | `schemas/reservation_detail.py:37-55` · `:171-176`(없으면 null) | ✓ 단 `canResend` 빠짐 → **W3** |
| D3 | SPEC-007 `:529` · `:571` · `:799` | `common/error_codes.py:30` · `day/errors.py:164-168`(409) | ✓ |
| D4 | SPEC-007 `:541` · `:594` | `error_codes.py:29` · `:31` · `errors.py:157-161` · `:171-175` · `questionnaire_kos.py:147` · `:163` | ✓ |
| D5 | SPEC-003 `:645` | `reservation_detail.py:63-66` · `:78` | ✓ |
| D6 | SPEC-005 `:50` · `:356` | `services/display_push.py:39-56`(`aps.alert{title, body}` · sound 없음 · 최상위 `kind` `"display"` · `environment` · `hospitalId` · `requestId`) · `PushLogic.kt:28` 채널 `display` · `:80` tag `display:{requestId}` | ✓ |
| D7 | SPEC-007 `:566` | `services/passport_scan.py:407` | ✓ |
| D8 | SPEC-007 `:541` | `schemas/displays.py:60-61` · `:73-74`(`str \| None` · 늘 넣음) | ✓ |
| D9 · D13 | SPEC-007 `:552` · `:800` · SPEC-003 `:645` | `policies/displays.py:50-68`(opened = 문진 · 스캔 같은 시한 · `del kind`) · `reservation_detail.py:120-134` | ✓ |
| D10 | SPEC-007 `:571` | `passport_scan.py:236-241` · `:309-310`(`_adapter` 앞) | ✓ 단 조건이 넓게 적힘 → **W7** |
| D11 | SPEC-007 `:591` · `:809` | `questionnaire_public.py:208-209`(502) · 직원 경로 `errors.py:78-82`(503) | ✓ |
| D12 | SPEC-007 `:597` | `questionnaire_public.py:68-73` REASONS · `:113-140`(row 없으면 로그만 · 1분 1줄) | ✓ |
| D14 | SPEC-006 `:460` | `schemas/reservations.py:15-150` — 최상위 `today` · `date` · `weekday` · `isToday` · `nowMin` · `openMin` · `axis` · `columns` · `cards` · `rows` · `bands` · `filter{total, counts}` · `notice{content, date}` · `inhouse{chips, items}` | ✓ |
| D15 | 바꿀 것 없음 | — | ✓(처분 맞음) |
| D16 | SPEC-007 `:548` · SPEC-003 `:1342` | `services/displays.py:78-83`(`sha256(b"day-qweb\|" + key)`) | ✓ |
| D17 | SPEC-007 `:548` · SPEC-003 `:1342` | `services/displays.py:131-133` | ✓ |
| 설정 이름 | SPEC-007 `:548` · `:594` · `:811` | `common/config.py:212`(`emr_http_timeout_seconds` 15) · `:215` · `:216` · `:218` | ✓ |

### 1-2. fix 라운드(F1 · BW · AW)

| # | SPEC 자리 | 코드 대조 | 결과 |
|---|---|---|---|
| F1 | SPEC-007 `:592` ① · SPEC-000 `:1240` · `:51` ② | `services/displays.py:452-475`(UPDATE … WHERE pending∧여는 시한 ∨ opened∧쓰는 시한 RETURNING) · `questionnaire_public.py:349-352`(못 잡으면 다시 읽어 410 / 409) · `:381-385`(IntegrityError → 409) · `reception.py:107` · migration `:50-56`(`deleted_at IS NULL`) | ✓ |
| BW1 | SPEC-007 `:592` · `:591` | `questionnaire_public.py:321-328`(Redis 잠금 실패 = 잠금 없이 진행) · `routers/api/public_questionnaire.py:60-72`(500 `internal_error` + PUBLIC_HEADERS) | ✓ |
| BW2 | SPEC-007 `:592` ③ ④ · SPEC-000 `:1242` | `public_questionnaire.py:130-134` · `questionnaire_kos.py:128-130` | ✓ |
| BW3 | SPEC-007 `:594` | `questionnaire_reads.py:19-32`(멈춤 = HTTP + 여유 · 회차 = HTTP + 여유/2) · `questionnaire_kos.py:93` · `:102-122`(`updated_at == stamp` 일 때만 씀) | ✓ |
| BW4 | SPEC-007 `:591` | `questionnaire_public.py:245-254` | ✓ |
| BW5 | SPEC-007 `:592` ① | 라우터 `:120`(`gate_post` = IP 5/분 → 토큰 없음) → `:121-129`(본문 400) → 서비스 `:315`(토큰 3/분) → `:317`(판정) · `LIMIT_POST_IP = 5` · `LIMIT_POST_TOKEN = 3`(`:55`) | ✓ |
| BW6 | SPEC-007 `:597` · OQ-D40 `:810` | `questionnaire_public.py:84-101`(Redis 실패 = 통과) · `:124-127`(간격 끔) | ✓ · 「유지 여부 사용자 확인 남음」 적혀 있음 |
| BW7 | SPEC-007 `:597` | 뜻 ✓ — `static/day.js:5643-5653`. **SPEC 이 적은 줄 `:5473-5487` 은 틀림** → **W2** | 줄 번호 낡음 |
| 스캔 칸 꼴 | SPEC-007 `:571` | `passport_scan.py:79-87` | ✓ |
| AW1 | SPEC-003 `:669` · `:851` | `PassportScanActivity.kt:98` · `ScanChannel.kt:63-72` · `scan_channel.dart:58-66` · `scan_screen.dart:134` · `:153` · `TextScanner.swift:82-84`(하는 일 없음) | ✓ |
| AW2 | SPEC-003 `:664` · `:851` | `PassportScanActivity.kt:213` · `:232` → `cameraFailed()` `:381-387` = `ScanHub.fail("no_camera")` | ✓ |
| AW3 | SPEC-003 `:664` | `scan_screen.dart:68-86`(`scanValueOk`) · `:89-93` · `:95-96`(대문자) · `:248-251`(`_canSave`) · `:454` · `:511` · `:519-539`(성별 · 다시 누르면 비움) · `reservation_copy.dart:196` `yyyy-MM-dd` | ✓ |
| AW4 | SPEC-003 `:664` | `mrz.dart:87-108`(`maxSwaps = 2`) · `:156-157`(바꿨으면 종합 검사) · `scan_screen.dart:471-473`(`warning_amber_rounded` · `Ms.yellow` · 글자 없음) | ✓ |
| AW5 | SPEC-003 `:683`(U-30) | `display_flows.dart:263-278` · `display_inbox.dart:79-83` · `reservation_api.dart:42-44`(close = `canceled`) | ✓ |

### 1-3. 항목 3 ~ 8

| 항목 | SPEC 자리 | 대조 | 결과 |
|---|---|---|---|
| 3 migration | SPEC-000 `:47` · `:51` ③ · SPEC-007 `:773` · SPEC-003 `:1297` | migration `:29` revision · `:30` down `0029_partner_charty` | ✓ |
| 4 국적/통역 | SPEC-007 `:146` · `:215` · `:823` · SPEC-003 `:645` | 웹 `templates/partials/reservations_detail.html:109` · 앱 `reservation_detail.dart:316-318` · `reservation_copy.dart:74-75`(「통역필요」 · 「대한민국」) | ✓ |
| 5 W3 | SPEC-003 `:616` · `:91` ② | `chart_photos.dart:205-225`(검정 · [닫기] · `BoxFit.contain`) · `app/lib` 전체에 `InteractiveViewer` 없음 = 「확대 · 이동 없음」 맞음 | ✓ |
| 5 W4 | SPEC-003 `:583` · `:91` ① | `chart_sheet.dart:272-273` | ✓ |
| 5 OQ-119 | SPEC-002 `:53` · `:739` · `:750` · `:1685` | `schemas/board.py:89`(`baseBody: str`) · `board_responses.py:512`(`body: str \| None`) · `chart_controller.dart:156`(`?? ''`) · `board_charts.py:18-57` · `schemas/photos.py:43` · `errors.py:233-244` | ✓ 단 SPEC-003 쪽 문장 → **W4** |
| 5 OQ-120 | SPEC-002 `:747` · `:1685` | `routers/api/board_photos.py:1-5`(공용 `{detail, code, field}` · 같은 코드) | ✓ |
| 6 OQ-A83 | SPEC-003 `:1160` · `:1164` · `:1628` · SPEC-004 `:638` · `10-decision.md:40` · `20-spec.md:104` | `app/ios/Runner/Info.plist:52-53` 과 글자가 같다(쉼표까지) · `_RESUME.md:126` 사용자 결정 | ✓ |
| 6 dev 메뉴 | SPEC-003 `:91` ⑥ 끝 문장 | 사실만 적음 · 바꿀 것 없음 | ✓ |
| 7 `_RESUME` §2 대조 | — | §2 2026-11-25 · 26 행(`:38-73` · `:125-127`)과 SPEC 을 다시 봤다. 빠진 계약 결정은 없다 | ✓ |
| 8 30-work · log | `30-work.md:9` · `:43` · `:45` · `log.md:5` · `:17` | 우리 Delivery 칸에만 붙임 · 상태 `in_dev` 그대로 · log 종류 enum 맞음 | ✓ |

## 2. 닫은 OQ · 열린 채 둔 것

| OQ | 근거 | 결과 |
|---|---|---|
| OQ-119 · 120(SPEC-002) | 구현(위) · `_RESUME.md:27` | ✓ |
| OQ-A83(SPEC-003) | 사용자 2026-11-26 · #296 | ✓ |
| OQ-N25(SPEC-005 `:529`) | `routers/api/notifications.py:136-144` `own_device` | ✓ |
| OQ-D29 · D30 · D31 · D39 · D42 · D06(SPEC-007) | 구현 줄(위) · D31 = `notification_events.py:26-27`(TTL 25초) · `routers/api/streams.py:23`(TICK 10초) · `notifications.py:129-131` · D06 = 코디 지시 「사용자 기본값 = 웹 템플릿」(spec-sync-2 지시 4) | ✓ |
| BW6(OQ-D40) | 「유지 여부는 사용자 확인 남음」 | ✓ 열린 채 |
| 국적 alpha-2 | SPEC-003 OQ-A9 `:1468` · SPEC-000 OQ-02-1 그대로 열림 | ✓ 열린 채. 단 SPEC-007 `:571` 에 연결 없음 → **W6** |
| OQ-A95 `:1640` · OQ-A93 `:1638` | 기본값 · 출시 전 그대로 | ✓ 열린 채 |
| **OQ-A90** `:1635` | 본문 `:669` 은 「~~WORK~~ 프레임 · 바이트를 메모리에만 · 파일 0」으로 바뀜. 표 행은 「WORK 에서 정함」 그대로 열림 | **반만 닫힘 → W1** |

## 3. 지적

### W1 — OQ-A90 이 본문에서만 정해지고 표에서는 열려 있다 · 근거 줄이 없다

- 자리: SPEC-003 `:669`(본문) ↔ `:1635`(OQ-A90 행). spec-sync-2 처분표에도 없다.
- 근거: 본문은 지키는 방법을 「WORK」에서 「프레임 · 바이트를 메모리에만 · 파일 0」으로 바꿨다. 하지만 코드 근거를 적지 않았다. OQ 행은 아직 「WORK 에서 정함」이고 `20-spec.md:104` 도 A90 을 열린 범위(A84 ~ A95)에 넣는다.
  - 코드 사실은 본문과 맞다: `PassportScanActivity.kt:277-278` · `ScanChannel.kt:125-126` = `ByteArrayOutputStream`. Android 스캔 파일에는 `File(` · `cacheDir` · `createTempFile` · `FileOutputStream` 이 없다.
- 고칠 방향: 아래 둘 중 하나.
  - 본문에 위 근거 줄을 달고, OQ-A90 행을 「→ 닫음(2026-11-26 spec-sync-2 · 구현)」으로 닫는다. `20-spec.md:104` 의 범위 글도 맞춘다.
  - 또는 본문을 「WORK」 그대로 되돌린다.

### W2 — BW7 근거 줄 번호가 낡았다

- 자리: SPEC-007 `:597` 「`static/day.js:5473-5487`」.
- 근거: `a76496c4` 에서 그 줄은 다른 코드다. 실제 자리는 `day.js:5643-5653`(`sessionStorage` · `history.replaceState`)이다. `fb08fe4e` 기준 번호가 그대로 남았다(spec-sync-2 리포트 「주의 4」).
- 고칠 방향: `:5643-5653` 으로 고친다.

### W3 — U-26 문진 칸 목록에 `canResend` 가 없다

- 자리: SPEC-003 `:645` 「`questionnaire{sendStatus(…), time, submittedAt}`」.
- 근거: 구현 응답에는 `canResend: bool`(「[다시 보내기] 대상 · 웹만 · 앱엔 버튼 없음」)도 있다(`schemas/reservation_detail.py:45-47` · be-2 D2 에 적힘). 이 칸은 `extra=forbid` 모델이라 늘 실린다.
- 고칠 방향: 「· `canResend`(웹만 — 앱은 안 씀)」를 덧붙인다.

### W4 — SPEC-003 의 `baseBody` 문장이 null → `""` 을 말하지 않는다

- 자리: SPEC-003 `:588` 「`baseBody` · `baseDoctorStaffId` = 그 칸 `base` 그대로」 · `:791` 표. 그런데 SPEC-002 `:1685` 는 「DAY-SPEC-003 … 바꿀 것 없음」이라고 적었다.
- 근거: `base.body` 가 `null` 이면 앱은 `""` 를 보낸다(`chart_controller.dart:156`). 「그대로」 보내면 400 이다(`schemas/board.py:89`). SPEC-002 `:739` 에는 적었지만, 앱 독자가 읽는 SPEC-003 에는 없다.
- 고칠 방향: SPEC-003 `:588` 에 「(`base.body` 가 `null` 이면 `""` — DAY-SPEC-002 `:739`)」를 한 줄 덧붙인다. 그러면 SPEC-002 `:1685` 의 「바꿀 것 없음」도 맞는 말이 된다. 아니면 `:1685` 에서 그 말을 지운다.

### W5 — SPEC-003 의 「서버 쪽 열린 것」 줄이 낡았다

- 자리: SPEC-003 `:1624` 「서버 쪽 열린 것 = DAY-SPEC-007 OQ-D27 ~ D40 · DAY-SPEC-005 OQ-N25 · N26 · DAY-SPEC-006 OQ-R40」.
- 근거:
  - N25 는 이번에 닫혔는데 취소선이 없다.
  - D29 · D30 · D31 · D39 는 닫혔고, D41 · D42 는 범위 밖에 있다.
  - 이번에 고친 `20-spec.md:104`(「D27 ~ D42(… 닫음 · D40 구현값)」 · 「~~N25~~」)와 서로 다르다. 이번 hunk 에서 N22 → N26 만 고쳤다.
- 고칠 방향: `20-spec.md:104` 와 같은 꼴로 맞춘다.

### W6 — 국적 alpha-2 계약 문장에 열린 확인을 잇지 않았다

- 자리: SPEC-007 `:571` 「`nationality` = 대문자 두 글자(`[A-Z]{2}`)」.
- 근거: 구현 그대로이고(`passport_scan.py:85`) 그것은 맞다. 하지만 KOS 가 alpha-3 도 받는지는 아직 사용자 확인 대상이다(spec-sync-2 「미결 2」 · SPEC-003 OQ-A9 · SPEC-000 OQ-02-1). 이 문장만 읽으면 닫힌 계약으로 보인다.
- 고칠 방향: 「(KOS 국적 꼴 확인 = DAY-SPEC-003 OQ-A9 · DAY-SPEC-000 OQ-02-1 — 열림)」 꼬리를 단다. 새 규칙은 아니다.

### W7 — 「저장소 꺼짐 = KOS 전에 503」의 조건이 넓게 적혔다

- 자리: SPEC-007 `:571` 끝 「단 저장소가 설정 안 됨(꺼짐)이면 KOS 를 부르기 전에 503 `photo_disabled`(고객 수정도 안 함 …)」.
- 근거: 구현은 사진이 있을 때만 저장소를 본다(`passport_scan.py:309` `target = _storage() if data is not None else None`). 손 입력(사진 없음)이면 저장소가 꺼져 있어도 KOS 고객 수정은 그대로 한다. 문장이 「사진 저장」 단계 안에 있어 뜻은 통하지만, 따로 떼어 읽으면 손 입력도 503 으로 읽힌다.
- 고칠 방향: 「사진이 있고 저장소가 설정 안 됨이면 …」으로 좁힌다.

## 4. 참고(고치지 않아도 됨)

- **R1 · log 옛 행 고침** — `log.md:30`(2026-11-25 행)의 `N22 → N26` 은 이미 있던 log 행을 고친 것이다. 다만 아직 main 에 머지되지 않은 같은 PR(#964) 안에서 merge-dev-2 가 놓친 번호를 바로잡은 것이라 받아들일 만하다.
- **R2 · migration 근거 줄** — SPEC-000 `:51` ③ 은 migration `:30` 을 가리킨다. `:30` 은 down_revision 이고 revision 이름은 `:29` 에 있다. 둘 다 그 자리라 뜻은 맞다.
- **R3 · OQ-D06 근거** — 근거는 `_RESUME` §2 의 사용자 행이 아니라 코디 지시(spec-sync-2 지시 4 「사용자 기본값」)다. 웹은 #280 부터 SPEC(「안 보임」)과 다르게 그려 왔다. 이번에 SPEC 을 구현에 맞춘 것은 지시대로다. 사용자에게 한 번 알려 둘 만하다.

## 5. 사용자 확인 필요(열린 채 — 이번 검수에서 다시 열지 않음)

1. BW6 — Redis 장애 때 속도 제한 · 거절 기록 간격을 끄는 정책을 유지할지(SPEC-007 OQ-D40).
2. 국적 alpha-2 강제 — KOS 가 alpha-3 를 받는지(SPEC-003 OQ-A9 · SPEC-000 OQ-02-1 · W6).
3. OQ-A95(Android `CAMERA` 뒤 `image_picker`) 실물 확인 · OQ-A93(ML Kit 지표 · 고지) 출시 전.
