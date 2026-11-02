# 검수 — 백엔드 「두 벌 뼈대」 (SPEC-004 v0.5.1 · 커밋 `51ecceb`) · 2026-09-14

검수자: reviewer (read-only). **코드도 문서도 한 글자 고치지 않았다.**
대상: `51ecceb` 하나. 정본: `spec-004-meeting-note.md` v0.5.1 (`§4.0`·`§4.1`·`§4.2`·`§7`·`§8`·`§10`·`§11.4`).
근거는 전부 내가 읽은 줄과 내가 돌린 것이다 — 워커 보고의 「했다」는 하나도 그대로 받지 않았다.

---

## 0. 판정

**조건부 PASS — FAIL 1 · WARN 4 · nit 1.**

아홉 갈래는 **아홉 다 닫혔다.** 조용히 통과할 자리로 짚어 준 다섯(개명 미발생 · `source` 의 `ai` 은퇴 ·
예외 분기 통삭 · `or lines` 폴백 · `clear_track` 안건 삭제)은 **다섯 다 제대로 닫혀 있다.**
**계보는 저장에 살아남는다** — 내가 따로 짠 시나리오 넷으로 확인했다(§3).

FAIL 하나는 **아홉 갈래 밖에서 났다**: 벌 축이 생기면서 «이전 회의 맥락»을 싣는 두 자리가
세 벌을 다 싣게 됐는데 아무도 track 을 걸지 않았다. 계약이 그 자리에 요구하는 것은 **최종 벌 하나**다.

---

## 1. 아홉 갈래 대조표

| # | 갈래 | 확인한 자리 | 판정 |
|---|---|---|---|
| ① | 안건에 벌 축 · `source` 를 사람 벌 안으로 · `ai` 값 은퇴 | `domain.py:78-88` (`TRACK_MEMO/AI/FINAL`·`AGENDA_TRACKS`·`LINE_TRACKS = AGENDA_TRACKS`·`ORIGIN_TRACKS`) · `domain.py:106` `AGENDA_SOURCES = {manual,set,carried,derived}` · `domain.py:155` `ensure_agenda_source(value, *, track)` 가 사람 벌 밖의 출처를 **거절** · `persistence.py:368` `track` 열 · `:377` `source` nullable | **PASS** |
| ② | AI 가 사람 안건에 줄을 안 붙인다 (D14 폐기) | `application.py:1277 replace_ai_track` — `existing.get(output.agenda_id)` 경로가 없다 · `schemas/ai_batch_output.json` 에 `agenda_id`·`source` **0건**(전문 확인) · `batch.py` 전체에 `agenda_id` **0건** · `domain.py:170 ensure_line_track` 이 벌 불일치를 거절 · `application.py:524 write_memo` 가 사람 벌 아닌 안건을 거절 | **PASS** |
| ③ | 전량 교체의 「메모 줄이 매달린 AI 안건은 남긴다」 예외 삭제 | `platform/meetings.py:631 replace_track` — 본문이 `self.clear_track(meeting, track)` **한 줄**이다. 조건이 뒤집힌 것이 아니라 분기가 통째로 없다 | **PASS** |
| ④ | 합성이 최종 벌 전량 신규 · 원본 불가침 · 재시도가 안건까지 비운다 | `platform/meetings.py:588 clear_track` — 줄 → 후보 → **안건** 순서로 지운다(0.4.x 는 줄만) · `application.py:665 commit_finalized` 가 `clear_track(FINAL)` 뒤 언제나 `_create_agenda(track=FINAL)` · 내 probe 4 가 실측 확인(§3) | **PASS** |
| ⑤ | 자리표시 제목을 AI 가 채우던 것 폐기 (D48) | `application.py:67 QUICK_START_AGENDA_TITLE = ""` · `replace_ai_track` 에 `title_placeholder` 분기 **0건**(`grep title_placeholder` 는 생성·응답·사람 편집 자리만 남음) | **PASS** |
| ⑥ | 종료 뒤 상세가 세 벌 전부 · 내보내기는 최종 벌 | `application.py:1584 _detail` 의 `agendas` 가 **track 필터 없이** 전량 · `application.py:831 export` 가 `agenda["track"] == TRACK_FINAL` 로 거른다. **`or lines` 폴백은 src 전역에 0건**(grep) | **PASS** |
| ⑦ | 줄의 벌 표기 | **개명이 일어나지 않았다.** `src/` 전역 `human` 54건은 전부 다른 도메인의 영어 산문("human confirmation" 등)이고 **트랙 리터럴로 쓰인 `human` 은 0건**이다. 안건과 줄이 `LINE_TRACKS = AGENDA_TRACKS` 로 **같은 집합**을 쓴다 (`domain.py:88`) — 한 벌을 두 이름으로 부르지 않는다. 되레 `tests/unit/test_meeting_domain.py:116` 이 `ensure_line_track("human", …)` 가 **거절되는 것**을 건다 | **PASS** |
| ⑧ | `can_edit_agendas` 벌별 셋 · `ai` 언제나 거짓 · **서버가 실제로 거절** | `policy.py:139 AgendaTrackGates(memo, ai, final)` · `:39-45` 상태 집합(정리 중은 어느 집합에도 없다) · `policy.py:245 _agenda_gates` · `application.py:1357 _agenda_target` 이 `gates[track]` 하나로 **409 를 던진다** · 응답은 `application.py:1566/1568`. **화면 힌트가 아니다** — `tests/contract/test_meeting_finalize.py:455-459` 가 종료에서 원본 두 벌의 제목·줄·삭제 셋 다 **409** 를 실제 API 로 건다. 내 probe 3 이 「진행 중」도 같은 방식으로 확인했다 | **PASS** |
| ⑨ | 최종 벌 저장이 줄 id 로 계보를 잇는다 (§8-9) | `commands.py:184 MeetingNoteLineInput(line_id: UUID\|None, text)` · `policy.py:58 normalize_final_line_rows`(글자 배열은 **받지 않는다**) · `platform/meetings.py:507 save_final_lines` 가 **다섯 갈래를 여기서 가른다**. 옛 `replace_lines`(delete → insert)는 코드에 없다 | **PASS** |

