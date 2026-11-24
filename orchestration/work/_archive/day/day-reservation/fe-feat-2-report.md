# fe-feat-2 결과 보고 — 담당자 「미정」 표시(e2e E4 · E5 화면 쪽)

## 상태: done (실물 확인은 backend `card.staff` 가 붙은 뒤 · 스택 안 건드림 · 커밋 안 함)

## 수행
- **E4** `partials/reservations_parts.html` `inhouse_card` — 접수가 아닌 카드(= 상담 대기부터)는 선 아래 「상담」 줄을 늘 그린다 · 값 = `counselor_name` 있으면 「○○ 실장」, null 이면 「미정」(R48 「있을 때만」 뒤집음). 금액 줄 규칙은 그대로.
- **E5** `partials/reservations_parts.html` `card` — `card.staff = {role, name|null}|null`(backend 필드 이름 그대로) → 이름 · 국적 줄 아래 한 줄 `day-res-card__staff`: counselor = 「상담사 ○○○」/「상담사 미정」, doctor = 「담당의 ○○○」/「담당의 미정」, null(또는 키 없음 · 다른 role) = 줄 없음. 어느 단계에 줄을 줄지는 서버 판정(화면은 staff 만 봄).
- `styles/app.css` → `static/day.css`: `.day-res-card__staff`(12px/1.3 · tertiary · 한 줄 말줄임 · margin-top 2px) — 카드 높이 66px(안쪽 56px) 그대로, 이름 + 국적 · 배지 줄 ~38px + 담당자 줄 ~18px 로 안에 든다. 귀가 카드 흐림 · 카드 폭 규칙은 기존 그대로 적용.
- `tests/architecture/test_screen_copy.py` — 사용자 확정 문구 「미정」 · 「상담사」 · 「담당의」(근거 = e2e-1 E4 · E5).

## 시험
- `backend/tests/day/web/test_reservations_screen.py` — `_card` 기본 `staff: None` · TODAY_VIEW 상담 대기 카드에 `staff{counselor, null}` · 새 시험 `test_표_카드_담당자_한_줄`(상담사 미정 · 상담사 박예진 · 담당의 미정 · 담당의 김원장 · null = 줄 없음) · 원내 카드 단언을 E4 로 고침(박진행 「상담 미정」 · 홍귀가 귀가 대기 「상담 미정」) · 고정본 다시 씀.

## 검증
| 명령 | 결과 |
|---|---|
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 498 passed |
| `uv run pytest tests/day/web/test_reservations_screen.py`(고정본 포함) | 17 passed |
| `npm run check` | 통과 · node 109 pass |
| ruff check · format | 통과 |

## 볼 것
- 지금 트리의 backend presentation 에는 아직 `staff` 키가 없다(동시 작업) — 키가 없으면 줄이 안 나올 뿐 깨지지 않는다. 붙은 뒤 실물에서 확인.
