# prod-deploy-re1 A1 — 앱 카드 테두리(파란 띠) 없애기 결과 보고

## 상태: done (캡처만 pending)

## 수행 — 바꾼 파일:줄
| 파일:줄 | 전 | 후 |
|---|---|---|
| `app/lib/ui/board_screen.dart:296` 시술현황 탭 카드 | `Border.all(color: c.state == 'doing' ? Ms.primary : Ms.gray200)` | `Border.all(color: Ms.gray200)` |
| `app/lib/ui/room_screen.dart:533` 방 상세 시술 행 | `Border.all(color: doing ? Ms.primary : Ms.gray200)` | `Border.all(color: Ms.gray200)` |
| `app/test/ui/detail_polish_test.dart` (끝에 1개 추가 · theme import) | — | 「시술 중 카드 · 시술 행 = 평소 테두리」: 카드 · 행 top 색 = `Ms.gray200`, 행 배경 = `Ms.primary100` 유지 |

그대로 둔 것: 시술 중 행의 연한 DAY 배경(`room_screen.dart:531` `Ms.primary100`) · 「확인 필요」 상자 옅은 빨강 바탕 + 왼쪽 빨간 띠(`board_screen.dart:347`) · 문구 변경 없음.

## grep 표 — `app/lib` 의 `Border.all(` · `BorderSide(` · `border:` 중 상태로 색이 바뀌는 것
(고정 색 테두리 · 구분선(`Border(top/bottom/left/right: …gray200)`) · 입력칸(`OutlineInputBorder`) · `InputBorder.none` 은 상태 무관이라 표에서 뺐다.)

| 위치 | 무엇 | 조건 | 판단 | 처리 |
|---|---|---|---|---|
| `ui/board_screen.dart:296` | 시술현황 카드 바깥 테두리 | `doing` → primary | 대상 | **바꿈** |
| `ui/room_screen.dart:533` | 방 상세 시술 행 테두리 | `doing` → primary | 대상 | **바꿈** |
| `ui/board_screen.dart:240` | 필터 칩 | selected · alert | 칩 | 그대로 |
| `ui/board_screen.dart:249` | 칩 안 점 링 | ring | 칩 | 그대로 |
| `ui/board_screen.dart:347` | 확인 필요 상자 왼쪽 빨간 띠 | needs | 3차 B안 · 사용자 언급 없음 | 그대로 |
| `ui/room_screen.dart:295` (`Boxed border: fg`) | 방 상세 호출 강조 상자 테두리 | 호출 종류/지연 → red · primary | **애매** — 카드 · 행이 아니라 강조 상자. 상태별 색 테두리이긴 함 | 그대로(코디 판단 필요) |
| `ui/room_screen.dart:596` (`Boxed border: Ms.primary`) | 방 상세 「시술 모두 완료」 강조 상자 | 상자 자체가 완료 시에만 뜸(고정 primary) | **애매** — 파란 테두리지만 상태로 색을 바꾸는 줄은 아님 | 그대로(코디 판단 필요) |
| `ui/widgets.dart:61` | 배지/버튼 outline | outline | 버튼 | 그대로 |
| `ui/widgets.dart:250` | 작은 상자(인자 border) | 호출측 | 공용 위젯 | 그대로 |
| `ui/interpret_widgets.dart:66` · `:320` | 통역 언어 선택 칩 | on | 칩 | 그대로 |
| `ui/interpret_widgets.dart:431` | 통역 마이크 버튼 링 | listening · paused | 버튼 | 그대로 |
| `ui/doctor_picker.dart:315` · `:416` · `:478` | 의사 선택 항목 · 라디오 · 체크 | on | 선택 컨트롤 | 그대로 |
| `chat/chat_kit.dart:176` | 체크박스 | value · enabled | 컨트롤 · allowed_paths 밖 | 그대로 |
| `chat/chat_kit.dart:204` | 채팅 선택 카드 | selected → primary | **애매** — 선택 표시. allowed_paths(`app/lib/ui/`) 밖 | 그대로 |
| `chat/chat_kit.dart:372` | 상태 점 링 | dotRing | 점 | 그대로 |
| `chat/screens/chat_attach_sheet.dart:253` | 첨부 사진 선택 테두리 | on | 선택 표시 · 범위 밖 | 그대로 |
| `chat/screens/chat_forward_sheet.dart:338` | 전달 대상 라디오 | on | 컨트롤 · 범위 밖 | 그대로 |
| `chat/screens/chat_room_screen.dart:354` | 말풍선 | mine → 없음 | 말풍선(상태 색 아님) | 그대로 |

## 검증
- `flutter analyze lib/ui/board_screen.dart lib/ui/room_screen.dart test/ui/detail_polish_test.dart` → **No issues found**
- `flutter test test/ui/detail_polish_test.dart test/ui/status_box_test.dart test/ui/app_flow_test.dart test/ui/actions_test.dart` → **74 passed, 0 failed** (새 시험 1개 포함)
- flutter = `/Users/kknaks/fvm/versions/3.44.8/bin/flutter` (PATH 에 없음)
- 전/후 캡처: **pending** — 역할 rules 「시뮬레이터를 건드리지 않는다」 · 앱 세션 몫.

## 계약 대조
- 사용자 A1 「띠는 다 없애자」 = 같음. 스펙 :194 · :334 · :342(「연한 DAY 배경 · 테두리」)는 아직 옛 문장 — planner 수정 대기. :261 · :719 「카드 테두리 평소 그대로」와 같음.

## 이슈 · 코디가 확인할 것
1. 애매 2곳: 방 상세 호출 강조 상자(`room_screen.dart:295`, red/primary 테두리) · 「시술 모두 완료」 상자(`:596`, primary 테두리) — 사용자 「파란 띠 다」에 들어가는지 결정 필요.
2. `chat/chat_kit.dart:204` 선택 카드 primary 테두리 — 범위 밖 · 선택 표시라 둠.
3. 커밋 안 함. `app/store/` · `app/tool/store_capture/` 건드리지 않음.

## 정정 (2026-11-12 · 코디 — 사용자 「상세 말고 현황탭만 고치라고 했다」)
- 범위 = 시술현황 탭 카드 `board_screen.dart:296` 하나뿐. 이 변경은 그대로 둔다.
- `room_screen.dart:533`(방 상세 시술 행) → **원래대로 되돌림**(`git checkout`). 시술 중 행은 다시 primary 테두리.
- `detail_polish_test.dart` 추가 시험에서 방 상세 행 단언(openCard · task-t1 테두리 · 배경)을 지움. 현황 탭 카드 테두리 단언만 남김(시험 이름: 「시술 중 현황 탭 카드 = 평소 테두리(DAY 주색 띠 없음)」).
- 강조 상자 ① `room_screen.dart:295` · ② `:596` — 손대지 않음(결정 끝). 위 「이슈」 1번은 끝난 일.
- 지금 diff: `app/lib/ui/board_screen.dart` (1줄) · `app/test/ui/detail_polish_test.dart` (+17줄). room_screen 변경 없음.
- 검증: `flutter analyze lib/ui/board_screen.dart test/ui/detail_polish_test.dart` → No issues found · `flutter test` detail_polish · status_box · app_flow · actions → **74 passed, 0 failed**.
