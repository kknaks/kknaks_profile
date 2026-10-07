# [frontend · 셸] WORK-011 Phase SHELL — 데스크톱 앱(medi-ax) 카톡 수집기

사용자 본인이 자기 Mac 에서 자기 카카오톡을 메시지함으로 보려는 작업이다. 사용자가 직접 지시했다.

## 읽을 것
- WORK-011 「Phase SHELL」: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md`
- SPEC-006 v0.6.0 · SPEC-009 v0.5.1 (같은 폴더의 `../20-spec/`)
- 서버 쪽 실제 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/be3-report.md` (카톡 수신 · 기기 토큰)
- **기존 코드를 가져다 쓴다**: 사용자의 mykakao 레포 `/Users/kknaks/git/toy_pr2/mykakao` (이 Mac 에서 이미 동작한 사용자 본인 코드) — 카톡 로컬 데이터를 읽는 부분은 이 코드를 그대로 옮겨(Rust 로) 쓴다. 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/`

## 범위
`frontend/src-tauri/` + `frontend/src/lib/shell.ts` 수신부만. WORK-011 Phase SHELL 항목 전부(SPEC-006 개정 · 메뉴 막대 상주 · 닫기 = 웹뷰 파괴 · 카톡 커맨드 · 수집기 · 기기 토큰 키체인 · medi-ax 판에만).
같은 워크트리에서 다른 워커는 지금 없다. 커밋·push 금지.

## 검증
코드 레포 AGENTS.md 의 셸 검증(cargo check · cargo test · clippy · shell-verify-strict SHELL_FLAVOR=medi-ax). 이 Mac 에서 수집기를 한 번 돌려 로컬 API(`http://127.0.0.1:8001`, 데모 사용자 jiho)로 방 목록·메시지가 올라가는지 확인하고 숫자로 보고. 막히면 바로 코디에게 물어라.

## 완료 보고
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_d1bc29d4-64a6-44b7-8c97-73728de8f837 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: SHELL 카톡 수집기" --body "변경 파일 / 요약 / 검증 수치 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] SHELL 카톡 수집기 완료 — 한 줄 요약. 상세는 인박스." --enter
```
