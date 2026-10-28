# 규칙 하나로 다시 — 2026-10-25 (사용자 지시 · `no-kind-instructions.md` 대체)

`_RESUME.md` §2 2026-10-25 마지막 결정 줄이 정본이다. 요약:

> **KOS 작업은 type(PROCEDURE · ETCETERA) 무관 전부 같은 시술.** 예외는 **「방 배정」 하나**.

「방 배정」 = 방이 붙은 ETCETERA 작업(지금 `rules.is_room_task` 판정 그대로).

## backend (`procedure/back/`) — 지금 반쯤 고친 상태에서 이 규칙으로 마무리
1. 스냅샷 `procedures[]` = KOS 작업 **전부**(CANCELED 만 뺌). **「방 배정」도 싣는다** — back 에서 거르지 않는다(10-23 WP-BE1 거르기 되돌림).
2. 스냅샷 작업마다 `isRoomTask: bool` 필드 하나 추가(`schemas/board.py`) — front 가 숨기는 데 쓴다.
3. 판정(pickable · canStart · canFinish · 호출 대상 · canCall · `all_done` · `payment_required` · 고객 상태 · need 등): **type 으로 거르지 않는다.** 「방 배정」만 판정에서 뺀다(체크 · 호출 · 시작 · 종료 대상 아님 · 「전부 완료」에서 기다리지 않음).
4. [귀가 대기]: KOS 취소 대상 = **아직 안 끝난 「방 배정」 작업만**. 다른 작업은 전부 완료여야 [귀가 대기]가 되므로 취소할 것이 없다.
5. 시험: ① ETCETERA(방 없음 · 예: 시트팩)가 일반 시술과 같게 체크 · 시작 · 종료 · 전부 완료에 든다 ② 시트팩이 안 끝났으면 [귀가 대기] 불가 ③ 방 배정은 스냅샷에 실리고 `isRoomTask=true` · 판정에서 빠짐 ④ [귀가 대기] 취소 sequences = 방 배정만 ⑤ 기존 드래그 순서 · 방 판정(type 무관) 시험 그대로 통과. `test_rules.py` 포함 전부 고친 뒤 `uv run ruff check . && uv run pytest -q` 전체 1회.

## frontend (`procedure/front/`) — 지난 수정(기타 작업 = 일반 시술 줄)은 그대로 두고
1. `types.ts` 에 `isRoomTask: boolean`.
2. **`isRoomTask` 인 줄만 그리지 않는다** — 카드 시술 줄 · 고객 탭 번호 원 · 호출 대상 · 개수 어디에도 안 보이게(`grep` 으로 작업 목록 쓰는 곳 전부).
3. 가짜 보드는 back 몫(방 배정 예시 1개 · 시트팩 예시 1개를 back 이 넣는다).
4. `npx tsc --noEmit && npm run lint && npm run build` 1회.

## 하지 않는 것
- 앱(`procedure/app/`) — 이번 판 아님. 문서(SPEC)는 코디가 뒤에 맞춘다.
- 헤더 · 드래그 · 순서 저장 · 방 판정(type 무관)은 건드리지 않는다.
