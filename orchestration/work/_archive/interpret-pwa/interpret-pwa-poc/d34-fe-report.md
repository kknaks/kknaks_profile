# D-34 — frontend 결과 보고 (시작 오버레이에서 언어 고르기)

## 상태: done (실기기 · 실 back 확인은 pending — 아래)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(main 9befd18 위 · 커밋 없음). 범위 `front/**` 만.

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `front/components/interpret/StartOverlay.tsx`(새) | State-1 오버레이 — 제목 「통역할 언어를 고르세요」 + 언어 단추 7개(목록 표시 이름 그대로: English · 日本語 · 中国 · 简体中文 · 臺灣 · 繁體中文 · ไทย · Tiếng Việt · 廣東話) · 두 줄 그리드(2칸 · 마지막 廣東話 는 두 칸) · 단추 h64 이상 · 흰 바탕 · 둥글기 12 · `text-typo-heading-md-600`. **마지막에 쓴 언어는 표시만** — `border-primary text-primary` + 「지난번」 · `aria-current` (자동 선택 · 자동 시작 없음 · 처음이면 표시 없음). 화면 루트 `absolute inset-0 z-20 bg-ms-overlay` → 헤더(햄버거)까지 덮음(시안 State-1 · WARN-3 그대로) · **회전 없음**(상담사 방향 · 외국어 영역 뒤집힘과 무관). 훅 없음(시험용) |
| `front/components/interpret/InterpretScreen.tsx` | 옛 「탭해서 통역 시작」 두 쪽 오버레이 → `StartOverlay`. 단추 누름 = `onStartPick(l)`: 그 언어로 바꾸고 기억 · 언어가 바뀌면 자막 비움 · **사용자 동작 안에서 바로 `startSession(l)`**(AudioContext 깨우기 → 마이크 → WS → `start{lang}` · §7.4). 백그라운드 복귀(`conn` idle)도 같은 오버레이 |
| `front/lib/start.ts`(새) | `pickStart(picked, current)` → `{lang, clearCaptions}` |
| `front/lib/prefs.ts` | `readLastLang()` — 기억값이 있을 때만 그 언어 · 처음이면 null |
| `front/tests/start-overlay.test.ts`(새) | ① 단추 7개 순서 · 렌더만으로는 시작 안 함 · zh-Hant 단추 누름 → onPick('zh-Hant') · `pickStart` ② 마지막 언어만 `aria-current` · 처음이면 없음 |

- `TapIcon`(손가락)은 이 화면에서 더 안 쓴다(`components/icons.tsx` 에 남겨 둠).
- 외국어 오버레이 문구 `FOREIGN_PHRASES[*].idle` 은 이제 화면에 안 나온다(값은 남겨 둠 · 계약 영향 없음).

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(경고 0) |
| `npm run build` | 통과 |
| `npx vitest run` | 8 파일 · **32 통과**(새 2) |
| 클래스 대조 | 200 · 없는 것 0 |

스크린샷 `d34-fe-shots/`(390 × 844 · 운영 빌드):

| 파일 | 확인값 |
|---|---|
| `D34-overlay-upright-mode.png` | 오버레이 transform 없음 · 헤더 햄버거 자리 = 오버레이(안 눌림) · 단추 7개 · 「臺灣 · 繁體中文 · 지난번」 표시 |
| `D34-overlay-flipped-mode.png` | 뒤에 있는 외국어 카드는 `matrix(-1,0,0,-1)`(뒤집힘) · **오버레이와 그 조상은 회전 없음**(바로) · 같은 7개 |

- 단추 누름 확인: 日本語 누름 → WS 1개(`/api/interpret?token=…`) · 보낸 첫 텍스트 `{"type":"start","lang":"ja"}` · 오버레이 닫힘 · 「연결 중…」 · 기억값 `ja` · 언어 단추 「日本語」. 그 전(렌더 · 새로고침)엔 WS 0 · 보낸 것 0.
- 방법: `:3800` · `:8800` 을 compose 가 쓰고 있어 포트를 열지 않고 운영 빌드를 헤드리스 Chrome request interception 으로 내줬다(서비스 워커 우회 · back 호출 · WS 는 페이지 안 가짜 · compose 안 건드림).

## 이슈 · 코디가 확인할 것

1. **시안 없음** — 제목 문구 「통역할 언어를 고르세요」 · 「지난번」 표시 · 단추 크기 · 마지막 단추 두 칸은 frontend 기본값(medikit 토큰만). designer 시안이 생기면 맞춘다.
2. 실기기(iPhone)에서 단추 탭 → 마이크 권한 → 소리 나는지(AudioContext 가 단추 탭 안에서 깨는지) · 실 back 실발화는 compose 재빌드 · 배포 뒤.
3. 시작 뒤 언어를 바꾸는 길(외국어 카드의 언어 목록)은 그대로 있다.

## 추가 — 시안 r6 맞춤 (2026-10-27)

시안 `design/project/State-1-Start.dc.html`(r6 · 10:38) 값으로 `StartOverlay.tsx` 를 고쳤다(다른 파일 그대로):

| 항목 | 시안 r6 | 구현 |
|---|---|---|
| 제목 | 「통역할 언어를 고르세요」 `text-typo-title-md-600 text-ms-white` | 같음(`h2#start-title` · 대화상자 `aria-labelledby`) |
| 부제 | 「누르면 그 언어로 바로 통역을 시작해요」 `text-typo-body-400` 흰 · 투명도 .8 | 같음(`opacity-80`) |
| 배치 | 세로 가운데 · 안쪽 24/16 · 사이 20 · 2열 그리드 사이 12 | 같음(최대 폭 제한 없앰 — 시안대로 가득) |
| 단추 | h72 · 둥글기 12 · 테두리 2 · `bg-ms-white border-ms-white text-ms-gray-800 text-typo-title-sm-600` · 廣東話 두 칸(마지막) | 같음 |
| 마지막 언어 | `bg-primary-100 border-primary` + 「최근 사용」 `text-typo-caption-md-600 text-primary` | 같음(「지난번」 → 「최근 사용」) |

검증(1회): `tsc` 통과 · `lint` 통과 · `build` 통과 · `vitest` 32/32 · 클래스 198 중 없는 것 0. 스크린샷 `d34-fe-shots/D34-overlay-upright-mode.png`(+ `-flipped-mode` 도 다시 찍음 — 오버레이 회전 없음 · 헤더 덮음) 갱신. 日本語 누름 → `start{lang:"ja"}` 그대로.
