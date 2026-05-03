---
id: spec-03
type: spec
title: 잔디 잡 명세 — 입력 4개 + LLM 종합 + activity.yaml upsert + git push
status: draft
created: 2026-05-01
updated: 2026-05-03
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[adr-03-scheduler-attribution]]"
tags: [spec, scheduler, llm, activity, github]
---

# 잔디 잡 명세

## Summary

매일 1회 백엔드 안 APScheduler가 실행. 입력 4개(`daily/YYYY-MM-DD.md` narrative + `notes`/`contents` 로컬 git log + GitHub Events API)를 수집해 Anthropic Haiku 4.5에 종합 → ko/en 한 줄 요약 + kind 결정 → `persona/activity.yaml` 한 entry upsert → fetch+rebase 후 git push (3회 retry) → `load_all()` 셀프 호출로 메모리 갱신. 첫 부팅 시 365일 백필 1회.

---

## 1. 트리거 + 실행 환경

### 1.1 스케쥴

- **시각**: 매일 **00:05 KST** (`Asia/Seoul`)
- **target_date**: `date.today() - 1` (직전 날). 즉 자정 직후 발동해서 *어제* entry 박음
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

**`uvicorn --workers N` (N>1) 으로 실행 시 스케쥴러 N번 발동**.

대응:
- 홈서버 운영은 single-worker (`uvicorn main:app` 또는 `--workers 1`)
- 부팅 시 워커 수 검증:

```python
import os
if int(os.environ.get("WEB_CONCURRENCY", 1)) > 1:
    raise RuntimeError(
        "Multi-worker deployment 금지 — APScheduler가 N번 발동. "
        "single-worker로 띄우거나 spec-03 §1.3 distributed lock 적용."
    )
```

### 1.3 (선택) distributed lock — 만약 multi-worker 운영 필요해지면

APScheduler의 `JobStore`를 SQLAlchemy + sqlite로 박고, 잡 실행 시 file lock. 본 spec 시점엔 single-worker 가정.

---

## 2. 입력 수집

오늘 = `date.today()` (KST 기준). 수집은 병렬.

### 2.1 입력 1: `daily/YYYY-MM-DD.md` (narrative — 1순위)

```python
from pathlib import Path
import frontmatter

def read_daily_narrative(today: date) -> str | None:
    path = Path(f"persona/daily/{today.strftime('%Y-%m-%d')}.md")
    if not path.exists():
        return None
    post = frontmatter.load(path)
    return post.content   # 본문만 (frontmatter 제외)
```

본인이 직접 쓴 narrative라 LLM이 "본인 의도" 이해에 가장 가치 큰 입력. 없는 날은 `None` → LLM 프롬프트에서 "narrative 없음" 명시.

### 2.2 입력 2: 로컬 git log — `notes/` 변경 (note kind 입력)

```python
import subprocess

def git_log_today(path: str, today: date) -> list[dict]:
    # ⚠ TZ 명시 — homeserver clock이 UTC여도 KST 자정 기준으로 잘림
    since_iso = f"{today.isoformat()}T00:00:00+09:00"
    until_iso = f"{(today + timedelta(days=1)).isoformat()}T00:00:00+09:00"
    result = subprocess.run(
        ["git", "log", "--since", since_iso, "--until", until_iso,
         "--name-status", "--pretty=format:%H%n%s%n", path],
        capture_output=True, text=True, check=True,
    )
    # parse: [{commit_sha, subject, files: [...]}]
    return _parse_git_log(result.stdout)

notes_changes = git_log_today("persona/notes/", today)
```

> **TZ 주의**: 홈서버 system clock이 UTC면 `--since "2026-04-30"` 만 박을 시 KST 자정~오전 9시 commit을 다른 날로 잡음. 명시적 `+09:00` ISO timestamp 사용 (또는 plan-01에서 홈서버 TZ를 KST로 박음).

### 2.3 입력 3: 로컬 git log — `contents/` 변경 (study kind 입력)

