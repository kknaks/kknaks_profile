# 리뷰 리포트 — day-app 시술현황 상단 인박스 탭 제거(SPEC-003 개정 ⑤ · WP v6) / doc · 좁은 검수 (2026-11-10)

- 대상:
  - 스펙 트리 `4a5d4a47` 위 미커밋 `products/day/20-spec/spec-003-mobile-app.md`(+31/−30 · 파일 1개)
  - profile `delivery-request-v6.json` · `tabs-removal-spec-report.md`
- 원천:
  - `tabs-removal-spec-brief.md` · `_RESUME.md` :3 · :306 — 사용자 「이거 아직도 있는데?」 → 「응 시술현황은 카드만 보여주면 된느거 아니야?」 · 코디 확정 안내 = 상단 3탭 제거 · 4필터 + 카드 · 하단 4메뉴 유지
  - `delivery-request-v5.json` · `delivery-v5-approved-result.json`(contract `7327938e…` · plan_digest `fad1184b…`)
  - 코드 `4ee33f95`(읽기 근거만)
- 방법:
  - diff 직접 대조 · `git diff --check` · 옛 탭 정의 잔존 grep
  - v5 ↔ v6 JSON 경로 diff · harness 모델 1회
  - lint · schema는 planner 로그를 확인하고 반복하지 않았다
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 1)

계약 문장은 의도대로 바뀌었다:
- 시술현황 본문 = 연결 상태 줄 + 칩 4개 + `cards[]`만이다.
- 상단 3탭 · 호출/완료 목록 · 검색이 빠졌고 숨은 화면으로 옮기지 않았다.
- 수락 경로는 카드 호출 줄 · 상세 호출 상자 · 푸시로 남고, 직무 분기는 그대로다.
- 서버 `calls[]` · `doneTab[]` 수신 · 귀가 처리 · API는 무변경이다.

WP v6도 같은 Delivery의 최소 갱신이다. WARN 1건은 와이어프레임 줄을 지우면서 **아이패드 왼쪽 레일(하단 4메뉴)의 글자 한 칸까지 함께 지운 것**이다.

## FAIL

없음.

## WARN

### W1. 아이패드 와이어프레임의 4메뉴 레일이 깨졌다 — 「예약현황」의 「현황」 칸이 탭 줄과 함께 삭제됨
- 위치: `spec-003-mobile-app.md:104-110`(Wireframe 아이패드 열)
- 원천:
  - `4a5d4a47`의 같은 줄 = `│ 현황 │ [현황][호출 n][시술 완료 n] │`. 왼쪽 칸 「현황」은 레일의 「예약 / **현황**」(예약현황) 둘째 글자이고, 오른쪽만 지울 대상(인박스 탭)이다.
  - 브리프 「아래 4메뉴를 잘못 지우지 않음」.
- 문제:
  - 지금 레일 글자는 `예약 / 시술 / 현황 / 채팅 / 설정`이다. 「예약현황 · 시술현황 · 채팅 · 설정」이 아니라 「예약 · 시술현황 · …」처럼 읽혀, 4메뉴 그림이 틀어졌다.
  - 본문 U-2 · A-25 · A-40 · v6 A14는 4메뉴를 그대로 말해 계약 충돌은 아니다. 그러나 mobile 워커와 시각 검수가 보는 ASCII가 원천과 어긋난다.
- 수정 방향(planner · 한 줄): 그 줄을 통째로 지우지 말고 레일 칸은 남긴다. 예: `│ (끊김 줄 다음 · 폰 칸 그대로) │ │ 현황 │ 전체 · 확인 필요 · 시작 가능 · 시술 대기│`처럼 오른쪽 내용만 한 줄씩 당긴다. 또는 `│ 현황 │ (빈칸) │`으로 레일 글자를 되살린다. 폰 열의 탭 줄 삭제는 그대로 둔다.

## 범위 · 의미 정합 (diff 실측)

