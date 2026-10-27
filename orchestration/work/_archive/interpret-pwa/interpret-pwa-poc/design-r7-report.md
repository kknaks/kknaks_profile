# interpret-pwa 시안 r7 결과 보고 — 듣기 방식 전환 · 누르고 말하기 (D-36)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793067971-7854`(전 `1793065090-39a3`) · 게시 충돌 없음
- 워크트리 main `145c872` 기준. 게시 전 로컬 `design/`이 캔버스와 같은 것을 확인했다(바이트 수).
- 아트보드 19 → 22개. 새 줄 「6 · 듣기 방식 · 누르고 말하기 (D-36)」(y=4800).

## 새 화면 3개

| 화면 | 세그먼트 | 원 | 원 위(고른 언어 · 180°) | 원 아래(한국어) |
|---|---|---|---|---|
| `Mode-Auto-Idle`(6-1) | **자동 듣기** 선택 | 대기 그대로(64px · gray-400 · 마이크 · 링) | ● Please speak(purple) | 말씀하세요 |
| `PTT-Ready`(6-2) | **누르고 말하기** 선택 | 64px **흰 원 + 2px `border-ms-gray-500`** + 마이크(gray-700) — 「눌러야 듣는다」를 대기(회색으로 채운 원)와 구분 | ● Hold to speak(gray-600) | 누르고 말하세요 |
| `PTT-Pressed`(6-3) | **누르고 말하기** 선택 | 듣는 중 그대로 — 화자 색 · 88px(음량 예) · 링 7px. 예는 한국어(primary) | ● Listening to Korean…(primary) | 한국어 듣는 중 |

### 모드 전환(세그먼트)
- 위치는 원 **왼쪽**(원 줄을 3칸 grid `1fr 92px 1fr`로 · 원은 가운데 그대로). 초기화(#5 · D-29)는 원 **오른쪽**이라 같은 화면에 함께 있어도 겹치지 않는다.
- 세로 두 칸 · 폭 104px · 칸 높이 28px · 바탕 `bg-ms-gray-200` 모서리 8px · 고른 칸 `bg-ms-white text-ms-gray-800 caption-md-600` + 그림자 `0 1px 3px rgba(0,0,0,.08)` · 안 고른 칸 `text-ms-gray-700 caption-md-500`. `role="radiogroup"`/`radio`. 한국어만 · 회전 없음.
- 주의: 「작은 세그먼트」 요청대로 칸 높이 28px이다. 터치 권장 44px보다 작다. 상담사가 가끔 쓰는 설정이라 작게 두었다. 실기기에서 누르기 어려우면 32~36px로 올린다.

### 「Hold to speak」 류 7개 언어 제안(front 상수용 · 원 위 안내)

| lang | 안 누름(Hold to speak) |
|---|---|
| en | Hold to speak |
| ja | 押しながら話してください |
| zh | 按住说话 |
| zh-Hant | 按住說話 |
| th | กดค้างไว้แล้วพูด |
| vi | Nhấn giữ để nói |
| yue | 㩒住講嘢 (문어로 맞추려면 按住說話) |

- 누름 상태의 원 위 문구는 지금의 듣는 중 문구 그대로다(#6 Listening to Korean… · #7 Listening).

## 검증
- 캔버스와 로컬의 바이트 수가 같다: `canvas.json` 5413 · `Mode-Auto-Idle` 6184 · `PTT-Ready` 6223 · `PTT-Pressed` 6218. 나머지 파일은 전 버전 그대로.
- 쓴 클래스(`border-ms-gray-500` · `bg-ms-gray-200` · `caption-md-500/600` 등)는 모두 medikit 번들에 있다. 새 hex는 없다(세그먼트 그림자 rgba 하나).
- 커밋 안 함.

## 코디 · frontend가 볼 것
- SPEC §7.3에 모드 두 개를 더해야 한다: 누르고 말하기의 「안 누름」 상태(문구 · 원 모양)와 「누름 = 듣는 중」. TTS 재생 중 누르면 재생 멈춤 · 큐 비움 · 듣기. 멈춤 #5 · 초기화는 그대로.
- 누르고 말하기 모드의 #5(멈춤)는 사실상 「안 누름」과 겹친다. 두 모드에서 #5를 어떻게 보일지(그대로 둘지) frontend 판단이 필요하다. 시안은 따로 그리지 않았다.
- **r7 처분(코디 · 버전 `1793068035-f0d6`)**: 세그먼트 칸 터치 높이 28px → 44px(보이는 높이도 44 · 바탕 패딩 2px · 칸 사이 0 → 92px로 원 칸과 같음 · 6-1/6-2/6-3 모두). `PTT-Ready`에 원 오른쪽 「초기화」(State-5와 같은 outlined gray s 단추 · 세그먼트는 왼쪽이라 겹치지 않음)를 넣음. 바이트: Mode-Auto-Idle 6182 · PTT-Ready 6886 · PTT-Pressed 6216(캔버스=로컬).
