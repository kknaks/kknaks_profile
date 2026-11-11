# [planner] WP v2 리뷰 W1 최소 정정
역할/원천/경계는 wp-v2-brief.md 그대로. profile작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-wp-v2-report.md 전체를 읽고 W1과 참고2건만 정정. 대상 delivery-request-v2.json, 보고 planner-wp-v2-fix-report.md 두개만. 기존planner-wp-v2-report는옛판보존.
W1: dependencies[1]/review_surface[7]③의 A7오기를고치고 정확한영향=SPEC003 U3확인필요테두리/U4상세머리/A2재호출, 카드need키가아예없어져needs[]만있음 명시. A16/A19에기존확인필요테두리·머리표시회귀조건추가. 옆계약5상황을새로약속하지말고정합dependency그대로.
참고: review_surface[4]의 is_demo제거→컬럼유지·동작분기만제거로사실정정. predeploy[0]과A12검증조건이애매하면실제변경별회귀검사시점과pending조건분명히일치시킴(불필요한옛전체backend테스트재발주금지).
새계약/버전3/승인receipt/스펙/코드/GitHub변경없음. 여전히v2미발행. JSON파싱·schema/model검증1회, 결과한국어보고. 하위위임금지. livepreamble우선·worker_done한번·idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
