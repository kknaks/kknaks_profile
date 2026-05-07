"""LeetCode GraphQL + neetcode-gh raw 응답 shape 탐색 스크립트.

plan-02 M3 (a) fetch 단계의 *실 응답* 을 보고 fetch.py 모듈 설계 결정.

사용법:
    python scripts/explore_leetcode.py            # default = two-sum
    python scripts/explore_leetcode.py contains-duplicate

zero-dep — stdlib urllib 만. 본 스크립트는 탐색용이라 back/ 의존성 안 박음.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

LEETCODE_GRAPHQL = "https://leetcode.com/graphql/"
NEETCODE_RAW_BASE = "https://raw.githubusercontent.com/neetcode-gh/leetcode/main/python"

QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    content
    difficulty
    exampleTestcases
    hints
    topicTags {
      name
      slug
    }
    sampleTestCase
    metaData
  }
}
"""


def fetch_leetcode(slug: str) -> dict:
    """LeetCode GraphQL POST."""
    body = json.dumps(
        {
            "query": QUESTION_QUERY,
            "variables": {"titleSlug": slug},
            "operationName": "questionData",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        LEETCODE_GRAPHQL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (kknaks-profile-explore)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fetch_neetcode(slug: str, number: int) -> tuple[str, str]:
    """neetcode-gh repo 의 python solution raw fetch.

    Returns (path_tried, content_or_error).
    """
    # neetcode-gh 패턴: python/0001-two-sum.py
    candidates = [
        f"{NEETCODE_RAW_BASE}/{number:04d}-{slug}.py",
        f"{NEETCODE_RAW_BASE}/{slug}.py",  # fallback
    ]
    last_err = ""
    for url in candidates:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kknaks-profile-explore"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return url, resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            last_err = f"{e.code} at {url}"
            continue
    return "(none)", f"all paths failed; last: {last_err}"


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "two-sum"
    print(f"=== LeetCode GraphQL — slug='{slug}' ===\n")

    try:
        data = fetch_leetcode(slug)
    except urllib.error.HTTPError as e:
        print(f"GraphQL HTTP error: {e.code} {e.reason}")
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"body: {body}")
        sys.exit(1)

    if "errors" in data:
        print("GraphQL errors:", json.dumps(data["errors"], indent=2, ensure_ascii=False))
        sys.exit(1)

    q = data.get("data", {}).get("question")
    if q is None:
        print("question = null. slug 잘못됐을 가능성.")
        print("response:", json.dumps(data, indent=2, ensure_ascii=False)[:500])
        sys.exit(1)

    # 핵심 필드 출력
    print(f"questionId         : {q.get('questionId')}")
    print(f"questionFrontendId : {q.get('questionFrontendId')}")
    print(f"title              : {q.get('title')}")
    print(f"titleSlug          : {q.get('titleSlug')}")
    print(f"difficulty         : {q.get('difficulty')}")
    print(f"topicTags          : {[t['slug'] for t in q.get('topicTags', [])]}")
    print(f"hints              : {len(q.get('hints', []))} hint(s)")

    print(f"\n--- content (HTML?) — first 800 chars ---")
    print((q.get("content") or "")[:800])

    print(f"\n--- exampleTestcases (raw string) ---")
    print(repr(q.get("exampleTestcases")))

    print(f"\n--- sampleTestCase (raw) ---")
    print(repr(q.get("sampleTestCase")))

    print(f"\n--- metaData (raw) ---")
    print(repr(q.get("metaData")))

    # neetcode-gh fetch
    number = int(q.get("questionFrontendId") or 0)
    print(f"\n=== neetcode-gh raw — slug='{slug}', number={number} ===\n")
    url, code = fetch_neetcode(slug, number)
    print(f"resolved URL: {url}")
    print(f"size        : {len(code)} chars")
    print(f"\n--- code (first 1200 chars) ---")
    print(code[:1200])


if __name__ == "__main__":
    main()
