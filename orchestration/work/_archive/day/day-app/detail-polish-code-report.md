# day-app mobile — 룸 상세 다듬기(SPEC-003 개정 ④) (task_46339b4a4e49 · ctx_67ea976cd328)

## 상태: done

- 기준: SPEC-003 `4a5d4a4705b07fd66272867d85115376b1289400`(개정 ④). 사용자 「ㅇ으 그렇게 해서 이거까지 발주하자」.
- 코드: `day-app` HEAD `47be2cb0` clean 위. `app/` 만 · 커밋 · push · merge 0 · 하위 위임 0. 서버 · env · 네이티브 · 서명 · 다른 기기 0.

## 변경

| 파일 | 변경 |
|---|---|
| `lib/ui/widgets.dart` `DetailHeader` | `centerTitle` 옵션 추가(기본 false = 이전 동작 그대로). 켜면 `CustomMultiChildLayout` 으로 뒤로 버튼을 왼쪽에 놓고, 제목은 양쪽에 (뒤로 버튼 폭 + 8) 을 비운 폭 안에서 **머리 전체 폭 정가운데** · 말줄임. DetailHeader 사용처는 룸 상세 하나뿐 |
| `lib/ui/room_screen.dart` | (A) 룸 머리 `centerTitle: true`. (B) 호출 강조 상자 = `oc.waiting`(called 줄이 남은 호출)만 · 전부 수락된 호출 상자 숨김. (C) `_taskCard` 5상태 — 1줄 시술명 좌 · 시간 우(진행중 큰 `elapsedMmss` · 완료 「완료 {spanMin}」 / 시각 없으면 「완료」) · 2줄 담당의(없거나 빈 값 = 「담당의 미정」 · 진행중 「· HH:MM 시작」) 좌 + 조작 우: 준비중 · 호출 중 · 수락 뒤 [시작](서버 `canStart` · 요청 중 · board edit — 호출 중은 서버 false 로 회색) / 진행중 [종료] [⋮] / 완료 [⋮]. 상태 Pill 배지 · 행 [수락] · 호출 대상 · 호출 경과 글자 제거. ⋮ = 기존 `canUndoStart` · `canUndoFinish` + board edit · 확인 창 · API · 문구 그대로 |
| `test/ui/detail_polish_test.dart`(신규 10) | 전부 수락 상자 숨김 · 부분 수락/복수 호출 중 미수락만 상자(상단 수락 유지) · 호출 중 행 [수락] 없음 · 회색 [시작] 눌러도 요청 0 · 배지 글자 없음 · 준비중 서버 canStart true → [시작] 켜짐 · POST start · 조작이 둘째 줄 안(제목 줄 아래 · [종료] 다음 ⋮) · 진행중 「담당의 · HH:MM 시작」 · 큰 mm:ss · 「완료 8분」 · 시각 없으면 「완료」 · 보기만 직무 조작 0 · 머리 제목 중심 = 머리 중심(폰 · 320 긴 이름 · 아이패드 레일 뺀 폭) · 뒤로 버튼과 겹침 0 |
| `test/capture/visual_capture_test.dart` | 5상태 · 부분/모두 수락 · 320/599/600 긴 시술명 · 긴 담당의 · 긴 방 이름 장면 추가 |

바뀌지 않음: 시술 수 · 완료 수 · 서버 순서 · 목록 2줄 상태 박스 · 호출 탭 · 상단 호출 상자 내용과 직무별 수락 · 재호출 · 모두 완료 귀가 상자 · 마취 칸 · 통역 · 세션 · API · 푸시.

## 검증 (`detail-polish-evidence/logs/`)

| 명령(cd app · FVM 3.44.8) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **200 passed · 29 skipped(캡처 전용) · 0 failed**(이전 190 + 새 10 · 기존 회귀 모두 통과) |
| 캡처 `DAY_CAPTURE_DIR=…/screens fvm flutter test test/capture/visual_capture_test.dart` | 29 passed → PNG 86 + 시뮬레이터 2 |
| `fvm flutter build ios --no-codesign` | ✓ 17.5MB · ATS 키 0 |
| 표준 `lib/main.dart` 로컬 sim debug 빌드(브리프 4개 dart-define) | ✓ |
| native 47 | 재실행 안 함(native 변경 0) |

## 스크린샷 (`detail-polish-evidence/screens/` · fixture 렌더 = 실데이터 아님 · 실글꼴)

- `phone-detail-5states` · `-scrolled` / `ipad-detail-5states` · `-scrolled`: 진행중(연한 DAY · 「05:24」 · 「KOS-DEMO · 13:54 시작」 · [종료][⋮]) · 준비중(KOS-DEMO · 서버 canStart true → 켜진 [시작]) · 호출 중(담당의 미정 · 회색 [시작]) · 수락 뒤(김원장 · [시작]) · 완료(회색 · 「완료 11분」 · [⋮]). 상단 호출 상자는 미수락 호출(리쥬란)만.
- `*-detail-partial-accept`(상자 남음 · 「원장 골라 수락 · 1건」) · `*-detail-all-accepted`(상자 없음 · 행에 김원장).
- `phone320/short599/short600-detail-long-rows` · `-scrolled` · `-done`: 머리 「A-레이저 시술…」 가운데 말줄임 · 뒤로와 겹침 0 · 큰 「75:03」 · 긴 담당의 말줄임 · [시작] · 「완료 11분」 · ⋮ 잘림 0.
- 머리 가운데: 모든 상세 PNG(폰 = 화면 가운데 · 아이패드 = 레일 뺀 콘텐츠 폭 가운데).

## 시뮬레이터

- `orca-mobile-iphone` 5C9E05C7-… 에 `simctl install` 덮어쓰기(uninstall · erase · 로그아웃 · 토큰 삭제 0) → **최종 PID 28681**. 사용자가 로그인해 둔 세션이 복원된 로컬 현황 목록 화면(`simulator-after-reinstall.png`) 그대로. 로그인 입력 · 업무 조작 0.

## 남은 것

- 상세 마취 칸 글자(OQ-A31 남은 부분)는 범위 밖.
- 사용자 실기기 · 로컬 실데이터에서 상세 5상태 눈 확인은 사용자(조작은 하지 않았음).
