#!/usr/bin/env python3
"""resume.md → A4 PDF (kknaks.dev 인쇄 테마).

사용:
    python3 build_pdf.py <resume.md> [output.pdf]

- frontmatter(전략 메모)는 PDF 에 넣지 않는다 — 채용담당자용 문서다.
- md → HTML 은 pandoc(gfm), HTML → PDF 는 playwright chromium 인쇄.
- 테마는 claude_design/kknaks_profile_v2.1.0/print/print.css 이식 —
  라이트 시트 · Inter + JetBrains Mono · 터미널 그린 액센트 ·
  mono 섹션 헤더(01 Label ────). 연락처 라벨은 이메일/깃허브/블로그.
- resume-template.md 구조를 전제한다:
  h1(이름) 직후 p 가 「직함\\n지역 · 이메일 · [github] · [사이트]」 헤더 블록,
  경력 h3 는 「… · YYYY.MM – …」 로 끝나면 기간을 우측 정렬,
  「→ 링크 · 링크」 문단은 링크 행으로 스타일링.
- 의존: pandoc, playwright(파이썬 패키지 + chromium).
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg-0:#ffffff; --bg-1:#fafaf8; --bg-2:#f3f3f0;
  --line-1:#e6e6e1; --line-2:#d2d2cc; --line-3:#b9b9b3;
  --fg-0:#0e0e0c; --fg-1:#2a2a26; --fg-2:#555550; --fg-3:#8a8a85;
  --accent:oklch(0.52 0.16 152);
  --accent-soft:oklch(0.94 0.06 152);
  --accent-line:oklch(0.78 0.10 152);
  --font-sans:'Inter','Apple SD Gothic Neo',-apple-system,'Segoe UI',sans-serif;
  --font-mono:'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace;
}
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; }
body {
  margin: 0; padding: 0;
  font-family: var(--font-sans);
  font-feature-settings: 'ss01','cv11','tnum';
  color: var(--fg-0); background: var(--bg-0);
  font-size: 11.5px; line-height: 1.65;
  counter-reset: sec;
}
body.cover-letter { font-size: 12.5px; line-height: 1.85; }
body.cover-letter h2 { font-size: 10.5px; margin: 24px 0 12px; }
body.cover-letter p { margin: 8px 0; }
body.cover-letter header.hd { margin-bottom: 20px; }
.mono { font-family: var(--font-mono); }

/* ── header ─────────────────────────────── */
header.hd {
  display: flex; align-items: flex-start; gap: 18px;
  padding-bottom: 18px; border-bottom: 1px solid var(--line-2);
  margin-bottom: 16px;
}
.hd-main { flex: 1; min-width: 0; }
.hd-caps {
  font-family: var(--font-mono); font-size: 10px; color: var(--fg-3);
  text-transform: uppercase; letter-spacing: 0.18em;
}
h1 {
  font-size: 32px; line-height: 1.05; margin: 4px 0 0; font-weight: 700;
  letter-spacing: -0.025em; display: flex; align-items: baseline; gap: 10px;
}
h1 .handle { font-family: var(--font-mono); font-size: 14px; color: var(--fg-3); font-weight: 400; }
.hd-role { font-family: var(--font-mono); font-size: 11px; color: var(--fg-2); margin-top: 5px; }
.hd-contact {
  text-align: right; font-family: var(--font-mono); font-size: 10px;
  line-height: 1.8; color: var(--fg-1); flex-shrink: 0;
}
.hd-contact span { color: var(--fg-3); margin-right: 4px; }

/* ── sections ───────────────────────────── */
h2 {
  display: flex; align-items: center; gap: 8px;
  font-family: var(--font-mono); font-size: 10px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.16em; color: var(--fg-0);
  margin: 20px 0 10px;
  page-break-after: avoid;
}
h2::before {
  counter-increment: sec;
  content: '0' counter(sec);
  color: var(--accent); font-weight: 400;
}
h2::after { content: ''; flex: 1; height: 1px; background: var(--line-1); }

h3 {
  font-size: 13px; font-weight: 600; letter-spacing: -0.01em;
  margin: 13px 0 4px; display: flex; align-items: baseline; gap: 8px;
  page-break-after: avoid;
}
h3 .period {
  margin-left: auto; font-family: var(--font-mono);
  font-size: 10px; color: var(--fg-3); font-weight: 400; white-space: nowrap;
}
h3 + p { margin-top: 2px; }

p { margin: 5px 0; color: var(--fg-1); }
ul { margin: 5px 0; padding-left: 15px; }
li { margin: 3.5px 0; font-size: 11px; line-height: 1.6; color: var(--fg-1); page-break-inside: avoid; }
strong { color: var(--fg-0); font-weight: 600; }
a { color: var(--accent); text-decoration: none; }

p.linkline {
  font-family: var(--font-mono); font-size: 10px; color: var(--fg-3);
  margin: 4px 0 10px;
}

/* ── skills table ───────────────────────── */
table { border-collapse: collapse; width: 100%; margin: 6px 0; page-break-inside: avoid; }
th, td { border: 1px solid var(--line-1); padding: 5px 10px; text-align: left; font-size: 10.5px; }
th {
  background: var(--bg-1); font-family: var(--font-mono); font-weight: 500;
  font-size: 9.5px; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--fg-3); white-space: nowrap;
}
td:first-child { font-family: var(--font-mono); font-size: 10px; color: var(--fg-2); white-space: nowrap; }

/* ── footer ─────────────────────────────── */
footer.ft {
  border-top: 1px solid var(--line-1); margin-top: 18px; padding-top: 9px;
  display: flex; justify-content: space-between;
  font-family: var(--font-mono); font-size: 9px; color: var(--fg-3);
}
"""

