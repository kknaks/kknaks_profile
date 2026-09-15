# [frontend] 가독성·업무 요청 폼·자료 닫기 위치 수정

너는 sc-ax frontend 워커다. 역할 문서를 먼저 읽어라:
- /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md (+ rules.md·skills.md·tools.md·workflow.md)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`
브랜치 `kknaksss/sc-meeting-room`, 확인한 HEAD `75360fe`, base `origin/main`.
사용자는 이번 대화에서 아래 시안 수정안을 검토하고 프론트 구현 발주를 명시 승인했다. 커밋·push·PR 금지.
기존 DS sync 작업의 미커밋 변경(.design-sync/, frontend/ds-entry.tsx)을 보존한다. 이 파일들은 이번 수정 대상에서 제외한다. 새 워크트리·하위 워커를 만들지 않는다.

## 1. 사용자 승인과 참조

사용자가 아래 5개 스크린샷을 보며 확정한 수정이다. '이제 보내고 수정한 다음에 결과 받아오자'로 발주/결과 회수 승인.
이미지 폴더 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/visual-review-2026-09-14: 26-list-low-contrast.png, 27-request-label-wrap.png, 28-assignee-option-contrast.png, 29-material-close-position.png, 30-reference-button-contrast.png를 모두 직접 열어 확인한다.
현재 사용자 수정과 앞선 작업을 보존하고 아래 항목만 수정. 종료 후 직전 보고 기준 555 테스트 통과.

## 2. 회의 목록 글자 대비

날짜·제목 없음·참석 인원·목록 구획 등 현재 회색으로 묻히는 텍스트를 검은색(DS 기본 본문 잉크 토큰)으로 맞춘다. 실제 회의 제목도 같은 읽을 수 있는 대비. 상태 배지의 의미 색상(실패 빨강·종료 초록 등)은 유지. 선택/hover 배경과 비활성 의미를 손상하지 않는다.

## 3. 업무 요청 폼

- '요청할 업무'와 필수 *가 한 줄에 붙어야 한다. 별표가 다음 줄로 내려가지 않도록 label 구조/스타일 수정. 필수 의미/접근성 유지.
- 참조자·참고 업무·시작 단계 섹션 라벨은 검은색.
- 담당 후보 드롭다운에서 선택 가능한 사람 이름도 검은색. 회색이라 비활성으로 오해되지 않게 한다.
- '참고 업무 연결' 버튼은 실제 활성 상태라면 검은 글씨와 DS 배경/테두리로 버튼임이 보이게 한다. **실제 disabled일 때만 회색**이라는 사용자 지시. 활성 선택 항목/버튼을 흐리게 하는 CSS를 점검하되 실제 권한·disabled 상태를 강제로 활성화하지 않는다.
- 참조자 선택 칩 등 해당 폼의 활성 조작 텍스트도 같은 기준. 입력 placeholder/진짜 disabled를 일괄 검정으로 바꾸거나 앱 전체 무차별 CSS override는 하지 않는다. 안내 문구 전체 재작성은 범위 아님.
- 일반 모달과 공용 DS에 영향이 있으면 범위를 확인하고 보고. 문구/제출 payload/담당 후보 목록/권한/시스템 회의 요청자 기록/일반 업무 요청 기능 유지.

## 4. 자료 미리보기 닫기

자료 미리보기 헤더의 ×가 파일명 바로 옆에 붙어 있다. 헤더 오른쪽 끝으로 배치. 제목 영역은 가용 폭 안에서 줄바꿈 또는 기존 말줄임 규칙을 따르고 닫기와 겹치지 않게 한다. 닫기 동작/aria label·키보드 포커스·드로어 동작 유지. PDF 뷰어 내부 툴바/파일 내용/업로드는 범위 아님.

## 5. 구현·제약

기존 ds/부품·--scax-* 토큰을 재사용하고 필요한 CSS/variant만 추가. ds에 문구 하드코딩 금지. 구 .btn/.field/.badge/.avatar 재도입 금지. 검정 hex 직접 박기보다 DS 본문 토큰.
allowed_paths: frontend/src의 관련 구현·스타일·라벨·테스트만. 결과 파일 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/frontend-contrast-result.md만 별도 쓰기 허용.
backend/·API 구조·viewModels·권한 정책·docs/·.design-sync/·frontend/ds-entry.tsx·사용자 기존 수정 보존. 시작 시 git diff/status와 영향 파일 확인. 커밋·push·PR·DB reset·새 워커·새 워크트리 금지.

## 6. 검증·보고

npx tsc --noEmit 및 전체 npx vitest run. 병렬 부하 실패 시 정확한 실패와 직렬 결과를 구분. 직전 555 통과. 스타일만을 그대로 복제하는 테스트를 불필요하게 늘리지 말고 필수 label/활성·disabled/닫기 접근성 등 실제 회귀 위험만 확인.
사용자는 실제 e2e를 직접 하므로 실제 회의/업무/업로드를 생성·변경하는 UI 검증 금지. 가능한 비파괴 프리뷰로 스크린샷과 대비/필수 표시 줄바꿈/닫기 위치를 확인하고, 브라우저로 확인하지 못한 것은 명시.
결과 보고에는 항목별 변경 파일·실제 사용한 DS 토큰/variant·검증 결과·미결·시각 검증 여부를 포함. 완료 후 아래 2채널로 회신하고 대기.

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
