# SPEC-001 · SPEC-002 0.2.0 재검수 지시서

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-review-doc-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · 무엇을 보나(§2 의 1~8) · 제약 · 검증 · §9 완료 보고는 그대로 적용한다. 다른 점만 아래에 있다.

경로: `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것(더)

1. `$W/review-spec-001-002.md` ← 1차 검수(FAIL 1 · WARN 11 · NOTE 10)
2. `$W/spec-fix1-instructions.md` ← 수정 지시
3. `$W/_RESUME.md` §2 맨 위 행(11-16 「검수 뒤 결정 4」) ← 사용자 결정
4. 두 SPEC 맨 끝 「변경 기록」 절(지적 → 고친 줄)

## 할 것

1. 1차 지적 22 건마다 닫혔는지 — 닫힘 / 부분 / 안 닫힘 + 문서:줄.
2. 결정 4 · 추천 확정 6(SPEC-002 O-3 · O-4 · O-6 · O-12 · O-13 · O-14)이 본문에 맞게 들어갔는지.
3. **이번에 새로 쓴 곳**(보조 입력 2종 · `facets.hier` · `ledger_check[]` · 답 키 재추출 절차 · A 열 MCP 3 · 단계 6b)을 1차와 같은 기준(§2 의 1~8)으로 새로 검수. 인용 표본 10 개 이상 · 숫자 5 개 이상 다시 센다.
4. 새로 열린 SPEC-001 O-13(하위 1단 vs 자손 전부) · O-14(ledger_check 범위)의 주장 수치(부작용 5개 +390 행 · 조건 10개 +77 행 · 제품 213건)를 gold/silver 로 확인.

## 산출

- `$W/review-spec-001-002-r2.md` **1개만**(1차 리포트는 고치지 마라). 머리에 문서별 판정 + 1차 지적 닫힘 표 + 새 지적 표.
