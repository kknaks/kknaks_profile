# 보고 — 「최종 회의록만 회의록이다」, 백엔드 · 2026-09-14

정본: `decision-final-is-the-note.md` (사용자 결정 2026-09-14). 커밋 `fa49c90`.

## 한 줄

넷 중 **셋이 서버 변경**이고(① 진행 중 사람 벌 편집 · ③ 빈 근거 거절 · ④ 승격 후보 조직 전체)
**②는 프론트에 있다** — 코디 결정 ② 대로 서버를 건드리지 않고 전수로 올렸다. `agendas()` 를 벌 없이
부르는 자리는 전수로 훑어 **넷 다 그대로가 맞다**는 판단과 근거를 §5 에 적었다.

**③이 제일 무거웠다.** 근거를 잃는 자리가 프롬프트도 스키마도 아니라 **합성 입력(재료)**이었다 —
`_track_view` 가 `evidence` 를 싣지 않아 모델이 자기가 이미 아는 구간을 못 보고 있었다.

---

## ① 임시 두 벌을 임시로 다룬다

**무엇을** — 사람 벌 안건을 「진행 중」에도 고치고 지운다. AI 벌은 그대로 언제나 거짓.

| 자리 | 무엇을 했나 |
|---|---|
| `modules/meetings/policy.py:45` `MEMO_AGENDA_EDITABLE_STATUSES` | `{예정, 취소}` → **`{예정, 진행 중, 취소}`** |
| `policy.py:48` `MEMO_AGENDA_ADDABLE_STATUSES` | 더하기와 **같은 집합**이 됐다 (전에는 더하기만 「진행 중」이 있었다) |
| `policy.py:26-44` 게이트 표 주석 | 왜 열렸는지를 적었다 — 사람 벌은 최종 회의록을 지을 **임시 재료**이고, 0.4.x 의 잠금은 「원본이 최종본처럼 잠겨 있던 때」의 규칙이다 |

**「매달린 메모가 갈 곳을 잃는다」는 어떻게 되나** — 0.4.x 가 잠근 이유였다. 답은 이미 계약에 있다:
**안건을 지우면 같은 벌의 줄이 함께 지워진다** (§4.1-10). 사람이 자기가 적은 것을 지우는 것이고,
최종 회의록은 재전사문 위에서 새로 지어지므로 그 삭제가 회의록을 깨지 않는다.

**바뀌지 않은 것 셋** — 「정리 중」은 여전히 어느 벌도 열지 않는다(합성이 그 재료를 읽는 중이다) ·
「종료」·「실패」에서 원본 두 벌은 여전히 읽기 전용이다(그때는 최종본을 대조하는 근거다) ·
**결론 표시는 여전히 최종 벌에만** 있다(§4.0-5 — 임시가 열렸다고 최종의 값이 사람 벌로 오지 않는다).

`AI_AGENDA_*_STATUSES` 는 빈 집합 그대로다.

---

## ② 최종만 「회의록」의 자리를 갖는다 — **서버 변경 0** (코디 결정 ②)

### [다음 회의 예약]

**서버에 딛을 자리가 없다.** 게이트로 올려 ②를 받았다.

- `MeetingDetailPage.tsx:1127` 이 상세 응답의 `record.agendas` 를 **벌로 거르지 않고**
  `.filter(!concluded).map(title)` 해서 `BookingModal` 에 넘긴다.
- 모달은 `POST /api/meetings` 에 **제목 글자만** 싣는다 (`agendas: [{title}]`).
- 서버는 `carried_from_meeting_id` 를 받아 그 제목들에 `source='carried'` 를 달 뿐,
  **그 제목이 어느 벌에서 왔는지 알 방법이 없다** — 글자뿐이다.

상세 응답이 이미 `track` 을 싣고 있으므로 프론트가 `.filter(track === 'final')` 한 줄을 더하면
끝난다. 새 엔드포인트를 세우는 것은 §4.1-11(「담아 예약 모달을 연다」까지만 정했다)에 없는 발명이라
하지 않았다. → §6 깨진 프론트 계약 1번.

### 안건 한도

**서버는 이미 벌마다 센다** — 지난 판에서 고쳤고 이번에 테스트로 걸었다.

- `domain.py:140 ensure_agenda_capacity` — **벌 하나**가 이고 있는 수를 본다
- `application.py:997 add_agenda` — `agenda_count(meeting, track=track)` 을 넘긴다
- `application.py:298 _validated_creation` — 예약 모달의 드래프트를 세는 자리이고, 그 안건은 전부
  사람 벌에 서므로 벌별 셈과 같다

