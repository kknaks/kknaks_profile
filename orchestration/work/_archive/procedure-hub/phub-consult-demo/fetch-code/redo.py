"""JSON 깨짐 턴만 다시 불러(같은 앱 프롬프트 · 고친 `verify.parse`) understand_<모음>.jsonl 의 그 줄을 바꾼다. 원래 줄은 `redo_<모음>.jsonl` 에 남긴다."""
import asyncio, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay54 as R
from clinic_chat.consult import verify as vf

async def main():
    md = R.common.md_sets()
    sets = {"sample": R.M.load_turns(md), "outside": [t for t in R.run4.outside_turns(md) if R.era(t["row"]) != "jev"]}
    for name, ts in sets.items():
        p = R.OUT / f"understand_{name}.jsonl"
        rows = [json.loads(x) for x in p.read_text().splitlines()]
        bad = [i for i, x in enumerate(rows) if x["json"] is None]
        if not bad:
            continue
        with open(R.OUT / f"redo_{name}.jsonl", "a") as f:
            for i in bad:
                f.write(json.dumps(rows[i], ensure_ascii=False) + "\n")
        new = await R.call_all([ts[i] for i in bad], 2)
        for i, x in zip(bad, new):
            x["redo"] = True
            rows[i] = x
        p.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
asyncio.run(main())