### 1.1 「조용히 통과하는 자리」 다섯 — 전수 재확인

| 자리 | 무엇을 봤나 | 결과 |
|---|---|---|
| 개명 미발생 | `grep -rn human src/` 54건 전수 육안 확인 | 트랙 리터럴 `human` **0건**. 안건·줄이 같은 이름 |
| `source` 의 `ai` 은퇴 | enum(`domain.py:106`) · 검증(`domain.py:155`) · 기본값(`application.py:999`·`1300`·`690` 이 AI·최종에 `source=None`) · 프롬프트(`batch.py`·`finalize.py` 에 `source` 지시 0건) · 스키마 두 벌 · 픽스처 | **전 계층에서 사라졌다.** `tests/unit/test_meeting_domain.py:267` 의 `"source": "ai"` 는 **스키마 위반을 거는 음성 단정**이다 |
| 예외 분기 | `platform/meetings.py:631` | **통째로 사라졌다.** 조건 뒤집기 아님 |
| `or lines` 폴백 | `application.py:831` | **폴백 없이** `track == final` 안건만 낸다. 최종 벌이 비면 빈다 |
| `clear_track` 안건 삭제 | `platform/meetings.py:588` | 줄 → 후보 → **안건**. probe 4 가 실측 |

---

## 2. 지적 목록

### F-1 · **FAIL** — 「이전 회의 맥락」이 세 벌을 다 싣는다 (track 이 안 걸렸다)

**자리**
- `backend/src/ax_workspace/modules/meetings/application.py:589-590` (`finalize_input`)
- `backend/src/ax_workspace/modules/meetings/application.py:1188-1189` (`warm_start_context`)

```python
carried = {
    "title": source.title,
    "agendas": [
        {"title": agenda.title, "concluded": bool(agenda.concluded)}
        for agenda in self._repository.agendas(source)      # ← track 이 없다
    ],
}
```

