# 리뷰 리포트 — deploy-surface-multi / code(BE+FE 통합) · WP-131 (2026-09-22)

리뷰어: `@mediness-reviewer` (read-only) · 워크트리 `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`
기준: SPEC-051(2026-09-22 개정) · WP-131 · 시안 `21-html/Product Management.html` · 역할문서 `roles/mediness/reviewer/rules.md`

---

## 종합 판정: **PASS** — 계약 위반 0 · FAIL 0 · WARN 4 · 관찰 5

§3 계약 전 항목이 코드에 반영돼 있다. `기본` 이 sentinel 로 새는 자리 0건, trim 값이 실제 저장 경로에 쓰이는 것 확인, migration 5단계·`server_default` 부재·down 가드가 코드로 확인됨, `/gm` 회귀 0 이 **하드코딩 기대문자열**로 고정됨. WARN 4건은 전부 비블로킹이며 **코디네이터 판단 항목**이다(수정 없이 PR 가능).

---

## 검수 범위

- **커밋 없음** — `HEAD == origin/dev == e64b97cf`. 변경은 전량 워킹트리 미커밋이므로 범위 산정은 `git status` + `git diff` + untracked 로 했다.
- 수정 20파일 + untracked 2파일 = **22파일** (BE 16 / FE 6), +1482 / −153.
  - BE 앱 9: `core/errors.py` · `models/product_deployment.py` · `repositories/product_deployment_repo.py` · `routers/deployments.py` · `schemas/deployment.py` · `seeds/deployments.py` · `services/deployment.py` · `services/gm_command.py` · `services/dashboard/db_source.py`
  - BE 테스트 5 + untracked 2: `tests/api/test_admin_deployments.py` · `tests/api/test_gm_command.py` · `tests/schema/test_product_deployment_schema.py` · `tests/services/test_dashboard_split.py` · `tests/services/test_deployment.py` · **(신규)** `alembic/versions/0139_deployment_surface_key.py` · **(신규)** `tests/migrations/test_0139_deployment_surface_key.py`
  - FE 6: `components/admin/products/{DeployInfoModal,EnvBlockCard,EnvBlockView,useDeployInfo}` · `components/pipeline/DeployInfoSection.tsx` · `lib/admin-deployments.ts`
- **실행한 검사**: `git status/diff` · 전수 grep(`기본` / `DEFAULT_SURFACE_KEY` / `surface_key` / `usedEnvs` / `환경당 1개` / `window.confirm`) · `ProductDeployment(...)` 생성자 전수 AST 스캔(surface_key 누락 탐지) · alembic head 체인 확인 · 시안 HTML ↔ TSX 대조 · `components/ui/confirm-dialog.tsx` API 대조.
- **안 한 것(계약)**: 코드 수정 0, 테스트 실행 0, 스택/포트 기동 0. 관문 수치는 코디 실측을 인용한다.
- 기존 실패 12건(`TestProductAssigneeAccess`)은 `flaky-baseline-evidence.md` 판정을 **인용만** 한다 — 재조사 안 함. 이번 diff 가 `policies/deployment.py`·게이트를 **한 줄도 건드리지 않은 것**은 diff 로 확인했다(두 파일 모두 변경 목록에 없음).

---

## 축별 판정표

