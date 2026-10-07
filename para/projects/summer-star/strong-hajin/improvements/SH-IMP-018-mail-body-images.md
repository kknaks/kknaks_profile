# SH-IMP-018 — 메일 본문 이미지가 깨진다

상태: 완료  
생성일: 2026-10-07  
갱신일: 2026-10-07  
출처: 운영 화면(사용자), 2026-10-07

## 문제

메시지함 메일 본문의 이미지가 깨진 아이콘(`?`)·빈 칸으로 나온다.

## 화면 근거

- 메일: vercel[bot] 「Re: [kknaks/kknaks_profile] concept: strong-hajin-inbox 회고를 개념으로 소화한다 …(PR #82)」 (2026-10-07 09:30)
- 표의 Project 칸 아이콘 · Deployment 칸 상태 이미지(「?」 깨짐 아이콘)가 안 보인다. 링크·텍스트는 정상
- 외부 URL 이미지(GitHub·Vercel 이 메일 HTML 에 `<img src="https://…">` 로 거는 것)로 추정 **(확인 필요)**

## 세 화면 비교 (사용자 2026-10-07 · 같은 종류 vercel[bot] 메일)

| 화면 | 상단 vercel 삼각형 아이콘 | Project 칸 아이콘(「N」) | Deployment 칸 상태 점(주황) |
|---|---|---|---|
| Gmail 원본 | 보임 | 보임 | 보임 + 「Building」 |
| 웹(`ax.medisolveai.xyz`) | 보임 | **안 보임**(빈 칸) | **안 보임** — 대체 텍스트 「Building」 만 |
| 데스크톱 앱 | 보임 | **빈 칸** | **깨진 아이콘 「?」** |

- **웹·앱 둘 다** 일부 이미지만 막힌다 — 삼각형 아이콘은 뜨므로 「외부 이미지 전부 차단」 이 아니다. 출처(호스트)·형식·속성에 따라 갈릴 가능성 **(확인 필요)**
- 웹은 대체 텍스트, 앱은 깨진 아이콘 — 막히는 층이 다를 수 있다

## 원인 확정 (2026-10-07 · 운영 back 로그 + FE 리포트 §8)

- 외부 이미지는 막지 않는다 — 정제가 원격 `src` 를 떼고 **서버 프록시**(`/api/inbox/mail/{id}/remote-image?u=`)로 받는다(사용자 결정 10-06). 광고 메일(훌라로) 이미지처럼 PNG·JPEG 는 앱에서도 보인다
- 운영 로그: `remote image refused: host=camo.githubusercontent.com reason=이미지가 아닙니다` 반복 · 해당 요청 400. GitHub camo 가 감싼 원래 주소는
  - Deployment 상태 = `https://vercel.com/static/status/building.svg` → **SVG**
  - Project 아이콘 = `https://vercel.com/api/www/avatar?projectId=…&s=32` → 받은 바이트가 래스터 아님(SVG 추정)
- 프록시는 **바이트로 래스터(PNG·JPEG·GIF·WebP)만** 받고 SVG 는 거절한다 — 「같은 origin 에서 스크립트가 된다」 는 **의도된 규칙**(`external_inbox_upstream.py:10, 51, 356-360`). 그래서 SVG 를 쓰는 GitHub·Vercel 알림 메일의 아이콘만 빠진다. 삼각형 로고는 래스터라 보인다
- 웹 「대체 텍스트」 vs 앱 「깨진 ?」 — 같은 400 을 엔진(Chromium·WebKit)이 다르게 그리거나 오류 핸들러가 한쪽에서만 돈 것(코드로는 못 가름, FE §8-7)
- 결정할 것: SVG 를 받을지(서버에서 래스터로 바꿔 주기 / `Content-Security-Policy: sandbox` · `nosniff` 를 단 채 `image/svg+xml` 로 내주기 — `<img>` 로 그린 SVG 는 스크립트가 돌지 않는다) · 아니면 그대로 두고 실패 표시만 통일

## 결정 (사용자 2026-10-07)

- **프록시가 SVG 도 받는다** — 래스터로 바꾸지 않고 `image/svg+xml` 그대로 내주되 응답에 `Content-Security-Policy: sandbox`(+ `default-src 'none'`) · `X-Content-Type-Options: nosniff` 를 단다. `<img>` 로 그린 SVG 는 스크립트가 돌지 않고, 주소를 직접 열어도 sandbox 로 막힌다
- 나머지 거절 규칙(크기 · 리다이렉트 · 사설 IP 등)은 그대로
- 바뀌는 문서: 정제·프록시 docstring 의 「SVG 거절」(`external_inbox_upstream.py:10, 51`) · SPEC-008 원격 이미지 절

## 조사 항목

- 메일 본문 렌더 경로(`MailFrame.tsx` — iframe 에 직접 써 넣는 방식, WORK-011 PR #15)에서 외부 이미지를 막는 것: iframe `sandbox` · CSP(`img-src`) · 서버 정제(sanitize)에서 `src` 를 지우거나 바꾸는지 · 외부 이미지 차단 정책이 의도된 것인지(SPEC-008)
- 인라인 이미지(`cid:`)는 어떻게 처리하나
- 웹과 데스크톱 앱이 다르게 막는지(셸 CSP · on_navigation)
- **뜨는 이미지와 안 뜨는 이미지의 차이** — 같은 메일 HTML 에서 삼각형 아이콘과 Project·Deployment 이미지의 `src` 호스트·형식(svg/png)·속성 비교

## 진행 관리

- [ ] 조사(고도화 묶음 조사 FE 에 추가)
- [ ] 외부 이미지 표시 정책 결정 → 구현

## 완료 기록

- 2026-10-07 — WORK-012(DEC-009 · SPEC-008 v0.6.0 · SPEC-010) 로 구현 · 운영 반영(코드 PR #16 `5c8345e` · 2루프 #17 `d2a06fa`) · 운영 E2E 확인.
