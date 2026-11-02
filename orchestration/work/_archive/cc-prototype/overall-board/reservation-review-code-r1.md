# 리뷰 리포트 — 예약 현황(SPEC-005 0.2.0) / code r1 (2026-10-26)

- 대상: `cc-prototype` 워크트리 `overall-board`(branch `kknaksss/overall-board`) **커밋 안 된 작업 트리 전체**(수정 28 · 새 파일 21). 앞 커밋 `d05cd88` 까지는 대상 아님
- 기준: SPEC-005 0.2.0 · WORK-007(WP-E2E 「reviewer:」 칸) · DEC-006 · **addendum-1(W1 ~ W5 · SPEC 보다 우선)** · `reservation-kos-probe-report.md`(K1 ~ K10) · SPEC-003 0.5.1 / SPEC-004(회귀)
- 실행(읽기만 · 포트 안 씀): `cd procedure/back && uv run pytest -q` = **310 passed**(경고 1 — starlette httpx deprecation, 기존) · `cd procedure/front && npx tsc --noEmit` = **0 오류**. lint · build 는 돌리지 않았다(frontend 리포트: lint 0 · build 성공)
- 코드 수정 0 · KOS 호출 0 · 프로세스 0

## 판정: FAIL

FAIL 1(frontend · 한 줄 고침) · WARN 7. 계약 본체(접수 묶음 · 신분 조건 · 두 구역 · 수납 필요 · 2계층 · 정원 · 이동 · 고객 저장 · 특이사항 · 오류 매핑 · `can.*` · KOS 본문 · 회귀 · 계층 · 누출)는 PASS.

## FAIL

| # | 파일:줄 | 무엇 | 근거 | 고칠 것 | 몫 |
|---|---|---|---|---|---|
| F1 | `procedure/front/components/reservations/DetailModal.tsx:944` | 상담 카드 「{이름} 실장 호출됨 · HH:MM」의 {이름}에 **`cons.calledBy`(버튼을 누른 ccc 계정 이름)** 를 먼저 쓴다. back 은 `calledBy` = 마지막 `counselor_call` 이벤트의 actor 계정 이름(`service/reservations.py:605`)이고 가짜 값도 「데스크 1」(`fake_reservations.py:323`)이다 → 실물에서 「코디 실장 호출됨 · 14:02」처럼 **호출한 데스크 이름이 실장 이름 자리에** 나온다 | SPEC-005 §5.8 「상담 카드에 「{이름} 실장 호출됨 · HH:MM」(마지막 `counselor_call` 이벤트)」 — {이름} = 호출된 상담사 · E2E #25 | {이름} = `cons.counselor?.name`(실장 호출 = KOS `counselor` 지정이라 호출 뒤 그 값이 그 실장). `calledBy` 를 보이고 싶으면 「· 데스크 {calledBy}」 로 따로 | frontend |

## WARN

