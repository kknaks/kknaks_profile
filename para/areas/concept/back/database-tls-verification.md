---
type: concept
id: database-tls-verification
title: DB 연결 TLS 검증 — 드라이버마다 다른 sslmode (asyncpg verify-full)
aliases:
  - asyncpg TLS
  - verify-full
  - sslmode
  - PGSSLROOTCERT
  - DB TLS
  - 인증서 검증
up:
  - 2026-11-09-day-data-architecture
tags:
  - database
  - tls
  - python
  - 보안
---

# DB 연결 TLS 검증 — 드라이버마다 다른 sslmode

DB 연결을 암호화하는 것(TLS)과 **상대가 진짜 그 DB 서버인지 인증서로 확인하는 것**(검증)은 다른 단계다. PostgreSQL 의 `sslmode=verify-full` 은 둘 다 하라는 뜻인데, **이 문법은 libpq(C 드라이버)의 것이라 다른 드라이버는 다르게 받는다.**

## 정의

1. **libpq 단계** — `disable` · `require`(암호화만) · `verify-ca`(인증서 체인) · `verify-full`(체인 + 호스트 이름). 관리형 DB 문서는 대개 이 문법으로 적혀 있다
2. **asyncpg 는 libpq 를 안 쓴다** — 연결 URL 에 `sslmode=verify-full` 을 넣으면 TypeError 가 나거나 인자를 못 받는다. asyncpg 는 `?ssl=verify-full` 처럼 자기 인자로 받는다
3. **검증에는 루트 CA 파일이 필요하다** — 기본 위치에 CA 묶음이 없으면 「CA 파일 없음」 으로 실패한다. 컨테이너에서는 OS 묶음을 지정한다(`PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`)
4. **시작 때 검사한다** — 설정이 빠지거나 파일이 없으면 첫 요청이 아니라 기동에서 멈추게 한다 → [[fail-fast]]

## 사용 예시

```text
문서대로:  postgresql+asyncpg://...?sslmode=verify-full   → TypeError / CA 없음
고친 뒤:   postgresql+asyncpg://...?ssl=verify-full
          PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt
확인:      터널로 실제 DB 에 앱 코드의 연결 경로 그대로 1회 연결
```

## 왜 중요한가

- **문서가 맞아도 우리 드라이버에 안 맞을 수 있다** — 관리형 DB 안내 · 배포 문서는 libpq 기준이다. 문서대로 넣었다면 첫 배포에서 앱이 DB 에 못 붙었다. 코드 검수가 잡았고, 실제 DB 로 확인하고 고쳤다
- **`require` 로 낮추면 조용히 약해진다** — 붙기는 하지만 상대 서버를 확인하지 않는다. 오류를 없애려고 단계를 내리는 것은 우회로다

## 경계와 오해

- **암호화 ≠ 검증** — 연결이 TLS 라는 것만으로 상대가 맞는 서버라는 보장이 없다
- **로컬에서 붙었다 ≠ 운영에서 붙는다** — 로컬 DB 는 TLS 없이 받기도 한다. 운영과 같은 조건(관리형 DB · 같은 CA)으로 한 번은 지나가야 한다 → [[dev-prod-parity]]
- **ORM 연결 URL 은 드라이버에 그대로 넘어가지 않을 수 있다** — 쿼리 인자 중 무엇이 어디로 가는지는 드라이버 문서를 본다 → [[data-source]]

## 함께 보는 개념

- [[dev-prod-parity]] — 운영과 같은 조건으로 1회 확인
- [[fail-fast]] — 설정 누락을 기동에서 멈추기
- [[data-source]] — 연결을 만드는 자리
- [[database-user]] — 연결 주체 쪽 설정

## 출처

- [[2026-11-09-day-data-architecture]] §2 · §3 — DAY 배포: libpq `sslmode=verify-full` 이 asyncpg 에서 안 먹음 → `?ssl=verify-full` + `PGSSLROOTCERT` + 시작 검사, 터널로 실제 DB 1회 연결 확인(#233 검수 H1 · 코드 `937dbb68`)
