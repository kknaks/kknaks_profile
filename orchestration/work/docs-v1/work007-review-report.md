# WORK-007 검수 리포트 — 회의 중 · STT 중계 · 2트랙 · AI 배치

- 대상: `b09a16a`(백엔드 Phase 1~4) · `ecb7f07`(프론트 Phase 5~6), 브랜치 `kknaksss/docs-v1`, 기준 `618d5bb`. 90 파일 +9341/−185
- 방법: **read-only.** 코드·테스트를 고치지 않았고 테스트를 돌리지 않았다. 커밋 메시지의 「pytest 449 passed · vitest 240 passed」는 **검증하지 않은 워커 보고값**이다. 앱 창 실물 확인도 하지 않았다(발주 조건). 프론트 워커가 코디 인박스로 보낸 「실물 확인 필요」 목록은 이 워커에게 오지 않아 **테스트 파일의 표기와 코드 주석에서 재구성**했다(§1-7).
- 판정 기준: 정책(DEC-003 §1·§2·§3·§4·§6·§7·§STT) → 아키텍처(`backend/README` §5-1·§5-2·§8-2·§8-3·§12 · `frontend/README` · `system/README` 흐름 ③ · `domains/meeting.md`) → SPEC-007(§2 U-1~U-8 · §4 · Case Matrix 15행 · §6 26개) → WORK-007 Phase 1~6. 항목마다 `파일:줄` + 어긋난 문서 절을 단다. 근거를 못 대는 것은 싣지 않았다.

## 0. 판정 요약

| 등급 | 건수 | 한 줄 |
|---|---|---|
| **FAIL** | **2** | F-1 AI 업무 줄 **유형 배지의 원천(`task.workType`)이 응답에 없다** — SPEC-007 §4·U-4 가 담기로 했는데 백엔드가 빠뜨렸다(§1-9 판정 ①). F-2 프론트 `startCapture` 실패를 `catch {}` 로 삼켜 **설계 밖 실패를 「마이크 연결이 끊겼습니다」로 접는다** |
| **WARN** | **4** | W-1 `start()` 가 service 안에서 `commit()` · W-2 백그라운드 배치 태스크의 예외가 미회수 로그로만 남는다 · W-3 WS `4404` 가 먼저 「서버 연결이 끊겼습니다」로 보인다 · W-4 `kind≠task` 의 `taskId` 를 조용히 뗀다 |
| **문서 공백** | **13** | §5 — 가장 큰 것은 D-1(SPEC-006 필드 소유 표에 `workType` 없음) · D-2(웜스타트 실패 뒤 회의 상태 미정의) · D-8(**compose 에 Redis·worker 가 없는데 WP 는 있다고 전제**) |

코디가 지정한 축은 F-1·F-2 를 뺀 전부 **PASS** 다 — 공용 부품 두 번째 구현 0건 · 자동 재연결 0건 · `except Exception` 0건 · 2트랙 경계 준수 · §7-B 8항목 0건 · 정책에 있는데 없는 것 0건 · 수치 5종 일치 · 키 격리 · **통과로 위장한 E2E 항목 0건**. 상세는 §1.

## 1. 코디 지정 축

### 1-1. 공용 부품 — 두 번째 구현 유무

**프론트**

| 부품 | 판정 | 근거 |
|---|---|---|
| `AgendaLineTree` — `track ===` 0건 | **PASS** | `AgendaLineTree.tsx`·`AgendaHeader.tsx`·`LineRow.tsx`·`EvidenceChip.tsx` 에 `track`·`"human"`·`"ai"` 문자열 0건(grep). 차이는 `expandable`·`onToggleDone`·`onChipClick`·`badgeFor`·`renderLineActions` props 뿐(`AgendaLineTree.tsx:31-50`). 회의록 탭은 `MeetingLiveView.tsx:340-348`(`expandable={false}`), AI 탭은 `:350-361`(`expandable` + `onChipClick`) 로 **같은 컴포넌트**. `static.test.ts` ⑫ 가 5파일에 대해 고정. `AgendaLineTree.test.tsx:113-149` 가 같은 컴포넌트에 `track='ai'` 데이터를 넣어 두 모양을 검사 |
| `MeetingStatusBar` ↔ WORK-006 `MeetingTopBar` | **PASS** | `MeetingTopBar.tsx` **삭제**, `waiting`·`headline` 변형을 `MeetingStatusBar.tsx:29-39` 가 흡수. `MeetingPreviewPanel.tsx`·`MeetingScheduledPage.tsx` 가 새 이름을 import. `static.test.ts` ⑥ 이 「`(TopBar\|StatusBar)` 파일 하나」로 고정. 한 자리(top 150 · 1640×56) 를 두 파일이 다투지 않는다 — [09] L733 · SPEC-007 Placement L98 |
| `TranscriptPanel` · `PromptBar` · `LineKindPopover` | **PASS** | 부모·라우트·회의 상태를 import 하지 않는다(`static.test.ts` ⑬). `TranscriptPanel` 은 `ref.scrollToRange` + `clearHighlight`(`:97-120`), `PromptBar` 는 콜백 셋만(`:38-58`). WORK-008 이 그대로 쓸 수 있는 형태 |
| `lib/api/ws.ts` — `new WebSocket(` 유일 | **PASS** | grep: `lib/api/ws.ts:83` 1건(테스트 `test/fakeWebSocket.ts` 제외). `static.test.ts` ⑪ 고정 |
| WORK-006 재사용 | **PASS** | `MeetingLiveView.tsx:34·42·435-440` — `MeetingAttachmentsTab`·`AttachmentAddTrigger`·`openAttachmentFileDrawer`(→ `DrawerFrame`) 그대로. `MeetingAttachmentsTab.tsx:113-114` 의 `V2Gate` 드롭 영역이 회의 중에도 같은 것. 첨부 드로어 두 벌 없음(WP Open Issues 「첨부 열기 드로어의 소유」) |
| `lib/` 승격분 사용 | **PASS** | `lib/hooks/useRowFailures.ts`·`useWorkSettings.ts`·`lib/api/errors.ts`(`inlineErrorMessage`) 존재. `MeetingLiveView` 는 `features/meetings/errors.ts` 의 `meetingInlineError` 를 지나 그것을 쓴다 |
| features 사이 import 0건 | **PASS** | `features/meetings` 에서 `@/features/*` 타 영역 import 0건(grep) · `static.test.ts` ⑨ |

**백엔드**