`§2.2`와 동일 패턴. path만 `persona/contents/`.

### 2.4 입력 4: GitHub commits API — 외부 활동 (commit kind 입력)

> **API 변경 주의** (2026-05): `/users/{user}/events` 의 `PushEvent.payload.commits` 가 빈 배열로 반환됨 (GitHub 동작 변경). `/repos/{owner}/{repo}/commits` 직접 호출로 전환.

#### 2.4.1 tracked repos 추출 — `persona/projects/*.md` SoT

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
        slug = repo_url.split("github.com/", 1)[1].rstrip("/").rstrip(".git")
        if slug.count("/") == 1:
            slugs.add(slug)
    return slugs
```

#### 2.4.2 fetch_repo_commits — repo × account 호출

```python
import httpx
from datetime import date, timedelta

async def fetch_repo_commits(
    owner_repo: str, today: date, token: str, author: str = "",
) -> list[dict]:
    """`/repos/{owner_repo}/commits` — 오늘 (KST) author commits.

    - `since` / `until` 파라미터 KST 기준 ISO timestamp.
    - `author` (optional) — GitHub username 또는 email 매칭.
    - 403/404/409 (권한 없거나 빈 repo) 는 silently skip — 다른 token 시도 가능.
    """
    if not token or not owner_repo:
        return []
    since = f"{today.isoformat()}T00:00:00+09:00"
    until = f"{(today + timedelta(days=1)).isoformat()}T00:00:00+09:00"
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

#### 2.4.3 main_job — tracked × accounts 호출 + dedupe

```python
tracked_repos = extract_tracked_repos(get_data().get("projects", []))
seen: set[tuple[str, str]] = set()
commits: list[dict] = []
for repo in tracked_repos:
    for acc in config.gh_accounts():   # 개인 + 회사 PAT
        for c in await fetch_repo_commits(repo, today, acc["token"], author=acc["user"]):
            key = (c["repo"], c["msg"])
            if key in seen:
                continue
            seen.add(key)
            commits.append(c)
```

GitHub commits API:
- **인증**: PAT (개인 + 회사 분리 — `GH_TOKEN_PERSONAL` / `GH_TOKEN_COMPANY`). 각 계정의 private repo 는 그 계정 PAT 으로만 보임.
- **author 필터**: GitHub `author` 파라미터 — username 또는 email 매칭. 본인 commit 만 발라냄 (PR merge 시 타인 commit 제외).
- **TZ**: `since` / `until` ISO timestamp (`+09:00`). UTC/KST 변환 GitHub 가 처리.
- **rate limit**: 5000 req/hour (PAT). tracked × accounts 호출이라도 무관.
- **보존**: commits API 는 모든 history 반환 (events API 의 90일 제약 없음).

---

## 3. LLM 호출

### 3.1 모델 + 호출 라이브러리

- **모델**: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- **호출 라이브러리**: **`open-kknaks`** (본인 OSS, ADR-04). Anthropic SDK 미사용. Pro/Max 구독 활용 → API 비용 0
- 이유: 매일 1회 짧은 요약. Sonnet은 오버. Haiku는 빠름

### 3.2 프롬프트 (단일 user message)

