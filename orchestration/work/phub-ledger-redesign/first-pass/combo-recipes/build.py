"""combo-recipes.json 1차 수집 빌드.

실행(레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/combo-recipes/build.py

원본은 읽기만 한다. 산출물은 이 폴더에만 쓴다:
  source-map.json · morphology.json · expressions.json · coverage.json · review.md · build-output.txt
수동 입력: manual-expressions.json · segmentation-review.json · manual-observations.json
"""
import hashlib
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/combo-recipes.json"
SRC = REPO / SRC_REL

LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- 원본 고정
HASH_START = sha256(SRC)
RAW = SRC.read_bytes()
TEXT = RAW.decode("utf-8")
BYTE_AT = [0]
for ch in TEXT:
    BYTE_AT.append(BYTE_AT[-1] + len(ch.encode("utf-8")))


def bspan(s, e):
    return [BYTE_AT[s], BYTE_AT[e]]


# ---------------------------------------------------------------- 자체 파서
def ptr_escape(k):
    return k.replace("~", "~0").replace("/", "~1")


class Parser:
    WS = " \t\r\n"

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.keys = []
        self.duplicates = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def string(self):
        s = self.i
        assert self.t[s] == '"'
        self.i += 1
        out = []
        esc = False
        while True:
            c = self.t[self.i]
            if c == '"':
                self.i += 1
                break
            if c == "\\":
                esc = True
                n = self.t[self.i + 1]
                if n == "u":
                    out.append(chr(int(self.t[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                else:
                    out.append({'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                                "n": "\n", "r": "\r", "t": "\t"}[n])
                    self.i += 2
                continue
            out.append(c)
            self.i += 1
        return "".join(out), [s, self.i], esc

    def value(self, ptr, parent, key, index, key_span):
        self.ws()
        s = self.i
        c = self.t[s]
        node = {"pointer": ptr, "parent": parent, "key": key, "index": index,
                "key_span": key_span}
        self.nodes.append(node)
        if c == "{":
            self.i += 1
            seen = {}
            order = []
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, kesc = self.string()
                    self.keys.append({"pointer": ptr + "/" + ptr_escape(k), "key": k,
                                      "span": ks, "byte_span": bspan(*ks), "has_escape": kesc,
                                      "occurrence_in_object": seen.get(k, 0)})
                    if k in seen:
                        self.duplicates.append({"object": ptr, "key": k, "span": ks})
                    seen[k] = seen.get(k, 0) + 1
                    order.append(k)
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    self.value(ptr + "/" + ptr_escape(k), ptr, k, None, ks)
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node.update(type="object", keys=order, child_count=len(order))
        elif c == "[":
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
            node.update(type="array", child_count=n)
        elif c == '"':
            v, sp, esc = self.string()
            node.update(type="string", value=v, has_escape=esc,
                        value_span=None if esc else [sp[0] + 1, sp[1] - 1])
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.t, s)
            lit = m.group(0)
            self.i = m.end()
            if lit in ("true", "false"):
                node.update(type="boolean", value=lit == "true")
            elif lit == "null":
                node.update(type="null", value=None)
            elif m.group(1) or m.group(2):
                node.update(type="number", value=float(lit))
            else:
                node.update(type="integer", value=int(lit))
        node["span"] = [s, self.i]
        node["byte_span"] = bspan(s, self.i)
        node["literal"] = self.t[s:self.i] if node["type"] not in ("object", "array") else None


P = Parser(TEXT)
P.value("", None, None, None, None)
P.ws()
assert P.i == len(TEXT), "trailing data"
NODES = P.nodes
BY_PTR = {n["pointer"]: n for n in NODES}
for i, n in enumerate(NODES):
    n["doc_order"] = i
    n["leaf"] = n["type"] not in ("object", "array") or n["child_count"] == 0
    n["path_pattern"] = re.sub(r"/\d+(?=/|$)", "/[]", n["pointer"]) or "(root)"
DOC = json.loads(TEXT)


def resolve(doc, ptr):
    if ptr == "":
        return doc
    cur = doc
    for part in ptr[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


# ---------------------------------------------------------------- 구획
def segment_of(ptr):
    m = re.match(r"^/recipes/(\d+)(/|$)", ptr)
    return f"S{int(m.group(1)) + 1}" if m else "S0"


for n in NODES:
    n["segment"] = segment_of(n["pointer"])

# ---------------------------------------------------------------- 형태소
EXCLUDE_RULES = [
    (re.compile(r"^/version$"), "버전 번호 문자열(언어 텍스트 아님)"),
    (re.compile(r"^/updated$"), "날짜 문자열 YYYY-MM-DD"),
    (re.compile(r"^/recipes/\d+/id$"), "레시피 ID 코드(R+숫자)"),
    (re.compile(r"^/recipes/\d+/goal$"), "영문 소문자·하이픈 코드값(goal). 원문 보존, 형태소 미적용"),
    (re.compile(r"^/recipes/\d+/procedures/\d+$"), "다른 원장 항목을 가리키는 M 코드 참조"),
]


def exclusion_reason(ptr):
    for rx, why in EXCLUDE_RULES:
        if rx.match(ptr):
            return why
    return None


def run_kiwi():
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi(num_workers=1, model_type="cong")
    return kiwi, kiwipiepy.__version__


KIWI, KIWI_VER = run_kiwi()
try:
    import importlib.metadata as md
    MODEL_VER = md.version("kiwipiepy_model")
except Exception:  # noqa
    MODEL_VER = "미확인"


def tokens_of(text, base):
    out = []
    for t in KIWI.tokenize(text):
        s, e = t.start, t.start + t.len
        out.append({"form": t.form, "tag": t.tag, "lemma": t.lemma, "start": s, "end": e,
                    "surface": text[s:e], "form_equals_surface": t.form == text[s:e],
                    "file_span": [base + s, base + e] if base is not None else None})
    return out


values_m, excluded = [], []
for n in NODES:
    if n["type"] != "string":
        continue
    why = exclusion_reason(n["pointer"])
    if why:
        excluded.append({"pointer": n["pointer"], "value": n["value"], "reason": why})
        continue
    vs = n["value_span"]
    values_m.append({"pointer": n["pointer"], "segment": n["segment"], "column": n["key"],
                     "text": n["value"], "file_span_of_text": vs,
                     "tokens": tokens_of(n["value"], vs[0] if vs else None)})


def camel_split(k):
    return re.findall(r"[a-z]+|[A-Z][a-z]*", k)


field_names = []
for k in sorted({kk["key"] for kk in P.keys}):
    occ = [kk["pointer"] for kk in P.keys if kk["key"] == k]
    field_names.append({"field": k, "occurrences": len(occ), "occurrence_pointers": occ,
                        "kiwi_tokens": tokens_of(k, None),
                        "rule_split_not_kiwi": camel_split(k)})

# 오분절 규칙의 출현별 기록
SEG = json.loads((OUT / "segmentation-review.json").read_text())
seg_flags = []
for rule in SEG["rules"]:
    hits = 0
    pat = [tuple(x) for x in rule["tokens"]]
    for v in values_m:
        if rule["pointers"] and v["pointer"] not in rule["pointers"]:
            continue
        toks = v["tokens"]
        for i in range(len(toks) - len(pat) + 1):
            if all((toks[i + j]["form"], toks[i + j]["tag"]) == pat[j] for j in range(len(pat))):
                s, e = toks[i]["start"], toks[i + len(pat) - 1]["end"]
                seg_flags.append({"rule": rule["id"], "pointer": v["pointer"], "token_indices": list(range(i, i + len(pat))),
                                  "span": [s, e], "surface": v["text"][s:e],
                                  "raw_tokens": [f"{a}/{b}" for a, b in pat],
                                  "correct_reading": rule["correct_reading"], "impact": rule["impact"]})
                hits += 1
    if hits != rule["expected_count"]:
        sys.exit(f"segmentation rule {rule['id']} hits {hits} != expected {rule['expected_count']}")
tag_incons = []
for form in SEG["tag_inconsistency"]["forms"]:
    tags = {}
    for v in values_m:
        for i, t in enumerate(v["tokens"]):
            if t["form"] == form:
                tags.setdefault(t["tag"], []).append({"pointer": v["pointer"], "span": [t["start"], t["end"]]})
    tag_incons.append({"form": form, "by_tag": tags})

morph = {
    "source": {"path": SRC_REL, "sha256": HASH_START},
    "analyzer": {"name": "Kiwi (kiwipiepy)", "kiwipiepy": KIWI_VER, "kiwipiepy_model": MODEL_VER,
                 "model_type": "cong", "num_workers": 1,
                 "tokenize_kwargs": "기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, blocklist=None, split_sents=False)",
                 "user_dictionary": "없음(기본 사전만)", "typos": None,
                 "tagset": "Kiwi 품사 체계(세종 기반 확장)",
                 "lemma": "Kiwi Token.lemma 그대로. 분석기가 준 값만 기록하며 도메인 표준명 아님",
                 "span": "각 값 문자열 기준 Unicode 코드 포인트 [start,end). file_span 은 원본 파일 텍스트 기준",
                 "correction": "출력을 교정하지 않았다. 알려진 오분절은 segmentation_flags 에 출현별로 둔다"},
    "excluded_values": excluded,
    "values": values_m,
    "field_names": field_names,
    "field_name_note": "필드명은 영문 camelCase 라 Kiwi 가 SL 한 토큰으로 낸다. rule_split_not_kiwi 는 대소문자 경계 규칙 분할이며 Kiwi 출력이 아니다.",
    "segmentation_flags": seg_flags,
    "tag_inconsistency": tag_incons,
}

# ---------------------------------------------------------------- 표현
exprs = []


def add_expr(ptr, s, e, text, cat, method, extra=None):
    v = BY_PTR[ptr]
    base = v["value_span"][0]
    rec = {"pointer": ptr, "segment": v["segment"], "column": v["key"], "span": [s, e],
           "file_span": [base + s, base + e], "text": text, "category": cat, "method": method}
    if extra:
        rec.update(extra)
    exprs.append(rec)


SENT_RX = re.compile(r"[^.]+\.?")
for v in values_m:
    ptr, t = v["pointer"], v["text"]
    add_expr(ptr, 0, len(t), t, "segment.value", "auto.whole_value")
    for m in SENT_RX.finditer(t):
        s, e = m.start(), m.end()
        while s < e and t[s] == " ":
            s += 1
        if s < e:
            add_expr(ptr, s, e, t[s:e], "segment.sentence", "regex.sentence('. ' 경계)")
            for cm in re.finditer(r"[^,→]+", t[s:e]):
                cs, ce = s + cm.start(), s + cm.end()
                while cs < ce and t[cs] == " ":
                    cs += 1
                while ce > cs and t[ce - 1] == " ":
                    ce -= 1
                if cs < ce and (cs, ce) != (s, e):
                    add_expr(ptr, cs, ce, t[cs:ce], "segment.clause", "regex.clause(',' '→' 경계)")
    REGEXES = [
        (r"\d+(?:~\d+)?\s?(?:개월마다|개월|주|회차|회|분|살|클|개)", "quantity_time", "regex.number_unit"),
        (r"\d+~\d+", "range", "regex.range"),
        (r"월 \d+회|\d+개월마다 \d+회|간격|반복", "periodic", "regex.periodic"),
        (r"\([^()]*\)", "parenthetical", "regex.paren"),
        (r"'[^']*'", "patient_quote", "regex.quote"),
        (r"[+/=→·:~]|\bor\b", "symbol", "regex.symbol"),
        (r"가능|검토|결정|필요시|부족하면|에 따라|후 ", "condition_or_possibility", "keyword.list"),
        (r"않|없|못|안 |불가", "negation", "keyword.negation"),
    ]
    for rx, cat, meth in REGEXES:
        for m in re.finditer(rx, t):
            add_expr(ptr, m.start(), m.end(), m.group(0), cat, meth)
    # 형태소 기반 수식·조건 후보 — 토큰이 든 어절 전체
    toks = v["tokens"]
    for i, tk in enumerate(toks):
        cat = None
        if tk["tag"] in ("MAG", "VA", "XR", "MM") or tk["tag"].startswith("VA") or tk["tag"].startswith("XSA"):
            cat = "modifier_candidate"
        elif (tk["tag"] == "NNB" and tk["form"] == "시") or (tk["tag"] == "EC" and tk["form"] == "면"):
            cat = "condition_candidate"
        if not cat:
            continue
        s, e = tk["start"], tk["end"]
        while s > 0 and t[s - 1] != " ":
            s -= 1
        while e < len(t) and t[e] != " ":
            e += 1
        add_expr(ptr, s, e, t[s:e], cat, f"morph.eojeol({tk['form']}/{tk['tag']})",
                 {"token_index": i, "token_span": [tk["start"], tk["end"]]})

MAN = json.loads((OUT / "manual-expressions.json").read_text())
for ptr, text, occ, cats, note in MAN["entries"]:
    v = BY_PTR[ptr]["value"]
    idx = -1
    for _ in range(occ + 1):
        idx = v.find(text, idx + 1)
        if idx < 0:
            sys.exit(f"manual expression not found: {ptr} {text!r} occ {occ}")
    for c in cats:
        if c not in MAN["categories"]:
            sys.exit(f"unknown category {c}")
    add_expr(ptr, idx, idx + len(text), text, "manual:" + "+".join(cats), "manual.direct_read",
             {"manual_categories": cats, "note": note, "occurrence": occ})

# 오탐 표시 — 출현 단위
FALSE_POS = [
    ("/recipes/5/name", "안 ", "keyword.negation", "「동안(童顔)」의 일부. 부정 아님"),
    ("/recipes/5/patientExplanation", "안 ", "keyword.negation", "「동안 얼굴」의 일부. 부정 아님"),
    ("/recipes/1/patientExplanation", "실로", "morph.eojeol(실로/MAG)", "K-1 오분절 유래. 실(시술)+로"),
    ("/recipes/5/patientExplanation", "이마·미간·눈가", "morph.eojeol(이/MM)", "K-3 오분절 유래. 「이마」"),
]
fp_hits = 0
for ptr, text, meth, why in FALSE_POS:
    m = [x for x in exprs if x["pointer"] == ptr and x["text"] == text and x["method"] == meth]
    if len(m) != 1:
        sys.exit(f"false-positive mark mismatch {ptr} {text} {meth}: {len(m)}")
    m[0]["review"] = {"false_positive": True, "reason": why}
    fp_hits += 1
# regex.number_unit 은 회차·개월마다를 회·개월보다 먼저 두어 부분일치를 피한다
for i, x in enumerate(exprs):
    x["id"] = f"E{i:04d}"

expressions = {
    "source": {"path": SRC_REL, "sha256": HASH_START},
    "note": "auto.* / regex.* / keyword.* / morph.* 는 기계 후보 추출이다. 전수 의미 해석이 아니다. manual.direct_read 는 직접 읽기 수집이다. 구간은 값 문자열 기준 코드 포인트 [start,end), file_span 은 파일 기준. 같은 구간이 여러 범주로 겹치는 것은 의도된 겹침이다.",
    "methods": {
        "auto.whole_value": "형태소 적용 값 전체",
        "regex.sentence('. ' 경계)": "[^.]+\\.? 로 문장 분할 후 앞 공백 제거",
        "regex.clause(',' '→' 경계)": "문장 안을 , 또는 → 로 나눈 구(문장과 같으면 생략)",
        "regex.number_unit": "숫자(+~숫자)+단위 낱말(개월마다·개월·주·회차·회·분·살·클·개)",
        "regex.range": "숫자~숫자",
        "regex.periodic": "월 N회 · N개월마다 N회 · 간격 · 반복",
        "regex.paren": "괄호 구",
        "regex.quote": "작은따옴표 구",
        "regex.symbol": "+ / = → · : ~ or",
        "keyword.list": "가능·검토·결정·필요시·부족하면·에 따라·후",
        "keyword.negation": "않·없·못·「안 」·불가 (부정 탐색용; 실제 부정 0, 오탐 2 표시)",
        "morph.eojeol(...)": "MAG·VA*·XR·MM·XSA* 토큰 또는 조건 표지(시/NNB·면/EC)가 든 어절",
        "manual.direct_read": "manual-expressions.json"
    },
    "expressions": exprs,
}

# ---------------------------------------------------------------- coverage
OBS = json.loads((OUT / "manual-observations.json").read_text())
segments = []
SEG_DEF = [("S0", "상위 메타데이터와 recipes 컨테이너", ["", "/version", "/updated", "/description", "/recipes"])]
for i in range(len(DOC["recipes"])):
    SEG_DEF.append((f"S{i + 1}", f"/recipes/{i} ({DOC['recipes'][i]['id']} {DOC['recipes'][i]['name']})", [f"/recipes/{i}"]))
for sid, label, roots in SEG_DEF:
    owned = [n["pointer"] for n in NODES if n["segment"] == sid]
    leaves = [n["pointer"] for n in NODES if n["segment"] == sid and n["leaf"]]
    o = OBS["segments"][sid]
    for ob in o["observations"]:
        for p in ob["pointers"]:
            if p not in BY_PTR:
                sys.exit(f"observation pointer invalid {p}")
    segments.append({
        "id": sid, "label": label, "root_pointers": roots,
        "pointer_range": [owned[0], owned[-1]],
        "owned_pointers": owned, "owned_leaf_pointers": leaves,
        "file_span": [BY_PTR[owned[0]]["span"][0] if sid != "S0" else 0,
                      BY_PTR[owned[-1]]["span"][1] if sid != "S0" else len(TEXT)],
        "context_refs": [] if sid == "S0" else ["/description", "/recipes"],
        "context_note": "S0 의 루트·/recipes 컨테이너는 S0 가 소유하고, S1~S7 은 /description 을 문맥으로 함께 읽었다(소유 아님)." if sid != "S0" else "S0 는 루트 객체·상위 스칼라·recipes 배열 컨테이너만 소유. 배열 원소는 S1~S7 소유.",
        "machine_extraction": "done",
        "direct_read": "done",
        "read_log": o["read_log"],
        "observation_ids": [ob["id"] for ob in o["observations"]],
        "review_file": "review.md", "review_anchor": f"#{sid.lower()}",
    })
coverage = {
    "source": {"path": SRC_REL, "sha256": HASH_START},
    "note": "machine_extraction=기계 열거·분석 완료, direct_read=에이전트가 그 구획 원문을 직접 읽음. 원장이 작아(6,486 bytes) 구획 8개를 한 세션에서 순차로 읽었다.",
    "last_read_position": "S7 끝(/recipes/6/followUp/3/action)",
    "remaining_segments": [],
    "segments": segments,
}

# ---------------------------------------------------------------- source-map
source_map = {
    "source": {"path": SRC_REL, "bytes": len(RAW), "code_points": len(TEXT), "sha256": HASH_START,
               "encoding": "UTF-8", "bom": RAW[:3] == b"\xef\xbb\xbf", "newlines": TEXT.count("\n"),
               "backslash_count": TEXT.count("\\"), "non_bmp_chars": sum(1 for c in TEXT if ord(c) > 0xFFFF)},
    "span_note": "span = 파일 텍스트의 코드 포인트 [start,end) (JSON 리터럴 전체, 문자열은 따옴표 포함). value_span = 디코딩 문자열이 놓인 코드 포인트 구간(이스케이프 없을 때만; 이 원장은 이스케이프 0). byte_span = UTF-8 바이트 [start,end).",
    "duplicate_keys": P.duplicates,
    "nodes": NODES,
    "key_occurrences": P.keys,
    "field_names": {k: [kk["pointer"] for kk in P.keys if kk["key"] == k] for k in sorted({kk["key"] for kk in P.keys})},
}

# ---------------------------------------------------------------- review.md
TYPE_KO = {"string": "문자열", "integer": "정수", "number": "실수", "boolean": "불리언", "null": "null",
           "object": "객체", "array": "배열"}


def cell(s):
    return str(s).replace("|", "\\|")


def fmt_val(n):
    if n["type"] == "string":
        return cell(n["value"])
    if n["type"] in ("object", "array"):
        return "(빈 " + TYPE_KO[n["type"]] + ")"
    return n["literal"]


patterns = {}
for n in NODES:
    patterns.setdefault(n["path_pattern"], []).append(n)

L = []
L.append("# combo-recipes.json — 1차 조사 (읽기용)\n")
L.append("> 원문 값과 잠정 관찰을 분리한다. 값 표의 「원문 값」 칸은 디코딩된 원문 그대로이고(표 안 `|` 만 `\\|` 로 이스케이프), 관찰은 각 구획의 「잠정 관찰」 절에 근거 Pointer 와 함께 둔다. 공통 개념 ID·동의어·관계 방향·정규화는 하지 않았다(1차 범위 밖). 원문의 효과·임상 서술은 **원장에 적혀 있다는 사실**로만 기록한다.\n")
L.append("## 상태\n")
L.append("| 항목 | 상태 |\n|---|---|")
L.append("| **1차 범위 종료** | 예 — 아래 기준 충족(validation.md) |")
L.append("| **원장 전체 완료** | **아님** — 원문 부족 B·잠정 P·후속 F·원문 불일치 I 가 남아 있다(issues.md) |")
L.append("| 전수 읽기 | 구획 8/8 직접 읽음 (coverage.json) |")
L.append(f"| 구조·값 수집 | 노드 {len(NODES)}개 · 키 출현 {len(P.keys)}개 · 말단 {sum(1 for n in NODES if n['leaf'])}개 (source-map.json) |")
L.append(f"| 형태소·표현 수집 | 적용 값 {len(values_m)} · 제외 {len(excluded)} · 토큰 {sum(len(v['tokens']) for v in values_m)} · 표현 {len(exprs)}(수동 {len(MAN['entries'])}) |")
L.append("| 기계 검증 | verify.py — validation.md |")
L.append("| 읽기 검토 | 같은 에이전트의 별도 관점 재독(독립 검토자 아님) — validation.md §3 |")
L.append(f"| 알려진 분석 오류 | 오분절 규칙 {len(SEG['rules'])}개 · 출현 {len(seg_flags)}건 (morphology.json segmentation_flags) |")
L.append("| 열린 미결 · 후속 의미 조사 | issues.md — 사용자 결정 필요(C) 0건(검토 후 판단 근거는 issues.md §0) |\n")
L.append("## 원본\n")
L.append("| 항목 | 값 |\n|---|---|")
L.append(f"| 경로 | `{SRC_REL}` |")
sm = source_map["source"]
L.append(f"| 크기 | {sm['bytes']:,} bytes · {sm['code_points']:,} code points · UTF-8 · BOM {'있음' if sm['bom'] else '없음'} · 개행 {sm['newlines']} · 백슬래시(이스케이프) {sm['backslash_count']} · BMP 밖 문자 {sm['non_bmp_chars']} |")
L.append(f"| sha256 | `{HASH_START}` |")
L.append(f"| 중복 키 | {len(P.duplicates)}건 |\n")
L.append("구간 기준: source-map 의 `span` 은 파일 텍스트 코드 포인트 `[start,end)`, morphology·expressions 의 `span` 은 값 문자열 기준(파일 기준은 `file_span`). 바이트는 `byte_span`.\n")
L.append("## 컬럼 구성\n")
L.append("| 원본 컬럼명(경로 패턴) | 자료형 | 중첩 구조 | 출현 | 원문 예시 | 예시 위치 | 빈 값 |\n|---|---|---|---|---|---|---|")
for pat, ns in patterns.items():
    types = sorted({TYPE_KO[n["type"]] for n in ns})
    n0 = ns[0]
    if n0["type"] == "object":
        nest = "객체 {" + ", ".join(n0["keys"]) + "}"
    elif n0["type"] == "array":
        lens = sorted({n["child_count"] for n in ns})
        nest = "배열 길이 " + "/".join(map(str, lens))
    else:
        nest = "스칼라"
    empties = sum(1 for n in ns if (n["type"] == "string" and n["value"] == "") or n["type"] == "null"
                  or (n["type"] in ("object", "array") and n["child_count"] == 0))
    ex = fmt_val(n0) if n0["type"] not in ("object", "array") or n0["child_count"] == 0 else "—"
    if len(ex) > 60:
        ex = ex[:60] + "…(전체는 구획 표)"
    L.append(f"| `{pat}` | {'/'.join(types)} | {nest} | {len(ns)} | {ex} | `{n0['pointer'] or '(root)'}` | {empties} |")
L.append("\n- 선택적 필드: 없음 — recipes 7개 모두 11키 전부, followUp 원소 28개 모두 week·action 두 키.")
L.append("- 빈 문자열·빈 배열·빈 객체·null: 0.\n")
L.append("## 구획 목차\n")
L.append("| 구획 | 범위 | 소유 말단 | 직접 읽음 |\n|---|---|---|---|")
for sg in segments:
    L.append(f"| [{sg['id']}](#{sg['id'].lower()}) | {sg['label']} | {len(sg['owned_leaf_pointers'])} | {sg['direct_read']} |")
L.append("")
for sg in segments:
    sid = sg["id"]
    L.append(f"<a id=\"{sid.lower()}\"></a>\n## {sid} — {sg['label']}\n")
    L.append(f"읽기 기록: {sg['read_log']}\n")
    L.append("### 원문 값\n")
    L.append("| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |\n|---|---|---|---|")
    for p in sg["owned_pointers"]:
        n = BY_PTR[p]
        if n["key"] is not None:
            col = n["key"]
        elif n["index"] is not None:
            col = f"{BY_PTR[n['parent']]['key']}[{n['index']}]"
        else:
            col = "(root)"
        if n["leaf"]:
            L.append(f"| `{p}` | {col} | {TYPE_KO[n['type']]} | {fmt_val(n)} |")
        else:
            desc = ("키 " + ", ".join(n["keys"])) if n["type"] == "object" else f"원소 {n['child_count']}개"
            L.append(f"| `{p or '(root)'}` | {col} | {TYPE_KO[n['type']]} | ({desc}) |")
    L.append("\n### 잠정 관찰 (원문 아님)\n")
    L.append("| ID | 상태 | 근거 Pointer | 관찰 |\n|---|---|---|---|")
    for ob in OBS["segments"][sid]["observations"]:
        L.append(f"| {ob['id']} | {ob['status']} | {' '.join('`'+x+'`' for x in ob['pointers'])} | {cell(ob['text'])} |")
    flags = [f for f in seg_flags if segment_of(f["pointer"]) == sid]
    if flags:
        L.append("\n### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)\n")
        L.append("| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |\n|---|---|---|---|---|---|")
        for f in flags:
            L.append(f"| {f['rule']} | `{f['pointer']}` | {f['span']} | {cell(f['surface'])} | {' '.join(f['raw_tokens'])} | {cell(f['impact'])} |")
    nman = sum(1 for e in exprs if e["segment"] == sid and e["method"] == "manual.direct_read")
    L.append(f"\n수동 표현 {nman}건 · 전체 표현 {sum(1 for e in exprs if e['segment'] == sid)}건 → expressions.json (segment=\"{sid}\")\n")
L.append("## 기록 위치\n")
for f in ["source-map.json", "morphology.json", "expressions.json", "coverage.json", "issues.md", "validation.md",
          "build.py", "verify.py", "manual-expressions.json", "manual-observations.json", "segmentation-review.json"]:
    L.append(f"- [{f}](./{f})")
review = "\n".join(L) + "\n"

# ---------------------------------------------------------------- 쓰기
def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


dump("source-map.json", source_map)
dump("morphology.json", morph)
dump("expressions.json", expressions)
dump("coverage.json", coverage)
(OUT / "review.md").write_text(review)

HASH_END = sha256(SRC)
log(f"source sha256 start={HASH_START} end={HASH_END} same={HASH_START == HASH_END}")
log(f"nodes={len(NODES)} keys={len(P.keys)} leaves={sum(1 for n in NODES if n['leaf'])} duplicates={len(P.duplicates)}")
log(f"strings={sum(1 for n in NODES if n['type']=='string')} applied={len(values_m)} excluded={len(excluded)} tokens={sum(len(v['tokens']) for v in values_m)}")
log(f"kiwipiepy={KIWI_VER} model={MODEL_VER} model_type=cong num_workers=1")
log(f"seg_rules={len(SEG['rules'])} seg_flags={len(seg_flags)} expressions={len(exprs)} manual={len(MAN['entries'])} false_positive_marked={fp_hits}")
(OUT / "build-output.txt").write_text("\n".join(LOG) + "\n")
if HASH_START != HASH_END:
    sys.exit("source changed during build")
