# [frontend] 후속 — 회의 중 화면 5항목만 수정

너는 sc-ax frontend 워커다. 역할 문서를 먼저 읽어라:
- /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md (+ rules.md·skills.md·tools.md·workflow.md)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`
브랜치 `kknaksss/sc-meeting-room`, 확인한 HEAD `75360fe`, base `origin/main`.
사용자는 이번 대화에서 아래 시안 수정안을 검토하고 프론트 구현 발주를 명시 승인했다. 커밋·push·PR 금지.
기존 DS sync 작업의 미커밋 변경(.design-sync/, frontend/ds-entry.tsx)을 보존한다. 이 파일들은 이번 수정 대상에서 제외한다. 새 워크트리·하위 워커를 만들지 않는다.

## 1. SSOT — 먼저 읽을 것

이번 최신 사용자 지시: **회의 중 화면만 먼저 발주**. 이전 A~F 구현 위에서 이어 작업한다. 종료 후 변경은 이번 범위가 아니다.
- SPEC: /Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec/products/sc-ax/20-spec/spec-004-meeting-note.md §6 메모, §7 AI 중간 요약, §7.3 트랙 경계, §3.3 권한.
- 디자인: /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/_archive/sc-ax/sc-meeting-redesign/design/MeetingWorkspace.html 및 DS tokens/styles/components read-only.
- 사용자 스크린샷: /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/visual-review-2026-09-14/21-current-live-footer.png, 22-design-live-footer.png, 23-design-live-attachment.png, 24-current-live-ai-empty.png, 17-current-transcript-narrow.png. 직접 열어 비교.
- 이번 브리프가 승인된 변경 계약이다. 기존 보고의 미결을 임의로 확대 처리하지 않는다.

## 2. 배경

이전 FE 작업 이후 사용자가 회의 중 실물 화면을 확인했다. 메모 입력 폭, AI 결과 전 표시, 좁은 스크립트, 진행 중 첨부 버튼, 종료 버튼 스타일을 수정한다. 사용자에게 5항목으로 설명했고 '응 중만 발주하자'로 승인받았다.

## 3. 계약

backend는 읽어서 실제 API/envelope를 확인만 한다. API가 없거나 계약이 부족하면 근거와 함께 보고. 임의 API·가짜 저장·추론 권한 금지.
사용자가 첨부 업로드 문제는 직접 수정했다고 명시했다. 과거 500 오류 수리·처리 워커 기동·첨부 모달 리팩터링은 이번 범위에서 제외하고 사용자 변경을 보존한다.
메모 POST는 agendas/{agendaId}/lines로 안건 선택이 필요하다(§6). 대상 안건 선택·+ 새 안건 기능을 제거하지 않는다. 회의 중 메모 권한 및 실제 저장 동작 유지.

## 4. 핵심 파일

MeetingDetailPage.tsx와 회의 중 메모/스크립트/안건 부품, styles/meetings·workspace·components, lib/labels, DS Button/Spinner/empty state 등 실제 파일 확인.
MeetingLive.test.tsx와 관련 테스트. 현재 shownAgendas는 AI batch가 없으면 일반 agendas로 fallback하고 있어 사람이 쓴 안건 제목과 빈 후보 상자를 보여준다. 실제 저장된 AI 결과를 상세 응답으로 복원하는 경우까지 살펴본다.

## 5. allowed_paths

frontend/src/의 위 5항목에 필요한 코드·DS 스타일·라벨·테스트만.
backend/, docs/, .design-sync/, frontend/ds-entry.tsx 및 다른 사용자 수정은 보존. 시작 전 git diff/status를 확인하고 영향 파일을 나열한다.

## 6. 구현 — 회의 중 5항목

1. 하단 메모 입력줄: 시안처럼 상세 칸 너비 대부분을 입력줄로 사용하고 오른쪽에 DS 보라색 '기록' 버튼. 현재 왼쪽에 짧게 몰린 폭/여백 수정. 안건 선택과 + 새 안건은 스펙상 기능이므로 유지하고 입력 공간과 자연스럽게 배치. 저장 실패 시 입력 보존, 키보드 동작과 권한 유지. 시안의 하단 상태 데모 막대는 복제하지 않는다.
2. AI 요약 대기: **실제 AI 요약 결과가 없을 때** 일반 안건 및 빈 다음 할 일 상자를 대신 나열하지 말고 정확한 문구 **'AI 요약이 곧 생성됩니다.'** 표시. labels에서 prop으로 전달. 실제 AI 결과가 도착하면 해당 AI 트랙 안건/줄/잠정 후보로 전환. stream.batch 유무만으로 판정해 새로고침 후 이미 저장된 AI 요약을 숨기지 않는다. AI가 기존 안건을 요약한 경우도 유효하므로 source=AI로만 필터하지 않는다. AI 트랙·메모 트랙 분리 및 읽기 전용 후보 계약 유지.
3. 스크립트 가독성: 진행 중 탭의 발언은 '시간 · 화자' 위 한 줄, 본문 아래 열 전체 너비. 발언 간격 확보. DS 본문 크기/일반 굵기/본문색/행간, 화자 작은 크기/중간 굵기, 시간 같은 작은 크기/읽을 수 있는 보조색. 폭 때문에 글자를 축소하지 않는다. 시각 칩과 근거 점프/현재 줄 강조/실시간 갱신/스크롤 보존. 캐릭터가 발언을 가리지 않도록 조정. 드래그 너비 조절은 미승인이라 구현하지 않는다. 종료 화면 디자인을 별도로 바꾸지 말되 공용 스타일로 영향이 생기면 명시 보고.
4. 진행 중 + 자료 첨부 버튼: 사용자 수정으로 이미 해결됐는지 먼저 확인. 실제 계약/권한에 따라 파일 목록 바로 아래 버튼이 빠져있을 때만 표시/연결 수정. 업로드 처리·모달·API를 다시 고치지 않는다. backend가 미지원이면 그대로 보고. 상태만으로 권한을 새로 추론하지 않는다.
5. 회의 종료 버튼: 최신 사용자 정정 — 현재 빨간색 solid 버튼을 유지한다. 검은 글자/채움 없는 형태로 바꾸지 않는다. 이미 바꿨으면 기존 DS danger/solid로 복원. 종료 동작·확인·권한·확장 아이콘 위치·집중 모드 유지.

## 7. 제외·보존

- 종료 후 '최종 회의록 생성 중입니다.' 스피너: 다음 발주로 보류.
- 종료 후 업무 요청 모달 상태|요청자 제거: 다음 발주로 보류.
- 완료 회의 정보 편집 진입점 결정: 이번 범위 아님.
- 첨부 업로드 500: 사용자 해결, 이번 수정 제외.
- backend/API 구조·viewModels·envelope 판단·상태 관리 책임 변경 금지. 새 워커·워크트리 생성 금지. 커밋·push·PR 금지.
- DS 부품/--scax-* 토큰 사용. 필요한 스타일만 DS에 보완. ds 안 문구 하드코딩·구 클래스 금지.

## 8. 검증·보고

회의 중 위 5항목 회귀 동작을 테스트. tsc --noEmit 오류 0, npx vitest run 전체 실행. 직전 기준 532 통과(직렬 실행 결과)이며 기본 병렬 간헐 타임아웃은 숨기지 않고 별도 보고. 접근성·텍스트 실패는 기능부터 확인. 이탈 가드 잠금 2건 유지. '없음' 단언으로 기능 삭제를 정당화하지 않는다.
사용자가 실제 회의 중 테스트를 직접 진행하므로 실제 회의 시작/종료·업로드 등 쓰기성 브라우저 검증을 임의로 하지 않는다. 가능한 비파괴 시각 확인만 수행하고 실제 브라우저 미검증 항목은 명시한다. 전체 빌드·acceptance-e2e·DB reset 금지.
결과는 1~5 각각 완료/미완료, 변경 파일, 테스트 정확한 명령/수치, 미지원 계약, 사용자 첨부 변경 보존 여부를 포함한다. 종료 후 범위는 손대지 않았는지 명시. 결과 보고는 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/frontend-live-result.md에 남기는 것만 별도 허용한다.

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
