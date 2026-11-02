# [backend] BE 수정 판 4 — 코디 로컬 실물에서 나온 결함 2 (2026-10-06)

로컬 스택(COMPOSE_PROJECT_NAME=strong-hajin-work · DB `ax_demo_inbox` @ localhost:54329 · API 8001 · 연동 워커 떠 있음 — **코디가 띄운 것. 끄거나 재시작하지 말고, 재현은 너 자신의 일회용 DB/프로세스로**). 로그: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-------/e8bacd93-7b19-4fba-8b82-958947d59a1e/scratchpad/local-stack.log`

## 결함 1 — Gmail: 백필 100통 뒤 「끊김」 (토큰은 멀쩡)
- 사용자 jiho 로 실제 Gmail 연결(동의 OK) → `backfill_count=100`·메시지 100 저장 → 바로 `status=disconnected` · 로그 `gmail integration … lost its token: PERMISSION_DENIED`
- 원인 후보: `platform/external_gmail.py` 의 오류 분류가 **403 이면 무조건 `UpstreamAuthRevoked`**(:43) — 403 PERMISSION_DENIED 는 토큰 폐기가 아닐 수 있다(특정 메시지·첨부·라벨 접근 거부, Workspace 정책, 할당량 등)
- 고칠 것: ① 응답 본문(`error.message`·`errors[].reason`)을 **로그에 남기고**(토큰·메일 내용 제외) ② 토큰 폐기 판정은 401/invalid_grant(또는 토큰 갱신 실패)일 때만 — 403 은 그 호출만 실패로(해당 메시지 건너뛰고 표시 · 반복되면 백오프) ③ 실제 어느 호출(profile / watch / list_inbox / get_message)에서 403 이 났는지 재현해 보고
## 결함 2 — 슬랙: 연결 3분 뒤 「끊김 revoked」 (토큰은 멀쩡 — auth.test ok)
- jiho 슬랙 연동(개발 토큰) 08:40 UTC 생성 → 08:43 `status=disconnected, disconnected_reason=revoked` · 같은 토큰으로 지금 `auth.test` 정상 · HTTP 로그에 disconnect 요청 없음 · 워커 로그에 경고 줄도 없음(조용히 끊김)
- 찾을 것: `revoked` 를 쓰는 모든 경로 grep(F-1 재확인·팬아웃·Socket Mode 이벤트 `tokens_revoked`/`app_uninstalled` 처리·방 재확인 실패 분류 등) — 왜 멀쩡한 토큰을 revoked 로 표시했나. **조용히 끊는 경로에는 경고 로그**를 남겨라
- `tokens_revoked` 이벤트라면 그 이벤트의 사용자 id 가 이 연동의 사용자인지 대조하는지 확인(남의 토큰 폐기 이벤트로 내 연동을 끊으면 안 된다)

## 범위
`backend/` 만 · 시험 추가 · 검증은 바뀐 것만 · 커밋 금지 · 끝나면 §9(subject "backend 완료: BE 수정 판 4") — 코디 핸들 term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b
