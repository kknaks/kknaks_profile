# qa-1 리포트 — 웹 화면 검수 · 예약 현황판 F1 ~ F6 · 6개월 경과 (Playwright)

- 대상: 로컬 스택 `http://127.0.0.1:11340`(워크트리 `day-reservations-fix` 미커밋 코드 · KOS DEMO 지점) · 2026-11-28 15:18 ~ 15:40 KST
- 도구: Playwright 1.49.1(Python) · headless Chromium · 1600×1100 · 로그인 1회(테스트 계정) · 쿠키 공유
- 방문: `def4cbab`(고객 `b26e24e0` · 리프팅 19:00 ~ 20:00 · 재진 · 문진 없음) · `7511bbb0`(고객 `1b9a7c0c` · 리프팅 19:30 ~ 20:30 · 오늘 문진 제출 있음). 처음 받은 17:00 · 17:30 방문(`d2798075` · `6bf64ef7`)은 이미 취소 상태여서 backend 가 다시 만든 위 두 건을 썼다.
- KOS 쓰기 동작(저장 · 옮기기 · 취소 · [다시 보내기] · 문진 제출)은 누르지 않았다. 「링크 복사하기」 · 「링크 열기」만 눌렀다(DAY 안 `display_request`).
- 스크린샷: `qa-1/`

## 결과 표

