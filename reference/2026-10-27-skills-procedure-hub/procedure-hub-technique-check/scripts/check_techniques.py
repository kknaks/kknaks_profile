"""기법 원장 점검 — 지도가 4단계로 정한 원천 칸을 다시 펼쳐 step4-techniques.json · step4-decisions.json 과 맞춰 본다.

읽기만 한다. 원장(step4-techniques.json · .md) · 결정(step4-decisions.json) · 지도(source-map.json) · 앞 단계 정본 · 원천은 고치지 않는다 —
결과는 결정 목록의 재료다. 표준 라이브러리만 쓴다.

    python3 <이 파일> \
        --work orchestration/work/phub-recommend \
        --out <scratchpad>/technique-check.json        # --source <원천 폴더> 로 새 스냅샷을 볼 수 있다

본다(지금 원천 기준 — 가상 문장 시험은 하지 않는다. _RESUME §2 10-28 4단계 「끝 조건 지금 원천 open 0 · 가상 문장 시험 없음」):
- 지도 4단계 칸 재추출 — source-map.json fields 중 destinations.stage = 결정 source_map.stage 인 칸만 원천에서 펼친다
  - extracted ↔ taxonomy 글자 같은 줄 = 중복(결정 dedupe 규칙)
  - 펼쳤는데 결정 expressions[] 에 없는 (파일, 키, 원문) = open(결정 없는 표현)
  - 결정에 있는데 원천에 없는 표현 = stale
  - 지도 칸이 원천에서 0줄 = 오류(원천 키가 바뀌었나)
- 노드 — id 겹침 · 2층(상위가 있고 그 상위는 큰 기법) · 근거 칸 빈칸 · 근거 없는 노드(원천 표현 · 계열 기본 · 초안 · 세부 근거 다 없음)
- 값이 사전 안 — 표현 행 layers · muscles · attach · technique_hint pulse_mode · modes · ablative · pulse_scope(step2 보조 하위 계열) ·
  pulse_by_medium · modes → 노드 · 대상 근육 부위 · site_layer_split(부위 · 묶음 층) — 부위는 step3-sites.json 노드
- 계열 기본 18 = step2 계열 — 집합 같음 · 기본 · 보조 노드 있음 · 이름 같음
- 넘겨받은 것 — step2 · step3 이 4단계로 넘긴 것 전수가 handoffs[] 에 행선지를 갖나(step4-apply.py 와 같은 기준)
- technique_hint · 초안 65 — step2 hint 원문 · procedure-master-v3 techniques 와 결정이 같은가
- 원장 ↔ 재추출 — 원장 expressions[] 의 (파일, 키, 원문) · 수 · 묶음 · 노드가 다시 센 값과 같은지 · summary 셈 · open 0 · md 셈 줄

종료 코드: errors 0 · open 0 이면 0, 아니면 1.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

BUCKETS = {"속성", "넘김", "노드로"}
STAGES = {"2단계", "5단계", "7단계", "8단계", "계열 밖", "시맨틱"}


def txt(v) -> str:
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", required=True, help="orchestration/work/phub-recommend")
    ap.add_argument("--source", help="원천 폴더(없으면 결정 source.path)")
    ap.add_argument("--out", help="결과 JSON 경로(없으면 stdout)")
    a = ap.parse_args()

    W = Path(a.work)
    DEC = json.loads((W / "step4-decisions.json").read_text())
    LED = json.loads((W / "step4-techniques.json").read_text())
    SMAP = json.loads((W / DEC["source_map"]["file"]).read_text())
    S3D = json.loads((W / DEC["zone_site"]["file"]).read_text())
    S3 = json.loads((W / "step3-sites.json").read_text())
    S2 = json.loads((W / "step2-families.json").read_text())
    PM = json.loads((W / "procedure-master-v3.json").read_text())
    SRC = Path(a.source or DEC["source"]["path"])
    md_path = W / "step4-techniques.md"

    errors: list[dict] = []
    opened: list[dict] = []

    def err(kind: str, msg: str, **kw) -> None:
        errors.append(dict(kind=kind, msg=msg, **kw))

    # ── 1. 지도 4단계 칸 → 원천 줄 ──
    stage = DEC["source_map"]["stage"]
    cells = [f for f in SMAP["fields"] if any(d["stage"] == stage for d in f["destinations"])]
    LBL = DEC["index_label"]

    def expand(node, parts, prefix, out):
        if not parts:
            if isinstance(node, list):
                out.extend((prefix, txt(v)) for v in node)
            elif node is not None:
                out.append((prefix, txt(node)))
            return
        p, rest = parts[0], parts[1:]
        if p == "{code}":
            for k in node:
                expand(node[k], rest, k, out)
            return
        m = re.fullmatch(r"(\w+)\[\]", p)
        if m:
            name = m.group(1)
            for el in node.get(name, []) if isinstance(node, dict) else []:
                if LBL.get(name) not in el:
                    err("색인 칸 없음", f"{name} 원소에 {LBL.get(name)} 없음 — 결정 index_label 확인", cell=name)
                    continue
                expand(el, rest, f"{prefix + '.' if prefix else ''}{name}[{el[LBL[name]]}]", out)
            return
        if isinstance(node, dict) and p in node:
            expand(node[p], rest, f"{prefix + '.' if prefix else ''}{p}", out)

    raw: list[tuple] = []
    per_cell = {}
    src_cache: dict = {}
    for c in cells:
        fp = SRC / c["file"]
        if c["file"] not in src_cache:
            if not fp.exists():
                err("원천 파일 없음", f"{fp}", file=c["file"])
                src_cache[c["file"]] = None
            else:
                src_cache[c["file"]] = json.loads(fp.read_text())
        vals: list = []
        if src_cache[c["file"]] is not None:
            expand(src_cache[c["file"]], c["path"].split("."), "", vals)
        per_cell[f"{c['file']}#{c['path']}"] = len(vals)
        if not vals:
            err("지도 칸 0줄", f"{c['file']} {c['path']} 이 원천에 0줄 — 원천 키가 바뀌었나", cell=f"{c['file']}#{c['path']}")
        raw += [(c["file"], k, t) for k, t in vals]

    DD = DEC["dedupe"]
    against = collections.defaultdict(set)
    for f, k, t in raw:
        if f == DD["against_file"] and k.endswith(".extracted.related_techniques"):
            against[k.split(".")[0].removeprefix("modality[").rstrip("]")].add(t)
    rows, dup = [], collections.Counter()
    for f, k, t in raw:
        if f == DD["file"] and t in against.get(k.split(".")[0], ()):
            dup[k] += 1
            continue
        rows.append((f, k, t))
    cnt = collections.Counter(rows)
    uniq = list(dict.fromkeys(rows))

    # ── 2. 기준 목록 ──
    NODES = {}
    for n in DEC["nodes"]:
        if n["id"] in NODES:
            err("노드 id 겹침", n["id"])
        NODES[n["id"]] = n
    for n in DEC["nodes"]:
        if n["parent"] and (n["parent"] not in NODES or NODES[n["parent"]]["parent"]):
            err("노드 2층 넘음", f"{n['id']} 상위 {n['parent']} — 없거나 상위가 세부 기법", node=n["id"])
        if not (n.get("basis") or "").strip() or not n.get("medical_name"):
            err("노드 근거 · 의학 용어 빈칸", n["id"], node=n["id"])
    DI = DEC["dictionaries"]
    LAYERS, PULSE, ABL = set(DI["layer"]), set(DI["pulse_mode"]), set(DI["ablative"])
    MODES = {m["value"]: m for m in DI["modes"]}
    MUSCLES = {m["key"]: m for m in DI["target_muscle"]}
    SITES = {n["name"] for n in S3["nodes"]}
    ZONE_SITE = {z["zone"]: z["node"] for z in S3D["danger_zone_mapping"]}
    FAMS = {f["id"]: f for f in S2["families"]}

    for m in MUSCLES.values():
        for s in m["sites"]:
            if s not in SITES:
                err("값 사전 밖", f"대상 근육 {m['key']} 부위 {s} — 3단계 노드 아님", muscle=m["key"])
    for m in MODES.values():
        if m["node"] not in NODES:
            err("값 사전 밖", f"가능 방식 {m['value']} → 노드 {m['node']} 없음")
    for medium, ps in DEC["pulse_by_medium"].items():
        for p in ps:
            if p not in PULSE:
                err("값 사전 밖", f"pulse_by_medium {medium} {p} — pulse_mode 사전 밖")
    for sp in DEC["site_layer_split"]:
        if ZONE_SITE.get(sp["zone"]) != sp["group_site"]:
            err("층 나눔 오류", f"{sp['zone']} → {sp['group_site']} 가 3단계 danger_zone_mapping 과 다름")
        for s in sp["splits"]:
            if s["site"] not in SITES or not set(s["layers"]) <= set(sp["group_layers"]) or not set(s["layers"]) <= LAYERS:
                err("층 나눔 오류", f"{s['site']} {s['layers']} — 부위 없음 · 묶음 층 밖 · 층 사전 밖")

    # ── 3. 표현 행 ↔ 결정 ──
    route = {}
    for e in DEC["expressions"]:
        k = (e["file"], e["key"], e["text"])
        if k in route:
            err("결정 중복", f"expressions {list(k)} 두 번")
        route[k] = e

    def check_expr(e) -> str | None:
        if e["bucket"] not in BUCKETS:
            return f"묶음 {e['bucket']}"
        if e["bucket"] == "노드로" and e.get("node") not in NODES:
            return f"노드 {e.get('node')} 없음"
        if e["bucket"] == "넘김" and e.get("stage") not in STAGES:
            return f"넘김 단계 {e.get('stage')}"
        if e.get("node") and e["node"] not in NODES:
            return f"노드 {e['node']} 없음"
        for l in e.get("layers") or []:
            if l not in LAYERS:
                return f"층 {l} 사전 밖"
        if e.get("layers"):
            z = re.match(r"zones\[(\w+)\]", e["key"])
            if not z or z.group(1) not in ZONE_SITE:
                return "층 값인데 zone → 부위 대응 없음(3단계)"
        for m in e.get("muscles") or []:
            if m["muscle"] not in MUSCLES:
                return f"대상 근육 {m['muscle']} 사전 밖"
            if any(s not in SITES for s in m["sites"]):
                return f"부위 {m['sites']} 3단계 노드 아님"
        for x in e.get("attach") or []:
            if "muscle" in x and x["muscle"] not in MUSCLES:
                return f"근거 대상 근육 {x['muscle']} 사전 밖"
            if "layer" in x and (x["layer"] not in LAYERS or x.get("site") not in SITES):
                return f"근거 층 {x['layer']}@{x.get('site')} 사전 · 부위 밖"
        return None

    for f, k, t in uniq:
        e = route.get((f, k, t))
        if e is None:
            opened.append(dict(type="결정 없는 표현", file=f, key=k, text=t, count=cnt[(f, k, t)]))
            continue
        bad = check_expr(e)
        if bad:
            err("행선지 오류", bad, file=f, key=k, text=t)
    found = set(uniq)
    stale = [list(k) for k in route if k not in found]

    # ── 4. 넘겨받은 것(step4-apply.py §5 와 같은 기준) ──
    s3_def = {tuple(d["key"]) for d in S3["deferred"] if "4단계" in d["stage"]}
    s3_cmp = {(s["normalized"], s["group"]) for s in S3["strings"] if any("4단계" in h.get("stage", "") for h in (s["handoff"] or []))} - s3_def
    s3_note = {n["name"] for n in S3["nodes"] if n.get("handoff_note") and "4단계" in n["handoff_note"]}
    s3_str = {(s["normalized"], s["group"]) for s in S3["strings"]}
    s2_def = {f["id"] for f in S2["families"] for d in (f.get("deferred") or []) if "4단계" in str(d.get("deferred_to"))}
    s2_led = {x["ledger_id"] for x in S2["product_family"]}
    cov = collections.defaultdict(set)
    muscle_used = collections.Counter()
    for h in DEC["handoffs"]:
        r, ok = h["source_ref"], True
        t = r["type"]
        if t == "step3_deferred":
            ok = tuple(r["key"]) in s3_def
            cov["def"].add(tuple(r["key"]))
        elif t == "step3_compound":
            ok = all(tuple(x) in s3_cmp for x in r["keys"])
            cov["cmp"] |= {tuple(x) for x in r["keys"]}
        elif t == "step3_handoff_note":
            ok = r["node"] in s3_note
            cov["note"].add(r["node"])
        elif t == "step2_deferred":
            ok = r["family"] in s2_def
            cov["fam"].add(r["family"])
        elif t == "step2_ledger":
            ok = all(i in s2_led for i in r["ledger_ids"])
        elif t == "step3_string":
            ok = tuple(r["key"]) in s3_str
        if not ok:
            opened.append(dict(type="넘겨받은 것 원천 없음", id=h["id"], item=h["item"]))
        for m in h.get("muscles") or []:
            if m["muscle"] not in MUSCLES or not set(m["sites"]) <= set(MUSCLES[m["muscle"]]["sites"]):
                err("넘겨받은 것 값 오류", f"{h['id']} 대상 근육 {m['muscle']} @ {m['sites']} — 사전 · 부위 밖", id=h["id"])
            muscle_used[m["muscle"]] += 1
        for lm in h.get("landmarks") or []:
            if lm["site"] not in SITES:
                err("넘겨받은 것 값 오류", f"{h['id']} 주입 지표 부위 {lm['site']} 없음", id=h["id"])
    for src, have, cv in (("step3 deferred", s3_def, "def"), ("step3 부위+다른 축", s3_cmp, "cmp"),
                          ("step3 handoff_note", s3_note, "note"), ("step2 deferred 4단계", s2_def, "fam")):
        for k in sorted(have - cov[cv]):
            opened.append(dict(type="넘겨받은 것 행선지 없음", source=src, item=list(k) if isinstance(k, tuple) else k))

    for e in DEC["expressions"]:
        if (e["file"], e["key"], e["text"]) in found:
            for m in e.get("muscles") or []:
                muscle_used[m["muscle"]] += 1
            for x in e.get("attach") or []:
                if "muscle" in x:
                    muscle_used[x["muscle"]] += 1
    for k in MUSCLES:
        if not muscle_used[k]:
            err("근거 없는 대상 근육", f"{k} — 원천 행 · 근거 속성 · 넘겨받은 것 0", muscle=k)

    # ── 5. technique_hint(장비 속성) ──
    hint_src = {x["ledger_id"]: x for x in S2["product_family"] if x.get("technique_hint")}
    hint_dec = {h["ledger_id"]: h for h in DEC["technique_hints"]}
    for lid, s in hint_src.items():
        h = hint_dec.get(lid)
        if h is None:
            opened.append(dict(type="결정 없는 technique_hint", ledger_id=lid, hint=s["technique_hint"]))
            continue
        if h["hint"] != s["technique_hint"]:
            err("technique_hint 오류", f"{lid} 원천 hint {s['technique_hint']} ≠ 결정 {h['hint']}", ledger_id=lid)
        if any(p not in PULSE for p in h["pulse_mode"]) or any(m not in MODES for m in h["modes"]) or any(x["value"] not in ABL for x in h["ablative"]):
            err("값 사전 밖", f"technique_hint {lid} pulse_mode · modes · ablative", ledger_id=lid)
        if h.get("pulse_scope") and not any(x["sub_family"] in h["pulse_scope"] for x in s.get("also_sub_families") or []):
            err("technique_hint 오류", f"{lid} pulse_scope {h['pulse_scope']} — step2 보조 하위 계열에 없음", ledger_id=lid)
    stale += [["technique_hints", k] for k in hint_dec if k not in hint_src]
    scoped = [dict(ledger_id=h["ledger_id"], name=h["name"], pulse_mode=h["pulse_mode"], pulse_scope=h["pulse_scope"])
              for h in DEC["technique_hints"] if h.get("pulse_scope")]

    # ── 6. 계열 기본 기법 = step2 계열 ──
    fd = {f["family"]: f for f in DEC["family_defaults"]}
    for fid, fam in FAMS.items():
        f = fd.get(fid)
        if f is None:
            opened.append(dict(type="결정 없는 계열 기본 기법", family=fid, name=fam["name"]))
            continue
        if f["default"] not in NODES or any(x not in NODES for x in f["also"]):
            err("계열 기본 기법 오류", f"{fid} 노드 {f['default']} · {f['also']} 없음", family=fid)
        if f.get("family_name") != fam["name"]:
            err("계열 기본 기법 이름", f"{fid} 결정 {f.get('family_name')} ≠ step2 {fam['name']}", family=fid)
    stale += [["family_defaults", k] for k in fd if k not in FAMS]

    # ── 7. 초안 큰 기법 ──
    dd = {t["id"]: t for t in DEC["draft_techniques"]}
    pm_ids = set()
    for t in PM["techniques"]:
        pm_ids.add(t["id"])
        d = dd.get(t["id"])
        if d is None:
            opened.append(dict(type="결정 없는 초안 기법", id=t["id"], name=t["name"]))
        elif d["name"] != t["name"] or d["verdict"] not in ("유지", "합침", "버림") or (d["verdict"] != "버림" and d["node"] not in NODES):
            err("초안 기법 오류", f"{t['id']} {t['name']}", id=t["id"])
    stale += [["draft_techniques", k] for k in dd if k not in pm_ids]

    # ── 8. 노드 근거 ──
    def has(i: str) -> bool:
        return (any(e.get("node") == i and e["bucket"] == "노드로" and (e["file"], e["key"], e["text"]) in found for e in DEC["expressions"])
                or any(f["default"] == i or i in f["also"] for f in DEC["family_defaults"])
                or any(t["node"] == i and t["verdict"] != "버림" for t in DEC["draft_techniques"])
                or i in {m["node"] for m in MODES.values()})
    for i, n in NODES.items():
        if not has(i) and not any(has(c) for c, cn in NODES.items() if cn["parent"] == i):
            err("근거 없는 노드", f"{i} {n['name']}", node=i)

    # ── 9. 원장 ↔ 재추출 · summary · md ──
    led_rows = {(r["file"], r["key"], r["text"]): r for r in LED["expressions"] if r["bucket"] != "중복"}
    led_dup = {r["key"]: r["count"] for r in LED["expressions"] if r["bucket"] == "중복"}
    drift = []
    for k in uniq:
        r = led_rows.get(k)
        e = route.get(k)
        if r is None:
            drift.append(dict(key=list(k), what="원장에 행 없음"))
        elif r["count"] != cnt[k]:
            drift.append(dict(key=list(k), what=f"수 원장 {r['count']} ≠ 재추출 {cnt[k]}"))
        elif e and (r["bucket"] != e["bucket"] or r.get("node") != e.get("node") or r.get("stage") != e.get("stage")):
            drift.append(dict(key=list(k), what="원장 묶음 · 노드 · 단계 ≠ 결정"))
    for k in led_rows:
        if k not in found:
            drift.append(dict(key=list(k), what="원장에만 있음(원천에 없음)"))
    if dict(dup) != led_dup:
        drift.append(dict(key=["중복"], what=f"중복 묶음 원장 {led_dup} ≠ 재추출 {dict(dup)}"))
    for d in drift:
        err("원장 낡음", f"{d['key']} {d['what']} — step4-apply.py 재실행 필요", key=d["key"])

    bk = collections.Counter(route[k]["bucket"] for k in uniq if k in route)
    if dup:
        bk["중복"] = len(dup)
    counted = dict(cells=len(cells), lines=len(raw), values=len(uniq) + len(dup), unique_values=len(uniq), dup_groups=len(dup),
                   dup_lines=sum(dup.values()), nodes=len(NODES), by_bucket=dict(bk), family_defaults=len(fd), hints=len(hint_dec),
                   handoffs=len(DEC["handoffs"]), target_muscles=len(MUSCLES),
                   dictionaries={k: len(v) for k, v in DI.items() if k not in ("device_attrs", "unit_procedure_attrs")})
    S = LED["summary"]
    said = dict(cells=S["source"]["cells"], lines=S["source"]["lines"], values=S["source"]["values"], unique_values=S["source"]["unique_values"],
                dup_groups=S["source"]["dup_groups"], dup_lines=S["source"]["dup_lines"], nodes=S["nodes"], by_bucket=S["by_bucket"],
                family_defaults=S["family_defaults"], hints=S["hints"], handoffs=S["handoffs"], target_muscles=S["target_muscles"],
                dictionaries=S["dictionaries"])
    for x in counted:
        if counted[x] != said[x]:
            err("summary 불일치", f"{x}: 원장 {said[x]} ≠ 다시 센 값 {counted[x]}")
    if LED["open"]:
        err("원장 open", f"step4-techniques.json open {len(LED['open'])}", open=LED["open"])
    if md_path.exists():
        md = md_path.read_text()
        for pat, val in ((r"\*\*노드 (\d+)\*\*", S["nodes"]), (r"\*\*표현 (\d+)행\*\*", S["source"]["values"]), (r"\*\*open (\d+)\*\*", len(LED["open"]))):
            m = re.search(pat, md)
            if not m or int(m.group(1)) != val:
                err("md 셈 불일치", f"{pat} md {m.group(1) if m else '없음'} ≠ json {val} — md 를 손으로 고쳤거나 재실행 안 함")
    else:
        err("md 없음", str(md_path))

    fx = W / "step4-fixtures" / "result.json"
    fixture = None
    if fx.exists():
        r = json.loads(fx.read_text())
        fixture = dict(passed=r["passed"], total=r["total"])

    res = dict(
        source=dict(path=str(SRC), map_stage=stage, cells=len(cells), lines_per_cell=per_cell),
        counted=counted, ledger=said,
        nodes=[dict(id=i, name=n["name"], parent=n["parent"]) for i, n in NODES.items()],
        family_defaults={f: f"{x['default']}" + (f" (+{' · '.join(x['also'])})" if x["also"] else "") for f, x in fd.items()},
        pulse_scope_rows=scoped,
        fixture_result=fixture,
        open=opened, stale_decisions=stale, errors=errors,
        totals=dict(open=len(opened), stale=len(stale), errors=len(errors)))
    out = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out)
    else:
        print(out)
    print(json.dumps(dict(res["totals"], nodes=len(NODES), values=counted["values"], by_bucket=dict(bk)), ensure_ascii=False), file=sys.stderr)
    return 0 if not errors and not opened else 1


if __name__ == "__main__":
    sys.exit(main())
