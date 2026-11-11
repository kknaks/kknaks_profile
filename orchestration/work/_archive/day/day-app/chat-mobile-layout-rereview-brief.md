# 채팅 앱 W1 후속 독립 재검수
너는 기존 backend 독립리뷰어며 app 작성 참여0이다. 이번 read-only 앱 재검수 대상은 chat-mobile-layout-evidence-report.md의 새 변경(키보드 viewInsets 원형 복원, 긴 직무명 헤더 폭, 가로/긴문자/키보드 증거)뿐. 기존 전체 app 검수는 chat-mobile-review.md PASS/WARN1로 완료, 전체 서버 코드 검수도 완료. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS.md, 역할 reviewer, SPEC b0f71ec3 003/004, 앞 두보고를 읽고 실제 diff와 PNG를 검수해라. 브리프는 1장이고 보고에 링크된 증거는 근거자료다.
원형77173cf8 read-only gitshow로 키보드 viewInsets 처리 대조. 폰 가로844x390, 폰 키보드 열림(입력창/메뉴가 위에), iPad 키보드, 긴 직원명/그룹제목/자유직무명, 전달시트 필수버튼 접근·스크롤을 실제PNG와 관련 테스트로 확인. 임시 debug e=null 등 예외 숨김/overflow무시가 남아있지 않은지도 확인. 테스팅은 제품 경계 의미를 보장, 기대값으로 버그를 숨기지 않는다. 관련 집중 테스트 및 analyze만(전체245·native·build 무의미 재실행0). 제품코드 변경 전후 기저캡처/시술현황 셸/모달 회귀 확인. 실제 시뮬레이터·실계정·DB·서버 조작0. app 코드 수정0·commit/push/하위위임0. 발견시 file:line·재현·최소정정만 보고.
최종 chat-mobile-layout-rereview.md / 검수파일hash / 명령결과 / FAIL·WARN 및 실기기·라이브pending 구분. 새 lifecycle preamble IDs, --outcome succeeded/failed 및 --report-path 실제경로 포함하여 완료보고 1회 후 idle.

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