| # | 축 | 판정 | 한 줄 근거 |
|---|---|---|---|
| 1 | 계약 반영(§3 전 항목) | **PASS** | 3축 유니크·trim 저장·NOT NULL·no server_default·String(50)·PATCH 개명·불변 축·400 2종·409 3축·표기 행 수 판정·정렬 2축 분리·대시보드 1칸 유지 — 전부 코드에 있다 |
| 2 | allowed_paths | **PASS(조건부)** | 변경 전량이 `back/` ∪ `front/`. **커밋이 없어 워커별 귀속은 git 으로 증명 불가** — 아래 참고 |
| 3 | `기본` sentinel 누수 | **PASS** | 전수 grep 결과 값 분기 0건. 대시보드 `_link_priority` 만 표시 우선순위로 사용(허용), 그 구분이 코드 주석·테스트로 읽힌다 |
| 4 | trim 저장 | **PASS** | 검증 경로와 저장 경로가 **같은 변수**를 쓴다(`services/deployment.py:201,207` → `surface_key=surface`) |
| 5 | migration | **PASS** | 5단계 순서·`server_default` 부재·down 가드·`down_revision="0138_task_body_refs"`(실제 head, 단일 head) |
| 6 | `/gm` 회귀 0 고정 | **PASS** | `test_gm_command.py::test_output_is_byte_identical_to_the_pre_surface_shape` 가 기대문자열을 **하드코딩** |
| 7 | FE ↔ 시안 정합 | **PASS** | `envBlockHTML`·`addSurfaceBlock`·`commitDeploys`·`ENVS`↔`ENV_DISPLAY_ORDER` 동작 일치. `useConfirm()` 이탈은 의도된 것(흠 아님) |
| 8 | 에러 문구·코드 | **PASS** | 서버 문구 3종이 §케이스 매트릭스와 **글자까지 동일**. 지어낸 서버 문구 0 |
| 9 | 테스트가 무엇을 고정하나 | **WARN** | BE 테스트는 구현 베끼기가 아니라 **반례**를 심어 놓았다(우수). 다만 FE 자동 테스트 0 + 상한값 이중 정의 미고정 |
| 10 | 사용자가 실물에서 만날 자리 | **관찰 5건** | FAIL 아님. 아래 §관찰 |

---

## 지적 (FAIL)

**없음.** §3 계약 중 코드에 반영되지 않은 항목을 찾지 못했다.

계약 항목별 확인 위치(전수):

