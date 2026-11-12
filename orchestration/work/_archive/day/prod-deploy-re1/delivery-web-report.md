# delivery-web — 웹 피드백 스펙 개정(SPEC-002 개정 ⑱) + 새 Delivery (2026-11-11 · planner)

## 결과 한 줄

SPEC-002 개정 ⑱(W3 · W4 · W5 · 차트 모달 문장) — 스펙 워크트리 미커밋 · 새 Delivery **CENTURION_DAY#245** 발행(L3 · plan 승인 안 함) · lint --strict 0 error.

## 워크트리

- `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec` · 새 브랜치 `kknaksss/prod-deploy-re1-spec-web` ← `origin/main` 7bdde9f2(#933 머지 · 시작 때 미커밋 변경 없음 확인)
- 바뀐 파일(미커밋 · 커밋 · PR 은 코디): `products/day/20-spec/spec-002-procedure-board.md` · `products/day/log.md`(:17 새 행 · spec-change · DAY-SPEC-002)

## SPEC-002 개정 ⑱ — 어디를 바꿨나

| 결정(_RESUME §2) | 바꾼 곳 |
|---|---|
| W3 방 옮기기 목록 | 개정 노트 ⑱ · 기획안 표 2-1 정책 1·2 행 · 화면 구성 E53 행 · U-15 첫 줄(「방 이름만」 · 「room.order 순」 → 「비어 있음」/「배정됨」 · 빈 방 먼저 → 배정됨(묶음 안 room.order) · 배정됨 정의 다섯 경우 · 배정됨도 고름) · 스냅샷 `rooms[]`(배정됨 여부 — 칸 이름은 구현 PR) |
| W4 점유 이동 이벤트 연쇄 | KOS 쓰기 표 「방 배정 없음」 3행(응답 → 상세 조회 → change-tasks-room 2건 → 상세 조회 확인 · 「다음 조회로 안다」 취소선) · 규칙 28 · OQ-38 |
| W5 복귀 = 삭제 | U-15 [복귀하기] 줄 · 점유 판정 줄 · 용어 「원래 방」 · KOS 쓰기 표 복귀 3행(complete=false → cancel reason=DELETE → change-tasks-room · 확인 = 사라짐) · 귀가 대기 행에 「CANCEL 그대로」 · 규칙 29 · 33(지운 행 deleted_at 포함) |
| 차트 모달 | U-14 「모양」 새 줄(머리 = 판 카드 고객 줄 · 바이탈 줄 · 세 칸 2줄 고정 · 칸 안 스크롤 · 담당자 목록 = 의사 호출 창 사람 줄 · 아바타 · 이름 · 직군 오른쪽) · 「작성자」 줄 = 화면에 안 보임(데이터 · API 그대로 · 옛 문장 취소선) · :526 차트 JSON `staffOptions[].job` · `customer.gender` · `birthDate` · OQ-47 |

열린 것으로 둔 것(새 OQ — 결정에 없어서): **OQ-51** 「배정됨」 남은 경우(상담 단계인데 방 있는 방문 · 귀가 `completed` 방문 · 묶음 머리 줄) · **OQ-52** 「그 예약 상세 조회」 KOS 경로 · 새 작업 가려내기 · 못 찾을 때 · **OQ-53** 「방 배정」 DELETE 데모 실물(complete=false 필요 여부 · 조회에서 빠지는지 · sequence 재사용 · KOS 웹에서 지운 「방 배정」도 규칙 33 에 넣을지) · **OQ-54** 직군 둘 다 = 미결(글자 없음).

해석 메모(코디 확인 바람):
- W3 「접수 중 방 있음」 → 「접수 단계인데 방이 있는 방문」으로 적음 · 상담 단계는 결정에 없어 OQ-51.
- W5 「지운 행도 사본에 남겨 원래 방 판정」 → 「복귀로 지운」 행으로 좁혀 적음 · KOS 웹에서 지운 행은 OQ-53.
- 차트 머리 = 「판 카드 고객 줄」에 바이탈 줄(성별 · 만 나이 · 국적)도 넣었다 — 코드(`board_chart_parts.html:60-61` 이 `customer_line` + `vital`) · gender · birthDate 를 더한 이유와 맞춤.
- 화면 글자 새로 지은 것 없음(「비어 있음」 · 「배정됨」 · 「간호」 · 「피부관리」 · 「원장」 = 사용자 결정).

## 새 Delivery — CENTURION_DAY#245

- https://github.com/MediSolveAIDev/CENTURION_DAY/issues/245 · key `day/web-room-move-return-feedback` · contract_version 1 · **L3**(실제 병원 KOS 쓰기가 바뀜 — DELETE · complete=false · 이벤트 연쇄)
- 범위 = W3 · W4 · W5 기능 변화만. 차트 모달은 Non-Goal(디자인 · 이미 구현 · 스펙 문장만).
- baseline = `origin/main` 7bdde9f2 · CLI `spec_baseline_state = ready`(SPEC-002 가 main 에서 stable). **단 개정 ⑱ 은 아직 머지 전** — Review Surface[0] 에 「스펙 PR 머지 → 같은 key contract_version 2 재결속 → 사용자 승인 · v1 plan_digest 는 승인하지 않는다」 명시(#243 v1 과 같은 길).
- --plan exit 0 → --apply exit 0 · status `created` · core healthy · partial=true(task_projection blocked / delivery-plan-review-required — 승인 전 정상)
- 라벨: `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready`
- contract_digest: `sha256:525413b6ba9c671918fd32858d4024b7a684309c6855d33fa793f8f898d7284f`
- plan_digest: `sha256:271a767fd07301115592a0338cc1bba53838351e8c1641fc42a2253ecae3df9e` — **승인 receipt 적용 안 함**
- Review Surface 에 코드는 같은 PR(#244)에 쌓는다(사용자 「같은 pr 같은 작업」)고 적음.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v1.request.json` · `web.v1.plan.json` · `web.v1.apply.json`

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning(products/day 0건 · 나머지는 다른 제품)

## 다음(코디)

1. 스펙 브랜치 커밋 · PR(mediness) → 머지(사용자)
2. #245 v2 재결속(같은 key · contract_version 2 · baseline = 새 origin/main) → 사용자 승인

## 수정 1 (2026-11-11 · review-doc-3 N1 ~ N6 · 코디 결정)

스펙(미커밋 · 같은 브랜치 `kknaksss/prod-deploy-re1-spec-web` · `spec-002-procedure-board.md` 만 — log.md 행은 그대로 맞음):
- **N1** 「10초 조회는 KOS 웹 변경 받기용으로만」 → 「이 연쇄는 10초 일정 조회를 기다리지 않는다(10초 조회는 그대로 — KOS 웹 변경 받기 · 다른 쓰기의 확인)」 — 개정 노트 ⑱ · 규칙 28 · KOS 쓰기 표 3행 · :84 끝에 「(점유 이동 · 「방 배정」 없음은 상세 조회로 바로 확인 — 규칙 28)」.
- **N2** OQ-52 = 기본값(코디 · 구현 PR 에서 확정): 상세 조회 = `schedule/v1/queries/get-schedule-detail`(본문 `scheduleId`) · 새 「방 배정」 = 보내기 전에 없던 sequence 중 기타 작업 id = 설정 `room_assign_etc_task_id` · 못 찾으면 지금처럼 10초 일정 조회로 넘어감. KOS 쓰기 표 add 행 · 규칙 28 에 연결. **HAR 위치 메모**: 지시의 `reference/2026-11-06-repo-structure/har/방선택.har` 는 `day-fix-web-app/reference` 아래에 없었고 `~/Downloads/방선택.har` 에서 확인함 — 경로 · 본문 키(`scheduleId`) · 응답에 `sequence` 있음만 봤다(값 안 옮김). 레포 reference 로 옮길지는 코디.
- **N3** complete=false 는 결정 — KOS 쓰기 표 복귀 1행 「앞에 보내는 것은 결정(KOS 웹 순서) — 「방 배정」에도 KOS 가 받는지는 데모 실물로」 · OQ-53 = 데모 실물 확인 항목만(KOS 가 거절하지 않는지 · DELETE 뒤 조회에서 빠지는지 · sequence 재사용).
- **N4** 「복귀로 지운 행」 → 「지운 「방 배정」 행(`deleted_at` · 지운 곳 무관)」 — 개정 노트 · 점유 판정 · 용어 「원래 방」 · 규칙 29 · 33 · OQ-53 끝 항목 지움. (해석 메모 2 철회)
- lint --strict: exit 0 · **0 error** · 263 warning(products/day 0)

Delivery #245 → **contract_version 2**(--plan exit 0 → --apply exit 0 · status `scope-delta-recorded` · core healthy · partial=true = 승인 전 blocked 정상):
- **N1 · N2** W4 줄 · A2(세 경로 — 찾음 · 못 찾음 → 10초 조회로 · 주기 상수 그대로 — 시험으로 고정) · code_surface(get-schedule-detail 클라이언트 · 지금 없음) · verification
- **N3** open_questions 에서 complete=false 뺌 · Review Surface 「complete=false 를 앞에 보내는 것은 결정」 · predeploy 에 OQ-53 확인 항목
- **N4** W5 줄 · A4 「지운 곳 무관」
- **N5** 되돌리기 문장 = 「되돌린 코드는 지운 「방 배정」 행을 읽지 않는다 — 원래 방은 visit.room_id 로 떨어질 수 있다(그날 방문만)」
- **N6** A6 = 클릭 → 마지막 확인 시각을 event_log · external_outbox 로 재서 Issue 에 기록(research-1 19.8 ~ 27.1초와 나란히 · 목표 수치 없음)
- 참고 반영: Non-Goal 1 끝에 「차트 JSON 칸 추가의 계약 대조는 하지 않음 — #244 본문에 적는다」 · Review Surface[0] 다음 재결속 = contract_version 3
- Issue 본문 갱신 2026-11-11T12:10:01Z · 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` · baseline 7bdde9f2(ready · 개정 ⑱ 머지 전)
- contract_digest `sha256:464543b70b81f56b9a4eaf45883b6d5e3260c04b91f9bf0db879cf868bf92af4`
- plan_digest `sha256:e181dbda6a1a59cadc1f59ba278e7cf9ffae30c4611eac22041e26849379c952` — **승인 receipt 적용 안 함**
- 산출물 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v2.request.json` · `web.v2.plan.json` · `web.v2.apply.json`

## 승인 (2026-11-11 · 사용자 「승인이라고 발주해」 · 코디 지시)

- receipt `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v2.approval-receipt.json` = `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"sha256:e181dbda6a1a59cadc1f59ba278e7cf9ffae30c4611eac22041e26849379c952"}`
- **--plan(receipt 포함)**: exit 0 · origin/main 그대로 7bdde9f2 · plan_digest **같음**(e181dbda…) · contract_digest 같음(464543b7…) · plan_review approved
- **--apply(receipt 포함)**: exit 0 · status **`plan-approved`** · execution_state ready · core healthy
- **라벨(#245)**: `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready`(갱신 2026-11-11T12:33:56Z)
- **next_action**: `implement-and-open-code-pr` · human_gate=false · 다음 skill `review-delivery`(코드 PR 열린 뒤)
- task_projection: `pending` — `mediness.task_draft_request` 로 Task 초안을 만들라는 안내(utterance)가 나왔다. **하지 않았다**(지시 범위 밖 · 필요하면 코디). partial=true 는 이 pending 때문.
- **#243 은 건드리지 않음** — 라벨 `delivery-plan:review` 그대로 · 마지막 갱신 11:25:13Z(v2 apply 때) 그대로 확인.
- 남은 길(그대로): 승인은 baseline 7bdde9f2(개정 ⑱ 머지 전) 결속 v2 에 대한 것 — 스펙 PR 머지 뒤 contract_version 3 재결속을 할지는 코디(재결속하면 plan_digest 가 바뀌어 다시 승인이 필요할 수 있음).
- 산출물 `web.v2.approve.plan.json` · `web.v2.approve.apply.json`

## 수정 2 — 스펙 ⑱ 보충 ⑤ · ⑥ (2026-11-12)

근거: 사용자 2026-11-12 「b로 발주해」 · 웹 e2e W6 · `be-3-report.md` 「관찰」 · `review-code-8-report.md` 참고 1.
대상: 브랜치 `kknaksss/prod-deploy-re1-spec-web`(PR #934) 위에 커밋하지 않은 변경. 커밋은 코디가 한다.

### 넣은 것
- **⑤ 연쇄 결과 바로 반영**: 점유 이동 연쇄가 받은 상세 조회 결과를 판에 바로 반영한 뒤 신호를 보낸다. 띠가 10초 조회를 기다리지 않는다.
  - 고친 곳: 규칙 28, :84 동기화 문장, KOS 쓰기 표의 점유 이동 3행, U-15 띠 문단.
- **⑥ 반영 대기 중 [복귀하기] 숨김**: 그 방문에 KOS 반영 대기 쓰기(`pending` · `sent` op)가 있으면 [복귀하기]를 보이지 않는다. 반영이 끝나면 다시 보인다.
  - 고친 곳: 규칙 29 첫머리, U-15 띠 문단과 「점유는 한 번이 끝」 팝오버 문장, 화면 구성 E53 행, 카드 구성 줄, 사용 흐름 2단계, 스냅샷 `canReturnRoom`.
  - `canReturnRoom` 은 이제 「점유 중이고 반영 대기 op 이 없을 때」만 true다.
- 개정 노트 ⑱ 에 ⑤ · ⑥ 문장을 더했다. frontmatter `last_updated` 는 2026-11-12 다.
- `log.md` 에 2026-11-12 `spec-change` 행 하나를 더했고, 최종 수정일도 바꿨다.

### grep 으로 일부러 그대로 둔 곳
- :133 기획안 대조 표: 기획안 내용이라 그대로 둔다.
- :408 흐름 3단계: 누른 뒤 결과만 적은 문장이다.
- OQ-40: 닫힌 결정의 기록이다.
- OQ-48: 토스트 글자 항목이다.

### 정하지 않은 것
- 서버가 숨김 중에 들어온 `room-return` 요청(오래된 화면)을 거절할지, 거절한다면 그 이름은 아무것도 적지 않았다.
- 오류 매트릭스에 새 행을 넣지 않았다. 결정에 없는 내용이다.
- 새 화면 문구는 넣지 않았다.

### 검증
- `python3 scripts/lint-pipeline.py --strict` 결과: 0 error, 263 warning. `products/day` 경고는 0이다.

### 참고
- 워크트리의 `products/day/60-release/app-store-preparation.md` 는 이번 작업 전부터 수정된 상태였다. 내가 고친 파일이 아니라 건드리지 않았다.

## 수정 3 — review-doc-5 W1 · W2 반영 (2026-11-12)

대상: 같은 브랜치(`kknaksss/prod-deploy-re1-spec-web` · PR #934)의 미커밋 변경. 커밋은 코디가 한다.

- **W1 · 규칙 22 예외**: 「하나 예외」를 「예외」로 고쳤다. 예외는 셋이다.
  - 「시작 취소」: 그대로 둔다.
  - 방 이동: 「방 배정」을 만드는 중이면 막는다(규칙 28 · 개정 ⑯). 이미 있던 결정을 같은 자리에 옮겨 적은 것뿐이다.
  - [복귀하기]: 그 방문에 반영 대기 쓰기가 있으면 보이지 않는다(규칙 29 · 개정 ⑱).
- **W2 · (가)를 받음**:
  - 케이스 매트릭스의 `room_not_held` 행 아래에 1행을 넣었다: `| 복귀 — 그 방문에 반영 대기 쓰기 있음 | 복귀 | 409 | conflict | 거절(규칙 29 · 화면은 버튼 안 보임 · 개정 ⑱) |`.
  - 규칙 29 끝에 「반영 대기 쓰기가 있을 때 온 복귀 요청은 서버도 409 `conflict` 로 거절한다(케이스 매트릭스 · 토스트 글자 §5 OQ-48)」를 더했다.
  - OQ-48 은 고치지 않고 열어 둔 그대로다.
- **안 한 것**: 참고 1 ~ 4 는 손대지 않았다. 새 화면 문구도 넣지 않았다.
- **log.md**: 2026-11-12 ⑱ 보충 행의 요약 끝에 W1 · W2 내용을 덧붙였다. 새 행은 만들지 않았다.
- **검증**: `lint-pipeline.py --strict` 결과 0 error · 263 warning. `products/day` 쪽은 0건이다.

## 수정 4 — SPEC-003 상태 색 테두리 없음 (2026-11-12 · e2e A1)

대상: 브랜치 `kknaksss/prod-deploy-re1-spec-web` 의 미커밋 변경. 바꾼 파일은 `spec-003-mobile-app.md` 와 `log.md` 두 개다. 커밋은 코디가 한다.

- **고친 곳**: 상태에 따라 카드 · 행 테두리 색을 바꾸던 문장을 전부 「상태 색 테두리 없음 — 평소 테두리 그대로」로 바꿨다. 줄 번호는 개정 노트를 넣기 전 기준이다.
  - :194 §2 「테마」 — 진행 중 시술 카드
  - :261 U-3 확인 필요 — 「시술 중 등 다른 상태도 같다」를 더했다
  - :334 시술 행 와이어
  - :342 「진행중」 행
  - :719 오류 · 상태 표의 확인 필요 행
  - OQ-A20 — 토큰 대상에서 「테두리」를 지웠다
- **그대로 둔 것**:
  - 연한 배경과 「확인 필요」 상자의 옅은 빨강 바탕 + 왼쪽 띠(B안)
  - :180 · :255 · A-33 · A-37 · A-43 · OQ-A29 · OQ-A35 — 이미 「카드 테두리 없음 · 평소 그대로」 쪽이라 고칠 것이 없었다
  - :274 「지금 카드 테두리 = `Ms.red`」 — 토큰 이름이 어디서 왔는지 적은 괄호다. 동작을 정하는 문장이 아니라서 손대지 않았다. 코디가 지우라고 하면 지운다
- **기록**: 개정 노트 ⑪ 한 줄을 Delivery sync 노트 다음에 넣었다. `last_updated` 는 2026-11-12 다. `log.md` 에 2026-11-12 `spec-change` · DAY-SPEC-003 한 행을 더했다.
- **손대지 않은 것**: Delivery, 새 문구, `60-release/app-store-preparation.md`(앱 세션 것).
- **검증**: `lint-pipeline.py --strict` 결과 0 error · 263 warning, `products/day` 경고 0건.

## 수정 5 — SPEC-003 개정 ⑪ 범위 = 시술현황 탭 카드만 (2026-11-12 · 사용자 「상세 말고 현황탭만」)

대상: 같은 브랜치의 미커밋 변경. 바꾼 파일은 `spec-003-mobile-app.md` 와 `log.md` 다. 커밋은 코디가 한다.

- **⑪ 개정 노트**: 범위를 「**시술현황 탭 카드**」로 좁혔다. 사용자 원문과 「방 상세 시술 행은 그대로」를 적었다. 고친 곳 목록은 이제 §2 「테마」 · U-3 · 오류 표다.
- **되돌린 것(수정 4 전 문장 그대로)**: 방 상세 시술 행 와이어(:336 「연한 DAY 배경 · 테두리 · 경과 크게」), 「진행중」 행(:344), OQ-A20(진행 중 시술 연한 주색 배경 · 테두리의 토큰). 방 상세 시술 행은 테두리를 계속 쓰므로 OQ-A20 도 원문으로 돌렸다.
- **§2 「테마」(:196)**: 원문 「연한 배경 · 테두리」로 돌린 다음, 「(시술현황 탭 카드는 상태 색 테두리 없음 — 평소 테두리 그대로 · 개정 ⑪)」를 붙였다.
- **그대로 둔 것**:
  - U-3 확인 필요(:263)와 오류 표 확인 필요 행(:721). 둘 다 시술현황 탭 카드 이야기다.
  - 방 상세 강조 상자. 이번 결정 대상이 아니어서 적지 않았다.
- **:276 괄호(review-doc-6 참고 2)**: 「지금 카드 테두리 = `Ms.red`」를 「개정 ⑧ 전 카드 테두리 색 = `Ms.red`」로 고쳤다.
- **log.md**: 2026-11-12 DAY-SPEC-003 행 요약을 「시술현황 탭 카드 … 방 상세 시술 행 그대로 · 사용자 「상세 말고 현황탭만」」으로 고쳤다. 새 행은 만들지 않았다.
- **검증**: `lint-pipeline.py --strict` 결과 0 error · 263 warning, `products/day` 0건. `app-store-preparation.md` 는 손대지 않았다.

## 수정 6 — SPEC-003 개정 ⑫ 설정 「정보」 · 개인정보 처리 안내 링크 (2026-11-12)

근거: 사용자 2026-11-12 「설정에 정보 탭 만들고 두자」 · 「곧 출시 예정은 그대로」. 대상 브랜치의 미커밋 변경이고, 커밋은 코디가 한다.

- **SPEC-003 개정 ⑫ 노트**: ⑪ 다음에 한 줄을 넣었다.
  - 설정 탭 「정보」(사용자 글자) 안에 「개인정보 처리 안내」 링크를 둔다. 링크 글자는 60-release §6-1 승인 문안 제목이다.
  - 링크는 `https://day.medisolveai.com/privacy` 를 외부 브라우저로 연다. 앱 안 개인정보 경로(§7-2 #6)는 이것으로 닫는다.
  - 예약현황 「곧 출시 예정」은 그대로다(#7). 결정만 기록했고 동작은 바뀌지 않는다.
- **충돌 맞춤**:
  - :24 개요: 설정 = 계정 · 로그아웃 · 「정보」
  - :83 §1 범위 표 「넣음」: 「정보」를 더했고, 「곧 출시 예정」 그대로 · 사용자 2026-11-12 를 적었다
  - :94 「뺌」: 「설정 탭의 계정 · 「정보」 밖 상세」로 고쳤다. 「정보」는 범위 안이다
  - U-2 설정 줄
  - U-16: 「정보」 불릿을 새로 넣었다. 지금 보이는 것은 계정 · 로그아웃 · 「정보」 다
  - User Scenario 화면 줄
  - A-27: 「정보」 → 외부 브라우저를 더했다
- **정하지 않은 것**: 「정보」 칸 모양(설정 안 칸인지, 하위 화면인지). 구현 때 정하고 리뷰에서 눈으로 확인한다. 새 화면 문구는 없다. 쓴 글자는 「정보」(사용자)와 「개인정보 처리 안내」(§6-1 승인 제목)뿐이다.
- **60-release `app-store-preparation.md`**: §7-2 표의 #6 · #7 두 행만 고쳤다. #6 은 「결정됨 … `lib/` 구현은 아직 · 담당 앱 코디(구현)」, #7 은 「결정됨 — 그대로 · 앱 변경 없음」이다.
  - 앱 세션의 미커밋 변경은 그대로 남아 있다. 고치기 전 사본과 diff 를 떠 보니 두 줄만 바뀌었다. 사본: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/app-store-preparation.before6.md`
  - frontmatter `last_updated` 는 앱 세션 것이라 건드리지 않았다.
  - #7 은 지시에 이름이 없었다. 같은 사용자 결정이라 「미결정」으로 두면 사실과 달라져서 함께 표시했다. 빼야 하면 그 한 줄만 되돌리면 된다.
- **log.md**: 2026-11-12 `spec-change` · DAY-SPEC-003 행 하나를 더했다.
- **검증**: `lint-pipeline.py --strict` 결과 0 error · 263 warning. `products/day` 쪽은 0건이다.

## 수정 7 — review-doc-7 W1 · 60-release #6 · #7 · :100 (2026-11-12)

앱 작업은 메인 코디가 넘겨받았다(`mobile-handoff.md`). 그래서 이번에는 앱 세션이 커밋하지 않은 60-release 문장도 고쳤다. 고친 곳은 아래 세 줄뿐이고, 다른 미커밋 내용은 그대로 두었다. 고치기 전 사본은 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/app-store-preparation.before7.md` 에 있고, 사본과 diff 하면 세 줄만 다르다. 커밋하지 않았다.

- **① #7 (:376)**: 「막는 것」을 `심사(2.1) — 위험 남음(사용자가 그대로 두기로 함)` 으로 바꿨다. 「지금」은 「결정됨 — 그대로」, 「담당」은 「—」 그대로 두었다.
- **② :100**: 「…제출할지(숨김 · 완성)는 [미정](§7 — …)」을 「…는 결정됨 — 그대로(§7-2 #7 — Apple 심사 가이드 2.1 완성도)」로 바꿨다.
- **③ #6 (:375)**: 「`lib/` 구현은 아직」을 「앱 구현됨(코드 커밋 `1d4ccfba` · 실기기 Safari 확인) · `/privacy` 200 은 남음(#1)」으로 바꿨다.
  - 커밋 번호와 Safari 확인은 코디 지시를 그대로 옮겼다. 앱 레포를 내가 직접 보지는 않았다.
  - 「담당」 칸은 원래 값 「앱 코디(구현)」 그대로다. 앱 구현이 끝났으니 「—」이나 「서버 코디(#1)」로 바꿀지는 코디가 정한다. 이번 W1 처럼 결정에 없는 칸 판단은 하지 않았다.
- frontmatter `last_updated` · SPEC · log.md 는 바꾸지 않았다. 60-release 는 log 대상이 아니다.
- 검증: `lint-pipeline.py --strict` → 0 error · 263 warning · `products/day` 0건.

## 수정 8 — #245 contract_version 3 (2026-11-12 · 코디 결정 「공개 페이지는 #245」)

### 더한 것 (v2 request 위에)

- **target_specs**: DAY-SPEC-002 · **DAY-SPEC-001 · DAY-SPEC-003** (셋 다 main 에서 stable).
- **Target Delta** 4줄 더함:
  - W6 연쇄 결과를 판에 바로 반영한 뒤 신호(⑱ ⑤).
  - W7 반영 대기(pending · sent) 중 [복귀하기] 숨김 · canReturnRoom = false · room-return 409 conflict(⑱ ⑥ · W2 (가) · 규칙 22 · 29 · 매트릭스).
  - P1 공개 페이지 GET /privacy · /support 로그인 없이 · 본문 = 60-release §6 그대로(SPEC-001 ⑦).
  - P2 앱 설정 「정보」 → /privacy 외부 브라우저(SPEC-003 ⑫).
- **Acceptance** A7 ~ A10 (W6 · W7 · P1 · P2 각 하나 · P2 는 앱 시험 + 실기기 1회).
- **Non-Goals**:
  - 「DB migration · 앱 변경」 → 「앱 변경(설정 「정보」 링크 P2 밖)」.
  - 앱 카드 테두리(SPEC-003 ⑪ · 디자인만) 줄 더함 — A1 은 넣지 않음.
  - 공개 페이지 글자 바꾸기 · 60-release §7 사실 확인 · 공개 페이지 prod 배포 실행 줄 더함.
- **code_surface**: board 쪽(W6 · W7) · public_pages.py · public_page.html · public/*.txt · main.py · app.css(P1 — 코드 워크트리에 이미 있음 · 미커밋) · app shell.dart · app_flow_test.dart(P2 · 커밋 1d4ccfba).
- phases BE-4 · FE-3 · APP · verification · predeploy(공개 페이지 prod 200 확인) · scope_delta 「v2 → v3」 한 줄.
- Review Surface[0]: 다음 재결속 = **contract_version 4**(스펙 PR #934 머지 뒤).

### 결과

- baseline = origin/main **7bdde9f2 그대로**(#934 미머지 · ⑱ 보충 · ⑦ · ⑫ 은 아직 baseline 밖 — v2 와 같은 길). spec_baseline_state ready.
- --plan exit 0 · status planned → --apply exit 0 · status `scope-delta-recorded` · core healthy · partial=true(task_projection blocked / delivery-plan-review-required — 승인 전 정상).
- Issue #245 본문 갱신 2026-11-12T04:07:39Z · meta contract_version=3.
- **라벨**: `delivery-plan:approved` → **`delivery-plan:review`** (v2 승인은 v3 에 이어지지 않음) · `execution-plan:ready` · `spec-baseline:ready`.
- contract_digest `sha256:01991b047f6b312b4fd867881b14932c99fc92a6a44ef0c59d8a76a3c2011c59`
- **plan_digest (v3 · 승인 대상)** `sha256:846f85023d65b4f42083aff021a3bf8dd83a56e5f3b2d1c138f172996bfac5e6` — **승인 receipt 적용 안 함(사용자 몫)**.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v3.request.json` · `web.v3.plan.json` · `web.v3.apply.json`.

### 확인 필요

- Issue **제목은 바뀌지 않았다** — request title 은 고쳤지만 CLI 가 기존 제목을 둔다. 손으로 바꿀지 코디가 정할 일(지시에 없어 안 바꿈).
- 승인이 v2 → review 로 돌아갔다. 코드 작업이 이미 승인 v2 아래 진행 중이면 v3 승인 전까지 task_projection 이 blocked 다.
- 60-release #1 담당 칸 그대로.

### 검증

- lint `--strict` exit 0 · 0 error · 263 warning · `products/day` 0. 스펙 파일은 이번에 손대지 않음(수정 — 공개 페이지 의 미커밋 3파일 그대로).

## 수정 9 — review-doc-8 W1 (가) · #245 contract_version 4 (2026-11-12)

- **바꾼 것 하나**: Non-Goal 7 끝에 「· 이미 구현(같은 코드 PR #244 · 01bbed49) · 이 Delivery 범위 아님」(Non-Goal 0 과 같은 방식). 나머지는 v3 request 그대로 — v3 ↔ v4 diff = contract_version 3 → 4 와 Non-Goal 7 두 줄뿐.
- baseline = origin/main 7bdde9f2 그대로 · spec_baseline_state ready.
- --plan exit 0 · planned → --apply exit 0 · status `scope-delta-recorded` · core healthy · partial=true(task_projection blocked / delivery-plan-review-required — 승인 전 정상).
- Issue #245 갱신 2026-11-12T04:11:12Z · meta contract_version=4 · 본문 Non-Goals 에 새 구절 확인.
- 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready`.
- contract_digest `sha256:a70ddc2aa70353c10a76d6e79ee9e25242e8b9329e2bdf9a6ed8095d0ef652be`
- **plan_digest (v4 · 승인 대상 · v3 846f8502… 은 대체됨)** `sha256:962c8c5c31859eb302602b52985f4c666b0317db02cb7bd804bb36784b21c852` — **승인 receipt 적용 안 함(사용자 몫)**.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v4.request.json` · `web.v4.plan.json` · `web.v4.apply.json`.
- lint `--strict` exit 0 · 0 error · `products/day` 0 · 스펙 파일 손대지 않음.

### 확인 필요(「그 밖 변경 금지」라 손대지 않음)

- Review Surface[0] 은 아직 「스펙 PR 머지 → contract_version 4 로 재결속」이라고 쓴다. 이번에 4 를 써서 머지 뒤 재결속은 5 가 된다 — 고칠지 코디가 정할 일.
- scope_delta 에 「v3 → v4」 줄을 더하지 않았다(같은 이유).

## 승인 — #243 v2 · #245 v4 (2026-11-12 · 사용자 「응 승인해」 · 코디 지시)

### 적용 전 확인 (둘 다 같음 → 진행)

- origin/main = 7bdde9f2 그대로. receipt 없이 --plan 을 다시 돌려 plan_digest 를 다시 계산하고, Issue 본문 meta 와 대조했다.

| Delivery | contract_version | 다시 계산한 plan_digest | Issue meta plan_digest | contract_digest(재계산 = Issue) |
|---|---|---|---|---|
| #243 | 2 | `sha256:3923f54de098a1512dc77de84789af391fe8f1d5c0f7759e4fb9b1467058b094` | 같음 | `sha256:ed0cd574…f41f3` |
| #245 | 4 | `sha256:962c8c5c31859eb302602b52985f4c666b0317db02cb7bd804bb36784b21c852` | 같음 | `sha256:a70ddc2a…652be` |

- #243 의 digest 는 delivery-report.md 「v2 apply」 절의 전체 값과도 같다.

### 적용

- receipt(각각): `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":<위 값>}` — `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v2.approval-receipt.json` · `web.v4.approval-receipt.json`.
- **#243**: --plan(receipt) exit 0 · plan_review approved · digest 같음 → --apply exit 0 · status `plan-approved` · core healthy · execution_state ready.
- **#245**: --plan(receipt) exit 0 · plan_review approved · digest 같음 → --apply exit 0 · status `execution-updated` · core healthy · execution_state ready.
- **라벨 확인**: 둘 다 `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` (#243 갱신 2026-11-12T04:14:03Z · #245 04:14:16Z).
- next_action(둘 다): `implement-and-open-code-pr` · human_gate false.
- task_projection(둘 다): pending — `mediness.task_draft_request`(Task 초안 만들기). 지시에 없어 만들지 않았다.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v2.approve.plan.json` · `prod.v2.approve.apply.json` · `web.v4.approve.plan.json` · `web.v4.approve.apply.json`.

### 확인 필요

- 두 승인은 baseline 7bdde9f2 결속이다. 스펙 PR #934(⑱ 보충 · SPEC-001 ⑦ · SPEC-003 ⑫)가 머지되면 #245 재결속(v5)을 할지는 코디가 정할 일 — 재결속하면 plan_digest 가 바뀌어 다시 승인이 필요할 수 있다.
- #245 Review Surface[0] 의 「다음 재결속 = contract_version 4」 문구는 그대로 낡아 있다(수정 9 에서 보고).

## 수정 10 — 시술 현황 보기 = 모든 직군 · #245 v5 (2026-11-12 · 사용자 「모든 직군은 시술현황 조회 돼야지 · 조작만 막히고」)

### 스펙 (products/day · 미커밋 3파일 · 시작 때 워크트리 깨끗 · HEAD 42c0ac1a)

- **DAY-SPEC-002 개정 ⑲** (§3 「권한 — 1차 기본」):
  - 키 표 `board` view 줄에 「**모든 직군**」.
  - 직무 표 「CS팀 · 경영지원 · 마케팅 · 촬영팀」 = 보기 ✓ · 수정 · 수락 없음 · 근거 칸 「보기만(사용자 2026-11-12 …)」.
  - 새 줄 「보기(`board` view)는 모든 직군 — 아래 판정은 수정 · 수락을 가른다」.
  - 판정 순서 「① 이름 표 → ② 태그 → ③ **보기**」 · ③ 「그 밖은 보기(~~그 밖은 없음~~)」.
  - 이름 표: 경영지원 · 마케팅 · CS팀(콜센터) = **보기**. 「줄을 남기는 이유 = 빼면 태그 `admin` 으로 수정 · 수락까지 열림」 한 줄.
  - **이번 한 번 맞춤** 새 줄: 이미 행이 들어간 병원(dev 데모 · prod 명동점)은 바뀐 표를 따라가지 않으므로, 한 번만 `board` 행이 없는(행 없음 · 지운 행) 직무를 `board` view 로 맞춘다. 이미 view · edit 인 행과 `board.accept` 행은 그대로(edit 을 view 로 낮추지 않음). 사람이 바꾼 행을 가르는 칸이 없어 이번에는 구분 없이 `board` view 만 맞춘다. 「사람이 바꾸거나 지운 행은 되돌리지 않는다」의 예외는 이 한 번뿐이고 그 뒤 회차는 다시 없는 행만 넣는다. 방법은 backend.
  - 케이스 매트릭스 「직무에 권한 행 없음 · level 모자람」 동작 칸 「전부」 → 「조작(`board` edit · `board.accept` edit)」 · 결과 칸 끝 「보기는 모든 직군이라 이 줄에 걸리지 않는다」.
  - 머리 개정 노트 ⑲.
- **DAY-SPEC-001 개정 ⑧**: 「권한 행이 없는 직무는 아무것도 못 한다」가 있는 네 곳(§2 대응표 `forbidden` 줄 · 흐름 7 · 규칙 9 · OQ-11)에 「단 시술 현황 보기는 모든 직군(DAY-SPEC-002 개정 ⑲)」 예외 · 개정 노트 ⑧.
- **grep 으로 보고 그대로 둔 곳**: SPEC-003 :427 · :465 · :616 · :700 · :728 · A-14b · A-44 · A-47 · OQ-A15(`board` view 를 조건으로 쓸 뿐 · 모든 직군이 되어도 문장은 맞음) · SPEC-000 :1400 · SPEC-004 :431 · SPEC-002 개정 노트 ⑩ · log.md 옛 행(이력).
- **log.md** 2026-11-12 한 행(DAY-SPEC-002, DAY-SPEC-001).
- lint `--strict` exit 0 · 0 error · `products/day` 0.

### Delivery #245 → contract_version 5

- v4 위에: Target Delta **R1** 한 줄 · Acceptance **A11** 한 줄(R1 판정용 — 계약 줄마다 판정 줄을 두는 지금 모양에 맞춤) · scope_delta 「v4 → v5」. 그 밖 그대로(diff 확인).
- baseline origin/main 7bdde9f2 그대로 · ready.
- --plan exit 0 · planned → --apply exit 0 · `scope-delta-recorded` · core healthy · partial=true(blocked / delivery-plan-review-required — 승인 전 정상).
- Issue #245 갱신 2026-11-12T04:38:29Z · meta contract_version=5 · 라벨 `delivery-plan:approved` → **`delivery-plan:review`**(v4 승인은 v5 에 이어지지 않음).
- contract_digest `sha256:b78bd7084a86086ae1ef85a805b23d006bd7b4583b6b916fdce8e29aaff91c97`
- **plan_digest (v5 · 승인 대상)** `sha256:7fed2dace0435d728d8b251d3c2c0b774eb45c828d98ff29fb21b84d32aef923` — **승인 receipt 적용 안 함(리뷰 뒤 코디 지시)**.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v5.request.json` · `web.v5.plan.json` · `web.v5.apply.json`.

### 확인 필요

- #245 Non-Goal 「DB migration · 앱 변경(…)」: 이번 한 번 맞춤을 backend 가 데이터 migration 으로 하면 이 줄과 부딪친다. 방법은 backend 몫이라 스펙 · 계약에서 정하지 않았다.
- Review Surface[0] 의 「다음 재결속 = contract_version 4」 문구는 여전히 낡음(수정 9 에서 보고).
- 승인이 review 로 돌아가서 #245 task_projection 이 다시 blocked 다 — 진행 중 코드 작업이 있으면 v5 승인 전까지 막힌다.

## 수정 11 — review-doc-9 W1 (가) · W2 (1) · W3 · #245 v6 (2026-11-12)

### 스펙 (미커밋 3파일 그대로 — 수정 10 위에)

- **W1 (가) 행으로 준다**:
  - SPEC-001 네 곳(§2 대응표 · 흐름 7 · 규칙 9 · OQ-11): 「모든 직군에 준다」 → 「**기본값으로 모든 직군에 넣는다**(DAY-SPEC-002 ③)」. 개정 노트 ⑧ 도 「행으로 줌 · 규칙 9 는 그대로 · 사람이 `board` 행을 지운 직무는 보기도 막힌다」로.
  - SPEC-002 매트릭스: 동작 칸은 다시 「전부」 · 결과 칸 「보기는 기본값이 모든 직군 — 사람이 `board` 행을 지운 직무만 이 줄」.
  - SPEC-002 같은 뜻으로 맞춘 곳: 「보기는 기본값으로 모든 직군에 넣는다」 줄 · 키 표 「기본값 = 모든 직군」 · 개정 노트 ⑲ 첫 문장 「기본값으로 … 넣는다」와 끝 문장.
  - SPEC-003 그대로.
- **W2 (1)**: 「이번 한 번 맞춤」 줄을 지우고 「**행이 없는 직무는 다음 동기화 회차가 기본값대로 넣는다**(규칙 그대로) · 사람이 지운 `board` 행(`deleted_at`)은 그대로 — 그 직무는 보기도 막힌다」로 바꿈. 코디가 센 개수(지운 board 행 dev 0 · prod 0)는 스펙에 적지 않았다(실행 상태라).
- log.md 같은 행을 같은 뜻으로 고침.
- 「이번 한 번」은 이제 SPEC-001 · SPEC-002 · log.md 어디에도 없다(grep 0).
- lint `--strict` exit 0 · 0 error · `products/day` 0.

### #245 → contract_version 6 (W3)

- **R1** 문장: 「기본 권한 행으로 … 넣음 · 행 없는 직무는 다음 동기화 회차가 넣음 · 사람이 지운 board 행은 그대로(그 직무는 403)」 — 맞춤 줄 삭제.
- **A11**: 「이름 표에 없고 태그도 없는 직무」로 · 「board 행이 없던 직무는 다음 회차에 board view 가 생김 · 기존 edit 행 그대로 · 사람이 지운 board 행은 되살아나지 않음」 · 맞춤 줄 삭제.
- phase 「BE-5 R1 기본 권한(시드 기본값 · 시험)」 · code_surface `backend/day/services/default_permissions.py` · verification 「배포 뒤 dev · prod 에서 board 행 없는 직무 0 을 개수로 확인(값 없이 개수만)」 · scope_delta 「v5 → v6」.
- predeploy 는 넣지 않음(W2 가 (1)이라).
- baseline origin/main 7bdde9f2 그대로 · ready.
- --plan exit 0 → --apply exit 0 · `scope-delta-recorded` · core healthy · blocked / delivery-plan-review-required(승인 전 정상).
- Issue #245 갱신 2026-11-12T04:43:01Z · contract_version=6 · 본문에 BE-5 · default_permissions.py 확인 · 라벨 `delivery-plan:review`.
- contract_digest `sha256:4250a3e8cbe63b07c0462e97d355c84e3d80309916bb55a22bcc01a38454c3d1`
- **plan_digest (v6 · 승인 대상)** `sha256:cc536c46fac07d4c801636d404430fe6ec07fc99f0cb147f2e11b3a0f52886c8` — **승인 receipt 적용 안 함**.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v6.request.json` · `web.v6.plan.json` · `web.v6.apply.json`.

### 확인 필요

- 수정 10 의 「DB migration Non-Goal 충돌」 걱정은 W2 (1)로 사라짐(한 번 맞춤 없음).
- Review Surface[0] 「다음 재결속 = contract_version 4」는 여전히 낡음.

## 승인 v6 — #245 (2026-11-12 · 사용자 「스펙 리뷰하고 wp 승인처리하고」 · 재리뷰 9b PASS · 코디 지시)

- **적용 전 확인 (같음 → 진행)**: origin/main 7bdde9f2 그대로. receipt 없이 --plan 재계산 → plan_digest · contract_digest 가 Issue meta 와 같고 contract_version=6.
- **plan_digest (승인됨)** `sha256:cc536c46fac07d4c801636d404430fe6ec07fc99f0cb147f2e11b3a0f52886c8`
- contract_digest `sha256:4250a3e8cbe63b07c0462e97d355c84e3d80309916bb55a22bcc01a38454c3d1`
- receipt `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v6.approval-receipt.json` = `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":<위 값>}`.
- --plan(receipt) exit 0 · plan_review approved → --apply(receipt) exit 0 · status `plan-approved` · core healthy · execution_state ready.
- **라벨 확인**: `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready`(갱신 2026-11-12T04:45:12Z).
- next_action `implement-and-open-code-pr` · human_gate false · task_projection pending(Task 초안 — 지시에 없어 만들지 않음).
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/web.v6.approve.plan.json` · `web.v6.approve.apply.json`.
- 남은 것(그대로): 승인은 baseline 7bdde9f2 결속 · 스펙 PR #934 머지 뒤 재결속 여부는 코디 · Review Surface[0] 「다음 = v4」 문구 낡음.
