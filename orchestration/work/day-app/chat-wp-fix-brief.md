# [planner] WPv7 WARN 정정

profile work/day-app/chat-wp-brief.md/chat-wp-report.md/chat-wp-review.md 및 delivery-request-v7.json 읽기. 같은환경/지침/스펙53adbd49 유지. 편집허용 profile delivery-request-v7.json + chat-wp-fix-report.md만. SPEC/코드/GitHub/commit/push/merge/하위위임0.
리뷰 W1~W4 전부최소정정: rollback migration없음옛문장범위+forwardonly파일0006/0007보존(기능코드만revert), APNs재시도·죽은토큰원천77173cf8 push.py28~31/286~306 고정·기존status skipped_no_key/token_removed사용·키없음은메시지전송실패아님·토큰무효는송신시점binding/token동일할때만해제하여새토큰등록보존, A13/verification 누적v1∪v7범위, constraint need→현재SPEC003목록. 참고phase번호정정. 새제품정책0.

코디추가 실행파일경계만명확화(Contract새기능아님): code_surface에 backend/day/schemas/devices.py·enums/misc.py(기기enum필요시)·day/errors.py·main.py 또는 runtime조립실제등록경로를 현코드읽어정확히허용; app native새파일+Xcodepbxproj소스등록·theme/format/widgets재사용/README필수내용도 기능경계내허용. 앱은app/만이라는큰경계를좁은임의파일목록때문에편법으로우회하지않게. backend tasks 등록/Runtime/APIrouter 실제조립위치확인, server compose.yaml api/worker/scheduler 설정전달도 local뿐아니라필수경계있으면예시이름만명시(실설정/기동변경0). tests/architecture·migration·컬럼snapshot 검증에필요한실제test경로허용. common다른패키지업무코드확장0(현재WP common/config의설정만예외).
rollback/인수조건/범위체크에추가경계반영. 공식doc참조/lock/실키사용자/스크래치E2E/한codePR237/dev·merge마지막/baselinepending/targetspec4/version7 유지. JSONschema/model각최종1회 오류0, 수정key 목록·전후매핑 보고. 마지막check/ack+worker_done exactID outcome/reportpath1회후idle.

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
