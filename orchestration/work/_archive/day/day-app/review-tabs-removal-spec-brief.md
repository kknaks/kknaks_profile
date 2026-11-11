# [reviewer_doc] 상단 인박스 탭 제거 SPEC/WPv6 검수
read-only·하위위임/수정/GitHubwrite/commit/merge0. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/tabs-removal-spec-brief.md/tabs-removal-spec-report.md/delivery-request-v6.json, spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec 4a5d4a47대비SPEC003diff. code tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 4ee33f95 읽기만.
현재사용자가상단현황/호출/완료3탭제거확인「응 시술현황은 카드만 보여주면 된느거 아니야?」. 기존4필터+서버cards[]목록만, DAY공통머리/하단4메뉴/서버판정/직무별수락/상세개정④유지. 별도호출/완료목록·검색UI제거, 새대체메뉴·완료카드합치기·새정렬·서버API변경0. U2/U10/U11·수락진입점·AC·ASCII·관련OQ의옛내부탭정의정합, 아래4메뉴를잘못지우지않음. 서버calls/doneTab수신계약은그대로. 기존귀가처리도그대로. WPsame235/key/version6/L3/mainpending/1PR237/사용자merge마지막·현재지시결속.
모델/schema/lint실행로그확인, 필요한최소검증만. 기록원천은4a5d4a47+개정⑤미커밋(코디head결속)정직표기. 삭제기능의옛인수조건존재여부·이전합의회귀없음확인. 산출물 profile review-tabs-removal-spec-report.md(PASS/WARN/FAIL근거), livepreamble정확ID/outcome/report-path로worker_done한번후idle.

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
