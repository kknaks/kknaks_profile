# [planner · micro] WP-131 Phase 상태 갱신 — 검수 PASS 후

**`reviewer_code` 검수가 끝났다: PASS (계약 위반 0 · FAIL 0 · WARN 4 · 관찰 5).**

**네가 Phase 상태를 안 올리고 넘긴 판단이 옳았다** — 「어느 Phase 가 착지했는지 내가 검증하지 않았다」가 정확한 이유였다. 이제 근거가 생겼으니 올린다.

Phase 8 에 SPEC AC 대응을 **억지로 만들지 않고** 「대응 AC 가 없다 — 구멍이 아니라 축이 다르다」로 처리한 것도 맞다. AC 16건은 계약 층이고 대시보드 결정성은 구현 층이라, 거기서 AC 를 지어냈으면 대응표가 거짓이 됐다.

## 근거 — 코디가 직접 돌린 수치

| 대상 | 결과 |
|---|---|
| `tests/migrations/test_0139_deployment_surface_key.py` | **8 passed** (왕복 + down 중복가드 실제 재현) |
| `tests/api/test_gm_command.py` + `tests/api/test_admin_deployments.py` | **63 passed / 12 failed** |
| `tests/services/test_deployment.py` | (gm 과 합산) 57 passed |
| `tests/services/test_dashboard_split.py` | **30 passed** (기존 25 무수정 통과 = 행 1건 제품 불변) |
| `front` `npx tsc --noEmit` | **exit 0** |
| `front` `vitest __tests__/wp131-deploy-surface.test.tsx` | **5 passed** |

**12 failed 는 기존 환경 문제**다 — `flaky-baseline-evidence.md` 에 판정이 있다(우리가 무접촉인 파일이 같은 사유로 9/11 실패). **재조사하지 마라.**

검수 지적 중 **잠복 버그 4건 + FE 테스트 신설**이 추가 판으로 닫혔다(`sa_text` 별칭 · 상한 단일화 + 소스 단언 · `showSurface` 서버 기준 · 미저장 초안 확인 제거 · `wp131-deploy-surface.test.tsx` 5건 + `vitest.config.ts` 등재).

## 할 것 — `work-131-deploy-surface-axis.md` 한 파일

1. **Phase 1~8 의 `Status:` 를 `DONE` 으로.** 각 Phase 의 **`완료 증거` 칸에 위 표의 해당 수치**를 적어라(Phase 별로 무엇이 그 Phase 를 증명하는지 골라서 — 예: Phase 1 = migration 8 passed, Phase 4 = `/gm` 회귀 하드코딩 테스트, Phase 8 = dashboard 30 passed 중 기존 25 무수정 통과).
2. **frontmatter `status: proposed` → `in_dev`.** ⚠ **`done` 으로 올리지 마라 — 머지·배포 전이다.** 이 레포 선례가 그렇다(`log.md` 2026-09-01 행: 「**`done` 으로 올리지 않는다 — 머지·배포 전이다**」, WP-129·130 이 P0 실측을 Pre-deploy 로 이월한 채 `in_dev` 로 갔다).
3. **`products/mediness/30-work.md` 3표 동기** — Status Board·WP List 의 WP-131 상태를 `proposed` → `in_dev`. **Spec Coverage 의 SPEC-051 행은 이미 `in_dev` 라 그대로**(derive 도 그대로 맞는다 — 커버 WP 에 `in_dev` 가 섞이면 derive 가 `in_dev`).
4. **§Open Issues 에 2루프 이월 3건을 추가**해라. 검수가 「관찰」로 분리한 것 중 **사용자 화면 결정이 필요한 것들**이다(리포트 `review-code-report.md` §관찰 참조):
   - **O-1** 모달 배치 저장이 빈 신규 카드 하나로 전부 중단된다(시안은 `continue`, TSX 는 `return`). 행 수가 늘수록 비싸고 에러가 화면 밖에 뜬다. **정책 결정이라 사용자 E2E 에서 정한다.**
   - **O-2** 「surface 오름차순」이 층마다 다른 정렬(FE `localeCompare(ko)` / `/gm`·대시보드 파이썬 코드포인트 / DB PG collation). 계약 위반은 아니나 **모달 순서와 슬랙 순서가 갈릴 수 있다.**
   - **O-5** 「환경 불변」 안내문이 카드마다 반복(6행이면 6번). 반복 위치는 화면 결정.
   - 이미 아는 관찰 3건(`prod` 칩 6회 · 백필 `기본` 첫인상 · 빈 surface 를 저장 눌러야 앎)도 **같은 자리에 묶어라** — 2루프가 한 목록을 본다.
5. **§Pre-deploy Check 에 한 줄 추가** — 기존 실패 12건(`TestProductAssigneeAccess`)이 **테스트 DB 의 `org_unit↔department` 매핑 seed 누락**이라 초록을 못 본다는 것. **권한 회귀 0 은 diff 로 확인했고**(`policies/deployment.py`·게이트 무변경), 배포 전 **실환경에서 담당자 경로 1건은 손으로 확인**할 것.

## 하지 말 것

- **`status: done` 금지.** 머지·배포 전이다.
- **`spec-051`·`21-html`·`log.md` 를 고치지 마라** (`30-work.md` 는 3번 항목만).
- **계약을 바꾸지 마라.** Phase 내용·AC 대응표는 확정이다.
- **12건 기존 실패를 재조사하지 마라.**
- 코드 레포 수정 금지. 커밋·push·PR 금지 — **코디가 PR #762 브랜치에 얹는다.**

## 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- **0 error 유지.** warning 수가 263 에서 달라지면 **전문을 인용**해라 — 3표 동기가 어긋나면 여기서 잡힌다.

## 리포트

`planner-report.md` 에 「9차 — Phase 상태 갱신」 절로. 올린 Phase·증거·3표 동기 결과 + lint 수치.

끝나면 §9 완료 보고 두 채널. **코디handle 은 preamble 값을 믿어라.**
