# [mobile] 채팅 이식 코디 발견 누락 수정

기존v7app구현같은tree, chat-mobile-code-brief/report/최종WPv7·SPEC004@53adbd49·코디최신지시읽기. allowedapp/·profile chat-mobile-completion-fix-report.md/evidence만. backend워커진행중dirty건드리지않음. commit/push/merge/subagent0.

먼저독립적으로진행가능한것:
1) 네report §5 'DAY채팅탭엔연결줄없음'은SPEC004@53adbd49 W3정정과불일치. §3케이스매트릭스 :433는채팅화면머리아래SPEC003U12같은노란줄(처음서버연결중…/끊김다시연결중)을독립채팅stream기준으로보이도록명세. ChatState/Stream status를UI에잇고boardstream과혼동0, 원문글자그대로·신규문구0. 최초/끊김/복구테스트, 권한없는board와무관하게chatstatus동작. 코드contract새로만들지말고명시누락구현.
2) SPM Package.resolved 두개는실제공식전이의존 pin있음을코디확인했으니둘다커밋대상유지(프로젝트/워크스페이스빌드재현성). 실경로/키없음확인. README에채팅iOS의존/권한·서버API활성화전제·후속notification공통interface 간단기록가능.
3) iPad원형대조 pair가원형가로/DAY세로라정밀대조불가. 같은viewport의phone/iPad pair를재캡처(원형scratchcopy는원본repo수정0, 원천/출력경로보고). 대표목록·대화·시트·정보·전달·첨부/오류 최소. 사용자sim세션45031유지/uninstall/logout/실API쓰기0.

이어야할permission fix는문서리뷰PASS코디메시지를받은뒤진행(그전source편집은위1~3만):
- 같은병원활성직원전체·board무관채팅이확정돼있으므로 'Phase.forbidden에chatstate는있지만전체셸없어채팅진입불가'는v7결과미달. 코디가SPEC003모호문장을기존SPEC004뜻대로명확화중(chat-permission-spec-wp-fix-brief.md), 새정책/권한승인필요없음.
- /me200의유효활성직원인데 board권한만없으면authenticated셸/채팅/설정진입유지,시술현황영역에만기존권한없음안내. board API/SSE·고객정보/통역시작0·서버권한확대0. 실제/me403·직원비활성/세션무효는기존차단, chatforbidden과boardpermissiononly를근거없이같이취급해inactive사람캐시노출0. 구체Phase/소스별콜백은유지/분리하되공용세션401보호회귀0.
- 임의기능축소/다른모듈추가0·새UI문구0. 활성직원board없음→chat진입/전송UI가능·settingslogout·board네트워크0을실제위젯으로, 실제authforbidden은차단/캐시정리·늦은403/401세션교체보호검증.

문서PASS후최종테스트/analyze/native54+iOS unsigned/simulatorbuild(관련최종1회,소스미변화영역과거재실행무한0)·새PNG·세션보존설치. 전체test기준240, 수치정직갱신. 코드와새SPEC정합/원천기능누락0/기존시술현황회귀 및실서버11040채팅404pending구분. 정확preamble checkack/taskdispatch outcome/report worker_done1회후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_e8a8842c-a789-4862-93a5-7886d6bd1c61 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

