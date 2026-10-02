# [reviewer_code] WP-131 코드 검수 — surface 축 (BE 17파일 + FE 6파일)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **너는 read-only 다.** 코드를 고치지 말고 **테스트도 돌리지 마라.** 산출물은 **리뷰 리포트 파일 1개뿐**이다.
⚠ **BE·FE 워커는 끝났다** — 충돌 없다. 변경은 **워킹트리에 미커밋**이다.
⚠ **너는 이 작업의 맥락이 하나도 없다.** §1 을 전부 읽고 시작해라.

## 1. SSOT — 먼저 읽을 것

**계약은 다른 레포에 있다** (spec PR #762, `dev` 에는 없다). 절대경로로 읽어라:

1. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/30-work/work-131-deploy-surface-axis.md`
   ← **빌드 계획. Phase 1~8 · SPEC AC 16건 대응표 · Pre-deploy · Rollback.**
2. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md`
   ← **외부 계약.** §3 API·§Validation·**§케이스 매트릭스(에러 문구·코드의 단일 SoT)**·§4·§5 AC.
3. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/21-html/Product Management.html`
   ← **시안 = FE 의 정본.** 모달 확정 모양.
4. `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/flaky-baseline-evidence.md`
   ← ⚠ **기존 실패 12건 판정이 끝나 있다. 재조사하지 마라.** 인용만 해라.

**기대는 개념**:

- `…/para/areas/concept/db/unique-key.md` — 앱 정규화와 DB 제약이 **같은 값**을 봐야 유일성이 성립한다(trim 저장).
- `…/para/areas/concept/db/functional-dependency.md` — 부분 종속이 남았는지.
- (경로 앞부분은 `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가`)

## 2. 배경 — 무엇을 검수하나

배포 레지스트리의 식별 키를 `(product_slug, environment)` → **3축**으로 넓혔다. BE(Phase 1~5 + 8) · FE(Phase 6~7) 가 끝났고 **코디가 이미 관문 수치를 직접 돌려 확인**했다:

| 대상 | 코디 실측 |
|---|---|
| `tests/migrations/test_0139_deployment_surface_key.py` | 8 passed |
| `tests/api/test_gm_command.py` + `tests/services/test_deployment.py` | 57 passed |
| `tests/api/test_admin_deployments.py` | 36 passed / **12 failed(기존·무관, 판정 파일 있음)** |
| `tests/services/test_dashboard_split.py` | 30 passed |
| `front` `npx tsc --noEmit` | exit 0 |

**네 일은 수치 재확인이 아니라 「수치가 못 보는 것」을 보는 것이다.**

## 3. 계약 (이 기준으로 판정해라 — 어긋나면 FAIL)

- **3축 유니크** `(product_slug, environment, surface_key)`. 행 1개 = 표면 1개.
- **`surface_key`** — 자유 입력 · **trim 한 값을 저장**(검증에만 쓰면 `기본` 과 `기본␣` 이 둘 다 통과해 유니크가 샌다) · **NOT NULL 이 계약** · `String(50)` · **`server_default` 없음** · PATCH 개명 가능 · `product_slug`·`environment` 불변.
- **`기본` 은 sentinel 도 프리필도 아니다** — 백필 값 하나로만. 서버가 이 값으로 **분기하지 않는다**.
- **`/gm` surface 표기 = 그룹 행 수 ≥ 2 일 때만**(값 판정 아님). **단일 surface 제품 출력이 확장 전과 문자 단위로 동일**해야 한다.
- **migration 5단계 순서**(컬럼 → 백필 → NOT NULL → 구 유니크 DROP → 확장 유니크 ADD) + **down 에 중복 그룹 가드**.
- **400 2종**(빈 값/공백만 · 50자 초과 + `detail.max_length`) · **409 는 3축 전부 같을 때만**. **문구·코드는 SPEC §케이스 매트릭스 소유 — 지어낸 문구가 있으면 FAIL.**
- **FE** — 환경 소진 폐지 · 신규 카드 surface **빈 값 + placeholder**(`기본` 프리필 금지) · 시연계정 1건 이상 행 삭제는 **확인 단계**(0건은 확인 없이) · 표시 정렬 `prod → stg → dev → demo` × surface 오름차순, **select 옵션 순서와 별개 배열**.
- **대시보드(사용자 결정 2026-09-22)** — 카드는 환경당 1칸 유지, `기본` 우선 → 없으면 surface 오름차순. **「대표 surface」 개념 신설 금지.**

**불변** — 권한 게이트·`product_assignment` 판정 / 환경 enum 4종 / `/gm` 인자 2토큰 / `demo_accounts` JSONB shape / `ProductLinks` shape / 민감값 두 축.

## 4. 검수 축 — 축마다 PASS/WARN/FAIL + 근거(파일:줄)

`git diff origin/dev...HEAD` 와 **untracked** 로 범위를 먼저 산정해라(커밋이 없으니 `git status` + `git diff` 로 본다).

1. **계약 반영** — §3 전 항목이 코드에 있나. 문서엔 있는데 코드에 없는 것.
2. **allowed_paths** — BE 가 `back/` 만, FE 가 `front/` 만 건드렸나. **같은 워크트리를 공유했으므로 서로의 영역 침범이 제일 위험하다.**
3. **`기본` 이 sentinel 로 새지 않았나** — **전수 grep.** 이 값으로 분기하는 자리가 한 곳이라도 있으면 계약 위반이다. 대시보드 `_link_priority` 의 정렬 키 사용은 **허용**(표시 우선순위) — 그 구분이 코드에서 읽히는지 보라.
4. **trim 값이 실제로 저장되는가** — 검증 경로와 저장 경로가 **같은 값**을 쓰는지 코드로 따라가라. 갈리면 유니크가 샌다.
5. **migration** — 5단계 순서 · `server_default` 부재 · **down 가드가 실제로 막는지** 코드로 확인. `down_revision` 이 실제 head 를 가리키는지(`0138_task_body_refs`).
6. **`/gm` 회귀 0 이 테스트로 고정됐나** — 「문자 단위 동일」이 **하드코딩 기대문자열**로 박혔는지. 느슨하면 회귀를 못 잡는다.
7. **FE ↔ 시안 정합** — 시안의 `envBlockHTML`·`addSurfaceBlock`·`commitDeploys`·`ENV_DISPLAY_ORDER` **동작**과 실제 TSX 가 맞나. ⚠ **삭제 확인이 `useConfirm()` 인 것은 의도된 시안 이탈이다**(WKWebView 는 `confirm()` 이 항상 false — `components/ui/confirm-dialog.tsx` 머리 주석). 이걸 흠으로 잡지 마라.
8. **에러 문구·코드가 SPEC §케이스 매트릭스와 글자까지 같은가.**
9. **테스트가 무엇을 고정하나** — 통과 숫자가 아니라 **무엇을 막는 테스트인지**. 구현을 그대로 베낀 테스트(같이 틀리면 같이 통과)가 있으면 지적해라.
10. **사용자가 실물에서 만날 자리** — 계약은 맞는데 **운영자 눈에 이상해 보일 자리**. 테스트가 못 보는 층이고 이게 2루프 비용이 된다. **FAIL 이 아니라 「관찰」로 분리**해 적어라. (알려진 것: `prod` 칩 6회 반복 · 백필 `기본` 첫인상 안내 부재 · 빈 surface 를 저장 눌러야 앎. **이미 아는 것 말고 새로 보이는 것**을 찾아라.)

**리포트 경로(반드시)**: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/review-code-report.md`
**scratchpad 금지 — 네 터미널이 죽으면 같이 죽는다.** (이 작업에서 워커 터미널이 실제로 두 번 죽었다.)

형식: 종합 판정 → 축별 판정표 → 지적(파일:줄 + 근거 계약/규칙 + 제안) → 관찰(축 10) → 무관.

## 5. allowed_paths

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 위 리뷰 리포트 파일 1개뿐)`

## 6. 하지 말 것

- **코드를 고치지 마라. 테스트를 돌리지 마라.** 판정과 근거만.
- **12건 기존 실패를 재조사하지 마라** — 판정 파일이 있다.
- **확정된 계약·사용자 결정에 대안을 제시하지 마라.** 반영 여부만 판정한다.
- **워커 보고를 근거로 원본 확인을 건너뛰지 마라.**
- **로컬 스택·포트·프로세스 금지.**
- 커밋·push·PR 금지.

## 7. 검증

리뷰는 read-only — **코드를 고치지 않고 테스트도 돌리지 않는다.** `git diff` + untracked 로 범위를 산정하고, 판정(PASS/WARN/FAIL)과 위반 목록(**파일:줄 + 근거 규칙**)을 리포트에 남긴다.

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값은 브리프 작성 시점 것이고 **이 세션에서 세 번 바뀌었다.** preamble 과 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --from term_031286fc-0499-4bcf-988f-e4d787c5a1fb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer_code 완료: <한 줄>" \
  --body "판정 / 지적 요약 / 근거 / 미결·주의점"

orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 \
  --text "[worker_done] reviewer_code 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --text "[질문] reviewer_code: <질문>" --enter`
