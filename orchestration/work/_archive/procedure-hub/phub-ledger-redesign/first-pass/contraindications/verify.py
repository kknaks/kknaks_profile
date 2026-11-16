#!/usr/bin/env python3
"""contraindications.json 1차 조사 — 독립 검증 (표준 라이브러리만, 읽기 전용).

레포 루트에서:
  python3 orchestration/work/phub-ledger-redesign/first-pass/contraindications/verify.py

원본과 결과 파일을 읽기만 한다. 어떤 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.
build.py 의 스캐너를 쓰지 않고 json.loads(object_pairs_hook) 로 원본을 따로 열거한다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC = REPO / "orchestration/work/phub-recommend/bronze/phub-ledger/contraindications.json"

FAILS = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def esc(k):
    return str(k).replace("~", "~0").replace("/", "~1")


def main():
    raw0 = SRC.read_bytes()
    h0 = hashlib.sha256(raw0).hexdigest()
    text = raw0.decode("utf-8")
    load = lambda n: json.loads((HERE / n).read_text())
    sm, mo, ex, cov = load("source-map.json"), load("morphology.json"), load("expressions.json"), load("coverage.json")
    man = load("manual-expressions.json")
    review = (HERE / "review.md").read_text()

    # 1. 해시
    check("hash.source_map", sm["source"]["sha256"] == h0, sm["source"]["sha256"])
    check("hash.coverage", cov["source_sha256"] == h0)
    check("hash.review", h0 in review)
    check("size", sm["source"]["bytes"] == len(raw0))

    # 2. 독립 열거 (중복 키 감지)
    dups = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)

    data = json.loads(text, object_pairs_hook=hook)
    check("dup_keys.none_in_source", not dups, dups)
    check("dup_keys.recorded_match", len(sm["duplicate_keys"]) == len(dups))
    nodes = {}

    def walk(v, p):
        if isinstance(v, dict):
            nodes[p] = ("object", len(v), None)
            for k, c in v.items():
                walk(c, f"{p}/{esc(k)}")
        elif isinstance(v, list):
            nodes[p] = ("array", len(v), None)
            for i, c in enumerate(v):
                walk(c, f"{p}/{i}")
        else:
            t = {str: "string", bool: "boolean", type(None): "null"}.get(type(v), "number")
            nodes[p] = (t, None, v)

    walk(data, "")
    smn = {n["pointer"]: n for n in sm["nodes"]}
    check("nodes.no_duplicate_pointer", len(smn) == len(sm["nodes"]))
    miss = set(nodes) - set(smn)
    extra = set(smn) - set(nodes)
    check("nodes.source_to_map", not miss, sorted(miss)[:5])
    check("nodes.map_to_source", not extra, sorted(extra)[:5])
    bad = [p for p, (t, ln, v) in nodes.items() if p in smn and (smn[p]["type"] != t or
           (ln is not None and smn[p]["length"] != ln) or (ln is None and smn[p]["value"] != v))]
    check("nodes.type_length_value", not bad, bad[:5])
    leaves = {p for p, (t, ln, v) in nodes.items() if t not in ("object", "array") or ln == 0}
    check("leaves.flag", leaves == {p for p, n in smn.items() if n["is_leaf"]})

    # 3. 원문 구간 재현
    badspan = []
    for p, n in smn.items():
        a, b = n["literal_span"]
        lit = text[a:b]
        ba, bb = n["byte_span"]
        if raw0[ba:bb].decode("utf-8") != lit:
            badspan.append((p, "byte"))
        if n["type"] in ("object", "array"):
            if json.loads(lit) != (data if p == "" else None) and p == "":
                badspan.append((p, "root"))
            if lit[0] not in "{[" or lit[-1] not in "}]":
                badspan.append((p, "container"))
        else:
            if json.loads(lit) != n["value"] or lit != n["literal"]:
                badspan.append((p, "literal"))
        if n["type"] == "string":
            ia, ib = n["inner_file_span_cp"]
            if text[ia:ib] != n["value"] or (ia, ib) != (a + 1, b - 1):
                badspan.append((p, "inner"))
    check("spans.literal_byte_inner_reproduce", not badspan, badspan[:5])
    badkey = [k for k in sm["keys"] if text[k["file_span_cp"][0]:k["file_span_cp"][1]] != json.dumps(k["key"], ensure_ascii=False)]
    check("keys.span_reproduce", not badkey, badkey[:3])
    check("keys.count", len(sm["keys"]) == sum(ln for t, ln, v in nodes.values() if t == "object"))

    # 4. 커버리지 — 양방향·중복·상태·결과 파일
    owned = [p for s in cov["sections"] for p in s["owned_leaf_pointers"]]
    check("coverage.no_duplicate_owner", len(owned) == len(set(owned)), len(owned) - len(set(owned)))
    check("coverage.source_leaves_owned", not (leaves - set(owned)), sorted(leaves - set(owned))[:5])
    check("coverage.owned_are_source_leaves", not (set(owned) - leaves), sorted(set(owned) - leaves)[:5])
    conts = [p for s in cov["sections"] for p in s["owned_containers"]]
    check("coverage.containers_bidirectional", set(conts) == set(nodes) - leaves and len(conts) == len(set(conts)))
    for s in cov["sections"]:
        check(f"coverage.{s['id']}.direct_read_done", s["read_status"] == "direct_read_done", s["read_status"])
        check(f"coverage.{s['id']}.review_file", (HERE / s["review_file"]).exists())
        check(f"coverage.{s['id']}.review_anchor", f"## {s['review_anchor']}" in review, s["review_anchor"])
        for p in s["shared_context"]:
            check(f"coverage.{s['id']}.shared_context_exists", p in nodes, p)
            check(f"coverage.{s['id']}.shared_not_owned_here", p not in s["owned_leaf_pointers"], p)
    check("coverage.remaining_empty", cov["remaining_sections"] == [])

    # 5. 형태소 적용·제외 대응
    strings = {p for p, (t, ln, v) in nodes.items() if t == "string"}
    nonstr = {p for p, (t, ln, v) in nodes.items() if t in ("number", "boolean", "null")}
    app = [r["pointer"] for r in mo["records"]]
    exc = [e["pointer"] for e in mo["exclusions"]]
    check("morph.no_double_assign", len(set(app) & set(exc)) == 0 and len(app) == len(set(app)) and len(exc) == len(set(exc)))
    check("morph.all_scalars_assigned", set(app) | set(exc) == strings | nonstr,
          sorted((strings | nonstr) ^ (set(app) | set(exc)))[:5])
    APPLY = {"description", "from_name", "to_name", "interval", "note"}
    check("morph.apply_rule", all(p.rsplit("/", 1)[-1] in APPLY for p in app) and
          all(p.rsplit("/", 1)[-1] not in APPLY for p in exc))
    check("morph.exclusion_reason", all(e["reason"] for e in mo["exclusions"]))
    badtok = []
    for r in mo["records"]:
        if r["text"] != nodes[r["pointer"]][2]:
            badtok.append((r["pointer"], "text"))
        last = 0
        for t in r["tokens"]:
            if not (0 <= t["start"] <= t["end"] <= len(r["text"])) or r["text"][t["start"]:t["end"]] != t["surface"] or t["start"] < last:
                badtok.append((r["pointer"], t))
            last = t["start"]
        if not r["tokens"] and r["text"].strip():
            badtok.append((r["pointer"], "empty"))
    check("morph.tokens_spans", not badtok, badtok[:3])
    st = mo["settings"]
    check("morph.settings", st["analyzer"] == "kiwipiepy" and st["version"] == "0.24.1" and st["model_type"] == "cong" and st["num_workers"] == 1)
    fn = {f["field_name"] for f in mo["field_names"]}
    check("morph.field_names_cover_keys", fn == {k["key"] for k in sm["keys"]})
    badseg = []
    for r in mo["segmentation_review"]["rows"]:
        v = nodes.get(r["pointer"], (None, None, None))[2]
        a, b = r["span_cp"]
        pat = r["term"][3:] if r["term"].startswith("re:") else re.escape(r["term"])
        if v is None or not re.fullmatch(pat, v[a:b]) or r["verdict"] not in ("ok", "known_issue"):
            badseg.append(r)
    check("morph.segmentation_rows_reproduce", not badseg, badseg[:2])

    # 6. 표현
    ids = [e["id"] for e in ex["items"]]
    check("expr.ids_unique", len(ids) == len(set(ids)))
    badex = []
    for e in ex["items"]:
        n = smn.get(e["pointer"])
        a, b = e["span_cp"]
        if not n or n["value"][a:b] != e["text"]:
            badex.append(e["id"]); continue
        ia = n["inner_file_span_cp"][0]
        if e["file_span_cp"] != [ia + a, ia + b] or text[ia + a:ia + b] != e["text"]:
            badex.append(e["id"])
    check("expr.spans_reproduce", not badex, badex[:5])
    key = [(e["pointer"], tuple(e["span_cp"]), e["method"], e.get("pattern_name")) for e in ex["items"]]
    check("expr.no_exact_duplicate", len(key) == len(set(key)))
    manual = [e for e in ex["items"] if e["method"] == "manual_reading"]
    check("expr.manual_all_built", len(manual) == len(man["items"]) and
          all(m["text"] == e["text"] and m["pointer"] == e["pointer"] for m, e in zip(man["items"], manual)))
    check("expr.manual_in_review", all(f"| {e['id']} |" in review or f"`{e['id']}`" in review for e in manual),
          [e["id"] for e in manual if e["id"] not in review][:5])

    # 7. review.md — 모든 말단 값이 원본 컬럼명·Pointer·원문 값 그대로
    missing_rows = []
    for p in leaves:
        t, ln, v = nodes[p]
        k = p.rsplit("/", 1)[-1]
        row = f"| {k} | `{p}` | {t} | {v} |"
        if row not in review:
            missing_rows.append(p)
    check("review.every_leaf_row", not missing_rows, missing_rows[:5])
    for i in range(len(data["rules"])):
        check(f"review.rule_heading_{i}", f"### /rules/{i}\n" in review)
    check("review.observation_separate", review.count("**잠정 관찰 (원문 아님)**") == len(data["rules"]) + 1)
    known = [r for r in mo["segmentation_review"]["rows"] if r["verdict"] == "known_issue"]
    check("review.known_issue_listed", all(f"`{r['pointer']}` [{r['span_cp'][0]},{r['span_cp'][1]})" in review
                                           for r in known if r["pointer"].startswith("/rules/")))
    for f in ("issues.md", "validation.md", "build.py", "coverage.json"):
        check(f"files.{f}", (HERE / f).exists())

    # 8. issues.md 의 「`Pointer` [a,b)」 인용이 원문 값 안 구간인지
    iss = (HERE / "issues.md").read_text()
    badref = []
    for m in re.finditer(r"`(/[^`]+)` \[(\d+),(\d+)\)", iss):
        p, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        v = nodes.get(p, (None, None, None))[2]
        if not isinstance(v, str) or not (0 <= a < b <= len(v)):
            badref.append(m.group(0))
    check("issues.span_refs_valid", not badref, badref[:5])
    ptrs = set(re.findall(r"`(/rules/\d+/[a-z_]+)`", iss))
    check("issues.pointer_refs_exist", ptrs <= set(nodes), sorted(ptrs - set(nodes))[:5])

    # 9. 원본 불변
    check("hash.unchanged_end", hashlib.sha256(SRC.read_bytes()).hexdigest() == h0)

    for name, ok, d in CHECKS:
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" — {d}"))
    print(f"\nsource sha256 {h0}")
    print(f"nodes {len(nodes)} · leaves {len(leaves)} · owned {len(owned)} · morph applied {len(app)} excluded {len(exc)} · "
          f"tokens {sum(len(r['tokens']) for r in mo['records'])} · expressions {len(ids)} (manual {len(manual)}) · known_issue {len(known)}")
    print(f"checks {len(CHECKS)} · failed {len(FAILS)}")
    if FAILS:
        sys.exit(1)
    print("VERIFY PASS")


if __name__ == "__main__":
    main()
