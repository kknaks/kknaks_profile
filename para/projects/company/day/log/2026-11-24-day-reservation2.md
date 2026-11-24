# 작업 요약 — day-reservation2 (day)

기간: `2026-11-24`
결과: DAY 웹 **예약 등록 · 예약 상세(예약 → 귀가) · 카드 우클릭 · 예약 현황 SSE** 구현. 스펙 mediness #961(DAY-SPEC-007 새로 · SPEC-006 ⑫ ⑬ · SPEC-002 ㉘ · SPEC-000 ②). 코드 CENTURION_DAY #280(dev 대상 · origin/dev `e76e27be` 위 rebase · migration 0026 ~ 0028 · check.sh 전체 통과). Delivery #275 ~ #278(4판). 사용자 화면 확인 B1 ~ B42(고침 34 · 철회 7 · 남음 1).

## 1. 무엇을 했나

시안 v9(`20261124_예약현황_시연`)의 예약 상세 모달 · 예약 등록 창을 만들었다. 오른쪽 시술 목록만 시안 대신 사용자와 정한 와이어(KOS 시술권 카드 모양).

- **예약 등록 창**: 기존 고객 · 새 고객([저장 후 예약 등록] = 같은 고객 찾기 → KOS 고객 만들기 → 예약 만들기) · 예약그룹 · 담당자 = 로그인 직원 · 지정 의사(`reservationGroup.doctors`) · 유입 · 메모 · 미리보기 「새 예약」 카드 · 빈 칸 hover [+]
- **예약 상세 모달 — 단계 전부**: 예약(변경 · 취소 · 의사 지정 · 동행) → 접수(신분증 확인 · 「시술만 진행」 · 오늘 ✓ · 오더 메모) → 상담 대기(상담사 = KOS 상담 기록 · 관리실 = 방 배정) → 시술 대기 · 진행 → 귀가 대기 → 귀가(작업 취소 뒤 `COMPLETED`). 이전 방문 기록(재진) · 시술 목록 · 수납 정보(원내 현황 금액 + 할인 전 가격) · KOS 웹 딥링크(수납 · 처방)
- **카드 우클릭**: 예약 변경 = 옮기기 모드 끌기 · 예약 취소 · 동행 추가(모달 체크) — 「카드 위에 끌어 놓아 묶기」는 없앰
- **예약 현황 SSE**(10초 폴링 대체) + **쓰기 즉시 확인**(보낸 즉시 KOS 다시 읽기 → SSE `write_confirmed`)
- KOS 데모 지점 **실물 확인 4회**로 쓰기 13종을 연 뒤 스펙을 썼다(reserve · update-reservation · create-visitor · 공개 cancel-reservation · recept · create / change-consultation · 시술권 add-flow-tasks · change-order-memo · CONSULTATION_WAITING · COMPLETED 등)

## 2. 적용한 기술·개념

- **원천에 칸이 있으면 원천에 쓰고 사본은 동기화로 · 없을 때만 우리 DB** → [[external-write-queue]]
  - 상담사 = 예약 칸(`update-reservation counselor`)이 아니라 **KOS 상담 기록**(`create-consultation` · 있으면 `change-consultation-counselors`) — 사용자 HAR 「상담사 지정」으로 바로잡았다. 표 카드 · 원내 현황이 원래 읽던 원천이라 「상담사 미정」 어긋남이 사라졌다.
  - 귀가는 열린 작업이 있으면 KOS 가 400(`procedures NotAvailable`) — 작업 CANCEL 뒤 `COMPLETED` 를 한 묶음으로 계획. `write_open` 은 경로 + 값만, 순서 · 단계 조건은 계획 / 쓰기 큐가 판정.
  - 신분증 확인 · 귀가 사유 · 동행은 KOS 에 칸이 없어 DAY 만.
  - 시술권 오늘 작업 `round.current` = 쓴 + 쓰는 중 + 1 — 다회권 HAR 로 확인. 보낼 때 KOS `get-ticket-bundles` 를 읽어 본문을 채운다(DAY 사본으로 짓지 않음).
- **주기 동기화(받기)와 이벤트 확인(보내기)은 다른 길** → [[polling]] · [[server-sent-events]]
  - 화면이 SSE 여도 확인이 10초 회차를 기다리면 의미가 없다(사용자 「SSE 를 안 하겠다고? 이게 말이냐」). 보낸 즉시 그 일정을 1초 간격으로 다시 읽어 확인 · 상한 넘으면 다음 회차가 이어받음.
  - 단계 바꾸기(`change-flow-step`)만 즉시 확인에서 빠져 10초 늦던 것을 화면 확인 B28 에서 잡았다(outbox `created_at` → `updated_at` 비교).
  - 「바뀐 게 없어도 신호」 → 표 전체를 5 ~ 10초마다 · 한 순간 3 ~ 6번 다시 받아 렉(B41). 보이는 값이 바뀐 때만 신호 + 다시 받기 합침.
  - HTTP/1.1 같은 주소 동시 연결 6개 — 화면 하나가 SSE 2개(알림 + 판)를 열어 탭 여러 개면 새 요청이 대기(B42 · 남음).
- **DAY 사본만 보는 화면의 「데이터 없음」을 코드 버그로 착각하지 않기** → [[input-space-enumeration]]
  - 「재진인데 이전 방문이 없다」 = 오늘 만든 로컬 DB(방문 29건 · 백필 실패) 탓. dev DB 를 로컬로 복사(고객 574 · 방문 1,377 · 암호화 키 dev 값)한 뒤 바로 보였다.
  - 「다 초진」 = KOS 는 귀가 처리 때 「신규 환자」를 지운다 · 데모 데이터를 귀가 처리 없이 만들어 신규로 남았던 것. KOS `isNew` 판정이 맞았다(B5 · B9 · B12 · B13 철회).
