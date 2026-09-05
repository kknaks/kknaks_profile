
# 재개 노트 — docs-v1 (task-management)

> **작업 단위 = 이 워크트리(브랜치 task-management-app) 1개 = 이 slug 1개.**
> v1 문서 파이프라인(디자인 분석 → 영역별 baseline+decision → spec)이 전부 여기서 돈다.
> 워커 추가 발주는 새 slug 를 파지 않고 `new-work.sh task-management docs-v1 --workers <w>` 로 이 폴더에 브리프를 더한다.

**지금**: Phase 1 완료 · 결정형 OQ 16건 해소 · **구조 게이트 3건 확정**(정적 빌드 / shadcn / 유동 반응형)
**다음**: **Phase 2 — SPEC-000 공통 기반부터.** 디자인 대기 항목은 `design-requests.md`(병행)

세팅: `scripts/new-work.sh task-management docs-v1` · 설정 SSOT `config/projects/task-management.json`
코디handle: `term_6a4ac855-2a13-4484-b808-4c25182cbb2b` (09-03 세션 재연결로 갱신 — 이전 `term_e6d07c2f…` 는 stale)

## 워크트리

- `docs`: 코디 워크트리 공유 (`workspace: coordinator`) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (branch `task-management-app`, base `origin/main` → PR `main`). 워커 개별 워크트리 없음.

## 0. 계획 (2026-09-03 사용자 합의)

범위: 현 패키지 6영역. 홈·채팅 제외(디자인 재입수 시), 자료함은 문서함 확정안.
영역당 문서 세트: **기획서 BASE**(템플릿+왜+기능명세+인/아웃바운드) + **정책서 DEC**(8절, CRUD 규약) → **기능정의서 SPEC**(기존 템플릿). 영역 하나씩 직렬.

### Phase 1 — 영역별 BASE+DEC (writer, 영역당 발주 1회)

| # | 영역 | 문서 | 순서 근거 | 상태 |
|---|---|---|---|---|
| 1 | 인증·설정 | BASE-001+DEC-001 | 프로젝트·유형 관리가 설정 소관 — 업무가 참조하므로 최우선 (사용자 확정) | **작성 완료 — 사용자 리뷰 대기** |
| 2 | 내 업무 | BASE-002+DEC-002 | 원자 도메인. 설정의 프로젝트·유형 소비 | **작성 완료 — 사용자 리뷰 대기** |
| 3 | 회의록 | BASE-003+DEC-003 | 내 업무 생성/수정 규약 소비 | **작성 완료 — 사용자 리뷰 대기** |
| 4 | 문서함 | BASE-004+DEC-004 | 업무·회의록의 첨부 대상 (확정안 기준) | **작성 완료 — 사용자 리뷰 대기** |
| 5 | 캘린더 | BASE-005+DEC-005 | 업무·회의록 드로어 재사용 — 늦을수록 결정 적음 | **작성 완료 — 사용자 리뷰 대기** |
| 6 | 메시지함 | BASE-006+DEC-006 | **v1 목록 UI만, 기능 전부 v2**(수신이 연동에 걸림) | **작성 완료 — 사용자 리뷰 대기** |

영역 사이클: writer 발주 → 코디 검증 → 사용자 리뷰·OQ 답 → accepted → 다음 영역.
임의 결정 금지 — 닫히지 않은 것은 전부 Open Questions.

### Phase 2 — SPEC

- 진입 게이트(사용자): Q-28 Tauri 정적 export · Q-33 shadcn 도입+토큰 매핑 · Q-34 실측좌표 vs 유동
- SPEC-000 공통 기반(토큰·셸·오버레이 3종)부터 → 영역별 SPEC 은 accepted 정책서 순서대로

### Phase 3 — 코드

- `kknaks/task_management` 스캐폴딩이 첫 work. config 에 `repos.code` 추가, 코드 워커는 개별 워크트리 + 문서 경로 배제, 문서/코드 PR 분리.

## 1. 지금

