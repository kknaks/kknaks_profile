# 작업 요약 — day-reservation (day)

기간: `2026-11-23` ~ `2026-11-24`
결과: DAY 웹 예약 현황 끝 · dev 배포까지(`4bf0b4a1` · migration 0018 ~ 0023 적용). 스펙 mediness #958 → main `32b83390`(SPEC-006 개정 ① ~ ⑪ · SPEC-000 · SPEC-002 ㉗). 코드 CENTURION_DAY #272(dev 대상 · 커밋 3 · migration 0018 ~ 0023 · 전체 check.sh 2584 passed). Delivery #267 ~ #269 재결속(머지된 main 기준). dev 배포 · prod 는 다음(§7).

## 1. 무엇을 했나

시안(`20261113_예약현황_시연`)을 디자인 참고로, 동작은 사용자 결정으로 만들었다. 처음엔 「조회만」이었는데 e2e 를 돌며 범위가 다섯 덩이로 커졌다.

- **조회**: 예약 그룹 열 · 병원 예약 설정 간격 시간 축 · 내원 단계 7색 · 신규 · 국적 · 수납 필요. 오늘은 기존 10초 동기화, 다른 날짜는 열 때 중앙 서버가 KOS 에서 한 번 최신화(Redis 10초 캐시 → (병원 · 날짜) 잠금). 첫 화면은 최대 3초 기다린 뒤 이전 사본.
- **원내 현황 탭**: 오늘 원내 카드 · 칩 · 상담 실장 · 결제총액 / 수납 / 미수.
- **공지 「수정하기」 + KOS 동기화**: 누른 직원 KOS 토큰으로 직접 쓰기(create / change / delete) · KOS → DAY 공지 동기화를 새로.
- **표 카드**: 담당자 줄(상담사 / 담당의 · 미정) · 폭 140 · 한 줄 고정 · 30분 행 한 줄 5장 넘으면 아래 줄.
- **동행 그룹(DAY 전용)**: 같은 열 · 같은 30분 행 카드를 끌어 겹쳐 놓아 묶기 · 새 테이블 두 개 · 파란 테두리 띠.

## 2. 적용한 기술·개념

- **「보는 날짜 최신화」를 화면 요청이 아니라 중앙 작업 하나로 — 잠금 전에 캐시** → [[distributed-lock]] · [[database-lock]]
  - 처음 브리프는 「조회 경로에서 KOS 호출 금지」였다(코디 잘못). 사용자: 흐름은 KOS → DAY → DB, 그 날짜 원본도 KOS 다.
  - 「PC 마다 KOS 를 부르면 충돌」 → 사용자: 「동기화는 서버에서만 하면 충돌 안 남」(R39). 오늘은 10초 회차, 다른 날짜는 열 때 중앙에 한 번(R40) · 주기 재최신화 없음(부하).
  - 꺾쇠 연타가 같은 날짜를 여러 번 넣는 문제 → 사용자 제안 「레디스 10초 캐싱 · 락 걸기 전에」. 잠금보다 앞에서 거르니 잠금 경쟁 자체가 줄었다.
  - 오늘 10초 회차와 날짜 최신화가 같은 행을 잡으면 **날짜 쪽이 양보**(`lock_timeout` 1500ms) — 오늘 화면이 우선.
- **10초 폴링 화면에서 사람이 손대는 칸 지키기** → [[polling]]
  - 날짜를 바꾸면 폴링이 멈추는 버그(요청 출처가 둘) → day.js 시계 하나 · 요청 출처 고정.
  - 공지 편집 중 · 카드 끄는 중에는 폴링이 그 칸을 덮지 않게, 목록 스크롤 · 칩 가로 위치는 조각을 끼운 뒤 되살렸다. 쓰기 응답은 「세대」를 올려 늦게 온 옛 폴링이 덮지 못하게 했다.
