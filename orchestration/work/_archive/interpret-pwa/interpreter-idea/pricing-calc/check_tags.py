"""보고서 근거 표기 검사 — 숫자가 있는 줄마다 근거 태그(실측·공식·사용자 지정·계산·추정·비교용·정할 것)가 있어야 한다.
표의 행은 같은 행의 「근거」 칸이 태그를 가지면 통과. 제목(#) · 이미지 줄 · §참조 · `코드` · URL · 날짜 속 숫자는 셈에서 뺀다."""
import re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[4] / "reference/2026-11-12-interpreter-idea/pricing-design.md"
# 근거 4종 + 추정 · 비교용 · 정할 것만. 〔정의〕 · 〔코드〕 같은 보조 태그는 근거로 치지 않는다(검수 F1).
TAGS = ("〔실측", "〔공식", "〔사용자 지정", "〔계산", "〔추정", "〔비교용", "〔정할 것")
AUX = ("〔정의", "〔코드")
bad, n_lines = [], 0
lines = R.read_text().splitlines()
for i, line in enumerate(lines, 1):
    is_header = line.startswith("|") and i < len(lines) and re.fullmatch(r"\|[-:| ]+\|", lines[i])
    if line.startswith("#") or line.startswith("![") or is_header:
        continue
    s = re.sub(r"`[^`]*`", "", line)
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"§\d+(\.\d+)?", "", s)
    s = re.sub(r"\d{4}-\d{2}-\d{2}", "", s)
    s = re.sub(r"\|[-:| ]+\|$", "", s)
    if not re.search(r"\d", s):
        continue
    n_lines += 1
    if not any(t in line for t in TAGS):
        bad.append((i, line))
aux = [(i, l) for i, l in enumerate(lines, 1) if any(t in l for t in AUX)]
print(f"숫자 있는 줄 {n_lines} · 근거 없는 줄 {len(bad)} · 보조 태그(〔정의〕·〔코드〕) 줄 {len(aux)}")
for i, l in aux:
    print("AUX", i, l)
bad += aux
for i, l in bad:
    print(i, l)
sys.exit(1 if bad else 0)
