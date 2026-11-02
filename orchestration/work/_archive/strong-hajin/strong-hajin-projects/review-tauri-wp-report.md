# 리뷰 리포트 — strong-hajin-projects / WORK-006 계획 (planner 모드, 2026-09-22)

## 판정: FAIL — FAIL 3건(승인저지 2 · 비저지 1) · WARN 8건

문서 검수만 했다. **빌드·테스트·실측·서버 접속·배포를 하나도 실행하지 않았다.** 아래 「확인한 것」의
근거는 전부 파일 읽기와 read-only `git` 조회다. 실측 미수행·구현 수단 미선택 자체는 FAIL 로 세지 않았다.

계획의 뼈대(계측 먼저 → 판정 게이트 → 셸 → 배선 → 통합 재측정 → 운영/릴리즈)와 AC·실측·DEC 전수
추적은 **실제로 맞다**(아래 수치 검증). FAIL 셋은 전부 **경계·소유·순서**의 문제이고, 계약(I-1~I-8)이나
SPEC 본문을 건드리는 수정은 필요 없다.

---

## 검수 범위

- 대상: `para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md` (999줄, untracked 신규 1건)
- 기준 문서: `20-spec/spec-006-tauri-wrapper.md` v0.2.3 · `10-decision/decision-005-tauri-wrapper.md` D-01~09 ·
  `orchestration/runbook.md` · `AGENTS.md` · `para/para.md` · `para/projects/project.md` ·
  `orchestration/roles/strong-hajin/reviewer/*` · `templates/projects/30-work/work.md` ·
  `tauri-wp-writer-brief.md` · `tauri-wp-writer-report.md` · `tauri-deployment-decisions.md` ·
  `tauri-spec-finalization.md`
- 실행한 검사 (전부 읽기 성격)
  - `python3 rules/check-concept-map.py` → **exit 0** (`scripts/lint-pipeline.py` 는 **레포에 없다** — `scripts/` 디렉토리 자체가 없어 실행 안 함)
  - frontmatter `yaml.safe_load` OK · 템플릿 14절 전부 존재·순서 일치 · `- [x]` **0건** · Phase Status **8개 전부 TODO** · `progress: 0`
  - AC/실측/DEC 전수 카운트(아래) · 의존 방향 검사
  - 코드 기준 HEAD 재확인: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
    branch `kknaksss/strong-hajin-projects` · HEAD **`a1f67915aa8eeb551327b858428c5d4c1519e1b4`** · `git status --porcelain` **0건** →
    WORK-006 §Code Surface 표와 **일치**
  - 인용 좌표 표본 검증: `stream.ts:234·251·258·317-319·322·327-331` · `MeetingDetailPage.tsx:932` ·
    `labels.ts:772` · `BrowserRecordingPage.tsx:13·22-27·30-44·47` · `App.tsx:401·684` ·
    `api.ts` fetch **9곳(103·118·127·277·568·1022·1099·1346·1371)** · `auth_sessions.py:12` ·
    `http_auth.py:106-107` · `delivery/Dockerfile:63` · `Makefile:25` → **전부 일치**
- allowed_paths 대조: 원 워커 브리프 §5 는 두 파일. `git status` 상 워커가 남긴 것은
  `work-006-tauri-wrapper.md` + `tauri-wp-writer-report.md` **둘뿐**. **이탈 0건.**

---

## 위반 (FAIL)

### F-1 (승인저지) — Meta 의 「코드가 겹치지 않는다 / 워크트리를 따로 잡는다」는 **사실과 다르고 런북 고정 규칙과 충돌한다**

- 위치: `work-006-tauri-wrapper.md:57-63` (Meta — Depends on work / Parallel work) · `:98` (Work Summary — Branch/PR)
  > `Depends on work`: 없음. WORK-001 ~ WORK-005 와 **코드가 겹치지 않는다** … 다만 **같은 코드 레포를 쓰므로 워크트리를 따로 잡는다**
  > `Branch/PR` | 미정 — 코드 워크트리 `strong-hajin-tauri` 제안