HTML_SHELL = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{css}</style></head><body class="{body_class}">{body}
<footer class="ft"><span>generated from {source_name} · kknaks jd-analysis kit</span><span>kknaks.dev</span></footer>
</body></html>"""


def strip_frontmatter(md: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", md, count=1, flags=re.S)


LABEL_KO = {"email": "이메일", "github": "깃허브", "blog": "블로그", "site": "블로그"}


def themed_header(html: str, document_label: str = "resume") -> str:
    """h1 + 직후 p 를 테마 헤더로 재구성.

    p 형식: 직함 줄 / 지역 줄 / `email : …`·`github : …`·`blog : …` 줄들.
    줄 경계는 <br> 또는 개행. 라벨 줄은 우측 연락처 블록으로, 라벨 없는 줄은
    직함 뒤에 ` · ` 로 잇는다.
    """
    m = re.search(r"<h1[^>]*>(.*?)</h1>\s*<p>(.*?)</p>", html, re.S)
    if not m:
        return html
    name = m.group(1).strip()
    content = m.group(2)

    contact_re = re.compile(
        r"(email|github|blog|site)\s*:\s*(<a\b[^>]*>.*?</a>|[^\s<]+)", re.I | re.S
    )
    rows = []
    first_label_at = None
    for cm in contact_re.finditer(content):
        if first_label_at is None:
            first_label_at = cm.start()
        value = re.sub(r">(https?://)", ">", cm.group(2)).strip()
        rows.append(f"<div><span>{LABEL_KO[cm.group(1).lower()]}</span>{value}</div>")

    role_src = content[:first_label_at] if first_label_at is not None else content
    role_parts = [
        ln.strip().strip("\\").strip(" ·")
        for ln in re.split(r"<br\s*/?>|\n", role_src)
    ]
    role_parts = [ln for ln in role_parts if ln]

    role_line = " · ".join(role_parts)
    header = (
        '<header class="hd">'
        '<div class="hd-main">'
        f'<div class="hd-caps">{document_label} · 한국어</div>'
        f"<h1>{name} <span class=\"handle\">· kknaks</span></h1>"
        f'<div class="hd-role">{role_line}</div>'
        "</div>"
        f'<div class="hd-contact">{"".join(rows)}</div>'
        "</header>"
    )
    return html[: m.start()] + header + html[m.end():]


def split_h3_period(html: str) -> str:
    """h3 가 「… · YYYY.MM – …」 로 끝나면 기간을 우측 정렬 span 으로."""
    def repl(m: re.Match) -> str:
        title, period = m.group(1), m.group(2)
        return f'<h3><span>{title}</span><span class="period">{period}</span></h3>'

    return re.sub(
        r"<h3[^>]*>(.*?) · (\d{4}\.\d{2}[^<]*)</h3>", repl, html, flags=re.S
    )


def mark_linklines(html: str) -> str:
    return html.replace("<p>→", '<p class="linkline">→')


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")

    md = strip_frontmatter(src.read_text(encoding="utf-8"))
    body = subprocess.run(
        ["pandoc", "--from", "gfm", "--to", "html", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout
    is_cover_letter = src.stem == "cover-letter"
    label = "cover letter" if is_cover_letter else "resume"
    body = mark_linklines(split_h3_period(themed_header(body, label)))
    html = HTML_SHELL.format(
        css=CSS,
        body=body,
        body_class="cover-letter" if is_cover_letter else "resume",
        source_name=src.name,
    )

    from playwright.sync_api import sync_playwright

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = f.name

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(f"file://{html_path}", wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(out), format="A4", print_background=True,
                margin={"top": "14mm", "right": "15mm", "bottom": "14mm", "left": "15mm"},
            )
        finally:
            browser.close()

    print(f"saved: {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
