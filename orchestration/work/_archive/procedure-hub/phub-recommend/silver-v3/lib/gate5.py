# -*- coding: utf-8 -*-
"""결정 묶음 5 게이트 자료 — ERD v3.2 노드 단위(발주서 `../silver-build-7-brief.md` C).

out/gate/batch5.json(웹 페이지 입력 · 2B 스키마) · batch5.md(사람 읽기) · batch5-weak.json(⑦ weak — 게이트에 올리지 않음).
  1. 원장 사건 노드(origin=ledger · unreviewed) — 노드마다: 핵심어 · 원장 횟수 · 계열·항목 · 원문 예 3 · 설명(원장 문맥)
     옵션 = 부작용 맞음(종류 8: dictionary_add · category) / 부작용 아님 → 메모(exclude · dictionary_value) / 접기 → ⑦ strong 상대(fold_approve · 사전 값 쌍)
  2. ⑦ strong 쌍 — 같다(fold_approve · keep 쪽) / 다르다(conflict_close not_same) / 보류(결정 없음) · 원장 병기 「X(Y)」 쌍은 추천 「같다」
  3. 씨앗 승인(`../erd-v3.2-seed-candidates.json` proposed) — 부위 · 성분 · 줄임말: 승인(dictionary_add) / 제외(scope_review 기록)
  4. 결정 묶음 3 미결(out/gate/batch3.json 그대로 · 공기색전은 v3.2 물질 칸 기준으로 옵션 갱신)
decision_payload = 그 옵션을 고르면 만들어질 결정 파일 본문(ERD v3.2 §5 kind 구조체 완성형 · status=proposed) — `apply_gate.py --gate out/gate/batch5.json` 이 decisions/batch5/ 에 쓴다.
원문은 브론즈 원장에서 locator 로 직접 읽는다(ERD 꼴 locator 는 원장 위치로 옮겨 읽는다 · 읽기 실패 0 이어야 한다). 추천은 원장이 말할 때만(추정 금지).
"""
import copy
import json
import os
import re
from collections import Counter, OrderedDict, defaultdict

from .decisions import validate
from .gate2b import G, node
from .gate3 import leaves_of, opt
from .provenance import parse_loc, resolve, split_path
from .util import dedupe, md_table, mkid, norm, write_json, write_text

BATCH = "DEC-2026-11-05-B5"
BATCH_NOTE = "결정 묶음 5 (게이트 out/gate/batch5.json · ERD v3.2 노드 단위 — 원장 사건 노드 · ⑦ strong · 씨앗 · 묶음 3 미결)"
ERD_REF = "erd-v3.2.md §0.2 · §1.5 · §1.7 · §5"
CATS = OrderedDict([("local", ("국소", "국소 일시 반응")), ("inflam", ("염증", "염증/감염")), ("vascular", ("혈관", "혈관")), ("neuro", ("신경", "신경")),
                    ("pigment", ("색소", "색소")), ("struct", ("구조", "구조/이물")), ("systemic", ("전신", "전신")), ("function", ("기능", "기능"))])
SEED_FILE = "erd-v3.2-seed-candidates.json"


def _h(s):
    return mkid("X", s)[2:]


class G5(G):
    def __init__(self, S, decisions_dir):
        super().__init__(S, decisions_dir)
        self.read_fail = []

    def resolve_erd(self, lc):
        """ERD 꼴 locator(rec 의 배열 자리에 코드 · 예 `…items[].name@M8/0/5`) → 원장 위치 locator. 배열 자리의 코드는 그 배열 원소의 id·category 로 찾는다."""
        p = parse_loc(lc)
        cur = self.L[p["file"]]
        rec = [] if p["rec"] in ("-", "") else p["rec"].split("/")
        out, ri = [], 0
        for name, n_arr in split_path(p["path"]):
            if name == "{code}":
                out.append(rec[ri])
                cur = cur[rec[ri]]
                ri += 1
            else:
                cur = cur[name]
            for _ in range(n_arr):
                r = rec[ri]
                ri += 1
                if re.fullmatch(r"\d+", r):
                    idx = int(r)
                else:
                    idx = next(i for i, x in enumerate(cur) if isinstance(x, dict) and (x.get("id") == r or x.get("category") == r))
                out.append(str(idx))
                cur = cur[idx]
        return f"{p['file']}:{p['path']}@{'/'.join(out) if out else '-'}"

    def ev(self, lc, note=None):
        o = super().ev(lc, note)
        if str(o["text"]).startswith("<읽기 실패"):
            try:
                src = self.resolve_erd(lc)
                q = parse_loc(src)
                v = resolve(self.L[q["file"]], q["path"], q["rec"])
                o = OrderedDict([("file", q["file"]), ("locator", lc), ("text", v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)), ("source_locator", src)] + ([("note", note)] if note else []))
            except Exception:  # noqa: BLE001
                self.read_fail.append(lc)
        return o

    def src(self, lc):
        """결정 source_refs 용 원장 위치 locator."""
        o = self.ev(lc)
        return o.get("source_locator") or lc


