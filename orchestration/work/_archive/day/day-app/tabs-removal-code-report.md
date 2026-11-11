# day-app mobile — 시술현황 = 필터 + 카드 목록만(SPEC-003 개정 ⑤) (task_ca406aadb692 · ctx_0e43195026fa)

## 상태: done

- 기준: SPEC-003 `06239a1c7d45e95a02e5aab61b9d29bea6b7aca3`(개정 ⑤). 사용자 「응 시술현황은 카드만 보여주면 된느거 아니야?」.
- 코드: `day-app` HEAD `4ee33f95` clean 위. `app/` 만 · 커밋 · push · merge 0 · 하위 위임 0. 서버 · env · 네이티브 · 서명 · 다른 기기 0.

## 변경

| 파일 | 변경 |
|---|---|
| `lib/ui/board_screen.dart` | 상단 「현황 · 호출 n · 시술 완료 n」 탭 · 선택 상태(`_tab`) · 3본문 `IndexedStack` · 호출 탭 목록(`_callsTab` · `_callCard`) · 시술 완료 탭 목록/검색(`_doneTab` · `_doneCard` · 검색 상태/컨트롤러) 삭제 · 쓰지 않게 된 import 1개 정리. 본문 = 연결 줄 + 칩 4개(서버 `inbox.section`) + `cards[]` 카드(폰 한 열 · 아이패드 격자 · 서버 순서) 그대로 |
| `test/ui/app_flow_test.dart` | 옛 탭 기대만 정정: 셸 테스트 = 탭 키 · 「현황/호출 n/시술 완료 n」 글자 없음 + 칩 4개 + 카드 바로 보임 · 보기만 직무 = 호출 탭 대신 카드의 호출 상태 확인(수락 버튼 없음 · 상세 조작 없음 그대로) · 직무별 수락 그룹 = 「호출 탭」 경로 2건(간호사 · 원장 각 1)만 제거, **목록 카드 · 상세 경로의 간호 드로어 대리 · 원장 즉시 수락과 정확 body 테스트는 그대로** |
| `test/capture/visual_capture_test.dart` | 호출 탭 · 시술 완료 탭 캡처 장면 삭제(대체 루트 만들지 않음) · fixture 는 서버처럼 `calls[]` · `doneTab[]` 을 늘 실음(수신만) |

바뀌지 않음: `BoardSnapshot.calls` · `doneTab` · `waitingCallCount` · `homeCount` 모델 · API · SSE · 세션 · 푸시(룸 상세 열기) · KOS 실패 토스트의 doneTab 찾기 · 하단 4메뉴 · DAY/종 · 카드 2줄 상태 박스 · 카드 직접 수락 · 룸 상세(개정 ④) · 마취 · 통역 · README(인박스 탭 서술 없음 — 103행 「탭 이동」은 푸시 탭).

## 검증 (`tabs-removal-evidence/logs/`)

| 명령(cd app · FVM 3.44.8) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **198 passed · 27 skipped(캡처 전용) · 0 failed** — 200 에서 「호출 탭」 경로 수락 2건만 뺌(그 화면이 없음). 세션 race · 푸시 · 환경 · 직무별 수락(카드 · 상세) · 빈 판 · 권한 · 상세 개정 ④ 회귀 그대로 통과 |
| 캡처 | 27 passed → PNG 82 + 시뮬레이터 2 |
| `fvm flutter build ios --no-codesign` | ✓ 17.4MB |
| 표준 `lib/main.dart` 로컬 sim debug 빌드(인자 `logs/simulator-build-args.txt`) | ✓ |
| native 47 | 재실행 안 함(native 변경 0) |

## 스크린샷 (`tabs-removal-evidence/screens/` · fixture 렌더 = 실데이터 아님 · 실글꼴)

- `phone-board-list` · `ipad-board-list` · `phone320-long-list` · `short599/600-long-list`: 머리 바로 아래 칩 4개 → 카드 · 상단 탭 없음 · 4메뉴/레일 그대로.
- 카드 수락(`*-call-wait-list-*`) · 상세 개정 ④(`*-detail-*`) · 상태 박스(`*-status-*`) 장면 재생성.
- `simulator-before-reinstall.png` / `simulator-after-reinstall.png` — 실제 시뮬레이터(로컬 day-local 테스트 데이터 · 이름은 보고서에 옮기지 않음).

## 시뮬레이터

- `orca-mobile-iphone` 5C9E05C7-… 에 `simctl install` 덮어쓰기(uninstall · erase · 로그아웃 · 토큰 삭제 0) → **최종 PID 45830**. 사용자 세션이 복원된 시술현황 화면 — 상단 탭 없이 칩 4개 · 카드. 로그인 입력 · 업무 조작 0.

## 남은 것

- 없음(이번 범위). 코디 독립 리뷰 대기.
