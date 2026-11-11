# [planner] 로컬 DAY API 정합 — SPEC003 및 WP v3 소비 계약 정리

역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/ 문서·mediness AGENTS 라우팅을읽는다. 하위워커/내부서브에이전트금지. 앞맥락파일로복원.
작업트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD1551fa22. 기존SPEC PR921 OPEN. profilework /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app.

## 1. 사용자승인·원천
사용자최신 「응 작업 시작하자 ! 지금 테스트는 로컬 백엔드로 올렷어 !」. WPv2 #235의 구현진행을승인했고 로컬최신API소비를지정. 기존요구 DAY기준으로맞춤·백엔드는수정하지않음. 머지는마지막명시지시만. WPv2 phase1의업무계약정합부터수행. 문서선머지gate없음.
읽을것 profile _RESUME.md, delivery-request-v2.json, review-wp-v2-2-report.md, ui-spec-brief.md, planner-ui-spec-fix-report.md, research-prototype-toasts.md. 앱스펙003전문+SPEC001. 옆세션 _RESUME.md, /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md @e421b77b4bb836c7c557419dd3fad22db1900862 (read-only), 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 @a1c90b9dc63271dc06023ec0a530c53a216a296c. localhost11040 healthready200, 실제이브랜치로day-local가동(옆_RESUME확인). API/코드는스펙소비근거이지새업무정책을짓는권한아님.

## 2. 최소정합 계약
최신DAY업무규칙은옆SPEC002를소비, UI13항목기존그대로. 아래6차이중소비에필요한것만003정합:
- card need삭제→needs[]: 서버가정한5상황 why wait/anes/call/accept/home 소비. 앱은새업무판정안함. 카드4행·4필터그대로, 확인필요테두리/상세표시는서버needs있을때. 기존2종제한은DAY업무원천갱신에따라교체. 정확한필드/문구는SPEC002/웹원문.
- 재호출: tasks[].canRecall 서버bool+기존권한, called줄에노출. need.why==call5분조건은제거. 대상call·처음대상기본선택·API그대로, 권한확대없음.
- 취소: 세로⋮ 시작취소/완료취소는유지. 최신DAY의확인모달·원문 「{시술} 시작을 취소할까요?」「{시술} 완료를 취소할까요?」「시작 취소/완료 취소」「닫기」소비. 토스트안되돌리기없음유지. 폰시트/iPad모달 등앱적응은기존패턴, 문구창작없음.
- 마취: lastMinutes삭제→lastSeconds. 서버초값표시형식변환만(업무재계산금지). 사용자확정목록 「시술대기-마취완료 N분」의분표시는초→분시간format으로유지, 상세도합의UI존중. 진행runningSince/long/limits를소비, 회차start/end반복·귀가시서버닫힘동작수용. 서버 long>20분기준존중.
- pickable은서버ready-only값소비, 시트체크입력조건그대로.
- 원장변경API/푸시유형은이번새UI기능에추가하지않음. 방이동/차트쓰기/알림서버/APNs서버/통역서버범위밖그대로.
현재구현·SPEC002와정확대조해 파서가쓰는추가변경(검색body필드등)있으면필요한API소비정합만기록, 새기능으로확대금지.

## 3. SPEC수정범위
SPEC003의본문/표/시나리오/A조건/차이표/OQ를동일계약으로정리. 기존13UI원천보존, 원장직접/간호대리/TW/성공토스트2.6초/UI4행/4메뉴/배지서버없음 유지. 버전/last_updated는레포규약대로, 미머지/코드미반영표시보존. 옆SPEC002는수정하지않고그exactsha를소비원천에기록. SPEC001/D1환경·세션·SSE보안무관변경금지.

## 4. WPv3 입력
기존#235같은idempotency day/day-app, v3=현재v2+1. riskL3누적유지, latestoriginmain(코디fetch시3f57c1af...) exactSHA·baselinepending정직. delivery-request-v3.json을v2에서최소변경: 위업무/API소비정합으로A2/A16/A17/A19등모순정리·scope_delta원천/사용자최신지시명시, phase1대조가해결한것과남은로컬검증을구분. 새app/만·backend변경없음. 기존승인receipt대행하지않음,코디가현재사용자진행지시와결속. 이번태스크GitHub쓰지않음.

## 5. allowed_paths
products/day/20-spec/spec-003-mobile-app.md, 20-spec.md 최소정합. profilework delivery-request-v3.json, planner-local-alignment-report.md만. 다른스펙/30-work/옆세션/코드읽기전용. 커밋/push/PR/merge/서버조작/로그인/실env읽기금지. json은CLI입력뿐WP원장은235.

## 6. 검증·완료
SPEC상호모순0·UI13회귀0·정확API필드·권한재계산0, git diff --check, lint --strict(DAY0), JSONschema/model0. 보고에정합표/원천file:line/업무결정변경없음/실물검증미실행을한국어로. livepreambleID우선,worker_done한번후idle. 다음독립리뷰PASS뒤mobile코드발주예정.

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
