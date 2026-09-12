# 코드 검수 3 — WP-002 스트림 중계 + WP-006 P3 진행 중 화면

- 작성: 2026-09-10 / `reviewer_code` (read-only · 검수 1·2 와 같은 세션)
- 범위: `git diff 5751efa..HEAD` — 커밋 하나(`806f52c`), 51파일 **+2,997 / −6,339**.
- **HEAD 를 읽었다.** `backend/` 워킹트리는 검수 도중 WP-003 워커가 손대기 시작했다(§7에 귀속 근거). 인용한 `파일:줄` 은 전부 `git show HEAD:<path>` 기준이다.
- **아무 파일도 고치지 않았다.** 워크트리에 만든 것 0 — 격리 실행은 스크래치패드에 `git archive` 로 뽑아 돌렸고 `git stash` 는 쓰지 않았다.

---

## 0. 총평 — **FAIL — 재발주 필요 (BE 1건)**

지운 것이 만든 것보다 두 배 많은 커밋이고, 그 방향이 옳다. 폐기 목록(§11.1)이 **한 줄도 남지 않고** 사라졌고(잔존 참조 3건은 전부 주석과 부정 단정), 도메인/전송/provider 가 `stream.py` ↔ `entrypoints` ↔ `platform/soniox.py` 로 깨끗이 갈렸다 — `stream.py` 에 provider 이름이 없는 것이 계약이라는 docstring 이 실제로 지켜진다. 프레임 계약은 BE `_stream_message` 와 FE `ServerFrame` 이 키 하나까지 맞고, 코디의 실물 e2e 관측 6가지가 **전부 코드와 일치**한다. 검증도 녹색이다(HEAD 66 · tsc 0 · vitest 39).

막는 것은 **하나**다. **업스트림 역할에 「회의를 시작한 사람」 게이트가 없다** — 서버는 첫 프레임의 `role` 을 그대로 믿는다. 아무 참석자나(심지어 **공유받은 열람자**도) `role:"upstream"` 을 먼저 보내면 그 회의의 단 하나뿐인 업스트림 슬롯을 차지하고, 정작 회의를 시작한 사람은 `meeting_stream_active` 로 막힌다. SPEC §5.2-5 가 「그 자리는 회의를 시작한 사람의 연결이 갖는다」고 못박은 자리이고, FE 는 그 규칙대로 역할을 고르지만 **서버가 클라이언트의 선언을 검증하지 않는다.** 고치는 것은 분기 앞 한 줄 + 테스트 하나다.

이월 WARN 셋 중 **W5·W6 은 해소됐고 W9 는 해소되지 않았다** — 리포트의 「처리」 주장과 코드가 어긋난다(§8).

---

## 1. BE↔FE 프레임 계약 일치 — **PASS**

`_stream_message`(`entrypoints/http.py:188-221`)가 dto↔wire 의 유일한 접점이고, FE `ServerFrame`(`meetings/stream.ts:32-37`)이 그 모양 그대로다.

| 프레임 | BE (`http.py`) | FE (`stream.ts`) | |
|---|---|---|---|
| 첫 프레임 | `StreamAuthFrame` `{type, role, audio?}` · `accessToken` 은 받아도 무시(`:178-185`) | `:78` `{type:"auth", role, audio}` — audio 는 upstream 만 | ✅ |
| `ready` | `:191-196` `meetingStartedAt`(isoformat) · `latestBatchSeq` · `speakerCount` | `:33` 동일 3키 | ✅ |
| `transcript.partial` | `:197-204` `segments[{speakerLabel, atMs, text}]` | `:34` `TranscriptSegment` 동일 | ✅ |
| `transcript.final` | `:205-216` `item{id, speakerLabel, atMs, endMs, content}` | `:35` `TranscriptItem` 동일 | ✅ |
| `ai.batch` | `:218` `{seq, agendas}` | `:36` 동일 | ✅ |
| `error` | `:220` `{code:"meeting_stream_disconnected", reason}` | `:37` 동일 · `:97` 이 `reason` 을 붙든다 | ✅ |

