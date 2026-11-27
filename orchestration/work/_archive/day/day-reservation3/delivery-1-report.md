# delivery-1 결과 보고 — DAY-SPEC-008 Delivery 발행

## 상태: done (사람 gate 에서 멈춤 — delivery-plan:review)

## 수행 내용

- **Delivery Issue**: [MediSolveAIDev/CENTURION_DAY#297](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/297) — 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`
  - idempotency key `day/day-spec-008/reservation-request` · contract version 1 · **L3**
  - contract digest `sha256:3ec7731462ecf2bbc9a545d1b8cc430bc82eb6275c16734214f5b2754252721d`
  - **plan digest `sha256:64d36d9c05298c2713d9f6de5b5f4fa5320d39704df3e705207eea6d9ae4d181`**
  - target SPEC = DAY-SPEC-008 · 006 · 005 · 007 · 000
  - next_action = `review-delivery-plan`(human_gate) · Task projection = blocked(review-required — 정상)
- json: `delivery/request-v1-reservation-request.json` · `plan-v1-reservation-request.json` · `apply-v1-reservation-request.json`(+ `.err` 는 uv 빌드 로그만)
- mediness: `products/day/30-work.md` Spec Coverage 008 행 = Delivery #297 · `log.md` wp-add 한 줄 → 커밋 `0a3ca725` push(브랜치 `kknaksss/day-reservation3-spec` · PR #968 위 · 머지 안 함)

## baseline — 지시와 다른 곳 (중요)

- 지시는 baseline = `1990be22`(PR #968 머리)였지만 **CLI 가 새 Delivery 의 baseline 을 「fetch 한 latest origin/main」으로만 받는다**(`tools/harness/src/mediness_harness/workflow.py:925` — 다르면 `requested SPEC baseline is not the fetched latest origin/main revision` · `references/requests.md` 첫 줄). 우회하지 않고 문서화된 정상 경로로 갔다: **baseline = origin/main `ae8cec61b459692fc074100386cb33a45b0665d9`**(SPEC-008 없음 → CLI 가 `spec-baseline:pending` 으로 판정). SPEC-008 계약 원천 `1990be22` · PR #968 은 Issue Review Surface 에 적었다.
- #968 머지 뒤: 같은 key · **contract_version 2** · 새 origin/main SHA 로 다시 `--apply` → `spec-baseline:ready`(결과 계약 같으면 재승인 없음 — `rules/delivery-workflow.md`).

## WP 표 (한 Delivery · Issue Execution phases)

| WP | 범위 | 의존 | 완료 조건 |
|---|---|---|---|
| WP-0 BE 바닥 | ① **착수 전 실물 확인** OQ-Q01(KOS 화면 「당일 지정 상담사」 저장 요청 = `reservation.counselor` · `reserve` 에 바로 되나) · Q02(W4 한 본문 + `reservationMemo` · `funnel`) · Q03(`create-visitor` `email` 저장) — 결과를 Issue 에 · 안 되면 멈추고 사용자 질문 ② migration(새 표 4 · `notification.reservation_request_id` · `NotificationKind.reservation_request` · `closed_reason` · ext `partner` null · 유일키 병원 단위 · 중복 행이면 멈춤) ③ 모델 ④ ext 키 병원당 하나(partner 전수 · 한도 · `_charty` · 테스트 11개) | 없음(첫 단계) | 실물 확인 셋 기록 · alembic up/down · ext 회귀 없음 · taewoo 리뷰 항목 |
| WP-1 BE ext | E1 ~ E8 · 본문 검증(길이 · phone · 1000자 · 목록 값) · 판정 RQ24 · 버전 번호 · Idempotency · 상태 표 ext 줄 · 철회 · 알림 행 + `announce_unread` · SSE 신호 | WP-0 ②③ | A1 · 계약 테스트 |
| WP-2 BE 웹 | 조각 경로 · 생성 / 수정 / 취소 묶음(W1 · W2 · W3 · W4 + 메모 · 유입 · W5 · W18 · 메모 합치기) · `visit_id` = W3 확인 · `reservation_applied` · 확인 대기 · 같이 누름 409 · 스레드 retry · `dismiss-failure` · 공용 retry 409 · 댓글 · 변경 요청 · 철회 · 자동 닫힘 · `hospital_seen_at` · 알림 목록 transport 거름 · target 칸 | WP-0 · (WP-1 과 병렬) | A3 · A4 · A6 |
| WP-3 FE | 오른쪽 목록 · 상세 창 1 · 2 · 3열(시안 v15) · 시간 머리 칩 · U-5 버튼 · 입력부 · [철회] · [다시 시도] · [접음] · SSE 다시 받기(입력값 유지) · `day.js` 알림 갈래 · `?request=&date=` | 조각 계약만(WP-0 과 같이 시작) | A5 |
| e2e | 로컬 KOS 데모 지점 실물 1회(ext 요청 → 생성 → KOS 확인 → 수정 → 취소 · 두 번째 브라우저 SSE) → 사용자 화면 확인 | 넷 다 | A7 |

## BE ↔ FE 계약 (SPEC-008 인용 — 새로 짓지 않음)

- **조각 경로** = SPEC-008 §3 「웹 경로」 표: `GET /reservations/requests`(목록) · `GET /reservations/requests/{id}`(창) · `GET …/{id}/day?date=&pick=`(2열) · `POST …/{id}/create | update | cancel`(form `version` · `memo`) · `POST …/{id}/retry` · `POST …/{id}/dismiss-failure` · `POST …/{id}/comments`(form `type` · `body` · `proposals[]`) · `POST …/{id}/comments/{comment_id}/withdraw`
- **오류** = 400 `memo_too_long` · 409 `customer_ambiguous` · `request_version_changed` · `visit_stage_changed` · `reservation_past_date` · `request_closed` · `change_request_waiting` · 503 `kos_unavailable` — 글자는 빈 문구(OQ-Q04)
- **SSE**(`/reservations/stream`) = 새 신호 `reservation_request`(본문 = 스레드 id) + 기존 `write_confirmed` · `kos_failed`(SPEC-007) — 목록 · 열린 창 다시 받기 · 입력 중 글 · 메모 · 칩 유지(U-1)
- **버튼 규칙** = U-5 표(답할 버전 종류 · 변경 요청 대기 · 실패 묶음 · 접은 뒤 · 끝난 스레드 · 권한) — 서버가 그 상태를 창 조각에 실어 보냄 · 화면은 그대로 그림
- **알림** = 목록 응답 `target{requestId, date}` · `day.js` `kind = reservation_request` → `/reservations?request={requestId}&date={date}`(SPEC-005 U-6 · SPEC-006 ⑭ ⑤)
- 글자 = SPEC-008 §2 「임시 글자 목록」만

## 승인 receipt 적용 명령 (코디 / 사용자 몫 — 적용하지 않음)

담당자가 Issue #297 의 결과 계약(Target Delta · Acceptance · Non-Goals · Review Surface)을 확인한 뒤:

```bash
D=/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/delivery
cat > $D/approval-v1.json <<'EOF'
{"decision":"approved","reviewer_type":"human","reviewer":"<사람 이름>","plan_digest":"sha256:64d36d9c05298c2713d9f6de5b5f4fa5320d39704df3e705207eea6d9ae4d181"}
EOF
cd /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec
uv run --project tools/harness mediness start-delivery \
  --request $D/request-v1-reservation-request.json \
  --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec \
  --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3 \
  --github-repo MediSolveAIDev/CENTURION_DAY \
  --plan-approval-receipt $D/approval-v1.json --apply --json
```

- 주의: 이 재실행 때 fetch 한 origin/main 이 `ae8cec61` 에서 바뀌었어도 **기존 Issue 는 request 의 baseline 을 그대로 쓴다**(`workflow.py:929`) — 문제없음. 승인 뒤 다음 action 은 `prepare-spec-baseline`(#968 머지 → version 2 재결속)일 것.

## 검증

- `lint-pipeline.py --strict` → 0 error · 263 warning(전부 타 제품 · products/day 0) · 커밋 훅 lint 통과
- plan · apply exit 0 · Issue 라벨 확인(`gh issue view 297`)

## 미결 · 주의점

- **baseline SHA 가 지시(`1990be22`)와 다름** — 위 「baseline」 절. 지시대로 1990be22 로 보내면 CLI 가 거절한다(우회 없음).
- **코드 수정 없음 · SPEC 본문 변경 없음 · 승인 receipt 적용 없음 · PR 머지 없음.**
- `tools/harness/.venv` 가 `uv run` 으로 생겼다(git status 깨끗 — 무시 목록에 있음).
- 1 PR 이 크다(BE 셋 + FE) — Review Surface 에 적음.
