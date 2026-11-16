"""products.json 1차 수집 — 구조·값·형태소·복합 표현.

실행(레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/products/build.py

입력(읽기 전용): 원장 products.json, 같은 폴더의 수동 검토 기록
  manual-expressions.json · segmentation-review.json · observations.json
출력(같은 폴더): source-map.json · morphology.json · expressions.json · review.md · build-output.txt
원본은 읽기만 한다. 모든 문자 구간은 디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end).
"""
import hashlib, json, os, re, sys
from collections import OrderedDict

ROOT = os.getcwd()
SRC = "orchestration/work/phub-recommend/bronze/phub-ledger/products.json"
OUT = os.path.dirname(os.path.abspath(__file__))
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s)


def sha(b):
    return hashlib.sha256(b).hexdigest()


raw = open(os.path.join(ROOT, SRC), "rb").read()
H0 = sha(raw)
text = raw.decode("utf-8")
assert not text.startswith("﻿")
# 코드 포인트 → 바이트 오프셋
BOFF = [0]
for ch in text:
    BOFF.append(BOFF[-1] + len(ch.encode("utf-8")))


def bspan(s, e):
    return [BOFF[s], BOFF[e]]


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 1. 자체 파서
NODES, KEYS, DUPS = [], [], []
WS = " \t\r\n"


