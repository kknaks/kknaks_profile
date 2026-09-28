# SPEC-051 OQ-4 ① 해소 — 배포 레지스트리 surface 축 추가 결과 보고

작성: mediness `planner` · 2026-09-22
워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec` (브랜치 `kknaksss/deploy-surface-multi-spec`, base `origin/mediness`)

## 상태: done

---

## 수행 내용

### 수정 파일 (2개 — 커밋·push·PR 없음)

| 파일 | 내용 |
|---|---|
| `products/mediness/20-spec/spec-051-product-deploy-registry.md` | 본 작업의 실질 대상. surface 축 전면 정합 (+128/−64) |
| `products/mediness/log.md` | 변경 이력 표에 `2026-09-22 / spec-change / MEDINESS-SPEC-051` entry 1행 prepend |

`30-work/` 는 만들지 않았고(§7 범위 제약), 코드 레포(`mediness-app`)는 **읽기만** 했다.

### 핵심 결정 반영 — 사용자 확정 4줄을 계약으로 박음

식별 키 `(product_slug, environment)` → **`(product_slug, environment, surface_key)`**. 행 1개 = surface 1개.
근거 서술의 뼈대는 **함수종속** — 계약이 기대던 「(제품, 환경) → 서비스 URL」이 `nexus` prod(6표면)·`say` prod(say-admin)에서 깨졌으므로 결정자를 한 축 더 붙여 「(제품, 환경, surface) → 서비스 URL」을 복원한다. 문서 안에서 이 문장이 §변경노트 / §4 Functional Rule / §6 OQ-4 ① 세 곳에서 같은 결로 반복된다.

### 절별 반영

| 절 | 바뀐 것 |
|---|---|
| frontmatter | `version` 0.0.2 → **0.0.3**, `last_updated` → **2026-09-22** |
| 머리 변경 노트 | **2026-09-22 변경 노트** 신설(①~⑤ + 「바뀌지 않는 것」). 2026-07-31 노트 위에 배치(최신 우선) |
| 2026-07-31 노트 끝줄 | 「`(제품,환경)` 유니크 불변」 구절을 **supersede 표기**로 정정 (역사 보존 + 계약 분기 제거) |
| §1 Domain note | 키에 `surface_key` 추가, 「(product, environment, surface_key) 1건 = URL + 시연계정 0~N」 |
| §1 Open Questions | OQ-4 ① RESOLVED / ② 열림 반영 |
| §2 Wireframe | [기본정보] 탭 요약 줄 = 배포 행 1건(환경·surface·URL·계정수). 모달을 **환경 그룹 × 그룹 안 surface 행 N개**로 재작도 |
| §2 Wireframe `/gm` | 복수 surface 예시 블록 신설 (`/gm nexus prod` → 6카드 형태) |
| §2 U-1/U-2/U-3 · S-1 | `[+ surface 추가]` CTA 신설, 409 축 교체, 환경 소진 규칙 폐지 명시 |
| §3 API 표 + bullet | POST body에 `surface_key`, 409 조건 3축, **PATCH 대상 필드에 `surface_key` 포함**, GET 응답 행마다 `surface_key` 필수, **GET query surface 필터는 두지 않음(근거 포함)** |
| §3 `/gm` 계약 | 인자 파싱 **2토큰 유지**(근거 명시) · 응답 본문 = 행 1건 = 카드 1장 · **surface 표기 규칙** · 정렬 3키 |
| §3 Validation | `surface_key` 행 신설(비어있지 않음/길이/정규화) + 유니크 행을 3축으로 교체 |
| §3 케이스 매트릭스 | `DUPLICATE_DEPLOYMENT` 메시지·판정축 갱신, `VALIDATION_ERROR` 에 surface 사유 2종 추가 |
| §3 상태/Lifecycle | `surface_key` 단락 신설(환경과 **직교**, enum 아님, 개명 가능) |
| §4 FE Implementation | 환경 그룹 렌더 · **환경 소진 규칙 폐지** · `기본` 프리필 · 기존 행 환경 불변 |
| §4 Functional Rule | surface 축 · **`기본` 은 sentinel 아님** · surface 이름의 소유자는 운영자 |
| §4 DB | 유니크 확장 + 백필 5단계 순서 + **NOT NULL 이 계약인 이유** + 중복 판정 대소문자 규칙 + 타입/번호는 WP 이관 |
| §5 AC | surface 케이스 **11건 추가** (브리프 요구 5건 전부 포함) |
| §6 | OQ-4 를 ①(RESOLVED)/②(열림) 2행으로 분리, 탈락 대안 2종 명시 |
| §데이터/부록 | 전 8행 `surface_key=기본` 백필 노트, `say` 비고 갱신, nexus 행은 **만들지 않음** |
| §Related | 손댈 것 없음(stale 없음) — 무변경 |

### 내가 제안한 세부 (사용자 확정 밖 — 리뷰 대상)

1. **기본값 문자열 = `기본`** (ASCII `default` 아님). 근거 — `surface_key` 는 자유 입력이라 `demo`↔`시연` 같은 **표시 별칭 층이 없다**. 저장값이 곧 화면에 보이는 값이므로, 운영자가 치게 될 어휘(「고객 홈페이지」·「운영자 어드민」)와 같은 언어여야 한다. 동시에 **`기본` 을 sentinel 로 만들지 않는다**고 §4 에 못박았다 — 서버는 이 값으로 분기하지 않고, 마이그레이션 백필 + FE 프리필 두 곳에만 나타나는 평범한 리터럴이다.
2. **길이 상한 = trim 후 50자 권장**, 초과 400(`detail.max_length`). 근거 — 한글 표면명이 7~10자 수준이라 여유가 충분하고, 복합 유니크 인덱스에 들어가는 컬럼이라 무제한 Text 보다 경계가 있는 편이 낫다. 정확한 컬럼 타입은 WP 이관.
3. **정규화 = 앞뒤 공백 trim 만. 대소문자는 접지 않는다.** 근거 — collation 이 중복 판정을 바꾼다는 함정을 명시적으로 닫아 둔 것. 표시 라벨이라 서버가 표기를 고치면 운영자가 친 값을 잃고, 한글엔 대소문자가 없어 실익이 작다. 접어야 한다는 요구가 생기면 함수 인덱스(WP).
4. **GET `?surface_key` 필터 = 두지 않는다.** 근거 — 유일한 소비자(모달)가 제품 단위로 전부 받아 클라이언트에서 그룹핑하고, 한 (제품,환경)의 행 수가 한 자릿수라 필터가 줄여 줄 것이 없다. 필요해지면 후방호환 추가.
5. **`surface_key` 는 PATCH 가능** (`product_slug`·`environment` 는 여전히 불변). 근거 — 식별 키의 일부지만 본질은 **운영자가 붙인 표시 라벨**이고, 개명을 삭제+재생성으로 강요하면 그 행의 시연계정이 사라진다. 변경 결과가 같은 (제품,환경) 안 중복이면 409.
6. **`/gm` surface 표기 = 그룹 행이 2건 이상일 때만.** 근거 — **값(`기본`)이 아니라 그룹의 행 수로 판정**하므로 `기본` 이 sentinel 이 되지 않고, 기존 단일 surface 제품의 `/gm` 출력이 확장 전과 한 글자도 달라지지 않는다(회귀 0).
7. **`/gm` 인자 파싱은 2토큰 유지.** 근거 — `surface_key` 는 공백을 포함할 수 있는 자유 입력이라 3번째 토큰의 경계를 결정적으로 자를 수 없고, 환경 키워드처럼 닫힌 값 공간도 아니다. 게다가 결과가 한 자릿수라 전부 내보내는 편이 싸다.
8. **`/gm` 정렬 3키** (`slug` → `environment` → `surface_key`) — 같은 그룹 안 행 순서가 호출마다 흔들리지 않게.

---

## 검증

### lint

```
$ python3 scripts/lint-pipeline.py --strict
0 error, 263 warning        # 변경 전후 동일
```

- **mediness 범위 ERROR = 0** ✅ (변경 전 0 → 변경 후 0)
- mediness WARN = **1건, 변경 전과 동일**: `products/mediness/30-work.md:243` SPEC-030 Spec Coverage 구현 상태 `in_dev` ≠ derive `done`. **이번 작업과 무관한 기존 WARN**(SPEC-030/WP-045·089·090·113).
- 나머지 262 WARN 은 전부 **타 제품**(selly·charty·linky 등)의 기존 `doc_no`/`version` 누락 — **무관**. 총계가 변경 전후 동일하므로 신규 0건.

### 자가 점검 — 옛 표현 전수 grep

`(product_slug, environment)` / `(제품,환경)` / `제품 × 환경 = 유니크` / `환경당 1개` / `환경 블록` / `미사용 환경` / `모든 제품×환경` 전수 확인 → **SPEC-051 안에 유니크를 2축으로 말하는 문장은 남아 있지 않다.** 남은 `(product_slug, environment)` 문자열은 전부 **의도적**이다:
- 2026-09-22 변경 노트의 「`(product_slug, environment)` → `(…, surface_key)`」 전이 서술
- 2026-07-31 노트 끝줄의 supersede 표기
- §Validation 의 「`(product_slug, environment)` **만으로는 유니크가 아니다**」 (부정문)
- §4 DB 의 마이그레이션 서술(구 유니크 DROP)
- AC·`/gm` 의 「같은 `(product_slug, environment)` 안에서」 = 그룹 지시어(유니크 주장 아님)

### 참고 출처

- 규칙: `rules/document-pipeline.md`(변경 라우팅·frontmatter·log.md·한 곳 원칙), `rules/qa/llms.md`
- 선례 문체: `products/mediness/30-work/work-071-deploy-demo-env-gm.md`
- 코드(읽기만): `back/app/models/product_deployment.py`(`uq_product_deployment_slug_env`·`demo_accounts` JSONB), `back/app/schemas/deployment.py`(PATCH 가 `environment` 를 **필드 자체로 두지 않음** 확인), `back/app/routers/deployments.py`, `back/app/services/deployment.py`(409 발생 지점 = `store.exists` + `IntegrityError`), `back/app/services/gm_command.py`(`_render_cards` 정렬·`_format_deployment` 카드 포맷), `front/components/admin/products/EnvBlockCard.tsx`·`useDeployInfo.ts`(`usedEnvs` disable·`addEnvBlock` 미사용 환경 선택·`save` 사전 중복검증), `back/app/seeds/products_prod_snapshot.py`(nexus 등재 확인)

---

## 다른 팀 영향

### BE (후속 WP 에서 손댈 지점 — 이번 태스크는 문서까지)

- `product_deployment` 에 `surface_key` 컬럼 + NOT NULL + `기본` 백필, `uq_product_deployment_slug_env` → 3축 유니크 교체 (migration 번호·컬럼 타입은 WP 결정).
- `DeploymentCreateRequest` 에 `surface_key` 추가, `DeploymentUpdateRequest` 에 `surface_key` 추가(**PATCH 가능으로 계약함** — 현행은 필드 부재), `DeploymentRow` 에 `surface_key` 추가.
- `DeploymentService.create` 의 `exists(product_slug, environment)` → 3축, `update` 에 surface 중복 재검사(PATCH 개명 경로).
- `gm_command._render_cards` 정렬에 `surface_key` 추가, `_format_deployment` 헤더에 조건부 surface(그룹 행 ≥2).
- **권한·환경 enum·`/gm` 활성 필터는 손대지 않는다.**

### FE

- `EnvBlockCard` 의 `usedEnvs` disable 과 `useDeployInfo.save`/`saveBlock` 의 「같은 환경 1개」 사전검증이 **폐지 대상**이다. 중복 축이 `(환경, surface_key)` 로 바뀐다.
- `addEnvBlock` 의 「미사용 환경 자동 선택」도 성립하지 않는다(환경이 소진되지 않음).
- 렌더 구조가 flat 블록 리스트 → **환경 그룹 × 그룹 안 surface 행**으로 바뀐다.
- 기존 행의 환경 select 는 **지금도 PATCH 로 전달되지 않아 아무 효과가 없다**(실측). 계약을 읽기 전용 칩으로 명시화했다.

### 문서 (이번에 안 건드린 것 — 판단 필요)

1. **`products/mediness/21-html/Product Management.html`** — legacy 시안에 「제품 × 환경 = 유니크」 문구 3곳(269·276·518행). 구 SPEC-050 제품관리 표면 시안이라 이미 2026-07-15 편집표면 이관으로 stale 상태다. 이번 범위 밖이라 손대지 않았다. 갱신 또는 폐기 판단 필요.
2. **SPEC-052** — 배포 블록을 「참조만·데이터 모델은 SPEC-051 owns」로만 기술하므로 **정합 깨짐 없음**. 수정 불필요(확인 완료).
3. **SPEC-050 카탈로그 「17 row」** — seed 에 medi·casty·payment·homepage·nexus 5건이 추가돼 실제 수가 다르다. SPEC-051 §1·§4 에도 「카탈로그 17 row 의 subset」 표현이 남아 있으나 **surface 관심사와 무관한 기존 staleness** 라 손대지 않았다.
4. **`log.md` entry 추가 여부** — 파이프라인 규칙(§변경 라우팅)은 spec 본문 변경 PR 에 entry 1건을 요구하지만, **최근 PR(#687·#691 등)은 log entry 를 추가하지 않는 실운영 패턴**이다. 규칙 쪽을 따라 1행 넣어 두었으니, 코디네이터의 PR 플로우와 맞지 않으면 그 1행만 드롭하면 된다.

---

## 이슈 / 주의점

### ⚠️ OQ-1 과의 충돌을 「데이터 현황 갱신」으로 처리했다 (확인 요망)

브리프는 OQ-1 을 다시 열지 말라고 했고 **결정은 건드리지 않았다.** 다만 OQ-1 본문과 §부록이 「더데이랩스 홈페이지 = 카탈로그 비등재 → 제외」라고 **사실**을 적고 있었는데, `back/app/seeds/products_prod_snapshot.py` 에 `{"slug": "nexus", "label": "더데이랩스(홈페이지)", "kind": "product", "ordering": 12, "is_active": True}` 로 **등재돼 있다.** 그대로 두면 같은 문서가 「nexus prod 6표면」과 「nexus 는 레지스트리 제외」를 동시에 말하게 되어 계약이 둘로 갈린다.

처리 = **규칙 불변 / 입력 갱신**. OQ-1 규칙(「카탈로그에 실재하는 active product-kind 만 대상」)은 한 글자도 바꾸지 않고, 그 규칙의 **입력이 바뀌었다**는 사실만 2곳(OQ-1 본문·§부록 제외 문장)에 표기했다. OQ-1 본문에는 이미 「(OQ-1 결정 자체 불변 — 데이터 현황만 갱신.)」이라는 선례 문장이 있어 같은 결을 따랐다. **status 는 RESOLVED 그대로다.**

이 판단이 브리프의 「OQ-1 을 다시 열지 마라」와 어긋난다고 보면 해당 2곳만 되돌리면 된다(다른 절엔 영향 없음).

### 기타

- **`version` 0.0.2 → 0.0.3** — 브리프 지시대로 올렸다. 다만 `rules/document-pipeline.md` 는 `version` 을 「상위기획 사이클 버전 = 제품 버전, 문서를 고쳤다고 올리지 않는다」로 규정한다. mediness 에는 `00-baseline/planning/{version}-상위기획.md` 가 없고, 현행 SPEC 분포는 0.0.2 가 52건 / **0.0.3 이 3건**(SPEC-150·151·240 = 최신 사이클)이다. 즉 0.0.3 은 실재하는 사이클이므로 「이번 사이클에 다시 grounding 됐다」는 의미로 읽히며 규칙과 충돌하지 않는다. (참고: 이 필드는 과거 0.0.2→0.0.3→0.0.2 로 churn 한 이력이 있다 — 9858641e 가 올렸다가 2ee630ed 가 되돌림.)
- **nexus 실데이터 미박제** — 6개 실 URL·시연계정은 문서 어디에도 넣지 않았다. `/gm` 예시의 URL 은 전부 `https://…` 플레이스홀더이고 surface 이름 3종(「고객 홈페이지」·「운영자 어드민」·「BE API」)은 **형태 예시**로 명시했다. 비밀번호 평문 없음.
- **`/gm nexus prod`** — 브리프는 `/gm 넥서스 prod` 로 썼지만, 카탈로그 label 이 「더데이랩스(홈페이지)」라 `넥서스` 토큰은 slug/label 어느 쪽으로도 정규화되지 않는다. 예시를 **slug `nexus`** 로 바꿔 실제로 동작하는 커맨드를 박았다(카드 헤더는 실제 label 「더데이랩스(홈페이지) (nexus)」로 표기).
- **`/gm nexus prod` 의 활성 필터** — nexus 는 `is_active=True` 라 `/gm` 에 정상 노출된다(확인 완료).
- **WP 미작성** — §7 대로 `30-work/` 는 손대지 않았다. 위 「다른 팀 영향」의 BE·FE 항목이 그대로 WP 발주 입력이 된다.