| 계약(§3) | 코드 |
|---|---|
| 3축 유니크 | `models/product_deployment.py:111-117`(문서용) · `alembic/versions/0139_deployment_surface_key.py:82-85`(실제 제약) |
| trim **저장** | `services/deployment.py:54-73`(정규화) → `:201`·`:207`·`:214`(같은 값 저장) · 테스트 `test_deployment.py::test_trimmed_value_is_what_gets_stored_so_the_unique_cannot_leak` + `test_admin_deployments.py::test_the_stored_value_is_trimmed_and_the_unique_holds`(DB 실값 SELECT) |
| NOT NULL 계약 | `models/product_deployment.py:93` · migration `:80` · 테스트 `test_product_deployment_schema.py::test_surface_key_is_not_null_without_default` |
| `server_default` 없음 | migration 에 `server_default` 인자 부재(`:69`) · 테스트가 `information_schema.column_default IS NULL` 로 단언(`test_0139…:118-123`) |
| `String(50)` | `models:93`(`SURFACE_KEY_MAX_LENGTH`) · migration `_MAX_LENGTH=50`(`:64`) · `character_maximum_length == 50` 단언 |
| PATCH 개명 / slug·env 불변 | `schemas/deployment.py` `DeploymentUpdateRequest.surface_key` 신설 · `services/deployment.py:250-262` · 테스트 `test_product_slug_and_environment_stay_immutable` |
| `기본` 비-sentinel | grep 전수 — 분기 0. `gm_command.py:56-58` 이 「값을 보지 않는 이유」를 주석으로 남겼고, 테스트 `test_single_row_group_hides_even_a_non_default_name` 이 **값 판정이 아님을 반례로 증명** |
| `/gm` 표기 = 행 수 ≥ 2 | `gm_command.py:101-112`(`group_size`) · 테스트 4건(그룹별 공존·전이·2카드·미표기) |
| migration 5단계 | `0139…:67-86` 순서 그대로 |
| down 중복 가드 | `0139…:90-91` + `_guard_no_multi_surface_groups()`(`:99-127`) — 그룹명·건수를 메시지에 싣는다. 테스트 `test_downgrade_stops_explicitly_once_a_group_has_two_surfaces` 가 **「반쯤 되돌아간 상태를 남기지 않는지」까지** 단언 |
| 400 2종 | `services/deployment.py:63-72` — `surface_key 는 비어 있을 수 없습니다` / `surface_key 가 너무 깁니다` + `detail.max_length` |
| 409 3축 | `services/deployment.py:76-86` `_duplicate()` — `이미 등재된 제품·환경·surface 입니다: {slug}/{env}/{surface}` (§케이스 매트릭스와 글자 일치) · 사전검사 + `IntegrityError` **두 겹** (`:207` / `:224` / `:260` / `:281`) |
| seed 스킵 키 3축 | `seeds/deployments.py:118-142` · 테스트 `test_reseed_adds_nothing_even_next_to_an_operator_made_surface` |
| FE 환경 소진 폐지 | `EnvBlockCard.tsx:117-142`(`usedEnvs` prop 자체 제거) · grep 잔재 0 |
| FE 신규 카드 빈 값 + placeholder | `useDeployInfo.ts:59-71`(`emptyBlock` → `surfaceKey: ""`) · `EnvBlockCard.tsx` placeholder `기본 · 고객 홈페이지 · 운영자 어드민 …` |
| FE 삭제 확인(계정 ≥ 1) | `EnvBlockCard.tsx:79-93` · 0건은 확인 없이(`if (n > 0)`) |
| FE 표시 정렬 별개 배열 | `lib/admin-deployments.ts:25-31`(`DEPLOY_ENVIRONMENTS` = select) vs `:37-43`(`DEPLOY_ENV_DISPLAY_ORDER` = 표시) — 시안 `ENVS`↔`ENV_DISPLAY_ORDER` 분리와 동형 |
| 대시보드 환경당 1칸 + 결정성 | `dashboard/db_source.py:60-77`(`_link_priority`) · `:160-166`(바깥·안쪽 모두 `setdefault`) · 「대표 surface」 컬럼·플래그·API 필드 0 |
| 불변 축 | 게이트(`policies/deployment.py`·`routers/deployments.py` 권한부) 무변경 · 환경 enum 4종 무변경 · `/gm` 인자 파싱 무변경(테스트로 고정) · `demo_accounts` JSONB shape 무변경 · `ProductLinks` shape 무변경 · 민감값 두 축 무변경 |

---

## 경미 (WARN) — 비블로킹, 코디네이터 판단

### W-1. FE(Phase 6·7)에 자동 테스트가 0건이다 — SPEC AC 4·5·6·14 를 지키는 실행 가능한 장치가 없다
- 근거: `front/vitest.config.ts` 가 있고 `front/__tests__/` 에 WP 단위 컴포넌트 테스트가 다수 있다(가장 최근 커밋 `e64b97cf` 도 `wp130-composer-multi-attach.test.tsx` 를 동반). **이번 FE 변경분에 대응하는 `__tests__` 파일이 없다** — `grep -rln "Deployment|useDeployInfo" front/__tests__` = 0건.
- 다만 **WP-131 §Phase 7 검증이 「P7(수동)」으로 계획했다** — 계획 위반은 아니다. 즉 이것은 "계획대로인데 리포 관례와 어긋난다"는 자리다.
- 실질 영향: AC 4(빈 값으로 열림)·5(삽입 위치·환경 상속)·6(저장 카드 환경 불변)·14(삭제 확인 취소 시 요청 0)이 **사람 손 검증에만 매달려 있다**. 특히 AC 14 「취소하면 네트워크 요청 0」은 회귀가 조용하다.
- 권장: 최소 1파일(`front/__tests__/wp131-deploy-surface.test.tsx`) — `addSurfaceBlock` 삽입 위치·신규 카드 빈 값·삭제 확인 취소 시 `fetch` 미호출 3건만이라도.

