# review-doc r3 처분 (코디 · 2026-10-27) — 기본값 통보

| # | 처분 | 누가 |
|---|---|---|
| F1 귀가 색 | **구현이 맞다** — SPEC §5.1 숫자를 `view.tsx` 값대로(상세 머리 완료 gray-400 · 귀가 대기 칩 gray-200 + 700 등 실제 값) | planner |
| W1 「첫 번째」 기준 | **화면이 보여 준 공지를 고친다**: 요청 `noticeId`(행 id → `kos_id`)가 저장 직전 다시 읽은 KOS 목록에 있으면 그것을 change/delete · 없으면(지워졌거나 null) KOS 응답 첫 번째 · 그것도 없으면 create. 화면 · board 는 사본 순(`released_at, id`) 첫 번째 하나 | backend 코드 · planner 문서 |
| W2-1 호출 없음 | `event_log` 남기지 않는다(지금 구현) | planner |
| W2-2 `noticeId` | 저장 뒤 다시 읽은 행의 ccc id(create 도 새 행 id) · delete 는 지운 행 id | backend 확인 · planner |
| W2-3 글자 수 | front 도 **trim 길이**로 센다(back 과 같음) | frontend · planner |
| W2-4 편집 중 날짜 이동 | 막지 않는다 · **편집 내용을 버리고** 토스트 「저장하지 않은 공지 편집을 취소했어요」 | frontend · planner |
| W3 문구 | 「사본 다시 읽기(최대 10초) — 기준은 저장 직전 back 다시 읽기」 | planner |
| W4 · 사용자 결정 2 · §9 #43 | 실물은 「KOS 웹에서 그 예약을 **취소**」가 404 를 내지 않을 수 있으므로 → **단위 시험으로 확인 · 실물은 관찰되면 기록**으로 낮춘다 | planner |
| W5 | frontend 브리프에 원인 보고 · 스크린샷 이미 있음 · 원인이 `procedure/front/app/**` · 공용 컴포넌트에 있으면 **고쳐도 된다**(범위 넓힘) | frontend · planner(WORK-007 줄) |
| W6 | §9 #46 (g) 두 브라우저 단계 더함(리뷰 예시 그대로) | planner |
| W7 | WP-FIX1 완료 · WP-E2E 본문 #1 ~ #46 · frontmatter status | planner |
| W8 · 사용자 결정 1 | **원장 목록에서도 빠지는 게 맞다**(시스템 계정은 원장도 상담사도 아님) → SPEC-003 §2 env 설명에 「상담사 · 담당자 목록과 같이 씀」 한 줄 + **OQ-519 닫음**(D-59 로) · 「그 지점 시스템 계정 id」 = 사람이 아닌 KOS 계정(KOS-DEMO 류 · 로그인 계정 말고) | planner(SPEC-003 한 줄 · OQ 닫기만) |
