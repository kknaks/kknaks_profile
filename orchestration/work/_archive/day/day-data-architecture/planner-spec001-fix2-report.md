# SPEC-001 검수 WARN 반영 + SPEC-000 token_hash · OQ-04-1 — 결과 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 브랜치) · `products/day/` 만. 커밋 안 함. 결정 원천 = 바뀐 `erd/04-staff.md` 「로그인 · 세션 계약 (2026-11-05 사용자 결정 — DAY-SPEC-001)」 절 + `login_session.token_hash` 행 + 「정할 것」1 닫힘.

### `products/day/20-spec/spec-001-login-session.md`

| 줄 | 바뀐 것 | 검수 |
|---|---|---|
| :25 | 머리 「2026-11-05 개정 ②」 — 결정 원천 = 04 「로그인 · 세션 계약」 절 | — |
| :85 (S-1 3) | 처음 만든 `account` 는 `is_active = true` | W4-2 |
| S-1 5 | 비활성 판정 = 기준 정보 동기화가 KOS `get-accounts.activate` 로 채운 `staff.is_active` | 열린 것 |
| S-3 2 | 병원 여럿 → 후보 + 임시 토큰(5분) → `POST /api/auth/hospital`(임시 토큰 · 고른 병원) → 진짜 세션 · 하나면 바로 세션 | 열린 것 |
| S-4 1 | 로그아웃된 세션 요청 = `unauthorized` | W1 g |
| §3 API 표 | login / hospital 행에 임시 토큰(5분) · `POST /api/auth/hospital` · `POST /api/auth/logout` 확정 | W1 a · b |
| :146 | **세션 토큰** = 따로 만든 무작위 값 · 쿠키 / Bearer 에 그 토큰 · DB 에는 `login_session.token_hash`(UNIQUE) — 세션 id 를 그대로 쓰지 않음 | W4-1 |
| Validation | 형식 · 길이 검사는 KOS 에 맡긴다(사용자 2026-11-05) · 병원 고르기는 임시 토큰 5분 안 | W2 |
| 케이스 매트릭스 | `kos_unavailable` = KOS 장애(KOS 403 `Unsupported client.` 포함 · 시간 제한 15초 넘김) · 2단계 인증 안내는 「문구 예시 — 확정은 화면 SPEC」 · `session_expired` = 만료(+ KOS 조기 401) · `unauthorized` = 세션 없음 · 로그아웃된 세션 · 코드 근거 문장을 「사용자 2026-11-05 결정」으로 교체 | W1 c~g · W2 |
| Flow | 임시 토큰 · token_hash · 무작위 세션 토큰 | — |
| :228 Functional Rule | 7 「세션 토큰 무작위 · token_hash 만」 새로 · 2 account 기본값 · 6 임시 토큰 · 10 KOS 시간 제한 15초 · 12 비활성 판정 (13개로) | W4 · 열린 것 |
| §5 「검수 뒤 정한 것」 표 새로 | 11행 — 경로 2 · 추가 코드 3 · kos_unavailable / session_expired 범위 · 형식 검사 · 안내 문구 · 세션 토큰 · account 기본값 · 시간 제한 · 비활성 판정 · 임시 토큰 | — |
| :276 「아직 열린 것」 | 1개만 남김(아래 미결 1) + permission_key(SPEC-000 OQ-04-2) 참조 | — |

### `products/day/20-spec/spec-000-data-model.md` (생성기로 다시 옮김 — diff 9줄)

- :595 §3 04 `login_session` 표에 `token_hash` 행(원천 그대로). `id` 설명이 원천대로 「DAY 로그인 세션」(「쿠키가 가리킨다」 빠짐).
- :615 `#### 로그인 · 세션 계약` — 원천 04 의 새 절은 **SPEC-001 이 정본이라 복제하지 않고 링크 한 줄**만(한 곳 원칙). 생성기가 이 절을 빼도록 바꿈.
- :1293 OQ-04-1 취소선 + 「→ 정함: DAY-SPEC-001 OQ-6(1차는 막기 — 사용자 2026-11-05)」.
- `last_updated` 2026-11-05.

### `products/day/40-architecture/erd.md`

- :134 인벤토리 `login_session` 핵심 키에 `token_hash` UNIQUE.

### `products/day/log.md`

- :17 2026-11-05 `spec-change` · DAY-SPEC-001, DAY-SPEC-000 · #909.

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 은 타 제품 기존 — 무관)
```

SPEC-000 은 원천 04 를 다시 생성했다 — 원천 대비 바뀐 줄은 위 세 자리뿐(표 행 누락 0).

## 미결 · 주의점

1. **임시 토큰(5분)이 지난 병원 고르기 요청의 오류 코드** — 결정은 「5분 임시 토큰」까지라 만료 시 코드(`session_expired` / `unauthorized`)는 정하지 않았다. SPEC-001 「아직 열린 것」에 하나 남겼다. 권장: `session_expired`(시간이 지나 끝난 것 — 「만료」와 같은 뜻).
2. **KOS 가 만료 전에 401 을 줄 때의 코드** — 결정은 `session_expired` 를 「만료만」, `unauthorized` 를 「세션 없음 · 로그아웃된 세션」으로 정했다. KOS 조기 401 은 「DAY 세션 만료 = KOS 토큰 만료」의 연장으로 보고 `session_expired` 에 두었다 — 다르게 보려면 알려 달라.
3. 원천 04 를 SPEC-000 에 옮길 때 새 「로그인 · 세션 계약」 절은 링크로만 두었다(생성기가 그 절을 제외). 원천을 그대로 옮긴다는 1판 계약과 한 곳 원칙이 부딪쳐 한 곳 원칙을 택했다.
4. 이전 리포트대로 — Delivery #227 의 target 에 SPEC-001 을 넣는 재결속(version 2 · L3 재승인)은 코디 몫.
