# [reviewer] 상태박스 구현 좁은 독립 검수

read-only 코드·시각 reviewer, 하위위임금지. 코드/spec/GitHub/서버 변경·커밋/push/merge0. 앞 맥락 파일에서 읽기.
대상 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app app/ 기존미커밋 위 상태박스 후속. 원천 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/status-box-code-brief.md, status-box-code-report.md, review-status-box-spec-report.md와 spec worktree SPEC003 개정③. 이전review-mobile-ui-report.md PASS(WARN4)·mobile-ui-fix1-report.md 후속미검수도이번판에포함.

이번코드변경은status-box-before-manifest.json·status-box-evidence/before-{board_screen,format}.dart.txt 대비확인. 목록 _nowBox 4상태만2줄(상태·시간/담당의 → 시술명 외N개), 단수생략·화살표없음, 경과mm:ss초갱신/60분이상누적, 완료lastSeconds÷60내림, firstdoing행title/time/doctor일치, done은집계제외, 비어있으면임의값없음. 서버long색/기존우선순위/현재타이머/API권한그대로. 호출박스/수락/귀가/상세/헤더변경0. 헤더가운데정렬은기록만.
코디 중간피드백 msg_32e7595777ed/mm:ss완료20분320폭말줄임과 msg_8ed594d80c62/doing담당의empty fallback도 최종 반영 확인. actualsim 첫카드의 state doing+doing행없음이면 시간/이름빈칸은 SPEC 빈값규칙대로이며 backendflow→state와task_state는별개(읽기코드근거). 서버새fallback정책추가하지않았는지확인. 기존로그인세션복원·실제local판조회는확인됐고로그인입력/업무조작은미실행.
직접열람PNG: 대기·마취진행·마취초과·마취완료·시술중 phone+iPad 대표, 320긴시술명외N개보존·상태시간가독성·담당의긴경우겹침0. 4행카드·4탭/원형DAY스타일유지. 새card미술만보지말고실코드상대표행/초갱신/빈값/null/60분형식도확인.
기존WARN4후속: calls[]카드정합/실호출카운트/호출·완료탭증거, 폰시트방·고객2줄, 320/599/600수락버튼·active시작 캡처(기존screens-fix1도읽기). probe200은인증통합아님·제품probe/ATS예외0·기존로그인보존·표준main재설치로그. 그부분코드확인만으로판단가능하면추가전체테스트반복불필요.
검증은좁은관문테스트1회 + analyze필요시. mobile전체test로그가최종수정이후통과인지확인. counts본인이재실행한것/보고만본것구분.
보고 profile review-status-box-code-report.md(PASS/WARN/FAIL·직접본PNG/실명령·직원실물에서만날자리·미검증실로그인명시). preambleID/outcome/report-path로worker_done한번후idle. 새변경요청/계약밖기능0.

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