합산으로 세는 자리는 **서버에 없다.** 실측에서 보신 `agendas.length >= 20` 은
`MeetingDetailPage.tsx:1031` 의 프론트 셈이다. → §6 깨진 프론트 계약 2번.

### 메모 대상 드롭다운 (조사 근거 2)

**서버는 이미 거절한다** — `write_memo` 가 `ensure_line_track(TRACK_MEMO, agenda_track=…)` 로
사람 벌이 아닌 안건을 422 로 막는다(지난 판). 드롭다운이 AI 안건을 **보여 주는 것**이
`MeetingDetailPage.tsx:1052` 다. → §6 깨진 프론트 계약 3번.

---

## ③ 근거 없는 최종 줄을 거절한다

**근거를 잃는 자리를 찾았다 — 합성 입력이었다.**

실측이 「최종 9줄 중 2줄이 근거 0개인데 같은 문장이 AI 벌에서는 근거 1개를 갖고 있었다」였다.
AI 벌 줄은 자기가 딛는 구간을 **이미 원장에 갖고 있는데**, 합성에 넘기는 재료가 그 값을 싣지 않았다:

```
application.py:1813 _track_view  →  {line_id, agenda_id, text, at_ms}      # evidence 가 없다
```

그래서 모델은 다시 쓸 때 그 구간을 **세션 기억에서 되살려야** 했고, 못 살리면 빈 근거를 냈다.
프롬프트가 「없는 구간을 지어내지 마라」라고만 말하고 있었으므로 **비우는 쪽이 안전한 답**이었다.

### 세 자리를 함께 고쳤다

| # | 자리 | 무엇을 |
|---|---|---|
| 1 | `application.py:1813 _track_view` | **`evidence` 를 싣는다.** 나가는 이름(`start_ms`·`end_ms`)으로 옮겨 실어 응답과 같은 모양으로 읽히게 했다 |
| 2 | `schemas/ai_final_output.json` `lines[].evidence` | **`minItems: 1`.** 설명에 「재료로 받은 AI 벌 줄의 `evidence` 를 그대로 이어 적어라 · 하나도 없으면 그 시도 전체가 실패한다」를 적었다 |
| 3 | `finalize.py:157 _bind_evidence` | 근거 결박 **뒤에** 빈 줄이 남으면 `SchemaViolation` — 지어낸 구간이 떨어져 나가 빈 것도 같이 잡힌다 |
| 4 | `finalize.py:271 _FINAL_INSTRUCTIONS` | 「반드시 단다 · AI 벌 줄의 것을 그대로 이어 적어라 · 사람 벌 줄은 `at_ms` 무렵의 구간이다 · 지어내면 떨어져서 거절된다」 |

**줄을 버리지 않고 그 시도를 실패시킨다.** 버리면 사람이 적었고 AI 가 옮긴 내용이 아무 말 없이
사라진다. 실패는 세 번까지 다시 걸리고(§8-8) 그 재시도가 근거를 붙일 기회다. 재료가 이제 근거를
싣고 있으므로 모델은 **이어 적기만 하면 된다.**

**회의 중 배치(AI 벌)는 그대로 관대하다** — 근거를 잃어도 본문이 산다 (§7.1 검증). 결정이 말하는
것은 최종 회의록 하나이고, AI 벌은 임시 재료라 같은 잣대를 댈 자리가 아니다.

---

## ④ 승격 담당 후보는 조직도 전체

**새 표면 하나** — `GET /api/meetings/{meeting_id}/promotion-candidates`.

| 자리 | 무엇을 |
|---|---|
| `platform/organization_access.py:888 meeting_promotion_candidates` | 활동 중 + **답할 수 있는** 사람 전원. 참석자 먼저, 그다음 이름 순 |
| `modules/meetings/application.py:787 promotion_candidate_attendees` | 참석자 목록 + **여는 판정**(승격과 같다 — 참석자 전원) |
| `bootstrap/application.py:2837 meeting_promotion_candidates` | 회의 쪽에서 판정을 지나고 조직 쪽에서 사람을 낸다 |
| `entrypoints/http.py:750` | 라우트. 응답은 기존 `CandidateResponse`(`id`·`display_name`) 그대로 |

