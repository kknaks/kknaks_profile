# 보고 — 메모·사람 벌 안건 변경을 스트림으로 내려보낸다 · 2026-09-15

`backend-memo-line-edit-report.md` 열린 물음 1번의 답(사용자 결정 2026-09-15). 커밋 `f89de32`.

## 한 줄

프레임 **넷**을 더했다 — `memo.line.updated` · `memo.line.removed` · `agenda.updated` ·
`agenda.removed`. **「바뀐 것 하나」로 가고 모든 프레임이 id 로 제자리를 짚는다**(그것이 에코 처리다).
**안건도 같은 구멍이어서 같은 결로 냈다.** 사람 벌만 민다. 기존 프레임 둘은 이름도 본문도 그대로다.
회의 테스트 233개 초록 · 전체 1240 passed.

---

## 1. 프레임 모양과 고른 이유

### 낸 것 넷 (기존 둘은 그대로)

| 타입 | 본문 | 언제 | 화면이 |
|---|---|---|---|
| `memo.line` *(기존)* | `{agendaId, line}` | 메모를 **썼다** | 목록에 더한다 |
| **`memo.line.updated`** | `{agendaId, line}` | 메모를 **고쳤다** | `line.line_id` 로 찾아 **갈아 끼운다** |
| **`memo.line.removed`** | `{agendaId, lineId}` | 메모를 **지웠다** | 그 `lineId` 를 **지운다** |
| `agenda.added` *(기존)* | `{agenda}` | 사람 벌 안건이 **섰다** | 목록에 더한다 |
| **`agenda.updated`** | `{agenda}` | 사람 벌 안건 제목이 **바뀌었다** | `agenda.agenda_id` 로 찾아 **갈아 끼운다** |
| **`agenda.removed`** | `{agendaId}` | 사람 벌 안건이 **사라졌다** | 그 안건과 **그 아래 줄을 함께** 지운다 |

`_stream_message` 의 camelCase 계약 그대로다 — 봉투 키는 `type`·`agendaId`·`lineId`·`agenda`·`line`,
그 **안의 dto 는 상세 응답과 같은 snake_case**(`line_id`·`at_ms`·`track`…)다. 기존 `memo.line`·
`agenda.added` 가 이미 그 모양이고 화면이 상세 응답의 항목과 같은 코드로 그린다.

### 「바뀐 것 하나」로 갔다 — 벌 통째가 아니라

AI 배치는 `ai.batch` 로 **그 벌 전체**를 보내고 화면이 통째로 다시 그린다. 메모에 그 모양을 쓰지 않은
이유는 **쓰는 주체가 다르기** 때문이다.

- AI 벌은 **배치 하나가 회차마다 전량 교체**한다 — 그 회차 출력이 곧 전체이므로 통째가 자연스럽다.
- 메모는 **한 줄씩 쌓인다**(§6-7 자동 저장). 통째로 보내면 그 프레임이 만들어진 시점과 화면이 적용하는
  시점 사이에 들어온 줄이 **지워진다.** 회의 중이라 그 틈이 실제로 열린다.

그래서 프레임 하나가 **줄 하나 / 안건 하나**를 말한다.

### 기존 이름을 고치지 않았다

`memo.line` 을 `memo.line.added` 로 맞추면 셋이 균형을 이루지만 **지금 붙어 있는 화면이 깨진다.**
얻는 것은 이름의 균형뿐이고 잃는 것은 도는 회의다. 「추가는 `memo.line`, 나머지는 `memo.line.*`」의
살짝 기운 모양을 그대로 두고 이 문단을 근거로 남긴다. (같은 이유로 op 필드를 넣지 않았다 — 이 모듈은
`transcript.partial`/`transcript.final` 처럼 **타입을 갈라 쓰는** 결이다.)

---

## 2. 안건도 냈다 — 근거

**같은 구멍이었고 더 아프다.** 서는 것만 내려가고 있었다 (`agenda.added`, D45).

- **제목이 바뀌면** — 참여자 화면이 옛 제목을 들고, 그 아래 쌓이는 메모가 엉뚱한 이름 밑에 선다.
  회의 중 사람 벌 안건 수정이 이제 열려 있으므로(사용자 결정 2026-09-14) **실제로 생기는 자리**다.
