# [reviewer] WORK-008 검수 — 종료 · 통합 · 편집 · 업무 연동

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`)

```bash
git log --oneline ac9ee5b..HEAD    # a48cbe2(be 1·2) · a5ae4c6(fe 3·4·6) · Phase 5
git diff ac9ee5b...HEAD --stat
```

**산출물** — `orchestration/work/docs-v1/work008-review-report.md` **1개**.

## 1. 네 층

```
정책       10-decision/decision-003 §4·§5·§6·§7 · decision-002(완료 게이트)
아키텍처    40-architecture/backend §6·§7·§8-2·§8-3 · frontend · database/domains/meeting.md M-19·M-20
SPEC       20-spec/spec-008 §2 U-1~U-11 · §4 · Case Matrix · §6 Acceptance 25개
           + spec-004(완료 게이트·같은 상태 409) · spec-003(업무 생성)
WP         30-work/work-008 Phase 1~6
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. 완료 게이트 우회 — **가장 중요하다. 여기가 뚫리면 FAIL**

```
work-005 L137  회의록의 「업무 갱신」이 PATCH /api/tasks/{id}/status 와
               task_service.change_status() **이 하나를 지난다**
               — 회의록 쪽에 판정 코드를 두지 않는다
work-005 L147  task.status 를 대입하는 코드는 change_status() 안에만
work-005 L294  우회하지 않는지를 WORK-008 이 검증 항목으로 확인한다
```

**직접 grep 해서 확인해라**

```
① task.status 에 값을 대입하는 코드가 change_status() 밖에 있나
② meeting_* 서비스가 TaskCompletionBlockedError 를 잡아 다르게 처리하나
③ 전이 그래프·완료 조건 판정이 meeting_* 에 있나
④ task_service.py 가 변경됐나 (변경 0 이어야 한다)
```

**게이트가 거부했을 때 아무것도 안 바뀌는지** — `task.status` · `due_date` · 메모 수 · `pending_change` DB 전후 비교가 테스트에 있나.
**같은 상태로 보낼 때 409 가 사용자에게 보이나**(SPEC-004 L478 — 보이면 안 된다).

### 2-2. 통합 규칙 — 모델을 믿었나

```
DEC-003 §4 L102   사람 줄 우선. AI 가 사람 문장을 다듬거나 바꾸지 않는다
DEC-003 OQ-7 L180 중복 판정은 유사도가 아니라 **구조**
```

**모델 출력에서 본문(`content`·`kind`·`detail`)을 읽는 코드가 있으면 FAIL 이다.** 참조 id 와 자리만 받아야 한다.
실패 5종(사람 줄 누락 · 이중 계승 · AI 중복 참조 · 참조 없음 · `headline` 누락/초과)이 테스트로 고정됐나.

### 2-3. 삭제 경계 (ERD M-20)

```
merged 만 지운다. human · ai · transcript · 녹음 · task 는 남는다
source_human_line_id · source_ai_line_id 로 이어진 원본을 지우지 않는다
안건 삭제·추가·상태 변경은 종료 후에 없다. 줄 순서 변경 없다
```

**DB 전후 비교 테스트가 있나.**

### 2-4. 공용 부품 — 세 work 가 공유하는 축

```
AgendaLineTree      **안에 track 비교 0** — WORK-007 이 세운 규칙을 008 이 깼나
                    008 은 agendas={merged} 로 부르기만 해야 한다
MeetingStatusBar    상단 바 **한 파일**. generating · failed · headline 변형.
                    두 번째 바(HeadlineBar · GeneratingBar 등)를 만들었나
MeetingDetailBody   전체 페이지와 상세 드로어가 **같은 본문**을 쓰나 (Phase 6 의 목적)
TranscriptPanel · PromptBar · DrawerFrame · ConfirmModal · Selector · TypeBadge
features 사이 import 0 · lib/ 훅 재사용
build_detail 1개 · _assert_allowed 1곳 · task_service 미변경
```

### ⛔ 2-4-b. **워커가 정적 검사를 완화했다 — 판정해라**

WORK-006 검수 W-1 에서 「`features/*` 사이 import 0」을 닫고 `static.test` 로 고정했다.
**Phase 5 워커가 그 검사를 「배럴 import 는 허용」으로 바꾸고 2건을 넣었다.**

```
features/meetings/components/LinkTaskDrawer.tsx:32
    canTransition · fetchRelationCandidates · TaskRelation   ← @/features/tasks
features/meetings/hooks/useMeetingTaskLink.tsx:33
    openTaskDetailDrawer · useTaskDoneToast                  ← @/features/tasks
```

워커 보고: 「`features/tasks` 는 `useTaskDoneToast` 추출 + 배럴 export 4개만,
static ⑨ 가 배럴 import 를 허용하는 점 명문화 여부」.

**판정할 것**

