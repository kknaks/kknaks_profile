---
type: concept
id: distributed-processing
title: 분산 처리 (Distributed Processing)
aliases:
  - 분산 처리
  - distributed processing
  - 분산 시스템
  - 데이터 분산
  - horizontal scaling
  - 수평 확장
up:
  - 2026-07-29-database-selection-guide
tags:
  - distributed-systems
  - scalability
  - 처리량
  - 일관성
---

# 분산 처리 (Distributed Processing)

데이터와 처리를 여러 노드에 나눠 저장·실행해 입출력 처리량을 높이는 방식이다.

## 정의

- 단일 노드 대신 여러 서버(노드)에 데이터를 분산 저장한다.
- 요청도 여러 노드가 병렬로 처리해 처리량이 늘어난다.
- 도큐먼트 DB(MongoDB 등)·컬럼 패밀리 DB(Cassandra 등)는 분산을 염두에 두고 설계되어 분산 구성이 상대적으로 쉽다.
- 핵심 트레이드오프: **처리량↑, 일관성↓** — 노드 간 동기화가 지연되면 각 노드가 서로 다른 값을 반환할 수 있다.

## 왜 중요한가

단일 DB 서버는 처리량에 한계가 있다. 대량의 읽기·쓰기가 필요한 서비스에서 분산 처리는 수직 확장(더 좋은 서버) 대신 수평 확장(서버 추가)으로 처리량 문제를 해결하는 핵심 수단이다. 데이터베이스 선택 시 분산을 염두에 두고 설계된 DB인가가 중요한 기준이 된다.

## 경계와 오해

- **처리량↑ ≠ 정확도↑** — 분산 환경에서는 노드 간 데이터 동기화가 완벽하지 않아 일시적 불일치(eventual consistency)가 발생할 수 있다. 금융 거래처럼 정확도가 핵심이면 단일 노드 기반 관계형 DB가 더 적합하다.
- **분산 처리는 쓰기 비용도 증가** — 데이터를 여러 노드에 동시에 써야 하므로 쓰기 지연이 늘 수 있다.

## 함께 보는 개념

- [[db-normalization]] — 정규화를 포기(비정규화)하면 분산 구성이 쉬워지는 관계

## 출처

- [[2026-07-29-database-selection-guide]] — 도큐먼트 DB·컬럼 패밀리 DB의 특성으로 소개; 대량 입출력 서비스에 적합하지만 DB 간 정확도가 떨어질 수 있다는 트레이드오프로 설명