**close code·reason** — `stream.py:16-33` 이 상수를 한 곳에 두고, FE `closureOf`(`stream.ts:55-61`)가 그대로 되읽는다: `1000`→ended · `4401`→unauthorized · `4404`→not_found · `4409` + `meeting_stream_active`→taken / 그 밖→stale_status · 나머지→disconnected. 브리프 §3 과 일치. 오류 뒤 닫는 `1011`(`stream.py:20`)은 브리프·SPEC 이 코드를 지정하지 않은 자리이고 코디 실물 관측과 맞는다.

---

## 2. 인증·열람 축 — **FAIL (업스트림 게이트)**

| 확인 | 결과 |
|---|---|
| 쿠키 principal 이 REST 와 같은 이음새인가 | **PASS** — `connection_principal`(`http_auth.py:82-96`)이 REST 의 `session_principal` 을 그대로 부르고, 개발 페르소나 헤더도 REST 와 같은 갈래로만 남긴다. 실패는 예외가 아니라 `None`(WS 는 상태코드가 없다) |
| 첫 프레임 없음·무효 → 4401 | **PASS** — `http.py:790-797`, 5초(`AUTH_TIMEOUT_SECONDS`) · 사유를 가르지 않는다. 테스트 `test_meeting_stream.py:161`·`:170` |
| 비참석 → 4404 존재 숨김 | **PASS** — `stream_service.py:124-128`, 없는 회의와 참석 아닌 회의가 같은 답. 테스트 `:180` |
| 상태≠in_progress → 4409 `invalid_meeting_status` | **PASS** — `stream_service.py:129-131`. 테스트 `:190` |
| 두 번째 업스트림 → 4409 `meeting_stream_active` | **PASS** — `stream_service.py:135-139`, 첫 세션은 건드리지 않는다. 테스트 `:200` |
| **업스트림 = 회의를 시작한 사람인가** | **FAIL** — 아래 |

### F1 · FAIL — 업스트림 역할에 소유자 게이트가 없다 (담당: BE)

- `modules/meetings/stream_service.py:134` — `if role == ROLE_UPSTREAM:` 뒤에 **누구인지 묻는 줄이 없다.** 첫 프레임의 `role` 선언이 곧 역할이다.
- `modules/meetings/application.py:428-440` `stream_admission` 은 `_can_read_detail` 만 본다 — 그 함수는 **참석자 또는 공유받은 사람**에게 참을 돌려준다(검수 2 에서 확인한 두 축). `MeetingAdmission`(`stream_service.py:80-88`)에 소유자 정보 자체가 실리지 않는다. `grep 'owner|starter|created_by' stream_service.py` → **0건**.
- 어긋난 기준:
  - SPEC §5.2-5 — 「오디오를 올리는 연결은 회의당 하나다. … **그 자리는 회의를 시작한 사람의 연결이 갖는다**」
  - SPEC §5.3 연결 조건 — 「그 회의의 **참석자**이고 회의 상태가 「진행 중」이다」 (공유받은 사람은 참석자가 아니다)
  - FE 브리프 §2:22 — 「`role` 은 **회의를 시작한 사람(만든 사람) = upstream**, 그 외 참석자 = subscribe」
- 결과 둘:
  1. 아무 참석자나 `role:"upstream"` 을 먼저 보내면 슬롯을 가져가고, 정작 회의를 시작한 사람이 `meeting_stream_active` 로 막힌다.
  2. **공유받은(열람) 사람도 업스트림이 될 수 있다** — 자기 마이크를 남의 회의 원문(`meeting_transcripts`)과 오디오 원본에 적재한다. 열람만 열고 수정 권한을 주지 않는다는 §3.2-2 를 우회한다.
