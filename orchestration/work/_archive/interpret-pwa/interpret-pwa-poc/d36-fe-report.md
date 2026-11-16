# D-36 — frontend 결과 보고 (「누르고 말하기」 모드 · 시안 r7)

## 상태: done (iPhone 실기기 길게 누름 · 실 back 실발화는 pending)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(main 145c872 위 · 커밋 없음). 범위 `front/**` 만 · back 무변경(WS 메시지 그대로).

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `front/components/interpret/ModeToggle.tsx`(새) | 원 왼쪽 세로 세그먼트 「자동 듣기 / 누르고 말하기」(시안 r7 — 트랙 `bg-ms-gray-200` 104 · 둥글기 8 · 안쪽 2 / 칸 **h44**(코디 처분 ① 누르는 영역 44) · 고른 칸 `bg-ms-white text-ms-gray-800 caption-md-600` + 옅은 그림자 · 안 고른 칸 투명 `text-ms-gray-700 caption-md-500`) · `role=radiogroup/radio` · 가운데 줄이라 회전 없음 |
| `front/components/interpret/Circle.tsx` | `hold` 가 있으면 클릭 대신 누르고 있는 동안: `pointerdown`(+ pointer capture) = 시작 · `pointerup` · `pointercancel` · `lostpointercapture` · `pointerleave` = 끝 · 키보드 Space/Enter 누름/뗌 · `contextmenu` 막음 · iOS 길게 누름 대비 `touch-none select-none [-webkit-touch-callout:none] [-webkit-user-select:none]` · aria-label 「누르고 있는 동안 말하기」. **안 누름 모양**(시안 PTT-Ready) = 64 흰 원 + 2px `border-ms-gray-500` + 마이크 22 |
| `front/components/interpret/InterpretScreen.tsx` | 모드 상태 · 기억 · `ready` 뒤 누르고 말하기면 바로 `pause` · 누름 = `pressDown`(재생 구간이면 `clearPlayback` → `resume`) · 뗌 = `pressUp`(`pause` → back finalize) · 모드 바꿈(자동 → 누르고 말하기 = `pause` · 반대 = `resume`) · 「초기화」 = 원 오른쪽 · 시안 r7 모양(흰 · `border-ms-gray-300` · h33 · 둥글기 6 · `text-typo-body-500` · 다시 아이콘) — 멈춤 #5 와 누르고 말하기 안 누름에서 보임(처분 ②) · 원 위 안내 점 = gray-600 |
| `front/lib/view.ts` | `CircleInput.ptt` · `holding` · 상태 `holdToTalk`(판정: 시작 전 > 오류 > 연결 중 > 출력 중 > **누르고 말하기 안 누름** > 멈춤 > 듣는 중 > 대기) · `canReset` 에 `holdToTalk` |
| `front/lib/ptt.ts`(새) | `pressDown(session, outputting)` · `pressUp(session)` |
| `front/lib/prefs.ts` | `readMode` · `writeMode`(`interpret.mode` · 처음 `auto`) |
| `front/lib/interpret.ts` | `get outputting`(반이중 게이트 기준 — 표시보다 먼저 참) |
| `front/lib/langs.ts` · `lib/phrases.ts` | 원 아래 「누르고 말하세요」 · 원 위 `holdToTalk` 7개 언어(r7 리포트 표: Hold to speak · 押しながら話してください · 按住说话 · 按住說話 · กดค้างไว้แล้วพูด · Nhấn giữ để nói · 㩒住講嘢) |
| `front/components/icons.tsx` | `ResetIcon`(시안 r7) |
| `front/lib/demo.ts` | 개발 가짜 렌더 `ptt` · `ptt-hold` |
| `front/tests/ptt.test.ts`(새) | 누름/뗌 → resume/pause · TTS 중 누름 → clear 뒤 resume · 상태 판정(안 누름 · 누름 = 듣는 중 · 출력 중이 위 · 자동은 그대로) · 초기화 보임 · 문구 · 모드 기억(localStorage) |

- 누름 상태 = 지금의 듣는 중 그대로(음량 반응 64 → 88 · 화자 색 · 캡션 오기 전은 대기 모양). 자동 듣기 모드 · 멈춤 #5 · 초기화 · 자동 스크롤은 그대로.
- medikit `Button` 의 `leftIcon` 은 크기 토큰(`'sm'`)을 아이콘 props 로 넣어 우리 SVG 의 `width` 를 깨뜨린다 → `<span>` 로 감쌌다(초기화 · 다시 연결 — 다시 연결 아이콘도 그동안 안 보였을 수 있다).

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과 |
| `npx vitest run` | 9 파일 · **36 통과**(새 4) |
| 클래스 대조 | 209 · 없는 것 0 |

스크린샷 `d36-fe-shots/`(390 × 844 · 운영 빌드 · 실제 흐름: 오버레이 English → 가짜 WS `ready` → 모드 바꿈 → 원 누름):

| 파일 | 시안 | 확인값 |
|---|---|---|
| `D36-1-mode-auto-idle.png` | Mode-Auto-Idle | 「말씀하세요」 · 원 64 gray-400 · 세그먼트 「자동 듣기 ✓」 h44 · 보낸 것 `start:en` |
| `D36-2-ptt-ready.png` | PTT-Ready | 「누르고 말하세요」 · 원 위 「Hold to speak」(gray-600 점 · 뒤집힘) · 흰 원 2px 테두리 · 「초기화」 보임 · 보낸 것 `+ pause` · `localStorage interpret.mode = ptt` · 원 `touch-action:none` · `user-select:none` |
| `D36-3-ptt-pressed.png` | PTT-Pressed | 누름 → `resume` · 캡션 `side=me` → 「한국어 듣는 중」 primary · 원 위 「Listening to Korean…」 · 초기화 숨김. 뗌 → `pause` · 다시 「누르고 말하세요」 |

- 방법: `:3800` · `:8800` 을 compose 가 쓰고 있어 포트 없이 운영 빌드를 request interception 으로 내줌 · 서비스 워커 우회 · WS 는 페이지 안 가짜(메시지 주입) · compose 안 건드림.

## 이슈 · 코디가 확인할 것

1. **iPhone 실기기**: 길게 누를 때 텍스트 선택 · 확대 · 콘텍스트 메뉴가 안 뜨는지 · 손가락이 원 밖으로 미끄러질 때(pointer capture 로 뗄 때까지 유지 — `pointerleave` 는 캡처 중엔 안 옴) · 누름 → 소리 · 뗌 → 번역 TTS. 재빌드 · 배포 뒤.
2. 누르고 말하기 모드의 「누름」 중 TTS 가 오면(다른 사람이 아직 누르고 있을 때) 반이중 그대로 송신 막힘 — 시안 · DEC 에 따로 없음.
3. 「초기화」 모양을 시안 r7(흰 · 회색 테두리 · 다시 아이콘)로 바꿔서 멈춤 #5 의 초기화도 같은 모양이 됐다(State-5 시안과 같은 값).
4. SPEC §7.3 에 「누르고 말하기 안 누름」 상태 · 모드 전환 추가 필요(코디 → planner · r7 리포트도 같은 말).
