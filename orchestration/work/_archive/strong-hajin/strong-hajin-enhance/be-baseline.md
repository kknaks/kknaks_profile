# WP1-BE 기준선 (고치기 전)

- 코드: 워크트리 `strong-hajin-enhance` · HEAD `f0ad522` · `git status` clean (2026-10-07)
- 격리 PostgreSQL: `docker run postgres:16.6` 이름 `sh-enhance-be-pgtest` · `127.0.0.1:55439` (사용자 54329 는 건드리지 않음)

| 시험 | 명령 | 결과 |
|---|---|---|
| unit + architecture (인벤토리 drift 포함) | `make test-unit` | **477 passed**, 1 deselected · exit 0 |
| contract (병렬 + 직렬) | `make test-contract` | 병렬 **1245 passed** · 직렬 **128 passed** · exit 0 |
| postgres 통합 | `make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:55439/ax_test` | **106 passed** · exit 0 |

**기존 실패: 0건.** 이후 실패는 모두 「이번 실패」로 본다.

- `make verify` 는 기준선에서 돌리지 않았다. frontend 쪽은 frontend 워커가 동시에 고치는 중이다. 또한 `make frontend-test` 는 병렬 vitest 인데, 사용자 로컬 스택이 떠 있는 기계에서는 병렬 vitest 를 쓰지 않는다(WORK-012 P-9)

---

# WP2-BE 기준선 (WP1 커밋 `e51fe3b` 위 · 고치기 전)

| 시험 | 결과 |
|---|---|
| `make test-unit` | **491 passed** · exit 0 |
| `make test-contract` | 병렬 **1268 passed** · 직렬 **128 passed** · exit 0 |
| `make test-postgres`(격리 `127.0.0.1:55439`) | **107 passed** · exit 0 |

**기존 실패: 0건.**
