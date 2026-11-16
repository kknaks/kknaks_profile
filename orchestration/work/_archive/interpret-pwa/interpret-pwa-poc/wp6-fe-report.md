# WORK-001 WP6-FE 결과 보고 — front 수정 묶음(시안 · D-18 ~ D-25 · 리뷰 FAIL-1 · WARN-3 · WARN-4)

## 상태: done (실기기 · iOS · PWA 설치는 pending — 배포 뒤)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` · 커밋 없음(1루프 변경 위에 고침). 범위 `front/**` 만.
진행 중 코디가 범위를 넷 더했다 — **D-22**(원 위아래 두 언어 안내) · **D-22 보충**(한국어 듣는 중에도 외국어 안내) · **D-23**(원 줄 축소 140 · 원 64) · **D-24**(자막 말풍선 + 16px · 시안 Captions r3) · **D-25**(자막 자동 스크롤 + 「↓ 최신」). 모두 반영했다. 시안과 다르면 D-22 ~ D-25 가 이긴다는 지시대로 했고, designer 가 16:48 · 16:55 에 올린 시안 r3(State-* · Captions)는 그 값에 맞췄다.

## 수행 — 파일 · 화면 목록

| 파일 | 무엇 |
|---|---|
| `front/app/styles/ceramique-theme.css`(새) | cc-prototype `origin/main:procedure/front/app/styles/ceramique-theme.css` 복사(시안 사본과 같음 확인) |
| `front/app/layout.tsx` | `<html lang="ko" data-product="ceramique">` · import 순서 medikit styles → ceramique → patches · `metadata.title` · `applicationName` · `apple-mobile-web-app-title` 「통키」 · body `bg-ms-gray-100` |
| `front/app/manifest.ts` | `name` 「통키」 · `short_name` 「Tongky」 |
| `front/app/globals.css` | 출력 중 링 두 겹 맥박(`--ring` rgb · 7px 18% + 15px 8%) |
| `front/app/styles/medikit-patches.css` | `[BaseModal-1]` 추가 — 용어집 모달만 BaseModal 머리 · 26px 간격 숨김(부제를 넣을 수 없어 시안 머리를 몸에 그림) |
| `front/app/login/page.tsx` | 시안 Main · Login-Error · Login-Locked — 카드 · 48px 말풍선 원 · 「통키」 · 부제 · medikit `Input`(xl 50 · `isError` = `border-red` · `aria-invalid`) · 눈 단추(`showPasswordToggle`) · medikit `Button` xl · 401 줄(아이콘) · 429 `bg-red-100` 박스(시계) · 네트워크 줄 |
| `front/components/icons.tsx`(새 · 옛 `components/interpret/icons.tsx` 지움) | 시안 인라인 SVG — 햄버거 · 회전(⇅ 삭제) · 말풍선 · 경고 · 시계 · 손가락 · 마이크 · 스피커 · ‖ · ! · 다시 · 책 · 로그아웃 |
| `front/components/interpret/InterpretScreen.tsx` | 헤더 56 · main 12/16/16 · 카드 둘(흰 · 12 · 그림자 · 14/16) · 회전 단추(바로 보기 = `bg-primary-100 border-primary-500 text-primary`) · `ComboBox` l(44 · 최소 156) · **가운데 줄 140(D-23)** — 원 위 = 고른 언어 안내 + 색 점(외국어 영역과 같이 뒤집힘 · D-22) · 92 상자 · 원 아래 = 한국어 안내 · 오류 = `bg-red-100` 박스 + 원 56 + 문구 · [다시 연결](medikit Button ss round) · **오버레이를 화면 루트로**(헤더까지 덮음 · WARN-3 · 손가락 원 72 · 흰 선 · 위 절반은 뒤집힘 따라감) |
| `front/components/interpret/Circle.tsx` | 상태별 색 · 크기(D-23 · 시안 r3: 기본 64 · 오류 56) · 글리프 · 링 · aria-label 「멈춤」/「다시 듣기」 |
| `front/components/interpret/CaptionArea.tsx` | **말풍선(D-24)** — 영역을 보는 사람 말 = 오른쪽(한국어 영역 `bg-primary-100` · 외국어 영역 `bg-purple-100`) · 상대 = 왼쪽 `bg-ms-gray-200` · 최대 80% · 16(말한 쪽 아래 4) · 8/12 · 사이 8 · `text-typo-heading-md-500`(16px) · `final:false` `text-ms-gray-600` · **자동 스크롤(D-25)** — 맨 아래 40px 안이면 따라감 · 올려 두면 안 끌어내림 · 새 말풍선이면 「↓ 최신」(medikit Button ss round) · 영역마다 따로 |
| `front/components/interpret/HeaderMenu.tsx` | 햄버거 44(열림 `bg-ms-gray-200` · 「메뉴 열기/닫기」) · 「Tongky」 `text-typo-title-md-600 text-primary` · Popover 196 · 10 · 6 · `shadow-pop-over-more` · 위 58 · 왼쪽 8 · 용어집(gray-800) · 구분선 · 로그아웃(`text-red`) |
| `front/components/interpret/GlossaryModal.tsx` | BaseModal(560 · 720 · 14) · 제목 「용어집 · 〈언어 이름〉」 `text-typo-title-sm-600` · 부제 「〈count〉개 · 읽기 전용」 · `CloseIcon` · Table 34 / 30 / 36% · 머리 `bg-ms-gray-200` · 칸 글자 시안 값 · 몸만 스크롤 |
| `front/lib/output.ts`(새) | 재생 쪽 판단 — **FAIL-1** 버림 표시(큐 비우면 다음 `audio_start` 까지 조각 · `audio_end` 버림 · 게이트 안 건드림) · **WARN-4** 출력 표시 = 그 발화 첫 조각 재생 시작 시각(마이크 막음은 `audio_start` 즉시) |
| `front/lib/interpret.ts` | `HalfDuplexGate` 직접 대신 `OutputController` 사용 · `onAudio` 에서 버림 |
| `front/lib/view.ts` | `Line.mine` · `isMine(side, area)`(D-24) |
| `front/lib/scroll.ts`(새) | `isNearBottom`(40px) · `hasNewBelow`(D-25) |
| `front/lib/langs.ts` · `lib/phrases.ts` | 외국어 안내에 `listeningKorean`(D-22 보충) · `latest`(「↓ 최신」 외국어 영역) 6개 언어 |
| `front/lib/demo.ts` | 상태 시안과 같게 자막 비움 · `captions` 데모(시안 Captions 문장) |
| `front/public/icons/*` · `scripts/make-icons.mjs` · `public/offline.html` | 아이콘 · 오프라인 화면 색 ceramique `#2498bd` · 제목 통키 |
| `front/scripts/check-classes.mjs` | 클래스 변수(`const card = '…'`) · 원 `cls` 도 대조하게 넓힘 |
| `front/tests/output.test.ts` · `tests/scroll.test.ts`(새) · `tests/view.test.ts` | FAIL-1 · WARN-4 · D-24 · D-25 · D-22 보충 시험 |

