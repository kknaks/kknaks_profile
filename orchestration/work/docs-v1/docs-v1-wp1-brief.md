
# [architect] WP 1그룹 — WORK-001 스캐폴딩 · 002 로그인·세션 · 003 업무 설정

너는 **task-management `architect` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**⚠ 이 워크트리는 코디네이터와 공유한다.** §5 가 지정한 파일 외에는 **만들거나 고치지 마라.** git 은 읽기만.

## 1. SSOT — 먼저 읽을 것

경로는 전부 `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/` 기준.

**양식 (반드시 따를 것)**
- `templates/projects/30-work/work.md` — **이 구조를 그대로 쓴다.** Meta / Work Summary / Role Assignment / Scope / Code Surface / Domain·Schema / Dependency / Internal Interface Contract / **Execution(Phase 별 Status·작업·검증·완료 증거)** / Pre-deploy Check / Rollback / Done Criteria / Open Issues / Related
- `templates/projects/30-work/README.md` — 인덱스 양식(코디가 채운다, 참고만)

**계약 (이 WP 가 구현할 것)**
- `para/projects/summer-star/task-management/20-spec/spec-000-scaffold.md`
- `.../spec-001-auth-session.md`
- `.../spec-002-work-settings.md`

**구조·규약 (여기서 파일 경로·계층이 나온다)**
- `.../40-architecture/backend/README.md` — 계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약
- `.../40-architecture/frontend/README.md` — 라우트·디렉토리·페칭·토큰·오버레이·반응형
- `.../40-architecture/system/README.md` — 구성·흐름
- `.../40-architecture/database/README.md` (+ `domains/account.md`) — ERD·불변식

**정책 (참조)**
- `.../10-decision/decision-001-auth-settings.md`

## 2. 배경 / 무엇을 바꾸나

v1 spec 12건이 다 섰다. 이제 **WP(빌드 계획)** 를 쓴다 — **dev 가 이 문서만 보고 PR 을 나누고 작업을 시작할 수 있어야** 한다.

이번은 **1그룹(SPEC-000~002)** 이다. 사용자가 **기능 하나를 만들고 실제 앱 창에서 E2E 로 확인한 뒤 다음으로 넘어가는** 방식이라, WP 도 그 단위로 끊는다.

## 3. 계약 — 이미 확정된 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| **코드 레포** | **별도 clone** — `github.com/kknaks/task_management`. **이 워크트리(`kknaks_profile`)에 코드를 만들지 않는다.** 이 레포의 `app/back` 은 다른 제품이다 |
| 개발 방식 | **처음부터 Tauri 포함.** 백엔드 로컬 + 프론트 `tauri dev` 앱 창. 기능마다 실제 셸에서 E2E 검증 |
| 타깃 | v1 에 **macOS · Windows 둘 다** |
| 프론트 | Next.js **정적 빌드**(`output: 'export'`) + shadcn/ui + Tailwind + TanStack Query v5. **동적 세그먼트 금지**(전부 `?id=`), 모든 page 는 `use client`, 미들웨어 없음, 전역 상태 라이브러리 없음 |
| 백엔드 | FastAPI + **uv**, router→service→repository, **schema(FE 계약) / dto(내부)**, **Postgres 비동기** |
| 인증 | **Bearer**(쿠키 없음). access 1h / refresh 7d. 「유지」 체크 시 **OS 키체인**, 미체크 시 메모리. **토큰 저장소는 한 곳에서만 다룬다** |
| 계정 | **DB 시드로만 생성** |
| AI 런타임 | **open-kknaks 의 codex** — 호스트 바이너리 **바인드 마운트**. Anthropic/OpenAI SDK 직접 import 금지 (1그룹 범위 밖이지만 스캐폴딩이 자리를 잡는다) |
| 실패 | **설계한 실패만 처리, 그 밖은 fallback 없이 전파.** `except Exception` 금지·임의 재시도 금지·조용한 기본값 금지 |

## 4. WP 를 쓸 때 지킬 것

- **spec 의 외부 계약 본문을 복제하지 마라.** frontmatter `links.specs` 로 연결하고, WP 에는 **어떻게 만들 것인가**(파일·순서·검증)를 쓴다
- **`Code Surface` 에 실제 파일 경로 후보**를 적는다 — 아키텍처의 디렉토리 트리를 따른다. 이게 spec 과 WP 의 결정적 차이다
- **Phase 는 PR 단위로 끊는다.** 각 Phase 에 `Status` · 작업 체크리스트 · **검증 체크리스트** · 완료 증거 칸
- **검증은 사용자가 앱 창에서 직접 확인하는 문장**으로 — spec 의 Acceptance 를 실행 절차로 옮긴다
- Phase 순서는 **의존이 적은 것부터**. 앞 Phase 가 끝나면 그 자체로 돌아가야 한다(반쯤 만든 상태로 다음으로 넘어가지 않게)
- `Rollback` 은 실제로 되돌리는 절차를 적는다(migration revert·브랜치 폐기 등)
- 정하지 못한 것은 `Open Issues` 로. **임의 결정 금지**

