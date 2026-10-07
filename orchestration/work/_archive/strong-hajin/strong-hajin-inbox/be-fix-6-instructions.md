# [backend] BE 수정 판 6 — 슬랙 방 목록(available-rooms) 느림 (사용자 2026-10-06)

실측: 첫 쪽 20.6초(be-fix-123 보고). 원인: `platform/external_slack.py` 가 DM 상대마다 `users.info`(:108·:120·:160), 그룹 DM 마다 `conversation_members` + 참여자마다 `users.info` 를 **하나씩 순서대로** 부른다 — 이 계정 기준 DM 53 · 그룹 DM 35(참여자 수 × 호출) → 수십~수백 번 왕복 + 슬랙 속도 제한.

## 고칠 것
1. **이름은 한 번에**: `users.list`(페이지 몇 번)로 워크스페이스 사용자 id→이름·봇 여부 맵을 만들고 **캐시**(워크스페이스별 · 10분 정도 · 프로세스 메모리 또는 DB) — `users.info` 개별 호출 없앰. 연동 워커의 방 이름 풀이(sync.py:473·476)도 같은 캐시를 쓴다
2. **그룹 DM 참여자**: 이름이 `mpdm-a--b--c-1` 형식이면 거기서 사용자명(handle)을 뽑아 맵으로 실명 변환 — `conversation_members` 호출 없앰(형식이 다를 때만 대체로 부름)
3. **목록 응답 캐시**: 사용자별 available-rooms 결과를 짧게(1~2분) 캐시 · 「방 추가」 창을 다시 열 때 즉시
4. 목표: **첫 쪽 2초 안**(로컬 실측으로 숫자 보고 · 코디 스택의 jiho 로 측정은 읽기만 · 네 프로세스에서 같은 토큰 `~/.slack_test_token` 으로 재현 가능)
5. 속도 제한(429)이면 Retry-After 존중 · 시험

`backend/` 만 · 커밋 금지 · 끝나면 §9(subject "backend 완료: BE 수정 판 6") · 코디 핸들 term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b

## 추가 (사용자 · 같은 판)
- 사용자가 「대화방·채팅방 로딩이 오래 걸린다」 — 방 고르기 목록뿐 아니라 **메시지함에서 방을 열 때**(`GET /api/inbox/rooms/{id}/messages` · users 맵 · permalink 만들기)와 **메시지함 목록**(`GET /api/inbox/messages`)도 실측해 느린 곳을 같은 방식(이름 캐시 · 외부 호출 없애기 · N+1 쿼리 제거)으로 고쳐라. 각 엔드포인트 고치기 전/후 ms 를 표로
