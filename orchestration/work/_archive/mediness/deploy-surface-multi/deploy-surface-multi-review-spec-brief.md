# [reviewer_spec] SPEC-051 surface 축 확장 검수 — 스펙·시안 정합과 계약 무결성

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

**너는 이 작업의 맥락이 하나도 없다.** 아래 §1~§3 을 먼저 다 읽어라.
같은 워크트리에서 `planner` 가 작업했고 **지금은 끝났다** — 충돌 없다. 변경은 **워킹트리에 미커밋 상태**로 있다(`git diff` 로 본다).

⚠ **너는 read-only 다.** 문서를 고치지 마라. 산출물은 **리뷰 리포트 파일 1개뿐**이다(§6-마지막).
고치고 싶은 것이 보이면 **고치지 말고 리포트에 적어라.** 수정은 원 워커에게 재발주한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md` ← **검수 대상 1. 계약의 SoT**
- 같은 워크트리 `products/mediness/21-html/Product Management.html` ← **검수 대상 2. 시안**(배포정보 모달 구간)
- 같은 워크트리 `products/mediness/log.md` ← 검수 대상 3 (spec-change entry 1행)
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/planner-report.md`
  ← **planner 가 4판에 걸쳐 남긴 리포트.** 무엇을 왜 그렇게 했는지가 여기 있다. **다만 이건 피검자의 진술이다 — 근거로 인용하되 사실로 믿지 마라. 전부 원본에서 직접 확인해라.**
- 같은 워크트리 `products/mediness/20-spec/spec-050-product-catalog.md` · `spec-052-product-pipeline-registry.md` · `spec-003-capability-rbac.md` — 인접 계약(카탈로그·[기본정보] 탭 표면·capability leaf)
- 같은 워크트리 `rules/document-pipeline.md` · `rules/qa/llms.md`

**기대는 개념** — 이 검수가 따를 판단 기준:

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/functional-dependency.md`
  — 이번 변경의 본질. 「(제품, 환경) → URL」함수종속이 깨져서 결정자를 한 축 더 붙인 것이다. **부분 종속이 남아 있지 않은지**(환경에만 매달려야 할 속성이 표면 행에 흩어졌거나 그 반대) 이 잣대로 봐라.
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/unique-key.md`
  — 복합 유니크를 **넓히는** 변경이 무엇을 허용하고 무엇을 여전히 막는지. NULL 허용 여부가 유니크 의미를 바꾸는 지점 포함.

## 2. 배경 / 무엇을 바꿨나

SPEC-051 은 배포 레지스트리를 `(product_slug, environment)` 유니크로 고정했고 항목당 `service_url` 이 하나였다. `nexus`(더데이랩스 홈페이지) prod 에 서비스 URL 이 6개라 두 번째부터 409 로 막힌다. 스펙 §6 **OQ-4 ①** 이 이 문제를 열어 둔 자리였다.

**사용자가 2026-09-22 에 모델을 확정했고**, planner 가 4판에 걸쳐 반영했다. 최종 산출은 `spec-051` + `21-html` + `log.md` 세 파일 미커밋 변경이다.

⚠ **판이 넷으로 늘어난 것은 코디네이터가 범위를 뒤에 세 번 넓혔기 때문이지 planner 의 실패가 아니다.** 아래는 **전부 코디 책임**이니 planner 흠으로 잡지 마라:

- 2차(`21-html` 시안 동기화) — 1차 브리프가 대상을 `spec-051` 한 파일로 좁게 적었다.
- 3차(`기본` 프리필 제거 · Wireframe 평평화) — planner 가 **자기가 1차에 쓴 문장의 약점을 자진 신고**했고 코디가 처분했다.
- 4차(시안 호출부 `surface:'기본'` 제거) — **코디가 「시안은 이미 빈 값이라 맞다」고 잘못 판정**했고(템플릿만 보고 호출부를 놓쳤다) planner 가 그 오판을 잡아 보고했다.

**네가 볼 것은 「최종 상태가 옳은가」다.** 과정의 판 수가 아니다.

## 3. 계약 (사용자 확정 — 이 기준으로 판정해라)

