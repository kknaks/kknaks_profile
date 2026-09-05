
# [frontend] WORK-003 Phase 2·3 — 팔레트 토큰 · 배지/dot 공용 · 업무 설정 화면

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001·002 와 **WORK-003 Phase 1(유형·프로젝트 API 8표면)** 이 커밋돼 있다. 네 몫은 `app/front` 다 — **백엔드 코드를 건드리지 마라.**

먼저 확인해라: `git log --oneline -3` 에 `ffc544d`(유형·프로젝트 API)가 보여야 한다. 안 보이면 **멈추고 물어라.**
그리고 **백엔드를 실제로 띄워서** 붙는다 — `make up && make migrate && make seed`.
**시드 값은 네 `.env` 에 채운다**(`.env.example` 은 비어 있는 게 맞다 — 자격증명을 레포에 두지 않는다).

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-003-work-settings.md` — **Phase 2·3 이 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 1(API)은 **이미 끝났다** — 다시 하지 마라. **§Internal Interface Contract 를 반드시 읽어라** — 후속 work 가 의존하는 접점이 거기 있다

**계약**
- `20-spec/spec-002-work-settings.md` — **업무 설정 계약**(U-1~U-8 화면·문구·CTA · Case Matrix · **팔레트 8종 Data Contract**)

**구조·규약 (여기서 라우트·디렉토리·규칙이 나온다)**
- `40-architecture/frontend/README.md` — **라우트 트리·디렉토리 구조·페칭·토큰→CSS 변수·오버레이·반응형·정적 빌드 제약**
- `40-architecture/system/README.md` — 구성·흐름(Tauri 셸의 역할)
- `40-architecture/backend/README.md` §10 · §8-2 — API 표면·에러 코드
- `40-architecture/frontend/README.md` **§5-3 색 렌더**(`data-color-token`, 인라인 hex 금지) · §3-3 캐시 무효화 · §11 테스트

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§v2 스코프 규칙**
- `00-design/09-design-tokens.md` · `디자인 시스템.dc.html` — **토큰 원본**(색·타입·간격·오버레이)

## 2. 배경 / 무엇을 만드나

유형·프로젝트 API 가 돈다(WORK-003 Phase 1). 로그인도 된다(WORK-002). 네가 **업무 설정 화면**을 만든다 — **업무·회의·캘린더가 전부 이 색과 컴포넌트를 쓰게 되므로, 화면보다 팔레트·공용 컴포넌트를 먼저 세운다.**

끝나면 **앱 창에서 유형과 프로젝트를 만들고, 이름·색을 고치고, 지운다.** 기본 3종은 색만 바뀐다.

## 3. 계약 — 못박힌 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 스택 | **Next.js 정적 빌드**(`output: 'export'`) + **shadcn/ui** + Tailwind + **TanStack Query v5** |
| 정적 빌드 제약 | **동적 세그먼트 금지**(전부 `?id=`) · 모든 `page` 는 `'use client'` · **Route Handler·미들웨어·Server Action 미사용** |
| 상태 | 서버 상태는 TanStack Query, UI 상태는 URL 쿼리 + 로컬. **전역 상태 라이브러리 없음.** `retry:false` |
| 색 | **컴포넌트에 hex 리터럴 금지** — 토큰을 CSS 변수로 등록하고 그것만 쓴다 |
| 오버레이 | Drawer 840 / Modal 600 / Popover 200–400. **드로어 위에 모달 금지** |
| 반응형 | **유동** — 1920 좌표는 참고값, absolute 금지 |
| **팔레트 8종** | `indigo`·`violet`·`steel`·`mint`·`sky`·`amber`·`rose`·`graphite`. **프론트는 `tokens.css` 한 곳에서만 정의**한다(서버는 이미 한 곳) |
| **색 렌더** | 컴포넌트는 **`data-color-token="<name>"`** 을 받고 CSS 가 변수 쌍을 고른다. **인라인 `style` 로 hex 금지**(FE §5-3). 팔레트에 없는 토큰명이 오면 **중립 색으로 떨어뜨리고 항목을 숨기지 않는다** |
| **기본 유형 3종** | **색만 편집.** 화면이 컨트롤을 감춰도 **서버 판정이 정본**이다(`work_type_locked`) — **두 겹으로 막는다** |
| **자동 저장** | 인라인 편집은 blur 저장. **실패는 토스트 + 해당 필드 실패 상태**, **자동 재시도 없음**. 해제는 「다시 저장 성공」 또는 「재편집 후 저장 성공」 **둘뿐** — 시간 경과로 사라지지 않는다 |
| **오버레이** | 색 고르기는 **팝오버**, 삭제 확인은 **모달 600**. 「한 줄짜리 개체는 인라인」·「드로어 위 모달 금지」 |
| 캐시 | `['workTypes']`·`['projects']`. **`['tasks']`·`['meetings']` 키는 등록만** 해 두고 무효화 연결은 소비 그룹에서(지금은 그 키가 없다) |
| 목록 응답 | `{ items: [...] }` — **`items` 를 꺼내는 것은 `api.ts` 까지**이고 훅 위로는 배열이 올라간다 |
| v2 | UI 는 그리되 비활성 + 「v2에서 제공됩니다」 — 숨기지 않는다 |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 2** — 팔레트 토큰 · 배지/dot 공용 컴포넌트
**Phase 3** — 업무 설정 화면 · 자동 저장 · 삭제 모달

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 1(백엔드)은 이미 끝났다.** `app/back` 을 건드리지 마라.

**Phase 2 가 먼저인 이유** — 팔레트와 배지·dot 은 **업무·회의·캘린더가 전부 쓴다.** 화면부터 만들면
색이 화면 안에 갇히고 다음 work 가 복제한다. 공용 컴포넌트를 세우고 그 위에 화면을 얹는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부 (`src-tauri` 포함)
- 루트 `Makefile`·`.gitignore` 는 **프론트 항목 추가만**(백엔드 항목을 고치지 마라)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
**`app/back/` 을 건드리지 마라.** **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. **먼저 `git log --oneline -3` 으로 `ffc544d`(유형·프로젝트 API)를 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 2·3 + **§Internal Interface Contract**) → **SPEC-002** → 아키텍처 frontend §5-3·§3-3·§11.
3. **Phase 2 를 끝내고 검증까지 통과시킨 뒤** Phase 3 으로 간다.
4. **앱 창에서 실제로 유형·프로젝트를 만들어** 확인한다(`make up`→`migrate`→`seed`→`app`). 이게 이 WP 의 최종 검증이다.
5. 각 Phase 의 **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.
6. **테스트를 쓴다** — `frontend §11` 필수 항목 중 이 범위에 걸리는 것(색 렌더·자동 저장 실패 표시). WORK-002 가 Vitest+RTL+MSW 를 이미 붙여놨다.

## 7. 범위 제약 — 하지 말 것

- **Phase 1 을 다시 하지 않는다**(API 는 끝났다). `app/back` 을 건드리지 마라.
- **유형·프로젝트를 「고르는」 화면**(업무 생성 드로어·필터)을 만들지 않는다 — 소비 그룹 몫이다.
- **집계 카운트(「이번 달 8건」)를 만들지 않는다** — v1 에 없다(S002-OQ-3).
- **복원 UI 를 만들지 않는다** — v1 에 없다.
- **shadcn 컴포넌트를 미리 다 설치하지 마라** — 이번에 필요한 것만.
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**WP 의 Phase 2·3 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히 **앱 창에서**:

- 유형을 **종류·이름·색**으로 만들고 목록에 나오는가
- **기본 3종**: 이름 편집·삭제 컨트롤이 **없고**, **색은 바뀌는가**
- 같은 이름으로 또 만들면 **SPEC-002 Case Matrix 문구**가 뜨는가
- 삭제 확인 **모달 600** 이 뜨고, 지우면 목록에서 빠지는가
- **자동 저장 실패**: 네트워크를 끊고 이름을 고치면 **토스트 + 그 필드에 실패 표시**가 남고, **재시도가 자동으로 나가지 않는가**(네트워크 탭 확인)
- 컴포넌트에 **hex 리터럴이 0** 인가 · 색이 전부 **`data-color-token`** 으로 그려지는가
- 프로젝트 쪽도 같은 흐름이 도는가

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
