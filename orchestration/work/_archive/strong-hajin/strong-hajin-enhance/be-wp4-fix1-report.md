# WP4-BE 수정 1 결과 보고 — 검수 WARN 운영 전 필수 셋

## 상태: done (커밋하지 않음 · WP4-BE 위 워크트리 변경)

- 근거: `be-wp4-fix1-instructions.md` · `review-wp4-code-report.md`
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`

## 1. 지시 3/3

| # | 고친 것 | 위치 | 시험 |
|---|---|---|---|
| **W-1**(코디 판정 ①) | 업무 출처는 **참고 자료를 실은 턴 이후 같은 「업무 생성」 흐름**에만 붙는다. 제안 턴까지 그 대화의 가장 최근 메시지 참고 자료를 찾은 뒤, **그 참고 자료 턴부터 지금까지 그 대화에서 다른 업무 생성 제안이 확정된 적이 있으면 붙이지 않는다**.<br>— 대상 제안: `task.create_self`·`task.assign`·`work_request.create`, 상태 `approved`, 이번 제안 제외<br>— 한 번 확정되면 그 참고 자료의 흐름은 끝난다. 같은 대화의 나중 무관한 업무에 새지 않고 「업무 만듦」 도 늘지 않으며, 사건도 내지 않는다<br>— 다른 메시지를 새로 실으면 새 흐름이다<br>— 거절된 제안은 흐름을 닫지 않는다(확정만 닫는다) | `B/platform/actions.py:729`(docstring) · `:757-771`(`flow_closed`) | `T/contract/test_inbox_message_context.py`:<br>— **참고 자료 → 업무 확정 → 다른 업무 확정 = 둘째 출처 없음** · 수 1 그대로 · 사건 0 · 새 메시지를 실은 셋째는 그 메시지가 붙음<br>— 초안 거절 뒤 다음 턴 제안은 여전히 그 흐름(출처 붙음) |
| **W-2**(운영 장애 위험) | 운영 SQL 을 갈랐다:<br>① **`2026-10-07-inbox-message-origin.sql` = 칸 셋만**(nullable `ADD COLUMN` 셋 · `psql -1` 트랜잭션 안전 · 인덱스 없음)<br>② **`….concurrent.sql` = 운영 인덱스**(`CREATE INDEX CONCURRENTLY` · autocommit)<br>③ 새 **`…-index.sql` = 격리 검증용**(트랜잭션 안 `CREATE INDEX` · 머리 「**운영에는 쓰지 않는다**」 · 선례 `2026-09-28-w7-successor-index.sql` 모양)<br>세 파일 머리에 **운영 적용 순서**를 적었다: ① 칸 → ② 이미지 → ③ 인덱스(concurrent — ② 뒤 언제든, 없어도 기능은 돈다) | `backend/migrations/manual/2026-10-07-inbox-message-origin.sql` · `….concurrent.sql` · `…-index.sql` · `docs/domain-model.md`(순서 한 줄) | `T/integration/postgres/test_inbox_message_origin_postgres.py`:<br>— 칸 판은 **`ALTER TABLE` 만** · 한 트랜잭션에서 두 번(재적용) · 인덱스가 **생기지 않음**<br>— 이어 `.concurrent.sql` 을 **autocommit** 으로 → 인덱스 생김<br>— 격리판이 트랜잭션 안에서 돌고, 정의가 concurrent 판과 같음(`CONCURRENTLY` 뺀 글자 비교) |
| **W-6** | 참고 자료의 메시지를 못 찾으면(남의 것 · 지운 방·연동 · 없는 id) 404 이되 `detail = {code: "INBOX_MESSAGE_NOT_FOUND", message: "참고한 메시지를 찾을 수 없습니다 — 지워졌거나 방을 나갔습니다"}` — 대화가 사라진 줄 알지 않게. 새 예외 `ContextMessageNotFound`(`ConversationNotFound` 하위 · 실행 직전 다시 해석할 때도 같은 예외 → 그 턴 실패) | 예외 `B/modules/ax_execution/conversations.py:33` · 해석기 `B/platform/conversations.py:1049,1053` · 매핑 `B/entrypoints/http.py:523`(일반 `ResourceNotFound` 앞) | 남의 메시지 404 의 `detail` 전문 · 지운 방·연동 404 의 `code` |

## 2. 검증 (관련 시험만)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | `tests/architecture` · contract: `test_inbox_message_context.py`(21 · 새 2 포함) · `test_conversation_lifecycle.py` · `test_conversation_command_tools.py` · `test_action_center.py` · `test_task_origin.py` · `test_task_creation_contract.py` · `test_mcp_action_items.py` | **213 passed** · 0 failed |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0` | `test_inbox_message_origin_postgres.py` | **4 passed**(운영 파일 순서 1 · 격리판 1 · 왕복 1 · schema_sync 1) |

- 인벤토리: HTTP·MCP 시그니처 변경 없음 — architecture(drift 시험 포함) 통과
- 전체 `make test` · `make verify` 는 돌리지 않았다

## 3. 미결 · 주의점

1. W-1 의 「다른 제안 확정」 은 **업무 생성 세 종류**만 센다. 같은 대화에서 회의 생성·업무 수정 같은 다른 종류가 확정돼도 흐름은 닫히지 않는다 — 「업무 생성 흐름」 으로 읽었다. 모든 종류로 넓히려면 조건 한 줄이다.
2. W-1 은 검수의 H-1 한 갈래를 남긴다: 메시지로 연 대화에서 **요약만** 받고 아무 업무도 확정하지 않은 채 「다른 일 하나 만들어 줘」 하면, 그 업무에는 여전히 출처가 붙는다(코디 판정 ①의 정의 그대로).
3. W-6 의 문구는 서버가 정한다. 화면이 `detail.message` 를 그대로 보이는지는 FE 몫이다.