class P:
    def __init__(s, t):
        s.t, s.i = t, 0

    def ws(s):
        while s.i < len(s.t) and s.t[s.i] in WS:
            s.i += 1

    def string(s):
        """반환: (디코딩 값, 리터럴 시작, 리터럴 끝, 디코딩 문자 → 원문 코드포인트 위치 목록, 이스케이프 유무)"""
        st = s.i
        assert s.t[s.i] == '"'
        s.i += 1
        out, pos, has_esc = [], [], False
        while True:
            c = s.t[s.i]
            if c == '"':
                s.i += 1
                return "".join(out), st, s.i, pos, has_esc
            if c == "\\":
                has_esc = True
                n = s.t[s.i + 1]
                if n == "u":
                    out.append(chr(int(s.t[s.i + 2:s.i + 6], 16)))
                    pos.append(s.i)
                    s.i += 6
                else:
                    out.append({'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}[n])
                    pos.append(s.i)
                    s.i += 2
            else:
                out.append(c)
                pos.append(s.i)
                s.i += 1

    def value(s, ptr, parent, key, idx):
        s.ws()
        c = s.t[s.i]
        node = OrderedDict(pointer=ptr, parent=parent, key=key, index=idx, depth=ptr.count("/"))
        NODES.append(node)
        st = s.i
        if c == "{":
            node["type"] = "object"
            s.i += 1
            seen, order = {}, []
            s.ws()
            if s.t[s.i] == "}":
                s.i += 1
            else:
                while True:
                    s.ws()
                    k, ks, ke, _, kesc = s.string()
                    s.ws()
                    assert s.t[s.i] == ":"
                    s.i += 1
                    cptr = ptr + "/" + esc(k)
                    if k in seen:
                        DUPS.append({"object_pointer": ptr, "key": k, "first_key_span": seen[k], "dup_key_span": [ks, ke]})
                    seen[k] = [ks, ke]
                    order.append(k)
                    KEYS.append(OrderedDict(key=k, object_pointer=ptr, value_pointer=cptr, member_index=len(order) - 1,
                                            span=[ks, ke], byte_span=bspan(ks, ke), has_escape=kesc))
                    s.value(cptr, ptr, k, None)
                    s.ws()
                    if s.t[s.i] == ",":
                        s.i += 1
                        continue
                    assert s.t[s.i] == "}"
                    s.i += 1
                    break
            node["member_keys"] = order
            node["length"] = len(order)
        elif c == "[":
            node["type"] = "array"
            s.i += 1
            n = 0
            s.ws()
            if s.t[s.i] == "]":
                s.i += 1
            else:
                while True:
                    s.value(f"{ptr}/{n}", ptr, None, n)
                    n += 1
                    s.ws()
                    if s.t[s.i] == ",":
                        s.i += 1
                        continue
                    assert s.t[s.i] == "]"
                    s.i += 1
                    break
            node["length"] = n
        elif c == '"':
            v, a, b, pos, e = s.string()
            node["type"] = "string"
            node["value"] = v
            node["value_span"] = [a + 1, b - 1]
            node["has_escape"] = e
            node["decoded_to_source_cp"] = None if not e else pos
        else:
            m = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(s.t, s.i)
            lit = m.group(0)
            s.i = m.end()
            if lit in ("true", "false"):
                node["type"], node["value"] = "boolean", lit == "true"
            elif lit == "null":
                node["type"], node["value"] = "null", None
            else:
                node["type"], node["value"] = "number", json.loads(lit)
        node["span"] = [st, s.i]
        node["byte_span"] = bspan(st, s.i)
        node["literal"] = s.t[st:s.i] if node["type"] not in ("object", "array") else None
        if node["type"] in ("object", "array", "string"):
            node["empty"] = (node.get("length") == 0) if node["type"] != "string" else (node["value"] == "")
        return node


p = P(text)
p.value("", None, None, None)
p.ws()
assert p.i == len(text), "trailing data"

# json.loads 와 대조(중복 키 감지는 object_pairs_hook)
hook_dups = []


def hook(pairs):
    ks = [k for k, _ in pairs]
    if len(ks) != len(set(ks)):
        hook_dups.append(ks)
    return dict(pairs)


data = json.loads(text, object_pairs_hook=hook)
BYP = {n["pointer"]: n for n in NODES}


def resolve(ptr):
    cur = data
    for part in ptr.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


# ---------------------------------------------------------------- 2. 문맥
def pattern(ptr):
    return re.sub(r"/\d+(?=/|$)", "/*", ptr)


for n in NODES:
    parts = n["pointer"].split("/")[1:]
    ctx = OrderedDict()
    if parts:
        ctx["section"] = parts[0]
        sec = data.get(parts[0])
        if isinstance(sec, dict) and "category_id" in sec:
            ctx["section_category_id_pointer"] = f"/{parts[0]}/category_id"
    if len(parts) >= 3 and parts[1] == "products":
        ip = f"/{parts[0]}/products/{parts[2]}"
        item = resolve(ip)
        ctx["item_pointer"] = ip
        ctx["item_index"] = int(parts[2])
        ctx["item_name"] = item.get("name")
        ctx["item_name_pointer"] = ip + "/name" if "name" in item else None
        ctx["sibling_field_pointers"] = [ip + "/" + esc(k) for k in item]
    n["pattern"] = pattern(n["pointer"])
    # 컬럼 패턴: 깊이 2 이상이면 최상위 섹션 키도 * 로 (섹션 공통 컬럼 비교용)
    n["column_pattern"] = re.sub(r"^/[^/]+", "/*", n["pattern"]) if n["depth"] >= 2 else n["pattern"]
    n["context"] = ctx

# 필드명 출현 위치
FIELD_OCC = OrderedDict()
for k in KEYS:
    FIELD_OCC.setdefault(k["key"], OrderedDict()).setdefault(pattern(k["value_pointer"]), []).append(k["value_pointer"])

# ---------------------------------------------------------------- 3. 형태소 분석 적용/제외
EXCLUDE_RULES = [
    # (규칙 id, 판정 함수, 사유)
    ("X-version", lambda n: n["pointer"] == "/version", "버전 식별 코드 '1.2'. 언어 텍스트가 아님. 값은 source-map 에 보존"),
    ("X-date", lambda n: n["pointer"] == "/updated", "ISO 날짜 YYYY-MM-DD 리터럴. 형태소 대상 아님. 시간 표현으로 expressions 에 보존"),
    ("X-category-code", lambda n: re.fullmatch(r"/[^/]+/category_id(/\d+)?", n["pointer"]) is not None,
     "분류 코드(M+숫자). 원장 내부 ID. 다른 원장(taxonomy 등) 참조 여부는 후속 연결 과제"),
    ("X-country-code", lambda n: re.fullmatch(r"/[^/]+/products/\d+/country", n["pointer"]) is not None and re.fullmatch(r"[A-Z]{2}", n["value"]) is not None,
     "국가 코드(대문자 2자). 코드값"),
    ("X-placeholder", lambda n: n["value"] == "-", "자리표시 '-' 한 글자. 언어 텍스트 아님. 값의 뜻(미상/해당 없음)은 원문에 없어 issues 에 기록"),
]
FIELDNAME_EXCLUDE = "필드명은 ASCII snake_case/영문 식별자(예: name_en, legal_warning). 언어 텍스트 값과 역할이 달라 형태소 분석에서 제외. 모든 출현 위치는 source-map.keys·field_name_occurrences 에 보존"

from kiwipiepy import Kiwi
import kiwipiepy

kiwi = Kiwi(model_type="cong", num_workers=1)
TOK_OPTS = {}  # tokenize 기본값 그대로 사용

applied, excluded = [], []
for n in NODES:
    if n["type"] != "string":
        continue
    rule = next((r for r in EXCLUDE_RULES if r[1](n)), None)
    if rule:
        excluded.append(OrderedDict(pointer=n["pointer"], value=n["value"], rule=rule[0], reason=rule[2]))
        continue
    v = n["value"]
    toks = kiwi.tokenize(v, **TOK_OPTS)
    base = n["value_span"][0]
    tl = []
    for i, t in enumerate(toks):
        s, e = t.start, t.start + t.len
        # 이스케이프가 없으므로 디코딩 인덱스 + value_span 시작 = 파일 코드 포인트 (검증에서 재확인)
        tl.append(OrderedDict(i=i, form=t.form, tag=t.tag, lemma=t.lemma, span=[s, e], surface=v[s:e],
                              file_span=[base + s, base + e], byte_span=bspan(base + s, base + e),
                              word_position=t.word_position, sent_position=t.sent_position, raw_form=t.raw_form,
                              typo_cost=t.typo_cost, score=round(float(t.score), 6)))
    applied.append(OrderedDict(pointer=n["pointer"], field=n["key"], pattern=n["pattern"], text=v,
                               file_span_of_text=n["value_span"], context=n["context"], tokens=tl))

key_excl = [OrderedDict(key=k["key"], value_pointer=k["value_pointer"], span=k["span"], reason="FIELDNAME") for k in KEYS]

# 오분절·오태깅 수동 검토 기록 대응
segrev = json.load(open(os.path.join(OUT, "segmentation-review.json")))
TOKSET = {(r["pointer"], t["span"][0], t["span"][1], t["form"], t["tag"]) for r in applied for t in r["tokens"]}
seg_missing = []
for o in segrev["occurrences"]:
    for f, tg, sp in o["tokens"]:
        if (o["pointer"], sp[0], sp[1], f, tg) not in TOKSET:
            seg_missing.append((o["id"], f, tg, sp))

# ---------------------------------------------------------------- 4. 복합 표현
EXPR = []


def add_expr(ptr, s, e, cat, method, note=None, **kw):
    v = BYP[ptr]["value"]
    base = BYP[ptr]["value_span"][0]
    d = OrderedDict(id=None, pointer=ptr, field=BYP[ptr]["key"], span=[s, e], text=v[s:e], file_span=[base + s, base + e],
                    byte_span=bspan(base + s, base + e), category_candidate=cat, method=method,
                    value_text=v, item_pointer=BYP[ptr]["context"].get("item_pointer"),
                    item_name=BYP[ptr]["context"].get("item_name"))
    if note:
        d["note"] = note
    d.update(kw)
    EXPR.append(d)


STR_NODES = [n for n in NODES if n["type"] == "string"]
# (a) 값 전체 구획: 모든 문자열 값(제외 값 포함) — 값 단위 문맥 단위
for n in STR_NODES:
    add_expr(n["pointer"], 0, len(n["value"]), "segment.value", "auto:whole-value")
# (b) 문장 구획: Kiwi split_into_sents (2문장 이상인 값만 기록)
for r in applied:
    sents = kiwi.split_into_sents(r["text"])
    if len(sents) > 1:
        for s in sents:
            add_expr(r["pointer"], s.start, s.end, "segment.sentence", "auto:kiwi.split_into_sents")
# (c) 정규식 후보 — 수집 보조. 의미 분류 아님
REGEX = [
    ("operator.plus", r"[^\s+]+(?:\+[^\s+]*)+", "'+' 연결 문자열(앞뒤 피연산자 포함, 공백 기준)"),
    ("operator.slash", r"[^\s/]+(?:/[^\s/]+)+", "'/' 연결 문자열(공백 기준)"),
    ("operator.middot", r"[^\s·]+(?:·[^\s·]+)+", "'·' 연결 문자열"),
    ("paren.group", r"[^\s(]*\([^()]*\)", "괄호 보충(앞 붙은 말 포함)"),
    ("quote.single", r"'[^']*'", "작은따옴표 인용"),
    ("dash.em", r"\s—\s", "줄표 '—' 구분"),
    ("number.or.year", r"\d+(?:\.\d+)?", "숫자"),
    ("latin.run", r"[A-Za-z][A-Za-z0-9:.\-]*(?:\s[A-Za-z0-9][A-Za-z0-9:.\-]*)*", "로마자 연속(공백 포함)"),
    ("neg.prohib.cand", r"없음|금지|아닌|아님|만\s|만으로|예정|소지|위반|반복|등\)", "부정·금지·한정·예정·가능성 단서 문자열(키워드)"),
]
for n in STR_NODES:
    if n["value"] == "-" or n["pointer"] == "/version" or re.fullmatch(r"/[^/]+/category_id(/\d+)?", n["pointer"]):
        continue
    for cat, rx, desc in REGEX:
        for m in re.finditer(rx, n["value"]):
            add_expr(n["pointer"], m.start(), m.end(), "regex." + cat, "regex:" + rx, note=desc)
# (d) 수동 표현 — 원문을 직접 읽고 기록
man = json.load(open(os.path.join(OUT, "manual-expressions.json")))
man_missing = []
for m in man["expressions"]:
    v = BYP[m["pointer"]]["value"]
    occ = m.get("occurrence", 0)
    idx, start = -1, 0
    for _ in range(occ + 1):
        idx = v.find(m["text"], start)
        if idx < 0:
            break
        start = idx + 1
    if idx < 0:
        man_missing.append(m)
        continue
    add_expr(m["pointer"], idx, idx + len(m["text"]), "manual." + m["viewpoint"], "manual:read",
             note=m.get("note"), manual_id=m["mid"], occurrence=occ)
for i, x in enumerate(EXPR):
    x["id"] = f"E{i:04d}"

# ---------------------------------------------------------------- 5. 자체 검증(빌드 시점)
fails = []


def chk(c, m):
    if not c:
        fails.append(m)


chk(not DUPS and not hook_dups, "duplicate keys")
for n in NODES:
    v = resolve(n["pointer"])
    chk(json.loads(text[n["span"][0]:n["span"][1]]) == v, "span " + n["pointer"])
    if n["type"] == "string":
        chk(text[n["value_span"][0]:n["value_span"][1]] == n["value"] or n["has_escape"], "vspan " + n["pointer"])
allp = []


def walk(v, ptr):
    allp.append(ptr)
    if isinstance(v, dict):
        for k, c in v.items():
            walk(c, ptr + "/" + esc(k))
    elif isinstance(v, list):
        for i, c in enumerate(v):
            walk(c, f"{ptr}/{i}")


walk(data, "")
chk(sorted(allp) == sorted(BYP) and len(allp) == len(NODES), "bidirectional")
chk(not man_missing, "manual missing %r" % man_missing)
chk(not seg_missing, "segrev missing %r" % seg_missing)
for r in applied:
    for t in r["tokens"]:
        chk(text[t["file_span"][0]:t["file_span"][1]] == t["surface"], "tok " + r["pointer"])
H1 = sha(open(os.path.join(ROOT, SRC), "rb").read())
chk(H0 == H1, "hash changed")

# ---------------------------------------------------------------- 6. 출력
SOURCE = OrderedDict(path=SRC, size_bytes=len(raw), code_points=len(text), sha256_start=H0, sha256_end=H1,
                     encoding="utf-8, BOM 없음, 개행 없음(한 줄)",
                     offset_unit="span·value_span·file_span: 디코딩된 파일 전체 텍스트의 Unicode 코드 포인트 [start,end). "
                                 "byte_span: UTF-8 바이트 [start,end). 토큰·표현의 span 은 해당 값(디코딩 문자열) 기준 코드 포인트 [start,end)")


def dump(name, obj):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


dump("source-map.json", OrderedDict(
    source=SOURCE,
    notes=["노드 span 은 리터럴 전체(문자열은 따옴표 포함), value_span 은 따옴표 제외 원문 구간.",
           "이스케이프 0건: 모든 문자열의 value_span slice == 디코딩 값. decoded_to_source_cp 는 이스케이프가 있을 때만 채운다(이번 null).",
           "literal 은 스칼라 노드의 JSON 리터럴 원문(문자열은 따옴표 포함). object/array 는 null.",
           "context: section(최상위 키)·item_pointer(products 배열 항목)·sibling_field_pointers(같은 항목의 형제 필드, 원본 순서).",
           "구조적 사실(키·순서·계층)을 기록할 뿐 의미적 정합을 승인하지 않는다."],
    duplicate_keys=DUPS,
    counts=OrderedDict(nodes=len(NODES), keys=len(KEYS),
                       by_type={t: sum(1 for n in NODES if n["type"] == t) for t in ["object", "array", "string", "number", "boolean", "null"]},
                       empty_nodes=[n["pointer"] for n in NODES if n.get("empty")]),
    field_name_occurrences=FIELD_OCC,
    keys=KEYS,
    nodes=NODES))

dump("morphology.json", OrderedDict(
    source=OrderedDict(path=SRC, sha256_start=H0),
    analyzer=OrderedDict(name="Kiwi (kiwipiepy)", kiwipiepy_version=kiwipiepy.__version__,
                         model_type=kiwi.model_type, num_workers=kiwi.num_workers, user_dictionary=None,
                         added_user_words=0, tokenize_options="기본값(추가 인자 없음: normalize_coda=False, split_complex=False, "
                                                              "blocklist=None, match_options=Match.ALL 기본)",
                         typo_correction="미사용(Kiwi 생성 시 typos 미지정)",
                         space_tolerance=kiwi.space_tolerance, space_penalty=kiwi.space_penalty,
                         cutoff_threshold=kiwi.global_config.cutoff_threshold, integrate_allomorph=kiwi.integrate_allomorph,
                         max_unk_form_size=kiwi.max_unk_form_size,
                         tagset="Kiwi 품사 체계(세종 기반 + SL/SH/SN/SW/W_* 등)",
                         lemma_source="Token.lemma (kiwipiepy 제공값을 그대로 기록. 작업자가 생성하지 않음)",
                         span_basis="Token.start/len = 입력 문자열(디코딩 값) 코드 포인트. 정규화 없이 원문 값을 그대로 입력"),
    field_names=OrderedDict(policy=FIELDNAME_EXCLUDE, unique_field_names=list(FIELD_OCC), occurrences=key_excl),
    excluded_rules=[OrderedDict(rule=r[0], reason=r[2]) for r in EXCLUDE_RULES],
    excluded_values=excluded,
    values=applied,
    segmentation_review=segrev))

dump("expressions.json", OrderedDict(
    source=OrderedDict(path=SRC, sha256_start=H0),
    method_notes=["segment.value: 모든 문자열 값 전체(값 단위 문맥).",
                  "segment.sentence: Kiwi split_into_sents 가 2문장 이상으로 나눈 값의 문장 구간.",
                  "regex.*: 정규식 후보. 수집 보조이며 의미 분류·전수 의미 해석이 아니다. 오탐 가능.",
                  "manual.*: 원문을 직접 읽고 기록한 구절. viewpoint 는 탐색 관점이지 확정 분류가 아니다.",
                  "같은 구간이 여러 관점·방법으로 겹치는 것은 의도된 겹침이다. 같은 (pointer, span, category, method) 반복은 없어야 한다."],
    regex_rules=[OrderedDict(category="regex." + c, pattern=r, desc=d) for c, r, d in REGEX],
    manual_viewpoints=man["viewpoints"],
    expressions=EXPR))

# ---------------------------------------------------------------- review.md
obs = json.load(open(os.path.join(OUT, "observations.json")))


def lit(n):
    if n["literal"] is not None:
        return n["literal"]
    if n["type"] == "array":
        el = [BYP[f'{n["pointer"]}/{i}'] for i in range(n["length"])]
        if all(e["literal"] is not None for e in el):
            return "[" + ", ".join(e["literal"] for e in el) + "]"
        return f"[object × {len(el)}]"
    return "{" + ", ".join(n["member_keys"]) + "}"


def md(s):
    return str(s).replace("|", "\\|")


L = []
A = L.append
A("# products.json — 1차 조사 (읽기용)\n")
A("> 이 문서는 생성물이다(build.py). 원문 값 칸과 잠정 관찰 칸을 분리했다. 잠정 관찰은 확정 데이터가 아니다.\n")
A("## 0. 원본과 상태\n")
A(f"- 원본: `{SRC}`")
A(f"- 크기 {len(raw)} 바이트 · {len(text)} 코드 포인트 · UTF-8 · BOM 없음 · 한 줄 · 이스케이프 0")
A(f"- sha256 (빌드 시작/끝 동일): `{H0}`")
A(f"- 노드 {len(NODES)} · 키 {len(KEYS)} · 중복 키 {len(DUPS)} · 빈 값 {sum(1 for n in NODES if n.get('empty'))}")
A(f"- 형태소: 적용 {len(applied)}값 / {sum(len(r['tokens']) for r in applied)}토큰 · 제외 {len(excluded)}값 · 필드명 {len(KEYS)}출현 제외")
A(f"- 표현 후보: {len(EXPR)}건 (값 구획 {sum(1 for x in EXPR if x['category_candidate']=='segment.value')} · "
  f"문장 {sum(1 for x in EXPR if x['category_candidate']=='segment.sentence')} · "
  f"정규식 {sum(1 for x in EXPR if x['method'].startswith('regex'))} · 수동 {sum(1 for x in EXPR if x['method']=='manual:read')})")
A("- 상태 보고는 `validation.md` 맨 위, 미결은 `issues.md`.\n")

A("## 1. 최상위 구성\n")
A("| 원본 키 | 자료형 | 원문 값 / 구성 | Pointer |")
A("|---|---|---|---|")
for k in BYP[""]["member_keys"]:
    n = BYP["/" + esc(k)]
    if n["type"] == "object":
        desc = "object { " + ", ".join(n["member_keys"]) + " }; products " + str(BYP[n["pointer"] + "/products"]["length"]) + "개"
    else:
        desc = lit(n)
    A(f"| `{k}` | {n['type']} | {md(desc)} | `{n['pointer']}` |")
A("")

A("## 2. 컬럼 구성 표\n")
A("깊이 2 이상 경로의 첫 `*` 는 최상위 섹션 키(8개), 그 뒤 `*` 는 배열 인덱스. 출현 수는 실제 노드 수. 예시는 첫 출현. 변형·선택 필드·자리표시를 따로 행으로 둔다.\n")
A("| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 | 원문 예시 | 예시 위치 | 변형·선택 여부 |")
A("|---|---|---|---|---|---|")
pats = OrderedDict()
for n in NODES:
    if n["pointer"] == "":
        continue
    pats.setdefault((n["column_pattern"], n["type"]), []).append(n)
items_total = sum(BYP[f"/{esc(k)}/products"]["length"] for k in BYP[""]["member_keys"] if BYP["/" + esc(k)]["type"] == "object")
for (pt, ty), ns in pats.items():
    nest = {"object": "object", "array": "array", "string": "string", "number": "number", "boolean": "boolean", "null": "null"}[ty]
    if pt.startswith("/*/products/*/"):
        nest += " · products 배열 항목 object 안"
    elif pt.endswith("/products"):
        nest += " of object"
    elif pt == "/*/category_id/*":
        nest += " · category_id 배열 원소"
    ex = ns[0]
    var = ""
    if pt.startswith("/*/products/*/"):
        secs = OrderedDict()
        for n in ns:
            secs[n["context"]["section"]] = secs.get(n["context"]["section"], 0) + 1
        var = f"항목 {len(ns)}/{items_total}; " + ", ".join(f"{s} {c}" for s, c in secs.items())
        if len(ns) < items_total:
            var = "선택 필드 — " + var
    if pt == "/*/category_id":
        var = ("string: " if ty == "string" else "array: ") + ", ".join(n["context"]["section"] for n in ns)
    exl = lit(ex)
    A(f"| `{pt}` | {nest} | {len(ns)} | {md(exl)} | `{ex['pointer']}` | {md(var)} |")
# 자리표시 '-' 와 boolean 값 분포 별도 행
for pt in ["/*/products/*/manufacturer", "/*/products/*/country"]:
    ns = [n for n in NODES if n["column_pattern"] == pt and n.get("value") == "-"]
    if ns:
        A(f"| `{pt}` = `\"-\"` | string 자리표시 | {len(ns)} | \"-\" | " + ", ".join(f"`{n['pointer']}`" for n in ns) + " | 값 변형(자리표시) |")
for val in (True, False):
    ns = [n for n in NODES if n["column_pattern"] == "/*/products/*/mfds" and n["value"] is val]
    A(f"| `/*/products/*/mfds` = `{str(val).lower()}` | boolean | {len(ns)} | {str(val).lower()} | `{ns[0]['pointer']}` 외 | 값 분포 |")
mf_abs = [f"/{esc(k)}/products/{i}" for k in BYP[""]["member_keys"] if BYP["/" + esc(k)]["type"] == "object"
          for i in range(BYP[f"/{esc(k)}/products"]["length"]) if f"/{esc(k)}/products/{i}/mfds" not in BYP]
A(f"| `/*/products/*/mfds` 키 없음 | — | {len(mf_abs)} | (키 없음) | `{mf_abs[0]}` … `{mf_abs[-1]}` | 선택 필드 부재 |")
ksv = OrderedDict()
for n in NODES:
    if n["column_pattern"] == "/*/products/*":
        ksv.setdefault(tuple(n["member_keys"]), []).append(n["pointer"])
for ks, ps in ksv.items():
    A(f"| `/*/products/*` 키 구성 {{{', '.join(ks)}}} | object 변형 | {len(ps)} | (키 순서 그대로) | " + ", ".join(f"`{p_}`" for p_ in ps[:3]) + (f" 외 {len(ps)-3}" if len(ps) > 3 else "") + " | 항목 키 구성 변형 |")
A(f"| 빈 문자열·빈 배열·빈 객체·null | — | {sum(1 for n in NODES if n.get('empty') or n['type']=='null')} | (없음) | — | 원본에 0건 |")
A("")

A("## 3. 항목별 값 (원본 컬럼명 그대로, 원본 순서)\n")
A("원문 값 칸은 JSON 리터럴 그대로다(문자열은 따옴표 포함). 관찰은 §4 에만 적는다.\n")
for k in BYP[""]["member_keys"]:
    sec = BYP["/" + esc(k)]
    if sec["type"] != "object":
        continue
    cid = BYP[f"/{esc(k)}/category_id"]
    A(f"### `{k}` — category_id {md(lit(cid))} (`{cid['pointer']}`) · products {BYP[f'/{esc(k)}/products']['length']}개\n")
    A("| 항목 | 원본 컬럼명 | 원문 값 | Pointer |")
    A("|---|---|---|---|")
    A(f"| (묶음) | `category_id` | {md(lit(cid))} | `{cid['pointer']}` |")
    if cid["type"] == "array":
        for i in range(cid["length"]):
            e_ = BYP[f"{cid['pointer']}/{i}"]
            A(f"| (묶음) | `category_id` [{i}] | {md(lit(e_))} | `{e_['pointer']}` |")
    for i in range(BYP[f"/{esc(k)}/products"]["length"]):
        it = BYP[f"/{esc(k)}/products/{i}"]
        for j, kk in enumerate(it["member_keys"]):
            n = BYP[it["pointer"] + "/" + esc(kk)]
            A(f"| {'**' + str(i) + '**' if j == 0 else ''} | `{kk}` | {md(lit(n))} | `{n['pointer']}` |")
    A("")

A("## 4. 잠정 관찰 (원문 값과 분리)\n")
A("상태: `잠정`=근거 있는 관찰이나 확정 아님 · `후속`=후속 의미 조사/연결 과제 · `원문부족`=원문에 정보가 없음. 자세한 처리는 issues.md.\n")
A("| id | 관찰 | 근거 Pointer | 상태 | issues |")
A("|---|---|---|---|---|")
for o in obs["observations"]:
    for p_ in o["pointers"]:
        chk(p_ in BYP, "obs pointer " + p_)
    A(f"| {o['id']} | {md(o['text'])} | " + "<br>".join(f"`{p_}`" for p_ in o["pointers"]) + f" | {o['status']} | {o.get('issue','')} |")
A("")
A("## 5. 구조화 기록으로 가는 길\n")
A("- 노드·키·구간·문맥: `source-map.json` (`nodes[].pointer` 로 찾기)")
A("- 형태소: `morphology.json` `values[]`(적용) · `excluded_values[]`(제외 사유) · `field_names`(필드명 제외) · `segmentation_review`(알려진 오분절·오태깅, 출현별)")
A("- 복합 표현: `expressions.json` (`manual.*` 는 직접 읽기, `regex.*` 는 보조 후보)")
A("- 읽기 범위·검증: `validation.md` · 미결: `issues.md`")
with open(os.path.join(OUT, "review.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

log("source", SRC, len(raw), "bytes", len(text), "cp", "sha256", H0)
log("nodes", len(NODES), "keys", len(KEYS), "dups", len(DUPS), "types", {t: sum(1 for n in NODES if n['type'] == t) for t in ['object', 'array', 'string', 'number', 'boolean', 'null']})
log("morph applied", len(applied), "tokens", sum(len(r["tokens"]) for r in applied), "excluded", len(excluded), "fieldname occ", len(KEYS))
log("segrev occurrences", len(segrev["occurrences"]))
log("expressions", len(EXPR), "manual", len(man["expressions"]))
log("sha256_end", H1, "same" if H0 == H1 else "CHANGED")
log("build_checks_failed", len(fails))
for f_ in fails:
    log("FAIL", f_)
with open(os.path.join(OUT, "build-output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
sys.exit(1 if fails else 0)
