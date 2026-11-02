# 보고 — 회의록 두 벌 뼈대, 백엔드 (SPEC-004 v0.5.1) · 2026-09-14

## 한 줄

일곱 갈래 + §11.4 표에 없는 둘(⑧ 벌별 게이트 · ⑨ 저장 계보)을 전부 넣었다. 커밋 `51ecceb`,
검수 지적을 닫은 커밋 `ec025f9`. 회의 테스트 **14개 파일 218개** 전부 초록이고 전체 **1227 passed** ·
**남은 실패 2건은 변경 전에도 실패했다** (`material_worker_recovery`, 회의와 무관). 게이트 하나 올려 답을 받았고(최종 벌 전량 비우기 ↔
승격된 후보), 계약에 구멍 하나를 발견해 아래 §열린 물음에 올린다.

**벌 이름은 `memo`·`ai`·`final` 이다** (사용자 결정 2026-09-14). SPEC §4.0-2 는 `human` 으로 적혀
있으나 사용자가 뒤집었다 — 줄이 이미 쓰던 표기를 그대로 두고 **안건의 벌 이름을 그 표기에 맞췄다.**
「한 벌 한 이름」은 그대로 만족하고, 저장된 글자가 뜻을 바꾸지 않으며, 기존 DB 행도 건드리지 않는다.
스펙 §4.0-2 · §11.4 마지막 행의 `human` 표기 정정은 코디가 따로 낸다.

---

## 1. 일곱 갈래 — 무엇을 어떻게

### ① 안건에 벌 축 신설 · `source` 를 사람 벌 안으로 좁힘

| 자리 | 무엇을 했나 |
|---|---|
| `platform/persistence.py:363` `MeetingAgendaRecord.track` | `String(10)` · `NOT NULL` · `server_default 'memo'`. 인덱스를 `ix_meeting_agendas_meeting_order` → **`ix_meeting_agendas_meeting_track_order`**(`meeting_id, track, order_index`)로 갈았다 |
| `persistence.py:377` `source` | `NOT NULL` → **nullable**. AI 벌·최종 벌의 안건은 `NULL` 이다 (§4.1-2) |
| `modules/meetings/domain.py:78-88` | `TRACK_MEMO`·`TRACK_AI`·`TRACK_FINAL` · `AGENDA_TRACKS` · `LINE_TRACKS = AGENDA_TRACKS` · `ORIGIN_TRACKS`(계보가 가리킬 수 있는 두 벌) |
| `domain.py:83` `AGENDA_SOURCES` | `{manual, set, carried, derived}` — **`ai` 은퇴** |
| `domain.py:146` `ensure_agenda_track` · `:155` `ensure_agenda_source(value, *, track)` | 출처가 사람 벌 밖에서 오면 **거절한다**(버리지 않는다). 벌 경계를 잘못 읽은 호출이고, 조용히 지우면 그 오독이 남는다 |
| `domain.py:71` `MAX_AGENDAS_PER_TRACK` | 한도의 뜻이 「회의당 20」에서 **「벌당 20」**으로 좁아졌다 (§4.0-3). `MAX_AGENDAS_PER_MEETING` 별칭은 걷었다 |
| `platform/meetings.py:361 agendas(track=…)` · `:395 agenda_count(track=…)` · `:405 next_agenda_order(track=…)` | 벌을 골라 읽는다. **순서는 벌 안에서 1 부터 다시 매겨진다** — 화면의 「안건 N」과 같은 값이다 |
| `application.py:1444 _agenda_view` | 응답의 첫 값이 `track` 이다. `source` 는 사람 벌만, `merged_from` 은 최종 벌만 |

### ② AI 가 사람 안건에 줄을 붙이지 않는다 (D14 폐기)

- `application.py:1263 replace_ai_track` — `existing.get(output.agenda_id)` 로 사람 안건을 이어 쓰던
  경로를 **통째로 걷었다.** 배치 출력의 안건은 언제나 AI 벌에 새로 선다.
- `schemas/ai_batch_output.json` — `agendas[].agenda_id` · `agendas[].source` **두 필드를 걷었다**
  (`required` 에서도). W-6 이 정한 값이다.
- `batch.py:95 BatchAgenda` — `agenda_id`·`source` 필드 삭제, `parse_output` 도 그에 맞췄다.
- `batch.py:193 build_warm_start_prompt` · `:241 _BATCH_INSTRUCTIONS` — 「이미 있는 안건에 맞으면 그
  `agenda_id` 를 그대로 적으라」는 지시를 걷고 「**사람의 안건에 줄을 붙이지 않는다 · 사람 안건에 할
  말이 있으면 네 벌에 그 안건을 세우고 거기 적는다**」로 바꿨다.
- `application.py:1108 warm_start_context` — 사람 벌 안건을 **맥락으로만** 싣고 **`agenda_id` 를
  싣지 않는다**(W-6). 이어 쓸 사람 안건이 없으므로 id 를 줄 이유가 사라졌다.
- `application.py:504 write_memo` — **경로의 안건이 사람 벌의 것이 아니면 거절한다** (§6-8).
- `application.py:527 append_line` · `domain.py:170 ensure_line_track` — **줄의 벌과 안건의 벌은
  언제나 같다** (§4.2-9). 다른 벌의 안건 id 를 실은 줄은 거절한다.

### ③ AI 벌 전량 교체의 예외 삭제

`platform/meetings.py:631 replace_track` — 「메모 줄이 매달린 AI 안건은 남긴다」 분기(옛 `:552`)가
**통째로 사라졌다.** `replace_track` 은 이제 `clear_track` 을 그대로 부른다: 그 벌의 줄 → 후보 →
안건을 차례로 지운다(매달린 것을 먼저 떼야 외래키가 끊기지 않는다).

### ④ 합성이 최종 벌을 전량 신규 작성 · 원본 불가침

