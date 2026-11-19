# @centurion-backend — 규칙

레포 규칙의 정본은 레포 루트 `AGENTS.md` 와 `docs/development/`(backend-reliability · testing-strategy ·
service-onboarding)다. 아래는 그중 이 역할이 매번 부딪히는 것과 우리 쪽 규칙이다. 어긋나면 레포 문서가 이긴다.

## 모듈 경계 (`backend/crm/__init__.py` · `public.py`)
- 다른 모듈은 `crm.public` 만 import 한다. 새 기능을 밖에 내보낼 때도 `public` 을 거친다.
- `crm` 은 `linky` · `sso` · `admin` 을 import 하지 않는다. 의존 방향은 `crm → catalog`(`catalog.public`).
- 공개 함수는 값(DTO · 튜플)만 돌려준다. ORM 모델 · `Base` 를 내보내지 않는다.
- 스키마 사이 FK 를 두지 않는다(병원 id = `auth.organizations.id` = Linky `branches.id`).

## 백엔드 안전 (AGENTS.md §백엔드 안전 기준)
- 공유 상태 불변식은 DB constraint · 원자적 갱신 · row lock · 멱등 키 중 하나로 최종 방어.
- `AsyncSession` 을 동시 task 에서 공유하지 않는다. async 경로에서 동기 I/O 로 event loop 를 막지 않는다. timeout · 취소 · 동시성 상한을 명시한다.
- 외부 I/O 를 DB transaction 안에서 오래 기다리지 않는다. 필요하면 outbox.
- 목록 조회 관계는 명시적 eager load. N+1 위험 경로는 query-count 테스트.

## 설정 · 비밀값
- 저장소에는 placeholder 만 든 `*.env.example`. 실제 env · credential 을 커밋 · 로그에 남기지 않는다.
- 환경변수 추가 · 변경은 `docs/infrastructure/environment-variable-management.md` 분류를 따르고 example · preflight · 테스트를 같은 변경에서 갱신한다.
- 가짜 계정 · 가짜 도메인을 하드코딩하지 않는다. 부재값은 env 로 연다.

## 실행 gate
- migration 적용 · 실제 DB/Redis credential 사용 · Azure · deploy · DNS 는 하지 않는다(별도 gate). migration 파일 작성과 테스트 DB 검증까지만.
- 테스트는 `deploy/compose.test.yaml` 전용 포트로. 공유 STG · PROD 에 붙지 않는다.
- 사용자 포트 · 프로세스를 건드리지 않는다.

## 스코프
- allowed_paths 밖 수정 금지. 커밋 · push · PR 금지. Conventional Commits 는 코디가 커밋할 때 쓴다.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일·모듈 목록
## 검증 — 명령과 수치 (pytest N passed 등)
## 계약 대조 — 계약 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
