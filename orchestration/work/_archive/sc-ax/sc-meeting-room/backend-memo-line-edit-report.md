# 보고 — 사람 벌의 줄 수정·삭제, 백엔드 · 2026-09-15

정본: `decision-final-is-the-note.md` §바뀌는 것 1 (「메모·안건을 고치고 지울 수 있다 — 진행 중에도」).
지난 판이 **안건만** 열어 남겨 둔 자리다(직전 보고서 §10-3). 커밋 `6a9c41a`.

## 한 줄

`PATCH`·`DELETE /api/meetings/{id}/agendas/{agendaId}/lines/{lineId}` 둘을 냈다 — **줄 하나가 한
요청이고** 사람 벌에만 열린다. 최종 벌은 한 덩어리 저장 그대로이고 AI 벌은 여전히 닫혀 있다.
회의 테스트 229개 전부 초록 · 전체 1242 passed · 남은 2건은 변경 전에도 실패한 `material_*` flaky.

---

## 1. 고른 표면 모양과 이유

### 줄 하나가 한 요청이다 — 최종 벌과 다르게

| | 사람 벌 (이번에 낸 것) | 최종 벌 (기존) |
|---|---|---|
| 주소 | `…/agendas/{agendaId}/lines/{lineId}` | `…/agendas/{agendaId}` |
| 단위 | **줄 하나** | 그 안건의 **줄 목록 전체** |
| 본문 | `{text}` | `{lines: [{line_id?, text}], expected_last_saved_at?}` |
| 계보 | 없다 (사람 벌은 계보를 갖지 않는다) | `from_lines` 를 줄 단위로 잇는다 |
| stale 판정 | 없다 | 안건 단위 (`expected_last_saved_at`) |

**왜 한 줄씩인가** — 메모는 한 줄씩 자동 저장으로 쌓이는 기록이다 (§6-7: 「자동 저장이고 저장 버튼을
두지 않는다」). 고치는 단위를 안건 전체로 두면 **회의가 도는 동안** 그 사이에 들어온 줄을 덮어쓴다:
사람이 세 줄째를 고치는 동안 네 줄째를 던졌으면, 목록 전체 저장은 네 줄째를 지운다. 최종 벌은 회의가
끝난 뒤 한 덩어리로 편집하는 화면이라(`[수정]`→`[저장]`) 그 문제가 없다.

**쓰는 자리와 같은 주소 아래 같은 본문을 쓴다** — `POST …/lines` 가 `{text}` 로 한 줄을 쓰고,
`PATCH …/lines/{lineId}` 가 같은 `{text}` 로 그 줄을 고친다. 화면이 두 모양을 익힐 일이 없다.

### 최종 벌에는 이 문을 열지 않았다

`PATCH …/lines/{lineId}` 를 최종 벌에도 열면 **두 가지를 우회한다** —

1. **줄 계보** — 한 덩어리 저장은 「id 가 왔고 본문이 달라진 줄의 `from_lines` 만 지운다」를 판정한다
   (§8-9). 줄 하나만 오는 문은 그 판정 없이 본문을 바꾼다.
2. **「그 사이에 누가 저장했나」** — 안건 단위 stale 판정(`expected_last_saved_at` · `SCR-106-I16`)이
   목록 저장에 걸려 있다.

그래서 최종 벌 안건의 줄에 이 문으로 오면 **409** 다. 시험이 그것과 「한 덩어리 저장은 그대로 돈다」를
같이 건다.

### AI 벌은 열지 않았다

`§7.3` 이 예외 없이 금지한다. 이 문이 AI 벌에 열리면 배치가 매 회차 **전량 교체**하는 기록을 사람이
중간에 고쳐 두는 모양이 되고, **다음 회차에 그 수정이 말없이 사라진다.** → **409**.

---

## 2. 파일:줄

