# [reviewer] WORK-006 검수 — 회의록 목록 · 생성 · 시작 전

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`)

```bash
git log --oneline b757e2a..HEAD    # a7e1bd4(be) · 2d6319e(fe)
git diff b757e2a...HEAD --stat
```

**대상** — `a7e1bd4`(백엔드 Phase 1~3) · `2d6319e`(프론트 Phase 4~6). 둘 다 커밋돼 있다.

**산출물** — `orchestration/work/docs-v1/work006-review-report.md` **1개**. 코디 워크트리에 쓴다.

## 1. 네 층으로 본다 — 코드가 아니라 문서 기준

문서는 코디 워크트리 절대경로로 읽는다.
`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | SoT | 무엇을 |
|---|---|---|
| **정책** | `10-decision/decision-003-meeting-notes.md` · `decision-001` · `decision-004` · `decision-005` | 소프트 딜리트 · 녹음 원본 보존 · 첨부 두 갈래 · v2 게이트 · 장소 없음 · 화자 이름 없음 · 자동 재시도 없음 |
| **아키텍처** | `40-architecture/backend/README.md` · `frontend/README.md` · `database/README.md` · `database/domains/meeting.md` | 계층 · ORM 경계 · schema/dto · 트랜잭션 · `Query(alias)` / 정적 빌드 · 색 토큰 · 오버레이 · tokenStore |
| **SPEC** | `20-spec/spec-006-meeting-setup.md` | §2 U-1~U-8 · §4 표면·Validation·**Case Matrix 11행이 그대로 구현됐나** · §6 Acceptance 22개 |
| **WP** | `30-work/work-006-meeting-setup.md` | Phase 1~6 범위를 지켰나 · **범위 밖을 건드리지 않았나** |

## ⛔ 2. 이번에 반드시 볼 축 — 코디가 지정한다

### 2-1. 공용 컴포넌트 재사용 — **두 번째 구현이 있으면 FAIL**

`frontend/README.md` L112 「`shared/` 는 두 영역 이상이 쓰는 것만」 · L163 「영역 사이 import 금지」.
**규칙은 문서에 있는데 지금까지 리뷰 축으로 지정한 적이 없다. 이번에 본다.**

```
프론트
  DrawerFrame 840      생성 드로어가 이 위에 얹혔나. features/meetings 안에 자체 프레임 0
  Selector             유형·프로젝트. 하단 「+ 새 프로젝트로 추가」 인라인 행이
                       components/shared/Selector.tsx 하나인가
                       — 고쳤다면 업무 생성 드로어(SPEC-003 U-1)가 깨지지 않았나
  첨부 팝오버 360       SPEC-003 U-7 그대로인가. 회의용 사본 0
  Calendar             한 벌인가 (기간 스테퍼 · 일시 입력 공유)
  ItemRow              h44 · 테두리 없음 · padding 0 16 · border-bottom #F1F2F5
  EmptyState · StatusDot · 배지 · 팔레트 8종
  V2Gate               로컬 업로드
  MeetingTopBar        **한 파일**인가 (waiting · headline 두 변형)
  isEnterSubmit()      lib/keyboard.ts 하나인가 — 새 IME 가드 0

백엔드
  schedule_service     겹침 검사·파생을 소비만 했나. 두 번째 구현 0
                       판정식 `start_at < :end AND end_at > :start` 가 한 파일에만
  build_detail()       정의가 1개인가. 표면마다 다른 조립 0
  _assert_allowed      상태 가드가 한 곳인가
```

### 2-2. 기획·정책에 없는 것이 화면에 있나

`spec-006` §7 「시안에 있으나 기획·정책에 없어 제외」 **18행**이 정본이다. 화면에 있으면 **FAIL**.

```
취소된 회의 행 · 「· 회의실 A」 · 「요약」 문단 + 「AI 생성」 배지 · PNG 첨부 행
유형 고정 칩 3종 · 「만들면 바로 회의 시작」 토글 · 「회의 정보 수정」 버튼
AI 안건 생성 일체(프롬프트 모드 칩 · 추천 안건 칩 · 전송 버튼 · 「초안을 만들어 줍니다」)
「MacBook Pro 마이크 · 내 목소리 등록됨」 푸터
```

**반대도 본다** — 정책에 있는데 없는 것. 삭제 모달 경고 문안(「녹음 원본은 지워지지 않고 서버에 남습니다」) · 한 줄 요약 바 · V2Gate 토스트.

