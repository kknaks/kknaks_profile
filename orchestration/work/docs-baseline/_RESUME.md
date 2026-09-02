
# 재개 노트 — docs-baseline (ontology-demo)

**지금**: SPEC-001·002·003·005 발주(task_ca52bf6b772c), docs 워커 작성 중. PR #32 병합 대기.
**다음**: 완료 보고 오면 검증(특히 「제안—리뷰 필요」 목록) → 사용자 리뷰 → spec 커밋·PR. SPEC-004 는 디자인 귀환 후.
**확정(2026-09-02 문답)**: 마스킹 표기 = 김○○ / 010-****-1234 / 1990-**-** · 접속 게이트 = env 난수 비번 1개(값은 사용자가 배포 시 주입), 내부망이라 추가 가드 없음.

세팅: `scripts/new-work.sh ontology-demo docs-baseline` · 설정 SSOT `config/projects/ontology-demo.json`
코디handle: `term_45e793be-0adb-44c7-9d9a-eb35c4f48320`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline` (branch `kknaksss/docs-baseline`, base `origin/ontology-demo` → PR `ontology-demo`)

## 1. 지금

- [~] docs 워커 — DEC-001~005 작성 중 (+ BASE-001 raw→accepted 동기, 브리프 `docs-decisions-docs-brief.md`)
- [ ] 완료 시: diff 검증 → 사용자 리뷰 → baseline+decision 문서 PR 1건(`kknaksss/docs-baseline` → `ontology-demo`)
- [ ] 워커가 「개념 필요」 보고 시 코디가 `para/areas/concept/` 노트 생성 후 `up:` 연결 재지시
- [!] SPEC-004(화면)는 디자인 핸드오프 귀환 대기 (`reference/ontology_demo/design/`). spec 분할 확정도 미결

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-02 | ~~단일 레포형 문서도 워커 발주 (runbook 전면 개정)~~ → 같은 날 축소: **runbook 은 원복**(기본 = 코디 직접), 문서 워커 발주는 **ontology-demo 한정 예외**로 config notes 에만. kknaks-dev 기존 방식이 조용히 뒤집히는 걸 사용자가 잡음 | 사용자 지시 |
| 2026-09-02 | 문서 위치 = 신규 제품 `para/projects/summer-star/ontology-demo/` (summary_dest 도 이동) | 사용자 선택 |
| 2026-09-02 | 프론트 = 정식 3페이지(채팅·모니터링·데이터), `app/front/` 통합. 디자인은 별도 세션(핸드오프 `reference/ontology_demo/DESIGN_HANDOFF.md`) | 사용자 지시 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| docs | `term_b25f6462-b5e3-41fe-aa61-ad32e81ba66a` | `task_ca52bf6b772c` | `ctx_371d84bbfab6` | `docs-specs-docs-brief.md` | 진행 |
| docs | (같음) | `task_65fb3666d260` | `ctx_3e15c3c45ee1` | `docs-dec002-up-fix-brief.md` | 완료·PR#32 포함 |
| docs | (같음) | `task_713063497cfc` | `ctx_7ed01caa356c` | `docs-decisions-docs-brief.md` | 완료·검증통과·사용자 승인 |
| docs | (같음) | `task_87f39fa33d40` | `ctx_fccf1f154451` | `docs-baseline-docs-brief.md` | 완료·검증통과·사용자 승인 |

## 4. 산출물

- 커밋: `bce52d7` — runbook 개정 + docs 워커 config/role + 제품 문서 스캐폴딩 (ontology-demo 푸시됨)
- 커밋: `43dd669` — pii-masking 개념 신설 + area 맵 백필 (ontology-demo 푸시됨)
- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/32 (`kknaksss/docs-baseline` → `ontology-demo`, 커밋 0400ddb)

## 5. 이력 (최신이 위)

- `2026-09-02` runbook 개정(문서도 워커 발주) → docs 워커 신설 → 스캐폴딩 커밋·푸시(bce52d7) → BASE-001 발주(task_87f39fa33d40)
