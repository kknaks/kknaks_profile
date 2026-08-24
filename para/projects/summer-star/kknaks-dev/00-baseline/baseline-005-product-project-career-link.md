---
type: baseline
id: KDEV-BL-005
title: "제품·프로젝트·커리어 연동 + 레지스트리 관리 화면"
status: raw
product: kknaks-dev
source:
  type: idea
  ref: "kknaks 요청 2026-08-03 — 파일 기반 데이터 DB화 검토, 프로젝트/프로덕트부터"
links:
  baselines: []
  decisions:
    - "[[decision-017-product-registry-and-admin-scaffold|KDEV-DEC-017]]"
  specs:
    - "[[spec-014-product-registry-and-admin|KDEV-SPEC-014]]"
  works:
    - "[[work-018-product-registry-admin|KDEV-WORK-018]]"
  releases: []
  related:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
    - "[[baseline-002-app-db-and-admin|KDEV-BL-002]]"
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/raw
---

# 제품·프로젝트·커리어 연동 + 레지스트리 관리 화면

**제품(`products/**` 내부 문서)·프로젝트(`showcase.md` 공개 카드)·커리어(`persona/career/`)는 같은 커밋에서 나오는데, 셋을 잇는 키가 시스템에 없다.** 그 키를 레지스트리에 만들고, 레지스트리를 관리 화면에서 다루고, 그다음 잔디 잡이 그 키를 따라 제품까지 갱신하게 한다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

> kknaks 요청 (2026-08-03). 대화 중 방향이 두 번 크게 바뀌었고, **바뀐 뒤의 결론**을 적는다.

**처음 발주**

- 파일 기반 데이터(`persona/algorithms` 76 · `daily` 93 · `contents` 24 · `career` 5 · `posts` 1 · `profile.md` · `_map.md` · `showcase.md` 13)의 **DB화 후보를 판정**한다. 전부 옮기는 것이 목표가 아니다.
- admin 사이드바의 `soon` 자리 여섯(콘텐츠·노트·프로젝트·알고리즘·커리어·설정)을 **무엇으로 채울지** 정한다.
- 판단 축: 사람이 쓰는가 / git 이력이 의미를 갖는가 / 승인 게이트가 이미 쓰는가 / Obsidian 으로 여는가 / 부팅 로드 비용.
- `tracked_repos` 이관([[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]])이 이 발주의 선례다.

**정정 ① — 프로젝트와 프로덕트부터, 그리고 "이 둘은 연동돼 있는 것 아닌가"**

> "프로젝트 → 블로그에 노출 / 프로덕트 → 상세스펙·개발계획 등을 담는 내부 옵시디언 문서. 이거 사실 2개는 상호 연동 되어 있는 거 아니야?"

맞다. 다만 연동이 **폴더명 하나**로만 돼 있고 이미 깨져 있다(아래 Context).

**정정 ② — showcase 는 md 로 남긴다 (설계가 여기서 뒤집혔다)**

> "아니 지금 showcase 남겨야 할 거 같은데? 지금 결과 문서는 md로 계속 관리해야. 내가 로컬에서 md 작업 하지 않을까."

- 본문을 DB 로 옮기는 안(`project_detail` 테이블)을 **폐기**한다. 카드 본문은 Obsidian 에서 사람이 쓴다.
- 그러면 **DB 가 가질 것은 조인과 운영 상태뿐**이다. 옮길 데이터가 사실상 없다.

**정정 ③ — 낡음의 해법이 "관리 화면 편집" 이 아니라 "잔디 잡 확장" 이다**

> "잔디잡 → career / product / 잔디 이렇게 올려야 하겠네? 잔디잡 스케줄 → 정보 조회 → 어디에 뭐 쓸지 카탈로그 동적 생성 할 수 있을 것 같아서."

- career 는 이미 커밋에서 자동 갱신된다. **product 만 그 경로가 없다.**
- 목적지 카탈로그를 레지스트리에서 동적으로 만든다 — 지금 `career_map` 이 하는 일의 product 판.

**확정된 범위 (P1 / P2)**

```text
P1  product_slug 컬럼 + admin 레지스트리 CRU + 깃 연동
P2  잔디 산출물에 product 추가 (목적지 카탈로그 동적 생성)
```