### W-2. `surface_key` 상한 50 이 **네 곳에 각각 하드코딩**돼 있고, 어긋나도 테스트가 안 잡는다
- `back/app/models/product_deployment.py:50` `SURFACE_KEY_MAX_LENGTH = 50` / `back/alembic/versions/0139_deployment_surface_key.py:64` `_MAX_LENGTH = 50` / `back/tests/migrations/test_0139_deployment_surface_key.py:124` `== 50` / `back/tests/services/test_deployment.py:363` `== 50`.
- 근거: 같은 파일이 **백필 리터럴에 대해서는** 두 정의가 갈라지는 것을 막는 단언을 일부러 심어 놨다(`test_admin_deployments.py:628` — migration 소스를 읽어 `_BACKFILL == DEFAULT_SURFACE_KEY` 확인). **상한값에는 같은 장치가 없다.**
- 실패 시나리오: 누군가 `SURFACE_KEY_MAX_LENGTH` 를 100 으로 올리고 migration 을 안 쓰면 — 앱은 60자를 통과시키고 DB 가 `VARCHAR(50)` 으로 거부해 **400 이 아니라 500** 이 난다. 현재 테스트는 전부 50 을 하드코딩하고 있어 초록을 유지한다.
- 권장: `_BACKFILL` 과 동형으로 `test_admin_deployments.py` 에 `_MAX_LENGTH = {SURFACE_KEY_MAX_LENGTH}` 소스 단언 1줄 추가, 또는 `character_maximum_length == SURFACE_KEY_MAX_LENGTH` 로 교체.

### W-3. SPEC AC 4 의 「409 가 아니라 **400**」이 FE 에서는 HTTP 400 으로 관측되지 않는다
- `useDeployInfo.ts:281-284`(saveBlock) · `:391-396`(save) 가 빈 surface 를 **클라이언트에서 먼저 차단**한다(`SURFACE_REQUIRED`). 따라서 「그대로 저장」 시 서버 400 이 발생하지 않고 인라인 문구만 뜬다.
- 근거 대조: SPEC §4 FE 는 「빈 값 저장은 400 … 의도한 실패 선택」이라 쓰고, 동시에 「저장 전 클라이언트 사전 검증」도 요구한다. **시안 `commitDeploys`(`Product Management.html:580`) 역시 클라이언트에서 alert 로 차단**하며 문구에 `(VALIDATION_ERROR 400)` 을 달아 둔다 — 즉 시안이 정본이라면 현 구현이 맞다.
- 사용자 눈에 보이는 결과(「이름을 지어라」· 무의미한 중복 충돌 없음)는 계약 그대로다. **서버 400 경로 자체는 살아 있고 테스트로 고정돼 있다**(`test_blank_surface_key_400`).
- 판정을 FAIL 로 올리지 않는 이유: 계약의 *목적*(운영자에게 이름을 요구)과 시안이 모두 현 구현 편이다. 다만 **AC 4 를 「400 응답」으로 문자 그대로 검수하면 어긋나 보인다** — 코디가 AC 체크 시 알고 있어야 한다.
- 참고(문구): 클라이언트 사전검증 문구 `surface(표면 이름)를 입력하세요 — 비어 있을 수 없습니다.`(`useDeployInfo.ts:74`)는 서버 문구(`surface_key 는 비어 있을 수 없습니다`)와 다르다. §케이스 매트릭스가 소유하는 것은 **서버 문구**이고 그것은 일치하므로 위반 아님.

### W-4. `test_gm_command.py` — 새로 추가한 `from sqlalchemy import text` 가 다수 함수의 지역변수 `text` 에 가려진다
- `back/tests/api/test_gm_command.py:18` 이 모듈 레벨 `text` 를 들여왔는데, 같은 파일의 기존/신규 테스트 9곳이 `text = res.json()["text"]` 로 **같은 이름을 덮어쓴다**(`:114,129,137,146,223,242,273,285,297`).
- 현재는 버그가 아니다 — SQL `text()` 를 쓰는 함수(`test_marking_disappears_…`)가 지역 `text` 를 만들지 않는다. **다음 사람이 그 함수들 중 하나에 SQL 한 줄을 넣는 순간 `TypeError`** 가 난다.
- 권장: `from sqlalchemy import text as sa_text` 로 별칭, 또는 지역변수명을 `body_text` 로.

