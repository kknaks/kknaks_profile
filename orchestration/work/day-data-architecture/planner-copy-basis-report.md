# planner-copy-basis 결과 보고 — done (미커밋)

- **SPEC-001** 「웹 화면」 절에 「화면 글자」 표 — 병원 선택(병원 고르기 제목) · 처음으로(로그인으로 돌아가기 링크) · MediSolve AI(로그인 카드 위) · DAY(로그인 카드 제목) · 「이 밖은 SPEC · 시안에 있는 글자만」.
- **SPEC-002 개정 ⑪** — §3 케이스 매트릭스 아래 「오류 · 실패 토스트 글자」 표: 409 등 조작 오류 16줄(코드 ↔ 글자 · `routers/board.py` `MESSAGES` 그대로) + SSE `kos_failed` 「KOS 반영 실패 — 데스크에서 KOS 를 확인하세요」(`KOS_FAILED_MESSAGE`) · 401 · 403 은 SPEC-001 대응표 참조. 규칙 22 의 「같은 문구는 디자인」 → 이 표 참조.
- 근거: 원천 screen 「결정 — 근거 없던 화면 문구」(사용자 2026-11-08) · frontend-copy-audit 「사용자 확인」.
- `log.md` 한 줄 · lint `--strict` 0 error.
