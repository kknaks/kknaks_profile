# WORK-001 WP3 결과 보고 — front 뼈대 · 화면 · PWA

## 상태: done (실기기 · PWA 설치 · 실발화는 pending)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` · 브랜치 `kknaksss/interpret-pwa-poc` · 커밋 없음(변경만).

## 수행 — 파일 · 화면 목록

설정 · 빌드
- `front/package.json` — Next 16.4.3 · React 19.3 · Tailwind 3.4 · `@medisolve-ai/medikit@1.4.0` · pretendard 1.3.9 · `next dev/start -p 3800` · `test`(vitest)
  - ⚠ 원형 고정값 `next ^16.4.0` 은 `npm run build` 가 **보안 경고로 멈춘다**(GHSA-2464-fhr4-w9xw 등 critical — 16.0.0 ~ 16.4.0). 같은 16.4 패치인 **16.4.3** 으로 올림(`eslint-config-next` 도). SPEC 은 「Next.js 16」 만 정함
- `front/package-lock.json` · `tsconfig.json` · `eslint.config.mjs` · `postcss.config.mjs` · `global.d.ts` · `.gitignore` · `.dockerignore` — 원형 `procedure/front` 복사
- `front/tailwind.config.ts` — `medikitPreset` + content 에 medikit dist(원형 방식)
- `front/next.config.ts` — standalone · `/sw.js` no-cache 헤더
- `front/.env.example` — `NEXT_PUBLIC_API_BASE_URL=` 이름만(개발 값은 `.env.local` · gitignore)
- `front/Dockerfile` — 원형 방식(ARG → ENV → build · standalone · 비루트) · 포트 3800
- `front/vitest.config.ts` · `front/tests/*.test.ts`