def payload(pid, kind, target, new_value, reason, ledger_refs, extra_refs=()):
    refs, seen = [], set()
    for r in [{"kind": "ledger", "ref": x} for x in ledger_refs] + [{"kind": "erd", "ref": ERD_REF}, {"kind": "brief", "ref": "silver-build-7-brief.md C"}] + list(extra_refs):
        k = (r["kind"], r["ref"])
        if k not in seen:
            seen.add(k)
            refs.append(OrderedDict([("kind", r["kind"]), ("ref", r["ref"])]))
    return OrderedDict([("id", pid), ("kind", kind), ("target", target), ("new_value", new_value), ("reason", reason), ("decided_by", None), ("decided_at", None),
                        ("status", "proposed"), ("source_refs", refs), ("batch", BATCH_NOTE)])


def _examples(g, contexts, n=3):
    """원문 예 — 서로 다른 원문 n 개(첫 출현 순 · 원장에서 다시 읽는다)."""
    out, seen = [], set()
    for c in contexts:
        t = c.get("text")
        if t in seen:
            continue
        seen.add(t)
        out.append(g.ev(c["locator"], f"원문 예 · {c.get('kind')} · {c.get('modality')}"))
        if len(out) >= n:
            break
    return out


def _where(contexts):
    fam = dedupe(c.get("modality") for c in contexts if c.get("modality"))
    items = dedupe(f"{c.get('modality')}/{c['item']}" for c in contexts if c.get("item"))
    prods = dedupe(f"{c.get('modality')}/{c['product']}" for c in contexts if c.get("product"))
    kinds = dict(Counter(c.get("kind") for c in contexts))
    fc = dict(Counter(c.get("frequency_class") or c.get("severity") for c in contexts if c.get("frequency_class") or c.get("severity")))
    return OrderedDict([("modalities", fam), ("items", items), ("products", prods), ("kinds", kinds), ("frequency_or_severity", fc)])