| # | 파일:줄 | 무엇 | 근거 | 제안 | 몫 |
|---|---|---|---|---|---|
| W1 | `back/app/domain/reservation_rules.py:279` · `back/app/service/reservations.py:909` | 예약 메모 [저장] 켜짐 = `main ≠ canceled` 만 — SPEC §5.14 의 「`flow_step ≠ COMPLETED`」 조건이 빠져 **귀가 완료 예약도 메모 저장이 열린다** | addendum-1 W4 문구(「메모 저장 = `main ≠ canceled`」)를 글자 그대로 따랐다 — addendum 이 SPEC 보다 우선이라 위반은 아님. W4 의 뜻이 「부도를 연다」뿐이었는지(완료 막기는 남기는지) 코디 확인 필요 | 코디 결정: 그대로(addendum 문구) / `and flow_step != "COMPLETED"` 되살림(back 2곳 · front 는 `can.editMemo` 만 보므로 무변경) | backend(결정 뒤) |
| W2 | `back/app/domain/reservation_rules.py:129-133`(줄 = 축 시작부터 간격) · `back/app/service/reservations.py:861-862`(이동 = 자정 기준 `% interval`) · `front/components/reservations/ScheduleTable.tsx:184-188`(`rowAt` = 축 시작 기준) | **축 시작이 그 칸 간격의 배수가 아니면** 줄 · [+] · 놓기 자리가 KOS 슬롯 · back 이동 검사와 어긋난다. 예: 60분 칸이 있는 날 KOS 에서 09:30 운영 밖 예약이 하나 있으면 축이 09:30 으로 늘어 60분 칸 줄 = 09:30 · 10:30 … → 거기 놓으면 back 400 「간격 경계가 아니에요」 · 그 줄 `slots` 는 KOS 정각 슬롯과 안 맞아 `full` 이 늘 false · [+] 등록은 10:30 시작 60분 예약을 KOS 로 보냄 | SPEC §5.2 「칸마다 자기 간격으로 줄」 · §7.5 「`start` 는 그 칸 간격 경계」 — 경계의 기준점이 계약에 없다. 데모(전 그룹 10:00 시작 · 축 밖 예약 0)에서는 안 난다 | 기준점을 하나로: 줄 시작 = 축 시작을 그 칸 간격으로 내림(`a0 - a0 % iv`) — back `lines` · front `rowAt`/줄 그리기 같이. 또는 SPEC 에 「경계 = 자정 기준」 한 줄 | backend · frontend |
| W3 | `back/app/service/reservations.py:689-726` | 예약 등록 검사 순서: 409 `slot_full`(692) 이 404 `없는 고객`(699) · 400(유입 · 담당자 · 지정 의사 · 상담사 · 귀가 희망 시각 703 ~ 726) 보다 먼저 | SPEC §7.1 「검사 순서 = 401 → 403 → 400 → 404 → 409 → 502」 | 400 · 404 검사를 정원 409 앞으로(정원 검사는 `kos_write` 직전) | backend |
| W4 | `back/app/service/reservations.py:635-639` ↔ `back/app/domain/reservation_rules.py:283` | [미확인으로] 409 `identity_locked` 판정은 **고객 단위**(그 고객의 *오늘* 예약 중 접수 뒤가 하나라도 있으면) · 버튼 켜짐 `can.unconfirmIdentity` 는 **연 예약 단위**(`main ∈ {reserved, noshow}`). 같은 고객이 오늘 접수 뒤 + 다른 날 예약을 가진 경우, 다른 날 예약 상세에서 버튼은 켜지고 누르면 409 | SPEC §5.14 「[미확인으로]만 접수 전」 · backend 「해석한 곳 ⑥」 | 둘을 한 식으로(권장: 연 예약 기준 — `identity` 요청에 예약 id 가 없으니 `can` 쪽을 고객 단위 판정에 맞추는 게 쉽다) | backend |
| W5 | `back/app/service/reservations.py:422-423` | 고객 검색 생년월일 = 내부 `get-visitors` 본문 `dateOfBirth: "yyyy-MM-dd 00:00:00.000Z"` — **KOS 가 받는지 미확인**(K1 은 `indexOfPage · countInPage · visitorName · phoneNumber · chartNumber · sort` 만 봄 · backend 「해석 ⑦」) | WP-KOS K1 · SPEC §7.4(`birth` 칸) · OQ-706 | E2E #8 에서 생년월일 하나로 검색해 결과 확인 → 무시되면 front 칸을 끄거나 SPEC 개정 | 코디(E2E) |
| W6 | `back/app/container.py` · `back/app/domain/models.py` · `back/app/service/kos_errors.py`(새) · `back/tests/conftest.py` · `back/tests/test_kos_sync.py` · `procedure/README.md:42-43`(API 줄 role 목록) | WORK-007 WP-BE* 대상 파일 목록 · addendum W3 · 코디 허가(env 이름 줄) 밖. 다만 모두 브리프 allowed_paths `procedure/back/**` 안이고 필요한 배선(컨테이너 · 모델 · 오류 매핑 · 시험 고정값)이라 FAIL 로 보지 않음. README 는 env 줄 외에 API 설명 줄 하나(role 에 coordinator)를 고침 | `rules.md` 「allowed_paths 이탈 = FAIL」(경로는 안 · 목록만 밖) | WORK-007 대상 파일에 더해 기록(addendum W3 처럼) | 코디 |
| W7 | `back/app/domain/errors.py:42-48` | `NotReady`(501 `not_ready`) — BE0 뼈대용 · 지금 쓰는 곳 0(backend 「⑩」) | — | 지우기(다음 수정 batch 에 같이) | backend |

## 항목별 대조 (요약 — 근거는 파일:줄)

### 1. SPEC §1 ~ §8 ↔ 코드

