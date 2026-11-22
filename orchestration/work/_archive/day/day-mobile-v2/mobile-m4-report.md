# day-mobile-v2 M4 결과 보고 — 통역 화면 글자 대조(통키 `56e43a0`)

## 상태: done — 코드 글자 변경 0건(「바꿈」 행 없음) · 결정 필요 1줄(원천 없음 · 지움 제안)

base = `841454c4`. 바꾼 파일 = 캡처 테스트 하나(`app/test/capture/m4_capture_test.dart` 새로). 앱 코드 · 글자 무수정.

원천: 통키 `interpret-pwa` `56e43a0` `front/lib/phrases.ts` · `front/components/interpret/Circle.tsx` · `InterpretScreen.tsx` · `front/lib/interpret.ts` · 통키 SPEC-001 §7.3 상태 표. 통키 0.9.5(세 참여자)는 「화면 문구 그대로」(SPEC-001 변경 이력 0.9.5 · §1)라 **반이중 걷음 뒤 새로 생긴 화면 글자가 없다** — 통키 출력 중 상태의 원 아래 글자는 「〈언어〉로 출력 중」 하나뿐이고 듣기 여부 안내 줄은 없다.

## 표 — 통역 화면 글자 전부

경로 접두어: `app/lib/`. 「0.2.0 맞나」 = 반이중 걷음 · 재생 중에도 들음 · 끼어들기 · 차례 끝 1초 · 멈춤 동작 기준.