| 부품 | 판정 | 근거 |
|---|---|---|
| `build_detail` 1개 · `agendas.ai`·`latestBatchSeq` | **PASS** | `test_meeting_live_static.py:91-98` 이 `build_detail(` 1회 · `MeetingDetailDTO(` 1회 · 다른 service 에 0회를 고정. 조립 변경 없이 WORK-006 의 트랙별 조회(`list_agendas`·`max_succeeded_batch_seq`)가 채운다. `test_meeting_live_api.py:314` 「같은 빌더에서 ai 트랙·latestBatchSeq」 |
| `_assert_allowed` 1곳 | **PASS** | `meeting_service.py:89·108` `line_write` 행만 추가. `_ALLOWED` 가 stream·batch service 에 없다(정적 테스트 `:96-98`). WS 의 `status≠recording` 판정은 close code 로 나가야 해서 `meeting_stream_service.py:126` 이 별도로 비교한다 — 표의 두 번째 사본이 아니라 다른 표면(§5 D-9 참조) |
| `schedule_service` | **PASS** | 이 diff 가 `schedule_*`·`start_at`·`end_at` 를 건드리지 않는다. 겹침·파생 두 번째 구현 0 |
| codex 옵션 빌더 한 함수 | **PASS** | `integrations/agent.py:57-70` `build_codex_options()` 하나. 웜스타트(`session_id=None`, `meeting_batch_service.py:514-519`)와 배치(`resume`, `:242-247`)가 같은 함수를 지난다. `test_meeting_live_static.py:46-55` 가 `"mode": "session"`·`["output_schema"] =` 출현을 이 파일 하나로 고정 |

### 1-2. 정책이 못박은 실패 처리 — DEC-003 §7 · BASE-003 L43

| 항목 | 판정 | 근거 |
|---|---|---|
| 자동 재연결 0건 | **PASS** | 백: `meeting_stream_service.py:142-148` finally 에서 레지스트리 삭제 + `shutdown()` 뿐, `retry`·`reconnect`·재접속 루프 0(정적 테스트 `:78-88`). 프론트: `ws.ts:99-124` 의 `onclose` 는 `4401` 갱신 1회 재연결(FE §4-2 예외)만 하고 그 밖은 `finish()`. `useMeetingStream.ts:275-284` `openSocket` 은 `resume()` 안에서만(`:296-312`), 마운트 effect 는 닫기만(`:315-325`). `setInterval`/`setTimeout` 재연결 0(`static.test.ts` ⑪ — `EvidenceChip.tsx:41` 은 캡션 2초, `useNow.ts:18` 은 표시 시계). `useMeetingStream.test.tsx:158·193` 이 「새 연결 0건」을 소켓 생성 스파이로 검사 |
| `except Exception` 0건 | **PASS** | service 3파일·integrations 3파일 0건(정적 테스트). 포착은 `SttUpstreamError`·`OSError`(`meeting_stream_service.py:208·265·276·303`)·`AgentRunFailed`·`AgentRunTimeout`(`meeting_batch_service.py:248`)·`_SchemaViolation`(`:262`)·`json.JSONDecodeError`(`:353`)뿐. 프론트는 F-2 참조 |
| 배치 실패 → 조용히 · 다음 배치에 병합 · 표시 없음 | **PASS** | `meeting_batch_service.py:248-257` `failed` 기록 + return. 커서는 성공분만(`meeting_batch_run_repository.py:29-36`). WS 프레임 없음. `test_worker_timeout_is_failed_silently_and_merged_into_the_next_batch` |
| 스키마 위반 → 전체 폐기 · 부분 파싱 0 | **PASS** | `_parse_output`(`:346-389`) 은 리스트를 다 만든 뒤에야 돌려주고, 어느 항목이든 `_SchemaViolation` 이면 `:262-271` 에서 `discarded` + return — 적재 함수에 닿지 않는다. **BE §12 테스트 6** = `test_schema_violation_discards_the_whole_batch`(`test_meeting_batch.py:160`) |
| 없는 업무 참조 → 그 줄만 action 강등 · 내용 유지 | **PASS** | `_demote_if_needed`(`:392-404`) — `kind`·`task_id` 만 바꾸고 `content`·`detail`·`evidence` 는 그대로. **BE §12 테스트 7** = `test_task_outside_the_whitelist_is_demoted_to_action_keeping_its_body`(`:195`). 화이트리스트 = `task_repository.list_meeting_context`(`:726-753`) — 프로젝트 있으면 그 프로젝트, 없으면 `project_id IS NULL`(M-15-a) |
| 파일 적재 실패 → 그 자리에서 끊는다 | **PASS** | `_feed`(`:256-279`) ① `storage.append` → `OSError` 면 `_fail(write_failed)` + `return False` → `_pump_client` 종료 → Soniox 로 가지 않는다. `test_append_failure_closes_with_write_failed_before_reaching_upstream`. `storage.py:47-56` 은 재시도·대체 경로 없음 |
| 마이크·스트림 실패 → 일시정지 + 사유 · 「다시 연결」 버튼 0 | **PASS** | 사유 4종 + `elsewhere` 문구가 `MeetingStatusBar.tsx:42-48` 한 곳. 헤더 버튼은 「일시정지」/「재개」/「회의 종료」뿐(`MeetingLiveView.tsx:255-281`), 「다시 연결」 문자열 0(`static.test.ts` ⑭). 마이크 트랙 `ended` → `pause{mic}` 프레임 + `paused/mic`(`useMeetingStream.ts:130-139`) |
| **설계 밖 실패에 fallback** | **FAIL 1** | **F-2** `useMeetingStream.ts:170-175` — 아래 §2 |

### 1-3. 2트랙 경계

