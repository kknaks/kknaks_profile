
# [frontend] WORK-004 Phase 4~6 — 공용 오버레이 · 생성 드로어 · 상세/페이지 승격

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001~003 과 **WORK-004 Phase 1~3(업무 API)** 이 커밋돼 있다. 네 몫은 `app/front` 다 — **백엔드 코드를 건드리지 마라.**

먼저 확인해라: `git log --oneline -3` 에 `aec6222`(업무 도메인·API)가 보여야 한다. 안 보이면 **멈추고 물어라.**
그리고 **백엔드를 실제로 띄워서** 붙는다 — `make up && make migrate && make seed`.
**시드 값은 네 `.env` 에 채운다**(`.env.example` 은 비어 있는 게 맞다 — 자격증명을 레포에 두지 않는다).

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-004-tasks-crud.md` — **Phase 4·5·6 이 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 1~3(API)은 **이미 끝났다** — 다시 하지 마라. **§Internal Interface Contract 를 반드시 읽어라**

**계약**
- `20-spec/spec-003-tasks-crud.md` — **업무 계약**(U-1~ 화면·문구·CTA · Case Matrix · Data Contract)

**구조·규약 (여기서 라우트·디렉토리·규칙이 나온다)**
- `40-architecture/frontend/README.md` — **라우트 트리·디렉토리 구조·페칭·토큰→CSS 변수·오버레이·반응형·정적 빌드 제약**
- `40-architecture/system/README.md` — 구성·흐름(Tauri 셸의 역할)
- `40-architecture/backend/README.md` §10 · §8-2 — API 표면·에러 코드
- `40-architecture/frontend/README.md` **§6 오버레이 3종**(드로어 폭 840 고정 — 2026-09-06 규칙) · §5-3 색 렌더 · §3-3 캐시 무효화 · §11 테스트

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§v2 스코프 규칙**
- `00-design/09-design-tokens.md` · `디자인 시스템.dc.html` — **토큰 원본**(색·타입·간격·오버레이)

## 2. 배경 / 무엇을 만드나

업무 API 가 돈다(WORK-004 Phase 1~3). 네가 **업무를 만들고 여는 화면**을 만든다.

**이 그룹이 `DrawerFrame` 을 처음 세운다** — 회의·캘린더가 전부 그것을 쓴다. 화면보다 오버레이 프레임을 먼저 세운다(Phase 4).

끝나면 **앱 창에서 업무를 만들고, 열어서 고치고, ⤢ 로 전체 페이지로 넓힌다.**

## 3. 계약 — 못박힌 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 스택 | **Next.js 정적 빌드**(`output: 'export'`) + **shadcn/ui** + Tailwind + **TanStack Query v5** |
| 정적 빌드 제약 | **동적 세그먼트 금지**(전부 `?id=`) · 모든 `page` 는 `'use client'` · **Route Handler·미들웨어·Server Action 미사용** |
| 상태 | 서버 상태는 TanStack Query, UI 상태는 URL 쿼리 + 로컬. **전역 상태 라이브러리 없음.** `retry:false` |
| 색 | **컴포넌트에 hex 리터럴 금지** — 토큰을 CSS 변수로 등록하고 그것만 쓴다 |
| 오버레이 | Drawer 840 / Modal 600 / Popover 200–400. **드로어 위에 모달 금지** |
| 반응형 | **유동** — 1920 좌표는 참고값, absolute 금지 |
| **드로어 폭** | **840 고정.** `DrawerFrame` 이 **한 곳에서** 정하고 **폭을 prop 으로 받지 않는다**(`width`·`size`·`className` 금지). 다른 폭이 필요해 보이면 그건 드로어가 아니라 다른 표면이다. 유일한 예외는 **좁은 화면 전체화면 전환**이고 그 판정도 `DrawerFrame` 안이다(FE §6-2, 2026-09-06) |
| **`Sheet`·`Dialog` 직접 import 금지** | 화면은 `openDrawer`·`openConfirm` 만 부른다 — 그러면 규격이 화면마다 갈린다 |
| **상태 전이는 이번 범위가 아니다** | WORK-005 가 전용 엔드포인트로 소유한다. **상태를 바꾸는 UI 를 만들지 마라**(리스트 셀·칸반도 WORK-005) |
| **첨부** | **URL 링크만.** `kind=doc`(자료함 문서)은 서버가 거부한다 — 문서함 work 가 실체화한다. 화면에 자료함 선택 경로를 만들지 마라 |
| **재사용** | 팔레트·`TypeBadge`·`ColorDot`·`InlineEditText`(+`saveFailed` prop)·`AutoSaveFailureNotice`·`ConfirmModal`·`V2Gate` — **다시 만들지 마라** |
| **자동 저장** | 인라인 편집은 blur 저장. 실패는 **U-7 규격**(토스트 + 필드 표시 + 행 아래 「다시 저장」, **자동 재시도 없음**) |
| 캐시 | `['tasks']` 등록·무효화. 유형·프로젝트가 바뀌면 `['tasks']` 도 무효화(배지 이름·색이 딸려 있다) |
| 목록 응답 | `{ items: [...] }` — **`items` 를 꺼내는 것은 `api.ts` 까지** |
| v2 | UI 는 그리되 비활성 + 「v2에서 제공됩니다」 — 숨기지 않는다 |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 4** — 공용 오버레이·표시 컴포넌트(**`DrawerFrame` 신설**·`Selector`·상태/유형 표시)
**Phase 5** — 생성 드로어
**Phase 6** — 상세 드로어 · 전체 페이지 승격 · 인라인 편집 · 자식 블록

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 1~3(백엔드)은 이미 끝났다.** `app/back` 을 건드리지 마라.

**Phase 4 가 먼저인 이유** — `DrawerFrame` 은 **회의·캘린더가 전부 쓴다.** 화면부터 만들면 규격이
화면 안에 갇히고 다음 work 가 복제한다. WORK-003 에서 자동 저장 실패 표시가 그렇게 샜다(검수 F-1).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부 (`src-tauri` 포함)
- 루트 `Makefile`·`.gitignore` 는 **프론트 항목 추가만**(백엔드 항목을 고치지 마라)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
**`app/back/` 을 건드리지 마라.** **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. **먼저 `git log --oneline -3` 으로 `aec6222`(업무 API)를 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 4~6 + **§Internal Interface Contract**) → **SPEC-003** → 아키텍처 frontend **§6 오버레이**·§5-3·§3-3·§11.
3. **Phase 를 순서대로** 하고 각 Phase 끝에서 검증까지 통과시킨 뒤 다음으로 간다.
4. **앱 창에서 실제로 업무를 만들어** 확인한다(`make up`→`migrate`→`seed`→`app`). 이게 이 WP 의 최종 검증이다.
5. **테스트를 쓴다** — 드로어 폭이 한 곳에서만 정해지는지, 자동 저장 실패 표시가 U-7 대로인지.

## 7. 범위 제약 — 하지 말 것

- **Phase 1~3 을 다시 하지 않는다**(API 는 끝났다). `app/back` 을 건드리지 마라.
- **상태를 바꾸는 UI 를 만들지 않는다** — 리스트/칸반·상태 드롭다운·완료 게이트 전부 **WORK-005** 몫이다.
- **자료함 첨부 경로를 만들지 않는다**(서버가 거부한다).
- **복원 UI 를 만들지 않는다.**
- **shadcn 컴포넌트를 미리 다 설치하지 마라** — 이번에 필요한 것만.
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**WP 의 Phase 4~6 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히 **앱 창에서**:

- **제목 + 유형**만으로 업무가 만들어지는가. 유형을 안 고르면 「만들기」가 **비활성**인가
- 만든 업무를 **열어서 인라인으로 고치면 자동 저장**되는가
- **⤢ 로 전체 페이지로 승격**되고, 같은 내용이 보이는가
- 할일·메모·첨부(**URL 링크**)·연관이 붙는가
- **자동 저장 실패**: API 를 내리고 고치면 U-7 표시가 남고 **자동 재시도가 0건**인가(네트워크 탭)
- **상태를 바꾸는 UI 가 없는가**(WORK-005 몫)

**정적 검사도 적어라**:
- **`Sheet` 직접 import 0건** · **폭 리터럴(`840`·`w-[840px]`)이 `DrawerFrame` 밖에 0건**
- 컴포넌트 hex 0 · 인라인 style 0 · 실패 상태 `useState` 0 · 동적 세그먼트 0

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
