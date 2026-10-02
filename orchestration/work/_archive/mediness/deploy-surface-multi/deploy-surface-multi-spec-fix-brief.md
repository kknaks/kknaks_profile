# [planner · 수정판] SPEC-051 검수 지적 13건 반영

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

**⚠ 너는 이 작업의 맥락이 하나도 없다.** 앞 판 워커의 터미널이 죽었다. **아래 §1 을 전부 읽고 시작해라.** 지금 워크트리엔 **미커밋 변경 3파일**이 이미 있다 — 그게 앞 판의 산출물이고, 네 일은 **그것을 고치는 것**이지 처음부터 쓰는 게 아니다.

⚠ **역할 문서 `rules.md` 의 「`products/{service}/` 안은 손대지 않는다」는 charty·linky 등 타 제품 얘기다.** `products/mediness/` 는 네 담당이다.

## 1. 먼저 읽을 것 (순서대로)

1. `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/review-spec-report.md`
   ← **이번 작업의 지시서 본체. 330줄 전부 읽어라.** 지적 14건이 「파일:줄 + 근거 + 제안」으로 들어 있다. 아래 §3 은 그 중 **무엇을 어떻게 처분할지 내가 정한 것**이고, 근거와 세부는 리포트에 있다.
2. `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/planner-report.md`
   ← 앞 판 워커가 4판에 걸쳐 남긴 기록. 무엇을 왜 그렇게 했는지.
3. `git -C /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec diff`
   ← 지금 워크트리의 미커밋 변경 3파일. **이게 네가 고칠 대상이다.**
4. 워크트리 `rules/document-pipeline.md` — 특히 **§Harness v1 실행 계약(:5-13)** 과 §`log.md` 요약 규약.
5. 워크트리 `products/mediness/20-spec/spec-051-product-deploy-registry.md` (본문) · `21-html/Product Management.html` (시안) · `log.md`

**기대는 개념**:

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/unique-key.md`
  — W-12 의 잣대. 앱 층 정규화와 DB 층 제약이 **같은 값**을 봐야 유일성이 성립한다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/functional-dependency.md`
  — O-5 의 잣대. 같은 사실을 여러 행에 복제하면 수정 이상이 생긴다.

## 2. 배경 — 이 작업이 어디쯤인가

SPEC-051(제품 배포·시연계정 레지스트리)의 유니크를 `(product_slug, environment)` → **`(product_slug, environment, surface_key)`** 로 넓혀 한 환경에 서비스 URL 이 여럿인 제품(`nexus` prod 6표면)을 담게 했다. 사용자 확정 2026-09-22, OQ-4 ① RESOLVED.

앞 판 planner 가 4판에 걸쳐 스펙·시안·log 를 고쳤고, **`reviewer_spec` 이 검수해 WARN(FAIL 0 · 경미 14)** 을 냈다. 네 일은 **그 14건 중 13건을 반영**하는 것이다(1건은 내가 「조치 없음」으로 처분 — §3 W-10).

**계약 축은 이미 확정됐고 건드리지 않는다**: 유니크 3축 · 계정은 surface 행마다 · `surface_key` 자유 입력 · 범위는 구조까지(nexus 실데이터 미투입) · `기본` 은 백필 값 하나(sentinel·프리필 아님) · `/gm` 표기는 그룹 행 수 판정 · PATCH 개명 허용 · NOT NULL 계약 · 빈 값 저장은 400 · 평평 카드 + 정렬.

**불변 축도 그대로**: 권한 leaf·`product_assignment` / 환경 enum 4종 / `/gm` ephemeral·3초·활성 필터 / 민감값 두 축(DB 평문·문서 미박제) / OQ-1·2·3·5·6 RESOLVED · **OQ-4 ② 는 열린 채**.

## 3. 처분 — 코디가 정했다. 이대로 반영해라

> 각 항목의 **근거·제안 세부는 리뷰 리포트의 같은 번호**에 있다. 리포트를 읽고 그 제안을 따르되, 아래에서 내가 **선택지를 고른 것**은 그 선택을 따라라.

### 1순위 — 다음 판이 실제로 걸린다

- **W-5** `/gm` 파싱 근거 문장이 **현행 카탈로그에서 거짓**(`spec-051:256`). 카탈로그에 `slug='dev'`(kind=category)가 실재한다. → 리포트 제안대로 **주장을 사실로 좁혀라**: 「등재 대상(product-kind)의 어떤 slug/label 도 환경 키워드가 아니다(category kind 에 `dev`·`qa` 가 실재하나 배포를 가질 수 없어 판정에 들어오지 않는다)」.
- **W-12** `surface_key` **trim 한 값을 저장하는지** 미명시(`:403`) → **「trim 한 값을 저장한다(앱이 정규화한 값이 곧 DB 유니크가 보는 값). 저장 후 재-trim 비교는 하지 않는다.」** 를 박아라. W-6 의 길이 상한도 **저장값 기준**임이 함께 읽히게.
- **W-1** 시안 정렬 방향이 와이어프레임과 반대 → **표시 정렬은 `prod → stg → dev → demo`** 로 확정한다(운영이 먼저). ① `spec-051` §4 FE 에 **환경 정렬 방향을 한 줄로 못박고** ② 시안 `envOrder` 를 그 순서로 바꾼다. ③ **`ENVS`(select 옵션 순서)와 `envOrder`(표시 정렬)를 같은 배열로 겸하지 마라** — 분리해라.
- **W-2** 시안이 출처 없는 say-admin 계정을 박았다 → **리포트의 (b) 를 택한다.** 시안 9번째 행의 `accts` 를 **비우고**(`accts:[]`) note 에 「가상 예시 — 실 데이터는 운영자 입력」을 적어라. 복수 surface 를 보여주는 목적은 계정 없이도 달성된다. **`spec-051:476` 은 고치지 마라**(사정거리를 넓히는 (a) 안은 탈락).

