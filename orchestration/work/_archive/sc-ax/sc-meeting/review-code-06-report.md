# 코드 검수 6 — FE P4·소수정 + BE 후속(E1~E6) + WP-005

- 작성: 2026-09-10 / `reviewer_code` (read-only · 검수 1~5 와 같은 세션)
- 범위: `git diff 8397d8f..59e1102` — 커밋 넷(`9644e7c` FE P4 · `96d5312` BE 후속 · `ad4da8a` FE 소수정 · `59e1102` WP-005), 35파일 **+2,308 / −216**.
- **격리본으로 읽고 돌렸다.** FE P5 워커가 병렬로 `frontend/` 를 고치는 중이었다(실행 직전 워킹트리 10항목: `api.ts`·`AttachModal.tsx`·`ShareModal.tsx`·`styles.css`·`viewModels.ts` 수정 + `DropZone.tsx`·`FileList.tsx`·`shot_*.mjs` 신규). BE·FE 수치 **둘 다** `git archive 59e1102` 격리본 기준이고 `git stash` 는 쓰지 않았다(FE 는 실 `node_modules` 를 심볼릭 링크로만 빌려 썼고 검수 뒤 링크만 지웠다).
- **아무 파일도 고치지 않았다.** 워크트리·`.git` 변경 0.

---

## 0. 총평 — **PASS (WARN 4)**

**재발주할 것이 없다.** 네 커밋이 각자 맡은 것을 다 했고 서로를 깨지 않았다. 특히 세 가지가 눈에 띈다.

**① 근거 칩 NaN 의 뿌리를 한 자리에서 막았다.** AI 스키마는 안에서 `from_ms`/`to_ms` 로 말하고 화면 계약은 `start_ms`/`end_ms` 다 — `_evidence_span` 이 **나가는 자리 한 곳**(`_line_view`)에서만 옮기고, 저장은 받은 그대로 둔다. FE 도 계약 키만 읽고 숫자가 아니면 칩을 그리지 않는다. 양쪽이 각자 막았고 겹치는 것이 낭비가 아니다.

**② E1 드레인이 「기다리다 잃는 것」을 피했다.** `finish` 는 정상 종료에서만 부르고(`_failed is None`), 드레인이 어떻게 끝나든 **`finally` 에서 열린 블록을 적재한다.** 종료 프레임은 `_ended` 플래그로 한 번만 나가고, 상한 8초는 상수 한 곳이다. keepalive 도 오디오 경로와 경합하지 않는다 — 10초 무음일 때만 깨어나고 보내는 것이 **JSON 제어 메시지**라 오디오 바이트 순서에 끼어들 여지가 없다.

**③ E4·E6 이 기존 계약을 건드리지 않는 모양으로 들어왔다.** `eligible_member_ids: frozenset[str] = frozenset()` 는 빈 기본값이라 회의 밖 호출자가 그대로 돌고, 검사 순서도 기존 규칙을 마지막 폴백으로 남긴다. work 계약 테스트 5파일 회귀 0이 그것을 뒷받침한다.

검수 5 의 **W-a(D26 세 필드 FE 소비)는 닫혔다.** 새로 생긴 WARN 은 하나 — FE `MeetingLive.test.tsx` 의 `ai.batch` 케이스가 **부하를 타면 간헐적으로 깨진다**(7회 중 2회). 제품 코드가 아니라 테스트 헬퍼가 소켓 생성을 안 기다리는 문제이고, 고치는 자리는 한 줄이다.

---

## 1. FE P4 — **PASS**

