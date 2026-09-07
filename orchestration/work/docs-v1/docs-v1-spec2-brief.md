
# [architect] SPEC 배치 ② — 003·004 내 업무 · 005 문서함

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
- `para/projects/summer-star/task-management/10-decision/decision-002-my-tasks.md` — **내 업무 주 근거**
- `.../decision-004-library.md` — **문서함 주 근거**
- `.../decision-001-auth-settings.md` — 유형·프로젝트를 제공하는 쪽(소비 규약)
- `.../decision-005-calendar.md` §3 — **`schedule` 은 파생**, 기한은 업무가 소유
- 대응 기획서 `00-baseline/baseline-002-my-tasks.md` · `baseline-004-library.md`

**배치 ① 산출물 (같은 결로 이어 쓸 것)**
- `.../20-spec/spec-000-scaffold.md` · `spec-001-auth-session.md` · `spec-002-work-settings.md`
- 특히 **에러 코드 명명·Case Matrix 형식·Acceptance 문장 톤**을 맞춰라. **팔레트 8종**(SPEC-002 §4)을 그대로 참조한다

**아키텍처 (구조·규약 — 이미 확정)**
- `.../40-architecture/system/README.md` · `backend/README.md` · `frontend/README.md` · `database/README.md`(+`domains/account.md`)
- 특히 `backend §10` API 표면 · `backend §8` 에러 규약 · `frontend §1~3` 라우트·디렉토리·페칭

**디자인**
- `00-design/01-screens.md`~`08-responsive.md`(내 업무 전 범위) · `업무 화면 정의서.dc.html`
- `00-design/14-library.md` · `문서함.dc.html`
- **`09-design-tokens.md`** · **`디자인 시스템.dc.html`**
- `orchestration/work/docs-v1/design-requests.md` — **§A 정정 15건**(디자인이 틀린 것) · **§B 미설계 목록** · §C 기술 확정
- `orchestration/work/docs-v1/docs-v1-design-report.md` — 화면 P-18~P-31(내 업무) · P-56~P-60(문서함) · 공용 컴포넌트 S-xx
- `orchestration/work/docs-v1/mediness-markdown-study.md` — **마크다운 렌더·편집 확정 근거**

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
| 업무 유형 | **필수.** 설정의 동적 유형을 참조(SPEC-002 가 제공) |
| 업무 프로젝트 | **N:1, 0..1개.** 무소속 허용. M:N 없음 |
| **완료 게이트** | 완료 전이 시점에 **결과자료 ≥1 또는 완료 결과 작성** 중 하나가 없으면 **완료되지 않는다**(안내 토스트). 리스트 셀·상세·칸반 DnD 모두 동일 |
| 기한 | **업무가 `due_date` 를 소유**한다. `schedule` 은 파생 — 캘린더는 배치 ④ |
| 상태 변경 지점 | ① 리스트 상태 셀(팝오버) ② 상세 드롭다운 ③ 칸반 DnD |
| 첨부 | **자료함 문서(md) 또는 URL 링크.** pdf·docx 는 v2 |
| 문서함 | PARA 4종 고정 트리(하위 자유) · **md 만 업로드** · **업로드만**(새 문서 생성 없음) · 자동 저장 · 폴더는 **빈 것만 삭제** |
| 마크다운 | **`react-markdown` 렌더 + `textarea` 편집.** 에디터 라이브러리 미사용. 플러그인 세트는 한 파일에 모아 전 영역 공유 |
| 문서함 v2 | AI 색인·버전 관리·검색·휴지통 — UI 는 그리되 비활성 + 안내 |
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
| **완료 결과 입력 UI** — 신설 필드. 완료 시 결과자료가 없으면 결과를 쓰게 하는 흐름 + **거부 토스트 문구/규격** | DEC-002 OQ-1 |
| **칸반 DnD 규격** — 드롭 대상 하이라이트·플레이스홀더·드래그 중 카드 | DEC-002 OQ-2 |
| **미설계 6종** — 빈 상태 · 지연 뱃지 · 스켈레톤 · 검색 결과 · 칸반 드래그 중 · 카드 컨텍스트 메뉴 | DEC-002 OQ-3 |
| **업무 삭제 진입점** (복원은 v2 — 없음) | DEC-002 OQ-4 |
| **폴더 삭제 진입점** — 빈 폴더만 삭제 가능 | DEC-004 OQ-3 |
| **내 업무·문서함 반응형** — 내 업무는 P-28~31 이 있으나 **유동 레이아웃 기준으로 재해석**(§C Q-34 · A-13). 문서함은 미설계 | Q-34 · 분석 §7-2 |
| 유형 배지에서 「취소」 제거 | 취소는 상태다 (§A-2) |
| 완료 시 결과자료 강제 | 디자인 「막지 않는다」를 **뒤집는다** (§A-3) |