- **dev 가 또 앞서 나가 migration 번호를 밀었다** → [[database-migration]]
  - dev #274 · #279 가 `0024_customer_memo` · `0025_visit_photo` → 우리 0024 ~ 0026 을 0026 ~ 0028 로. 충돌은 기능이 아니라 공용 파일(`day.js` 한 파일 · 공용 템플릿 · 쓰기 큐 · 화면 문구 시험)에서 났다 → `day.js` 화면별 분리가 필요(§7).
- **시안 · 원천 · 결정을 「한 기준」으로 먼저 고정하고 칸에 대입** → [[contract-surface-enumeration]]
  - 「KOS 에 칸이 있으면 KOS · 화면은 시안 · 데이터 없는 칸은 빈 값 · 다음 판 동작은 비활성」 — 이걸 처음에 세웠다면 대부분의 질문이 없었다.

## 3. 막혔던 것 / 사고

- **코디가 쓸데없는 질문을 계속 올렸다(사용자 격노 다수).** 자료(시안 · HAR · DB · KOS)로 답이 나오는 것을 칸마다 물었다(SNS 종류 · 초진 판정 · 관리실 표시 등). 원인 = 원칙(KOS 우선 · 시안 우선 · 미완 = 빈 값)을 먼저 세우지 않음.
- **말을 좁게 읽고 엇나갔다.** 「예약부터 귀가까지 하나씩」(구현 순서였는데 논의 순서로 읽음) · 「SSE 로 해」(화면만으로 읽고 KOS 즉시 확인을 다음 스펙으로 미룸) · 「처방은 KOS 에서」(못 한다로 읽음) · 「모아 봐」(고치기까지 넘김) · 「멈춰」(작업을 멈추라는 뜻으로 읽음). 기억 `feedback_doc_pipeline_before_dispatch`(재촉 ≠ 순서 건너뛰기) 보강.
- **순서를 두 번 깼다.** 스펙 검수 중 구현을 나란히 띄웠다가 「스펙 쓰고 순서대로」 → 전부 멈춤. 1판만 끝내고 「화면 확인」을 부탁해 「다 끝내고 말하라고 했지」.
- **사용자가 보는 로컬 스택을 묻지 않고 내렸다**(워커 재시작 요청 · DB 복사 중). 그 사이 KOS 예약이 안 들어왔다.
- **API `--reload` 가 열린 SSE 때문에 멈춤**(워커가 파일을 고칠 때마다). e2e 중에는 워커가 코드를 고치지 않고, 고침은 모아서 끝난 뒤 코디가 재시작.
- **포트 충돌**: 다른 워크트리(day-chart-photo)가 11040 대를 써서 11140 대로.
- **로컬 백필 실패**: KOS 데모 시스템 계정을 dev 서버 · day-chart-photo · 우리 스택이 같이 써서 동시 로그인 한도 → dev DB 복사로 대신.

## 4. 결정

정본 `reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D56) · 화면 확인 `orchestration/work/_archive/day/day-reservation2/e2e-1-feedback.md`(B1 ~ B42).

| 결정 | 왜 |
|---|---|
| 예약 상세 = 시안 v9 · 시술 목록만 코디 와이어(KOS 시술권 카드 모양) | 사용자 「시안대로 · 시술 목록만 바뀜」 |
| 쓰기 = 내부 API 모듈 + 쓰기 큐 · 확인은 데모 실물 | `writes.py` 원칙 · 사용자 |
| 상담사 = KOS 상담 기록 · 초진 / 재진 = KOS `isNew` | 사용자 HAR · KOS 동작 |
| 예약 현황 SSE + 쓰기 즉시 확인(D52 · D53) | 사용자 「10초마다 기다리라고?」 |
| 구현 4판(예약 · 접수 → 상담 · 시술 · 귀가) Delivery #275 ~ #278 | 사용자 「한 번에 못 끝내는 스펙」 |
| 상담 정보 칸 → 바닥 줄 `□시술만 진행 [상담사] [관리실] [접수]` · [예약 취소] = [예약 변경] 옆 | cc-prototype · 사용자 |

## 6. 산출물

- 스펙: MediSolveAIDev/mediness#961(`479d8f46` · `54bbeb14` · `6eba367a`)
- 코드: MediSolveAIDev/CENTURION_DAY#280(`a0b42a36`)
- Delivery: CENTURION_DAY #275 · #276 · #277 · #278
- 조사 · 실물: `research-detail-1-report.md` · `be-probe-1 ~ 4-report.md` · HAR `수납시술추가` · `할인` · `시술권사용` · `상담사 지정`

## 7. 잔여

- **B42 SSE 연결 한도**: 화면 하나 = SSE 하나(알림 + 판 합치기) 또는 운영 HTTP/2 확인
- **`day.js` 화면별 분리**(예약 현황 · 예약 상세 · 시술 현황 · 차트 · 공용) — 이번 rebase 충돌 원인
- 다음 스펙: 문진 QR · 여권 스캔(앱) · 상담사 순번(다음 차례 · 상담중) · 외국인 신분확인
- 세트 여러 개 시술권의 `round.total` · 국가번호 목록(남은 OQ)
- KOS 데모 시스템 계정을 여러 DAY 인스턴스가 같이 씀 → 로컬은 별도 계정 필요

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-reservation2/README|day-reservation2]]
<!-- work-links:end -->
