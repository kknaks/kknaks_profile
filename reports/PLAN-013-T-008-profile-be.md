# PLAN-013-T-008 결과 보고

## 상태: done

WORK-009 BE 몫(C-1~C-4). 채팅④ 방안을 Source Inbox로 push하는 BE. 코드 레포
`/Users/kknaks/git/toy_pr2/ax-graph/apps/api`. T-006 워킹트리 변경분(retriever) 무접촉.
**미커밋** — admin 검수 후 일괄(브랜치 생성 안 함).

## 수행 내용

### C-1 push endpoint
- `POST /graph/chats/{chat_id}/push-to-inbox` (`axkg/api/routes/graph.py`).
- 권한 **staff·admin 모두 허용**: graph 라우터가 `main.py`에서 `get_current_auth`(로그인만)로
  등록돼 있어 staff·admin 공통 접근이다 — 인박스 표면(`sources` 라우터, `require_admin`)의
  admin 경계는 무변경. 단일 쓰기 액션이며 인박스 목록/관리 표면 접근을 부여하지 않는다
  (AXKG-SPEC-008 push 행).
- 본인 소유 chat만: `ChatService.assemble_conversation_for_push`가 owner 스코프를 강제해
  타인/삭제 세션은 `CHAT_SESSION_NOT_FOUND`(404). 기존 `/graph/chats/*` owner 스코프와 동일.

### C-2 대화 직렬화 — OQ 확정값
- **조립 위치 = 서버**(AXKG-SPEC-006 §7 OQ 확정). 근거: 채팅 이력의 SoT가 서버이므로
  클라이언트 직렬화를 신뢰하지 않고 서버가 `chat_id`로 대화를 authoritative하게 조립한다 →
  "push 시점까지의 대화 전부"를 위·변조 없이 보장하고, 직렬화 형식을 BE 한 곳에 고정한다.
- **직렬화 형식 = role heading**: 각 메시지를 `## {Role}\n{content}` 블록으로, 블록 사이는
  빈 줄로 구분한다. Role 라벨 = `User`/`Assistant`/`System`. 근거: raw_text는 요약①(LLM)이
  소비하므로 role 구분이 명확한 markdown이 파싱·정제에 유리하다. 공백뿐인 메시지는 잡음
  제거로 스킵한다. (`serialize_conversation` in `services/chat.py`)
- **request `raw_text` 계약 정리**: 서버 조립으로 확정하면서 SPEC §4의 `raw_text(required)`
  항목을 **optional**로 정리했다. request는 `run_id`(optional)만 의미가 있고, `raw_text`가
  와도 무시하고 서버 조립본을 authoritative로 쓴다. (`ChatPushRequest`)
- **`run_id` 컷오프**: 주어지면 그 run의 응답(assistant, 없으면 user 질문)까지를 컷오프로
  삼아 "push 시점까지"를 경계 짓는다. 없으면 세션 전체를 담는다. run_id는 provenance이기도
  하다. **대화 길이 상한/truncation은 이번 라운드 미도입**(SPEC-006 §7 OQ 그대로).
- `EMPTY_PUSH_TEXT` 검증: 조립 결과가 trim 후 빈 문자열이면 `EmptyPushTextError` → 422.

### C-3 chat source 생성
- `SourceService.create_chat_push` (`services/sources.py`): `source_channel=chat`,
  `source_url=null`, `normalized_url=null`, `slack_message_ts=null`(metadata 미기록),
  `raw_text`=대화 전부(필수·trim 후 non-empty)로 `received` 생성.
- push provenance: `metadata.chat_push = {chat_id, run_id?}`.
- 중복 병합 안 함: chat source는 URL이 없어 normalized_url 중복 판정 대상이 아니다.
- **DB 계약 변경**: `source_channel` CHECK를 4값(`slack/manual/chat/upload`)으로 확장하고,
  URL이 없는 채널을 위해 `source_url`·`normalized_url`을 nullable로 완화 →
  마이그레이션 `0020_source_channel_chat_upload.py`. **WORK-010의 `upload` 채널도 이번
  마이그에 함께 추가**(T-009 중복 마이그 방지). NULL은 partial unique index
  `uq_sources_normalized_url_active`에서 서로 distinct하게 취급돼 chat/upload 다건 공존이
  가능하다(PG/sqlite 공통). 모델(`models/source.py`·`models/enums.py`)·DTO·schema 동기.

### C-4 파이프라인 합류
- 생성 직후 manual과 **동일 배선**으로 자동 요약 트리거: open-kknaks 구성 시
  `start_summary`(received → summarizing + `collect_source_summary` queued task) 후
  background `execute_source_summary` 연결(커밋 순서도 manual과 동일). 미구성(테스트/오프라인)이면
  received로 둔다. URL이 없으므로 `raw_text`(대화 전부)가 곧 요약 입력 — User Note Fallback
  경로 재사용(SPEC-012 무변경). 이후 분류→문서화 게이트·분류 승인(admin)은 slack/manual과 동일.

## 테스트/검증 결과

- 신규 `tests/test_chat_push_to_inbox.py` 11건:
  - 정상 push(admin·staff) 201 / 미인증 401
  - 타인 chat push 404(owner 스코프)
  - source 필드 계약(channel=chat·url null·slack_ts null·raw_text·submitted_by·chat_push provenance)
  - 서버 조립 — assistant 방안 포함(`## User`/`## Assistant`), role heading 형식 유닛
  - 빈 대화 422(`EMPTY_PUSH_TEXT`) — endpoint + 서비스
  - 요약 파이프라인 합류(received → start_summary → summarizing + collect_source_summary task)
  - `run_id` 컷오프(이후 턴 제외)
- 전체 `cd apps/api && uv run pytest`: **414 passed**(기존 403 + 신규 11), in-memory sqlite.
- `uv run alembic heads` → `0020 (head)` 단일 head, 체인 `0019 → 0020` 정상.

## 다른 팀 영향

- **@profile-fe**: push CTA/상태 표면은 PLAN-013-T-010에서 이미 구현(work-009 C-5 done).
  BE 계약 정합 포인트 — 응답 `{source_id, status:"received"}`, 요청 body `{run_id?}`(서버가
  대화 조립하므로 `raw_text` 전송 불필요), Case `EMPTY_PUSH_TEXT`(422). FE가 `raw_text`를
  보내던 구현이면 서버가 무시하므로 동작엔 무해하나 불필요.
- **API 스키마 변경(FE 소비 주의)**: `Source.source_url`·`normalized_url`이 이제 **nullable**이다
  (chat·upload channel은 null). FE Source 타입이 non-null 가정이면 완화 필요.

## 이슈/블로커

- 없음. 커밋은 하지 않았다(admin 검수 대기).
- 참고: T-009(WORK-010 upload intake)는 이 마이그(0020)의 `upload` 채널을 재사용하고
  `original_filename`만 별도 마이그로 추가하면 된다 — blocked 아님.
