# day-reservation2 1판 frontend 결과 보고 (Delivery #275)

## 상태: done (커밋 · push 안 함 — 워크트리 변경만)

## 수행 — 템플릿 · 조각 · 정적 파일
- 새 라우터 `backend/day/routers/reservation_detail.py` — GET visits/{id} · book · visits/{id}/edit · customers · POST /reservations · PUT …/schedule · POST …/cancel · PUT …/doctor · PUT /reservations/companions/group · POST …/retry · POST /reservations/retry. `routers/reservations.py` 가 include(앱 조립 그대로) · 옛 끌어 묶기 PUT /reservations/companions · …/leave 라우트 제거(D45).
  쓰기 응답 = 본문 없음 + `HX-Reswap: none` + `HX-Trigger day:res-queued{writeId, visitId, action, message}`(시안 알림 글자는 라우터 `queued_message`) · 같은 고객 = RB-11 조각(`HX-Retarget [data-day-res-dup-slot]`) · 동행 저장 = 모달 + `day:res-saved`.
- 템플릿 새로: `partials/reservations_detail.html`(모달 틀 1판 칸) · `reservations_book.html`(등록 / 변경 창) · `reservations_book_who.html`(고객 찾기 목록) · `reservations_book_dup.html`(RB-11) · `reservations_dialogs.html`(RP-04 · 우클릭 메뉴 · RC-03 · 고객 카드 · 실패 토스트 매크로) · `reservations_toast_kos_failed.html`(SSE kos_failed 본문 — backend 렌더).
- 고침: `reservations.html`(sse-connect /reservations/stream · kos_failed sse-swap · `[data-day-res-sse]` · session_expired · #reservation-float · 우클릭 메뉴) · `reservations_main.html`(10초 폴링 → SSE 다시 받기 source) · `reservations_parts.html`(카드 우클릭 켜짐 `data-day-res-ctx-on` · 빈 칸 `data-day-res-bookable` · 끌어 묶기 폼 / is-companion 제거).
- `static/day.js` — 10초 시계 제거 · SSE reservation 다시 받기(막히면 미뤘다 1초 재확인) · write_confirmed / kos_failed 로 잠금 풂 · 알림 · 모달 다시 받기 · 등록 창(찾기 · 고르기 · 새 고객 · 필수 검사 · 달력(지난 날 꺼짐) · 열별 시간 · 미리보기 카드 · 같은 고객 토큰 재전송 · 새 카드 반짝임) · 우클릭 메뉴 · 옮기기 모드(점선 · 끌기 · 미리보기 · PUT schedule) · 동행 체크(묶음 같이 체크) · 이전 방문 접기 · 「준비중입니다」 · 카드 끌어 묶기 코드 제거.
- `styles/app.css` 토큰 + 클래스 → `static/day.css` 빌드(재현 검사 통과).
- 승인 받아 allowed_paths 밖: `tests/architecture/test_screen_copy.py` VISIBLE 근거 표 84줄(시안 v9 · SPEC-007 · D 근거) · `scripts/frontend/tests/res-*.test.mjs`(폴링 · 끌어 묶기 시험 → SSE · 옮기기 · 우클릭 시험) · 고정본 2개 재생성.

## 검증
- `uv run python -m pytest -q backend/tests/day/web backend/tests/architecture` = **529 passed**(새 화면 시험 26개 포함).
- `npm --prefix scripts/frontend run check`(CSS 재현 · ESLint · Stylelint · Prettier · node 시험) = 통과 · node **125 pass / 0 fail**. 도구는 스크래치에 설치 후 임시 symlink(지움).
- ruff check / format = 통과(내 파일) · mypy(라우터 · 시험) = 내 파일 오류 0.
- 인라인 스크립트 0 · style 속성 / 태그 0(grep · test_web_rules).

## 계약 대조
- contract-v1.md 를 먼저 적고 backend 와 맞춤 — backend 서비스 이름 · 인자 · 값 이름이 그대로임(detail_view · book_view · … · retry · DETAIL_KEY · writeId).
- 보탠 줄: board_view `detail_editable`(없으면 빈 칸 등록 · 우클릭 변경/취소가 꺼진 채 보임) · 새 오류 코드 web_errors 등록 — backend 에 요청함.

## 이슈 · 코디가 확인할 것
- backend `detail_view.customer.name` = `customer.name` — U-3 은 외국인이면 한글 발음 우선(표시 이름). backend 쪽 확인 필요.
- SNS 목록에서 `etc` 는 이름이 정해지지 않아 뺐다(D54 「etc 이름은 정하지 않음」) — 사용자 확인.
- [접수] = 오늘 예약 단계에 꺼진 자리만(2판). 빈 칸 hover [+] 힌트는 그리지 않음.
- 실패 토스트는 공용 토스트(2초 뒤 사라짐) 그대로 — 「다시 시도」 를 누를 시간이 짧을 수 있음.
- 실물 e2e(A5) · 브라우저 화면 확인은 안 함(로컬 스택 금지) — 코디 몫.
