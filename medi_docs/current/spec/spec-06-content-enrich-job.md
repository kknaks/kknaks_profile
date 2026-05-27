---
id: spec-06
type: spec
title: 콘텐츠 enrich 잡 명세 — pending stub 폴링 + yt-dlp/transcript + LLM + MD 갱신
status: draft
created: 2026-05-02
updated: 2026-05-02
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[adr-05-content-pending-enrich]]"
  - "[[adr-04-llm-via-open-kknaks]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-03-activity-scheduler]]"
tags: [spec, scheduler, llm, content, youtube, open-kknaks]
---

# 콘텐츠 enrich 잡 명세

## Summary

백엔드 안 APScheduler 가 5~15 분 주기 interval 로 실행. `persona/contents/*.md` 를 스캔해 `status: pending` MD 를 발견하면, 해당 파일의 `youtubeId` 로 ① yt-dlp 메타데이터 ② youtube-transcript-api 자막 ③ open-kknaks LLM 요약 (Claude Haiku 4.5) 을 거쳐 frontmatter (title/summary/duration/tags) 와 본문 (개념/적용/실수 3-section) 을 채우고 `status: published` 로 갱신, fetch+rebase 후 git push (3회 retry), `load_all()` 셀프 호출로 메모리 갱신.

---

## 1. 트리거 + 실행 환경

### 1.1 스케줄

- **주기**: 10 분 interval (`Asia/Seoul` 무관 — 시각 의존 없음)
- **이유**: 사용자가 pending stub 을 push 한 뒤 사이트에 표시되기까지의 지연을 짧게. 너무 짧으면 폴링 부하, 너무 길면 UX 저하.
- **구현**: APScheduler `AsyncIOScheduler` + interval trigger

```python
scheduler.add_job(
    content_enrich_job,
    "interval",
    minutes=10,
    id="content-enrich",
    coalesce=True,           # 백엔드 재시작 중 미스된 실행은 모아서 1번만
    max_instances=1,         # 동시 실행 차단
    next_run_time=datetime.now(),  # 부팅 즉시 1회 (선택)
)
```

### 1.2 single-worker 강제

`spec-03` §1.2 와 동일 — multi-worker 시 잡 N 번 발동. 부팅 시 `WEB_CONCURRENCY` 검증 (이미 `spec-03` 에서 구현, 본 잡도 같은 검증 재사용).

### 1.3 잔디 잡과의 분리

`spec-03` 잔디 잡과는 별도 잡 (다른 `id`). 서로의 실행 결과에 의존하지 않음 — 잔디 잡이 contents 변경을 입력으로 잡지만 (kind=study), enrich 잡이 늦게 돌아도 다음 날 잔디 잡이 잡으니 정합.

---

## 2. 입력 수집 (pending MD 스캔)

### 2.1 스캔 대상

```python
from pathlib import Path
import frontmatter

CONTENTS_DIR = Path("persona/contents")

def scan_pending_contents() -> list[Path]:
    """status: pending 인 contents MD 만 반환."""
    pending: list[Path] = []
    for md_path in CONTENTS_DIR.glob("C-*.md"):
        post = frontmatter.load(md_path)
        if post.metadata.get("status") == "pending":
            pending.append(md_path)
    return pending
```

- `C-*.md` glob — `spec-01` §3.5 파일명 컨벤션 (`C-NNN-slug.md`)
- frontmatter 파싱 실패하는 파일은 skip + 로그 (사용자 작성 오류 — 잡이 실패하면 안 됨)

### 2.2 처리 순서

`scan_pending_contents()` 결과를 한 번의 잡 실행에서 **순차 처리**. 동시성 X — Pro/Max rate limit 안전 + git push 충돌 회피 (한 잡 인스턴스 안에서 commit 직렬화).

만약 한 번의 폴링에서 pending 이 N 개라도 (드문 케이스) 같은 잡 안에서 N 회 LLM 호출 + N 회 commit. 잡 max_instances=1 이라 다음 tick 까지 다 못 끝내도 다음 tick 에 이어 처리.

### 2.3 사용자 입력 frontmatter

사용자가 박는 최소 frontmatter (`spec-01` §3.5 갱신 후 명세):

```yaml
---
id: C-005
type: content
youtubeId: dQw4w9WgXcQ
status: pending          # required
intent: |                # optional — 사용자가 "이 영상에서 강조하고 싶은 점" 한 줄
  FastAPI Depends 세션 lifecycle 가 핵심
---
```

