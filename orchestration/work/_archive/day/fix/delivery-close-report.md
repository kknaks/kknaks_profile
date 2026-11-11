# Delivery #241 — baseline 재결속 · 머지 마감 결과

## 상태: 막힘(규칙대로 멈춤) — 닫지 않음 · 아무것도 쓰지 않음

| 항목 | 값 |
|---|---|
| Issue | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/241 — **OPEN** |
| 라벨(그대로) | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| contract_version | 5 그대로(v6 은 `--plan` 만 · 적용 안 함) |
| baseline | **pending** — mediness `origin/main` = `1a450bcf7f0ed97128a7210bdccb7331ed0fa890`(#929 스쿼시) 에서 다시 봐도 CLI `missing_target_specs = [DAY-SPEC-000]` |
| 이유 | DAY-SPEC-000 이 main 에서 `status: draft` — 「stable SPEC 없음」으로 본다. stable 로 올리는 것은 사람 판단이라 고치지 않았다(우회 안 함) |
| 코드 PR | #242 MERGED → `dev` · head `87cf2dec9e62db937cdcb6cc9c52f010baed8357` · merge `7b099e8f2973003f4d5203d082ca2a81ced23ec8` |
| review-delivery | **못 함** — `--plan` 결과 `{"status":"conflict","error":"delivery review requires a ready stable SPEC baseline"}`(harness `workflow.py` `review_delivery` 가 baseline ready 를 먼저 요구). `--apply` 는 실행하지 않음 · Issue · PR 에 쓴 것 0 |
| next_action | `review-delivery-plan`(v6 plan — 아래) → 실제로는 **SPEC-000 stable 결정이 먼저** |
| 닫혔나 | **아니오** |

## 한 일

1. `git fetch origin` → `origin/main` = `1a450bcf…`. 워크트리 파일 수정 0.
2. 재결속 request v6(같은 key `day/fix-device-feedback-interpret` · contract_version 6 · `spec_baseline_revision = 1a450bcf…` · 결과 계약 v5 그대로)을 `start-delivery --plan` 으로 확인:
   - `spec_baseline_state = pending` · `missing_target_specs = [DAY-SPEC-000]`
   - `plan_digest = sha256:3fb28dfcc23cf85cf8e6804faf752d47e34fa951119b4ed18a32f50eb7d78288` — **v5 승인 digest 와 같다**(재결속만으로는 재승인이 필요 없는 모양) · contract_digest(v6) = `sha256:f6668fca5be6c2b0a8c157c07fc46c58c1b9b1c57c012a032d083354d1d5020d`
   - pending 이 그대로라 **적용하지 않았다**(revision 만 바뀐 pending 을 기록하는 것은 막힌 상태를 우회하는 것과 다르지 않고, 다음 단계(review)를 열지 못함).
3. `review-delivery --plan`(읽기 전용 · 수용 항목은 `undetermined` 로만 넣어 아무것도 「통과」로 적지 않음) → conflict(위). 실기기 · TestFlight 몫은 한 것으로 적지 않았다.
4. 2차 Delivery(#234 · #235 · #236 · #239) 손대지 않음 · MCP Task 카드 처리 0.

## 사용자가 정할 것

1. **DAY-SPEC-000(데이터 모델)을 `stable` 로 올릴지** — 이것 없이는 #241 이 `spec-baseline:ready` 가 될 수 없고, 그래서 머지 마감(review-delivery → spec-sync → 닫기)을 시작할 수 없다. 2차 Delivery #234 · #239 도 같은 SPEC-000 을 target 으로 pending 이라 함께 정할 일이다.
   - 올리면: 스펙 PR(SPEC-000 `status: stable`) 머지 → 같은 key · v6 · 새 `origin/main` 으로 재결속(`plan_digest` 가 지금처럼 같으면 재승인 없이 ready) → `review-delivery`(merge `7b099e8f…`) → `run-spec-sync` → 닫기.
   - 안 올리면: #241 은 pending 으로 남고 닫을 수 없다(규칙상 우회 길 없음). 다른 길(target SPEC 에서 SPEC-000 을 빼기)은 결과 계약 변경(version 올림 · 재승인)이라 사람 판단.
2. **실기기 · TestFlight 확인**(아직 안 함) — review-delivery 때 수용 항목 A7 · A11 · A14(사용자 실기기 — 통역 긴 세션 · 채팅 사진 · 읽음 숫자 · 하단 메뉴 등)와 TestFlight 빌드 2 결과가 있어야 그 항목을 「통과」로 적을 수 있다. 없으면 그 항목은 `undetermined` 로 남고 마감 판단이 사람에게 간다.

## 코디 실물 확인(브리프 · 기록만)

dev 서버: 통역 사전 로그 `glossary seed loaded: version=2026-10-27.6` · 저장소 올리기 → 크기 → 전체/범위 읽기 → 경로 `chat/{병원 id}/…` → 없는 키 → 지우기(관리 ID · 컨테이너 `dev`) 통과 · api 오류 로그 0 — review-delivery 를 할 수 있게 되면 A4 · A8 · A13 근거로 쓸 수 있다.

## 파일

- `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v6.request.json` · `fix.v6.plan.json`(적용 안 함)
- 같은 폴더 `fix.review.request.json` · `fix.review.plan.json`(conflict)
