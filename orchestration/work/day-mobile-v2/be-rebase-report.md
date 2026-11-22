# day-mobile-v2 rebase 결과 보고 — origin/dev(f724b149) 위로 · migration 0013 · 0014

## 상태: done (push 안 함 — 코디가 force push)

- 브랜치 `kknaksss/day-mobile-v2` · 옛 HEAD `921d88cd`(base `844eace4` · 16커밋)
- **새 HEAD `8a76c35bc956a32fb64d66968274ba5069cf058d`** = `origin/dev` `f724b149`(#265 `0012_kos_keys`) 위 16커밋 + 번호 고침 커밋 1 = 17커밋
- 작업 트리 깨끗(추적 파일 변경 없음)

## 충돌과 푼 방법

| 커밋 | 파일 | 충돌 | 푼 방법 |
|---|---|---|---|
| `9162ee18`(P3 호출 취소 알림) | `backend/tests/migrations/test_alembic.py` | `HEAD =` 한 줄 — dev `0012_kos_keys` ↔ 우리 `0012_doctor_call_cancel_kind` | rebase 중에는 그 커밋의 값(우리 쪽)으로 두고, 마지막 번호 고침 커밋에서 새 head `0014_device_platform_android` 로 맞춤 |

그 밖 15커밋은 충돌 없이 적용(dev 쪽 변경은 `emr/` · `models/` · KOS 키 테이블 · 시험 — 우리 변경과 겹치지 않음). 중간 커밋들은 head 가 둘인 상태(0012 두 개)를 지나므로, 하나씩 따로 체크아웃하면 alembic head 가 둘이다 — 끝 커밋에서 하나로 닫힘(브리프 3 대로 번호 고침은 끝 커밋 하나).

## migration 번호

| 옛 | 새 | down_revision |
|---|---|---|
| `20261120_0012_doctor_call_cancel_kind.py` · `0012_doctor_call_cancel_kind` | `20261120_0013_doctor_call_cancel_kind.py` · **`0013_doctor_call_cancel_kind`** | `0012_kos_keys`(dev) |
| `20261120_0013_device_platform_android.py` · `0013_device_platform_android` | `20261120_0014_device_platform_android.py` · **`0014_device_platform_android`** | `0013_doctor_call_cancel_kind` |

- 함께 고친 곳: `tests/migrations/test_alembic.py`(HEAD) · `test_doctor_call_cancel_migration.py`(파일 · 이름 · down 대상 `0012_kos_keys`) · `test_device_platform_android_migration.py`(파일 · 이름 · down 대상) · `day/enums/notification.py` · `day/enums/device.py`(주석의 migration 번호)
- 커밋 `8a76c35b chore(migrations): 0013 · 0014 로 — dev 0012_kos_keys 뒤`

## 검증

| 항목 | 결과 |
|---|---|
| `scripts/check.sh --static` | **통과**(구조 · ruff · format · strict mypy · Taut · frontend) |
| migration 실제 PG(격리) — 한 단계씩 | up `0011 → 0012_kos_keys → 0013_doctor_call_cancel_kind → 0014_device_platform_android` · down `→ 0013 → 0012 → 0011` · up head = `0014` · `alembic heads` = `0014_device_platform_android (head)` 하나(일회 시험 파일로 돌리고 지움) |
| `scripts/test.sh -q backend/tests/migrations` | **40 passed**(base 까지 내렸다 올림 · `alembic check` · 우리 두 migration up/down/up 포함) |
| `scripts/test.sh -q`(전체 · 격리 인프라) | **2166 passed** |
| `cd app && flutter analyze` (fvm 3.44.8) | No issues found |
| `flutter test` | **416 passed**(~81 skip · 기존 그대로) |

## 코디가 확인할 것

- push 는 하지 않았다 — `git push --force-with-lease origin kknaksss/day-mobile-v2` 는 코디 몫(origin 은 아직 `921d88cd`).
- `flutter` 가 PATH 에 없어 `~/fvm/versions/3.44.8/bin/flutter`(앱 `.fvmrc` 와 같은 판)로 돌렸다.
