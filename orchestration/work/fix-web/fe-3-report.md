# fix-web fe-3 결과 보고 — E1 · E2 · E4 방 카드 오더 메모 (frontend)

## 상태: done (infra 테스트 pending — fe-1 과 같은 사유)

## 수행
| 파일 | 무엇 |
|---|---|
| `backend/day/templates/ui.html` `memo()` | 제목 줄 `.day-memo__head` = `<span class="day-memo__title">오더 메모</span>` + 상담사마다 `sq_badge(name, "gray")`(기존 배지 매크로 · 11px) + 5줄 넘을 때만 오른쪽 끝 `<button class="day-memo__more" data-day-memo-toggle>펼치기/접기</button>`(아이콘 · aria-label 대체 — 보이는 글자가 이름). 그 아래 `.day-memo__box` 내용. 구분선 없음. 새 인자 `counselors=[]` |
| `backend/day/templates/partials/board_parts.html:170` | `counselors=card.counselors or []` 전달(키 없을 때도 안전). 메모 없으면 칸 없음 그대로 |
| `backend/day/static/day.js` | 토글 때 글자 「펼치기」↔「접기」(aria-label 대신 textContent) · 다시 그릴 때 펼침 복원(restoreState)도 글자 맞춤 · 머리 주석 |
| `backend/day/styles/app.css` → `static/day.css` 재빌드 | `.day-memo` 세로 배치 gap 4 · `.day-memo__head`(flex · wrap · gap 4) · `.day-memo__title` 12/500 secondary · `.day-memo__box` **14px**(오른쪽 아이콘 자리 22px 패딩 삭제) · `--day-memo-max-h` **93px**(14 × 1.3 × 5 = 91 + 여유 2 — 앞과 같은 여유) · `.day-memo__more` 파란 글자(`--day-text-brand` 토큰 · 12/500 · 배경 없음 · hover/focus `--ms-primary-100`) — 기존 토큰만 |
| `backend/day/routers/kit_board.py` | 견본 world 상담사 2명((HAR 의 상담사) · 한소라 · `BStaff(…, False)`) · 시술실 A(6줄 메모) 2명 · 레이저실 1 1명 · 레이저실 2 에 짧은 메모 + 0명. backend 의 `BVisit.counselor_ids` → 스냅샷 `cards[].counselors` 로 소비 |
| `backend/day/templates/partials/kit_page.html` | G10 메모 견본 = 상담사 0 · 1 · 2명 · 펼치기 · 접기 |
| `backend/tests/architecture/test_screen_copy.py` | 근거 「오더 메모」(E4) · 「펼치기」(E1) · 「접기」(시안 + E1). 「메모」 · 「메모 접기」 · 「메모 크게 보기」 · 「크게 보기」 근거 삭제 → 「메모 크게 보기」 · 「메모 접기」 · 「크게 보기」 지운 문구 목록에 |
| `backend/tests/day/web/test_board_page.py` | `test_오더_메모_제목_줄_상담사_배지_펼치기`(V1 배지 2 + 펼치기 · V2 배지 1 · V3 배지 0 · 버튼은 5줄 넘을 때만 · 구분선 없음 · aria 「메모 …」/maximize 없음 · CSS 14px · 93px · js 글자 전환) · `test_오더_메모_펼침은_접기_글자`(open=true → 「접기」 · 상담사 없으면 배지 없음 · 제목만) |

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture` → **123 passed**
- `uv run pytest -q -m "not infra" backend/tests` → **933 passed, 319 deselected**(backend 동시 변경 포함)
- `ruff check backend` OK · `ruff format --check` OK · `node --check day.js` OK · `scripts/build-css.sh` 재빌드
- 추가 줄 인라인 스크립트 · `style=` · `onclick` · `eval(` grep → **0** · 손 CSS 없음(app.css 클래스 규칙 + 기존 토큰)
- pending: `scripts/test.sh`(infra) — 사용자 `day-local` DB 뿐이라 미실행 · 브라우저 눈 확인 안 함

## 계약
- `cards[].counselors: [{staffId, name}]` 그대로 소비(이름만 표시 · 순서 = 서버 순서). 없으면 제목 「오더 메모」만. 앱 변경 0.

## 코디가 확인할 것
- 배지 색: 시안 없음 — 회색 solid(`sq_badge gray`)로 둠. 제목 글자 12px/500 secondary 도 시안 없음(카드 머리 제목과 같은 크기).
- 상담사가 많으면 제목 줄이 줄바꿈된다(flex-wrap) — 「펼치기」는 마지막 줄 오른쪽 끝.