- FE 는 규칙대로 고른다(자기 역할을 스스로 정해 보낸다) — 즉 **서버가 클라이언트의 선언을 검증하지 않는 구조**다. 「tool adapter 는 Principal 을 위조하거나 authorization 을 우회하지 않는다」(action-execution.md §3)와 같은 계열의 구멍이다.
- **테스트 공백**: `test_a_subscriber_does_not_take_the_upstream_slot`(`:419`)은 `role=subscribe` 가 슬롯을 안 먹는지만 본다. 「비소유 참석자가 upstream 을 못 잡는다」는 **0건**.
- **고칠 방향 한 줄**: `MeetingAdmission` 에 `owner_id`(또는 `is_starter`)를 실어, `serve()` 의 upstream 분기 앞에서 `member_id != owner_id` 면 `4409 meeting_stream_active`(또는 `4404`)로 닫는다 + 회귀 테스트 1개.
  - 겸해 **subscribe 를 참석자로 좁힐지는 코디 결정**이다 — 시안 `REPORT-회의실-v2.md:152` 는 공유받은 사람이 「진행 중」에 AI 요약·스크립트를 본다고 해서 지금의 subscribe 허용이 맞다. 좁혀야 하는 것은 upstream 뿐이다.

---

## 3. 오디오 경로 — **PASS**

| 확인 | 근거 |
|---|---|
| 컨테이너 형식 → `audio_format=auto`, `sample_rate` 제외 | `platform/soniox.py:45-62` `build_config` — 컨테이너면 `_AUTO_FORMAT`, `sample_rate`·`num_channels` 를 **넣지 않는다**(어긋난 수치를 함께 보내면 provider 가 거절). 테스트 `test_meeting_stream.py:466` |
| endpoint detection 미사용 | `soniox.py:46` — 키 자체를 config 에 싣지 않는 것이 「미사용」 ✓ 브리프 §3 |
| 청크 순서: ① 원본 append → ② 업스트림 | `stream_service.py:402-420` `_feed` — append 가 `OSError` 면 `write_failed` 로 끊고 **②로 가지 않는다**. 테스트 `:233`(순서) · `:250`(적재 실패) |
| `ready` 전 전송 없음 | 서버가 버림(`stream_service.py:404-406`) · FE 가 **아예 안 보냄**(`stream.ts:107-110`) — 이중 ✓ |
| 64KB / 250ms 한도 | `meetings/microphone.ts:13-15` `MAX_CHUNK_BYTES = 64*1024` · `CHUNK_MS = 250`, `:21` 넘는 청크는 잘라 순서대로 보낸다 |
| 선언 형식 | `microphone.ts:11` `webm/opus` · 16kHz · mono → 서버가 컨테이너로 보고 `auto` 로 옮긴다 ✓ |
| 원본 위치가 리포에 안 들어가나 | `settings.py:29` `.scax/recordings`, `.gitignore:13-14` 가 `/.scax/`·`/backend/.scax/` 를 무시한다 — **커밋되지 않는다** ✓ (트리 밖은 아니고 ignore 다) |
| 원본 key 가 응답에 실리나 | `storage_key` 가 `entrypoints/` 에 **0건**, application/repository 안에만 산다(`application.py:102`·`461-463`). 테스트 `:293` |

> 참고(문제 아님): `microphone.ts:21` 이 64KB 초과 청크를 자르고 `platform/recordings.py:43` 은 「webm 청크를 자르면 파일이 깨진다」고 경고하지만, 자른 조각이 **순서대로 전부** append 되므로 바이트 스트림은 동일하게 복원된다. 경고가 가리키는 것은 누락·재배열이다.

---

## 4. 적재·경계 — **PASS**

