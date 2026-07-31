---
type: decision
id: KDEV-DEC-014
title: "커밋 조사 원천 — 레포 레지스트리 DB화 + 로컬 bare 클론"
status: proposed
product: kknaks-dev
created_at: 2026-07-31
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-016-grass-gate-and-publish|KDEV-DEC-016]]"
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
---

# 커밋 조사 원천 — 레포 레지스트리 DB화 + 로컬 bare 클론 (ADR-014)

잔디가 무엇을 추적할지는 **DB 레지스트리**가 정하고, 커밋을 무엇으로 조사할지는 **서버에 클론한 bare 레포**가 정한다. GitHub API 커밋 조회를 대체한다.

> [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]] 의 1·2번. 착지 경로는 [[decision-015-grass-destinations-and-formats|KDEV-DEC-015]], 게이트 편입은 [[decision-016-grass-gate-and-publish|KDEV-DEC-016]] 이 다룬다.

## Context

- 관련 baseline: [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]
- **추적 대상이 md 에서 온다.** `products/*/showcase.md` 의 `links.repo` → `_load_products_showcase()` → `get_data()["projects"]` → `main_job.py:80-82`. 현재 13개. 스케줄러가 persona 메모리에 의존한다.
- **입력이 얇다.** `inputs.py:208-212` 의 `fetch_repo_commits()` 는 `{"repo", "msg"}` 둘만 돌려준다. diff·파일 통계·sha·브랜치가 없어, `2026-07-28.md` 의 `commit: 25` 가 커밋 메시지 25줄만을 근거로 2줄로 압축됐다. **커밋 서술 품질의 병목은 프롬프트가 아니라 입력이다.**
- **API 로는 상세를 못 받는다.** 커밋별 `files[]`·`stats` 는 `/repos/{o}/{r}/commits/{sha}` 를 커밋당 1회 불러야 한다(N+1). 목록 endpoint 는 default branch 만 본다 — feature 브랜치 작업이 통째로 누락된다.
- **author 필터 기준이 다르다.** 지금은 GitHub username 을 API 에 넘기지만(`main_job.py:96`), 로컬 `git log` 는 author name/email 로만 매칭한다. `config.py:65` 주석은 "email 이 commit author 필터" 라고 적어 놓고 실제로는 `bot_identity()`·`bot_emails()` 에서만 쓰인다.
- **레포 루트 아래에 클론을 둘 수 없다.** compose 가 `.:/repo` 를 rw 로 마운트하고, `reload.py` 의 `git reset --hard origin/main` 과 `apply/git.py rollback()` 의 `git clean -fd` 가 그 아래를 쓸어낸다.
- **워커는 `/repo:ro`** — "capture worker 가 repo-local skill 을 읽되 파일은 쓰지 못하게 한다"가 명시된 설계다.
- **예산이 실질 상한이다.** `worker/run.py:36-39` `CostMiddleware(worker_budget_usd=5.0, global_budget_usd=20.0)`. 매일 도는 잡이다.

## Options

### 추적 목록의 SoT

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `showcase.md` 유지 | 원천 하나 | 프론트 표시용 필드가 잡의 설정을 겸한다. 표시와 추적을 따로 못 정한다 |
| **B** | **DB 레지스트리 신설, showcase 는 표시 전용** | 표시/추적 분리, 계정·경로규칙 등 잡 전용 값을 붙일 자리 | 두 값이 갈라질 수 있다 |

### 커밋 상세의 원천

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | GitHub API 커밋별 상세 호출 | 클론 불필요 | 커밋당 1회(N+1), rate limit, default branch 만 |
| **B** | **서버에 bare 클론 + 로컬 git** | 호출 0, `--all` 로 전 브랜치, `--numstat`·diff 무료 | 디스크, 초기 클론 시간 |

### 클론 방식

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A** | **bare full clone + 주기 fetch** | 단순, diff 가 항상 로컬, 과거 이력 전부 | 디스크를 가장 많이 쓴다 |
| B | partial (`--filter=blob:none`) | 디스크 절약 | 조사할 때마다 blob 페치 — 네트워크 실패가 조사 실패로 |
| C | shallow (`--depth`) | 디스크 최소 | 조상 부재로 diff 실패 가능, 과거 이력 없음 |

## Decision

### D1. 추적 SoT 를 DB 로 옮기고, `showcase.md` 는 표시 전용으로 남긴다

`links.repo` 는 프론트 `project-detail.tsx:121-123` 이 GitHub 링크로 렌더하므로 **삭제하지 않는다.** 역할만 나눈다.