| 자리 | 무엇을 했나 |
|---|---|
| `platform/meetings.py:588 clear_track` | **줄만 비우던 것 → 안건까지 비운다** (리뷰가 짚은 자리). 줄 → 후보 → 안건 순서 |
| `application.py:672 commit_finalized` | `existing` 조회와 「`agenda_id` 가 오면 이어 쓴다」를 걷었다. 최종 안건을 **언제나 새로 세운다**. `merged_from`·`from_lines` 를 `surviving_lineage` 로 걸러 싣는다 |
| `schemas/ai_final_output.json` | `agendas[].agenda_id` → **`merged_from`**(필수 · 빈 배열 허용) · `agendas[].source` 삭제 · `lines[].line_ids` → **`from_lines`** |
| `finalize.py:54 FinalLine` · `:70 FinalAgenda` | `FinalAgenda.agenda_id`·`source` → `merged_from`. `BatchLine` 을 상속한 `FinalLine` 이 `from_lines` 를 더 든다 |
| `finalize.py:265 _FINAL_INSTRUCTIONS` | 「이어 쓰는 안건이 **없다**」 · 「`merged_from` 에 그 안건이 나온 원본 안건 id 를 적어라 — 이것이 사람에게 「내가 적은 안건이 어디로 갔나」를 말하는 유일한 값이다」 |
| `finalize.py:340 build_final_prompt` | `agendas=` 하나 → **`memo_agendas=`·`ai_agendas=` 둘.** 두 벌의 안건 목록이 각자 재료로 실린다 (§8-3) |
| `application.py:595 finalize_input` | `memo_agendas`·`ai_agendas`·`memo_agenda_ids`·`ai_agenda_ids`·`memo_lines`·`ai_lines` |
| `application.py:774 retry_finalize` | 「최종 벌만 갈아 끼운다」로 docstring 정정 — 실제 비우기는 `commit_finalized` 의 `clear_track(final)` 하나다 |
| `finalize_service.py:9` | 「사람이 만든 안건은 하나도 빠지지 않는다」 → 「**원본 두 벌은 불가침이다** · 한 벌이 비어도 돈다(W-1)」 |

### ⑤ `title_placeholder` 를 AI 가 채우던 것 폐기 (D48)

- `application.py:1205` 의 「자리표시 제목은 AI 가 채운다」 분기를 **삭제했다.**
- `application.py:59 QUICK_START_AGENDA_TITLE` — `"안건 1"` → **`""`** (W-7: 「제목 값은 빈 값이다」).
  덤으로 「안건 1. 안건 1」 겹침(§12 R-50)의 **서버 쪽 원인이 사라진다** — 빈 제목을 화면이 무엇으로
  그리는가는 기획 소유 그대로다.
- 빠른 시작 안건의 `order_index` 를 **0 → 1** 로 고쳤다. 순서가 벌 안에서 1 부터 매겨지는데 0 이
  섞여 있으면 다음 안건이 1 로 나서 같은 번호가 둘이 된다.
- `title_placeholder` 열과 응답 필드는 **남긴다** — 「제목이 아직 자리표시인가」는 화면이 그 자리를
  다르게 그릴 근거이고 §4.1-7 이 개념을 유지한다. 사라진 것은 **AI 가 채우는 경로** 하나다.

### ⑥ 종료 뒤 상세 응답이 세 벌을 전부 낸다

- 상세 응답(`_detail` → `_agenda_view`)은 **원래도 줄을 걸러내지 않았다.** 리뷰가 짚은
  `application.py:778` 의 `[l for l in agenda["lines"] if l["track"]=="final"] or agenda["lines"]`
  한 줄은 `_detail` 이 아니라 **`export()`** 안에 있었다. 상세 응답이 원본을 가렸던 것은 안건에 벌
  축이 없어 **세 벌이 한 목록으로 섞여 나왔기** 때문이고, 벌 축이 그것을 가른다.
- `application.py:826 export` — 그 한 줄을 **`track == "final"` 안건만 내는 것**으로 바꿨다.
  `or agenda["lines"]` 폴백도 걷었다: 「내보내기에는 원본을 담지 않는다」(§8-11 마지막 줄)이므로
  최종 벌이 비면 비는 것이 맞다.

### ⑦ 줄의 벌 표기

**사용자 결정으로 되돌렸다** — 줄은 `memo`·`ai`·`final` 그대로이고, **안건의 벌 이름을 그 표기에
맞췄다.** 「한 벌 한 이름」(§4.0-2)은 그대로 만족한다. 그 결과 고칠 자리가 0 이고 DB 기존 행의
`meeting_lines.track` 도 손대지 않는다.

---

## 2. §11.4 표에 없지만 계약이 요구한 둘

### ⑧ `can_edit_agendas` 가 벌별 판정 셋이 됐다

`policy.py:160 AgendaTrackGates` — `memo`·`ai`·`final` 셋을 든 frozen dataclass. `as_dict()` 가
응답 모양을 낸다. `policy.py:203 MeetingView.can_edit_agendas` · `.can_add_agenda` 가 둘 다 이 형이다.

```
MEMO_AGENDA_EDITABLE_STATUSES  = {scheduled, cancelled}
MEMO_AGENDA_ADDABLE_STATUSES   = {scheduled, cancelled, in_progress}
FINAL_AGENDA_EDITABLE_STATUSES = FINAL_AGENDA_ADDABLE_STATUSES = {done, failed}
AI_AGENDA_*_STATUSES           = frozenset()   # 언제나 거짓
```

「정리 중」이 어느 집합에도 없다 — 정리가 도는 동안에는 어느 벌도 열리지 않는다.

게이트를 지나는 자리:
- `application.py:1042 _agenda_target(track=…, adding=…)` — `gates[track]` 하나로 판정한다.
- `add_agenda` 는 **상태가 벌을 정한다** — 「종료」·「실패」면 최종 벌, 아니면 사람 벌. 사람이
  `[수정]` 에서 세운 최종 안건의 `merged_from` 은 비어 있다 (§8-9).