| 자리 | 무엇을 |
|---|---|
| `platform/meetings.py:583 line(agenda, line_id, lock=)` | 그 안건의 줄 하나. **안건을 함께 묻는다** — 다른 안건의 줄 id 로는 찾히지 않는다 |
| `platform/meetings.py:592 rewrite_line_text` | 본문만 고친다. **`at_ms` 와 저자는 그대로** — 그 값은 그 줄이 «적힌» 자리를 말한다 (§6-5) |
| `platform/meetings.py:605 delete_line` | 줄 하나를 지운다. `order_index` 를 다시 매기지 않는다 — 빈 번호가 생겨도 목록 순서는 그대로다 |
| `modules/meetings/application.py:534 edit_memo_line` | 본문 정규화(`normalize_memo_text`) → 고침 → `last_saved_at` 갱신 |
| `application.py:553 remove_memo_line` | 지움 → **자동 취소 재판정** (§3.1-8) |
| `application.py:565 _memo_line_target` | **게이트 넷을 한 곳에서** — 만든 사람 · `can_edit_agendas.memo` · 사람 벌 안건 · 그 안건의 줄 |
| `bootstrap/application.py:1646` · `:1660` | 트랜잭션 경계. **배치 트리거를 새로 걸지 않는다**(§3 참조) |
| `entrypoints/http.py:833` · `:856` | 두 라우트 |
| `docs/unified-operations-inventory.json` | 두 라우트를 `status: excluded`(E2)로 올렸다 — MCP 도구를 내지 않는 이유는 **AI 가 사람 벌에 쓰지도 고치지도 않는다**(§7.3) |

### 게이트는 안건과 같은 축이다

`can_edit_agendas.memo` — **예정 · 진행 중 · 취소**에서 열리고 **정리 중 · 종료 · 실패**에 닫힌다.
안건과 같은 값을 쓰는 이유는 닫히는 이유가 같기 때문이다: 「종료」·「실패」에서 사람 벌은 최종본을
대조하는 **근거**이고 고칠 수 있으면 근거가 되지 못한다 (D53). 「정리 중」에는 합성이 그 재료를 읽는다.

---

## 3. 두 가지 판단 (발주에 없던 자리)

### ① 배치 트리거를 새로 걸지 않았다

`write_memo` 는 커밋 뒤 `CAUSE_AGENDA_SWITCH` 로 배치를 평가한다 — 메모가 안건을 옮겼다는 것은 화제가
바뀌었다는 뜻이다. **수정·삭제에는 걸지 않았다.**

- 배치는 제출하는 자리에서 `memo_lines` 를 **다시 읽으므로** 고친 본문이 다음 회차에 그대로 실린다.
- 오타를 고칠 때마다 provider 를 부르면 회의 중 호출이 타자 수만큼 늘고, 안건 전환 트리거는
  「화제가 바뀌었다」는 신호이지 「글자가 바뀌었다」가 아니다.

### ② 실시간 스트림에 프레임을 만들지 않았다 — **프론트가 알아야 하는 자리다**

`write_memo` 는 커밋 뒤 `MemoLineFrame` 으로 방 전체에 민다(§5.3 · D41) — 참석자가 폴링하지 않고
그 자리에서 줄을 본다. **수정·삭제에는 그에 맞는 프레임이 없다.** 프레임 집합
(`AudioFrame`·`ReadyFrame`·`TranscriptPartial`/`Final`·`AiBatchFrame`·`MemoLineFrame`·
`AgendaAddedFrame`·`StreamErrorFrame`)에 쓸 만한 것이 없고, 새 프레임은 §5.3 의 계약을 늘리는 일이라
발주에 없이 만들지 않았다.

**결과** — 회의 중에 메모를 고치거나 지우면 **그 방에 붙어 있는 다른 참석자 화면은 옛 줄을 그대로
들고 있다**(다시 열거나 다시 불러올 때 맞춰진다). 쓴 사람 자신의 화면은 응답으로 바로 맞는다.
프레임을 낼지는 §5.3 개정과 프론트 브리프에서 정할 일로 남긴다 → §6 열린 물음 1.

---

## 4. 프론트가 쓸 계약

### 메모 한 줄 고치기

