# WORK-012 Phase 3 (frontend) — 완료 보고

브랜치 `kknaksss/docs-v1` · 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1` · **커밋·push 하지 않음**(be+fe 한 커밋은 코디가 낸다)

## 변경 파일 (전부 `app/front/src/features/meetings/`)

소스 11
- `components/MeetingStatusBar.tsx` — `generating` 단계 문구 둘 · `failed` 「다시 시도」 + 사유 툴팁 · `headline` 카운트 다섯
- `hooks/useMeetingFinalizeJob.ts` — 상한 1230 · `retry()`(`/finalize`) · `errorCode` 보존 · 종결 시 트랜스크립트 무효화
- `api.ts` — `integrateMeeting` → **`finalizeMeeting`**(`POST …/finalize`)
- `types.ts` — `MergedSummary` 다섯(`integratedAt` 삭제) · `JobPhase` `transcription|final` · `JobErrorCode` 5종 ·
  `MeetingLine.pendingChange` → **`payload`** · `sourceHumanLineId`·`sourceAiLineId` **삭제**(0008 이 컬럼을 지웠다) · `LinePayload`
- `components/MeetingDetailBody.tsx` — 생성중 캡션 · AI 안내 바 · AI 탭 dot · 「다시 시도」 배선 · 스크립트 `follow={false}`
- `components/TranscriptPanel.tsx` — `follow` prop(종료 후 자동 따라가기 없음) · `data-transcript-scroller`
- `errors.ts` — `INTEGRATE_FAILED_MESSAGE` → `FINALIZE_FAILED_MESSAGE`(「다시 시도를 시작하지 못했습니다」)
- `closeFixtures.ts` · `closeState.ts` · `components/LineTaskButton.tsx` · `components/LinkTaskDrawer.tsx` ·
  `components/MeetingPreviewPanel.tsx` · `hooks/useMeetingEdit.tsx` · `hooks/useMeetingTaskLink.tsx` — `payload` 이름 · 어휘

테스트 9 — `MeetingStatusBar.test`(+4) · `MeetingClosedPage.test`(+1 · 전면 갱신) · `TranscriptPanel.test`(+2) ·
`static.test`(㉒ 신설 4 · ⑲ 수치 갱신) · `MeetingDetailDrawer.test` · `MeetingPreviewPanel.test` · `MeetingEditMode.test` ·
`MeetingTaskLink.test` · `AgendaLineTree.test` · `MeetingLiveView.test` · `useMeetingStream.test` · `aiBatch.test`

`src-tauri/tauri.conf.json` 은 **내가 만진 게 아니다** — 디스패치 전부터 modified 였다.

## 구현 요약

- **단계 문구 둘** — `generatingLabel(phase, attempt)` 하나가 정한다. `phase !== "final"` 이면 「녹음을 다시 받아쓰고 있습니다」
  (첫 폴링 전 `null` 도 ① 문구), `final` 이면 「회의록을 정리하고 있습니다」 + `attempt>1` 일 때 「· 다시 시도 중 (n−1/2)」.
  **처리 시간을 적지 않는다**(MF-37).
- **실패 배너 하나** — 문구는 「회의록 생성 실패 · 회의록 탭에 회의 중 작성한 원본을 보여 드립니다」 하나이고 **사유는 툴팁으로만**
  갈린다(`transcription_*` → 「녹음을 다시 받아쓰지 못했습니다」 · `final_*`·`job_timeout` → 「회의록을 정리하지 못했습니다」).
  버튼은 「다시 시도」이고 툴팁은 「녹음을 다시 받아쓰고 회의록을 다시 정리합니다 · 원본은 바뀌지 않습니다」.
  **`errorCode` 의 출처** — `MeetingDetail` 에 실패 사유가 없고 종결과 동시에 `activeJobId` 가 `null` 이 되므로,
  폴링 훅이 **마지막으로 종결된 job** 의 `errorCode` 를 들고 있다가 배너에 준다. 새로고침으로 들어오면 볼 job 이 없어
  `null` 이고 배너는 사유 툴팁 없이 뜬다(§ 미결 참조).
- **카운트 다섯** — `mergedSummary` 를 그대로 그린다(화면이 세지 않는다). 드로어(`stacked`)도 같은 값 다섯을 두 줄로.
- **폴링** — `JOB_POLL_MAX_COUNT` 480 → **1230**. 종결에서 상세 + 목록 + **트랜스크립트**를 무효화한다(①이 블록을 갈아끼운다 — M-9-a).
  상한·조회 실패는 「상태를 확인하지 못했습니다 · 다시 확인」만 남기고 **실패로 꾸미지 않는다**(기존 규칙 유지).
- **AI 탭 안내 바** — 「배치 n회 반영」(배치 0 이면 「AI 요약 없음」). 「종결 · HH:MM」·「종결 정리 중」·「종결 정리 실패」 **전부 폐기**.
  AI 탭 dot 은 언제나 `#B3B3B3` — 종료 후 배치가 다시 돌지 않는다(MF-56).
- **스크립트 푸터** — 「전체 스크립트 n분 · 화자 n명」은 이미 있었고(`ceil(마지막 endMs / 60000)`), **자동 따라가기만** 껐다
  (`follow={false}`) — 종료 후 열자마자 끝으로 튀지 않는다.
