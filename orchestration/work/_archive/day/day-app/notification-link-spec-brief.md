# [planner] 알림005↔모바일003 후속 연결 정합

환경지침기존동일. SPEC tree HEAD0d0ba25f3df50d87c70ece8f7a5ac4362b475173, 알림005 재검수PASS(notification-spec-rereview.md), 최초003/004채팅계약53adbd49. notification-spec-report/fix/rereview의「다른SPEC후속패치목록」만 적용.
코디의독립병행방법정교화: 채팅code워커2명에게 msg_d68d00cbe6ea/msg_b5ed8820a69e로 계약원천을git53adbd49의003/004/000/001에계속핀한다고안내완료. Gitobject는불변이므로 workingtree003의알림연결만동결해제해도v7코드계약은변하지않는다. 이에기존005의 '채팅동결해제뒤'는이번workingtree003알림연결범위에한해충족. 채팅코드자체/API/authority타입변경X, 후속005구현WP전까지알림코드아직0.
편집허용 spec-003-mobile-app.md의알림연결만(U2종/§1알림범위/U16설정/D2원장호출발송·D5알림함/A26/OQA19), spec-005-notifications.md의선행조건완료/연결소유정합만. 다른003시술현황/채팅/세션/API/role/문구·004/000/001/002/index/coverage 코드/WP/GitHub/commit/push/merge0. 보고 profile notification-link-spec-report.md 하나.
의미: 종배지/목록/설정알림칸/원장호출발송 계약소유=005, 기존기기등록/APNs공유통로=004/v7. 003의 '미구현/배지없음/계정로그아웃만'절대문장을 005이전단계로한정하고 005구현뒤해당계약이적용됨을 명시(지금코드완료주장0). 003v7채팅은그대로. 알림005statusstable보존/신규기능문구발명0. 다른SPEC000schema/tokens수신자정책0변경.
검증gitdiffcheck/lintstrict최종1회DAY0, 000/001/002/004 git53adbd49blob동일증명. 원천005리뷰통과내용재설계0. 변경절·이전/이후·코드범위미변경·미실행정직보고. 정확preamble/outcome/report worker_done1회checkack후idle.

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
