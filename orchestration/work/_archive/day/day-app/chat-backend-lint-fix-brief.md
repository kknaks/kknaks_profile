# 채팅 서버 재검수 W-R1 최소 정정
너는 기존 backend 작성자다. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS.md와 보고 chat-backend-rereview.md를 읽어라. scripts/deploy/day_vm.py:183 docstring의 E501 하나만 두 줄로 나눈다. 허용 경로는 이 파일 1개와 profile 보고 chat-backend-lint-fix-report.md뿐. 다른 코드·앱·DB·서버·env·배포·Git commit/push·하위위임 금지. `uv run ruff check backend scripts` 및 diff로 의미 변화0을 확인하고 전체 테스트는 재실행하지 마라. 전후 hash와 명령 결과 보고. 이 한 줄 정정은 기존 독립 리뷰의 최소 정정이며 코디가 직접 최종 lint 재확인한다. lifecycle은 새 preamble의 IDs, --outcome succeeded/failed 및 --report-path 실제 경로로 1회 완료보고 후 idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_bdc96429-0e21-4311-bca9-622e97ece387 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