```
PATCH /api/meetings/{meetingId}/agendas/{agendaId}/lines/{lineId}
Content-Type: application/json

{ "text": "고쳐 쓴 줄" }
```

**응답 200** — 그 줄 하나다. 상세 응답의 `lines[]` 항목과 **같은 모양**이다.

```json
{
  "line_id": "…", "track": "memo", "order": 2, "text": "고쳐 쓴 줄",
  "author": "mina", "at_ms": 41230, "evidence": [], "from_lines": []
}
```

- `at_ms` · `author` · `order` · `line_id` 는 **바뀌지 않는다.** 화면이 그 줄을 제자리에서 갈아 끼우면 된다.
- `text` 는 **1~2000자**. 앞뒤 공백은 서버가 떼고, 공백뿐이면 거절한다.

### 메모 한 줄 지우기

```
DELETE /api/meetings/{meetingId}/agendas/{agendaId}/lines/{lineId}
→ 204 No Content
```

확인을 받지 않는다 (사람이 자기가 적은 임시 재료를 걷는 것이다). 본문이 없다.

### 실패 코드 — 둘이 같다

| 코드 | 언제 | 화면이 할 일 |
|---|---|---|
| **422** | `text` 가 비었다(공백뿐) · 2000자를 넘었다 | 입력 칸에 그대로 두고 알린다. **빈 줄로 지우려 하지 말고 `DELETE` 를 쓴다** |
| **409** | `can_edit_agendas.memo` 가 거짓(정리 중·종료·실패) · **최종 벌의 줄** · **AI 벌의 줄** | 그 자리에 편집을 세우지 않는다. 뜨면 상세를 다시 읽어 상태를 맞춘다 |
| **404** | 그 줄이 없다 · **그 안건의 줄이 아니다** · 회의를 만든 사람이 아니다 · 회의를 볼 수 없다 | 목록을 다시 읽는다. **거절이 404 로 나가는 것이 이 모듈의 기존 계약이다** (§3.2-1 — 권한 밖도 「없는 것처럼」 답한다). 403 을 기다리지 마라 |

### 화면이 편집을 세우는 근거

- **`meeting.can_edit_agendas.memo`** — 안건의 [수정]·[삭제]와 **같은 값**이다. 줄에도 이 값을 쓴다.
- 서버가 다시 검사하므로 화면은 이 값으로 자리를 세우기만 하면 된다 (§6-5 의 `can_write_memo` 와 같은 결).
- **`can_write_memo` 와 다르다** — 그쪽은 「새 메모를 쓸 수 있는가」(만든 사람 × **진행 중**)이고,
  고치기·지우기는 **예정·취소에서도 열린다**. 두 값이 어긋나는 상태가 실제로 있다.

### 깨지는 것은 없다

기존 필드의 형도 값도 바뀌지 않았다. **더해진 표면 둘**이고, 화면이 그것을 부르지 않으면 지금 동작이
그대로다. 다만 §3-② 의 스트림 자리는 **프론트가 알고 있어야 하는 한계**다.

---

## 5. 테스트가 거는 것

| 테스트 | 무엇을 거는가 |
|---|---|
| `test_meeting_memo_batch.py::test_a_memo_line_is_fixed_and_dropped_one_line_at_a_time_while_the_meeting_runs` | **진행 중 사람 벌 줄을 고칠 수 있다 · 지울 수 있다.** `at_ms`·저자·`line_id` 가 그대로 · **빈 본문은 422** · 남은 줄은 그대로 · 없는 줄은 404(지운 줄을 다시 지워도 같다) |
| `…::test_a_memo_line_belongs_to_the_agenda_in_its_path_and_to_no_other` | 다른 안건의 줄 id 로는 찾히지 않는다 (404) — 주소가 「어느 안건의 어느 줄」을 말한다 |
| `…::test_the_ai_track_lines_are_refused_by_the_one_line_surface` | **AI 벌 줄은 수정·삭제 둘 다 409** 이고 한 글자도 바뀌지 않는다 |
| `…::test_the_memo_track_lines_close_once_they_are_the_evidence` | **`can_edit_agendas.memo` 가 거짓이면 거절된다** — 정리 중·종료·실패 세 상태를 각각 밟아 409 를 보고, 그 뒤에도 본문이 그대로임을 본다 |
| `…::test_only_the_person_who_made_the_meeting_changes_its_memo_lines` | 만든 사람 하나다 — 참석자(jiho)도 밖의 사람(sora)도 404 이고 두 거절이 밖에서 구별되지 않는다 |
| `test_meeting_finalize.py::test_the_final_track_is_saved_as_one_list_and_not_one_line_at_a_time` | **최종 벌은 기존 계약대로 돈다** — 줄 하나씩 고치는 문은 409, 한 덩어리 저장은 **줄 id 를 싣고** 200, **빈 근거 거절**도 그대로 살아 있다 |