| 확인 | 근거 |
|---|---|
| transcript 소비 · at_ms 축 | `MeetingDetailPage.tsx` 가 `readMeetingTranscript` 로 `items`/`memos` 를 받아 한 축에 섞는다 · `viewModels.ts:753` `at_ms: number \| null` |
| 근거 칩 → 탭 전환 + 하이라이트 | `MeetingDetailPage.tsx:791-800` — 칩이 `startMs/endMs` 를 들고 `marked` 와 비교해 `on` 을 켠다 |
| **promote 이음매가 다른 화면 무영향** | `WorkModals.tsx` 변경분이 +22줄뿐이고 **선택 prop 추가**다. 다른 화면의 기존 호출자가 그대로 돈다 — `tsc` 0 에러와 FE 52 통과가 뒷받침 |
| finalize 버그 수정 · export `<a href>` 하나 | `MeetingDetailPage.tsx:681` `<a className="btn" href={meetingExportUrl(...)}>` — 스크립트가 파일을 만들지 않는다 |
| title_candidate 표시·확정 | `viewModels.ts`·`labels.ts` 에 자리 · 상세가 「제목 없는 회의」 대신 후보를 내고 사람이 저장해야 제목이 된다 |
| 409 `meeting_agenda_stale` 처리 | `api.ts`·`MeetingDetailPage.tsx` 가 `current` 를 받아 현재 줄로 되그린다 |
| 작성자 표시 이름 | `personName` 경유, null 가드 유지(검수 5 W9 해소분 그대로) |
| **`can_write_memo`·`started_at` 소비 (W-a)** | `viewModels.ts:809`·`:812` — **검수 5 W-a 닫힘 ✓** |
| hex 리터럴 | `frontend/src/meetings`·`GutterList.tsx` 전수 **0건** |
| `api.ts` 밖 fetch | **0건** |
| 시안 밖 요소 | 신규 테스트 `MeetingAfter.test.tsx`(306줄)가 P4 표면을 덮고, `MeetingLive.test.tsx:355` 의 「AI 채팅·알림 없음」 부정 단정이 유지된다 |

---

## 2. FE 소수정 — **PASS**

| 확인 | 근거 |
|---|---|
| D31 벽시계(`started_at` + `at_ms`) | `labels.ts:603-608` `meetingWallClock` — 기준점과 오프셋으로 실제 시각을 만든다 |
| **NaN 가드** | `:604` `if (!startedAt \|\| typeof atMs !== "number" \|\| !Number.isFinite(atMs)) return ""` · `:606` `Number.isNaN(base)` · 호출부 `MeetingDetailPage.tsx:794` 가 `Number.isFinite` 로 한 번 더 거르고 `:796` 이 빈 라벨을 버린다. 「가리킬 수 없는 칩을 세우지 않는다」 |

---

## 3. E1~E3 — **PASS**

| 확인 | 근거 |
|---|---|
| `finish` 한 번만 | `platform/soniox.py:124-132` `_send_end` 가 `self._ended` 로 막는다 — 「더 올 오디오가 없다는 신호. 한 번만 보낸다」. 호출처도 하나다(`shutdown` → `_drain_upstream`, `_serve_upstream` 의 `finally` 에서 한 번) |
| **정상 종료에서만 드레인** | `stream_service.py` `shutdown` — `if self._upstream is not None and self._failed is None: await self._drain_upstream()`. 업스트림이 이미 끊긴 실패 경로에서는 기다리지 않는다(「기다릴 상대가 없다」) |
| **`finally` flush** | 같은 자리의 `try/finally` — 「드레인이 어떻게 끝나든 열린 블록은 적재한다 — 기다리다 잃는 것이 이 자리의 실패다」. `_drain_upstream` 안에서도 `SttUpstreamError` 를 삼키고 받은 데까지 남긴다 |
| 상한 8초가 상수 한 곳 | `modules/meetings/stream.py:53` `DRAIN_TIMEOUT_SECONDS = 8.0` — `stream_service` 와 `soniox_smoke.py` 가 같은 상수를 import |
| **keepalive 가 오디오 경로와 경합하지 않는가** | **PASS** — `_pump_keepalive` 는 `loop.time() - self._last_audio_at >= KEEPALIVE_IDLE_SECONDS`(`stream.py:55`, 10초) 일 때만 보낸다. 보내는 것은 `soniox.py:117-122` 의 **JSON 제어 메시지**(`{"type":"keepalive"}`)이지 오디오 바이트가 아니라, 청크 사이에 끼어도 **순서 보존이 깨지지 않는다.** `_feed` 가 매 청크마다 `_last_audio_at` 을 갱신하므로 오디오가 흐르는 동안에는 아예 깨어나지 않는다 |
| keepalive 가 세션을 잘못 끝내지 않는가 | `_upstream is None` 일 때만 조용히 `return`(그때는 이미 세션 종료) · `SttUpstreamError` 면 `_fail` 뒤 종료 — 둘 다 의도된 종료다 |
| **스모크가 키·본문을 출력하지 않는가** | **PASS** — `scripts/soniox_smoke.py` 의 `print` 는 셋뿐이고(`:111` 키 없음 안내 · `:116` 오류 코드 · `:118` receipt), receipt 는 `settled_before_end_frame`·`settled_after_end_frame`·`settled_tokens`·`provisional_tokens`·`last_end_ms`·`total_ms` **숫자뿐**이다. 전사 본문도 키도 나가지 않는다 |