- **사라지면** — 참여자 화면에 **없는 안건이 남는다.** 그리고 메모 칸의 안건 고르기가 그것을 계속
  내어, 주최자가 그것을 고르면 서버가 **404** 로 답한다. 줄 쪽의 「없는 줄을 고치려 들면 404」와
  같은 모양이고, 안건은 **그 아래 줄이 함께 사라지므로** 화면이 들고 있는 양이 더 크다.

### 사람 벌만 민다

| 벌 | 왜 |
|---|---|
| `memo` | **민다.** 사람이 회의 중에 손대는 유일한 벌이다 |
| `ai` | **안 민다.** `ai.batch` 로 통째로 간다 — 같은 회차를 두 계약으로 두 번 받으면 그 둘이 어긋나는 순간이 생긴다 |
| `final` | **안 민다.** 최종 벌은 「종료」·「실패」에만 서고 **서버는 종료 시점에 스트림을 닫는다** (§5.3) — 밀 방이 없다 |

판정은 **밀기 전에** 한다 — `bootstrap/application.py` 가 `result["track"] == TRACK_MEMO` 를 보고,
삭제는 `remove_agenda` 가 **지운 안건의 벌을 돌려주게** 고쳐서(`application.py:1174`) 같은 판정을 한다.
`add_agenda` 의 기존 push 에도 그 조건을 더했다 — 「종료」·「실패」에서 세우는 안건은 최종 벌이고,
그때 방이 없어 무해했지만 조건 없이 부르는 코드는 다음 사람에게 거짓말을 한다.

---

## 3. 에코 처리 — id 로 제자리를 짚는다

**쓴 사람에게도 같은 프레임이 간다.** 방 전체 브로드캐스트는 기존 계약이고(`_Room.broadcast`:
「확정·AI 증분은 업스트림 자신에게도 간다 — 화면이 하나의 계약만 읽는다」) 바꾸지 않았다.

**보낸 사람을 서버가 빼지 않는 이유 둘** —

1. **한 사람이 탭을 둘 열 수 있다.** 보낸 연결만 빼면 되지만 «그 사람의 다른 탭»은 받아야 한다.
   연결 단위로 빼는 것은 방이 「누가 보냈나」를 프레임마다 들고 다녀야 한다는 뜻이다.
2. **필요가 없다.** 모든 새 프레임이 **멱등**하게 설계돼 있다.

| 프레임 | 두 번 적용하면 |
|---|---|
| `memo.line.updated` | `lineId` 로 찾아 갈아 끼우므로 **같은 결과** |
| `memo.line.removed` | 없는 `lineId` 를 지우므로 **아무 일도 없다** |
| `agenda.updated` | `agenda_id` 로 갈아 끼우므로 **같은 결과** |
| `agenda.removed` | 같다 |

**화면이 할 일** — `line_id`/`agenda_id` 를 키로 **upsert·delete** 하면 에코를 따로 다루지 않아도 된다.
기존 `memo.line`(추가)만 유일하게 append 이므로, 그쪽도 `line_id` 키로 upsert 하면 자기 요청의 응답과
프레임이 겹쳐도 두 번 그리지 않는다 — **이미 그렇게 하고 있으면 새로 할 일이 없다.**

`actor` 필드를 넣지 않았다: 사람 벌을 쓰고 고치고 지우는 사람은 **언제나 회의를 만든 사람 하나**이고
(§3.3 · §6-1) 화면은 그 값을 `meeting.created_by` 로 이미 안다. 늘 유도되는 값을 프레임마다 실어
보내지 않는다.

---

## 4. 프론트가 쓸 계약

**전송** — 기존 회의 스트림 하나다. `WS /api/meetings/{meetingId}/stream`, 첫 프레임 `auth`
(`role: "upstream" | "subscribe"`) 뒤 `ready`. 새 프레임은 그 통로에 섞여 온다.

### `memo.line.updated`

```json
{ "type": "memo.line.updated", "agendaId": "…",
  "line": { "line_id": "…", "track": "memo", "order": 2, "text": "고쳐 쓴 줄",
            "author": "mina", "at_ms": 41230, "evidence": [], "from_lines": [] } }
```

