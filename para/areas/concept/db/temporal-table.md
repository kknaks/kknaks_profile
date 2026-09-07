---
type: concept
id: temporal-table
title: 기간형 테이블 (Temporal Table)
aliases:
  - 기간형 테이블
  - temporal table
  - valid_from/valid_to
  - 이력 원장
  - 기간 겹침 제약
up:
  - 2026-09-07-sc-org
tags:
  - database
  - 모델링
  - postgresql
---

# 기간형 테이블 (Temporal Table)

**관계를 현재 상태가 아니라 유효 기간(`valid_from`, `valid_to`)을 가진 행으로 저장하는 것.**
"누가 어느 부서인가"가 아니라 "누가 언제부터 언제까지 어느 부서였나"를 원장으로 남긴다.

## 정의

mediness 조직도(→ SC 조직도 반입)가 사례다. 소속·직급·직책·고용이 전부 기간 행이다:

- **half-open 구간 `[from, to)`** — 현재 유효 = `valid_from <= now AND (valid_to IS NULL OR now < valid_to)`.
  경계가 반열림이라 연속된 두 기간(전임자 퇴임일 = 후임자 취임일)이 겹치지 않는다
- **변경은 UPDATE 가 아니다** — 기존 행의 `valid_to` 를 마감하고 새 행을 만든다.
  이력을 덮어쓰는 순간 원장이 아니게 된다
- **삭제도 없다** — 기간 마감(`valid_to`)·논리 취소(`cancelled_at`)·비활성(`active=false`)만 있다

## 겹침은 애플리케이션이 아니라 DB 가 막는다

같은 사람이 같은 대상에 겹치는 기간을 갖는 것을 PostgreSQL **GiST EXCLUDE 제약**으로 막는다:

```sql
EXCLUDE USING gist (
  organization_member_id WITH =,
  tstzrange(valid_from, valid_to, '[)') WITH &&
) WHERE (is_primary)          -- 주소속은 시점당 1개
```

- [[unique-key]] 의 일반화다 — "같으면 안 된다"를 등호만이 아니라 **범위 겹침(`&&`) 연산자**로 검사한다
- 스칼라 컬럼과 range 를 한 제약에 섞으려면 `btree_gist` 확장이 필요하다
- 애플리케이션 검사로 옮기면 동시성 하에서 같은 보장이 안 나온다 — 두 트랜잭션이 동시에
  "겹침 없음"을 읽고 둘 다 넣는다. 제약은 그 자체가 직렬화 지점이다

## 대가

- **테이블·제약이 몇 배로 는다** — 조인 없는 평면 스키마 대비 "지금" 조회에도 as-of 판정이 붙는다
- **NULL 하한의 함정** — 시작일을 nullable 로 완화하면 그 range 는 하한 무한대라 모든 기간과
  겹친다. 그 사람에게 두 번째 기간을 넣으려면 시작일부터 채워야 한다 (SC 반입에서 실제로 밟음 —
  입사일이 15/169 뿐이라 완화했고, 제약을 문서에 남겼다)
- **현재만 필요하면 과설계다** — 이력 요구가 없다는 확신이 있으면 평면 스키마가 맞다.
  단, 나중에 이력 요구가 오면 전면 재설계가 된다 — 갈림길은 스키마를 정할 때 한 번뿐이다
