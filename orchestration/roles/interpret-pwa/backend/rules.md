# @interpret-pwa-backend — 규칙

## FastAPI
- Python 3.12, `uv`. 계층은 router → service → repository. ORM 은 repository 를 넘지 않고,
  아래층은 HTTP 를 모르고 도메인 예외만 던진다. 트랜잭션 경계는 요청 하나.
- 설정은 env 로만. 비밀값(Soniox 키 · 로그인 계정값)을 커밋하지 않는다 — `.env.example` 만 둔다.
- 계정 · 도메인을 코드에 하드코딩하지 않는다. env 로 연다.

## 외부 서비스
- Soniox · Procedure Hub 경로는 실물 호출 1회가 완료 조건이다. 키는 사용자가 넣은 `back/.env` 에서만 읽고 값을 출력 · 로그 · 리포트에 쓰지 않는다. 키가 없으면 pending 으로 보고.

## 안전
- 사용자 포트·프로세스를 건드리지 않는다. SPEC 이 정한 포트만 쓴다.

## 스코프
- allowed_paths 밖 수정 금지. 커밋·push·PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일·모듈 목록
## 검증 — 명령과 수치 (pytest N passed 등)
## 계약 대조 — SPEC 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
