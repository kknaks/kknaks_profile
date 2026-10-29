"""부위 원장 점검 — 원천 이름 칸을 다시 훑어 step3-sites.json · step3-decisions.json 과 맞춰 본다.

읽기만 한다. 원장(step3-sites.json) · 결정(step3-decisions.json) · 사전(step3-lexicon.json) · 원천은 고치지 않는다 —
결과는 결정 목록의 재료다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --work orchestration/work/phub-recommend \
        --out <scratchpad>/site-check.json          # --source <원천 폴더> 로 새 스냅샷을 볼 수 있다

본다(지금 원천 기준 — 가상 문장 · 해부학 목록 확장 시험은 하지 않는다. _RESUME §2 10-28 「끝 조건 = 지금 원천 기준」):
- 이름 칸 전수 재추출 — 결정 name_fields 17칸만 걷고 사전(step3-lexicon.json entries)으로 부위 문자열을 뽑는다
  - 뽑혔는데 결정 strings[] 에 없는 문자열 = open(새 문자열 — 판정 필요). strings_out_of_scope 에 있으면 「셈 밖 결정 되살림 후보」로 같이 표시
  - 사전 밖 부위 형태소(잔여 · 허용 목록 대조 · 이름 칸만) = open
  - 결정에 있는데 원천에 없는 문자열 = stale
  - name_fields 칸이 원천에 없음(0칸) = 오류
- 결정 행 — destination · nodes(노드 53 안) · deferred_stage · kind ↔ handoff(D-07) · 근거 약 행의 질문
- 노드 근거 — 노드마다 이름 칸 문자열 ≥1 또는 name_field_exception(묶음 자리)
- 전문의 용어 — anatomical_name 값(en · ko)에 근육 · 뼈 · 혈관 · 신경 표지가 0 인지(이름 2벌 규칙). 근육 이름이 상담 말인 노드 이름(승모근)은 보지 않는다
- 원장 ↔ 재추출 — 원장 strings[] 의 키 · 등장 수 · 행선지가 다시 센 값과 같은지(원장이 결정보다 낡았나) · summary 셈 · open 0

종료 코드: errors 0 · open 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

D07 = "부위+다른 축(D-07)"
# 이름 2벌 규칙 — 전문의 용어(겉자리 이름)에 들어가면 안 되는 표지. 해부학 목록이 아니라 「근육 · 뼈 · 혈관 · 신경」이라는 종류 표지만 본다
NOT_SURFACE_EN = re.compile(r"\b(muscle|musculus|m\.|mm\.|bone|os|artery|arteria|vein|vena|nerve|nervus|ligament|fascia)\b", re.I)
NOT_SURFACE_KO = re.compile(r"[가-힣]+(근|뼈|동맥|정맥|신경|인대|근막)(?![가-힣])")


def norm(s: str) -> str:
    k = re.sub(r"\s+", "", s)
    return k.lower() if re.match(r"^[A-Za-z]", k) else k


def fold(s: str) -> str:
    out = []
    for ch in s:
        if "À" <= ch <= "ɏ":
            b = "".join(c for c in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(c))
            out.append(b if len(b) == 1 else ch)
        else:
            out.append(ch)
    return "".join(out)


def walk(x, path, f, out):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(v, path + [k], f, out)
    elif isinstance(x, list):
        for v in x:
            walk(v, path + [None], f, out)
    elif isinstance(x, str):
        out.append((f, ".".join("[]" if p is None else p for p in path), fold(x)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", required=True, help="orchestration/work/phub-recommend")
    ap.add_argument("--source", help="원천 폴더(없으면 결정 source.path)")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    W = Path(a.work)
    DEC = json.loads((W / "step3-decisions.json").read_text())
    LEX = json.loads((W / DEC["lexicon"]).read_text())
    LED = json.loads((W / "step3-sites.json").read_text())
    TREE = json.loads((W / DEC["tree_source"]["file"]).read_text())[DEC["tree_source"]["key"]]
    SRC = Path(a.source or DEC["source"]["path"])

    errors: list[dict] = []
    opened: list[dict] = []

    def err(kind: str, msg: str, **kw) -> None:
        errors.append(dict(kind=kind, msg=msg, **kw))

    # ── 1. 원천 → 이름 칸 ──
    files = sorted(glob.glob(str(SRC / DEC["source"]["glob"])))
    src_all: list[tuple] = []
    for fp in files:
        walk(json.loads(Path(fp).read_text()), [], os.path.basename(fp), src_all)
    nf = [(x["file"], x["key"]) for x in DEC["name_fields"]["fields"]]
    nf_set = set(nf)
    src = [r for r in src_all if (r[0], r[1]) in nf_set]
    per_field = collections.Counter((r[0], r[1]) for r in src)
    for fk in nf:
        if per_field[fk] == 0:
            err("이름 칸 없음", f"name_fields {fk[0]} {fk[1]} 이 원천에 0칸 — 원천 키가 바뀌었나", field=list(fk))

    # ── 2. 사전 매치(step3-apply.py 와 같은 우선순위 · 같은 정규화) ──
    compiled = [((i - 100000 if e["first"] else i), e, re.compile(e["pattern"], 0 if e["case_sensitive"] else re.I))
                for i, e in enumerate(LEX["entries"])]
    found: dict = {}
    covered = []
    for f, p, s in src:
        ms = []
        for pr, e, rx in compiled:
            for m in rx.finditer(s):
                if m.end() > m.start():
                    ms.append((m.start(), pr, m.end(), e))
        ms.sort(key=lambda t: (t[0], t[1]))
        pos, cv = 0, []
        for st, pr, en, e in ms:
            if st < pos:
                continue
            pos = en
            cv.append((st, en))
            if e["expr"].startswith("#skip"):
                continue
            k = (norm(s[st:en]), e["expr"])
            c = found.setdefault(k, dict(count=0, variants=collections.Counter(), samples=[]))
            c["count"] += 1
            c["variants"][s[st:en]] += 1
            if len(c["samples"]) < 2:
                c["samples"].append(dict(file=f, key=p, text=s[max(0, st - 20):en + 20]))
        covered.append(cv)

    # ── 3. 잔여(사전 밖 부위 형태소 · 이름 칸만) ──
    RS = LEX["residual"]
    node_terms = {re.sub(r"\(묶음\)$", "", n) for n in DEC["nodes"]} | {x["key"][0] for x in DEC["strings"] if x["destination"] == "node"}

    def node_list_end(t: str) -> bool:
        m = re.search(r"([가-힣A-Za-z]+)\s*$", t)
        if not m:
            return False
        w = m.group(1)
        conj = re.search(r"(?<=[가-힣])[과와]$", w)
        if conj:
            w = w[:-1]
        if w not in node_terms:
            return False
        return bool(conj) or not re.search(r"[,·/、(]\s*$", t[:m.start()])

    allowed = {x.lower() for g in RS["allowed"] for x in g["tokens"]}
    allowed_pat = [(re.compile(p["token"]), re.compile(p["before"]), p.get("not_after_node_term", False)) for p in RS.get("allowed_patterns", [])]
    morph = ([(m, re.compile(re.escape(m))) for m in RS["morphemes_ko"]]
             + [(m["label"], re.compile(m["pattern"])) for m in RS.get("morpheme_patterns_ko", [])]
             + [(m, re.compile(re.escape(m), re.I)) for m in RS["stems_en"]])
    reviewed = DEC.get("residual_reviewed", [])
    residual: dict = collections.OrderedDict()
    for (f, p, s), cv in zip(src, covered):
        seen = set()
        for m, rx in morph:
            for mm in rx.finditer(s):
                if any(x <= mm.start() < y for x, y in cv):
                    continue
                x, y = mm.start(), mm.end()
                while x > 0 and re.match("[가-힣A-Za-z]", s[x - 1]):
                    x -= 1
                while y < len(s) and re.match("[가-힣A-Za-z]", s[y]):
                    y += 1
                if (x, y) in seen:
                    continue
                seen.add((x, y))
                t = s[x:y]
                if t.lower() in allowed or any(tp.fullmatch(t) and bp.search(s[:x]) and not (na and node_list_end(s[:x])) for tp, bp, na in allowed_pat):
                    continue
                if any(rv["token"] == t and rv["file"] == f and rv["context"] in s for rv in reviewed):
                    continue
                r = residual.setdefault(t, dict(token=t, morpheme=m, count=0, sample=f"{f}:{p} …{s[max(0, x - 20):y + 20]}…"))
                r["count"] += 1

    # ── 4. 노드 = 트리 + 추가 ──
    parent = {t["name"]: t["parent"] for t in TREE}
    for ad in DEC["node_additions"]:
        parent[ad["name"]] = ad["parent"]
    if set(DEC["nodes"]) != set(parent) or set(DEC["node_ids"]) != set(parent):
        err("노드 목록", "nodes · node_ids 와 트리 + node_additions 가 다름",
            only_decisions=sorted(set(DEC["nodes"]) - set(parent)), only_tree=sorted(set(parent) - set(DEC["nodes"])))

    # ── 5. 결정 행 ↔ 재추출 ──
    route = {}
    for s in DEC["strings"]:
        k = tuple(s["key"])
        if k in route:
            err("결정 중복", f"strings 키 {list(k)} 두 번")
        route[k] = s
    oos = {tuple(x["key"]): x for x in DEC.get("strings_out_of_scope", {}).get("strings", [])}
    for k in sorted(found, key=lambda k: (k[1], k[0])):
        if k not in route:
            c = found[k]
            o = dict(type="결정 없는 문자열", key=list(k), string=c["variants"].most_common(1)[0][0], count=c["count"], sample=c["samples"][:1])
            if k in oos:
                o["out_of_scope_decision"] = {x: oos[k].get(x) for x in ("destination", "nodes", "kind", "deferred_stage", "decided_by")}
            opened.append(o)
    for t in residual.values():
        opened.append(dict(type="사전 밖 부위 형태소", **t))
    stale = [list(k) for k in route if k not in found]

    weak_rows = []
    for k, s in route.items():
        bad = None
        if s["destination"] == "node":
            if not s.get("nodes") or any(n not in parent for n in s["nodes"]):
                bad = f"노드 {s.get('nodes')} 없음"
            elif bool(s.get("handoff")) != (s.get("kind") == D07):
                bad = f"kind {s.get('kind')} ↔ handoff {'있음' if s.get('handoff') else '없음'}"
        elif s["destination"] == "deferred":
            if not s.get("deferred_stage"):
                bad = "deferred 단계 없음"
        else:
            bad = f"destination {s['destination']}"
        if bad:
            err("행선지 오류", bad, key=list(k))
        if s.get("weak"):
            weak_rows.append(list(k))

    # ── 6. 노드 근거 · 전문의 용어 ──
    by_node = collections.defaultdict(list)
    for k, s in route.items():
        if s["destination"] == "node" and k in found:
            for n in s["nodes"]:
                by_node[n].append(k)
    no_basis, not_surface = [], []
    for name, na in DEC["nodes"].items():
        if not by_node.get(name) and not na.get("name_field_exception"):
            no_basis.append(name)
        if not na.get("anatomical_en") or not na.get("anatomical_level"):
            err("전문의 용어 없음", f"{name} anatomical_en · level 빈칸", node=name)
        hit = NOT_SURFACE_EN.findall(na.get("anatomical_en") or "") + NOT_SURFACE_KO.findall(na.get("anatomical_ko") or "")
        if hit:
            not_surface.append(dict(node=name, en=na.get("anatomical_en"), ko=na.get("anatomical_ko"), hit=hit))
    for n in no_basis:
        err("노드 근거 0", f"{n} — 이름 칸 문자열 0 · name_field_exception 없음", node=n)
    for x in not_surface:
        err("전문의 용어에 근육 · 뼈 · 혈관 표지", f"{x['node']}: {x['en']} · {x['ko']}", **x)
    danger = [z for z in DEC["danger_zone_mapping"] if DEC["nodes"].get(z["node"], {}).get("danger_zone") != z["zone"]]
    for z in danger:
        err("위험 부위 대응 불일치", f"{z['zone']} → {z['node']}")

    # ── 7. 원장 ↔ 재추출 · 결정 ──
    led = {(r["normalized"], r["group"]): r for r in LED["strings"]}
    drift = []
    for k, c in found.items():
        r = led.get(k)
        if r is None:
            drift.append(dict(key=list(k), what="원장에 행 없음"))
            continue
        if r["count"] != c["count"]:
            drift.append(dict(key=list(k), what=f"등장 원장 {r['count']} ≠ 재추출 {c['count']}"))
        s = route.get(k)
        if s and (r.get("destination") != s["destination"] or (r.get("nodes") or []) != (s.get("nodes") or []) or r.get("deferred_stage") != s.get("deferred_stage")):
            drift.append(dict(key=list(k), what="원장 행선지 ≠ 결정"))
    for k in led:
        if k not in found:
            drift.append(dict(key=list(k), what="원장에만 있음(원천에 없음)"))
    for d in drift:
        err("원장 낡음", f"{d['key']} {d['what']} — step3-apply.py 재실행 필요", key=d["key"])
    S = LED["summary"]
    counted = dict(strings=len(found), occurrences=sum(c["count"] for c in found.values()),
                   to_node=sum(1 for k in found if route.get(k, {}).get("destination") == "node"),
                   deferred=sum(1 for k in found if route.get(k, {}).get("destination") == "deferred"),
                   nodes=len(DEC["nodes"]), weak_strings=sum(1 for k in found if route.get(k, {}).get("weak")))
    ledger_said = dict(strings=S["strings"], occurrences=S["occurrences"], to_node=S["to_node"]["strings"], deferred=S["deferred"]["strings"],
                       nodes=S["nodes"], weak_strings=S["weak_strings"])
    for x in counted:
        if counted[x] != ledger_said[x]:
            err("summary 불일치", f"{x}: 원장 {ledger_said[x]} ≠ 다시 센 값 {counted[x]}")
    if LED["open"]:
        err("원장 open", f"step3-sites.json open {len(LED['open'])}")
    weak_q = {q["id"] for q in LED["doctor_questions"] if q["kind"].startswith("근거 약 문자열")}
    for k in weak_rows:
        if tuple(k) in found and f"{k[0]}|{k[1]}" not in weak_q:
            err("근거 약 질문 없음", f"{k} weak 인데 의료진 질문 없음", key=k)

    res = dict(
        source=dict(path=str(SRC), files=len(files), string_fields=len(src_all), name_fields=len(nf), name_field_cells=len(src)),
        counted=counted, ledger=ledger_said,
        kinds=dict(collections.Counter(route[k]["kind"] for k in found if k in route)),
        deferred_by_stage=dict(collections.Counter(route[k]["deferred_stage"] for k in found if route.get(k, {}).get("destination") == "deferred")),
        anatomical_level=dict(collections.Counter(n["anatomical_level"] for n in DEC["nodes"].values())),
        name_field_exception=[n for n, na in DEC["nodes"].items() if na.get("name_field_exception")],
        handoff_note_nodes=[n for n, na in DEC["nodes"].items() if na.get("handoff_note")],
        weak_strings=weak_rows,
        doctor_questions=len(LED["doctor_questions"]),
        open=opened, stale_decisions=stale, errors=errors,
        totals=dict(open=len(opened), stale=len(stale), errors=len(errors)))
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(txt)
    else:
        print(txt)
    print(json.dumps(dict(res["totals"], **counted), ensure_ascii=False), file=sys.stderr)
    return 0 if not errors and not opened else 1


if __name__ == "__main__":
    sys.exit(main())
