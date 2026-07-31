---
type: baseline
id: KDEV-BL-004
title: "커밋 잔디 파이프라인 — 로컬 클론 상세조사 + 승인 게이트 + career 누적"
status: accepted
product: kknaks-dev
source:
  type: idea
  ref: "kknaks 요청 2026-07-30 — 잔디 잡에 승인 게이트 붙이기 + 커밋 상세조사 + 착지 경로 재설계"
links:
  baselines: []
  decisions:
    - "[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]]"
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-016-grass-gate-and-publish|KDEV-DEC-016]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
created_at: 2026-07-30
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/accepted
---

# 커밋 잔디 파이프라인 — 로컬 클론 상세조사 + 승인 게이트 + career 누적

잔디 잡(`main_job.py`)은 BL-003 이 정리한 auto-commit 경로 4개 중 **유일하게 승인 게이트가 안 붙은 경로**다. 여기에 게이트를 붙이면서, 커밋 정보를 GitHub API 가 아니라 **서버에 클론한 레포에서 상세히 조사**하고, 그 결과를 daily 한 파일이 아니라 **career·concept 까지 세 목적지**로 보낸다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

> kknaks 요청 (2026-07-30). 대화 진행 중 네 번 정정됐고, 정정된 결론을 적는다.

**하고 싶은 것 — 4개 작업**

1. **추적 레포 목록을 DB로.** 스케줄러가 더 이상 md(`products/*/showcase.md`)에서 레포 목록을 읽지 않는다. 새 테이블이 필요하다.
2. **서버에 코드를 클론해 두고 커밋 기록을 상세히 조사한다.** 한 번에 모든 레포를 조사하지 않고:
   ```text
   조사 시작 → 조사할 목록 리스트 출력 → 응답 종료
     → 각 응답을 토대로 → (병렬, 지금은 워커 1이라 순차) 상세조사
     → 결과 취합 → 승인 게이트 이동
   ```
3. **유튜브 승인 게이트처럼 승인 게이트를 태운다.** 기존 게이트 구조를 재사용할 수 있는지가 관심사.
4. **착지 경로를 확정한다.** 지금 구조를 버리고 새로 정한다. 그래프는 지금 엉망이라 **이걸 다 구축한 뒤에** 손본다 — 이번 범위에서 그래프 정합은 고려하지 않는다.

**대화 중 정정된 것 (중요 — 초안이 틀렸던 부분)**

- **레포별 조사 깊이 차등은 필요 없다.** author 필터로 내 커밋만 가져오니 "남의 코드를 긁는다"는 문제가 애초에 없다. 조사는 균일하게 깊게 하고, **공개 수준은 승인 게이트에서 판단한다.**
- **`persona/areas/` 신설은 폐기.** area 개념을 새 층으로 만드는 게 아니라 **기존 `persona/career/*.md` 를 갱신**한다.
- **`career/studio.md` 신설도 폐기.** 다닌 적 없는 회사를 만들면 안 된다. 대신 DB 행이 `type: company|studio` 와 `detail: medisolve|null` 을 들고, **`company` 인 것만 career 로 간다.**
- **concept 은 일간이다.** 주간 롤업으로 밀 이유가 없다 — 구현하다 배운 개념은 그날 나오고 미루면 잃는다.
- **career 도 일간이다.** 별도 주간 파이프라인을 만들지 않는다. 크게 바뀔 게 없으니 "매일 갱신하되 대개 변경 없음"이 정상이다.
- **`inbox/` idea 는 제외.** 잔디에서 idea 로 갈 일이 없다.
- **`bullets` 는 제외.** 이력서 PDF 문장이라 AI 가 건드리지 않는다.
- **`products/*/30-work/*.md` 갱신은 안 한다.**
- **수동 트리거 파이프라인(casestudy → showcase·posts)은 이번 범위 밖.**

**부수 요구**

- career 양식을 커밋 구조에 맞게 자세하게 바꿔야 한다.
- 문서 파이프라인 진입점(`agent.md`)도 그에 맞춰 고쳐야 한다.

## Context

작업 착수 시점(2026-07-30) 코드 실측.

### 잔디 잡은 사람 개입 지점이 0이다

BL-003 Context 의 auto-commit 경로 표 첫 줄이 이 잡이고, 그 뒤 WORK-012~016 으로 Slack 지식캡처는 승인 게이트로 옮겨졌다. **잔디·algorithm·content_enrich 셋은 그대로 남았고, 이번 대상은 잔디다.**

