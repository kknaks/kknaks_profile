# day-reservation2 마무리(B1 ~ B10 + 2 · 3 · 4판) frontend 결과 보고
## 상태: done (커밋 · push 안 함)

## 수행
- `templates/partials/reservations_detail.html` 다시 씀 — 단계 전부(예약 · 접수 · 상담 대기 · 상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기 · 귀가 · 취소 · 노쇼)
  - B8: 회색 「미확인」 · 「작성 필요」 · 「문진 전」 · 묶음 사이 구분선 · [예약 변경] 줄 오른쪽 끝 · 예약메모 = 라벨 아래 전체 폭 상자 · 의사 지정 = 일반 글자(hover 바탕 · 밑줄 없음) · 오른쪽 시술 목록 표 + 「추가된 시술이 없습니다.」 + 0 원 수납 카드 · 상담 정보 칸(상담사* · 관리실 선택* · 시술만 진행) · [접수] 파랑 활성(POST …/reception) · 「{국적} / 통역필요」
  - 신분증 체크(PUT …/identity · 모달 다시 그림) · 시술만 진행(초진 = RP-05) · 시술 정보(관리실 · 오더 메모 글 칸 / [수정] PUT …/order-memo) · 상담 대기 = 고르면 바로 PUT …/counselor · …/room · 상담 진행부터 잠금(「선택 안 함」)
  - 시술 목록 = 결정 와이어(상품명 · 오늘 · 상태 · n/m회 · 머리 줄 → 들여 쓴 구성 줄 · ✓ / 접수 + 시술만 = 체크) · 귀가 사유 상자 · 수납 정보(경고 / 수납 완료 배지 · 상품 합계 · 할인 · 총 · 수납 완료 · 수납 필요 빨강)
  - 아래 버튼(U-9): [상담 대기] / [시술 대기](빠진 칸 회색 · 누르면 깜빡임 + 「… 먼저 해 주세요」 · hx-include 로 화면 값 한 번에) · [n원 수납] = KOS 딥링크 새 창 · 「KOS에서 수납 중」 꺼짐 · [귀가 처리] · [처방전 출력] 딥링크 새 창(URL 없으면 꺼짐)
- `partials/reservations_dialogs.html` — RP-01(사유 · 비면 [귀가] 꺼짐) · RP-02(미수) · RP-03 · RP-05 · 고객 카드 `data-day-res-visit`(미리보기 초진 판정)
- `routers/reservation_detail.py` — POST reception · PUT identity · POST consultation-waiting · PUT counselor · PUT room · POST procedure-waiting(line_ids 여러 개) · PUT order-memo · POST discharge + 시안 알림 글자
- `static/day.js` — B1 빈 칸 [+](열 안 자식 요소 위에서도) · B6 최근 고객 목록 처음엔 닫힘 · 바깥 누르면 닫힘 · B7 미리보기 = 「새 예약」 + 초진(고른 재진 고객이면 없음) · 2 ~ 4판 동작(시술만 · 빠진 칸 · 오늘 ✓ · 오더 메모 · 귀가 사유)
- `styles/app.css`(+ `day.css` 빌드) — 위 모양 · B7 점선 테두리 · 경고 테두리 토큰
- 테스트: `tests/day/web/test_reservation_detail_stages_screen.py`(새 · 18) · `test_reservation_detail_screen.py`(B8 기준으로 고침) · `test_reservations_screen.py`(ghost · 「새 예약」 금지 풂 = RB-12 · 국적 이름) · `test_screen_copy.py`(근거 43줄)
- 계약: `contract-v1.md` §6 — 읽기 값은 backend 이름으로 맞춤 · 쓰기 이름 = `reservation_writes.<표 이름>`

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture/test_screen_copy.py` = 232 passed
- mypy(routers/reservation_detail.py) 통과 · ruff 통과 · eslint/stylelint/prettier 통과 · `node --test` 125 pass · CSS 빌드 1회 + `--check`
- 템플릿 인라인 `<script>` · `style=` 0
- pending: architecture 테스트 다수는 pytest 단독 실행 시 `scripts` 모듈 수집 오류(실행 방식 문제 · `scripts/check.sh` 로 코디 확인) · 실물 화면 확인(스택 멈춤 지시)

## 코디 기본 · 주의
- B3 · B4 · B5 · B9(국적 이름 · 대시 연락처 · DAY 재진 판정)은 값 = backend 몫 — 화면은 받은 값 그대로
- 시술 목록 머리 = 와이어(상품명 · 오늘 · 상태) — 시안 2칸과 다름(코디 지시 「와이어만 다름」)
- 상태 색: 시술 전 · 시술 중 = 파랑, 시술 후 · 미진행 = 회색(코디 기본)
- 「1년 안 재진」 신분확인 「생략 (1년 이내)」 · 문진 「다시 받기」는 값이 없어 그리지 않음(문진 = 다음 스펙)
- 상담사 · 관리실 목록 검색 칸 없음(목록만) · 「상담 없이 귀가」 배너 없음(원천 없음)