---

## 6. 테스트 결과

```
cd backend && uv run pytest -n auto --dist worksteal
→ 2 failed · 1242 passed (240s)
```

- **회의 테스트 229개 전부 초록** — `tests/unit/test_meeting_*.py` 48 · `tests/contract/test_meeting_*.py` 181.
- 남은 2건은 **둘 다 `tests/contract/test_material_worker_recovery.py`** 이고 **내 첫 기준선(변경 전
  커밋, `6 failed · 1217 passed`)에 같은 이름이 있다.** 그 파일만 따로 돌리면 전부 통과한다 —
  병렬 부하의 리스·시각 경합이고 자료 경로를 한 줄도 건드리지 않았다.
- 내 변경으로 깨진 것은 없었다. 인벤토리(`test_operation_inventory.py`)는 새 라우트 둘을 올려 맞췄다.

---

## 7. 열린 물음

1. **회의 중 메모 수정·삭제가 다른 참석자 화면에 실시간으로 닿지 않는다** (§3-②). 새 WS 프레임은
   §5.3 계약을 늘리는 일이라 만들지 않았다. 낼지 말지와 그 모양(`memo.line.updated`/`removed` 인지,
   `MemoLineFrame` 에 삭제 표시를 더하는지)은 §5.3 개정과 프론트 브리프의 몫이다.
2. **`todo.reference.line_ids`** 가 여전히 원본 줄 id 를 가리킬 수 있다(직전 보고서에서 옮겨 온 것).
   이번 판과 무관하지만, **메모 줄이 지워질 수 있게 되면서 그 참조가 끊길 자리가 하나 늘었다** —
   지금은 그 값을 화면이 그리지 않으므로 아프지 않다.
3. **`evidence` 를 든 메모 줄은 없다** — 사람 벌 줄은 `at_ms` 로 서고 근거 칩을 갖지 않으므로 수정이
   근거를 깨뜨리지 않는다. 최종 벌 줄의 `from_lines` 가 지워진 메모 줄을 가리킬 수는 있는데,
   그 계보는 **존재만 검증하고 없는 id 는 그 id 만 버린다**(§4.2-10)라 이미 답이 있다.

---

## 8. 하지 않은 것 (경계 확인)

- **AI 벌을 열지 않았다** — 수정·삭제 둘 다 409 이고 시험이 그것을 건다. 사람이 AI 벌에 손대는 길은 없다.
- **충돌 판정 미유입** (`OQ-308`) — `merge_conflicts` 류 필드·판정 로직 0건.
- **프론트 무수정.** 동시에 도는 프론트 워커의 미커밋 산출물과 그가 더한 `Makefile` e2e 타깃은
  스테이징하지 않았다 — 경로를 하나하나 지정했고 `git add .` 도 `git stash` 도 쓰지 않았다.
- **로컬 스택·DB 무접촉** — API·워커·postgres·vite 를 건드리지 않았고 DB 에 아무것도 돌리지 않았다.
- **최종 벌 계약 무수정** — 한 덩어리 저장·줄 계보·빈 근거 거절·stale 판정 그대로다.
- **push·PR 없음.** 커밋 `6a9c41a` 하나만 로컬에 있다.
