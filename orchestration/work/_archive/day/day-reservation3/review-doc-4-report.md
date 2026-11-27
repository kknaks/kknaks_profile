# 리뷰 리포트 — day-reservation3 / doc 4차 (2026-11-26)

대상: 같은 워크트리 미커밋 변경(planner 고침 3 뒤). 대조: `review-doc-3-report.md` · `planner-fix-3-instructions.md`(코디 기본값 — 다시 열지 않음) · CENTURION_DAY `origin/dev`(`routers/` · `templates/` · `emr/outbox_rules.py`). 파일 수정 0 · lint 1회. 사용자 질문(Q04 · Q05 · Q08 · Q12 · Q15 · Q20)은 지적하지 않음.

## 판정: WARN — FAIL 0 · WARN 1 (3차 M1 · M2 닫힘)

스레드 쓰기 행을 **다시 보낼 수 있는 입구**를 코드에서 전수로 셌다. 모두 막혔거나 스레드 「확인 대기」 안에서만 열린다. 남은 이중 예약 길은 하나다. 새 구멍이 아니라, SPEC-007 이 이미 받아들인 「만들기 쓰기 시간 초과」 위험이 스레드의 [접음] · [예약 생성]으로 이어지는 자리다(V1).

### WARN

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| V1 | spec-008:202 · 273 · 418 · 462 ↔ 코드 `emr/outbox_rules.py:54 ~ 60 · 76 ~ 83 · 101` | **만들기 쓰기(W2 · W3)는 시간 초과 · 오래 확인 안 됨이면 바로 `failed` 가 된다. 그런데 그때 KOS 에는 이미 예약이 생겼을 수 있다**(코드 주석 「시간 초과 뒤 KOS 에 이미 생겼으면 둘이 된다」). `failed` 행은 뒤 조회로도 확인되지 않으니(`decide_on_poll` 은 SENT · PENDING 만 본다), `visit_id` 가 연결되지 않아 스레드는 「예약 없음」이다. 이때 ① [다시 시도]를 누르면 W3 을 한 번 더 보낸다 ② [접음]을 누르면 → 링키 `change`(→ `new`) 나 답할 버전 `new` 에 [예약 생성]이 다시 켜진다 → 어느 쪽이든 KOS 예약이 둘이 될 수 있다. 한편 동기화로 들어온 그 KOS 예약은 스레드와 이어지지 않은 채 표에 뜬다. SPEC-007 은 웹 예약 등록에서 같은 위험을 「사람이 고른다」(D9 · D22)로 받아들였다. SPEC-008 에는 이 경우가 적혀 있지 않아, 직원이 확인할 것도 구현이 막을 것도 없다 | SPEC-007 D9 · D22 · 코디 결정 11-26 F2 · N1(이중 예약 막기) | 코디 기본값 하나를 고른다. ⓐ SPEC-007 과 같이 「사람이 고른다」를 SPEC-008 실패 처리(462)에 적는다 — W2 · W3 실패 줄에 「KOS 에 생겼는지 표에서 먼저 확인」 안내(글자 비움 · OQ-Q04). 또는 ⓑ W3 이 `failed` 로 끝난 묶음을 접으면 그 스레드의 [예약 생성]을 같은 고객 · 같은 시각 DAY 사본 예약이 없을 때만 연다. 어느 쪽이든 케이스 표에 한 줄 |

## 3차 지적 — 닫힘 확인

| # | 고친 자리(파일:줄) | 판정 |
|---|---|---|
| M1 | spec-008:417(공용 다시 시도 두 길 = 스레드 행이면 늘 409) · 418(접을 때 「접힘」 · 어느 다시 시도 길로도 못 보냄) · 462(공용 토스트 「다시 시도」 = 스레드 열기) · spec-000:677 · spec-007 고침 6 ⑥ · spec-007:538 | 닫힘 — 세 문서가 같은 말 |
| M2 | spec-008:370 E5 `closedReason` = `withdrawn` · `expired` · `folded`(병원이 처리를 접음) · spec-000:671 | 닫힘 |

## 스레드 쓰기 행 다시 보내는 입구 — 전수 (지시 ②)

방법: `git -C CENTURION_DAY grep -n -i 'retry\|resend\|requeue' origin/dev -- backend/day/routers` + 같은 말 `templates` · `static/day.js` + 쓰기 큐 자동 재전송(`emr/outbox_rules.py`).