- **언제** — `PATCH /api/meetings/{id}/agendas/{agendaId}/lines/{lineId}` 가 **커밋된 뒤.**
- `line` 은 `memo.line` 과 **같은 본문**이고 상세 응답의 `lines[]` 항목과도 같다.
- `line_id`·`at_ms`·`author`·`order` 는 **바뀌지 않는다** — 제자리에서 `text` 만 갈아 끼우면 된다.

### `memo.line.removed`

```json
{ "type": "memo.line.removed", "agendaId": "…", "lineId": "…" }
```

- **언제** — `DELETE …/lines/{lineId}` 커밋 뒤. 본문이 없다(지워진 줄에 실을 내용이 없다).

### `agenda.updated`

```json
{ "type": "agenda.updated",
  "agenda": { "agenda_id": "…", "track": "memo", "order": 1, "title": "고쳐 쓴 안건",
              "source": "manual", "merged_from": [], "concluded": false,
              "last_saved_at": "…", "title_placeholder": false, "lines": [...], "todos": [] } }
```

- **언제** — `PATCH /api/meetings/{id}/agendas/{agendaId}` 가 **사람 벌 안건**을 고쳤고 커밋된 뒤.
- `agenda.added` 와 **같은 본문**이다 — `lines`·`todos` 를 포함한 그 안건 전체.
- **`track` 은 언제나 `"memo"`** 다. 다른 벌은 이 프레임을 타지 않는다.

### `agenda.removed`

```json
{ "type": "agenda.removed", "agendaId": "…" }
```

- **언제** — `DELETE /api/meetings/{id}/agendas/{agendaId}` 가 **사람 벌 안건**을 지우고 커밋된 뒤.
- **그 안건에 매달렸던 줄도 함께 사라졌다** (§4.1-10) — 화면도 그 안건과 그 줄을 같이 지운다.

### 셋만 기억하면 된다

1. **id 로 제자리를 짚는다** — `lineId`·`agendaId` 로 upsert·delete. 그러면 에코도, 프레임이 두 번
   와도 안전하다 (§3).
2. **자기가 보낸 것도 되돌아온다** — HTTP 응답으로 이미 그렸으면 같은 자리를 다시 쓰게 된다(무해).
3. **놓쳐도 회의가 깨지지 않는다** — 방이 없으면(회의가 도는 중이 아니면) 서버는 조용히 건너뛰고,
   변경은 이미 저장돼 있다. 화면은 다음에 열 때 상세 응답으로 맞춰진다.

### 깨지는 것은 없다

기존 프레임 둘(`memo.line`·`agenda.added`)은 **타입 이름도 본문도 그대로**다. 더해진 타입 넷이고,
`switch (frame.type)` 에 `default` 가 있으면 지금 화면은 **모르는 타입을 무시**하며 그대로 돈다.

---

## 5. 테스트가 거는 것

| 테스트 | 무엇을 거는가 |
|---|---|
| `test_meeting_stream.py::test_fixing_and_dropping_a_memo_line_reaches_every_connection_in_the_room` | **고치면 간다 · 지우면 간다.** 쓴 사람과 구독자에게 **같은 프레임**이 가고, 고침은 `memo.line` 과 같은 본문(`line_id`·`author`·`track` 그대로)이며 삭제는 `{type, agendaId, lineId}` 정확히 그것뿐 |
| `…::test_renaming_and_dropping_a_memo_agenda_reaches_every_connection_in_the_room` | **안건 제목 변경·삭제도 간다.** 고침은 `agenda.added` 와 같은 본문이고 `track == "memo"`, 삭제는 `{type, agendaId}` |
| `…::test_the_ai_track_does_not_ride_the_memo_frames` | **AI 벌 변경으로는 이 프레임이 나가지 않는다.** 배치가 AI 벌을 세우면 `ai.batch` 하나로 가고, 그 앞에 지나간 프레임에 메모·안건 타입이 **한 장도 없다**(`_drain_recording` 이 지나친 타입을 모아 본다) |
| `…::test_someone_outside_the_meeting_never_receives_the_memo_frames` | **참석자가 아니면 받지 않는다** — 프레임을 걸러서가 아니라 **방에 못 들어와서**다. 밖의 사람은 붙지 못하고(`_SUBSCRIBE` 뒤 끊긴다), 그 사이 메모가 바뀌고 사라져도 나가는 자리가 없다 |
| `test_a_memo_someone_writes_reaches_every_connection_in_the_room` *(기존)* | 쓰기는 그대로 돈다 — 기존 계약이 안 깨졌다 |
| `test_an_agenda_the_host_adds_mid_meeting_reaches_every_connection` *(기존)* | `agenda.added` 도 그대로 — 사람 벌 조건을 더했지만 회의 중 안건은 사람 벌이라 그대로 나간다 |