---

## 관찰 (축 10) — 계약은 맞는데 운영자 눈에 걸릴 자리. **FAIL 아님**

> 브리프가 알려준 기존 3건(`prod` 칩 6회 반복 · 백필 `기본` 첫인상 안내 부재 · 빈 surface 를 저장 눌러야 앎)은 제외하고, **새로 보이는 것**만 적는다.

### O-1. 모달의 배치 저장이 **빈 신규 카드 하나 때문에 전부 멈춘다** (가장 비쌀 자리)
- `useDeployInfo.ts:391-407` — `save()` 의 사전검증 루프가 빈 surface 를 만나면 `return` 한다. `setSaving(true)` **전**이라 그 시점까지의 삭제 스테이징(`removedIds`)·다른 카드의 수정이 **한 건도 커밋되지 않는다.**
- 확장 전에는 `if (b.id === null && !url) continue;`(구 코드) 가 **빈 신규 카드를 조용히 스킵**했다 — 그 한 줄이 이번에 제거됐다(의도적이고 시안 `commitDeploys` 의 검사 순서를 따른 것).
- 운영자 시나리오: `[+ 환경 추가]` 를 눌러 놓고 마음을 바꿔 다른 카드만 고친 뒤 [저장] → **아무것도 안 저장되고**, 에러는 화면 밖(목록 맨 뒤)의 빈 카드에 인라인으로 뜬다. 카드가 6장이면 스크롤해야 원인을 본다.
- 시안과의 차이: 시안은 같은 자리에서 `continue`(그 행만 건너뛰고 나머지는 저장), TSX 는 `return`(전부 중단). 기존 TSX 관례(블록 인라인 + 중단)를 따른 결과라 「이탈」은 아니지만, **행 수가 늘어난 뒤에야 비용이 드러나는 자리**다.
- 인라인 편집 경로(`DeployInfoSection` → `saveBlock`)는 행 단위라 이 문제가 없다. **모달 경로만** 해당.

### O-2. 「surface 오름차순」이 층마다 **다른 정렬**이다 — 모달 순서와 `/gm` 순서가 갈릴 수 있다
- FE 표시: `lib/admin-deployments.ts:60` `localeCompare(…, "ko")`
- `/gm`: `gm_command.py:107` 파이썬 기본(코드포인트) 정렬
- 대시보드 선택: `db_source.py:76` 파이썬 코드포인트
- DB 조회: `product_deployment_repo.py:90-94` PG collation
- 계약상 문제는 아니다 — SPEC 은 `/gm` 정렬과 FE 표시 정렬을 **각자 소유**라고 못 박았고, `/gm` 에 요구한 것은 「호출마다 달라지지 않을 것」(결정성)뿐이며 그건 만족한다.
- 다만 운영자 체감: 대소문자만 다른 두 이름(`Admin` / `admin` — 계약상 둘 다 허용, 테스트 `test_case_is_not_folded` 가 보장)이나 기호로 시작하는 이름이 섞이면 **모달에서 본 순서와 슬랙 카드 순서가 다르다.** 「내가 위에 둔 게 슬랙에선 아래」라는 문의가 날 수 있는 자리.

### O-3. `[+ surface 추가]` 를 누르는 즉시, **저장하지도 않았는데** 옆 행의 읽기 뷰에 surface 라벨이 돋아난다
- `DeployInfoSection.tsx:147-150` — `showSurface` 를 `d.blocks.filter(같은 환경).length >= 2` 로 계산하는데, `d.blocks` 에는 **아직 POST 되지 않은 신규 블록**이 포함된다.
- 결과: `[+ surface 추가]` 클릭 → 그 환경의 기존 행 읽기 뷰에 `· 기본` 이 즉시 붙는다 → 신규 카드를 취소/삭제하면 다시 사라진다.
- 계약(「행 수 ≥ 2 일 때만」)은 서버 상태 기준으로 읽는 편이 자연스럽고, 지금은 **폼 상태 기준**이다. `/gm`(서버 기준)과 순간적으로 어긋난다.

