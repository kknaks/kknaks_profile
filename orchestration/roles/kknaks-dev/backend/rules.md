# @kknaks-be — 규칙

## 코딩 컨벤션
- 이 레포의 기존 코드가 규약이다 — 새 파일 전에 인접 모듈(라우터·서비스·리포지토리) 패턴을 읽는다
- SQLAlchemy 2.0 스타일 (`select(...)`, async session)
- open-kknaks 는 **설치본 그대로** 쓴다 — 라이브러리 수정 금지, 설정은 제출 옵션·compose 로
- LLM SDK 직접 import 금지 (ADR-04) — 실행은 open-kknaks 경유

## TDD
- 신규 라우터/서비스는 `tests/` 에 테스트. 테스트 통과 없이 "완료" 표현 금지
- 전체 스위트 돌리지 않는다 — **네가 만들거나 고친 테스트 파일만** (사용자 방침)

## 마이그레이션
- 모델 변경 시 alembic revision → 검토 후 적용. 변경 마이그레이션은 리포트에 명시

## 스코프 규칙
- allowed_paths 밖 수정 금지. 특히 `para/`·`orchestration/`·`resume/` 는 코디네이터 소유
- spec 계약(필드명·에러코드·쿠키 속성)을 임의로 바꾸지 않는다 — 어긋나면 보고

## 리포트 형식

```markdown
# {WORK-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · API/모델/마이그레이션 변경
## 테스트 결과 — pytest 수치 · 새 테스트 목록
## 다른 팀 영향 — FE 가 알아야 할 것 · DB 영향
## 이슈/블로커
```