- `update_agenda`·`remove_agenda` 는 **그 안건이 선 벌**로 게이트를 고른다.
- `update_agenda` 의 `concluded` 는 **최종 벌에만** 열린다 (§4.0-5) — 원본 두 벌의 안건은 결론
  여부를 갖지 않는다. 사람 벌 안건에 `concluded` 가 오면 409.

**내가 정한 것 하나** — `can_add_agenda` 도 같은 벌별 셋으로 만들었다. 계약이 필드 «모양»을 정한
것은 `can_edit_agendas` 뿐이다(§3.3 `:185`). 다만 §4.1-6 표의 「안건 추가」 칸이 **이미 벌마다
다르고**, 불리언 하나로는 「종료에 최종 벌은 더할 수 있고 사람 벌은 못 한다」를 낼 수 없다 —
F-2 가 `can_edit_agendas` 에서 거부한 것과 같은 모양이다. 값을 발명한 것이 아니라 표를 기계적으로
옮겼다. 아니라면 되돌리기는 한 줄이다.

### ⑨ 최종 벌 저장이 줄 id 를 실어 계보를 잇는다

`PATCH /api/meetings/{id}/agendas/{agendaId}` 의 `lines` 가 `string[]` → **`{line_id?, text}[]`**.

- `commands.py:184 MeetingNoteLineInput` — `line_id: UUID | None` · `text: str`.
- `policy.py:58 normalize_final_line_rows` — 모양만 본다. 빈 줄은 버린다. **글자 하나는 받지 않는다**
  (`{"text": …}` 로 와야 한다): id 없이 목록만 받으면 손대지 않은 줄의 계보까지 첫 저장에 사라지고,
  그것이 검수 F-3 이 막은 자리다. 관용을 두면 그 버그가 조용히 돌아온다.
- `platform/meetings.py:507 save_final_lines` — 다섯 갈래를 여기서 가른다. 옛 `replace_lines`(그 안건
  그 트랙 줄을 delete 하고 다시 insert)는 **삭제했다** — 그것이 계보를 전멸시키던 코드다.

| 온 것 | 무엇을 하나 |
|---|---|
| id 가 왔고 본문이 그대로 | 그 줄을 이어 쓴다. `from_lines` **그대로** |
| id 가 왔고 본문이 달라짐 | **그 줄의** `from_lines` 만 지운다 |
| id 없이 옴 | 새 줄, 계보 없음 |
| 목록에 없는 id | 지워진 줄. 그 줄과 그 계보가 함께 사라진다 |
| 모르는 id | **그 줄만** 거절. 저장 전체를 물리지 않는다 |

- `_rewrite_note_lines` 는 **최종 벌이 아니면 409** 다 — 원본 두 벌은 사후에 손대는 자리가 없다 (D53).
- `entrypoints/http.py:788` 이 `model_dump(exclude_unset=True)` → **`request.changes()`** 를 쓴다
  (MCP·승인 재생은 이미 `changes()` 를 썼다).

### 계보 — 새로 만든 값

- `persistence.py:385 MeetingAgendaRecord.merged_from` — JSON `NOT NULL` · `server_default '[]'`
- `persistence.py:428 MeetingLineRecord.from_lines` — 같음 (`text` 가 이 클래스의 열 이름이라
  `sqlalchemy.text()` 를 가린다 — DDL 문자열로 적었다)
- `domain.py:186 surviving_lineage(claimed, *, known_ids)` — **존재만 검증한다.** 없는 id 는 그 id 만
  버리고 안건·줄 자체는 산다. 중복도 접는다. 「정말 그 줄에서 나왔는가」는 AI 의 자기보고라
  검증하지 않는다 — 검증 가능한 근거는 `evidence` 다.
- `commit_finalized` 가 `agenda_ids_in_tracks(ORIGIN_TRACKS)` · `line_ids_in_tracks(ORIGIN_TRACKS)`
  로 아는 집합을 만들어 그것으로 걸러 저장한다.

---

## 3. 새로 건 테스트 — 무엇을 거는가

**「벌이 갈렸다는 사실 자체」를 거는 것만 적는다.** 개명만으로 조용히 통과하는 테스트가 아니다.

| 테스트 | 무엇을 거는가 |
|---|---|
| `test_meeting_memo_batch.py::test_the_ai_track_is_replaced_whole_and_never_touches_a_human_agenda` **(다시 씀)** | **AI 가 사람 안건에 못 쓴다.** 사람 안건 아래에 `memo` 줄만 있고, AI 안건은 출처가 `null` 이고, 2회차에 **AI 안건 id 가 전부 새로 나며**(집합 교집합 0) 사람 벌은 한 글자도 안 바뀐다. 원래 이 테스트는 「사람 안건에 `ai` 줄이 매달린다」를 걸고 있었다 |
| `test_meeting_memo_batch.py::test_a_person_cannot_write_a_memo_into_the_ai_track` **(신규)** | 사람이 AI 벌 안건에 메모를 던지면 422 이고 **한 줄도 들어가지 않는다** |
| `test_meeting_finalize.py::test_the_merge_writes_a_new_final_track_and_leaves_both_origin_tracks_untouched` **(다시 씀)** | **합성이 원본을 안 건드린다.** 원본 두 벌의 응답이 저장 전후 `==` 로 같다. 최종 안건은 새 id 이고 `merged_from` 이 두 원본을 든다. 고아 줄 0 (외래키 순서) |
| `test_meeting_finalize.py::test_the_two_origin_tracks_stay_readable_and_read_only_once_the_meeting_is_closed` **(신규)** | **종료 응답에 세 벌이 다 있다** + 원본 두 벌은 제목·줄·삭제 셋 다 409 + 게이트가 `{memo:F, ai:F, final:T}` |
| `test_meeting_finalize.py::test_saving_the_final_track_keeps_the_lineage_of_every_line_it_did_not_change` **(신규)** | **저장이 계보를 안 죽인다.** 다섯 갈래를 한 번에 — 그대로 둔 줄은 계보 유지 · 고친 줄만 계보 삭제 · 새 줄 계보 없음 · 모르는 id 는 그 줄만 거절 · 빠진 id 는 삭제. **두 번째 저장에도 계보가 그대로다** |
| `test_meeting_finalize.py::test_a_failed_merge_can_be_retried_and_lands_under_the_new_rule` (보강) | **재시도가 최종 벌만 지운다** — AI 벌 줄이 그대로 남는다 |
| `test_meeting_finalize.py::test_a_meeting_that_already_closed_is_never_merged_again` **(내용 교체)** | 아래 §4 참조 |
| `test_meeting_policy.py::test_agenda_gates_are_three_verdicts_and_the_ai_track_is_never_open` **(신규)** | 여섯 상태 × 두 축 전수. 「진행 중은 더하기만 열린다」 · 「정리 중은 어느 벌도 아니다」 · 「종료·실패는 최종 벌만」 · **`ai` 는 어느 상태에서도 거짓이고 키는 언제나 낸다** |
| `test_meeting_domain.py::test_a_line_hangs_only_on_an_agenda_of_its_own_track` **(신규)** | 벌이 어긋난 줄은 거절 |
| `test_meeting_domain.py::test_lineage_keeps_only_ids_that_point_at_this_meeting_and_drops_the_rest` **(신규)** | 계보는 존재만 검증하고 없는 id 만 버린다 |
| `test_meeting_domain.py::test_agenda_source_vocabulary_is_closed_and_belongs_to_the_human_track_alone` (보강) | `ai` 출처 은퇴 + 다른 두 벌에 출처가 오면 거절 |
| `test_meeting_policy.py::test_final_line_rows_carry_their_id_and_drop_empty_sentences` **(내용 교체)** | 글자 목록을 **받지 않는다** (옛 `normalize_note_lines` 테스트를 대체) |
| `test_meeting_core.py` 게이트·빠른시작·결론표시 (보강) | 게이트가 벌별 셋 · 빠른 시작 제목이 빈 값 · 결론 표시는 최종 벌만 · 사람 벌 안건에 저장하면 409 |