| 항목 | 판정 | 근거 |
|---|---|---|
| AI 는 `track='ai'` 에만 INSERT · 사람 트랙 개입 0 · 줄 제안 0 | **PASS** | `_persist`(`meeting_batch_service.py:410-482`) 의 `create_agenda`·`create_line` 이 전부 `MeetingTrack.AI`. 사람 안건·줄 UPDATE 경로 없음. 프롬프트도 「고치지도 제안하지도 마라」(`:603`). `test_batch_input_carries_human_context_read_only`(`:337`) 가 사람 줄이 그대로임을 검사 |
| AI 안건은 사람 회의록 탭에 안 보인다(DEC-003 §4 L96) | **PASS** | 회의록 탭 `AgendaLineTree agendas={human}`(`MeetingLiveView.tsx:341`), AI 탭만 `meeting.agendas.ai`(`:351`). `MeetingLiveView.test.tsx:333` 「회의록 탭에는 AI 없음」 |
| AI 증분 즉시 반영 · 버퍼링 0 · 「배치 n회 반영」(L97) | **PASS** | 백: 적재 트랜잭션 커밋 직후 `push_ai_batch`(`:289-291`), 세션 없으면 건너뛰고 다음 `ready.latestBatchSeq`(`meeting_stream_service.py:151-159`). `test_successful_batch_is_pushed_right_after_commit`. 프론트: `ai.batch` → `mergeAiBatch` 로 캐시 직접 병합(`useMeetingStream.ts:215-229`), 안내 바 「배치 n회 반영 · HH:MM」(`MeetingLiveView.tsx:327-335`), 미확인 점 6px(`:311`). 재연결 뒤 `ready.latestBatchSeq > 캐시` 면 상세 재조회(`:184-188`) |
| 배치 입력 = 사람 안건·줄 **읽기 전용 컨텍스트**(ERD M-6 정정) | **PASS** | `build_batch_prompt`(`:580-609`) — `humanAgendas`(전량 · `state` 포함) · `humanLines`(미처리 구간 이후 · `list_human_lines_since`) · `aiAgendas`(`sourceAgendaId` 포함) · `taskWhitelist`. SPEC-007 §4 「배치 입력」 5행 그대로 |
| 확정 토큰만 적재 · 잠정은 표시용(§3) | **PASS** | `_handle_tokens`(`meeting_stream_service.py:309-318`) — `is_final` 만 `_absorb_final` → 블록 경계에서 `create_block`. 잠정은 `TranscriptPartialFrame` 교체 push 뿐. `meeting_transcript_repository.py` 에 잠정용 함수 없음. `test_partials_are_pushed_as_replacements_and_never_stored` |
| 화자 익명 라벨까지만 · 이름 입력 0(§2) | **PASS** | `TranscriptPanel.tsx:153·180` 「화자 {label}」, 클릭 핸들러·입력 없음. `speaker_label` 은 번호 문자열(`soniox.py:118-126`). `TranscriptPanel.test.tsx:26` 「이름 입력 자리 없음」 |

### 1-4. 그리지 않았나(SPEC-007 §7-B) · 있어야 하는데 없는 것

| §7-B 항목 | 화면 | 근거 |
|---|---|---|
| 상태 바 파형 15개 막대 | **0건** | `MeetingStatusBar.tsx:85-93` dot + 문구 + 경과뿐. `static.test.ts` ⑭ 「wave·파형」 0 |
| 상태 바 「자동 저장 · 09:42」 | **0건** | 상태 바에 없고 **탭 안내 바**(`MeetingLiveView.tsx:327-331`)에만 — U-2 L126 |
| 「회의실 A」 | **0건** | 부제 `MeetingLiveView.tsx:250-252` 날짜 · 유형명. ⑭ 고정 |
| 프롬프트 「+」 | **0건** | `PromptBar.tsx:196-264` 칩·라벨·입력·시각·전송뿐. `PromptBar.test.tsx:37` |
| AI 요약 카드 | **0건** | AI 탭이 `AgendaLineTree`(트리). `MeetingLiveView.test.tsx:333` 「트리(카드 아님)」 |
| 「회의 중 작성」·「· 안건 1」 | **0건** | WORK-006 `MeetingAttachmentsTab`·`AttachmentFileDrawer` 재사용(WORK-006 검수 §1-2 PASS 분). ⑭ 고정 |
| PNG/PDF 행 | **0건** | 위와 같음. `MeetingLiveView.test.tsx:385` |
| 잠정 발화의 시각 | **0건** | `TranscriptPanel.tsx:169-189` 잠정 블록은 dot + 「화자 n」 + 본문 + 캐럿, 시각 없음. `TranscriptPanel.test.tsx:40` |

| 정책에 있는데 있어야 하는 것 | 화면 | 근거 |
|---|---|---|
| `/` 팝오버 「업무」 항목 | **있음** | `LineKindPopover.tsx:25` `LINE_KINDS = [discussion, decision, task, action]`, 칩 「업」(`:31`). `PromptBar.test.tsx:65` 4종 |
| 일시정지 3종에서 「회의 종료」 활성 | **있음** | `MeetingLiveView.tsx:272-280` `disabled={connecting}` 만 — `paused/*` 전부 활성. `MeetingLiveView.test.tsx:149` 「서버 연결이 끊겼습니다 + 회의 종료 활성」 |
| 안건 배지 「대기」 | **있음** | `MeetingLiveView.tsx:53-57` `next → "대기"`. `AgendaLineTree.test.tsx:74` |
| 「재개」 버튼 · 「안건 선택」 · 빈 상태 2종 · 사유 상태 바 4종 | **있음** | `MeetingLiveView.tsx:255-264` · `PromptBar.tsx:217-227` · `:347·356-360` · `MeetingStatusBar.tsx:42-48` |

### 1-5. 수치 — DEC-003 §STT L164·L162

| 항목 | 정책 | config 기본값 | `.env.example` | 판정 |
|---|---|---|---|---|
| 확정 발화 임계 | 600자 | `config.py:56` 600 | `:39` 600 | ✔ |
| 안건 전환 최소 | 80자 | `:58` 80 | `:41` 80 | ✔ |
| 최대 대기 | 180초 | `:60` 180 | `:43` 180 | ✔ |
| 배치 타임아웃 | 120초 | `:62` 120 | `:45` 120 | ✔ |
| 회의당 세션 | 1 | `:64` 1 (≠1 이면 `RuntimeError` `meeting_batch_service.py:108-111`) | `:47` 1 | ✔ |
| 모델 · 힌트 · 화자 분리 · endpoint | `stt-rt-v5` · `["ko"]` · `true` · 미사용 | `soniox.py:33-34·65-77` — config dict 에 endpoint 키 자체가 없다 | — | ✔ |

`test_meeting_live_api.py:61` `test_batch_numbers_match_dec_003` 가 5수치를 고정한다. 트리거 3종은 `evaluate`(`meeting_batch_service.py:149-174`)에서 `≥600` · `≥80`(agenda_switch) · `>0`(timer) — 79자/80자 경계 테스트 있음(`test_agenda_switch_fires_at_80_chars_not_79`). 블록 경계 300자·2초·프레임 5초는 SPEC 값 그대로 상수(`meeting_stream_service.py:75-76` · `meeting_stream_router.py:39`).

### 1-6. 키

