#!/usr/bin/env python3
"""원장 JSON 21개 컬럼(키) 구조 기계 스캔.

입력: /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/*.json (읽기 전용)
출력: 같은 디렉토리의 bronze-ledger-column-scan.json

규칙
- 배열은 경로에 `[]` 로 접는다.
- 코드형 동적 키(M1, P1-2, M1-2-1, auto-63-..., M1_to_M7)는 `{code}` 로 접는다.
- 잎 = 스칼라 또는 빈 배열/빈 객체.
"""
import glob
import json
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

SRC = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bronze-ledger-column-scan.json")

CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")
CODE_VAL_RE = re.compile(r"^[MP]\d+(?:-\d+)*$")          # 값으로 쓰인 계열/고민 코드
CODE_PREFIX_RE = re.compile(r"^([MP]\d+(?:-\d+)*)[-_ ](.+)$")  # "M1-보톡스" 같은 코드+이름 합성
ID_TAIL_RE = re.compile(r"^(P-\d+|new-\d+|\d+(-\d+)*|[A-Z]+-\d+)$")   # 코드 뒤에 붙은 것이 이름이 아닌 id 꼬리
NAME_KEYS = {"name", "label", "cc", "cc_group", "category", "from", "to", "from_name", "to_name", "procedures", "products", "combo",
             "optimal_combo", "sequence", "pair", "categories", "recommended_base", "problem", "subcategory", "title", "patient_name",
             "target", "goal", "phase", "type", "tier", "tierLabel", "productTier", "unit", "level", "group", "ingredient", "material",
             "manufacturer", "primary_concerns", "upgrade", "avoid", "incompatible", "modality_ref", "procedure_ref", "name_ko", "name_en",
             "category_en", "concern", "concern_en", "subtitle", "plan_name", "age", "age_group", "rule", "icon", "id", "procedure_id"}
LANG_KEY_RE = re.compile(r"(?:^|_)(ko|en|ja|zh)$")
EX_LEN = 50
MAX_DISTINCT_TRACK = 20000


def fold_key(k):
    return "{code}" if CODE_KEY_RE.match(k) else k


def trunc(s):
    s = str(s).replace("\n", "⏎")
    return s if len(s) <= EX_LEN else s[:EX_LEN] + "…"


