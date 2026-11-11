# 리뷰 리포트 — day-app 로컬 API 정합 W1 재검수 / doc (2026-11-10)

- 대상:
  - 스펙 트리 HEAD `1551fa22` 위 미커밋 `products/day/20-spec/spec-003-mobile-app.md`(+43/−28 · 앞 리뷰 +42/−27)
  - profile `delivery-request-v3.json` · `planner-local-alignment-fix-report.md`
- 근거:
  - 앞 리뷰 `review-local-alignment-report.md` W1 · 참고
  - `local-alignment-fix-brief.md`
  - 옆 SPEC-002 @`e421b77b` 규칙 16 · 코드 @`a1c90b9d` `board_rules.py:466-470`(앞 리뷰 실측)
- 방법:
  - 수정 문장을 직접 대조했다.
  - diff hunk 목록을 앞 리뷰와 비교했다.
  - v2 ↔ v3 경로 diff로 바뀐 키 집합을 비교했다.
  - `git diff --check`와 JSON 파싱을 한 번씩 했다. 전체 lint · schema는 지시대로 반복하지 않았다.
  - 스펙 · JSON · 코드는 수정하지 않았다.

## 판정: PASS (FAIL 0 · WARN 0)

## W1 — 해소

| 확인 | 위치 | 결과 |
|---|---|---|
| 중복 문구 제거 · 합성 머리 한 번 | `spec-003-mobile-app.md:207` U-4 「표시 우선순위」 | 모두 완료로 머리가 「시술 모두 완료 · 귀가 대기 전」이면 `needs.home` 「귀가 대기 전」은 따로 칩 · 글자로 그리지 않는다. 다른 needs(`wait` · `anes` · `call` · `accept`) 원문은 그대로다. 새 글자는 없다(두 글자 모두 기존 원천) |
| 서버 판정 보존 | `:198` U-3 | `home`이 실리면 `inbox.section = need` → 테두리 빨강 · 「확인 필요」 칩 집계에 들어간다는 것을 **서버 값 소비 결과 · 앱이 지우거나 바꾸지 않음**으로 사실 기록했다(규칙 16 · `board_rules.py:466-470` — 원천과 일치) |
| 모두 완료 상자 · 버튼 | `:692` A-33 | 강조 상자 「시술 모두 완료」 · 「마지막 종료」 · [귀가 대기](`canHome`) 그대로 + 「머리 합성 글자 한 번 · home 따로 안 그림 · 테두리/칩은 서버 그대로」 |
| A-37 | `:696` | 5상황 원문 · 재판정 없음 유지 + 「모두 완료 상태의 home 글자는 합성 머리가 대신(A-33)」 — A-33과 모순 없음 |
| OQ-A29 기본값 | `:761` | 우선순위 명시(서버 `needs.home` · 테두리 · 칩 집계 그대로 · 다른 needs 원문 그대로 · 리뷰 확인) — 기본값 진행 UI OQ로 남겼고 승인 게이트는 없다 |
| WP v3 A21 · A26 | `$.acceptance[21]` · `$.acceptance[26]` | SPEC A-33 · A-37과 같은 문장 · 같은 범위 |

## 참고 정정 — 해소

| 확인 | 결과 |
|---|---|
| A-31 · A-32 실물 칸 | `:690` · `:691` 「✓ dev」 → 「✓ 로컬 day-local(D-6 뒤 dev)」 |
| v3 A2 통합 검증 | `$.acceptance[2]` 「사용자 로컬 day-local(a1c90b9d · D-6 전 — dev 91728737엔 canRecall 없음 · D-6 뒤 dev)」 |
| acceptance[0] 표기 | 「완료 정의(누적 v3)」 · 「v3 완료 근거가 아니다」 |
| exact SHA | 「1551fa22 + 개정 ②(미커밋 · 코디 커밋 head로 결속)」 표기 유지(브리프대로) |

## 회귀 · 무관 변경

- SPEC diff hunk 목록(33개 자리)은 앞 리뷰와 같다. 바뀐 내용은 `:198` · `:207` · `:690-692` · `:696` · `:761` 줄 안뿐이다. 6 API 소비(needs · canRecall · 확인 창 · lastSeconds · pickable · 새 오류 코드 2개) 문장, UI 13항목(A-25 ~ A-36의 나머지), SPEC-001 · D-1 · 세션 · 푸시 · 통역 절은 무변경이다.
- v3 JSON: 파싱 OK · contract_version 3 · L3 · `day/day-app` · baseline `3f57c1af…` · acceptance 27 · target_delta 15 · non_goals 11 · review_surface 10. v2 대비 바뀐 키는 28개다. 앞 리뷰 27개 + `acceptance[21]` 1개이고, `[0]` · `[2]` · `[26]`은 이미 바뀐 키 안에서 문장만 바뀌었다. 그 밖 키 변경은 없다.
- `git diff --check` → 출력 없음 · exit 0 · `git status` M 1개(spec-003). `20-spec.md` · 타 SPEC · 코드는 무변경이다.

## 참고 (결함 아님 · 선택)

- U-4에서 needs가 `home` 하나뿐이고 모두 완료일 때 머리의 「확인 필요」 라벨 자체를 남길지가 문장상 명시되지 않았다. 「home 글자를 따로 그리지 않는다」와 합성 머리 취지로 보면, 그 경우 확인 필요 라벨도 합성 머리로 갈음된다고 읽는 게 자연스럽다. 카드 테두리 · 칩은 서버 그대로다. 구현 리뷰 때 이 읽기로 확인하면 된다.
- A-33 실물 칸은 「✓ dev」로 남아 있다(planner가 의도적으로 유지 · `canHome`은 dev에도 있음). 다만 같은 행에 추가된 needs · 테두리 부분은 D-6 전 dev에 없으므로, 그 부분 실물 확인은 로컬 day-local이다.
- U-8 「정확히 20분」 표현(서버 설정 기준 분)은 범위 밖으로 남겼다. 업무 판정은 `long` 소비라 영향이 없다.

## 남은 것

- 코디: 개정 ② 커밋(exact SHA) → v3 plan(origin/main 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply → mobile 발주.
- D-6(옆 #920 · #236 머지 순서 · 사용자) · 로컬 day-local 통합 검증 · 사용자 OQ(A8 · A21 · A27 · A28 · A29 · A30).
