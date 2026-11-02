---
type: concept
id: resource-scoped-token
title: 리소스 범위 단명 토큰 (Resource-scoped Short-lived Token)
aliases:
  - 회의별 토큰
  - 단명 토큰
  - allowlist 표면
  - meeting token
  - 토큰 링크
  - 로그인 없는 링크
  - 고객 문진 링크
  - URL fragment 토큰
up:
  - 2026-09-08-docs-v1
  - 2026-10-28-overall-board
tags:
  - auth
  - token
  - mcp
  - allowlist
---

# 리소스 범위 단명 토큰

사람 계정의 access 토큰 대신, **리소스 하나(회의 하나)에만 묶인 짧은 토큰**을 자동화(AI 도구 서버)에게 준다. 토큰은 세션 테이블의 행이고, 그 행으로 계정·리소스 범위를 판정하며, 폐기는 행 삭제다.

## 정의

1. **발급** — 리소스가 활성 상태로 전이할 때(`/start`) 같은 트랜잭션에서 `auth_session(kind='meeting', meeting_id)` 행 하나를 INSERT 한다. 리소스당 하나.
2. **원문 저장** — refresh 토큰처럼 해시만 두지 않고 **원문을 컬럼**에 둔다. 매 제출이 원문을 헤더에 실어야 하는데, 제출마다 재발급하면 오버헤드다. 단명 · 리소스 범위 · 행 삭제 폐기라 노출 위험이 refresh 와 다르다. 회전하지 않으므로 `revoked_at` 도 없다.
3. **표면 allowlist** — 이 토큰으로 열리는 REST 는 명시된 몇 개뿐(`(method, route.path)` 집합). 그 밖은 존재를 숨기는 404. 「경로에 `{meeting_id}` 가 있을 때만 범위 검사」로 두면 목록 API 가 열린다 — 검수가 잡았다.
4. **폐기** — 리소스가 종결될 때 best-effort DELETE. 실패는 만료(TTL 분 단위)가 흡수한다.
5. **재시도** — 종결 뒤 다시 돌리는 경로(`/finalize`)는 행이 없으므로 **같은 발급 함수로 새로 낸다.** 남은 행이 있으면 지우고 내서 「리소스당 하나」를 유지한다. 「실패 시 안 지움」은 TTL 때문에 늦은 재시도를 못 살린다.

## 사용 예시

```python
_MEETING_TOKEN_SURFACES = frozenset({
    ("GET", "/api/meetings/current"), ("GET", "/api/meetings/current/tasks"),
    ("GET", "/api/meetings/{meeting_id}"), ("GET", "/api/tasks/{task_id}"),
    ("GET", "/api/work-types"), ("GET", "/api/auth/session"),
})
```

## 다른 꼴 — 로그인 없는 사람에게 주는 링크

같은 발상(리소스 하나 · 짧은 시한 · 정해진 표면)을 **계정이 없는 사람**에게 링크로 줄 수 있다. 전체현황판의 고객 문진은 직원 기기 안 잠금 화면 대신 **고객 자기 폰의 웹 페이지(`/q`)** 로 열린다 — 데스크 화면이나 직원 앱이 QR 을 보여 주고 고객이 찍는다.

- **요청 1행 = 링크 1개** — 띄우기 요청 행 하나가 링크 하나를 만든다. 문진 전용 표는 없다
- **토큰 = HMAC(서버 비밀, 「종류 | 행 id | 무작위 nonce」)** — DB 엔 nonce 와 **토큰 해시만** 두고 원문은 없다. 그래도 로그인한 직원 화면은 같은 식으로 링크를 **다시 그릴 수 있다**(새로고침 · 나중에 받는 앱). 찾기는 해시로, 찾은 뒤 HMAC 을 다시 계산해 상수 시간 비교. 회의 토큰이 원문 컬럼을 둔 것과 반대 선택이다 — 여기는 다시 그리기만 필요하고 서버가 원문을 보관할 이유가 없다
- **토큰은 URL 의 `#` 뒤(fragment)에** — 브라우저가 fragment 를 서버로 보내지 않으므로 ingress · back 접근 로그와 다른 사이트 `Referer` 에 안 남는다. 페이지는 `location.hash` 에서 읽어 **헤더**로만 싣는다(경로 · 쿼리 금지). `no-referrer` · `noindex`
- **시한 둘 · 한 번 제출** — 여는 시한 10분(QR 이 떠 있는 동안) · 연 뒤 쓰는 시한 60분 · 제출 성공이면 그 링크는 끝(두 번째는 409). 새 요청이 옛 것을 닫는다
- **표면은 공개 API 두 개(읽기 · 제출)** — 돌려주는 것은 그 행 한 고객의 이름 · 미리 채움 · 양식뿐. 예약 id · 원천 id · 다른 예약은 싣지 않는다. 직원 세션 코드를 아예 안 쓰는 별도 호출부라 직원 폰에서 열려도 직원 토큰이 실리지 않는다
- **남는 위험은 글로 적는다** — 링크를 가진 사람은 미리 채운 값을 본다. 짧은 시한 · 한 번 제출 · 틀린 토큰 속도 제한으로 줄일 뿐이다. 클라이언트 IP 를 어느 헤더에서 믿을지는 리뷰에서 경고로 남았다

## 왜 중요한가

무상태 JWT 는 폐기 표면이 없어 「마감 시 best-effort 폐기」가 성립하지 않는다. 지울 행이 있어야 한다. 그렇다고 새 테이블을 만들 이유는 없다 — 이미 있는 세션 테이블에 종류 하나를 더하면 된다.

## 경계와 오해

- **원문 컬럼은 예외다** — 사람 토큰(refresh)에는 여전히 해시만. 원문을 두는 근거(단명 · 범위 · 삭제 폐기 · 제출마다 재사용)가 전부 있을 때만.
- **범위 검사는 경로 패턴이 아니라 allowlist 로** — 「id 가 있는 경로만 검사」는 목록·검색 표면을 놓친다.
- **부분 인덱스는 비유니크** — 「리소스당 하나」는 상태 전이 게이트가 지키고, 재발급 순간 두 행이 겹칠 수 있어 유니크로 못 건다.

## 함께 보는 개념

- [[tool-allowlist-by-phase]] — 이 토큰을 헤더에 싣는 도구 호출
- [[jwt]] — 서버 저장 없이 검증하는 다른 토큰(폐기 표면이 없다)
- [[external-write-queue]] — 제출을 원천에 보내고 다시 읽을 때 원천이 첫 제출본을 주는 경우
- 사람 토큰(refresh)의 회전·해시 규칙은 `account.md` A-7

## 출처

- [[2026-10-28-overall-board]] §2 — 고객 문진 = 로그인 없는 토큰 링크 웹 페이지(HMAC · nonce · 해시만 저장 · fragment · 10분 / 60분 · 한 번 제출 — SPEC-006 · DEC-008 · 코드 `00853e1`)
- 코드: `app/back/api/deps.py` `_MEETING_TOKEN_SURFACES` · `service/auth_service.py issue_meeting_token/revoke_meeting_token` · 커밋 `0b3f7b7` · `0415290`
- 문서: `para/projects/summer-star/task-management/40-architecture/database/domains/account.md` A-13 · 검수 `work009-review-report.md` F-1
