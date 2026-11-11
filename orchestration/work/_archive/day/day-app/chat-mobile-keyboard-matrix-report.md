# 키보드 시험 2장면 추가 — task_2e352bf68dc1 / ctx_eb35fe0fa1e6

- 범위: `chat-mobile-layout-rereview.md` W1 — 아이패드 · 폰 가로 키보드 열림 대화 2장면만. **제품 코드 변경 0 · 새 UI 문구 0** · commit/push/하위위임 0 · 전체 시험 · native · 빌드 · 사용자 시뮬레이터 · 서버 · DB 0.
- 결과: **두 장면 PASS · 제품 결함 재현 없음**(질문 필요 없음).

## 변경 파일

| 파일 | sha256 |
|---|---|
| `app/test/capture/chat_capture_test.dart` | `4d9b6a8ae79b9561dc4e575cef7be31d4b69bf352683d849becf9d06fb520661` |

`layout()` 그룹(레이아웃 W1)에 장면 2개 추가:
- `ipad 대화 · 키보드 열림(viewInsets 400)` — 1024×1366 · 아이패드 오른쪽 칸 대화
- `land 대화 · 키보드 열림(viewInsets 200)` — 844×390 · 폰 대화

각 장면: 입력칸 누름 → `viewInsets` 설정 → `noOverflow` → 3줄 입력 → `noOverflow` → 입력칸 · [+] · [보내기] `reachable`(hitTestable + 화면 안 + **아래 끝 ≤ 화면 높이 − 키보드**) → PNG.

제품 코드 변경 0 증거: 브리프 파일보다 새로 바뀐 파일 = `app/test/capture/chat_capture_test.dart` 하나(`find app/lib app/ios/Runner -newer <brief>` 결과 없음). 작업트리의 `app/lib` diff 는 이전 태스크(미커밋) 그대로.

## 실행

`DAY_CAPTURE_DIR=<evidence>/keyboard-matrix fvm flutter test test/capture/chat_capture_test.dart --plain-name "레이아웃"` → **7/7 PASS**(기존 레이아웃 5 + 새 2). 로그 `chat-mobile-evidence/keyboard-matrix/test-layout.txt`.

## PNG(직접 열어 확인) — `chat-mobile-evidence/keyboard-matrix/`

| 파일 | sha256 앞 16자 | 확인 |
|---|---|---|
| `kb-ipad-400-chat.png` | `b39bc55dd1069dbb` | 레일 전체 높이 그대로 · 목록 칸 · 대화 칸이 키보드(아래 400pt) 위에서 끝남 · 3줄 입력줄 · [+] · [보내기] 잘림 0 · 머리 그대로 |
| `kb-land-200-chat.png` | `1daebc2be5990ab5` | 머리 · 마지막 말풍선 · 3줄 입력줄 · [+] · [보내기]가 키보드(아래 200pt) 위 · 탭바 숨김 · 잘림 0 |

(같은 폴더의 나머지 16장은 같은 그룹 실행으로 다시 만든 기존 레이아웃 장면.)

## 미결

- 실기기 키보드(실제 높이 · 예측 막대 · 하드웨어/분할 키보드)는 위젯 시험의 고정 viewInsets 대체 — pending(이전과 같음).