```text
scheduler.py:22   cron 09:05 KST
→ main_job.py     inputs(git log + GitHub API) → counts 코드 계산
                  → llm.summarize_daily (Haiku, body+summary)
                  → upsert.write_daily (persona/daily/{date}.md)
                  → git_push.commit_and_push_with_retry (origin/main)
                  → reload_data() → notify_slack
```

- 유일한 방어는 `main_job.py:45` 의 `auto:false`(본인 작성) skip 과 `upsert.py:34` 의 이중 확인뿐이다.
- LLM 호출이 `client.result()` 로 **요청 안에서 블로킹**한다(`llm.py:181`). WORK-016 이 게이트 경로 전체에 세운 "실행은 비동기다" 규율 밖에 있다.
- `commit_and_push_with_retry` 는 **롤백이 없다.** push 실패 시 로컬 커밋이 남고, 다음 `POST /admin/reload` 의 `git reset --hard origin/main` 이 그것을 조용히 삭제한다(`apply/git.py:3-9` 가 이 함수를 쓰지 않는 이유로 명시).

### 커밋 입력이 얇다 — 서술이 뭉뚱그려지는 원인

`inputs.py:208-212` 의 `fetch_repo_commits()` 가 돌려주는 것은 `{"repo", "msg"}` **둘뿐**이다. diff·파일 통계·sha·브랜치·PR 이 없다.

- `2026-07-28.md` 는 `commit: 25` 인데 근거가 커밋 메시지 25줄이고, 본문 commits 섹션이 2줄로 압축돼 있다.
- 반면 notes·contents 는 파일 본문을 각 4096·2048자씩 넣는다(`main_job.py:76-77`). 그쪽만 재료가 있다.
- 커밋별 `files[]`·`stats` 를 API 로 받으려면 `/repos/{o}/{r}/commits/{sha}` 를 **커밋당 1회** 호출해야 한다(N+1).
- `/repos/{o}/{r}/commits` 는 **default branch 만** 본다. feature 브랜치 작업이 안 잡힌다.

### 길이 상한이 형식보다 먼저 걸린다

`llm.py:21 BODY_HARD_LIMIT = 600`, 프롬프트는 `≤500자 markdown narrative` 를 지시한다(`llm.py:100`). 섹션 구조를 늘려도 500자면 못 채운다.

### daily body 는 아무도 읽지 않는다 — career body 는 읽힌다

이 비대칭이 목적지 설계를 갈랐다.

| | 노출 경로 | body |
|---|---|---|
| `persona/daily/*.md` | `_derive_activity()`(`persona_loader.py:423-430`) → `/api/activity` → `contrib-grass.tsx` | **노출 안 됨.** `counts`(잔디 색 강도)·`summary[]`(셀 클릭 카드)만 추출 |
| `persona/career/*.md` | `/api/career`(`career.py:37`) → `career-timeline.tsx:127-246` | **`ReactMarkdown` 으로 렌더됨** |
| `career.bullets` | `print.py:56` → `resume.tsx:518` | PDF 이력서 전용. 사이트 미노출 |

- daily 89건(`2026-05-01` ~ `2026-07-28`, 88건이 `auto:true`)이 쌓여 있으나 `_derive_activity` 가 **rolling 365일**로 자른다(`persona_loader.py:414`). 그 밖은 파일로만 남고 사이트에서 사라진다. **누적이 어디로도 흐르지 않는다.**
- career 본문은 `## 무슨 일 하는지` · `## 챌린지` · `## 배운 점` 3섹션이 **전부 `(TBD — 사용자 채움)`** 이다. 사이트에 렌더되는 자리가 비어 있다.

### career 형식 SoT 가 없다

`persona_loader.py:68 REQUIRED_FIELDS["career"]` 가 필수 frontmatter(`type`·`period`·`display_order`·`title`·`org`·`summary`·`stack`)만 알고, **본문 섹션 구조를 정의한 문서가 없다.** `medisolve-ai.md` 의 `(TBD)` 스캐폴드가 사실상 유일한 힌트다.

daily 도 형식 SoT 가 흩어져 있다 — 섹션 구조는 `llm.py:100-119` 프롬프트, frontmatter 는 `upsert.py:46-51`, 소비 필드는 `_derive_activity`. `derived.py:5-8` 이 교안에서 "프롬프트에 명세를 적는 것은 이중 SoT" 라고 없앤 문제가 잔디에는 남아 있다.

