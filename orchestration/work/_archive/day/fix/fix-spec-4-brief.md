# [planner] fix 스펙 4판 — 피드백 8 · 9 · 10 추가 + 작업 계획 · Delivery #241 갱신

너는 **day `planner` 워커**(스펙 1 ~ 3판 · `wp-plan.md` · Delivery #241 을 한 같은 터미널)다.

- 사용자 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/e2e-feedback.md` 「버그 기록」 **8 · 9 · 10** · 그림 `e2e-shots/08-app-chat-longpress-floating.png`
- 결정: `…/work/fix/_RESUME.md` §2
- 지금 코드(읽기 — 1 ~ 7번 · 통역 구현이 미커밋으로 들어 있다): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(브랜치 이름이 **`kknaksss/fix-app-re1`** 로 바뀌었다)
- 스펙 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(브랜치 **`kknaksss/fix-app-re1-spec`** · 1 ~ 3판 미커밋 위에 이어서) · 범위 `products/day/` · 커밋 · push · PR 금지

사용자(2026-11-11): 「지금 내가 말한 거 8, 9, 10 까지 해야 하는 거 아니야? 10번은 카톡식으로」 — 커밋 전에 이 셋을 같은 작업에 넣는다.

## A. 스펙 (DAY-SPEC-004 중심)

### 8번 — 길게 누르기 화면이 뜸 (버그)
키보드가 열린 채 메시지를 길게 누르면 키보드는 닫히는데 강조 말풍선(복사본) · 메뉴가 키보드가 있던 때의 자리에 남아 원래 대화와 어긋난다. 키보드가 닫힌 상태에서는 정상.
- U-4 「길게 누르기」에 **맞아야 하는 결과**를 적는다: 강조 말풍선 · 메뉴는 화면이 자리를 다시 잡은 뒤(키보드가 닫힌 뒤)의 그 말풍선 자리에 붙는다 · 메뉴가 화면 밖으로 나가지 않는다. 어떻게 고칠지(키보드를 닫지 않고 띄울지 · 닫힌 뒤 자리를 다시 잴지)는 구현 몫 — 스펙은 결과와 수용 항목만. 원인을 추측해 적지 않는다(코드에서 확인한 사실만).

### 9번 — 폰 대화 화면에서 하단 4메뉴 숨김 (확정을 바꿈)
- SPEC-004 U-2 `:163` 「하단 4메뉴는 그대로 보인다(프로토 탭바 유지)」를 대체한다: **폰의 대화 화면(과 그 위에 쌓이는 방 정보 · 모아보기 등 채팅 스택 화면)에서는 하단 4메뉴를 숨긴다 · 채팅 목록에서는 보인다 · 아이패드(왼쪽 레일)는 그대로.** 사용자 이유: 「[대화내용][입력창][하단탭] 이 키보드를 누르면 [대화내용][입력창][키보드] 로 바뀌는 경험이 이상하다」.
- 「그 위에 쌓이는 화면」까지 숨기는 것은 **코디 기본값**(사용자는 대화 상세만 말함) — OQ 로 표시.
- 영향받는 자리를 전부 찾는다: SPEC-003 U-2(앱 셸 · 하단 4메뉴) · 「보고 있는 방」 판정(`:172` — 「지금 메뉴 = 채팅」 조건이 탭을 숨겨도 그대로 서는지) · 푸시 탭 이동 · 앱 안 배너 · 탭 배지 · 와이어 · 수용 항목 C-A16(「하단 4메뉴 … 회귀 0」) · 「프로토와 다른 곳」.

### 10번 — 메시지별 읽음 표시 (기능 추가 · 카톡식)
**사용자 확정**: 카톡식 — 말풍선 옆에 **안 읽은 사람 수**, 읽을 때마다 줄고 **0 이면 사라진다**.
**코디 기본값(통보 · 뒤집을 수 있음 — OQ 로)**: 내 메시지 · 남의 메시지 모두 · 1:1 도 같은 방식(1 → 사라짐) · 세는 사람 = 그 메시지를 볼 수 있는(`from_seq`) **지금 멤버** 중 보낸 사람 빼고 · 나간 멤버 · 비활성 직원(SPEC-004 「활성 직원」 아님)은 세지 않는다(숫자가 영원히 남지 않게) · 시스템 줄 · 지운 메시지에는 없음.

네가 정할 것(계약):
- 서버가 앱에 무엇을 주나 — 이미 `chat_member.last_read_seq` 가 있다. 후보: 방 응답 `members[]` 에 각자의 `lastReadSeq` + 읽음 실시간 이벤트(누가 어디까지 읽었나) → 앱이 메시지 `seq` 와 견줘 수를 센다 / 서버가 메시지마다 수를 준다. **지금 구조(이미 있는 칸 · 이벤트)를 가장 덜 바꾸는 쪽**을 고르고 이유를 적는다. migration 이 필요한지.
- 실시간: 읽음 요청(#15) 뒤 다른 멤버 화면의 숫자가 줄어야 한다 — 기존 채팅 SSE 에 어떤 이벤트로(새 이벤트면 이름 · 필드 · 받는 사람 · 얼마나 자주 — 읽음 폭주 때 묶기) · 끊겼다 다시 붙을 때 메우기 규칙(기존 `since` 메우기와의 관계).
- 표시: 숫자의 자리(말풍선 옆 · 시각과의 관계) · 색은 앱 `ui/theme.dart` 에 **이미 있는 토큰 이름**으로(없으면 「구현 때 정함 · 눈 확인」) · 「수정됨」 표시 · 사진 · 동영상 말풍선 · 길게 누르기 복사본과 겹칠 때. **새 화면 글자 없음**(숫자만).
- 멤버 변동: 초대(새 멤버는 `from_seq` 앞 메시지를 못 봄 — 세지 않음) · 나가기 · 비활성 전환 때 숫자가 어떻게 바뀌나.
- 성능 상한: 그룹 최대 20명 · 메시지 한 화면 — 계산이 어디서 도는지.
- 푸시 · 목록 안 읽음 Badge · 탭 배지는 바꾸지 않는다.

### 공통 규칙
근거 없는 정책 0 · 화면 문구 지어 넣지 않기 · 영향받는 절 · 케이스 매트릭스 · 수용 항목(C-A 새 번호) · OQ · 「프로토와 다른 곳」 · SPEC-000 전수 수정 · 개정 머리말 · `log.md`. 값(키 등) 없음.

## B. 작업 계획 갱신

`/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` 에 **WP 를 더한다**(기존 WP 4개는 구현 · 리뷰가 끝났다 — 고치지 않는다 · 「끝남」 표시만):
- WP-BE-3 읽음 표시 서버 · WP-APP-3 채팅 화면(8 · 9 · 10 앱 쪽). 같은 틀: 근거 스펙 절 · 수용 항목 · **grep 으로 센 고칠 파일**(지금 미커밋 코드 기준) · 하지 말 것 · 시험 · 실물 몫 · §3 계약 표에 읽음 계약 추가 · 순서(서버 계약 표로 앱이 동시에 짓는다).

## C. Delivery #241 갱신

`start-delivery` 규칙대로 **같은 idempotency key `day/fix-device-feedback-interpret` 의 contract_version 을 올려** 결과 계약에 8 · 9 · 10 을 더한다(새 Issue 를 만들지 않는다). 브랜치 이름이 바뀐 것(`kknaksss/fix-app-re1` · `kknaksss/fix-app-re1-spec`)도 Execution 에 맞춘다. baseline 은 계속 pending.

계약이 바뀌면 앞 승인은 stale 이 된다. 사용자는 위 지시로 이 셋을 넣으라고 했다 — **더해진 것이 8 · 9 · 10 뿐이고 위험 수준이 그대로(L3)면** 새 plan_digest 로 승인 receipt(`reviewer_type: human` · `reviewer: kknaksss`)를 적용한다. 그 밖의 것이 더해졌거나 등급 · 조건이 달라지면 **승인하지 말고 멈춰서 보고**한다. 2차 Delivery 는 건드리지 않는다.

## 검증 · 보고

```
python3 scripts/lint-pipeline.py --strict     # products/day/ ERROR 0
```

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-4-report.md`
— 바꾼 문서 · 절(문서:줄) · 읽음 계약을 어느 방식으로 왜 · migration 유무 · 정할 것(사용자 몫만 · 후보 · 추천) · `wp-plan.md` 추가분 요약 · Delivery(contract_version · plan_digest · 라벨 · 승인 적용 여부) · lint.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "바꾼 문서 / 읽음 계약 방식 · migration / 정할 것 N건 / Delivery digest · 승인 / lint"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] planner: <질문>" --enter`
