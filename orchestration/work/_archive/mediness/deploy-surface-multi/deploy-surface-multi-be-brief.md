# [backend] WP-131 Phase 1~5 — 배포 레지스트리 surface 축 (3축 유니크 + migration + seed + /gm)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **`frontend` 워커가 같은 워크트리의 `front/` 에서 병렬 작업 중이다. `front/` 를 절대 건드리지 마라.** 너는 `back/` 만이다. 같은 트리를 공유하므로 `git add -A`·`git checkout .` 류의 전체 범위 명령도 쓰지 마라.

⚠ **너는 이 작업의 맥락이 하나도 없다.** §1 을 전부 읽고 시작해라.

## 1. SSOT — 먼저 읽을 것

**계약은 다른 레포에 있다. 이 워크트리에 없으니 절대경로로 읽어라** (spec PR #762 로 올라갔고 `dev` 에는 아직 없다):

1. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/30-work/work-131-deploy-surface-axis.md`
   ← **네 작업서. 전부 읽어라.** §Code Surface 가 만질 파일을 줄번호까지, §Domain/Schema 가 컬럼 타입·제약명·인덱스 순서·**migration 5단계**를 근거와 함께 잡아 놨다. **Phase 1~5 가 네 몫**이다(6·7 은 FE).
2. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md`
   ← **외부 계약.** §3 API·§Validation·§케이스 매트릭스(에러 문구·코드의 단일 SoT)·§4 DB·§5 AC.
3. 작업 워크트리 `back/AGENTS.md`(있으면) — 레포 규약.

**기대는 개념**:

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/unique-key.md`
  — **이번 작업의 핵심 잣대.** 유일성은 값을 쓰는 순간 DB 가 저장된 바이트로 판정한다. 앱 정규화와 DB 제약이 **같은 값**을 봐야 성립한다(→ trim 값 저장).
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/para/areas/concept/db/database-migration.md`
  — 5단계 순서가 왜 그 순서인지. 되돌릴 수 없는 지점이 어디인지.

## 2. 배경 / 무엇을 바꾸나

배포 레지스트리가 **환경당 서비스 URL 1개**를 전제로 굳어 있다(`uq_product_deployment_slug_env`). `nexus` prod 에 URL 이 6개라 두 번째부터 409 로 튕긴다. 식별 키에 **`surface_key`** 한 축을 더해 `(product_slug, environment, surface_key)` 로 넓힌다. 행 1개 = 표면 1개 = URL 1개 + 시연계정 0~N.

**계약은 확정됐다(SPEC-051 stable, 2026-09-22 개정). 발명하지 마라.** 계약과 어긋나는 사실이 나오면 **코드를 고치기 전에 보고해라** — 스펙으로 되돌린다.

## 3. 계약 (FE 와 합의됨 — 이대로 제공)

- **필드명 `surface_key`** — POST body 필수 · PATCH body 선택(보내면 개명) · **GET 응답 모든 행에 항상 포함**(백필 행은 `"기본"`). camelCase 변환 없음(현행 `product_slug`·`service_url` 관례).
- **409 판정 축 = 3축.** 같은 환경 + 다른 surface = 201. 다른 환경 + 같은 surface = 201. 셋 다 같을 때만 409.
- **400 사유 2종** — 빈 값/공백만 · 50자 초과(`detail.max_length` 동봉). **문구·코드는 SPEC §케이스 매트릭스가 소유한다 — 지어내지 마라.**
- **`/gm` 카드 헤더 surface 표기 = 그 (제품, 환경) 그룹의 행 수 ≥ 2 일 때만.** **값(`기본`) 판정이 아니다.**

## 4. 먼저 읽을 핵심 파일

WP §Code Surface 표가 전부 잡아 놨다. 요지:

- `back/app/models/product_deployment.py` — 컬럼 + `UniqueConstraint` 3축(`…_slug_env` → `…_slug_env_surface`)
- `back/alembic/versions/` — **head 가 `0124_meeting_v2_topic_evidence` 인지 네가 직접 확인**하고 `0125_deployment_surface_key` 신규
- `back/app/schemas/deployment.py` — ⚠ **`DeploymentUpdateRequest` 에는 `surface_key` 필드가 아예 없다**(「식별 키는 불변」 주석과 함께). 이건 고치는 게 아니라 **새로 여는 일**이다. 주석도 함께 정정해라.
- `back/app/services/deployment.py` — ⚠ **`update` 에 중복 검사 자체가 없다.** 개명 중복 재검사를 **신설**해야 한다.
- `back/app/seeds/deployments.py` — ⚠ **existing set 이 2축이라 3축으로 안 바꾸면 재실행 때 중복이 들어온다.**
- `back/app/services/gm_command.py` — 정렬 3키 + 조건부 표기

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/` · `docker-compose.yml` · `docker-compose.local.yml` (이번엔 쓸 일 없을 것이다)

**`front/` 금지** — FE 워커 몫이다.

## 6. Phase — WP-131 §Execution 그대로

1. **Phase 1** — `surface_key` 컬럼 + 3축 유니크 마이그레이션. **5단계 순서는 SPEC 계약이라 뒤집지 마라**(컬럼 추가 → `기본` 백필 → NOT NULL → 구 유니크 DROP → 확장 유니크 ADD). `server_default` 를 두지 마라 — 두면 「빈 값이면 400」 계약이 DB 층에서 조용히 우회된다. **`downgrade` 도 반드시 써라**: 첫머리에 중복 그룹 검사(`GROUP BY product_slug, environment HAVING count(*) > 1`)를 돌려 결과가 있으면 **명시적 에러로 중단**하고 어느 그룹이 걸리는지 메시지에 실어라. 제약 실패 메시지만 보고 원인을 짐작하게 두지 않는다.
2. **Phase 2** — 스키마 3곳 + trim 정규화 + 3축 중복 판정 + `update` 개명 재검사 신설. **trim 한 값을 저장한다**(검증에만 쓰지 마라 — `기본` 과 `기본␣` 이 둘 다 통과해 유니크가 샌다). 사전 검사와 DB 제약을 **두 겹 다 살려라**(사전 검사 = 친절한 에러, `IntegrityError` → 409 = 진짜 보증).
3. **Phase 3** — seed 8행 `surface_key='기본'` + **idempotent 키 3축 교체**. 검증에서 **재실행 중복을 직접 재현**해라.
4. **Phase 4** — `/gm` 정렬 3키 + 조건부 표기. **완료 조건 = 기존 단일 surface 제품 출력이 확장 전과 문자 단위로 동일**.
5. **Phase 5** — pytest 회귀. SPEC §5 surface AC 16건 중 **BE 몫과 1:1**(WP 에 대응표가 있다).

**Phase 를 진행하며 WP 문서의 `Status:` 를 갱신하지 마라** — 그건 다른 레포이고 코디 몫이다. 보고로 대신한다.

## 7. 하지 말 것

- **계약을 발명하지 마라.** 에러 문구·코드는 SPEC §케이스 매트릭스가 소유한다.
- **`demo_accounts` 를 별도 테이블로 정규화하지 마라** — JSONB 임베드 유지(WP-043 P1 결정).
- **권한 게이트·환경 enum·`/gm` 인자 파싱을 건드리지 마라.** 불변이다.
- **`front/` 금지.**
- **`migration` 5단계 순서를 바꾸지 마라.**
- **로컬 스택(`make local-stack`)을 띄우지 마라** — 사용자 방침. 포트·프로세스도 건드리지 마라.
- 커밋·push·PR 금지.

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만>
```

(전체 스위트 금지 — 사용자 방침. `DATABASE_URL` 은 `back/pyproject.toml` 의 테스트 DB = `localhost:25434/mediness_test`.) **검증은 1회만 — 통과하면 반복하지 마라.**

추가로:
- **migration 왕복** — `alembic upgrade head` → `downgrade -1` → `upgrade head` 가 도는지. down 의 중복 가드가 **실제로 걸리는지도** 한 번 재현해라(같은 (제품,환경)에 2행 만든 뒤 down 시도 → 명시적 에러).
- 기존에 깨져 있던 무관한 실패는 **"무관"으로 분리**해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다 — **이 세션에서 세 번 바뀌었다.** preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --from term_201334b3-620b-4b5d-b969-f4c7e9837a87 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고:
  `orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --text "[질문] backend: <질문>" --enter`