**근거**
- `platform/meetings.py:366 agendas(meeting, *, track=None)` — 「`track` 을 안 주면 **세 벌 전부**」다.
  이 두 줄은 `5e7a41d` 에서 **한 글자도 바뀌지 않았고**(같은 코드를 옛 판 `:556`·`:1098` 에서 확인),
  그때는 안건이 한 벌이라 맞는 코드였다. **벌 축이 생기며 조용히 틀린 코드가 됐다.**
- 계약: `§7.1` 첫 배치 행 = 「**이어진 이전 회의의 맥락(안건과 결론)**」. `§4.0-5` = 「**결론 표시가 서는 것은
  최종 벌뿐이다** — 사람 벌과 AI 벌의 안건은 결론 여부를 갖지 않는다」. 그러므로 이 자리가 실어야 하는
  것은 이전 회의의 **최종 벌 하나**다.
- 지금 도는 것: 이전 회의의 `memo`·`ai` 안건까지 실리고 **전부 `concluded: false` 를 달고 나간다** —
  §4.0-5 가 「갖지 않는다」고 한 값을 프롬프트가 **거짓으로 단정해서** 낸다. 목록이 최대 3배가 되고,
  AI 벌 안건은 이전 회의의 AI 가 매 회차 갈아 끼우던 중간 산물이라 맥락으로서의 값도 없다.
- **같은 파일이 바로 옆줄에서는 제대로 걸렀다** — `application.py:1204` 가 현재 회의 안건을
  `self._repository.agendas(meeting, track=TRACK_MEMO)` 로 싣는다. 두 자리만 빠진 기계적 누락이다.

**실측 — 돌려서 봤다**

이전 회의를 합성까지 끝내(사람 벌 1 + 최종 벌 1) 그것을 `carried_from_meeting_id` 로 이어받은 회의를
세우고 `warm_start_context` 를 읽었다:

```
CARRIED AGENDAS IN WARM START:
  [{'concluded': False, 'title': '첫 안건'},        ← 이전 회의의 **사람 벌** 안건
   {'concluded': False, 'title': '이전 최종 안건'}]  ← 이전 회의의 **최종 벌** 안건
```

**사람 벌 안건이 「이전 회의의 결론」으로 프롬프트에 실린다.** AI 벌이 있는 회의였으면 셋이 된다.

**왜 FAIL 인가** — 계약이 「최종 벌」이라고 말한 자리에 세 벌이 간다. 응답 계약이나 저장 데이터가 아니라
**프롬프트 입력**이라 폭발 반경은 작지만, 「계약과 다른 것이 돈다」에 해당한다.
**테스트 0건** — `carried_from` 이 붙은 회의로 배치·합성을 돌리는 시험이 없어 앞으로도 안 잡힌다.
(위 실측은 내가 검수용으로 따로 짠 probe 다.)

### F-2 · **WARN** — 프론트 계약 전수에 「`ai_batch` 스트림 페이로드 축소」가 빠졌다

**자리** `application.py:1332` (`replace_ai_track` 의 return)

```python
# 지금 (51ecceb)
return [self._agenda_view(a, lines, todos) for a in self._repository.agendas(meeting, track=TRACK_AI)]
# 전 (5e7a41d:1237)
return [self._agenda_view(a, lines, todos) for a in self._repository.agendas(meeting)]
```

이 반환값이 `bootstrap/application.py:532 → :546 schedule_push_ai_batch → stream_service.py:169
push_ai_batch_threadsafe` 로 그대로 SSE 에 실린다. 즉 **회의 중 스트림 이벤트가 「세 벌 전체 트리」에서
「AI 벌만」으로 줄었다.** 계약상은 맞다 (`§7.1` 적재 행 — 「화면은 회차마다 **AI 벌을** 통째로 다시 받아
다시 그린다」). 문제는 **워커 보고 §4「깨진 프론트 계약 전수」에 이 항목이 없다**는 것이다.
화면이 이 이벤트로 `agendas` 를 통째로 갈아 끼우고 있으면 배치가 한 번 돌 때마다 사람 벌이 화면에서
사라진다 — 다음 바퀴 발주서가 이것을 모르면 그 자리를 못 고친다. **목록에 한 행 더해야 한다.**

### F-3 · **WARN** — `§8-5`「이미 승격된 것은 남긴다」가 구현에도 테스트에도 없다

