"""content enrich 잡 — pending 스캔 → yt-dlp + transcript + LLM → MD 갱신 → push (spec-06).

git push 부분만 STUB (잔디 잡 git_push.py 와 분리 — 잔디 검증 완료 후 통합).
외부 호출 (yt-dlp / youtube-transcript-api / open-kknaks) 은 모두 실 구현.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import frontmatter
import yt_dlp
from open_kknaks import ClaudeClient, RedisBroker
from youtube_transcript_api import YouTubeTranscriptApi

import config
from service.jobs.git_push import commit_and_push_with_retry

logger = logging.getLogger("kknaks-back.content-enrich")

KST = timezone(timedelta(hours=9))
ALLOWED_KINDS = {"study", "talk", "tutorial", "review"}

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "extract_flat": False,
}

LLM_MODEL = "claude-haiku-4-5-20251001"
LLM_NAMESPACE = "kknaks-portfolio"
LLM_TIMEOUT_S = 180


# ───────────────────────────────────────────────────────────────────────
# 입력 — pending 스캔 (spec-06 §2)
# ───────────────────────────────────────────────────────────────────────

def scan_pending_contents(contents_dir: Path) -> list[Path]:
    """status: pending 인 contents MD 만 반환 (spec-06 §2.1).

    frontmatter 파싱 실패한 파일은 skip + 로그.
    """
    pending: list[Path] = []
    for md_path in sorted(contents_dir.glob("C-*.md")):
        try:
            post = frontmatter.load(md_path)
        except Exception as e:
            logger.warning("frontmatter parse failed: %s — %s", md_path, e)
            continue
        if post.metadata.get("status") == "pending":
            pending.append(md_path)
    return pending


# ───────────────────────────────────────────────────────────────────────
# 외부 호출 — 실 구현 (spec-06 §3)
# ───────────────────────────────────────────────────────────────────────

def extract_metadata(youtube_id: str) -> dict:
    """yt-dlp 메타 — spec-06 §3.1."""
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title") or "",
        "description": info.get("description") or "",
        "duration_s": int(info.get("duration") or 0),
        "channel": info.get("uploader") or info.get("channel") or "",
        "tags": info.get("tags") or [],
        "thumbnail": info.get("thumbnail") or "",
        "upload_date": info.get("upload_date") or "",
    }


def extract_transcript(youtube_id: str) -> str | None:
    """youtube-transcript-api 1.x — ko 우선, 없으면 en (spec-06 §3.2). 실패 시 None."""
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(youtube_id, languages=["ko", "en"])
    except Exception as e:
        logger.warning("transcript fetch error for %s: %s", youtube_id, e)
        return None
    return " ".join(s.text.strip() for s in fetched.snippets if getattr(s, "text", None))


def _build_prompt(
    metadata: dict,
    transcript: str | None,
    user_intent: str | None,
) -> str:
    """spec-06 §3.3 프롬프트 빌드."""
    transcript_block = (
        f"[자막 (전체)]\n{transcript[:8000]}\n"
        if transcript
        else "[자막]\n(자막 없음 — 메타데이터와 description 만으로 가공)\n"
    )
    intent_block = f"[사용자 의도 — 1순위]\n{user_intent}\n\n" if user_intent else ""
    tags_str = ", ".join((metadata.get("tags") or [])[:20])
    desc_truncated = (metadata.get("description") or "")[:2000]
    return f"""YouTube 영상의 강의 교안을 작성한다. **외부 사람이 영상을 안 보고도 이 문서만으로 이해·학습할 수 있어야 한다.**

[원본 메타]
- title: {metadata.get('title', '')}
- channel: {metadata.get('channel', '')}
- duration: {metadata.get('duration_s', 0)}s
- tags: {tags_str}
- description: {desc_truncated}

{intent_block}{transcript_block}

