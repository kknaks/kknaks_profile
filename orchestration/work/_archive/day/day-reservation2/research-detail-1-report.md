# research-detail-1 — 예약 상세 모달: 칸 · 버튼 원천 전수 표 + 시술현황 차트 비교

- 작성: day researcher · 2026-11-24 · 읽기 전용(코드 · 문서 · DB 고치지 않음)
- 근거 ref
  - 시안 = `reference/2026-11-23-reservation/20261124_예약현황_시연.html`(v9) — 줄 번호 = 원본 파일 줄(base64 만 `DATA` 로 바꾼 사본과 줄 수 같음 · 사본 `/private/tmp/rsv-detail-research/v9.html`). 「시안 L줄」로 적음
  - 11-13판 = 같은 폴더 `20261113_예약현황_시연 (1).html`(사본 `v1113.html`)
  - 코드 = CENTURION_DAY `origin/dev` `4bf0b4a1` — `dev:경로:줄`
  - 스펙 = mediness `origin/main` `c43633be` — `SPEC-006` · `SPEC-002` · `SPEC-000`
  - cc = cc-prototype `origin/main` — `cc:경로:줄`
  - KOS 공개 API 목록 = `ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md`(이하 「KOS 문서」)
  - 결정 = `reference/2026-11-23-reservation/reservation-board-decisions.md`(R1 ~ R75)

---

## 0. 한 줄 답

| # | 물음 | 답 |
|---|---|---|
| 1 | 칸 전수 | 시안 모달 칸 **38개** = **그대로 5 · 일부만 있음 6 · 가공 20 · 없음 7**. 없음 = 성명(여권) 매퍼 · 신분확인 · 초진 문진 · 건강정보 · 시술메모 · 귀가 사유 · 안내 띠 판정. 일부만 = 국적/통역의 「통역」 · 희망 시술의 「예산」 · 예약메모 작성자/시각 · 관리실 정원 · 시술권 기간 · 오더 메모 작성자/시각 |
| 2 | 버튼 · 동작 전수 | **51행** = 모달 data-s5 36 + 입력 3 + 흉내 막대 7 + 우클릭 5. DAY 에 경로가 이미 있는 건 **동행 묶기/풀기 · 귀가 대기(시술 현황 [귀가 대기])** 정도. 접수 · 상담/시술 대기 배정 · 예약 취소 · 예약 변경 · 의사 지정 · 오더 메모 쓰기 · 귀가(완료) · 수납 · 처방전 · 신분 확인 · 문진 띄우기는 **DAY 경로 없음** |
| 3 | 시술현황 차트와 비교 | 차트 모달 = 「고객 머리 줄 + [간호관리차트 \| 의사차트] 탭 × 시술마다 한 행(시술명 · 담당자 · 차트 글)」. 새 모달과 **같은 것은 고객 머리 줄(이름 · 발음 · 성별 · 만 나이 · 국적)과 시술 줄 목록 원천뿐**. 차트 JSON · 조각은 「오늘 판 카드 · 시술 완료 탭 방문만」 열려(`is_chartable`) 예약 · 앞날 · 지난 날 방문엔 그대로 못 쓴다. 새 모달이 차트를 「일부 고친 것」이라고 볼 근거는 코드에 없다 — 겹침이 작다 |
| 4 | 단계 경계 | 조건식 6개(`today` · `past` · `recvArea` · `live` · `cut` · `wide`)로 갈림 — §4 표. 시안 `S5` 는 **노쇼를 만들지 않는다**(색 표에만 있음) |
| 5 | 이전 방문 | DAY DB 에 같은 고객의 지난 `visit` 이 있다 — 데모 dev = 백필 `--from 2026-08` ~ 어제(11-19 실행 · 방문 1,319). prod 백필 실행 여부는 **확인 안 됨**. 네 줄 중 「예약 담당」 · 「받은 시술」은 DAY 칸 있음, 「상담」(실장 · 원장) · 「시술」(원장)은 가공(상담 기록 · 집도의) |
| 6 | 우클릭 메뉴 | 예약 변경 = KOS `schedule/open/v2/commands/update-reservation`(cc 는 내부 `schedule/reservation/v2/commands/update-reservation`) · 예약 취소 = `schedule/open/v1/commands/cancel-reservation` — **DAY 에 둘 다 경로 없음**. 동행 = 시안은 「모달 안 체크박스로 같은 열 · 같은 시각 예약을 고름」 · DAY 는 「카드를 다른 카드 위에 끌어 놓기 · 30분 행」(R66 · R71) |
| 7 | 로컬 데모 DB 표본 | **확인 못 함** — 접속 값이 `deploy/local.env`(읽기 금지)에만 있고, 로컬 docker 를 건드리지 말라는 조건. 표본 없이 칸 채움은 코드상의 동기화 여부(§1 「DAY 저장」 칸)로만 답함 |
| 8 | 빠진 것 | 새 KOS 읽기 3(문진 제출본 · 문진 양식 · (선택) 고객 상세) · 새 KOS 쓰기 7 이상(접수 · 단계 변경 · 예약 취소 · 예약 변경 · 예약 메모 · 오더 메모 · 상담 정보) · DAY 새 기록 4(신분확인 기록 쓰기 경로 · 시술메모/귀가 사유 · 메모 작성자/시각 · 시술권 기간). §8 표 |

---

## 「정할 것」(사용자에게 물을 것)

결정하지 않았다. 선택지와 근거만.