- **근거 ①(사실 오류)**: WORK-005 의 코드는 커밋 **`a1f6791` 단 하나**이고 **`origin/main` 에 아직 없다.**
  그 커밋이 바꾼 파일에 WORK-006 Phase 4 의 파일 범위가 그대로 들어 있다 —
  `git diff --stat origin/main..HEAD` → `frontend/src/App.tsx | 35 +`, `frontend/src/lib/labels.ts | 126 +`.
  WORK-006 자신도 `:196`(`App.tsx:684`)·`:191`(`labels.ts:772`)·Phase 4 파일 범위(`:493-495`)에서 **같은 두 파일을 연다.**
  「코드가 겹치지 않는다」는 문장과 **같은 Meta 안의** 「접점은 `features/meetings/` 와 `App.tsx` 두 곳」(`:60-62`)도 서로 부딪친다.
- **근거 ②(규약 위반)**: `orchestration/runbook.md:59-68` 고정 규칙 —
  「코디 세션 1개 = 작업 1개 = `work/<slug>/` 1개 = **레포당 워크트리 1개** = 레포당 브랜치 1개 …
  **WORK 번호는 작업 단위가 아니다** … 코드 워커는 코드 레포에 **워크트리 하나**를 갖고 그 안에서 WORK 를 이어 쌓는다」.
  같은 절이 기록한 2026-09-05 사고가 정확히 이 형태다 — 「새로 판 워크트리가 `origin/main` 기준이라 앞 WORK 의 코드가 없는 **빈 트리에 워커를 태웠다**」.
  `config/projects/strong-hajin.json` 의 code repo `base` 도 `origin/main` 이라, 지금 `new-work.sh` 로 새 워크트리를 파면 **a1f6791 이 없는 트리**가 뜬다.
- 영향: 계획서를 그대로 읽고 발주하면 ① WORK-005 코드가 없는 트리 위에서 `App.tsx`·`labels.ts` 를 고치고
  ② 나중에 두 브랜치가 같은 두 파일에서 충돌한다. **문서가 사고를 지시하는 상태**다.
- 최소 수정 (Meta 3줄 + Work Summary 1줄)
  - `Depends on work`: 「없음 … 겹치지 않는다」 → **「코드 접점 있음 — `frontend/src/App.tsx` · `frontend/src/lib/labels.ts` 는 WORK-005 의 `a1f6791`(아직 `origin/main` 미머지)이 이미 바꾼 파일이다」**
  - 「같은 코드 레포를 쓰므로 워크트리를 따로 잡는다」 → **「런북 §1 대로 같은 작업 단위의 기존 코드 워크트리·브랜치(`kknaksss/strong-hajin-projects`)에 이어 쌓는다. 새 워크트리는 사용자가 새 코디 세션을 띄울 때만 생기고, 그때 base 는 WORK-005 가 머지된 `origin/main`(또는 `kknaksss/strong-hajin-projects`)이어야 한다」**
  - `Branch/PR` 의 `strong-hajin-tauri` 제안은 위 문장으로 대체한다.

### F-2 (승인저지) — **운영 주소를 실재하게 만드는 실행 Phase 가 없다.** Phase 8 이 주인 없는 선행에 매달린다

- 위치: Phase 6 (`:603-604`, `:637-641`, `:648-651`) ↔ Phase 8 (`:715-717`) ↔ Scope 포함 (`:132-137`) ↔ Done Criteria (`:941`)
  > Phase 6 **출력**: 「**배포 구성안 1건**(차트·Application·values·ingress·네임스페이스·rollback) — **실행은 아니다**」
  > Phase 6 **하지 말 것**: 「**서버를 기동·중단하지 마라. 배포하지 마라.** 이 Phase 의 산출물은 **문서**다」
  > Phase 6 **완료 기준**: 「**이 Phase 는 인수조건을 닫지 않는다** — 전제를 세우는 단계다」
  > Phase 8 **입력**: 「Phase 6 의 **구성안 실행 결과**(운영 주소가 실재한다)」 / **파일 범위**: 「그 밖의 코드는 **0줄**」
  > Scope **포함**: 「운영 배포 준비: **FE 정적 서빙** · 같은 origin API·WS 라우팅 · …」
