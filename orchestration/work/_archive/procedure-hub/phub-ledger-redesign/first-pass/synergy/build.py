#!/usr/bin/env python3
"""synergy.json 1차 조사 — 재현 빌드.

실행(레포 루트):
  OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
    python orchestration/work/phub-ledger-redesign/first-pass/synergy/build.py

쓰는 파일은 이 스크립트가 있는 폴더 안의 source-map.json · morphology.json ·
expressions.json · link-observations.json · review.md · build-output.txt 뿐이다.
원본은 읽기만 한다(시작·끝 해시 비교).
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/synergy.json"
SRC = ROOT / SRC_REL

LINK_FIELDS = ["from", "from_category", "to", "to_category", "type", "reason", "timing", "target"]
READ_BLOCKS = [("B0", "top", None), ("B1", "links", (0, 29)), ("B2", "links", (30, 59)),
               ("B3", "links", (60, 89)), ("B4", "links", (90, 114))]

log_lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    log_lines.append(s)
    print(s)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def esc(p):
    return str(p).replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- parser
class Scanner:
    """위치를 기록하는 JSON 스캐너. 중복 키를 덮어쓰지 않고 기록한다."""

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.keys = []
        self.duplicate_keys = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def string_literal(self):
        t = self.t
        assert t[self.i] == '"', self.i
        j = self.i + 1
        while True:
            c = t[j]
            if c == "\\":
                j += 2
                continue
            if c == '"':
                break
            j += 1
        lit = t[self.i + 1:j]
        val = json.loads(t[self.i:j + 1])
        start = self.i
        self.i = j + 1
        return start, j + 1, lit, val

    def value(self, pointer, parent, key, index):
        self.ws()
        t = self.t
        c = t[self.i]
        node = {"pointer": pointer, "parent": parent, "key": key, "index": index}
        self.nodes.append(node)
        if c == "{":
            start = self.i
            self.i += 1
            node["type"] = "object"
            children = []
            seen = Counter()
            self.ws()
            if t[self.i] == "}":
                self.i += 1
            else:
                order = 0
                while True:
                    self.ws()
                    ks, ke, klit, k = self.string_literal()
                    seen[k] += 1
                    cp = pointer + "/" + esc(k)
                    if seen[k] > 1:
                        self.duplicate_keys.append({"object_pointer": pointer, "key": k, "occurrence": seen[k], "key_span": [ks, ke]})
                        cp = cp + f"#dup{seen[k]}"
                    self.keys.append({"key": k, "object_pointer": pointer, "value_pointer": cp, "order": order,
                                      "key_span": [ks, ke], "key_has_escape": "\\" in klit})
                    order += 1
                    children.append(k)
                    self.ws()
                    assert t[self.i] == ":"
                    self.i += 1
                    self.value(cp, pointer, k, None)
                    self.ws()
                    if t[self.i] == ",":
                        self.i += 1
                        continue
                    assert t[self.i] == "}"
                    self.i += 1
                    break
            node["children"] = children
            node["length"] = len(children)
            node["span"] = [start, self.i]
        elif c == "[":
            start = self.i
            self.i += 1
            node["type"] = "array"
            n = 0
            self.ws()
            if t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(pointer + "/" + str(n), pointer, None, n)
                    n += 1
                    self.ws()
                    if t[self.i] == ",":
                        self.i += 1
                        continue
                    assert t[self.i] == "]"
                    self.i += 1
                    break
            node["length"] = n
            node["span"] = [start, self.i]
        elif c == '"':
            s, e, lit, val = self.string_literal()
            node.update({"type": "string", "span": [s, e], "literal_span": [s + 1, e - 1], "value": val,
                         "has_escape": "\\" in lit, "empty": val == ""})
        else:
            m = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(t, self.i)
            assert m, self.i
            lit = m.group(0)
            v = json.loads(lit)
            node.update({"type": "null" if v is None else "boolean" if isinstance(v, bool) else "number",
                         "span": [m.start(), m.end()], "value": v})
            self.i = m.end()
        return node


def link_index_of(pointer):
    m = re.match(r"^/links/(\d+)(?:/|$)", pointer)
    return int(m.group(1)) if m else None


def block_of(li):
    if li is None:
        return "B0"
    for b, _, r in READ_BLOCKS:
        if r and r[0] <= li <= r[1]:
            return b
    raise ValueError(li)


def context_for(pointer):
    li = link_index_of(pointer)
    ctx = {"read_block": block_of(li), "link_index": li}
    if li is not None:
        ctx["link_pointer"] = f"/links/{li}"
        m = re.match(r"^/links/\d+/(.+)$", pointer)
        if m:
            ctx["field"] = m.group(1)
            ctx["sibling_pointers"] = [f"/links/{li}/{f}" for f in LINK_FIELDS if f != m.group(1)]
    return ctx


def pattern_of(pointer):
    return re.sub(r"/\d+(?=/|$)", "/*", pointer)


# ---------------------------------------------------------------- main
def main():
    raw = SRC.read_bytes()
    h_start = sha256(raw)
    text = raw.decode("utf-8")
    bom = text.startswith("﻿")
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + len(ch.encode("utf-8")))
    assert cum[-1] == len(raw)

    sc = Scanner(text)
    root = sc.value("", None, None, None)
    sc.ws()
    assert sc.i == len(text), "trailing data"

    for n in sc.nodes:
        n["byte_span"] = [cum[n["span"][0]], cum[n["span"][1]]]
        if n["type"] == "string":
            n["literal_byte_span"] = [cum[n["literal_span"][0]], cum[n["literal_span"][1]]]
        n["pattern"] = pattern_of(n["pointer"])
        n["context"] = context_for(n["pointer"])
    for k in sc.keys:
        k["key_byte_span"] = [cum[k["key_span"][0]], cum[k["key_span"][1]]]
        k["context"] = context_for(k["value_pointer"])

    field_occ = defaultdict(lambda: defaultdict(list))
    for k in sc.keys:
        field_occ[k["key"]][pattern_of(k["value_pointer"])].append(k["value_pointer"])

    source_info = {
        "path": SRC_REL,
        "size_bytes": len(raw),
        "code_points": len(text),
        "sha256_start": h_start,
        "encoding": "utf-8" + (", BOM 있음" if bom else ", BOM 없음") + (", 개행 없음(한 줄)" if "\n" not in text else ""),
        "escape_count_in_string_literals": sum(1 for n in sc.nodes if n["type"] == "string" and n["has_escape"]),
        "non_bmp_chars": sum(1 for ch in text if ord(ch) > 0xFFFF),
        "offset_unit": "디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end). byte_span 은 UTF-8 바이트 [start,end)",
    }

    type_counts = Counter(n["type"] for n in sc.nodes)
    source_map = {
        "source": source_info,
        "notes": [
            "span: 파일 전체 텍스트 기준 코드 포인트 [start,end). 문자열 노드의 span 은 따옴표 포함 JSON 리터럴 구간, literal_span 은 따옴표 제외 구간.",
            "has_escape=false 이면 literal_span 원문 slice == 디코딩 value. 이 원장은 이스케이프 0건이다(source.escape_count_in_string_literals).",
            "context.read_block 은 직접 읽기 구획(B0 상위, B1 links 0–29, B2 30–59, B3 60–89, B4 90–114). sibling_pointers 는 같은 link 안에서 함께 해석할 다른 7개 필드.",
            "이 기록은 구조적 사실(키·순서·계층·값)만 담는다. from/to/type 등의 의미적 정합은 승인하지 않는다.",
        ],
        "counts": {"nodes": len(sc.nodes), "by_type": dict(type_counts), "key_occurrences": len(sc.keys),
                   "distinct_keys": len(field_occ)},
        "duplicate_keys": sc.duplicate_keys,
        "field_name_occurrences": {k: dict(v) for k, v in sorted(field_occ.items())},
        "keys": sc.keys,
        "nodes": sc.nodes,
    }

    data = json.loads(text)
    links = data["links"]
    strings = [n for n in sc.nodes if n["type"] == "string"]

    # ---------------------------------------------------------------- morphology
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi(num_workers=1, model_type="cong")

    POLICY = [
        {"pattern": "/version", "action": "exclude", "reason": "버전 표기 문자열(숫자·점). 언어 텍스트 아님"},
        {"pattern": "/updated", "action": "exclude", "reason": "ISO 날짜 문자열(YYYY-MM-DD). 언어 텍스트 아님"},
        {"pattern": "/links/*/from_category", "action": "exclude", "reason": "분류 코드값(M+숫자). 언어 텍스트 아님", "value_regex": r"^M\d+$"},
        {"pattern": "/links/*/to_category", "action": "exclude", "reason": "분류 코드값(M+숫자). 언어 텍스트 아님", "value_regex": r"^M\d+$"},
        {"pattern": "/links/*/from", "action": "apply", "role": "명칭 문자열(한국어·영문 혼합, 일부는 'Mxx-' 코드 접두 포함). 접두 부분은 SR14 로 출현별 표시"},
        {"pattern": "/links/*/to", "action": "apply", "role": "명칭 문자열(위와 같음)"},
        {"pattern": "/links/*/type", "action": "apply", "role": "관계 유형 값(한국어 단어 3종: 함께·다음에·대신)"},
        {"pattern": "/links/*/reason", "action": "apply", "role": "서술 문장"},
        {"pattern": "/links/*/timing", "action": "apply", "role": "시점·간격·조건 서술"},
        {"pattern": "/links/*/target", "action": "apply", "role": "목적·분야 라벨(일부 '/' 포함)"},
    ]
    pol = {p["pattern"]: p for p in POLICY}

    values, excluded = [], []
    for n in strings:
        p = pol.get(n["pattern"])
        if p is None:
            raise SystemExit(f"policy missing for {n['pattern']}")
        if p["action"] == "exclude":
            if "value_regex" in p and not re.match(p["value_regex"], n["value"]):
                raise SystemExit(f"exclude regex mismatch {n['pointer']} {n['value']}")
            excluded.append({"pointer": n["pointer"], "value": n["value"], "reason": p["reason"], "context": n["context"]})
            continue
        toks = kiwi.tokenize(n["value"])
        tl = []
        for ti, tk in enumerate(toks):
            s, e = tk.start, tk.start + tk.len
            tl.append({"i": ti, "form": tk.form, "tag": str(tk.tag), "lemma": tk.lemma, "span": [s, e],
                       "surface": n["value"][s:e], "form_equals_surface": tk.form == n["value"][s:e], "zero_length": s == e})
        values.append({"source": "value", "pointer": n["pointer"], "field": n["key"], "text": n["value"],
                       "file_span_of_text": n["literal_span"], "context": n["context"], "tokens": tl})

    field_names = []
    for k in sorted(field_occ):
        toks = kiwi.tokenize(k)
        field_names.append({"source": "field_name", "field_name": k, "occurrence_patterns": sorted(field_occ[k]),
                            "occurrence_count": sum(len(v) for v in field_occ[k].values()),
                            "tokens": [{"form": t.form, "tag": str(t.tag), "lemma": t.lemma, "span": [t.start, t.start + t.len],
                                        "surface": k[t.start:t.start + t.len]} for t in toks],
                            "identifier_parts_rule_based": k.split("_")})

    # segmentation review (phrase rules)
    rules = json.loads((OUT / "segmentation-review-rules.json").read_text(encoding="utf-8"))["rules"]

    def tok_match(actual, pattern):
        out = []
        for a, p in zip(actual, pattern):
            pf, pt = p.rsplit("/", 1)
            if pt != a["tag"] or (pf != "*" and pf != a["form"]):
                return False
            out.append(True)
        return len(actual) == len(pattern)

    seg_review, seg_unmatched = [], []
    rule_counts = Counter()
    for r in rules:
        rx = re.compile(r["regex"]) if "regex" in r else re.compile(re.escape(r["phrase"]))
        for v in values:
            for m in rx.finditer(v["text"]):
                s, e = m.span()
                ov = [t for t in v["tokens"] if t["span"][0] < e and t["span"][1] > s]
                verdict = None
                for var in r["variants"]:
                    if tok_match(ov, var["tokens"]):
                        verdict = var
                        break
                rec = {"rule": r["id"], "kind": r["kind"], "pointer": v["pointer"], "phrase": v["text"][s:e], "phrase_span": [s, e],
                       "tokens": [[t["form"], t["tag"], t["span"], t["i"]] for t in ov]}
                if verdict is None:
                    seg_unmatched.append(rec)
                    continue
                rec["verdict"] = verdict["verdict"]
                if verdict["verdict"] == "issue":
                    rec["issue"] = verdict["issue"]
                    rec["impact"] = verdict["impact"]
                    rec["status"] = "표시됨(교정 아님) — 원시 Kiwi 토큰 유지"
                else:
                    rec["status"] = "해당 출현 직접 확인: 문제 없음"
                rule_counts[(r["id"], verdict["verdict"])] += 1
                seg_review.append(rec)
    if seg_unmatched:
        for u in seg_unmatched:
            log("UNMATCHED", json.dumps(u, ensure_ascii=False))
        raise SystemExit("segmentation rule variants do not cover all occurrences")

    # POS review: 수식·부정·수량 관련 품사의 모든 출현을 서명별로 판정
    pos_rules = json.loads((OUT / "pos-review-rules.json").read_text(encoding="utf-8"))
    REVIEW_TAGS = set(pos_rules["review_tags"])
    sig = {(x["form"], x["tag"]): x for x in pos_rules["signatures"]}
    pos_review, pos_unmatched = [], []
    for v in values:
        for t in v["tokens"]:
            if t["tag"] not in REVIEW_TAGS:
                continue
            x = sig.get((t["form"], t["tag"]))
            rec = {"pointer": v["pointer"], "token_index": t["i"], "form": t["form"], "tag": t["tag"], "span": t["span"],
                   "context_window": v["text"][max(0, t["span"][0] - 8):t["span"][1] + 8]}
            if x is None:
                pos_unmatched.append(rec)
                continue
            verdict = x["verdict"]
            note = x.get("note")
            for ex in x.get("exceptions", []):
                if ex["pointer"] == v["pointer"] and ex["span"] == t["span"]:
                    verdict, note = ex["verdict"], ex["note"]
            rec.update({"verdict": verdict, "note": note})
            pos_review.append(rec)
    if pos_unmatched:
        for u in pos_unmatched:
            log("POS-UNMATCHED", json.dumps(u, ensure_ascii=False))
        raise SystemExit("pos-review signatures do not cover all occurrences")

    tok_total = sum(len(v["tokens"]) for v in values)
    morphology = {
        "source": source_info,
        "analyzer": {
            "name": "Kiwi (kiwipiepy)", "kiwipiepy": kiwipiepy.__version__, "model_type": "cong", "num_workers": 1,
            "env": "uv run --python 3.12 --with kiwipiepy==0.24.1, OMP_NUM_THREADS=1",
            "tokenize_kwargs": "기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, blocklist=None, compatible_jamo=False, split_sents=False, typos=None)",
            "user_dictionary": "없음(기본 내장 사전만)",
            "tagset": "Kiwi 품사 체계(세종 기반 확장: NNG/NNP/NNB/NR/NP/VV/VA/VX/VCP/VCN/MM/MAG/MAJ/J*/E*/X*/S*)",
            "lemma": "Kiwi Token.lemma 값 그대로(용언은 Kiwi 가 '다'를 붙인 기본형). 도메인 표준명 아님. 분석기가 주지 않는 기본형은 만들지 않았다",
            "span": "각 값 문자열 기준 코드 포인트 [start,end). 파일 기준 = file_span_of_text[0] + start. 축약·불규칙 활용은 여러 형태소가 같은 표면 구간을 공유(form_equals_surface=false). 표면에 없는 형태소를 Kiwi 가 복원한 경우 길이 0 구간 [k,k] 이며 zero_length=true·surface=''(이 원장에서는 VCP '이' 7출현)",
        },
        "policy": POLICY,
        "counts": {"values_analyzed": len(values), "values_excluded": len(excluded), "tokens": tok_total,
                   "field_names": len(field_names), "segmentation_review": len(seg_review),
                   "segmentation_issue": sum(1 for r in seg_review if r["verdict"] == "issue"),
                   "segmentation_ok": sum(1 for r in seg_review if r["verdict"] == "ok"),
                   "pos_review": len(pos_review),
                   "pos_review_issue": sum(1 for r in pos_review if r["verdict"] == "issue")},
        "excluded_values": excluded,
        "values": values,
        "field_names": field_names,
        "field_name_note": "필드명은 영문 snake_case 식별자다. Kiwi 결과(SL)는 보존하되 언어 텍스트와 역할이 다르다. '_' 기준 분해는 규칙 기반(identifier_parts_rule_based)이며 분석기 산출이 아니다.",
        "segmentation_review_note": "segmentation-review-rules.json 의 구절 규칙을 모든 출현에 적용한 결과. 원시 토큰은 교정하지 않았다. 규칙 밖 토큰의 정확성은 보장하지 않는다(NNP/NNG 구분, VA/VV 구분 등은 출현별로 판정하지 않음).",
        "segmentation_review": seg_review,
        "pos_review_note": "pos-review-rules.json 의 review_tags 에 해당하는 모든 토큰 출현을 (form,tag) 서명으로 판정. 판정은 수식·부정·수량·범위 신호로서의 쓸모를 본 것이며 교정 아님.",
        "pos_review": pos_review,
    }

    # ---------------------------------------------------------------- expressions
    exprs = []

    def add(v, s, e, cat, method, source):
        exprs.append({"pointer": v["pointer"], "field": v["field"], "span": [s, e], "text": v["text"][s:e],
                      "category_candidate": cat, "method": method, "source": source,
                      "context": {"link_index": v["context"].get("link_index"), "read_block": v["context"]["read_block"]}})

    RULES = [
        ("quantity_time", "regex", r"\d+(?:~\d+)?\s*(?:주|개월|일|종)(?:\s*(?:후|뒤|간격))?"),
        ("quantity_time", "regex", r"택 ?1"),
        ("time_reference", "keyword", r"같은 날|직후|순차|단계별|순서"),
        ("sequence_marker", "regex", r"(?<![가-힣])(?:후|뒤)(?=\s|$|,)|먼저|→|이어가면|(?<=[ㄴ-힣]) 뒤(?=\s)"),
        ("negation", "regex", r"\S*지 않\S*|불가\S*|아니라|아닌|미허가|않음"),
        ("possibility_hedge", "regex", r"\S+ 수 있\S*|소지가 있\S*|제한적\S*|가능\S*|상이\S*|주로|보조적|입증되지|고려할 수|확립된"),
        ("condition_scope", "regex", r"에 한해|에 한정\S*|에 따라|해당 시|경우|할 때는|\S+만(?=\s)|모두|둘 다|등(?=\s)"),
        ("condition_connective", "regex", r"\S+(?:하면|으면|당기면|하면서)(?=\s|$)"),
        ("degree_intensity", "regex", r"극대화|배가|상승|가속|촉진|오래|빠르\S*|빠른|빠름|점차|과도한|선택적으로|한번에|동시\S*|이중|더블|바로|직접|전체적으로|더(?=\s)|비슷\S*|자연스러\S*|자연스럽게|단단하게|탄탄한|매끈한|타이트하게|깊이"),
        ("depth_layer", "regex", r"깊은 층|얕은 층|전체 층|전층|전 층|목표 층|깊은|얕은|표피|진피 표면|진피|표면|겉면|심부|SMAS|피부 속|흉터 아래"),
        ("region_candidate", "regex", r"(?<![가-힣A-Za-z])(?:바디라인|사각턱|턱끝|코끝|콧대|코 라인|V라인|얼굴윤곽|얼굴|두피|모낭|몸매|바디|턱|코)"),
        ("material_annotation", "regex", r"\S+\([^)]+\)"),
        ("symbol_operator", "regex", r"\+|=|→|·|/|~|(?<![A-Za-z])vs(?![A-Za-z])"),
        ("selection_criterion", "regex", r"\S+ (?:차이로|따라) 선택\S*|선택이 달라짐|선택 가능|교체 가능|대체 가능|대체재|\S*대안|택 ?1|\S+로 선택"),
        ("evidence_regulatory", "regex", r"임상\S*|검증\S*|근거\S*|입증\S*|미허가|위법|허가된|심의|승인|첨단재생의료|화장품\S*|표준"),
        ("risk_event", "regex", r"감염|이물육아종|(?<!이물)육아종|위험"),
        ("alternative_connective", "regex", r"또는|\S+이나(?=\s)|\S+거나(?=\s)"),
        ("state_appearance_modifier", "regex", r"꺼진|처진|묵은|손상된|맑은|맑고|촉촉하게|화사하고|어려 보이는|세련된|입체적|갸름한|건강한|좋게|(?<![가-힣])빈(?=\s)|미세한|미세(?=\s|구멍|채널)|전반적|물리적|근육성|표정 주름|데일리"),
        ("origin_modifier", "regex", r"(?<![가-힣])자가\S*|배양\S*|유래|연어DNA"),
        ("comparison", "regex", r"서로 다른|(?<![가-힣])다른(?=\s)|원조|후발"),
        ("name_candidate", "regex", r"(?<![가-힣])실(?=로\s)"),
    ]
    NAME_KEYWORDS = sorted(set(json.loads((OUT / "name-keywords.json").read_text(encoding="utf-8"))["keywords"]), key=lambda s: (-len(s), s))

    for v in values:
        add(v, 0, len(v["text"]), "segment.value", "값 전체", "whole")
        if v["field"] == "reason":
            for m in re.finditer(r"[^.]+(?:\.|$)", v["text"]):
                s, e = m.span()
                while s < e and v["text"][s] == " ":
                    s += 1
                if e > s:
                    add(v, s, e, "segment.sentence", "regex 문장분할: '.' 기준", "regex")
            for m in re.finditer(r"[^,+=→]+", v["text"]):
                s, e = m.span()
                while s < e and v["text"][s] == " ":
                    s += 1
                while e > s and v["text"][e - 1] == " ":
                    e -= 1
                if e > s and (e - s) < len(v["text"]):
                    add(v, s, e, "segment.operator_part", "regex 분할: ',' '+' '=' '→' 기준", "regex")
        for cat, method, pat in RULES:
            for m in re.finditer(pat, v["text"]):
                if m.end() > m.start():
                    add(v, m.start(), m.end(), cat, f"{method}: {pat}", method)
        for kw in NAME_KEYWORDS:
            for m in re.finditer(re.escape(kw), v["text"]):
                add(v, m.start(), m.end(), "name_candidate", "keyword(수동 명칭 목록 name-keywords.json 부분문자열)", "keyword")

    # manual
    manual = json.loads((OUT / "manual-expressions.json").read_text(encoding="utf-8"))
    vmap = {v["pointer"]: v for v in values}
    for me in manual["expressions"]:
        v = vmap[me["pointer"]]
        occ = [m.start() for m in re.finditer(re.escape(me["text"]), v["text"])]
        k = me.get("occurrence", 0)
        if not occ or k >= len(occ):
            raise SystemExit(f"manual expression not found: {me}")
        s = occ[k]
        exprs.append({"pointer": v["pointer"], "field": v["field"], "span": [s, s + len(me["text"])], "text": me["text"],
                      "category_candidate": me["category_candidate"], "method": "manual(원문 직접 읽기에서 지정)", "source": "manual",
                      "note": me.get("note"), "context": {"link_index": v["context"].get("link_index"), "read_block": v["context"]["read_block"]}})

    # 오탐 표시: 형태소·문맥 검토로 확인한 후보 오탐
    fp = json.loads((OUT / "expression-review.json").read_text(encoding="utf-8"))["false_positives"]
    fpi = {(f["pointer"], tuple(f["span"]), f["category_candidate"]): f for f in fp}
    used = set()
    for i, x in enumerate(exprs):
        x["id"] = f"E{i:05d}"
        key = (x["pointer"], tuple(x["span"]), x["category_candidate"])
        if key in fpi:
            x["review"] = {"verdict": "false_positive", "note": fpi[key]["note"]}
            used.add(key)
    missing_fp = set(fpi) - used
    if missing_fp:
        raise SystemExit(f"expression-review entries not matched: {missing_fp}")

    # dup check
    dk = Counter((x["pointer"], tuple(x["span"]), x["category_candidate"], x["method"]) for x in exprs)
    dups = [k for k, c in dk.items() if c > 1]
    if dups:
        raise SystemExit(f"duplicate expressions: {dups[:5]}")

    cat_counts = Counter(x["category_candidate"] for x in exprs)
    expressions = {
        "source": source_info,
        "method": {
            "note": "범주는 탐색 관점의 후보 표시이며 확정 분류가 아니다. regex·keyword·수동목록 결과를 전수 의미 해석으로 쓰지 않는다. 같은 구간이 여러 범주에 겹치는 것은 의도된 겹침이다(같은 pointer·span·category·method 중복은 0으로 검사).",
            "rules": [{"category_candidate": c, "method": m, "pattern": p} for c, m, p in RULES]
                     + [{"category_candidate": "segment.value", "method": "값 전체", "pattern": None},
                        {"category_candidate": "segment.sentence", "method": "regex 문장분할('.')", "pattern": r"[^.]+(?:\.|$)"},
                        {"category_candidate": "segment.operator_part", "method": "regex 분할(',' '+' '=' '→')", "pattern": r"[^,+=→]+"},
                        {"category_candidate": "name_candidate", "method": "keyword", "pattern": "name-keywords.json"},
                        {"category_candidate": "(manual)", "method": "manual-expressions.json", "pattern": None}],
            "span": "값 문자열 기준 코드 포인트 [start,end)",
            "false_positive_review": "expression-review.json 에 출현별로 적은 후보 오탐은 삭제하지 않고 review.verdict=false_positive 로 표시",
        },
        "counts": {"total": len(exprs), "by_category": dict(sorted(cat_counts.items())),
                   "false_positive_marked": sum(1 for x in exprs if "review" in x)},
        "expressions": exprs,
    }

    # ---------------------------------------------------------------- link observations (computed + manual)
    obs = []
    pairs = defaultdict(list)
    for i, l in enumerate(links):
        pairs[frozenset([l["from"], l["to"]])].append(i)
    for k, idx in pairs.items():
        if len(idx) > 1:
            kinds = [(links[i]["from"], links[i]["type"], links[i]["to"]) for i in idx]
            same_dir = len({(a, c) for a, _, c in kinds}) == 1
            obs.append({"kind": "same-endpoint-pair-multiple-links", "computed": True,
                        "pointers": [f"/links/{i}" for i in idx],
                        "quote": [x for t in kinds for x in t],
                        "observation": ("같은 방향" if same_dir else "방향이 반대인 출현 포함") + "; type 값: " + "·".join(b for _, b, _ in kinds),
                        "status": "잠정 관찰(중복·역방향·관계 차이 여부는 후속 의미 조사)"})
    prefixed = []
    for i, l in enumerate(links):
        for f in ("from", "to"):
            m = re.match(r"^(M\d+)-", l[f])
            if m:
                prefixed.append(f"/links/{i}/{f}")
                if m.group(1) != l[f + "_category"]:
                    obs.append({"kind": "prefix-category-mismatch", "computed": True, "pointers": [f"/links/{i}/{f}", f"/links/{i}/{f}_category"],
                                "quote": [l[f], l[f + "_category"]], "observation": "접두 코드와 category 값 불일치", "status": "구조적 사실"})
    obs.append({"kind": "prefix-in-name", "computed": True, "pointers": prefixed, "quote": ["Mxx-"],
                "observation": f"from/to {len(prefixed)}/230 출현이 'Mxx-' 접두를 갖는다. 접두 코드는 모두 같은 link 의 *_category 값과 같다. README 작성 규칙('Mxx- 접두 금지')과 다르다",
                "status": "구조적 사실 + 규칙 대조. README 규칙의 적용 시점·대상은 원문만으로 확정 불가(후속)"})
    mobs = json.loads((OUT / "manual-link-observations.json").read_text(encoding="utf-8"))["observations"]
    for o in mobs:
        o = dict(o)
        o["computed"] = False
        obs.append(o)
    link_observations = {"source": source_info, "note": "link 단위(여러 필드에 걸친) 관찰. computed=true 는 build.py 계산, false 는 원문 직접 읽기에서 적은 것(manual-link-observations.json). 모두 잠정이며 관계·의미를 확정하지 않는다. quote 는 원문 그대로의 값 또는 그 부분문자열이다.", "observations": obs}

    # ---------------------------------------------------------------- write
    def dump(name, obj):
        (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    h_end = sha256(SRC.read_bytes())
    for o in (source_map, morphology, expressions, link_observations):
        o["source"]["sha256_end"] = h_end
    dump("source-map.json", source_map)
    dump("morphology.json", morphology)
    dump("expressions.json", expressions)
    dump("link-observations.json", link_observations)

    # review.md
    tpl = (OUT / "review-template.md").read_text(encoding="utf-8")
    tpl = tpl.replace("{{LINK_VALUES}}", render_links(links))
    tpl = tpl.replace("{{STATS}}", render_stats(source_map, morphology, expressions, link_observations))
    (OUT / "review.md").write_text(tpl, encoding="utf-8")

    log("sha256_start", h_start)
    log("sha256_end  ", h_end)
    log("nodes", len(sc.nodes), dict(type_counts), "keys", len(sc.keys), "dup_keys", len(sc.duplicate_keys))
    log("values_analyzed", len(values), "excluded", len(excluded), "tokens", tok_total, "field_names", len(field_names))
    log("seg_review", len(seg_review), dict(sorted((f"{a}:{b}", c) for (a, b), c in rule_counts.items())))
    log("pos_review", len(pos_review), Counter(r["verdict"] for r in pos_review))
    log("expressions", len(exprs), dict(sorted(cat_counts.items())))
    log("false_positive_marked", expressions["counts"]["false_positive_marked"])
    log("link_observations", len(obs))
    (OUT / "build-output.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    if h_start != h_end:
        raise SystemExit("SOURCE CHANGED")


def md(s):
    return str(s).replace("|", "\\|")


def render_links(links):
    out = []
    for b, kind, r in READ_BLOCKS:
        if r is None:
            continue
        out.append(f"\n### {b} — `/links/{r[0]}` ~ `/links/{r[1]}`\n")
        out.append("| # | from | from_category | to | to_category | type | timing | target |")
        out.append("|---|---|---|---|---|---|---|---|")
        for i in range(r[0], r[1] + 1):
            l = links[i]
            out.append(f"| `/links/{i}` | {md(l['from'])} | {l['from_category']} | {md(l['to'])} | {l['to_category']} | {l['type']} | {md(l['timing'])} | {md(l['target'])} |")
        out.append("")
        out.append("| # | reason (원문 그대로) |")
        out.append("|---|---|")
        for i in range(r[0], r[1] + 1):
            out.append(f"| `/links/{i}/reason` | {md(links[i]['reason'])} |")
    return "\n".join(out)


def render_stats(sm, mo, ex, lo):
    c = mo["counts"]
    return "\n".join([
        f"- 노드 {sm['counts']['nodes']}개 {sm['counts']['by_type']} · 키 출현 {sm['counts']['key_occurrences']} · 고유 키 {sm['counts']['distinct_keys']} · 중복 키 {len(sm['duplicate_keys'])}",
        f"- 형태소: 분석 값 {c['values_analyzed']} · 제외 {c['values_excluded']} · 토큰 {c['tokens']} · 필드명 {c['field_names']} · 구절 규칙 판정 {c['segmentation_review']}(issue {c['segmentation_issue']} / ok {c['segmentation_ok']}) · 품사 출현 판정 {c['pos_review']}(issue {c['pos_review_issue']})",
        f"- 표현 후보 {ex['counts']['total']} · 오탐 표시 {ex['counts']['false_positive_marked']}",
        f"- link 관찰 {len(lo['observations'])}건(계산 {sum(1 for o in lo['observations'] if o['computed'])} · 직접 {sum(1 for o in lo['observations'] if not o['computed'])})",
    ])


if __name__ == "__main__":
    main()