### O-4. 미저장 초안을 지울 때도 **파괴적(빨강) 확인 모달**이 뜨고 「사라집니다」라고 말한다
- `EnvBlockCard.tsx:79-93` — 확인 게이트의 조건이 `block.accounts.length > 0` 하나다. `block.id === null`(아직 서버에 없음)을 보지 않는다.
- 시나리오: `[+ 환경 추가]` → 계정 2줄 입력 → 마음 바꿔 [삭제] → 「이 배포 행(prod · (이름 없음))을 삭제하면 시연계정 2건이 함께 사라집니다」 + destructive 스타일. 실제로는 서버에 아무것도 없어 **`deleteBlock` 이 로컬에서 폐기만 한다**(`useDeployInfo.ts:353-361`).
- SPEC §UX 문구(「이 배포 행({환경} · {surface})을 삭제하면 시연계정 {N}건이 함께 사라집니다」)를 그대로 쓴 결과라 계약 위반은 아니고, `(이름 없음)` 폴백도 준비돼 있다. 다만 **되돌릴 것이 없는 삭제에 되돌릴 수 없다는 톤**이 붙는다.
- 모달 경로에서는 반대 방향의 어긋남도 있다: `DeployInfoModal` 의 `onRemove` 는 `removeEnvBlock`(스테이징)이라, 확인 모달이 「사라집니다」라고 말한 시점에는 **아직 DELETE 가 안 나간다**(모달 [저장] 때 나간다). 모달을 그냥 닫으면 아무 일도 안 일어난다 — 계약(「취소 시 아무것도 바뀌지 않음」)에는 부합하지만 문구는 즉시 삭제를 암시한다.

### O-5. 저장된 카드마다 「환경 불변 — 옮기려면 삭제 후 재생성」 안내문이 **행 수만큼 반복**된다
- `EnvBlockCard.tsx:117-122` — `isSaved` 분기에서 select 를 이 문장으로 치환한다. 카드마다 있으므로 nexus prod 6행이면 **같은 문장이 6번** 보인다(기존에 지적된 `prod` 칩 6회와 같은 층의, 그러나 별개 요소).
- 계약대로 「환경은 읽기 전용 칩」을 구현한 결과이고, 안내 자체는 운영자가 한 번은 읽어야 하는 정보다. 반복 위치(카드마다 vs 모달 상단 1회)는 화면 결정이라 여기서 판정하지 않는다.

---

## 확인한 것 (PASS 근거 — 체크리스트 전항)

