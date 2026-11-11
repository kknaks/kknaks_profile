# [planner] DAY 내부 채팅 SPEC 초안

## 1. 역할·읽을 것
이전 턴 맥락에 의존하지 말고 이 브리프부터 읽는다. 코디는 orchestration/runbook.md 절차를 따른다. 너는 planner이며 하위 워커·내부 subagent 위임 금지. 역할 문서 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/ 아래 지침을 읽는다.
스펙 작업 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec HEAD 06239a1c7d45e95a02e5aab61b9d29bea6b7aca3, origin/main 9692e1fb461bf8c4e52bf489e37ab8ff875f9918. AGENTS.md → context/manifest.yaml/index.md/current-state.md → rules/document-pipeline.md/delivery-workflow.md, products/day/README.md/20-spec.md/30-work.md 순서와 관련 하위 규칙을 읽는다.
코드 read-only /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD b6c034bfa239bd4f12f1a29c6e58c74d82c87de6 의 AGENTS.md · auth/session · model misc/enums · default_permissions · 앱 구조도 읽는다.
프로필 절대 루트 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck. 여기 orchestration/work/day-app/research-chat-notifications.md 와 _RESUME.md를 읽되 과거 기록보다 이번 브리프/사용자 최신 지시 우선.

## 2. 사용자 지시·결과
사용자: 내부 채팅은 기존 프로토 앱 채팅을 그대로 옮기고 DAY 권한 등 일부만 수정, 디자인 최대한 유지. 마지막 승인: 「응 일단 채팅 기능 스펙부터 앱 구현 까지 진행하자」. 채팅에 초점. 알림센터 전체나 Android 앱 신설까지 자동 확장하지 않는다. 현재 iOS 개발버전 우선·플랫폼 등록/서명/TestFlight/실제 키는 사용자. 스펙→독립리뷰→WP(기존 GitHub #235 업데이트)→코드→독립리뷰. 코드 PR237 하나, spec PR921 이어 사용, 머지는 마지막에 사용자 지시 때만.
이번 발주는 SPEC 단계만이다. SPEC-004 번호 사용 가능 여부를 확인하여 내부 채팅 전용 상세 SPEC을 draft로 작성하고 SPEC003 채팅 자리/범위와 최소 연결한다. 기존 SPEC000 데이터 모델·SPEC001 세션·SPEC002 병원 권한 계약을 바꾸지 않는다. SPEC index와 Spec Coverage 최소 동기화 허용. WP request/코드 생성은 아직 하지 않는다.

## 3. 원천·이식 범위
프로토 /Users/kknaks/git/toy_pr2/cc-prototype 는 read-only. 반드시 pinned git ref 77173cf8b62f0b27ec54ec4ee22e9d308b7f701e 의 git show로 읽는다. 로컬 checkout dbf0b53은 오래되어 채팅 없다. checkout/pull/편집 금지.
원천 procedure/app/lib/chat/{chat_link,chat_model,chat_search,chat_state,chat_ui,chat_view,photo_pick,video_pick}.dart, screens/chat_{list,room,info,new,attach_sheet,forward_sheet,media,photo,video}_screen.dart, chat_app1~7_test.dart; procedure/back/app/api/chat.py/service/chat.py 및 관련 attachment/push/SSE. 실제 원문 기능/문구/상호작용을 조사하여 근거 파일/ref/줄 매핑. 원천 SPEC007 원문은 경로 미확인: 없는 내용을 인용하지 않는다.
방 목록·1:1·그룹·초대·나가기·숨기기·음소거·읽음/미읽음·수정/삭제·전달·검색·사진/동영상/뷰어 등 기존 기능을 멋대로 줄이지 말고 원문 동작을 계약화한다. 어떤 검색이 로컬인지도 원천대로 확인. DAY 4메뉴 중 채팅 슬롯 사용, phone/iPad와 색상/타이포만 DAY 기준. 새 화면 문구 창작 금지, 기존 문구 명시적 출처. 원천 디자인을 다시 설계하지 않는다.
서버는 채팅 테이블만 있고 API0인 사실을 정직하게 밝힌다. 앱 구현을 위한 HTTP/SSE/첨부 업로드다운로드 계약도 이 SPEC에 구체화한다(실제 현재 구현인 것처럼 쓰지 않는다). API 프로토 endpoint/요청/응답과 DAY UUID/seq/병원/세션으로 바뀌는 필드 매핑. 데이터모델 from_seq, last_read_seq, direct_key 병원내 unique, client_id idempotency, soft delete, 탈퇴/재초대 경계/권한/원자성/동시성은 원천과 DAY 모델을 대조한다. 기존 이벤트 통로를 쓰는 방식/재연결 누락 복구/다중 기기 읽음·캐시·병원변경·로그아웃 격리 계약 포함. 외부URL로 Bearer/첨부 유출 금지, 인증과 병원 멤버십 서버 검증.
채팅 push/탭 배지/앱내 배너/알림클릭 방진입은 기존 원천 동작으로 정리하되 기기 API/APNs 발송 서버 미구현 D2와 의존성을 구분. 이 발주가 Android·FCM통일·원장호출 수신자 정책·상담사 호출·알림센터 전부 구현 승인은 아니다. 사진/동영상 저장소와 제한값은 원천·현행 DAY architecture 근거를 확인하고 미정이면 실제 OQ로 남긴다. DAY-ESC-001은 보관/열람 미결 추적이지 자의적인 구현 금지/새 승인 절차로 만들지 않는다.

## 4. 사용자에게 질문한 실제 미결(회신 전 제안/확정 구분)
코디가 async로 두 가지를 질문해 회신 대기 중이다. 초안은 독립적으로 진행하되 아래는 확정했다고 쓰지 말고 제안/OQ로 표기하고 보고한다. 코디가 회신을 전달한다.
1) 같은 병원의 활성 직원 전체가 1:1/그룹 대화를 할 수 있도록 할지 vs 직무별 제한. DAY 병원 격리/활성 멤버십은 기존 계약, 채팅 권한 배포정책은 아직 회신 전. 프로토의 active+password 조건은 KOS에 부적합하므로 그대로 금지. 제안은 board 권한과 독립인 같은 병원 활성 직원 전체, 임의 chat 권한 키를 기존 결정으로 발명하지 않는다.
2) 서버 API를 이 세션 backend 워커가 구현할지 vs 옆 백엔드 세션이 구현할지. 앞서 app/만 허용했던 경계 때문에 코디가 질문한 것. 지금 서버 구현 담당 확정/코드 변경은 하지 않는다. 스펙 계약 작성은 가능. 개발 완료/실기기 push 검증 등 미실행 결과를 완료로 쓰지 않는다.

