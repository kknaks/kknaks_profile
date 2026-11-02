# [frontend] 회의 빠른 시작 중복 생성 방지

너는 sc-ax frontend 워커다. 역할 문서를 먼저 읽어라:
- /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md (+ rules.md·skills.md·tools.md·workflow.md)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`
브랜치 `kknaksss/sc-meeting-room`, 확인한 HEAD `75360fe`, base `origin/main`.
사용자는 이번 대화에서 아래 시안 수정안을 검토하고 프론트 구현 발주를 명시 승인했다. 커밋·push·PR 금지.
기존 DS sync 작업의 미커밋 변경(.design-sync/, frontend/ds-entry.tsx)을 보존한다. 이 파일들은 이번 수정 대상에서 제외한다. 새 워크트리·하위 워커를 만들지 않는다.

## 1. 승인된 버그 수정

사용자 보고: 회의 시작 클릭 한 번에 POST /api/meetings/quick-start가 1ms 간격 두 번, 둘 다 201, 회의 2건 생성. 사용자 원인 분석: MeetingListPage.tsx quickStart의 setBusy 함수형 업데이터 안에서 void async로 API 호출. 개발 StrictMode의 업데이터 재호출로 두 요청 발생. current 가드는 막지 못함.
이번은 이 버그와 같은 부수효과 패턴만 수정. 앞선 회의 중 작업은 완료된 상태이며 종료 후 화면 변경은 여전히 미발주.

## 2. 현재 상태

사용자가 backend를 방금 수정하고 재기동했다고 명시. backend/는 읽기 전용이며 한 줄도 수정 금지. 사용자 기존 프론트 변경도 보존. quick-start/예약 외 무관한 변경 금지.

## 3. 수정 계약

- 네트워크/외부 부수효과를 setState 함수형 업데이터 밖으로 이동. 업데이터는 순수하게 유지.
- useRef 같은 즉시 반영 잠금으로 중복 진입 차단: if inFlight.current return; 잠금 true; setBusy(true); try 실제 호출/성공 이동; catch 기존 onError; finally 잠금 false 및 busy false.
- 실패 후 재시도 가능, 성공 시 onOpenMeeting 한 번. StrictMode를 끄거나 백엔드로 문제를 떠넘기지 않는다.
- busy state만으로 연타 차단하지 않는다. 기존 idempotency/API 계층/권한 판단 유지.

## 4. 점검 범위

MeetingListPage.tsx quickStart, bookMeeting/BookingModal의 회의 생성 경로, frontend/src 내 set* 함수형 업데이터 안 await·void async·네트워크 호출·기타 외부 부수효과 패턴을 전수 검색한다. 같은 원인이 있으면 해당 경로를 최소 수정, 없으면 조사 근거 보고. 단순 텍스트 검색으로 없는 것으로 단정하지 말고 호출 경로를 확인한다.

## 5. allowed_paths

frontend/src의 관련 구현·테스트만. backend/, docs/, .design-sync/, frontend/ds-entry.tsx 및 타 작업 변경 금지. 시작 시 diff/status로 현재 변경 보존. 커밋·push·PR·DB reset 금지.

## 6. 검증

StrictMode로 렌더한 회귀 테스트: 클릭 한 번 API 호출 1회, 응답 대기 중 빠른 연타에도 1회, 실패 후 잠금 해제/재시도. 예약 생성도 해당 패턴이면 회귀 테스트. 실제 기능으로 검증하고 없음 단언으로 회피 금지.
cd frontend && npx tsc --noEmit
cd frontend && npx vitest run
직전 보고 직렬 543 통과. 병렬 간헐 실패가 있으면 정확한 실패/직렬 결과를 구분한다.
사용자는 DevTools Network에서 클릭당 POST 1회를 확인하길 요청했다. 현재 실제 회의/데이터를 임의 생성하는 검증은 피하고, 격리된 브라우저 API mock 등 가능하면 비파괴 검증. 실제 Network 검증을 하지 못하면 완료 보고에 명확히 남겨 사용자가 확인할 수 있게 한다. 실제 생성 검증을 했다고 허위 보고 금지.

## 7. 결과 보고

수정 원인·파일·같은 패턴 조사 결과·quick-start/예약 각각 영향·테스트 명령/수치·실제 브라우저 Network 확인 여부를 보고. 결과 파일 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/frontend-duplicate-start-result.md만 별도 쓰기 허용. 종료 후 UI 작업을 섞지 않는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_fa9914b3-124d-43d2-81ec-10417df53069 --from term_08a8813a-da42-428b-9fff-52586fe9614f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fa9914b3-124d-43d2-81ec-10417df53069 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fa9914b3-124d-43d2-81ec-10417df53069 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
