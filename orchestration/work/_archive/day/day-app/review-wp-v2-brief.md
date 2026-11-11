# [reviewer_doc] DAY 앱 WP v2 독립검수
역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/ 문서와 mediness AGENTS.md/Delivery workflow를 읽는다. 대상 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec. 앞 맥락은 파일로 복원. 하위워커/내부서브에이전트 금지.

## 1. 원천
profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ 안 wp-v2-brief.md(현재계약), delivery-request-v2.json, planner-wp-v2-report.md, delivery235-current.json(v1현재), delivery-request.json(v1), _RESUME.md, review-ui-spec2-report.md. SPEC003 exact1551fa22 전문 및SPEC001. 최신origin/main exact3f57c1af…와준비된로컬SPEC를구분. 옆세션 day-procedure-board-2/_RESUME.md와그spec/code트리 read-only로호환표근거확인.

## 2. 검수목표
기존#235 누적계약version2이며UI교정13항목+기존로그인/세션/SSE/푸시/통역클라이언트회귀보존. 원장즉시본인/간호대리, 4메뉴/알림/설정계정, 4필터·4행카드·마취·목록수락·시술상태/더보기·호출시트·전체완료·통역드로어/TW·성공토스트/토스트되돌리기없음이Acceptance에빠지지않음. 과거155/47/663검증이새UI완료로기재되면FAIL. 이번후속변경app/만, 기존PR의D1유지·새backend/웹수정없음. 코드PR237하나·모든merge사용자지시만. D2D3D5서버신규범위밖. 새문구/번역/API발명없음. OQ보류정확.
옆세션의새업무동작(재호출·취소모달·need·반복마취·원장변경)이앱003과다르면구체source/sha/줄+정합dependency로기록. 충돌을숨기거나새업무규칙을WP로덮어쓰지않음, 해당구현전spec정합·서버합류확인이선행이라는표시. WP작성자체를막는과도한gate/선머지강제없음.
계약version2·sameidempotency·scope_delta·fullSHA/실제mainbaselinepending·riskL3누적보존, stalev1승인복제금지. 기존승인으로새계약승인주장없음.

## 3. 산출물
profile작업폴더 review-wp-v2-report.md 한개만생성. PASS/WARN/FAIL 각지적json경로+SPEC근거+수정방향. 13항목커버표/기존회귀/옆세션정합의존목록. 실제schema검증+JSON파싱. 코드테스트/빌드/lint반복없음. 스펙/코드/GitHub/입력JSON수정금지. CLIapply/승인receipt/커밋/push금지. 수정은원planner에게돌림.

## 4. 완료
livepreamble우선. 마지막메일확인후worker_done한번, idle. WP리뷰만이며코드구현착수아님.

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
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