### 바꿔 쓴 테스트 하나 — 무엇을 걸고 있었고 무엇으로 바꿨나

`test_a_second_merge_keeps_the_candidates_that_were_already_requested`
→ **`test_a_meeting_that_already_closed_is_never_merged_again`**

- **원래 걸던 것**: 「합성을 한 번 더 돌려도 **승격된 후보는 남는다**」 (§8-5). 제품에 그 길이 없어
  저장소 시점에서 `status` 를 `summarizing` 으로 **강제 기입해** 길을 만들어 확인했다 (테스트 주석도
  「완료를 다시 정리 중으로 돌리는 길은 없으므로」라고 적어 두었다).
- **지금 거는 것**: 「**그 길이 열려 있지 않다**」 — `(DONE, SUMMARIZING) not in MEETING_TRANSITIONS`,
  `ensure_transition` 이 거절, `POST /finalize` 가 「완료」에서 409, 그리고 승격된 후보가 그대로 서 있다.
- **왜 바꿨나**: 벌이 갈리며 최종 벌을 다시 지으면 **안건까지 전량 비우므로** 그 안건에 매달린 승격
  후보가 함께 죽는다. 예외를 두는 것(갈래 ①)은 v0.5.1 이 방금 걷어낸 모양을 최종 벌에 다시 세우는
  것이고, 재배치 규칙을 짓는 것(②)은 발명이다. 코디 결정은 **③ — 도달 불가로 두고 전제를 코드에
  남긴다** 였다. 보장의 «내용»이 바뀌었으므로 테스트도 그 내용을 건다.
- `platform/meetings.py:588 clear_track` docstring 에 **딛고 있는 가정**을 적었다: 승격된 후보가
  여기 매달릴 수 있는 유일한 길은 `done → summarizing` 이고 전이표가 그것을 막는다
  (`domain.py:MEETING_TRANSITIONS`) · **그 전이가 열리면 이 줄이 승격된 후보를 조용히 죽인다** ·
  `ensure_todo_actionable` 은 회의 상태를 보지 않으므로 그쪽이 막아 주지 않는다.

---

## 4. 깨진 프론트 계약 전수 — 다음 바퀴 발주서의 재료

`frontend/` 는 한 글자도 고치지 않았다. 아래가 전부다.

### 4.1 `track` 리터럴

**깨지지 않는다.** 줄의 `track` 은 `"memo" | "ai" | "final"` 그대로다 (`lib/viewModels.ts:851`).
사용자 결정으로 개명을 되돌린 결과다 — `MeetingDetailPage.tsx:74,139,376,458,508,516,555,822,825,883,886`
과 `LiveScript.tsx:28,53` 은 손댈 것이 없다.

### 4.2 envelope 필드 — 형이 바뀐 것 둘 (컴파일이 깨진다)

| 필드 | 전 | 후 | 프론트 자리 |
|---|---|---|---|
| `meeting.can_edit_agendas` | `boolean` | **`{memo: boolean, ai: boolean, final: boolean}`** | `viewModels.ts:917` 형 선언 · `MeetingDetailPage.tsx:293` `Boolean(meeting?.can_edit_agendas)` · `:288`·`:305` 주석 |
| `meeting.can_add_agenda` | `boolean` | **`{memo, ai, final}`** (§2 ⑧ 「내가 정한 것」) | `viewModels.ts` 의 `MeetingInfo`(선언 있음) · 「+ 새 안건」을 세우는 자리 |

`MeetingDetailPage.tsx:293` 의 `canEditAgendas = Boolean(meeting?.can_edit_agendas) && !live && !settling`
는 **객체가 늘 truthy 라 조용히 항상 참이 된다** — 타입 에러로 잡히지만 형 선언을 `any` 로 넘기면
게이트가 새는 자리다. `&& !live && !settling` 도 이제 서버가 말한다(「진행 중」·「정리 중」이 게이트에
반영됨) — 화면이 상태를 다시 추론할 필요가 없다.

### 4.3 envelope 필드 — 늘어난 것 셋 (읽지 않으면 기능이 안 선다)

