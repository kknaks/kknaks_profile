# 리뷰 리포트 — day-reservation3 / doc 5차 · SPEC-008 마감 검수 (2026-11-27)

대상: 워크트리 `day-reservation3-spec` 커밋 `HEAD` `2eec7303`(origin/main `af1e5809` 위 한 커밋 · `git diff origin/main..HEAD`).
대조한 것:
- `planner-close-1-instructions.md` · `planner-close-1-report.md`
- `be-swagger-1-report.md` ③ ④ · `be-swagger-2-report.md` · `fe-nav-1-report.md` ⑤
- 코드 `CENTURION_DAY/day-reservation3`

파일 수정 0 · 커밋 · stash 0 · lint 1회. 사용자 질문(Q04 · Q05 · Q08 · Q12 · Q15 · Q20)은 지적하지 않았다. 코디 기본값도 다시 열지 않았다.

## 판정: WARN — FAIL 0 · WARN 4

main 쪽 내용은 빠진 것이 없다. 번호 충돌은 한 곳만 빼고 바르게 갈렸고, 그 한 곳은 옛 log 행이다(X1). SPEC 의 판정 규칙 · 식별값 · W3 counselor · W18 · cancel 202 · 재시도 응답 · 오류 코드 · 로그인 뒤 갈 곳 · 셸 메뉴는 코드 분기와 같다. 남은 넷은 모두 문장을 맞추는 일이다.

### WARN

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| X1 | `log.md:50`(2026-11-25 `spec-change, wp-remove` 행) | **이미 있던 log 행의 번호를 바꿨다.** 「이 PR 의 DAY-SPEC-006 개정 ⑭(웹 화면 열림 설정)」 → 「개정 ⑮」. 이 행은 base `ae8cec61` 에도 그대로 있던 11-25 기록이다. 그때의 ⑭(되돌린 웹 열림 설정)를 가리킨다. 지금 ⑮ 는 예약 요청 칸(11-26)이므로, 바뀐 글은 다른 개정을 가리키게 된다. planner 보고 ①의 「우리 글만 바꿈」과도 다르다 | `git diff origin/main..HEAD -- products/day/log.md`(-/+ 한 쌍) · `git show ae8cec61:products/day/log.md`(같은 행 있음) · `rules/document-pipeline.md` §log.md(누적 장부) | 이 행을 origin/main 글 그대로 「개정 ⑭」로 되돌린다. 번호 바꿈 기록은 11-27 행 하나로 충분하다 |
| X2 | `spec-008:290` · `:336` · `:538` · `:592` ↔ 코드 `services/reservation_request_ext.py:389 ~ 393` · `policies/reservation_request.py:customer_changed` | 「예약 있음」에 **초진 · 2명 이상 `change`** 는 400 이라고 적혀 있다. 그런데 코드는 `thread.customer_id != checked.matched` 로만 본다. 초진 **생성 확인 대기 중**(W3 확인 전 · E1 이 초진이라 `thread.customer_id = None`)에 초진(`matched = None`) `change` 가 오면 `None == None` 이라 **202 로 받는다.** 2명 이상 `change` 도 같다. 고객이 이미 연결된 뒤(재진이거나 W3 확인 뒤)에는 SPEC 대로 400 이다 | 코드 분기 · `create()` `customer_id=checked.matched` · be-swagger-1 ④(`customer_changed`) | SPEC 에 한 줄을 더한다. 「스레드에 고객이 아직 없음(초진 생성 확인 대기) = 막지 않음 · 비교 = 스레드 고객 ↔ 새 판정 고객」. 코드를 고칠 일은 아니다. W3 확인 때 `_link_visit` 이 고객을 정하는 흐름과 맞다 |
| X3 | `spec-008:455` · `:500` · `spec-007` 고침 7 | 공용 다시 시도 두 길이 스레드 행이면 「늘 409」라고만 적혀 있고 **오류 코드 이름이 없다.** 코드는 새 코드 `request_thread_write`(`services/reservation_writes.py:360` · `:366` · `common/error_codes.py:144`)를 낸다. SPEC-008 · 007 어디에도 이 이름이 없다(grep 0). QA 기대 결과에 코드 값이 비어 있다 | 코드 grep · document-pipeline 「error code 가 바뀜 → SPEC」 | 455 행 409 칸에 `request_thread_write` 를 적고, SPEC-007 고침 7 의 같은 줄에도 적는다 |
| X4 | `spec-001:206`(대응표 「권한 없는 동작 · 화면(로그인 뒤 갈 곳 포함)」) · `:222` 규칙 7 · `:553` 규칙 9 | 로그인 뒤 갈 곳이 `/reservations` 로 바뀌었다(개정 ⑮ · `:158`). 그런데 대응표의 「로그인 뒤 갈 곳 포함」 칸은 아직 「단 시술 현황 보기(`board` view)는 기본값으로 모든 직군」만 근거로 든다. 지금 로그인 직후에 보는 권한은 `reservation` view(SPEC-006 R31 · 코드 `routers/reservations.py` `require_permission("reservation")`)다. fe-nav-1 ③ 의 「`board` 만 있는 직무 = 로그인 직후 권한 없음」도 이 칸에서 읽히지 않는다 | `fe-nav-1-report.md` ③ ⑤ · spec-006:452 R31 | 206 칸에 「로그인 뒤 갈 곳 = 예약 현황 → `reservation` view(모든 직무 기본값 · R31) · 사람이 그 행을 지운 직무는 로그인 직후 권한 없음 화면」 한 줄. 규칙 7 · 9 는 `board` 기본값 설명이라 그대로 둬도 된다 |