> 아래는 **2026-09-22 사용자 결정**이다. 스펙이 이것과 어긋나면 FAIL 이다. **이 결정 자체에 대안을 제시하지 마라** — 네 일은 반영 여부 판정이다.

1. **모델 = 별 행.** 유니크 `(product_slug, environment, surface_key)`. `nexus` prod = 6행. 행 1개 = surface 1개.
2. **시연계정은 surface 행마다.** `demo_accounts` shape 무변경.
3. **`surface_key` = 자유 입력 문자열**(enum 아님). 검증은 비어있지 않음 + 같은 (제품,환경) 안 중복 금지(409).
4. **범위는 구조까지.** `nexus` 실데이터 6건은 배포 후 운영자가 모달 입력 — **문서에 박지 않는다.**

**코디가 승인한 planner 제안**(이것도 계약이다):

- 백필 기본값 `기본` — **sentinel 아님, 프리필 아님.** 백필 값 하나로만 존재.
- `/gm` surface 표기는 **값이 아니라 그룹 행 수 2건 이상**으로 판정 → 기존 단일 surface 제품 출력 회귀 0.
- `surface_key` 는 PATCH 로 개명 가능. `product_slug`·`environment` 는 불변.
- `surface_key` **NOT NULL 이 계약**(NULL 허용 시 유니크가 무력화).
- 신규 카드 surface 입력은 **빈 값 + placeholder**. 빈 채 저장은 **400**(409 아님).
- 모달 구조 = **평평 카드 + (환경, surface) 정렬**. 중첩 DOM 계층 아님.
- `/gm` 인자 토큰 2개 유지(surface 토큰 없음). GET 에 surface query 필터 미도입.

**불변이어야 하는 것** — 하나라도 바뀌었으면 FAIL:

- 권한 — `deployment.registry.read/update` leaf + `product_assignment` 참여 축 (2026-07-22·07-31 결정)
- 환경 enum — `dev`/`stg`/`prod`/`demo` 4종. surface 는 **환경과 직교하는 새 축**이지 환경 값이 아니다
- `/gm` 의 ephemeral · 3초 동기 · 활성 필터(`is_active=false` 제외, 조회 경로 전용)
- 민감값 두 축 — DB·런타임 응답엔 평문 / **스펙 문서·git 엔 미박제**
- OQ-1·OQ-2·OQ-3·OQ-5·OQ-6 은 RESOLVED 유지. **OQ-4 ②(watch prod 조직별 계정 그룹)는 열린 채 유지**

## 4. 먼저 읽을 핵심 파일 (코드 — 읽기만. 다른 레포다)

`/Users/kknaks/git/harness_works/mediness-app` — **읽기만. 절대 고치지 마라.** 스펙이 현행 구현과 어디서 갈리는지, 그 갈림이 **WP 로 넘어갈 수 있게 명시돼 있는지** 보는 용도다.

- `back/app/models/product_deployment.py` — 현행 `uq_product_deployment_slug_env`(2축), `demo_accounts` JSONB
- `back/app/schemas/deployment.py` · `routers/deployments.py` · `services/deployment.py` — 현행 API shape·409 발생 지점
- `back/app/services/gm_command.py` — 현행 `/gm` 응답 조립
- `front/components/admin/products/EnvBlockCard.tsx` · `useDeployInfo.ts` — 현행 `usedEnvs` 환경 소진 로직
- `back/app/seeds/deployments.py` — 백필 대상 기존 행

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 검수 항목 — 축마다 PASS / WARN / FAIL + 근거(파일:줄)

`git diff` 와 untracked 로 **변경 범위를 먼저 산정**한 뒤 시작해라.

