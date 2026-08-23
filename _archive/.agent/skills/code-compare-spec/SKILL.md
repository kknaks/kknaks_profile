---
name: code-compare-spec
description: spec 문서 하나를 실제 BE/FE 코드와 대조해 어긋남을 잡고 신 spec 템플릿 구조로 최신화할 때. 계약 표면(API·enum·state·validation·에러)은 코드 grounding 필수, 근거 없는 계약은 OQ로 박고 자율 삭제하지 않는다. 제품 무관, spec 한 개 단위. 트리거 "spec-NNN 코드 대조" / "spec 최신화".
allowed_tools: [Read, Grep, Glob, Edit, Write, Bash]
runs_scripts:
  - "../../scripts/product_doc_pipeline.py"
---

# code-compare-spec — 코드 대조 spec 최신화

## When to invoke

한 spec 문서(`products/<product>/20-spec/spec-NNN-*.md`)를 **실제 코드**(BE/FE)와 대조해 신 템플릿으로 최신화할 때. **제품 무관**, spec **한 개 단위** 호출. 결과: 코드와 어긋남 0 + `templates/product/20-spec/spec.md` 구조 + 새/변경 결정은 `templates/product/10-decision/decision.md` 양식으로 `10-decision/`에 기록.

> 템플릿·룰 내용을 이 스킬에 복사하지 않는다. 이 스킬은 *절차*만 들고, 구조·양식은 런타임에 아래 SSOT 파일을 **읽어서** 따른다.

이 레포 spec은 **외부 계약** 문서다 — UX/FE/BE/Data 계약과 enum·state·에러 케이스만 담는다. 라우트·컴포넌트 파일 경로·repository/service 구조 같은 **구현 디테일은 spec에 넣지 않고 `30-work/`로 넘긴다**(Work Handoff). 코드 대조의 목적은 spec의 *계약 표면*을 코드 실체에 맞추는 것이지, 구현을 spec으로 끌어오는 게 아니다.

## Inputs (호출 시 오케스트레이터가 넘김 — 경로 하드코딩 금지)

| 인자 | 의미 | 예 |
|---|---|---|
| `product` | 제품 slug. 경로의 `<product>`에 대입 | `open-kknaks` |
| `spec` | 대상 spec ID/파일 | `spec-001-task-model-and-lifecycle.md` |
| `be_root` | **백엔드 코드 루트 절대경로** | `/abs/.../open-kknaks` |
| `fe_root` | **프론트 코드 루트 절대경로** | `/abs/.../profile-front` |
| `extra_roots` | (선택) AI/MCP 등 추가 코드 루트 | `[/abs/.../agent]` |
| `resolved_oq` | (선택, pass 2+) 직전 pass에서 사용자가 해소한 OQ 결정 | — |

> 이 레포는 **문서 SoT만** 들고, 코드는 **별도 레포**다(예: 백 `profile-api`, 프론트 Vercel, `open-kknaks`, `mac-remote`). 코드 루트는 위 인자로만 받는다. 누락 시 진행하지 말고 오케스트레이터에 요청.

## 따라야 할 SSOT (런타임에 읽음 — 베끼지 말 것)

- 구조: `templates/product/20-spec/spec.md` — 섹션 구조와 각 섹션 지시(UX Contract `U-N`, User Scenario `S-N`, API 계약 table, Validation, Case Matrix, Flow, State Machine)를 그대로 따른다.
- 결정 양식: `templates/product/10-decision/decision.md`
- 파이프라인·라우팅·hub 규칙: `rules/product-doc-pipeline.md`
- 검증 스크립트: `.agent/scripts/product_doc_pipeline.py` (현재 **validate-only scaffold** — hub/log 자동 sync 안 함)

## Orchestration (실행 분담 — pass 반복 모델)

**서브에이전트(Agent 도구)**로 돈다. 서브에이전트는 실행 중 사용자에게 못 물으므로, **충돌마다 멈추지 않고 OQ에 박고 끝까지 진행** → 여러 pass로 수렴.

- **서브에이전트 (spec 1개 = 1개)**: Inputs 받아 Procedure 수행. 막히면 OQ로 박고 진행. 반환 `{ 갱신한 섹션, 새 OPEN-NNN, 정정 제안 }`.
- **오케스트레이터(메인 세션)**:
  - **Pass 1**: 대상 spec들에 서브에이전트 투입(각 호출에 코드 루트 주입), 1차 재작성 + OQ 누적. 사용자 안 물음.
  - **Pass 경계**: 누적 `OPEN-NNN` + `정정 제안`을 **묶음으로** 사용자에게 1회 제시 → 일괄 결정 → decision 생성/OQ 해소로 박음.
  - **Pass 2+**: 해소된 OQ(`resolved_oq`) 걸린 spec만 재투입. **Open Questions 빌 때까지** 반복.

