
# 재개 노트 — day-data-architecture (day)

**지금**: backend 워커 — Delivery #224 뼈대 구현 중(CENTURION_DAY 워크트리 `day-data-architecture` · 브랜치 `kknaksss/day-data-architecture` · base `v2-dev`). PR #909 머지는 사용자가 구현 뒤에 한다 — 머지 요청하지 말 것. Delivery #224~#227(CENTURION_DAY) 생성 — 전부 `delivery-plan:review`(사용자 계약 승인 대기) · `spec-baseline:pending`(PR #909 머지 대기). PR #909 보정 커밋 `60fae27b`
**다음**: SPEC 먼저 닫는다(사용자 2026-11-05 — 「스펙도 없는데 wp를 만든거야?」): SPEC-001 로그인 · 세션(PR #909 에 같이) → 검수 → #909 머지 · SPEC 확정 → Delivery #224~#226 재결속 · 승인, #227 은 SPEC-001 기준으로 계약 다시 → backend 발주

세팅: `scripts/new-work.sh day day-data-architecture` · 설정 SSOT `config/projects/day.json`
코디handle: `term_70b6f193-86a2-4c1d-8965-4e2220cef9b3`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` (branch `kknaksss/day-data-architecture-spec`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] mediness PR #909 — 사용자 리뷰 · 머지
- [ ] 워커 터미널 2개(planner · reviewer) 정리 — 머지 뒤
- [!] `reference/2026-11-03-cc-day/screen/시술현황_프로토타입.html`(3MB · 사용자 추가) — public 레포라 내용 확인 전 미커밋
- [!] planner 미결 13항(planner-report.md) — 사용자 판단 필요분 있음(product_option_id FK · ESC 기본값 · version · context/products.md 등)
- [!] 원천 문서가 `reference/2026-11-03-cc-day/erd/` 로 옮겨짐(사용자 · 내용 동일) + `screen/` 추가 — 프로필 미커밋
- [ ] PR — mediness `main`(spec 레포) · 원천 문서는 profile `kknaksss/day`(이미 push)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-05 | **구현 먼저 · 머지는 나중**(사용자: 「왜 자꾸 머지하라는 거야 일단 구현하고 머지할 건데」) — #224 계약 승인으로 보고 backend 발주 | 사용자 |
| 2026-11-05 | SPEC-001 로그인 · 세션 OQ 11개 전부 권장대로(경로 `/api/auth/*` · 웹 쿠키 `day_session` + 앱 Bearer · 세션 = KOS 토큰 만료 · 1차는 병원 직원만 · 2단계 인증 계정은 막고 안내(명동점 90개 중 0개) 등) | 사용자 |
| 2026-11-05 | ~~Delivery 를 SPEC 머지 전에 연다~~ → **SPEC 먼저 닫고 Delivery**. #227 은 대상 SPEC 없이 열린 것(코디 실수) — SPEC-001 뒤 계약 다시 | 사용자 지적 |
| 2026-11-05 | 백엔드 작업 계획은 mediness 새 규칙 — GitHub Delivery Issue(start-delivery). WP 파일 안 씀. 디자인 변동 가능 → 백엔드만, 로그인까지 4개 | 사용자 |
| 2026-11-05 | cc-prototype #20 — KOS 내부 API 브라우저 헤더 필수 → DAY 연동 · 로그인에 반영 | cc-prototype `77173cf` |
| 2026-11-03 | 테이블 설계 01~07 확정 — 원천 `reference/2026-11-03-cc-day/` | 사용자 칸 단위 검토(아티팩트 승인/반려) |
| 2026-11-03 | mediness 제품 slug `day` · ID prefix `DAY` | 코디(카탈로그 slug `day` · 스캐폴드 기본값) |
| 2026-11-03 | 검수 FAIL 대응: 원천 묶은 행 42개 분리(deleted_at NULL 허용) · `consultation_procedure` · `visit_occupied_resource_doctor` 칸 표 추가 · ESC-001 값 그대로 | 사용자 「둘 다 그대로 가고 재발주」 |
| 2026-11-03 | 컬럼 수준 계약은 SPEC-000(데이터 모델), architecture 는 관계 · invariant 만 | mediness `rules/document-pipeline.md` · selly SPEC-000 선례 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_256e3ec1a806` | `ctx_e497e1180940` | `day-data-architecture-spec-brief.md` | 완료(터미널 유지 — 수정 재발주용) |
| reviewer_doc | `term_441c2cdb-68e6-4463-b694-d8d6adfc7210` | `task_0fbf4462273f` | `ctx_6b32d164d0aa` | `day-data-architecture-review-doc-brief.md` | 1판 FAIL(터미널 유지) |
| backend #224 | `term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f` | `task_b55365041983` | `ctx_54b11e55fc04` | `day-data-architecture-be-brief.md` | 발주 · 진행 |
| planner SPEC-001 결정 반영 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_23966603a026` | `ctx_f348cbceb7b3` | `planner-spec001-fix-instructions.md` | 발주 · 진행 |
| planner SPEC-001 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_a536db100de3` | `ctx_34532b18e680` | `planner-spec001-instructions.md` | 완료(OQ 11) |
| planner delivery | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_226ed1ca2070` | `ctx_65b9ce7dbcbe` | `planner-delivery-instructions.md` | 완료(human gate) · request JSON → `delivery/` |
| planner arch | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_78d14ef22adb` | `ctx_51d128cdd28e` | `planner-arch-instructions.md` | 완료 · 검수 WARN → 해소 |
| planner 수정 1판 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_18d832312263` | `ctx_91b93dee59be` | `planner-fix-1-instructions.md` | 발주 · 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/909 (`f92a8acb` · `974caeac` · `e71e3849` · `60fae27b` · SPEC-001 커밋)
- Delivery: CENTURION_DAY #224 뼈대(L2) · #225 데이터 모델(L3) · #226 KOS 연동(L3) · #227 로그인(L3) — plan_digest 는 `planner-delivery-report.md`
- 코드 레포: CENTURION_DAY v2-dev `8e4fb4b5` — AGENTS.md 「아직 정하지 않은 것」 로그인 · 배포 제거(사용자 2026-11-05)
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-05` 40-architecture 추가(planner) → 검수 WARN(정본 낡음) → AGENTS.md 갱신 · PR #909 커밋
- `2026-11-03` 수정 2판 → 재검수 PASS → mediness PR #909
- `2026-11-03` 검수 FAIL → 원천 수정 · planner 수정 1판 발주
- `2026-11-03` planner 완료 → reviewer_doc 발주
- `2026-11-03` 사용자 승인 → planner 발주(run `run_86b1e890ecc2`)
- `2026-11-03` new-work.sh · `products/day` 스캐폴드(`scaffold-product.sh day DAY DAY`) · planner 브리프 작성

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