### backend 리뷰 체크리스트 (`rules.md` §backend)
- **계층 방향** — `routers/deployments.py` 에 `session.execute`·`select()` **없음**(변경분은 `surface_key` 전달 3줄 + docstring). ✔
- **DB 접근 위치** — 쿼리는 `repositories/product_deployment_repo.py` 에만. `services/deployment.py` 는 `store` protocol 만 호출. `dashboard/db_source.py` 의 `select()` 는 **기존 자리**(이 파일은 원래 dashboard 전용 조립 모듈, 이번에 자리를 바꾸지 않았다). ✔
- **자리 규칙** — 정규화·중복 판정 = service, 문구 상수 = `core/errors.py` + service, 제약 = alembic, 상수(`DEFAULT_SURFACE_KEY`·`SURFACE_KEY_MAX_LENGTH`) = model. HTTPException 이 repository 로 내려온 곳 없음. ✔
- **재사용** — `_normalize_environment` 옆에 `_normalize_surface_key` 를 같은 관례로 추가(재구현 아님). 409 생성이 4곳에서 중복될 뻔한 것을 `_duplicate()` 헬퍼 하나로 모았다(`services/deployment.py:76-86`). `DEFAULT_SURFACE_KEY` 를 seed·dashboard 가 **import 해서** 쓰고 리터럴을 복제하지 않는다. migration 만 의도적으로 복제하고 **그 이유를 주석에 남긴 뒤 테스트로 고정**했다 — 이 리포에서 본 재사용 판단 중 가장 잘 된 축. ✔
- **스키마 경계** — 응답은 `DeploymentRow`(Pydantic) 경유(`routers/deployments.py:84-92`). 모델 직접 노출 없음. ✔
- **마이그레이션** — `models/` 변경에 대응하는 `0139_deployment_surface_key.py` 가 diff 에 있다. head 체인 검증: `0137_tasks_created_by_ix` → `0138_task_body_refs` → `0139_deployment_surface_key`, **단일 head**. `revision` 문자열 ≠ 파일명 관례도 지켰다. ✔
- **테스트 존재·의미** — 신규 경로마다 있고, **구현을 베낀 테스트가 아니다**. 근거로 삼은 반례 3개:
  1. `test_single_row_group_hides_even_a_non_default_name` — 값 판정이면 통과하고 행 수 판정이라야 통과한다.
  2. `test_default_surface_wins_over_other_surfaces` — `기본` 을 **마지막에 INSERT** 해서 덮어쓰기 구현이 우연히 통과하는 길을 막았다.
  3. `test_falls_back_to_the_first_surface_in_ascending_order` — `기본` 이 없는 그룹으로 「sentinel 아님」을 코드에서 성립시킨다.
  추가로 `test_update_without_a_rename_does_not_disguise_other_integrity_errors` 는 **409 둔갑 방지**라는 잘 안 쓰는 방향까지 잡는다. ✔

### frontend 리뷰 체크리스트 (`rules.md` §frontend)
- **컴포넌트 재사용** — 삭제 확인을 새로 만들지 않고 기존 `components/ui/confirm-dialog.tsx` 의 `useConfirm()` 사용(`EnvBlockCard.tsx:18,70`). API(`title`/`description`/`confirmLabel`/`danger`) 실물 대조 완료. 그 파일 머리 주석이 「WKWebView 는 `confirm()` 이 항상 false」를 이미 근거로 갖고 있어 시안 이탈이 정당화된다. ✔
- **기존 코드 활용** — 정렬·enum·라벨을 `lib/admin-deployments.ts` 에 두고 두 화면이 import. 훅(`useDeployInfo`)에 로직이 남고 컴포넌트는 렌더만. `errorMessage()`(`lib/admin`) 재사용으로 **서버 문구가 그대로 화면에 뜬다**(`useDeployInfo.ts:338,449,470`) — FE 가 서버 문구를 다시 쓰지 않는다. ✔
- **자리 규칙** — `compareDeployDisplay`·`deployEnvDisplayRank` 가 `lib/` 에 있다(모달·인라인 2곳 사용). 페이지 안 사유화 없음. ✔
- **중복** — `emptyBlock()` 추출로 `addEnvBlock`/`addSurfaceBlock` 의 블록 리터럴 복붙을 제거. `dupeKey`/`duplicateMessage`/`SURFACE_REQUIRED` 를 상수·함수로 뽑아 `saveBlock`·`save` 두 경로가 **같은 문구·같은 키**를 쓴다. ✔
- **컨벤션** — 시안의 class 문자열·구조를 그대로 옮겼고(`env-surface` 입력란 마크업 대조), 기존 파일의 Tailwind 토큰(`mgray`/`mred`/`brand`) 관례와 일치. ✔

