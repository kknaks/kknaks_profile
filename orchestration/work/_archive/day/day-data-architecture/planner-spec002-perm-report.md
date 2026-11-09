# planner-spec002-perm 결과 보고 — done (미커밋)

- **SPEC-002 개정 ⑨** — §3 에 「권한 — 1차 기본」 절 새로(원천 screen 「결정 — 시술 현황 1차 기본 권한」 그대로): 키 3(`board` view · `board` edit · `board.accept` edit) 표 · 직무 표 5줄 · 수락 = 간호사 · 원장 모두 · 태그 매핑(nurse · skincare · doctor · admin → 전부 / counselor · coordinator · call_counselor 만 → 보기 / 그 밖 없음) · 이름으로 덮는 줄(마취과 = 태그 없음 → 전부 · 경영지원 · 마케팅 = admin 태그지만 없음 · 구현은 직무 표를 정확히) · DAY_ADMIN_EMAILS 그대로 · 공용 PC = 로그인 계정 권한. API 표 권한 칸 머리 → 이 절 참조 · OQ-02 「정함」.
- **SPEC-000** OQ-04-2 — 시술 현황 몫만 닫음(다른 화면 몫은 그때).
- `log.md` 한 줄 · lint `--strict` 0 error.
