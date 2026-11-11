# [reviewer_doc] 룸 상세 후속 SPEC/WPv5 독립 검수

read-only·하위위임금지. spec/code/GitHub쓰기·커밋·머지0. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/detail-polish-spec-brief.md(정확합의전문), detail-polish-spec-report.md, detail-polish-spec-layout-fix-report.md(버튼둘째줄ASCII보완), delivery-request-v5.json, _RESUME 최신. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec d6d961e9 대비SPEC003diff. code읽기만 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 47be2cb0.
이번3항목: 룸명헤더전체폭정중앙/왼쪽뒤로가기, 상세상단은called남은호출박스만(부분/여러호출유지·수락완료숨김), 시술행5상태(준비/호출/수락후시작, 진행mm:ss+[종료][⋮], 완료N분+[⋮])·모든행상태Pill제거·행수락/호출정보제거. 수락동작은상단호출박스/기존목록/호출탭유지. 호출중시작비활성, ready_wait와accepted의canStart/권한/요청중보존(준비중이라도서버true를막지않음), 기존취소확인/권한그대로. 완료N분spanMin기존규칙·null이면완료만. 상세마취/목록상태박스/푸시/세션/API/서버0. OQ31헤더부분만해소, 마취유지.
WPv4→v5 same235/1개PR/사용자최신승인원문「ㅇ으 그렇게 해서 이거까지 발주하자」결속·L3/기존pendingmainbaseline·기존의존/rollback보존. version/digest는코디CLI. SPEC ASCII/U4/U6/U7/AC/OQ 충돌0·새업무판정/문구발명0. model/schema/lint로그확인하고필요한최소검증만. 이전회차미해결을새범위에섞지않음.
산출물 profile review-detail-polish-spec-report.md(PASS/WARN/FAIL근거·좁은수정요청), 수정금지. livepreamble task/dispatch/outcome/report-path로worker_done1회뒤idle. 코드발주는코디가한다.

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
