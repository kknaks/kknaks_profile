# 리뷰 리포트 — fix-web-spec / doc 재검토 (2026-11-12)

대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec` 미커밋 4파일(spec-002 개정 ⑳ · spec-003 개정 ⑬ · 20-spec.md · log.md). 기준 = 같은 브리프 · 앞 리포트 `review-doc-1-report.md`. planner 반영 기록 = `spec-report.md` 「리뷰 반영」 절(:104-118).

## 판정: PASS

review-doc-1 의 FAIL 3건 · WARN 3건이 모두 반영됐다. 새로 생긴 문제 없음.

## FAIL

없음.

## WARN

없음.

## 지난 지적 확인

| # | 위치 | 지금 | 판정 |
|---|---|---|---|
| F1 | `spec-002-procedure-board.md:414` | 시나리오 2번 취소선 + 「수락 뒤 미시작은 확인 필요에 들지 않는다(개정 ⑳ · 규칙 16)」 | 해소 |
| F2 | `spec-002-procedure-board.md:418` | 「「{원장} 수락 n분째」 카드가 있었으면 … 다시 센다」 취소선(개정 ⑳) | 해소 |
| F3 | `spec-002-procedure-board.md:858` | 규칙 31 「규칙 27 전부」 목록의 「수락 뒤 미시작」 다시 셈 취소선(개정 ⑳ 뺌) | 해소 |
| W1 | `spec-003-mobile-app.md:374` | U-11 = 「수락 대기 n」 목록 · 앞 판 「수락함」 묶음은 개정 ⑳ 에서 웹에서도 뺌 | 해소 |
| W2 | `spec-003-mobile-app.md:205` | 「시작 가능」 · 「시술 대기」 · 「수락함」 = 웹에서 개정 ⑳ 에 뺌 · 앱 칩 글자 근거로는 그대로 | 해소 |
| W3 | `spec-003-mobile-app.md:290` · `:891` | 인용 출처 = 「DAY-SPEC-002 앞 판 U-10 원문(개정 ⑳ 전)」 · 웹은 W4 로 상태 글자 · 경과 · 앱 글자 그대로 | 해소 |

## 다시 점검한 것

- 잔재: spec-002 안 「수락 뒤 미시작」 · 「수락 n분째」 출현 중 취소선 · 개정 ⑳ 기록 · 「뺐다/뺌」 문맥이 아닌 줄 = **0**(grep).
- 이번 반영분 밖 변경 없음: diff 증가분이 지적된 줄(spec-002 :414 · :418 · :858 · spec-003 :205 · :374, :290 · :891 은 기존 변경 줄 안)뿐. 4파일 외 변경 없음(`git status`).
- 결정 표 W1 ~ W11 · 결정 A 반영 · 넘침 없음 · backend 계약 일치 · OQ-56 · OQ-57 열림 상태 — review-doc-1 판정 그대로 유효.
- lint: `python3 scripts/lint-pipeline.py --strict` → **0 error, 263 warning · exit 0**. products/day 출현 0 · warning 은 전부 다른 제품(무관).

## 직원이 실물에서 만날 자리

(review-doc-1 과 같음)
- 호출 뒤 5분 전에는 웹에서 [재호출]을 누를 곳이 없음(OQ-56 · 사용자 확인 필요).
- 빈 「확인 필요」 · 「수락 대기」 탭 = 숫자 0 · 빈 목록(OQ-57).
- 깔린 앱에서도 「{원장} 수락 n분째」가 사라지고 그 카드는 「시작 가능」 칩으로 옮겨짐.

## 참고(기존 부채)

- `30-work.md` 에 Delivery #249 줄 없음 — spec-sync 몫(범위 밖).
