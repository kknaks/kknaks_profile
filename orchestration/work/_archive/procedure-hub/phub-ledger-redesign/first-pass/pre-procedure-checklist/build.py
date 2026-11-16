#!/usr/bin/env python3
"""pre-procedure-checklist.json 1차 수집 재현 스크립트.

레포 루트에서:
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/pre-procedure-checklist/build.py

원본은 읽기만 한다. 쓰기는 이 스크립트가 있는 폴더 안뿐이다.
수동 기록(manual/segment-notes.json)은 읽기만 하고, 생성물에 합쳐 넣는다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SRC = ROOT / "orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json"
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json"
NOTES = HERE / "manual/segment-notes.json"

SPAN_DOC = ("span 단위: 'cp' = 디코딩된 원본 파일 전체 문자열(UTF-8 디코딩)의 Unicode 코드포인트 인덱스 [start,end), "
            "'byte' = 원본 파일 바이트 오프셋 [start,end). literal_* = JSON 리터럴(따옴표 포함) 구간. "
            "value_cp_in_file = 문자열 값 내용(따옴표 제외) 구간 — 이 원본에는 이스케이프가 0개라 디코딩 값과 리터럴 내부가 1:1 이다. "
            "value_offsets = 디코딩된 값 문자열 내부의 코드포인트 [start,end).")


# ---------------------------------------------------------------- JSON 스캐너
class Scanner:
    """중복 키 감지·리터럴 구간 기록용 최소 JSON 스캐너. 값은 json.loads 로 재확인한다."""

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.dup_keys = []
        self.escapes = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\n\r":
            self.i += 1

    def string(self):
        s = self.i
        assert self.t[s] == '"'
        j = s + 1
        esc = False
        while True:
            c = self.t[j]
            if c == "\\":
                esc = True
                j += 2
                continue
            if c == '"':
                break
            j += 1
        self.i = j + 1
        lit = self.t[s:self.i]
        return s, self.i, json.loads(lit), esc

    def value(self, ptr, parent, key, index, key_span):
        self.ws()
        s = self.i
        c = self.t[s]
        rec = {"pointer": ptr, "parent": parent, "key": key, "index": index, "key_literal_cp": key_span}
        self.nodes.append(rec)
        if c == "{":
            rec["json_type"] = "object"
            self.i += 1
            seen = {}
            n = 0
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    ks, ke, k, kesc = self.string()
                    if kesc:
                        self.escapes.append({"where": "key", "cp": [ks, ke]})
                    if k in seen:
                        self.dup_keys.append({"object": ptr, "key": k, "first_cp": seen[k], "dup_cp": [ks, ke]})
                    seen[k] = [ks, ke]
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    cptr = ptr + "/" + k.replace("~", "~0").replace("/", "~1")
                    self.value(cptr, ptr, k, None, [ks, ke])
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            rec["child_count"] = n
            rec["keys_in_order"] = list(seen.keys())
        elif c == "[":
            rec["json_type"] = "array"
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(f"{ptr}/{n}", ptr, None, n, None)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            rec["child_count"] = n
        elif c == '"':
            ss, se, v, esc = self.string()
            rec["json_type"] = "string"
            rec["value"] = v
            rec["has_escape"] = esc
            if esc:
                self.escapes.append({"where": "value", "pointer": ptr, "cp": [ss, se]})
        else:
            m = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(self.t, s)
            lit = m.group(0)
            self.i = m.end()
            v = json.loads(lit)
            rec["json_type"] = "null" if v is None else ("boolean" if isinstance(v, bool) else "number")
            rec["value"] = v
        rec["literal_cp"] = [s, self.i]
        return rec


def ptr_get(doc, ptr):
    if ptr == "":
        return doc
    cur = doc
    for part in ptr[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def owner_of(ptr, segments):
    hits = []
    for seg in segments:
        ok = False
        for p in seg["owns_prefixes"]:
            if p in seg.get("owns_exact_only", []) or p == "":
                if ptr == p:
                    ok = True
            elif ptr == p or ptr.startswith(p + "/"):
                ok = True
        if ok:
            hits.append(seg["id"])
    return hits


# ---------------------------------------------------------------- 분석 대상 분류
CODE_RULES = [
    (re.compile(r"^/version$"), "excluded", "버전 코드값(문자열 '1.1') — 언어 텍스트 아님"),
    (re.compile(r"^/updated$"), "excluded", "날짜 코드값(YYYY-MM-DD) — 언어 텍스트 아님"),
    (re.compile(r"^/universal_checks/\d+/id$"), "excluded", "영문 snake_case 식별자 — ID/코드값. 라벨·설명과 함께 원문 보존"),
    (re.compile(r"^/universal_checks/\d+/type$"), "excluded", "영문 snake_case 유형 코드(enum 형태) — 코드값. 정의는 원문에 없음(issues 참조)"),
    (re.compile(r"^/category_specific/\d+/id$"), "excluded", "카테고리 코드(M1…M17) — ID/코드값"),
    (re.compile(r"^/category_specific/\d+/checks/\d+/type$"), "excluded", "영문 snake_case 유형 코드(enum 형태) — 코드값"),
    (re.compile(r"^/description$"), "analyzed", "언어 텍스트(원장 설명, 한국어+영문 혼합)"),
    (re.compile(r"^/universal_checks/\d+/(label|description)$"), "analyzed", "언어 텍스트(한국어+영문·숫자 혼합)"),
    (re.compile(r"^/category_specific/\d+/name$"), "analyzed", "언어 텍스트(카테고리 이름, 한국어+영문 혼합)"),
    (re.compile(r"^/category_specific/\d+/checks/\d+/label$"), "analyzed", "언어 텍스트(확인 항목 문구, 한국어+영문·숫자 혼합)"),
]


def classify(ptr):
    for rx, st, why in CODE_RULES:
        if rx.match(ptr):
            return st, why
    return None, None


# ---------------------------------------------------------------- 자동 표현 후보 패턴
AUTO_PATTERNS = [
    ("AP-NUM-UNIT", r"\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)?\s*(?:mg|%|개월|주|일|시간|년)", "숫자(+범위)+단위"),
    ("AP-RANGE", r"\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?|\b[IVX]+-[IVX]+\b", "하이픈 수치/로마숫자 범위"),
    ("AP-MULT", r"x\d+", "x+숫자 표기"),
    ("AP-YEAR", r"(?<!\d)(?:19|20)\d{2}(?!\d)", "연도 형태 4자리"),
    ("AP-PAREN", r"\([^()]*\)", "괄호 안 구절"),
    ("AP-SLASH", r"[^\s/(),—]+(?:/[^\s/(),—]+)+", "슬래시 나열"),
    ("AP-DASH", r"—[^—]*$", "줄표(—) 뒤 구절"),
    ("AP-ALT", r"\bvs\b|\bor\b|또는", "대안·비교 접속(vs/or/또는)"),
    ("AP-NEG", r"불가|아닌|아니|않|금기|제한|없|비(?=HA|박리성|녹는)|무감각", "부정·금지·제한 어휘"),
    ("AP-POSS", r"수 있|가능성|가능|위험|어려움|예측 불가", "가능성·위험 어휘"),
    ("AP-COND", r"(?<=[가-힣A-Za-z\)]) 시(?=[ ,)\s]|$)|경우|이내|이후|후(?=[ )]|$)|전부터|전(?=\))|중인|중이거나|중단|대기|하에|따라|병행", "조건·시점 어휘"),
    ("AP-MODAL", r"필수|필요|반드시|원칙|고려|판단|상의|확인|준비|안내|설명|고지|평가", "권고·의무·행위 어휘"),
    ("AP-DEGREE", r"최소|최근|대폭|특히|충분한|과도한|고용량|중등도 이상|점진적|더|크게|장시간|일부|대부분|개인차|조기|사전|고위험군|이상", "정도·범위·근사 어휘"),
    ("AP-ETC", r"(?<=[가-힣A-Za-z0-9]) 등(?=[ )—,]|$)", "열린 나열 '등'"),
]


def main():
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + len(ch.encode("utf-8")))
    doc = json.loads(text)
    sc = Scanner(text)
    sc.value("", None, None, None, None)
    sc.ws()
    assert sc.i == len(text), "trailing data"
    notes = json.loads(NOTES.read_text(encoding="utf-8"))
    segs = notes["segments"]
    seg_by_id = {s["id"]: s for s in segs}

    nodes = sc.nodes
    for n in nodes:
        s, e = n["literal_cp"]
        n["literal_byte"] = [cum[s], cum[e]]
        if n["key_literal_cp"]:
            ks, ke = n["key_literal_cp"]
            n["key_literal_byte"] = [cum[ks], cum[ke]]
        if n["json_type"] == "string":
            n["value_cp_in_file"] = [s + 1, e - 1]
        n["is_leaf"] = n["json_type"] not in ("object", "array")
        n["is_empty_container"] = (not n["is_leaf"]) and n["child_count"] == 0
        if n["json_type"] == "string" and n["value"] == "":
            n["is_empty_string"] = True
        own = owner_of(n["pointer"], segs)
        n["segment"] = own[0] if len(own) == 1 else own
        # 문맥 참조
        p = n["pointer"]
        m = re.match(r"^/universal_checks/(\d+)", p)
        ctx = {}
        if m:
            it = doc["universal_checks"][int(m.group(1))]
            ctx = {"item_pointer": f"/universal_checks/{m.group(1)}", "item.id": it.get("id"), "item.label": it.get("label")}
        m = re.match(r"^/category_specific/(\d+)(?:/checks/(\d+))?", p)
        if m:
            cat = doc["category_specific"][int(m.group(1))]
            ctx = {"category_pointer": f"/category_specific/{m.group(1)}", "category.id": cat.get("id"), "category.name": cat.get("name")}
            if m.group(2) is not None:
                ctx["check_pointer"] = f"/category_specific/{m.group(1)}/checks/{m.group(2)}"
                ctx["check.label"] = cat["checks"][int(m.group(2))].get("label")
                ctx["check.type"] = cat["checks"][int(m.group(2))].get("type")
        if ctx:
            n["context"] = ctx

    # ---- source-map.json
    key_occ = {}
    for n in nodes:
        if n["key"] is not None:
            key_occ.setdefault(n["key"], []).append(n["pointer"])
    source_map = {
        "source": {"path": SRC_REL, "bytes": len(raw), "sha256": sha, "codepoints": len(text),
                   "encoding": "utf-8", "bom": raw[:3] == b"\xef\xbb\xbf", "trailing_newline": raw.endswith(b"\n"),
                   "lines": text.count("\n") + 1},
        "span_units": SPAN_DOC,
        "duplicate_keys": sc.dup_keys,
        "escapes": sc.escapes,
        "counts": {
            "nodes": len(nodes),
            "leaves": sum(1 for n in nodes if n["is_leaf"]),
            "objects": sum(1 for n in nodes if n["json_type"] == "object"),
            "arrays": sum(1 for n in nodes if n["json_type"] == "array"),
            "empty_containers": sum(1 for n in nodes if n["is_empty_container"]),
            "empty_strings": sum(1 for n in nodes if n.get("is_empty_string")),
            "nulls": sum(1 for n in nodes if n["json_type"] == "null"),
            "by_type": {t: sum(1 for n in nodes if n["json_type"] == t) for t in ["object", "array", "string", "number", "boolean", "null"]},
        },
        "field_name_occurrences": {k: {"count": len(v), "pointers": v} for k, v in key_occ.items()},
        "nodes": nodes,
    }
    (HERE / "source-map.json").write_text(json.dumps(source_map, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- morphology.json
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")
    known = notes.get("morph_known_errors", [])
    # 오분절 출현 구간(span) = 디코딩된 값 문자열의 코드포인트 [start,end). 수동 기록에 있고 여기서 재현을 확인한다.
    for k in known:
        kv = ptr_get(doc, k["pointer"])
        if "span" not in k or kv[k["span"][0]:k["span"][1]] != k["surface"] or kv.count(k["surface"]) != 1:
            raise SystemExit(f"known_error span 재현 실패 {k['pointer']} {k['surface']}")
    records, excluded, field_names = [], [], []
    for n in nodes:
        if n["json_type"] != "string":
            continue
        st, why = classify(n["pointer"])
        if st is None:
            raise SystemExit(f"unclassified string leaf {n['pointer']}")
        if st == "excluded":
            excluded.append({"pointer": n["pointer"], "value": n["value"], "reason": why, "segment": n["segment"]})
            continue
        v = n["value"]
        toks = []
        for t in kiwi.tokenize(v):
            s, e = t.start, t.start + t.len
            shared = bool(toks) and s < toks[-1]["end"]
            toks.append({"span_shared_with_prev": shared, "form": t.form, "tag": t.tag, "lemma_tool": t.lemma, "start": s, "end": e,
                         "surface": v[s:e], "surface_equals_form": v[s:e] == t.form,
                         "file_cp": [n["value_cp_in_file"][0] + s, n["value_cp_in_file"][0] + e]})
        sents = [{"text": x.text, "start": x.start, "end": x.end} for x in kiwi.split_into_sents(v)]
        ke = [k for k in known if k["pointer"] == n["pointer"]]
        records.append({"pointer": n["pointer"], "segment": n["segment"], "reason": why, "text": v,
                        "value_cp_in_file": n["value_cp_in_file"], "sentences": sents, "tokens": toks,
                        "known_errors": ke})
    for k, ptrs in key_occ.items():
        toks = [{"form": t.form, "tag": t.tag, "lemma_tool": t.lemma, "start": t.start, "end": t.start + t.len,
                 "surface": k[t.start:t.start + t.len]} for t in kiwi.tokenize(k)]
        field_names.append({"field_name": k, "role": "field_name(구조 키) — 언어 텍스트와 별도 기록",
                            "occurrences": len(ptrs), "occurrence_pointers": ptrs, "tokens": toks,
                            "note": "영문 snake_case 식별자. kiwi 는 SL(외국어) 토큰으로만 나눈다 — 영어 형태 분석 아님"})
    morph = {
        "analyzer": {"name": "kiwipiepy", "version": kiwipiepy.__version__, "python": sys.version.split()[0],
                     "model_type": "cong", "num_workers": 1, "user_dictionary": None,
                     "options": "Kiwi(num_workers=1, model_type='cong'); tokenize(text) 기본값(정규화·typo 교정 없음, split_complex 기본); split_into_sents 기본",
                     "dictionary": "kiwipiepy 0.24.1 내장 기본 사전(kiwipiepy_model 동봉), 사용자 사전 없음",
                     "tagset": "Kiwi 세종 확장 품사 체계(NNG,NNP,NNB,SL,SN,SW,SSO,SSC,SP,SO,JX,JKO,…)",
                     "lemma_note": "lemma_tool 은 kiwipiepy Token.lemma 값 그대로(도구 제공). 에이전트가 기본형을 만들지 않았다",
                     "offset_note": "start/end = 디코딩된 값 문자열의 코드포인트 [start,end) (kiwi Token.start/len). file_cp = 원본 디코딩 전체 문자열 기준. 한 음절이 둘 이상의 형태소로 분석되면(예: 인→이/VCP+ᆫ/ETM, 져→지+어) kiwi 가 같은 구간을 겹쳐 준다 — span_shared_with_prev=true 로 표시하고 그대로 둔다(surface≠form)"},
        "language_note": "원문은 한국어 본문에 영문 약어·영단어(NOAC, NSAIDs, AAD Task Force, ablative, Fitzpatrick, PIH, RF/HIFU, HA, PMMA, BMI, PAH, G6PD, MTS, HIFES/EMS, mg, or, vs)가 섞여 있다. kiwi 는 영문을 SL 토큰으로만 보존하며 영어 형태소 분석은 하지 않는다(K 한계). 다른 언어(한자·일본어 등)는 없다.",
        "records": records,
        "excluded": excluded,
        "field_names": field_names,
        "known_errors": known,
    }
    (HERE / "morphology.json").write_text(json.dumps(morph, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- expressions.json
    auto = []
    for r in records:
        v = r["text"]
        for pid, rx, desc in AUTO_PATTERNS:
            for m in re.finditer(rx, v):
                auto.append({"pattern": pid, "pointer": r["pointer"], "segment": r["segment"], "match": m.group(0),
                             "start": m.start(), "end": m.end(),
                             "file_cp": [r["value_cp_in_file"][0] + m.start(), r["value_cp_in_file"][0] + m.end()],
                             "context_value": v})
    manual = []
    leaf_by_ptr = {n["pointer"]: n for n in nodes}
    for seg in segs:
        for ex in seg["manual_expressions"]:
            n = leaf_by_ptr[ex["pointer"]]
            v = n["value"]
            occ = ex.get("occurrence", 0)
            pos = -1
            for _ in range(occ + 1):
                pos = v.find(ex["text"], pos + 1)
            if pos < 0:
                raise SystemExit(f"manual expression not found: {ex}")
            manual.append(dict(ex, segment=seg["id"], start=pos, end=pos + len(ex["text"]),
                               file_cp=[n["value_cp_in_file"][0] + pos, n["value_cp_in_file"][0] + pos + len(ex["text"])],
                               context_value=v))
    expr = {
        "method": {
            "auto": "AUTO_PATTERNS 정규식(build.py)에 실제로 일치한 구간뿐이다. 패턴 밖 표현은 이 목록에 없다 — 전수 의미 해석이 아니다.",
            "manual": "구획별 직접 읽기에서 수집한 구절(manual/segment-notes.json). perspectives 는 탐색 관점 태그이며 확정 분류가 아니다. 겹침은 의도된 것이다(전체 구절과 하위 구절을 함께 보존).",
            "patterns": [{"id": p, "regex": rx, "desc": d} for p, rx, d in AUTO_PATTERNS],
            "offsets": "start/end = 디코딩된 값 문자열 코드포인트 [start,end); file_cp = 원본 전체 디코딩 문자열 기준",
        },
        "auto_candidates": auto,
        "manual_expressions": manual,
    }
    (HERE / "expressions.json").write_text(json.dumps(expr, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- coverage.json
    cov_segs = []
    for seg in segs:
        owned = [n["pointer"] for n in nodes if n["segment"] == seg["id"]]
        leaves = [n["pointer"] for n in nodes if n["segment"] == seg["id"] and n["is_leaf"]]
        cov_segs.append({
            "id": seg["id"], "title": seg["title"], "owns_prefixes": seg["owns_prefixes"],
            "owns_exact_only": seg.get("owns_exact_only", []), "context_refs": seg["context_refs"],
            "pointer_range": [owned[0], owned[-1]] if owned else None,
            "owned_pointers": owned, "owned_leaf_pointers": leaves,
            "owned_counts": {"nodes": len(owned), "leaves": len(leaves)},
            "machine_extraction": "done(build.py: source-map·morphology·expressions)",
            "direct_reading": seg["read_status"],
            "read_by": seg.get("read_by"), "read_note": seg.get("read_note"),
            "review_file": f"review-part-{seg['id']}.md",
        })
    coverage = {"source_sha256": sha, "source_path": SRC_REL,
                "status_values": {"planned": "계획만 — 미독", "read": "직접 읽기 완료 + 관찰 기록"},
                "ownership_rule": "pointer == prefix 또는 prefix+'/' 로 시작하면 소유. owns_exact_only 는 정확 일치만. 컨테이너·말단 모든 노드가 정확히 한 구획에 속해야 한다(verify.py).",
                "segments": cov_segs}
    (HERE / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- review parts
    rec_by_ptr = {r["pointer"]: r for r in records}
    auto_by_ptr = {}
    for a in auto:
        auto_by_ptr.setdefault(a["pointer"], []).append(a)

    def esc(s):
        return str(s).replace("|", "\\|").replace("\n", " ")

    def val_cell(n):
        if n["json_type"] == "string":
            return esc(n["value"])
        return esc(json.dumps(n["value"], ensure_ascii=False))

    for seg in segs:
        L = [f"# review-part-{seg['id']} — {seg['title']}", "",
             f"- 원본: `{SRC_REL}` (sha256 `{sha}`)",
             f"- 직접 읽기 상태: **{seg['read_status']}**" + (f" — {seg.get('read_note')}" if seg.get("read_note") else ""),
             f"- 소유 Pointer: {', '.join('`'+p+'`' for p in seg['owns_prefixes'])}" + (" (정확 일치만: " + ", ".join('`'+p+'`' for p in seg.get('owns_exact_only', [])) + ")" if seg.get('owns_exact_only') else ""),
             f"- 공동 참조 문맥(소유 아님): {', '.join('`'+p+'`' for p in seg['context_refs']) or '없음'}",
             "- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.", "",
             "## 원문 값 (원본 컬럼명 그대로, 원본 순서)", ""]
        owned = [n for n in nodes if n["segment"] == seg["id"]]
        L += ["| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |",
              "|---|---|---|---|---|---|"]
        for n in owned:
            name = n["key"] if n["key"] is not None else (f"[{n['index']}]" if n["index"] is not None else "(root)")
            if n["is_leaf"]:
                st, why = classify(n["pointer"]) if n["json_type"] == "string" else ("excluded", "비문자열")
                r = rec_by_ptr.get(n["pointer"])
                tk = " ".join(f"{t['form']}/{t['tag']}" for t in r["tokens"]) if r else "—"
                L.append(f"| `{n['pointer']}` | `{name}` | {n['json_type']} | {val_cell(n)} | {st} | {esc(tk)} |")
            else:
                extra = f"keys={n.get('keys_in_order')}" if n["json_type"] == "object" else ""
                L.append(f"| `{n['pointer'] or '(root)'}` | `{name}` | {n['json_type']}(자식 {n['child_count']}) | {esc(extra)} | — | — |")
        L += ["", "## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)", ""]
        cnt = {}
        for n in owned:
            for a in auto_by_ptr.get(n["pointer"], []):
                cnt.setdefault(a["pattern"], []).append(f"`{a['pointer']}`[{a['start']},{a['end']}) «{esc(a['match'])}»")
        if cnt:
            for pid in [p for p, _, _ in AUTO_PATTERNS if p in cnt]:
                L.append(f"- **{pid}** ({len(cnt[pid])}): " + "; ".join(cnt[pid]))
        else:
            L.append("- 없음")
        L += ["", "## 수동 수집 표현 (직접 읽기 — 원문 구간)", ""]
        if seg["manual_expressions"]:
            L += ["| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |", "|---|---|---|---|---|"]
            for ex in [m for m in manual if m["segment"] == seg["id"]]:
                L.append(f"| `{ex['pointer']}` | [{ex['start']},{ex['end']}) | {esc(ex['text'])} | {esc(', '.join(ex.get('perspectives', [])))} | {esc(ex.get('note', ''))} |")
        else:
            L.append("- (아직 없음)")
        L += ["", "## 잠정 관찰 (원문 아님 — 근거 위치 포함)", ""]
        L += [f"- {o}" for o in seg["observations"]] or ["- (아직 없음)"]
        L += ["", "## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)", ""]
        L += [f"- **{i['code']}-{i['id']}** [{i['status']}] {i['text']} — 위치: {', '.join('`'+p+'`' for p in i.get('pointers', []))}" for i in seg["issues"]] or ["- (아직 없음)"]
        ke = [k for k in known if any(k["pointer"] == n["pointer"] for n in owned)]
        L += ["", "## 알려진 형태소 오분절 (K — 출현별)", ""]
        L += [f"- `{k['pointer']}` «{esc(k['surface'])}» → 원시 `{esc(k['raw_tokens'])}` — 영향: {esc(k['impact'])}" for k in ke] or ["- 없음(직접 대조에서 기록할 것 없음)" if seg["read_status"] == "read" else "- (미대조)"]
        (HERE / f"review-part-{seg['id']}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- review.md (목차·상태·컬럼 구성)
    patterns = {}
    for n in nodes:
        pat = re.sub(r"/\d+", "/*", n["pointer"]) or "(root)"
        d = patterns.setdefault(pat, {"types": set(), "count": 0, "example": None, "example_ptr": None, "empty": 0, "parents": set()})
        d["types"].add(n["json_type"] + (f"(자식 {n['child_count']})" if not n["is_leaf"] and pat.endswith("checks") else ""))
        d["count"] += 1
        if n["is_leaf"] and d["example"] is None:
            d["example"], d["example_ptr"] = n["value"], n["pointer"]
        if n.get("is_empty_string") or n["is_empty_container"]:
            d["empty"] += 1
    # 선택적 필드 확인: 같은 부모 패턴 객체 중 해당 키가 없는 경우
    obj_pats = {}
    for n in nodes:
        if n["json_type"] == "object":
            pat = re.sub(r"/\d+", "/*", n["pointer"]) or "(root)"
            obj_pats.setdefault(pat, []).append(n["keys_in_order"])
    optional = []
    for pat, ks in obj_pats.items():
        allk = set().union(*map(set, ks))
        for k in sorted(allk):
            miss = sum(1 for kk in ks if k not in kk)
            if miss:
                optional.append(f"`{pat}/{k}` 누락 {miss}/{len(ks)}")
        orders = {tuple(k) for k in ks}
        obj_pats[pat] = (len(ks), orders)
    st_all = all(s["read_status"] == "read" for s in segs)
    R = ["# pre-procedure-checklist.json — 1차 수집 review", "",
         "## 상태", "",
         f"- **1차 범위 종료: {'예' if st_all and notes.get('first_pass_closed') else '아니오(진행 중)'}** · **원장 전체 완료 아님**(의미 조사·공통 모델·관계 확정은 후속 단계)",
         f"- 전수 읽기: {sum(1 for s in segs if s['read_status']=='read')}/{len(segs)} 구획 직접 읽기 완료",
         f"- 구조·값 수집: 노드 {len(nodes)} · 말단 {source_map['counts']['leaves']} · 객체 {source_map['counts']['objects']} · 배열 {source_map['counts']['arrays']} · 빈 컨테이너 {source_map['counts']['empty_containers']} · 빈 문자열 {source_map['counts']['empty_strings']} · null {source_map['counts']['nulls']} · 중복 키 {len(sc.dup_keys)} · 이스케이프 {len(sc.escapes)}",
         f"- 형태소·표현 수집: kiwi 적용 문자열 {len(records)} · 제외 {len(excluded)}(코드값) · 필드명 {len(field_names)}종 별도 · 자동 후보 {len(auto)}(정규식 일치분만) · 수동 표현 {len(manual)}",
         "- 기계 검증 / 읽기 검토 / 미결: [validation.md](validation.md) · [issues.md](issues.md) · 재개: [progress.md](progress.md)",
         "",
         "## 원본", "",
         f"- 경로 `{SRC_REL}` · {len(raw)} bytes · {len(text)} codepoints · sha256 `{sha}` · UTF-8, BOM 없음, 한 줄(끝 개행 없음), 이스케이프 0, 중복 키 0",
         "",
         "## 컬럼 구성 표 (경로 패턴별, 원본 컬럼명 그대로)", "",
         "| 원본 컬럼명/경로 패턴 | 자료형·중첩 | 출현 수 | 빈 값 수 | 원문 예시 | 예시 위치 |", "|---|---|---|---|---|---|"]
    for pat, d in patterns.items():
        ex = esc(d["example"]) if d["example"] is not None else "(컨테이너)"
        R.append(f"| `{pat}` | {esc(', '.join(sorted(d['types'])))} | {d['count']} | {d['empty']} | {ex} | `{d['example_ptr'] or '—'}` |")
    R += ["", "### 객체 형태 변형·선택적 필드", ""]
    for pat, (cnt_, orders) in obj_pats.items():
        R.append(f"- `{pat}` 객체 {cnt_}개 · 키 순서 변형 {len(orders)}종: " + " / ".join("[" + ", ".join(o) + "]" for o in orders))
    R.append("- 선택적 필드(같은 패턴 객체 중 일부에만 있는 키): " + ("; ".join(optional) if optional else "없음 — 같은 패턴의 객체는 모두 같은 키 집합"))
    R.append("- 구조 차이(원문 사실): `universal_checks/*` 는 id·label·type·description 4키, `category_specific/*/checks/*` 는 label·type 2키(id·description 없음).")
    types = {}
    for n in nodes:
        if n["key"] == "type":
            types.setdefault(n["value"], []).append(n["pointer"])
    R += ["", "### `type` 값 분포 (코드값 — 뜻은 원문에 정의 없음)", "",
          "| type 원문 값 | universal_checks | category_specific checks |", "|---|---|---|"]
    for t, ps in types.items():
        R.append(f"| `{t}` | {sum(1 for p in ps if p.startswith('/universal'))} | {sum(1 for p in ps if p.startswith('/category'))} |")
    R += ["", "## 구획 목차", "", "| 구획 | 범위 | 소유 노드/말단 | 직접 읽기 | 파일 |", "|---|---|---|---|---|"]
    for c in cov_segs:
        R.append(f"| {c['id']} | {esc(c['title'])} | {c['owned_counts']['nodes']}/{c['owned_counts']['leaves']} | {c['direct_reading']} | [review-part-{c['id']}.md](review-part-{c['id']}.md) |")
    R += ["", "## 구조화 기록", "",
          "- `source-map.json` — 모든 노드(컨테이너·말단) Pointer·자료형·원문 값·리터럴 구간(cp/byte)·키 구간·문맥 참조·소유 구획",
          "- `morphology.json` — 분석 설정, 문자열별 kiwi 원시 토큰(form/tag/lemma_tool/구간), 문장 분리, 제외 목록(사유), 필드명 별도, 알려진 오분절",
          "- `expressions.json` — 자동 후보(정규식 일치분만)와 수동 수집 표현(직접 읽기)",
          "- `coverage.json` — 구획별 소유 Pointer 집합·읽기 상태·대응 review 파일",
          ]
    (HERE / "review.md").write_text("\n".join(R) + "\n", encoding="utf-8")

    # ---- issues.md
    I = ["# issues — pre-procedure-checklist.json 1차 미결", "",
         "코드: **A**=에이전트 추출/해석 오류 · **B**=원문 정보 부족 · **C**=현재 사용자 결정 필요 · 보조: **K**=알려진 분석 한계 · **P**=잠정 관찰 · **F**=후속 의미 조사 · **I**=원문 내 불일치(원문 변경 제안은 후속 확인 후보이며 지금 선택 대기 아님)", "",
         "상태: open(열림) · fixed(에이전트가 고침·재검증) · recorded(한계로 기록, 1차 종료를 막지 않음) · deferred(후속 단계 — 21개 비교 후)", ""]
    allis = [dict(i, segment=s["id"]) for s in segs for i in s["issues"]] + [dict(i, segment="전체") for i in notes.get("global_issues", [])]
    for code in "ABCKPFI":
        sub = [i for i in allis if i["code"] == code]
        I += [f"## {code} ({len(sub)})", ""]
        if not sub:
            I.append("- 없음" + (" — " + notes.get("c_zero_reason", "") if code == "C" else ""))
        for i in sub:
            I.append(f"- **{code}-{i['id']}** [{i['status']}] ({i['segment']}) {i['text']} — 위치: {', '.join('`'+p+'`' for p in i.get('pointers', []))}")
        I.append("")
    kn = notes.get("morph_known_errors", [])
    I += [f"## K-형태소 오분절 출현 목록 ({len(kn)})", "",
          "구간 = 해당 Pointer 의 디코딩된 값 문자열 안 Unicode 코드포인트 [start,end). " f"{len(kn)}출현 모두 그 값에서 표면형이 정확히 1회 나온다.", ""]
    I += [f"- `{k['pointer']}` [{k['span'][0]},{k['span'][1]}) «{k['surface']}» → `{k['raw_tokens']}` — {k['impact']}" for k in kn] or ["- 없음"]
    (HERE / "issues.md").write_text("\n".join(I) + "\n", encoding="utf-8")
    print(f"ok sha={sha} nodes={len(nodes)} leaves={source_map['counts']['leaves']} morph={len(records)} excl={len(excluded)} auto={len(auto)} manual={len(manual)}")


if __name__ == "__main__":
    main()
