# [reviewer_doc] DAY 채팅 SPEC 독립검수

스펙 작업 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec. read-only, 하위위임·commit/push/GitHub·외부 코드/서버/DB 조작 금지. 보고서 하나만 프로필 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/chat-spec-rereview.md 에 작성한다.
먼저 해당트리 AGENTS.md의 문서/제품 규칙과 profile orchestration/roles/day/reviewer/ 지침, chat-spec-brief.md·chat-decisions-20261110.md·chat-spec-report.md 를 읽는다. 새 SPEC004(내부 채팅)와 기존SPEC003 채팅/D2 연결, SPEC000 device 최소개정, 인덱스/coverage 변경 전체 diff 검수. 후속 허용은 코디 메시지 msg_c7bb47e0e0e2: device 필수 메타데이터와 세션결속을 같은 단계에서 닫음. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, 프로토 /Users/kknaks/git/toy_pr2/cc-prototype 77173cf8b62f0b27ec54ec4ee22e9d308b7f701e git show 원문은 read-only.
사용자 확정: 프로토 채팅 디자인 그대로 DAY 색상/세션/병원·권한에 맞춤, 같은 병원 활성 직원 전체가 상대, 이번 세션 서버+앱 구현, iOS 우선·설정/서명/키 사용자, SPEC→리뷰→WP→리뷰→코드→리뷰, 기존 PR237하나/머지는 마지막. 자동 Android/전체알림센터/의사호출 정책 확장 없음.
검수: 원천 기능(1:1/그룹/초대·탈퇴/숨기기/음소거/읽음/수정삭제/전달검색/사진동영상·미디어모아보기/푸시·배너·배지)과 문구/폰·iPad 디자인 대응 누락/자의적변경0. API 계약 요청응답·UUID/seq/client_id/from_seq·에러·실시간재접속 복구·병원격리/세션교체·동시성·권한·정합 확인. 서버가 테이블만 존재하므로 제안계약과 현재구현 구분. SPEC000과 충돌/숨은데이터모델변경(특히 device 환경/앱id/동일계정 다중병원·APNs)을 확인. 채팅 push를 D2핑계로 제외하지 않으며 플랫폼 실키 부재는 별도 사용자설정이지 구현무능으로 둔갑 금지. DAY-ESC001 등 기존미결을 자의적승인/구현금지로 만들지 않음. 실제 미결과 개발시 선택 가능한 구현상세 구분. 최소 인수조건이 앱·서버에서 검증가능한지 확인.
판정 PASS/WARN/FAIL, 지적당 파일:줄/원천근거/영향/최소정정안. lint-pipeline.py --strict 1회 products/day ERROR0, 타제품기존은분리. git diff --check 및 경계 검수. 새 WP나 코드 수정 금지. 최신 preamble exactID/handle 권한과 check/ack 후 worker_done 한 번(--outcome succeeded/failed, 실제 --report-path), 완료후idle.

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

추가 집중: 코드 AGENTS는 repository층 없음(서비스가 SQLAlchemy 세션 직접사용), SPEC에 Repository를 도입한 듯 오기 없는지 확인. 기기 구세션 delayed PUT/DELETE가 신세션 등록을 덮거나 삭제하지 않는지 API에 명확히. migration 과거행은 nullable 등 안전한 전환·미결속행 발송 제외/재등록으로 활성 계약이 가능한지.

## 이번 재검수 범위
이전 chat-spec-review.md + chat-spec-fix-brief.md + chat-spec-fix-report.md 읽고 W1~3 및 코디 후속(device 구PUT+namespace/동시보장, 삭제행포함멱등·멱등반환병원검증, PHPhotoLibrary키,004stable/index)이 실제문장으로 해결됐는지 좁게검수. 새정책0/기존API권한·UI회귀0. 원천전부 처음부터 다시조사하지 말고 바뀐절과연결되는근거만. 보고서는 chat-spec-rereview.md.
mobile-deployment 후속 참고는 코디가 실제확인: 현재 :134는 「권한(알림·카메라·사진 등)은 그 기능이 앱 범위에 들어올 때만 켠다, 범위는스펙」이라 새채팅범위와모순없음. '알림마이크만이라문서갱신필요'라고미확인가정으로범위확대하지말고 사실확인.
기술적불변식을구체구현테이블명/락전략까지SPEC에서정하라고요구하지않는다(WP몫). 다만관찰결과보장할수없는모순있으면근거지적. lint strict는최종본1회, 경계확인. 최신preamble exactID/outcome/report worker_done1회후idle.