## 검증 — 명령과 결과 (WP6-FE 행의 부분 명령 · 최종 코드 1회씩)

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(경고 0) |
| `npm run build` | 통과(Next 16.4.3) |
| `npx vitest run` | 4 파일 · **23 통과**(새 8 — FAIL-1 「pause 뒤 같은 발화 조각 → 재생 0 · 게이트 그대로 · 다음 `audio_start` 뒤 재생」 · WARN-4 「앞 발화 재생 중 다음 `audio_start` → 표시는 앞 발화 끝(다음 첫 조각 시작)에 · 마이크 막음 즉시」 · 재생 끝 → 표시 없음 · D-24 좌우 3 · D-25 2 · D-22 보충 1) |
| `node scripts/check-classes.mjs` | **쓴 클래스 166 · 빌드 CSS 에 없는 것 0**(시안에서 옮긴 `bg-primary-100` · `border-primary-500` · `bg-red-100` · `border-red` · `bg-purple-100` · `bg-ms-overlay` · `shadow-pop-over-more` · `text-typo-title-md-600` · `text-typo-title-lg-600` 등 포함) · 음성 대조: 변수에 넣은 가짜 `bg-ms-gray-900` 도 잡힘 |
| manifest(운영 빌드 `next start`) | `"name":"통키","short_name":"Tongky"` · 페이지 `<title>통키</title>` · `data-product="ceramique"` · `apple-mobile-web-app-title` 통키 |