### 시안 대조 (7축 상세)
| 시안 | TSX | 결과 |
|---|---|---|
| `ENVS`(select) / `ENV_DISPLAY_ORDER`(표시) **두 배열** | `DEPLOY_ENVIRONMENTS` / `DEPLOY_ENV_DISPLAY_ORDER` | 일치 |
| `envOrder()` + `localeCompare(,'ko')` 로 prefill 정렬 | `compareDeployDisplay` (`useDeployInfo.ts:168`, prefill 1회) | 일치(정렬 시점까지 동일 — 타이핑 중 카드가 안 움직인다) |
| `addSurfaceBlock` = `insertAdjacentHTML('afterend')` + 환경 상속 + surface 빈 값 | `useDeployInfo.ts:247-259` (`slice(0,at+1), next, slice(at+1)`) | 일치 |
| `addEnvBlock` = `beforeend` + `defaultEnv()`(안 쓴 환경, 없으면 prod) | `useDeployInfo.ts:235-241` | 일치 |
| `commitDeploys` 검사 순서 = **surface → url → 중복** | `useDeployInfo.ts:281-303` · `:391-407` | 일치 |
| 중복 키 `env+' '+surface` | `dupeKey()` — 동일 구분자 ` ` | 일치 |
| 저장 행은 환경 칩(select 없음) | `isSaved` 분기(`EnvBlockCard.tsx:117`) | 일치 |
| placeholder `기본 · 고객 홈페이지 · 운영자 어드민 …` | 동일 문자열 | 일치 |
| 삭제 확인 문구 | title/description 2단 분할(medikit) — 문장 내용 동일 | 의도된 이탈(WP §Open Issues 가 형태를 WP·시안 판단으로 넘겼다) |
| `confirm()` | `useConfirm()` | **의도된 이탈 — 흠 아님**(브리프 명시) |

### allowed_paths (축 2) — 조건부 PASS 의 이유
- 변경 22파일이 전량 `back/` ∪ `front/` 안에 있고, 리포 밖 파일·설정·문서 변경 0건이다.
- **그러나 커밋이 하나도 없어(`HEAD == origin/dev`) 「BE 워커가 `back/` 만, FE 워커가 `front/` 만 건드렸는지」는 git 으로 증명할 수 없다.** 워킹트리 하나에 두 워커의 산출물이 섞여 있고 저자 정보가 없다.
- 대신 가능한 검증을 했다: 각 파일의 변경 내용이 그 파일이 속한 Phase 와 일치하는지 내용으로 대조했고(BE 파일에 FE 개념, FE 파일에 BE 개념이 섞인 곳 없음), 언어·계층 교차 오염 0건이다. **결론: 실질 이탈 없음. 절차상 증명은 불가.**

---

## 기존 부채 (이번 판정 제외)

- **`useDeployInfo.save()` 의 부분 실패가 ID 를 동기화하지 않는다** — `useDeployInfo.ts:426-476`. 배치 중 3번째 카드가 409/400 으로 실패하면 `return` 하는데, 이미 성공한 1·2번 카드의 POST 응답을 `replaceBlock` 하지 않아 로컬 `id` 는 여전히 `null` 이다. 사용자가 3번을 고쳐 다시 [저장] 하면 **1·2번이 재-POST 되어 409** 가 난다. 구조는 확장 전과 동일한 **기존 부채**지만, surface 축으로 한 모달의 행 수가 늘어나 **부분 실패 확률이 올라갔다**(nexus prod 6행). 같은 함수의 `saveBlock` 은 `replaceBlock` 을 한다(`:343`) — 두 경로가 갈려 있다.
- 테스트 DB `org_unit ↔ department` 매핑 seed 부재로 `product_assignment` 생성 경로 전반이 실패한다 — `flaky-baseline-evidence.md` 판정 그대로. 이번 작업 범위 밖.

---

## 무관 (이번 변경과 접점 0)

- `tests/api/test_admin_deployments.py::TestProductAssigneeAccess` 12건 실패 — 환경 문제. 판정 파일 인용, 재조사 안 함. 이번 diff 가 `policies/deployment.py`·게이트를 건드리지 않은 것은 변경 파일 목록으로 확인했다.
- `tests/schema/test_product_assignment_schema.py` 9건 실패 — 같은 사유(무접촉 파일).
- MCP 서버 `pm-dashboard` 연결 타임아웃 — 이 리뷰와 무관(도구 환경).
