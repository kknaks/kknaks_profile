# [backend] WORK-008 Phase 6 핫픽스 — 대화·회의 배치가 세션을 잃으면 새로 이어 간다 (B-04)

너는 Phase 4·5 를 한 **strong-hajin `backend` 워커**다. 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` — **지금 detached HEAD(`3d47a32` = main)**. 먼저 `git switch -c kknaksss/strong-hajin-hotfix-session origin/main` 으로 브랜치를 만들고 작업한다(커밋은 코디). 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.

## 운영 증거 (2026-10-02, 배포 직후)
`worker-conversation` 로그: `Codex CLI conversation 이(가) 종료 코드 1 로 실패했습니다: Error: thread/resume: thread/resume failed: no rollout found for thread id 01a0f4c0-… (code -32600)` 반복. 화면: 「Codex CLI session to resume is not available here」 → 다시 시도도 실패. 배포 전에 시작한 대화의 세션이 옛 파드 로컬과 함께 사라졌다.

## 계약 (WP `…/30-work/work-008-polish.md` Phase 6)
1. 대화 turn 이 resume 불가(세션 없음 — Phase 4 의 판정 재사용, `no rollout found` 포함)면 그 대화의 provider 세션을 버리고(`reset_provider_session` 등 기존 경로) **최근 대화 기록을 담아 새 세션으로** 같은 turn 안에서 이어 간다. 사용자는 실패를 보지 않는다
2. 회의 배치(웜스타트 세션 resume)도 같은 대비
3. resume 를 쓰는 곳 전수(네 Phase 4 보고의 ①~④)가 이제 모두 대비를 갖는지 표로
4. 일반 실패(세션 있음)는 지금처럼 실패 — 대비가 진짜 오류를 삼키지 않게

## 하지 말 것 / 검증
- 운영 접근·커밋·서버 기동·로컬 codex 금지. `backend/` 만
- 테스트: 세션 없는 대화 turn 성공(새 세션·기록 포함) · 회의 배치 성공 · 세션 있음 일반 실패는 실패 · `make test-unit` · `make test-contract`

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WORK-008 Phase 6 핫픽스" --body "변경 파일:줄 / resume 전수 대비표 / 테스트 결과"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] backend 완료 — Phase 6 핫픽스. 상세는 인박스." --enter
```
