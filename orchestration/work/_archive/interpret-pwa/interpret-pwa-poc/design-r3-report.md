# interpret-pwa 시안 r3 결과 보고 — 원 위 외국어 안내 (D-22)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793000713-ef2f`(r2 `1792999779-5fe7`) · 게시 충돌 없음
- 참고: 캔버스 공유 상태가 지금 「링크가 있는 모든 사람」이다(사용자가 바꾼 것으로 보임).

## 바꾼 화면 (10개)

| 화면 | 원 위(고른 언어 · 180°) | 원 아래(한국어 · 그대로) |
|---|---|---|
| `Interpret-Flipped` | ● Please speak(회전 아이콘으로 바로 보기 전환 시 함께 바로) | 말씀하세요 |
| `Interpret-Upright` | ● Please speak(기본 바로 · 아이콘으로 뒤집힘) | 말씀하세요 |
| `Captions` | ● Listening | 영어 듣는 중 |
| `State-2-Error` | [!] Connection error(red-100 상자 그대로 옮김) | 연결이 끊겼어요 + [다시 연결] |
| `State-3-Connecting` | ● Connecting… | 연결 중… |
| `State-4a-Speaking-Foreign` | ● Speaking in English | 영어로 출력 중 |
| `State-4b-Speaking-Korean` | ● Speaking in Korean | 한국어로 출력 중 |
| `State-5-Paused` | ● Paused | 멈춤 · 원을 눌러 다시 듣기 |
| `State-7-Listening-Foreign` | ● Listening | 영어 듣는 중 |
| `State-8-Idle` | ● Please speak | 말씀하세요 |

- 외국어 카드 안(드롭다운 아래)의 안내 줄 + 색 점은 지웠다. 원 위에만 한 번 보인다. 문구·색·글자 스타일은 옮기기 전과 같다.
- 원 줄 높이를 **196px에서 240px**로 늘렸다(위 안내가 들어갈 자리). 두 카드는 각각 22px씩 낮아졌다.

## 바꾸지 않은 것 · 이유
- `State-1-Start`: 화면 전체 오버레이가 이미 위(Tap to start · 뒤집힘)와 아래(탭해서 통역 시작)를 두 언어로 마주 보게 보여 준다. 원 주변에 안내 문구가 없다.
- `State-6-Listening-Korean`: SPEC §7.3 #6의 외국어 영역 안내가 「—」라 원 위에 넣을 문구가 없다(원래도 카드 안에 없었다).
- `Menu` · `Glossary`(브리프 범위 밖): 배경 통역 화면이다. Menu 배경에는 아직 카드 안 「Please speak」 줄이 남아 있다. 맞추려면 한 줄만 고치면 된다(코디 판단).

## 검증
- 캔버스 `project/` 파일 23개와 로컬 `design/project/` 23개의 바이트 수가 모두 같다.
- 새 클래스나 색은 없다(기존 블록을 옮기고 `transform`만 더했다). `design/README.md`에 r3 절을 더했다.

## 코디가 확인할 것
- SPEC §7.2 배치 그림과 §7.3 「외국어 영역 안내」 칸을 「원 위 · 뒤집힘」으로 옮겨 적어야 한다(D-22).

---

## r3 추가 (코디 요청) — 버전 `1793000774-ad1c`

| 화면 | 바꾼 것 |
|---|---|
| `State-6-Listening-Korean` | 원 위에 고른 언어 안내 추가(180°): **primary 색 점** + 「Listening to Korean…」. 원 줄 196px → 240px(다른 상태와 같음) |
| `Menu` | 배경 통역 화면의 카드 안 「Please speak」 줄을 원 위(180°)로 옮김 · 원 줄 240px |

#6 외국어 안내 문구(상대가 기다리는 뜻 · front 상수 표에 넣을 값 제안):

| lang | 문구 |
|---|---|
| en | Listening to Korean… |
| ja | 韓国語を聞いています… |
| zh | 正在听韩语… |
| th | กำลังฟังภาษาเกาหลี… |
| vi | Đang nghe tiếng Hàn… |
| yue | 正在聽韓語… |

- 이로써 D-22가 상태 #2–#8 전부 · 배치 2 · 자막 · 메뉴에 들어갔다. #1(시작 전)은 오버레이 자체가 위아래 두 언어라 그대로 두었다.
- SPEC §7.3 #6 「외국어 영역 안내」 칸을 「—」에서 위 문구로 바꿔야 한다(OQ-006 문구 표에 #6이 추가됨 · 6개 언어 × 7칸에서 8칸으로).
- 검증: 캔버스 `Menu.dc.html` 6440B · `State-6-Listening-Korean.dc.html` 5163B가 로컬과 같다. 나머지 21개 파일은 r3 그대로.