**자리** `platform/meetings.py:588 clear_track` — 최종 벌 안건의 `MeetingTodoRecord` 를
**승격 여부와 무관하게** 지운다. 그 결과 `platform/meetings.py:~700 replace_todos` 의
「승격된 후보는 유지한다」 로직은 **최종 벌에 대해 죽은 코드**다.

이것은 워커가 게이트로 올렸고 코디가 **갈래 ③(도달 불가로 두고 전제를 코드에 남긴다)** 을 골랐다.
**나도 도달 불가를 확인했다** — `domain.py:55 MEETING_TRANSITIONS` 에 `(DONE, SUMMARIZING)` 이 없고,
`policy.py:ensure_todo_actionable` 이 `provisional=True` 를 막아 「실패」 회의의 배치 후보는 승격되지 않는다.
그래서 지금은 사고가 아니다. 다만 **계약 문장은 §8-5 에 그대로 서 있고, 그것을 거는 테스트가 사라졌다**
(`test_a_second_merge_keeps_the_candidates_that_were_already_requested` 삭제).
SPEC 다음 판이 §8-5 를 정정하거나(최종 벌 재작성에는 이 규칙이 걸리지 않는다) 예외를 정해야 한다.

### F-4 · **WARN** — `can_add_agenda` 의 응답 모양을 워커가 정했다

**자리** `policy.py:205` · `application.py:1568`. 계약이 «모양»을 정한 것은 `can_edit_agendas` 하나다
(`§3.3` · `§4.1-6` 판정 필드 열). 워커가 `can_add_agenda` 도 벌별 셋으로 만들었다.
`§4.1-6` 표의 「안건 추가」 칸이 이미 벌마다 다르므로 **값을 발명한 것이 아니라 표를 기계적으로 옮긴 것**이고
불리언 하나로는 「종료에 최종 벌은 더할 수 있고 사람 벌은 못 한다」를 낼 수 없다 — 판단은 옳다.
다만 **응답 계약이 하나 늘었으니** 스펙에 한 줄로 못 박아야 한다(지금은 코드가 정본).

### F-5 · **WARN** — 보고서의 테스트 수치가 실측과 다르다

| | 워커 보고 §7 | 내 실측 |
|---|---|---|
| 회의 테스트 파일 | 13개 | **14개** (`tests/unit/test_meeting_*.py` 7 · `tests/contract/test_meeting_*.py` 7) |
| 회의 테스트 수 | unit 64 · contract 205 | **unit 48 · contract 169 = 217 passed** |
| 전체 | 1226 passed · 2 failed | **1224 passed · 4 failed** (아래 §4) |

수치가 틀렸을 뿐 **초록이라는 결론은 같다.** 다만 보고를 읽는 사람이 「269개가 회의를 건다」로 읽게 되므로
정정이 필요하다.

### nit · 테스트 «이름»에 개명 잔재

`tests/unit/test_meeting_domain.py:82 test_agenda_source_vocabulary_is_closed_and_belongs_to_the_human_track_alone` ·
`tests/contract/test_meeting_memo_batch.py:393 …_never_touches_a_human_agenda` · 지역변수 `human_agenda`
(`test_meeting_memo_batch.py:403` · `test_meeting_finalize.py:429`).
벌 이름은 `memo` 인데 **테스트 이름만 `human` 을 쓴다.** 저장 값·응답·리터럴은 전부 `memo` 라 계약에는
영향이 없지만 「한 벌 한 이름」이 이름 축에서만 어긋난다.

---

## 3. 계보 시나리오 확인 결과 — **살아남는다**

워커 테스트를 믿지 않고 **내가 따로 네 갈래를 짜서 돌렸다**
(`scratchpad/test_reviewer_probe.py` — 검수용이라 리포에 남기지 않았다).

