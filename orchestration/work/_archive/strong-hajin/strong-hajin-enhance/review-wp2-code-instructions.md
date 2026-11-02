# [reviewer 코드 검수] WORK-012 WP2 (BE + FE)

기존 브리프(`strong-hajin-enhance-review-brief.md`)의 규칙 그대로 — **읽기 전용**, 리포트 한 장, 시험·빌드·서버 실행 금지(수치는 워커·코디가 낸다).

- 대상: 코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance` 의 **미커밋 변경 전부**(WP1 은 커밋 `e51fe3b` — 그 뒤 변경만)(`git diff` · `git status` — 새 파일 포함)
- 계약: `P/30-work/work-012-enhance.md` 「Phase WP2-BE」·「Phase WP2-FE」 의 체크박스 + Code Surface WP2 표 · SPEC-010 · SPEC-008 v0.6.0 해당 절 · 추가 SH-IMP-020(`P/improvements/SH-IMP-020-quick-meeting-label.md`)
- 워커 리포트: `W/be-wp2-report.md` · `W/fe-wp2-report.md` · 기준선 `W/be-baseline.md` · `W/fe-baseline.md`

물음:
1. 계약 체크박스마다 구현됐나(파일:줄) — 빠진 것·다르게 한 것
2. **Code Surface 전수** — WP1 표의 자리를 네가 다시 grep 해 변경이 닿았나. 같은 심볼·패턴을 쓰는데 안 닿은 자리
3. BE↔FE 계약 일치 — 안건 `source` 페이로드 · `download=1` · 받기/원본 주소 · `integration.changed` 사건 모양
4. 회귀 위험 — 기한 규칙 변경이 다른 호출자에 · `download=1` 이 미리보기 경로에 · SVG 허용이 첨부(`_download`) 경로에 새지 않나 · 공유 상수 분리(「빠른 회의」)
5. 시험이 계약을 실제로 잡나(이름만 있고 단언이 약한 시험)
6. **사람 눈에 이상해 보일 자리** — 앱 E2E 에서 사용자가 걸릴 곳

리포트: `W/review-wp2-code-report.md` · 판정 PASS/WARN/FAIL · §끝에 FAIL/WARN 목록(워커 재발주용, BE/FE 구분).
완료 보고: 기존 브리프 §6 두 명령(subject 「reviewer 완료: WP2 코드 검수 <판정>」, 리포트 이름만 바꿔서).

## WP2 에서 특히 볼 것
- 추가 계약: 보정 표 위치 = 회의 상세 응답 **최상위 `term_corrections`**(null/[]/행 — 코디 판정, SPEC-010 반영) · 상세 모양을 돌려주는 응답 전부(PATCH 포함)
- 새 표 `meeting_term_corrections` · `meetings.term_corrected_at` + 운영 SQL `migrations/manual/2026-10-07-meeting-term-corrections.sql` — 스키마 경로가 코드 레포 규칙(일반 API startup DDL 금지)을 지키나 · 운영 SQL 과 ORM 이 일치하나
- timeout 새 세션 재시도: 세션 교체 시점 · 배치 한 줄(겹침 없음) · 재시도 중 도착분 합치기 · 워커 lease 바닥 3300초가 최종 900초 × 시도와 맞나
- AI 맥락 목록: 조직 전체 · 완료/취소 업무 제외 · 매 턴 실음 — 크기 상한 없음(BE 미결)
- BE 리포트 「미결」 6개를 하나씩 판정(결함인가 · 계약대로인가)