- **돈의 정의는 「그날 실제로 들어온 돈」 하나로 — DB 를 열 때마다 말하지 않는다** → [[input-space-enumeration]] · [[derived-predicate]]
  - 수납 = 거래 합(선불카드 · 예전 시술권 차감 제외 — 이미 받은 돈) · 미수 = 결제 전 수납 건 남은 돈 + 수납 필요 시술의 옵션가(+ 진료항목 과세면 VAT) · 결제총액 = 수납 + 미수.
  - 미수 ⓑ 는 KOS 수납 창이 「+ 추가」 때 하는 계산(옵션가 + VAT)과 같다. 수납 건이 생기면 실제 금액(할인 · 수정)으로 대신한다.
  - 결제 뒤 `payment_required` 가 한 회차 늦게 꺼지는 표본이 실제로 있어 「같은 옵션이 이번 방문 수납 건에 있으면(상태 무관) ⓑ 에서 뺌」(R54)으로 이중 셈을 막았다.
  - 사용자 HAR 두 개(추가 수납)가 KOS 흐름(initialize → add-pending → register → add-transaction → accept)을 그대로 보여 줘 정의를 고정할 수 있었다.
- **방문 단위 쓰기 큐에 안 맞는 쓰기는 직접 호출 · 외부 id 는 매핑 테이블** → [[external-write-queue]] · [[external-id-mapping-table]]
  - 공지는 방문이 없어 `external_outbox`(visit_id NOT NULL · 일정 동기화로 확인)에 못 태운다. create 의 새 id 도 받아야 한다 → 로그인처럼 요청 안 직접 호출(R59).
  - KOS 공지 id 는 `notice` 칸이 아니라 `external_ref(entity_type='notice')`. 저장 대상은 「화면이 보인 공지의 KOS id 가 다시 읽은 목록에 있으면 그것」(R62) — 계약에 `notice.id` 가 빠진 것을 검수가 잡았다.
  - 공지 동기화 실패는 일정 회차와 savepoint 로 떼어 시술 현황판에 번지지 않게 했다(R62 · W3-1).
- **dev 가 두 번 앞서 나가 migration 번호를 두 번 밀었다 · 권한 행은 데이터 migration** → [[database-migration]]
  - 1차: dev #270 의 0015 · 0016 과 겹쳐 0015 → 0017. 2차: dev #273 의 `0017_ext_catalog` 와 겹쳐 0017 ~ 0022 → 0018 ~ 0023. 로컬 DB 는 옛 번호에 서 있어 `alembic_version` 을 공통 조상으로 되돌린 뒤 다시 올렸다.
  - 「배포 직후 예약 현황 403」: 권한 행 시드가 시간 회차 · 로그인 때만 돌았다. 사용자: 「마이그레이션 해주면 되는 문제」 → alembic 데이터 migration(`ON CONFLICT DO NOTHING`). 브리프가 migration 을 막아 둔 것이 코디 잘못.
  - 거래 상태 enum 은 PG enum 이라 값 추가 migration 이 반드시 필요했다(검수 W7-5).
- **화면 배치는 서버가 줄 · 자리까지 정하고 화면은 그리기만** → [[contract-surface-enumeration]]
  - 「한 줄 5장 넘으면 아래 줄」을 넣자 카드 높이(시작 ~ 끝)와 줄 접기가 충돌했다(검수 F11-2) → 카드 한 줄 고정 높이(R70). 동행 「같은 시간대」를 열 간격 칸으로 두면 60분 열에서 그룹이 30분 행 둘에 걸쳤다(F11-3) → 배치와 같은 30분 행(R71).
  - 동행 묶기 서버 검사가 끈 카드 날짜만 봐서 손으로 만든 요청이면 다른 날 카드끼리 묶였다(코드 검수 F4-1) — 두 카드 다 검사.

## 3. 막혔던 것 / 사고

