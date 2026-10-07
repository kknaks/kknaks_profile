# [backend] BE 수정 판 5 — 메일 이미지가 안 나옴 + 읽음 처리 예외 (사용자 화면 확인, 2026-10-06)

판 4 와 같은 판으로 이어서. 로그 = 판 4 와 같은 local-stack.log. 사용자 결정: 메일 원격 이미지는 **자동 표시(우리 프록시 경유)** — FE 가 판 2 로 바꾸는 중.

사용자 비교: 원본 메일(삼성SDS 뉴스레터 「The Insight」)은 상단 배너 이미지·「뉴스레터 구독하기」 이미지 버튼이 보이는데 우리 화면에선 **배너가 통째로 없고 버튼은 글자만**, 폭도 좁게 그려진다.

## 고칠 것
1. **이미지 프록시 실패율**: 로그 기준 `/api/inbox/mail/{id}/remote-image` 65건 중 **502 44건 · 400 6건 · 200 15건**. 원인별로 재현·수정 — 리다이렉트(추적·CDN·camo 는 대개 302 → **홉마다 SSRF 재검사하며 몇 번 따라가기**) · http 스킴 · 래스터 판별/Content-Type 이 엄격한지(webp·gif·없는 type) · 크기 한도 · SNI/핀 연결 · 타임아웃. 실패 사유를 로그에 한 줄
2. **소독기가 배경 이미지를 지움**: HTML 메일은 `<td background=…>`·`style="background-image:url(…)"`·`<table background>` 로 배너를 많이 그린다 — **지우지 말고 프록시 URL 로 바꿔** 남겨라(CSS `url()` 도). 폭·정렬 속성(table width·align·bgcolor·cellpadding 등 레이아웃 속성)도 과하게 지우지 않는지 확인 — 원본과 레이아웃이 다르게 좁아지는 원인
3. **읽음 처리 예외**: `POST /api/inbox/mail/{id}/read` 가 500(로그 traceback: `inbox.py:594 mark_mail_read` → `external_channels_inbox_store.py:261 mark_message_read`) — 원인 수정 + 시험
검증: 삼성SDS 뉴스레터 같은 실제 HTML 메일 1통(로컬 DB `ax_demo_inbox` 의 jiho 메일 중 제목 「(광고) 삼성SDS 인사이트」 — **읽기만**, 코디 스택 끄지 말 것)을 네 프로세스에서 소독·프록시 경로로 돌려 이미지 URL 이 몇 개 살아남고 프록시가 몇 개 200 인지 숫자로.
