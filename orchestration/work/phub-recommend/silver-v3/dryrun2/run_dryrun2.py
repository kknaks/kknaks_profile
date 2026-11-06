#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""드라이런 2차 — Kiwi 형태소 분석으로 부작용 핵심어를 다시 뽑아(T0~T4) 1차 규칙(R2→R1→R3→R4→S)과 함께 7차 260 노드가 몇 남나 센다.
발주서 ../../silver-dryrun2-brief.md · 결정 아님.

silver-v3/.venv-kiwi/bin/python dryrun2/run_dryrun2.py            # 분석 → out-dryrun2/dryrun2.json · report.md
silver-v3/.venv-kiwi/bin/python dryrun2/run_dryrun2.py --verify   # + 7차 불변 확인(시스템 python3 로 build.py && check.py && tests/run_tests.py)

lib/ · out/ · decisions/ · baseline/ · build.py · ERD 파일 · 브론즈 · dryrun/(1차) 는 읽기만 한다.
규칙 적용(셈) 순서: T3 → T4 → T2 → T1 → R2 → R1 → R3 → R4 → S · 겹치면 먼저 적용된 규칙에 센다.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict

DRY2 = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(DRY2)
ERD_DIR = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out-dryrun2")
sys.path.insert(0, HERE)
sys.path.insert(0, DRY2)

import common2 as C  # noqa: E402
from lib import v32 as V32  # noqa: E402
from lib.decompose import ADV_MEMBER_SPLIT, ADV_PAREN  # noqa: E402
from lib.util import norm  # noqa: E402
import dry2_au as D2  # noqa: E402
import kiwi_t0 as KT  # noqa: E402

ORDER = ["T3", "T4", "T2a", "T2b", "T1", "R2", "R1"]
USER_KINDS = {"T2b": "T2b", "T1-EF": "AMB", "T1-none": "AMB", "ANOM": "AMB", "T1-partial": "AMB", "T1-standalone": "AMB"}
GONE_CLOSED = {"T3", "T4", "T2a-rest"}