- 근거: 여덟 Phase 어디에도 ① 차트·Application·values 를 **실물 파일로 쓰는 단계** ② **arm64 운영 이미지 빌드**
  ③ **FE 정적 서빙 배선**(6-3 옵션 A 의 정적 서빙 컨테이너) ④ **배포 실행**이 없다. Phase 8 소유에
  「사용자(배포 실행)」가 있으나 작업 1~5 에 배포 단계가 없고 파일 범위가 그것을 금지한다.
  원 워커도 보고서 §6 에서 자인한다 — 「**Phase 6 의 구성안은 문서다. 실제 차트·Application 작성과 배포는 … 별도 발주가 맞다 — 이 계획은 그 자리를 열어 두기만 했다**」.
- 영향: Done Criteria 「모든 Phase 가 DONE 또는 SUPERSEDED」가 **도달 불가**다. AC-T24 와 M-1·M-5 의 최종 확인이
  계획 밖의 미지정 작업에 걸린다. Scope 「포함」이 약속한 정적 서빙·같은 origin 라우팅을 **아무 Phase 도 만들지 않는다.**
- 최소 수정 (둘 중 하나)
  - **(a) 권장** Phase 6 을 **6a(결정·구성안)** / **6b(구성 실물 작성·운영 이미지 빌드·정적 서빙 배선·배포 실행 — 사용자 승인 뒤)** 로 가르고,
    6b 에 소유(코디 구성 + `backend`/`frontend` 워커 + 사용자 실행)·파일 범위·완료 기준을 적는다. Phase 8 의존을 **6b** 로 바꾼다.
  - **(b)** 실행을 이 work 밖으로 빼려면 Scope 「제외」 표에 **「운영 배포 실행 → 별도 work」** 행을 더하고,
    Phase 8 과 AC-T24·M-1/M-5 최종을 **그 work 뒤로** 명시적으로 미룬다(Done Criteria 에도 같은 문장).

### F-3 (비저지 — Phase 7 발주 전까지 수정하면 된다) — OQ-T02 가 Phase 7 을 막지 않는다고 적혔으나, Phase 7 의 **발행 단계는 운영 주소가 있어야 한다.** 그리고 Phase 8 뒤 **재빌드·재발행 단계가 없다**

- 위치: 미결 게이트 `:886`(OQ-T02 행 — 막는 Phase 「6 · 8」, 막지 않는 것 「1~5·**7**」) ↔ Phase 7 작업 3~5 (`:673-680`) ↔ Phase 8 작업 1 (`:726-727`)
- 근거: Phase 7 작업 4 는 「**그 판이 여는 운영 주소**」를 기록으로 남기라 하고, 작업 5 는 GitHub Releases 에
  설치파일을 **발행**하라 한다. 그런데 Phase 8 작업 1 이 그제서야 `capabilities` 의 `remote.urls` 를
  **운영 origin 으로 바꾼다.** 즉 Phase 7 이 낸 설치파일은 운영 origin 을 갖지 않은 판이고,
  **그 뒤 다시 빌드해 발행하는 단계가 계획에 없다.**
- 영향: 순서대로 따르면 「운영 주소를 안 여는 설치파일」이 Release 에 올라간다. AC-T24(Phase 8) 는
  **배포된 앱**의 성질인데 검증 대상 판이 존재하지 않게 된다.
- 최소 수정: ① 미결 게이트 OQ-T02 행의 「막는 Phase」에 **「7 의 발행 단계」**를 더한다
  ② Phase 7 을 **7a(fixture origin 판 빌드 + M-10 측정 — OQ-T02 무관)** / **7b(운영 origin 판 빌드·Release 발행)** 로 가르고
  **7b 를 Phase 8 의 origin 확정 뒤**에 둔다(또는 Phase 8 완료 기준에 「운영 origin 을 박은 판을 다시 빌드·발행한다」를 명시).

---

## 경미 (WARN) — 전부 비저지

