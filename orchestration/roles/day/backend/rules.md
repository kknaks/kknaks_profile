# @day-backend — 규칙

## 아카이브와의 관계
- 기존 v0.1 코드(origin/stg)는 **참고만**. 통째로 복사하지 않는다 — 가져온 곳은 리포트에 `origin/stg:<파일>` 로 남긴다.

## 구조 · 계층 — 정본은 레포 `AGENTS.md`
- 레포 `AGENTS.md` 의 「저장소 구조」 · 「계층 규칙」 · 「외부 CRM 연동」이 기준이다. 여기와 다르면 AGENTS.md 가 이긴다.
- router 는 HTTP 만 · service 가 SQLAlchemy 세션을 직접 쓴다 · **repository 층을 만들지 않는다** · 묶음 조회는 `queries/`.
- 모델 감추기 — ORM 은 `day` 밖으로 안 나간다. 밖은 `day.public` 의 DTO 만.
- 기능 하나는 같은 파일 이름으로 — `models/` · `dtos/` · `enums/` · `schemas/` · `services/`.
- 테이블은 `day` 스키마 · 업무 테이블에 병원 id · 외부 id 는 `vendor` + `external_id`(업체 전용 칸 금지).
- 업체 차이는 `emr/<업체>/mapper.py` 에서만 흡수. 외부 쓰기는 `outbox` 로 — transaction 안에서 기다리지 않는다.
- 설정은 env 로만. 비밀값을 커밋하지 않는다 — `.env.example` 만 둔다.
- 가짜 계정 · 가짜 도메인을 하드코딩하지 않는다. 부재값은 env 로 연다.
- 외부 응답에 없는 정보를 다른 필드로 추정해 채우지 않는다.

## 안전
- 사용자 포트 · 프로세스를 건드리지 않는다. SPEC 이 정한 포트만 쓴다. 공유 STG · PROD DB 금지.
- migration 을 실제 DB 에 적용하지 않는다(테스트 DB 제외).

## 스코프
- allowed_paths 밖 수정 금지. 커밋 · push · PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일 · 모듈 목록
## 검증 — 명령과 수치 (pytest N passed 등)
## 계약 대조 — SPEC 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