# =====================================================================================
# 1. 원장 사건 노드
# =====================================================================================
def node_items(g, S, strong_by_node):
    A = S.ctx["adv"]
    nodes = sorted(A["ledger_events"], key=lambda n: (-len(n["locators"]), n["canonical"]))
    by_ctx = defaultdict(list)
    for n in nodes:
        for c in n["contexts"]:
            by_ctx[n["canonical"]].append(c)
    # 문구 항목 · 이름 — 노드가 든 자리(효과 계산)
    ent_of = defaultdict(list)
    for e in A["phrase_dictionary"]:
        for ev in e.get("ledger_events") or []:
            ent_of[ev].append(e)
    name_of = defaultdict(list)
    for r in A["complications"]:
        for sp in r.get("spans") or []:
            if sp[0] == "event" and sp[1] in {n["canonical"] for n in nodes}:
                name_of[sp[1]].append(r)
    subs = []
    for n in nodes:
        nm = n["canonical"]
        ctxs = by_ctx[nm]
        where = _where(ctxs)
        ev = _examples(g, ctxs)
        ents = ent_of.get(nm, [])
        only = [e for e in ents if {c["event"] for c in e["candidates"]} == {nm}]
        names = name_of.get(nm, [])
        refs = [g.src(l) for l in n["locators"]]
        pid = f"{BATCH}-N-{n['id'][4:]}"
        opts = []
        for key, (short, cat) in CATS.items():
            p_ = payload(pid, "dictionary_add", OrderedDict([("dictionary", "adverse_event_type")]), OrderedDict([("canonical", nm), ("synonyms", []), ("category", cat)]),
                         f"결정 묶음 5 — 원장 사건 노드 「{nm}」(원장 {len(n['locators'])} 자리)는 부작용이 맞다 · 종류 {cat}. 사건 사전 값이 된다(origin=decision · 단위 id 그대로).", refs)
            opts.append(opt(f"adverse:{key}", f"부작용 맞음 — 종류 {short}" + ("" if short == cat else f"({cat})") + (" · 새 종류 값" if key == "function" else ""),
                            f"사건 사전 adverse_event_type 값 「{nm}」(category={cat}) — 노드가 사전 값이 되어 문구 {len(ents)} 항목 · 이름 {len(names)} 의 그 사건이 new → exact · 단위 id 는 그대로(DIC-sha(adverse_event_type|{nm}) 같은 식)", p_, True))
        p_ = payload(pid, "exclude", OrderedDict([("kind", "dictionary_value"), ("key", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", nm)]))]), OrderedDict([("excluded", True)]),
                     f"결정 묶음 5 — 원장 사건 노드 「{nm}」는 부작용이 아니다 → 메모. 노드를 세우지 않고 그 토큰은 설명(보존) · 사건이 남지 않는 문구는 메모(note).", refs)
        opts.append(opt("not_adverse", "부작용 아님 → 메모", f"노드를 세우지 않는다(토큰은 parsed.explanation 보존) — 이 노드만 사건인 문구 {len(only)} 항목은 메모(note)로 · 다른 사건과 함께인 문구 {len(ents) - len(only)} 항목은 그 사건만 남는다 · 이름 {len(names)}", p_, True))
        for d in strong_by_node.get(nm, []):
            other = d["other"] if d["node"] == nm else d["node"]
            okind = d["other_kind"] if d["node"] == nm else "ledger"
            p_ = payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", nm), ("into", other)]), OrderedDict([("keep", other)]),
                         f"결정 묶음 5 — 원장 사건 노드 「{nm}」를 「{other}」({'사전 사건' if okind == 'dictionary' else '원장 노드'})에 접는다(⑦ strong · 규칙 {', '.join(d['rules'])}). 노드는 그 값의 동의어 · 단위 id 는 접힐 곳 기준.", refs,
                         [{"kind": "erd", "ref": d["erd_key"]}])
            opts.append(opt(f"fold:{other}", f"접기 → 「{other}」({'사전' if okind == 'dictionary' else '원장 노드'} · ⑦ strong {', '.join(d['rules'])})",
                            f"「{nm}」는 「{other}」의 동의어 — 이 노드의 문구·이름 자리가 「{other}」 단위로 간다 · 그 ⑦ 은 resolved", p_, True))
        desc = "; ".join(f"{c.get('kind')} · {c.get('modality')} · {c.get('frequency_class') or c.get('severity') or '—'}" + (f" · 항목 {c['item']}" if c.get("item") else "") + (f" · 제품 {c['product']}" if c.get("product") else "") for c in ctxs[:3])
        subs.append(node(f"node/{n['id']}", "ledger_event", f"원장 사건 노드 「{nm}」 — 부작용으로 둘까?",
                         f"핵심어 「{nm}」 · 원장 {len(n['locators'])} 자리 · 계열 {', '.join(where['modalities']) or '—'}" + (f" · 항목 {len(where['items'])}" if where["items"] else "") + (f" · 제품 {len(where['products'])}" if where["products"] else "") +
                         f" · 문구 사전 {len(ents)} 항목 · 이름 {len(names)}. 설명(원장 문맥): {desc}" + (f" … 외 {len(ctxs) - 3}" if len(ctxs) > 3 else ""),
                         ev, opts, None, "원장 칸은 「부작용 문구」라는 것만 말하고 종류(국소·염증·혈관·신경·색소·구조·전신·기능)를 적은 칸이 없다 — 추천 없음(추정 금지).",
                         OrderedDict([("node", OrderedDict([("id", n["id"]), ("canonical", nm), ("core_tokens", n.get("core_tokens")), ("n_locators", len(n["locators"])), ("locators", n["locators"]),
                                                            ("where", where), ("phrase_entries", [e["id"] for e in ents]), ("only_event_phrases", [e["id"] for e in only]), ("names", [r["locator"] for r in names]),
                                                            ("strong_partners", [(d["other"] if d["node"] == nm else d["node"]) for d in strong_by_node.get(nm, [])])]))])))
    return node("ledger-nodes", "ledger_event", f"원장 사건 노드 {len(subs)} — 부작용 맞음(종류) / 아님(메모) / 접기(⑦ strong)",
                "V3.2-0 노드 원칙: 부작용 문구의 토막에 사전 사건이 0 이면 핵심어가 새 사건 노드(origin=ledger · unreviewed)다. 노드마다 사람이 정한다 — 종류(category)를 주면 사건 사전 값 · 아니면 메모 · 같은 것이면 ⑦ strong 상대에 접는다.",
                [], [], None, "하위 항목마다", {"subitems": subs})


# =====================================================================================
# 2. ⑦ strong 쌍
# =====================================================================================
def paren_outer(L, a, b):
    """원장 병기 「X (Y)」 — 괄호 밖(본 표기) 쪽. 부작용 문구 자리 전부에서 찾는다(없으면 None)."""
    from .v32 import CUR
    for ax, kind, f, p, loc_, text, mod in CUR.get("texts") or []:
        m = re.fullmatch(r"\s*([^()]+?)\s*\(([^()]+)\)\s*", str(text))
        if m and ax == "adverse":
            x, y = norm(m.group(1)), norm(m.group(2))
            if {x, y} == {norm(a), norm(b)}:
                return a if norm(a) == x else b
    return None


def dup_items(g, S, strong):
    A = S.ctx["adv"]
    nodes = {n["canonical"]: n for n in A["ledger_events"]}
    ev_dict = {norm(e["canonical"]): e for e in g.dicts["adverse_event_type"]["entries"]}
    subs = []
    for c in strong:
        d = c["pair"]
        a, b, bk = d["node"], d["other"], d["other_kind"]
        na = nodes.get(a)
        ev = [dict(x, note=f"「{a}」 " + x.get("note", "")) for x in _examples(g, na["contexts"] if na else [])]
        refs = [g.src(l) for l in (na["locators"] if na else [])]
        bdesc = ""
        if bk == "ledger":
            nb = nodes.get(b)
            ev += [dict(x, note=f"「{b}」 " + x.get("note", "")) for x in _examples(g, nb["contexts"] if nb else [])]
            refs += [g.src(l) for l in (nb["locators"] if nb else [])]
            bdesc = f"원장 노드 「{b}」 원장 {len(nb['locators']) if nb else 0} 자리"
        else:
            e = ev_dict.get(norm(b)) or {}
            bdesc = f"사전 사건 「{b}」(category {e.get('category') or '—'} · 동의어 {', '.join(s_['value'] for s_ in e.get('synonyms', [])[:6]) or '없음'})"
        pid = f"{BATCH}-D-{_h(d['erd_key'])}"
        opts = [opt(f"same:keep:{b}", f"같다 — 접기(「{b}」 쪽 유지)", f"「{a}」는 「{b}」의 동의어 — 「{a}」 노드 자리 전부 「{b}」 단위로 · 이 ⑦ resolved",
                    payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", a), ("into", b)]), OrderedDict([("keep", b)]),
                            f"결정 묶음 5 — ⑦ strong 「{a}」 ↔ 「{b}」 같다 · 「{b}」 유지(규칙 {', '.join(d['rules'])})", refs, [{"kind": "erd", "ref": d["erd_key"]}]), True)]
        if bk == "ledger":
            opts.append(opt(f"same:keep:{a}", f"같다 — 접기(「{a}」 쪽 유지)", f"「{b}」는 「{a}」의 동의어 — 「{b}」 노드 자리 전부 「{a}」 단위로 · 이 ⑦ resolved",
                            payload(pid, "fold_approve", OrderedDict([("dictionary", "adverse_event_type"), ("canonical", b), ("into", a)]), OrderedDict([("keep", a)]),
                                    f"결정 묶음 5 — ⑦ strong 「{a}」 ↔ 「{b}」 같다 · 「{a}」 유지(규칙 {', '.join(d['rules'])})", refs, [{"kind": "erd", "ref": d["erd_key"]}]), True))
        opts.append(opt("different", "다르다", "둘 다 유지 — 이 ⑦ dismissed(close_verdict not_same)",
                        payload(pid, "conflict_close", OrderedDict([("conflict_key", copy.deepcopy(c["stable_key"]))]), OrderedDict([("verdict", "not_same"), ("note", f"「{a}」 ≠ 「{b}」")]),
                                f"결정 묶음 5 — ⑦ strong 「{a}」 ↔ 「{b}」 다르다(not_same)", refs, [{"kind": "erd", "ref": d["erd_key"]}]), True))
        opts.append(opt("hold", "보류", "결정 없음(⑦ open 그대로)", None, None))
        rec, why = None, "표기 규칙만 맞는 후보 — 같은 것인지는 원장이 말하지 않는다(추천 없음)."
        if "paren_pair" in d["rules"]:
            if bk == "dictionary":
                rec, why = f"same:keep:{b}", f"원장이 「{a}」와 「{b}」를 병기 「X(Y)」로 적었다 — 같은 것 · 사전 사건 「{b}」 쪽 유지."
            else:
                outer = paren_outer(g.L, a, b)
                if outer:
                    rec, why = f"same:keep:{outer}", f"원장이 「{a}」와 「{b}」를 병기 「X(Y)」로 적었다 — 같은 것 · 괄호 밖 본 표기 「{outer}」 쪽 유지."
        subs.append(node(f"dup/{_h(d['erd_key'])}", "duplicate_candidate", f"⑦ 「{a}」 ↔ 「{b}」 — 같은가?",
                         f"원장 노드 「{a}」 원장 {len(na['locators']) if na else 0} 자리 ↔ {bdesc} · 규칙 {', '.join(d['rules'])}(strong) · 안정 키 {d['erd_key']}",
                         ev, opts, rec, why, OrderedDict([("pair", d), ("conflict_id", c["id"]), ("stable_key", c["stable_key"])])))
    return node("dup-strong", "duplicate_candidate", f"⑦ strong {len(subs)} 쌍 — 같다(접기) / 다르다 / 보류",
                "V3.2-0 ⑦ 노드끼리(원장 노드 ↔ 사전 사건 · 원장 노드 ↔ 원장 노드) · strong = 원장 병기 X(Y) · X+감/증/형성/감각 ↔ X · 짧은 쪽이 긴 쪽의 낱말 · 자모 1 치환. 유사도 점수 없음.",
                [], [], None, "하위 항목마다(원장 병기 쌍만 추천)", {"subitems": subs})


# =====================================================================================
# 3. 씨앗
# =====================================================================================
def seed_items(g, S, seeds):
    out = []
    for grp, dname, title in (("site", "site", "부위"), ("ingredient_material", "ingredient_material", "성분"), ("product_abbrev", "product_name", "줄임말·옛 이름")):
        rows = [r for r in seeds["seeds"][grp]["rows"] if r.get("status") == "proposed"]
        subs = []
        for r in rows:
            val = r.get("value") or r.get("fragment")
            locs = list(r.get("locators") or [])
            ev = [g.ev(l, f"씨앗 근거({title})") for l in locs[:3]]
            refs = [g.src(l) for l in locs]
            key = f"{grp}|{val}|{r.get('product', '')}"
            pid = f"{BATCH}-S-{_h(key)}"
            if grp == "site":
                syns = [x["value"] for x in r.get("synonyms", []) if x.get("n")]
                nv = OrderedDict([("canonical", val), ("synonyms", syns), ("category", None), ("kind", r["kind"]), ("parent", r.get("parent"))])
                eff = f"부위 사전 값 「{val}」(kind={r['kind']} · parent={r.get('parent') or '—'}" + (f" · 동의어 {', '.join(syns)}" if syns else "") + f") — 원장 {r['n']} 자리 조각이 부위로"
                syn_txt = ", ".join("{}({})".format(x["value"], x["n"]) for x in r.get("synonyms", []))
                why = f"부위 닫힌 목록(V3.2-4) 값 「{val}」(kind {r['kind']} · parent {r.get('parent') or '—'}) — 원장 {r['n']} 자리" + (f" · 동의어 후보 {syn_txt}" if syn_txt else "")
            elif grp == "ingredient_material":
                nv = OrderedDict([("canonical", val), ("synonyms", []), ("category", None)])
                eff = f"성분 사전 값 「{val}」 — 시술 라벨에서 다른 primary 가 없으면 what=성분(V3.2-6) · 있으면 ingredient_fragments"
                why = f"성분 씨앗 「{val}」 — 원장 {r['n']} 자리 · 근거 {r.get('basis')}"
            else:
                pe = next((e for e in g.dicts["product_name"]["entries"] if norm(e["canonical"]) == norm(r["product"])), None)
                nv = OrderedDict([("canonical", r["product"]), ("synonyms", [r["fragment"]]), ("category", None)])
                if pe is not None and pe.get("code") is not None:
                    nv["code"] = pe.get("code")
                if r.get("product_origin") == "taxonomy":
                    nv["origin"] = "taxonomy"
                eff = f"제품 「{r['product']}」({r.get('product_origin')})의 동의어 「{r['fragment']}」 — 그 조각이 제품으로 닿는다(같은 조각을 다른 제품에도 승인하면 먼저 적용된 것만 남는다)"
                why = f"「{r['fragment']}」 ↔ 제품 「{r['product']}」 — {r.get('rule')} · 원장 {r['n']} 자리"
                val = f"{r['fragment']}→{r['product']}"
            p_add = payload(pid, "dictionary_add", OrderedDict([("dictionary", dname)]), nv, f"결정 묶음 5 — 씨앗 승인({title}) 「{val}」(erd-v3.2-seed-candidates.json · V3.2-3/4/5/6)", refs,
                            [{"kind": "erd", "ref": f"{SEED_FILE}#seeds/{grp}"}])
            p_no = payload(pid, "scope_review", OrderedDict([("erd_ref", f"{SEED_FILE}#seeds/{grp}"), ("review_item", val)]), OrderedDict([("disposition", f"씨앗 제외 — {title} 사전에 넣지 않는다")]),
                           f"결정 묶음 5 — 씨앗 제외({title}) 「{val}」 — 기록만", refs, [{"kind": "erd", "ref": f"{SEED_FILE}#seeds/{grp}"}])
            opts = [opt("approve", "승인", eff, p_add, True), opt("exclude", "제외", "사전에 넣지 않는다 — 기록만(scope_review · 빌드 값 그대로)", p_no, True)]
            subs.append(node(f"seed-{grp}/{_h(key)}", "dictionary_add", f"{title} 씨앗 「{val}」 — 사전에 넣을까?", why, ev, opts, None,
                             "씨앗 묶음은 승인 절차(닫힌 사전·문맥 추정·접두 규칙) — 원장이 값을 선언하지 않는다(추천 없음).", OrderedDict([("seed", r)])))
        out.append(node(f"seed-{grp}", "dictionary_add", f"씨앗 — {title} {len(subs)}", seeds["seeds"][grp].get("why_closed") or seeds["seeds"][grp].get("why_not_auto") or seeds["seeds"][grp].get("note") or "",
                        [], [], None, "하위 항목마다", {"subitems": subs}))
    return out


# =====================================================================================
# 4. 묶음 3 미결(그대로 · 공기색전 v3.2 갱신)
# =====================================================================================
def batch3_items(g, S, items3):
    out = copy.deepcopy(items3)
    AU = S.ctx["AU"]
    for it in out:
        if it["id"] != "air-embolism-qualifier":
            continue
        lc = it["options"][0]["decision_payload"]["target"]["locator"]
        now = []
        for u in AU.name_units.get(lc, []):
            x = AU.units[u]
            now.append(f"({x['event']}, {x.get('site') or 'none'}, {x.get('qualifier') or 'none'})")
        row = next((r for r in S.ctx["adv"]["complications"] if r["locator"] == lc), {})
        side = (row.get("parsed") or {}).get("side") or []
        same = now == it["proposed"]
        pl = it["options"][0]["decision_payload"]
        pl["target"] = OrderedDict([("kind", "name"), ("locator", lc)])
        pl["reason"] = pl["reason"].replace("(v3.1: 세 칸 단위 + R15 경과로 옮김)", "(v3.2: target.kind=name · 물질 칸 qualifier=공기)")
        it["options"][0]["label"] = "지정(고정) → " + " + ".join(it["proposed"])
        it["options"][0]["effect"] = ("v3.2 분해(물질 칸 · 노드 원칙)로 이 이름은 이미 " + " + ".join(now) + " — 결정은 그 지정을 사람 판단으로 고정한다(뒤 사전 변경에도 유지)" if same else
                                      "이 이름의 단위가 " + " + ".join(it["proposed"]) + " 로 바뀐다 · 지금 " + (" + ".join(now) or "단위 없음")) + \
            (f" · 「{' '.join(side)}」 은 감염 토막의 side(보존 · 단위 칸 아님 · 노드 후보 목록)" if side else "")
        it["options"][1]["label"] = "지금대로(v3.2 분해 그대로 — " + (" + ".join(now) or "단위 없음") + ")"
        it["now"] = now
        it["target_kind_note"] = "v3.2: target.kind=name — complications 이름 ERD 꼴 locator(@M16/10) · 단위 세 칸(사건, 부위, 물질) · 「공기색전」 = 접두 수식 공기 + 사건 색전"
        it["why"] = "V3-1 수식(물질) 칸으로 「공기색전」은 (색전 · 물질 공기)로 읽힌다. v3.2 노드 원칙으로 「카테터 관련 감염」 토막은 사전 사건 감염에 exact 로 붙고 「카테터 관련」은 side(보존)다 — " + \
            ("그래서 지금 분해가 이미 제안과 같다. 남은 것은 이 지정을 결정으로 고정할지뿐이다." if same else "지금 분해와 제안이 다르다.")
        it["recommend_reason"] = ("v3.2 에서 두 옵션의 단위가 같다 — 고정 여부만 남고 원장은 그것을 말하지 않는다(추천 없음)." if same else it["recommend_reason"])
        it["v32_updated"] = True
    return out


# =====================================================================================
def build_gate_5(S, out_dir, seeds_path):
    g = G5(S, S.ctx["args"].decisions)
    seeds = json.load(open(seeds_path, encoding="utf-8"))
    dups = S.ctx.get("ledger_dup_conflicts", [])
    strong = [c for c in dups if c.get("grade") == "strong" and c["status"] == "open"]
    weak = [c for c in dups if c.get("grade") == "weak" and c["status"] == "open"]
    strong_by_node = defaultdict(list)
    for c in strong:
        strong_by_node[c["pair"]["node"]].append(c["pair"])
        if c["pair"]["other_kind"] == "ledger":
            strong_by_node[c["pair"]["other"]].append(c["pair"])
    items = [node_items(g, S, strong_by_node), dup_items(g, S, strong)] + seed_items(g, S, seeds)
    b3p = os.path.join(out_dir, "gate", "batch3.json")
    items3 = json.load(open(b3p, encoding="utf-8")) if os.path.exists(b3p) else []
    items += batch3_items(g, S, items3)
    ids = set()
    for it, s in leaves_of(items):
        if s["id"] in ids:
            raise AssertionError(f"게이트 자리 id 중복 {s['id']}")
        ids.add(s["id"])
        for o in s["options"]:
            p = o["decision_payload"]
            if p:
                errs = [e for e in validate(dict(p, decided_by="x")) if "decided_by" not in e]
                if errs:
                    raise AssertionError(f"{s['id']} {o['key']}: {errs}")
        s["already_decided"] = dedupe(x for o in s["options"] for x in g.already(o["decision_payload"]))
        if s["recommended"] is not None and s["recommended"] not in [o["key"] for o in s["options"]]:
            raise AssertionError(f"{s['id']} recommended {s['recommended']} 없음")
    if g.read_fail:
        raise AssertionError(f"원장 읽기 실패 {len(g.read_fail)}: {g.read_fail[:5]}")
    gd = os.path.join(out_dir, "gate")
    os.makedirs(gd, exist_ok=True)
    write_json(os.path.join(gd, "batch5.json"), items)
    nodes = {n["canonical"]: n for n in S.ctx["adv"]["ledger_events"]}
    weak_rows = [OrderedDict([("conflict_id", c["id"]), ("pair", c["pair"]), ("stable_key", c["stable_key"]),
                              ("node_locators", nodes.get(c["pair"]["node"], {}).get("locators", [])),
                              ("other_locators", nodes.get(c["pair"]["other"], {}).get("locators", []) if c["pair"]["other_kind"] == "ledger" else [])]) for c in weak]
    write_json(os.path.join(gd, "batch5-weak.json"), weak_rows)
    write_text(os.path.join(gd, "batch5.md"), render_md(items, weak_rows))
    lv = list(leaves_of(items))
    per = OrderedDict()
    for it in items:
        n_ = len(it.get("subitems") or [it])
        r_ = sum(1 for s in (it.get("subitems") or [it]) if s["recommended"] is not None)
        per[it["id"]] = {"leaves": n_, "recommended": r_}
    return {"items": len(items), "leaves": len(lv), "by_item": per, "recommended": sum(1 for _, s in lv if s["recommended"] is not None), "weak": len(weak_rows),
            "evidence": sum(len(s["evidence"]) for _, s in lv), "read_fail": len(g.read_fail), "options": sum(len(s["options"]) for _, s in lv)}


def render_md(items, weak_rows):
    lv = list(leaves_of(items))
    rec = sum(1 for _, s in lv if s["recommended"] is not None)
    o = ["# 결정 묶음 5 — 게이트 자료(ERD v3.2 노드 단위)", "",
         f"상위 {len(items)} · 고를 자리 {len(lv)} · 추천 있음 {rec} · 추천 없음 {len(lv) - rec} · ⑦ weak {len(weak_rows)} 은 `batch5-weak.json`(게이트에 올리지 않음).",
         "원문은 브론즈 원장에서 locator 로 직접 읽었다(ERD 꼴 locator 는 원장 위치로 옮겨 읽음). 추천은 원장이 말할 때만 — 없으면 「—」. "
         "고른 결과는 `python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json` 으로 결정 파일이 된다(→ decisions/batch5/ · answers = {자리 id: 옵션 key}).", "",
         md_table(["묶음", "자리", "추천"], [(it["id"], len(it.get("subitems") or [it]), sum(1 for s in (it.get("subitems") or [it]) if s["recommended"] is not None)) for it in items]), ""]
    for it in items:
        o += [f"## {it['id']} — {it['title']}", "", it["why"], ""]
        subs = it.get("subitems") or [it]
        if it["id"] in ("ledger-nodes",):
            o.append(md_table(["#", "노드", "원장 횟수", "계열", "항목·제품", "원문 예", "접기 후보(⑦ strong)"],
                              [(i + 1, s["node"]["canonical"], s["node"]["n_locators"], ", ".join(s["node"]["where"]["modalities"]) or "—", len(s["node"]["where"]["items"]) + len(s["node"]["where"]["products"]),
                                " / ".join(f"「{str(e['text'])[:40]}」" for e in s["evidence"]), ", ".join(s["node"]["strong_partners"]) or "—") for i, s in enumerate(subs)]))
            o.append("")
            o.append("옵션(노드마다 같음): `adverse:local|inflam|vascular|neuro|pigment|struct|systemic|function`(부작용 맞음 · 종류) · `not_adverse`(부작용 아님 → 메모) · `fold:<상대>`(⑦ strong 상대에 접기). 결정 본문은 batch5.json.")
            o.append("")
            continue
        if it["id"] == "dup-strong":
            o.append(md_table(["#", "노드", "상대", "상대 종류", "규칙", "추천", "근거"], [(i + 1, s["pair"]["node"], s["pair"]["other"], s["pair"]["other_kind"], ", ".join(s["pair"]["rules"]), s["recommended"] or "—", s["recommend_reason"][:60]) for i, s in enumerate(subs)]))
            o.append("")
            continue
        if it["id"].startswith("seed-"):
            o.append(md_table(["#", "자리", "값", "근거", "원문 예"], [(i + 1, s["id"], s["title"], s["why"][:80], " / ".join(f"「{str(e['text'])[:30]}」" for e in s["evidence"])) for i, s in enumerate(subs)]))
            o.append("")
            continue
        for s in subs:
            if s is not it:
                o += [f"### {s['id']} — {s['title']}", "", s["why"], ""]
            for e in s["evidence"][:8]:
                o.append(f"- `{e['locator']}` — 「{str(e['text']).replace(chr(10), ' ')[:140]}」" + (f" ({e['note']})" if e.get("note") else ""))
            o.append("")
            o.append(md_table(["옵션", "뜻", "적용되면", "결정"], [(f"**{x['key']}**" if x["key"] == s["recommended"] else x["key"], x["label"], x["effect"], (f"{x['decision_payload']['kind']} `{x['decision_payload']['id']}`" if x["decision_payload"] else "결정 없음")) for x in s["options"]]))
            o.append(f"\n추천: **{s['recommended'] or '—'}** — {s['recommend_reason']}\n")
    return "\n".join(o)
