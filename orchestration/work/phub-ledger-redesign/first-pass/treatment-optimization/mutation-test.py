"""verify.py 변이 시험: 결과 폴더를 임시 디렉토리에 복사해 한 곳씩 망가뜨리고 verify 가 실패(exit 1)를 내는지 본다.
실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/mutation-test.py
원본·결과 폴더는 건드리지 않는다. 임시 디렉토리는 끝나면 지운다."""
import json, os, shutil, sys, runpy, io, contextlib, tempfile
D = os.path.dirname(os.path.abspath(__file__))
SP = tempfile.mkdtemp(prefix="to-mut-")
ROOT = os.path.abspath(os.path.join(D, *[".."]*5))
def run(name, mutate):
    w = os.path.join(SP, "mut-" + name)
    if os.path.exists(w): shutil.rmtree(w)
    shutil.copytree(D, w, ignore=shutil.ignore_patterns("__pycache__"))
    mutate(w)
    g = runpy.run_path(os.path.join(w, "verify.py"), run_name="not_main")
    g["main"].__globals__["HERE"] = w; g["main"].__globals__["SRC"] = os.path.join(ROOT, "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json")
    g["main"].__globals__["CHECKS"].clear(); g["main"].__globals__["FAIL"].clear()
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): g["main"]()
        code = 0
    except SystemExit as e: code = e.code
    except Exception as e: code = "exception:" + type(e).__name__
    fails = [l for l in buf.getvalue().splitlines() if l.startswith("FAIL")]
    print(name, "exit", code, "|", "; ".join(f.split(" — ")[0] for f in fails))
def jedit(w, f, fn):
    p = os.path.join(w, f); d = json.load(open(p, encoding="utf-8")); fn(d); json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
run("baseline", lambda w: None)
run("coverage_drop_leaf", lambda w: jedit(w, "coverage.json", lambda d: d["segments"][5]["owned_leaf_pointers"].pop(3)))
run("coverage_dup_leaf", lambda w: jedit(w, "coverage.json", lambda d: d["segments"][6]["owned_leaf_pointers"].append(d["segments"][5]["owned_leaf_pointers"][0])))
run("coverage_unread", lambda w: jedit(w, "coverage.json", lambda d: d["segments"][12].__setitem__("direct_reading", "not_read")))
def tokmut(d): d["tokens"][100]["start"] += 1
run("token_span_shift", lambda w: jedit(w, "morphology.json", tokmut))
def rowdel(w):
    p = os.path.join(w, "review-part-3.md"); s = open(p, encoding="utf-8").read().splitlines()
    s = [l for l in s if not l.startswith("| `/combination_rules/4/detail` |")]; open(p, "w", encoding="utf-8").write("\n".join(s))
run("review_row_deleted", rowdel)
def exmut(d):
    for e in d["expressions"]:
        if e["source"] == "manual_direct_reading": e["span"][0] += 1; break
run("expr_span_shift", lambda w: jedit(w, "expressions.json", exmut))
def srcval(d):
    for n in d["nodes"]:
        if n["pointer"] == "/annual_plans/1/schedule/4/procedures/0": n["value"] = "토닝 3회"
run("source_map_value_changed", lambda w: jedit(w, "source-map.json", srcval))
shutil.rmtree(SP)
