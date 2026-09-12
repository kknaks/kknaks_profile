# [frontend] WP-006 Phase 3 — 진행 중 화면: WS 스트림 클라이언트 · 마이크 업스트림 · 실시간 스크립트 · 메모 탭 · AI 요약 탭

너는 **sc-ax `frontend` 워커**다. WP-006 P1·2 를 한 세션이면 그 맥락을 쓴다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/frontend/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (HEAD `5751efa` → PR `main`)

⚠ **backend 워커가 같은 워크트리에서 WP-002(WS 서버)를 병렬로 만든다.** `backend/` 읽기만. 서버는 네 작업 중 아직 없다 — §3 계약대로 만들고 **WS 를 모킹**해 테스트한다. 실물 연결은 코디가 붙인다.

## 1. SSOT

- **SPEC 0.4.1** `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` — **§5.2 · §5.3 스트림 계약(인증=세션 쿠키, 첫 프레임 {type:auth, role, audio}) · §5.4 · §6 메모 트랙 · §7 AI 중간 요약(ai.batch 통째 교체)**.
- **WP-006** `30-work/work-006-meeting-screens.md` **Phase 3** 작업·검증 4건.
- **시안(정본)** `orchestration/work/sc-meeting/design/회의실.dc.html` 진행 중 상태 — 두 탭(「메모」 기본 · 「AI 요약」), 진행 표시(경과 시간), 스크립트 탭 실시간(잠정 회색 교체·확정 추가·화자 N), 메모 입력(안건 드롭다운 + 한 줄 + 던지기 secondary 버튼). `REPORT-회의실-v2.md` 가시성 표.
- 현행: `frontend/src/liveTranscription.ts`(브라우저 직결 — **삭제**) · `MeetingDrawer.tsx`·`MeetingDrawer.test.tsx`·`CalendarMeetings.test.tsx`(구 드로어 — **삭제**, WP-002 와 한 배포) · `api.ts` 의 realtime 함수(삭제).

## 2. 계약

**WS `/api/meetings/{meetingId}/stream`** (같은 오리진, 쿠키가 실림)
- 연결 직후 첫 프레임: `{"type":"auth","role":"upstream"|"subscribe","audio":{"format":"…","sampleRate":N,"channels":1}}` — `audio` 는 upstream 만. 5초 안.
- upstream: `ready` 받은 뒤 바이너리 오디오 청크 전송(64KB 이하, 250ms 이하 간격). `role` 은 **회의를 시작한 사람(만든 사람) = upstream**, 그 외 참석자 = subscribe.
- 서버→: `ready{meetingStartedAt, latestBatchSeq, speakerCount}` · `transcript.partial{segments[{speakerLabel, atMs, text}]}`(**교체 렌더**, 회색) · `transcript.final{item{id, speakerLabel, atMs, endMs, content}}`(**추가 렌더**) · `ai.batch{seq, agendas[…]}`(**AI 탭 통째 교체**, id 붙들지 않음) · `error{code:"meeting_stream_disconnected", reason}` → 닫힘.
- close: `4401` 인증 → 로그인으로 · `4404` → 「없는 회의」 · `4409` reason `invalid_meeting_status`(상세 재조회) | `meeting_stream_active`(「다른 창에서 진행 중」 표시 — 문구는 OQ-311, 임시 문구 쓰고 리포트에 적어라) · `1000` 회의 종료 → 상세 재조회(정리 중 화면).
- **자동 재연결·재시도 없음.** 끊기면 그대로 드러낸다(상태 줄에 표시).
- **pause/resume 없음.**

**메모 쓰기** (WP-003 소유 — 아직 없다. api.ts 에 함수 두고 모킹): `POST /api/meetings/{id}/agendas/{agendaId}/lines` body `{text}` → `Line`(track memo). 만든 사람만, in_progress 만. 응답 줄을 메모 탭에 바로 붙인다(낙관 렌더 금지 — 응답 후).

**오디오**: `getUserMedia({audio:true})` → 16kHz mono PCM(AudioWorklet 또는 MediaRecorder webm/opus 중 하나 — **고른 형식을 첫 프레임 `audio` 에 그대로 선언**하고 리포트에 적어라. 서버는 선언을 Soniox 에 그대로 넘긴다). 마이크 거부 시 화면이 멈추지 않고 상태 줄에 표시.

## 3. 그릴 것 (시안 진행 중 상태 그대로)

- 상단 진행 표시(경과 시간 = now − meetingStartedAt).
- 왼쪽 탭 둘: 「메모」(안건 드롭다운 기본 = 첫 안건 · 한 줄 입력 · 던지기 → 메모 줄이 그 안건 블록 아래 쌓임 · 만든 사람만 입력 칸) · 「AI 요약」(ai.batch 도착 시 안건 블록 전체 교체, 스크롤 튀지 않게 — 사용자가 위로 스크롤 중이면 유지).
- 오른쪽 「스크립트」 탭: 확정 줄 추가(화자 N · 시각 mm:ss · 본문), 잠정 줄 회색 교체, 메모 줄도 시각 자리에 「메모 · 이름」으로 섞임(E26).
- [회의 종료] → `POST /end` → 서버가 WS 닫음(1000) → 「정리 중」 화면.
- 상태 줄: 연결 중 / 진행 중 / 끊김(사유) / 다른 창에서 진행 중.

## 4. allowed_paths

- `frontend/` 만. `backend/` 읽기 전용.

## 5. 하지 말 것

- pause/resume·자동 재연결·화자 이름·알림·AI 채팅 — 금지.
- 시안에 없는 요소·문구 금지(스트림 안내 문구는 OQ-311 — 임시 문구는 리포트에 표로).
- `api.ts` 밖 fetch/WebSocket 생성 금지(WS 클라이언트도 `api.ts` 또는 `frontend/src/meetings/stream.ts` 한 곳). hex 리터럴 금지. dev 서버·5176 금지.

## 6. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <네가 만들거나 고친 테스트만>. 전체 빌드·e2e 금지. WS·getUserMedia 는 모킹. 검증 1회
```

- WP-006 P3 검증 4항목 + 계약 항목을 테스트로: 비소유 참석자에게 메모 입력 칸 없음 · ai.batch 통째 교체와 스크롤 유지 · 회의 종료 시 연결 닫히고 정리 중 화면 · 상단에 AI 채팅·알림 없음 · partial 교체/final 추가 렌더 · 4409 meeting_stream_active 표시 · 끊김 표시(재연결 없음) · 첫 프레임 형식.
- `git rm` 대상 삭제 후 tsc 통과: `liveTranscription.ts` · `MeetingDrawer.tsx` · `MeetingDrawer.test.tsx` · `CalendarMeetings.test.tsx`(캘린더 회의 탭 잔재 포함).

## 7. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WP-006 Phase 3 스트림 화면" \
  --body "변경/삭제 파일 / 오디오 형식 선언 / 검증 수치 / 계약 준수 / 임시 문구 표 / TODO(WP-003 메모 API) / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WP-006 Phase 3. 상세는 인박스." --enter
```