| 확인 | 근거 |
|---|---|
| 블록 경계 상수 한 곳 | `modules/meetings/stream.py:41-45` — `BLOCK_MAX_CHARS=300` · `BLOCK_GAP_MS=2000` · `DEFAULT_SPEAKER`. 판정은 `BlockBuilder`(`:228-276`) **한 자리**뿐이고 `build_blocks`(`:279`)도 같은 경계를 지난다. 테스트 `:436`(화자 변경·길이·침묵 셋) |
| `at_ms` 기준 = 회의 시작 | `stream_service.py:369-370` `base_ms = _now_ms_since(started_at)` · 테스트 `:461` |
| 새 표가 reset_demo 스키마 안 | `platform/persistence.py:366` `meeting_transcripts` · `:388` `meeting_recording_files` · `:272` `meetings.started_at` — 전부 `Base` 하위라 `reset.py` 의 `create_all` 이 만든다. `create_all` 은 여전히 `bootstrap/reset.py` 한 곳 |
| **폐기 잔존 참조** | `realtime-credential`·`realtime-segments`·`speaker-assignments`·`meeting_raw_transcript*`·`refinement*`·`summary_suggestion*`·`adopt_summary`·`FinalTranscriber`·`liveTranscription`·`MeetingDrawer`·`stt-async-v5` 전수 grep → **살아 있는 참조 0건**. 걸린 3건은 `soniox.py:12`(폐기 사실을 적은 주석)·`test_meeting_stream.py:317`(라우트에 없음을 단정하는 **부정 단정**) 뿐 |
| 폐기 라우트가 실제로 없나 | 테스트 `:313` `test_no_route_offers_a_provider_credential_or_a_direct_upload_any_more` |

---

## 5. 동시성·정리 — **PASS**

| 확인 | 근거 |
|---|---|
| `_Room` 이 `finally` 에서 빠지나 | 업스트림 `stream_service.py:183-187` · 구독 `:202-206` — 둘 다 `finally` 에서 `_drop_if_empty`. `:209` 가 `self._rooms.get(...) is room` 을 확인해 **재생성된 방을 지우지 않는다** |
| provider 가 닫히나 | `shutdown()` `:382-390` — 열린 블록을 먼저 적재하고 `finally` 에서 `_upstream.close()` |
| `_Outbox` 가 소켓을 pump 하나로만 만지나 | **PASS** — `:251-296`. 닫기도 프레임(`_CloseRequest`)으로 큐에 들어가고(`:269-270`), 소켓을 실제로 만지는 것은 `pump`(`:283-296`) 뿐이다. 다른 루프에서 온 put 은 `call_soon_threadsafe`(`:278-280`)로 큐 소유 루프에 넘긴다 |
| 백프레셔가 확정을 버리지 않나 | `:264-267` — 큐가 `OUTBOX_MAX` 를 넘으면 **`TranscriptPartialFrame` 만** 버린다. 확정·AI·오류는 남는다 (SPEC §5.3 잠정 「밀리면 버릴 수 있다」) |
| `/end` 가 1000 으로 닫고 그 뒤 프레임 없나 | `http.py:738` → `close_for_end`(`:144-153`) → `_Room.end()`(`:236-240`) → 각 연결이 `request_close(CLOSE_ENDED, REASON_ENDED)`. `pump` 는 `_CloseRequest` 를 만나면 닫고 **`return`** 하므로 그 뒤 전송이 없다(`:287-292`). 오류 프레임을 앞세우지 않는다 ✓ SPEC §5.3 정상 종료. 테스트 `:395` |
| 설계 밖 예외가 삼켜지나 | `_race`(`:498-510`)가 `task.result()` 로 **그대로 올린다** — 설계한 실패는 `SttUpstreamError`·`OSError` 둘뿐 |

---

## 6. FE — **PASS (W9 이월)**