```python
import json
from open_kknaks import ClaudeClient

# client는 main.py lifespan에서 생성 + 의존성 주입 (ADR-04 §4.2)

async def summarize_activity(
    today: date,
    narrative: str | None,
    notes: list,
    contents: list,
    commits: list,
    client: ClaudeClient,
) -> dict:
    bullets_notes    = "\n".join(f"- {n['subject']}" for n in notes) or "(없음)"
    bullets_contents = "\n".join(f"- {c['subject']}" for c in contents) or "(없음)"
    bullets_commits  = "\n".join(f"- [{c['repo']}] {c['msg'].splitlines()[0]}" for c in commits) or "(없음)"
    narrative_block = (
        f"[본인 narrative — 1순위 입력]\n{narrative}\n"
        if narrative else
        "[본인 narrative]\n(오늘 daily/*.md 미작성 — 사실 데이터로만 요약)\n"
    )

    prompt = f"""오늘({today.isoformat()}) 한 사람의 활동 데이터다.
narrative는 본인 시각의 컨텍스트(1순위 입력), 나머지 3개는 kind 후보다.

{narrative_block}
[kind 후보 1 — note] notes 변경
{bullets_notes}

[kind 후보 2 — study] contents 변경
{bullets_contents}

[kind 후보 3 — commit] GitHub 외부 커밋
{bullets_commits}

다음을 결정해라:
1. kind: "commit" | "note" | "study" 중 가장 의미 있는 활동의 kind. 세 후보 모두 비어있으면 null
2. count: notes + contents + commits 항목 수의 합 (narrative는 셈에서 제외)
3. summary: 무슨 작업을 했는지 한국어/영어 한 줄 (각각 60자 이내, 자연스러운 어투)

응답은 다음 JSON 한 객체만 (다른 텍스트 X):
{{"kind": "...", "count": 0, "summary": {{"ko": "...", "en": "..."}}}}
"""

    task_id = await client.submit(
        prompt=prompt,
        model="claude-haiku-4-5-20251001",
        timeout=120,
        max_retries=2,
    )
    task = await client.result(task_id, timeout=120)
    return json.loads(task.result)
```

### 3.3 응답 검증

```python
def validate_llm_response(resp: dict, today: date) -> dict:
    assert resp.get("kind") in {"commit", "note", "study", None}
    assert isinstance(resp.get("count"), int) and resp["count"] >= 0
    assert isinstance(resp.get("summary"), dict) or resp["summary"] is None
    if resp["summary"]:
        assert "ko" in resp["summary"] and "en" in resp["summary"]
    return {
        "date":    today.strftime("%Y.%m.%d"),
        "count":   resp["count"],
        "kind":    resp["kind"],
        "summary": resp["summary"],
    }
```

검증 실패 시 — LLM 재호출 1회 retry (max_tokens 늘리거나 프롬프트에 "JSON만 출력" 강조). 재차 실패 시 entry skip + 로그.

### 3.4 kind enum 정책

본 spec 시점엔 4종: `commit | note | study | null`.
- `ship` 은 정의 안 됨 (planning-01 §6 미정 결정 — 향후 추가 시 `kind` enum 확장 + 프론트 색상 매핑 갱신).

---

## 4. activity.yaml upsert (idempotent)

같은 날 잡이 두 번 돌아도 결과 동일해야 함 (재실행/백필 안전).

**`totalCount` 정책 = rolling 365일** (잔디는 1년 격자라 spec-01 §4 mock 의도와 정합). 365일 넘은 entry는 트림.

```python
import yaml
from pathlib import Path
from datetime import date, timedelta

ACTIVITY_PATH = Path("persona/activity.yaml")
WINDOW_DAYS = 365

def upsert_activity(entry: dict):
    data = yaml.safe_load(ACTIVITY_PATH.read_text()) if ACTIVITY_PATH.exists() else {
        "since": entry["date"], "until": entry["date"], "totalCount": 0, "items": []
    }
    # 같은 date entry 제거 후 추가 (upsert)
    data["items"] = [e for e in data["items"] if e["date"] != entry["date"]]
    data["items"].append(entry)
    data["items"].sort(key=lambda e: e["date"])

    # rolling 365일 트림
    today = date.fromisoformat(entry["date"].replace(".", "-"))
    cutoff = today - timedelta(days=WINDOW_DAYS - 1)
    cutoff_str = cutoff.strftime("%Y.%m.%d")
    data["items"] = [e for e in data["items"] if e["date"] >= cutoff_str]

    data["since"]      = data["items"][0]["date"]
    data["until"]      = data["items"][-1]["date"]
    data["totalCount"] = sum(e["count"] for e in data["items"])

    ACTIVITY_PATH.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
```

> 만약 향후 누적 카운트(전체 기간)도 필요해지면 별도 필드 `totalCountAllTime` 추가. 본 spec 시점엔 rolling 365 한 가지만.