def sha_tree(d):
    h = hashlib.sha256()
    for root, _, fs in sorted(os.walk(d)):
        for f in sorted(fs):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, d).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


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
    S, call = C.capture_7th()
    A7 = S.ctx["adv"]
    dj, L = call[0][0], call[0][2]
    gate = json.load(open(os.path.join(HERE, "out", "gate", "batch5.json"), encoding="utf-8"))
    G = {it["id"]: it for it in gate}
    ln_slots = G["ledger-nodes"]["subitems"]
    dup_slots = G["dup-strong"]["subitems"]
    seed_slots = [(gid, s) for gid in ("seed-site", "seed-ingredient_material", "seed-product_abbrev") for s in G[gid]["subitems"]]
    b3_slots = []
    for gid in ("m5-rename", "m16-technique", "site-synonyms", "air-embolism-qualifier", "records"):
        it = G[gid]
        b3_slots += [(gid, s) for s in it["subitems"]] if it.get("subitems") else [(gid, it)]
    nodes0 = OrderedDict((norm(n["canonical"]), n) for n in A7["ledger_events"])
    assert {norm(s["node"]["canonical"]) for s in ln_slots} == set(nodes0), "7차 노드 ≠ 게이트 260"
    strong0 = [d for d in A7["duplicate_pairs"] if d["grade"] == "strong"]
    gate_pairs = [(s["pair"]["node"], s["pair"]["other"], s["pair"]["other_kind"], tuple(s["pair"]["rules"])) for s in dup_slots]
    assert {(norm(a), norm(b)) for a, b, _, _ in gate_pairs} == {(norm(d["new"]), norm(d["existing"])) for d in strong0}, "7차 ⑦ strong ≠ 게이트 96"
    base_surface = A7["base_surface"]
    dict_canon = {norm(v): v for v in base_surface.values()}

    def dkey(name):
        n = norm(name)
        return norm(base_surface[n]) if n in base_surface else n

    # ---- T0
    kt = KT.KiwiT0(dj)
    adv_texts = [t for t in V32.ledger_texts(L) if t[0] == "adverse"]
    t0_split = kt.split_check()
    t0_ctx = kt.context_split([t[5] for t in adv_texts])
    r2n = {norm(w): w for w in C.R2_LISTED}
    r1n = {norm(w): w for w in C.R1_LISTED}
    t0_r2_conflict = []
    for v, dns in kt.registered.items():
        nv = norm(v)
        hits = [w for k, w in r2n.items() if nv != k and (nv.startswith(k) or nv.endswith(k))]
        if hits:
            t0_r2_conflict.append(OrderedDict([("value", v), ("dictionaries", dns), ("r2_words", hits)]))
    t0_equal_r = [OrderedDict([("value", v), ("dictionaries", dns), ("as", "R2" if norm(v) in r2n else "R1")]) for v, dns in kt.registered.items() if norm(v) in r2n or norm(v) in r1n]
    t0 = OrderedDict([("dictionaries_used", [d["name"] for d in dj["dictionaries"]]), ("n_dictionaries_used", len(dj["dictionaries"])), ("not_registered_dictionary", "phrase_dictionary"),
                      ("event_entries", len([e for d in dj["dictionaries"] if d["name"] == "adverse_event_type" for e in d["entries"]])),
                      ("value_pairs", len(kt.values)), ("registered_unique", len(kt.registered)), ("skipped_no_letters", kt.skipped), ("failed", kt.failed),
                      ("by_dictionary", Counter(dn for dn, v in kt.values)), ("split_standalone", t0_split), ("split_in_context", [(v, t, m) for v, t, m in t0_ctx]),
                      ("r2_conflicts", t0_r2_conflict), ("registered_equal_r_words", t0_equal_r)])

    # ---- 2차 분해(T + R2 + R1)
    A2, ST, CUR2 = C.run_stage2(call, kt, C.R1_LISTED, C.R2_LISTED)
    nodes2 = OrderedDict((norm(n["canonical"]), n) for n in A2["ledger_events"])
    seglog = ST.seglog

    # 문구에 문장꼴 멤버가 있나(T2 범위 — 문구 단위 vs 멤버 단위)
    def phrase_sentence(text):
        """바깥 묶음(괄호 밖)의 멤버 중 「--」「—」「:」 앞쪽에 문장꼴이 있나 — 괄호 안은 T3 가 따로 다루고(괄호 안 문장꼴은 그 괄호만 T2), 구분자 뒤는 T4 가 이미 서술로 둔다."""
        outer = ADV_PAREN.sub(" ", text)
        dm = D2.T4_DELIM.search(outer)
        offs = D2.member_offsets(outer)
        parts = [p.strip() for p in ADV_MEMBER_SPLIT.split(outer) if p.strip()]
        for i, part in enumerate(parts):
            if dm and i < len(offs) and offs[i] > dm.start():
                continue
            if D2.sentence_info(kt, part, ST.r1)[0]:
                return True
        return False

    # 2차 노드 이름을 Kiwi 로 따로(이름 하나만) 다시 분석 — 조사·어미(J*·E*)가 나오면 분석기가 문맥마다 다르게 본 것(문맥 안 = 명사 · 이름 하나 = 용언+어미)
    #  → 그 노드는 T1 적용이 애매 — 노드로 세우지 않고 애매 — 사용자(노드 아님)로 센다
    bad_sa = OrderedDict()
    for k, n in nodes2.items():
        je = [(f, t) for f, t, a, b in kt.tokens(n["canonical"]) if t.startswith("J") or t.startswith("E")]
        if je:
            bad_sa[k] = [(f, t) for f, t, a, b in kt.tokens(n["canonical"])]
    for r in seglog:
        if r["kind"] == "node" and any(dkey(t) in bad_sa for t in r["target"]):
            r["kind"] = "T1-standalone"
            r["rules"] = (r["rules"] or []) + ([] if "T1" in r["rules"] else ["T1"])
            for t in r["target"]:
                if dkey(t) in bad_sa:
                    r["amb"].append(f"T1: 「{t}」 — 문맥 안에선 명사로 분석됐지만 이름 하나로는 {' '.join(f'{f}/{g}' for f, g in bad_sa[dkey(t)])} — 분석기 판정이 갈림 · 적용 안 함")
    for k in bad_sa:
        nodes2.pop(k)

    by7 = defaultdict(list)
    for r in seglog:
        if r["k7"][0] == "node":
            by7[norm(r["k7"][1])].append(r)
    for k, n in nodes0.items():
        assert sorted(set(n["locators"])) == sorted({r["loc"] for r in by7[k]}), f"7차 노드 자리 ≠ 2차 기록: {n['canonical']}"

    def entry_out(r):
        """→ (class, key, rule) · class = node|dict|closed|T2b|AMB|excluded."""
        kd = r["kind"]
        fr = r["rules"][0] if r["rules"] else None
        if kd == "excluded":
            return ("excluded", None, fr)
        if kd in ("node", "T2a-capture"):
            ks = [dkey(t) for t in r["target"]]
            cls = "dict" if all(k in dict_canon for k in ks) else "node"
            return (cls, ks, fr)
        if kd in GONE_CLOSED:
            return ("closed", None, fr)
        return (USER_KINDS[kd], None, fr)

    def first_rule(rs):
        rr = [x for x in rs if x]
        return sorted(rr, key=ORDER.index)[0] if rr else None

    # 7차 노드 → 2차(T·R2·R1 뒤)
    fT = {}
    for k, n in nodes0.items():
        es = by7[k]
        outs = [entry_out(r) for r in es]
        if any(c == "node" and k in ks for c, ks, _ in outs):
            fT[k] = ("same", k, None)
            continue
        closed = [(c, ks, fr) for c, ks, fr in outs if c in ("node", "dict", "closed")]
        if closed:
            tg = sorted({x for c, ks, fr in closed if ks for x in ks})
            rule = first_rule([fr for c, ks, fr in closed])
            if len(tg) == 1 and all(c != "closed" for c, ks, fr in closed):
                fT[k] = ("to", tg[0], rule)
            elif not tg:
                fT[k] = ("gone", None, rule)
            else:
                fT[k] = ("split", tg, rule)
            continue
        if any(c == "T2b" for c, _, _ in outs):
            fT[k] = ("T2b", None, "T2b")
        elif any(c == "AMB" for c, _, _ in outs):
            fT[k] = ("AMB", None, "T1")
        else:
            fT[k] = ("excluded", None, None)

    def name_of(k):
        if k in nodes2:
            return nodes2[k]["canonical"]
        if k in nodes0:
            return nodes0[k]["canonical"]
        return dict_canon.get(k, k)

    # ---- R3 (2차 노드)
    occ_events = {lc: {dkey(e) for e in r["events"]} for lc, r in ST.rec.items()}
    cand = {k for k in nodes2 if ST.solo_strict[k] == 0}
    Dset = set(cand)
    sole = {}
    changed = True
    while changed:
        changed = False
        for k in sorted(Dset):
            for lc in nodes2[k]["locators"]:
                others = occ_events.get(lc, set()) - {k} - Dset
                if not others:
                    Dset.discard(k)
                    sole[k] = (lc, ST.rec.get(lc, {}).get("text"))
                    changed = True
                    break
    amb_r3 = {k for k in Dset if ST.solo_loose[k] > 0}
    D_final = Dset - amb_r3
    amb_r3_paren = set()
    for k in nodes2:
        if k in Dset or ST.solo_strict[k] == 0 or ST.solo_strict[k] != ST.solo_inner[k]:
            continue
        if all(occ_events.get(lc, set()) - {k} - D_final for lc in nodes2[k]["locators"]):
            amb_r3_paren.add(k)
    alive = [k for k in nodes2 if k not in D_final]

    # ---- R4 병기 쌍
    SEP = re.compile(r"[·/,+:;—]|\s및\s|\s또는\s|--")

    def t1name(x, strip=False):
        toks = kt.tokens(x)
        ws = D2.ws_spans(x)
        if D2.sentence_info(kt, x, ST.r1)[0] or kt.anom.get(x):
            return None
        tw = [(f, tg, a, b, next((wi for wi, w in enumerate(ws) if w[0] <= a < w[1]), -1)) for f, tg, a, b in toks]
        units, dropped, _, _ = D2.noun_units(tw, ST.dict_values, ST.r1 | ST.r2, [w[2] for w in ws])
        if not units:
            return None
        sym = [t for t in tw if t[1] in ("SL", "SN", "SH") and norm(t[0]) not in ST.dict_values]
        if (dropped or sym) and not strip:
            return None       # 조사·어미 밖 내용 형태소(「심한」 등)를 버려야만 키가 되면 괄호 앞 범위가 애매 — 떼는 꼴(strip)에서만 본다
        if strip:
            units = D2.strip_r1(D2.strip_r2(units, ST.r2)[0], ST.r1)[0]
        return D2.join_units(units)

    def keyof(x, keys, strip=False):
        if not strip and dkey(x) in keys:
            return dkey(x)
        nm = t1name(x, strip)
        return dkey(nm) if nm and dkey(nm) in keys else None

    def paren_pairs(keys, strip=False, raw_only=False):
        out = OrderedDict()
        for ax, kind, f, p, lc, text, mod in adv_texts:
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
                if raw_only:
                    ka, kb = dkey(X), dkey(inner)
                    ka, kb = (ka if ka in keys else None), (kb if kb in keys else None)
                else:
                    ka, kb = keyof(X, keys, strip), keyof(inner, keys, strip)
                if ka and kb and ka != kb:
                    out.setdefault(tuple(sorted((ka, kb))), []).append((lc, s_))
        return out

    keys7 = set(dict_canon) | set(nodes0)
    keysF = set(dict_canon) | set(alive)
    P7 = paren_pairs(keys7, raw_only=True)
    PF = paren_pairs(keysF)
    PFs = paren_pairs(keysF, strip=True)
    r4_amb, r4_amb_kind = {}, {}
    for pr_, locs in P7.items():
        if pr_ in PF:
            continue
        m_ = []
        for x in pr_:
            if x in dict_canon:
                m_.append(x)
            else:
                st, tg, _ = fT.get(x, ("same", x, None))
                m_.append(x if st == "same" else (tg if st == "to" else None))
        if all(y is not None and (y in dict_canon or y in alive) for y in m_) and m_[0] != m_[1]:
            r4_amb[pr_] = locs
            r4_amb_kind[pr_] = "changed"
    for pr_, locs in PFs.items():
        if pr_ not in PF and any(x in nodes2 for x in pr_):
            r4_amb[pr_] = locs
            r4_amb_kind[pr_] = "stripped"
    r4_pairs = {pr_: locs for pr_, locs in PF.items() if any(x in nodes2 for x in pr_) and not all(x in dict_canon for x in pr_)}

    # ---- S(23 쌍) — 두 끝이 2차에도 그대로인 것만
    s_pairs, s_amb = [], []
    for a, b, bk, rules in gate_pairs:
        if not (set(rules) & C.S_RULES):
            continue
        ka, kb = norm(a), dkey(b)
        ok = (ka in nodes2 and ka not in D_final) and (kb in dict_canon or (kb in nodes2 and kb not in D_final))
        (s_pairs if ok else s_amb).append((a, b, bk, rules))

    # ---- 접기 묶음
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
        return len(nodes2[k]["locators"]) if k in nodes2 else 0

    kept = {}
    for r, ms in groups.items():
        ds = [x for x in ms if x in dict_canon]
        ns = [x for x in ms if x in nodes2]
        if not ds and len(ns) > 1:
            kept[r] = sorted(ns, key=lambda x: (-n_locs(x), name_of(x)))[0]

    def fold_rule(k):
        r = group_of.get(k)
        ms = groups.get(r, [])
        if len(ms) < 2:
            return None
        if not group_dicts(k) and kept.get(r) == k:
            return None
        r4 = uf4.find(k)
        tgt = group_dicts(k) or [kept.get(r)]
        if any(t and uf4.find(t) == r4 for t in tgt):
            return "R4"
        return "S"

    # ---- 애매 이유
    phrase_sent_cache = {}

    def psent(text):
        if text not in phrase_sent_cache:
            phrase_sent_cache[text] = phrase_sentence(text)
        return phrase_sent_cache[text]

    node_entries2 = defaultdict(list)    # 2차 노드 키 → 그 노드를 세운 2차 기록
    for r in seglog:
        if r["kind"] == "node":
            for t in r["target"]:
                node_entries2[dkey(t)].append(r)

    def amb_reasons(k):
        rs = []
        es = node_entries2.get(k, [])
        seen = set()
        for r in es:
            for a in r["amb"]:
                if a not in seen:
                    seen.add(a)
                    rs.append(a)
        t2p = [r for r in es if not r["sentence_words"] and psent(r["text"])]
        if t2p and len(t2p) == len(es):
            rs.append(f"T2 범위: 이 노드가 선 자리 {len(t2p)} 곳 전부 문구 안 다른 멤버가 문장꼴(「{t2p[0]['text']}」) — 문구 단위로 읽으면 서술, 멤버 단위로 읽어 노드로 둠")
        if k in amb_r3:
            rs.append(f"R3: 엄격 단독 0 · 느슨 단독 {ST.solo_loose[k]} — 「그 말 하나」 기준이 애매")
        if k in amb_r3_paren:
            rs.append(f"R3: 단독 {ST.solo_strict[k]} 자리가 전부 괄호 안(「{ST.solo_inner_texts[k][0]}」) · 모든 자리에 다른 사건 있음 — 괄호 안 단독을 「그 말 하나」로 볼지 애매")
        for pr_ in r4_amb:
            if k in pr_:
                a, b = pr_
                tx = sorted({t for _, t in r4_amb[pr_]})[0]
                if r4_amb_kind[pr_] == "stripped":
                    rs.append(f"R4: 「{tx}」는 괄호 앞·안에서 R1/R2 말을 떼야만 「{name_of(a)}」=「{name_of(b)}」 병기 — 괄호 앞 범위가 애매")
                else:
                    rs.append(f"R4: 7차 병기 「{tx}」의 한쪽이 T·R 규칙으로 바뀜 — 병기 쌍이 그 꼴과 같은지 애매")
        return rs

    # ---- 노드 자리 판정(260)
    node_rows = []
    for s in ln_slots:
        nm = s["node"]["canonical"]
        k = norm(nm)
        es = by7[k]
        dest = Counter()
        for r in es:
            c, ks, fr = entry_out(r)
            if c in ("node", "dict"):
                lab = ("사전 사건 「" + ", ".join(dict_canon[x] for x in ks) + "」") if c == "dict" else ("노드 「" + ", ".join(name_of(x) for x in ks) + "」")
                dest[f"{'/'.join(r['rules']) or '그대로'} → {lab}"] += 1
            else:
                dest[f"{'/'.join(r['rules']) or '-'} → {r['kind']}"] += 1
        row = OrderedDict([("slot", s["id"]), ("node", nm), ("n", len(nodes0[k]["locators"])), ("rule", None), ("bucket", None), ("to", None), ("ambiguous", []), ("dest", dict(dest))])
        st, tg, rule = fT[k]
        if st in ("to", "gone", "split"):
            row["rule"], row["to"] = rule, (name_of(tg) if st == "to" else ([name_of(x) for x in tg] if st == "split" else None))
            row["how"] = st
            node_rows.append(row)
            continue
        if st in ("T2b", "AMB"):
            row["bucket"] = st
            row["ambiguous"] = sorted({a for r in es for a in r["amb"]}) if st == "AMB" else []
            node_rows.append(row)
            continue
        if st == "excluded":
            row["rule"] = "excluded"
            node_rows.append(row)
            continue
        if k in D_final:
            row["rule"] = "R3"
            node_rows.append(row)
            continue
        fr = fold_rule(k)
        if fr:
            gd = group_dicts(k)
            row["rule"], row["to"] = fr, (dict_canon[gd[0]] if gd else name_of(kept[group_of[k]]))
            node_rows.append(row)
            continue
        row["ambiguous"] = amb_reasons(k)
        node_rows.append(row)

    # ---- ⑦ strong 96
    strongT = {tuple(sorted((dkey(d["new"]), dkey(d["existing"])))) for d in A2["duplicate_pairs"] if d["grade"] == "strong"}

    def fmapT(k):
        if k in dict_canon:
            return ("same", k, None)
        return fT.get(k, ("same", k, None))

    dup_rows = []
    for s, (a, b, bk, rules) in zip(dup_slots, gate_pairs):
        ka, kb = norm(a), dkey(b)
        row = OrderedDict([("slot", s["id"]), ("a", a), ("b", b), ("b_kind", bk), ("rules", list(rules)), ("rule", None), ("bucket", None), ("how", None), ("now", (a, b)), ("ambiguous", []), ("_changed", None), ("_k", None)])
        ma, mb = fmapT(ka), fmapT(kb)
        if "split" in (ma[0], mb[0]):
            row["ambiguous"].append(f"T·R 뒤 한쪽이 자리마다 다른 사건으로 갈림: {ma[1] if ma[0] == 'split' else mb[1]}")
            dup_rows.append(row)
            continue
        if ma[0] in ("T2b", "AMB") or mb[0] in ("T2b", "AMB"):
            row["bucket"] = "T2b" if "T2b" in (ma[0], mb[0]) else "AMB"
            row["how"] = "한쪽이 노드 아님(" + "/".join(x[0] for x in (ma, mb) if x[0] in ("T2b", "AMB")) + ")"
            dup_rows.append(row)
            continue
        na = ma[1] if ma[0] in ("same", "to") else None
        nb = mb[1] if mb[0] in ("same", "to") else None
        if (na, nb) != (ka, kb):
            rule = first_rule([x[2] for x in (ma, mb) if x[0] not in ("same",)])
            if na is None or nb is None or na == nb:
                row["rule"], row["how"], row["now"] = rule, "merged" if na == nb else "gone", (name_of(na) if na else None, name_of(nb) if nb else None)
                dup_rows.append(row)
                continue
            if tuple(sorted((na, nb))) not in strongT:
                row["rule"], row["how"], row["now"] = rule, "dissolved", (name_of(na), name_of(nb))
                dup_rows.append(row)
                continue
            ka, kb = na, nb
            row["_changed"] = rule
        row["now"] = (name_of(ka), name_of(kb))
        if ka in D_final or kb in D_final:
            row["rule"], row["how"] = "R3", "dropped"
            dup_rows.append(row)
            continue
        if ka in amb_r3 or kb in amb_r3 or ka in amb_r3_paren or kb in amb_r3_paren:
            row["ambiguous"].append("R3 단독 기준 애매(한쪽)")
        if uf4.find(ka) == uf4.find(kb):
            row["rule"], row["how"] = "R4", "folded"
            dup_rows.append(row)
            continue
        if ufs.find(ka) == ufs.find(kb):
            row["rule"], row["how"] = "S", "folded"
            dup_rows.append(row)
            continue
        if set(rules) & C.S_RULES:
            row["ambiguous"].append("S 쌍인데 한쪽이 규칙으로 바뀌어 23 쌍 그대로가 아님")
        for k_ in (ka, kb):
            if k_ in nodes2:
                row["ambiguous"] += [f"「{name_of(k_)}」: {x}" for x in amb_reasons(k_) if not x.startswith("R3")]
        row["_k"] = (ka, kb)
        dup_rows.append(row)
    by_g = defaultdict(list)
    for row in dup_rows:
        if row["rule"] or row["bucket"] or not row["_k"]:
            continue
        by_g[tuple(sorted((ufs.find(row["_k"][0]), ufs.find(row["_k"][1]))))].append(row)
    for gk_, rows_ in by_g.items():
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

    # ---- 규칙 뒤 ⑦ strong 재계산
    kr = CUR2["kinds"]
    live_nodes = OrderedDict((k, nodes2[k]) for k in alive)
    dupF = V32.duplicate_pairs(live_nodes, base_surface, kr, [tuple(p) for p in PF])
    strongF, seen = [], set()
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
    remaining_dup_keys = {gk(*r["_k"]) for r in dup_rows if not r["rule"] and not r["bucket"] and r["_k"]}
    F_keys = {gk(dkey(d["new"]), dkey(d["existing"])) for d in strongF}
    new_strong = [d for d in strongF if gk(dkey(d["new"]), dkey(d["existing"])) not in remaining_dup_keys]
    for r in dup_rows:
        r["in_recalc"] = bool(r["_k"]) and not r["rule"] and not r["bucket"] and gk(*r["_k"]) in F_keys
    partners = defaultdict(list)
    for d in strongF:
        a_, b_ = dkey(d["new"]), dkey(d["existing"])
        partners[a_].append(f"{d['existing']}({'/'.join(d['rules'])})")
        partners[b_].append(f"{d['new']}({'/'.join(d['rules'])})")

    # ---- 남는 노드 정보
    for r in node_rows:
        k = norm(r["node"])
        r["n_after"] = n_locs(k)
        r["name_after"] = name_of(k) if k in nodes2 else None
        r["solo_strict"], r["solo_loose"] = ST.solo_strict[k], ST.solo_loose[k]
        r["sole"] = sole[k][1] if k in sole else None
        r["partners"] = partners.get(k, [])
        gm = groups.get(group_of.get(k), [])
        r["group"] = [name_of(x) for x in gm if x != k] if len(gm) > 1 and not r["rule"] and not r["bucket"] else []
        r["example"] = (by7[k][0]["text"] if by7[k] else None)

    # ---- 2차가 새로 세운 노드 이름(260 에 없던 것) · 남는 새 노드 전부(최종 묶음)
    def is_kept_name(k):
        gm = groups.get(group_of.get(k), [])
        return not (len(gm) > 1 and (group_dicts(k) or kept.get(group_of[k]) != k))
    new_names = [k for k in alive if k not in nodes0 and is_kept_name(k)]
    from_of = defaultdict(set)
    for r in seglog:
        if r["kind"] == "node":
            for t in r["target"]:
                if dkey(t) not in nodes0:
                    from_of[dkey(t)].add(r["core7"])
    final_nodes = [k for k in alive if is_kept_name(k)]

    # ---- 조사·어미 검사(남는 새 노드 전부) — 이름을 Kiwi 로 다시 분석 · J*/E* 형태소가 하나라도 있으면 실패
    pe_check = []
    for k in final_nodes:
        nm = name_of(k)
        toks = kt.tokens(nm)
        je = [(f, t) for f, t, a, b in toks if t.startswith("J") or t.startswith("E")]
        built = [r["core7"] for r in node_entries2.get(k, [])]
        pe_check.append(OrderedDict([("node", nm), ("morphs", [(f, t) for f, t, a, b in toks]), ("particle_or_ending", je), ("anomaly", kt.anom.get(nm, []))]))
    pe_fail = [x for x in pe_check if x["particle_or_ending"]]

    # ---- 자리 수 표
    COLS = ["T3", "T4", "T2a", "T1", "R2", "R1", "R3", "R4", "S", "excluded"]
    table = OrderedDict()
    for bname, rows in (("ledger-nodes", node_rows), ("dup-strong", dup_rows)):
        c = Counter(r["rule"] for r in rows if r["rule"])
        rem = [r for r in rows if not r["rule"] and not r["bucket"]]
        table[bname] = OrderedDict([("slots", len(rows))] + [(x, c.get(x, 0)) for x in COLS] + [("closed", sum(c.values())), ("T2b_user", sum(1 for r in rows if r["bucket"] == "T2b")),
                                   ("amb_nonnode_user", sum(1 for r in rows if r["bucket"] == "AMB")), ("remaining", len(rem)), ("remaining_ambiguous", sum(1 for r in rem if r["ambiguous"]))])
    for bname, sl in (("seeds", seed_slots), ("batch3", b3_slots)):
        table[bname] = OrderedDict([("slots", len(sl))] + [(x, 0) for x in COLS] + [("closed", 0), ("T2b_user", 0), ("amb_nonnode_user", 0), ("remaining", len(sl)), ("remaining_ambiguous", 0)])

    # ---- 1차 대조
    R1J = json.load(open(os.path.join(HERE, "out-dryrun", "dryrun.json"), encoding="utf-8"))
    first_remaining = [r for r in R1J["node_rows"] if not r["rule"]]
    row2 = {r["node"]: r for r in node_rows}

    def dest_class(r):
        """2차에서 1차 남음 노드가 어디로 갔나(분류)."""
        if not r["rule"] and not r["bucket"]:
            return None
        if r["bucket"] == "T2b":
            return "문장꼴 — 사용자(T2b)"
        if r["bucket"] == "AMB":
            return "애매 — 사용자(노드 아님 · " + ", ".join(sorted({x.split(':')[0] for x in r["ambiguous"]})) + ")"
        rl = r["rule"]
        if rl == "T3":
            return "괄호(T3)"
        if rl == "T4":
            return "서술(T4 · 「--」「—」「:」 뒤)"
        if rl == "T2a":
            return "문장꼴 (a) — 사전 사건으로 합류 또는 서술" if r.get("to") else "문장꼴 (a) — 서술"
        if rl == "R3":
            return "조각 버림(R3 · 보존 목록)"
        to = r.get("to")
        tos = to if isinstance(to, list) else ([to] if to else [])
        if tos and all(norm(t) in dict_canon or dkey(t) in dict_canon for t in tos):
            return f"사전 사건으로 합류({rl})"
        if rl == "R2":
            return "부위로(R2) → 노드 「" + ", ".join(tos) + "」"
        return f"다른 노드 이름으로({rl}) → 「" + ", ".join(tos) + "」"
    vanished = []
    stayed = []
    for r1 in first_remaining:
        r = row2[r1["node"]]
        dc = dest_class(r)
        if dc:
            vanished.append(OrderedDict([("node", r1["node"]), ("n", r1["n"]), ("first_ambiguous", bool(r1["ambiguous"])), ("rule2", r["rule"] or r["bucket"]), ("to", r.get("to")), ("class", dc), ("dest", r["dest"])]))
        else:
            stayed.append(r1["node"])
    no_reason = [v for v in vanished if not v["class"]]
    first_closed_now_remaining = []
    for r1 in R1J["node_rows"]:
        if r1["rule"]:
            r = row2[r1["node"]]
            if not r["rule"] and not r["bucket"]:
                first_closed_now_remaining.append(OrderedDict([("node", r1["node"]), ("rule1", r1["rule"]), ("to1", r1["to"]), ("why2", r["ambiguous"] or ("2차 규칙으로 안 닫힘 — 발주서대로 R1 에서 「이상」을 뺐다" if r1["rule"] == "R1" and "이상" in r1["node"] else "2차 규칙으로 안 닫힘")), ("name_after", r["name_after"])]))

    # ---- §3 T2 문장꼴 문구 전수 · §4 T3 괄호 전수 · §7 사건 칸
    def t2_shape(text):
        """문장꼴 멤버가 명사로 끝나나(용언이 명사를 꾸미기만 — 「가벼운 출혈」「드물게 X」) · 용언으로 끝나나(「…사라짐」「…생길 수 있음」)."""
        out = set()
        outer = ADV_PAREN.sub(" ", text)
        for g in [outer] + ADV_PAREN.findall(text):
            for part in ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part or not D2.sentence_info(kt, part, ST.r1)[0]:
                    continue
                cont = [t for t in kt.tokens(part) if not (t[1].startswith("J") or t[1].startswith("E") or t[1].startswith("S"))]
                out.add("명사로 끝남(용언은 꾸밈)" if cont and cont[-1][1] in ("NNG", "NNP", "NNB", "XSN", "SL") else "용언으로 끝남")
        return sorted(out)

    # T4 구분자 뒤에 Kiwi 가 사전 사건 NNG 로 본 말(7차 사전 일치는 지우지 않았다 — 기록만)
    t4_dict_after = []
    for ph in list(A2["phrase_rows"]) + [dict(locator=r["locator"], text=r["text"]) for r in A2["complications"]]:
        text = ph["text"]
        for g in [ADV_PAREN.sub(" ", text)] + ADV_PAREN.findall(text):
            dm = D2.T4_DELIM.search(g)
            if not dm:
                continue
            after = g[dm.end():]
            ds = [t[0] for t in kt.tokens(after) if t[1] in KT.NOUN_TAGS and norm(t[0]) in base_surface]
            if ds:
                t4_dict_after.append((ph["locator"], text, after.strip(), ds))

    seg_by_loc = defaultdict(list)
    for r in seglog:
        seg_by_loc[r["loc"]].append(r)
    rows2 = A2["phrase_rows"]
    t2_rows = OrderedDict()
    for ph in rows2:
        text = ph["text"]
        if not psent(text):
            continue
        evs = ST.rec.get(ph["locator"], {}).get("events", [])
        segs = seg_by_loc.get(ph["locator"], [])
        e = t2_rows.setdefault(text, OrderedDict([("text", text), ("status7", ph["status"]), ("n", 0), ("locators", []), ("dict_events", []), ("captured", []), ("site", []), ("predicates", []),
                                                  ("outcomes", []), ("class", None)]))
        e["n"] += 1
        e["locators"].append(ph["locator"])
        if e["n"] > 1:
            continue
        e["dict_events"] = sorted({x for x in evs if dkey(x) in dict_canon})
        e["captured"] = sorted({t for r in segs if r["kind"] == "T2a-capture" for t in r["target"]})
        e["site"] = sorted({s_ for r in segs for s_ in r["site"]})
        outer = ADV_PAREN.sub(" ", text)
        preds = []
        for g in [outer] + ADV_PAREN.findall(text):
            for part in ADV_MEMBER_SPLIT.split(g):
                if part.strip():
                    preds += D2.sentence_info(kt, part.strip(), ST.r1)[1]
        e["predicates"] = preds
        e["outcomes"] = sorted({r["kind"] for r in segs})
        e["shape"] = t2_shape(text)
        e["class"] = D2.classify_remainder(" ".join(preds) + " " + text)
        e["t2"] = "(a)" if (e["dict_events"] or e["captured"]) else "(b)"
        if ph["status"] in ("note", "sentence"):
            e["t2"] = f"— (7차 {ph['status']} · 분해·단위 없음)"
    for nm_ in [r for r in A2["complications"]]:
        text = nm_["text"]
        if psent(text):
            e = t2_rows.setdefault(text, OrderedDict([("text", text), ("status7", "complication_name"), ("n", 0), ("locators", []), ("dict_events", []), ("captured", []), ("site", []), ("predicates", []), ("outcomes", []), ("class", None)]))
            e["n"] += 1
            e["locators"].append(nm_["locator"])
            segs = seg_by_loc.get(nm_["locator"], [])
            evs = ST.rec.get(nm_["locator"], {}).get("events", [])
            e["dict_events"] = sorted({x for x in evs if dkey(x) in dict_canon})
            e["captured"] = sorted({t for r in segs if r["kind"] == "T2a-capture" for t in r["target"]})
            e["site"] = sorted({s_ for r in segs for s_ in r["site"]})
            e["predicates"] = D2.sentence_info(kt, text, ST.r1)[1]
            e["outcomes"] = sorted({r["kind"] for r in segs})
            e["shape"] = t2_shape(text)
            e["class"] = D2.classify_remainder(text)
            e["t2"] = "(a)" if (e["dict_events"] or e["captured"]) else "(b)"

    t3_rows = OrderedDict()
    for ph in list(rows2) + [dict(locator=r["locator"], text=r["text"], status="complication_name") for r in A2["complications"]]:
        text = ph["text"]
        for inner in ADV_PAREN.findall(text):
            kd_, ratio = D2.paren_kind(kt, inner, ST.r1)
            if kd_ not in ("S", "tie"):
                continue
            e = t3_rows.setdefault((text, inner), OrderedDict([("text", text), ("inner", inner), ("kind", kd_), ("ratio", round(ratio, 3)), ("n", 0), ("locators", []),
                                                               ("dict_in_paren", sorted({dict_canon[dkey(t[0])] for t in kt.tokens(inner) if dkey(t[0]) in dict_canon})),
                                                               ("proposal", "R15 속성(수치·발생률)" if re.search(r"\d|%", inner) else "병기 약어·문헌 후보")]))
            e["n"] += 1
            e["locators"].append(ph["locator"])

    empty_any, empty_t2b, empty_amb = [], [], []
    st_cnt = Counter(r["status"] for r in rows2)
    for r in rows2:
        if r["status"] not in ("exact", "new"):
            continue
        ev = {dkey(e) for e in ST.rec.get(r["locator"], {}).get("events", [])} - D_final
        if ev:
            continue
        kinds = {x["kind"] for x in seg_by_loc.get(r["locator"], [])}
        item = (r["locator"], r["text"], sorted(kinds))
        if "T2b" in kinds and not (kinds - {"T2b", "T2a-rest", "T4", "T3"}):
            empty_t2b.append(item)
        elif kinds & {"T1-EF", "T1-none", "ANOM"}:
            empty_amb.append(item)
        else:
            empty_any.append(item)
    names_empty = []
    for r in A2["complications"]:
        ev = {dkey(e) for e in ST.rec.get(r["locator"], {}).get("events", [])} - D_final
        if not ev:
            names_empty.append((r["locator"], r["text"], sorted({x["kind"] for x in seg_by_loc.get(r["locator"], [])})))

    # ---- R1 · R2 기록(2차)
    r1_hits = Counter(w for r in seglog for e, w in r["r1"])
    r2_hits = Counter(w for r in seglog for w in r["r2"])
    r1_names = defaultdict(set)
    for r in seglog:
        for e, w in r["r1"]:
            r1_names[w].add(r["core7"])
    r2_names = defaultdict(set)
    for r in seglog:
        for w in r["r2"]:
            r2_names[w].add(r["core7"])
    glued = []
    for r in seglog:
        sep7 = {norm(t) for t in r["core7"].split()}
        for x, ws_ in (("R2", r["r2"]), ("R1", [w for e, w in r["r1"]])):
            for w in ws_:
                if norm(w) not in sep7:
                    glued.append(OrderedDict([("core7", r["core7"]), ("rule", x), ("word", w), ("to", r["target"]), ("loc", r["loc"])]))

    conf_vals = {norm(x["value"]): x for x in t0_r2_conflict}
    conf_hit = OrderedDict()
    for r in seglog:
        for u in r.get("units") or []:
            if norm(u) in conf_vals:
                conf_hit.setdefault(conf_vals[norm(u)]["value"], []).append((r["core7"], r["target"]))
    t0["r2_conflicts_hit_in_node_segments"] = conf_hit
    t0["standalone_disagree"] = [(name_of(k) if k in nodes0 else k, v) for k, v in bad_sa.items()]

    # ---- 저장
    res = OrderedDict([
        ("brief", "../../silver-dryrun2-brief.md"), ("order", "T3 → T4 → T2 → T1 → R2 → R1 → R3 → R4 → S"), ("kiwi", {"version": __import__("kiwipiepy").__version__, "top_n": KT.TOP_N}),
        ("t0", t0), ("table", table), ("table_1st", R1J["table"]),
        ("node_rows", node_rows), ("dup_rows", dup_rows),
        ("seed_slots", [(g, s["id"], s["title"]) for g, s in seed_slots]), ("b3_slots", [(g, s["id"], s.get("title")) for g, s in b3_slots]),
        ("seglog_kinds", Counter(r["kind"] for r in seglog)), ("seglog_n", len(seglog)),
        ("r1_hits", r1_hits), ("r1_names", {k: sorted(v) for k, v in r1_names.items()}), ("r2_hits", r2_hits), ("r2_names", {k: sorted(v) for k, v in r2_names.items()}), ("glued_rr", glued),
        ("r3_dropped", [OrderedDict([("node", name_of(k)), ("solo_strict", ST.solo_strict[k]), ("solo_loose", ST.solo_loose[k]), ("occurrences", [(lc, ST.rec.get(lc, {}).get("text"), sorted(name_of(e) for e in occ_events.get(lc, set()) if e != k)) for lc in nodes2[k]["locators"]])]) for k in sorted(D_final, key=name_of)]),
        ("r3_sole_kept", [OrderedDict([("node", name_of(k)), ("locator", v[0]), ("text", v[1])]) for k, v in sorted(sole.items(), key=lambda kv: name_of(kv[0]))]),
        ("r4_pairs", [OrderedDict([("a", name_of(a)), ("b", name_of(b)), ("texts", sorted({t for _, t in locs}))]) for (a, b), locs in r4_pairs.items()]),
        ("r4_ambiguous", [OrderedDict([("a", name_of(a)), ("b", name_of(b)), ("kind", r4_amb_kind[(a, b)]), ("texts", sorted({t for _, t in locs}))]) for (a, b), locs in r4_amb.items()]),
        ("s_pairs", [OrderedDict([("a", a), ("b", b), ("rules", list(r))]) for a, b, bk, r in s_pairs]), ("s_ambiguous", [OrderedDict([("a", a), ("b", b), ("rules", list(r)), ("a_2nd", fT.get(norm(a), ("?",))[0])]) for a, b, bk, r in s_amb]),
        ("nodes", OrderedDict([("dict_events", len(dict_canon)), ("nodes_7th", len(nodes0)), ("strong_7th", len(strong0)), ("nodes_after_T_R2_R1", len(nodes2)), ("r3_dropped", len(D_final)),
                               ("alive_after_R3", len(alive)), ("final_node_groups", len(final_nodes)), ("new_names", [OrderedDict([("node", name_of(k)), ("n", n_locs(k)), ("from", sorted(from_of.get(k, []))), ("ambiguous", amb_reasons(k)), ("partners", partners.get(k, []))]) for k in sorted(new_names, key=lambda x: (-n_locs(x), name_of(x)))]),
                               ("final_nodes", [OrderedDict([("node", name_of(k)), ("n", n_locs(k)), ("ambiguous", amb_reasons(k))]) for k in sorted(final_nodes, key=lambda x: (-n_locs(x), name_of(x)))])])),
        ("strong_recalc", OrderedDict([("strong_after_rules", len(strongF)), ("of_which_new", len(new_strong)), ("new_pairs", [OrderedDict([("a", d["new"]), ("b", d["existing"]), ("rules", d["rules"])]) for d in new_strong]),
                                       ("remaining_slots_in_recalc", sum(1 for r in dup_rows if r.get("in_recalc"))), ("all_pairs", [OrderedDict([("a", d["new"]), ("b", d["existing"]), ("rules", d["rules"])]) for d in strongF])])),
        ("particle_check", OrderedDict([("checked", len(pe_check)), ("fail", pe_fail), ("rows", pe_check)])),
        ("first_vs_second", OrderedDict([("first_remaining", len(first_remaining)), ("vanished", vanished), ("stayed", stayed), ("no_reason", no_reason), ("first_closed_now_remaining", first_closed_now_remaining)])),
        ("t2_phrases", list(t2_rows.values())), ("t3_parens", list(t3_rows.values())), ("t4_dict_after", t4_dict_after),
        ("first_nodes", OrderedDict((k_, v_) for k_, v_ in R1J["nodes"].items() if not isinstance(v_, list))), ("first_strong_recalc", R1J["strong_recalc"]["strong_after_rules"]),
        ("first_new_names", len(R1J["nodes"]["new_node_names"])),
        ("phrases", OrderedDict([("occurrences", len(rows2)), ("by_status", dict(st_cnt)), ("by_status_7th", dict(Counter(r["status"] for r in A7["phrase_rows"]))), ("empty_event_cell", empty_any), ("empty_t2b", empty_t2b), ("empty_amb_user", empty_amb), ("names_empty", names_empty)])),
        ("seglog", [OrderedDict((k_, v_) for k_, v_ in r.items() if k_ not in ("text",)) | {"text": r["text"]} for r in seglog]),
        ("out_hash_before", out_hash_before), ("out_hash_after_analysis", sha_tree(os.path.join(HERE, "out"))),
    ])
    with open(os.path.join(OUT, "dryrun2.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1, default=list)
    verify = None
    if opt.verify:
        cmd = "python3 build.py && python3 check.py && python3 tests/run_tests.py"
        env = dict(os.environ)
        env.pop("VIRTUAL_ENV", None)
        env["PATH"] = ":".join(p for p in env.get("PATH", "").split(":") if ".venv-kiwi" not in p)
        p = subprocess.run(cmd, shell=True, cwd=HERE, capture_output=True, text=True, env=env)
        man = json.load(open(os.path.join(HERE, "out", "manifest.json"), encoding="utf-8"))
        base = json.load(open(os.path.join(HERE, "baseline", "manifest-7차.json"), encoding="utf-8"))
        verify = OrderedDict([("cmd", cmd), ("python3", subprocess.run("command -v python3", shell=True, capture_output=True, text=True, env=env).stdout.strip()), ("returncode", p.returncode), ("stdout", p.stdout), ("stderr", p.stderr),
                              ("key_out", man.get("determinism_key")), ("key_baseline", base.get("determinism_key")),
                              ("out_hash_before", out_hash_before), ("out_hash_after_build", sha_tree(os.path.join(HERE, "out")))])
        with open(os.path.join(OUT, "verify-7차.json"), "w", encoding="utf-8") as fh:
            json.dump(verify, fh, ensure_ascii=False, indent=1)
    elif os.path.exists(os.path.join(OUT, "verify-7차.json")):
        verify = json.load(open(os.path.join(OUT, "verify-7차.json"), encoding="utf-8"))
    import render2
    render2.write(res, verify, os.path.join(OUT, "report.md"))
    print(json.dumps(table, ensure_ascii=False))


if __name__ == "__main__":
    main()