| 확인 | 위치 | 결과 |
|---|---|---|
| 본문 = 칩 4 + `cards[]`만 | 개정 ⑤ 머리 `:43` · U-2 `:193-196` · U-3 제목 · 화면 목록 `:633` · A-25 · A-40 | PASS — 「탭 셋」 정의(호출 n · 시술 완료 n 계산) 삭제 · 칩 · `inbox.section` · 서버 순서 · 칩 숫자 문장 무변경 |
| 빠진 것 · 옮기지 않음 | §1 뺌 행 `:81` · U-10 · U-11 「1차 앱에서 뺌」 · non_goals(v6 [6]) | PASS — 다른 메뉴 · 숨은 화면 없음 명시 · 새 대체 메뉴 · 완료 카드 합치기 · 새 정렬 없음 |
| 수락 경로 | U-6 들어오는 곳 = 카드 호출 줄 · 상세 호출 상자 · 푸시 · §1 넣음 행 「목록 카드 · 상세 · 푸시에서」 · S-2 · 프로토 차이표 · A-2 · A-39 · 닫은 것(수락 동선, 기록 + 「이후 개정 ⑤로 없음」) | PASS — 직무 분기 · API · 권한 무변경 · 수락 자리가 사라진 곳 없음 |
| 서버 수신 계약 | 스냅샷 표 `calls[]` 「수신만 · 카드 호출 줄 순서」 · `doneTab[]` 「수신만 · KOS 실패 토스트 방 · 고객 찾기」 · U-10/U-11 「정의는 DAY-SPEC-002 소유 그대로」 | PASS — U-13 KOS 실패 토스트의 `doneTab[]` 사용과 일치 |
| 귀가 처리 | U-9 `:308` 「카드가 목록에서 빠짐 · `doneTab` 서버 계약 그대로 · 완료 목록 없음」 · A-33 · v6 A21 | PASS — `canHome` · 확인 창 없음 · 되돌리기 없음 그대로 |
| 보기만 직무 | A-1 · S-3 「판(카드 목록) · 룸 상세는 보임」 | PASS — 옛 「호출 · 시술 완료는 보인다」 정정 · 권한 무변경 |
| 하단 4메뉴 · 머리 · 상세 | A-25 · A-40 · v6 A14 문장 · 개정 ④ 상세 · 2줄 상태 박스 무변경 | PASS(문장) · ASCII는 W1 |
| 옛 정의 잔존 | grep 「호출 탭 · 시술 완료 탭 · 인박스 탭 · 「현황」 탭」 → 모두 「개정 ⑤로 뺌/없음」 표기, 웹 SPEC-002 U-10 인용, 개정 ④ 역사 서술(`:41`)에만 남음 | PASS(아래 참고 1) |
| 삭제 기능의 옛 인수 조건 | A-1 · A-2 · A-25 · A-33 · A-39 정정 · 호출/완료 탭 전용 A 행은 원래 없었다(U-10 · U-11 본문만) · OQ-A2 · OQ-A30 정정 | PASS — 살아 있는 옛 AC 없음 |
| 이전 합의 회귀 | 13 UI · 로컬 API(needs · canRecall · 확인 창 · lastSeconds · pickable) · 상태 박스 2줄 · 상세 개정 ④ 문장 무변경 | PASS |

## WP v6 (`delivery-request-v6.json`)

| 점검 | 결과 |
|---|---|
| 모델 | `DeliveryRequest.model_validate` OK(contract_version 6 · L3) · 파싱 OK · schema 0 errors(planner 로그) |
| 버전 · 결속 | #235 현재 v5(`delivery-v5-approved-result.json` contract `7327938e…` · plan_digest `fad1184b…`)를 scope_delta가 정확히 인용 · 코드 head `4ee33f95` · 사용자 원문 + 코디 확정 안내를 실행 승인으로 결속 |
| 같은 Delivery | `day/day-app` · baseline `3f57c1af…` pending · app/만 · PR #237 하나 · 사용자 마지막 merge · backend 수정 없음 |
| 최소 diff(v5 → v6) | 바뀐 키 = title · scope_delta · contract_version · A0 · A1 · A2 · A14 · A21 · A27 · A28(추가) · target_delta[1] · [8] · [10] · [17](추가) · review_surface[0] · [11] · [12](추가) · non_goals[6] · phases[3] · verification[0]. 그 밖 무변경 |
| 원천 SHA | 「4a5d4a47 + 개정 ⑤ 미커밋 — 코디 커밋 head로 결속」 정직 표기 |
| 승인 | receipt · 승인 주장 없음(L3 새 plan_digest 승인은 코디 몫) |

## 검증

- `git diff --check` → 출력 없음 · exit 0 · `git status` M 1개(spec-003). 타 SPEC · `20-spec.md` · 코드 무변경.
- planner 로그: lint `--strict` 0 error / 263 warning · `products/day` 0 · v6 schema 0 errors.

## 참고 (결함 아님)

1. 개정 ④ 머리(`:41`)의 「호출 수락은 상단 호출 강조 상자 · 목록 카드 · 호출 탭에서만」은 그 개정 당시 기록이다. 개정 ⑤ 머리가 뒤에서 대체를 밝혀 충돌은 아니다. 「(호출 탭은 이후 개정 ⑤로 없음)」 꼬리를 달면 읽기 쉽다.
2. 코드 메모(`calls`/`doneTab` 파싱 유지)는 SPEC 스냅샷 표와 일치한다. 구현 때 탭 카운터(`calls` 미수락 수 · `doneTab` home 수) 계산 코드를 지워도 수신 모델은 남기는지만 코드 리뷰에서 확인하면 된다.

## 남은 것

- planner: W1 와이어 레일 한 칸 복원(문장 · JSON 변경 불필요).
- 코디: 개정 ⑤ 커밋(exact head) → v6 plan(origin/main 재 fetch) → L3 승인 → #235 apply → mobile 발주(board_screen 상단 3탭 · 호출/완료 본문 제거만).