- **수납 · 미수에서 코디가 말을 계속 바꿨다(사용자 격노).** DB 를 열 때마다 「미수 모름」 → 「있음」, 220,000 → 110,000(옵션 하나에 구성 2줄), 선불카드 결제 포함 → 제외 → 포함. 원인은 「돈이 언제 실제로 들어오나」라는 기준 하나를 먼저 잡지 않고, 옵션 과세 칸이 비자 진료항목(`treatment_item.taxation`)까지 안 보고 「모른다」고 한 것. 기억 `feedback_day_payment_cash_inflow` 로 남겼다.
- **「수납 필요」 붙는 단계를 두 번 오독했다.** 귀가 대기부터 → 사용자 「단계 상관없이」. KOS 는 수납 필요가 남으면 귀가 대기로 못 넘어가므로 귀가 대기 조건은 참이 될 수 없었다.
- **스펙 PR 을 승인 = 머지로 읽고 스쿼시 머지를 시도했다.** 사용자 「병합하지 말고 · 최초 스펙이라」 → Delivery 는 main SHA + `spec-baseline:pending` 으로 시작, 구현 뒤 머지. 기억 `feedback_first_spec_pending_baseline`.
- **스택 재기동이 자꾸 막혔다.** API `--reload` 가 열린 연결에서 「Waiting for connections to close」로 멈추고, 재기동하면 TIME_WAIT 로 Address already in use. 포트 bind 시험 루프로 기다린 뒤 띄웠다.
- **Orca 재시작으로 워커 터미널이 전부 사라졌다(11-24).** 발주가 `inject_rejected`. 새 터미널을 만들고 브리프 머리에 「앞 리포트 먼저 읽기 · 절대 경로」를 넣어 이었다. 「이 폴더」 같은 상대 표현은 새 워커가 못 찾았다.
- **워커 질문(ask)을 늦게 봤다.** 하트비트 사이에 섞인 question 을 바로 못 보고 rebase 2 워커가 10분 넘게 기다렸다.
- **KOS 로그인 기기 한도로 공지 쓰기 실물 1회를 워커가 못 했다**(`SignInLimitExceeded`). 우회하지 않고 사용자 e2e 로 넘겼다.
- **rebase 2 에서 기존 실패 6건이 드러났다** — 동행 테이블 등록 빠짐 3 · 정형 검증 기준값 3(visit_task 인덱스 · load_world 분리). 해시만 바꾸지 않고 TLC 8 사례 · 실 PG 대조 · Lean 절차로 맞췄다.

## 4. 결정

정본은 작업 폴더 `reference/2026-11-23-reservation/reservation-board-decisions.md`(R1 ~ R75). 큰 줄기만:

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-23 | 흐름 KOS → DAY → DB · 동기화는 서버 중앙 작업만(R39) · 10초는 오늘만 · 다른 날짜는 열 때 한 번 + 잠금(R40) | 사용자 |
| 2026-11-23 | 잠금 전 Redis 10초 캐시 · 날짜 쪽 양보 · 첫 화면 최대 3초 | 사용자 |
| 2026-11-23 | 권한 행 = alembic 데이터 migration | 사용자 |
| 2026-11-23 | 수납 필요 = 단계 무관 `payment_required`(R42) | 사용자 |
| 2026-11-23 | 금액 = 병원에 그날 실제 들어오는 돈(R49 ~ R54) | 사용자 |
| 2026-11-23 | 공지 수정 = 직원 토큰 직접 쓰기 · KOS → DAY 공지 동기화 · 오늘 · 앞날만(R58 ~ R62) | 사용자 승인(기본값) |
| 2026-11-23 | 카드 폭 줄임 · 한 줄 5장 넘으면 아래 줄(R64) · 한 줄 고정 높이 · 같은 30분 행(R70 · R71) | 사용자 / 코디 |
| 2026-11-23 | 동행 그룹 = DAY 전용 새 테이블 · 겹쳐 놓아 묶기 · 지난 날 막음(R65 ~ R69) | 사용자 |
| 2026-11-24 | 동행 띠 = 진한 파랑 테두리만(글자 · 탭 없음 · 행 여백 없음 — R75) | 사용자 「이거 때문에 시간 다 밀림」 |
| 2026-11-24 | #958 · #272 머지 · 이번 작업 끝 | 사용자 |

## 5. 날짜별 로그

