"""장부 tokens 의 캐시 갈래(지금 시대) — 앞 대화가 cache_read 로 읽히나. 실행: python3 cache_split.py"""
import json
from pathlib import Path
d = json.loads((Path(__file__).resolve().parent / "out/decompose.json").read_text())
cur = [t for t in d["turns"] if not t["era"].startswith("before") and t["sent"]]
s = {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0}
for t in cur:
    for k in s:
        s[k] += int((t["tokens_parts"] or {}).get(k) or 0)
tot = s["input_tokens"] + s["cache_creation_input_tokens"] + s["cache_read_input_tokens"]
hist = sum(t["history_tok"] for t in cur)
print(json.dumps({**s, "input_total": tot, "cache_read_share": round(100 * s["cache_read_input_tokens"] / tot, 1),
                  "cache_creation_share": round(100 * s["cache_creation_input_tokens"] / tot, 1),
                  "history_tok": hist, "turns": len(cur),
                  "weighted_input_equiv(1.25cc+0.1cr+1in)": round(1.25 * s["cache_creation_input_tokens"] + 0.1 * s["cache_read_input_tokens"] + s["input_tokens"])}, ensure_ascii=False))