| # | 입구(코드) | 무엇을 다시 보내나 | 스레드 행에 대해 SPEC | 판정 |
|---|---|---|---|---|
| 1 | 새 `POST /reservations/requests/{request_id}/retry`(spec-008:416) | 그 스레드 실패 묶음 | 확인 대기일 때만 · 접었거나 확인됐으면 409(N1) | ✓ 막힘 |
| 2 | `POST /reservations/visits/{visit_id}/retry`(`routers/reservation_detail.py:335 ~ 347`) | 그 방문의 실패한 쓰기 | 스레드 행이면 늘 409(spec-008:417 · spec-007 고침 6 ⑥) | ✓ 막힘 |
| 3 | `POST /reservations/retry` `write_id`(`reservation_detail.py:350 ~ 360`) | 방문 없는 쓰기(새 예약 W3 실패) | 늘 409(같음) | ✓ 막힘 |
| 4 | 예약 현황 실패 토스트 「다시 시도」(`templates/partials/reservations_dialogs.html:120 ~ 126` — 2 · 3 을 부름) | 2 · 3 과 같음 | 스레드 행이면 스레드 창을 엶(spec-008:462) · 경로가 막혀도 2 · 3 이 409 | ✓ 막힘 |
| 5 | 시술 현황 실패 토스트(`templates/partials/board_toast_kos_failed.html`) | 없음 — 「다시 시도」 버튼 없음(글만) | 해당 없음 | ✓ |
| 6 | 쓰기 큐 자동 재전송 — 만들기 아닌 쓰기의 오류 · 값 안 맞음(`outbox_rules.py:35 ~ 40 · 64 · 116 ~ 117` · 최대 3번) | W4 · W5 · W18 | `pending` · `sent` 일 때만(= 확인 대기 안) · `failed` 뒤엔 안 보냄 · 접은 행은 `failed` | ✓ 대기 안에서만 |
| 7 | 쓰기 큐 자동 재전송 — 만들기(W2 · W3) | 없음 — 오류면 바로 `failed`(`outbox_rules.py:54 ~ 60` · 「저절로 다시 보내지 않는다」) | 해당 없음 | ✓ (단 KOS 에 생겼을 수 있음 → V1) |
| 8 | 웹 버튼 다시 누름 [예약 생성] · [예약 수정] · [예약 취소] | 새 묶음(다시 보내기 아님) | 확인 대기 · 「예약 있음」이면 409(W2 · F2) | ✓ (V1 의 「예약 있음」 못 앎만 남음) |
| 9 | `…/photos/{photo_id}/kos-retry`(`routers/board_photos.py:178` · `api/board_photos.py:132`) · `/api/id-photos/{id}/kos-retry`(`api/displays.py:193`) · `…/questionnaire/resend`(`reservation_displays.py:149`) | 사진 · 여권 · 문진 쓰기 | 스레드 묶음 행이 아님 | 무관 |
| 10 | ext 쓰기 전달(`services/ext_delivery.py` `run_partner_outbox`) | `partner_outbox`(다른 표) | ext E1 ~ E6 은 KOS 를 부르지 않음(spec-008 Rule 7) | 무관 |

입구 10 개 가운데 스레드 행을 「확인 대기」 밖에서 다시 보낼 수 있는 것 = **0**. 이중 예약 길 = V1 하나(다시 보내기가 아니라 「KOS 에 생겼는데 DAY 가 모름」).

## 문서끼리 대조

| 규칙 | spec-008 | spec-000 | spec-007 | 맞나 |
|---|---|---|---|---|
| 공용 retry 409 | 417 · 462 | 677 | 고침 6 ⑥ · 538 | ✓ |
| 「접힘」 = 못 보냄 | 418 · 462 | 677(표시 칸 = WORK) | 고침 6 ⑥ · 538 | ✓ |
| 토스트 「다시 시도」 → 스레드 열기 | 462 | — | 고침 6 ⑥ · 538 | ✓ |
| `folded` | 202 · 273 · 370 · 499 | 671 | — | ✓ |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error** · 263 warning — products/day 0줄(다른 제품 · 무관)
- 지적마다 파일:줄 + 근거(코드 ref · SPEC-007 D 번호 · 코디 결정 번호). 사용자 질문 OQ 지적 0 · 리포 수정 · 커밋 · stash 0