lib
- `lib/api.ts` — back 호출 한 곳(`login` · `me` · `glossary` · `openInterpretSocket`) · 주소는 `NEXT_PUBLIC_API_BASE_URL` 만 · 보호 API 401 → 토큰 지우고 `/login`
- `lib/session.ts` — `localStorage` `interpret.session` = `{token, expiresAt}` · 만료면 읽을 때 지움
- `lib/langs.ts` — 6개 언어 · 드롭다운 이름(자기 표기) · 한국어 이름 · **외국어 영역 문구 6 × 7(+ 출력 중 2값)**
- `lib/prefs.ts` — 마지막 언어 · 뒤집힘 기억
- `lib/view.ts` — 자막 영역 배치(§7.5) · 원 상태 판정(§7.3 #1 ~ #8) 순수 함수
- `lib/phrases.ts` — 원 아래(한국어) · 외국어 영역 안내 문구
- `lib/demo.ts` — 가짜 렌더(개발 서버에서만 `/?demo=<상태>`)

화면
- `/login`(`app/login/page.tsx`) — 「통역」 `text-typo-headline-md-600` · medikit `Input` × 2 · `Button` solid 가득 · 오류 한 줄 `text-red`(서버 message 그대로 · 네트워크 「서버에 연결하지 못했어요」) · 아이디 미리 채움 없음
- `/`(`app/(main)/page.tsx` + 가드 `app/(main)/layout.tsx`) — `components/interpret/InterpretScreen.tsx`
  - 헤더(뒤집히지 않음) 햄버거 = 인라인 SVG + medikit `Popover` · `Button` 두 개(용어집 · 로그아웃)
  - 외국어 영역 `rotate-180`(기본) · medikit `ComboBox`(6개 · `hasSearch=false` · `hasAllOption=false`) · 전환 아이콘(인라인 SVG) · 안내 문구(고른 언어 · 오류 때 `ErrorIcon`)
  - 가운데 원(고정 높이 줄) · 한국어 안내 · 오류면 문구 + [다시 연결]
  - 한국어 영역 · 자막(`final:false` `text-ms-gray-500` · `final:true` `text-ms-gray-800` · 끝으로 따라감)
  - 「탭해서 통역 시작」 오버레이(`bg-ms-overlay`) — 외국어 쪽 절반은 고른 언어 · 뒤집힘을 따름
- 용어집 패널 `components/interpret/GlossaryModal.tsx` — medikit `BaseModal` + `Table` · 열 때마다 `GET /api/glossary?lang=` · 세 칸 카테고리 · 한국어 · 〈언어〉 · `loaded=false` 문구
- PWA — `app/manifest.ts`(통역 · standalone · portrait · 192 · 512 · maskable) · `apple-touch-icon` 180(`layout.tsx` metadata) · `public/icons/*.png`(`scripts/make-icons.mjs` 로 생성) · `public/sw.js`(앱 껍데기만 · `/api` · 다른 출처 · WS 안 건드림 · 오프라인 = `public/offline.html` 「인터넷 연결이 필요해요」) · 운영 빌드에서만 등록(`components/ServiceWorker.tsx`) · wake lock(통역 화면 · 다시 보이면 재요청 · 기능 감지)

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과(출력 0) |
| `npm run lint` | 통과(경고 0) |
| `npm run build` | 통과 — 16.4.3 · 경로 `/` · `/login` · `/manifest.webmanifest` |
| `npx vitest run` | 2 파일 · 15 시험 통과(영역 배치 · 상태 판정 · 멈춤 중 출력 → 멈춤 · 백그라운드 → 시작 전 · 오류 외국어 문구 · 반이중 타이머) |
| `node scripts/check-classes.mjs`(빌드 CSS 전수 대조) | **쓴 클래스 78개 · 없는 것 0** · 음성 대조: 일부러 넣은 `bg-ms-gray-900` 은 잡힘 |

실 back 확인 — back 워커의 WP1 코드(워크트리 `back/` 그대로 · 읽기만)를 `:8800` 에 **가짜 로그인 값**(실행 때 무작위 생성 · 파일 · 리포트에 안 씀)으로 띄우고, front dev `:3800` + 헤드리스 Chrome(가짜 마이크 장치)으로:

| 항목 | 결과 |
|---|---|
| 토큰 없이 `/` | `/login` 으로 |
| 틀린 비밀번호 | 서버 문구 「아이디 또는 비밀번호가 맞지 않아요」 한 줄 |
| 로그인 | `/` · `localStorage` 키 `token` · `expiresAt` |
| 통역 화면 진입 | 「탭해서 통역 시작」 오버레이(탭 전 WS · 마이크 없음) |
| 용어집 6개 언어 | en · ja · zh · th · vi · yue 모두 158행 · 제목 「용어집 · 〈한국어 이름〉」 · 세 칸 · yue 번체(「填充劑」) 그대로 |
| 오버레이 탭 | AudioContext · 마이크 · WS(`?token=`) · `start` → back 이 `error no_api_key`(키 없음) → 오류 상태 · 「SONIOX_API_KEY 가 .env 에 없어요」 + [다시 연결] · 외국어 영역 「Connection error」 + `ErrorIcon` |
| 로그아웃 | `/login` · 토큰 지워짐 |

스크린샷 `wp3-fe-shots/`
- `01-login` · `02-login-error` · `03-start-overlay-flipped` · `04-menu` · `05-glossary-{en,ja,zh,th,vi,yue}` · `06-after-tap-error-no-key`
- 가짜 렌더(뒤집힘) `10-demo-flipped-{idle,error,connecting,output-foreign,output-korean,paused,paused-output,listen-ko,listen-fo,standby}` · 바로 보기 `10-demo-upright-{idle,listen-fo,standby}`
- `20-combobox-open-flipped` · `21-combobox-open-upright`

띄운 프로세스(back `:8800` · front dev `:3800`)는 WP4 실 back 확인 뒤 내린다. 사용자 포트(3700 · 8700 LISTEN 중)는 건드리지 않았다.

## 계약 대조 — SPEC 항목별

| SPEC | 같음 / 다름 |
|---|---|
| §2.2 포트 3800 고정(`package.json` · Dockerfile) | 같음 |
| §2.3 `NEXT_PUBLIC_API_BASE_URL` — `.env.local` · Dockerfile ARG → ENV 만 | 같음 |
| §3.2 토큰 `localStorage` `interpret.session` `{token, expiresAt}` · 만료 지움 | 같음 |
| §3.3 응답 · 오류 모양 · 401 → 로그인 · 로그아웃 3단계 | 같음(실 back 응답 모양 확인) |
| §4.6 용어집 응답 `{loaded, version, count, lang, rows:[{category, ko, term}]}` | 같음(실 back) |
| §6 화면 둘 · 토큰 없으면 `/login` · medikit · `data-product` 없음 | 같음 |
| §7.1 로그인 배치 · 문구 | 같음 |
| §7.2 배치 · 180° · 전환 아이콘(인라인 SVG) · `ComboBox` · 방향 기억(처음 뒤집힘) · 언어 바꿈(stop → 새 start · 자막 지움) | 같음 |
| §7.3 상태 8개 · 색 클래스 · 판정 순서 · 외국어 문구 | 같음(가짜 렌더 · 단위 시험) |
| §7.6 햄버거 `Popover` + `Button` · `BaseModal` + `Table` · 패널 안 뒤집힘 | 같음 |
| §8 manifest · 아이콘 · 서비스 워커 · wake lock · 오프라인 화면 | 같음 — 서비스 워커는 손으로 쓴 `public/sw.js`(라이브러리 없음 · Next 16 Turbopack 과 무관) |

## 이슈 · 코디가 확인할 것

1. **Next 16.4.0 → 16.4.3**(위) — 원형 레포 `procedure/front` 도 같은 경고 대상이다(원형은 이 작업 범위 밖이라 안 건드림).
2. **OQ-010 — 뒤집힌 상태에서 `ComboBox` 펼친 목록은 뒤집히지 않는다**(`20-combobox-open-flipped`: 목록이 바로 선 채 화면 아래쪽으로 펼쳐짐 · 5개 보이고 `廣東話` 는 스크롤). SPEC 기본값대로 그대로 둠 → 로컬 E2E 피드백.
3. **오버레이 범위** — SPEC 「화면 전체 오버레이」 를 **헤더 아래 전체**로 했다(헤더의 햄버거 → 로그아웃 · 용어집은 시작 전에도 열 수 있게). 원 · 드롭다운 · 아이콘은 덮인다.
4. **외국어 영역 문구 6 × 7** — `lib/langs.ts` 상수. 원어민 검수 없음(OQ-006 · WP5). yue 는 번체 · 출력 언어 이름 「中文」(TTS 가 만다린 · OQ-001).
5. 시안 없는 자리(기본값으로 둔 것 · OQ-010): 원 88px · 음량 배율 1.0 ~ 1.5(대기 1.0 ~ 1.2) · 맥박(`.ip-pulse` 회색 그림자) · 두 영역 바탕 `bg-ms-gray-100` · 자막 글자 `text-typo-title-md-500` · 헤더 52px.
6. 용어집 표는 좁은 화면에서 가로 스크롤(긴 표기 · 괄호 병기).
7. pending — 실기기(마이크 · PWA 설치 · 화면 꺼짐 방지 · iOS) · 서비스 워커 동작(운영 빌드 + 보안 출처) · 맥 Safari 확인.
