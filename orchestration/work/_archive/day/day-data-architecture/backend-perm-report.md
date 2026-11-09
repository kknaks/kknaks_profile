# 시술 현황 1차 기본 권한 채우기 (백엔드)

`e5912d2b` 위 미커밋. 정본: 원천 `procedure-board-decisions.md` 「결정 — 시술 현황 1차 기본 권한」(사용자 2026-11-08).

## #231 영향
없음 — 권한 행이 채워져, `/board` 버튼 숨김(`permissions`)이 직무대로 실제로 갈린다. `DAY_ADMIN_EMAILS` 는 그대로다.

## 만든 것
- `day/services/default_permissions.py`:
  - `defaults_for(name, tags)` — 순수 함수. 결과는 셋 중 하나다.

    | 묶음 | 행 |
    |---|---|
    | 보기 · 수정 · 수락 | `board`=edit(edit 은 view 포함) + `board.accept`=edit |
    | 보기 | `board`=view |
    | 없음 | 행 없음 |

  - 판정 순서는 ① 이름 표 → ② 태그 → ③ 없음이다.
    - 태그 규칙: `nurse` · `skincare` · `doctor` · `admin` 중 하나라도 있으면 전부다. 그 밖에 `counselor` · `coordinator` · `call_counselor` 가 있으면 보기다.
  - `seed(session, hospital_id)` — 그 병원 살아 있는 직무마다 **없는 (직무, 키) 행만** `INSERT … ON CONFLICT DO NOTHING` 한다.
- `services/emr_sync.run_master` — `apply_master` 와 같은 transaction 에서 `seed` 를 부른다. 회차 결과에 `permissions_seeded`(넣은 행 수)가 실린다.

### 이름 표 — 태그만으로는 결정 표와 다른 직무(데모 지점 KOS 이름)
결정 표는 「경영지원 · 마케팅 · 마취과」를 이름 줄로 적었다. 실제 데모 태그와 맞춰 보니 **두 줄이 더** 태그 규칙과 달라서 표가 이기게 넣었다.

| 직무 | 데모 태그 | 태그 규칙 결과 | 결정 표 |
|---|---|---|---|
| 경영지원 | admin | 전부 | **없음** |
| 마케팅 | admin | 전부 | **없음** |
| 마취과 | (없음) | 없음 | **전부** |
| **CS팀(콜센터)** | call_counselor | 보기 | **없음**(표 「CS팀」) |
| **상담총괄실장** | counselor · admin | 전부 | **보기** |

- 아래 두 줄(CS팀 · 상담총괄실장)은 결정 문구 「태그만으로 안 되는 줄은 이름으로 덮는다 · 구현이 정확히 이 표를 내야 한다」를 따랐다.
  - planner 가 SPEC-002 에 이름 표 다섯 줄로 적을 것.
- 이름은 데모 KOS 이름 그대로다(`CS팀(콜센터)` 괄호 포함 · 앞뒤 공백만 무시). 다른 병원은 이름이 다르면 태그 규칙만 탄다 — 병원을 붙일 때 코디가 확인.

## 기본값과 사람이 고친 값 — 지금 정책 · 제안
- **지금(구현)**: 「없는 행만 넣고 있는 행은 절대 안 건드린다」.
  - PK 가 `(job_role_id, permission_key)` 이고 지운 행(`deleted_at`)도 PK 를 잡는다. 그래서 사람이 **바꾼** 수준 · **지운** 행 모두 다음 회차가 되돌리지 않는다.
  - 기본값 「없음」인 직무는 행이 없어 매 회차 다시 판정된다. KOS 에서 태그가 바뀌면(예: 마케팅에 nurse 추가 — 이름 표가 먼저라 그대로 없음) 판정이 바뀔 수 있다.
  - 이 방식의 한계:
    - 결정 표가 나중에 바뀌어도 이미 있는 행은 안 바뀐다(새 키만 들어간다).
    - KOS 에서 태그가 줄어도 남은 권한이 안 빠진다.
    - 「이 행이 기본값인지 사람이 고쳤는지」를 행만 보고는 모른다.
- **제안(관리 화면이 생길 때 · migration 필요)**: `job_role_permission` 에 `source`(`default` | `manual`) · `updated_by_staff_id` 를 둔다.
  - 동기화는 `source = default` 인 행만 표대로 넣고 · 바꾸고 · 지운다.
  - 관리 화면에서 고치면 `manual` 이 되어 동기화가 다시는 손대지 않는다.
  - 「기본값으로 되돌리기」는 `manual` → 지우기 → 다음 회차가 `default` 로 다시 넣는다.
  - 표가 바뀌면 `default` 행만 따라간다.

## 테스트
- DB 없이(`tests/day/test_default_permissions.py`):
  - 데모 직무 15개(이름 · 태그 = `day_dev` 기준 정보 그대로) → 결정 표와 정확히 같다.
  - 다른 이름은 태그 규칙 · 앞뒤 공백.
- infra(`test_emr_sync_service.py`):
  - 기준 정보 회차 → 직무마다 `defaults_for` 와 같은 행 · `permissions_seeded` 수.
  - 한 직무의 `board` 를 view 로 낮추고 `board.accept` 를 지운 뒤 다시 회차 → 0행 넣음 · 바뀐 값 그대로.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 307 passed |
| `scripts/test.sh -q` | 465 passed |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait api worker scheduler` |

## 실물(데모 지점 · scheduler 시작 때 기준 정보 회차 · 이름 · 키만)
worker `emr master … done` · `permissions_seeded: 19`(전부 8직무 × 2 + 보기 3직무).

| 직무 | 권한 행 |
|---|---|
| 간호 · 피부관리 · 마취과 · 원장 · 대표원장 · OWNER · 관리자 · ADMIN | `board=edit` · `board.accept=edit` |
| 코디 · 상담실장 · 상담총괄실장 | `board=view` |
| CS팀(콜센터) · 경영지원 · 마케팅 · 촬영팀 | 없음 |

결정 표와 같다.

## 남은 것
- SPEC-002: 이름 표 다섯 줄(CS팀 · 상담총괄실장 추가)을 planner 가 적을 것.
- 관리 화면이 생길 때 `source` 칸(위 제안) 결정.
- 다른 병원 연결 때 직무 이름 확인(코디).
