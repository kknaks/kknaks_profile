# planner-local-alignment-fix 결과 보고 — 로컬 API 정합 W1 + 참고 최소 보완

## 상태: done (커밋 · GitHub · 승인 receipt · 20-spec.md · 타 SPEC · 코드 변경 없음)

## 수정 위치

### `products/day/20-spec/spec-003-mobile-app.md` (미커밋 · 개정 ② 위 제자리)

| 자리 | 고친 것 |
|---|---|
| U-4 머리(`needs` 원문 문장 끝) | **표시 우선순위** 추가 — 모든 시술 완료로 머리 상태가 사용자 확정 「시술 모두 완료 · 귀가 대기 전」이면 `needs` 의 `home` 「귀가 대기 전」을 머리에 따로 칩 · 글자로 그리지 않음(합성 머리 한 번) · 다른 needs(`wait` · `anes` · `call` · `accept`) 원문은 그대로 |
| U-3 확인 필요 테두리 | 사실 추가 — 모든 시술이 끝나는 순간 서버가 `home` 을 싣고 `inbox.section = need` → 카드 테두리 빨강 · 「확인 필요」 칩 집계에 들어감 = 서버 값 소비 · 앱이 지우거나 바꾸지 않음(옆 SPEC-002 @e421b77b 규칙 16 · `board_rules.py:466-470`) |
| A-33 | 모두 완료 때 머리 합성 글자 한 번 · `home` 글자 중복 없음 · 테두리 · 칩은 서버 값 그대로 |
| A-37 | 모두 완료 상태의 `home` 글자는 합성 머리가 대신(A-33) |
| OQ-A29 기본값 | 위 우선순위 명시(서버 `needs.home` · 테두리 · 칩 집계는 그대로 · 리뷰 확인) |
| A-31 · A-32 실물 칸 | 「✓ dev」 → 「✓ 로컬 day-local(D-6 뒤 dev)」 |

모두 완료 강조 상자(「시술 모두 완료」 · 「마지막 종료」 · [귀가 대기]) · `canHome` · 서버 판정 · 새 글자 · API 변경 없음.

### `delivery-request-v3.json` (contract_version 3 그대로 · 항목 수 그대로 — acceptance 27)

| 경로 | 고친 것 |
|---|---|
| `acceptance[0]` | 「완료 정의(v2)」 → 「완료 정의(누적 v3)」 · 「v2 완료 근거가 아니다」 → 「v3 …」 |
| `acceptance[2]` A2 | 통합 검증 = 사용자 로컬 day-local(a1c90b9d · D-6 전 · dev 91728737 엔 canRecall 없음 · D-6 뒤 dev) |
| `acceptance[21]` A21 | 모두 완료 때 머리 합성 글자 한 번 · `needs.home` 따로 안 그림 · 서버 needs · 테두리 · 칩 집계 그대로(U-4 · OQ-A29) |
| `acceptance[26]` A26 | 「귀가 대기 전」 원문 뒤에 「모두 완료면 home 글자는 합성 머리가 대신 — A21」 |

exact SHA 결속은 그대로 — SPEC 원천 「1551fa22 + 개정 ②(미커밋 · 코디 커밋 head 로 결속)」 표기 유지.

## 검증

- `git diff --check` → 통과
- `delivery-request-v3.json` JSON parse 1회 → OK(contract_version 3 · acceptance 27)
- 전체 lint · schema 는 의미 있는 구조 변경이 없어 반복하지 않음(문장 · 표 셀만 수정 · 키 · 항목 수 불변)

## 미결

- 리뷰 참고 중 U-8 「정확히 20분은 초과 아님」(a1c90b9d 기준 분 = 서버 설정)은 브리프 범위 밖이라 그대로 — 업무 판정은 `long` 소비라 영향 없음.
- A-33 실물 칸은 「✓ dev」 그대로(브리프가 A-31 · A-32 만 지정 · `canHome` 은 dev 에도 있음).
- 다음: 코디 개정 ② 커밋 → v3 plan → L3 승인 → mobile 발주.
