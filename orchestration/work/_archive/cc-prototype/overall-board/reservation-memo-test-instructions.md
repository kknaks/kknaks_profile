# [researcher] 추가 지시 — 「특이사항」 = visitor.memo 확인 (데모 쓰기 허가 · 1건)

앞 판 `reservation-reception-test-report.md` 에 이어진다. 완료 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 테넌트 assert · 운영 키 금지는 앞 판 §0 과 같다.

## 무엇을 하나

사용자 결정(2026-10-26): 시안 「주의사항」 = KOS 고객 **「특이사항」**. 확인할 것:
1. KOS 웹 고객 정보의 「특이사항」이 `visitor.memo`(공개 일정 · `getVisitor`)와 같은 칸인가
2. 내부 `visitor/v2/commands/update-visitor-management-information` 이 **묶음 전체를 덮어쓰나** — 메모만 바꾸려면 무엇을 같이 보내야 하나(유입 · 추천인 · 고객 유형 · 분류 · 담당 · 동의 · customAttributes)

## 허가된 쓰기 (이것만 · 1회)

- 앞 판 시험 A 일정의 **고객 1명**에게 `update-visitor-management-information` 1회. 방법: 내부 `get-visitor` 로 지금 관리 정보 전체를 읽고 → `memo` 만 `[ccc 시험] 특이사항 확인` 으로 바꾸고 → 나머지는 읽은 값 그대로 보낸다. 본문 모양은 `reservation-visitor-update-report.md` §2.3 · 웹앱 JS 기준
- 보내기 전후로 `get-visitor`(내부) · `getVisitor`(공개) · 그 고객 일정 상세의 `visitor.memo` 를 조회해 **메모 외 필드가 하나도 안 바뀌었는지** 필드마다 비교
- 끝나면 되돌리지 않는다(시험 메모는 남겨 둔다)

## 사용자 확인 부탁(리포트에 적기만)

KOS 웹 고객 정보 「특이사항」에 시험 문구가 보이는지는 사람이 본다 → 「정할 것」에 「사용자 눈 확인」으로.

## allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-memo-test-report.md`

리포트에 id · 이름 등 값 금지. 정할 것은 Q-79 부터.
