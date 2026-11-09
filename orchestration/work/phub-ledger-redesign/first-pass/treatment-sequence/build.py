"""treatment-sequence.json 1차 수집 재현 스크립트.

실행(레포 루트에서):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/build.py

원본은 읽기만 한다. 쓰는 곳은 이 스크립트가 있는 폴더뿐이다.
입력(수동 기록, 같은 폴더): manual-expressions.json, segmentation-review.json, review-notes.md
출력: source-map.json, morphology.json, expressions.json, review.md, validation-machine.json, build-output.txt
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../../.."))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-sequence.json"
SRC = os.path.join(ROOT, SRC_REL)

LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


raw = open(SRC, "rb").read()
SHA_START = sha(raw)
text = raw.decode("utf-8")
assert not text.startswith("\ufeff")

# 코드 포인트 인덱스 -> UTF-8 바이트 오프셋
BYTE_AT = [0]
for ch in text:
    BYTE_AT.append(BYTE_AT[-1] + len(ch.encode("utf-8")))
assert BYTE_AT[-1] == len(raw)


def bspan(a, b):
    return [BYTE_AT[a], BYTE_AT[b]]


def esc_ptr(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 파서
class Parser:
    """중복 키를 덮어쓰지 않고 감지하는 재귀 하강 JSON 파서. 위치는 코드 포인트."""

    def __init__(self, s):
        self.s = s
        self.i = 0
        self.nodes = []
        self.keys = []
        self.duplicates = []

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        assert self.s[self.i] == '"', self.i
        start = self.i
        self.i += 1
        out = []
        has_escape = False
        while True:
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                break
            if c == "\\":
                has_escape = True
                e = self.s[self.i + 1]
                if e == "u":
                    out.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                else:
                    out.append({'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}[e])
                    self.i += 2
                continue
            out.append(c)
            self.i += 1
        return "".join(out), start, self.i, has_escape

    def value(self, ptr, parent, key, index):
        self.ws()
        c = self.s[self.i]
        start = self.i
        node = {"pointer": ptr, "parent": parent, "key": key, "index": index}
        self.nodes.append(node)
        if c == "{":
            node["type"] = "object"
            self.i += 1
            seen = {}
            order = []
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke, kesc = self.string()
                    cptr = ptr + "/" + esc_ptr(k)
                    rec = {"key": k, "object_pointer": ptr, "value_pointer": cptr, "order_in_object": len(order),
                           "span": [ks, ke], "byte_span": bspan(ks, ke), "has_escape": kesc}
                    if k in seen:
                        self.duplicates.append({"key": k, "object_pointer": ptr, "first_span": seen[k], "dup_span": [ks, ke]})
                        rec["duplicate_of_earlier"] = True
                    seen[k] = [ks, ke]
                    self.keys.append(rec)
                    order.append(k)
                    self.ws()
                    assert self.s[self.i] == ":"
                    self.i += 1
                    self.value(cptr, ptr, k, None)
                    self.ws()
                    if self.s[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.s[self.i] == "}"
                    self.i += 1
                    break
            node["children"] = order
            node["length"] = len(order)
        elif c == "[":
            node["type"] = "array"
            self.i += 1
            n = 0
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(f"{ptr}/{n}", ptr, None, n)
                    n += 1
                    self.ws()
                    if self.s[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.s[self.i] == "]"
                    self.i += 1
                    break
            node["length"] = n
        elif c == '"':
            v, a, b, e = self.string()
            node.update({"type": "string", "value": v, "value_span": [a + 1, b - 1], "has_escape": e,
                         "json_literal": self.s[a:b]})
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.s, self.i)
            lit = m.group(0)
            self.i = m.end()
            if lit in ("true", "false"):
                node.update({"type": "boolean", "value": lit == "true"})
            elif lit == "null":
                node.update({"type": "null", "value": None})
            else:
                isint = m.group(1) is None and m.group(2) is None
                node.update({"type": "integer" if isint else "number", "value": int(lit) if isint else float(lit)})
            node["json_literal"] = lit
        node["span"] = [start, self.i]
        node["byte_span"] = bspan(start, self.i)
        return node


P = Parser(text)
P.value("", None, None, None)
P.ws()
assert P.i == len(text), "trailing data"
NODES = P.nodes
BYPTR = {n["pointer"]: n for n in NODES}
log(f"nodes={len(NODES)} keys={len(P.keys)} duplicates={len(P.duplicates)}")


# ---------------------------------------------------------------- 문맥
def context(ptr):
    parts = ptr.split("/")[1:]
    if not parts:
        return {"block": "top", "item_index": None, "item_pointer": None, "field": None, "sibling_pointers": []}
    block = parts[0]
    if len(parts) == 1 or BYPTR["/" + block]["type"] != "array" or block == "principles":
        # principles 는 문자열 배열: 항목 자체가 값
        idx = int(parts[1]) if len(parts) > 1 else None
        item = "/" + "/".join(parts[:2]) if len(parts) > 1 else None
        sib = []
        if idx is not None:
            arr = BYPTR["/" + block]
            sib = [f"/{block}/{i}" for i in range(arr["length"]) if i != idx and abs(i - idx) == 1]
        return {"block": block, "item_index": idx, "item_pointer": item, "field": None,
                "sibling_pointers": sib, "sibling_note": "principles 는 독립 문장 배열: 앞뒤 항목만 인접 문맥으로 둔다" if idx is not None else None}
    idx = int(parts[1])
    item = f"/{block}/{idx}"
    field = parts[2] if len(parts) > 2 else None
    item_node = BYPTR[item]
    sib = [f"{item}/{esc_ptr(k)}" for k in item_node.get("children", []) if k != field]
    return {"block": block, "item_index": idx, "item_pointer": item, "field": field, "sibling_pointers": sib}


for n in NODES:
    n["context"] = context(n["pointer"])
for k in P.keys:
    k["context"] = context(k["value_pointer"])

# 필드명 출현
FIELD_OCC = {}
for k in P.keys:
    pat = re.sub(r"/\d+(?=/|$)", "/*", k["value_pointer"])
    FIELD_OCC.setdefault(k["key"], {}).setdefault(pat, []).append(k["value_pointer"])

SOURCE = {
    "path": SRC_REL,
    "size_bytes": len(raw),
    "code_points": len(text),
    "sha256_start": SHA_START,
    "encoding": "utf-8, BOM 없음",
    "newline_count": text.count("\n"),
    "backslash_count": text.count("\\"),
    "non_bmp_count": sum(1 for ch in text if ord(ch) > 0xFFFF),
    "non_ascii_symbols": sorted({f"U+{ord(ch):04X} {ch}" for ch in text if ord(ch) > 0x7F and not ("\uac00" <= ch <= "\ud7a3")}),
    "offset_unit": "디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end). byte_span 은 UTF-8 바이트 [start,end)",
}

# ---------------------------------------------------------------- 형태소
from kiwipiepy import Kiwi  # noqa: E402
import kiwipiepy  # noqa: E402
import importlib.metadata as _md  # noqa: E402

kiwi = Kiwi(num_workers=1, model_type="cong")
ANALYZER = {
    "name": "Kiwi (kiwipiepy)",
    "kiwipiepy": kiwipiepy.__version__,
    "kiwipiepy_model": _md.version("kiwipiepy_model"),
    "constructor": "Kiwi(num_workers=1, model_type='cong') — 나머지 생성자 인자는 기본값(기본 사전 로드, 오타 교정 없음, 표준어 방언)",
    "model_type": kiwi.model_type,
    "num_workers": kiwi.num_workers,
    "tokenize_kwargs": "기본값(kiwi.tokenize(text) — split_sents=False, normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, blocklist=None, compatible_jamo=False)",
    "user_dictionary": "없음(사용자 사전 미사용, 기본 결과 보존)",
    "tagset": "Kiwi 품사 체계(세종 기반 확장 NNG/NNP/NNB/NR/NP/VV/VA/VX/VCP/VCN/MM/MAG/MAJ/J*/E*/XS*/XR/S*/W_* 등)",
    "lemma": "Kiwi Token.lemma 값 그대로. 도구가 주지 않는 기본형은 만들지 않는다.",
    "offset": "Kiwi Token.start/len 을 값 문자열 기준 [start,start+len) 으로 기록. 원장에 BMP 밖 문자가 없어 Kiwi 오프셋 == 코드 포인트 오프셋(검증: surface == text[span] 전수)",
    "normalization": "없음. 원문 값 문자열을 그대로 입력",
    "runtime": "Python " + sys.version.split()[0],
}

VERSION_RE = re.compile(r"^\d+(\.\d+)+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CODE_RE = re.compile(r"^M\d+$")


def classify(n):
    v = n["value"]
    if n["pointer"] == "/version" and VERSION_RE.match(v):
        return "exclude", "버전 문자열(숫자·점). 언어 텍스트 아님"
    if n["pointer"] == "/updated" and DATE_RE.match(v):
        return "exclude", "날짜 문자열(YYYY-MM-DD). 언어 텍스트 아님"
    if CODE_RE.match(v):
        return "exclude", "카테고리 코드값(M+숫자, 한글 없음). 다른 원장 항목을 가리키는 식별자 — 형태소 대상 아님, 원문·위치 보존"
    return "analyze", None


def toks(s):
    out = []
    for t in kiwi.tokenize(s):
        a, b = t.start, t.start + t.len
        out.append({"form": t.form, "tag": t.tag, "lemma": t.lemma, "span": [a, b], "surface": s[a:b],
                    "form_equals_surface": t.form == s[a:b]})
    return out


SEG = json.load(open(os.path.join(HERE, "segmentation-review.json"), encoding="utf-8"))
values, excluded = [], []
for n in NODES:
    if n["type"] == "string":
        kind, why = classify(n)
        if kind == "exclude":
            excluded.append({"pointer": n["pointer"], "value": n["value"], "reason": why, "context": n["context"]})
        else:
            values.append({"source": "value", "pointer": n["pointer"], "text": n["value"],
                           "file_span_of_text": n["value_span"], "context": n["context"], "tokens": toks(n["value"])})
non_string_leaves = [{"pointer": n["pointer"], "type": n["type"], "json_literal": n["json_literal"],
                      "reason": f"{n['type']} 말단 — 형태소 대상 아님(원문 리터럴 보존)"}
                     for n in NODES if n["type"] in ("integer", "number", "boolean", "null")]
field_names = []
for k in sorted(FIELD_OCC):
    field_names.append({"source": "field_name", "field_name": k,
                        "occurrence_patterns": sorted(FIELD_OCC[k]),
                        "occurrence_count": sum(len(v) for v in FIELD_OCC[k].values()),
                        "tokens": toks(k),
                        "identifier_parts_rule_based": k.split("_"),
                        "role": "필드명(스키마 식별자). 언어 텍스트와 구분해 별도 분석. 영문 snake_case 라 Kiwi 는 SL 로만 낸다 — 규칙 분할(underscore)을 함께 둔다"})

# 오분절 검토(수동, 출현별) 적용: 각 기록의 pointer/span/raw token 이 실제 Kiwi 출력과 맞는지 확인
VBY = {v["pointer"]: v for v in values}
seg_errors = []
for r in SEG["occurrences"]:
    v = VBY.get(r["pointer"])
    if v is None:
        seg_errors.append(f"seg: 분석 값 없음 {r['pointer']}")
        continue
    a, b = r["phrase_span"]
    if v["text"][a:b] != r["phrase"]:
        seg_errors.append(f"seg: phrase 불일치 {r['pointer']} {r['phrase_span']} {v['text'][a:b]!r}!={r['phrase']!r}")
    got = [[t["form"], t["tag"], t["span"]] for t in v["tokens"] if t["span"][0] >= a and t["span"][1] <= b]
    if got != r["raw_tokens"]:
        seg_errors.append(f"seg: raw_tokens 불일치 {r['pointer']} {r['phrase']} got={got}")
log(f"segmentation review occurrences={len(SEG['occurrences'])} errors={len(seg_errors)}")
for e in seg_errors:
    log("  " + e)

MORPH = {"source": SOURCE, "analyzer": ANALYZER,
         "scope_note": "문자열 노드 전부를 analyze/exclude 로 나눈다. 비문자열 말단은 non_string_leaves 로 따로 둔다. 필드명은 field_names 로 따로 분석한다.",
         "excluded_values": excluded, "non_string_leaves": non_string_leaves, "values": values, "field_names": field_names,
         "segmentation_review": SEG}

# ---------------------------------------------------------------- 복합 표현
RULES = [
    ("quantity_unit_time", "regex", re.compile(r"[>≥<]?\d+(?:\.\d+)?(?:\s*[-~]\s*\d+(?:\.\d+)?)?\s*(?:°C|%\+?|일|주|개월|시간|분|회|차)")),
    ("timing_session", "keyword", re.compile(r"당일|같은 날|동일 세션|별도 세션|원데이|즉시|이후|이내|후에도|이상 대기|대기|간격")),
    ("order_direction", "keyword", re.compile(r"→|먼저|나중에|나중|마지막|다음|전에|선행|역순|순서|뒤에|후(?=[ ,\)]|$)|이후|(?<![가-힣])전(?=[ ,]|$)")),
    ("negation_prohibition", "keyword", re.compile(r"금지|않[가-힣]*|아님|아직|미허가|부족[가-힣]*|피함|불가|없[가-힣]*|아닌")),
    ("possibility_risk", "keyword", re.compile(r"가능[가-힣]*|위험|소지|수 있[가-힣]*")),
    ("necessity_recommendation", "keyword", re.compile(r"필수|필요[가-힣]*|권장|권고|한정|한해|준수|만\s사용|으로 한정")),
    ("condition_scope", "keyword", re.compile(r"[가-힣A-Za-z]+ 시(?=[ ,])|경우|하에|에 한해|에 한정|이상(?=[ ,]|$)|최소|범위|국소 부위|전안면|같은 부위|동일 부위|모든|등(?=[ )\.,]|$)|(?<=[가-힣] )중(?=[ ,]|$)|에는|에도|면(?= )")),
    ("hedge_degree", "keyword", re.compile(r"웬만하면|보수적으로|충분한|극대화|유연|높은|낮은|일률|개별|실제|많고|이론적|기본값|기본(?=[ ,]|$)|완전|촉진|정밀|넓은|어느 순서든")),
    ("evidence_citation", "regex", re.compile(r"(?:JCD|ASDS|AAD|ASPS|PRS|Global Aesthetics Consensus|Derm Surg)(?:\s[A-Za-z]+)*(?:\s\d{4})?|RCT|in vitro|in vivo|전문가 합의[가-힣]*|전문가 컨센서스|컨센서스|합의 수준|임상 가이드|논문|근거[가-힣]*|연구")),
    ("category_code_ref", "regex", re.compile(r"M\d+(?:-[가-힣A-Za-z]+)?")),
    ("symbol_relation", "regex(구조 기호)", re.compile(r"→|\+|/|·|~|⚠️|>|(?<=[0-9가-힣A-Za-z])-(?=[0-9가-힣A-Za-z])")),
    ("parenthetical", "regex(괄호와 앞 어절)", re.compile(r"[^\s(]*\([^()]*\)")),
    ("latin_term", "regex(라틴 문자열)", re.compile(r"(?<!°)[A-Za-z][A-Za-z0-9\-]*(?:\s[A-Za-z][A-Za-z0-9\-]*)*")),
]
SENT_SPLIT = re.compile(r"(?<=\.)\s+(?=\S)|\s+—\s+|;\s+")

MANUAL = json.load(open(os.path.join(HERE, "manual-expressions.json"), encoding="utf-8"))
exprs = []
manual_errors = []


def add(ptr, a, b, cat, method, extra=None):
    v = VBY[ptr]["text"] if ptr in VBY else BYPTR[ptr]["value"]
    e = {"pointer": ptr, "span": [a, b], "text": v[a:b], "category_candidate": cat, "method": method}
    if extra:
        e.update(extra)
    e["context"] = BYPTR[ptr]["context"]
    exprs.append(e)


for v in values:
    ptr, s = v["pointer"], v["text"]
    add(ptr, 0, len(s), "segment.value", "값 전체")
    # 문장·절 분할(regex). 값 전체와 같으면 생략
    pos = 0
    pieces = []
    for m in SENT_SPLIT.finditer(s):
        if s[:m.start()].count("(") > s[:m.start()].count(")"):
            continue  # 괄호 안 구분자는 절 경계로 쓰지 않는다
        pieces.append((pos, m.start()))
        pos = m.end()
    pieces.append((pos, len(s)))
    if len(pieces) > 1:
        for a, b in pieces:
            if b > a:
                add(ptr, a, b, "segment.clause", "regex 절 분할: '.' 뒤 공백, ' — ', '; ' 기준(괄호 안 제외)")
    for cat, meth, rx in RULES:
        for m in rx.finditer(s):
            if m.end() > m.start():
                add(ptr, m.start(), m.end(), cat, meth + ": " + rx.pattern[:60])
    # Kiwi 품사 기반: 부사(MAG)·관형사(MM)·부정지정사(VCN)·보조용언(VX) 포함 어절 + 다음 어절
    words = [(m.start(), m.end()) for m in re.finditer(r"\S+", s)]
    for t in v["tokens"]:
        if t["tag"] in ("MAG", "MM", "VCN", "VX", "MAJ"):
            wi = next(i for i, (a, b) in enumerate(words) if a <= t["span"][0] < b)
            a = words[wi][0]
            b = words[min(wi + 1, len(words) - 1)][1]
            add(ptr, a, b, "modifier_phrase", f"Kiwi 품사 {t['tag']}('{t['form']}') 포함 어절+다음 어절",
                {"kiwi_token": [t["form"], t["tag"], t["span"]]})

for m in MANUAL["phrases"]:
    ptr = m["pointer"]
    s = VBY[ptr]["text"] if ptr in VBY else None
    if s is None:
        manual_errors.append(f"manual: 분석 값 없음 {ptr}")
        continue
    hits = [i for i in range(len(s)) if s.startswith(m["text"], i)]
    occ = m.get("occurrence", 0)
    if len(hits) <= occ:
        manual_errors.append(f"manual: 원문에 없음 {ptr} {m['text']!r}")
        continue
    a = hits[occ]
    add(ptr, a, a + len(m["text"]), m["category_candidate"], "manual(직접 읽기)",
        {"reading_note": m.get("note"), "manual_id": m["id"]})
log(f"manual phrases={len(MANUAL['phrases'])} errors={len(manual_errors)}")
for e in manual_errors:
    log("  " + e)

# 중복 제거 금지: 같은 (pointer, span, category, method) 가 두 번 생기면 생성 오류로 센다
sig = {}
dup_gen = []
for e in exprs:
    k = (e["pointer"], tuple(e["span"]), e["category_candidate"], e["method"])
    if k in sig:
        dup_gen.append(k)
    sig[k] = 1
exprs.sort(key=lambda e: (BYPTR[e["pointer"]]["span"][0], e["span"][0], -e["span"][1], e["category_candidate"]))
for i, e in enumerate(exprs):
    e["id"] = f"E{i:05d}"
log(f"expressions={len(exprs)} duplicate_generation={len(dup_gen)}")

EXPR = {"source": SOURCE,
        "method": {"note": "범주는 탐색 관점의 후보 표시이며 확정 분류가 아니다. regex·keyword·품사·수동목록 결과를 전수 의미 해석으로 쓰지 않는다. 같은 구간이 여러 범주에 겹치는 것은 의도된 겹침이다. 'manual(직접 읽기)' 는 원문을 읽고 함께 보존해야 할 구절로 고른 것이다.",
                   "span": "값 문자열 기준 코드 포인트 [start,end). 파일 기준 = source-map 의 value_span[0] + start",
                   "rules": [{"category_candidate": c, "method": m, "pattern": r.pattern} for c, m, r in RULES]
                   + [{"category_candidate": "segment.clause", "method": "regex 절 분할", "pattern": SENT_SPLIT.pattern},
                      {"category_candidate": "modifier_phrase", "method": "Kiwi 품사 MAG/MM/VCN/VX/MAJ 포함 어절+다음 어절", "pattern": None}],
                   "known_false_positives": MANUAL.get("known_false_positives", [])},
        "expressions": exprs}

# 알려진 오탐 기록이 실제 표현을 가리키는지 확인
fp_errors = []
for fp in MANUAL.get("known_false_positives", []):
    ok = any(e["pointer"] == fp["pointer"] and e["span"] == fp["span"] and e["category_candidate"] == fp["category_candidate"]
             for e in exprs)
    if not ok:
        fp_errors.append(f"fp: 대응 표현 없음 {fp}")
for e in fp_errors:
    log("  " + e)

# ---------------------------------------------------------------- source-map
SRCMAP = {"source": SOURCE,
          "notes": ["span: 파일 전체 텍스트 기준 코드 포인트 [start,end). 문자열 노드의 span 은 따옴표 포함(JSON 리터럴), value_span 은 따옴표 제외(리터럴 내부). 이스케이프가 있으면 value_span slice 와 디코딩 값이 다를 수 있으나 이 원장은 백슬래시 0개라 동일하다.",
                    "byte_span: UTF-8 파일 바이트 [start,end).",
                    "context: 상위 블록·항목 위치·같은 항목의 형제 필드 Pointer. 구조적 사실(순서·계층)만 기록하며 의미 정합을 승인하지 않는다.",
                    "비문자열 말단은 json_literal(원문 리터럴)과 value(파싱 값)를 함께 둔다."],
          "duplicate_keys": P.duplicates,
          "field_name_occurrences": FIELD_OCC,
          "keys": P.keys,
          "nodes": NODES}

# ---------------------------------------------------------------- 내장 기계 검증
checks = []


def check(name, ok, detail=""):
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    log(f"[{'OK' if ok else 'FAIL'}] {name} {detail}")


ref = json.loads(text)


def resolve(obj, ptr):
    for p in ptr.split("/")[1:]:
        p = p.replace("~1", "/").replace("~0", "~")
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    return obj


bad = 0
for n in NODES:
    r = resolve(ref, n["pointer"])
    if n["type"] in ("object", "array"):
        if len(r) != n["length"]:
            bad += 1
    elif r != n["value"] or type(r) is not type(n["value"]):
        bad += 1
    if json.loads(text[n["span"][0]:n["span"][1]]) != r:
        bad += 1
    if raw[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") != text[n["span"][0]:n["span"][1]]:
        bad += 1
check("노드 정방향(Pointer 해소·span 재파싱·byte_span 디코딩)", bad == 0, f"nodes={len(NODES)} bad={bad}")

# 역방향: json.loads 결과의 모든 위치가 노드로 있는지
allp = []


def walk(o, p):
    allp.append(p)
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + "/" + esc_ptr(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{p}/{i}")


walk(ref, "")
check("노드 역방향(json.loads 위치 전부 존재)", set(allp) == set(BYPTR) and len(allp) == len(NODES),
      f"loads={len(allp)} nodes={len(NODES)}")
check("중복 키 0", not P.duplicates, str(len(P.duplicates)))
check("문자열 value_span == 값", all(text[n["value_span"][0]:n["value_span"][1]] == n["value"] for n in NODES if n["type"] == "string"))
strs = [n for n in NODES if n["type"] == "string"]
check("문자열 노드 = analyze + exclude", len(strs) == len(values) + len(excluded)
      and {n["pointer"] for n in strs} == {v["pointer"] for v in values} | {e["pointer"] for e in excluded},
      f"strings={len(strs)} analyze={len(values)} exclude={len(excluded)}")
tb = sum(1 for v in values for t in v["tokens"] if v["text"][t["span"][0]:t["span"][1]] != t["surface"])
check("형태소 surface == text[span]", tb == 0, f"tokens={sum(len(v['tokens']) for v in values)}")
eb = sum(1 for e in exprs if (VBY[e["pointer"]]["text"] if e["pointer"] in VBY else BYPTR[e["pointer"]]["value"])[e["span"][0]:e["span"][1]] != e["text"])
check("표현 text == 값[span]", eb == 0, f"expressions={len(exprs)}")
check("표현 생성 중복 0", not dup_gen, str(dup_gen[:3]))
check("수동 표현 원문 존재", not manual_errors, str(len(manual_errors)))
check("오분절 기록 원문·원시토큰 일치", not seg_errors, str(len(seg_errors)))
check("알려진 오탐 기록 대응", not fp_errors, str(len(fp_errors)))
SHA_END = sha(open(SRC, "rb").read())
check("원본 해시 불변(build 시작/끝)", SHA_START == SHA_END, SHA_END)
SOURCE["sha256_end"] = SHA_END


# ---------------------------------------------------------------- review.md 생성
def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def jt(n):
    t = n["type"]
    if t == "array":
        kinds = sorted({BYPTR[f"{n['pointer']}/{i}"]["type"] for i in range(n["length"])})
        return f"array[{n['length']}] of {'/'.join(kinds) or '(빈 배열)'}"
    if t == "object":
        return f"object{{{n['length']}}}"
    return t


notes_raw = open(os.path.join(HERE, "review-notes.md"), encoding="utf-8").read()
NOTES = {}
cur = None
for line in notes_raw.split("\n"):
    m = re.match(r"^@@(\S+)\s*$", line)
    if m:
        cur = m.group(1)
        NOTES[cur] = []
        continue
    if cur:
        NOTES[cur].append(line)
NOTES = {k: "\n".join(v).strip() + "\n" for k, v in NOTES.items()}

out = []
out.append(NOTES.get("header", ""))
out.append("## 2. 컬럼 구성 표 (자동 생성 — 원본 컬럼명·경로 패턴 그대로)\n")
out.append("경로 패턴의 `*` 는 배열 색인. 「출현」은 그 패턴에 실제로 있는 노드 수, 「자료형」은 그 패턴의 실제 노드 자료형(변형이 있으면 행을 나눔). 예시는 첫 출현의 원문 JSON 리터럴과 Pointer.\n")
out.append("| 원본 컬럼명 | 경로 패턴 | 자료형 / 중첩 | 출현 | 원문 예시(JSON 리터럴) | 예시 위치 | 비고(구조 사실) |")
out.append("|---|---|---|---|---|---|---|")
pat_rows = {}
for n in NODES:
    pat = re.sub(r"/\d+(?=/|$)", "/*", n["pointer"]) or "(루트)"
    pat_rows.setdefault((pat, jt(n) if n["type"] not in ("array",) else "array of " + "/".join(sorted({BYPTR[f"{n['pointer']}/{i}"]["type"] for i in range(n["length"])}))), []).append(n)
for (pat, t), ns in pat_rows.items():
    n0 = ns[0]
    name = pat.rsplit("/", 1)[-1] if pat != "(루트)" else "(루트)"
    name = "(배열 원소)" if name == "*" else name
    lit = text[n0["span"][0]:n0["span"][1]]
    if len(lit) > 70:
        lit = lit[:70] + "…"
    note = []
    if n0["type"] == "array":
        lens = sorted({x["length"] for x in ns})
        note.append("길이 " + ",".join(map(str, lens)))
    parent_pat = re.sub(r"/[^/]+$", "", pat)
    if "*" in pat and name != "*":
        parents = [x for x in NODES if (re.sub(r"/\d+(?=/|$)", "/*", x["pointer"]) == parent_pat)]
        if len(ns) < len(parents):
            note.append(f"선택적: {len(parents)}개 항목 중 {len(ns)}개에만 있음")
    if n0["type"] == "string" and any(x["value"] == "" for x in ns):
        note.append("빈 문자열 포함")
    out.append(f"| `{md(name)}` | `{md(pat)}` | {md(t)} | {len(ns)} | `{md(lit)}` | `{md(n0['pointer'])}` | {md('; '.join(note))} |")
out.append("")
out.append(NOTES.get("structure", ""))

BLOCK_TITLES = {"top": "3. 상위 스칼라", "principles": "4. principles", "sequence_order": "5. sequence_order",
                "incompatible_same_day": "6. incompatible_same_day", "common_combos": "7. common_combos",
                "minimum_intervals": "8. minimum_intervals"}


def leaf_lines(n):
    """항목 아래 모든 말단을 원본 컬럼명 그대로 (배열 원소는 순서·Pointer 포함)."""
    rows = []
    if n["type"] == "object":
        for k in n["children"]:
            c = BYPTR[f"{n['pointer']}/{esc_ptr(k)}"]
            if c["type"] == "array":
                if c["length"] == 0:
                    rows.append((k, "(빈 배열)", c["pointer"], "array[0]"))
                for i in range(c["length"]):
                    g = BYPTR[f"{c['pointer']}/{i}"]
                    rows.append((f"{k}[{i}]", g["value"] if g["type"] == "string" else g["json_literal"], g["pointer"], g["type"]))
            else:
                rows.append((k, c["value"] if c["type"] == "string" else c["json_literal"], c["pointer"], c["type"]))
    return rows


for block in ["top", "principles", "sequence_order", "incompatible_same_day", "common_combos", "minimum_intervals"]:
    out.append(f"## {BLOCK_TITLES[block]} — 원문 값 (자동 생성, 전부)\n")
    if block == "top":
        out.append("| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |")
        out.append("|---|---|---|---|")
        for k in BYPTR[""]["children"]:
            c = BYPTR["/" + k]
            if c["type"] == "string":
                out.append(f"| `{k}` | string | {md(c['value'])} | `/{k}` |")
            else:
                out.append(f"| `{k}` | {jt(c)} | (아래 절) | `/{k}` |")
    elif block == "principles":
        out.append("| 순서 | 원문 값 (`principles[i]`) | Pointer |")
        out.append("|---|---|---|")
        for i in range(BYPTR["/principles"]["length"]):
            out.append(f"| {i} | {md(BYPTR[f'/principles/{i}']['value'])} | `/principles/{i}` |")
    else:
        arr = BYPTR["/" + block]
        for i in range(arr["length"]):
            item = BYPTR[f"/{block}/{i}"]
            out.append(f"### `/{block}/{i}` — 키 {item['length']}개: {', '.join('`' + k + '`' for k in item['children'])}\n")
            out.append("| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |")
            out.append("|---|---|---|---|")
            for k, val, p, t in leaf_lines(item):
                out.append(f"| `{k}` | {t} | {md(val)} | `{p}` |")
            out.append("")
    out.append("")
    if block in NOTES:
        out.append(NOTES[block])
out.append(NOTES.get("footer", ""))
open(os.path.join(HERE, "review.md"), "w", encoding="utf-8").write("\n".join(out))

# ---------------------------------------------------------------- 쓰기
STATS = {"nodes": len(NODES), "keys": len(P.keys), "field_names": len(FIELD_OCC), "string_nodes": len(strs),
         "analyzed_values": len(values), "excluded_values": len(excluded), "non_string_leaves": len(non_string_leaves),
         "tokens": sum(len(v["tokens"]) for v in values), "field_name_tokens": sum(len(f["tokens"]) for f in field_names),
         "expressions": len(exprs), "manual_phrases": len(MANUAL["phrases"]),
         "segmentation_occurrences": len(SEG["occurrences"]), "known_false_positives": len(MANUAL.get("known_false_positives", []))}
log("stats " + json.dumps(STATS, ensure_ascii=False))


def dump(name, obj):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


dump("source-map.json", SRCMAP)
dump("morphology.json", MORPH)
dump("expressions.json", EXPR)
dump("validation-machine.json", {"source": SOURCE, "stats": STATS, "checks": checks,
                                 "failure_count": sum(1 for c in checks if not c["ok"])})
open(os.path.join(HERE, "build-output.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
if any(not c["ok"] for c in checks):
    sys.exit(1)
