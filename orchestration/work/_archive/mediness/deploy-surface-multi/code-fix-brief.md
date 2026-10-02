# [backend+frontend 통합] WP-131 검수 지적 반영 — 잠복 버그 4건

너는 **mediness 코드 워커**다(이번 판은 BE·FE 둘 다 네 몫 — 워커 하나로 직렬 처리한다). 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md`·`skills.md`·`tools.md`·`workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 문서들)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **너는 이 작업의 맥락이 하나도 없다.** 앞 판 워커들의 터미널이 **전부 죽었다.** §1 을 먼저 읽어라.
⚠ **워크트리에 미커밋 변경 22파일이 이미 있다.** 그게 앞 판 산출물이고 **네 일은 그 위에 얹는 것**이지 다시 만드는 게 아니다. `git checkout .`·`git add -A`·`git stash` 류 **전체 범위 명령 절대 금지** — 치면 통째로 날아간다.

## 1. 먼저 읽을 것

1. `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/review-code-report.md`
   ← **이번 작업의 지시서 본체. 192줄 전부 읽어라.** 지적이 「파일:줄 + 실패 시나리오 + 권장」으로 들어 있다. 아래 §2 는 **내가 처분을 고른 것**이고 근거·세부는 리포트에 있다.
2. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/30-work/work-131-deploy-surface-axis.md` — 빌드 계획(다른 레포)
3. `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec/products/mediness/20-spec/spec-051-product-deploy-registry.md` — 외부 계약
4. `git -C /Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi diff` — 지금 있는 변경

⚠ `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스-배포정보-추가/orchestration/work/deploy-surface-multi/flaky-baseline-evidence.md` — **기존 실패 12건 판정 끝났다. 재조사·수정 금지.**

## 2. 처분 — 이 넷만 한다

> 검수 판정은 **PASS**(FAIL 0)다. 아래는 전부 **비블로킹 잠복 버그**이고, 지금 고치는 게 나중보다 싸서 닫는다.

### ① W-4 — `text` 이름 가림 (BE, 1줄)

`back/tests/api/test_gm_command.py:18` 의 모듈 레벨 `from sqlalchemy import text` 가, 같은 파일 9곳(`:114,129,137,146,223,242,273,285,297`)의 지역변수 `text = res.json()["text"]` 에 가려진다. **지금은 버그가 아니다** — SQL `text()` 를 쓰는 함수가 지역 `text` 를 안 만든다. **다음 사람이 그 함수들 중 하나에 SQL 한 줄을 넣는 순간 `TypeError`** 가 난다.

→ **`from sqlalchemy import text as sa_text` 로 별칭**을 주고 사용처를 맞춰라. (지역변수명을 바꾸는 쪽은 9곳을 건드리니 택하지 마라.)

### ② W-2 — 상한 50 이 네 곳에 각각 하드코딩 (BE, 단언 1~2줄)

`models/product_deployment.py:50 SURFACE_KEY_MAX_LENGTH = 50` · `alembic/versions/0139_…:64 _MAX_LENGTH = 50` · 테스트 2곳이 `== 50`.

**실패 시나리오**: 누가 `SURFACE_KEY_MAX_LENGTH` 를 100 으로 올리고 migration 을 안 고치면 — 앱이 60자를 통과시키고 DB 가 `VARCHAR(50)` 으로 거부해 **400 이 아니라 500** 이 난다. 지금 테스트는 전부 50 을 하드코딩해 **초록을 유지한다.**

→ **이미 있는 선례를 그대로 따라라.** 같은 레포가 백필 리터럴에 대해선 두 정의가 갈라지는 걸 막는 단언을 심어 놨다(`tests/api/test_admin_deployments.py:628` — migration 소스를 읽어 `_BACKFILL == DEFAULT_SURFACE_KEY` 확인). **상한값에 동형 장치**를 만들어라. 그리고 테스트의 `== 50` 하드코딩을 **`== SURFACE_KEY_MAX_LENGTH`** 로 바꿔 한 곳만 고치면 되게 하라.

### ③ O-3 — 저장도 안 했는데 옆 행에 surface 라벨이 돋는다 (FE)

`front/components/pipeline/DeployInfoSection.tsx:147-150` 이 `showSurface` 를 `d.blocks.filter(같은 환경).length >= 2` 로 세는데, `d.blocks` 에 **아직 POST 안 된 신규 블록이 포함**된다. `[+ surface 추가]` 를 누르는 순간 기존 행 읽기 뷰에 `· 기본` 이 붙었다가, 신규 카드를 취소하면 사라진다.

→ **카운트를 서버에 있는 행 기준으로** 바꿔라(`id !== null` 인 블록만). 계약의 「행 수 ≥ 2 일 때만 표기」는 **서버 상태 기준**이고, `/gm` 도 서버 기준이라 지금은 둘이 순간적으로 어긋난다.

### ④ O-4 — 미저장 초안 삭제에도 파괴적 확인이 뜬다 (FE)

`front/components/admin/products/EnvBlockCard.tsx:79-93` 의 확인 게이트 조건이 `block.accounts.length > 0` 하나뿐이라 **`block.id === null`(아직 서버에 없음)을 안 본다.** `[+ 환경 추가]` → 계정 2줄 입력 → 마음 바꿔 [삭제] 하면 「시연계정 2건이 함께 사라집니다」 + 빨강 파괴적 모달이 뜨는데, **실제로는 서버에 아무것도 없어 로컬 폐기만 한다**.

→ **게이트에 「서버에 이미 있는 행일 것」을 추가**해라(`block.id !== null && accounts.length > 0`). 계약(SPEC §UX)이 말하는 손실은 **저장된 시연계정**이지 입력 중인 초안이 아니다. 문구·스타일은 그대로 두고 **조건만** 좁혀라.

### ⑤ W-1 — FE 자동 테스트 0건 (FE, 신규 1파일)

이번 FE 변경분에 대응하는 `front/__tests__/` 파일이 없다(`grep -rln "Deployment|useDeployInfo" front/__tests__` = 0). WP §Phase 7 이 「P7(수동)」으로 계획했으니 **계획 위반은 아니다** — 다만 리포 관례와 어긋나고, 특히 **AC 14 「삭제 확인 취소 시 네트워크 요청 0」은 회귀가 조용하다.**

→ **최소 1파일** `front/__tests__/wp131-deploy-surface.test.tsx` 를 만들어라. 세 건만:
1. `[+ surface 추가]` 가 **누른 카드 바로 아래**에 삽입되고 **환경을 물려받으며** surface 는 **빈 값**(AC 4·5)
2. **저장된 카드의 환경이 편집 불가**(select 없음, 칩만) (AC 6)
3. **삭제 확인에서 취소하면 `fetch` 가 한 번도 안 불린다** (AC 14)

기존 `front/__tests__/` 의 **최근 파일을 먼저 읽고 그 관례**(렌더 헬퍼·모킹 방식)를 따라라. 새 방식을 발명하지 마라.

## 3. 하지 말 것

- **O-1·O-2·O-5 는 건드리지 마라.** 사용자 E2E 뒤 2루프 몫이다(모달 배치 저장 중단 정책 · 층별 정렬 차이 · 안내문 반복). **화면 결정이라 사용자가 봐야 한다.**
- **W-3 은 조치 없음** — 계약 위반이 아니다(시안도 클라이언트 차단이고 서버 400 경로는 살아 있으며 테스트로 고정돼 있다).
- **계약을 바꾸지 마라** — 3축 유니크·`기본` 비-sentinel·`/gm` 표기 규칙·에러 문구·`ProductLinks` shape·권한·환경 enum 전부 불변.
- **12건 기존 실패를 고치려 들지 마라.**
- **WP·SPEC 문서를 고치지 마라** — 다른 레포, 코디 몫.
- **로컬 스택·dev 서버·포트 금지.**
- 커밋·push·PR 금지.

## 4. 검증

**네가 만진 파일만. 전체 스위트·전체 빌드 금지 — 사용자 방침. 검증은 1회만.**

```
cd back && uv run python -m pytest tests/api/test_gm_command.py tests/api/test_admin_deployments.py -q
cd front && npx tsc --noEmit && npx vitest run __tests__/wp131-deploy-surface.test.tsx
```

- `back` 쪽 `test_admin_deployments.py` 는 **12 failed 가 정상**이다(기존·환경 문제, 판정 파일 참조). **36 passed 가 유지되는지**만 본다.
- `front` 에 `node_modules` 가 없으면 메인 체크아웃(`/Users/kknaks/git/harness_works/mediness-app/front/node_modules`)을 심볼릭 링크로 걸고 **검증 후 반드시 제거**해라(남으면 다음 사람 dev 서버가 500 난다).
- `ruff` 는 변경 파일 한정.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값은 브리프 작성 시점 것이고 **이 세션에서 세 번 바뀌었다.**

- 보고 본문에 **①~⑤ 번호마다 고친 자리(파일:줄) 또는 「조치 없음 + 사유」**를 한 줄씩. 빠진 번호가 있으면 안 된다.

```bash
orca orchestration send \
  --to term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --from term_6caf0195-f54d-4b50-ac72-a2b4c4c57893 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "code-fix 완료: <한 줄>" \
  --body "①~⑤ 처리 결과 / 검증 수치 / 미결·주의점"

orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 \
  --text "[worker_done] code-fix 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_738cfbd7-e3b8-4712-9ff5-f6ee713d4be1 --text "[질문] code-fix: <질문>" --enter`