### 레포 목록 출처와 career 매핑 구멍

```text
products/<product>/showcase.md  links.repo
→ persona_loader._load_products_showcase()  (부팅/reload 시 glob)
→ get_data()["projects"]                     (프로세스 메모리)
→ main_job.py:80-82 → inputs.extract_tracked_repos()
```

- 현재 13개. `links.repo` 는 프론트 `project-detail.tsx:121-123` 이 GitHub 링크로 렌더하므로 **showcase 에서 없앨 수 없다.**
- `showcase.md` 의 `org` 분포는 **`company` 5 / `studio` 8**.
- `persona/career/` 는 5개 — `medisolve-ai`(`is_current: true`) · `quantus` · `likelion` · `dowha-eng` · `bitcamp`. **`studio` 에 대응하는 career 문서가 없다.**

### author 필터 기준이 바뀐다

지금은 GitHub API 에 `params["author"] = acc["user"]`(**GitHub username**)를 넘긴다(`main_job.py:96`). 로컬 `git log` 는 username 을 모르고 **author name/email** 로만 매칭한다.

- `gh_accounts()` 의 `email` 이 그때 처음 커밋 필터로 쓰인다. 지금은 `bot_identity()`·`bot_emails()`(webhook self-push 필터)에서만 쓰인다 — `config.py:65` 주석이 "email 은 commit author 필터"라고 적어 놓고 실제로는 아니다.
- 커밋 author email 이 여러 개일 수 있다(개인·회사·GitHub `noreply`). 하나만 걸면 조용히 누락된다.

### 승인 게이트 재사용 범위 (실측)

`models.py:11-13` 이 `source_kind`·`stage_name`·`kind` 에 CHECK 를 일부러 안 걸었다("파이프라인 정의에서 오는 값은 제약하지 않는다"). **새 파이프라인 추가에 마이그레이션이 없다.**

| 모듈 | 손댈 것 |
|---|---|
| `core/models.py` 테이블 8개 | 없음 |
| `pipeline/definitions.py` | `Pipeline` 등록 |
| `pipeline/gates.py` (open/harvest/feedback/regenerate/retry/approve) | 없음 — `gates.py:3-5` 가 재사용을 명시 |
| `pipeline/executor.py` `AgentStage` | `prompt`/`payload`/`parse` 서브클래스 |
| `pipeline/driver.py` | 없음 — 상태로만 판단, `source_kind` 무관 |
| `api/routers/queue.py` + admin FE | 없음 — `GET /meta`(`queue.py:83-96`)가 정의를 내려줘 화면이 따라옴 |
| `pipeline/runtime.py` | 스테이지 등록 |

안 맞는 곳은 **전부 발행부와 체인 진행부**다.

- **`chain.py` 가 route 를 전제한다.** `enabled_stages(None)` 이 `()` 를 돌려주므로(`chain.py:40-41`) route 게이트가 없는 파이프라인은 `next_stage` 가 항상 `None` → 첫 승인에서 `chain_complete` → 즉시 발행. **게이트가 1개면 우연히 맞고, 2개 이상이면 두 번째가 조용히 건너뛰어진다.**
- **`apply/plan.py build_actions()`** 가 스테이지 이름을 하드코딩한다(`plan.py:102` `for stage in ("source_note", "derived")`, `:118` concept). 파일을 만드는 스테이지가 늘면 이 함수를 고쳐야 한다.
- **`ALLOWED_PREFIXES`**(`plan.py:25`)에 `persona/daily/`·`persona/career/` 가 없다 → `PATH_NOT_ALLOWED`. `LAYER_PREFIX`(`plan.py:32-39`)에 `daily`·`career` 가 없다 → `UNKNOWN_TYPE`.
- **create/replace 만 있다.** daily·career 는 **둘 다 정상**이다(첫 회 생성, 이후 덮어쓰기). `create` 는 파일이 있으면 `ALREADY_EXISTS`(`plan.py:224-228`), `replace` 는 없으면 `TARGET_MISSING`(`plan.py:235`).
- **`graph_check.virtual_nodes()`(`graph_check.py:44-54`)가 모든 액션을 그래프 노드로 얹는다.** "그래프 노드가 아닌 산출물" 개념이 없다.
- **`auto:false` 보호가 발행부에 없다.** `apply/executor._write_all()` 은 그냥 덮어쓴다.
- **중복 판정 축이 다르다.** `QueueItem` 의 unique index 는 `normalized_url` 기준이다(`models.py:116-124`). 잔디는 URL 이 없고 **날짜**가 축이다.
- **스케줄러용 접수 진입점이 없다.** `intake()` 는 source_url/note 를 받는 사람·Slack 전제다(`intake.py:5` 는 "잡이 같은 큐로 들어온다"고 써 두었으나 경로가 없다).