## 5. allowed_paths — 이 밖은 건드리지 마라

`para/projects/summer-star/task-management/30-work/` 아래 **신규 3건만**:

1. `work-001-scaffold.md` — **SPEC-000**. 레포 초기화·Tauri 셸·Next 정적·shadcn 세팅·FastAPI+uv·Postgres·compose·마이그레이션 도구·시드 계정·헬스체크. **완료 = `tauri dev` 로 앱 창이 뜨고 백엔드 헬스체크가 보인다**
2. `work-002-auth-session.md` — **SPEC-001**. 로그인 화면·Bearer 발급/갱신·키체인 저장소·세션 가드(레이아웃 컴포넌트)·로그아웃·확인 모달·v2 게이트 컴포넌트. **완료 = 로그인해서 들어가고 앱을 껐다 켜도 유지된다**
3. `work-003-work-settings.md` — **SPEC-002**. 유형·프로젝트 CRUD(백+프론트)·팔레트 8종 토큰·인라인 추가 행(종류 셀렉터)·색 팝오버·삭제 모달·소프트 딜리트. **완료 = 유형과 프로젝트를 만들고 고치고 지운다**

**id 는 `WORK-001`·`WORK-002`·`WORK-003`, `status: todo`, `work_type: new-feature`.**
frontmatter `links.specs`·`links.decisions`·`links.works`(의존)를 채워라.

그 외 일체 금지 — spec·정책서·아키텍처·index·log 는 **코디네이터 소관**. 커밋·push 금지.
**코드를 만들지 마라** — WP 는 계획 문서다.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT(양식 → spec 3건 → 아키텍처).
2. **WORK-001 스캐폴딩** — Phase 를 「레포·백엔드 기동 / DB·마이그레이션·시드 / 프론트 정적+shadcn / Tauri 셸 결합」 정도로 끊고, **각 Phase 끝에서 무엇이 돌아가는지**를 검증에 적어라. `repos.code` 추가가 필요한 것도 Open Issues 나 Meta 의 External dependency 에 남긴다.
3. **WORK-002 로그인·세션** — 백(토큰 발급·갱신·시드 계정) → 프론트(로그인 화면·저장소·가드) 순. **토큰 저장소 추상화**가 한 파일에 갇히는지 검증에 넣어라.
4. **WORK-003 업무 설정** — 백 CRUD → 프론트 화면. **팔레트 8종을 CSS 변수로 등록**하는 것이 여기 들어간다(SPEC-002 §4).
5. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- **코드를 만들지 않는다.** WP 문서 3건만.
- spec 계약 본문을 복제하지 않는다 — 링크로.
- 2그룹 이후(내 업무·문서함·회의록·캘린더·설정·메시지함)는 **이번 범위가 아니다.**
- 이 워크트리에 코드 디렉토리를 만들지 않는다 — 코드는 **별도 레포**다.
- 선택지를 나열하지 않는다 — **하나로 정하고 근거를 단다.**

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. DEC-001~006 을 어기는 구조를 제안하지 않았는지 자기점검(충돌 발견 시 고치지 말고 Open Questions). 사용자가 못박은 스택·계층 제약 준수. 결정마다 근거(DEC-00x §y · SPEC-00x §y) 병기, 선택지를 남기지 말고 단일 방식으로 서술
```

추가 자기점검 — 보고에 결과를 적어라:

- 세 WP 가 **템플릿 구조**를 다 갖췄나(불필요한 절은 「해당 없음」)
- **`Code Surface` 에 실제 파일 경로**가 아키텍처 디렉토리 트리를 따라 적혔나
- **Phase 가 PR 단위**이고, 각 Phase 끝에서 **그 자체로 돌아가는가**
- 검증 항목이 **앱 창에서 사람이 확인하는 절차**인가
- spec 계약 본문을 **복제하지 않았나**(링크로 연결)
- 코드 레포가 **별도 clone** 임이 반영됐나(이 워크트리에 코드를 두지 않는다)

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
  --subject "architect 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] architect 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
