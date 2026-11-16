"""problem-packages 1차 결과 독립 검증. 레포 루트에서:

  python3 orchestration/work/phub-ledger-redesign/first-pass/problem-packages/verify.py

원본과 결과 파일을 읽기만 한다(어떤 파일도 쓰지 않음). 실패가 하나라도 있으면 종료 코드 1.
pp_common.py·build.py 를 쓰지 않고 표준 json 파서로 원본 구조를 다시 세운다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC = REPO / "orchestration/work/phub-recommend/bronze/phub-ledger/problem-packages.json"
SECTIONS = ["S00"] + [f"S{i:02d}" for i in range(1, 15)]
STATUSES = set("ABCIKPF")

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        if len(fails) <= 40:
            print("FAIL:", msg)


def J(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


raw = SRC.read_bytes()
h_start = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
byte_at = [0]
for ch in text:
    byte_at.append(byte_at[-1] + len(ch.encode("utf-8")))

# ---- 독립 파싱: 중복 키 감지 + 전체 Pointer 집합 ----
dups = []


def hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            dups.append(k)
        seen.add(k)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
ok(not dups, f"duplicate keys {dups}")
truth = {}  # pointer -> (type, value or child info)
order = []


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def walk(x, p):
    order.append(p)
    if isinstance(x, dict):
        truth[p] = ("object", list(x.keys()))
        for k, v in x.items():
            walk(v, p + "/" + esc(k))
    elif isinstance(x, list):
        truth[p] = ("array", len(x))
        for i, v in enumerate(x):
            walk(v, f"{p}/{i}")
    elif isinstance(x, str):
        truth[p] = ("string", x)
    elif isinstance(x, bool):
        truth[p] = ("boolean", x)
    elif x is None:
        truth[p] = ("null", None)
    elif isinstance(x, int):
        truth[p] = ("integer", x)
    else:
        truth[p] = ("number", x)


walk(data, "")
leaf_ptrs = {p for p, (t, _) in truth.items() if t not in ("object", "array")}
str_ptrs = {p for p, (t, _) in truth.items() if t == "string"}
empty_ptrs = {p for p, (t, v) in truth.items() if (t == "object" and not v) or (t == "array" and v == 0) or (t == "string" and v == "")}
all_keys = set()
for p, (t, v) in truth.items():
    if t == "object":
        all_keys |= set(v)


def section_of(p):
    parts = p.split("/")[1:]
    if len(parts) >= 2 and parts[0] == "problems" and parts[1].isdigit():
        return f"S{int(parts[1]) + 1:02d}"
    return "S00"


# ---- source-map ----
sm = J("source-map.json")
ok(sm["source"]["sha256"] == h_start, "source-map sha256 != current source")
ok(sm["source"]["bytes"] == len(raw) and sm["source"]["codepoints"] == len(text), "source size mismatch")
sm_ptrs = [n["pointer"] for n in sm["nodes"]]
ok(len(sm_ptrs) == len(set(sm_ptrs)), "source-map duplicate pointers")
ok(set(sm_ptrs) == set(truth), f"source-map pointer set mismatch: missing {len(set(truth)-set(sm_ptrs))} extra {len(set(sm_ptrs)-set(truth))}")
ok(sm_ptrs == order, "source-map node order != document order")
ok(set(sm["empty_values"]) == empty_ptrs, "empty_values mismatch")
ok(set(sm["field_names"]) == all_keys, "field_names set mismatch")
for k, fv in sm["field_names"].items():
    real = [p for p in order if p and p.rsplit("/", 1)[1] == esc(k) and truth[p.rsplit("/", 1)[0] or ""][0] == "object"]
    ok(fv["pointers"] == real, f"field_name {k} occurrence pointers mismatch")
for n in sm["nodes"]:
    p = n["pointer"]
    if p not in truth:
        continue
    t, v = truth[p]
    ok(n["type"] == t, f"type {p}")
    ok(n["section"] == section_of(p), f"section {p}")
    a, b = n["literal_cp_span"]
    ok(json.loads(text[a:b]) == (data if p == "" else json.loads(text[a:b])), f"literal parse {p}")
    ok(raw[n["literal_byte_span"][0]:n["literal_byte_span"][1]].decode("utf-8") == text[a:b], f"literal bytes {p}")
    ok(byte_at[a] == n["literal_byte_span"][0] and byte_at[b] == n["literal_byte_span"][1], f"literal byte map {p}")
    if t == "object":
        ok(n["child_keys"] == v and n["child_count"] == len(v), f"child keys {p}")
    elif t == "array":
        ok(n["child_count"] == v, f"child count {p}")
    else:
        ok(n["value"] == v, f"value {p}")
        ok(json.loads(text[a:b]) == v, f"literal value {p}")
        if t == "string":
            c0, c1 = n["content_cp_span"]
            ok(text[c0:c1] == v, f"content span {p}")
            ok(raw[n["content_byte_span"][0]:n["content_byte_span"][1]].decode("utf-8") == v, f"content bytes {p}")
    if "key_literal_cp_span" in n:
        ka, kb = n["key_literal_cp_span"]
        ok(json.loads(text[ka:kb]) == n["key"], f"key span {p}")

# ---- coverage ----
cv = J("coverage.json")
ok(cv["source_sha256"] == h_start, "coverage sha")
ok([s["id"] for s in cv["sections"]] == SECTIONS, "coverage section ids")
union = []
for s in cv["sections"]:
    union += s["owned_pointers"]
    ok(all(section_of(p) == s["id"] for p in s["owned_pointers"]), f"{s['id']} owns foreign pointer")
    ok(set(s["owned_leaf_pointers"]) == {p for p in s["owned_pointers"] if p in leaf_ptrs}, f"{s['id']} owned leaves")
    ok(set(s["owned_empty_values"]) == {p for p in s["owned_pointers"] if p in empty_ptrs}, f"{s['id']} owned empties")
    ok(s["direct_read"] == "done", f"{s['id']} not directly read")
    ok(s["machine_extracted"] == "done", f"{s['id']} not extracted")
    ok((HERE / s["review_file"]).exists(), f"{s['id']} review file missing")
    ok((HERE / s["manual_record"]).exists(), f"{s['id']} manual record missing")
    man = json.loads((HERE / s["manual_record"]).read_text(encoding="utf-8"))
    ok(man["section"] == s["id"] and man["read_status"] == "done", f"{s['id']} manual status")
    ok(len(man["observations"]) > 0, f"{s['id']} has no observations")
    for ref in s["shared_context_refs"]:
        ok(ref in truth and section_of(ref) == "S00", f"{s['id']} context ref {ref}")
ok(len(union) == len(set(union)), f"coverage duplicate ownership {len(union)-len(set(union))}")
ok(set(union) == set(truth), f"coverage union mismatch missing={len(set(truth)-set(union))} extra={len(set(union)-set(truth))}")
ok(cv["reading_log"]["remaining"] == [], "reading_log remaining not empty")

# ---- morphology ----
mo = J("morphology.json")
ok(mo["analyzer"]["kiwipiepy"] == "0.24.1" and mo["analyzer"]["model_type"] == "cong" and mo["analyzer"]["num_workers"] == 1, "analyzer config")
tv_ptrs = [t["pointer"] for t in mo["text_values"]]
ex_ptrs = [e["pointer"] for e in mo["excluded"]]
ok(len(tv_ptrs) == len(set(tv_ptrs)), "morph text_values duplicates")
ok(not (set(tv_ptrs) & set(ex_ptrs)), "morph applied and excluded overlap")
ok(set(tv_ptrs) | set(ex_ptrs) == leaf_ptrs, f"morph applied∪excluded != leaves (missing {len(leaf_ptrs-set(tv_ptrs)-set(ex_ptrs))})")
ok(set(tv_ptrs) <= str_ptrs, "morph applied to non-string")
for e in mo["excluded"]:
    ok(bool(e["reason"]), f"exclusion without reason {e['pointer']}")
    ok(any(re.search(r["pattern"], e["pointer"]) for r in mo["exclusion_rules"]) or truth[e["pointer"]][0] != "string",
       f"exclusion not matching rule {e['pointer']}")
ntok = 0
zero_width = []
for t in mo["text_values"]:
    v = truth[t["pointer"]][1]
    ok(t["value"] == v, f"morph value {t['pointer']}")
    ok(len(t["tokens"]) > 0, f"no tokens {t['pointer']}")
    base = t["file_cp_span"][0]
    ok(text[base:t["file_cp_span"][1]] == v, f"morph file span {t['pointer']}")
    last = 0
    for k in t["tokens"]:
        ntok += 1
        a, b = k["span"]
        # Kiwi 는 복원 형태소(예: '리쥬란'의 이/VCP)를 길이 0 구간으로 줄 수 있다 — 표면 '' 로 기록돼야 한다
        ok(0 <= a <= b <= len(v) and a >= last, f"token span order {t['pointer']} {k['i']}")
        if a == b:
            zero_width.append((t["pointer"], k["form"], k["tag"]))
            ok(k["surface"] == "" and not k["form_equals_surface"], f"zero-width token flag {t['pointer']}")
        last = a
        ok(v[a:b] == k["surface"], f"token surface {t['pointer']} {k['i']}")
        ok(k["form_equals_surface"] == (k["surface"] == k["form"]), f"form flag {t['pointer']}")
        ok(text[k["file_cp_span"][0]:k["file_cp_span"][1]] == k["surface"], f"token file span {t['pointer']}")
        ok(bool(k["tag"]) and k["lemma"] is not None, f"token tag/lemma {t['pointer']}")
ok(ntok == mo["applied_counts"]["tokens"], "token count")
ok({f["field_name"] for f in mo["field_names"]} == all_keys, "morph field names")
for ke in mo["known_errors"]:
    ok(ke["occurrence_count"] == len(ke["occurrences"]) > 0, f"{ke['id']} occurrences")
    for o in ke["occurrences"]:
        v = truth[o["pointer"]][1]
        ok(v[o["span"][0]:o["span"][1]] == o["trigger"], f"{ke['id']} span {o['pointer']}")
        ok(text[o["file_cp_span"][0]:o["file_cp_span"][1]] == o["trigger"], f"{ke['id']} file span")

# ---- expressions ----
ex = J("expressions.json")
ok(ex["counts"]["manual"] == len(ex["manual"]), "manual count")
ids = [e["id"] for e in ex["manual"]]
ok(len(ids) == len(set(ids)), "manual expr id duplicates")
keyset = [(e["pointer"], e["span"][0], e["span"][1], e["text"]) for e in ex["manual"]]
ok(len(keyset) == len(set(keyset)), f"manual expr duplicate (pointer,span) {len(keyset)-len(set(keyset))}")
for grp in ("manual", "regex_candidates", "clause_segments"):
    for e in ex[grp]:
        p = e["pointer"]
        ok(p in str_ptrs, f"{grp} pointer {p}")
        if p not in str_ptrs:
            continue
        v = truth[p][1]
        a, b = e["span"]
        ok(v[a:b] == e["text"], f"{grp} span {p} {e['text']!r}")
        ok(text[e["file_cp_span"][0]:e["file_cp_span"][1]] == e["text"], f"{grp} file span {p}")
        ok(e["section"] == section_of(p), f"{grp} section {p}")
        if "file_byte_span" in e:
            ok(raw[e["file_byte_span"][0]:e["file_byte_span"][1]].decode("utf-8") == e["text"], f"{grp} bytes {p}")
ok(set(e["pointer"] for e in ex["regex_candidates"]) <= set(tv_ptrs), "regex on non-applied value")
# 수동 표현은 15 구획 모두에 있어야 한다
ok({e["section"] for e in ex["manual"]} == set(SECTIONS), "manual expressions missing in some section")

# ---- cue review ----
cr = J("cue-review.json")
ok(cr["counts"]["unresolved"] == 0, f"cue unresolved {cr['counts']['unresolved']}")
cover = {}
for e in ex["manual"]:
    cover.setdefault(e["pointer"], []).append(e["span"])
cue_regex = [r for r in ex["regex_candidates"] if r["group"] == "cue"]
ok(len(cue_regex) == len(cr["rows"]), "cue rows != cue regex candidates")
for r in cr["rows"]:
    cov = any(a <= r["span"][0] and r["span"][1] <= b for a, b in cover.get(r["pointer"], []))
    ok(cov == r["covered_by_manual"], f"cue covered flag {r['pointer']}")
    ok(cov or bool(r["decision"] and r["reason"]), f"cue uncovered without decision {r['pointer']} {r['text']}")
dec = json.loads((HERE / "manual" / "cue-decisions.json").read_text(encoding="utf-8"))["decisions"]
rowkeys = {(r["pointer"], r["text"], r["span"][0]) for r in cr["rows"] if not r["covered_by_manual"]}
ok(all((d["pointer"], d["text"], d["span"][0]) in rowkeys for d in dec), "cue decision for nonexistent uncovered hit")

# ---- manual records: 관찰 상태·Pointer ----
issue_ids = set()
for s in SECTIONS:
    man = json.loads((HERE / "manual" / f"{s}.json").read_text(encoding="utf-8"))
    for o in man["observations"]:
        ok(o["status"] in STATUSES, f"{o['id']} status")
    for it in man["issues"]:
        ok(it["status"] in STATUSES - {"P"}, f"{it['id']} issue status")
        ok(it["id"].startswith(it["status"] + "-"), f"{it['id']} prefix/status mismatch")
        issue_ids.add(it["id"])
for k in mo["known_errors"]:
    issue_ids.add(k["id"])
ok(not any(i.startswith("C-") for i in issue_ids), "C issue present without user-decision record")

# ---- review markdown ----
rv = (HERE / "review.md").read_text(encoding="utf-8")
for s in cv["sections"]:
    ok(f"]({s['review_file']})" in rv, f"review.md lacks link {s['review_file']}")
    part = (HERE / s["review_file"]).read_text(encoding="utf-8")
    ok("## 원문 값" in part and "## 잠정 관찰" in part, f"{s['id']} part sections")
    for p in s["owned_pointers"]:
        t, v = truth[p]
        row = next((ln for ln in part.splitlines() if ln.startswith("| ") and f"| `{p or '(루트)'}` |" in ln), None)
        ok(row is not None, f"{s['id']} part missing pointer {p}")
        if row and t == "string":
            ok(f"| {v.replace('|', chr(92) + '|')} |" in row, f"{s['id']} part value mismatch {p}")
        if row and p:
            col = p.rsplit("/", 1)[1]
            colname = col if not col.isdigit() else f"({p.rsplit('/', 2)[1]} 원소)"
            ok(f"| `{colname}` |" in row, f"{s['id']} part column name {p}")
iss = (HERE / "issues.md").read_text(encoding="utf-8")
for i in issue_ids:
    ok(f"### {i}" in iss, f"issues.md missing {i}")
for f in ["review.md", "source-map.json", "morphology.json", "expressions.json", "issues.md", "validation.md",
          "coverage.json", "progress.md", "build.py", "verify.py"]:
    ok((HERE / f).exists(), f"missing output {f}")

h_end = hashlib.sha256(SRC.read_bytes()).hexdigest()
ok(h_start == h_end, "source changed during verify")
print(f"source sha256 start={h_start} end={h_end}")
print(f"nodes={len(truth)} leaves={len(leaf_ptrs)} strings={len(str_ptrs)} empty={len(empty_ptrs)} fields={len(all_keys)}")
print(f"sections={len(cv['sections'])} owned_union={len(set(union))} text_values={len(tv_ptrs)} excluded={len(ex_ptrs)} tokens={ntok}")
print(f"manual={len(ex['manual'])} regex={len(ex['regex_candidates'])} clauses={len(ex['clause_segments'])} cue_rows={len(cr['rows'])} issues={len(issue_ids)}")
print(f"zero_width_tokens={len(zero_width)} forms={sorted({(f, g) for _, f, g in zero_width})}")
print(f"checks={checks} fails={len(fails)}")
sys.exit(1 if fails else 0)
