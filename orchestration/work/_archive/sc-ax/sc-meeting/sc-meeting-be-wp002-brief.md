# [backend] WP-002 — 스트림 중계: `WS /api/meetings/{id}/stream` · 서버 소유 Soniox 세션 · 오디오 원본 · 참석자 fan-out

너는 **sc-ax `backend` 워커**다. WP-001 을 한 세션이면 그 맥락을 써도 된다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/backend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`, HEAD `5751efa` = WP-001+WP-006 커밋 → PR `main`)

⚠ `frontend/` 는 읽기만(FE 워커가 Phase 3 를 뒤에 붙인다). 너는 `backend/` 만 쓴다. **`frontend/src/liveTranscription.ts` 삭제는 FE 몫** — 너는 백엔드 직결 표면만 걷는다.

## 1. SSOT — 먼저 읽을 것

- **SPEC**: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` (0.4.1, 커밋 a54c2e6e0) — **§5.2 오디오 중계 · §5.3 스트림 계약 · §5.4 전사와 화자 · §5.5 오디오 원본 · §5.6 한도**, §2.2 데모 범위 밖, §11 폐기/계승.
- **WP**: 같은 리포 `30-work/work-002-meeting-stream-relay.md` — Scope·Code Surface·Domain·Interface Contract·Phase 1~3 검증 = 완료 조건.
- **원형(task-management, 읽기만)**: `/Users/kknaks/git/toy_pr2/task_management/app/back/api/meeting_stream_router.py`(WS 라우트·첫 프레임 5초 인증·dto↔JSON) · `service/meeting_stream_service.py`(세션 레지스트리 `is_active`·`serve`·`close_for_end`·`push_ai_batch` · `StreamSession.run/_pump_client/_feed/_pump_upstream/_handle_tokens/_close_block/_persist_block/_pump_outbox/_send_ready/_fail` · `finally` 종료) · `integrations/soniox.py`(`SttConnector/SttSession` 프로토콜 · `build_config` · `SonioxSession.tokens()` · `install_connector` 테스트 대역) · `dto/meeting_stream.py` · `schemas/meeting_stream.py` · `tests/test_meeting_stream.py`·`tests/fakes/soniox.py`(테스트 패턴). 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md` §4.
- **현행 코드 사실**: `orchestration/work/sc-meeting/survey-01-ai-provider-report.md` §4.1-①②(브라우저 직결·2-pass) · `soniox-study.md`(`orchestration/work/_archive/task-management/docs-v1/`).
- **코드 검수 2 이월**: `orchestration/work/sc-meeting/review-code-02-report.md` W9·W5·W6.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

현행은 브라우저가 Soniox 임시 키로 직접 websocket 을 열고, 확정 구간을 POST 로 되돌려 보내며, 녹음 파일을 종료 후 `stt-async-v5` 로 재전사한다. 새 계약은 **브라우저→우리 서버 WS→Soniox** 중계, **실시간 전사가 정본**, **오디오 원본은 중계 경로에서 서버가 적재**, 참석자는 같은 WS 에 구독으로 붙는다. 이 WP 는 그 통로만 만든다. AI 배치(WP-003)·합성(WP-004)은 이 통로를 **소비**한다 — `push_ai_batch` 같은 push 통로와 「블록 확정 이벤트·미처리 커서」 자리만 열어 둔다.

## 3. 계약 — SPEC §5.3 그대로 + 코디 확정 사항

- **인증(코디 확정 — ax 는 세션 쿠키)**: WS 핸드셰이크의 `scax_session` 쿠키로 principal 을 푼다(`session_principal` 과 같은 판정). 첫 프레임 `{"type":"auth","role":"upstream"|"subscribe","audio":{"format":…,"sampleRate":…,"channels":…}}` — `accessToken` 은 **받지 않는다**(있어도 무시). 첫 프레임 5초 안, 없으면 `4401`. 회의 없음·참석자 아님 `4404`(존재 숨김). 상태≠in_progress 또는 업스트림 이미 있음 `4409`(reason 에 `invalid_meeting_status` | `meeting_stream_active`). 회의 종료로 서버가 닫음 `1000`.
- **클라→서버**: 바이너리 오디오 청크(`ready` 전은 버림). `pause/resume` 프레임 **없음**(오면 무시하고 닫지 않는다).
- **서버→클라**: `ready {meetingStartedAt, latestBatchSeq, speakerCount}` · `transcript.partial {segments:[{speakerLabel, atMs, text}]}`(교체, 저장 안 함) · `transcript.final {item:{id, speakerLabel, atMs, endMs, content}}`(추가, 적재와 동시 push) · `ai.batch {seq, agendas:[…]}`(WP-003 이 채움 — 여기선 push 통로만) · `error {code:"meeting_stream_disconnected", reason:"upstream"|"write_failed"}` → close.
- **원형과 다른 점**: pause/resume 없음 · 화자 이름 없음(익명 `speakerLabel` 만) · 회의 id 는 UUID · 인증은 쿠키 · 상태 어휘 `in_progress`.
- **처리 순서**: 오디오 청크 = ① 원본 append → ② 업스트림 전달. ① 실패 = `error write_failed` + 종료. 업스트림은 인증 뒤에 연다(과금).
- **블록 경계(구현 재량, 값은 정해서 상수로)**: 같은 화자 확정 토큰을 화자 변경 · 300자 · 2초 침묵에서 닫는다(원형과 동일). `atMs` 는 회의 시작(`started` 전이 시각) 기준.
- **Soniox 설정**: `stt-rt-v5` · `language_hints:["ko"]` · `enable_speaker_diarization:true` · endpoint detection 미사용 · 키는 서버 env `SONIOX_API_KEY`(Makefile 의 `SONIOX_ENV_FILE` 관례).
- **저장 모델**(WP §Domain): `MeetingTranscript`(확정 블록: meeting_id · seq · speaker_label · at_ms · end_ms · text) · `MeetingRecordingFile`(원본 위치·무결성, **API 응답 금지**). 현행 `meeting_raw_transcript_*`·`refinement_*`·`summary_*`·`speaker_identity_*` 계열은 폐기(§11.1) — reset_demo 스키마에서 제거.
- **종료**: WP-001 의 `POST /end`(in_progress→summarizing) 뒤에 `close_for_end(meeting_id)` 가 업스트림·구독 전부 `1000` 으로 닫는다(WP-004 가 그 뒤 합성을 얹는다).

## 4. 먼저 읽을 핵심 파일

- 원형 세 파일(§1) 전문 — 특히 `StreamSession` 의 `_feed`(append→forward) · `_pump_outbox`(백프레셔: 잠정만 버림) · `finally`.
- `backend/src/ax_workspace/entrypoints/http.py` — `session_principal`·쿠키 이름·현행 회의 라우트(recordings/start·stop·realtime 잔존분 제거 대상).
- `backend/src/ax_workspace/platform/soniox.py`(현행 임시키·async 전사 — 재작성) · `platform/recordings.py`(로컬 저장 port — 원본 append 로 확장) · `bootstrap/application.py`·`bootstrap/meeting_worker.py`(finalize 잡·2-pass 경로 — 폐기).
- `backend/tests/contract/test_meeting_recordings.py`·`test_meeting_followups.py`·`test_meeting_material_search.py` — 2-pass 에 기대던 픽스처. **새 전사 모델로 다시 세운다**(`meeting_transcript_record` 내부 판 어댑터 제거).
- `backend/pyproject.toml` — `websockets` 17.1 이미 있음. 추가 의존 금지 없이 되는지 확인.

## 5. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`
- `frontend/` 읽기 전용.

