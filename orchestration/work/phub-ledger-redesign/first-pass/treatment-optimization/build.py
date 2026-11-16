#!/usr/bin/env python3
"""treatment-optimization.json 1차 조사 산출물 재현 생성기.

실행(레포 루트에서):
  OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
    python orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/build.py

입력: 원본 원장(읽기 전용) + 이 폴더의 manual/*.json (직접 읽기 기록).
출력: 이 폴더 안의 source-map.json · morphology.json · expressions.json · coverage.json ·
      review.md · review-part-*.md · issues.md · build-output.txt.
원본과 다른 폴더는 쓰지 않는다. validation.md 는 생성하지 않는다(verify 실행 결과를 손으로 적는 문서).
"""
import hashlib
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, *[".."] * 5))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json"
SRC = os.path.join(ROOT, SRC_REL)
MANUAL = os.path.join(OUT, "manual")
EXPECTED_SHA = "07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b"

LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def esc_tok(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- JSON 위치 스캐너
class Scanner:
    """원문 텍스트를 직접 훑어 노드마다 코드포인트 구간을 기록한다. 중복 키를 덮어쓰지 않고 감지한다."""

    WS = " \t\n\r"

    def __init__(self, text, byte_off):
        self.t = text
        self.i = 0
        self.b = byte_off
        self.nodes = []
        self.keys = []
        self.dups = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def string_lit(self):
        t = self.t
        s = self.i
        assert t[s] == '"', (s, t[s])
        j = s + 1
        while True:
            c = t[j]
            if c == "\\":
                j += 2
                continue
            if c == '"':
                break
            j += 1
        e = j + 1
        lit = t[s:e]
        self.i = e
        return s, e, lit, json.loads(lit)

    def node(self, ptr, parent, key, index):
        self.ws()
        t = self.t
        s = self.i
        c = t[s]
        rec = OrderedDict(pointer=ptr, parent=parent, key=key, index=index)
        self.nodes.append(rec)
        if c == "{":
            rec["type"] = "object"
            self.i += 1
            children = []
            seen = {}
            order = 0
            self.ws()
            if t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    ks, ke, klit, k = self.string_lit()
                    self.ws()
                    assert t[self.i] == ":"
                    self.i += 1
                    cptr = ptr + "/" + esc_tok(k)
                    if k in seen:
                        self.dups.append({"object_pointer": ptr, "key": k, "first_order": seen[k], "dup_order": order, "span": [ks, ke]})
                    seen.setdefault(k, order)
                    self.keys.append(OrderedDict(key=k, object_pointer=ptr, value_pointer=cptr, order_in_object=order,
                                                 span=[ks, ke], byte_span=[self.b[ks], self.b[ke]], has_escape="\\" in klit))
                    children.append(k)
                    self.node(cptr, ptr, k, None)
                    order += 1
                    self.ws()
                    if t[self.i] == ",":
                        self.i += 1
                        continue
                    assert t[self.i] == "}"
                    self.i += 1
                    break
            rec["children"] = children
            rec["length"] = len(children)
        elif c == "[":
            rec["type"] = "array"
            self.i += 1
            n = 0
            self.ws()
            if t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.node(ptr + "/" + str(n), ptr, None, n)
                    n += 1
                    self.ws()
                    if t[self.i] == ",":
                        self.i += 1
                        continue
                    assert t[self.i] == "]"
                    self.i += 1
                    break
            rec["length"] = n
        elif c == '"':
            ss, se, lit, val = self.string_lit()
            rec["type"] = "string"
            rec["value"] = val
            rec["value_span"] = [ss + 1, se - 1]
            rec["has_escape"] = "\\" in lit
            rec["json_literal"] = lit
        else:
            m = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(t, s)
            lit = m.group(0)
            self.i = m.end()
            val = json.loads(lit)
            rec["type"] = ("boolean" if isinstance(val, bool) else "null" if val is None else
                           "integer" if isinstance(val, int) else "number")
            rec["value"] = val
            rec["json_literal"] = lit
        e = self.i
        rec["span"] = [s, e]
        rec["byte_span"] = [self.b[s], self.b[e]]
        return rec


def rebuild(nodes):
    by = {n["pointer"]: n for n in nodes}

    def r(p):
        n = by[p]
        if n["type"] == "object":
            return OrderedDict((k, r(p + "/" + esc_tok(k))) for k in n["children"])
        if n["type"] == "array":
            return [r(p + "/" + str(i)) for i in range(n["length"])]
        return n["value"]
    return r("")


def pattern_of(ptr):
    return "/".join("*" if x.isdigit() else x for x in ptr.split("/"))


# ---------------------------------------------------------------- 구획
SEGMENTS = [
    ("SEG-00", "상위 메타·원칙", "", "review-part-1.md"),
    *[(f"SEG-{i + 1:02d}", f"by_concern/{i}", f"/by_concern/{i}", "review-part-1.md" if i < 4 else "review-part-2.md") for i in range(8)],
    ("SEG-09", "by_age_group 전체", "/by_age_group", "review-part-3.md"),
    ("SEG-10", "combination_rules 전체", "/combination_rules", "review-part-3.md"),
    *[(f"SEG-{11 + i}", f"annual_plans/{i}", f"/annual_plans/{i}", "review-part-4.md") for i in range(3)],
]


def owner(ptr):
    m = re.match(r"^/by_concern/(\d+)(/|$)", ptr)
    if m:
        return f"SEG-{int(m.group(1)) + 1:02d}"
    if re.match(r"^/by_age_group/\d+(/|$)", ptr):
        return "SEG-09"
    if re.match(r"^/combination_rules/\d+(/|$)", ptr):
        return "SEG-10"
    m = re.match(r"^/annual_plans/(\d+)(/|$)", ptr)
    if m:
        return f"SEG-{11 + int(m.group(1))}"
    return "SEG-00"


def is_leaf(n):
    return n["type"] not in ("object", "array") or n["length"] == 0


# ---------------------------------------------------------------- 형태소 분석 적용/제외
EXCLUDE_RULES = [
    (r"^/version$", "버전 코드값(숫자.숫자). 언어 텍스트 아님"),
    (r"^/updated$", "날짜 코드값(YYYY-MM-DD). 언어 텍스트 아님"),
    (r"^/by_concern/\d+/icon$", "아이콘 식별자(영문 소문자 코드). 언어 텍스트 아님"),
    (r"^/by_concern/\d+/severity_levels/\d+/evidence_level$", "등급 코드값(영문 열거: high·moderate). 자연어 문장 아님"),
    (r"^/combination_rules/\d+/priority$", "우선도 코드값(영문 열거: critical·important·moderate·caution). 자연어 문장 아님"),
]


def exclusion(ptr):
    for rx, why in EXCLUDE_RULES:
        if re.match(rx, ptr):
            return why
    return None


def scripts(s):
    out = []
    if re.search(r"[가-힣]", s):
        out.append("hangul")
    if re.search(r"[A-Za-z]", s):
        out.append("latin")
    if re.search(r"[\u4e00-\u9fff]", s):
        out.append("hanja")
    if re.search(r"\d", s):
        out.append("digit")
    return out


# ---------------------------------------------------------------- 자동 후보 정규식 (전수 의미 해석 아님)
AUTO_PATTERNS = [
    ("R01-number-unit", r"\d+(?:\.\d+)?(?:\s?[-~]\s?\d+(?:\.\d+)?)?\s?(?:nm|회|차|개월|주|일|시간|만원|건|사이클)(?:\+|/년)?", "숫자(범위)+단위"),
    ("R02-roman-range", r"\b[IVX]+~[IVX]+\b", "로마숫자 범위"),
    ("R03-parenthetical", r"\([^()]*\)", "괄호 구간"),
    ("R04-slash-join", r"[^\s/()·,+→:.]+(?:\s?/\s?[^\s/()·,+→:.]+)+", "`/` 로 이은 구간"),
    ("R05-plus-join", r"[^\s+()→,:.]+(?:\s?\+\s?[^\s+()→,:.]+)+", "`+` 로 이은 구간"),
    ("R06-arrow", r"→", "화살표(순서 표기)"),
    ("R07-or-alt", r"(?:(?<=\s)|^)(?:or|또는)(?=\s)", "대안 접속(or·또는)"),
    ("R08-prohibit", r"금지|금기|피(?:하|할)|avoid", "금지·회피"),
    ("R09-possible", r"가능|할 수 있|수 있음|수 있어", "가능성"),
    ("R10-sameday", r"같은\s?날|당일|동시|직후|즉시|즉각", "같은 날·동시·직후"),
    ("R11-within-after", r"(?:(?<=\s)|^)(?:후|내|이내|이상|이후|후부터)(?=[\s,.)]|$)|후부터|최소", "후·내·이내·이상·최소"),
    ("R12-order", r"먼저|나중|선행|시작|마무리", "순서·시작·마무리"),
    ("R13-interval-repeat", r"간격|반복|사이사이|교차|매회|지속", "간격·반복·교차"),
    ("R14-risk", r"위험|감염|용해|반동|PIH|결절|확산|저하", "위험·부작용 어휘"),
    ("R15-recommend", r"권장|권고|필수|필요|선택|중요|중시|우선|고려|충분", "권고·필요·선택"),
    ("R16-limit-only", r"(?<=[가-힣])만(?=[\s,.)]|$)|단독|제한|미승인|승인 0건", "제한·단독·미승인"),
    ("R17-negation", r"않|없|미(?=승인|용)|비(?=수술|침습|가교|마사지|필요)|불필요|부자연", "부정 표지(불완전 목록)"),
    ("R18-degree", r"저출력|고출력|고에너지|과도한|과잉|약한|얕은|깊은|딥|미세|심한|뚜렷한|가벼운|경미|중등도|중증|적극적|점진적|공격적|장기|광범위|대량|소규모|다양한|엄격한|정확한|충분한|적정|초과", "정도·깊이·세기 수식(불완전 목록)"),
    ("R19-season-time", r"여름철|가을|연말|하반기|(?:(?<=\s)|^)(?:월|분기|연)(?=[\s,]|$)", "계절·시기·빈도 단위(어절 단독 월·분기·연)"),
    ("R20-latin-run", r"[A-Za-z][A-Za-z0-9:.\-]*(?:\s[A-Za-z][A-Za-z0-9:.\-]*)*", "라틴 문자 연속 구간"),
]
AUTO_RX = [(pid, re.compile(rx), desc) for pid, rx, desc in AUTO_PATTERNS]

CLAUSE_SPLIT = re.compile(r"(?:\.\s|\.$|;\s|→|,\s|:\s| — )")

# 수식·부정 성격 토큰(누락 점검용). 이 목록에 걸린 토큰이 수동 표현으로 덮였는지 또는 검토됐는지 확인한다.
CHECK_TAGS = {"MAG", "MAJ", "MM", "VA", "XPN", "XSA", "VCN", "VX", "NR"}
CHECK_FORMS = {"않", "없", "못", "미", "비", "불", "만", "도", "후", "내", "이내", "이상", "최소", "가능", "금지", "단독", "동시", "당일", "직후", "즉시"}


def main():
    sha_start = sha256(SRC)
    raw_bytes = open(SRC, "rb").read()
    text = raw_bytes.decode("utf-8")
    byte_off = [0] * (len(text) + 1)
    acc = 0
    for i, ch in enumerate(text):
        byte_off[i] = acc
        acc += len(ch.encode("utf-8"))
    byte_off[len(text)] = acc
    sc = Scanner(text, byte_off)
    sc.node("", None, None, None)
    sc.ws()
    assert sc.i == len(text), "trailing content"
    nodes = sc.nodes
    parsed = json.loads(text, object_pairs_hook=OrderedDict)
    assert rebuild(nodes) == parsed, "scanner rebuild mismatch"
    log("source", SRC_REL, "sha256", sha_start, "expected_match", sha_start == EXPECTED_SHA)
    log("nodes", len(nodes), "keys", len(sc.keys), "dups", len(sc.dups))

    by_ptr = {n["pointer"]: n for n in nodes}
    for n in nodes:
        n["segment"] = owner(n["pointer"])
        n["pattern"] = pattern_of(n["pointer"])
        if n["type"] == "string":
            vs = n["value_span"]
            n["literal_equals_decoded"] = text[vs[0]:vs[1]] == n["value"]
        # 문맥: 가장 가까운 항목 객체와 그 형제 필드
        parts = n["pointer"].split("/")
        ctx = OrderedDict()
        if len(parts) >= 3 and parts[2].isdigit():
            ctx["item_pointer"] = "/".join(parts[:3])
        if len(parts) >= 5 and parts[3] in ("severity_levels", "schedule") and parts[4].isdigit():
            ctx["sub_item_pointer"] = "/".join(parts[:5])
        if n["parent"] is not None and by_ptr[n["parent"]]["type"] == "object":
            ctx["sibling_pointers"] = [n["parent"] + "/" + esc_tok(k) for k in by_ptr[n["parent"]]["children"] if k != n["key"]]
        elif n["parent"] is not None:
            ctx["array_pointer"] = n["parent"]
            ctx["array_length"] = by_ptr[n["parent"]]["length"]
        ctx["block"] = parts[1] if len(parts) > 1 else "(root)"
        n["context"] = ctx

    field_occ = defaultdict(lambda: defaultdict(list))
    for k in sc.keys:
        field_occ[k["key"]][pattern_of(k["value_pointer"])].append(k["value_pointer"])

    source = OrderedDict(path=SRC_REL, size_bytes=len(raw_bytes), code_points=len(text), sha256_start=sha_start,
                         encoding="utf-8", bom=raw_bytes[:3] == b"\xef\xbb\xbf", newline_count=text.count("\n"),
                         backslash_count=text.count("\\"), non_bmp_count=sum(ord(c) > 0xFFFF for c in text))
    source_map = OrderedDict(
        source=source,
        notes=[
            "span: 원본 파일 전체 디코딩 텍스트 기준 Unicode 코드 포인트 [start,end). 문자열 노드의 span 은 따옴표 포함(JSON 리터럴 구간).",
            "value_span: 문자열 JSON 리터럴 내부(따옴표 제외) 코드 포인트 구간. 이스케이프가 있으면 디코딩 값과 다를 수 있다 → literal_equals_decoded 로 표시. 이 원장은 백슬래시 0 이라 전부 동일.",
            "byte_span: UTF-8 파일 바이트 [start,end).",
            "segment: 그 노드를 소유하는 구획. coverage.json 참조.",
            "중복 키는 json 파서에 맡기지 않고 스캐너가 직접 감지한다(duplicate_keys).",
        ],
        duplicate_keys=sc.dups,
        field_name_occurrences={k: dict(v) for k, v in field_occ.items()},
        keys=sc.keys,
        nodes=nodes,
    )

    # ------------------------------------------------ manual
    manual = {}
    for sid, *_ in SEGMENTS:
        p = os.path.join(MANUAL, sid.lower() + ".json")
        if os.path.exists(p):
            manual[sid] = json.load(open(p, encoding="utf-8"))
    seg_review = json.load(open(os.path.join(MANUAL, "segmentation-review.json"), encoding="utf-8")) if os.path.exists(os.path.join(MANUAL, "segmentation-review.json")) else {"entries": []}
    expr_review = json.load(open(os.path.join(MANUAL, "expression-review.json"), encoding="utf-8")) if os.path.exists(os.path.join(MANUAL, "expression-review.json")) else {"auto_false_positives": [], "uncovered_token_reviews": []}
    global_issues = json.load(open(os.path.join(MANUAL, "global-issues.json"), encoding="utf-8")) if os.path.exists(os.path.join(MANUAL, "global-issues.json")) else {"issues": []}

    # ------------------------------------------------ morphology
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")
    strings = [n for n in nodes if n["type"] == "string"]
    applied, excluded, nonstring = [], [], []
    tokens = []
    for n in strings:
        why = exclusion(n["pointer"])
        rec = OrderedDict(pointer=n["pointer"], segment=n["segment"], value=n["value"], scripts=scripts(n["value"]))
        if why:
            rec["reason"] = why
            excluded.append(rec)
            continue
        if n["value"] == "":
            rec["reason"] = "빈 문자열"
            excluded.append(rec)
            continue
        toks = kiwi.tokenize(n["value"])
        tids = []
        for i, t in enumerate(toks):
            tid = f"{n['pointer']}#t{i}"
            s, e = t.start, t.start + t.len
            tokens.append(OrderedDict(id=tid, value_pointer=n["pointer"], segment=n["segment"], i=i, form=t.form, tag=t.tag,
                                      lemma=t.lemma, start=s, end=e, surface=n["value"][s:e], surface_equals_form=n["value"][s:e] == t.form,
                                      word_position=t.word_position, sent_position=t.sent_position, sub_sent_position=t.sub_sent_position))
            tids.append(tid)
        rec["token_count"] = len(tids)
        if "latin" in rec["scripts"] and "hangul" not in rec["scripts"]:
            rec["language_note"] = "라틴 문자만 있는 값: Kiwi 는 SL(외국어) 토큰으로 자를 뿐 영어 형태소·기본형을 제공하지 않는다(K-02)."
        elif "latin" in rec["scripts"] or "hanja" in rec["scripts"]:
            rec["language_note"] = "혼합 문자 값: 라틴/한자 구간은 SL/SH 토큰으로만 나뉜다(K-02)."
        applied.append(rec)
    for n in nodes:
        if n["type"] not in ("string", "object", "array"):
            nonstring.append(OrderedDict(pointer=n["pointer"], segment=n["segment"], type=n["type"], value=n["value"],
                                         reason="비문자열 말단(정수 등). 원문 값만 보존하고 형태소 분석 대상 아님"))
    field_names = []
    for k in sorted(field_occ):
        toks = kiwi.tokenize(k)
        field_names.append(OrderedDict(field_name=k, role="field_name(필드명 — 원문 텍스트와 별도)",
                                       occurrence_count=sum(len(v) for v in field_occ[k].values()),
                                       patterns=sorted(field_occ[k]),
                                       tokens=[OrderedDict(form=t.form, tag=t.tag, lemma=t.lemma, start=t.start, end=t.start + t.len) for t in toks]))
    tok_by_val = defaultdict(list)
    for t in tokens:
        tok_by_val[t["value_pointer"]].append(t)

    # 알려진 오분절 기록 검증·부착
    seg_entries = []
    for e in seg_review.get("entries", []):
        v = by_ptr[e["pointer"]]["value"]
        s, en = e["span"]
        assert v[s:en] == e["text"], ("segmentation-review text mismatch", e)
        inside = [f"{t['form']}/{t['tag']}" for t in tok_by_val[e["pointer"]] if t["start"] < en and t["end"] > s]
        assert inside == e["raw_tokens"], ("segmentation-review raw tokens mismatch", e, inside)
        seg_entries.append(e)

    morphology = OrderedDict(
        analyzer=OrderedDict(name="kiwipiepy", version=kiwipiepy.__version__, model_type="cong", num_workers=1,
                             default_dict=True, user_dict=None, typo_correction=None,
                             tokenize_options="기본값(match_options=ALL, normalize_coda=False, split_complex=False, split_sents=False, stopwords=None)",
                             tagset="Kiwi(세종 기반) 품사 태그", env="uv run --python 3.12 --with kiwipiepy==0.24.1, OMP_NUM_THREADS=1"),
        offset_unit="각 값 문자열(디코딩) 기준 Unicode 코드 포인트 [start,end). 파일 기준 = source-map value_span[0] + start. Kiwi 의 start/len 을 그대로 썼다(BMP 밖 문자 0 이라 UTF-16 과 코드포인트가 같다).",
        lemma_note="lemma 는 Kiwi Token.lemma 를 그대로 기록했다(용언은 '-다' 붙인 꼴, 그 외는 form 과 같음). 도구가 주지 않는 기본형을 만들어 채우지 않았다.",
        surface_note="surface 는 원문 구간 그대로. 활용·축약으로 form 과 surface 가 다르면 surface_equals_form=false.",
        no_stopword_removal="조사·어미·부사·형용사·부정 표지를 지우지 않았다.",
        counts=OrderedDict(string_values=len(strings), applied=len(applied), excluded=len(excluded),
                           nonstring_leaves=len(nonstring), tokens=len(tokens), field_names=len(field_names),
                           known_segmentation_issues=len(seg_entries)),
        applied_values=applied,
        excluded_values=excluded,
        nonstring_leaves=nonstring,
        field_names=field_names,
        known_segmentation_issues=seg_entries,
        tokens=tokens,
    )

    # ------------------------------------------------ expressions
    exprs = []
    fp_keys = {(f["pointer"], f["pattern"], f["span"][0], f["span"][1]): f for f in expr_review.get("auto_false_positives", [])}
    used_fp = set()
    for n in strings:
        if exclusion(n["pointer"]):
            continue
        v = n["value"]
        for pid, rx, desc in AUTO_RX:
            for m in rx.finditer(v):
                if m.end() == m.start():
                    continue
                key = (n["pointer"], pid, m.start(), m.end())
                rec = OrderedDict(id=f"{n['pointer']}#{pid}@{m.start()}", source="auto_regex", pattern=pid, pattern_desc=desc,
                                  pointer=n["pointer"], segment=n["segment"], span=[m.start(), m.end()], text=m.group(0))
                if key in fp_keys:
                    rec["review"] = OrderedDict(false_positive=True, note=fp_keys[key]["note"])
                    used_fp.add(key)
                exprs.append(rec)
        # 절 단위(문맥 보존용 자동 분할)
        pos = 0
        cuts = [(m.start(), m.end()) for m in CLAUSE_SPLIT.finditer(v)]
        if cuts:
            ci = 0
            for (cs, ce) in cuts + [(len(v), len(v))]:
                seg_text = v[pos:cs]
                ls = pos + (len(seg_text) - len(seg_text.lstrip()))
                re_ = cs - (len(seg_text) - len(seg_text.rstrip()))
                if re_ > ls:
                    exprs.append(OrderedDict(id=f"{n['pointer']}#clause{ci}", source="auto_clause", pattern="C01-clause-split",
                                             pattern_desc="`. ` `; ` `→` `, ` `: ` ` — ` 기준 절 분할(문맥 단위, 의미 단위 아님)",
                                             pointer=n["pointer"], segment=n["segment"], span=[ls, re_], text=v[ls:re_]))
                    ci += 1
                pos = ce
    missing_fp = set(fp_keys) - used_fp
    assert not missing_fp, ("expression-review false positive not matched", missing_fp)
    # 수동 표현
    manual_count = 0
    for sid, m in manual.items():
        for j, me in enumerate(m.get("manual_expressions", [])):
            n = by_ptr[me["pointer"]]
            v = n["value"]
            occ = [x.start() for x in re.finditer(re.escape(me["text"]), v)]
            assert occ, ("manual expression not found", sid, me)
            k = me.get("occurrence", 0)
            if len(occ) > 1 and "occurrence" not in me:
                raise AssertionError(("manual expression ambiguous; set occurrence", sid, me, occ))
            s = occ[k]
            exprs.append(OrderedDict(id=f"{sid}#m{j}", source="manual_direct_reading", pattern=None, pointer=me["pointer"],
                                     segment=n["segment"], span=[s, s + len(me["text"])], text=me["text"], kinds=me["kinds"],
                                     note=me.get("note")))
            manual_count += 1
            assert n["segment"] == sid, ("manual expression outside its segment", sid, me)
    # 수식·부정 성격 토큰의 수동 표현 포괄 점검
    man_spans = defaultdict(list)
    for e in exprs:
        if e["source"] == "manual_direct_reading":
            man_spans[e["pointer"]].append(tuple(e["span"]))
    reviewed = {(r["pointer"], r["span"][0], r["span"][1]): r for r in expr_review.get("uncovered_token_reviews", [])}
    check = []
    for t in tokens:
        if t["tag"] in CHECK_TAGS or t["form"] in CHECK_FORMS:
            cov = any(s <= t["start"] and t["end"] <= e for s, e in man_spans[t["value_pointer"]])
            mis = any(se["pointer"] == t["value_pointer"] and se["span"][0] <= t["start"] and t["end"] <= se["span"][1] for se in seg_entries)
            st = ("known_missegmentation" if mis else "covered_by_manual" if cov else
                  ("reviewed" if (t["value_pointer"], t["start"], t["end"]) in reviewed else "UNREVIEWED"))
            rec = OrderedDict(token_id=t["id"], pointer=t["value_pointer"], span=[t["start"], t["end"]], form=t["form"], tag=t["tag"], status=st)
            if st == "reviewed":
                rec["review_note"] = reviewed[(t["value_pointer"], t["start"], t["end"])]["note"]
            check.append(rec)
    unrev = [c for c in check if c["status"] == "UNREVIEWED"]
    stale_reviews = [k for k in reviewed if not any((c["pointer"], c["span"][0], c["span"][1]) == k for c in check)]
    assert not stale_reviews, ("stale uncovered_token_reviews", stale_reviews)
    # 수동·자동 어느 쪽에도 덮이지 않은 어절(검토 보조)
    all_spans = defaultdict(list)
    for e in exprs:
        if e["source"] != "auto_clause" and not e.get("review", {}).get("false_positive"):
            all_spans[e["pointer"]].append(tuple(e["span"]))
    uncovered_eojeol = []
    for n in strings:
        if exclusion(n["pointer"]):
            continue
        v = n["value"]
        for m in re.finditer(r"\S+", v):
            ws, we = m.start(), m.end()
            while ws < we and v[ws] in ".,;:()—'":
                ws += 1
            while we > ws and v[we - 1] in ".,;:()—'":
                we -= 1
            if we == ws:
                continue
            if not any(s <= ws and we <= e for s, e in all_spans[n["pointer"]]):
                uncovered_eojeol.append(OrderedDict(pointer=n["pointer"], span=[ws, we], text=v[ws:we]))

    counts = defaultdict(int)
    for e in exprs:
        counts[e["source"]] += 1
    expressions = OrderedDict(
        notes=[
            "span: 각 값 문자열 기준 Unicode 코드 포인트 [start,end). 겹침은 의도된 것(같은 구간을 여러 관점으로 본다).",
            "auto_regex 는 AUTO_PATTERNS 의 실제 일치분뿐이다. 패턴 밖 표현을 덮지 않는다. 키워드 목록은 불완전 목록이다.",
            "auto_clause 는 구두점·화살표 기준 기계 분할이며 의미 단위가 아니다.",
            "manual_direct_reading 은 구획별 직접 읽기에서 적은 구절(manual/seg-XX.json). kinds 는 탐색 관점 태그이며 확정 분류가 아니다.",
            "review.false_positive=true 는 직접 대조로 확인한 자동 후보 오탐(manual/expression-review.json).",
            "modifier_token_check: Kiwi 의 수식·부정 성격 토큰(CHECK_TAGS·CHECK_FORMS)이 수동 표현에 덮였는지, 알려진 오분절 구간 안인지(known_missegmentation), 아니면 사유를 적어 검토했는지. UNREVIEWED 0 이 목표.",
            "uncovered_eojeol: 앞뒤 구두점을 뗀 어절 중 자동 정규식(오탐 제외)·수동 구절 어느 것에도 덮이지 않은 것. 직접 전수 검토했다(validation.md §3) — 대부분 단독 시술명·고민명 값이다.",
        ],
        auto_patterns=[OrderedDict(id=p, regex=r, desc=d) for p, r, d in AUTO_PATTERNS],
        check_tags=sorted(CHECK_TAGS), check_forms=sorted(CHECK_FORMS),
        counts=OrderedDict(total=len(exprs), **counts, auto_false_positive=len(used_fp), modifier_tokens_checked=len(check),
                           modifier_tokens_unreviewed=len(unrev), uncovered_eojeol=len(uncovered_eojeol)),
        expressions=exprs,
        modifier_token_check=check,
        uncovered_eojeol=uncovered_eojeol,
    )

    # ------------------------------------------------ coverage
    coverage_segments = []
    for sid, title, prefix, part in SEGMENTS:
        owned = [n["pointer"] for n in nodes if n["segment"] == sid]
        leaves = [n["pointer"] for n in nodes if n["segment"] == sid and is_leaf(n)]
        ctx = []
        if sid != "SEG-00":
            blk = prefix.split("/")[1]
            ctx = ["", "/" + blk]
            if sid.startswith("SEG-1") and sid >= "SEG-11":
                ctx.append("/by_age_group")
        m = manual.get(sid)
        coverage_segments.append(OrderedDict(
            segment=sid, title=title,
            pointer_range=(prefix + "/**" if prefix else "/(root, 상위 스칼라·optimization_principles·네 블록 컨테이너 자체)"),
            owned_node_count=len(owned), owned_leaf_count=len(leaves), owned_leaf_pointers=leaves,
            owned_container_pointers=[p for p in owned if p not in leaves],
            context_refs=ctx,
            context_note=("소유하지 않고 문맥으로만 참조하는 포인터. 값의 소유는 owned_* 에만 있다." if ctx else None),
            machine_extraction="done",
            direct_reading=(m["read_status"] if m else "not_read"),
            direct_reading_note=(m.get("read_note") if m else None),
            manual_record=(f"manual/{sid.lower()}.json" if m else None),
            review_file=part, review_anchor=f"#{sid.lower()}",
        ))
    coverage = OrderedDict(
        source_sha256=sha_start, segment_rule="build.py owner(): /by_concern/N → SEG-(N+1), /by_age_group/N → SEG-09, /combination_rules/N → SEG-10, /annual_plans/N → SEG-(11+N), 그 외 SEG-00",
        status_values={"machine_extraction": "done = build.py 가 구조·값 추출", "direct_reading": "direct_read_done = 원문을 직접 읽고 manual 기록 저장 / not_read = 미독"},
        segments=coverage_segments,
    )

    # ------------------------------------------------ write JSON
    def dump(name, obj):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write("\n")
    dump("source-map.json", source_map)
    dump("morphology.json", morphology)
    dump("expressions.json", expressions)
    dump("coverage.json", coverage)

    # ------------------------------------------------ markdown
    write_reviews(nodes, by_ptr, manual, source, sc, field_occ, morphology, expressions, coverage_segments, text)
    write_issues(manual, global_issues, expressions, morphology)

    sha_end = sha256(SRC)
    log("tokens", len(tokens), "applied", len(applied), "excluded", len(excluded), "nonstring", len(nonstring))
    log("expressions", dict(expressions["counts"]))
    log("segments_read", sum(1 for c in coverage_segments if c["direct_reading"] == "direct_read_done"), "/", len(coverage_segments))
    log("sha256_end", sha_end, "unchanged", sha_end == sha_start)
    with open(os.path.join(OUT, "build-output.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")
    if sha_end != sha_start or sha_start != EXPECTED_SHA:
        sys.exit(2)


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def jtype(n):
    if n["type"] in ("object", "array"):
        return f"{n['type']}({n['length']})"
    return n["type"]


def column_table(nodes, by_ptr):
    rows = OrderedDict()
    obj_counts = defaultdict(int)
    for n in nodes:
        if n["type"] == "object":
            obj_counts[n["pattern"]] += 1
    for n in nodes:
        if n["pointer"] == "":
            continue
        variant = n["type"]
        if n["type"] in ("array", "object") and n["length"] == 0:
            variant = f"empty_{n['type']}"
        elif n["type"] == "string" and n["value"] == "":
            variant = "empty_string"
        key = (n["pattern"], variant)
        r = rows.setdefault(key, OrderedDict(count=0, example=n, lengths=set()))
        r["count"] += 1
        if n["type"] in ("array", "object"):
            r["lengths"].add(n["length"])
    out = ["| 원본 컬럼명 / 경로 패턴 | 자료형·변형 | 중첩 구조 | 출현 수 | 존재 범위 | 원문 예시 (첫 출현) | 예시 Pointer |", "|---|---|---|---|---|---|---|"]
    for (pat, variant), r in rows.items():
        ex = r["example"]
        parent_pat = pattern_of(ex["parent"]) if ex["parent"] is not None else None
        presence = ""
        if ex["key"] is not None and parent_pat in obj_counts:
            tot = obj_counts[parent_pat]
            have = sum(1 for n in nodes if n["type"] == "object" and n["pattern"] == parent_pat and ex["key"] in n["children"])
            presence = f"{have}/{tot} 객체" + (" (선택적 필드)" if have < tot else "")
        if ex["type"] == "object":
            nest = "객체 키: " + ", ".join(f"`{k}`" for k in ex["children"])
        elif ex["type"] == "array":
            ln = sorted(r["lengths"])
            nest = f"배열 길이 {ln[0]}~{ln[-1]}" if len(ln) > 1 else f"배열 길이 {ln[0]}"
        else:
            nest = "말단"
        exv = ex.get("json_literal", "") if ex["type"] not in ("object", "array") else ("[]" if variant == "empty_array" else "(컨테이너)")
        if len(exv) > 90:
            exv = exv[:90] + "…(전체는 해당 구획)"
        out.append(f"| `{md(pat)}` | {variant} | {md(nest)} | {r['count']} | {presence} | {md(exv)} | `{md(ex['pointer'])}` |")
    return "\n".join(out)


def col_name(n, by):
    """원본 컬럼명: 객체 필드는 키 그대로, 배열 원소는 「부모 필드명[인덱스]」."""
    if n["key"] is not None:
        return n["key"]
    if n["index"] is not None:
        pk = by[n["parent"]]["key"]
        return f"{pk}[{n['index']}]" if pk is not None else f"{col_name(by[n['parent']], by)}[{n['index']}]"
    return "(root)"


def seg_section(sid, title, nodes, manual, part_name):
    lines = [f"<a id=\"{sid.lower()}\"></a>", f"## {sid} — {title}", ""]
    own = [n for n in nodes if n["segment"] == sid]
    m = manual.get(sid)
    lines.append(f"- 직접 읽기: **{m['read_status'] if m else 'not_read'}** — {m.get('read_note', '') if m else ''}")
    lines.append(f"- 소유 노드 {len(own)} · 말단(빈 컨테이너 포함) {sum(1 for n in own if is_leaf(n))}")
    lines.append("")
    lines.append("### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)")
    lines.append("")
    lines.append("| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |")
    lines.append("|---|---|---|---|")
    by = {x["pointer"]: x for x in nodes}
    for n in own:
        col = col_name(n, by)
        if n["type"] in ("object", "array"):
            val = ("[]" if n["length"] == 0 and n["type"] == "array" else "{}" if n["length"] == 0 else
                   ("키: " + ", ".join(n["children"])) if n["type"] == "object" else f"원소 {n['length']}개")
            val = f"_{md(val)}_"
        else:
            val = md(n["json_literal"])
        lines.append(f"| `{md(n['pointer'])}` | `{md(col)}` | {jtype(n)} | {val} |")
    lines.append("")
    if m:
        lines.append("### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)")
        lines.append("")
        lines.append("| ID | 상태 | 근거 Pointer | 관찰 |")
        lines.append("|---|---|---|---|")
        for o in m.get("observations", []):
            lines.append(f"| {o['id']} | {o['status']} | {'<br>'.join('`' + md(p) + '`' for p in o['pointers'])} | {md(o['text'])} |")
        lines.append("")
        lines.append(f"### 수동 수집 구절 ({len(m.get('manual_expressions', []))}건 · 구간은 expressions.json `source=manual_direct_reading`)")
        lines.append("")
        lines.append("| Pointer | 원문 구절 | 탐색 관점(kinds) |")
        lines.append("|---|---|---|")
        for me in m.get("manual_expressions", []):
            lines.append(f"| `{md(me['pointer'])}` | {md(me['text'])} | {md(', '.join(me['kinds']))} |")
        lines.append("")
        if m.get("issues"):
            lines.append("### 이 구획의 미결 (issues.md 에 모음)")
            lines.append("")
            for it in m["issues"]:
                lines.append(f"- **{it['id']}** [{it['class']}] {it['text']} — {', '.join('`' + p + '`' for p in it['pointers'])}")
            lines.append("")
    return "\n".join(lines)


def write_reviews(nodes, by_ptr, manual, source, sc, field_occ, morphology, expressions, cov, text):
    parts = defaultdict(list)
    for sid, title, prefix, part in SEGMENTS:
        parts[part].append((sid, title))
    for part, segs in parts.items():
        body = [f"# treatment-optimization.json — 1차 조사 {part.replace('.md', '')}", "",
                "> 원문 값 표는 build.py 가 원본에서 자동 생성했다. 잠정 관찰·수동 구절은 manual/seg-XX.json 의 직접 읽기 기록이다. 원장의 임상·규제 서술은 **원장에 적혀 있다는 사실**로만 기록했고 검증·보충하지 않았다.",
                "> 상태 기호: P 잠정 · B 원문 정보 부족 · I 원문 내 불일치 후보 · F 후속 의미 조사 · K 알려진 분석 한계 · A 에이전트 추출 오류 · C 사용자 결정 필요.", "",
                "[← 목차 review.md](./review.md)", ""]
        for sid, title in segs:
            body.append(seg_section(sid, title, nodes, manual, part))
        with open(os.path.join(OUT, part), "w", encoding="utf-8") as f:
            f.write("\n".join(body) + "\n")

    mc = morphology["counts"]
    ec = expressions["counts"]
    read = sum(1 for c in cov if c["direct_reading"] == "direct_read_done")
    L = []
    L.append("# treatment-optimization.json — 1차 조사 (읽기용 목차)")
    L.append("")
    L.append(f"**상태**: 1차 범위 — 구획 직접 읽기 {read}/{len(cov)} · 기계 검증은 [validation.md](./validation.md) · **원장 전체 완료 아님** — 미결은 [issues.md](./issues.md).")
    L.append("")
    L.append("> 이 문서와 review-part-*.md 는 **원문 대응**(자동 생성 표)과 **잠정 관찰**(직접 읽기)을 다른 칸·절로 나눈다. 공통 개념 ID·동의어 병합·부위 체계·관계 방향·적용 조건은 정하지 않았다(1차 범위 밖). 최적화 추천 문구를 확정 관계·임상 사실로 승인하지 않는다.")
    L.append("")
    L.append("## 0. 원본과 기록 위치")
    L.append("")
    L.append("| 항목 | 값 |")
    L.append("|---|---|")
    L.append(f"| 원본 | `{source['path']}` |")
    L.append(f"| 크기 | {source['size_bytes']:,} bytes · {source['code_points']:,} code points · UTF-8 · BOM {'있음' if source['bom'] else '없음'} · 개행 {source['newline_count']} · 백슬래시 {source['backslash_count']} · BMP 밖 {source['non_bmp_count']} |")
    L.append(f"| sha256 | `{source['sha256_start']}` (원장 폴더 HASHES.txt 접두 `07b9ebe0a843280b` 와 일치) |")
    L.append(f"| 구조·값 | [source-map.json](./source-map.json) — 노드 {len(nodes)} · 키 출현 {len(sc.keys)} · 필드명 {len(field_occ)}종 · 중복 키 {len(sc.dups)} |")
    L.append(f"| 형태소 | [morphology.json](./morphology.json) — 문자열 {mc['string_values']} 중 분석 {mc['applied']} / 제외 {mc['excluded']} · 비문자열 말단 {mc['nonstring_leaves']} · 필드명 {mc['field_names']} · 토큰 {mc['tokens']:,} · 알려진 오분절 출현 {mc['known_segmentation_issues']} |")
    L.append(f"| 복합 표현 | [expressions.json](./expressions.json) — 전체 {ec['total']:,} (자동 정규식 {ec.get('auto_regex', 0):,} · 자동 절 {ec.get('auto_clause', 0):,} · 직접 읽기 수동 {ec.get('manual_direct_reading', 0):,}) · 자동 오탐 표시 {ec['auto_false_positive']} · 수식·부정 토큰 점검 {ec['modifier_tokens_checked']} (미검토 {ec['modifier_tokens_unreviewed']}) |")
    L.append("| 구획·범위 | [coverage.json](./coverage.json) · 진행 기록 [progress.md](./progress.md) |")
    L.append("| 미결 | [issues.md](./issues.md) |")
    L.append("| 검증 | [validation.md](./validation.md) · [verify.py](./verify.py) |")
    L.append("| 재현 | [build.py](./build.py) · 직접 읽기 기록 `manual/seg-00.json`~`seg-13.json` · 오분절 기록 `manual/segmentation-review.json` · 표현 검토 `manual/expression-review.json` · 전역 미결 `manual/global-issues.json` |")
    L.append("")
    L.append("구간 기준: source-map 의 `span` 은 파일 전체 디코딩 텍스트의 코드 포인트 `[start,end)`(문자열은 따옴표 포함), `value_span` 은 따옴표 제외. morphology·expressions 의 `start/end`·`span` 은 해당 값 문자열 기준. 바이트 구간은 `byte_span`. 이 원장은 이스케이프 0 이라 JSON 리터럴 내부와 디코딩 문자열이 같다(검증됨).")
    L.append("")
    L.append("## 1. 구획 목차와 읽기 상태")
    L.append("")
    L.append("| 구획 | 범위 | 소유 말단 | 기계 추출 | 직접 읽기 | 문서 |")
    L.append("|---|---|---|---|---|---|")
    for c in cov:
        L.append(f"| {c['segment']} | `{md(c['pointer_range'])}` ({md(c['title'])}) | {c['owned_leaf_count']} | {c['machine_extraction']} | {c['direct_reading']} | [{c['review_file']}](./{c['review_file']}{c['review_anchor']}) |")
    L.append("")
    L.append("읽기 방식: 각 구획을 원문 순서대로 화면에 펼쳐 전 필드·전 배열 원소를 직접 읽고, 읽은 즉시 `manual/seg-XX.json` 에 관찰·수동 구절·미결을 저장했다. 이후 형태소 토큰 전체와 자동 후보·미덮임 어절을 원문과 나란히 다시 대조했다([validation.md](./validation.md) §3). 같은 에이전트의 관점 바꾼 재읽기이며 독립 검토자가 아니다.")
    L.append("")
    L.append("## 2. 컬럼 구성 표 (자동 생성 — 원본 컬럼명·경로 패턴 그대로)")
    L.append("")
    L.append("배열 인덱스는 `*` 로 묶었다. 같은 패턴이라도 자료형·빈 값 변형은 따로 행을 둔다. 「존재 범위」 가 전체보다 작으면 선택적 필드다.")
    L.append("")
    L.append(column_table(nodes, by_ptr))
    L.append("")
    L.append("### 구조 관찰 (잠정 — 원문 칸과 분리)")
    L.append("")
    L.append("- 상위 8키: 스칼라 3(`version`·`updated`·`consensus_method`) + 배열 5(`optimization_principles` 문자열 4 · `by_concern` 객체 8 · `by_age_group` 객체 4 · `combination_rules` 객체 8 · `annual_plans` 객체 3).")
    L.append("- `by_concern/*/severity_levels` 는 모든 고민에서 길이 3(경미·중등도·중증 순). 단계 객체 8필드가 기본이고 `caveats` 는 `/by_concern/3/severity_levels/2` 에만 있다.")
    L.append("- `by_age_group` 의 `upgrade` 는 3/4, `note` 는 1/4 객체에만 있다. `annual_plans/*/schedule` 은 모두 12개월, `month` 는 정수 1~12 오름차순, `procedures` 길이 1~3.")
    L.append("- `contraindicated_combos` 빈 배열 `[]` 은 빈 값 변형 행으로 따로 셌다. 빈 문자열·null·빈 객체는 없다.")
    L.append("- 원장 안에서 서로 다른 블록이 같은 대상을 다른 표기로 부른다(예: 「HIFU(슈링크/울쎄라)」/「HIFU(울쎄라/슈링크)」/「울쎄라 HIFU」). 연결·병합은 하지 않았다(issues F).")
    L.append("")
    L.append("## 3. 형태소·표현 수집 범위 (자동과 직접의 구분)")
    L.append("")
    L.append("- 자동: 구조 열거·Pointer·구간, Kiwi 형태소 분석(분석 대상 전체 값), 정규식 후보(R01~R20 실제 일치분), 구두점 기준 절 분할, 수동 구절 위치 찾기, 수식·부정 토큰의 수동 표현 포괄 점검.")
    L.append("- 직접: 14구획 원문 통독과 관찰, 수동 구절 수집(패턴 밖 형용사·부사·회피/권고·깊이·속도·근사·수치단위·「후/시」 조건 포함), 토큰 전체 열람 후 오분절 출현 기록, 자동 후보 열람 후 오탐 표시, 수식·부정 토큰 중 수동 구절 밖 토큰의 개별 검토.")
    L.append("- 정규식 후보는 패턴 일치분뿐이다. 수동 구절은 직접 읽기에서 적은 것이며, 이 둘을 합쳐도 원문 전체의 의미 해석이 아니다. 대표 표현으로 모든 복합 표현을 덮었다고 주장하지 않는다 — 덮이지 않은 어절 목록은 expressions.json `uncovered_eojeol`.")
    L.append("- 다국어: 한국어 외 라틴(영어 약어·문헌명·원어 괄호)·한자(美·韓) 구간이 있다. Kiwi 는 이를 SL/SH 토큰으로만 나누며 영어 형태소·기본형은 없다(K-02). 원문은 그대로 보존했다.")
    L.append("")
    with open(os.path.join(OUT, "review.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def write_issues(manual, global_issues, expressions, morphology):
    allis = []
    for sid, m in manual.items():
        for it in m.get("issues", []):
            allis.append((sid, it))
        for o in m.get("observations", []):
            if o["status"] in ("F",):
                allis.append((sid, {"id": "F-" + o["id"], "class": "F", "pointers": o["pointers"], "text": o["text"]}))
    for it in global_issues.get("issues", []):
        allis.append(("전역", it))
    by_cls = defaultdict(list)
    for sid, it in allis:
        by_cls[it["class"]].append((sid, it))
    names = OrderedDict([("A", "에이전트 추출/해석 오류"), ("B", "원문 정보 부족"), ("C", "현재 사용자 결정 필요"),
                         ("I", "원문 내 불일치 후보"), ("K", "알려진 분석 한계"), ("P", "잠정"), ("F", "후속 의미 조사")])
    L = ["# treatment-optimization.json — 미결 기록", "",
         "> build.py 가 manual/seg-XX.json 의 issues·F 관찰과 manual/global-issues.json 에서 생성한다. 손으로 고치지 말고 manual 을 고친 뒤 재생성한다.",
         "> 기호: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · I=원문 내 불일치(후보) · K=알려진 분석 한계 · P=잠정 · F=후속 의미 조사. 원문 내 불일치를 C 로 부르지 않는다. 원본 변경 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 선택 대기로 올리지 않는다.", "",
         "## 요약", "", "| 기호 | 뜻 | 건수 | 처리 상태 |", "|---|---|---|---|"]
    status = {"A": "발견 즉시 수정·재검증(아래 목록은 수정 이력)", "B": "열림 — 원문에 정보가 없어 1차에서 닫을 수 없음. 사용자 추측으로 메우지 않음",
              "C": "0 — 아래 「사용자 결정 0의 근거」 참조", "I": "열림 — 판정하지 않고 위치만 기록. 원본 수정 제안은 후속 확인 후보",
              "K": "기록됨 — 한계로 남김(교정 안 함)", "P": "review-part 의 잠정 관찰 절에 있음", "F": "열림 — 전체 21개 비교 뒤 의미 조사 단계"}
    for c, nm in names.items():
        cnt = len(by_cls.get(c, []))
        if c == "P":
            cnt = sum(1 for m in manual.values() for o in m.get("observations", []) if o["status"] == "P")
        L.append(f"| {c} | {nm} | {cnt} | {status[c]} |")
    L.append("")
    for c in ["A", "K", "B", "I", "F"]:
        items = by_cls.get(c, [])
        L.append(f"## {c} — {names[c]} ({len(items)})")
        L.append("")
        if not items:
            L.append("- 없음")
        for sid, it in items:
            L.append(f"- **{it['id']}** ({sid}) {it['text']}")
            if it.get("pointers"):
                L.append(f"  - 위치: {', '.join('`' + p + '`' for p in it['pointers'])}")
            if it.get("impact"):
                L.append(f"  - 영향: {it['impact']}")
            if it.get("resolution"):
                L.append(f"  - 처리: {it['resolution']}")
            if it.get("note"):
                L.append(f"  - 비고: {it['note']}")
        L.append("")
    L.append("## C — 현재 사용자 결정 필요 (0)")
    L.append("")
    for line in global_issues.get("user_decision_zero_basis", []):
        L.append(f"- {line}")
    L.append("")
    with open(os.path.join(OUT, "issues.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
