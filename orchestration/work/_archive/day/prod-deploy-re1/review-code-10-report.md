# 리뷰 리포트 — prod-deploy-re1 / code 10 · 앱 카드 테두리 A1 (2026-11-12)

대상: 워크트리 미커밋 `app/` 변경(HEAD `cf8f5037` 위). `app/store/` · `app/tool/store_capture/` 는 범위 밖이라 보지 않았다.
- `app/lib/ui/board_screen.dart`(1줄)
- `app/test/ui/detail_polish_test.dart`(+17줄)

근거:
- e2e-feedback.md A1
- mobile-border-report.md 「정정」 절
- 사용자 「상세 말고 현황탭만」
- spec 워크트리 SPEC-003 개정 ⑪(`spec-003-mobile-app.md:57` · `:196` · `:263` · `:721`)

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `flutter analyze`(app 전체 · fvm 3.44.8) | No issues found |
| `flutter test test/ui/detail_polish_test.dart test/ui/status_box_test.dart test/ui/app_flow_test.dart test/ui/actions_test.dart` | **74 passed** (모두 통과) |

시뮬레이터 · 실기기는 쓰지 않았다(캡처는 앱 세션 몫 · mobile-border-report pending 그대로).

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 현황 탭 카드만 바뀜 | PASS | `git diff -- app` = `board_screen.dart:296` 한 줄(`RoomCard` 바깥 `Border.all(color: c.state == 'doing' ? Ms.primary : Ms.gray200)` → `Ms.gray200`)과 시험 파일 하나뿐이다. 카드 바탕 `Ms.white` · radius · padding 은 그대로다 |
| 방 상세 room_screen 원상 | PASS | `git diff HEAD -- app/lib/ui/room_screen.dart` 가 비어 있다. `room_screen.dart:531-533` 시술 중 행 = `Ms.primary100` 바탕 + `Ms.primary` 테두리 그대로다. 강조 상자(`:295` · `:596`)도 손대지 않았다 |
| 연한 배경 그대로 | PASS | 현황 카드 안 시술 중 상자 `_nowBox` `bg: Ms.primary100`(`board_screen.dart:419` 부근)은 바뀌지 않았다. 방 상세 행 바탕도 그대로다 |
| 확인 필요 상자 띠 그대로 | PASS | `_box`(`board_screen.dart:328-345`)의 `Ms.red100` 바탕 + 왼쪽 `Ms.red` 띠(`_needStripe` 3.0)는 바뀌지 않았다. 기존 시험 `status_box_test.dart:187` · `app_flow_test.dart:157-158` 이 통과한다 |
| 스펙 대조 | PASS | 개정 ⑪ 「시술현황 탭 카드 바깥 테두리는 상태에 따라 색을 바꾸지 않는다 · 방 상세 시술 행은 그대로 · 연한 배경 · 확인 필요 상자는 그대로」와 같다 |
| 시험이 결정을 단언 | PASS(+참고) | 새 시험 「시술 중 현황 탭 카드 = 평소 테두리」가 `state: 'doing'` 카드(`card-v1`)의 바깥 Container 테두리 top 색 = `Ms.gray200` 을 단언한다. 바뀌기 전 코드라면 `Ms.primary` 라 실패한다. 결정의 핵심(현황 탭 카드 띠 없음)은 잡는다 |

## 참고

- 참고 1(시험 공백 — 결정의 다른 절반): 「방 상세는 그대로」를 단언하는 시험이 없다. 정정 때 방 상세 행 단언을 지우면서 「시술 중 행 = primary 테두리 + primary100 바탕」도 함께 사라졌다. 누군가 다시 「띠 다 없애기」로 room_screen 을 바꿔도 시험이 초록이다. 권고: 같은 시험이나 옆 시험에 방 상세 `task-t1` 행 테두리 = `Ms.primary` · 바탕 = `Ms.primary100` 단언 한 줄을 둔다(지운 단언을 값만 바꿔 되살리면 된다).
- 참고 2: 새 시험 끝 `expect(h, isNotNull)` 은 아무것도 확인하지 않는다(무해 · 지워도 된다). 현황 카드 안 시술 중 상자 바탕(`now-doing-v1` = `Ms.primary100`)도 같은 시험에서 단언하면 「연한 배경 그대로」까지 잡힌다.
- 참고 3(스펙 문장): SPEC-003 :336 · :344 의 방 상세 「진행중 = 연한 DAY 배경 · 테두리」는 방 상세 문장이라 이번 결정과 맞다. 옛 문장이 아니다. mobile-border-report 「계약 대조」의 「:334 · :342 옛 문장 · planner 수정 대기」는 정정 뒤로는 해당이 없다.
