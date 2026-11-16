# [backend] WP19 수정 — 리뷰 W-1(아주 큰 N 에서 기동 실패)

리포트: `orchestration/work/interpreter-idea/review-wp19-code-report.md` W-1. SPEC §5.9 표를 코디가 고쳤다(커밋 전 — 코디 워크트리 SPEC 을 다시 읽어라).

- **N 범위 = 1 ~ 36,500**(100년). 넘으면 「그 밖의 값」 — 경고 1줄 · off · 기동 성공
- `parse_keep_days` 가 **어떤 문자열에도 예외를 올리지 않게** — 4,300 자리 넘는 숫자(`int()` ValueError)도 경고 · off. `int()` 전에 자릿수로 걸러도 된다
- 시험 추가: `36500` → N(기동 성공 · `keep_days=36500`) · `36501` · `1000000` · `"9"*5000` → 경고 1줄 · off · 기동 성공(TestClient lifespan)
- 그 밖 변경 금지 · 관문 명령 1회 · `wp19-be-report.md` 끝에 「수정 1」 절 추가 · 완료 보고는 브리프 §9 그대로(같은 task · dispatch id)