참고(지적 아님): `spec-008:589` 는 식별값이 「정확히 같음」이라고 적었다. 코드는 이메일만 앞뒤 공백 · 대소문자를 무시한다(`reservation_request_ext.py:239` `lower(trim(email))`). 이름 비교 방식(대소문자 · 띄어쓰기 무시)과 같은 결이라 위험은 없다. 원하면 Rule 1 괄호에 「이메일 대소문자 무시」를 더하면 된다.

## ① main 쪽 내용 · 번호 충돌

방법: `git diff -U0 ae8cec61..origin/main -- products/day` 에서 더해진 줄 **794줄**(12 파일)을 하나씩 `git show HEAD:<파일>` 줄 집합과 대조했다.

| 결과 | 줄 |
|---|---|
| HEAD 에 그대로 있음 | 787 |
| `last_updated` · `최종 수정` 날짜 칸(11-27 로 바뀜 · 예상한 차이) | 5 |
| 낱말 단위로 합쳐 바뀐 줄 — `20-spec.md:50`(main 문진 · 여권 취소선 + 우리 「예약 요청 → DAY-SPEC-008」) · `:106`(끝에 `· DAY-SPEC-008 §5`) | 2 — 두 줄 모두 main 글이 빠짐없이 들어 있음 |

`origin/main..HEAD` 에서 지운 main 줄도 전부 봤다. 날짜 · 우리가 바꾼 SPEC-001 · 006 의 옛 줄(취소선으로 남김) · `20-spec.md` 합친 줄 · **log 11-25 행(X1)** 이 전부다.

| 번호 | 확인 | 판정 |
|---|---|---|
| SPEC-006 ⑭ / ⑮ | main ⑭ = 직원 앱 예약현황(`spec-006:56` · `20-spec.md:50` · `10-decision.md:40` 그대로) · 우리 = ⑮(`:52` 보충 · `:54` 본문 · 183 · 193 · 194 · 197 · 203) · spec-005 · spec-008:255 · 259 · 318 · 915 도 ⑮ | ✓ (log:50 만 X1) |
| SPEC-007 고침 6 / 7 | main 고침 6 · 보충 · spec-sync-2(`spec-007:51 ~ 55`) 그대로 · 우리 = 고침 7(214 · 216 · 219 · 221) · spec-008:259 · 20-spec · log 「고침 7」 · `10-decision.md:40 · 63` · spec-000 · 005 의 「고침 6」은 모두 main(WORK-002) 글 | ✓ |
| SPEC-001 ⑭ / ⑮ | main ⑭ = KOS 쓰기 토큰 예외(`spec-001:55` · `:548`) · 우리 = ⑮(`:53` · 158 · 159 · 611) | ✓ |
| SPEC-000 ③ · SPEC-005 | 날짜 개정(main 11-25 · 우리 11-26 / 11-27)이라 겹침 없음 | ✓ |
| 충돌 표지 | `grep -rn '^<<<<<<<\|^=======\|^>>>>>>>' products/day` = 0 | ✓ |
| `doc_no` | SPEC-008 `DAY-DOC-12` = 전체 1건(main 과 겹침 없음) | ✓ |

## ② SPEC ↔ 코드

