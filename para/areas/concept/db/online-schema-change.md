---
type: concept
id: online-schema-change
title: 운영 스키마 변경 — 칸(트랜잭션) → 이미지 → 인덱스(CONCURRENTLY) 로 가르기 (Online Schema Change)
aliases:
  - 더하기만 migration
  - additive migration
  - 운영 마이그레이션
  - 무중단 스키마 변경
  - CREATE INDEX CONCURRENTLY
  - INVALID 인덱스
  - indisvalid
  - manual SQL 순서
up:
  - 2026-11-19-customer-erd
  - 2026-10-07-strong-hajin-enhance
  - 2026-11-20-day-cc-mig
tags:
  - database
  - postgresql
  - 운영
  - 마이그레이션
---

# 운영 스키마 변경 — 칸(트랜잭션) → 이미지 → 인덱스(CONCURRENTLY) 로 가르기

돌고 있는 서비스의 표를 바꿀 때 **잠금의 크기가 다른 변경을 한 번에 돌리지 않고** 단계로 가르는 것. Strong Hajin 은 운영 SQL 을 세 판으로 나눈다 — **① 칸 추가(한 트랜잭션) → ② 새 코드 이미지 배포 → ③ 인덱스를 `CREATE INDEX CONCURRENTLY` 로 따로.**

## 정의

1. **칸 판** — nullable 칸·새 표처럼 짧은 잠금으로 끝나는 additive 변경. 한 트랜잭션(`psql -1`)으로 돌려 반쯤 들어간 상태를 남기지 않는다. 옛 코드는 새 칸을 모른 채 돈다 — **이미지보다 먼저**
2. **이미지** — 새 칸을 쓰는 코드를 올린다
3. **인덱스 판** — 큰 표의 인덱스는 `CONCURRENTLY` 로 쓰기를 막지 않고 만든다. **`CONCURRENTLY` 는 트랜잭션 블록 안에서 돌 수 없다** — 그래서 칸 판과 같은 파일·같은 `-1` 에 둘 수 없고, 섞으면 일반 `CREATE INDEX` 로 쓰면서 그 표의 쓰기를 통째로 막게 된다
4. **INVALID 인덱스를 확인한다** — `CONCURRENTLY` 가 중간에 실패하면 인덱스가 **무효(`indisvalid = f`)로 남는다.** 적용 뒤 `pg_index.indisvalid` 를 보고, 무효면 지우고(`DROP INDEX CONCURRENTLY`) 다시 만든다
5. 파일 머리에 **적용 순서**를 적고, 운영은 그 순서로 적용한다

## 왜 중요한가

- 칸 추가와 `tasks` 같은 바쁜 표의 인덱스가 한 파일에 섞여 있으면, 통째로 돌리는 순간 그 표의 쓰기가 인덱스가 다 만들어질 때까지 멈춘다 — 사용자에게는 「저장이 안 된다」 로 보인다
- 무효 인덱스는 조용히 남는다 — 쿼리 계획에 쓰이지 않으면서 쓰기 비용만 낸다

## 경계와 오해

- **[[database-migration]](DB 를 다른 곳으로 옮기기) ≠ 스키마 변경** — 이 개념은 같은 DB 안에서 표 모양을 바꾸는 순서다
- **롤백은 이미지 쪽만** — additive 칸·표는 남겨도 옛 코드가 돈다. 칸을 지우는 되돌림은 따로 판을 둔다
- 로컬의 자동 스키마 맞춤(additive sync)이 운영 순서를 대신하지 않는다

## 함께 보는 개념

- [[database-index]] — 인덱스를 만드는 비용
- [[database-lock]] — 무엇이 얼마나 잠기는가
- [[ddl]] — 바꾸는 문장 자체
- [[zero-downtime-deployment]] — 이미지 쪽의 무중단

## 더하기만 · 이전 이미지 호환 — 자동 migration 배포에서

DAY 는 dev 에 머지하면 배포가 `alembic upgrade head` 를 자동으로 돌리고, 롤백은 이미지만 바꾼다(forward-only). 그래서 2026-11-19 의 새 테이블 28개 · `visit_task` 칸 3개는 **더하기만**(새 칸 nullable · 데이터 이동 없음)으로 했다. 이전 코드가 새 스키마 위에서 그대로 돈다.

- **유일 제약은 운영 동기화가 깨질 자리를 먼저 본다**: ERD 의 1:0..1 을 전부 DB 유일로 막으면, 원천(KOS)이 취소한 작업과 같은 티켓을 다시 쓸 때 **지금 돌고 있는 현황판 동기화가 막힌다.** 빈 테이블이고 위험이 낮은 하나(`ticket_bundle.purchase_item_id`)만 걸었다.
- **이미 적용된 migration 은 고치지 않는다**: 백필용 `visit` 날짜 인덱스를 0010 에 넣었다가, 0010 이 이미 dev 에 적용된 뒤라 **새 0011** 로 옮겼다.
- **레포 선례가 없으면 일반 `CREATE INDEX`** — `lock_timeout` 으로 대기만 끊는다. 다만 그동안 쓰기가 막히므로, prod 는 행 수를 보고 한가한 시간에 돌린다(CONCURRENTLY 는 트랜잭션 밖이라 별도 판).

## 스키마를 미리 넓히기 — 외부 키 전부를 한 번에

DAY day-cc-mig(2026-11-20): 기능을 붙일 때마다 칸을 더하면 상용 DB 에 마이그레이션이 계속 쌓인다. 그래서 KOS 응답 키 2,155 를 HAR 로 전수 대조해, 빈 키 632 를 migration 0012 **한 번**에 더했다(새 표 12 · 지금 23표 nullable 180칸 · 지금 칸 변경 0). 값은 이미 도는 동기화 회차와 수동 업데이트(`--stage kos_keys`)가 채운다. 질의마다 답이 바뀌는 응답(예약 칸 · 칸 점유)과 계산할 수 있는 값은 표로 두지 않았다 — 「다 저장」의 경계. ← [[2026-11-20-day-cc-mig]]

## 출처

- [[2026-10-07-strong-hajin-enhance]] §2 — Strong Hajin WORK-012 운영 SQL(`migrations/manual/2026-10-07-inbox-message-origin*.sql` · 검수 WP4 W-2 · 운영 `indisvalid=t` 확인)
- [[2026-11-19-customer-erd]] §2 — migration 0010 더하기만 · 0011 인덱스 · 유일 제약 판단(`review-code-1-report.md` §5 · `review-code-6-report.md`)
