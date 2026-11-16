# 리뷰 리포트 — day-app 카드 상태 박스 2줄(SPEC-003 개정 ③ · WP v4) / doc · 좁은 검수 (2026-11-10)

- 대상:
  - 스펙 트리 `cdde456a` 위 미커밋 `products/day/20-spec/spec-003-mobile-app.md`(+34/−14 · 파일 1개)
  - profile `delivery-request-v4.json`
  - 최신 범위 정정 `status-box-spec-fix-report.md`(이전 `status-box-spec-report.md`의 「호출 박스 2줄」 서술은 정정으로 무효 — 그 기준으로 봄)
- 원천:
  - `status-box-spec-brief.md`(사용자 원문 3단계 + 구현 승인 「응 일단 이거 부터 바꾸고 오자」)
  - `_RESUME.md` :3-4 · :282-286
  - `delivery-request-v3.json` · `delivery235-v3-verified.json`(#235 현재 v3)
- 방법:
  - diff 직접 대조 · `git diff --check`
  - v3 ↔ v4 JSON 경로 diff · harness 모델 검증 1회
  - 전체 lint · schema는 planner 실행 로그(0 error · 0 errors)를 확인하고 반복하지 않았다
  - 스펙 · JSON · 코드 수정 없음 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

## 핵심 확인

| 확인 | 근거 | 결과 |
|---|---|---|
| 호출 박스 변경 제외 | diff hunk가 U-3 「호출 뒤 카드」 본문 · A-30에 **없다**(cdde456a 원문 그대로). 개정 ③ 머리 `:39` 「호출 상태 박스 · 호출 줄 · 수락 버튼 · 귀가 대기 자리 · … 룸 머리는 바꾸지 않는다」 · U-3 「범위」 bullet · A-28 「호출 상태 박스는 A-30 그대로」 · OQ-A21 「겹치면 호출 상태 … 개정 ③이 바꾸지 않음」. v4 `$.acceptance[18]` = v3 원문 + 「이번은 현재 상황 상자 4상태만 · 호출 정의는 v3 그대로」 | PASS — 호출 박스 2줄 · 「수락 대기 · mm:ss」 · 호출 시술명 집계 문장 0 |
| 시술 중 대표 행 일치 | U-3 시술 중 bullet: 대표 행 = 서버 순서 첫 `doing` 줄 · 그 행의 `startedAt`(mm:ss) · `doctor.name`(없으면 「담당의 미정」) · `title`을 함께 쓰고 나머지 `doing`만 「외 N개」 · 「다른 시술의 시간 · 담당의를 섞지 않음」. 담당의 bullet · 시술명 bullet · A-29 · OQ-A21 · v4 A16 · A17 · target_delta[15] · scope_delta · review_surface[10]이 같은 뜻 | PASS — SPEC · JSON 한 묶음으로 일치 |
| 4상태 2줄 · 화살표 없음 · 단수 외N개 없음 | U-3 4번 · ASCII 예 3개(`시술 중 · 05:24 / KOS-DEMO` · `마취 중 · 12:34 / 담당의 미정` · `시술 대기 · 마취 완료 20분 / 담당의 미정`) · 「1개면 외 N개 없음」 · 「화살표 · 펼침 · 3줄째 없음」 | PASS — 사용자 원문 · 최종 합의와 일치 |
| 시간 형식 | 진행 중 시술 · 마취 = 초 단위 mm:ss · 분 60 넘어도 누적(예 75:03) · 형식 변환만 · 마취 완료 = `lastSeconds ÷ 60` 내림 N분 | PASS — 업무 재계산 없음 |
| 색 · 서버 판정 | 연보라 · `anesthesia.long` 빨강 · 시술 중 DAY 주색 계열(OQ-A20) · needs · canRecall 등 그대로 | PASS |
| 옛 한 줄 정의 충돌 | 「마취 중 · HH:MM 시작 · 기준 N분 + 오른쪽 경과」 · 「한 줄 상자」 · 「시술 대기 - 마취 완료」는 U-3 · U-8 · A-29 · v4 A17에서 「대체」로만 남는다. OQ-A30 기본값도 상태 박스 2줄로 갱신 | PASS — 충돌 0 |
| 새 정책 여부 | 대기/마취 시술명 = done 아닌 줄 서버 순서 첫 값 · 담당의 = 기존 첫 담당의 fallback(OQ-A21 기존 기본값) · 모은 줄 없으면 2줄 비움(글자 짓지 않음). 모두 「앱 표시 선택 · 업무 판정 아님」으로 OQ-A21에 리뷰 확인 대상으로 남김 | PASS — 새 업무 판정 · 우선순위 · 다중 담당의 정책 없음 |
| 룸 머리 가운데 | OQ-A31 「기록해」 · 구현 안 함 · v4 scope_delta도 「구현 안 함」 | PASS — 기록만 |

## WP v4 (`delivery-request-v4.json`)

| 점검 | 결과 |
|---|---|
| 모델 | `DeliveryRequest.model_validate` OK(contract_version 4 · L3) · JSON 파싱 OK · schema 0 errors(planner 로그) |
| 같은 Delivery | idempotency `day/day-app` · baseline `3f57c1af…` pending · code_surface 「app/만」 · acceptance 27 · target_specs 그대로 |
| 버전 · 원천 | #235 현재 v3(`delivery235-v3-verified.json` · contract `e688d8a7…` 일치) + 1 = 4. scope_delta가 v3 contract · plan_digest `701c2a2a…`를 인용하고 사용자 원문 3단계 + 승인 「응 일단 이거 부터 바꾸고 오자」를 그대로 결속 |
| 최소 diff(v3 → v4) | 바뀐 키 = title · scope_delta · contract_version · acceptance[0] · [16] · [17] · [18](문장 덧붙임) · target_delta[9] · target_delta[15](추가) · review_surface[0] · [10](추가) · phases[3] · verification[0] · open_questions[0]. 그 밖(A2 · A19 ~ A26 · non_goals · dependencies · rollback 등)은 동일 |
| 기존 원칙 | PR #237 하나 · app/만 · backend 수정 없음 · 서버 판정 · API · 권한 · 세션 · 사용자 마지막 merge 무변경. 승인 receipt · 승인 주장 없음(L3 새 plan_digest 승인은 코디 몫) |
| 원천 SHA | `review_surface[0]` · scope_delta = 「cdde456a + 개정 ③(미커밋 — 코디 커밋 head로 결속)」 정직 표기 |

## 검증

- `git diff --check` → 출력 없음 · exit 0 · `git status` M 1개(spec-003). `20-spec.md` · 타 SPEC · 코드 무변경.
- planner 로그(fix 보고): lint `--strict` 0 error / 263 warning · `products/day` 0 · v4 schema 0 errors.

## 참고 (결함 아님 · 권고)

- **룸 상세 마취 진행 글자 정의**: U-8 `:278`이 옛 한 줄 정의를 「대체됐다」고 지운 뒤 「룸 상세 마취 칸의 글자는 … 그대로 둔다(OQ-A31)」고만 적는다. 그 결과 룸 상세 진행 중 마취 글자(옛 「마취 중 · HH:MM 시작 · 기준 N분 + 경과」)가 SPEC 본문에서 정의 없이 참조만 남는다. 이번 코드 범위(RoomCard._nowBox만)에는 영향이 없다. 다음 손볼 때 「룸 상세 마취 칸 = 2026-11-10 판 한 줄(HH:MM 시작 · 기준 N분 + 경과) 그대로」 한 구절을 남기면 정의가 끊기지 않는다.
- 마취 중과 시술 중이 겹칠 때(마취 진행 중 `doing` 줄 있음) 어느 상자를 보일지는 개정 ③ 전부터의 순서(마취 중 조건 먼저)를 그대로 둔다. 새로 정한 것은 없다.
- A-28 실물 칸은 「✓ dev」 그대로다. 상태 박스 2줄 자체는 dev에서도 보이지만 `lastSeconds` 부분은 로컬 day-local(D-6) 기준이다.

## 남은 것

- 코디: 개정 ③ 커밋(exact head) → v4 plan(origin/main 재 fetch) → L3 승인 → #235 apply → mobile 코드 발주(RoomCard._nowBox 4상태만).
- 룸 머리 가운데 정렬 · 룸 상세 마취 글자는 사용자 확인 뒤 별도(OQ-A31).