### 시안 대조 스크린샷 — `wp6-fe-shots/`(390 × 844 · 시안 파일과 같은 상태 · 가짜 렌더는 개발 서버 `/?demo=`)

계산값: `--ms-primary` = **`#2498bd`** · 로그인 단추 `rgb(36,152,189)` · 오버레이 시작 전 햄버거 자리 `elementFromPoint` = 오버레이 단추(**햄버거 안 눌림**) · 메뉴 위 58 · 왼쪽 8 · 폭 196 · 로그아웃 `rgb(255,78,81)` · 안내 글자 13px · 말풍선 16px.

| # | 파일 | 시안 | 같음 | 다름(이유) |
|---|---|---|---|---|
| 1 | `01-Main` | Main | 카드 · 말풍선 원 · 통키 · 부제 · 칸 · 단추 | 눈 아이콘 = medikit `EyeIcon`(Input `showPasswordToggle` — aria · gray-600 은 시안과 같음) |
| 2 | `02-Login-Error` | Login-Error | 두 칸 `border-red` · `aria-invalid` · 아이콘 + 빨간 줄 | — |
| 3 | `03-Login-Locked` | Login-Locked | `bg-red-100` 박스 · 시계 · 칸 테두리 그대로 | — |
| 4 | `04-Interpret-Flipped` | Interpret-Flipped | 헤더 · 카드 · 회전 단추 · 뒤집힘 | 원 줄 = D-22 · D-23(140 · 원 64 · 위 안내) — 시안 r3 와 같음 |
| 5 | `05-Interpret-Upright` | Interpret-Upright | 회전 단추 `bg-primary-100 border-primary-500 text-primary` | 위와 같음 |
| 6 | `06-Captions` | Captions r3 | 말풍선 좌우 · 색 · 80% · 16(4) · 16px · gray-600 | — |
| 7 | `07-State-1-Start` | State-1-Start | 화면 루트 오버레이 · 헤더 덮음 · 손가락 원 · 흰 선 · 위 절반 뒤집힘 | — |
| 8 | `08-State-2-Error` | State-2-Error r3 | 원 56 · 링 5 · 위 `bg-red-100` 박스 · 아래 문구 + [다시 연결] h28 | 아래 문구 = 실제 오류 message(시안 「연결이 끊겼어요」는 예시) · 박스 아이콘 = medikit `ErrorIcon`(SPEC §7.3) |
| 9 | `09-State-3-Connecting` | State-3 | 64 · 점 셋 6px | — |
| 10 | `10-State-4a-Speaking-Foreign` | State-4a | purple 64 · 스피커 · 링 두 겹 맥박 · 점 purple | — |
| 11 | `11-State-4b-Speaking-Korean` | State-4b | primary · 점 primary | — |
| 12 | `12-State-5-Paused` | State-5 | 64 · ‖ · 「다시 듣기」 | — |
| 13 | `13-State-6-Listening-Korean` | State-6 | primary · 마이크 | 원 위 「Listening to Korean…」 + primary 점(D-22 보충) · 음량 64 → 88(가짜 렌더는 64) |
| 14 | `14-State-7-Listening-Foreign` | State-7 | purple · 「Listening」 | 위와 같음(시안은 88 예시) |
| 15 | `15-State-8-Idle` | State-8 r3 | 64 · 링 7 gray · 「Please speak」 | — |
| 16 | `16-Menu` | Menu | 위 58 · 왼쪽 8 · 196 · 열림 `bg-ms-gray-200` · 로그아웃 red | 항목 hover `bg-ms-gray-100`(시안에 hover 없음) |
| 17 | `17-Glossary` | Glossary | 제목 「용어집 · English」 · 부제 「158개 · 읽기 전용」 · 칸 111 / 98 / 117px(34 / 30 / 36%) · 158행 | 닫기 아이콘 = medikit `CloseIcon` 20(시안 22) |
| D-22 | `D22-upright-output-foreign` · `D22-upright-idle-overlay` + `04`(뒤집힘) · `10`(출력 중) | — | 바로 보기면 원 위 안내 · 오버레이 위 절반 모두 바로 · 뒤집힘이면 함께 180° | — |
| D-24 | `D24-bubbles-live` | — | 가짜 back 실흐름 말풍선 | — |
| D-25 | `D25-latest-button` | — | 한국어 영역만 위로 올림 → 그 영역 아래 「↓ 최신」 · 외국어 영역은 계속 따라감 | — |
| 실발화 | `L1-live-progress` · `L2-live-after` | — | 실 back · 실 Soniox | — |