`intent` 가 있으면 LLM 프롬프트에 우선 컨텍스트로 주입 (§3.3) — 자막만으로는 본인 강조점이 안 잡혀서 LLM 본문이 generic 해질 위험 회피.

---

## 3. 처리 — 메타 + 자막 + LLM

### 3.1 yt-dlp 메타 추출

```python
import yt_dlp

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,    # 영상 파일 다운로드 X — 메타만
    "extract_flat": False,
}

def extract_metadata(youtube_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title":       info.get("title"),
        "description": info.get("description"),
        "duration_s":  info.get("duration"),       # 초 단위 int
        "channel":     info.get("uploader"),
        "tags":        info.get("tags") or [],
        "thumbnail":   info.get("thumbnail"),
        "upload_date": info.get("upload_date"),    # YYYYMMDD
    }
```

**duration 포맷**: `info["duration"]` 은 초. frontmatter 표기는 `MM:SS` 또는 `HH:MM:SS` (기존 `C-001` 컨벤션 — `"18:42"`). 변환 헬퍼:

```python
def format_duration(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s   = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
```

### 3.2 youtube-transcript-api 자막 추출

```python
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def extract_transcript(youtube_id: str) -> str | None:
    """ko 우선, 없으면 en, 둘 다 없으면 자동 생성 자막. 모두 실패 시 None."""
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(youtube_id)
        # ko 수동 자막 → en 수동 자막 → ko 자동 → en 자동 순
        for lang_pref in [["ko"], ["en"]]:
            try:
                t = transcripts.find_manually_created_transcript(lang_pref)
                return _join_transcript(t.fetch())
            except NoTranscriptFound:
                continue
        for lang_pref in [["ko"], ["en"]]:
            try:
                t = transcripts.find_generated_transcript(lang_pref)
                return _join_transcript(t.fetch())
            except NoTranscriptFound:
                continue
        return None
    except TranscriptsDisabled:
        return None

def _join_transcript(segments: list[dict]) -> str:
    return " ".join(s["text"].strip() for s in segments if s.get("text"))
```

자막이 없는 영상 — `transcript = None` 으로 다음 단계 진행 (메타 + description 만 LLM 에 전달, 본문 품질 저하 감수).

### 3.3 open-kknaks LLM 호출

```python
import json
from open_kknaks import ClaudeClient

async def summarize_content(
    youtube_id: str,
    metadata: dict,
    transcript: str | None,
    user_intent: str | None,
    client: ClaudeClient,
) -> dict:
    transcript_block = (
        f"[자막 (전체)]\n{transcript[:8000]}\n"
        if transcript else
        "[자막]\n(자막 없음 — 메타데이터와 description 만으로 가공)\n"
    )
    intent_block = (
        f"[사용자 의도 — 1순위]\n{user_intent}\n"
        if user_intent else
        ""
    )

    prompt = f"""YouTube 영상의 강의 교안을 작성한다. **외부 사람이 영상을 안 보고도 이 문서만으로 이해·학습할 수 있어야 한다.**

[원본 메타]
- title: {metadata['title']}
- channel: {metadata['channel']}
- duration: {metadata['duration_s']}s
- tags: {", ".join(metadata['tags'][:20])}
- description: {(metadata['description'] or '')[:2000]}

{intent_block}{transcript_block}

다음 6개 항목을 결정해라:
1. title: 교안 제목 (한국어/영어 각각, 60자 이내, 원본 title 보다 간결·구체적)
2. summary: 영상 핵심 한 줄 (한국어/영어 각각, 80자 이내)
3. tags: 기술 스택/키워드 (3~7개, 소문자 + #prefix — 예 `#fastapi`)
4. concept: 핵심 개념 짧은 문장 **4~6개** (한국어, 각 1~2문장, 사이트 카드용 압축 요약). body 의 풀 설명을 한 줄씩 압축한 형태.
5. body: 강의 교안 (한국어 markdown). **반드시 다음 8개 H2 섹션을 순서대로 모두 포함**:
   - `## 개요`: 주제와 왜 중요한지 (1~2문단, 독자가 왜 이 글을 읽어야 하는지)
   - `## 배경 / 사전 지식`: 이해에 필요한 선수 지식·용어 정의
   - `## 핵심 개념`: 단락별 정의 + 작동 원리 (개념별 H3 분리 권장)
   - `## 작동 원리`: 단계별 설명 (numbered list 또는 시퀀스 식)
   - `## 코드 예시`: 실행 가능한 코드 (최소 1개 ```언어``` 블록) + 각 줄/블록 의미 주석
   - `## 함정·실수`: 흔히 빠지는 실수 + 회피법 (영상 짚은 것 + 일반적 함정)
   - `## 베스트 프랙티스`: 권장 패턴, 대안, 더 나아가는 팁
   - `## 참고`: 영상에서 언급된 추가 자료·링크 (없으면 "(영상 내 명시 없음)")
   섹션은 빠짐없이 박되, 영상에 명시 안 된 항목은 자막에서 합리적 추론하거나 베스트 프랙티스로 채운다. **분량 압축 X — 외부 사람이 학습 가능한 수준으로 풍부하게.**