| 필드 | 어디 | 무엇 |
|---|---|---|
| `agenda.track` | 안건마다 | `"memo" \| "ai" \| "final"`. **화면이 세 벌을 가르는 유일한 축** |
| `agenda.merged_from` | 안건마다 | `string[]`. 최종 안건이 묶은 원본 안건 id. 「(계보: 사람 벌 안건 2 · AI 벌 안건 1)」이 이 값을 읽는다 (§4.2 도식) |
| `line.from_lines` | 줄마다 | `string[]`. 최종 줄이 딛는 원본 줄 id |

`viewModels.ts:848 MeetingLine` 과 `:886 MeetingAgenda` 에 세 필드를 더해야 한다.

### 4.4 값이 바뀐 것 둘

| 필드 | 전 | 후 | 프론트 자리 |
|---|---|---|---|
| `agenda.source` | `"manual" \| "set" \| "carried" \| "derived" \| "ai"` | **`ai` 은퇴** · AI 벌·최종 벌 안건은 **`null`** | `viewModels.ts:891` 형 선언(`\| "ai"` 삭제 · `\| null` 추가) · `labels.ts:427 meetingAgendaSourceText(source: string)` 가 `null` 을 받는다(지금은 `?? ""` 로 빈 글자를 내므로 **런타임은 견딘다**) · `BookingModal.tsx:420` · `MeetingDetailPage.tsx:894` |
| 빠른 시작 안건의 `title` | `"안건 1"` | **`""`** (`title_placeholder: true`) | 화면 라벨이 「안건 N. {제목}」이라 지금은 「안건 1. 」로 보인다. **빈 제목을 무엇으로 그리는가는 기획 소유**(§12 R-50) — 그 결정이 오기 전까지는 화면 판단이다 |

### 4.5 응답 모양 — 목록이 길어진다

- `GET /api/meetings/{id}` 의 **`agendas` 가 세 벌을 전부 낸다.** 지금 화면은 `agendas` 를 한 목록으로
  그리므로 **같은 회의가 최대 3배로 보인다.** 가장 눈에 띄게 깨지는 자리다.
  - 「진행 중」: 「메모」 탭은 `track === "memo"`, 「AI 요약」 탭은 `track === "ai"` 로 걸러야 한다.
    **탭을 넘으면 안건 목록도 바뀐다** (§4.2-6 · D51) — 0.4.x 는 같은 목록을 두 번 냈다.
  - 「종료」·「실패」: 최종 벌을 본문으로, 원본 두 벌을 「원본」 자리에. **그 자리가 탭인지 드로어인지는
    미결이다** (`OQ-319`) — 서버는 세 벌을 다 내므로 화면이 고르면 된다.
- 안건의 `order` 가 **벌 안에서 1 부터** 다시 매겨진다. 세 벌을 한 목록으로 그리면 「안건 1」이 셋 보인다.
- `GET /api/meetings/{id}/export` 는 **최종 벌만** 담는다 (변화 없음에 가깝다 — 폴백만 사라졌다).

### 4.6 요청 모양 — 깨지는 것 하나

`PATCH /api/meetings/{id}/agendas/{agendaId}` 의 `lines`:

```
전: {"lines": ["첫 줄", "둘째 줄"]}
후: {"lines": [{"line_id": "…", "text": "첫 줄"}, {"text": "새로 더한 줄"}]}
```

- 글자 배열은 **422** 다. 관용을 두지 않았다 — 그것이 계보를 죽이던 모양이다 (F-3).
- 화면은 **읽어 온 `line_id` 를 편집 상태에 들고 있어야 한다.** 지금 `MeetingDetailPage.tsx:458` 은
  `stale.lines.filter(track==="final").map(line => line.text)` 로 **글자만** 뽑아 편집 상태에 담는다 —
  그 `.map` 이 id 를 버리는 자리다. `{line_id, text}` 를 함께 들고, 사람이 더한 줄만 `line_id` 없이 보낸다.
- 원본 두 벌의 안건에 `lines` 를 보내면 **409** 다.
- `concluded` 를 최종 벌 아닌 안건에 보내면 **409** 다.

### 4.7 MCP 도구 (참고)

`meeting_agenda_update` 의 입력 스키마가 바뀌어 `docs/unified-operations-inventory.json` 을
다시 떴다 (30줄 추가 1줄 변경 — 그 도구 항목 하나만).

---

## 5. 게이트로 올린 것

| | 무엇 | 결과 |
|---|---|---|
| 1 | **최종 벌 전량 비우기 ↔ 「이미 승격된 후보는 남긴다」 충돌** — 승격된 후보가 최종 벌 안건에 매달려 있는데 그 안건을 전량 지우면 후보도 죽는다 | **답을 받았다 — 갈래 ③**(도달 불가로 두고 전제를 코드에 남긴다). §3 「바꿔 쓴 테스트」 참조 |

**게이트로 올리지 않고 문서에서 답을 찾은 것 셋** (브리프 §8 이 짚은 자리):
- 「한쪽 벌이 비면」 → **§8-3 · W-1 이 정했다**: 그래도 합성을 돈다. 두 벌이 다 비어도 돈다.
  구현은 `finalize_input` 이 빈 목록을 그대로 싣고 `_summarizing` 이 안건 0개로도 선다
  (`test_a_meeting_opened_with_no_agenda_finalizes_on_what_the_batch_built` 가 건다).
- 「종료 뒤 사람 벌 편집」 → **§4.1-6 · D53 이 정했다**: 읽기 전용. `can_edit_agendas.memo` 가 거짓.
- 「배치 출력의 `agenda_id`」 → **W-6 이 정했다**: 싣지 않는다. 스키마 필드와 프롬프트 지시를 함께 걷었다.

---

## 6. 스키마가 기존 행에 하는 일

alembic 이 없으므로 `make sync-demo-schema`(= `reset_demo --sync`)다. **사용자 DB(`ax_demo`)에는
`plan()` 도 `apply()` 도 돌리지 않았다** — 기존 행을 어떻게 할지(`OQ-320`)는 사용자가 정하는 중이고
실물 회의가 도는 중이다. 0.4.x 스키마를 sqlite 로 재현해 계획과 결과만 확인했다.