- 시안 `.dc.html` 은 `support.js` · `<x-dc>` 런타임이 없어 로컬에서 그려지지 않는다 → **나란히 이미지가 아니라 시안 파일의 클래스 · 크기 값과 대조**했다(위 표).

### 실발화 1회 — 실 back + 실 Soniox(키는 루트 `.env` · 코드가 읽음 · 값 출력 0)

- 순서(포트 겹침 방지): 16:50:19 `8800` 비어 있음 확인 → **내가 back(워크트리 `back/` 의 그때 코드 · WP6-BE 진행 중 상태)을 `:8800` 에 띄움**(16:50) → 로그인 · 용어집 · 실발화 3회 → **17:02:05 내가 띄운 back 내림** → 17:03 가짜 WS(`:8800` · D-25 · FAIL-1 확인) 띄웠다 내림 → front dev `:3800` · `next start :3800` 내림. 마지막 확인: 8800 · 3800 비어 있음 · 사용자 포트 3700 · 8700 안 건드림.
- 로그인: 헤드리스 Chrome 에 루트 `.env` 값을 스크립트가 직접 넣음(출력 · 파일 기록 0) → 200.
- 마이크: Chrome 파일 가짜 마이크(`--use-file-for-fake-audio-capture`)가 이 환경에서 무음(RMS 0)이라, **시험 장치로 `getUserMedia` 를 WAV 재생 스트림으로 바꿔 끼움**(앱 코드 아님). 음성 = macOS `say`(한국어 Yuna 「안녕하세요. 오늘 보톡스 상담을 받으러 오셨나요?」 → 6초 쉼 → 영어 Samantha 「Yes. I want to ask about fillers for my cheeks.」).
- 결과(마지막 회 · MutationObserver 시각):

| ms | 원 | 한국어 안내 |
|---|---|---|
| 0 → 1666 | gray-300 → gray-400 | 연결 중… → 말씀하세요 |
| 2928 | primary | 한국어 듣는 중 |
| 7707 | purple | 영어로 출력 중 |
| 12615 | purple | 영어 듣는 중 |
| 15977 | primary | 한국어로 출력 중 |
| 21502 | gray-400 | 말씀하세요 |

  - 자막: 외국어 영역 = 「Hello, did you come in for today's Botox consultation?」 · 「Yes, I want to ask about fears for my cheeks.」 / 한국어 영역 = 「안녕하세요, 오늘 보톡스 상담을 받으러 오셨나요?」 · 「네, 제가 두려워하는 것에 대해 여쭤보고 싶어요. 볼에 대해서요.」 — 각 영역에 자기 언어만(D-16).
  - TTS 수신 u1 176,128 B · u2 245,760 B · **재생 구간(`audio_start` ~ 재생 끝 + 400 ms · 4,659 ms · 6,116 ms) 마이크 송신 0 B** · 재개 뒤 첫 송신 3 ms.
  - WARN-4: 출력 표시는 `audio_start` 뒤 584 · 591 ms(첫 조각 재생 시작)에 바뀜 · 마이크 막음은 `audio_start` 즉시.
  - 용어집 모달 158행 · 로그아웃 때 `stop` 전송.
  - 참고(front 밖): 「fillers」 가 「fears」 로 잡혔다 — `say` 합성 음성 한 번이라 판정하지 않음(STT · 용어집은 WP6-BE · WP7).
