# [writer] WORK-011 초안 — 외부 채널 연동 · 메시지함 · 프로필 · Mac 카톡 수집 (2026-10-06)

SPEC 3차 검수가 도는 동안 **WORK-011 초안**을 쓴다. 검수가 고칠 거리를 내면 그만큼 뒤에 고친다.

## 근거
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` v0.4.0 · `spec-009-mac-kakao-collector.md` v0.4.0 · `spec-006-tauri-wrapper.md` v0.5.0
- 형식 본보기 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md`(Meta · 원칙 · Work Summary · Code Surface · Phase 별(무엇이 끝나야 시작하나 · 파일 겹침 · 완료 조건 · 시험) · Pre-deploy Check · 반영 · Rollback · Done Criteria · Open Issues) · `work-006-tauri-wrapper.md`(셸 작업 선례)
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 · 운영 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/70-runbook/runbook-002-production-deploy.md`
- 코드(읽기만) `/Users/kknaks/git/toy_pr2/Strong_hajin` origin/main

## 쓸 것
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md` (새로) + `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/README.md` 한 줄
- **Phase 를 워커별·파일 겹침 기준으로 쪼갠다.** 워커: backend · frontend · 데스크톱 셸/Rust(선례대로 어느 워커가 `frontend/src-tauri/` 를 맡는지 work-006/010 을 따라라) · infra(`k8s_infra_mac` 차트: 연동 워커 Deployment replicas 1 · hostPath 마운트(카톡 첨부·프로필 이미지) · Secret 키 · Pub/Sub SA 키 파일 마운트 · ingress body size)
- 권장 순서(SPEC 계약 근거로 조정 가능): ① BE 기반(스키마·연동/기기 토큰/고른 방/메시지/첨부/읽음 저장 · 소유 검사) → ② BE 슬랙(Socket Mode 워커·백필·메우기·사람별 팬아웃) / BE Gmail(watch+pull·history·백필) / BE 카톡 업로드 수신 — 병행 가능 여부를 파일로 판단 → ③ BE 메시지함 API·WS·첨부 중계·이미지 프록시·답장(슬랙·메일)·프로필/비밀번호 → FE 는 계약 고정 뒤 병행(메시지함 2/3열·답장·설정 세 연동·프로필 · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` + design-change-1~6) → ④ 셸/Rust(SPEC-006 개정 · 상주·숨기기·메뉴 막대 · 카톡 커맨드 · 수집기 · 기기 토큰 키체인) → ⑤ infra → ⑥ 코디 로컬 실물 확인 → 운영 반영
- 각 Phase **완료 조건 = 실물 확인 항목**(외부 서비스는 실제 호출 1회: Gmail 연결·수신·답장 · 슬랙 연결·수신·스레드·답장·파일 · 카톡 수집·첨부)
- **카톡 DB 를 여는 모듈**은 SPEC-009 처럼 「구현 몫 — mykakao DEC-001·SPEC-001·`~/git/toy_pr2/mykakao` 를 Rust 로 옮김」 참조만. 이 부분은 **워커가 안전 장치에 막힐 위험**을 Open Issues 에 적고, 막히면 코디에게 바로 묻게 한다
- 로컬 비밀값은 `~/.config/google/env` · `~/.config/slack/env` (Makefile 로드 추가가 BE 작업에 포함) · 운영은 Secret
- 사용자 E2E 체크리스트 자리(`reference/2026-10-06-strong-hajin-inbox/`)를 Done Criteria 에

## 하지 말 것
SPEC 고치지 마라(어긋나면 Open Issues) · 코드 레포 쓰기 금지 · 커밋 금지. 끝나면 §9 로 보고.
