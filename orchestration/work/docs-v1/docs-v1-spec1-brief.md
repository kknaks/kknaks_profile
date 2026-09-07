
# [architect] SPEC 배치 ① — 000 스캐폴딩 · 001 로그인·세션 · 002 업무 설정

너는 **task-management `architect` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**⚠ 이 워크트리는 코디네이터와 공유한다.** §5 가 지정한 파일 외에는 **만들거나 고치지 마라.** git 은 읽기만.

## 1. SSOT — 먼저 읽을 것

경로는 전부 `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/` 기준.

**양식 (반드시 따를 것)**
- `templates/projects/20-spec/spec.md` — **7절 구조를 그대로 쓴다.** Context / UX Contract / User Scenario / Interface Contract(API·Validation·Case Matrix·Flow·State·Data) / Implementation Rules / Verification / Open Questions

**정책 (닫힌 계약)**
- `para/projects/summer-star/task-management/10-decision/decision-001-auth-settings.md` — 이 배치의 주 근거
- `.../decision-002-my-tasks.md` — 유형·프로젝트를 소비하는 쪽(참조용)
- 대응 기획서 `00-baseline/baseline-001-auth-settings.md`

**아키텍처 (구조·규약 — 이미 확정)**
- `.../40-architecture/system/README.md` · `backend/README.md` · `frontend/README.md` · `database/README.md`(+`domains/account.md`)
- 특히 `backend §10` API 표면 · `backend §8` 에러 규약 · `frontend §1~3` 라우트·디렉토리·페칭

**디자인**
- `00-design/11-auth-profile.md` · `로그인 · 계정 · 프로필.dc.html` · **`09-design-tokens.md`** · **`디자인 시스템.dc.html`** · `08-responsive.md`
- `orchestration/work/docs-v1/design-requests.md` — **§A 정정 15건**(디자인이 틀린 것) · **§B 미설계 목록** · §C 기술 확정
- `orchestration/work/docs-v1/work-settings-proposal.html` — 업무 설정 **참고 시안**(확정 아님, 방향만)
- `orchestration/work/docs-v1/docs-v1-design-report.md` — 화면 P-04~P-13 · 공용 컴포넌트 S-xx

## 2. 배경 / 무엇을 바꾸나

정책·아키텍처가 다 닫혔다. 이제 **spec** 을 쓴다 — client/QA 가 이 문서만 읽고 따를 수 있는 **외부 계약**이다. 이후 WP(구현 단위)와 코드가 여기서 나온다.

spec 은 **검증 단위**로 자른다. 사용자가 기능 하나를 만들고 **실제 앱 창에서 E2E 로 확인한 뒤** 다음으로 넘어간다.

## 3. 계약 — 이미 확정된 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 개발 방식 | **처음부터 Tauri 포함.** 백엔드 로컬 + 프론트 `tauri dev` 앱 창. 기능마다 실제 셸에서 E2E 검증 |
| 프론트 | Next.js **정적 빌드**(`output: 'export'`) + shadcn/ui + Tailwind. **동적 세그먼트 금지**(전부 `?id=`), 모든 page 는 `use client`, 미들웨어 없음 |
| 상태·페칭 | TanStack Query v5 단일, 전역 상태 라이브러리 없음, `retry:false` |
| 백엔드 | FastAPI + uv, router→service→repository, **schema(FE 계약) / dto(내부)**, Postgres 비동기 |
| 인증 | **Bearer** (쿠키 없음). access 1h / refresh 7d. 「유지」 체크 시 **OS 키체인**, 미체크 시 메모리 |
| 계정 | **DB 시드로만 생성.** 회원가입·비밀번호 찾기 없음 |
| 유형 | **동적** — 종류(`미팅|업무`) + 이름 + 색(허용 팔레트). 기본 3종은 삭제 불가·이름/종류 고정·**색만 편집** |
| 프로젝트 | 이름 + 색. slug 없음(자동 키) |
| 삭제 | 소프트 딜리트. **v1 에 복원 UI 없음** |
| 실패 | **설계한 실패만 처리, 그 밖은 fallback 없이 전파.** 자동 저장 실패 = 토스트 + 해당 필드 실패 표시(자동 재시도 없음) |
| v2 스코프 | UI 는 그리되 비활성 + 「v2에서 제공됩니다」 토스트. **숨기지 않는다** |

## 4. **미설계 화면은 네가 확정한다** — 이번 발주의 핵심

**디자인 작업은 끝났다.** 남은 미설계 화면은 디자이너에게 더 요청하지 않고, **`09-design-tokens.md` 와 `디자인 시스템.dc.html` 의 토큰·규칙을 적용해 spec 안에서 직접 확정한다.**

적용할 규칙(디자인 시스템 [10 RULES] 등):
- 오버레이 3종 — **Drawer 840**(여러 값 편집) / **Modal 600**(되돌리기 어려운 결정 하나) / **Popover 200–400**(고르기). **드로어 위에 모달을 겹치지 않는다**
- **한 줄짜리 개체는 인라인**, 탭·로그·첨부가 붙는 개체만 드로어. 필드 4개 이하면 드로어를 열지 않는다
- **자동 저장이 기본** — 저장 버튼은 드로어 안에서만
- **검정은 위치, 보라는 선택** — `#1E1E1E` 는 화면당 하나
- 단축키로 되더라도 **화면에는 항상 버튼**
- 반응형은 **유동** — 1920 좌표는 참고값, absolute 금지. 여백 240→80→48, 1280 미만은 안내 화면