- 가짜 back(:8800) 확인: D-25 표(위) · FAIL-1 — 출력 중 원 누름 → `pause` 전송 · 그 뒤 같은 발화 조각 2초 · `audio_end` 동안 안내는 「멈춤」 그대로(재생 안 함) · 다음 `audio_start`(u13) → 「한국어로 출력 중」 → 끝나고 「멈춤」.

## 계약 대조 — SPEC 0.3.0 · DEC

| 항목 | 같음 / 다름 |
|---|---|
| §6 테마 ceramique · 색 규칙 · 앱 이름 · 아이콘 | 같음 |
| §7.1 로그인 3 상태 | 같음(눈 아이콘만 medikit) |
| §7.2 배치 · 회전 단추 · 햄버거 · `ComboBox` | 같음 — 펼친 목록은 여전히 안 뒤집힘(OQ-010) · 선택 이름 글자색은 medikit 안쪽 `text-ms-black`(시안 gray-800) |
| §7.3 상태 8개 · 원 · 글리프 · 링 · 점 · 오버레이 헤더 덮음 | 같음 — 크기는 **D-23**(시안 r3 = 64 · 56 · 92 상자 · 140 줄) · 안내 위치는 **D-22**(SPEC 표의 「외국어 영역 안내」 → 원 위) · 한국어 듣는 중 외국어 안내 있음(**D-22 보충**이 SPEC 「—」 를 이김) |
| §7.4 FAIL-1 버림 · WARN-4 표시 시점 | 같음(단위 시험 + 실발화 + 가짜 back) |
| §7.5 자막 | **D-24** 말풍선 · 16px(코디 결정)로 바뀜 · `final:false` gray-600 · D-16 그대로 · **D-25** 자동 스크롤 |
| §7.6 메뉴 · 용어집 모달 | 같음 |
| §8 manifest 이름 | 같음 |
| §9.2 | 클래스 0 누락 · 17장 · 단위 시험 |

## 이슈 · 코디가 확인할 것

1. **SPEC 갱신 필요(코디 → planner)**: §7.3 원 크기 · 안내 위치(D-22 · D-23) · 상태 6 외국어 안내(D-22 보충) · §7.5 말풍선 · 16px · 자동 스크롤(D-24 · D-25) · 가운데 줄 196 → 140.
2. **13px 안내 글자**: medikit 에 13px typo 토큰이 없다(caption 12 · body 14). 시안처럼 `text-typo-caption-md-500/600` + `!text-[13px]` — `!` 없이는 토큰 크기(12px)가 이겨 13px 가 안 된다(계산값으로 확인).
3. **새 문구(원어민 검수 없음 · OQ-006 범위)**: `listeningKorean` 6개(en 「Listening to Korean…」 등) · 「↓ 최신」 외국어 영역 라벨 6개(en 「Latest」 · ja · zh · yue 「最新」 · th 「ล่าสุด」 · vi 「Mới nhất」) — 코디 지시에 외국어 영역 라벨 값이 없어 frontend 가 정했다. 한국어 영역은 「↓ 최신」.
4. **BaseModal 패치**(`[BaseModal-1]`): 부제 · 제목 크기를 시안대로 하려고 용어집 모달만 medikit 머리를 숨기고 몸에 그렸다. DS 반영 요청 후보.
5. 시안 `.dc.html` 을 로컬에서 그릴 수 없어 이미지 나란히 대조는 못 했다(값 대조로 대신).
6. 개발 전용 가짜 렌더 `/?demo=` 에 `captions` 를 더했다(운영 빌드에서는 꺼짐).
7. pending — 휴대폰 실기기(마이크 · iOS AudioContext · PWA 설치 · 화면 꺼짐 방지) · 맥 Safari. 실 사람 목소리 발화는 WP7.
8. 지우려다 못 한 것: 스크린샷 폴더의 옛 파일 정리용 `rm` 이 안전 검사로 막혔다 — 같은 이름으로 덮어써서 남은 옛 파일은 없다(`wp6-fe-shots/` 는 이번 회 파일만).
