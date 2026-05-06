---
id: spec-03
type: spec
title: 스케쥴러 잡 명세 — daily-activity (잔디) + neetcode-canonical (algorithm)
status: draft
created: 2026-05-01
updated: 2026-05-05
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[planning-03-algorithm-daily-tab]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-07-algorithms-trace]]"
  - "[[adr-03-scheduler-attribution]]"
  - "[[adr-06-daily-as-grass-sot]]"
tags: [spec, scheduler, llm, activity, github, daily, algorithms]
---

# 스케쥴러 잡 명세

## Summary

APScheduler 가 매일 2 잡 발동:

1. **`daily-activity` (잔디 잡)** — **09:05 KST** 발동. 어제 데이터 (`notes/`/`contents/` 변경 + GitHub commits) → counts (deterministic) + LLM body·summary (Haiku 4.5 via open-kknaks) → `persona/daily/{어제}.md` 갱신. `activity.yaml` 폐지 (ADR-06).
2. **`neetcode-canonical` (algorithm 잡)** — **23:00 UTC** 발동. NeetCode 150 시퀀스의 다음 slug → 5 단계 source-first 파이프라인 (LeetCode GraphQL + neetcode-gh + LLM gap-filler) → `persona/algorithms/A-NNN-slug.md` 박음 + `today` 필드 mutation. 상세 spec-07.

두 잡은 **인프라 공유** (redis broker · open-kknaks worker · git push retry · `load_all` 메모리 reload), **큐만 분리** (`daily` vs `algorithm`).

§1~10 = `daily-activity` 잡 명세. §11 = `neetcode-canonical` 잡 명세 (spec-07 의 인터페이스 이행). §12 = 향후 확장.

---

## 1. 트리거 + 실행 환경

### 1.1 스케쥴

- **시각**: 매일 **09:05 KST** (`Asia/Seoul`) = 00:05 UTC
- **target_date**: `date.today() - 1` (직전 날). 어제 entry 박음
- **TZ 안전 시각 선택**: 컨테이너 TZ = UTC 인 상태에서 `date.today()` 가 "어제 KST" 와 일치하려면 UTC 자정 이후 발동 필요. 09:05 KST = 00:05 UTC 가 자정 직후 가장 빠른 시각. 00:05 KST 발동 시 컨테이너 시각은 전날 15:05 UTC → `date.today()` 가 그저께를 반환하는 off-by-one 발생 (b6979da 사고)
- **이유**:
  - 캘린더 day-fixed 윈도우 `[어제 00:00 KST, 오늘 00:00 KST)` — 하루 전체 commit 확보 + 23:55 발동 시 발생하던 23:55~24:00 5분 commit 유실 제거
  - miss-fire (서버 down 후 coalesce 발동) 시에도 attribution 명확 — `target_date=어제` 라 발동 시각 흔들려도 entry 키 안 흔들림
- **구현**: APScheduler `AsyncIOScheduler` + cron trigger

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
    daily_activity_job,
    "cron",
    hour=9, minute=5,
    timezone="Asia/Seoul",
    id="daily-activity",
    coalesce=True,           # 백엔드 재시작 중 미스된 실행은 모아서 1번만
    max_instances=1,         # 동시 실행 차단
)
```

> **잡 함수 시그니처**: `run_daily_activity_job(*, target_date: date | None = None, ...)`. 미지정 시 어제. 백필(§7) / 수동 테스트는 `target_date=date(YYYY,MM,DD)` 로 override.

### 1.2 single-worker 강제 (ADR-03 §4.4 mitigation)

`uvicorn --workers N` (N>1) 으로 실행 시 스케쥴러 N번 발동.

대응:
- 홈서버 운영은 single-worker (`uvicorn main:app` 또는 `--workers 1`)
- 부팅 시 워커 수 검증 (back/main.py `_check_single_worker`)

### 1.3 본인 작성 vs 자동 생성 충돌 회피

target 날의 `persona/daily/{date}.md` 가 이미 존재하고 frontmatter `auto: true` 가 *아닌* 경우 (= 본인이 박은 narrative) → **잡 skip**. 본인 narrative 우선.

```python
existing = read_daily(target)
if existing and not existing.get("auto"):
    logger.info("daily/%s.md exists with auto=false — skip", target)
    return existing  # 잔디 viz 는 본인 narrative 의 frontmatter 그대로
