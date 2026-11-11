# [reviewer_doc] 채팅 Delivery235 v7 독립검수

read-only. 하위위임·SPEC/JSON/코드·GitHub·DB·commit/push/merge 수정0. 보고서 하나만 profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/chat-wp-review.md.
스펙 tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD53adbd49126c12c887b897854107aa7310cc4f75, 코드tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEADb6c034bf. 각AGENTS/mediness delivery-workflow/document-pipeline/역할지침 읽고 profile chat-wp-brief.md/chat-wp-report.md/delivery-request-v7.json을 v6/approvedresult, SPEC004+000device+003+001, 사용자chat-decisions-20261110.md/research/chat-spec-rereview와 대조.
판정대상: 같은issue235/keyday/day-app·v7정확1증분·L3·canonicalmain9692baselinepending정직·implementation근거reviewed53adbd49·한codePR237/dev/merge사용자마지막·iOS우선·기존프로토디자인/문구·병원활성직원전체·서버도이세션 계약/AC/code_surface/review_surface/실행계획정합. 임의feature축소·OQ핑계채팅push제외0, Android/전체알림센터/원장호출발송을몰래확대0. 코드후키/Apple설정사용자/실기기pending과mock만완료를분리. PG/Redis 실제통합/단위와앱시각검증·native빌드, 서명0. 이전v6범위 app/만/자리만/API0/권한알림마이크만/새APIs없음 문구가v7과충돌하지않는지.
안전집중: 병원격리(멱등응답도), clientId삭제행/동시성/초대경계/첨부MIME·Range·임시파일·선택흐름, 재접속since변경유실·세션폐기·다기기읽음, device구PUT/DELETE·tokennamespace원자성/APNs실패와퇴사·바인딩/토큰교체경합. 구체락전략은execution으로검증가능해야함. rollback은failclosed·데이터삭제0·데모email비우기prod failopen0.
옆migration0006 원천byte/hash+EventLogIndex 최소의존반영안과0007 한head가실행가능한지 read-only 실물 확인. 옆전체branch강제merge/dev선머지/임의downrevision/미검증두head방치 금지. sharedspec30work상세원장발명0, JSON만CLI입력.
JSON schema/model실검증1회 errors0, scope/mapping·누락·모순 판정 PASS/WARN/FAIL 각파일:줄+영향+최소수정안. 근거없는추가승인/미결양산0. 실제검증안된것은pending표기. 최신preambleexactID/outcome/reportpath worker_done1회, checkpoint/완료전check/ack, 후idle.

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
