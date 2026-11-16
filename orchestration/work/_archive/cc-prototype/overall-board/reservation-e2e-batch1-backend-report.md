# 예약 현황 E2E batch 1 — backend 결과 보고

- 2026-10-27 · task_94466333cbda · 코드 = `3c3c6ad` 위 미커밋(procedure/back 만)
## 상태: done

## 수행 — 파일
- `app/schemas/reservations.py` — 등록 본문 `consultationRequired · sedationRequired · doctorStaffIds` 뺌 · `RouteRequest` 뺌 · `ReceptionRequest.route`(consultation · direct · 기본 consultation) · `Can.addConsultation` · `ReservationInfo.consultationRequired` 뺌 · `ReservationForm.doctors` 뺌 · `ReservationForm.snsTypes` · `SnsIn/SnsOpt.type` = KOS enum Literal · 409 코드 `route_locked · identity_incomplete` 뺌, `not_consultation_addable` 넣음
- `app/domain/reservation_rules.py` — `axis()` = 06:00–22:00 고정(축 밖 카드만 늘림) · `can()` 신분 · 고객 정보 조건 뺌 · `editRoute` = 접수 전(예약 · 부도) 초진 · 재진 모두 · `addConsultation`
- `app/service/reservations.py` — 빈 조건 검색 허용 · form `doctors` 뺌 + `snsTypes` · 등록 KOS 본문 `doctors: []` · 상담 필요 · 수면마취 안 보냄 · `route()` 삭제 · 상세: 그 일정 KOS 바로 읽기(`refresh_schedule`) · 상세 「상담」 줄 = ccc 기록(접수 끝 단계 · 상담 추가) / 지금 상담 단계
- `app/service/reception.py` — 신분 확인(get-visitor) 삭제 · 끝 단계 = `route` · 기다림 0.5초 × 10 · 방 지정 확인은 바로 읽기 · 끝 단계 뒤 사본에 먼저 싣고 즉시 응답 → 3초 뒤 다시 읽기 + 시술 현황 조회는 뒤에서 · `consultation_add()`
- `app/api/reservations.py` — `PUT /reservations/{id}/route` 삭제 · `POST /reservations/{id}/reception {roomId, route}` · `POST /reservations/{id}/consultation-add`(본문 없음 · Ok)
- `app/service/fake_reservations.py` — 위와 같은 꼴(축 · can · form · 빈 검색)
- tests: `fake_kos.py`(등록 본문 칸 없음 허용) · `test_resv_board/contract/detail/reception/write.py` 고침 + 새 시험(상담 추가 3 · 경로 판정 · 상세 바로 읽기 · 빠진 등록 칸 422)

## 검증
- `uv run ruff check .` → All checks passed
- `uv run pytest -q` → **325 passed**(앞 313 + 새 시험)

## # 1 ~ 23 (backend 몫)
| # | 처리 |
|---|---|
| 1 | ✔ 빈 조건 = 내부 `get-visitors` 빈 값(최근 방문 순 · 20개 페이지) · 400 없앰 · `GET /api/customers/search?page=1` |
| 2 · 9 · 6 | 해당 없음(front) |
| 3 | 값 그대로 — `resourceIndex` 는 **묶음 번호이지 겹침 줄 번호가 아님**. 겹침 줄은 front 가 카드 `start/end` 로 계산(같은 칸 · 겹치는 시각). 따로 필드 안 넣음 |
| 4 | ✔ `axis` = 06:00–22:00 고정(축 밖 예약만 늘림 · 휴무일도 같은 축) · 운영 시간 = `columns[].open`(회색은 front) · `rows` 도 06–22 전 줄 |
| 5 · 19 · 20 | 해당 없음(front) |
| 7 | 추가 값 없음 — 머리 표기용 `columns[].capacities` + `zones[].title` 으로 충분(한 꼴로 그리는 건 front) |
| 8 | 해당 없음 — 검색 응답에 경고용 값 없음 · KOS `duplicated_visitor` 409 + `candidate` 그대로 |
| 10 · 11 | 해당 없음(front) |
| 12 | ✔ `can.receive` = 접수 갈래(새 접수 · 이어 하기)면 켜짐 · 접수 묶음 신분 확인 + `identity_incomplete` 없앰. 상세 `customer.identity`(fields · complete)는 표시용으로 남김 |
| 13 | ✔ `PUT /route`(KOS `update-reservation{consultationRequired}`) 삭제 · 접수 본문 `route` → 끝 단계(consultation → 상담 대기 · direct → 시술 대기) · `can.editRoute` = 접수 전 초진 · 재진 모두 · 상세 `reservation.consultationRequired` 뺌(KOS 값 안 읽음) |
| 14 | ✔ 측정 · 줄임 — 아래 |
| 15 | ✔ `POST consultation-add` + `can.addConsultation` · KOS 시험 받음 — 아래 |
| 16 · 18 | 해당 없음(front) |
| 17 | ✔ 상세 GET 이 **그 일정을 KOS 에서 바로 읽음**(내부 get-schedule-detail · 날짜 캐시 10초와 별개) → 5초 폴링마다 `paymentRequired` · 단계가 곧바로 반영(시험 `test_detail_reads_schedule_fresh_every_time`). 금액은 원래 열 때마다 KOS 직접 |
| 21 · 22 | ✔ 등록 요청에서 세 칸 뺌(보내면 422) · KOS `reserve` 본문에 `consultationRequired · sedationRequired` 없음 · `doctors: []`(KOS 화면 빈 값과 같음 — reservation-create-report) · form `doctors` 뺌 |
| 23 | ✔ `form.snsTypes = ["etc","kakaotalk","line","instagram","whatsapp","wechat"]`(값만 · 한글은 front) · 등록 · 고객 정보 수정 `sns.type` 이 이 enum 밖이면 422 |

