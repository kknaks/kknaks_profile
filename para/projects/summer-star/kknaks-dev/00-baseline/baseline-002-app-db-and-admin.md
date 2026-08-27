---
type: baseline
id: KDEV-BL-002
title: "md-only 운영에서 애플리케이션 DB화 + 관리자 기능"
status: accepted
product: kknaks-dev
source:
  type: idea
  ref: "kknaks 요청 2026-07-27 — 로그인/관리자 페이지부터 DB화 시작"
links:
  baselines: []
  decisions:
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs:
    - "[[spec-006-admin-auth|KDEV-SPEC-006]]"
  works: []
  releases: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/accepted
---

# md-only 운영에서 애플리케이션 DB화 + 관리자 기능

지금까지 `kknaks.dev`는 모든 콘텐츠를 md 파일(frontmatter가 SoT)로만 운영해 왔다. 여기서부터 **애플리케이션 데이터**를 관계형 DB로 옮기기 시작하고, 그 첫 삽으로 소유자 전용 **관리자 로그인/화면**을 만든다.

## Raw

> kknaks 요청 (2026-07-27)

- 헤더 우상단에 톱니(설정) 아이콘을 만들어 **관리자용 페이지**로 들어간다.
- `.env`에 id/pwd를 넣고, 그 값으로 **유저 시드**를 만들어 로그인한다.
- 로그인은 **쿠키 기반 JWT**로 한다.
- 로그인 후에는 일단 **목(mock) 페이지**로 둔다. 상세 페이지는 다음에 계획한다.
- "그동안 문서를 md로만 관리하고 DB화를 안 했는데, 이제 DB화를 진행할 계획이다."

## Context

작업 착수 시점(2026-07-27) 진단.

- 백엔드(`app/back`)는 FastAPI **in-memory persona 서버** — 부팅 시 `persona/`·`reference/`·`permanent/` md를 로드해 메모리 dict로 서빙한다. **관계형 DB가 없다.**
- 인프라에는 Redis(open-kknaks broker)만 있고 Postgres/MySQL 등 관계형 DB 서비스가 docker-compose에 없다.
- 인증 장치가 전무하다 — 기존 인증은 `admin/reload`의 HMAC 토큰(webhook/cron 전용)뿐, 사람이 로그인하는 세션 개념이 없다.
- 지식그래프([[baseline-001-repo-knowledge-graph|KDEV-BL-001]])는 **파일(frontmatter)이 SoT**라는 전제 위에 검증 게이트가 서 있다. 이 전제는 유지되어야 한다.

## Why It Matters

- 앞으로 콘텐츠를 브라우저에서 직접 쓰고 고치려면 "소유자만 접근하는 관리 영역"이 반드시 먼저 있어야 한다. 로그인은 DB화의 진입점이다.
- md-only는 정적 지식그래프에는 맞지만, 사용자 상태·세션·동적 편집 같은 **운영 데이터**에는 맞지 않는다. 관계형 DB가 필요한 시점이다.
- 단, 지식그래프 SoT를 DB로 끌고 오면 검증 게이트(L1~L6)와 옵시디언 그래프가 무너진다. 그래서 **무엇을 DB로 옮기고 무엇을 파일로 남길지 경계**를 처음부터 정해야 한다.

## Possible Direction

(이후 [[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]로 확정)

- 애플리케이션/운영 데이터(현재는 users)만 관계형 DB로. 지식그래프(persona/reference/permanent md)는 파일 SoT 유지.
- DB 엔진·ORM·마이그레이션 토대를 이번에 함께 깐다(첫 테이블이 곧 스키마 관리 시작점).
- 인증은 쿠키 JWT + `.env` 시드 단일 관리자. 회원가입·다중 유저·권한 세분화는 범위 밖.
- admin 화면은 인증 게이트만 있는 목 페이지로 시작, 실제 관리 기능은 후속 spec.