```
ALTER TABLE meeting_agendas ADD COLUMN track VARCHAR(10) DEFAULT 'memo' NOT NULL;
ALTER TABLE meeting_agendas ADD COLUMN merged_from JSON DEFAULT '[]' NOT NULL;
ALTER TABLE meeting_lines   ADD COLUMN from_lines JSON DEFAULT '[]' NOT NULL;
사람이 정할 것: (없음)
```

- **기존 행이 기본값으로 찬다.** `meeting_agendas.track = 'memo'` · `merged_from = '[]'` ·
  `meeting_lines.from_lines = '[]'`. 기존 안건은 **사람 벌로 서서 「메모」 탭에 그대로 보인다.**
  계보가 빈 목록인 것은 맞는 값이다 — 벌이 갈리기 전의 안건·줄이라 가리킬 원본이 없다.
- 줄의 `track` 은 원래 있던 열이라 손대지 않는다 (`memo` 그대로).

> **⚠ 이 결과는 `schema_sync` 를 고친 뒤의 것이다.** 첫 판 보고서는 「기존 행이 전부 `NULL` 이 되고
> 기존 안건이 세 벌 필터에 안 걸린다」고 적었는데, 그것이 그때의 **실제 동작이었다.** 원인은 이
> 바퀴의 컬럼이 아니라 `schema_sync` 자체였고 별도 커밋 `addddbc` 로 고쳤다 — 아래 §11.

### 이관 코드는 쓰지 않았다

`OQ-320` 미결이다. 다만 **`schema_sync` 를 고친 뒤로 이관이 필요한 자리가 없어졌다** — 기존 안건이
`'memo'` 로 차므로 「`track IS NULL` 인 행을 무엇으로 채우나」라는 물음 자체가 서지 않는다. 「이미
쌓인 회의를 어느 벌로 옮기나」의 나머지(종료된 회의의 안건을 `final` 로 볼 것인가 등)는 그대로
`OQ-320` 이 정할 것이고, 내가 정하지 않았다.

### 인덱스 하나

`ix_meeting_agendas_meeting_order` → `…_meeting_track_order` 로 이름이 바뀌었다. `schema_sync` 는
**기존 표의 인덱스를 손대지 않으므로** 옛 인덱스가 남고 새 인덱스는 서지 않는다. 성능 문제이지
정합 문제는 아니다 — 데모 규모에서 눈에 띄지 않는다. (이 자리는 고치지 않았다: 인덱스 교체는
「잃을 수 있는 것」이라 그 도구의 설계상 사람 몫이다.)

---

## 7. 테스트 결과

```
cd backend && uv run pytest -n auto --dist worksteal
→ 3 failed · 1230 passed (189s)
```

세 판(세 벌 뼈대 · 검수 지적 · `schema_sync`) 뒤의 최신 결과다. **남은 3건은 전부
`tests/contract/test_material_worker_recovery.py` 이고, 그 파일만 따로 돌리면 5개가 전부 통과한다**
(`5 passed in 16.65s`) — 병렬 부하에서 리스·시각 경합에 걸리는 flaky 이고 내 변경이 자료 경로를
한 줄도 건드리지 않았다. 실행마다 2~4건 사이로 흔들린다.

**검수가 정정한 수치** (F-5) — 첫 판 보고서가 「13파일 · 269개 · 1226/2」로 적었는데 틀렸다.
바른 값은 **14파일 · 217개**(검수 시점: unit 48 · contract 169) · **1224 passed · 4 failed** 다.
검수 시점의 실패 4건은 전부 `material_*` 이고 **변경 전 커밋에서도 4건**이라는 것을 검수자가 별도
워크트리로 증명했다 — **결론은 같고 숫자만 틀렸다.** 이번 판에서 회의 테스트가 하나 늘어
(§10 새 테스트) 지금은 **218개**이고, 같은 명령의 최신 결과가 위 블록이다. `material_*` flaky 군은
실행마다 2~4건 사이로 흔들린다(시각·리스 경합).

### 신규/기존 실패 분리

| 실패 | 판정 | 근거 |
|---|---|---|
| `test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` | **변경 전에도 실패** | ① 내 첫 수정 **전에** 같은 명령을 돌린 기준선에 이 이름이 있다 (`6 failed, 1217 passed`) ② 검수자가 **별도 워크트리의 변경 전 커밋**에서 같은 실패를 재현했다 |
| `test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result` | **변경 전에도 실패** | 같음 |
| `test_material_worker_recovery.py::test_expired_owner_cannot_publish_after_a_new_attempt_takes_over` | **flaky (같은 군)** | 내 첫 기준선 6건에는 이 이름이 없었다 — 다만 **같은 파일의 같은 리스 경합 군**이고, 그 파일만 따로 돌리면 5개가 전부 통과한다. 병렬 부하가 만드는 실패다 |

- 기준선의 6건은 전부 `material_*`(자료 검색·워커 lease·폴더)였고 **회의 경로가 하나도 없었다.**
  지금 남은 2건은 그 6건의 부분집합이다 — 나머지 4건은 이번 실행에서 통과했다(시각·리스 경합에
  걸리는 flaky 군이고, 실패 메시지가 `['running','completed'] != ['failed','completed']` 처럼
  타이밍 그대로다).
- **회의 테스트는 14개 파일 218개 전부 초록이다**: `tests/unit/test_meeting_*.py` **7개 48 passed** ·
  `tests/contract/test_meeting_*.py` **7개 170 passed**.
- 내 변경으로 새로 깨져서 **고친** 것 3건: `test_operation_inventory.py`(MCP 스키마 스냅샷 재생성) ·
  `test_codex_cli.py` 2건(배치·합성 출력 고정값을 새 스키마로).

---

## 8. 열린 물음 — 스펙 다음 판으로

