# 리뷰 리포트 — day-reservation3 / doc (2026-11-26)

대상: 워크트리 `mediness-mediness/day-reservation3-spec` 미커밋 변경 — `spec-008-reservation-request.md`(새 · draft · 603줄) · SPEC-006 개정 ⑭ · SPEC-005 2026-11-26 개정(U-6) · SPEC-007 고침 6 · SPEC-000 개정 ③ · `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md`.
대조: 결정 RQ1 ~ RQ44 · 코디 결정 11-26 ①~④ · 시안 v15(base64 뺀 사본 grep) · design-1 ~ 6 「지은 문구」 · 본문 초안 · be-probe-1 ~ 4 · CENTURION_DAY `origin/dev` `a76496c4`(fetch 안 함).
리포 파일 수정 0 · lint 1회만 실행.

## 판정: FAIL — FAIL 3 · WARN 14

ext API · partner 전수 표 · KOS 쓰기 본문 · 알림 받는 사람 · 결정 반영 대부분은 정확하다. 다만 상태 표의 구멍 둘(F1 · F2)은 **같은 고객 이중 예약**으로 이어질 수 있고, F3 은 결정된 동작(RQ23)을 기본값으로 바꿨다. 셋 다 문장 몇 줄로 고칠 수 있다.

### FAIL

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| F1 | spec-008:233 · 234 · 235 · 236 · 248 | **「확정」 × 「예약 없음」 칸이 비어 있다.** 표는 `change`/`cancel` 행을 「예약 있음 / 없음」으로 나누는데, 확정 열은 「예약 있음」 줄에만 값이 있고 「예약 없음」 줄(234 · 236)은 빈 칸이다. 그런데 248 은 「예약 있음」을 **지금 사본**(`reservation_status ≠ canceled`)으로 보므로, 확정 뒤 KOS 에서 예약이 취소되면(당일 미방문 취소 등 RQ2 의 평소 흐름) 스레드는 「확정」인데 「예약 없음」이 된다. 이때 링키 `change` · `cancel` 은 정해지지 않았다. 같은 자리의 E3 철회도 239(「확정 → 409」)와 267(「예약이 있었던 스레드 → 409」)이 서로 다른 기준이다. 236 의 409 `request_not_applied` 는 「철회를 쓰라」고 하지만 취소됨 스레드는 E3 도 409 라서 갈 곳이 없다 | RQ2(스레드가 따라가지 않음) · RQ12 · 코디 결정 ① · 판정 축 5 | 확정 × 예약 없음 줄을 채운다(예: 취소됨 열처럼 `change` → `new` 기록 · `cancel` → 409). OQ-Q10 과 묶어 코디 기본값으로 둔다. E3 의 409 기준은 248 정의 하나로 맞추고, 취소됨 · 예약 없음 스레드의 `cancel` 409 메시지는 철회 대신 「이미 끝난 요청」 뜻으로 바꾼다 |
| F2 | spec-008:405 · 407 · 248 ↔ spec-000:673 | **W3 은 성공하고 W18 이 실패하면 이중 예약이 된다.** 407 은 그 경우를 「예약 있음」으로 보라고 한다. 그런데 「예약 있음」의 정의(248)는 「이 스레드로 만든 `visit`」이고, 그 연결(`reservation_request.visit_id`)은 순서 묶음의 **마지막 쓰기 확인 뒤**(405 · spec-000:673)에야 생긴다. 그래서 W18 이 `failed` 인 동안은 「예약 없음」이 되고, 링키 `change` 가 오면 `new` 로 기록된다(Rule 3). 그 상태에서 [예약 생성]을 누르면 KOS 에 두 번째 예약이 생긴다. 초진(W2 · W3 · W18)도 같다 | 코드 `reservation_book.py:258`(visit 사본은 W3 확인 때 생김) · SPEC-007 D9 · 코디 결정 ① | `visit_id` 는 **W3 확인 때** 연결한다(`reservation_applied` 와 상태 전이는 지금처럼 마지막 확인 뒤). 「예약 있음」 = `visit_id` 있음 ∧ 취소 아님으로 고정하고, spec-000:673 설명도 고친다 |
| F3 | spec-008:384 · 535(OQ-Q02) | **[예약 수정]은 기본값으로 예약 메모 · 유입을 KOS 에 보내지 않는다.** 확인 전엔 이 두 칸을 빼고, 「화면 · 링키에 반영 안 됨으로 남김」이라고 썼다. 하지만 RQ23 은 예약 메모가 「생성 · 수정 때 같이 나감」이라고 **정했고**, RQ27 은 유입을 KOS 칸으로 보낸다고 정했다. 메모 합치기(RQ28)에 든 희망 시술 · 통역이 바뀐 수정 버전도 KOS 에 닿지 않는다. 그런데도 `reservation_applied`(수정)는 남아, 링키는 반영된 줄 알고 고객에게 확정을 알린다(RQ36) | RQ23 · RQ27 · RQ28 · RQ36 · be-probe-2 ⓒ(`counselor` 만 시험 · 「최상위 칸은 보낸 것만 바뀐다」는 추정) | 계약은 RQ23 그대로 둔다(수정 때 메모 · 유입을 보냄). OQ-Q02 는 **구현 착수 전 실물 확인**(be-probe 한 번 · `update-reservation {scheduleId, reservationMemo, funnel}`)으로 바꾼다. KOS 가 받지 않으면 그때 사용자에게 묻는다. 「보내지 않음」 대체 동작은 지운다 |

