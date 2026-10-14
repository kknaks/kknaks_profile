# WORK-001 WP10 결과 보고 — SPEC 0.3.0 §0-b 데이터 · 동작

## 상태: done

## 수행 — 파일·모듈 목록

`cc/back/` 만. 커밋 없음. 통역 무변경.

| 파일 | 변경 |
|---|---|
| `app/service/memo_parse.py` | **삭제** — 양식 의존 가공 전부(⚠ 뽑기 · `------` 나누기 · OUT TIME · 빈 양식 줄 · 타 병원 이력 · 동행 · 예약 메모 칸) |
| `app/service/memos.py`(새) | 메모 공개 시점(쓰인 시점) · 방문 카드 `visits[]` · 위험 단어 일치 · 지정 직원(`mentionedStaffIds` — 오늘 근무 직원 이름 문자열 일치). **원문을 자르거나 바꾸지 않는다** |
| `app/service/bundles.py`(새) | 시술 후보 = **묶음 n/m** — 보유 시술권 세트 · 오늘 결제분(상담 종료 이벤트 시술, 같은 이름 한 줄) · 원장 상담(동선에 있으면 뺌). `resolve` = 묶음의 다음 1장(1회 차감) |
| `app/service/patient_service.py` | 다시 씀 — `customerMemo` · `reservationMemo` 원문 · `visits` · `riskWords` · `riskHits` · `mentionedStaffIds` · `requestedProcedures`(KOS) · `outTime` = `desiredDischargeDateTimeUtc` 만 · 차트 = KOS 구조 필드 · `route` 에 담당자 메모 없음 · `tickets` = 묶음 n/m. `cautions` · `order` · `consult` · `reception` · `history` · `pastSchedules` 없앰 |
| `app/domain/board.py` | 상담 완료 이벤트 = 공개 · 미결제만(**동선에 안 붙임**) · `payment_complete` 조건(상담 완료 뒤 · 이벤트 시술 또는 금액) · **`no_show` 조작 + KOS 주석** · 노쇼 예약 접수 막음 · `add_procedures` 가 해석된 항목(시술 · 원장 상담)을 받음 |
| `app/service/board_service.py` | check-in · add-procedures 의 `bundleId` 해석 · `no_show` · board 에 `customers[].mentionedStaffIds` · `riskWords` · 예약 행 `procedure`/`doctor` 제거 · `payment_complete` 에 이벤트 전체 전달 |
| `app/schemas/requests.py` · `app/api/desk.py` | check-in 단계 = `kind` 또는 `bundleId` · add-procedures = `bundleIds`(+ 이름만 `items`) · `POST /api/desk/no-show` |
| `app/seed/build.py` | 보유 시술권 묶음 `bundleId`(KOS `ticketGroupId`, 없으면 결제 id + 순서) · 예약 행에서 `procedure`/`doctor` 제거 |
| `app/config.py` · `app/container.py` · `.env.example` | `CC_RISK_WORDS`(기본 임플란트 · 아스피린 · 수면 · 알레르기 · 켈로이드 · 임신 · 지정 · 거부) |
| `README.md` | 0.3.0 API — 환자 상세 예시(원문 · visits · 강조 재료) · 후보 묶음 예시 · 조작 표(check-in `bundleId` · add-procedures `bundleIds` · `no-show` · 새 오류 code) · 예약 행 · `riskWords` · `mentionedStaffIds` |
| `tests/` | `test_scenario.py` 다시 씀 · `test_flow.py`(test_2 · 3 · 6 · 노쇼 · blocks) · `test_kos_comments.py`(조작 13) · 픽스처: 포텐자 묶음 7/10 · 예약 메모에 「상담사A 지정 요청」 |
| `data/seed.json` · `cc.db` | `seed build --date 2026-10-09` 로 다시 만듦(이전 것 `seed.20261013-174820.json`) |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest` | **48 passed**(픽스처 · 임시 DB) |
| `uv run ruff check .` | **All checks passed** |
| KOS 주석 · 호출 | 조작 함수 **13/13**(no_show 추가, 블록 19) · 호출 코드 0 |
| 양식 문자열 가공 | **0** — `test_no_memo_form_parsing_in_code`: `app/` 코드 줄에 `------` · `OUT TIME` · `특이사항` · `임플란트 여부` · `[상담내용]` · `받은시술` 0건, `memo_parse.py` 없음 |
| `seed build`(실제 시나리오) | 예약 8 · 직원 14(의사 2 · 상담사 3 · 피부관리사 2 · 간호사 4 · 코디 3) · 이벤트 8 |
| 실제 시나리오 스모크(임시 DB) | 재내원 WANG YI TING — 접수 전 지난 카드 1(오늘 카드 없음) · 후보 「포텐자 펌핑팁 7/10」·「쥬베룩 스킨 2cc 2/3」. 8명 상담 종료 → 동선 단계 **1개 그대로**(상담) · 오늘 후보 1~10개 · 미결제 0~3,166,790원. 응답 전체 이메일 0 · 캡처 실명 0 |

이번 항목:
- S2 visits(지난 카드 공개 · 오늘 잠금): `test_6_revisit_bundles_and_visits` · `test_2`
- 상담 종료 → 후보만: `test_consultation_done_gives_candidates_only` · `test_3`
- 묶음 n/m → 1회 차감: `test_6`(7/10 → 고르면 6/10 · 같은 묶음 두 번 = 2장 · 1/1 소진 뒤 `bundle_empty`)
- 원장 상담 중복 없음: `test_doctor_consult_candidate_not_duplicated`
- 노쇼: `test_no_show`(st noshow · 다시 400 · 노쇼 예약 접수 400 · 접수한 고객 400)
- 원문 그대로: `test_memos_raw_risk_words_and_mentions`(예약 메모 · 오늘 상담 · 오더 = 픽스처 원문과 같음) · grep 시험
- 실명 0: 스모크(캡처 이름 대조) · 응답 이메일 · 생년월일 0(`test_responses_have_no_email_birth_phone`)
- 결제 완료 뒤 후보의 시술권 연결: `test_payment_complete_links_tickets` · 담당자 메모는 방문 카드에만: `test_task_done_memo_only_in_visit_card`

## 계약 대조 — SPEC 0.3.0 §0-b

| 항목 | 판정 | 비고 |
|---|---|---|
| 원칙 — 원문 그대로 · 구조 필드만 | 같음 | 아웃 = `desiredDischargeDateTimeUtc`, 예약 시술 = `requestedProcedures` |
| 원칙 — 강조(위험 단어 · 직원 이름) | 같음 | 강조 표시는 front. back 은 `riskWords` · `riskHits` · `mentionedStaffIds` |
| 원칙 — 공개 = 쓰인 시점 | 같음 | 오늘 카드는 접수 뒤에만 생김(예약 상세엔 오늘 칸 없음 — #13) |
| 1 방문 카드 | 같음 | 날짜 · 상담사(KOS 상담 기록 counselors) · 상담 원문 · 오더 원문 · 그날 시술 · 담당자 메모, 최근이 위 |
| 2 상담 종료 = 후보만 · 원장 상담 중복 제거 · 미결제 · [결제 완료] | 같음 | |
| 3 후보 묶음 n/m · 1회 차감 | 같음 | 오늘 결제분은 같은 이름끼리 한 묶음 |
| 4 노쇼 | 같음 | 주석 「공개 없음 — KOS 요청(예약 상태 노쇼)」 |
| 5 지정 직원 | 같음 | 고객 · 예약 · 오늘/지난 상담 · 오더 원문 중 **지금 보이는 것**에서 |
| 6 빼는 것(cautions · 메모 outTime · 예약 행 procedure/doctor · 동선 담당자 메모) | 같음 | |

## 이슈 · 코디가 확인할 것

1. **지정 직원 · 위험 단어는 단순 문자열 일치라 잡음이 있다** — 실제 시나리오에서 상담 종료 뒤 거의 모든 고객의 `mentionedStaffIds` 에 그 상담사가 잡힌다(오더지 사본의 「실장 : ○○」 줄). 「임플란트」도 빈 양식 줄 「[임플란트 여부] x」에서 걸린다. 양식에 기대지 않는 원칙대로 걸러내지 않았다 — 화면에서 「지정 요청」 표시가 과해 보이면 규칙(예: 예약 · 고객 메모만)을 정할 것
2. 상담 종료 뒤 동선에 남은 단계가 없으면(후보만 있는 상태) 방 상태가 「귀가 대기」가 된다 — 데스크가 [시술 추가] 하면 다시 대기 단계. 「시술 추가 대기」 같은 별도 문구가 필요하면 SPEC 에서 정할 것
3. 예약 행 `st` 는 그대로(`booked` · `checked` · `canceled` · `noshow`) — 예약 탭 거르기(접수 전 · 귀가 · 노쇼)는 front. 귀가는 `customers[].flowStep == COMPLETED` 로 안다
4. 이름만 넣는 직접 추가(`items: [{label}]`)는 남겨 두었다(후보에 없는 시술). 필요 없으면 front 가 안 쓰면 된다
5. `data/seed.json` · `cc.db` 다시 만듦 — **8600 서버 재시작 · [초기화] 필요**. front(WP11)는 README 의 바뀐 응답(`visits` · 묶음 후보 · `no-show` · 없어진 필드)으로 맞춰야 한다

## fix1 — 상담 종료 뒤 「귀가 대기」 오표시 (2026-10-13)

- `app/domain/board.py` — 상담 완료 이벤트 때 오늘 결제 시술 순번을 고객에 `todayTaskSeqs` 로 남긴다(ETCETERA 원장 상담 제외). `status_of`: 남은 단계가 없어도 **동선에 안 넣은 오늘 결제 후보가 있거나 미결제 > 0** 이면 「다음 단계 대기」(`need: next` — 화면 「확인 필요」). 「귀가 대기」(`need: discharge`)는 남은 단계 · 남은 오늘 후보 · 미결제가 모두 없을 때만. 보유 시술권(지난 결제분)만 남은 경우는 귀가 대기 그대로
- 시험 2개(`test_fix1_candidates_left_is_next_not_discharge` — 상담 종료 직후 · 결제 완료 뒤에도 next, 후보를 다 넣고 다 끝내면 discharge / `test_fix1_only_held_tickets_left_is_discharge` — 재내원 보유 시술권만 → discharge, 상담만 · 금액 0 → discharge). `uv run pytest` **50 passed** · `uv run ruff check .` **All checks passed**
- KOS `flowStep` 전이는 그대로(남은 단계가 없으면 상담 종료 때 `PROCEDURE_DONE`) — 화면 상태만 바뀐다
- 응답 모양 변경 없음. 시드에는 고객이 없어 `seed.json` 은 그대로 쓴다(이 칸은 상담 종료 때 생긴다)
