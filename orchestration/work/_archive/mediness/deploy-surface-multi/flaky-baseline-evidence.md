# 기존 실패 기준선 — deploy-surface-multi (BE)

> **한 번 판정하고 파일로 남긴다.** 이후 워커·검수는 이 판정을 인용한다.
> 안 남기면 「이번 계약이 초록이다」가 증명이 안 닫힌다(런북 §STEP 6).
> 판정자: 코디네이터 · 2026-09-22 · 워크트리 `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`

## 판정: **환경 문제 — 이번 변경과 무관**

### 대상 12건

`back/tests/api/test_admin_deployments.py::TestProductAssigneeAccess` **전건**:

```
test_assignee_get_own_product_200          test_assignee_create_own_product_201
test_assignee_get_includes_password        test_assignee_create_other_product_403
test_assignee_get_without_slug_403         test_assignee_any_department_allowed
test_assignee_get_other_product_403        test_assignee_patch_own_product_200
test_assignee_patch_other_product_403      test_assignee_delete_own_product_204
test_assignee_patch_unknown_id_403         test_assignee_delete_other_product_403
```

`tests/api/test_admin_deployments.py` 단독 실행 = **12 failed, 36 passed**.

### 원인

`product_assignment` INSERT 시 **DB 트리거**가 거절한다:

```
WBS_DEPARTMENT_ORG_UNIT_UNMAPPED: be
```

테스트 DB(`localhost:25434/mediness_test`)에 **`org_unit` ↔ `department` 매핑 seed 가 없다.** 코드 결함이 아니라 테스트 DB 상태다.

### 무관하다는 근거 — 교차 확인 (코디 직접 실행)

**우리가 한 글자도 건드리지 않은 파일**이 같은 사유로 실패한다:

```bash
$ git status --porcelain tests/schema/test_product_assignment_schema.py
(출력 없음 — 무접촉)

$ uv run python -m pytest tests/schema/test_product_assignment_schema.py -q
9 failed, 2 passed in 7.50s
```

실패 축이 전부 `product_assignment` 생성 경로다(`TestLeadExclusion` · `TestDepartmentNoDbConstraint` · `TestFk` …). **surface 축과 접점이 0** 이다 — 우리 변경은 `product_deployment` 테이블과 `/gm`·모달뿐이고 `product_assignment` 를 읽지도 쓰지도 않는다.

### 이번 계약이 초록이라는 증거 (코디 직접 실행)

| 대상 | 결과 |
|---|---|
| `tests/migrations/test_0139_deployment_surface_key.py` | **8 passed** (왕복 upgrade→downgrade→upgrade + down 중복가드) |
| `tests/api/test_gm_command.py` + `tests/services/test_deployment.py` | **57 passed** |
| `tests/api/test_admin_deployments.py` | 36 passed / 12 failed(위 12건 = 전부 `TestProductAssigneeAccess`) |

**surface 축을 검증하는 항목 중 실패는 0건이다.**

### 주의

- 이 12건은 **권한(`product_assignment` 참여자) 경로**를 검증하는 테스트다. 환경 때문에 **지금 초록을 못 보는 것**이지 「권한이 안 깨졌음이 증명됐다」는 뜻은 아니다.
- 우리 변경이 권한 게이트를 건드리지 않았다는 것은 **diff 로** 확인한다(`policies/deployment.py`·`routers/deployments.py` 의 게이트 부분 무변경).
- 테스트 DB 에 `org_unit↔department` 매핑을 시드하면 이 12건은 살아난다. **이번 작업 범위 밖**이다.
