# day-chart-photo frontend(WP ③) 결과 보고
## 상태: done (커밋 · push 안 함 — 워크트리 변경만)

## 수행 — 템플릿 · 조각 · 정적 파일
- `templates/partials/board_chart_parts.html` 다시 씀 — 탭 셋(간호관리차트 | 의사차트 | 시술전후사진) · 탭 줄 `.day-chart__bar` 오른쪽 끝 「최근 저장 : HH:MM」(탭마다 · `tasks[].{kind}.savedAt` 최댓값) + [저장](`data-day-chart-save` · 차트 탭만 · 처음 꺼짐 · edit 아니면 없음) · 차트 탭 = form 하나(`hx-post /board/visits/{id}/chart` · trigger `day:chart-save` · `hx-params=chart,taskId,body,staffId,baseLogId,baseBody,baseDoctorStaffId` · target this · outerHTML) · 줄 = div(숨은 칸 taskId · staffId · baseLogId · baseBody · baseDoctorStaffId(의사만) + textarea body) · 담당자 라디오 이름 = 줄마다 `staffPick-{task}-{kind}`(보내지 않음) · E59 확인 창(「저장하지 않고 닫을까요?」 · 「계속 쓰기」 · 「버리고 닫기」 — 기획 4-2) · 사진 탭 자리 `hx-get …/photos` trigger `day:photos-load`
- `partials/board_chart.html` — modal 호출만(stored_staff 뺌)
- `partials/board_chart_tab.html` 새로 — K3(계약 보충 1): form + 그 탭 「최근 저장」 OOB + message 있을 때만 토스트 + action 이면 board_action
- `partials/board_photos.html` 새로 — K4: 묶음(title = 서버 값) · 썸네일(data:) → `…/original` 새 창 · ✕ 삭제(POST …/delete) · 묶음마다 올리기(multipart · change 로 바로) · 둘 다 `#chart-photos-{visit}` innerHTML · 보기 권한이면 올리기 · 삭제 없음 · 글자 짓지 않음
- `partials/board_chart_saved.html` 지움(K5)
- `templates/base.html` — 로그아웃 바로 왼쪽 `header_staff` 「이름 직군」(직군 없으면 이름만) · `icons.html` — lucide `plus` 하나 더함
- `static/day.js` — 자동 저장 전부 걷어냄(칸 나감 · 2초 · 줄 저장 · reconcile · 다시 시도 · 저장하지 않고 닫기 · close 가로채기) → 탭 저장(바뀐 줄만 · 안 바뀐 줄 칸은 htmx 가 값 모으는 그 순간만 disabled) · [저장] 켜짐 동기화 · 409 chart_conflict 면 보냈던 줄을 「바뀐 줄」로 유지 · ✕ / 바깥 / Escape / cancel 가로채기(capture) → 확인 창 · 사진 탭 고를 때 조각 읽기(내용 없을 때만 → 실패하면 다음 선택 때 다시)
- `styles/app.css` — `.day-chart__bar` · `.day-chart__tools` · `.day-header__who` · `.day-photos*`(토큰만) → `static/day.css` 빌드

## 검증
- `uv run pytest -q backend/tests/day/web/test_board_page_chart_controller.py test_board_page_charts.py test_board_page_chart_photos.py` → 9 passed
- 참고: `backend/tests/day/web` 전체 + `architecture/test_screen_copy.py` → 190 passed
- `npm --prefix scripts/frontend run check`(CSS 재현 · ESLint · Stylelint · Prettier · node 117) → 통과
- 인라인 `<script>` · `style=` grep(차트 · 사진 · base 템플릿) → 0
- architecture 전체: 4 failed — 모두 backend 진행 중 변경(`dtos/board_views.py` stale schema projection · ChartCellResponse · ChartTaskView projection) — **무관(backend 몫)**
- 실행 못 함(pending): Bombadil 차트 평가 · 실물 e2e(A8 — ①②③ 합친 로컬 · KOS 데모) · 브라우저 실제 클릭(확인 창 · Escape)

## scripts/frontend — 지운 것 · 바꾼 것(코디 보충 2)
- 지움: `tests/chart-recovery.test.mjs`(자동 저장 응답 유실 · reconcile · 재시도 14건 — 자동 저장 전용)
- 바꿈: `tests/controllers.test.mjs` 「200 입력 → 한 번 저장」 → 「입력은 저장 · 타이머 0 · [저장] 동기화만」
- 새로: `tests/chart-save.test.mjs`(바뀐 줄만 dirty · [저장] 한 요청 + 안 바뀐 줄 disabled 는 그 순간만 · 보내는 중 두 번째 없음 · 바뀐 것 없으면 요청 0 · 409 뒤 보낸 줄 dirty 유지)
- 바꿈: `bombadil/chart.mjs` — 요청 경로 `/board/visits/{visit}/chart` · ack = 응답 form 의 그 줄 baseLogId · trigger 단계 = (blur 모드면 머리 누름) → [저장] 누름 · 저장 뒤 닫기(escape 모드 = Esc). MODES(`verification_properties.py`)는 그대로 — **실행 안 함**
- 그대로: `tests/chart-trace.test.mjs` · `bombadil/chart-trace.mjs`(수동 관찰 · `/chart` 요청 세기 — 의미 유지)

## 그 밖 수정(allowed 밖 — 화면 문구 가드)
- `backend/tests/architecture/test_screen_copy.py` — 「시술전후사진」 · E59 세 글자 근거 추가 · 자동 저장 복구 글자 5개 지움(「다시 시도」는 예약 현황이 써서 남김 · 근거 고침)
- `.agents/skills/verify-day-web/features/clinical-chart.md` 갱신(명시적 저장 · 확인 창 · 충돌 · 네트워크 · 사진 탭)

## 계약 대조
- K1 같음(`base` · `logId` · 「최근 저장」 템플릿 계산) · K2 같음(칸 이름 · 순서 = 줄마다 taskId · staffId · baseLogId · baseBody · baseDoctorStaffId · body) · K3 같음(계약 보충 1 값 이름 — backend router 가 같은 이름으로 넘김 확인) · K4 같음(`group["items"]` 로 읽음 — dict · 객체 둘 다 됨) · K5 템플릿 · day.js 쪽 지움
- U-14: 저장 뒤 창 안 닫힘(OQ-80 기본값) · 탭 옮겨도 쓴 것 남음(OQ-82) · Escape = ✕(OQ-79 기본값) · 바깥 = 아무 일 없음

## 이슈 · 코디가 확인할 것
- 사진 삭제 ✕ · 올리기 칸에 aria-label 이 없다(글자 근거 없음 · OQ-88) — 사용자 확인
- 원본 열기 = 새 창(크게 보기 모양 OQ-87 전 임시)
- 자동 저장 때의 「응답 유실 확인」 로직을 지웠다 — 시간 초과 뒤 서버가 이미 저장했으면 다시 [저장]이 409 충돌(내 글 + 내 글 이어 붙임)로 걸릴 수 있다. 명시적 저장에서 어떻게 할지 정해야 함(SPEC 「실패 안내는 WORK 에서」)
- `.agents/skills/verify-day-web/SKILL.md:130` 「입력·자동 저장·닫기」 문장 남음(지정 파일 밖)
- `scripts/devtools/verification_*`(줄 저장 경로) 는 backend 몫 — 아직 옛 경로를 볼 수 있음
- 헤더 표시는 backend `web.render` 의 `header_staff`(request.state) 에 기댄다
