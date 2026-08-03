---
type: concept
id: connection-lifetime-mismatch
title: 커넥션 수명 미스매치 (Connection Lifetime Mismatch)
aliases:
  - connection lifetime mismatch
  - maxLifetime 미스매치
  - maxLifetime mismatch
  - 커넥션 타임아웃 불일치
  - 풀 타임아웃 미스매치
  - 커넥션 수명 불일치
up:
  - 2026-07-29-db-connection-pool-sizing
tags:
  - DB
  - 커넥션풀
  - HikariCP
  - 타임아웃
  - 장애패턴
---

# 커넥션 수명 미스매치 (Connection Lifetime Mismatch)

클라이언트 커넥션 풀의 최대 수명 설정이 중간 계층(프록시·풀러·로드밸런서)의 유휴 타임아웃보다 길 때, 중간 계층이 먼저 끊은 연결을 풀이 모르고 재사용하여 쿼리 오류가 발생하는 패턴이다.

## 정의

**구성 요소:**

- **클라이언트 풀의 maxLifetime**: 풀이 커넥션을 교체하기 전까지 유지하는 최대 시간. HikariCP 기본값은 30분.
- **중간 계층의 idle timeout**: 프록시·풀러·NLB 등이 유휴 세션을 강제 종료하는 시간.

**미스매치 발생 조건:** `중간 계층 idle timeout < 클라이언트 풀 maxLifetime`

**발생 경로:**

1. 중간 계층이 idle timeout 경과 후 세션을 끊는다.
2. 클라이언트 풀은 maxLifetime이 남아 있어 해당 커넥션을 살아있다고 간주한다.
3. 이후 요청에서 이 죽은 커넥션으로 쿼리를 시도 → 오류 발생.

**주요 발생 환경:**

| 중간 계층 | idle timeout 기본값 | HikariCP 기본값(30분)과의 관계 |
|---|---|---|
| PgBouncer | server_idle_timeout 10분 | 즉시 충돌 |
| RDS Proxy | AWS 관리형 타임아웃 | 설정에 따라 충돌 |
| NLB | 흐름 유휴 타임아웃 | 설정에 따라 충돌 |

**권장 설정:** `maxLifetime ≤ min(중간 계층 idle timeout) - 30초`

HikariCP 공식 문서: "데이터베이스나 인프라가 부과하는 커넥션 시간 제한보다 몇 초 짧게 설정하라."

## 왜 중요한가

DB 자체(PostgreSQL 기본 idle timeout = 무제한, MySQL = 8시간)와 직접 연결할 때는 거의 문제가 없다. 그러나 PgBouncer, RDS Proxy, NLB 등 중간 계층을 도입하는 순간 잠재적 장애가 생긴다. 중간 계층 도입은 운영 최적화 목적으로 흔히 일어나지만, maxLifetime 점검이 누락되면 간헐적 쿼리 오류가 발생하고 원인을 추적하기 어렵다.

## 경계와 오해

- **DB 자체의 idle timeout과는 별개다** — PostgreSQL은 기본 무제한이라 직접 연결 시에는 대개 발생하지 않는다. 중간 계층이 끼면서 생기는 문제다.
- **커넥션 풀 크기와 무관하다** — 풀 사이즈를 최적화해도 이 설정이 틀리면 간헐적 오류가 발생한다.
- **maxLifetime을 무조건 짧게 하는 것도 비효율이다** — 너무 짧으면 커넥션을 자주 교체해 생성 비용이 누적된다. "중간 계층 타임아웃보다 몇 초 짧게"가 원칙이다.

## 함께 보는 개념

- [[connection-pool-sizing-formula]] — 풀 사이즈 공식. 수명 설정과 함께 커넥션 풀 구성 시 함께 점검해야 하는 항목이다.

## 출처

- [[2026-07-29-db-connection-pool-sizing]] — HikariCP maxLifetime 기본값 30분과 PgBouncer server_idle_timeout 기본값 10분의 미스매치; 외부 풀러·프록시 도입 시 반드시 점검; 30초 이상 짧게 설정 권장; HikariCP 공식 문서 인용
