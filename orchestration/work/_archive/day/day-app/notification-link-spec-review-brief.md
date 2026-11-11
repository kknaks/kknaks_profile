# [reviewer_doc] 알림003↔005 연결 좁은 검수

read-only/하위위임·commit·push0. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD0d0ba25f 위미커밋003/005두파일만. 관련AGENTS/문서규칙/역할유지. notification-link-spec-brief.md/report·이전005재검수보고·현재두파일diff검수. 채팅code계약은git53adbd49불변핀(양code워커안내msg_d68d00cbe6ea/msg_b5ed8820a69e)으로보존, working003알림연결만코디가동결해제. 000/001/002/004여전히불변.
범위/판정: 003절대미구현문구를005구현전단계로한정하고005구현뒤계약소유연결만최소정합, 005선행조건적용표기정직·현재코드완료아님, 시술현황/채팅/세션/API/수신자/role/문구변경0, 별도WPv8착수전문서정합충족인지. 005이미검수된API/AC재설계0. lint최종1회DAY0/diffcheck/000001002004blob53ad동일. 보고하나 profile work/day-app/notification-link-spec-review.md. PASS/WARN/FAIL·fileline근거·actualvalidation, 정확worker_done/checkack후idle. 원천전체처음부터재조사X.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_4fc8346e-2c4e-4f56-a8a4-96120c073f8c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
