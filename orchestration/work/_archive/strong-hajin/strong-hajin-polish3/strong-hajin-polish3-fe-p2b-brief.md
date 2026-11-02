# [frontend] WORK-010 Phase 2b — 진행 상태 셀렉트 · 담당 제안 · 걸린 일 상자 · 푸터·「진행과 판단」 삭제

너는 이 워크트리를 조사하고 Phase 1·2a 를 끝낸 **strong-hajin `frontend` 워커**다. 맥락이 끊겼으면 아래 파일만으로 이어 갈 수 있다. 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` (Phase 1·2a 는 코디가 커밋했다 — `git log` 로 확인)
⚠ Phase 3(셸) 미커밋 변경이 같은 워크트리에 있을 수 있다(`frontend/src-tauri/`·`lib/shell.ts`·`App.tsx` 다운로드 수신부·`labels.ts` `shellDownload`). **그 자리는 건드리지 마라.** `labels.ts` 는 정확한 위치 편집만.

## 1. SSOT
- **SPEC-007 v0.5.1** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` — **§2.10.1(`⋯`) · §2.10.3 걸린 일 · §2.10.5 진행 상태 셀렉트(상태×역할 표) · §2.10.6 담당 셀렉트 · §2.10.9(2b 몫)** · §3 S-10·S-11 · §6 「고도화 3차」 AC. SPEC 이 정본
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` — **Phase 2b(2b-1 ~ 2b-3)** 체크박스 = 계약 (W7 확인 대기 = 글자만 · W8 목록 행 `TaskQuickActions` 그대로 반영됨)
- 2a 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-fe-p2a-report.md`(있으면 — 2a 에서 남긴 것 중 2b 와 닿는 것)
- 너의 조사 `fe-survey-report.md` §4-3(진행과 판단 8구획) · §4-4(푸터 매트릭스) · §4-8(부품) · §5 / 서버 `be-survey-report.md` §4-4(reassign) · §4-5(허용표·사유·활성 담당자만)
- 기준선 `flaky-baseline-evidence.md`

## 2. 이 페이지의 범위 (상세는 WP 2b)
1. **진행 상태 셀렉트** — 옵션은 SPEC §2.10.5 표 그대로(서버 허용표 — 화면이 규칙을 만들지 않는다) · 확인 대기 = 글자만 · 막힘/업무 취소(사유 필수, 취소는 맨 아래 빨강)/완료에서 재개(사유 선택) = **작은 모달**(`ReasonPrompt`/`BlockReasonPrompt` 재사용, 본문 막힘 입력 `isBlocking` 은 모달로) · 요청 업무 완료 = `CompletionReportModal` · 미완 체크리스트 직접 완료 = 기존 확인창 · 서버 거절 = 서버 문장 공통 오류 토스트 + 셀렉트 원래 값 · 상세 `startBlocked` disabled 경로 삭제 · 목록 선례 `TaskStateCell`/`TaskStateValue` 와 부품을 나눠 쓸 수 있으면 나눠 쓴다
2. **`⋯` 메뉴** — 요청 업무의 요청자에게만(지금 「취소 제안」·「조건 변경 제안」 조건) · 항목 둘 → 지금 모달
3. **담당 셀렉트** — `canAssign && !readOnly` 일 때만 · 고르면 사유(선택) 작은 모달 → `/reassign` · 성공 뒤 「{대상}에게 변경 제안 중」 · 대기 제안이 있으면 다시 안 열림 · 「담당자 변경」 단추·겹 `Modal` 정리
4. **걸린 일 상자** — 「진행과 판단」 구역 제목·덩어리 삭제, 구획 1~5·7 은 조건이 참일 때만 메타 정보 바로 아래 상자(안의 단추 조건 그대로)
5. **푸터 전부 삭제** — `Modal` 에 footer 를 넘기지 않는다(빈 줄 없음) · `scax-blocked-note` 는 상세에서만 사라지고 **공용 CSS·목록 행은 그대로**(W8)
6. SPEC §2.10.9 「지우는 것 — 전수」와 1:1 대조표를 보고에 붙인다

