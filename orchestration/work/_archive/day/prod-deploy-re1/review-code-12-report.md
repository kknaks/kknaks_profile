# 리뷰 리포트 — prod-deploy-re1 / code 12 · 공개 페이지 /privacy · /support (fe-3 · 2026-11-12)

대상: 워크트리 미커밋 fe-3.
- 새 파일: `routers/public_pages.py` · `templates/public_page.html` · `templates/public/{privacy,support}.txt` · `tests/day/web/test_public_pages.py`
- 바뀐 파일: `day/main.py` · `styles/app.css` · `static/day.css`(빌드)

근거:
- fe-3-report.md
- 스펙 미커밋 SPEC-001 개정 ⑦(`spec-001*.md:37` · `:105`)
- 본문 원천 `60-release/app-store-preparation.md` §6-1(:248-294) · §6-2(:320-348)

## 판정: PASS

FAIL 0 · WARN 0 · 참고 4.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| 대조 스크립트(scratchpad `cmp_public.py` · 원천 §6-1 · §6-2 코드 블록을 직접 잘라 비교) | privacy: txt = 원천 **43줄 바이트 단위 같음** · 렌더된 `<main>` 보이는 줄 = 원천 빈 줄 뺀 **33줄 같음**. support: txt = 원천 **25줄 같음** · 렌더 **18줄 같음**. 지어 넣은 글자 0 · 빠진 줄 0 |
| 같은 스크립트 — 링크 · 연락처 | privacy href = `https://soniox.com/policies/privacy-policy` · `mailto:dev@medisolveai.com`. support href = `https://day.medisolveai.com/privacy` · `mailto:dev@medisolveai.com`. 메일 주소는 `dev@medisolveai.com` 하나뿐이고 전화번호 꼴은 0 |
| 격리 스택(`day-rv12` · 127.0.0.1:11152/11153) + `scripts/test.sh` — test_public_pages · test_login_page · tests/architecture | **44 passed** |
| 프록시 흉내(scratchpad `proxy_check.py` · 실제 `create_application()` · `X-Forwarded-Proto: https` · `Host: day.medisolveai.com` · redirect 안 따라감) | `/privacy` 200 · `/support` 200 · `/privacy?utm=1` 200 · Location 없음. 가짜·만료 쿠키(`day_session=expired-or-forged`)로도 `/privacy` · `/support` 200(DB 조회 없음). 비교용 `/board`(쿠키 없음)는 303 `/login` 그대로다 |
| `uv run ruff check backend` · `ruff format --check`(새 · 바뀐 py) | 통과 |
| 스택 `down -v` 뒤 `docker ps` | day-local-* 다섯만 남음 — 11040 · day-local 손대지 않음 |

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 본문 = 원천 글자 단위 | PASS | 위 대조와 같다. `parse`(`public_pages.py:62-71`)는 줄을 나누기만 하고 글자를 바꾸지 않는다. 링크는 글자를 그대로 두고 `<a>` 만 씌운다(`_parts` `:47-59`). Jinja 자동 escape 가 켜져 있고, `"…"` 따옴표는 렌더 뒤 unescape 비교에서 같았다 |
| 연락처 = dev@ 만 | PASS | 본문 메일은 `dev@medisolveai.com` 한 종류뿐이다(두 페이지). 템플릿에는 다른 글자 · 연락처가 없다(`public_page.html` 한글 0). 시험 `test_지원_메일만_있고_다른_연락처는_없다` |
| 비로그인 · 로그인 · 만료 세션 200 | PASS | 라우트에 의존성이 없다(`:83-90` · `Request` 만). `render(..., session=None)`(`:79`)라 로그인한 사람도 같은 페이지다. base 의 `hx-headers` · 로그아웃 form 은 `{% if session %}`(`base.html:21` · `:53`)이라 그려지지 않는다. 만료 · 위조 쿠키도 읽지 않으므로 200(위 프록시 흉내) |
| 세션 · CSRF · 병원 선택 예외가 이 두 경로에만 | PASS | 앱 전체에 미들웨어가 없다(`add_middleware` · `@app.middleware` grep 0 — runtime · common · day). 인증 · CSRF · 병원 선택은 라우트별 의존성이다. 그래서 「예외 목록」을 손댄 곳이 없고, 새 라우터 두 경로만 의존성 없이 붙었다. `main.py` diff 는 `web_routers()` 목록에 `public_router` 추가와 docstring 뿐이다 |
| 다른 경로 인증 약해짐 없음 | PASS | 다른 라우터 · 의존성 · 예외 처리기는 바뀌지 않았다. `/privacy` · `/support` 는 다른 라우터와 겹치지 않는다(grep). `/board` 무쿠키 303 `/login` 이 그대로임을 확인했다. GET 만 있다(POST 는 405) |
| prod 프록시(https) 뒤 리다이렉트 없음 | PASS(+참고 1) | 정확한 경로(`/privacy` · `/support` · 쿼리 붙어도)는 3xx 가 없다. Caddy 는 모든 경로를 api 로 넘긴다(`deploy/caddy/Caddyfile` · 바뀌지 않음). App Store · 앱이 쓰는 주소는 끝 `/` 가 없는 `https://day.medisolveai.com/privacy` 다 |
| medikit 사용 | PASS | 색은 모두 medikit 토큰(`--ms-gray-100/200/700/800` · `--ms-white` · `--ms-black` · `--ms-primary`)이다. 폭 토큰 `--day-legal-w` 는 `:root` 기존 `--day-login-w` 옆에 있다. 로그인 화면과 같은 틀(회색 바탕 · 흰 카드 · 테두리 · 둥근 16)이다. 인라인 `style=` · 스크립트 · CDN 은 0이다. `day.css` 는 빌드 산출물로 source-sha 가 갱신됐고 diff 는 `day-legal` 규칙뿐이다. architecture(클래스-CSS 대조) 통과 |
| 캡처 눈 확인 | PASS | `fe3-privacy-desktop.png`(1280): 제목 h1 · 소제목 1~8 · 「· 」 줄 내어쓰기 · soniox · 메일 링크(파랑 밑줄) · 끝 「시행일」 · 머리 메뉴 · 레일 · 로그인 링크 없음. `fe3-support-mobile.png`(390 @2x): 카드 좌우 여백 · 줄 바꿈이 자연스럽고, 긴 URL 이 줄 넘김으로 잘 들어간다(`overflow-wrap: anywhere`). 가로 스크롤 흔적 없음 |
| 시험 | PASS | 비로그인 200 · 본문 줄 = txt · 원천 핵심 글자 · 메뉴 · 로그인 · 로그아웃 form · hx-headers 없음 · 링크 허용 셋 · 쿠키 · HX 요청에도 같음 · 메일 하나 · 전화 없음. 쿠키 시험의 `"anything"` 이 곧 만료 · 위조 세션 경우다 |

