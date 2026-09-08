---
type: concept
id: resource-scoped-token
title: 리소스 범위 단명 토큰 (Resource-scoped Short-lived Token)
aliases:
  - 회의별 토큰
  - 단명 토큰
  - allowlist 표면
  - meeting token
up:
  - 2026-09-08-docs-v1
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

## 왜 중요한가

무상태 JWT 는 폐기 표면이 없어 「마감 시 best-effort 폐기」가 성립하지 않는다. 지울 행이 있어야 한다. 그렇다고 새 테이블을 만들 이유는 없다 — 이미 있는 세션 테이블에 종류 하나를 더하면 된다.

## 경계와 오해

- **원문 컬럼은 예외다** — 사람 토큰(refresh)에는 여전히 해시만. 원문을 두는 근거(단명 · 범위 · 삭제 폐기 · 제출마다 재사용)가 전부 있을 때만.
- **범위 검사는 경로 패턴이 아니라 allowlist 로** — 「id 가 있는 경로만 검사」는 목록·검색 표면을 놓친다.
- **부분 인덱스는 비유니크** — 「리소스당 하나」는 상태 전이 게이트가 지키고, 재발급 순간 두 행이 겹칠 수 있어 유니크로 못 건다.

## 함께 보는 개념

- [[tool-allowlist-by-phase]] — 이 토큰을 헤더에 싣는 도구 호출
- 사람 토큰(refresh)의 회전·해시 규칙은 `account.md` A-7

## 출처

- 코드: `app/back/api/deps.py` `_MEETING_TOKEN_SURFACES` · `service/auth_service.py issue_meeting_token/revoke_meeting_token` · 커밋 `0b3f7b7` · `0415290`
- 문서: `para/projects/summer-star/task-management/40-architecture/database/domains/account.md` A-13 · 검수 `work009-review-report.md` F-1
