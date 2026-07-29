---
type: reference
id: 2026-07-29-db-connection-pool-sizing
title: DB 커넥션 풀 사이징 원리와 실무 함정
date: 2026.07.29
source: https://m.youtube.com/watch?v=uhMhv8yGAyM
source_type: youtube
source_title: "아키텍트가 알아야 할 커넥션 풀의 기본과 함정 | 멤버십 영상"
source_author: 코딩하는기술사
source_published_at: 2026.06.15
tags:
  - db
  - connection-pool
  - performance
  - postgresql
  - hikaricp
---

# DB 커넥션 풀 사이징 원리와 실무 함정

## 개요

DB 커넥션 풀 사이즈를 어떻게 결정해야 하는지 다루는 백엔드·아키텍처 실무 강의다. PostgreSQL 위키, HikariCP 문서, Oracle RWP 팀의 권고를 근거로 삼아 "물리 코어 × 2" 공식을 중심으로 풀 사이징 원리를 설명한다. 멀티 WAS 환경에서의 배분 전략, 타임아웃 미스매치 같은 실무 함정도 함께 다룬다.

의견글(실무 해설 강의)에 가깝다. PostgreSQL 위키, HikariCP 공식 문서, Oracle RWP 문서를 1차 자료로 인용하나, 강사가 이를 선별·해석하여 실무 권고로 재구성한 형태다.

## 출처와 맥락

코딩하는기술사 채널의 멤버십 전용 영상(2026-06-15 업로드, 약 37분). 특정 제품·서비스 홍보는 없다. 강사는 PostgreSQL 위키, HikariCP GitHub README, Oracle RWP(Real-World Performance) 팀 문서를 인용하며, "30초 이상 짧게"·"25% 이하면 축소 가능" 같은 수치는 강사 본인의 실무 권고다.

## 핵심 주장

- 커넥션 수를 늘려도 일정 수를 넘으면 TPS가 오히려 떨어진다. 컨텍스트 스위칭·락 경쟁·캐시 교체 비용이 누적되기 때문이다.
- 풀 사이즈 출발점은 `DB 물리 코어 수 × 2 + 스핀들 수`다. NVMe SSD 환경에서 스핀들은 0으로 간주하므로 사실상 `코어 × 2`다. 이 값은 최종값이 아니라 부하 테스트로 스위트 스폿을 찾는 시작점이다.
- 멀티 WAS 환경에서는 각 인스턴스 풀 사이즈의 합산이 DB 맥스 커넥션을 초과해서는 안 된다. 배분 이론값은 `(코어 × 2) ÷ WAS 수`이며, 가용성을 고려하면 이보다 약간 높이되 합산이 DB 맥스 커넥션을 크게 넘지 않도록 한다.
- 풀 고갈의 주범은 대부분 풀 크기 부족이 아니라 롱 트랜잭션이다. 트랜잭션 안에 외부 호출이나 무거운 연산이 있으면 커넥션 점유 시간이 늘어 풀이 고갈된다.
- HikariCP의 `maxLifetime`은 중간 계층(PgBouncer, RDS Proxy, NLB 등)의 idle timeout보다 반드시 짧게 설정해야 한다. 강사 권고는 30초 이상 짧게.

## 주요 개념

<!-- concept 노트가 없으므로 개념 후보만 기재한다. -->

개념 후보:
- USL(Universal Scalability Law) — 동시 처리 단위 증가 시 자원 경쟁·일관성 비용 누적으로 처리량이 감소하는 성능 확장 모델
- 커넥션 풀 사이징 공식 — PostgreSQL 위키 유래의 `코어 × 2 + 스핀들` 경험칙
- 리틀의 법칙 진단 활용 — `TPS = 활성 커넥션 ÷ 쿼리 실행 시간`으로 풀 부족과 쿼리 부족을 구별하는 진단 프레임
- maxLifetime 미스매치 — 중간 계층 도입 시 타임아웃 불일치로 발생하는 커넥션 오류 패턴

## 근거와 사례

