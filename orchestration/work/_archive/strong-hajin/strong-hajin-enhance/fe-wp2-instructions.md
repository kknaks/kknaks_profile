# [frontend] WORK-012 Phase WP2-FE — 다음 판

기존 구현 브리프(`strong-hajin-enhance-fe-impl-brief.md`)의 규칙 그대로(allowed_paths · 하지 말 것 · 커밋 금지 · 포트 금지). **WP1 은 커밋됐다(`e51fe3b`)** — 그 위에서 이어 간다.

- 할 일: `P/30-work/work-012-enhance.md` **「Phase WP2-FE」 절의 계약 체크박스 전부** + Code Surface WP2 표의 자리 전부(표 밖에서 같은 심볼을 쓰는 곳도)
- 계약: SPEC-010 해당 절(맥락 목록 · timeout · 정정 pass · 보정 표 · 안건 순서 · 배치 한 줄 · 새 세션 재시도) · DEC-009
- WP2-BE 와 병렬이다. 보정 표 응답 모양(`term_corrections`: `null` / `[]` / 행 목록)·안건 순서는 WORK-012 WP2-BE 절과 SPEC-010 에 고정돼 있다 — 그 계약대로 소비하라
- 검증: `npx vitest run --no-file-parallelism`(직렬 — 병렬 금지) · `make frontend-build` — 기존 실패는 `W/fe-baseline.md` 와 대조해 분리
- 리포트: `W/fe-wp2-report.md` (체크박스별 파일:줄 · 닿은 자리 개수 · 새 시험 · 검증 수치 · 미결)
- 완료 보고: 기존 브리프 §7 두 명령(subject 「frontend 완료: WP2-FE」, 리포트 이름 fe-wp2-report.md). **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