| 절 | 판정 | 확인한 곳 |
|---|---|---|
| §3.2 표 · 열 · MIGRATIONS | PASS | `repository/db.py:105-160`(표 9 · `customer.gender` 마이그레이션) · 옛 DB 시험 통과 |
| §3.4 코디 계정 · 수락 | PASS | `service/accounts.py`(`_fixed` · `_passwords` coordinator) · `service/actions.py` `accept()` `admin`\|`coordinator`(doctorId 없으면 400) · `tests/test_auth_roles.py:156`(코디 수락 · 400) · front `lib/session.ts:12` · `lib/types.ts:158` |
| §4.2 1시간 목록 · 날짜별 · 캐시 · 잠금 · 실패 · 오늘 갱신(W7) | PASS | `kos/reservation_sync.py:177-364`(구역 → 그룹 `zoneIds` 전 구역 → 다른 구역 방(`KOS_ZONE_ID` 밖만) → 유입 → 기타 작업 · `ensure` 날짜 잠금 · `sync.lastError` · 슬롯 · 공지 · 금액 실패는 이름만) · `service/reservations.py:245-251`(`ensure_today` — 상세 457 · 접수 `reception.py:100`) |
| §5.1 2계층 | PASS | `reservation_rules.py:13-39`(취소 · 부도 먼저 · 모르는 단계 = 예약) |
| §5.2 칸 · 축 · 카드 · 「그룹 없음」 | PASS(W2 제외) | `reservation_rules.py:95-145` · `service/reservations.py:270-320`(묶음당 1장 · 「그룹 없음」 `groupId:null` · `capacities` 구역별) · front `ScheduleTable.tsx`(1시간 144 · 칸 간격 · 운영 밖 회색 · 지금 줄 · 자동 스크롤 · 겹침 상한) |
| §5.3 건수 | PASS | `service/reservations.py:290-292 · 322-325` |
| §5.4 정원(구역별) · [+] · 드래그 · 제자리 · 길이 · 구역 그대로 · W2(꺼진 구역 금지) | PASS | back `reservations.py:307-317 · 845-892`(제자리 허용 · 길이 유지 · 같은 날짜 · 구역 꺼짐 400) · front `ScheduleTable.tsx:263-287`(카드 구역 슬롯 `full` · `zoneOn` · 빨간 점선 · 제자리) · `live/page.tsx:79-101`(낙관 → 실패 원위치 + 토스트) |
| §5.5 등록(신규 구분 · 중복 409 + candidate · 구역 기본 · 담당자 기본 · uuid4 · `funnel` 코드 행 전체 · 정원 409) | PASS(W3 제외) | `reservations.py:678-842` · front `NewReservationModal.tsx:53-76 · 118-129 · 184 · 213 · 223-227` |
| **§5.6 접수 묶음** — 0단계 갈래 다시 정함 · 끝 단계 이후 = 보내지 않고 ok · 신분 칸 409 + `fields`(W5) · 붙은 방 고정 `room_locked` · 구역 밖 방 400 · `room_busy` · `room_task_missing` · 건너뛰기 4종 · 1초 × 5 · `kos_slow` · 멈춤 + `step` · 되돌리지 않음 · `event_log(reception)` · tick | PASS | `service/reception.py:92-198` |
| §5.7 방 · 사용 중(구역별 · type 무관 · 귀가 대기 뺌) | PASS | `reservations.py:109-118 · 488-493` |
| §5.8 상담 카드 · 상담사 상태(두 구역) · [실장 호출] | PASS(표시 F1 제외) | `reservations.py:121-129 · 594-611` · `reception.py:201-218` |
| §5.9 수납 필요 · 잇는 키(`visit.kos_id` · `kos_sequence` · 호출 원천 `doctor_call_item` = `Rules._called` 와 같은 표) · 금액 | PASS | `reservation_rules.py:163-211` · `repo.py:366-372` · 카드 · 원내 · 정산 같은 함수(`ResvContext.payment`) |
| §5.10 [귀가 완료] — 수납 필요 막기 · 공개 `changeFlowStep(COMPLETED)` · KOS 400 → 409 | PASS | `reception.py:221-235` · `kos_errors.py:30-37` |
| §5.11 건강 · 확인 필요 · 제출본 없음(`errorProperties visitorId NotFound`) · 이력 1회 | PASS | `reservation_rules.py:288-303` · `reservations.py:568-573 · 580-592` · `repo.py`(UNIQUE · INSERT OR IGNORE) |
| §5.12 ① 신분 칸(외국인 · 내국인 · 국적 빈 값 = 외국인 · 영문명 하나 이상) ② ccc 표시만 | PASS(W4 제외) | `reservation_rules.py:219-234` · `reservations.py:628-641` · front `DetailModal.tsx:373-414` |
| §5.13 이전 방문(같은 날 뺌) · 고객 저장(다시 읽은 묶음 + 바꾼 칸 · 없던 키 안 보냄) · 특이사항(관리 묶음 + memo · 빈 배열 뺌) | PASS | `reservations.py:164-190 · 930-976 · 984-1024` |
| §5.14 `can.*`(addendum W4 반영) | PASS(W1 · W4 확인) | `reservation_rules.py:270-284` · front 는 `can.*` · `receiveMode` · `roomLocked` 만 봄(`DetailModal.tsx`) |
| §6.1 헤더 — 항목 순서 · 「현황」 글자 = 시술 현황 · 부모 활성 두 경로 · `/reservations` → live | PASS | `AppHeader.tsx:13-25 · 78-79` · `app/(main)/reservations/page.tsx` |
| §6.2 ~ §6.7 화면 · 갱신(10초 · 직후 + 2초 · 상세도 W1) · 토스트 | PASS(F1 제외) | `lib/hooks.ts:119-190` · `live/page.tsx` · `ResvAside.tsx` · `NewReservationModal.tsx` · `DetailModal.tsx:132-154` |
| §7.1 오류 본문 `step` · `candidate` · `fields` · 403 `fake_board` · 가짜 GET 넷 | PASS(순서 W3) | `domain/errors.py:7-12` · `main.py:48-49 · 85` · `api/reservations.py` · `api/deps.py:27` |
| §7.2 ~ §7.5 모양 | PASS | `schemas/reservations.py` · `tests/test_resv_contract.py` |
| §7.6 경로 34 | PASS | `tests/test_order.py` `test_route_count_34`(예약 15 · 합 34) |