---

# 2차 — 시안(21-html) 동기화

작성: 2026-09-22 (추가 지시 `planner-followup-instructions.md` 수행)

## 상태: done

대상 = **`products/mediness/21-html/Product Management.html` 한 파일** (+71/−32). spec-051 은 다시 건드리지 않았다.

---

## 고친 자리 전수 (최종 파일 기준 줄 번호)

### A. 문구 — 「제품 × 환경 = 유니크」 가정 (지시 1·2·3)

| 줄 | 무엇을 |
|---|---|
| `:16-18` | frontmatter `summary` — 「환경 블록 0~N = dev/stg/prod 서버 URL」 → 「배포 행 0~N = (환경, surface) 1조합 = dev/stg/prod/demo …, 유니크 = (제품, 환경, surface), 한 환경에 행 여러 개」 |
| `:27` | frontmatter `sections[SPEC-051].role` — 같은 취지로 교체 |
| `:271` | 모달 상단 설명 — 「환경(prod/stg/dev)별 … 제품 × 환경 = 유니크.」 → 「환경 × 표면(surface)별 … **제품 × 환경 × surface = 유니크** — 한 환경에 surface 행 여러 개.」 |
| `:278` | 경고 배너 — 「제품 × 환경 중복이면 저장 시 409.」 → 「**제품 × 환경 × surface** 가 전부 같으면 409 — 같은 환경이라도 surface 이름이 다르면 정상 저장. surface 가 비면 400.」 |
| `:443` | 시연계정 주석 — 「(환경 블록 안, 0~N 반복)」 → 「(배포 행 = (환경, surface) 안 … **계정은 surface 행마다 따로 붙는다**)」 |
| `:463-465` | `envBlockHTML` 머리 주석 — 「환경 블록 1개」 → 「배포 행 1개 = (환경, surface) 1조합」 + 「환경은 소진되지 않는다」 + 「환경만으로는 유니크가 아니다」 |
| `:531-532` | `renderEnvBlocks` 주석 — 「배포 환경 블록 prefill」 → 「배포 행 prefill … (환경 → surface) 정렬」 |
| `:549-550` | `commitDeploys` 주석 — 「제품 × 환경 중복은 인라인 경고」 → 「중복 판정 축 = **(제품, 환경, surface)**」 |
| `:582` | `openDeploy` 인라인 주석 — 「환경 블록 prefill」 → 「배포 행 prefill — (환경, surface) 조합 0~N」 |

### B. surface 입력 필드 (지시 2)

| 줄 | 무엇을 |
|---|---|
| `:484-485` | `envBlockHTML` 에 **surface 라벨 + `.env-surface` 입력** 신설. 위치 = 환경 헤더 바로 아래·서비스 URL 바로 위. 클래스는 기존 `.env-url` 입력과 **동일**(`mb-2 w-full rounded-md border border-mgray-200 px-2.5 py-1.5 text-[12px] …`), `font-mono` 만 뺌(표시 라벨이라). 새 컴포넌트·새 색·새 간격 없음 |
| `:480` | 블록 헤더 우측에 **`[+ surface 추가]`** 버튼 추가(기존 `[삭제]` 버튼과 같은 클래스·같은 `plus` 아이콘, `gap-1.5` 로 묶음) |

### C. 환경 소진 로직 제거 (지시 3)

| 줄 | 무엇을 |
|---|---|
| `:538-542` | `nextEnv()` → **`defaultEnv()`** 로 개명 + 역할 재정의. 계산식은 같지만 의미가 「소진(=더 못 고름)」 → 「**아직 안 쓴 환경을 먼저 집어 주는 편의 기본값**」이다. 주석에 「전부 쓴 뒤에도 계속 추가된다(같은 환경 중복 허용, surface 로 구분)」을 명시 |
| `:548-552` | **`addSurfaceBlock(blockEl)`** 신설 — 같은 환경의 배포 행을 **바로 아래에** 1개 더 붙인다. 이 버튼의 존재 자체가 「환경이 소진되지 않는다」의 증거 |
| `:544-546` | `addEnvBlock()` — 새 행의 `surface` 를 **`기본` 프리필**(SPEC-051 §4 FE) |
| `:533` | `renderEnvBlocks` 가 `(환경 → surface)` 로 정렬해 같은 환경 행이 붙어 보이게 함(시각적 그룹, DOM 은 평평) |

> 주의 — **원래 `<select>` 에는 `disabled` 가 없었다.** 시안의 「환경 소진」은 ① `nextEnv()` 가 안 쓴 환경만 고르는 것과 ② 저장 시 `seen.has(env)` 로 같은 환경을 거절하는 것, 두 곳에만 있었다. 둘 다 위에서 닫았다.

### D. 중복 판정 축 (지시 4·7)

| 줄 | 무엇을 |
|---|---|
| `:559` | `commitDeploys` 가 env 를 `b.dataset.env` 에서 읽도록 변경(저장 행엔 select 가 없으므로) |
| `:560` | `.env-surface` 값을 **trim 만** 해서 읽는다(대소문자는 접지 않음 — SPEC-051 §4 DB) |
| `:562` | surface 빈 값 → `VALIDATION_ERROR 400` 경고 후 스킵 |
| `:563-564` | 중복 키를 `env` → **`env + " " + surface`**(구분자는 사용자가 못 치는 NUL) 로 교체. 409 메시지도 `{slug}/{env}/{surface}` 로 |
| `:566` | 저장 행 shape 에 `surface` 포함 |

### E. 목업 데이터 (지시 5)

| 줄 | 무엇을 |
|---|---|
| `:400-401` | `DEPLOYS` 머리 주석에 「행 키 = (slug, env, **surface**) 3축」 + 「seed 8행은 전부 `surface='기본'`(sentinel 아님, 개명 가능)」 |
| `:403, 410, 413, 416, 419, 422, 425, 428` | 기존 8행 전부에 `surface:'기본'` 추가 |
| `:406-409` | **복수 surface 예시 1건 신설** — 같은 `(say, prod)` 에 `기본` + **`say-admin`** 2행 공존. 「같은 prod·다른 surface → 409 아님」을 note 에 박음 |
| `:405` | `say` 기본 행 note 에서 「say-admin = ?service=say-admin — 복수 surface(OQ-4)」 제거(이제 실제 별 행이 됐으므로 설명이 불필요) |

> **`nexus` 실데이터는 쓰지 않았다.** 복수 surface 예시를 `nexus` 대신 `say` 로 잡은 이유 — ① `nexus` 는 이 시안의 `PRODUCTS` 카탈로그 목록에 없고 추가하면 SPEC-050 스코프를 건드린다, ② `say-admin` 표면은 **이미 이 파일(구 note)과 spec-051 §부록에 커밋돼 있던 사실**이라 새로 공개되는 정보가 0이다. 비밀번호는 전 행 `masked:true` 그대로 — 평문 없음.

### F. 부수 — `demo` 환경 누락 정합 (지시 6 「시안을 스펙에 맞춘다」)

시안의 `ENVS` 가 `['dev','stg','prod']` 로 **`demo` 를 빼먹고 있었다**(2026-07-31 WP-071 이후로 stale). SPEC-051 §상태 enum 은 4종이고 실 FE 는 이미 `demo` 를 실어 배포했다 — 시안만 뒤처진 상태였다. surface 축과 별개 축이지만 같은 모달 구간이고, 이대로 두면 FE 워커가 3-env select 를 만든다.

| 줄 | 무엇을 |
|---|---|
| `:437` | `envChip` 에 `demo` 추가 — 값은 **실 FE `envChipClass` 에서 그대로 복사**(`bg-brand-50 text-brand-500 border border-brand-100`). 색을 새로 고르지 않았다 |
| `:439` | `ENVS` 에 `'demo'` 추가 |
| `:440` | `envLabel()` 신설 — 표시만 `시연`, 값은 ASCII enum(실 FE `deployEnvLabel` 과 동일) |
| `:441` | `envOrder()` 신설 — 정렬용 |
| `:459, 476, 477` | 칩·select 옵션 표시에 `envLabel` 적용 |

**이 F 절만 독립적으로 되돌릴 수 있다** — surface 축과 얽힌 곳이 없다(정렬용 `envOrder` 만 남기면 됨).

### G. 부수 — 저장된 행의 환경 불변 (지시 6)

SPEC-051 §4 FE 가 「기존 행의 환경은 불변 — PATCH 가 `environment` 를 받지 않으므로 읽기 전용 칩」이라고 계약했는데 시안은 **모든 블록에 환경 select** 를 달고 있었다. 이건 스케치 차원이 아니라 UX Contract 와 어긋나는 지점이라 시안을 스펙에 맞췄다.

