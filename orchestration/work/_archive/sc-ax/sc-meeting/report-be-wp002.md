WP-002 완료. 브라우저→우리 서버 WS→Soniox 중계 통로를 세우고, 확정 발화 적재·오디오 원본 append·참석자 fan-out·종료 시 서버 닫기를 붙였으며, 파일 재전사 2-pass 계열을 스키마·라우트·워커·자료 다리까지 전부 걷어냈다. 검증 254 passed / 0 failed (스트림 20 + 회의 31 + 영향 파일 전부 + tests/architecture 15, -m 'not integration', 1회) · make reset-demo 새 스키마로 성공. 남은 것은 FE Phase 3 와 WP-003/004 가 소비할 통로 둘(push_ai_batch · 미처리 커서)의 호출자뿐이다.

## 변경 파일 (신규 3 · 수정 14 · 삭제 9)
신규: modules/meetings/stream.py(프레임·포트·블록 경계) · modules/meetings/stream_service.py(레지스트리·세션) · tests/contract/test_meeting_stream.py(20건)
수정: entrypoints/http.py(WS 라우트·프레임 변환·폐기 라우트 제거) · entrypoints/http_auth.py(connection_principal) · platform/soniox.py(실시간 재작성) · platform/recordings.py(append) · platform/persistence.py · platform/meetings.py · platform/native_materials.py · bootstrap/application.py(_SessionStreamGateway·조립) · bootstrap/material_sources.py · bootstrap/settings.py · modules/meetings/application.py · modules/jobs/domain.py · Makefile · docs/domain-model.md · tests/architecture/test_architecture.py · tests/contract/test_relation_graph_scale.py · tests/contract/test_material_search_public.py
삭제: modules/meetings/{transcription,refinement,summary,jobs,recordings}.py · bootstrap/meeting_worker.py · entrypoints/meeting_worker.py · tests/contract/{test_meeting_recordings,test_meeting_followups,test_meeting_material_search,test_meeting_realtime는 WP-001에서,test_soniox_adapter}.py

## 구현 요약
- **라우트**: `WS /api/meetings/{id}/stream` 하나. 핸드셰이크의 `scax_session` 쿠키로 principal 을 풀고(`connection_principal`, 개발 페르소나 헤더는 REST 와 같은 이음새), 첫 프레임 5초. dto↔JSON 변환은 `_WebSocketStreamClient`·`_stream_message` 에서만.
- **세션**: `MeetingStreamService` 가 회의당 `_Room`(업스트림 하나 + 구독 여럿). `serve` 가 참석(4404)·상태(4409)·단일 업스트림(4409) 을 가르고 `finally` 가 레지스트리에서 빼고 provider 를 닫는다. 업스트림은 인증 뒤에 연다(과금).
- **어댑터**: `SonioxRealtimeConnector` — `stt-rt-v5` · `language_hints:["ko"]` · `enable_speaker_diarization:true` · endpoint detection 키 없음. 키는 서버 env 만. 실패는 `SttUpstreamError` 하나.
- **저장**: `meeting_transcripts`(확정 블록 meeting_id·seq·speaker_label·at_ms·end_ms·text) · `meeting_recording_files`(원본 위치·무결성, 응답 금지) · `meetings.started_at`(at_ms 의 기준점, /start 와 quick-start 가 채운다).
- **블록 경계**: 화자 변경 · 300자 · 2초 침묵 (`stream.py` 상수 하나에만). 빈 블록은 행이 되지 않는다.

## 계약 준수 (§3)
close code 4401(첫 프레임 없음·무효, 사유 안 흘림) · 4404(회의 없음·비참석, 존재 숨김) · 4409(`invalid_meeting_status`|`meeting_stream_active`) · 1000(`/end`) · 1011(error 뒤). 프레임 `ready{meetingStartedAt,latestBatchSeq,speakerCount}` · `transcript.partial{segments[{speakerLabel,atMs,text}]}` · `transcript.final{item{id,speakerLabel,atMs,endMs,content}}` · `ai.batch{seq,agendas}` · `error{code:"meeting_stream_disconnected",reason:"upstream"|"write_failed"}`. `accessToken` 은 와도 무시, `pause`/`resume` 은 버리고 닫지 않는다. 처리 순서 ① 원본 append → ② 업스트림 전달, ① 실패 시 ②로 가지 않는다(테스트로 고정).

