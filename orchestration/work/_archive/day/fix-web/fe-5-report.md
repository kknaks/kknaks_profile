# fix-web fe-5 결과 보고 — E2E 2회차 F1: 오더 메모 내용 12px (frontend)

## 상태: done (infra 테스트 pending — 앞과 같은 사유)

## 수행
| 파일 | 무엇 |
|---|---|
| `backend/day/styles/app.css` | `.day-memo__box` font-size 14px → **12px**(`.day-memo__title` 12px 와 같음) · `--day-memo-max-h` 93px → **80px**(12 × 1.3 × 5 = 78 + 여유 2 — 1차 값) · 주석 근거 「E2E 2회차 F1」 |
| `backend/day/static/day.css` | `scripts/build-css.sh` 재빌드 — HEAD 대비 메모 값 = max-h 80px · 내용 12px |
| `backend/day/templates/ui.html` | memo 매크로 주석의 E2(14px) 근거 → 「2회차 F1 내용 12px」 |
| `backend/tests/day/web/test_board_page.py` | 메모 테스트 CSS 단언: `.day-memo__box` 12px · `.day-memo__title` 12px · `--day-memo-max-h: 80px` · docstring 근거 갱신 |

「펼치기」 표시는 fe-4 그대로(높이를 day.js 가 잼 — max-h 토큰만 바뀌어 별도 변경 없음).

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture` → **123 passed**
- `uv run pytest -q -m "not infra" backend/tests` → **936 passed, 320 deselected**
- `ruff check backend` OK · `ruff format --check` OK
- 인라인 스크립트 · 손 CSS 추가 없음(app.css 기존 규칙 값만)
- pending: infra(`scripts/test.sh`) · 브라우저 눈 확인
