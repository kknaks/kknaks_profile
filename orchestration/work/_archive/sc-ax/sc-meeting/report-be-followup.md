E1~E6 여섯 건을 모두 고쳤다. 검증 282 passed / 0 failed (회의 119 + **work·권한 회귀 163 · 실패 0**, -m 'not integration', tests/architecture 포함), make reset-demo 성공, 실제 Soniox 는 부르지 않았다. 드레인을 넣다가 「기다리다 잃는」 두 번째 경로를 하나 더 찾아 같이 막았고, 남은 것은 코디의 실물 재확인뿐이다.

## 변경 파일 (12)
backend/src/ax_workspace/modules/meetings/{stream,stream_service,application,finalize,finalize_service}.py · modules/organization_access/catalog.py · modules/work/requests.py · platform/soniox.py · bootstrap/application.py · scripts/soniox_smoke.py · tests/contract/{test_meeting_stream,test_meeting_finalize}.py

## E1 — 종료 시 업스트림 드레인
- `SttSession` 에 `finish(timeout_seconds)` 신설: end frame 을 **한 번만** 보내고(`_send_end`) `finished` 까지 남은 토큰을 낸다. `close()` 는 이미 보냈으면 닫기만 한다.
- `_UpstreamSession.shutdown()` 이 정상 종료(`self._failed is None`)에서만 `_drain_upstream()` 을 돌아 확정 토큰을 블록에 넣고, 그 뒤 flush·적재·소켓 닫기. 업스트림 오류 경로는 지금대로 받은 것까지.
- 상한 `DRAIN_TIMEOUT_SECONDS = 8.0` (`stream.py` 한 곳).
- **덤으로 찾은 것**: 드레인이 취소되면(클라이언트가 이미 끊겨 태스크가 cancel 되는 흔한 경로) 그 뒤의 flush 가 통째로 건너뛰어 **열린 블록이 사라졌다.** 이건 드레인 이전부터 있던 손실 경로다 — flush 를 `finally` 로 옮겨 어떤 식으로 끝나든 적재되게 했다. 테스트가 「provider 가 끝내 답하지 않아도 받아 둔 것은 남는다」로 고정한다.
- 테스트 3: end frame 뒤 final 둘 + finished 가 블록에 들어감 · 상한/취소 시 받은 것까지 적재 · 오류 경로는 `finish` 를 부르지 않음.

## E2 — Soniox keepalive
- `SttSession.keepalive()` 신설(`{"type":"keepalive"}`). 세션에 `_pump_keepalive` 펌프를 더해 마지막 오디오로부터 `KEEPALIVE_IDLE_SECONDS = 10.0`(`stream.py` 한 곳) 지나면 보낸다. 실패하면 기존 `upstream` 실패 경로로 접힌다.
- 테스트 3: 무음 10초 → keepalive 1회 이상 · 오디오가 계속 오면 0회 · 상수 두 개가 한 곳에 있는지.

## E3 — 스모크 스크립트
- 새 어댑터(`SonioxRealtimeConnector`·`AudioDeclaration` pcm_s16le 16k mono) 위에 다시 썼다. 100ms 청크로 흘리며 토큰을 세고, **end frame 뒤 꼬리를 따로 센다**(`settled_before_end_frame` · `settled_after_end_frame` · `last_end_ms` · `total_ms`). 본문·키는 출력하지 않고 확정 토큰이 0이면 exit 1. `SONIOX_API_KEY` 없으면 exit 2(확인함). Makefile 타깃 그대로.

## E4 — 참석자 배정 (D29)
- `WorkRequestApplication.create(eligible_member_ids=frozenset())` 추가 — 그 집합에 든 사람은 조직 경계와 무관하게 eligible. 회의 승격만 `attendee_ids(meeting)`(참석자 ∪ 만든 사람)을 넘긴다. **기본값은 빈 집합이라 work 회귀 0.**
- 테스트 2: 대표→인사(교차 조직 참석자) 201 · 비참석 교차 조직(sora) 422 「eligible assignee」.

## E5 — 기준일 · 제목 스탬프
- 합성 입력에 `starts_on`·`next_meeting_on`(`2026-09-10 (목)` 모양, `finalize.describe_day`)을 싣고 프롬프트 본문 첫 줄에 「**기준일: …** — 상대 날짜 표현은 이 날을 기준으로 환산한다」를 세웠다. 지시문도 「상대 표현도 기준일로 환산해 YYYY-MM-DD」로 고쳤다.
- description 스탬프가 title 이 없으면 이번 `title_candidate` 를 쓴다 — 「회의 제목 없는 회의 · 안건 N 에서」로 나가지 않는다.
- 테스트 3: 프롬프트에 기준일·환산 지시 포함 · 제목 없는 회의의 스탬프가 후보 이름 · 발화 날짜가 due 로 살아남음.

## E6 — 팀장 권한 (D30)
- `_LEAD_CAPABILITIES` 에 `work_request.create` 한 줄. WP-004 가 「팀장 403」으로 고정해 둔 테스트를 D30 으로 뒤집고(201), 「참석자인 팀장이 후속을 넘긴다」 테스트를 더했다.

## 검증 수치
- 회의: stream 27 · finalize 34 · memo_batch 27 · core 31 = 119
- work·권한 회귀: request_amendment · request_evidence_and_cc · task_assignments · task_origin · task_delivery · product_operations · decision_continuity · action_center · access_roles · access_parity · access_administration · mcp · mcp_action_items · architecture = **163 passed, 실패 0**
- 합계 282 passed / 0 failed. `make reset-demo` 성공.

## 미결
- keepalive 10초·드레인 8초는 잠정값이다(실측 idle timeout 20초 기준). 상수는 `modules/meetings/stream.py` 두 줄.
- E5 는 프롬프트를 고친 것이라 **실제 모델이 상대 날짜를 옳게 환산하는지는 실물에서만 확인된다** — 대역 테스트는 「기준일이 프롬프트에 실렸는가」와 「AI 가 낸 ISO 날짜가 살아남는가」까지다.
- E1 드레인 상한 8초가 실제 꼬리(실측 약 6초)에 충분한지도 실물 확인이 필요하다.
- 실제 Soniox·Codex 호출은 하지 않았다. `make soniox-smoke` 1회는 코디 몫이다.
- 커밋·push 하지 않았다. `frontend/` 는 손대지 않았다.