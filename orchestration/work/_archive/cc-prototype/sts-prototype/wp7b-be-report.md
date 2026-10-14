# WORK-001 WP7b 결과 보고 — 목데이터 시나리오 로더 · 상담 완료 이벤트 · [결제 완료] · 미결제 금액

## 상태: done

## 수행 — 파일·모듈 목록

`cc/back/` 만. 커밋 없음. 통역 무변경.

| 파일 | 변경 |
|---|---|
| `app/seed/build.py` | **새로 씀** — 시나리오 로더(`load_scenario`: `seed.json` + `events/*.json`) · 개원 전 시드 · 직원(`staffIds` + 이벤트 상담사, 없으면 백업 규칙) · 5직군. **캡처 직접 읽기 제거** |
| `app/seed/__main__.py` | `build [--date] [--scenario]` — `CC_SCENARIO_DIR`(기본 `data/scenario`). `--date` 는 시나리오 날짜 확인용 |
| `app/seed/capture.py` | 시각 도우미만 남김(캡처 읽기 `Capture` 삭제) · `app/seed/names.py` 삭제(이름 치환은 시나리오가 함) |
| `app/domain/board.py` | 고객에 이벤트 칸(`consultApplied` · `consultation` · `orderMemo` · `payment` · `unpaidAmount` · `paid`), 단계에 `paymentRequired` · `assigneeMemo`. **상담 완료 이벤트**(상담 단계 finish 때) · **시술 완료 이벤트**(시술 finish 때 담당자 메모) · **`payment_complete` 조작 + KOS 주석** |
| `app/service/board_service.py` | finish 에 그 고객 이벤트 전달 · `payment_complete` · 응답에 `unpaidAmount`(고객 · 방) · `paid` · 단계 `paymentRequired` |
| `app/service/patient_service.py` | 원천 = 시드 + 고객 상태(이벤트). 메모 공개 = 상담 완료 이벤트 뒤 · 「오늘 결제」 = [결제 완료] 뒤 · `pastSchedules` · 지난 방문 이력 · 동선 `memo`(시술 완료 이벤트) · 후보 = 보유 시술권 + (상담 완료 뒤) 동선에서 빠진 이벤트 시술 |
| `app/service/staff_service.py` | home 행에 `unpaidAmount` |
| `app/api/desk.py` | `POST /api/desk/payment-complete` |
| `app/config.py` · `.env.example` | `CC_SCENARIO_DIR=data/scenario` |
| `README.md` | 시나리오 · 이벤트 설명, 값 사전(`paymentRequired` · `unpaidAmount`), board · patient 예시 갱신(`unpaidAmount` · `paid` · `pastSchedules` · route `paymentRequired`/`ticketId`/`kosSequence`), 후보 · 조작 표(`payment-complete`, `nothing_to_pay`) |
| `tests/fixtures/`(새) | **가짜 직원**(`kos-staff.json`, 12명 · 가짜 이메일) · **가짜 시나리오**(`scenario/seed.json` 5일정 — 첫 방문 · 재내원(보유 시술권 · 지난 방문 synthetic) · 취소 + `events/sch-1.json`(상담 완료 · 결제 완료 · 시술 완료) · `sch-4.json`(상담만)) — 형식 문서 그대로 |
| `tests/` | `test_scenario.py`(새) · `test_flow.py`(픽스처 기준으로 다시 씀) · `conftest.py`(픽스처 · 임시 DB) · `helpers.py`(`consult_done`) · `test_kos_comments.py`(조작 12) · `test_privacy_memo.py` 삭제(캡처 의존 → `test_scenario` 의 응답 검사로) |
| `data/seed.json` · `data/cc.db` | researcher 시나리오(`data/scenario/`)가 와 있어 **`seed build --date 2026-10-09` 로 만들어 둠**(이전 것 `seed.20261013-161715.json`) |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest` (cc/back) | **43 passed** — 시험 픽스처 + 임시 DB(사용자 `data/` 안 씀). 캡처 · 실제 `kos-staff.json` 없이 돈다 |
| `uv run ruff check .` | **All checks passed** |
| KOS 주석 | 조작 함수 **12/12**(payment_complete 추가, 블록 18) · KOS 호출 코드 0(시험 · grep) |
| `seed build --date 2026-10-09`(실제 시나리오) | 예약 8(취소 0) · **직원 14 = 의사 2 · 상담사 3 · 피부관리사 2 · 간호사 4 · 코디 3**(사용자 지정 인원과 같음) · 이벤트 8 |
| 실제 시나리오 스모크(임시 DB, `seed.json` 사본) | 8명 모두 접수(상담) → 방 → 배정 → 시작 · 종료 → 상담 완료 이벤트 적용(추가 단계 10 · 5 · 4 · 2 · 4 · 10 · 2 · 1개, 미결제 0~3,166,790원) → [결제 완료] 7명 200(시술권 연결 9 · 4 · 3 · 1 · 3 · 9 · 1장), 1명(수납필요 · 금액 없음) 400 `nothing_to_pay`. 응답 전체 이메일 0 · `dateOfBirth` 0 · **캡처 실제 고객 이름 0** · 재내원 1명(`pastSchedules` 1 · 보유 시술권 2) |

이번 항목:
- 상담 완료 → 단계 추가 · 수납필요 · 금액: `test_consultation_done_adds_tasks_unpaid`(원장 상담 + 시술 3, `paymentRequired` · planned · `kosSequence` 유지, 고객 · 방 `unpaidAmount` 1,280,000, 오더 · 상담 메모 · ⚠ 주의(양쪽) · 타 병원 이력 열림, 「오늘 결제」 아직 없음)
- 결제 완료 → 해제 · 0 · ticketId: `test_payment_complete`(상담 전 400, 뒤 수납필요 전부 해제 · 0 · `paid` · `ticketIdsBySequence` 대로 연결 · 「오늘 결제」/「서비스(0원)」 공개 · 두 번째 400)
- 시술 완료 → 담당자 메모: `test_task_done_reveals_assignee_memo`(진행 중엔 없음, 종료 뒤 이벤트 메모, 이벤트 없는 순번은 빈 값)
- 재내원 시드 → 보유 시술권 후보: `test_6_revisit_default_tickets`(AVAILABLE 장만 · USED 제외 · 접수하면 동선에 · 후보에서 빠짐 · `pastSchedules` · 지난 방문 이력)
- 그 밖: 상담만(시술 0 · 금액 0) → 귀가 대기 · 이벤트 파일 없는 고객 · 직원 백업 규칙 · §11 1~7 다시(픽스처)

## 계약 대조 — SPEC 0.2.1 §0-a · scenario-format.md

| 항목 | 판정 | 비고 |
|---|---|---|
| 시드 = 시나리오 파일, 캡처 직접 읽기 없음 | 같음 | `seed.json` 의 `ticketBundles` · `pastSchedules` · `staffIds` 사용 |
| 상담 완료 이벤트(상담 단계 [종료]) | 같음 | 상담 기록 · 오더 메모 · tasks → 단계(planned · `paymentRequired` · `kosSequence`) · 결제 합계 → `unpaidAmount`. 이미 동선에 있는 순번 · 시술권은 다시 넣지 않음 |
| [결제 완료] | 같음 | 경로 `/api/desk/payment-complete`. 주석 「KOS 결제 조회 — 공식 getPurchaseSummariesByVisitor · getTicketBundlesQuery」 |
| 시술 완료 이벤트 | 같음 | `taskDone[sequence].assigneeMemo` → 동선 그 줄 `memo` |
| 차트 「오늘 결제」 = [결제 완료] 뒤 | 같음 | |
| 응답 `unpaidAmount`(방 · 고객) · `paymentRequired` · `pastSchedules` · 보유 시술권 | 같음 | 환자 상세에도 `unpaidAmount` · `paid` |
| `staffIds`(코디 답) | 같음 | 이벤트 상담사가 목록에 없으면 더한다. 없으면 백업(이벤트 등장 + COORDINATOR 활성) |

## 이슈 · 코디가 확인할 것

1. **직군 규칙 보완** — `staffIds` 사람 중 이벤트에 상담사로 나오지 않은 사람은 **COUNSELOR 태그를 후보에서 뺐다**(태그가 여럿일 때만). 안 그러면 CALL_COUNSELOR · COUNSELOR · COORDINATOR 를 함께 가진 코디가 §4 우선순위로 「상담사」가 된다. 실제 시나리오 결과가 사용자 지정 인원(의사 2 · 코디 3 · 간호사 4 · 피부관리사 2 + 상담사 3)과 맞는다
2. 상담 단계 없이 접수한 고객(재내원 등)은 상담 완료 이벤트가 들어올 자리가 없어 오더 · 상담 메모가 열리지 않는다 — 재내원은 `pastSchedules`(지난 상담 · 오더)로 본다. 0.2.0 의 「상담 단계가 없으면 처음부터 공개」는 이벤트 모델로 바뀌며 없어졌다
3. 이벤트 시술은 상담 종료 순간 **자동으로 동선 뒤에 붙는다**(§0-a 「단계로 추가」) — 데스크는 순서 · 배정만. 수납필요인 단계도 배정 · 시작은 막지 않는다(SPEC 에 막는 조건 없음)
4. 실제 시나리오 고객 이름에 `[TW]` · `[HK]` · `[JP]` 접두가 붙어 있다(KOS 이름 꼴 그대로 — researcher 결정). 화면에 그대로 나온다
5. `data/seed.json` · `data/cc.db` 를 새 시나리오로 다시 만들었다 — **8600 서버는 재시작 · [초기화] 필요**
6. WP8 front: README 의 새 필드(`unpaidAmount` · `paid` · `paymentRequired` · `pastSchedules` · route `ticketId`/`kosSequence`) · `payment-complete`

## WP7c — 고객 이름 국적 접두 떼기 (2026-10-13)

- `app/seed/build.py` — 시드 build 때 `visitor.name` 에서 `^\[[A-Z]{2}\]\s*` 를 한 번 떼어 저장(`display_name`). 예약 목록 · board · home · 환자 상세 이름이 모두 이 값을 쓴다. `nationality` 그대로, 메모 본문 · 이벤트는 손대지 않음
- 시험 1개(`test_name_prefix_removed` — 픽스처에 `[TW] CHEN YU` · `[JP]SATO AOI` 를 넣어 board · 예약 · 고객 · 환자 상세 · 순회형 home 이름과 국적 확인). `uv run pytest` **44 passed** · `uv run ruff check .` **All checks passed**
- `seed build --date 2026-10-09` 로 `data/seed.json` 다시 만듦(이전 것 `seed.20261013-162554.json`) — 예약 8 이름: LIU JIA HUI · CHEN XIAO WEN · 김하늘 · WANG YI TING · CHAN MEI LING · LIN YA CHEN · TANAKA YUKI · HUANG SHU FEN(국적 TW · TW · KR · TW · HK · TW · JP · TW). 8600 서버는 재시작 · [초기화] 뒤 반영
