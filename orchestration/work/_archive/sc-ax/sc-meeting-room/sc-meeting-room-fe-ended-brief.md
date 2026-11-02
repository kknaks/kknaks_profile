# [frontend] 종료 후 최종 회의록 생성 안내·업무 요청 모달 정리

너는 sc-ax frontend 워커다. 역할 문서를 먼저 읽어라:
- /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md (+ rules.md·skills.md·tools.md·workflow.md)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`
브랜치 `kknaksss/sc-meeting-room`, 확인한 HEAD `75360fe`, base `origin/main`.
사용자는 이번 대화에서 아래 시안 수정안을 검토하고 프론트 구현 발주를 명시 승인했다. 커밋·push·PR 금지.
기존 DS sync 작업의 미커밋 변경(.design-sync/, frontend/ds-entry.tsx)을 보존한다. 이 파일들은 이번 수정 대상에서 제외한다. 새 워크트리·하위 워커를 만들지 않는다.

## 1. 이번 승인 범위

사용자가 회의 중 작업 완료를 확인한 뒤 '종료 까지 갈거야 발주하자'로 종료 후 보류 항목 구현을 승인했다. 확정 항목은 아래 두 가지다. 이전 구현(547 테스트)과 사용자 첨부·backend 수정 위에서 이어 작업한다.
- 참고 이미지: /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/visual-review-2026-09-14/25-current-final-generating.png, 18-current-followup-modal.png, 19-followup-fixed-metadata.png.
- SPEC 읽기 전용: /Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec/products/sc-ax/20-spec/spec-004-meeting-note.md §8 종료 합성, §9-5 D40·R-48 후속업무 요청자.
- DS: 현재 frontend/src/ds와 styles의 --scax-* 토큰. 필요한 스타일이 없으면 기존 DS에 최소 추가. 구 DS 클래스 금지.

## 2. 종료 후 생성 안내

현재 회의 종료 후 정리 중 화면은 설명이 부족한 긴 스켈레톤 7줄이다. 사용자 확정: **스피너 + '최종 회의록 생성 중입니다.'** 로 바꾼다.
- 실제 종료 이후 정리 중 상태에만 표시. 이전 'AI 요약이 곧 생성됩니다.'는 회의 중이며 혼동 금지.
- 스켈레톤 대신 읽기 쉬운 로딩 안내를 회의록 본문 영역에 표시. 기존 DS Spinner/StatusNote 등 적절한 부품을 먼저 찾고 없으면 DS 방식으로 보완. 문구는 labels에서 전달, ds에 하드코딩 금지. 접근성 status/busy 알림 고려.
- 성공하면 실제 최종 회의록으로 전환. 실패하면 실제 실패 상태/사유 안내로 전환하고 영구 스피너로 가리지 않는다. 기존 폴링/스트림 종료/재전사·합성 계약/재조회 유지. 프론트 타이머로 성공을 지어내지 않는다.
- 종료 직후, 정리 중 새로고침, 정리 완료, 실패 전환을 기존 테스트 방식으로 검증한다.

## 3. 회의 후속 업무 요청 모달

사용자 확정: 회의록 다음 할 일에서 업무 생성으로 여는 모달에서 **상태 | 요청자 영역 전체 제거**. 항상 판단 대기·시스템(회의)인 값이므로 생성 폼에 불필요.
- 회의에서 여는 후속 요청에만 적용. 일반 업무 요청/일반 업무 생성 모달은 유지.
- 실제 요청자는 system:meeting, 누른 사람은 promoted_by와 참조라는 backend 계약 유지. 표시만 제거하고 payload·source_meeting_id/source_agenda_id·참조자·담당 선택·기한·체크리스트·요청 제출 흐름 유지.
- 기존 모달 재사용 구조에 명확한 context/prop을 최소 추가하는 등 현재 설계로 분리. 제목/사람 이름/상태를 추론해 회의 후속 요청 여부를 판정하지 않는다.
- 요청 성공 후 후보의 요청됨 표시, 중복 방지·이탈 가드·실패 후 입력 보존 유지.
- 회의에서 열린 모달은 해당 메타가 없고 나머지 필드/실제 제출값이 유지되는지, 일반 요청은 메타가 유지되는지 테스트.

## 4. 이미 처리한 것·제외

- 스크립트 가독성은 앞 작업에서 공용 부품 변경으로 종료에도 적용 완료. 이번에는 재구현하지 말고 회귀 여부만 확인.
- 첨부 업로드는 사용자가 직접 수정. 첨부·워커 기동·backend 수정 금지.
- 진행 중 첨부 허용 여부는 SPEC/BE 계약 문제로 남아있으며 이번 범위 제외.
- 완료 회의 정보 편집 진입점 문제는 사용자 결정이 아직 없으므로 임의로 디자인을 발명하지 말고 별도 미결로 보고.
- 회의 중 메모/AI 대기/빨간 종료 버튼·중복 quick-start 잠금은 보존.

## 5. 계약·allowed_paths

frontend/src 내 두 항목에 필요한 구현·DS·스타일·labels·테스트만 수정. backend는 읽기 전용. docs/, .design-sync/, frontend/ds-entry.tsx·사용자 수정 보존. API가 부족하면 근거와 함께 보고하고 억지 API/가짜 동작 구현 금지. 상태 관리·api.ts·viewModels·권한 판단 책임 경계 유지.
시작 시 git status/diff와 영향 파일 확인. 커밋·push·PR·새 워커·새 워크트리·DB reset 금지.

## 6. 검증·완료 보고

npx tsc --noEmit 오류 0 및 전체 npx vitest run. 직전 직렬 547 통과. 기본 병렬 부하 민감성은 정확히 구분 보고하고 필요시 직렬 결과를 함께 제출. 이탈 가드 잠금과 StrictMode quick-start 회귀 유지. 텍스트/접근성 실패는 기능을 확인하고, 없음 단언으로 제거된 기능을 정당화하지 않는다.
사용자가 실제 회의 e2e는 직접 한다. 실제 회의를 임의 생성/종료하거나 요청을 실제 전송하지 말고 단위 테스트 및 가능한 비파괴 시각 확인을 한다. 실제 화면 미검증 범위를 명시. 전체 build/acceptance-e2e 금지.
결과 파일 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/frontend-ended-result.md 쓰기만 추가 허용. 항목별 결과·변경 파일·테스트 정확한 명령/수치·미결·사용자 변경 보존·브라우저 확인 여부 보고 후 2채널 완료 알림.

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