시험 발판 하나 — `_drain_recording(socket, wanted)` 를 더했다. `_drain_until` 과 같지만 **지나친
프레임의 종류를 함께 돌려준다**: 「오지 않았어야 하는 것」을 거는 데 그 목록이 필요하다.

---

## 6. 테스트 결과

```
cd backend && uv run pytest -n auto --dist worksteal
→ 8 failed · 1240 passed (335s)
```

- **회의 테스트 233개 전부 초록** — `tests/unit/test_meeting_*.py` 48 ·
  `tests/contract/test_meeting_*.py` 185. 스트림 파일만 따로 28 passed.
- **실패 8건은 전부 `material_*`** (`search` · `search_owners` · `folders` · `worker_recovery`)이고
  **그 네 파일을 따로 돌리면 36개가 전부 통과한다** (`36 passed in 75.53s`).
  - 그중 6건은 내 첫 기준선(변경 전 커밋, `6 failed · 1217 passed`)에 있던 이름이고, 나머지 둘도
    **같은 파일·같은 군**이다.
  - 이번 실행이 **335초**로 평소(약 200초)보다 길다 — 프론트 워커가 같은 기계에서 자기 테스트를
    동시에 돌리는 중이고, 이 군은 리스·시각 경합에 걸리는 flaky 다. 실행마다 2~8건 사이로 흔들린다.
- **자료 경로를 한 줄도 건드리지 않았다.** 내 변경으로 깨진 테스트는 없었다.

---

## 7. 하지 않은 것 (경계 확인)

- **AI 벌·최종 벌 무접촉** — `ai.batch` 계약과 최종 벌 저장 계약은 한 줄도 바꾸지 않았다.
  시험이 「AI 벌 변경으로는 이 프레임이 나가지 않는다」를 직접 건다.
- **폴링으로 때우지 않았다** — 통로는 이미 있었고 프레임만 없었다.
- **충돌 판정 미유입** (`OQ-308`) — `merge_conflicts` 류 0건.
- **권한 판정을 새로 얹지 않았다** — 스트림이 붙는 자리에서 이미 판정한다. 프레임에 또 얹으면
  판정이 두 곳에 살고 조용히 어긋난다.
- **프론트 무수정.** 동시에 도는 프론트 워커의 미커밋 산출물과 그가 더한 `Makefile` e2e 타깃은
  스테이징하지 않았다 — 경로를 하나하나 지정했고 `git add .` 도 `git stash` 도 쓰지 않았다.
- **로컬 스택·DB 무접촉** — API·워커·postgres·vite 를 건드리지 않았고 DB 에 아무것도 돌리지 않았다.
- **MCP 도구를 새로 내지 않았다** — 프레임은 도구 표면이 아니고, 메모 줄 수정·삭제 HTTP 둘은 지난 판에
  `excluded`(E2)로 올려 두었다.
- **push·PR 없음.** 커밋 `f89de32` 하나만 로컬에 있다.

---

## 8. 열린 물음

1. **회의가 도는 중이 아니면 프레임이 나가지 않는다** — 방이 없으면 조용히 건너뛴다(기존 push 들과
   같은 결). 「예정」·「취소」에서도 사람 벌 안건·줄을 고칠 수 있으므로(사용자 결정 2026-09-14) 그때의
   변경은 스트림을 타지 않는다. **그 상태에는 방에 붙은 사람이 없으니 지금은 아프지 않다** — 회의
   시작 전에 여럿이 같은 화면을 보는 흐름이 생기면 다시 볼 자리다.
2. **`agenda.updated` 는 `concluded`·`order` 변경에도 나간다** — 사람 벌 안건이면 무엇이 바뀌었든
   그 안건 전체를 다시 보낸다. 지금 사람 벌은 `concluded` 를 갖지 않고(§4.0-5, 409로 막힌다) `order`
   변경 표면도 화면에 없어 **실질적으로 제목 하나**다. 필드별로 가르지 않은 것은 프레임을 늘리지 않기
   위해서다.
