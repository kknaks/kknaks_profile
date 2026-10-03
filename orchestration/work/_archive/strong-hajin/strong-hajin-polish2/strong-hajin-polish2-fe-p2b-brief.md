# [frontend] WORK-009 Phase 2b — 업무 상세 날짜 넷 · 메타 간격 · 「마감일」 이름·형식 통일

너는 앞서 이 워크트리를 조사한 **strong-hajin `frontend` 워커**다(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md`). 맥락이 끊겼으면 아래 파일만으로 이어 갈 수 있다. 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (base `origin/main` `3d47a32`)
⚠ **backend 워커가 같은 워크트리 `backend/` 에서 Phase 1 을 동시에 한다.** 너는 `frontend/` 만. 서버 변경은 필요 없다(`started_at`·`completed_at` 은 업무 응답에 이미 있다 — be-survey §3-4).

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` — **Phase 2b(2b-1 · 2b-2)** 와 원칙. 체크박스 하나하나가 계약이다. 2b-1 의 DOM 트리는 지금 코드를 1:1 로 옮긴 것이다
- SPEC(정본 — WP 와 다르면 SPEC 이 맞다): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`
  - SPEC-007 v0.4.0 §2.2 「날짜 넷」·「출처 줄」 · §3 S-1 · §6
  - SPEC-001 v0.5.0 U-17 · §6 · OQ-Q(코디 닫음 — WP 2b-2 에 답이 있다)
  - SPEC-003 v0.4.0 Data Contract 「업무 날짜」
- 너의 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §4 · §5 (줄 번호는 `3d47a32` 기준 — 심볼로 다시 찾아라)

## 2. 무엇을 하나 (요약 — 상세는 WP)
1. **상세 사실 줄 날짜 넷** — 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일 순, 값 없는 칸은 서지 않음, 시각은 Asia/Seoul 날짜로(UTC 자름 금지). 편집 DateField 라벨 「시작 예정일」·「마감일」
2. **메타 간격** — 사실 줄과 출처 줄 사이 DS 간격 토큰, 글자 계층 맞춤, 링크 문구 그대로
3. **「마감일」·`2026/10/06` 통일** — `due_date` 를 보이는 라벨 전부(「기한 지남」 칩·「기한 초과」 배지 포함), 업무 날짜 표시 형식 전부, DateField 입력 표기, 캘린더 거절 문구 날짜. **유지**: 만들기 창·캘린더 「시작일」 라벨, 캘린더 날 머리, 축 눈금, 업무 날짜가 아닌 표시(회의 시각 등). 포맷터를 하나로 모은다

**쓰는 곳을 전부 센다** — 라벨 키·하드코딩 문자열·포맷터 호출·날짜 표시 자리를 grep 으로 전부 세고 **바꾼 자리 / 유지한 자리(이유)** 표를 보고에 낸다. 판단이 갈리는 자리는 표에 적는다.

## 3. allowed_paths
- `frontend/src/` (테스트 포함). `frontend/src-tauri/` 금지

## 4. 하지 말 것
- 커밋·push 금지. **서버·프론트를 띄우지 마라. 사용자 포트(8001·5176·54329)를 건드리지 마라**
- 새 모양을 만들지 마라 — DS 부품·토큰만, 시안 없는 자리는 DS-gaps 로 보고

## 5. 검증
```
make frontend-test (직렬: frontend 에서 npx vitest run --no-file-parallelism) · frontend 에서 npx tsc --noEmit · make frontend-build. 같은 검증 중복 실행 금지. envelope 으로 권한 판단, api.ts 밖 fetch 금지, 기존 부품/viewModels 재사용.
```
- **기준선 먼저**(고치기 전 테스트 실패 목록 — 날짜 의존 5건이 기준선이다: CreateWork 시작일 4 · CreateWorkLayout 1)
- 새 테스트: 상세 날짜 넷(시작 전·진행 중·완료 각각 보이는 칸) · KST 경계(UTC 15:00 이후 시각이 다음 날로) · 포맷터 · 「마감일」 라벨 주요 자리

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_82fc2322-7b14-4d60-90ee-efe1c243fd31 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-009 Phase 2b" \
  --body "변경 파일 / 바꾼 자리·유지한 자리 표 / 포맷터 정리 / 기준선 vs 결과 / DS-gaps / 미결"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] frontend 완료 — WORK-009 Phase 2b. 상세는 인박스." --enter
```
막히면: `orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --text "[질문] frontend: <질문>" --enter`
