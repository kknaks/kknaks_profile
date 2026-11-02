# [frontend] 사이드바 상단 시안 적용 — 비활성 알림·기존 설정 이동

너는 sc-ax frontend 워커다. 역할 문서를 먼저 읽어라:
- /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md (+ rules.md·skills.md·tools.md·workflow.md)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`
브랜치 `kknaksss/sc-meeting-room`, 확인한 HEAD `75360fe`, base `origin/main`.
사용자는 이번 대화에서 아래 시안 수정안을 검토하고 프론트 구현 발주를 명시 승인했다. 커밋·push·PR 금지.
기존 DS sync 작업의 미커밋 변경(.design-sync/, frontend/ds-entry.tsx)을 보존한다. 이 파일들은 이번 수정 대상에서 제외한다. 새 워크트리·하위 워커를 만들지 않는다.

## 1. 승인 범위·시안

사용자 최신 지시: 전체 사이드바가 아니라 **상단만** 먼저 시안대로. 알림은 기능이 없으므로 비활성. 기존 설정 진입점을 시안 상단 설정 위치로 이동해 현재 설정 기능에 연결. 사용자가 '발후해'(발주해)로 승인했다.
시안 이미지 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/visual-review-2026-09-14/31-design-sidebar-top.png를 직접 열어 확인. 시안의 보라색 이미지 선택 테두리/상단 SCR 캡션은 디자인 도구 UI이므로 구현하지 않는다.

## 2. 구현 항목

- 상단 실제 사용자 아바타·이름·직책을 시안처럼 좌측에 배치, 오른쪽에 사이드바 접기 버튼.
- 아래에 알림 행 → 설정 행 → 가로 구분선. 시안의 배경·여백·크기·정렬·아이콘을 DS 기준으로 맞춘다.
- 알림은 **실제 disabled 상태**로 클릭·키보드 실행이 안 되게, 비활성 색상과 접근성 적용. 알림 점/미확인 건수는 넣지 않는다. 기능을 새로 만들지 않는다.
- 설정은 현재 사이드바에 있는 설정 동작을 이 위치로 옮겨 그대로 연결한다. 기존 하단 설정 진입점은 중복되지 않게 이동 처리하고 로그아웃 등 다른 동작은 보존. 새 설정 페이지를 만들지 않는다.
- 사이드바 접기/펼치기 기능과 축소 상태 접근성·툴팁 등 기존 동작 유지. 접힌 상태에서도 기존 navigation 기능이 깨지지 않게 확인.
- 사용자의 실제 이름·직책·사진 데이터를 사용. 사진/직책 데이터가 없으면 기존 Avatar fallback 또는 빈 값 처리하고 API 부족을 보고. 시안의 인물/직책을 가짜로 넣지 않는다.
- DS Icon/Avatar/Button 기존 부품과 SVG glyph를 먼저 확인. 대응 SVG가 있으면 재사용, 정확한 아이콘이 없으면 디자인 로컬 사본에서 확인. 필요한 아이콘을 찾지 못하면 무엇이 필요한지 보고하고 임의 엉뚱한 아이콘으로 바꾸지 않는다.

## 3. 제외

하단 메뉴 순서/이름/업무·회의 외 페이지 활성화 정책·로고·버전 재구성은 이번 범위 아님. 사용자 최초 전체 사이드바 요청은 상단만으로 범위가 좁혀졌다. 현재 하단 라우팅은 유지.
회의 화면·첨부·백엔드 변경·새 알림 기능 금지. settings 동작을 다른 페이지로 추측 연결하지 말고 실제 현재 코드를 확인.

## 4. 소스·allowed_paths

작업 워크트리 /Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room. 앞 프론트 변경은 5e7a41d로 커밋됐고 이후 사용자 변경이 있을 수 있으니 HEAD/status/diff부터 확인. 사용자 backend 수정은 절대 건드리지 않는다.
frontend/src의 shell/sidebar/App 라우팅 연결 중 필요한 부분·DS·스타일·labels·관련 테스트만. 역할 문서와 현재 AGENTS 지침 준수.
기존 ds/부품 및 --scax-* 토큰 사용. CSS 없으면 DS 방식으로 최소 추가. ds에 사람이 읽는 문구 하드코딩 금지, 호출부가 lib/labels에서 전달. 구 .btn/.field/.badge/.avatar 재도입 금지.
backend/·api.ts 구조·viewModels 책임·권한 정책·docs/·.design-sync/·frontend/ds-entry.tsx 수정 금지. 커밋·push·PR 금지(이전 사용자의 커밋 승인은 이미 수행된 변경에 대한 1회 요청, 이번 추가 수정은 미커밋으로 남길 것).

## 5. 검증·결과

설정 진입이 기존 기능을 열고 알림은 비활성, 접기/펼치기와 실제 사용자 fallback이 유지되는 의미 있는 검증. 순수 스타일을 복제하는 테스트 추가는 피한다.
cd frontend && npx tsc --noEmit
cd frontend && npx vitest run
전체 테스트는 필요한 1회만 수행하고 통과 후 같은 테스트를 여러 번 반복하지 않는다. 실패/새 변경/구체적인 미해결 우려가 있을 때만 관련 재검증. 병렬 부하 문제는 실패 종류와 직렬 검증이 필요한 근거를 명시.
비파괴 시각 확인이 가능하면 확인하되 실제 회의·업무 생성/변경 금지. 단순 static harness만 확인하면 실제 앱과 구분 보고. UI 확인 불가이면 명시하고 불필요하게 오래 붙잡지 않는다.
결과 파일 /Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/frontend-sidebar-top-result.md 쓰기만 추가 허용. 파일 목록·각 항목 완료 여부·실제 settings 연결·아이콘/프로필 데이터 미비·테스트 결과·시각 확인 여부를 보고하고 2채널 완료 후 대기.

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
