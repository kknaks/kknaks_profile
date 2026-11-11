# [planner] 권한문장 사실오류W1 최소정정

chat-permission-spec-wp-review.md W1과현재003/004diff읽기. 허용003U1괄호예/같은권한문장만·profilev8JSON Execution 추가연결·report chat-permission-spec-final-fix-report.md. 코드/GitHub/commit/push/하위위임0. 실제/me는세션도중staff비활성에도200인것이현계약이므로, /me401/403예를 '세션주인없음401·기존인증불가'로줄이고세션도중inactive/멤버십상실은004chatactor/stream403로막음·토스트/채팅목록비움이라고기존004기준한구절. 현재/me행동바꾸기/서버API/권한키/새UI문구0. board없음(/me200)엔셸/채팅/설정진입유지·board API/SSE/고객/통역0 그대로. 다른004명확화C-A1보존,000001002005동결.
추가실행상세만: v7 backend리뷰W2/W3로 day_vm optionalsecret2/Git금지키+diskwritablepersistent경계가필수마감임확인. 코디 delivery-request-v7-execution.json(기존v7contract불변·execution만) 만들었으니v8 execution에도해당code_surface/verification/rollback추가사항을보존(새사용자policy/API없음). 기존v8콜알림내용잃지말고추가3키그대로참조·v8고유내용유지, v7기준digest불변. 새v8계약/버전/baseline변경0. JSONschema/model최종1회0, lint/diffcheck/변경key보고. exactpreambleID/outcome/report worker_done1회/checkack후idle.

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