6. kind: 영상 유형 — "study" | "talk" | "tutorial" | "review" 중 하나

응답 형식 — 정확히 다음 순서대로 박는다:

[1] JSON 한 객체만 (다른 텍스트 X, 코드블록 ```json``` 도 박지 않음, **body 필드 없음**):
{{
  "title":   {{"ko": "...", "en": "..."}},
  "summary": {{"ko": "...", "en": "..."}},
  "tags":    ["#tag1", "#tag2"],
  "concept": ["문장1", "문장2", "문장3", "문장4"],
  "kind":    "tutorial"
}}

[2] 빈 줄 하나

[3] 정확히 `---BODY---` 한 줄

[4] 강의 교안 markdown 본문 (raw — JSON escape 불필요, `"`, 코드블록, 줄바꿈 자유롭게 사용. 본문은 `## 개요` 부터 시작).
"""

    task_id = await client.submit(
        prompt=prompt,
        model="claude-haiku-4-5-20251001",
        timeout=180,                   # 자막이 길면 처리 시간 증가
        max_retries=2,
    )
    task = await client.result(task_id, timeout=180)
    return _parse_response(task.result)


def _parse_response(text: str) -> dict:
    """JSON metadata + ---BODY--- separator + raw markdown body 분리.

    body 를 JSON 안에 박으면 따옴표/줄바꿈 escape 실수로 invalid JSON 사례 잦음 (e.g. C-018 H-jSrhvnaLY)
    → body 를 JSON 밖으로 분리. JSON 안에는 짧고 안전한 필드만.
    """
    if "---BODY---" not in text:
        raise ValueError("missing_body_separator")
    json_part, body_part = text.split("---BODY---", 1)
    start, end = json_part.find("{"), json_part.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("missing_json_object")
    meta = json.loads(json_part[start : end + 1])
    meta["body"] = body_part.strip()
    return meta
```

자막 토큰 절감 — 8000 자 컷 (Haiku 입력 한도 안에서 안전).

### 3.4 응답 검증

```python
def validate_llm_response(resp: dict) -> dict:
    assert isinstance(resp.get("title"), dict) and {"ko", "en"} <= resp["title"].keys()
    assert isinstance(resp.get("summary"), dict) and {"ko", "en"} <= resp["summary"].keys()
    assert isinstance(resp.get("tags"), list) and 1 <= len(resp["tags"]) <= 10
    assert all(t.startswith("#") for t in resp["tags"])
    assert isinstance(resp.get("concept"), list) and 2 <= len(resp["concept"]) <= 10
    assert all(isinstance(c, str) and c.strip() for c in resp["concept"])
    assert isinstance(resp.get("body"), str) and len(resp["body"]) >= 50
    if resp.get("kind") not in {"study", "talk", "tutorial", "review"}:
        resp["kind"] = "study"   # fallback (Claude 가 종종 빠뜨림)
    return resp
```

검증 실패 시 — 1회 retry. 재차 실패 시 `status: error` + `error_reason: "llm_validation_failed"` 로 기록.

---

## 4. MD 갱신 (idempotent)

### 4.1 frontmatter 머지

사용자가 박은 frontmatter 의 키는 **유지** (사용자가 수동으로 박은 값 우선). 잡이 채우는 키는 *비어있을 때만* 박음 (사용자가 검수 후 수정한 값을 다시 덮지 않기 위함).

```python
def merge_frontmatter(user_meta: dict, llm_resp: dict, metadata: dict, today: date) -> dict:
    # 사용자 입력 보존 (필수: id, type, youtubeId, status, intent)
    out = dict(user_meta)

    # 잡이 채우는 키 — 비어있을 때만
    out.setdefault("date",       today.strftime("%Y.%m.%d"))
    out.setdefault("day",        f"Day {_compute_day_index(today)}")
    out.setdefault("title",      llm_resp["title"])
    out.setdefault("summary",    llm_resp["summary"])
    out.setdefault("duration",   format_duration(metadata["duration_s"]))
    out.setdefault("speaker",    metadata["channel"])
    out.setdefault("tags",       llm_resp["tags"])
    out.setdefault("concept",    llm_resp["concept"])
    out.setdefault("kind",       llm_resp["kind"])

    # 자막 가용성 표시 (선택적 표시용)
    out["transcript"] = bool(metadata.get("_transcript_available"))

    # 마지막에 status 갱신 (성공)
    out["status"] = "published"
    out["enriched_at"] = datetime.now(KST).isoformat()
    return out
```

> `Day N` 인덱스 계산은 `spec-01` §3.5 의 day 컨벤션을 따름 — 첫 contents 부터의 누적 일수. `_compute_day_index` 는 같은 디렉토리의 기존 contents 중 가장 큰 day 값 + 1 로 결정 (단순화).

### 4.2 본문 dump

```python
def write_enriched(md_path: Path, frontmatter_dict: dict, body: str):
    post = frontmatter.Post(content=body, **frontmatter_dict)
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
```

본문은 LLM 응답의 `body` 그대로 (개념/적용/실수 3 섹션). 사용자가 검수 후 수정해서 push 하면, 다음 잡 폴링 시 `status: published` 라 skip — 덮어쓰지 않음 (멱등).

---

## 5. git push retry loop

`spec-03` §5 패턴 그대로 재사용 — 차이는 add 대상이 `persona/activity.yaml` 이 아니라 `persona/contents/C-NNN-slug.md`.

```python
def commit_enriched_content(md_path: Path, max_retries: int = 3):
    msg = f"chore: enrich {md_path.stem}"
    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(["git", "fetch", "origin"], check=True)
            subprocess.run(["git", "rebase", "origin/main"], check=True)
            diff = subprocess.run(["git", "diff", "--quiet", str(md_path)]).returncode
            if diff == 0:
                return
            subprocess.run(["git", "add", str(md_path)], check=True)
            subprocess.run(["git", "commit", "-m", msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return
        except subprocess.CalledProcessError as e:
            if attempt == max_retries:
                logger.error(f"git push failed after {max_retries} retries: {e}")
                return
            time.sleep(2 ** attempt)
```

git auth / user identity 는 `spec-03` §5.1, §5.2 그대로 재사용 (홈서버 동일 환경).

---

## 6. 메모리 reload

push 성공 후 `load_all()` 셀프 호출 — `spec-03` §6 패턴.

```python
async def content_enrich_job():
    pending = scan_pending_contents()
    if not pending:
        return

    client = app.state.claude_client   # ADR-04 lifespan 주입

    for md_path in pending:
        try:
            await _enrich_one(md_path, client)
        except Exception as e:
            _mark_error(md_path, reason=str(e))
            continue

    # 메모리 캐시 갱신
    from main import load_all
    load_all()


async def _enrich_one(md_path: Path, client: ClaudeClient):
    post = frontmatter.load(md_path)
    youtube_id = post.metadata["youtubeId"]
    user_intent = post.metadata.get("intent")

    metadata   = extract_metadata(youtube_id)
    transcript = extract_transcript(youtube_id)
    metadata["_transcript_available"] = transcript is not None

    llm_resp = await summarize_content(youtube_id, metadata, transcript, user_intent, client)
    llm_resp = validate_llm_response(llm_resp)

    new_meta = merge_frontmatter(post.metadata, llm_resp, metadata, date.today())
    write_enriched(md_path, new_meta, llm_resp["body"])
    commit_enriched_content(md_path)
```

---

## 7. 실패 처리

```python
def _mark_error(md_path: Path, reason: str):
    post = frontmatter.load(md_path)
    post.metadata["status"] = "error"
    post.metadata["error_reason"] = reason
    post.metadata["errored_at"] = datetime.now(KST).isoformat()
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    commit_enriched_content(md_path)   # 에러 상태도 commit (사용자가 git에서 보고 대응)
```

| 실패 케이스 | 대응 |
|---|---|
| yt-dlp 메타 추출 실패 (영상 비공개/삭제/지역 차단) | `status: error`, `error_reason: "metadata_extraction_failed"` |
| youtube-transcript-api 자막 차단/없음 | 무시 (transcript=None 으로 진행). `transcript: false` frontmatter 박음 |
| open-kknaks 호출 실패 (worker 다운, OAuth 만료) | 1회 retry. 재차 실패 시 `status: error`, `error_reason: "llm_call_failed"` |
| LLM 응답 JSON 파싱/검증 실패 | 1회 retry. 재차 실패 시 `status: error`, `error_reason: "llm_validation_failed"` |
| frontmatter merge 시 사용자 입력 frontmatter 형식 위반 | 잡 abort + 로그 — 사용자가 stub 수정 후 다시 push해야 함. status 변경 X |
| git push 3회 retry 실패 | enriched MD 는 로컬에 남고 commit-pending. 다음 tick 에서 `status: published` 라 skip — 다음 잡 호출 외부 메커니즘 (M8 webhook 또는 다음 push 시) 필요 |

**사용자 재시도 흐름**: `status: error` 박힌 파일을 직접 `status: pending` 으로 되돌리고 push → 다음 tick 에 잡이 다시 처리.

---

## 8. 멱등성 / 재실행 안전

- `scan_pending_contents()` 가 `status: pending` 만 반환 → 같은 파일이 두 번 처리되지 않음 (한 번 처리 후 `published` 됨)
- `_mark_error` 도 `status: error` 박으니 다음 tick 에 다시 잡힐 일 X
- 사용자가 수동으로 published 상태의 본문을 수정해도, status 가 published 라 잡이 덮지 않음
- 사용자가 status 를 pending 으로 되돌리면 → 잡이 frontmatter 의 잡-출력 키 (`title`/`summary`/`tags` 등) 도 다시 덮어씀 — `merge_frontmatter` 의 `setdefault` 는 *비어있을 때만* 박지만, status 를 되돌릴 때 사용자가 해당 키들도 같이 비워야 명확. 이 워크플로우는 runbook 으로 박음 (`spec-06` 시점 out-of-scope)

---

## 9. secret 관리

| 키 | 용도 | 보관 |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | open-kknaks worker 가 claude CLI 인증용 (`adr-04` §2.2) — 본 잡 코드는 직접 안 봄, broker 통신 | docker-compose `.env` |
| `REDIS_URL` | open-kknaks broker 접속 — `spec-03` §8 와 동일 | docker-compose env |
| `GH_TOKEN` | git push 시 PAT 사용 (SSH deploy key 사용 시 불요) — `spec-03` §8 와 동일 | systemd EnvironmentFile |
| (yt-dlp / youtube-transcript-api) | API key **불요** — 둘 다 스크래핑 방식 | — |

**ANTHROPIC_API_KEY 불요** (`adr-04` 결정).

---

## 10. 검증 / fail-safe

- 잡 자체가 백엔드 프로세스를 죽이지 않음 — 모든 예외는 `_mark_error` 로 status 만 갱신
- `status: error` 박힌 파일은 사이트 표시 시 어떻게 처리할지 — `spec-02` API 응답에서 `status != published` 는 제외하는 게 안전. 본 spec 시점 out-of-scope (별도 갱신)
- 폴링 부하 — pending MD 가 N=0 일 땐 단순 glob + frontmatter 파싱만 (수십 ms). 부담 없음

---

## 11. 향후 확장 여지 (이 spec 범위 밖)

- 본문 템플릿 다양화 — 영상 종류별 (강연/리뷰/튜토리얼) 다른 섹션 구성
- 자동 위키링크 — 본문에 등장한 기술 키워드를 `persona/notes/*.md` 와 매칭해 `[[wikilink]]` 로 치환
- multi-language 본문 — 현재 본문은 한국어만. en 본문을 별도로 LLM 호출해 박을지 결정 (비용 + 품질 trade-off)
- preview 모드 — `status: pending` 인 영상도 스켈레톤으로 표시 (frontmatter title 만 사용자가 미리 박았을 때)
- 사용자가 "이 영상 enrich 다시 돌려" 명령용 admin endpoint (현재는 status 수동 되돌림)
- 자막 길이가 8000 자 넘는 긴 영상 — chunking + 단계별 요약 (현재는 단순 truncate)