- **HikariCP 위키 벤치마크(PostgreSQL 대상)**: 약 50 커넥션 부근부터 TPS가 평탄화된다. 조건: PostgreSQL 단일 인스턴스, 구체적 하드웨어·쿼리 조건은 영상에서 미제시.
- **Oracle RWP 권고**: CPU 코어당 평균 프로세스 수 10개 이하. 기준은 물리 코어이며 하이퍼스레딩 논리 코어 제외. 출처 문서 URL은 영상 설명란 참조 예정으로만 언급.
- **PostgreSQL 위키**: `코어 × 2 + 스핀들` 공식이 수년간 다양한 벤치마크에서 경험적으로 수렴됐다고 서술. 단, 시작값일 뿐 실제 스위트 스폿은 부하 테스트로 찾아야 한다고 위키 자체에서 명시.
- **각 라이브러리 기본값**: HikariCP(Java) 10, ADO.NET 100, node-postgres 10, SQLAlchemy QueuePool 5(+최대 10 임시, 순간 최대 15). ADO.NET의 100은 안전 상한선이며 Microsoft 공식 가이드는 워크로드에 맞게 조정하라고 명시.
- **PostgreSQL 맥스 커넥션 기본값 100**: 시스템 예약·관리자 접속 제외 시 실사용 가능 약 90. AWS RDS 가이드 예: 맥스 500이면 풀러는 400으로 설정.

## 적용 가능성

> 아래는 원문 요약이 아니라 적용을 위한 **해석**이다.

- **운영 중인 시스템 점검**: HikariCP 메트릭으로 피크 시간대 평균 액티브 커넥션 측정 후 판단. 풀 대비 25% 이하 → 축소 검토 가능, 25~65% → 신중 적용, 60% 이상 → 축소 금지. 변경 시 단계적 적용과 즉시 롤백 준비 필수.
- **신규 시스템**: `코어 × 2`를 maxPoolSize 초기값으로 설정하고 부하 테스트로 조정. minIdle = maxPoolSize(고정 풀)로 런타임 변동 오버헤드 제거.
- **멀티 WAS 배분**: 전체 WAS 인스턴스의 풀 합산이 DB 맥스 커넥션의 80% 이하가 되도록 배분. 합산 초과 우려 시 PgBouncer 같은 외부 풀러 도입 검토.
- **중간 계층 도입 시**: maxLifetime을 해당 계층의 idle timeout보다 최소 30초 이상 짧게 설정(PgBouncer 기본 server_idle_timeout = 10분 → maxLifetime을 9분 30초 이하로).
- **TPS 개선 순서**: 풀 확장보다 쿼리 튜닝·인덱스·캐시로 응답 시간을 단축하는 것을 우선. 응답 시간 절반 → TPS 이론상 2배.

## 한계와 검증이 필요한 부분

- 강사의 실무 해설이며 1차 실험 데이터가 아니다. "30초 이상 짧게"·"25% 이하면 축소 가능" 등의 수치는 근거 조건이 영상에 제시되지 않은 강사 권고다.
- `코어 × 2` 공식은 PostgreSQL 위키 유래다. HikariCP는 타 DB에도 대체로 적용 가능하다고 명시하나, MySQL·Oracle·MS SQL Server 등 DB별 실측 검증이 필요하다.
- HikariCP 벤치마크의 "50 커넥션 부근 평탄화"는 구체적 하드웨어·쿼리 조건이 영상에 제시되지 않았다.
- 오토스케일링 환경의 동적 풀 배분 전략은 "외부 풀러를 사용하라"는 권고만 있고 구체적 설정값이 없다.
- 멤버십 전용 강의라 동일 URL로 외부 검증이 어렵다. 인용된 PostgreSQL 위키, HikariCP README, Oracle RWP 문서를 별도로 확인할 필요가 있다.

## 참고

- PostgreSQL 위키 커넥션 풀링 페이지 (영상 설명란 링크 예정으로 언급, URL 미제시)
- HikariCP GitHub Wiki 벤치마크 페이지 (영상 설명란 링크 예정으로 언급, URL 미제시)
- Oracle Database Application Connection Strategies 문서 (영상 설명란 링크 예정으로 언급, URL 미제시)
