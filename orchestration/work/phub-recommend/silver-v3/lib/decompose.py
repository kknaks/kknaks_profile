# -*- coding: utf-8 -*-
"""분해 규칙 — ERD v3 §1.3(참조 해결) · §1.4(시술 튜플) · §1.5(부작용 튜플).

참조 구현 `erd-v3-tuples.py`(→ erd-v2.4-tuples.py → v2.3 → v2.2 → v2.1 → v2 → erd-v1.1-resolve.py 상속 사슬)의 **최종 유효 로직**을
상속 없이 한 모듈로 옮겼다. 같은 입력(사전 · resolve_rules · 원장)에 같은 튜플 · 같은 id · 같은 등록 순서가 나와야 한다
(check.py ③ 이 erd-v3-tuples.json 요약과 키 단위로 대조한다). 유사도·추측 없음.

v3(V3-1~V3-5):
  V3-1 부작용 튜플 (event, site, course, qualifier) — 수식 조각은 같은 멤버 안에서만 · 접두 수식 + 사건 가름(「공기색전」) · 식별자 네 칸
  V3-2 괄호 안 조각 하나가 회사 사전·제품 사전에 닿으면 바깥 what 의 그 회사 제품 / 그 제품
  V3-3 stopwords(resolve_rules.step2_decompose.stopwords) 는 조각이 아니라 qualifier_text · `\\d+차` → session_index
  V3-4 `+` 함께 · `/` 부위 둘 함께·대안 둘 또는 · 괄호 안 대안은 바깥 하나(alternatives) · 「무엇을 하나 × 부위 여럿」→ 튜플 여럿(anchor REF-…#s<i>) · member_mode
  V3-5 site.kind — layer 는 시술 site 칸에 넣지 않는다(layer_fragments)

사전은 `dic_json`(erd-v3-dictionaries.json 모양)으로 받는다 — 결정 ① dictionary_add · canonical_rename 을 적용한 사전을 넘기면
분해가 그 사전으로 다시 돈다(ERD §5.2 「빌드는 분해를 다시 돌린다」).
"""
import re
import unicodedata
from collections import Counter, OrderedDict, defaultdict

from .util import norm, mkid, dedupe

CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")
PRIMARY_KINDS = ("modality", "modality_subcategory", "procedure", "product")
DICT_WHAT_KINDS = ("product", "modality_subcategory", "modality", "ingredient")
SUMMARY_DICT_WHAT_KINDS = ("product", "modality_subcategory", "modality")   # 요약 지표 tuples_dict_what_site_none_ratio 는 참조 구현(erd-v3.2-tuples.py)도 성분을 넣지 않고 센다   # v3.2(V3.2-6): 성분 사전 what 도 사전 값(접힘 가능) — v3.1 이하 분해에는 성분 what 이 없어 차이 없음
END_KINDS = ["procedure", "modality", "subcategory", "product", "unresolved"]
SEP_RE = re.compile(r"([+/&,])")
V32_ROW_KEYS = ("grammar_tokens", "ingredient_fragments", "gloss")
AND_SEPS = {"+", "&", ","}
SESSION_RE = re.compile(r"^(\d+)\s*차$")
COUNT_RE = re.compile(r"^(\d+)\s*회")
PRINCIPLES = OrderedDict([
    ("A", "미상 칸이 하나라도 있으면 다른 이름과 접지 않는다."),
    ("B", "조각을 버리지 않는다. 한 칸에 후보가 둘이면 단위를 둘로 나누거나(부위 「이마/눈가」→ 둘) 미해결로 둔다."),
    ("C", "수식어(경과·부위)는 **같은 멤버 안에서 바로 붙은 사건**에만 준다. 이름 전체에서 끌어오지 않는다."),
    ("D", "표현(adverse_expression)은 단위를 **가리키기만** 한다. 표현에서 새 단위를 만들지 않는다."),
])
V1_NAMES = {"보톡스(턱선+광대)": "보톡스(턱선/광대)", "보톡스 이마+미간": "보톡스 이마/미간", "필러 볼+턱": "필러 볼/턱", "필러 팔자+볼": "필러 팔자/볼"}  # 브론즈 2판 `+` 4곳의 1판 이름(실측 대조)


def with_alias(dic_json):
    """사전 순서의 'procedure' 자리는 catalog_item_name 을 읽는다(ERD §1.3 dictionary_order_note)."""
    d = dict(dic_json)
    ds = list(d["dictionaries"])
    cat = next(x for x in ds if x["name"] == "catalog_item_name")
    if not any(x["name"] == "procedure_name" for x in ds):
        ds.append(dict(cat, name="procedure_name"))
    d["dictionaries"] = ds
    return d


def locator(file, path, record):
    return f"{file}:{path}@{record}"


# ===========================================================================
# 사전 색인 · 개체 id
# ===========================================================================
class Lexicon:
    """§1.3 분해가 읽는 사전 7(계열 · 제품명 · 하위분류 라벨 · 분류 항목 이름 · 부위 · 단위 · 제품 등급)."""

    def __init__(self, dic_json):
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        self.idx = {k: defaultdict(set) for k in ["modality", "product", "modality_subcategory", "procedure", "site", "unit", "product_tier"]}
        src = {"modality": "modality", "product": "product_name", "modality_subcategory": "modality_subcategory_label", "procedure": "procedure_name",
               "site": "site", "unit": "unit", "product_tier": "product_tier"}
        for kind, dname in src.items():
            for e in D[dname]["entries"]:
                code = e.get("code")
                for k in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]:
                    self.idx[kind][norm(k)].add((code, e["canonical"]))
        self.sub_ids = {s["value"] for e in D["modality_subcategory_label"]["entries"] for s in e.get("synonyms", []) if s.get("link") == "code"}
        self.site_entries = D["site"]["entries"]

    def hits(self, kind, text):
        return self.idx[kind].get(norm(text), set())


def site_kind_of(e):
    """부위 사전 값의 kind(V3-5) — 사전에 없으면 얼굴 = region, 그 밖 anatomical(참조 구현 Ids3 와 같은 기본값)."""
    return e.get("kind") or ("region" if e["canonical"] == "얼굴" else "anatomical")


class Ids:
    """개체 id(ERD §1.1 식별자) — 원장 taxonomy + 사전 · v3 색인(부위 kind · 수식 사전 · 회사 · stopwords)."""

    def __init__(self, dic_json, L, resolve_rules=None):
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        tx = L["taxonomy.json"]
        self.v33 = dic_json.get("erd_version") == "v3.3"   # v3.3(V3.3-E): 사건 사전에 category 없음
        self.mod = {m["id"]: {"id": mkid("MOD", m["id"]), "label": m["category"], "family": m["id"]} for m in tx["modality"]}
        self.sub = {}
        self.sub_by_label = defaultdict(list)
        for m in tx["modality"]:
            for sc in m["subcategories"]:
                e = {"id": mkid("SUB", f"{m['id']}|{sc['label']}"), "label": f"{sc['id']} {sc['label']}", "family": m["id"], "code": sc["id"], "raw_label": sc["label"]}
                self.sub[sc["id"]] = e
                self.sub_by_label[(m["id"], norm(sc["label"]))].append(e)
        self.prod = {}
        for e in D["product_name"]["entries"]:
            self.prod[norm(e["canonical"])] = {"id": mkid("PRD", f"{e['code']}|{e['canonical']}"), "label": e["canonical"], "family": e["code"], "code": e["code"]}
        self.site = {}
        for e in D["site"]["entries"]:
            key = e.get("zone_id") if e.get("site_kind") == "backbone" else e["canonical"]
            self.site[norm(e["canonical"])] = {"id": mkid("SIT", key), "label": e["canonical"]}
        self.tech = {norm(e["canonical"]): {"id": e["id"], "label": e["canonical"]} for e in D["technique"]["entries"]}
        self.tech_surface = {}
        for e in D["technique"]["entries"]:
            self.tech_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.tech_surface[norm(s["value"])] = e["canonical"]
        self.family_tech = {}
        for pr in L["procedure-profiles.json"]["profiles"]:
            self.family_tech[pr["id"]] = list(dict.fromkeys(pr["mechanism"]))

        def surf(name):
            ent, sf = {}, {}
            for e in D[name]["entries"]:
                ent[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"]} if self.v33 else {"id": e["id"], "label": e["canonical"], "category": e.get("category")}
                sf[norm(e["canonical"])] = e["canonical"]
                for s in e.get("synonyms", []):
                    sf[norm(s["value"])] = e["canonical"]
            return ent, sf

        self.event, self.event_surface = surf("adverse_event_type")
        # v3.3(V3.3-C(1)): 분해 꼴(decomposed_from · 「혈관 폐색」→ 사건 폐색 + 부위 혈관) — 옛 값·옛 id 로 가리킨 결정이 (사건, 부위)로 닿는다
        self.event_decomposed = {}
        for e in D["adverse_event_type"]["entries"]:
            df = e.get("decomposed_from")
            if isinstance(df, dict) and df.get("value"):
                self.event_decomposed[norm(df["value"])] = {"event": e["canonical"], "site": df.get("site"), "old_id": df.get("old_id"), "rule": df.get("rule")}
                for a in e.get("aliases") or []:
                    self.event_decomposed[a] = self.event_decomposed[norm(df["value"])]
        self.course, self.course_surface = surf("course")
        self.rsite, self.rsite_surface = surf("relative_site")
        self.site_surface = {}
        for e in D["site"]["entries"]:
            self.site_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.site_surface[norm(s["value"])] = e["canonical"]
        # V3-5 부위 kind
        self.site_kind = {norm(e["canonical"]): site_kind_of(e) for e in D["site"]["entries"]}
        # V3-1 수식 사전
        self.qualifier, self.qualifier_surface = {}, {}
        for e in D.get("adverse_qualifier", {"entries": []})["entries"]:
            self.qualifier[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"], "kind": e.get("kind")}
            self.qualifier_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.qualifier_surface[norm(s["value"])] = e["canonical"]
        # V3-2 회사 사전 — 정준값 · 동의어 · `/` 로 이어진 회사명 각각
        self.manufacturer_surface = {}
        for e in D["manufacturer"]["entries"]:
            self.manufacturer_surface[norm(e["canonical"])] = e["canonical"]
            for part in e["canonical"].split("/"):
                self.manufacturer_surface.setdefault(norm(part), e["canonical"])
            for s in e.get("synonyms", []):
                self.manufacturer_surface[norm(s["value"])] = e["canonical"]
        # 제품 → 제조사(원장 products.json · taxonomy products[].manufacturer)
        self.product_company = defaultdict(set)
        for sec, body in L["products.json"].items():
            if isinstance(body, dict):
                for pr in body["products"]:
                    if pr.get("manufacturer") and pr["manufacturer"] != "-":
                        self.product_company[norm(pr["name"])].add(pr["manufacturer"])
        for m in tx["modality"]:
            for pr in m["products"]:
                if pr.get("manufacturer") and pr["manufacturer"] != "-":
                    self.product_company[norm(pr["name"])].add(pr["manufacturer"])
        # V3-3 stopwords
        sw = ((resolve_rules or {}).get("step2_decompose") or {}).get("stopwords", {}) or {}
        self.stopwords = {norm(w["word"]): w["word"] for w in sw.get("words", [])}
        self.stopwords_enabled = True

    def products_of_company(self, family, company_canonical):
        """바깥 what 의 계열 안 제품 중 제조사가 그 회사인 제품(정준값 기준 · `/` 분리 각각)."""
        out = []
        for k, p in self.prod.items():
            if family and family not in str(p["family"]).split("|"):
                continue
            comps = self.product_company.get(k, set())
            for c in comps:
                if self.manufacturer_surface.get(norm(c)) == company_canonical:
                    out.append(p)
                    break
        return out


# ===========================================================================
# §1.3 참조 분해기 (v3: stopwords · 괄호 안 회사 · layer 부위 · 분리 기호 기록)
# ===========================================================================
class Resolver:
    PRIMARY = ("product", "modality_subcategory", "procedure")
    DEPTH = {"modality": "modality", "modality_subcategory": "subcategory", "procedure": "procedure", "product": "product"}

    def __init__(self, lex, rules, ids):
        self.lex = lex
        self.rules = rules
        self.ids = ids
        s2 = rules["step2_decompose"]
        self.paren_re = re.compile(s2["paren_regex"])
        self.combo_re = re.compile("[" + re.escape("".join(s2["combo_symbols"])) + "]")
        self.spec_re = re.compile(s2["spec_regex"])
        self.code_re = re.compile(rules["step1_family"]["code_regex"])
        self.exclude = None  # 분류 항목 자기 이름(자기 참조 금지)
        self.scoped = None   # ② canonical_mapping(라벨 from_ref · scope=REF-) — 이 anchor 를 분해하는 동안만 {norm(조각): (span, 결정 id)}
        self.scoped_used = None

    @staticmethod
    def _in_family(code, family):
        return code is not None and family is not None and family in str(code).split("|")

    def _primary_base(self, text, family, types=None):
        kinds_allowed = [k for k in self.PRIMARY if types is None or k in types]
        allhits = {k: (self.lex.hits(k, text) if k in kinds_allowed else set()) for k in self.PRIMARY}
        if not any(allhits.values()):
            return None
        scoped = {k: {h for h in v if self._in_family(h[0], family)} for k, v in allhits.items()}
        use, cross = (scoped, False) if family and any(scoped.values()) else (allhits, family is not None)
        kinds = [k for k in self.PRIMARY if use[k]]
        kind = "procedure" if "procedure" in kinds else "modality_subcategory" if "modality_subcategory" in kinds else "product"
        hs = use[kind]
        codes = set()
        for h in hs:
            codes |= set(str(h[0]).split("|"))
        if len(codes) > 1 and not (family and family in codes):
            return {"kind": "ambiguous", "text": text, "codes": sorted(codes), "overlap": kinds}
        h = sorted(hs, key=lambda x: str(x))[0]
        code = family if (family and family in codes) else h[0]
        return {"kind": kind, "text": text, "code": code, "canonical": h[1], "overlap": kinds if len(kinds) > 1 else None, "cross_family": cross}

    def primary(self, text, family, types=None):
        p = self._primary_base(text, family, types)
        if p and self.exclude and p["kind"] == "procedure" and norm(p["canonical"]) == self.exclude:
            t = text.strip()
            for k in ("product", "modality_subcategory"):
                h = set(self.lex.hits(k, t))
                if h:
                    hh = {x for x in h if self._in_family(x[0], family)} or h
                    x = sorted(hh, key=lambda z: str(z))[0]
                    return {"kind": k, "text": t, "code": family if (family and family in str(x[0]).split("|")) else x[0], "canonical": x[1], "overlap": None, "cross_family": not self._in_family(x[0], family)}
            return None
        return p

    def classify(self, text, family, types=None):
        """조각 → 사전 kind. 순서: 계열 → 제품 → 하위분류 → 분류 항목 → 부위 → 규격 → 제품 등급."""
        t = text.strip()
        if not t:
            return None
        if self.scoped and norm(t) in self.scoped:
            span, did = self.scoped[norm(t)]
            if self.scoped_used is not None and did not in self.scoped_used:
                self.scoped_used.append(did)
            return dict(span, text=t)
        if types is None or "modality" in types:
            m = self.lex.hits("modality", t)
            if m:
                codes = {h[0] for h in m}
                if len(codes) == 1:
                    c = next(iter(codes))
                    return {"kind": "modality", "text": t, "code": c, "canonical": sorted(m)[0][1]}
        p = self.primary(t, family, types)
        if p:
            return p
        s = self.lex.hits("site", t)
        if s:
            return {"kind": "site", "text": t, "canonical": sorted(s)[0][1]}
        nt = unicodedata.normalize("NFKC", t)
        if self.spec_re.match(nt) or self.lex.hits("unit", t):
            return {"kind": "spec", "text": t, "canonical": nt}
        tier = self.lex.hits("product_tier", t)
        if tier:
            return {"kind": "product_tier", "text": t, "canonical": sorted(tier)[0][1]}
        return None

    def classify2(self, frag, family):
        c = self.classify(frag, family)
        if c is None:
            t = norm(frag)
            if t in self.ids.tech_surface:
                return {"kind": "technique", "text": frag.strip(), "canonical": self.ids.tech_surface[t]}
        return c

    def classify3(self, frag, family, where):
        """v3: layer 부위는 시술 site 가 아니다(layer_site) · 괄호 안에서만 회사 사전(manufacturer)."""
        c = self.classify2(frag, family)
        if c and c["kind"] == "site" and self.ids.site_kind.get(norm(c["canonical"])) == "layer":
            return {"kind": "layer_site", "text": frag.strip(), "canonical": c["canonical"]}
        if c is None and where == "inner":
            t = norm(frag)
            if t in self.ids.manufacturer_surface:
                return {"kind": "manufacturer", "text": frag.strip(), "canonical": self.ids.manufacturer_surface[t]}
        return c

    def is_stop(self, tok):
        return self.ids.stopwords_enabled and norm(tok) in self.ids.stopwords

    def whole(self, label, family, types=None):
        c = self.classify(label, family, types)
        if c and c["kind"] in ("modality", "product", "modality_subcategory", "procedure") and (types is None or c["kind"] in types):
            return c
        return None

    def decompose(self, label, family, exclude=None):
        """묶음(outer/inner) → 멤버(조합 기호 · 앞 기호를 sep 으로 기록) → 조각(사전 순서 · 공백 토큰 최장 구간 · stopwords 는 조각 아님)."""
        self.exclude = exclude
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members, sep = [], None
            for piece in SEP_RE.split(g):
                if piece in ("+", "/", "&", ","):
                    sep = piece
                    continue
                part = piece.strip(" ·")
                if not part:
                    continue
                spans, untouched, stops = [], [], []
                c = self.classify3(part, family, where)
                if c and c["kind"] != "ambiguous":
                    spans.append(c)
                else:
                    toks = part.split()
                    i = 0
                    while i < len(toks):
                        found = None
                        for j in range(len(toks), i, -1):
                            h = self.classify3(" ".join(toks[i:j]), family, where)
                            if h and h["kind"] != "ambiguous":
                                found = (h, j)
                                break
                        if found:
                            spans.append(found[0])
                            i = found[1]
                        else:
                            if self.is_stop(toks[i]):
                                stops.append(toks[i])
                            else:
                                amb = self.classify(toks[i], family)
                                untouched.append({"text": toks[i], "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                            i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched, "stopwords": stops, "sep": sep})
                sep = None
            groups.append({"where": where, "members": members})
        self.exclude = None
        return groups

    def decompose_whole_first(self, label, family, exclude=None):
        """§1.4 v2.1: 통째 일치를 먼저 — 라벨 전체가 사전 값 하나면 쪼개지 않는다."""
        self.exclude = exclude
        try:
            w = self.whole(str(label), family)
        finally:
            self.exclude = None
        if w:
            return [{"where": "outer", "members": [{"text": str(label).strip(), "spans": [w], "untouched": []}]}], True
        return self.decompose(str(label), family, exclude=exclude), False

    def resolve(self, label, hint=None, types=None):
        """§1.3 그대로(resolved · decomposed · unresolved) — step1 제품 대응·canonical_category 에 쓴다."""
        label = str(label)
        family = hint
        w = self.whole(label, family, types)
        if w:
            return {"label": label, "hint": hint, "status": "resolved", "depth": self.DEPTH[w["kind"]], "family": w.get("code") or family,
                    "target": f"{self.DEPTH[w['kind']]}:{w.get('code')}:{w['canonical']}", "overlap": w.get("overlap"), "spans": [w], "untouched": [], "canonical": w["canonical"], "code": w.get("code")}
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        fragments = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            for part in self.combo_re.split(g):
                part = part.strip(" ·")
                if part:
                    fragments.append((where, part))
        spans, untouched = [], []
        for where, frag in fragments:
            c = self.classify(frag, family)
            if c and c["kind"] != "ambiguous":
                c["where"] = where
                spans.append(c)
                continue
            toks = frag.split()
            i = 0
            while i < len(toks):
                found = None
                for j in range(len(toks), i, -1):
                    h = self.classify(" ".join(toks[i:j]), family)
                    if h and h["kind"] != "ambiguous":
                        found = (h, j)
                        break
                if found:
                    found[0]["where"] = where
                    spans.append(found[0])
                    i = found[1]
                else:
                    untouched.append({"text": toks[i], "where": where})
                    i += 1
        status = "unresolved" if untouched else "decomposed"
        return {"label": label, "hint": hint, "status": status, "depth": None, "family": family, "target": None, "spans": spans, "untouched": untouched}


# ===========================================================================
# §1.4 시술 튜플
# ===========================================================================
def ref_anchor(label, hint):
    return mkid("REF", f"{label}|{hint}")


def tuple_id(what_id, site_id, tech_id, what_kind, anchor):
    all_dict = what_kind in DICT_WHAT_KINDS and site_id != "none" and tech_id != "none"
    key = f"{what_id}|{site_id}|{tech_id}" + ("" if all_dict else f"|{anchor}")
    return mkid("PRC", key), all_dict


def _frag(s):
    return f"{s['kind']}:{s['canonical']}"


def _groups_view(groups):
    return [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]],
                                               "stopwords": m.get("stopwords", []), "sep": m.get("sep")} for m in g["members"]]} for g in groups]


