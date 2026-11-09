---
type: concept
id: test-tiering
title: 테스트 층 나누기 — 기본 실행은 빠르게, 실제 인프라는 표식으로 (Test Tiering)
aliases:
  - 테스트 나누기
  - DB 없는 단위 테스트
  - infra 표식
  - pytest marker
  - not infra
up:
  - 2026-11-09-day-data-architecture
tags:
  - 테스트
  - pytest
  - 검증
---

# 테스트 층 나누기 — 기본 실행은 빠르게, 실제 인프라는 표식으로

테스트를 **외부 자원 없이 도는 것**과 **실제 DB · Redis 같은 인프라가 있어야 도는 것**으로 갈라, 기본 실행은 앞쪽만 수 초에 끝내고 뒤쪽은 표식을 달아 전체 실행에서만 돌린다.

## 정의

1. **표식이 층이다** — 인프라가 필요한 시험에 표식(`@pytest.mark.infra`)을 단다
2. **기본 실행은 표식을 뺀다** — `pytest -m "not infra"` 가 기본. 저장 · 화면 수정마다 돈다
3. **전체 실행은 표식까지** — 실제 DB · Redis 를 띄운 환경(CI · 단계 끝 검증)에서만 돈다
4. **기본 층이 DB 없이 돌 수 있는 것은 구조 덕이다** — repository 를 넘지 않는 ORM, 대역을 넣을 수 있는 service 가 있어야 한다 → [[layered-architecture]] · [[dependency-injection]]

## 사용 예시

```text
pytest -m "not infra"   # 수 초 · DB 없음 · 기본
pytest                  # 전체 · 실제 PG · Redis 필요
```

## 왜 중요한가

- **느린 시험은 안 돌린다** — 기본 실행이 DB 를 띄워야 하면 사람도 워커도 시험을 건너뛴다. 빠른 층이 있어야 매번 돈다
- **실패 원인이 갈린다** — 기본 층 실패는 코드, 인프라 층에서만 실패하면 연결 · 스키마 · 설정 쪽이다

## 경계와 오해

- **기본 층 통과 ≠ 동작 확인** — 대역이 실제와 다르게 굴면 기본 층은 거짓 초록이 된다. 인프라 층과 운영 같은 조건 1회가 남아 있어야 한다 → [[dev-prod-parity]]
- **표식 누락이 가장 흔한 구멍** — DB 를 쓰는 시험에 표식을 빠뜨리면 기본 실행이 환경에 따라 깨진다. 「DB 없이 도나」 를 CI 의 한 단계로 확인하면 잡힌다
- **[[schema-parity-test]] 와 다르다** — 그쪽은 무엇을 시험하나, 여기는 언제 돌리나

## 함께 보는 개념

- [[layered-architecture]] — DB 없는 층을 가능하게 하는 구조
- [[dev-prod-parity]] — 인프라 층 다음 단계
- [[schema-parity-test]] — 인프라 층에 들어가는 시험의 예

## 출처

- [[2026-11-09-day-data-architecture]] §2 — DAY v2 백엔드: 기본 `-m "not infra"` 수 초 · 실제 DB · Redis 는 `infra` 표식으로 전체 실행에서만(코드 `ec2a2681` · 역할 규칙 「테스트 나누기」)
