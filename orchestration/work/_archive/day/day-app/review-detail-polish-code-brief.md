# [reviewer] 룸 상세 다듬기 독립 코드·시각 검수

read-only·하위위임금지. spec/code/GitHub/서버/시뮬조작0, commit/push/merge0. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/detail-polish-code-brief.md/detail-polish-code-report.md/review-detail-polish-spec-report.md, spec tree SPEC003개정④ exact head는보고서확인. code tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 47be2cb0 대비diff. 이전 UI판190pass/native47기반, 이전report재검수할필요없음.
검수초점:
1 헤더룸이름전체폭정중앙(뒤로버튼뺀영역가운데아님), 320긴이름에서뒤로가기접근/semantics겹침0. 공유widgets헤더바뀌면room만적용다른화면default보존.
2 상세호출박스는미수락called남은호출만. 전부수락숨김/부분·여러호출중남은대기는그대로. 상단수락간호대리/원장즉시/재호출/목록/호출탭정책0변경.
3 시술5상태모든조작둘째줄오른쪽. 행수락/상태Pill/호출대상·호출경과없음. 준비/수락후시작은canStart/권한/busy보존(readytrue사례반드시), 호출중비활성시작. 진행=상단제목/큰mm:ss분누적·아래담당의/시각+[종료][⋮], 완료=상단제목/완료N분(값없으면완료만)·아래담당의+[⋮], 회색톤. 데이터그행만·새timer0·spanMin변경0. canUndo/확인창/API/권한보존, readonly새동작0. 320긴제목/담당의/큰시간줄침범없음.
시각phone+iPad5상태/320헤더·시술긴이름/부분·모두수락 PNG직접보기. caller/accepted같은행이면[시작]비활성/활성만다름이의도. 시술행클릭차트열기원래동작보존, 공통메뉴/통역/마취/목록2줄상태박스회귀0.
검증: 최종소스시각뒤 fulltest/analyze/build로그확인, 너는좁은관문1회와필요시analyze, 전체반복불필요. 수정/화면조작금지. 사용자세션/데이터보존된sim최종PID·표준main/로컬origin로그확인(로그인입력/업무쓰기는없음). 서버/env/native/서명변경0.
보고 profile review-detail-polish-code-report.md(PASS/WARN/FAIL/근거·직접본PNG·실행한것/보고만본것·직원실물에서만날자리). livepreambleID/outcome/report-path로worker_done한번후idle. 새범위/정책추가요구하지말고계약내실제결함만지적.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_1d5db035-7383-46d1-97ae-2e65e50e3927 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