| 줄 | 무엇을 |
|---|---|
| `:469-473` | `envBlockHTML` 에 `d.saved` 분기 — 저장 행은 select 없이 칩 + 「환경 불변 — 옮기려면 삭제 후 재생성」 힌트(기존 `text-[11px] text-mgray-400` 토큰), 신규 행만 select |
| `:533` | `renderEnvBlocks` 가 prefill 행에 `saved:true` 부여 |
| `:540, 550, 559` | env 읽기를 `.env-sel` → `dataset.env` 로 통일(select 유무와 무관하게 동작. `recolorEnv` 가 이미 `dataset.env` 를 동기화하고 있었다) |

---

## 검증

### lint

```
$ python3 scripts/lint-pipeline.py --strict
0 error, 263 warning        # 1차 직후와 완전히 동일
```

- **mediness ERROR 0 유지** ✅. mediness WARN 도 여전히 1건뿐이고 내용도 그대로(`30-work.md:243` SPEC-030 — 무관한 기존 건).
- `21-html` 전용 lint 규칙(`doc_no` 누락/placeholder = ERROR)도 통과 — `doc_no: MEDINESS-DOC-121` 손대지 않았다.

### JS 문법 + 동작 시뮬레이션

브라우저 없이 확인했다. 인라인 `<script>` 를 떼어 내 `node --check` → **문법 OK**. 이어서 `commitDeploys` 판정부만 DOM 스텁으로 실행:

| 케이스 | 결과 |
|---|---|
| 같은 환경 + **다른** surface 2개 | 저장 `prod/고객 홈페이지`, `prod/운영자 어드민` — **경고 없음** ✅ |
| 같은 환경 + **같은** surface 2개 | 첫 행만 저장, `이미 등재된 제품·환경·surface 입니다: nexus/prod/기본 (DUPLICATE_DEPLOYMENT 409)` ✅ |
| surface 가 공백뿐 | 저장 0건, `surface 는 비어 있을 수 없습니다 … (VALIDATION_ERROR 400)` ✅ |
| **다른** 환경 + 같은 surface | 둘 다 저장 — 환경이 다르면 같은 이름 OK ✅ |
| 한 환경에 surface 6개 (nexus prod 모양) | 6행 전부 저장, 경고 없음 ✅ |
| `demo` 환경 | 정상 저장 ✅ |

정렬도 따로 확인 — `stg/기본 → prod/고객 홈페이지 → prod/기본 → prod/say-admin → demo/기본` 처럼 **같은 환경 행이 인접**하고 순서가 결정적이다.

### 「제품 × 환경」 유니크 가정 전수 grep

```
$ grep -nE "제품 ?× ?환경([^ ×]|$)|제품, ?환경\)|\(제품,환경\)|환경당|nextEnv|usedEnvs" "products/mediness/21-html/Product Management.html"
(결과 없음)
```

파일에 남은 「제품 × 환경」 문자열은 **전부 `× surface` 가 뒤따르는 3축 표기**다(`:17`·`:27`·`:271`·`:278`·`:465`·`:549`). `환경 블록`·`환경별`·`prod/stg/dev` 같은 구 어휘도 0건.

---

## 스펙과 시안이 어긋났던 지점

1. **`demo` 환경 누락** — 시안 `ENVS` 가 3종. → **시안을 고쳤다**(위 F절, 실 FE 값 복사).
2. **저장된 행의 환경 select** — 스펙은 읽기 전용 칩. → **시안을 고쳤다**(위 G절).
3. **모달 구조: 중첩 vs 평평** — 스펙 §2 Wireframe 은 「환경 그룹 박스 **안에** surface 행 중첩」으로 그렸고, 시안은 「평평한 배포 행 카드 + (환경→surface) 정렬로 시각적 그룹 + 행 헤더의 `[+ surface 추가]`」다. **고치지 않았다** — 이유: ① 추가 지시 2·3번이 「블록에 surface 필드를 넣는다 / 같은 환경으로 블록을 여러 개」라는 평평한 모델을 전제하고 있고, ② SPEC-051 §2 Wireframe 스스로 「골격만 — 컴포넌트/경로 발명 X, **UX 세부는 WP·시안 확정**」이라 선언해 시안이 UX 세부의 권한을 갖는다. 계약(환경 소진 없음 / surface per row / 3축 유니크)은 셋 다 충족한다. 다만 스펙 §2·§4 문구에 「환경 그룹 0~N × 그룹 안 surface 행 0~N」이 꽤 구체적으로 박혀 있으니, **표현을 시안 쪽(평평 + 정렬 그룹)으로 낮출지는 코디 판단**이다.

### 스펙 쪽에 약점이 하나 보인다 (고치지 않고 보고 — 지시대로)

