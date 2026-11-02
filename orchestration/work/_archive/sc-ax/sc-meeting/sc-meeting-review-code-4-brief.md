# [reviewer_code] 코드 검수 4 — WP-003 메모·AI 배치 + 검수 3 F1 해소 (차분만)

너는 **sc-ax `reviewer_code` 워커**다. 검수 1~3 을 한 세션이다 — **WP-003 커밋 차분만** 본다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` — 읽기만. 범위 = `git diff bfc9770..HEAD`(HEAD = WP-003 커밋). 서버·reset·5176/8001 금지. 워킹트리는 **WP-004 워커가 동시에 고친다** — 검수 3 처럼 `git archive HEAD` 격리본으로 돌려라(반드시).

## 1. 기준

- SPEC 0.4.1 §6 메모 트랙 · §7(7.1 배치 계약 · 7.2 도구 · 7.3 경계) · §5.4-7 transcript · §13 OQ-307/315. WP-003 `30-work/work-003-memo-ai-batch.md` Phase 1~3 검증.
- 브리프 `sc-meeting-be-wp003-brief.md` §3(코디 확정 계약: 메모 API · D26 at_ms/transcript/can_write_memo/started_at · 웜스타트 · 트리거 600/80/90 · MCP persona=만든 사람 · 레지스트리 allowlist 4 · strict 스키마 · 강등 규칙 · 전량 교체 · push · `/end` 뒤 미발행 · 세션 유지). 워커 리포트 `report-be-wp003.md`.
- 검수 3 F1(`review-code-03-report.md`) + D27: upstream = 만든 사람만 → 비소유 upstream 4409 `not_meeting_owner`, subscribe = 참석+공유 유지.
- 코디 실물 e2e(2026-09-10): scheduled 메모 409 · start 뒤 `can_write_memo` true·`started_at` 실림 · 메모 201 `{track:memo, at_ms:25, author:yuna, order:1}` · 빈 문자열 422 · 비소유 메모 404 · 비소유 upstream **4409 not_meeting_owner** · 비소유 subscribe ready · transcript 200 `{items:0, memos:1}` · `/end` 뒤 메모 409 · **실제 Codex 웜스타트 성공**(`meeting_ai_sessions` 1행, 시작 20초 뒤). 코드가 이 관측과 일치하는지 대조.
- 원형 `/Users/kknaks/git/toy_pr2/task_management/app/back/service/meeting_batch_service.py` · `ai_schemas/meeting_notes.json` — 원형과 어긋난 곳은 「의도된 차이」인지 리포트 근거로 판단.

## 2. 확인 — 각각 PASS/FAIL(파일:줄)

1. **F1 해소** — MeetingAdmission 에 소유자 정보 · role=upstream 비소유 4409 `not_meeting_owner` 가 오디오·provider 전에 나는가 · 테스트 3(비소유 upstream · 소유자 upstream · 공유 subscribe).
2. **메모 API** — 경로·body `{text}`·201 Line(track memo, at_ms 서버 계산, author=member_id) · 게이트(만든 사람·in_progress·안건 소속) · 422 빈 문자열 · FE `api.ts addMeetingMemoLine` 과 모양 일치.
3. **D26** — 모든 Line 에 `at_ms`(ai/final null) · `GET /transcript` 열람 축(비참석 404·공유 200·scheduled 빈 배열)과 응답 키(camelCase items/memos) · MeetingDetail `can_write_memo`·`started_at` · FE viewModels 와 충돌 없음(새 필드 추가만).
4. **웜스타트·세션** — `/start` 뒤 백그라운드 · 실패해도 회의 정상 · session ref 저장 방식이 현행 `conversation_provider_session_references` 와 같은 결 · 세션이 `/end` 뒤 닫히지 않음(WP-004 가 씀).
5. **트리거·동시성** — 600자/안건 전환(<80자 생략)/90초 가 상수 한 곳 · 회의당 lock 1 · 실행 중 트리거 병합 · 커서(직전 성공 배치 이후)가 실패 시 되돌아가는가.
6. **MCP·레지스트리** — persona = 만든 사람 바인딩 · allowlist 가 설정에서 오고 도구 4개가 read-only · 쓰기 도구 노출 0 · env 값·키 인용 0.
7. **스키마·검증·적재** — strict(additionalProperties false · 전부 required · nullable) · 위반 시 전체 폐기 + 직전 성공분 유지 · task_id/evidence 강등 규칙 · AI 트랙 전량 교체에서 사람 안건 제목·출처 불변 · 트랜잭션 하나 · provider 호출은 트랜잭션 밖 · push 페이로드가 FE `ai.batch` 기대(MeetingDetail Agenda 모양, lines=track ai)와 일치 · `/end` 뒤 미발행.
8. **경계·회귀** — modules/* 가 fastapi/sqlalchemy/subprocess import 0 · 스키마 변경 reset_demo 안 · 검증 재현 1회: `cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_stream.py <WP-003 테스트> tests/architecture -m 'not integration'` · 리포트 주장 vs 코드 불일치.

## 3. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-code-04-report.md` — 총평(PASS / FAIL — 재발주) · 항목 1~8 표 · FAIL 파일:줄 + 방향 · WARN 이월.

## 4. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 4" \
  --body "총평 / 항목 1~8 / FAIL·WARN / 검증 수치"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 4: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
