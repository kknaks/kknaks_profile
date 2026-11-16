# fe-3 — 공개 페이지 `/privacy` · `/support` (P1 · 2026-11-12)

worktree `CENTURION_DAY/prod-deploy-re1` · **커밋 안 함**.

## 결과

- `GET /privacy` · `GET /support` — 로그인 없이 200(iPhone Safari UA 포함). 세션 · CSRF 의존성 없음.
  쿠키가 있어도(로그인한 사람) · HX 요청이어도 같은 페이지.
- 본문 = `60-release/app-store-preparation.md` §6-1 · §6-2 코드 블록 **원문 그대로**.
  - 원문은 스크립트로 코드 블록을 그대로 잘라 `backend/day/templates/public/{privacy,support}.txt` 에 넣었다(손으로 옮겨 적지 않음).
  - 화면은 그 줄을 나눠 그리기만 한다. 빈 줄 = 묶음, 묶음 첫 줄이 「· 」가 아니고 뒤에 줄이 있으면 소제목(h2), 첫 묶음 = 제목(h1). 글자 · 순서 변경 없음.
  - 검증: 렌더된 `<main>` 의 보이는 글자를 줄 단위로 60-release 원문과 비교. **privacy 33줄 · support 18줄 모두 같음**.
  - 링크만 건다(글자는 그대로): `https://…` 주소 둘(soniox 정책 · day.medisolveai.com/privacy), `dev@medisolveai.com` → `mailto:`.
- 모양: 로그인 화면과 같은 바깥 틀(gray-100 바탕 · 흰 카드 · 테두리 · 둥근 16). 글이 길어 위에서 시작하고 폭은 720px. 모바일(≤480px)에서는 바깥 여백 16px.
  - 머리 메뉴 · 레일 · 로그인 링크 · 로그아웃 버튼 없음. 다른 연락처 · 전화 · 이름 없음. 지원 메일은 dev@medisolveai.com 하나.
- 탭 제목은 base 의 기존 규칙 그대로 「<제목> · DAY」다(예: 「DAY 지원 · DAY」). base 를 바꾸지 않으려고 그대로 뒀다.

## 바꾼 파일

| 파일 | 내용 |
|---|---|
| `backend/day/routers/public_pages.py` (새) | `/privacy` · `/support` 라우터 · 원문 줄 나누기 · 링크 |
| `backend/day/templates/public_page.html` (새) | base 를 쓰고 body 를 공개 안내 카드로 바꿈 |
| `backend/day/templates/public/privacy.txt` · `support.txt` (새) | §6-1 · §6-2 원문 |
| `backend/day/main.py` | `web_routers()` 에 공개 라우터 추가 |
| `backend/day/styles/app.css` · `static/day.css` | `.day-legal*` · `--day-legal-w` · build-css 다시 빌드 |
| `backend/tests/day/web/test_public_pages.py` (새) | 아래 시험 |

서버 설정 · 데이터 · 다른 화면 · Caddy 는 바꾸지 않았다. Caddy 는 이미 모든 경로를 api 로 넘긴다. 미들웨어로 거는 세션은 없고, 세션은 라우트별 의존성이다.

## 시험

- 새 시험(`test_public_pages.py`):
  - 비로그인 GET 200, 본문 줄이 원문 txt 와 같고 원문에 60-release 핵심 글자가 들어 있음.
  - 머리 메뉴 · 로그인 링크 · 로그아웃 form · hx-headers 없음. 본문 링크는 허용한 세 개뿐.
  - 세션 쿠키가 있거나 HX 요청이어도 같은 페이지.
  - 메일은 지원 메일 하나뿐이고 전화번호 없음.
- 원문이 저장소 밖(spec 저장소)이라 CI 시험은 txt 기준이다. txt = 60-release 원문 대조는 위 검증 스크립트로 한 번 했다.
- 공개 경로 아키텍처 시험은 없다(찾아봄). `test_screen_copy` 는 `*.html` · day.js 의 글자만 보는데, 공개 본문은 `.txt` 라 근거 표에 넣지 않았다(근거 = 60-release §6). 템플릿에는 한글이 없다.
- 격리 스택(`day-fe-iso` · 11142/11143 · 새 비밀번호)에서 `scripts/test.sh` 로 `test_public_pages` · `test_login_page` · `test_web_rules` · `test_screen_copy` 를 돌렸다.
  - 1차: 2 failed. 시험 쪽 오류였다 — 「로그아웃」이 원문 본문에 있다. 로그아웃 form 검사로 고쳤다.
  - 2차: **28 passed**. 끝나고 `down -v` · env 파일 삭제. day-local · 11040 은 건드리지 않았다.
- ruff check · format 통과.

## 캡처

같은 앱을 127.0.0.1:11150 에 잠깐 띄워 찍고 내렸다.

- `fe-captures/fe3-privacy-desktop.png` — 1280 폭 · 전체 높이
- `fe-captures/fe3-support-mobile.png` — 390 폭 · iPhone 에뮬레이션 · @2x

## 정할 것 · 참고

- 60-release §6 머리 주석: 「시행일 2026-11-12(예정)」은 공개일에 맞춰 고칠 값이다. 바뀌면 txt 한 줄만 고치면 된다(§7-2 #10).
- §7-1 T1 · T3 · T4 · T5 확인 결과가 본문과 다르면 문안 → txt 순서로 고친다.
