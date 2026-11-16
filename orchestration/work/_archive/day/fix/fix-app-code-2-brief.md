# [mobile] fix 코드 2 — WP-APP-3 채팅 화면(길게 누르기 자리 · 하단 탭 숨김 · 읽음 표시)

너는 **day `mobile` 워커**(WP-APP-1 · APP-2 · 수정 1 을 한 같은 터미널)다.

- **작업 계획**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` — 「WP-APP-3 채팅 화면」 · §3 「읽음 계약 표」 · §4 순서
- **계약의 SoT**(미커밋 스펙): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` 개정 ④ — U-2 「하단 4메뉴 숨김」 · 「메시지별 읽음 표시」 · U-4 「자리가 맞아야 한다」 · §3 `Member` · 실시간 `chat_member_read` · C-A16 · C-A22 ~ C-A25 · OQ-C16 ~ C18 / `spec-003-mobile-app.md` 개정 ⑩ · U-2 예외
- 사용자가 본 것: `…/work/fix/e2e-feedback.md` 8 · 9 · 10 · 그림 `e2e-shots/08-app-chat-longpress-floating.png` · Delivery CENTURION_DAY#241 v2(승인됨)
- 스펙에 없는 것은 발명하지 마라. **문서 리뷰어가 이 스펙 4판을 지금 검수 중이다** — 계약이 바뀌면 코디가 정정을 보낸다. 모호한 곳은 짐작으로 메우지 말고 물어라.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(브랜치 이름이 **`kknaksss/fix-app-re1`** 로 바뀌었다 · 앞 판 변경 미커밋 그대로 그 위에). ⚠ backend 워커가 같은 워크트리의 `backend/` 에서 동시에 일한다 — 그쪽은 읽기만. `git stash` · `checkout -- .` · `clean` 금지.

## 할 것

`wp-plan.md` 「WP-APP-3」 그대로. 서버(WP-BE-3)는 같은 시간에 짓는다 — §3 계약 표 + 테스트 더블로 짓는다.

1. **8번 길게 누르기 자리(버그)** — 먼저 **재현 조건을 코드로 확인**한다(키보드가 열린 채 길게 누름 → 키보드가 닫히며 목록이 다시 잡히는데 강조 말풍선 · 메뉴는 누른 순간에 잰 자리에 고정). 원인을 확인한 사실로 보고에 적고, 스펙 U-4 의 결과(화면이 다시 잡힌 뒤의 그 말풍선 자리에 붙음 · 메뉴가 안전 영역 밖으로 안 나감 · 키보드를 닫은 채 누른 지금 모양이 기준)를 맞춘다. 시험: 키보드 inset 이 있다가 없어지는 위젯 시험으로 자리 일치를 **실패할 수 있게**.
2. **9번 폰 대화 화면에서 하단 4메뉴 숨김** — 채팅 목록에서는 보임 · 대화 화면과 그 위 채팅 화면 · 새 대화 · 초대에서 숨김(OQ-C16 기본값) · 아이패드 레일 그대로. 「보고 있는 방」 판정 · 앱 안 배너 · 푸시로 들어오기 · 탭 배지 값은 그대로. 채팅 거절(403) 안내 화면에서는 탭이 **보여야** 한다(다른 메뉴로 갈 수 있게). 하단 탭을 찾는 기존 시험을 전부 grep 으로 세어 깨진 것 · 고친 것을 표로.
3. **10번 읽음 표시(카톡식)** — 말풍선 옆에 안 읽은 사람 수 · 0 이면 표시 없음. 셈 규칙은 스펙 그대로(앱이 `members[]` 의 `lastReadSeq` · `fromSeq` 로 센다) — 셈은 **순수 함수 하나**에 두고 표 시험(그룹에서 한 명씩 읽음 · 보낸 사람 · 초대된 새 멤버 · 나간 멤버 · 비활성 · 지운 메시지 · 시스템 줄 · 1:1). `chat_member_read` 이벤트 반영(뒤늦게 온 작은 값이 큰 값을 덮지 않게) · `chat_room` 이벤트 · 다시 연결. 자리 · 색 = OQ-C18 기본값(시각 칸에서 시각 위 · `Ms.primary`). **새 화면 글자 0**(숫자만).

## 범위 제약

allowed_paths: `app/lib/` · `app/test/`. 금지: `app/ios/` · `pubspec.yaml` 의존성 · `app/lib/interpret/` · `backend/` · 서명 · 업로드 · 시뮬레이터 · 실기기 · 사용자 포트/로컬 스택 · 커밋 · push.

## 검증

`cd app && fvm flutter analyze` · 고친 테스트 파일만 `fvm flutter test <파일들>` · 마지막에 `fvm flutter test` 전체 1회 · `fvm flutter build ios --no-codesign` 1회.
캡처(기존 방식 · 가짜 값만) → `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-captures/` 에 새 이름으로: 폰 대화 화면(하단 탭 없음 · 읽음 숫자가 보이는 말풍선과 0 이라 없는 말풍선이 같이) · 키보드가 열린 대화 화면 · 길게 누르기 메뉴(키보드 열렸다 닫힌 뒤) · 채팅 목록(탭 있음) · 아이패드 대화.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-3-report.md` — 변경 파일 / 8번 원인(확인한 사실) / 하단 탭 시험 전수 표 / 읽음 셈 표 시험 / 수용 항목 ↔ 시험 / §3 계약 표와 앱이 읽는 필드 대조 / 새 화면 글자(0 이어야) / 수치 / 캡처 목록 / 스펙과 다른 곳 · 물을 것 / pending.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 수 / 시험 수치 / 캡처 / 스펙과 다른 곳 / pending"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
