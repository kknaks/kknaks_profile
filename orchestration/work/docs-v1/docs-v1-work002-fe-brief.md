
# [frontend] WORK-002 Phase 2·3 — 로그인 화면 · 토큰 저장소 · 설정 셸 + 검수 지적 1건

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001(스캐폴딩)과 **WORK-002 Phase 1(인증 API)** 이 이미 커밋돼 있다. 네 몫은 `app/front` 다 — **백엔드 코드를 건드리지 마라.**

먼저 확인해라: `git log --oneline -3` 에 `37a8ce1`(인증 API)이 보여야 한다. 안 보이면 **멈추고 물어라.**
그리고 **백엔드를 실제로 띄워서** 붙는다 — `make up && make migrate && make seed`. 시드 계정은 **`kknaks` / `dev1234!`** 다.

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-002-auth-session.md` — **Phase 2·3 이 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 1(인증 API)은 **이미 끝났다** — 다시 하지 마라

**계약**
- `20-spec/spec-001-auth-session.md` — **인증 계약**(UX·시나리오·API·Case Matrix). 화면 문구·상태가 여기 있다

**구조·규약 (여기서 라우트·디렉토리·규칙이 나온다)**
- `40-architecture/frontend/README.md` — **라우트 트리·디렉토리 구조·페칭·토큰→CSS 변수·오버레이·반응형·정적 빌드 제약**
- `40-architecture/system/README.md` — 구성·흐름(Tauri 셸의 역할)
- `40-architecture/backend/README.md` §10 · §8-2 — **API 표면과 에러 코드**(프론트가 분기할 키)

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§v2 스코프 규칙**
- `00-design/09-design-tokens.md` · `디자인 시스템.dc.html` — **토큰 원본**(색·타입·간격·오버레이)

## 2. 배경 / 무엇을 만드나

인증 API 가 돈다(WORK-002 Phase 1 — 로그인·갱신·로그아웃·세션 4표면). 프론트 골격과 Tauri 셸도 서 있다(WORK-001). 네가 **로그인 화면과 세션 파이프라인**을 만든다.

끝나면 **앱 창에서 `kknaks` / `dev1234!` 로 로그인해 들어가고, 앱을 껐다 켜도 유지되고, 로그아웃하면 다시 로그인 화면으로 돌아온다.**

## 3. 계약 — 못박힌 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 스택 | **Next.js 정적 빌드**(`output: 'export'`) + **shadcn/ui** + Tailwind + **TanStack Query v5** |
| 정적 빌드 제약 | **동적 세그먼트 금지**(전부 `?id=`) · 모든 `page` 는 `'use client'` · **Route Handler·미들웨어·Server Action 미사용** |
| 상태 | 서버 상태는 TanStack Query, UI 상태는 URL 쿼리 + 로컬. **전역 상태 라이브러리 없음.** `retry:false` |
| 색 | **컴포넌트에 hex 리터럴 금지** — 토큰을 CSS 변수로 등록하고 그것만 쓴다 |
| 오버레이 | Drawer 840 / Modal 600 / Popover 200–400. **드로어 위에 모달 금지** |
| 반응형 | **유동** — 1920 좌표는 참고값, absolute 금지 |
| **인증 전송** | **Bearer**(쿠키 없음). `Authorization: Bearer <access>` |
| **토큰 보관** | 「로그인 상태 유지」 체크 시 refresh 를 **OS 키체인**에, 미체크면 **메모리에만**. **브라우저 저장소 폴백을 두지 마라** — 셸이 없으면 `persist=true` 요청에 **예외를 던진다**(DEC-001 §4, 2026-09-05 개정) |
| 토큰 저장소 | **`tokenStore` 한 파일에서만** 다룬다 — 그 밖에서 키체인·localStorage 직접 호출 금지 |
| 갱신 | access 만료 시 **refresh 로 1회 갱신**하고, 실패하면 로그인 화면으로. **재시도를 반복하지 마라** |
| **주의** | 로그아웃한 refresh 를 다시 보내면 **재사용 감지가 걸려 그 계정 세션이 전부 끊긴다**. 로그아웃 뒤 갱신을 재시도하면 안 된다 |
| 에러 | 헤더없음·만료·위조가 **전부 401 `token_expired`** 로 온다(사유 비노출). 프론트는 갱신 1회로 종결 |
| v2 | UI 는 그리되 비활성 + 「v2에서 제공됩니다」 — 숨기지 않는다 |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 2** — 토큰 저장소 · 요청 파이프라인 · 로그인 화면
**Phase 3** — 설정 셸 · 로그아웃 모달 · v2 표시 컴포넌트

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 1(백엔드)은 이미 끝났다.** `app/back` 을 건드리지 마라.

### 함께 고칠 것 — WORK-001 검수 지적 (W-2)

`app/front/tailwind.config.ts:114` `gutter` 가 **1440 에서 96px** 인데 아키텍처 `frontend §7-1` 표는 **80px** 이다.
단일 `clamp` 로는 「1280~1439 는 48 고정 / ≥1440 은 80→240 보간」 두 구간을 함께 만족시킬 수 없다.

→ **구간을 나눈다.** 예) 기본 `--gutter: 48px`, `@media (min-width:1440px)` 에서 `clamp(80px, …, 240px)`.
Tailwind `spacing.gutter` 가 그 변수를 가리키게 한다. 지금은 한 화면만 쓰지만 **이후 전 화면이 이 값을 탄다.**

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부 (`src-tauri` 포함)
- 루트 `Makefile`·`.gitignore` 는 **프론트 항목 추가만**(백엔드 항목을 고치지 마라)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
**`app/back/` 을 건드리지 마라.** **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. **먼저 `git log --oneline -3` 으로 `37a8ce1`(인증 API)을 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 2·3) → **SPEC-001** → 아키텍처 frontend §3·§4.
3. W-2 gutter 정정을 먼저 해치운다.
4. **Phase 2 를 끝내고 검증까지 통과시킨 뒤** Phase 3 으로 간다.
5. **앱 창에서 실제로 로그인**해 확인한다(`make up`→`migrate`→`seed`→`app`). 이게 이 WP 의 최종 검증이다.
6. 각 Phase 의 **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 1 을 다시 하지 않는다**(인증 API 는 끝났다). `app/back` 을 건드리지 마라.
- WORK-003 의 화면(유형·프로젝트 관리)을 **미리 만들지 않는다.**
- **회원가입·비밀번호 찾기 링크를 만들지 마라** — 정책상 없다(SPEC-001, 하단 3링크는 v2 게이트).
- **shadcn 컴포넌트를 미리 다 설치하지 마라** — 이번에 필요한 것만.
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**WP 의 Phase 2·3 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히 **앱 창에서**:

- **`kknaks` / `dev1234!` 로 로그인**해서 들어가는가
- 틀린 비밀번호면 **SPEC-001 Case Matrix 의 문구**가 뜨는가 (어느 쪽이 틀렸는지 말하지 않는가)
- **「로그인 상태 유지」 체크 후 앱을 껐다 켜면 로그인이 유지**되는가. **미체크면 로그아웃**되는가
- **로그아웃하면 로그인 화면으로** 돌아가고, 그 뒤 **갱신을 재시도하지 않는가**(재사용 감지가 걸리면 실패다)
- `tokenStore` **밖에서 키체인·localStorage 호출이 0** 인가
- 컴포넌트에 **hex 리터럴이 0** 인가 · gutter 가 **1440 에서 80px** 인가(W-2)

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