| 항목 | 판정 | 근거 |
|---|---|---|
| `SONIOX_API_KEY` 가 프론트로 내려가는 경로 | **0건** | 읽는 코드 `config.py:35` + `integrations/soniox.py:154` 뿐(정적 테스트 `:22-33`). `schemas/`·`api/` 에 `soniox` 문자열 0(`:36-43`). WS 프레임 모델(`schemas/meeting_stream.py`)에 제공자 이름·주소·키 없음. 프론트 `audioCapture.ts:4-7` 「프론트는 STT 상대를 모른다」 — `AUDIO_DECLARATION={format:'auto',…}` 만 선언 |
| `.env.example` 빈 값 | ✔ | `.env.example:26` `SONIOX_API_KEY=` |
| 커밋·로그·문서에 실제 값 | **0건** | `git log -p 618d5bb..HEAD` 에 키 형태 문자열 0(grep). `.env` 는 `.gitignore:5-7` 로 제외, 추적 파일 아님. `SonioxConnector` 는 키를 인스턴스에만 들고 로그하지 않는다(`soniox.py:129-145`) |
| `ai_session_id`·`recording_path` 응답 비노출 | ✔ | `MeetingAiContextDTO`(`dto/meeting.py`) 는 배치·스트림 내부용, `MeetingDetail`·`LineItem`·WS 프레임에 두 필드 없음 |

### 1-7. E2E 대체 — 「실물 확인 필요」 통합표

WP Phase 6 검증 27항목 중 **테스트로 옮긴 것 25 · 못 옮긴 것 2**. 못 옮긴 것은 `MeetingLiveView.test.tsx:4` 와 `audioCapture.ts:11-12` 에 「실물 확인 필요」로 **정직하게 남아 있다.** 통과로 처리한 항목은 **0건**이다.

| # | 항목 | 층 | 왜 테스트로 못 닫나 | 어디에 적혀 있나 |
|---|---|---|---|---|
| 1 | macOS Tauri(WKWebView) `getUserMedia` 권한 프롬프트 → 허용 → 캡처 · Windows 확인 시점 | FE | jsdom 목(`test/mediaMock.ts`) | `audioCapture.ts:11-12` · WP Phase 6 L330 |
| 2 | `MediaRecorder` 지원 mime(webm/opus vs mp4/aac) · 실제 청크 크기 ≤64KB · 250ms 간격 | FE | 목 recorder | `audioCapture.ts:5-8·22` |
| 3 | 1280~1439 좌 유동 + 우 400 · 첨부 드로어 전체화면 · <1280 안내 화면에서 스트림 유지 | FE | 픽셀·뷰포트 테스트를 두지 않는다(FE §11) | `MeetingLiveView.test.tsx:4` 「반응형 실측」 |
| 4 | 근거 칩 → `scrollIntoView` 실제 스크롤 위치(하이라이트는 테스트 됨) | FE | jsdom 에 `scrollIntoView` 없음 | `TranscriptPanel.tsx:109` |
| 5 | 「재개」 뒤 화자 번호가 이어지는가(같은 세션) / 끊김 재개 뒤 새 세션 라벨 | FE+BE | 대역 Soniox 는 라벨을 스크립트로 준다 | S-6·S-7 — 실 Soniox 필요 |
| 6 | Soniox 응답 필드(`tokens[].speaker`·`start_ms`·`end_ms`·`finished`·`error_code`) 실측 | BE | 대역 재생 | `soniox.py:8-10` (백엔드 보고 1) |
| 7 | 오디오 포맷 — 프론트 `format:'auto'` + webm 컨테이너를 Soniox 가 받는가 · `auto` 면 `sample_rate` 생략이 맞는가 | FE+BE | 대역 | `soniox.py:35-36·74-76` · `audioCapture.ts:5-7` (백엔드 보고 2) |
| 8 | codex `--output-schema` 가 `ai_schemas/meeting_batch.json` 을 그대로 강제하는가 | BE | 대역 gateway | `agent.py:7-8` (백엔드 보고 3) |
| 9 | 웜스타트 결과에서 `result_session_id` 가 실제로 회수되는가 | BE | 대역 `WARM_SESSION_ID` | `agent.py:120` · `fakes/agent.py:14` (백엔드 보고 4) |
| 10 | **compose 에 Redis·open-kknaks worker 없음** — `docker-compose.local.yml:8-24` 는 `db`·`api` 뿐(`:3` 「회의록 배치에서 합류한다」 주석만). 현재 compose 로는 `/start` 의 웜스타트가 브로커 연결에서 예외 → **회의를 시작할 수 없다** | Ops | 인프라 | 백엔드 보고 5 · WP L43 전제 오류(§5 D-8) |
| 11 | 일시정지 중 Soniox 유휴 연결 유지 시간 실측 | BE | 실 Soniox | WP Open Issues L365 (백엔드 보고 6) |
| 12 | `at_ms` 기준 — `_base_ms`(업스트림 연결 시점 오프셋 + 일시정지 누적, `meeting_stream_service.py:20·194-195·289-294`) 가 근거 칩 벽시계와 맞는가 | BE | 실 오디오 | 백엔드 보고 7 |
| 13 | NPM 리버스 프록시 WS upgrade 통과 · idle timeout ≥300분 | Ops | 인프라 | WP Pre-deploy L337 (백엔드 보고 8) |
| 14 | 백엔드를 실제로 내렸을 때 브라우저 close code(1006) → 「서버 연결이 끊겼습니다」 | FE | 대역은 `1011`·`1006` 를 스크립트로 준다(`useMeetingStream.test.tsx:193`) | 실 네트워크 확인 |

### 1-8. 코디가 이미 판정한 것 — 확인만

`POST …/lines` 응답이 `LineItem` 이다 — `meeting_router.py:232-249` `response_model=LineItem` · 201. SPEC-007 §4 L320 대로이며 FAIL 로 올리지 않는다. 단 **SPEC-008 §4 L490 은 같은 표면을 `201 MeetingDetail` 로 적었다** — WORK-008 이 밟을 자리라 §5 D-13 에 적었다.

### 1-9. 프론트 워커가 올린 불일치 — AI 「업무」 줄 유형 배지 판정

**판정: ① — SPEC 이 `workType` 을 담기로 했는데 백엔드가 빠뜨렸다. 덤으로 SPEC-006 필드 소유 표가 세 SPEC 과 어긋난 문서 공백이 하나 있다(D-1).**

