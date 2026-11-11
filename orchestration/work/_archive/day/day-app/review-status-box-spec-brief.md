# [reviewer_doc] 상태박스 SPEC/WP 좁은 검수

너는 read-only reviewer_doc. 맥락은 파일에서 읽는다. 하위위임금지. source/spec/code 수정·커밋·push·GitHubwrite·merge금지.
원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/status-box-spec-brief.md 및 _RESUME 최신 사용자 결정, status-box-spec-report.md, status-box-spec-fix-report.md(최신 범위정정), delivery-request-v4.json. spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec 기존 cdde456a 대비 SPEC003 diff. 기존 WPv3 보존 확인.
이번 범위는 목록 RoomCard._nowBox 시술대기/마취중/마취완료대기/시술중 상태박스만: 항상2줄(상태·시간/담당의 → 시술명 외 N개), 화살표없음, 단수 외N개없음, 진행중mm:ss/완료N분, 연보라/long서버빨강 유지. 호출박스/수락/귀가/상세영역 및 헤더 변경 없음. 헤더가운데는 기록만. 같은235/기존1개PR/사용자마지막merge/app만/서버판정/API/세션 보존. User승인원문 「응 일단 이거 부터 바꾸고 오자」를 결과계약에정확히결속, baselinepending보존.
SPEC003 ASCII/U3/U8/AC/OQ의 구한줄/분경과정의충돌0, WPv4의 최소scope/기존원칙보존, schema·lint 기존planner로그확인/필요시최소실행. 60분이상분누적mm:ss·시술중첫doing행시간/담당의/시술명한묶음인지명확성확인. 불명확한업무정책을새로정한곳은지적. 기존약정밖구현요구를추가하지않음.
산출물 profile review-status-box-spec-report.md, PASS/WARN/FAIL·근거·적은수정권고만. preamble task/dispatch정확히worker_done 1회(outcome/report-path포함)뒤idle. 코디가다음단계발주.

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
