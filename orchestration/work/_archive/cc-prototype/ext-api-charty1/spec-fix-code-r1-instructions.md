# planner 5차 — 코드 검수 r1 의 SPEC 한 줄들 (SPEC-008 0.4.4)

원 브리프 제약 그대로. 근거 `review-code-r1.md` Q1 ~ Q3 · W5. 코디 기본값으로 DEC-012 에 D 번호 하나로 묶어 적고, SPEC 0.4.4 변경 이력 1행.

- Q1 · §6.11 4 ⓐ: 「처음 봄 때 이미 귀가면 ⓒ 몫도 겸한다(`final_tried = 1`)」 · T57 에 그 갈래
- Q2 · §6.4 · T48: KOS 「고객 없음」 = HTTP 404 **또는** 400 + `errorProperties` `id NotFound` → 같은 404 `customer_not_found`(선례 문진 `visitorId NotFound`). 실물 꼴은 E2E-LOCAL ① 에서 확인
- Q3 · §6.12 표: `customer.customerId` = 고객 사본이 없으면 null(직원 상세의 0 과 다름)
- W5 · §6.11 · §6.9: board 는 `event_log` 를 그날 예약 id 로 걸러 읽는다(전체 읽기 아님)
- T49: 명시 `null` 은 「없음」(섞임 판정은 값이 있는 칸 기준)

보고: 고친 곳 표 · public grep · 두 채널.