### 2. 기본값 · 워커 「다르게 한 곳」 10개

- §10 planner 기본값(OQ-701 · 702 · 704 ~ 715 · 717 · 720 ~ 727 · 729 · 731 ~ 742 · 752 · 757 ~ 759)이 코드에 그대로다 — 예: 10초 폴링 `lib/hooks.ts:119-120` · 캐시 10 `config.py:32` · 동기 쓰기 `reservations.py:644-655` · uuid4 `:737` · 담당자 = 시스템 계정 `:783-790` · 이동 = 내부 `update-reservation` `:885` · 「신규 고객 / 기존 고객 · No.」 `NewReservationModal.tsx:228` · 부도 빨강 외곽선 `view.tsx:33-34` · 국기 `flag-icons` `view.tsx:221-244`. addendum W1 ~ W5 모두 반영(W1 `DetailModal.tsx:140` · W2 `ScheduleTable.tsx:269` + `reservations.py:863` · W4 `reservation_rules.py:275 · 279` · W5 `reception.py:174`)

| 워커 | 다르게/해석 | 판정 |
|---|---|---|
| BE ① | `slots` · `rows` = 축 전체 줄(운영 밖 포함) | PASS — §5.4 「[+] 운영 시간 안팎 상관없이」와 맞음 |
| BE ② | 켜진 구역 0 인 칸 `plusAllowed=false` | PASS — 등록할 구역이 없다(§5.5 400 과 같은 뜻) |
| BE ③ | 「그룹 없음」 칸은 그런 카드가 있을 때만 | PASS — §5.2 「그 예약을 모은다」 |
| BE ④ | `additionalPhone` = `phone` 꼴 | PASS |
| BE ⑤ | 축 밖 예약 = 30분 단위로 늘림 · 휴무 요일에도 카드가 있으면 축 | PASS(축 늘림 자체) — 단 늘린 축의 간격 경계는 W2 |
| BE ⑥ | `identity_locked` = 그 고객의 오늘 예약 중 접수 뒤 | WARN → W4 |
| BE ⑦ | 검색 생년월일 본문 꼴 | WARN → W5 |
| BE ⑧ | 등록 `counselorStaffId` 가 상담사 아님 = 400 | PASS — §7.5 400 「형식 · 빈 필수」 범위 · `not_counselor` 는 실장 호출용 |
| BE ⑨ | 없는 방 id = 404 | PASS — §7.5 「없는 id = 404」 |
| BE ⑩ | 501 `not_ready` 없음 | PASS(남은 클래스는 W7) |
| FE ① | `rows[]` 에 없는 줄도 [+] | PASS — back 이 축 전 줄을 주므로 사실상 front 확장 축 줄만 |
| FE ② | front 도 축을 늘림(둘 중 큰 쪽) | PASS — 규칙 값(§5 머리 목록) 아님 · back 축과 같은 식 |
| FE ③ | SNS 종류 자유 입력 | PASS — KOS enum 미확인 |
| FE ④ | 겹침 상한 넘으면 칸 안 가로 스크롤 | PASS — §5.2 문장 그대로 |
| FE ⑤ | 나라 이름 표 67개 · 없는 코드는 코드 | PASS — OQ-734 · §6.3 |

