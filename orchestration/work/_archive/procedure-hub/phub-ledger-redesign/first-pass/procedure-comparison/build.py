"""procedure-comparison.json 1차 조사 재현 스크립트.

실행(레포 루트에서):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/procedure-comparison/build.py

입력: 원본(읽기 전용) + 같은 폴더의 수동 기록
  manual-expressions.json        직접 읽으며 고른 다어절·문맥 표현(정확 부분문자열)
  segmentation-review.json       직접 대조로 확인한 오분절·오태깅 출현(교정 아님, 표시)
  expression-review.json         regex·keyword 후보 중 직접 판정한 오탐·부분일치
  review-template.md             읽기용 문서의 손으로 쓴 부분(<!-- GENERATED:* --> 자리에 원문 표를 채움)
산출: source-map.json · morphology.json · expressions.json · validation-machine.json · review.md
      · tokens-readable.txt(직접 대조용 토큰 열람본)

구간 기준
  span          파일 전체 디코딩 텍스트의 Unicode 코드 포인트 [start,end) — JSON 리터럴(따옴표 포함) 구간
  value_span    문자열 노드의 리터럴 안쪽(따옴표 제외) 파일 코드 포인트 구간
  byte_span     같은 리터럴의 UTF-8 파일 바이트 구간 [start,end)
  토큰·표현 span 해당 값의 디코딩 문자열 기준 코드 포인트 [start,end)
  이 원장은 이스케이프 0건이라 디코딩 문자열 == 리터럴 안쪽이다. 노드마다 decoded_equals_literal_interior 로 기록한다.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.getcwd()
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/procedure-comparison.json"
SRC = os.path.join(ROOT, SRC_REL)
OUT = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(SRC):
    sys.exit(f"원본을 찾을 수 없다(레포 루트에서 실행): {SRC}")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_manual(name, default):
    p = os.path.join(OUT, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


# ---------------------------------------------------------------- 1. 원본 고정
HASH_START = sha256(SRC)
RAW = open(SRC, "rb").read()
TEXT = RAW.decode("utf-8")
BYTE_OFF = [0]
for ch in TEXT:
    BYTE_OFF.append(BYTE_OFF[-1] + len(ch.encode("utf-8")))
SRC_FACTS = {
    "path": SRC_REL, "bytes": len(RAW), "code_points": len(TEXT), "encoding": "utf-8",
    "bom": RAW.startswith(b"\xef\xbb\xbf"), "newlines": TEXT.count("\n"), "backslash_escapes": TEXT.count("\\"),
    "non_bmp_chars": sum(1 for c in TEXT if ord(c) > 0xFFFF), "non_ascii_chars": sum(1 for c in TEXT if ord(c) > 127),
    "sha256_start": HASH_START,
}


# ------------------------------------------- 자체 파서: 위치 + 중복 키 감지
class P:
    NUM = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null")

    def __init__(self, s):
        self.s, self.i = s, 0
        self.nodes, self.keys, self.dups = [], [], []

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n":
            self.i += 1

    @staticmethod
    def esc(k):
        return k.replace("~", "~0").replace("/", "~1")

    def string(self):
        assert self.s[self.i] == '"'
        j = self.i + 1
        while self.s[j] != '"':
            j += 2 if self.s[j] == "\\" else 1
        lit = self.s[self.i:j + 1]
        self.i = j + 1
        return json.loads(lit), lit

    def value(self, ptr, parent, key, order):
        self.ws()
        c, start = self.s[self.i], self.i
        if c in "{[":
            node = {"pointer": ptr, "parent": parent, "key": key, "order_in_parent": order,
                    "type": "object" if c == "{" else "array", "span": None}
            if c == "{":
                node["children_keys"] = []
            self.nodes.append(node)
            self.i += 1
            self.ws()
            close = "}" if c == "{" else "]"
            n, seen = 0, {}
            if self.s[self.i] == close:
                self.i += 1
            else:
                while True:
                    if c == "{":
                        self.ws()
                        ks = self.i
                        k, _ = self.string()
                        if k in seen:
                            self.dups.append({"object": ptr, "key": k, "first_span": seen[k], "dup_span": [ks, self.i]})
                        seen[k] = [ks, self.i]
                        cptr = ptr + "/" + self.esc(k)
                        self.keys.append({"key": k, "object_pointer": ptr, "value_pointer": cptr, "order": n,
                                          "span": [ks, self.i]})
                        node["children_keys"].append(k)
                        self.ws()
                        assert self.s[self.i] == ":"
                        self.i += 1
                        self.value(cptr, ptr, k, n)
                    else:
                        self.value(f"{ptr}/{n}", ptr, n, n)
                    n += 1
                    self.ws()
                    if self.s[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.s[self.i] == close
                    self.i += 1
                    break
            node["span"] = [start, self.i]
            node["length"] = n
            return
        if c == '"':
            v, lit = self.string()
            self.nodes.append({"pointer": ptr, "parent": parent, "key": key, "order_in_parent": order, "type": "string",
                               "value": v, "json_literal": lit, "span": [start, self.i], "value_span": [start + 1, self.i - 1],
                               "decoded_equals_literal_interior": lit[1:-1] == v, "empty": v == ""})
            return
        m = self.NUM.match(self.s, self.i)
        assert m, f"parse error at {self.i}"
        tok = m.group(0)
        self.i = m.end()
        t = "boolean" if tok in ("true", "false") else "null" if tok == "null" else "number"
        self.nodes.append({"pointer": ptr, "parent": parent, "key": key, "order_in_parent": order, "type": t,
                           "value": json.loads(tok), "json_literal": tok, "span": [start, self.i]})


p = P(TEXT)
p.value("", None, None, None)
p.ws()
assert p.i == len(TEXT), "trailing content"
NODES, KEYS, DUPS = p.nodes, p.keys, p.dups
DATA = json.loads(TEXT)


def resolve(doc, ptr):
    cur = doc
    for part in ptr.split("/")[1:] if ptr else []:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


CTX_RE = re.compile(r"^/comparisons/(\d+)(?:/([^/]+))?(?:/(\d+))?(?:/([^/]+))?")


def context(ptr):
    m = CTX_RE.match(ptr)
    if not m:
        return {"block": "top"}
    ci = int(m.group(1))
    comp = DATA["comparisons"][ci]
    ctx = {"block": f"comparison[{ci}]", "comparison_pointer": f"/comparisons/{ci}", "comparison_id": comp["id"],
           "comparison_title": comp["title"], "comparison_subtitle": comp["subtitle"]}
    if m.group(2):
        ctx["field"] = m.group(2)
        if m.group(3) is not None:
            ctx["item_index"] = int(m.group(3))
            ctx["array_length"] = len(comp[m.group(2)])
            if m.group(2) == "procedures":
                pr = comp["procedures"][int(m.group(3))]
                ctx["procedure_pointer"] = f"/comparisons/{ci}/procedures/{m.group(3)}"
                ctx["procedure_name"] = pr["name"]
                ctx["procedure_category"] = pr["category"]
                ctx["procedure_sibling_fields"] = list(pr.keys())
                if m.group(4):
                    ctx["procedure_field"] = m.group(4)
    return ctx


for n in NODES:
    n["byte_span"] = [BYTE_OFF[n["span"][0]], BYTE_OFF[n["span"][1]]]
    if "value_span" in n:
        n["value_byte_span"] = [BYTE_OFF[n["value_span"][0]], BYTE_OFF[n["value_span"][1]]]
    n["pointer_pattern"] = re.sub(r"/\d+", "/*", n["pointer"]) or "(root)"
    n["context"] = context(n["pointer"])
for k in KEYS:
    k["byte_span"] = [BYTE_OFF[k["span"][0]], BYTE_OFF[k["span"][1]]]
    k["key_pointer_pattern"] = re.sub(r"/\d+", "/*", k["value_pointer"])

field_occ = {}
for k in KEYS:
    field_occ.setdefault(k["key"], {}).setdefault(k["key_pointer_pattern"], []).append(k["value_pointer"])

# 경로 패턴별 자료형·출현 수(컬럼 구성 표의 기계 근거)
patterns = {}
for n in NODES:
    pt = patterns.setdefault(n["pointer_pattern"], {"types": {}, "count": 0, "examples": [], "empty_values": 0})
    pt["count"] += 1
    pt["types"][n["type"]] = pt["types"].get(n["type"], 0) + 1
    if n.get("empty") or (n["type"] in ("array", "object") and n["length"] == 0) or n["type"] == "null":
        pt["empty_values"] += 1
    if len(pt["examples"]) < 2:
        pt["examples"].append({"pointer": n["pointer"], "value": n.get("value") if n["type"] not in ("array", "object") else f"<{n['type']} length {n['length']}>"})
# 객체 패턴별 선택적 키(일부 객체에만 있는 키)
obj_keysets = {}
for n in NODES:
    if n["type"] == "object":
        obj_keysets.setdefault(n["pointer_pattern"], []).append((n["pointer"], n["children_keys"]))
optional_keys = {}
for pat, lst in obj_keysets.items():
    allk = {k for _, ks in lst for k in ks}
    for k in sorted(allk):
        present = [ptr for ptr, ks in lst if k in ks]
        if len(present) != len(lst):
            optional_keys.setdefault(pat, {})[k] = {"present_in": present, "absent_in": [ptr for ptr, ks in lst if k not in ks]}
key_orders = {pat: sorted({tuple(ks) for _, ks in lst}) for pat, lst in obj_keysets.items()}

# --------------------------------- 형태소 분석 적용/제외 판정
EXCLUDE_RULES = [
    ("/version", re.compile(r"^\d+(\.\d+)+$"), "version string: 숫자·점 버전 표기. 언어 텍스트 아님"),
    ("/updated", re.compile(r"^\d{4}-\d{2}-\d{2}$"), "date string: ISO 날짜. 언어 텍스트 아님"),
    ("/comparisons/*/id", re.compile(r"^[a-z]+(_[a-z]+)*$"), "identifier: 비교군 ID(영문 snake_case 코드). 원문 보존, 구조 사실로만 기록"),
    ("/comparisons/*/procedures/*/category", re.compile(r"^M\d+$"), "identifier: 분류 코드(Mxx). 원장 안에 정의 없음 — 원문 보존, 구조 사실로만 기록"),
    ("/comparisons/*/procedures/*/pih_risk", re.compile(r"^[a-z]+(_[a-z]+)*$"), "enum-like code: 영문 소문자 snake_case 등급 코드. 언어 분석 대신 코드값으로 보존"),
    ("/comparisons/*/procedures/*/pain", re.compile(r"^[★☆]+$"), "symbol rating: ★/☆ 기호열. 형태소 분석 대상 언어 아님 — 기호 개수는 구조 관찰로만 기록, 수치 척도로 확정하지 않음"),
]


def exclusion(n):
    for pat, rx, reason in EXCLUDE_RULES:
        if n["pointer_pattern"] == pat:
            if rx.match(n["value"]):
                return reason
            raise SystemExit(f"제외 규칙 패턴과 값 형태 불일치: {n['pointer']} {n['value']!r}")
    return None


STRINGS = [n for n in NODES if n["type"] == "string"]

from kiwipiepy import Kiwi  # noqa: E402
import kiwipiepy  # noqa: E402

kiwi = Kiwi(num_workers=1, model_type="cong")
KIWI_INFO = {
    "analyzer": "kiwipiepy", "version": kiwipiepy.__version__, "model_type": kiwi.model_type, "num_workers": kiwi.num_workers,
    "constructor": "Kiwi(num_workers=1, model_type='cong')",
    "tokenize_call": "kiwi.tokenize(text) — 모든 옵션 기본값(normalize_coda=False, z_coda=True, split_complex=False, "
                     "split_sents=False, saisiot=None, blocklist=None, compatible_jamo=False)",
    "dictionary": "kiwipiepy 내장 기본 사전(kiwipiepy_model 동봉)", "user_dictionary": "없음",
    "typo_correction": "사용 안 함(typos=None)",
    "pos_tagset": "Kiwi 품사 체계(세종 품사 기반 + SL/SH/SN/W_* 확장, -R/-I 불규칙 표지)",
    "lemma": "Token.lemma 를 그대로 기록. Kiwi 가 주는 값이며 도메인 표준명 아님. 도구가 주지 않는 기본형은 만들지 않음",
    "offset_basis": "Token.start/len = 입력 문자열의 코드 포인트 인덱스. 입력은 원문 값 그대로(정규화 없음)",
}


def analyze(text):
    out = []
    for t in kiwi.tokenize(text):
        s, e = t.start, t.start + t.len
        out.append({"form": t.form, "tag": t.tag, "lemma": t.lemma, "span": [s, e], "surface": text[s:e],
                    "form_equals_surface": t.form == text[s:e]})
    return out


morph_records, excluded = [], []
for n in STRINGS:
    ex = exclusion(n)
    if ex:
        excluded.append({"pointer": n["pointer"], "pointer_pattern": n["pointer_pattern"], "value": n["value"], "reason": ex,
                         "context": n["context"]})
        continue
    morph_records.append({"source": "value", "pointer": n["pointer"], "pointer_pattern": n["pointer_pattern"],
                          "text": n["value"], "file_span_of_text": n["value_span"], "context": n["context"],
                          "tokens": analyze(n["value"])})
TEXTS = {r["pointer"]: r["text"] for r in morph_records}
TOKS = {r["pointer"]: r["tokens"] for r in morph_records}


def split_identifier(name):
    """분석기 미지원 보완: snake_case 를 규칙으로 나눈다(형태소 분석 아님)."""
    return [x for x in name.split("_") if x]


field_morph = []
for f in sorted(field_occ):
    field_morph.append({"source": "field_name", "field_name": f, "occurrence_patterns": sorted(field_occ[f]),
                        "occurrence_count": sum(len(v) for v in field_occ[f].values()),
                        "kiwi_tokens": analyze(f), "identifier_parts_rule_based": split_identifier(f),
                        "role": "필드명(스키마 식별자). 언어 텍스트 값과 구분해 기록 — 영문 식별자라 Kiwi 결과는 SL/기호 분절만 의미 있음"})

# 기계 표시: 미등록·외국어·고유명사 추정·기호 등 원문 대조가 필요한 토큰(오류 판정 아님)
AUTO_FLAG_TAGS = {"UN": "미등록(UN)", "NNP": "고유명사 추정(NNP) — 원문 대조 필요", "XR": "어근(XR)", "SL": "외국어(SL)",
                  "SH": "한자(SH)", "W_SERIAL": "일련번호(W_SERIAL)", "SW": "기타 기호(SW)"}
auto_flags = []
for r in morph_records:
    for i, t in enumerate(r["tokens"]):
        if t["tag"] in AUTO_FLAG_TAGS:
            auto_flags.append({"pointer": r["pointer"], "token_index": i, "form": t["form"], "tag": t["tag"], "span": t["span"],
                               "reason": AUTO_FLAG_TAGS[t["tag"]]})
        elif t["form"] in ("+", "/", "·", "→", ">", "=", "-", "—") and t["tag"].startswith("S"):
            auto_flags.append({"pointer": r["pointer"], "token_index": i, "form": t["form"], "tag": t["tag"], "span": t["span"],
                               "reason": f"구조 기호 '{t['form']}' — 원문 역할(함께·대안·범위·순서·비교) 대조 필요"})

# 직접 대조로 확인한 오분절·오태깅(출현 단위). 토큰이 실제로 있어야 한다 — 없으면 build 실패.
SEG = load_manual("segmentation-review.json", {"occurrences": []})
seg_review, seg_errors = [], []
for o in SEG["occurrences"]:
    toks = TOKS.get(o["pointer"])
    if toks is None:
        seg_errors.append(f"pointer 없음 {o['pointer']}")
        continue
    want = [tuple(x) for x in o["tokens"]]
    got = [(t["form"], t["tag"], t["span"][0], t["span"][1]) for t in toks]
    if not all(tuple([w[0], w[1], w[2][0], w[2][1]]) in got for w in want):
        seg_errors.append(f"토큰 불일치 {o['pointer']} {o['phrase']}")
        continue
    a, b = o["phrase_span"]
    if TEXTS[o["pointer"]][a:b] != o["phrase"]:
        seg_errors.append(f"구간 불일치 {o['pointer']} {o['phrase']}")
        continue
    seg_review.append({**o, "status": "표시됨(교정 아님) — 원시 Kiwi 토큰 유지"})

# ------------------------------------------------- 2. 복합 표현 후보 수집
exprs = []


def add(ptr, s, e, cat, method, **extra):
    t = TEXTS[ptr][s:e]
    if not t.strip():
        return
    exprs.append({"pointer": ptr, "span": [s, e], "text": t, "category_candidate": cat, "method": method, **extra})


NUM = r"\d+(?:\.\d+)?"
RULES = [
    ("quantity_range_unit", "regex(수·범위·단위)", re.compile(
        rf"(?:RR\s*)?{NUM}(?:\s*-\s*{NUM})?\+?\s*(?:개월|주|일|회|만원|nm|%|시간|년)?(?:/(?:바이알|시린지|부위|회|810nm))?"
        r"(?:\s*(?:후|간격|점진|이상|\+))?")),
    ("timing_course", "keyword(시점·경과·지속)", re.compile(
        r"즉시|즉각적?|점진적?|[가-힣]*후(?=[ )]|$)|간격|지속|유지[가-힣]*|재발[가-힣]*|영구적?|반영구|평생|장기적?|초기|"
        r"빠름|느림|짧음|길고|생착|다운타임|아직|여러 회|다회|반복[가-힣]*")),
    ("negation_limit", "keyword(부정·불가·제한·부족)", re.compile(
        r"없[가-힣]*|않[가-힣]*|안 됨|아님|아닌|아니[가-힣]*|어려[가-힣]*|어렵[가-힣]*|부족|제한[가-힣]*|부재|비수술|녹지 않아|불가[가-힣]*")),
    ("possibility_risk", "keyword(가능성·위험·경향·기대)", re.compile(r"가능|위험|경향|기대[가-힣]*|수 있[가-힣]*|주의")),
    ("frequency_degree_comparison", "keyword(빈도·정도·비교)", re.compile(
        r"드물[가-힣]*|가장|최강|최저|최대|최소|높[가-힣]*|낮[가-힣]*|약[하한함](?:[가-힣]*)?|약간|강[한함력]|강하[가-힣]*|심한|중등도|중증|경미|"
        r"미세|깊[은게이]|깊이|얕[가-힣]*|굵은|밝은|어두운|현저히|특히|상대적으로|더 |뚜렷[가-힣]*|큼|크[다게]|적합|경제적|대량|소량|국소|넓은|"
        r"대면적|선택적|정밀|저밀도|저에너지|저출력|고강도|고급|과다|정적|표면|구조적|물리적|자연스[가-힣]*|가벼운|대비|순 안전|> ")),
    ("condition_scope", "keyword(조건·범위·대상)", re.compile(
        r"[가-힣A-Za-z/]+ 시(?=[ ,.)]|$)|[가-힣]+시(?= |$)|경우|별(?=\))|[가-힣]+별|따라|의존|원하는|에서|에는|에 |만 |단독[가-힣]*|전체[가-힣]*|타입별|생착분")),
    ("necessity_recommendation", "keyword(필요·권장·선택)", re.compile(r"필요|필수|권장|선택|핵심|원칙|처치")),
    ("evidence_statement", "keyword(근거·연구·통계)", re.compile(r"근거[가-힣]*|RCT|후향적|관찰연구|대조군|연구|보고[가-힣]*|RR|만족도|발생률|흡수율|생착률|재발률")),
    ("symbol_relation", "regex(구조 기호)", re.compile(r"→|\+|/|·|=|>|—|(?<=[0-9A-Za-z가-힣])-(?=[0-9A-Za-z가-힣])|:")),
    ("parenthetical", "regex(괄호와 앞 어절)", re.compile(r"[^\s(]*\s?\([^()]*\)")),
    ("latin_term", "regex(라틴 문자열)", re.compile(r"[A-Za-z][A-Za-z0-9:\-]*(?:\s[A-Za-z0-9][A-Za-z0-9:\-]*)*")),
]

for r in morph_records:
    ptr, text = r["pointer"], r["text"]
    add(ptr, 0, len(text), "segment.value", "값 전체")
    # 문장 분할: '. ' 경계
    bounds = [0] + [m.end() for m in re.finditer(r"\.\s+", text)]
    if len(bounds) > 1:
        bounds.append(len(text))
        for a, b in zip(bounds, bounds[1:]):
            seg = text[a:b].rstrip()
            add(ptr, a, a + len(seg), "segment.sentence", "regex 문장분할: '. ' 뒤 경계")
    # 쉼표 절 분할(최상위 괄호 밖 ', ' 기준)
    depth, last, parts = 0, 0, []
    for i, ch in enumerate(text):
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            parts.append((last, i))
            last = i + 1
    if parts:
        parts.append((last, len(text)))
        for a, b in parts:
            seg = text[a:b]
            s = a + len(seg) - len(seg.lstrip())
            e = b - (len(seg) - len(seg.rstrip()))
            add(ptr, s, e, "segment.comma_part", "괄호 밖 ',' 기준 분할")
    # 콜론 앞 머리말(evidence_notes)
    m = re.match(r"^([^:：]+):\s", text)
    if m:
        add(ptr, 0, m.end(1), "segment.colon_head", "첫 ':' 앞 머리말")
    for cat, method, rx in RULES:
        for mm in rx.finditer(text):
            g = mm.group(0)
            if not g.strip():
                continue
            s = mm.start() + len(g) - len(g.lstrip())
            e = mm.end() - (len(g) - len(g.rstrip()))
            add(ptr, s, e, cat, method)
    # 품사 기반 수식어: MAG/MM/VA/XR/VCN/MAJ 포함 어절 + 다음 어절
    eoj = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    for t in r["tokens"]:
        if t["tag"] in ("MAG", "MM", "VA", "VA-I", "VA-R", "XR", "VCN", "MAJ"):
            for k, (a, b) in enumerate(eoj):
                if a <= t["span"][0] < b:
                    e = eoj[k + 1][1] if k + 1 < len(eoj) else b
                    add(ptr, a, e, "modifier_phrase", f"Kiwi 품사 {t['tag']} 포함 어절+다음 어절",
                        source_token={"form": t["form"], "tag": t["tag"], "span": t["span"]})
                    break

MANUAL = load_manual("manual-expressions.json", {"expressions": []})
manual_nohit = []
for me in MANUAL["expressions"]:
    hits = 0
    targets = [me["pointer"]] if me.get("pointer") else list(TEXTS)
    for ptr in targets:
        for m in re.finditer(re.escape(me["text"]), TEXTS[ptr]):
            add(ptr, m.start(), m.end(), me["category_candidate"], "manual(직접 읽기)", note=me.get("note"))
            hits += 1
    if hits == 0:
        manual_nohit.append(me["text"])

# 중복 생성 제거: (pointer, span, category, method) 완전 중복만 하나로. 다른 범주의 같은 구간은 의도된 겹침으로 둔다.
seen, deduped, dup_removed = set(), [], 0
for x in exprs:
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"])
    if k in seen:
        dup_removed += 1
        continue
    seen.add(k)
    deduped.append(x)
exprs = sorted(deduped, key=lambda x: (x["pointer"], x["span"][0], -x["span"][1], x["category_candidate"]))
REVIEW = load_manual("expression-review.json", {"items": []})
rev_map = {(i["pointer"], tuple(i["span"]), i["category_candidate"]): i for i in REVIEW["items"]}
rev_used = set()
for i, x in enumerate(exprs):
    x["id"] = f"E{i + 1:05d}"
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"])
    if k in rev_map:
        x["review"] = {"verdict": rev_map[k]["verdict"], "note": rev_map[k]["note"]}
        rev_used.add(k)
    x["context"] = context(x["pointer"])
rev_unused = [list(k) for k in rev_map if k not in rev_used]
# 오분절 표시 출현에서 파생된 표현 후보 표시
seg_tok_keys = {(s["pointer"], w[2][0], w[2][1], w[0], w[1]) for s in seg_review for w in s["tokens"]}
for x in exprs:
    st = x.get("source_token")
    if st and (x["pointer"], st["span"][0], st["span"][1], st["form"], st["tag"]) in seg_tok_keys:
        x["derived_from_flagged_token"] = True

# 어떤 표현 후보(segment.* 제외)에도 덮이지 않은 어절 — 직접 읽기 대조용
uncovered = []
for r in morph_records:
    cov = [x["span"] for x in exprs if x["pointer"] == r["pointer"] and not x["category_candidate"].startswith("segment.")]
    for m in re.finditer(r"\S+", r["text"]):
        if not any(a < m.end() and b > m.start() for a, b in cov):
            uncovered.append({"pointer": r["pointer"], "span": [m.start(), m.end()], "text": m.group(0)})

# ------------------------------------------------------------ 3. 산출 + 기계 검증
HASH_END = sha256(SRC)
SRC_FACTS["sha256_end"] = HASH_END

checks = {}


def check(name, cond, detail=None):
    checks[name] = {"pass": bool(cond), **({"detail": detail} if detail is not None else {})}


check("hash_unchanged", HASH_START == HASH_END)
check("no_duplicate_keys", not DUPS, DUPS)
bad = [n["pointer"] for n in NODES if json.loads(TEXT[n["span"][0]:n["span"][1]]) != resolve(DATA, n["pointer"])]
check("node_span_reparse", not bad, bad)
allp = []


def walk(v, ptr):
    allp.append(ptr)
    if isinstance(v, dict):
        for k, c in v.items():
            walk(c, ptr + "/" + P.esc(k))
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, f"{ptr}/{i}")


walk(DATA, "")
check("bidirectional_pointer_set", set(allp) == {n["pointer"] for n in NODES} and len(allp) == len(NODES),
      {"json_paths": len(allp), "nodes": len(NODES)})
check("morph_partition", {r["pointer"] for r in morph_records} | {e["pointer"] for e in excluded} == {n["pointer"] for n in STRINGS}
      and not ({r["pointer"] for r in morph_records} & {e["pointer"] for e in excluded}))
tokbad = [r["pointer"] for r in morph_records for t in r["tokens"] if r["text"][t["span"][0]:t["span"][1]] != t["surface"]]
check("token_surface_reproduces", not tokbad, tokbad)
check("segmentation_review_matches_tokens", not seg_errors, seg_errors)
check("manual_expressions_all_hit", not manual_nohit, manual_nohit)
check("expression_review_all_used", not rev_unused, rev_unused)
check("expr_span_reproduces", all(TEXTS[x["pointer"]][x["span"][0]:x["span"][1]] == x["text"] for x in exprs))
check("every_value_has_segment", {x["pointer"] for x in exprs if x["category_candidate"] == "segment.value"} == set(TEXTS))

meta = {"source": SRC_FACTS, "generator": "build.py", "span_convention": __doc__.split("구간 기준")[1].split('"""')[0].strip()}

