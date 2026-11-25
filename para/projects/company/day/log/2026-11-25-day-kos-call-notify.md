# 작업 요약 — day-kos-call-notify (day)

기간: `2026-11-25` ~ `2026-11-25`
결과: KOS 에서 건 원장 호출도 DAY 원장 호출 알림 · 푸시를 탄다. 스펙 mediness #965 → main `bf440f27`(DAY-SPEC-002 개정 ㉚ 규칙 40 · SPEC-005). 코드 CENTURION_DAY #285 → dev `1b5bba22` · 같은 날 **prod 배포**(migrate-prod 0009 → 0028 · ff). 웹 예약 현황 · 고객 메뉴 막음 #286 → dev `de0d0dab` → prod. Delivery #283(#284 는 not planned).

## 1. 무엇을 했나

간호사가 DAY 대신 KOS 화면에서 원장을 호출하는 경우가 있다. DAY 는 그 호출을 10초 동기화로 받기만 하고(`visit_task.doctor_called_at` · `called_doctor`) `doctor_call` 을 만들지 않아서, 원장에게 알림 · 푸시가 0 이었다(dev DB 확인 — 호출 시각은 있는데 `doctor_call` 0건).

- 작업 쓰기 공통 경로(`_apply_tasks`)가 방문 잠금 뒤 KOS 호출 시각이 **늦어진 것**과 READY 전이를 관측으로 모은다. 커밋하는 서비스(10초 일정 조회 · 예약 상세 연쇄 두 커밋 · 외부 연동 `ext_sync`)가 같은 transaction 에서 DAY `doctor_call` 을 만들고, 커밋 뒤 기존 `after_call`(알림 행 · 실시간 · 푸시)을 부른다.
- 알림 kind · 글자 · payload 를 바꾸지 않아 prod 정식 앱 0.1.0 도 그대로 받는다. migration 없음.
- 핫픽스라 prod 로 바로 나갔다. 사용자 「급하다」 — dev 머지 · dev 배포 · migrate-prod · prod ff 를 한 번에 이었다.
- 곁가지: 웹 메뉴 「예약」 · 「고객」 · 헤더 「예약 현황」 링크를 빼서 글자만(화면 · 라우트 그대로 · dev · prod 둘 다).

착지까지 문서 검수 3회(WARN 9 → 6 → PASS), 코드 검수 2회(WARN 4 + INFO 6 → PASS · 작은 지적까지 전부 고침), 로컬 KOS DEMO 실물 1회, 배포 4번(dev 2 · prod 2).

## 2. 적용한 기술·개념

- **동기화가 본 외부 변화를 내 도메인 행으로 — 「내가 쓴 것의 메아리」 거르기** → [[external-write-queue]] · [[idempotency]]
  - DAY 에서 누른 호출은 쓰기 큐(`call-tasks-doctors`)로 KOS 에 가고, 다음 동기화에서 같은 호출 시각으로 돌아온다. 이걸 KOS 호출로 보면 알림이 두 번 간다.
  - DAY 는 호출 때 KOS 시각을 모르므로(KOS 가 받은 시각을 새로 찍음) 값 비교가 안 된다. 그래서 **op 시간 창**으로 판정했다: 같은 방문 · 그 sequence 의 op 가 pending · sent 면 메아리, confirmed · 2xx 뒤 failed 면 `updated_at` + 30초까지 메아리, 보내기 전 막힌 failed(`last_error` BLOCKED · 토큰 없음)만 창 밖.
  - 실물: KOS↔DAY 시각 차 +0.3초(op 생성 → KOS 시각) · +4.2초(KOS 시각 → confirmed) — 30초 창 안에 넉넉히.
  - 늦게 커밋된 옛 사본이 값을 되돌렸다가 다시 오는 경우(코드 검수 W1)는 두 겹: `call_changed` 는 앞으로만(`called_at > before`) + 규칙 40 이 만든 호출의 KOS 시각을 `event_log` `kosCalledAt` 에 남기고 그 최댓값 이하면 안 만듦. `doctor_called_at` 저장 규칙은 그대로.
