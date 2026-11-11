# [planner] 상태 박스 2차 합의 SPEC·WP 최소 반영

기존 day-app 작업의 후속, 앞 대화 맥락은 파일에서 확인. spec worktree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec (cdde456a 위), allowed products/day/20-spec/spec-003-mobile-app.md 한 파일 + profile 산출물. 역할 AGENTS.md/프로젝트 규칙 읽기. 코드·서버·다른SPEC·20-spec.md·30-work.md 변경금지. 하위워커/내부agent금지. 커밋/push/merge금지.
읽을 것: SPEC003 U3/U8/A28/A29/OQ21/30, profile mobile-ui-fix1-report.md(기존app미커밋), delivery-request-v3.json 및 현재 #235의 승인 계약(읽기만), _RESUME.md 최신.

사용자 확정 원문(2026-11-10): 「상태별 박스 항상 2줄로 하자」 → 「귀가 대기 수락 말고 상태별 박스 디자인 구성좀 통일하자 ... 상태 담당의 / - 시술명 (1개 이상일 경우 외 n개 v표시)」 → 「아래 화살표는 필요 없을거 같아」. 최종 합의: 카드 안 현재상황 박스 첫째줄 왼쪽 상태·시간, 오른쪽 담당의(없으면 담당의 미정), 둘째줄 시술명(복수면 첫 시술명 외 N개, 단수는 외N개 생략), 화살표/펼침 없음. 상태예: 시술 중 · 05:24 / KOS-DEMO; 마취 중 ·12:34 / 담당의 미정; 시술 대기 · 마취 완료20분 / 담당의 미정. 진행중 시술·마취 경과는 초단위 mm:ss(분은60넘어도계속누적; 형식변환만), 마취 완료는 lastSeconds÷60내림 N분. 기존 한줄 마취(시작시각/기준/오른쪽분)를 위 구조로 대체. 연보라/서버long빨강·시술중DAY색·서버판정 그대로.
시술명 집계는 박스 해당 상태의 시술만(시술중 doing; 대기/마취는 미완료시술), 서버순서 첫값. 새API·우선순위·다중담당의정책 없음(기존첫담당의/호출우선 유지). 호출 _callBox·_callLine 전체·수락버튼·귀가대기영역·상세시술행·룸헤더는 이번범위밖. RoomCard._nowBox 4상태만 교정. A30 등 호출 정의는 기존 그대로. 사용자가 헤더방이름가운데수정은 「기록해」라 했으므로 구현하지 않는다.
사용자 구현승인 「응 일단 이거 부터 바꾸고 오자」. 추가 승인질문 없이 이 합의 최소 반영. 레이아웃에 필요한 표시집계만, 업무판정아님.

산출물: 1) SPEC003 관련 절·ASCII·AC·충돌OQ 최소 정합 2) delivery-request-v4.json(기존v3기반, 결과계약 변화에따라version4·scope_delta 명시, 기존same235/app/만/권한/의존/baselinepending유지, 사용자위지시결속) 3) status-box-spec-report.md(변경/검증/구현메모). WP는GitHub이슈가원장이고JSON입력만작성, GitHubwrite금지. lint DAYerror0·JSONschema0. 기존v3입력보존. 코디가독립리뷰후CLI적용하고코드발주한다. 새기능/새정책없이좁게끝낼것.

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
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