### 3. KOS 호출 본문 = WP-KOS 판정 모양

PASS. 경로 · 키를 `reservation-kos-probe-report.md` 와 하나씩 맞춰 봤다.

| 호출 | 코드 | WP-KOS |
|---|---|---|
| 구역 · 그룹 · 다른 구역 방 · 유입 · 기타 작업 | `reservation_sync.py:24-27 · 193-253` | K1 같음 |
| 하루 예약 `{baseDateUtc(KST 0시 UTC .000Z), reservationGroupIds, zoneIds 전 구역}` | `reservation_sync.py:290-291` · `clock.kos_utc` | K1 같음 |
| 슬롯 `data[{reservationGroupId, zoneId, slots[{zone{id}, …}]}]` | `reservation_sync.py:322-341` | K1 같음 |
| 공지 · 수납 · 상세 넷(`get-visitor` · 양식 · 제출본 최상위 · 이전 방문) | `reservation_sync.py:343-364` · `reservations.py:552-578` | K1 · 주의 1 · 2 |
| `find-duplicated-visitor` · `create-visitor`(동의 플래그 없음 · 생년월일 꼴) · `reserve`(7칸 · `funnel{funnel:<행 전체>, funnelDetail}`) | `reservations.py:705-707 · 735-750 · 807-834` | K2 |
| 이동 `occupiedResources{items:[id · type · reservationTime · reservationGroup{reservationGroupId, zoneId, doctors}]}` | `reservations.py:876-886` | K3 |
| 진행 경로 · 실장 호출 · 메모 · 취소 | `reservations.py:900 · 911 · 923` · `reception.py:214` | K4 · K5 · K6 · C1/N1 |
| 고객 저장(읽은 묶음 키만 + 바꾼 칸 · `dateOfBirth "… 00:00:00.000Z"` · 만료일 `yyyy-MM-dd`) | `reservations.py:937-948 · 984-1024` | K7 |
| 접수 묶음 `recept` · `add-flow-tasks(etceteraConfiguration)` · `change-tasks-room{sequences, roomId}` · 내부 `change-flow-step{id, step}` · 방 없음 = `room.id` 빈 값 | `reception.py:35-38 · 121-146` · `reservation_sync.py:106-107` | K8 · 주의 3 · 4 |
| 귀가 공개 `change-flow-step{scheduleId, step:"COMPLETED"}` | `reception.py:230-231` | K9 · K9b |
| 고객 검색 `get-visitors` | `reservations.py:419-423` | K1 같음 — `dateOfBirth` 키만 미확인(W5) |

- 운영 키 · 실제 테넌트 하드코딩 0 — 테넌트는 `settings.kos_tenant_id`(딥링크 `reservations.py:624`) · 시험은 `fake.test` 도메인 · 지어낸 id

### 4. 시술 현황 회귀

