"""procedure-profiles.json 1차 조사 재현 스크립트.

실행(레포 루트에서):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/build.py

산출: 같은 폴더의 source-map.json · morphology.json · expressions.json · validation-machine.json
원본은 읽기만 한다. 구간은 모두 디코딩된 문자열의 Unicode 코드 포인트 [start,end).
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.getcwd()
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json"
SRC = os.path.join(ROOT, SRC_REL)
OUT = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---------------------------------------------------------------- 1. 원본 고정
HASH_START = sha256(SRC)
RAW_BYTES = open(SRC, "rb").read()
TEXT = RAW_BYTES.decode("utf-8")
BYTE_OFF = [0]  # code point index -> byte offset
for ch in TEXT:
    BYTE_OFF.append(BYTE_OFF[-1] + len(ch.encode("utf-8")))


# ------------------------------------------- 자체 파서: 위치 + 중복 키 감지
class P:
    def __init__(self, s):
        self.s, self.i = s, 0
        self.nodes, self.keys, self.dups = [], [], []

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n":
            self.i += 1

    def esc_pointer(self, k):
        return k.replace("~", "~0").replace("/", "~1")

    def value(self, ptr, parent, key):
        self.ws()
        c, start = self.s[self.i], self.i
        if c == "{":
            node = {"pointer": ptr, "parent": parent, "key": key, "type": "object", "span": None, "children": []}
            self.nodes.append(node)
            self.i += 1
            seen = {}
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    ks = self.i
                    k = self.string()
                    ke = self.i
                    if k in seen:
                        self.dups.append({"object": ptr, "key": k, "first_span": seen[k], "dup_span": [ks, ke]})
                    seen[k] = [ks, ke]
                    cptr = ptr + "/" + self.esc_pointer(k)
                    self.keys.append({"key": k, "object_pointer": ptr, "value_pointer": cptr, "span": [ks, ke]})
                    node["children"].append(k)
                    self.ws()
                    assert self.s[self.i] == ":"
                    self.i += 1
                    self.value(cptr, ptr, k)
                    self.ws()
                    if self.s[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.s[self.i] == "}"
                    self.i += 1
                    break
            node["span"] = [start, self.i]
            node["length"] = len(node["children"])
            return
        if c == "[":
            node = {"pointer": ptr, "parent": parent, "key": key, "type": "array", "span": None}
            self.nodes.append(node)
            self.i += 1
            n = 0
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(ptr + "/" + str(n), ptr, n)
                    n += 1
                    self.ws()
                    if self.s[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.s[self.i] == "]"
                    self.i += 1
                    break
            node["span"] = [start, self.i]
            node["length"] = n
            return
        if c == '"':
            v = self.string()
            self.nodes.append({"pointer": ptr, "parent": parent, "key": key, "type": "string", "value": v,
                               "span": [start, self.i], "value_span": [start + 1, self.i - 1]})
            return
        m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.s, self.i)
        assert m, f"parse error at {self.i}"
        tok = m.group(0)
        self.i = m.end()
        if tok in ("true", "false"):
            t, v = "boolean", tok == "true"
        elif tok == "null":
            t, v = "null", None
        else:
            t, v = "number", json.loads(tok)
        self.nodes.append({"pointer": ptr, "parent": parent, "key": key, "type": t, "value": v,
                           "raw": tok, "span": [start, self.i]})

    def string(self):
        assert self.s[self.i] == '"'
        j = self.i + 1
        while self.s[j] != '"':
            if self.s[j] == "\\":
                j += 1
            j += 1
        lit = self.s[self.i:j + 1]
        self.i = j + 1
        return json.loads(lit)


p = P(TEXT)
p.value("", None, None)
p.ws()
assert p.i == len(TEXT), "trailing content"
NODES, KEYS, DUPS = p.nodes, p.keys, p.dups
BY_PTR = {n["pointer"]: n for n in NODES}
DATA = json.loads(TEXT)


def resolve(doc, ptr):
    cur = doc
    if ptr == "":
        return cur
    for part in ptr.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def context(ptr):
    m = re.match(r"^/profiles/(\d+)(/([^/]+))?(/(\d+))?", ptr)
    if not m:
        return {"block": "top", "profile_index": None}
    idx = int(m.group(1))
    prof = DATA["profiles"][idx]
    ctx = {"block": f"profile[{idx}]", "profile_index": idx, "profile_pointer": f"/profiles/{idx}",
           "profile_id": prof.get("id"), "profile_name": prof.get("name")}
    if m.group(3):
        ctx["field"] = m.group(3)
        ctx["field_pointer"] = f"/profiles/{idx}/{m.group(3)}"
        if m.group(5) is not None:
            ctx["item_index"] = int(m.group(5))
            ctx["array_length"] = len(prof[m.group(3)])
    return ctx


for n in NODES:
    n["byte_span"] = [BYTE_OFF[n["span"][0]], BYTE_OFF[n["span"][1]]]
    n["context"] = context(n["pointer"])
for k in KEYS:
    k["byte_span"] = [BYTE_OFF[k["span"][0]], BYTE_OFF[k["span"][1]]]
    k["context"] = context(k["value_pointer"])

# 필드명 출현 위치 집계
field_occ = {}
for k in KEYS:
    gen = re.sub(r"/\d+", "/*", k["value_pointer"])
    field_occ.setdefault(k["key"], {}).setdefault(gen, []).append(k["value_pointer"])

# --------------------------------- 형태소 분석 적용/제외 판정 (텍스트 값)
ID_RE = re.compile(r"^M\d+$")
SNAKE_RE = re.compile(r"^[a-z]+(_[a-z]+)*$")
VERSION_RE = re.compile(r"^\d+(\.\d+)+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def exclusion(n):
    v, key = n["value"], n["key"]
    if ID_RE.match(v):
        return "identifier: 항목 ID(Mxx). 언어 표현 아님 — 원문 보존, 구조 사실로만 기록"
    if VERSION_RE.match(v):
        return "version string: 숫자·점 버전 표기"
    if DATE_RE.match(v):
        return "date string: ISO 날짜"
    if SNAKE_RE.match(v):
        return "enum-like code: 영문 소문자 snake_case 코드값(phase·mechanism·needsAnesthesia·position). 언어 분석 대신 코드값으로 보존"
    return None


STRINGS = [n for n in NODES if n["type"] == "string"]

from kiwipiepy import Kiwi  # noqa: E402
import kiwipiepy  # noqa: E402

kiwi = Kiwi()
KIWI_OPTS = {"tokenize_kwargs": "기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, blocklist=None, compatible_jamo=False, split_sents=False)",
             "user_dictionary": "없음", "model_type": getattr(kiwi, "model_type", None),
             "kiwipiepy": kiwipiepy.__version__, "typos": None}


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
        excluded.append({"pointer": n["pointer"], "value": n["value"], "reason": ex, "context": n["context"]})
        continue
    morph_records.append({"source": "value", "pointer": n["pointer"], "text": n["value"],
                          "file_span_of_text": n["value_span"], "context": n["context"],
                          "tokens": analyze(n["value"])})

field_names = sorted({k["key"] for k in KEYS})
field_morph = [{"source": "field_name", "field_name": f, "occurrence_patterns": sorted(field_occ[f].keys()),
                "occurrence_count": sum(len(v) for v in field_occ[f].values()),
                "tokens": analyze(f)} for f in field_names]

# ------------------------------------------- 오분절·미등록어 후보 (기계 표시)
seg_flags = []
for r in morph_records:
    toks = r["tokens"]
    for i, t in enumerate(toks):
        reasons = []
        if t["tag"] in ("UN", "W_SERIAL", "W_HASHTAG", "W_MENTION", "W_URL", "W_EMAIL", "W_EMOJI"):
            reasons.append(f"tag {t['tag']}")
        if t["tag"] == "NNP":
            reasons.append("NNP(고유명사 추정) — 원문 대조 필요")
        if t["tag"] == "XR":
            reasons.append("XR 어근")
        if t["tag"] in ("SL", "SH"):
            reasons.append(f"{t['tag']} 외국어/한자")
        if t["tag"] in ("SO", "SW", "SP", "SS", "SSO", "SSC", "SE"):
            if t["form"] in ("→", "+", "/", "·", "~", "-", "X"):
                reasons.append(f"기호 '{t['form']}' — 구조 기호 역할 원문 대조")
        if reasons:
            seg_flags.append({"pointer": r["pointer"], "token_index": i, "form": t["form"], "tag": t["tag"],
                              "span": t["span"], "reasons": reasons})

# 직접 원문 대조로 확인한 오분절·오태깅 규칙. 규칙마다 실제 출현 토큰을 찾아 기록한다(규칙 hit 0 = 오류).
TEXTS_M = {r["pointer"]: r["text"] for r in morph_records}
SEG_RULES = json.load(open(os.path.join(OUT, "segmentation-review-rules.json"), encoding="utf-8"))
seg_review, seg_rule_nohit = [], []
for rule in SEG_RULES:
    hits = 0
    for r in morph_records:
        text = r["text"]
        for m in re.finditer(re.escape(rule["phrase"]), text):
            a, b = m.start(), m.end()
            toks = [t for t in r["tokens"] if a <= t["span"][0] < b]
            if not rule["tokens"]:
                found = [t for t in r["tokens"] if t["tag"] == "W_SERIAL" and t["span"][0] < b and t["span"][1] > a] if rule["phrase"] == "-" else []
                if found:
                    seg_review.append({"rule": rule["id"], "pointer": r["pointer"], "phrase_span": [a, b],
                                       "tokens": [(t["form"], t["tag"], t["span"]) for t in found], "kind": rule["kind"], "issue": rule["issue"]})
                    hits += 1
                continue
            for i in range(len(toks) - len(rule["tokens"]) + 1):
                if all((toks[i + j]["form"], toks[i + j]["tag"]) == tuple(rule["tokens"][j]) for j in range(len(rule["tokens"]))):
                    seg_review.append({"rule": rule["id"], "pointer": r["pointer"], "phrase_span": [a, b],
                                       "phrase": text[a:b],
                                       "tokens": [(toks[i + j]["form"], toks[i + j]["tag"], toks[i + j]["span"]) for j in range(len(rule["tokens"]))],
                                       "kind": rule["kind"], "issue": rule["issue"]})
                    hits += 1
                    break
    if hits == 0:
        seg_rule_nohit.append(rule["id"])


# 출현 단위 판정: 지정 품사 전부 + 의미위험 서명 전부를 모든 값에서 훑은 결과(segmentation-occurrence-review.json)
OCC = json.load(open(os.path.join(OUT, "segmentation-occurrence-review.json"), encoding="utf-8"))
OCC_SCOPE_TAGS = set(OCC["scope"]["sweep_tags"])
OCC_SCOPE_SIGS = {tuple(x) for x in OCC["scope"]["signatures"]}
OCC_BY_KEY = {}
occ_dup = []
for o in OCC["occurrences"]:
    k = (o["pointer"], o["span"][0], o["span"][1], o["form"], o["tag"])
    if k in OCC_BY_KEY:
        occ_dup.append(k)
    OCC_BY_KEY[k] = o
occ_missing, occ_stale = [], []
live_keys = set()
for r in morph_records:
    for t in r["tokens"]:
        k = (r["pointer"], t["span"][0], t["span"][1], t["form"], t["tag"])
        if t["tag"] in OCC_SCOPE_TAGS or (t["form"], t["tag"]) in OCC_SCOPE_SIGS:
            live_keys.add(k)
            if k not in OCC_BY_KEY:
                occ_missing.append(k)
occ_stale = [k for k in OCC_BY_KEY if k not in live_keys]
covered = {(s["pointer"], tok[2][0], tok[2][1], tok[0], tok[1]) for s in seg_review for tok in s["tokens"]}
for o in OCC["occurrences"]:
    if o["verdict"] == "correct":
        continue
    k = (o["pointer"], o["span"][0], o["span"][1], o["form"], o["tag"])
    if k not in covered:
        txt = TEXTS_M[o["pointer"]]
        seg_review.append({"rule": o["rule"], "source": "occurrence_sweep", "pointer": o["pointer"],
                           "phrase_span": o["span"], "phrase": txt[o["span"][0]:o["span"][1]],
                           "tokens": [(o["form"], o["tag"], o["span"])], "kind": o["verdict"], "issue": o["reason"]})
for s_ in seg_review:
    s_.setdefault("source", "phrase_rule")
    s_["status"] = "표시됨(교정 아님) — 원시 Kiwi 토큰 유지"
# 대응 검사: 판정 mis-* 출현 ↔ seg_review 토큰 (범위 안 서명만)
seg_keys = {(s["pointer"], tok[2][0], tok[2][1], tok[0], tok[1]) for s in seg_review for tok in s["tokens"]}
occ_mis_not_marked = [k for k, o in OCC_BY_KEY.items() if o["verdict"] != "correct" and k not in seg_keys]
marked_but_correct = [k for k in seg_keys if k in OCC_BY_KEY and OCC_BY_KEY[k]["verdict"] == "correct"]


def split_identifier(name):
    """분석기 미지원 보완: camelCase/snake_case 를 규칙으로 나눈다(형태소 분석 아님)."""
    parts = []
    for chunk in name.split("_"):
        parts += re.findall(r"[A-Z]{2,}(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|[A-Z]+|\d+", chunk)
    return parts


for f in field_morph:
    f["identifier_parts_rule_based"] = split_identifier(f["field_name"])

# ------------------------------------------------- 2. 복합 표현 후보 수집
TEXTS = {r["pointer"]: r["text"] for r in morph_records}
exprs = []


def add(ptr, s, e, cat, method, note=None):
    exprs.append({"pointer": ptr, "span": [s, e], "text": TEXTS[ptr][s:e], "category_candidate": cat,
                  "method": method, **({"note": note} if note else {})})


RULES = [
    ("segment.sentence", "regex 문장분할: 값 전체를 '. ' 또는 '; ' 뒤 공백 기준으로 자름", None),
    ("quantity_unit_time", "regex", re.compile(
        r"(?:SPF)?\d+(?:\.\d+)?(?:\s*(?:~|-)\s*\d+(?:\.\d+)?)?\s*(?:U|ml|mm|G|%|분|시간|일|주|개월|회|개|\+)?"
        r"(?:/\d+(?:\.\d+)?(?:~\d+(?:\.\d+)?)?\s*ml)?(?:\s*(?:전|후|내|이내|간|까지|부터|이상|에 걸쳐|동안))?")),
    ("quantity_unit_time", "regex(비숫자 수량)", re.compile(r"수\s*(?:시간|십\s*시간|천\s*개)(?:~수십\s*시간)?|수 시간~수십 시간")),
    ("timing", "keyword", re.compile(r"당일|직후|즉시|즉각|시간 지체 없이|맨 처음|마지막|같은 날|시술 전|시술 후|시술 중|시술 직후|"
                                    r"시술 시작 전|전에|뒤에|후에|먼저|이후|미리|점진적으로|점차|서서히|생착 완료")),
    ("negation_prohibition", "keyword", re.compile(r"금지|불가|불필요|않[가-힣]*|없[가-힣]*|아닌|아니[가-힣]*|미확인|미입증|"
                                                  r"비추|자제|피하[가-힣]*|피해야|위법|X(?=\)| |$)|제한적|절대")),
    ("negation_phrase", "regex(부정·금지와 앞 어절)", re.compile(r"[^\s,()]+지\s+않[가-힣]*|[^\s,()]+\s+(?:절대\s+)?금지|[^\s,()]+\s+아닌|[^\s,()]+\s+없[가-힣]*|[^\s,()]+\s+불가|[^\s,()]+\s+자제|[^\s,()]+\s+피하[가-힣]*")),
    ("possibility_risk", "keyword", re.compile(r"가능|수 있[가-힣]*|위험[가-힣]*|대개|약 (?=\d)|정상|자연스러운")),
    ("condition_scope", "keyword", re.compile(r"[가-힣A-Za-z]+\s?시(?=[ ,.)])|[가-힣A-Za-z]+이면|[가-힣]+(?<!으)면(?= )|경우|에 따라|따라|에 한함|"
                                             r"만 |에서만|별로|여부")),
    ("necessity_recommendation", "keyword", re.compile(r"필수|필요[가-힣]*|권장[가-힣]*|반드시|충분[가-힣]*|철저|확인")),
    ("comparison_degree", "keyword", re.compile(r"가장|최소|최대|이상|이내|높[가-힣]*|낮[가-힣]*|크[므고]|큼|적음|김|미미|극대화|"
                                               r"강하게|강한|과도한|과격한|격한|극심한|급격한|약간의|가벼운|부드럽[가-힣]*|"
                                               r"충분한|미량|미세|얇은|깊이|심부|상층|정밀|선택적|균질한|자잘한")),
    ("reason_purpose", "keyword", re.compile(r"[가-힣]*(?:이므로|으므로)|[가-힣]+하여|때문[가-힣]*|위해|대비|목적|방지|예방|[가-힣]+(?<=[가-힣])로 인한|에 의해")),
    ("scope_listing_alternative", "keyword", re.compile(r"(?<=[가-힣A-Za-z)] )등(?=[ ,)]|$)|(?<=[가-힣A-Za-z])등(?= )|\b등(?=을|의)|또는|\bor\b|(?<= )외(?= )|[가-힣A-Za-z]+별(?=[ ,]|$)|양쪽|단독|모든|다른|특정|개별|실제|명확히|각각|전신|일부")),
    ("comparison_degree", "keyword(보강)", re.compile(r"고강도|초극대|중대|점진적|[가-힣]+(?:ㄹ|을)?수록|지날수록|달라[가-힣]*|다름|유사[가-힣]*|정형화된|조기|불균형한|물리적|구조적|전통적[가-힣]*|미온수|너무|빠르[가-힣]*|자연(?= )")),
    ("symbol_relation", "regex(구조 기호)", re.compile(r"→|\+|/|·|~|=|(?<=[0-9가-힣A-Za-z])-(?=[0-9가-힣A-Za-z])")),
    ("parenthetical", "regex(괄호와 앞 어절)", re.compile(r"[^\s(]*\([^()]*\)")),
    ("latin_term", "regex(라틴 문자열)", re.compile(r"[A-Za-z][A-Za-z0-9\-]*(?:\s[A-Za-z][A-Za-z0-9\-]*)*")),
]

for r in morph_records:
    ptr, text = r["pointer"], r["text"]
    # 값 전체
    add(ptr, 0, len(text), "segment.value", "값 전체")
    # 문장 분할
    starts = [0] + [m.end() for m in re.finditer(r"(?<=[.;])\s+", text)]
    if len(starts) > 1:
        bounds = starts + [len(text) + 1]
        for a, b in zip(bounds, bounds[1:]):
            seg_end = b - 1 if b <= len(text) else len(text)
            seg = text[a:seg_end].rstrip()
            add(ptr, a, a + len(seg), "segment.sentence", RULES[0][1])
    # 화살표 분할
    if "→" in text:
        pos = 0
        for part in text.split("→"):
            s = pos + (len(part) - len(part.lstrip()))
            e = pos + len(part.rstrip())
            add(ptr, s, e, "segment.arrow_part", "'→' 기준 분할(좌우 구절)")
            pos += len(part) + 1
    for cat, method, rx in RULES[1:]:
        for m in rx.finditer(text):
            if m.end() > m.start() and m.group(0).strip():
                s = m.start() + (len(m.group(0)) - len(m.group(0).lstrip()))
                e = m.end() - (len(m.group(0)) - len(m.group(0).rstrip()))
                if cat == "quantity_unit_time" and not re.search(r"\d|수", text[s:e]):
                    continue
                add(ptr, s, e, cat, method)
    # 품사 기반 수식어: MAG/VA/XR 를 포함한 어절과 다음 어절
    eoj = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    for t in r["tokens"]:
        if t["tag"] in ("MAG", "MM", "VA", "VA-I", "VA-R", "XR", "VCN", "MAJ"):
            for k, (a, b) in enumerate(eoj):
                if a <= t["span"][0] < b:
                    e = eoj[k + 1][1] if k + 1 < len(eoj) else b
                    add(ptr, a, e, "modifier_phrase", f"Kiwi 품사 {t['tag']}('{t['form']}') 포함 어절+다음 어절")
                    exprs[-1]["source_token"] = {"form": t["form"], "tag": t["tag"], "span": t["span"]}
                    break

# 수동 목록: 직접 읽으며 고른 다어절·명칭 표현. 모든 값에서 정확 부분문자열 출현을 전부 찾는다.
MANUAL = json.load(open(os.path.join(OUT, "manual-expressions.json"), encoding="utf-8"))
manual_missing = []
for item in MANUAL:
    hits = 0
    for ptr, text in TEXTS.items():
        for m in re.finditer(re.escape(item["text"]), text):
            a, b = m.start(), m.end()
            emb = (a > 0 and re.match(r"[0-9A-Za-z가-힣.]", text[a - 1]) and re.match(r"[0-9A-Za-z가-힣]", text[a])) or \
                  (b < len(text) and re.match(r"[0-9.]", text[b]) and re.match(r"[0-9]", text[b - 1]))
            note = item.get("note")
            if emb:
                note = (note or "") + " | embedded=true: 더 큰 어절/수치 안의 부분 일치(예: '5분'⊂'15분'). 독립 표현 아닐 수 있음"
            add(ptr, a, b, item["category_candidate"], "manual_list+exact_substring", note)
            hits += 1
    if hits == 0:
        manual_missing.append(item["text"])

# 같은 (pointer, span, category, method) 완전 중복 제거 — 기록
seen, dedup, dup_removed = set(), [], 0
for x in exprs:
    k = (x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"])
    if k in seen:
        dup_removed += 1
        continue
    seen.add(k)
    dedup.append(x)
exprs = dedup
# 원문 대조로 확인한 기계 추출 오탐. 지우지 않고 review 로 표시한다.
EXPR_REVIEW = json.load(open(os.path.join(OUT, "expression-review.json"), encoding="utf-8"))["entries"]
ER_BY_KEY = {(e_["pointer"], e_["span"][0], e_["span"][1], e_["category_candidate"]): e_ for e_ in EXPR_REVIEW}
er_hits = {k: 0 for k in ER_BY_KEY}
derived_fp = []
for x in exprs:
    k = (x["pointer"], x["span"][0], x["span"][1], x["category_candidate"])
    if k in ER_BY_KEY:
        er = ER_BY_KEY[k]
        er_hits[k] += 1
        x["review"] = "false_positive: " + er["reason"]
        x["review_basis"] = {"source": "expression-review.json", "verdict": er["verdict"]}
    elif "source_token" in x:
        st = x["source_token"]
        o = OCC_BY_KEY.get((x["pointer"], st["span"][0], st["span"][1], st["form"], st["tag"]))
        if o and o["verdict"] != "correct":
            x["review"] = f"false_positive(오태깅 유래): 근거 토큰 {st['form']}/{st['tag']} @{st['span']} 판정 {o['verdict']} — {o['reason']}"
            x["review_basis"] = {"source": "segmentation-occurrence-review.json", "pointer": x["pointer"],
                                 "token_span": st["span"], "form": st["form"], "tag": st["tag"],
                                 "verdict": o["verdict"], "rule": o["rule"]}
            derived_fp.append(x)
    if "review" not in x and "embedded=true" in (x.get("note") or ""):
        x["review"] = "partial_match: 더 큰 어절 안의 부분 일치 — 원문 대조 필요"
for i, x in enumerate(exprs):
    x["id"] = f"E{i:05d}"
    x["context"] = BY_PTR[x["pointer"]]["context"]

# ------------------------------------------------------------- 3. 검증
checks = {}
# 해시
HASH_END = sha256(SRC)
checks["hash_unchanged"] = HASH_START == HASH_END
# 중복 키
checks["duplicate_keys"] = DUPS
# 양방향: 파서 노드 -> json.loads 값 / json.loads 전체 경로 -> 노드
fwd_bad = []
for n in NODES:
    v = resolve(DATA, n["pointer"])
    if n["type"] in ("string", "number", "boolean", "null"):
        if type(v) is not type(n["value"]) or v != n["value"]:
            fwd_bad.append(n["pointer"])
        if json.loads(TEXT[n["span"][0]:n["span"][1]]) != v:
            fwd_bad.append(n["pointer"] + " (span)")
    else:
        if json.loads(TEXT[n["span"][0]:n["span"][1]]) != v:
            fwd_bad.append(n["pointer"] + " (container span)")


def walk(v, ptr, acc):
    acc.append((ptr, v))
    if isinstance(v, dict):
        for k, c in v.items():
            walk(c, ptr + "/" + k.replace("~", "~0").replace("/", "~1"), acc)
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, f"{ptr}/{i}", acc)


ALL = []
walk(DATA, "", ALL)
bwd_missing = [ptr for ptr, _ in ALL if ptr not in BY_PTR]
checks["forward_mismatch"] = fwd_bad
checks["backward_missing"] = bwd_missing
checks["node_count"] = len(NODES)
checks["json_loads_path_count"] = len(ALL)
checks["pointer_unique"] = len(BY_PTR) == len(NODES)
# 문자열 값 구간: 이스케이프 없으면 원문 slice == 값
checks["string_value_slice_mismatch"] = [n["pointer"] for n in STRINGS if TEXT[n["value_span"][0]:n["value_span"][1]] != n["value"]]
# 키 구간
checks["key_slice_mismatch"] = [k["value_pointer"] for k in KEYS if TEXT[k["span"][0]:k["span"][1]] != json.dumps(k["key"], ensure_ascii=False)]
# 바이트 구간
checks["byte_span_mismatch"] = [n["pointer"] for n in NODES if RAW_BYTES[n["byte_span"][0]:n["byte_span"][1]].decode("utf-8") != TEXT[n["span"][0]:n["span"][1]]]
# 형태소 적용/제외 대응
morph_ptrs = {r["pointer"] for r in morph_records}
ex_ptrs = {e["pointer"] for e in excluded}
checks["morph_both_or_neither"] = sorted((morph_ptrs & ex_ptrs) | ({n["pointer"] for n in STRINGS} - morph_ptrs - ex_ptrs))
checks["morph_applied_count"] = len(morph_ptrs)
checks["morph_excluded_count"] = len(ex_ptrs)
checks["field_names_analyzed"] = len(field_morph)
checks["field_names_total"] = len(field_names)
# 토큰 구간: 범위 안, surface == slice, 비어 있지 않음, 텍스트 커버(공백 외 모든 문자가 어떤 토큰에 덮임)
tok_bad, uncovered = [], []
for r in morph_records:
    cov = [False] * len(r["text"])
    for t in r["tokens"]:
        s, e = t["span"]
        if not (0 <= s < e <= len(r["text"])) or r["text"][s:e] != t["surface"]:
            tok_bad.append((r["pointer"], t))
        for i in range(max(s, 0), min(e, len(r["text"]))):
            cov[i] = True
    for i, c in enumerate(r["text"]):
        if not cov[i] and not c.isspace():
            uncovered.append({"pointer": r["pointer"], "index": i, "char": c})
checks["token_span_bad"] = tok_bad
checks["token_uncovered_nonspace_chars"] = uncovered
checks["token_count"] = sum(len(r["tokens"]) for r in morph_records)
checks["token_form_not_surface"] = sum(1 for r in morph_records for t in r["tokens"] if not t["form_equals_surface"])
# 표현 구간
checks["expr_slice_bad"] = [x["id"] for x in exprs if TEXTS[x["pointer"]][x["span"][0]:x["span"][1]] != x["text"] or not x["text"]]
checks["expr_count"] = len(exprs)
checks["expr_marked_false_positive"] = sum(1 for x in exprs if x.get("review", "").startswith("false_positive"))
checks["expr_marked_partial_match"] = sum(1 for x in exprs if x.get("review", "").startswith("partial_match"))
checks["expr_marked_false_positive_regex_keyword"] = sum(1 for x in exprs if x.get("review_basis", {}).get("source") == "expression-review.json")
checks["expr_marked_false_positive_mistag_derived"] = len(derived_fp)
checks["expression_review_entries_not_matched_once"] = [list(k) for k, n in er_hits.items() if n != 1]
checks["expression_review_text_mismatch"] = [list(k) for k, e_ in ER_BY_KEY.items() if TEXTS[k[0]][k[1]:k[2]] != e_["text"]]
# 오태깅 유래 대응: 판정 mis 토큰에서 만든 modifier 후보는 전부 표시, correct 토큰 유래는 표시 0
checks["mistag_derived_unmarked"] = [x["id"] for x in exprs if "source_token" in x and OCC_BY_KEY.get((x["pointer"], x["source_token"]["span"][0], x["source_token"]["span"][1], x["source_token"]["form"], x["source_token"]["tag"]), {}).get("verdict", "correct") != "correct" and "오태깅 유래" not in x.get("review", "")]
checks["modifier_without_source_token"] = [x["id"] for x in exprs if x["category_candidate"] == "modifier_phrase" and "source_token" not in x]
checks["modifier_source_token_not_in_occurrence_review"] = [x["id"] for x in exprs if "source_token" in x and x["source_token"]["tag"] in OCC_SCOPE_TAGS and (x["pointer"], x["source_token"]["span"][0], x["source_token"]["span"][1], x["source_token"]["form"], x["source_token"]["tag"]) not in OCC_BY_KEY]
checks["occurrence_review_count"] = len(OCC_BY_KEY)
checks["occurrence_review_verdicts"] = {v: sum(1 for o in OCC_BY_KEY.values() if o["verdict"] == v) for v in sorted({o["verdict"] for o in OCC_BY_KEY.values()})}
checks["occurrence_review_missing_tokens"] = occ_missing
checks["occurrence_review_stale_entries"] = occ_stale
checks["occurrence_review_duplicates"] = occ_dup
checks["occurrence_mis_not_in_segmentation_review"] = occ_mis_not_marked
checks["segmentation_review_marks_correct_token"] = marked_but_correct
checks["segmentation_review_from_occurrence_sweep"] = sum(1 for s_ in seg_review if s_["source"] == "occurrence_sweep")
checks["expr_exact_duplicates_removed"] = dup_removed
checks["segmentation_review_hits"] = len(seg_review)
checks["segmentation_rules_without_hit"] = seg_rule_nohit
checks["manual_terms"] = len(MANUAL)
checks["manual_terms_not_found"] = manual_missing
# 모든 형태소 대상 값에 표현(값 전체 segment)이 있는가
checks["values_without_value_segment"] = sorted(morph_ptrs - {x["pointer"] for x in exprs if x["category_candidate"] == "segment.value"})

# ------------------------------------------------------------- 4. 출력
SRC_INFO = {"path": SRC_REL, "size_bytes": len(RAW_BYTES), "code_points": len(TEXT),
            "sha256_start": HASH_START, "sha256_end": HASH_END, "encoding": "utf-8, BOM 없음, 개행 없음(한 줄)",
            "offset_unit": "디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end). byte_span 은 UTF-8 바이트 [start,end)"}

json.dump({"source": SRC_INFO,
           "notes": ["span: 파일 전체 텍스트 기준 코드 포인트 [start,end). 문자열 노드의 span 은 따옴표 포함, value_span 은 따옴표 제외.",
                     "원장에 이스케이프 문자가 없어 value_span slice == 디코딩 값 (validation 참고).",
                     "context 는 상위 항목·필드·배열 위치. 함께 해석할 주변 필드는 같은 profile_pointer 아래 형제 노드다.",
                     "구조적 사실(ID·순서·계층)을 기록할 뿐 의미적 정합을 승인하지 않는다."],
           "duplicate_keys": DUPS,
           "field_name_occurrences": {k: {g: v for g, v in sorted(d.items())} for k, d in sorted(field_occ.items())},
           "keys": KEYS, "nodes": NODES},
          open(os.path.join(OUT, "source-map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump({"source": SRC_INFO, "analyzer": {"name": "Kiwi (kiwipiepy)", **KIWI_OPTS,
                                             "tagset": "Kiwi 품사 체계(세종 기반 확장: NNG/NNP/NNB/VV/VA/MAG/J*/E*/X*/S*/W_* 등)",
                                             "lemma": "Kiwi Token.lemma 값 그대로(용언은 Kiwi 가 '다'를 붙인 기본형). 도메인 표준명 아님",
                                             "span": "각 값 문자열 기준 코드 포인트 [start,end). 파일 기준은 file_span_of_text[0]+start",
                                             "surface": "text[start:end]. 축약·불규칙 활용은 여러 형태소가 같은 구간을 공유(form_equals_surface=false)"},
           "excluded_values": excluded, "values": morph_records, "field_names": field_morph,
           "segmentation_flags": seg_flags,
           "segmentation_review_note": "직접 원문 대조로 확인한 오분절·오태깅. rules=segmentation-review-rules.json. 원래 토큰은 고치지 않고 이 목록으로 표시한다. 여기 없는 토큰이 정답이라는 뜻은 아니다(기계 표시 segmentation_flags 는 확인 후보).",
           "segmentation_review": seg_review,
           "field_name_note": "필드명은 Kiwi 가 camelCase 를 SL 한 토큰으로 처리(분석 미지원). identifier_parts_rule_based 는 규칙 분할 보완이며 형태소 분석 결과가 아니다."},
          open(os.path.join(OUT, "morphology.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump({"source": SRC_INFO,
           "method": {"note": "범주는 탐색 관점의 후보 표시이며 확정 분류가 아니다. regex·keyword·품사·수동목록 결과를 전수 의미 해석으로 쓰지 않는다. 같은 구간이 여러 범주에 겹치는 것은 의도된 겹침이다.",
                      "rules": [{"category_candidate": c, "method": m, "pattern": (rx.pattern if rx else None)} for c, m, rx in RULES],
                      "manual_list": "manual-expressions.json (직접 원문을 읽으며 고른 표현; 모든 값에서 정확 부분문자열 출현 전부 기록)"},
           "expressions": exprs},
          open(os.path.join(OUT, "expressions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

json.dump({"source": SRC_INFO, "checks": checks},
          open(os.path.join(OUT, "validation-machine.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

summary = {k: (v if not isinstance(v, list) else (len(v) if len(v) > 5 else v)) for k, v in checks.items()}
print(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
cats = {}
for x in exprs:
    cats[x["category_candidate"]] = cats.get(x["category_candidate"], 0) + 1
print(json.dumps(cats, ensure_ascii=False))