| # | 위치 | 내용 · 근거 | 최소 수정 |
|---|---|---|---|
| **W-1** | `:254` | 「**Phase 1 ~ 5 는 위 어느 것에도 막히지 않는다.** 전부 개발 fixture(로컬)에서 돈다」 — **바로 위 표**(`:253`)가 「Windows 실기 \| 사용자(OQ-W01) \| **Phase 2·5·7 의 Windows 축**」이라 적는다. 같은 쪽에서 모순 | 「**Phase 1~5 의 macOS 축은** 위 어느 것에도 막히지 않는다」로 한정 |
| **W-2** | 실측표 M-1 행(`:766`) · Phase 1 작업 3·7(`:331`·`:343`) | M-1 의 fixture 를 「로컬 fixture origin」이라고만 쓴다. **SPEC §6 M-1 은 「로컬 https origin 을 허용 목록에 넣어 본다」**(spec `:898`)로 **https** 를 지정했다. 실물 fixture 는 평문이다 — `frontend/vite.config.ts:9-15` (`server.port 5173`, `/api` 프록시 `ws:true`), `Makefile:185` 의 `npm run dev`. M-1 은 **중단 판정의 근거**라 프로토콜이 다르면 판정이 흔들린다 | M-1 방법 칸에 「로컬 **https** fixture origin」을 못박고, 평문 `localhost` 는 M-2·M-4(마이크 secure context) 전용으로 갈라 적는다 |
| **W-3** | Phase 5 완료 기준(`:576-582`) · AC 추적표 Phase 5 절(`:823-847`) | Phase 5 가 닫는 21건 중 **여덟**(T01~T04←M-9, T26←M-5, T27·T28←M-2b, T32·T38←M-6)의 「실측」이 **Phase 2 의 fixture 측정**이다. Phase 5 가 「다시 잰다」인지 「Phase 2 기록을 인용한다」인지 표기가 없다. 특히 **AC-T01~T04 는 「회의 업스트림으로 마이크가 열린 뒤」**(spec `:786`)라 탐침 셸 버튼이 아니라 **제품 녹음 위**에서 나야 하는 증거다 | Phase 5 「측정 규칙」에 한 줄 — 「**M-9 의 세 갈래를 제품 배선 위에서 한 번 더 확인하고 M-11 기록에 병기한다.** 나머지(M-5·M-2b·M-6)는 Phase 2 기록을 인용하고 인용임을 표시한다」 |
| **W-4** | `:218` · Phase 6 작업 2(`:619-620`) | 「`argocd/applications/*.yaml` \| **열 개** 전부 `targetRevision: main`」 — 레포 실물은 **9개**(`arc-controller`·`arc-runners-medisolve`·`cloudflared`·`datastores-dev`·`datastores-prod`·`kakao-tracker`·`mediness-dev`·`mediness-prod`·`private-pypi`). 「열 개」는 `tauri-deployment-decisions.md` 의 **클러스터 조회** 수다. 「전부 main」은 양쪽 다 참(`grep targetRevision` 비-main 0건) | 「레포 Application **9개**(2026-09-22 클러스터 조회 10개) 전부 `main`」 |
| **W-5** | Phase 7 실패 시 다음 조치(`:705-707`) | 「Windows 빌드 환경이 없으면 **macOS 만 먼저 낸다**」 — D-07(둘 다 지원)에 대한 **출시 범위 축소**인데 그 자리에 승인 주체가 없다. (Phase 7 소유의 「사용자(… Release 발행 승인)」와 「하지 말 것」의 「사용자 승인 없이 Release 를 발행하지 마라」가 간접적으로 덮지만, **범위 축소 자체**를 올리라는 문장은 없다) | 「… macOS 만 먼저 낸다(**OQ-W06 의 처분으로 사용자 승인을 받은 뒤**)」 한 구절 추가 |
| **W-6** | 미결 게이트 OQ-W02·OQ-W04 행(`:887`·`:889`) ↔ Open Issues(`:956`) | Open Issues 가 「**전부 옵션 + 권장으로 정리했고**」라 쓰는데 **OQ-W02 에만 권장이 없다**(W03·W04 는 「권장」 표기 있음). 또 **OQ-W04**(ingress 경로 분기 vs 백엔드 `StaticFiles`)는 권장안 A 가 **제품 계약을 바꾸지 않는 구현 선택**인데 Phase 6 을 막는 **사용자** 미결로 올라 있다 — 사용자 gate 하나가 불필요하게 는다. (OQ-W02 자체는 **회사 org 레포**(`MediSolveAIDev/k8s_infra_mac`)에 개인 제품 차트를 넣는 문제라 **진짜 사용자 결정이 맞다** — D-08 은 클러스터를 정했지 레포를 정하지 않았다) | ① OQ-W02 에 권장 한 줄을 붙인다 ② OQ-W04 의 성격을 「**구현이 고를 것 — 코디 기본값 A(ingress 경로 분기), 사용자가 뒤집으면 변경**」으로 바꾸고 Phase 6 의 차단 목록에서 뺀다 |
| **W-7** | Code Surface `:185` | 「`stream.ts:251` … 마이크가 **실제로 열리는 유일한 자리**」 — 실물은 **둘**이다. `frontend/src/features/meetings/microphone.ts:31` 과 `frontend/src/features/browser/liveTranscription.ts:11` 이 각각 `getUserMedia` 를 부른다(같은 문서의 L-07 행이 후자를 인정한다) | 「**회의 라이브에서** 마이크가 열리는 유일한 자리」로 한정 |
| **W-8** | 실측표 M-2 행(`:767`) · Phase 2 중단 조건(`:420`) | M-2 를 `audio/webm;codecs=opus` **하나**로 재고 「열리지 않으면 **중단**」이라 쓴다. 실물은 두 경로가 다르다 — 회의 라이브는 `microphone.ts:17` 의 **단일 MIME 하드코딩**(후보 없음), 브라우저 인터랙션은 `liveTranscription.ts:13` 이 **이미 후보 셋**(`audio/webm;codecs=opus` → `audio/webm` → `audio/mp4`)을 갖는다. 뭉뚱그리면 ① 브라우저 경로가 mp4 로 살아 있는데 전체를 중단하거나 ② 회의 경로가 죽었는데 「하나는 됐다」로 넘어간다. 서버 수용 경로도 WS 스트림 vs 업로드로 다르다 | M-2 방법 칸을 **두 경로로 갈라** 적고, 중단 조건을 「**회의 라이브 경로(`microphone.ts:17` 의 단일 MIME)가 열리지 않을 때**」로 한정. 브라우저 경로는 「어느 후보로 떨어졌는가 + 그 원본을 서버가 받는가」를 따로 관측 |