### 2순위 — 계약의 빈칸

- **W-3** `기본` 가시성 비대칭 → **`/gm` 과 같은 규칙으로 통일한다.** [기본정보] 탭 블록 요약도 **그 환경의 행이 1건뿐이면 surface 를 생략**한다. 근거: 이번 라운드의 목표가 「기존 단일 surface 제품 화면 회귀 0」이고, 한 화면만 예외면 그 목표가 반쪽이다. `spec-051:91` 과 예시 `:85-86` 을 그에 맞게 고쳐라.
- **W-6** 길이 상한 → **50자를 계약으로 확정한다**(「권장」 삭제). 케이스 매트릭스(`:316`)·AC(`:442`)가 이미 강제하고 있으니 그쪽에 맞춘다. **trim 후 저장값 기준**임을 W-12 와 묶어 명시.
- **W-7** AC 추가 — 「`GET /api/v1/deployments?product_slug=charty` 응답의 **모든 행에 `surface_key` 가 실린다**(백필 행은 `기본`)」.
- **W-8** ① AC `:450` 을 **제품 무관 문장**으로 다시 써라(nexus 는 괄호 예시로만). 지금은 「배포 후 운영자 입력」이라 출시 시점에 nexus 행이 0건이므로 실행 불가능한 AC 다. ② **전이 AC 1줄 추가** — 「2행 중 1행을 삭제하면 남은 1행의 `/gm` 카드에서 surface 표기가 사라진다」. 이게 「값이 아니라 그룹 행 수로 판정」의 증명이다.

### 3순위 — 규약·정리

- **W-9** `log.md` 종류를 **`spec-change, open-resolve`** 로. 요약 본문은 손대지 마라(이미 좋다).
- **W-4** `spec-051:185` 「환경별」 → 「배포 행별(환경 · surface)」.
- **W-14** `:63`·`:391` 의 **「17 row」 숫자를 지우고** 성질만 남겨라 — 「카탈로그 전부가 아니라 서버가 실재하는 product-kind 만」. 행 수는 코드가 SoT 다(실측 30행, 시안 frontmatter 는 18 이라 적는다 — 한 사실이 세 숫자로 살고 있다).
- **W-11** 시안 frontmatter `generated_at` 갱신 + `:15-18` summary·`:27` sections.role 의 진입점을 **[기본정보] 탭**으로. **본문 모달의 진입 흐름 재작성은 하지 마라** — 범위 밖 부채다.

### 추가 — 검수가 「부채」로 분류했지만 이번에 닫는다

- **AC 재현 불가** — 시안 `commitDeploys` 의 `if(!url) continue;` 가 surface 빈 값 검사보다 **먼저**라(`Product Management.html:562-564`), 아무것도 안 채운 신규 카드가 **400 없이 조용히 버려진다.** 그래서 AC `:443`(「[+ surface 추가] 후 그대로 저장 → 409 아니라 400」)을 시안이 재현하지 못한다. **검사 순서를 바꿔** surface 빈 값이 먼저 잡히게 해라. 이번 라운드가 AC 로 승격한 시나리오다.
- **O-4 삭제 확인이 계약에 없다** — surface 행 1건 삭제 = **그 표면의 시연계정 전부 소멸**이다. 스펙은 그 손실을 이미 안다(`:244` 가 PATCH 개명을 허용하는 근거가 「삭제 후 재생성을 강요하면 시연계정을 잃는다」였다). 같은 손실이 `[삭제]` 버튼엔 아무 방어 없이 열려 있고 §UX·§케이스 매트릭스 어디에도 확인 단계가 없다. **§UX Contract 에 「시연계정이 있는 행 삭제는 확인 단계를 거친다」를 계약으로 넣고**, 케이스 매트릭스에 대응 행을 추가해라. (시안 `:481` 의 즉시 삭제도 확인 단계를 타게 고쳐라.)
- **O-5 탈락 근거 문장이 현행 데이터와 어긋난다** — `:461` 이 대안 ⓑ 를 탈락시킨 근거가 「환경 단위 공통 속성이 없다(비고·계정 전부 표면별)」인데, 현행 seed `note` 실값은 「v0.1.0 Holding — 운영비용 이슈로 서버 내림」·「v1.1.0, 시술상품 등록완료」처럼 **환경(인스턴스) 단위 사실**이다. **결정은 그대로 두되**(사용자 확정, 되돌리지 마라) **그 근거 문장을 사실에 맞게 좁혀라** — 예: 「URL·시연계정은 표면별이다. `note` 는 현행 데이터상 환경 단위 사실이 섞여 있어 표면마다 중복 기재될 수 있다 — 이 잔여 종속은 OQ-4 ② 와 같은 층이라 그때 함께 본다」. **OQ-4 ② 항목에도 이 연결을 한 줄 남겨라.**

