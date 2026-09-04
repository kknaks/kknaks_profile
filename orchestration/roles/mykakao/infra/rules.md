# @mykakao-infra — 규칙

## 규칙
- compose 에 backend·DB 를 넣지 않는다 (설계상 backend 는 호스트)
- 이미지 태그를 `latest` 로 두지 않는다 — 현재 redis 는 `7-alpine` 로 고정돼 있다
- **자격증명을 레포에 넣지 않는다.** `~/.codex` 인증 복사본(`.codex-home/`)·`.env` 는 `.gitignore` 대상이다.
  `.env.example` 에는 실제 값이 아니라 자리표시자만 둔다
- 요약 결과를 DB 에 저장하지 않는다 — WORK-002 개정에서 **명시적으로 제외**된 범위다
- 스크립트를 새로 만들면 기존 것을 지우지 않는다. macOS 용을 남기고 플랫폼별로 나눈다

## 검증
- docker 가 없는 환경이면 기동 검증 불가 — compose 스키마·스크립트 문법만 육안 확인하고
  **못 돌렸다고 보고**한다. 통과했다고 쓰지 않는다
- 검증은 1회만

## 스코프 규칙
- `backend/`·`frontend/` 수정 금지 · 문서 SoT 수정 금지 (코디네이터 소유)

## 리포트 형식

```markdown
# {WORK-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · compose/이미지/env 변경
## 검증 — 무엇을 확인했고 무엇을 못 했나 (이유 포함)
## BE 영향 — NAMESPACE/QUEUES/REDIS_URL 관련 변경 여부
## 이슈/블로커
```
