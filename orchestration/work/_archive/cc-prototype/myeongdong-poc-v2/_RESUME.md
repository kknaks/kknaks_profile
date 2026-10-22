# 재개 노트 — myeongdong-poc-v2 (cc-prototype)

**지금**: 배포 완료(ccc.medisolveai.xyz = procedure) · TestFlight 빌드 1 처리 대기 → 사용자 실기기 E2E(아이폰 · 아이패드 · 워치). 그 뒤 로그인 접근 제한(OQ-601) · 문서 PR · 마감
**다음**: [WP1 완료] 오면 frontend 발주 → backend WP4 · frontend 완료 → reviewer → 수정 → 코디 로컬 확인 → 사용자 로컬 E2E. (코드 워크트리 `orca/workspaces/cc-prototype/myeongdong-poc-v2`) (`new-work.sh cc-prototype myeongdong-poc-v2 --workers backend,frontend`) → reviewer → 수정 → 사용자 로컬 E2E → infra · 배포 · `_archive/cc`

세팅: `scripts/new-work.sh cc-prototype myeongdong-poc-v2` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de`

## 워크트리

- 문서(코디): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` · 브랜치 `kknaksss/명동-POC-v2` (slug 는 kebab 규칙 때문에 영문)
- 코드: 아직 없음(`kknaksss/cc-prototype` main `339293e` = 2차)
- 참고(read-only): `/Users/kknaks/git/ax-clinic-project` — 명동 인터뷰(10-16 6건, 브랜치 `kknaksss/명동인터뷰1` → 사용자가 머지 지시) · KOS 키 · 사용법 메인

## 1. 지금

