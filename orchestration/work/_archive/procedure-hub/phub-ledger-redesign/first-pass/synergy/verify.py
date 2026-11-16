#!/usr/bin/env python3
"""synergy.json 1차 조사 결과 독립 검증. 표준 라이브러리만 쓴다. 어떤 파일도 쓰지 않는다.

실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/synergy/verify.py
실패가 하나라도 있으면 종료 코드 1.
"""
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
SRC = ROOT / "orchestration/work/phub-recommend/bronze/phub-ledger/synergy.json"
EXPECTED_SHA = "2c0fb244f6dc7f8521be355e83586bc7b6446979c041a51c77046bae1c3c653f"


def load(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def walk(obj, ptr=""):
    """독립 순회: (pointer, type, value_or_None, children/len)."""
    if isinstance(obj, dict):
        yield ptr, "object", None, list(obj.keys())
        for k, v in obj.items():
            yield from walk(v, ptr + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif isinstance(obj, list):
        yield ptr, "array", None, len(obj)
        for i, v in enumerate(obj):
            yield from walk(v, f"{ptr}/{i}")
    else:
        t = "string" if isinstance(obj, str) else "boolean" if isinstance(obj, bool) else "null" if obj is None else "number"
        yield ptr, t, obj, None


def resolve(obj, ptr):
    if ptr == "":
        return obj
    cur = obj
    for part in ptr.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def check_all(raw, text, data, sm, mo, ex, lo, fail):
    # ---------- 1. source identity
    h = hashlib.sha256(raw).hexdigest()
    if h != EXPECTED_SHA:
        fail("source sha256 != expected", h)
    for name, o in (("source-map", sm), ("morphology", mo), ("expressions", ex), ("link-observations", lo)):
        s = o["source"]
        if s["sha256_start"] != EXPECTED_SHA or s["sha256_end"] != EXPECTED_SHA:
            fail(f"{name} sha recorded mismatch")
        if s["size_bytes"] != len(raw) or s["code_points"] != len(text):
            fail(f"{name} size mismatch")

    # ---------- 2. duplicate keys (independent)
    dups = []

    def hook(pairs):
        c = Counter(k for k, _ in pairs)
        dups.extend(k for k, n in c.items() if n > 1)
        return dict(pairs)
    json.loads(text, object_pairs_hook=hook)
    if dups or sm["duplicate_keys"]:
        fail("duplicate keys present", dups, sm["duplicate_keys"])

    # ---------- 3. structure bijection
    ref = {p: (t, v, c) for p, t, v, c in walk(data)}
    nodes = sm["nodes"]
    np = Counter(n["pointer"] for n in nodes)
    if any(c > 1 for c in np.values()):
        fail("duplicate node pointers", [p for p, c in np.items() if c > 1][:5])
    if set(np) != set(ref):
        fail("node pointer set mismatch", sorted(set(ref) - set(np))[:5], sorted(set(np) - set(ref))[:5])
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + len(ch.encode("utf-8")))
    for n in nodes:
        p = n["pointer"]
        if p not in ref:
            continue
        t, v, c = ref[p]
        if n["type"] != t:
            fail("type mismatch", p)
        s, e = n["span"]
        if json.loads(text[s:e]) != resolve(data, p):
            fail("span does not reproduce node", p)
        if raw[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") != text[s:e] or n["byte_span"] != [cum[s], cum[e]]:
            fail("byte_span mismatch", p)
        if t == "string":
            ls, le = n["literal_span"]
            lit = text[ls:le]
            if (lit if not n["has_escape"] else json.loads('"' + lit + '"')) != v or n["value"] != v:
                fail("literal/value mismatch", p)
            if [ls - 1, le + 1] != [s, e]:
                fail("literal_span not inside quotes", p)
            if raw[n["literal_byte_span"][0]:n["literal_byte_span"][1]].decode("utf-8") != lit:
                fail("literal_byte_span mismatch", p)
        elif t == "object":
            if n["children"] != c:
                fail("children order mismatch", p)
        elif t == "array":
            if n["length"] != c:
                fail("array length mismatch", p)
        else:
            if n["value"] != v:
                fail("scalar mismatch", p)
        if p:
            par = p.rsplit("/", 1)[0]
            if n["parent"] != par:
                fail("parent mismatch", p)
    # keys
    keys = sm["keys"]
    exp_keys = sum(len(c) for t, v, c in ref.values() if t == "object")
    if len(keys) != exp_keys:
        fail("key occurrence count", len(keys), exp_keys)
    seen_kp = set()
    for k in keys:
        s, e = k["key_span"]
        if json.loads(text[s:e]) != k["key"]:
            fail("key span", k["value_pointer"])
        if raw[k["key_byte_span"][0]:k["key_byte_span"][1]].decode("utf-8") != text[s:e]:
            fail("key byte span", k["value_pointer"])
        if k["value_pointer"] in seen_kp:
            fail("dup key value_pointer", k["value_pointer"])
        seen_kp.add(k["value_pointer"])
        if ref.get(k["object_pointer"], (None,))[0] != "object" or k["value_pointer"] not in ref:
            fail("key pointers invalid", k["value_pointer"])
        if resolve(data, k["object_pointer"]) is not None and list(resolve(data, k["object_pointer"]).keys())[k["order"]] != k["key"]:
            fail("key order", k["value_pointer"])
    # field occurrence index
    occ = sum(len(v) for pats in sm["field_name_occurrences"].values() for v in pats.values())
    if occ != len(keys):
        fail("field_name_occurrences total", occ, len(keys))
    for kname, pats in sm["field_name_occurrences"].items():
        for pat, ptrs in pats.items():
            for p in ptrs:
                if not p.endswith("/" + kname) or p not in ref:
                    fail("field occurrence pointer", p)

    # ---------- 4. morphology coverage
    str_ptrs = {p for p, (t, v, c) in ref.items() if t == "string"}
    vals = {v["pointer"]: v for v in mo["values"]}
    excl = {x["pointer"]: x for x in mo["excluded_values"]}
    if len(vals) != len(mo["values"]) or len(excl) != len(mo["excluded_values"]):
        fail("duplicate pointer in morphology values/excluded")
    if set(vals) & set(excl):
        fail("pointer both analyzed and excluded", sorted(set(vals) & set(excl))[:5])
    if set(vals) | set(excl) != str_ptrs:
        fail("analysis coverage mismatch", sorted(str_ptrs - set(vals) - set(excl))[:5])
    pol = {p["pattern"]: p for p in mo["policy"]}
    for p in str_ptrs:
        pat = re.sub(r"/\d+(?=/|$)", "/*", p)
        if pat not in pol:
            fail("no policy for", pat)
            continue
        want = pol[pat]["action"]
        got = "apply" if p in vals else "exclude"
        if want != got:
            fail("policy/action mismatch", p)
        if got == "exclude":
            if excl[p]["value"] != ref[p][1] or not excl[p]["reason"]:
                fail("excluded value/reason", p)
            if "value_regex" in pol[pat] and not re.match(pol[pat]["value_regex"], ref[p][1]):
                fail("excluded value does not fit code regex", p)
    for p, v in vals.items():
        text_v = ref[p][1]
        if v["text"] != text_v:
            fail("analyzed text != source", p)
        fs, fe = v["file_span_of_text"]
        if text[fs:fe] != text_v:
            fail("file_span_of_text", p)
        covered = [False] * len(text_v)
        last = -1
        for i, t in enumerate(v["tokens"]):
            s, e = t["span"]
            if not (0 <= s <= e <= len(text_v)) or (s == e) != t.get("zero_length", False):
                fail("token span out of range / zero_length flag", p, i)
                continue
            if t["surface"] != text_v[s:e]:
                fail("token surface", p, i)
            if t["i"] != i:
                fail("token index", p, i)
            if s < last:
                fail("token order", p, i)
            last = s
            if t["form_equals_surface"] != (t["form"] == text_v[s:e]):
                fail("form_equals_surface flag", p, i)
            for j in range(s, e):
                covered[j] = True
        miss = [j for j, ch in enumerate(text_v) if not ch.isspace() and not covered[j]]
        if miss:
            fail("characters not covered by any token", p, miss[:5])
    fn = {f["field_name"] for f in mo["field_names"]}
    if fn != set(sm["field_name_occurrences"]):
        fail("field names analyzed != keys", fn ^ set(sm["field_name_occurrences"]))
    for f in mo["field_names"]:
        for t in f["tokens"]:
            if f["field_name"][t["span"][0]:t["span"][1]] != t["surface"]:
                fail("field name token surface", f["field_name"])
        if "_".join(f["identifier_parts_rule_based"]) != f["field_name"]:
            fail("identifier parts", f["field_name"])

    # ---------- 5. segmentation & pos review references
    for r in mo["segmentation_review"]:
        v = vals.get(r["pointer"])
        if v is None:
            fail("seg review pointer not analyzed", r["pointer"])
            continue
        s, e = r["phrase_span"]
        if v["text"][s:e] != r["phrase"]:
            fail("seg review phrase span", r["pointer"], r["phrase"])
        for form, tag, sp, i in r["tokens"]:
            t = v["tokens"][i]
            if (t["form"], t["tag"], t["span"]) != (form, tag, sp):
                fail("seg review token ref", r["pointer"], i)
            if not (sp[0] < e and sp[1] > s):
                fail("seg review token not overlapping", r["pointer"], i)
        if r["verdict"] not in ("issue", "ok") or (r["verdict"] == "issue" and not r.get("impact")):
            fail("seg review verdict", r["pointer"])
    rules = load("segmentation-review-rules.json")["rules"]
    for rule in rules:
        rx = re.compile(rule["regex"]) if "regex" in rule else re.compile(re.escape(rule["phrase"]))
        want = {(v["pointer"], m.start()) for v in mo["values"] for m in rx.finditer(v["text"])}
        got = {(r["pointer"], r["phrase_span"][0]) for r in mo["segmentation_review"] if r["rule"] == rule["id"]}
        if want != got:
            fail("seg rule occurrences not all judged", rule["id"], len(want), len(got))
    tags = set(load("pos-review-rules.json")["review_tags"])
    want = {(p, t["i"]) for p, v in vals.items() for t in v["tokens"] if t["tag"] in tags}
    got = Counter((r["pointer"], r["token_index"]) for r in mo["pos_review"])
    if set(got) != want or any(c > 1 for c in got.values()):
        fail("pos review coverage", len(want), len(got))
    for r in mo["pos_review"]:
        t = vals[r["pointer"]]["tokens"][r["token_index"]]
        if (t["form"], t["tag"], t["span"]) != (r["form"], r["tag"], r["span"]) or r["verdict"] not in ("ok", "issue"):
            fail("pos review token ref", r["pointer"], r["token_index"])

    # ---------- 6. expressions
    ids = Counter(x["id"] for x in ex["expressions"])
    if any(c > 1 for c in ids.values()):
        fail("duplicate expression id")
    dk = Counter((x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"]) for x in ex["expressions"])
    if any(c > 1 for c in dk.values()):
        fail("duplicate expression (pointer,span,category,method)", [k for k, c in dk.items() if c > 1][:3])
    whole = set()
    for x in ex["expressions"]:
        v = vals.get(x["pointer"])
        if v is None:
            fail("expression on non-analyzed pointer", x["id"])
            continue
        s, e = x["span"]
        if not (0 <= s < e <= len(v["text"])) or v["text"][s:e] != x["text"]:
            fail("expression span/text", x["id"])
        if x["category_candidate"] == "segment.value":
            whole.add(x["pointer"])
            if [s, e] != [0, len(v["text"])]:
                fail("segment.value not whole", x["id"])
    if whole != set(vals):
        fail("segment.value missing for", sorted(set(vals) - whole)[:5])
    man = load("manual-expressions.json")["expressions"]
    got_man = Counter((x["pointer"], x["text"]) for x in ex["expressions"] if x["source"] == "manual")
    if sum(got_man.values()) != len(man):
        fail("manual expression count", sum(got_man.values()), len(man))
    fps = load("expression-review.json")["false_positives"]
    marked = {(x["pointer"], tuple(x["span"]), x["category_candidate"]) for x in ex["expressions"] if x.get("review", {}).get("verdict") == "false_positive"}
    if marked != {(f["pointer"], tuple(f["span"]), f["category_candidate"]) for f in fps}:
        fail("false positive marking mismatch")

    # ---------- 7. link observations
    for o in lo["observations"]:
        pool = []
        for p in o["pointers"]:
            if "*" in p:
                rx = re.compile("^" + re.escape(p).replace(r"\*", r"\d+") + "$")
                ms = [q for q in str_ptrs if rx.match(q)]
                if not ms:
                    fail("observation pattern matches nothing", p)
                pool += [ref[q][1] for q in ms]
            elif p not in ref:
                fail("observation pointer invalid", o.get("id", o["kind"]), p)
            else:
                pool += [v for q, (t, v, c) in ref.items() if (q == p or q.startswith(p + "/")) and t == "string"]
        for q in o["quote"]:
            if q == "Mxx-":
                continue
            if not any(q in s for s in pool):
                fail("observation quote not in source under pointers", o.get("id", o["kind"]), q)


def main():
    failures = []

    def fail(*a):
        failures.append(" ".join(str(x) for x in a))

    raw0 = SRC.read_bytes()
    text = raw0.decode("utf-8")
    data = json.loads(text)
    sm, mo, ex, lo = load("source-map.json"), load("morphology.json"), load("expressions.json"), load("link-observations.json")
    try:
        check_all(raw0, text, data, sm, mo, ex, lo, fail)
    except Exception as e:  # 검사 중 예외도 실패로 센다
        fail("exception during checks:", repr(e))

    # ---------- 8. mutation self-test (in memory only)
    mutants = []
    m1 = copy.deepcopy(sm)
    for n in m1["nodes"]:
        if n["pointer"] == "/links/54/timing":
            n["value"] = n["value"] + "X"
    mutants.append(("node value altered", m1, mo, ex, lo))
    m2 = copy.deepcopy(mo)
    m2["values"][3]["tokens"][0]["span"][1] += 1
    mutants.append(("token span altered", sm, m2, ex, lo))
    m3 = copy.deepcopy(mo)
    m3["values"].pop(10)
    mutants.append(("analyzed value dropped", sm, m3, ex, lo))
    m4 = copy.deepcopy(ex)
    m4["expressions"][5]["span"][0] += 1
    mutants.append(("expression span altered", sm, mo, m4, lo))
    m5 = copy.deepcopy(sm)
    m5["nodes"] = [n for n in m5["nodes"] if n["pointer"] != "/links/100/reason"]
    mutants.append(("node dropped", m5, mo, ex, lo))
    m6 = copy.deepcopy(mo)
    m6["segmentation_review"].pop(0)
    mutants.append(("segmentation judgement dropped", sm, m6, ex, lo))
    selftest = []
    for name, a, b, c, d in mutants:
        f2 = []
        try:
            check_all(raw0, text, data, a, b, c, d, lambda *x: f2.append(x))
        except Exception as e:
            f2.append(("exception", repr(e)))
        selftest.append((name, len(f2) > 0))
        if not f2:
            fail("self-test mutation not detected:", name)

    # ---------- 9. review.md 가 모든 link 값을 원본 컬럼명 순서대로 담는지
    rv = (OUT / "review.md").read_text(encoding="utf-8").splitlines()
    rows = {}
    for line in rv:
        m = re.match(r"^\| `(/links/\d+(?:/reason)?)` \| (.*) \|$", line)
        if m:
            if m.group(1) in rows:
                fail("review.md duplicate row", m.group(1))
            rows[m.group(1)] = [c.replace("\\|", "|") for c in re.split(r"(?<!\\) \| ", m.group(2))]
    for i, l in enumerate(data["links"]):
        want = [l[f] for f in ("from", "from_category", "to", "to_category", "type", "timing", "target")]
        if rows.get(f"/links/{i}") != want:
            fail("review.md link row mismatch", i)
        if rows.get(f"/links/{i}/reason") != [l["reason"]]:
            fail("review.md reason row mismatch", i)
    if len(rows) != 2 * len(data["links"]):
        fail("review.md row count", len(rows))
    hdr = "| # | from | from_category | to | to_category | type | timing | target |"
    if sum(1 for line in rv if line == hdr) != 4:
        fail("review.md column header (원본 컬럼명) missing")

    raw1 = SRC.read_bytes()
    if hashlib.sha256(raw1).hexdigest() != EXPECTED_SHA:
        fail("source changed during verify")

    summary = {
        "source_sha256": hashlib.sha256(raw1).hexdigest(),
        "nodes": len(sm["nodes"]), "keys": len(sm["keys"]), "string_values": sum(1 for n in sm["nodes"] if n["type"] == "string"),
        "analyzed": len(mo["values"]), "excluded": len(mo["excluded_values"]),
        "tokens": sum(len(v["tokens"]) for v in mo["values"]),
        "segmentation_review": len(mo["segmentation_review"]), "pos_review": len(mo["pos_review"]),
        "expressions": len(ex["expressions"]), "link_observations": len(lo["observations"]),
        "self_test": {n: ("detected" if ok else "MISSED") for n, ok in selftest},
        "failure_count": len(failures),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for f in failures[:50]:
        print("FAIL:", f)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