PASS.
- 기존 시험 전부 통과(310 = 기존 210 + 새 100)
- 헤더: 항목 하나 더함 · 「현황」 href = `items[0]` 그대로 · 활성 판정 두 경로(`AppHeader.tsx:13-25 · 78-79`) — SPEC §6.1 이 허용한 두 곳뿐
- 수락: 분기 하나만 넓힘(`service/actions.py` `accept()`) · 코디 doctorId 필수 시험
- 동기화 루프: `master_once` 뒤에 예약 목록을 붙이고 예외는 삼킴(`kos/runtime.py:57-61`) — 시술 현황 직원 · 방 조회 결과 · 순서 그대로(`test_kos_sync.py` 앞 5개 경로 같음)
- 다른 구역 방이 `room` 사본에 늘어도 시술 현황은 방을 id 로만 찾는다(`actions.py:110` · `board_service.py:86` · `push.py:91` · `rules.py:84` — 목록으로 도는 곳 0)
- `KosError` 메시지 문자열 그대로(`kos/client.py:285`) · `customer` 읽기에 `gender` 더함(마이그레이션이 먼저 돈다)

### 5. 계층 · 기능 독립 · allowed_paths

PASS.
- router(`api/reservations.py`)는 HTTP 만 · 규칙은 `domain/reservation_rules.py`(HTTP · DB · KOS 모름 · 도메인 예외만) · KOS 는 `kos/reservation_sync.py` · 저장은 `repository/repo.py`(sqlite 행 → dataclass · ORM 없음 · 밖으로 행 객체 안 나감) · service 가 pydantic 응답을 만드는 건 기존 `board_service` 와 같은 꼴
- import: back = `app.*` 만 · front = `@/lib/*` · `@/components/{common,reservations}` · medikit · react · next 만. `cc/` · 다른 기능 import 0
- 경로: back 은 `procedure/back/**` · front 는 `procedure/front/**` · `.env.example` · `README.md` 는 코디 허가 범위(목록 밖 파일은 W6). `procedure/app/`(시술실 앱) 변경 0

### 6. public 누출

PASS. 바뀐 · 새 파일 전부 grep(uuid · 24자리 hex · 이메일 · `Bearer <값>` · `eyJ` · 외부 URL) → 시험 가짜 도메인(`fake.test`) · 시험용 `Bearer nope.sig` 뿐. 가짜 데이터 이름 = 「고객」 · 「상담사 1」 · 「원장 1」 · 「가 원장」 꼴 · 구역 「4층 · 5층 · 미사용」 · 방 「B-룸1」. 실명 · 연락처 · KOS id · 금액 실값 0. env 는 이름만.

## 고객이 실물에서 만날 자리

1. **[실장 호출] 뒤 상담 카드에 데스크 이름이 실장 이름처럼 보인다**(F1) — E2E #25 에서 바로 보인다
2. **귀가 완료 예약의 메모 [저장]이 열린다**(W1 · addendum 문구 그대로) — 끝난 예약 메모를 고칠 수 있다
3. **60분 칸 + 운영 밖 09:30 예약이 있는 날** 드래그 · [+] 자리가 30분 어긋나 400 · 정원 미표시(W2) — 데모 데이터로는 안 남
4. 고객 검색을 **생년월일만**으로 하면 KOS 가 조건을 무시할 수 있다(W5 · E2E #8)
5. 신규 고객은 보내지 않아도 **정보성 알림 동의 = true** 로 저장된다(OQ-753 · 사용자 알림거리 — 코드 문제 아님)
6. 두 데스크가 같은 줄 마지막 자리에 거의 같이 놓으면 **정원을 넘길 수 있다**(OQ-760 · E2E #12 관찰 — 계약대로)
7. `KOS_WEB_BASE` 가 비면 [수납하기 ›] · [처방전 출력]이 회색(title 「KOS 웹 주소가 설정되지 않았어요」) — E2E 전 `.env` 확인

## 참고(기존 부채)

- SPEC-003 §7.4 의 경로 수 내역(「router 18 + health」)은 그쪽 부채 — SPEC-005 §7.6 이 적어 둔 대로 안 고침
- 시험 경고 1(starlette `httpx` deprecation) — 기존
- `procedure/README.md:67` 의 운영 키 이름 언급(`KOS_API_tenent` 금지 문구)은 기존 줄 · 값 아님
- frontend 리포트: `next build` 첫 실행이 Next 보안 업그레이드 안내로 exit 1(두 번째 성공) — 범위 밖 · 코디 판단
- `reception.py` 가 `ReservationService` 의 `_event` · `_reservation`(밑줄 메서드)을 직접 부름 — 동작 문제 없음 · 취향이라 지적 안 함

## 사용자 결정 필요

없음. 코디 확인 1건 — **W1**(addendum W4 「메모 저장 = `main ≠ canceled`」가 귀가 완료 막기까지 푼 뜻인지).
