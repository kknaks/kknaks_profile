# BE 수정 판 4·5 결과 보고

## 상태: done (커밋 안 함 · 코디 스택·DB 는 읽기만 · frontend/ 무접촉)

## 판 4 결함 1 — Gmail 백필 100통 뒤 「끊김 PERMISSION_DENIED」
- 재현(코디 DB 읽기만 + jiho refresh token 으로 같은 호출): 지금은 profile·목록 2쪽·메시지 100통·history·watch **전부 200** — 토큰은 멀쩡하다. 그 403 은 그때만 난 거절이었다
- 원인: `platform/external_gmail.py` 가 **403 이면 무조건 토큰 폐기**로 분류 · Gmail 은 속도 제한(`userRateLimitExceeded`·`rateLimitExceeded`)도 **403 + status `PERMISSION_DENIED`** 로 내는데 `reason` 을 안 보고 `status` 만 봤다. 백필이 메시지 100통을 연달아 받은 직후라 속도 제한일 가능성이 가장 높다(당시 본문을 안 남겨 확정 불가 — 이제 남긴다)
- 고친 것: ① 거절 응답의 http·status·reasons·message 를 한 줄 로그(토큰·메일 내용 없음) ② 토큰 폐기 = 401·`invalid_grant`(갱신 실패)만 ③ 사유가 속도·할당량이면 `UpstreamRateLimited`(Retry-After, 기본 60초) ④ 그 밖 403 = `UpstreamCallDenied` — 그 호출만 실패: get_message 면 **그 메일만 건너뛰고 로그**, 다른 호출이면 연동 유지 + 물러서기(30초→최대 30분 배수)

## 판 4 결함 2 — 슬랙 멀쩡한 토큰이 3분 뒤 「revoked」
- 원인(코디 로그 145행): 메시지함 방 첨부 받기 → `files.slack.com` 403 → BE-3 중계(`external_inbox_upstream._call`)가 **403 을 토큰 거절로** 보고 `inbox._with_token` 이 연동을 `revoked` 로 끊었다 — **경고 로그 없이**. 파일 주소 403 의 원인은 토큰에 **`files:read` 권한이 없어서**(실측 권한 12개에 없음). 같은 계열로 `missing_scope` 도 토큰 거절로 보고 있었다
- 고친 것: 중계 403 = 그 자원만 실패(502 `forbidden`, 연동 유지) · `missing_scope` 도 그 호출만 실패 · 토큰 거절은 401·`invalid_auth`·`token_revoked`… 만 · 연동을 끊는 **모든 자리에 경고 로그**(메시지함 중계·수집 저장소) · OAuth 슬랙 user scope 에 `files:read` 추가
- `tokens_revoked`·`app_uninstalled` 이벤트는 그동안 **무시**됐다(끊지도 않음). 이제 처리하되 **그 이벤트의 사용자 id 가 그 연동의 사용자일 때만**(`account_meta.user_id`) 끊고, 앱 삭제는 그 워크스페이스 전체 · 경고 로그
- ⚠ 운영·사람 할 일: 슬랙 앱 설정에 User Token Scope **`files:read`** 추가 후 재연결(개발 토큰도 새로 받아야 첨부 받기가 된다). 지금 토큰으로는 첨부 받기가 502 `forbidden` 으로 실패하지만 연동은 끊기지 않는다

