
# [architect] WP 2·3그룹 — 업무 2건 + 회의록 3건 (문서함은 이번 범위 아님)

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
- `para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md`
- `.../spec-004-tasks-status-views.md`
- `.../spec-006-meeting-setup.md`
- `.../spec-007-meeting-live.md`
- `.../spec-008-meeting-close.md`

**문서함(SPEC-005)은 이번 범위가 아니다** — 캘린더와 함께 다음 그룹으로 미뤘다(사용자 확정).

**1그룹 WP — 같은 결로 이어 쓸 것**
- `.../30-work/work-001-scaffold.md` · `work-002-auth-session.md` · `work-003-work-settings.md`
- **Phase 구성·검증 문장 톤·§Internal Interface Contract 쓰는 법**을 맞춘다

**구조·규약 (여기서 파일 경로·계층이 나온다)**
- `.../40-architecture/backend/README.md` — 계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약
- `.../40-architecture/frontend/README.md` — 라우트·디렉토리·페칭·토큰·오버레이·반응형
- `.../40-architecture/system/README.md` — 구성·흐름
- `.../40-architecture/database/README.md` (+ `domains/account.md`) — ERD·불변식

**정책 (참조)**
- `.../10-decision/decision-002-my-tasks.md` — **내 업무 주 근거**(유형 필수·프로젝트 N:1 무소속·**완료 게이트**·소프트 딜리트)
- `.../decision-003-meeting-notes.md` — **회의록 주 근거**(2트랙·배치 파이프라인·종료 통합·실패 정책·STT 전제)
- `.../decision-005-calendar.md` §3 — **`schedule` 은 파생**(기한은 업무가 소유)
- `orchestration/work/docs-v1/soniox-study.md` — STT 프로토콜·토큰 모델·화자 분리
- `.../decision-001-auth-settings.md` — 유형·프로젝트를 제공하는 쪽

## 2. 배경 / 무엇을 바꾸나

v1 spec 12건이 다 섰다. 이제 **WP(빌드 계획)** 를 쓴다 — **dev 가 이 문서만 보고 PR 을 나누고 작업을 시작할 수 있어야** 한다.

이번은 **업무 2건 + 회의록 3건**이다. 순서는 **업무 → 회의**다(회의가 업무를 생성·갱신하므로). 1그룹(WORK-001~003)은 **이미 구현·검수까지 끝났다** — 스캐폴딩·인증·업무 설정이 실제로 돈다. 그 위에 업무와 문서함을 얹는다.

사용자가 **기능 하나를 만들고 실제 앱 창에서 E2E 로 확인한 뒤 다음으로 넘어가는** 방식이라, WP 도 그 단위로 끊는다.

**1그룹에서 배운 것을 반영하라** — 이 셋은 실제로 값을 했다:

| 배운 것 | 어떻게 반영하나 |
|---|---|
| **공용 컴포넌트를 화면보다 먼저** | 여러 화면이 쓸 것(업무 카드·상태 배지·드로어 프레임)은 **앞 Phase 에 둔다.** 화면부터 만들면 다음 work 가 복제한다 |
| **정적 검사를 검증 항목에** | 「grep 으로 0건」처럼 **규칙이 지켜졌는지 기계로 확인**하는 항목을 넣는다(hex 리터럴 0 · 계층 위반 0 등) |
| **실패 경로를 실측으로** | 「자동 재시도가 없다」를 **네트워크 탭에서 요청 수로** 확인하게 하는 식. 「~하지 않는다」는 눈으로 못 본다 |

## 3. 계약 — 이미 확정된 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| **코드 레포** | **별도** — `github.com/kknaks/task_management`. **이 워크트리에 코드를 만들지 않는다** |
| **이미 있는 것** | 스캐폴딩·인증·유형/프로젝트 API·**팔레트 8종**·`TypeBadge`/`ColorDot`/`ColorPickerPopover`·`InlineEditText`·`ConfirmModal`·**U-7 자동저장 실패 규격**·`V2Gate` — **다시 만들지 말고 재사용**하게 WP 에 적어라 |
| **완료 게이트** | 완료 전이는 **전용 엔드포인트 하나**를 지나고 서비스가 판정한다. 리스트 셀·상세·칸반 DnD·(3그룹) 회의록 요청이 **전부 그 하나**를 지난다 |
| **기한** | 업무가 `due_date` 를 소유하고 `schedule` 은 파생 — **`PATCH /api/schedules` 는 없다** |
| 첨부 | 자료함 문서(md) 또는 **URL 링크** 2종 |
| 개발 방식 | **처음부터 Tauri 포함.** 백엔드 로컬 + 프론트 `tauri dev` 앱 창. 기능마다 실제 셸에서 E2E 검증 |
| 타깃 | v1 에 **macOS · Windows 둘 다** |
| 프론트 | Next.js **정적 빌드**(`output: 'export'`) + shadcn/ui + Tailwind + TanStack Query v5. **동적 세그먼트 금지**(전부 `?id=`), 모든 page 는 `use client`, 미들웨어 없음, 전역 상태 라이브러리 없음 |
| 백엔드 | FastAPI + **uv**, router→service→repository, **schema(FE 계약) / dto(내부)**, **Postgres 비동기** |
| 인증 | **Bearer**(쿠키 없음). access 1h / refresh 7d. 「유지」 체크 시 **OS 키체인**, 미체크 시 메모리. **토큰 저장소는 한 곳에서만 다룬다** |
| 계정 | **DB 시드로만 생성** |
| AI 런타임 | **open-kknaks 의 codex** — 호스트 바이너리 **바인드 마운트**. Anthropic/OpenAI SDK 직접 import 금지 (1그룹 범위 밖이지만 스캐폴딩이 자리를 잡는다) |
| 실패 | **설계한 실패만 처리, 그 밖은 fallback 없이 전파.** `except Exception` 금지·임의 재시도 금지·조용한 기본값 금지. `persist_changes` 는 **「실패 응답 자체가 쓰기인」 경우만**(현재 1건뿐) |

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

