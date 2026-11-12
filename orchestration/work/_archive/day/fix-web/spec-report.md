# fix-web-spec — 웹 피드백 W1 ~ W11 스펙 개정 · Delivery 발행 결과

## 상태: done (승인 대기 — receipt 적용 안 함)

| 항목 | 값 |
|---|---|
| Issue | **#249** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/249 (OPEN) |
| idempotency key | `day/fix-web-feedback-w1-w11` · contract_version 1 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` |
| risk_level | **L3** — 앱이 소비하는 공개 API(`/api/board` `needs[].why` · `needs[].doctorName` · `limits.acceptMin`)를 바꾸는 cross-repo 계약 변경. dev · prod 에 나가면 심사 중 · 설치된 앱 화면에서도 수락 뒤 미시작이 사라진다(크래시 없음). migration 없음 |
| contract_digest | `sha256:4534a40b2a19bf4b55a285f61ebf98e24d8a9b5631126bc05a2e0df0ccc3ea66` |
| plan_digest (승인 대상) | `sha256:1e055bf2b07acc21ee86b65d09eaf67e7d427869e98e292572e112138f422b8c` |
| baseline | `ready` · mediness `origin/main` `de59fe3f2710479f646df4334b222580a9552328` — **개정 ⑳ · ⑬ 은 이 워크트리에만 있음(미커밋)**. Review Surface[0] 에 적음: 스펙 PR 머지 → 같은 key 로 contract_version 2 재결속 → 그 뒤 사용자 승인(v1 digest 는 승인하지 않는 쪽 권장 — #245 때와 같은 순서) |
| next_action | `review-delivery-plan` · human_gate true |
| task_projection | blocked(`delivery-plan-review-required`) · `partial: true` — 승인 전이라 정상 |

## 스펙 변경 (products/day 만 · 미커밋 4파일)

### `20-spec/spec-002-procedure-board.md`

- **:42** 개정 ⑳ 머리 메모(W1 ~ W11 · 결정 A(변경) · 바뀐 절 목록)
- **:96** 1차 범위: 확인 필요 상황 4개
- **:122** 기획안 표 1-3 「수락 뒤 미시작」 → 상황 전체 안 함(사용자 2026-11-12)
- **:156** Placement: 의국 = 「수락 대기」 탭
- **:165** 화면 구성 E16 탭 「확인 필요 n / 수락 대기 n / 시술 완료 n」
  - E17 접는 칸 = 「시술 완료」 탭 묶음만
  - E22 [재호출] = 확인 필요 「받지 않은 호출」 카드만
- **:167** 판 카드 빨강 테두리 문장: 「확인 필요」 탭
- **:182** U-1 오더 메모 12px · 접힌 높이 5줄(W1)
- **:200** U-3 줄 버튼: 호출 줄 = 버튼 없음 · [수락] 뺌(W8)
- **:223** U-5 웹 [재호출] 자리 = 확인 필요 「받지 않은 호출」 카드 하나(OQ-56)
- **:229** U-6 [수락] = 「수락 대기」 탭에서만
- **:264-299** U-10 → 「인박스 — 확인 필요 탭」
  - 탭 「확인 필요 n」(n = 카드 수 = 상황 수) · 아코디언 없음
  - 앱용 `inbox.section` / `urgency` 판정 표는 그대로 보존(accept 만 걸렸던 카드 → `startable`)
  - 상황 표 4행: 수락 뒤 미시작 취소선. 「확인할 일」 칸 → 「상태 글자 · 경과」(대기 / 마취 / 호출 / 귀가대기 · n분째). 귀가 대기 전 버튼 = 없음(W10)
  - 확인 필요 카드 구조(W4)
  - 선택 해제 규칙(W9)
- **:302-307** U-11 → 「인박스 — 수락 대기 탭」
  - 탭 「수락 대기 n」 · 아코디언 · 수락함 없음(W2 · W7)
  - 카드 구조 그대로 · 버튼 [수락] 하나(W11)
- **:369-413** S-1 · S-2 · S-3 · S-5 · S-6 흐름 문장 맞춤(시술 대기 / 시작 가능 / 호출 탭 / 귀가 대기 카드 버튼)
- **:505** 호출 상태: `calls[]` 정의 · 웹 「수락 대기」 탭 = 수락 안 된 호출만
- **:596** `limits` 에서 `acceptMin` 삭제
- **:611** `needs[].why` 4값 · **`doctorName` 칸 삭제**(코디 지시 — backend 가 뺐음)
- **:612** `inbox` 주석(앱용)
- **:623** 카드별 section 문장
- **:679** 케이스 매트릭스 「인박스 목록 0건」(빈 상태 글자 없음 · OQ-57)
- **:808** SSE 갱신 범위 OOB: 「확인 필요」 · 「수락 대기」 탭 목록 · 탭 숫자
- **:835 · :839 · :842** 규칙 16: 4상황 · 수락 뒤 미시작 bullet 취소선 + 뺐다 · 수락 분 env 삭제
- **:854** 규칙 27: 「수락 뒤 미시작 카드는 닫히고 다시 센다」 취소선
- **:873** cc 와 다른 곳 「확인 필요」 행: 상황 4개
- **:876-886** 새 표 「개정 ⑳ — 기획안 · 시안과 달라진 곳」(브리프 §2 문장: 수락 뒤 미시작 뺌 · 사이드바 아코디언 없앰 · 사이드바 [귀가 대기] / 수락 대기 [재호출] 뺌 · 방 카드 줄 [수락] 뺌 · 카드 모양)
- **:969-971** OQ-55(**닫음 — doctorName 뺌**) · OQ-56 · OQ-57
- 규칙 31(:858)은 수락 뒤 미시작 문구가 없어 그대로 둠(차트의 「[수락] 때」는 수락 동작 얘기라 무관).

### `20-spec/spec-003-mobile-app.md`

- **:62** 개정 ⑬ 메모
  - 서버 `needs[].why` 4값 · `doctorName` · `acceptMin` 삭제
  - **앱 코드 · 새 빌드 없음** · 설치 앱에서 accept 표시가 사라짐 · 깨지지 않는 근거(`Need.parse` · `Limits`)
  - `inbox.section` · `urgency` 그대로 · 웹 탭 변경은 앱 칩과 무관
- **:237** 거르기 칩: 웹 칸은 접혔어도 앱 칩 4개 그대로
- **:267-268** 확인 필요 4개 · 겹침 표는 앞 판 기록 — accept 칸 없어짐(2 · 3 · 5번 안 생김)
- **:290** 룸 상세 머리 accept 글자 취소선(앱 코드 분기는 남음) · 함께 오는 needs 목록
- **:537 · :539** `limits` · `needs[]` 칸 목록
- **:813** 프로토 표: 4상황
- **:891** A-37 accept 글자 취소선

### `20-spec.md`

- :32 인박스(확인 필요 · 수락 대기 · 시술 완료)

### `log.md`

- :17 2026-11-12 `spec-change` 한 행(DAY-SPEC-002 개정 ⑳ · DAY-SPEC-003 개정 ⑬)

## 검증

- `python3 scripts/lint-pipeline.py --strict`: exit 0 · **0 error** · 263 warning
  - `products/day/` 는 0
  - 나머지는 다른 제품에 원래 있던 WARN이라 무관
- 화면 문구는 사용자 말만 썼다: 「확인 필요 n」 · 「수락 대기 n」 · 대기 / 마취 / 호출 / 귀가대기. 빈 상태 글자는 짓지 않았다(OQ-57).

## 정할 것 · 주의점

1. **OQ-56(사용자 확인)**: 사용자 결정 W6 · W11 의 결과로 웹 [재호출] 자리는 확인 필요 「받지 않은 호출」 카드 하나만 남는다.
   - 그래서 **호출 뒤 5분 전에는 웹에서 [재호출]을 누를 곳이 없다.** 개정 ⑮ 「경과와 상관없이 어느 칸이든」(F4)이 사라진다.
   - 결정대로 적고 열어 둠.
2. **OQ-57**: 탭이 비면 아코디언 머리도 없어 빈 목록이 된다. 빈 상태 글자는 정하지 않음.
3. **귀가대기 경과**: 「경과 형식 지금 그대로」를 따라 경과 없이 상태 글자만 보인다. 지금도 「귀가 대기 전」에는 n 이 없다.
4. **앱 글자**: 앱은 무수정이라 「대기 n분째」 같은 앱 글자는 그대로다. 웹 확인 필요 카드 모양(W4)만 바뀐다.
5. **baseline**: v1 은 개정 ⑳ 이 없는 `de59fe3f` 에 묶여 있다. 스펙 PR 머지 뒤 v2 재결속 → 승인 순서를 권장한다.
6. `tools/harness/.venv` 가 생김(gitignore — git status 영향 없음).
7. 코드 워크트리 수정 0 · 커밋 · push · PR 0.

## 파일

- request / plan / apply:
  - `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-web-spec/32d71c75-56c5-4631-a630-f268701d9f76/scratchpad/delivery/web.v1.request.json`
  - `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-web-spec/32d71c75-56c5-4631-a630-f268701d9f76/scratchpad/delivery/web.v1.plan.json`
  - `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-web-spec/32d71c75-56c5-4631-a630-f268701d9f76/scratchpad/delivery/web.v1.apply.json`

## 리뷰 반영 — review-doc-1 F1 ~ F3 · W1 ~ W3 (2026-11-12)

워크트리만 고쳤다(미커밋). Delivery #249 는 건드리지 않았다.

| # | 위치 | 반영 |
|---|---|---|
| F1 | spec-002:414 | 시나리오 2번 「원장이 수락했는데 5분 … 「{원장} 수락 n분째」」 취소선 + 「수락 뒤 미시작은 확인 필요에 들지 않는다(개정 ⑳ · 규칙 16)」 |
| F2 | spec-002:418 | 원장 변경 시나리오의 「「{원장} 수락 n분째」 카드가 있었으면 닫히고 다시 센다」 취소선(개정 ⑳) |
| F3 | spec-002:858 | 규칙 31 「규칙 27 전부」 목록의 「「수락 뒤 미시작」 다시 셈」 취소선(개정 ⑳ 뺌) |
| W1 | spec-003:374 | U-11 교차 참조 = 「수락 대기 n」 목록 · 앞 판 「수락함」 묶음은 개정 ⑳ 에서 웹에서도 뺌 |
| W2 | spec-003:205 | DAY 문구 목록에 주석: 「시작 가능」 · 「시술 대기」 · 「수락함」은 웹에서 개정 ⑳ 에 뺌 — 앱 칩 글자 근거로는 그대로(개정 ⑬) |
| W3 | spec-003:290 · :891 | 인용 출처 = 「DAY-SPEC-002 앞 판 U-10 원문(개정 ⑳ 전)」 — 웹은 상태 글자 · 경과로 바뀜 · 앱 글자 그대로(개정 ⑬) |

- spec-002 안 「수락 뒤 미시작」 · 「수락 n분째」 중 취소선 · 개정 ⑳ 기록이 아닌 살아 있는 문장은 0 이다(grep 확인).
- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning · `products/day` 0.

## 리뷰 반영 2 — review-doc-3 · review-code-3 W2 · W3 (2026-11-12)

워크트리만 고쳤다(미커밋). Delivery #249 는 건드리지 않았다.

| 위치 | 반영 |
|---|---|
| spec-002:185 | U-1 오더 메모 제목 줄 — 「펼치기」/「접기」의 「5줄 넘을 때」 = **화면에 보이는 줄 기준**(줄바꿈 없는 긴 한 줄도 5줄을 넘게 감기면 「펼치기」) |
| spec-002:189 | 상담사 배지 순서 보충 — `started_at` 없는 상담은 뒤 · 시작 시각이 같으면 상담 생성 순 |
| spec-002:190 | 지운 직원(`staff.deleted_at`)의 상담사는 배지에서 뺀다(판 조회 기존 직원 규칙과 같음 · 비활성 직원은 보임) |
| log.md:17 | 개정 ⑳ 행 요약 「오더 메모 12px」 → 「오더 메모 14px · 제목 줄 「오더 메모」 + 상담사 배지(`cards[].counselors`) · 「펼치기」 / 「접기」(E1 ~ E4)」 |

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning · `products/day` 0.

## 리뷰 반영 3 — E2E 2회차 F1 · 오더 메모 내용 12px (2026-11-12)

사용자 F1 은 「오더 메모 내용 글자 = 제목 「오더 메모」와 같은 12px」이고, E2 14px 를 취소한다. 워크트리만 고쳤다(미커밋). Delivery #249 는 건드리지 않았다.

| 위치 | 반영 |
|---|---|
| spec-002:42 | 개정 ⑳ 머리 메모 ⑦ — 내용 글자 = 12px · 제목과 같게 · 접힌 높이 = 12px 기준 5줄(~~E2 14px~~ 취소) |
| spec-002:182 | U-1 카드 안 오더 메모 — 12px(제목과 같게) · ~~14px~~ E2 취소 |
| spec-002:186 | U-1 「오더 메모 모양」 2번 — 내용 12px · 제목과 같게 · 12px 기준 5줄 |
| spec-002:895 | 「개정 ⑳ — 기획안 · 시안과 달라진 곳」 E39 행 — 12px(제목과 같게) · 근거에 F1 |
| spec-003:62 | 개정 ⑬ 메모 안 「14px」 → 「12px — DAY-SPEC-002 F1」(앱 변경 0 그대로) |
| log.md:17 | 개정 ⑳ 행 「오더 메모 14px」 → 「오더 메모 12px(제목과 같게 · 사용자 2026-11-12 F1 — E2 14px 취소)」 |

- 남은 「14px」는 전부 취소선 · 취소 기록이다(grep 확인).
- 제목 「오더 메모」 글자 크기를 12px 로 적은 것은 F1(코디 전달) 그대로다.
- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning · `products/day` 0.

## 리뷰 반영 4 — consultation(visit_id) 부분 인덱스 (2026-11-12)

backend 의 migration `0009_consultation_visit`(be-3-report)에 맞췄다. 사용자 결정은 「이번에 같이」다. 파일만 고쳤고 커밋은 하지 않았다(브랜치 커밋 `cfc72539` 위 미커밋 · 코디가 커밋). Delivery #249 는 건드리지 않았다.

| 위치 | 반영 |
|---|---|
| spec-000:8 | `last_updated` 2026-11-12 |
| spec-000:507 | `consultation` 표 아래 「인덱스」 줄 추가 — (`visit_id`) 부분 인덱스 `ix_consultation_visit_id` · `deleted_at IS NULL` · migration `0009_consultation_visit` · 칸 변경 없음 |
| spec-002:42 | 개정 ⑳ 머리 메모를 「migration 없음」에서 「migration = 인덱스 하나(`0009` · 칸 변경 없음)」로 바꿈(⑦ 문장 · 끝 문장 두 곳) |
| spec-002:188 | U-1 상담사 배지 「migration 없음」 → 「칸 변경 없음(migration 은 부분 인덱스 하나)」 — 같은 파일 안 모순을 없앰 |
| log.md:17 | 새 행 `spec-change` DAY-SPEC-000 · DAY-SPEC-002 — 인덱스 · E3 문구 바로잡음 |

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning · `products/day` 0.
- **주의**: Delivery #249 의 Non-Goals 에 「DB migration」이 있다. v2 재결속 때 「칸 변경 없음 · 인덱스 하나 예외」로 고쳐야 한다.
