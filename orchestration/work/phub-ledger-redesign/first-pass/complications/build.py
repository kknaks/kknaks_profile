#!/usr/bin/env python3
"""complications.json 1차 조사 — 재현 빌드.

레포 루트에서:
  uv run --python 3.12 --with kiwipiepy==0.24.1 python \
    orchestration/work/phub-ledger-redesign/first-pass/complications/build.py

원본은 읽기만 한다. 쓰는 곳은 이 파일이 있는 폴더뿐이다.
입력(수동 기록): manual-expressions.json · manual-observations.json ·
segmentation-review.json · review-template.md
출력: source-map.json · morphology.json · expressions.json · review.md · build-output.txt
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/complications.json"
SRC = REPO / SRC_REL

OFFSET_UNIT = ("디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end) — 시작 포함·끝 제외. "
               "byte_span 은 원본 파일 UTF-8 바이트 [start,end). 이 파일은 BMP 밖 문자가 없어 "
               "코드 포인트 = UTF-16 코드 단위(Kiwi 오프셋 단위)와 같다(빌드가 검사).")

LOG = []


def log(*a):
    line = " ".join(str(x) for x in a)
    LOG.append(line)
    print(line)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- 1. JSON 스캐너
class Scanner:
    """원문 위치를 보존하는 JSON 파서. 중복 키를 덮어쓰지 않고 기록한다."""

    WS = " \t\n\r"

    def __init__(self, text):
        self.s = text
        self.nodes = []
        self.keys = []
        self.duplicate_keys = []
        self.escapes = []

    def ws(self, i):
        while i < len(self.s) and self.s[i] in self.WS:
            i += 1
        return i

    def parse(self):
        i = self.ws(0)
        i = self.value(i, "", None, None)
        i = self.ws(i)
        if i != len(self.s):
            raise ValueError(f"trailing data at {i}")

    def string(self, i):
        assert self.s[i] == '"'
        j = i + 1
        out = []
        while True:
            c = self.s[j]
            if c == '"':
                return j + 1, "".join(out)
            if c == "\\":
                e = self.s[j + 1]
                simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                          "n": "\n", "r": "\r", "t": "\t"}
                if e in simple:
                    out.append(simple[e])
                    self.escapes.append([j, j + 2])
                    j += 2
                    continue
                if e == "u":
                    cp = int(self.s[j + 2:j + 6], 16)
                    self.escapes.append([j, j + 6])
                    j += 6
                    if 0xD800 <= cp < 0xDC00 and self.s[j:j + 2] == "\\u":
                        lo = int(self.s[j + 2:j + 6], 16)
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)
                        self.escapes.append([j, j + 6])
                        j += 6
                    out.append(chr(cp))
                    continue
                raise ValueError(f"bad escape at {j}")
            if ord(c) < 0x20:
                raise ValueError(f"control char at {j}")
            out.append(c)
            j += 1

    def value(self, i, ptr, parent, key):
        c = self.s[i]
        node = {"pointer": ptr, "parent": parent, "key": key}
        self.nodes.append(node)
        if c == "{":
            node["type"] = "object"
            children, seen = [], set()
            j = self.ws(i + 1)
            if self.s[j] == "}":
                j += 1
            else:
                order = 0
                while True:
                    ks = j
                    j, k = self.string(j)
                    kptr = ptr + "/" + k.replace("~", "~0").replace("/", "~1")
                    dup = k in seen
                    rec = {"key": k, "object_pointer": ptr, "value_pointer": kptr,
                           "span": [ks, j], "order_in_object": order, "duplicate": dup}
                    self.keys.append(rec)
                    if dup:
                        self.duplicate_keys.append(rec)
                        kptr = kptr + f"#dup{order}"
                    seen.add(k)
                    children.append(k)
                    j = self.ws(j)
                    assert self.s[j] == ":"
                    j = self.ws(j + 1)
                    j = self.value(j, kptr, ptr, k)
                    j = self.ws(j)
                    order += 1
                    if self.s[j] == ",":
                        j = self.ws(j + 1)
                        continue
                    assert self.s[j] == "}"
                    j += 1
                    break
            node["children"] = children
            node["length"] = len(children)
        elif c == "[":
            node["type"] = "array"
            j = self.ws(i + 1)
            n = 0
            if self.s[j] == "]":
                j += 1
            else:
                while True:
                    j = self.value(j, f"{ptr}/{n}", ptr, n)
                    n += 1
                    j = self.ws(j)
                    if self.s[j] == ",":
                        j = self.ws(j + 1)
                        continue
                    assert self.s[j] == "]"
                    j += 1
                    break
            node["length"] = n
        elif c == '"':
            node["type"] = "string"
            j, v = self.string(i)
            node["value"] = v
            node["value_span"] = [i + 1, j - 1]
        else:
            m = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(self.s, i)
            if not m:
                raise ValueError(f"bad value at {i}")
            lit = m.group(0)
            j = m.end()
            if lit in ("true", "false"):
                node["type"], node["value"] = "boolean", lit == "true"
            elif lit == "null":
                node["type"], node["value"] = "null", None
            else:
                node["type"] = "number"
                node["value"] = json.loads(lit)
        node["span"] = [i, j]
        node["literal"] = self.s[i:j] if node["type"] not in ("object", "array") else None
        return j


def context_of(ptr, data):
    parts = ptr.split("/")[1:]
    ctx = {"block": None, "category_index": None, "category_id": None, "category_name": None,
           "complication_index": None, "complication_name": None, "field": None}
    if not parts:
        ctx["block"] = "top"
        return ctx
    if parts[0] == "severity_levels":
        ctx["block"] = "severity_levels"
        ctx["field"] = parts[1] if len(parts) > 1 else None
        return ctx
    ctx["block"] = "categories"
    if len(parts) >= 2:
        ci = int(parts[1])
        cat = data["categories"][ci]
        ctx.update(category_index=ci, category_id=cat["id"], category_name=cat["name"])
        if len(parts) >= 3:
            ctx["field"] = parts[2]
        if len(parts) >= 4 and parts[2] == "complications":
            mi = int(parts[3])
            ctx["complication_index"] = mi
            ctx["complication_name"] = cat["complications"][mi]["name"]
            ctx["field"] = parts[4] if len(parts) >= 5 else None
    return ctx


# ---------------------------------------------------------------- 2. 형태소 적용·제외
URL_RE = re.compile(r"(?:https?://\S+|(?:[a-z0-9-]+\.)+(?:com|org|net|gov|xyz|io)/\S*)")
SEP_RE = re.compile(r"; ")


def url_subspans(v):
    out = []
    for m in URL_RE.finditer(v):
        e = m.end()
        while e > m.start() and (v[e - 1] in ";," or (v[e - 1] == ")" and "(" not in v[m.start():e])):
            e -= 1
        out.append([m.start(), e])
    return out


def classify(ptr, v):
    """('analyze'|'exclude', reason, url_subspans)"""
    if re.fullmatch(r"/categories/\d+/id", ptr):
        return "exclude", "code: 카테고리 ID 코드값(M+숫자). 언어 텍스트 아님", []
    if re.fullmatch(r"/categories/\d+/complications/\d+/severity", ptr):
        return "exclude", "code: severity 영문 열거 코드값(/severity_levels 의 키와 같은 문자열). 언어 텍스트 아님", []
    if not re.search(r"[A-Za-z0-9가-힣]", v):
        return "exclude", "symbol-only: 글자·숫자 없는 기호 단독 값. 형태소 분석 대상 언어 텍스트 아님(값 자체는 source-map·review 에 보존)", []
    if re.fullmatch(r"/categories/\d+/complications/\d+/evidence", ptr):
        subs = url_subspans(v)
        segs = [x for x in SEP_RE.split(v)]
        if subs and all(URL_RE.fullmatch(x.rstrip(";, ")) for x in segs):
            return "exclude", "url: '; ' 로 나뉜 조각이 전부 URL 인 출처 값. 형태소 분석 부적합", subs
        return "analyze", "text: 출처 값에 URL 아닌 설명 텍스트 포함 — 분석, URL 부분구간은 url_subspans 로 표시", subs
    return "analyze", "text: 언어 텍스트", []


# ---------------------------------------------------------------- 3. 복합 표현 규칙
KW = {
    "frequency_degree": ["대부분", "대개", "거의", "매우", "흔함", "흔히", "흔하", "드묾", "드물", "극히", "약 ",
                         "최대", "최빈", "가장", "현저", "특히", "다소", "소수", "일부", "사실상", "보편적",
                         "상대적으로", "필발", "전례", "빈도", "경미", "경도", "경증", "중증", "심하", "심한",
                         "심부", "표재", "과도", "충분", "철저", "적정", "적절", "보수적", "점진적", "소량", "다량",
                         "대량", "고용량", "저강도", "고출력", "저출력", "고농도", "저농도",
                         # 3회차 읽기(미포착 어절 열람)에서 보강
                         "가는", "가늘", "얕은", "얇은", "높은", "높", "낮은", "낮", "큰", "짧은", "넓은", "느린", "저속",
                         "고위험", "엄격", "정확", "적극적", "최소", "유일", "핵심", "광범위", "단시간", "장시간", "고희석",
                         "세밀", "균등", "과밀", "과량", "과주입", "심해", "강함", "강해", "약한", "강한"],
    "negation": ["않", "없", "무관", "금지", "금기", "불필요", "불가", "미시행", "아님", "아닌", "아니", "무효",
                 "불명", "불확실", "부족", "불충분", "부적절", "불량", "불응", "불균", "비가역", "비무균", "비멸균",
                 "비감염", "비중화", "비HA", "비박피", "비침습", "비점착", "비절연", "미만", "제외", "배제", "회피",
                 "자제", "중단", "피함", "피해야"],
    "possibility_uncertainty": ["가능", "수 있", "추정", "의심", "고려", "보고", "가설", "논란", "제한적", "근거",
                                "기대하지", "경향", "감별", "시도"],
    "condition_scope": ["경우", "때", "에 한해", "따라", "단,", "다만", "동반", "특히", "부위별", "유형별", "성분별",
                        "에서", "에서는", "만으로", "단독", "병용", "병합", "± ", "±",
                        # 3회차 보강
                        "필요시", "필요 시", "으로만", "만 사용", "이면", "하면", "든", "어느", "모든", "전반", "공통"],
    "comparison_contrast": ["보다", "달리", "별개", "비해", "더 ", "상대적", "오히려", "대비", "역설", "반면", "와 달리"],
    "obligation_recommendation": ["필수", "권고", "권장", "우선", "주의", "필요", "준수", "반드시", "교육", "고지",
                                  "확인", "안내", "어려"],
    "time_relative": ["즉시", "직후", "당일", "이내", "이후", "이전", "전후", "시술 전", "시술 후", "시술 중",
                      "주입 중", "간격", "지속", "소실", "발현", "지연", "초기", "급성", "만성", "장기", "단기",
                      "영구", "일시적", "일과성", "누적", "반복", "재진", "경과",
                      # 3회차 보강
                      "기존", "최근", "병력", "기왕력", "이차", "2차", "1차", "재시술", "재평가", "추적", "주기", "까지"],
    "cross_reference": ["site_specific", "별도", "참조", "항목", ".json", "taxonomy", "safety.", "IFU", "MAUDE",
                        "FDA", "PubMed", "PMC", "ASDS", "ASJ", "internal", "clinical-standard", "임상 표준", "통설"],
}
CONDITION_SI_RE = re.compile(r"[^\s,.;:()·]+ 시(?=[\s,.;:)]|$)")
QTY_RE = re.compile(
    r"(?:[<>~]\s*)?\d+(?:\.\d+)?(?:\s*[-–~/]\s*\d+(?:\.\d+)?)?\s*"
    r"(?:%|mg/mL|mg|mL/h|mL|U|kDa|nm|G|시간|분|일|주|개월|년|세|회/일|회|건|차|쌍|events|reports)?"
    r"(?:\s*(?:이상|이하|미만|이내|초과|까지|전후|후|전|경|간격|마다|째)(?![가-힣]))?")
NUMWORD_RE = re.compile(r"(?<![가-힣])수\s?(?:분(?!\s?(?:섭취|공급|유입|손실|해|·))|시간|일|주|개월|년)(?:\s*(?:내|이내|후|간|에 걸쳐))?")
RANGE_RE = re.compile(r"[^\s,;()]+~[^\s,;()]+")
SYMREL_RE = re.compile(r"[^\s,;()]+(?:\s?(?:/|·|\+|±|→|—|–)\s?[^\s,;()]+)+")
LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9.:'’\-]*(?:\s+[A-Za-z0-9][A-Za-z0-9.:'’\-]*)*")


def sentence_spans(v):
    """'. ' 또는 '; ' 뒤에서 자른다. 단 '. ' 앞이 라틴 대문자 한 글자(예: 'S. aureus')면 자르지 않는다."""
    spans, st = [], 0
    for m in re.finditer(r"(?<=[.;]) ", v):
        p = m.start() - 1
        if v[p] == "." and p >= 1 and re.fullmatch(r"[A-Z]", v[p - 1]) and (p < 2 or not v[p - 2].isalpha()):
            continue
        spans.append([st, m.start()])
        st = m.end()
    spans.append([st, len(v)])
    return [s for s in spans if s[1] > s[0]]


def paren_spans(v):
    out, stack = [], []
    for i, c in enumerate(v):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            out.append([stack.pop(), i + 1])
    return sorted(out)


def clause_spans(v):
    """괄호 밖 ', ' 와 문장 경계로 나눈 쉼표 절."""
    out = []
    for ss, se in sentence_spans(v):
        depth, st = 0, ss
        for i in range(ss, se):
            c = v[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth = max(0, depth - 1)
            elif c == "," and depth == 0:
                out.append([st, i])
                st = i + 1
                while st < se and v[st] == " ":
                    st += 1
        out.append([st, se])
    return [s for s in out if s[1] > s[0]]


def eojeol_span(v, a, b):
    s = a
    while s > 0 and not v[s - 1].isspace():
        s -= 1
    e = b
    while e < len(v) and not v[e].isspace():
        e += 1
    while e > b and v[e - 1] in ",.;":
        e -= 1
    return [s, e]


def enclosing(spans, a, b):
    for s, e in spans:
        if s <= a and b <= e:
            return [s, e]
    return None


# ---------------------------------------------------------------- main
def main():
    raw = SRC.read_bytes()
    h0 = sha256(raw)
    text = raw.decode("utf-8")
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert all(ord(c) <= 0xFFFF for c in text), "BMP 밖 문자 — 오프셋 단위 재검토 필요"
    cum = [0]
    for c in text:
        cum.append(cum[-1] + len(c.encode("utf-8")))
    bspan = lambda sp: [cum[sp[0]], cum[sp[1]]]

    sc = Scanner(text)
    sc.parse()
    data = json.loads(text)
    log(f"source sha256={h0} bytes={len(raw)} code_points={len(text)} nodes={len(sc.nodes)} "
        f"keys={len(sc.keys)} duplicate_keys={len(sc.duplicate_keys)} escapes={len(sc.escapes)}")

    source = {"path": SRC_REL, "size_bytes": len(raw), "code_points": len(text), "sha256_start": h0,
              "encoding": "UTF-8 · BOM 없음 · 개행 없는 한 줄",
              "escape_sequences": len(sc.escapes), "non_bmp_chars": 0,
              "offset_unit": OFFSET_UNIT}

    for n in sc.nodes:
        n["byte_span"] = bspan(n["span"])
        if "value_span" in n:
            n["value_byte_span"] = bspan(n["value_span"])
            lit_inner = text[n["value_span"][0]:n["value_span"][1]]
            n["decoded_equals_literal_inner"] = lit_inner == n["value"]
        n["context"] = context_of(n["pointer"], data)
    for k in sc.keys:
        k["byte_span"] = bspan(k["span"])
        k["context"] = context_of(k["object_pointer"], data)

    fno = {}
    for k in sc.keys:
        pat = re.sub(r"/\d+", "/*", k["value_pointer"])
        fno.setdefault(k["key"], {}).setdefault(pat, []).append(k["value_pointer"])

    source_map = {
        "source": source,
        "notes": [
            "nodes: 원문 JSON 의 모든 노드(객체·배열·문자열·숫자·불리언·null)를 문서 순서대로 1개씩. 빈 배열·빈 문자열도 노드다.",
            "span: 파일 전체 텍스트 기준 코드 포인트 [start,end). 문자열 노드의 span 은 따옴표 포함 JSON 리터럴, value_span 은 따옴표 안쪽.",
            "value 는 디코딩된 값, literal 은 원문 JSON 리터럴. 이 파일엔 이스케이프가 0개라 decoded_equals_literal_inner 가 전부 true 여야 한다.",
            "keys: 모든 키 출현(객체 안 순서 포함). duplicate=true 면 같은 객체 안 중복 키(이 파일은 0).",
            "context: 노드가 속한 카테고리·부작용 항목·필드. 해석이 아니라 위치 정보다.",
        ],
        "duplicate_keys": sc.duplicate_keys,
        "escape_sequences": sc.escapes,
        "field_name_occurrences": fno,
        "keys": sc.keys,
        "nodes": sc.nodes,
    }

    # ---------------- 형태소
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")
    analyzer = {
        "name": "Kiwi (kiwipiepy)", "kiwipiepy": kiwipiepy.__version__, "python": sys.version.split()[0],
        "constructor": "Kiwi(num_workers=1, model_type='cong') — 그 밖 생성자 인자 기본값(내장 기본 사전)",
        "model_type": "cong", "num_workers": 1, "user_dictionary": "없음(추가 단어 0)",
        "tokenize_kwargs": "기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, "
                           "blocklist=None, compatible_jamo=False, split_sents=False, typos=None)",
        "tagset": "Kiwi 품사 체계(세종 기반 확장: NNG/NNP/NNB/NR/NP/VV/VA/MAG/MAJ/MM/J*/E*/X*/S*/W_* 등)",
        "lemma": "Kiwi Token.lemma 값 그대로. 도구가 주는 값 외에 기본형을 만들지 않았다.",
        "offset": "Kiwi Token.start/len 을 값 문자열 기준 [start,start+len) 으로 기록. surface = text[span].",
        "normalization": "없음 — 원문 문자열을 그대로 입력(정규화 전후 대응 불필요).",
        "invocation": "uv run --python 3.12 --with kiwipiepy==0.24.1",
    }
    values, excluded = [], []
    for n in sc.nodes:
        if n["type"] != "string":
            continue
        v = n["value"]
        act, reason, subs = classify(n["pointer"], v)
        if act == "exclude":
            excluded.append({"pointer": n["pointer"], "value": v, "reason": reason,
                             "url_subspans": subs, "context": n["context"]})
            continue
        toks = []
        for i, t in enumerate(kiwi.tokenize(v)):
            sp = [t.start, t.start + t.len]
            toks.append({"i": i, "form": t.form, "tag": str(t.tag), "lemma": t.lemma, "span": sp,
                         "surface": v[sp[0]:sp[1]], "form_equals_surface": t.form == v[sp[0]:sp[1]],
                         "in_url_subspan": any(a <= sp[0] and sp[1] <= b for a, b in subs)})
        values.append({"pointer": n["pointer"], "text": v, "file_span_of_text": n["value_span"],
                       "reason": reason, "url_subspans": subs, "context": n["context"], "tokens": toks})
    field_names = []
    for k in sorted(fno):
        toks = [{"i": i, "form": t.form, "tag": str(t.tag), "lemma": t.lemma, "span": [t.start, t.start + t.len],
                 "surface": k[t.start:t.start + t.len]} for i, t in enumerate(kiwi.tokenize(k))]
        field_names.append({"field_name": k, "occurrence_patterns": sorted(fno[k]),
                            "occurrence_count": sum(len(x) for x in fno[k].values()),
                            "tokens": toks, "identifier_parts_rule_based": k.split("_"),
                            "note": "필드명은 영문 식별자. Kiwi 결과(SL 등)와 '_' 분할을 함께 남긴다. 필드명의 뜻은 정하지 않는다."})

    seg = json.loads((HERE / "segmentation-review-rules.json").read_text())
    seg_occ, seg_errors = [], []
    for rule in seg["rules"]:
        raw_t = [tuple(x) for x in rule["raw_tokens"]]
        hits, other = 0, 0
        for val in values:
            t = val["text"]
            for mm in re.finditer(re.escape(rule["phrase"]), t):
                a, b = mm.start(), mm.end()
                ov = [x for x in val["tokens"] if x["span"][1] > a and x["span"][0] < b]
                if [(x["form"], x["tag"]) for x in ov] == raw_t:
                    hits += 1
                    seg_occ.append({"id": f"{rule['id']}-{hits:02d}", "rule": rule["id"], "pointer": val["pointer"],
                                    "phrase": rule["phrase"], "phrase_span": [a, b],
                                    "raw_tokens": [[x["form"], x["tag"], x["span"]] for x in ov],
                                    "token_indexes": [x["i"] for x in ov], "kind": rule["kind"],
                                    "issue": rule["issue"], "impact": rule["impact"],
                                    "status": "표시됨(교정 아님) — 원시 Kiwi 토큰 유지", "context": val["context"]})
                else:
                    other += 1
        rule["occurrences_flagged"] = hits
        rule["occurrences_other_analysis"] = other
        if hits == 0:
            seg_errors.append(f"seg rule {rule['id']} matched 0 occurrences")
    if seg_errors:
        for e in seg_errors:
            log("ERROR", e)
        sys.exit(1)
    seg["occurrences"] = seg_occ
    ntok = sum(len(x["tokens"]) for x in values)
    morphology = {"source": source, "analyzer": analyzer,
                  "scope_note": "문자열 노드 전부를 values(분석) 또는 excluded_values(제외·사유) 중 정확히 한 곳에 둔다. "
                                "숫자·불리언·null 노드는 이 원장에 없다. 필드명은 field_names 에 따로 분석한다.",
                  "values": values, "excluded_values": excluded, "field_names": field_names,
                  "segmentation_review_note": seg["note"], "segmentation_review_rules": seg["rules"],
                  "segmentation_review": seg["occurrences"]}
    log(f"morphology: analyzed={len(values)} excluded={len(excluded)} tokens={ntok} field_names={len(field_names)} "
        f"segmentation_review={len(seg['occurrences'])}")

    # ---------------- 복합 표현
    exprs = []
    rules = []

    def add(n, sp, cat, method, extra=None):
        v = n["value"]
        rec = {"pointer": n["pointer"], "span": sp, "text": v[sp[0]:sp[1]], "category_candidate": cat,
               "method": method}
        if extra:
            rec.update(extra)
        rec["context"] = n["context"]
        exprs.append(rec)

    rules += [
        {"category_candidate": "segment.value", "method": "값 전체", "pattern": None},
        {"category_candidate": "segment.sentence", "method": "regex 문장분할: '. ' 또는 '; ' 뒤 공백에서 자름. "
         "'S. aureus' 처럼 앞이 라틴 대문자 한 글자인 '. ' 는 자르지 않음", "pattern": "(?<=[.;]) "},
        {"category_candidate": "segment.clause", "method": "괄호 밖 ', ' 와 문장 경계로 자른 절", "pattern": None},
        {"category_candidate": "segment.parenthetical", "method": "괄호 짝 (중첩 포함, 괄호 포함 구간)", "pattern": None},
        {"category_candidate": "quantity_unit_time", "method": "regex 숫자(범위)+단위+후치 시간·범위어. 단위 없는 숫자(열거 번호·연도·PMID 등)도 후보로 남는다 — 수량이라는 판정 아님",
         "pattern": QTY_RE.pattern},
        {"category_candidate": "quantity_unit_time", "method": "regex '수+시간단위'(수일·수 시간 등) — 수치 없는 시간 표현. 앞이 한글이면(가수분해) 제외, '수분 섭취·공급·유입·손실·수분·전해질'(물)은 제외",
         "pattern": NUMWORD_RE.pattern},
        {"category_candidate": "range", "method": "regex '~' 양옆 어절(공백 없이 붙은 것만). 앞이 공백인 '~숫자'(예: '~87%')는 근사 표기라 범위로 잡지 않음 — manual.approx_prefix 로 따로 기록", "pattern": RANGE_RE.pattern},
        {"category_candidate": "symbol_relation", "method": "regex '/ · + ± → — –' 로 이어진 어절 묶음 — "
         "기호 의미(대안·병기·인과 등)는 정하지 않음", "pattern": SYMREL_RE.pattern},
        {"category_candidate": "latin_term", "method": "regex 라틴 문자 연속 구간(URL 부분구간 제외)",
         "pattern": LATIN_RE.pattern},
        {"category_candidate": "condition_scope", "method": "regex '<어절> 시' (조건 '…시')", "pattern": CONDITION_SI_RE.pattern},
    ]
    for cat, kws in KW.items():
        rules.append({"category_candidate": cat, "method": "keyword 부분문자열 → 감싼 어절(span)과 감싼 절(clause_span) 기록",
                      "pattern": kws})
    rules.append({"category_candidate": "manual.*", "method": "직접 읽기로 고른 구절(manual-expressions.json). "
                  "build 가 원문에서 위치를 찾고 없으면 실패", "pattern": None})

    for n in sc.nodes:
        if n["type"] != "string":
            continue
        v = n["value"]
        act, _, subs = classify(n["pointer"], v)
        add(n, [0, len(v)], "segment.value", "값 전체", {"analysis": act})
        if act == "exclude":
            continue
        inurl = lambda a, b: any(s <= a and b <= e for s, e in subs) or any(a < e and s < b for s, e in subs)
        sents = sentence_spans(v)
        if len(sents) > 1:
            for sp in sents:
                add(n, sp, "segment.sentence", "regex 문장분할")
        clauses = clause_spans(v)
        if len(clauses) > 1:
            for sp in clauses:
                add(n, sp, "segment.clause", "괄호 밖 쉼표 절")
        for sp in paren_spans(v):
            add(n, sp, "segment.parenthetical", "괄호 짝", {"clause_span": enclosing(clauses, *sp)})
        seen = set()
        for rx, cat, meth in [(QTY_RE, "quantity_unit_time", "regex 숫자+단위"),
                              (NUMWORD_RE, "quantity_unit_time", "regex 수+시간단위"),
                              (RANGE_RE, "range", "regex ~"),
                              (SYMREL_RE, "symbol_relation", "regex 기호연결"),
                              (LATIN_RE, "latin_term", "regex 라틴"),
                              (CONDITION_SI_RE, "condition_scope", "regex '…시'")]:
            for m in rx.finditer(v):
                a, b = m.start(), m.end()
                while b > a and v[b - 1] in " .,;":
                    b -= 1
                if b <= a or not re.search(r"\w", v[a:b]):
                    continue
                if cat == "quantity_unit_time" and rx is QTY_RE and not re.search(r"\d", v[a:b]):
                    continue
                if inurl(a, b):
                    continue
                key = (a, b, cat, meth)
                if key in seen:
                    continue
                seen.add(key)
                add(n, [a, b], cat, meth, {"clause_span": enclosing(clauses, a, b)})
        for cat, kws in KW.items():
            hits = set()
            for kw in kws:
                for m in re.finditer(re.escape(kw), v):
                    a, b = m.start(), m.end()
                    if inurl(a, b):
                        continue
                    ej = eojeol_span(v, a, b)
                    k = (ej[0], ej[1], kw)
                    if k in hits:
                        continue
                    hits.add(k)
                    add(n, ej, cat, "keyword", {"keyword": kw, "keyword_span": [a, b],
                                                "clause_span": enclosing(clauses, a, b)})

    man = json.loads((HERE / "manual-expressions.json").read_text())
    nmap = {n["pointer"]: n for n in sc.nodes}
    merr = []
    for r in man["expressions"]:
        n = nmap.get(r["pointer"])
        if not n or n["type"] != "string":
            merr.append(f"manual {r['id']}: bad pointer {r['pointer']}")
            continue
        v = n["value"]
        occ = [m.start() for m in re.finditer(re.escape(r["text"]), v)]
        k = r.get("occurrence", 0)
        if len(occ) <= k:
            merr.append(f"manual {r['id']}: text not found {r['text']!r} @ {r['pointer']}")
            continue
        a = occ[k]
        add(n, [a, a + len(r["text"])], "manual." + r["category_candidate"], "manual",
            {"manual_id": r["id"], "note": r.get("note"), "clause_span": enclosing(clause_spans(v), a, a + len(r["text"]))})
    if merr:
        for e in merr:
            log("ERROR", e)
        sys.exit(1)
    for i, e in enumerate(exprs):
        e["id"] = f"E{i:05d}"
    # 키 순서 정리(id 먼저)
    exprs = [{"id": e["id"], **{k: v for k, v in e.items() if k != "id"}} for e in exprs]
    from collections import Counter
    cc = Counter(e["category_candidate"] for e in exprs)
    expressions = {"source": source, "method": {
        "note": "범주는 탐색 관점의 후보 표시이며 확정 분류가 아니다. regex·keyword·수동목록 결과를 전수 의미 해석으로 쓰지 않는다. "
                "같은 구간이 여러 범주에 겹치는 것은 의도된 겹침이다. keyword 후보에는 오탐이 섞여 있다(예: '비'로 시작하는 낱말, '보고'의 동음). "
                "오탐 판정은 하지 않았고, 직접 읽기에서 확인한 의미 위험은 manual-observations·issues 에 따로 적었다.",
        "rules": rules, "counts_by_category": dict(sorted(cc.items()))},
        "expressions": exprs}
    log(f"expressions: total={len(exprs)} manual={len(man['expressions'])} " +
        " ".join(f"{k}={v}" for k, v in sorted(cc.items())))

    # ---------------- 관찰 검사
    obs = json.loads((HERE / "manual-observations.json").read_text())
    oerr = []
    for o in obs["observations"]:
        for ev in o["evidence"]:
            n = nmap.get(ev["pointer"])
            if n is None:
                oerr.append(f"obs {o['id']}: bad pointer {ev['pointer']}")
            elif ev.get("quote") and (n["type"] != "string" or ev["quote"] not in n["value"]):
                oerr.append(f"obs {o['id']}: quote not in {ev['pointer']}: {ev['quote']!r}")
    if oerr:
        for e in oerr:
            log("ERROR", e)
        sys.exit(1)
    log(f"observations: {len(obs['observations'])} (evidence quotes all found)")

    # ---------------- review.md
    review = render_review(sc, data, nmap, source, obs, values, excluded, ntok, len(exprs), cc,
                           len(seg["occurrences"]), len(man["expressions"]))

    h1 = sha256(SRC.read_bytes())
    assert h1 == h0, "원본 해시 변경!"
    for d in (source_map, morphology, expressions):
        d["source"] = dict(source, sha256_end=h1)
    (HERE / "source-map.json").write_text(json.dumps(source_map, ensure_ascii=False, indent=1))
    (HERE / "morphology.json").write_text(json.dumps(morphology, ensure_ascii=False, indent=1))
    (HERE / "expressions.json").write_text(json.dumps(expressions, ensure_ascii=False, indent=1))
    (HERE / "review.md").write_text(review)
    log(f"source sha256 end={h1} unchanged={h1 == h0}")
    (HERE / "build-output.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------------- review.md
def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def render_review(sc, data, nmap, source, obs, values, excluded, ntok, nexpr, cc, nseg, nman):
    tpl = (HERE / "review-template.md").read_text()
    by_scope = {}
    for o in obs["observations"]:
        by_scope.setdefault(o["scope"], []).append(o)

    def obs_block(scope):
        out = []
        for o in by_scope.get(scope, []):
            ev = "; ".join(f"`{e['pointer']}`" + (f" 「{e['quote']}」" if e.get("quote") else "") for e in o["evidence"])
            ref = f" → {o['issue']}" if o.get("issue") else ""
            out.append(f"- **{o['id']}** ({o['kind']}) {o['text']}{ref}  \n  근거: {ev}")
        return "\n".join(out)

    # 컬럼 구성 표
    strings = [n for n in sc.nodes if n["type"] == "string"]
    comps = [c for cat in data["categories"] for c in cat["complications"]]
    rows = []

    def first(pat):
        rx = re.compile("^" + pat + "$")
        return [n for n in sc.nodes if rx.match(n["pointer"])]

    def ex(n, cut=60):
        if n["type"] == "string":
            v = n["value"]
            return "\"" + md(v if len(v) <= cut else v[:cut] + "…") + "\""
        if n["type"] == "array":
            return "[]" if n["length"] == 0 else f"[{n['length']}개]"
        return n["type"]

    spec = [
        ("(루트)", "", "object", "키 2개: severity_levels, categories"),
        ("severity_levels", "/severity_levels", "object", "키 4개(mild, moderate, severe, critical)"),
        ("severity_levels.mild", "/severity_levels/mild", "string", "스칼라"),
        ("severity_levels.moderate", "/severity_levels/moderate", "string", "스칼라"),
        ("severity_levels.severe", "/severity_levels/severe", "string", "스칼라"),
        ("severity_levels.critical", "/severity_levels/critical", "string", "스칼라"),
        ("categories", "/categories", "array", "객체 배열"),
        ("categories[].id", r"/categories/\d+/id", "string", "스칼라(코드)"),
        ("categories[].name", r"/categories/\d+/name", "string", "스칼라"),
        ("categories[].complications", r"/categories/\d+/complications", "array", "객체 배열"),
        ("categories[].complications[]", r"/categories/\d+/complications/\d+", "object", "부작용 항목 객체"),
    ]
    for f in ["name", "severity", "incidence", "onset", "duration", "mechanism", "risk_factors",
              "management", "prevention", "evidence"]:
        spec.append((f"categories[].complications[].{f}", rf"/categories/\d+/complications/\d+/{f}",
                     "array" if f == "risk_factors" else "string",
                     "문자열 배열" if f == "risk_factors" else "스칼라"))
    spec.append(("categories[].complications[].risk_factors[]", r"/categories/\d+/complications/\d+/risk_factors/\d+",
                 "string", "배열 항목"))
    for label, pat, typ, nest in spec:
        ns = first(re.escape(pat) if not "\\d" in pat else pat) if pat else [sc.nodes[0]]
        types = sorted({n["type"] for n in ns})
        if label.startswith("categories[].complications[].") and label.count(".") == 2 and not label.endswith("[]"):
            presence = f"{len(ns)}/{len(comps)} 항목"
        else:
            presence = f"{len(ns)}회"
        e = ns[0]
        loc = f"`{e['pointer']}`" if e["pointer"] else '`""`(루트)'
        rows.append(f"| `{label}` | {('`' + pat + '`') if pat else '`\"\"`(빈 문자열 = 루트)'} | {'/'.join(types)} | {nest} | {presence} | {ex(e)} | {loc} |")
    # 변형·빈 값·선택 필드 행
    empty_rf = [n for n in first(r"/categories/\d+/complications/\d+/risk_factors") if n["length"] == 0]
    full_rf = [n for n in first(r"/categories/\d+/complications/\d+/risk_factors") if n["length"] > 0]
    rows.append(f"| `…risk_factors` (빈 배열 변형) | 〃 | array | 길이 0 | {len(empty_rf)}/{len(comps)} 항목 | [] | `{empty_rf[0]['pointer']}` |")
    lens = sorted({n['length'] for n in full_rf})
    rows.append(f"| `…risk_factors` (항목 있는 변형) | 〃 | array | 길이 {lens[0]}~{lens[-1]} | {len(full_rf)}/{len(comps)} 항목 | [{full_rf[0]['length']}개] | `{full_rf[0]['pointer']}` |")
    no_dur = [i for i, c in enumerate(comps) if "duration" not in c]
    no_ev = [i for i, c in enumerate(comps) if "evidence" not in c]
    rows.append(f"| `…duration` (키 없음 변형) | — | (없음) | 선택 필드 | {len(no_dur)}/{len(comps)} 항목에 키 자체가 없음 | (키 없음) | 예 `/categories/0/complications/0` |")
    rows.append(f"| `…evidence` (키 없음 변형) | — | (없음) | 선택 필드 | {len(no_ev)}/{len(comps)} 항목에 키 자체가 없음 | (키 없음) | 예 `/categories/0/complications/3` |")
    dash = [n for n in strings if n["value"] == "-"]
    for n in dash:
        rows.append(f"| `…{n['key']}` (기호 단독 값) | 〃 | string | 스칼라 | {len(dash)}회 | \"-\" | `{n['pointer']}` |")
    ev_url = [x for x in excluded if x["reason"].startswith("url")]
    ev_txt = [x for x in values if x["pointer"].endswith("/evidence")]
    rows.append(f"| `…evidence` (URL만 변형) | 〃 | string | 스칼라 | {len(ev_url)}회 | \"{md(ev_url[0]['value'][:60])}…\" | `{ev_url[0]['pointer']}` |")
    rows.append(f"| `…evidence` (설명 텍스트 포함 변형) | 〃 | string | 스칼라 | {len(ev_txt)}회 | \"{md(ev_txt[0]['text'][:60])}…\" | `{ev_txt[0]['pointer']}` |")
    col_table = ("| 원본 컬럼명(경로 패턴) | JSON Pointer 패턴 | 자료형 | 중첩 구조 | 출현 | 원문 예시 | 예시 위치 |\n"
                 "|---|---|---|---|---|---|---|\n" + "\n".join(rows))

    # 키 순서 변형
    orders = {}
    for i, c in enumerate(comps):
        orders.setdefault(tuple(c.keys()), []).append(i)
    order_lines = []
    flat = [(ci, mi) for ci, cat in enumerate(data["categories"]) for mi in range(len(cat["complications"]))]
    for k, ids in orders.items():
        ptrs = ", ".join(f"`/categories/{flat[i][0]}/complications/{flat[i][1]}`" for i in ids)
        order_lines.append(f"| {len(k)} | `{', '.join(k)}` | {len(ids)} | {ptrs} |")
    order_table = "| 키 수 | 키 순서(원문 그대로) | 항목 수 | 위치 |\n|---|---|---|---|\n" + "\n".join(order_lines)

    # 항목별 값
    items = []
    sev = data["severity_levels"]
    items.append("### severity_levels\n\n| 원본 컬럼명 | Pointer | 원문 값 |\n|---|---|---|")
    for k in sev:
        items.append(f"| `{k}` | `/severity_levels/{k}` | {md(sev[k])} |")
    items.append("")
    if by_scope.get("/severity_levels"):
        items.append("**잠정 관찰**\n\n" + obs_block("/severity_levels") + "\n")
    for ci, cat in enumerate(data["categories"]):
        items.append(f"### `/categories/{ci}` — id `{cat['id']}` · name 「{cat['name']}」 · complications {len(cat['complications'])}개\n")
        # 카테고리 id·name 도 값마다 개별 Pointer 행(batch-01 검토 §3.3 보완 1)
        items.append("| 원본 컬럼명 | Pointer | 원문 값 |\n|---|---|---|")
        for f in ("id", "name"):
            items.append(f"| `{f}` | `/categories/{ci}/{f}` | {md(cat[f])} |")
        items.append("")
        if by_scope.get(f"/categories/{ci}"):
            items.append("**잠정 관찰 (카테고리)**\n\n" + obs_block(f"/categories/{ci}") + "\n")
        for mi, c in enumerate(cat["complications"]):
            base = f"/categories/{ci}/complications/{mi}"
            items.append(f"#### `{base}` — {md(c['name'])}\n")
            items.append("| 원본 컬럼명 | Pointer | 원문 값 |\n|---|---|---|")
            for f in ["name", "severity", "incidence", "onset", "duration", "mechanism", "risk_factors",
                      "management", "prevention", "evidence"]:
                if f not in c:
                    items.append(f"| `{f}` | — | (키 없음) |")
                    continue
                v = c[f]
                if isinstance(v, list):
                    if not v:
                        items.append(f"| `{f}` | `{base}/{f}` | [] (빈 배열) |")
                    for k, x in enumerate(v):
                        items.append(f"| `{f}[{k}]` | `{base}/{f}/{k}` | {md(x)} |")
                else:
                    items.append(f"| `{f}` | `{base}/{f}` | {md(v)} |")
            extra = [k for k in c if k not in ("name", "severity", "incidence", "onset", "duration", "mechanism",
                                               "risk_factors", "management", "prevention", "evidence")]
            assert not extra, extra
            items.append("")
            if by_scope.get(base):
                items.append("**잠정 관찰**\n\n" + obs_block(base) + "\n")
    top_obs = obs_block("/")
    out = tpl
    rep = {
        "{{SHA}}": source["sha256_start"], "{{BYTES}}": f"{source['size_bytes']:,}",
        "{{CP}}": f"{source['code_points']:,}", "{{NODES}}": str(len(sc.nodes)), "{{KEYS}}": str(len(sc.keys)),
        "{{NSTR}}": str(len(strings)), "{{NVAL}}": str(len(values)), "{{NEXC}}": str(len(excluded)),
        "{{NTOK}}": f"{ntok:,}", "{{NEXPR}}": f"{nexpr:,}", "{{NSEG}}": str(nseg), "{{NMAN}}": str(nman),
        "{{NOBS}}": str(len(obs["observations"])),
        "{{COLUMN_TABLE}}": col_table, "{{ORDER_TABLE}}": order_table, "{{ITEMS}}": "\n".join(items),
        "{{TOP_OBS}}": top_obs,
        "{{EXPR_COUNTS}}": " · ".join(f"{k} {v}" for k, v in sorted(cc.items())),
    }
    for k, v in rep.items():
        out = out.replace(k, v)
    assert "{{" not in out, re.findall(r"\{\{\w+\}\}", out)
    return out


if __name__ == "__main__":
    main()
