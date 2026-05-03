---
id: spec-03
type: spec
title: 잔디 잡 명세 — 입력 → counts (deterministic) + LLM body·summary → daily/{date}.md
status: draft
created: 2026-05-01
updated: 2026-05-03
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[adr-03-scheduler-attribution]]"
  - "[[adr-06-daily-as-grass-sot]]"
tags: [spec, scheduler, llm, activity, github, daily]
---

# 잔디 잡 명세

## Summary

매일 00:05 KST 백엔드 안 APScheduler가 발동. 어제 데이터 (`notes/`/`contents/` 그날 변경 파일 본문 + GitHub commits) 를 수집 → counts (commit/note/study) 는 코드가 deterministic 으로 계산 → LLM (Haiku 4.5 via open-kknaks) 이 ko/en 한 줄 summary + ≤500자 narrative body 생성 → `persona/daily/{어제}.md` 에 frontmatter (auto/counts/summary) + body 한 commit 으로 push → `load_all()` 셀프 호출로 메모리 갱신. **`activity.yaml` 폐지** (ADR-06) — `/api/activity` 응답은 모든 `daily/*.md` frontmatter 집계 derive.

---

## 1. 트리거 + 실행 환경

### 1.1 스케쥴

- **시각**: 매일 **00:05 KST** (`Asia/Seoul`)
- **target_date**: `date.today() - 1` (직전 날). 자정 직후 발동해서 *어제* entry 박음
- **이유**:
  - 캘린더 day-fixed 윈도우 `[어제 00:00, 오늘 00:00)` — 하루 전체 commit 확보 + 23:55 발동 시 발생하던 23:55~24:00 5분 commit 유실 제거
  - miss-fire (서버 down 후 coalesce 발동) 시에도 attribution 명확 — `target_date=어제` 라 발동 시각 흔들려도 entry 키 안 흔들림
- **구현**: APScheduler `AsyncIOScheduler` + cron trigger

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
    daily_activity_job,
    "cron",
    hour=0, minute=5,
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
1. summary: 무슨 작업을 했는지 한국어/영어 한 줄 (각각 60자 이내, 자연스러운 어투)
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
{{"summary": {{"ko": "...", "en": "..."}}, "body": "..."}}
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
    if not isinstance(body, str):
        raise ValueError("invalid_body")
    if len(body) > 600:                     # 500자 룰 + 100자 grace
        body = body[:600] + "...(truncated)"
    return {"summary": summary, "body": body}
```

검증 실패 시 — LLM 재호출 1회 retry. 재차 실패 시 entry skip + 로그.

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

## 11. 향후 확장 여지 (이 spec 범위 밖)

- 프론트 `contrib-grass.tsx` viz upgrade — counts dict 활용해서 kind 별 stripe 또는 dominant color
- counts 키 추가 (예: `ship`, `review`, `design`) — `_meta.yaml` 색 매핑 + spec-01 §7 정합
- 다른 자동 산출물 (weekly digest, monthly summary) — 같은 패턴으로 별도 잡
- LLM 모델 업그레이드 (Sonnet) — 비용 검토 후
- multi-worker 운영 시 distributed lock — §1.2 옵션
- `daily/2026/` 식 연도 파티션 — 1년 후 `daily/` 비대해지면 검토