## 코디 추가 지시 둘 — 반영
① **컨테이너 형식 매핑**: `build_config` 가 `webm/opus`·`webm`·`ogg`·`mp3`·`wav` 등 컨테이너면 `audio_format='auto'` 로 보내고 `sample_rate`·`num_channels` 를 뺀다. raw(`pcm_s16le` 등)만 선언값 그대로. 테스트 `test_a_container_format_reaches_the_provider_as_auto_without_invented_numbers` 로 양쪽 고정. 파일 확장자도 `webm/opus`→`.webm` 로 매핑.
② **청크 순서 보존**: 받은 순서 그대로 append 하고 그대로 흘린다 — 재프레이밍·드롭·버퍼링 없음. `LocalDirectoryRecordingStorage.append` 는 `open("ab")` 한 번이고, 테스트가 세 청크를 보낸 뒤 원본 파일 바이트와 업스트림 수신 목록이 **둘 다 순서 그대로**임을 확인한다.

## 폐기 제거 목록 (SPEC §11.1)
라우트: `recordings/start`·`recordings/{id}/stop`·`realtime-credential`·`realtime-segments`·`summaries/{id}/statements/{i}/promote`·`speaker-assignments`·`meetings/{id}/materials/{mid}/content`.
표: `meeting_recordings`·`meeting_raw_transcript_revisions`·`meeting_raw_transcript_segments`·`meeting_speaker_identity_assignments`·`meeting_transcript_refinement_revisions`·`meeting_transcript_refinement_segments`·`meeting_summary_suggestions`·`meeting_summary_evidence`·`meeting_followup_promotions`.
코드: 2-pass `stt-async-v5` 어댑터 · finalize durable job(`meeting.recording.finalize`)·워커·Makefile `meeting-worker` 타깃(local-stack·acceptance 에서도 제거, 스키마 probe 를 `meeting_transcripts` 로) · 회의 native 자료 다리(`meeting_raw`/`meeting_refinement`/`meeting_recording` kind + material_sources 회의 분기) · `meeting_queue_*`·`meeting_worker_concurrency` 설정.

## WP-003·004 인계
- `WorkflowApplication.push_meeting_ai_batch(meeting_id, seq=, agendas=)` — AI 트랙 전체 push 통로. 호출자 없음.
- `WorkflowApplication.unprocessed_meeting_transcript(meeting_id, after_seq=)` — 미처리 확정 블록 커서. 호출자 없음. 블록이 닫히는 자리(`_persist_block`)가 배치 트리거의 자리다.
- `WorkflowApplication.close_meeting_stream(meeting_id)` — `/end` 가 이미 부른다. 합성 job 은 그 뒤에 얹으면 된다.
- `meeting_followup_tasks` 는 지금 빈 목록이다 — 승격이 요약 문장에서 안건의 「다음 할 일」(`meeting_todos.linked_*`, WP-001 이 만든 자리)로 옮겨 갔다. 회의–업무 그래프 간선은 WP-004 가 다시 세운다.
- **⚠ `/api/materials/search` 에서 회의 내용이 일시적으로 빠진다** — 회의 native 자료 다리를 폐기 테이블과 함께 걷었다(코디 결정 A). SCAX-WP-005 가 새 `meeting_transcripts` 위에 `meeting_transcript` kind 로 다시 세운다.

## 이월 WARN
- **W9**: BE 는 이미 `MeetingLine.author_id` 를 nullable 로 두고 `author: member_id|null` 로 낸다. `viewModels.ts:891` 의 `author: string` 은 FE 몫이다(AI 줄이 서는 WP-003 전에).
- **W5**: `MeetingVersionConflict` → **409** 로 매핑했다(`MeetingStateConflict` 와 같은 줄).
- **W6**: `CreateMeetingRequest` 에 `extra="forbid"` 를 넣었다.

## 그 밖
- 아키텍처 테스트 신설 `test_the_browser_never_learns_the_stt_provider` — 프론트 소스에 provider 주소·모델·키 이름이 없고, 백엔드에서도 그 이름을 아는 파일은 `platform/soniox.py` 와 조립층 `bootstrap/application.py` 둘뿐임을 고정한다.
- 연결마다 event loop 가 다를 수 있어(시험 하네스·멀티 루프 서버) `_Outbox` 가 큐 소유 루프를 기억하고 밖에서 온 것은 `call_soon_threadsafe` 로 깨운다. 소켓을 직접 만지는 것은 pump 하나이고 **닫기도 프레임으로 온다** — 다른 연결이 남의 소켓을 만지지 않는다.
- `make reset-demo` 1회 성공(코디 로컬 스택이 그 시점에 끊겼을 수 있다 — 예상된 결과).
- 실제 Soniox 는 부르지 않았다. 대역(`FakeSttConnector`)으로만 검증했고 실물 확인은 코디 몫이다.
- 미결(WP Open Issues 그대로): 업스트림 소유자 이탈 시 승계(`OQ-305`) · 구독자에게 잠정까지 밀지(`OQ-310`, 지금은 업스트림에게만) · 오디오 형식 실측.
- 커밋·push·PR 하지 않았다. `frontend/` 는 읽기만 했다.