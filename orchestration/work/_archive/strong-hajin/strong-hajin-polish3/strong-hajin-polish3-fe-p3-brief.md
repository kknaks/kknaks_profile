# [frontend] WORK-010 Phase 3 — 데스크톱 셸 · 첨부 응답을 파일로 저장

너는 **strong-hajin `frontend` 워커**(이번 몫은 Tauri 셸)다. **너는 이 작업의 맥락이 없다** — 먼저 읽어라:
- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`
- SPEC-006(정본) `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` — **U-5 · S-14 · E-15 · §5 · AC-T44~48 · M-15 · OQ-T12·T13(코디 닫음)**, 그리고 권한 최소 원칙(U-1·§2.5 「셸은 문구를 그리지 않는다」)
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` — **Phase 3** 체크박스(계약)
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-survey-report.md` §2-3·§2-4 · `be-survey-report.md` §2(서버 헤더·wry 0.55.1 `navigation.rs` 분석)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` (base `origin/main` `d1b5137`)
⚠ **다른 frontend 워커가 같은 워크트리 `frontend/src/` 에서 Phase 1 을 동시에 한다**(LoginPage·MeetingDetailPage). **너는 `frontend/src-tauri/` 와 토스트 수신부 `frontend/src/lib/shell.ts`·`frontend/src/App.tsx` 만** 만진다. 그 밖의 `frontend/src/` 가 필요하면 코디에게 먼저 묻는다.

## 1. 문제
운영 데스크톱(medi-ax)에서 회의 상세 「내보내기」(`GET /api/meetings/{id}/export?format=html` → `text/html` + `Content-Disposition: attachment; filename*=UTF-8''…`)를 누르면 **내보낸 HTML 이 앱 창에 그려지고 돌아갈 길이 없다**(사용자 확인). 셸에 다운로드 핸들러가 없고, wry 는 핸들러가 없으면 표시 가능한 MIME 을 Allow 한다.

## 2. 계약 (요약 — 상세는 WP Phase 3 · SPEC-006 U-5)
1. 첨부 응답은 **OS 다운로드 폴더에 대화상자 없이** 저장, 파일명은 서버 `filename*`(UTF-8 한글), 같은 이름이면 `이름 (1).html` 처럼 번호. **창의 문서는 바뀌지 않는다.** 같은 origin 이동(내보내기)과 `_blank` 첨부 링크(업무 자료·요청 첨부) 둘 다
2. 저장 결과(성공 + 파일 이름 / 실패)는 **셸이 웹 앱에 알리고, 웹 앱이 기존 공통 토스트**(`App.tsx` `putNotice`)로 보인다. 셸은 문구를 그리지 않는다
3. 인라인 `_blank`(채팅 근거·AX 링크·표시 가능한 자료)는 바꾸지 않는다(OQ-T13)
4. medi-ax·strong-hajin 두 판 모두
5. **권한·플러그인 최소** — capabilities 변경을 전부 보고하고, 파일 권한을 웹에 열지 않는다(저장은 Rust 쪽에서)
6. **먼저 확인**: tauri 2.11.6 / wry 0.55.1 에서 (a) 응답 단계 `Content-Disposition` 으로 첨부를 가를 수 있는지 (b) `download_handler`(on_download)가 WKWebView 에서 `text/html` 첨부에 대해 실제로 불리는지 — 소스(`~/.cargo/registry`)로 확인. **불리지 않는 구조면 구현 전에 그 근거와 대안을 코디에게 묻는다**(예: `on_navigation` 에서 export 경로를 가로채 Rust 가 쿠키를 실어 직접 받기 — 쿠키 접근 가능 여부 포함)

## 3. allowed_paths
- `frontend/src-tauri/` · `frontend/src/lib/shell.ts` · `frontend/src/App.tsx` (+ 그 둘의 옆자리 테스트)

## 4. 하지 말 것
- 커밋·push 금지. **앱·서버·프론트를 띄우지 마라. 사용자 포트(8001·5176·54329)를 건드리지 마라** — macOS 실기 확인은 코디가 한다(네가 `make tauri-local` 을 돌리지 않는다)
- 서명·공증·dmg 빌드 금지. 서버 코드 수정 금지

## 5. 검증
```
frontend/src-tauri 에서 cargo check · 핵심 로직(파일명 파싱·번호 붙이기·첨부 판별) cargo test · cargo clippy -- -D warnings. 웹 수신부를 바꿨으면 frontend 에서 해당 테스트 + npx tsc --noEmit. 실제 실행하지 못한 검증(실기·Windows)은 pending 으로 보고.
```
- 보고에 **코디가 실기로 확인할 절차**(어느 화면에서 무엇을 누르고 무엇이 보여야 하나)를 적는다

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p3-worker-report.md` 에 **파일로도** 남긴다(터미널이 죽어도 이어지게).
```bash
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(셸) 완료: WORK-010 Phase 3" \
  --body "변경 파일 / 계약 체크 결과 / grep 으로 센 자리 표 / 기준선 vs 결과 / DS-gaps / 미결"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] frontend 완료 — WORK-010 Phase 3. 리포트 fe-p3-worker-report.md" --enter
```
막히면: `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] frontend: <질문>" --enter`
