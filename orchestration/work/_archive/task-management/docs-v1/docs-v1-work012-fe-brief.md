# [frontend] WORK-012 Phase 3 — 생성중 phase 둘 · 실패 「다시 시도」 · 카운트 다섯 · 폴링 1230

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-012 백엔드(Phase 0~2)가 방금 들어왔다** — 아직 커밋 전이다(`git status` · `git diff HEAD -- app/back`). be+fe 를 한 커밋으로 낸다. 응답이 바뀐 것: `payload` 키(옛 `pendingChange`) · `mergedSummary` 다섯(`integratedAt` 없음) · `GET /api/jobs` 의 `progress.phase ∈ {transcription, final}` · `errorCode` 5종 · `POST …/finalize`(옛 `/integrate`).

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-012-meeting-close.md            ← 네 빌드 계획. **Phase 3 만.** Code Surface 프론트 행 · Internal Interface(프론트 폴링 · mergedSummary) · Phase 3 검증
  20-spec/spec-008-meeting-close.md            ← **U-1**(생성중 — 단계 문구 둘 · 편집 잠금 · 폴링 실패 「다시 확인」 · 상한) · **U-2**(실패 배너 · 「다시 시도」 · 툴팁 사유) · **U-3**(상단 바 = AI 한 줄 요약 · 카운트 다섯 · 스크립트 푸터) · U-4(드로어의 두 줄 바) · §4 Case Matrix(job 실패 5종 · 폴링 실패) · §4 「수치」(2초 · 1230회) · §6 AC
  40-architecture/frontend/README.md           ← §3-3 무효화(job 종결) · §3-5 code 분기 · §8 종료 · 실패 표시
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §3-1 · §3-2   ← MF-25 · 37 · 56 · 58
```

**시각 정본** — 회색 상태 바는 `회의록.dc.html` L586~592 규격(SPEC-007 U-1) · 한 줄 요약 바는 `디자인 시스템.dc.html` [09] L727~733. **새 시안 없음** — 지금 `MeetingStatusBar` 의 세 변형(`generating` · `failed` · `headline`)이 그 규격이다. 문구·값만 바꾼다.

## 1. 범위 — Phase 3

```
MeetingStatusBar.tsx     generating 에 phase 둘 — 「녹음을 다시 받아쓰고 있습니다」(transcription) / 「회의록을 정리하고 있습니다」(final) · 재시도 중이면 「· 다시 시도 중 (n/2)」
                         failed 버튼 「다시 시도」(옛 「다시 생성」 폐기) · 툴팁 사유 둘(transcription_* / final_*)
                         headline 카운트 다섯 「안건 n · 논의 n · 결정 n · 액션 n · 업무 n」 · 드로어(stacked) 도 다섯
useMeetingFinalizeJob.ts JOB_POLL_MAX_COUNT 480 → 1230 · progress.phase 노출 · 상한·조회 실패에서 멈추고 「다시 확인」만
api.ts · types.ts        POST …/finalize · MergedSummary 다섯 · JobProgress.phase 두 값 · errorCode 5종 · pendingChange → payload
MeetingClosedPage.tsx    생성중 두 단계 · 실패 배너 · AI 탭 안내 바는 회의 중 값 그대로(「종결」 문구 0)
TranscriptPanel.tsx      종료 후 푸터 「전체 스크립트 n분 · 화자 n명」(n분 = 마지막 endMs ÷ 60000 올림) · 자동 따라가기 없음
closeFixtures.ts · 테스트
```

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
MeetingStatusBar 하나    상단 바 세 변형이 한 파일. 두 번째 바(HeadlineBar · GeneratingBar 등) 금지
MeetingDetailBody 하나   페이지·드로어가 같은 본문. 건드리지 않는다(카운트는 StatusBar 가 그린다)
편집 모드 · payload 드로어 · 줄 버튼 · 칩   WORK-013. 건드리지 마라
breadcrumb · 헤더 순서 · 미리보기 패널   WORK-014
「종결 · HH:MM」 · 「종결 정리 중」 · 「다시 생성」   옛 어휘. 0건이어야 한다
fetch 직접 · Sheet/Dialog 직접 import · hex 리터럴 · retry:true   금지
```

## 3. 계약

- 상단 바 `generating` — `progress.phase` 로 문구 둘. `attempt>1` 이면 「· 다시 시도 중 (n/2)」(n = attempt−1)
- `failed` 배너 — 「회의록 생성 실패 · 회의록 탭에 회의 중 작성한 원본을 보여 드립니다」 + 「다시 시도」 → `POST …/finalize` → `202 {jobId}` → 폴링 재개(①부터 — 문구가 transcription 으로 돌아간다). 툴팁: `transcription_*` → 「녹음을 다시 받아쓰지 못했습니다」 / `final_*`·`job_timeout` → 「회의록을 정리하지 못했습니다」. **`ended+succeeded` 에는 버튼 없음**
- `headline` 바 — `mergedSummary` 다섯 그대로 그린다(화면이 세지 않는다). `headline` null 이면 바 없음
- 폴링 — 2초 · 1230회 · 종결(`succeeded|failed`)에서 멈춤 · 조회 실패·상한은 「상태를 확인하지 못했습니다 · 다시 확인」 — 실패로 꾸미지 않는다 · job 종결 시 `['meetings','detail',id]` + `['meetings','list',…]` + 트랜스크립트 무효화
- 스크립트 푸터 — 「전체 스크립트 n분 · 화자 n명」

## 4. allowed_paths

```
app/front/
```

## 5. 검증

WP §Execution Phase 3 검증 체크리스트 전부. 특히 — 문구 순서(transcription → final) · 재시도 문구 · 실패 상태에서만 「다시 시도」 · `POST /finalize` 호출(MSW) · 카운트 다섯 = 트리 수 · 폴링 상수 1230 · 정적 `종결|다시 생성|pendingChange|integratedAt|/integrate` 0(grep)

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -8   # Errors 줄 0
```

**앱 창 실측** — 가능하면 `tauri dev` 로 회의 하나를 끝내 두 단계 문구 → 최종 회의록 → 카운트 다섯을 보고 캡처 경로를 보고에. 못 띄우면 그 사실만 적어라.

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WORK-012 Phase 3" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(tsc · vitest · 정적 · 앱 창) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — WORK-012 회의 종료 프론트. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