- `showcase.md links.repo` — 공개 사이트에 **보여줄 링크**
- DB 레지스트리 — 잔디가 **커밋을 긁을 대상**

둘이 갈라질 수 있음을 감수한다. 보여주지만 안 긁는 레포, 안 보여주지만 긁는 레포가 정당한 상태다.

`main_job.py:80` 의 `from main import get_data`(순환 import 회피용 지역 import)와 `inputs.py:145 extract_tracked_repos()` 는 제거된다.

### D2. 레지스트리 행

```text
slug            "owner/name"           unique
type            company | studio
detail          career 파일 stem       type=company 일 때 필수, studio 는 null
account         personal | company     클론·fetch 토큰 선택
enabled         bool                   삭제 대신 끄기
path_rules[]    "app/back/**" → "backend"
last_fetched_at timestamptz | null
last_error      text | null
```

- `detail` 은 **career 파일 stem 그대로** 쓴다(`medisolve-ai`). `medisolve` 로 두면 매핑 테이블이 하나 더 생긴다.
- 클론 운영 상태(`last_fetched_at`·`last_error`)는 **이 행에 둔다.** 13행짜리에 테이블 둘은 과하다. 행이 수백 개가 되거나 클론 이력이 필요해지면 그때 분리한다 — 그때 옮기는 비용도 작다.
- `type`·`detail` 이 career 귀속을 정하는 방식은 [[decision-015-grass-destinations-and-formats|KDEV-DEC-015]] D4 에서 계약된다.

**`path_rules` 는 전역 기본값 + 레포별 예외다** (OQ-3 해소). 13개 레포에 전부 적으면 레포 구조가 바뀔 때마다 손봐야 한다.

```text
전역 기본   app/back/**·**/backend/**   → backend
            app/front/**·**/frontend/** → frontend
            products/**·docs/**·*.md    → docs
            *.yml·*.yaml·Dockerfile*    → infra
행별 예외   위 관례를 안 따르는 레포만 적는다. 비어 있으면 기본값만 적용
```

**초기 시드는 `showcase.md` 에서 1회 이관한다** (OQ-4 해소). `links.repo` 13건을 파싱해 `slug` 를 만들고 `org`(`company`/`studio`)를 `type` 으로 옮긴다. `detail` 만 손으로 채운다(company 5건). 손으로 13행을 넣으면 slug 오타가 조용히 "추적 안 됨" 이 되는데, 그 실패는 로그에도 안 남는다.

### D3. 커밋 원천을 로컬 bare 클론으로 바꾼다

```bash
git clone --bare                                    # 최초 1회
git fetch --all --prune                             # 잡 진입 시
git log --all --numstat --format=... \
        --author=kknaks \
        --since "{date}T00:00:00+09:00" \
        --until "{date+1}T00:00:00+09:00"
```

`--all` 을 쓴다. **실측(`mediness`): 전체 2,556 커밋 vs `main` 2,178 — 378건(+17.3%)이 브랜치에만 있다.** 본인 커밋만 봐도 1,067 vs 989 로 **78건(+7.9%)** 이 default branch 밖이다. 그 손실이 중복 위험보다 크다(중복은 D6 이 처리한다).

**bare full clone** 을 채택한다. 워크트리가 없어 `.git` 만 차지하면서 `log`·`show`·`diff` 가 전부 로컬에서 되고, 네트워크 왕복이 조사 경로에 끼지 않는다.

**디스크는 제약이 아니다** (OQ-1 실측). `mediness` bare = **129M**(size-pack 117.7 MiB, 객체 27,946). GitHub API `size` 대비 배율 **×1.16** 으로 13개 레포 합계 API 276.9 MB → **환산 약 321 MB**. `mediness`(111MB)·`persona_counselor`(69MB)·`study_timelapse`(42MB) 셋이 80%이고 나머지 10개는 합쳐 55MB 다. partial 로 낮출 이유가 없다.

### D4. 클론은 레포 루트 밖 전용 볼륨에 둔다

```yaml
volumes:
  repo-cache:/cache/repos      # back 에 rw
```

**워커 마운트는 건드리지 않는다.** diff 는 **back 이 텍스트로 뽑아 프롬프트에 주입**한다. 클론 볼륨을 워커에 마운트하고 AI 가 직접 뒤지게 하는 대안은 조사 깊이는 좋아지지만 워커가 전체 코드에 상시 접근하게 되고 토큰 사용량을 통제할 자리가 사라진다.

### D5. author 매칭은 **identity 패턴 하나 + drift 감지**다

