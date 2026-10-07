# [backend] WORK-012 Phase WP2-BE — 다음 판

기존 구현 브리프(`strong-hajin-enhance-be-impl-brief.md`)의 규칙 그대로(allowed_paths · 하지 말 것 · 커밋 금지 · 포트 금지). **WP1 은 커밋됐다(`e51fe3b`)** — 그 위에서 이어 간다.

- 할 일: `P/30-work/work-012-enhance.md` **「Phase WP2-BE」 절의 계약 체크박스 전부** + Code Surface WP2 표의 자리 전부(표 밖에서 같은 심볼을 쓰는 곳도)
- 계약: SPEC-010 해당 절(맥락 목록 · timeout · 정정 pass · 보정 표 · 안건 순서 · 배치 한 줄 · 새 세션 재시도) · DEC-009
- WP1 검수 WARN 함께: **W-5** 계약 시험 앱에서 연동 사건 묶음 타이머를 `coalesce_seconds=0` 으로 주입(진짜 1초 타이머가 시험에서 돌지 않게) · **W-7** `external_inbox_upstream.py:91` `REMOTE_IMAGE_TYPES` 죽은 상수 정리
- **외부 서비스 실물**: 정정 pass·다시 쓰기는 Codex 를 부른다 — 단위 시험은 가짜로 하되, 리포트에 「실물 1회 확인은 코디 E2E」 로 남겨라(네가 실물 Codex 를 부르지 마라)
- 새 테이블/컬럼(용어 보정 표 · `term_corrected_at`)은 코드 레포 규칙대로 — 스키마 변경 경로는 `AGENTS.md` 를 따른다(일반 API startup DDL 금지)
- 검증: `make test-unit` · `make test-contract` · `make test-postgres` · 인벤토리 drift · 마지막 `make test` — 기존 실패는 `W/be-baseline.md` 와 대조해 분리
- 리포트: `W/be-wp2-report.md` (체크박스별 파일:줄 · 닿은 자리 개수 · 새 시험 · 검증 수치 · 미결)
- 완료 보고: 기존 브리프 §7 두 명령(subject 「backend 완료: WP2-BE」, 리포트 이름 be-wp2-report.md). **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