> 코디 실물 E1(「드레인 후 transcript 2블록 301+34자, 41.4초」)과 일치한다 — 34자 꼬리가 end frame 뒤에 확정되는 구간이고, 그것이 이 수정이 지키려던 자리다.

---

## 4. E4~E6 — **PASS**

| 확인 | 근거 |
|---|---|
| `eligible_member_ids` **기본값 빈 집합** | `modules/work/requests.py:219` `eligible_member_ids: frozenset[str] = frozenset()` — 회의 밖 호출자는 인자를 안 줘도 같게 돈다 |
| 회의 경로만 참석자 ∪ 만든 사람 | `:229` `at_the_meeting = assignee_id in eligible_member_ids` · `:230` 이 `oneself` → `at_the_meeting` → **기존 `is_work_request_assignee`** 순으로 보므로 기존 규칙이 마지막 폴백으로 남는다. 「같이 앉아 있던 사람에게 일을 넘기는 것은 조직 경계를 묻는 자리가 아니다 — 그 밖은 기존 규칙 그대로다」 |
| 기준일 프롬프트 (E5) | `finalize.py:215` 「**아래 기준일로 환산해 YYYY-MM-DD 로** 적어라 — 환산이 서지 않으면 null 로 둔다」 · `:231`·`:253` 이 요일까지 싣는다(상대 날짜 환산에 필요) |
| 스탬프 title_candidate | `finalize.py:59`·`:104` — `FinalNotes.title_candidate` 를 스키마에서 받아 적재로 넘긴다 |
| 팀장 capability **한 줄** | `catalog.py` 에 `"work_request.create"` 한 줄 + 근거 주석(D30) |
| **뒤집은 테스트가 D30 을 명시** | `test_meeting_finalize.py:653`·`:717` — 「팀장도 회의에서 나온 일을 넘긴다 — 승격은 언제나 업무 요청이다 (**D30**)」 |

> 코디 실물 E4(참석자 승격 201)·E5(due ISO 환산)와 일치.

---

## 5. WP-005 — **PASS**

