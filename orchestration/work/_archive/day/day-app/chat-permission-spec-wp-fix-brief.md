# [planner] 구현발견 채팅 진입 권한 문장 정합 + WPv8 W1

spec tree HEADb1260dd2, 기존AGENTS/문서/역할지침. 읽기 chat-mobile-code-report.md §3·§7, SPEC004 권한(board무관·같은병원활성직원전체)·사용자chat-decisions-20261110.md, notification-wp-review.md W1. 기존SPEC003 U1:182는board권한없으면시술현황대신권한없음이라고썼으나앱이그것을전체셸없음으로해석해활성직원이채팅탭진입불가. 사용자결정/SPEC004가정본이므로정책새로정하지말고003의적용범위를명확화.
편집허용 SPEC003의U1권한없음·필요연결매트릭스·A1 등동일모호문장만(시술현황영역에만권한없음표시, /me200유효활성직원은셸·채팅·설정진입유지; board API/SSE/고객정보·통역은권한없으면안엶). 실제인증불가/직원비활성/병원멤버십상실(/me실제403 등)은기존권한없음/인증실패처리유지, 채팅무관정책으로보드/환자정보권한확대X. board서비스만forbidden이면그영역차단, authstaff불가와구분. 서버새code/API/권한키추가X. 필요한SPEC004 UI진입연결한구절/AC만같은뜻으로보완가능(이미명백한부분재설계0). 현재v7구현권한의해석정정이지신규결과계약아님(워커에게코디가approvedpatch후알릴것).
추가WPv8리뷰W1: delivery-request-v8.json execution.dependencies[2]의board backend무변경을업무규칙/스냅샷/응답무변경+v8커밋후알림훅예외로한정. 다른JSON변경은새SPEC원천sha코디커밋뒤갱신대상이라는정직연결만(직접미래hash생성X). v7입력immutable수정0·v8version8유지·scope확대0. JSONschema/model최종1회ERROR0.
허용문서003/(최소004)·profile v8JSON·chat-permission-spec-wp-fix-report.md. 000/001/002/005·다른index/coverage·코드/GitHub/commit/push/merge/subagent0. 원문권한없음글자기존그대로,새UI문구0. lint/diffcheck·권한표/시술현황/세션인증·API불변증거. 기존checkbox/minorOQ양산0. 정확preamblecheckack/outcome/report worker_done1회후idle.

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