### WARN

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W1 | spec-008:239 · 244 · 249 · 481(Rule 5) ↔ spec-000:676 | **쓰기 큐 확인을 기다리는 사이(`pending_version_id` 있음)의 E3 철회 · 자동 닫힘 · E2 `cancel` 이 정해지지 않았다.** 이대로면 스레드는 「닫힘」인데 뒤이어 KOS 확인이 와서 예약이 생길 수 있다 | RQ31(예약 없을 때만 닫힘) · 249 | pending 중에는 E3 = 409 `request_already_applied`(또는 새 코드) · 자동 닫힘 건너뜀 · `cancel` = 「예약 있음」으로 본다 |
| W2 | spec-008:365 ~ 367 · 469 | 두 데스크가 거의 같이 누르면 둘 다 통과한다. 먼저 누른 쓰기가 확인 전이면 상태 · 답할 버전이 그대로라 `version` 비교로는 걸리지 않는다. 그런데 409 `request_version_changed` 조건(366)에 「pending 중」이 없다 | spec-000:676 `pending_version_id` · DAY-SPEC-007 D52 | create · update · cancel 의 409 조건에 「`pending_version_id` 있음」을 더한다(스레드 행 잠금 — Rule 4 와 같게) |
| W3 | spec-008:239 · 244 · 247 · 251 | 「답변 대기」 `change_request` 가 남은 채로 철회(E3)나 자동 닫힘이 오면 어떻게 되는지 없다. 병원이 시간을 제안했는데 링키가 답하지 않으면 자동 닫힘이 흔히 일어나는데, 그 댓글은 늘 `waiting` 으로 남는다 | RQ31 · RQ34 · RQ35 | 닫힐 때 `waiting` → `withdrawn`(또는 `superseded`)으로 바꿀지, 그대로 둘지를 한 줄로 정한다(코디 기본값) |
| W4 | spec-008:112 · 144 · 539(OQ-Q06) ↔ spec-000:660 ~ 750 | 빨간 점(「아직 열지 않음」)을 저장할 칸이나 표가 SPEC-000 에 없다. OQ-Q06(직원마다 / 병원 공용)이 열려 있으면 구현자가 DB 를 지어내야 한다 | 판정 축 6 · 체크리스트 「추측으로 메워야 하는 빈칸」 | 코디 기본값을 고른다(예: 병원 공용 = `reservation_request.partner_unread_at`, 직원마다 = 읽음 표). 고른 것을 SPEC-000 에 칸으로 넣는다 |
| W5 | spec-008:146 · 418 · 419 ↔ spec-005:178 ~ 183 · spec-006:54 | **웹 알림을 누른 뒤 열 자리가 계약에 없다.** ① 응답 `NotificationTarget` 은 `visitId` · `callId` 뿐이고 모르는 칸을 막는다(`schemas/notification_responses.py:19` · `FROZEN_FORBID_CONFIG`). 그래서 `requestId` 와 희망 날짜를 실을 칸이 필요한데 SPEC 에 없다 ② `day.js:5377` `NOTIFY_KIND` · `onclick → /board` 를 나누는 곳은 「더함」이라고만 썼다 ③ `/reservations?request={id}` 쿼리는 SPEC-006 개정 ⑭ 에 없다 ④ 앱 `unread` 를 빼는 것: 스트림 `notification {unread}` 는 **계정 채널 하나**(`notification_events.channel(hospital, account)`)라 앱 · 웹이 같은 수를 받는다. 그래서 수는 늘 이 종류를 빼고 세야 하고, 목록만 `CurrentSessionData.transport`(쿠키 / Bearer)로 갈라야 한다 — 「앱(Bearer) 스트림 수에서 거른다」는 이 구조에서 그대로는 안 된다 ⑤ 알림 행을 만든 뒤 `announce_unread` 로 웹을 깨우는 것도 적혀 있지 않다 | 코드 refs 왼쪽 · RQ39 · 코디 결정 ② | SPEC-005 U-6 에 target 모양(`requestId` · `date`), 수 = 늘 뺌 · 목록 = transport 로 거름, 만든 뒤 `announce_unread` 를 적는다. SPEC-006 ⑭ 에는 `?request=` 를 연다고 한 줄 더한다 |
| W6 | spec-008:478(Rule 2) · 274 | Rule 2 는 「KOS 고객을 DAY 사본에 받아 두어 링키가 `/customers/lookup` 으로 `customerId` 를 얻게」라고 한다. 그런데 lookup 은 **KOS 를 이름 + 이메일로 직접 찾는다**(`ext.py:497` `refresh_search` · `ExtLookupRequest` = `name + email` 또는 `customerId`). 그래서 사본을 받아 둘 까닭이 맞지 않다. 더 큰 문제는 이메일이 없는 고객(RQ16 은 이메일 선택)이면 링키가 `customerId` 를 얻을 길이 없어, 「고객 확인 필요」 → 새 버전 고리(RQ24 · Q4)가 막힌다는 점이다 | RQ16 · RQ24 · 코디 결정 ④ | Rule 2 의 이유 문장을 고친다(사본은 선택). 「이메일 없는 고객의 `customerId` 얻는 길」을 새 OQ(사용자 질문)로 둔다 |
| W7 | spec-008:391 · 534(OQ-Q01) · spec-007:47 ① | 결정 「열린 것」은 「KOS 『당일 지정 상담사』 본문 키는 **실물(브라우저 요청)로 확인**」이다. 그런데 SPEC 은 be-probe-2 #6(API 시험 · `reservation.counselor` 가 들어감)을 곧 그 화면 칸으로 보았다. OQ-Q01 은 `reserve` 본문만 묻는다 | 결정 「열린 것」 2번째 · RQ27 · be-probe-2 #6(화면 칸 대조 없음) | OQ-Q01 에 「KOS 새 예약 화면 『당일 지정 상담사』 저장 요청이 `reservation.counselor` 인지 브라우저 요청으로 확인」을 더한다. W18 은 「확인 전 제안」으로 둔다 |
| W8 | spec-008:83 ~ 102 · 159 ~ 166 · 199 ~ 202 | 「지은 문구」를 「임시(기획 확인)」로 표시하라는 규칙(spec-008:25 · 브리프 §7)이 일부만 지켜졌다. 표시 없는 것 — design-2 ④: 「여권 성명」 · 「최근 방문」 · 「보유 시술권」 · 「{언어} 통역 필요」 · 「통역 불필요」 · 「없음」 · 「예약 현황 표에서 시간을 누르세요」 · 칩 「빼기」 / design-4 ④: 「예약 정보」 · 「직원 메모」 · 「외 n건」 / design-1 §5: 상태 배지 「요청됨 · 확정 · 취소됨 · 닫힘」 · 입력부 「글」 · 「보내기」 · 「제안 일시」 · 글쓴이 「링키 · {이름}」 | design-1 §5 · design-2 ④ · design-4 ④ · 결정 「열린 것」 1번째 | RW-12 · 13 · 31 · 33 · 35 줄과 U-3 · U-4 · U-8 에 「임시(기획 확인)」을 붙이거나, 「임시 글자 전부」 목록을 한 표로 따로 만든다(OQ-Q04 와 연결) |
| W9 | spec-008:257 · 265 ~ 272 · 284 ~ 303 | ① ext 새 오류 코드의 `message` 글자가 없다. `ExtErrorBody.message` 는 필수이고 기존 코드는 모두 한국어 글을 준다(`ext_common.py` · `ext.py:124` 등). OQ-Q04 는 웹 오류 글자만 다룬다 ② 칸 길이 상한이 없다(`body` · `authorName` · `name` · `desiredProcedures` · `reason`) ③ `phone` 「앞 0 없음」을 받을 때 400 으로 막는지가 정해지지 않았다. 막지 않으면 버튼을 눌러야 `_visitor_open` 정규식(`writes.py:234`)에서 걸린다 | 판정 축 2 · 코드 refs 왼쪽 | 새 ext 코드마다 message 를 「임시」로 적거나 OQ-Q04 에 ext 글자를 더한다. 길이 상한 · `phone` 형식을 E1 의 400 조건에 적는다 |
| W10 | spec-008:338 ~ 355 | partner 전수 표는 **값을 쓰는 곳에 빠짐이 없다**(아래 전수 표). 다만 구현자가 바로 짜기엔 셋이 빠졌다 ① 테스트 11개 파일(`test_ext_writes.py` 21줄 · `test_column_snapshot.py` 8 · `test_constraints.py` 6 · `test_room_move_chain.py` 6 · `test_models.py` 5 · `test_ext_contract.py` 3 · 그 밖)이 표에 없다 ② 유일키를 (`hospital_id`, `request_key`)로 좁히기 전에 **이미 쌓인 행 가운데 partner 만 다른 같은 키**를 어떻게 할지(migration 실패 위험 · 0017 · 0029 유일키) ③ 한도가 병원 하나에 분당 60 으로 합쳐진다(링키 + 차티 = 지금의 절반). 그리고 `_charty` 403 을 없애면 링키 키로 차티 전용 경로(동의서 · 결제 요청)가 열린다 — 10-decision 에 있지만 **taewoo 리뷰 확인 항목**으로 SPEC 표에도 이름을 적을 것 | RQ7 · `models/ext.py:25 · 62` · `routers/api/ext.py:111 · 123 ~ 127` | 표에 테스트 줄 · 중복 행 처리(예: 겹치면 migration 이 멈추고 보고) · 한도 영향 · 차티 경로 열림을 「리뷰 확인」으로 더한다 |
| W11 | spec-008:113 · 158 | [고객 차트] 「기존 DAY 고객 차트」라고만 했다. 경로(`/customers/{customer_id}/chart` — `routers/customers.py:75`)와 권한이 없다. 한편 SPEC-007 RD-02 는 고객 이름을 누르면 「준비중입니다」다(D46). 같은 예약 현황 화면 안에서 경험이 갈린다 | 시안 `data-rq-chart` · SPEC-007 D46 | 경로 · 권한(보기 키)을 적고, SPEC-007 D46 과 다르다는 것을 「시안과 다른 곳」이나 OQ 에 한 줄 적는다 |
| W12 | spec-008:161 · 551(OQ-Q18) · U-3 | 「최근 방문」 · 「보유 시술권」 · 「직원 메모」의 원천 규칙이 본문에는 정한 것처럼 쓰였고, OQ-Q18 에는 제안으로 남아 있다(시술 이름 · 「귀가 완료」 기준) | 체크리스트 「열린 것을 닫힌 것처럼」 | 본문에 「제안 · OQ-Q18」을 붙이거나 코디 기본값으로 닫는다 |
| W13 | spec-000:46 · spec-005:44 · spec-006:54 · spec-007:47(모두 `status: stable`) | stable SPEC 넷이 **draft** SPEC-008 의 계약을 「개정」으로 담았다(예: SPEC-006 R32 = 목록이 있음). 지금 Delivery(#267 ~ #278 · #283 · #289 ~ #291)의 재결속 · spec-sync 때 「이미 정해진 계약」으로 읽힐 수 있다 | rules/document-pipeline.md 「SPEC frontmatter status 가 확정 표현」 · delivery-workflow | 각 개정 머리에 「DAY-SPEC-008 stable 전까지 계획 · 코드 없음」을 한 구절 더한다(SPEC-005 는 이미 「코드에는 아직 없다」가 있음) |
| W14 | 30-work.md:51 | 브리프 §2-6 「30-work 는 이번에 쓰지 않는다」. 하지만 Spec Coverage 행이 없으면 lint ERROR(SPEC 파일 ↔ Spec Coverage 동기)라서 더한 것은 필요한 변경이다. 행 내용은 「WORK 안 씀 · proposed」로 맞다 | brief §2-6 · lint 규칙 | 그대로 두되 코디가 브리프와 다른 점으로 알아 둔다 |

## 직원이 실물에서 만날 자리

- 링키가 이메일 없이 보낸 동명이인 고객 → 「고객 확인 필요」 뒤 링키가 `customerId` 를 못 구해 스레드가 멈춤(W6)
- 확정 뒤 당일 미방문 취소된 예약에 링키가 수정을 올림 → 상태 미정(F1)
- 상담사 지정(W18)만 실패한 예약에 수정이 와서 [예약 생성] → KOS 이중 예약(F2)
- 메모만 바꾼 수정 요청을 [예약 수정] → KOS 메모 그대로 · 링키는 반영됨으로 앎(F3)
- 시간을 제안했는데 답이 없어 자동으로 닫힌 스레드에 「답변 대기」가 계속 보임(W3)
- 같은 요청을 두 데스크가 동시에 [예약 생성](W2)

## 참고(기존 부채 · 이번 범위 밖)

- 웹 예약 등록 `book()` 은 생년월일이 선택이다(OQ-Q08 · 결정 「열린 것」 그대로)
- 기존 ext `POST /reservations` 는 지난 시각 검사가 없다(`ext_writes.py` · `past` 없음). 새 `request_past_start` 는 SPEC-008 에만 있다

---

## RQ 대조 표 (RQ1 ~ RQ44 · 코디 결정 ①~④)

✓ = 빠짐 · 틀림 없음 · △ = 들어갔으나 지적 있음(번호)

| RQ | 반영 | SPEC 자리 | 판정 |
|---|---|---|---|
| RQ1 | 오른쪽 「예약 요청」 칸 + ext | §1 · U-1 · SPEC-006 ⑭ | ✓ |
| RQ2 | 요청 흐름만 · 생애 안 따라감 | §1:48 · 248 · 461 | △ F1(「예약 있음」을 지금 사본으로 판정 → 확정 × 예약 없음 구멍) |
| RQ3 | 스레드 = 예약 하나 · 고객 밑 여럿 | §1:49 · 용어 | ✓ |
| RQ4 | 근무 데이터 뺌 | §1:61 · RW-24 | ✓ |
| RQ5 | 표 카드 입구 없음 | Placement · SPEC-006 ⑭ ③ | ✓ |
| RQ6 | `/api/ext/reservation-requests` · 기존 키 · 바로 예약 그대로 | §3 ext 머리 · §1 | ✓ |
| RQ7 | 키 병원당 하나 · `partner` 제거 · 한도 · outbox 유일키 · `X-Day-Client` · taewoo | §3 「ext 키」 · 10-decision | △ W10(테스트 · 중복 행 · 한도 · 차티 경로) |
| RQ8 | 목록(`updated_since`) + 상세 | E4 · E5 | ✓(쪽 나누기 OQ-Q13) |
| RQ9 | 예약 그룹 · 유입 채널 목록(닫힌 것 뺌) | E7 · E8 | ✓ |
| RQ10 | 원장 · 상담사 id = 기존 직원 목록 | 요청 본문 · (기존) 줄 | ✓ |
| RQ11 | E1 · E2(`change` · `cancel`) · `Idempotency-Key` | E1 · E2 · 259 | ✓ |
| RQ12 | 버전 = 링키 · 확정 뒤 다시 열림 | 상태 표 233 · 235 | △ F1 |
| RQ13 | 번호 서버 · `baseVersion` 없음 | Rule 4 · 케이스 445 | ✓ |
| RQ14 | 완성본 · 병원 칸 없음 · 취소 = `reason` | 요청 본문 · 305 | ✓ |
| RQ15 | 담당자 = 누른 직원 | KOS 쓰기 381 · 시안과 다른 곳 | ✓ |
| RQ16 | 고객 칸 · 이름 · 생년월일 필수 · 이메일 선택 · `customerId` | 요청 본문 286 ~ 294 · W2 `email` | △ W6(이메일 없으면 lookup 불가) |
| RQ17 | 시작 필수 · 끝 = 그룹 간격 | 295 · 381 | ✓ |
| RQ18 | 예약 그룹 필수 | 296 | ✓ |
| RQ19 | 원장 · 상담사 선택 | 297 · 298 | ✓ |
| RQ20 | 희망 시술 = 글 | 299 | ✓ |
| RQ21 | 통역 한 칸 · null = 필요 없음 | 300 | ✓(코드 목록 OQ-Q07) |
| RQ22 | 유입 필수 · 목록에서 고름 · 상세 유입 뺌 | 301 · 381 | ✓ |
| RQ23 | 메모 = 링키 · 병원이 고침 · 생성 · 수정 때 같이 나감 · 「1:1 상담」 = 메모 글 | U-4 · 399 · 402 | **✗ F3**(수정 때 안 보냄이 기본값) |
| RQ24 | `customerId` / 이름 + 생년월일 · 0 · 1 · 2+ · 「고객 확인 필요」 | Rule 1 · 케이스 455 | △ W6 |
| RQ25 | 후보 고르는 화면 없음 · 기획안과 다른 곳 | RW-17 · 기획안 표 511 | ✓ |
| RQ26 | 칸별 저장 · 버전 고정 · 생성 뒤 메모 동기화 그대로 | spec-000 version 표 · 403 | ✓ |
| RQ27 | 기존 쓰기 W2 ~ W5 · KOS 칸이 있는 값(그룹 · 시간 · 원장 · 상담사 · 담당자 · 유입) | KOS 쓰기 표 · W18 | △ W7(「당일 지정 상담사」 실물) · F3(수정 때 유입) |
| RQ28 | `필드: 내용` · 순서 · 빈 줄 뺌 · 한국어 언어 이름 · 1000자 400 · 희망 시술 목록 칸 비움 | 메모 합치기 397 ~ 403 | ✓(필드 이름 = 임시 · OQ-Q04) |
| RQ29 | 상태 두 층 | 용어 · 상태 표 | ✓ |
| RQ30 | 거절 버튼 없음 · 버튼 하나 · 위치 | U-5 · RW-16 | ✓ |
| RQ31 | 생성 전 닫힘 = 철회 · 일시 지남 | E3 · Rule 5 | △ W1 · W3 |
| RQ32 | 댓글 종류 3개 | 용어 · E6 · 웹 댓글 | ✓ |
| RQ33 | 일시만 여러 개 · 그룹 없음 · 다른 날 · 새 버전으로 답 | U-7 · RW-23 | ✓ |
| RQ34 | 새 버전 → 「대체됨」 · 버튼 다시 | 247 · 시안과 다른 곳 494 | ✓ |
| RQ35 | 보낸 버전 버튼 숨김 · 높이 유지 · 철회 → 돌아옴 | U-5 176 · U-7 | ✓(문구 비움 · OQ-Q04) |
| RQ36 | 반영 때 자동 · 동작 · 일시 · 링키 조회 | 405 · E5 `reservation_applied` | △ F2 · F3 |
| RQ37 | 요청됨 · 확정 = 씀 · 취소됨 · 닫힘 = 읽기 · 새 버전이면 다시 열림 | U-9 · E6 409 · 상태 표 | ✓ |
| RQ38 | 고르기 위주 · 글 선택 | U-7 192 | ✓ |
| RQ39 | 웹 OS 알림 · `ADMIN` · `COORDINATOR` · `day.js` · enum migration · 받는 때 | §3 알림 · SPEC-005 U-6 · SPEC-000 07 | △ W5 |
| RQ40 | 앱 푸시 · 앱 화면 뺌 | 알림 「앱」 · SPEC-005 | ✓ |
| RQ41 | 예약 등록 권한 직원 | 웹 경로 권한 372 · U-5 · U-9 | ✓(`reservation.detail` = `policies/permissions.py:19` 있음) |
| RQ42 | 1 · 2 · 3열 구성 · 1160 × 700 · 7줄 · 「없음」 | U-2 ~ U-6 | ✓ |
| RQ43 | 배지 = 답할 버전 종류 / 끝나면 스레드 상태 | U-4 165 · 시안과 다른 곳 | ✓ |
| RQ44 | 정원 표시 없음 · 「지금 → 새」 없음 · 「열」 범위 밖 · 직원 메모 규칙 · 「외 n건」 | U-3 · U-6 · RW-17 | ✓(`customer_memo.important` = 코드 `models/customer.py:215` 있음) |
| 코디 ① | 생성 전 `change` = 신규 · `cancel` = 409(철회 경로) | Rule 3 · 상태 표 234 · 236 · E2 | △ F1(취소됨 · 확정 칸) |
| 코디 ② | 새 종류는 앱 unread · 목록에서 뺌(웹만) | 419 · SPEC-005 U-6 | △ W5 ④(채널 구조) |
| 코디 ③ | 재진 그날 예약 = 안 막음 · OQ | Rule 8 · OQ-Q05 · 케이스 465 | ✓ |
| 코디 ④ | 초진 W1 KOS 같은 고객 → 막고 「고객 확인 필요」 | Rule 2 · 케이스 454 · KOS 쓰기 382 | △ W6(Rule 2 의 이유 문장) |

결정에 없는 정책 발명: F3 의 「수정 때 안 보냄」 대체 동작 하나. 그 밖의 새 규칙(`request_past_start` · `reservation_past_date` · `visit_stage_changed` · E6 `Idempotency-Key` 필수 · 오류 코드 이름)은 본문 초안 · SPEC-007 · 기존 ext 관례에 근거가 있고 「이름 제안」으로 표시돼 있다.

## partner 전수 대조 표

`git -C CENTURION_DAY grep -n partner origin/dev -- backend`: 155줄(테스트 뺌 · migration 포함). 이 가운데 **`PartnerGrant.partner` 값이나 `partner` 칸을 쓰는 곳**은 `\.partner\b | partner= | "partner" | ext_partner` 로 다시 거른 결과와 SPEC-008:340 ~ 351 표를 한 줄씩 맞춰 보았다.

| 코드(origin/dev) | 쓰임 | SPEC 표 줄 | 판정 |
|---|---|---|---|
| `schemas/ext_common.py:14` `PartnerGrant.partner` | 칸 정의 | 342 | ✓ |
| `routers/api/ext.py:110` `request.state.ext_partner` | 상태 | 343 | ✓ |
| `routers/api/ext.py:111` 한도 키 | 병원 × partner | 344 | ✓ |
| `routers/api/ext.py:124` `_charty` | 403 | 345 | ✓(W10 — 차티 경로 열림을 리뷰 항목으로) |
| `routers/api/ext.py:192 · 196 · 198` 접근 로그 · IP 한도 `integration is None` | 로그 · 판단 | 343 | ✓(인증 여부를 따로 두라는 것까지 있음) |
| `routers/api/ext.py:321 · 343 · 377 · 522 · 576` | `record_view` · `charty_writes` 에 넘김 | 346 | ✓ |
| `routers/api/ext.py:597 · 614 · 631 · 650` | `Writer(…, grant.partner)` | 346 | ✓ |
| `routers/api/ext.py:491 · 526 · 542 · 546 · 609 · 626 · 645` `partner_actor` | `X-Ext-Staff-Id` 변수 이름일 뿐 | 351 「이름」 묶음 · 261 | ✓(값 아님) |
| `models/ext.py:25 · 38` `partner_outbox` 칸 · 유일키 | 칸 · 유일키 | 347 | ✓(W10 ② 중복 행) |
| `models/ext.py:53` `partner_consultation_start.partner` | 칸(PK = `visit_id` · 유일키 없음) | 348 | ✓ |
| `models/ext.py:62 · 69` `partner_payment_request` 칸 · 유일키 | 칸 · 유일키 | 348 | ✓ |
| `services/ext_writes.py:52 · 56 · 72 · 90 · 140` | 기록 · `replay` 거름 · payload | 349 | ✓ |
| `services/ext_charty.py:55 · 81 · 154 · 165 · 180` | 기록 · 결제 재요청 거름 | 350 | ✓ |
| `services/ext_audit.py:13 · 26`(+ `:27` `partner_staff_id` 키 이름) | payload | 350 | ✓ |
| `common/config.py:105` `ext_partner_grants` | env 이름 | 351 · 353 | ✓ |
| `services/emr_sync.py:421 · 428` `run_partner_outbox` · 결과 키 `"partner"` | 이름(값 아님) | 351(`ext_delivery` 묶음) | ✓ |
| `emr/base.py` · `ext_commands.py` · `kos/ext_reads.py` · `kos/agreements.py` · `normalized.py` · `sync_kos_keys.py` · `sync_partner_guards.py` · `sync_schedules.py` · `dtos/partner_agreements.py` · `schemas/ext_agreements.py` · `schemas/ext_charty.py` · `services/ext_agreements.py` · `ext_customer.py` · `ext_delivery.py` · `ext_detail.py` · `ext_refresh.py` · `ext_sync.py` · `tasks/ext_refresh.py` · `common/logs.py:41`(주석) · `static/PRETENDARD-LICENSE.txt` | 이름 · 주석 · docstring — `partner` 값을 읽지 않음 | 351 은 다섯 묶음만 이름을 들었지만 「값을 쓰지 않음 · 이름 그대로」 원칙에 모두 든다 | ✓ |
| `migrations/0017 · 0029`(칸 · 유일키) · `0030`(down_revision 이름) | 지난 migration | 524(번호 = WORK) | ✓(새 migration 필요 — W10 ②) |
| `tests/**` 11개 파일 | 시험 | **없음** | W10 ① |

값을 쓰는 곳 가운데 표에서 빠진 것: **0** → FAIL 없음.

## OQ 분류 표

| OQ | 정말 열렸나 | 분류 제안 | 메모 |
|---|---|---|---|
| Q01 `reserve` 에 `counselor` | 예 | **구현 때 실물 확인** | W7: 「당일 지정 상담사」 = `reservation.counselor` 화면 확인도 더함 |
| Q02 `update-reservation` 메모 · 유입 | 예 | **구현 착수 전 실물 확인 → 안 되면 사용자 질문** | F3: 대체 동작 지우기 |
| Q03 W2 `email` | 예 | 구현 때 실물 확인 | `_visitor_open` 은 모르는 키를 막지 않는다(`writes.py:234`). 「열어야 함」보다 「실물에서 저장되나」만 보면 된다 |
| Q04 화면 문구 | 예 | **사용자(기획자) 질문** | W8 · W9 ① 의 글자도 여기로 |
| Q05 재진 그날 예약 막나 | 예(코디 ③ = 이번엔 안 막음) | 사용자 질문(다음 판) | — |
| Q06 빨간 점 범위 | 예 | **코디 기본값(지금)** | W4 — DB 칸이 달려 있어 착수 전에 닫아야 함 |
| Q07 통역 코드 · 한국어 이름 | 예 | 코디 기본값(지금) | 메모 합치기에 이름이 다 필요하다 — `APP_LANGS` 7개 이름표를 정한다 |
| Q08 `book()` 생년월일 선택 | 예(결정 「열린 것」) | 사용자 질문(범위 밖) | — |
| Q09 확정 스레드 수정 버전 일시 지남 | 예 | 코디 기본값 | 「요청됨 그대로」 제안 그대로 받아도 됨 |
| Q10 취소됨 스레드 `change` · `cancel` | 예 | 코디 기본값 | F1 과 함께 표 칸으로 닫기 |
| Q11 `X-Day-Client` 값 규칙 | 예 | 코디 기본값 | 제안(영소문자 · 숫자 · `-` 1 ~ 16) 그대로 |
| Q12 키 나누기 · 배포 순서 | 예 | **사용자 · taewoo(배포)** | 링키 · 차티 외부 키 교체 일정 포함 |
| Q13 E4 쪽 나누기 · 경계 | 예 | 코디 기본값 / WORK | (`updated_at`, `id`) 커서 제안 |
| Q14 메모 안 줄바꿈 | 예 | 코디 기본값 | 「그대로」 |
| Q15 확정 스레드 고객 바꾸기 | 예 | **사용자 질문** | KOS 고객 바꾸기 쓰기가 없다(RQ27) — 거절할지 받을지는 제품 판단 |
| Q16 운영 시간 밖 · 간격 칸 | 예 | 코디 기본값 | 웹 예약 등록 `start_at` 과 같게(지금은 「받음」) |
| Q17 「고객 확인 필요」 글쓴이 · 버튼 · 사본 | 예 | 코디 기본값 | W6: 「사본」 까닭 고치기 |
| Q18 「최근 방문」 원천 | 예 | 구현 때 실물(데이터) · 코디 기본값 | W12 |
| Q19 확인 전 새 버전 | 예 | 코디 기본값 | F2 · W1 과 같이 보기 |
| (새 제안) 이메일 없는 고객의 `customerId` | 없음 → 더할 것 | **사용자 질문** | W6 |
| (새 제안) 닫힐 때 「답변 대기」 처리 | 없음 → 더할 것 | 코디 기본값 | W3 |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning(모두 다른 제품: selly 등 — **products/day 0줄** · 무관)
- `doc_no: DAY-DOC-12` = products/day 안에서 하나뿐(현행 최대 다음 번호)
- 시안 v15(base64 뺀 사본) grep: SPEC 이 시안 문구로 든 「새 예약 요청이 없어요」 · 「보내지 못했습니다」 · 「예약을 만들었어요 / 수정했어요 / 취소했어요」 · 토스트 세 개 · 「원장/상담사」 · 「예약 생성됨 · 수정됨 · 취소됨」 · 「제안 일시」 · 「예약 현황 표에서 시간을 누르세요」 · 「1160」 → 모두 있음. 「고객 확인 필요」는 시안에 0 — RQ24 의 글자(근거 있음)
- 모든 FAIL · WARN 에 파일:줄 + 근거(RQ# · be-probe § · 코드 ref)를 달았다. 근거 없는 지적 0
- 리포 파일 수정 · 커밋 · stash 0
