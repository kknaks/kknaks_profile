# [reviewer_doc] 채팅 UI 진입 기존권한 문장·v8W1 검수

read-only/하위위임·commit/push/코드·GitHub0, report profile work/day-app/chat-permission-spec-wp-review.md. spec tree HEADb1260dd2 위미커밋003/004, profilev8request만. 관련AGENTS/규칙/역할기존유지. chat-permission-spec-wp-fix-brief/report +mobile-code-report §3·§7, 기존사용자같은병원활성직원전체·board무관 chat확정/기존004정책/notification-wp-reviewW1 대조.
검수대상: 003U1/SSE403매트릭스/A1 및004C-A1 한구절이 /me200활성직원board권한만없음이면시술현황메뉴본문만권한없음·셸/채팅/설정허용으로명확화되어있는지, 실제/me403인증/직원비활성/멤버십상실은기존차단·셸없음 유지. board API/SSE·고객정보/통역권한확대0/새authcode/API/key/화면문구0. 새정책/새유저승인아닌이미확정된004board독립UI진입의003모호문장정합. 서버권한우회0·세션401보호기존. v8 deps2W1boardbackend업무규칙/스냅샷/응답무변경+호출커밋뒤알림hook예외 한정 +deps17원천커밋후갱신기록만, 다른v8내용회귀0/schema/model정합.
lintstrict최종1회DAY0/diffcheck·000001002005blob b126동일. 결과PASS/WARN/FAIL fileline·근거·모순재검수, 정확preambleworker_done/checkack후idle.

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
