#!/usr/bin/env python3
"""treatment-optimization 1차 조사 산출물 독립 검증기.

실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/verify.py
- 표준 라이브러리만 쓴다(Kiwi 불필요). 어떤 파일도 쓰지 않는다.
- build.py 의 스캐너를 쓰지 않고 json 파서 + 자체 재귀로 원문 경로 집합을 다시 만든다.
- 실패가 하나라도 있으면 exit 1.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 5))
SRC = os.path.join(ROOT, "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json")
EXPECTED_SHA = "07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b"

FAIL = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, ok, detail))
    if not ok:
        FAIL.append(f"{name}: {detail}")


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def vcol(n, nmap):
    if n["key"] is not None:
        return n["key"]
    if n["index"] is not None:
        par = nmap[n["parent"]]
        return f"{vcol(par, nmap) if par['key'] is None else par['key']}[{n['index']}]"
    return "(root)"


def main():
    raw = open(SRC, "rb").read()
    sha0 = hashlib.sha256(raw).hexdigest()
    check("source.sha256_expected", sha0 == EXPECTED_SHA, sha0)
    text = raw.decode("utf-8")

    dups = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return OrderedDict(pairs)
    data = json.loads(text, object_pairs_hook=hook)
    check("source.duplicate_keys_none", not dups, str(dups))

    # 독립 경로 열거
    truth = OrderedDict()

    def walk(x, p):
        if isinstance(x, dict):
            truth[p] = ("object", list(x.keys()))
            for k, v in x.items():
                walk(v, p + "/" + esc(k))
        elif isinstance(x, list):
            truth[p] = ("array", len(x))
            for i, v in enumerate(x):
                walk(v, p + "/" + str(i))
        else:
            truth[p] = ("scalar", x)
    walk(data, "")

    def subtree(p):
        x = data
        for t in [s for s in p.split("/")[1:]]:
            t = t.replace("~1", "/").replace("~0", "~")
            x = x[int(t)] if isinstance(x, list) else x[t]
        return x

    sm = load("source-map.json")
    check("source_map.sha256", sm["source"]["sha256_start"] == sha0, sm["source"]["sha256_start"])
    check("source_map.size", sm["source"]["size_bytes"] == len(raw) and sm["source"]["code_points"] == len(text), "")
    nodes = sm["nodes"]
    ptrs = [n["pointer"] for n in nodes]
    check("source_map.no_duplicate_pointer", len(ptrs) == len(set(ptrs)), str([p for p, c in Counter(ptrs).items() if c > 1][:5]))
    missing = [p for p in truth if p not in set(ptrs)]
    extra = [p for p in ptrs if p not in truth]
    check("source_map.pointers_source_to_map", not missing, str(missing[:5]))
    check("source_map.pointers_map_to_source", not extra, str(extra[:5]))
    check("source_map.order", ptrs == list(truth.keys()), "문서 순서 불일치")
    bad_val, bad_span, bad_byte, bad_vspan = [], [], [], []
    bmap = {}
    acc = 0
    for i, ch in enumerate(text):
        bmap[i] = acc
        acc += len(ch.encode("utf-8"))
    bmap[len(text)] = acc
    for n in nodes:
        p = n["pointer"]
        if p not in truth:
            continue
        kind, tv = truth[p]
        if kind == "object":
            if n["type"] != "object" or n["children"] != tv:
                bad_val.append(p)
        elif kind == "array":
            if n["type"] != "array" or n["length"] != tv:
                bad_val.append(p)
        else:
            if n.get("value") != tv or type(n.get("value")) is not type(tv):
                bad_val.append(p)
        s, e = n["span"]
        try:
            if json.loads(text[s:e]) != subtree(p):
                bad_span.append(p)
        except Exception:
            bad_span.append(p)
        bs, be = n["byte_span"]
        if (bmap[s], bmap[e]) != (bs, be) or raw[bs:be].decode("utf-8") != text[s:e]:
            bad_byte.append(p)
        if n["type"] == "string":
            vs, ve = n["value_span"]
            if text[vs:ve] != n["value"] or n.get("json_literal") != text[s:e]:
                bad_vspan.append(p)
    check("source_map.values_types_match_source", not bad_val, str(bad_val[:5]))
    check("source_map.span_reparses_to_source_subtree", not bad_span, str(bad_span[:5]))
    check("source_map.byte_span", not bad_byte, str(bad_byte[:5]))
    check("source_map.value_span_literal", not bad_vspan, str(bad_vspan[:5]))
    # 키 출현
    true_keys = [(p, k, i) for p, (kind, tv) in truth.items() if kind == "object" for i, k in enumerate(tv)]
    sm_keys = [(k["object_pointer"], k["key"], k["order_in_object"]) for k in sm["keys"]]
    check("source_map.keys_bidirectional_with_order", sorted(sm_keys) == sorted(true_keys) and len(sm_keys) == len(set(sm_keys)), f"{len(sm_keys)} vs {len(true_keys)}")
    check("source_map.keys_document_order", [k["span"][0] for k in sm["keys"]] == sorted(k["span"][0] for k in sm["keys"]), "")
    bad_k = [k for k in sm["keys"] if json.loads(text[k["span"][0]:k["span"][1]]) != k["key"]]
    check("source_map.key_spans", not bad_k, str(bad_k[:3]))
    fo = sm["field_name_occurrences"]
    fo_set = sorted((k, p) for k, pats in fo.items() for ps in pats.values() for p in ps)
    check("source_map.field_name_occurrences", fo_set == sorted((k["key"], k["value_pointer"]) for k in sm["keys"]), "")

    leaves = [p for p, (kind, tv) in truth.items() if kind == "scalar" or (kind in ("object", "array") and (tv == [] or tv == 0))]
    containers = [p for p in truth if p not in set(leaves)]

    # coverage
    cov = load("coverage.json")
    check("coverage.sha256", cov["source_sha256"] == sha0, "")
    owned_leaf = [p for s in cov["segments"] for p in s["owned_leaf_pointers"]]
    owned_cont = [p for s in cov["segments"] for p in s["owned_container_pointers"]]
    check("coverage.leaf_no_duplicate_owner", len(owned_leaf) == len(set(owned_leaf)), str([p for p, c in Counter(owned_leaf).items() if c > 1][:5]))
    check("coverage.leaf_source_to_segments", not (set(leaves) - set(owned_leaf)), str(sorted(set(leaves) - set(owned_leaf))[:5]))
    check("coverage.leaf_segments_to_source", not (set(owned_leaf) - set(leaves)), str(sorted(set(owned_leaf) - set(leaves))[:5]))
    check("coverage.container_bidirectional", sorted(owned_cont) == sorted(containers) and len(owned_cont) == len(set(owned_cont)), "")
    seg_of = {}
    for s in cov["segments"]:
        for p in s["owned_leaf_pointers"] + s["owned_container_pointers"]:
            seg_of[p] = s["segment"]
    smseg = {n["pointer"]: n["segment"] for n in nodes}
    check("coverage.segment_matches_source_map", all(smseg[p] == seg_of.get(p) for p in smseg), "")
    for s in cov["segments"]:
        sid = s["segment"]
        check(f"coverage.{sid}.direct_read", s["direct_reading"] == "direct_read_done", s["direct_reading"])
        mf = os.path.join(HERE, s["manual_record"] or "__none__")
        ok = os.path.exists(mf)
        check(f"coverage.{sid}.manual_record_exists", ok, str(s["manual_record"]))
        if ok:
            m = json.load(open(mf, encoding="utf-8"))
            check(f"coverage.{sid}.manual_record_segment", m["segment"] == sid and m["read_status"] == "direct_read_done", "")
            check(f"coverage.{sid}.manual_has_observations", len(m.get("observations", [])) > 0, "")
        rf = os.path.join(HERE, s["review_file"])
        check(f"coverage.{sid}.review_file_anchor", os.path.exists(rf) and f'<a id="{sid.lower()}"></a>' in open(rf, encoding="utf-8").read(), s["review_file"])
        bad_ctx = [p for p in s["context_refs"] if p not in truth or seg_of.get(p) == sid]
        check(f"coverage.{sid}.context_refs_valid_not_owned", not bad_ctx, str(bad_ctx))

    # review 문서: 모든 노드가 소유 구획의 review-part 에 Pointer·원본 컬럼명·원문 값으로 실렸는지
    parts = {s["segment"]: open(os.path.join(HERE, s["review_file"]), encoding="utf-8").read() for s in cov["segments"]}
    missing_rows = []
    nmap = {n["pointer"]: n for n in nodes}
    for n in nodes:
        doc = parts[n["segment"]]
        # 구획 절만 잘라 본다
        a = doc.find(f'<a id="{n["segment"].lower()}"></a>')
        b = doc.find('<a id="', a + 5)
        sec = doc[a:b if b > 0 else len(doc)]
        ptr_md = n["pointer"].replace("|", "\\|")
        line = next((ln for ln in sec.splitlines() if ln.startswith(f"| `{ptr_md}` |")), None)
        if line is None:
            missing_rows.append(n["pointer"])
            continue
        col = vcol(n, nmap)
        if f"`{col}`" not in line:
            missing_rows.append(n["pointer"] + " (컬럼명)")
        if n["type"] not in ("object", "array") and n["json_literal"].replace("|", "\\|") not in line:
            missing_rows.append(n["pointer"] + " (값)")
    check("review.every_node_row_in_owning_part", not missing_rows, str(missing_rows[:5]))
    rv = open(os.path.join(HERE, "review.md"), encoding="utf-8").read()
    check("review.toc_links_all_parts", all(f"({s['review_file']}#{s['segment'].lower()})" in rv.replace("./", "") for s in cov["segments"]), "")
    pats = set(re.sub(r"/\d+", "/*", p) for p in truth if p)
    check("review.column_table_all_patterns", all(f"| `{pt}` |" in rv for pt in pats), str([pt for pt in pats if f"| `{pt}` |" not in rv][:5]))

    # morphology
    mo = load("morphology.json")
    strings = [p for p, (k, v) in truth.items() if k == "scalar" and isinstance(v, str)]
    nonstr = [p for p, (k, v) in truth.items() if k == "scalar" and not isinstance(v, str)]
    ap = [a["pointer"] for a in mo["applied_values"]]
    ex = [a["pointer"] for a in mo["excluded_values"]]
    check("morph.applied_excluded_partition", sorted(ap + ex) == sorted(strings) and not (set(ap) & set(ex)), f"{len(ap)}+{len(ex)} vs {len(strings)}")
    check("morph.excluded_have_reason", all(a.get("reason") for a in mo["excluded_values"]), "")
    check("morph.nonstring_listed", sorted(a["pointer"] for a in mo["nonstring_leaves"]) == sorted(nonstr), "")
    check("morph.field_names_all_keys", sorted(f["field_name"] for f in mo["field_names"]) == sorted(set(k for _, k, _ in true_keys)), "")
    vals = {p: truth[p][1] for p in strings}
    tok_by = {}
    bad_tok = []
    for t in mo["tokens"]:
        tok_by.setdefault(t["value_pointer"], []).append(t)
        v = vals.get(t["value_pointer"])
        if v is None or not (0 <= t["start"] <= t["end"] <= len(v)) or v[t["start"]:t["end"]] != t["surface"]:
            bad_tok.append(t["id"])
    check("morph.token_surface_reproduces_source", not bad_tok, str(bad_tok[:5]))
    check("morph.token_ids_unique", len({t["id"] for t in mo["tokens"]}) == len(mo["tokens"]), "")
    check("morph.applied_token_counts", all(len(tok_by.get(a["pointer"], [])) == a["token_count"] > 0 for a in mo["applied_values"]), "")
    check("morph.tokens_only_on_applied", set(tok_by) == set(ap), "")
    uncovered_chars = []
    for p in ap:
        v = vals[p]
        cov_c = [False] * len(v)
        for t in tok_by[p]:
            for i in range(t["start"], t["end"]):
                cov_c[i] = True
        for i, c in enumerate(v):
            if not c.isspace() and not cov_c[i]:
                uncovered_chars.append((p, i, c))
    check("morph.every_nonspace_char_in_some_token", not uncovered_chars, str(uncovered_chars[:5]))
    bad_seg = []
    for e in mo["known_segmentation_issues"]:
        v = vals[e["pointer"]]
        s, en = e["span"]
        raw_t = [f"{t['form']}/{t['tag']}" for t in tok_by[e["pointer"]] if t["start"] < en and t["end"] > s]
        if v[s:en] != e["text"] or raw_t != e["raw_tokens"] or not e.get("impact"):
            bad_seg.append((e["pointer"], e["text"]))
    check("morph.known_segmentation_issues_reproduce", not bad_seg, str(bad_seg[:5]))
    sr = json.load(open(os.path.join(HERE, "manual/segmentation-review.json"), encoding="utf-8"))
    check("morph.segmentation_review_all_attached", len(sr["entries"]) == len(mo["known_segmentation_issues"]), "")

    # expressions
    ex_ = load("expressions.json")
    ids = [e["id"] for e in ex_["expressions"]]
    check("expr.ids_unique", len(ids) == len(set(ids)), str([i for i, c in Counter(ids).items() if c > 1][:5]))
    sig = [(e["source"], e.get("pattern"), e["pointer"], tuple(e["span"]), tuple(e.get("kinds") or [])) for e in ex_["expressions"]]
    check("expr.no_exact_duplicate", len(sig) == len(set(sig)), str([s for s, c in Counter(sig).items() if c > 1][:3]))
    bad_e = [e["id"] for e in ex_["expressions"] if e["pointer"] not in vals or vals[e["pointer"]][e["span"][0]:e["span"][1]] != e["text"] or smseg[e["pointer"]] != e["segment"]]
    check("expr.span_reproduces_source", not bad_e, str(bad_e[:5]))
    excluded_set = set(ex)
    check("expr.none_on_excluded_values", not [e for e in ex_["expressions"] if e["pointer"] in excluded_set], "")
    man_expected = []
    for s in cov["segments"]:
        m = json.load(open(os.path.join(HERE, s["manual_record"]), encoding="utf-8"))
        for me in m.get("manual_expressions", []):
            man_expected.append((me["pointer"], me["text"]))
    man_got = [(e["pointer"], e["text"]) for e in ex_["expressions"] if e["source"] == "manual_direct_reading"]
    check("expr.manual_bidirectional", sorted(man_expected) == sorted(man_got), f"{len(man_expected)} vs {len(man_got)}")
    # 자동 정규식 재실행 대조
    auto_re = [(p["id"], re.compile(p["regex"])) for p in ex_["auto_patterns"]]
    re_auto = set()
    for p in ap:
        for pid, rx in auto_re:
            for m in rx.finditer(vals[p]):
                if m.end() > m.start():
                    re_auto.add((p, pid, m.start(), m.end()))
    got_auto = set((e["pointer"], e["pattern"], e["span"][0], e["span"][1]) for e in ex_["expressions"] if e["source"] == "auto_regex")
    check("expr.auto_regex_rerun_bidirectional", re_auto == got_auto, f"{len(re_auto)} vs {len(got_auto)}")
    rv_ = json.load(open(os.path.join(HERE, "manual/expression-review.json"), encoding="utf-8"))
    fp_got = set((e["pointer"], e["pattern"], e["span"][0], e["span"][1]) for e in ex_["expressions"] if e.get("review", {}).get("false_positive"))
    fp_exp = set((f["pointer"], f["pattern"], f["span"][0], f["span"][1]) for f in rv_["auto_false_positives"])
    check("expr.false_positive_marks_match_review", fp_got == fp_exp, f"{len(fp_got)} vs {len(fp_exp)}")
    tags, forms = set(ex_["check_tags"]), set(ex_["check_forms"])
    need = set(t["id"] for t in mo["tokens"] if t["tag"] in tags or t["form"] in forms)
    have = {c["token_id"]: c["status"] for c in ex_["modifier_token_check"]}
    check("expr.modifier_check_complete", need == set(have), f"{len(need)} vs {len(have)}")
    check("expr.modifier_check_none_unreviewed", "UNREVIEWED" not in have.values(), str(Counter(have.values())))

    # issues / 문서
    iss = open(os.path.join(HERE, "issues.md"), encoding="utf-8").read()
    miss_iss = []
    for s in cov["segments"]:
        m = json.load(open(os.path.join(HERE, s["manual_record"]), encoding="utf-8"))
        for it in m.get("issues", []):
            if f"**{it['id']}**" not in iss:
                miss_iss.append(it["id"])
            if it.get("note") and f"  - 비고: {it['note']}" not in iss:
                miss_iss.append(it["id"] + ":note")
    gi = json.load(open(os.path.join(HERE, "manual/global-issues.json"), encoding="utf-8"))
    for it in gi["issues"]:
        if f"**{it['id']}**" not in iss:
            miss_iss.append(it["id"])
    check("issues.all_recorded", not miss_iss, str(miss_iss))
    for f in ["review.md", "issues.md", "validation.md", "progress.md", "build.py", "source-map.json", "morphology.json", "expressions.json", "coverage.json"]:
        check(f"files.{f}", os.path.exists(os.path.join(HERE, f)), "")

    sha1 = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    check("source.sha256_unchanged_end", sha1 == sha0, sha1)

    for name, ok, detail in CHECKS:
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" — {detail}"))
    print(f"checks={len(CHECKS)} failures={len(FAIL)} nodes={len(truth)} leaves={len(leaves)} tokens={len(mo['tokens'])} expressions={len(ids)}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # 예상 밖 구조 손상도 실패로 보고한다
        for name, ok, detail in CHECKS:
            print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" — {detail}"))
        print(f"FAIL verify.unexpected_exception — {type(exc).__name__}: {exc}")
        print(f"checks={len(CHECKS)} failures={len(FAIL) + 1}")
        sys.exit(1)
