# [backend] WP-002 후속 — 종료 시 업스트림 드레인 · Soniox keepalive · 스모크 스크립트 (코디 실물 e2e 발견 3건)

너는 **sc-ax `backend` 워커**다. WP-002~004 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = **8397d8f** WP-004 커밋). `backend/` 만. ⚠ frontend 워커(P4)와 reviewer 가 같은 트리에서 병렬 — `frontend/` 금지, 커밋 금지.

## 발견 (코디 실물 e2e, 2026-09-10, 실제 Soniox 키 · 40초 한국어 합성 음성 pcm_s16le)

| # | 관측 | 원인 | 고칠 것 |
|---|---|---|---|
| **E1** | 어댑터 직결 프로브: end frame(`""`) 을 보내면 확정 토큰 232개·`finished` 정상. **end frame 없이 30초 두면 196개에서 멈춤** — 마지막 약 6초(150자)는 end frame 이 와야 확정된다. 릴레이 경로 3회 모두 `meeting_transcripts` 에 **280자·end_ms≈35000 블록 하나만** 남고 41초까지의 뒷부분이 사라짐. `/end` 로 정상 종료한 회의(`a1fa7f1e…`)도 같음 | `MeetingUpstreamSession.shutdown()` 이 열린 블록을 flush 한 뒤 `upstream.close()` 로 end frame 만 보내고 **`finished` 까지 드레인하지 않는다**. 뒤늦게 확정될 토큰이 버려진다 | `/end`·클라이언트 정상 종료 시: ① end frame 전송 → ② `tokens()` 를 `finished` 까지(상한 예: 8초) 계속 소비해 `_handle_tokens` 로 블록에 넣는다 → ③ 그 뒤 flush·적재 → ④ 소켓 닫기. 업스트림 오류(408 등)로 끝나는 경로는 지금대로(받은 것까지 적재). 테스트: fake connector 가 end frame 뒤에 final 2개 + finished 를 내면 블록에 들어가는지 · 상한 초과 시 받은 것까지 적재 |
| **E2** | 오디오가 멈춘 뒤 **정확히 20초** 에 Soniox 가 `error_code 408` 로 끊음(프로브·릴레이 모두 재현) → `error{reason:"upstream"}` + 1011 | Soniox idle timeout. 브라우저 MediaRecorder 는 무음도 보내므로 데모 영향은 낮지만 마이크가 멈추면(OS 권한 회수·탭 절전) 회의가 통째로 끊긴다 | 업스트림 세션에 **오디오가 N초(잠정 10초) 없으면 Soniox keepalive 프레임 `{"type":"keepalive"}` 전송**(Soniox 실시간 API 규격). 상수 한 곳. 테스트: fake 시계로 10초 무음 → keepalive 1회 |
| **E3** | `make soniox-smoke` 가 `ModuleNotFoundError: ax_workspace.modules.meetings.transcription` | WP-002 가 지운 모듈을 `backend/scripts/soniox_smoke.py` 가 아직 import | 새 어댑터(`SonioxRealtimeConnector` · `AudioDeclaration`) 위에 다시 쓴다 — 짧은 wav/pcm 을 보내고 end frame 뒤 finished 까지 받아 **토큰 개수·소요 시간만** 출력(본문·키 출력 금지). Makefile 타깃은 그대로 |

| **E4** | 승격 `POST …/todos/{id}/promote {assignee_id:"hyeon"}` → **422 「assignee is not an eligible assignee」**(대표 yuna → 인사 hyeon, 회의 참석자). 자기 자신 승격은 201 | SPEC-001 배정 규칙(교차 조직 422)이 회의 경로에도 적용 — §9 는 담당 후보 = **참석자 먼저** | **D29**: 회의 승격에서는 assignee 가 **그 회의 참석자(attendees)면 조직 경계와 무관하게** eligible(`allow_self_assignment` 옆에 참석자 예외 하나 — `WorkRequestApplication.create` 기본값은 그대로, work 회귀 0). 참석자 밖은 기존 규칙. 테스트: 참석자 교차 조직 201 · 비참석 교차 조직 422 |
| **E5** | 실제 합성 결과: 「이번 주 금요일까지」·「다음 주 목요일 오전까지」가 발화에 있는데 `due_candidate` 전부 null · description 마지막 줄이 「회의 제목 없는 회의 · 안건 2 에서」 | 프롬프트에 **기준일(회의 일시)** 이 없어 상대 날짜를 ISO 로 못 만듦 · 제목 자리에 title_candidate 미사용 | 합성 프롬프트에 회의 `starts_at`(날짜·요일)과 이어진 다음 회의 일시를 싣고 「상대 표현은 기준일로 환산해 YYYY-MM-DD」 지시 · description 스탬프는 title 없으면 title_candidate 로. 테스트: 대역 출력 검증 + 프롬프트에 기준일 포함 단정 |
| **E6** | 팀장 역할에 `work_request.create` 없음 → 참석자여도 승격 403(WP-004 보고) | 조직 카탈로그 시드 | **D30**: 시드에서 팀장 역할에 `work_request.create` 부여(한 줄). 기존 테스트가 「팀장 403」을 고정했다면 그 테스트를 D30 으로 뒤집는다 |

참고: 경계 규칙(화자 변경·300자·2초)은 정상 — 한 화자 독백 280자는 블록이 안 닫히는 게 맞다(코디 확인).

## 검증

```
cd backend && uv run pytest -q tests/contract/test_meeting_stream.py tests/contract/test_meeting_finalize.py <work 계약 테스트> tests/architecture -m 'not integration'. 실제 Soniox 호출 금지(코디가 한다). 검증 1회
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-002/004 후속(드레인·keepalive·스모크·참석자 배정·기준일·팀장 권한)" \
  --body "변경 파일 / E1~E6 처리 / 검증 수치(+work 회귀) / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-002 후속. 상세는 인박스." --enter
```
