
# 재개 노트 — day-reservation (day)

**지금**: e2e 2회차 사용자 OK(「잘 된다」) → 코드 커밋 `4b1d1662` · dev 가 `a03b83a4`(#270 · migration 0015 · 0016) 로 나가 be rebase 1 발주(0017 로) · 스펙 R42 정정 `8a0f54e9` push(#958)
**PR**: #272 draft 열림 · 로컬 DB 0014 로 표시 되돌린 뒤 dev 0015 · 0016 + 0017 upgrade · 스택 재기동 정상
**마감 순서(사용자 「합치고 코드 · 문서 · 이슈 · 프로필 다 정리 · 이번 작업 끝」 — 머지 승인)**: ① rebase 2 + check.sh → #272 push · 본문 · ready · 머지 ② planner 21 → 검수 → #958 커밋 · 머지 ③ Delivery #267 ~ #269 재결속(baseline = 머지된 main · scope_delta = addendum · R42 ~ R75) → 30-work ④ 로컬 DB 재정렬 · 스택 내림 · env 사본 지움 ⑤ SUMMARY · archive-work.sh · 개념 · profile PR · **마감 진행(11-24): 코드 2차 커밋 `68a37b87` → rebase 2(dev `b2f28990` · dev 0017_ext_catalog 겹침 → 우리 0018 ~ 0023) · 남은 결정 = #958 · #272 머지 · SPEC-000/002 맞추기 · env 사본 지우기** · **4묶음 진행: E6 카드 배치 + E7 동행 그룹(DAY 전용 새 테이블 · R64 ~ R69 · 계약 v4) + W3-1/2 · 공지 · E4/E5 는 코드 검수 3 PASS(미커밋) · 스펙 ⑨ `039bbfd7`** · **e2e 3회차: E4 상담 미정 · E5 표 카드 담당자(be-feat-2 · fe-feat-2) · 공지 수정하기 + KOS 동기화 조사(cc 는 KOS change-content/create/delete 로 씀) 진행** · **원내 현황 구현 끝 · 코드 검수 2 진행 · 스펙 `12cef6b4` push · 로컬 0018 적용 · 스택 재기동 → 사용자 e2e** · **원내 현황 발주**(사용자 「코드까지 진행해」): 결정 R46 ~ R53 · 계약 `contract-v2-inhouse.md` · planner + be + fe 병렬. 금액 = 병원에 그날 실제 들어오는 돈(수납 = 거래 − 선불카드 차감 · 미수 = 결제 전 잔액 + 수납 필요 옵션가 + VAT · 결제총액 = 합). 이전 메모: **다음 피처 착수**(사용자 「현황탭 카드」): 조사 먼저 — 이번 방문 수납총액 · 결제총액 · 미수총액 + 상담 실장 원천(사용자 용어). 기본값 통보함: 수납 필요 배지 = R42 · 카드 누르기 동작 없음 · 10초 폴링 · SPEC-006 개정(#958) + 코드 #272
**PR 방침**: code PR 하나에 이 작업 전부(다음 피처 원내 현황 · 공지 수정하기까지) 올린다 — 1차 = 조회(사용자 2026-11-23)
**다음**: 사용자 e2e 피드백 모아 한 번에 → 2루프 고침 or 커밋 · code PR(dev) → #958 머지 · Delivery 재결속(scope_delta = addendum 1 ~ 9)

세팅: `scripts/new-work.sh day day-reservation` · 설정 SSOT `config/projects/day.json`
코디handle: `term_d912bb9d-2159-4afe-b544-4e23566d3037`(11-24 Orca 재시작 뒤) · Run `run_3c3bbc2ae3e9`(재시작 뒤 `orca orchestration run-use --id`)

코디 워크트리는 `kknaks_profile/day-ext`(브랜치 `kknaksss/day-ext`) — 사용자가 이 세션을 띄운 곳. 미추적 `reference/2026-11-23-day-ext/` 는 ext 이관(다른 사람 몫) 자료 — 이 작업 PR 에 넣을지는 마감 때 확인

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (branch `kknaksss/day-reservation-spec`, base `origin/main` → PR `main`)

- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` (base `origin/dev` `5ece25ea` → PR `dev`)

## 1. 지금

- [ ] 원내 현황 Delivery: #267 ~ #269 범위 밖(새 화면 · 금액 · R53 매핑) → 재결속 때 scope_delta 또는 새 Issue · 30-work Coverage 갱신 · SPEC-000 transaction status enum(approved · canceled) ↔ R53 어긋남 맞추기(planner-fix-12 미결 1 · 2)

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] reviewer_doc — SPEC-006 1차 검수 → `review-doc-1-report.md`
- [x] planner — SPEC-006 draft(새 파일 + 20-spec · 30-work · 10-decision · log) · 미커밋
- [ ] reviewer_doc 검수 → 사용자 리뷰 → WORK 작성 → backend · frontend
- [x] ~~사용자 확인 모음~~ → 결정 4 ~ 7(`contract-v1-addendum.md`)
- [ ] (옛) 사용자 확인 모음: W-6 정원 null 열 머리 「m분」만 · W-4 날짜 tx ↔ 오늘 회차 행 경합 · 실물 1 배포 뒤 최대 1시간 403(권한 시드가 기준 정보 회차) · 실물 2 꺾쇠 연타 = 날짜별 KOS 최신화 병렬(속도 제한 없음)
- [ ] e2e 피드백(모아서 한 번에 발주): ① 다른 날짜 첫 화면 = 중앙 최신화 끝날 때까지 짧게(최대 3초) 기다린 뒤 그림 ② 날짜 바꾼 뒤 10초 폴링 멈춤 — 버그(05:46:31 · 05:49:49 뒤 요청 0) ③ 수납 필요 원천 = visit_task.payment_required(시술 현황과 같게 · OQ-R15) 추천 — 붙는 단계(접수부터 / 귀가 대기부터) 사용자 답 대기
- [ ] **다음 피처**(이번 e2e 끝난 뒤 · 사용자 2026-11-23): 오른쪽 패널 「원내 현황」 탭 카드(시안 stageCard L1777 — 이름 · 수납 배지 · 단계 · 상담 실장 · 총 합계 / 수납 필요 / 수납 완료) · 공지 날짜 오른쪽 파란 「수정하기」(cc PUT /reservations/notice 처럼 DAY 에만 저장 추천)
- [ ] 2루프 후보: 백엔드 파일 고칠 때 --reload 가 「Waiting for connections to close」에서 멈춤(열린 연결 — SSE 등) · 재기동 때 포트 TIME_WAIT 로 start 가 Address already in use
- [!] 로컬 env: CENTURION_DAY/day-reservation/deploy/local.env · kos-demo.env(0600 · gitignored · 메인 local.env 를 둘로 나눔) — archive 전에 지우거나 옮길 곳 확인(워크트리째 지워짐) · 스택 내림(./stop.sh) 확인
- [!] 범위 = 조회만(표 + 오른쪽 공지 / 예약 요청 자리). 상세 모달 · 예약 요청 내용 · 앱으로 보내기(여권 · 전후 사진 · 문진)는 뒤 단계 — 전후 사진은 cc 에도 없음(새로 설계)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-23 | 예약 현황 조회 결정 R1 ~ R16 · 열린 것 O1 · O2 | 정본 `reference/2026-11-23-reservation/reservation-board-decisions.md` (사용자 대화) |
| 2026-11-23 | researcher 단계 건너뜀 — 표 데이터가 DB 에 다 있어 SPEC 으로 바로 | 사용자 승인 |
| 2026-11-23 | **R17 날짜 이동 동작 · 흐름 KOS → DAY → DB(보는 날짜를 KOS 에서 최신화) · R18 선동기화 안 함 · R19 동기화 멈춤 표시 = OQ · R20 그룹 없는 방문 없음** — 코디 브리프의 「조회 부작용 없음(KOS 호출 금지)」은 코디 잘못으로 취소 | 사용자 (1차 검수 F-1 · W-2 · W-3 뒤) |
| 2026-11-23 | R26 보는 날짜 최신화 = 오늘 동기화와 같은 범위(일정 + 구매 · 시술권 · 카드) · R27 날짜 잠금 따로 · 받는 중이면 사본으로(OQ-R24 · R25 닫음) — 2차 검수 결과와 함께 planner 고침 2 에 넣을 것 | 사용자 |
| 2026-11-23 | 날짜 최신화 조건 C1 완성된 상태만 보임 · C2 조용히 건너뛰지 않음 · C3 구매도 그 날짜 것 · C4(OQ-R28 기본안) 세 단계 다 받고 그림 · 실패면 이전 사본 — SPEC 은 조건만, 함수 설계는 WORK | 코디(3차 검수 F3-1 · F3-2 뒤) · C4 는 사용자 확인 대기 |
| 2026-11-23 | **R29 갱신 = 중앙 한 번 최신화(보는 중인 날짜만 · 병원 · 날짜당 한 번) · PC 는 DB 만** · R30 실패 = 이전 사본 · R31 권한 = 모든 직원 · board 방식 키 · R32 요청 칸 = 제목만 · R33 나머지 OQ 기본안(R06 cc 문구 제외 · R03 ⓑ 코디 기본) | 사용자(R29 = 사용자 제안 「중앙 하나에서 최신화」) |
| 2026-11-23 | **R39 동기화 = 서버 중앙 작업만(쓰는 쪽 하나)** · 화면 요청은 「보는 중」 + 먼저 요청만 · R29 첫 열기 즉시 최신화 · C4 뒤집음 | 사용자 「동기화는 서버에서만 — 충돌 안 남」 |
| 2026-11-23 | **R40 10초 동기화 = 오늘만 · 다른 날짜 = 열 때 중앙에 1회 요청 → 저장 · (병원 · 날짜) 잠금 · 주기 재최신화 없음(부하)** — R29 보는 중 · 만료 · 주기 뒤집음 · OQ-R34 · R35 · R37 닫음 | 사용자 |
| 2026-11-23 | **SPEC-006 승인** · R41 OQ-R36 폴링(DB 만) · OQ-R38 ⓐ · spec PR 발행 승인 | 사용자 |
| 2026-11-23 | **#958 머지하지 않는다** — 최초 스펙이라 Delivery 는 main SHA + spec-baseline:pending 으로 시작 · Delivery 승인은 사용자가 함 · 코디의 스쿼시 머지 시도는 사용자 거절 | 사용자 「병합하지 말고 하라고 · 최초 스펙이라 그렇게 해야해」 |
| 2026-11-23 | **구현 먼저 · #958 머지는 구현 끝난 뒤** — spec-baseline:pending 상태로 코드 착수 | 사용자 「머지는 구현 끝나고 한다고!」 |
| 2026-11-23 | 계약 V1 보충 — today · open_min · axis.time_gray_spans[](판정 ① backend) · 컨텍스트 이름 = 계약 이름 최상위 · fe 가 test_screen_copy.py 에 시안 문구만 추가 허용 → `contract-v1-addendum.md` · Delivery 재결속 때 scope_delta 로 실을 것 | 코디(fe 질문) |
| 2026-11-23 | 코드 검수 뒤 결정: 행 경합 = 날짜 쪽 양보 · ~~권한 시드 = 서버 시작 때~~ → 권한 행 = 데이터 migration(addendum 9 · 사용자 「마이그레이션 해주면 되는 문제」 · 브리프 migration 금지는 코디 잘못) · 꺾쇠 연타 막음(화면 debounce + ~~병원당 날짜 최신화 1개~~ → 잠금 전에 Redis 10초 캐시 · addendum 8 — 사용자 「레디스 10초 캐싱 · 락 걸기 전에」) · 정원 null = 「30분」만 | 사용자 |
| 2026-11-23 | R42 수납 필요 = 귀가 대기 ∧ visit_task.payment_required · R43 첫 화면 최대 3초 기다림 · e2e 고침과 스펙 개정 병렬(사용자 「수정해」) | 사용자 |
| 2026-11-23 | **R42 정정 — 수납 필요 = 단계 무관 · payment_required 하나라도**(KOS 는 수납필요 남으면 귀가 대기로 못 넘어감 → 귀가 대기 조건은 참이 될 수 없음) · be 고침 4 · planner R42 정정 발주 | 사용자 |
| 2026-11-23 | 원내 현황 탭 · 공지 수정하기 = 이번 e2e 끝난 뒤 다음 피처 | 사용자 |
| 2026-11-23 | 시안은 디자인 참고(생김새 · 문구 정본), 동작은 결정 > 시안 > cc | 사용자 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

⚠ 2026-11-24 Orca 재시작으로 planner · backend · reviewer · reviewer_doc 터미널 사라짐 — 다음 발주 때 새로 만들고 브리프 머리에 「앞 리포트 먼저 읽기」

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_32c495fd-8360-4e2c-99f1-c2d248162907`(11-24 새) | `task_3a44a294d8e4` | `ctx_eff8a3258092` | `planner-fix-21-instructions.md` | 마감: SPEC-006 R73 ~ R75 · migration 번호 · SPEC-000 / 002 맞추기 진행 |
| backend | `term_79a67d5c-d6dd-4a1e-91ac-4a61eacc88b0`(11-24 새) | `task_85b8ff71bb66` | `ctx_49bb7ef52d7d` | `be-rebase-2-instructions.md` | dev #271 · #273 위 rebase · migration 0018 ~ 0023 · 전체 check.sh 진행 |
| frontend | `term_a7b01ec8-b518-4fca-8dd6-74a7b7033158`(11-24 새 터미널) | `task_5c28ffbc427d` | `ctx_5fb91985241c` | `fe-feat-5-fix-2-instructions.md` | R75 꼬리표 · 행 여백 없앰 진행 |
| reviewer(code) | `term_096158dd-fa56-4eed-b30b-56b5c89f4097` | `task_6a91109ca83a` | `ctx_82418f6e6541` | `review-code-2-instructions.md` | 원내 현황 코드 검수 진행 |
| reviewer_doc | `term_608f78e2-e84c-40c0-929b-467d1bb5d971` | `task_ff5f480fbfd7` | `ctx_c88f5ae83a73` | `review-doc-7-instructions.md` | 7차 FAIL 2 · WARN 6 완료 · retain |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/958 (`1870f68c` · 머지 전)
- Delivery: CENTURION_DAY#267 · #268 · #269 (L2 · approved · spec-baseline:pending)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/272 (draft · 1차 조회 `431c081b` · dev `a03b83a4` 위 · migration 0017)
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-23` e2e 1회차 → fe · be 고침 3 · 개정 ⑦(#958 079437fc) · 코디 757 + node 17 passed · 스택 재기동
- `2026-11-23` be · fe 고침 2 완료 · 코디 563 passed · env 나눔 · 로컬 스택 --kos-demo 기동 · e2e 대기
- `2026-11-23` reviewer(code) WARN(FAIL 1 · WARN 6) → fe · be 고침 1 병렬
- `2026-11-23` be #268 완료 · 코디 관문 350 passed · reviewer(code) 발주
- `2026-11-23` be #267 끝(24 passed) · fe #269 완료(12 passed · 코디 재실행 확인) · be #268 진행
- `2026-11-23` Delivery v2 재결속 · 재승인(poll=1 · task 입구 · V0 ~ V4) → backend · frontend 병렬 발주
- `2026-11-23` Delivery 검수 FAIL 4 · WARN 6(`review-delivery-1-report.md`) → planner 재결속 발주
- `2026-11-23` Delivery #267 · #268 · #269 발행 · 승인 · #958 에 Coverage 커밋 34c99b25 · reviewer_doc Delivery 검수 발주
- `2026-11-23` Delivery --plan conflict(baseline 1870f68c ≠ origin/main) · WP 3(be-read · be-refresh · fe) request 준비 · `delivery-1-report.md`
- `2026-11-23` 고침 9(승인 · stable) · spec 커밋 `1870f68c` · PR #958 · CENTURION_DAY 워크트리(be · fe 브리프 자리) · planner Delivery 발주
- `2026-11-23` planner 고침 7 · 8 완료(lint 0 · S6:306 R40 확인) → 사용자 승인 대기
- `2026-11-23` 6차 FAIL 1 · WARN 3(`review-doc-6-report.md`) → planner 고침 7
- `2026-11-23` planner 고침 6(R40) 완료 · reviewer_doc 6차 발주
- `2026-11-23` planner 고침 5 완료(R39 잔존 0) · 사용자 R40 → planner 고침 6 발주
- `2026-11-23` 5차 검수 FAIL 1 · WARN 5(`review-doc-5-report.md`) → planner 고침 5 발주
- `2026-11-23` planner 고침 4b(R39) 완료(lint 0) · reviewer_doc 5차 발주
- `2026-11-23` planner 고침 4 완료(R29 ~ R33 · 남은 OQ-R34 ~ R38) · R39 추가 지시(같은 터미널 · 번호 겹침으로 R34 → R39 정정)
- `2026-11-23` 4차 검수 WARN 3(`review-doc-4-report.md`) → 사용자 R29 ~ R33 → planner 고침 4 발주
- `2026-11-23` planner 고침 3 완료(lint 0) · reviewer_doc 4차 발주
- `2026-11-23` 3차 검수 FAIL 2 · WARN 3(`review-doc-3-report.md`) → planner 고침 3 발주
- `2026-11-23` planner 고침 2 완료(lint 0) · reviewer_doc 3차 발주
- `2026-11-23` 2차 검수 FAIL 1 · WARN 5(`review-doc-2-report.md`) → planner 고침 2 발주
- `2026-11-23` planner 고침 1 완료(lint 0) · reviewer_doc 2차 발주
- `2026-11-23` 1차 검수 FAIL 1 · WARN 9(`review-doc-1-report.md`) → 사용자 R17 ~ R20 → planner 고침 1 발주
- `2026-11-23` planner 완료(SPEC-006 draft · lint 0 error) · reviewer_doc 발주
- `2026-11-23` slug 세움 · 결정 파일 작성 · Run 생성 · planner 발주(terminal create → worker-start --terminal)

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