```

---

## 2. 입력 수집

target = `date.today() - 1` (KST 기준, §1.1). 수집은 병렬 가능.

### 2.1 입력 1: `notes/` 그날 변경 파일 본문

`notes/` 디렉토리의 그날 git commit 에서 변경된 파일들의 *본문* 을 읽음 (subject 만이 아니라 frontmatter 제외 본문 전체).

```python
def read_changed_files_today(path: str, target: date, repo: Path) -> list[dict]:
    """그날 변경된 .md 파일들의 frontmatter + 본문 반환.

    [{path, frontmatter, body}, ...]
    """
    since_iso = f"{target.isoformat()}T00:00:00+09:00"
    until_iso = f"{(target + timedelta(days=1)).isoformat()}T00:00:00+09:00"
    result = subprocess.run(
        ["git", "log", "--since", since_iso, "--until", until_iso,
         "--name-only", "--pretty=format:", path],
        cwd=repo, capture_output=True, text=True, check=True,
    )
    paths = sorted({line for line in result.stdout.splitlines() if line.endswith(".md")})
    out = []
    for p in paths:
        full = repo / p
        if not full.exists():
            continue  # commit 후 삭제된 파일
        post = frontmatter.load(full)
        out.append({"path": p, "frontmatter": dict(post.metadata), "body": post.content})
    return out

