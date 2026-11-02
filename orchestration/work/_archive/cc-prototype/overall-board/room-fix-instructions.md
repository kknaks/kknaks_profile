# 방 판정 수정 — 2026-10-25 (로컬 E2E 중 발견 · 사용자 지시)

**사실**: 데모 지점 10-25 고객 3명(KOS 화면에서 A-룸1 · 4 · 6 에 배정됨)이 ccc 에서 `room_id` NULL → 카드 0. 원인 = `procedure/back/app/kos/sync.py:38-44` `_room_task` 가 **ETCETERA 이고 room 있는 작업만** 방으로 본다. 이번 KOS 데이터엔 ETCETERA 가 없고 방이 **PROCEDURE 작업마다** 붙어 있다(DB `procedure.room_kos_id`).

**결정**(`_RESUME.md` §2 2026-10-25 줄): 카드 방 = 그 일정의 작업 중 **type 무관 room 이 붙은 작업**들에서 고른다 — 여럿이면 `roomAssignedDateTimeUtc` 가 가장 늦은 것(없으면 다음 규칙은 네가 정하고 기본값 표시). 입실 시각(`room_assigned_at`)도 그 작업 값. 「방 배정」 줄을 스냅샷에서 빼는 판정(`is_room_task` = 방 있는 ETCETERA)은 **그대로**.

## planner 몫
- SPEC-003 0.4.2 → **0.4.3**: §3.3 KOS 필드 대응표의 방 · 입실 줄, §5.1 「방이 있다」 근거, OQ-511 관련 문장, §9 E2E 에 「방 배정 작업 없이 시술 작업에만 방이 있어도 카드가 뜬다」 한 줄. WORK-005 에 WP-BE3(방 판정) 한 줄. 부록에 처분 한 줄. `(r4)` 표기.

## backend 몫 (planner 뒤)
- `_room_task` 를 type 무관으로(이름도 뜻에 맞게) · 시험: ① PROCEDURE 에만 방 → 카드 방 있음 ② ETCETERA 방 + PROCEDURE 방 → 가장 늦은 배정 ③ 방 없음 → 카드 없음 ④ 「방 배정」 줄 빼기는 그대로. `uv run ruff check . && uv run pytest -q` 전체 1회.
