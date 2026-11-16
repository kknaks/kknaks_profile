"""problem-combos 1차 수집 재현 스크립트.

레포 루트에서:
  uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/problem-combos/build.py

원본은 읽기만 한다. 출력은 이 폴더 안에만 쓴다.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "../../../phub-recommend/bronze/phub-ledger/problem-combos.json"))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json"
MANUAL = os.path.join(HERE, "manual")


def out(name, obj):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        if isinstance(obj, str):
            f.write(obj)
        else:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write("\n")


def esc_ptr(k):
    return k.replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 위치 추적 파서
class Parser:
    """원문 문자열 위에서 값마다 [start,end) 코드포인트 구간을 기록한다. 중복 키를 감지한다."""

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []  # 문서 순서
        self.dups = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        s = self.i
        assert self.t[s] == '"'
        j = s + 1
        while True:
            c = self.t[j]
            if c == "\\":
                j += 2
                continue
            if c == '"':
                break
            j += 1
        self.i = j + 1
        lit = self.t[s:self.i]
        return json.loads(lit), s, self.i

    def value(self, ptr, parent, key):
        self.ws()
        c = self.t[self.i]
        s = self.i
        node = {"pointer": ptr, "parent": parent, "key": key}
        self.nodes.append(node)
        if c == "{":
            self.i += 1
            keys = []
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke = self.string()
                    if k in keys:
                        self.dups.append({"pointer": ptr, "key": k, "key_literal_span": [ks, ke]})
                    keys.append(k)
                    node.setdefault("key_literal_spans", []).append({"key": k, "span": [ks, ke]})
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    self.value(ptr + "/" + esc_ptr(k), ptr, k)
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node.update(type="object", keys=keys, length=len(keys))
        elif c == "[":
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(ptr + "/" + str(n), ptr, n)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            node.update(type="array", length=n)
        elif c == '"':
            v, s, e = self.string()
            node.update(type="string", value=v, content_span=[s + 1, e - 1])
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.t, self.i)
            self.i = m.end()
            v = json.loads(m.group(0))
            node.update(type={bool: "boolean", type(None): "null"}.get(type(v), "number"), value=v)
        node["literal_span"] = [s, self.i]
        return node


def main():
    raw_bytes = open(SRC, "rb").read()
    sha = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode("utf-8")
    p = Parser(text)
    p.value("", None, None)
    p.ws()
    assert p.i == len(text), "trailing data"
    assert json.loads(text) is not None
    # 코드포인트 -> 바이트 오프셋
    boff = [0]
    for ch in text:
        boff.append(boff[-1] + len(ch.encode("utf-8")))
    non_bmp = [i for i, ch in enumerate(text) if ord(ch) > 0xFFFF]
    has_escape = "\\" in text

    for n in p.nodes:
        s, e = n["literal_span"]
        n["literal_byte_span"] = [boff[s], boff[e]]
        n["empty_container"] = n["type"] in ("object", "array") and n["length"] == 0
        n["is_leaf"] = n["type"] not in ("object", "array") or n["empty_container"]
        for kl in n.get("key_literal_spans", []):
            kl["byte_span"] = [boff[kl["span"][0]], boff[kl["span"][1]]]
    nodes = {n["pointer"]: n for n in p.nodes}
    data = json.loads(text)

    # ---------------------------------------------------------- 구획
    combos = data["combos"]
    segments = [{"segment_id": "S0", "scope": "루트 객체·메타데이터(version/updated/description)와 /combos 배열 컨테이너",
                 "owned_root": None}]
    for i, c in enumerate(combos):
        segments.append({"segment_id": f"S{i+1}", "scope": f"/combos/{i} ({c['problem_id']} {c['problem']}) 전체",
                         "owned_root": f"/combos/{i}"})

    def seg_of(ptr):
        m = re.match(r"^/combos/(\d+)(/|$)", ptr)
        return f"S{int(m.group(1))+1}" if m else "S0"

    for n in p.nodes:
        n["segment_id"] = seg_of(n["pointer"])
        # 상위 문맥: 묶음(problem_id·problem)과 패키지(id·name)
        ctx = []
        m = re.match(r"^/combos/(\d+)", n["pointer"])
        if m:
            ci = int(m.group(1))
            ctx += [f"/combos/{ci}/problem_id", f"/combos/{ci}/problem"]
            m2 = re.match(r"^/combos/(\d+)/packages/(\d+)", n["pointer"])
            if m2:
                pj = int(m2.group(2))
                ctx += [f"/combos/{ci}/packages/{pj}/id", f"/combos/{ci}/packages/{pj}/name"]
        n["context_pointers"] = [c for c in ctx if c != n["pointer"]]

    # ---------------------------------------------------------- 형태소
    EXCLUDE = [
        (r"^/version$", "버전 식별자(숫자·점)"),
        (r"^/updated$", "날짜 식별자(ISO 날짜 문자열)"),
        (r"^/combos/\d+/problem_id$", "묶음 ID 코드(P숫자)"),
        (r"^/combos/\d+/packages/\d+/id$", "패키지 ID 코드(P숫자-숫자)"),
        (r"^/combos/\d+/packages/\d+/tier$", "영문 등급 코드(entry/recommended/premium/vip) — tierLabel이 한국어 표시값"),
        (r"^/combos/\d+/packages/\d+/procedures/\d+$", "시술 코드(M숫자) — 정의는 다른 원장"),
    ]
    from kiwipiepy import Kiwi
    import kiwipiepy
    kiwi = Kiwi(num_workers=1, model_type="cong")

    def tok(s):
        res = []
        for t in kiwi.tokenize(s):
            res.append({"form": t.form, "tag": t.tag, "start": t.start, "end": t.start + t.len,
                        "surface": s[t.start:t.start + t.len], "lemma_tool": t.lemma,
                        "base_form_tool": t.base_form, "oov": bool(getattr(t, "oov", False)),
                        "form_equals_surface": t.form == s[t.start:t.start + t.len], "zero_width": t.len == 0})
        return res

    morph_records = []
    for n in p.nodes:
        if n["type"] != "string":
            continue
        rec = {"record_id": f"V{len(morph_records):04d}", "role": "value", "pointer": n["pointer"],
               "segment_id": n["segment_id"], "text": n["value"]}
        reason = next((r for pat, r in EXCLUDE if re.match(pat, n["pointer"])), None)
        if reason:
            rec.update(applied=False, exclude_reason=reason, tokens=[])
        else:
            rec.update(applied=True, tokens=tok(n["value"]))
        morph_records.append(rec)
    field_names = []
    for n in p.nodes:
        for kl in n.get("key_literal_spans", []):
            field_names.append({"key": kl["key"], "owner_pointer": n["pointer"], "key_literal_span": kl["span"],
                                "key_literal_byte_span": kl["byte_span"], "segment_id": seg_of(n["pointer"] + "/" + esc_ptr(kl["key"]))})
    uniq_keys = sorted({f["key"] for f in field_names})
    field_tok = {k: tok(k) for k in uniq_keys}

    # 알려진 오분절 — 직접 읽기에서 확인한 전문어 표면형. 토큰 경계가 표현 내부에 떨어지면 출현별로 기록.
    TERMS = ["스킨부스터", "스킨보톡스", "히알루로니다아제", "폴리뉴클레오타이드", "실루엣소프트", "슈링크유니버스",
             "더블로골드", "리쥬란", "쥬비덤", "이브아르", "보툴렉스", "울쎄라", "올리지오", "포텐자", "인트라셀",
             "피코슈어", "피코웨이", "레블라이트", "피코레이저", "니들RF", "실리프팅", "SMAS층", "Nd:YAG", "TGF-β",
             "PN/PDRN", "PRP/SB", "CO2", "1클", "골든루틴", "트라넥사민산", "저플루언스", "바이오스티뮬레이터",
             "스컬트라", "광경근", "멜라노사이트", "멜라스마", "프락셔널", "프락셀", "턱필러", "사각턱", "하안면",
             "동적주름", "정적주름", "볼륨손실", "콜라겐감소", "열응고", "미세열손상", "DNA회복", "모공벽", "턱폭",
             "V라인", "골든루틴", "풀패키지", "열손상", "자가혈", "접촉냉각",
             "안내", "심부", "이중", "PDRN이", "가능성"]
    # 원문 읽기에서 확인한 품사 오분석 판정용: 이 태그가 표현 안에 나오면 '품사 오분석'
    NOUNISH = {"NNG", "NNP", "NNB", "SL", "SN", "SH", "SW", "SO", "SP", "XSN", "JKS"}
    IMPACT = {"안내": "안/MAG(부정 부사)+내/VV — 부정 표현 탐색 시 오탐. 원문은 '주의 안내'(명사)",
              "리쥬란": "제품명이 리쥬/NNP+이/VCP+란/ETM 으로 분해 — 제품명 표면형 복원 필요",
              "하안면": "하/VV 또는 하안/NNP 로 분해 — 부위 표현 손실",
              "심부": "심/XR+부 — 층 표현 손실",
              "이중": "이/MM(관형사)+중 — '이중'(이중 타겟) 수량 의미 손실",
              "PDRN이": "주격조사 '이'를 MM(관형사)으로 분석",
              "니들RF": "니들/NNP+RF/SL 또는 니/NP+들/XSN+RF — 시술명 분해",
              "광경근": "광/경/근 세 조각 — 해부 용어 손실"}
    TERMS = list(dict.fromkeys(TERMS))
    known_errors = []
    for rec in morph_records:
        if not rec["applied"]:
            continue
        s = rec["text"]
        for term in TERMS:
            for m in re.finditer(re.escape(term), s):
                a, b = m.start(), m.end()
                inside = [t for t in rec["tokens"] if t["start"] < b and t["end"] > a]
                cuts = sorted({t["start"] for t in inside if a < t["start"] < b} | {t["end"] for t in inside if a < t["end"] < b})
                overflow = [t for t in inside if t["start"] < a or t["end"] > b]
                bad_tag = [t for t in inside if t["tag"] not in NOUNISH]
                if term == "PDRN이":
                    bad_tag = [t for t in inside if t["form"] == "이" and t["tag"] == "MM"]
                    cuts = []
                if term == "가능성" and not bad_tag:
                    continue
                if cuts or overflow or bad_tag:
                    known_errors.append({"status": "K", "record_id": rec["record_id"], "pointer": rec["pointer"],
                                         "span": [a, b], "text": term,
                                         "raw_tokens": [f"{t['form']}/{t['tag']}[{t['start']},{t['end']})" for t in inside],
                                         "issue": "품사 오분석" if bad_tag else ("복합 표현 분리(명사 계열 조각)" if cuts else "토큰이 표현 경계를 넘음"),
                                         "impact": IMPACT.get(term, "표면형 단위 개념 후보 추출 시 조각 결합 필요 — 기본형은 도메인 표준명이 아님")})
    # 수식·조건·부정 형태 관찰: 부정 부사/형용사 '안'·'없'·'않'과 '수 있' 의 출현 구간을 토큰 기준으로 기록(보조)
    MOD_TAGS = {"MAG": "일반부사", "MAJ": "접속부사", "VA": "형용사", "VCN": "부정지정사", "EC": "연결어미", "XSA": "형용사파생접미사"}
    modifier_tokens = []
    for rec in morph_records:
        for t in rec["tokens"]:
            if t["tag"] in MOD_TAGS or t["form"] in ("안", "않", "없", "못") or t["tag"].startswith("VA"):
                modifier_tokens.append({"record_id": rec["record_id"], "pointer": rec["pointer"], "span": [t["start"], t["end"]],
                                        "form": t["form"], "tag": t["tag"]})

    morphology = {
        "source": {"path": SRC_REL, "sha256": sha},
        "analyzer": {"name": "kiwipiepy", "version": kiwipiepy.__version__, "model_type": "cong", "num_workers": 1,
                     "user_dictionary": None, "options": "Kiwi(num_workers=1, model_type='cong'); tokenize(text) 기본값",
                     "pos_tagset": "Kiwi 세종 확장 품사 체계",
                     "run": "uv run --python 3.12 --with kiwipiepy==0.24.1"},
        "span_unit": "디코딩된 원문 문자열(text 필드)의 Unicode 코드포인트 인덱스 [start,end). 원본 파일 위치는 source-map.json의 content_span(코드포인트)·literal_byte_span(바이트)으로 환산",
        "span_note": "원문에 BMP 밖 문자 없음 — kiwi 오프셋과 코드포인트 오프셋 일치(non_bmp_count=%d)" % len(non_bmp),
        "lemma_note": "lemma_tool·base_form_tool은 kiwipiepy가 반환한 값 그대로. 에이전트가 기본형을 생성하지 않음. form은 분석기 정규화형으로 surface(원문 구간)와 다를 수 있음(form_equals_surface=false)",
        "zero_width_note": "kiwipiepy가 원문에 표면형 없이 복원한 형태소(예: '리쥬란'의 이/VCP, '-란' 앞 생략 지정사)는 start==end, surface='' (zero_width=true). 도구 출력 그대로 보존",
        "stopwords_removed": False,
        "exclusions_rule": [{"pointer_pattern": pat, "reason": r} for pat, r in EXCLUDE],
        "value_records": morph_records,
        "field_name_occurrences": field_names,
        "field_name_tokens": field_tok,
        "field_name_note": "필드명은 영문 camelCase/snake_case 식별자. 언어 텍스트와 역할이 달라 별도 기록. 분석 결과(대부분 SL 한 덩어리)는 의미 분석 근거가 아님",
        "known_missegmentations": known_errors,
        "known_missegmentations_method": "직접 읽기에서 확인한 전문어 표면형 목록(TERMS)을 각 값에서 찾아, 토큰 경계가 표현 내부에 있거나 경계를 넘는 출현을 전부 기록. 목록 밖 오분절은 기록되지 않았을 수 있음(K 한계)",
        "modifier_tokens": modifier_tokens,
        "modifier_tokens_method": "품사 MAG/MAJ/VA*/VCN/EC/XSA 및 형태 안/않/없/못 토큰 기록 — 수식·부정·조건 탐색 보조. 수식 대상은 판정하지 않음",
    }

    # ---------------------------------------------------------- 표현
    expressions = []

    def add_expr(ptr, a, b, kind, method, note="", src=None):
        v = nodes[ptr]["value"]
        expressions.append({"expr_id": f"E{len(expressions):04d}", "pointer": ptr, "segment_id": seg_of(ptr),
                            "span": [a, b], "text": v[a:b], "kind": kind, "method": method, "note": note,
                            "file_span": [nodes[ptr]["content_span"][0] + a, nodes[ptr]["content_span"][0] + b],
                            "manual_source": src})

    manual = {}
    for sid in [s["segment_id"] for s in segments]:
        manual[sid] = json.load(open(os.path.join(MANUAL, f"{sid}.json"), encoding="utf-8"))
    manual_problems = []
    for sid, m in manual.items():
        for k, e in enumerate(m["expressions"]):
            ptr = e["pointer"]
            v = nodes[ptr]["value"]
            hits = [x.start() for x in re.finditer(re.escape(e["text"]), v)]
            if not hits:
                manual_problems.append({"segment_id": sid, "index": k, "problem": "원문에 없음", "text": e["text"]})
                continue
            for h in hits:
                add_expr(ptr, h, h + len(e["text"]), e["kind"], "manual", e["note"] + ("" if len(hits) == 1 else f" (같은 값 안 {len(hits)}회 출현 — 각각 기록)"), f"manual/{sid}.json#expressions/{k}")

    # 문장 구간(문맥 보존용) — 언어 텍스트 값의 문장 단위
    sentences = []
    for rec in morph_records:
        if not rec["applied"]:
            continue
        s = rec["text"]
        start = 0
        for m in re.finditer(r"[.!?](?=\s|$)", s):
            seg = s[start:m.end()]
            lead = len(seg) - len(seg.lstrip())
            sentences.append({"pointer": rec["pointer"], "span": [start + lead, m.end()], "text": s[start + lead:m.end()]})
            start = m.end()
        if s[start:].strip():
            lead = len(s[start:]) - len(s[start:].lstrip())
            sentences.append({"pointer": rec["pointer"], "span": [start + lead, len(s)], "text": s[start + lead:]})
    # 자동 후보 패턴
    PATTERNS = [
        ("수량·범위", r"\d+(?:\.\d+)?\s*~\s*\d+(?:\.\d+)?\s*(?:만/회|만|회|일|개월|주|분|%|년|cc|배)?"),
        ("수량·단위", r"(?<![\d~])\d+(?:\.\d+)?\s*(?:만|회|일|개월|주|분|%|년|cc|배|시간|가지|개|살|위|대|총사|차)(?![가-힣]*~)"),
        ("순서 기호 연쇄", r"[^\s.→]+(?:\([^)]*\))?(?:\s*→\s*[^\s.→]+(?:\([^)]*\))?)+"),
        ("괄호 주석", r"[^\s(]*\([^)]*\)"),
        ("대안 표지", r"\S+\s(?:or|또는)\s\S+|[^\s/+]+/[^\s/+]+"),
        ("부정", r"\S*(?:않|없|아닌|아니|안 |못 )\S*"),
        ("가능성", r"\S*(?:수 있|가능)\S*"),
        ("조건 어미", r"\S+(?:시면|으면|하면|이면|려면|시려면)"),
        ("정도·빈도 부사", r"(?<![가-힣A-Za-z])(?:가장|매우|훨씬|더|약간의|거의|드물게|반드시|엄격|확실하게|점점|상대적으로|일시|약)\s\S+"),
    ]
    for rec in morph_records:
        if not rec["applied"]:
            continue
        for kind, pat in PATTERNS:
            for m in re.finditer(pat, rec["text"]):
                if m.end() > m.start() and m.group(0).strip():
                    add_expr(rec["pointer"], m.start(), m.end(), kind, "regex:" + pat)

    expr_doc = {
        "source": {"path": SRC_REL, "sha256": sha},
        "span_unit": "각 값의 디코딩 문자열 코드포인트 [start,end); file_span은 원본 파일 전체 디코딩 텍스트 기준 코드포인트",
        "methods": {"manual": "구획 직접 읽기에서 기록한 표현(manual/S*.json). kind는 탐색 관점 라벨이며 확정 분류 아님",
                    "regex": "보조 후보 추출. 전수 의미 해석 아님. 겹침은 의도된 것(같은 구간이 여러 관점에 걸림)"},
        "expressions": expressions,
        "sentences": sentences,
        "manual_unlocated": manual_problems,
    }

    # ---------------------------------------------------------- source-map
    smap = {
        "source": {"path": SRC_REL, "sha256": sha, "bytes": len(raw_bytes), "codepoints": len(text),
                   "line_count": text.count("\n") + 1, "has_backslash_escape": has_escape, "non_bmp_count": len(non_bmp),
                   "bom": text.startswith("\ufeff"), "duplicate_keys": p.dups},
        "span_units": {"literal_span": "원본 파일 디코딩 텍스트 코드포인트 [start,end) — JSON 리터럴(따옴표 포함)",
                       "literal_byte_span": "원본 파일 UTF-8 바이트 [start,end)",
                       "content_span": "문자열 따옴표 안쪽 코드포인트 [start,end). 원문에 이스케이프가 없어 디코딩 문자열과 1:1"},
        "nodes": p.nodes,
    }

    # ---------------------------------------------------------- coverage
    all_ptrs = [n["pointer"] for n in p.nodes]
    leaf_ptrs = [n["pointer"] for n in p.nodes if n["is_leaf"]]
    cov_segments = []
    for s in segments:
        sid = s["segment_id"]
        owned = [n["pointer"] for n in p.nodes if n["segment_id"] == sid]
        ctx = sorted({c for n in p.nodes if n["segment_id"] == sid for c in n["context_pointers"]} - set(owned))
        m = manual[sid]
        cov_segments.append({
            "segment_id": sid, "scope": s["scope"],
            "pointer_range": [owned[0], owned[-1]],
            "owned_pointers": owned,
            "owned_leaf_pointers": [x for x in owned if nodes[x]["is_leaf"]],
            "context_refs": ctx + (["/description"] if sid != "S0" else []),
            "machine_extracted": True,
            "direct_read": "read",
            "direct_read_record": f"manual/{sid}.json",
            "review_file": f"review-part-{sid}.md",
            "observation_count": len(m["observations"]), "manual_expression_count": len(m["expressions"]),
            "issue_ids": [i["id"] for i in m["issues"]],
        })
    coverage = {"source_sha256": sha, "status": "all_segments_direct_read",
                "all_pointers": all_ptrs, "all_leaf_pointers": leaf_ptrs,
                "ownership_rule": "각 노드(컨테이너·말단)는 정확히 한 구획이 소유. 상위 문맥(problem_id·problem·패키지 id·name, /description)은 context_refs로 공동 참조만 함",
                "segments": cov_segments}

    # ---------------------------------------------------------- review
    def md(v):
        return str(v).replace("|", "\\|").replace("\n", " ")

    def jtype(n):
        return n["type"]

    parts = {}
    for s in cov_segments:
        sid = s["segment_id"]
        m = manual[sid]
        L = [f"# review-part-{sid} — {s['scope']}", "", f"원본: `{SRC_REL}` sha256 `{sha}`", "",
             "## 원문 값", "", "원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.", ""]
        if sid == "S0":
            L += ["| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |", "|---|---|---|---|"]
            for ptr in s["owned_pointers"]:
                n = nodes[ptr]
                val = n.get("value", f"({n['type']} 길이 {n.get('length')}, 키 {n.get('keys','')})")
                L.append(f"| `{md(n['key']) if n['key'] is not None else '(root)'}` | {jtype(n)} | {md(val)} | `{ptr or '(root)'}` |")
        else:
            ci = int(sid[1:]) - 1
            base = f"/combos/{ci}"
            L += [f"### `{base}` 묶음", "", "| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |", "|---|---|---|---|"]
            L.append(f"| (묶음) | object | 키 {md(nodes[base]['keys'])} | `{base}` |")
            for k in ["problem_id", "problem"]:
                n = nodes[f"{base}/{k}"]
                L.append(f"| `{k}` | {n['type']} | {md(n['value'])} | `{n['pointer']}` |")
            L.append(f"| `packages` | array | (길이 {nodes[base+'/packages']['length']}) | `{base}/packages` |")
            for j in range(nodes[base + "/packages"]["length"]):
                pb = f"{base}/packages/{j}"
                L += ["", f"### `{pb}` — {md(nodes[pb+'/id']['value'])} {md(nodes[pb+'/name']['value'])}", "",
                      "| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |", "|---|---|---|---|",
                      f"| (패키지) | object | 키 {md(nodes[pb]['keys'])} | `{pb}` |"]
                for k in nodes[pb]["keys"]:
                    n = nodes[f"{pb}/{esc_ptr(k)}"]
                    if n["type"] == "array":
                        L.append(f"| `{k}` | array | (길이 {n['length']}) | `{n['pointer']}` |")
                        for x in range(n["length"]):
                            e = nodes[f"{n['pointer']}/{x}"]
                            L.append(f"| `{k}[{x}]` | {e['type']} | {md(e['value'])} | `{e['pointer']}` |")
                    else:
                        L.append(f"| `{k}` | {n['type']} | {md(n['value'])} | `{n['pointer']}` |")
        L += ["", "## 잠정 관찰 (원문과 분리)", "", "| Pointer | 상태 | 관찰 |", "|---|---|---|"]
        for o in m["observations"]:
            L.append(f"| `{o['pointer']}` | {o['status']} | {md(o['note'])} |")
        L += ["", "## 수동 수집 표현 (원문 구간)", "", "| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |", "|---|---|---|---|---|"]
        for e in expressions:
            if e["method"] == "manual" and e["segment_id"] == sid:
                L.append(f"| `{e['pointer']}` | [{e['span'][0]},{e['span'][1]}) | {md(e['text'])} | {md(e['kind'])} | {md(e['note'])} |")
        L += ["", "## 이 구획의 미결", ""]
        if m["issues"]:
            L += ["| ID | 상태 | Pointer | 내용 |", "|---|---|---|---|"]
            for i in m["issues"]:
                L.append(f"| {i['id']} | {i['status']} | `{i['pointer']}` | {md(i['note'])} |")
        else:
            L.append("이 구획에서 새로 연 미결 없음(공통 미결은 issues.md).")
        kn = [k for k in known_errors if seg_of(k["pointer"]) == sid]
        L += ["", f"## 알려진 형태소 오분절 (K) — {len(kn)}건", "", "상세·원시 토큰은 `morphology.json#/known_missegmentations`.", ""]
        L += ["| Pointer | 구간 | 표현 | 원시 토큰 |", "|---|---|---|---|"]
        for k in kn:
            L.append(f"| `{k['pointer']}` | [{k['span'][0]},{k['span'][1]}) | {md(k['text'])} | {md(' '.join(k['raw_tokens']))} |")
        parts[sid] = "\n".join(L) + "\n"
    for sid, body in parts.items():
        out(f"review-part-{sid}.md", body)

    # 컬럼 구성 표: 경로 패턴별
    pat_rows = {}
    for n in p.nodes:
        pat = re.sub(r"/\d+", "/*", n["pointer"]) or "(root)"
        r = pat_rows.setdefault(pat, {"type": set(), "count": 0, "example": None, "lengths": set()})
        r["type"].add(n["type"])
        r["count"] += 1
        if n["type"] in ("object", "array"):
            r["lengths"].add(n["length"])
        if r["example"] is None:
            r["example"] = n
    total_pk = sum(len(c["packages"]) for c in combos)
    R = ["# problem-combos 1차 조사 — review", "",
         "## 상태", "",
         "- **1차 범위 종료: 예** (아래 조건 충족 — 상세 validation.md)",
         "- **원장 전체 완료 아님** — 의미 관계·공통 개념·원문 부족(B)·후속(F) 미결이 남음(issues.md)",
         f"- 전수 읽기: 구획 {len(cov_segments)}/{len(cov_segments)} 직접 읽음 (coverage.json, manual/S*.json)",
         f"- 구조·값 수집: 노드 {len(p.nodes)}개(말단 {len(leaf_ptrs)}개) 전부 source-map.json",
         f"- 형태소·표현 수집: 값 {len(morph_records)}건 중 적용 {sum(r['applied'] for r in morph_records)}·제외 {sum(not r['applied'] for r in morph_records)}(사유 기록), 필드명 출현 {len(field_names)}건; 표현 {len(expressions)}건(수동 {sum(e['method']=='manual' for e in expressions)})",
         f"- 알려진 분석 오류(K): {len(known_errors)}건 출현별 기록", "",
         "## 원본", "",
         f"- 경로: `{SRC_REL}`", f"- sha256: `{sha}` · {len(raw_bytes)} bytes · {len(text)} 코드포인트 · 1줄(개행 없음)",
         f"- 중복 키 {len(p.dups)}건 · 백슬래시 이스케이프 {'있음' if has_escape else '없음'} · BOM 없음 · BMP 밖 문자 {len(non_bmp)}개",
         f"- 묶음(combos) {len(combos)}개 · 패키지 {total_pk}개", "",
         "## 컬럼 구성 표", "",
         "모든 경로 패턴. 선택적 필드·빈 값 확인 결과: 모든 패키지가 같은 12키를 같은 순서로 가짐(선택적 필드 0). 빈 문자열·빈 배열·빈 객체·null 0건(verify.py가 재확인).", "",
         "| 원본 컬럼명/경로 패턴 | 자료형 | 중첩 구조·길이 | 출현 수 | 원문 예시 | 예시 Pointer |", "|---|---|---|---|---|---|"]
    for pat, r in pat_rows.items():
        ex = r["example"]
        exv = ex.get("value", f"키 {ex.get('keys')}" if ex["type"] == "object" else f"길이 {ex.get('length')}")
        lens = ("길이 " + ",".join(map(str, sorted(r["lengths"])))) if r["lengths"] else "말단"
        R.append(f"| `{pat}` | {'/'.join(sorted(r['type']))} | {lens} | {r['count']} | {md(exv)[:120]} | `{ex['pointer'] or '(root)'}` |")
    R += ["", "## 구획 목차", "", "| 구획 | 범위 | 소유 노드 | 말단 | 직접 읽기 | 관찰 | 수동 표현 | 파일 |", "|---|---|---|---|---|---|---|---|"]
    for s in cov_segments:
        R.append(f"| {s['segment_id']} | {md(s['scope'])} | {len(s['owned_pointers'])} | {len(s['owned_leaf_pointers'])} | {s['direct_read']} | {s['observation_count']} | {s['manual_expression_count']} | [review-part-{s['segment_id']}.md](review-part-{s['segment_id']}.md) |")
    R += ["", "## 전체에 걸친 잠정 관찰 (원문과 분리)", "",
          "- 패키지 tier 구성이 묶음마다 다름: P2·P3은 entry/recommended/premium/vip 4개, P9·P11은 entry/recommended 2개, 나머지 3개. (P)",
          "- 대안 기호 `or`·`/`·`또는`, 결합 기호 `+`, 순서/인과 기호 `→`, 부위 나열 `·`가 혼용됨. README 작성 규칙과 일치 여부는 기호만으로 확정하지 않음. (P/I)",
          "- 괄호의 쓰임: 브랜드(보톡스(엘러간)), 변형(나보타(희석)), 부위(나보타(교근)), 별칭((골든루틴)), 기전(보톡스(근이완)), 약어 풀이(PIH(시술 후 색소침착)), 코드(동적주름(M1)), 고지((개인차 있음)). (P)",
          "- products 배열은 24개 패키지 모두 원소 1개이며 그 안에 결합·대안이 문자열로 들어 있음. (P)",
          "- 같은 원장 안 어조 차이: 일부 항목(P3-4·P5-2·P11-2·P9-2 일부)은 유보·근거 수준 고지, 다수는 단정적 상담 문구. (P/I)",
          "- M코드·TXA 등은 이 원장 안에 정의가 없음 — 다른 원장과의 연결은 후속(F).", "",
          "## 다른 산출물", "",
          "- `source-map.json` 전체 노드·구간·바이트 · `morphology.json` 형태소·제외·K · `expressions.json` 표현·문장 · `coverage.json` 구획 소유 · `issues.md` 미결 · `validation.md` 검증 · `progress.md` 진행 · `manual/S*.json` 구획별 직접 읽기 기록"]
    out("review.md", "\n".join(R) + "\n")

    out("source-map.json", smap)
    out("morphology.json", morphology)
    out("expressions.json", expr_doc)
    out("coverage.json", coverage)
    print(json.dumps({"sha256": sha, "nodes": len(p.nodes), "leaves": len(leaf_ptrs), "morph_records": len(morph_records),
                      "applied": sum(r["applied"] for r in morph_records), "expressions": len(expressions),
                      "manual_unlocated": len(manual_problems), "known_missegmentations": len(known_errors),
                      "dups": len(p.dups)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
