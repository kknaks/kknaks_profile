"""combo-recipes 1차 산출물 독립 검증. 표준 라이브러리만 쓰고 build.py 코드를 가져오지 않는다.
아무 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.

레포 루트에서: python3 orchestration/work/phub-ledger-redesign/first-pass/combo-recipes/verify.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
SRC = REPO / "orchestration/work/phub-recommend/bronze/phub-ledger/combo-recipes.json"
EXPECTED_SHA = "1bb7c309e8ec72768ae9c5db94e1911188be240f4c7d770d54244008aeab0c94"

FAIL = []
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    if not ok:
        FAIL.append(f"{name}: {detail}")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


h0 = sha(SRC)
check("source sha256 at start", h0 == EXPECTED_SHA, h0)
RAW = SRC.read_bytes()
TEXT = RAW.decode("utf-8")

# 중복 키 감지 + 독립 경로 열거
dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return dict(pairs)


DOC = json.loads(TEXT, object_pairs_hook=hook)
check("no duplicate keys (object_pairs_hook)", not dups, str(dups))


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def walk(o, p=""):
    yield p, o
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, p + "/" + esc(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{p}/{i}")


ALL = dict(walk(DOC))


def is_leaf(v):
    return not isinstance(v, (dict, list)) or len(v) == 0


LEAVES = {p for p, v in ALL.items() if is_leaf(v)}


def jtype(v):
    if isinstance(v, bool):
        return "boolean"
    if v is None:
        return "null"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    return "object" if isinstance(v, dict) else "array"


def load(name):
    p = OUT / name
    check(f"file exists {name}", p.exists())
    return json.loads(p.read_text()) if p.exists() and name.endswith(".json") else (p.read_text() if p.exists() else "")


SM = load("source-map.json")
MO = load("morphology.json")
EX = load("expressions.json")
CO = load("coverage.json")
REVIEW = load("review.md")
for f in ["issues.md", "validation.md", "build.py", "manual-expressions.json", "manual-observations.json",
          "segmentation-review.json"]:
    load(f)

for name, obj in [("source-map", SM["source"]), ("morphology", MO["source"]), ("expressions", EX["source"]),
                  ("coverage", CO["source"])]:
    check(f"{name} records source sha", obj.get("sha256") == h0)

# ---- source-map 양방향
nodes = SM["nodes"]
nptrs = [n["pointer"] for n in nodes]
check("source-map pointers unique", len(nptrs) == len(set(nptrs)))
check("source-map ⊇ all paths", not (set(ALL) - set(nptrs)), str(sorted(set(ALL) - set(nptrs))[:5]))
check("source-map ⊆ all paths", not (set(nptrs) - set(ALL)), str(sorted(set(nptrs) - set(ALL))[:5]))
check("source-map node count", len(nodes) == len(ALL), f"{len(nodes)} vs {len(ALL)}")
bad = []
BYTE = [0]
for ch in TEXT:
    BYTE.append(BYTE[-1] + len(ch.encode("utf-8")))
for n in nodes:
    v = ALL.get(n["pointer"])
    if jtype(v) != n["type"]:
        bad.append(("type", n["pointer"]))
        continue
    s, e = n["span"]
    if json.loads(TEXT[s:e]) != v:
        bad.append(("span", n["pointer"]))
    bs, be = n["byte_span"]
    if RAW[bs:be].decode("utf-8") != TEXT[s:e] or [BYTE[s], BYTE[e]] != [bs, be]:
        bad.append(("byte", n["pointer"]))
    if n["type"] not in ("object", "array"):
        if n["value"] != v:
            bad.append(("value", n["pointer"]))
    if n["type"] == "string" and n["value_span"] is not None:
        a, b = n["value_span"]
        if TEXT[a:b] != v:
            bad.append(("value_span", n["pointer"]))
    if n["leaf"] != is_leaf(v):
        bad.append(("leaf", n["pointer"]))
check("node type/value/span/byte_span reproduce", not bad, str(bad[:5]))
# 키
kocc = SM["key_occurrences"]
nkeys = sum(len(v) for v in ALL.values() if isinstance(v, dict))
check("key occurrence count == keys in document", len(kocc) == nkeys, f"{len(kocc)} vs {nkeys}")
kbad = [k for k in kocc if json.loads(TEXT[k["span"][0]:k["span"][1]]) != k["key"] or k["pointer"] not in ALL]
check("key spans reproduce key literal", not kbad, str(kbad[:3]))

# ---- coverage 양방향
segs = CO["segments"]
owned = [p for s in segs for p in s["owned_pointers"]]
check("coverage: no pointer owned twice", len(owned) == len(set(owned)),
      str([p for p in set(owned) if owned.count(p) > 1][:5]))
check("coverage: all paths owned", not (set(ALL) - set(owned)), str(sorted(set(ALL) - set(owned))[:5]))
check("coverage: no unknown owned paths", not (set(owned) - set(ALL)), str(sorted(set(owned) - set(ALL))[:5]))
owned_leaves = [p for s in segs for p in s["owned_leaf_pointers"]]
check("coverage: leaf union == all leaves", set(owned_leaves) == LEAVES and len(owned_leaves) == len(LEAVES))
for s in segs:
    check(f"coverage {s['id']} leaves ⊆ owned", set(s["owned_leaf_pointers"]) <= set(s["owned_pointers"]))
    check(f"coverage {s['id']} direct_read done", s["direct_read"] == "done" and s["machine_extraction"] == "done")
    check(f"coverage {s['id']} review file exists", (OUT / s["review_file"]).exists())
    anchor = s["review_anchor"].lstrip("#")
    check(f"coverage {s['id']} review anchor present", f'<a id="{anchor}"></a>' in REVIEW)
    for c in s["context_refs"]:
        check(f"coverage {s['id']} context ref valid {c}", c in ALL)
    # 구획 소유의 일관: S0 = 비-recipes 원소, Sk = /recipes/k-1 아래
    for p in s["owned_pointers"]:
        m = re.match(r"^/recipes/(\d+)(/|$)", p)
        want = f"S{int(m.group(1)) + 1}" if m else "S0"
        if want != s["id"]:
            check(f"coverage {s['id']} owns foreign pointer", False, p)
check("coverage: no remaining segments", CO["remaining_segments"] == [])

# ---- review 값 표 대조
row_rx = re.compile(r"^\| `([^`]*)` \| (.+?) \| (\S+) \| (.*) \|$")
TYPE_KO = {"string": "문자열", "integer": "정수", "number": "실수", "boolean": "불리언", "null": "null",
           "object": "객체", "array": "배열"}
seen_rows = {}
in_values = False
for line in REVIEW.splitlines():
    if line.startswith("#"):
        in_values = line.strip() == "### 원문 값"
        continue
    if not in_values:
        continue
    m = row_rx.match(line)
    if not m:
        continue
    ptr = "" if m.group(1) == "(root)" else m.group(1)
    if ptr not in ALL:
        continue
    seen_rows.setdefault(ptr, []).append((m.group(2), m.group(3), m.group(4)))
rbad = []
for p in ALL:
    rows = seen_rows.get(p, [])
    if len(rows) != 1:
        rbad.append(("rows", p, len(rows)))
        continue
    col, typ, val = rows[0]
    v = ALL[p]
    last = p.rsplit("/", 1)[-1] if p else ""
    if p == "":
        want_col = "(root)"
    elif last.isdigit() and isinstance(ALL[p.rsplit("/", 1)[0]], list):
        want_col = f"{p.rsplit('/', 2)[-2]}[{last}]"
    else:
        want_col = last.replace("~1", "/").replace("~0", "~")
    if col != want_col:
        rbad.append(("col", p, col))
    if typ != TYPE_KO[jtype(v)]:
        rbad.append(("type", p, typ))
    if is_leaf(v):
        shown = val.replace("\\|", "|")
        want = v if isinstance(v, str) else json.dumps(v)
        if shown != want:
            rbad.append(("value", p, shown))
check("review: every path has exactly one value row with original column name, type, exact value", not rbad, str(rbad[:5]))

# ---- 형태소 적용/제외
strings = {p for p, v in ALL.items() if isinstance(v, str)}
applied = [v["pointer"] for v in MO["values"]]
excluded = [x["pointer"] for x in MO["excluded_values"]]
check("morph: applied ∩ excluded = ∅", not (set(applied) & set(excluded)))
check("morph: applied ∪ excluded = all strings", set(applied) | set(excluded) == strings and
      len(applied) + len(excluded) == len(strings))
check("morph: every exclusion has reason", all(x["reason"] for x in MO["excluded_values"]))
check("morph: excluded values equal source", all(ALL[x["pointer"]] == x["value"] for x in MO["excluded_values"]))
tbad = []
ntok = 0
for v in MO["values"]:
    t = v["text"]
    if t != ALL[v["pointer"]]:
        tbad.append(("text", v["pointer"]))
    base = v["file_span_of_text"][0]
    if TEXT[base:base + len(t)] != t:
        tbad.append(("file_span_of_text", v["pointer"]))
    covered = [False] * len(t)
    for tk in v["tokens"]:
        ntok += 1
        s, e = tk["start"], tk["end"]
        if not (0 <= s < e <= len(t)) or t[s:e] != tk["surface"]:
            tbad.append(("tok_span", v["pointer"], s))
        if TEXT[tk["file_span"][0]:tk["file_span"][1]] != tk["surface"]:
            tbad.append(("tok_file", v["pointer"], s))
        if (tk["form"] == tk["surface"]) != tk["form_equals_surface"]:
            tbad.append(("fes", v["pointer"], s))
        for i in range(s, e):
            covered[i] = True
    miss = [i for i, c in enumerate(t) if not c.isspace() and not covered[i]]
    if miss:
        tbad.append(("uncovered", v["pointer"], miss[:3]))
check(f"morph: tokens reproduce source & cover all non-space chars ({ntok} tokens)", not tbad, str(tbad[:5]))
keys_all = {k["key"] for k in kocc}
check("morph: every field name analysed", {f["field"] for f in MO["field_names"]} == keys_all)
an = MO["analyzer"]
check("morph: analyzer recorded (cong, 1 thread, version)", an["model_type"] == "cong" and an["num_workers"] == 1
      and an["kiwipiepy"] == "0.24.1")
SEGR = json.loads((OUT / "segmentation-review.json").read_text())
fbad = []
vals = {v["pointer"]: v for v in MO["values"]}
for f in MO["segmentation_flags"]:
    v = vals[f["pointer"]]
    s, e = f["span"]
    if v["text"][s:e] != f["surface"]:
        fbad.append(("surface", f["rule"], f["pointer"]))
    toks = [v["tokens"][i] for i in f["token_indices"]]
    if [f"{t['form']}/{t['tag']}" for t in toks] != f["raw_tokens"]:
        fbad.append(("tokens", f["rule"], f["pointer"]))
for r in SEGR["rules"]:
    c = sum(1 for f in MO["segmentation_flags"] if f["rule"] == r["id"])
    if c != r["expected_count"] or c == 0:
        fbad.append(("count", r["id"], c))
check(f"morph: segmentation flags reproduce ({len(MO['segmentation_flags'])} occurrences, {len(SEGR['rules'])} rules)",
      not fbad, str(fbad[:5]))

# ---- 표현
exprs = EX["expressions"]
ebad = []
ids = [x["id"] for x in exprs]
if len(ids) != len(set(ids)):
    ebad.append("dup id")
keyset = set()
for x in exprs:
    v = ALL.get(x["pointer"])
    if not isinstance(v, str):
        ebad.append(("ptr", x["id"]))
        continue
    s, e = x["span"]
    if not (0 <= s < e <= len(v)) or v[s:e] != x["text"]:
        ebad.append(("span", x["id"]))
    if TEXT[x["file_span"][0]:x["file_span"][1]] != x["text"]:
        ebad.append(("file_span", x["id"]))
    k = (x["pointer"], s, e, x["category"], x["method"])
    if k in keyset:
        ebad.append(("exact dup", x["id"]))
    keyset.add(k)
check(f"expressions: spans reproduce, ids unique, no exact duplicates ({len(exprs)})", not ebad, str(ebad[:5]))
whole = {x["pointer"] for x in exprs if x["category"] == "segment.value"}
check("expressions: every applied value has segment.value", whole == set(applied))
MAN = json.loads((OUT / "manual-expressions.json").read_text())
man_ex = [x for x in exprs if x["method"] == "manual.direct_read"]
mbad = []
for ptr, text, occ, cats, note in MAN["entries"]:
    hits = [x for x in man_ex if x["pointer"] == ptr and x["text"] == text and x.get("occurrence") == occ]
    if len(hits) != 1:
        mbad.append((ptr, text))
check(f"expressions: manual entries each present once ({len(MAN['entries'])})",
      not mbad and len(man_ex) == len(MAN["entries"]), str(mbad[:3]))
manual_segments = {x["segment"] for x in man_ex}
check("expressions: every segment has manual expressions", manual_segments == {s["id"] for s in segs})
fps = [x for x in exprs if x.get("review", {}).get("false_positive")]
check("expressions: false-positive marks have reasons", all(x["review"]["reason"] for x in fps) and len(fps) == 4,
      str(len(fps)))

# ---- 관찰 포인터
OBS = json.loads((OUT / "manual-observations.json").read_text())
obad = [(o["id"], p) for s in OBS["segments"].values() for o in s["observations"] for p in o["pointers"] if p not in ALL]
check("observations: pointers valid", not obad, str(obad[:3]))
check("observations: statuses in {P,F,B,I,K}", all(o["status"] in "PFBIK" for s in OBS["segments"].values()
                                                   for o in s["observations"]))
for s in OBS["segments"].values():
    for o in s["observations"]:
        if f"| {o['id']} |" not in REVIEW:
            check(f"observation {o['id']} in review", False)

h1 = sha(SRC)
check("source sha256 at end", h1 == h0, h1)

for name, ok, detail in RESULTS:
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if not ok and detail else ""))
print(f"checks={len(RESULTS)} failure_count={len(FAIL)} paths={len(ALL)} leaves={len(LEAVES)} strings={len(strings)}")
sys.exit(1 if FAIL else 0)