단일 spec만 최신화하면 pass 반복 없이 Procedure 1회 + 끝에서 사용자에게 OQ 제시로 충분하다.

## Procedure (서브에이전트가 spec 1개에 수행)

1. **읽기** — 대상 spec(`products/<product>/20-spec/<spec>`) + 의존 SPEC + 관련 DEC. 그리고 위 §SSOT 파일들(구조·양식·룰)을 읽어 기준 확보.

2. **grounding 3출처 수집** — spec 본문은 셋 중 하나라도 근거 필요:
   - 기획/정책: `products/<product>/00-baseline/`, `context/`, `products/<product>/40-architecture/`
   - 코드: 인자 `be_root`/`fe_root`/`extra_roots`에서 endpoint·enum·테이블·컴포넌트를 grep. **경로는 인자값만**.
   - 결정: `products/<product>/10-decision/`

3. **코드 대조 맵** — spec의 **계약 표면**(API method/path/권한, enum, state transition, validation 규칙, Case Matrix 에러행) ↔ 코드 실체 1:1. 불일치 분기:
   - 코드 有 / spec 無 → spec 계약에 추가 (근거 명확하면 즉시, OQ 아님)
   - spec 有 / 코드 無 → 기획·정책에 있으면 `OPEN-NNN` 박제, 어디에도 없으면 OQ 아님 → 반환 `정정 제안`
   - 코드·정책·기획 다 살아있는데 **서로 어긋남** → `OPEN-NNN` 박제 후 진행. **멈추지 않음**. 결정은 pass 경계 일괄 (자율 결정·삭제 금지)

4. **재작성** — `templates/product/20-spec/spec.md` 구조대로 spec 본문 갱신.
   - **계약 표면만** 갱신한다. 모든 계약 항목은 step 2 코드/정책/결정에 grounding — **발명 금지**. 코드에 없는 endpoint·enum·상태를 지어내지 않는다.
   - grep으로 드러난 **구현 디테일**(파일 경로, service 구조 등)은 spec에 넣지 말고 `Work Handoff`에 적어 `30-work/`로 넘긴다.
   - spec frontmatter: `links` wikilink를 유효하게 유지하고 `updated_at`을 갱신한다(`tags` 패턴 보존).
   - 새/변경 결정은 `templates/product/10-decision/decision.md` 양식으로 `products/<product>/10-decision/decision-NNN-*.md`를 만든다. frontmatter `links`·`created_at/updated_at` 채우고, `10-decision/README.md` 결정 로그 표에 등록한다.

5. **hub + validate** — `20-spec/README.md` Spec 목록(Coverage) 갱신, `log.md` 1줄 추가, (필요시 `30-work/README.md`). `python3 .agent/scripts/product_doc_pipeline.py --strict`로 검증한다. **스크립트는 현재 validate-only scaffold라 hub/log를 자동으로 채우지 않는다 — 위 hub들은 직접 갱신**한 뒤 validate를 통과시킨다.

## Checklist

- [ ] `templates/product/20-spec/spec.md` 구조 준수 (섹션 누락 시 "해당 없음"+근거)
- [ ] UX Contract `U-N` · User Scenario `S-N` · Case Matrix가 spec 템플릿 양식 준수
- [ ] 계약 표면(API method/path/권한 · enum · state transition · validation · 에러행) 전부 실제 코드 grounding (발명 0건)
- [ ] grep으로 드러난 구현 디테일은 spec이 아니라 `Work Handoff` → `30-work/`
- [ ] grounding 미충족: 근거 있으면 OQ / 어디에도 없으면 정정 제안 (자율 삭제 X)
- [ ] spec frontmatter: `links` wikilink 유효 · `updated_at` 갱신 · `tags` 패턴 보존
- [ ] 결정은 `decision.md` 양식 + `10-decision/README.md` 등록
- [ ] hub(`20-spec/README.md`) 갱신 + `product_doc_pipeline.py --strict` 통과

## Failure / Rollback

- **코드 루트 인자 누락** → 진행 X, 오케스트레이터에 요청.
- **코드↔정책 모순** → 자율 결정 X. OQ 박제 후 진행, pass 경계 일괄 결정.
- **단일 spec 범위 초과** → 멈추고 반환에 명시, 별도 호출로 분리.
- **`--strict` 실패** → frontmatter `links` wikilink·`tags` 패턴·required README부터 점검. 본문/hub 행 임의 삭제 금지.

## Related

- 구조/양식: `templates/product/20-spec/spec.md`, `templates/product/10-decision/decision.md`
- 규칙: `rules/product-doc-pipeline.md`
- 검증: `.agent/scripts/product_doc_pipeline.py`
