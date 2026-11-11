# 채팅 앱 리뷰 W1 화면 검증 보완 — task_ba1abfcbf8d0 / ctx_6e556e2b7ae2

- 범위: 리뷰 `chat-mobile-review.md` W1(가로 · 긴 글자 · 키보드 열린 화면 증거 없음)만. commit/push/하위위임 0 · 서버/스펙/사용자 시뮬레이터/실계정 0.
- 결과: **새 레이아웃 검증 5개 PASS · PNG 16장 · 실제 overflow 2건 재현 → 제품 코드 최소 수정 2곳**(원형 근거 있음)

## 1. 변경 파일

| 파일 | 변경 | 종류 |
|---|---|---|
| `app/test/capture/chat_capture_test.dart` | `layout()` 그룹 추가(캡처 폴더 없어도 늘 돈다 · 폴더 있으면 PNG) · `boot(extra:)` 로 긴 값 fixture 주입 · `noOverflow`(takeException = null) · `reachable`(hitTestable + 화면/키보드 위 안) | 시험 |
| `app/lib/ui/shell.dart` | 폰: 탭 본문에 `removeViewInsets(removeBottom: true)` 추가 · 아이패드: `resizeToAvoidBottomInset: false` + 본문만 키보드만큼 `Padding`(레일은 전체 높이) | **제품(재현된 overflow)** |
| `app/lib/chat/screens/chat_room_screen.dart` | 1:1 대화 머리의 역할 Badge 를 `Flexible` 로 | **제품(재현된 overflow)** |

## 2. 재현된 overflow 와 근거

1. **키보드 열림 + 여러 줄 입력 — `RenderFlex overflowed by 25 pixels on the bottom`**(`chat_room_screen.dart:225` Column).
   원인: 셸 Scaffold 가 이미 키보드 높이를 뺀 본문에 `viewInsets` 를 그대로 넘겨 대화 화면 Scaffold 가 **한 번 더** 뺐다(가용 높이 ≈ 844−336−336).
   원형 근거: cc-prototype 77173cf8 `lib/screens/shell.dart:139-147` 「키보드 높이는 이 Scaffold 가 이미 뺐으므로 안쪽에 다시 넘기지 않는다(넘기면 대화 화면 Scaffold 가 한 번 더 빼 …)」 → `removeViewInsets(removeBottom: true)` · 아이패드 `:116-133`(resizeToAvoidBottomInset false · 본문만 Padding). **이식 때 빠뜨린 원형 줄을 되살린 것** — 새 디자인 · 문구 0.
2. **긴 직무명 1:1 머리 — `RenderFlex overflowed by 16 pixels on the right`**(`chat_room_screen.dart:195` Row, 폰).
   원인: 원형 머리 Row 는 제목만 `Flexible` · Badge 는 고정 폭 — 원형 다섯 역할(2~3자)이면 맞지만 DAY 직무 이름은 자유 글자(SPEC-004 OQ-C3 · 글자 = `job_role.name`).
   수정: Badge 를 `Flexible` 로(MsBadge 안 글자는 원래 말줄임) — 배치 · 색 · 글자 그대로, 넘칠 때만 줄어듦. 짧은 직무는 전과 같은 화면(기존 캡처 장면 그대로 통과).

## 3. 새 검증(단언) — `fvm flutter test test/capture/chat_capture_test.dart --plain-name "레이아웃"` → **5/5 PASS**

| 시험 | 단언 |
|---|---|
| 폰 가로 844×390 — 목록 · 대화 | overflow 0 · [새 대화] · 채팅 탭 · 입력칸 · [+] · [보내기] · [방 정보] · ‹채팅 누를 수 있고 화면 안 |
| 폰 대화 키보드 열림(viewInsets 336) | overflow 0(여러 줄 6줄 입력 포함) · 탭바 숨김 · 입력칸 · [+] · [보내기]가 **키보드 위** · 말풍선 메뉴(키보드 열림) [공유] · [복사] 누를 수 있음 |
| 긴 직원명(17자) · 긴 그룹 제목 · 긴 직무명(「피부관리 상담 코디네이터 실장」) × 폰 · 폰 가로 · 아이패드 | 목록 행 · 그룹 머리 · 1:1 머리 · 긴 말풍선 · 전달 시트 overflow 0 · [새 대화] · [방 정보] · [보내기] · 전달 [전송] · [닫기] 누를 수 있음 |

수정 전 같은 시험이 위 2건으로 실패(재현) → 수정 후 통과.

## 4. PNG(직접 열어 확인) — `chat-mobile-evidence/layout/`

`land-01-list` · `land-02-chat` · `kb-01-chat-input` · `kb-02-message-menu` · `{phone,land,ipad}-long-01-list` · `-02-group-header` · `-03-direct` · `-04-forward` (16장)
- 위 · 아래 잘림 없음: 머리 · 탭바 · 입력줄 모두 보임. 가로에서 대화 머리 · 입력줄 · 탭바가 한 화면.
- 키보드: 입력줄이 키보드 영역(아래 336pt 빈 칸) 바로 위 · 탭바 숨김 · 6줄 입력은 5줄 높이에서 칸 안 스크롤(원형 규칙) · 말풍선 메뉴는 키보드 위.
- 긴 값: 목록 이름 · 그룹 제목 · 미리보기 말줄임 · 99+ · 직무 Badge 전체(목록) / 머리는 이름 · Badge 둘 다 말줄임 · 가로 · 아이패드는 전체 표시 · 전달 시트 행 전체 표시.

## 5. 회귀 · 빌드(제품 코드 바뀐 부분만 · 로그 `chat-mobile-evidence/logs3/`)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues |
| `fvm flutter test test/ui test/chat test/capture/chat_capture_test.dart` | **120 passed · 20 skipped**(캡처 장면 — 폴더 없음) · 실패 0 — 셸을 쓰는 시술현황 · 룸 상세 · 통역 · 세션 · 채팅 위젯 시험 포함 |
| `fvm flutter build ios --release --no-codesign` | 성공 20.6MB |

전체 `flutter test` 는 브리프대로 다시 돌리지 않았다(바뀐 파일 = 셸 · 대화 화면 Dart 만 → test/ui · test/chat 이 덮음). native 소스 변경 0 → native 재실행 · 시뮬레이터 빌드/설치 안 함(사용자 세션 PID 70352 그대로).

## 6. native PASS 수 차이(54 vs 55) — 원인만

같은 실행 로그 `chat-mobile-evidence/logs2/native-logic.txt` 에서 `grep -c "^PASS "` = **54**(시험 줄) · `grep -c "PASS"` = **55**(마지막 요약 줄 `ALL PASS` 도 셈). 실패 0 · 제품 변경 0. 보고 기준은 시험 줄 54.

## 7. 미결

- 실기기 키보드(높이 · 예측 막대 · 아이패드 하드웨어 키보드 · 분할 키보드)는 위젯 시험의 viewInsets 고정값 대체 — 실기기 pending.
- 아이패드 가로(1366×1024) 장면은 이번 범위(폰 가로) 밖 — 셸 키보드 수정은 원형 아이패드 분기 그대로라 필요하면 같은 그룹에 장면만 더하면 된다.
- 로컬 11040 채팅 API 404(활성화 전제)는 이전 보고 그대로.