json.dump({**meta, "summary": {"nodes": len(NODES), "keys": len(KEYS), "duplicate_keys": DUPS,
                               "types": {t: sum(1 for n in NODES if n["type"] == t) for t in sorted({n["type"] for n in NODES})},
                               "strings": len(STRINGS), "empty_strings": sum(1 for n in STRINGS if n["value"] == ""),
                               "empty_arrays": [n["pointer"] for n in NODES if n["type"] == "array" and n["length"] == 0],
                               "empty_objects": [n["pointer"] for n in NODES if n["type"] == "object" and n["length"] == 0]},
           "pointer_patterns": patterns, "object_key_orders": {k: [list(x) for x in v] for k, v in key_orders.items()},
           "optional_keys": optional_keys, "field_name_occurrences": field_occ,
           "nodes": NODES, "keys": KEYS},
          open(os.path.join(OUT, "source-map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

tag_counts = {}
for r in morph_records:
    for t in r["tokens"]:
        tag_counts[t["tag"]] = tag_counts.get(t["tag"], 0) + 1
json.dump({**meta, "analyzer": KIWI_INFO,
           "summary": {"values_analyzed": len(morph_records), "values_excluded": len(excluded),
                       "tokens": sum(len(r["tokens"]) for r in morph_records), "field_names": len(field_morph),
                       "tag_counts": dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
                       "auto_flags": len(auto_flags), "segmentation_review_occurrences": len(seg_review)},
           "exclusion_rules": [{"pointer_pattern": a, "value_shape": b.pattern, "reason": c} for a, b, c in EXCLUDE_RULES],
           "values": morph_records, "excluded_values": excluded, "field_names": field_morph,
           "auto_flags": auto_flags, "segmentation_review": seg_review},
          open(os.path.join(OUT, "morphology.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

cat_counts = {}
for x in exprs:
    cat_counts[x["category_candidate"]] = cat_counts.get(x["category_candidate"], 0) + 1
json.dump({**meta, "note": "category_candidate 는 탐색 관점 이름이다. 확정 분류·의미 해석 아님. regex·keyword 후보는 전수 의미 조사가 아니다.",
           "methods": [{"category_candidate": c, "method": m, "pattern": rx.pattern} for c, m, rx in RULES]
           + [{"category_candidate": "segment.*", "method": "값 전체·문장('. ')·괄호 밖 쉼표·콜론 머리말 분할"},
              {"category_candidate": "modifier_phrase", "method": "Kiwi MAG/MM/VA/XR/VCN/MAJ 토큰 포함 어절+다음 어절"},
              {"category_candidate": "(manual)", "method": "manual-expressions.json 의 문자열을 모든 텍스트 값에서 정확 부분문자열로 전부 찾음"}],
           "summary": {"expressions": len(exprs), "by_category": dict(sorted(cat_counts.items())),
                       "exact_duplicates_removed": dup_removed,
                       "reviewed": {v: sum(1 for x in exprs if x.get("review", {}).get("verdict") == v) for v in sorted({i["verdict"] for i in REVIEW["items"]})},
                       "derived_from_flagged_token": sum(1 for x in exprs if x.get("derived_from_flagged_token")),
                       "uncovered_eojeol": len(uncovered)},
           "expressions": exprs, "uncovered_eojeol": uncovered},
          open(os.path.join(OUT, "expressions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump({"source": SRC_FACTS, "checks": checks, "failure_count": sum(1 for c in checks.values() if not c["pass"])},
          open(os.path.join(OUT, "validation-machine.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 직접 대조용 토큰 열람본
with open(os.path.join(OUT, "tokens-readable.txt"), "w", encoding="utf-8") as f:
    for r in morph_records:
        f.write(f"\n## {r['pointer']}\n{r['text']}\n")
        f.write(" ".join(f"{t['form']}/{t['tag']}[{t['span'][0]},{t['span'][1]}]" for t in r["tokens"]) + "\n")
    f.write("\n# 미포착 어절(어떤 표현 후보에도 안 덮임)\n")
    for u in uncovered:
        f.write(f"{u['pointer']} {u['span']} {u['text']}\n")

# ----------------------------------------------------------- 4. 읽기용 review.md
def md(v):
    return str(v).replace("|", "\\|")


def gen_columns():
    rows = ["| 원본 컬럼명 / JSON 경로 패턴 | 자료형·중첩 | 출현 수 | 원문 예시 | 예시 위치(Pointer) | 비고(구조 사실) |", "|---|---|---|---|---|---|"]
    for pat, info in patterns.items():
        types = ", ".join(f"{t}×{c}" for t, c in info["types"].items())
        ex = info["examples"][0]
        val = ex["value"]
        note = []
        parent_pat = pat.rsplit("/", 1)[0] or "(root)"
        leaf = pat.rsplit("/", 1)[-1]
        if parent_pat in optional_keys and leaf in optional_keys[parent_pat]:
            o = optional_keys[parent_pat][leaf]
            note.append(f"선택적 키: {len(o['present_in'])}개 객체에만 있음, {len(o['absent_in'])}개에 없음")
        if info["empty_values"]:
            note.append(f"빈 값 {info['empty_values']}")
        rows.append(f"| `{pat}` | {types} | {info['count']} | {md(json.dumps(val, ensure_ascii=False))} | `{ex['pointer'] or '(빈 문자열 = 루트)'}` | {'; '.join(note)} |")
    return "\n".join(rows)


def gen_values():
    out = ["### 3.0 최상위 `(root)`\n", "| 원본 컬럼명 | 원문 값 | Pointer |", "|---|---|---|"]
    for k, v in DATA.items():
        out.append(f"| {k} | {md(v) if not isinstance(v, list) else f'<array length {len(v)}>'} | `/{k}` |")
    for ci, c in enumerate(DATA["comparisons"]):
        base = f"/comparisons/{ci}"
        out.append(f"\n### 3.{ci + 1} `{base}` — id `{c['id']}`\n")
        out.append("| 원본 컬럼명 | 원문 값 | Pointer |")
        out.append("|---|---|---|")
        for k in c:
            if k in ("procedures", "evidence_notes"):
                out.append(f"| {k} | <array length {len(c[k])}> | `{base}/{k}` |")
            else:
                out.append(f"| {k} | {md(c[k])} | `{base}/{k}` |")
        if "evidence_notes" in c:
            out.append(f"\n**evidence_notes** (`{base}/evidence_notes`, 원본 순서)\n")
            out.append("| # | 원문 값 | Pointer |")
            out.append("|---|---|---|")
            for i, v in enumerate(c["evidence_notes"]):
                out.append(f"| {i} | {md(v)} | `{base}/evidence_notes/{i}` |")
        else:
            out.append(f"\n**evidence_notes** — 이 비교군 객체에는 키 자체가 없다(빈 배열 아님).\n")
        for pi, pr in enumerate(c["procedures"]):
            pb = f"{base}/procedures/{pi}"
            out.append(f"\n**procedures/{pi}** (`{pb}`)\n")
            out.append("| 원본 컬럼명 | 원문 값 | Pointer |")
            out.append("|---|---|---|")
            for k, v in pr.items():
                out.append(f"| {k} | {md(v)} | `{pb}/{k}` |")
    return "\n".join(out)


def gen_seg():
    rows = ["| 서명 | 원문 구절 | 원시 토큰 | 종류 | 영향 | 출현(Pointer [구간]) |", "|---|---|---|---|---|---|"]
    by = {}
    for s in seg_review:
        by.setdefault(s["signature"], []).append(s)
    for sid in sorted(by):
        o = by[sid]
        toks = " ".join(f"{w[0]}/{w[1]}" for w in o[0]["tokens"])
        where = "<br>".join(f"`{x['pointer']}` {x['phrase_span']}" for x in o)
        rows.append(f"| {sid} | {md(o[0]['phrase'])} | {md(toks)} | {o[0]['kind']} | {md(o[0]['impact'])} | {where} |")
    return "\n".join(rows)


def gen_expr():
    rows = ["| category_candidate | 건수 | 방법 |", "|---|---|---|"]
    meth = {}
    for x in exprs:
        meth.setdefault(x["category_candidate"], set()).add(x["method"].split("(")[0])
    for c, n in sorted(cat_counts.items()):
        rows.append(f"| {c} | {n} | {', '.join(sorted(meth[c]))} |")
    rows.append(f"| **합계** | **{len(exprs)}** | 완전 중복 제거 {dup_removed}건 |")
    rv = {}
    for x in exprs:
        if "review" in x:
            rv[x["review"]["verdict"]] = rv.get(x["review"]["verdict"], 0) + 1
    rows.append("")
    rows.append(f"직접 판정(expression-review.json): {', '.join(f'{k} {v}' for k, v in sorted(rv.items()))}. "
                f"오분절 표시 토큰에서 파생된 modifier_phrase {sum(1 for x in exprs if x.get('derived_from_flagged_token'))}건(표시만, 삭제 안 함). "
                f"어떤 표현 후보(segment.* 제외)에도 덮이지 않은 어절 {len(uncovered)}개 — expressions.json `uncovered_eojeol`.")
    return "\n".join(rows)


tpl_path = os.path.join(OUT, "review-template.md")
if os.path.exists(tpl_path):
    tpl = open(tpl_path, encoding="utf-8").read()
    tpl = tpl.replace("<!-- GENERATED:COLUMNS -->", gen_columns()).replace("<!-- GENERATED:VALUES -->", gen_values())
    tpl = tpl.replace("<!-- GENERATED:SEG -->", gen_seg()).replace("<!-- GENERATED:EXPR -->", gen_expr())
    open(os.path.join(OUT, "review.md"), "w", encoding="utf-8").write(tpl)

print(json.dumps({"nodes": len(NODES), "keys": len(KEYS), "dups": len(DUPS), "strings": len(STRINGS),
                  "analyzed": len(morph_records), "excluded": len(excluded),
                  "tokens": sum(len(r["tokens"]) for r in morph_records), "auto_flags": len(auto_flags),
                  "seg_review": len(seg_review), "expressions": len(exprs), "uncovered": len(uncovered),
                  "manual_nohit": manual_nohit, "seg_errors": seg_errors, "rev_unused": rev_unused,
                  "failures": [k for k, v in checks.items() if not v["pass"]]}, ensure_ascii=False, indent=1))