| 문서 | `task` 요약의 정의 | 근거 |
|---|---|---|
| **SPEC-007 §4** LineItem(track=ai) 예시 | `task: { id, title, workType: { id, name, colorToken } }` | L378 |
| SPEC-007 U-4 기대 결과 | 「`kind='task'` 는 … 라벨 옆에 그 업무의 **유형 배지**([09] L671 — `workType` 이름·색)를 단다」 | L161 |
| SPEC-007 Data Contract | 「AI 업무 줄의 유형 배지 \| `meeting_line.task_id` → `task.work_type`(상세·WS 응답의 `task` 요약)」 | L566 |
| **SPEC-008 §4** merged LineItem 예시 · L484 | `task: { id, title, status, workType:{…}, dueDate, isDeleted }` — 「SPEC-007 `LineItem.task` 에 `status`·`dueDate`·`isDeleted` 를 **더한** 모양」 | L450-451 · L484 · L644 |
| SPEC-006 §4 필드 소유 표 | `task` 요약(`{ id, title, status, dueDate, isDeleted }` — `kind=task` 일 때, SPEC-008) — **`workType` 없음** | L447 |
| SPEC-006 §4 | 「줄의 **의미·표시**·쓰기 표면은 SPEC-007·008 이 정본이고 이 spec 은 자리만 고정한다」 | L448 |
| 디자인 시스템 [09] | 업무 줄 = 라벨 `#5F6470` + **유형 배지**(22px r4 `#F4F7FF`/`#3F5F94`) + 「업무 갱신」 | L668~672 |

- **코드**: `schemas/meeting.py:210-217` `LineTaskSummary` = `id·title·status·dueDate·isDeleted`, `dto/meeting.py:73-80` 같음, `repository/meeting_child_repository.py:190-213` `_line_to_dto` 는 `Task` 만 조인하고 `work_type` 을 읽지 않는다. WS `ai.batch` 도 같은 `LineItem` 이라(`schemas/meeting_stream.py:132`) 두 경로 모두 `workType` 이 없다. 프론트 `LineRow.tsx:14` 는 「`task` 요약에 `workType` 이 없어 그리지 않는다」고 적고 뺐다.
- **왜 ①인가**: 줄의 의미·표시 정본은 SPEC-007·008 이고(SPEC-006 L448), 그 둘이 **일치해서** `workType` 을 담는다. SPEC-006 표는 「이름의 정본」을 자처하지만 `task` 요약 행은 SPEC-008 이 정의한다고 스스로 적었고(L447 「SPEC-008」), 그 SPEC-008 정의에 `workType` 이 있다. 시안·정책([09] L671 · DEC-003 §1 L54 「유형 배지」)도 같다. 따라서 **백엔드가 응답에 `workType` 을 빠뜨린 것**이고, 프론트가 배지를 뺀 것은 그 결과다.
- **처리**: **F-1**(§2). 백엔드가 `LineTaskSummaryDTO` 에 `work_type{id,name,color_token,is_deleted}` 를 더하고(`_line_to_dto` 에서 `work_type` 조인 — 목록 조회 `_WorkTypeRef` 와 같은 방식), 프론트가 `LineRow` 에 공용 `TypeBadge` 를 단다. **WORK-008 「업무 갱신」 버튼이 같은 자리**(라벨 + 배지 + 버튼, [09] L668~672)를 쓰므로 WORK-008 착수 전에 닫아야 한다. SPEC-006 L447 표 정정은 D-1.

## 2. FAIL

**F-1. AI 업무 줄의 유형 배지 원천 `task.workType` 이 상세·WS 응답에 없다** — 백엔드
- `schemas/meeting.py:210-217` · `dto/meeting.py:73-80` · `repository/meeting_child_repository.py:190-213` · (결과) `LineRow.tsx:14`
- 어긋난 문서: SPEC-007 §4 L378 LineItem(track=ai) · U-4 L161 · Data Contract L566 · SPEC-008 §4 L450-451·L484 · [09] L671
- 근거·판정은 §1-9. 화이트리스트를 통과한 AI 업무 줄이 화면에서 「업무」 라벨만 달고 유형을 잃는다 — U-4 기대 결과 미충족 · §6 Acceptance 「`/` 팝오버 … 업무 줄은 배지·버튼 없음」은 **사람 줄** 얘기고 AI 줄은 배지가 있어야 한다.
- 수정 규모: 백 소(dto 1 필드 + 조인 1 + schema 1), 프론트 소(`LineRow` 에 `TypeBadge` 1). 원 워커에게 재발주.

**F-2. `startCapture` 실패를 `catch {}` 로 삼켜 마이크 실패로 접는다 — 설계 밖 실패의 fallback** — 프론트
- `features/meetings/hooks/useMeetingStream.ts:170-175`
  ```ts
  try { captureRef.current = startCapture(mic, …); } catch { onTrackEnded(); }
  ```