### 실행 환경 제약

- **클론 위치.** `docker-compose.yml` 이 `.:/repo` 를 rw 로 마운트한다. 레포 루트 아래 클론은 `reload.py` 의 `git reset --hard origin/main` 과 `apply/git.py rollback()` 의 `git clean -fd` 사정권이다. **별도 볼륨이 필수다.**
- **워커는 `/repo:ro`.** "capture worker 가 repo-local skill 을 읽되 파일은 쓰지 못하게 한다"가 명시된 설계다.
- **예산이 실질 상한.** `worker/run.py:36-39` `CostMiddleware(worker_budget_usd=5.0, global_budget_usd=20.0)`. 매일 도는 잡에서 13 레포 × diff 는 여기 부딪힌다.
- **동시성.** back 은 `--workers 1` 하드락(`runtime.py:7` 모듈 전역 레지스트리 성립 조건). open-kknaks 워커는 부하 때문에 1로 운용 중이나 **커밋된 `docker-compose.yml:107` 에는 `CONCURRENCY: "2"` 가 env 치환 없이 리터럴로 박혀 있다** — 재배포 시 2로 돌아간다.

## Why It Matters

- **BL-003 이 세운 전제가 잔디에서만 안 지켜진다.** "AI 첫 판단이 곧 SoT 가 되고 있다"가 그대로 남아 있고, 매일 09:05 에 자동으로 반복된다. 지식캡처는 게이트로 옮겨졌는데 잔디는 아니다.
- **커밋 서술 품질이 LLM 이 아니라 입력 탓이다.** 커밋 메시지만 보고 "무엇을 왜 고쳤는지" 를 쓰라는 것이라, 템플릿을 정교하게 만들어도 채울 재료가 없다. 상세 조사가 선행 조건이다.
- **daily 89건이 누적되지 않는다.** 365일 창을 벗어나면 사이트에서 사라지고, 그 사이 축적된 것이 어디로도 흐르지 않는다. 1년 뒤에도 "지금 뭘 하고 있나"를 말해 주는 문서가 없다.
- **사이트에 렌더되는 career 본문이 비어 있다.** `(TBD — 사용자 채움)` 이 그대로 노출된다. 채울 재료는 매일 커밋으로 생산되고 있는데 연결이 없다.
- **개념이 유튜브에서만 나온다.** 구현하다 배운 것이 `permanent/concept/` 로 가는 경로가 없다. 코드 주석에는 쌓이는데(제출/수확 분리, 낙관적 잠금, 원자적 발행) 지식 그래프에는 안 들어간다.
- **롤백 없는 push 가 승인한 것을 지울 수 있다.** 잔디가 `commit_and_push_with_retry` 를 쓰는 한, push 실패로 남은 로컬 커밋이 다음 reload 에 삭제된다. 게이트를 붙이면서 `publish_atomic` 으로 옮겨야 한다.

## Possible Direction

아직 결정은 아니다. decision 에서 확정한다.

### 작업 순서 (요청의 1~4번)

```text
1번  추적 레포 레지스트리 DB화        스케줄러 입력 전환
2번  로컬 클론 + 상세 커밋 조사        입력 보강 (fan-out)
4번  경로·양식 확정                  templates + agent.md   ← 3번보다 선행
3번  승인 게이트 연결 + apply/ 확장    발행 경로
```

4번이 3번보다 먼저다 — 목적지 형식이 없으면 게이트가 승인할 대상을 만들 수 없다.

### 레지스트리 행 모양 (1번)

```text
slug         제품/레포 식별자
type         company | studio
detail       career 파일 stem (medisolve-ai) | null
account      personal | company        클론·fetch 토큰 선택
enabled      bool                      삭제 대신 끄기
path_rules[] app/back/** → backend     조사 분해용
```