1. **「승격된 후보가 있는 최종 벌을 다시 지으면 무엇을 하나」가 SPEC 에 없다.** §8-5 는 「이미 승격된
   것은 남긴다」고 하고 §8-5·§8-8 은 「최종 벌을 안건까지 전량 비운다」고 하는데, 승격된 후보는
   최종 벌 안건에 매달린다(§8.2 `agenda_id`). 지금은 **도달 불가**라 급하지 않다 — 전이표에
   `done → summarizing` 이 없고 승격은 「종료」의 최종 후보에만 열린다. 그 두 다리 중 하나만
   무너지면 승격된 후보가 FK 로 조용히 죽는다. 코드에 전제를 주석으로 남겼다.
2. **`OQ-320`(기존 데이터 이관)이 이제 구체적인 한 줄로 좁혀졌다** — `meeting_agendas.track` 이
   `NULL` 인 기존 행을 무엇으로 채우나. 「버린다」면 사라지는 물음이다 (§6 참조).
3. **`todo.reference.line_ids` 가 여전히 원본 줄 id 를 가리킬 수 있다.** §8.2 는 「최종 후보는 최종
   벌 줄을 가리킨다」고 하는데, AI 는 저장 전이라 최종 줄 id 를 모른다 — 지금 구현은 AI 가 적어 준
   것을 그대로 담는다. **0.4.x 부터 있던 자리이고 §11.4 일곱 갈래에 없어 손대지 않았다.**
4. **`can_add_agenda` 의 응답 모양**을 내가 벌별 셋으로 정했다 (§2 ⑧). 계약이 모양을 정한 것은
   `can_edit_agendas` 뿐이다 — 아니면 되돌리기는 한 줄이다.

---

## 10. 검수 지적을 닫았다 (커밋 `ec025f9`)

리뷰: `review-backend-two-tracks-report.md` — 판정 **조건부 PASS**.

### FAIL — 「이전 회의 맥락」이 세 벌을 다 실었다

`application.py:590`(합성 입력) · `:1189`(웜스타트 맥락)의 `self._repository.agendas(source)` 에
**`track` 이 안 걸려 있었다.** 이어진 이전 회의의 사람 벌·AI 벌 안건까지 프롬프트에 들어갔다.
§7.2 는 이전 회의 조회가 「안건과 **결론**」을 준다고 했고 그 회의의 정본은 최종 벌이다.

더 나쁜 것은 `concluded` 였다 — **결론 표시가 서는 것은 최종 벌뿐인데**(§4.0-5) 원본 두 벌의 안건이
`concluded: false`, 즉 「결론 안 남」을 달고 AI 에게 실렸다. **없는 사실을 근거로 준 것이다.**

→ 두 자리 모두 **`agendas(source, track=TRACK_FINAL)`** 로 좁혔다. 각 자리에 왜 최종 벌 하나인지를
주석으로 남겼다.

**새 테스트** — `test_meeting_finalize.py::test_the_previous_meeting_is_carried_as_its_final_track_alone`

거는 것: 지난 회의 하나를 **세 벌이 다 선 「종료」**까지 끌고 가고(사람 안건 + 배치가 세운 AI 안건 +
합성이 지은 최종 안건 둘), 그것을 `carried_from_meeting_id` 로 이어받는 회의에서 **세 자리를 본다** —

1. **웜스타트 맥락**(`warm_start_context`)의 `carried_from.agendas` 가 최종 벌 둘뿐이고
   `concluded` 가 그 벌의 값 그대로(`[True, False]`)다.
2. **합성 입력**(`finalize_input`)의 같은 자리도 최종 벌 둘뿐이다.
3. **실제로 나간 프롬프트**에 원본 두 벌의 제목(「사람이 적은 안건」·「AI 가 세운 안건」)이
   **한 번도 오르지 않고** 최종 벌 제목은 오른다.

**고치기 전 코드에서 이 테스트가 실패하는 것을 확인했다** — `track=TRACK_FINAL` 을 되돌리면
`['사람이 적은 안건', 'AI 가 세운 안건', '결론 난 최종 안건', '결론 안 난 최종 안건']` 이 나온다.
검수가 「이 자리를 거는 테스트가 없어서 코드를 읽어서 찾았다」고 한 그 구멍이 이것으로 막혔다.

덤 하나 — `_with_recording` 이 `session.query(...).one()` 으로 음원을 골라 **한 시험에 회의가 둘
서면 깨졌다.** 회의를 지정해 고르게 고쳤다(이어진 회의를 세우는 시험이 이번에 처음 생겼다).

### WARN — 내가 닫은 것 둘

- **F-5 수치 정정** — §7 에 반영했다. 첫 판 보고서의 「13파일 · 269개 · 1226/2」가 틀렸고 바른 값은
  「14파일 · 217개 · 1224 passed · 4 failed」다. **결론(전부 `material_*` · 변경 전에도 실패)은 같고
  숫자만 틀렸다.** 이번 판에서 테스트가 하나 늘어 218개다.
- **nit `human` 잔재** — 테스트 이름 셋과 지역 변수를 `memo` 로 맞췄다:
  `test_agenda_source_vocabulary_is_closed_and_belongs_to_the_memo_track_alone` ·
  `test_the_ai_track_is_replaced_whole_and_never_touches_a_memo_agenda` ·
  `test_two_memo_agendas_may_be_folded_into_one_when_the_merge_rewrites_the_note` ·
  `memo_agenda`/`still_memo` 지역 변수. 「모르는 벌 이름」 케이스의 `"human"` 리터럴은 `"origin"` 으로
  바꿨다 — `human` 은 이제 **틀린 이름의 예시**로 쓰일 이유도 없다.

### WARN — 손대지 않은 것 둘 (코디가 가져간다)

- **F-3** §8-5 「이미 승격된 것은 남긴다」가 구현·테스트에서 사라진 건 — 갈래 ③ 결정대로다.
  **되돌리지 않았다.** §8 열린 물음 1번이 그것이다.
- **F-4** `can_add_agenda` — **그대로 뒀다.** §2 ⑧ 의 서술이 그 근거다.

