
# 재개 노트 — day-kos-call-notify (day)

**지금**: prod = de0d0dab(KOS 호출 알림 + 메뉴 막음) 배포 끝 · 사용자 prod 실물(KOS 호출 → 이건학 알림) 기다림 · 그 뒤 마감(#965 머지 · Delivery 재결속 · 회고 · 아카이브 · 로컬 스택 정리) | 이전: 코드 r2 PASS · be-fix-2 완료 · 로컬 스택 11140(--kos-demo --scheduler · day-local-39984074e7) → e2e-1 O(1~6 · OQ-99 = calledDoctors [] · OQ-106 같은 ms · 시계 차 +0.3/+4.2초) · 알림 행은 DEMO 원장 계정 없어 미검증 · #965 sync-1 fe203994 반영 끝
**다음**: planner done → reviewer_doc 같은 턴 발주 → 사용자 확인 → WP → 코드(be·fe) → dev 배포 → dev→prod ff

세팅: `scripts/new-work.sh day day-kos-call-notify` · 설정 SSOT `config/projects/day.json`
코디handle: `term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` (branch `kknaksss/day-kos-call-notify-spec`, base `origin/main` → PR `main`)
- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify` (branch `kknaksss/day-kos-call-notify`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] 원장 계정 알림 행 · iPad 시뮬레이터 · 웹 OS 알림 — 사용자에게 원장 계정 or dev 에서 확인
- [x] dev 배포 45551140415 success(05:18Z) · migrate-prod 45552733092 success(05:20Z · day_prod 0028) · prod ff a6aa4ba5..1b5bba22
- [x] Deploy DAY prod 45552966913 success(05:36Z) · prod 1b5bba22 · DB 0028 · login 200 · worker ERROR 0 · 배포 뒤 doctor_call 0(쏟아짐 없음) · 이건학 = 원장{doctor}(05:35 sync_master)
- [ ] prod 실물: 간호가 KOS 에서 이건학 지정 호출 → 앱 · 웹 알림(사용자)
- [x] menu-hide PR #286 → dev de0d0dab(dev 배포 05:51Z) → prod ff · Deploy DAY prod 45556457174 success(06:02Z) · prod HREFS = procedure 만
- [!] 마감 때: 워크트리 deploy/local.env · kos-demo.env(ignored · 정본에서 복사 · 포트 111xx) · 로컬 스택 stop · 볼륨 day-local-39984074e7
- [ ] 로컬 스택(코디) + KOS DEMO 실물 e2e(지정 · 전체 · 여러 작업) → OQ-99 · 106 닫기 · iPad 시뮬레이터
- [ ] #965 머지(구현 끝난 뒤) → v2 재결속
- [ ] 사용자 확인(planner 가 바꾼 것: A5 수락 = 호출 안 닫음 · A2 지정 2명 이상 = 전체 · 설정 `DAY_WEB_RESERVATION_CUSTOMER_ENABLED`) → 30-work WP
- [ ] 코드: backend(동기화 → doctor_call + after_call · 메아리 막기) · frontend(화면 열림 설정)
- [ ] 첫 실물: DEMO 에서 KOS 「전체 호출」만 1회 → calledDoctors 표현 확인(OQ)
- [ ] dev 배포 · 실물(KOS 지정/전체 호출 → 웹 OS 알림 · 앱 푸시) → 병원 마감 뒤 dev→prod ff · migrate-prod `--ref prod`(0009→0028) · prod FCM 키 · worker · beforeAfter
- [!] 지난 이력 백필은 나중(수동) · 정식 앱 0.1.0 깨질 수 있음 수용

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-25 | KOS 에서 건 호출도 DAY 원장 호출 알림 · 푸시(기존 kind doctor_call 그대로) | 사용자 「간호사들이 코스 쓰는 경우가 잇는데 알림이 안와」 |
| 2026-11-25 | ~~prod 핫픽스 브랜치~~ → dev 에서 작업 · dev→prod ff 로 전체 배포(prod ⊂ dev 확인) | 사용자 |
| 2026-11-25 | 백필은 나중 | 사용자 |
| 2026-11-25 | ~~prod 웹 고객 차트 · 예약 현황은 프론트에서 끔(설정값)~~ → **범위 밖 · 사용자가 직접**(코디 오독 · #284 not planned 닫음 · #965 에서 SPEC-006 ⑭ · 007 걷음) | 사용자 「웹은 안해 일단 알림 푸쉬만 · 웹을 끄는거는 내가 알아서」 |
| 2026-11-25 | 지정 2명 이상 = 그 원장들만(called_doctor 로 받는 사람 계산 · migration 없음) — planner r1 「전체」 기본값 뒤집음 | 검수 r1 W5 · 브리프 A2 |
| 2026-11-25 | Delivery = main b152d463 ready + review_surface 에 계약 원천 #965 명시 · 머지 뒤 v2 재결속(pending 은 target SPEC 이 main stable 이라 CLI 불가) | 사용자 「우회해서 만들수 잇잖아」 |
| 2026-11-25 | 규칙 40 판정 경로에 ext_sync(_load_date) 두 커밋도 포함 · date_sync · backfill 은 오늘 아님이라 제외 → 스펙 ㉚ 머리 「두 경로」를 코드 목록으로 맞출 것(코드 PR 뒤 spec sync) | backend 질문 · 코디 |
| 2026-11-25 | 코드 검수 지적은 크기 상관없이 전부 고친다 | 사용자 「작은 지적도 해야지」 |
| 2026-11-25 | W1: call_changed 앞으로만 + event_log kosCalledAt 최댓값 이하면 안 만듦(저장 규칙 무변경) · W2 합집합 · I3 대표 = 가장 작은 sequence · I1 EmrError 로 넓힘 | 코디(검수 r1) |
| 2026-11-25 | dev 머지 · prod 배포까지 바로(병원 지금 안 씀 · 마감 기다리지 않음) · prod FCM 키는 이번에 안 넣음(Android 0.1.0 FCM 없음) | 사용자 「prod도 머지 해서 배포 까지」 |
| 2026-11-25 | 웹 메뉴 예약 현황 · 고객 버튼 막기 — dev · prod 둘 다 · menu.py HREFS 3키 빼기(글자만) · 라우트 그대로 · 브랜치 kknaksss/day-menu-hide | 사용자 「막는 버튼만 잇으면 될듯」 · 「dev · prod 둘 다」 |
| 2026-11-25 | 이건학 prod 원장 = KOS 직무 원장 → 배포 재시작 때 sync_master 로 반영 확인(DB 직접 수정 안 함) | 사용자 「이건학에 원장 넣어주라」 |
| 2026-11-25 | 앱 실물 확인(시뮬레이터)은 iPad 시뮬레이터로 | 사용자 「우리 시뮬레이터는 아이패드로 하자」 |
| 2026-11-25 | 정식 앱 0.1.0 이 서버 업데이트 뒤 깨질 수 있음 수용 | 사용자 「응」 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_3c969939-da51-442e-ae55-14dff670d50f` | `task_5ba52f6a346b` | `ctx_75774ce5f1fc` | `day-kos-call-notify-spec-brief.md` | 완료 · release (Run `run_2551445f4847`) |
| reviewer_doc | `term_b8c205fc-71b5-43b2-93e6-db7f0b335e61` | `task_effb56b27860` | `ctx_1de2802cb867` | `day-kos-call-notify-review-doc-brief.md` | r1 WARN · release |
| planner r2 | `term_3c969939-da51-442e-ae55-14dff670d50f` | `task_8720c783a6e2` | `ctx_440019cf20f0` | `day-kos-call-notify-spec-r2-brief.md` | 완료 · release |
| reviewer_doc r2 | `term_b8c205fc-71b5-43b2-93e6-db7f0b335e61` | `task_6ec0dc6ea101` | `ctx_ecc2c1b2dff1` | `day-kos-call-notify-review-doc-r2-brief.md` | WARN · release |
| planner r3 | `term_3c969939-da51-442e-ae55-14dff670d50f` | `task_fe60714d2c45` | `ctx_565c2ba7c7b8` | `day-kos-call-notify-spec-r3-brief.md` | 완료 · release |
| planner delivery-1 | `term_3c969939-da51-442e-ae55-14dff670d50f` | `task_8243bd9cd219` | `ctx_943a1a54a949` | `planner-delivery-1-instructions.md` | 완료 · release |
| backend | `term_37cbc4e2-b360-4a0f-8b74-afb7507b05f8` | `task_a332bdfdd4b5` | `ctx_695cacb1d001` | `day-kos-call-notify-be-brief.md` | 1루프 완료 · release |
| reviewer code | `term_1b030364-a6be-4990-bbf2-1479ce60dbcb` | `task_f683afa04a6e` | `ctx_53a2156555d2` | `day-kos-call-notify-review-brief.md` | r1 WARN · release |
| backend fix-1 | `term_37cbc4e2-b360-4a0f-8b74-afb7507b05f8` | `task_1bc0be034550` | `ctx_414e55f065aa` | `be-fix-1-instructions.md` | 완료 · release |
| reviewer code r2 | `term_1b030364-a6be-4990-bbf2-1479ce60dbcb` | `task_88c31681d7ed` | `ctx_d63cb3fa2b2d` | `review-code-2-instructions.md` | 검수 중 |
| reviewer_doc r3 | `term_b8c205fc-71b5-43b2-93e6-db7f0b335e61` | `task_882d5765ead0` | `ctx_d99f1d744720` | `day-kos-call-notify-review-doc-r3-brief.md` | PASS · release |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/965 (a498d34b)
- Delivery: CENTURION_DAY#283 (WP-1 BE) · ~~#284 (WP-2 웹)~~ not planned
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/285 → dev `1b5bba22`
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>


## 다음 작업 후보 (이 작업 밖 · 2026-11-25 사용자)

- **방 배정(방 점유) 자동 완료** — 고객이 **시술 대기로 넘어올 때** KOS 「방 배정」 작업을 완료로(지금 = 귀가 대기 때 취소). 현장: KOS 카드에 「시술 진행중 + 방 배정 준비중」이 불편. 시술 대기 진입은 주로 KOS 에서 → 동기화가 단계 변화를 보고 DAY 가 완료 쓰기. **귀가 대기 때도 남은 방 배정은 「취소」 → 「완료」**(사용자 2026-11-25 「귀가 대기때도 완료 처리 하자」).
- **방별 순 탭** — 방 순서 = 방 목록 순(A_룸1 부터) · ① 빈 방 = **기존 `ui.empty_state`(빈 상자 아이콘 `empty-inbox`) + 글자 「방이 비었어요」**(KOS 와 같은 빈 상자 그림 · 사용자 2026-11-25 캡처) ② 시술 대기 이전(접수 · 상담 대기 · 상담 진행 · 방 있음) = **지금 카드 머리 · 고객 부분 그대로 + 내원 단계 한 줄**(오더 메모 · 시술 목록 · 버튼 없음) ③ 시술 대기 · 진행 = 지금 카드 그대로(사용자 2026-11-25 「그래야 수정이 덜」). 「방 배정」 줄은 어디에도 안 보임. ② 단계 줄 = **[색 점] 단계 이름** — 글자 = 예약 현황 원내 현황 `policies/reservation_inhouse.py` STAGES(접수 · 상담 대기 · 상담 진행) · 색 = `styles/app.css` 토큰 `--day-st-reception` · `--day-st-consult-wait` · `--day-st-consult`(사용자 2026-11-25 「예약현황 색깔 그대로 · [dot] 접수」). ② 경과 시간 = **넣음** · 지금 단계로 바뀐 때부터(`visit_flow_log`) · 표시는 DAY 판의 기존 경과 시간 모양 그대로(사용자 2026-11-25 「우리 시간 스타일로」). 미정 = / ② 마취 칩 · 방 옮기기 기본 = 안 보임 · 막음.
- prod 「바로 시작」 KOS 집도의 실패 = 명동점 시스템 계정 직무에 의사 태그 없음 → KOS 「시스템」 직무(의사 태그) 만들어 해결(16:02 DAY 반영) · 다음 바로 시작 → 종료 실물 확인 대기.
- 남는 것: KOS 쓰기 실패 때 DAY 시작 상태 남음(DAY≠KOS) · 재시도 중 다음 동작 충돌 · [귀가 대기] 확인 창 없음.

## 5. 이력 (최신이 위)

- `2026-11-25` 착수 · HAR 의사호출2 + dev DB 로 「동기화는 받는데 doctor_call 0건」 확인 · planner 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
