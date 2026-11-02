# @mykakao-be — 규칙

## 코딩 컨벤션
- 이 레포의 기존 코드가 규약이다 — 새 파일 전에 인접 모듈을 읽는다
- SQLAlchemy 2.0 스타일 (`select(...)`), 엔진은 `mode=ro` — **카톡 원본 DB 에 쓰기 금지**
- open-kknaks 는 **설치본 그대로** 쓴다 — 라이브러리 수정 금지, 설정은 제출 옵션·compose 로
- LLM SDK 직접 import 금지 — 실행은 open-kknaks(codex) 경유

## 안전 규칙 — 이 프로젝트 고유
- 카톡 로컬 DB 는 **읽기 전용**이다. 열기·복사·마이그레이션 어떤 이유로도 원본을 쓰지 않는다
- 키·user_id·device UUID 를 로그·리포트·커밋에 남기지 않는다. 값이 필요하면 `<redacted>` 로 적는다
- 실제 대화 내용을 리포트·테스트 픽스처에 붙여넣지 않는다 — 익명 샘플을 만든다

## 테스트
- 신규·변경 로직은 `backend/tests/` 에 테스트. 테스트 통과 없이 "완료" 표현 금지
- 전체 스위트 돌리지 않는다 — **네가 만들거나 고친 테스트 파일만** (사용자 방침)
- 실 DB 가 필요한 테스트는 만들지 않는다 — 순수 함수(키 유도·프롬프트 조립·파싱)를 분리해 테스트한다

## 스코프 규칙
- allowed_paths 밖 수정 금지. `frontend/` 는 FE, `worker/`·compose 는 infra 담당
- 문서 SoT(kknaks_profile 레포의 `para/…/mykakao/`)는 **read-only** — 코디네이터 소유
- spec 계약(필드명·SSE 이벤트명·에러코드)을 임의로 바꾸지 않는다 — 어긋나면 보고

## 리포트 형식

```markdown
# {WORK-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · API/스키마/키유도 변경
## 테스트 결과 — 수치 · 새 테스트 목록
## 다른 팀 영향 — FE 가 알아야 할 것 · infra(큐·env) 영향
## 이슈/블로커
```