| 확인 | 근거 |
|---|---|
| WS 생성이 `stream.ts` 한 곳 | `git grep 'new WebSocket'` → **`meetings/stream.ts:70` 하나** ✓ (`api.ts` 와 같은 규약) |
| 자동 재연결 없음 | 회의 코드에 `reconnect`/`backoff`/타이머 재접속 **0건**. `stream.ts:12` 가 이유를 적는다 |
| partial 교체 / final 추가 | `stream.ts:123-124`(타입 주석) · `MeetingStreamState.partial` 은 통째 교체, `finals` 는 누적. 테스트 `MeetingLive.test.tsx` 13건 통과 |
| `ai.batch` 통째 교체 + 스크롤 유지 | `stream.ts:125-126` 「줄 id 를 붙들지 않는다」 · 스크롤은 `MeetingDetailPage.tsx:241-249` 가 `pinned` 여부를 기억해 `useLayoutEffect` 로 복원. 테스트 `MeetingLive.test.tsx:258-279` 가 `scrollTop` 120 유지를 단정 |
| 4409 `meeting_stream_active` 표시 | `stream.ts:59` → `{kind:"taken"}` → `MeetingDetailPage.tsx:376` 부근 상태 줄 문구 |
| 마이크 거부 시 화면 유지 | `MeetingStreamState.micDenied`(`stream.ts:127-128`) — 상태 줄로만 알린다 |
| 메모 낙관 렌더 없음 | `MeetingDetailPage.tsx:124-125` 「응답으로 돌아온 줄만 담는다(낙관 렌더 없음)」 · `:805-807` `onSaved` 뒤에만 push |
| 삭제 4파일 잔존 참조 | `MeetingDrawer`·`liveTranscription` grep **0건** ✓ |
| hex 리터럴 | 신규 FE 파일 전수 **0건** ✓ |
| D25 부품 셋이 DS 어휘만 쓰나 | `Composer.tsx`(`composer`·`btn icon h30`·`field-error`) · `GutterList.tsx`(`gutter-list`·`gutter-row`·`gutter-meta`) · `StatusNote.tsx`(`status-note`/`danger`) — 새 색·새 그림자 0, 인라인은 수치 여백뿐 ✓ |
| **`author` null 처리 (W9)** | **미해소** — §8 |

---

## 7. 회귀 — **PASS (HEAD 66/66)**

⚠ **워킹트리 오염 귀속**. 검수 시작 시점 `git status --porcelain` 은 **비어 있었으나**, BE 테스트를 돌리는 사이 WP-003 워커가 5파일을 고치기 시작했다:

```
 M backend/src/ax_workspace/bootstrap/application.py
 M backend/src/ax_workspace/entrypoints/http.py
 M backend/src/ax_workspace/modules/meetings/application.py
 M backend/src/ax_workspace/platform/meetings.py
 M backend/src/ax_workspace/platform/persistence.py
```
(`frontend/` 는 끝까지 **깨끗했다** — FE 수치는 오염 없음)

| 실행 | 결과 | 귀속 |
|---|---|---|
| 워킹트리에서 BE | **3 failed, 63 passed** | **전부 WP-003 진행분** |
| **HEAD 격리본**에서 BE | **66 passed** | ✅ HEAD 는 녹색 |
| FE `npx tsc --noEmit` | **0 에러** | — |
| FE `npx vitest run src/meetings/` | **39 passed** / 3 files (MeetingList 9 · MeetingLive 13 · MeetingDetail 17) | — |

**귀속 근거** (`git stash` 미사용):
1. 실패 메시지가 워킹트리 변경을 직접 가리킨다 — `test_a_line_hangs_from_an_agenda_...` 는 줄 뷰에 **`at_ms` 가 하나 더 붙어서** 깨졌고, `git diff HEAD` 가 그 필드를 더한 줄(`append_line(..., at_ms=...)` · `"atMs": line.at_ms`)을 보여 준다. 나머지 둘도 같은 `at_ms` 계열 변경으로 `stored` 행 모양이 바뀌어 깨졌다.
2. 결정적 확인 — `git archive HEAD | tar -x` 로 스크래치패드에 **HEAD 순정본**을 뽑아 같은 명령을 돌렸다(워크트리·`.git` 무변경). 그 3건이 **전부 통과**했고 총계 **66 passed** 로 코디 수치와 같다.
   - 그 실행에서 처음 뜬 architecture 실패 4건은 내가 `backend/` 만 뽑아 `Makefile`·`frontend/package.json`·`README.md` 가 없어서였다. 셋을 마저 뽑자 3건이 사라졌고, 마지막 하나(`test_stack_target_is_declared_phony_and_documented`)도 `README.md` 부재(`FileNotFoundError`)가 원인이라 **추출 아티팩트**다.