- [x] **Phase 1** — BASE/DEC-001~006 + 결정형 OQ 16건 해소
- [x] **구조 게이트 3건** — 정적 빌드 / shadcn / 유동 반응형
- [x] **아키텍처 ①②** — system·database(+domains 5)·backend·frontend 9문서. architect OQ 10건 해소
- [~] **Phase 2 SPEC 12건 · 4배치** — ① 000~002 ✅ / ② 003~005 ✅ / **③ 006~008 진행** / ④ 009~011 대기
- [ ] **이어서(사용자 지시 2026-09-05): ③ 검증 → ④ 발주·검증 → WP 1그룹 작성**
- [ ] **WP 1그룹** = SPEC-000~002 대응 구현 단위(스캐폴딩 → 로그인·세션 → 업무 설정). 스캐폴딩이 첫 work 이고, 그때 config 에 **`repos.code`**(`kknaks/task_management` 별도 clone) 추가
- [!] **미설계 화면은 디자이너에게 넘기지 않는다** — 디자인 작업은 끝났고, **spec 이 디자인 시스템 토큰·규칙으로 직접 확정**한다(배치별로 닫는 중)
- [!] **남은 OQ 2건뿐** — 브라우저 하한(FE-OQ-2)·Tauri 창 minWidth(FE-OQ-3). 둘 다 앱 창에서 돌려보면 정해진다
- [!] spec 이 정책서에 없던 것을 정하면 **코디가 사용자 확인 후 정책서에 승인 기록**한다(DEC-002 §「SPEC 판단 승인분」이 표본)
- [!] 알림은 **별도 도메인** — v1 범위 밖, 나중에 영역 하나 필요

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-03 | 문서 워커는 workspace=coordinator 로 코디 워크트리에 직접 탑승 (유실 재발 방지) | 사용자 승인 · runbook §workspace |
| 2026-09-03 | 기획서=템플릿+왜+인/아웃바운드+기능명세(기능 단위), 정책서=템플릿+규약(CRUD 기준), 기능정의서=기존 템플릿. 영역 하나씩 진행 | 사용자 지시 |
| 2026-09-03 | designer 역할 = 페이지 구성 + Next.js 구조 + shadcn 컴포넌트 + 공용 컴포넌트 도출 + 소요 파악 | 사용자 지시 |
| 2026-09-03 | 홈화면.dc.html 패키지 제외(홈·채팅은 나중) · 자료함 정본=문서함.dc.html · 메시지함 v1 범위 보류 | 사용자 확정 (Q-27·26·35) |
| 2026-09-03 | ~~문서화는 내 업무부터~~ → **인증·설정부터** (09-03 번복 — 업무가 설정의 프로젝트·유형을 참조하므로 설정 선행) | 사용자 확정 |
| 2026-09-03 | 작업 단위 = 워크트리 1개 = slug 1개. design-frontend-structure+auth-docs → docs-v1 통합 | 사용자 교정 · runbook §workspace |
| 2026-09-03 | Phase 1~3 전체 계획(§0) 합의 | 사용자 승인 |
| 2026-09-03 | **문서(기획·정책·spec)는 발주하지 않는다** — 논의로 닫고 코디가 직접 작성, 사용자 리뷰. 워커 발주는 분석형 작업과 Phase 3 코드만 | 사용자 확정 |
| 2026-09-03 | 인증·설정 정책 일괄 확정 — 상세는 DEC-001 (로그인·세션·유형/프로젝트·소프트 딜리트·목 UI 4종) | 사용자 논의 |
| 2026-09-03 | 내 업무 정책 일괄 확정 — 상세는 DEC-002 (유형 필수·프로젝트 N:1 무소속·완료 게이트·DnD·소프트 딜리트) | 사용자 논의 |
| 2026-09-03 | STT 엔진 = **Soniox**(stt-rt-v5·ko·화자분리 on·endpoint detection off). 전송은 프론트→백엔드→Soniox 릴레이(백엔드가 원본 적재 겸함) | 사용자 논의 · soniox-study |
| 2026-09-03 | 회의록 정책 일괄 확정 — 상세는 DEC-003 (**사람·AI 2트랙**·배치 조합 트리거·증분 후 전체 재정리·통합본 정본) | 사용자 논의 |
| 2026-09-03 | 문서함 정책 일괄 확정 — 상세는 DEC-004 (PARA 고정·두 축 독립·md 전용·업로드만·색인/버전 v2·휴지통) | 사용자 논의 |
| 2026-09-03 | 캘린더 정책 일괄 확정 — 상세는 DEC-005. **schedule 테이블 분리**가 이 영역의 구조 결정(업무·회의 시간 이관, 겹침 검사 단일화, v2 외부 캘린더 자리) | 사용자 논의 |
| 2026-09-03 | **웹 우선 개발, Tauri 래핑은 마지막** — 개발은 브라우저 기준, Tauri 는 배포 층(셸: 마이크 권한·키체인·파일 선택창). 마이크 스파이크도 래핑 시점으로 연기 | 사용자 확정 |
| 2026-09-03 | **인증 전송 개정: 쿠키 → Bearer** — Tauri 웹뷰 origin 문제 + 「앱 종료 시 로그아웃」을 세션 쿠키 수명에 맡기지 않기 위함. refresh 는 OS 키체인(웹 개발 중엔 브라우저 저장소로 임시, 저장소 추상화 한 곳에서) | 사용자 확정 (아키텍트 제안 수용, DEC-001 개정) |
| 2026-09-03 | **기술 스택 확정** — Next.js **정적 빌드**(`output: 'export'`, 데이터는 클라이언트→FastAPI) · **shadcn/ui 도입**(토큰을 CSS 변수로) · **유동 반응형**(1920 실측 좌표는 참고값, absolute 금지) | 사용자 확정 |
| 2026-09-03 | **메시지함 v1 = 목록 UI만, 기능 전부 v2** — 수신이 연동(목 UI)에 걸려 v1 에 받을 메시지가 없다. "v1도 지금 너무 비대해" | 사용자 확정 |
| 2026-09-03 | **v2 예약 UI 가 여러 영역에 누적** — 소셜 로그인·목소리·연동 관리·계정 삭제(DEC-001) + AI 색인·버전(DEC-004). 「v2에서 제공됩니다」 표시 **공통 규격**이 필요 (DEC-004 OQ-2) | 코디 관찰 |
| 2026-09-03 | **설계한 실패만 처리하고 그 외 예외는 fallback 없이 전파** — 광범위 예외 포착은 깨진 지점을 가린다. DEC-003 §7 에 명시, 이후 영역에도 같은 원칙 적용 | 사용자 확정 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend (WORK-001 P1·2) | `term_d6f9d145-12d9-4645-8762-5d4399063bd8` | `task_652a15f48f00` | `ctx_b124b7ae7fe0` | `docs-v1-work001-be-brief.md` | 완료 — 커밋 `2a4d29a`, 검증 10/10 |
| frontend (WORK-001 P3·4) | `term_f01dc2f5-b55c-4016-b40a-93628c497a25` | `task_7e2bf4726de0` | `ctx_7d3baf2cf47a` | `docs-v1-work001-fe-brief.md` | 완료 — 커밋 `84882c0`, 앱 창 E2E 통과 |
| reviewer (WORK-001) | `term_82e0a355-3e75-47b2-8e8f-2d03e3458c47` | `task_5ae8b0e0bc24` | `ctx_00c0163ca443` | `docs-v1-work001-review-brief.md` | 완료 — FAIL 0 · WARN 3 · 문서 공백 18 |
| frontend (WORK-003 P2·3) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_1d2587dd689b` | `ctx_e15797bfefbc` | `docs-v1-work003-fe-brief.md` | **진행** — 팔레트·공용 컴포넌트·설정 화면 |
| backend (WORK-004 P1~3) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_3f9640623be2` | `ctx_470ee3f4a2e9` | `docs-v1-work004-be-brief.md` | 완료 — 업무 도메인·본체 API·자식 컬렉션 |
| frontend (WORK-004 P4~6) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_2c1d45b0afd9` | `ctx_b78cc4317744` | `docs-v1-work004-fe-brief.md` | 완료 — 커밋 `7550e1b`, DrawerFrame 840 단일 소유 |
| backend (WORK-004 후보 표면) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_43cc89b19825` | `ctx_6dec49ec6b57` | `docs-v1-work004-be-fix-brief.md` | 완료 — 커밋 `70924d7`, 컬렉션 표면 전환·pytest 80 |
| backend (WORK-004 scope·total) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_be9dfadef1b9` | `ctx_67d31922b6b5` | `docs-v1-work004-scope-be-brief.md` | 완료 — 커밋 `9897ff5`, pytest 92 · scope 별 total 2/39/41 |
| frontend (WORK-004 칩 3) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_5cd1c8a8c416` | `ctx_76a2f51cc313` | `docs-v1-work004-chips-fe-brief.md` | 완료 — 커밋 `99a45e7`, 칩별 4/40/42건 실측 |
| reviewer (WORK-004) | `term_7bdbe08f-3921-4838-af97-65a981dc702c` | `task_117e21ab82e0` | `ctx_11aeef4eac46` | `docs-v1-work004-review-brief.md` | 완료 — **FAIL 4 · WARN 10 · 공백 7**. 드로어 규격·게이트 뒷문 두 축은 PASS |
| backend (WORK-004 FAIL 수정) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_7a39c670d5c6` | `ctx_a063e8f064e1` | `docs-v1-work004-fix-be-brief.md` | 완료 — 커밋 `ddb53d2`, pytest 237 |
| frontend (WORK-004 FAIL 수정) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_5621f6b473fd` | `ctx_06853a01ece8` | `docs-v1-work004-fix-fe-brief.md` | 완료 — 커밋 `b46771d`, 앱 창 6항목 + 결함 1건 추가 발견·수정 |
| frontend (WORK-004 U-7 마무리) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_5458181ac7ab` | `ctx_9625b1db052f` | `docs-v1-work004-attach-notice-brief.md` | 완료 — 커밋 `c6ba429`, 해제 컨트롤 신설·404 분기 |
| backend (WORK-005 P1·2) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_c949630b9ce4` | `ctx_b86bdef9d3ac` | `docs-v1-work005-be-brief.md` | 완료 — 커밋 `46fe87a`, pytest 291 · 리비전 0003 추가 |
| frontend (WORK-005 P3·4) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_aa0ea21b217c` | `ctx_b5a8899aba10` | `docs-v1-work005-fe-brief.md` | 완료 — 커밋 `ad2d4a5`, 71통과 · **DnD 드롭 캡처 미완** |
| reviewer (WORK-005) | `term_7bdbe08f-3921-4838-af97-65a981dc702c` | `task_3ee2cc39983c` | `ctx_e0896b768dec` | `docs-v1-work005-review-brief.md` | **진행** — 게이트 단일 판정·낙관적 갱신 반대 축 |
| architect (WP 5건) | `term_27b5a8ac-c826-4d41-aa07-f3e8e7c99436` | `task_9a711335fc43` | `ctx_f7e9d11792c5` | `docs-v1-wp2-brief.md` | 완료 — 커밋 `0fbf95a`, WORK-004~008 |
| frontend (WORK-003 FAIL 수정) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_738950d797de` | `ctx_b5b661721471` | `docs-v1-work003-fix-brief.md` | 완료 — 커밋 `61ac762`, 6초 잔존·재시도 0 실측 |
| reviewer (WORK-003) | `term_7bdbe08f-3921-4838-af97-65a981dc702c` | `task_d624e85e4787` | `ctx_bea03af664a2` | `docs-v1-work003-review-brief.md` | 완료 — FAIL 1 · WARN 7 · 공백 12 |
| backend (WORK-003 P1) | (같은 터미널) | `task_0a73641cb226` | `ctx_eca4171a6527` | `docs-v1-work003-be-brief.md` | 완료 — 커밋 `ffc544d` |
| frontend (WORK-002 FAIL 수정) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_0d73d27dfe90` | `ctx_626a38011048` | `docs-v1-work002-fix-brief.md` | 완료 — 커밋 `533843e`, F-3 실측 200→401 |
| reviewer (WORK-002) | `term_7bdbe08f-3921-4838-af97-65a981dc702c` | `task_37a4fa98da1e` | `ctx_2717269ded8c` | `docs-v1-work002-review-brief.md` | 완료 — **FAIL 3 · WARN 4 · 공백 13** |
| frontend (WORK-002 P2·3) | `term_758c07cd-9ca9-49c3-9ad7-25f82bcc782a` | `task_ca9c6d573f35` | `ctx_22727520ae54` | `docs-v1-work002-fe-brief.md` | 완료 — 커밋 `c49ae72`, 앱 창 로그인 왕복 |
| backend (WORK-002 P1) | `term_27cfe374-d8ad-41b0-a814-04f142c5626e` | `task_95532fa465bc` | `ctx_2af9c8e23129` | `docs-v1-work002-be-brief.md` | 완료 — 커밋 `37a8ce1`, pytest 31 + curl 전항목 |
| ~~backend (WORK-002 1차)~~ | ~~`term_07e3fc7a…`~~ | ~~`task_ac218285b40e`~~ | ~~`ctx_c7499e125b30`~~ | (폐기) | 중지 — 잘못 만든 워크트리(빈 트리)에서 발주. 위 행으로 재발주 |
| architect spec② | `term_da8c7759-cf0d-4d3f-bdb5-fba8798cf3ce` | `task_e07df0fc245a` | `ctx_2f06821688a3` | `docs-v1-spec2-brief.md` | **진행** — SPEC-003·004·005 |
| architect spec① | (같은 터미널) | `task_41b985520192` | `ctx_ae07aac081a1` | `docs-v1-spec1-brief.md` | 완료·검증 PASS |
| architect 아키텍처② | (같은 터미널) | `task_95fed4429873` | `ctx_623f62aa44fd` | `docs-v1-arch2-brief.md` | 완료·검증 PASS |
| architect ① | (같은 터미널) | `task_b3fa2aca8cc3` | `ctx_4d1e7388e22f` | `docs-v1-arch-brief.md` | 완료·검증 PASS |
| designer | (종료) | `task_319a3ee765d4` | `ctx_cb4ec3ab8c8a` | `docs-v1-design-brief.md` | 완료·검증 PASS |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- 리포트: `docs-v1-design-report.md` — P-01~72 · F-1~13 · C-01~49 · S-01~34 · Q-01~42
- **디자인 요청서**: `design-requests.md` — 정정 A-1~12 · 미설계 B-1~6 · 게이트 C
- 참고 시안: `work-settings-proposal.html` (**확정 아님**, 방향만)
- 조사: `soniox-study.md`
- 커밋: `3e13975` 리포트 · `e9db33a` 사용자 확정 4건 · `efd54e3` slug 통합

## 5. 이력 (최신이 위)

- `2026-09-06` **WORK-005 구현 완료** — Phase 3·4(`ad2d4a5`)로 세 진입점이 `useTaskStatus` 훅 하나를 지난다(정적 검사로 호출처 1곳 증명). **남은 미완 1건: 칸반 DnD 드롭의 네트워크 캡처** — macOS 네이티브 드래그 세션이 합성 이벤트를 안 먹어 자동으로는 성사되지 않는다(탭·타이밍·커서 워프 전부 실패). **사람 손 1회면 닫힌다** — Done Criteria 의 「캡처 3장」 중 하나다
- `2026-09-06` **WORK-005 Phase 1·2 완료**(커밋 `46fe87a`, pytest 291). **WP 의 「마이그레이션 없음」을 벗어나 리비전 0003 추가** — 실행취소가 「마지막 로그가 전이인가 + 직전 상태」를 판정해야 하는데 한국어 로그 본문 되파싱은 문구가 바뀌면 조용히 깨진다. `cancelledAt` 도 저장될 곳이 없어 취소 전이 로그 시각에서 파생한다. ERD T-8-a·T-8-b 반영
- `2026-09-06` **WORK-004 완전 종료** — 첨부·연관 U-7 마무리(`c6ba429`)에서 **연관 해제 컨트롤이 아예 없던 것**과 **첨부 팝오버가 실패에도 입력을 비우던 것**을 추가로 잡았다. 전자는 SPEC-003 U-8 갱신(`632bd93`)으로 닫았다 — 서버 DELETE 표면은 §4 에 처음부터 있었고 화면 문구만 비어 있었다
- `2026-09-06` **워커 질문은 `orca terminal send` 로** — `orca orchestration ask` 는 답이 안 닿아 같은 질문이 세 번 반복되고 7분 넘게 막혔다. 브리프에 명시 절로 넣는다
- `2026-09-06` **WORK-004 완료** — 검수 FAIL 4 · WARN 10 전부 수정(백 `ddb53d2` pytest 237 / 프론트 `b46771d` 61통과). 프론트가 수정 검증 중 **결함 1건을 더 찾았다** — 할일·메모가 `void mutateAsync` 로 결과를 안 받아 낙관 반영이 되돌아가기만 하고 아무 말도 안 남았다. **되돌아가기만 하면 사용자는 체크가 안 눌린 줄 안다**
- `2026-09-06` **U-7 실패 표시는 낙관적 갱신 여부와 별개 축** — 낙관적이면 「되돌린다 + 말한다」, 아니면 「안 바뀐다 + 말한다」. 어느 쪽이든 말은 해야 한다. 첨부·연관 네 자리에 남은 공백을 마저 닫는다
- `2026-09-06` **WORK-004 검수 FAIL 4 · WARN 10 · 공백 7** — 브리프가 지목한 두 축(드로어 폭 소유권·게이트 뒷문)은 PASS. 대신 **상세 헤더가 표시 전용**이라 제목·기한·유형·프로젝트를 못 고치는 것(F-1~3, Acceptance 4항목 실행 불가)과 **할일 응답 타입 불일치로 인한 상세 캐시 오염**(F-4)을 잡았다. 문서 공백 7건을 먼저 닫고 양쪽 수정 발주
- `2026-09-06` **자식 컬렉션 응답 형태를 계약으로 확정** — 쓰기 표면은 전부 `TaskDetail`, 삭제만 204, 없는 자식 삭제는 404. SPEC 이 비워 둔 자리라 구현이 넷 중 셋만 그렇게 했고 할일만 달랐다. **응답 형태는 계약이지 구현 재량이 아니다**
- `2026-09-06` **§8-2 코드 표에 「절차」를 못박음** — spec 이 새 코드를 정하면 그 work 의 검수에서 코디가 반영한다. 같은 공백이 세 검수 연속으로 올라왔다
- `2026-09-06` **WORK-004 계약 공백 2건을 닫음** — ① 연관업무 후보를 **컬렉션 표면**으로(생성 드로어에는 자기 id 가 없다) ② 필터 칩 3 의 대응물 **`scope`·`total`** 신설(칩은 필터인데 서버엔 정렬 힌트뿐이었다). 둘 다 SPEC-003 §4 갱신 후 발주
- `2026-09-06` 아키텍처 backend §3 에 **쿼리 alias 규칙** 추가 — `alias_generator` 는 본문 모델에만 걸린다. 빠뜨리면 파라미터가 조용히 무시되고 200 이 난다(WORK-004 에서 실제로 밟음, WORK-005 목록·필터가 같은 자리)
- `2026-09-03` **Phase 1 완료** — 6영역 BASE/DEC 작성. 논의로 닫고 코디가 직접 작성(발주 없음)
- `2026-09-03` 전체 계획(§0) 합의, _RESUME 에 등재
- `2026-09-03` 작업 단위 교정 — slug 2개(design-frontend-structure·auth-docs)를 docs-v1 로 통합 (사용자 지적)
- `2026-09-03` 사용자 확정 4건 반영 (홈화면 제외·자료함 정본·메시지함 보류·시작 영역) — 시작 영역은 이후 인증·설정으로 번복
- `2026-09-03` designer 리포트 완료·검증 PASS·커밋. 총계(참고안 제외) Page 24 · 오버레이 27 · 신규 컴포넌트 ~43 · 공용 34
- `2026-09-03` designer 발주 (workspace=coordinator 첫 실전). 추후 참고: sonioc(?)·LLM 채팅 내용 추가 예정 — §1 결정 ① 로 이동