---

## 코디네이터 우려 1~3 에 대한 답

### 우려 1 — 「같은 코드 레포이므로 워크트리를 따로 잡는다」가 런북과 충돌하나?

**충돌한다. 그리고 「WORK-005 와 코드가 안 겹친다」도 사실이 아니다.** → **F-1(저지).**
실제 파일 충돌 근거를 찾았다 — WORK-005 의 유일한 커밋 `a1f6791` 이 `frontend/src/App.tsx`(+35)와
`frontend/src/lib/labels.ts`(+126)를 바꿨고 **아직 `origin/main` 에 없다.** WORK-006 Phase 4 는 그 두 파일을 다시 연다.
새 워크트리는 `base: origin/main`(프로젝트 config)이라 **WORK-005 코드가 없는 트리**가 된다 — 런북 §1 이 기록한
2026-09-05 사고 그대로다. 새 워크트리가 필요한 상황은 **사용자가 새 코디 세션을 띄울 때**뿐이고,
그때도 base 가 `a1f6791` 을 포함해야 한다.

### 우려 2 — Phase 6 이 문서 구성안뿐이면, Phase 8 전에 실제 구현·배포 Phase 가 있나?

**없다.** → **F-2(저지).** 차트·Application 실물 작성, arm64 운영 이미지 빌드, FE 정적 서빙 배선, 배포 실행
어느 것도 Phase 를 갖지 못했다. 원 워커 보고서 §6 이 「별도 발주가 맞다 — 자리를 열어 두기만 했다」로 자인한다.
그 결과 Phase 8 의 입력(「운영 주소가 실재한다」)과 Done Criteria(「모든 Phase DONE」)가 **계획 안에서 충족될 수 없다.**
다만 **운영 프로파일 해소(P-1/OQ-W05)를 이 work 밖 별도 decision 으로 민 것은 타당하다** — 인증·프로파일은
새 사용자 계약이고, SPEC-006 을 워커가 고치지 않은 것이 맞다. 공백은 **그 결정이 닫힌 뒤의 실행 주체**다.

