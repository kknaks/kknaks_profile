# 폰 피드백 2 — frontend 결과 보고 (D-28 개정 · D-29 · D-30)

## 상태: done (화면 · 실기기 확인 pending — 아래 이슈 1)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(폰 피드백 1 변경 위 · 커밋 없음). 범위 `front/**` 만(코디 지시 — backend · designer 절은 각 워커).

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `front/lib/langs.ts` | **D-28 개정** 목록 표기 zh 「中国 · 简体中文」 · zh-Hant 「臺灣 · 繁體中文」 · yue 「廣東話」 그대로 · 한국어 이름 zh 「중국어」 · zh-Hant **「대만어」**(원 아래 「대만어로 출력 중」 · 「대만어 듣는 중」) |
| `front/components/interpret/GlossaryModal.tsx` | 제목 · 셋째 칸 머리 = 한국어 이름(「용어집 · 대만어」 · 「용어집 · 중국어」 …) |
| `front/lib/interpret.ts` | `clearPlayback()` — 재생 큐 비움 · 남은 조각은 다음 `audio_start` 까지 버림(FAIL-1 과 같은 길) · 멈춤 · 연결 유지 |
| `front/lib/view.ts` | `canReset(state)` — 멈춤(#5)에서만 true |
| `front/components/interpret/InterpretScreen.tsx` | **D-29** 멈춤 때 원 상자 오른쪽(가운데 줄 · 안 뒤집힘)에 「초기화」(medikit Button outlined · gray · ss · round · 한국어만 · 확인 창 없음) → `clearPlayback()` + 두 영역 말풍선 비움. 멈춤 · 언어 · WS 그대로 |
| `front/lib/api.ts` | `authConfig()` = `GET /api/auth/config` · `demoLogin()` = `POST /api/auth/demo`(둘 다 인증 없음 · 비밀번호 front 에 없음) |
| `front/app/login/page.tsx` | **D-30** 진입 때 config → `demoLogin: true` 면 입력 칸 없이 「로그인」 단추 하나(→ demo → 통역 화면) · false 거나 실패면 지금 화면 · 받기 전에는 단추 · 칸을 그리지 않음(깜빡임 방지) · 데모 오류(401 등)는 지금처럼 서버 문구 한 줄 |
| `front/tests/langs.test.ts` · `tests/reset.test.ts`(새) | 표기 · 한국어 이름 · 「대만어로 출력 중」 / 초기화는 멈춤에서만 · 누르면 TTS 버림(남은 조각 버림 · 다음 audio_start 재생) |

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과 |
| `npx vitest run` | 6 파일 · **28 통과**(새 1 · 고침 1) |
| 클래스 대조 | 170 · 없는 것 0 |

## 계약 대조

| DEC | front |
|---|---|
| D-28 개정 — 목록 · 한국어 이름 · 대만을 중국어 하위로 안 씀 | 같음 |
| D-29 — 멈춤에서만 · 원 옆 · 한국어만 · 말풍선 비움 · TTS 버림 · 멈춤 · 언어 유지 · 확인 창 없음 | 같음 |
| D-30 — config → 단추 하나 · demo · 꺼짐/실패면 지금 화면 · 비밀번호 번들 없음 | 같음 — 응답 모양 `{demoLogin}` · demo 응답 = login 과 같은 `{token, expiresAt}` 로 소비(backend 와 합의 모양) |

## 이슈 · 코디가 확인할 것

1. **브라우저 · 화면 확인 못 함** — `:3800` · `:8800` 을 compose(`interpret-pwa-poc-front-1` · `-back-1`)가 계속 쓰고 있어 내 dev 서버를 띄우지 않았다(남은 프로세스 없음 · compose 안 건드림). compose 재빌드 뒤 확인: 드롭다운 7개 표기 · 멈춤 때 「초기화」 위치 · 데모 로그인 단추(`INTERPRET_DEMO_LOGIN=true`) · 꺼짐이면 기존 화면.
2. 「초기화」 위치: 원 상자(92) 오른쪽 12px · 세로 가운데. 오류 상태(#2)와 멈춤 중 출력(#4)에서는 안 보임(`canReset` = #5 만).
3. 데모 모드에서 config 응답이 늦으면 로그인 카드 머리만 잠깐 보인다(입력 칸이 나왔다 사라지는 깜빡임을 피하려고).
4. 시안: designer 가 State-5 · 데모 로그인 시안을 올리면 값 대조 필요(이번엔 시안 없이 medikit 기본 값).