def session_tokens(groups):
    """v3.1(V3.1-5) — 규격(spec) 조각 중 `\\d+차`(회차) · `\\d+회`(횟수) 토큰 — 참조 구현 erd-v3.1-tuples.py _session_tokens 와 같다."""
    out = []
    for g in groups:
        for m in g["members"]:
            for s in m["spans"]:
                kind, canon = (s["kind"], s["canonical"]) if isinstance(s, dict) else (s[0], s[1])
                if kind != "spec":
                    continue
                cc = unicodedata.normalize("NFKC", str(canon)).replace(" ", "")
                ms = SESSION_RE.match(cc)
                mc = COUNT_RE.match(cc)
                if ms:
                    out.append({"token": canon, "kind": "차", "value": int(ms.group(1))})
                elif mc:
                    out.append({"token": canon, "kind": "회", "value": int(mc.group(1))})
    return out


def _is_primary_member(m):
    return any(s["kind"] in PRIMARY_KINDS for s in m["spans"])


def _site_only_member(m):
    return bool(m["spans"]) and all(s["kind"] == "site" for s in m["spans"]) and not m["untouched"]


def _primary_only_member(m):
    return bool(m["spans"]) and all(s["kind"] in PRIMARY_KINDS for s in m["spans"]) and not m["untouched"]


UNRESOLVED_REASON = {"multi_primary": "primary 조각 둘 이상(조합 아님) → ⑨ 미해결 (버리고 접지 않음)", "multi_site": "한 멤버 안의 site 조각 둘 이상(분리 기호 없음) → ⑨ 미해결", "multi_technique": "technique 조각 둘 이상 → ⑨ 미해결",
                     "unusable_primary": "what 으로 쓸 수 없는 primary 조각 → ⑨ 미해결", "combo_outside_fragment": "조합 멤버 밖 primary/site 조각 → ⑨ 미해결", "company_product": "괄호 안 회사의 제품이 바깥 계열에 하나가 아님 → ⑨ 미해결", "combo_mixed": "한 라벨에 `+` 와 `/` 가 섞임 → ⑨ 미해결"}


