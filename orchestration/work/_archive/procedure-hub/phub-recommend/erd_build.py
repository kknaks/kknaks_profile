# -*- coding: utf-8 -*-
"""ERD v1 산출물 생성기. 입력: 원장 21 + 스캔 JSON + erd_spec/erd_colmap. 출력 4개 + 검산 결과 부착."""
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec as S  # noqa
import erd_colmap as C  # noqa

WORK = "/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend"
LEDGER = S.LEDGER_DIR
SCAN = json.load(open(os.path.join(WORK, "bronze-ledger-column-scan.json"), encoding="utf-8"))
FILES = list(SCAN["files"].keys())
L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in FILES}
CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")
MCODE_RE = re.compile(r"^(M\d+)(?:[-_ ](.+))?$")


def norm(s):
    if s is None:
        return None
    s = unicodedata.normalize("NFKC", str(s)).casefold()
    return re.sub(r"\s+", "", s)


def mkid(prefix, key):
    return f"{prefix}-{hashlib.sha256(norm(key).encode()).hexdigest()[:10]}"


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ---------------------------------------------------------------------------
# 경로 워커: 스캔과 같은 규칙 ([] = 배열, {code} = 코드형 동적 키)
# ---------------------------------------------------------------------------
def walk(data, path):
    """yield (value, ctx) ctx = {'codes': [...], 'parents': [...dicts/lists...], 'record': 가장 가까운 dict}"""
    toks = path.split(".") if path else []

    def rec(node, i, codes, parents):
        if i == len(toks):
            yield node, {"codes": codes, "parents": parents, "record": next((p for p in reversed(parents) if isinstance(p, dict)), None)}
            return
        tok = toks[i]
        arr = tok.endswith("[]")
        key = tok[:-2] if arr else tok
        if key == "{code}":
            if not isinstance(node, dict):
                return
            for k, v in node.items():
                if CODE_KEY_RE.match(k):
                    yield from rec_after(v, i, arr, codes + [k], parents + [node])
        else:
            if not isinstance(node, dict) or key not in node:
                return
            yield from rec_after(node[key], i, arr, codes, parents + [node])

    def rec_after(v, i, arr, codes, parents):
        if arr:
            if isinstance(v, list):
                if not v and i == len(toks) - 1:
                    return  # 빈 배열은 "x[]" 잎이 아니라 "x" 잎
                for item in v:
                    yield from rec(item, i + 1, codes, parents + [v])
        else:
            yield from rec(v, i + 1, codes, parents)

    yield from rec(data, 0, [], [])


def values_at(file, path):
    return [(v, ctx) for v, ctx in walk(L[file], path) if not isinstance(v, (list, dict))]


def distinct_at(file, path):
    c = Counter()
    for v, _ in values_at(file, path):
        if v is None:
            continue
        c[v if not isinstance(v, bool) else str(v).lower()] += 1
    return c


# ---------------------------------------------------------------------------
# 사전
# ---------------------------------------------------------------------------
DICTS = OrderedDict()


class Dict_:
    def __init__(self, name, label, note=""):
        self.name, self.label, self.note = name, label, note
        self.entries = OrderedDict()  # norm(canonical) -> entry
        self.candidates = []          # 정준값에 연결되지 않은 후보
        DICTS[name] = self

    def src(self, file, path, n, kind="value"):
        return {"file": file, "path": path, "n": n, "kind": kind}

    def add_canonical(self, value, file, path, n=1, kind="value", **extra):
        k = norm(value)
        e = self.entries.get(k)
        if e is None:
            e = {"id": mkid("DIC", f"{self.name}|{value}"), "canonical": value, "sources": [], "synonyms": [], "definition": None}
            e.update(extra)
            self.entries[k] = e
        e["sources"].append(self.src(file, path, n, kind))
        for kk, vv in extra.items():
            if kk not in e or e[kk] in (None, "", [], {}):
                e[kk] = vv
        return e

    def add_synonym(self, canonical_norm, value, file, path, n=1, link="id-join", kind="value"):
        e = self.entries[canonical_norm]
        if norm(value) == canonical_norm:
            e["sources"].append(self.src(file, path, n, kind))
            return e
        for s in e["synonyms"]:
            if norm(s["value"]) == norm(value):
                s["sources"].append(self.src(file, path, n, kind))
                return e
        e["synonyms"].append({"value": value, "link": link, "sources": [self.src(file, path, n, kind)]})
        return e

    def add_definition(self, canonical_norm, text, file, path):
        e = self.entries[canonical_norm]
        e["definition"] = {"text": text, "source": self.src(file, path, 1)}

    def add_candidate(self, value, file, path, n=1, note=""):
        self.candidates.append({"value": value, "sources": [self.src(file, path, n)], "status": "unresolved", "note": note})

    def find(self, value):
        k = norm(value)
        if k in self.entries:
            return self.entries[k]
        for e in self.entries.values():
            for s in e["synonyms"]:
                if norm(s["value"]) == k:
                    return e
        return None

    def to_json(self):
        return {"name": self.name, "label": self.label, "note": self.note,
                "canonical_count": len(self.entries),
                "synonym_count": sum(len(e["synonyms"]) for e in self.entries.values()),
                "candidate_count": len(self.candidates),
                "entries": list(self.entries.values()), "candidates": self.candidates}


def simple_enum(name, label, sources, note="", definitions=None, synonyms=None):
    """sources: [(file, path)] 값 사전. definitions: [(norm_value, file, path)] 정의문 경로 (잎 이름이 값)."""
    d = Dict_(name, label, note)
    for f, p in sources:
        for v, n in distinct_at(f, p).items():
            d.add_canonical(v, f, p, n)
    for f, p in (definitions or []):
        leaf = p.rsplit(".", 1)[-1]
        txt = [v for v, _ in values_at(f, p)]
        if norm(leaf) not in d.entries:
            d.add_canonical(leaf, f, p, 1, kind="key")
        d.add_definition(norm(leaf), txt[0] if txt else None, f, p)
    for canon, syn, f, p, link in (synonyms or []):
        d.add_synonym(norm(canon), syn, f, p, 1, link=link, kind="value" if link != "key" else "key")
    return d


def key_enum(name, label, keyed_sources, note="", synonyms=None, definitions=None):
    """값이 키 이름인 사전. keyed_sources: [(file, leaf_path, key_value)]"""
    d = Dict_(name, label, note)
    for f, p, k in keyed_sources:
        n = sum(1 for _ in values_at(f, p))
        d.add_canonical(k, f, p, n, kind="key")
    for canon, syn, f, p in (synonyms or []):
        d.add_synonym(norm(canon), syn, f, p, sum(1 for _ in values_at(f, p)), link="key-normalization", kind="key")
    for f, p in (definitions or []):
        leaf = p.rsplit(".", 1)[-1]
        txt = [v for v, _ in values_at(f, p)]
        if norm(leaf) not in d.entries:
            d.add_canonical(leaf, f, p, 1, kind="key")
        d.add_definition(norm(leaf), txt[0] if txt else None, f, p)
    return d


