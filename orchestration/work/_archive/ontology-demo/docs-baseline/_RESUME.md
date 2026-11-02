
# 재개 노트 — docs-baseline (ontology-demo)

**지금**: spec 5건 커밋(2523b40, **푸시 보류** — 사용자 지시: PR 은 WP 까지 묶어 한 번에). WORK-001~010 발주(task_60060f3b4b0a), docs 워커 작성 중.
**다음**: WP 완료 → 검증 → 사용자 WP 리뷰(승인 게이트) → 커밋·푸시(PR #32 갱신) → fe 워커 config/role 신설 → 코드 발주(WORK-001 부터).
**확정(2026-09-02 문답)**: 마스킹 표기 김○○/010-****-1234/1990-**-** · 게이트 env 비번 1개 · 채팅 미니그래프 제거(칩+?edge= 점프) · Pretendard next/font · 정량추정 문구 제거 · 월 집계 = gold_kpi_monthly View · lag 표기 "<정수>d" 통일.
**디자인 조정 대기 20건**: SPEC-004 §7.2 표 + `reference/ontology_demo/DESIGN_FEEDBACK.md` (디자인 세션 재방문 시 입력).

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
| design-fix | `term_0b5d9a19-47c2-470a-bca5-529f70b859ef` | `task_c744fc9c4402` | `ctx_2658e775a421` | `design-fix-brief.md` | 진행 — 디자인 패키지 조정 20건·신규 3건·재키잉 (design/ 폴더 한정 쓰기). 완료 후: 코디 검증 → docs 소수정(SPEC-001 좌표 '미배정' 채움·§7.2 정리·SPEC-004 ready) → WORK-004 발주 가능 |
| docs | `term_b25f6462…` | `task_bb37976fda08` | `ctx_2b0bb31d2f7c` | `docs-spec-node-fix-brief.md` | 완료·검증통과·커밋(5b890cf) — naver=intervention·gu=organic 정본 확인 |
| research | `term_0b5d9a19-47c2-470a-bca5-529f70b859ef` | `task_ac360b43ab2d` | `ctx_120f994d4466` | `research-codex-mcp-brief.md` | 완료 — `research-codex-mcp-report.md` 506줄. WORK-002·003 브리프에 §5(적용 체크리스트)·함정 2건(approval_mode·features.apps=false)·§5.6(착수 전 5건) 반영할 것 |
| docs | `term_b25f6462-b5e3-41fe-aa61-ad32e81ba66a` | `task_e4d9b6098dd1` | `ctx_7f38b61be87e` | `docs-spec004-and-revisions-brief.md` | 완료 — SPEC-004 draft + 4건 ready, WP 5건까지 완료·푸시(f40bfcf) |
| reviewer | `term_0b5d9a19-47c2-470a-bca5-529f70b859ef` | `task_0fc1c83a9e8f` | `ctx_86bdf5fc0f1d` | `review-design-feasibility-brief.md` | 완료 — 리포트 `review-design-feasibility-report.md`, 전 페이지 FEASIBLE-WITH-CHANGES |
| docs | (같음) | `task_ca52bf6b772c` | `ctx_371d84bbfab6` | `docs-specs-docs-brief.md` | 완료·검증통과 — 제안 21건 전건 사용자 확정(4건 문답: 그래프 패널 제거·Pretendard·정량추정 제거·월 View) |
| docs | (같음) | `task_65fb3666d260` | `ctx_3e15c3c45ee1` | `docs-dec002-up-fix-brief.md` | 완료·PR#32 포함 |
| docs | (같음) | `task_713063497cfc` | `ctx_7ed01caa356c` | `docs-decisions-docs-brief.md` | 완료·검증통과·사용자 승인 |
| docs | (같음) | `task_87f39fa33d40` | `ctx_fccf1f154451` | `docs-baseline-docs-brief.md` | 완료·검증통과·사용자 승인 |

## 4. 산출물

- 커밋: `bce52d7` — runbook 개정 + docs 워커 config/role + 제품 문서 스캐폴딩 (ontology-demo 푸시됨)
- 커밋: `43dd669` — pii-masking 개념 신설 + area 맵 백필 (ontology-demo 푸시됨)
- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/32 (`kknaksss/docs-baseline` → `ontology-demo`, 커밋 0400ddb)

## 5. 이력 (최신이 위)

- `2026-09-02` runbook 개정(문서도 워커 발주) → docs 워커 신설 → 스캐폴딩 커밋·푸시(bce52d7) → BASE-001 발주(task_87f39fa33d40)
