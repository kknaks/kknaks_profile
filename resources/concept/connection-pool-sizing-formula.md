---
type: concept
id: connection-pool-sizing-formula
title: 커넥션 풀 사이징 공식 (Connection Pool Sizing Formula)
aliases:
  - 커넥션 풀 사이징 공식
  - connection pool sizing formula
  - 커넥션 풀 사이징
  - DB 풀 사이징 공식
  - 코어 × 2 공식
  - pool sizing formula
  - 풀 사이즈 공식
up:
  - 2026-07-29-db-connection-pool-sizing
tags:
  - DB
  - 커넥션풀
  - 성능
  - PostgreSQL
  - 인프라
---

# 커넥션 풀 사이징 공식 (Connection Pool Sizing Formula)

PostgreSQL 위키에서 유래한 경험칙으로, DB 커넥션 풀의 최대 크기 시작점을 **`물리 CPU 코어 수 × 2 + 유효 스핀들 수`** 로 계산한다.

## 정의

```
최적 풀 사이즈 시작점 = 물리 CPU 코어 수 × 2 + 유효 스핀들 수
```

**각 항의 의미:**

- **물리 CPU 코어 수**: 하이퍼스레딩(논리 코어)을 제외한 실제 코어 수. DB 쿼리는 메모리 접근이 빈번해 하이퍼스레딩 효과가 미미하고 오히려 캐시 경쟁을 유발한다. 8코어 16스레드 CPU라면 코어 카운트는 8이다.
- **× 2 이유**: DB 쿼리는 CPU 연산과 I/O 대기가 번갈아 발생한다. I/O 대기 중 코어가 놀지 않도록 여유 하나를 더 두는 것이다. × 3, × 4는 컨텍스트 스위칭·캐시 무효화·락 경쟁을 오히려 키운다([[universal-scalability-law]] 참조).
- **유효 스핀들 수**: HDD RAID 구성 시 물리 디스크 회전축 수. NVMe SSD 환경에서는 회전축이 없고 I/O 대기도 거의 없으므로 **0**으로 간주. 데이터가 메모리에 모두 캐시된 경우도 0.

2026년 NVMe 환경에서 사실상의 공식:

```
풀 사이즈 시작점 ≈ 물리 CPU 코어 수 × 2
```

**멀티 WAS 환경 주의:**

각 WAS에 공식값을 독립 적용하면 안 된다. DB가 감당할 총량을 WAS 수로 배분해야 한다.

- WAS 4대, DB 8코어 → 총 허용량 16개 → WAS당 4개 (DB 보호 우선)
- 가용성 우선이면 WAS당 5~6개 (한 대 장애 시 나머지가 여유 있게 처리)
- 합산이 DB의 `max_connections`를 초과하면 장애 발생

## 왜 중요한가

임의의 큰 값(50, 100)을 설정하면 [[universal-scalability-law]] 법칙에 따라 TPS가 오히려 감소한다. 기본값(HikariCP 10개)을 그대로 쓰면 DB 자원이 충분해도 풀이 병목이 될 수 있다. HikariCP 벤치마크에서 PostgreSQL은 약 50 커넥션 부근부터 TPS가 평탄화되며, Oracle RWP 팀은 코어당 평균 10개 이하를 권고한다.

## 경계와 오해

- **최종값이 아니라 시작점이다** — 반드시 부하 테스트로 실제 스위트 스폿을 찾아야 한다. PostgreSQL 위키도 "이 값은 시작값일 뿐"이라고 명시한다.
- **멀티 WAS에서 WAS별 공식값을 그대로 쓰면 안 된다** — WAS 4대에 각각 16개를 설정하면 총 64개가 DB max_connections 100을 초과해 장애가 발생한다.
- **100개 이상은 안티패턴이다** — HikariCP 벤치마크에서 약 50 커넥션 이후 TPS가 평탄화된다.
- **현재 잘 돌아가는 시스템에 즉시 적용하지 않는다** — 피크 시간대 평균 활성 커넥션을 측정한 후, 풀 사이즈 대비 25% 이하이면 축소 검토 가능. 60% 이상이면 축소 금지.

## 함께 보는 개념

- [[universal-scalability-law]] — `× 2`에서 멈추는 이론적 근거. 더 늘릴수록 처리량이 감소하는 이유를 설명한다.
- [[little-law]] — 이 공식으로 정한 시작값이 목표 TPS를 달성하는지 검증하는 진단 도구.

## 출처

- [[2026-07-29-db-connection-pool-sizing]] — PostgreSQL 위키 기원 공식 소개; NVMe 환경에서 스핀들 = 0으로 사실상 `코어 × 2`; HikariCP 공식 가이드와 Oracle RWP 문서에서 동일 공식 인용; 멀티 WAS 배분 주의사항 및 현행 시스템 적용 시 측정 우선 원칙 제시