1. **계약 반영** — §3 의 사용자 확정 4건 + 코디 승인 제안 7건이 스펙에 **정확히** 들어갔나. 문구만 있고 계약 절(§3 API·Validation·케이스 매트릭스)에 안 내려온 것이 있나.
2. **내부 정합 (제일 중요)** — 유니크 3축이 **모든 절에서 한 가지 의미**인가. 「(제품, 환경)만으로 유니크」를 전제하는 서술·예시·AC 가 **한 줄이라도** 남아 있으면 FAIL. §개요·§Placement·§Wireframe·§UX·§API·§`/gm`·§Validation·§케이스·§Lifecycle·§FE·§Functional·§DB·§AC·§OQ·§부록 **전 절을 훑어라.**
3. **스펙 ↔ 시안 정합** — `21-html` 배포정보 모달이 스펙 §2·§4 와 어긋나는 자리. **planner 가 12항목 대조로 12/12 라고 보고했는데, 그 12항목이 무엇이었는지에 갇히지 말고 네가 독립으로 항목을 세워 다시 대조해라.** 목업 JS(`envBlockHTML`·`addEnvBlock`·`addSurfaceBlock`·`commitDeploys`·`renderEnvBlocks`·`defaultEnv`)의 **실제 동작**이 스펙 서술과 맞는지 코드로 확인해라 — 주석이 아니라 코드다.
4. **불변 축 침범** — §3 「불변이어야 하는 것」 6줄 중 건드려진 것.
5. **민감값** — 비밀번호 평문·`nexus` 실 URL·실 계정이 **스펙이든 시안이든** 박혔나. 시안 목업 데이터도 본다.
6. **AC 검증 가능성** — §5 AC 가 **실제로 돌려볼 수 있는 문장**인가. 「잘 동작한다」류 모호한 항목, 근거 없이 참이 되는 항목, surface 복수 케이스가 빠진 구멍.
7. **WP 로 넘길 것이 명시됐나** — 스펙이 계약까지만 적고 구현 결정(migration 번호·컬럼 타입·백필 SQL·FE 컴포넌트 분해)을 WP 이관으로 남겼나. 반대로 **스펙이 구현 세부를 과하게 박아** WP 의 재량을 뺏은 자리도 지적해라.
8. **코드와의 gap** — §4 의 현행 구현 대비 **무엇을 바꿔야 하는지가 스펙에서 읽히는가.** 다음 판(WP·BE·FE)이 이 문서만 보고 움직일 수 있나. **읽히지 않는 자리가 곧 다음 판의 사고 지점이다.**
9. **문서 규칙** — frontmatter(version·last_updated·sources), lineage, `rules/document-pipeline.md` 준수, `log.md` entry 정합.
10. **사람 눈에 이상해 보일 자리** — 계약은 맞는데 **운영자가 실물에서 만나면 어색할 자리**를 짚어라. (예: 카드 6장에 `prod` 칩이 6번 반복되는 것, surface 이름이 비어 열리는 첫인상, 삭제 UX.) 테스트가 못 보는 층이고, 이게 다음 2루프 비용이 된다. **FAIL 로 잡지 말고 「관찰」로 분리해 적어라.**

**리포트는 반드시 아래 경로에 남긴다:**
`/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/review-spec-report.md`
**scratchpad 에 쓰지 마라 — 네 터미널이 죽으면 같이 죽는다.**

리포트 형식: 종합 판정(PASS/WARN/FAIL) → 축별 판정표 → 지적 목록(**파일:줄 + 근거 규칙/계약 + 제안**) → 관찰(항목 10) → 무관 항목.

## 7. 범위 제약 — 하지 말 것

- **문서를 고치지 마라.** 오타 하나도. 리포트에 적어라.
- **코드 레포를 고치지 마라.** 읽기만.
- **확정된 모델 결정(§3)에 대안을 제시하지 마라.** 반영 여부만 판정한다.
- **planner 리포트를 근거로 삼아 원본 확인을 건너뛰지 마라.** 피검자 진술이다.
- **판 수·과정을 흠으로 잡지 마라** (§2 — 코디 책임).
- 커밋·push·PR 하지 마라.

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- **mediness 범위 ERROR 0** 확인. 타 제품 기존 WARN/ERROR 는 **"무관"으로 분리 보고**.
- 참고 기준선: 코디가 직접 돌린 결과가 **0 error / 263 warning** 이고 **4판 내내 고정**이었다. 네 수치가 다르면 그 자체가 지적 대상이다.
- 리뷰는 read-only — **문서를 고치지 않고**, 판정과 근거만 낸다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --from term_855499b4-966c-4283-86f6-d2478f77f501 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 \
  --text "[worker_done] reviewer_spec 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --text "[질문] reviewer_spec: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
