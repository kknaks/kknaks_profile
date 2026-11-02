# [researcher] 추가 지시 — 예약 이동 · 취소 · 부도 · 취소 되돌리기 (조회 + 데모 쓰기 시험)

앞 판 `reservation-memo-test-report.md` 에 이어진다. 완료 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 테넌트 assert · 운영 키 금지는 `reservation-reception-test-instructions.md` §0 과 같다.

## 1. 무엇을 하나

시안 예약 현황의 **카드 드래그 이동**(design-analysis-report §6 · Q-13)과 예약 상세 **[예약 취소]**, 그리고 상태 2계층의 **취소 · 부도**(`_RESUME` §2 「상태 = 2계층」)를 KOS 로 할 수 있는지 본다.

사용자(2026-10-26): **KOS 는 드래그 앤 드롭을 지원하지 않는다 — 별도 버튼으로 이동한다. 드래그는 ccc 가 지원하는 것**(KOS 쪽 호출은 같은 이동 API 로).

## 2. 읽을 것 (gitignore · 값 옮기지 마라)

`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/` 의 5개. 코디가 본 쓰기:

| 파일 | 장면 | 쓰기(항목 번호) |
|---|---|---|
| `예약이동.har` (12) | KOS 이동 버튼 | #7 `schedule/reservation/v2/commands/update-reservation` |
| `예약상세_수정.har` (34) | 예약 상세에서 그룹 · 시각 바꿔 저장 | #29 `update-reservation` |
| `예약취소.har` (33) | [예약 취소] → 고객 의사 취소 | #26 `schedule/reservation/v1/commands/cancel-reservation` |
| `예약부도.har` (11) | [예약 취소] → 예약 부도 | #6 `cancel-reservation` |
| `예약취소_되돌리기.har` (15) | 취소 → 되돌리기 | #5 `cancel-reservation` → #10 `revoke-canceled-reservation` |

**이 표로 끝내지 말고 다섯 파일의 KOS 요청을 전부 세어** 인벤토리를 만든다.

## 3. 할 일

1. 인벤토리(파일별 · 순서대로 · 본문 키 · 응답 모양).
2. **`update-reservation` 해부** — 두 건(이동 버튼 · 상세 수정) 본문 비교. 시각 · 그룹 · 구역만 바꾸나, 예약 전체(메모 · 상담 필요 · 담당 · 유입 · 지정 의사 …)를 통째로 보내나(빠진 필드가 지워지나 — 전후 조회로). 정원 초과 · 휴무 · 같은 고객 겹침 거절 조건(스펙 오류 코드)
3. **`cancel-reservation`** — 취소 · 부도가 본문의 무엇으로 갈리나(사유 enum?) · 일정 `reservation.status`(`CANCELED` · `NO_SHOW`) · flowStep 은 그대로인지 · 접수된 뒤에도 되나
4. **`revoke-canceled-reservation`** — 되돌리면 어느 상태로 가나 · 부도도 되돌리나
5. **공개 짝**: 공개 스펙의 예약 변경 · 취소 · 부도 · 복구 작업(이름 · 필드 · 차이). 없으면 「공개 없음」
6. **데모 쓰기 시험(허가)** — ccc 가 보낼 모양으로 각 1회:
   - 이동: 오늘 이후 데모 `RESERVED` 일정 1건을 **다른 시각 + 다른 예약 그룹**으로 1회(공개 짝이 있으면 공개로, 없으면 내부). 앞 판 시험 A · B 일정은 쓰지 마라
   - 취소 → 되돌리기: 다른 `RESERVED` 일정 1건에 취소 1회 → 되돌리기 1회
   - 부도: 일정이 남으면 1건에 부도 1회(되돌리지 않음)
   - 대상이 모자라면 데모 기존 고객으로 내부 `reserve` 로 만들어도 된다(「시험용으로 만듦」 표시). **시술 대기로 두지 마라**
   - 각 쓰기 전후 조회로 바뀐 필드 비교 · 반영 지연(0~3초) 감안
7. 시안 비교: 드래그 이동(놓으면 바로 이동 · 확인 없음) · [예약 취소](접수 전만 · 상태 「취소」) · 범례 「취소 · 부도」와 맞추기. 「정할 것」은 Q-83 부터 — 결정하지 마라

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-move-cancel-report.md`

리포트에 id · 토큰 · 이름 등 값 금지(모양만).