**무엇을 걷었나** — `task_assignment_candidates` 가 걸던 셋이다.

| 걸리던 것 | 왜 승격에는 안 걸리나 |
|---|---|
| `scope_for(TASK_ASSIGN)` 범위 | **요청 주체가 회의(시스템)다** (D40). 누른 사람이 부탁하는 것이 아니라 그 회의에서 나온 일로 기록되므로 그 사람의 배정 권한을 타지 않는다 — §9-5 의 「시스템이 보내므로 담당 후보에 조직 경계 제한이 없다」 |
| 본인 제외 | **누르는 사람 자신이어도 된다** (§9-5) |
| `task.self_manage` | **받은 사람이 수락해야 업무가 선다** — 그 판단이 그 사람 몫이라 우리가 미리 걸러 줄 일이 아니다 |

**남긴 것 하나** — `_can_answer`(로그인이 있는가). 권한이 아니라 **도달 가능성**이다: 답할 수 없는
사람에게 요청을 보내면 그 요청은 영영 기다린다.

**`/api/task-assignment-candidates` 는 한 줄도 건드리지 않았다** — 그것은 업무 관리 규칙이고,
테스트가 그 사실을 건다(mina 는 `task.assign` 이 없어 그 엔드포인트에서 여전히 403 이다).

MCP 도구는 내지 않았다 — 화면 한 자리를 위한 조회이고 **AI 는 담당을 고르지 않는다**(§8.2).
`unified-operations-inventory.json` 에 `status: excluded` · `decision: E2` 로 사유·대안·재고 조건과
함께 올렸다.

---

## 5. `agendas()` 전수 — 벌 없이 부르는 자리

```
$ grep -rn "agendas(" src/ax_workspace/ | grep -v "def agendas"
```

| 자리 | 벌 | 판단 |
|---|---|---|
| `application.py:424` `apply_legacy_note` | `track=TRACK_MEMO` | ✅ 이미 걸려 있다 — 옛 회의록 글자를 사람 벌 줄로 옮기는 자리다 |
| `application.py:456` `cancel` | **없음** | ✅ **맞다.** 회의를 취소하면 회의록·안건·자료가 **함께** 사라진다 (§3.1-12). 세 벌 전부가 대상이다 |
| `application.py:577` `finalize_input` | **없음** | ✅ **맞다.** 바로 아래 `:593-594` 에서 `memo_agendas`·`ai_agendas` 로 **직접 가른다.** 합성은 원본 두 벌이 다 필요하고, 최종 벌은 이 시점에 비어 있다 |
| `application.py:593` `finalize_input` (이전 회의) | `track=TRACK_FINAL` | ✅ 지난 판 FAIL 을 고친 자리 |
| `application.py:834` `_detail_for_owner` | **없음** | ✅ **맞다.** 합성 잡이 자기 결과를 돌려주는 투영이고 상세 응답과 같은 모양이어야 한다 — §8-11 이 세 벌을 전부 내라고 한다 |
| `application.py:1195` `warm_start_context` (이전 회의) | `track=TRACK_FINAL` | ✅ 지난 판 FAIL 을 고친 자리 |
| `application.py:1210` `warm_start_context` (이 회의) | `track=TRACK_MEMO` | ✅ 사람이 예약으로 세운 안건을 맥락으로 싣는다 (§4.1-8) |
| `application.py:1338` `replace_ai_track` | `track=TRACK_AI` | ✅ push 가 실을 것은 AI 벌 하나다 |
| `application.py:1590` `_detail` | **없음** | ✅ **맞다.** §8-11 — 상세는 세 벌을 전부 낸다. 무엇을 그릴지는 화면이 `track` 으로 고른다 |

**고칠 것이 없었다.** 벌 없이 부르는 넷은 전부 「세 벌이 다 필요한」 자리다. 지난 판 FAIL 두 건은
**이전 회의**를 읽는 자리였고 이미 닫혀 있다.

같은 결로 훑은 이웃 하나 — `agenda_count()` 는 `add_agenda` 한 곳에서만 불리고 `track=` 이 걸려 있다.

---

## 6. 깨진 프론트 계약 전수

`frontend/` 는 한 글자도 고치지 않았다. **1~3 은 이번 결정이 새로 만든 것이 아니라 이번 결정이
드러낸 것**이고, 4~6 이 이번 서버 변경으로 새로 깨진 자리다.