다음 6개 항목을 결정해라:
1. title: 교안 제목 (한국어/영어 각각, 60자 이내, 원본 title 보다 간결·구체적)
2. summary: 영상 핵심 한 줄 (한국어/영어 각각, 80자 이내)
3. tags: 기술 스택/키워드 (3~7개, 소문자 + #prefix — 예 `#fastapi`)
4. concept: 핵심 개념 짧은 문장 **4~6개** (한국어, 각 1~2문장, 사이트 카드용 압축 요약). body 의 풀 설명을 한 줄씩 압축한 형태. 예: ["HNSW는 다층 그래프로 ANN을 수행한다.", "상위 레이어일수록 sparse — ...", ...]
5. body: 강의 교안 (한국어 markdown). **반드시 다음 8개 H2 섹션을 순서대로 모두 포함**:
   - `## 개요`: 주제와 왜 중요한지 (1~2문단, 독자가 왜 이 글을 읽어야 하는지)
   - `## 배경 / 사전 지식`: 이해에 필요한 선수 지식·용어 정의 (모르는 사람도 따라올 수 있도록)
   - `## 핵심 개념`: 단락별 정의 + 작동 원리 (개념별 H3 분리 권장)
   - `## 작동 원리`: 단계별 설명 (numbered list 또는 시퀀스 다이어그램 식)
   - `## 코드 예시`: 실행 가능한 코드 (최소 1개 ```언어``` 블록) + 각 줄/블록의 의미 주석 또는 본문 설명
   - `## 함정·실수`: 흔히 빠지는 실수 + 회피법 (영상에서 짚은 것 + 일반적인 함정)
   - `## 베스트 프랙티스`: 권장 패턴, 대안, 더 나아가는 팁
   - `## 참고`: 영상에서 언급된 추가 자료·링크 (없으면 "(영상 내 명시 없음)")
   섹션은 빠짐없이 박되, 영상에 명시되지 않은 항목은 자막에서 합리적으로 추론하거나 일반적으로 알려진 베스트 프랙티스로 채운다. 분량 짧게 압축 X — 외부 사람이 학습 가능한 수준으로 풍부하게.
6. kind: 영상 유형 — "study" | "talk" | "tutorial" | "review" 중 하나

응답은 다음 JSON 한 객체만 (다른 텍스트 X, 코드블록 ```json``` 도 안 박음):
{{
  "title":   {{"ko": "...", "en": "..."}},
  "summary": {{"ko": "...", "en": "..."}},
  "tags":    ["#tag1", "#tag2"],
  "concept": ["문장1", "문장2", "문장3", "문장4"],
  "body":    "## 개요\\n...\\n\\n## 배경 / 사전 지식\\n...",
  "kind":    "tutorial"
}}
"""


async def summarize_content(
    youtube_id: str,
    metadata: dict,
    transcript: str | None,
    user_intent: str | None,
    client: ClaudeClient,
) -> dict:
    """open-kknaks LLM 호출 — spec-06 §3.3, ADR-04."""
    prompt = _build_prompt(metadata, transcript, user_intent)
    task_id = await client.submit(
        prompt=prompt,
        model=LLM_MODEL,
        timeout=LLM_TIMEOUT_S,
        max_retries=2,
    )
    task = await client.result(task_id, timeout=LLM_TIMEOUT_S)
    return json.loads(_extract_json(task.result or ""))


def _extract_json(text: str) -> str:
    """LLM 응답에서 JSON 객체만 추출 — Claude 가 ```json ... ``` 또는 prefix 텍스트 박는 패턴 대응."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


# ───────────────────────────────────────────────────────────────────────
# 검증 + 변환 (spec-06 §3.4, §4)
# ───────────────────────────────────────────────────────────────────────

def validate_llm_response(resp: dict) -> dict:
    """spec-06 §3.4 — 응답 형식 검증."""
    title = resp.get("title")
    summary = resp.get("summary")
    tags = resp.get("tags")
    concept = resp.get("concept")
    body = resp.get("body")
    kind = resp.get("kind")

    if not (isinstance(title, dict) and {"ko", "en"} <= title.keys()):
        raise ValueError("invalid_title")
    if not (isinstance(summary, dict) and {"ko", "en"} <= summary.keys()):
        raise ValueError("invalid_summary")
    if not (isinstance(tags, list) and 1 <= len(tags) <= 10 and all(isinstance(t, str) and t.startswith("#") for t in tags)):
        raise ValueError("invalid_tags")
    if not (isinstance(concept, list) and 2 <= len(concept) <= 10 and all(isinstance(c, str) and c.strip() for c in concept)):
        raise ValueError("invalid_concept")
    if not (isinstance(body, str) and len(body) >= 50):
        raise ValueError("invalid_body")
    if kind not in ALLOWED_KINDS:
        logger.warning("kind=%r not in %s — fallback to 'study'", kind, ALLOWED_KINDS)
        resp["kind"] = "study"
    return resp


def format_duration(seconds: int) -> str:
    """초 → MM:SS 또는 H:MM:SS (spec-06 §3.1)."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _compute_day_index(contents_dir: Path) -> int:
    """기존 contents 중 가장 큰 day 값 + 1 — spec-06 §4.1 단순화 룰."""
    max_day = 0
    for md_path in contents_dir.glob("C-*.md"):
        try:
            post = frontmatter.load(md_path)
        except Exception:
            continue
        day_str = str(post.metadata.get("day", "Day 0"))
        try:
            n = int(day_str.split()[-1])
            max_day = max(max_day, n)
        except (ValueError, IndexError):
            continue
    return max_day + 1


def merge_frontmatter(
    user_meta: dict,
    llm_resp: dict,
    metadata: dict,
    today: date,
    day_index: int,
    transcript_available: bool,
) -> dict:
    """사용자 입력 보존 + 잡 출력 추가 (spec-06 §4.1).

    setdefault — 사용자가 미리 박은 값은 덮지 않음. status/transcript/enriched_at 은 항상 갱신.
    """
    out = dict(user_meta)
    out.setdefault("date", today.strftime("%Y.%m.%d"))
    out.setdefault("day", f"Day {day_index:02d}")
    out.setdefault("title", llm_resp["title"])
    out.setdefault("summary", llm_resp["summary"])
    out.setdefault("duration", format_duration(metadata["duration_s"]))
    out.setdefault("speaker", metadata["channel"])
    out.setdefault("tags", llm_resp["tags"])
    out.setdefault("concept", llm_resp["concept"])
    out.setdefault("kind", llm_resp["kind"])
    out["transcript"] = bool(transcript_available)
    out["enriched_at"] = datetime.now(KST).isoformat(timespec="seconds")
    out["status"] = "published"
    out.pop("error_reason", None)
    out.pop("errored_at", None)
    return out


def write_enriched(md_path: Path, frontmatter_dict: dict, body: str) -> None:
    """enriched MD 디스크 쓰기 (spec-06 §4.2)."""
    post = frontmatter.Post(content=body, **frontmatter_dict)
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")


def mark_error(md_path: Path, reason: str) -> None:
    """잡 실패 시 status: error + error_reason 박기 (spec-06 §7)."""
    try:
        post = frontmatter.load(md_path)
    except Exception:
        logger.error("cannot mark error on unparseable file: %s", md_path)
        return
    post.metadata["status"] = "error"
    post.metadata["error_reason"] = reason
    post.metadata["errored_at"] = datetime.now(KST).isoformat(timespec="seconds")
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")


# ───────────────────────────────────────────────────────────────────────
# 잡 orchestrator (spec-06 §6)
# ───────────────────────────────────────────────────────────────────────

async def _enrich_one(md_path: Path, contents_dir: Path, client: ClaudeClient) -> None:
    """파일 1개 enrich — spec-06 §6 핵심 흐름."""
    post = frontmatter.load(md_path)
    youtube_id = post.metadata.get("youtubeId")
    if not youtube_id:
        raise ValueError("missing_youtubeId")
    user_intent = post.metadata.get("intent")

    metadata = extract_metadata(youtube_id)
    transcript = extract_transcript(youtube_id)
    transcript_available = transcript is not None

    llm_resp = await summarize_content(youtube_id, metadata, transcript, user_intent, client)
    llm_resp = validate_llm_response(llm_resp)

    day_index = _compute_day_index(contents_dir)
    new_meta = merge_frontmatter(
        post.metadata,
        llm_resp,
        metadata,
        date.today(),
        day_index,
        transcript_available,
    )
    write_enriched(md_path, new_meta, llm_resp["body"])


async def run_content_enrich_job(
    client: ClaudeClient | None = None,
    *,
    dry_run_push: bool | None = None,
) -> int:
    """spec-06 §6 — pending 스캔 → enrich → push → reload.

    client 미지정 시 함수 내부에서 broker 연결/종료 (self-contained — main.py lifespan 미갱신 단계).
    Returns 처리한 파일 수.
    """
    contents_dir = config.PERSONA_DIR / "contents"
    if not contents_dir.exists():
        logger.info("contents dir 없음: %s", contents_dir)
        return 0

    pending = scan_pending_contents(contents_dir)
    if not pending:
        return 0

    logger.info("content enrich: %d pending", len(pending))
    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push

    own_broker: RedisBroker | None = None
    if client is None:
        own_broker = RedisBroker(url=config.redis_url(), namespace=LLM_NAMESPACE)
        await own_broker.connect()
        client = ClaudeClient(broker=own_broker)
        logger.info("open-kknaks broker connected (self-contained): %s", config.redis_url())

    processed = 0
    try:
        for md_path in pending:
            try:
                await _enrich_one(md_path, contents_dir, client)
                commit_and_push_with_retry(
                    paths=[md_path],
                    message=f"chore: enrich {md_path.stem}",
                    dry_run=dry_run,
                )
                processed += 1
            except Exception as e:
                logger.exception("content enrich failed: %s", md_path)
                mark_error(md_path, reason=f"{type(e).__name__}: {e}")
                commit_and_push_with_retry(
                    paths=[md_path],
                    message=f"chore: enrich {md_path.stem} (error)",
                    dry_run=dry_run,
                )
    finally:
        if own_broker is not None:
            await own_broker.close()

    if processed > 0:
        from main import load_all

        load_all()
        logger.info("content enrich done: %d processed", processed)
    return processed
