
# [frontend] WORK-001 Phase 3·4 — Next 정적 빌드 · shadcn · 토큰 · **Tauri 셸 결합**

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/work-001-scaffold`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** `app/back` 은 **이미 다른 워커가 끝내 커밋했다**(Phase 1·2). 네 몫은 `app/front` 다 — **백엔드 코드를 건드리지 마라.**

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-001-scaffold.md` — **Phase 3·4 가 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 1·2(백엔드)는 **이미 끝났다** — 다시 하지 마라

**계약**
- `20-spec/spec-000-scaffold.md` — 기동·환경변수·헬스체크·시드 계약

**구조·규약 (여기서 라우트·디렉토리·규칙이 나온다)**
- `40-architecture/frontend/README.md` — **라우트 트리·디렉토리 구조·페칭·토큰→CSS 변수·오버레이·반응형·정적 빌드 제약**
- `40-architecture/system/README.md` — 구성·흐름(Tauri 셸의 역할)
- `40-architecture/backend/README.md` §10 — **API 표면**(헬스체크 응답 형태)

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§v2 스코프 규칙**
- `00-design/09-design-tokens.md` · `디자인 시스템.dc.html` — **토큰 원본**(색·타입·간격·오버레이)

## 2. 배경 / 무엇을 만드나

백엔드는 이미 돈다(Phase 1·2 완료 — compose 로 Postgres·API 기동, `GET /api/health` 가 DB 왕복 포함 응답). 네가 **프론트의 바닥과 Tauri 셸**을 놓는다.

끝나면 **`tauri dev` 로 앱 창이 뜨고, 그 창이 로컬 백엔드에 붙어 「서버에 연결되었습니다」를 보여준다.** 이게 이 제품의 첫 E2E 다.

## 3. 계약 — 못박힌 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 스택 | **Next.js 정적 빌드**(`output: 'export'`) + **shadcn/ui** + Tailwind + **TanStack Query v5** |
| 정적 빌드 제약 | **동적 세그먼트 금지**(전부 `?id=`) · 모든 `page` 는 `'use client'` · **Route Handler·미들웨어·Server Action 미사용** |
| 상태 | 서버 상태는 TanStack Query, UI 상태는 URL 쿼리 + 로컬. **전역 상태 라이브러리 없음.** `retry:false` |
| 색 | **컴포넌트에 hex 리터럴 금지** — 토큰을 CSS 변수로 등록하고 그것만 쓴다 |
| 오버레이 | Drawer 840 / Modal 600 / Popover 200–400. **드로어 위에 모달 금지** |
| 반응형 | **유동** — 1920 좌표는 참고값, absolute 금지 |
| **Tauri** | **처음부터 포함**(§C-4). 백엔드는 로컬, 프론트는 `tauri dev` 앱 창. 셸이 맡는 것은 **마이크 권한·OS 키체인·파일 선택창**뿐 |
| 토큰 저장소 | **한 파일에서만** 다룬다 — 그 밖에서 키체인·localStorage 직접 호출 금지 (WORK-002 가 채운다. Phase 3·4 는 자리만) |
| v2 | UI 는 그리되 비활성 + 「v2에서 제공됩니다」 — 숨기지 않는다 |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 3** — Next 정적 빌드 · shadcn 세팅 · 토큰 · 연결 확인 화면
**Phase 4** — **Tauri 셸 결합**

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 1·2(백엔드)는 이미 끝났다.** `app/back` 을 건드리지 마라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부 (`src-tauri` 포함)
- 루트 `Makefile`·`.gitignore` 는 **프론트 항목 추가만**(백엔드 항목을 고치지 마라)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
**`app/back/` 을 건드리지 마라.** **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. 역할 문서 → WP(Phase 3·4) → SPEC-000 → 아키텍처 frontend·system.
2. **Phase 3 을 끝내고 검증까지 통과시킨 뒤** Phase 4 로 간다. 반쯤 만든 채로 넘어가지 않는다.
3. **토큰은 `09-design-tokens.md` 를 CSS 변수로 옮긴다** — shadcn 테마에 연결하고, 컴포넌트에서는 변수만 쓴다.
4. Phase 4 에서 **백엔드를 실제로 띄워 앱 창에서 연결을 확인**한다(`make up` 후 `tauri dev`). 이게 이 WP 의 최종 검증이다.
5. 각 Phase 의 **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 1·2 를 다시 하지 않는다**(백엔드는 끝났다).
- WORK-002·003 의 화면(로그인·설정)을 **미리 만들지 않는다.** 이번은 **바닥과 연결 확인 화면**까지다.
- **shadcn 컴포넌트를 미리 다 설치하지 마라** — Phase 3 에 필요한 것만.
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**WP 의 Phase 3·4 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히:

- `out/` 산출물에 **동적 세그먼트 경로가 없는가**
- 브라우저에서 연결 확인 화면이 **백엔드 헬스를 실제로 읽는가**
- **`tauri dev` 로 앱 창이 뜨고** 그 창에서 「서버에 연결되었습니다」가 보이는가
- 백엔드를 내리면 그 화면이 **연결 실패 상태**로 바뀌는가(성공으로 두면 실패다)
- 컴포넌트에 **hex 리터럴이 0** 인가

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