| # | 자리 | 무엇이 | 무엇으로 |
|---|---|---|---|
| 1 | `MeetingDetailPage.tsx:1127` | `record.agendas.filter(!concluded)` 가 **세 벌을 다 담는다** — [다음 회의 예약] 모달에 5개가 간다(화면엔 2개) | `.filter((a) => a.track === "final" && !a.concluded)` |
| 2 | `MeetingDetailPage.tsx:1031` | `agendas.length >= 20` — **세 벌 합산**으로 한도를 센다. AI 벌이 차면 사람이 자기 안건을 못 세운다 | 사람 벌만 세고, 서버가 409 로 막는 것과 같은 셈이어야 한다 |
| 3 | `MeetingDetailPage.tsx:1052` | 메모 대상 드롭다운에 **AI 벌 안건이 뜬다.** 고르면 서버가 422 | `track === "memo"` 인 안건만 |
| 4 | `MeetingDetailPage.tsx:293` 부근 | 「진행 중」에 사람 벌 **[수정]·[삭제]가 서지 않는다** — 서버가 이제 연다 | `can_edit_agendas.memo` 를 그대로 읽으면 된다. 화면이 상태로 다시 추론하는 자리가 있으면 걷는다 |
| 5 | `api.ts:733 getTaskAssignmentCandidates` | 승격 모달이 **업무 배정 후보**를 쓴다 — 6명 중 2명, 배정 권한이 없으면 **403** | `GET /api/meetings/{id}/promotion-candidates` 로 갈아탄다. 응답 모양은 같다(`{id, display_name}[]`) |
| 6 | `MeetingDetailPage.tsx:703 orderedAssignees` | 참석자를 앞으로 끌어올리는 정렬 | **서버가 이미 그 순서로 낸다** — 그대로 둬도 무해하지만 중복이다 |

**형이 바뀐 응답 필드는 없다.** `can_edit_agendas`·`can_add_agenda` 는 지난 판에서 이미 벌별 셋이
됐고 이번 판은 **값만** 바뀌었다(진행 중 `memo: false → true`).

**새 엔드포인트 하나** — `GET /api/meetings/{meeting_id}/promotion-candidates`,
응답 `[{id, display_name}]`, 참석자 먼저. 여는 사람은 그 회의의 참석자다(아니면 404).

---

## 7. 새 테스트 — 무엇을 거는가

| 테스트 | 무엇을 거는가 |
|---|---|
| `test_meeting_core.py::test_the_host_may_stand_up_and_fix_and_drop_an_agenda_while_the_meeting_is_running` **(다시 씀)** | **진행 중 사람 벌 안건 삭제가 된다** — 제목을 고치고, 메모를 매단 뒤 지우면 그 줄이 함께 사라진다. **AI 벌은 같은 상태에서 고치기·지우기 둘 다 409** |
| `test_meeting_core.py::test_the_memo_track_is_edited_whenever_it_is_the_working_copy_and_locked_once_it_is_evidence` **(다시 씀)** | 여섯 상태를 훑어 **열렸다 닫히는 축**을 건다 — 예정·진행 중 열림 · 정리 중 닫힘 · 종료에 닫히고 최종 벌이 열림. 결론 표시는 진행 중에도 최종 벌만 |
| `test_meeting_core.py::test_the_twenty_agenda_limit_is_counted_per_track_not_across_the_three` **(신규)** | **한도가 벌마다 20이다** — 사람 벌 20 + AI 벌 20 = 40 이어도 사람 벌 한도는 사람 벌만 보고, 하나 지우면 한 자리가 난다 |
| `test_meeting_finalize.py::test_a_final_line_without_evidence_is_refused_and_the_attempt_fails` **(신규)** | **빈 근거 최종 줄이 거절된다** — 세 번 다 같은 답이면 「실패」이고 사유는 사람이 읽는 한 줄 |
| `test_meeting_finalize.py::test_a_final_line_whose_only_span_is_out_of_range_is_refused_too` **(신규)** | 스키마는 지나고 **근거 결박에서 떨어져 빈 것도** 거절된다. 근거가 둘인데 하나만 범위 밖이면 **그 근거만 떨어지고 줄은 산다**(그 결은 안 바뀌었다) |
| `test_meeting_finalize.py::test_the_synthesis_is_handed_the_spans_its_own_lines_already_stand_on` **(신규)** | **재료가 근거를 싣는다** — `finalize_input` 의 `ai_lines` 에 구간이 있고, 실제로 **나간 프롬프트에도** 그 값이 있다 |
| `test_meeting_finalize.py::test_promotion_candidates_are_the_whole_directory_with_the_attendees_first` **(신규)** | **승격 후보에 조직 전체와 본인이 있다**(6명 전원 · `mina` 포함) · 참석자가 앞 둘 · id·이름만 · 회의를 못 보는 사람은 404 · **업무 관리 목록은 여전히 403** · 배정 권한 없는 사람이 눌러도 승격이 선다 |
| `test_meeting_policy.py` (보강) | 진행 중 `can_edit_agendas.memo` 가 참. `ai` 는 여섯 상태 전부 거짓 |