## 6. 구현 단계 (WP-002 Phase 1→2→3)

1. **Phase 1** — WS 라우트(쿠키 인증·첫 프레임·close code) · 참석/상태 판정 · 회의당 세션 레지스트리(업스트림 하나) · `finally` 종료. 원형의 `StreamClient` 포트 패턴 그대로(dto↔JSON 은 entrypoint 층에서만). 테스트 대역(`install_connector` 식)으로 WS 계약 테스트.
2. **Phase 2** — Soniox 실시간 어댑터(`SttConnector/SttSession`) · 청크 append→forward · 적재 실패 시 `error write_failed`+종료 · **현행 직결 표면 제거**: realtime-credential 잔존물·recordings/start·stop 라우트·`stt-async-v5` 재전사·finalize 잡·`meeting_transcript_record` 어댑터. 폐기 테이블 제거.
3. **Phase 3** — 잠정 push(저장 없음)·확정 블록 적재+push · 구독 fan-out · 백프레셔(잠정만 버림) · `/end` 뒤 서버 닫기(`1000`) · `push_ai_batch(meeting_id, seq, payload)` 통로와 「미처리 확정 블록 커서」 조회 함수(WP-003 용, 호출자 없음).
4. **이월 WARN**: `MeetingLine.author` nullable(W9) · `MeetingVersionConflict` 409(W5) · `CreateMeetingRequest extra="forbid"`(W6).
5. §8 검증 → 자기점검 → 완료 보고.

## 7. 범위 제약 — 하지 말 것

- AI 배치·합성·자료·공유·화면 금지(WP-003~006). `push_ai_batch` 는 통로만.
- 일시정지·재개·마이크·화자 이름·세션 회전(300분)·자동 재연결 — 만들지 않는다.
- 계약(§3) 필드명·close code 변경 금지. 프론트 수정 금지. Alembic 금지(reset_demo). 비밀값 커밋 금지.
- **실제 Soniox 호출은 테스트에서 하지 않는다**(대역). 키가 있는 실물 확인은 코디가 한다.
- `make local-stack`·dev 서버·5176/8001 사용 금지. `make reset-demo` 는 1회 허용(코디 스택이 죽는 건 예상됨 — 완료 보고에 적어라).

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration' + uv run pytest -q tests/architecture (경계 테스트는 항상). 전체 스위트·integration 마커 금지 — 사용자 방침. 자기점검 — modules/*/domain.py·application.py 가 fastapi/mcp/sqlalchemy/websockets 를 import 하지 않는가 · entrypoints 가 platform 구현을 직접 import 하지 않는가 · 스키마 변경을 reset_demo 밖에서 하지 않았는가. 검증은 1회만
```

- WP-002 Phase 1~3 검증 9항목을 전부 테스트로: 두 번째 업스트림 4409 · 비참석 4404(존재 숨김) · 상태≠in_progress 4409 · 번들/응답에 provider 주소·키 없음 · append 실패 주입 시 즉시 종료 · 원본 파일 잔존 + 응답 미노출 · 잠정 미저장 · 구독자 둘 동일 확정 수신 · `/end` 뒤 전부 닫힘.
- `make reset-demo` 1회 성공.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context> \
  --subject "backend 완료: WP-002 스트림 중계" \
  --body "변경 파일 / 구현 요약(라우트·세션·어댑터·저장) / 검증 수치 / 계약 준수(§3 close code·프레임) / 폐기 제거 목록 / WP-003·004 인계(push 통로·커서) / 이월 WARN 처리 / reset-demo 결과 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-002. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라.
