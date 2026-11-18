"""앱 장부(turns.jsonl) → 채점이 읽는 칸만 남긴 runs/<이름>-rows.jsonl. usage: slim.py <turns.jsonl> [이름=now]"""
import json, sys, os
from paths import RUN
src = sys.argv[1]; name = sys.argv[2] if len(sys.argv) > 2 else "now"
CONS = ("after", "queries", "ask", "ask_why", "retract", "turn_kind", "diff", "jev_requests", "close", "viewing",
        "understand", "site_filter", "site_index", "follow_target")  # 0.4(SPEC-008 E8-pre) 넷 더함
n = 0
with open(os.path.join(RUN, f"{name}-rows.jsonl"), "w", encoding="utf-8") as f:
    for l in open(src, encoding="utf-8"):
        r = json.loads(l)
        if r.get("phase") != "end": continue
        tr = r.get("trace") or {}; ep = tr.get("entry_pick") or {}; c = r.get("consult") or {}
        f.write(json.dumps({"conv_id": r["conv_id"], "turn": r["turn"], "phase": "end", "question": r.get("question"), "error": r.get("error"),
            "targets": r.get("targets"), "kinds": r.get("kinds"), "end_state": r.get("end_state"), "timing": r.get("timing"),
            "list": r.get("list"), "sites": r.get("sites"),
            "trace": {"front": {"targets": (tr.get("front") or {}).get("targets")}, "entry": {"resolve_candidates": (tr.get("entry") or {}).get("resolve_candidates")},
                      "entry_pick": ({k: ep.get(k) for k in ("result", "requests", "per_candidate", "skipped")} if ep else None)},
            "consult": {k: c.get(k) for k in CONS} if c else None,
            "material": {"new_lines": [{"n": x.get("n"), "gid": x.get("gid")} for x in (r.get("material") or {}).get("new_lines") or []
                                       if x.get("gid")], "seen_lines": (r.get("material") or {}).get("seen_lines") or []},
            "depth": tr.get("depth"), "answer": (r.get("answer") or "")[:300], "tokens_over": (r.get("error") or {}).get("kind") == "fold" or r.get("reason") == "FT5"},
            ensure_ascii=False) + "\n"); n += 1
print("rows", n)
