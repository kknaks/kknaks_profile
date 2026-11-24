# [backend] fix-1 — 코드 검수 review-code-1 반영 (C18 · C19 · C20 · C21 · W6 · W7)

읽을 것(이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`): `review-code-1-report.md` W1 · W2 · W4 · W5 · W6(README 부분) · W7 · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` C18 ~ C21 · SPEC 고침 `planner-fix-3-report.md`(규칙 31 새 문장 — SoT).

- C18(W1): `policies/board_chart_tabs.py` DAY 쪽 판정 — `baseLogId` 뒤 이력이 전부 `source=kos` 이고 마지막 값 == 요청 base 면 걸리지 않음. 테스트: 409 → 동기화(`source=kos` 이력 추가) → 다시 저장 = 200 · 글 한 번만.
- C19(W2): 마지막 이력 = 같은 직원 · `source=day` · 같은 글 · 담당자면 그 줄 건너뜀(저장 0 · 걸림 0). 테스트: 커밋 뒤 응답 유실 흉내 → 같은 요청 다시 = 200 · 이력 1개. README `:197-198` 문장 바로잡기.
- C20(W4): `chart_text` 비교 정규화 CRLF · CR → LF. 테스트 포함.
- C21(W5): 집도의 「한 명」 = 매핑 전 KOS 외부 id 개수 — `chart_base` 와 `_kos_values` 같은 단계.
- W7: `"staff_not_listed"` → `common/error_codes.py` 상수.

검증: `scripts/test.sh -q backend/tests/day/board` · ruff · mypy(만진 파일). 커밋 금지. frontend 가 병렬로 `day.js` · 템플릿을 고친다 — 건드리지 마라. 보고 `be-fix-1-report.md` + preamble worker_done 두 채널.