### 우려 3 — Windows 출시 범위를 임의로 바꾼 것인가?

**아니다 — 범위 변경을 승인한 문장은 없다.** Phase 2·5·7 의 측정 규칙이 「Windows 실기가 없으면
**「검증 불가(장비 없음)」로 남기고** macOS 결과로 대신하지 않는다」를 일관되게 박았고, Pre-deploy Check 와
Done Criteria 도 「검증된 것처럼 쓰지 않는다」로 받는다. D-07 도 「방향이고, 이 판의 결과는 macOS 하나」라고
구분했다. 다만 **「macOS 만 먼저 낸다」의 승인 주체가 그 자리에 없다** → **W-5**(한 구절 추가로 닫힌다).

---

## 원 워커 검수 포인트 R-1 ~ R-7 에 대한 답

| # | 판정 | 근거 |
|---|---|---|
| **R-1** 판정 게이트 세 갈래 | **OK (W-8 단서)** | 「진행/보완/중단」이 조건과 다음 행동까지 표로 갈라져 있고, 「보완」은 「어긋난 항목을 구현 규칙으로 흡수」로 Phase 3 이 받는 자리(작업 7 의 `BLOCKED` 회귀 포함)가 있다. 다만 M-2 를 두 녹음 경로로 갈라야 중단 조건이 과잉/과소가 되지 않는다 → W-8 |
| **R-2** AC Phase 배정 | **OK** | `AC-T17` 은 「훅을 잰다」로 M-3 에 걸려 있고 점유 잔존과 섞이지 않았다(spec `:805-808` 과 일치). `AC-T24` 는 Phase 3 「개발 origin 잠정」 / Phase 8 「최종」으로 갈라졌다. `AC-T32`·`AC-T38` 은 구현 층을 M-6 결과로 미루고 Phase 5 는 「확인 창이 하나만 뜨는가」만 잰다 — 모순 없음. 전수도 맞다(아래 수치) |
| **R-3** I-1~I-8 이 실제로 닫히나 | **OK** | 여덟 줄이 SPEC §4「왜 TTL 을 버렸나」·§5「점유의 안전성」의 문장과 1:1 로 대응하고(비교 확인), Phase 3 「하지 말 것」에 「TTL·타이머·주기 갱신을 넣지 마라」, Phase 4 「하지 말 것」에 「주기적으로 도는 것을 만들지 않는다」, Phase 1 탐침에도 같은 금지가 박혔다. 「어려우면 구현을 바꾸지 말고 코디에게 올린다」도 Phase 3·5 양쪽에 있다 |
| **R-4** M-2b 측정 수단 | **성립한다** | `backend/src/ax_workspace/platform/auth_sessions.py:12` `DEFAULT_SESSION_TTL = timedelta(hours=12)` — **env 로 열려 있지 않다**(생성자 기본값). 세션은 DB 테이블이고 `AuthSessionRecord.expires_at` 을 `member_for()` 가 매 조회마다 본다(`:33-35`) → **개발 DB 의 행을 과거로 당기면 제품 코드 0줄로 만료를 만들 수 있다.** 더 싼 대안은 안 보인다(TTL 을 env 로 여는 것은 제품 변경이므로 제안하지 않은 판단이 맞다) |
| **R-5** Phase 6 「사실 / 제안」 분리 | **지켜졌다** | 6-1~6-4 네 칸 모두 좌=확인된 사실(좌표 포함) / 우=옵션+권장으로 갈렸고, 작업 1 이 「**코디가 대신 정하지 않는다**」로 닫는다. 사실 칸의 좌표를 표본 검증했다 — `http_auth.py:106-107`(`cookie_secure` = PRODUCTION 일 때만) · `delivery/Dockerfile:63`(`codex-linux-x64`/`x86_64-unknown-linux-musl`) · `Makefile:25`(`PROTECTED_PLATFORM ?= linux/amd64`) **전부 일치**. 다만 권장 표기 자체가 빠진 칸이 하나 있다 → W-6 |
| **R-6** Rollback 「되돌릴 수 없는 것」 | **보강 권장(비저지)** | 식별자·발행된 Release 둘은 맞다. 표 본문이 이미 「Argo Application 을 지우면 워크로드가 사라지고 **데이터는 되돌아오지 않는다**」를 담고 있으나, 「되돌릴 수 없는 것」 목록에는 **영속 볼륨/DB 삭제**가 항목으로 올라와 있지 않다. 한 줄 추가를 권한다 — 「**PVC·hostPath 를 지운 뒤의 녹음 원본·자료 파일**(`AX_RECORDINGS_DIR`·`AX_MATERIALS_DIR`)」 |
| **R-7** Phase 6 과 3·4 의 병행 | **판단은 맞다(조건부)** | 파일이 안 겹치는 것은 사실이다(Phase 6 은 인프라 레포·운영 이미지 자리, Phase 3·4 는 `frontend/`). 다만 **F-2 를 닫은 뒤** — 6b(실행)가 생기면 `frontend/` 빌드 산출물과 순서를 공유하므로 그 지점부터는 병행이 아니라 순서가 된다. 「사람이 하나다」는 코디 판단이 맞다 |

