# [mobile] PR 포장 검사 줄끝 공백 수정

코드 트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, branch kknaksss/day-app. 앱 독립 재검수 PASS(155 tests/native47/analyze0/build OK) 뒤 코디가 app/을 stage했다. git diff --cached --check에서 `app/test/support/ui_harness.dart:64: new blank line at EOF` 한 건을 발견했다.

허용 변경은 이 파일의 마지막 불필요한 빈 줄만 제거하는 것, profile work/day-app/mobile-packaging-report.md 한 줄 보고서뿐이다. 다른 코드·문서·테스트 의미를 바꾸지 않는다. 모든 app 파일은 이미 stage되어 있으므로 git index/commit/push/PR을 건드리지 말고 working tree만 고친다. 의미 변화 0인 줄끝 정리라 analyze/test/build를 반복할 필요 없다. 코디가 이 파일을 다시 stage하고 diff --cached --check를 검증한다. git diff --word-diff로 빈 줄 외 변화가 없는지 확인한다. 하위 위임 0. 결과는 한국어로 보고하고 live preamble의 새 id/outcome을 사용한다. 모든 merge/배포 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_aae94499-001a-4959-98e2-fe0f3f02961d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
