# @cc-prototype-backend — 규칙

## 기능 독립 (DEC-001 D-03)
- 기능 폴더 밖의 코드를 import 하지 않는다. 공통 모듈을 레포 루트에 만들지 않는다.
- DB · compose · env · 의존성(`pyproject.toml`·`uv.lock`)은 기능 폴더 안에 둔다.
- 기능 폴더를 통째로 지워도 다른 기능이 그대로 돌아야 한다.

## FastAPI
- Python 3.12, `uv`. 계층은 router → service → repository. ORM 은 repository 를 넘지 않고,
  아래층은 HTTP 를 모르고 도메인 예외만 던진다. 트랜잭션 경계는 요청 하나.
- 설정은 env 로만. 비밀값을 커밋하지 않는다 — `.env.example` 만 둔다.
- 데모용이라도 가짜 계정·가짜 도메인을 하드코딩하지 않는다. 부재값은 env 로 연다.

## 안전
- 사용자 포트·프로세스를 건드리지 않는다. 기능의 SPEC 이 정한 포트만 쓴다.

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
