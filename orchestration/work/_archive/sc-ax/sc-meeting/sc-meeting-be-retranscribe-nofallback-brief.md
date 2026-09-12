# [backend] 재전사 폴백 폐기 — 재전사 실패 = 회의 「실패」 · 결과 수신 끊김 고침 · 최종 스크립트는 언제나 재전사 원문

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD b440c6b = 네 2-pass 커밋). `backend/` 만. 커밋 금지. 서버 재기동 금지. 실물 Soniox 호출 금지(대역).

## 왜 (실물 1회차, 회의 d6e7b8e0)
Soniox 비동기 전사는 completed 됐는데 `GET /v1/transcriptions/{id}/transcript` 본문을 읽다 끊겼다:
`http.client.IncompleteRead(131070 bytes read, 44042 more expected)` → `SttUpstreamError("재전사 결과 실패")` → 파이프라인이 **실시간 원문 유지로 폴백**해 `transcript_source=realtime` 로 조용히 done. 사용자가 본 것 = 재전사 안 된 원문 위의 합성. 그 폴백은 코디 브리프의 잘못이다.

## 사용자 결정 (2026-09-11, D44 정정) — 문구 그대로 지켜라
1. **폴백 없음.** 재전사가 실패하면(업로드 실패 · 상태 error · 결과 수신 실패 · 빈 결과 · 상한 초과 · 녹음 없음) 회의는 **`failed`** 로 가고 `failure_reason` 은 D43 대로 사람 말 한 줄(무엇이 안 됐고 [다시 시도] 하면 된다). 실시간 원문 위에서 합성하지 않는다. 합성 단계로 넘어가지 않는다.
2. **[다시 시도](`POST /finalize`)는 재전사부터 다시** 돈다.
3. **최종 원문(`meeting_transcripts` 의 done 상태분)·합성 재료는 언제나 재전사 결과다.** `transcript_source` 값은 done 이면 항상 `final` — `realtime` 갈래·`REALTIME_NOTICE` 경로·상수는 지운다(열은 남겨도 된다).
4. **결과 수신 고침.** `platform/soniox.py _call` 의 urllib 단발 `response.read()` 가 큰 본문에서 끊긴다. 스트리밍으로 끝까지 읽고(`Content-Length`/chunked 모두), `IncompleteRead`·시간 초과·5xx 는 **같은 transcription_id 로 결과 GET 만 재시도**(3회, 2·4·8초 백오프). 그래도 안 되면 위 1 의 실패. 상태 폴링·업로드는 지금대로.
5. lease: `meeting_finalize_lease_seconds` 기본을 재전사 상한(1200)보다 크게(1800) — 네가 미결로 올린 것, 코디가 이 자리에서 받는다.

## 검증 (대역, 실물 0)
`cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'`. 테스트로: 재전사 실패 여섯 갈래 전부 `failed` + 사람 말 + 합성 미호출 · `/finalize` 가 재전사부터 · 성공 시 `transcript_source=final` · 결과 GET 이 두 번 끊기고 세 번째에 오면 성공 · 세 번 다 끊기면 실패. 기존 「실시간 유지」 테스트는 새 규칙으로 바꾼다.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 재전사 폴백 폐기" \
  --body "변경 파일 / 실패 여섯 갈래·재시도·lease / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 재전사 폴백 폐기. 상세는 인박스." --enter
```
