# [reviewer] 시술현황 상단3탭제거 독립 코드·시각 검수
read-only·하위위임/코드spec수정/GitHub쓰기/서버·시뮬조작/commit/merge0. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/tabs-removal-code-brief.md/tabs-removal-code-report.md/review-tabs-removal-spec2-report.md(최신PASS), spec tree SPEC003개정⑤. code tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD4ee33f95 대비diff.
확인: 상단현황/호출n/시술완료n탭과선택상태/별도호출·완료·검색UI없음, 연결상태+기존4필터+cards[]만. 숨은대체라우트/새메뉴·새정렬·doneTab완료카드합치기없음. 하단4메뉴·DAY머리/종·폰1열/iPad격자/필터서버section/서버순서/카드2줄상태·카드직접수락·상세수락·푸시진입/세션race/API모델수신/귀가처리/개정④모두보존. 삭제된UI만맞춰테스트정정하고핵심수락/권한/세션검증은살아있는지확인.
직접PNG phone/iPad/320상단확인(탭3개없고필터아래즉시카드), 수락가능카드/readonly/빈판/상세개정④필요장면. fulltest/analyze/build가마지막소스후인지로그확인. 너는좁은관문1회+필요시analyze만, 전체반복불필요. 서버/env/native변경0·기존로그인/데이터보존된같은sim PID·실행인자로그확인. 증거는fixture/actual구분, 실제로그인입력·업무쓰기는미실행.
보고 profile review-tabs-removal-code-report.md(PASS/WARN/FAIL근거·직접본PNG·직접검증/로그확인구분·직원실물자리·남은의존). 실명본문복사안함. livepreamble task/dispatch/outcome/report-path로worker_done한번후idle.

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