---

## 5. git push retry loop (ADR-03 §4.3 구체화)

```python
import subprocess

def commit_and_push_with_retry(today: date, max_retries: int = 3):
    msg = f"chore: activity {today.isoformat()}"
    for attempt in range(1, max_retries + 1):
        try:
            # fetch + rebase (history divergence 회피)
            subprocess.run(["git", "fetch", "origin"], check=True)
            subprocess.run(["git", "rebase", "origin/main"], check=True)
            # activity.yaml은 백엔드만 쓰므로 rebase 충돌 불가

            # 변경 없으면 commit skip (idempotent — 같은 entry 재실행)
            diff = subprocess.run(["git", "diff", "--quiet", "persona/activity.yaml"]).returncode
            if diff == 0:
                return   # no changes, nothing to push

            subprocess.run(["git", "add", "persona/activity.yaml"], check=True)
            subprocess.run(["git", "commit", "-m", msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return
        except subprocess.CalledProcessError as e:
            if attempt == max_retries:
                # 모두 실패 — 로그만, 다음 날 retry. activity.yaml은 commit-pending 상태로 남음
                logger.error(f"git push failed after {max_retries} retries: {e}")
                return
            time.sleep(2 ** attempt)   # 2s, 4s
```

### 5.1 git auth (ADR-03 §4.4)

홈서버에 deploy SSH key 또는 PAT 박음:
- **권장**: GitHub deploy key — repo Settings → Deploy keys → Add deploy key. **반드시 "Allow write access" 체크** (default는 read-only). 키 위치 `~/.ssh/id_kknaks_profile`
- systemd: `EnvironmentFile=/etc/kknaks-api.env` (GH_TOKEN 박을 경우, 권한 600)
- git remote는 SSH (`git@github.com:kknaks/kknaks-profile.git`) 또는 HTTPS + PAT

### 5.2 git user identity

자동 commit이라 사용자 ID 명확화:
```bash
# 홈서버 git config
git config user.name  "kknaks-bot"
git config user.email "kknaks-bot@kknaks.dev"
```

→ git log에서 사람 commit과 시각적 구분 가능.

---

## 6. 메모리 reload

push 성공 후 `load_all()` 셀프 호출.

```python
async def daily_activity_job():
    today = date.today()
    narrative = read_daily_narrative(today)
    notes     = git_log_today("persona/notes/", today)
    contents  = git_log_today("persona/contents/", today)
    commits   = []
    for u in GH_USERS:
        commits.extend(await fetch_repo_commits(repo, today, acc["token"], author=acc["user"]))

    resp  = summarize_activity(today, narrative, notes, contents, commits)
    entry = validate_llm_response(resp, today)
    upsert_activity(entry)
    commit_and_push_with_retry(today)

    # 메모리 캐시 갱신 (back/main.py의 load_all)
    # ⚠ 함수 내부 import — module-level이면 main ↔ scheduler 순환 의존
    from main import load_all
    load_all()
```

---

## 7. 백필 (첫 부팅 365일 1회)

GitHub Events API는 90일까지만 → 백필 시 fallback:

| 시점 | 입력 |
|---|---|
| 최근 90일 | Events API 가능 |
| 90일~365일 | GitHub GraphQL `contributionsCollection` (commit count만, 메시지 없음) → LLM 가공 없이 `count` + `kind=commit` + `summary=null`로 박음 |

```python
async def backfill_365_days():
    today = date.today()
    for offset in range(365, -1, -1):
        target = today - timedelta(days=offset)
        # ... §2의 입력 수집 (단, 90일 넘으면 graphql fallback)
        # ... §3의 LLM 호출 (입력 부족하면 skip)
        # ... §4의 upsert
    commit_and_push_with_retry(today, max_retries=3)
```

수동 스크립트로 1회 실행. APScheduler에 안 박음.