### W-13 — 내가 정했다. 스펙 쪽 반영만 해라

- **Spec Coverage** `products/mediness/30-work.md:247` 의 SPEC-051 **구현 상태를 `done` → `in_dev`** 로 바꿔라. 계약이 방금 늘었고 surface 축은 한 줄도 구현되지 않았는데 `done` 이면 대시보드를 보는 사람이 「다 됐다」로 읽는다. **린트가 derive 불일치 WARN 을 낼 텐데 그게 정상이다** — 같은 파일 SPEC-030 에 이미 같은 WARN 이 있고(`30-work.md:243`), 계약이 커버 WP 를 앞지른 상태를 나타내는 **선례**다. 그 WARN 이 뜨는 것을 「무관」이 아니라 **의도된 신호**로 보고해라.
- **「후속 WP」 어휘는 이번에 고치지 마라.** 리뷰어도 단독 수정을 권하지 않았다 — 문서 전반 어휘라 이 SPEC 만 고치면 또 다른 비대칭이 된다. 별건으로 남긴다.
- **Delivery Issue 개설은 코디가 한다.** 네가 `start-delivery` 를 돌리거나 `30-work/work-NNN-*.md` 를 만들지 **마라**(Harness v1 — `rules/document-pipeline.md:10`).

### W-10 — 조치 없음

frontmatter `version: 0.0.3` **그대로 둔다.** 규칙 문면(「문서를 고쳤다고 올리지 않는다」)과 mediness 실태가 갈리는데, mediness 엔 앵커가 될 `00-baseline/planning/` 디렉토리 자체가 없고 최근 판 SPEC 세 건(150·151·240)이 전부 0.0.3 이다. **관행을 따른다.** 규칙-실태 괴리는 이 작업 범위 밖이니 **건드리지 마라.**

## 4. allowed_paths

- `products/mediness/`
- `context/`

대상 4파일: `20-spec/spec-051-product-deploy-registry.md` · `21-html/Product Management.html` · `log.md` · `30-work.md`(W-13, 그 한 행만).

## 5. 하지 말 것

- **확정된 계약 축·불변 축을 건드리지 마라**(§2 목록).
- **`spec-051:476` 의 사정거리를 넓히지 마라**(W-2 의 (a) 안은 탈락).
- **W-10 version 을 건드리지 마라.**
- **「후속 WP」 어휘를 고치지 마라**(W-13).
- **`start-delivery` 실행·`30-work/work-NNN-*.md` 생성 금지.**
- **코드 레포(`mediness-app`) 수정 금지** — 읽기만.
- **시안 본문의 진입 흐름 재작성 금지**(W-11 은 frontmatter 3줄만).
- 커밋·push·PR 금지.

## 6. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- 기준선: 변경 전 **0 error / 263 warning**(4판 고정).
- **예상 결과: 0 error / 264 warning** — 늘어난 1건이 W-13 의 SPEC-051 `in_dev` derive WARN 이면 정상이다. 그 WARN 의 **전문을 보고서에 인용**해라. 다른 이유로 늘었으면 그건 문제다.
- `node --check` 로 시안 JS 문법.
- **시안 `commitDeploys` 를 실제로 돌려** 빈 surface + 빈 URL 카드가 **400 으로 잡히는지**(조용히 버려지지 않는지) 확인해라.
- 자가 점검 grep: 「17 row」 잔존 0 / 「환경별 URL·시연계정 수」 잔존 0 / `ENVS` 와 `envOrder` 가 분리됐는지.

## 7. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/planner-report.md` 에 **「5차 — 검수 지적 반영」** 절로 이어 붙여라(새 파일 금지). 지적 번호(W-1…W-14 · O-4 · O-5)마다 **고친 자리(파일:줄) 또는 「조치 없음 + 사유」**를 한 줄씩. 빠진 번호가 있으면 안 된다.

**scratchpad 에 쓰지 마라 — 네 터미널이 죽으면 같이 죽는다.** (앞 판 워커의 터미널이 실제로 죽었다.)

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이라 오래됐을 수 있다 — **이 세션에서 실제로 두 번 바뀌었다.** preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --from term_3a4cc1ce-2b87-4f61-ae01-b7252cfc2c50 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "planner 수정판 완료: <한 줄>" \
  --body "지적별 처리 결과 / 검증 수치 / 미결·주의점"

orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 \
  --text "[worker_done] planner 수정판 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고:
  `orca terminal send --terminal term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1 --text "[질문] planner: <질문>" --enter`
