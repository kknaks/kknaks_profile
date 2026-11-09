#!/usr/bin/env python3
"""extracted.json 1차 조사 — 재현 빌드.

실행(레포 루트에서):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/extracted/build.py

원본은 읽기만 한다. 결과는 이 파일이 있는 폴더에만 쓴다.
수동 기록(직접 읽기 결과)은 manual-observations.json · manual-expressions.json ·
segmentation-review.json 에 있고, 이 스크립트는 그 인용이 실제 원문 값 안에 있는지 검사한 뒤 배치만 한다.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/extracted.json"
SRC = ROOT / SRC_REL
OUT_REL = "orchestration/work/phub-ledger-redesign/first-pass/extracted"

SPAN_NOTE = ("span = 디코딩된 원문 텍스트(파일 전체) 기준 Unicode 코드 포인트 [start,end), 시작 포함·끝 제외. "
             "byte_span = UTF-8 파일 바이트 [start,end). value_span = 문자열 리터럴의 따옴표 안쪽 코드 포인트 구간. "
             "morphology·expressions 의 span 은 해당 값 문자열(디코딩 결과) 기준 코드 포인트 [start,end).")


# ---------------------------------------------------------------- raw scanner
class Scanner:
    """위치를 기록하는 JSON 스캐너. 중복 키를 덮어쓰지 않고 출현 순서대로 남긴다."""

    WS = " \t\r\n"

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.dup_keys = []
        self.escapes = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def string(self):
        assert self.t[self.i] == '"', self.i
        s = self.i
        self.i += 1
        has_esc = False
        while True:
            c = self.t[self.i]
            if c == "\\":
                has_esc = True
                self.i += 2
                continue
            if c == '"':
                self.i += 1
                break
            self.i += 1
        lit = self.t[s:self.i]
        if has_esc:
            self.escapes.append([s, self.i])
        return json.loads(lit), [s, self.i], has_esc

    def value(self, ptr, parent, key, index, key_span):
        self.ws()
        c = self.t[self.i]
        node = {"pointer": ptr, "parent": parent, "key": key, "index": index, "key_span": key_span}
        self.nodes.append(node)
        s = self.i
        if c == "{":
            node["type"] = "object"
            self.i += 1
            seen = {}
            children = []
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, kspan, _ = self.string()
                    if k in seen:
                        self.dup_keys.append({"object": ptr, "key": k, "spans": [seen[k], kspan]})
                    seen[k] = kspan
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    cp = ptr + "/" + k.replace("~", "~0").replace("/", "~1")
                    children.append(k)
                    self.value(cp, ptr, k, None, kspan)
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node["keys"] = children
            node["length"] = len(children)
        elif c == "[":
            node["type"] = "array"
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
            node["length"] = n
        elif c == '"':
            v, sp, esc = self.string()
            node.update(type="string", value=v, has_escape=esc, value_span=[sp[0] + 1, sp[1] - 1])
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.t, self.i)
            lit = m.group(0)
            self.i = m.end()
            v = json.loads(lit)
            node.update(type={type(None): "null", bool: "boolean", int: "number", float: "number"}[type(v)], value=v)
        node["span"] = [s, self.i]
        node["literal"] = self.t[s:self.i] if node["type"] not in ("object", "array") else None


def cp_to_byte(text):
    """코드 포인트 인덱스 → 바이트 오프셋 표."""
    out = [0]
    for ch in text:
        out.append(out[-1] + len(ch.encode("utf-8")))
    return out


def field_path(ptr):
    """원본 컬럼명 경로: /M10/safety/common/0 → safety.common[0] (최상위 키는 항목 ID 로 따로 보인다)."""
    parts = ptr.split("/")[2:]
    s = ""
    for p in parts:
        if p.isdigit():
            s += f"[{p}]"
        else:
            s += ("." if s else "") + p
    return s


def pattern_of(ptr):
    parts = ptr.split("/")[1:]
    if not parts or parts == [""]:
        return "(루트)"
    out = ["<항목 키>"] + [("[]" if p.isdigit() else p) for p in parts[1:]]
    s = out[0]
    for p in out[1:]:
        s += p if p == "[]" else "." + p
    return s


def ptr_pattern(ptr):
    parts = ptr.split("/")[1:]
    if not parts:
        return '""'
    return "/" + "/".join(["M\\d+"] + [("\\d+" if p.isdigit() else p) for p in parts[1:]])


# ---------------------------------------------------------------- 분석 적용/제외 규칙
EXCLUDE_FIELDS = {
    "procedure_id": "코드값(Mxx-영문 대문자 식별자). 원문 보존, 형태소 분석 제외",
    "extracted_at": "날짜값(YYYY-MM-DD). 원문 보존, 형태소 분석 제외",
    "updated": "날짜값(YYYY-MM-DD). 원문 보존, 형태소 분석 제외",
    "guardrail_version": "버전 문자열(숫자.숫자). 원문 보존, 형태소 분석 제외",
    "source_type": "영문 소문자 열거 코드값(kr/general/us). 원문 보존, 형태소 분석 제외",
}
ENGLISH_FIELDS = {"name_en"}


def analysis_decision(node):
    if node["type"] != "string":
        return None
    key = node["pointer"].split("/")[-1] if not node["pointer"].split("/")[-1].isdigit() else node["pointer"].split("/")[-2]
    if key in EXCLUDE_FIELDS:
        return ("excluded", EXCLUDE_FIELDS[key])
    if key in ENGLISH_FIELDS:
        return ("analyzed", "영문 언어 텍스트(시술 영문명). Kiwi 결과는 SL 위주이며 영어 형태 분석이 아님 — 원시 결과로만 보존")
    return ("analyzed", "언어 텍스트")


# ---------------------------------------------------------------- 표현 후보 규칙
NUM = r"\d+(?:\.\d+)?"
RULES = [
    ("quantity_unit_time", "regex",
     rf"(?:약\s?|최소\s?|평균\s?|거의\s?)?(?<![A-Za-z\d.])(?<![A-Za-z]-){NUM}(?![A-Za-z\d])(?:\s?~\s?{NUM})?\s?(?:%|mm|개월|주일|주|일간|일|시간|분|회|년대|년|도|장|형|배|차)?(?:\s?(?:이상|이내|이하|미만|초과|간|경|전후|후|뒤|째|정도|간격|에 불과))?"),
    ("quantity_word", "regex", r"(?:수만|수천|수백|수십)\s?회|수\s?(?:시간|일|주|개월|년)|수일|수주|수개월|수년|수 주|수 개월"),
    ("range", "regex", r"\S*~\S*|이상|이내|이하|미만|초과"),
    ("time_relative", "keyword",
     r"직후|직전|당일|이후|이전|후에|후\b|후부터|후 |뒤\b|전\b|중\b|중에|중인|중이|동안|간\b|부터|까지|최근|초기|즉시|즉각|순간적|서서히|점점|빠르게|단시간|시간이 지나면서|시간 지나면|마지막|처음|장기|단기|영구|반영구|오래|주기적|정기적|반복"),
    ("frequency_degree", "keyword",
     r"극히|드물게|드묾|드물지만|드문|흔함|흔한|가장 흔|대부분|일부|약간|가벼운|가볍게|심한|심하게|심각한|극심한|과도한|과다한|과하게|과한|과도|충분한|충분하지|매우|크게|훨씬|거의|최대|최소|강하게|강한|강력한|꼼꼼히|철저히|자주|깊이|깊은|얕은|얇은|높은|높이|낮은|미세한|미세|소량|대량|고농도|저농도|고용량|고강도|고에너지|너무|비교적|풍부|만족스럽|개인차|사람마다|선택적|국소"),
    ("course_duration_marker", "keyword",
     r"일시적|영구|반영구|지속|호전|회복|사라짐|사라지|누적|유지|소실|만성|급성"),
    ("degree_adverb_extra", "keyword",
     r"더\b|잘\b|가장|많이|많은|완전히|아주|억지로|단순히|꾸준히|전반적인|적극적인|직접|스스로|자연스럽게|특정"),
    ("scope_restriction", "keyword", r"\S+만(?=[\s,.)]|$)|만으로"),
    ("causal_marker", "keyword", r"때문에|으로 인해서|으로 인해|로 인해|으로 인한|로 인한|므로|에 의해|에 의한|에 따른"),
    ("endpoint_addition_marker", "keyword", r"최종|최신|더해|뿐만 아니라|에 더해"),
    ("state_marker", "keyword",
     r"활동성|진행 중|진행되|조절이 안 되는|노인성|선천적|염증성|감염성"),
    ("negation", "keyword",
     r"없이|없음|없고|없는|없으므로|없다|않고|않는|않기|않으면서|않아|않음|않으며|않도록|지 않|못|안 되|안 될|불가능|미입증|미착용|미흡|확인되지|비수술|비침습|비박피|비현실|부적절|불만족|불균일|불균형|불분명|불편"),
    ("possibility_uncertainty", "keyword",
     r"수 있|수도 있|가능성|가능\b|가능 |위험|우려|의심|불명확|아직|충분하지 않|에 따라 다름|에 따라 차이|차이가|차이 있|달라"),
    ("condition_scope", "keyword",
     r"경우|\S+ 시\b|\S+ 시 |때\b|때는|에 따라|특히|단,|이면|하면|되면|한다면|으면|\S+에서\b|에 한해|대해|병행 시|병합 시|사용 시|투여 시|시술 시"),
    ("obligation_recommendation", "keyword",
     r"필요|권장|좋음|좋다|피하기|피하고|피함|하지 않기|않기|할 것|알릴 것|주의|조심|꼭|반드시|상의|의사에게|금지|중단|미루는|유지|착용|대응"),
    ("comparison_contrast", "keyword",
     r"보다|비해|달리|비슷|대신|대안|뿐만 아니라|만으로|이지만|지만|오히려|기존|일반적인|일반 |과 같은|와 같은|와 같이|같은 "),
    ("symbol_relation", "regex", r"\s?--\s?|\s?—\s?|→|·|/|\+|;|:|~|(?<=\S)-(?=\S)"),
    ("evidence_marker", "keyword", r"RCT|보고|연구|승인|FDA|식약처|입증|확인되지|평가|근거"),
    ("year_date", "regex", r"\d{4}년대?|\d{4}-\d{2}-\d{2}|\d{4}\b"),
    ("quoted_name", "regex", r"'[^']+'"),
    ("latin_term", "regex", r"[A-Za-z][A-Za-z0-9₂:\-\.]*(?:[ /&][A-Za-z][A-Za-z0-9₂:\-\.]*)*"),
    ("population_subgroup", "keyword",
     r"환자|체질|사람\b|사람|임산부|임신|수유|생리|피부 유형|아시안|어두운 피부|피부색|저체중|면역결핍|사용자|복용 중|이력"),
    ("site_or_layer_keyword", "keyword",
     r"얼굴|이마|미간|눈가|눈밑|눈썹|윗눈꺼풀|눈꺼풀|눈\b|볼\b|볼살|뺨|광대뼈|턱선|이중턱|사각턱|뾰족턱|턱|코끝|콧등|콧구멍|코\b|입술|입꼬리|인중|목\b|두피|손등|손끝|발끝|가슴|엉덩이|복부|배\b|허벅지|팔뚝|팔\b|종아리|옆구리|무릎|관자놀이|다리|골반저근|진피|표피|피하지방|각질층|유두진피|망상진피|지방층|진피층|표피층|피부 아래|피부 속|혈관|시술 부위|주사 부위|주입 부위|채취 부위|이식 부위|치료 부위"),
]


def detect_names(nodes):
    """원장 안의 /Mx/name 값과 그 앞부분 약칭(공백·괄호 앞)을 교차 참조 탐색어로 쓴다."""
    out = {}
    for n in nodes:
        if re.fullmatch(r"/M\d+/name", n["pointer"]):
            nm = n["value"]
            out[nm] = n["pointer"]
            head = re.split(r"[ (]", nm)[0]
            if head != nm and len(head) >= 2:
                out.setdefault(head, n["pointer"])
            for part in nm.split("/"):
                if part != nm and len(part) >= 2:
                    out.setdefault(part, n["pointer"])
    return out


def paren_spans(v):
    st, out = [], []
    for i, c in enumerate(v):
        if c == "(":
            st.append(i)
        elif c == ")" and st:
            s = st.pop()
            out.append([s, i + 1])
    return sorted(out)


def depth_map(v):
    d, out = 0, []
    for c in v:
        if c == "(":
            d += 1
        out.append(d)
        if c == ")":
            d = max(0, d - 1)
    return out


def sentence_spans(v):
    out, s = [], 0
    for m in re.finditer(r"(?<=[^\d\s])\.(?=\s|$)", v):
        e = m.end()
        out.append([s, e])
        s = e
        while s < len(v) and v[s] == " ":
            s += 1
    if s < len(v) and out:
        out.append([s, len(v)])
    return out if len(out) > 1 else []


def clause_spans(v):
    dm = depth_map(v)
    cuts = []
    for m in re.finditer(r", | -- | — |; ", v):
        if dm[m.start()] == 0:
            cuts.append((m.start(), m.end()))
    for m in re.finditer(r"(?<=[^\d\s])\. (?=\S)", v):
        cuts.append((m.start() + 1, m.end()))
    cuts.sort()
    if not cuts:
        return []
    out, s = [], 0
    for a, b in cuts:
        if a > s:
            out.append([s, a])
        s = b
    if s < len(v):
        out.append([s, len(v)])
    return out


def main():
    raw = SRC.read_bytes()
    h0 = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    sc = Scanner(text)
    sc.value("", None, None, None, None)
    sc.ws()
    assert sc.i == len(text), "trailing data"
    nodes = sc.nodes
    b = cp_to_byte(text)
    utf16_ok = all(ord(c) <= 0xFFFF for c in text)

    # 구획: S00 = 루트 컨테이너, S01.. = 최상위 키(파일 순서)
    top = [n for n in nodes if n["parent"] == ""]
    sections = [{"id": "S00", "top_key": None, "pointer_prefix": "", "review_file": "review.md",
                 "review_anchor": "#s00-루트"}]
    for i, n in enumerate(top, 1):
        sections.append({"id": f"S{i:02d}", "top_key": n["key"], "pointer_prefix": n["pointer"],
                         "review_file": f"review-part-{i:02d}-{n['key']}.md"})
    def section_of(ptr):
        if ptr == "":
            return "S00"
        tk = ptr.split("/")[1]
        for s in sections[1:]:
            if s["top_key"] == tk:
                return s["id"]
        raise KeyError(ptr)

    for n in nodes:
        n["section"] = section_of(n["pointer"])
        n["byte_span"] = [b[n["span"][0]], b[n["span"][1]]]
        if n["key_span"]:
            n["key_byte_span"] = [b[n["key_span"][0]], b[n["key_span"][1]]]
        if n["type"] == "string":
            inner = text[n["value_span"][0]:n["value_span"][1]]
            n["decoded_equals_literal_inner"] = inner == n["value"]
        n["field_path"] = field_path(n["pointer"]) if n["pointer"].count("/") >= 2 else None
        n["path_pattern"] = pattern_of(n["pointer"])
        n["pointer_pattern"] = ptr_pattern(n["pointer"])
        parts = n["pointer"].split("/")
        if len(parts) >= 2 and parts[1]:
            n["context"] = {"item_pointer": "/" + parts[1], "item_name_pointer": "/" + parts[1] + "/name",
                            "item_procedure_id_pointer": "/" + parts[1] + "/procedure_id",
                            "field_group_pointer": "/" + "/".join(parts[1:3]) if len(parts) >= 3 else None,
                            "parent_pointer": n["parent"]}
        else:
            n["context"] = None
        # 빈 값 표시
        n["is_empty"] = (n["type"] == "null") or (n["type"] == "string" and n["value"] == "") or \
            (n["type"] in ("object", "array") and n["length"] == 0)
        n["is_leaf"] = n["type"] not in ("object", "array") or n["length"] == 0

    byptr = {n["pointer"]: n for n in nodes}
    assert len(byptr) == len(nodes), "pointer 중복(중복 키) — 별도 처리 필요"

    # 필드명 출현
    field_occ = {}
    for n in nodes:
        if n["key"] is not None:
            field_occ.setdefault(n["key"], []).append({"pointer": n["pointer"], "key_span": n["key_span"],
                                                       "key_byte_span": n["key_byte_span"]})

    source_map = {
        "source": {"path": SRC_REL, "sha256": h0, "bytes": len(raw), "code_points": len(text),
                   "encoding": "UTF-8", "bom": raw.startswith(b"\xef\xbb\xbf"), "newlines": text.count("\n"),
                   "escape_literals": sc.escapes, "duplicate_keys": sc.dup_keys,
                   "non_bmp_chars": sum(1 for c in text if ord(c) > 0xFFFF),
                   "non_ascii_non_hangul_chars": sorted({c for c in text if ord(c) > 127 and not ("가" <= c <= "힣")})},
        "span_note": SPAN_NOTE,
        "counts": {"nodes": len(nodes), "key_occurrences": sum(len(v) for v in field_occ.values()),
                   "distinct_keys": len(field_occ),
                   "by_type": {t: sum(1 for n in nodes if n["type"] == t) for t in
                               ("object", "array", "string", "number", "boolean", "null")},
                   "leaves": sum(1 for n in nodes if n["is_leaf"]),
                   "empty_values": sum(1 for n in nodes if n["is_empty"])},
        "nodes": nodes,
        "field_name_occurrences": field_occ,
    }

    # ------------------------------------------------ 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")
    analyzer = {
        "name": "Kiwi (kiwipiepy)", "kiwipiepy": kiwipiepy.__version__, "python": sys.version.split()[0],
        "constructor": "Kiwi(num_workers=1, model_type='cong'); 그 밖 생성자 인자는 기본값(내장 기본 사전)",
        "model_type": "cong", "num_workers": 1, "user_dictionary": "없음(추가 단어 0)",
        "tokenize_kwargs": "kiwi.tokenize(text) 기본값 — 옵션 인자 전달 없음",
        "tagset": "Kiwi 품사 체계(세종 기반 확장)",
        "lemma": "Kiwi Token.lemma 그대로 기록. 도구가 주지 않는 기본형은 만들지 않았다.",
        "offset": "Kiwi Token.start/len(UTF-16 코드 단위) — 이 원장은 BMP 밖 문자가 0이라 코드 포인트와 같다(빌드 검사). surface = value[span].",
        "invocation": "uv run --python 3.12 --with kiwipiepy==0.24.1",
        "utf16_equals_codepoint": utf16_ok,
    }
    analyzed, excluded = [], []
    for n in nodes:
        dec = analysis_decision(n)
        if n["type"] != "string":
            if n["is_leaf"]:
                excluded.append({"pointer": n["pointer"], "type": n["type"], "value": n.get("value"),
                                 "reason": "문자열 아님(" + n["type"] + ") — 형태소 분석 대상 아님. 값 보존"})
            continue
        if dec[0] == "excluded":
            excluded.append({"pointer": n["pointer"], "type": "string", "value": n["value"], "reason": dec[1]})
            continue
        v = n["value"]
        toks = []
        for i, t in enumerate(kiwi.tokenize(v)):
            surf = v[t.start:t.start + t.len]
            toks.append({"i": i, "form": t.form, "tag": t.tag, "lemma": getattr(t, "lemma", None),
                         "span": [t.start, t.start + t.len], "surface": surf})
        analyzed.append({"pointer": n["pointer"], "section": n["section"], "field_path": n["field_path"],
                         "reason": dec[1], "value": v, "tokens": toks})
    fieldnames = []
    for k in sorted(field_occ):
        fieldnames.append({"field_name": k, "occurrences": len(field_occ[k]),
                           "tokens": [{"form": t.form, "tag": t.tag, "span": [t.start, t.start + t.len],
                                       "surface": k[t.start:t.start + t.len]} for t in kiwi.tokenize(k)],
                           "underscore_split": k.split("_"),
                           "note": "필드명(영문 식별자 또는 항목 키 Mxx)은 언어 텍스트와 분리해 기록. 뜻은 정하지 않는다."})

    seg_review = json.loads((HERE / "segmentation-review.json").read_text(encoding="utf-8"))
    an_by = {a["pointer"]: a for a in analyzed}
    marks = []
    for r in seg_review["occurrences"]:
        a = an_by[r["pointer"]]
        s, e = r["span"]
        assert a["value"][s:e] == r["text"], ("seg-review text mismatch", r)
        raw_t = [t for t in a["tokens"] if t["span"][0] < e and t["span"][1] > s]
        got = [f"{t['form']}/{t['tag']}" for t in raw_t]
        assert got == r["raw_tokens"], ("seg-review raw tokens mismatch", r["pointer"], r["text"], got, r["raw_tokens"])
        for t in raw_t:
            t.setdefault("review_marks", []).append(r["id"])
        marks.append(r)
    morphology = {"analyzer": analyzer, "span_note": SPAN_NOTE, "counts": {
        "analyzed_values": len(analyzed), "tokens": sum(len(a["tokens"]) for a in analyzed),
        "excluded_leaves": len(excluded), "field_names": len(fieldnames), "review_marked_occurrences": len(marks)},
        "review_scope": seg_review["scope"],
        "analyzed": analyzed, "excluded": excluded, "field_names": fieldnames,
        "segmentation_review": marks}

    # ------------------------------------------------ 표현
    names = detect_names(nodes)
    exprs = []

    def add(n, sp, cat, method, extra=None):
        v = n["value"]
        rec = {"id": f"E{len(exprs) + 1:05d}", "pointer": n["pointer"], "section": n["section"],
               "category_candidate": cat, "method": method, "span": sp, "text": v[sp[0]:sp[1]],
               "context_value_pointer": n["pointer"]}
        if extra:
            rec.update(extra)
        exprs.append(rec)

    for n in nodes:
        if n["type"] != "string":
            continue
        v = n["value"]
        dec = analysis_decision(n)
        add(n, [0, len(v)], "segment.value", "값 전체")
        if dec[0] == "excluded":
            continue
        for sp in sentence_spans(v):
            add(n, sp, "segment.sentence", "'.' + 공백/끝 기준 문장")
        for sp in clause_spans(v):
            add(n, sp, "segment.clause", "괄호 밖 ', ' · ' -- ' · ' — ' · '; ' 와 문장 경계로 자른 절")
        for sp in paren_spans(v):
            add(n, sp, "segment.parenthetical", "괄호 쌍(중첩 포함)")
        for cat, kind, pat in RULES:
            for m in re.finditer(pat, v):
                if m.end() > m.start() and m.group(0).strip():
                    a, z = m.start(), m.end()
                    while a < z and v[a] == " ":
                        a += 1
                    while z > a and v[z - 1] == " ":
                        z -= 1
                    if cat == "quantity_unit_time" and not re.search(r"\d", v[a:z]):
                        continue
                    add(n, [a, z], cat, kind + ": " + pat[:60] + ("…" if len(pat) > 60 else ""))
        for nm, src in names.items():
            for m in re.finditer(re.escape(nm), v):
                if n["pointer"] == src:
                    continue
                add(n, [m.start(), m.end()], "cross_reference_name", "원장 내 /Mx/name 값·약칭 문자열 일치(관계 확정 아님)",
                    {"matched_name_pointer": src})
    manual = json.loads((HERE / "manual-expressions.json").read_text(encoding="utf-8"))
    for me in manual["expressions"]:
        n = byptr[me["pointer"]]
        v = n["value"]
        occ = [m.start() for m in re.finditer(re.escape(me["text"]), v)]
        assert occ, ("manual expression not found", me)
        k = me.get("occurrence", 0)
        a = occ[k]
        add(n, [a, a + len(me["text"])], "manual." + me["category"], "수동(직접 읽기)",
            {"manual_id": me["id"], "note": me.get("note")})
    # 정확히 같은 (pointer, span, category) 중복 생성 검사
    seen = set()
    for e in exprs:
        key = (e["pointer"], tuple(e["span"]), e["category_candidate"])
        assert key not in seen, ("duplicate expression", e)
        seen.add(key)
    cats = {}
    for e in exprs:
        cats[e["category_candidate"]] = cats.get(e["category_candidate"], 0) + 1
    expressions = {"span_note": SPAN_NOTE,
                   "note": "범주는 탐색용 후보이며 확정 분류가 아니다. 규칙은 원문 문자열에 직접 적용했고 형태소 품사를 쓰지 않았다. "
                           "같은 구간이 여러 범주에 겹치는 것은 의도한 것이다. 같은 (pointer, span, 범주) 중복 생성은 0 으로 검사했다.",
                   "rules": [{"category_candidate": c, "kind": k, "pattern": p} for c, k, p in RULES],
                   "cross_reference_terms": names,
                   "counts": {"total": len(exprs), "by_category": dict(sorted(cats.items()))},
                   "expressions": exprs}

    # ------------------------------------------------ 관찰 · coverage
    obs = json.loads((HERE / "manual-observations.json").read_text(encoding="utf-8"))
    for o in obs["observations"]:
        for ev in o["evidence"]:
            v = byptr[ev["pointer"]]
            hay = v["value"] if v["type"] == "string" else json.dumps(v.get("value"), ensure_ascii=False)
            if v["type"] in ("object", "array"):
                hay = ""
            if ev.get("quote"):
                assert ev["quote"] in hay, ("observation quote not found", o["id"], ev)
    read_log = json.loads((HERE / "reading-log.json").read_text(encoding="utf-8"))
    cov_sections = []
    for s in sections:
        owned = [n["pointer"] for n in nodes if n["section"] == s["id"]]
        leaves = [n["pointer"] for n in nodes if n["section"] == s["id"] and n["is_leaf"]]
        rl = read_log["sections"][s["id"]]
        entry = dict(s)
        entry.update({
            "pointer_range": {"prefix": s["pointer_prefix"], "first": owned[0], "last": owned[-1],
                              "file_span": [byptr[owned[0]]["span"][0], max(byptr[p]["span"][1] for p in owned)] if s["id"] != "S00" else byptr[""]["span"]},
            "owned_pointers": owned if s["id"] != "S00" else [""],
            "owned_leaf_pointers": leaves if s["id"] != "S00" else [],
            "context_refs": (["(없음 — 루트)"] if s["id"] == "S00" else
                             ["", s["pointer_prefix"] + "/name", s["pointer_prefix"] + "/procedure_id"]),
            "context_note": ("S00 은 루트 객체 노드만 소유한다. 각 항목 구획은 루트를 문맥으로 참조만 하고, 자기 항목의 name·procedure_id 는 "
                             "소유하면서 구획 안 모든 값의 문맥으로 함께 참조한다."),
            "machine_extraction": "완료(build.py — 구조·Pointer·구간·형태소·규칙 후보)",
            "direct_read": rl["status"], "read_passes": rl["passes"],
            "manual_observation_ids": [o["id"] for o in obs["observations"] if o["section"] == s["id"]],
            "manual_expression_ids": [m["id"] for m in manual["expressions"] if byptr[m["pointer"]]["section"] == s["id"]],
            "segmentation_review_ids": [r["id"] for r in marks if byptr[r["pointer"]]["section"] == s["id"]],
            "open_issue_refs": sorted({i for o in obs["observations"] if o["section"] == s["id"] for i in o.get("issue_refs", [])}),
        })
        if s["id"] == "S00":
            entry["owned_pointers"] = [""]
        cov_sections.append(entry)
    coverage = {"source": {"path": SRC_REL, "sha256": h0},
                "partition": "최상위 객체 1개(S00 루트) + 최상위 키 17개(파일 순서, 항목 하나 = 구획 하나). 항목 길이가 1,256~2,165자로 한 번에 전부 읽을 수 있어 항목 안을 더 쪼개지 않았다.",
                "last_read": read_log["last_read"], "remaining_sections": [s["id"] for s in cov_sections if s["direct_read"] != "직접 읽음"],
                "sections": cov_sections}

    # ------------------------------------------------ review
    write_reviews(nodes, byptr, sections, obs, manual, marks, exprs, analyzed, excluded, source_map, morphology, expressions, coverage, field_occ, read_log)

    for name, data in [("source-map.json", source_map), ("morphology.json", morphology),
                       ("expressions.json", expressions), ("coverage.json", coverage)]:
        (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    h1 = hashlib.sha256(SRC.read_bytes()).hexdigest()
    assert h0 == h1
    print(f"source sha256 start={h0} end={h1}")
    print(f"nodes={len(nodes)} analyzed={len(analyzed)} tokens={morphology['counts']['tokens']} excluded={len(excluded)} "
          f"expressions={len(exprs)} manual_expr={len(manual['expressions'])} observations={len(obs['observations'])} "
          f"seg_marks={len(marks)} sections={len(sections)}")


def md(v):
    return str(v).replace("|", "\\|")


def fmt_val(n):
    if n["type"] == "string":
        return md(n["value"])
    if n["type"] in ("object", "array"):
        return "(빈 " + n["type"] + ")" if n["length"] == 0 else f"({n['type']} · {n['length']})"
    return md(json.dumps(n["value"]))


def write_reviews(nodes, byptr, sections, obs, manual, marks, exprs, analyzed, excluded, source_map, morphology, expressions, coverage, field_occ, read_log):
    tmpl = (HERE / "review-template.md").read_text(encoding="utf-8")
    obs_by_sec = {}
    for o in obs["observations"]:
        obs_by_sec.setdefault(o["section"], []).append(o)
    an_ptr = {a["pointer"] for a in analyzed}
    ex_by = {e["pointer"]: e["reason"] for e in excluded}

    # 컬럼 구성 표
    pats = {}
    for n in nodes:
        key = (n["path_pattern"], n["type"])
        pats.setdefault(key, []).append(n)
    col_rows = []
    order = []
    for n in nodes:
        k = (n["path_pattern"], n["type"])
        if k not in order:
            order.append(k)
    for k in order:
        lst = pats[k]
        ex = lst[0]
        items = sorted({x["pointer"].split("/")[1] for x in lst if x["pointer"]}, key=lambda s: int(s[1:]) if s else 0)
        if ex["type"] in ("object", "array"):
            lens = sorted({x["length"] for x in lst})
            struct = (("키: " + ", ".join(ex["keys"])) if ex["type"] == "object" else "문자열 배열") + f" · 길이 {lens[0]}~{lens[-1]}" if lens else ""
            if ex["type"] == "object":
                keysets = sorted({tuple(x["keys"]) for x in lst})
                if len(keysets) > 1:
                    struct = "키 구성 변형 " + str(len(keysets)) + "종(§2.2) · 길이 " + f"{lens[0]}~{lens[-1]}"
            sample = fmt_val(ex)
        else:
            struct = "스칼라"
            sample = fmt_val(ex)
        if len(sample) > 80:
            sample = sample[:80] + " …(전체는 해당 구획 표)"
        opt = "(루트)" if ex["pointer"] == "" else ("전 항목(17)" if len(items) == 17 else ("항목 " + ", ".join(items)))
        shown = '`""`' if ex["pointer"] == "" else f"`{ex['pointer']}`"
        col_rows.append(f"| `{k[0]}` | `{ex['pointer_pattern']}` | {k[1]} | {struct} | {len(lst)} | {opt} | {sample} | {shown} |")

    keysets = {}
    for n in nodes:
        if n["type"] == "object":
            keysets.setdefault((n["path_pattern"], tuple(n["keys"])), []).append(n["pointer"])
    ks_rows = [f"| `{p}` | {len(k)} | `{', '.join(k)}` | {len(v)} | {', '.join(('`'+x+'`') if x else '`""`' for x in v)} |"
               for (p, k), v in keysets.items()]

    toc = []
    for s in coverage["sections"]:
        if s["id"] == "S00":
            toc.append(f"| S00 | (루트) | `\"\"` | 1 | {s['direct_read']} | 이 문서 §S00 |")
            continue
        nm = byptr[s["pointer_prefix"] + "/name"]["value"]
        toc.append(f"| {s['id']} | `{s['top_key']}` {md(nm)} | `{s['pointer_prefix']}` … | {len(s['owned_pointers'])} (말단 {len(s['owned_leaf_pointers'])}) | {s['direct_read']} | [{s['review_file']}](./{s['review_file']}) |")

    cats = expressions["counts"]["by_category"]
    rep = {
        "{{SHA}}": source_map["source"]["sha256"], "{{BYTES}}": f"{source_map['source']['bytes']:,}",
        "{{CP}}": f"{source_map['source']['code_points']:,}", "{{NODES}}": str(source_map["counts"]["nodes"]),
        "{{KEYOCC}}": str(source_map["counts"]["key_occurrences"]), "{{DKEYS}}": str(source_map["counts"]["distinct_keys"]),
        "{{BYTYPE}}": " · ".join(f"{k} {v}" for k, v in source_map["counts"]["by_type"].items()),
        "{{LEAVES}}": str(source_map["counts"]["leaves"]), "{{EMPTY}}": str(source_map["counts"]["empty_values"]),
        "{{ANALYZED}}": str(morphology["counts"]["analyzed_values"]), "{{TOKENS}}": f"{morphology['counts']['tokens']:,}",
        "{{EXCLUDED}}": str(morphology["counts"]["excluded_leaves"]), "{{FIELDN}}": str(morphology["counts"]["field_names"]),
        "{{SEGMARKS}}": str(len(marks)), "{{EXPRS}}": f"{expressions['counts']['total']:,}",
        "{{MANUALEXPR}}": str(len(manual["expressions"])), "{{OBS}}": str(len(obs["observations"])),
        "{{COLROWS}}": "\n".join(col_rows), "{{KSROWS}}": "\n".join(ks_rows), "{{TOC}}": "\n".join(toc),
        "{{CATS}}": " · ".join(f"{k} {v}" for k, v in cats.items()),
        "{{GLOBALOBS}}": "\n".join(obs_line(o) for o in obs_by_sec.get("S00", [])),
        "{{LASTREAD}}": md(json.dumps(read_log["last_read"], ensure_ascii=False)),
    }
    out = tmpl
    for k, v in rep.items():
        out = out.replace(k, v)
    assert "{{" not in out, re.findall(r"\{\{\w+\}\}", out)
    (HERE / "review.md").write_text(out, encoding="utf-8")

    for s in coverage["sections"]:
        if s["id"] == "S00":
            continue
        p = s["pointer_prefix"]
        nm = byptr[p + "/name"]["value"]
        lines = [f"# {s['id']} — `{s['top_key']}` ({md(nm)}) · extracted.json 1차 조사", "",
                 f"> 구획 {s['id']} · 소유 Pointer `{p}` 와 그 아래 {len(s['owned_pointers'])}개 노드(말단 {len(s['owned_leaf_pointers'])}). "
                 f"문맥 참조: 루트 `\"\"`, `{p}/name`, `{p}/procedure_id`. 직접 읽기 상태: **{s['direct_read']}** "
                 f"({'; '.join(s['read_passes'])}).",
                 "> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. "
                 "[목차로](./review.md#구획-목차)", "",
                 "## 1. 모든 값 (원본 순서)", "",
                 "| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |",
                 "|---|---|---|---|---|---|"]
        i = 0
        for n in nodes:
            if n["section"] != s["id"]:
                continue
            i += 1
            col = n["field_path"] if n["field_path"] else f"(항목 {s['top_key']})"
            if n["type"] == "string":
                an = "분석" if n["pointer"] in an_ptr else "제외: " + ex_by[n["pointer"]].split(".")[0]
            elif n["is_leaf"]:
                an = "제외: 문자열 아님"
            else:
                an = "—(컨테이너)"
            lines.append(f"| {i} | `{col}` | `{n['pointer']}` | {n['type']} | {fmt_val(n)} | {an} |")
        lines += ["", "## 2. 잠정 관찰 (원문과 분리)", "",
                  "각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, "
                  "F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.", ""]
        for o in obs_by_sec.get(s["id"], []):
            lines.append(obs_line(o))
        lines += ["", "## 3. 수동 표현 기록 (직접 읽기)", "",
                  "| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |", "|---|---|---|---|---|"]
        for m in manual["expressions"]:
            if byptr[m["pointer"]]["section"] == s["id"]:
                lines.append(f"| {m['id']} | {m['category']} | `{m['pointer']}` | {md(m['text'])} | {md(m.get('note') or '')} |")
        lines += ["", "## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)", "",
                  "| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |", "|---|---|---|---|---|---|---|"]
        for r in marks:
            if byptr[r["pointer"]]["section"] == s["id"]:
                lines.append(f"| {r['id']} | `{r['pointer']}` | [{r['span'][0]},{r['span'][1]}) | {md(r['text'])} | {md(' + '.join(r['raw_tokens']))} | {md(r['problem'])} | {md(r['impact'])} |")
        nexp = sum(1 for e in exprs if e["section"] == s["id"])
        lines += ["", f"규칙 기반 표현 후보 {nexp}건(이 구획)은 [expressions.json](./expressions.json) 의 `section: \"{s['id']}\"` 에 있다. "
                  "후보이며 전수 의미 해석이 아니다.", ""]
        (HERE / s["review_file"]).write_text("\n".join(lines), encoding="utf-8")


def obs_line(o):
    ev = "; ".join(f"`{e['pointer']}`" + (f" 「{md(e['quote'])}」" if e.get("quote") else "") for e in o["evidence"])
    refs = (" → " + ", ".join(o["issue_refs"])) if o.get("issue_refs") else ""
    return f"- **{o['id']}** ({o['kind']}) {md(o['text'])}{refs}  \n  근거: {ev}"


if __name__ == "__main__":
    main()
