# 코드 검수 — WORK-012 2루프 (E-2 · E-3 · E-4 FE · E-6 BE)

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: 코드 워크트리의 **`cc5d46d` 뒤 미커밋 변경 전부** — 22파일(+543/−161) · 새 파일 3(`shellDownloads.ts` · `roomSelectTestKit.ts` · `test_e6_ax_draft_save_repro.py`)
- 근거: `e2e-feedback-batch-1.md`(E-2·E-3·E-4·E-6 · E-6 결정 갱신 = AX 도 `save_draft` → 같은 카드 다음 회차) · `fe-loop2-report.md` · `be-loop2-e6-report.md` · `be-loop2-e6b-report.md`
- 한 일: diff 읽기 · `rg` 재확인. **시험·빌드·앱은 돌리지 않았다** — 워커 수치: FE 124 + 인접 117 · BE 404 + 159(흔들림 1) · postgres 51
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/`

---

## 0. 판정 — **WARN**

E-2 · E-3 · E-4 · E-6 모두 사용자 결정대로 구현됐다. 그 밖도 확인했다:
- 셸·계약 무변경
- E-6 병합 규칙이 사람 저장·확정에도 같이 걸리면서 기존 화면 동작을 깨지 않는다 — 화면이 칸을 «빼서» 비우는 자리는 다시 찾아도 없다
- 위임 턴의 확정·거절은 여전히 막힌다

**FAIL 0 · WARN 5.** 무거운 것은 하나다 — E-6 의 「목록 칸 = 전체 교체」.
- AX 가 「참석자 추가해 줘」 를 **새 사람만 담아** 보내면 기존 참석자가 조용히 빠진다.
- 규칙은 프롬프트(「목록 전체를 보내라」)에만 있고 서버는 막지 않는다.

---

## 1. E-2 앱 받기 진행 표시 (FE)

| 물음 | 본 것 | 판정 |
|---|---|---|
| 짝짓기 순서 | `F/lib/shellDownloads.ts` `settle` `:45-50` — 성공 사건의 이름이 진행 중 이름(또는 셸 번호 「이름 (n).ext」 를 뗀 이름 `baseName` `:41`)과 같으면 그것 → 아니면 **가장 오래된** 것 → 60초 타이머 `:20,:66` | PASS |
| 웹 무변경 | `startShellDownload` 가 `hasShell()` 이 거짓이면 아무것도 안 함 `:62` · 링크·`href` 는 그대로(WP1 의 `?download=1` 같은 탭) | PASS |
| 「모두 다운로드」 여러 개 | `downloadAll` 이 항목마다 `startShellDownload(href, name)` · 사건마다 하나씩 걷힘(`InboxAttachments.tsx:107,131`) | PASS |
| 실패 토스트에도 걷히나 | 실패 사건(이름 없음) → 가장 오래된 것을 걷는다 | PASS |
| 셸 무변경 · dmg 불필요 | `src-tauri/` diff 없음 · 기존 사건(`strong-hajin:download`)만 듣는다(`lib/shell.ts:232-243` `onShellDownload`) | PASS |
| 자리 | `DownloadLink` `:46-64`(파일 카드·PDF·메일 첨부·메일 이미지 받기 `MailView.tsx:420`) · `Thumb` 위 원 `:210` · `.scax-thumb__busy` `inbox.css:332` · `aria-busy`·「… 받는 중」 | PASS |
| 짝이 어긋나는 갈래 | 셸 사건은 **회의록 내보내기 등 다른 받기에도 같은 이름으로** 온다. 첨부를 받는 중에 내보내기가 끝나면, 이름이 안 맞아 「가장 오래된」 첨부 스피너가 먼저 걷힌다. 같은 첨부를 받는 중 다시 누르면 받기는 두 번 나가고 스피너는 하나뿐이라 첫 사건에 걷힌다 | WARN(W-4 · 경미) |

---

## 2. E-3 회의실 = 드롭다운 (FE)

| 물음 | 본 것 | 판정 |
|---|---|---|
| 모양 | `F/features/meetings/RoomSelect.tsx:165-194` — DS `Select`<br>— 수정: 맨 위 「기존 — 회의실 N (변경 안 함)」(조회 실패면 「(확인 못 함)」) → 묶음 머리 「다른 회의실」(`group` — 구분선 자리) → 「회의실 예약 없음」 → 가능한 방<br>— 생성: 첫 줄·머리 없음 | PASS(참고: 구분은 선이 아니라 **묶음 머리 글자** 「다른 회의실」 — DS `Select` 의 `select-group`. 사용자 그림의 「─────」 와 모양이 조금 다르다) |
| 비활성+이유 | 기존 줄 `disabled` + `description`(이유) · 고른 채면 목록을 안 열어도 아래 한 줄 `:196` | PASS |
| 가용 없음 · 조회 실패 | 아래 안내 줄 · 실패 + [다시 시도] 그대로 · 고른 방 빠짐 · 불러온 방 이유 그대로 | PASS |
| 거절 뒤 `unset` | 값 `""` + 트리거 안내 「회의실을 골라 주세요」 | PASS |
| AX 제안 표지 | 수정 카드 라벨 옆 그대로(WP3 fix — `ActionMeetingUpdateCard`) | PASS |
| 네 자리 · 계약 | 부품 하나라 네 자리가 같이 바뀐다 · 값 모양(`RoomChoice`)·조회 조건·300ms·`onStatus`·409 처리 무변경 → `wp3-contract-fixed.md` 그대로 | PASS |
| 줄 글자 | 방 줄 = `room.name` 만(`:178`). SPEC-010 §2.2 그림은 「회의실 1 (6인)」 — **정원이 줄에 안 보인다** | WARN(W-3 · 경미) |
| DS 자동 검색칸 | 방이 8개를 넘으면 DS 가 검색칸을 세운다(`ds/Select.tsx:147` `SEARCH_THRESHOLD`) — 의도와 맞는지 앱 확인(FE 리포트 남은 확인 2) | 참고 |

---

## 3. E-4 AX 수정 카드 세로 배치 (FE)

| 물음 | 본 것 | 판정 |
|---|---|---|
| 원인 | `styles/ax.css:252` `.scax-actioncard>div{display:flex}` 가 카드 직속 칸 묶음을 가로 한 줄로 만들었다 — 맞는 진단 | PASS |
| 고침 | 칸 묶음을 `.action-task-content`(세로 격자 · `ax.css:375`) 안으로 — `ActionMeetingUpdateCard.tsx:209`. 한 줄은 날짜+시각만, 참석자·외부 참석자·회의실은 아래로 · CSS 추가 없음 | PASS — 코드로는 넘침 원인이 없어졌다. 폭 실측은 jsdom 한계로 앱 확인(E2E) |
| AX 생성 카드 | `.ax-draft-card__body{display:block}` 이 이미 직속 flex 를 덮는다 — 배치 변경 없음 · 회의실만 드롭다운 | PASS |
| 시험 | 칸 묶음이 `.action-task-content` 안 · 일정 줄에 참석자 없음 · CSS 규칙 지킴(새 2) | 보통(구조만 · 폭은 못 본다) |

---

## 4. E-6 AX 초안 수정 = `save_draft` (BE)

| 물음 | 본 것 | 판정 |
|---|---|---|
| 위임 턴: `save_draft` 만 통과 | `B/entrypoints/mcp.py` `_propose_action_item_command`: `ax.*` 항목에서 `save_draft` 는 **그 카드의 `allowed_commands` 에 있을 때만** 통과(없으면 `AX_DRAFT_SAVE_UNAVAILABLE`) · 그 밖 명령은 `AX_DECISION_REFUSED`. 위임 턴의 `save_draft` 는 `causation_ref="ax_turn:<id>"` 로 응용에 간다 | PASS |
| 병합 규칙 | `B/modules/actions/confirmation.py:187-213` `merge_creation_draft`<br>— 지금 회차를 `normalize_ax_draft` 로 펴고 보낸 칸만 덮는다<br>— `null` = 비우기(비울 수 없는 칸은 생성 검증 422)<br>— 목록은 통째 교체<br>— 회의 `location` 에 값이 오면 422<br>— 모르는 칸은 뒤의 생성 모델(`extra=forbid`)이 422<br>대상 = `task.create_self`·`work_request.create`·`meeting.reservation.create` | PASS(W-1) |
| 사람 저장·확정도 같은 규칙 · 기존 동작 | `action_center.normalize` `:598-613` 이 `draft` 가 올 때만 병합. 화면이 칸을 «빼서» 비우는 자리를 다시 찾았다:<br>— 업무 초안 수정 창 `WorkModals.tsx:5078-5092` = 빈 값 `null`·빈 목록 `[]` 명시<br>— 회의 초안 `AxDraftCard.tsx:601` = `{...contract.values, ...input}` 전체<br>— 확정은 전체<br>— 수정 카드는 계약상 바뀐 칸만(다른 종류)<br>→ **없음**. BE 시험 중 「칸을 빼서 담당자 없음 422」 를 보던 1건만 `null` 로 바뀌었다 — 의도된 계약 변경 | PASS |
| 첨부 유지 | `attachment_draft_ids` 를 안 보내면 지금 회차 선택을 잇는다 `action_center.py:639` · 곁 고침: 회의 초안 저장의 첨부 확인 주인 종류 `"task"` → `"meeting"`(`:1072`) — 옳은 수정 | PASS |
| 감사 `edited_by` | 회차를 열 때 `action_item_audit_events(event_type="draft_saved", payload={submission_version, edited_by: person\|ax, causation_ref?})` `:1086~` · AX 판정 = 문맥 `current_causation()` 이 `ax_turn:` 으로 시작 · 고친 것이 없으면 회차·기록 없음 | PASS(응답 미노출 — H-3) |
| 사유 노출(C) | `anticipated_tool_error`: 도메인 예외·위임 거절·입력 검증만 `ToolError("<코드>: <한 줄>")` 로 모델에 · 그 밖(프로그램 오류)은 그대로 「예상 못 한 실패」(traceback 유지) · 메시지 200자 상한 | PASS |
| 회차 번호 | 초안 1 → 사람 2 → AX 3(시험 `test_e6_ax_draft_save_repro.py` · 사람이 고친 제목·목적 유지) | PASS |
| 낡은 기준 | AX 의 `base_submission_version` 이 낡으면 거절 + 사유 → 다시 읽고 보냄(BE 미결 3) | PASS |
| 인벤토리 | `action_item_command` 설명 1항목 | PASS |

---

## 5. 사람 눈에 이상해 보일 자리

| # | 자리 | 무엇이 걸리나 |
|---|---|---|
| H-1 | **AX 에게 「참석자 추가」 → 기존 참석자가 사라진다** | 목록 칸은 통째 교체 — AX 가 새 사람만 보내면 기존이 빠진다. 프롬프트가 「목록 전체」 를 말하지만 서버 안전장치가 없다(W-1) |
| H-2 | **스피너가 엉뚱한 때 걷힌다** | 첨부 받는 중 회의록 내보내기가 끝나거나, 이름이 셸 저장 이름과 다를 때(셸이 이름을 다듬은 경우) 가장 오래된 받기가 먼저 걷힌다(W-4) |
| H-3 | **회차가 올랐는데 누가 고쳤는지 안 보인다** | 사람이 2회차를 만든 뒤 AX 가 3회차를 만들면 카드는 「초안 · 3회차」 만 보인다 — `edited_by` 는 감사 표에만 있고 응답(`rounds[]`)·화면에 없다(BE 미결 2) |
| H-4 | **드롭다운 줄에 정원이 없다** | 「회의실 1」 만 보여 인원 맞는 방인지 줄에서 모른다(가능 목록은 이미 정원으로 걸렀지만 크기 비교가 안 된다 · W-3) |
| H-5 | **드롭다운 팝오버가 서랍·모달에서 잘림** | 좁은 AX 서랍 · 모달 안 팝오버의 잘림은 코드로 확인 불가 — 앱 확인(FE 남은 확인 2·3) |

---

## 6. FAIL / WARN 목록(재발주용)

### FAIL — 없음

### WARN (5)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-1 | BE(+코디 판정) | `B/modules/actions/confirmation.py:187-213` · `B/platform/codex_cli.py` `AX_DRAFT_EDIT_RULE` | 목록 칸 전체 교체를 프롬프트로만 지킨다 — AX 가 더할 항목만 보내면 기존 항목이 조용히 사라진다(H-1) | ① AX 수정(`causation=ax_turn`)에서 목록이 **줄어들면** 거절 + 사유(「목록 전체를 보내라」) · 또는 ② 실물 확인(「참석자 추가」 1회)으로 충분하다고 코디가 판정 |
| W-2 | BE+FE | 회차 응답 `rounds[]` | `edited_by` 미노출(H-3) | 원하면 응답 한 칸 + 「AX 수정」 표지(BE 미결 2) — 2루프 밖이면 기록만 |
| W-3 | FE | `F/features/meetings/RoomSelect.tsx:178` | 방 줄에 정원이 없다(SPEC §2.2 그림 「회의실 1 (6인)」) | `label` 에 정원 · 또는 `description` 으로 |
| W-4 | FE | `F/lib/shellDownloads.ts:45-50` | 다른 받기(내보내기)의 사건·이름 불일치·같은 첨부 두 번 누르기에서 스피너가 엉뚱하게 걷힘(H-2) | 경미 — 60초 안전판이 있다. 내보내기 사건을 거르려면 셸 사건에 종류가 필요(셸 변경 → dmg) — 지금은 두어도 됨 |
| W-5 | 코디(실물) | E-3·E-4 | 팝오버 잘림 · 좁은 서랍 폭 · 검색칸 자동 · 받기 스피너 실물 | 앱 E2E 체크리스트(FE 리포트 「남은 앱 실물 확인」 1~3) |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - diff 전부
  - 셸 사건 계약(`lib/shell.ts`)과 짝짓기
  - `RoomSelect` 줄 구성과 DS `Select` 의 묶음·비활성·검색 규칙
  - 수정 카드 배치 원인·고침
  - E-6:
    - MCP 위임 갈림
    - 병합·잠금 칸·첨부 유지·감사 기록·사유 노출
    - 화면이 칸을 빼서 비우는 자리 전수(없음)
- **확인 안 한 것**
  - 시험·빌드·앱 실행(폭·팝오버·셸 실물)
  - `normalize_ax_draft` 의 회의 종류 처리 내부 — 워커 시험을 믿었다
