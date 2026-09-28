# [planner] SPEC-051 OQ-4 해소 — 배포 레지스트리에 surface 축 추가 (환경당 URL 1개 → N개)

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

**너는 이 작업의 맥락이 하나도 없다.** 아래 §1 을 먼저 다 읽고 시작해라.
같은 워크트리에 `reviewer_spec` 이 **나중에** 탄다 — 지금은 너 혼자다. 네 산출물이 그 검수 대상이다.

⚠ **역할 문서 `rules.md` 의 「`products/{service}/` 안은 손대지 않는다」는 charty·linky 등 타 제품 얘기다.**
이번 대상 `products/mediness/` 는 **네 담당이고 §5 allowed_paths 에 들어 있다.** 헷갈리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md`
  ← **이번에 고칠 문서. 계약의 SoT.** 여기 없는 건 발명하지 마라.
- 같은 워크트리 `products/mediness/30-work/work-071-deploy-demo-env-gm.md`
  ← **거의 동형인 선례**(환경 enum 에 `demo` 를 추가하며 DB·API·`/gm`·FE 를 함께 정합한 판). 이번 작업의 **문체·절 구성·변경 노트 형식**을 여기에 맞춰라.
- 같은 워크트리 `products/mediness/20-spec/spec-050-product-catalog.md` — `product` 카탈로그(slug·`is_active`). `nexus` 가 여기 등재돼 있다.
- 같은 워크트리 `products/mediness/20-spec/spec-052-product-pipeline-registry.md` — [기본정보] 탭 = 배포정보 편집 표면의 소유자.
- 같은 워크트리 `products/mediness/20-spec/spec-003-capability-rbac.md` — `deployment.registry.read/update` leaf 체계.
- 같은 워크트리 `rules/document-pipeline.md` · `rules/qa/llms.md` — 문서 규칙.

**기대는 개념** — 이 작업이 따를 판단 기준:

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/functional-dependency.md`
  — **이번 변경의 본질이 이것이다.** 기존 스펙은 「(제품, 환경) → URL」이 함수종속이라고 **가정**했는데, nexus 가 그 가정을 깼다. 종속이 깨진 자리에 결정자를 하나 더 붙이는 게 이번 수정이다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/unique-key.md`
  — 복합 유니크 키를 넓히는 것이 무엇을 허용하고 무엇을 여전히 막는지. §Validation 의 중복 규칙을 여기 기준으로 다시 써라.

## 2. 배경 / 무엇을 바꾸나

SPEC-051 은 배포 레지스트리를 `(product_slug, environment)` **유니크**로 고정했고, 항목당 `service_url` 이 **하나**다. 구현도 그대로 굳었다 — `back/app/models/product_deployment.py` 의 `uq_product_deployment_slug_env`, FE `EnvBlockCard` 가 `usedEnvs` 로 이미 쓴 환경을 select 에서 제외해 **환경당 블록 1개**. 그래서 한 환경에 서비스 URL 이 둘 이상인 제품은 두 번째부터 `409 DUPLICATE_DEPLOYMENT` 로 튕긴다.

**`nexus`(더데이랩스 홈페이지)가 그 한계를 터뜨린 첫 제품이다.** prod 환경에 서비스 URL 이 **6개**다(고객 홈페이지 FE · 운영자 어드민 FE · BE 등 — 실제 목록은 이번 범위 밖, §7). `nexus` 는 카탈로그에 active 로 등재돼 있다(`back/app/seeds/products_prod_snapshot.py` ordering 12, label 「더데이랩스(홈페이지)」) — OQ-1 의 「홈페이지 제외」는 이미 지나간 상태이므로 **OQ-1 을 다시 열지 마라.**

이건 스펙이 이미 미뤄 둔 자리다 — **§6 OQ-4 ①「say-admin 류 복수 서비스 surface(URL 복수 허용 vs 별 행)」**. 계약서엔 "URL 복수·계정 복수 허용"이라 써 놓고 데이터 모델 결정을 BE WP 로 넘겼는데, 구현이 단수로 굳어 계약과 어긋난 상태다. `say` prod 도 같은 대기줄에 있다(§데이터/부록 비고 `say-admin = ?service=say-admin — 복수 surface(OQ-4)`).

**사용자가 2026-09-22 에 모델 방향을 확정했다.** 이번 태스크는 그 결정을 SPEC-051 에 반영해 **OQ-4 ① 을 RESOLVED 로 닫는 것**이다.

## 3. 계약 (사용자 확정 — 이대로 반영. 재논의·재제안 금지)

> 아래 네 줄은 **2026-09-22 사용자 결정**이다. 대안을 다시 늘어놓지 말고 이대로 문서에 박아라.

1. **모델 = 별 행.** 유니크 키를 `(product_slug, environment, surface_key)` 로 **확장**한다. `nexus` prod = 6행. 행 하나가 곧 surface 하나다. (surfaces JSONB 배열·별도 surface 테이블은 **검토했고 탈락**했다 — 되살리지 마라.)
2. **시연계정은 surface 행마다 따로 붙는다.** 행마다 `demo_accounts` 를 갖는 현행 구조가 그대로 답이다 — **계정 쪽 shape 은 건드리지 않는다.** `prod/어드민`엔 계정이 있고 `prod/BE API`엔 없을 수 있다.
3. **`surface_key` 는 자유 입력 문자열.** enum 아니다(제품마다 surface 종류가 달라 enum 은 다음 제품에서 또 막힌다). 검증은 두 가지만 — **비어 있지 않음** + **같은 `(product_slug, environment)` 안에서 중복 금지**(중복이면 409). 사용자가 모달에서 「고객 홈페이지」·「운영자 어드민」·「say-admin」처럼 직접 친다. 길이 상한 등 세부는 네가 제안하고 근거를 달아라.
4. **기존 행 마이그레이션은 기본값 1개로 흡수한다.** 이미 있는 8개 seed 행은 `surface_key` 에 기본값(예: `기본`·`default` — 값은 네가 제안)을 채우면 그대로 유효하다. 기존 `(제품,환경)` 유니크를 쓰던 데이터가 깨지지 않아야 한다.

**바뀌지 않는 것** (착각 금지):
- 권한 게이트 — `deployment.registry.read/update` + `product_assignment` 참여 축, 2026-07-22·07-31 결정 전부 **불변**.
- 민감값 두 축 — DB·런타임 응답엔 평문 / **스펙 문서·git 엔 미박제**. 이번 문서에도 비밀번호·실 URL 을 박지 마라.
- 환경 enum — `dev`/`stg`/`prod`/`demo` 그대로. surface 는 환경과 **직교하는 새 축**이지 환경 값이 아니다.
- `/gm` 의 활성 필터·ephemeral·3초 동기 응답 계약.

## 4. 먼저 읽을 핵심 파일 (코드 — 읽기만. 이 레포가 아니다)

코드는 **다른 레포**다(`/Users/kknaks/git/harness_works/mediness-app`). **읽기만 하고 절대 고치지 마라.** 현행 구현이 스펙과 어디까지 일치하는지 확인하는 용도다.

- `back/app/models/product_deployment.py` — `uq_product_deployment_slug_env`, `demo_accounts` JSONB, enum `deployment_environment`. **지금의 단수 제약이 사는 곳.**
- `back/app/schemas/deployment.py` · `back/app/routers/deployments.py` · `back/app/services/deployment.py` — API 계약의 실제 shape·409 발생 지점.
- `back/app/services/gm_command.py` — `/gm` 응답 조립. **행이 N개로 늘면 응답 본문이 어떻게 보여야 하는지**를 여기 현행 포맷 기준으로 제안해라.
- `front/components/admin/products/EnvBlockCard.tsx` · `useDeployInfo.ts` — `usedEnvs` 로 환경을 소진시키는 현행 UX. **surface 축이 생기면 「환경 블록 안에 surface 행 N개」로 바뀐다** — UX Contract·Wireframe 을 그 모양으로 다시 써라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

실질 수정 대상은 **`products/mediness/20-spec/spec-051-product-deploy-registry.md` 한 파일**이다. 다른 spec 을 고치고 싶어지면 고치지 말고 §리포트 「다른 팀 영향」에 적어라.

## 6. 구현 단계

1. **§1 읽기** 전부 — 특히 work-071 의 변경 노트 형식.
2. **SPEC-051 frontmatter** — `version` 0.0.2 → 0.0.3 (work-071 이 어떻게 올렸는지 확인해 관례를 따라라), `last_updated` = 2026-09-22.
3. **본문 머리에 「2026-09-22 변경 노트」 추가** — 기존 「2026-07-31 변경 노트」 형식 그대로. 무엇이 왜 바뀌는지(함수종속 가정이 깨졌다), 무엇이 안 바뀌는지(§3 「바뀌지 않는 것」)를 명시.
4. **§3 계약 정합** — API 표의 POST 설명(`product_slug + environment + service_url` → surface 포함), 409 조건, PATCH 대상 필드, GET 응답 shape(행이 N개), query 파라미터에 surface 필터가 필요한지 판단해 제안.
5. **§3 `/gm` 계약 정합** — 한 제품·환경에 행이 여럿일 때 ephemeral 응답 본문 표기. `/gm 넥서스 prod` 가 6줄로 나오는 모양을 예시로 박아라. 인자 파싱에 surface 토큰을 **추가하지 않는다**(3토큰 파싱은 과설계 — 다만 판단 근거를 한 줄 남겨라).
6. **§3 Validation 표** — `(product_slug, environment)` 유니크 행을 `(product_slug, environment, surface_key)` 로 교체하고, `surface_key` 행 신설(비어있지 않음 / 동일 제품·환경 내 중복 금지 / 길이 제안).
7. **§3 케이스 매트릭스 · §5 Acceptance Criteria** — surface 복수 케이스 AC 추가. 최소: 같은 (제품,환경)에 surface 다른 행 2개 생성 성공 / surface 까지 같으면 409 / surface 별 시연계정 분리 / 기존 단일 행이 기본 surface 로 계속 조회됨 / `/gm` 에 N행 노출.
8. **§2 UX Contract · Wireframe · §4 Frontend Implementation** — 「환경 블록 1개」 → 「환경 블록 안 surface 행 N개」. `usedEnvs` 로 환경을 소진시키던 규칙이 **어떻게 바뀌는지**(같은 환경을 다시 고를 수 있어야 한다) 명시.
9. **§4 DB 절** — 유니크 키 확장 + `surface_key` 컬럼 + 기존 행 기본값 백필. 구체 migration 번호·컬럼 타입은 **WP 이관**이라고 적어라(스펙은 계약까지).
10. **§6 OQ-4** — ① 을 **RESOLVED 2026-09-22(사용자)** 로 닫고 결정 내용·근거·탈락 대안을 적는다. **② watch prod 조직별 계정 그룹은 그대로 열어 둔다** — 이번 결정으로 ② 가 해소되는지 아닌지 한 줄로 판단해 적어라(surface 축으로 표현 가능한지).
11. **§데이터/부록** — `say` prod 비고의 `복수 surface(OQ-4)` 를 새 모델 기준으로 갱신. **`nexus` 행은 추가하지 마라**(§7).
12. **§Related** 정합.
13. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/planner-report.md` 에 남긴다 (역할 문서 `rules.md` 의 리포트 형식). **scratchpad 에 쓰지 마라 — 네 터미널이 죽으면 같이 죽는다.**