시험 발판 하나 — `_line()` 의 `evidence` 기본값이 **실재하는 구간 하나**가 됐다. 「근거를 안 쓴
시험」이 곧 「거절되는 출력」이 되므로, 빈 근거를 일부러 보내는 시험만 `evidence=[]` 를 명시한다.

---

## 8. 테스트 결과

```
cd backend && uv run pytest -n auto --dist worksteal
→ 2 failed · 1236 passed (225s)
```

- **회의 테스트는 전부 초록이다** — `tests/unit/test_meeting_*.py` **48** · `tests/contract/test_meeting_*.py` **175** (합 223).
- 남은 2건은 **둘 다 `tests/contract/test_material_worker_recovery.py`** 이고 **내 첫 기준선(변경 전
  커밋, `6 failed · 1217 passed`)에 같은 이름이 있다.** 그 파일만 따로 돌리면 전부 통과한다 —
  병렬 부하에서 리스·시각 경합에 걸리는 flaky 이고 자료 경로를 한 줄도 건드리지 않았다.
- 내 변경으로 깨져서 **고친** 것 둘: `test_codex_cli.py`(최종 출력 고정값에 근거를 실었다) ·
  `test_operation_inventory.py`(새 라우트를 목록에 올렸다).

---

## 9. 하지 않은 것 (경계 확인)

- **충돌 판정 미유입** — `merge_conflicts` 류 필드·판정 로직 **0건** (`OQ-308`).
- **프론트 무수정.** 동시에 도는 프론트 워커의 미커밋 산출물과 그가 더한 `Makefile` e2e 타깃
  (`e2e-meeting-three-tracks`)은 **스테이징하지 않았다** — 경로를 하나하나 지정했고 `git add .` 도
  `git stash` 도 쓰지 않았다.
- **사용자 로컬 스택 무접촉** — API·워커·postgres·vite 를 죽이거나 재시작하지 않았고
  **DB 에 아무것도 돌리지 않았다**(`plan()`·`apply()` 포함).
- **`/api/task-assignment-candidates` 무수정** — 업무 관리 규칙은 그대로다.
- **표면 발명 없음** — [다음 회의 예약] 목록 엔드포인트는 게이트로 물어 ②(안 만든다)를 받았다.
- **push·PR 없음.** 커밋 `fa49c90` 하나만 로컬에 있다.

---

## 10. 열린 물음

1. **`OQ-318`(사람 벌 안건 전수 보존 강제)은 이 결정으로 성립하지 않는다** — 임시를 최종처럼 보존할
   이유가 없다. 결정 문서 §범위 밖이 그렇게 적었고, 코드에도 그 검사가 없다(지난 판에 이미 없었다).
   스펙 개정 때 종결 처리할 자리다.
2. **`todo.reference.line_ids` 가 여전히 원본 줄 id 를 가리킬 수 있다** — §8.2 는 「최종 후보는 최종
   벌 줄을 가리킨다」고 하는데 AI 는 저장 전이라 최종 줄 id 를 모른다. 0.4.x 부터 있던 자리이고
   이번 넷에 없어 손대지 않았다. 근거를 최종 줄에 묶는 일이 끝났으니 다음 판에 같이 볼 만하다.
3. **사람 벌 줄(메모) 자체의 수정·삭제는 이번 판에 없다** — 결정 §바뀌는 것 1 이 「메모·안건을 고치고
   지울 수 있다」고 했는데, 발주 ①은 **안건**만 지목했고 줄을 고치는 표면(`PATCH .../lines/{id}` 류)은
   계약에도 없다. 안건을 지우면 그 줄이 함께 사라지므로 「지우는」 길은 있다. 줄 하나를 따로 고치는
   자리가 필요한지는 기획·스펙 개정에서 정할 일로 남긴다.
