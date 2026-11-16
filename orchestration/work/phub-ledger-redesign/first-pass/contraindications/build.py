#!/usr/bin/env python3
"""contraindications.json 1차 조사 — 재현 빌드.

레포 루트에서:
  uv run --no-project --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/contraindications/build.py

원본은 읽기만 한다. 쓰는 곳은 이 파일이 있는 폴더뿐이다.
입력(수동 기록): manual-expressions.json · manual-observations.json ·
segmentation-review.json · reading-log.json
출력: source-map.json · morphology.json · expressions.json · coverage.json · review.md ·
build-output.txt
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/contraindications.json"
SRC = REPO / SRC_REL
OUT_REL = "orchestration/work/phub-ledger-redesign/first-pass/contraindications"

OFFSET_UNIT = ("span_cp = 디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end) (시작 포함·끝 제외). "
               "file_span_cp = 원본 파일 텍스트(UTF-8 디코딩) 전체 기준 코드 포인트 [start,end). "
               "byte_span = 원본 파일 UTF-8 바이트 [start,end). literal_span = JSON 리터럴(따옴표 포함) 의 file 코드 포인트 구간. "
               "이 파일은 이스케이프 0 · BMP 밖 문자 0 이라 문자열 내부 리터럴 = 디코딩 문자열이고 "
               "코드 포인트 = UTF-16 코드 단위(빌드가 검사).")

LOG = []


def log(*a):
    line = " ".join(str(x) for x in a)
    LOG.append(line)
    print(line)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- 1. 위치 보존 JSON 스캐너
class Scanner:
    WS = " \t\n\r"

    def __init__(self, text):
        self.s = text
        self.nodes = []
        self.keys = []
        self.duplicate_keys = []
        self.escapes = []

    def ws(self, i):
        while i < len(self.s) and self.s[i] in self.WS:
            i += 1
        return i

    def parse(self):
        i = self.value(self.ws(0), "", None, None, 0)
        if self.ws(i) != len(self.s):
            raise ValueError(f"trailing data at {i}")

    def string(self, i):
        j, out = i + 1, []
        while True:
            c = self.s[j]
            if c == '"':
                return j + 1, "".join(out)
            if c == "\\":
                e = self.s[j + 1]
                simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                          "n": "\n", "r": "\r", "t": "\t"}
                if e in simple:
                    out.append(simple[e]); self.escapes.append([j, j + 2]); j += 2; continue
                if e == "u":
                    out.append(chr(int(self.s[j + 2:j + 6], 16)))
                    self.escapes.append([j, j + 6]); j += 6; continue
                raise ValueError(f"bad escape at {j}")
            if ord(c) < 0x20:
                raise ValueError(f"control char at {j}")
            out.append(c); j += 1

    def value(self, i, ptr, parent, key, order):
        c = self.s[i]
        node = {"pointer": ptr, "parent_pointer": parent, "key": key, "order": order}
        self.nodes.append(node)
        if c == "{":
            node["type"] = "object"
            children, seen = [], set()
            j = self.ws(i + 1)
            if self.s[j] == "}":
                j += 1
            else:
                n = 0
                while True:
                    ks = j
                    j, k = self.string(j)
                    kptr = ptr + "/" + k.replace("~", "~0").replace("/", "~1")
                    dup = k in seen
                    rec = {"key": k, "object_pointer": ptr, "value_pointer": kptr,
                           "file_span_cp": [ks, j], "order_in_object": n, "duplicate": dup}
                    self.keys.append(rec)
                    if dup:
                        self.duplicate_keys.append(rec)
                        kptr += f"#dup{n}"
                    seen.add(k); children.append(k)
                    j = self.ws(j); assert self.s[j] == ":"
                    j = self.value(self.ws(j + 1), kptr, ptr, k, n)
                    j = self.ws(j); n += 1
                    if self.s[j] == ",":
                        j = self.ws(j + 1); continue
                    assert self.s[j] == "}"; j += 1; break
            node["children"] = children
            node["length"] = len(children)
        elif c == "[":
            node["type"] = "array"
            j = self.ws(i + 1); n = 0
            if self.s[j] == "]":
                j += 1
            else:
                while True:
                    j = self.value(j, f"{ptr}/{n}", ptr, n, n)
                    n += 1; j = self.ws(j)
                    if self.s[j] == ",":
                        j = self.ws(j + 1); continue
                    assert self.s[j] == "]"; j += 1; break
            node["length"] = n
        elif c == '"':
            node["type"] = "string"
            j, v = self.string(i)
            node["value"] = v
            node["inner_file_span_cp"] = [i + 1, j - 1]
        else:
            m = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(self.s, i)
            lit = m.group(0); j = m.end()
            node["type"] = {"true": "boolean", "false": "boolean", "null": "null"}.get(lit, "number")
            node["value"] = json.loads(lit)
        node["literal_span"] = [i, j]
        if node["type"] not in ("object", "array"):
            node["literal"] = self.s[i:j]
        return j


def resolve(data, ptr):
    cur = data
    for p in ptr.split("/")[1:]:
        p = p.replace("~1", "/").replace("~0", "~")
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    return cur


def is_leaf(n):
    return n["type"] not in ("object", "array") or n["length"] == 0


# ---------------------------------------------------------------- 분석 적용·제외 규칙
APPLY_FIELDS = {
    "description": "원장 설명 한국어 문장",
    "from_name": "시술명 한국어 표기(혼합 언어 포함)",
    "to_name": "시술명 한국어 표기(혼합 언어 포함)",
    "interval": "간격 서술 한국어 구절",
    "note": "근거·순서·조건 서술 한국어 문장",
}
EXCLUDE_FIELDS = {
    "version": "버전 문자열(숫자·점) — 언어 텍스트 아님",
    "updated": "날짜 문자열(YYYY-MM-DD) — 언어 텍스트 아님",
    "from": "원장 내부 ID 코드(M+숫자) — 식별자",
    "to": "원장 내부 ID 코드(M+숫자) — 식별자",
    "level": "영문 등급 코드(safe/caution/warning) — 열거 코드값",
}


def morph_role(ptr):
    field = ptr.rsplit("/", 1)[-1]
    if field in APPLY_FIELDS:
        return "applied", APPLY_FIELDS[field]
    if field in EXCLUDE_FIELDS:
        return "excluded", EXCLUDE_FIELDS[field]
    return None, None


def section_of(ptr):
    if ptr.startswith("/rules/"):
        return "S1"
    return "S0"


def context_of(ptr, data):
    parts = ptr.split("/")[1:]
    if len(parts) >= 2 and parts[0] == "rules":
        ri = int(parts[1]); r = data["rules"][ri]
        sib = [f"/rules/{ri}/{k}" for k in r]
        return {"block": "rules", "rule_index": ri, "rule_pointer": f"/rules/{ri}",
                "rule_from": r.get("from"), "rule_to": r.get("to"),
                "rule_from_name": r.get("from_name"), "rule_to_name": r.get("to_name"),
                "field": parts[2] if len(parts) > 2 else None,
                "read_with": [p for p in sib if p != ptr],
                "shared_context": ["/description"]}
    return {"block": "top", "field": parts[0] if parts else None,
            "read_with": ["/version", "/updated", "/description"]}


def main():
    raw = SRC.read_bytes()
    h0 = sha256(raw)
    text = raw.decode("utf-8")
    log("source", SRC_REL, "bytes", len(raw), "sha256", h0)
    assert all(ord(c) < 0x10000 for c in text), "non-BMP char"
    sc = Scanner(text); sc.parse()
    data = json.loads(text)
    log("nodes", len(sc.nodes), "keys", len(sc.keys), "dup_keys", len(sc.duplicate_keys), "escapes", len(sc.escapes))

    # byte offsets
    cp2b = [0]
    for ch in text:
        cp2b.append(cp2b[-1] + len(ch.encode("utf-8")))
    for n in sc.nodes:
        n["byte_span"] = [cp2b[n["literal_span"][0]], cp2b[n["literal_span"][1]]]
        assert raw[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") == text[n["literal_span"][0]:n["literal_span"][1]]
        if n["type"] == "string":
            a, b = n["inner_file_span_cp"]
            assert text[a:b] == n["value"], n["pointer"]  # 이스케이프 0 조건
        if n["pointer"]:
            assert resolve(data, n["pointer"]) == n.get("value", resolve(data, n["pointer"]))
        n["is_leaf"] = is_leaf(n)
        n["section"] = section_of(n["pointer"])
        n["context"] = context_of(n["pointer"], data)
        r, why = morph_role(n["pointer"]) if n["type"] == "string" else (None, None)
        n["morph"] = {"role": r, "reason": why} if r else None
    for k in sc.keys:
        a, b = k["file_span_cp"]
        k["byte_span"] = [cp2b[a], cp2b[b]]

    # 구조 사실(의미 승인 아님)
    rules = data["rules"]
    id_names = {}
    for i, r in enumerate(rules):
        for side in ("from", "to"):
            id_names.setdefault(r[side], {}).setdefault(r[side + "_name"], []).append(f"/rules/{i}/{side}")
    pairs = {}
    for i, r in enumerate(rules):
        pairs.setdefault(tuple(sorted([r["from"], r["to"]])), []).append(i)
    key_sets = {}
    for i, r in enumerate(rules):
        key_sets.setdefault(tuple(r.keys()), []).append(i)
    struct = {
        "rule_count": len(rules),
        "rule_key_orders": [{"keys": list(k), "rules": v} for k, v in key_sets.items()],
        "id_to_names": id_names,
        "ids_present": sorted(id_names, key=lambda x: int(x[1:])),
        "unordered_pair_duplicates": {"-".join(k): v for k, v in pairs.items() if len(v) > 1},
        "self_pairs": [i for i, r in enumerate(rules) if r["from"] == r["to"]],
        "level_values": sorted({r["level"] for r in rules}),
        "level_counts": {lv: sum(1 for r in rules if r["level"] == lv) for lv in sorted({r["level"] for r in rules})},
        "from_sequence": [r["from"] for r in rules],
    }
    log("rules", len(rules), "ids", struct["ids_present"], "pair_dups", struct["unordered_pair_duplicates"],
        "levels", struct["level_counts"])

    leaves = [n["pointer"] for n in sc.nodes if n["is_leaf"]]
    source_map = {
        "source": {"path": SRC_REL, "bytes": len(raw), "sha256": h0, "code_points": len(text),
                   "lines": text.count("\n") + 1, "trailing_newline": text.endswith("\n"),
                   "encoding": "utf-8", "bom": raw.startswith(b"\xef\xbb\xbf")},
        "offset_unit": OFFSET_UNIT,
        "parser": "build.py Scanner — 중복 키 감지·원문 구간 보존. 결과 json.loads 와 대조.",
        "duplicate_keys": sc.duplicate_keys,
        "escapes": sc.escapes,
        "counts": {"nodes": len(sc.nodes), "leaves": len(leaves), "keys": len(sc.keys),
                   "by_type": {t: sum(1 for n in sc.nodes if n["type"] == t) for t in
                               ("object", "array", "string", "number", "boolean", "null")},
                   "empty_containers": [n["pointer"] for n in sc.nodes if n["type"] in ("object", "array") and n["length"] == 0],
                   "empty_strings": [n["pointer"] for n in sc.nodes if n["type"] == "string" and n["value"] == ""]},
        "structure_facts": struct,
        "nodes": sc.nodes,
        "keys": sc.keys,
    }

    # ---------------------------------------------------------------- 2. 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(model_type="cong", num_workers=1)
    settings = {"analyzer": "kiwipiepy", "version": kiwipiepy.__version__, "model_type": kiwi.model_type,
                "num_workers": kiwi.num_workers, "default_dict": "기본 내장 사전(load_default_dict 기본값)",
                "user_dict": None, "typos": None,
                "tokenize_options": {"match_options": "Match.ALL(기본)", "normalize_coda": False, "z_coda": True,
                                     "split_complex": False, "split_sents": False, "saisiot": None,
                                     "stopwords": None, "blocklist": None},
                "pos_scheme": "Kiwi 품사 태그(세종 기반 확장)",
                "unit": "값 하나씩 독립 분석. 원문 정규화 없음 — 입력 문자열 = 디코딩 원문 그대로",
                "offset": "token start/end 는 kiwipiepy 가 돌려준 입력 문자열 인덱스. BMP 문자만 있어 코드 포인트와 같다",
                "lemma": "Token.lemma 를 도구 출력 그대로 기록. 도구가 주지 않는 기본형은 만들지 않는다"}
    log("kiwi", settings["version"], settings["model_type"], "workers", settings["num_workers"])

    def tok(s):
        out = []
        for t in kiwi.tokenize(s):
            out.append({"form": t.form, "tag": str(t.tag), "lemma": t.lemma, "start": t.start, "end": t.end,
                        "len": t.len, "surface": s[t.start:t.end], "score": round(t.score, 4),
                        "oov": bool(getattr(t, "oov", False))})
        return out

    records, exclusions = [], []
    for n in sc.nodes:
        if n["type"] != "string":
            continue
        role = n["morph"]
        if role and role["role"] == "applied":
            records.append({"id": f"T{len(records):04d}", "pointer": n["pointer"], "text": n["value"],
                            "file_span_cp": n["inner_file_span_cp"], "reason": role["reason"],
                            "tokens": tok(n["value"])})
        else:
            exclusions.append({"pointer": n["pointer"], "value": n["value"],
                               "reason": role["reason"] if role else "규칙 없음"})
    for n in sc.nodes:
        if n["type"] not in ("string", "object", "array"):
            exclusions.append({"pointer": n["pointer"], "value": n["value"], "reason": f"{n['type']} 값 — 텍스트 아님"})
    field_names = {}
    for k in sc.keys:
        field_names.setdefault(k["key"], []).append(k["value_pointer"])
    field_records = [{"field_name": f, "occurrences": len(ps), "pointers": ps, "role": "field_name",
                      "note": "영문 snake_case 식별자. 언어 텍스트와 역할을 나눠 기록만 한다",
                      "tokens": tok(f)} for f, ps in field_names.items()]

    # 전문어 출현별 분절 대조
    seg = json.loads((HERE / "segmentation-review.json").read_text())
    seg_rows = []
    for term, rv in seg["terms"].items():
        for rec in records:
            pat = term[3:] if term.startswith("re:") else re.escape(term)
            for m in re.finditer(pat, rec["text"]):
                a, b = m.span()
                toks = [f"{t['form']}/{t['tag']}" for t in rec["tokens"] if t["start"] < b and t["end"] > a]
                ov = rv.get("by_pointer", {}).get(rec["pointer"], rv)
                seg_rows.append({"term": term, "pointer": rec["pointer"], "span_cp": [a, b], "tokens": toks,
                                 "verdict": ov["verdict"], "impact": ov.get("impact", "")})
    # 하나의 리뷰 규칙이 실제 원문 출현에 닿는지
    for term in seg["terms"]:
        assert any(r["term"] == term for r in seg_rows), f"segmentation term not in text: {term}"
    known = [r for r in seg_rows if r["verdict"] == "known_issue"]
    log("morph records", len(records), "tokens", sum(len(r["tokens"]) for r in records), "excluded", len(exclusions),
        "seg_rows", len(seg_rows), "known_issue occurrences", len(known))
    morphology = {"settings": settings, "records": records, "exclusions": exclusions,
                  "field_names": field_records,
                  "segmentation_review": {"method": seg["_about"], "rows": seg_rows,
                                          "summary": {"rows": len(seg_rows), "known_issue": len(known),
                                                      "ok": sum(1 for r in seg_rows if r["verdict"] == "ok")}}}

    # ---------------------------------------------------------------- 3. 복합 표현
    by_ptr = {n["pointer"]: n for n in sc.nodes}
    man = json.loads((HERE / "manual-expressions.json").read_text())
    exprs = []
    for it in man["items"]:
        n = by_ptr[it["pointer"]]
        v = n["value"]
        occ = it.get("occurrence", 1)
        starts = [m.start() for m in re.finditer(re.escape(it["text"]), v)]
        assert len(starts) >= occ, f"manual expression not found: {it}"
        a = starts[occ - 1]; b = a + len(it["text"])
        exprs.append({"id": f"E{len(exprs):04d}", "method": "manual_reading", "pointer": it["pointer"],
                      "text": it["text"], "occurrence": occ, "occurrences_in_value": len(starts),
                      "span_cp": [a, b], "file_span_cp": [n["inner_file_span_cp"][0] + a, n["inner_file_span_cp"][0] + b],
                      "tags": it["tags"], "observation": it["note"],
                      "whole_value": it["pointer"] + "", "context": n["context"]})
    n_manual = len(exprs)
    AUTO = [
        ("quantity_range", r"\d+(?:일|주|개월)?~\d+(?:일|주|개월)"),
        ("quantity", r"\d+(?:일|주|개월)"),
        ("lower_bound", r"\d+(?:일|주|개월) ?이상"),
        ("same_day", r"같은 날"),
        ("possibility", r"가능|수 있음"),
        ("recommendation", r"권장"),
        ("prohibition", r"금지"),
        ("prevention", r"방지"),
        ("risk", r"위험|우려"),
        ("order", r"먼저|순서|후 |전 |다음"),
        ("condition", r"\S+ 시 |다르면|따라 다름|특히"),
        ("negation_degree", r"무관|적음|부족|과도한|과자극|과축적|과교정|극대화|강한|완전히|완전"),
        ("evidence", r"이론적|임상 근거"),
        ("open_list", r" 등\)"),
        ("arrow", r"→"),
        ("plus", r" \+ "),
        ("slash", r"/"),
        ("middot", r"·"),
        ("paren", r"\([^)]*\)"),
        ("colon_branch", r": "),
        ("level_code_in_text", r"safe|caution|warning"),
    ]
    for rec in records:
        n = by_ptr[rec["pointer"]]
        for name, pat in AUTO:
            for m in re.finditer(pat, rec["text"]):
                a, b = m.span()
                exprs.append({"id": f"E{len(exprs):04d}", "method": "regex", "pattern_name": name, "pattern": pat,
                              "pointer": rec["pointer"], "text": m.group(0), "span_cp": [a, b],
                              "file_span_cp": [n["inner_file_span_cp"][0] + a, n["inner_file_span_cp"][0] + b],
                              "context": n["context"]})
    keyset = [(e["pointer"], tuple(e["span_cp"]), e["method"], e.get("pattern_name")) for e in exprs]
    dups = len(keyset) - len(set(keyset))
    same_span = {}
    for e in exprs:
        same_span.setdefault((e["pointer"], tuple(e["span_cp"])), []).append(e["id"])
    same_span_groups = [v for v in same_span.values() if len(v) > 1]
    log("expressions manual", n_manual, "regex", len(exprs) - n_manual, "exact_dups", dups,
        "same_span_groups(intended overlaps)", len(same_span_groups))
    assert dups == 0
    expressions = {"method": {"manual_reading": "전체 원문을 직접 읽고 표현을 고름(manual-expressions.json). tags 는 탐색 관점",
                              "regex": "수집 보조 후보. 의미 해석 아님. 아래 patterns",
                              "patterns": [{"name": a, "pattern": b} for a, b in AUTO],
                              "overlap_policy": "표현 구간 겹침은 의도된 것(전체 구절 + 부분 구절, manual + regex). 같은 pointer·span·method·pattern 의 완전 중복은 0이어야 한다"},
                   "counts": {"manual": n_manual, "regex": len(exprs) - n_manual, "exact_duplicates": dups,
                              "same_span_groups": len(same_span_groups)},
                   "same_span_groups": same_span_groups,
                   "items": exprs}

    # ---------------------------------------------------------------- 4. 커버리지
    rl = json.loads((HERE / "reading-log.json").read_text())
    owned = {"S0": [p for p in leaves if section_of(p) == "S0"], "S1": [p for p in leaves if section_of(p) == "S1"]}
    containers = {"S0": [n["pointer"] for n in sc.nodes if not n["is_leaf"] and section_of(n["pointer"]) == "S0"],
                  "S1": [n["pointer"] for n in sc.nodes if not n["is_leaf"] and section_of(n["pointer"]) == "S1"]}
    coverage = {"source_sha256": h0, "total_leaf_pointers": len(leaves),
                "note": "owned_leaf_pointers = 그 구획이 소유한 원문 말단 값(빈 컨테이너 포함). shared_context = 함께 읽되 소유하지 않는 상위 문맥. "
                        "read_status 는 reading-log.json 의 직접 읽기 기록에서 온다. machine_extraction 은 build.py 자동 처리 범위.",
                "sections": []}
    for sid in ("S0", "S1"):
        r = rl["sections"][sid]
        coverage["sections"].append({
            "id": sid, "pointer_range": r["pointer_range"], "owned_leaf_pointers": owned[sid],
            "owned_containers": containers[sid], "shared_context": r["shared_context"],
            "read_status": r["read_status"], "read_method": r["read_method"], "read_order": r["read_order"],
            "last_read_pointer": r["last_read_pointer"],
            "machine_extraction": {"source_map": True, "morphology": True, "regex_candidates": True},
            "review_file": "review.md", "review_anchor": r["review_anchor"],
            "observations_file": "manual-observations.json", "issues_file": "issues.md"})
    coverage["remaining_sections"] = [s["id"] for s in coverage["sections"] if s["read_status"] != "direct_read_done"]

    # ---------------------------------------------------------------- 5. review.md
    obs = json.loads((HERE / "manual-observations.json").read_text())
    expr_by_ptr = {}
    for e in exprs:
        if e["method"] == "manual_reading":
            expr_by_ptr.setdefault(e["pointer"], []).append(e)
    L = []
    w = L.append
    w("# contraindications.json — 1차 조사 (읽기용)\n")
    w("> **1차 범위 종료: 예(코디 확인 전)** · **원장 전체 완료 아님** — 의미 모델·정규화·관계 확정은 하지 않았다. 미결은 [issues.md](./issues.md).\n")
    w(f"- 원본: `{SRC_REL}` · {len(raw)} bytes · sha256 `{h0}` · 1줄 압축 JSON · 끝 줄바꿈 {'있음' if text.endswith(chr(10)) else '없음'} · BOM 없음")
    w(f"- 노드 {len(sc.nodes)} · 말단 {len(leaves)} · 키 출현 {len(sc.keys)} · 중복 키 {len(sc.duplicate_keys)} · 이스케이프 {len(sc.escapes)} · 빈 값 0")
    w("- 구간 단위: " + OFFSET_UNIT)
    w("- 기계 기록: [source-map.json](./source-map.json) · [morphology.json](./morphology.json) · [expressions.json](./expressions.json) · [coverage.json](./coverage.json) · 검증 [validation.md](./validation.md)\n")
    w("## 상태\n")
    fmt = {"nodes": len(sc.nodes), "leaves": len(leaves), "keys": len(sc.keys), "applied": len(records),
           "tokens": sum(len(r["tokens"]) for r in records), "excluded": len(exclusions), "manual": n_manual,
           "regex": len(exprs) - n_manual, "known": len(known),
           "level_counts": " · ".join(f"{k} {v}" for k, v in struct["level_counts"].items())}
    for row in obs["status"]:
        w(f"- **{row[0]}**: {row[1].format_map(fmt)}")
    w("\n## 구획 목차\n")
    w("| 구획 | 원문 Pointer 범위 | 소유 말단 수 | 직접 읽기 | 절 |")
    w("|---|---|---|---|---|")
    for s in coverage["sections"]:
        w(f"| {s['id']} | `{s['pointer_range']}` | {len(s['owned_leaf_pointers'])} | {s['read_status']} | [{s['review_anchor']}](#{s['review_anchor'].lower().replace(' ', '-').replace('·', '')}) |")
    w("\n## 컬럼 구성 표\n")
    w("| 원본 컬럼명 / JSON 경로 패턴 | 자료형 · 중첩 | 출현 | 값 형태 변형 | 원문 예시 | 예시 위치 |")
    w("|---|---|---|---|---|---|")
    for row in obs["columns"]:
        w("| " + " | ".join(c.format_map(fmt) for c in row) + " |")
    w("\n빈 문자열·빈 배열·빈 객체·null·숫자·불리언: **없음**(빌드 집계 0). 선택적 필드: **없음** — 27개 rule 모두 같은 7개 키를 같은 순서로 가진다.\n")

    w("## S0 · 최상위 메타데이터\n")
    w("| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |")
    w("|---|---|---|---|")
    for p in ("/version", "/updated", "/description"):
        n = by_ptr[p]
        w(f"| {n['key']} | `{p}` | {n['type']} | {n['value']} |")
    w(f"| rules | `/rules` | array(object) 길이 {by_ptr['/rules']['length']} | (S1) |")
    w("\n**잠정 관찰 (원문 아님)**\n")
    for o in obs["sections"]["S0"]:
        w(f"- {o}")
    w("\n**직접 읽기 표현** (`/description`)\n")
    for e in expr_by_ptr.get("/description", []):
        w(f"- `{e['id']}` [{e['span_cp'][0]},{e['span_cp'][1]}) 「{e['text']}」 — {', '.join(e['tags'])}" + (f" · 관찰: {e['observation']}" if e['observation'] else ""))

    w("\n## S1 · rules 전체\n")
    w("구획 공통 문맥: `/description`(「시술 간 금기/주의사항/간격 매트릭스」). 각 rule 은 원본 배열 순서대로다.\n")
    for i, r in enumerate(rules):
        w(f"### /rules/{i}\n")
        w("| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |")
        w("|---|---|---|---|")
        for k, v in r.items():
            w(f"| {k} | `/rules/{i}/{k}` | {type(v).__name__ if not isinstance(v, str) else 'string'} | {v} |")
        es = [e for f in ("interval", "note", "from_name", "to_name") for e in expr_by_ptr.get(f"/rules/{i}/{f}", [])]
        if es:
            w("\n직접 읽기 표현 (원문 구간)\n")
            w("| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |")
            w("|---|---|---|---|---|")
            for e in es:
                w(f"| {e['id']} | `{e['pointer']}` | [{e['span_cp'][0]},{e['span_cp'][1]}) | {e['text'].replace('|', '¦')} | {', '.join(e['tags'])} |")
        w("\n**잠정 관찰 (원문 아님)**\n")
        olist = obs["rules"].get(str(i), [])
        for o in olist:
            w(f"- {o}")
        exo = [e for e in es if e["observation"]]
        for e in exo:
            w(f"- `{e['id']}`: {e['observation']}")
        if not olist and not exo:
            w("- (별도 관찰 없음)")
        ks = [x for x in known if x["pointer"].startswith(f"/rules/{i}/")]
        if ks:
            w("\n알려진 형태소 오분절 (원시 출력 · 미교정)\n")
            for x in ks:
                w(f"- `{x['pointer']}` [{x['span_cp'][0]},{x['span_cp'][1]}) 「{x['term']}」 → {' + '.join(x['tokens'])} — {x['impact']}")
        w("")
    w("## 구조 사실 (원문 그대로 · 의미 승인 아님)\n")
    w(f"- 등장 ID: {', '.join(struct['ids_present'])} (M10 없음)")
    w("- ID ↔ 이름: " + "; ".join(f"{k}={'/'.join(v.keys())}({sum(len(x) for x in v.values())})" for k, v in
                                    sorted(id_names.items(), key=lambda x: int(x[0][1:]))))
    w(f"- level 값별 수: {struct['level_counts']}")
    w(f"- 순서 무시한 쌍 중복: {struct['unordered_pair_duplicates'] or '없음'} · 자기 쌍: {struct['self_pairs'] or '없음'}")
    w(f"- from 순서(배열 순): {' '.join(struct['from_sequence'])}")
    (HERE / "review.md").write_text("\n".join(L) + "\n")

    for name, obj in (("source-map.json", source_map), ("morphology.json", morphology),
                      ("expressions.json", expressions), ("coverage.json", coverage)):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
    h1 = sha256(SRC.read_bytes())
    assert h0 == h1, "source changed during build"
    log("source sha256 unchanged", h1 == h0)
    (HERE / "build-output.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
