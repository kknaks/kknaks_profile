# 채팅 앱 독립리뷰 W1 화면 검증 보완
너는 mobile 작성자다. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS.md, chat-mobile-review.md, chat-mobile-completion-fix-report.md를 먼저 읽어라. 이번 수정은 W1(가로·긴글자·키보드 열린 화면 증거 부재)만. app/test/capture/chat_capture_test.dart 및 필요한 app/test 전용 fixture, profile chat-mobile-layout-evidence-report.md/별도 PNG 증거만 허용. 제품 코드 수정은 실제 overflow 재현된 경우에만 최소 수정하고 원형/스펙 대조 근거를 보고한다. 임의 문구·디자인·정책 추가0, 다른 backend/spec/사용자 시뮬레이터/실계정/서버 조작0, commit/push/하위위임0.
폰 가로844x390 목록·대화, 대화 viewInsets 키보드 열림 입력창/메뉴, 긴 직원명·그룹제목·직무명 목록/머리/전달시트의 대표 장면을 fixture로 캡처하고 RenderFlex overflow0, 필수 조작 버튼 접근 가능을 단언한다. 기존 테스트를 그대로 다시 다 돌리지 말고 관련 캡처/위젯만 재현, 제품 코드 수정이 있으면 analyze 및 해당회귀+필요빌드. 상단/하단 잘림·키보드가 입력창 가림 여부는 실제PNG 열어 확인. nativePASS 수는 코디54, 리뷰어55로 보고차이가 있으므로 기존 로그의 PASS 줄 세어 원인만 보고(제품변경0).
최종 chat-mobile-layout-evidence-report.md에 변경파일·검증명령·PNG·제품코드변화여부·미결 기록. lifecycle은 새 preamble의 IDs, --outcome succeeded/failed 및 --report-path 실제 경로로 1회 완료보고 후 idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_e8a8842c-a789-4862-93a5-7886d6bd1c61 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