1. `work-004-tasks-crud.md` — **SPEC-003**. 업무 테이블·생성 드로어·상세(드로어 ↔ ⤢ 페이지)·인라인 편집 자동 저장·할일/메모/참고자료/로그·연관업무. **완료 = 업무를 만들고 열어서 고친다**
2. `work-005-tasks-status-views.md` — **SPEC-004**. 상태 전이 5종·**완료 게이트**(전용 엔드포인트 단일 판정)·취소 모달·소프트 딜리트·리스트/칸반 뷰·필터·정렬·**칸반 DnD**. **완료 = 업무를 완료까지 보내고 리스트↔칸반을 오간다**
3. `work-006-meeting-setup.md` — **SPEC-006**. 회의록 테이블·목록·생성 드로어(제목·프로젝트·유형·일시·안건·첨부)·시작 전 화면(안건 프롬프트)·회의 시작·삭제 모달·프로젝트 필터 칩. **완료 = 회의를 만들고 안건을 적고 시작한다**
4. `work-007-meeting-live.md` — **SPEC-007**. 마이크 캡처·**WS 2단 중계**(프론트↔백↔Soniox)·실시간 스크립트(잠정/확정 토큰·화자 라벨)·사람 트랙 프롬프트·**AI 배치 파이프라인**(open-kknaks codex·트리거·증분·회차 표시)·AI 요약 탭 트리·녹음 원본 적재. **완료 = 말하면 스크립트가 쌓이고 AI 탭이 채워진다**
5. `work-008-meeting-close.md` — **SPEC-008**. 「생성중」 상태·마지막 배치·**통합본 생성**(사람 줄 우선)·실패 배너/다시 생성·근거 타임칩·편집 모드(줄 수정·종류 전환·드로어 3종)·**업무 생성/갱신 버튼**(WORK-005 완료 게이트 소비)·회의 상세 드로어. **완료 = 회의를 끝내면 통합본이 나오고 액션 줄에서 업무가 생성된다**

**첨부 주의** — 문서함이 다음 그룹으로 미뤄졌다. 업무 참고자료·회의 첨부의 **「자료함에서 선택」은 스텁**이고, **URL 링크만 실동작**한다. 각 WP 에 그 사실과 「문서함 work 가 실체화한다」를 적어라.

**id 는 `WORK-004`~`WORK-008`, `status: todo`, `work_type: new-feature`.**
frontmatter `links.specs`·`links.decisions`·`links.works`(의존)를 채워라.

그 외 일체 금지 — spec·정책서·아키텍처·index·log 는 **코디네이터 소관**. 커밋·push 금지.
**코드를 만들지 마라** — WP 는 계획 문서다.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT(양식 → spec 3건 → 아키텍처).
2. **1그룹 WP 3건을 먼저 읽어** Phase 구성·검증 문장 톤을 맞춘다.
3. **WORK-004 업무 CRUD** — 마이그레이션(업무·할일·메모·첨부·로그·연관)이 여기 들어간다. 백 → 프론트 순. **드로어 ↔ 페이지 승격**이 같은 컴포넌트를 두 표면에 쓰는 구조라 Phase 를 나눌 때 고려하라.
4. **WORK-005 상태·뷰** — **완료 게이트가 이 WP 의 핵심**이다. 세 진입점이 **같은 엔드포인트**를 지나는지를 검증 항목으로 못박아라. 칸반 DnD 규격도 여기.
5. **WORK-006 회의 생성·시작 전** — 회의록 테이블(안건·줄·트랜스크립트·첨부) 마이그레이션이 여기. 유형은 **종류=미팅**만 거른다.
6. **WORK-007 회의 중** — **이 그룹에서 가장 무겁다.** WS 2단 중계·오디오 릴레이·배치 세션 유지(open-kknaks codex)·2트랙 격리. **실패 4종**(배치 실패·스키마 위반·없는 업무 참조·연결 끊김)을 Phase 검증에 넣어라.
7. **WORK-008 종료·통합·편집** — 통합본 생성이 핵심. **업무 생성/갱신이 WORK-005 의 완료 게이트를 우회하지 않는지**를 검증 항목으로.
5. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- **코드를 만들지 않는다.** WP 문서 3건만.
- spec 계약 본문을 복제하지 않는다 — 링크로.
- **문서함·캘린더·개인 설정·메시지함은 이번 범위가 아니다.**
- **1그룹 WP(WORK-001~003)를 고치지 마라** — 이미 구현이 끝났다.
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
- 코드 레포가 **별도** 임이 반영됐나
- **이미 있는 것을 다시 만들라고 하지 않았나**(팔레트·배지/dot·InlineEditText·ConfirmModal·U-7·V2Gate — 재사용으로 적었나)
- **완료 게이트가 단일 엔드포인트**로 적혔나(세 진입점이 같은 하나를 지난다)
- **정적 검사·실측 검증 항목**이 들어갔나(「~하지 않는다」를 기계로 확인)

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