| # | 지금 글자 | 파일:줄 | 0.2.0 동작과 맞나 | 통키 같은 뜻 글자 | 통키 파일:줄 | 처분 |
|---|---|---|---|---|---|---|
| 1 | **「번역 음성이 나오는 동안은 듣지 않아요」**(재생 중 안내 줄) | `ui/interpret_widgets.dart:409` | **아니다** — 이제 재생 중에도 듣고 끼어들면 멈춘다 | 없음(통키 출력 중 = 원 아래 「〈언어〉로 출력 중」만 · 듣기 안내 줄 없음) | `front/lib/phrases.ts:15` · SPEC-001 §7.3 #4 | **원천 없음 · 지움 제안**(안내 줄만 비우고 상태 「번역 읽는 중」은 둠 — 사용자 결정 대기) |
| 2 | 「번역 읽는 중」(재생 중 상태) | `ui/interpret_widgets.dart:409` | 맞다(재생 중) | 「〈언어〉로 출력 중」 / 「한국어로 출력 중」 — 같은 상태 · 다른 글자 · 출력 언어(side)를 앎 | `front/lib/phrases.ts:15` | 그대로(앱은 재생 발화의 side 를 화면에 넘기지 않아 그 글자를 그대로 못 씀 — 바꾸려면 기능 추가 · 원천은 있음) |
| 3 | 「듣는 중」 · 「양쪽 말을 모두 들어요 · 누가 말했는지 자동으로 구분해요 · 누르면 멈춤」 | `ui/interpret_widgets.dart:411` | 맞다 | 「한국어 듣는 중」 / 「〈언어〉 듣는 중」 · 「말씀하세요」 | `front/lib/phrases.ts:19-23` | 그대로 |
| 4 | 「멈춤」 · 「누르면 다시 들어요 · 시술 중 잠깐 끌 때」 | `ui/interpret_widgets.dart:412` | 맞다(멈춤 중에도 확정된 번역은 읽음 — 그때는 #2 가 보임) | 「멈춤 · 원을 눌러 다시 듣기」 | `front/lib/phrases.ts:17` · `Circle.tsx:71` | 그대로 |
| 5 | 「연결 안 됨」 · 「[다시 연결]을 눌러 주세요」 | `ui/interpret_widgets.dart:413` | 맞다 | (오류 원 아래 = 서버 문구 + [다시 연결]) | `phrases.ts:11` · `InterpretScreen.tsx:357` | 그대로 |
| 6 | 「연결 중」 · 「마이크와 통역 서버를 연결하고 있어요」 | `ui/interpret_widgets.dart:414` | 맞다 | 「연결 중…」 · 「연결 중」 | `phrases.ts:13` · `Circle.tsx:73` | 그대로 |
| 7 | 「다시 연결」(버튼) | `ui/interpret_widgets.dart:402` | 맞다 | 「다시 연결」 | `InterpretScreen.tsx:357` | 그대로 |
| 8 | 「통역을 준비하고 있어요」 / 「말씀하시면 자막이 나와요」(빈 자막 영역) | `ui/interpret_widgets.dart:338` | 맞다 | 「연결 중…」 / 「말씀하세요」 | `phrases.ts:13 · :23` | 그대로 |
| 9 | 「한국어는 {언어}로, {언어}는 한국어로 옮겨요」 | `ui/interpret_widgets.dart:341` | 맞다 | 없음(통키는 화면 두 영역) | — | 그대로 |
| 10 | 「의료진」 / 「{고객} 님」(말풍선 이름) | `ui/interpret_widgets.dart:361` | 맞다 | 없음(통키는 영역으로 구분) | — | 그대로 |
| 11 | 「번역 중…」(번역 전 말풍선) | `ui/interpret_widgets.dart:383` | 맞다 | 없음(통키는 빈 번역 줄을 안 만듦 · `view.ts:43`) | — | 그대로 |
| 12 | 「통역 · 」 + 언어(드로어 머리) | `ui/interpret_widgets.dart:267` | 맞다 | — | — | 그대로 |
| 13 | 「통역 종료」(아이패드) / 「종료」(폰) | `ui/interpret_widgets.dart:293` | 맞다 | — | — | 그대로 |
| 14 | 「빠른 말하기 · {언어}」 / 아이패드 「통역 · {언어}」(통역 바) | `ui/interpret_widgets.dart:106` | 맞다 | 없음(통키에 통역 바 없음 · 프로토 글자) | — | 그대로 |
| 15 | 「통역하기」(통역 바 버튼) | `ui/interpret_widgets.dart:112` | 맞다 | 없음 | — | 그대로 |
| 16 | 「이 기기에 {언어} 음성이 없어요」(빠른 말하기 토스트) | `ui/interpret_widgets.dart:31` | 맞다(빠른 말하기 = 기기 TTS · 통역 서버와 무관) | 없음 | — | 그대로 |
| 17 | 빠른 말하기 문장 6개(「조금 뜨거울 수 있어요」 …) · 언어 이름 | `interpret/langs.dart:15-22 · :56-76` | 맞다 | — | — | 그대로 |
| 18 | 「통역 서버에 연결할 수 없어요」 | `interpret/interpret_client.dart:131` | 맞다 | 「통역 서버에 연결하지 못했어요.」(같은 뜻 · 끝말 다름) | `front/lib/interpret.ts:138` | 그대로(동작과 어긋나지 않음) |
| 19 | 「통역 서버와 연결이 끊겼어요」 | `interpret/interpret_client.dart:132` | 맞다 | 「통역 서버와 연결이 끊겼어요.」 | `front/lib/interpret.ts:150` | 그대로 |
| 20 | 「통역 서버가 로그인을 받지 않았어요 — 다시 로그인해 주세요」 | `interpret/interpret_client.dart:133` | 맞다 | 없음(통키 로그인 다름) | — | 그대로 |
| 21 | 「마이크를 쓸 수 없어요 — 설정 → {앱} → 마이크를 켜 주세요」 | `state/interpret_controller.dart:146` | 맞다 | (브라우저 문구 — 앱과 다른 갈래) | `front/lib/interpret.ts:103` | 그대로 |
| 22 | 「마이크 소리를 받지 못했어요」 | `state/interpret_controller.dart:202` | 맞다 | 「이 브라우저에서 마이크 소리를 처리하지 못했어요.」 | `front/lib/interpret.ts:127` | 그대로 |
| 23 | 「마지막 통역 HH:MM · N문장」(닫은 뒤 요약) | `state/interpret_controller.dart:227` | 맞다(빈 final 지우기로 지워진 말풍선은 셈에서 빠짐 — P5) | 없음 | — | 그대로 |
| — | **대리 수락 창(U-6) 「호출할 시술 · N개」** | `ui/doctor_picker.dart:433`(`_chosenSection` · 대리 수락은 `ui/accept.dart:44` `procs` 로 채움) | — | — | — | **바꾸지 않음 — 위치만**(사용자 글자 대기 · 웹 수락 창 single 엔 이 칸 없음) |

## 「바꿈」 반영
- 없음. 0.2.0 과 어긋나는 글자는 #1 하나인데 통키에 같은 뜻 글자가 없어 바꾸지 않았다(브리프 「원천 없음 → 바꾸지 말고」).

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+412 ~81 All tests passed**(~81 = 캡처 · 평소 skip · 새 캡처 2 포함) |
| `fvm flutter build ios --no-codesign` | ✓ Built `Runner.app` (20.8MB) |
| 캡처 `DAY_CAPTURE_DIR=… flutter test test/capture/m4_capture_test.dart` | 2/2 · 6장(그림자 켬) |

## 캡처 (`shots/`)
`m4-{phone,ipad}-drawer-listening.png`(「듣는 중」) · `m4-{phone,ipad}-drawer-playing.png`(「번역 읽는 중」 + #1 안내 줄) · `m4-{phone,ipad}-drawer-paused.png`(「멈춤」). 목 WS(테스트 더블) · 실제 서버 · 마이크 무접촉. 번체 자막의 「燙」 이 네모로 찍힌 것은 캡처 글꼴(Apple SD Gothic Neo) 탓 — 앱 문제 아님.

## 코디가 사용자에게 물을 것
1. **#1 「번역 음성이 나오는 동안은 듣지 않아요」** — 0.2.0 과 틀린 말. 선택: ⓐ 안내 줄 비움(제안 · 상태 「번역 읽는 중」만) ⓑ 사용자가 새 글자를 정함 ⓒ 그대로.
2. (선택) #2 「번역 읽는 중」 → 통키 「〈언어〉로 출력 중」 / 「한국어로 출력 중」 으로 맞출지 — 원천은 있으나 재생 발화의 언어를 화면까지 넘기는 기능이 필요(이번 범위 「기능 그대로」 밖).
3. 대리 수락 창 「호출할 시술 · N개」(`ui/doctor_picker.dart:433`) 글자.