| 확인 | 근거 |
|---|---|
| **evidence 키 투영** | `application.py:1297-1305` `_evidence_span` — `start_ms`(없으면 `from_ms`)·`end_ms`(없으면 `to_ms`)로 옮기고 **`_line_view`(`:1192`) 한 곳에서만** 부른다. 줄이 나가는 자리가 그 하나라 detail 이 전부 덮인다. transcript(`items`/`memos`)와 export 는 줄 evidence 를 싣지 않아 어긋날 키가 없다(`export.py` 는 회의 정보·줄·다음 할 일 셋만) |
| 자료 4 라우트 | `http.py:930`(list) · `:940`(attach, 201) · `:968`(detach, 204) · `:979`(content) |
| 게이트 — 참석자 · in_progress 409 · 올린 사람 삭제 | `materials.py:163-170` `_writable` = readable + `is_attendee` + **in_progress 면 `MeetingStateConflict`**(409) · `:157-158` detach 는 `uploaded_by == principal.id` 아니면 `MeetingAccessDenied` → 404. 「회의를 만든 사람도 남의 자료를 못 뗀다」 |
| 열람 축 | `_gate.readable` 가 상세와 같은 축(참석·공유) — 코디 실물 「열람자 자료 삭제 404」와 일치 |
| 20MB · PDF/MD | `:26` `MAX_MEETING_MATERIAL_BYTES = 20 * 1024 * 1024` · `:129-134` 크기→`REASON_TOO_LARGE`, 형식→`REASON_UNSUPPORTED`(`accepts`) |
| **부분 성공 201 / 전부 실패 422** | `:139-142` — 하나라도 붙으면 `(attached, failed)` 를 201 로, 하나도 못 붙으면 `MeetingMaterialsRejected` → `http.py:961` `{"code": "meeting_materials_rejected"}` 422. 코디 실물(혼합 201 attached 1/failed 2 · 전부 실패 422)과 일치 |
| 저장 위치·응답에 storage key 없음 | `_view`(`:208`)가 binding·attachment 표면만 낸다 — 자료 모듈의 기존 규약 그대로 |
| `GET /shares` **basis** | `application.py:607-634` `viewers` — 참석(만든 사람 포함)은 `basis:"attendee"`, 공유는 `"share"`, 이미 참석인 사람은 공유 쪽에서 건너뛴다(`:625-626`). 「참석은 거둘 수 없고 공유만 거둔다」 |
| **중복 건너뜀** | `share_many`(`:636-650`) — `already = 참석 ∪ 만든 사람 ∪ 이미 열람` 에 들면 **조용히 건너뛴다**. 「알림은 가지 않는다」 |
| **참석자 삭제 409** | `revoke_share`(`:674-687`) — `:680-682` 대상이 참석자면 `MeetingStateConflict` → 409. 「참석을 빼는 자리는 회의 정보 편집이다」 |
| 검색 갈래 | `bootstrap/material_sources.py:104-130` — `MEETING_READ` + `readable_rows(principal)` 로 **열람 축**을 걸고, ① 회의에 붙인 파일과 ② `material_id_for(MEETING_TRANSCRIPT, meeting_id)` 로 **회의당 원문 하나**를 낸다. `resource_type == "meeting"` 이면 그 회의로 좁히고 못 열면 `MaterialNotFound` |
| **검색 회귀 0** | `test_material_search_public.py` 포함 198 통과 (§6) |

---

## 6. 회귀·경계 — **PASS (WARN 1)**

| 검사 | 결과 |
|---|---|
| BE (격리본, 1회) | **198 passed** (264.98s) — meeting_core · meeting_stream · meeting_memo_batch · meeting_finalize · **meeting_materials(신규)** · material_search_public · work 계약 5파일 · architecture. **실패 0** |
| FE `npx tsc --noEmit` (격리본) | **0 에러** |
| FE `npx vitest run src/meetings/` (격리본) | **52 tests** / 4 files — 첫 실행에서 **1 failed**, 이후 재실행에서 전부 통과 → **간헐 실패**(W-2) |
| 경계 | `modules/*` 의 fastapi·mcp·sqlalchemy·subprocess import **0건** · `create_all` 은 `bootstrap/reset.py` 하나 |
| 리포트 주장 vs 코드 | 일치. 검수 5 의 W-a 는 실제로 닫혔고, E1~E6 여섯 건이 모두 코드에 있다 |

### W-2 · WARN — FE `MeetingLive.test.tsx` 의 `ai.batch` 케이스가 간헐적으로 깨진다 (담당: FE, 테스트 한 줄)