**확정한 화면은 spec §2 UX Contract 에 상태·문구·CTA·기대결과까지 적는다.** 그리고 **닫은 OQ 를 spec §7 에 「어느 OQ 를 무엇으로 닫았는지」로 남겨라** — 코디가 정책서 OQ 표를 갱신할 근거가 된다.

## 5. allowed_paths — 이 밖은 건드리지 마라

`para/projects/summer-star/task-management/20-spec/` 아래 **신규 3건만**:

1. `spec-003-tasks-crud.md` — 업무 생성 드로어·상세(드로어/페이지 승격)·인라인 편집·할일/메모/참고자료/로그·연관업무. **검증: 업무를 만들고 열어서 고친다**
2. `spec-004-tasks-status-views.md` — 상태 전이 5종·**완료 게이트**·취소(모달)·소프트 딜리트·리스트/칸반 뷰·필터·정렬. **검증: 업무를 완료까지 보내고 리스트↔칸반을 오간다**
3. `spec-005-library.md` — PARA 트리·목록·즐겨찾기·업로드 드로어·문서 상세/편집(md)·메타데이터·연결·더보기. **검증: md 를 올리고 열어서 고치고 업무에 연결한다**

그 외 일체 금지 — 정책서·기획서·아키텍처·디자인 원본·index·log 는 **코디네이터 소관**. 커밋·push 금지.

**id 는 `SPEC-003`·`SPEC-004`·`SPEC-005`, `status: draft`, `version: 0.0.1`.** frontmatter `links.decisions`·`links.baselines` 를 채워라.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT(양식 먼저).
2. **배치 ① 세 문서를 먼저 읽어** 형식·에러 코드 명명·톤을 맞춘다.
3. **SPEC-003 업무 생성·상세** — 드로어 840·⤢ 페이지 승격·인라인 편집·자동 저장. 첨부는 **자료함 md + URL 링크** 두 종류.
4. **SPEC-004 상태·뷰** — **완료 게이트가 이 spec 의 핵심**이다. 세 진입점(셀·상세·DnD)에서 **같은 판정**을 거치게 계약을 쓰고, 미충족 시 거부 토스트를 §2·Case Matrix 양쪽에 박아라. 칸반 DnD 규격도 여기서 확정.
5. **SPEC-005 문서함** — 트리·업로드(md 만)·상세/편집. 마크다운은 `mediness-markdown-study.md` 결론을 따른다. v2 항목(색인·버전·검색·휴지통)은 **비활성 UI + 안내**로 계약에 넣는다.
5. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- 코드를 만들지 않는다. **문서만.**
- **spec 에 내부 구현을 두지 않는다**(템플릿 경고) — 테이블 schema 전문·ORM·repository 구조·파일 경로·PR 계획·구현 순서는 **WP 와 코드 몫**이다. 외부에 관찰되는 계약만.
- 정책·아키텍처를 다시 논의하거나 어기지 않는다. 충돌은 고치지 말고 Open Questions.
- 배치 ③~④(회의록·캘린더·개인 설정·메시지함)는 **이번 범위가 아니다.** 캘린더 표시·드래그는 배치 ④ 몫이니 여기서는 `schedule` 파생 사실만 참조하고 화면을 쓰지 마라.
- 선택지를 나열하지 않는다 — **하나로 정하고 근거를 단다.**

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. DEC-001~006 을 어기는 구조를 제안하지 않았는지 자기점검(충돌 발견 시 고치지 말고 Open Questions). 사용자가 못박은 스택·계층 제약 준수. 결정마다 근거(DEC-00x §y · P/C/S/F/Q-xx) 병기, 선택지를 남기지 말고 단일 방식으로 서술
```

추가 자기점검 — 보고에 결과를 적어라:

- 세 문서가 **템플릿 7절 구조**를 다 갖췄나(빈 절은 「해당 없음」으로 명시)
- **완료 게이트가 세 진입점 모두에 같은 규칙으로** 적혔나(리스트 셀·상세 드롭다운·칸반 DnD)
- 첨부가 **md 문서 + URL 링크 두 종류**로 적혔나
- 배치 ① 과 **에러 코드 명명·Case Matrix 형식**이 어긋나지 않나
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