| probe | 무엇을 걸었나 | 결과 |
|---|---|---|
| **1** | 계보 든 최종 줄 **셋 중 가운데 하나만** 고쳐 저장 → 나머지 둘의 `from_lines` 가 사는가. 이어서 **세 번 더** 저장 | **통과.** `[[root0], [], [root2]]` 가 네 번째 저장 뒤에도 그대로. **줄 id 도 그대로**(새로 만들어진 것이 아니다) |
| **2** | 같은 `line_id` 를 **두 번** 실음 · **다른 최종 안건**의 줄 id 를 실음 | **통과.** 둘째 중복은 떨어지고 남의 줄도 그 줄만 거절, **저장 전체는 살고** 남의 줄은 제 안건에 그대로 |
| **3** | 「진행 중」 게이트가 **서버에서** 새는가 — 사람 벌 제목 PATCH · DELETE · 추가 POST · 참석자 시점 | **통과.** 제목 409 · 삭제 409 · 추가 201 · 참석자는 세 벌 전부 거짓. 응답 값과 서버 판정이 같다 |
| **4** | 재시도가 최종 벌 «안건까지» 비우고 원본은 그대로 두는가 (사람이 `[수정]` 에서 더한 최종 안건 포함) | **통과.** 1회차 최종 안건도 사람이 더한 최종 안건도 재시도 뒤 사라지고, 사람 벌 줄은 그대로 |

**판정: 「안건의 줄을 지우고 새로 만든다」로 짜여 있지 않다.** `save_final_lines`
(`platform/meetings.py:507`) 가 기존 레코드를 **찾아 이어 쓰고**, 본문이 달라진 줄에서만 `from_lines = []`
를 놓는다. 문서 검수 F-3 이 막으려던 자리가 실제로 막혔다.

워커 테스트 `test_saving_the_final_track_keeps_the_lineage_of_every_line_it_did_not_change`
(`tests/contract/test_meeting_finalize.py:795`)도 **다섯 갈래를 한 번에 + 두 번째 저장까지** 건다 —
빈 단언이 아니다.

---

## 4. 테스트 판정

```
cd backend && uv run pytest -n auto --dist worksteal
→ 4 failed · 1224 passed (278s)
```

### 4.1 신규 테스트가 «무엇을 거나» — 개명 추종인가, 벌이 갈렸다는 사실인가

읽은 결과 **개명 추종은 하나도 없다.** 근거로 셋만 인용한다.

- `test_meeting_memo_batch.py:393` — 2회차 배치 뒤 **AI 안건 id 집합의 교집합이 0**
  (`assert not first_round_ai_ids & {…}`) 이고 사람 벌 안건은 id·제목·줄이 그대로다.
  개명만으로는 절대 통과하지 않는다.
- `test_meeting_finalize.py:455-459` — 원본 두 벌에 제목·줄·삭제를 **API 로 던져 409 를 받는다.**
  `can_edit_agendas` 값이 아니라 서버 거절을 건다.
- `test_meeting_policy.py:88` — 여섯 상태 × 두 축 전수. 「진행 중은 더하기만」·「정리 중은 어느 벌도 아님」·
  `for status in MeetingStatus: assert add["ai"] is False` 까지 돈다.

### 4.2 테스트를 지우거나 약하게 고쳐 초록을 만든 자리

`git diff 5e7a41d 51ecceb -- backend/tests` 전수:
**삭제 5 · 신규 10 · assert −56 / +121.**

| 삭제된 테스트 | 판정 |
|---|---|
| `test_a_merge_survives_an_ai_agenda_the_batch_built_and_hung_its_own_lines_on` | 0.4.x 덮어쓰기 보장. **계약이 폐기한 것**이라 삭제가 맞다 |
| `test_a_memo_the_person_wrote_on_an_ai_agenda_is_not_swept_away_with_it` | 그 예외 분기 자체가 사라졌다. 삭제가 맞다 |
| `test_a_second_merge_keeps_the_candidates_that_were_already_requested` | **§8-5 문장은 살아 있는데 보장이 사라졌다** → F-3 |
| `test_agenda_source_vocabulary_is_closed_in_the_meeting_domain` | 더 센 것으로 교체(벌 경계까지 건다) |
| `test_note_lines_keep_meaningful_trimmed_sentences_in_order` | `test_final_line_rows_carry_their_id_…` 로 교체. 「글자 목록을 **받지 않는다**」를 더 건다 |

