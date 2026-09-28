# [frontend] WP-131 Phase 6~7 — 배포정보 모달 surface 축 (환경 소진 폐지 + 평평 카드)

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **`backend` 워커가 같은 워크트리의 `back/` 에서 병렬 작업 중이다. `back/` 을 절대 건드리지 마라.** 너는 `front/` 만이다. 같은 트리를 공유하므로 `git add -A`·`git checkout .` 류 전체 범위 명령도 쓰지 마라.

⚠ **BE 를 기다리지 마라.** 아래 §3 접점 2개만 알면 BE 머지 전에 끝낼 수 있다. BE 응답이 아직 `surface_key` 를 안 줄 수 있으니 **없을 때 터지지 않게** 짜라(백필 행은 `"기본"` 이 오는 게 정상이다).

⚠ **너는 이 작업의 맥락이 하나도 없다.** §1 을 전부 읽고 시작해라.

## 1. SSOT — 먼저 읽을 것

**계약과 시안은 다른 레포에 있다. 절대경로로 읽어라** (spec PR #762 로 올라갔고 `dev` 에는 없다):

1. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/30-work/work-131-deploy-surface-axis.md`
   ← **네 작업서.** §Code Surface 가 만질 파일을 **줄번호까지** 잡아 놨다. **Phase 6·7 이 네 몫**(1~5 는 BE).
2. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/21-html/Product Management.html`
   ← 🔑 **시안이 정본이다.** 배포정보 모달의 확정 모양이 여기 있다. `envBlockHTML`·`addEnvBlock`·`addSurfaceBlock`·`removeEnvBlock`·`commitDeploys`·`renderEnvBlocks`·`ENVS`/`ENV_DISPLAY_ORDER` 를 **코드로** 읽어라 — 주석이 아니라 동작이 기준이다. **시안과 다르게 만들고 싶으면 만들지 말고 보고해라.**
3. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md`
   ← §2 UX Contract·Wireframe·§4 Frontend Implementation·§5 AC.

**기대는 개념**: 해당 없음 (이번 FE 작업은 DB·계약 개념이 아니라 시안 추종이다).

## 2. 배경 / 무엇을 바꾸나

배포정보 모달이 **환경당 블록 1개**를 전제로 굳어 있다 — `useDeployInfo` 가 이미 쓴 환경을 골라 주고(`addEnvBlock`), `EnvBlockCard` 가 `usedEnvs` 로 select 를 disable 한다. 식별 키에 `surface_key` 가 들어가면서 **같은 환경을 여러 번 고를 수 있어야 한다**(`nexus` prod 6표면).

## 3. 계약 (BE 와 합의됨 — 이대로 소비)

**이 두 줄만 알면 BE 없이 착수된다:**

1. **필드명 = `surface_key`** — 요청·응답 양쪽 동일, camelCase 변환 없음(현행 `product_slug`·`service_url`·`demo_accounts` 관례). POST 필수 · PATCH 선택(보내면 개명) · **GET 응답 모든 행에 항상 포함**(백필 행은 `"기본"`).
2. **중복 축 = 3축** `(product_slug, environment, surface_key)` — 같은 환경이라도 surface 가 다르면 정상, **셋 다 같을 때만 409**.

그 밖에:
- **400 사유 2종** — 빈 값/공백만 · 50자 초과. 서버가 최종 판정한다.
- **표시 정렬(화면 전용) = 환경 `prod → stg → dev → demo` × surface 오름차순.** ⚠ **신규 카드 환경 select 의 옵션 순서와는 별개 축이다 — 한 배열로 겸하지 마라.** 시안의 `ENVS` ↔ `ENV_DISPLAY_ORDER` 분리가 정본이다.
- `product_slug`·`environment` 는 **불변** — 저장된 행의 환경은 편집 불가(칩만). 옮기려면 삭제 후 재생성.

## 4. 먼저 읽을 핵심 파일 (WP §Code Surface 가 줄번호까지 잡아 놨다)

- `front/components/admin/products/useDeployInfo.ts` — `addEnvBlock` 의 미사용 환경 선택(`:184-193`) · `saveBlock` 의 「환경당 1개」 사전검증(`:229-231`) · `save` 의 `seen` 중복맵(`:326-333`) → **전부 3축으로**. 응답 매핑(`:67`)에 `surface_key`
- `front/components/admin/products/EnvBlockCard.tsx` — surface 입력란 · `usedEnvs` disable(`:98`) **제거** · 저장 행은 환경 읽기전용 칩 · `[삭제]`(`:144`) **확인 단계** · `[+ surface 추가]` CTA
- `front/components/admin/products/EnvBlockView.tsx` — 읽기 전용 표시에 surface (**그 환경 행이 2건 이상일 때만**)
- `front/components/admin/products/DeployInfoModal.tsx` — 표시 정렬 · **평평한 카드 나열(그룹 컨테이너 없음)**

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

**`back/` 금지** — BE 워커 몫이다.

## 6. 해야 할 것 — 계약이 못 박은 자리 넷

1. **환경 소진 규칙 폐지** — `usedEnvs` disable 제거. 같은 환경으로 카드를 여러 장 만들 수 있어야 한다. 사전 검증의 중복 축도 3축으로.
2. **신규 카드 surface 입력은 빈 값 + placeholder** — ⚠ **`기본` 을 프리필하지 마라.** `[+ surface 추가]` 는 이미 그 환경에 카드가 있을 때 누르는 버튼이라, `기본` 카드가 이미 있으면 그 프리필이 **반드시 409 를 부른다.** 빈 채 저장하면 400 인데 그게 **의도한 실패**다 — 「이름을 지어라」가 무의미한 중복 충돌보다 고치기 쉽다. placeholder 문구는 시안 그대로.
3. **삭제 확인 단계** — **시연계정이 1건 이상 딸린 행의 `[삭제]` 는 확인을 거친다.** 확인 문구가 사라지는 것을 말해야 한다(어느 (환경 · surface) 행인지 + 시연계정 N건이 함께 사라진다는 사실). 취소하면 `DELETE` 가 발행되지 않는다. **시연계정 0건 행은 잃을 것이 없어 확인 없이 삭제.** 시안은 `confirm()` 이지만 **실물은 medikit 컴포넌트 판단** — 레포에 쓰던 확인 UI 가 있으면 그걸 쓰고, 없으면 무엇을 골랐는지 보고해라.
4. **표시 정렬 + 평평 카드** — `prod → stg → dev → demo` × surface 오름차순. 그룹 컨테이너를 만들지 마라(정렬 결과로 같은 환경이 붙어 보이는 것이 전부).

## 7. 하지 말 것

- **시안과 다르게 만들지 마라.** 다르게 하고 싶으면 **만들지 말고 보고**해라.
- **`기본` 을 프리필하지 마라.**
- **`back/` 금지.**
- **1루프에서 픽셀·간격·문구를 완벽히 맞추려 시간 쓰지 마라** — 계약대로 세우는 판이다. 눈으로 보고 고치는 건 사용자 E2E 뒤 2루프다.
- **로컬 스택(`make local-stack`)·dev 서버를 띄우지 마라** — 사용자 방침. 포트·프로세스 금지.
- 커밋·push·PR 금지.

## 8. 검증

```
cd front && npx tsc --noEmit
```

(네가 만진 파일 **0 에러**) + `prettier --check <네가 만진 파일만>`. **전체 빌드·전체 포맷 검사 금지 — 사용자 방침. 검증은 1회만.**

기존에 깨져 있던 무관한 실패는 **"무관"으로 분리**해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다 — **이 세션에서 세 번 바뀌었다.** preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --from term_44462bf6-319f-4265-b045-935794944cd0 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고:
  `orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --text "[질문] frontend: <질문>" --enter`