- 어긋난 문서: DEC-003 §7 L131-132 「처리하는 실패는 열거한 것뿐 … 광범위한 예외 포착은 어디서 깨졌는지를 가린다」 · BASE-003 L43 · SPEC-007 §4 Case Matrix 마이크 실패 행(**권한 거부 · 장치 분리 · 트랙 `ended`** 만) · §5 L587 · FE §3-5 「그 밖 — 가리지 않는다」 · FE §11 금지 7
- 무엇이 가려지나: `MediaRecorder` 부재 · 후보 mime 전부 미지원(`audioCapture.ts:50-55` 가 던지는 `NotSupportedError`) 같은 **환경 실패**가 「일시정지 · 마이크 연결이 끊겼습니다」 + 서버로 `pause{mic}` 프레임(`:136`)으로 나간다. 서버는 정상 일시정지로 보고 Soniox 세션을 유지하며, 사용자가 「재개」를 누르면 마이크 트랙은 살아 있어(`hasLiveAudioTrack`) `resume` 프레임 → `ready` → 다시 `startCapture` 실패 → 같은 문구 — **원인 없이 도는 상태**가 된다. 하필 실물 확인이 안 된 WKWebView `MediaRecorder`(§1-7 #2)가 이 자리다.
- 수정 규모: 소 — `catch` 를 걷어 전파하거나(설계 밖), 굳이 잡으려면 사유를 드러내는 별도 문구 + 토스트로. `:153-157` 의 `getUserMedia` 실패 `catch` 는 Case Matrix 행 그대로(토스트 「마이크를 사용할 수 없습니다」)라 지적하지 않는다.

## 3. WARN

**W-1. `meeting_service.start()` 가 service 안에서 `session.commit()` 을 부른다** — 백엔드
- `service/meeting_service.py:464`
- 규약: BE §2 표 「service — `commit()` 금지」 · §7 「service·repository 는 flush 까지만 하고 commit 을 모른다」. 반면 BE §7 「외부 호출 — 읽기 → (커밋) → 외부 호출 → 새 세션에서 쓰기」 · WP L169 「전이 커밋 → 제출 → 새 세션에서 `ai_session_id` UPDATE」 가 **이 자리의 커밋을 요구**한다. 코드는 WP 를 따랐고 docstring(`:444-451`)에 사유를 적었다. 「새 세션」이 아니라 같은 세션의 새 트랜잭션이라는 점도 다르다.
- 판정: 규약끼리 충돌한 자리다 — 코드 수정보다 **BE §2/§7 정합(D-3)** 이 먼저. 문서가 정해지면 자리를 옮기든 예외로 명시하든 한다.

**W-2. 백그라운드 배치 태스크의 「전파」가 미회수 예외 로그로만 남는다** — 백엔드
- `service/meeting_batch_service.py:117-121` `schedule()` — `asyncio.create_task(evaluate(...))` + `_tasks.discard` 콜백뿐, `task.result()` 를 아무도 읽지 않는다. 블록 닫힘(`meeting_stream_service.py:378`)·안건 전환(`meeting_service.py:581·606` 커밋 뒤 훅)에서 부르는 실제 경로가 전부 이것이다.
- 규약: BE §8-1 「그 밖의 예외는 전파 — 500 으로 나가고 로그에 스택이 남는다. 그게 의도다」 · WP Phase 4 L265 「프로토콜 오류 → **500 으로 전파**」. 배치는 요청 경계 밖이라 500 이 없고, 설계 밖 예외(예: `ai_session_id` 없음 `RuntimeError` `:234-236`, 브로커 도달 불가)는 asyncio 가 GC 시점에 「Task exception was never retrieved」로 남길 뿐이다. `test_protocol_errors_propagate_without_a_failed_row`(`test_meeting_batch.py:255`) 는 `evaluate()` 를 **직접** 부르므로 이 경로를 검사하지 않는다.
- 판정: 실패를 삼키지는 않지만 드러내는 자리가 없다. `_tasks.discard` 자리에서 `task.result()` 를 읽어 스택 로그로 남기는 정도의 정리 대상. 문서 쪽은 D-4.

**W-3. WS `4404` 를 받으면 먼저 「일시정지 · 서버 연결이 끊겼습니다」가 그려진다** — 프론트
- `hooks/useMeetingStream.ts:262-266` — `NOT_FOUND` → 상세 무효화 + `paused/stream:upstream`. 재조회가 404 로 돌아오면 `MeetingDetailPage.tsx:42` 가 「없는 회의록입니다」를 그리므로 **최종 화면은 맞다.**
- 규약: SPEC-007 §4 close code 표 L305 `4404` → 「없는 회의록입니다」. 그 사이 상태 바 문구가 사실과 다르다(서버는 살아 있다).
- 판정: 동작은 되나 규약 이탈. 4404 는 상태 바를 갈지 말고 재조회 결과로만 갈리면 된다. 문서 쪽은 D-7.

**W-4. `kind≠task` 인 출력 줄의 `taskId` 를 조용히 뗀다** — 백엔드
- `service/meeting_batch_service.py:397-400` — 강등도 폐기도 아닌 무음 정정. `ai_schemas/meeting_batch.json:42` 는 `taskId` 를 조건 없이 `integer|null` 로 두어 스키마가 잡지 않는다.
- 규약: SPEC-007 §4 배치 출력 L421 「`taskId` — `kind=task` 일 때만, 없으면 null」 · BE §8-1 「기본값으로 때우지 않는다」. 검증 표 2단(스키마)·3단(화이트리스트) 어느 행도 이 경우를 적지 않았다(D-5).
- 판정: 정책 문면상 「조용한 대체」. 폐기(2단)로 볼지 무시로 볼지는 문서가 정해야 하나, 정해지기 전이라도 최소한 `reason` 로그는 남겨야 한다.

## 4. 층별 판정 요약

- **정책(DEC-003)** — §1 표(업무 줄 4종 · 일시정지 v1 · 마이크/스트림 실패 → 일시정지 · 로컬 업로드 v2 게이트 · 장소 없음 · 「대기」) 전부 반영. §2 익명 화자 ✔. §3 확정 토큰만 ✔ · 녹음 원본 중계 경로 append ✔(`storage.py`). §4 2트랙·AI 안건 축·증분 즉시·무소속 웜스타트 ✔. §6 녹음 파일은 소프트 딜리트와 무관하게 남는다(이 diff 에 삭제 경로 없음) ✔. §7 — F-2·W-4 외 ✔. §STT ✔(§1-5).
- **아키텍처(BE)** — 계층: service 에 `fastapi`·`schemas` import 0(정적 테스트) · repository dto 반환 · WS 는 `dto/meeting_stream.py` ↔ `schemas/meeting_stream.py` 를 api 층 `WebSocketStreamClient`(`meeting_stream_router.py:43-74`)에서만 변환 ✔. §5 블로킹 금지: 파일 append `anyio.to_thread`(`storage.py:49`) ✔. §5-1 업스트림은 인증 뒤(`serve` → `run():207`) · ①append→②전달 · 백프레셔 잠정만(`:382-386`, `test_backpressure_drops_only_partials`) · finally ✔. §5-2 싱글턴 gateway(`agent.py:123-130`) · `resume` · `output_schema` ✔. §7 트랜잭션: 배치는 단계마다 `session_scope`(`:229-287`), codex 대기 중 세션 없음 ✔ — W-1 참조. §8-2: `4401/4404/4409(reason 문자열)` · `error{meeting_stream_disconnected, reason}` · `invalid_meeting_status` 409(`test_line_write_outside_recording_is_409`) ✔ · `validation_error` 에 `field`(`main.py:37·68`, G-2) ✔. §9 소유 검사 먼저(`_require_meeting` · WS `find_active(account_id)`) ✔. §11 `SONIOX_API_KEY` 기본값 없음 ✔. §12 실제 Postgres · 대역은 `integrations/` 경계에서만(`conftest.py:56-81`) · 필수 테스트 6·7 ✔.
- **아키텍처(FE)** — §2 규칙: `app/` 에 로직 0 · 영역 사이 import 0 · `fetch` 직접 0 ✔. §3-2 `retry:false` 그대로(뮤테이션에 재시도 없음 · `MeetingLiveView.test.tsx:228` 「재요청 0건」) ✔. §3-3 캐시 키는 `queryKeys.ts` 에 `meetingTranscript`·`meetingStartIntent` 추가 ✔ — 무효화는 `['meetings','detail',id]` 만(WP 캐시 키 행) ✔. §3-4 낙관적 갱신 없음(`useMeetingMutations.ts:158-187` 서버 응답 뒤 반영) ✔. §3-5 `code` 분기 · 트랜스크립트 실패 「불러오지 못했습니다」+「다시 시도」(`MeetingLiveView.tsx:410-421`) ✔. §3-6 시각 포맷은 `lib/datetime.ts`(`formatClock`·`msToWallClock`·`formatElapsed`) ✔, 컴포넌트 `new Date()` 포맷 0. §4-2 WS 첫 프레임 · `4401` 갱신 1회(`ws.ts:107-124` · `ws.test.ts:58-128`) ✔. §5 hex 리터럴 0 · `text-[NNpx]` 0(grep) ✔. §6 `Sheet`/`Dialog` 직접 import 0 · 첨부 드로어는 `openAttachmentFileDrawer` ✔. §7 `position:absolute` 0, 우 열 `clamp(400,…,464)`(`MeetingLiveView.tsx:293`) ✔ — 실측은 §1-7 #3. §8 훅 하나가 WS 소유 · 포맷 격리 `audioCapture.ts` ✔. §9 `V2Gate` 재사용 ✔.
- **SPEC-007** — U-1~U-7 규격 대조 ✔(§1-3·§1-4·§2·§3 참조). Case Matrix 15행: `validation_error` 인라인(`:173-176`) · `not_found`(W-3) · `invalid_meeting_status` 토스트+재조회(`:136-141` · `useMeetingStream.ts:255-261`) · `meeting_stream_active`(`:250-254`) · `disconnected upstream/write_failed`(`:267-270`) · 예고 없는 close ✔ · 마이크 실패 ✔ · 배치 실패/스키마/강등 표시 없음 ✔ · 줄 5xx 토스트+입력 유지 ✔ · 안건 5xx 토스트+배지 그대로 ✔ · 트랜스크립트 실패 ✔ · 첨부 삭제됨(WORK-006 드로어) ✔ · 로컬 드롭 요청 0 ✔ · `4401` ✔. **F-1 이 U-4 기대 결과 1건 미충족.** §6 26개 중 앱 창 실물 2개 남음(§1-7).
- **WORK-007** — Phase 1: 리비전 없음(`0005` 가 이미 보유 — `alembic/versions/0005_meeting_domain.py` 에 `recording_started_at`·`source_agenda_id`·`uq_meeting_agenda_human_active`, `test_two_active_human_agendas_are_rejected_by_partial_unique`) ✔ · enums 는 `dto/enums.py`(G-9) · env ✔ · 어댑터 3 + 대역 3 ✔. Phase 2~4 검증 항목 전부 테스트 존재(§1 표들). Phase 5·6 검증 항목 → `useMeetingStream.test`·`AgendaLineTree.test`·`TranscriptPanel.test`·`PromptBar.test`·`MeetingStatusBar.test`·`MeetingLiveView.test` + `static.test.ts` ⑪~⑭. 범위 밖 변경: 백엔드가 `task_service`·`core/constants`·`core/security`·`test_auth` 등에 `field` 를 넣은 것은 브리프 §4-b 지시분 · 프론트가 `MeetingPreviewPanel`·`MeetingScheduledPage` 를 만진 것은 TopBar 흡수의 이름 바꿈 — 둘 다 범위 안. `.env.example` 은 루트(WP 는 `app/back/`) — 기존 관습.

## 5. 문서 공백

| # | 어디 | 무엇 | 필요한 것 |
|---|---|---|---|
| **D-1** | **SPEC-006 §4 필드 소유 표 L447** | `task` 요약을 `{ id, title, status, dueDate, isDeleted }` 로 적어 **`workType` 이 없다.** SPEC-007 L378·L566, SPEC-008 L450·L484, [09] L671 은 있다. 이 표가 「이름의 정본」이라 백엔드가 여기를 따라 빠뜨렸을 가능성이 크다(F-1) | 표에 `workType{ id, name, colorToken, isDeleted }` 추가. 세 SPEC 정합 |
| **D-2** | DEC-003 §7 · SPEC-006 §4 `/start` Case Matrix · SPEC-007 §4 웜스타트 | **웜스타트 제출이 실패하면?** 목록 밖이라 전파(500)가 맞고 코드도 그렇게 한다(`meeting_service.py:451` · `test_warm_start_failure_propagates_and_is_not_hidden`). 그런데 전이는 이미 커밋돼 회의는 `recording` + `ai_session_id NULL` 로 남고, 이후 모든 배치가 `RuntimeError`(`meeting_batch_service.py:234-236`)로 끝난다. 사용자는 500 토스트 뒤 새로고침하면 회의 중 화면을 본다 | 정책 결정 — 전이를 되돌릴지 · 배치 없이 진행할지 · 재제출 표면을 둘지. 최소한 SPEC-006 `/start` Case Matrix 에 행 하나 |
| **D-3** | `backend/README.md` §2 표 L37 ↔ §7 L175 · WP L169 | service `commit()` 금지와 「읽기 → (커밋) → 외부 호출」이 충돌한다. 요청 중간 커밋을 **누가** 하나(router? service? 별도 유닛?)가 없다(W-1) | §7 외부 호출 행에 자리를 명시하고 §2 표에 예외로 부기 |
| D-4 | `backend/README.md` §5-3 · §8-1 | 「전파 = 500 + 스택 로그」는 요청 경로 기준. 백그라운드 태스크(배치 `schedule()`)의 설계 밖 예외가 어디로 가는지 없다(W-2). WP Phase 4 L265 「500 으로 전파」는 직접 호출에서만 성립 | 백그라운드 태스크 예외 = 스택 로그 + 태스크 종료(상태 행 남기지 않음) 를 §5-3 에 |
| D-5 | SPEC-007 §4 검증 표 2·3단 | `kind≠task` 인데 `taskId` 가 온 출력 — 스키마 위반(폐기)인지 무시인지 없다. 코드는 무음 정정(W-4) | 2단에 「`kind≠task` 의 `taskId` 비-null」을 넣거나 3단에 「떼고 넘긴다 · 로그」를 넣거나 |
| D-6 | SPEC-007 §4 Case Matrix L456 · BE §8-2 | 인라인 문구 예시 「2000자까지 입력할 수 있습니다」를 화면이 낼 수 없다 — 서버 `detail` 은 고정 「입력값을 확인해 주세요」(`main.py:66`) 이고 프론트는 그것을 그대로 그린다(`MeetingLiveView.tsx:175`). G-2 의 연장 — `field` 는 이제 오지만 **문구의 주인**이 없다 | `field → 문구` 매핑을 화면 몫으로 못박든지(FE §3-5), 서버 `detail` 을 필드별로 하든지 |
| D-7 | SPEC-007 §4 close code 표 L305 | `4404` 행이 문구만 있고 **상태 바를 어떻게 두는지** 없다(W-3) | 「상태 바 갱신 없이 상세 재조회 → 없는 회의록 화면」 |
| **D-8** | WP L43 Depends on(「WORK-001 — compose 의 Redis·worker」) · Pre-deploy L339 | **`docker-compose.local.yml` 에 Redis·open-kknaks worker 가 없다**(`:8-24` db·api 뿐, `:3` 주석). WP 가 있다고 전제한 채 발주됐다. `config.py:46-48` 기본값 `redis://localhost:6379` 는 컨테이너 안에서 닿지 않는다 | WP 전제 정정 + Ops 항목으로 compose 보강 발주. 이게 없으면 §1-7 #10 대로 `/start` 가 전부 500 |
| D-9 | `backend/README.md` §5-1 · §8-2 각주 | WS 의 `status≠recording`·단일 세션 판정이 close code 로 나가야 해서 `_assert_allowed` 표를 못 쓴다 — `meeting_stream_service.py:126-132` 가 따로 비교한다. 「상태 가드 1곳」 규칙과의 관계가 문서에 없어 다음 검수가 두 번째 가드로 오인할 수 있다 | §5-1 에 「WS 판정은 stream service 가 close code 로, REST 표와 별개」 한 줄 |
| D-10 | WORK-007 WP L104 · L186 | `core/enums.py` — **G-9 재발.** 코드는 `dto/enums.py`(`BatchTriggerCause`·`StreamPauseReason`·`StreamDisconnectReason` 도 거기). L105 `app/back/.env.example` 도 실제는 루트 `.env.example` | WP 경로 정정 · `backend/README.md` §4 트리에 `dto/enums.py` |
| D-11 | SPEC-007 §5 트리거 ② L589 ↔ Flow L507-510 · U-2 L128 | ②는 「`state:"active"` 성공」만 트리거인데 Flow 는 `done` 뒤에도 평가한다. 코드는 `done` 으로 **다음 `next` 가 자동 활성될 때만** 평가하고(`meeting_service.py:599-606`) 마지막 안건 완료는 평가하지 않는다 | 「전환」의 정의 — 활성 안건이 바뀔 때(자동 활성 포함)인지, `done` 자체인지 |
| D-12 | SPEC-007 §4 WS 오류 프레임 L298 · close 표 | `error` 프레임 뒤 서버가 닫을 때 **close code** 가 없다. 코드는 `1011`(`meeting_stream_service.py:68`) — 화면은 「그 밖」으로 받아 맞게 동작하나 계약에 값이 없다 | L298 에 「이후 close `1011`」 부기 |
| D-13 | SPEC-007 §4 L320 ↔ SPEC-008 §4 L490 | `POST …/lines` 응답이 SPEC-007 은 `201 LineItem`, SPEC-008 은 `201 MeetingDetail`. 코디 판정(§1-8)대로 회의 중은 `LineItem` 이 맞다 — 그러면 SPEC-008 의 종료 후 편집이 같은 표면에서 형태를 바꾸는 셈이라 WORK-008 이 밟는다 | SPEC-008 §4 L490 을 `LineItem` 으로 맞추거나, 상태별 응답 형태가 다르다고 명시 |

## 6. WORK-006 검수 잔여 5건 — 현재 상태

| # | 무엇 | 코드 | 문서 | 상태 |
|---|---|---|---|---|
| **G-2** | `validation_error` 에 어느 필드인지 없음 | **닫힘** — `core/exceptions.py` `ValidationError(field=)` · `main.py:37·41-68` 두 핸들러 · 회의·업무·설정·인증 전부 같은 모양(`test_validation_error_names_the_first_invalid_field` · `test_task_and_setting_validation_errors_share_the_field_shape`). 프론트는 `618d5bb` 부터 `field` 소비 | `backend/README.md` §8-2 표에 `validation_error` 행 자체가 없고 `field` 언급 0(grep) | **코드 닫힘 · 문서 남음** — §8-2 에 행 추가(`{detail, code, field}`) + D-6 |
| G-3 | 문서함 전 임시 계약(`doc` → `validation_error`)이 SPEC-006 에 각주로 없음 | 그대로 — `meeting_service.py` `_validate_attachment` 가 `kind=doc` 을 `validation_error("kind")` 로 거부 | SPEC-006 §4 에 각주 없음(`unsupported_file_type` 행만 · grep) | **남음** — 문서 |
| G-5 | 유형·프로젝트 훅·`useRowFailures` 가 사는 층 | **닫힘** — `lib/hooks/useRowFailures.ts`·`useWorkSettings.ts`·`lib/api/errors.ts`(`inlineErrorMessage`) 로 승격(`618d5bb`), WORK-007 도 그것을 쓴다 | `frontend/README.md` §2 규칙 4 에 자리 명시 없음(grep 0) | **코드 닫힘 · 문서 남음** |
| G-6 | SPEC-006 U-7 목록 행 규격(padding 11/12 · r10 · 1px · 타일 32) ↔ `ItemRow`(h44 · 테두리 없음 · 22 타일) | 그대로 `ItemRow` — 회의 중 첨부 탭도 같은 것 | SPEC-006 L226 그대로 | **남음** — 문서 |
| G-9 | WP 의 `core/enums.py`·`MeetingAttachmentKind` 표기 | 코드는 `dto/enums.py`·`AttachmentKind` 공유로 일관 | WORK-006 L109·L191 그대로 · **WORK-007 L104·L186 이 같은 오기를 반복**(D-10) | **남음** — 문서, 재발 |

## 7. 가장 심각한 3건

1. **F-1 + D-1 — AI 업무 줄 유형 배지의 원천이 없다.** SPEC-007·008·[09] 가 한목소리로 `task.workType` 을 요구하는데 SPEC-006 필드 소유 표 하나가 빠뜨렸고 백엔드가 그 표를 따랐다. WORK-008 「업무 갱신」 버튼이 같은 자리(라벨 + 배지 + 버튼)라 지금 안 닫으면 다음 work 가 두 번 고친다. 수정은 작다(조인 1 · 필드 1 · 배지 1).
2. **D-8 + §1-7 #10 — compose 에 Redis·worker 가 없다.** WP 가 「WORK-001 이 넣었다」고 전제했지만 `docker-compose.local.yml` 은 db·api 뿐이다. 이 상태로는 `/start` 의 웜스타트가 브로커에서 예외를 내고, D-2 대로 회의는 `recording` 으로 남는다 — **회의를 한 번도 시작할 수 없다.** 코드 FAIL 이 아니라 인프라·문서 문제이고, 회의록 실물 확인 전부가 이것에 막혀 있다.
3. **F-2 — `startCapture` 의 `catch {}`.** 실물 확인이 안 된 바로 그 자리(WKWebView `MediaRecorder`)의 실패가 「마이크 연결이 끊겼습니다」로 위장된다. 정책이 가장 강하게 말한 원칙(「설계한 실패만 처리한다 — 광범위한 포착은 어디서 깨졌는지를 가린다」)의 위반이고, 실물 확인 때 원인을 찾지 못하게 만든다. 한 줄 수정.