## #14 측정(가짜 KOS · 가상 시계 — 스크립트 scratchpad `measure_reception.py`)
가정: KOS 호출 하나 = L초 · 쓰기 반영 = recept 3초 · add-flow-tasks 3초 · change-tasks-room 즉시 · change-flow-step 3초(reservation-reception-test-report 실측 0 ~ 3초 중 최악). 새 접수 · 바로 시술.

| L | 전(`3c3c6ad`) 응답까지 · KOS 호출 | 후 응답까지 · KOS 호출 |
|---|---|---|
| 0.1초 | 8.80초 · 18 | **7.50초** · 20 |
| 0.25초 | 11.50초 · 18 | **8.25초** · 17 |
| 0.5초 | 13.00초 · 16 | **10.50초** · 15 |

- 전: 단계(0.25초) — 오늘 사본 1.0 · 0단계 읽기 · get-visitor · recept · 1초 × 3 읽기 · add-flow-tasks · 1초 × 3 · 방 지정 · **1초 뒤** 읽기 · 끝 단계 · 끝 읽기 · 시술 현황 조회 → 11.5초. 끝 읽기는 KOS 반영 전이라 사본에 **RECEPTION 을 다시 써 넣음**(화면 「접수」가 다음 조회까지 남음 — 「시술 대기가 늦다」의 한 원인)
- 줄인 곳: ① 신분 읽기 삭제(#12) ② 반영 기다림 1초 → 0.5초 간격(한도 5초 그대로) ③ 방 지정은 바로 보이므로 첫 읽기를 기다리지 않음 ④ 끝 단계 뒤 **사본에 끝 단계를 먼저 싣고 바로 응답** — KOS 확인 읽기 · 시술 현황 조회는 3초 뒤 뒤에서(응답 밖 3.5초)
- 남은 큰 몫 = KOS 반영 대기(recept · add-flow-tasks 각 ~3초). **제안(안 함)**: 접수를 공개 `changeFlowStep(RECEPTION)` 으로 바꾸면 단계가 응답 직후 보인다(reception-test-report B) → 약 3초 더 줄일 수 있음. 오늘 데모 시험에선 내부 recept 도 0.0초에 보였다(반영 지연은 들쭉날쭉)

## §3 [+ 상담 추가] KOS 시험(데모 · 코디 승인 A · 스크립트 scratchpad `kos_consult_add_test.py` · 결과 `consult_add_result*.md`)
- 테넌트: 데모 표식 계정(KOS-DEMO) assert 통과 · 운영 키 사용 0 · 쓰기 경로 가드(허가 목록 밖 · 같은 경로 두 번째 차단)
- 대상: **시험용 일정 1건을 새로 만듦** — 4층 「기타」 10:30–11:00 · 데모 기존 고객(최근 방문 1번) · 메모 `[ccc 데모 2026-10-27] 상담추가 시험` · 방 지정 없음(시술 현황 카드 안 생김). 일정 id 는 로컬 scratchpad 파일에만
- 순서 · 결과(쓰기 6번)
  1. 내부 `reserve` — 200 (바로 읽기 404 → 다음 실행에서 보임)
  2. 내부 `recept` — 200 · RECEPTION 0.0초 뒤 보임
  3. 내부 `change-flow-step{PROCEDURE_WAITING}` — **400** InvalidRequestException
  3'. 같은 호출 **재시도 1회**(코디 지시 전 내 판단) — **400 `procedures · NotFound`** — 작업 0개면 KOS 가 시술 대기를 막음. 바뀐 것 없음
  4. 내부 `add-flow-tasks` 「방 배정」 ETCETERA 1개(방 없음) — 200 · 0.6초 뒤 보임
  5. 내부 `change-flow-step{PROCEDURE_WAITING}` — 200 · 0.6초 뒤 보임
  6. **공개 `change-flow-step{scheduleId, step: CONSULTATION_WAITING}` — 200 `{}` · +0.1초에 `CONSULTATION_WAITING`**(공개 · 내부 상세 · grouped 셋 다)
- 바뀐 값: 공개 · 내부 상세 둘 다 `flowStep` · `flowStepUpdatedDateTimeUtc` · `updatedDateTimeUtc` **세 개뿐**. 예약 상태 `IN_PROGRESS` · 접수 시각 · 작업 1개 · `consultationRequired=false` · 상담사 없음 그대로 — 상담 기록 · 작업 안 생김
- **판정: 받음** → [+ 상담 추가] = 그 호출 + ccc 이벤트 `consultation_add{reservationId, fromStep}` 로 구현. 상담 기록은 안 만든다(KOS [상담 시작] 몫)
- 끝 상태(남김): `CONSULTATION_WAITING` · `IN_PROGRESS` · 「방 배정」 ETCETERA 1개(방 없음 · NOT_STARTED)
- 덤: 3' 로 확인 — ccc 「바로 시술」 묶음은 「방 배정」 작업이 있으니 시술 대기를 받는다(room-report 와 같음)

## 계약 — front 에 전한 것과 다른 곳
- 코디 전달 ①~⑤ 그대로. 덧붙여 (a) form `doctors` 빠짐 (b) 상세 `reservation.consultationRequired` 빠짐 — 코디에 알림(terminal)
- `can.addConsultation` = KOS 단계 시술 대기 · 시술 중 · 귀가 대기 이고 취소 · 부도 아님. 서버도 KOS 단계를 다시 읽어 같은 조건(아니면 409 `not_consultation_addable`)
- `reception` 본문 `route` 를 빼면 기본 `consultation`

## 이슈 · 코디가 확인할 것
- SPEC 0.3.0 에 반영할 것: 축 고정 06–22 · `PUT /route` 없음 · `reception.route` · `consultation-add` · form `snsTypes` · 등록 세 칸 없음 · 상세 GET 이 그 일정을 KOS 에서 바로 읽음(상세 1번 = KOS 호출 +1)
- 상세 「상담」 줄 판정이 ccc 기록 기준 — KOS 화면에서 직접 상담 대기로 접수한 뒤 시술 대기로 넘어간 고객은 「상담」 줄이 안 보인다(ccc 기록 없음)
- 응답 뒤 할 일(3초 뒤 확인 · 시술 현황 조회)은 프로세스 안 백그라운드 — 서버가 그 사이 꺼지면 다음 10초 조회가 대신 맞춘다

---

# 리뷰 r2 수정(W1 · W3)
## 상태: done
- **W1 반영 지연 창 보호**: `ReservationService.pin_step(kos_id, step)` — 접수 묶음 · 상담 추가가 끝 단계를 사본에 실을 때 5초(`PIN_SEC`) 창을 건다. `refresh_schedule`(상세 GET · 묶음 다시 읽기)은 KOS 단계가 그보다 앞(`flow_rank` — `FLOW_STATE` 순서)이면 먼저 실은 단계 · 시각을 지키고, 5초가 지났거나 KOS 가 그 단계 이상이면 창을 풀고 정상 덮어쓴다. 파일: `app/service/reservations.py` · `app/domain/reservation_rules.py`(`FLOW_ORDER` · `flow_rank`) · `app/service/reception.py`(`_settle` → `pin_step`)
  - 상담 추가는 이전 단계(시술 대기 ~)가 상담 대기보다 뒤라 창이 바로 풀린다(공개 호출은 +0.1초에 반영 — §3 시험)
  - 날짜 조회(`ensure_day`)는 그대로 — 상세는 그 뒤 `refresh_schedule` 이 다시 지켜 최종 값이 끝 단계
- **W3**: `SnsOpt.type` = `str | None` · `''`/공백 → None · enum 밖 KOS 값 통과(`app/schemas/reservations.py`). 등록 `SnsIn.type` 은 enum 그대로
- 시험: `test_pinned_end_step_survives_stale_detail_read`(창 안 지킴 · 6초 뒤 KOS 값 · KOS 가 앞서면 풀림) · `test_personal_sns_type_blank_and_unknown`(5개)
- 검증: `uv run ruff check .` All checks passed · `uv run pytest -q` **331 passed**