| # | 물을 것 | 선택지 | 근거 |
|---|---|---|---|
| Q1 | **범위** — 이번 판 모달 | ⓐ 읽기만(칸 표시 · 이전 방문 접기 · 동행 이름 눌러 이동 · 닫기) ⓑ ⓐ + DAY 에 이미 경로가 있는 쓰기(동행 · 시술 현황과 같은 귀가 대기) ⓒ 시안 버튼 전부(접수 · 배정 · 취소 · 변경 · 귀가 · 수납 …) | §2 — 경로 있는 쓰기는 동행 · 귀가 대기 뿐. ⓒ 는 §8 의 새 KOS 쓰기 7개 이상 |
| Q2 | 「시술현황 차트 일부 기능 수정」의 뜻 | ⓐ 새 모달을 따로 짓는다(차트는 그대로) ⓑ 차트 모달 안에 예약 정보를 더한다 ⓒ 새 모달의 시술 목록 줄에서 차트 모달을 연다(시술 현황과 같은 입구) ⓓ 사용자 말의 대상이 다른 것 | §3 — 겹침 = 머리 줄 · 시술 줄 목록뿐. 차트 열림 조건 `is_chartable`(오늘 판 · 시술 완료 탭) |
| Q3 | 노쇼 | ⓐ 시안처럼 노쇼 상태 화면 없음(취소로 보임?) ⓑ 머리 「노쇼」 · 색 `--red`(시안 `S5_C` 에 있음) · 버튼 없음(`cut`) | 시안 L2053 `S5` 는 노쇼를 안 만듦 · L2055 색 · L2137 ~ 2138 조건엔 있음 · DAY `reservation_status = no_show` 있음 · SPEC-006 툴팁 「노쇼」 |
| Q4 | 신분확인 · 초진 문진 · 건강정보 세 줄 | ⓐ 이번 판 숨김 ⓑ 칸만 두고 값 없음 표시(시안 `미확인` · `작성 필요` · `문진 전`) ⓒ KOS 읽기 새로(문진 = `get-questionnaire-submit` · `get-visitor-questionnaire` · 신분 = 고객 상세 신분 칸 채움 여부) + 신분확인 기록 쓰기 | DAY `identity_check` · `questionnaire_history` 테이블은 있으나 쓰는 곳 · 읽는 곳 0(`git grep` · §1 #8 ~ 10) · cc 는 KOS 읽기 + 자체 기록 |
| Q5 | 「특이사항」 원천 | ⓐ `customer.customer_notes`(KOS 고객 `memo`) ⓑ `customer.legacy_notes`(KOS `migratedMemo`) ⓒ 없음(숨김) | 시안 L2173 `cu.caution`(가짜 칸) · cc `remark` = KOS 고객 `memo`(cc 스키마 `DetailCustomer.remark`) |
| Q6 | 「의사 지정」 원천 | ⓐ `visit.requested_doctor_id`(KOS `reservation.doctor`) ⓑ 묶음(occupiedResources)의 의사(cc 방식 — DAY 저장 확인 안 됨) ⓒ `visit.consultation_info_doctor_id` | `dev:backend/day/emr/kos/mapper.py:581` · cc `ReservationInfo.doctors` |
| Q7 | 「상담사」 원천 — 상담 정보 칸 | ⓐ R48 과 같게(상담 기록 첫 상담사 → 일정 상담 정보 상담사) ⓑ `visit.requested_counselor_id`(예약 때 지정 상담사) | R48 · `dev:backend/day/queries/reservations.py:160` · `mapper.py:578` |
| Q8 | 수납 정보 다섯 숫자 | 「총 수납 금액 = 결제총액(R51) · 수납 완료 = 수납(R49) · 수납 필요 = 미수(R50)」로 읽어도 되나 · 「상품 합계」 · 「할인 금액」은 ⓐ 구매 항목 원가 합 · (원가 − 조정 금액) 합 ⓑ 이번 판 0 / 숨김 | 시안 L2220 ~ 2225(할인 = 음수 상품 줄 — DAY 엔 그런 줄 없음 · `purchase_item.adjusted_amount` · `purchase_price_adjustment` 있음) · R49 ~ R55 엔 합계 · 할인 정의 없음 |
| Q9 | 수납 경고 · 「수납 완료」 배지 단계 조건 | ⓐ 시안대로 귀가 대기 · 귀가에서만 경고 ⓑ R42 처럼 단계 상관없이 | 시안 L2221 `warnPay = need && [귀가 대기, 귀가]` · R42 「단계 상관없이」 · R55(둘 중 하나) |
| Q10 | 시술 목록 「진행 / 미진행」 | ⓐ 오늘 작업(`visit_task`)이 있는 구매 구성 = 진행 · 없는 것 = 미진행 ⓑ 작업 상태(`visit_task.status` · 완료 / 취소) ⓒ 상태 칸 숨김 | 시안 L2213 ~ 2215 = 가짜 규칙(상품마다 첫 시술만 진행) |
| Q11 | 시술 목록의 행 단위 | ⓐ 구매 항목(상품) → 구성 시술(시안 모양) ⓑ 오늘 작업 줄(시술 현황과 같은 목록) | 시안 L2209 `pkgOf` · `dev:backend/day/models/purchase.py` `PurchaseItem` · `PurchaseItemComposition` |
| Q12 | 예약메모 「덧붙이기」 · 작성자 · 시각 | ⓐ 보기만(KOS `reservationMemo` 한 덩어리) ⓑ 덧붙이기 = KOS 메모 끝에 이어 씀(KOS `change-reservation-memo`) · 작성자 · 시각은 DAY 에 따로 남김 | v9 에 [덧붙이기] 버튼이 그려지지 않음 — 처리기만 남음(L2312 ~ 2315) |
| Q13 | 국적/통역의 「통역필요」 | ⓐ 국적만 ⓑ `customer.language`(KOS 언어)로 「통역필요」 판정 | 시안 L2173 = 외국인이면 고정 문구 「통역필요」 — DAY 에 통역 여부 칸 없음 |
| Q14 | 시술메모 · 귀가 사유 | ⓐ 뺌 ⓑ DAY 새 기록(귀가 처리 사유 · 시술 현황 「덜 끝난 채 귀가 대기」 사유) | DAY 시술 현황 [귀가 대기]에 사유 입력 없음(`dev:backend/day/services/board_tasks.py:222`) |
| Q15 | 안내 띠 「시술 없이 (바로) 귀가…」 판정 | ⓐ 뺌 ⓑ 「상담 뒤 시술 작업 0개로 귀가 대기」 같은 규칙을 새로 | 시안 L2229 `s.consultOnly`(charty 흉내 버튼에서만 켜짐) |
| Q16 | 관리실 정원 「(n/침대 수)」 | ⓐ 이름만(시술 현황 방 옮기기처럼) ⓑ 침대 수 원천을 새로 | 시안 L2056 `BEDS = 2`(가정) · SPEC-002 U-15 「침대 수 · (n/m) 없음」 |
| Q17 | 이름 누르기 → 고객 차트 | ⓐ 시안 그대로 「준비중입니다」 알림 ⓑ 누르는 동작 없음 | 시안 L2623 `CHART_READY = false` · L2624 |
| Q18 | 처방전 출력 | ⓐ 뺌 ⓑ 시안처럼 버튼 + 「아직 그리지 않았어요」 류 ⓒ KOS 웹 링크(cc `Settlement.links.prescription`) | 시안 L2363 = 「처방전 발급 화면은 아직 그리지 않았어요」 · DAY `prescription` 동기화 있음(`dev:backend/day/emr/sync_schedule_sales.py:71`) |
| Q19 | 이전 방문 범위 | ⓐ DAY DB 의 지난 방문(백필 · 동기화된 것만) ⓑ KOS `get-schedules-by-visitor` 를 열 때 읽음(cc 방식) | §5 · prod 백필 실행 여부 확인 안 됨 |
| Q20 | 동행 고르기 방식 | ⓐ 지금 구현(끌어 놓기)만 · 모달은 이름 · 이동만 ⓑ 시안처럼 모달 체크박스도 · 그때 조건 = 시안 「같은 열 · 같은 시각」 vs R71 「같은 30분 행」 | 시안 L2179 `x.at === r.at` · R66 · R71 · R73 |
| Q21 | 시술권 칸(시술만 진행) | ⓐ 뺌 ⓑ DAY 시술권 사본에서 잔여 · 회차(기간 · 마지막 사용은 원천 없음) | `dev:backend/day/models/ticket.py:69` — 만료 칸 없음 |

---

## 1. 칸 전수 표 — 시안에서 센 칸 **38개** = 표 38행

**센 방법**(시안 `detailV6Html` L2133 ~ 2251): `kv(` 고유 이름 **14** · `fld(` 고유 키 **4**(who · room · tix · order — 호출 7) · `noteSec(` **2** · `<dt>` **8** · `<th>` **2** · 그 밖 `m6-` 칸 **8**(`m6-head` 단계 · `m6-name` 이름 · `f-vbadge` 초진/재진 · `m6-kv is-memo` 예약메모(L2186 — `kv(` 를 안 거침) · `m6-pc-t` 총 수납 금액 · `m6-pch` 수납 머리 표시 · `m6-banner` 안내 띠 · `m6-pvc` 방문 날짜) = **38**. 판정 수 = 그대로 5(#2 · 3 · 11 · 13 · 14) · 일부만 6(#7 · 17 · 18 · 20 · 21 · 22) · 가공 20 · 없음 7(#4 · 8 · 9 · 10 · 25 · 26 · 37). `<h4>` 5개(이전 방문 기록 · 예약 정보 · 상담 정보/시술 정보 · 시술 목록 · 수납 정보)는 칸 묶음 제목이라 칸에 안 셈.

판정: **그대로** = DAY 칸 값을 바로 · **가공** = DAY 값을 조인 · 계산 · 문구로 바꿔야 · **없음** = DAY 에 원천 없음.
「차트」 = 시술현황 차트 모달에 이미 있나.

| # | 칸(시안 문구) · 시안 줄 | 보이는 단계(§4) | DAY DB 원천 | KOS 원천 | DAY 저장 | 차트 | 판정 |
|---|---|---|---|---|---|---|---|
| 1 | 머리 = 단계 이름(귀가면 「귀가 완료」) · 색 · L2249 · L2053 | 전부 | `visit.reservation_status` + `visit.flow_step`(SPEC-006 U-5 판정 · `dev:backend/day/enums/visit.py`) | 일정 `reservation.status` · `flowStep`(`mapper.py:570` · `:594`) | O | 없음 | 가공(시안 이름 · 「상담 진행」 · 「시술 진행」 · 「귀가 완료」) |
| 2 | 고객 이름(외국인 = 한글 발음 우선) · L2160 · L2171 | 전부 | `customer.name_pronunciation` / `customer.name` | 일정 `visitor.phoneticName` · `name`(`mapper.py:310`) | O | 있음 `board_chart_parts.html:61` | 그대로 |
| 3 | 초진 / 재진 배지 · L2161 | 전부 | `visit.is_new` | 일정 `visitor.isNew`(`mapper.py:602`) | O | 차트 JSON 에 없음(`presentation/board.py:397` customer 에 isNew 안 실음) | 그대로(null 처리 정할 것) |
| 4 | 성명(여권) · L2172 | 외국인만 | `customer.passport_surname` · `passport_given_names` 칸만 — **채우는 매퍼 없음**(`git grep passport_surname` 매퍼 0). 시안 값 = 영문 이름(`r.name`) → `customer.name` | KOS 고객 상세 `passportSurname`(cc `IdentityField`) | 칼럼만 · 값 확인 안 됨 | 없음 | 가공(`customer.name`) 또는 없음 — 정할 것 |
| 5 | 연락처(없으면 SNS) · L2172 | 전부 | `customer.phone_country_code` · `phone_number` / `sns_type` · `sns_account_id` | 일정 `visitor.phone` · `snsInfo`(`mapper.py:316` · `:320`) | O | 없음 | 가공(형식) |
| 6 | 생년월일/성별(만 나이) · L2172 | 전부 | `customer.birth_date` · `gender` | 일정 `visitor.dateOfBirth` · `gender` | O | 있음(성별 · 만 나이 `board_chart_parts.html:62`) | 가공(만 나이) |
| 7 | 국적/통역 · L2173 | 전부 | `customer.nationality` · 통역 = **없음**(`customer.language` 만 있음) | 일정 `visitor.nationality` | 국적 O | 국적 있음 | 국적 그대로 · 통역 없음(Q13) |
| 8 | 신분확인 · L2149 ~ 2152 | 전부(값 모양은 단계 · 국적 · 재진으로 갈림) | `identity_check` 테이블 **있으나 쓰는 · 읽는 코드 0**(`dev:backend/day/models/reception.py:52`) · 신분 번호 = `customer.registration_number` · `passport_number`(암호화 · KOS 키 보충 `mapper_kos_keys.py:454 ~ 456`) | 상태 API 없음(cc = 자체 기록 + KOS 고객 상세 신분 칸 채움 여부) | 기록 X · 번호 O | 없음 | 없음(Q4) |
| 9 | 초진 문진(O / 날짜 · 작성 필요 · 다시 받기) · L2153 | 전부 | `questionnaire_history` 테이블 **있으나 쓰는 · 읽는 코드 0**(`reception.py:85`) | `visitor/open/v1/queries/get-questionnaire-submit` · `get-visitor-questionnaire`(KOS 문서 L209 · L211) | X | 없음 | 없음(Q4) |
| 10 | 건강정보(확인 필요 n · 펼침 Q/A) · L2156 ~ 2158 | 전부 | 위와 같음 | 위와 같음(cc `Health` = 양식 「건강 정보」 쪽 질문 × 제출 답) | X | 없음 | 없음(Q4) |
| 11 | 특이사항 · L2173(`cu.caution` 있을 때만) | 전부 | 후보 `customer.customer_notes` · `customer.legacy_notes` | 일정 `visitor.memo`(`mapper.py:318`) · 고객 `migratedMemo`(`mapper_kos_keys.py:477`) | O | 없음 | 그대로 — 원천 정할 것(Q5) |
| 12 | 담당자(예약 담당) · L2189 | 전부 | `visit.reservation_assignee_id` → `staff.name` | 일정 `reservation.reservationAssignee`(`mapper.py:574`) | O(`sync_schedules.py:377`) | 없음 | 가공(이름 조인) |
| 13 | 예약 일시 · L2189 | 전부 | `visit.reserved_start_at` · `reserved_end_at` | `reservation.startDateTime` · `endDateTime` | O | 없음 | 그대로(시안은 끝 = 시작 + 30분 고정 L2189 — DAY 는 실제 끝) |
| 14 | 동행 · L2179 ~ 2184 | 전부(고치기 = 지난 날 · 취소 · 노쇼 아니면) | `companion_group` · `companion_member`(R65 · `dev:backend/day/models/companion.py`) | 없음(DAY 전용) | O | 없음 | 그대로 |
| 15 | 의사 지정(없으면 「지정 안 함」) · L2175 ~ 2177 | 전부(고치기 = 오늘 예약 · 접수) | `visit.requested_doctor_id`(후보 · Q6) | `reservation.doctor`(`mapper.py:581`) | O | 없음 | 가공(원장 이름 · 「원장」 붙임) |
| 16 | 유입채널 · L2189 | 전부 | `visit.funnel_id` → `funnel.name` · `visit.funnel_detail` | `reservation.funnel`(`mapper.py:583`) | O | 없음 | 가공(이름 조인) |
| 17 | 희망 시술/ 예산 · L2190 | 전부 | `visit_requested_procedure`(option_title · product_title · price_amount) · 예산 = **없음** | `reservation.requestedProcedures`(`mapper.py:540`) | 시술 O · 예산 X | 없음 | 시술 가공 · 예산 없음 |
| 18 | 예약메모(줄마다 「시각 · 작성자」) · L2185 ~ 2187 | 전부 | `visit.reservation_notes`(한 덩어리) · 작성자 · 시각 = **없음** | `reservation.reservationMemo`(`mapper.py:573`) | 본문 O | 없음 | 본문 그대로 · 작성자/시각 없음(Q12) |
| 19 | 상담사(상담 정보) · L2203 | 취소 · 노쇼 아님 · 시술만이 아닐 때 | R48 = `consultation.counselor_id`(시작 순 첫 줄) → `visit.consultation_info_counselor_id` · 후보 `visit.requested_counselor_id` | 일정 `consultations[].counselors`(`mapper.py:510`) · 상담 정보 counselor(`mapper_kos_keys.py:301`) · `reservation.counselor` | O | 없음(판 카드엔 `counselors` `board_parts.html:183`) | 가공(Q7) |
| 20 | 관리실 선택 · L2203 ~ 2205 | 취소 · 노쇼 아님 | `visit.room_id` → `room`(판 카드 방 규칙 SPEC-002 ⑰) · 정원 = **없음** | 작업 `room`(`mapper.py` `card_room`) | O | 차트 없음(판 카드 `CardViewData.room`) | 이름 그대로 · 정원 없음(Q16) |
| 21 | 시술권(시술만 · 오늘 접수 전) · L2198 ~ 2200 · L2204 | 오늘 예약 · 접수 ∧ 시술만 ∧ 쓸 수 있는 시술권 | `ticket_bundle` · `ticket_set` · `ticket`(잔여 = 상태별 수) · 기간 · 마지막 사용 = **없음**(`ticket.py:69` 만료 칸 없음) | 시술권 조회(동기화 `sync_tickets.py`) | O(기간 X) | 없음 | 가공 · 기간 없음(Q21) |
| 22 | 오더 메모(+ 작성자 · 시각) · L2201 ~ 2205 | 취소 · 노쇼 아님 ∧ 시술만 | `visit.procedure_order_note` · 작성자 · 시각 = **없음** | 일정 `orderMemo`(`mapper.py:603`) | 본문 O | 판 카드에 있음 `board_parts.html:183` · 차트 없음 | 본문 그대로 · 작성자/시각 없음 |
| 23 | 시술 목록 · 상품명(상품 → 구성) · L2216 ~ 2218 | 전부(시술 대기 ~ 귀가만 줄 · 그 전 = 「추가된 시술이 없습니다.」) | `purchase_item`(title · product_title) → `purchase_item_composition` 또는 `visit_task`(title) | 구매 · 일정 tasks | O | 시술 줄 이름 있음(`board_chart_parts.html:43`) | 가공(Q11) |
| 24 | 시술 목록 · 상태 「진행 / 미진행」 · L2215 | 위와 같음 | `visit_task.status`(`enums/task.py:9`) · 오늘 작업 있음/없음 | tasks | O | 없음 | 가공(규칙 정할 것 Q10) |
| 25 | 시술메모 · L2227(`s.early`) | 사유가 있을 때 | **없음** | 없음 | X | 없음 | 없음(Q14) |
| 26 | 귀가 사유 · L2227(`s.homeWhy`) | 사유가 있을 때 | **없음** | 없음 | X | 없음 | 없음(Q14) |
| 27 | 상품 합계 · L2223 | 전부(상담 끝나기 전 = 0 원) | 구매 항목 금액(정의 없음 · Q8) | 구매 | O | 없음 | 가공 — 정의 정할 것 |
| 28 | 할인 금액 · L2223 | 전부 | `purchase_item.adjusted_amount` · `purchase_price_adjustment`(정의 없음) | 구매 | O | 없음 | 가공 — 정의 정할 것 |
| 29 | 총 수납 금액 · L2224 | 전부 | R51 결제총액(`dev:backend/day/policies/reservation_amounts.py:69`) | 구매 · 거래 · 작업 수납필요 | O | 없음 | 가공 — R51 그대로 쓸 수 있음 |
| 30 | 수납 완료 · L2225 | 전부 | R49 수납 | 위와 같음 | O | 없음 | 가공 — R49 |
| 31 | 수납 필요 · L2225 | 전부(시술 대기 전 = 0) | R50 미수 | 위와 같음 | O | 없음 | 가공 — R50 |
| 32 | 수납 머리 「수납되지 않은 금액이 있습니다」 / 「수납 완료」 배지 · L2221 ~ 2222 | 경고 = 귀가 대기 · 귀가 / 배지 = 미수 없음 ∧ 총액 > 0 | R42 `visit_task.payment_required` · R50 | 작업 수납필요 | O | 판 카드 「수납 필요」 `board_parts.html:143` | 가공(단계 조건 Q9) |
| 33 | 이전 방문 카드 날짜 · L2166 | 재진만 | 같은 고객 지난 `visit.reserved_start_at` | 일정(백필) | O(백필 범위) | 없음 | 가공 |
| 34 | 이전 방문 · 예약 담당 · L2167 | 재진만 | 그 방문 `reservation_assignee_id` | 위와 같음 | O | 없음 | 가공 |
| 35 | 이전 방문 · 상담(「○○ 실장, ○○ 원장」) · L2167 | 재진만 | 그 방문 `consultation.counselor_id` · `doctor_id`(KOS 둘 이상이면 비움 `mapper.py:496`) | 일정 consultations | O(한 명일 때만) | 없음 | 가공 |
| 36 | 이전 방문 · 시술(원장) · L2167 | 재진만 | 그 방문 작업 집도의 `visit_task_staff.role = doctor` | tasks doctors | O | 없음 | 가공 |
| 37 | 안내 띠 「시술 없이 바로 귀가하는 고객입니다.」 / 「시술 없이 귀가한 고객입니다.」 · L2229 | 시술 대기 ~ 귀가 ∧ 상담만 | **판정 원천 없음** | 없음 | X | 없음 | 없음(Q15) |
| 38 | 이전 방문 · 받은 시술 · L2167 | 재진만 | 그 방문 살아 있는 `visit_task.title`(「방 배정」 · 취소 뺌) | tasks | O | 시술 줄 이름(오늘 방문만) | 가공(시안은 방문마다 1 ~ 3개 가짜) |

---

## 2. 버튼 · 동작 전수 표 — **51행**

**센 방법**: 시안 파일 전체 `data-s5="…"` 정적 고유 값 29 + 동적(`M(` 의 `cancel` · `recv` · `rx` · `cbox(` 의 `id-toggle` · `only-toggle` · `s5Combo` 의 `${kind}` = `who` · `room`) 7 = **모달 동작 36**. 입력(`data-s6-doc` select · `data-s5-f` 오더 메모 글 칸 · `data-s5-why` 귀가 사유 글 칸) **3**. 흉내 막대 `mimicBtns` **7**(L2255 ~ 2264). 우클릭 `data-ctx` 고유 **5**(L2894 ~ 2921). 36 + 3 + 7 + 5 = **51**.
(`data-s6-memo` · `memo-add` · `memo-save` · `memo-cancel` · `memo-more` · `form` · `mode` · `tix` · `c-to-proc` · `to-proc` · `c-save` · `c-sign` · `id-ok` = 처리기만 있고 v9 모달에 그려지는 버튼 없음 — 세지 않음. 「예약메모 덧붙이기」는 v9 에서 버튼이 사라졌다.)

### 2-1. 모달 동작 36 + 입력 3

| # | 동작(시안 문구) · 시안 줄 | 보이는 단계 | 바뀌는 것 | KOS 쓰기 | DAY 에 있는 경로 |
|---|---|---|---|---|---|
| 1 | `close` 닫기 ✕ · 바깥 · L2249 · L2296 | 전부 | 화면만 | — | 없음(화면) |
| 2 | `chart` 이름 → 고객 차트 · L2171 · L2330 | 전부 | 「준비중입니다」(L2624) | — | 없음 |
| 3 | `qr-menu` [문진 QR] · L2146 | 오늘 예약 · 접수 ∧ 문진 안 함 ∧ live | 메뉴 열림 | — | 없음 |
| 4 | `survey` 태블릿에 / 모바일로 띄우기 · L2146 · L2339 | 위와 같음 | 문진 「표시 중」 → 끝나면 자동 채움 · **신분 또는 문진 끝 = 접수로 바뀜**(L2332 `arrive`) | 문진 제출 = `visitor/open/v1/commands/submit-visitor-questionnaire`(cc `procedure/back/app/service/questionnaire.py:35`) · 접수 = 아래 #30 | `display_request` 테이블만(쓰는 코드 0) · 앱 경로 없음(`routers/api/` 에 접수 · 문진 없음) |
| 5 | `scan` [여권 스캔] · L2148 · L2334 | 외국인 ∧ 1년 안 재진 아님 ∧ 오늘 예약 · 접수 ∧ 미확인 | 「코디 휴대폰에서 스캔 중」 → 저장 · 접수로 | 신분증 사진 KOS 올리기(cc `id_photo.py:34` 근처 · 경로 확인 안 됨) · 접수 | 없음(`id_photo` 테이블만) |
| 6 | `scan-cancel` 취소 · L2151 | 스캔 중 | 스캔 그만 | — | 없음 |
| 7 | `id-toggle` 「신분증 확인」 체크 · L2152 · L2335 | 내국인 ∧ 오늘 예약 · 접수 ∧ live | 신분 확인 표시 · 체크 = 접수로 / 풀면 예약으로 되돌림 | 신분 기록 KOS 없음(cc = 자체 기록) · 접수 #30 | 없음(`identity_check` 만) |
| 8 | `hv` 건강정보 펼침 · L2157 | 문진 있음 ∧ 확인 필요 있음 | 화면만 | — | 없음 |
| 9 | `pv` 이전 방문 카드 펼침 · L2166 | 재진 | 화면만 | — | 없음 |
| 10 | `pv-toggle` 이전 방문 접기 · 펼치기 · L2170 | 재진 | 화면만(창 닫아도 유지) | — | 없음 |
| 11 | `change` [예약 변경] · L2188 · L2354 | 예약 ∧ 지난 날 아님 | 예약 등록 창 고치기 모드(`openBook({edit})` L2440) | `schedule/open/v2/commands/update-reservation`(KOS 문서 L170) · cc 내부 `schedule/reservation/v2/commands/update-reservation`(cc `service/reservations.py:85`) | 없음 |
| 12 | `grp-edit` 「+ 동행 추가」 / [수정] · L2183 ~ 2184 | 지난 날 · 취소 · 노쇼 아님 | 체크 목록 열림 | — | 동행 쓰기 있음(#14) |
| 13 | `grp-pick` 동행 체크 · L2180 | 위와 같음 | 고름(묶음 전체 함께) | — | — |
| 14 | `grp-save` [저장] · L2182 · L2303 | 위와 같음 | 새 묶음 · 남은 1명 풀림 | 없음(DAY 전용 R65) | **있음** `PUT /reservations/companions` · `/leave`(`dev:backend/day/routers/reservations.py:167` · `:187`) — 단 1:1 끌어 놓기 계약(묶음 통째 저장 아님) |
| 15 | `grp-cancel` [취소] · L2182 | 위와 같음 | 화면만 | — | — |
| 16 | `grp-go` 동행 이름 → 그 예약 상세 · L2183 | 동행 있음 | 다른 방문 모달 | — | 없음(화면) |
| 17 | `doc-edit` 의사 지정 누름 · L2177 | 오늘 예약 · 접수 ∧ live | 고르기 목록 | — | — |
| 18 | `data-s6-doc` 의사 고름 · L2176 · L2382 | 위와 같음 | 의사 지정 바꿈 | `update-reservation`(예약 묶음 doctors · cc) — 확인 안 됨 | 없음 |
| 19 | `only-toggle` 「시술만 진행」 체크 · L2206 · L2324 | 오늘 예약 · 접수 ∧ live | 상담 정보 → 시술 정보 · 초진이면 확인 창 | (접수 때 진행 경로로 반영) | 없음 |
| 20 | `only-new-ok` 초진 확인 창 [진행] · L2273 | 초진에서 #19 | 위와 같음 | — | — |
| 21 | `dd` 콤보 열기(상담사 · 관리실) · L2118 | live | 목록(검색) | — | — |
| 22 | `who` 상담사 고름 · L2120 · L2345 | live ∧ 상담 | 상담사 · 상담 대기면 바로 바뀜 | 상담사 = `schedule/open/v1/commands/update-schedule-consultation-info`(상담 정보 counselor — 본문 확인 안 됨) 또는 접수 묶음 | 없음 |
| 23 | `room` 관리실 고름 · L2120 · L2341 | live | 관리실 · 상담 대기면 바로 바뀜 | `schedule/flow/v1/commands/change-tasks-room`(접수 땐 「방 배정」 `add-flow-tasks` — cc `reception.py:36 ~ 37`) | 시술 현황 방 이동 있음 `POST /board/visits/{id}/room-move`(`dev:backend/day/routers/board.py:522`) — 오늘 판 카드만 |
| 24 | `tix-use` [시술권 사용] · L2200 | 오늘 예약 · 접수 ∧ 시술만 | 회차 +1 표시 | 시술권 작업 넣기(`add-flow-tasks` ticket — 확인 안 됨) | 없음 |
| 25 | `tix-undo` [사용 취소] · L2200 | 위와 같음 | 되돌림 | — | 없음 |
| 26 | `order-edit` 오더 메모 [수정] · L2205 | live ∧ 시술만 ∧ 접수 뒤 | 글 칸 열림 | — | — |
| 27 | `order-save` [저장] · L2201 · L2366 | 위와 같음 | 오더 메모 · 작성자 · 시각 | `schedule/v1/commands/change-order-memo`(`dev:backend/day/emr/kos/ext_reads.py:261` — 외부 연동 워커 전용 · 시스템 계정) | 웹 경로 없음(ext 만) |
| 28 | `order-cancel` [취소] · L2201 | 위와 같음 | 화면만 | — | — |
| 29 | `cancel` [예약 취소] · L2235 → 확인 창 L2282 | 예약 ∧ 지난 날 아님 | 확인 창 | — | — |
| 30 | `recv` [접수] · L2235 · L2353 | **오늘** 예약 | 접수 | `schedule/v1/commands/recept`(cc `reception.py:35`) | 없음 |
| 31 | `assign` [상담 대기] / [시술 대기] · L2236 · L2348 | 접수(빠진 칸 있으면 회색 · 누르면 깜빡임) | 방 · 상담사 · 단계(상담 대기 / 시술 대기) | `add-flow-tasks`(방 배정) → `change-tasks-room` → `change-flow-step`(cc `reception.py:36 ~ 39`) | 단계 쓰기 일부 있음(`FlowStepWriteData` `dev:backend/day/dtos/emr_writes.py:52` · KOS 경로 `writes.py:51`) — 접수 단계용 서비스 없음 |
| 32 | `home` [귀가 처리] · L2237 · L2243 → 확인 창 | 오늘 상담 대기 · 상담 진행 / 오늘 시술 대기 · 시술 진행 · 귀가 대기 | 확인 창(귀가 대기 전이면 사유 필수 · 미수 있으면 경고) | — | — |
| 33 | `home-ok` 확인 창 [귀가] / [귀가 처리] · L2276 ~ 2281 · L2359 | 위와 같음 | **귀가(완료)** | `change-flow-step` `COMPLETED` — DAY 는 이 값을 **막는다**(`dev:backend/day/emr/kos/writes.py:75` 「step = COMPLETED 는 막는다」) | 시술 현황 [귀가 대기](= `procedure_done`) 만 있음 `POST /board/visits/{id}/home`(`board.py:579` · `services/board_tasks.py:222`) — 「귀가 완료」 경로 없음 |
| 34 | `pop-close` 확인 창 [취소] / [닫기] · L2273 ~ 2282 | 확인 창 | 화면만 | — | — |
| 35 | `rx` [처방전 출력] · L2239 · L2363 | 오늘 귀가 대기 · 귀가 | 「처방전 발급 화면은 아직 그리지 않았어요」 | 확인 안 됨 | 없음(`prescription` 동기화만) |
| 36 | `pay` [n원 수납] / [시술권 정산] → [KOS에서 수납 중] · L2241 · L2360 | 오늘 시술 대기 · 시술 진행 · 귀가 대기 ∧ 미수 | 「KOS 수납 화면에 항목과 금액을 넣어 두었어요」 | 수납 창에 항목 넣기 — **KOS 경로 확인 안 됨**(공개 문서에 수납 생성 command 없음 · 조사 `research-payment-1` 은 읽기만) | 없음 |
| 37 | 입력 `data-s6-doc`(#18 의 select) | — | — | — | — |
| 38 | 입력 `data-s5-f="order"` 오더 메모 글 칸(접수 전 시술만 · L2204) | 오늘 예약 · 접수 ∧ 시술만 | 오더 메모(접수 때 같이) | `change-order-memo` | 없음 |
| 39 | 입력 `data-s5-why` 귀가 사유 글 칸 · L2277 | 귀가 대기 전 귀가 | 사유(필수) | 없음(KOS 칸 확인 안 됨) | 없음 |

### 2-2. 「다른 화면에서 일어나는 일」 흉내 막대 7 — **DAY 화면 동작 아님**(표시만)

L2255 ~ 2264 · 오늘 방문만: `c-start` 상담 시작 · `c-done` 상담 완료 (시술 진행) · `c-home` 상담 완료 (바로 귀가) · `p-start` 시술 현황 · 첫 시술 시작 · `p-done` 시술 현황 · 귀가 대기 · `p-early` 시술 현황 · 덜 끝난 채 귀가 대기(사유) · `kos-paid` KOS · 수납 완료. 참고: `p-start` · `p-done` 은 DAY 시술 현황에 실제 경로가 있다(시작 `POST /board/tasks/{id}/{action}` `board.py:563` · 귀가 대기 `board.py:579`). `p-early` 의 「사유」는 DAY 시술 현황에 없다.

### 2-3. 우클릭 메뉴 5(§6)

| # | 동작 · 시안 줄 | 켜짐 조건(L2898) | 바뀌는 것 | KOS 쓰기 | DAY 경로 |
|---|---|---|---|---|---|
| 47 | `move` 예약 변경 = 끌어 옮김 · L2913 · L2932 ~ 2940 | `r.st === '예약' && r.day >= 0` | 열 · 30분 칸 바뀜 · 동행에서 빠짐 | `update-reservation`(v2) 또는 `reschedule-by-time-slot`(KOS 문서 L147) | 없음(DAY 끌기는 동행 묶기 전용) |
| 48 | `cancel` 예약 취소 · L2914 | 위와 같음 | 확인 창 | — | — |
| 49 | `cancel-ok` 확인 창 [예약 취소] · L2916 | 확인 창 | 취소 · 동행에서 빠짐 | `schedule/open/v1/commands/cancel-reservation`(KOS 문서 L144 · cc `service/reservations.py:86`) | 없음 |
| 50 | `cancel-no` 확인 창 [닫기] · 바깥 · L2915 | 확인 창 | 화면만 | — | — |
| 51 | `grp` 동행 추가 · L2917 | `r.st !== '취소' && r.day >= 0` | 모달을 열고 동행 고르기(#12)를 켬 | 없음 | 동행 쓰기 있음(#14) |

---

## 3. 시술현황 차트 모달과 비교

### 3-1. 차트 모달 구성

| 항목 | 내용 · 근거 |
|---|---|
| 여는 경로 | `GET /board/visits/{visit_id}/chart?sec=` (HTMX 만 · 아니면 `/board` 로) `dev:backend/day/routers/board.py:289` · 판 카드 시술명 영역 · 「시술 완료」 탭 시술 줄(`board_parts.html:88` · `:262`) · SPEC-002 U-14 |
| 열리는 방문 | `is_chartable` = 오늘 판 카드 ∨ 「시술 완료」 탭 단계(`dev:backend/day/presentation/board.py:383`) — 그 밖 404 |
| 권한 | 보기 = `board` view(`board.py:303`) · 쓰기 칸 = `board` edit 또는 전체 권한(`board.py:318 _can_edit`) |
| JSON 모양 | `ChartResponseData{visitId, visitDate, customer{name, phoneticName, gender, birthDate, nationality}, firstTab, tasks[{id, title, assignee, doctor}], staffOptions{assignee[], doctor[]}}` · 칸 = `{body, staffId, author, savedAt, logId}`(`dev:backend/day/dtos/board_views.py:190 ~ 227` · 만드는 곳 `presentation/board.py:387`) |
| 칸 | 머리 = 이름 · 발음 / 성별 · 만 나이 · 국적 · 「최근 저장 : HH:MM」 · 탭 [간호관리차트 \| 의사차트] · 표 「시술명 · 담당자 · 차트 내용」 시술마다 한 행(`board_chart_parts.html:55 ~ 79`) |
| 버튼 · 동작 | 닫기 · 탭 · 담당자 고르기(`ui.staff_picker`) · 글 자동 저장(칸 나갈 때 + 2초) · 다시 시도 — `POST /board/tasks/{task_id}/chart`(`board.py:433`) → 이력 1행 + `assignee_note` / `doctor_note` + KOS `change-flow-tasks-assignee-memo` · `doctor-memo` · 집도의 바뀌면 `change-tasks-doctors`(`services/board_charts.py:54 ~ 183`) · 409 충돌 토스트 |
| 조각 | `partials/board_chart.html`(4줄 — 매크로 호출만) · `board_chart_parts.html`(`row` · `modal` · `saved_at`) · `board_chart_saved.html`(저장 응답 OOB) |

### 3-2. ⓐ 같은 것 · ⓑ 차트에만 · ⓒ 새 모달에만

| 구분 | 항목 |
|---|---|
| ⓐ 같은 것 | 고객 이름 · 한글 발음 · 성별 · 만 나이 · 국적(차트 머리 = 새 모달 고객 정보 #2 · #6 · #7 일부) · 시술 줄 목록 원천(`visit_task` · 「방 배정」 · 취소 뺌 — 새 모달 시술 목록을 작업 단위로 할 때만 · Q11) · 가운데 모달 + 닫기 |
| ⓑ 차트에만 | 간호관리차트 · 의사차트 탭 · 시술마다 담당자 고르기 · 차트 글 자동 저장 · 이력 · 충돌 처리 · 「최근 저장」 · KOS 메모 쓰기 |
| ⓒ 새 모달에만 | 머리 단계 이름 · 색 · 초진/재진 · 연락처 · 성명(여권) · 신분확인 · 문진 · 건강정보 · 특이사항 · 예약 정보 7칸 · 상담 정보(상담사 · 관리실 · 시술권 · 오더 메모) · 시술 목록 상품 → 구성 · 진행/미진행 · 시술메모 · 귀가 사유 · 수납 정보 5숫자 · 이전 방문 기록 · 안내 띠 · 단계별 아래 버튼 · 확인 창 |

### 3-3. 재사용 근거(설계 결정 아님)

- **차트 JSON 그대로는 못 씀**: 열림 조건이 `is_chartable`(오늘 판 · 시술 완료 탭)이라 예약 · 앞날 · 지난 날 · 취소 방문은 404(`presentation/board.py:383` · `services/board_charts.py:43`). 판 세계(`load_world` — 오늘 판 한 병원)를 읽어 만든다(`services/board_charts.py:178`).
- **머리 매크로는 쓸 수 있음**: `ui.customer_line` · `ui.vital`(`board_chart_parts.html:61 ~ 62`)은 값만 받는 매크로다.
- **조각 구조**: `board_chart.html` 은 `charts.modal(...)` 한 줄이라 새 모달이 같은 파일을 늘리면 차트 JSON 계약(`SPEC-002 개정 ⑯`)을 건드린다. 예약 쪽 조각은 `reservations_*.html` 규칙(AGENTS.md 「기능 하나를 고치면 같은 파일 이름」).
- **시술 목록 → 차트 열기**(Q2 ⓒ): 새 모달 시술 줄에서 `GET /board/visits/{id}/chart` 를 부르면 오늘 판 방문만 열린다 — 다른 날엔 404.
- 수납 숫자는 차트가 아니라 원내 현황 금액(`policies/reservation_amounts.py` · `queries/reservation_inhouse.py`)을 다시 쓸 수 있다(R49 ~ R55).

---

## 4. 단계 경계 — 시안 조건식 그대로

정의(L2135 ~ 2138): `today = r.day === 0` · `past = r.day < 0` · (앞날 = `r.day > 0`) · `recvArea = today && ['예약','접수'].includes(st)` · `live = !['귀가','예약 취소','노쇼'].includes(st) && !past` · `cut = ['예약 취소','노쇼'].includes(st)` · `wide = ['시술 대기','시술 진행','귀가 대기','귀가'].includes(st)`
단계 이름 `S5`(L2053 ~ 2054): 예약 · 예약 취소 · 귀가 · 귀가 대기 · 상담 진행 · 시술 대기 / 시술 진행 · 상담 대기 · 접수 — **노쇼는 만들지 않음**.

| 요소 | 조건식(시안) | 줄 |
|---|---|---|
| 머리 글자 | `st === '귀가' ? '귀가 완료' : st` · 색 `S5_C[st]` | L2249 |
| [문진 QR] | `live && recvArea && d.health === 'none'` | L2146 |
| [여권 스캔] | `foreign && !kept && recvArea && live && s.id === 'idle'`(`kept = 재진 && !d.fresh` = 1년 안 재진) | L2147 ~ 2148 |
| 신분확인 값 | `kept` → 「생략 (1년 이내)」 / 외국인 → 「여권 저장됨 · 번호」 · 스캔 중 · 「미확인」 / 내국인 ∧ `recvArea && live` → 체크 / 그 밖 → 「O」 · 「미확인」 | L2149 ~ 2152 |
| 초진 문진 값 | 작성 중 · `O / 날짜` · 오래된 재진 「다시 받기」 · 「작성 필요」 | L2153 |
| 건강정보 | 문진 전 「문진 전」 · 없음 「특이사항 없음」 · 있음 「확인 필요 n」 | L2156 |
| 성명(여권) | `foreign` | L2172 |
| 특이사항 | `cu.caution` 있을 때 | L2173 |
| 이전 방문 기록 | `r.visit === '재진'` | L2163 |
| [예약 변경] | `st === '예약' && !past` | L2188 |
| 동행 고치기 | `canEdit = !past && !cut` · 같은 시각 후보 `x.day === r.day && x.track === r.track && x.at === r.at && x.st !== '취소'` | L2179 |
| 의사 지정 고치기 | `recvArea && live` | L2177 |
| 상담 정보 묶음 | `!cut` · 제목 = 시술만이면 「시술 정보」 | L2206 |
| [시술만 진행] 체크 | `recvArea && live` | L2206 |
| 상담 정보 몸 | `!only` → 상담사 + 관리실 / `only && recvArea` → 시술권(쓸 수 있을 때) + 관리실 + 오더 메모 글 칸 / `only && !recvArea` → 관리실 + 오더 메모(보기 · `live` 면 [수정]) | L2203 ~ 2205 |
| 콤보 고르기 | `live` 면 고르기 · 아니면 잠긴 칸 | L2196 |
| 시술 목록 줄 · 수납 숫자 | `wide` 일 때만 값 · 아니면 「추가된 시술이 없습니다.」 · 0 원 | L2209 · L2210 · L2216 |
| 시술메모 · 귀가 사유 | `s.early` · `s.homeWhy` 있을 때 | L2227 |
| 수납 경고 / 「수납 완료」 | 경고 `need && ['귀가 대기','귀가']` · 배지 `!need && payT > 0` | L2221 |
| 수납 필요 숫자 | `wide ? max(0, owe) : 0` | L2225 |
| 안내 띠 | `wide && s.consultOnly` | L2229 |
| 아래 버튼 전체 | `!past && !cut` (지난 날 · 취소 · 노쇼 = 버튼 없음) | L2234 |
| 예약 | [예약 취소] + `today` 면 [접수] (앞날 = [예약 취소]만) | L2235 |
| 접수 | [상담 대기] / [시술 대기](빠진 칸 있으면 회색) | L2236 |
| 상담 대기 · 상담 진행 | `today` 면 [귀가 처리] | L2237 |
| 시술 대기 ~ 귀가 | `wide && today` — 귀가 대기 · 귀가 = 왼쪽 [처방전 출력] · `st !== '귀가'` 면 수납 버튼(미수 있을 때) + [귀가 처리] | L2238 ~ 2244 |
| 귀가 확인 창 | 귀가 대기 전 = 사유 필수 / 미수 있음 = 경고 / 그 밖 = 단순 | L2274 ~ 2281 |
| 우클릭 | 예약 변경 · 취소 = `r.st === '예약' && r.day >= 0` · 동행 추가 = `r.st !== '취소' && r.day >= 0` | L2898 |
| 흉내 막대 | `r.day === 0` 만 | L2256 |

---

## 5. 이전 방문 기록

- **DAY 에서 읽을 수 있나**: 있다. 같은 `customer_id` 의 지난 `visit`(`reserved_start_at` < 이번) — 화면용 조회는 아직 없다(`queries/` 에 고객별 방문 목록 없음 · 시술 현황 고객 검색은 「시술 완료」 탭 오늘 고객만 SPEC-002 U-13).
- **어디까지 과거**: 백필 = 수동 `python -m runtime.backfill --from YYYY-MM` · 어제까지 · 오늘 거부(`dev:backend/day/services/emr_backfill.py:1 ~ 17` · `month_windows` `:171`). 데모 dev 는 `--from 2026-08`(데모 데이터 8월부터) 로 11-19 실행 · 방문 1,319(`_archive/day/customer-erd/_RESUME.md:4` · `be-3-report.md:105`). **prod 백필은 실행했는지 확인 안 됨**(customer-erd `_RESUME.md:5` 는 「prod = 11-20 병원 마감 뒤」 계획까지만).
- 지난 방문의 칸은 일정 동기화와 같은 반영 함수라 현재 방문과 같은 칸이 찬다(`emr_backfill.py:6`).

| 시안 줄 | 원천 | 판정 |
|---|---|---|
| 날짜 | `visit.reserved_start_at`(현지 날짜) | 가공 |
| 예약 담당 | 그 방문 `visit.reservation_assignee_id` → `staff.name` | 가공 |
| 상담(「○○ 실장, ○○ 원장」) | 그 방문 `consultation.counselor_id` · `consultation.doctor_id`(KOS 에 둘 이상이면 비움 `mapper.py:496`) → 없으면 `visit.consultation_info_counselor_id` · `consultation_info_doctor_id` | 가공 · 비는 경우 있음 |
| 시술(원장) | 그 방문 작업 `visit_task_staff.role = doctor`(집도의) | 가공 |
| 받은 시술 | 그 방문 살아 있는 `visit_task.title`(「방 배정」 · 취소 뺌) | 가공 |
| (cc 비교) | cc 는 KOS `schedule/open/v1/queries/get-schedules-by-visitor` 를 열 때 읽음 · 같은 날 뺌 · 최신 순(cc `schemas/reservations.py` `PreviousVisit`) | — |

시안 대상 = `r.visit === '재진'`(L2163). 취소 · 노쇼 방문을 넣을지는 시안이 말하지 않음(가짜 `pastVisits` L2605 는 늘 「시술 진행」).

---

## 6. 우클릭 메뉴

| 메뉴 | 시안 | KOS 쓰기 | DAY 경로 |
|---|---|---|---|
| 예약 변경 | 카드가 점선(`is-moving`) → 끌어 다른 열 · 30분 칸에 놓음 · 미리보기 카드 · 동행이면 빠짐(L2913 · L2924 ~ 2940) | 공개 `schedule/open/v2/commands/update-reservation`(현행) · `reschedule-by-time-slot`(현행) · 옛 `v1 update-reservation`(deprecated)(KOS 문서 L147 · L152 · L170) · cc 는 내부 `schedule/reservation/v2/commands/update-reservation`(cc `service/reservations.py:85` · 라우터 `POST /reservations/{id}/move` cc `api/reservations.py:263`) | **없음** |
| 예약 취소 | 확인 창 「○○ HH:MM 예약을 취소할까요?」 · 「취소한 예약은 시간표에 회색으로 남아요.」 → 취소 · 동행 빠짐(L2896 · L2916) | `schedule/open/v1/commands/cancel-reservation`(KOS 문서 L144 · cc `service/reservations.py:86` · `POST /reservations/{id}/cancel` cc `api/reservations.py:293`) | **없음** |
| 동행 추가 | 모달을 열고 「동행」 칸 체크 목록을 켬 → 같은 열 · **같은 시작 시각**(`x.at === r.at`) 예약 중 체크 · 이미 묶인 사람을 고르면 그 묶음 전체 · [저장] = 고른 사람 + 나 = 새 묶음(L2917 · L2179 · L2300 ~ 2308) | 없음 | 지금 구현 = 카드를 **다른 카드 위에 끌어 놓기**(1:1 · 이미 다른 그룹이면 옮김) · 조건 = 같은 열 ∧ **같은 30분 행**(R66 · R71) · 풀기 = 띠 밖 빈 곳(R66) · `PUT /reservations/companions` · `/leave`(`routers/reservations.py:167` · `:187`) |

동행 차이: ① 입구(모달 체크 vs 끌어 놓기) ② 조건(같은 시작 시각 vs 같은 30분 행) ③ 저장 단위(묶음 통째 다시 짓기 vs 한 명씩 옮김) ④ 시안은 「예약 변경으로 옮기면 동행에서 빠짐」(L2939 `leaveGrp`) — DAY 는 KOS 에서 시간 · 그룹이 바뀌어 조건이 깨지면 빠짐(R67).

---

## 7. 로컬 데모 DB 표본 — 확인 못 함

- 접속법: README — PostgreSQL `127.0.0.1:11042` · 사용자 · 비밀번호는 `deploy/local.env` 에서(`dev:README.md:18` · `deploy/compose.local.yaml:63 ~ 65`). 브리프 §5 가 `*.env` 읽기와 로컬 docker 손대기를 막아 접속하지 않았다.
- 대신 §1 「DAY 저장」 칸 = 코드상 동기화 여부. 실제 채움(특히 `customer.customer_notes` · `visit.requested_doctor_id` · `visit.funnel_id` · `consultation.*` · `visit_requested_procedure`)은 표본으로 다시 볼 것 — 코디가 SELECT 권한을 주면 단계별 방문 하나씩 O / 빈칸으로 채울 수 있다.

---

## 8. 빠진 것 — 새로 필요한 것

| 무엇 | 칸 · 동작 | 필요한 것 | KOS API(근거) |
|---|---|---|---|
| 문진 · 건강정보 읽기 | #9 · #10 | 새 KOS 읽기 + (선택) `questionnaire_history` 채움 | `visitor/open/v1/queries/get-questionnaire-submit` · `get-visitor-questionnaire`(KOS 문서 L209 · L211 · cc `PATH_Q_FORM` · `PATH_Q_SUBMIT`) |
| 문진 띄우기 · 제출 | 동작 #3 · #4 | 띄우기 요청(`display_request` 쓰기) · 고객 화면 · 제출 | `visitor/open/v1/commands/submit-visitor-questionnaire`(cc `questionnaire.py:35`) |
| 신분확인 | #8 · 동작 #5 · #7 | `identity_check` 쓰기 경로(웹 · 앱) · 신분 칸 채움 여부 읽기 | 고객 상세 `visitor/v2/queries/get-visitor`(cc `PATH_VISITOR` — 내부) · 사진 올리기 경로 확인 안 됨 |
| 성명(여권) | #4 | `passport_surname` 매퍼 | 고객 상세(`get-visitor`) |
| 통역 여부 | #7 | 판정 원천 | 확인 안 됨 |
| 예산 | #17 | 원천 | 확인 안 됨 |
| 예약메모 작성자 · 시각 · 덧붙이기 | #18 | DAY 메모 기록 · KOS 메모 쓰기 | `schedule/open/v1/commands/change-reservation-memo`(cc `PATH_MEMO`) |
| 오더 메모 작성자 · 시각 · 쓰기 | #22 · 동작 #27 · #38 | 웹 쓰기 경로(지금은 ext 워커만) | `schedule/v1/commands/change-order-memo`(`ext_reads.py:261`) |
| 상담사 지정 | 동작 #22 | 쓰기 | `schedule/open/v1/commands/update-schedule-consultation-info`(본문 counselor 확인 안 됨) |
| 시술권 기간 · 마지막 사용 | #21 | `ticket` 만료 칸 · 사용 이력 | 시술권 조회 응답 칸 확인 안 됨 |
| 관리실 정원 | #20 | 침대 수 | 확인 안 됨 |
| 시술메모 · 귀가 사유 | #25 · #26 · 입력 #39 | DAY 새 기록 | 없음(DAY 전용) |
| 안내 띠 판정 | #37 | 규칙 | — |
| 접수 | 동작 #30 · #4 · #5 · #7 | 웹 접수 경로 · 쓰기 큐 | `schedule/v1/commands/recept`(cc `reception.py:35`) |
| 상담 대기 / 시술 대기 배정 | 동작 #31 | 방 배정 작업 · 방 · 단계 | `schedule/v1/commands/add-flow-tasks` · `schedule/flow/v1/commands/change-tasks-room` · `schedule/v1/commands/change-flow-step`(cc `reception.py:36 ~ 38` · DAY `writes.py:47 ~ 54` 에 경로 상수 있음) |
| 귀가(완료) | 동작 #33 | `COMPLETED` 쓰기 허용(지금은 막음 `writes.py:75`) | `change-flow-step` step `COMPLETED` |
| 예약 취소 | 동작 #29 · #49 | 쓰기 | `schedule/open/v1/commands/cancel-reservation` |
| 예약 변경 | 동작 #11 · #47 | 쓰기(예약 등록 창 포함) | `schedule/open/v2/commands/update-reservation` · `reschedule-by-time-slot` |
| 의사 지정 바꾸기 | 동작 #18 | 쓰기 | `update-reservation`(묶음 doctors — 확인 안 됨) |
| 수납 넣기 | 동작 #36 | KOS 수납 창에 항목 넣기 | **확인 안 됨**(공개 문서에 수납 command 없음 · HAR 필요) |
| 처방전 | 동작 #35 | — | 확인 안 됨 |
| 이전 방문 | §5 | 고객별 방문 조회(`queries/`) · prod 백필 확인 | (선택) `schedule/open/v1/queries/get-schedules-by-visitor` |
| 노쇼 표시 | 머리 | 시안 `S5` 에 없음 | — |

## 주의 · 미결

- v9 는 「예약메모 덧붙이기」 버튼을 그리지 않는다(처리기 L2312 ~ 2315 만). 11-13판 대비 v9 에 더해진 것 = 이전 방문 기록(h4 · dt 4 · pv · pv-toggle) · 동행 칸(grp 5동작) · 우클릭 메뉴. 빠진 것 = `M('고객 리포트')`(11-13판 grep 결과에만 있음).
- 시안 수납 숫자는 가짜 `r.pay = [총액, 낸 돈]` — 「할인 = 음수 상품 줄」은 DAY 구매 모양과 다르다(Q8).
- KOS 쓰기는 이 조사에서 호출하지 않았다. 경로는 코드 · cc · 공개 문서 목록에서만 확인 — 본문 · 응답은 「확인 안 됨」 표시한 곳 그대로.