### 2-3. 배지 문구

**DEC-003 §1 표: 회의 중 「대기」 / 종료 후·목록 「다음 논의로」.**
WORK-006 의 화면(목록 · 미리보기 · 시작 전)은 **전부 「다음 논의로」**여야 한다.

### 2-4. 워커가 판단을 요청한 것 — **코디가 이미 허용했다. FAIL 로 올리지 마라**

```
schedule_repository.py 에 「소프트 딜리트된 회의 제외」 조건 1줄 추가
  WP 는 「이 파일을 수정하지 않는다」였으나
  SPEC-006 §4 「회의를 지우면 schedule 조회에서 빠진다(행은 남는다)」가 그 필터를 요구한다
  → 코디 허용. **다만 그 조건이 업무 일정에 영향을 주지 않는지는 봐라**
```

### 2-4-b. 프론트 워커가 올린 확인 요청 2건 — **판정해라**

```
② AttachmentPopover 에 role="reference" 를 채워 버렸다
   워커 말: 「계약이 필수라서」
   → SPEC-003 U-7 · SPEC-006 U-7 을 열어 그 필드가 정말 필수인지,
     회의 첨부에서 그 값이 맞는지 판정해라

④ features/meetings → features/settings import 3건
   MeetingCreateDrawer.tsx L37·L38 · useAgendaAutoSave.tsx L26
   워커 말: 「tasks 선례를 답습했다」
   → frontend/README.md L163 「영역 사이 import 금지.
     공유가 필요하면 components/shared/ 나 lib/ 로 올린다.
     단 하나의 예외: 업무·회의 드로어를 캘린더가 재사용」
     이 import 가 그 예외에 해당하나? 아니면 shared/ 로 올려야 하나?
   → tasks 에도 같은 게 있으면 **둘 다** 지적하고, 어느 쪽으로 정리할지 적어라
```

**아래 5건은 코디가 이미 넘겼다. FAIL 로 올리지 마라** — ① PanelTabs 의 `--tm-ink`(시안 [09] 패널 탭이 Ink 밑줄) · ③ 드롭 영역만 `V2Gate`(「자료함에서 선택」은 실동작) · ⑤ 기본 일시 하루 끝 22:30–23:30 · ⑥ `V2Gate` 드롭 가로채기(요청 0 을 지키려면 필요) · ⑦ `AttachmentList onRemove` optional.

### 2-5. E2E 를 대체한 테스트

이번 발주는 **앱 창 실물 확인을 하지 않았다.** WP 의 「앱 창에서 …」 항목이 `vitest` 로 옮겨졌는지 보고,
**옮기지 못한 것이 「실물 확인 필요」로 정직하게 남았는지** 확인해라. **통과로 처리한 게 있으면 FAIL 이다.**

## 3. 판정

```
FAIL   계약·정책 위반, 또는 Phase 검증 항목 미충족  → 원 워커에게 수정 재발주
WARN   동작은 하나 규약 이탈, 또는 범위 밖 변경
PASS

항목마다 파일:줄 + 어긋난 문서의 절 번호를 단다
근거를 못 대면 싣지 않는다 — 추측으로 지적하지 마라
```

**「문서 공백」은 지적과 분리해 별도 절**에 모은다 — 정책이 안 정해 구현이 임의로 정한 것 · Case Matrix 에 없는 에러가 코드에 있는 것(또는 반대) · 문서끼리 모순되는 것. **어느 문서의 어느 절에 무엇이 필요한지**를 적어라.

## 4. 하지 마라

1. **코드를 고치지 마라. 테스트를 돌리지 마라**(필요하면 코디에 요청)
2. **문서를 고치지 마라** — 공백은 보고만
3. **취향으로 지적하지 마라.** 문서에 근거가 있는 것만
4. **커밋·push 하지 마라**
5. 산출물은 리뷰 리포트 **1개**뿐

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_3bd1b48b-0d0c-4acb-9a59-1ce280a83012 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-006 검수 완료" \
  --body "FAIL n · WARN n · 문서 공백 n / 공용 컴포넌트 재사용 판정(두 번째 구현 유무) / 기획·정책에 없는데 화면에 있는 것 / 정책에 있는데 없는 것 / 배지 문구 / E2E 대체 테스트와 「실물 확인 필요」 목록의 정직성 / 가장 심각한 3건"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-006 검수 완료. 상세는 인박스." --enter
```
