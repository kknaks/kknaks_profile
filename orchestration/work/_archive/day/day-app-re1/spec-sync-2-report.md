# spec-sync-2 결과 보고 — SPEC 을 머지된 구현에 맞춤(마감 전)

## 상태: done (워크트리 변경만 · 커밋 · push 안 함)

- 스펙 워크트리 `mediness-mediness/day-app-re1-spec`(HEAD `538befe4`) · 근거 코드 = CENTURION_DAY `a76496c4`(#296 · 그 아래 #295 `8fe0095a`) — 코드는 `git show`/`git grep` 로 읽기만 했다.
- 원칙: 구현이 정본이다. 문장마다 「2026-11-26 spec-sync-2」 꼬리표를 달고 근거 파일:줄 @`a76496c4` 를 적었다. 앞 문장은 ~~취소선~~으로 남겼다. 새 규칙 · 새 화면 글자는 넣지 않았다(새 글자는 구현이 이미 쓰는 것뿐: `yyyy-MM-dd` 자리 글은 cc 원천, ⚠ 는 아이콘이라 글자가 없다).
- 바꾼 파일 11개(+83 −71): SPEC-000 · 002 · 003 · 004 · 005 · 006 · 007 · `20-spec.md` · `10-decision.md` · `30-work.md` · `log.md`.
- 개정 머리말 보충을 새로 단 곳: SPEC-000 `:51` · SPEC-002 `:53`(㉜ 아래) · SPEC-003 `:91`(㉓ 아래) · SPEC-005 `:50` · SPEC-007 `:54`(고침 6 보충 아래). main 쪽 문장(#965 · #966 · #967)은 건드리지 않았다.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning**, `products/day` 줄 **0**(day 범위 0/0). warning 263개는 전부 다른 제품의 기존 것이다(무관).
- 번호 참조 검사(merge-dev-2 §4 방식 · 스크립트 `scratchpad/refs.py`): OQ-A · OQ-N · OQ-D · SPEC-002 OQ-9x~12x · SPEC-003 U-n 참조를 정의 행 · 절과 대조했다.
  - HEAD(`538befe4`)와 비교해 **새로 끊긴 참조 0**.
  - 정의 행 꼴이 달라 「없음」으로 잡히는 것 197건은 HEAD 에도 똑같이 있던 옛 닫힌 OQ다(A50 · N14 등 — 무관).
- 뜻 검사(우리 번호 범위에 걸친 짧은 꼴 목록): **merge-dev-2 가 놓친 곳 3개를 찾아 고쳤다.** `OQ-N25 · N22` 의 `N22` 는 옛 `N22` 에서 바꾸지 않고 남은 것이다(지금 N22 = main 의 「KOS 에서 건 호출」 OQ). 그래서 `N26` 으로 고쳤다 — `20-spec.md:104` · SPEC-003(개정 ㉓ 대조 줄) · `log.md:30`. 다시 돌린 결과 0.

## 처분표 — 항목 1 ~ 8

### 1. be-2 계약 차이 D1 ~ D17

| # | 처분 | 바꾼 곳(파일:줄) | 근거 코드 @`a76496c4` |
|---|---|---|---|
| D1 칸 이름 | 고침 — `kos_status` · `kos_error` · `kos_sent_at` → `crm_status` · `crm_error` · `crm_sent_at` · enum `questionnaire_crm_status` | SPEC-000 `:47` · `:51` · `:1203` · `:1240`~`:1245` · SPEC-007 `:597`(고착) · `:773`(DB) · SPEC-003 `:1297`(대조 표) | `backend/day/models/reception.py:34` · `:119` |
| D2 문진 상태 키 | 고침(이름 적음) — `questionnaire{sendStatus, time, submittedAt}` · `health[]` · 행 없음 = `null` | SPEC-003 U-26 「값 원천」 `:645` | be-2 §0 · `schemas/reservation_detail.py`(review-code-2 §1 PASS) |
| D3 | 고침 — 409 `customer_not_linked` | SPEC-007 `:529`(passport GET) · `:571`(스캔 ①) · `:799`(OQ-D29) | `common/error_codes.py:30` · `day/errors.py:168` |
| D4 | 고침 — 409 `display_closed` · `questionnaire_not_failed` | SPEC-007 `:542`(닫기) · `:594`(다시 보내기) | `common/error_codes.py:29` · `:31` · `day/errors.py:161` · `:175` |
| D5 동행 | 고침(이름 적음) — `companions[{visitId, name}]` | SPEC-003 `:645` | be-2 D5 |
| D6 iOS 푸시 | 고침 — `aps.alert` + 최상위 `kind` · `requestId` · `environment` · `hospitalId` | SPEC-005 `:356` · `:50` | `services/display_push.py:39-56` |
| D7 | 고침 — 응답 `identity{status, method, checkedAt}` | SPEC-007 `:566` | be-2 D7 |
| D8 | 고침 — `deviceName` · `qrUrl` 키가 늘 있음(없으면 null) | SPEC-007 `:541` | be-2 D8 |
| D9 · D13 | 고침 — `displays[]` 칸 · 시한은 읽을 때 판정 · 스캔 `opened` 도 60분 | SPEC-007 `:552`(규칙 5) · `:800`(OQ-D30 닫음) · SPEC-003 `:645` | `policies/displays.py:56-67` |
| D10 | 고침 — 저장소 설정이 꺼져 있으면 KOS 를 부르기 전에 503 `photo_disabled` | SPEC-007 `:573` | `services/passport_scan.py:237` |
| D11 | 고침 — 502 `kos_unavailable` | SPEC-007 `:591` · OQ-D39 닫음 | `services/questionnaire_public.py:209` |
| D12 | 고침 — `qweb_denied` 는 병원을 아는 거절만 | SPEC-007 `:597`(보안 행) | `questionnaire_public.py:120-135` |
| D14 목록 JSON | 고침 — 「칸 이름은 WORK」 → camelCase 칸 목록 | SPEC-006 `:460` | be-2 D14 · `schemas/reservations.py` |
| D15 날짜 글자 | 바꿀 것 없음 — 「웹과 같은 글자」가 이미 계약 | — | — |
| D16 | 고침 — HMAC 키 = `ENCRYPTION_KEY` 에서 따로 뽑음 | SPEC-007 `:549` · SPEC-003 `:1342` | `services/displays.py:79-83` |
| D17 | 고침 — origin = `DAY_PUBLIC_API_BASE` · 없으면 요청 주소 | SPEC-007 `:549` · SPEC-003 `:1342` | `services/displays.py:132` |
| 설정 이름 | 고침 — `DAY_DISPLAY_TTL_MINUTES` · `DAY_QWEB_FILL_MINUTES` · `DAY_QWEB_STUCK_MARGIN_SECONDS` | SPEC-007 `:549` · `:552` · `:597` · OQ-D41 | `common/config.py:215-218` |

### 2. fix 라운드 변경

| # | 처분 | 바꾼 곳 | 근거 |
|---|---|---|---|
| F1 제출 1회 | 고침 — 원자적 `UPDATE … RETURNING` 으로 넘김 · 답 행은 같은 트랜잭션 · `display_request_id` 부분 유일 `live_unique`(`uq_questionnaire_history_display_request_id`) | SPEC-007 `:592`(제출 ①) · SPEC-000 `:1240` · `:51` ② | `services/displays.py:452-472` · `questionnaire_public.py:306-383` · `models/reception.py:107` · migration `:50-51` |
| BW1 | 고침 — Redis 잠금은 앞막이만 · 뜻밖의 실패 = 500 `internal_error` + 공개 머리 | SPEC-007 `:592` | `routers/api/public_questionnaire.py:68` · `questionnaire_public.py:321-330` |
| BW2 | 고침 — 고객 200 이 KOS 를 기다리지 않음(응답 뒤 `send_detached`) | SPEC-007 `:592` ③ ④ · SPEC-000 `:1244` | `public_questionnaire.py:133` |
| BW3 | 고침 — 회차 시한(HTTP 한도 + 여유/2) · 다시 잡힌 행은 덮지 않음 | SPEC-007 `:595` | `questionnaire_reads.py:31` · `questionnaire_kos.py:73-125` |
| BW4 | 고침 — 양식을 받는 중에 닫힌 링크 = 410 / 409 | SPEC-007 `:591` | be-fix-2 `questionnaire_public.py:245-256` |
| BW5 | 고침 — POST 검사 차례(IP → 토큰 없음 → 본문 → 토큰 제한 → 판정) | SPEC-007 `:592` ① | `questionnaire_public.py:299` |
| BW6 | 구현 그대로 적음 — Redis 장애 = 속도 제한 · 거절 기록 간격 끔 | SPEC-007 `:597` · OQ-D40 `:810` | `questionnaire_public.py:85-100` · **유지할지는 사용자 확인 남음**(be-fix-2 §4-2) |
| BW7 | 고침 — 주소창의 `#토큰` 을 지우고 사본은 `sessionStorage` 에 | SPEC-007 `:597` | `static/day.js:5473-5487` |
| BW8 | SPEC 에 쓸 것 없음(시험만) | — | — |
| 코디 추가(스캔 칸 꼴) | 고침 — 400 `fields.<칸>` · 국적 `[A-Z]{2}` · 여권번호 `[A-Z0-9]{1,9}` · `YYYY-MM-DD` | SPEC-007 `:571` | `services/passport_scan.py:80-87` |
| AW1 | 고침 — Android `FLAG_SECURE` · iOS 는 효과 없음 · 채널 `secure(bool)` | SPEC-003 U-28 `:669` · 채널 표 `:851` | `PassportScanActivity.kt:98` · `ScanChannel.kt:63-72` |
| AW2 | 고침 — 카메라 시작 실패 = 「이 기기는 카메라를 쓸 수 없어요」 + [손으로 입력] · 요청은 닫지 않음 | SPEC-003 `:665` · `:851` | `PassportScanActivity.kt:213` · `:232` |
| AW3 | 고침 — 확인 칸 꼴 · 성별 고르기 · [저장] 꺼짐 · 400 칸 빨강 | SPEC-003 `:666` | `scan_screen.dart:64-100` · `:248` · `:520` |
| AW4 | 고침 — MRZ 고치기는 2자리까지 + 종합 검사 숫자 · ⚠ 아이콘(「종합 검사 숫자 안 봄」 줄) | SPEC-003 `:664` | `mrz.dart:85-106` · `:150-157` |
| AW5 | 고침 — 받은 스캔의 상세 읽기 실패 = 표시를 풀거나 `close canceled` | SPEC-003 U-30 `:683` | `display_flows.dart:256-279` · `display_inbox.dart:79-84` |
| AW6 · AW7 | SPEC 에 쓸 것 없음(내부 · 출시 고지 — OQ-A93 은 열린 채로 둠) | — | — |

### 3. migration 이름

고침 — 「번호 WORK(dev 끝 0028 뒤)」를 `0030_display_questionnaire_kos`(down `0029_partner_charty`)로 바꿨다.
- 바꾼 곳: SPEC-000 `:47` · `:51` ③ · SPEC-007 `:773` · SPEC-003 `:1297`
- 근거: migration `:30`
- 「0029」로 우리 것을 적은 SPEC 문장은 원래 없었다. 이름이 정해지지 않은 「WORK」 자리만 있었다.

### 4. 「국적 / 통역필요」

고침 — 외국인은 `{국적} / 통역필요`, 내국인은 국적 값(없으면 「대한민국」)으로 적었다. 사용자 기본값 = 웹 템플릿을 따른다.
- 이 문장은 SPEC-003 U-3 이 아니라 **DAY-SPEC-007 U-3** 에 있었다(SPEC-003 U-26 이 그 U-3 을 가리킨다).
- 바꾼 곳: SPEC-007 `:146`(시안 요소 #7) · `:215`(U-3) · `:823`(OQ-D06) · SPEC-003 U-26 `:645`
- 근거: 웹 `templates/partials/reservations_detail.html:109`(#280 부터 이렇게 그림) · 앱 `app/lib/ui/reservation_detail.dart:317`

### 5. WORK-001 W3 · W4 · OQ-119

| 항목 | 처분 | 바꾼 곳 | 근거 |
|---|---|---|---|
| W3 크게 보기 | 고침 — 차트 전용 새 화면 · 같은 꼴(핀치 없음) | SPEC-003 U-24 `:616` · `:91` ② | `chart_photos.dart:205-221` |
| W4 저장 띠 | 고침 — 탭 줄 바로 아래 오른쪽 띠 | SPEC-003 `:583` · `:91` ① | `chart_sheet.dart:272-273` |
| OQ-119 | 닫음 — 응답 모양 = 이름 제안 그대로(`details.conflicts` · 사진 `title`) · 요청 `baseBody` 는 문자열만(`null` = 400) · GET `base.body` 가 `null` 이면 앱이 `""` 로 보냄 | SPEC-002 `:739` · `:750` · `:1685` · `:53` | `schemas/board.py:89` · `schemas/board_responses.py:512` · `chart_controller.dart:156` · `day/errors.py:236-244` |
| (같이) OQ-120 | 닫음 — 사진 오류도 `/api` 공용 모양 | SPEC-002 `:747` · OQ 표 | `routers/api/board_photos.py:4` |

### 6. 사용자 결정 닫기

**OQ-A83(옛 A79) iOS 카메라 문구 — 닫음.** 사용자 문구로 적었다(2026-11-26 · #296).
- 바꾼 곳: SPEC-003 §4 권한 표 `:1160` · `:1164` · OQ-A83 `:1628` · SPEC-004 OQ-C7 `:638` · `10-decision.md:40` · `20-spec.md:104`
- 근거: `app/ios/Runner/Info.plist:52-53` 이 같은 글자다.

**dev 메뉴 「예약 현황」 · 「고객」 다시 열림(`65b2de5e`) — 바꿀 것 없음.** day SPEC · 30-work · log 를 찾아봤지만 #286 메뉴 막음을 적은 문장이 없었다. SPEC-003 머리말 ⑥ 에 이 사실만 한 줄 남겼다.

### 7. `_RESUME.md` §2 2026-11-25 · 26 WORK-002 결정 대조

**빠진 결정 0.** 결정 행을 하나씩 SPEC 과 대조했다:
- 범위 · 예약현황 탭 · 태블릿 보내기 → U-25 ~ U-31 · SPEC-007 규칙 1 ~ 8
- 아이패드 · 갤럭시 → U-28 Android
- Q7 · Q6 · DAY-ESC-001 참조 · 문진 DAY 저장
- 공용 코디 계정 · 5대 한도
- 읽기 전용 · 웹과 닮게
- U1 스캔 → 신분확인 O(OQ-D36)
- U2 채널 · U3 글자 · U4 여권번호 안 실음
- WORK-001 E2E 「지금대로」 → W3 · W4(이번에 맞춤)
- 11-26 iOS 문구 → 6

11-26 의 TestFlight · Play internal · 「KOS 데모 데이터 그대로」 · 「마감」은 SPEC 계약이 아니라 반영하지 않았다.

### 8. `30-work.md` · `log.md`

- `30-work.md`: Spec Coverage 의 우리 Delivery 칸 8곳(SPEC-000 · 002 · 003 · 004 · 005 · 006 · 007)에 Code PR #295 `8fe0095a` · #296 `a76496c4` · spec-sync-2 를 덧붙였다. 상태는 `in_dev` 그대로 두고 「최종 수정」을 2026-11-26 으로 바꿨다.
- `log.md:17`: spec-sync-2 행을 새로 넣었다(2026-11-26 · 근거 = 이 리포트).
- `20-spec.md:104`: 열린 OQ 목록을 고쳤다(A83 · N25 닫음 · D 범위 · N22 → N26).

### 닫은 OQ 모음

| SPEC | 닫은 OQ |
|---|---|
| SPEC-002 | OQ-119 · OQ-120 |
| SPEC-003 | OQ-A83 |
| SPEC-005 | OQ-N25(구현이 기본값과 같음 · `routers/api/notifications.py:136-143`) |
| SPEC-007 | OQ-D29(코드 이름) · OQ-D30 · OQ-D31 · OQ-D39 · OQ-D42 · OQ-D06 |

값만 적은 것: OQ-D41(여유 60초 · 두 번 보냄은 열린 채) · OQ-D40(구현값 · BW6). SPEC-005 채널 id 는 `display` 로 적었다.

## 구현 의심

없다. SPEC 을 어긴 것으로 보이는 구현은 찾지 못했다. 다른 점은 모두 이름 제안 · WORK 자리 · 사용자 기본값 · 리뷰를 거친 fix 였다.

## 미결 · 주의점(사용자 · 코디 몫)

1. **BW6 Redis 장애 = 제한 끔.** 구현대로 SPEC 에 적었지만, 이 정책을 유지할지는 사용자가 확인해야 한다(be-fix-2 §4-2). SPEC-007 OQ-D40 에 「확인 남음」으로 적었다.
2. **국적 alpha-2 강제.** KOS 가 alpha-3 도 받는지 확인하지 않았다(be-fix-2 §4-1 · SPEC-003 OQ-A9 · SPEC-000 OQ-02-1). SPEC 에는 구현 규칙만 적었다.
3. **OQ-A95 Android `CAMERA` 뒤 `image_picker`.** review-code-2 가 코드 근거로 PASS 했지만 실물 확인 전이라 열어 뒀다. **OQ-A93**(ML Kit 지표 · 오픈소스 고지 — AW7)도 출시 전 항목이라 열어 뒀다.
4. **근거 줄 번호.** app-fix-2 · be-fix-2 리포트의 줄 번호(`fb08fe4e` 기준)는 `a76496c4` 에서 몇 개만 확인했다(mrz · scan_screen · PassportScanActivity · display_flows · display_inbox · Info.plist · 서버 쪽 주요 줄). merge-dev-3 에서 dev 쪽 `app/` 변경이 없었으니 앱 줄은 그대로일 것이다.
5. **SPEC-003 Wireframe 그림.** W4 띠 자리를 그림에서 고치지 않았다(그림 안에 「탭 줄 오른쪽」 글자가 없다).
