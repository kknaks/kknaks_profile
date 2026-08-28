
# [backend] 리뷰 반영 수정 1차 — sliding·409 경합·retry 경로 외 (WORK-023 후속)

너는 아까 WORK-023 을 구현한 **kknaks-dev `backend` 워커**다. 리뷰(`orchestration/work/recruiter-chat/review-code-report.md`)가 나왔고 코디 판정이 끝났다. 아래 수정만 한다 — 다른 리팩토링 금지.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat` (기존 변경 위에 계속)
spec 은 **v0.0.5** 로 개정됐다 — retry 계약이 추가됐다:
`/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md`

## 수정 목록 (코디 판정 포함)

1. **F1 (W1 — sliding, 판정 ③ 둘 다)**: ① 세션이 유효한 **매 응답마다** `Set-Cookie` 재발급(브라우저 만료 연장), ② `resolve` 가 `last_seen_at + 30일` 지난 세션을 만료로 판정(그 요청은 새 손님 — 새 세션 발급 경로). 테스트: 재사용 요청에 Set-Cookie 나감 · 만료 세션 무효.
2. **F2 (W2 — 판정: 409 로 접는다)**: partial unique 위반 `IntegrityError` 를 **서비스 계층에서** 잡아 도메인 Conflict 예외로 변환 → 기존 핸들러가 409 `{"detail":"CONVERSATION_BUSY"}`. 계층 규약 유지(아래층 HTTP 무지). 테스트는 HTTP 응답 코드까지 단언.
3. **F3 (W6 — spec v0.0.5 신규 계약)**: `POST /api/chat/conversations/{id}/messages/{message_id}/retry` — 대상이 이 대화의 **failed assistant** 가 아니면 404, 대화에 pending 있으면 409. 성공 시 그 메시지를 pending 으로 되돌리고(content·steps·sources 초기화) 같은 질문으로 재제출, 200 `{message: assistant(pending)}`. 새 user/assistant 행을 만들지 않는다.
4. **F4 (W4)**: problem 합성 slug 왕복 검증을 career 와 동일하게 — 정본 slug 불일치도 404.
5. **F5 (W5)**: MCP `back_client` 경로 조립에 `urllib.parse.quote(slug, safe="")` — 모델 제어 문자열이 URL 문법으로 흐르는 자리를 구조로 닫는다.
6. **F6 (W10)**: 재생 초기화를 **첫 재생 text 이벤트 수신 시점**으로 미룬다(lazy) — 스트림이 죽어 이벤트가 0건이면 기존 부분 텍스트가 보존된 채 failed 마감. finalize 불변식(「실패 마감은 부분 텍스트를 지우지 않는다」)과 일치시킨다. 「재생인데 스트림 소멸」 테스트 추가.
7. **F7 (W3)**: `redact_config_overrides` 죽은 코드 정리 — 실제 로그를 내는 자리가 있으면 연결하고, 없으면 제거. `runtime.py` 예외 로깅이 제출 인자(-c 목록)를 문자열에 싣지 않음을 확인/보장.

W9(chat-tool 이 schemas 층을 안 씀)는 **수용 — 고치지 마라** (소비자가 우리 MCP 하나).

## 검증

```
cd app/back && uv run pytest -q tests/  (이번엔 채팅 테스트 전부 — 기존 105 + 신규가 전부 통과해야 한다)
cd ../mcp && uv run pytest -q
```

## 완료 보고 — 기존과 같은 2채널. 핸들은 dispatch preamble 값이 우선.

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "backend fix1 완료: <한 줄>" --body "F1~F7 각각 무엇을 어떻게 / 테스트 수치"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend fix1 완료 — <한 줄>. 상세는 인박스." --enter
```