---

## 전수 검증 수치 (확인한 것)

| 항목 | 기준 | 결과 |
|---|---|---|
| AC 전수 | SPEC `AC-T01`~`AC-T43` | SPEC 유니크 **43** / WORK 추적표 유니크 **43** — **누락 0 · 초과 0** |
| AC Phase 배정 | 중복 0 | Phase 3=**15** · 4=**5** · 5=**21** · 7=**1** · 8=**1** = **43**, 중복 0 |
| 실측 전수 | M-1~M-14 + M-2b = 15 | 실측표 **15행** 전수 — Phase 2=**10** · Phase 5=**4** · Phase 7=**1**. M-1·M-5 는 Phase 8 「최종 확인만」(새 항목 아님) |
| 실측↔AC 정합 | SPEC §6 의 「막히는 인수조건」 | AC 추적표의 「실측」 칸이 SPEC 의 대응과 어긋난 행 **0건** |
| DEC 추적 | D-01~D-09 | **9건 전수**, 각각 받는 자리 + 상태(받음/부분/경계만). D-03 「부분」(일시정지 부재)·D-06 「부분」(절차서 후속)·D-07 「⚠ Windows 미확인」 표기가 사실과 일치 |
| 선행조건 순환 | 0 | `1→2→3→4→5`, `6`(미결 gate·3·4 병행), `7←5`, `8←5·6·7` — 역참조 0. **단, F-2·F-3 의 「주인 없는 선행」은 순환이 아니라 공백이다** |
| 계약 보존 | 브리프 §3 여덟 | 네이티브 소유 · 커맨드 **넷** · TTL/renew 없음 · 「완료」 사건 해제 · 취소된 닫기 보존 · degraded 재무장 · 늦은 acquire 잔존 0 · 웹 hang 한계 — **I-1~I-8 로 전수 보존.** SPEC 본문 복제 없음 |
| SPEC·DEC 불변 | diff 0줄 | `git status` 상 `20-spec/`·`10-decision/` 의 두 파일은 이번 워커 이전에 이미 untracked 로 있던 것이고, WORK 워커가 남긴 변경은 없다. index·`log.md` 도 **미수정**(갱신안만 제안) |
| 자리 규칙 | `para/projects/project.md` 단계 | `30-work/work-006-*.md` — 새 최상위 디렉토리 없음. 산출물 2건 모두 브리프 §5 안 |
| 양식·frontmatter | `templates/projects/30-work/work.md` | 14절 전부 존재·순서 일치. frontmatter 필수 키 전부 · `links.decisions`/`links.specs` 가 **실재 파일**을 가리킴 |
| 검증 완료 선체크 금지 | `- [x]` 0 | **0건** · Phase Status 8개 전부 `TODO` · `progress: 0` · `status: todo` |
| 린트 | `rules/check-concept-map.py` | **exit 0**. `scripts/lint-pipeline.py` 는 **확인 안 함 — 레포에 `scripts/` 자체가 없다** |
| 코드 좌표 | a1f6791 | 표본 **16곳 전부 일치**(§검수 범위에 목록). `api.ts` fetch **9곳** 개수·줄번호 일치 |
| 워커 설정 사실(P-4) | `config/projects/strong-hajin.json` | `frontend.allowed_paths = ["frontend/"]` — `src-tauri/` 를 덮는다 ✓. `verify` 에 `cargo`·tauri 명령 **없음** ✓ → 제안이 사실에 맞다 |
| fixture 실행 가능성 | `Makefile` | `local-stack`(:193) · `frontend-test`(:96) · `verify`(:102) **전부 실재** ✓ |

