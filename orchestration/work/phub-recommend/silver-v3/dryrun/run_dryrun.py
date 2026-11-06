#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""묶음5 432 자리 드라이런 — 규칙 R2→R1→R3→R4→S 로 몇 자리가 닫히나 센다(결정 아님 · 발주서 ../../silver-dryrun-brief.md).

python3 dryrun/run_dryrun.py            # 분석 → out-dryrun/dryrun.json · report.md (7차 확인 절은 verify 뒤 다시 쓴다)
python3 dryrun/run_dryrun.py --verify   # + 7차 불변 확인(build.py && check.py && tests/run_tests.py) 출력을 report §6 에

lib/ · out/ · decisions/ · baseline/ · build.py · ERD 파일 · 브론즈는 읽기만 한다. 이 프로세스 안에서만 lib.v32.AdverseUnits32 를 dry_au.DryAdverseUnits 로 바꿔 끼운다.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict

DRY = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(DRY)
ERD_DIR = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out-dryrun")
sys.path.insert(0, HERE)
sys.path.insert(0, DRY)

from lib import pipeline  # noqa: E402
from lib import v32 as V32  # noqa: E402
from lib.util import norm  # noqa: E402
import dry_au as DA  # noqa: E402

# ---------------------------------------------------------------------------
# 규칙 데이터(발주서 문장 그대로 · 괄호 꼴은 두 꼴 다)
# ---------------------------------------------------------------------------
R1_LISTED = ["장기간", "장기적", "임시", "일시", "일시적", "지속", "지속적", "영구", "영구적", "중등도", "중증", "심한", "경미", "경미한", "과도", "과도한", "이상", "불규칙",
             "미세", "미세한", "약간", "약간의", "광범위", "광범위한", "초기", "드문", "높음", "증가", "덜"]
R2_LISTED = ["신경", "하악변연신경", "안면신경", "감각신경", "눈", "안구", "결막", "눈썹", "눈꺼풀", "표정근", "근육", "두피", "피부", "진피", "혈관", "전신", "표면", "주사 부위", "시술 부위"]
S_RULES = {"suffix_감", "suffix_증", "suffix_형성"}
R1_CLASSES_138 = {"degree", "timing", "incidence"}


def sha_tree(d):
    h = hashlib.sha256()
    for root, _, fs in sorted(os.walk(d)):
        for f in sorted(fs):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, d).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def default_args():
    return argparse.Namespace(bronze=os.path.join(ERD_DIR, "bronze", "phub-ledger"), step1=os.path.join(ERD_DIR, "step1-products.json"), erd=os.path.join(ERD_DIR, "erd-v3.2.json"),
                              dict=os.path.join(ERD_DIR, "erd-v3.2-dictionaries.json"), colmap=os.path.join(ERD_DIR, "erd-v3.2-column-map.md"), tuples=os.path.join(ERD_DIR, "erd-v3.2-tuples.json"),
                              tuples_prev=os.path.join(ERD_DIR, "erd-v3.1-tuples.json"), decisions=os.path.join(HERE, "decisions"), seeds=os.path.join(ERD_DIR, "erd-v3.2-seed-candidates.json"),
                              out=os.path.join(HERE, "out"), baseline=os.path.join(HERE, "baseline", "manifest-1차.json"), bootstrap=False, propose=False, propose5_rules=False, propose4=False)


def capture_7th():
    """7차 파이프라인을 그대로 돌려(쓰기 없음) 마지막 분해 호출의 입력을 잡는다."""
    cap = []
    orig = V32.run_v32

    def rec(*a, **k):
        cap.append((a, k))
        return orig(*a, **k)
    V32.run_v32 = rec
    try:
        S = pipeline.run(default_args())
    finally:
        V32.run_v32 = orig
    return S, cap[-1]


def run_stage(call, r1, r2):
    DA.STATE = DA.DryState(r1, r2)
    orig = V32.AdverseUnits32
    V32.AdverseUnits32 = DA.DryAdverseUnits
    try:
        a, k = call
        P, A, C, X = V32.run_v32(*a, **k)
    finally:
        V32.AdverseUnits32 = orig
    return A, DA.STATE, dict(V32.CUR)