`test_codex_cli.py`·`test_meeting_finalize_service.py` 의 수정은 **고정값을 새 스키마로 옮긴 것뿐**이고
단언을 뺀 자리가 없다. **약화 0건, F-3 한 자리만 보장이 실제로 사라졌다.**

### 4.3 실패 분리

4건 전부 `material_*` — **이 커밋이 손대지 않은 파일**이다 (`git show --stat` 에 `material` 없음).

| 실패 | 판정 | 근거 |
|---|---|---|
| `test_report_material_search.py::test_report_discovery_is_not_limited_to_recent_ui_reports_and_keeps_long_body_tail` | **기존** · flaky | 단독 실행하면 통과 · `5e7a41d` 에서도 실패(아래) |
| `test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` | **기존** · flaky | 단독 실행하면 통과 · `5e7a41d` 에서도 실패(아래) |
| `test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result` | **기존** · flaky | 단독 실행하면 통과 · `5e7a41d` 에서도 실패(아래) |
| `test_material_folders.py::test_personal_and_team_folder_uploads_search_without_tasks_and_open_through_their_owner` | **기존** · flaky | 단독 실행하면 통과 · `5e7a41d` 에서도 실패(아래) |

```
uv run pytest <위 넷> -q → 4 passed (19s)
```

**변경 «전» 커밋에서 같은 명령을 돌린 결과** — 워커 보고의 「원래 그랬다」를 그대로 받지 않고
`5e7a41d` 를 별도 worktree(`git worktree add --detach`, 공유 워크트리 무접촉)에 떠서 전체를 돌렸다:

```
5e7a41d (변경 전)  → 4 failed · 1219 passed (292s)
   FAILED test_material_integrity_lifecycle.py::test_partial_search_requires_a_file_anchor_…
   FAILED test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_…
   FAILED test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result
   FAILED test_material_folders.py::test_personal_and_team_folder_uploads_search_…

51ecceb (변경 후) → 4 failed · 1224 passed (278s)
   위 넷 중 셋이 같은 이름이고, 나머지 하나는 같은 군의 다른 `material_*` 이다
```

**변경 전에도 같은 수·같은 군이 실패한다.** 실패 «집합»이 실행마다 조금씩 달라지는 것이
이 군이 flaky 라는 증거이고, 회의 경로는 양쪽 실행 어디에도 없다.
통과 수 차이 `1219 → 1224` 는 이번 커밋이 더한 테스트 수와 맞는다.
**회의 테스트는 217개 전부 초록이다.**

---

## 5. 프론트가 고쳐야 할 것 전수 — 워커 보고 대조

워커 §4 의 목록은 **정확하다.** 내가 백엔드 API 표면에서 센 것과 대조한 결과 **한 건이 빠졌다**(F-2).
`frontend/` 는 열지 않았고 — 발주 지시 그대로 — 아래는 전부 백엔드 diff 에서 센 것이다.

| # | 표면 | 무엇이 바뀌나 | 워커 보고 |
|---|---|---|---|
| 1 | `meeting.can_edit_agendas` | `boolean` → `{memo, ai, final}` (`application.py:1566`) | §4.2 ✅ |
| 2 | `meeting.can_add_agenda` | `boolean` → `{memo, ai, final}` (`application.py:1568`) | §4.2 ✅ |
| 3 | `agenda.track` | **신규** (`application.py:1730`) — 화면이 세 벌을 가르는 유일한 축 | §4.3 ✅ |
| 4 | `agenda.merged_from` | **신규** `string[]` (`application.py:1739`) | §4.3 ✅ |
| 5 | `line.from_lines` | **신규** `string[]` (`application.py:1722`) | §4.3 ✅ |
| 6 | `agenda.source` | `"ai"` 은퇴 · AI·최종 벌은 **`null`** (`application.py:1736` · `persistence.py:377`) | §4.4 ✅ |
| 7 | 빠른 시작 안건 `title` | `"안건 1"` → `""` (`application.py:67`) | §4.4 ✅ |
| 8 | `GET /api/meetings/{id}` 의 `agendas` | **세 벌 전부**가 한 목록으로 온다 (`application.py:1584`). `order` 가 **벌 안에서 1부터** 다시 매겨진다 (`platform/meetings.py:375-380`) | §4.5 ✅ |
| 9 | `GET /api/meetings/{id}/export` | `or lines` 폴백 제거 — 최종 벌이 비면 **빈다** (`application.py:831`) | §4.5 ✅ |
| 10 | `PATCH …/agendas/{id}` 의 `lines` | `string[]` → `{line_id?, text}[]`. 글자 배열은 **422** (`commands.py:184` · `policy.py:58`) | §4.6 ✅ |
| 11 | `PATCH …/agendas/{id}` | 원본 두 벌에 `lines` → **409** (`application.py:1069`) · 최종 벌 아닌 안건에 `concluded` → **409** (`application.py:1051`) | §4.6 ✅ |
| 12 | **SSE `ai_batch` 이벤트의 `agendas`** | **세 벌 전체 트리 → AI 벌만** (`application.py:1332`, 옛 `5e7a41d:1237`) | **❌ 빠졌다 → F-2** |
| 13 | MCP `meeting_agenda_update` 입력 스키마 | `docs/unified-operations-inventory.json` 재생성(그 도구 항목 하나만 — 내가 diff 전수 확인) | §4.7 ✅ |

