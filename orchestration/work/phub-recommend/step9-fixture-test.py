"""step9-apply.py 고정 시험(8단계와 같은 틀) — 하나라도 FAIL 이면 종료 코드 1.

갈래
- none / determinism      : 원천 · 결정 그대로 → open 0 · 사람 확인 0 / 두 번 실행 바이트 같음
- record                  : 규칙마다 그 원천 행의 레코드(상태 · 붙는 노드 · 표시 · section) — 기대값은 실물 원천에서 뽑음
- record_status_prefix    : D9-6 원문 보관은 붙이지 않음
- source_conflict         : D9-4 extracted.json 이 정본과 다른 칸은 싣지 않음
- section_map             : D9-1 관리 · 예방 → safety.management(8단계 실버 그대로)
- value_dictionary        : D9-7 값 사전 8
- slot                    : D9-3 ①②③ 처분(긴 쪽 · 짧은 쪽 · 늦은 쪽 · 둘 다)
- guard_resolved_one      : ② 칸은 골드로 숫자 값 하나만(alternatives 는 emit 밖)
- remove_decision         : 결정 한 줄 빼면 open
- canon_mutate            : 5단계 단위 시술이 없어지면 그 레코드는 open
입력: step9-fixtures/cases.json · step9-decisions.json · step9-apply.py · 실버 정본 · 원천
출력: step9-fixtures/result.json
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
CASES = json.load(open(W / "step9-fixtures" / "cases.json", encoding="utf-8"))["cases"]
DEC = json.load(open(W / "step9-decisions.json", encoding="utf-8"))


def run(td, dec=None, canon=None):
    cmd = [sys.executable, str(W / "step9-apply.py"), "--out", str(td)]
    if dec:
        cmd += ["--decisions", str(dec)]
    if canon:
        cmd += ["--canon", str(canon)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None, p.stderr.strip()[-300:]
    return json.load(open(Path(td) / "step9-explanations.json", encoding="utf-8")), None


def numset(t):
    s = set(re.findall(DEC["conflict_resolution"]["numeric_regex"], t))
    return s or ({"0"} if any(z in t for z in DEC["conflict_resolution"]["zero_words"]) else set())


def main():
    res = []
    with tempfile.TemporaryDirectory() as t0:
        base, err = run(t0)
        if base is None:
            print("기본 실행 실패", err)
            return 1
        a_json = (Path(t0) / "step9-explanations.json").read_bytes()
        a_md = (Path(t0) / "step9-explanations.md").read_bytes()
    rec = {r["source"]["path"]: r for r in base["records"]}
    rid = {r["id"]: r for r in base["records"]}
    slots = {(e["node"], e["slot"]): e for e in base["node_slots"]}
    for c in CASES:
        ok, why = False, ""
        k = c["kind"]
        try:
            if k == "none":
                ok = base["summary"]["open"] == 0 and base["summary"]["human_check"] == 0
                why = f"open {base['summary']['open']}"
            elif k == "determinism":
                with tempfile.TemporaryDirectory() as t1:
                    run(t1)
                    ok = (Path(t1) / "step9-explanations.json").read_bytes() == a_json and (Path(t1) / "step9-explanations.md").read_bytes() == a_md
            elif k == "record":
                r = rec[c["path"]]
                got = {"status": r["status"], "nodes": r["attach"]["nodes"], "flags": r["attach"]["flags"], "section": r["section"]}
                ok = all(got[x] == v for x, v in c["expect"].items())
                why = json.dumps(got, ensure_ascii=False)
            elif k == "record_status_prefix":
                n = sum(1 for r in base["records"] if r["rule"] == c["rule"] and r["status"].startswith(c["status_prefix"]) and not r["attach"]["nodes"])
                ok = n >= c["min"]
                why = f"{n}"
            elif k == "source_conflict":
                ok = any(x["path"] == c["path"] and x["rule"] == c["rule"] for x in base["source_conflicts"]) and rec[c["path"]]["attach"]["nodes"] == []
            elif k == "section_map":
                x = next(x for x in base["section_map"] if x["path"] == c["path"])
                ok = all(x[a] == v for a, v in c["expect"].items())
                why = json.dumps(x, ensure_ascii=False)
            elif k == "value_dictionary":
                cnt = {}
                for x in base["value_dictionary"]:
                    cnt[x["dictionary"]] = cnt.get(x["dictionary"], 0) + 1
                ok = cnt == c["expect"]
                why = json.dumps(cnt, ensure_ascii=False)
            elif k == "slot":
                e = slots[(c["node"], c["slot"])]
                ex = c["expect"]
                ok = e["class"] == ex["class"]
                if "emit" in ex:
                    ok &= e["emit"] == ex["emit"]
                if "emit_n" in ex:
                    ok &= len(e["emit"]) == ex["emit_n"]
                if "multi_source" in ex:
                    ok &= bool(e.get("multi_source")) == ex["multi_source"]
                if "resolved_by" in ex:
                    ok &= e.get("resolved_by") == ex["resolved_by"] and ex["resolved_text_has"] in rid[e["resolved"]]["text"] and bool(e["alternatives"])
                why = json.dumps({x: e.get(x) for x in ("class", "emit", "resolved_by", "resolved", "alternatives")}, ensure_ascii=False)[:300]
            elif k == "guard_resolved_one":
                bad = [e for e in base["node_slots"] if e["class"] == "②" and (
                    sum(1 for x in e["emit"] if numset(rid[x]["text"])) != 1 or set(e["alternatives"]) & set(e["emit"]))]
                ok = not bad
                why = f"위반 {len(bad)}"
            elif k == "remove_decision":
                d = json.loads(json.dumps(DEC))
                head, _, leaf = c["path"].partition(".")
                if leaf:
                    del d[head][leaf]
                else:
                    d[head] = [x for x in d[head] if x != c["value"]]
                with tempfile.TemporaryDirectory() as td:
                    dp = Path(td) / "dec.json"
                    dp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
                    o, err = run(Path(td) / "out", dec=dp)
                    ok = o is not None and any(x["type"] == c["expect_open"] for x in o["open"])
                    why = err or f"open {len(o['open'])}"
            elif k == "canon_mutate":
                with tempfile.TemporaryDirectory() as td:
                    cd = Path(td) / "canon"
                    cd.mkdir()
                    for f in DEC["canon"]:
                        shutil.copy(W / f, cd / f)
                    s5 = json.load(open(cd / c["file"], encoding="utf-8"))
                    s5["units"] = [u for u in s5["units"] if u["id"] != c["remove_unit"]]
                    (cd / c["file"]).write_text(json.dumps(s5, ensure_ascii=False), encoding="utf-8")
                    o, err = run(Path(td) / "out", canon=cd)
                    ok = o is not None and any(x["type"] == c["expect_open"] and f"unit_procedure:{c['remove_unit']}" in (x.get("missing") or []) for x in o["open"])
                    why = err or f"open {len(o['open'])}"
        except Exception as ex:  # noqa: BLE001
            ok, why = False, f"{type(ex).__name__}: {ex}"
        res.append({"id": c["id"], "kind": k, "what": c["what"], "pass": bool(ok), "detail": why})
    out = {"cases": len(res), "pass": sum(r["pass"] for r in res), "fail": [r["id"] for r in res if not r["pass"]], "results": res}
    (W / "step9-fixtures" / "result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for r in res:
        print(("PASS " if r["pass"] else "FAIL ") + r["id"] + " — " + r["what"] + ("" if r["pass"] else f" ({r['detail']})"))
    print(f"{out['pass']}/{out['cases']}")
    return 0 if not out["fail"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