- `type=company` + `detail` → 그 career 문서를 갱신 대상으로 삼는다. `type=studio` → career 갱신 없음.
- `showcase.md` 의 `links.repo`(프론트 표시용)는 유지하고, **추적 SoT 만 DB 로 옮긴다.** 두 값이 갈라질 수 있음을 감수한다(보여주지만 안 긁는 레포, 반대의 경우).
- `detail` 값은 career 파일 stem 그대로 써야 한다. `medisolve` 로 두면 `medisolve-ai.md` 와 매핑 테이블이 하나 더 생긴다.
- 클론 운영 상태(`last_fetched_at`, 클론 실패)를 이 행에 둘지 분리할지는 미결.

### 로컬 클론 + fan-out (2번)

```text
/cache/repos/{owner}/{name}.git     bare, 레포 루트 밖 (필수)
git fetch --all --prune             잡 진입 시
git log --all --numstat --author=<emails> --since/--until
```

- API N+1 이 사라지고 `--all` 로 feature 브랜치까지 잡힌다. `--numstat` 이 커밋별 파일·라인을 주므로 **커밋 하나를 기술 영역 여러 개로 분해**할 수 있다.
- **diff 는 back 이 텍스트로 뽑아 프롬프트에 주입한다.** 워커에 클론 볼륨을 마운트하는 대안은 워커가 회사 코드 전체에 상시 접근하게 되고 토큰 통제가 어렵다.
- fan-out 은 **게이트 밖(`kind="auto"`)에 둔다.** `gates.py:300-319 _submit()` 이 게이트당 revision 1개 + AITask 1개를 만들고 `harvest()` 가 `drafting` 하나를 `FOR UPDATE` 로 잡아 멱등성을 얻는다 — 여기에 N 개를 매달면 그 전제가 깨진다. `gates.py` 코어는 건드리지 않는다.
- `--all` 을 쓰면 squash merge 레포에서 같은 작업이 브랜치 커밋 + merge 커밋으로 두 번 세어질 수 있다.

### 착지 경로 (4번) — 목적지 3개

| 경로 | `type` | 액션 | 조건 | 갱신 범위 |
|---|---|---|---|---|
| `persona/daily/{YYYY-MM-DD}.md` | `daily` | upsert | 활동 > 0 · 기존 `auto:false` 아님 | 파일 전체 |
| `persona/career/{stem}.md` | `career` | replace | `type=company` 커밋 있음 · `is_current: true` · `changed: true` | 본문 섹션 + `stack` |
| `permanent/concept/{slug}.md` | `concept` | upsert | 개념 후보 + 승인 | 신규 or 보충 |

제외 확정: `bullets`(이력서 PDF) · `products/*/30-work/*.md` · `products/*/showcase.md` · `persona/posts/*.md` · `inbox/*.md` · career 의 `period`·`is_current`·`display_order`·`title`·`org`·`summary`·`location`.

`products/` 를 안 열어도 되므로 `plan.py` 의 allowlist 를 패턴 매칭으로 바꿀 필요가 없다 — prefix 2개 추가로 끝난다.

### 파이프라인 정의 (3번)

```python
DAILY_COMMIT = Pipeline("daily_commit", (
    Stage("collect",     "auto"),   # git log·numstat·career 귀속·counts (LLM 없음)
    Stage("investigate", "auto"),   # ×N fan-out — 레포별 diff 조사
    Stage("compose",     "auto"),   # 취합 — daily·career·concept 초안
    Stage("daily",       "gate"),   # 하루 1개. 승인 = 발행
))
```

youtube + 이것 = 2개. `definitions.py:10-11` 이 정의를 DB 로 옮길 시점을 "소스 종류 3개 초과"로 못 박아 뒀으므로 아직 코드 상수를 유지한다.

- **게이트가 1개라 `chain.py` 의 route 전제 버그가 안 터진다.** 다만 잠복하므로 `enabled_stages(None)` → "정의된 게이트 전부" 로 일반화할지 이번에 정해야 한다. 파이프라인이 2개일 때 일반화하는 비용이 4개일 때보다 싸다.
- **route 게이트는 없다.** 목적지가 고정이라 고를 것이 없다. `discard` 대응은 `QueueItem.status="discarded"` 로 이미 있다.
- **활동 0 / `auto:false` 는 `collect` 에서 끝낸다.** 게이트까지 올라온 항목은 "발행할 내용이 있는 날"만이어야 한다.
- **"변경 없음"을 정당한 출력으로 둔다.** ① 그 career 에 그날 커밋이 0이면 스테이지를 아예 만들지 않는다(결정적, LLM 미호출). ② 커밋은 있으나 더할 게 없으면 `changed: false`. 안전망은 `apply/git.py:81-86` 의 `git diff --cached --quiet` 다.