def type_name(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "list(empty)" if not v else "list"
    if isinstance(v, dict):
        return "dict(empty)" if not v else "dict"
    return type(v).__name__


class PathStat:
    def __init__(self):
        self.types = Counter()
        self.count = 0
        self.null = 0
        self.empty = 0
        self.examples = []
        self.distinct = Counter()
        self.distinct_overflow = False
        self.num_min = None
        self.num_max = None

    def add(self, v):
        self.count += 1
        t = type_name(v)
        self.types[t] += 1
        if v is None:
            self.null += 1
            return
        if (isinstance(v, str) and v.strip() == "") or (isinstance(v, (list, dict)) and not v):
            self.empty += 1
            return
        if isinstance(v, (list, dict)):
            return
        if isinstance(v, bool):
            key = str(v).lower()
        elif isinstance(v, (int, float)):
            key = repr(v)
            self.num_min = v if self.num_min is None else min(self.num_min, v)
            self.num_max = v if self.num_max is None else max(self.num_max, v)
        else:
            key = v
        if len(self.distinct) < MAX_DISTINCT_TRACK or key in self.distinct:
            self.distinct[key] += 1
        else:
            self.distinct_overflow = True
        ex = trunc(v)
        if ex not in self.examples and len(self.examples) < 3:
            self.examples.append(ex)

    def to_dict(self):
        d = OrderedDict()
        d["types"] = dict(self.types)
        d["count"] = self.count
        d["null"] = self.null
        d["empty"] = self.empty
        d["examples"] = self.examples
        d["distinct_n"] = len(self.distinct) + (1 if self.distinct_overflow else 0)
        d["distinct_overflow"] = self.distinct_overflow
        str_only = all(isinstance(k, str) and not re.match(r"^(true|false|-?\d)", k) for k in self.distinct) if self.distinct else False
        if "str" in self.types and len(self.distinct) <= 10 and not self.distinct_overflow and self.count >= 3 and len(self.distinct) < self.count:
            d["enum_like"] = True
            d["enum_values"] = [{"v": trunc(k), "n": n} for k, n in self.distinct.most_common()]
        else:
            d["enum_like"] = False
        if self.num_min is not None:
            d["num_range"] = [self.num_min, self.num_max]
        return d


class FileScan:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.bytes = os.path.getsize(path)
        with open(path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.paths = OrderedDict()          # folded path -> PathStat
        self.arrays = OrderedDict()         # folded path of array -> lengths
        self.dyn_dicts = OrderedDict()      # folded path of dynamic-key dict -> keys
        self.record_sets = OrderedDict()    # path of array-of-dict -> list of records
        self.code_hits = defaultdict(lambda: defaultdict(int))   # code -> path -> n
        self.code_name_pairs = defaultdict(Counter)              # code -> Counter(name)
        self.name_hits = defaultdict(lambda: defaultdict(int))   # short string value -> path -> n
        self.lang_paths = []

    def stat(self, p):
        if p not in self.paths:
            self.paths[p] = PathStat()
        return self.paths[p]

    def walk(self, v, p):
        if isinstance(v, dict) and v:
            keys = list(v.keys())
            dyn = all(CODE_KEY_RE.match(k) for k in keys)
            if dyn:
                self.dyn_dicts.setdefault(p, []).extend(keys)
                for k in keys:
                    self.code_hits[k][(p + "." if p else "") + "{code}"] += 1
                    child = v[k]
                    if isinstance(child, dict):
                        for nk in ("name", "category", "label", "title"):
                            if nk in child and isinstance(child[nk], str):
                                self.code_name_pairs[k][child[nk]] += 1
                                break
            for k, c in v.items():
                self.walk(c, f"{p}.{fold_key(k)}" if p else fold_key(k))
            return
        if isinstance(v, list) and v:
            self.arrays.setdefault(p, []).append(len(v))
            if all(isinstance(x, dict) for x in v):
                self.record_sets.setdefault(p, []).extend(v)
            for x in v:
                self.walk(x, p + "[]")
            return
        # leaf
        st = self.stat(p)
        st.add(v)
        if isinstance(v, str):
            s = v.strip()
            if CODE_VAL_RE.match(s):
                self.code_hits[s][p] += 1
            else:
                m = CODE_PREFIX_RE.match(s)
                if m and len(s) <= 40:
                    self.code_hits[m.group(1)][p] += 1
                    if not ID_TAIL_RE.match(m.group(2)):
                        self.code_name_pairs[m.group(1)][m.group(2)] += 1
            last_key = p.rsplit(".", 1)[-1].replace("[]", "")
            if 0 < len(s) <= 24 and "\n" not in s and last_key in NAME_KEYS:
                self.name_hits[s][p] += 1
        last = p.rsplit(".", 1)[-1].replace("[]", "")
        if LANG_KEY_RE.search(last) or last in ("ko", "en", "ja", "zh"):
            if p not in self.lang_paths:
                self.lang_paths.append(p)

    def collect_code_name_pairs_from_records(self):
        # id+name / category+name / from+from_name / to+to_name / problem_id+problem / category_id+(parent key)
        pair_keys = [("id", "name"), ("id", "category"), ("id", "title"), ("category", "name"),
                     ("from", "from_name"), ("to", "to_name"), ("problem_id", "problem"),
                     ("from_category", "from"), ("to_category", "to"), ("modality_ref", "name")]
        for recs in self.record_sets.values():
            for r in recs:
                for ck, nk in pair_keys:
                    c, n = r.get(ck), r.get(nk)
                    if isinstance(c, str) and CODE_VAL_RE.match(c) and isinstance(n, str):
                        m = CODE_PREFIX_RE.match(n)
                        self.code_name_pairs[c][m.group(2) if m else n] += 1

    def identifier_candidates(self):
        out = OrderedDict()
        for p, recs in self.record_sets.items():
            n = len(recs)
            keyset = Counter()
            for r in recs:
                for k in r:
                    keyset[fold_key(k)] += 1
            cands = []
            for k in ("id", "code", "problem_id", "category_id", "category", "name", "title", "label",
                      "cc", "problem", "from", "to", "pmid", "doi", "statement", "procedure_id", "zone"):
                if k in keyset:
                    vals = [r.get(k) for r in recs if k in r]
                    hashable = [json.dumps(x, ensure_ascii=False, sort_keys=True) if isinstance(x, (list, dict)) else x for x in vals]
                    dup = [v for v, c in Counter(hashable).items() if c > 1]
                    cands.append(OrderedDict(key=k, present=len(vals), records=n,
                                             distinct=len(set(hashable)), unique=(len(set(hashable)) == len(vals) == n),
                                             duplicates=[trunc(d) for d in dup[:10]]))
            sparse = {k: c for k, c in keyset.items() if c < n}
            out[p] = OrderedDict(records=n, keys=dict(keyset), sparse_keys=sparse, candidates=cands)
        return out

    def top_level(self):
        d = self.data
        if isinstance(d, list):
            return OrderedDict(kind="array", length=len(d))
        meta, datak = [], []
        for k, v in d.items():
            if isinstance(v, (list, dict)):
                datak.append(OrderedDict(key=k, kind=type_name(v), size=len(v)))
            else:
                meta.append(OrderedDict(key=k, value=trunc(v)))
        dyn = all(CODE_KEY_RE.match(k) for k in d)
        return OrderedDict(kind="object", dynamic_code_keys=dyn, meta=meta, data=datak)

    def run(self):
        self.walk(self.data, "")
        self.collect_code_name_pairs_from_records()
        res = OrderedDict()
        res["file"] = self.name
        res["bytes"] = self.bytes
        res["top_level"] = self.top_level()
        res["arrays"] = OrderedDict((p, OrderedDict(n_arrays=len(l), min=min(l), max=max(l), total=sum(l))) for p, l in self.arrays.items())
        res["dynamic_key_dicts"] = OrderedDict((p, OrderedDict(n_keys=len(ks), keys=ks[:60])) for p, ks in self.dyn_dicts.items())
        res["leaf_paths"] = OrderedDict((p, s.to_dict()) for p, s in self.paths.items())
        res["leaf_count"] = len(self.paths)
        res["record_sets"] = self.identifier_candidates()
        res["lang_paths"] = self.lang_paths
        res["observations"] = self.observations(res)
        return res

    def observations(self, res):
        obs = []
        for p, s in res["leaf_paths"].items():
            ts = [t for t in s["types"] if t != "null"]
            if len(ts) > 1:
                obs.append(f"타입 섞임: `{p}` → {s['types']}")
            if s["null"]:
                obs.append(f"null {s['null']}/{s['count']}: `{p}`")
            if s["empty"]:
                obs.append(f"빈값 {s['empty']}/{s['count']}: `{p}`")
        for p, rs in res["record_sets"].items():
            if rs["sparse_keys"]:
                obs.append(f"일부 레코드에만 있는 키 (`{p}`, {rs['records']}건): " + ", ".join(f"{k}={c}" for k, c in rs["sparse_keys"].items()))
            for c in rs["candidates"]:
                if c["key"] in ("id", "problem_id", "code", "pmid") and c["duplicates"]:
                    obs.append(f"식별자 중복 (`{p}`.{c['key']}): {c['duplicates']}")
        return obs


def normalize_name(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[\s_\-/·,.]+", "", s)
    return s


def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.json")))
    result = OrderedDict(source=SRC, n_files=len(files), files=OrderedDict())
    all_codes = defaultdict(lambda: defaultdict(dict))   # code -> file -> {path: n}
    code_names = defaultdict(lambda: defaultdict(Counter))  # code -> file -> Counter(name)
    name_hits = defaultdict(lambda: defaultdict(dict))   # name -> file -> {path:n}
    lang = OrderedDict()
    for fp in files:
        fs = FileScan(fp)
        r = fs.run()
        result["files"][fs.name] = r
        for code, paths in fs.code_hits.items():
            all_codes[code][fs.name] = dict(paths)
        for code, cnt in fs.code_name_pairs.items():
            code_names[code][fs.name] = cnt
        for nm, paths in fs.name_hits.items():
            name_hits[nm][fs.name] = dict(paths)
        if fs.lang_paths:
            lang[fs.name] = fs.lang_paths
        print(f"{fs.name:34s} {fs.bytes:8d}B  leaves={len(fs.paths):3d}", file=sys.stderr)

    # 교차 식별자: 코드
    def code_sort(c):
        m = re.match(r"([MP])(\d+)(.*)", c)
        return (m.group(1), int(m.group(2)), m.group(3))
    cross_codes = OrderedDict()
    for code in sorted(all_codes, key=code_sort):
        cross_codes[code] = OrderedDict(
            files=OrderedDict((f, all_codes[code][f]) for f in sorted(all_codes[code])),
            names=OrderedDict((f, dict(code_names[code][f])) for f in sorted(code_names[code])) if code in code_names else {},
        )
    result["cross_codes"] = cross_codes

    # 코드 → 이름 불일치 (파일 간 다른 이름)
    conflicts = OrderedDict()
    for code, per_file in code_names.items():
        names = set()
        for cnt in per_file.values():
            names.update(cnt.keys())
        if len(names) > 1:
            conflicts[code] = OrderedDict((f, dict(c)) for f, c in sorted(per_file.items()))
    result["code_name_variants"] = OrderedDict(sorted(conflicts.items(), key=lambda kv: code_sort(kv[0])))

    # 이름 기반 교차: taxonomy 의 정준 이름(계열·고민·세부·항목·제품)이 다른 파일 어디에 나오나
    tax = result["files"]["taxonomy.json"]
    canon = OrderedDict()
    tdata = json.load(open(os.path.join(SRC, "taxonomy.json"), encoding="utf-8"))
    for m in tdata["modality"]:
        canon[m["category"]] = ("modality.category", m["id"])
        for sc in m.get("subcategories", []):
            for it in sc.get("items", []):
                canon.setdefault(it["name"], ("modality.subcategories[].items[].name", it["id"]))
        for pr in m.get("products", []) or []:
            if isinstance(pr, dict) and "name" in pr:
                canon.setdefault(pr["name"], ("modality.products[].name", m["id"]))
            elif isinstance(pr, str):
                canon.setdefault(pr, ("modality.products[]", m["id"]))
    for p in tdata["problem"]:
        canon[p["category"]] = ("problem.category", p["id"])
        for sc in p.get("subcategories", []):
            canon.setdefault(sc["label"], ("problem.subcategories[].label", sc["id"]))
            for it in sc.get("items", []):
                canon.setdefault(it["name"], ("problem.subcategories[].items[].name", it["id"]))
    pdata = json.load(open(os.path.join(SRC, "products.json"), encoding="utf-8"))
    for k, v in pdata.items():
        if isinstance(v, dict):
            for pr in v["products"]:
                canon.setdefault(pr["name"], ("products.json " + k, v["category_id"]))
    cross_names = OrderedDict()
    for nm, (origin, oid) in canon.items():
        hits = name_hits.get(nm, {})
        if len(hits) >= 1:
            cross_names[nm] = OrderedDict(origin=origin, origin_id=oid,
                                          files=OrderedDict((f, hits[f]) for f in sorted(hits)))
    result["cross_names"] = cross_names

    # 표기 변형: 정규화하면 같은데 표면형이 다른 짧은 문자열
    norm_groups = defaultdict(set)
    for nm in name_hits:
        n = normalize_name(nm)
        if len(n) >= 2:
            norm_groups[n].add(nm)
    variants = OrderedDict()
    for n, forms in sorted(norm_groups.items()):
        if len(forms) > 1 and not all(CODE_VAL_RE.match(f) or re.match(r"^[MP]\d+(-\d+)*-", f) for f in forms):
            variants[n] = OrderedDict((f, OrderedDict((fn, name_hits[f][fn]) for fn in sorted(name_hits[f]))) for f in sorted(forms))
    result["surface_variants"] = variants


    # ---------- 교차 점검 (원장 간 기계 비교) ----------
    def load(n):
        return json.load(open(os.path.join(SRC, n), encoding="utf-8"))
    cc = OrderedDict()
    mod_ids = [m["id"] for m in tdata["modality"]]
    prob_ids = [p["id"] for p in tdata["problem"]]
    # (a) 파일별 M/P 코드 커버리지
    cov = OrderedDict()
    for code in mod_ids + prob_ids:
        cov[code] = sorted(all_codes.get(code, {}).keys())
    cc["code_coverage_by_file"] = cov
    file_code_sets = OrderedDict()
    for fn in result["files"]:
        s_ = sorted({c for c in all_codes if fn in all_codes[c] and re.match(r"^[MP]\d+$", c)}, key=code_sort)
        file_code_sets[fn] = s_
    cc["file_top_code_sets"] = file_code_sets
    # (b) extracted.json[M] vs taxonomy.modality[M].extracted
    ex = load("extracted.json")
    cmp = OrderedDict()
    for m in tdata["modality"]:
        a = ex.get(m["id"]); b = m.get("extracted")
        if a is None or b is None:
            cmp[m["id"]] = "missing"
            continue
        a_core = {k: v for k, v in a.items() if k not in ("name", "name_en", "source", "source_type", "extracted_at", "procedure_id", "guardrail_version", "updated")}
        same = (a_core == b)
        diff_keys = sorted(set(a_core) ^ set(b)) + sorted(k for k in set(a_core) & set(b) if a_core[k] != b[k])
        cmp[m["id"]] = OrderedDict(identical_core=same, extracted_only_keys=sorted(set(a) - set(b)), taxonomy_only_keys=sorted(set(b) - set(a)), differing_keys=diff_keys)
    cc["extracted_vs_taxonomy_extracted"] = cmp
    # (c) taxonomy modality name vs category
    cc["taxonomy_modality_name_vs_category"] = [OrderedDict(id=m["id"], category=m["category"], name=m.get("name")) for m in tdata["modality"] if m.get("name") != m["category"]]
    # (d) products.json vs taxonomy.modality[].products
    tp = OrderedDict((m["id"], [p_["name"] for p_ in (m.get("products") or [])]) for m in tdata["modality"])
    pj = OrderedDict()
    for k, v in pdata.items():
        if isinstance(v, dict):
            cid = v["category_id"]
            names = [p_["name"] for p_ in v["products"]]
            pj[k] = OrderedDict(category_id=cid, n=len(names), names=names)
    pcmp = OrderedDict()
    for k, v in pj.items():
        cids = v["category_id"] if isinstance(v["category_id"], list) else [v["category_id"]]
        tax_names = []
        for cid in cids:
            tax_names += tp.get(cid, [])
        pcmp[k] = OrderedDict(category_id=v["category_id"], products_json_only=sorted(set(v["names"]) - set(tax_names)), taxonomy_only=sorted(set(tax_names) - set(v["names"])), common=len(set(v["names"]) & set(tax_names)))
    cc["products_json_vs_taxonomy_products"] = OrderedDict(by_section=pcmp, taxonomy_products_per_modality=OrderedDict((k, len(v)) for k, v in tp.items()))
    # (e) pih-risk procedure_ref ∈ taxonomy item ids
    item_ids = {it["id"]: (m["id"], sc["id"], it["name"]) for m in tdata["modality"] for sc in m["subcategories"] for it in sc["items"]}
    sub_ids = {sc["id"]: (m["id"], sc["label"]) for m in tdata["modality"] for sc in m["subcategories"]}
    pih = load("pih-risk.json")
    cc["pih_procedure_ref_check"] = [OrderedDict(procedure_ref=p_["procedure_ref"], category=p_["category"], name=p_["name"],
                                                 in_taxonomy_items=p_["procedure_ref"] in item_ids, in_taxonomy_subcategories=p_["procedure_ref"] in sub_ids,
                                                 taxonomy_item_name=item_ids.get(p_["procedure_ref"], (None, None, None))[2]) for p_ in pih["procedures"]]
    refc = Counter(p_["procedure_ref"] for p_ in pih["procedures"])
    cc["pih_procedure_ref_duplicates"] = {k: v for k, v in refc.items() if v > 1}
    # (f) problem-packages: cc vs taxonomy problem items; procedure names; products
    pp = load("problem-packages.json")
    tax_prob_items = {(p_["id"], it["name"]) for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"]}
    tax_prob_item_names = Counter(it["name"] for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"])
    pp_cc = {(pr["problem_id"], c["cc"]) for pr in pp["problems"] for c in pr["complaints"]}
    cc["problem_packages_cc_vs_taxonomy_items"] = OrderedDict(
        taxonomy_items=len(tax_prob_items), packages_cc=len(pp_cc),
        only_in_taxonomy=sorted(f"{a}:{b}" for a, b in tax_prob_items - pp_cc),
        only_in_packages=sorted(f"{a}:{b}" for a, b in pp_cc - tax_prob_items),
        cc_group_vs_subcategory_label_mismatch=[])
    # cc_group vs subcategory label
    sc_label_by_item = {}
    for p_ in tdata["problem"]:
        for sc in p_["subcategories"]:
            for it in sc["items"]:
                sc_label_by_item[(p_["id"], it["name"])] = sc["label"]
    mm = []
    for pr in pp["problems"]:
        for c in pr["complaints"]:
            lbl = sc_label_by_item.get((pr["problem_id"], c["cc"]))
            if lbl is not None and lbl != c["cc_group"]:
                mm.append(OrderedDict(problem_id=pr["problem_id"], cc=c["cc"], cc_group=c["cc_group"], taxonomy_label=lbl))
    cc["problem_packages_cc_vs_taxonomy_items"]["cc_group_vs_subcategory_label_mismatch"] = mm
    pn = Counter(); pnc = defaultdict(Counter); prod = Counter(); combo_names = Counter()
    for pr in pp["problems"]:
        for c in pr["complaints"]:
            for q in c["procedures"]:
                pn[q["name"]] += 1; pnc[q["name"]][q["category"]] += 1
                for x in q.get("products") or []:
                    prod[x] += 1
            for cb in c.get("combos") or []:
                for x in cb["combo"]:
                    combo_names[x] += 1
    mod_cat = {m["id"]: m["category"] for m in tdata["modality"]}
    cc["problem_packages_procedure_names"] = [OrderedDict(name=n, n=c, categories=dict(pnc[n]), taxonomy_category_of_code={k: mod_cat.get(k) for k in pnc[n]}) for n, c in pn.most_common()]
    all_prod_names = set()
    for v in pj.values():
        all_prod_names |= set(v["names"])
    tax_prod_names = {x for v in tp.values() for x in v}
    tax_item_names = {it["name"] for m in tdata["modality"] for sc in m["subcategories"] for it in sc["items"]}
    cc["problem_packages_products"] = [OrderedDict(name=n, n=c, in_products_json=n in all_prod_names, in_taxonomy_products=n in tax_prod_names, in_taxonomy_items=n in tax_item_names) for n, c in prod.most_common()]
    cc["problem_packages_combo_member_names"] = [OrderedDict(name=n, n=c, is_procedure_name=n in pn) for n, c in combo_names.most_common()]
    # (g) problem-combos
    pc = load("problem-combos.json")
    cc["problem_combos_problems"] = [OrderedDict(problem_id=c["problem_id"], problem=c["problem"], taxonomy_category=next((p_["category"] for p_ in tdata["problem"] if p_["id"] == c["problem_id"]), None), n_packages=len(c["packages"])) for c in pc["combos"]]
    cc["problem_combos_missing_problems"] = [p_["id"] + ":" + p_["category"] for p_ in tdata["problem"] if p_["id"] not in {c["problem_id"] for c in pc["combos"]}]
    pcp = Counter(x for c in pc["combos"] for pk in c["packages"] for x in pk["products"])
    cc["problem_combos_products_values"] = [OrderedDict(v=k, n=n) for k, n in pcp.most_common()]
    # (h) synergy from/to
    sy = load("synergy.json")
    ft = Counter(); mism = []
    for l in sy["links"]:
        ft[l["from"]] += 1; ft[l["to"]] += 1
        for a, b in (("from", "from_category"), ("to", "to_category")):
            m_ = CODE_PREFIX_RE.match(l[a])
            if not m_ or m_.group(1) != l[b]:
                mism.append(OrderedDict(value=l[a], category=l[b]))
    cc["synergy_node_names"] = [OrderedDict(v=k, n=n) for k, n in sorted(ft.items(), key=lambda kv: code_sort(CODE_PREFIX_RE.match(kv[0]).group(1)) if CODE_PREFIX_RE.match(kv[0]) else ("Z", 0, kv[0]))]
    cc["synergy_prefix_category_mismatch"] = mism
    cc["synergy_type_values"] = dict(Counter(l["type"] for l in sy["links"]))
    cc["synergy_target_values"] = dict(Counter(l["target"] for l in sy["links"]))
    # (i) treatment-sequence / optimization free-text names
    ts = load("treatment-sequence.json")
    cc["treatment_sequence_names"] = OrderedDict(
        sequence_categories=[x for so in ts["sequence_order"] for x in so["categories"]],
        incompatible_pairs=[so["pair"] for so in ts["incompatible_same_day"]],
        common_combo_sequences=OrderedDict((so["name"], so["sequence"]) for so in ts["common_combos"]),
        minimum_intervals=[OrderedDict(**{k: v for k, v in so.items()}) for so in ts["minimum_intervals"]])
    to = load("treatment-optimization.json")
    oc = Counter(x for b in to["by_concern"] for s_ in b["severity_levels"] for x in s_["optimal_combo"])
    cc["treatment_optimization_optimal_combo_values"] = [OrderedDict(v=k, n=n) for k, n in oc.most_common()]
    cc["treatment_optimization_age_values"] = OrderedDict(recommended_base=sorted({x for b in to["by_age_group"] for x in b["recommended_base"]}), primary_concerns=sorted({x for b in to["by_age_group"] for x in b["primary_concerns"]}), annual_schedule_procedures=sorted({x for a in to["annual_plans"] for s_ in a["schedule"] for x in s_["procedures"]}))
    cc["treatment_optimization_concern_vs_taxonomy_problem"] = [OrderedDict(concern=b["concern"], concern_en=b["concern_en"], icon=b["icon"]) for b in to["by_concern"]]
    # (j) taxonomy problem items modality_ref
    bad = [OrderedDict(item=it["name"], ref=r) for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"] for r in it["modality_ref"] if r not in mod_ids]
    cc["taxonomy_problem_modality_ref_unknown"] = bad
    cc["taxonomy_problem_items_empty_modality_ref"] = [f'{p_["id"]}:{it["name"]}' for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"] if not it["modality_ref"]]
    # (k) version/updated table
    cc["version_updated"] = OrderedDict((fn, OrderedDict(version=load(fn).get("version"), updated=load(fn).get("updated"))) for fn in result["files"])
    # (l) key casing per file
    def keys_of(o, acc):
        if isinstance(o, dict):
            for k, v in o.items():
                if not CODE_KEY_RE.match(k):
                    acc.add(k)
                keys_of(v, acc)
        elif isinstance(o, list):
            for x in o:
                keys_of(x, acc)
        return acc
    casing = OrderedDict()
    for fn in result["files"]:
        ks = keys_of(load(fn), set())
        camel = sorted(k for k in ks if re.search(r"[a-z][A-Z]", k))
        snake = sorted(k for k in ks if "_" in k)
        casing[fn] = OrderedDict(n_keys=len(ks), camelCase=camel, snake_case_n=len(snake))
    cc["key_casing"] = casing
    # (m) taxonomy per-modality counts
    cc["taxonomy_modality_counts"] = [OrderedDict(id=m["id"], category=m["category"], group=m["group"], subcategories=len(m["subcategories"]),
                                                  items=sum(len(sc["items"]) for sc in m["subcategories"]), products=len(m.get("products") or []),
                                                  empty_item_subcats=[sc["id"] + ":" + sc["label"] for sc in m["subcategories"] if not sc["items"]]) for m in tdata["modality"]]
    def id_pattern(i):
        if re.match(r"^M\d+-\d+-\d+$", i): return "M#-#-#"
        if re.match(r"^M\d+-[A-Za-z가-힣]+-\d+$", i): return "M#-word-#"
        if re.match(r"^auto-M\d+-\d+$", i): return "auto-M#-timestamp"
        if re.match(r"^auto-M\d+-[A-Za-z]+-\d+$", i): return "auto-M#-word-timestamp"
        if re.match(r"^auto-\d+-\d+$", i): return "auto-#-timestamp"
        if re.match(r"^new-\d+$", i): return "new-timestamp"
        return "other:" + i
    idp = OrderedDict()
    for m in tdata["modality"]:
        c_ = Counter(id_pattern(it["id"]) for sc in m["subcategories"] for it in sc["items"])
        idp[m["id"]] = dict(c_)
    cc["taxonomy_modality_item_id_patterns"] = idp
    cc["taxonomy_modality_subcategory_id_patterns"] = dict(Counter(("M#-#" if re.match(r"^M\d+-\d+$", sc["id"]) else "other:" + sc["id"]) for m in tdata["modality"] for sc in m["subcategories"]))
    cc["taxonomy_problem_item_id_patterns"] = dict(Counter(id_pattern(it["id"]) for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"]))
    cc["taxonomy_product_id_patterns"] = dict(Counter(("M#-P-#" if re.match(r"^M\d+-P-\d+$", pr["id"]) else "other:" + pr["id"]) for m in tdata["modality"] for pr in (m.get("products") or [])))
    cc["taxonomy_problem_counts"] = [OrderedDict(id=p_["id"], category=p_["category"], subcategories=len(p_["subcategories"]), items=sum(len(sc["items"]) for sc in p_["subcategories"])) for p_ in tdata["problem"]]
    dupn = [n for n, c in Counter(it["name"] for m in tdata["modality"] for sc in m["subcategories"] for it in sc["items"]).items() if c > 1]
    cc["taxonomy_modality_item_name_duplicates"] = [OrderedDict(name=n, ids=[k for k, v in item_ids.items() if v[2] == n]) for n in dupn]
    dupp = [n for n, c in tax_prob_item_names.items() if c > 1]
    cc["taxonomy_problem_item_name_duplicates"] = [OrderedDict(name=n, where=[f'{p_["id"]}/{sc["id"]}' for p_ in tdata["problem"] for sc in p_["subcategories"] for it in sc["items"] if it["name"] == n]) for n in dupp]
    # 세부 extracted 키 변형(taxonomy items)
    kv = Counter()
    for m in tdata["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                e = it.get("extracted") or {}
                for sect in ("safety", "indications", "onset_duration"):
                    for k in (e.get(sect) or {}):
                        kv[f"{sect}.{k}"] += 1
    cc["taxonomy_item_extracted_subkeys"] = OrderedDict(sorted(kv.items()))
    # (n) literature per code
    lit = load("literature-evidence.json")
    cc["literature_per_code"] = [OrderedDict(code=k, name=v["name"], moa=len(v["moa"]), adverse_effects=len(v["adverse_effects"]), effects=len(v["effects"])) for k, v in lit["categories"].items()]
    # (o) 17 계열 × 파일 커버리지 매트릭스 (최상위 레코드 id/category 기준)
    cc["modality_file_matrix"] = OrderedDict((m["id"], OrderedDict((fn, m["id"] in file_code_sets[fn]) for fn in result["files"])) for m in tdata["modality"])
    # (p) complications/timeline 가 다루는 계열
    cc["complications_categories"] = [c["id"] + ":" + c["name"] for c in load("complications.json")["categories"]]
    cc["timeline_categories"] = [t["category"] + ":" + t["name"] + " (id=" + t["id"] + ")" for t in load("post-procedure-timeline.json")["timelines"]]
    cc["pih_categories"] = dict(Counter(p_["category"] for p_ in pih["procedures"]))
    cc["contraindication_pairs"] = sorted({r["from"] + "→" + r["to"] for r in load("contraindications.json")["rules"]}, key=lambda x: (code_sort(x.split("→")[0]), code_sort(x.split("→")[1])))
    # (q) market-pricing unit values
    mp = load("market-pricing.json")
    cc["market_pricing_units"] = dict(Counter(i["unit"] for c in mp["categories"] for i in c["items"]))
    cc["market_pricing_items_per_category"] = OrderedDict((c["id"], len(c["items"])) for c in mp["categories"])
    # (r) procedure-comparison categories/names
    pcmp2 = load("procedure-comparison.json")
    cc["procedure_comparison_procedures"] = [OrderedDict(comparison=c["id"], name=p_["name"], category=p_["category"]) for c in pcmp2["comparisons"] for p_ in c["procedures"]]
    # (s) combo-recipes goal/intensity
    cr = load("combo-recipes.json")
    cc["combo_recipes"] = [OrderedDict(id=r["id"], name=r["name"], goal=r["goal"], intensity=r["intensity"], procedures=r["procedures"]) for r in cr["recipes"]]
    # (t) 계열 이름 표기 - 파일별 M코드 이름
    cc["modality_names_by_file"] = OrderedDict((code, OrderedDict((f, list(c.keys())) for f, c in sorted(code_names[code].items()))) for code in mod_ids)
    # ---------- 추가 점검 ----------
    ex2 = OrderedDict()
    # literature patient_* 텍스트 안의 각주 잔재/문자 섞임
    cit = Counter(); mixed = Counter(); samples = defaultdict(list)
    for code, cat in lit["categories"].items():
        for sect in ("moa", "adverse_effects", "effects"):
            for st in cat[sect]:
                for lang_ in ("ko", "en", "zh", "ja"):
                    t = st.get("patient_" + lang_, "")
                    if re.search(r"\[\d+\]", t):
                        cit[lang_] += 1
                        if len(samples["cite_" + lang_]) < 2: samples["cite_" + lang_].append(trunc(t))
                    has_hangul = re.search(r"[가-힣]", t) is not None
                    if lang_ != "ko" and has_hangul:
                        mixed[lang_] += 1
                        if len(samples["hangul_in_" + lang_]) < 3: samples["hangul_in_" + lang_].append(trunc(t))
    ex2["literature_patient_text_citation_remnants"] = dict(cit)
    ex2["literature_patient_text_hangul_in_other_lang"] = dict(mixed)
    ex2["literature_samples"] = dict(samples)
    ex2["literature_empty_sections"] = OrderedDict((sect, [c for c, v in lit["categories"].items() if not v[sect]]) for sect in ("moa", "adverse_effects", "effects"))
    # market-pricing 순서 점검
    ex2["market_pricing_order_violations"] = [OrderedDict(category=c["id"], name=i["name"], low=i["low"], mid=i["mid"], high=i["high"]) for c in mp["categories"] for i in c["items"] if not (i["low"] <= i["mid"] <= i["high"])]
    # procedure-profiles
    pf = load("procedure-profiles.json")["profiles"]
    ex2["procedure_profiles_duration_violations"] = [p_["id"] for p_ in pf if p_["durationMin"] > p_["durationMax"]]
    po = Counter(p_["phaseOrder"] for p_ in pf)
    ex2["procedure_profiles_phaseOrder_duplicates"] = {str(k): [p_["id"] for p_ in pf if p_["phaseOrder"] == k] for k, v in po.items() if v > 1}
    ex2["procedure_profiles_phase_values"] = OrderedDict((p_["id"], OrderedDict(phase=p_["phase"], phaseOrder=p_["phaseOrder"], mechanism=p_["mechanism"], needsAnesthesia=p_["needsAnesthesia"])) for p_ in pf)
    # enum 키 vs 정의 키 매칭
    comp = load("complications.json")
    ex2["complications_severity_values_vs_levels"] = OrderedDict(levels=list(comp["severity_levels"].keys()), used=sorted({c["severity"] for cat in comp["categories"] for c in cat["complications"]}))
    ex2["pih_risk_values_vs_levels"] = OrderedDict(levels=list(pih["risk_levels"].keys()), used=sorted({p_["pih_risk"] for p_ in pih["procedures"]}))
    ppt = load("post-procedure-timeline.json")
    ex2["timeline_phase_keys_vs_reaction_levels"] = OrderedDict(levels=list(ppt["reaction_levels"].keys()), phase_keys=sorted({k for t in ppt["timelines"] for ph in t["phases"] for k in ph.keys()}))
    ex2["timeline_period_values"] = dict(Counter(ph["period"] for t in ppt["timelines"] for ph in t["phases"]))
    ex2["procedure_comparison_pih_risk_values"] = dict(Counter(p_["pih_risk"] for c in pcmp2["comparisons"] for p_ in c["procedures"]))
    ex2["procedure_comparison_pain_values"] = dict(Counter(p_["pain"] for c in pcmp2["comparisons"] for p_ in c["procedures"]))
    ex2["procedure_comparison_ids"] = [OrderedDict(id=c["id"], title=c["title"], n=len(c["procedures"])) for c in pcmp2["comparisons"]]
    prc = load("pre-procedure-checklist.json")
    ex2["pre_checklist_type_values"] = OrderedDict(universal=dict(Counter(u["type"] for u in prc["universal_checks"])), category_specific=dict(Counter(c["type"] for cat in prc["category_specific"] for c in cat["checks"])))
    # products.json 자리표시자
    ex2["products_json_placeholders"] = [OrderedDict(section=k, name=p_["name"], manufacturer=p_.get("manufacturer"), country=p_.get("country"), mfds=p_.get("mfds", "KEY_ABSENT")) for k, v in pdata.items() if isinstance(v, dict) for p_ in v["products"] if p_.get("manufacturer") == "-" or p_.get("country") == "-" or "mfds" not in p_ or p_.get("mfds") is False]
    ex2["products_json_section_category_id_types"] = OrderedDict((k, type_name(v["category_id"])) for k, v in pdata.items() if isinstance(v, dict))
    # taxonomy products mfds null 위치
    ex2["taxonomy_products_mfds_null"] = [m["id"] + ":" + pr["name"] for m in tdata["modality"] for pr in (m.get("products") or []) if pr.get("mfds") is None]
    ex2["taxonomy_items_detail_empty"] = [m["id"] + ":" + it["id"] + ":" + it["name"] for m in tdata["modality"] for sc in m["subcategories"] for it in sc["items"] if not (it.get("detail") or "").strip()]
    ex2["taxonomy_items_with_flags"] = [OrderedDict(modality=m["id"], id=it["id"], name=it["name"], flags=[k for k in ("verification_needed", "classification_issue", "is_marketing_name", "canonical_category", "correction_note", "reclassified_to") if k in it]) for m in tdata["modality"] for sc in m["subcategories"] for it in sc["items"] if any(k in it for k in ("verification_needed", "classification_issue", "is_marketing_name", "correction_note", "reclassified_to"))]
    ex2["taxonomy_modalities_without_extracted_or_products"] = [OrderedDict(id=m["id"], has_extracted="extracted" in m, products_n=len(m.get("products") or [])) for m in tdata["modality"]]
    ex2["extracted_json_key_order"] = list(ex.keys())
    ex2["extracted_source_values"] = dict(Counter(v["source"] for v in ex.values()))
    ex2["extracted_source_type_values"] = dict(Counter(v["source_type"] for v in ex.values()))
    ex2["extracted_serious_null_codes"] = [k for k, v in ex.items() if v["safety"].get("serious") is None]
    ex2["extracted_safety_keys"] = dict(Counter(k for v in ex.values() for k in v["safety"].keys()))
    # synergy 대상 타깃 근사 중복
    ex2["synergy_from_to_category_counts"] = OrderedDict(from_category=dict(Counter(l["from_category"] for l in sy["links"])), to_category=dict(Counter(l["to_category"] for l in sy["links"])))
    # problem-combos tier/productTier
    ex2["problem_combos_enum"] = OrderedDict(tier=dict(Counter(pk["tier"] for c in pc["combos"] for pk in c["packages"])), tierLabel=dict(Counter(pk["tierLabel"] for c in pc["combos"] for pk in c["packages"])), productTier=dict(Counter(pk["productTier"] for c in pc["combos"] for pk in c["packages"])), priceRange=[pk["priceRange"] for c in pc["combos"] for pk in c["packages"]])
    ex2["problem_combos_package_id_vs_taxonomy_subcategory_id"] = [OrderedDict(package_id=pk["id"], package_name=pk["name"], taxonomy_subcategory_label=sub_ids_p.get(pk["id"])) for c in pc["combos"] for pk in c["packages"]] if (sub_ids_p := {sc["id"]: sc["label"] for p_ in tdata["problem"] for sc in p_["subcategories"]}) else []
    # anatomy
    an = load("anatomy-danger-zones.json")
    ex2["anatomy_zones"] = [OrderedDict(id=z["id"], name_ko=z["name_ko"], danger_level=z["danger_level"], danger_color=z["danger_color"], filler_risk_level=z["filler_specific"]["risk_level"], tissue_keys=sorted(z["tissue_data"].keys())) for z in an["zones"]]
    # consent 중복 문자열
    cons = load("consent-checklist.json")
    ex2["consent_contraindication_repeats"] = [OrderedDict(v=k, n=n) for k, n in Counter(x for c in cons["categories"] for x in c["contraindications"]).most_common(8)]
    # treatment-sequence/ optimization 단위
    ex2["treatment_optimization_evidence_level"] = dict(Counter(s_["evidence_level"] for b in to["by_concern"] for s_ in b["severity_levels"]))
    ex2["treatment_optimization_total_duration"] = dict(Counter(s_["total_duration"] for b in to["by_concern"] for s_ in b["severity_levels"]))
    ex2["combination_rules_priority_consensus"] = [OrderedDict(rule=r["rule"], priority=r["priority"], consensus=r["consensus"]) for r in to["combination_rules"]]
    # 계열명(17)과 고민명(14) 정준 이름
    ex2["canonical_modality_names"] = OrderedDict((m["id"], OrderedDict(ko=m["category"], en=m["category_en"], group=m["group"])) for m in tdata["modality"])
    ex2["canonical_problem_names"] = OrderedDict((p_["id"], OrderedDict(ko=p_["category"], en=p_["category_en"])) for p_ in tdata["problem"])
    result["extra_checks"] = ex2
    result["cross_checks"] = cc
    result["lang_paths"] = lang
    result["total_leaf_paths"] = sum(r["leaf_count"] for r in result["files"].values())
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"written {OUT}; total leaf paths = {result['total_leaf_paths']}", file=sys.stderr)


if __name__ == "__main__":
    main()