- **한 변화에 행 하나 — 비교는 잠금 뒤 같은 transaction 에서** → [[distributed-lock]]
  - 판 조작과 두 동기화 경로가 모두 방문 advisory lock(`board:{visit_id}`)을 잡는다. 이전 값을 **그 잠금을 잡은 뒤** 읽어야 동기화 회차 · 판 조작이 겹쳐도 호출이 하나다. 스펙은 처음 「같은 transaction 안」이라고만 적어 잠금 밖에서 읽는 구현도 허용했다(문서 검수 W3).
  - 1루프 겹침 시험은 다른 행 잠금(`Refs.link`) 덕에 방문 잠금 없이도 초록이었다. 워커가 스스로 짚었고, 판 조작이 잠금을 쥔 채 동기화를 띄우는 시험(W4)으로 바꿔 잠금을 빼면 빨강이 되게 했다.
- **저장 경로는 「적힌 두 개」가 아니라 전부** → [[contract-surface-enumeration]]
  - 스펙은 판정 자리를 10초 조회 · 예약 상세 연쇄 둘로 적었다. 구현 중 워커가 `ext_sync._load_date` 도 오늘 KOS 값을 먼저 저장할 수 있다고 물었다 — 거기 안 붙이면 10초 조회가 「안 바뀜」으로 보고 알림을 영영 놓친다. `emr_date_sync`(오늘 skip `:172`) · `emr_backfill`(`--to` 오늘 거부 `:161`)은 오늘이 들어오지 않아 제외. 표로 남겨 스펙을 코드 목록으로 맞췄다.
- **KOS 실물이 기본값을 닫았다** → [[input-space-enumeration]]
  - 「전체 호출」 = `doctorIds` 없이 → KOS `calledDoctors: []`(OQ-99). 한 요청 여러 작업 = 시각이 밀리초까지 같음(OQ-106 · 30초 묶음은 안전 여유). 추측으로 확정하지 않고 OQ + 기본값으로 두었다가 첫 실물로 닫았다.
  - 지정 2명 이상은 처음 planner 가 「전체 호출」로 바꿨다(`target_staff_id` 1칸). 검수가 migration 없이 사용자 결정(그 원장들만)을 지킬 길(`called_doctor` 행으로 받는 사람 계산)을 짚어 되돌렸다. 그 계산은 `kind = one` 규칙 40 호출만 — 전체 호출에 걸면 받는 사람이 0명이 된다(r2 N1).
- **같은 이미지를 dev → prod 로 — 빌드 없이 승격** → [[artifact-promotion]] · [[ci-cd]]
  - prod 배포는 dev 배포가 만든 같은 SHA 이미지를 ACR 에서 가져오고, migrate-prod 는 「dev DB 가 그 이미지 head 인지」를 먼저 본다. 그래서 dev 배포가 끝나기 전엔 prod 를 시작할 수 없다. 스쿼시 머지로 SHA 가 바뀌어 PR 검사 통과를 재사용하지 못하고, dev · prod 배포 워크플로가 각각 검사를 다시 돈다(각 ~10분).

## 3. 막혔던 것 / 사고

- **사용자 말을 범위로 잘못 읽었다.** 「고객 차트, 예약현황은 비활성화 (프론트)에서 나중에 할거야」를 이번 작업 범위로 넣어 SPEC-006 ⑭ · Delivery #284 까지 냈다 → 「웹은 안해 · 끄는 거는 내가 알아서」. #284 not planned · 스펙에서 걷음. 몇 시간 뒤 사용자가 다른 방식(메뉴 링크만 빼기 · dev · prod 둘 다)을 직접 요청해 #286 으로 나갔다.
- **스펙 검수 3회 · 드문 경쟁 상황에 시간을 썼다.** 사용자 「아니 이게 어려워 ?」 — 핵심은 한 줄(새 호출 → `doctor_call` → `after_call`)인데 핫픽스에 맞는 속도가 아니었다. 그 뒤 「작은 지적도 해야지」로 지적은 전부 고쳤다.
- **Delivery 발행 두 번 막힘.** harness 는 baseline = fetch 한 origin/main 만 받고, pending 은 target SPEC 이 main 에 stable 이 아닐 때만 준다(`surfaces.py:99-123`). 개정 스펙이라 ready 만 나옴 → 사용자 「우회해서 만들수 잇잖아」 → main ready + review_surface 첫 줄에 「계약 원천 = #965」 · 머지 뒤 v2 재결속.
- **배포 대기.** 사용자 「ci 말고 머지」로 PR 검사를 기다리지 않고 머지했지만, 배포 워크플로 안의 검사는 건너뛸 수 없었다. prod 도 검사가 다시 돈다는 걸 처음엔 「약 2분」이라고 잘못 말했다(과거 run 시간만 보고). 같은 질문(「다 됐어」 · 「검사 얼마나」 · 「왜 또 하냐」)이 여러 번 왔다.
- **원인 단정을 두 번 고쳤다.** ① 고객 B 「종료」 KOS 400 을 「집도의가 없어서」라 했다가, 같은 상황의 고객 A 의 시술 종료가 들어간 걸 보고 「바로 시작 재시도와 종료가 겹침」으로 고침. ② 와이어프레임에 지금 카드에 없는 「[시술 진행]」 배지를 지어 넣었다가 사용자 캡처로 바로잡음.
- **새 코디 띄우기 두 번 실패.** `orca worktree create --repo path:<워크트리>` 가 `repo_not_found`(응답은 「launch outcome unknown」으로 와서 원인이 가려짐) → `--repo id:<repoId>` 로 해결.
- **orca 가 `run-create` 없이 발주를 안 받음**(`run_required`) — 런북에 없는 단계.
- **DEMO 원장에 DAY 계정이 없어** 알림 행 1행은 로컬에서 검증 못 했다(받는 사람 계산은 시험이 덮음). prod 에서 이건학 = KOS 직무 「원장」 → 배포 재시작 때 `sync_master` 로 반영.