| 항목 | SPEC | 코드 | 판정 |
|---|---|---|---|
| 판정 Rule 1 | `spec-008:589` 이름(대소문자 · 띄어쓰기 무시) + 식별값 하나 이상 · 국적 양쪽 있을 때만 · 1 = 재진 · 0 = 초진 · 2+ = 막음 | `reservation_request_ext.py:219 ~ 258` `same_customers`(이름 `regexp_replace \s` + `lower` · `or_(birth, phone+dial, sns, email)` · 국적 = DAY 빈 값 또는 같음 · `limit 2`) · `policies:match_result` | ✓ (이메일 대소문자 = 참고) |
| 식별값 필수 · `birthDate` 선택 | `:358` · `:374` · `:526` 400 | `schemas/ext_reservation_request.py:167` `date \| None` · `:181 ~ 185` `model_validator` | ✓ |
| [예약 생성] W3 `counselor` | `:470` 최상위 `counselor{id,name}` · W18 없음 | `reservation_request_actions.py:322 ~ 329` `ReserveWriteData(counselor=…)` · `emr/kos/writes.py:141 ~ 142`(`reserve` 만 `counselor` 풂) · `:361 ~ 373` | ✓ |
| W1 · W2 `email` | `:471` | `reservation_book.py:126 ~ 129` W1 · `writes.py:337` W2 | ✓ |
| W18 = [예약 수정] 바꿈 · 지움만 | `:473` · `:478` · `:482`(`counselor: {}`) | `reservation_request_actions.py:400 ~ 406`(`visit.requested_counselor_id` 와 비교) · `writes.py:152 ~ 155` · `:393 ~ 401` | ✓ |
| 예약이 이미 취소된 스레드 `cancel` | `:272` 요청됨 · 확정 → 202 `canceled` + `reservation_applied` `cancel` · 취소됨 · 닫힘 409 | `policies:recorded_kind`(`has_visit ∧ status ∈ {REQUESTED, CONFIRMED}` → CANCEL) · `reservation_request_ext.py:412 ~ 430` `closing` → CANCELED + 댓글(`SYSTEM`) | ✓ |
| 동기화 자동 `canceled` | `:281` 요청됨 ∧ 마지막 `cancel` ∧ 예약 없음 | `settle.py:148` `cancel_done`(REQUESTED ∧ CANCEL ∧ ¬booked) | ✓ |
| `customer_changed` | `:290` · `:336` · `:592` | `reservation_request_ext.py:389 ~ 393` | 대부분 ✓ · 초진 확인 대기 = X2 |
| 재시도 `accepted_status` | `:300` 처음 응답 그대로 · spec-000 `accepted_status` | `reservation_request_ext.py:319` `_replay` · `:354`(E1) · `:414`(E2) · `models/reservation_request.py:134` · migration `20261126_0031` | ✓ |
| ext 오류 코드 표 | `:321 ~ 346` | `common/error_codes.py:126 ~ 146` · be-swagger-1 ③ 와 같음 · 검사 순서(404 → 본문 → 상태) = `add_version` 순서 | ✓ |
| 웹 공용 retry 409 | `:455` 「늘 409」 | `reservation_writes.py:360 · 366` `request_thread_write` | 코드 이름 빠짐 = X3 |
| 로그인 뒤 갈 곳 | `spec-001:158` · `:611` `/reservations` | `routers/login.py:71 ~ 77` | ✓ (대응표 = X4) |
| 셸 메뉴 | `spec-001:159` · `spec-006:134 · 142 · 451` 「현황」 `status` · 화면 있는 메뉴 = 고객 · 현황 | `menu.py:22`(`status` · 「현황」) · `:36 ~ 42` HREFS(`customer` · `status` · 탭 둘) | ✓ |
| 화면 글자 | `spec-008:160 · 162 · 166` 「답변 대기중」 · [철회] · [KOS 등록 실패] | `templates/partials/reservations_request_parts.html:17` | ✓ (`reservations_request_window.html:4` 주석만 옛 글자 · 동작 무관) |

## ③ stable · lint

- stable 근거는 `spec-008:42` ⑩ 에 있다. 구현 머지 · dev 배포 · 실물 e2e 2회가 끝났고 prod 는 다음이다. 남은 OQ(Q04 · Q05 · Q08 · Q18 · Q22 · Q23)는 모두 비차단이다. `20-spec.md:90` SPEC List = stable · `30-work.md:51` = `in_dev` 이고, lint 5→6 게이트와도 맞는다. ✓
- `python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error** · 263 warning. products/day 는 0줄이다(다른 제품 · 무관).
- 한계: 이 코드 워크트리 HEAD 는 `8a5ee874`(#297 커밋)다. SPEC 이 적은 dev 스쿼시 `65506f35` 는 로컬에 없어 대조하지 못했다(fetch 하지 않음). 그래서 위 코드 ref 는 `8a5ee874` 기준이다. 지시서의 「dev 머지본」이라는 말대로 같은 내용이라고 보았다.