## 7. 범위 제약 — 하지 말 것

- **WP(`30-work/`) 를 쓰지 마라.** 이번 태스크는 **SPEC 개정까지**다. WP 는 사용자 리뷰 뒤 별도 발주한다.
- **코드 레포(`mediness-app`)를 고치지 마라.** 읽기만.
- **`nexus` 의 실제 6개 URL·시연계정을 문서에 박지 마라.** 데이터 투입은 이번 범위가 아니다(배포 후 사용자가 모달에서 직접 입력). §데이터/부록 seed 표에 nexus 행을 만들지 마라.
- **비밀번호 평문을 어디에도 쓰지 마라** (§4 Functional Rule 축2).
- **권한 게이트·환경 enum·`/gm` 활성 필터를 건드리지 마라.** 이번 관심사는 surface 축 하나다.
- **OQ-1(레지스트리 포함 범위)·OQ-2(비번 저장)·OQ-5·OQ-6 을 다시 열지 마라.** 전부 RESOLVED 다.
- **확정된 모델 결정(§3)에 대안을 다시 제시하지 마라.** 세부(기본값 문자열·길이 상한·GET query 파라미터)만 제안 대상이다.
- 커밋·push·PR 하지 마라.

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- **mediness 제품 범위 ERROR 0** 이면 통과. 타 제품의 기존 WARN/ERROR 는 **"무관"으로 분리해** 보고한다.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 추가로 자가 점검: 문서 안에 **`(product_slug, environment)` 만 쓰는 옛 표현이 남아 있지 않은지** grep 으로 전수 확인해라. 한 군데만 남아도 계약이 둘로 갈린다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --from term_c1552692-d75c-42c6-8d40-8e4db637a457 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