---

## 남은 사용자 결정 — 「진짜 결정」과 「구현 선택」을 가른다

**진짜 사용자 결정 (5)**

| ID | 결정 | 왜 사용자 몫인가 |
|---|---|---|
| OQ-T01 | 최소 OS · CPU 아키텍처 · 설치파일 형식 | 배포 대상의 범위 — 문서로 답이 안 난다 |
| OQ-T02 | 운영 도메인 | 소유한 이름이 있어야 한다. **발명 금지가 지켜졌다** |
| OQ-T03 | 배포 대상 · 서명 · 공증 · 자동 업데이트 | 서명 신원·비용. 참조 제품에 선례 0건(문서가 그렇게 적었다) |
| OQ-W01 / OQ-W06 | Windows **실기** 보유 / Windows **빌드 환경** | 장비 사실. 없으면 그 축은 검증 불가로 남는다 |
| OQ-W02 | 배포 구성이 들어갈 레포 | **회사 org 레포**(`MediSolveAIDev/k8s_infra_mac`)에 개인 제품 차트를 넣는 문제. D-08 은 클러스터를 정했지 레포를 정하지 않았다 → **재확인이 필요한 이유가 있다** (다만 권장안은 붙여라 — W-6) |
| OQ-W05 | 운영 프로파일 해소(라우트 등록 / 새 프로파일 / `cookie_secure` 분리) | 인증·배포 프로파일 = **새 제품 계약**. 별도 decision 으로 민 판단이 맞다 |

**구현 선택 — 사용자 gate 로 둘 필요가 없는 것 (2)**

- **OQ-W04** FE 정적 서빙 방식 — 권장 A(ingress 경로 분기)는 제품 코드를 안 건드린다. **코디 기본값으로 통보하고 진행**해도 되는 자리 → W-6
- **OQ-T06**(허용 origin 값) · **OQ-T08**(L-12 처분) · **OQ-T10**(창 닫기와 프로세스) — 이미 「구현이 고를 것」으로 올바르게 분류돼 있다
- **OQ-W03**(arm64 운영 이미지 신설)은 **이미지 하나가 느는 비용 결정**이라 사용자 몫으로 둔 것이 타당하다

---

## 기존 부채 (이번 판정 제외)

- `work-005-projects.md:101` 「**커밋은 아직 0건이다** — 1루프의 모든 변경이 코드 워크트리에만 있다(2026-09-22 확인)」가 **낡았다.**
  지금은 `a1f6791` 한 커밋으로 들어가 워크트리가 깨끗하다. WORK-006 이 만든 문제는 아니지만, F-1 을 고칠 때
  같이 보면 좋다(코디 몫).
- `k8s_infra_mac/README.md` 의 `k8s-test` 설명이 실물(`main` 추적)과 다르다 — WORK-006 이 인용하지 않고
  사실을 다시 센 것은 맞는 처리다. 레포 자체의 부채.

---

## 검수하지 않은 것 (숨기지 않는다)

- **실측·빌드·테스트·설치·배포를 하나도 실행하지 않았다.** 계획의 실행 가능성은 문서·코드 읽기로만 판단했다.
- `scripts/lint-pipeline.py` **미실행** — 레포에 없다.
- 인프라 레포의 **비밀값 파일을 열지 않았다.** `charts/`·`argocd/applications/` 의 Application·차트 구조만 읽었다.
- 서버·클러스터에 **접속하지 않았다.** 클러스터 상태는 `tauri-deployment-decisions.md` 의 기록을 인용했고,
  레포 파일로 교차 확인 가능한 것만(Application 수·`targetRevision`) 직접 셌다 → W-4.
- Tauri v2 의 `remote.urls`·네비게이션 훅의 **실제 동작을 검증하지 않았다.** 그것이 M-1·M-3·M-7 의 목적이고,
  이 계획이 미수행으로 둔 것이 맞다.
