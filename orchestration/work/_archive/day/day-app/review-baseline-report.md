# 리뷰 리포트 — day-app / stable 기준선 최종 검수 (2026-11-09)

- 대상: `mediness-mediness/day-app-spec` · `kknaksss/day-app-spec` · HEAD `b4cd1a00` · fetch한 `origin/main` = `3f57c1af09afa7ce185cd754244c714bf1ec11e5`
- 근거: `planner-baseline-report.md` · `baseline-brief.md` · `review-policy-report.md`(PASS) · `review-wp2-report.md`(PASS) · `delivery-request.json` · `delivery-plan-approval.json`(human · 「응 진행하자 !」 · `sha256:c4f70ae3…c75e`) · Issue #235
- read-only. 역할 경로 `roles/day/reviewer_doc/`는 없어서 `roles/day/reviewer/`를 따랐다.

## 판정: PASS (차단 없음)

이번 변경은 **상태 표시뿐이다**: SPEC-001/003 `draft→stable` · 인덱스 Status 2칸 · coverage 2칸. 승인된 결과계약의 의미 변화는 **0**이다. main에 새로 올라온 planning 원문(v1.0.0)과 승인 SPEC 사이에 의미 차이가 있다. 하지만 모두 사용자가 직접 정한 결정 범위 안이라 **최신 직접 결정이 우선**이고, FAIL 사유가 아니다(아래 R-1).
**이 PASS는 stable main 도달 · baseline ready · 코드 구현 · 서버 통합 완료가 아니다.** 앱 · 서버 코드는 미착수다. main 머지 뒤 #235를 version 2 · 새 main SHA로 재결속해야 ready가 된다.

## 실행한 명령 · 결과

| 명령 | 결과 |
|---|---|
| `git fetch origin main` · `git rev-parse HEAD origin/main` | `b4cd1a00…` / `3f57c1af…` |
| `git diff --name-only HEAD origin/main` | 추가된 것은 `products/{day,charty,linky,procedure-hub}/00-baseline/planning/*.md`뿐(day 10개 · 2026-11-09 08:10–08:13 UTC). 로컬 수정 5파일과 교집합 없음 |
| `git status --short` · `git diff --stat` | 같은 5파일(4 M + SPEC-003 새로) · `116+/14-` · 다른 경로 · `30-work/` · WP 파일 없음 |
| `python3 scripts/lint-pipeline.py --strict` | exit 0 · `0 error, 263 warning` · **products/day 해당 0**(263건은 다른 제품 — 무관) |
| `git diff --check` | exit 0 · 출력 없음. 추적 안 된 SPEC-003 줄끝 공백 0 |
| (참고) `--release-gate` | DAY ERROR 2(SPEC-000/002 draft · coverage proposed). 이것은 버전 cut 전용 검사라 이번 판정에 쓰지 않는다 |

## 정합 확인

| 항목 | 결과 |
|---|---|
| frontmatter | `spec-001` · `spec-003` = `stable`(L6) · `spec-000` · `spec-002` = `draft` 그대로 |
| `20-spec.md` SPEC List L66-69 | 001 · 003 = stable · 000 · 002 = draft — frontmatter와 같음 |
| `30-work.md` Spec Coverage | 001 · 003 = `[Delivery #235](…/CENTURION_DAY/issues/235) \| proposed` · 000 · 002는 그대로. 형식은 다른 제품(`products/watch/30-work.md`의 `[Delivery #N](url)`) 선례와 같다. 구현 상태 `proposed` = 코드 미착수와 맞다(완료를 선언하지 않음) |
| `mobile-deployment.md` | 이번에 변경 없음(mtime 16:17 · 정책 리뷰 이전). §9-1 허용 목록 · 리다이렉트 금지 · 서버 분리 유지가 SPEC-001/003과 정합 |
| `delivery-request.json` | wp2 PASS(16:45) 뒤 변경 없음(mtime 16:43). 승인 digest 대상 그대로 |
| 계약 표지 유지(SPEC-003 610줄 = 정책 리뷰 때와 같음) | 재호출 = 웹 E22 조건 · 75초 · `/me` 뒤 원자 저장 · 「연결 대상 검증」(userinfo 등 거절 · allowlist) · 통역 = `board` view · `is_admin` · 푸시 = 기존 호출 대상 · 간호사 대리 수락 · 상담사 호출 = 향후 · OQ-A1/A9/A11 정책 표 그대로 · OQ-A15/17 닫은 것 · 인수조건 행 모두 4칸. SPEC-001: 60초 · 리다이렉트 금지 · `DAY_DEMO_API_BASE` fail-closed 그대로 |
| 범위 경계 | D-1만 backend 예외 · D-2/D-3 서버는 범위 밖 · 앱은 더블 · 방 이동/차트/seed는 옆 세션 · 새 문구 없음(문구 OQ = 글자 없이 코드) — 변경 없음 |

## 남은 위험 (차단 아님 · 코디/사용자 판단용)

- **R-1 planning 원문과의 의미 차이** — `planner-baseline-report.md` 표 그대로 확인했다.
  - 원문: 「데이(CC)-기획안-·-모바일」 정책 2 = 「모바일에서는 보기 · 호출 수락 · 관리실 통역 · 알림 받기만 · 마취/시작/종료/귀가 대기는 CC-06」. 「시술-현황」은 간호사가 수락 없이 시작하고, 전체 호출은 「그날 근무 원장」에게 간다. 통역은 charty가 맡고 기록을 저장한다.
  - 이 다섯 주제는 모두 **사용자가 2026-11-09에 직접 정한 결정**(프로토 기능을 DAY 기준으로 · 간호사 대리 수락 필수 · OQ-A15 · OQ-A17)과 #235 승인 범위 안이다 → 최신 직접 결정이 우선이고, 다시 미정으로 돌리지 않는다.
  - 다만 시간 순서를 적어 둔다. planning 업로드는 08:10–08:13 UTC(= 17:10–17:13 KST)이고, 승인 파일은 17:35(로컬)다. 사용자가 원문을 본 뒤 승인했는지는 이 레포에서 확인할 수 없다. planner 권장대로, PR 전에 「#235 1차 범위 유지 vs v1.0.0 정렬」을 사용자에게 한 줄 확인하면 뒤집힐 위험이 줄어든다. 정렬로 가면 SPEC 개정과 #235 `scope_delta` 재승인이 필요하다.
  - 「다시 알림」(수락 뒤 미시작 원장 재푸시)은 승인 SPEC에 없다. 없는 기능이고 충돌은 아니며, 완료로 선언된 곳도 없다.
- **R-2 stable SPEC이 draft SPEC에 기댄다** — SPEC-003은 업무 규칙 정본으로 DAY-SPEC-002(draft)를 참조한다. 옆 세션 PR #920이 SPEC-002 · SPEC-001(규칙 5 `is_demo` · 머리 개정)을 고친다. #920이 먼저 머지되든 나중에 머지되든 stable SPEC-001 줄 충돌을 정리해야 한다(이전 리포트와 같은 주의).
- **R-3 완료 오인 금지** — coverage `proposed` · D-1 미구현 · D-2/D-3 미구현/미배정 · 통합 검증 pending · Apple/키/env는 사용자 몫. 지금 문서는 이 상태를 정확히 표시한다.

## 다음

코디: commit · rebase(`3f57c1af` — 교집합 없음) · push · SPEC PR(→ main). 머지 뒤 #235를 같은 key · version 2 · 새 main SHA로 재결속(spec-baseline ready)한 다음 코드 착수.
