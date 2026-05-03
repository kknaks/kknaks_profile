---
id: adr-01
type: adr
title: DB 사용 안 함 — yaml/md SoT + FastAPI 메모리 캐시
status: accepted
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
tags: [adr, storage, architecture]
---

# DB 사용 안 함 — yaml/md SoT + FastAPI 메모리 캐시

## Summary

페르소나 콘텐츠는 `persona/**/*.md` (+ `_meta.yaml`, `activity.yaml`)를 SoT로 두고, 백엔드 FastAPI는 부팅 시 메모리 dict로 로드해서 응답 소스로 사용. **별도 DB(Postgres/SQLite 등)는 도입하지 않음.**

---

## 1. Context

이 프로젝트는 1년차 백엔드 엔지니어의 개인 포트폴리오. 데이터 양과 운영 컨텍스트가 일반 웹 서비스와 매우 다름:

- **데이터 규모** (mock 기준 + 1년 운영 후 추정):
  - profile 1, career 5-10, projects ~10, notes 18~수백, contents 매일 1개 (연 365), activity 365일 격자
  - 총 메모리 1MB 미만 예상
- **쓰기 주체**: 본인 1명. 동시 쓰기 충돌 X
- **읽기 패턴**: 외부 방문자, 캐시 가능
- **호스팅**: 본인 홈서버 (셀프호스팅) — 프로세스/디스크 부담 최소화 필요
- **개발 우선순위**: 빠른 개발 + 유지보수 편의 (이 프로젝트엔 백엔드 엔지니어링 자체가 차별점이 아님; 다른 회사 프로젝트에서 충분히 노출됨)

---

## 2. Decision

**DB 사용 안 함**. 다음 구조로 간다:

```
persona/**/*.md  ──→  FastAPI 부팅 시 yaml.safe_load + frontmatter parse
                          ↓
                     메모리 dict (`_data["career"] = [...]`)
                          ↓
                     /api/* 응답 (?lang= 분기, 메모리에서 추출)
```

- 검색은 메모리 inverted index (notes 수백 개 수준이면 ms 단위)
- 페르소나 git push → webhook 또는 systemd restart → 재부팅 → 메모리 갱신
- 자동 산출물(`activity.yaml`)은 cron 잡이 직접 yaml 갱신 + git commit + reload endpoint

---

## 3. Alternatives Considered

### 3.1 Postgres + 페르소나 → DB 적재
- **장점**: SQL 검색·정렬·필터 자유, 표준 패턴
- **단점**: 마이그레이션·백업·인덱스 관리 부담. 데이터 양 대비 명백한 오버킬. Postgres 프로세스 추가로 홈서버 자원 점유
- **기각 이유**: 운영 부담 vs 가치 비대칭

### 3.2 SQLite + yaml/md → 빌드 시 sqlite로 적재
- **장점**: 파일 한 개. SQL 자유. 백업 = 파일 복사
- **단점**: yaml과 sqlite 두 SoT 동기화 필요. 변환 한 단계 추가. 검색·정렬은 어차피 메모리로도 충분
- **기각 이유**: 메모리 dict 대비 추가 가치가 없음. 실제로 SQL이 필요해지면 그때 incremental 도입 가능 (3.4 참조)

### 3.3 풀 SSG (백엔드 자체 X)
- **장점**: 호스팅 정적 nginx만. 가장 단순
- **단점**: AI 가공(`activity.yaml` 생성 등) 잡을 어딘가에서 돌려야 함. GitHub Actions 가능하지만 백엔드 컴포넌트 자체가 빠지면 "백엔드 엔지니어 포트폴리오"의 컨셉 모순
- **기각 이유**: AI 잡 + 향후 확장 여지를 위해 백엔드 컴포넌트 1개는 살리는 게 정합

### 3.4 (현 결정) DB 없음 + 메모리 dict
- **장점**: 운영 부담 0, 코드 단순(150-200줄), 부팅·응답 모두 빠름, git diff = audit log
- **단점**: 데이터 만 단위 넘으면 메모리 부담. 실시간 동시 쓰기 불가
- **수용 가능한 이유**: 본 프로젝트는 두 단점 모두 해당 없음

---

## 4. Consequences

### 4.1 즉시 효과
- DB 마이그레이션·백업·인덱스 관리 코드 0
- 호스팅 단순화: 홈서버에 uvicorn + nginx만 (Postgres daemon 없음)
- 콘텐츠 변경 이력 = git history (별도 audit 시스템 불요)

### 4.2 코드 영향
- 부팅 시 `load_all()` 함수 하나로 모든 yaml/md 메모리 로드
- API 핸들러는 메모리 dict에서 dict comprehension으로 응답 구성
- 검색은 메모리 inverted index (한 번 빌드)

### 4.3 마이그레이션 트리거 (이 결정을 재검토할 조건)

다음 중 하나가 발생하면 SQLite부터 incremental 도입:

| 트리거 | 의미 |
|---|---|
| notes 만 단위 도달 | 메모리 인덱스 빌드 시간 부담 |
| 동적 기능 도입 (방문자 카운트, 댓글, 좋아요) | 동시 쓰기 + 트랜잭션 필요 |
| 다인 admin 시스템 | yaml git 충돌 회피 위해 DB 락 필요 |
| 복잡한 cross-카테고리 join 쿼리 추가 | SQL 표현력 필요 |

마이그레이션 비용 추정: yaml→SQLite 30분-1시간 (API 응답 스키마 안 바뀜 → 프론트 무영향)

### 4.4 위험 + 완화

| 위험 | 완화 |
|---|---|
| yaml 파싱 에러로 부팅 실패 | 부팅 검증 fail-fast (spec-01 §6). 사전 차단(git pre-commit hook 또는 CI 검증)은 plan-01에서 결정 |
| 페르소나 git push와 reload 사이 race | webhook이 reload endpoint 호출 (단일 토큰 인증) |
| 메모리 누수 (재로드 시 이전 dict 잔존) | `_data` 전역 dict 통째 교체 (Python GC 처리) |