- **`pendingChange` → `payload`** — 타입 · 요청 본문 키 · 함수 이름(`payloadSummary`)까지 기계적 rename. 동작은 그대로다
  (편집 모드 · 드로어 · 줄 버튼의 **모양과 흐름을 바꾸지 않았다** — WORK-013 몫).

## 검증

- `npx tsc --noEmit` → **Errors 0**
- `npx vitest run` → **35 files / 327 tests 전부 통과**(0 실패)
- `npx next lint` → **Error 0**
- 새 단언 요지
  - 「회의 종료」 → 「녹음을 다시 받아쓰고 있습니다」 → (`phase:"final"`, `attempt:2`) 「회의록을 정리하고 있습니다 · 다시 시도 중 (1/2)」
    순서 · `attempt` 3 이면 (2/2) · 첫 폴링 전(`phase:null`)도 ① 문구 · 문구에 「분/초/예상」 0
  - 폴링 2초 간격 · 종결 뒤 상세 GET 한 번 + **트랜스크립트 한 번** · 이후 폴링 0 · 5xx 면 스피너 유지 + 「다시 확인」(재요청 0)
  - `ended+failed` 에서만 「다시 시도」 → **`POST …/finalize`** 호출(MSW) → ①부터(문구가 재전사로 복귀) ·
    성공한 회의록에는 버튼 0 · 409 → 토스트 + 상세 재조회 · 옛 `/integrate` 핸들러는 **불리지 않는다**
  - 사유 툴팁 5종 매핑 전부 · `errorCode` 가 `null` 이면 툴팁 없음
  - 한 줄 요약 카운트가 **회의록 탭에 그려진 수와 정확히 같다**(안건 4 · 논의 2 · 결정 1 · 액션 1 · 업무 1 — DOM 에서 세어 비교) ·
    드로어도 같은 다섯
  - AI 안내 바에 「종결」 0 · 생성중 캡션 「정리가 끝나면 이 탭이 최종 회의록으로 바뀝니다」
  - `follow={false}` 면 새 블록에도 스크롤이 0 에 머문다(회의 중 기본값은 바닥으로 따라간다 — 둘 다 단언)
- 정적 검사(`static.test.ts` ㉒ 신설 4 · ⑲ 갱신)
  - 화면 문구에 「종결」·「다시 생성」 0(주석 제외) · `pendingChange`·`integratedAt`·`final_batch`·`"integration"` 0
  - `/integrate` 를 부르는 코드 0 · `finalizeMeeting(` 호출자는 `api.ts` + 폴링 훅 **둘뿐**
  - 단계 문구·실패 배너 문구의 소유자가 `MeetingStatusBar.tsx` **하나**(두 번째 상단 바 0)
  - `JOB_POLL_MAX_COUNT = 1230` · 훅에 `setInterval`·`setTimeout`·자동 재시도 0

## 계약 준수

- 상단 바는 `MeetingStatusBar` 한 파일 · 본문은 `MeetingDetailBody` 하나(카운트는 StatusBar 가 그린다)
- 편집 모드 · payload 드로어 · 줄 버튼 · 칩의 **동작을 바꾸지 않았다**(rename 뿐) · breadcrumb · 헤더 순서 · 미리보기 패널 손대지 않음
- `fetch` 직접 호출 · Sheet/Dialog 직접 import · hex 리터럴 · `retry:true` 0
- `app/back/` · 문서 · compose 0 파일

## 미결 · 주의점

- **앱 창 실측 미완 · tauri dev 흰 화면**(WORK-011 때와 같은 증상 · 내 변경과 무관). `next dev` 는 `/`·`/tasks/` 모두 200 인데
  웹뷰만 빈 화면으로 남는다. 캡처 `w012-01-app.png`(같은 폴더). 띄웠던 dev 프로세스는 모두 정리했다.
  두 단계 문구 → 최종 회의록 → 카운트 다섯의 실측은 **Soniox 오디오 + 워커로 실제 회의를 끝내야** 만들 수 있어 무인으로는 못 만든다.
- **실패 사유 툴팁의 계약 공백** — `MeetingDetail` 에 `errorCode` 가 없어, 새로고침으로 실패 화면에 들어오면 사유 툴팁이 없다
  (배너·「다시 시도」는 정상). 사유를 항상 보여야 한다면 상세 응답에 필드가 필요하다.
- **AI 안내 바의 `HH:MM` 이 빠졌다** — 시안 문구는 「배치 n회 반영 · HH:MM」인데 그 시각은 **회의 중 화면이 세던 값**이라
  상세 응답에 없다(`integratedAt` 은 MF-56 으로 사라졌다). `updatedAt` 같은 다른 시각을 끌어다 쓰지 않고 시각 없이 그린다.
  필드를 더할지는 문서가 정할 몫이다.
- **`finalBatchState` 는 응답에 남아 있다**(SPEC-008 §4 Data Contract 은 「없다」고 적었는데 `schemas/meeting.py` 가 아직 보낸다).
  프론트는 이제 **쓰지 않는다** — 타입에만 남겨 뒀다. 백엔드가 빼면 타입에서 지우면 된다.
- 백·프론트 **같이 배포**해야 한다 — `/integrate` 경로가 사라지고 `payload`·`mergedSummary` 모양이 바뀐다.