def build_dictionaries():
    tx = L["taxonomy.json"]
    # --- modality
    d = Dict_("modality", "계열", "정준값 = taxonomy modality[].category. 동의어는 원장에 코드 연결(같은 레코드의 id/코드 키)이 있는 이름 키만 자동 등록 (질문 1)")
    for m in tx["modality"]:
        e = d.add_canonical(m["category"], "taxonomy.json", "modality[].category", 1, code=m["id"], name_en=m["category_en"], group=m["group"])
        d.add_synonym(norm(m["category"]), m["id"], "taxonomy.json", "modality[].id", 1, link="code")
        d.add_synonym(norm(m["category"]), m["category_en"], "taxonomy.json", "modality[].category_en", 1, link="id-join")
    code2norm = {m["id"]: norm(m["category"]) for m in tx["modality"]}
    joins = [
        ("complications.json", "categories[].name", "id"), ("consent-checklist.json", "categories[].name", "id"),
        ("contraindications.json", "rules[].from_name", "from"), ("contraindications.json", "rules[].to_name", "to"),
        ("market-pricing.json", "categories[].name", "id"), ("patient-education.json", "categories[].name", "id"),
        ("patient-education.json", "categories[].patient_name", "id"), ("pre-procedure-checklist.json", "category_specific[].name", "id"),
        ("procedure-profiles.json", "profiles[].name", "id"), ("procedure-profiles.json", "profiles[].name_en", "id"),
    ]
    for f, p, jk in joins:
        cnt = Counter()
        for v, ctx in values_at(f, p):
            cnt[(ctx["record"][jk], v)] += 1
        for (code, v), n in cnt.items():
            d.add_synonym(code2norm[code], v, f, p, n)
    for f, p in [("extracted.json", "{code}.name"), ("extracted.json", "{code}.name_en"), ("extracted.json", "{code}.procedure_id"), ("literature-evidence.json", "categories.{code}.name")]:
        for v, ctx in values_at(f, p):
            d.add_synonym(code2norm[ctx["codes"][-1]], v, f, p, 1, link="code-key")
    for sec, body in L["products.json"].items():
        if isinstance(body, dict) and isinstance(body.get("category_id"), str):
            d.add_synonym(code2norm[body["category_id"]], sec, "products.json", f"{sec}.category_id", 1, link="section-key", kind="key")
    for t in L["post-procedure-timeline.json"]["timelines"]:
        code = t["category"].split("-")[0]
        if d.find(t["name"]) is not None and norm(t["name"]) in d.entries:
            d.add_synonym(code2norm[code], t["id"], "post-procedure-timeline.json", "timelines[].id", 1, link="id-join(name==계열명)")
            d.add_synonym(code2norm[code], t["name"], "post-procedure-timeline.json", "timelines[].name", 1)
        else:
            d.add_candidate(t["id"], "post-procedure-timeline.json", "timelines[].id", 1, f"name `{t['name']}` 이 계열명과 정규화 불일치 → alias 아님(R15.source_label 보조)")
    # 리포트 §3.4 에서 보이는 '시술 종류' 층 이름은 후보로만 (질문 10)
    for v, ctx in values_at("problem-packages.json", "problems[].complaints[].procedures[].name"):
        pass

    # --- problem
    d = Dict_("problem", "고민", "정준값 = taxonomy problem[].category (질문 12). 코드 연결 동의어만 자동, 다른 분류는 후보")
    p2n = {}
    for p in tx["problem"]:
        d.add_canonical(p["category"], "taxonomy.json", "problem[].category", 1, code=p["id"], name_en=p["category_en"])
        d.add_synonym(norm(p["category"]), p["id"], "taxonomy.json", "problem[].id", 1, link="code")
        d.add_synonym(norm(p["category"]), p["category_en"], "taxonomy.json", "problem[].category_en", 1)
        p2n[p["id"]] = norm(p["category"])
    for f, p, jk in [("problem-packages.json", "problems[].problem", "problem_id"), ("problem-combos.json", "combos[].problem", "problem_id")]:
        for v, ctx in values_at(f, p):
            d.add_synonym(p2n[ctx["record"][jk]], v, f, p, 1)
    for f, p in [("treatment-optimization.json", "by_concern[].concern"), ("treatment-optimization.json", "by_concern[].concern_en"),
                 ("procedure-comparison.json", "comparisons[].id"), ("procedure-comparison.json", "comparisons[].title")]:
        for v, n in distinct_at(f, p).items():
            if d.find(v) is not None:
                e = d.find(v)
                d.add_synonym(norm(e["canonical"]), v, f, p, n, link="exact")
            else:
                d.add_candidate(v, f, p, n, "고민 사전 정규화 불일치 — 사람 결정 필요")

    # --- site
    d = Dict_("site", "부위", "뼈대 = anatomy 11 zone (is_backbone). taxonomy problem 하위분류 라벨 + cc_group 52 는 정규화 일치면 동의어, 아니면 확장 정준값(is_backbone=false) (질문 24 · 재검토 §8-2)")
    for z in L["anatomy-danger-zones.json"]["zones"]:
        d.add_canonical(z["name_ko"], "anatomy-danger-zones.json", "zones[].name_ko", 1, is_backbone=True, zone_id=z["id"], name_en=z["name_en"])
        d.add_synonym(norm(z["name_ko"]), z["id"], "anatomy-danger-zones.json", "zones[].id", 1, link="id-join")
        d.add_synonym(norm(z["name_ko"]), z["name_en"], "anatomy-danger-zones.json", "zones[].name_en", 1, link="id-join")
    for f, p in [("taxonomy.json", "problem[].subcategories[].label"), ("problem-packages.json", "problems[].complaints[].cc_group")]:
        for v, n in distinct_at(f, p).items():
            e = d.find(v)
            if e is not None:
                d.add_synonym(norm(e["canonical"]), v, f, p, n, link="exact")
            else:
                d.add_canonical(v, f, p, n, is_backbone=False)

    # --- technique
    d = Dict_("technique", "기법", "출처 4곳의 distinct 값. 정규화 일치만 병합. taxonomy 하위분류 label 중 분류축 값은 재검토 §8-4")
    for f, p in [("procedure-profiles.json", "profiles[].mechanism[]"), ("products.json", "energy_device.products[].type"),
                 ("pih-risk.json", "procedures[].subcategory"), ("taxonomy.json", "modality[].subcategories[].label")]:
        for v, n in distinct_at(f, p).items():
            e = d.find(v)
            if e is None:
                d.add_canonical(v, f, p, n)
            else:
                d.add_synonym(norm(e["canonical"]), v, f, p, n, link="exact")
    for e in d.entries.values():
        e["only_in_taxonomy_subcategory"] = all(s["file"] == "taxonomy.json" for s in e["sources"]) and not e["synonyms"]

    # --- 단순 열거 사전들
    simple_enum("severity", "부작용 등급", [("complications.json", "categories[].complications[].severity")],
                definitions=[("complications.json", f"severity_levels.{k}") for k in ["mild", "moderate", "severe", "critical"]])
    key_enum("reaction_level", "시술 후 반응 등급(timeline)", [("post-procedure-timeline.json", f"timelines[].phases[].{k}[]", k) for k in ["normal", "abnormal", "caution", "emergency"]],
             definitions=[("post-procedure-timeline.json", f"reaction_levels.{k}") for k in ["normal", "abnormal", "caution", "emergency"]])
    simple_enum("pih_risk_level", "PIH 위험도", [("pih-risk.json", "procedures[].pih_risk"), ("procedure-comparison.json", "comparisons[].procedures[].pih_risk")],
                note="`none` 은 procedure-comparison 에만, `very_high` 는 pih-risk 에만 — 합집합. 재검토 §8-7",
                definitions=[("pih-risk.json", f"risk_levels.{k}") for k in ["very_low", "low", "moderate", "high", "very_high"]])
    simple_enum("interaction_level", "시술 쌍 규칙 등급", [("contraindications.json", "rules[].level")])
    d = key_enum("condition_level", "사람 조건 등급(금기·확인)",
                 [("extracted.json", "{code}.contraindications.absolute[]", "absolute"), ("extracted.json", "{code}.contraindications.relative[]", "relative"),
                  ("consent-checklist.json", "categories[].contraindications[]", "contraindication"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.contraindications[]", "contraindication")],
                 note="키 이름(absolute/relative/contraindication) + pre-procedure type 값. absolute_contraindication→absolute, relative_contraindication→relative 는 동의 정규화(③)")
    for f, p in [("pre-procedure-checklist.json", "universal_checks[].type"), ("pre-procedure-checklist.json", "category_specific[].checks[].type")]:
        for v, n in distinct_at(f, p).items():
            if v == "absolute_contraindication":
                d.add_synonym(norm("absolute"), v, f, p, n, link="③ 동의 정규화")
            elif v == "relative_contraindication":
                d.add_synonym(norm("relative"), v, f, p, n, link="③ 동의 정규화")
            else:
                d.add_canonical(v, f, p, n)
    simple_enum("synergy_type", "시너지 종류", [("synergy.json", "links[].type")], note="R18.kind 매핑: 함께→synergy_together, 다음에→synergy_after, 대신→synergy_instead")
    d = Dict_("package_tier", "패키지 등급", "problem-combos tier↔tierLabel 은 같은 레코드 쌍 → 동의어. combo-recipes intensity 는 정규화 일치만 병합")
    pairs = Counter()
    for v, ctx in values_at("problem-combos.json", "combos[].packages[].tier"):
        pairs[(v, ctx["record"]["tierLabel"])] += 1
    for (t, lab), n in pairs.items():
        d.add_canonical(t, "problem-combos.json", "combos[].packages[].tier", n)
        d.add_synonym(norm(t), lab, "problem-combos.json", "combos[].packages[].tierLabel", n, link="record-pair")
    for v, n in distinct_at("combo-recipes.json", "recipes[].intensity").items():
        e = d.find(v)
        if e:
            d.add_synonym(norm(e["canonical"]), v, "combo-recipes.json", "recipes[].intensity", n, link="exact")
        else:
            d.add_canonical(v, "combo-recipes.json", "recipes[].intensity", n)
    simple_enum("product_tier", "제품 등급(국산/수입)", [("problem-combos.json", "combos[].packages[].productTier")], note="7 표면형 전부 정준값. 병합은 사람 결정 (재검토 §8-6)")
    d = simple_enum("unit", "단위", [("market-pricing.json", "categories[].items[].unit"), ("market-pricing.json", "currency")], note="값 단위 17 + 통화 + 키 이름에서 오는 단위(day/month/week/mm/ml/cm/percent)")
    for f, p, k in [("treatment-sequence.json", "minimum_intervals[].min_days", "day"), ("treatment-sequence.json", "minimum_intervals[].min_months", "month"),
                    ("combo-recipes.json", "recipes[].followUp[].week", "week"), ("treatment-optimization.json", "annual_plans[].schedule[].month", "month"),
                    ("anatomy-danger-zones.json", "zones[].vessels[].depth_mm", "mm"), ("anatomy-danger-zones.json", "zones[].filler_specific.max_per_point_ml", "ml"),
                    ("anatomy-danger-zones.json", "zones[].botox_specific.diffusion_range_cm", "cm"), ("anatomy-danger-zones.json", "zones[].tissue_data.within_5mm_percent", "percent"),
                    ("procedure-profiles.json", "profiles[].prepTime", "minute"), ("procedure-profiles.json", "profiles[].durationMin", "minute")]:
        d.add_canonical(k, f, p, sum(1 for _ in values_at(f, p)), kind="key")
    simple_enum("period", "시술 후 시기 구간", [("post-procedure-timeline.json", "timelines[].phases[].period")])
    simple_enum("phase_label", "시술 후 시기 라벨", [("post-procedure-timeline.json", "timelines[].phases[].label")])
    simple_enum("evidence_level", "근거 수준", [("treatment-optimization.json", "by_concern[].severity_levels[].evidence_level")])
    simple_enum("rule_priority", "규칙 우선도", [("treatment-optimization.json", "combination_rules[].priority")])
    simple_enum("consensus", "합의 표시", [("treatment-optimization.json", "combination_rules[].consensus")])
    d = Dict_("accuracy_rubric", "문헌 정확도 점수 구간", "literature accuracy_summary.rubric 문자열에서 구간 분해(③)")
    rub = L["literature-evidence.json"]["accuracy_summary"]["rubric"]
    for lo, hi, lab in re.findall(r"(\d+)-(\d+)=([^,]+)", rub):
        d.add_canonical(f"{lo}-{hi}", "literature-evidence.json", "accuracy_summary.rubric", 1, kind="derived", label=lab.strip())
    simple_enum("anesthesia", "마취", [("procedure-profiles.json", "profiles[].needsAnesthesia")])
    simple_enum("position", "체위", [("procedure-profiles.json", "profiles[].position")])
    simple_enum("floor_phase", "플로어 단계", [("procedure-profiles.json", "profiles[].phase")])
    simple_enum("session_phase", "동일 세션 순서 단계", [("treatment-sequence.json", "sequence_order[].phase")])
    simple_enum("modality_group", "계열 묶음", [("taxonomy.json", "modality[].group")])
    simple_enum("source_type", "extracted 출처 유형", [("extracted.json", "{code}.source_type")])
    simple_enum("nerve_type", "신경 종류", [("anatomy-danger-zones.json", "zones[].nerves[].type")])
    d = Dict_("danger_level", "부위 위험 등급", "정수 level 과 color 는 zone 마다 1:1 쌍 → color 를 동의어로. filler_specific.risk_level 도 같은 값")
    pairs = Counter()
    for v, ctx in values_at("anatomy-danger-zones.json", "zones[].danger_level"):
        pairs[(str(v), ctx["record"]["danger_color"])] += 1
    for (lv, col), n in pairs.items():
        d.add_canonical(lv, "anatomy-danger-zones.json", "zones[].danger_level", n)
        d.add_synonym(norm(lv), col, "anatomy-danger-zones.json", "zones[].danger_color", n, link="record-pair")
    for v, n in distinct_at("anatomy-danger-zones.json", "zones[].filler_specific.risk_level").items():
        d.add_canonical(str(v), "anatomy-danger-zones.json", "zones[].filler_specific.risk_level", n)
    simple_enum("purpose_label", "목적 라벨", [("combo-recipes.json", "recipes[].goal"), ("synergy.json", "links[].target"), ("treatment-optimization.json", "by_concern[].icon"), ("procedure-comparison.json", "comparisons[].id")],
                note="영/한 슬러그 혼재. 고민 사전과는 정규화 일치만 (질문 12). 비슷한 값(안티에이징/안티에이징 패키지 등)은 ⑦ 후보")
    d = simple_enum("country", "제조국", [("products.json", f"{s}.products[].country") for s in ["botulinum_toxin", "filler_ha", "biostimulator", "skin_booster", "thread_lift", "energy_device", "prp_exosome", "stem_cell"]] + [("taxonomy.json", "modality[].products[].country")],
                    note="`-` 자리표시자는 null 로 (질문 18) — 정준값 아님")
    d.entries.pop(norm("-"), None)
    d.add_candidate("-", "products.json", "skin_booster.products[].country", 1, "자리표시자 → null")
    simple_enum("manufacturer", "제조사", [("products.json", f"{s}.products[].manufacturer") for s in ["botulinum_toxin", "filler_ha", "biostimulator", "skin_booster", "thread_lift", "energy_device", "prp_exosome", "stem_cell"]] + [("taxonomy.json", "modality[].products[].manufacturer")],
                note="`클래시스`/`클래시스(Classys)` 는 병합하지 않음(⑦). `-` 는 null")
    DICTS["manufacturer"].entries.pop(norm("-"), None)
    DICTS["manufacturer"].add_candidate("-", "products.json", "skin_booster.products[].manufacturer", 1, "자리표시자 → null")
    simple_enum("ingredient_material", "성분·재질", [("products.json", "biostimulator.products[].ingredient"), ("products.json", "skin_booster.products[].ingredient"), ("products.json", "thread_lift.products[].material"), ("taxonomy.json", "modality[].products[].ingredient"), ("taxonomy.json", "modality[].products[].material")])
    simple_enum("product_type", "제품 유형", [("products.json", "energy_device.products[].type"), ("products.json", "prp_exosome.products[].type"), ("products.json", "stem_cell.products[].type"), ("taxonomy.json", "modality[].products[].type")])
    simple_enum("age_group", "연령대", [("treatment-optimization.json", "by_age_group[].age"), ("treatment-optimization.json", "annual_plans[].age_group")], note="`40대+` 와 `40대`·`50대+` 는 입도가 다름 — 병합 안 함 (재검토 §8-12)")
    d = Dict_("concern_severity", "고민 중증도", "`경미 (fine lines)` 합성값에서 괄호 앞을 정준값으로(③). 괄호 안은 R13.severity_detail")
    for v, n in distinct_at("treatment-optimization.json", "by_concern[].severity_levels[].level").items():
        head = v.split(" (")[0].strip()
        d.add_canonical(head, "treatment-optimization.json", "by_concern[].severity_levels[].level", n, kind="derived")
        d.add_synonym(norm(head), v, "treatment-optimization.json", "by_concern[].severity_levels[].level", n, link="③ 합성값 분해")
    simple_enum("pain_scale", "통증 별점", [("procedure-comparison.json", "comparisons[].procedures[].pain")])
    key_enum("frequency_class", "부작용 빈도 분류(키 이름)",
             [("extracted.json", "{code}.safety.common[]", "common"), ("extracted.json", "{code}.safety.uncommon[]", "uncommon"), ("extracted.json", "{code}.safety.serious[]", "serious"),
              ("extracted.json", "{code}.safety.emergency[]", "emergency"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.long_term[]", "long_term"),
              ("consent-checklist.json", "categories[].emergency_signs[]", "emergency")],
             synonyms=[("common", "common_adverse_effects", "taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]"),
                       ("serious", "serious_adverse_effects", "taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]"),
                       ("common", "common_side_effects", "taxonomy.json", "modality[].products[].extracted.safety.common_side_effects[]")],
             note="동의 키 정규화 (질문 20)")
    return DICTS


# ---------------------------------------------------------------------------
# 참조 해결 (§9 미해결 목록 · 충돌 예상)
# ---------------------------------------------------------------------------
class Index:
    def __init__(self):
        tx = L["taxonomy.json"]
        self.idx = defaultdict(list)  # norm -> [(type, code/modality, display)]
        dm = DICTS["modality"]
        for e in dm.entries.values():
            self.idx[norm(e["canonical"])].append(("modality", e["code"], e["canonical"]))
            for s in e["synonyms"]:
                self.idx[norm(s["value"])].append(("modality", e["code"], e["canonical"]))
        self.sub_ids, self.item_ids, self.mod_ids = set(), set(), set()
        for m in tx["modality"]:
            self.mod_ids.add(m["id"])
            for sc in m["subcategories"]:
                self.sub_ids.add(sc["id"])
                self.idx[norm(sc["label"])].append(("subcategory", m["id"], sc["label"]))
                for it in sc["items"]:
                    self.item_ids.add(it["id"])
                    self.idx[norm(it["name"])].append(("procedure", m["id"], it["name"]))
            for pr in m["products"]:
                self.idx[norm(pr["name"])].append(("product", m["id"], pr["name"]))
        for sec, body in L["products.json"].items():
            if isinstance(body, dict):
                cid = body["category_id"]
                for pr in body["products"]:
                    cands = [c for c in self.idx[norm(pr["name"])] if c[0] == "product"]
                    if not cands:
                        self.idx[norm(pr["name"])].append(("product", cid if isinstance(cid, str) else "|".join(cid), pr["name"]))

    def resolve(self, label, hint=None, types=None):
        k = norm(label)
        cands = self.idx.get(k, [])
        if types:
            cands = [c for c in cands if c[0] in types]
        if hint:
            cands2 = [c for c in cands if c[1] == hint or (c[0] == "product" and hint in c[1].split("|"))]
            cands = cands2
        if not cands:
            return None, "unresolved"
        typesf = {c[0] for c in cands}
        tag = "resolved"
        # 깊이 우선순위: 계열명과 일치 → modality · 그다음 procedure(항목) · subcategory · product
        if "modality" in typesf and len(typesf) > 1:
            cands = [c for c in cands if c[0] == "modality"]
            tag = "resolved(계열명 일치→modality)"
        elif "procedure" in typesf and len(typesf) > 1:
            others = typesf - {"procedure"}
            cands = [c for c in cands if c[0] == "procedure"]
            tag = f"resolved(item+{'/'.join(sorted(others))} 겹침→procedure)"
        elif "subcategory" in typesf and "product" in typesf:
            cands = [c for c in cands if c[0] == "subcategory"]
            tag = "resolved(subcategory+product 겹침→subcategory)"
        mods = {c[1] for c in cands}
        if len(cands) > 1 and len(mods) > 1:
            return None, f"ambiguous({len(cands)}: " + ", ".join(sorted(mods)) + ")"
        return cands[0], tag


def resolution_report(IDX):
    R = OrderedDict()

    def run(name, items, note=""):
        """items: [(label, hint, types)]"""
        rows = []
        seen_lh = set()
        for label, hint, types in items:
            if (label, hint) in seen_lh:
                continue
            seen_lh.add((label, hint))
            c, tag = IDX.resolve(label, hint, types)
            rows.append({"label": label, "hint": hint, "result": tag, "target": (f"{c[0]}:{c[1]}:{c[2]}" if c else None)})
        n = len(rows)
        res = sum(1 for r in rows if r["result"].startswith("resolved"))
        unres = [r for r in rows if not r["result"].startswith("resolved")]
        byd = Counter(r["target"].split(":")[0] for r in rows if r["target"])
        R[name] = {"note": note, "n": n, "resolved": res, "unresolved": len(unres), "by_depth": dict(byd),
                   "unresolved_labels": sorted({(r["label"], r["hint"], r["result"]) for r in unres}, key=lambda x: (str(x[0]), str(x[1]))), "rows": rows}

    def split_code(s):
        m = MCODE_RE.match(s)
        return (m.group(1), m.group(2)) if m else (None, s)

    # synergy nodes
    nodes = Counter()
    for l in L["synergy.json"]["links"]:
        nodes[l["from"]] += 1
        nodes[l["to"]] += 1
    items = []
    for nd in nodes:
        code, lab = split_code(nd)
        items.append((lab, code, None))
    run("synergy.links[].from/to (노드 52)", items, "코드로 계열 확정 후 이름을 같은 계열 안에서 해결")
    # problem-packages procedures[].name
    pp = L["problem-packages.json"]
    seen = {}
    for p in pp["problems"]:
        for c in p["complaints"]:
            for pr in c["procedures"]:
                seen[(pr["name"], pr["category"])] = 1
    run("problem-packages.procedures[].name (시술 종류 29)", [(n, h, None) for n, h in seen], "질문 10")
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for cb in c["combos"] for x in cb["combo"])
    run("problem-packages.combos[].combo[] (멤버 29)", [(n, None, None) for n in seen], "힌트 없음")
    seen = Counter(x for p in pp["problems"] for c in p["complaints"] for pr in c["procedures"] for x in pr["products"])
    run("problem-packages.procedures[].products[] (제품 34)", [(n, None, ("product",)) for n in seen], "제품 사전만")
    pc = L["procedure-comparison.json"]
    run("procedure-comparison.procedures[].name (39)", [(pr["name"], pr["category"], None) for c in pc["comparisons"] for pr in c["procedures"]], "질문 11")
    to = L["treatment-optimization.json"]
    seen = Counter(x for c in to["by_concern"] for s in c["severity_levels"] for x in s["optimal_combo"])
    run("treatment-optimization.optimal_combo[] (57)", [(n, None, None) for n in seen])
    seen = Counter(x for g in to["by_age_group"] for k in ["recommended_base", "avoid", "upgrade"] for x in g.get(k, []))
    run("treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", [(n, None, None) for n in seen])
    seen = Counter(x for pl in to["annual_plans"] for s in pl["schedule"] for x in s["procedures"])
    run("treatment-optimization.annual_plans.schedule[].procedures[] (29)", [(n, None, None) for n in seen], "`토닝 4회` 횟수 섞임")
    ts = L["treatment-sequence.json"]
    items = []
    for s in ts["sequence_order"]:
        for c in s["categories"]:
            code, lab = split_code(c)
            if code and lab is None:
                items.append((DICTS["modality"].find(code)["canonical"], code, ("modality",)))
            elif code and c in IDX.sub_ids:
                items.append((c, code, None))  # 실존 하위분류 id
            else:
                items.append((lab if lab else c, code, None))
    run("treatment-sequence.sequence_order[].categories[] (19)", items, "질문 7: 실존 하위분류 id 는 id 로, 코드만은 계열로, 코드+라벨은 라벨을 계열 안에서")
    # 실존 id 를 라벨로 넣은 항목 보정
    for r in R["treatment-sequence.sequence_order[].categories[] (19)"]["rows"]:
        if r["label"] in IDX.sub_ids:
            r["result"] = "resolved(subcategory id)"
            r["target"] = f"subcategory:{r['hint']}:{r['label']}"
    rr = R["treatment-sequence.sequence_order[].categories[] (19)"]
    rr["resolved"] = sum(1 for r in rr["rows"] if r["result"].startswith("resolved"))
    rr["unresolved"] = rr["n"] - rr["resolved"]
    rr["unresolved_labels"] = sorted({(r["label"], r["hint"], r["result"]) for r in rr["rows"] if not r["result"].startswith("resolved")}, key=lambda x: (str(x[0]), str(x[1])))
    rr["by_depth"] = dict(Counter(r["target"].split(":")[0] for r in rr["rows"] if r["target"]))
    run("treatment-sequence.incompatible_same_day[].pair[] (14 distinct)", [(x, None, None) for p in ts["incompatible_same_day"] for x in p["pair"]])
    run("treatment-sequence.minimum_intervals from/to (14 distinct)", [(x, None, None) for m in ts["minimum_intervals"] for x in (m["from"], m["to"])])
    run("treatment-sequence.common_combos[].sequence[] (22 distinct)", [(x, None, None) for c in ts["common_combos"] for x in c["sequence"]])
    ppt = L["post-procedure-timeline.json"]
    items = []
    for t in ppt["timelines"]:
        code, lab = split_code(t["category"])
        items.append((t["name"], code, None))
    run("post-procedure-timeline.timelines[].name (10)", items, "category 계열에는 항상 붙고, 이름은 더 구체 대상 시도")
    mp = L["market-pricing.json"]
    run("market-pricing.items[].name (122)", [(i["name"], c["id"], None) for c in mp["categories"] for i in c["items"]], "질문 11")
    # pih ref
    rows = []
    for p in L["pih-risk.json"]["procedures"]:
        ref = p["procedure_ref"]
        depth = "procedure" if ref in IDX.item_ids else "subcategory" if ref in IDX.sub_ids else "modality" if ref in IDX.mod_ids else "broken"
        rows.append({"label": p["name"], "hint": ref, "result": "resolved" if depth != "broken" else "unresolved", "target": f"{depth}:{ref}"})
    R["pih-risk.procedure_ref (26)"] = {"note": "질문 5 깊이", "n": len(rows), "resolved": sum(r["result"] == "resolved" for r in rows), "unresolved": sum(r["result"] != "resolved" for r in rows),
                                        "by_depth": dict(Counter(r["target"].split(":")[0] for r in rows)), "unresolved_labels": [], "rows": rows}
    # R13 problem labels
    dp = DICTS["problem"]
    rows = []
    for c in to["by_concern"]:
        e = dp.find(c["concern"])
        rows.append({"label": c["concern"], "hint": None, "result": "resolved" if e else "unresolved", "target": f"problem:{e['code']}:{e['canonical']}" if e else None})
    for c in pc["comparisons"]:
        e = dp.find(c["id"]) or dp.find(c["title"])
        rows.append({"label": f"{c['id']} / {c['title']}", "hint": None, "result": "resolved" if e else "unresolved", "target": f"problem:{e['code']}:{e['canonical']}" if e else None})
    for g in to["by_age_group"]:
        for x in g["primary_concerns"]:
            e = dp.find(x)
            rows.append({"label": x, "hint": g["age"], "result": "resolved" if e else "unresolved", "target": f"problem:{e['code']}:{e['canonical']}" if e else None})
    R["고민 사전 일치 (concern 8 · comparison 9 · primary_concerns 17)"] = {"note": "질문 12", "n": len(rows), "resolved": sum(r["result"] == "resolved" for r in rows), "unresolved": sum(r["result"] != "resolved" for r in rows),
                                                                          "by_depth": dict(Counter(r["target"].split(":")[0] for r in rows if r["target"])), "unresolved_labels": sorted({(r["label"], r["hint"], r["result"]) for r in rows if r["result"] != "resolved"}, key=lambda x: (str(x[0]), str(x[1]))), "rows": rows}
    # site
    ds = DICTS["site"]
    bb = sum(1 for e in ds.entries.values() if e.get("is_backbone"))
    ext = [e["canonical"] for e in ds.entries.values() if not e.get("is_backbone")]
    R["부위 사전 (뼈대 11 + 확장)"] = {"note": "질문 24", "n": len(ds.entries), "resolved": bb, "unresolved": len(ext), "by_depth": {"backbone": bb, "extension": len(ext)}, "unresolved_labels": [(x, None, "extension") for x in ext], "rows": []}
    # canonical_category
    rows = []
    for m in L["taxonomy.json"]["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                if "canonical_category" in it:
                    lab = it["canonical_category"].split(">")[-1].strip()
                    code = it["canonical_category"].split()[0]
                    c, tag = IDX.resolve(lab, code, ("subcategory",))
                    rows.append({"label": it["canonical_category"], "hint": it["name"], "result": tag, "target": f"{c[0]}:{c[1]}:{c[2]}" if c else None})
    R["taxonomy canonical_category → 하위분류 (6)"] = {"note": "질문 23", "n": len(rows), "resolved": sum(r["result"].startswith("resolved") for r in rows), "unresolved": sum(not r["result"].startswith("resolved") for r in rows), "by_depth": {}, "unresolved_labels": sorted({(r["label"], r["hint"], r["result"]) for r in rows if not r["result"].startswith("resolved")}, key=lambda x: (str(x[0]), str(x[1]))), "rows": rows}
    return R


def conflict_estimates(IDX):
    tx = L["taxonomy.json"]
    E = []
    # Q2 extracted vs taxonomy
    ex = L["extracted.json"]
    diff = []
    for m in tx["modality"]:
        a, b = ex[m["id"]], m["extracted"]
        keys = ["overview", "mechanism", "indications", "contraindications", "safety", "onset_duration", "aftercare", "related_techniques"]
        dk = [k for k in keys if a.get(k) != b.get(k)]
        if dk:
            diff.append((m["id"], dk))
    E.append({"kind": "value_conflict", "what": "modality 본문 extracted.json vs taxonomy modality[].extracted (질문 2)", "n": len(diff), "detail": [f"{c}: {','.join(k)}" for c, k in diff]})
    # Q3 products
    pj = {}
    for sec, body in L["products.json"].items():
        if isinstance(body, dict):
            for pr in body["products"]:
                pj[norm(pr["name"])] = (sec, pr["name"])
    tp = {}
    for m in tx["modality"]:
        for pr in m["products"]:
            tp[norm(pr["name"])] = (m["id"], pr["name"])
    only_p = [v[1] for k, v in pj.items() if k not in tp]
    only_t = [v[1] for k, v in tp.items() if k not in pj]
    E.append({"kind": "value_conflict", "what": "제품 목록 products.json vs taxonomy products (질문 3: 티엠버스/타임버스 쌍 1 + 신펄 + 볼뉴머 = 3)", "n": 3, "detail": [f"products.json 에만: {only_p}", f"taxonomy 에만: {only_t}"]})
    # Q9 cc duplicates
    names = Counter((p["id"], it["name"]) for p in tx["problem"] for sc in p["subcategories"] for it in sc["items"])
    byname = Counter(it["name"] for p in tx["problem"] for sc in p["subcategories"] for it in sc["items"])
    dups6 = [f"{k}×{n}" for k, n in byname.items() if n > 1]
    dups2 = [f"{k[0]}:{k[1]}×{n}" for k, n in names.items() if n > 1]
    E.append({"kind": "value_conflict", "what": "주호소 이름 중복 — 발주서 기본값 9 (이름만으로 6)", "n": len(dups6), "detail": dups6 + [f"(problem_id, 이름) 결합이면 남는 중복 {len(dups2)}: {dups2} — 재검토 §8-18"]})
    # cc_group mismatch (중복 이름 포함: 같은 (pid, cc) 의 taxonomy label 집합과 비교)
    labmap = defaultdict(set)
    for p in tx["problem"]:
        for sc in p["subcategories"]:
            for it in sc["items"]:
                labmap[(p["id"], it["name"])].add(sc["label"])
    mm = []
    for p in L["problem-packages.json"]["problems"]:
        for c in p["complaints"]:
            labs = labmap.get((p["problem_id"], c["cc"]))
            if labs and c["cc_group"] not in labs:
                mm.append(f"{p['problem_id']} {c['cc']}: packages `{c['cc_group']}` vs taxonomy {sorted(labs)}")
    E.append({"kind": "value_conflict", "what": "cc_group ≠ taxonomy 하위분류 label", "n": len(mm), "detail": mm})
    # pih name vs item name
    itname = {it["id"]: it["name"] for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"]}
    pm, pm_hard = [], []
    strip = lambda x: norm(re.sub(r"\s*\([^)]*\)", "", x))
    for p in L["pih-risk.json"]["procedures"]:
        if p["procedure_ref"] in itname and norm(itname[p["procedure_ref"]]) != norm(p["name"]):
            t = f"{p['procedure_ref']}: pih `{p['name']}` vs taxonomy `{itname[p['procedure_ref']]}`"
            (pm_hard if strip(p["name"]) != strip(itname[p["procedure_ref"]]) else pm).append(t)
    E.append({"kind": "value_conflict", "what": "pih procedure_ref 가 가리키는 항목의 이름과 괄호를 벗겨도 다른 행 (같은 id 에 다른 이름)", "n": len(pm_hard), "detail": pm_hard})
    E.append({"kind": "duplicate_candidate", "what": "pih name 이 항목명과 괄호 보충만 다른 행 (source_label 로 보존, ⑦ 참고)", "n": len(pm), "detail": pm})
    # item name duplicates
    itn = Counter(norm(it["name"]) for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"])
    E.append({"kind": "duplicate_candidate", "what": "taxonomy 항목 이름 중복(계열 간)", "n": sum(1 for v in itn.values() if v > 1), "detail": [k for k, v in itn.items() if v > 1]})
    # surface variants (⑦)
    E.append({"kind": "duplicate_candidate", "what": "표면형 변형 묶음 (리포트 §3.10, 괄호·공백·영/한만 다른 것)", "n": len(SCAN["surface_variants"]), "detail": "리포트 §3.10 목록 그대로 ⑦ 후보"})
    E.append({"kind": "duplicate_candidate", "what": "procedure-profiles mechanism regenerative/regeneration · 제조사 클래시스/클래시스(Classys) · purpose_label 유사값(안티에이징/안티에이징 패키지 등 4쌍)", "n": 6, "detail": []})
    # adverse effect name variants
    E.append({"kind": "duplicate_candidate", "what": "complications 합병증 표기 변형(홍반 3 · 부종 2 · 화상 2 · 비대칭 2 · 감염 2 · 주사부위반응 2)", "n": 6, "detail": "리포트 §3.10"})
    # unregistered (⑧)
    E.append({"kind": "unregistered_value", "what": "사전 밖 값 — pih_risk `none`(comparison) 은 합집합으로 등록, `-` 자리표시자 2 → null", "n": 2, "detail": ["products.json skin_booster 스킨보톡스 manufacturer/country `-`"]})
    return E


def q14_bundles():
    tx = L["taxonomy.json"]
    empties = [(p["id"], sc["label"], it["name"]) for p in tx["problem"] for sc in p["subcategories"] for it in sc["items"] if not it["modality_ref"]]
    A = ["서브시전", "에어서브시전", "윤곽주사", "지방분해주사", "HPL", "BNLS", "브이올렛", "컷슬린", "두피메조"]
    B = ["반영구", "경구약", "FUE", "FUT", "미라드라이", "실리콘시트", "스테로이드주사", "경화요법", "엔더몰로지"]
    rows = []
    for pid, lab, name in empties:
        n = norm(name)
        a = [x for x in A if norm(x) in n]
        b = [x for x in B if norm(x) in n]
        bucket = "① 계열 매핑 후보" if a else "② 계열 없음 격리(범위 검토)" if b else "미배정(발주서 목록에 없음)"
        rows.append({"problem": pid, "subcategory": lab, "name": name, "bucket": bucket, "matched": (a or b)})
    return rows


# ---------------------------------------------------------------------------
# 문서 생성
# ---------------------------------------------------------------------------
def build_column_map():
    rows = []
    for f, v in SCAN["files"].items():
        for p, st in v["leaf_paths"].items():
            r = C.resolve(f, p)
            rows.append({"file": f, "path": p, "type": "/".join(st["types"].keys()), "count": st["count"], "dest": r[1], "target": r[2], "note": r[3]})
    return rows


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def mermaid():
    lines = ["erDiagram"]
    rels = [
        ("MODALITY", "MODALITY_SUBCATEGORY", "||--o{", "R1 has_subcategory"), ("MODALITY_SUBCATEGORY", "PROCEDURE", "||--o{", "R2 has_procedure"),
        ("PROCEDURE", "PRODUCT", "}o--o{", "R3 uses_product"), ("MODALITY", "PRODUCT", "||--o{", "R4 offers_product"),
        ("MODALITY", "TECHNIQUE", "}o--o{", "R5 applies_technique"), ("PROBLEM", "PROBLEM_SUBCATEGORY", "||--o{", "R6"),
        ("PROBLEM_SUBCATEGORY", "COMPLAINT", "||--o{", "R7 has_complaint"), ("COMPLAINT", "MODALITY", "}o--o{", "R8 addressed_by"),
        ("COMPLAINT", "PROCEDURE", "}o--o{", "R9 recommends"), ("COMPLAINT", "SITE", "}o--o|", "R10 located_at"),
        ("PROBLEM_SUBCATEGORY", "SITE", "}o--o|", "R11 subcategory_site"), ("PACKAGE", "PROCEDURE", "}o--o{", "R12 member"),
        ("PACKAGE", "PROBLEM", "}o--o{", "R13 for_problem"), ("COMPLAINT", "PACKAGE", "}o--o{", "R14 offers_combo"),
        ("PROCEDURE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"), ("SITE", "ADVERSE_EFFECT", "}o--o{", "R15 may_cause"),
        ("PROCEDURE", "PERSON_CONDITION", "}o--o{", "R16 contraindicated_for"), ("PERSON_CONDITION", "PROCEDURE", "}o--o{", "R17 age_group_guidance"),
        ("PROCEDURE", "PROCEDURE", "}o--o{", "R18 interaction"), ("EVIDENCE_STATEMENT", "CITATION", "}o--||", "R19 cites"),
        ("ADVERSE_EFFECT", "CITATION", "}o--o|", "R19 cites"), ("CLINICAL_RULE", "CITATION", "}o--o|", "R19 cites"),
        ("MODALITY", "EVIDENCE_STATEMENT", "||--o{", "R20 has_evidence"), ("SITE", "ANATOMICAL_STRUCTURE", "}o--o{", "R21 contains"),
        ("SITE", "MODALITY", "}o--o{", "R22 injection_guidance"), ("CONFLICT", "DECISION", "}o--o|", "R24 resolved_by"),
        ("SOURCE_FILE", "CONFLICT", "||--o{", "R25 provenance"),
    ]
    for a, b, c, lab in rels:
        lines.append(f"    {a} {c} {b} : \"{lab}\"")
    lines.append("    %% R9·R12·R15·R16·R18 의 시술 축 끝은 MODALITY|MODALITY_SUBCATEGORY|PROCEDURE|PRODUCT 중 하나(target_depth). R25 provenance 는 모든 개체에 닿는다")
    return "\n".join(lines)


def write_outputs(colrows, dicts, RES, CONF, Q14):
    # ---------------- erd-v1.json
    files_meta = []
    tiers = {f: (t, basis, note) for f, t, basis, note in S.SOURCE_FILES}
    for f in FILES:
        meta = {}
        if isinstance(L[f], dict):
            for k in ["version", "updated", "description", "consensus_method", "source_method", "currency", "note"]:
                if isinstance(L[f].get(k), str):
                    meta[k] = L[f][k]
        t, basis, note = tiers[f]
        files_meta.append({"file": f, "sha256": sha256(os.path.join(LEDGER, f)), "bytes": SCAN["files"][f]["bytes"], "snapshot_date": S.SNAPSHOT,
                           "trust_tier": t, "trust_basis": basis, "trust_note": note, "version": meta.get("version"), "updated": meta.get("updated"),
                           "method": meta.get("consensus_method") or meta.get("source_method"), "leaf_paths": SCAN["files"][f]["leaf_count"]})
    dest_counter = Counter(r["dest"] for r in colrows)
    ent_json = []
    for e in S.ENTITIES:
        ent_json.append({"key": e["key"], "prefix": e["prefix"], "label": e["label"], "definition": e["definition"], "identity": e["identity"],
                         "beyond_minimum": e.get("beyond_minimum", False), "aliases": e["aliases"],
                         "attrs": [{"name": a[0], "type": a[1], "required": a[2], "sources": a[3], "rule": a[4]} for a in e["attrs"]]})
    rel_json = []
    for r in S.RELATIONS:
        rel_json.append({**r, "attrs": [{"name": a[0], "type": a[1], "note": a[2]} for a in r["attrs"]]})
    erd = OrderedDict([
        ("erd_version", "v1"), ("status", "draft — 사용자 승인 전"), ("written", "2026-11-04"), ("bronze_snapshot", S.SNAPSHOT),
        ("layers", {"bronze": "원장 21 그대로, 바이트 보존, SHA256 식별", "semantic": "이 ERD + 값 사전, 승인이 정본 조건, 버전 개정", "silver": "ERD 를 따르는 정규화 레코드, 모든 값에 (file, path) 출처", "gold": "실버 조합 뷰, 새 사실 금지"}),
        ("normalize_rule", S.NORMALIZE_RULE), ("id_rule", S.ID_RULE),
        ("source_files", files_meta),
        ("entities", ent_json), ("relations", rel_json), ("enums", S.ERD_ENUMS),
        ("quality_rules", [{"no": a, "class": b, "rule": c} for a, b, c in S.QUALITY_RULES]),
        ("synonym_key_normalization", {"secondary": "extended", "peak_effect": "peak", "common_adverse_effects": "common", "common_side_effects": "common", "serious_adverse_effects": "serious", "absolute_contraindication": "absolute", "relative_contraindication": "relative", "M1_to_M7": "M1,M2,M3,M4,M5,M6,M7"}),
        ("q25", [{"no": n, "answer": a} for n, a in S.Q25]),
        ("review_items", REVIEW),
        ("q14_bundles", Q14),
        ("column_map_summary", {"leaf_paths": len(colrows), "by_dest": dict(dest_counter), "by_entity": dict(Counter(r["target"].split(".")[0] for r in colrows if r["dest"] == "개체")), "by_dict": dict(Counter(r["target"] for r in colrows if r["dest"] == "사전")), "by_relation": dict(Counter(r["target"].split(".")[0].split("(")[0] for r in colrows if r["dest"] == "엣지"))}),
        ("dictionaries_summary", [{"name": d.name, "label": d.label, "canonical": len(d.entries), "synonyms": sum(len(e["synonyms"]) for e in d.entries.values()), "candidates": len(d.candidates)} for d in dicts.values()]),
        ("resolution_report", {k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in RES.items()}),
        ("conflict_estimates", CONF),
    ])
    json.dump(erd, open(os.path.join(WORK, "erd-v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ---------------- dictionaries
    dj = OrderedDict([("erd_version", "v1"), ("bronze_snapshot", S.SNAPSHOT), ("normalize_rule", S.NORMALIZE_RULE["name"]),
                      ("source_kinds", {"value": "그 경로의 값 자체", "key": "그 경로의 키 이름(또는 섹션 키)이 값 — 단수/복수 차이 허용", "derived": "그 경로의 합성값에서 ③ 형식 교정으로 잘라낸 부분값(원문의 부분 문자열)"}),
                      ("dictionaries", [d.to_json() for d in dicts.values()])])
    json.dump(dj, open(os.path.join(WORK, "erd-v1-dictionaries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ---------------- column map md
    md = ["# ERD v1 — 원장 잎 키 573 행선지 표", "",
          f"작성 2026-11-04 · 입력 `bronze-ledger-column-scan.json`(잎 키 {len(colrows)}) · 행선지 범주 5: 개체(개체.속성) / 사전 / 엣지(엣지 속성) / 브론즈(브론즈 원문만) / 버림", "",
          "표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v1.md §3) · `bronze` · `drop`. 비고의 ①~⑤ 는 품질 규칙 번호, 「질문 N」은 §7 답.", "",
          "## 요약", "", md_table(["행선지", "잎 키 수"], sorted(dest_counter.items(), key=lambda x: -x[1]) + [("합계", len(colrows))]), ""]
    for f in FILES:
        rs = [r for r in colrows if r["file"] == f]
        md.append(f"## `{f}` — 잎 키 {len(rs)}")
        md.append("")
        md.append(md_table(["#", "경로", "타입", "횟수", "행선지", "표적", "비고"], [(i + 1, f"`{r['path']}`", r["type"], r["count"], r["dest"], f"`{r['target']}`", r["note"]) for i, r in enumerate(rs)]))
        md.append("")
    open(os.path.join(WORK, "erd-v1-column-map.md"), "w", encoding="utf-8").write("\n".join(md))
    return erd


def build_erd_md(erd, colrows, dicts, RES, CONF, Q14):
    o = []
    A = o.append
    A("# ERD v1 — 피부과 시술 허브 메달리온 시맨틱 정의")
    A("")
    A("작성 2026-11-04 · 상태 **초안(사용자 승인 전)** · 브론즈 스냅샷 2026-10-26 · 발주서 `erd-v1-brief.md`")
    A("")
    A("기계용 동본 `erd-v1.json` · 값 사전 `erd-v1-dictionaries.json` · 잎 키 행선지 `erd-v1-column-map.md` · 검산 `erd-v1-check.py` (결과 §10)")
    A("")
    A("## 1. 범위와 층")
    A("")
    A("| 층 | 무엇 | 규칙 |")
    A("|---|---|---|")
    A("| 브론즈 | 원장 21개 JSON 그대로 | 바이트 보존·수정 금지. 파일 SHA256 이 식별자(§6 표). 스냅샷 2026-10-26 |")
    A("| 시맨틱 | 이 ERD + 값 사전 | 문서. 사용자 승인이 정본 조건. 버전으로 개정(v1 → v2 …) |")
    A("| 실버 | ERD 를 따르는 정규화 레코드 | **모든 값은 (파일, 잎 키 경로) 출처를 가진다.** 출처 없는 값 금지. 충돌은 둘 다 보관 |")
    A("| 골드 | 실버 조합 뷰 | 실버에 없는 사실을 만들지 않는다. 충돌 미판정 레코드 제외 |")
    A("")
    A("지식은 원장 21개와 컬럼 리포트에서만 가져왔다. step*·source-map·DATA-001·DEC-*·silver-*·`_archive/` 는 열지 않았다.")
    A("")
    A("### 1.1 정규화(「같은 것」판정)와 식별자")
    A("")
    A(f"- 정규화 `{S.NORMALIZE_RULE['name']}`: " + " → ".join(S.NORMALIZE_RULE["steps"]))
    A(f"- {S.NORMALIZE_RULE['note']}")
    A(f"- 식별자: `{S.ID_RULE['format']}`. canonical_key 는 개체별(§2 각 표의 「식별자」). {S.ID_RULE['canonical_key']}")
    A("- 「같은 것」 = 정규화 완전 일치(①) + 사전 동의어(②)만 자동. 유사도·추측 매칭은 ⑦ 후보로만 남긴다.")
    A("")
    A("### 1.2 다이어그램 (개체·관계만)")
    A("")
    A("```mermaid")
    A(mermaid())
    A("```")
    A("")
    A("## 2. 개체 목록")
    A("")
    A(f"개체 {len(S.ENTITIES)}개. 발주서 최소 목록(제품·계열·부위·기법·단위 시술·고민·부작용·금기 조건·문헌 인용·충돌·결정) 11 + 추가 {sum(1 for e in S.ENTITIES if e.get('beyond_minimum'))}(표시 ★). 설명문·FAQ·가격·환자 교육문·고지문은 전부 속성이다.")
    A("")
    for e in S.ENTITIES:
        star = " ★" if e.get("beyond_minimum") else ""
        A(f"### 2.{S.ENTITIES.index(e)+1} `{e['key']}` — {e['label']}{star} (접두 `{e['prefix']}`)")
        A("")
        A(f"- 정의: {e['definition']}")
        A(f"- 식별자(canonical_key): {e['identity']}")
        A(f"- aliases: {e['aliases']}")
        A("")
        A(md_table(["속성", "타입", "필수", "출처 원장 키", "정규화·규칙"], [(a[0], a[1], "○" if a[2] else "", "<br>".join(f"`{s}`" for s in a[3]) if a[3] else "(파생/ERD 정의)", a[4]) for a in e["attrs"]]))
        A("")
    A("## 3. 관계 목록")
    A("")
    A(f"관계 {len(S.RELATIONS)}개. `proc_axis` = modality | modality_subcategory | procedure | product 중 하나(엣지 속성 `target_depth` 로 깊이 기록). 시너지·순서·간격·시술간 금기는 **R18 하나**의 `kind` 속성이다.")
    A("")
    for r in S.RELATIONS:
        A(f"### {r['id']} `{r['name']}` — {r['from']} → {r['to']} ({r['card']})")
        A("")
        if r["attrs"]:
            A(md_table(["엣지 속성", "타입", "비고"], [(a[0], a[1], a[2]) for a in r["attrs"]]))
            A("")
        A("- 출처: " + (", ".join(f"`{s}`" for s in r["sources"]) if r["sources"] else "(ERD 정의 · 실버 빌더 생성)"))
        if r["note"]:
            A(f"- 규칙: {r['note']}")
        A("")
    A("### 3.1 ERD 정의 열거형 (원장 출처 없음 — 값 사전과 구분)")
    A("")
    A(md_table(["열거형", "값"], [(k, ", ".join(v)) for k, v in S.ERD_ENUMS.items()]))
    A("")
    A("## 4. 값 사전 목록")
    A("")
    A("전부 `erd-v1-dictionaries.json`. 정준값·동의어마다 출처(파일·키·횟수·kind value/key)가 붙는다. 「후보」는 정준값에 자동 연결되지 않은 값(사람 결정 대기).")
    A("")
    A(md_table(["사전", "라벨", "정준값", "동의어", "후보", "출처 키"], [(d.name, d.label, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), len(d.candidates), ", ".join(sorted({f"`{s['file']}:{s['path']}`" for e in d.entries.values() for s in e["sources"]} | {f"`{s['file']}:{s['path']}`" for e in d.entries.values() for sy in e["synonyms"] for s in sy["sources"]})[:6]) + (" …" if len({(s['file'], s['path']) for e in d.entries.values() for s in e["sources"]}) > 6 else "")) for d in dicts.values()]))
    A("")
    A("사전 하나에 비고가 있는 것:")
    A("")
    for d in dicts.values():
        if d.note:
            A(f"- `{d.name}`: {d.note}")
    A("")
    A("## 5. 충돌·결정 개체 정의 + 규칙 ①~⑩ + 신뢰 순위")
    A("")
    A("충돌(`conflict`)·결정(`decision`) 개체 정의는 §2.18·§2.19. 충돌은 기계가 남기고(대상·값들·출처들·해결 규칙·상태), 결정은 사람이 남긴다(무엇을·왜·누가·언제·적용 대상). 원장은 고치지 않고 결정만 쌓는다.")
    A("")
    A(md_table(["#", "분류", "규칙"], S.QUALITY_RULES))
    A("")
    A("빈값과 「없음」: 안 적힌 것(키 없음·null·빈 배열·빈 문자열) = null(미입력). 명시적으로 없다고 적힌 것만 빈 목록. 단계 끝 = 컬럼 행선지 미정 0 · 충돌 미판정 0.")
    A("")
    A("### 5.1 원장 신뢰 순위 (파일별)")
    A("")
    A(md_table(["순위", "파일", "근거 키", "비고"], [(t, f"`{f}`", b, n) for f, t, b, n in sorted(S.SOURCE_FILES, key=lambda x: (x[1], x[0]))]))
    A("")
    A("`products.json` 의 `products[].mfds` 필드만 2(식약처 허가)로 격상한다. 4등급 파일 안의 「교과서」표현은 AI 합의 라벨이지 실제 교과서가 아니다. 순위가 같은 출처끼리 값이 다르면 ⑥ 충돌.")
    A("")
    A("## 6. 원장 파일 21 → 개체 매핑 요약")
    A("")
    rows = []
    for fm in erd["source_files"]:
        f = fm["file"]
        rs = [r for r in colrows if r["file"] == f]
        ents = Counter(r["target"].split(".")[0] for r in rs if r["dest"] == "개체" and not r["target"].startswith("source_file"))
        rels = Counter(r["target"].split(".")[0].split("(")[0] for r in rs if r["dest"] == "엣지")
        dcts = Counter(r["target"] for r in rs if r["dest"] == "사전")
        drops = [r["path"] for r in rs if r["dest"] in ("버림", "브론즈")]
        main = ", ".join(f"{k}({v})" for k, v in ents.most_common(3))
        sub = ", ".join(f"{k}({v})" for k, v in ents.most_common()[3:]) + ("; " if ents.most_common()[3:] and rels else "") + ", ".join(f"{k}({v})" for k, v in rels.most_common())
        rows.append((f"`{f}`", fm["trust_tier"], fm["sha256"][:12], fm["leaf_paths"], main or "—", sub or "—", ", ".join(k.replace("dict:", "") for k in dcts) or "—", f"{len(drops)}: " + ", ".join(f"`{d}`" for d in drops[:3]) + (" …" if len(drops) > 3 else "") if drops else "0"))
    A(md_table(["파일", "순위", "sha256(12)", "잎", "주 개체", "부 개체·엣지", "사전", "브론즈만/버림"], rows))
    A("")
    A("## 7. 질문 25 답")
    A("")
    A(md_table(["#", "답 (발주서 §6 기본값 적용)"], S.Q25))
    A("")
    A("## 8. 기본값 재검토")
    A("")
    A("기준·기본값에 없거나 원장과 맞지 않는 판단. 바꾸지 않고 사유만 적는다. 사용자 결정이 나면 결정 개체로 기록하고 v2 에 반영.")
    A("")
    for i, it in enumerate(REVIEW, 1):
        A(f"### 8-{i}. {it['title']}")
        A("")
        A(f"- 관련: {it['ref']}")
        A(f"- 원장 사실: {it['fact']}")
        A(f"- v1 에서 한 것(기본값대로): {it['applied']}")
        A(f"- 물을 것: {it['ask']}")
        A("")
    A("## 9. ERD 승인 때 사용자가 볼 것")
    A("")
    A("### 9.1 사전 표 (정준값 수 · 동의어 · 후보)")
    A("")
    A(md_table(["사전", "정준값", "동의어", "후보(미연결)"], [(d.name, len(d.entries), sum(len(e["synonyms"]) for e in d.entries.values()), "; ".join(c["value"] for c in d.candidates) or "—") for d in dicts.values()]))
    A("")
    A("핵심 사전 정준값 전체:")
    A("")
    for name in ["modality", "problem", "site", "technique"]:
        d = dicts[name]
        A(f"- `{name}` ({len(d.entries)}): " + " · ".join((e["canonical"] + (f"[{e['code']}]" if e.get("code") else "") + ("" if e.get("is_backbone", True) else "(확장)")) for e in d.entries.values()))
    A("")
    A("### 9.2 격리 목록 (자동 연결 실패 → ⑨ unresolved_reference 예상)")
    A("")
    A(md_table(["참조 자리", "건", "해결", "미해결", "해결 깊이", "비고"], [(k, v["n"], v["resolved"], v["unresolved"], ", ".join(f"{a}={b}" for a, b in v["by_depth"].items()) or "—", v["note"]) for k, v in RES.items()]))
    A("")
    tot_un = sum(v["unresolved"] for k, v in RES.items() if not k.startswith("부위 사전"))
    A(f"미해결 참조(⑨) 합계 **{tot_un}** (자리별 distinct 라벨 기준, 부위 확장 정준값 {RES['부위 사전 (뼈대 11 + 확장)']['unresolved']} 은 제외 — 그건 §8-2). 목록:")
    A("")
    for k, v in RES.items():
        if v["unresolved_labels"]:
            A(f"- **{k}** ({v['unresolved']}): " + " · ".join((f"`{l}`" + (f"@{h}" if h else "") + (f"({t})" if t not in ("unresolved", "extension") else "")) for l, h, t in v["unresolved_labels"]))
    A("")
    A("질문 14 두 묶음(modality_ref 빈 26 항목):")
    A("")
    A(md_table(["고민", "하위분류", "항목", "묶음", "발주서 목록 일치"], [(r["problem"], r["subcategory"], r["name"], r["bucket"], ", ".join(r["matched"]) or "—") for r in Q14]))
    A("")
    A("### 9.3 충돌 예상 수")
    A("")
    A(md_table(["종류", "무엇", "건"], [(c["kind"], c["what"], c["n"]) for c in CONF]))
    A("")
    for c in CONF:
        if c["detail"] and isinstance(c["detail"], list):
            A(f"- {c['what']}: " + "; ".join(str(x) for x in c["detail"]))
    A("")
    A(f"합계: value_conflict {sum(c['n'] for c in CONF if c['kind']=='value_conflict')} · duplicate_candidate {sum(c['n'] for c in CONF if c['kind']=='duplicate_candidate')} · unregistered_value {sum(c['n'] for c in CONF if c['kind']=='unregistered_value')} · unresolved_reference {tot_un}. 전부 사람 판정 전 `open`.")
    A("")
    A("### 9.4 결정 개체로 미리 적재될 원장 메모 (질문 23)")
    A("")
    tx = L["taxonomy.json"]
    rows = []
    for m in tx["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                for k in ["classification_issue", "reclassified_to", "correction_note", "verification_needed", "canonical_category"]:
                    if k in it:
                        rows.append((m["id"], it["id"], it["name"], k, str(it[k])[:70] + ("…" if len(str(it[k])) > 70 else "")))
    A(md_table(["계열", "항목 id", "항목", "키", "값"], rows))
    A("")
    A("## 10. 검산 결과")
    A("")
    A("`erd-v1-check.py` 를 독립 실행한 출력을 그대로 붙였다(같은 폴더에서 `python3 erd-v1-check.py` 로 재검산). 검사 A 잎 키 행선지 · B 사전 값 출처 · C ERD 출처 키·표적 · D 브론즈 sha256.")
    A("")
    return "\n".join(o)


REVIEW = [
    {"title": "complications.json 의 신뢰 순위 — 발주서 목록은 4, 원장엔 판단 키가 없다", "ref": "발주서 §5 · 질문 25",
     "fact": "complications.json 에는 version/updated/source_method/consensus_method 가 전혀 없다(21개 중 taxonomy·extracted 와 함께 3개).",
     "applied": "규칙 「키로 판단, 확신 없으면 3 으로 두고 표시」를 따라 3 + 표시. 다른 4등급 세 파일은 consensus_method 로 4 확정.",
     "ask": "complications.json 을 4 로 고정할 근거(원장 밖 지식)가 있으면 결정 개체로 내려 주면 v2 에서 4 로 바꾼다."},
    {"title": "cc_group 52 를 부위 사전 동의어로 — 절반 가까이가 부위가 아니다", "ref": "질문 24",
     "fact": "cc_group 52 중 뼈대 11 과 정규화 일치하는 것은 소수(코·입술·팔자주름 등). 표정주름·깊은주름·기미·피지과다형·주사치료·약물치료 같은 값은 부위가 아니라 증상·치료 유형 라벨이다. taxonomy problem 하위분류 label 53 도 같은 성격.",
     "applied": "기본값대로 전부 부위 사전에 넣되, 뼈대 불일치 값은 is_backbone=false 확장 정준값으로 두고 §9.1 에 표시.",
     "ask": "확장 정준값 중 「부위」로 남길 것과 「고민 하위분류 라벨」로 되돌릴 것을 가르는 결정. 이마/관자놀이·턱/턱선·볼/광대 같은 복합 라벨은 뼈대 두 개로 쪼갤지."},
    {"title": "taxonomy 항목 `indications.secondary` ≡ `extended` 가정", "ref": "질문 20",
     "fact": "modality 층은 extended 만, 항목 층은 extended 4 / secondary 9 로 갈린다. 같은 뜻인지 원장에 근거 없음.",
     "applied": "동의 키 정규화 기본값대로 secondary → extended 로 합치고 원문 키는 출처 경로로 남긴다.",
     "ask": "secondary 를 별도 속성으로 둘지."},
    {"title": "기법 사전의 경계 — taxonomy 하위분류 label 전부를 기법 후보로 넣었다", "ref": "§4 기법 개체",
     "fact": "하위분류 label 72 중 수입·국산·용도별·국산 HA·수입 HA·재질별·형태별·브랜드·기타·추가·시그니처 프로그램 등은 분류축이지 기법이 아니다. 에너지/방법을 뜻하는 label(프락셔널·IPL·HIFU (초음파) …)만 기법이다.",
     "applied": "네 출처(mechanism·energy_device type·pih subcategory·하위분류 label)의 distinct 값을 전부 정준값으로 두고, taxonomy 에서만 나온 값에 `only_in_taxonomy_subcategory` 플래그를 붙였다(사전 JSON).",
     "ask": "플래그 붙은 값 중 기법으로 인정할 것의 목록. 나머지는 사전에서 뺀다."},
    {"title": "질문 14 두 묶음과 실제 26 항목 이름의 대조", "ref": "질문 14",
     "fact": "§9.2 표. 발주서 목록과 원장 항목 이름을 부분 일치로 대조하면 ① 11 · ② 11 · 미배정 4 (P6 약물치료 · P13 미녹시딜·피나스테리드·두타스테리드). 발주서의 「경구약 4」가 이 4개를 가리키는지는 원장에 근거가 없다(수만 같다). 브이올렛은 P11·P12 두 곳에 있어 ① 에 2행.",
     "applied": "묶음 배정을 이름 부분 일치로만 하고 미배정 4 는 그대로 남김. ② 묶음 전부에 「범위 검토」 표시.",
     "ask": "미배정 항목의 묶음, 그리고 ① 묶음의 「기존 계열 매핑」 대상 계열(원장에 근거 없음)."},
    {"title": "product_tier 7 표면형 병합", "ref": "질문 22",
     "fact": "`국산+수입 혼합`·`수입+국산`·`국산/수입`·`혼합` 은 같은 뜻으로 보이나 원장에 근거 없음.",
     "applied": "7개 전부 정준값.", "ask": "병합 규칙."},
    {"title": "pih_risk_level 에 `none`(procedure-comparison) 을 합집합으로 넣었다", "ref": "사전 pih_risk_level",
     "fact": "pih-risk 5단계(very_low~very_high)에 `none` 은 없고, comparison 5값에는 `very_high` 가 없다.",
     "applied": "합집합 6값. `none` 의 정의문은 없음(null).", "ask": "`none` = very_low 동의어인지, 별도 등급인지."},
    {"title": "literature adverse_effects 문장 32 를 부작용 개체(문장 이름)로", "ref": "§4 부작용 개체",
     "fact": "발주서는 literature adverse_effects 를 부작용 개체로 모으라 했다. 문장(영문 한 줄)이 곧 이름이 되어 complications 의 이름형 부작용과 모양이 다르고, 자동 병합은 0 이다.",
     "applied": "kind=literature_claim 으로 부작용 개체에 두고, 이름형 부작용과의 연결은 ⑦ 후보/사람 결정.",
     "ask": "이대로 둘지, moa/effects 와 같이 evidence_statement 로 옮기고 부작용 개체와는 「근거 문장→부작용」 엣지로 할지."},
    {"title": "post-procedure-timeline `name` 의 구체 수준", "ref": "질문 7·11",
     "fact": "timeline name 10 중 계열명과 일치하는 것은 일부(보톡스·실리프팅·스킨부스터·바이오스티뮬레이터/콜라겐부스터). `프락셔널 CO2 레이저`·`HA 필러`·`HIFU/RF 리프팅`·`케미컬 필링 (중간 깊이)` 는 계열보다 좁다.",
     "applied": "R15 엣지는 category 계열(또는 M16-DCA 하위분류)에 붙이고 name 은 source_label. 더 좁은 대상은 사전 일치 시도 → §9.2 미해결.",
     "ask": "좁은 이름을 항목/하위분류에 사람이 매핑할지, 계열 수준으로 둘지."},
    {"title": "treatment-optimization concern 8 · procedure-comparison 9 ↔ 고민 14", "ref": "질문 12",
     "fact": "정규화 일치하는 것만 자동(§9.2). 주름 개선·볼륨 손실·바디컨투어링·rejuvenation 등은 불일치.",
     "applied": "사전 `problem` 후보로 두고 패키지→고민 엣지(R13)는 미해결.", "ask": "후보별 고민 코드 결정(또는 「별개 축」 결정)."},
    {"title": "synergy 노드 이름이 항목과 제품 양쪽에 있을 때 항목 우선", "ref": "질문 8",
     "fact": "울쎄라·써마지FLX·포텐자 등 29종은 taxonomy 항목이면서 제품이다.",
     "applied": "R18 끝점은 procedure(항목) 우선, 제품은 R3 로 따라감. 결과 태그 `item+product 겹침` 으로 표시.",
     "ask": "제품을 끝점으로 둘지."},
    {"title": "age_group `40대+`(annual_plans) vs `40대`·`50대+`(by_age_group)", "ref": "사전 age_group",
     "fact": "입도가 다른 두 체계.", "applied": "5값 전부 정준값, 병합 안 함.", "ask": "`40대+` = {40대, 50대+} 로 전개할지."},
    {"title": "anatomy botox_specific → M1, filler_specific → M2 (키 이름으로 계열 지정)", "ref": "R22",
     "fact": "원장에 M 코드가 없다. 키 이름 botox/filler 가 사전 동의어(botox: timeline id, filler_ha: products 섹션)와 겹쳐 계열을 지정했다.",
     "applied": "R22 엣지의 계열 끝을 키 이름으로 고정.", "ask": "지정 승인."},
    {"title": "pih-risk `notes.M1_to_M7` 범위 키 전개", "ref": "③ 형식 교정",
     "fact": "키가 범위 표기. 값 문장도 M1~M7 를 열거한다.", "applied": "M1..M7 일곱 계열의 pih_note 로 전개.", "ask": "승인."},
    {"title": "market-pricing 항목 122 · problem-combos products 문장 24 는 자동 연결이 거의 0", "ref": "질문 11",
     "fact": "`이마 주름 (수입)`·`울쎄라 (풀페이스)` 처럼 괄호 보충이 붙어 정규화 일치가 안 된다(§9.2). products 문장은 `A or B + C` 합성.",
     "applied": "계열 속성(price_items)·패키지 속성(products_text)으로 보존, 시술/제품 연결 없음.",
     "ask": "괄호 앞 토큰 일치 같은 완화 규칙을 허용할지(허용하면 ⑦이 아니라 ②가 된다)."},
    {"title": "complications evidence URL `;` 분리, literature 각주·언어 섞임 정제 — 정제 규칙의 위치", "ref": "질문 19 · ③",
     "fact": "ERD 는 「정제한다」까지만 정하고 정제 규칙(정규식)은 실버 빌더 명세로 남겼다.",
     "applied": "원문은 브론즈, 정제값은 실버 속성.", "ask": "정제 규칙을 ERD v2 에 넣을지 빌더 명세로 둘지."},
    {"title": "universal_checks 12 는 계열 엣지 없이 person_condition.universal=true", "ref": "R16",
     "fact": "원장은 공통 체크를 계열과 묶지 않는다.", "applied": "속성 플래그.", "ask": "17계열 전부에 R16 엣지를 펼칠지."},
    {"title": "주호소 이름 중복 — 이름만으로 6, (problem_id, 이름) 결합이면 2", "ref": "질문 9",
     "fact": "problem-packages 의 cc 는 problem_id 와 함께 온다. 이름만 보면 6개(아그네스·스킨보톡스·프락셔널레이저·니들RF·서브시전·브이올렛)가 여러 고민에 반복되지만, (problem_id, 이름) 으로 결합하면 P9 안의 니들RF·프락셔널레이저 2건만 모호하다.",
     "applied": "기본값대로 6건을 충돌 개체로 예상(§9.3). 결합 키는 (problem_id, 이름) 으로 ERD 에 적었다.",
     "ask": "충돌을 6으로 둘지 2로 줄일지."},
    {"title": "procedure-comparison 의 시술별 비교값(통증·다운타임·비용 …)을 R12 엣지 속성에", "ref": "R12",
     "fact": "같은 시술이 두 비교표에 다른 값으로 들어갈 수 있다(히알루론산 필러 2회).", "applied": "비교표(package kind=comparison)→멤버 엣지 속성.",
     "ask": "시술 개체 속성으로 올리고 값 충돌을 ⑥으로 다룰지."},
]


def main():
    colrows = build_column_map()
    dicts = build_dictionaries()
    IDX = Index()
    RES = resolution_report(IDX)
    CONF = conflict_estimates(IDX)
    Q14 = q14_bundles()
    erd = write_outputs(colrows, dicts, RES, CONF, Q14)
    md = build_erd_md(erd, colrows, dicts, RES, CONF, Q14)
    open(os.path.join(WORK, "erd-v1.md"), "w", encoding="utf-8").write(md)
    # 검산 부착
    spec = importlib.util.spec_from_file_location("chk", os.path.join(WORK, "erd-v1-check.py"))
    chk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chk)
    ok, report = chk.run_checks()
    with open(os.path.join(WORK, "erd-v1.md"), "a", encoding="utf-8") as f:
        f.write(report + "\n")
    with open(os.path.join(WORK, "erd-v1-column-map.md"), "a", encoding="utf-8") as f:
        f.write("## 검산 결과\n\n" + report + "\n")
    print("OK" if ok else "FAIL")
    print(report)
    print("dests", Counter(r["dest"] for r in colrows))
    print("dicts", len(dicts), "entities", len(S.ENTITIES), "relations", len(S.RELATIONS), "review", len(REVIEW))
    print("unresolved total(excl site)", sum(v["unresolved"] for k, v in RES.items() if not k.startswith("부위 사전")))


if __name__ == "__main__":
    main()
