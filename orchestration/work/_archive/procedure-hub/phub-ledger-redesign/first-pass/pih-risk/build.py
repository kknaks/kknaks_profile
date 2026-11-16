#!/usr/bin/env python3
"""pih-risk.json 1차 조사 재현 빌드.

실행 (레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/pih-risk/build.py

읽는 것: 원본 원장(읽기 전용) + 이 폴더의 수동 기록
  segments.json · manual/facets.json · manual/S*.json(구획별 읽기 기록·관찰·수동 표현·오분절)
쓰는 것: 이 폴더 안의 source-map.json · morphology.json · expressions.json ·
  coverage.json · review.md · review-part-S*.md
원본은 열기만 하고 쓰지 않는다. 시작/끝 해시를 비교한다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/pih-risk.json"
SRC = REPO / SRC_REL
EXPECTED_SHA = "cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8"


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ptr_escape(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 위치 스캐너
class Scanner:
    """디코딩된 원문(str) 위를 직접 훑어 모든 값·키의 리터럴 구간을 잡는다.
    json.loads 와 독립이며, 결과 값은 json.loads 로 다시 대조한다.
    중복 키는 덮어쓰지 않고 출현 순서대로 기록한다."""

    WS = " \t\r\n"

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.keys = []
        self.dupes = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def string(self):
        s = self.i
        assert self.t[s] == '"'
        j = s + 1
        while True:
            c = self.t[j]
            if c == "\\":
                j += 2
                continue
            if c == '"':
                break
            j += 1
        self.i = j + 1
        raw = self.t[s:self.i]
        return json.loads(raw), s, self.i, raw

    def value(self, ptr, parent, keyidx, depth, member_key=None):
        self.ws()
        c = self.t[self.i]
        node = {"pointer": ptr, "parent": parent, "key_or_index": keyidx, "depth": depth}
        if member_key is not None:
            node["member_key"] = member_key
        order = len(self.nodes)
        self.nodes.append(node)
        node["order"] = order
        s = self.i
        if c == "{":
            node["type"] = "object"
            self.i += 1
            self.ws()
            seen = {}
            n = 0
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke, kraw = self.string()
                    kp = ptr + "/" + ptr_escape(k)
                    krec = {"key": k, "member_pointer": kp, "object_pointer": ptr,
                            "cp": [ks, ke], "raw_literal": kraw, "member_index": n}
                    if k in seen:
                        self.dupes.append({"object_pointer": ptr, "key": k, "first_cp": seen[k], "dup_cp": [ks, ke]})
                        krec["duplicate_of_earlier"] = True
                    seen[k] = [ks, ke]
                    self.keys.append(krec)
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    self.value(kp, ptr, k, depth + 1, member_key={"cp": [ks, ke]})
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node["child_count"] = n
        elif c == "[":
            node["type"] = "array"
            self.i += 1
            self.ws()
            n = 0
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(ptr + "/" + str(n), ptr, n, depth + 1)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            node["child_count"] = n
        elif c == '"':
            v, _, _, raw = self.string()
            node["type"] = "string"
            node["value"] = v
            node["has_escape"] = "\\" in raw
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.t, self.i)
            assert m, f"bad token at {self.i}"
            self.i = m.end()
            v = json.loads(m.group(0))
            node["type"] = "null" if v is None else "boolean" if isinstance(v, bool) else "number"
            node["value"] = v
        node["cp"] = [s, self.i]
        node["raw_literal"] = self.t[s:self.i]
        if node["type"] in ("object", "array"):
            node["empty"] = node["child_count"] == 0
            del node["raw_literal"]  # 컨테이너는 구간만 둔다 (전문 중복 방지)
        else:
            node["empty"] = node["type"] == "string" and node["value"] == ""
        return node


def cp_to_byte_table(text):
    tbl = [0]
    for ch in text:
        tbl.append(tbl[-1] + len(ch.encode("utf-8")))
    return tbl


def get_by_pointer(doc, ptr):
    if ptr == "":
        return doc
    cur = doc
    for part in ptr.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def segment_of(ptr, segs):
    hits = []
    for s in segs:
        if ptr in s.get("owns_exact", []):
            hits.append(s["id"])
        elif any(ptr == p or ptr.startswith(p + "/") for p in s["prefixes"]):
            hits.append(s["id"])
    return hits


def item_context(ptr, doc):
    m = re.match(r"^/procedures/(\d+)", ptr)
    if not m:
        top = ptr.split("/")[1] if ptr else ""
        return {"scope": "top-level", "top_key": top}
    i = int(m.group(1))
    p = doc["procedures"][i]
    return {"scope": "procedure", "index": i, "item_pointer": f"/procedures/{i}",
            "category": p["category"], "subcategory": p["subcategory"],
            "name": p["name"], "procedure_ref": p["procedure_ref"]}


# ---------------------------------------------------------------- 분석 적용/제외 정책
VALUE_EXCLUDE = [
    (re.compile(r"^/version$"), "version_code", "버전 식별자(\"1.0\"). 언어 텍스트 아님"),
    (re.compile(r"^/updated$"), "date", "날짜(ISO). 언어 텍스트 아님"),
    (re.compile(r"^/procedures/\d+/category$"), "id_code", "카테고리 코드(Mxx). 식별자"),
    (re.compile(r"^/procedures/\d+/procedure_ref$"), "id_code", "원장 간 참조 코드(Mxx-x-x). 식별자"),
    (re.compile(r"^/procedures/\d+/pih_risk$"), "enum_code", "risk_levels 키를 가리키는 영문 열거 코드. 언어 텍스트로 분석하지 않고 원문 보존"),
]
KEY_EXCLUDE = [
    (re.compile(r"^/notes/[^/]+$"), "id_key", "notes 의 키는 카테고리 코드(M1_to_M7·M10·M16·M17). 식별자 키"),
    (re.compile(r"^/risk_levels/[^/]+$"), "enum_key", "risk_levels 의 키는 영문 열거 코드(very_low 등). pih_risk 값과 같은 코드 체계"),
]


def classify(rules, ptr):
    for rx, kind, why in rules:
        if rx.search(ptr):
            return kind, why
    return None, None


TEXT_KIND = [
    (re.compile(r"^/risk_levels/[^/]+$"), "numeric_range_text"),
    (re.compile(r"^/procedures/\d+/pih_rate$"), "numeric_range_text"),
]


def text_kind(ptr):
    for rx, k in TEXT_KIND:
        if rx.search(ptr):
            return k
    return "language_text"


# ---------------------------------------------------------------- 문장 단위 (문맥 보존용)
SENT_RX = re.compile(r"[^.]+?(?:\.(?=\s|$)|$)")


def sentences(text):
    """마침표+공백/끝 기준 분할. 소수점(1.5mm)은 뒤가 공백이 아니라 자르지 않는다."""
    out = []
    i = 0
    while i < len(text):
        m = re.compile(r"\.(\s+|$)").search(text, i)
        end = m.end(0) if m else len(text)
        stop = m.start(0) + 1 if m else len(text)
        seg = text[i:stop]
        lead = len(seg) - len(seg.lstrip())
        if seg.strip():
            out.append([i + lead, stop])
        i = end
    return out


def main():
    start_sha = sha256(SRC)
    if start_sha != EXPECTED_SHA:
        sys.exit(f"원본 해시 불일치: {start_sha}")
    raw_bytes = SRC.read_bytes()
    text = raw_bytes.decode("utf-8")
    doc = json.loads(text)
    sc = Scanner(text)
    sc.value("", None, None, 0)
    sc.ws()
    assert sc.i == len(text), "trailing data"
    b = cp_to_byte_table(text)
    segs = json.loads((HERE / "segments.json").read_text())["segments"]
    global MANUAL
    MANUAL = {s["id"]: json.loads((HERE / "manual" / f"{s['id']}.json").read_text())
              for s in segs if (HERE / "manual" / f"{s['id']}.json").exists()}

    for n in sc.nodes:
        n["byte"] = [b[n["cp"][0]], b[n["cp"][1]]]
        if n["type"] == "string":
            n["value_cp"] = [n["cp"][0] + 1, n["cp"][1] - 1]  # 따옴표 제외. 이스케이프 0 이라 디코딩 문자열 = 원문 구간
            n["value_byte"] = [b[n["value_cp"][0]], b[n["value_cp"][1]]]
        if "member_key" in n:
            mk = n["member_key"]["cp"]
            n["member_key"]["byte"] = [b[mk[0]], b[mk[1]]]
        n["leaf"] = n["type"] not in ("object", "array") or n["empty"]
        assert get_by_pointer(doc, n["pointer"]) == n.get("value", get_by_pointer(doc, n["pointer"]))
        own = segment_of(n["pointer"], segs)
        n["segment"] = own[0] if len(own) == 1 else own
        n["context"] = item_context(n["pointer"], doc)
    for k in sc.keys:
        k["byte"] = [b[k["cp"][0]], b[k["cp"][1]]]
        k["name_cp"] = [k["cp"][0] + 1, k["cp"][1] - 1]
        own = segment_of(k["member_pointer"], segs)
        k["segment"] = own[0] if len(own) == 1 else own

    source_map = {
        "source": {"path": SRC_REL, "sha256": start_sha, "bytes": len(raw_bytes),
                   "codepoints": len(text), "newlines": text.count("\n"),
                   "backslash_escapes": text.count("\\"), "duplicate_keys": sc.dupes,
                   "top_level_type": "object"},
        "units": {
            "cp": "디코딩 전 원문 파일 텍스트(UTF-8 디코딩 str)의 Unicode 코드포인트 인덱스 [start,end). JSON 리터럴 전체(문자열은 따옴표 포함)",
            "byte": "원문 파일 바이트 오프셋 [start,end)",
            "value_cp": "문자열 노드의 내용 구간(따옴표 제외) — 이 파일엔 이스케이프가 0개라 디코딩 값 == 원문 text[value_cp]",
            "member_key.cp": "객체 멤버의 키 리터럴(따옴표 포함) 구간",
            "pointer": "RFC 6901 JSON Pointer. 중복 키 0 이라 Pointer 만으로 유일",
        },
        "counts": {
            "nodes": len(sc.nodes),
            "by_type": {t: sum(1 for n in sc.nodes if n["type"] == t) for t in sorted({n["type"] for n in sc.nodes})},
            "leaves": sum(1 for n in sc.nodes if n["leaf"]),
            "empty_containers": sum(1 for n in sc.nodes if n["type"] in ("object", "array") and n["empty"]),
            "empty_strings": sum(1 for n in sc.nodes if n["type"] == "string" and n["empty"]),
            "key_occurrences": len(sc.keys),
            "distinct_keys": len({k["key"] for k in sc.keys}),
        },
        "nodes": sc.nodes,
        "keys": sc.keys,
    }

    # ------------------------------------------------ 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")
    TOK_OPTS = {"normalize_coda": False, "z_coda": True, "split_complex": False, "compatible_jamo": False, "saisiot": None}

    def analyze(s):
        toks = kiwi.tokenize(s, **TOK_OPTS)
        out = []
        for i, t in enumerate(toks):
            out.append({"i": i, "form": t.form, "tag": t.tag, "lemma": t.lemma,
                        "start": t.start, "end": t.start + t.len, "surface": s[t.start:t.start + t.len],
                        "word_position": t.word_position, "sent_position": t.sent_position,
                        "score": round(t.score, 4), "oov": bool(t.oov) if hasattr(t, "oov") else None})
        return out

    morph = []
    rid = 0
    for n in sc.nodes:
        if n["type"] != "string":
            if n["leaf"]:
                morph.append({"record_id": f"V{rid:04d}", "role": "value", "pointer": n["pointer"], "segment": n["segment"],
                              "applied": False, "exclusion": {"kind": "non_string" if not n["empty"] else "empty_container",
                                                             "reason": "문자열이 아닌 말단/빈 컨테이너 — 형태소 대상 아님(원문 보존)"}})
                rid += 1
            continue
        kind, why = classify(VALUE_EXCLUDE, n["pointer"])
        rec = {"record_id": f"V{rid:04d}", "role": "value", "pointer": n["pointer"], "segment": n["segment"],
               "text": n["value"], "value_cp": n["value_cp"]}
        rid += 1
        if kind:
            rec.update(applied=False, exclusion={"kind": kind, "reason": why})
        else:
            rec.update(applied=True, text_kind=text_kind(n["pointer"]), tokens=analyze(n["value"]))
        morph.append(rec)
    kid = 0
    for k in sc.keys:
        kind, why = classify(KEY_EXCLUDE, k["member_pointer"])
        rec = {"record_id": f"K{kid:04d}", "role": "field_name", "member_pointer": k["member_pointer"], "segment": k["segment"],
               "text": k["key"], "name_cp": k["name_cp"]}
        kid += 1
        if kind:
            rec.update(applied=False, exclusion={"kind": kind, "reason": why})
        else:
            rec.update(applied=True, tokens=analyze(k["key"]))
        morph.append(rec)

    segrev = {"_doc": "구획별 수동 기록(manual/S*.json 의 segmentation)을 모은 것. 원시 출력은 교정하지 않았다. status K=알려진 분석 한계(미교정)",
              "occurrences": []}
    _vals = {n["pointer"]: n for n in sc.nodes}
    for sid, sm in MANUAL.items():
        for x in sm.get("segmentation", []):
            ptr, txt, rawt, impact, st = x[:5]
            occ = x[5] if len(x) > 5 else 1
            v = _vals[ptr]["value"]
            pos = -1
            for _ in range(occ):
                pos = v.find(txt, pos + 1)
                if pos < 0:
                    sys.exit(f"오분절 기록 원문 불일치: {x}")
            segrev["occurrences"].append({"segment": sid, "pointer": ptr, "text": txt, "occurrence": occ,
                                          "span": [pos, pos + len(txt)], "file_cp": [_vals[ptr]["value_cp"][0] + pos, _vals[ptr]["value_cp"][0] + pos + len(txt)],
                                          "raw_tokens": rawt, "impact": impact, "status": st})
    morphology = {
        "source_sha256": start_sha,
        "analyzer": {"name": "kiwipiepy", "version": kiwipiepy.__version__, "model_type": "cong", "num_workers": 1,
                     "user_dictionary": None, "builtin_dictionary": "kiwipiepy_model 기본(설치된 패키지 내장)",
                     "tokenize_options": TOK_OPTS, "tagset": "Kiwi 품사 태그(세종 기반 + SL/SN/SH/SW 등)",
                     "lemma": "Kiwi Token.lemma 를 그대로 기록(동사·형용사는 '-다' 형). 도구가 준 값 외 기본형을 만들지 않았다",
                     "offsets": "start/end 는 분석에 넣은 문자열(=디코딩 값=원문 value_cp 구간)의 코드포인트 [start,end). 파일 위치 = value_cp[0]+start",
                     "surface": "원문 text[start:end]. form 과 다를 수 있다(예: ᆫ 어미는 앞 글자 구간을 공유)"},
        "policy": {"values_excluded": [{"pattern": rx.pattern, "kind": k, "reason": w} for rx, k, w in VALUE_EXCLUDE],
                   "keys_excluded": [{"pattern": rx.pattern, "kind": k, "reason": w} for rx, k, w in KEY_EXCLUDE],
                   "text_kind": "language_text 와 numeric_range_text(pih_rate·risk_levels 값) 를 구분. 숫자 범위 문자열도 분석은 적용하되 의미는 expressions 에서 원문 그대로 둔다",
                   "field_name_role": "role=field_name 은 스키마 키다. 언어 텍스트(role=value)와 섞어 세지 않는다",
                   "stopwords": "제거 없음 — 조사·어미·부사·접두 부정 모두 보존"},
        "segmentation_review": segrev,
        "counts": {"records": len(morph), "applied": sum(1 for r in morph if r["applied"]),
                   "excluded": sum(1 for r in morph if not r["applied"]),
                   "tokens": sum(len(r.get("tokens", [])) for r in morph)},
        "records": morph,
    }

    # ------------------------------------------------ 표현
    manual = {"facet_vocabulary": json.loads((HERE / "manual" / "facets.json").read_text()),
              "expressions": [dict(zip(("pointer", "text", "facets", "note", "status"), x[:5]), **({"occurrence": x[5]} if len(x) > 5 else {}))
                              for sm in MANUAL.values() for x in sm.get("expressions", [])]}
    nodes_by_ptr = {n["pointer"]: n for n in sc.nodes}
    exprs = []
    eid = 0
    for e in manual["expressions"]:
        n = nodes_by_ptr[e["pointer"]]
        v = n["value"]
        occ = e.get("occurrence", 1)
        pos = -1
        for _ in range(occ):
            pos = v.find(e["text"], pos + 1)
            if pos < 0:
                sys.exit(f"표현 원문 불일치: {e}")
        st, en = pos, pos + len(e["text"])
        sent = next(([a, z] for a, z in sentences(v) if a <= st and en <= z), None)
        exprs.append({"expr_id": f"E{eid:04d}", "method": "manual_reading", "pointer": e["pointer"],
                      "segment": n["segment"], "text": e["text"], "occurrence": occ,
                      "span_in_value": [st, en], "file_cp": [n["value_cp"][0] + st, n["value_cp"][0] + en],
                      "file_byte": [b[n["value_cp"][0] + st], b[n["value_cp"][0] + en]],
                      "sentence_span_in_value": sent, "sentence_text": v[sent[0]:sent[1]] if sent else None,
                      "full_value": v, "item_context": n["context"],
                      "facets": e["facets"], "note": e.get("note", ""), "status": e.get("status", "P")})
        eid += 1
    # 정규식 보조 후보 (수량·단위·범위) — 의미 해석 아님
    NUM_RX = re.compile(r"(?:[<>~]\s?)?\d+(?:\.\d+)?(?:\s?[-~]\s?\d+(?:\.\d+)?)?\s?(?:%|nm|mm|주|개월|J|)\+?")
    regex_cands = []
    for n in sc.nodes:
        if n["type"] != "string" or classify(VALUE_EXCLUDE, n["pointer"])[0]:
            continue
        for m in NUM_RX.finditer(n["value"]):
            if not re.search(r"\d", m.group(0)):
                continue
            st, en = m.span()
            covered = [x["expr_id"] for x in exprs if x["pointer"] == n["pointer"] and x["span_in_value"][0] <= st and en <= x["span_in_value"][1]]
            regex_cands.append({"cand_id": f"R{len(regex_cands):04d}", "method": "regex", "pattern": NUM_RX.pattern,
                                "pointer": n["pointer"], "segment": n["segment"], "text": m.group(0),
                                "span_in_value": [st, en], "file_cp": [n["value_cp"][0] + st, n["value_cp"][0] + en],
                                "covered_by_manual": covered})
    expressions = {
        "source_sha256": start_sha,
        "method": {"manual_reading": "원문을 구획별로 직접 읽으며 수동 기록(manual-expressions.json). facets 는 탐색 관점이지 확정 분류가 아니다",
                   "regex": "수량·단위·범위 후보를 찾는 보조 정규식. 의미 판정 아님. covered_by_manual 로 수동 기록과 대조",
                   "span": "span_in_value 는 디코딩 값의 코드포인트 [start,end). file_cp/file_byte 는 원문 파일 위치",
                   "overlap": "표현끼리 겹침은 의도된 것(전체 구절과 내부 수식어를 함께 보존). 같은 (pointer, span, facets) 중복은 오류로 verify 가 검사",
                   "status": "P=잠정 관찰 · F=후속 의미 조사 · B=원문 정보 부족 · I=원문 내 불일치 · K=알려진 분석 한계"},
        "facet_vocabulary": manual["facet_vocabulary"],
        "counts": {"manual": len(exprs), "regex_candidates": len(regex_cands),
                   "regex_uncovered": sum(1 for r in regex_cands if not r["covered_by_manual"])},
        "expressions": exprs,
        "regex_candidates": regex_cands,
    }

    # ------------------------------------------------ coverage
    rlog = {"segments": [dict(segment=sid, **{k: v for k, v in sm.items() if k not in ("expressions", "segmentation")}) for sid, sm in MANUAL.items()]}
    reads = {r["segment"]: r for r in rlog["segments"]}
    cov_segs = []
    for s in segs:
        owned = sorted([n["pointer"] for n in sc.nodes if n["segment"] == s["id"]], key=lambda p: nodes_by_ptr[p]["order"])
        leaves = [p for p in owned if nodes_by_ptr[p]["leaf"]]
        r = reads.get(s["id"], {})
        cov_segs.append({"id": s["id"], "title": s["title"], "pointer_prefixes": s["prefixes"], "owns_exact": s.get("owns_exact", []),
                         "context_refs": s["context_refs"], "owned_nodes": owned, "owned_leaf_pointers": leaves,
                         "owned_key_occurrences": [k["member_pointer"] for k in sc.keys if k["segment"] == s["id"]],
                         "machine_extracted": True, "direct_read": r.get("direct_read", False),
                         "read_status": r.get("status", "unread"), "last_read_pointer": r.get("last_read_pointer"),
                         "review_file": s["review_file"], "observations_count": len(r.get("observations", []))})
    coverage = {"source_sha256": start_sha, "all_leaf_pointers": [n["pointer"] for n in sc.nodes if n["leaf"]],
                "all_node_pointers": [n["pointer"] for n in sc.nodes],
                "status_legend": {"machine_extracted": "build.py 가 구간·값을 뽑았다(읽음 아님)",
                                  "direct_read": "에이전트가 구획 원문을 문맥과 함께 직접 읽고 reading-log.json 에 관찰을 남겼다"},
                "segments": cov_segs}

    for name, obj in [("source-map.json", source_map), ("morphology.json", morphology),
                      ("expressions.json", expressions), ("coverage.json", coverage)]:
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")

    write_reviews(doc, sc, segs, reads, exprs, morph, segrev, source_map, rlog)

    end_sha = sha256(SRC)
    assert end_sha == start_sha
    print(json.dumps({"start_sha": start_sha, "end_sha": end_sha, **source_map["counts"],
                      "morph": morphology["counts"], "expr": expressions["counts"]}, ensure_ascii=False))


# ---------------------------------------------------------------- 읽기용 문서
def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def jtype(n):
    return n["type"]


def write_reviews(doc, sc, segs, reads, exprs, morph, segrev, source_map, rlog):
    nodes = sc.nodes
    byp = {n["pointer"]: n for n in nodes}
    # 컬럼 구성 표: 경로 패턴별
    def pat(p):
        return re.sub(r"/procedures/\d+", "/procedures/{i}", re.sub(r"/risk_factors/\d+$", "/risk_factors/{j}", p))
    groups = {}
    for n in nodes:
        groups.setdefault(pat(n["pointer"]), []).append(n)
    rows = []
    for pt, ns in groups.items():
        types = sorted({n["type"] for n in ns})
        nest = ", ".join(sorted({f"{n['type']}[{n['child_count']}]" for n in ns if 'child_count' in n})) or "말단"
        ex = next((n for n in ns if n["type"] not in ("object", "array")), ns[0])
        exv = md(json.dumps(ex.get("value"), ensure_ascii=False)) if "value" in ex else "(컨테이너)"
        empties = sum(1 for n in ns if n["empty"])
        rows.append(f"| `{pt or '(root)'}` | {'/'.join(types)} | {nest} | {len(ns)} | {empties} | {exv} | `{ex['pointer'] or '(root)'}` |")
    seg_rows = []
    for s in segs:
        r = reads.get(s["id"], {})
        seg_rows.append(f"| {s['id']} | {s['title']} | {', '.join('`'+p+'`' for p in s.get('owns_exact', []) + s['prefixes'])} | "
                        f"{'직접 읽음' if r.get('direct_read') else '**미독**'} | `{r.get('last_read_pointer')}` | [{s['review_file']}](./{s['review_file']}) |")
    from collections import Counter
    key_orders = "; ".join(f"{' → '.join(k)} ×{c}" for k, c in Counter(tuple(p.keys()) for p in doc["procedures"]).items())
    rf_len = ", ".join(f"{k}개 {v}항목" for k, v in sorted(Counter(len(p["risk_factors"]) for p in doc["procedures"]).items()))
    risk_dist = ", ".join(f"{k} {v}" for k, v in Counter(p["pih_risk"] for p in doc["procedures"]).items())
    cat_dist = ", ".join(f"{k} {v}" for k, v in Counter(p["category"] for p in doc["procedures"]).items())
    CMP_NOTE = {0: "low 상한 5 와 맞닿음 — B2", 5: "**I1** 하한 10 이 high 범위 밖", 12: "**I2** ~1% 가 '< 1%' 경계"}
    cmp_rows = [f"| `/procedures/{i}` | {md(p['name'])} | {p['pih_risk']} | {md(doc['risk_levels'][p['pih_risk']])} | {md(p['pih_rate'])} | {CMP_NOTE.get(i, '범위 안')} |"
                for i, p in enumerate(doc["procedures"])]
    head = (HERE / "review-head.md").read_text() if (HERE / "review-head.md").exists() else ""
    c = source_map["counts"]
    out = [head,
           "## 원본\n",
           f"- 경로 `{source_map['source']['path']}` · sha256 `{source_map['source']['sha256']}` · {source_map['source']['bytes']} bytes · {source_map['source']['codepoints']} 코드포인트 · 줄바꿈 {source_map['source']['newlines']} · 백슬래시 이스케이프 {source_map['source']['backslash_escapes']} · 중복 키 {len(source_map['source']['duplicate_keys'])}",
           f"- 노드 {c['nodes']} ({', '.join(f'{k} {v}' for k, v in c['by_type'].items())}) · 말단 {c['leaves']} · 빈 컨테이너 {c['empty_containers']} · 빈 문자열 {c['empty_strings']} · 키 출현 {c['key_occurrences']} (서로 다른 키 {c['distinct_keys']})\n",
           "## 컬럼 구성 표 (원본 컬럼명/경로 패턴 그대로)\n",
           "`{i}` = procedures 배열 인덱스 0–25, `{j}` = risk_factors 배열 인덱스. 원문 예시는 해당 패턴의 첫 출현.\n",
           "| 원본 경로 패턴 | 자료형 | 중첩(컨테이너[자식수]) | 출현 수 | 빈 값 | 원문 예시 | 예시 위치 |", "|---|---|---|---|---|---|---|", *rows, "",
           "## 키 구성의 변형\n",
           f"- procedures 26 항목의 키 순서: {key_orders}",
           "- 선택적 필드: 없음(26 항목 모두 9 키). 빈 문자열·빈 배열·빈 객체·null: 0. 숫자·불리언 말단: 0(수치는 모두 문자열 — 예 `\"~5%\"`, `\"1.0\"`).",
           f"- risk_factors 길이 분포: {rf_len}",
           f"- 열거/코드 값 분포 — pih_risk: {risk_dist} · category: {cat_dist}\n",
           "## 대조 — pih_risk · pih_rate · risk_levels (원문 값 / 잠정 관찰 분리)\n",
           "| Pointer | name (원문) | pih_risk (원문) | risk_levels[pih_risk] (원문) | pih_rate (원문) | 잠정 관찰 |", "|---|---|---|---|---|---|", *cmp_rows, "",
           "## 구획 목차 (모든 값은 구획 파일에 원본 컬럼명 그대로 실림)\n",
           "| 구획 | 범위 | 소유 Pointer | 읽기 상태 | 마지막 읽은 Pointer | 파일 |", "|---|---|---|---|---|---|", *seg_rows, ""]
    (HERE / "review.md").write_text("\n".join(out) + "\n")

    exprs_by_ptr = {}
    for e in exprs:
        exprs_by_ptr.setdefault(e["pointer"], []).append(e)
    for s in segs:
        r = reads.get(s["id"], {})
        owned = [n for n in nodes if n["segment"] == s["id"]]
        L = [f"# {s['id']} — {s['title']}\n", f"[← review.md 목차](./review.md)\n",
             f"- 읽기 상태: {'직접 읽음' if r.get('direct_read') else '**미독**'} · 마지막 읽은 Pointer `{r.get('last_read_pointer')}`",
             f"- 공동 참조 문맥(소유 아님): {', '.join('`'+x+'`' for x in s['context_refs']) or '없음'}\n",
             "## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)\n",
             "원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.\n",
             "| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |", "|---|---|---|---|---|---|"]
        for n in owned:
            k = n["key_or_index"]
            kname = "(root)" if n["pointer"] == "" else (f"[{k}]" if isinstance(k, int) else k)
            if n["type"] in ("object", "array"):
                val = f"({n['type']}, 자식 {n['child_count']})"
            else:
                val = md(json.dumps(n["value"], ensure_ascii=False))
            eids = ", ".join(e["expr_id"] for e in exprs_by_ptr.get(n["pointer"], []))
            L.append(f"| `{n['pointer'] or '(root)'}` | {md(kname)} | {n['type']} | {val} | {n['cp'][0]}–{n['cp'][1]} | {eids} |")
        L += ["", "## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)\n"]
        obs = r.get("observations", [])
        if obs:
            L += ["| # | 상태 | 근거 Pointer | 관찰 |", "|---|---|---|---|"]
            for i, o in enumerate(obs, 1):
                L.append(f"| {i} | {o['status']} | {', '.join('`'+p+'`' for p in o['pointers'])} | {md(o['text'])} |")
        else:
            L.append("(관찰 기록 없음)")
        L += ["", "## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)\n",
              "| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |", "|---|---|---|---|---|---|---|"]
        for e in exprs:
            if e["segment"] == s["id"]:
                L.append(f"| {e['expr_id']} | `{e['pointer']}` | {md(e['text'])} | {e['span_in_value'][0]}–{e['span_in_value'][1]} | {', '.join(e['facets'])} | {e['status']} | {md(e['note'])} |")
        L += ["", "## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)\n"]
        occ = [o for o in segrev.get("occurrences", []) if o.get("segment") == s["id"]]
        if occ:
            L += ["| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |", "|---|---|---|---|---|"]
            for o in occ:
                L.append(f"| `{o['pointer']}` | {md(o['text'])} [{o['span'][0]},{o['span'][1]}) | {md(o['raw_tokens'])} | {md(o['impact'])} | {o['status']} |")
        else:
            L.append("(이 구획에 기록된 출현 없음)")
        L += ["", "## 5. 미결 (이 구획)\n"]
        opn = r.get("open", [])
        L += [f"- {x}" for x in opn] if opn else ["(없음)"]
        (HERE / s["review_file"]).write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