class ProcedureTuples:
    def __init__(self, lex, rules, ids, L, scoped=None):
        self.R = Resolver(lex, rules, ids)
        self.scoped = scoped or {}     # anchor(REF-) → {norm(조각): (span, 결정 id)}
        self.scoped_hits = defaultdict(list)   # 결정 id → anchor
        self.ids = ids
        self.L = L
        self.tuples = OrderedDict()
        self.catalog = OrderedDict()
        self.items = []
        for m in L["taxonomy.json"]["modality"]:
            for si, sc in enumerate(m["subcategories"]):
                for ii, it in enumerate(sc["items"]):
                    self.items.append((m["id"], sc["id"], it["name"]))
        self.item_index = defaultdict(list)
        for fam, sub, name in self.items:
            self.item_index[norm(name)].append((fam, sub, name))
        self.item_ids = {it["id"]: (m["id"], sc["id"], it["name"]) for m in L["taxonomy.json"]["modality"] for sc in m["subcategories"] for it in sc["items"] if it.get("id")}
        self._busy = set()
        self.company_applied = []     # V3-2 (라벨, 회사, 제품)
        self.multi_tuples = []        # V3-4 「무엇을 하나 × 부위 여럿」
        self.alternatives = []        # V3-4 괄호 안 대안

    @staticmethod
    def cat_what(family, name):
        return {"id": mkid("CAT", f"{family}|{name}"), "label": name, "family": family}

    def register(self, what_kind, what, site, tech, origin, src, unregistered, anchor, status_extra=None, matched=None):
        site_id = site["id"] if site else "none"
        tech_id = self.ids.tech[norm(tech)]["id"] if tech else "none"
        tid, all_dict = tuple_id(what["id"], site_id, tech_id, what_kind, anchor)
        t = self.tuples.get(tid)
        if t is None:
            t = {"id": tid, "what_kind": what_kind, "what_id": what["id"], "what_label": what["label"], "family": what.get("family"),
                 "site": site["label"] if site else None, "site_id": site_id, "technique": tech, "technique_id": tech_id, "technique_origin": "fragment" if tech else "none",
                 "all_dict_values": all_dict, "anchor": None if all_dict else anchor, "origins": [], "status": "complete", "unregistered_fragments": [], "sources": []}
            self.tuples[tid] = t
        if origin not in t["origins"]:
            t["origins"].append(origin)
        t["sources"].append(dict(src, anchor=anchor, matched_text=matched if matched is not None else src.get("label")))
        for u in unregistered:
            if u not in t["unregistered_fragments"]:
                t["unregistered_fragments"].append(u)
        if unregistered:
            t["status"] = "partial"
        elif status_extra == "ambiguous" and t["status"] == "complete":
            t["status"] = "ambiguous"
        return tid

    def _what_from_span(self, s, family, for_item):
        k = s["kind"]
        if k == "product":
            e = self.ids.prod.get(norm(s["canonical"]))
            return ("product", e, f"product:{s['canonical']}" + ("(타 계열)" if s.get("cross_family") else ""))
        if k == "modality_subcategory":
            fam = s.get("code")
            cands = self.ids.sub_by_label.get((fam, norm(s["canonical"]))) if fam and "|" not in str(fam) else None
            if not cands:
                return None
            if for_item and fam != family:
                return None
            return ("modality_subcategory", cands[0], f"subcategory:{cands[0]['label']}")
        if k == "modality":
            e = self.ids.mod.get(s.get("code"))
            return ("modality", e, f"modality:{s['canonical']}") if e else None
        return None

    def what_of(self, s, family, for_item):
        if s["kind"] == "procedure":
            fam = s.get("code")
            cands = [x for x in self.item_index.get(norm(s["canonical"]), []) if ("|" not in str(fam) and x[0] == fam) or "|" in str(fam)]
            if not cands:
                cands = self.item_index.get(norm(s["canonical"]), [])
            if not cands:
                return None
            fam2, sub2, name2 = cands[0]
            rec = self.catalog_tuple(fam2, sub2, name2)
            if rec is None or not rec.get("procedure_id") or rec["result"] != "tuple":
                return None
            t = self.tuples[rec["procedure_id"]]
            if for_item and t["what_kind"] not in DICT_WHAT_KINDS:
                return None
            return {"kind": t["what_kind"], "what": {"id": t["what_id"], "label": t["what_label"], "family": t["family"]},
                    "basis": f"catalog_item:{name2}[{fam2}]→{t['what_kind']}:{t['what_label']}",
                    "via_item": {"family": fam2, "name": name2, "cat_id": mkid("CAT", f"{fam2}|{name2}"), "procedure_id": rec["procedure_id"],
                                 "anchor": t["anchor"], "site": (t["site"], t["site_id"]) if t["site_id"] != "none" else None,
                                 "technique": t["technique"] if t["technique_id"] != "none" else None}}
        w = self._what_from_span(s, family, for_item)
        if not w:
            return None
        return {"kind": w[0], "what": w[1], "basis": w[2], "via_item": None}

    # --- v2.2 조립(조합 멤버는 self.assemble — v3 규칙 — 로 내려간다)
    def assemble22(self, groups, family, for_item, anchor, label_text=None):
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        untouched = [u["text"] for g in groups for m in g["members"] for u in m["untouched"]]
        qualifiers = [(s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("spec", "product_tier")]
        frag = {"primaries": [_frag(s) for s in all_spans if s["kind"] in PRIMARY_KINDS],
                "sites": dedupe(s["canonical"] for s in all_spans if s["kind"] == "site"),
                "techniques": dedupe(s["canonical"] for s in all_spans if s["kind"] == "technique")}
        base = {"untouched": untouched, "qualifiers": qualifiers, "fragments": frag}
        if for_item and untouched:
            return dict(base, kind="self", reason="unregistered", status="partial")
        combo_members = None
        for g in groups:
            pm = [m for m in g["members"] if any(s["kind"] in PRIMARY_KINDS for s in m["spans"])]
            if len(pm) >= 2:
                combo_members = pm
                break
        if combo_members is not None:
            cm = {id(m) for m in combo_members}
            subs = [dict(self.assemble([{"where": "member", "members": [m]}], family, for_item, f"{anchor}#m{i}", m["text"]), text=m["text"]) for i, m in enumerate(combo_members)]
            member_fams = {str(x["what"].get("family")) for x in subs if x["kind"] == "tuple"}
            outside = [s for g in groups for m in g["members"] if id(m) not in cm for s in m["spans"]]
            bad = [_frag(s) for s in outside if s["kind"] == "site" or s["kind"] == "technique" or (s["kind"] in PRIMARY_KINDS and not (s["kind"] == "modality" and str(s.get("code")) in member_fams))]
            if bad:
                return dict(base, kind="ambiguous", reason="combo_outside_fragment", status="ambiguous", detail=bad)
            badm = [x for x in subs if x["kind"] != "tuple"]
            if badm:
                return dict(base, kind="ambiguous", reason="combo_member_" + badm[0].get("reason", badm[0]["kind"]), status="ambiguous", detail=[x.get("fragments") for x in badm])
            return dict(base, kind="combo_ref", members=subs, family_fragments=[_frag(s) for s in outside if s["kind"] == "modality"])
        prim, fam_frags, unusable = [], [], []
        for s in all_spans:
            if s["kind"] not in PRIMARY_KINDS:
                continue
            s2 = s
            if s["kind"] == "modality":
                ph = self.R.lex.hits("product", s["text"])
                if ph:
                    hh = {x for x in ph if self.R._in_family(x[0], family)} or ph
                    x = sorted(hh, key=lambda z: str(z))[0]
                    s2 = {"kind": "product", "text": s["text"], "code": x[0], "canonical": x[1], "cross_family": not self.R._in_family(x[0], family)}
                elif for_item:
                    if str(s.get("code")) == str(family):
                        fam_frags.append(s)
                        continue
                    unusable.append(_frag(s))
                    continue
            w = self.what_of(s2, family, for_item)
            if w is None:
                unusable.append(_frag(s))
                continue
            prim.append((s2, w))
        non_mod_fams = {str(w["what"].get("family")) for s2, w in prim if w["kind"] != "modality"}
        keep = []
        for s2, w in prim:
            if w["kind"] == "modality" and str(w["what"].get("family")) in non_mod_fams:
                fam_frags.append(s2)
                continue
            keep.append((s2, w))
        seen, uniq = set(), []
        for s2, w in keep:
            if w["what"]["id"] in seen:
                continue
            seen.add(w["what"]["id"])
            uniq.append((s2, w))
        base["family_fragments"] = [_frag(s) for s in fam_frags]
        if unusable:
            return dict(base, kind="ambiguous", reason="unusable_primary", status="ambiguous", detail=unusable)
        if len(uniq) >= 2:
            return dict(base, kind="ambiguous", reason="multi_primary", status="ambiguous", detail=[w["basis"] for _, w in uniq])
        via = uniq[0][1]["via_item"] if uniq else None
        sites = list(frag["sites"])
        if via and via["site"] and via["site"][0] not in sites:
            sites.append(via["site"][0])
        techs = list(frag["techniques"])
        if via and via["technique"] and via["technique"] not in techs:
            techs.append(via["technique"])
        if len(sites) >= 2:
            return dict(base, kind="ambiguous", reason="multi_site", status="ambiguous", detail=sites)
        if len(techs) >= 2:
            return dict(base, kind="ambiguous", reason="multi_technique", status="ambiguous", detail=techs)
        if uniq:
            s2, w = uniq[0]
            what_kind, what, basis = w["kind"], w["what"], w["basis"]
        elif for_item:
            return dict(base, kind="self", reason="no_primary", status="complete")
        else:
            return dict(base, kind="hint_only")
        site = self.ids.site[norm(sites[0])] if sites else None
        tech = techs[0] if techs else None
        own_anchor = anchor
        exact = (via is not None and len(all_spans) == 1 and all_spans[0]["kind"] == "procedure" and not untouched and label_text is not None and norm(all_spans[0]["text"]) == norm(label_text))
        if exact:
            own_anchor = via["anchor"] or anchor
        return dict(base, kind="tuple", what_kind=what_kind, what=what, what_basis=basis, site=site, technique=tech, anchor=own_anchor,
                    extra_primaries=[], extra_sites=[], via_item=via["name"] if via else None)

    # --- v3 조립: V3-2 회사·제품 괄호 · V3-4 괄호 안 대안 · 무엇을 하나 × 부위 여럿 · combo member_mode · V3-3/V3-5 주석
    def _assemble_members(self, members, family, for_item, anchor, label_text):
        return self.assemble22([{"where": "outer", "members": members}], family, for_item, anchor, label_text)

    @staticmethod
    def _annotate(groups, base):
        mems = [m for g in groups for m in g["members"]]
        base["qualifier_text"] = [t for m in mems for t in m.get("stopwords", [])]
        sess = [int(SESSION_RE.match(unicodedata.normalize("NFKC", s["canonical"]).replace(" ", "")).group(1)) for m in mems for s in m["spans"] if s["kind"] == "spec" and SESSION_RE.match(unicodedata.normalize("NFKC", s["canonical"]).replace(" ", ""))]
        base["session_index"] = sess[0] if sess else None
        base["layer_fragments"] = [s["canonical"] for m in mems for s in m["spans"] if s["kind"] == "layer_site"]
        base["manufacturer_fragments"] = [s["canonical"] for m in mems for s in m["spans"] if s["kind"] == "manufacturer"]
        base.setdefault("member_mode", None)
        base.setdefault("alternatives", None)
        # v3.1(V3.1-5) — 회·차 규격 토큰 · 첫 「회」 = session_count · 첫 「차」 = session_index
        toks = session_tokens(groups)
        base["session_tokens"] = toks
        counts = [t["value"] for t in toks if t["kind"] == "회"]
        base["session_count"] = counts[0] if counts else None
        sx = [t["value"] for t in toks if t["kind"] == "차"]
        base["session_index"] = sx[0] if sx else None
        return base

    @staticmethod
    def _mode_of(members):
        seps = {m["sep"] for m in members[1:]}
        if seps and seps <= AND_SEPS:
            return "and"
        if seps == {"/"}:
            return "or"
        if not seps:
            return None
        return "mixed"

    @staticmethod
    def _manufacturer_scope(groups):
        """V3-2 scope — 회사 사전(manufacturer)은 「inner 묶음 하나 · 멤버 하나 · 조각 하나」일 때만 조각이다. 그 밖에서 회사 사전에 닿은 조각은
        미등록 조각(⑨ · 항목은 partial)으로 되돌린다 — 조각을 버리지 않는다(정의 1). 반환 (groups, 범위 안 회사 조각 여부)."""
        mf = [(gi, mi) for gi, g in enumerate(groups) for mi, m in enumerate(g["members"]) for s in m["spans"] if s["kind"] == "manufacturer"]
        if not mf:
            return groups, False
        inner = [g for g in groups if g["where"] == "inner"]
        in_scope = (len(inner) == 1 and len(inner[0]["members"]) == 1 and len(inner[0]["members"][0]["spans"]) == 1 and not inner[0]["members"][0]["untouched"]
                    and mf == [(groups.index(inner[0]), 0)])
        if in_scope:
            return groups, True
        out = []
        for g in groups:
            ms = []
            for m in g["members"]:
                bad = [s for s in m["spans"] if s["kind"] == "manufacturer"]
                if bad:
                    m = dict(m, spans=[s for s in m["spans"] if s["kind"] != "manufacturer"],
                             untouched=list(m["untouched"]) + [{"text": s["text"], "reason": "회사 사전은 괄호 안 조각 하나일 때만(V3-2)"} for s in bad])
                ms.append(m)
            out.append(dict(g, members=ms))
        return out, False

    def assemble(self, groups, family, for_item, anchor, label_text=None):
        groups, company_scope = self._manufacturer_scope(groups)
        base = self.assemble22(groups, family, for_item, anchor, label_text)
        base = self._annotate(groups, base)
        if base["untouched"]:
            return base  # ⑨ unregistered — 규칙은 사전 값을 만들지 않는다
        outer = groups[0]
        inners = groups[1:]
        outer_prims = [m for m in outer["members"] if _is_primary_member(m)]
        # ---- V3-2 괄호 안 회사·제품 (inner 묶음 하나 · 멤버 하나 · 조각 하나)
        if len(inners) == 1 and len(inners[0]["members"]) == 1 and len(outer_prims) == 1:
            im = inners[0]["members"][0]
            sp0 = im["spans"][0] if len(im["spans"]) == 1 else None
            if sp0 is not None and sp0["kind"] == "procedure" and norm(sp0["canonical"]) in self.ids.prod:
                sp0 = dict(sp0, kind="product", overlap_kind="procedure")
            if sp0 is not None and not im["untouched"] and sp0["kind"] in ("manufacturer", "product"):
                sp = sp0
                sub = self._assemble_members(outer["members"], family, for_item, anchor, label_text)
                sub = self._annotate(groups, sub)
                if sub["kind"] == "tuple" and sub["what_kind"] in ("modality", "modality_subcategory", "product"):
                    fam = str(sub["what"].get("family"))
                    if sp["kind"] == "manufacturer":
                        cands = self.ids.products_of_company(fam if fam != "None" else None, sp["canonical"])
                        if len(cands) == 1:
                            sub.update(what_kind="product", what=cands[0], what_basis=f"company_paren:{sp['canonical']}→product:{cands[0]['label']}", company=sp["canonical"])
                            self.company_applied.append({"label": label_text, "company": sp["canonical"], "product": cands[0]["label"], "family": fam})
                            return sub
                        return dict(base, kind="ambiguous", reason="company_product", status="ambiguous", detail=[p["label"] for p in cands], company=sp["canonical"])
                    e = self.ids.prod.get(norm(sp["canonical"]))
                    if e is not None:
                        sub.update(what_kind="product", what=e, what_basis=f"company_paren:product:{e['label']}" + ("(타 계열)" if fam not in str(e["family"]).split("|") else ""), cross_family=fam not in str(e["family"]).split("|"))
                        self.company_applied.append({"label": label_text, "company": None, "product": e["label"], "family": fam})
                        return sub
        if company_scope:
            # 괄호 안 회사 조각 하나 — 바깥 what(계열명·제품명 하나)이 없거나 사전 값 what 이 아니면 그 회사 제품을 정할 수 없다(⑨ company_product)
            comp = [s["canonical"] for g in groups for m in g["members"] for s in m["spans"] if s["kind"] == "manufacturer"]
            return dict(base, kind="ambiguous", reason="company_product", status="ambiguous", detail=[], company=comp[0] if comp else None)
        # ---- V3-4 괄호 안 대안: inner 묶음 하나가 `/` 로 나뉜 primary 멤버 둘 이상 · 바깥 primary 하나
        alt_groups = [ig for ig in inners if len(ig["members"]) >= 2 and all(_primary_only_member(m) for m in ig["members"]) and self._mode_of(ig["members"]) == "or"]
        other_inner_prims = [m for ig in inners for m in ig["members"] if ig not in alt_groups and _is_primary_member(m)]
        if alt_groups and len(alt_groups) == 1 and len(outer_prims) == 1 and not other_inner_prims:
            sub = self._assemble_members(outer["members"] + [m for ig in inners if ig not in alt_groups for m in ig["members"]], family, for_item, anchor, label_text)
            sub = self._annotate(groups, sub)
            if sub["kind"] == "tuple":
                alts = []
                for m in alt_groups[0]["members"]:
                    w = None
                    for s in m["spans"]:
                        if s["kind"] in PRIMARY_KINDS:
                            w = self.what_of(s, family, False) if s["kind"] != "modality" else {"kind": "modality", "what": self.ids.mod.get(s.get("code")), "basis": f"modality:{s['canonical']}"}
                            break
                    alts.append({"text": m["text"], "fragments": [_frag(s) for s in m["spans"]], "what_kind": w["kind"] if w and w.get("what") else None, "what_id": w["what"]["id"] if w and w.get("what") else None})
                sub.update(member_mode="or", alternatives=alts)
                self.alternatives.append({"label": label_text, "what": f"{sub['what_kind']}:{sub['what']['label']}", "alternatives": [a["text"] for a in alts]})
                return sub
        # ---- V3-4 「무엇을 하나 × 부위 여럿」: primary 멤버 하나 + 부위만 멤버(`+`/`/` 또는 괄호 안) · 그 밖 멤버 없음
        mems = [(g["where"], i, m) for g in groups for i, m in enumerate(g["members"])]
        prim = [(w, i, m) for w, i, m in mems if _is_primary_member(m)]
        siteonly = [(w, i, m) for w, i, m in mems if _site_only_member(m)]
        others = [(w, i, m) for w, i, m in mems if not _is_primary_member(m) and not _site_only_member(m) and (m["spans"] or m["untouched"])]
        if len(prim) == 1 and siteonly and not others:
            pw, pi, pm = prim[0]
            ok_sep = all((w == "inner" and i == 0) or m["sep"] in ("+", "/") or (w == "outer" and i == 0 and pi == 1 and pm["sep"] in ("+", "/")) for w, i, m in siteonly)
            pm_sites = [s for s in pm["spans"] if s["kind"] == "site"]
            if ok_sep and len(pm_sites) <= 1 and len([s for s in pm["spans"] if s["kind"] == "technique"]) <= 1:
                sub = self._assemble_members([pm], family, for_item, anchor, label_text)
                sub = self._annotate(groups, sub)
                # primary 멤버의 site = 그 멤버를 조립한 튜플의 site(멤버 안 부위 조각 · 또는 닿은 분류 항목 튜플의 site — §1.4 site 「참조가 분류 항목에 닿았고
                # 그 항목 튜플에 site 가 있으면 그 값도 센다」) — 시험 tests/test_rules_procedure.SiteTechnique.test_multi_tuple_counts_item_site
                own = [sub["site"]["label"]] if sub["kind"] == "tuple" and sub.get("site") else [s["canonical"] for s in pm_sites]
                sites = dedupe(own + [s["canonical"] for w, i, m in siteonly for s in m["spans"]])
                # ERD §1.3 V3-4 문장 그대로 「부위 여럿」일 때만 — 괄호 안 부위 하나(「X (전체얼굴)」)는 v2.2 그대로 튜플 하나(참조 구현은 결정 뒤 사전에서만 생기는 이 경우를
                # multi_tuple 1 로 만든다 · 결정 전 실측(erd-v3-tuples.json)에는 0 건이라 대조값은 같다)
                if sub["kind"] == "tuple" and len(sites) >= 2:
                    site_objs = [self.ids.site[norm(x)] for x in sites]
                    out = dict(base, kind="multi_tuple", what_kind=sub["what_kind"], what=sub["what"], what_basis=sub["what_basis"], technique=sub["technique"], sites=site_objs,
                               member_mode="and", via_item=sub.get("via_item"), extra_primaries=[], extra_sites=[], symbols=sorted({m["sep"] for w, i, m in siteonly if m["sep"]} | {"()"} if any(w == "inner" for w, i, m in siteonly) else {m["sep"] for w, i, m in siteonly if m["sep"]}))
                    self.multi_tuples.append({"label": label_text, "what": f"{sub['what_kind']}:{sub['what']['label']}", "sites": sites, "symbols": out["symbols"]})
                    return out
        # ---- combo_ref 의 member_mode(V3-4)
        if base["kind"] == "combo_ref":
            cm = None
            for g in groups:
                pm_ = [m for m in g["members"] if _is_primary_member(m)]
                if len(pm_) >= 2:
                    cm = pm_
                    break
            mode = self._mode_of(cm) if cm else None
            if mode == "mixed":
                return dict(base, kind="ambiguous", reason="combo_mixed", status="ambiguous", detail=[m["text"] for m in cm])
            base["member_mode"] = mode or "and"
        return base

    def _self(self, family, name, a):
        what = self.cat_what(family, name)
        f = a["fragments"]
        # multi_site · multi_technique 의 detail = 센 값 전부(멤버 조각 + 닿은 분류 항목 튜플의 값) — §1.4 「항목 자신(ambiguous · multi_site · site=none · extra_sites 에 전부)」
        sites = list(a["detail"]) if a.get("reason") == "multi_site" else list(f["sites"])
        techs = list(a["detail"]) if a.get("reason") == "multi_technique" else list(f["techniques"])
        site = self.ids.site[norm(sites[0])] if len(sites) == 1 else None
        tech = techs[0] if len(techs) == 1 else None
        return {"what_kind": "catalog_item", "what": what, "site": site, "technique": tech,
                "extra_primaries": list(f["primaries"]), "extra_sites": sites if len(sites) != 1 else [],
                "extra_techniques": techs if len(techs) != 1 else []}

    # --- ① 분류 항목 (v2.2 본체)
    def _catalog_tuple22(self, family, sub, name):
        key = (family, name)
        if key in self.catalog:
            return self.catalog[key]
        if key in self._busy:
            return None
        self._busy.add(key)
        cat_id = self.cat_what(family, name)["id"]
        groups, whole = self.R.decompose_whole_first(name, family, exclude=norm(name))
        a = self.assemble(groups, family, True, cat_id, name)
        rec = {"family": family, "subcategory": sub, "name": name, "catalog_item_id": cat_id, "whole_match": whole, "anchor": cat_id,
               "groups": _groups_view(groups), "fragments": a["fragments"], "family_fragments": a.get("family_fragments", [])}
        src = {"origin": "catalog_item", "label": name, "family": family, "catalog_item_id": cat_id}
        if a["kind"] == "combo_ref":
            ids = [self.register(m["what_kind"], m["what"], m["site"], m["technique"], "catalog_item", src, [], m["anchor"], matched=m["text"]) for m in a["members"]]
            rec.update({"result": "combo_ref", "procedure_id": ids[0] if ids else None, "member_ids": ids, "member_pids": list(ids), "member_anchors": [m["anchor"] for m in a["members"]], "unregistered": [], "qualifiers": a["qualifiers"], "what_basis": "combo", "status": "complete",
                        "extra_primaries": [], "extra_sites": []})
        elif a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], "catalog_item", src, [], cat_id)
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "site": a["site"]["label"] if a["site"] else None,
                        "technique": a["technique"], "technique_origin": "fragment" if a["technique"] else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete",
                        "extra_primaries": [], "extra_sites": [], "candidate_name": []})
        else:
            sf = self._self(family, name, a)
            st = a.get("status", "complete")
            tid = self.register("catalog_item", sf["what"], sf["site"], sf["technique"], "catalog_item", src, a["untouched"], cat_id, status_extra=st)
            self.tuples[tid]["candidate_name"] = list(a["untouched"])
            reason = a.get("reason")
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": "catalog_item", "what_basis": f"self:{reason}", "self_reason": reason, "self_detail": a.get("detail", []),
                        "site": sf["site"]["label"] if sf["site"] else None, "technique": sf["technique"], "technique_origin": "fragment" if sf["technique"] else "none",
                        "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": st, "candidate_name": list(a["untouched"]),
                        "extra_primaries": sf["extra_primaries"], "extra_sites": sf["extra_sites"], "extra_techniques": sf["extra_techniques"]})
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    # --- ① 분류 항목 — v3(multi_tuple · 주석)
    def catalog_tuple(self, family, sub, name):
        key = (family, name)
        if key in self.catalog:
            return self.catalog[key]
        if key in self._busy:
            return None
        self._busy.add(key)
        cat_id = self.cat_what(family, name)["id"]
        groups, whole = self.R.decompose_whole_first(name, family, exclude=norm(name))
        a = self.assemble(groups, family, True, cat_id, name)
        if a["kind"] != "multi_tuple":
            self._busy.discard(key)
            self.catalog.pop(key, None)
            rec = self._catalog_tuple22(family, sub, name)
            for k_ in ("qualifier_text", "session_index", "layer_fragments", "manufacturer_fragments", "member_mode", "alternatives"):
                rec[k_] = a.get(k_)
            rec["company"] = a.get("company")
            for k_ in V32_ROW_KEYS:   # v3.2 보존 조각(분해기 ProcedureTuples32 가 낼 때만)
                if a.get(k_):
                    rec[k_] = list(a[k_])
            return rec
        rec = {"family": family, "subcategory": sub, "name": name, "catalog_item_id": cat_id, "whole_match": whole, "anchor": cat_id,
               "groups": _groups_view(groups), "fragments": a["fragments"], "family_fragments": a.get("family_fragments", [])}
        src = {"origin": "catalog_item", "label": name, "family": family, "catalog_item_id": cat_id}
        anchors = [f"{cat_id}#s{i}" for i in range(len(a["sites"]))]
        ids = [self.register(a["what_kind"], a["what"], st, a["technique"], "catalog_item", dict(src, site_index=i), [], anchors[i], matched=name) for i, st in enumerate(a["sites"])]
        rec.update({"result": "multi_tuple", "procedure_id": ids[0], "member_ids": ids, "member_pids": list(ids), "member_anchors": anchors, "member_mode": "and", "unregistered": [], "qualifiers": a["qualifiers"], "what_basis": a["what_basis"], "status": "complete",
                    "extra_primaries": [], "extra_sites": [], "sites": [s["label"] for s in a["sites"]], "qualifier_text": a["qualifier_text"], "session_index": a["session_index"], "layer_fragments": a["layer_fragments"], "manufacturer_fragments": a["manufacturer_fragments"], "alternatives": None})
        for k_ in V32_ROW_KEYS:
            if a.get(k_):
                rec[k_] = list(a[k_])
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    def run_catalog(self):
        for fam, sub, name in self.items:
            self.catalog_tuple(fam, sub, name)

    # --- ② ③ 참조
    def run_reference(self, label, hint, origin, slot):
        """v3.1(V3.1-5) — 회·차 규격: R12 자리면 첫 값을 session_index / session_count(둘째부터는 qualifier_text) · R9/R17/R18/③ 는 qualifier_text 만."""
        r = self._run_reference3(label, hint, origin, slot)
        rel = SLOT_RELATION.get(slot, "—") if slot != MARKET_SLOT else "—"
        toks = session_tokens(r.get("groups") or [])
        r["session_tokens"] = toks
        r["session_relation"] = rel
        if rel == "R12":
            r["session_target"] = "R12.session_index/session_count" if toks else None
            sess = [x["value"] for x in toks if x["kind"] == "차"]
            cnts = [x["value"] for x in toks if x["kind"] == "회"]
            r["session_index"] = sess[0] if sess else None
            r["session_count"] = cnts[0] if cnts else None
            extra = [t["token"] for i, t in enumerate(toks) if any(t2["kind"] == t["kind"] for t2 in toks[:i])]
            if extra:
                r["qualifier_text"] = list(r.get("qualifier_text") or []) + extra
        else:
            if toks:
                r["qualifier_text"] = list(r.get("qualifier_text") or []) + [t["token"] for t in toks]
                r["session_target"] = "qualifier_text"
            else:
                r["session_target"] = None
            r["session_index"] = None
            r["session_count"] = None
        return r

    def _run_reference3(self, label, hint, origin, slot):
        anc = ref_anchor(label, hint)
        if label is None and hint in self.ids.mod:
            label = "__MODALITY__" + hint     # 「M9」 처럼 코드만 적힌 노드(synergy `M코드-이름` 의 이름 없음)
        elif isinstance(label, str) and label in self.ids.mod:
            label = "__MODALITY__" + label
        elif isinstance(label, str) and label in self.ids.sub:
            label = "__SUBID__" + label
        elif isinstance(label, str) and label in self.item_ids:
            # 분류 항목 id(M8-1-1 · auto-…) — 그 항목의 튜플이 끝(anchor = CAT- · 조합·부위 여럿 항목은 anchor 가 멤버 튜플로 풀린다)
            fam, sub_, name = self.item_ids[label]
            rec = self.catalog_tuple(fam, sub_, name)
            return {"label": label, "hint": hint, "ref_id": anc, "result": "tuple", "procedure_id": rec["procedure_id"], "anchor": rec["catalog_item_id"], "via_item": name, "via_item_id": label,
                    "what_kind": self.tuples[rec["procedure_id"]]["what_kind"], "what_basis": f"catalog_item_id:{label}", "status": rec["status"], "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"procedure:{name}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [], "whole_match": True, "groups": [],
                    "family_fragments": [], "qualifier_text": [], "session_index": None, "layer_fragments": [], "manufacturer_fragments": [], "member_mode": None, "alternatives": None, "company": None,
                    "technique": None, "technique_origin": "none", "site": None}
        if isinstance(label, str) and label.startswith("__MODALITY__"):
            code = label[12:]
            return {"label": code, "hint": code, "ref_id": anc, "result": "node", "end_kind": "modality", "end_id": self.ids.mod[code]["id"], "what_basis": "modality_code", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality:{code}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [],
                    "qualifier_text": [], "session_index": None, "layer_fragments": [], "member_mode": None, "alternatives": None}
        if isinstance(label, str) and label.startswith("__SUBID__"):
            sid = label[9:]
            e = self.ids.sub[sid]
            return {"label": sid, "hint": hint, "ref_id": anc, "result": "node", "end_kind": "subcategory", "end_id": e["id"], "what_basis": "subcategory_id", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality_subcategory:{e['label']}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [],
                    "qualifier_text": [], "session_index": None, "layer_fragments": [], "member_mode": None, "alternatives": None}
        self.R.scoped, self.R.scoped_used = self.scoped.get(anc), []
        try:
            groups, whole = self.R.decompose_whole_first(label, hint)
        finally:
            for did in self.R.scoped_used:
                if anc not in self.scoped_hits[did]:
                    self.scoped_hits[did].append(anc)
            self.R.scoped, self.R.scoped_used = None, None
        a = self.assemble(groups, hint, False, anc, str(label))
        base = {"label": label, "hint": hint, "ref_id": anc, "whole_match": whole, "fragments": a["fragments"], "family_fragments": a.get("family_fragments", []), "groups": _groups_view(groups),
                "qualifier_text": a.get("qualifier_text", []), "session_index": a.get("session_index"), "layer_fragments": a.get("layer_fragments", []), "manufacturer_fragments": a.get("manufacturer_fragments", []),
                "member_mode": a.get("member_mode"), "alternatives": a.get("alternatives"), "company": a.get("company")}
        for k_ in V32_ROW_KEYS:   # v3.2 보존 조각(분해기 ProcedureTuples32 가 낼 때만)
            if a.get(k_):
                base[k_] = list(a[k_])
        src = {"origin": origin, "slot": slot, "label": label, "family": hint, "ref_id": anc}
        if a["untouched"]:
            base.update({"result": "unresolved", "unresolved_reason": "unregistered", "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "reason": "미등록 조각 있음 → ⑨ 미해결",
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "ambiguous":
            base.update({"result": "unresolved", "unresolved_reason": a["reason"], "unregistered": [], "qualifiers": a["qualifiers"], "detail": a.get("detail"),
                         "reason": UNRESOLVED_REASON.get(a["reason"], a["reason"] + " → ⑨ 미해결"),
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "multi_tuple":
            anchors = [f"{anc}#s{i}" for i in range(len(a["sites"]))]
            ids = [self.register(a["what_kind"], a["what"], st, a["technique"], origin, dict(src, site_index=i, member=True), [], anchors[i], matched=str(label)) for i, st in enumerate(a["sites"])]
            base.update({"result": "multi_tuple", "member_ids": ids, "member_pids": list(ids), "member_anchors": anchors, "member_count": len(ids), "member_mode": "and", "what_kind": a["what_kind"], "what_basis": a["what_basis"], "sites": [s["label"] for s in a["sites"]], "technique": a["technique"],
                         "symbols": a["symbols"], "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "extra_primaries": [], "extra_sites": []})
            return base
        if a["kind"] == "combo_ref":
            ids = [self.register(m["what_kind"], m["what"], m["site"], m["technique"], origin, dict(src, member=True), [], m["anchor"], matched=m["text"]) for m in a["members"]]
            base.update({"result": "combo_ref", "member_ids": dedupe(ids), "member_pids": list(ids), "member_anchors": [m["anchor"] for m in a["members"]], "member_count": len(a["members"]), "member_mode": a.get("member_mode") or "and",
                         "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "extra_primaries": [], "extra_sites": []})
            return base
        if a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], origin, src, [], a["anchor"])
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "site": a["site"]["label"] if a["site"] else None, "technique": a["technique"],
                         "technique_origin": "fragment" if a["technique"] else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "anchor": a["anchor"], "via_item": a.get("via_item"),
                         "extra_primaries": [], "extra_sites": []})
            return base
        if hint and hint in self.ids.mod:
            f = a["fragments"]
            site = self.ids.site[norm(f["sites"][0])] if f["sites"] else None
            tech = f["techniques"][0] if f["techniques"] else None
            tid = self.register("modality", self.ids.mod[hint], site, tech, origin, src, [], anc)
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": "modality", "what_basis": f"hint_family:{hint}", "site": site["label"] if site else None, "technique": tech,
                         "technique_origin": "fragment" if tech else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "anchor": anc, "extra_primaries": [], "extra_sites": []})
            return base
        base.update({"result": "none", "unregistered": [], "qualifiers": a["qualifiers"], "reason": "primary 조각도 계열 힌트도 없음", "extra_primaries": [], "extra_sites": list(a["fragments"]["sites"])})
        return base


def tids_of(r):
    return [r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", []) if r["result"] in ("combo_ref", "multi_tuple") else []


# ---------------------------------------------------------------------------
# 참조 자리(② 13 + ③ market-pricing) — v1.1 §9.2 자리 그대로. 자리마다 (label, hint, types, 원장 위치 목록)
# ---------------------------------------------------------------------------
MC = re.compile(r"^(M\d+)(?:[-_ ](.+))?$")


def split_code(s):
    m = MC.match(s)
    return (m.group(1), m.group(2)) if m else (None, s)


SLOT_RELATION = OrderedDict([
    ("synergy.links[].from/to (노드 52)", "R18"),
    ("problem-packages.procedures[].name (시술 종류 29)", "R9"),
    ("problem-packages.combos[].combo[] (멤버 29)", "R12"),
    ("problem-packages.procedures[].products[] (제품 34)", "R9"),
    ("procedure-comparison.procedures[].name (39)", "R12"),
    ("treatment-optimization.optimal_combo[] (57)", "R12"),
    ("treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", "R17"),
    ("treatment-optimization.annual_plans.schedule[].procedures[] (29)", "R12"),
    ("treatment-sequence.sequence_order[].categories[] (19)", "R18"),
    ("treatment-sequence.incompatible_same_day[].pair[] (14 distinct)", "R18"),
    ("treatment-sequence.minimum_intervals from/to (14 distinct)", "R18"),
    ("treatment-sequence.common_combos[].sequence[] (22 distinct)", "R12"),
    ("post-procedure-timeline.timelines[].name (10)", "R15"),
])
MARKET_SLOT = "market-pricing.items[].name (122)"


def slot_items(L, lex):
    """{slot: [(label, hint, types)]} — 참조 구현 slot_items 와 같은 순서·같은 항목(중복 포함, 실행 시 (label,hint) 로 거른다)."""
    S = OrderedDict()
    nodes = Counter()
    for l in L["synergy.json"]["links"]:
        nodes[l["from"]] += 1
        nodes[l["to"]] += 1
    S["synergy.links[].from/to (노드 52)"] = [(lab, code, None) for nd in nodes for code, lab in [split_code(nd)]]
    pp = L["problem-packages.json"]
    seen = OrderedDict()
    for p in pp["problems"]:
        for c in p["complaints"]:
            for pr in c["procedures"]:
                seen[(pr["name"], pr["category"])] = 1
    S["problem-packages.procedures[].name (시술 종류 29)"] = [(n, h, None) for n, h in seen]
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for cb in c["combos"] for x in cb["combo"])
    S["problem-packages.combos[].combo[] (멤버 29)"] = [(n, None, None) for n in seen]
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for pr in c["procedures"] for x in pr["products"])
    S["problem-packages.procedures[].products[] (제품 34)"] = [(n, None, ("product",)) for n in seen]
    pc = L["procedure-comparison.json"]
    S["procedure-comparison.procedures[].name (39)"] = [(pr["name"], pr["category"], None) for c in pc["comparisons"] for pr in c["procedures"]]
    to = L["treatment-optimization.json"]
    seen = Counter(x for c in to["by_concern"] for s in c["severity_levels"] for x in s["optimal_combo"])
    S["treatment-optimization.optimal_combo[] (57)"] = [(n, None, None) for n in seen]
    seen = Counter(x for g in to["by_age_group"] for k in ["recommended_base", "avoid", "upgrade"] for x in g.get(k, []))
    S["treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)"] = [(n, None, None) for n in seen]
    seen = Counter(x for pl in to["annual_plans"] for s in pl["schedule"] for x in s["procedures"])
    S["treatment-optimization.annual_plans.schedule[].procedures[] (29)"] = [(n, None, None) for n in seen]
    ts = L["treatment-sequence.json"]
    items = []
    for s in ts["sequence_order"]:
        for c in s["categories"]:
            items.append(seq_category_item(c, lex))
    S["treatment-sequence.sequence_order[].categories[] (19)"] = items
    S["treatment-sequence.incompatible_same_day[].pair[] (14 distinct)"] = [(x, None, None) for p in ts["incompatible_same_day"] for x in p["pair"]]
    S["treatment-sequence.minimum_intervals from/to (14 distinct)"] = [(x, None, None) for m in ts["minimum_intervals"] for x in (m["from"], m["to"])]
    S["treatment-sequence.common_combos[].sequence[] (22 distinct)"] = [(x, None, None) for c in ts["common_combos"] for x in c["sequence"]]
    ppt = L["post-procedure-timeline.json"]
    S["post-procedure-timeline.timelines[].name (10)"] = [(t["name"], split_code(t["category"])[0], None) for t in ppt["timelines"]]
    mp = L["market-pricing.json"]
    S[MARKET_SLOT] = [(i["name"], c["id"], None) for c in mp["categories"] for i in c["items"]]
    return S


def seq_category_item(c, lex):
    code, lab = split_code(c)
    if code and lab is None:
        return ("__MODALITY__" + code, code, None)
    if code and c in lex.sub_ids:
        return ("__SUBID__" + c, code, None)
    return (lab if lab else c, code, None)


def ref_key(label, hint):
    """원장 위치 → 참조 행 키. 참조 행은 (label, hint) 로 하나(같은 라벨·힌트 = 같은 참조)."""
    return (label, hint)



# ---------------------------------------------------------------------------
# §9.5.8 엣지 자리별 끝 분포 — 참조 구현 edge_ends(v3: multi_tuple · member_mode) 그대로(집계용)
# ---------------------------------------------------------------------------
def edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids):
    cat = {(r["family"], r["name"]): r for r in cat_recs}
    item_by_id = {}
    for m in L["taxonomy.json"]["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                item_by_id[it["id"]] = (m["id"], it["name"])
    sub_ids = set(ids.sub)
    mod_ids = set(ids.mod)

    def classify_code(v):
        v = str(v)
        if v in mod_ids:
            return ("modality", ids.mod[v]["id"], None)
        if v in sub_ids:
            return ("subcategory", ids.sub[v]["id"], None)
        if v in item_by_id:
            fam, name = item_by_id[v]
            rec = cat[(fam, name)]
            return ("procedure", rec.get("procedure_id"), rec["catalog_item_id"])
        return ("unresolved", None, None)

    rows = []

    def text_row(slot, rel, rrows, product_slot=False):
        c = Counter()
        mm = Counter()
        n_multi = 0
        for r in rrows:
            if r["result"] == "tuple":
                c["product" if product_slot else "procedure"] += 1
                mm[r.get("member_mode")] += 1
            elif r["result"] in ("combo_ref", "multi_tuple"):
                c["procedure"] += 1
                mm[r.get("member_mode")] += 1
                n_multi += 1 if r["result"] == "multi_tuple" else 0
            elif r["result"] == "node":
                c[r["end_kind"]] += 1
            else:
                c["unresolved"] += 1
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("kind", "text"), ("n", len(rrows))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("member_mode_and", mm.get("and", 0)), ("member_mode_or", mm.get("or", 0)), ("multi_tuple", n_multi)]))

    for slot, rrows in ref_rows.items():
        text_row(slot, SLOT_RELATION[slot], rrows, product_slot=slot.startswith("problem-packages.procedures[].products[]"))
    text_row(MARKET_SLOT, "—", mk_rows)

    def code_row(slot, rel, values):
        c = Counter()
        for v in values:
            if isinstance(v, tuple) and v[0] == "item":
                c["procedure"] += 1
            elif isinstance(v, tuple) and v[0] == "product":
                c["product" if ids.prod.get(norm(v[2])) else "unresolved"] += 1
            else:
                c[classify_code(v)[0]] += 1
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("kind", "code"), ("n", len(values))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("member_mode_and", 0), ("member_mode_or", 0), ("multi_tuple", 0)]))

    r3 = [r for r in cat_recs if r["result"] == "tuple" and r.get("what_kind") == "product" and r.get("whole_match") and str(r.get("what_basis", "")).startswith("product:") and "(타 계열)" not in str(r.get("what_basis", ""))]
    rows.append(OrderedDict([("slot", "taxonomy.json:modality[].subcategories[].items[].name = 같은 계열 제품명 (①)"), ("relation", "R3"), ("kind", "code"), ("n", len(r3))] + [(k, (len(r3) if k == "procedure" else 0)) for k in END_KINDS]
                            + [("member_mode_and", 0), ("member_mode_or", 0), ("multi_tuple", 0)]))
    comp = L["complications.json"]
    code_row("complications.json:categories[].id (10)", "R15", [c["id"] for c in comp["categories"]])
    code_row("pih-risk.json:procedures[].procedure_ref (26)", "R15", [p["procedure_ref"] for p in L["pih-risk.json"]["procedures"]])
    tl = L["post-procedure-timeline.json"]
    code_row("post-procedure-timeline.json:timelines[].category (10)", "R15", [t["category"] for t in tl["timelines"]])
    code_row("post-procedure-timeline 문구 (R29 → R15)", "R15", [t["category"] for t in tl["timelines"] for ph in t["phases"] for k in ("normal", "abnormal", "caution", "emergency") for _ in (ph.get(k) or [])])
    code_row("consent-checklist emergency_signs (R29 → R15)", "R15", [c["id"] for c in L["consent-checklist.json"]["categories"] for _ in (c.get("emergency_signs") or [])])
    ex = L["extracted.json"]
    code_row("extracted safety (R29 → R15)", "R15", [code for code, v in ex.items() if CODE_KEY_RE.match(code) for k in ("common", "uncommon", "serious", "emergency") for _ in ((v.get("safety") or {}).get(k) or [])])
    tx = L["taxonomy.json"]
    code_row("taxonomy modality safety (R29 → R15)", "R15", [m["id"] for m in tx["modality"] for k in ("common", "uncommon", "serious") for _ in (((m.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy item safety (R29 → R15)", "R15", [("item", m["id"], it["name"]) for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"] for k in ("common", "serious", "common_adverse_effects", "serious_adverse_effects", "long_term") for _ in (((it.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy product safety (R29 → R15)", "R15", [("product", m["id"], pr["name"]) for m in tx["modality"] for pr in m["products"] for k in ("common", "serious", "common_side_effects") for _ in (((pr.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    lit = L["literature-evidence.json"]
    code_row("literature adverse_effects (R29 → R15)", "R15", [code for code, c in lit["categories"].items() for _ in (c.get("adverse_effects") or [])])
    code_row("consent-checklist.json:categories[].id (17)", "R16", [c["id"] for c in L["consent-checklist.json"]["categories"]])
    code_row("pre-procedure-checklist.json:category_specific[].id (17)", "R16", [c["id"] for c in L["pre-procedure-checklist.json"]["category_specific"]])
    code_row("contraindications.json:rules[].from/to (27×2)", "R18", [x for r in L["contraindications.json"]["rules"] for x in (r["from"], r["to"])])
    code_row("combo-recipes.json:recipes[].procedures[] (M 코드)", "R12", [x for r in L["combo-recipes.json"]["recipes"] for x in r["procedures"]])
    code_row("problem-combos.json:combos[].packages[].procedures[] (M 코드)", "R12", [x for c in L["problem-combos.json"]["combos"] for p in c["packages"] for x in p["procedures"]])
    tot, by_rel = Counter(), OrderedDict()
    for r in rows:
        if r["relation"] == "—":
            continue
        d = by_rel.setdefault(r["relation"], Counter())
        for k in END_KINDS:
            tot[k] += r[k]
            d[k] += r[k]
        d["n"] += r["n"]
    live = [r for r in rows if r["relation"] != "—"]
    return {"rows": rows, "total": dict(tot), "total_n": sum(r["n"] for r in live), "by_relation": {k: dict(v) for k, v in by_rel.items()},
            "text_slots": sum(1 for r in live if r["kind"] == "text"), "code_slots": sum(1 for r in rows if r["kind"] == "code"),
            "relations_covered": sorted({r["relation"] for r in live}, key=lambda x: int(x[1:])),
            "member_mode": {"and": sum(r["member_mode_and"] for r in live), "or": sum(r["member_mode_or"] for r in live)}, "multi_tuple_ends": sum(r["multi_tuple"] for r in live)}


def scoped_label_spans(decisions, ids):
    """② canonical_mapping 중 from_ref 가 라벨(조각)이고 scope 가 REF- anchor 목록인 것 → {anchor: {norm(조각): (span, 결정 id)}}.
    ERD §5.2: from_ref 를 to_id 로 읽는다(scope 의 anchor 안에서만). 미해결 참조는 튜플이 없어 분해 때 읽어야 한다."""
    out = {}
    for d in decisions:
        if not is_scoped_label_mapping(d):
            continue
        to = d["new_value"]["to_id"]
        span = None
        for code, m in ids.mod.items():
            if m["id"] == to:
                span = {"kind": "modality", "code": code, "canonical": m["label"]}
        for sid, e in ids.sub.items():
            if e["id"] == to:
                span = {"kind": "modality_subcategory", "code": e["family"], "canonical": e["raw_label"], "overlap": None, "cross_family": False}
        for e in ids.prod.values():
            if e["id"] == to:
                span = {"kind": "product", "code": e["code"], "canonical": e["label"], "overlap": None, "cross_family": False}
        if span is None:
            continue
        for a in d["target"]["scope"]:
            out.setdefault(a, {})[norm(d["target"]["from_ref"])] = (span, d["id"])
    return out


ID_PREFIX = re.compile(r"^(R5:|MOD-|SUB-|PRD-|TEC-|CAT-|REF-|DIC-)")


def is_scoped_label_mapping(d):
    t = d.get("target") or {}
    sc = t.get("scope") or []
    return d.get("kind") == "canonical_mapping" and isinstance(t.get("from_ref"), str) and not ID_PREFIX.match(t["from_ref"]) and sc and sc != ["*"] and all(str(a).startswith("REF-") for a in sc)


def _run_slots(PT, S):
    ref_rows = OrderedDict()
    mk_rows = []
    for slot, items in S.items():
        rows, seen = [], set()
        origin = "market_pricing" if slot == MARKET_SLOT else "reference"
        for label, hint, types in items:
            if (label, hint) in seen:
                continue
            seen.add((label, hint))
            row = PT.run_reference(label, hint, origin, slot)
            row["_in"] = [label, hint]
            rows.append(row)
        if slot == MARKET_SLOT:
            mk_rows = rows
        else:
            ref_rows[slot] = rows
    return ref_rows, mk_rows


def run_procedure(dic_json, resolve_rules, L, scoped_decisions=None, prev_tuples=None, bronze_version=2, pt_cls=None):
    """① 분류 항목 → ② 참조 → ③ market-pricing. stopwords 를 끈 실행(V3-3 전후 대조용 · 수치만)을 먼저 한 번 더 돌린다(참조 구현과 같은 순서).
    반환: PT, ids, lex, cat_recs, ref_rows, mk_rows, summary."""
    lex = Lexicon(with_alias(dic_json))
    S = slot_items(L, lex)
    scoped0 = scoped_label_spans(scoped_decisions or [], Ids(dic_json, L, resolve_rules))
    # stopwords 전(V3-3 비교용)
    ids0 = Ids(dic_json, L, resolve_rules)
    ids0.stopwords_enabled = False
    pt_cls = pt_cls or ProcedureTuples   # v3.2: lib.v32.ProcedureTuples32(토큰화 · 병기 · 성분 what)
    PT0 = pt_cls(lex, resolve_rules, ids0, L, scoped0)
    PT0.run_catalog()
    ref0, mk0 = _run_slots(PT0, S)
    # 본 실행
    ids = Ids(dic_json, L, resolve_rules)
    PT = pt_cls(lex, resolve_rules, ids, L, scoped_label_spans(scoped_decisions or [], ids))
    PT.run_catalog()
    cat_recs = list(PT.catalog.values())
    ref_rows, mk_rows = _run_slots(PT, S)
    summary = procedure_summary(PT, ids, lex, cat_recs, ref_rows, mk_rows, L, resolve_rules, (list(PT0.catalog.values()), ref0, mk0), prev_tuples, bronze_version, dic_json)
    return {"PT": PT, "ids": ids, "lex": lex, "cat_recs": cat_recs, "ref_rows": ref_rows, "mk_rows": mk_rows, "slots": S, "summary": summary}


def value_dictionaries(dic_json):
    return [d for d in dic_json["dictionaries"] if d.get("kind") != "phrase_index"]


def stopword_overlap(dic_json, resolve_rules):
    """v3.1(V3.1-6) — stopword 와 정규화 완전 일치하는 사전 값·동의어(값 사전 전수 · 문구 사전 phrase_dictionary 는 분해가 쓰는 색인이라 뺀다 — ERD §9.5.13 「48 사전」)."""
    out = []
    for w in resolve_rules["step2_decompose"]["stopwords"]["words"]:
        hits = []
        for d in value_dictionaries(dic_json):
            for e in d["entries"]:
                if norm(e["canonical"]) == norm(w["word"]):
                    hits.append({"name": d["name"], "canonical": e["canonical"], "as": "canonical"})
                for sy in e.get("synonyms", []):
                    if norm(sy["value"]) == norm(w["word"]):
                        hits.append({"name": d["name"], "canonical": e["canonical"], "as": "synonym"})
        if hits:
            out.append({"word": w["word"], "dictionaries": hits})
    return out


def procedure_summary(PT, ids, lex, cat_recs, ref_rows, mk_rows, L, resolve_rules, run0, v24tup=None, bronze_version=2, dic_json=None):
    """참조 구현 erd-v3-tuples.py run_all 의 procedure.summary 와 같은 키·같은 값(check ③ 이 키마다 대조)."""
    T = PT.tuples
    cat0, ref0, mk0 = run0
    n_cat = len(cat_recs)
    cat_tuple_ids = [x for r in cat_recs for x in tids_of(r)]
    cat_distinct = list(dict.fromkeys(cat_tuple_ids))

    def slot_summary(rows):
        c = Counter(r["result"] for r in rows)
        st = Counter(r.get("status") for r in rows if r["result"] in ("tuple", "combo_ref", "multi_tuple"))
        return {"n": len(rows), "tuple": c.get("tuple", 0), "multi_tuple": c.get("multi_tuple", 0), "combo_ref": c.get("combo_ref", 0), "node": c.get("node", 0), "unresolved": c.get("unresolved", 0), "none": c.get("none", 0), "complete": st.get("complete", 0), "partial": st.get("partial", 0),
                "unresolved_by_reason": dict(Counter(r.get("unresolved_reason") for r in rows if r["result"] == "unresolved")),
                "node_by_kind": dict(Counter(r.get("end_kind") for r in rows if r["result"] == "node")),
                "member_mode": dict(Counter(r.get("member_mode") for r in rows if r.get("member_mode"))),
                "with_alternatives": sum(1 for r in rows if r.get("alternatives")), "with_qualifier_text": sum(1 for r in rows if r.get("qualifier_text")), "with_session_index": sum(1 for r in rows if r.get("session_index") is not None),
                "distinct_tuples": len({x for r in rows for x in tids_of(r) if x}),
                "new_tuples_not_from_catalog": len({x for r in rows for x in tids_of(r) if x and "catalog_item" not in T[x]["origins"]}),
                "whole_match": sum(1 for r in rows if r.get("whole_match")),
                "by_what_kind": dict(Counter(T[x]["what_kind"] for r in rows for x in tids_of(r) if x))}

    folded = []
    for tid in cat_distinct:
        names = [r for r in cat_recs if tid in tids_of(r)]
        t = T[tid]
        own_unreg = list(dict.fromkeys(u for r in names for u in r.get("unregistered", [])))
        folded.append({"procedure_id": tid, "what_kind": t["what_kind"], "what": t["what_label"], "n_items": len(names), "item_status": [r.get("status") for r in names], "all_dict_values": t["all_dict_values"], "unregistered": own_unreg})
    multi_anchor = []
    for t in T.values():
        anchors = list(dict.fromkeys(s["anchor"] for s in t["sources"]))
        if len(anchors) >= 2:
            multi_anchor.append({"procedure_id": t["id"], "all_dict_values": t["all_dict_values"]})
    # V3-8: 기법 상속 후보 — 계열 + 하위분류별 scope
    inh = []
    for fam, techs in sorted(ids.family_tech.items()):
        if len(techs) != 1:
            continue
        ts = [t for t in T.values() if t["technique_id"] == "none" and str(t.get("family")) == fam]
        cat_items = [r for r in cat_recs if r["family"] == fam and r.get("technique_origin") == "none"]
        by_sub = OrderedDict()
        for r in cat_items:
            by_sub.setdefault(r["subcategory"], []).append(r)
        inh.append({"kind": "canonical_mapping", "from_ref": f"R5:{fam}", "to_technique": techs[0], "to_id": ids.tech[norm(techs[0])]["id"], "scope": [r["catalog_item_id"] for r in cat_items], "scope_note": f"technique=none 인 {fam} 분류 항목의 CAT- id 전부(참조 튜플은 REF- 로 따로) · v3: 하위분류 단위 from_ref=R5:<하위분류 id> 로 scope 를 가를 수 있다",
                    "tuples": len(ts), "catalog_items": len(cat_items), "items": [r["name"] for r in cat_items],
                    "by_subcategory": [{"from_ref": f"R5:{sub}", "subcategory": sub, "label": ids.sub[sub]["label"] if sub in ids.sub else sub, "catalog_items": len(rs), "scope": [r["catalog_item_id"] for r in rs], "items": [r["name"] for r in rs]} for sub, rs in by_sub.items()]})
    mixed = sorted(f for f, v in ids.family_tech.items() if len(v) != 1)
    mixed_detail = [{"family": fam, "techniques": ids.family_tech[fam], "subcategories": [{"subcategory": sc["id"], "label": sc["label"], "catalog_items": len(sc["items"])} for sc in next(m for m in L["taxonomy.json"]["modality"] if m["id"] == fam)["subcategories"]]} for fam in mixed]
    unreg_all = Counter()
    unreg_by_origin = {"catalog_item": Counter(), "reference": Counter(), "market_pricing": Counter()}
    for r in cat_recs:
        for u in r.get("unregistered", []):
            unreg_all[u] += 1
            unreg_by_origin["catalog_item"][u] += 1
    for rows in ref_rows.values():
        for r in rows:
            for u in r.get("unregistered", []):
                unreg_all[u] += 1
                unreg_by_origin["reference"][u] += 1
    for r in mk_rows:
        for u in r.get("unregistered", []):
            unreg_all[u] += 1
            unreg_by_origin["market_pricing"][u] += 1
    # ---- V3-3 실측: stopwords 전후
    unreg0 = Counter()
    for r in cat0 + [r for v in ref0.values() for r in v] + mk0:
        for u in r.get("unregistered", []):
            unreg0[u] += 1
    all_ref = [r for v in ref_rows.values() for r in v] + mk_rows
    all_ref0 = [r for v in ref0.values() for r in v] + mk0
    stop_hits = Counter()
    stop_locs = defaultdict(list)
    for r in cat_recs:
        for w in r.get("qualifier_text") or []:
            stop_hits[norm(w)] += 1
            stop_locs[norm(w)].append(f"taxonomy.json:modality[].subcategories[].items[].name@{r['family']}/{r['name']}")
    for r in all_ref:
        for w in r.get("qualifier_text") or []:
            stop_hits[norm(w)] += 1
            stop_locs[norm(w)].append(f"{r.get('ref_id')}:{r['label']}")
    for r in cat_recs + all_ref:
        for g in r.get("groups", []):
            for m in g["members"]:
                for k_, c_ in m["spans"]:
                    if k_ != "spec":
                        continue
                    cc = unicodedata.normalize("NFKC", str(c_)).replace(" ", "")
                    for w_, rx in (("회", COUNT_RE), ("차", SESSION_RE)):
                        if rx.match(cc):
                            stop_hits[norm(w_)] += 1
                            stop_locs[norm(w_)].append((f"taxonomy.json:modality[].subcategories[].items[].name@{r['family']}/{r['name']}" if "name" in r else f"{r.get('ref_id')}:{r['label']}") + f" (규격 {c_})")
    stop_table = []
    for w in resolve_rules["step2_decompose"]["stopwords"]["words"]:
        nw = norm(w["word"])
        stop_table.append({"word": w["word"], "origin": w["origin"], "hits": stop_hits.get(nw, 0), "locators": dedupe(stop_locs.get(nw, []))[:12], "unregistered_before": unreg0.get(w["word"], 0), "unregistered_after": unreg_all.get(w["word"], 0),
                           "in_dictionary": bool(lex.hits("product", w["word"]) or lex.hits("modality", w["word"]) or lex.hits("modality_subcategory", w["word"]) or lex.hits("procedure", w["word"]) or lex.hits("site", w["word"]))})
    ref_changed_by_stop = []
    r0map = {(r["label"], r.get("hint")): r for r in all_ref0}
    for r in all_ref:
        r0 = r0map.get((r["label"], r.get("hint")))
        if r0 and (r0["result"] != r["result"] or r0.get("unresolved_reason") != r.get("unresolved_reason") or sorted(r0.get("unregistered", [])) != sorted(r.get("unregistered", []))):
            ref_changed_by_stop.append({"label": r["label"], "hint": r.get("hint"), "slot": next((k for k, v in ref_rows.items() if r in v), "market-pricing.items[].name (122)"), "before": f"{r0['result']}:{r0.get('unresolved_reason') or ''}[{','.join(r0.get('unregistered', []))}]", "after": f"{r['result']}:{r.get('unresolved_reason') or ''}[{','.join(r.get('unregistered', []))}]", "qualifier_text": r.get("qualifier_text")})
    stop_summary = {"unregistered_distinct_before": len(unreg0), "unregistered_total_before": sum(unreg0.values()), "unregistered_distinct_after": len(unreg_all), "unregistered_total_after": sum(unreg_all.values()),
                    "words": stop_table, "words_with_locator": sum(1 for w in stop_table if w["locators"]), "words_total": len(stop_table), "references_changed": ref_changed_by_stop, "references_resolved_newly": sum(1 for x in ref_changed_by_stop if x["after"].startswith(("tuple", "combo_ref", "multi_tuple")) and not x["before"].startswith(("tuple", "combo_ref", "multi_tuple")))}
    # ---- V3-4 실측: `+`/`/` 라벨 전수
    combo_rows = []
    for slot, rows in list(ref_rows.items()) + [(MARKET_SLOT, mk_rows)]:
        for r in rows:
            lab = str(r["label"])
            if "+" in lab or "/" in lab:
                combo_rows.append({"slot": slot, "label": lab, "hint": r.get("hint"), "v1_name": V1_NAMES.get(lab), "symbols": sorted(set(ch for ch in lab if ch in "+/")), "result": r["result"], "reason": r.get("unresolved_reason"), "unregistered": r.get("unregistered", []),
                                   "member_mode": r.get("member_mode"), "alternatives": [a["text"] for a in r["alternatives"]] if r.get("alternatives") else None, "sites": r.get("sites"),
                                   "tuples": [f"{T[x]['what_kind']}:{T[x]['what_label']}×{T[x]['site'] or 'none'}×{T[x]['technique'] or 'none'}" for x in tids_of(r)], "qualifier_text": r.get("qualifier_text"), "detail": r.get("detail")})
    for r in cat_recs:
        if "+" in r["name"] or "/" in r["name"]:
            combo_rows.append({"slot": "① taxonomy 항목", "label": r["name"], "hint": r["family"], "v1_name": None, "symbols": sorted(set(ch for ch in r["name"] if ch in "+/")), "result": r["result"], "reason": r.get("self_reason"), "unregistered": r.get("unregistered", []), "member_mode": r.get("member_mode"), "alternatives": [a["text"] for a in r["alternatives"]] if r.get("alternatives") else None, "sites": r.get("sites"),
                               "tuples": [f"{T[x]['what_kind']}:{T[x]['what_label']}×{T[x]['site'] or 'none'}×{T[x]['technique'] or 'none'}" for x in tids_of(r)], "qualifier_text": r.get("qualifier_text"), "detail": r.get("self_detail")})
    plus_v2 = [c for c in combo_rows if c["v1_name"]]
    v24_cmp_rows = []
    if v24tup:
        r24 = {}
        for slot, rows in list(v24tup["procedure"]["references"].items()) + [(MARKET_SLOT, v24tup["procedure"]["market_pricing"])]:
            for r in rows:
                r24[(slot, str(r["label"]), r.get("hint"))] = r
        T24 = {t["id"]: t for t in v24tup["procedure"]["tuples"]}
        for slot, rows in list(ref_rows.items()) + [(MARKET_SLOT, mk_rows)]:
            for r in rows:
                key = (slot, str(r["label"]), r.get("hint"))
                old = r24.get(key)
                if old is None:
                    old_lab = V1_NAMES.get(str(r["label"]))
                    old = r24.get((slot, old_lab, r.get("hint"))) if old_lab else None
                o_desc = (f"{old['result']}:{old.get('unresolved_reason') or ''}" + ("[" + ",".join(_short(T24[x]) for x in ([old.get('procedure_id')] if old['result'] == 'tuple' else old.get('member_ids', [])) if x) + "]" if old["result"] in ("tuple", "combo_ref") else "")) if old else "(없음 · 2판 새 이름)"
                n_desc = f"{r['result']}:{r.get('unresolved_reason') or ''}" + (f"[{','.join(_short(T[x]) for x in tids_of(r))}]" if r["result"] in ("tuple", "combo_ref", "multi_tuple") else "")
                if o_desc != n_desc:
                    v24_cmp_rows.append({"slot": slot, "label": r["label"], "hint": r.get("hint"), "v24": o_desc, "v3": n_desc, "why": ("V3-4 부위 여럿" if r["result"] == "multi_tuple" else "V3-4 괄호 안 대안" if r.get("alternatives") else "V3-3 stopwords" if r.get("qualifier_text") else "V3-2 회사·제품 괄호" if r.get("company") or str(r.get("what_basis", "")).startswith("company_paren") else "2판 이름" if r["label"] in V1_NAMES else "")})
    # ---- V3-2 실측: 괄호 안 조각 하나짜리 전수
    PAREN = re.compile(r"\(([^()]*)\)")
    comp_cands = []

    def paren_probe(where, text, hint):
        for inner in PAREN.findall(text):
            if any(ch in inner for ch in "+/&,"):
                continue
            frag = inner.strip()
            if not frag:
                continue
            nf = norm(frag)
            comp_cands.append({"where": where, "text": text, "inner": frag, "manufacturer": ids.manufacturer_surface.get(nf), "product": ids.prod[nf]["label"] if nf in ids.prod else None,
                               "touches": "manufacturer" if nf in ids.manufacturer_surface else "product" if nf in ids.prod else "-"})
    for slot, rows in list(ref_rows.items()) + [(MARKET_SLOT, mk_rows)]:
        for r in rows:
            paren_probe(slot, str(r["label"]), r.get("hint"))
    for r in cat_recs:
        paren_probe("① taxonomy 항목", r["name"], r["family"])
    for c in L["problem-combos.json"]["combos"]:
        for p in c["packages"]:
            for x in p.get("products", []) or []:
                paren_probe("problem-combos.json:combos[].packages[].products[] (속성 문장)", x, None)
    for code, v in L["extracted.json"].items():
        if CODE_KEY_RE.match(code):
            for x in v.get("related_techniques", []) or []:
                paren_probe("extracted.json:{code}.related_techniques[] (설명 문장)", x, code)
    for m in L["taxonomy.json"]["modality"]:
        for x in ((m.get("extracted") or {}).get("related_techniques") or []):
            paren_probe("taxonomy.json:modality[].extracted.related_techniques[] (설명 문장)", x, m["id"])
    company_summary = {"candidates": len(comp_cands), "touch_manufacturer": sum(1 for c in comp_cands if c["touches"] == "manufacturer"), "touch_product": sum(1 for c in comp_cands if c["touches"] == "product"), "no_touch": sum(1 for c in comp_cands if c["touches"] == "-"),
                       "applied": PT.company_applied, "applied_n": len(PT.company_applied), "ambiguous_company_product": sum(1 for r in all_ref if r.get("unresolved_reason") == "company_product"),
                       "botox_allergan_sites": [c for c in comp_cands if "엘러간" in c["inner"] or "더모톡신" in c["inner"]], "unregistered_inner_top": [list(x) for x in Counter(c["inner"] for c in comp_cands if c["touches"] == "-").most_common(30)], "candidates_all": comp_cands}
    cat_tuples = [T[i] for i in cat_distinct]
    tup_rows = [r for r in cat_recs if r["result"] == "tuple"]
    fold2 = [f for f in folded if f["n_items"] >= 2]
    none_t = [t for t in T.values() if not t["all_dict_values"]]
    EE = edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids)
    s = OrderedDict([
        ("bronze_version", bronze_version),
        ("catalog_items", n_cat),
        ("catalog_result", dict(Counter(r["result"] for r in cat_recs))),
        ("catalog_distinct_tuples", len(cat_distinct)),
        ("catalog_fold_ratio", round(len(cat_distinct) / n_cat, 3) if n_cat else None),
        ("catalog_tuples_with_2plus_items", len(fold2)),
        ("catalog_items_in_folded_tuples", sum(f["n_items"] for f in fold2)),
        ("catalog_folded_all_dict_values", sum(1 for f in fold2 if f["all_dict_values"])),
        ("catalog_folded_with_partial_item", sum(1 for f in fold2 if any(x == "partial" for x in f["item_status"]))),
        ("catalog_folded_with_2plus_partial_items", sum(1 for f in fold2 if sum(1 for x in f["item_status"] if x == "partial") >= 2)),
        ("catalog_fallback_to_parent", sum(1 for r in cat_recs if str(r.get("what_basis", "")).startswith("parent_subcategory"))),
        ("catalog_by_what_kind", dict(Counter(r.get("what_kind") for r in tup_rows))),
        ("catalog_by_what_basis", dict(Counter(str(r.get("what_basis", "")).split(":")[0] if not str(r.get("what_basis", "")).startswith("self:") else str(r.get("what_basis", "")) for r in tup_rows))),
        ("catalog_status", dict(Counter(r.get("status") for r in tup_rows))),
        ("catalog_whole_match", sum(1 for r in cat_recs if r.get("whole_match"))),
        ("catalog_self_items", sum(1 for r in tup_rows if r.get("what_kind") == "catalog_item")),
        ("catalog_self_by_reason", dict(Counter(r.get("self_reason") for r in tup_rows if r.get("what_kind") == "catalog_item"))),
        ("catalog_self_with_site", sum(1 for r in tup_rows if r.get("what_kind") == "catalog_item" and r.get("site"))),
        ("catalog_site_none", sum(1 for r in tup_rows if not r.get("site"))),
        ("catalog_site_none_ratio", round(sum(1 for r in tup_rows if not r.get("site")) / max(1, len(tup_rows)), 3)),
        ("catalog_technique", dict(Counter(r.get("technique_origin") for r in tup_rows))),
        ("catalog_technique_none_ratio", round(sum(1 for r in tup_rows if r.get("technique_origin") == "none") / max(1, len(tup_rows)), 3)),
        ("catalog_tuple_site_none_ratio", round(sum(1 for t in cat_tuples if t["site_id"] == "none") / max(1, len(cat_tuples)), 3)),
        ("catalog_tuple_technique_none_ratio", round(sum(1 for t in cat_tuples if t["technique_id"] == "none") / max(1, len(cat_tuples)), 3)),
        ("catalog_multi_tuple", sum(1 for r in cat_recs if r["result"] == "multi_tuple")),
        ("catalog_with_qualifier_text", sum(1 for r in cat_recs if r.get("qualifier_text"))),
        ("catalog_with_layer_fragments", sum(1 for r in cat_recs if r.get("layer_fragments"))),
        ("catalog_company_applied", sum(1 for r in cat_recs if str(r.get("what_basis", "")).startswith("company_paren"))),
        ("reference_slots", OrderedDict((k, slot_summary(v)) for k, v in ref_rows.items())),
        ("reference_total", slot_summary([r for v in ref_rows.values() for r in v])),
        ("market_pricing", slot_summary(mk_rows)),
        ("tuples_total", len(T)),
        ("tuples_by_origin", {k: sum(1 for t in T.values() if k in t["origins"]) for k in ["catalog_item", "reference", "market_pricing"]}),
        ("tuples_by_what_kind", dict(Counter(t["what_kind"] for t in T.values()))),
        ("tuples_status", dict(Counter(t["status"] for t in T.values()))),
        ("tuples_site_none_ratio", round(sum(1 for t in T.values() if t["site_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_technique_none_ratio", round(sum(1 for t in T.values() if t["technique_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_any_none_ratio", round(sum(1 for t in T.values() if t["site_id"] == "none" or t["technique_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_technique_origin", dict(Counter(t["technique_origin"] for t in T.values()))),
        ("tuples_dict_what_site_none_ratio", round(sum(1 for t in T.values() if t["what_kind"] in SUMMARY_DICT_WHAT_KINDS and t["site_id"] == "none") / max(1, sum(1 for t in T.values() if t["what_kind"] in SUMMARY_DICT_WHAT_KINDS)), 3)),
        ("tuples_all_dict_values", sum(1 for t in T.values() if t["all_dict_values"])),
        ("tuples_anchored", len(none_t)),
        ("tuples_with_2plus_anchors", len(multi_anchor)),
        ("tuples_with_2plus_anchors_not_all_dict", sum(1 for m in multi_anchor if not m["all_dict_values"])),
        ("tuples_site_by_kind", dict(Counter(ids.site_kind.get(norm(t["site"]), "none") if t["site"] else "none" for t in T.values()))),
        ("tuples_layer_site", sum(1 for t in T.values() if t["site"] and ids.site_kind.get(norm(t["site"])) == "layer")),
        ("technique_inherited", sum(1 for t in T.values() if t["technique_origin"] == "inherited")),
        ("families_without_single_technique", mixed),
        ("families_mixed_detail", mixed_detail),
        ("inheritance_candidates", [dict({k: v for k, v in c.items() if k not in ("items", "scope")}, by_subcategory=[{kk: vv for kk, vv in b.items() if kk not in ("scope", "items")} for b in c["by_subcategory"]]) for c in inh]),
        ("code_references_node", sum(1 for rows in ref_rows.values() for r in rows if r["result"] == "node")),
        ("edge_ends_total", EE["total"]),
        ("edge_ends_total_n", EE["total_n"]),
        ("edge_ends_by_relation", EE["by_relation"]),
        ("edge_ends_slots", {"text": EE["text_slots"], "code": EE["code_slots"], "relations": EE["relations_covered"]}),
        ("edge_ends_member_mode", EE["member_mode"]),
        ("edge_ends_multi_tuple", EE["multi_tuple_ends"]),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", [list(x) for x in unreg_all.most_common(30)]),
        ("unregistered_top30_by_origin", {k: [list(x) for x in v.most_common(30)] for k, v in unreg_by_origin.items()}),
        ("stopwords", stop_summary),
        ("combo_labels", len(combo_rows)), ("combo_labels_all", combo_rows), ("combo_plus_v2", plus_v2),
        ("combo_by_result", dict(Counter(c["result"] + (":" + c["reason"] if c["reason"] else "") for c in combo_rows))),
        ("combo_member_mode", dict(Counter(c["member_mode"] for c in combo_rows if c["member_mode"]))),
        ("multi_tuples", PT.multi_tuples), ("alternatives", PT.alternatives),
        ("v24_reference_changes", v24_cmp_rows),
        ("company_paren", company_summary),
    ])
    # ---- v3.1(V3.1-5) 회·차 자리 실측 · (V3.1-6) stopwords 겹침 — 참조 구현 erd-v3.1-tuples.py run_all 과 같은 값
    sess = []
    for slot, rows in list(ref_rows.items()) + [(MARKET_SLOT, mk_rows)]:
        for r in rows:
            for t in r.get("session_tokens") or []:
                sess.append({"slot": slot, "relation": r.get("session_relation"), "label": r["label"], "hint": r.get("hint"), "token": t["token"], "kind": t["kind"], "value": t["value"], "target": r.get("session_target"), "result": r["result"],
                             "session_index": r.get("session_index"), "session_count": r.get("session_count"), "qualifier_text": r.get("qualifier_text")})
    for r in cat_recs:
        for t in session_tokens(r.get("groups") or []):
            sess.append({"slot": "① taxonomy 항목", "relation": None, "label": r["name"], "hint": r["family"], "token": t["token"], "kind": t["kind"], "value": t["value"], "target": None, "result": r["result"], "session_index": None, "session_count": None, "qualifier_text": r.get("qualifier_text")})
    s["session_tokens"] = sess
    s["session_summary"] = {"total": len(sess), "by_kind": dict(Counter(x["kind"] for x in sess)), "by_relation": dict(Counter(str(x["relation"]) for x in sess)), "by_target": dict(Counter(str(x["target"]) for x in sess)),
                            "r12_session_index": sum(1 for x in sess if x["relation"] == "R12" and x["kind"] == "차"), "r12_session_count": sum(1 for x in sess if x["relation"] == "R12" and x["kind"] == "회"), "to_qualifier_text": sum(1 for x in sess if x["target"] == "qualifier_text")}
    if dic_json is not None:
        ov = stopword_overlap(dic_json, resolve_rules)
        stop_summary["overlap"] = ov
        stop_summary["overlap_words"] = [o["word"] for o in ov]
        stop_summary["dictionaries_checked"] = len(value_dictionaries(dic_json))
    s["_inheritance_candidates_full"] = inh
    s["_unregistered_all"] = unreg_all
    return s


def _short(t):
    return f"{t['what_kind']}:{t['what_label']}×{t['site'] or 'none'}"


# ===========================================================================
# §1.5 부작용 튜플 (v3: 수식 칸 qualifier · 접두 수식 가름 · layer 부위)
# ===========================================================================
ADV_PAREN = re.compile(r"\(([^()]*)\)")
ADV_MEMBER_SPLIT = re.compile(r"[·/,+]|\s및\s|\s또는\s|--|—|:|;")
ADV_STRIP = "*'\"“”‘’.…`~!?"


def adverse_unit_id(event_id, site_id, course_id, qualifier_id="none"):
    """v3 부작용 단위 식별자 — 네 칸(event · site · course · qualifier · 없음은 'none')."""
    return mkid("ADV", f"{event_id}|{site_id}|{course_id}|{qualifier_id or 'none'}")


class AdverseTuples:
    def __init__(self, ids):
        self.ids = ids
        self.tuples = OrderedDict()
        self.units = {}
        self.lookup = {}
        # 사전 순서 relative_site → site → course → adverse_qualifier → event (setdefault = 앞 순서 우선)
        for surf, canon in ids.rsite_surface.items():
            self.lookup.setdefault(surf, ("relative", canon))
        for surf, canon in ids.site_surface.items():
            self.lookup.setdefault(surf, ("site", canon))
        for surf, canon in ids.course_surface.items():
            self.lookup.setdefault(surf, ("course", canon))
        for surf, canon in ids.qualifier_surface.items():
            self.lookup.setdefault(surf, ("qualifier", canon))
        for surf, canon in ids.event_surface.items():
            self.lookup.setdefault(surf, ("event", canon))
        self.maxlen = 6
        self.prefix_splits = []

    def split(self, text):
        parens = ADV_PAREN.findall(text)
        outer = ADV_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part:
                    continue
                toks = [t.strip(ADV_STRIP) for t in part.split()]
                toks = [t for t in toks if t]
                spans, untouched = [], []
                i = 0
                while i < len(toks):
                    found = None
                    for j in range(min(len(toks), i + self.maxlen), i, -1):
                        key = norm("".join(toks[i:j]))
                        if key in self.lookup:
                            found = (self.lookup[key], " ".join(toks[i:j]), j)
                            break
                    if found:
                        spans.append({"kind": found[0][0], "canonical": found[0][1], "text": found[1]})
                        i = found[2]
                        continue
                    # V3-1: 접두 수식 + 사건 (완전 일치만 · 「공기색전」)
                    tok = toks[i]
                    nt = norm(tok)
                    hit = None
                    for k in range(1, len(nt)):
                        if nt[:k] in self.ids.qualifier_surface and nt[k:] in self.ids.event_surface:
                            hit = (nt[:k], nt[k:])
                            break
                    if hit:
                        spans.append({"kind": "qualifier", "canonical": self.ids.qualifier_surface[hit[0]], "text": tok, "basis": "prefix_split"})
                        spans.append({"kind": "event", "canonical": self.ids.event_surface[hit[1]], "text": tok})
                        self.prefix_splits.append((tok, self.ids.qualifier_surface[hit[0]], self.ids.event_surface[hit[1]]))
                    else:
                        untouched.append(tok)
                    i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched})
            groups.append({"where": where, "members": members})
        return groups

    def site_key(self, site):
        if site is None:
            return "none"
        if site[0] == "relative":
            return self.ids.rsite[norm(site[1])]["id"]
        return self.ids.site[norm(site[1])]["id"]

    def qual_key(self, q):
        return self.ids.qualifier[norm(q)]["id"] if q else "none"

    def assemble(self, groups):
        """원칙 C: 사건이 놓인 멤버 안의 부위·경과·수식만 · 부위 나열 멤버(바로 앞)는 합친다. 원칙 B: 후보마다 튜플. 붙지 않은 조각은 extra."""
        out, merges = [], []
        extra_sites, extra_courses, extra_quals = [], [], []
        for g in groups:
            ms = g["members"]
            pending, pending_text = [], []
            for idx, m in enumerate(ms):
                spans = m["spans"]
                events = dedupe(s["canonical"] for s in spans if s["kind"] == "event")
                sites = dedupe((s["kind"], s["canonical"]) for s in spans if s["kind"] in ("relative", "site"))
                courses = dedupe(s["canonical"] for s in spans if s["kind"] == "course")
                quals = dedupe(s["canonical"] for s in spans if s["kind"] == "qualifier")
                qbasis = {s["canonical"]: s.get("basis", "member") for s in spans if s["kind"] == "qualifier"}
                if not events:
                    nxt = ms[idx + 1] if idx + 1 < len(ms) else None
                    if sites and not courses and not quals and not m["untouched"] and nxt is not None and any(s["kind"] == "event" for s in nxt["spans"]):
                        pending += sites
                        pending_text.append(m["text"])
                        continue
                    extra_sites += [s[1] for s in sites] + [s[1] for s in pending]
                    extra_courses += courses
                    extra_quals += quals
                    pending, pending_text = [], []
                    continue
                site_list = bool(pending)
                all_sites = dedupe(pending + sites)
                if site_list:
                    merges.append({"where": g["where"], "site_members": list(pending_text), "event_member": m["text"], "sites": [s[1] for s in all_sites], "events": events})
                # 부위 나열 멤버(바로 앞)에서 온 부위는 site_basis=site_list(ERD §2.14 · enum adverse_effect.site_basis) — 비우기 전에 잡아 둔다
                listed, listed_text = list(pending), list(pending_text)
                pending, pending_text = [], []
                site_opts = all_sites or [None]
                course_opts = courses or ["미상"]
                qual_opts = quals or [None]
                for ev in events:
                    for st in site_opts:
                        for co in course_opts:
                            for q in qual_opts:
                                out.append({"event": ev, "site": st, "course": co, "qualifier": q, "member": (" / ".join(listed_text) + " / " if site_list and listed_text else "") + m["text"],
                                            "site_basis": ("site_list" if site_list and st in listed else "member") if st else None, "course_basis": "member" if courses else None, "qualifier_basis": qbasis.get(q) if q else None,
                                            "n_site_candidates": len(all_sites), "n_course_candidates": len(courses), "n_qualifier_candidates": len(quals)})
            extra_sites += [s[1] for s in pending]
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        seen, uniq = set(), []
        for t in out:
            k = (t["event"], t["site"], t["course"], t["qualifier"])
            if k not in seen:
                seen.add(k)
                uniq.append(t)
        return uniq, untouched, {"extra_sites": dedupe(extra_sites), "extra_courses": dedupe(extra_courses), "extra_qualifiers": dedupe(extra_quals), "site_list_merges": merges}

    def register(self, t, src):
        ev = self.ids.event[norm(t["event"])]
        if t["site"] is None:
            site_id, site_label, site_kind = "none", None, "none"
        elif t["site"][0] == "relative":
            site_id, site_label, site_kind = self.ids.rsite[norm(t["site"][1])]["id"], t["site"][1], "relative"
        else:
            site_id, site_label, site_kind = self.ids.site[norm(t["site"][1])]["id"], t["site"][1], "site"
        cid = self.ids.course[norm(t["course"])]["id"]
        qid = self.qual_key(t["qualifier"])
        tid = adverse_unit_id(ev["id"], site_id, cid, qid)
        rec = self.tuples.get(tid)
        if rec is None:
            rec = {"id": tid, "event_kind": "dict", "event": ev["label"], "event_id": ev["id"], "event_category": ev["category"], "site_kind": site_kind, "site": site_label, "site_id": site_id,
                   "site_dict_kind": (self.ids.site_kind.get(norm(t["site"][1])) if t["site"] and t["site"][0] == "site" else ("relative" if t["site"] else None)),
                   "course": t["course"], "course_id": cid, "qualifier": t["qualifier"], "qualifier_id": qid, "qualifier_basis": t.get("qualifier_basis"),
                   "status": "complete", "unregistered_fragments": [], "origins": [], "sources": [], "anchor": None, "all_dict_values": True, "candidate_name": [], "event_fragments": [ev["label"]],
                   "extra_sites": [], "extra_courses": [], "extra_qualifiers": [], "site_basis": t.get("site_basis"), "course_basis": t.get("course_basis")}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        self.units[(rec["event_id"], rec["site_id"], rec["course_id"], rec["qualifier_id"])] = tid
        return tid

    def register_raw(self, text, tuples, untouched, extras, src, anchor):
        all_events = dedupe(t["event"] for t in tuples)
        sites = dedupe([t["site"][1] for t in tuples if t["site"]] + list(extras["extra_sites"]))
        courses = dedupe([t["course"] for t in tuples if t["course"] != "미상"] + list(extras["extra_courses"]))
        quals = dedupe([t["qualifier"] for t in tuples if t["qualifier"]] + list(extras["extra_qualifiers"]))
        cid = self.ids.course[norm("미상")]["id"]
        event_id = f"RAW:{anchor}"
        tid = mkid("ADV", f"{event_id}|none|{cid}|none|{anchor}")
        rec = self.tuples.get(tid)
        unatt = bool(extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"])
        if rec is None:
            cat = self.ids.event[norm(all_events[0])]["category"] if all_events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, "event_category": cat, "site_kind": "none", "site": None, "site_id": "none", "site_dict_kind": None, "course": "미상", "course_id": cid,
                   "qualifier": None, "qualifier_id": "none", "qualifier_basis": None,
                   "status": "partial" if untouched else "unresolved", "unregistered_fragments": list(untouched), "origins": [], "sources": [], "anchor": anchor, "all_dict_values": False, "candidate_name": list(untouched),
                   "event_fragments": all_events, "extra_sites": sites, "extra_courses": courses, "extra_qualifiers": quals, "site_basis": None, "course_basis": None,
                   "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "raw_reason": ("unregistered" if untouched else "") + ("+" if untouched and unatt else "") + ("unattached_fragments" if unatt else "")}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        return tid

    def candidates_of(self, tuples):
        out = []
        for t in tuples:
            ev = self.ids.event[norm(t["event"])]
            sid = self.site_key(t["site"])
            cid = self.ids.course[norm(t["course"])]["id"]
            qid = self.qual_key(t["qualifier"])
            key = (ev["id"], sid, cid, qid)
            out.append({"event": t["event"], "event_id": ev["id"], "site": t["site"][1] if t["site"] else None, "site_kind": t["site"][0] if t["site"] else "none", "site_id": sid, "course": t["course"], "course_id": cid,
                        "qualifier": t["qualifier"], "qualifier_id": qid, "qualifier_basis": t.get("qualifier_basis"),
                        "would_be_id": adverse_unit_id(ev["id"], sid, cid, qid), "exists": key in self.units, "unit_id": self.units.get(key), "site_basis": t["site_basis"], "course_basis": t["course_basis"], "member": t["member"]})
        return out

    def _row(self, text, src, groups, tuples, untouched, extras):
        spans = [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]
        return {"text": text, "spans": spans, "locator": src.get("locator"), "unregistered": untouched, "extra_sites": extras["extra_sites"], "extra_courses": extras["extra_courses"], "extra_qualifiers": extras["extra_qualifiers"], "site_list_merges": extras["site_list_merges"],
                "b_splits": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["n_site_candidates"], t["n_course_candidates"], t["qualifier"], t["n_qualifier_candidates"]) for t in tuples if t["n_site_candidates"] >= 2 or t["n_course_candidates"] >= 2 or t["n_qualifier_candidates"] >= 2],
                "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "event_fragments": dedupe(t["event"] for t in tuples),
                "qualifiers": dedupe(t["qualifier"] for t in tuples if t["qualifier"]), "assembled": tuples}

    def run_name(self, text, src):
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        base = self._row(text, src, groups, tuples, untouched, extras)
        unattached = bool(extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"])
        if untouched or unattached:
            tid = self.register_raw(text, tuples, untouched, extras, src, src["locator"])
            r = self.tuples[tid]
            base.update({"event_kind": "raw_name", "tuples": [(r["event"], None, "미상", None, None, None)], "tuple_ids": [tid], "candidate_name": untouched, "anchor": src["locator"], "raw_reason": r["raw_reason"]})
            return base
        ids = [self.register(t, src) for t in tuples]
        base.update({"event_kind": "dict" if ids else None, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"], t["qualifier"]) for t in tuples], "tuple_ids": ids, "candidate_name": [], "anchor": None})
        return base

    def run_expression(self, text, src):
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        cands = self.candidates_of(tuples)
        reasons = []
        if not cands:
            reasons.append("no_event")
        if untouched:
            reasons.append("unregistered")
        if extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"]:
            reasons.append("unattached_fragments")
        if cands and any(not c["exists"] for c in cands):
            reasons.append("no_unit")
        exact = not reasons
        ids = []
        if exact:
            for c in cands:
                tid = c["unit_id"]
                rec = self.tuples[tid]
                rec["sources"].append(src)
                if src["origin"] not in rec["origins"]:
                    rec["origins"].append(src["origin"])
                ids.append(tid)
        base = self._row(text, src, groups, tuples, untouched, extras)
        base.update({"candidates": cands, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"], t["qualifier"]) for t in tuples],
                     "tuple_ids": dedupe(ids), "match_status": "exact" if exact else "unlinked", "unlinked_reasons": reasons})
        return base


def adverse_phrases(L):
    """표현 레코드 전부 (kind, text, src) — src 에 ERD locator(`<파일>:<경로>@<계열>/<순번>`) + 원장 rec(실제 위치)."""
    raw = []
    for ci, cat in enumerate(L["consent-checklist.json"]["categories"]):
        for i, x in enumerate(cat.get("emergency_signs", []) or []):
            raw.append(("emergency_sign", x, {"origin": "consent", "file": "consent-checklist.json", "path": "categories[].emergency_signs[]", "modality": cat["id"], "context": {"frequency_class": "emergency"}, "rec": (ci, i)}))
    for ti, tl in enumerate(L["post-procedure-timeline.json"]["timelines"]):
        code = tl["category"].split("-")[0]
        for pi, ph in enumerate(tl["phases"]):
            for k in ["normal", "abnormal", "caution", "emergency"]:
                for i, x in enumerate(ph.get(k, []) or []):
                    raw.append(("symptom_phrase", x, {"origin": f"timeline.{k}", "file": "post-procedure-timeline.json", "path": f"timelines[].phases[].{k}[]", "modality": code,
                                                      "context": {"reaction_level": k, "period": ph["period"], "phase_label": ph["label"], "timeline": tl["name"]}, "rec": (ti, pi, i)}))
    ex = L["extracted.json"]
    for code, v in ex.items():
        if not CODE_KEY_RE.match(code):
            continue
        s = v.get("safety") or {}
        for k in ["common", "uncommon", "serious", "emergency"]:
            for i, x in enumerate(s.get(k) or []):
                raw.append(("safety_phrase", x, {"origin": "extracted.safety", "file": "extracted.json", "path": f"{{code}}.safety.{k}[]", "modality": code, "context": {"frequency_class": k}, "rec": (code, i)}))
    tx = L["taxonomy.json"]
    syn = {"common_adverse_effects": "common", "serious_adverse_effects": "serious", "common_side_effects": "common"}
    for mi, m in enumerate(tx["modality"]):
        s = (m.get("extracted") or {}).get("safety") or {}
        for k in ["common", "uncommon", "serious"]:
            for i, x in enumerate(s.get(k) or []):
                raw.append(("safety_phrase", x, {"origin": "taxonomy.modality.safety", "file": "taxonomy.json", "path": f"modality[].extracted.safety.{k}[]", "modality": m["id"], "context": {"frequency_class": k}, "rec": (mi, i)}))
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                s = (it.get("extracted") or {}).get("safety") or {}
                for k in ["common", "serious", "common_adverse_effects", "serious_adverse_effects", "long_term"]:
                    for i, x in enumerate(s.get(k) or []):
                        raw.append(("safety_phrase", x, {"origin": "taxonomy.item.safety", "file": "taxonomy.json", "path": f"modality[].subcategories[].items[].extracted.safety.{k}[]", "modality": m["id"],
                                                         "context": {"frequency_class": syn.get(k, k), "item_name": it["name"]}, "rec": (mi, si, ii, i), "item": (m["id"], it["name"])}))
        for pi, pr in enumerate(m["products"]):
            s = (pr.get("extracted") or {}).get("safety") or {}
            for k in ["common", "serious", "common_side_effects"]:
                for i, x in enumerate(s.get(k) or []):
                    raw.append(("safety_phrase", x, {"origin": "taxonomy.product.safety", "file": "taxonomy.json", "path": f"modality[].products[].extracted.safety.{k}[]", "modality": m["id"],
                                                     "context": {"frequency_class": syn.get(k, k), "product_name": pr["name"]}, "rec": (mi, pi, i), "product": (m["id"], pr["name"])}))
    lit = L["literature-evidence.json"]
    for code, cat in lit["categories"].items():
        for i, ae in enumerate(cat.get("adverse_effects", []) or []):
            raw.append(("evidence_statement", ae["statement"], {"origin": "literature", "file": "literature-evidence.json", "path": "categories.{code}.adverse_effects[].statement", "modality": code, "record": i,
                                                                 "patient_ko": ae.get("patient_ko"), "context": {}, "rec": (code, i)}))
    seq = Counter()
    out = []
    for kind, text, src in raw:
        key = (src["file"], src["path"], src.get("modality"))
        r = src.get("record")
        if r is None:
            r = seq[key]
            seq[key] += 1
        out.append((kind, text, dict(src, locator=locator(src["file"], src["path"], f"{src.get('modality')}/{r}"))))
    return out



PK_KEYS = ("text", "tuples", "b_splits", "site_list_merges", "candidates", "tuple_ids", "unregistered", "extra_sites", "extra_courses", "extra_qualifiers", "match_status", "unlinked_reasons", "qualifiers", "locator", "spans")


def run_adverse(ids, L, prev_tuples=None):
    AT = AdverseTuples(ids)
    comp_rows = []
    for ci, cat in enumerate(L["complications.json"]["categories"]):
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            r = AT.run_name(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc, "rec": (ci, i)})
            r.update({"modality": cat["id"], "severity": c.get("severity"), "record": i, "rec": (ci, i)})
            comp_rows.append(r)
    comp_tuple_ids = dedupe(x for r in comp_rows for x in r["tuple_ids"])
    n_units_before_expr = len(AT.tuples)
    expr_rows = []
    for kind, text, src in adverse_phrases(L):
        r = AT.run_expression(text, dict(src, kind=kind))
        r.update({"kind": kind, "modality": src.get("modality"), "origin": src["origin"], "path": src["path"], "file": src["file"], "context": src.get("context"), "rec": src["rec"], "item": src.get("item"), "product": src.get("product")})
        if kind == "evidence_statement" and src.get("patient_ko"):
            r2 = AT.run_expression(src["patient_ko"], dict(src, kind="patient_text", lang="ko", path="categories.{code}.adverse_effects[].patient_ko", origin="literature.patient_ko", locator=src["locator"].replace(".statement@", ".patient_ko@")))
            r["patient_ko"] = {k_: r2[k_] for k_ in PK_KEYS}
            union = r["candidates"] + [c for c in r2["candidates"] if c["would_be_id"] not in {x["would_be_id"] for x in r["candidates"]}]
            reasons = dedupe(r["unlinked_reasons"] + r2["unlinked_reasons"])
            exact = r["match_status"] == "exact" and r2["match_status"] == "exact"
            if not exact and (r["tuple_ids"] or r2["tuple_ids"]):
                for tid in r["tuple_ids"] + r2["tuple_ids"]:
                    rec = AT.tuples[tid]
                    rec["sources"] = [s_ for s_ in rec["sources"] if s_.get("locator") not in (r["locator"], r2["locator"])]
                    for o in ("literature", "literature.patient_ko"):
                        if o in rec["origins"] and not any(s_["origin"] == o for s_ in rec["sources"]):
                            rec["origins"].remove(o)
                r["tuple_ids"], r2["tuple_ids"], r["patient_ko"]["tuple_ids"] = [], [], []
            r["candidates_union"] = union
            r["unlinked_reasons"] = reasons
            r["match_status"] = "exact" if exact else "unlinked"
            r["tuple_ids_union"] = dedupe(r["tuple_ids"] + r2["tuple_ids"]) if exact else []
            r["basis"] = "both" if exact else "none"
        else:
            r["tuple_ids_union"] = r["tuple_ids"]
            r["candidates_union"] = r["candidates"]
        r["linked"] = r["match_status"] == "exact"
        expr_rows.append(r)
    assert len(AT.tuples) == n_units_before_expr, "표현이 튜플을 만들었다(원칙 D 위반)"
    summary = adverse_summary(AT, ids, comp_rows, comp_tuple_ids, expr_rows, prev_tuples)
    return {"AT": AT, "comp_rows": comp_rows, "comp_tuple_ids": comp_tuple_ids, "expr_rows": expr_rows, "summary": summary}


def adverse_summary(AT, ids, comp_rows, comp_tuple_ids, expr_rows, v24tup=None):
    """참조 구현 erd-v3-tuples.py run_adverse 의 summary 와 같은 키·같은 값."""
    A = AT.tuples
    adv_folded = []
    for tid in comp_tuple_ids:
        rows_ = [r for r in comp_rows if tid in r["tuple_ids"]]
        names = [f"{r['text']} [{r['modality']}]" for r in rows_]
        own_unreg = dedupe(u for r in rows_ for u in r["unregistered"])
        t = A[tid]
        adv_folded.append({"adverse_id": tid, "event_kind": t["event_kind"], "event": t["event"], "category": t["event_category"], "site": t["site"], "course": t["course"], "qualifier": t["qualifier"], "status": t["status"] if t["event_kind"] == "raw_name" else ("partial" if own_unreg else "complete"),
                           "all_dict_values": t["all_dict_values"], "n_names": len(names), "names": names, "unregistered": own_unreg})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["event_kind"], x["category"] or "", x["event"], x["qualifier"] or ""))
    adv_unreg = Counter()
    adv_unreg_by_origin = defaultdict(Counter)
    for r in comp_rows:
        for u in r["unregistered"]:
            adv_unreg[u] += 1
            adv_unreg_by_origin["complications"][u] += 1
    for r in expr_rows:
        for u in r["unregistered"]:
            adv_unreg[u] += 1
            adv_unreg_by_origin[r["kind"]][u] += 1
        if r.get("patient_ko"):
            for u in r["patient_ko"]["unregistered"]:
                adv_unreg[u] += 1
                adv_unreg_by_origin["patient_text(ko)"][u] += 1

    def all_cands(r):
        return r.get("candidates_union") or r["candidates"]

    def kind_summary(kind):
        rows = [r for r in expr_rows if r["kind"] == kind]
        return {"n": len(rows), "linked": sum(1 for r in rows if r["linked"]), "unlinked": sum(1 for r in rows if not r["linked"]),
                "match_status": dict(Counter(r["match_status"] for r in rows)),
                "unlinked_reasons": dict(Counter(x for r in rows if not r["linked"] for x in r["unlinked_reasons"])),
                "distinct_tuples": len({x for r in rows for x in r["tuple_ids_union"]}),
                "new_tuples_not_from_complications": len({x for r in rows for x in r["tuple_ids_union"] if "complications" not in A[x]["origins"]}),
                "candidate_units_not_existing": len({c["would_be_id"] for r in rows for c in all_cands(r) if not c["exists"]})}

    raw = [t for t in A.values() if t["event_kind"] == "raw_name"]
    dict_t = [t for t in A.values() if t["event_kind"] == "dict"]
    af2 = [f for f in adv_folded if f["n_names"] >= 2]
    lop = [r for r in comp_rows if "LOP" in r["text"]]
    course_split = [{"name": f"{r['text']} [{r['modality']}]", "event_kind": r["event_kind"], "tuples": [list(t[:3]) for t in r["dict_tuples"]]} for r in comp_rows
                    if r["dict_tuples"] and any(c in r["text"] for c in ("일시적", "지연성", "가역적", "Transient", "Delayed", "영구", "Late-Onset"))]
    all_rows = comp_rows + expr_rows + [dict(r["patient_ko"], kind="patient_text", text=r["patient_ko"]["text"]) for r in expr_rows if r.get("patient_ko")]
    site_outside_member = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[1] and t[4] not in ("member", "site_list")]
    site_list_merges = [{"text": r["text"], "kind": r.get("kind", "complications"), "merges": r["site_list_merges"]} for r in all_rows if r.get("site_list_merges")]
    multi_cand = [{"text": r["text"], "kind": r.get("kind", "complications"), "tuples": [t[:3] + (t[5],) for t in r["b_splits"]], "site_candidates": max(t[3] for t in r["b_splits"]), "course_candidates": max(t[4] for t in r["b_splits"]), "qualifier_candidates": max(t[6] for t in r["b_splits"])} for r in all_rows if r.get("b_splits")]
    headache_injection = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[0] == "두통" and t[1] == "주사 부위"]
    headache_injection_tuples = [t["id"] for t in A.values() if t["event"] == "두통" and t["site"] == "주사 부위"]
    unattached = [{"text": r["text"], "kind": r.get("kind", "complications"), "extra_sites": r["extra_sites"], "extra_courses": r["extra_courses"], "extra_qualifiers": r["extra_qualifiers"]} for r in all_rows if r["extra_sites"] or r["extra_courses"] or r["extra_qualifiers"]]
    raw_cells = {"n": len(raw), "site_none": sum(1 for t in raw if t["site_id"] == "none"), "course_unknown": sum(1 for t in raw if t["course"] == "미상"), "qualifier_none": sum(1 for t in raw if t["qualifier_id"] == "none"), "with_dict_tuples": sum(1 for t in raw if t.get("dict_tuples")),
                 "by_reason": dict(Counter(t["raw_reason"] for t in raw)), "with_extra_sites": sum(1 for t in raw if t["extra_sites"]), "with_extra_courses": sum(1 for t in raw if t["extra_courses"]), "with_extra_qualifiers": sum(1 for t in raw if t["extra_qualifiers"])}
    new_from_expr = [t["id"] for t in A.values() if "complications" not in t["origins"]]
    partial_linked = [r["text"][:40] for r in expr_rows if r["tuple_ids_union"] and (r["unregistered"] or (r.get("patient_ko") or {}).get("unregistered") or r["extra_sites"] or r["extra_courses"] or r["extra_qualifiers"] or (r.get("patient_ko") or {}).get("extra_sites") or (r.get("patient_ko") or {}).get("extra_courses") or (r.get("patient_ko") or {}).get("extra_qualifiers"))]
    cand_units = Counter()
    cand_units_detail = {}
    for r in expr_rows:
        for c in all_cands(r):
            if not c["exists"]:
                cand_units[c["would_be_id"]] += 1
                cand_units_detail.setdefault(c["would_be_id"], {"event": c["event"], "site": c["site"], "site_kind": c["site_kind"], "course": c["course"], "qualifier": c["qualifier"], "expressions": 0, "kinds": Counter()})
                cand_units_detail[c["would_be_id"]]["expressions"] += 1
                cand_units_detail[c["would_be_id"]]["kinds"][r["kind"]] += 1
    cand_units_list = [dict(v, id=k, kinds=dict(v["kinds"])) for k, v in sorted(cand_units_detail.items(), key=lambda x: -x[1]["expressions"])]
    q_names = [{"text": r["text"], "modality": r["modality"], "event_kind": r["event_kind"], "dict_tuples": r["dict_tuples"], "qualifiers": r["qualifiers"], "extra_qualifiers": r["extra_qualifiers"], "spans": [s for s in r["spans"] if s[0] == "qualifier"]} for r in comp_rows if r["qualifiers"] or r["extra_qualifiers"] or any(s[0] == "qualifier" for s in r["spans"])]
    q_exprs = [{"text": r["text"], "kind": r.get("kind"), "origin": r.get("origin"), "locator": r.get("locator"), "match_status": r.get("match_status"), "candidates": [(c["event"], c["site"], c["course"], c["qualifier"], c["exists"]) for c in r.get("candidates", []) if c["qualifier"]], "extra_qualifiers": r["extra_qualifiers"], "qualifier_spans": [s for s in r["spans"] if s[0] == "qualifier"]}
               for r in expr_rows + [dict(r["patient_ko"], kind="patient_text", origin="literature.patient_ko", locator=(r.get("locator") or "").replace(".statement@", ".patient_ko@"), spans=[]) for r in expr_rows if r.get("patient_ko")] if r.get("qualifiers") or r.get("extra_qualifiers") or any(s[0] == "qualifier" for s in r.get("spans", []))]
    q_tuples = [t for t in A.values() if t["qualifier_id"] != "none"]
    layer_tuples = [t for t in A.values() if t.get("site_dict_kind") == "layer"]
    layer_cands = [(r["text"][:40], c["event"], c["site"], c["exists"]) for r in expr_rows for c in all_cands(r) if c["site"] and ids.site_kind.get(norm(c["site"])) == "layer"]
    layer_extra = [(r["text"][:40], [s for s in r["extra_sites"] if ids.site_kind.get(norm(s)) == "layer"]) for r in all_rows if any(ids.site_kind.get(norm(s)) == "layer" for s in r["extra_sites"])]
    cmp = {}
    if v24tup:
        v24f = v24tup["adverse"]["folded"]
        g24 = sorted(sorted(f["names"]) for f in v24f if f["event_kind"] == "dict")
        g3 = sorted(sorted(f["names"]) for f in adv_folded if f["event_kind"] == "dict")
        raw24 = sorted(f["names"][0] for f in v24f if f["event_kind"] == "raw_name")
        raw3 = sorted(f["names"][0] for f in adv_folded if f["event_kind"] == "raw_name")
        ex24 = {r["locator"]: r["match_status"] for r in v24tup["adverse"]["expressions"]}
        ex3 = {r["locator"]: r["match_status"] for r in expr_rows}
        diff_ex = sorted([k, ex24.get(k), ex3.get(k)] for k in set(ex24) | set(ex3) if ex24.get(k) != ex3.get(k))
        T24 = {t["id"]: t for t in v24tup["adverse"]["tuples"]}
        tid24 = {r["locator"]: sorted({(T24[x]["event"], T24[x]["site"] or "", T24[x]["course"]) for x in r["tuple_ids_union"]}) for r in v24tup["adverse"]["expressions"]}
        tid3 = {r["locator"]: sorted({(A[x]["event"], A[x]["site"] or "", A[x]["course"]) for x in r["tuple_ids_union"]}) for r in expr_rows}
        diff_units = [k for k in tid24 if tid24[k] != tid3.get(k)]
        cmp = {"dict_fold_groups_v24": len(g24), "dict_fold_groups_v3": len(g3), "dict_fold_groups_same": g24 == g3, "fold_group_diff": [g for g in g24 if g not in g3] + [g for g in g3 if g not in g24],
               "raw_names_v24": len(raw24), "raw_names_v3": len(raw3), "raw_names_same": raw24 == raw3,
               "exact_v24": v24tup["adverse"]["summary"]["expressions_total"]["linked"], "exact_v3": sum(1 for r in expr_rows if r["linked"]), "match_status_diff": diff_ex, "linked_units_diff": diff_units,
               "tuples_v24": v24tup["adverse"]["summary"]["tuples_total"], "tuples_v3": len(A), "tuple_ids_changed": "식별자에 qualifier_id 가 들어가 ADV- 값은 전부 바뀐다(네 칸 키) — 접힘 그룹·exact 연결은 위 대조"}
    s = OrderedDict([
        ("principles", PRINCIPLES),
        ("complications_names", len(comp_rows)),
        ("complications_names_with_tuple", sum(1 for r in comp_rows if r["tuple_ids"])),
        ("complications_names_without_tuple", [f"{r['text']} [{r['modality']}]" for r in comp_rows if not r["tuple_ids"]]),
        ("complications_names_multi_tuple", sum(1 for r in comp_rows if len(r["tuple_ids"]) >= 2)),
        ("complications_names_raw", sum(1 for r in comp_rows if r["event_kind"] == "raw_name")),
        ("complications_names_raw_by_reason", dict(Counter(r["raw_reason"] for r in comp_rows if r["event_kind"] == "raw_name"))),
        ("complications_names_dict", sum(1 for r in comp_rows if r["event_kind"] == "dict")),
        ("complications_distinct_tuples", len(comp_tuple_ids)),
        ("complications_distinct_tuples_dict", sum(1 for t in comp_tuple_ids if A[t]["event_kind"] == "dict")),
        ("complications_distinct_tuples_raw", sum(1 for t in comp_tuple_ids if A[t]["event_kind"] == "raw_name")),
        ("complications_fold_ratio", round(len(comp_tuple_ids) / len(comp_rows), 3)),
        ("complications_tuples_with_2plus_names", len(af2)),
        ("complications_folded_all_dict_values", sum(1 for f in af2 if f["all_dict_values"] and not f["unregistered"])),
        ("complications_folded_with_unregistered", sum(1 for f in af2 if f["unregistered"])),
        ("complications_by_course", dict(Counter(A[t]["course"] for t in comp_tuple_ids))),
        ("complications_by_course_dict_only", dict(Counter(A[t]["course"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"))),
        ("complications_by_site_kind", dict(Counter(A[t]["site_kind"] for t in comp_tuple_ids))),
        ("complications_by_qualifier", dict(Counter(A[t]["qualifier"] or "none" for t in comp_tuple_ids))),
        ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_tuple_ids))),
        ("event_dictionary_values", len(ids.event)),
        ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("course_dictionary_values", len(ids.course)),
        ("relative_site_values", len(ids.rsite)),
        ("qualifier_dictionary_values", len(ids.qualifier)),
        ("site_dictionary_values", len(ids.site)),
        ("site_dictionary_by_kind", dict(Counter(ids.site_kind.values()))),
        ("course_member_only", True), ("site_member_only", True), ("qualifier_member_only", True), ("expressions_create_units", False), ("qualifier_none_is_value", True),
        ("course_split_examples", course_split),
        ("lop", [{"name": r["text"], "event_kind": r["event_kind"], "tuples": [list(t[:3]) for t in r["tuples"]], "dict_tuples": r["dict_tuples"]} for r in lop]),
        ("site_outside_member", len(site_outside_member)), ("site_outside_member_examples", site_outside_member[:10]),
        ("site_list_merges", len(site_list_merges)), ("site_list_merges_all", site_list_merges),
        ("multi_candidate_splits", len(multi_cand)), ("multi_candidate_splits_all", multi_cand),
        ("headache_x_injection_site", len(headache_injection)), ("headache_x_injection_site_tuples", headache_injection_tuples),
        ("unattached_fragments_texts", len(unattached)), ("unattached_fragments_all", unattached),
        ("raw_cells", raw_cells),
        ("expressions", OrderedDict((k, kind_summary(k)) for k in ["safety_phrase", "emergency_sign", "symptom_phrase", "evidence_statement"])),
        ("expressions_by_origin", OrderedDict((o, {"n": sum(1 for r in expr_rows if r["origin"] == o), "linked": sum(1 for r in expr_rows if r["origin"] == o and r["linked"]), "unlinked": sum(1 for r in expr_rows if r["origin"] == o and not r["linked"])}) for o in dict.fromkeys(r["origin"] for r in expr_rows))),
        ("expressions_total", {"n": len(expr_rows), "linked": sum(1 for r in expr_rows if r["linked"]), "unlinked": sum(1 for r in expr_rows if not r["linked"]), "match_status": dict(Counter(r["match_status"] for r in expr_rows)),
                               "unlinked_reasons": dict(Counter(x for r in expr_rows if not r["linked"] for x in r["unlinked_reasons"])), "patient_text_records": 4 * sum(1 for r in expr_rows if r["kind"] == "evidence_statement")}),
        ("expressions_raw_name_tuples", sum(1 for t in A.values() if t["event_kind"] == "raw_name" and "complications" not in t["origins"])),
        ("expressions_new_tuples", len(new_from_expr)),
        ("expressions_partial_linked", len(partial_linked)), ("expressions_partial_linked_examples", partial_linked[:10]),
        ("candidate_units_not_existing", len(cand_units)), ("candidate_units_not_existing_expressions", sum(cand_units.values())), ("candidate_units_not_existing_all", cand_units_list),
        ("literature_basis", dict(Counter(r.get("basis") for r in expr_rows if r["kind"] == "evidence_statement"))),
        ("tuples_total", len(A)), ("tuples_dict", len(dict_t)), ("tuples_raw_name", len(raw)),
        ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))),
        ("tuples_by_course", dict(Counter(t["course"] for t in A.values()))),
        ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))),
        ("tuples_by_qualifier", dict(Counter(t["qualifier"] or "none" for t in A.values()))),
        ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("tuples_all_dict_values", sum(1 for t in A.values() if t["all_dict_values"])),
        ("tuples_with_expression_sources", sum(1 for t in A.values() if any(s_["origin"] != "complications" for s_ in t["sources"]))),
        ("tuples_with_2plus_names_raw", sum(1 for f in af2 if f["event_kind"] == "raw_name")),
        ("folded_with_2plus_names", len(af2)),
        ("folded_with_partial_name", sum(1 for f in af2 if f["status"] == "partial")),
        ("folded_partial_detail", [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]),
        ("unregistered_distinct", len(adv_unreg)), ("unregistered_total", sum(adv_unreg.values())),
        ("unregistered_all", [list(x) for x in adv_unreg.most_common()]), ("unregistered_by_origin", {k: [list(x) for x in v.most_common()] for k, v in adv_unreg_by_origin.items()}),
        ("qualifier_names", len(q_names)), ("qualifier_names_all", q_names),
        ("qualifier_expressions", len(q_exprs)), ("qualifier_expressions_all", q_exprs),
        ("qualifier_tuples", len(q_tuples)), ("qualifier_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "course": t["course"], "qualifier": t["qualifier"], "event_kind": t["event_kind"], "basis": t.get("qualifier_basis"), "sources": len(t["sources"])} for t in q_tuples]),
        ("prefix_splits", dedupe(AT.prefix_splits)),
        ("qualifier_in_raw_dict_tuples", [{"text": t["event"], "dict_tuples": t["dict_tuples"], "extra_qualifiers": t["extra_qualifiers"]} for t in raw if any(x[3] for x in (t.get("dict_tuples") or [])) or t["extra_qualifiers"]]),
        ("layer_site_tuples", len(layer_tuples)), ("layer_site_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "course": t["course"]} for t in layer_tuples]),
        ("layer_site_candidates", len(layer_cands)), ("layer_site_candidates_all", layer_cands[:60]),
        ("layer_site_extra", len(layer_extra)), ("layer_site_extra_all", layer_extra[:60]),
        ("v24_comparison", cmp),
    ])
    s["_unregistered_all"] = adv_unreg
    return s
