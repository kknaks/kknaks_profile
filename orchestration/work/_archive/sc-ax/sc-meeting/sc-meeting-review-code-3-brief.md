# [reviewer_code] 코드 검수 3 — WP-002 스트림 중계 + WP-006 P3 진행 중 화면 (차분만)

너는 **sc-ax `reviewer_code` 워커**다. 검수 1·2 를 한 세션이다 — 그 위에서 **이번 커밋 차분만** 본다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` — 읽기만. 범위 = `git diff 5751efa..HEAD`(HEAD 하나 = WP-002 + FE P3). 서버·reset·5176/8001 금지. `backend/` 에서는 **다른 워커(WP-003)가 동시에 작업 중**이다 — 워킹트리가 아니라 **커밋(HEAD)** 을 읽어라(`git show HEAD:<path>`).

## 1. 기준

- SPEC 0.4.1 §5.2·§5.3(스트림 계약: 쿠키 인증 · 첫 프레임 `{type:auth, role, audio}` · close 4401/4404/4409/1000 · 프레임 5종) · §5.4(확정 블록 = 원문 정본 · 화자 익명) · §11.1 폐기 목록. `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md`
- WP-002 `30-work/work-002-meeting-stream-relay.md` · WP-006 Phase 3.
- 브리프 둘: `orchestration/work/sc-meeting/sc-meeting-be-wp002-brief.md` §3 · `sc-meeting-fe-p3-brief.md` §2. 워커 리포트: `report-be-wp002.md` · `report-fe-p3.md`.
- 코디 실물 e2e(로컬 스택, Soniox 키 없음): 4401(쿠키 없음·첫 프레임 없음) · 4404 · 4409 `invalid_meeting_status` · subscribe `ready{meetingStartedAt,latestBatchSeq:0,speakerCount:0}` · upstream → `error{reason:"upstream"}` + 1011 · `/end` → summarizing. **코드가 이 관측과 일치하는지** 대조.
- 이월 WARN 처리 주장: W9(FE `author: string` → BE 는 null 가능) · W5(409) · W6(extra=forbid).

## 2. 확인 — 각각 PASS/FAIL(파일:줄)

1. **BE↔FE 프레임 계약 일치** — 첫 프레임·`ready`·`transcript.partial/final`·`ai.batch`·`error` 의 키 이름과 형(camelCase)·close code 와 reason 문자열. FE `stream.ts` 타입 vs BE `stream.py`/`_stream_message`.
2. **인증·열람 축** — 쿠키 principal 이 REST 와 같은 이음새인가 · 비참석 4404(존재 숨김) · 업스트림 = 만든 사람만인가(브리프: 시작한 사람=upstream) · 두 번째 업스트림 4409 `meeting_stream_active`.
3. **오디오 경로** — 컨테이너 형식 → `audio_format=auto`(sample_rate 제외) · 청크 순서 보존(원본 append → 업스트림 전달, append 실패 시 전달 안 함) · 64KB/250ms 한도 · `ready` 전 전송 없음(FE) · 원본 저장 위치가 리포 밖·응답에 안 실림.
4. **적재·경계** — 확정 블록 경계(화자 변경·300자·2초) 상수 한 곳 · `meeting_transcripts`·`meeting_recording_files`·`meetings.started_at` 이 reset_demo 안 · 폐기 표·라우트가 §11.1 목록과 일치하고 잔존 참조 0(`grep` 로 realtime-credential·speaker-assignments 등).
5. **동시성·정리** — `_Room` 이 `finally` 에서 빠지고 provider 닫힘 · 이벤트 루프 넘나드는 `_Outbox` 가 소켓을 pump 하나로만 만지는가 · `/end` 가 1000 으로 닫고 그 뒤 프레임 없음.
6. **FE** — WS 생성이 `stream.ts` 한 곳 · 자동 재연결 없음 · partial 교체/final 추가 · ai.batch 통째 교체 + 스크롤 유지 · 4409 `meeting_stream_active` 표시 · 마이크 거부 시 화면 유지 · 메모 낙관 렌더 없음 · 삭제 4파일 잔존 참조 0 · `author` null 처리(W9) · hex 리터럴 0 · D25 부품 셋(Composer·GutterList·StatusNote)이 DS 토큰만 쓰는가.
7. **회귀** — 검증 재현 1회: `cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_stream.py tests/architecture -m 'not integration'`(코디 66 통과) · `cd frontend && npx tsc --noEmit && npx vitest run src/meetings/`(코디 39 통과). ⚠ backend 워킹트리가 WP-003 진행분으로 더러울 수 있다 — 실패가 HEAD 것인지 워킹트리 것인지 `git stash` 없이 구분해 적어라(`git status` 첨부).
8. **새 어긋남** — 브리프·SPEC 에 없는 것을 만들었는가(예: pause/resume 처리, 화자 이름, 알림) · 리포트 주장과 코드 불일치.

## 3. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-code-03-report.md` — 총평(PASS / FAIL — 재발주) · 항목 1~8 표 · FAIL 은 파일:줄 + 고칠 방향 한 줄 · WARN 이월 목록.

## 4. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 3" \
  --body "총평 / 항목 1~8 / FAIL·WARN / 검증 수치"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 3: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