- [ ] `kos-demo-api.md` §6 정할 것 9건 — v2 흐름 정할 때 같이
- [~] 시안 1단계 — v1 반려(배포 현황판과 구조 · 테마 · 글자 · 카드 다름) → r2 `Ceramique 시술현황판 v2.dc.html` 제작 중. **기준 = 배포 코드 `cc/front`(옛 시안 아님)**. 10-21 사용자가 claude design 에서 직접 고침 → 워커가 읽어 정책 후보 정리 → 사용자와 정책(DEC-005) 다음: 시안 보고 DEC-005 → SPEC-003(2차처럼 시안이 정본)
- [ ] DEC-005(시술 현황판 · KOS 데모 지점 실연동) — DEC-002 D-10 · OQ-208, DEC-004 D-18 「KOS 호출 안 함」을 대체
- [!] profile 레포는 public — KOS 키 값 · 토큰 · 실명 금지. 키 값은 ax-clinic-project(private) `scripts/.env` 에만
- [ ] HAR 미확인: 「특정 의사 선택」 호출(`doctorIds` 붙나) · 지정 원장 변경
- [ ] **시술 차트(보류 · 사용자 고민 중)** — KOS 간호관리차트 = `tasks[].assigneeMemo` · 의사차트 = `doctorMemo` · 시술 메모 = `memo`(데모 99작업 대조로 확인, 읽기 가능 · 쓰기 공개 API 없음). 현장에서 바로바로 쓰는 구조가 아니라 v2 범위 여부 미정. 정하면 저장 HAR 필요
- [ ] KOS 반영 방식(공개만 / 내부 API 까지 / KOS 요청) 결정 — 호출 · 수락은 내부 API 만
- [!] `kos-screenshot/` 은 untracked(ignore 아님) — 미러링 안 함, 필요하면 사용자에게

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-20 | 명동 PoC v2 = cc-prototype 의 다음 차수. 시술 현황판 | 사용자 — 10-16 인터뷰에서 시술 현황판 필요 |
| 2026-10-20 | 기존 `workflow.md` = v1(사용자가 생각한 것), 인터뷰 실제 문제점 = v2 | 사용자 |
| 2026-10-20 | KOS 는 데모 지점에 실제로 붙여 테스트 — 운영 호스트 `open-api.kos-solution.com` + `KOS_API_tenent_dev`. `.dev` 서버 아님 · 운영 명동점 키 금지 | 사용자 「이걸로 할거야」 · 코디 토큰 교환 · getZones/getAccounts 확인 |
| 2026-10-20 | KOS 키 값 · 사용법 메인 참고처 = ax-clinic-project. profile 엔 옮기지 않고 가리킨다 | 사용자 · profile public / ax-clinic private |
| 2026-10-20 | 데모 접속 정보 · API 는 baseline 이 아니라 `reference/2026-10-12-cc-prototype/kos-demo-api.md` | 사용자 「참고용으로 모아 둘 것」 |
| 2026-10-20 | `cc-prototype.json` 에 `repos.reference` = ax-clinic-project(read-only) | 사용자 |
| 2026-10-20 | v2 시작 상태 = 수납 끝난 일정(시술 대기). 데모 오늘 일정 2(작업 3 · 시작 전 · 결제 필요 · 시술권 없음 · 방/담당 없음 · `orderMemo` 있음)가 그 예 | 사용자 「이게 시술현황의 시작 상태」 · 코디 조회 |
| 2026-10-20 | 시술 현황판 = 어느 방에 누가(고객) 들어갔고, 시술과 메모를 보여 준다 | 사용자 |
| 2026-10-20 | 마취 타이머: [마취 시작] → 「마취 중 00분 경과 [마취 종료]」. 일정(고객) 단위, 여러 회차 가능(동시 진행 1개), 회차는 시술에 묶지 않는다. 시각은 우리 DB(KOS 일정 id 덧씌움) — KOS 「마취용」 가짜 계정 우회를 대체 | 사용자 「현장상황에 초점 · 굳이 묶을 필요 없어」 · 인터뷰(대표원장 16:56~17:42 · 간호사 05:06) |
| 2026-10-20 | KOS 직원 · 담당자 표시에서 `마취용` 계정은 뺀다 | 대표원장 인터뷰 · 데모 getAccounts |
| 2026-10-20 | 시술 준비(약물 · 장비)는 현황판에 표시하지 않는다 | 사용자 |
| 2026-10-20 | 원장 호출은 우리 앱에서 — KOS 와 같은 구조로 [전체 호출] · [특정 의사 선택]. 전체 = 원장 쪽에서 콜을 잡은 사람이 집도의 · 특정 = 지정된 원장이 승인 | 사용자 · 간호팀 부팀장 인터뷰 20:13 · 28:17 |
| 2026-10-20 | ~~시술 진행 = 원장이 콜을 잡은(승인한) 때~~ → 같은 날 뒤집음: **첫 시술 [시작] = 시술 진행** | 사용자 · 간호팀 부팀장 24:26 → 사용자 「원장 호출 콜로 판단하는 게 아니라 첫 시술 시작 버튼으로」 |
| 2026-10-20 | 모바일 앱 전까지 원장 쪽 = 기존 `/staff`(내 스케쥴 · 배정형) 위에 「들어온 콜」 칸 추가([콜 잡기] · [승인]) — 기존 화면 무변경(DEC-004 D-21) | 사용자 「일단 그렇게 가자」 |
| 2026-10-20 | 시술 진행 중에는 화면 · 컴퓨터를 조작하지 않는다 | 사용자 |
| 2026-10-20 | ~~원장 수락 한 번에 KOS 두 층을 같이 — `change-tasks-doctors` + `changeFlowStep(PROCEDURE)`~~ → 같은 날 뒤집음: `changeFlowStep(PROCEDURE)` 는 **첫 시술 [시작]** 때. KOS 의 별도 [시술 진행] 버튼은 여전히 우리 앱에 없다 | 사용자 「그렇게 가면 될거 같아」 → 「첫 시술 시작 버튼으로」 |
| 2026-10-20 | 상태 두 층: 일정 = 「시술 진행」 하나, 그 안에서 시술마다 진행 · 대기(· 완료) 구분 — 예: 시술1 진행 · 시술2 대기 | 사용자 |
| 2026-10-20 | 화면은 직원(직군) 중심이 아니라 **고객 중심** — 고객 아래 시술마다 [시작] · [종료], 순서는 현장이 정한다(아무 시술이나 시작). [종료] = KOS `change-tasks-complete`(그 작업) · [시작] = 우리 DB | 사용자 「고객중심으로 짜야 하지 않을까」 · 부팀장 06:07 · 10:07 |
| 2026-10-20 | **화면 분할(핵심: 시술실 안에서 시술을 제어)** — ① 간호 스테이션 PC = 시술 현황판: 전체 조회 + 제어는 **시술 시작 전(마취 · 의사 호출)과 귀가(대기)만** ② 시술실 태블릿 · 폰(일단 웹) = 그 고객의 시술마다 [시작] · [종료] + 마취 [시작] · [종료]. 시술 여러 개 동안은 여기서만 제어 ③ 원장 = 콜 수락 → 시술실로 이동. 모든 시술 종료 뒤 **귀가 대기는 현황판에서** 누른다 | 사용자 |
| 2026-10-20 | KOS ↔ ccc 는 계속 동기화한다(양방향) | 사용자 |
| 2026-10-20 | 화면 3개 — ① **시술실 고객 모니터**(방마다 1대 · 국가별 언어 · 지금 상담/시술 어디인지) = **다음 버전** ② **시술 태블릿 · 폰** = 직원 제어 ③ **시술 현황** = 간호 스테이션 조회. 원장은 의국에서 쉬다 콜 받고 시술실로 온다 | 사용자 |
| 2026-10-20 | 시술 태블릿 · 폰 = **개인 계정 로그인**(방 고정 기기 아님) — 로그인 뒤 고객(방)을 골라 제어 | 사용자 |
| 2026-10-20 | 태블릿 · 폰 고객 목록 = **전체 고객**(내 담당만 아님) — 어시팀이 서로 돕고, KOS 담당자 칸은 실제 어시가 아니다 | 사용자 「전체 고객으로 시작」 · 부팀장 04:02 · 16:34 |
| 2026-10-20 | KOS 쪽은 **시스템 계정 1개**(관리자 권한)로 ccc 가 로그인해 제어 — 의사 호출 전 담당자 지정 = 시스템 계정(공용 스테이션이라 담당자는 의미 없음). 내부 API 세션 인증도 이 계정. KOS 직원 · 담당자 표시에서 `마취용` 처럼 뺀다. 계정 생성은 사용자(KOS 화면) | 사용자 「시스템 계정을 따로 만들어서 관리자 권한」 |
| 2026-10-20 | (사실) KOS 내부 로그인 = `POST api.kos-solution.com/common/v1/user/commands/sign-in {email,password}` → `{data{id,email,name,tenantIds[],token(JWT)}, tokenExpiredDateTimeUtc}`. 수명 ≈14시간 · 쿠키 없음 · refresh 없음. 실을 헤더 이름은 HAR 에서 지워져 미확인(`Authorization` 추정) | HAR `로그인.har`(15:21 · 비밀번호 포함 — 확인 뒤 삭제 권고) |
| 2026-10-20 | KOS 토큰(내부 · 공개) 보관 = 만료 시각 기준(일자 키 아님) — 만료 10분 전 · 401 이면 재로그인 1회. **PoC 는 기존 SQLite**, PoC 뒤 PG + Redis 로 나눈다(그때 판단) | 사용자 「poc 지나면 pg랑 Redis」 |
| 2026-10-20 | **데이터 원천 = KOS 데모 지점 실연동.** v1 시드(시나리오 `seed.json` · events · `seed ensure`)는 지우지 않고 주석 처리(끔). 시안도 데모 데이터 모양으로 | 사용자 「시드 데이터 주석 처리하고 kos 데모 연동으로」 |
| 2026-10-21 | **시안 확정 = claude design `Ceramique 시술현황판 v2.dc.html`(사용자 수정본 · 로컬 `design-user-r3/`)**. 정책은 시안대로 — `design-r3-read-report.md` §4-1 P1~P19. 현황판 카드에서 시술 [시작] · [종료] · 현황판 「호출」 탭(의국 화면)에서 콜 수락 포함. 배포 코드와 다른 15곳은 코드를 시안에 맞춘다 | 사용자 「디자인은 이렇게 하고」 |
| 2026-10-21 | 플로우 ① — KOS 일정이 `PROCEDURE_WAITING` 이 되면(조회 주기만큼 뒤) 시술 현황판에 카드가 생긴다. **수납 전(`paymentRequired: true`)이어도 띄우고 「수납 필요」 표시** | 사용자 「응 맞아 띄워야해」 |
| 2026-10-21 | (사실) 지금 KOS 는 코디가 내원 때 **「방 배정」 작업(ETCETERA)** 을 넣고 방을 배정한다 → 고객은 오면 반드시 방이 있다. **방 없는 고객 = 라운지 대기**. 앞으로 ccc 내원현황에서 방을 미리 배정할 수 있게 된다(다음) | 사용자 · 데모 조회(「방 배정」 작업 READY · room A-룸1) |
| 2026-10-21 | 시술 현황판은 **방이 있는 시술 대기 고객만** 카드로(라운지 대기 · 방 배정 정보는 시술 현황에 필요 없다). ~~「방 배정」 작업은 시술 목록에 안 보인다~~(10-21 E2E 에서 뒤집음 → 방 배정 등 ETCETERA 도 읽기 전용 한 줄로 보인다 · `procedures[].kind`). 입실 시각 = 방이 배정된 시각(코디 기본값) | 사용자 「시술 현황에서는 그런 정보는 필요가 없어」 |
| 2026-10-21 | 플로우 ② — **마취는 시술 진행과 별개 상태**(고객 상태 대기 · 진행과 따로 돈다) → 시술 진행 중에도 [마취 시작] 가능. 확정 시안(`anesCtl` = 시술 대기만)과 다름 → 스펙에서 시안을 고친다 | 사용자 「마취랑 시술진행이랑 별개 상태 아니야?」 |
| 2026-10-21 | 마취 「확인이 필요」 기준 = 20분(병원 기본) | 사용자 「20분 기준이 맞아」 |
| 2026-10-21 | KOS 「마취용」 계정 배정은 ccc 가 하지 않는다(마취는 ccc DB 만) | 사용자 「업데이트할 필요는 없는 거 같아」 |
| 2026-10-21 | 플로우 ③④ — **호출은 만든 시각과 함께 기록에 쌓기만**(지우거나 고치지 않음). 시술마다 유효 호출 = 그 시술이 들어간 **가장 최근 호출**. 수락 = 그 호출이 유효 호출인 시술 중 **아직 수락 안 된 것만**(KOS `change-tasks-doctors` 도 그 sequences 만). 호출 탭에는 받을 시술이 남은 호출만. 확정 시안 P11(수락 = 수락 전 호출 전부)을 바꾼다. 호출 기록은 원장별 기여 로그로도 쓴다 | 사용자 「호출 생성 시각 기준으로 남기는 게」 · 「응」 |
| 2026-10-21 | [시작] 조건(시안 P4 확인) — 호출한 시술은 **수락 전엔 [시작] 꺼짐**, 수락 뒤 켜짐. 호출 안 한 시술은 담당의가 있을 때만 | 사용자 「호출 수락이 안 된 상태는 시작이 안 되잖아」 |
| 2026-10-21 | **새 호출이 생기면 그 호출에 든 시술은 [시작] 꺼짐**(유효 호출 = 가장 최근 호출 → 수락 전). 이미 수락된 시술을 다시 호출해도 마찬가지 — 새 호출이 수락될 때까지 시작 안 됨. 시술 진행 중이어도 같다(고객 상태는 진행 그대로) | 사용자 「새로운 호출이 생기면 시작이 안 되는 거지」(코디가 「새 시술」로 잘못 읽은 것을 바로잡음) |
| 2026-10-21 | **진행 중 · 완료된 시술은 원장을 바꿀 수 없다** — 체크칸 꺼짐(새 호출에 못 넣음). 호출 대상 = 대기 시술만. ③ 나머지는 기본값: 「원장 한 명」 호출은 HAR 확인 전까지 KOS 에 전체와 같은 요청 · 지정 원장은 ccc 만 / 원장 목록 = KOS 원장 역할(시스템 · 마취용 · 비활성 제외) / 비어 있음 = ccc 에서 진행 중 시술 없음 | 사용자 「완료 · 시작된 시술에서는 원장을 바꿀 수 없지」 |
| 2026-10-21 | 플로우 ④ — **[되돌리기] 뺀다**(시안 P10 · 토스트의 되돌리기 포함). 호출 · 수락은 로그로 쌓기만 — 되돌리기는 나중에 로그로 붙일 수 있다. [다른 원장에게] = 기존 지정 호출은 두고 같은 시술로 「전체」 호출을 새로 만든다(시각 기준 규칙) | 사용자 「되돌리기는 일단 빼자 · 로그만 쌓이면 나중에」 |
| 2026-10-21 | 수락하는 곳 = **의국 화면**(이번 범위 · 먼저). 개인 태블릿 · 폰 · 앱 수락은 나중. 의국 화면 = 시술 현황 화면의 「호출」 탭(시안 주석 「의국 화면」) — 의국 PC 에 띄워 두고 원장이 자기를 골라 [수락]. 로그에는 수락한 원장 · 시각 · 시술 · 호출 id | 사용자 「지금은 의국에서 화면에서 누른다고만 가정하자 · 이게 먼저 · 앱도 만들 거 같아서」 |
| 2026-10-21 | 되돌리기(수락 · [종료] 실수 포함)는 **이번 범위에서 정책을 정하지 않는다** — 나중에 로그 기반으로 한 번에. ~~지금은 실수하면 KOS 화면에서 고친다~~ → 같은 날 바로잡음: **현장은 KOS 를 직접 조작하지 않는다.** 실수 복구는 되돌리기 정책 때 정한다(지금은 로그만) | 사용자 「되돌리기 정책까지 정하기에는 너무 사이즈가 크지 않아?」 |
| 2026-10-21 | 플로우 ⑤ — **원칙: 시술 [시작] · [종료]는 시술실 안 태블릿 · 모바일.** 지금은 앱이 없으니 **간호 스테이션(현황판)에서 한다고 가정**. 나중엔 웹 ↔ 앱 모두 가능 — 바쁘면 스테이션이 보조. 태블릿 · 폰 화면(디자인 2단계)은 나중 | 사용자 |
| 2026-10-21 | [종료]는 **[시작]한 시술에만** — 시작 없이 종료 안 됨. 늦게 누르면 부정확한 건 어느 쪽이든 같으니 단계는 명시적으로 | 사용자 「시작 누르고 종료를 명시적으로 해야 하지」 |
| 2026-10-21 | 시안 r4(사용자 수정 · `design-user-r4/`) — 카드 아래 큰 버튼 하나: 시술이 남았으면 「시술 선택 후 의사 호출」(꺼짐) / 「의사 호출 · N건」, 다 끝나면 같은 자리가 [귀가 대기]. [귀가 대기]는 끝나기 전엔 안 보임. 그 외 r3 정책 그대로 | `design-r4-read-report.md` Q1~Q4 |
| 2026-10-21 | 플로우 ⑥ — **[귀가 대기] = 방을 빼서 라운지로 보낸다** | 사용자 「귀가대기는 라운지로 보낸다는 거지 · 방 빼라는 거야」 |
| 2026-10-21 | (사실) KOS 는 완료해도 작업의 `room` 을 지우지 않는다 — HAR `시술완료_상태.har`: `change-tasks-complete` 1건이 「방 배정」 포함 8개를 한 번에 DONE(10:28:17), 단계는 그 전 10:27:19 에 이미 `PROCEDURE_DONE`. 방은 `A-룸1` 그대로 → 「방 빠짐」은 방에 붙은 작업이 다 끝난 것으로 KOS 화면이 판단하는 것으로 보인다(추정) | 코디 HAR + 공개 API 재조회 |
| 2026-10-21 | (사실) KOS 화면은 **마지막 시술을 완료하는 순간 방을 「방이 비었어요」로 비운다** — 고객은 아직 「시술 진행」 카드에 있고 [귀가 대기] 전인데도. 데이터의 `room` 은 그대로 → 방 점유를 「안 끝난 작업」으로 판단하는 화면 규칙. HAR `시술완료_상태 copy.har`: `change-tasks-complete` [1] · [2] · [3] 하나씩(10:32:52~33:00) 뒤 `change-flow-step PROCEDURE`(10:33:05) | 사용자 캡처 + HAR |
| 2026-10-21 | **ccc 는 방을 시술 완료로 비우지 않는다** — 방은 **[귀가 대기](= 라운지로 · 방 빼기)를 누를 때까지 그 고객 것**. 그때 KOS `changeFlowStep(PROCEDURE_DONE)`. 마지막 시술 완료 ≠ 방 빼기 | 사용자 「사실 방이 빠지면 안 되는 거 아니야?」 |
| 2026-10-21 | 플로우 ⑦ — 10초 조회. **KOS 에 있는 상태는 KOS 가 기준**(일정 · 시술 목록 · 결제 · 오더 메모 · 방 · `flowStep` · 작업 완료/시각 · 집도의 · 호출 여부)으로 덮어쓰고, **KOS 에 없는 것만 ccc 기준**(마취 · [시작] 시각 · 호출 기록). ccc 에서 누른 뒤 KOS 반영 전엔 덮어쓰지 않고 「KOS 반영 중」 + 재전송 | 사용자 「응」 |
| 2026-10-21 | **장기 방향: KOS 를 화면 하나씩 점진 교체(나중에 제거)** — 당장 CRM 을 못 만들어서. 그래서 ccc 는 KOS 를 지나가기만 하지 않고 **고객 · 일정 · 시술을 ccc DB 에 KOS id 로 묶어 저장**(KOS 모양 그대로) — 나중에 원천만 ccc 로 바꾼다(v1 DEC-002 D-21 과 같은 방식) | 사용자 「나중에 KOS 를 제거하는 작업 · 한 화면씩 점진적 교체」 |
| 2026-10-21 | (사실) KOS 시술 현황 새로고침 = 내부 `POST /tenants/{id}/schedule/v2/queries/get-schedules-grouped-by-zone {zoneIds[], startDateTimeUtc, endDateTimeUtc}` 한 번 → 그날 구역의 **일정 전부**(이 HAR 15건 · 32KB · 65ms). 일정 한 건 = 공개 API 와 같은 모양 + **`visitor` 전체**(이름 · 연락처 · 생년월일 · 국적 · 메모 · isNew · 차트번호 …) · `tasks[]`(room · 시각 · 호출 · 집도의) · `orderMemo` · `taskTimers`. 방 목록은 `get-rooms` 함께. **10초 조회 후보**(공개 `getSchedulesByFlowStep` 은 단계별 8번) | HAR `시술현황_새로고침.har` |
| 2026-10-21 | **데이터 모델 원칙 — ccc DB 가 KOS 를 품는 더 큰 구조.** 모든 행에 ccc id(주인) + `kos_id`(있으면). KOS 에서 오는 것(고객 · 일정 · 시술 · 방 · 직원)은 지금 KOS 원천 · 10초 덮어씀, ccc 에만 있는 것(마취 회차 · 호출 기록 · 수락 · 시작 · 귀가 대기 · 조작 로그 · KOS 반영 상태). 필드 이름은 ccc 이름 + KOS 대응표(KOS 모양에 묶이지 않음). 조작은 이벤트 로그. 개인정보는 화면에 쓰는 것만. 테이블은 SPEC-003 에서. (앞의 「KOS 모양 그대로 저장」을 고침) | 사용자 「DB 는 우리 게 더 큰 구조가 돼야 하지? KOS 데이터 + 우리 데이터」 · 「응」 |
| 2026-10-21 | 조회 구역 = **「4층」만** | 사용자 「4층만 일단 하자」 |
| 2026-10-21 | **직원 · 방 정보 = KOS 에서 1시간에 한 번**(+ 서버 시작 때). 직원 = 공개 `getAccounts`(원장 역할 · 시스템 · 마취용 · 비활성 제외) · 방 = 내부 `get-rooms`(공개 API 에 없음). ccc DB 직원 · 방 테이블(ccc id + `kos_id`) | 사용자 「1시간에 한 번씩 요청하면 되나」 |
| 2026-10-21 | **KOS 조회 시간 = 09:00~21:00 KST**= **운영 10:00~20:00 의 앞뒤 1시간**(코디가 처음 08~22 로 잘못 읽음) —(10초 일정 조회 · 1시간 직원/방 모두). 밖에서는 조회 안 함. 10초 조회 API = 내부 `get-schedules-grouped-by-zone`(기본값) | 사용자 「운영 시간 앞뒤 1시간만 · 9시부터 21시까지」 |
| 2026-10-21 | **시스템 계정 = 사용자 개인 계정(`KOS_SYSTEM_EMAIL`) 그대로**, 데모 KOS 역할을 「관리자」(roleTags 1~7 전부)로 바꿈. 이 계정은 DOCTOR 태그(2)도 가져 원장 목록에 섞인다 → 원장 목록 · 담당자 표시에서 **계정 id 로 뺀다** | 사용자 「지금 아이디로 쓰면 돼 · 권한 바꿨어」 · 코디 `get-user-account` 확인 |
| 2026-10-21 | 데모에서는 시스템 계정(kknaks)이 **원장 태그를 가진 채로 둔다** — KOS 에서 호출 알림을 사용자가 직접 확인하려고. 운영에서는 의사만 받게(시스템 계정은 원장 태그 없이). ccc 원장 목록에서는 계속 계정 id 로 뺀다 | 사용자 「kknaks 도 가야 내가 KOS 에서 확인 · 운영에서는 의사만」 |
| 2026-10-21 | KOS 작업 「진행중」은 **수락(집도의 지정) 시점 그대로** 둔다 — 시술 단위 진행 중 · 대기의 기준은 ccc(KOS 는 현장이 안 본다). KOS `doctorAssignedDateTimeUtc` = 수락 시각, 시술 시작 시각은 ccc 에만 | 사용자 · E2E-2 |
| 2026-10-21 | [귀가 대기] = KOS 「방 배정」 등 남은 작업 취소 → `PROCEDURE_DONE`(E2E-3 그대로 · 시술 현황이 취소한다). **카드는 판에 흐리게 맨 뒤로 남고**, 데스크가 귀가(KOS `COMPLETED`) 처리하면 사라진다(E2E-8 되돌림). 데스크 귀가는 지금 KOS 화면 | 사용자 「귀가 대기는 남겨야 · 방배정은 시술현황에서 취소해줘야지」 |
| 2026-10-21 | **디자인 2단계 = Flutter PoC 앱**(시안 「간호사 모바일」 · 「시술실 태블릿」 · claude design `dda9a931` · 로컬 `design-mobile/`). 서버 = `procedure/back` 그대로 | 사용자(워커와 대화 · `design-mobile-read-report.md` §9 U1) |
| 2026-10-21 | 앱 **로직 정본 = 구현 코드(back 스냅샷 값)** — 시안은 화면 모양만. 시안 로직(마취 시작 전에만 · 동시 진행 막기 · 방 단위 수락 · 확인 필요 기준 · 필터 하나씩)은 버리고 `canStart` · `anesthesia` · `accept`(호출 1건) · `need` · `counts` 그대로 | U2 |
| 2026-10-21 | 계정 = **어드민 · 의사 · 간호사**. PoC 로그인 카드 = 어드민 + 의사 1 + 간호사 1. **DB 에는 사람마다 계정**(원장 = KOS 원장과 연결 · 간호사도 한 명씩) | U3 |
| 2026-10-21 | 통역 = **이전 PoC(`cc/back` `WS /api/interpret` · Soniox) 로직 · 언어**(zh 번체 · en · ja · th · fr · es · tl · hi) → `procedure/back` 으로 복사(D-01). 빠른 말하기 = **시안 문구 6개 하드코딩**(위 언어 번역). 병원별 설정은 나중 | U4 · U5 |
| 2026-10-21 | 앱 PoC 에서 뺌: 동의서 · 시술 메모 · [다시 알림] · 간호사 요청 · 빈 방/입실 예정 | 워커 정리 · 사용자 결정 없음 → 뺀 것으로(코디 기본값) |
| 2026-10-21 | (코디 기본값) 의사 계정 [수락] = **자기 자신으로 수락**(개인 계정이니 원장 고르기 없음). 어드민 · 간호사는 의국 화면처럼 원장을 골라 수락 | 워커 기본값(「고른다」)을 개인 계정 결정(U3)에 맞춰 고침 · 워커도 §9 정정으로 같은 결론(의사 계정 = 원장마다 1개 · PoC 는 원장 한 명 로그인 · 로그인 원장 이름으로 수락) |
| 2026-10-21 | **권한은 back 이 조작 API 마다 검사**(앱 버튼 숨김만으로 안 됨). 토큰에 역할(어드민 · 의사 · 간호사) + 연결 원장 id. 수락: 의사 = 로그인 원장으로 back 이 정함(다르면 403) · 지정 호출은 지정 원장만 · 간호사 403 · 어드민은 원장 골라 수락. 그 밖 조작(마취 · 호출 · 시작 · 종료 · 귀가 대기) = 세 역할 모두(기본값). `actor` = 로그인 계정. PoC 의사 = KOS 데모 실제 원장(시스템 계정 X). 역할별 허용 · 403 단위 시험 | 사용자 「권한 체크는 중요」 · `design-mobile-read-report.md` §9-1 |
| 2026-10-21 | 앱 E2E = **로컬 + 아이폰 + 아이패드(iOS 만)** · 사용자 맥북 로컬 빌드 → **TestFlight** · 기기는 초대 설치 | 사용자 · 보고서 §9-2 |
| 2026-10-21 | **오늘 앱 E2E 뒤 최종 배포** — back · front 를 `ccc.medisolveai.xyz` 에. 앱 서버 주소 입력칸 기본 = 맥 IP → 배포 뒤 https. 배포 확인: 통역 wss · SSE ingress 버퍼링/유휴 시간 · `SONIOX_API_KEY` · KOS 키 · 시스템 계정 · ccc 계정 = Secret | 사용자 §9-2 |
| 2026-10-21 | **원장 호출 푸시 알림을 이번 앱 PoC 에 넣는다**(D-34 「원장 호출 휴대폰 알림 = 다음」을 뒤집음). (코디 기본값) iOS APNs 직접(Firebase 없음 · .p8 인증 키) · 호출이 생기면 받을 원장에게: 지정 호출 = 그 원장 · 전체 호출 = 의사 계정 전원(기기 토큰 등록한) · 알림을 누르면 그 방 룸 상세. 앱 로그인 때 기기 토큰 등록. 키 · 팀 id 는 레포 밖 | 사용자 「푸시 알림 필요한데」 |
| 2026-10-21 | **관리자도 호출 푸시를 받는다** — 앱 로그인 카드에 관리자 추가(관리자 · 의사 · 간호사) · 관리자 기기는 모든 호출(전체 · 지정) 푸시 · 앱에서도 관리자 수락 = 원장 고름 | 사용자 「관리자도 알림을 받을 수 있으면 좋겠어」 |
| 2026-10-21 | **알림에서 바로 [수락]**(Apple Watch 포함 — iPhone 알림 액션은 워치에 그대로 보인다 · 워치 앱 없음). 의사 수신자 알림에만 카테고리 `CALL` + 액션 「수락」 → 앱이 백그라운드에서 `POST /api/calls/{callId}/accept`(doctorId 없음 = 자기 자신). 관리자 알림은 액션 없음(원장 골라야 하니 앱 열기). 성공 · 실패는 로컬 알림 한 줄, 실패면 누르면 룸 상세. 토큰은 키체인 | 사용자 「와치에도 · 수락 버튼까지 넣자」 |
| 2026-10-21 | **알림 내역을 DB 에 쌓는다** — `push_log`(호출 · 받는 사람 · 기기(토큰 끝 6자리) · 카테고리 · 상태 sent/failed/skipped_no_key/token_removed · APNs 결과 · 시각). 수락 출처(push · app · web)는 `X-Accept-Source` 헤더 → call_accept 이벤트에. 조회 API 는 나중(원장 기여 · 응답 시간) | 사용자 「알림 내역도 DB 에 쌓을 거지?」 |
| 2026-10-21 | Apple — **번들 id `com.kknaks.ceramique`**(개인 팀 · Explicit · Push Notifications · Broadcast 아님) 등록. Team ID 는 레포에 쓰지 않는다(`.env` · `Signing.xcconfig` 만). `.p8` = `~/keys/ceramique/`(레포 밖) | 사용자 |
| 2026-10-21 | App Store Connect 앱 레코드 「Ceramique」 생성 · **사용자 액세스 = 전체**(다른 사람도 써야 해서) · APNs 키 = Sandbox & Production · Team Scoped · 로컬 back 연결 완료(JWT 서명 OK) | 사용자 |
| 2026-10-21 | **배포 먼저** — 앱은 배포 주소(`https://ccc.medisolveai.xyz`)로 TestFlight. **로그인 접근 제한(OQ-601)은 배포 뒤** 앱 · 태블릿 · 웹을 다 확인하고 정한다(데모 · 데이터 없음이라 감수) | 사용자 「지금은 배포 먼저 · 비밀번호는 배포하고 확인하고 수정」 |
| 2026-10-21 | 코드 PR kknaksss/cc-prototype#3 머지(0f4634a) · 이미지 procedure-back/front(태그 = 전체 sha) · 클러스터 Secret cc-prototype-secret(22) · cc-prototype-apns 생성 · infra PR MediSolveAIDev/k8s_infra_mac#22 머지 · ArgoCD sync. Apple Developer 사용권 갱신 동의 완료(사용자) | 코디 · 사용자 |
| 2026-10-21 | **배포 완료 · 확인** — infra #23(APNs 마운트 /etc/apns · SA 토큰 끔 — /run/secrets ro 가 SA 마운트를 막아 CrashLoop 였음) · back/front Running · Synced Healthy. https://ccc.medisolveai.xyz: accounts 3 · board 카드 7 · KOS 공개/내부 true · SSE 첫 접속 + 10초마다 · 통역 wss 토큰 있음 열림/없음 403 · APNs JWT OK(production). Cloudflare 가 Python 기본 UA 를 403(Dart UA 는 200). TestFlight 빌드 1(1.0.0) 업로드 완료(처리 대기) | 코디 확인 |
| 2026-10-21 | **OQ-601 닫음 — 정상 로그인(웹 · 앱 둘 다)**: 아이디 + 비밀번호 · 계정 카드 목록 API(`GET /api/auth/accounts`) 공개 제거 · 비밀번호는 해시로 DB(서버 시작 때 env/Secret 값으로 어드민 · PoC 의사 · 간호사 설정 — 그 밖 원장 doctor 행은 비밀번호 없으면 로그인 불가) · 실패 반복 잠금(5회 · 1분) · 앱은 서버 주소 칸 유지 + 아이디/비번 폼 · 토큰은 지금처럼 키체인 | 사용자 「이제 로그인 정보 막자 · 정상 로그인으로 · 웹 앱 다」 |
| 2026-10-21 | (코디 기본값) 앱 코드 = `procedure/app/`(Flutter) · ~~기기 back = 배포 주소 · 기기 E2E 전 WP7~~ → 사용자 결정: **기기 back = 같은 Wi-Fi 맥 IP(http :8700 · 통역 ws)** · 앱 ATS 로컬 허용 · 로컬 네트워크 권한 문구 · back 0.0.0.0 · 맥 방화벽 8700 · 맥 IP 고정 또는 앱 서버 주소 입력칸. 배포는 맨 뒤 별도 | 코디 → 사용자 §9-2 |
| 2026-10-21 | (사실) **관리자 권한으로 쓰기 4종 다시 확인 — 모두 200**(데모 10-20 일정 · 작업 seq 4 쥬베룩, 10:48:27~30). 담당 = 시스템 계정 · **수락을 다른 원장 계정 id 로 대신 넣기 됨**(집도의 = 고른 원장) · 호출 뒤 `WAITING` → 수락 뒤 `READY` → 완료 `DONE`. 의국 화면에서 원장을 골라 수락하는 구조가 KOS 쪽에서도 된다 | 코디 실호출 |
| 2026-10-21 | **시술현황은 기존 코드를 무시하고 새로 만든다** — 꼬일 것 같으면 다른 디렉토리(새 기능 폴더) · 이전 것은 아카이브. **테마 · 디자인 시스템(medikit · Ceramique · 기존 컴포넌트 모양)은 유지** | 사용자 |
| 2026-10-21 | 새 기능 폴더 `procedure/`(front Next.js + back FastAPI · 새 DB) — 테마 · medikit · patches · 틀 컴포넌트는 `cc/` 에서 **복사**(기능끼리 import 금지). **배포 = 기존 주소 `ccc.medisolveai.xyz` 를 시술현황으로 교체** → `cc/` 는 배포에서 빠지므로 `_archive/cc/` 로 옮기고 Actions · infra 차트를 `procedure/` 로(코디 기본값). 헤더 메뉴 = 「시술 현황」 하나(기본값) | 사용자 「기존 주소로 올릴 거야」 |
| 2026-10-21 | ccc 로그인 = **관리자 계정 1개만**(간호 스테이션 · 의국 공용). 아이디 · 비밀번호는 env / k8s Secret(코드 · 레포에 값 없음). 직원 개인 계정은 나중 | 사용자 「계정은 일단 관리자 계정 하나만 · ccc 에도 로그인은 해야」 |
| 2026-10-21 | 로그인 = **v1 처럼 계정 카드를 눌러 바로**(비밀번호 검증 없음 · `GET /api/auth/accounts` → `POST /api/auth/login {id}`). 배포 때 접근 제한은 그때 다시 | 사용자 「기존 PoC 처럼 선택해서 로그인되게」 · r3 구현 완료 |
| 2026-10-21 | 범위 = **코드 구현까지**(문서 → 발주 → 구현 → 배포) | 사용자 |
| 2026-10-21 | 화면 갱신 = **SSE**(폴링 아님) — 현황판 · 의국 화면(호출 탭)이 실시간. back 이 ccc 조작 · KOS 10초 조회 변경 때 이벤트 발행 | 사용자 「sse 쓸 거지? 의국에서도 호출 정보가 실시간으로」 → planner 에 추가 지시 |
| 2026-10-21 | 검증 = 구현한 것만 단계별로, **통합 테스트는 마지막 한 번** | 사용자 |
| 2026-10-21 | (사실 · SPEC 정정 후보) 내부 쓰기의 시스템 계정 id = **`get-user-account` data.id**(= getAccounts email 일치 id). `sign-in` data.id(사용자 id)를 담당자로 넣으면 200 주고 무시. KOS `change-flow-step` 같은 단계로는 400 → 같은 단계로 보내지 않는다. `call-tasks-doctors` 는 귀가 대기 일정에서 400(시술 대기에선 10-20 · 21 200) | backend WP4 실호출 |
| 2026-10-21 | (사실) **`call-tasks-doctors` 400 = 시술 작업에 방이 없을 때**(`errorProperties roomId NotFound`). 방은 「방 배정」 작업에만 붙어 있고 시술 작업은 비어 있다 → 호출 전에 시술 작업에 방을 넣어야 한다(KOS 「방」 조작 HAR 필요) | 사용자 E2E · 코디 재현(데모 일정 seq 2) |
| 2026-10-20 | (사실) 내부 API 서버 호출 됨 — 사용자 개인 계정(데모 「원장」 역할)으로 `sign-in` 200 · 지점 = 「세라미크의원 명동점 DEMO」 1곳(구역 id 가 공개 API 데모와 같음). **헤더 `Authorization: Bearer <token>`**(공개 API 와 다름 — 그냥 토큰 400 · 없음 401) · Origin 없어도 됨. 내부 조회 15종 중 14 200(`get-rooms` 방 28 · `get-accounts` 78 · `get-roles` 15 …), `get-tax-refund-settings` 400 은 브라우저 HAR 에서도 400. 쓰기는 아직 안 함 | 코디 실호출(조회만) |
| 2026-10-20 | (사실) **내부 쓰기 4종 서버 호출 됨**(데모 일정 15:30 예약 · 작업 seq 2 하나) — `change-tasks-assignees` → `call-tasks-doctors` → `change-tasks-doctors` → `change-tasks-complete` 모두 200 `{}`. 공개 API 재조회: 담당 = 나 · 호출 후 status `WAITING` · 수락 후 `READY` + `doctorAssignedDateTimeUtc` · 완료 후 `DONE` + `completedDateTimeUtc`. **작업 하나만 호출 · 수락 가능**(sequences [2]). 완료는 `flowStep` 이 `PROCEDURE_WAITING` 이어도 받아 준다. 개인(원장 역할) 계정 — 시스템 계정 권한은 다시 확인 | 코디 실호출 15:59:55~16:00:01 |
| 2026-10-20 | 보통 **한 방(고객) = 원장 한 명이 시술 전부** — 의사 호출 · 수락은 남은 시술 전부에 한 번. 예외: 고객이 「이 시술만은 특정 원장에게」 → 그 시술만 골라 특정 원장 호출(KOS 화면도 시술 체크 「N개 선택됨」 → [의사 호출]). API 가 작업 단위 호출을 받으므로 그대로 된다 | 사용자 · 코디 실호출 · KOS 캡처 |
| 2026-10-20 | 시술 현황판 메인 = **도면이 아니라 오더지 카드 나열**(시술실1 · 오더지 | 시술실2 · 오더지 | …) — 간호사들이 오더지를 출력해 방 번호와 꽂아 두고 보는 방식 그대로. 정렬 필터 **[입실순 | 배치순]** | 사용자 · 부팀장 07:55(노티를 방 번호 · 고객 이름과 꽂아 두고 한 것은 지우고 체크) |
| 2026-10-20 | 카드는 고객이 있는 방만 · ~~귀가 대기 고객은 흐리게 맨 뒤~~(10-21 E2E 뒤집음 → 귀가 대기 = 방 빼기 = 가운데 판 · 현황에서 사라짐 · 고객 탭에만 남음) | 사용자 「응 맞아」(코디 기본값) |
| 2026-10-20 | 카드 안 순서 = **오더 메모 → 시술 진행**. 오더 메모는 사람마다 길이가 달라 **일정 높이 + 스크롤 + 접기 · 펴기** | 사용자 |
| 2026-10-20 | 현황판 시술 목록 = 체크박스(완료) — 끝난 시술이 시각 순으로 위, 진행 중 · 대기가 아래(남은 시술이 보이게). 정렬 방향은 확인 중 | 사용자 |
| 2026-10-20 | (사실) KOS 내부 API 순서 — 담당자 `change-tasks-assignees{scheduleId,sequences[],assigneeIds[]}` → 호출 `call-tasks-doctors{scheduleId,sequences[]}` → **원장 계정이 수락** = `change-tasks-doctors{scheduleId,sequences[],doctorIds[]}` → 진행 `change-flow-step{id,step:PROCEDURE}`(공개 `changeFlowStep` 과 같음). 호출만으론 단계 안 바뀜. 내부 `get-rooms` 로 방 목록 있음 | HAR `의사호출.har` · `의사호출_2.har`(데모 원장 계정 · gitignore) · 공개 API 재조회 |
| 2026-10-20 | (사실) 시술 완료 = 내부 `change-tasks-complete{scheduleId,sequences[],complete:true}` — 공개 API 없음(스펙 grep 0). 작업 하나씩(sequences [1]) · 그 작업만 DONE · 단계는 PROCEDURE 그대로 | HAR `시술완료.har`(14:46:34) · 공개 API 재조회 · 1차 HAR2 리포트와 같음 |
| 2026-10-20 | (사실) KOS 상태가 둘: ① 작업 칸(화면 「대기중 · 준비중 · 호출함 · 진행중」) — 원장 수락(`change-tasks-doctors`) 하면 「진행중」 ② 일정 단계(`flowStep`) — 수락해도 `PROCEDURE_WAITING` 그대로, 따로 [시술 진행] 버튼(`change-flow-step`)을 눌러야 `PROCEDURE`. 작업 status 는 수락 뒤에도 `READY` — 화면 「진행중」은 의사 배정으로 보인다(추정) | HAR `시술진행.har`(14:52:44 호출 · 49 수락 · flow-step 없음) · 공개 API 재조회 · 사용자 캡처 |
| 2026-10-20 | ~~원장(콜 받는) 쪽은 모바일 앱(Flutter 생각) — 담당자 화면 뷰를 다시 설계~~ → 같은 날 뒤집음: **모바일 앱은 나중에.** 원장 쪽 화면 형태는 열어 둔다 | 사용자 「모바일 앱은 일단 나중에」 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| researcher | `term_3ba80a1f-4021-41d3-a02a-e26f5d885e81` | `task_a5a80542b4fb` | `ctx_2d9bc9aaa060` | `myeongdong-poc-v2-research-brief.md` | 완료 · 검수 PASS |
| frontend(시안 조회) | `term_472056a9-e833-4f66-96e0-625e582bc2a0` | `task_2078129506df` | `ctx_7dd97dc23386` | `myeongdong-poc-v2-design-fetch-brief.md` | 완료 — 새 파일 0(사용자 「디자인 다 했어」 = 논의 끝, 오해) |
| frontend(시안 1단계) | `term_472056a9-e833-4f66-96e0-625e582bc2a0` | `task_68b26ac35ffc` | `ctx_f66fa1b591ce` | `myeongdong-poc-v2-design-brief.md` | 완료 → 사용자 반려(batch-1 #1~4) |
| frontend(시안 r2) | `term_472056a9-e833-4f66-96e0-625e582bc2a0` | `task_13c951c62303` | `ctx_373d925e5e42` | `myeongdong-poc-v2-design-r2-brief.md` | 완료 → 사용자가 claude design 에서 직접 고침(10-21) |
| frontend(사용자 시안 읽기) | `term_43097bde-bfcc-4b41-b2dc-1ca5fe87d29f` | `task_566157c2d750` | `ctx_2ca5b9a072de` | `myeongdong-poc-v2-design-r3-read-brief.md` | 완료 — 시안 확정 |
| frontend(시안 r4 읽기) | `term_43097bde-bfcc-4b41-b2dc-1ca5fe87d29f` | `task_327c188bc9ab` | `ctx_83fc55b4118c` | `myeongdong-poc-v2-design-r4-read-brief.md` | 완료 |
| planner(SPEC-003 · WORK-003) | `term_a66cea45-690c-4abd-b7a1-5382974272fb` | `task_d81941730952` | `ctx_240e6fb5ddf6` | `myeongdong-poc-v2-spec-brief.md` | 완료(SPEC-003 0.1.0 · WORK-003 · OQ-504~515 기본값) |
| backend(WP1~4) | `term_3104b9da-86f3-4f8e-980b-b17e658ed048` | `task_1f2d8a7076ab` | `ctx_550d2e7647d9` | `myeongdong-poc-v2-be-brief.md` | 완료 — 38 passed · 코디 비밀값 스캔 0 · 미결: call-tasks-doctors 400(PROCEDURE_DONE 일정이라 추정 → E2E 재확인) |
| frontend(WP5) | `term_4aa544c3-9fb7-4406-8e81-a8f9436cb41c` | `task_6a5fe7a1d382` | `ctx_361520808253` | `myeongdong-poc-v2-fe-brief.md` | 완료 — tsc · lint · build 0 · 장면 8 · 실 back 2브라우저 E2E · 미결: compose front 블록 없음 |
| reviewer(WP1~5) | `term_2f24ee8d-d098-45d1-bef3-fad96e9097f5` | `task_4a58af4e00a8` | `ctx_85550350c5c6` | `myeongdong-poc-v2-review-brief.md` | 완료 — FAIL 3 · WARN 14 · 규칙 PASS → 처분 `fix-decisions-r1.md` |
| backend(fix1) | `term_3104b9da-…` | `task_42cb5cd2215d` | `ctx_148ede2ec36c` | `myeongdong-poc-v2-be-fix1-brief.md` | 완료 — pytest 50 · compose back+front 기동 · 로그 token 0 |
| frontend(fix1) | `term_4aa544c3-…` | `task_fa016baf383f` | `ctx_1d0c266a6aa3` | `myeongdong-poc-v2-fe-fix1-brief.md` | 완료 — tsc · lint · build 0 · limits/long 은 back 반영 뒤 같이 확인 |
| planner(SPEC 정정 r1) | `term_a66cea45-…` | `task_e3b45893a5f7` | `ctx_4ef8f70e7770` | frontend(모바일 · 태블릿 시안 읽기) | `term_b58564e5-02cc-4eea-b04a-583f2001ff45` | `task_f6d42fc7df77` | `ctx_8d44715f52df` | `myeongdong-poc-v2-mobile-read-brief.md` | 완료 · §9 사용자 결정 |
| planner(SPEC-004 · WORK-004) | `term_023d238e-a118-4bb4-bd67-e7a3b2365607` | `task_3d2afa52414e` | `ctx_15d144ad7fc4` | `myeongdong-poc-v2-spec4-brief.md` | 완료 — SPEC-004 0.1.0 · WORK-004 WP1~10 · OQ-601~612(601 = 배포 전 로그인 접근 제한) |
| backend(SPEC-004 WP1→2) | `term_3104b9da-…` | `task_3ce7312e71c7` | `ctx_65697ef8e5dc` | `myeongdong-poc-v2-be4-brief.md` | 완료 — WP1 · WP2 · pytest 106 · 실 Soniox 1회(caption + 24kHz 음성) · WS 로그 token= 0 |
| frontend(SPEC-004 WP3) | `term_4aa544c3-…` | `task_eb2a75751dcb` | `ctx_882941e25f70` | backend(WP11 푸시) | `term_3104b9da-…` | `task_93f882974aa9` | `ctx_5fb5d2070413` | `myeongdong-poc-v2-be-push-brief.md` | 완료 — 113 passed · APNS 키 없으면 끔 · 실 APNs 는 키 뒤 |
| mobile(A1~A6 + WP12 푸시 + 알림 수락) | `term_bc187ae4-…` | `task_8f443ecc7002` | `ctx_d21e604f5ece` | `myeongdong-poc-v2-app-fix1-brief.md` | 완료 — test 54 · 알림 [수락] 실 back 200 · 실 APNs · 워치 · no-codesign pending |
| (이전) frontend WP3 | | | | `myeongdong-poc-v2-fe4-brief.md` | 완료 — 웹 admin 카드만 · 세션 role/name · 실 back 확인 · 실제 수락 왕복은 E2E 에서 |
| mobile(SPEC-004 WP4→5) | `term_bc187ae4-e41a-4843-a1a3-add2b82be1be` | `task_fe42a9bb1b97` | `ctx_607d4e905129` | `myeongdong-poc-v2-app-brief.md` | 완료 — analyze 0 · test 39 · iPhone 시뮬레이터에 실 back 으로 실행 중 · 미결: 호출 시트/통역/태블릿 화면 · 실 흐름 → 사용자 E2E · WP12 푸시는 E2E 뒤(렉) |
| (이전) planner 정정 r1 | | | | `myeongdong-poc-v2-spec-fix1-brief.md` | 완료 — SPEC-003 0.2.0(S1~S12 · OQ-516) · `calls[].limitMin` 빼기 작은 정정 지시 |

## 4. 산출물

- 리포트: `reference/2026-10-12-cc-prototype/kos-demo-api.md`(완료 — 전수 72 · 조회 47 호출 45 성공 · 수납→시술 고리 확인)

## 5. 이력 (최신이 위)

- `2026-10-20` `workflow.md` → `workflow-v1.md`(spec-001 링크 수정) · `workflow-v2.md` 작성
- `2026-10-20` researcher 완료 · 코디 검수 PASS(키·토큰·실명 0 — 코디가 .env 값 · 토큰 · 데모 직원 이름 직접 대조)
- `2026-10-20` researcher 발주(KOS 데모 참고 문서)
- `2026-10-20` main 체크아웃의 ignore 자료(`2026-10-12T161224-5b4603da/` · `cc-back-data/`)를 이 워크트리로 미러링
- `2026-10-20` slug 생성 · config 에 reference 레포 추가