GitHub username 을 API 에 넘기던 것(`main_job.py:96`)이 로컬 `git log` 에서는 통하지 않는다. `git log` 는 author **name/email 부분매칭(정규식)** 만 안다.

**실측 결과 identity 가 셋이었다** (OQ-2, `mediness` bare clone + 개인 레포 API):

| commit email | commit name | 출처 |
|---|---|---|
| `kknaks@medisolveai.com` | `kknaksss` · `이건학` | GitHub 계정 `kknaksss` (회사) |
| `benesia93@naver.com` | `kknaks` | GitHub 계정 `kknaks` (개인, PAT) |
| `kknaks@kknaksui-MacBookAir.local` | `kknaks` | `git config` 미설정 기기 |

`kknaks@medisolveai.com` 하나만 걸었다면 **`kknaks_profile` 최근 100커밋 중 50건(절반)을 잃었다.** GitHub API 는 계정에 묶인 이메일을 전부 인식해 주기 때문에 지금까지 드러나지 않았다.

**결정: `--author=kknaks` 단일 패턴을 쓴다.** 부분매칭이라 위 셋을 전부 덮는다 — email 셋 모두 `kknaks` 를 포함하고, name `kknaksss` 도 포함하며, `이건학` 은 email 로 걸린다. `mediness` 참여자 22명 중 `kknaks` 부분문자열을 가진 사람은 본인뿐이라 오탐도 없다.

**고정 email 목록은 채택하지 않는다.** 새 기기에서 `git config` 를 안 하면 `<user>@<hostname>.local` 이 또 생기는데(실측에서 이미 1건), 목록은 그때마다 조용히 샌다.

**identity drift 감지를 붙인다.** fetch 후 `git log --format='%an <%ae>' | sort -u` 로 그 레포의 매칭 identity 목록을 뽑아, **알려진 목록에 없는 것이 나오면 Slack 으로 알린다.** 양방향으로 쓴다 — 새 기기의 미설정 identity(누락)와, 다른 사람이 패턴에 걸린 경우(오탐)를 같은 장치가 잡는다. 조용히 어긋나는 것이 이 문제의 본질이므로 목록을 고정하는 것보다 **새 것을 발견하는 쪽**이 맞다.

`config.py:65` 주석("email 은 commit author 필터")과 구현의 불일치는 이 결정으로 해소된다 — 필터는 email 목록이 아니라 identity 패턴이 된다.

### D6. 중복 제거는 `(repo, tree-hash)`

`--all` 을 쓰면 squash merge 레포에서 같은 작업이 브랜치 커밋 + merge 커밋으로 두 번 잡힌다. 두 커밋은 **메시지가 다를 수 있어** 현행 `(repo, msg)` 키(`main_job.py:99`)로는 안 걸린다.

`git log --format=%T` 의 tree hash 가 같으면 결과 트리가 같은 작업이다. 이 키로 dedupe 한다.

**실측(`mediness`): 중복 tree 그룹 157개, 걸러질 커밋 163건.** D3 이 `--all` 로 얻은 378건 중 절반 가까이가 중복이었다 — dedupe 없이 `--all` 만 켜면 `counts["commit"]` 이 그만큼 부푼다. 두 결정은 짝으로 가야 한다.

### D7. diff 입력 상한

| 축 | 값 |
|---|---|
| 레포당 diff 총량 | 32KB |
| 커밋당 diff | 8KB |
| 레포당 커밋 | 30건 |

초과분은 diff 본문을 버리고 `--numstat` 요약(파일명 + ±라인)만 넣는다. **상한에 걸렸다는 사실을 payload 에 남긴다** — 조용히 잘리면 왜 그날 서술이 얕은지 화면에서 알 수 없다.

### D8. 회사 레포도 diff 를 전부 포함한다 — 레포별 차등 없음

author 필터가 내 커밋만 가져오므로 남의 코드를 긁는 문제가 애초에 없다. 조사 깊이는 **균일하게 깊게** 하고, 무엇을 공개할지는 [[decision-016-grass-gate-and-publish|KDEV-DEC-016]] 의 승인 게이트에서 사람이 정한다.

조사 결과는 DB(비공개)에 들어가고, 공개되는 것은 발행된 md 뿐이다. 이 둘을 같은 문제로 묶어 조사 단계에서 미리 깎으면, 정작 필요한 서술까지 못 만들면서 공개 통제는 게이트에 그대로 남는다.

### 기각

