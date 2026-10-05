# [frontend] WORK-010 Phase 1 — 로그인 문구 · 회의 「내보내기」 단추 · 회의 제목 인라인

너는 앞서 이 워크트리를 조사한 **strong-hajin `frontend` 워커**다(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-survey-report.md`). 맥락이 끊겼으면 아래 파일만으로 이어 갈 수 있다. 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` (base `origin/main` `d1b5137`)
⚠ **다른 frontend 워커가 같은 워크트리에서 Phase 3(데스크톱 셸)을 동시에 한다** — 그쪽은 `frontend/src-tauri/`·`frontend/src/lib/shell.ts`·`frontend/src/App.tsx` 를 만진다. **너는 그 세 곳을 건드리지 마라.** 필요하면 코디에게 묻는다.

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` — **Phase 1(1-1 · 1-2 · 1-3)** 과 원칙 P-1~P-5. 체크박스 하나하나가 계약이다. 이 세 항목은 SPEC 이 없어 **WP 가 계약**이다
- 너의 조사 `fe-survey-report.md` §1 · §2-1·2-2 · §3 (줄 번호는 `d1b5137` 기준 — 심볼로 다시 찾아라) · 서버 사실 `be-survey-report.md` §3(회의 제목 API·권한)
- 기준선 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/flaky-baseline-evidence.md` — FE 기존 실패 5건(이 밖의 실패만 네 변경 탓)

## 2. 무엇을 하나 (요약 — 상세는 WP)
1. **R1** 로그인 h1 = 「메디솔브 AX 프로젝트」, 설명 `p` 삭제
2. **R2a** 회의 상세 「내보내기」 단추를 옆 단추와 같은 sm 크기로(동작 불변)
3. **R3** 회의 상세 제목을 `InlineText` 로 인라인 수정(`can_edit_info` 일 때만, Enter·blur 저장 · Esc 취소 · 빈 값/안 바뀜 무시 · 실패 시 원래 값 + 오류 토스트) · 제목 없을 때만 「제목 후보: … [적용]」 · 저장 뒤 상위·목록·캘린더 레일 갱신

**쓰는 곳을 전부 센다** — 「제목 없는 회의」 대체 5곳, `updateMeetingInfo` 사용처, `<a>`+`scax-button` 3곳을 grep 으로 다시 세고 바꾼 자리/유지한 자리 표를 보고에 낸다.

## 3. allowed_paths
- `frontend/src/` (테스트 포함) — 단 `lib/shell.ts`·`App.tsx` 제외. `frontend/src-tauri/` 금지

## 4. 하지 말 것
- 커밋·push 금지. **서버·프론트를 띄우지 마라. 사용자 포트(8001·5176·54329)를 건드리지 마라**
- 새 모양을 만들지 마라 — DS 부품(`InlineText`·`Button`·`Toast`)·토큰만, 시안 없는 자리는 DS-gaps 로 보고
- 서버 코드 수정 금지(필요하면 코디에게)

## 5. 검증
```
frontend 에서 npx vitest run --no-file-parallelism (기준선 5건 분리) · npx tsc --noEmit · make frontend-build. 같은 검증 중복 실행 금지. api.ts 밖 fetch 금지, 기존 부품/viewModels/labels 재사용.
```
- 새 테스트: 로그인 문구 · 내보내기 단추 sm 클래스 · 제목 인라인(저장·Esc·빈 값·안 바뀜·권한 없음·실패 원복) · 후보 [적용](권한 있음/없음 · 제목 있으면 안 보임)

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p1-worker-report.md` 에 **파일로도** 남긴다(터미널이 죽어도 이어지게).
```bash
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-010 Phase 1" \
  --body "변경 파일 / 계약 체크 결과 / grep 으로 센 자리 표 / 기준선 vs 결과 / DS-gaps / 미결"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] frontend 완료 — WORK-010 Phase 1. 리포트 fe-p1-worker-report.md" --enter
```
막히면: `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] frontend: <질문>" --enter`