**이 배치에서 확정할 미설계 화면**:

| 항목 | 근거 |
|---|---|
| **업무 설정 화면**(유형·프로젝트 관리) — 설정 메뉴 위치, 등록 폼(**종류+이름+색**), 목록, 편집·삭제 | DEC-001 OQ-1 |
| **로그아웃 확인 모달 · 계정 삭제 확인 모달**(600) | DEC-001 OQ-3 |
| **자동 저장 실패 표시** — 토스트 문구 + 필드 실패 상태 시각 규격 | DEC-001 §7 |
| **v2 스코프 표시 규격** — 비활성 처리 + 토스트. **전 영역 공통 컴포넌트** | DEC-001 §v2 |
| **인증·설정 영역 반응형** | Q-22 |
| 삭제된 유형·프로젝트 복구 UI | **불필요** — v1 에 복원 없음(DEC-004 §4). OQ-2 는 이걸로 닫는다 |
| 로그인 폼 정정 | 「이메일」→**「아이디」**, 비밀번호 찾기·회원가입 링크 **제거** (§A-9) |

**확정한 화면은 spec §2 UX Contract 에 상태·문구·CTA·기대결과까지 적는다.** 그리고 **닫은 OQ 를 spec §7 에 「어느 OQ 를 무엇으로 닫았는지」로 남겨라** — 코디가 정책서 OQ 표를 갱신할 근거가 된다.

## 5. allowed_paths — 이 밖은 건드리지 마라

`para/projects/summer-star/task-management/20-spec/` 아래 **신규 3건만**:

1. `spec-000-scaffold.md` — 레포·Tauri 셸·Next 정적·FastAPI·Postgres·compose·시드. **검증: 앱 창이 뜨고 백엔드에 붙는다**
2. `spec-001-auth-session.md` — 로그인 화면·Bearer·키체인·세션 갱신·로그아웃(+확인 모달). **검증: 로그인해서 들어가고, 앱을 껐다 켜도 유지된다**
3. `spec-002-work-settings.md` — 유형·프로젝트 CRUD(업무의 전제). **검증: 유형 만들고 프로젝트 만든다**

그 외 일체 금지 — 정책서·기획서·아키텍처·디자인 원본·index·log 는 **코디네이터 소관**. 커밋·push 금지.

**id 는 `SPEC-000`·`SPEC-001`·`SPEC-002`, `status: draft`, `version: 0.0.1`.** frontmatter `links.decisions`·`links.baselines` 를 채워라.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT(양식 먼저).
2. **SPEC-000 스캐폴딩** — UI 가 거의 없으니 §2 는 최소, §4·§5 에 무게. 기동 절차·환경변수·시드 계정·헬스체크·`tauri dev` 로 앱이 뜨는 것까지가 계약이다.
3. **SPEC-001 로그인·세션** — §4 에서 미설계 화면 확정(로그인 폼 정정·확인 모달·실패 표시·v2 스코프 표시).
4. **SPEC-002 업무 설정** — 유형·프로젝트 화면을 §4 규칙으로 확정. **종류 셀렉터가 반드시 있어야 한다**(시안에 없다).
5. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- 코드를 만들지 않는다. **문서만.**
- **spec 에 내부 구현을 두지 않는다**(템플릿 경고) — 테이블 schema 전문·ORM·repository 구조·파일 경로·PR 계획·구현 순서는 **WP 와 코드 몫**이다. 외부에 관찰되는 계약만.
- 정책·아키텍처를 다시 논의하거나 어기지 않는다. 충돌은 고치지 말고 Open Questions.
- 배치 ②~④(내 업무·문서함·회의록·캘린더·설정·메시지함)는 **이번 범위가 아니다.**
- 선택지를 나열하지 않는다 — **하나로 정하고 근거를 단다.**

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. DEC-001~006 을 어기는 구조를 제안하지 않았는지 자기점검(충돌 발견 시 고치지 말고 Open Questions). 사용자가 못박은 스택·계층 제약 준수. 결정마다 근거(DEC-00x §y · P/C/S/F/Q-xx) 병기, 선택지를 남기지 말고 단일 방식으로 서술
```

추가 자기점검 — 보고에 결과를 적어라:

- 세 문서가 **템플릿 7절 구조**를 다 갖췄나(빈 절은 「해당 없음」으로 명시)
- **§4 미설계 화면을 전부 확정**했나. 각각 어느 토큰·규칙을 근거로 그렸는지 적혔나
- **닫은 OQ 목록**이 spec §7 에 남았나
- spec 에 내부 구현(파일 경로·ORM·repository)이 새어 들어가지 않았나
- Case Matrix 가 에러의 **단일 SoT** 인가(API 절에 에러를 흩지 않았나)
- 각 spec 의 **E2E 검증 기준**(§6 Acceptance)이 사용자가 앱 창에서 직접 확인할 수 있는 문장인가

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