---

## 8. 새 어긋남 · 리포트 대조

| 확인 | 결과 |
|---|---|
| pause/resume 처리를 만들었나 | **안 만들었다** ✓ — `stream.py:68-71` `IgnoredFrame` 으로 **버리되 닫지 않는다**(브리프 §3 그대로). 회의 코드에 pause/resume 프레임 0건 |
| 화자 이름 지정 | **없다** ✓ — `labels.ts:511` 이 D18 로 범위 밖임을 적은 주석뿐. 익명 `speakerLabel` 만 |
| 알림 | **없다** ✓ — `labels.ts:551` 주석 + `MeetingLive.test.tsx:355-357` 의 부정 단정 |
| 코디 실물 e2e 6건과 코드 일치 | **전부 일치** — 4401(`http.py:788`·`:796`) · 4404(`stream_service.py:127`) · 4409 `invalid_meeting_status`(`:130`) · subscribe `ready{…,latestBatchSeq:0,speakerCount:0}`(`:194-201` + `http.py:191-196`) · 키 없음 → `connect` 실패 → `error{reason:"upstream"}` + **1011**(`stream_service.py:364-368`·`489-495`) · `/end` → summarizing + 스트림 닫힘(`http.py:738`) |

### 이월 WARN 처리 주장 대조

| # | 주장 | 실제 | |
|---|---|---|---|
| **W5** | `MeetingVersionConflict` → 409 | **해소** — `http.py:554` `isinstance(error, (MeetingStateConflict, MeetingVersionConflict))` → 409 | ✅ |
| **W6** | `CreateMeetingRequest` `extra="forbid"` | **해소** — `http.py:266-269` | ✅ |
| **W9** | FE `author` null 대응 | **미해소** — `viewModels.ts:750` 이 여전히 `author: string`. BE 는 `line.author_id`(`application.py:707`)이고 컬럼이 nullable | ⚠️ |

**W9 상세(이월 WARN, 재발주 아님 — 다만 시한이 있다)**
`MeetingDetailPage.tsx:398` 이 `personName(memo.line.author)` 를 부르고, `labels.ts:73-75` `personName` 은 인자에 곧장 `.replace()` 를 건다 — **null 이면 TypeError 로 스크립트 탭이 죽는다.** 지금 그 자리에 들어가는 것은 `sessionMemos`(내가 방금 남긴 메모)뿐이고 메모는 늘 작성자가 있어 터지지 않는다. **WP-003 이 AI 트랙 줄(작성자 없음)을 같은 `MeetingLine` 타입에 실으면 그때 터진다.** 타입을 `author: string | null` 로 고치고 호출부에서 갈라 주면 끝난다.

---

## 9. 재발주 요약

| # | 담당 | 무엇 | 크기 |
|---|---|---|---|
| **F1** | BE | `MeetingAdmission` 에 소유자를 실어 `stream_service.py:134` 업스트림 분기 앞에서 「회의를 시작한 사람」만 통과시키고(그 밖은 4409/4404) 회귀 테스트 1개 | 소 |
| W9 | FE | `viewModels.ts:750` `author: string \| null` + `personName` 호출부 분기 — **WP-003 이 AI 줄을 싣기 전에** | 소 |
| — | 코디 | subscribe 를 참석자로 좁힐지(지금은 공유받은 사람도 구독 가능 — 시안 §3 가시성 표는 그것을 허용한다) | 결정 |
