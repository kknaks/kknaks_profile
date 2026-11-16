# SPEC-001 재검수 W1 — session_expired 범위 결과 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 브랜치) · 커밋 안 함. 원천 = 바뀐 `erd/04-staff.md` 「로그인 · 세션 계약」 오류 행(:128) · 재로그인 행(:129). 결정(사용자 2026-11-05): KOS 조기 401 → `session_expired` · 임시 토큰(5분) 만료 → `session_expired` · KOS 401 로 세션을 끝낼 때 `login_session.expires_at` 을 지금으로(`revoked_at` 은 로그아웃에만).

`products/day/20-spec/spec-001-login-session.md` — 지시한 자리만:

| 줄 | 바뀐 것 |
|---|---|
| :168 | 매트릭스 만료 행 — 「KOS 가 만료 전 401(KOS 토큰이 일찍 끝남)」 → 401 `session_expired` |
| :169 | 매트릭스 새 행 — 병원 고르기 임시 토큰(5분) 만료 → 401 `session_expired` · 로그인부터 다시 |
| :173 | 범위 문장 — `session_expired` 는 만료(KOS 조기 401 · 임시 토큰 만료 포함) |
| :209 | 상태도 — 「KOS 가 401 → expires_at 을 지금으로 당김」 |
| :230 | Functional Rule 8 — KOS 조기 401 이면 `login_session.expires_at` 을 지금으로 당긴다(`revoked_at` 은 로그아웃에만) · 그 뒤 요청은 `session_expired` |
| :268 | §5 「검수 뒤 정한 것」 `session_expired` 범위 행 — 원천 :128 · :129 문구대로 |
| :277-279 | 「아직 열린 것」 → 「없음」(permission_key 는 SPEC-000 OQ-04-2 참조만) |
| :36 | 메타 「Open Questions」 줄 — 「아직 열린 것 없음」(위와 같은 사실 · 숫자 안 맞는 것 정리) |

`products/day/log.md:17` — 2026-11-05 `spec-change` · DAY-SPEC-001 · #909.

그 밖(S-4 서술 등)은 건드리지 않았다 — S-4 2 「그 세션을 끝내고」는 바뀐 규칙과 어긋나지 않는다.

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 은 타 제품 기존 — 무관)
```

## 미결 · 주의점

- SPEC-001 에 열린 것 없음. 남은 일은 이전 리포트대로 Delivery #227 의 target 에 SPEC-001 을 넣는 재결속(version 2 · L3 재승인 — 코디 몫).