## 판 5 — 메일 이미지·레이아웃·읽음 500
1. 프록시 실패율(로그 65건: 502 44 · 400 6 · 200 15)
   - 502 의 원인 = **TLS 검증 실패**: 로컬 파이썬이 쓰는 시스템 CA 묶음(`/etc/ssl/cert.pem`)에 Sectigo R46 루트가 없어 `images.mkt-email.samsungsds.com` 이 `CERTIFICATE_VERIFY_FAILED`(같은 주소가 certifi 묶음으로는 검증됨) → 이미지 TLS 문맥 = **certifi + 시스템 루트**(검증을 끄지 않음) · `certifi` 직접 의존 한 줄
   - 리다이렉트: 301/302/303/307/308 을 **홉마다 http(s)·포트·DNS→공인 주소 검사를 다시 하며** 3번까지 따른다(Eloqua 푸터 추적 이미지가 302)
   - 형식: Content-Type 이 아니라 **바이트 머리**로 판별(PNG·JPEG·GIF·WEBP·BMP·ICO) — 없는 type·octet-stream·`image/jpg` 도 받음. SVG·HTML 은 거절 유지
   - 실패 사유를 한 줄 로그(host·사유)
   - 400 6건 = GitHub camo 를 거친 **SVG 배지**(vercel 상태 아이콘) — 설계상 SVG 는 받지 않으므로 의도된 거절
2. 소독기
   - `style` 속성에 `url(` 이 하나라도 있으면 **속성 전체를 지우던** 것 → `url()` 만 프록시 주소로 바꾸고 나머지 선언(폭·정렬·색)은 남긴다 · 위험 선언(@import·expression·javascript:·behavior)은 그 선언만 걷음
   - `background` 속성(table/tr/td/th)을 허용하고 원격이면 프록시 주소로
   - `<style>` 블록을 **소독해 남긴다**(뉴스레터의 글꼴·링크 색·모바일 @media) — `<` 제거로 태그 탈출 불가, url()→프록시, @import 등 걷음 · CSP(`img-src 'self' data:`)는 그대로
   - `<body>` 배경색·글꼴은 감싸개 div 로
   - 프록시 허용 목록(`remote_image_urls`)이 img 와 함께 **CSS·background 의 프록시 주소**도 센다
   - 안전본 판 2 — 머리 `SAFE_HTML_PREFIX` 로 판을 박아 **옛 캐시(판 1)는 열 때 다시 만든다**
   - `<img>` 는 종전대로 `data-ax-remote-src`(FE 판 2 가 프록시로 그림)
3. 읽음 500 = 같은 메일 읽음 요청이 겹쳐 `uq_external_read_states_member_message` 위반 → 낱장 읽음·방 읽음·모두 읽음 모두 savepoint 로 받아 「이미 읽음」

## 실물 숫자 (「(광고) 삼성SDS 인사이트」 · 코디 DB 읽기만 · 내 프로세스)
- 원문: `<img src=http…>` 24개(고유 22) · background 속성 0 · CSS url(http) 0 · `<style>` 1
- 소독 후: 원격 이미지 22개 생존 · style 속성 138→133(지워진 요소 몫) · width 속성 60→57 · `<style>`(+@media) 보존 · body 배경 #F2F6F9 보존 · script/on* 0
- 프록시: **22/22 → 200**(jpeg 15·png 6·gif 1, 리다이렉트 1 포함) — 고치기 전 같은 22개는 1개 302 + 21개 TLS 실패

## 검증
- make test-unit 473 passed · make test-contract 1241 + serial 128 passed (exit 0)
- 새·고친 시험: Gmail 사유별 분류(403 일반/속도제한/401/invalid_grant) · 메일 하나만 거절돼도 연동 유지 · tokens_revoked 는 그 사용자만 · 중계 403·missing_scope 가 연동을 안 끊음 + 끊을 땐 경고 로그 · CSS/background 프록시화·<style> 탈출 불가 · 리다이렉트 홉마다 SSRF · 판 1 캐시 재생성 + 배경 이미지 프록시 200 · 읽음 겹침
- BE-3 기존 시험 한 줄 갱신: 「안전본에 `<style` 없음」 → 「소독한 `<style>` 은 남고 @import 없음」(판 5 결정)

## 주의
- 슬랙 `files:read` 추가·재연결은 사람 몫(위)
- 코디 DB 의 jiho Gmail 연동은 `disconnected` 그대로다(나는 쓰지 않았다) — 새 코드로 다시 붙이려면 설정에서 「다시 연결」(또는 코디가 상태를 되돌림)
- 프록시 SVG 거절은 유지 — 배지류는 계속 안 보인다
