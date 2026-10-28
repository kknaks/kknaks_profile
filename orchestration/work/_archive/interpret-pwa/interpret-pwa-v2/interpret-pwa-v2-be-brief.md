# [backend] interpret-pwa WP16 — 사전 .6(새 시술 13 · 언어별 정정) · 통역 기록(D-41)

너는 **interpret-pwa backend 워커**다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/backend/role.md` (+ rules · skills · tools · workflow)
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-v2` (main 2a9d5a5) · 커밋 · push 금지 · 키는 `/Users/kknaks/git/toy_pr2/interpret-pwa/.env` 를 **읽기만**(값 출력 · 복사 금지) — 실물 호출 때 env 로 넘겨라

## SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.6.0** — §4.2.1 ~ §4.2.3(사전) · §5.9(통역 기록) · §9.6(배포 PVC) · §9.1 · §9.3 ⑲ ~ ㉑
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP16 행**(범위 · 완료 조건 · 부분 검증)
- DEC-001 D-39 ~ D-41 · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-dispositions.md`(**OQ-018 처분 포함 — SPEC 에 없는 건 이게 기준**) · 조사 리포트 3개(`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-r*-report.md`)

## 할 일
1. 시드 `back/seed/glossary.json` → version `2026-10-27.6`: §4.2.2 새 term 13(`kr-001` ~ `kr-013`) × 7 언어 · §4.2.3 기존 변경 · OQ-018 처분 ①~⑤ · 보이지 않는 글자 검사(白毒 U+200C) · 시드 검사 · 시험
2. 통역 기록 §5.9: `INTERPRET_RECORD_DIR` · 날짜별 JSONL(세션 시작/발화/끝) · 걸린 term 판정 · 음성 · 토큰 · IP · 계정값 0 · 7일 삭제(기동 때 + 하루 한 번) · 쓰기 실패는 경고만 · **새 경로 · 화면 없음**(test_api_surface 그대로 통과) · 시험(형식 · 삭제 · 실패해도 통역 계속 · 비밀값 0)
3. 실물 §9.3 ⑲ ~ ㉑ — ⑲ 7개 언어 크기 · 거절 0(넘으면 줄이기) · ⑳ 새 시술 정방향(zh-Hant · ja · en) + **대문자 영문 name TTS 를 파일로 저장**(`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/tts-samples/` 에 EXION · DENSITY · EMFACE wav/pcm → 코디가 듣는다) · ㉑ 로컬에서 기록 파일 생김 확인
4. `.env.example` 에 INTERPRET_RECORD_DIR(이름만) · docker-compose 에 로컬 볼륨
5. 검증 ruff · pytest 전체 · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/wp16-be-report.md`

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WP16" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] backend WP16 완료 — <한 줄>" --enter`
