# planner-fix-1 리포트 — review-doc-1 WARN 7 + 사용자 결정 D6′ · D12 ~ D15 (2026-11-25)

- 워커: day `planner` · task `task_76aef4d6c631` · dispatch `ctx_00f1621e4601`
- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` (planner-1 미커밋 변경 위 · 커밋 · push 없음)
- 개정 번호 새로 안 땀 — SPEC-003 개정 ㉑ · SPEC-002 개정 ㉚ 머리글에 「같은 날 보충」 한 단락으로 적음
- 줄 번호 = 작업 트리 기준 · `S3` = `products/day/20-spec/spec-003-mobile-app.md` · `S2` = `products/day/20-spec/spec-002-procedure-board.md`

## 변경 파일

- `products/day/20-spec/spec-003-mobile-app.md`
- `products/day/20-spec/spec-002-procedure-board.md`
- `products/day/10-decision.md` (:39)
- `products/day/log.md` (:17 — 새 줄 한 줄)
- `products/day/20-spec.md` — 고칠 것 없음(지도 문장이 바뀐 결정과 어긋나지 않음)

## WARN W1 ~ W7

| # | 처분 | 고친 곳 |
|---|---|---|
| W1 iOS 가장자리 밀기 | D12 로 닫음 — 미저장이면 밀기 = 막힘(아무 일 없음 · 확인 창 없음 · Flutter 기본) · ✕ = 확인 창. 닫기 표에서 뒤로 가기를 Android 뒤로 / iOS 밀기 두 줄로 나눔 · 옛 「확인 창」은 취소선 + 날짜 · 사유 | S3:571 · S3:577 · S3:988 · S3:1233(A-55) · S3:1107(D12 행) |
| W2 JSON 요청 빈 값 | `staffId` · `baseLogId` · `baseDoctorStaffId` = uuid 또는 `null` · `body` · `baseBody` = 문자열(빈 문자열 허용) · 칸 생략 · 모르는 칸 = 400 `invalid_request`(`extra=forbid` — `backend/common/schema_config.py:6` `FROZEN_FORBID_CONFIG` 확인) · `staffId = null` 은 409 `chart_staff_required` 까지 감 · 이름 제안(OQ-99) | S2:690 · S2:49 |
| W3 「읽기 전용」 잔재 | §3 소비 기준 = 문장 안 경로 이름을 긋고 날짜 · 사유(차트 · 원장 바꾸기 둘 다) · OQ-A34 질문 칸 = 「읽기만」 · 「차트 API 를 부르지 않으므로 …」 취소선 + 「개정 ㉑ 전 사실」 | S3:678 · S3:1313 |
| W4 `chart_too_long` | 두 곳에 「자리만 — 지금 서버는 보내지 않음」 · SPEC-002 케이스 매트릭스 행 가리킴 · 새 코드 만들지 않음 | S3:567 · S2:698 |
| W5 「최근 저장」 시간대 | 「기기 시간대」 → **병원 현지 시각(KST 고정 · 기기 시간대 무관)** — 앱 「마지막 종료 HH:MM」과 같은 `app/lib/ui/format.dart` `hm`(코드 `55e60aa4` :2 · :55-58 「병원 현지 KST 고정」 확인) · 웹 E58 `day_hm` 과 같음 | S3:558 |
| W6 카메라 / 앨범 갈래 | 계약 문장은 「사진을 고른다 — 여러 장(D1 · C28)」으로 줄이고 카메라 · 앨범 갈래는 「기본값(planner 제안 · OQ-A73)」으로 옮김 · OQ-A73 기본값 칸 · A-58 도 같게 | S3:587 · S3:1394 · S3:1236 |
| W7 A-38 | 「담당 원장 바꾸기」를 같은 자리에서 취소선 + 「0.2.0 개정 ⑲ U-22 로 부름」 | S3:1216 |

## 사용자 결정 (2026-11-25)

| 결정 | 처분 | 고친 곳 |
|---|---|---|
| D6′ | 미저장 없으면 ✕ · 뒤로 가기 · 끌어 내림 · 바깥 누름 다 닫힘(웹 U-14 와 같게 · 표의 옛 「닫히지 않음」 취소선) · 미저장 있으면 ✕ · Android 뒤로 = 확인 창 · 끌어 내림 · 바깥 누름 = 안 닫힘 · 「웹과 다른 곳」 문장 취소선(남은 차이 = iOS 밀기만) · **OQ-A71 닫음** | S3:83 ⑥ · S3:571-579 · S3:583 · S3:988-989(매트릭스 — 미저장 없음 행 추가) · S3:1233(A-55) · S3:1137(28행 #16) · S3:1105-1106(결정 표 D6 취소 · D6′ 행) · S3:1392 |
| D12 | 위 W1 | S3:577 · S3:1107 · A-55 |
| D13 | 탭 글자 = 「간호관리차트」 · 「의사차트」 · 「시술전후사진」 · 앱 옛 글자 취소선 · **OQ-A65 닫음** | S3:557 · S3:222(Wireframe) · S3:1229(A-51) · S3:1111 · S3:1386 |
| D14 | 아이패드 원장 고르기 팝오버(`doctor_picker.dart:83`) · 확인 창(`room_screen.dart:742`)도 세션(루트) Navigator · 원장 고르기 팝오버 투명 덮개(F1 · `doctor_picker.dart:88`) 그대로 · 팝오버 기준 위치는 WORK · **OQ-A76 닫음** | S3:599 · S3:83 ⑨ · S3:1230(A-52 — iPad 확인 추가) · S3:1112 · S3:1397 |
| D15 | iOS 권한 문구를 **사용자 글자 그대로** 표로 넣음(지금 문구 옆에 비교 · 지금 문구 = `Info.plist:52-57` @`55e60aa4` 확인) · 마이크 문구 그대로 · **Android = 해당 없음** — `AndroidManifest.xml` `uses-permission` 에 설명 칸이 없고 권한 창 글자는 OS 가 정함 · 카메라는 시스템 카메라 앱이라 `CAMERA` 선언도 없음(`AndroidManifest.xml:5-13` @`55e60aa4` 확인) · 옛 D10 문장 취소선 · A-17 = 「새 문구 없음 · D10」 취소선 + 「D15 표 글자 그대로 · Android 해당 없음」 · **OQ-A64 닫음**(막는 것 = 없음) · 10-decision 의 D10 문장 취소선 + D15 | S3:1045-1052 · S3:83 ⑩ · S3:1195(A-17) · S3:1113-1114 · S3:1385 · `10-decision.md:39` |

그 밖: S3:549 U-23 머리 · S3:83 · S2:49 머리글에 「같은 날 보충」 · `log.md:17` 한 줄(spec-change · DAY-SPEC-003, DAY-SPEC-002).

## 지어 넣은 글자

없음. 새로 들어간 화면 글자 = D13 탭 글자(웹 SPEC-002 C1 에 이미 있는 글자) · D15 권한 문구(사용자 지시 글자 그대로) 뿐.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error · 263 warning** · `products/day/` 줄 0(263 은 전부 다른 제품 기존 WARN — 무관 · fix 전과 같은 수)

## 남은 것 · 주의

- 열린 OQ 그대로: OQ-A63 · A66 ~ A70 · A72 · A73(이번에 갈래 기본값 추가) · A74 · A75 · A77 · A78 · SPEC-002 OQ-99 · OQ-100 — 전부 기본값 있음 · 착수 막는 것 없음(OQ-A64 가 닫혀 「막는 것」 칸 남은 것 0)
- review-doc-1 「참고(사소)」 — 결정 파일 경로 표기가 SPEC-003 / SPEC-002 frontmatter 에서 다른 것은 손대지 않음(링크 깨짐 아님 · 지시 범위 밖)
- 코드 주석 「세션 Navigator 에 묶는다」 부정확(`chart_sheet.dart:19` · `doctor_picker.dart:85`)은 WORK 몫
