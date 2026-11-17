# SPEC-001 · SPEC-002 0.3.0 재검수 2 지시서

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-review-doc-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · 무엇을 보나(§2 의 1~8) · 제약 · 검증 · §9 완료 보고는 그대로 적용한다.

경로: `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것(더)

1. `$W/review-spec-001-002-r2.md` ← 2차 검수(WARN 6 · NOTE 9)
2. `$W/spec-fix2-instructions.md` · `$W/spec-fix2-addendum.md` ← 수정 지시 + **사용자 원칙(폭은 빠짐없이 · 깊이만 Jev)**
3. `$W/_RESUME.md` §2 맨 위 두 행(원칙 · 재검수 뒤 결정 2)
4. 두 SPEC 맨 끝 「변경 기록」

## 할 것

1. r2 지적 15 · 결정 2 가 닫혔는지 — 닫힘 / 부분 / 안 닫힘 + 문서:줄.
2. **원칙 전수 대조** — SPEC-002 · SPEC-001 전체에서 폭이 Jev 점수 · 상한 · 상위 N · 잘라 내기 · 「보류 = 빠짐」 으로 줄어드는 자리가 남았는지 grep + 읽기로 전수. 종료 조건이 「폭 다 읽음 + 깊이 판단 끝 + gate」 인지. 남으면 FAIL.
3. 새로 쓴 곳(deepen / listed_only · G9 · D7 폭 누락 · O-18 · O-19 · 키 코드 칸 표 · asked_fields[])을 1차 기준으로 새로 검수 · 인용 표본 10 이상 · 숫자 5 이상 다시 셈.
4. 열린 것 표의 상태 칸(사용자 결정 대기 / 1회차 trace 뒤 / 구현 때)이 맞는지, **WORK(구현 계획) 시작 전에 사용자가 정해야 하는 것**만 따로 목록.

## 산출

- `$W/review-spec-001-002-r3.md` **1개만**. 머리에 문서별 판정 + r2 지적 닫힘 표 + 원칙 대조 결과 + 새 지적 + 「WORK 전 사용자 결정 목록」.
