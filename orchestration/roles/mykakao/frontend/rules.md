# @mykakao-fe — 규칙

## 코딩 컨벤션
- 기존 파일의 스타일이 규약이다 — 새 패턴 전에 두 HTML 을 다 읽는다
- 순수 DOM API 를 쓴다 (`fetch`·`EventSource`·`querySelector`). 라이브러리 추가 금지
- SSE 는 `EventSource` — 이벤트명·페이로드 키를 BE 계약 그대로 쓴다. 임의 매핑 금지

## 안전 규칙 — 이 프로젝트 고유
- 실제 대화 내용을 리포트·스크린샷·커밋에 남기지 않는다. 예시가 필요하면 익명 더미로 만든다
- user_id·device UUID·키가 화면이나 콘솔 로그에 나가지 않게 한다

## 검증
- 빌드·타입체크가 없다. 대신:
  1. `<script>` 블록을 뽑아 `node --check` 로 문법 확인
  2. 네가 만진 부분 diff 를 직접 대조
- 브라우저 실기동 확인은 **코디네이터가 backend 를 띄워서** 한다 — 워커가 서버를 띄우지 않는다
- 검증은 1회만. 못 돌리는 환경이면 **못 돌렸다고 보고**한다

## 스코프 규칙
- `frontend/` 밖 수정 금지. `backend/` 는 BE 담당
- 문서 SoT(kknaks_profile 레포 `para/…/mykakao/`)는 read-only — 코디네이터 소유

## 리포트 형식

```markdown
# {WORK-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · 화면/상호작용 변경
## 검증 — node --check 결과 · 육안 대조 범위 · 못 한 검증
## BE 에 필요한 것 — 계약 불일치·추가 필드 요청
## 이슈/블로커
```