### prod 에서 같이 본 것 (이 작업 코드와 무관 · 기존)

- **「바로 시작」 KOS 집도의 쓰기 4/4 실패**(11-21 1 · 11-25 3 · `value not reflected`). 명동점 시스템 계정 직무가 의사 태그 없는 「ADMIN」이라 KOS 가 집도의로 받지 않았다(DEMO 는 「관리자」에 의사 태그 → 됨). 사용자가 KOS 에 「시스템」 직무(의사 태그 · 시스템 계정만)를 만들어 해결(16:02 DAY 반영). 「ADMIN 에 의사 태그 추가」는 직원 9명이 원장 목록에 들어가므로 피했다.
  - 이어진 것: DAY 는 「진행중」(DAY `started_at`) · KOS 는 READY 로 어긋남, 재시도 중 [종료] → KOS 400(고객 B), 판 원장 칸 「간호관리」가 안 뜸(KOS 집도의에 시스템이 없어서).
- **고객 A 「아무도 귀가 대기 안 했다」** → `event_log` `visit.home` 15:00:41 직원 한 명의 웹 세션(오늘 유일 세션). 마지막 시술이 끝나면 아래 버튼 자리가 [귀가 대기]로 바뀌고 확인 창이 없다. 그때 「방 점유/원장 상담」이 KOS 에서 취소(설계대로). 15:10 귀가 완료는 KOS 에서. API 접속 로그는 배포 재시작으로 없음.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-25 | KOS 호출도 DAY 원장 호출 알림 · 푸시(kind · 글자 그대로 · migration 없음) | 사용자 「간호사들이 코스 쓰는 경우가 잇는데 알림이 안와」 |
| 2026-11-25 | ~~prod 핫픽스 브랜치~~ → dev 에서 작업 · dev → prod ff(prod ⊂ dev) | 사용자 |
| 2026-11-25 | 백필은 나중 · 정식 앱 0.1.0 깨질 수 있음 수용 | 사용자 |
| 2026-11-25 | ~~prod 웹 고객 · 예약 화면 설정값으로 끔(SPEC-006 ⑭ · #284)~~ → 범위 밖 → 나중에 메뉴 링크만 빼기(#286 · dev · prod) | 사용자 「웹은 안해」 → 「막는 버튼만」 |
| 2026-11-25 | 수락 = `doctor_call_accept`(호출 안 닫음) · KOS 수락은 W1 거름 + READY 전이 | 코드 사실 · 문서 검수 r1 W1 · r2 R1 |
| 2026-11-25 | 지정 2명 이상 = 그 원장들(`called_doctor` · kind one 만) · 대표 = 가장 작은 sequence 의 첫 원장 | 사용자 결정 A2 · 검수 W5 · N1 · I3 |
| 2026-11-25 | 메아리 = op 시간 창 30초 · 옛 사본 = 앞으로만 + `kosCalledAt` 최댓값 | 문서 검수 W6 · 코드 검수 W1 |
| 2026-11-25 | 판정 경로에 `ext_sync` 포함 · date_sync · backfill 제외 | 워커 질문 · 코디 |
| 2026-11-25 | Delivery = main ready + review_surface 「원천 #965」 · 머지 뒤 v2 | 사용자 「우회해서 만들수 잇잖아」 |
| 2026-11-25 | 코드 검수 지적은 크기 상관없이 전부 | 사용자 「작은 지적도 해야지」 |
| 2026-11-25 | 「ci 말고 머지」 · prod 까지 바로(병원 지금 안 씀) | 사용자 |

## 5. 날짜별 로그

- `2026-11-25` 오전 — 질문 「KOS 에서 호출하면 DAY 로 와?」 → 코드 · dev DB 로 「값만 받고 알림 없음」 확인 → HAR 의사호출2 → 범위 결정
- planner 스펙 r1 → 검수 WARN 9 → r2 → WARN 6 → r3 → PASS → #965 → Delivery 막힘 2회 → #283 · #284 → #284 범위 밖으로 걷음 → #283 승인
- backend 1루프(시험 51 · 2902 passed) → 코드 검수 r1 WARN → be-fix-1(변이 9 · 2909 passed) → r2 PASS → be-fix-2(N1 · I-a) · planner sync-1(스펙 맞춤)
- 로컬 스택(11140 · DEMO) e2e-1: 지정 · 전체 · 여러 작업 · 재호출 · 메아리 0 · KOS 수락 O
- 14:05 #285 dev 머지 → 14:18 dev 배포 → 14:20 migrate-prod 0028 → 14:36 prod 배포 → 이건학 원장 반영
- #286 메뉴 막음 → 14:51 dev → 15:02 prod
- 오후 — prod 로그 조사(고객 A 귀가 대기 · 바로 시작 실패 원인 = 시스템 직무) → KOS 「시스템」 직무 → 16:02 DAY 반영
- 다음 작업 `day-room-board` 결정 · 새 코디로 넘김

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/965 → main `bf440f27`
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/285 → dev `1b5bba22` → prod
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/286 → dev `de0d0dab` → prod
- Delivery: CENTURION_DAY#283 · ~~#284~~ not planned
- 리포트: `review-doc-r1` ~ `r3-report.md` · `review-code-r1` · `r2-report.md` · `be-impl-r1` · `be-fix-1` · `be-fix-2` · `be-menu-hide-report.md` · `e2e-1-report.md` · `delivery-1-report.md`
- 인수인계: `handoff-day-room-board.md`

## 7. 잔여

- **prod 실물** — 간호가 KOS 에서 원장(이건학 등 DAY 계정 있는 원장) 지정 호출 → 앱 · 웹 알림 1번 · 판 「호출」(사용자 확인 대기).
- **시스템 직무 효과 확인** — 다음 「바로 시작」 → 「종료」 KOS 쓰기 둘 다 `confirmed` · 판 원장 칸 「간호관리」.
- **prod 고객 B 의 시술 하나** — DAY 진행중 · KOS READY(집도의 없음) 어긋남. 다시 [종료] 또는 KOS 에서 집도의 · 완료.
- **KOS 쓰기 실패 뒤 DAY ≠ KOS** — 바로 시작 KOS 실패에도 DAY 는 시작으로 남음 · 재시도 중 다음 동작 충돌 · [귀가 대기] 확인 창 없음 → 다음 작업 후보.
- **prod FCM 키** 없음(Android 0.1.0 은 FCM 없어 영향 없음 · 0.2.0 정식 전 Key Vault `day-prod-fcm-service-account`).
- **지난 이력 백필**(prod 0010 · 0011 · kos_keys) — 사용자 나중에.
- **정식 앱 0.2.0** 심사(prod 서버가 0.2.0 기준으로 올라감 · 0.1.0 호환 안 챙김).
- **배포 검사 중복** — 스쿼시 SHA 에도 같은 트리면 검사 재사용하는 길(핫픽스 시간 단축) 검토.
- **다음 작업 `day-room-board`** — 방 배정 자동 완료(시술 대기 진입 · 귀가 대기) · 방별 순 ①②③ — 새 코디 진행 중(`handoff-day-room-board.md`).

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-kos-call-notify/README|day-kos-call-notify]]
<!-- work-links:end -->