---

## 11. 별건 — `schema_sync` 가 모델의 제약을 버렸다 (커밋 `addddbc`)

`bootstrap/schema_sync.py:36` 이 내던 DDL 이 **타입만** 실었다.

```
ddl = f"ALTER TABLE {name} ADD COLUMN {column.name} {column.type.compile(engine.dialect)}"
```

`nullable=False` 도 `server_default` 도 붙지 않아 **기본값이 있는 컬럼조차 nullable 로 붙었고, 그러면
기존 행이 전부 NULL 이 된다.** 이번 바퀴가 그 값을 치를 뻔했다 — `meeting_agendas.track` 은
`nullable=False, server_default 'memo'` 인데 DDL 에 둘 다 없어, 돌리면 사용자 DB 의 안건 52건이
`track = NULL` 이 되고 세 벌 필터 어디에도 걸리지 않아 **회의 39건이 빈 화면**이 된다.

**이번 컬럼만의 문제가 아니다** — 앞으로 모든 컬럼 추가에서 같은 일이 난다. `:37-39` 가 「NOT NULL
인데 기본값이 없으면 사람이 정한다」로 갈라 둔 것을 보면 **기본값이 있으면 그것을 실을 생각이었는데
실지 않은 것**이다.

### 무엇을 고쳤나

- `plan()` 이 컬럼 정의를 **손으로 조립하지 않고 SQLAlchemy 자신의 컴파일러**(`CreateColumn`)로 낸다.
  `CreateTable` 이 내는 것과 같은 글자이고, 기본값을 어떻게 인용하는지도 dialect 가 안다.
  → `track VARCHAR(10) DEFAULT 'memo' NOT NULL`. **기본값이 있는 NOT NULL 컬럼을 더하면
  데이터베이스가 기존 행을 그 값으로 채운다** — 그래서 이 한 자리가 「기존 행이 NULL 이 된다」를
  통째로 없앤다.
- **갈래를 하나 좁혔다**: 파이썬 쪽 `default=` 만 있고 `server_default` 가 없으면 **`manual` 로
  보낸다.** 전에는 조용히 nullable 로 붙였다 — `default=` 는 ORM 이 INSERT 할 때만 쓰여 **이미 있는
  행에 닿지 않으므로**, 모델은 「비어 있을 수 없다」는데 DB 에는 NULL 이 있는 상태가 된다.
- 덤 하나 — `MeetingLineRecord.from_lines` 의 `server_default` 를 글자로 줘서 SQLAlchemy 가 리터럴로
  **한 번 더 감쌌다**(기본값에 따옴표가 겹쳐 들어갔다). `text` 가 그 클래스의 열 이름이라
  `sqlalchemy.text()` 를 가리는 것이 원인이고, 별칭(`sql_text`)으로 부르게 고쳤다. 내가 첫 판에서
  만든 자리다.

### 새 테스트 넷 — `tests/contract/test_schema_sync.py`

| 테스트 | 무엇을 거는가 |
|---|---|
| `test_a_not_null_column_with_a_server_default_carries_both_into_the_ddl` | DDL 에 `NOT NULL` 과 `DEFAULT` 가 둘 다 있고, **`apply()` 뒤 기존 행이 그 값으로 찼다**(NULL 이 아니다). 문자열·JSON·불리언 셋 |
| `test_a_not_null_column_without_a_server_default_is_a_decision_for_a_person` | 파이썬 `default=` 만 있는 컬럼과 기본값이 없는 컬럼 **둘 다 DDL 0건 · manual 2건** |
| `test_a_nullable_column_is_added_as_the_model_wrote_it` | 비어 있어도 되는 컬럼은 `NOT NULL` 없이 붙고, 기본값이 있으면 그것도 실린다 |
| `test_the_meeting_track_axis_lands_on_existing_rows_rather_than_nulling_them` | **실물 자리** — 진짜 모델로 0.4.x 스키마를 재현해 이미 쌓인 안건·줄이 `track='memo'` · 계보 빈 목록으로 차는 것을 본다 |

**고치기 전 코드에서 넷 다 실패하는 것을 확인했다.** 검수가 「이 자리를 거는 테스트가 없어서 두 판이
지나도록 아무도 몰랐다」고 한 그 구멍이 이것으로 막혔다.

`tests/unit/` 에 두려다 `test_test_pyramid.py` 가 잡았다 — 단위 시험은 데이터베이스를 건너지 않는다.
`schema_sync` 는 본질이 데이터베이스라 `tests/contract/` 가 맞는 자리다.

### 안 한 것

- **사용자 DB(`ax_demo`)에 `plan()` 도 `apply()` 도 돌리지 않았다.**
- **이관 코드 없음** — `OQ-320` 은 사용자가 정하는 중이다. 다만 이 고침으로 「`track IS NULL` 인
  기존 행」이라는 자리가 애초에 생기지 않는다 (§6).
- 인덱스 교체는 손대지 않았다 — 「잃을 수 있는 것」이라 그 도구의 설계상 사람 몫이다.

---

## 9. 하지 않은 것 (경계 확인)

- **충돌 판정 미유입** — `merge_conflicts` 류 필드·API·판정 로직 **0건** (`OQ-308`).
- **프론트 무수정** — `frontend/` 를 한 글자도 고치지 않았다. 앞선 프론트 워커의 미커밋 산출물
  30여 파일은 **스테이징하지 않았다** (`git add` 에 경로를 하나하나 지정했고 `git add .` 도
  `git stash` 도 쓰지 않았다).
- **사용자 로컬 스택 무접촉** — API·워커·postgres 를 죽이거나 재시작하지 않았고
  `sync-demo-schema` 도 돌리지 않았다 (§6).
- **이관 코드 없음** (`OQ-320`).
- **가짜 데이터 없음** — 테스트가 쓰는 이름은 기존 픽스처의 `mina`·`jiho`·`sora` 그대로다.
- **push·PR·배포 없음.** 커밋 `51ecceb` 하나만 로컬에 있다.