- **CRUD 가 아니라 CRU.** `D` 는 [[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] D2 가 `enabled` 컬럼에 *"삭제 대신 끄기"* 로 이미 정해 뒀다.
- **제품 디렉토리를 화면에서 만들지 않는다.** 이미 있는 것 중에서 고른다(드롭다운). 새 제품은 baseline 부터 시작하는 것이지 관리 화면에서 생기지 않는다.
- **깃 연동을 P1 에 포함한다** — 등록 즉시 `sync_repo` 를 돌려 오타·토큰 실패를 그 자리에서 드러낸다.

## Context

작업 착수 시점(2026-08-03) 실측. 워크트리 `work-018-db` @ `d848b00`.

### 제품 18개 · showcase 13개 — 형태가 셋으로 갈린다

| 형태 | 개수 | 제품 |
|---|---:|---|
| showcase 만 (stage 0) | 7 | centurion-charty · centurion-mso · linky · mediness · nexus · **kknaks-profile · summer-star-company** |
| showcase + 파이프라인 | 6 | language-diary · mykakao · open-kknaks · persona-counselor · study-timelapse · wine-log |
| **파이프라인만 (showcase 없음)** | **5** | ax-knowledge-graph · cloud-file-organizer · **kknaks-dev** · mac-remote · mini-game |

[[spec-001-directory-structure|KDEV-SPEC-001]] §5 의 계약은 *"회사 프로젝트 = `showcase.md` 만, 개인 제품 = showcase + 파이프라인"* 인데, **셋째 줄 5개가 그 계약 밖에 있다.** `_load_products_showcase()` 가 `products/*/showcase.md` 만 긁으므로 이 5개는 `/api/projects` 에 뜰 방법이 없다.

`products/README.md` 의 제품 목록도 **18개 중 9개만** 적고 있다(ax-knowledge-graph·mini-game 처럼 파이프라인 있는 것도 누락).

### 같은 제품이 두 폴더로 쪼개져 있다

```text
products/kknaks-profile/showcase.md   id: P-02 · org: studio · "kknaks.dev"
                                       links.repo: github.com/kknaks/kknaks_profile
                                       ← 파일 이거 하나뿐
products/kknaks-dev/00-baseline…40-    "kknaks.dev와 이 레포 자체를 제품으로 운영하기 위한 SSOT"
```

**하나의 제품이다.** 두 폴더 사이에 링크가 없고 폴더명이 달라 폴더명 조인도 안 된다. `log.md` 보유가 이 갈림을 그대로 비춘다 — 파이프라인 있는 11개에만 있고, showcase-only 7개에는 없다.

### 조인 지점 넷 — 전부 약하거나 음의 신호다

| 지점 | 실제 결합 |
|---|---|
| 조인 키 | **디렉토리명뿐.** showcase frontmatter 에 제품을 가리키는 필드가 없고, 제품 문서에도 showcase 링크가 없다 |
| 지식그래프 | **showcase.md 는 노드가 아니다.** `persona_loader.py:238` 이 명시적으로 건너뛴다 — *"stem 동일 → 노드로 잡으면 L2 중복 폭발"* |
| doc pipeline | showcase 를 **음의 신호로만** 안다 — "showcase 有 + stage 無" 면 stage README 강제 면제(`product_doc_pipeline.py:195`). 둘의 연결은 검사하지 않는다 |
| `tracked_repos` | [[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] 가 `links.repo` 를 떼어 갔다. **제품을 가리키는 컬럼은 없다** |

### showcase 13개가 34일째 무수정이다

전부 마지막 수정이 같은 커밋이다 — `2026-06-30 feat(kg): WORK-004 projects→products/showcase 마이그레이션`.

| 축 | 값 |
|---|---|
| `(TBD)` 스텁 | 6 (centurion-charty·centurion-mso·linky·mediness·nexus·mykakao) |
| `visible: true` (사이트 노출) | 6 (kknaks-profile·language-diary·open-kknaks·persona-counselor·study-timelapse·wine-log) |
| `date` 최신 | 2026.06 (mykakao). 나머지 2026.02~05 |

**`org` 로 깨끗하게 갈린다** — `company` 5개는 **전부** `visible:false` + `(TBD)`. 카드로 쓸 의도가 없었고, 그 파일들이 존재한 이유는 "잔디가 긁을 레포 목록의 원천" 이었는데 DEC-014 가 그 역할을 가져갔다.

**낡은 것은 카드 내용이 아니라 모집단이다.** 최근 실작업(kknaks-dev WORK-011~017 · ax-knowledge-graph 스펙 12건 · mac-remote · cloud-file-organizer)은 전부 카드 없는 5개에 있다. 사이트에 보이는 6장은 2~5월 것이다.

### career 축은 이미 목적지가 데이터에서 나온다 — product 만 없다

```text
tracked_repos.detail ─→ collect_git.py:140  career_attribution(commits, detail_by_repo)
                     ─→ career_map { "medisolve-ai": [repo, …] }
                     ─→ daily.py:109  career_targets()   ← 목적지를 결정적으로 고른다
```

`daily.py:110` 주석: *"갱신 대상 career. **결정적으로 고른다 — 모델에게 묻지 않는다.**"* `product_slug` 컬럼을 넣으면 같은 기계가 `product_map` 을 낸다. **P2 는 신설이 아니라 대칭 채우기다.**

오타 방어도 이미 형태가 있다 — `missing_career()`(`daily.py:142`)가 `detail` 이 가리키는 문서 부재를 승인 화면까지 들고 간다. `daily.py:151` 이 그 방식을 택한 이유를 명시한다: *"DB 계층이 레포 파일시스템을 알게 되고, 나중에 career 파일 이름이 바뀌면…"* — **DB CHECK 로 파일 존재를 강제하지 않는다.**

### 레지스트리에 없는 레포 4개 — 잔디가 놓치고 있을 수 있다

카드 없는 5개 제품의 코드 레포가 `tracked_repos` 13행에 아예 없다.

| 제품 | Remote | 편입 |
|---|---|---|
| ax-knowledge-graph | README 상 `TBD`, 본문에 `kknaks/ax-graph` | 확인 필요 |
| cloud-file-organizer | `kknaksss/gcs_demo` | 가능 |
| mac-remote | Swift 별도 레포, README 에 Remote 없음 | 확인 필요 |
| mini-game | README 상 `TBD`, local clone `lunch_game` | 확인 필요 |
| kknaks-dev | `kknaks/kknaks_profile` | **이미 등록됨** (kknaks-profile 카드의 slug 로) |

그 레포들에 커밋했다면 **그날 daily 에 안 실렸다.**

### 등록 오타가 다음 날 09:05 까지 숨는다

`sync_repo`·`sync_all`(`service/jobs/repos.py`)을 부르는 곳은 **`collect_git.py:92` 한 군데뿐**이다. 잡 안에서만 돈다.

DEC-014 D2 가 시드를 자동화한 근거가 정확히 이것이다 — *"손으로 13행을 넣으면 slug 오타가 조용히 '추적 안 됨' 이 되는데, 그 실패는 로그에도 안 남는다."* **이번에 만들려는 것이 바로 손입력 화면이라, 즉시 검증 없이는 그 결정을 정면으로 거스른다.**

기계는 이미 있다 — `sync_repo(slug, account) -> SyncResult`, `last_fetched_at`·`last_error` 컬럼, SPEC-011 §4 Case Matrix 에러 코드, `_scrub()` 토큰 마스킹, `assert_outside_worktree()`.

### 토글이 둘인데 하나만 DB 다

| 토글 | 뜻 | 위치 |
|---|---|---|
| `enabled` | 잔디가 **긁을까** | `tracked_repos` (DB) |
| `visible` | 사이트에 **보여줄까** | `showcase.md` frontmatter (파일) |

`visible` 을 DB 로 올리면 **`/api/projects` 가 처음으로 Postgres 를 읽는다.** 지금 공개 API 는 전부 in-memory dict 다.

### 제품 문서 생성은 발행 계약 밖이다

`apply/plan.py:25 ALLOWED_PREFIXES` 에 `products/` 가 **없다.** 파일 쓰기는 `apply/executor` 독점이고([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D2), `POST /admin/reload` 의 `git reset --hard origin/main` 이 미커밋 파일을 지운다. **제품 디렉토리를 화면에서 만드는 것은 작은 일이 아니다.**

### DB화 후보 판정 (원 발주 ①에 대한 답)

| 데이터 | 규모 | 작성 주체 | git 이력 | 게이트 allowlist | 그래프 | 판정 |
|---|---:|---|---|---|---|---|
| `persona/algorithms/` | 76 | **잡 100%** | 노이즈 | ✗ | ✗ | **DB — 최우선** (별도 후속) |
| `persona/_map.md` | 1 | 스크립트 | 노이즈 | ✗ | ✗ | **폐기 → 화면이 대체** |
| `persona/contents/` | 24 | 잡 + 게이트 | 의미 있음 | ✓ | ✗ | 혼합 — 본문 파일 / `status` 큐 DB |
| `persona/daily/` | 93 | 게이트 | **커밋이 곧 기록** | ✓ | ✗ | **파일 유지** |
| `persona/career/` | 5 | 사람(fm) + 게이트(본문) | 의미 있음 | ✓ | ✗ | **파일 유지** |
| `products/*/showcase.md` | 13 | 사람 | 의미 있음 | ✗ | **✗ (제외돼 있다)** | **파일 유지 — 조인만 DB** |
| `persona/profile.md` | 1 | 사람 | 의미 있음 | ✗ | ✗ | **파일 유지** |
| `persona/posts/` | **0** | — | — | ✗ | ✗ | **판정 불가** — README 뿐 |

**이 baseline 이 다루는 것은 `showcase.md` 줄 하나다.** `algorithms`·`_map.md`·`contents` 는 별도 후속으로 남긴다.

판단 축 둘이 실측으로 무력화됐다.

- **부팅 로드 비용은 근거가 되지 않는다.** 부팅이 읽는 md 약 641개 중 **428개가 `products/**`**(`_build_graph_nodes` 의 그래프 빌드)다. persona 199개를 통째로 옮겨도 31% 만 준다.
- **DB화가 커밋 수를 줄인다.** `config.bot_identity()` 가 `gh_accounts()[0]` = 개인 계정이라 봇 커밋과 사람 커밋의 author 가 같고, DEC-014 D5 의 `--author=kknaks` 부분매칭이 봇 커밋도 잡는다. 잡 산출물을 DB 로 옮기면 그만큼 잔디에서 빠진다.

## Why It Matters

- **최근 작업이 사이트에 하나도 없다.** 카드 13장이 34일째 그대로고, 그동안 한 일은 카드가 없는 제품들에 있다. 포트폴리오 사이트의 모집단이 낡았다.
- **career 는 자동 갱신되는데 product 는 안 된다.** 같은 커밋, 같은 조사 결과에서 한쪽만 흐른다. `type=studio` 커밋은 daily 의 `counts` 에만 남고 제품 문서로 가지 않는다.
- **관리 화면이 오타 경로를 새로 연다.** DEC-014 가 자동 시드로 피한 문제를 손입력 화면이 되살린다. 깃 연동이 P1 에 붙어야 하는 이유다.
- **제품·프로젝트·커리어를 잇는 키가 없다.** `kknaks-dev`/`kknaks-profile` 처럼 이미 갈라진 곳이 있고, 갈라졌다는 사실을 알려 주는 장치가 없다.
- **`products/` 폴더 안에 사는데 그래프 밖인 파일이 13개 있다.** showcase 는 노드가 아니라서 L1~L6 이 안 본다. 링크가 깨져도 아무도 모른다.

## Possible Direction

아직 결정은 아니다. decision 에서 확정한다.

### P1 — 컬럼 + 레지스트리 관리 화면 + 깃 연동

| 구분 | 내용 |
|---|---|
| 스키마 | `alembic 0009` — `tracked_repos.product_slug` nullable |
| 검증 | **DB CHECK 로 안 건다.** 응답에 "그 `products/{slug}/` 가 실재하나" 를 얹는다 (`missing_career` 방식) |
| API | `GET /api/admin/repos` · `POST` 등록 · `PATCH` 수정 · `POST /{id}/sync` |
| 깃 | 등록·수정 시 백그라운드 `sync_repo`, 결과를 `last_error` 로. `BackgroundTasks`(`reload.py:142` 선례) |
| FE | **프로젝트** 슬롯 — 표 · `enabled` 토글 · 제품 드롭다운 · fetch 버튼 · 상태 |
| 시드 | 13행 손으로. **문자열 유도가 안 된다** — `kknaks/kknaks_profile` 이 `kknaks-profile` 인지 `kknaks-dev` 인지 코드가 모른다 |
| 제외 | 제품 문서 생성/삭제(파일) · `visible` 토글(파일) · 잔디 산출물 확장(P2) |

배관은 전부 있다 — `require_admin`(`auth.py:48`) · `get_db` · `queue.py:45` 라우터 선례 · admin 셸 · 사이드바 `ready` 기계 · `TrackedRepo` 모델. WORK-011(관리자 인증 MVP)과 비슷한 크기다.

관계 모양은 **한 컬럼**으로 시작한다. 별도 `projects` 테이블을 두지 않는 이유는 본문이 파일에 남아 담을 것이 없어서다. 한 레포에 제품이 둘인 경우(`kknaks-dev`/`kknaks-profile`)는 컬럼이 레포 쪽에 있으면 **표현할 수 없으므로**, 그 둘을 합칠지가 선결이거나 조인 테이블이 필요하다.

### P2 — 잔디 산출물에 product 추가

```text
스케줄 09:05
  → intake_daily(date)
  → collect       커밋 조사 + career_map + product_map   ← P1 컬럼이 여기서 쓰인다
  → investigate   레포별 fan-out
  → daily 게이트
       ├ persona/daily/{date}.md      항상            (있음)
       ├ persona/career/{stem}.md     company 귀속     (있음)
       └ products/{slug}/???          studio 귀속      (신설)
```

`career_targets()` → `product_targets()`, `missing_career()` → `missing_product()` 로 복제된다. 진짜 결정은 **목적지 하나**다.

| 후보 | 성격 | 문제 |
|---|---|---|
| `products/{slug}/log.md` | 날짜별 누적. **daily 와 성격이 같다** | showcase-only 7개엔 파일이 없다 |
| `products/{slug}/showcase.md` | 공개 카드. **사람이 로컬에서 쓰는 문서** | 덮어쓰면 사람 글이 날아간다 — career 규율(본문만·append 금지·압축 재서술·사람 전용 필드 보호) 각색 필요 |
| `products/{slug}/30-work/*` | 작업 문서 | 발주는 사람이 하는 것. 너무 무겁다 |

[[work-017-grass-commit-pipeline|KDEV-WORK-017]] Scope 제외 첫 줄이 *"`products/*/30-work`·`showcase.md`·`persona/posts/` 목적지 → 후속"* 이다. P2 가 그 후속이다.

`ALLOWED_PREFIXES` 에 `products/` 를 여는 순간 발행부가 제품 문서를 쓸 수 있게 된다 — **allowlist 를 얼마나 좁게 여는지**가 P2 의 안전 설계다.

### 관리 화면 여섯 슬롯의 성격

SoT 위치가 화면의 성격을 결정한다.

| SoT | 화면이 하는 일 | 슬롯 |
|---|---|---|
| DB | 진짜 CRU | 프로젝트(레지스트리) · 알고리즘(후속) |
| 파일 | **조회 + 게이트 발주.** 화면이 직접 쓰지 않는다 | 콘텐츠 · 노트 · 커리어 |
| — | 토큰·주기·상한 | 설정 |

파일을 화면에서 직접 못 고치는 것은 취향이 아니다. `reset --hard origin/main` 과 `apply/executor` 독점 두 계약을 동시에 깨기 때문이다.

## 미결 (decision 대상)

1. **레포 4개 편입 여부** — `ax-graph`·`gcs_demo`·mac-remote·`lunch_game`. Remote 가 `TBD` 인 것이 둘이라 등록하면 `REPO_NOT_FOUND` 로 떨어진다. 깃 연동이 붙으면 **등록해 보면 답이 나온다.**
2. **`kknaks-dev` + `kknaks-profile` 를 한 제품으로 합칠지** — 합치면 `product_slug` 가 예외 없는 조인 키가 되고 컬럼 하나로 끝난다. 안 합치면 조인 테이블이 필요하다.
3. **P2 목적지** — `log.md` / `showcase.md` / 둘 다(누적 vs 압축 재서술).
4. **잔디 셋째 산출물** — `concept` 을 product 로 대체할지, 넷째로 더할지. WORK-017 Open Issue 에 *"`permanent/concept/` 발행 경로가 어디서도 안 탔다"* 가 남아 있다.
5. **`visible` 을 DB 로 올릴지** — 올리면 공개 API 가 Postgres 를 읽는 첫 사례가 된다.
6. **회사 5개 showcase.md 를 지울지** — 역할이 끝났다. 지우면 `/api/projects` 모집단이 13 → 8 로 줄지만 `visible:false` 라 화면 변화는 없다.
7. **`products/README.md` 제품 목록 갱신 주체** — 18개 중 9개만 적혀 있다. 손으로 둘지, 화면/스크립트가 낼지.
8. **showcase 를 그래프 노드로 승격할지** — `persona_loader.py:238` 주석이 *"product-as-node 는 SPEC-002 후속"* 이라고 남겨 뒀다. `product_slug` 가 생기면 stem 중복 문제를 풀 재료가 생긴다.
