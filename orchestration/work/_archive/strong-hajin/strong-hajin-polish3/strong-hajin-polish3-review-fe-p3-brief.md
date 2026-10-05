# [reviewer] WORK-010 Phase 3 코드 검수 — 데스크톱 셸 첨부 저장

같은 reviewer 다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only** — 리포트 한 장만.

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` 의 미커밋 diff 중 **Phase 3 파일만**: `frontend/src-tauri/`(download.rs 신규·lib.rs·Cargo.toml/lock) · `frontend/src/lib/shell.ts`(+test) · `frontend/src/App.tsx`(+App.test.tsx) 의 다운로드 수신부 · `frontend/src/lib/labels.ts` 의 `shellDownload` 키.
⚠ 같은 워크트리에서 Phase 2a 워커가 `frontend/src/`(업무 상세 — `App.tsx` 의 AX 정리 포함)를 동시에 고치고 있다. **App.tsx 는 다운로드 수신부만** 본다.

## 2. 기준
- SPEC-006 v0.3.1 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` — U-5 · S-14 · E-15 · §5 · AC-T44~49 · M-15 · U-1/§2.5(셸 문구 없음) · 권한 최소 원칙 · U-4(앱 창을 덮지 않는다) · L-09(점유 정리)
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` Phase 3 · 결정 `fe-p3-decision.md` §4(B)·§5(X)
- 워커 보고 `fe-p3-worker-report.md`

## 3. 볼 것
1. 계약 체크마다 PASS/FAIL(파일:줄)
2. **가로채기 범위** — 같은 origin + `/api/` + GET 만인가. 다른 origin·셸 스킴·일반 화면 이동을 잘못 막지 않나. inline 은 정말 아무것도 안 하나(창을 덮지 않나 — U-4)
3. **쿠키·보안** — `cookies_for_url` 을 메인 스레드에서 부르지 않나(교착) · 쿠키를 로그·파일에 남기지 않나 · 다른 origin 으로 쿠키를 보내지 않나(리다이렉트 따라가기 포함) · TLS 검증 끄지 않나
4. **파일 쓰기** — 파일명 경로 조작(`../`·절대 경로·NUL·OS 금지 문자) 막나 · 번호 붙이기 · 임시 이름 → rename · 실패 경로
5. **웹 알림** — `eval` 로 넣는 문자열에 파일명이 들어갈 때 **스크립트 주입**이 안 되나(JSON 직렬화 등) · 셸이 아닌 브라우저에서 구독 안 함 · 문구는 labels
6. capabilities·커맨드·플러그인 변경 0 확인 · 새 crate(ureq) 기능 플래그
7. `cargo test`·`clippy` 를 돌려도 된다(`frontend/src-tauri` 에서) — 앱·서버는 띄우지 마라
8. **사용자가 실물에서 만날 자리** + 코디 실기 절차(보고 §6)가 계약 AC 를 다 덮나

## 4. 판정
FAIL · WARN · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-fe-p3-report.md` 하나

## 6. 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-010 Phase 3 <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 실물 자리 / 리포트 경로"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] reviewer 완료 — Phase 3 <판정>. 리포트 review-fe-p3-report.md" --enter
```