| # | 시나리오 | 판정 | 스크린샷 | 비고 |
|---|---|---|---|---|
| 1 | F2 배치 | **PASS** | `0-board-full.png` · `1-f2-layout.png` | 서버 rows = 10:00 ~ 24:00 1시간 행 14개 · 행 높이 140px · 60분 카드 136px(= 1행 − 위아래 2px 여백) · 30분 카드 66px(반) · 19:00 / 19:30 겹침 → 19:30 카드가 옆 자리(lane 1, x +144) · 20:00 행 넘는 19:30 카드 = 두 조각(R45 · `.day-res-part` 1개) · 시간 글자 = 1시간 행마다 하나 · 바탕 선 = 정시 행 경계에만(30분 선 없음) |
| 2 | F1 [+] | **PASS** (비고 1건) | `2-f1-hover-plus-tooltip.png` · `2-f1-lifting-1900-right.png` · `2-f1-lifting-1930-right.png` · `2-f1-gita-1900-right.png` · `2-f1-over-card.png` · `2-f1-register-window.png` | 오른쪽 여백 = 66px(카드 반 폭 근처) · 호버 → 점선(`border-style: dashed`) [+] 칸 · 툴팁 「리프팅 \| 19:30 ~ 20:30」 · 「기타 \| 19:00 ~ 19:30」(끝 = 그룹 간격) · 카드 위 호버 = [+] 없음 · 누르면 「예약 등록」 창(예약그룹 = 리프팅 · 예약일 = 오늘). 저장 안 누르고 Esc 로 닫음. **비고 W-a**: 60분 그룹에서 :30 칸(19:30)을 누르면 「예약 시간」이 비어 있음(「시간 선택」) — 선택지가 정각뿐이라 `start=19:30` 이 맞는 값이 없다. 19:00 칸은 19:00 이 골라져 열림 |
| 3 | F3 [문진 QR] | **PASS** | `3-detail-def4cbab.png` · `3-f3-popover.png` | 버튼 모양 = [예약 변경] · [예약 취소]와 같은 클래스(`day-res-dt__ss2` · 글자 #6E6E6E · 바탕 #F3F3F3 · opacity 1 · disabled 아님) → 비활성처럼 보이지 않음. 누르면 팝오버 **하나**: 위 「링크 복사하기」 · 「링크 열기」 / 선 / 아래 기기 칸. `aria-haspopup` 하위 메뉴 0 · 두 단계 없음. 문진 제출된 `7511bbb0` 은 [문진 QR] 이 안 보임(유효한 문진 있음 · `3-detail-7511bbb0.png`) |
| 4 | F5 기기 줄 | **부분 PASS** · 기기 줄 **데이터 없음** | `4-f5-device-rows-empty.png` · `3-detail-def4cbab.png` | 모달 안 별도 기기 카드(「데스크 · 접속 중」) **없음** ✓. DEMO 지점 등록 태블릿 `device` 0행이라 팝오버 기기 칸 = 빈 목록 글자 「띄울 수 있는 기기가 없어요 — 코디 계정으로 로그인한 기기가 보여요」만. `기기명 [점] 상태` · 초록/빨강 · 미연결 누름은 화면으로 확인 못 함(템플릿 `reservations_display_targets.html:13` 만 읽음 — 판정 근거 아님). [여권 스캔] = 두 방문 모두 대한민국 → 버튼 없음(데이터 없음) |
| 5 | F6 태블릿 보내기 | 웹 쪽 **PASS** · 기기 쪽 **로컬 미검증** | `6-link-copy-progress.png` · `5-f6-progress-after-12s.png` · `5-f6-web-progress-after-sse.png` | 태블릿 = Flutter 앱(DAY 웹에 기기 표시 화면 없음) · 등록 기기 0대 → 「로컬 미검증 · 태블릿 실물 필요」. 웹 쪽: 「링크 복사하기」 POST → SSE `display` → `GET /reservations/visits/def4cbab…` 다시 받기 뒤에도 진행 칸(대기 · 남은 시간 09:58 → 09:46)이 **사라지지 않음**(원래 F6 증상 = 수십 ms 만에 사라짐 → 고쳐짐). 기기 줄 누름은 기기 0대라 못 함 |
| 6 | 링크 | **FAIL** | `6-link-open-blank-tab.png` · `6-progress-pending.png` · `6-link-questionnaire-page.png` | 서버: 두 번 눌러도 같은 요청 · 같은 링크(DB `display_request` 해당 방문 pending 1행 · 응답 `data-day-res-dp-link` 같음 — D44 ✓) · 그 링크로 `/q` 문진 첫 화면(언어 칩 · 「박하늘(시험) 님」 · [시작]) 열림 ✓(제출 안 함). **그러나 화면 동작 실패**: 「링크 복사하기」 = 클립보드에 **안 들어감**(권한 허용 · 직접 `writeText` 는 됨) · 「링크 열기」 = 새 탭이 **about:blank 로 남음**. 원인 아래 FAIL-1 |
| 7 | D45 | **미검증**(다시 그리기를 일으킬 수 없음) | `7-d45-popover-after-redraw.png` | 페이지 A 에서 팝오버를 연 채 ① 페이지 B 가 같은 방문 「링크 복사하기」(15:23 · 15:33 두 번) ② 12초 대기(10초 동기화) → A 팝오버 **열린 채** 유지(`aria-expanded=true` · 메뉴 줄 보임). 그러나 A 의 모달 다시 받기(`GET /reservations/visits/…`) 가 **0회** — B 의 요청이 기존 열린 링크 요청을 다시 써서(D44 · 상태 그대로 `opened`) SSE `display` 가 안 났고, 동기화도 모달을 다시 받지 않음. 다시 그리기가 실제로 일어난 상태의 판정이 아니므로 PASS 를 주지 않는다. 진짜 다시 그리기를 일으킬 DAY 안 동작(동행 저장 · 신분증 확인 · 기기 줄 · 요청 [취소])은 허락 범위 밖이거나 기기 0대라 못 함. 참고: 팝오버를 연 페이지 **자기** 모달이 다시 그려질 때는 CSP 오류(WARN-1)가 나지만 팝오버 상태는 이 시험에서 보지 못함 |
| 8 | 6개월 경과 | **데이터 없음** | — | DB SELECT: `questionnaire_history` 살아 있는 행 1개(고객 `1b9a7c0c` · 오늘 06:14Z `web_submit`) · 6개월 넘은 행 0 → 「6개월 경과」 줄을 볼 고객 없음. 설정 기본값 `day_questionnaire_valid_months = 6`(`backend/common/config.py:221`). 문진 없는 `def4cbab` = 「초진 문진 작성 필요」 · 제출된 `7511bbb0` = 「제출됨 · 15:14 실패 [다시 보내기]」(누르지 않음) |
| 9 | 콘솔 · 네트워크 | **FAIL(경미)** | — | 네트워크 4xx/5xx 0. 콘솔 오류: 팝오버가 열린 채 모달이 다시 그려질 때마다 CSP `style-src-attr` 위반 1건씩(아래 WARN-1) · 다른 페이지에서 `pageerror "undefined"` 1회(재현 안 됨) |

## FAIL-1 「링크 복사하기」 · 「링크 열기」가 끝나지 않음

재현:
1. `/reservations` → `def4cbab` 카드 → 상세 → [문진 QR] → 「링크 복사하기」.
2. 응답(`POST /reservations/visits/{id}/display-requests` 200 · 모달에 `data-day-res-dp-link` 있음)이 와도 클립보드 값이 바뀌지 않음(Chromium `clipboard-read/write` 허용 · 같은 페이지에서 `navigator.clipboard.writeText('probe')` 는 정상).
3. 「링크 열기」 = 누를 때 `window.open("", "_blank")` 로 빈 탭이 열리고 링크로 바뀌지 않음(4초 뒤에도 `about:blank`).

원인(브라우저에서 확인):
- `backend/day/static/day.js:6120-6122` `dpLinkAfterRequest` 가 `e.detail.elt` 가 `[data-day-res-dp-link-act]` 폼인지로 고른다. 그런데 응답이 `#modal-root` 를 통째로 바꿔(`target="#modal-root"` · `reservations_display.html:21`) 폼이 문서에서 떨어진 뒤 `htmx:afterRequest` 가 온다. 실측: 폼에 직접 단 리스너 `beforeRequest connected=true` → `afterRequest connected=false` · document 리스너가 받은 `e.detail.elt` = `DIV#modal-root` · `e.detail.requestConfig.elt` = `FORM[data-day-res-dp-link-act=copy]`. 그래서 함수가 첫 줄에서 return → 클립보드 Promise 는 안 풀리고 빈 탭은 그대로.
- 고칠 자리 후보: `requestConfig.elt` 로 폼을 찾거나 swap 전 이벤트(`htmx:beforeSwap` 등)에서 링크를 읽는다(코드 수정은 qa 범위 밖).

## WARN

- **WARN-1 CSP 콘솔 오류**: 팝오버를 연 채 모달이 다시 그려지면 `Refused to apply inline style … style-src-attr` — 출처 `static/htmx.min.js:1:10350` · 대상 `<div id="res-dp-pop-questionnaire" … style="left: 519px; top: 265.5px;">`. htmx 가 같은 id 요소의 속성을 새 조각에 옮기며(settle) day.js 가 넣어 둔 위치 `style` 을 속성으로 쓰는 것으로 보임. 기능은 안 깨짐(위치값만).
- **WARN-2 진행 칸 글자**: 웹 QR 을 없앴는데(고침 8) 링크 요청 진행 칸 글자가 「고객 휴대폰 카메라로 찍어 주세요 · 남은 시간 mm:ss」 + [QR 닫기] 그대로(`reservations_display.html:66` · `:71`). 화면에 QR 이 없어 문구가 맞지 않음 — SPEC 글자 확인 필요.
- **W-a (F1)**: 위 표 2 비고 — 60분 그룹 :30 [+] 의 툴팁 「19:30 ~ 20:30」 · 등록 창 시간 빈 값. [+] 칸 단위가 그룹 간격과 무관하게 30분(`day.js:2457` `RES_SLOT_MIN = 30`). KOS 동작과 같은지 확인 필요.

## 사용자 피드백 F1 ~ F6 — 고쳐졌나

- **F1** 카드 오른쪽 여백 · 점선 [+] · 툴팁 · 누르면 그 그룹 · 시각 등록 창 → **고쳐짐**(60분 그룹 :30 칸 시간 빈 값 — W-a).
- **F2** 60분 = 1시간 행 하나 · 겹치면 옆 자리 · 30분 = 반 → **고쳐짐**.
- **F3** [문진 QR] 비활성처럼 안 보임 · 팝오버 하나(링크 복사하기 · 링크 열기 / 기기) → **모양은 고쳐짐 · 링크 두 동작은 화면에서 실패(FAIL-1)** · 팝오버가 다시 그리기에도 남는지(D45) 미검증.
- **F4** 6개월 경과 → **데이터 없음**(6개월 넘은 문진 행 0 · 화면 확인 못 함).
- **F5** 모달 안 별도 기기 카드 → **없어짐(고쳐짐)** · 기기 줄 `기기명 [점] 상태` 는 기기 0대라 **화면 미확인**.
- **F6** QR · 진행 칸이 다시 그리기 뒤 사라짐 → **웹 쪽 고쳐짐**(SSE 다시 받기 뒤에도 남음) · 태블릿에 문진이 뜨는지는 **로컬 미검증(태블릿 실물 필요)**.

## 남긴 상태

- DAY `display_request`: `def4cbab` 문진 링크 요청 1행(`16d672f3` · 기기 없음 · 링크를 `/q` 로 연 뒤 `opened` · 만료 시각 15:32:40 지났지만 `opened` 로 남음 — 다시 누르면 계속 재사용됨). KOS 쓰기 없음 · 문진 제출 없음.
- 참고(관찰): `opened` 링크 요청은 만료 시각이 지나도 `_open_link`(`services/displays.py:339`)가 계속 다시 써서 「남은 시간」 없는 같은 링크가 나온다 — 의도(고객 입력 중 유지)인지 SPEC 확인 권장.
- 로그인: 첫 로그인 스크립트가 대기 시간 초과로 한 번 더 돌아 DAY 세션 2개(`fdc6058a` · `e29c99ad`) · KOS 활성 로그인 2개가 생김. 끝에 KOS `revoke-active-sign-in` 으로 **둘 다 해제**(해제 뒤 목록 0) · DAY `e29c99ad` = 로그아웃 · `fdc6058a` = DAY 쪽 `revoked_at` 비어 있음(쿠키를 덮어써 로그아웃 못 함 · KOS 토큰은 해제돼 다음 사용 때 401 로 끝남).