**쓰는 곳을 전부 센다** — 푸터 단추 11종의 핸들러·상태 · `isBlocking`·`startBlocked`·`hasProgressBlock`·`openHandover` · `ReasonPrompt`/`BlockReasonPrompt`/`TermsChangePrompt`/`CompletionReportModal` 사용처 · 상태 셀렉트 부품 사용처(목록·프로젝트 우 패널 회귀)를 grep 으로 세고 **바꾼 자리 / 유지한 자리(이유)** 표.

## 2-1. 2a 검수에서 넘어온 것 (`review-fe-p2a-report.md` — 코디 답, 이 페이지에서 함께 고친다)
- **W1** 진행 상태 전이 · 담당 제안 · 체크리스트 명령을 **인라인 저장과 같은 직렬 대기열**에 태운다(SPEC-007 §5 「같은 줄」). 저장 중에 셀렉트를 바꿔도 422 경합이 나지 않게
- **W2** AX 참고 자료 경로가 죽었다(`App.tsx` 리포트가 짚은 줄들 · `ChatDrawer.tsx:13,16,103-105,135-137,341-352`). **지운다** — AX 를 열거나 판단할 때마다 도는 `getMyWork`/`getWorkRequests` 조회와 그 실패 토스트·stale 띠까지. 단 **`App.tsx` 의 다운로드 수신부(`onShellDownload`)는 건드리지 마라**(Phase 3 커밋됨). 지운 자리 표를 보고
- **W3** 업무 내용을 클릭하면 `p`→`textarea` 로 바뀌며 글자가 뛰고 캐럿이 맨 앞으로 간다 — 같은 글자 크기·줄 간격·안 여백으로 맞추고 캐럿을 끝으로(가능하면 누른 자리)
- **W4** 저장 중 표시 — SPEC §2.10.4 의 표시 규칙대로 필드 옆에 작게(없으면 실패 표시 자리와 같은 자리에 「저장 중」). 성공 토스트는 여전히 없음
- **W5** 인라인 저장 성공 시 전역 오류(앞서 뜬 오류 토스트)를 걷는다 — `MyWorkPage`/`TodayPage`/`CalendarPage` 호출부
- W6(내 업무·홈 날짜 저장의 해제 건수 문장)은 그대로

## 3. allowed_paths
- `frontend/src/` (테스트 포함) — 단 `lib/shell.ts` 금지 · `App.tsx` 다운로드 수신부 금지. `frontend/src-tauri/` 금지

## 4. 하지 말 것
- 커밋·push 금지. **서버·프론트를 띄우지 마라. 사용자 포트(8001·5176·54329)를 건드리지 마라**
- 새 모양을 만들지 마라 — DS 부품(`Select`·`ConfirmModal`·`ReasonPrompt`·`Badge`·`Button`)·토큰만. 시안 없는 자리(`⋯` 메뉴·걸린 일 상자 배치)는 기존 부품으로 짜고 DS-gaps 에 적는다
- 서버 코드 수정 금지. 서버 응답이 모자라면 우회 조립하지 말고 코디에게

## 5. 검증
```
frontend 에서 npx vitest run --no-file-parallelism (기준선 5건 분리) · npx tsc --noEmit · make frontend-build. 같은 검증 중복 실행 금지. api.ts 밖 fetch 금지, 기존 부품/viewModels/labels 재사용.
```
- 새/고친 테스트(WP Phase 2b 검증 목록): 상태×역할 옵션(§2.10.5 각 행) · 사유 필수 모달(빈 사유 막음) · 완료 보고 모달 · 남은 단계 확인창 · 409 토스트+원래 값 · `⋯` 요청자만 · 담당 셀렉트 권한·제안 중 · 걸린 일 상자 각 조건 · **푸터 없음** · 「진행과 판단」 없음
- 기존 테스트가 푸터 단추·「진행과 판단」을 단언하면 계약이 바뀐 것 — 「없다」로 뒤집을 수 있으면 뒤집는다
- 회귀: 내 업무 목록 상태 칸·프로젝트 우 패널

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

- **커밋·push·PR 하지 마라.** 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p2b-worker-report.md` 에 파일로도 남긴다.
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-010 Phase 2b" \
  --body "변경 파일 / 계약 체크 결과 / grep 으로 센 자리 표 / §2.10.9 대조표 / 기준선 vs 결과 / DS-gaps / 미결"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] frontend 완료 — WORK-010 Phase 2b. 리포트 fe-p2b-worker-report.md" --enter
```
막히면: `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] frontend: <질문>" --enter`