## 참고

- 참고 1(끝 `/`): `/privacy/` 는 Starlette `redirect_slashes` 로 307 `http://day.medisolveai.com/privacy` 다. uvicorn 이 `--proxy-headers`/`--forwarded-allow-ips` 없이 떠서(`deploy/compose.yaml:42-51`) scheme 이 http 로 나간다. Caddy 가 http → https 로 한 번 더 보내면 결국 열리지만, 한 단계 돈다. 앱 전체에 원래 있던 동작이고 이 변경과 무관하다. 등록 URL 에 `/` 가 없으므로 지금은 영향이 없다.
- 참고 2(나누기 규칙의 취약점): 「빈 줄 = 묶음 · 묶음 첫 줄이 `· ` 가 아니고 뒤에 줄이 있으면 소제목」은 지금 원천에 맞는다. 원천이 바뀌어 두 줄짜리 일반 문단이 생기면 첫 줄이 h2 로 그려진다. 글자는 그대로라 대조 시험은 통과하지만 모양이 틀어진다. 문안을 고칠 때(§7-2 #10 시행일 등) 캡처를 한 번 다시 보면 된다.
- 참고 3(원천 ↔ txt 동기화): CI 는 txt 기준이다. 원천(spec 저장소)이 바뀌어도 시험은 모른다. 문안 → txt 순서로 고치는 절차(fe-3 「정할 것」)를 코디가 기록해 두면 된다. 이번 리뷰 시점에는 둘이 바이트 단위로 같다.
- 참고 4(탭 제목): base 규칙대로 「DAY 지원 · DAY」 · 「DAY 개인정보 처리 안내 · DAY」로 DAY 가 두 번 나온다. 본문 글자가 아니라 지어 넣은 글자는 아니다. 눈에 거슬리면 코디가 판단한다.