### 양식 산출물 (4번)

```text
templates/persona/daily.md      신규 — 지금 llm.py + upsert.py 이중 SoT
templates/persona/career.md     신규 — 지금 SoT 없음
agent.md                        "별도 계열" 에 daily·career 등록
```

concept 는 `templates/knowledge/concept.md` + `rules/knowledge-note-pipeline.md` 를 **재사용한다.** 커밋 파이프라인이 그것을 읽게만 하면 된다 — `route.py:118-121` 이 이미 그 방식이다(프롬프트에 규칙을 복사하지 않고 레포에서 읽힌다).

career 템플릿 섹션 후보 — **이력서 문서이므로 커밋 구조를 그대로 노출하지 않는다.** 커밋 수 같은 숫자는 쓰지 않고 도출된 서술만 쓴다.

```text
## 무슨 일 하는지   담당 제품·서비스 1단락 + products 링크
## 담당 영역        path_rules 로 분해한 기술 영역 서술 (숫자 X)
## 챌린지          마주친 문제. 5~7줄 상한
## 배운 점          5~7줄 상한
## 대표 작업        work 문서 링크 (갱신은 안 하고 링크만)
```

핵심 규칙 둘을 템플릿에 박는다.

1. **append 금지 — 압축·재서술.** 새 줄을 더하지 않고 기존 줄을 더 정확하게 만든다. append 하면 `daily/*.md` 의 복사본이 되어 `knowledge-note-pipeline.md:167-169`("같은 사실은 한 곳에만")를 위반하고, 1년이면 챌린지가 200줄이 된다.
2. **상한 5~7줄.** 넘으면 합치거나 뺀다.

`bullets` 는 `content.md:68-76` 이 `id`·`day` 를 격리한 방식으로 "AI 가 정하지 않는다"에 명시한다.

### 게이트 화면에서 필요한 것

- `summary[]` 줄 단위 편집·삭제 (`payload_override`, `gates.py:549-550`)
- career 본문 문장 단위 승인 — concept 게이트의 `excluded` 토글(`plan.py:118-121`)과 같은 패턴
- 회사 레포 내용 절삭. 조사는 균일하게 깊게 하되 **공개 수준은 여기서 정한다**
- 승인 대기가 쌓이면 잔디에 구멍이 난다(지금은 그날 바로 push). `notify_slack` 을 발행 완료 알림에서 **승인 대기 알림**으로 바꿔야 한다

### 미결 (decision 대상)

1. **회사 코드 diff 를 외부 LLM 프롬프트로 보내는 것** — 공개 여부와 별개 문제(DB 저장 ≠ API 전송)다. 레포별이 아니라 계정별(personal/company)로 갈린다.
2. **`chain.py` route 전제 일반화를 이번에 할지** — daily 는 게이트 1개라 안 터지지만 다음 파이프라인이 밟는다.
3. **`## 담당 영역` 섹션 채택 여부** — 넣으면 `path_rules` 가 쓰이는 유일한 곳이고, 안 넣으면 그 컬럼이 필요 없어진다.
4. **레포당 diff 입력 상한** — `worker_budget_usd=5.0` / `global_budget_usd=20.0` 이 실질 제약.
5. **클론 방식** — bare + fetch vs shallow. 회사 레포 크기가 디스크를 정한다.
6. **날짜 축 중복 판정** — `normalized_url` 에 합성 키를 넣을지, 날짜 컬럼·부분 인덱스를 추가할지.
7. **`action="upsert"` 도입 여부** — daily·career 가 create/replace 양쪽에 걸린다.
8. **`--all` 과 squash merge 중복** — `counts["commit"]` 이 부풀 수 있다.
9. **클론 운영 상태 저장 위치** — 레지스트리 행 vs 별도 테이블.
10. **daily body 를 계속 쓸지** — 사이트에 노출되지 않는다. career·concept 스테이지 입력과 git 기록으로만 값이 있다.
