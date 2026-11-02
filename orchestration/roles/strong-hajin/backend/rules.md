# @sc-ax-be — 규칙

## 계층 — `tests/architecture/` 가 강제한다
- `modules/<도메인>/domain.py`·`application.py` 는 `fastapi`·`mcp`·`sqlalchemy` 를 import 하지 않는다
- `entrypoints/` 는 `platform/` 구현을 직접 import 하지 않는다 — `bootstrap/application.py` 가 조립한다
- 스키마 변경은 `entrypoints/reset_demo`(reset·`--sync`) 만 한다. 일반 API 시작은 스키마를 절대 바꾸지 않는다
- 도메인 예외는 모듈이 던지고 HTTP 상태는 `entrypoints/http.py` 가 매핑한다. 아래층은 HTTP 를 모른다
- 새 모듈·새 표는 `docs/domain-model.md` 대조표에 한 줄 추가한다 (ERD 항목 ↔ 표 ↔ 비고)

## 판단 계약 (ActionItem) — 어기면 FAIL
- 하나의 질문 = 하나의 ActionItem. 조정·재상신은 identity 유지 + Submission 추가
- envelope(`allowed_commands`·`waiting_on`·`preview`)는 server 가 만든다. client 가 kind 로 추론하게 만들지 않는다
- command 는 소유 모듈의 application operation 에 위임한다 (`WorkRequestApplication`·`TaskAssignmentApplication`·`ActionApplication`)
- 재전송은 영수증 — 같은 principal 의 같은 답은 두 번째 effect 없이 현재 envelope 를 돌려준다

## 잡 전송
- durable job 은 `platform/durable_jobs.py` 위(`FOR UPDATE SKIP LOCKED` claim · lease token · at-least-once). 확장 없는 vanilla PostgreSQL 에서 돌아야 한다 — PGMQ 등 확장 도입 금지
- handler 는 멱등이어야 한다. `AX_JOB_QUEUE_BACKEND=memory` 로 unit 테스트

## TDD
- 신규 operation·엔드포인트는 `tests/unit`(도메인) 또는 `tests/contract`(HTTP·MCP·adapter) 에 먼저 RED
- `integration` 마커는 일회용 PostgreSQL URL 이 있을 때만 — 브리프가 주지 않으면 쓰지 않는다
- 테스트 통과 없이 "완료" 표현 금지

## 스코프 규칙
- 작업 전 영향 파일 전수 나열 (entrypoints → application → platform → tests → domain-model.md)
- SPEC 에 없는 엔드포인트·표가 생기면 만들지 말고 코디네이터에게 묻는다
- `Makefile`·`docker-compose.yml` 은 실행 경로가 바뀔 때만 — 바꾸면 README 「띄우기」와 `tests/architecture/test_local_stack_targets.py` 를 같이 본다

## 리포트 형식

```markdown
# <slug> 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {추가/수정한 파일 목록}
- {엔드포인트·모듈·표 변경, domain-model.md 갱신 여부}

## 테스트 결과
- pytest 결과 (통과/실패 수) — 실행한 파일·마커
- tests/architecture 통과 여부

## 다른 팀 영향
- FE 가 알아야 할 envelope·응답 변경 (path, request, response)
- SPEC 과 어긋난 지점 (planner 보고 필요)

## 이슈/블로커
- {막힌 부분, 정책 합의 필요 항목}
```