# ---------------------------------------------------------------------------
class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    opt = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    out_hash_before = sha_tree(os.path.join(HERE, "out"))

    # ---- 7차 상태 · 게이트 432
    S, call = capture_7th()
    A7 = S.ctx["adv"]
    gate = json.load(open(os.path.join(HERE, "out", "gate", "batch5.json"), encoding="utf-8"))
    G = {it["id"]: it for it in gate}
    ln_slots = G["ledger-nodes"]["subitems"]
    dup_slots = G["dup-strong"]["subitems"]
    seed_slots = [(gid, s) for gid in ("seed-site", "seed-ingredient_material", "seed-product_abbrev") for s in G[gid]["subitems"]]
    b3_slots = []
    for gid in ("m5-rename", "m16-technique", "site-synonyms", "air-embolism-qualifier", "records"):
        it = G[gid]
        b3_slots += [(gid, s) for s in it["subitems"]] if it.get("subitems") else [(gid, it)]
    n_slots = len(ln_slots) + len(dup_slots) + len(seed_slots) + len(b3_slots)

    # ---- 0 단계(규칙 없음) — 7차 재현 확인
    A0, ST0, _ = run_stage(call, [], [])
    nodes0 = OrderedDict((norm(n["canonical"]), n) for n in A0["ledger_events"])
    gate_nodes = [s["node"]["canonical"] for s in ln_slots]
    assert {norm(x) for x in gate_nodes} == set(nodes0), "0 단계 노드 ≠ 게이트 260"
    assert [n["canonical"] for n in A0["ledger_events"]] == [n["canonical"] for n in A7["ledger_events"]], "0 단계 ≠ 7차 분해"
    strong0 = [d for d in A0["duplicate_pairs"] if d["grade"] == "strong"]
    gate_pairs = [(s["pair"]["node"], s["pair"]["other"], s["pair"]["other_kind"], tuple(s["pair"]["rules"])) for s in dup_slots]
    assert {(norm(a), norm(b)) for a, b, _, _ in gate_pairs} == {(norm(d["new"]), norm(d["existing"])) for d in strong0}, "0 단계 ⑦ strong ≠ 게이트 96"
    base_surface = A0["base_surface"]                         # norm(사전 표면) → 정준값
    dict_canon = {norm(v): v for v in base_surface.values()}  # norm(정준값) → 정준값
    L = call[0][2]

    def dkey(name):
        """사건 이름 → 비교 키(사전이면 정준값의 norm)."""
        n = norm(name)
        return norm(base_surface[n]) if n in base_surface else n

    # ---- R2 단계 · R2+R1 단계
    A2, ST2, _ = run_stage(call, [], R2_LISTED)
    A21, ST21, CUR21 = run_stage(call, R1_LISTED, R2_LISTED)
    tk = CUR21["tok"]
    nodes2 = OrderedDict((norm(n["canonical"]), n) for n in A2["ledger_events"])
    nodes21 = OrderedDict((norm(n["canonical"]), n) for n in A21["ledger_events"])

    def mapping(nodes_prev, rec_prev, nodes_now, rec_now, hits, before_idx, after_idx):
        """이전 단계 노드 → 지금 단계 사건(이름). 뗀 기록(앞 → 뒤)이 먼저 · 없으면 자리마다 사건 칸 차이."""
        hb = defaultdict(set)
        for h in hits:
            if h[after_idx] is not None:
                hb[norm(h[before_idx])].add(h[after_idx])
        out = {}
        for k, n in nodes_prev.items():
            if k in nodes_now:
                out[k] = ("same", n["canonical"])
                continue
            if hb.get(k):
                tg = sorted({dkey(x) for x in hb[k]})
                names = sorted(hb[k])
                out[k] = ("hit", names[0]) if len(tg) == 1 else ("ambiguous", names)
                continue
            tg = set()
            for lc in n["locators"]:
                evp = {dkey(e) for e in rec_prev.get(lc, {}).get("events", [])}
                evn = {dkey(e) for e in rec_now.get(lc, {}).get("events", [])}
                new = evn - (evp - {k})
                tg.add(tuple(sorted(new)))
            if len(tg) == 1:
                t = next(iter(tg))
                out[k] = ("diff", t[0]) if len(t) == 1 else (("gone", None) if not t else ("ambiguous", list(t)))
            else:
                out[k] = ("ambiguous", sorted(str(x) for x in tg))
        return out

    f2 = mapping(nodes0, ST0.rec, nodes2, ST2.rec, ST2.r2_hits, 1, 2)
    # R1 단계: R2+R1 실행의 R1 기록은 (말, 앞뒤, R2 뒤 핵심어, R1 뒤 핵심어, …)
    f1 = mapping(nodes2, ST2.rec, nodes21, ST21.rec, ST21.r1_hits, 2, 3)

    def name_of(k):
        if k in nodes21:
            return nodes21[k]["canonical"]
        if k in nodes2:
            return nodes2[k]["canonical"]
        if k in nodes0:
            return nodes0[k]["canonical"]
        return dict_canon.get(k, k)

    # ---- R3 (R2+R1 뒤 노드)
    occ_events = {lc: {dkey(e) for e in r["events"]} for lc, r in ST21.rec.items()}
    cand = {k for k in nodes21 if ST21.solo_strict[k] == 0}
    D = set(cand)
    sole = {}
    changed = True
    while changed:
        changed = False
        for k in sorted(D):
            for lc in nodes21[k]["locators"]:
                others = occ_events.get(lc, set()) - {k} - D
                if not others:
                    D.discard(k)
                    sole[k] = (lc, ST21.rec.get(lc, {}).get("text"))
                    changed = True
                    break
    amb_r3 = {k for k in D if ST21.solo_loose[k] > 0}
    D_final = D - amb_r3
    # 단독 자리가 전부 괄호 안 묶음이고, 사건인 모든 자리에 다른 사건이 있으면 — 괄호 안 단독을 「그 말 하나로 쓰인」 것으로 볼지 애매
    amb_r3_paren = set()
    for k in nodes21:
        if k in D or ST21.solo_strict[k] == 0 or ST21.solo_strict[k] != ST21.solo_inner[k]:
            continue
        if all(occ_events.get(lc, set()) - {k} - D_final for lc in nodes21[k]["locators"]):
            amb_r3_paren.add(k)
    alive = [k for k in nodes21 if k not in D_final]

    # ---- R4 병기 쌍(괄호 앞 ↔ 괄호 안 · 둘 다 사건 키) — 7차 키 · 규칙 뒤 키
    texts = [t for t in V32.ledger_texts(L) if t[0] == "adverse"]

    SEP = re.compile(r"[·/,+:;—]|\s및\s|\s또는\s|--")
    r1w, r2w = {norm(w) for w in R1_LISTED}, {norm(w) for w in R2_LISTED}

    def strip_r(x):
        """R2(앞 · 뒤에 말이 더 있을 때) → R1(앞뒤) 를 낱말 단위로 뗀 꼴 — 병기 쌍이 규칙 뒤에만 생기는지 보려고."""
        t = x.split()
        while len(t) > 1 and DA._match(t[0], r2w, tk):
            t = t[1:]
        while len(t) > 1 and (DA._match(t[0], r1w, tk) or DA._match(t[-1], r1w, tk)):
            t = t[1:] if DA._match(t[0], r1w, tk) else t[:-1]
        return " ".join(t)

    def paren_pairs(keys, stripped=False):
        """R4 병기 — 멤버(구분자 · / , + : ; — 및 또는 -- 로 가른 토막) 안에서 「X (Y)」: X = 토막 처음부터 괄호까지 전부 · Y = 괄호 안(구분자 없음). 둘 다 사건 키이면 쌍."""
        out = OrderedDict()
        for ax, kind, f, p, lc, text, mod in texts:
            s_ = str(text)
            for mm in re.finditer(r"\(([^()]*)\)", s_):
                inner = mm.group(1).strip()
                if not inner or SEP.search(inner):
                    continue
                head = s_[: mm.start()]
                cut = max([x.end() for x in SEP.finditer(head)] + [head.rfind(")") + 1, 0])
                X = head[cut:].strip()
                if not X:
                    continue
                a, b = (strip_r(X), strip_r(inner)) if stripped else (X, inner)
                ka, kb = dkey(a), dkey(b)
                if ka in keys and kb in keys and ka != kb:
                    out.setdefault(tuple(sorted((ka, kb))), []).append((lc, s_))
        return out

    keys7 = set(dict_canon) | set(nodes0)
    keysF = set(dict_canon) | set(alive)
    P7 = paren_pairs(keys7)
    PF = paren_pairs(keysF)
    r4_amb = {}   # 7차 병기 쌍인데 한쪽이 규칙으로 바뀌어 규칙 뒤 키에서 쌍이 아님
    r4_amb_kind = defaultdict(lambda: "changed")
    for pr_, locs in P7.items():
        if pr_ not in PF and any(x in nodes0 for x in pr_):
            r4_amb[pr_] = locs
    PFs = paren_pairs(keysF, stripped=True)
    for pr_, locs in PFs.items():
        if pr_ not in PF and any(x in nodes21 for x in pr_):
            r4_amb[pr_] = locs        # R1/R2 로 뗀 뒤에만 병기 쌍 — 괄호 앞 범위가 애매
            r4_amb_kind[pr_] = "stripped"
    r4_pairs = {pr_: locs for pr_, locs in PF.items() if any(x in nodes21 for x in pr_) and not all(x in dict_canon for x in pr_)}

    # ---- S(23 쌍) — 두 끝이 규칙 뒤에도 그대로인 것만
    s_pairs, s_amb = [], []
    for a, b, bk, rules in gate_pairs:
        if not (set(rules) & S_RULES):
            continue
        ka, kb = norm(a), dkey(b)
        ok = (ka in nodes21 and ka not in D_final) and (kb in dict_canon or (kb in nodes21 and kb not in D_final))
        (s_pairs if ok else s_amb).append((a, b, bk, rules))

    # ---- 접기 묶음(R4 → S)
    uf4, ufs = UF(), UF()
    for (ka, kb) in r4_pairs:
        uf4.union(ka, kb)
        ufs.union(ka, kb)
    for a, b, bk, rules in s_pairs:
        ufs.union(norm(a), dkey(b))
    groups = defaultdict(list)
    for k in alive:
        groups[ufs.find(k)].append(k)
    for k in list(ufs.p):
        if k in dict_canon:
            r = ufs.find(k)
            if k not in groups[r]:
                groups[r].append(k)
    group_of = {k: r for r, ms in groups.items() for k in ms}

    def group_dicts(k):
        r = group_of.get(k)
        return [x for x in groups.get(r, []) if x in dict_canon] if r else []

    def n_locs(k):
        return len(nodes21[k]["locators"]) if k in nodes21 else 0

    kept = {}
    for r, ms in groups.items():
        ds = [x for x in ms if x in dict_canon]
        ns = [x for x in ms if x in nodes21]
        if ds:
            continue
        if len(ns) > 1:
            kept[r] = sorted(ns, key=lambda x: (-n_locs(x), name_of(x)))[0]

    def fold_rule(k):
        """k 가 접히면 그 규칙(R4|S) · 접히지 않으면 None."""
        r = group_of.get(k)
        ms = groups.get(r, [])
        if len(ms) < 2:
            return None
        if not group_dicts(k) and kept.get(r) == k:
            return None
        r4 = uf4.find(k)
        if any(uf4.find(x) == r4 for x in ms if x != k and (x in dict_canon or x == kept.get(r) or x in nodes21)):
            # R4 만으로 접힐 곳(사전 또는 남는 이름)에 닿는가
            tgt = group_dicts(k) or [kept.get(r)]
            if any(uf4.find(t) == r4 for t in tgt if t):
                return "R4"
        return "S"

    # ---- 글자 붙은 R1/R2 말(붙여쓰기) — 애매 표시용
    r1n = sorted({norm(w) for w in R1_LISTED if len(norm(w)) >= 2}, key=len, reverse=True)
    r2n = sorted({norm(w) for w in R2_LISTED if len(norm(w)) >= 2}, key=len, reverse=True)

    def glued(name):
        out = []
        for t in name.split():
            nt = norm(t)
            for w in r2n:
                if nt.startswith(w) and len(nt) - len(w) >= 2 and nt != w:
                    out.append(("R2", w, t))
                    break
            for w in r1n:
                if nt != w and len(nt) - len(w) >= 2 and (nt.startswith(w) or nt.endswith(w)):
                    out.append(("R1", w, t))
                    break
        return out

    r2_pred = defaultdict(list)
    for w, core, prs, lc, text in ST21.r2_before_pred:
        r2_pred[norm(core)].append((w, prs, text))
    r2_alone = defaultdict(list)
    for w, core, lc, text in ST21.r2_alone:
        r2_alone[norm(core)].append((w, text))
    r1_mid = defaultdict(list)
    for w, core, lc, text in ST21.r1_middle:
        r1_mid[norm(core)].append((w, text))

    def amb_reasons(k):
        """규칙 문장이 애매해 적용하지 않은 이유(노드 k · 규칙 뒤 이름)."""
        rs = []
        nm = name_of(k)
        if k in r2_pred:
            w, prs, text = r2_pred[k][0]
            rs.append(f"R2 말 「{w}」 뒤가 용언 꼴({' '.join(prs)})뿐 — 「사건 앞」인지 애매(「{text}」)")
        for kind, w, t in glued(nm):
            rs.append(f"{kind} 말 「{w}」가 띄어쓰기 없이 붙음(「{t}」) — 「앞뒤 말」인지 애매")
        if k in r1_mid:
            rs.append(f"R1 말 「{r1_mid[k][0][0]}」가 이름 가운데 — 「앞뒤」 아님")
        if k in amb_r3:
            rs.append(f"R3: 엄격 단독 0 · 느슨 단독 {ST21.solo_loose[k]}(정도·경과·빈도 밖 수식어까지 빼면 단독) — 「그 말 하나」 기준이 애매")
        if k in amb_r3_paren:
            rs.append(f"R3: 단독 {ST21.solo_strict[k]} 자리가 전부 괄호 안(「{ST21.solo_inner_texts[k][0]}」) · 모든 자리에 다른 사건 있음 — 괄호 안 단독을 「그 말 하나」로 볼지 애매")
        for pr_ in r4_amb:
            if k in pr_ or any(f2.get(x, ("", None))[1] and norm(f2[x][1]) == k for x in pr_ if x in f2):
                a, b = pr_
                tx = sorted({t for _, t in r4_amb[pr_]})[0]
                if r4_amb_kind[pr_] == "stripped":
                    rs.append(f"R4: 「{tx}」는 괄호 앞·안에서 R1/R2 말을 떼야만 「{name_of(a)}」=「{name_of(b)}」 병기 — 괄호 앞 범위가 애매")
                else:
                    rs.append(f"R4: 7차 병기 「{tx}」의 한쪽이 R2 로 (사건, 부위)가 됨 — 병기 쌍이 그 꼴과 같은지 애매")
        return rs

    # ---- 노드 자리 판정
    node_rows = []
    for s in ln_slots:
        nm = s["node"]["canonical"]
        k = norm(nm)
        n7 = len(nodes0[k]["locators"])
        how2, t2 = f2[k]
        row = OrderedDict([("slot", s["id"]), ("node", nm), ("n", n7), ("rule", None), ("to", None), ("why", None), ("ambiguous", [])])
        if how2 == "ambiguous":
            row["ambiguous"].append(f"R2 뒤 이 노드가 자리마다 다른 사건으로 갈림: {t2}")
        elif how2 != "same":
            row["rule"], row["to"] = "R2", t2
            node_rows.append(row)
            continue
        k2 = k
        how1, t1 = f1.get(k2, ("same", nm))
        if how1 == "ambiguous":
            row["ambiguous"].append(f"R1 뒤 자리마다 다른 사건으로 갈림: {t1}")
        elif how1 != "same":
            row["rule"], row["to"] = "R1", t1
            node_rows.append(row)
            continue
        if k in D_final:
            row["rule"], row["to"] = "R3", None
            node_rows.append(row)
            continue
        fr = fold_rule(k)
        if fr:
            gd = group_dicts(k)
            row["rule"], row["to"] = fr, (dict_canon[gd[0]] if gd else name_of(kept[group_of[k]]))
            node_rows.append(row)
            continue
        row["ambiguous"] += amb_reasons(k)
        node_rows.append(row)

    # ---- ⑦ strong 자리 판정
    strong2 = {tuple(sorted((dkey(d["new"]), dkey(d["existing"])))) for d in A2["duplicate_pairs"] if d["grade"] == "strong"}
    strong21 = {tuple(sorted((dkey(d["new"]), dkey(d["existing"])))) for d in A21["duplicate_pairs"] if d["grade"] == "strong"}

    def fmap(f, k):
        if k in dict_canon:
            return ("same", dict_canon[k])
        return f.get(k, ("same", name_of(k)))

    dup_rows = []
    for s, (a, b, bk, rules) in zip(dup_slots, gate_pairs):
        ka, kb = norm(a), dkey(b)
        row = OrderedDict([("slot", s["id"]), ("a", a), ("b", b), ("b_kind", bk), ("rules", list(rules)), ("rule", None), ("how", None), ("now", (a, b)), ("why", None), ("ambiguous", []), ("_changed", None), ("_k", None)])
        # R2
        ma, mb = fmap(f2, ka), fmap(f2, kb)
        if "ambiguous" in (ma[0], mb[0]):
            row["ambiguous"].append(f"R2 뒤 갈림: {ma} / {mb}")
        else:
            na, nb = dkey(ma[1]) if ma[1] else None, dkey(mb[1]) if mb[1] else None
            if (na, nb) != (ka, kb):
                if tuple(sorted((ka, kb))) in r4_amb:
                    row["ambiguous"].append(f"R4 병기 쌍인데 R2 로 한쪽이 (사건, 부위)가 됨: 「{name_of(ka)}」→「{ma[1]}」 / 「{name_of(kb)}」→「{mb[1]}」")
                elif na is None or nb is None or na == nb:
                    row["rule"], row["how"], row["now"] = "R2", "merged" if na == nb else "gone", (ma[1], mb[1])
                    dup_rows.append(row)
                    continue
                elif tuple(sorted((na, nb))) not in strong2:
                    row["rule"], row["how"], row["now"] = "R2", "dissolved", (ma[1], mb[1])
                    dup_rows.append(row)
                    continue
                ka, kb = na, nb
                row["_changed"] = "R2"
        if row["ambiguous"]:
            dup_rows.append(row)
            continue
        # R1
        ma, mb = fmap(f1, ka), fmap(f1, kb)
        if "ambiguous" in (ma[0], mb[0]):
            row["ambiguous"].append(f"R1 뒤 갈림: {ma} / {mb}")
            dup_rows.append(row)
            continue
        na, nb = dkey(ma[1]) if ma[1] else None, dkey(mb[1]) if mb[1] else None
        if (na, nb) != (ka, kb):
            if na is None or nb is None or na == nb:
                row["rule"], row["how"], row["now"] = "R1", "merged" if na == nb else "gone", (ma[1], mb[1])
                dup_rows.append(row)
                continue
            if tuple(sorted((na, nb))) not in strong21:
                row["rule"], row["how"], row["now"] = "R1", "dissolved", (ma[1], mb[1])
                dup_rows.append(row)
                continue
            ka, kb = na, nb
            row["_changed"] = "R1"
        row["now"] = (name_of(ka), name_of(kb))
        # R3
        if ka in D_final or kb in D_final:
            row["rule"], row["how"] = "R3", "dropped"
            dup_rows.append(row)
            continue
        if ka in amb_r3 or kb in amb_r3 or ka in amb_r3_paren or kb in amb_r3_paren:
            row["ambiguous"].append("R3 단독 기준 애매(한쪽)")
        # R4 · S
        if uf4.find(ka) == uf4.find(kb):
            row["rule"], row["how"] = "R4", "folded"
            dup_rows.append(row)
            continue
        if ufs.find(ka) == ufs.find(kb):
            row["rule"], row["how"] = "S", "folded"
            dup_rows.append(row)
            continue
        if set(rules) & S_RULES:
            row["ambiguous"].append("S 쌍인데 한쪽이 규칙으로 바뀌어 23 쌍 그대로가 아님")
        for k_ in (ka, kb):
            if k_ in nodes21:
                row["ambiguous"] += [f"「{name_of(k_)}」: {x}" for x in amb_reasons(k_) if not x.startswith("R3")]
        row["_k"] = (ka, kb)
        dup_rows.append(row)

    # 같은 쌍이 된 자리(규칙 뒤 묶음 기준) — 하나만 남기고 나머지는 그 쌍을 만든 규칙으로 닫는다
    by_g = defaultdict(list)
    for row in dup_rows:
        if row["rule"] or not row["_k"]:
            continue
        ka, kb = row["_k"]
        by_g[tuple(sorted((ufs.find(ka), ufs.find(kb))))].append(row)
    for gk, rows_ in by_g.items():
        if len(rows_) < 2:
            continue
        rows_.sort(key=lambda r: (r["_changed"] is not None or tuple(sorted((norm(r["a"]), dkey(r["b"])))) != tuple(sorted(r["_k"])), dup_rows.index(r)))
        keeper = rows_[0]
        for r in rows_[1:]:
            ka, kb = r["_k"]
            raw_same = tuple(sorted((ka, kb))) == tuple(sorted(keeper["_k"]))
            r4_same = tuple(sorted((uf4.find(ka), uf4.find(kb)))) == tuple(sorted((uf4.find(keeper["_k"][0]), uf4.find(keeper["_k"][1]))))
            r["rule"] = r["_changed"] if (r["_changed"] and raw_same) else ("R4" if r4_same else "S")
            r["how"] = f"duplicate_of:{keeper['a']}↔{keeper['b']}"

    # ---- 규칙 뒤 ⑦ strong 재계산(R3 버린 노드 빼고 · R4·S 로 같은 묶음 쌍 빼고)
    kr = CUR21["kinds"]
    live_nodes = OrderedDict((k, nodes21[k]) for k in alive)
    PFk = {pr_ for pr_ in PF}
    dupF = V32.duplicate_pairs(live_nodes, base_surface, kr, [tuple(p) for p in PFk])
    strongF = []
    seen = set()
    for d in dupF:
        if d["grade"] != "strong":
            continue
        ka, kb = dkey(d["new"]), dkey(d["existing"])
        if ufs.find(ka) == ufs.find(kb):
            continue
        key = tuple(sorted((ufs.find(ka), ufs.find(kb))))
        if key in seen:
            continue
        seen.add(key)
        strongF.append(d)
    def gk(a_, b_):
        return tuple(sorted((ufs.find(a_), ufs.find(b_))))
    remaining_dup_keys = {gk(*r["_k"]) for r in dup_rows if not r["rule"] and r["_k"]}
    F_keys = {gk(dkey(d["new"]), dkey(d["existing"])) for d in strongF}
    new_strong = [d for d in strongF if gk(dkey(d["new"]), dkey(d["existing"])) not in remaining_dup_keys]
    for r in dup_rows:
        r["in_recalc"] = bool(r["_k"]) and not r["rule"] and gk(*r["_k"]) in F_keys

    partners = defaultdict(list)
    for d in strongF:
        a_, b_ = dkey(d["new"]), dkey(d["existing"])
        partners[a_].append(f"{d['existing']}({'/'.join(d['rules'])})")
        partners[b_].append(f"{d['new']}({'/'.join(d['rules'])})")
    for r in node_rows:
        k = norm(r["node"])
        r["n_after"] = n_locs(k)
        r["name_after"] = name_of(k) if k in nodes21 else None
        r["solo_strict"], r["solo_loose"] = ST21.solo_strict[k], ST21.solo_loose[k]
        r["sole"] = sole[k][1] if k in sole else None
        r["partners"] = partners.get(k, [])
        toks = r["node"].split()
        r["edge_words"] = sorted({toks[0], toks[-1]}) if len(toks) > 1 else []
        gm = groups.get(group_of.get(k), [])
        r["group"] = [name_of(x) for x in gm if x != k] if len(gm) > 1 and not r["rule"] else []

    # ---- 새 노드(규칙이 세운 이름 · 260 에 없던 것)
    new_nodes = [k for k in alive if k not in nodes0 and not (len(groups.get(group_of.get(k), [])) > 1 and (group_dicts(k) or kept.get(group_of[k]) != k))]
    from_of = defaultdict(set)
    for h in ST2.r2_hits:
        if h[2]:
            from_of[dkey(h[2])].add(h[1])
    for h in ST21.r1_hits:
        if h[3]:
            from_of[dkey(h[3])].add(h[2])
    from_of = {k: sorted(v) for k, v in from_of.items()}

    # ---- 자리 수 표
    bundles = OrderedDict([("ledger-nodes", node_rows), ("dup-strong", dup_rows)])
    table = OrderedDict()
    for bname, rows in bundles.items():
        c = Counter(r["rule"] for r in rows if r["rule"])
        rem = [r for r in rows if not r["rule"]]
        table[bname] = OrderedDict([("slots", len(rows))] + [(x, c.get(x, 0)) for x in ("R2", "R1", "R3", "R4", "S")] + [("remaining", len(rem)), ("ambiguous", sum(1 for r in rem if r["ambiguous"]))])
    for bname, sl in (("seeds", seed_slots), ("batch3", b3_slots)):
        table[bname] = OrderedDict([("slots", len(sl))] + [(x, 0) for x in ("R2", "R1", "R3", "R4", "S")] + [("remaining", len(sl)), ("ambiguous", 0)])

    # ---- R1 표(원장 전수 · 사건 핵심어 앞뒤에 붙은 횟수)
    stop138 = {norm(w["word"]): w["class"] for w in call[0][1]["tuple_rules"]["adverse"]["adverse_stopwords"]["words"]}
    D_ = {d["name"]: d for d in call[0][0]["dictionaries"]}
    course_surface = {norm(v) for e in D_["course"]["entries"] for v in [e["canonical"]] + [x["value"] for x in e.get("synonyms", [])]}
    site_surface = {norm(v): e["canonical"] for e in D_["site"]["entries"] for v in [e["canonical"]] + [x["value"] for x in e.get("synonyms", [])]}
    rsite_surface = {norm(v): e["canonical"] for e in D_["relative_site"]["entries"] for v in [e["canonical"]] + [x["value"] for x in e.get("synonyms", [])]}
    ev_tokens = set()
    for s_ in base_surface:
        ev_tokens.add(s_)
    for k, n in list(nodes0.items()) + list(nodes21.items()):
        for t in n["canonical"].split():
            ev_tokens.add(norm(t))
    r1N = {norm(w) for w in R1_LISTED}
    adj = Counter()
    tok_total = Counter()
    for ax, kind, f, p, lc, text, mod in texts:
        toks = V32.raw_tokens(text)
        stems = []
        for t in toks:
            st = tk.strip(t, lambda s_: norm(s_) in ev_tokens or norm(s_) in r1N)
            stems.append(norm(st[0]) if st else norm(t))
        for i, t in enumerate(toks):
            w = DA._match(t, r1N, tk)
            if not w:
                continue
            tok_total[w] += 1
            if (i > 0 and stems[i - 1] in ev_tokens) or (i + 1 < len(toks) and stems[i + 1] in ev_tokens):
                adj[w] += 1
    r1_strip = Counter(h[0] for h in ST21.r1_hits)
    r1_nodes = defaultdict(set)
    for h in ST21.r1_hits:
        r1_nodes[h[0]].add(h[2])
    r1_table = []
    for w in R1_LISTED:
        k = norm(w)
        r1_table.append(OrderedDict([("word", w), ("in_138", stop138.get(k)), ("course_dict", k in course_surface), ("adjacent_to_event", adj[k]), ("token_total", tok_total[k]),
                                     ("stripped_in_dryrun", r1_strip[k]), ("from_names", sorted(r1_nodes[k]))]))
    # ---- R2 표
    r2_strip = Counter(h[0] for h in ST2.r2_hits)
    r2_names = defaultdict(set)
    for h in ST2.r2_hits:
        r2_names[h[0]].add((h[1], h[2]))
    r2_table = []
    for w in R2_LISTED:
        k = norm(w)
        ex = ("site:" + site_surface[k]) if k in site_surface else (("relative_site:" + rsite_surface[k]) if k in rsite_surface else None)
        r2_table.append(OrderedDict([("word", w), ("existing_dict", ex), ("temp_site", None if ex else f"tmp-site:{w}"), ("stripped_in_dryrun", r2_strip[k]), ("names", sorted(r2_names[k]))]))
    # ---- 앞뒤 말(규칙 밖 · 적용 안 함 · 사용자 참고)
    edge_other = Counter()
    edge_nodes = defaultdict(set)
    for r in node_rows:
        if r["rule"]:
            continue
        toks = r["node"].split()
        if len(toks) < 2:
            continue
        for t in (toks[0], toks[-1]):
            edge_other[t] += 1
            edge_nodes[t].add(r["node"])

    # ---- §5 사건 칸이 비는 문구
    rows21 = A21["phrase_rows"]
    empty = []
    st_cnt = Counter()
    for r in rows21:
        st_cnt[r["status"]] += 1
        if r["status"] in ("exact", "new"):
            ev = {dkey(e) for e in ST21.rec.get(r["locator"], {}).get("events", [])} - D_final
            if not ev:
                empty.append((r["locator"], r["text"]))
    st7 = Counter(r["status"] for r in A7["phrase_rows"])
    names_empty = []
    for r in A21["complications"]:
        ev = {dkey(e) for e in ST21.rec.get(r["locator"], {}).get("events", [])} - D_final
        if r.get("unit_ids") and not ev:
            names_empty.append((r["locator"], r["text"]))

    # ---- 저장
    res = OrderedDict([
        ("brief", "../../silver-dryrun-brief.md"), ("slots_total", n_slots), ("table", table),
        ("node_rows", node_rows), ("dup_rows", dup_rows),
        ("seed_slots", [(g, s["id"], s["title"]) for g, s in seed_slots]), ("b3_slots", [(g, s["id"], s.get("title")) for g, s in b3_slots]),
        ("r1_table", r1_table), ("r2_table", r2_table),
        ("r3_dropped", [OrderedDict([("node", name_of(k)), ("solo_strict", ST21.solo_strict[k]), ("solo_loose", ST21.solo_loose[k]), ("occurrences", [(lc, ST21.rec.get(lc, {}).get("text"), sorted(name_of(e) for e in occ_events.get(lc, set()) if e != k)) for lc in nodes21[k]["locators"]])]) for k in sorted(D_final, key=name_of)]),
        ("r3_sole_kept", [OrderedDict([("node", name_of(k)), ("locator", v[0]), ("text", v[1])]) for k, v in sorted(sole.items(), key=lambda kv: name_of(kv[0]))]),
        ("r3_ambiguous_paren", [OrderedDict([("node", name_of(k)), ("solo", ST21.solo_strict[k]), ("texts", sorted(set(ST21.solo_inner_texts[k])))]) for k in sorted(amb_r3_paren, key=name_of)]),
        ("r3_ambiguous", [OrderedDict([("node", name_of(k)), ("solo_loose", ST21.solo_loose[k]), ("contexts", ST21.seg_contexts[k][:3])]) for k in sorted(amb_r3, key=name_of)]),
        ("r4_pairs", [OrderedDict([("a", name_of(a)), ("b", name_of(b)), ("texts", sorted({t for _, t in locs}))]) for (a, b), locs in r4_pairs.items()]),
        ("r4_ambiguous", [OrderedDict([("a", name_of(a)), ("b", name_of(b)), ("kind", r4_amb_kind[(a, b)]), ("texts", sorted({t for _, t in locs}))]) for (a, b), locs in r4_amb.items()]),
        ("s_pairs", [OrderedDict([("a", a), ("b", b), ("b_kind", bk), ("rules", list(r)), ("kept", (dict_canon[group_dicts(norm(a))[0]] if group_dicts(norm(a)) else name_of(kept.get(group_of.get(norm(a)), norm(a)))))]) for a, b, bk, r in s_pairs]),
        ("s_ambiguous", [OrderedDict([("a", a), ("b", b), ("rules", list(r))]) for a, b, bk, r in s_amb]),
        ("groups", [OrderedDict([("members", [name_of(x) for x in ms]), ("dict", [dict_canon[x] for x in ms if x in dict_canon]), ("kept", name_of(kept[r]) if r in kept else None)]) for r, ms in groups.items() if len(ms) > 1]),
        ("nodes", OrderedDict([("dict_events", len(dict_canon)), ("nodes_7th", len(nodes0)), ("strong_7th", len(strong0)), ("weak_7th", sum(1 for d in A0["duplicate_pairs"] if d["grade"] == "weak")), ("nodes_after_R2", len(nodes2)), ("nodes_after_R2R1", len(nodes21)), ("r3_dropped", len(D_final)),
                               ("alive_after_R3", len(alive)), ("node_groups_after_R4S", sum(1 for r, ms in groups.items() if not any(x in dict_canon for x in ms))),
                               ("new_node_names", [OrderedDict([("node", name_of(k)), ("n", n_locs(k)), ("from", from_of.get(k, [])), ("solo_strict", ST21.solo_strict[k]), ("partners", partners.get(k, [])), ("ambiguous", amb_reasons(k))]) for k in sorted(new_nodes, key=lambda x: (-n_locs(x), name_of(x)))]),
                               ("dict_events_names", sorted(dict_canon.values())), ("erd_base_events", [e["canonical"] for e in json.load(open(os.path.join(ERD_DIR, "erd-v3.2-dictionaries.json"), encoding="utf-8"))["dictionaries"][[d["name"] for d in json.load(open(os.path.join(ERD_DIR, "erd-v3.2-dictionaries.json"), encoding="utf-8"))["dictionaries"]].index("adverse_event_type")]["entries"] if e.get("origin") not in ("ledger", "taxonomy")])])),
        ("strong_recalc", OrderedDict([("strong_after_rules", len(strongF)), ("of_which_new", len(new_strong)), ("weak_after_rules", sum(1 for d in dupF if d["grade"] == "weak")),
                                       ("new_pairs", [OrderedDict([("a", d["new"]), ("b", d["existing"]), ("b_kind", d["existing_kind"]), ("rules", d["rules"]), ("ambiguous", ["S 규칙 꼴(접미사)이지만 가정 S 는 23 쌍만"] if set(d["rules"]) & S_RULES else [])]) for d in new_strong]),
                                       ("remaining_slots_in_recalc", sum(1 for r in dup_rows if r.get("in_recalc"))), ("remaining_slots_not_in_recalc", [OrderedDict([("a", r["a"]), ("b", r["b"]), ("now", r["now"])]) for r in dup_rows if not r["rule"] and not r.get("in_recalc")]),
                                       ("all_pairs", [OrderedDict([("a", d["new"]), ("b", d["existing"]), ("b_kind", d["existing_kind"]), ("rules", d["rules"])]) for d in strongF])])),
        ("edge_words_outside_rules", [OrderedDict([("word", w), ("nodes", sorted(edge_nodes[w]))]) for w, _ in edge_other.most_common()]),
        ("phrases", OrderedDict([("occurrences", len(rows21)), ("by_status_after", dict(st_cnt)), ("by_status_7th", dict(st7)), ("empty_event_cell", empty), ("names_empty_event_cell", names_empty)])),
        ("r2_before_pred", [(w, c, p, t) for w, c, p, lc, t in ST21.r2_before_pred]), ("r2_alone", [(w, c, t) for w, c, lc, t in ST21.r2_alone]), ("r1_middle", [(w, c, t) for w, c, lc, t in ST21.r1_middle]),
        ("out_hash_before", out_hash_before), ("out_hash_after_analysis", sha_tree(os.path.join(HERE, "out"))),
    ])
    with open(os.path.join(OUT, "dryrun.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1, default=list)
    verify = None
    if opt.verify:
        cmd = "python3 build.py && python3 check.py && python3 tests/run_tests.py"
        p = subprocess.run(cmd, shell=True, cwd=HERE, capture_output=True, text=True)
        man = json.load(open(os.path.join(HERE, "out", "manifest.json"), encoding="utf-8"))
        base = json.load(open(os.path.join(HERE, "baseline", "manifest-7차.json"), encoding="utf-8"))
        verify = OrderedDict([("cmd", cmd), ("returncode", p.returncode), ("stdout", p.stdout), ("stderr", p.stderr), ("key_out", man.get("determinism_key")), ("key_baseline", base.get("determinism_key")),
                              ("out_hash_before", out_hash_before), ("out_hash_after_build", sha_tree(os.path.join(HERE, "out")))])
        with open(os.path.join(OUT, "verify-7차.json"), "w", encoding="utf-8") as fh:
            json.dump(verify, fh, ensure_ascii=False, indent=1)
    elif os.path.exists(os.path.join(OUT, "verify-7차.json")):
        verify = json.load(open(os.path.join(OUT, "verify-7차.json"), encoding="utf-8"))
    import render
    render.write(res, verify, os.path.join(OUT, "report.md"))
    print(json.dumps(table, ensure_ascii=False))


if __name__ == "__main__":
    main()
