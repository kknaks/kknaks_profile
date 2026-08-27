# @mediness-be — 규칙

## 코딩 컨벤션
- mediness 레포의 `CLAUDE.md`, `AGENTS.md`, `rules/` 우선
- 4 계층 지향: Router (HTTP) / Service (비즈니스) / (Repository) / Schema (Pydantic 경계) / Model
- SQLAlchemy 2.0 스타일 (`select(...)`, `session.execute(...)`)
- 동기 라이브러리는 워커/스레드 풀로 격리

## TDD
- 신규 라우터/서비스는 `tests/` 에 단위 + 통합 테스트
- RED → GREEN → REFACTOR
- 테스트 통과 없이 "완료" 표현 금지

## 마이그레이션
- 모델 변경 시 `alembic revision --autogenerate` → 검토 후 적용
- 변경 마이그레이션은 리포트에 명시

## 스코프 규칙
- 작업 전 영향 받는 파일 목록을 전수 나열
- 계획서/스펙에 없는 파일이 생기면 admin / planning 에 보고
- `mediness/products/{service}/` 하위 서비스 코드/문서에는 손대지 않는다

## 리포트 형식

```markdown
# {PLAN-NNN-T-NNN} 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {추가/수정한 파일 목록}
- {API 엔드포인트, 모델, 마이그레이션 변경}

## 테스트 결과
- pytest 결과 (몇 개 통과/실패)
- 새로 추가한 테스트 목록

## 다른 팀 영향
- FE 가 알아야 할 API 변경 (path, request, response)
- DB 마이그레이션 영향
- planning 이 알아야 할 정책 불일치 사항

## 이슈/블로커
- {막힌 부분, 정책 합의 필요 항목}
```
