# 키보드 시험 2장면만 추가
기존 mobile 작성자다. chat-mobile-layout-rereview.md W1을 읽어라. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS 준수. 허용 파일 app/test/capture/chat_capture_test.dart와 profile 보고 chat-mobile-keyboard-matrix-report.md/증거PNG뿐. iPad1024x1366 viewInsets400, 폰 가로844x390 viewInsets200의 대화 화면 두 장면을 기존 layout그룹에 추가해 noOverflow + 입력창/보내기 hitTestable/키보드 위 단언. 제품코드 변경0, 새UI문구0. 제품 결함이 실제로 나오면 조용히 시험약화하지 말고 재현/최소정정 제안으로 코디질문.
관련 레이아웃 그룹만 실행하고 PNG 직접 열어 입력줄 잘림0확인. 전체테스트/native/build/사용자시뮬레이터/DB/서버/Gitcommit/push/하위위임0. 시험만 추가되므로 코디가 직접 같은 그룹을 최종 재현하고 기존 제품 독립리뷰PASS와 연결한다. 보고에 시험결과/파일hash/PNG/제품변경0을 남겨라. 새 preamble lifecycleIDs와 --outcome succeeded/failed --report-path 실제경로로 완료1회 후 idle.

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