- **증상**: `TypeError: Cannot read properties of undefined (reading 'accept')` — `MeetingLive.test.tsx:167` 의 `socket().accept()`.
- **원인**: `:101` `const socket = () => FakeSocket.instances[FakeSocket.instances.length - 1]` 가 **기다리지 않는다.** `connect()`(`:164-169`)는 `await screen.findByText("DB ax 전략")` 로 상세 렌더만 기다리는데, WS 는 그 뒤 별도 effect 에서 열린다. 부하를 타면 그 effect 가 아직 안 돌아 `instances` 가 비고 `undefined.accept()` 가 난다.
- **재현율**: 관측 7회 중 **2회 실패**(전체 4파일 첫 실행 · 단일 파일 첫 실행). 이후 단독 실행 1회 + 단일 파일 2회 + 전체 4파일 **5회 연속 52/52 통과**. 즉 **제품 코드가 아니라 타이밍**이다 — 실패한 두 번 모두 다른 작업 직후의 첫 실행이었다.
- **제품 결함이 아닌 근거**: 같은 파일의 나머지 13개가 언제나 통과하고, 실패가 단정 문장이 아니라 **헬퍼의 소켓 조회**에서 난다. `ai.batch` 렌더 규칙 자체는 통과할 때 정상 단정된다.
- **고칠 방향 한 줄**: `connect()` 에서 `socket()` 을 부르기 전에 `await waitFor(() => expect(FakeSocket.instances.length).toBeGreaterThan(0))` 를 넣는다(또는 `socket()` 자체를 `waitFor` 로 감싼다).
- **왜 지금 잡아야 하나**: 이대로 두면 CI 가 이유 없이 붉어지고, 다음 검수에서 「HEAD 실패인가 병렬 워커 탓인가」를 매번 다시 가려야 한다.

---

## 7. 코디 실물 대조 — 전부 일치

| 관측 | 코드 |
|---|---|
| E1 드레인 후 2블록(301+34자, 41.4초) | `shutdown` → `_drain_upstream`(정상 종료만) + `finally` flush · `DRAIN_TIMEOUT_SECONDS=8.0` |
| E4 참석자 승격 201 | `requests.py:229-230` `at_the_meeting` |
| E5 due ISO 환산 | `finalize.py:215`·`:253` 기준일+요일 |
| 근거 칩 NaN → `start_ms/end_ms` | `_evidence_span`(BE) + `Number.isFinite` 가드(FE) 양쪽 |
| 혼합 업로드 201(attached 1, failed 2 사유) | `materials.py:125-142` |
| 전부 실패 422 `meeting_materials_rejected` | `:139-141` + `http.py:961` |
| 진행 중 409 | `_writable` `:167-169` |
| shares basis | `viewers` `:615-633` |
| 참석자 삭제 409 | `revoke_share` `:680-682` |
| 열람자 상세 shared / `can_edit_info` false | 검수 2~3 에서 확인한 축 그대로 |
| 열람자 자료 삭제 404 | `detach` → `MeetingAccessDenied` → 404 |
| 검색 소유자·열람자 1건씩 | `material_sources.py:104-130` 회의당 원문 하나 |
| **W-a 해소** | `viewModels.ts:753`·`:809`·`:812` ✓ |

---

## 8. WARN 이월

| # | 자리 | 내용 | 담당 |
|---|---|---|---|
| **W-2**(새로 생김) | `frontend/src/meetings/MeetingLive.test.tsx:101`·`:167` | `ai.batch` 케이스 간헐 실패 — 헬퍼가 소켓 생성을 안 기다린다. 7회 중 2회. 테스트 한 줄 | FE |
| **W-1**(검수 5 이월) | `entrypoints/http.py:814` | 내보내기 거절이 422(`Literal["html"]`) — 브리프는 400 `unsupported_format`. **이번 범위에서 바뀌지 않았다.** 코드/브리프 중 하나를 맞추면 닫힌다 | 코디 결정 |
| **W-d**(검수 3~5 이월) | `platform/codex_cli.py` | 도구 필터가 CLI 의 `enabled_tools` config 에 산다. 서버 조립물이라 유효 — 기록만 | — |
| ~~W-a~~(검수 5) | `viewModels.ts` | **해소** — D26 세 필드(`at_ms`·`can_write_memo`·`started_at`)를 FE 가 소비한다 | ✅ |

---

## 9. 재발주 요약

**없다.** 남은 것은 테스트 한 줄(W-2)과 코디가 한 줄로 정할 W-1 뿐이다.
