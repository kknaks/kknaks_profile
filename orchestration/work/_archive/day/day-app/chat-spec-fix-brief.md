# [planner] 채팅 SPEC 리뷰 정정

이전 맥락 대신 chat-spec-brief.md·chat-decisions-20261110.md·chat-spec-report.md·chat-spec-review.md 및 현재 5경로 diff를 읽는다. 작업 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec, HEAD06239a1c 위 미커밋. 해당 AGENTS/문서규칙/역할 유지. 허용 SPEC004 신규, SPEC000 device 절만, SPEC003 채팅/푸시/권한 연결만, 20-spec.md index, 30-work.md 최소coverage. 보고 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/chat-spec-fix-report.md. 코드/WP/GitHub/commit/push/merge/하위위임0.

필수 W1~3 전부 최소정정: 이벤트는 6종, SPEC003 권한문장+AC A17에서 채팅카메라/사진보관함 SPEC004 연결, 채팅 끊김은 기존DAY 노란줄/동일원문 「연결 끊김 · 다시 연결 중」을 사용한다고 단일화(프로토 공용판스트림 줄을 DAY 채팅독립스트림에 연결하는 정합이며 새문구없음).

코디 후속 정합 두 건도 같은 리뷰대상으로 명확히(사용자 제품정책 확장 아님):
1. device 구세션 늦은PUT가 새로그인 등록을 덮지 않는다. DELETE 요청세션일치 보호만으론 부족. 등록은 현재 binding 보다 먼저 만들어진 로그인세션 요청이면 binding/token을 변경하지 않는 서버검증 불변식을 API/모델규칙/AC에 추가. 동시등록도 같은결과(서버 신뢰 세션 생성순서/동률 안전판정 등 구현은 WP, 임의사용자문구나클라이언트가보낸세션id 신뢰0). 같은세션 토큰갱신은 정상. 요청실패일반처리/무시응답은 기존API계약에 맞는 최소한 결정하고 결과를 보고. 미확인 서버없는권한을 첨부하지 않는다.
2. 같은 APNs 토큰 연결 유일성은 platform+app_id+push_env+push_token_hash namespace 안에서 원자적으로 보장. 다른topic/환경의 같은토큰문자열행을 해제하지 않는다. hash 단독 비유일색인으로 동시PUT보장했다고 쓰지말고, 보장되는관찰결과 명시(구체잠금/부분unique전략은 WP). 이미삭제한메시지 clientId 재전송은 새메시지/이벤트/푸시 안 생기게 삭제행 포함 멱등성을 명확히; 원천동작 바꾸지말고 DAYlive_unique주의보완. 기존 SPEC004 API 모든방/메시지/첨부는 병원검증이 멱등응답반환에도 적용됨을 한 구절로 보완.
review 참고4 PHPhotoLibraryPreventAutomaticLimitedAccessAlert=true는 프로토 최근사진/더고르기 권한흐름의 일부로 UI동일이식에 포함할지 명시. doc_no DAY-DOC8은 다른spec tree PR920 포함중복을 read-only확인해 없으면 사실만보고(번호를임의로바꾸지않음).

status: 사용자 채팅전체구현·같은병원활성직원·서버이세션 확정 + 이번정정은동일계약이므로 최종독립재검수 대상에서 SPEC004를 stable로 정리(index동기). SPEC000 기존draft를 전체stable로 바꾸는 범위확대0. canonical main baseline은 계속pending, 머지없음. SPEC003 기존stable보존.

lint strict 각최종변경후1회 products/day ERROR0(무관stderr출력은별도로그에저장/요약만), git diff--check, 변경경계. before/after/근거/새정책없음/정직미결 보고. 정확preamble task/dispatch/outcome/report-path worker_done1회, 완료전check/ack·후idle.

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
