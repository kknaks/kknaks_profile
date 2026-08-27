#!/usr/bin/env python3
"""공고 페이지를 받아 jd.md 초안(frontmatter + 원문)을 stdout 으로 낸다.

사용:
    python3 fetch_jd.py <URL> [> jd.md]

- 브라우저 UA 로 요청한다 (일반 UA 는 403 이 흔하다).
- greetinghr 류 Next.js SPA 면 __NEXT_DATA__ JSON 에서 본문(openingsInfo.detail)과
  메타(제목·마감·고용형태·근무지)를 뽑는다.
- 아니면 태그를 걷어낸 본문 텍스트를 낸다 — 사람이 다듬는 초안이다.
- 페이월·봇 차단(403 이 UA 재시도 후에도 남으면)은 우회하지 않고 그대로 실패한다.

표준 라이브러리만 쓴다.
"""

import html
import json
import re
import sys
import urllib.request
from datetime import date

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept-Language": "ko-KR,ko;q=0.9"}
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", errors="replace")


def strip_tags(fragment: str) -> str:
    txt = re.sub(r"<br\s*/?>", "\n", fragment)
    txt = re.sub(r"</(p|li|h\d|div)>", "\n", txt)
    txt = re.sub(r"<li[^>]*>", "- ", txt)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = html.unescape(txt)
    return re.sub(r"\n{3,}", "\n\n", txt).strip()


def find_key(obj, key):
    """중첩 JSON 에서 key 를 가진 첫 dict 값을 찾는다."""
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for v in obj.values():
            yield from find_key(v, key)
    elif isinstance(obj, list):
        for v in obj:
            yield from find_key(v, key)


def greeting_meta(data):
    """greetinghr __NEXT_DATA__ 에서 공고 메타를 뽑는다. 없으면 {}."""
    meta = {}
    for oi in find_key(data, "openingsInfo"):
        if not isinstance(oi, dict):
            continue
        meta["포지션"] = oi.get("title", "")
        meta["status"] = oi.get("status", "")
        meta["게시"] = (oi.get("openDate") or "")[:10]
        meta["마감"] = (oi.get("dueDate") or "")[:10]
        meta["본문"] = strip_tags(oi.get("detail", ""))
        break
    raw = json.dumps(data, ensure_ascii=False)
    for k, label in [
        ("employmentType", "고용형태"),
        ("careerType", "채용형태"),
        ("occupation", "직군"),
        ("location", "근무지"),
    ]:
        m = re.search(r'"%s"\s*:\s*"([^"]*)"' % k, raw)
        if m:
            meta[label] = m.group(1)
    return meta


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    url = sys.argv[1]
    page = fetch(url)

    meta, body = {}, ""
    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        page,
        re.S,
    )
    if m:
        data = json.loads(m.group(1))
        meta = greeting_meta(data)
        body = meta.pop("본문", "")
    if not body:
        body = strip_tags(re.sub(r"<(script|style)[^>]*>.*?</\1>", "", page, flags=re.S))

    print("---")
    print(f"source: {url}")
    print(f"fetched: {date.today().isoformat()}")
    for k in ("status", "포지션", "직군", "고용형태", "채용형태", "근무지", "게시", "마감"):
        if meta.get(k):
            print(f"{k}: {meta[k]}")
    print("---")
    print()
    print("# 채용공고 원문")
    print()
    print("> 아래는 크롤링 원문. 수정하지 않는다. (회사·법인명은 사람이 frontmatter 에 보충)")
    print()
    print(body)


if __name__ == "__main__":
    main()