**중간 실패 안전성**: 백필이 200번째 entry 쓰고 push 전에 죽어도 — `upsert_activity`가 idempotent이고 `since/until/totalCount` 는 매 entry마다 재계산되니 재실행 안전. 단순히 다시 돌리면 됨.

---

## 8. secret 관리

| 키 | 용도 | 보관 |
|---|---|---|
| ~~`ANTHROPIC_API_KEY`~~ | ~~LLM 호출~~ — **불요** (ADR-04 — open-kknaks worker 가 OAuth 토큰으로 claude CLI 호출) | — |
| `GH_TOKEN` | GitHub REST + GraphQL API 인증 — **필수**. 최소 scope: `read:user`, `public_repo` (private repo 활동도 잡으려면 `repo`). 백필(§7)의 GraphQL `contributionsCollection`은 인증 필수라 anonymous 호출 불가 | systemd EnvironmentFile (`/etc/kknaks-api.env`, chmod 600) |
| `REDIS_URL` | open-kknaks broker 접속 (ADR-04). docker-compose 내부에선 `redis://redis:6379`, host에선 `redis://localhost:46379` | docker-compose env |
| `RELOAD_TOKEN` | webhook → /admin/reload 인증 (M8) | 동상 |
| (SSH deploy key) | git 프로토콜 (push/fetch) — `~/.ssh/id_kknaks_profile`. **API 인증과 별개**. spec-03 §5.1 + plan-01 M0 | 파일시스템 |
| `CLAUDE_CODE_OAUTH_TOKEN` | open-kknaks worker 컨테이너가 claude CLI 호출용. 호스트에서 `claude setup-token` 1회 발급 (ADR-04 §2.2). worker 가 broker 통해 활용 — 본 잡 코드는 직접 안 봄 | docker-compose `.env` |

`.env` 파일은 `.gitignore` 박음 (절대 commit X). 로컬 dev:
```bash
# back/.env (gitignore)
GH_TOKEN=github_pat_...
REDIS_URL=redis://localhost:46379
RELOAD_TOKEN=...
```

---

## 9. 검증 / fail-safe

| 실패 케이스 | 대응 |
|---|---|
| Anthropic API 호출 실패 | 1회 retry. 재차 실패 시 그날 entry skip (다음 날 자동 다시 시도) |
| GitHub API 5xx/timeout | 1회 retry. 재차 실패 시 commits=[] 로 진행 (narrative + git log만으로 LLM 호출) |
| `daily/YYYY-MM-DD.md` 파싱 에러 (frontmatter 형식 위반) | narrative=None 으로 진행 + 로그 |
| activity.yaml write 실패 (디스크 가득) | 잡 abort + 로그 |
| git push 3회 retry 실패 | activity.yaml commit-pending 상태 유지. 다음 날 push 시도 시 자동 포함 |
| LLM 응답 JSON 파싱 실패 | 1회 retry. 재차 실패 시 entry skip |

모든 실패 케이스에서 백엔드 프로세스는 **죽지 않음** (잡은 매일 새로 시도).

---

## 10. 멱등성 / 재실행 안전

- `upsert_activity` 가 같은 date 항목을 갈아끼움 → 같은 날 잡 두 번 돌려도 결과 동일
- `commit_and_push_with_retry` 가 변경 없으면 skip → 재실행 시 빈 commit 생성 X
- 백필 스크립트도 재실행 안전 (날짜별 upsert)

→ 실수로 cron이 두 번 돌아도, 백필이 중복 실행되어도 안전.

---

## 11. 향후 확장 여지 (이 spec 범위 밖)

- `kind` enum 추가 (`ship` 등) — planning-01 §6 미정 항목 결정 시
- 다른 자동 산출물 (weekly digest, monthly summary) — 같은 패턴으로 별도 잡 추가
- LLM 모델 업그레이드 (Sonnet) — 비용 검토 후
- daily/*.md 자동 작성 (오늘 commit 기반 초안 생성 → 본인 검수) — 별도 잡
- multi-worker 운영 시 distributed lock — §1.3 옵션