SPEC-051 §4 FE 가 「`[+ 환경 추가]`/**`[+ surface 추가]`** 로 만든 행의 `surface_key` 입력란은 `기본` 프리필」이라고 적었는데, **`[+ surface 추가]` 는 이미 그 환경에 행이 있는 상태에서 누르는 버튼**이다. 그 그룹에 이미 `기본` 이 있으면 프리필이 **반드시 409 를 부른다**(사용자가 반드시 고쳐 써야 함).

시안은 **스펙대로** `기본` 프리필로 구현했고, 목업에서 그대로 저장하면 409 경고가 뜬다 — 규칙을 보여 준다는 점에선 오히려 교육적이다. 다만 실 FE 에서는 성가실 수 있으니, 스펙 §4 FE 를 「`[+ 환경 추가]` = `기본` 프리필 / `[+ surface 추가]` = 빈 값(그 그룹에 `기본` 이 이미 있으면)」으로 다듬는 선택지가 있다. **내가 넣은 문장이라 스스로 고치지 않고 판단을 넘긴다.**

### 남겨 둔 것 (의도)

- **`/GM` 슬랙 응답 패널(`:148-191`)** — 손대지 않았다. `/GM 차티` 예시는 charty prod·stg 각 1행짜리라, SPEC-051 §3 의 「그룹 행이 **2건 이상일 때만** surface 표기」 규칙상 **출력이 한 글자도 바뀌지 않는 게 정답**이다. 우연히 안 건드린 게 아니라 규칙상 변경 대상이 아니다(그리고 별도 섹션이라 지시 범위 밖).
- **`.env-block` CSS 클래스명** — 의미상 이제 「배포 행」이지만 셀렉터가 10곳 넘게 걸려 있어 이름은 유지하고 주석으로 못박았다(`:465`). 유니크 가정이 아니라 명명 잔재다.
- **`summary` 의 「product 18 row」** — 카탈로그 건수(SPEC-050 소관), surface 와 무관한 기존 staleness.

---

# 3차 — 스펙을 시안에 정합

작성: 2026-09-22 (추가 지시 `planner-followup-2-instructions.md` 수행)

## 상태: done — 단, **시안 쪽에 잔여 1건**(아래 「남은 어긋남」). 지시가 21-html 금지라 손대지 않았다.

대상 = **`products/mediness/20-spec/spec-051-product-deploy-registry.md` 한 파일** (+134/−64 누적). `21-html` 은 건드리지 않았다.

---

## 처분 ② — `기본` 프리필 전수 제거

지시서가 짚은 4곳이 전부였고, 추가로 **변경 노트 1곳**이 더 있었다(지시서 grep 밖).

| 줄 | 무엇을 |
|---|---|
| `:32` | **(지시서 목록 밖 — 내가 찾음)** 2026-09-22 변경 노트 ④ — 「`기본` 은 **sentinel 이 아니다**」 → 「**sentinel 도 프리필도 아니다** — 백필 값 하나로만 쓰이고…」 |
| `:129` | Wireframe 각주 — 「신규 행의 surface 입력은 `기본` 프리필」 → 「**빈 값**으로 열리고 placeholder 로 예시만(`기본 · 고객 홈페이지 · 운영자 어드민 …`). **`기본` 을 미리 채우지 않는다** — 이미 `기본` 카드가 있는 환경에서 `[+ surface 추가]` 를 누르면 그 프리필이 **반드시 409**. 빈 값 저장은 400」 |
| `:195` | UX Contract U-2 기대 결과 — 「(`surface_key` 는 `기본` 프리필)」 삭제 → 「**두 경우 모두 `surface_key` 입력은 빈 값으로 열린다**(placeholder 로 예시만) — 빈 채로 저장하면 400」 |
| `:213` | S-1 step 2 — 「`surface_key`」 → 「`surface_key`(**직접 입력 — 빈 값이면 400**)」 |
| `:381` | Frontend Implementation — 항목 제목을 「신규 행 프리필」 → 「**신규 카드의 surface 입력은 빈 값**」으로 바꾸고 근거(409 vs 400) 포함 |
| `:394` | Functional Rule — 「확장 시 기존 행 백필 값이자 모달 신규 행의 **프리필 문자열**일 뿐」 → 「**sentinel 도 프리필도 아니다** — **오직 「모델 확장 시 기존 행 백필 값」 하나**로만 쓰인다」. sentinel 부정은 지시대로 유지 |

### 400 이 409 보다 나은 실패라는 근거 (지시대로 한 줄 남김)

`:129`·`:381` 두 곳에 박았다 — **빈 값 → 400 「이름을 지어라」** 는 운영자가 무엇을 해야 하는지 바로 알려주는 실패다. 반면 `기본` 프리필 → **409 「이미 등재된 제품·환경·surface」** 는 *운영자가 아무것도 입력하지 않았는데* 중복 충돌을 던지는 것이라, 원인(내가 이름을 안 지었다)과 메시지(중복이다)가 어긋난다. 같은 막힘이라도 앞쪽이 고치기 쉽다.

### 관련 AC

프리필을 **전제한** AC 는 없었다(기존 `surface_key` 빈 값 400 AC 는 그대로 유효). 대신 **3건 신설**:

| 줄 | AC |
|---|---|
| `:443` | 신규 카드의 surface 입력이 빈 값으로 열린다 — 이미 `기본` 카드가 있는 환경에서 `[+ surface 추가]` 후 그대로 저장 → **409 가 아니라 400** |
| `:444` | `[+ surface 추가]` 카드는 누른 카드의 환경을 물려받고 바로 아래 삽입 / `[+ 환경 추가]` 카드는 맨 뒤 + 환경 선택 가능 |
| `:445` | 저장된 카드의 환경은 편집 불가(칩만), 같은 카드의 `surface_key` 는 편집 가능 |

---

## 처분 ① — §2 Wireframe 을 평평 카드 구조로 내림

| 줄 | 무엇을 |
|---|---|
| `:96-131` | **Wireframe ASCII 전면 재작도** — 「환경 그룹 박스 안에 surface 행 박스 중첩」 → **평평한 카드 나열**. 카드 1장 = `(환경, surface)` 1조합, 카드마다 환경 칩·`[+ surface 추가]`·`[삭제]`. 저장 카드(`[prod] 환경 불변`)와 신규 카드(`[dev ▾] 신규`, surface 빈 칸 + placeholder 줄)를 시각적으로 구분해 그렸다 |
| `:126` | 각주 신설 — 「**중첩 없음 — 카드가 평평하게 나열된다.** 같은 환경 카드가 붙어 보이는 것은 그룹 컨테이너가 아니라 **정렬**(환경 → surface) 결과다」 |
| `:127-128` | 두 버튼의 차이를 평평 구조 기준으로 재정의(아래 별도 절) |
| `:181` | UX Contract intro — 「환경 그룹 0~N × 그룹 안 surface 행 0~N」 → 「배포 행 카드 0~N — 카드 1장 = (환경, surface) 1조합」 |
| `:188` | U-1 기대 결과 — 「환경 그룹 + 그룹 안 surface 행 prefill」 → 「배포 행 카드 prefill — 환경 → surface 순 정렬」 |
| `:192` | U-2 상태 — 「환경 그룹 0~N × 그룹 안 surface 행 0~N」 → 「배포 행 카드 0~N + 카드별 시연계정」 |
| `:193` | U-2 문구 — 「환경 그룹마다 / 그룹 안 surface 행마다」 → 「**평평한 카드 나열**이고(중첩 컨테이너 없음) 같은 환경 카드는 정렬로 붙어 보인다. 카드마다 환경 칩 — **저장 카드는 칩만(환경 불변), 신규 카드만 select** —」 |
| `:194` | U-2 CTA — 「환경 그룹별 `[+ surface 추가]` · surface 행별 `[삭제]`」 → 「**카드별** `[+ surface 추가]`·`[삭제]`」 |
| `:213` | S-1 step 2 — 「(새 환경 그룹) / (이미 있는 환경 그룹에 행 1개)」 → 「(맨 뒤에 새 카드, 환경 선택 가능) / (그 카드 아래에 환경을 물려받은 카드)」 |
| `:378` | §4 컴포넌트 — 「환경 그룹 0~N × 그룹 안 surface 행 0~N 반복」 → 「**배포 행 카드 0~N 을 평평하게 반복**(… **그룹 컨테이너 컴포넌트를 두지 않는다**)」 |
| `:380` | §4 **`[+ 환경 추가]` vs `[+ surface 추가]` 항목 신설**(아래) |
| `:383` | §4 상태 — 「`environment` 로 **그룹핑**하고 그룹 안에서 정렬」 → 「`(environment → surface_key)` 순으로 **정렬만** 해서 평평하게 렌더 — 인접은 **정렬 결과이지 DOM 그룹이 아니다**」 |

### 두 버튼의 차이 (시안 `addEnvBlock`/`addSurfaceBlock` 실제 동작을 읽고 그대로 적음)

시안 코드를 확인한 결과 —

- `addEnvBlock()` → `insertAdjacentHTML('beforeend', …)` + `defaultEnv()`, `saved` 없음 → **목록 맨 뒤**에 카드 1장, **환경 select 있음**. `defaultEnv()` 는 아직 안 쓴 환경을 먼저 집어 주고 없으면 `prod` — **소진 규칙이 아니라 편의 기본값**.
- `addSurfaceBlock(blockEl)` → `blockEl.dataset.env` 를 읽어 `insertAdjacentHTML('afterend', …)`, `saved` 없음 → **누른 카드 바로 아래**에 카드 1장, 환경을 **물려받되** 신규 카드라 **select 는 살아 있어 바꿀 수 있다**.

이 두 문장을 `:127-128`(Wireframe 각주)·`:195`(U-2 기대 결과)·`:380`(§4 FE)에 같은 내용으로 박았다.

### 저장된 행 환경 불변 (지시 마지막 항목 — 확인 결과 이미 있었음)

2차에서 이미 반영돼 있었다 — §4 FE `:382` 「기존 행의 환경은 불변 — PATCH 가 `environment` 를 받지 않으므로… 읽기 전용 칩으로 두고, 옮기려면 삭제 후 재생성」 + Wireframe 각주 `:131`. 이번 판에 **U-2 문구(`:193`)와 AC(`:445`)에도 추가로 박아** 세 자리에서 같은 말을 하게 했다.

---

## 검증

### lint

```
$ python3 scripts/lint-pipeline.py --strict
0 error, 263 warning        # 1차·2차와 완전히 동일
```

mediness ERROR 0 유지, mediness WARN 도 여전히 1건(`30-work.md:243` SPEC-030 — 무관한 기존 건).

### `기본` 프리필 의미 잔존 grep

```
$ grep -n "프리필\|prefill" products/mediness/20-spec/spec-051-product-deploy-registry.md
```

남은 것은 **전부 부정문**(`:32` 「프리필도 아니다」, `:129`·`:381` 「미리 채우지 않는다」, `:394` 「미리 채워 넣지도 않는다」)과 **다른 의미의 `prefill`**(`:188`·`:192` — 저장된 데이터를 폼에 싣는다는 뜻, 비번은 prefill 안 함)뿐이다. **「신규 행에 `기본` 을 채운다」는 서술은 0건.**

`기본` 이라는 값 자체가 남은 자리는 ① 백필 값(`:32`·`:397`·`:469` §부록) ② `/gm` surface 표기 규칙의 sentinel 부정 예시(`:259`) ③ placeholder 예시 문자열 — 전부 의도한 용법이다.

### 스펙 ↔ 시안 대조 전수

`21-html` 의 실제 목업 동작과 스펙 §2·§4 모달 서술을 한 줄씩 맞춰 봤다.

| 계약 | 시안 실제 | 결과 |
|---|---|---|
| 평평한 카드 나열, 그룹 컨테이너 없음 | `#dDeployBlocks` 에 `.env-block` 평평 나열 | ✅ |
| 정렬 = 환경 → surface | `renderEnvBlocks` 의 `envOrder` + `localeCompare('ko')` | ✅ |
| `[+ 환경 추가]` = 맨 뒤 + 환경 select + 초기값(안 쓴 환경 else prod) | `addEnvBlock` → `beforeend`, `defaultEnv()`, `saved` 없음 | ✅ |
| `[+ surface 추가]` = 바로 아래 + 환경 물려받음 + select 살아 있음 | `addSurfaceBlock` → `afterend`, `dataset.env`, `saved` 없음 | ✅ |
| **신규 카드 surface = 빈 값 + placeholder** | `addEnvBlock`/`addSurfaceBlock` 이 `surface:'기본'` 을 넘김 | ❌ **어긋남 — 아래** |
| 저장 카드 환경 불변(칩만, select 없음) | `saved:true` → 힌트 + select 미렌더 | ✅ |
| 유니크 3축 / 셋 다 같을 때만 409 | `commitDeploys` 키 = `env + NUL + surface` | ✅ |
| surface 빈 값 → 400 | `commitDeploys` → `VALIDATION_ERROR 400` 분기 | ✅ |
| 카드 = surface + URL + 시연계정 0~N + 비고 | `envBlockHTML` 필드 순서 동일 | ✅ |
| 환경 = dev/stg/prod/시연 | `ENVS` 4종 + `envLabel` | ✅ |
| 빈 상태 문구 「배포정보 없음 — [환경 추가]로 등록」 | `dDeployEmpty` 동일 문자열 | ✅ |
| placeholder 문구 | `기본 · 고객 홈페이지 · 운영자 어드민 …` 동일 | ✅ |
| 409/400 **인라인** 표시 | 시안은 `alert()` | △ 의도한 비정합(아래) |

---

## 남은 어긋남 — **21-html 2줄**(지시가 금지해 손대지 않음)

**코디의 ② 판단 근거에 사실 하나가 빠져 있다.** 지시서는 「시안의 surface 입력은 `value="${d.surface||''}"` = 빈 값 + placeholder」라고 읽었는데, 그건 **템플릿이 `d.surface` 를 안 받았을 때**의 동작이다. 실제로는 2차에서 **내가 스펙(당시 「`기본` 프리필」)에 맞추느라** 두 호출부에 `surface:'기본'` 을 넘겼다. 즉 **지금 시안은 `기본` 을 프리필한다.**

```
products/mediness/21-html/Product Management.html
:542  // 주석 — "surface 는 `기본` 프리필(그대로 저장 가능·고쳐 써도 됨, SPEC-051 §4 FE)"
:544  envBlockHTML({env:defaultEnv(), surface:'기본'})   ← surface:'기본' 제거 필요
:550  envBlockHTML({env, surface:'기본'})                ← surface:'기본' 제거 필요
```

`surface:'기본'` 만 빼면 `d.surface` 가 `undefined` → 템플릿의 `${d.surface||''}` 가 빈 값을 렌더하고 placeholder 가 보인다. **정확히 코디가 서술한 그 동작**이 된다. 주석 1줄도 함께 고치면 3줄.

이번 판 지시가 「**21-html 은 이번에 건드리지 마라**」라 **손대지 않았다.** 다만 이 상태로는 이번 판의 검증 기준(「스펙 §2·§4 가 시안 실제 동작과 어긋나는 자리가 하나도 없는지」)을 **이 1건이 통과 못 한다** — 스펙은 「빈 값」, 시안은 「`기본` 프리필」이다. 4차 micro-task 로 지시하든 코디가 직접 2줄 지우든, 판단을 넘긴다.

### △ 의도한 비정합 1건 (고치지 않는 게 맞다고 봄)

**에러 표시가 시안은 `alert()`, 스펙·실 FE 는 인라인.** 시안은 surface 축 도입 **이전부터** 환경 중복을 `alert` 으로 처리하고 있었고(목업 편의), 실 FE(`useDeployInfo.patchBlock({error})` → `EnvBlockCard` 의 `block.error` 렌더)는 **인라인**이다. 즉 계약(인라인)이 맞고 시안이 목업 단축을 쓴 것이라, **스펙을 `alert` 으로 내리면 오히려 틀린다.** 스펙 §2 각주·§케이스 매트릭스의 「인라인」은 그대로 두었다.

### 부수 — 내 1차 `log.md` entry 1구절 정정

`products/mediness/log.md:18`(1차에 내가 넣은 미머지 entry)의 요약이 「FE 는 … **환경 그룹 안 surface 행 N개**로」라고 이번에 폐기된 구조를 말하고 있었다. 같은 브랜치의 내 entry라 「**(환경 → surface) 정렬의 평평한 배포 행 카드 N장**으로」로 정정했다(1구절). 지시의 「spec-051 한 파일」은 21-html 금지가 요지라 읽었고, 그대로 두면 원장이 스펙과 다른 구조를 말하게 된다. 불필요하다고 보시면 그 구절만 되돌리면 된다.

---

# 4차 — 시안 호출부 정합 (micro)

작성: 2026-09-22 (추가 지시 `planner-followup-3-instructions.md` 수행)

## 상태: done — **스펙↔시안 12/12 일치**

대상 = **`products/mediness/21-html/Product Management.html` 한 파일** (+2/−0 net, 실질 4줄). `spec-051` 은 건드리지 않았다.

---

## 고친 자리 (전수)

| 줄 | 무엇을 |
|---|---|
| `:545` | `addEnvBlock` — `envBlockHTML({env:defaultEnv(), surface:'기본'})` → **`envBlockHTML({env:defaultEnv()})`**. `d.surface` 가 `undefined` 가 되어 템플릿 `value="${d.surface||''}"` 가 빈 값을 렌더한다 |
| `:552` | `addSurfaceBlock` — `envBlockHTML({env, surface:'기본'})` → **`envBlockHTML({env})`** |
| `:542-543` | `addEnvBlock` 주석 — 「surface 는 `기본` 프리필(그대로 저장 가능·고쳐 써도 됨)」 → 「목록 맨 뒤에 배포 행 1개(환경 select 있음). surface 는 **빈 값**으로 열리고 placeholder 가 예시를 보여준다 — **`기본` 을 프리필하지 않는다**(이미 `기본` 행이 있는 환경이면 반드시 409). 빈 채로 저장하면 400 『비어 있지 않음』」 |
| `:549` | **(지시 목록 밖 — 내가 찾음)** `addSurfaceBlock` 주석에 같은 사실 1줄 추가 — 「surface 는 여기서도 **빈 값**(프리필 없음) — 이 버튼은 그 환경에 행이 이미 있을 때 누르므로 프리필이 곧 409 다」. `:542` 만 고치면 두 버튼 중 하나에만 근거가 붙어, 나중에 읽는 사람이 `addSurfaceBlock` 쪽은 규칙이 다른 줄 알 수 있다 |

`defaultEnv()` 는 지시대로 **그대로 뒀다.**

### 전수 확인 — 내가 다시 훑은 결과

지시서가 준 3곳이 **실제로 전수였다**(+ 대칭용 `:549` 주석 1줄). 근거:

- **`envBlockHTML(` 호출부 전수 = 3곳** — `:533`(저장 행, `{...d, saved:true}` 로 **실제 저장 데이터**를 펼침 — 정상), `:545`, `:552`. 리터럴 `surface:` 를 넘기던 곳은 뒤 둘뿐이었고 둘 다 걷었다.
- **`surface:'기본'` 리터럴 잔존 = 9곳, 전부 `DEPLOYS` seed 행**(`:403`~`:428`) — 이건 **백필 값**이라 남아야 한다(프리필이 아니다). `:407` 은 `surface:'say-admin'`(복수 surface 예시).
- **`prefill` 이라는 단어가 남은 2곳**(`:527`·`:583`)은 「저장된 데이터를 폼에 싣는다」는 **다른 의미**다(스펙 `:188`·`:192` 와 같은 용법). 비번은 prefill 안 함도 그대로.

---

## 검증

### lint

```
$ python3 scripts/lint-pipeline.py --strict
0 error, 263 warning        # 1·2·3차와 완전히 동일
```

mediness ERROR 0, mediness WARN 1건(`30-work.md:243` SPEC-030 — 무관한 기존 건).

### JS 문법 + 렌더 결과 확인

`node --check` → **문법 OK**. 이어서 `envBlockHTML` 을 실제로 실행해 렌더 결과를 뜯어봤다(주석을 믿지 않고 산출물을 봤다):

| | surface `value` | placeholder | 환경 select | 「환경 불변」 힌트 |
|---|---|---|---|---|
| **신규 카드** `envBlockHTML({env:'prod'})` | `""` ✅ | `기본 · 고객 홈페이지 · 운영자 어드민 …` ✅ | 있음 ✅ | 없음 ✅ |
| **저장 카드** `envBlockHTML({…, saved:true})` | `"기본"` ✅ | — | **없음** ✅ | 있음 ✅ |

`commitDeploys` 6케이스 시뮬레이션도 재실행 — 2·3차와 동일하게 전부 통과(같은환경+다른surface 저장 / 같은surface 409 / 빈값 400 / 다른환경 같은이름 저장 / 한환경 6surface 저장 / demo 저장).

### 스펙 ↔ 시안 12항목 대조 — **12/12**

| # | 계약 | 시안 실제 | 결과 |
|---|---|---|---|
| 1 | 평평한 카드 나열, 그룹 컨테이너 없음 | `#dDeployBlocks` 에 `.env-block` 평평 나열 | ✅ |
| 2 | 정렬 = 환경 → surface | `renderEnvBlocks` `envOrder` + `localeCompare('ko')` | ✅ |
| 3 | `[+ 환경 추가]` = 맨 뒤 + 환경 select + 초기값(안 쓴 환경 else prod) | `:545` `beforeend` + `defaultEnv()`, `saved` 없음 | ✅ |
| 4 | `[+ surface 추가]` = 바로 아래 + 환경 물려받음 + select 살아 있음 | `:552` `afterend` + `dataset.env`, `saved` 없음 | ✅ |
| 5 | **신규 카드 surface = 빈 값 + placeholder** | 렌더 결과 `value=""` + placeholder | ✅ **이번에 닫힘** |
| 6 | 저장 카드 환경 불변(칩만, select 없음) | `saved:true` → 힌트 + select 미렌더 | ✅ |
| 7 | 유니크 3축, 셋 다 같을 때만 409 | `commitDeploys` 키 = `env + NUL + surface` | ✅ |
| 8 | surface 빈 값 → 400 | `commitDeploys` `VALIDATION_ERROR` 분기 | ✅ |
| 9 | 카드 필드 순서 = surface → URL → 시연계정 → 비고 | `envBlockHTML` 렌더 순서 동일 | ✅ |
| 10 | 환경 = dev/stg/prod/시연 | `ENVS` 4종 + `envLabel` | ✅ |
| 11 | 빈 상태 문구 | 두 파일 **문자열 동일** — `배포정보 없음 — [환경 추가]로 등록` | ✅ |
| 12 | placeholder 문구 | 두 파일 **문자열 동일** — `기본 · 고객 홈페이지 · 운영자 어드민 …` | ✅ |

> △ **에러 표시(alert vs 인라인)** 는 3차 판단 그대로 유지 — 시안은 surface 축 도입 이전부터 `alert` 을 쓰던 목업 단축이고, 실 FE(`useDeployInfo` → `EnvBlockCard` 의 `block.error`)는 인라인이다. **계약(인라인)이 맞고 시안이 약식**이라 스펙을 내리지 않았다. 12항목에 넣지 않은 이유도 같다 — 계약 축이 아니라 목업 표현이다.

### `기본` 이 프리필 의미로 남은 자리 — **스펙·시안 양쪽 0건**

| 파일 | 남은 「프리필」 언급 | 성격 |
|---|---|---|
| `21-html` | `:543`·`:549` | **전부 부정문**(「프리필하지 않는다」·「프리필 없음」) |
| `spec-051` | `:32`·`:129`·`:381`·`:395` | **전부 부정문**(「프리필도 아니다」·「미리 채우지 않는다」·「미리 채워 넣지도 않는다」) |

실제로 값을 미리 채우는 코드·서술은 양쪽 모두 **0건**. `기본` 이 값으로 남은 자리는 ① `DEPLOYS` seed 9행 중 8행(백필) ② 스펙 §부록·§4 DB 의 백필 서술 ③ placeholder 예시 문자열 ④ `/gm` sentinel 부정 예시 — 전부 의도한 용법이다.

---

## 이번 판에서 새로 나온 어긋남

**없다.** 스펙 쪽에서 틀린 자리도 나오지 않았다(있었으면 고치지 않고 보고했을 자리다).

## 4판 누적 — 최종 변경 파일 3개

| 파일 | 변화 | 내용 |
|---|---|---|
| `products/mediness/20-spec/spec-051-product-deploy-registry.md` | +134/−64 | surface 축 계약(1차) + 프리필 제거·평평 구조(3차) |
| `products/mediness/21-html/Product Management.html` | +73/−32 | 시안 surface 축 동기화(2차) + 호출부 프리필 제거(4차) |
| `products/mediness/log.md` | +1 | `spec-change` entry 1행(1차, 3차에 1구절 정정) |

전 판 통틀어 `lint --strict` = **0 error / 263 warning 고정**(mediness ERROR 0, 신규 WARN 0). 커밋·push·PR 없음 — 워크트리에 변경만 남겼다.

---

# 5차 — 검수 지적 반영 (2026-09-22)

`reviewer_spec` WARN 판정(FAIL 0 · 경미 14)에 대한 코디 처분 13건 + 검수가 「부채」로 분류했으나 이번에 닫기로 한 3건을 반영했다. **계약 축·불변 축은 한 줄도 건드리지 않았다.**

## 지적별 처리 — 빠진 번호 없음

| # | 처리 | 고친 자리 |
|---|---|---|
| **W-1** | 반영 | ① `spec-051:386` 신설 — §4 FE 에 **「표시 정렬 방향」** 불릿(`prod → stg → dev → demo`, 운영이 먼저). 같은 불릿이 **select 옵션 순서와 별개 축**임을 명시하고 `/gm` 정렬(§3)은 소비 surface 가 달라 각자 소유함을 밝힘. ② 시안 `Product Management.html:443` 에 **`ENV_DISPLAY_ORDER = ['prod','stg','dev','demo']` 신설**, `:445` `envOrder` 가 이 배열을 본다. `ENVS`(`:440`)는 **select 옵션 순서 전용**으로 남아 둘이 분리됐다. 실측: charty 2행 → `prod/기본 → stg/기본`(와이어프레임과 일치, 회귀 해소) |
| **W-2** | 반영 — **(b) 안** | 시안 `:408-410` 9번째 행 `accts:[{label:'운영자', …}]` → **`accts:[]`**. 같은 줄 주석 + note 를 「가상 예시 — 실 데이터는 운영자 입력」으로. **`spec-051` 의 「git 에 박지 않는다」 문장(현 `:484`)은 손대지 않았다**((a) 안 탈락) |
| **W-3** | 반영 — **`/gm` 과 통일** | `spec-051:85-86` 와이어프레임 예시에서 `· 기본` 제거(charty 2행은 각 환경 1행뿐 → 미표기). `:91-92` 에 「요약 한 줄 = 환경 **[· surface]**」 + **표기 규칙은 `/gm` 과 같다**(그룹 행 2건 이상일 때만, 값이 아니라 행 수로 판정) 불릿 신설. `:186` U-1 상태 문구에도 같은 규칙 포인터 |
| **W-4** | 반영 | `spec-051:186`(구 `:185`) 「환경별 URL·시연계정 수 요약」 → **「배포 행별(환경 · surface) URL·시연계정 수 요약」**. 문서 전체에 「환경별 URL」 잔존 **0건** |
| **W-5** | 반영 | `spec-051:258`(구 `:256`) 주장을 사실로 좁힘 — 「**등재 대상(product-kind)** 의 어떤 slug/label 도 환경 키워드가 아니다」 + 괄호로 「category kind 에 `dev`·`qa` 가 **실재**하나 서버가 없어 배포를 가질 수 없어 판정에 들어오지 않는다」 + **「제품 정규화를 카탈로그 전체로 조회하면 안 되는 이유가 이것」**을 덧붙여 구현자가 틀리게 읽을 여지를 닫음 |
| **W-6** | 반영 — **50 을 계약으로 확정** | `spec-051:302`(Validation) 「50자(trim 후) **권장**」 → **「50자 — 계약(trim 후 저장값 기준)」**. `:409`(구 `:404`)의 WP 이관 목록에서 「길이 상한 구현」을 빼고 「컬럼 타입(상한 50 을 어느 타입으로 표현할지)」로 바꿔 **상한값 50 의 소유자가 §Validation 임**을 명시. 케이스 매트릭스·AC 와 반쪽 상태 해소 |
| **W-7** | 반영 | AC 신설 — 「**GET 응답 행마다 `surface_key`** — `GET …?product_slug=charty` 응답의 모든 행에 `surface_key` 가 실린다(백필 행은 `기본`). PATCH round-trip(개명)의 전제」 (`spec-051:455` AC) |
| **W-8** | 반영 | ① 구 `:450` AC 를 **제품 무관 문장**으로 재작성 — 「임의의 (제품, 환경)에 surface 행이 **2건 이상**이면 … 행 수만큼 카드 … (예: nexus prod 6행이면 6카드)」(nexus 는 괄호 예시로 강등). ② **전이 AC 신설** — 「2행 중 1행을 삭제하면 남은 1행의 `/gm` 카드에서 surface 표기가 **사라진다**. 남은 행의 `surface_key` 값은 그대로 — 표기는 값이 아니라 **그룹의 행 수**로 판정한다」 (`spec-051:459`) |
| **W-9** | 반영 | `log.md:18` 종류 `spec-change` → **`spec-change, open-resolve`**. **요약 본문 무변경**(지시대로) |
| **W-10** | **조치 없음 — 의도적** | `spec-051:9` frontmatter `version: 0.0.3` 그대로. 코디 처분 = mediness 관행(최근 SPEC 150·151·240 전부 0.0.3, `00-baseline/planning/` 디렉토리 부재)을 따른다. 규칙-실태 괴리는 이 작업 범위 밖 |
| **W-11** | 반영 — frontmatter 3줄만 | 시안 `:15-16` summary 진입점 → **「개인 스페이스 ▸ 제품 ▸ [기본정보] 탭(SPEC-052)의 배포 정보 블록 [배포정보 수정](2026-07-15 진입점 이관, SPEC-051 §2 Placement)」**, `:29` `sections[1].role` 동일 교체, `:35` `generated_at: 2026-06-12 → 2026-09-22`. **본문 모달의 진입 흐름은 재작성하지 않았다**(지시대로 — 범위 밖 부채) |
| **W-12** | 반영 | `spec-051:407` 에 불릿 신설 — 「**trim 한 값을 저장한다**(앱이 정규화한 값이 곧 DB 유니크가 보는 값). 저장 후 재-trim 비교는 하지 않는다」 + 누수 근거(유니크는 DB 가 **저장된 바이트**로 판정하므로 원문 저장 시 `기본`·`기본␣` 이 둘 다 통과) + **「길이 상한 50자도 저장값 기준」**. 이어지는 중복 판정 줄도 「trim 후 저장된 원문 비교」 → 「**저장된 값 그대로 비교**」로 모호성 제거. `:302` Validation 행에도 「trim 한 값을 저장한다」 동기 |
| **W-13** | 반영 — 스펙 쪽만 | `30-work.md:247` SPEC-051 Spec Coverage 구현 상태 **`done` → `in_dev`**. 「후속 WP」 어휘는 **고치지 않았다**(지시대로 — 문서 전반 어휘). `start-delivery` 미실행 · `30-work/work-NNN-*.md` 미생성 |
| **W-14** | 반영 | `spec-051:63` · `:395`(구 `:391`) 의 **「17 row」 숫자 삭제**, 성질만 — 「카탈로그 **전부가 아니라 서버가 실재하는 product-kind 만**」 + 「행 수는 코드가 SoT — 문서에 박지 않는다」. 문서 내 「17 row」 잔존 **0건** |
| **O-4** | 반영 (부채 → 이번에 닫음) | ① `spec-051:197` §UX U-2 에 **계약 불릿 신설** — 「**시연계정이 1건 이상 딸린 행의 `[삭제]` 는 확인 단계를 거친다**」 + 확인 문구가 말해야 할 것(어느 (환경·surface) 행인지 + 계정 N건이 함께 사라진다) + 근거(`:246` 이 PATCH 개명을 허용한 바로 그 손실) + 계정 0건 행은 확인 불필요 + 확인 UI 형태는 WP·시안. ② §케이스 매트릭스에 **`DELETE_CONFIRM_REQUIRED` 행 추가**(`:323`). ③ **AC 1줄 추가**(`:458`) — 취소 시 `DELETE` 미발행. ④ 시안 `:489` `onclick="…remove()"` → **`removeEnvBlock(this.closest('.env-block'))`**, `:563-572` 에 계정 수를 세어 `confirm()` 하는 함수 신설(계정 0건은 즉시 삭제) |
| **O-5** | 반영 — **결정은 그대로, 근거 문장만 사실에 맞게 좁힘** | `spec-051:469` OQ-4 ① 의 대안 ⓑ 탈락 근거에서 「환경 단위 공통 속성이 **없다**」를 걷어내고 — 「**URL·시연계정은 표면별이라 그 자리로 올라가지 않는다. 다만 `note` 는 다르다** — 현행 실값이 「v0.1.0 Holding — 운영비용 이슈로 서버 내림」처럼 **환경(인스턴스) 단위 사실**이라 표면마다 중복 기재된다(6표면이면 6번 적고 6번 고친다 = **수정 이상**). **이 잔여 종속을 알고도 ⓑ 를 택하지 않는다** — 조인 비용을 `note` 한 컬럼 때문에 치를 단계가 아니고, OQ-4 ② 와 **같은 층**이라 그때 함께 본다」. ② **OQ-4 ② 항목(`:470`)에 연결 한 줄** 추가 — 「함께 볼 것 — ① 이 남긴 잔여 종속: `note` 의 자리도 ② 를 닫을 때 같이 정한다」 |
| **부채 — AC 재현 불가** | 반영 (이번에 닫음) | 시안 `commitDeploys`(`:578-581`) **검사 순서 교체** — `if(!url) continue;` 가 surface 빈 값 검사보다 **먼저**여서 아무것도 안 채운 신규 카드가 400 없이 조용히 버려지던 것을, **surface 검사를 앞으로** 옮겼다. 이유를 주석으로 박음(AC 「[+ surface 추가] 후 그대로 저장 → 409 아니라 400」 재현). 덤으로 빈 URL 도 `continue` 스킵이 아니라 **400 alert** 로 바꿨다 — `spec-051` §Validation 이 `service_url` 을 「비어 있지 않음」으로 이미 계약하고 있어 조용한 스킵이 계약과 어긋났기 때문 |

## 검증

### lint

```
$ python3 scripts/lint-pipeline.py --strict
exit 0 — 0 error, 264 warning
```

- 기준선(4판 고정) = 0 error / **263** warning → 이번 **264**. 늘어난 **정확히 1건**이 W-13 이 의도한 신호다:

```
[WARN] products/mediness/30-work.md:247: MEDINESS-SPEC-051 Spec Coverage 구현 상태 'in_dev'
       ≠ covering WP 에서 derive 한 'done'
       (covering: MEDINESS-WP-058=done, MEDINESS-WP-071=done, MEDINESS-WP-073=done, MEDINESS-WP-087=done)
```

- **이 WARN 은 「무관」이 아니라 의도된 신호다.** 계약이 커버 WP 를 앞지른 상태(계약은 2026-09-22 에 늘었고 surface 축은 한 줄도 구현되지 않음)를 대시보드가 `done` 으로 말하지 않게 만든 결과이고, 린트는 「계약이 커졌는지」를 구조적으로 모르므로 derive 불일치로만 나타날 수밖에 없다. 같은 파일 `:243` 에 **SPEC-030 이 이미 같은 형태의 WARN** 을 갖고 있어 선례도 있다.
- mediness 범위 **ERROR 0**. `spec-051` · `log.md` · `21-html` 에 걸린 WARN **0건**. 나머지 262 WARN 은 전부 타 제품(selly·charty·linky 등)의 기존 `doc_no`/frontmatter 누락 — 무관.

### 시안 JS

- `node --check` — `<script>` 블록 2개(`:46-54`, `:290-620`) 전부 통과.
- **`commitDeploys` 실행 검증**(DOM shim 으로 카드 3장 투입):

```
입력: [prod/기본/URL 있음] · [prod/빈 surface/빈 URL] · [stg/기본/빈 URL]
출력 alert:
  · surface 는 비어 있을 수 없습니다: charty/prod (VALIDATION_ERROR 400)
  · 서비스 URL 은 비어 있을 수 없습니다: charty/stg/기본 (VALIDATION_ERROR 400)
저장된 행: ["prod/기본"]
```

→ 아무것도 안 채운 신규 카드가 **400 으로 잡힌다**(조용히 버려지지 않음). AC 재현 가능해짐.

- **정렬 검증**: `[stg/기본, prod/기본, dev/기본, prod/운영자 어드민]` → `prod/기본 → prod/운영자 어드민 → stg/기본 → dev/기본`. 와이어프레임과 일치.

### 자가 점검 grep

| 항목 | 결과 |
|---|---|
| `spec-051` 내 「17 row」 | **0건** |
| `spec-051` 내 「환경별 URL」 | **0건** |
| `ENVS` ↔ `envOrder` 분리 | **분리됨** — `ENVS`(`:440`, select 옵션) / `ENV_DISPLAY_ORDER`(`:443`, 표시 정렬), `envOrder` 는 후자만 참조 |
| `spec-051:484`(구 `:476`) 사정거리 | **무변경** — 「본 표·git 에 박지 않는다」 그대로 |
| 시안 say-admin 행 `accts` | **`[]`** — 지어낸 계정 제거 |
| frontmatter `version` | **`0.0.3` 그대로** |

## 변경 파일 4개 (커밋·push·PR 없음)

| 파일 | 변화 |
|---|---|
| `products/mediness/20-spec/spec-051-product-deploy-registry.md` | +212/−… (누적) — W-3·4·5·6·7·8·12·14 · O-4 · O-5 |
| `products/mediness/21-html/Product Management.html` | +126/−… (누적) — W-1·2·11 · O-4 · commitDeploys 순서 |
| `products/mediness/30-work.md` | 1행 — W-13 Spec Coverage `done → in_dev` |
| `products/mediness/log.md` | 1행 — W-9 종류 `spec-change, open-resolve` |

## 미결 · 코디 몫

- **Delivery Issue 개설**(W-13 ①) — `start-delivery` 는 실행하지 않았다(지시대로). surface 축 실행 원장이 아직 없다.
- **「후속 WP」 어휘**(W-13 ②) — 문서 전반 어휘라 이 SPEC 만 고치면 또 다른 비대칭. **별건으로 남긴다.**
- **`log.md` PR 번호 backfill** — 현재 `—`. 머지 후 채워야 한다.
- **시안 본문의 진입점 부채** — `Product Management.html` 본문은 여전히 구 「카탈로그 관리 컬럼 [배포정보] 버튼」 표면이다(frontmatter 만 [기본정보] 탭으로 정합). 2026-07-15 이관을 시안이 따라오게 하는 건 별건 재발주 대상.
- **카탈로그 행 수 3중 불일치** — 스펙에서는 숫자를 걷어냈으나 시안 frontmatter 는 여전히 「product 18 row」(자체 목업 seed 설명이라 이번 범위 밖으로 뒀다), 코드 실측은 30행.

---

# 6차 — WP 작성 (2026-09-22)

SPEC-051 2026-09-22 개정(surface 축)의 **빌드 계획**을 WP 파일로 만들었다. 사용자 지시(스펙·WP 동시 리뷰)에 따라 Delivery Issue 가 아니라 `30-work/` 파일로 갔고, **그 예외 사유를 WP §메타 첫 줄에 박았다.**

## 만든 것

| 파일 | 내용 |
|---|---|
| `products/mediness/30-work/work-131-deploy-surface-axis.md` (신규, 328줄) | `MEDINESS-WP-131` · `doc_no: MEDINESS-DOC-254` · `covers: MEDINESS-SPEC-051` · `status: proposed` · `owner: TBD` · `depends_on: []` |
| `products/mediness/30-work.md` (3자리) | Status Board 행 · WP List 행 · **Spec Coverage covering 칸에 WP-131** + 머리 「최종 수정」 갱신 |

`doc_no` — 현행 + `90-archive/` 전수 스캔 결과 mediness 최대가 `MEDINESS-DOC-253`(WP-132), `254`·`255` 는 미사용이라 **254** 를 잡았다. 전역 유일성 린트 통과.

`status` 는 템플릿·규칙 enum 을 따라 **`proposed`** 로 했다(WP-132 의 `planned` 는 enum 밖 값이라 따르지 않았다). frontmatter ↔ Status Board ↔ WP List 3자 일치.

## 틀 — work-071 을 그대로 물려받았다

같은 SPEC(051)의 동형 선례라 절 구성·frontmatter·Phase 결·Pre-deploy·Rollback 세밀도를 맞췄다. work-071 에 없던 절 2개를 더했는데 둘 다 이번 판의 성격 때문이다:

- **§의존 관계** — Phase 간 선후 + BE↔FE 병렬 접점(work-071 은 phase 4개라 §메타 한 줄로 충분했다. 이번은 7개)
- **§Execution 안의 AC 대응표** — 이번 SPEC 이 surface AC 를 16건 추가해서 「어느 AC 가 안 덮였나」가 눈으로 안 보인다

## 코드 실측 (읽기만 — `mediness-app` dev 브랜치, `39b187f0`)

| 확인한 것 | 실측값 | WP 가 쓴 결정 |
|---|---|---|
| alembic head | `0124_meeting_v2_topic_evidence` (versions 124개) | 신규 = **`0125_deployment_surface_key`**, `down_revision = "0124_meeting_v2_topic_evidence"` |
| 현행 유니크 | `uq_product_deployment_slug_env` (모델 `:__table_args__` + alembic 0030 소유) | → `uq_product_deployment_slug_env_surface` **이름까지 교체**(구 제약 잔존을 이름으로 판별하려고) |
| `product` FK | ORM 모델 없이 raw SQL 접근 → FK 제약은 alembic 0030 소유 | 그 관례 유지 |
| `DeploymentUpdateRequest` | `product_slug`·`environment` **필드 자체가 없음**(「식별 키는 불변」 docstring) | `surface_key` 를 **새로 여는 것**이 이 WP 의 일 + docstring 을 두 필드 한정으로 정정 |
| `DeploymentService.update` | **중복 검사 자체가 없음**(식별 키가 전부 불변 필드였으므로) | 개명 경로 중복 재검사 **신설**이 필요하다는 것을 Phase 2 가 명시 |
| `seeds/deployments.py` | existing set = `select(product_slug, environment)` → 2축 튜플 | Phase 3 — 3축으로. ⚠ 검수가 짚은 자리 |
| `gm_command._render_cards` | `sorted(key=(product_slug, environment.value))` | 3키 + `_format_deployment` 에 **그룹 행 수** 전달 |
| FE 「환경당 1개」 강제 | **세 자리** — `useDeployInfo.ts:184-193`(미사용 환경 선택)·`:229-231`(saveBlock 사전검증)·`:326-333`(save `seen` 맵) + `EnvBlockCard.tsx:98`(select disable) | Phase 6·7 이 네 자리 전부 열거 |

## 스펙이 WP 로 넘긴 것 — 전수 목록

SPEC 본문에서 「WP」·「WP 이관」·「후속 WP」·「WP·코드」로 적힌 자리를 전수로 훑었다. **이 WP 가 받는 것 / 범위 밖인 것**을 갈랐다.

| SPEC 위치 | 넘긴 것 | WP-131 처분 |
|---|---|---|
| `:409` | **컬럼 타입·migration 번호·인덱스 컬럼 순서** | ✅ **받음** — §Domain/Schema 결정표(`String(50)`·`0125`·`surface_key` 마지막), 근거까지 |
| `:404` · `:245` | 시연계정 정규화(별도 테이블 vs JSONB) | ✅ **받음** — JSONB 임베드 유지(현행 모델 docstring 의 WP-043 P1 결정 그대로), §Code Surface Domain note |
| `:408` | 대소문자 접기가 필요해지면 **함수 인덱스**(후속 결정) | ✅ **받음** — §Open Issues. 이번엔 접지 않는다 |
| `:304` | `service_url` **형식 강도** | ⭕ **받되 이번 범위 밖으로 명시** — surface 축과 무관한 선재 항목. 시안 검증(빈 값 400)까지만 |
| `:217` · `:241` | 삭제 **hard/soft** | ⭕ **hard 유지**(현행 `DELETE`). soft 비활성은 `:366` 과 같은 자리라 §Scope 제외로 명시 |
| `:366` | 배포 항목 **soft 비활성** 표현 | ❌ **제외** — §Scope 제외에 이유와 함께 |
| `:78` · `:380` | UX 세부·**구체 컴포넌트명/경로** | ✅ **받음** — §Code Surface 표가 실제 파일 6개를 줄번호까지 지목 |
| `:397` | 활성 필터 조인/구현 | ❌ **무변경** — WP-071 이 이미 구현. §Scope 제외(「`/gm` 인자 파싱·활성 필터 손대지 않는다」) |
| `:482` | 민감값 **seed 주입** | ❌ **제외** — nexus·say-admin 실데이터는 운영자 모달 입력 |
| `:468` (OQ-3) | 대시보드 DB-SoT 전환 | ❌ **범위 밖**(비블로킹, 다른 SPEC) |
| `:470` (OQ-4 ②) | 조직별 계정 그룹 + `note` 잔여 종속 | ❌ **범위 밖** — §메타 후속 항목 + §Scope 제외 |
| **(스펙에 없음 — 검수 발견)** | **seed idempotent 스킵 키 3축** | ✅ **받음 — Phase 3 단독**. 2축인 채로 두면 재실행 때 중복. 「이 Phase 의 존재 이유」를 두 번째 검증 항목이 직접 재현 |

## 스펙 §5 AC ↔ Phase 완료조건 대응표 (surface 축 16건)

> WP 본문 §Execution 에 같은 표를 실었다. **대응 안 되는 AC = 0.**

| SPEC AC | 구현 Phase | 회귀 |
|---|---|---|
| `:445` 같은 (제품,환경) 다른 surface 2건 → 둘 다 201 | P1 제약 · P2 판정 | P5 |
| `:446` 3축 전부 같은 재생성 → 409 | P2 | P5 |
| `:447` 빈 값/공백만/미지정 → 400 · 길이 초과 → 400 | P2 | P5 |
| `:448` 신규 카드 surface 빈 값 · 그대로 저장 → **409 아닌 400** | P6·P7 | P7 수동 |
| `:449` `[+ surface 추가]` 환경 물려받고 바로 아래 / `[+ 환경 추가]` 맨 뒤 | P7 | P7 수동 |
| `:450` 저장 카드 환경 편집 불가(칩) · surface 는 가능 | P7 | P7 수동 |
| `:451` surface 별 시연계정 분리 | P1 행 분리 | P5 |
| `:452` `surface_key` PATCH 개명 · 결과 중복 409 · slug/env 불변 | P2 | P5 |
| `:453` 기존 8행 무손상(`기본` 조회·건수·URL·계정 불변) | P1 백필 · P3 seed | P5 |
| `:454` 다른 환경이면 같은 이름 재사용 → 둘 다 201 | P1 제약 | P5 |
| `:455` **GET 응답 모든 행에 `surface_key`** | P2 | P5 |
| `:456` 2건 이상 → 행 수만큼 카드 + surface 표기 | P4 | P5 |
| `:457` 1건뿐이면 미표기(확장 전과 동일) | P4 | P5 |
| `:458` 시연계정 있는 행 삭제 = 확인 단계, 취소 시 미발행 | P7 | P7 수동 |
| `:459` **표기 전이** — 2행 중 1행 삭제 시 표기 사라짐 | P4 | P5 |
| `:460` `/gm` 2토큰 파싱 불변 | (무변경 — P4 가 **안 건드림을 확인**) | P5 |

역방향도 봤다 — **Phase 검증 항목 중 AC 에 근거가 없는 것**은 4개이고 전부 **구현 안전장치**라 AC 대상이 아니다: ① 백필 누락 시 NOT NULL 이 터지는 것을 의도적으로 재현(P1) ② `upgrade → downgrade → upgrade` 왕복(P1) ③ seed 재실행 멱등(P3 — 스펙에 없는 검수 발견분) ④ `/gm` 출력 **문자 단위** 비교(P4 — `:457` 의 「확장 전과 동일」을 실행 가능한 형태로 좁힌 것).

## Pre-deploy / Rollback — 되돌릴 수 없는 지점

지시대로 **파괴적 DDL** 을 정면으로 다뤘다.

- **백필 덜 된 상태의 `SET NOT NULL`** — 그 자리에서 migration 이 터지고 alembic 이 그 리비전을 **미완으로 남긴 채 멈춘다**(컬럼은 추가됐고 제약은 안 붙은 중간 상태) → 백엔드 기동 실패. Pre-deploy 1번이 `count(*) WHERE surface_key IS NULL = 0` 을 3단계 **전에** 확인하게 했다.
- **point of no return = 같은 (제품,환경)에 2행째가 생기는 순간.** 구 유니크 `(product_slug, environment)` 를 다시 붙이려는 순간 그 그룹이 중복이라 `ADD CONSTRAINT` 가 실패한다. 되돌리려면 **어느 행을 지울지 사람이 먼저 정해야** 하고 그건 운영 데이터 삭제 결정이다.
- **down 이 조용히 실패하지 않게** — down 첫머리에서 `GROUP BY 1,2 HAVING count(*) > 1` 을 돌려 걸리는 그룹을 메시지에 싣고 명시적으로 중단하도록 Phase 1 작업에 박았다.
- **금지 조합 2개** — BE 코드만 revert(migration 유지) = POST 가 NOT NULL 위반으로 500 / migration 만 down(코드 유지) = 없는 컬럼 읽어 즉시 터짐. 둘 다 ⛔ 로 명시하고 **BE revert 는 migration down 과 함께**라고 못박았다.
- **컬럼 DROP = 운영자가 친 surface 이름 소실** — 되돌린 뒤 다시 올리면 전부 `기본` 으로 재백필된다는 것도 표에 적었다.

## 검증

### lint — ⚠ **263. 기준선 264 에서 1건 줄었다** (예상과 다름 — 아래 이유)

```
$ python3 scripts/lint-pipeline.py --strict
exit 0 — 0 error, 263 warning
```

**줄어든 1건 = 5차가 의도적으로 만든 SPEC-051 derive WARN 이다.** 사라진 이유:

- Spec Coverage 의 `구현 상태` derive 규칙(`scripts/lint-pipeline.py:664-676`)은 **covering WP 의 frontmatter status 목록**에서 계산한다 — 「모두 done → done · 하나라도 in_dev 이상 → in_dev · 모두 proposed → proposed」.
- 5차 시점: covering = WP-058/071/073/087 **전부 done** → derive `done` ≠ 셀 `in_dev` → **WARN**(= 「계약이 커졌는데 그걸 받을 WP 가 없다」는 신호).
- 6차: covering 칸에 **WP-131(proposed)** 이 들어가 전부 done 이 아니게 됐고, done 이 섞여 있으므로 derive = **`in_dev`** → 셀과 일치 → **WARN 해소**.

**이건 신호를 지운 게 아니라 신호가 요구하던 것을 채운 것이다.** 그 WARN 의 의미는 「이 SPEC 의 늘어난 계약을 받을 실행 원장이 없다」였고, WP-131 이 바로 그 원장이다. 지금 대시보드는 `in_dev` + covering 에 `proposed` WP 하나 → 「계약은 늘었고 계획은 섰고 아직 구현 전」을 정확히 말한다.

**되돌리고 싶으면 한 줄이다** — `30-work.md` SPEC-051 행의 covering 칸에서 `MEDINESS-WP-131 (…)` 만 빼면 derive 가 다시 `done` 이 되어 WARN 이 264 로 복귀한다. 다만 그러면 **SPEC-051 을 커버하는 WP 가 Spec Coverage 에서 누락**되므로(§한 곳 원칙의 「SPEC-centric view」가 반쪽) 권하지 않는다.

- `30-work.md:245` **SPEC-030 derive WARN 은 그대로 남았다**(선재 WARN, 무관).
- mediness 범위 **ERROR 0**. 신규 WP 에 걸린 WARN **0건**(`doc_no`·frontmatter·WP List 동기·status 3자 일치 전부 통과). 나머지 262 = 타 제품 선재.

### 린트 3표 동기

| 표 | 조치 |
|---|---|
| `## WP List` | WP-131 행 추가 — **필수**(파일만 있고 목록에 없으면 ERROR) |
| `## Status Board` | WP-131 행 추가 — status 3자 일치(frontmatter/Board/List 전부 `proposed`) |
| `## Spec Coverage` | SPEC-051 covering 칸에 WP-131 — SPEC ID 동기는 원래 통과하지만, **covering 칸이 SPEC-centric view 의 본체**라 새 커버 WP 를 빼면 표가 거짓말을 한다. 위 WARN 변동의 원인 |

### doc_no

`MEDINESS-DOC-254` — 현행 + archive 전수 스캔(mediness max = 253), 파일 안 1회만 등장, 린트 전역 유일성 통과.

## 변경 파일 (커밋·push·PR 없음)

| 파일 | 상태 |
|---|---|
| `products/mediness/30-work/work-131-deploy-surface-axis.md` | **신규** (untracked) |
| `products/mediness/30-work.md` | 수정 — Status Board 1행 · WP List 1행 · Spec Coverage 1칸 · 머리 「최종 수정」 |
| `spec-051` · `21-html` · `log.md` | **손대지 않음**(5차 확정분 그대로) |

## 미결 · 코디 몫

- **lint 264 → 263** — 위 이유. 되돌림은 한 줄이나 권하지 않는다. **코디 판단.**
- **`log.md` entry** — 이번 WP 추가에 대한 `wp-add` 행을 넣지 않았다. 지시서가 `log.md` 를 「고치지 마라」로 묶었기 때문이다. 규칙(§변경 라우팅)은 WP 추가 시 entry 1건을 요구하므로, **PR 에 넣을지 코디가 정해야 한다**(5차의 `spec-change, open-resolve` 행에 `wp-add` 를 콤마 결합하는 방법도 있다 — 같은 PR 이므로).
- **`owner: TBD`** — 규칙상 개인 handle 이 정해지지 않았으면 TBD 이고 Status Board 도 TBD 로 두며 「다음 review 의 open item」이다. BE·FE 가 갈리는 WP 라 실제 배정이 필요하다.
- **예상 기간 `2~3d`·목표 완료 `TBD`** — Status Board 에 rough estimate 로 넣었다. 근거는 Phase 7개 중 BE 5·FE 2, migration 1건, 신규 테이블 0. 실제 착수 시 조정 대상.
- **`start-delivery` 미실행** — 지시대로. 이 WP 가 Harness v1 예외이므로 Delivery Issue 는 열지 않았다.

---

# 7차 — log wp-add (2026-09-22)

6차가 미결로 넘긴 `log.md` entry 를 닫았다. **2026-09-22 행 하나만** 고쳤다(`products/mediness/log.md:18`):

- `종류` → **`spec-change, open-resolve, wp-add`** (`rules/document-pipeline.md:330` enum · `:331` 콤마 결합)
- `영향 ID` → `MEDINESS-SPEC-051, **MEDINESS-WP-131**`
- `요약` 끝에 **한 문장 덧붙임** — 「실행 원장은 [WP-131](30-work/work-131-deploy-surface-axis.md)(7 Phase · BE+FE) — Harness v1 상 신규 실행은 Delivery Issue 이나 SPEC 과 동시 리뷰를 위해 사용자 판단으로 WP 로 만든 예외다」. **기존 본문은 한 글자도 안 고쳤다**(덧붙이기만).

선례 대조 — `log.md:22` `2026-08-31 | wp-add, spec-change | MEDINESS-WP-128, MEDINESS-SPEC-151, … |` 와 표기 형태 동일(종류 콤마 결합 · 영향 ID 에 WP+SPEC 병기). ID 순서만 지시대로 SPEC 뒤에 WP 를 뒀다(선례는 WP 가 앞 — `영향 ID` 순서는 규약이 정하지 않는다).

`lint --strict` = **0 error / 263 warning 유지**(변동 0). `log.md` 외 파일 변경 0 — `spec-051`·`21-html`·`30-work.md`·`work-131` 그대로.

**남은 것**: `PR` 칸 `—` 는 머지 후 PR 번호 backfill 대상(라우팅 판단이 필요 없는 예외 변경 — `rules/document-pipeline.md` §변경 라우팅).

---

# 8차 — WP 정정 (2026-09-22)

`work-131-deploy-surface-axis.md` **한 파일만** 고쳤다. `spec-051`·`21-html`·`log.md`·`30-work.md` 무변경.

## ① migration 번호 stale — 전수 정정 4자리

실측 대상이 낡았다는 것을 **워크트리 base 가 아닌 `origin/dev` 로 다시 확인**했다:

```
$ git ls-tree --name-only origin/dev back/alembic/versions/ | tail -1
back/alembic/versions/0138_task_body_and_references.py
$ git show origin/dev:back/alembic/versions/0138_task_body_and_references.py | grep '^revision'
revision: str = "0138_task_body_refs"
```

**파일명 ≠ revision id 를 원본에서 직접 확인했다.** 이 레포는 revision 문자열을 축약해 쓰는 관례다 — 바로 앞 `0137_tasks_created_by_index.py` 의 revision 도 `0137_tasks_created_by_ix` 다. 지시서가 경고한 함정이 실재한다.
(⚠ BE 가 만든 `0139` 파일 자체는 fetch 가능한 어느 remote 브랜치에도 아직 없다 — `origin/dev`·`origin/main`·`origin/edu-shots` 전수 확인. 그래서 `down_revision` 값은 **대상인 0138 의 `revision` 값**에서 확정했다. 결과는 같다.)

| 자리 | 전 | 후 |
|---|---|---|
| `:69` §Code Surface 표 | `0125_deployment_surface_key.py` / head `0124_meeting_v2_topic_evidence` / **「versions 124개」** | `0139_deployment_surface_key.py` / head `0138_task_body_and_references.py` → `down_revision = "0138_task_body_refs"` + **revision id ≠ 파일명 주의** 한 줄. **개수 실측값 삭제** |
| `:101` §Domain/Schema `Migration 필요 여부` | `0125_deployment_surface_key` | `0139_deployment_surface_key`(+ `down_revision` 명시) |
| `:148` Phase 1 작업 | `0125` / `down_revision = "0124_…"` | `0139` / `down_revision = "0138_task_body_refs"`(파일명이 아니라 **`revision` 값**임을 괄호로) |
| `:61-63` §Code Surface 머리 | (없음) | **기준 브랜치 = `origin/dev`** 명시 + **왜 어긋났는지 ⚠ 한 줄** 신설 |

**왜 어긋났는지(WP 에 박은 문장)**: 「이 WP 의 최초 실측(2026-09-22)이 `0124` 를 head 로 잡았으나 실제 `origin/dev` head 는 `0138` 이었다. 읽은 대상(`harness_works/mediness-app` canonical 체크아웃)이 **사용자 피처 브랜치 상태**라 `origin/dev` 보다 뒤처져 `0134`~`0138` 이 없었기 때문이다. **실측 자체는 맞았고 실측 대상이 낡았다.** 번호·head 는 착수 직전 `git ls-tree origin/dev back/alembic/versions/` 로 다시 본다. 파일 **개수**는 문서에 박지 않는다 — 코드가 SoT 다.」

개수 실측값을 지운 판단은 W-14 에서 「17 row」에 한 것과 같다 — 코드가 SoT 인 숫자를 문서에 박으면 또 굳는다.

### grep 전수 결과

| 패턴 | 잔존 |
|---|---|
| `0125` | **0** |
| `0124` | **1 — 의도적**(`:63` 의 「왜 어긋났는지」 문장. 틀렸던 번호를 말해야 하는 자리다) |
| 개수 실측값(`124개` 류) | **0** |

## ② 대시보드 2축 dict — Phase 8 신설 + Open Issues

**Phase 8 — BE: 대시보드 배포 링크 결정성 (환경당 1개 유지)** 를 끝에 붙였다(기존 1~7 을 renumber 하지 않았다 — BE 가 이미 그 번호로 굴렀다).

- **고치는 것은 손실이 아니라 비결정성이다** — 카드는 환경당 1개를 유지하고(대시보드 화면 무변경), 어느 것이 뜰지만 고정한다. 이 한 줄을 Phase 설명 첫머리에 뒀다.
- **선택 규칙**: `surface_key == "기본"` 우선 → 없으면 `surface_key` 오름차순 첫째.
- **`기본` = sentinel 아님 계약과의 충돌 차단** — 「여기서 `기본` 은 **대시보드 한 화면의 표시 정렬 규칙**일 뿐이고, 저장·검증·유니크·API 응답 어디에도 이 값으로 갈리는 분기를 만들지 않는다. **`기본` 이 없는 제품도 규칙 2단계로 똑같이 결정된다 — 값의 존재에 의존하지 않는다**」를 명시했다. 규칙이 `기본` **없이도 성립**한다는 점이 sentinel 이 아님의 실질적 증명이라 그 문장을 넣었다.
- **「대표 surface」 신설 안 함** — 컬럼·플래그·API 필드 0. 대표성을 데이터에 박는 것은 SPEC 판이라고 적었다.
- **검증 3건** — 행 2~3개일 때 여러 번 호출해도 같은 URL / `기본` 있으면 그것, 없으면 오름차순 첫째 / **행 1건 제품 결과 불변(회귀 0)**.
- **§Scope 포함**에 BE 항목 1줄, **§Open Issues** 에 남은 것 — 「카드는 여전히 환경당 1개라 nexus prod 6표면 중 1개만 보인다. 표면 여럿을 드러내는 방식은 **SPEC-100/101 소유**이며 SPEC-051 §6 OQ-3 과 **같은 층**이다. 이 WP 는 화면 계약을 만들지 않는다.」
- **AC 표 아래 한 줄 추가** — 「Phase 8 은 이 표에 없다 — 대시보드 결정성은 SPEC 계약이 아니라 **구현 층 결정**이라 대응 AC 가 없다. **구멍이 아니라 축이 다른 항목**이다.」 (AC↔Phase 대응 구멍 0 이라는 6차 주장이 Phase 8 때문에 깨진 것처럼 읽히지 않게.)

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error / 263 warning** (변동 0)
- WP 346줄 · Phase 8개 · `Status:` 라인 8개 전부 `TODO` 단독(형식 위반 0)
- `git status --porcelain` = `M products/mediness/30-work/work-131-deploy-surface-axis.md` **한 줄뿐**

## 넘기는 것

- **Phase 상태를 올리지 않았다** — 코디가 「BE·FE 가 실제로 굴렀고 migration 왕복 8/8 을 실증했다」고 했으나, 이번 지시서는 정정 2건만 요구했고 **어느 Phase 가 어디까지 착지했는지 나는 검증하지 않았다.** 지금은 8개 전부 `TODO` + frontmatter `proposed` 로 **3자 정합 상태**(lint 통과)다. 실제 착지분을 반영하려면 `review-wp`(코드 ↔ WP 대조) 판이 따로 필요하다 — frontmatter `in_dev` 전이와 `30-work.md` Board/WP List 동기가 함께 가야 한다.

---

# 9차 — Phase 상태 갱신 (2026-09-22)

`reviewer_code` PASS(계약 위반 0 · FAIL 0 · WARN 4 · 관찰 5) 근거로 Phase 상태를 올렸다. **`work-131` + `30-work.md` 두 파일만.**

## ⚠ 지시 3조건이 lint 와 동시 성립 불가였다 — (A) 로 갔다

지시가 요구한 것: ① Phase 1~8 전부 `DONE` ② frontmatter `done` **금지**(`in_dev`) ③ lint **0 error**.

그런데 `rules/document-pipeline.md` §자동 검증의 **7→8 게이트**는 「전 phase `DONE` 인데 frontmatter `status != done` → **ERROR(block)**」다. 셋을 동시에 만족하는 상태가 없다. 실제로 8개를 전부 DONE 으로 올리자:

```
[ERROR] products/mediness/30-work/work-131-deploy-surface-axis.md:
        MEDINESS-WP-131 phase 전부 DONE 인데 frontmatter status=in_dev — done 으로 갱신 필요 (생명주기 7→8)
```

**코디에게 물으려 했으나 Orca 런타임이 내려가 `ask`·`send` 가 닿지 않았다**(`The Orca runtime closed the connection before responding` ×2). 그래서 판단해서 진행하고 여기 남긴다.

**선택 = (A) Phase 5 만 `IN_PROGRESS`, 나머지 7개 `DONE`, frontmatter `in_dev`.** 근거 셋:

1. **지시가 인용한 선례와 같은 모양이다** — WP-129·130 이 「P0 은 prod DB 실측 3건이 **Pre-deploy 로 이월**돼 IN_PROGRESS」인 채 `in_dev` 로 갔다. 여기도 똑같이 Pre-deploy 로 이월된 항목이 Phase 5 에 있다.
2. **문서가 거짓말을 하지 않는다** — Phase 5 의 자기 검증 항목이 「격리 DB 에서 기존 배포·gm 테스트 **회귀 0 으로 전체 통과**」인데 `TestProductAssigneeAccess` 12건 기존 실패로 **실제로 미충족**이다. 그 줄에 `⏳ … 미충족` 을 달고 왜 그런지·어디로 이월됐는지를 같은 줄에 적었다. 나머지 4개 항목은 실제로 끝나서 `[x]`.
3. **지시 ②·③ 을 둘 다 지킨다** — `done` 으로 올리지 않았고 lint 는 **0 error**.

**되돌리기 쉽다** — (B)를 원하면 Phase 5 `Status` 를 `DONE` 으로, frontmatter 를 `done` 으로(두 줄). 다만 머지·배포 전이라 지시가 금지한 방향이다.

## Phase 별 상태 + 완료 증거

| Phase | Status | 완료 증거에 실은 것 |
|---|---|---|
| 1 migration | **DONE** | `test_0139_deployment_surface_key.py` **8 passed** — 5단계 순서·왕복 + **down 중복가드 실제 재현**(`charty/prod(2건)` 이 `RuntimeError` 메시지에 실리는 것까지). head 체인 `0137_… → 0138_task_body_refs → 0139_…` **단일 head** 검수 확인 |
| 2 스키마·서비스 | **DONE** | API+service 통과(Phase 5 합산). `_duplicate()` 헬퍼로 409 4곳 수렴 · `_normalize_surface_key` 를 기존 관례 옆에 추가 → 검수 재사용 ✔. 상한 단일화는 검수 지적분으로 추가 판 마감 |
| 3 seed | **DONE** | `DEFAULT_SURFACE_KEY` 를 seed·dashboard 가 **import**(리터럴 복제 0). migration 만 의도적으로 복제하고 **이유를 주석에 남긴 뒤 테스트로 고정** |
| 4 `/gm` | **DONE** | `test_gm_command.py` — 확장 전 출력과의 **문자 단위 비교**를 하드코딩 기대값으로 고정. `showSurface` 서버 기준 전환은 추가 판 마감 |
| 5 pytest 회귀 | **IN_PROGRESS** | **63 passed / 12 failed** · service(gm 합산) **57 passed**. 12 failed = 기존 환경(`org_unit↔department` seed 누락, 무접촉 파일이 같은 사유로 9/11 실패). 권한 회귀 0 은 **diff 확인** → Pre-deploy 이월 |
| 6 FE 훅 | **DONE** | `npx tsc --noEmit` **exit 0**. 배치 저장 중단 건(O-1)은 **정책이라 Open Issues 이월** |
| 7 FE 카드 | **DONE** | `vitest wp131-deploy-surface.test.tsx` **5 passed**(+`vitest.config.ts` 등재, 검수 지적분) · `tsc` exit 0. 미저장 초안 확인 제거(O-4)는 추가 판 마감 |
| 8 대시보드 | **DONE** | `test_dashboard_split.py` **30 passed** — 그중 **기존 25건이 무수정 통과**(= 행 1건 제품 출력 불변, 이 Phase 의 회귀 0 조건). 신규 5건이 결정성·`기본` 우선·부재 시 오름차순을 고정 |

DONE phase 의 작업/검증 체크박스 **61개를 `[x]` 로** 채웠다(work-071 선례 — DONE 인데 상자가 비어 있으면 문서가 스스로 모순된다). Phase 5 는 5개 중 4개만 체크, 미충족 1개는 `[ ] ⏳ … 미충족` 으로 남겼다.

## 30-work.md 3표 동기

| 표 | 조치 |
|---|---|
| `## Status Board` | WP-131 `proposed` → **`in_dev`**, 「다음」 칸 `발주 대기` → `머지·배포` |
| `## WP List` | WP-131 `proposed` → **`in_dev`** |
| `## Spec Coverage` | SPEC-051 행 `구현 상태` **`in_dev` 그대로**(derive 도 그대로 맞는다 — covering 에 `in_dev` 가 섞이면 derive 가 `in_dev`). 셀 안 WP-131 부연만 `**proposed**` → `**in_dev** — reviewer_code PASS, 머지·배포 전` |

3자 일치(frontmatter/Board/List = 전부 `in_dev`) 확인 — 중간에 Board·List 가 `proposed` 인 상태에서 lint 가 그 불일치를 ERROR 로 정확히 잡았고, 동기 후 사라졌다.

## §Open Issues — 2루프 이월 6건을 한 목록으로

「**2루프 이월 — 사용자 화면 결정이 필요한 것**」 소절을 만들어 검수 신규 3건 + 기존 3건을 **한 자리에** 묶었다(지시대로 — 2루프가 목록 하나를 본다). 머리에 「전부 계약 위반이 아니다(PASS·FAIL 0). 코드로 정할 수 없고 **운영자가 실물에서 만나 봐야 정해지는 것**들」을 달았다.

① 모달 배치 저장이 빈 신규 카드 하나로 전부 멈춤(시안 `continue` vs TSX `return` — **정책 결정이라 사용자 E2E**) · ② surface 오름차순이 층마다 다름(FE `localeCompare(ko)` / 파이썬 코드포인트 / PG collation — **모달 순서와 슬랙 순서가 갈릴 수 있다**) · ③ 「환경 불변」 안내문 행 수만큼 반복 · ④ `prod` 칩 6회 · ⑤ 백필 `기본` 첫인상 · ⑥ 빈 surface 를 저장 눌러야 앎.

기존 「대시보드가 표면 여럿을 드러내지 않는다」 등은 `### 그 밖` 으로 갈라 남겼다.

## §Pre-deploy Check — 12건 기존 실패 한 줄

권한 항목 바로 아래에 붙였다: 「⚠ **권한 경로는 테스트 초록으로 증명되지 않는다 — 실환경에서 손으로 1건 확인한다.**」 + 원인(`org_unit↔department` seed 누락, 무접촉 파일 9/11 동일 사유) + 권한 회귀 0 은 **diff 로 확인**(`policies/deployment.py`·게이트 무변경) + 밟을 것 2개(**담당자 계정으로 본인 담당 제품 편집 1건 + 담당 밖 403 1건**).

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error / 263 warning**(수치 변동 0, exit 0)
- `git status --porcelain` = `M 30-work.md` · `M 30-work/work-131-deploy-surface-axis.md` **두 줄뿐**. `spec-051`·`21-html`·`log.md`·코드 레포 무변경
- 12건 기존 실패 **재조사 안 함**(지시대로 — `flaky-baseline-evidence.md` 판정 인용만)