## 5. 편집 경계
허용: products/day/20-spec/spec-004-internal-chat.md(번호 확인 후), products/day/20-spec/spec-003-mobile-app.md의 채팅 연결만, products/day/20-spec.md 인덱스, products/day/30-work.md Spec Coverage 최소 행. 새 SPEC ID 다른 번호 필요시 먼저 코디 질문. 보고서 orchestration/work/day-app/chat-spec-report.md 1개. 그 외 문서/코드/backend/배포/DB/실제 env/비밀/GitHub/commit/push/merge/사용자 시뮬레이터 세션 조작 금지. 기존 UI005·auth·board 동작 보존. 트리 변경을 경계 넘어서 정리하지 않는다.

## 6. 검증·산출물
상세 SPEC(근거+UI와이어프레임+API+에러/격리+상태+인수조건+실제 OQ)과 보고서. lint-pipeline.py --strict 1회, products/day ERROR0(전체 무관은 분리). git diff --check, 편집 경계 확인. 보고서는 원천 기능 대비 누락0 매핑, 서버와 앱 구현 의존, 사용자답 필요한 것, 확인 불가 원천을 구분. WP 발주나 코드작업 앞지르지 않는다.
최신 Orca preamble의 exact task/dispatch/handle이 lifecycle 권한이다. 아래 구형 템플릿 명령에 --outcome succeeded/failed · 실제 --report-path와 --files-modified를 추가하고 worker_done은 단 한 번만 보낸다. 체크포인트와 완료 직전 check/ack로 코디 후속지시를 읽는다. 완료 후 idle.

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