- **레포별 조사 깊이 차등** — 조사(DB)와 공개(md)는 다른 축이다. 게이트가 이미 공개 축을 담당한다.
- **회사 레포 추적 제외** — commit count 가 크게 줄고 `medisolve-ai` career 가 영영 갱신되지 않는다.
- **partial / shallow clone** — 조사 신뢰성을 디스크와 바꾼다. 디스크가 실측으로 문제가 될 때 전환한다.
- **워커에 클론 볼륨 마운트** — `:ro` 설계 의도(워커는 읽고 쓰지 않는다)를 넘고, 토큰 통제 지점이 사라진다.
- **GitHub API 커밋별 상세 호출** — N+1 이고 default branch 한계가 남는다.
- **`(repo, msg)` dedupe 유지** — squash merge 를 못 잡는다.

## Rationale

- **판단 기준** — 잔디 서술 품질의 병목이 입력이라는 실측. 형식(템플릿)·길이 상한을 아무리 손봐도 커밋 메시지 25줄에서 나올 수 있는 서술에는 천장이 있다.
- **대안 대비** — API 상세 호출은 N+1 과 rate limit 을 매일 감수하면서도 default branch 한계가 남는다. 클론은 초기 비용 한 번에 그 둘을 동시에 없애고, `--numstat` 으로 **커밋 하나를 기술 영역 여러 개로 분해**하는 길까지 연다(DEC-015 D6 의 `## 담당 영역` 이 그 소비처다).
- **리스크**
  - 디스크 — 실측으로 해소(약 321MB). 잔여 위험은 레포 추가 시 재확인뿐.
  - 초기 클론 시간 — 최초 1회 수 분. 잡 밖에서 미리 돌린다.
  - identity drift — 새 기기에서 `git config` 를 안 하면 매칭이 조용히 샌다. D5 의 drift 감지가 유일한 방어다.
  - 토큰 — 회사 레포 클론에 `GH_TOKEN_COMPANY` 가 필요하다. 없으면 그 레포는 skip 되고 career 갱신이 조용히 멈춘다. 실패를 `last_error` 로 남기고 Slack 에 알린다.

## Scope

- **In** — 레지스트리 테이블 + 마이그레이션, `showcase.md` 1회 시드 이관, 클론 볼륨과 fetch 절차, `collect` 단계의 git 조사(`--all --numstat`, email 다중 author, tree-hash dedupe, diff 상한), `inputs.py` 의 GitHub API 커밋 경로 제거, **`docker-compose.yml:107` 의 `CONCURRENCY` 리터럴을 `${WORKER_CONCURRENCY:-1}` 로 분리**(OQ-5 해소 — 지금은 리터럴 `"2"` 라 재배포 시 실운영 값 1이 덮인다).
- **Out** — 착지 경로·문서 양식(DEC-015), 게이트 편입·발행(DEC-016), 레지스트리 관리 UI(admin 화면은 후속), `algorithms`·`content_enrich` 잡(별도 auto-commit 경로로 남는다).
- **영향을 받는 spec 후보** — 신규 spec(잔디 커밋 조사), `KDEV-SPEC-003`(잔디 잡 정의가 있는 spec 계열 확인 필요).

## Open Questions

**없다.** spec 착수를 막던 실측 2건이 2026-07-31 `mediness` 실측으로 닫혔다.

### 해소됨

| ID | Question | 결론 |
|---|---|---|
| ~~OQ-1~~ | 13개 레포 bare clone 총 디스크 | **~321 MB — 제약 아님, bare full 확정** (D3). `mediness` bare 129M 실측 → API 대비 ×1.16 환산 |
| ~~OQ-2~~ | 커밋 author identity 실제 값 | **identity 3종 확인 → `--author=kknaks` 단일 패턴 + drift 감지** (D5). email 고정목록은 기각 — `<user>@<hostname>.local` 이 계속 생긴다 |
| ~~OQ-3~~ | `path_rules` 를 레포마다 적을지 | **전역 기본값 + 레포별 예외** (D2). 13개에 전부 적으면 레포 구조 변경마다 손봐야 한다 |
| ~~OQ-4~~ | 레지스트리 초기 시드 | **`showcase.md` 에서 1회 이관** (D2). 손으로 넣으면 slug 오타가 로그도 없이 "추적 안 됨" 이 된다 |
| ~~OQ-5~~ | `CONCURRENCY` 리터럴 드리프트 | **`${WORKER_CONCURRENCY:-1}` 로 분리** (Scope In). 이번 범위 부수 작업 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 잔디 커밋 조사 (신규) | create | 레지스트리 스키마 · 클론/fetch · `collect` 계약(입력·상한·dedupe) |
| `KDEV-SPEC-003` | update | 잔디 잡 입력 정의 변경분 반영 |
