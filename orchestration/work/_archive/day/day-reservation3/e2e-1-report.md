# e2e 1 결과 보고 — 로컬 스택(11140 · kos-demo) + KOS 데모 지점 실물

## 상태: done (스택 시작 · 멈춤 · 코드 수정 없음)

- 2026-11-26 밤 · ext 로컬 키(값 출력 없음) · 웹 세션 하나(끝에 로그아웃) · DB = SELECT 만 · 스크립트 `/private/tmp/day-e2e-r3/`(`run.py` · `run.out` · `state.json` — id 앞 8자만)
- 시험 고객 = 이름 「E2E … (시험)」 · `example.com` 이메일 · 예약 = 3 ~ 8일 뒤 · **만든 예약 5건 전부 취소 확인**

## 맨 위 표

| # | 시험 | O/X | SSE · 시간 | 비고 |
|---|---|---|---|---|
| 1 | E7 · E8 · 직원 목록 | O | — | 그룹 13 · 유입 14 · 원장 · 상담사 태그로 고름 |
| 2 | 초진(이메일만) E1 | O | `reservation_request` **0.1s** | 202 `new` · 판정 `new` |
| 2 | 알림 행 | △ | — | **n=0 — 이 병원에 DAY 계정이 있는 직원이 시험 계정 하나(직무 nurse)뿐**이라 받는 사람 없음(아래 ①) |
| 2 | 목록 · 창 · 2열 조각 | O | — | 200 · 창에 [예약 생성] · 초진 배지 |
| 2 | [예약 생성] → W1 → W2 → W3 → 확정 | O | `write_confirmed` **1.6s** · 확정 1.1s | W2 본문 키 `name · gender · email` · W3 `counselor` · 합친 메모(희망 시술 → 통역 → 예약 메모) · 유입 |
| 2 | DAY 사본(KOS 다시 읽음) | O | — | 상담사 = 고른 직원 O · 유입 O · 메모 O |
| 2 | `reservation_applied` · E5 · E4 `updated_since`(5분 겹쳐) | O | — | E5 `confirmed` · `reservationId` 있음 |
| 2b | review W3 — 이름만 W1(같은 이름 · 다른 이메일) | **X(발견)** | — | 아래 ② |
| 3 | 재진(이름 대소문자 다름 · 이메일 대문자) | O | 2.1s | 판정 `returning`(앞 고객) · 생성 = W3 하나 |
| 4 | E2 `change`(시간 · 메모 · 희망 시술 · 상담사 null) → [예약 수정] | O | 2.1s | W4 한 본문 + `reservationMemo` · `funnel` · 시작 시간 바뀜 O |
| 4 | review W4 — 상담사 비움 | **X(발견)** | — | 아래 ③ |
| 5 | 변경 요청(칩 2) → E5 → E2 새 버전 → 대체됨 · 버튼 돌아옴 · [철회] | O | — | 확정 스레드에 보낸 첫 변경 요청 = 400(답할 버전 없음 — 상태 표대로 · 시험 순서 탓) · 새 버전 뒤 waiting · 칩 2 · 「답변 대기중」 · 새 버전 → `superseded` · [예약 수정] 돌아옴 · [철회] → `withdrawn` |
| 6 | 다른 고객 `change` → 400 `customer_changed` · 구분 값 없는 E1 → 400 | O | — | |
| 7 | E2 `cancel` → [예약 취소] → W5 | O | 2.1s | 취소됨 · applied = create · update · update · cancel |
| 8 | N5 순서 B(링키 `cancel` → 예약 현황에서 취소) | O | 10초 회차 안 | 자동 **취소됨** + `reservation_applied`(cancel · 누른 직원 없음) |
| 8 | N5 순서 A(예약 현황 먼저 취소 → 링키 `cancel`) | O(SPEC 대로) | — | E2 = 409 `request_finished`(예약 없음 cancel) — 링키는 E5 에서 「확정」 + 예약 취소를 볼 길이 없다 → 아래 ④ |
| 9 | 실패 한 건 | 건너뜀 | — | DB 를 건드리지 않고 KOS 실패를 만들 길이 없음 |
| 10 | 정리 · 로그아웃 | O | — | 5건 `canceled` · 로그아웃 204 |

## review W3 · W4 실물 결과

- **② W3(이름만 W1)**: 이메일만 있는 초진의 `find-duplicated-visitor` 본문 = `{name}` 하나. KOS 는 **같은 이름 고객이 있어도 「없음」** 으로 답했다(2b — 앞에서 만든 같은 이름 고객이 KOS 에 있음). 그래서 [예약 생성]이 막히지 않고 **같은 이름 KOS 고객이 하나 더 생겼다**(시험 고객 2명 — 지우지 않음). 같은 고객 판정은 DAY 쪽(이름 + 이메일)만 믿을 수 있다. 제안(결정 아님): W1 본문에 `email` 을 싣는 것이 KOS 에서 되는지 probe 한 번 · 또는 이 틈을 OQ 로.
- **③ W4(상담사 비움)**: 링키가 `counselorStaffId: null` 로 고쳐도 W18 을 보내지 않아(코드 `services/reservation_request_actions.py` [예약 수정] — `counselor is not None` 일 때만 W18) **KOS 「당일 지정 상담사」가 그대로 남는다**(다음 동기화 DAY 사본 `requested_counselor_id` = 이전 상담사). KOS 에 「없음」을 쓰는 본문은 실물 확인 전 — 기획 결정 · probe 필요.

## 버그 · 발견 목록

| # | 무엇 | 원인 file:line | 몫 |
|---|---|---|---|
| ① | 알림 받는 사람 = **DAY 에 한 번이라도 로그인해 계정이 생긴** admin · coordinator 직원만. 로컬 데모는 0명이라 행 0 — 코드 결함 아님. 실제 병원에서도 DAY 안 쓰는 직원은 못 받음(의도 확인) | `services/reservation_request_threads.py` `receivers`(Staff.account_id 조인) | 코디 · 기획 |
| ② | 이름만 W1 이 같은 이름을 못 찾음 → 중복 KOS 고객 | `services/reservation_book.py` `_lookup_body`(이메일 안 실음) ← `reservation_request_actions._new_customer` | be(실물) · 기획 |
| ③ | 상담사 비우기가 KOS 에 안 감 | `services/reservation_request_actions.py` [예약 수정] W18 조건 | be · 기획 |
| ④ | 순서 A(예약 현황 먼저 취소)면 링키 `cancel` = 409 `request_finished` 로 끝나 스레드는 「확정」으로 남는다 · 링키가 예약 취소를 알 길이 E5 에 없음(`reservationId` 만) | SPEC 정의대로(`policies/reservation_request.py` `recorded_kind`) | 코디 · 기획 |
| ⑤ | e2e 스크립트 첫 로그인 2번이 쿠키(`Secure`)를 못 받아 로그아웃을 못 한 DAY 세션 2개가 남음(KOS 기기 한도 쪽 영향은 확인 안 함) | 시험 도구(로컬 http 에 Secure 쿠키) | 코디 참고 |

코드 결함(fe/be)은 이번 시험에서 나오지 않았다.