```
frontend/README.md §2 규칙 4 (L163)
  「영역 사이 import 금지. 공유가 필요하면 components/shared/ 나 lib/ 로 올린다.
   **단 하나의 예외**: 업무·회의 상세/생성 드로어는 캘린더·회의록이 재사용한다 —
   이 드로어들은 소유 영역에 두고 features/<소유영역>/components/ 에서 직접 import 한다」

① openTaskDetailDrawer 는 그 예외에 해당하나? (업무 상세 드로어를 회의록이 연다)
② canTransition · fetchRelationCandidates · useTaskDoneToast 셋은?
   드로어가 아니라 로직·훅·API 다. lib/ 로 올려야 하나?
③ **정적 검사를 완화한 것 자체**가 옳은가 — 코드를 고치는 대신 가드를 연 것인가,
   아니면 규칙 문면이 실제 필요를 못 담고 있어 문서(FE §2)를 고쳐야 하는가
```

**②가 「올려야 한다」면 FAIL 이다**(직전 라운드에 닫은 규칙이 다시 열렸다).
**「예외가 맞다」면 문서 공백으로 올려라** — FE §163 의 예외 문면이 드로어만 말하는데 실제로는 더 넓다.

### 2-5. 편집 저장 경계

```
본문 · 종류 · 안건 이름   포커스 해제 자동 저장
줄 삭제                  **확인 모달 600**. 자동 저장이 아니다
「되돌리기」               없다
```

### 2-6. 그리지 않았나 (SPEC-008 §7 제외 목록)

```
되돌리기 · 보기 모드 프롬프트 바 · 근거 구간 수동 선택/「구간 추가」
「비워두면 …」 캡션 · 「시작 상태」 셀렉터 · 「연관 업무로 바꾸기」 토글+캡션
고정 유형명 「미팅·회의」 · 후보 목록 「대기·진행 중」
```

**있어야 하는 것** — 편집 중 **안건 제목 입력 상자**(결정 ②로 계약이 됐다) · 안건 배지 **「다음 논의로」** ·
한 줄 요약 바(`headline` null 이면 안 그림) · 「다시 생성」은 `ended+failed` 에서만.

### ⛔ 2-7. 통과 판정의 정직성 — **이번 work 에서 두 번 뚫렸다**

```
Phase 1·2   워커 「507 passed」  →  전체 스위트에서 1 failed (순서 의존). 코디가 잡음
Phase 3·4·6 워커 「283 passed」  →  Unhandled Rejection 1건.        코디가 잡음
```

**보고서의 숫자를 믿지 말고 네가 확인해라** — 단 **테스트를 돌리지는 마라**(read-only).
대신 **테스트 코드를 읽고** ① 단독 실행에만 의존하는 픽스처가 있나 ② 뮤테이션 거부를 받는 자리가 없는 경로가 있나를 본다.

### 2-8. E2E 대체 · 실물 확인 필요

앱 창 실물 확인을 하지 않았다. WP 의 「앱 창에서 …」·「네트워크 탭 실측」 항목이 테스트로 옮겨졌나,
**못 옮긴 것이 정직하게 남았나.** 통과로 처리한 게 있으면 **FAIL**.

**WORK-006·007 의 「실물 확인 필요」와 합쳐 한 표로 만들어라.** 사용자가 아침에 이걸로 확인한다.

### 2-9. 코디가 이미 판정한 것 — FAIL 로 올리지 마라

```
POST …/lines 응답이 LineItem 이다(MeetingDetail 전체 아님) — SPEC-007 §4. 코디 판정
service 의 _default_session_scope 안 commit() — BE §7 「백그라운드는 단계마다 세션·커밋」.
  도메인 로직이 커밋하는 게 아니라 요청 경계가 없는 자리의 get_db 대역이다
meeting_service.start() 의 commit() 1건 — BE §2 vs §7 규약 충돌. **문서 대기 중**(W-1)
웜스타트 실패 뒤 회의 상태 — 정책 공백. **사용자 결정 대기**(D-2)
```

## 3. 판정

```
FAIL / WARN / PASS. 항목마다 파일:줄 + 어긋난 문서의 절 번호
근거를 못 대면 싣지 마라
```

**「문서 공백」은 별도 절.** **WORK-006·007 에서 남은 공백의 현재 상태도 함께 적어라** —
G-3(문서함 임시 계약) · G-5(훅 층) · G-6(`ItemRow` 규격) · G-9(enums 경로) · W-1 · D-1 · D-2 · D-5 · D-8.

## 4. 하지 마라

1. **코드·테스트·문서를 고치지 마라. 테스트를 돌리지 마라**
2. **취향으로 지적하지 마라**
3. **커밋·push 하지 마라**

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_35404f8b-07cf-460e-8d73-d4e4870243c9 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-008 검수 완료" \
  --body "FAIL n · WARN n · 문서 공백 n / **완료 게이트 우회 4항목 grep 판정** / 통합 규칙(모델 본문 읽기·실패 5종) / 삭제 경계 DB 전후 / 공용 부품(track 비교·상단 바·DetailBody) / 편집 저장 경계 / 안 그린 것·있어야 하는 것 / **통과 판정의 정직성** / 실물 확인 필요 통합표(006·007·008) / 006·007 문서 공백의 현재 상태 / 가장 심각한 3건"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-008 검수 완료. 상세는 인박스." --enter
```