notes_changes = read_changed_files_today("persona/notes/", target, REPO)
```

> **TZ**: 명시적 `+09:00` ISO timestamp 사용 (홈서버 TZ 가 UTC 든 KST 든 결과 동일).
> **truncation**: 파일 본문이 N KB 초과 시 truncate (LLM 토큰 부담 회피). N = 4096 자 권장 (note 1개 평균 짧음).

### 2.2 입력 2: `contents/` 그날 변경 파일 본문

§2.1 동일 패턴. path = `persona/contents/`.

content 본문은 LLM enrich 결과라 길 수 있음 — truncate 더 적극적 (예: 2048 자).

### 2.3 입력 3: GitHub commits API — tracked repos × accounts

#### 2.3.1 tracked repos 추출 — `persona/projects/*.md` SoT

```python
def extract_tracked_repos(projects: list[dict]) -> set[str]:
    """projects/*.md 의 links.repo 에서 'owner/name' slug 추출.

    visible 무관 모든 projects 검사 (visible: false 항목도 잔디 잡 추적 — spec-01 §3.3, spec-02 §3.5).
    """
    slugs: set[str] = set()
    for proj in projects or []:
        repo_url = (proj.get("links") or {}).get("repo", "") or ""
        if "github.com/" not in repo_url:
            continue
        # rstrip(".git") 함정 회피 — 끝글자 g/i/t 가 잘림 (e.g. wine_log → wine_lo)
        slug = repo_url.split("github.com/", 1)[1].rstrip("/")
        if slug.endswith(".git"):
            slug = slug[:-4]
        if slug.count("/") == 1:
            slugs.add(slug)
    return slugs
```

#### 2.3.2 fetch_repo_commits — repo × account

```python
async def fetch_repo_commits(
    owner_repo: str, target: date, token: str, author: str = "",
) -> list[dict]:
    """`/repos/{owner_repo}/commits` — 그날 (KST) author commits.

    - `since` / `until` 파라미터 KST 기준 ISO timestamp.
    - `author` (optional) — GitHub username 또는 email 매칭.
    - 403/404/409 (권한 없거나 빈 repo) 는 silently skip.
    - msg 전체 (subject + body) 반환 — 이전엔 첫 줄만, 새 spec 은 LLM 컨텍스트 풍부화 위해 전체.
    """
    if not token or not owner_repo:
        return []
    since = f"{target.isoformat()}T00:00:00+09:00"
    until = f"{(target + timedelta(days=1)).isoformat()}T00:00:00+09:00"
    params = {"since": since, "until": until, "per_page": "100"}
    if author:
        params["author"] = author
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(
            f"https://api.github.com/repos/{owner_repo}/commits",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            params=params,
        )
        if r.status_code in (403, 404, 409):
            return []
        r.raise_for_status()
        commits = r.json()
    return [{"repo": owner_repo, "msg": c.get("commit", {}).get("message", "")} for c in commits]
```

#### 2.3.3 main_job — tracked × accounts 호출 + dedupe

```python
tracked_repos = extract_tracked_repos(get_data().get("projects", []))
seen: set[tuple[str, str]] = set()
commits: list[dict] = []
for repo in tracked_repos:
    for acc in config.gh_accounts():       # 개인 + 회사 PAT
        for c in await fetch_repo_commits(repo, target, acc["token"], author=acc["user"]):
            key = (c["repo"], c["msg"])
            if key in seen:
                continue
            seen.add(key)
            commits.append(c)
```

GitHub commits API:
- **인증**: PAT (개인 + 회사 분리 — `GH_TOKEN_PERSONAL` / `GH_TOKEN_COMPANY`). 각 계정의 private repo 는 그 계정 PAT 으로만 보임. 회사 레포 + 개인 token = 404 silently skip.
- **author 필터**: GitHub `author` 파라미터 — username 또는 email 매칭. 본인 commit 만 발라냄.
- **TZ**: `since` / `until` ISO timestamp (`+09:00`).
- **rate limit**: 5000 req/hour (PAT). tracked repo 수 ≤ 100 가정 OK.

---

## 3. counts (deterministic) + LLM (body + summary)

### 3.1 counts — 코드 계산

```python
counts = {
    "commit": len(commits),               # GitHub commits dedupe 후
    "note":   len(notes_changes),         # notes/*.md 그날 변경
    "study":  len(contents_changes),      # contents/*.md 그날 변경
}
```

LLM 추론 불요. source 1:1 매핑.

### 3.2 LLM 호출 — body + summary 만

#### 모델 + 라이브러리

- 모델: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- 라이브러리: **`open-kknaks`** (ADR-04). Anthropic SDK 미사용

#### 프롬프트

```python
async def summarize_daily(
    target: date,
    notes_changes: list[dict],     # [{path, frontmatter, body}, ...]
    contents_changes: list[dict],
    commits: list[dict],           # [{repo, msg}, ...]
    counts: dict,
    client: ClaudeClient,
) -> dict:
    """LLM 1 call → {body, summary}. counts 는 코드 계산이라 LLM 안 받음."""
    notes_block = _format_notes(notes_changes) or "(없음)"
    contents_block = _format_contents(contents_changes) or "(없음)"
    commits_block = _format_commits(commits) or "(없음)"

    prompt = f"""오늘({target.isoformat()}) 한 사람의 활동 데이터다.

활동 분포 (자동 집계):
- commits: {counts['commit']}
- notes:   {counts['note']}
- study:   {counts['study']}

[notes 변경 — 본문]
{notes_block}

[contents 변경 — 본문]
{contents_block}

[GitHub commits — msg 전체]
{commits_block}

다음 두 가지를 출력해라:
1. summary: 활동 단위별 한 줄 요약 — **list[str]** (ko/en 각각).
   라벨 규칙 (한 활동 단위 = 한 줄):
     - GitHub commits: `[<repo>] 작업요약` — 같은 repo 의 여러 commit 은 1줄로 합침
     - notes 변경: `[notes] 항목 요약` — 전체 1줄로 합침
     - contents 변경: `[study] 항목 요약` — 전체 1줄로 합침
   각 줄 80자 이내, 자연스러운 어투. 활동 분포가 0 인 카테고리는 라인 생성 X.
2. body: ≤500자 markdown narrative. 다음 섹션 구조:
   ## commits
   - [repo] msg 한 줄 + 의미 (1줄)
   ## notes
   - [note-id] 한 줄 정리
   ## study
   - [content-id] 키 takeaway (1줄)

   # 회고 / 다음
   (1~2줄, 추론 어렵면 비움)

응답은 다음 JSON 한 객체만 (다른 텍스트 X, 코드블록 ```json``` 도 박지 않음):
{{"summary": {{"ko": ["[repo] ...", "[notes] ..."], "en": ["[repo] ...", "[notes] ..."]}}, "body": "..."}}
"""
    task_id = await client.submit(prompt=prompt, model=LLM_MODEL, timeout=120, max_retries=2)
    task = await client.result(task_id, timeout=120)
    resp = json.loads(_extract_json(task.result or ""))
    return validate_llm_response(resp, target)
```

### 3.3 응답 검증

```python
def validate_llm_response(resp: dict, target: date) -> dict:
    summary = resp.get("summary")
    body = resp.get("body", "")

    if not isinstance(summary, dict) or "ko" not in summary or "en" not in summary:
        raise ValueError("invalid_summary")
    # ko/en 각각 list[str] — 빈 list 도 허용 (활동은 있는데 LLM 이 categorize 못한 edge case)
    for k in ("ko", "en"):
        v = summary[k]
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
            raise ValueError(f"invalid_summary_{k}_not_list_str")
    if not isinstance(body, str):
        raise ValueError("invalid_body")
    if len(body) > 600:                     # 500자 룰 + 100자 grace
        body = body[:600] + "...(truncated)"
    return {"summary": summary, "body": body}
```

검증 실패 시 — LLM 재호출 1회 retry. 재차 실패 시 entry skip + 로그.

> **Backward compat (loader)**: 기존 daily entry 들의 `summary` 는 `{ko: str, en: str}` (legacy) 형태로 박혀있음. `persona_loader._validate` 는 list[str] / str 둘 다 통과. 새 entry 는 list[str] 만 박힘. 프론트 잔디 viz 도 두 형태 모두 렌더 (Array.isArray 분기).

### 3.4 활동 0 (counts 합계 = 0) 처리

LLM 호출 skip. body 비움, summary=null:

```python
if sum(counts.values()) == 0:
    return {"summary": None, "body": "(활동 없음)"}
```

---

## 4. daily/{date}.md 갱신 (idempotent)

같은 날 잡이 두 번 돌아도 결과 동일.

```python
import frontmatter

def write_daily(target: date, counts: dict, summary: dict | None, body: str) -> Path:
    path = config.PERSONA_DIR / "daily" / f"{target.isoformat()}.md"
    fm = {
        "type": "daily",
        "date": target.strftime("%Y.%m.%d"),
        "auto": True,
        "counts": counts,
    }
    if summary is not None:
        fm["summary"] = summary

    post = frontmatter.Post(content=body, **fm)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path
```

**`auto: false` 충돌 회피** (§1.3 의 사전 검사로 잡 자체가 skip 되지만, 방어적으로):

```python
if path.exists():
    existing = frontmatter.load(path)
    if not existing.metadata.get("auto"):
        logger.warning("daily/%s.md auto=false — skip overwrite", target)
        return path
```

---

## 5. git push retry loop (ADR-03 §4.3 구체화)

`commit_and_push_with_retry` (공통 함수, spec-03/spec-06 공유) 그대로 사용. paths 변경:

```python
commit_and_push_with_retry(
    paths=[config.PERSONA_DIR / "daily" / f"{target.isoformat()}.md"],
    message=f"chore: daily {target.isoformat()}",
    dry_run=config.job_git_push_dry_run(),
)
```

자세한 인증 / retry / fetch+rebase 디테일은 `back/service/jobs/git_push.py` + ADR-03.

---

## 6. 메모리 reload

push 성공 후 `load_all()` 셀프 호출. `persona_loader` 가 `daily/*.md` 들 다시 읽으면서 새 파일 frontmatter 가 in-memory `daily` 리스트 + derived `activity` dict 양쪽 갱신.

```python
async def daily_activity_job(*, target_date: date | None = None, dry_run_push: bool | None = None):
    target = target_date or (date.today() - timedelta(days=1))

    # §1.3 본인 작성 우선
    existing = read_existing_daily(target)
    if existing and not existing.get("auto"):
        logger.info("daily/%s.md exists with auto=false — skip job", target)
        return existing

    notes_changes = read_changed_files_today("persona/notes/", target, REPO)
    contents_changes = read_changed_files_today("persona/contents/", target, REPO)
    commits = await fetch_all_tracked_commits(target)
    counts = compute_counts(notes_changes, contents_changes, commits)

    resp = await summarize_daily(target, notes_changes, contents_changes, commits, counts, client)
    path = write_daily(target, counts, resp["summary"], resp["body"])

    commit_and_push_with_retry(
        paths=[path],
        message=f"chore: daily {target.isoformat()}",
        dry_run=config.job_git_push_dry_run() if dry_run_push is None else dry_run_push,
    )

    # 메모리 reload — circular import 회피
    from main import load_all
    load_all()
```

---

## 7. 백필 (첫 부팅 365일 1회 — 옵션)

`daily/*.md` 1개씩 박는 형태로 백필. GitHub Events API 90일 + GraphQL `contributionsCollection` (90~365일) fallback:

| 시점 | 입력 | counts | summary/body |
|---|---|---|---|
| 최근 90일 | GitHub commits API + git log | deterministic (위 §3.1 와 동일) | LLM 호출 |
| 90~365일 | GraphQL `contributionsCollection` | counts={commit: N, note: 0, study: 0} (commit count 만) | summary=null, body=`(백필 — commit count 만)` |

```python
async def backfill_365_days():
    today = date.today()
    for offset in range(365, 0, -1):
        target = today - timedelta(days=offset)
        existing = read_existing_daily(target)
        if existing:
            continue                  # 이미 박혀있으면 skip (멱등)
        await run_daily_activity_job(target_date=target, dry_run_push=True)
    # 마지막에 한 번 묶어서 push
    commit_and_push_with_retry(
        paths=[config.PERSONA_DIR / "daily"],
        message=f"chore: backfill daily 365 days",
        dry_run=False,
    )
```

수동 스크립트로 1회 실행. APScheduler 에 안 박음.

---

## 8. secret 관리 (변경 없음)

| 키 | 용도 | 보관 |
|---|---|---|
| `GH_TOKEN_PERSONAL` / `GH_TOKEN_COMPANY` | GitHub REST API 인증 — tracked repos commits 조회 + git push | `.env` |
| `GH_USER_*`, `GH_EMAIL_*` | author 필터 + git commit identity | 동상 |
| `REDIS_URL` | open-kknaks broker | docker-compose env |
| `RELOAD_TOKEN` | webhook → /admin/reload 인증 | 동상 |
| `CLAUDE_CODE_OAUTH_TOKEN` | open-kknaks worker — claude CLI 호출 | docker-compose `.env` |

`.env` 는 `.gitignore` 박음.

---

## 9. 검증 / fail-safe

| 실패 케이스 | 대응 |
|---|---|
| open-kknaks LLM 호출 실패 | 1회 retry. 재차 실패 시 daily/{date}.md 박지 않음 (다음 날 자동 다시 시도) |
| GitHub API 5xx/timeout | 1회 retry. 재차 실패 시 commits=[] 로 진행 (notes/contents 만으로 LLM 호출) |
| `notes/*.md` 또는 `contents/*.md` frontmatter 파싱 에러 | 해당 파일 skip + 로그 |
| `daily/{date}.md` write 실패 (디스크 가득) | 잡 abort + 로그 |
| git push 3회 retry 실패 | daily/{date}.md commit-pending 상태 유지. 다음 날 push 시 자동 포함 (rebase) |
| LLM 응답 JSON 파싱 실패 | 1회 retry. 재차 실패 시 entry skip |
| LLM 응답 body > 600자 | truncate (`...(truncated)`) — soft enforcement |

모든 실패 케이스에서 백엔드 프로세스는 **죽지 않음** (잡은 매일 새로 시도).

---

## 10. 멱등성 / 재실행 안전

- `write_daily` 가 같은 path 갈아끼움 → 같은 날 잡 두 번 돌려도 결과 동일 (LLM 응답 wording 만 비결정적)
- `commit_and_push_with_retry` 가 변경 없으면 skip → 재실행 시 빈 commit 생성 X
- 백필 스크립트도 재실행 안전 (날짜별 file 단위)
- §1.3 본인 작성 (`auto: false`) 보존 — 잡 재실행해도 안 갈아엎음

---

## 11. `neetcode-canonical` 잡 (algorithm 큐)

planning-03 + spec-07 의 알고리즘 카테고리 자동 생성 잡. **잔디 잡과 별도 큐**, 매일 1 commit (`persona/algorithms/A-NNN-slug.md`) 박음.

### 11.1 트리거

- **시각**: 매일 **23:00 UTC** (= KST 다음날 08:00)
- **큐**: `algorithm` (잔디 잡은 `daily` 큐)
- **target_date**: `date.today()` (UTC) — 잡이 박는 날 자체. 잔디 잡과 달리 *어제 박지 않음* (오늘 박음)

```python
scheduler.add_job(
    neetcode_canonical_job,
    "cron", hour=23, minute=0, timezone="UTC",
    id="neetcode-canonical",
    coalesce=True, max_instances=1,
)
```

§1.2 (single-worker 강제) 동일 적용.

### 11.2 5 단계 파이프라인 (spec-07 §7 이행)

| 단계 | 작업 | 외부 호출 |
|---|---|---|
| (a) source fetch | LeetCode GraphQL + neetcode-gh raw | https |
| (b) 캐시 | local file 또는 redis (idempotent) | — |
| (c) 정규화 | statement trim · cases 추출 · core region 판별 · solution code 정답 라인 추출 | — |
| (d) LLM gap-filler | open-kknaks 1 호출 (clarifying·approach·logic distractor·trace worked_example·solution followup) | redis broker (잔디 잡과 동일 인프라) |
| (e) md 박음 | frontmatter + `## Data` yaml 블록 + git commit/push | git |

### 11.3 잡 함수 시그니처

```python
async def neetcode_canonical_job(*, target_date: date | None = None, dry_run_push: bool | None = None):
    target = target_date or date.today()
    seq_index = read_sequence_state()                  # redis state — §11.4
    slug = NEETCODE_150[seq_index]                     # 시퀀스의 다음 slug

    # (a) fetch — LeetCode + neetcode-gh
    leetcode_data = await fetch_leetcode_graphql(slug)
    solution_code = await fetch_neetcode_gh(slug)

    # (b) 캐시 — 위 호출 내부에서 redis hit 시 재호출 skip

    # (c) 정규화
    normalized = normalize(leetcode_data, solution_code)
    # → problem.statement·constraints·io / solution.code·complexity / trace.cases / core_region 라인 set

    # (d) LLM gap-filler — open-kknaks 1 호출
    llm_resp = await fill_gaps(normalized, client)
    # → clarifying·approach·logic.{format,slots distractor·why·label·indent}·trace.worked_example·solution.followup

    # (e) md 박음
    md_path = write_algorithm_md(target, seq_index, slug, normalized, llm_resp)
    prev_today_paths = clear_today_flag()              # §11.5 frontmatter mutation
    advance_sequence_state(seq_index + 1)

    commit_and_push_with_retry(
        paths=[md_path] + prev_today_paths,
        message=f"chore: algorithm A-{seq_index+1:03d} {slug}",
        dry_run=config.job_git_push_dry_run() if dry_run_push is None else dry_run_push,
    )

    # 메모리 reload — 같은 패턴 (§6)
    from main import load_all
    load_all()
```

### 11.4 시퀀스 상태 — redis

NeetCode 150 시퀀스의 진행도는 **redis** 에 저장 (잡이 갱신, 파일 안 만짐):

```
key: kknaks-portfolio:neetcode:next_index → "8"
key: kknaks-portfolio:neetcode:last_run   → "2026-05-05T23:00:00Z"
```

매 잡 후 `next_index` += 1. NeetCode 150 끝 (index 150) 도달 시 잡 정지 또는 다른 큐레이션 리스트로 전환 (수동 결정).

> **`_meta.yaml` 안 씀 이유**: spec-01 §1 의 `_meta.yaml` 은 *사람이 박는 enum 정의* 용도. 잡이 자동 갱신하는 시퀀스 상태는 redis 가 정합. 부팅 시 `_state.yaml` 같은 파일도 옵션이지만 redis 가 잔디 잡과 인프라 공유라 간단.

### 11.5 `today` 필드 mutation

잡의 **유일한 frontmatter mutation** (spec-07 §8.1):

1. 새 항목 frontmatter `today: true` 박힘
2. 이전 `today: true` 항목 (전날 박힌 것) → `today: false` 로 갱신
3. 두 변경을 한 commit 에 묶음

```python
def clear_today_flag() -> list[Path]:
    """이전 today=true 항목들의 frontmatter today: false 갱신.

    return: 갱신된 path 리스트 (commit paths 에 합류).
    """
    algos_dir = config.PERSONA_DIR / "algorithms"
    changed: list[Path] = []
    for p in algos_dir.glob("A-*.md"):
        post = frontmatter.load(p)
        if post.metadata.get("today") is True:
            post.metadata["today"] = False
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            changed.append(p)
    return changed
```

### 11.6 활동 0 처리 — N/A

잔디 잡과 달리 본 잡은 *콘텐츠 생성* 잡 → "활동 0" 개념 X. fetch·LLM 호출이 모두 성공해야 entry 박힘. 실패 시 §11.7 처리.

### 11.7 실패 처리

| 실패 | 처리 |
|---|---|
| LeetCode GraphQL down | 잡 실패 → 다음 날 재시도. 시퀀스 `next_index` 갱신 X (같은 slug 재시도) |
| neetcode-gh 솔루션 누락 (slug 미존재) | LLM fallback — `solution.code` LLM 생성, frontmatter `solution_source: 'llm-fallback'` 마킹 |
| LLM 응답 파싱 실패 | 1 retry. 재차 실패 시 잡 abort, 다음 날 재시도 |
| 외부 lib 의존 솔루션 (numpy 등) | trace·logic 그대로 진행 (adr-09 단순화 후 sandbox 부담 없음) |
| git push 3회 retry 실패 | spec-03 §5 의 `commit_and_push_with_retry` 동일 — pending 유지, 다음 날 자동 포함 |

### 11.8 잡 인프라 공유

| 인프라 | 잔디 잡 | algorithm 잡 |
|---|---|---|
| APScheduler 인스턴스 | 같음 | 같음 |
| redis broker | 같음 (kknaks-portfolio namespace) | 같음 |
| open-kknaks worker | 같음 | 같음 (큐만 다름) |
| `commit_and_push_with_retry` | 같음 | 같음 |
| `load_all` 셀프 호출 | 같음 | 같음 |
| single-worker 강제 (§1.2) | 같음 | 같음 |
| 큐 | `daily` | `algorithm` |
| 발동 시각 | 09:05 KST | 23:00 UTC |
| target_date | 어제 (KST) | 오늘 (UTC) |

### 11.9 잔디와의 자연스러운 공존

본 잡의 commit (`chore: algorithm A-NNN ...`) 은 다음 날 잔디 잡이 **GitHub commits API** 로 수집할 때 자동으로 카운트됨 — `commits` count +1 자연스럽게 박힘. 별도 처리 없이 잔디 시각화에 반영.

### 11.10 멱등성

- `next_index` 가 redis 에 박혀있어 재실행 시 같은 slug 재처리 X (§11.7 의 push 실패 케이스 외)
- `clear_today_flag()` 는 today=true 가 1개만 남도록 강제 — 두 번 돌아도 결과 같음
- 같은 날 두 번 발동하면 두 번째는 next_index 가 이미 갱신됐으므로 다음 slug 박음 (의도된 동작)

### 11.11 백필

`neetcode-canonical` 잡 백필은 **별도 스크립트** (수동 1회). NeetCode 150 의 첫 N 개를 days N 일 동안 한꺼번에 박을지, 아니면 출시일부터 1일 1개씩만 누적할지는 planning-03 §8 결정 박힘 — **백필 X**, 출시일부터 1/일.

---

## 12. 향후 확장 여지 (이 spec 범위 밖)

- 프론트 `contrib-grass.tsx` viz upgrade — counts dict 활용해서 kind 별 stripe 또는 dominant color
- counts 키 추가 (예: `ship`, `review`, `design`) — `_meta.yaml` 색 매핑 + spec-01 §7 정합
- 다른 자동 산출물 (weekly digest, monthly summary) — 같은 패턴으로 별도 잡
- LLM 모델 업그레이드 (Sonnet) — 비용 검토 후
- multi-worker 운영 시 distributed lock — §1.2 옵션
- `daily/2026/` 식 연도 파티션 — 1년 후 `daily/` 비대해지면 검토
