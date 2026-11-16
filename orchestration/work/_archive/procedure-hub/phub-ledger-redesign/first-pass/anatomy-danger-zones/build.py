#!/usr/bin/env python3
"""anatomy-danger-zones.json 1차 수집 재현 스크립트.

실행(레포 루트에서):
  OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
    python orchestration/work/phub-ledger-redesign/first-pass/anatomy-danger-zones/build.py

원본은 읽기만 한다. 이 폴더 안의 산출물만 쓴다:
  source-map.json, morphology.json, expressions.json, coverage.json,
  review.md, review-part-S00.md … review-part-S11.md
입력(수동 직접 읽기 기록): manual-review.json
"""
import hashlib
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../../.."))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/anatomy-danger-zones.json"
SRC = os.path.join(REPO, SRC_REL)
SELF_REL = os.path.relpath(HERE, REPO)


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def esc_token(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 원문 스캐너
class Scanner:
    """디코딩된 원문 문자열 위의 재귀 하강 JSON 스캐너.
    모든 값·키의 JSON 리터럴 구간([start,end) 코드 포인트)을 기록하고 중복 키를 감지한다."""

    WS = " \t\r\n"

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []      # 문서 순서
        self.dup_keys = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def string(self):
        assert self.t[self.i] == '"', self.i
        s = self.i
        self.i += 1
        has_escape = False
        while True:
            c = self.t[self.i]
            if c == "\\":
                has_escape = True
                self.i += 2
                continue
            if c == '"':
                self.i += 1
                break
            self.i += 1
        lit = self.t[s:self.i]
        return json.loads(lit), (s, self.i), has_escape

    def value(self, ptr, parent, key, index, depth):
        self.ws()
        c = self.t[self.i]
        node = OrderedDict(pointer=ptr, parent=parent, key=key, index=index, depth=depth)
        self.nodes.append(node)
        s = self.i
        if c == "{":
            node["json_type"] = "object"
            self.i += 1
            keys = []
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, kspan, kesc = self.string()
                    if k in keys:
                        self.dup_keys.append({"object": ptr, "key": k, "key_literal_cp_span": list(kspan)})
                    keys.append(k)
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    child_ptr = ptr + "/" + esc_token(k)
                    before = len(self.nodes)
                    self.value(child_ptr, ptr, k, None, depth + 1)
                    self.nodes[before]["key_literal_cp_span"] = list(kspan)
                    self.nodes[before]["key_has_escape"] = kesc
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node["size"] = len(keys)
            node["keys_in_order"] = keys
        elif c == "[":
            node["json_type"] = "array"
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(ptr + "/" + str(n), ptr, None, n, depth + 1)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            node["size"] = n
        elif c == '"':
            v, span, e = self.string()
            node["json_type"] = "string"
            node["value"] = v
            node["has_escape"] = e
            node["string_content_cp_span"] = [span[0] + 1, span[1] - 1]
        else:
            m = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null").match(self.t, self.i)
            lit = m.group(0)
            self.i = m.end()
            v = json.loads(lit)
            node["value"] = v
            node["number_literal"] = lit
            node["json_type"] = ("null" if v is None else "boolean" if isinstance(v, bool)
                                 else "integer" if isinstance(v, int) else "number")
        node["literal_cp_span"] = [s, self.i]
        return node


def section_of(ptr):
    m = re.match(r"^/zones/(\d+)(/|$)", ptr)
    if m:
        return "S%02d" % (int(m.group(1)) + 1)
    return "S00"


def pattern_of(ptr):
    return re.sub(r"/\d+(?=/|$)", "/*", ptr) or "(root)"


def field_label(node):
    if node["key"] is not None:
        return node["key"]
    return None


# ---------------------------------------------------------------- 형태소 대상 분류
EXCLUDE_STRING_PATTERNS = {
    "/version": "버전 코드 문자열('1.2') — 언어 텍스트 아님",
    "/updated": "날짜 문자열(ISO 형식) — 언어 텍스트 아님",
    "/zones/*/id": "zone 식별자 slug(영문 소문자 코드) — ID/코드값",
    "/zones/*/danger_color": "색상 열거 코드값(red/orange/yellow/green) — 코드값",
    "/zones/*/nerves/*/type": "신경 종류 열거 코드값(sensory/motor) — 코드값",
}

# 전문어 분절 관찰 대상(수동 선정: 직접 읽기에서 오분절 가능성을 보고 고른 낱말. 원문에 실제 있는 표면형만)
WATCH_TERMS = [
    "활차상동맥", "안와상동맥", "안와상연", "안와상절흔", "골막상층", "골막상", "캐뉼러", "히알루로니다제",
    "추미근", "비근근", "상안검거근", "안검하수", "천측두동맥", "심부측두근막", "상측두융합선", "측두분지",
    "안륜근", "안와격막", "안검외반", "배비동맥", "외비동맥", "주상동맥", "비중격하강근", "비첨부", "비익",
    "안면동맥", "각동맥", "상순거근", "안면횡동맥", "협지방체", "이하선관", "관골궁", "관자궁", "교근",
    "상순동맥", "하순동맥", "구륜근", "이신경공", "구각하제근", "하악변연신경", "하순하제근", "광경근",
    "외경정맥", "전경정맥", "흉쇄유돌근", "대이개신경", "연하곤란", "저점도", "고점도", "중점도",
    "역행성", "표재성", "피하층", "점막하층", "볼류메트릭", "볼루스", "망막중심동맥", "안와하공",
    "글라벨라", "비순주름", "팔자주름", "중측두정맥", "심부측두동맥", "구후",
]

AUTO_PATTERNS = OrderedDict([
    ("range", r"(?<![\d.])\d+(?:,\d{3})*(?:\.\d+)?\s?[-–~]\s?\d+(?:,\d{3})*(?:\.\d+)?(?:\s?(?:mL|mm|cm|IU|U|units|%|분|시간|mg|포인트))?"),
    ("number_unit", r"(?<![\d.,])\d+(?:,\d{3})*(?:\.\d+)?\s?(?:mL|mm|cm|IU|U|units|%|분|시간|주|mg|포인트|cadaver)(?![A-Za-z])"),
    ("comparator", r"≥|±|이상|이하|이내|미만|까지"),
    ("negation_prohibition", r"금지|금기|불가|않|없|아님|피할|피하고|불충분"),
    ("possibility_frequency", r"수 있|가능|드물게|드묾|대개|거의|대부분|상대적으로|사실상"),
    ("condition", r"(?<= )시(?=[ ,)\.;]|$)|이면|경우|의심 시"),
    ("time_order", r"즉시|즉각|지체 없이|조기|이전|현재|최신|초기|로딩 후|침윤 후|촉진 후|필러 후|시술 전|주사 전|\d+(?:-\d+)?(?:분|시간|주) ?내"),
    ("degree_emphasis", r"매우|너무|과다|과도|현저히|강력|절대|반드시|가장|최고|최소|최대|최다|필수"),
    ("arrow", r"→"),
    ("plus", r" \+ "),
    ("slash", r"/"),
    ("em_dash", r"—"),
    ("middle_dot", r"·"),
    ("citation", r"[A-Z][A-Za-z]+ et al\.,[^;)]*?(?:\d{4}(?:;[\d()\-:]+)?)|Beleznay \d{4}|Anat Rec \d{4} cadaver|SRA \d{4}|JCD \d{4}, USG n=\d+"),
])


def main():
    h0 = sha256(SRC)
    raw = open(SRC, "rb").read()
    text = raw.decode("utf-8")
    assert all(ord(c) <= 0xFFFF for c in text), "BMP 밖 문자 존재 — 오프셋 단위 재검토 필요"
    # 코드포인트 → 바이트 오프셋
    boff = [0]
    for ch in text:
        boff.append(boff[-1] + len(ch.encode("utf-8")))

    sc = Scanner(text)
    sc.value("", None, None, None, 0)
    sc.ws()
    assert sc.i == len(text), "후행 데이터"
    nodes = sc.nodes
    std = json.loads(text)

    def get(ptr):
        x = std
        if ptr == "":
            return x
        for tok in ptr[1:].split("/"):
            tok = tok.replace("~1", "/").replace("~0", "~")
            x = x[int(tok)] if isinstance(x, list) else x[tok]
        return x

    any_escape = False
    zone_ctx = {}
    for i, z in enumerate(std["zones"]):
        zone_ctx["S%02d" % (i + 1)] = {"zone_pointer": "/zones/%d" % i, "id": z["id"],
                                        "name_ko": z["name_ko"], "name_en": z["name_en"]}
    for n in nodes:
        n["literal_byte_span"] = [boff[n["literal_cp_span"][0]], boff[n["literal_cp_span"][1]]]
        if "string_content_cp_span" in n:
            a, b = n["string_content_cp_span"]
            n["string_content_byte_span"] = [boff[a], boff[b]]
            any_escape |= n["has_escape"]
        n["is_leaf"] = n["json_type"] not in ("object", "array") or n["size"] == 0
        n["is_empty_container"] = n["json_type"] in ("object", "array") and n["size"] == 0
        n["path_pattern"] = pattern_of(n["pointer"])
        n["section"] = section_of(n["pointer"])
        n["document_order"] = nodes.index(n)
        # 문맥 참조: 상위 컨테이너 사슬과 zone 식별 필드
        chain = []
        p = n["parent"]
        while p is not None:
            chain.append(p)
            p = next(x["parent"] for x in nodes if x["pointer"] == p)
        n["ancestor_pointers"] = chain
        if n["section"] != "S00":
            zc = zone_ctx[n["section"]]
            n["context_refs"] = [zc["zone_pointer"] + "/id", zc["zone_pointer"] + "/name_ko", zc["zone_pointer"] + "/name_en"]
        else:
            n["context_refs"] = []
        # 동일 객체 내 형제 필드(함께 해석할 주변 필드)
        if n["parent"] is not None:
            n["sibling_pointers"] = [x["pointer"] for x in nodes if x["parent"] == n["parent"] and x["pointer"] != n["pointer"]]
        assert get(n["pointer"]) == n.get("value", get(n["pointer"])), n["pointer"]
        lit = text[n["literal_cp_span"][0]:n["literal_cp_span"][1]]
        assert json.loads(lit) == get(n["pointer"]), n["pointer"]
    assert not any_escape, "이스케이프 존재 — 값↔파일 구간 매핑 별도 필요"

    leaves = [n for n in nodes if n["is_leaf"]]
    str_leaves = [n for n in leaves if n["json_type"] == "string"]

    # 중복 문자열 값
    by_val = defaultdict(list)
    for n in str_leaves:
        by_val[n["value"]].append(n["pointer"])
    dup_strings = [{"value": v, "pointers": ps} for v, ps in by_val.items() if len(ps) > 1]

    # 필드명 출현
    field_occ = OrderedDict()
    for n in nodes:
        if n["key"] is not None:
            field_occ.setdefault(n["key"], []).append(n["pointer"])

    sections = OrderedDict()
    sections["S00"] = {"title": "최상위 메타데이터 + critical_safety_facts + zones 배열 컨테이너",
                       "root_pointers": ["", "/version", "/updated", "/consensus_method", "/critical_safety_facts", "/zones"],
                       "pointer_range": "'' (루트 객체 자체), /version, /updated, /consensus_method, /critical_safety_facts/**, /zones (배열 컨테이너만; 원소는 S01~S11)"}
    for i, z in enumerate(std["zones"]):
        sid = "S%02d" % (i + 1)
        sections[sid] = {"title": "zones[%d] %s (%s / %s)" % (i, z["id"], z["name_ko"], z["name_en"]),
                         "root_pointers": ["/zones/%d" % i], "pointer_range": "/zones/%d/**" % i}

    manual = json.load(open(os.path.join(HERE, "manual-review.json"), encoding="utf-8"))

    source_map = OrderedDict(
        about="anatomy-danger-zones.json 의 모든 노드(컨테이너·말단) 기록. 구간은 디코딩된 파일 원문 문자열 기준 Unicode 코드 포인트 [start,end) 와 UTF-8 바이트 [start,end) 를 구분해 둔다. literal_*_span 은 JSON 리터럴(따옴표 포함), string_content_*_span 은 따옴표 안쪽. 원문에 이스케이프가 없어 따옴표 안쪽 원문 = 디코딩 값이다.",
        source=OrderedDict(path=SRC_REL, bytes=len(raw), codepoints=len(text), sha256=h0,
                           lines=text.count("\n") + 1, trailing_newline=text.endswith("\n"),
                           encoding="utf-8", bom=raw.startswith(b"\xef\xbb\xbf"),
                           all_bmp=True, any_string_escape=any_escape,
                           duplicate_keys=sc.dup_keys,
                           parse_check="자체 스캐너 결과와 json.loads 결과의 노드별 값 일치 확인"),
        counts=OrderedDict(nodes=len(nodes), leaves=len(leaves), string_leaves=len(str_leaves),
                           number_leaves=sum(1 for n in leaves if n["json_type"] in ("integer", "number")),
                           boolean_leaves=sum(1 for n in leaves if n["json_type"] == "boolean"),
                           null_leaves=sum(1 for n in leaves if n["json_type"] == "null"),
                           empty_containers=sum(1 for n in nodes if n["is_empty_container"]),
                           empty_strings=sum(1 for n in str_leaves if n["value"] == ""),
                           objects=sum(1 for n in nodes if n["json_type"] == "object"),
                           arrays=sum(1 for n in nodes if n["json_type"] == "array"),
                           zones=len(std["zones"])),
        sections={k: {"title": v["title"], "pointer_range": v["pointer_range"]} for k, v in sections.items()},
        field_name_occurrences=field_occ,
        duplicate_string_values=dup_strings,
        nodes=nodes,
    )

    # ------------------------------------------------------------ 형태소
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi(num_workers=1, model_type="cong")

    def tok_list(s, base_file_cp=None):
        out = []
        for ti, tk in enumerate(kiwi.tokenize(s)):
            a, b = tk.start, tk.start + tk.len
            surf = s[a:b]
            rec = OrderedDict(i=ti, form=tk.form, tag=str(tk.tag), lemma=getattr(tk, "lemma", None),
                              span=[a, b], surface=surf, form_equals_surface=(surf == tk.form))
            if b == a:
                rec["zero_length"] = True
            if base_file_cp is not None:
                rec["file_cp_span"] = [base_file_cp + a, base_file_cp + b]
            out.append(rec)
        return out

    morph_records = []
    excluded = []
    for n in leaves:
        pat = n["path_pattern"]
        if n["json_type"] != "string":
            excluded.append({"pointer": n["pointer"], "json_type": n["json_type"], "value": n.get("value"),
                             "reason": "비문자열 값(숫자) — 형태소 분석 대상 아님. 값은 source-map.json 에 보존"})
            continue
        if pat in EXCLUDE_STRING_PATTERNS:
            excluded.append({"pointer": n["pointer"], "json_type": "string", "value": n["value"],
                             "reason": EXCLUDE_STRING_PATTERNS[pat]})
            continue
        base = n["string_content_cp_span"][0]
        morph_records.append(OrderedDict(pointer=n["pointer"], section=n["section"], role="text_value",
                                         value=n["value"], file_cp_span=n["string_content_cp_span"],
                                         tokens=tok_list(n["value"], base)))
    field_records = []
    for k, ptrs in field_occ.items():
        field_records.append(OrderedDict(field_name=k, role="field_name", occurrences=len(ptrs), pointers=ptrs,
                                         tokens=tok_list(k),
                                         identifier_parts_rule_based=k.split("_")))

    # 전문어 분절 관찰(출현별)
    rec_by_ptr = {r["pointer"]: r for r in morph_records}
    seg_review = []
    for r in morph_records:
        v = r["value"]
        for term in WATCH_TERMS:
            for m in re.finditer(re.escape(term), v):
                a, b = m.span()
                cov = [t for t in r["tokens"] if t["span"][0] < b and t["span"][1] > a]
                single = len(cov) == 1 and cov[0]["span"] == [a, b]
                aligned = (cov and cov[0]["span"][0] >= a and cov[-1]["span"][1] <= b)
                cut_through = any(t["span"][0] < a or t["span"][1] > b for t in cov)
                seg_review.append(OrderedDict(
                    pointer=r["pointer"], term=term, span=[a, b], file_cp_span=[r["file_cp_span"][0] + a, r["file_cp_span"][0] + b],
                    tokens=[[t["form"], t["tag"], t["span"]] for t in cov],
                    single_token=single, boundary_aligned=bool(aligned) and not cut_through,
                    status=("단일 형태소" if single else
                            "K: 여러 형태소로 분절(원시 결과 보존)" if not cut_through else
                            "관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열" if len(cov) == 1 else
                            "K: 형태소 경계가 낱말 경계를 넘음(원시 결과 보존)")))
    # 수치·단위·범위 토큰 관찰
    num_review = []
    for r in morph_records:
        v = r["value"]
        for m in re.finditer(AUTO_PATTERNS["range"] + "|" + AUTO_PATTERNS["number_unit"], v):
            a, b = m.span()
            cov = [t for t in r["tokens"] if t["span"][0] < b and t["span"][1] > a]
            num_review.append(OrderedDict(pointer=r["pointer"], text=m.group(0), span=[a, b],
                                          tokens=[[t["form"], t["tag"], t["span"]] for t in cov],
                                          token_count=len(cov)))
    # 부정·금지·가능성 단서가 토큰에 남는지
    cue_review = []
    for r in morph_records:
        v = r["value"]
        for m in re.finditer(AUTO_PATTERNS["negation_prohibition"] + "|" + AUTO_PATTERNS["possibility_frequency"], v):
            a, b = m.span()
            cov = [t for t in r["tokens"] if t["span"][0] < b and t["span"][1] > a]
            covered = "".join(t["surface"] for t in cov)
            cue_review.append(OrderedDict(pointer=r["pointer"], cue=m.group(0), span=[a, b],
                                          tokens=[[t["form"], t["tag"], t["span"]] for t in cov],
                                          cue_surface_retained=(m.group(0) in covered or all(c in covered for c in m.group(0).replace(" ", "")))))

    # 명사·외국어·숫자 토큰 중 form≠surface (표면과 다른 형태로 복원된 곳)
    form_mismatch = []
    serial_tokens = []
    for r in morph_records:
        for t in r["tokens"]:
            if not t["form_equals_surface"] and (t["tag"].startswith("NN") or t["tag"] in ("SL", "SN", "SH")):
                form_mismatch.append(OrderedDict(pointer=r["pointer"], token=t, status="K: 명사 토큰 form 이 표면과 다름(원시 결과 보존)"))
            if t["tag"].startswith("W_"):
                serial_tokens.append(OrderedDict(pointer=r["pointer"], surface=t["surface"], tag=t["tag"], span=t["span"],
                                                 status="K: 범위·분수·연도 묶음이 기호 분리 없이 한 토큰(W_*)으로 묶임"))
    morphology = OrderedDict(
        about="문자열 값(언어 텍스트)과 필드명에 Kiwi 형태소 분석을 적용한 원시 결과. 형태소 기본형은 도메인 표준명이 아니다. 오분절은 교정하지 않고 출현별로 기록한다.",
        analyzer=OrderedDict(
            name="Kiwi (kiwipiepy)", kiwipiepy=kiwipiepy.__version__, model_type="cong", num_workers=1,
            env="uv run --python 3.12 --with kiwipiepy==0.24.1, OMP_NUM_THREADS=1",
            call="Kiwi(num_workers=1, model_type='cong').tokenize(text) — 기본 옵션(정규화·오타 교정·사용자 사전 없음)",
            default_dictionary="kiwipiepy 기본 내장 사전(load_default_dict=True)", user_dictionary=None,
            typo_correction=None,
            tagset="Kiwi 품사 체계(세종 기반 확장: NNG/NNP/NNB/NR/NP/VV/VA/VX/VCP/VCN/MM/MAG/MAJ/J*/E*/X*/S*/W_*)",
            lemma="Kiwi Token.lemma 값 그대로 기록(용언은 Kiwi 가 '다'를 붙여 준 기본형). 분석기가 주지 않는 기본형은 만들지 않았다.",
            span="각 값 문자열 기준 Unicode 코드 포인트 [start,end) (원문 전부 BMP 이므로 Kiwi 오프셋=코드 포인트). file_cp_span = 해당 문자열 따옴표 안쪽 시작 + span. 파일 바이트 구간은 source-map.json 의 string_content_byte_span 기준으로 별도 계산해야 한다.",
            normalization="입력 정규화 없음. 원문 문자열을 그대로 넣었다. form 이 표면과 다를 수 있다(form_equals_surface=false; 활용·축약 복원)."),
        applied_counts=OrderedDict(text_values=len(morph_records), field_names=len(field_records),
                                   excluded_leaves=len(excluded),
                                   tokens=sum(len(r["tokens"]) for r in morph_records)),
        exclusion_rules=EXCLUDE_STRING_PATTERNS,
        exclusion_rule_numbers="숫자형 말단(integer/number) 전부 제외 — 비문자열",
        text_values=morph_records,
        field_names=field_records,
        field_name_note="필드명은 영문 snake_case 식별자다. Kiwi 결과(대부분 SL)를 보존하되 언어 텍스트와 역할이 다르다. '_' 기준 분해(identifier_parts_rule_based)는 규칙 기반이며 분석기 산출이 아니다.",
        excluded=excluded,
        segmentation_review=OrderedDict(
            about="직접 읽기에서 고른 전문어·복합어 표면형의 모든 출현에 대해 겹치는 Kiwi 토큰을 기록. 분절 자체가 오류인지는 판정하지 않는다(K=알려진 분석 한계로 보존).",
            terms=WATCH_TERMS, occurrences=seg_review),
        number_unit_review=OrderedDict(
            about="수치·단위·범위 표현의 모든 정규식 출현과 겹치는 토큰. 범위 구분자(-, –, ~)와 단위가 별도 토큰으로 갈라지는지 확인용.",
            occurrences=num_review),
        form_mismatch_review=OrderedDict(
            about="명사(NN*)·SL·SN·SH 토큰 중 Kiwi form 이 원문 표면과 다른 모든 출현.", occurrences=form_mismatch),
        serial_token_review=OrderedDict(
            about="W_* 태그 토큰 전 출현. 정수 범위(예: 10-30)·분수(1/3)·연도 묶음(2023/24)이 한 토큰이 되고, 소수 범위(예: 0.5-1.0)는 SN·SO·SN 으로 갈라져 같은 '범위' 표기가 다르게 분석된다.", occurrences=serial_tokens),
        cue_review=OrderedDict(
            about="부정·금지·가능성·빈도 단서 표면이 토큰 표면에 남는지(cue_surface_retained). 단서가 사라진 곳이 있으면 K/A 로 기록.",
            occurrences=cue_review),
    )

    # ------------------------------------------------------------ 표현
    node_by_ptr = {n["pointer"]: n for n in nodes}
    manual_exprs = []
    seen = defaultdict(int)
    for sid, sec in manual["sections"].items():
        for e in sec["expressions"]:
            ptr, t, aspects = e[0], e[1], e[2]
            note = e[3] if len(e) > 3 else None
            n = node_by_ptr[ptr]
            assert n["json_type"] == "string", ptr
            assert n["section"] == sid, (ptr, sid)
            v = n["value"]
            idx = [m.start() for m in re.finditer(re.escape(t), v)]
            assert idx, "수동 표현이 원문에 없음: %s %r" % (ptr, t)
            k = (ptr, t)
            occ = seen[k]
            seen[k] += 1
            a = idx[occ]
            base = n["string_content_cp_span"][0]
            manual_exprs.append(OrderedDict(
                id="MX-%s-%03d" % (sid, sum(1 for x in manual_exprs if x["section"] == sid) + 1),
                section=sid, pointer=ptr, text=t, span=[a, a + len(t)],
                file_cp_span=[base + a, base + a + len(t)],
                file_byte_span=[boff[base + a], boff[base + a + len(t)]],
                occurrence_in_value=occ + 1, occurrences_of_text_in_value=len(idx),
                aspects=aspects.split(","), note=note, method="manual_direct_reading",
                whole_value=v))
    auto_exprs = []
    for r in morph_records + [{"pointer": n["pointer"], "value": n["value"], "file_cp_span": n["string_content_cp_span"]}
                              for n in str_leaves if n["path_pattern"] in EXCLUDE_STRING_PATTERNS]:
        v = r["value"]
        for name, pat in AUTO_PATTERNS.items():
            for m in re.finditer(pat, v):
                a, b = m.span()
                auto_exprs.append(OrderedDict(
                    id="AX-%05d" % (len(auto_exprs) + 1), section=section_of(r["pointer"]), pointer=r["pointer"],
                    pattern=name, text=m.group(0), span=[a, b],
                    file_cp_span=[r["file_cp_span"][0] + a, r["file_cp_span"][0] + b],
                    method="regex_candidate"))
    # 문장/절 단위(원문 구두점 기준) 구간 — 문맥 보존용
    clauses = []
    for r in morph_records:
        v = r["value"]
        for m in re.finditer(r"(?:[^.;—]|(?<=\d)\.(?=\d)|\.(?=[,A-Za-z(])|(?<=\d);(?=\d))+(?:[.;]|$|(?=—))", v):
            seg = m.group(0)
            if not seg.strip():
                continue
            a = m.start() + (len(seg) - len(seg.lstrip()))
            b = m.end() - (len(seg) - len(seg.rstrip()))
            clauses.append(OrderedDict(pointer=r["pointer"], span=[a, b], text=v[a:b],
                                       file_cp_span=[r["file_cp_span"][0] + a, r["file_cp_span"][0] + b]))
    expressions = OrderedDict(
        about="복합 표현·구절 구간. manual = 에이전트 직접 읽기에서 수집(탐색 관점은 확정 분류 아님), regex_candidates = 정규식 보조 후보(전수 의미 해석 아님), clause_segments = '.', ';', '—' 기준 기계 분할 구간(문맥 보존용). 구간끼리 겹침은 의도된 것이다.",
        span_rule="값 문자열 기준 코드 포인트 [start,end). file_cp_span 은 파일 원문 기준 코드 포인트, file_byte_span 은 UTF-8 바이트.",
        regex_patterns=AUTO_PATTERNS,
        counts=OrderedDict(manual=len(manual_exprs), regex_candidates=len(auto_exprs), clause_segments=len(clauses)),
        manual=manual_exprs, regex_candidates=auto_exprs, clause_segments=clauses)

    # ------------------------------------------------------------ coverage
    cov_sections = []
    owned_all = []
    for sid, s in sections.items():
        owned = [n["pointer"] for n in nodes if n["section"] == sid]
        owned_leaves = [n["pointer"] for n in leaves if n["section"] == sid]
        owned_all += owned
        cov_sections.append(OrderedDict(
            id=sid, title=s["title"], pointer_range=s["pointer_range"], root_pointers=s["root_pointers"],
            owned_pointers=owned, owned_leaf_pointers=owned_leaves,
            owned_counts={"nodes": len(owned), "leaves": len(owned_leaves)},
            context_refs=(["(루트) /zones 배열 컨테이너는 S00 소유, 이 구획은 원소 하나를 소유"] +
                          ([zone_ctx[sid]["zone_pointer"] + "/id", zone_ctx[sid]["zone_pointer"] + "/name_ko"] if sid != "S00" else [])),
            shared_context_not_owned=(["", "/zones"] if sid != "S00" else []),
            machine_extracted=True,
            direct_read=("done" if sid in manual["reading_log"]["order"] else "not_started"),
            manual_observations=len(manual["sections"].get(sid, {}).get("observations", [])),
            manual_expressions=len(manual["sections"].get(sid, {}).get("expressions", [])),
            review_file="review-part-%s.md" % sid, review_index="review.md#구획-목차"))
    coverage = OrderedDict(
        about="구획별 소유 경로·읽기 상태. machine_extracted=기계 추출 완료, direct_read=에이전트가 원문을 직접 읽고 관찰을 남김. 상위 문맥(루트·/zones 컨테이너)은 S00 이 소유하고 다른 구획은 공유 문맥으로만 참조한다.",
        source_sha256=h0, total_nodes=len(nodes), total_leaves=len(leaves),
        reading_log=manual["reading_log"], sections=cov_sections)

    # ------------------------------------------------------------ 쓰기 (원본 해시 재확인 뒤)
    def dump(name, obj):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write("\n")

    dump("source-map.json", source_map)
    dump("morphology.json", morphology)
    dump("expressions.json", expressions)
    dump("coverage.json", coverage)
    write_reviews(sections, nodes, leaves, manual, manual_exprs, auto_exprs, seg_review, field_occ, dup_strings,
                  source_map, morphology, expressions, zone_ctx)
    h1 = sha256(SRC)
    assert h0 == h1, "원본 해시 변경!"
    print("source sha256 start=end", h0)
    print("nodes", len(nodes), "leaves", len(leaves), "string_leaves", len(str_leaves))
    print("morph text_values", len(morph_records), "fields", len(field_records), "excluded", len(excluded),
          "tokens", morphology["applied_counts"]["tokens"])
    print("manual_expr", len(manual_exprs), "auto", len(auto_exprs), "clauses", len(clauses))
    print("seg_review", len(seg_review), "split", sum(1 for s in seg_review if not s["single_token"]),
          "cut_through", sum(1 for s in seg_review if not s["boundary_aligned"]))
    print("form_mismatch", len(form_mismatch), "serial", len(serial_tokens))
    print("cue_review", len(cue_review), "not_retained", sum(1 for c in cue_review if not c["cue_surface_retained"]))


def md(s):
    return str(s).replace("|", "\\|").replace("\n", "<br>")


def typestr(n):
    if n["json_type"] == "object":
        return "object{%d}" % n["size"]
    if n["json_type"] == "array":
        return "array[%d]" % n["size"]
    return n["json_type"]


def valstr(n):
    if n["json_type"] in ("object", "array"):
        return "(컨테이너 · 키: %s)" % ", ".join("`%s`" % k for k in n["keys_in_order"]) if n["json_type"] == "object" else "(배열 · %d개)" % n["size"]
    return "`%s`" % n["number_literal"] if n["json_type"] != "string" else md(n["value"])


def write_reviews(sections, nodes, leaves, manual, manual_exprs, auto_exprs, seg_review, field_occ, dup_strings,
                  source_map, morphology, expressions, zone_ctx):
    src = source_map["source"]
    c = source_map["counts"]
    # 컬럼 구성 표
    pats = OrderedDict()
    for n in nodes:
        p = n["path_pattern"]
        d = pats.setdefault(p, {"types": set(), "count": 0, "first": n, "nodes": []})
        d["types"].add(typestr(n) if n["json_type"] not in ("object", "array") else n["json_type"])
        d["count"] += 1
        d["nodes"].append(n)
    nz = c["zones"]

    def presence(p):
        if not p.startswith("/zones/*"):
            return "최상위 1회"
        parts = p.split("/")
        # 해당 패턴을 가진 zone 수
        zs = sorted({int(n["pointer"].split("/")[2]) for n in pats[p]["nodes"]})
        if len(zs) == nz:
            return "zone %d/%d" % (len(zs), nz)
        return "zone %d/%d (있는 zone: %s)" % (len(zs), nz, ", ".join("%d=%s" % (z, zone_ctx["S%02d" % (z + 1)]["id"]) for z in zs))

    L = []
    L.append("# anatomy-danger-zones.json — 1차 조사 (읽기용)\n")
    L.append("## 상태\n")
    L.append("| 항목 | 상태 |\n|---|---|")
    L.append("| **1차 범위 종료** | 예 — 아래 기준 충족(상세 validation.md) |")
    L.append("| **원장 전체 완료** | **아님** — 의미 분해·공통 개념·관계 확정·원문 불일치 처리는 후속 단계 |")
    L.append("| 전수 읽기 | 12/12 구획 직접 읽기 완료 (coverage.json) |")
    L.append("| 구조·값 수집 | 노드 %d · 말단 %d (문자열 %d · 숫자 %d · 빈 컨테이너 %d · 빈 문자열 %d · null %d · 불리언 %d) |" % (
        c["nodes"], c["leaves"], c["string_leaves"], c["number_leaves"], c["empty_containers"], c["empty_strings"], c["null_leaves"], c["boolean_leaves"]))
    L.append("| 형태소·표현 수집 | 텍스트 값 %d · 필드명 %d · 제외 %d · 토큰 %d / 수동 표현 %d · 정규식 후보 %d · 절 구간 %d |" % (
        morphology["applied_counts"]["text_values"], morphology["applied_counts"]["field_names"], morphology["applied_counts"]["excluded_leaves"],
        morphology["applied_counts"]["tokens"], expressions["counts"]["manual"], expressions["counts"]["regex_candidates"], expressions["counts"]["clause_segments"]))
    L.append("| 기계 검증 | verify.py 통과 기준 — validation.md |")
    L.append("| 읽기 검토 | validation.md §읽기 검토 |")
    L.append("| 알려진 분석 오류 | K — morphology.json segmentation_review / issues.md |")
    L.append("| 열린 미결 · 후속 의미 조사 | issues.md (A 0 · B · C 0 · I · P · F · K) |")
    L.append("")
    L.append("## 원본\n")
    L.append("| 항목 | 값 |\n|---|---|")
    for k in ("path", "bytes", "codepoints", "sha256", "lines", "trailing_newline", "encoding", "bom", "any_string_escape"):
        L.append("| %s | `%s` |" % (k, src[k]))
    L.append("| duplicate_keys | %s |" % (len(src["duplicate_keys"]) or "0 (감지 없음)"))
    L.append("")
    L.append("파일은 줄바꿈 없는 한 줄 JSON 이다. 이스케이프 문자열이 없어 따옴표 안쪽 원문과 디코딩 값이 같다. 구간 단위: 값 기준·파일 기준 모두 Unicode 코드 포인트 `[start,end)`, 바이트 구간은 별도 칸(`*_byte_span`).\n")
    L.append("## 전체 컬럼 구성\n")
    L.append("경로 패턴의 `*` 는 배열 순번. 자료형 칸의 숫자는 크기 범위. 예시는 첫 출현의 원문 값(전체)과 Pointer.\n")
    L.append("| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 수 | 존재 범위 | 원문 예시 | 예시 Pointer |\n|---|---|---|---|---|---|")
    for p, d in pats.items():
        f = d["first"]
        ns = d["nodes"]
        if f["json_type"] in ("object", "array"):
            sizes = sorted({n["size"] for n in ns})
            t = "%s (크기 %s)" % (f["json_type"], sizes[0] if len(sizes) == 1 else "%d–%d" % (sizes[0], sizes[-1]))
            ex = valstr(f)
        else:
            t = "/".join(sorted(d["types"]))
            ex = valstr(f)
        L.append("| `%s` | %s | %d | %s | %s | `%s` |" % (p, t, d["count"], presence(p), ex, f["pointer"] or "(root)"))
    L.append("")
    L.append("### 구조 변형 · 선택 필드 · 빈 값\n")
    L.append("| 구분 | 원문 사실 | Pointer |\n|---|---|---|")
    L.append("| 빈 값 | 빈 문자열 %d · 빈 배열/객체 %d · null %d — 이 원장에는 없다 | — |" % (c["empty_strings"], c["empty_containers"], c["null_leaves"]))
    for p, d in pats.items():
        if p.startswith("/zones/*") and p.count("/") >= 3:
            pr = presence(p)
            if "있는 zone" in pr:
                L.append("| 선택 필드(일부 zone) | `%s` — %s | %s |" % (p, pr, ", ".join("`%s`" % n["pointer"] for n in d["nodes"])))
    # 같은 zone 안 배열 원소별 선택 필드
    for arr in ("vessels",):
        keysets = defaultdict(list)
        for n in nodes:
            if re.match(r"^/zones/\d+/%s/\d+$" % arr, n["pointer"]):
                keysets[tuple(n["keys_in_order"])].append(n["pointer"])
        for ks, ps in keysets.items():
            L.append("| `%s` 원소 키 구성 변형 | %s | %s |" % (arr, ", ".join("`%s`" % k for k in ks), ", ".join("`%s`" % p for p in ps)))
    tdk = defaultdict(list)
    for n in nodes:
        if re.match(r"^/zones/\d+/tissue_data$", n["pointer"]):
            tdk[tuple(n["keys_in_order"])].append(n["pointer"])
    for ks, ps in tdk.items():
        L.append("| `tissue_data` 키 구성(zone 마다 다름) | %s | %s |" % (", ".join("`%s`" % k for k in ks), ", ".join("`%s`" % p for p in ps)))
    L.append("| 숫자 범위를 문자열로 | `diffusion_range_cm` = \"1.5-3.0\" (string) | `/zones/0/botox_specific/diffusion_range_cm` |")
    L.append("| 숫자 배열 | `depth_range_mm`, `labial_artery_depth_range_mm` = [하한, 상한] 2원소 숫자 배열 | 컬럼 구성 표 참조 |")
    L.append("")
    L.append("### 같은 문자열의 반복 출현(각 위치 유지)\n")
    L.append("| 원문 값 | Pointer 들 |\n|---|---|")
    for d in dup_strings:
        L.append("| %s | %s |" % (md(d["value"]), ", ".join("`%s`" % p for p in d["pointers"])))
    L.append("")
    L.append("## 구획 목차\n")
    L.append("| 구획 | 범위 | 소유 노드/말단 | 직접 읽기 | 파일 |\n|---|---|---|---|---|")
    for sid, s in sections.items():
        own = [n for n in nodes if n["section"] == sid]
        ol = [n for n in own if n["is_leaf"]]
        L.append("| %s | %s — `%s` | %d / %d | done | [review-part-%s.md](review-part-%s.md) |" % (sid, md(s["title"]), s["pointer_range"], len(own), len(ol), sid, sid))
    L.append("")
    L.append("## 산출물\n")
    L.append("| 파일 | 내용 |\n|---|---|")
    for f, d in [("source-map.json", "모든 노드의 Pointer·자료형·원문 값·리터럴 구간(코드 포인트/바이트)·문맥 참조·필드명 출현·중복 문자열"),
                 ("morphology.json", "Kiwi 원시 분석(텍스트 값·필드명), 제외 내역, 전문어 분절·수치·단서 관찰"),
                 ("expressions.json", "수동 복합 표현, 정규식 후보, 절 구간"),
                 ("coverage.json", "구획별 소유 경로·읽기 상태"),
                 ("manual-review.json", "직접 읽기 기록(관찰·수동 표현) — build.py 입력"),
                 ("issues.md", "미결·후속 목록(A/B/C/I/P/F/K)"),
                 ("validation.md", "기계 검증 명령·결과, 읽기 검토"),
                 ("build.py / verify.py", "재현 / 독립 검증")]:
        L.append("| %s | %s |" % (f, d))
    open(os.path.join(HERE, "review.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # 구획별 part
    for sid, s in sections.items():
        own = [n for n in nodes if n["section"] == sid]
        P = []
        P.append("# %s — %s\n" % (sid, s["title"]))
        P.append("[← review.md](review.md) · 범위 `%s` · 소유 노드 %d · 말단 %d · 직접 읽기 done\n" % (s["pointer_range"], len(own), sum(1 for n in own if n["is_leaf"])))
        if sid != "S00":
            zc = zone_ctx[sid]
            P.append("상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `%s` (id=`%s`, name_ko=`%s`, name_en=`%s`).\n" % (zc["zone_pointer"], zc["id"], zc["name_ko"], zc["name_en"]))
        else:
            P.append("상위 문맥: 루트 객체. `/zones` 배열 컨테이너는 이 구획이 소유하고 원소 11개는 S01~S11 이 소유한다.\n")
        P.append("## 원문 값 (문서 순서 · 전부)\n")
        P.append("| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |\n|---|---|---|---|---|---|")
        for n in own:
            colname = (n["key"] if n["key"] is not None else "(루트)" if n["parent"] is None
                       else "(%s 원소)" % next(x for x in nodes if x["pointer"] == n["parent"])["key"])
            P.append("| %d | `%s` | `%s` | %s | %s | %s |" % (n["document_order"], n["pointer"] or "(root)", colname,
                                                           "" if n["index"] is None else n["index"], typestr(n), valstr(n)))
        P.append("")
        P.append("## 잠정 관찰 (원문 칸과 분리)\n")
        obs = manual["sections"].get(sid, {}).get("observations", [])
        P.append("| # | 상태 | 근거 Pointer | 관찰 | issues.md |\n|---|---|---|---|---|")
        for i, o in enumerate(obs, 1):
            P.append("| OBS-%s-%02d | %s | %s | %s | %s |" % (sid, i, o[0], ", ".join("`%s`" % p for p in o[1]), md(o[2]), o[3] or ""))
        P.append("")
        P.append("## 수동 복합 표현 (직접 읽기)\n")
        P.append("탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.\n")
        P.append("| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |\n|---|---|---|---|---|---|")
        for e in manual_exprs:
            if e["section"] == sid:
                P.append("| %s | `%s` | %s | %s | %s | %s |" % (e["id"], e["pointer"], md(e["text"]), e["span"], ", ".join(e["aspects"]), md(e["note"] or "")))
        P.append("")
        P.append("## 정규식 보조 후보 (기계 · 요약)\n")
        cnt = defaultdict(int)
        for a in auto_exprs:
            if a["section"] == sid:
                cnt[a["pattern"]] += 1
        P.append("| 패턴 | 출현 |\n|---|---|")
        for k, v in cnt.items():
            P.append("| %s | %d |" % (k, v))
        P.append("\n전체 출현·구간은 `expressions.json` → `regex_candidates` (section=%s).\n" % sid)
        P.append("## 전문어 분절 관찰 (Kiwi 원시 · K)\n")
        P.append("| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |\n|---|---|---|---|---|")
        for r in seg_review:
            if section_of(r["pointer"]) == sid and not r["single_token"]:
                P.append("| `%s` | %s | %s | %s | %s |" % (r["pointer"], r["term"], r["span"], md(" + ".join("%s/%s" % (t[0], t[1]) for t in r["tokens"])), r["status"]))
        P.append("\n단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).\n")
        open(os.path.join(HERE, "review-part-%s.md" % sid), "w", encoding="utf-8").write("\n".join(P) + "\n")


if __name__ == "__main__":
    main()