---

## 6. 범위 — 새지 않았다

| 확인한 것 | 방법 | 결과 |
|---|---|---|
| 충돌 판정 미유입 (`OQ-308` · D-3) | `grep -rni "merge_conflict\|conflict" modules/meetings/ platform/meetings.py` | `merge_conflicts` 류 필드·API·판정 로직 **0건.** 남은 `*Conflict` 는 전부 기존의 `MeetingStateConflict`·`MeetingVersionConflict`·예약 멱등·스트림 close code 다 |
| `OQ-320` 임의 결정 없음 | `git show 51ecceb -- backend/src \| grep "UPDATE meeting\|backfill\|migrat"` | **0건.** 이관 코드 없다 |
| 프론트 무수정 | `git show --stat 51ecceb -- frontend` | **출력 0줄.** 커밋 20 파일이 전부 `backend/` + `docs/unified-operations-inventory.json` |
| 프론트 워커 미커밋 산출물 혼입 | `git show --stat 51ecceb` 전수 | `frontend/` **0건.** 워크트리의 미커밋 프론트 변경은 커밋에 들어가지 않았다 |
| 사용자 로컬 스택 | `sync-demo-schema` 실행 흔적 · 보고 §6 | 돌리지 않았다고 보고했고 커밋에도 자국이 없다 |

**스키마가 기존 행에 하는 일** — 워커 보고 §6 의 결론(`schema_sync` 가 `ADD COLUMN <type>` 만 내므로
기존 `meeting_agendas` 행의 `track` 이 `NULL` → 세 벌 필터 어디에도 안 걸림)은 `persistence.py:368`
(`server_default text("'memo'")`)와 `schema_sync` 의 성질로 설명이 일관된다. **`OQ-320` 이 정할 한 줄**로
좁혀진 것이 맞다. 나는 사용자 postgres 를 건드리지 않았으므로 실측하지 않았다.

---

## 7. 코디가 가져갈 것

1. **F-1 을 이번 바퀴에서 닫아라** — 두 줄에 `track=TRACK_FINAL` 을 거는 일이고, 그 회의로 배치·합성을
   돌리는 테스트가 하나도 없으니 시험도 함께 필요하다.
2. **F-2 를 프론트 발주서에 한 행 더해라** — 스트림 이벤트가 AI 벌만 싣는다.
3. **F-3·F-4 는 스펙 다음 판으로** — §8-5 승격 후보 문장 정정, `can_add_agenda` 모양 못 박기.
4. 스펙 `§4.0-2`·`§11.4` 마지막 행의 `human` 표기를 `memo` 로 정정해야 한다(사용자 결정 2026-09-14).
   구현은 이미 `memo` 이고 정본만 어긋나 있다.

*검수용 probe 는 `scratchpad/test_reviewer_probe.py` 에 있고 리포에 남기지 않았다.
검증용으로 만든 baseline worktree 도 정리했다.*