- `2026-11-23` 위치 확인 · 결정 R1 ~ R45 · SPEC-006 · 문서 검수 6회 · Delivery #267 ~ #269(pending) · 1차 코드 · 코드 검수 · rebase 1(0017) · e2e 1 · 2회차 · PR #272(draft) · 원내 현황 조사 · 금액 정의(HAR 두 개 · 데모 실측) · 개정 ⑧ ~ ⑩ · 공지 · 동행 · 배치 코드 · 코드 검수 2 ~ 4
- `2026-11-24` 동행 띠(R72 ~ R75) · 2차 커밋 · rebase 2(0018 ~ 0023 · 정형 검증 동기화) · 전체 check.sh 녹색 · 개정 ⑪ · SPEC-000 · SPEC-002 · #958 머지 · Delivery 재결속 · 회고 · 개념 · 아카이브

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.

- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/272 (dev 스쿼시 `4bf0b4a1` · dev 배포 success · DB `0023_companion_permission (head)`)
- 30-work PR: https://github.com/MediSolveAIDev/mediness/pull/959
- spec PR: https://github.com/MediSolveAIDev/mediness/pull/958 (main `32b83390`)
- Delivery: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/267 · #268 · #269
- 결정 정본: `reference/2026-11-23-reservation/reservation-board-decisions.md` · 계약 `contract-v1-addendum.md` · `contract-v2-inhouse.md` · `contract-v3-notice.md` · `contract-v4-companion.md`
- `kknaksss/day-reservation-close` → `main`
  - `e20fc215` docs(day): Delivery #267 · #268 · #269 재결속 — 30-work Spec Coverage · log
- `kknaksss/day-reservation` → `dev`
  - `85836b30` chore: 정형 검증 동기화 — 예약 현황 2차의 load_world 분리 · visit_task 인덱스 · 공지 참조 반영
  - `0328b1aa` feat: 예약 현황 2차 — 원내 현황 탭 · 담당자 줄 · 공지 수정 + KOS 동기화 · 카드 배치 · 동행 그룹 (DAY-SPEC-006 개정 ⑧ ~ ⑩)
  - `a08f1a0b` feat: 예약 현황 조회(웹) — 예약 표 · 공지 / 예약 요청 패널 · 다른 날짜 중앙 최신화 (DAY-SPEC-006)
- 리포트(이 작업 폴더): 조사 `research-payment-1` · `research-notice-1` · `research-companion-1` · 문서 검수 `review-doc-1` ~ `13` · 코드 검수 `review-code-1` ~ `4` · `be-*` · `fe-*` · `planner-*` · `delivery-*`

## 7. 잔여

- **dev 실물 확인**: dev 배포 됨(2026-11-24 · health OK · DB head 0023). 직원 토큰 공지 KOS 쓰기 실물 1회는 아직(로컬은 KOS 로그인 기기 한도).
- **Delivery spec-sync**: 세 Issue `implementation:conformant · spec-sync:pending`. 막힘 ① harness 가 PR 하나에 review 마커 하나라 #267 · #268 evidence stale(1 Delivery = 1 PR 밖) ② mediness 메인 체크아웃의 옛 로컬 브랜치 `mediness`(2026-07)가 `mediness/delivery-N-spec` 이름을 막음 → 사용자 판단 뒤 spec-sync · Issue close.
- **prod**: `vm-deploy.sh migrate prod`(dev 에 같은 revision 뒤) → deploy-prod.
- **동행 실패 알림 문구**: 비어 있음(빈 문구 = 토스트 없음 · 카드만 제자리). 사용자 문구 받으면 `board_messages` 에.
- **원내 현황 「수납 완료」 배지**: 시안대로 둠(사용자 「일단 두자」) — 실사용 뒤 다시 볼 것.
- **2루프 후보**: 동기화 멈춤 표시(OQ-R21) · `--reload` 가 열린 연결에서 멈춤 · 재기동 TIME_WAIT · 공지 「고친 직원 · 시각」(KOS 칸 없음) · 결제 수단 PLATFORM · EASY_PAY · MEDICAL_LOAN 표본 확인.
- **문서**: `40-architecture/erd.md` 에 동행 테이블 두 개 없음 · `models/companion.py` docstring 「같은 시작 칸」 → 30분 행(검수 13 W13-3).
- 상세 모달 · 예약 요청 내용 · 앱으로 보내기(여권 · 전후 사진 · 문진) · 끌어 놓기로 예약 옮기기는 다음 스펙.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-reservation/README|day-reservation]]
<!-- work-links:end -->
