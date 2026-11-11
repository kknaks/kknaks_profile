# [backend] DAY 채팅 서버 구현

WPv7 독립검수/CLI승인결속 뒤에만 발주한다. 발주 포인터의 최종 request/approved-result/리뷰를 읽고 exact계약 우선. 이 브리프 초안의 경계가 WP와 다르면 코디에게 질문. 하위워커/subagent 위임·commit/push/PR/merge 금지.
작업코드 tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD b6c034bfa239bd4f12f1a29c6e58c74d82c87de6 · branch kknaksss/day-app · targetdev(사용자지시전머지0). 루트AGENTS 및 거기 연결된 개발/백엔드안전/테스트지침과 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/ 역할을 읽는다. 사용자 이번확정으로 app/only의 채팅서버 예외확대. 앱워커는동시에app/만편집한다. 서로 dirty정리/stage/reset0.
스펙 read-only /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD53adbd49126c12c887b897854107aa7310cc4f75 SPEC004전문+000device/채팅모델+003push+001auth, profile work/day-app/chat-decisions-20261110.md/research-chat-notifications.md/chat-code-baseline.md/chat-wp-report.md/최종WP리뷰. 프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype pinned77173cf8b62f0b27ec54ec4ee22e9d308b7f701e git show의 procedure/back/app/api/chat.py·schemas/chat.py·service/chat.py·repository/chat관련·push/apns·사진동영상흐름·tests 참조. 현재checkout낡음/checkoutpull편집0. 앱원형기능의서버행동을DAY계층·UUID/seq·병원세션·활성직원에맞춰이식, 프로토repo층을복사하지않음(서비스가SQLAlchemy직접).

범위=최종WP code_surface의 backend(HTTP20+채팅전용SSE6+기기PUT/DELETE+APNs채팅+첨부디스크/Blob+서비스/쿼리/DTO/schema/에러/모델/증분migration/task/라우터등록/테스트), 서버설정예시·compose전달·uvdeps/lock/필요개발문서만. app/·웹frontend/templates/static/styles/board라우터·API/스냅샷·EMR/KOS/실env/실키/배포/DNS/다른세션tree금지. 사용자실제port11040/day-local서비스와DB/프로세스재시작·중지·migrate·seed 금지. 비밀파일읽기출력0, 테스트는기존하네스의로컬스크래치스키마·합성계정/병원/파일만, 운영·공유STG0. 변경이필요하면코디에게근거질문.

핵심계약: 같은병원활성직원전체, 비밀번호/board권한무관, account+staff활성·병원멤버십. UUID·roomseq/clientId·from_seq 경계·재초대옛대화없음. 1:1병원별unique/그룹20/초대·나가기·숨김·음소거·조회50·모아보기60·읽음단조/수정삭제·전달10부분실패·첨부제한/원문오류·API응답명 정확. softdelete clientId재시도도처음row(새메시지/이벤트/push0), 모든멱등리턴에도병원/멤버/경계검증. 클라이언트가보낸병원·계정·작성자·세션을신뢰0.
동시성불변식 실제PG로: roomseq배정+message+read+last_message_at 한tx/rowlock, directunique경합, clientId삭제행포함조회와동시생성보호, 첨부한번붙기/전달·삭제시파일마지막참조경합. DBquerycount/eagerload로N+1차단. ORMmodel day밖노출0, repository층0. 정확이벤트payload6종+권한분리전용stream, Redis프로세스간전달, commit뒤만발행(실패메우기가능), 중간세션폐기/직원비활성화/병원전환이면stream민감데이터0, 재접속since수정삭제유실0. SQLAlchemy한세션동시task공유0.
기기: SPEC000서버세션결속·구PUT무시/구DELETE새binding안삭제·동률고정순서·tokennamespace(platform/app_id/push_env/hash) 원자적하나/다른namespace불변·옛nullable행발송제외/토큰암호화·허용appid검증. 채팅push대상은원천정확히·같은병원현재유효기기/토큰교체/퇴사·mute 재검증, idempotency중복발송0, 만료/영구오류토큰비활성화가새등록지우지않음. APNs HTTP2/JWT 설정실키없으면발송skip·대화성공/감사기록정직, timeout/retry/concurrencybounds/cancel/작업중복안전. 원장호출발송/알림센터/FCM·Android추가0(기존원장호출API상태·수신자정책회귀0).
첨부: Blob(서버)/디스크(로컬) 기존아키텍처, 공개/서명URL로권한우회0·Bearer프록시/no-store·MIME실체검사·용량넘김boundedread·Range206/416/Content-Length/HEAD정합·경로탈출0. 큰videoeventloopblock/전체메모리적재0, 임시파일취소오류정리·삭제/전달참조안전. OS/파일I/O·SDK는async또는boundedworker, DBtx외부I/O기다림금지. 출처/공식SDK문서·버전lock기록(azure-storage-blob/APNs등).

migration: 착수최신dev·옆종료PR상태를확인. WP최소안=옆0006 파일byte/hash불변+같은EventLogIndex선언만의존으로가져오고새0007을잇는것(원천fb0351828664e0e709ab56fa962bc31151f5ae905fe24b9d7a17c6b7b50e0739), 또는동등검토된한head안. 옆tree/원천0006편집/전체feature강제merge/두heads방치0. 필요enum/modelnullable칸과snapshot/index실제PG증명. 과거데이터삭제/바꾸기0, 운영downgrade0. 새설정은placeholder예시+compose local/server API/worker전달·미설정failclosed를테스트/문서로검증, 실제env수정0.

검증: baseline code496notinfra/기존full663(신채팅근거아님) 위 새핵심unit·API/PG·Redis E2E·실제constraint/lock/upgrade/downgrade·한head·architecture·ruff. 기존 scripts/test.sh는스크래치테스트스키마만쓰는지확인후사용, 없거나위험하면코디질문/사유pending; 업무DB쓰기로우회0. mock은APNs·Blob외부경계만, 도메인mock완료금지. 합성두병원/다중병원계정/여러직원으로HTTP20+SSE6+로컬첨부+기기경합+push더블 endtoend필수. 키/APNs/Blob실물미실행과코드/로컬테스트완료구분. 테스트통과후반복0, 새실패/변경후필요만. 중요한설정누락compose검증(과거D1 env전달F1회귀) 포함.

산출 profile work/day-app/chat-backend-code-report.md 와 필요한 chat-backend-evidence/로그. API별구현·원천·tests/핵심경합·검증실명령수치·기존회귀·설정키이름/사용자후속·미실행정직기록·앱전달필요사항. private본문/계정·토큰출력0. WP/SPEC밖계약변경발견시코디질문. exactpreamblecheck/ack heartbeat cadence/worker_done outcome reportpath1회후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_bdc96429-0e21-4311-bca9-622e97ece387 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

## 발주 확정(사용자 승인 후)
WP=delivery-request-v7.json, 승인=delivery-v7-approved-result.json 및 delivery-v7-plan-approval.json, 최종WP리뷰=chat-wp-rereview.md. 사용자 「코드 구현 하자」. canonical main baseline pending은사용자마지막merge순서때문이며-reviewed 미머지SPEC53adbd49로지금구현(선merge요구0). 후속알림SPEC은사용자병행요청으로다른planner가005만쓰며003/004/000/001은동결, 코드계약변경없음. 알림함/원장호출발송로직은005후속WP전까지이코드발주범위밖, 그러나공유기기등록/APNs를재사용할수있게구조유지. 코디에게필요공유interface파일/구현선택을보고. 테스트하네스는기존승인된로컬스크래치환경의프로그램적설정주입만사용가능, env/키값모델출력·업무DB변경0.
