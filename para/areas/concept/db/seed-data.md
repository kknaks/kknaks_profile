---
type: concept
id: seed-data
title: 시드 데이터 (Seed Data)
aliases:
  - 시드
  - seed
  - 목데이터
  - 데모 데이터
  - 초기 데이터
  - dataset import
  - pg_dump
  - pg_restore
up:
  - 2026-10-01-strong-hajin-deploy
tags:
  - db
  - 운영
  - 데이터 이관
---

# 시드 데이터 (Seed Data)

**빈 DB 가 제품으로 동작하려면 미리 있어야 하는 데이터.** 제품이 원래 갖는 것(카탈로그)과 그 조직이 갖는 것(사람·조직도)은 **원천도 수명도 다르다** — 섞어 두면 목데이터를 뺄 수 없다.

## 정의

| 층 | 예 | 원천 | 운영에 |
|---|---|---|---|
| 제품 카탈로그 | 조직 단위 종류·권한·권장 역할·워크플로 정의 | 코드 | 항상 |
| 예시 조직(목데이터) | 예시 회사·데모 계정·데모 업무 | 코드 | **넣지 않는다** |
| 실제 조직 | 조직도·사람·직급·직위·로그인 | 사람(양식) | 넣는다 |

Strong Hajin 은 `seed_catalog(demo_organization=False)` 로 카탈로그만 깔고(`reset-catalog`), 실제 조직은 `dataset import` 로 한 트랜잭션에 넣는다.

## 왜 중요한가

**적재 도구는 로컬 DB 에만 돈다.** reset·import 둘 다 dev 프로파일 + localhost `ax_demo*` 가드가 있고, 운영 DB 에 넣는 경로는 코드에 없다. 가드를 풀지 않고 운영에 넣는 길은 **로컬에서 적재 → `pg_dump`(세션 표 제외) → 운영 `pg_restore`** 다. 코드 변경 없이 같은 데이터가 간다. dump 는 파일로 남기지 않고 stdin 으로 흘려 복원했다.

양식 범위도 배웠다 — 「유저 정보만」으로 좁혔다가 「조직도는 완벽해야 한다」로 세 번 되돌아왔다. 기준은 「최소」가 아니라 **제품이 받는 조직 정보 전부**(11표 중 프로젝트 둘만 빼고 9표)였다.

## 경계와 오해

- **dump 이관은 일회성이다** — 이후 유저를 더 넣을 운영 경로는 여전히 없다. 반복되면 운영용 적재 명령이 필요하다
- **실명 시드는 공개 레포에 두지 않는다** — 형식(README)만 커밋하고 CSV 는 Git 밖에 둔다
- **[[database-migration]] 과 다르다** — 그쪽은 스키마·엔진 이전, 이쪽은 빈 DB 에 처음 채우는 내용이다

## 함께 보는 개념

- [[database-migration]] — 데이터를 옮기는 다른 경우
- [[runtime-profile-gating]] — 적재 도구에 걸린 프로파일 가드

## 출처

- [[2026-10-01-strong-hajin-deploy]] — 조직도 9표 양식 → mediness prod 4명 조회 → 로컬 import → dump 로 운영 복원
