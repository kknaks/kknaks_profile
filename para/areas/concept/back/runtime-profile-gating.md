---
type: concept
id: runtime-profile-gating
title: 런타임 프로파일 게이트 (Runtime Profile Gating)
aliases:
  - 프로파일 게이트
  - profile gate
  - PRODUCTION 프로파일
  - 개발 전용 기능
  - 데모 바로가기
up:
  - 2026-10-01-strong-hajin-deploy
tags:
  - back
  - 설정
  - 보안
---

# 런타임 프로파일 게이트 (Runtime Profile Gating)

**실행 프로파일(development/test/production)에 따라 기능을 켜고 끄는 것.** 위험한 건 게이트 하나가 **서로 다른 질문 여럿**을 한꺼번에 답할 때다.

## 정의

게이트가 답하는 질문은 셋으로 갈라야 한다.

| 질문 | 예 | 프로파일에 묶나 |
|---|---|---|
| 이 기능이 **존재**하나 | `/api/auth/login` 라우트 등록 | 대개 아니다 |
| **누가** 부를 수 있나 | 세션 판정 | 아니다 — 인증이 정한다 |
| 개발 **지름길**을 노출하나 | 데모 계정 목록·데모 비밀번호·`X-Demo-Persona` | 그렇다 — 개발만 |

## 왜 중요한가

Strong Hajin 은 `local_login_enabled = profile != PRODUCTION` 하나가 「로그인 라우트 등록」과 「데모 계정 목록 노출」을 함께 쥐고 있었다. 그래서 **운영에는 로그인 수단이 하나도 없었다.** 라우트만 열면 데모 목록이 새고, 목록을 막으면 로그인이 없다.

답은 플래그를 가른 것이다 — 로그인은 모든 프로파일에 등록하고, 지름길만 `demo_shortcuts_enabled`(= 개발) 뒤에 뒀다. 그 전 작업에서도 같은 모양의 사고가 있었다: `developer_auth_enabled` 가 권한뿐 아니라 **라우트 등록**까지 감싸 PRODUCTION 에서 API 가 통째로 사라졌다.

## 경계와 오해

- **「운영을 개발 프로파일로 띄우면 되지」는 답이 아니다** — 지름길이 함께 열린다. 헤더 하나로 아무 멤버로나 행세할 수 있게 된다
- **가드는 지우는 게 아니라 좁힌다** — 데이터 적재 도구의 「로컬 DB 만」 가드는 그대로 두고 dump 로 우회 없이 옮겼다([[seed-data]])
- **테스트가 계약을 고정해야 한다** — 「운영 로그인 200·Secure 쿠키·틀린 비번 401·페르소나 헤더 401」처럼 프로파일별 기대를 시험으로 박는다

## 함께 보는 개념

- [[externalized-configuration]] — 프로파일 값이 오는 곳
- [[seed-data]] — 같은 프로파일 가드가 데이터 도구에도 걸린다

## 출처

- [[2026-10-01-strong-hajin-deploy]] — `local_login_enabled` → `demo_shortcuts_enabled` 로 가르고 로그인을 프로파일 무관 등록(코드 #5)
