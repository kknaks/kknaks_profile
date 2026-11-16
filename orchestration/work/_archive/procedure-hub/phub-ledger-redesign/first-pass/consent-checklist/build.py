"""consent-checklist.json 1차 수집 재현 빌드.

실행(레포 루트):
  uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/consent-checklist/build.py

원본은 읽기만 한다. 쓰기는 이 폴더 안에서만 한다.
구간 단위: 디코딩된 문자열의 Unicode 코드 포인트 [start,end). 파일 위치는 byte/codepoint 를 따로 적는다.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "../../../phub-recommend/bronze/phub-ledger/consent-checklist.json"))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/consent-checklist.json"


def out(name):
    return os.path.join(HERE, name)


def dump(name, obj):
    with open(out(name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def esc(seg):
    return str(seg).replace("~", "~0").replace("/", "~1")


# ---------------------------------------------------------------- 원문 파서
class Parser:
    """원문 텍스트를 직접 훑어 모든 노드의 JSON 리터럴 구간·중복 키를 기록한다."""

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []      # 값 노드
        self.keys = []       # 키 출현
        self.dups = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        assert self.t[self.i] == '"'
        s = self.i
        self.i += 1
        while True:
            c = self.t[self.i]
            if c == "\\":
                self.i += 2
                continue
            if c == '"':
                self.i += 1
                break
            self.i += 1
        lit = self.t[s:self.i]
        return json.loads(lit), s, self.i

    def value(self, ptr, parent, key, index):
        self.ws()
        c = self.t[self.i]
        s = self.i
        rec = {"pointer": ptr, "parent": parent, "key": key, "index": index}
        self.nodes.append(rec)
        if c == "{":
            self.i += 1
            seen = {}
            n = 0
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, ks, ke = self.string()
                    kp = ptr + "/" + esc(k) if ptr != "" else "/" + esc(k)
                    self.keys.append({"key": k, "object_pointer": ptr or "", "member_pointer": kp,
                                      "order": n, "literal_cp": [ks, ke]})
                    if k in seen:
                        self.dups.append({"object_pointer": ptr, "key": k, "first_order": seen[k], "dup_order": n})
                    seen[k] = n
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    self.value(kp, ptr, k, None)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            rec.update(type="object", length=n)
        elif c == "[":
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(f"{ptr}/{n}", ptr, None, n)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            rec.update(type="array", length=n)
        elif c == '"':
            v, _, _ = self.string()
            rec.update(type="string", value=v)
        else:
            m = re.compile(r"-?\d+(\.\d+)?([eE][+-]?\d+)?|true|false|null").match(self.t, self.i)
            lit = m.group(0)
            self.i = m.end()
            v = json.loads(lit)
            rec.update(type={bool: "boolean", type(None): "null"}.get(type(v), "number"), value=v)
        rec["literal_cp"] = [s, self.i]
        return rec


def build():
    raw = open(SRC, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    p = Parser(text)
    p.value("", None, None, None)
    p.ws()
    assert p.i == len(text)
    data = json.loads(text)

    # codepoint → byte
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + len(ch.encode("utf-8")))
    for r in p.nodes + p.keys:
        a, b = r["literal_cp"]
        r["literal_byte"] = [cum[a], cum[b]]
        r["literal"] = text[a:b] if r.get("type") not in ("object", "array") else None
    for r in p.nodes:
        if r["literal"] is None:
            r.pop("literal")
        r["empty"] = (r["type"] in ("object", "array") and r["length"] == 0) or r.get("value") == ""
        r["leaf"] = r["type"] not in ("object", "array")

    # 구획
    sections = [{"id": "S00", "title": "루트 메타데이터", "owned": [], "context": []}]
    for i, c in enumerate(data["categories"]):
        sections.append({"id": f"S{i+1:02d}", "title": f"/categories/{i} {c['id']} {c['name']}", "owned": [],
                         "context": ["/description", f"/categories/{i}/id", f"/categories/{i}/name"]})
    for r in p.nodes:
        ptr = r["pointer"]
        m = re.match(r"^/categories/(\d+)(/|$)", ptr)
        sec = f"S{int(m.group(1))+1:02d}" if m else "S00"
        r["section"] = sec
        next(s for s in sections if s["id"] == sec)["owned"].append(ptr)

    # 문맥: 값마다 카테고리·필드·같은 배열 앞뒤
    def ctx(ptr):
        m = re.match(r"^/categories/(\d+)/(\w+)(?:/(\d+))?$", ptr)
        if not m:
            return {"note": "루트 메타데이터"}
        i, f, j = int(m.group(1)), m.group(2), m.group(3)
        c = {"category_pointer": f"/categories/{i}", "category_id": data["categories"][i]["id"],
             "category_name": data["categories"][i]["name"], "field": f}
        if j is not None:
            arr = data["categories"][i][f]
            j = int(j)
            c["array_length"] = len(arr)
            c["prev_pointer"] = f"/categories/{i}/{f}/{j-1}" if j > 0 else None
            c["next_pointer"] = f"/categories/{i}/{f}/{j+1}" if j + 1 < len(arr) else None
        return c

    for r in p.nodes:
        r["context"] = ctx(r["pointer"])

    dump("source-map.json", {
        "source": {"path": SRC_REL, "size_bytes": len(raw), "sha256": sha, "encoding": "utf-8",
                   "bom": raw.startswith(b"\xef\xbb\xbf"), "line_count": text.count("\n") + 1,
                   "backslash_escape_count": text.count("\\")},
        "span_convention": "literal_cp = 디코딩된 파일 텍스트의 코드 포인트 [start,end) · literal_byte = 파일 UTF-8 바이트 [start,end) · 둘 다 JSON 리터럴(따옴표 포함) 구간. 값 내부 구간은 morphology/expressions 에서 디코딩 문자열 코드 포인트 [start,end).",
        "duplicate_keys": p.dups,
        "counts": {"nodes": len(p.nodes), "leaves": sum(r["leaf"] for r in p.nodes),
                   "containers": sum(not r["leaf"] for r in p.nodes),
                   "empty": sum(r["empty"] for r in p.nodes), "key_occurrences": len(p.keys)},
        "nodes": p.nodes,
        "key_occurrences": p.keys,
    })

    # ------------------------------------------------------------ 형태소
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi(num_workers=1, model_type="cong")
    morph_records = []
    applied, excluded = [], []
    EXCL = {"/version": "버전 식별자(숫자·점) — 언어 텍스트 아님",
            "/updated": "날짜 값(YYYY-MM-DD) — 언어 텍스트 아님"}
    for r in p.nodes:
        if not r["leaf"]:
            continue
        ptr = r["pointer"]
        if ptr in EXCL:
            excluded.append({"pointer": ptr, "value": r["value"], "reason": EXCL[ptr]})
            continue
        if re.match(r"^/categories/\d+/id$", ptr):
            excluded.append({"pointer": ptr, "value": r["value"], "reason": "카테고리 코드값(M+숫자) — 식별자, 언어 텍스트 아님"})
            continue
        if r["type"] != "string":
            excluded.append({"pointer": ptr, "value": r["value"], "reason": "비문자열"})
            continue
        v = r["value"]
        toks = []
        for k, t in enumerate(kiwi.tokenize(v)):
            s, e = t.start, t.start + t.len
            toks.append({"i": k, "form": t.form, "tag": t.tag, "start": s, "end": e, "surface": v[s:e],
                         "form_equals_surface": t.form == v[s:e], "sent_position": t.sent_position,
                         "score": round(t.score, 4)})
        applied.append(ptr)
        morph_records.append({"pointer": ptr, "role": "text_value", "value": v, "tokens": toks})
    # 알려진 오분절(작성자 대조 서명) — 출력은 교정하지 않고 출현을 기록
    segrev = json.load(open(out("segmentation-review.json"), encoding="utf-8"))
    known = []
    for sg in segrev["signatures"]:
        seq = [tuple(x) for x in sg["seq"]]
        hits = 0
        for mr in morph_records:
            T = mr["tokens"]
            for i in range(len(T) - len(seq) + 1):
                if not all((T[i+k]["form"], T[i+k]["tag"]) == seq[k] for k in range(len(seq))):
                    continue
                if "context_prev_tag" in sg and not (i > 0 and T[i-1]["tag"] == sg["context_prev_tag"]):
                    continue
                s, e = T[i]["start"], T[i+len(seq)-1]["end"]
                hits += 1
                for k in range(len(seq)):
                    T[i+k].setdefault("known_issue", []).append(sg["id"])
                known.append({"signature": sg["id"], "pointer": mr["pointer"], "start": s, "end": e,
                              "surface": mr["value"][s:e], "token_indexes": list(range(i, i+len(seq))),
                              "raw_tokens": [f"{T[i+k]['form']}/{T[i+k]['tag']}" for k in range(len(seq))],
                              "severity": sg["severity"], "impact": sg["impact"]})
        if hits != sg["expected_occurrences"]:
            raise SystemExit(f"segmentation signature {sg['id']} hits {hits} != expected {sg['expected_occurrences']}")
    # 필드명: 영문 snake_case 식별자 — 형태소 분석 제외, 출현은 source-map key_occurrences
    field_names = sorted({k["key"] for k in p.keys})
    for fn in field_names:
        excluded.append({"field_name": fn, "occurrences": [k["member_pointer"] for k in p.keys if k["key"] == fn],
                         "reason": "필드명(영문 snake_case 식별자) — 한국어 분석기 적용 제외. 원문 키 출현은 source-map.json key_occurrences"})
    dump("morphology.json", {
        "analyzer": {"name": "Kiwi (kiwipiepy)", "kiwipiepy": kiwipiepy.__version__, "model_type": "cong",
                     "num_workers": 1, "user_dictionary": None, "builtin_dictionary": "kiwipiepy 기본 내장",
                     "tokenize_kwargs": "기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, blocklist=None, compatible_jamo=False, split_sents=False, typos=None)",
                     "tagset": "Kiwi 품사 체계(세종 기반 + SL/SH/SN/W_* 등)",
                     "python": sys.version.split()[0]},
        "fields": {"form": "Kiwi token.form (도구가 낸 형태. 용언은 어간 형태). 별도 기본형(lemma)은 Kiwi 가 제공하지 않으므로 만들지 않았다",
                   "surface": "원문 값[start:end) — form 과 다를 수 있다(활용·축약)",
                   "start_end": "Kiwi token.start/len → 디코딩된 원문 값의 코드 포인트 [start,end). 정규화 없음(입력=원문 값 그대로)"},
        "applied_count": len(applied), "excluded_count": len(excluded),
        "token_count": sum(len(m["tokens"]) for m in morph_records),
        "excluded": excluded,
        "known_segmentation_issues": {"source": "segmentation-review.json", "global_limits": segrev["global_limits"],
                                      "occurrence_count": len(known), "occurrences": known,
                                      "scope_note": "이 목록 밖 토큰의 정확성은 보장하지 않는다. 출력은 교정하지 않았다."},
        "records": morph_records,
    })

    # ------------------------------------------------------------ 표현 후보
    exprs = []
    PATTERNS = [
        ("quantity_range", r"\d+(?:\.\d+)?\s*[-~–]\s*\d+(?:\.\d+)?\s*(?:개월|일|주|회|년|시간|분|%|mL)?"),
        ("quantity", r"(?:약\s*)?\d+(?:\.\d+)?\s*(?:개월|일간|일|주간|주|회|년|시간|분간|분|%|mL|°C|명|\+)"),
        ("parenthetical", r"\([^()]*(?:\([^()]*\)[^()]*)*\)"),
        ("dash_annotation", r"—[^—]+$"),
        ("time_window", r"\d+(?:-\d+)?\s*(?:개월|주|일|시간)\s*(?:이내|이상|간|후|전)|최소\s*[^,.]*?(?:개월|주)(?:간)?|수일(?:간| 내| 후)?|수주(?:간)?|수개월(?:~수년)?|수주-수개월"),
        ("possibility", r"[^,.()]*?(?:할|될|줄|이를|있을|날|올|볼|올릴)?\s*수 있(?:습니다|으며|음)|가능(?:성|하여|하지만|합니다)?|고려(?:될 수 있습니다| 가능)"),
        ("negation", r"[^,.()]*?(?:않[^\s,.]*|불가[^\s,.]*|아니[^\s,.]*|아닙니다|미입증|금지[^\s,.]*|금기[^\s,.]*|없[^\s,.]*)"),
        ("condition", r"[^,.()]*?(?:\s시(?=[\s,)])|경우|따라|하에|이면|하면|시에)"),
    ]
    KEYWORDS = {
        "frequency_modifier": ["매우 드물지만", "극히 드묾", "드물게", "드물지만", "드문", "대부분", "보통", "일부", "통상적"],
        "degree_modifier": ["심한", "심각한", "강한", "강하게", "상당한", "과도한", "급격한", "급격히", "급성", "중증", "고용량", "고에너지", "깊은", "얕은", "얇은", "짙은", "매우 어두운", "작은", "미세", "부드러운", "철저한", "철저히", "크게", "큰"],
        "course_modifier": ["일시적", "영구적", "지속적", "지연성", "점진적", "점점", "즉시", "즉각적인", "자연 탈락", "오히려", "비정상적", "장기"],
        "certainty_modifier": ["반드시", "필수", "꼭", "절대", "확실한", "원칙", "의심", "주의", "권장", "선택 사항", "중요"],
        "comparison": ["상대적으로", "보다", "초과", "이상", "이내", "최소", "약 "],
        "evidence": ["과학적 근거", "임상연구", "보고", "연구", "통계적으로", "CI", "Task Force", "판례", "데이터"],
    }
    eid = 0
    for r in p.nodes:
        if not r["leaf"] or r["type"] != "string" or r["pointer"] in EXCL or re.match(r"^/categories/\d+/id$", r["pointer"]):
            continue
        v, ptr = r["value"], r["pointer"]
        # 문장 단위(값 전체 또는 '. ' 경계)
        for m in re.finditer(r"(?:[^.]|\.(?!\s|$))+(?:\.(?=\s|$))?", v):
            seg = m.group(0)
            ls = len(seg) - len(seg.lstrip())
            s, e = m.start() + ls, m.end()
            if e > s:
                eid += 1
                exprs.append({"id": f"E{eid:04d}", "pointer": ptr, "start": s, "end": e, "text": v[s:e],
                              "category": "sentence_or_value", "method": "regex:sentence_split"})
        for cat, pat in PATTERNS:
            for m in re.finditer(pat, v):
                s, e = m.start(), m.end()
                while s < e and v[s] == " ":
                    s += 1
                while e > s and v[e-1] == " ":
                    e -= 1
                if e > s:
                    eid += 1
                    exprs.append({"id": f"E{eid:04d}", "pointer": ptr, "start": s, "end": e, "text": v[s:e],
                                  "category": cat, "method": f"regex:{cat}"})
        for cat, kws in KEYWORDS.items():
            for kw in kws:
                for m in re.finditer(re.escape(kw), v):
                    eid += 1
                    exprs.append({"id": f"E{eid:04d}", "pointer": ptr, "start": m.start(), "end": m.end(), "text": kw,
                                  "category": cat, "method": f"keyword:{kw}"})
    manual = json.load(open(out("manual-expressions.json"), encoding="utf-8"))
    vals = {r["pointer"]: r.get("value") for r in p.nodes}
    for mx in manual["items"]:
        v = vals[mx["pointer"]]
        occ = mx.get("occurrence", 0)
        s = -1
        for _ in range(occ + 1):
            s = v.find(mx["text"], s + 1)
        if s < 0:
            raise SystemExit(f"manual expression not found: {mx}")
        eid += 1
        exprs.append({"id": f"E{eid:04d}", "pointer": mx["pointer"], "start": s, "end": s + len(mx["text"]),
                      "text": mx["text"], "category": mx["category"], "method": "manual:direct_read",
                      "manual_id": mx["id"], "note": mx.get("note")})
    # 자동 후보 검토 규칙(작성자 대조): 오탐·문맥 주의 표시
    exrev = json.load(open(out("expression-review.json"), encoding="utf-8"))
    for rule in exrev["rules"]:
        n = 0
        for x in exprs:
            if x["method"] != rule["method"] or x["pointer"] != rule["pointer"] or x["start"] != rule["start"]:
                continue
            x.setdefault("review", []).append({"rule": rule["id"], "verdict": rule["verdict"], "note": rule["note"]})
            n += 1
        if n != rule["expected_matches"]:
            raise SystemExit(f"expression rule {rule['id']} matched {n} != {rule['expected_matches']}")
    # 같은 구간 겹침 통계
    seen = {}
    for x in exprs:
        seen.setdefault((x["pointer"], x["start"], x["end"]), []).append(x["id"])
    same = [v for v in seen.values() if len(v) > 1]
    dump("expressions.json", {
        "method": "자동 후보(regex·keyword)는 수집 보조이며 전수 의미 해석이 아니다. manual:direct_read 는 작성자가 원문을 직접 읽고 지정한 구간이다. 구간은 원문 값의 코드 포인트 [start,end). 구간 겹침은 의도된 것이며(같은 구절을 여러 관점으로 표시), 완전 동일 (pointer,start,end,category,method) 중복은 verify 가 검사한다.",
        "patterns": PATTERNS, "keywords": KEYWORDS,
        "counts": {"total": len(exprs), "manual": sum(x["method"].startswith("manual") for x in exprs),
                   "same_span_groups": len(same)},
        "items": exprs,
    })

    # ------------------------------------------------------------ coverage
    obs = json.load(open(out("manual-observations.json"), encoding="utf-8"))
    for s in sections:
        o = obs["sections"][s["id"]]
        s.update(read_status=o["read_status"], read_method=o["read_method"],
                 review_file="review.md", review_anchor=f"#{s['id'].lower()}",
                 pointer_range=(s["owned"][0], s["owned"][-1]),
                 leaf_count=sum(1 for r in p.nodes if r["section"] == s["id"] and r["leaf"]))
    dump("coverage.json", {
        "source_sha256": sha,
        "rule": "모든 노드(컨테이너·말단·빈 값)는 정확히 한 구획이 소유한다(owned). context 는 함께 읽은 상위 문맥 참조이며 소유가 아니다. read_status 는 작성자 직접 읽기 기록(manual-observations.json)에서 오며 기계 추출과 구분한다.",
        "last_read": obs["last_read"],
        "sections": sections,
    })

    write_review(data, p.nodes, sections, obs, sha, len(raw), morph_records, exprs)
    print(json.dumps({"sha256": sha, "nodes": len(p.nodes), "tokens": sum(len(m["tokens"]) for m in morph_records),
                      "expressions": len(exprs), "dups": len(p.dups)}, ensure_ascii=False))


def cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ")


def write_review(data, nodes, sections, obs, sha, size, morph, exprs):
    L = []
    A = L.append
    A("# consent-checklist.json — 1차 수집 읽기용 결과")
    A("")
    A("> **상태: 1차 수집 범위 종료 보고(코디 확인 전) · 원장 전체 완료 아님.** 열린 미결은 [issues.md](./issues.md), 검증은 [validation.md](./validation.md).")
    A("")
    A(f"- 원본: `{SRC_REL}` · {size} bytes · sha256 `{sha}`")
    A(f"- 노드 {len(nodes)} (말단 {sum(r['leaf'] for r in nodes)} · 컨테이너 {sum(not r['leaf'] for r in nodes)} · 빈 값 {sum(r['empty'] for r in nodes)}) · 중복 키 0")
    A(f"- 형태소: Kiwi 0.24.1 cong · 적용 값 {len(morph)} · 토큰 {sum(len(m['tokens']) for m in morph)} → [morphology.json](./morphology.json)")
    A(f"- 표현 후보 {len(exprs)} (수동 {sum(x['method'].startswith('manual') for x in exprs)}) → [expressions.json](./expressions.json)")
    A("- 구획·읽기 상태 → [coverage.json](./coverage.json) · 원문 위치·리터럴 구간 → [source-map.json](./source-map.json)")
    A("")
    A("원문 값 칸에는 원본 문자열을 그대로 싣는다(Markdown 표 안의 `|` 만 `\\|` 로 이스케이프). 잠정 관찰은 각 구획 아래 별도 표에 있으며 원문 칸과 섞지 않는다.")
    A("")
    A("## 컬럼 구성")
    A("")
    A("| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 | 원문 예시 | 예시 위치 |")
    A("|---|---|---|---|---|")
    cats = data["categories"]
    A(f"| `/` | object · 키 4 (version, updated, description, categories) | 1 | — | `""` (빈 Pointer = 루트) |")
    A(f"| `/version` | string | 1 | {cell(data['version'])} | `/version` |")
    A(f"| `/updated` | string (날짜 모양) | 1 | {cell(data['updated'])} | `/updated` |")
    A(f"| `/description` | string | 1 | {cell(data['description'])} | `/description` |")
    A(f"| `/categories` | array of object · 길이 {len(cats)} | 1 | — | `/categories` |")
    A(f"| `/categories/*` | object · 키 5 (id, name, mandatory_disclosures, contraindications, emergency_signs) · 전 항목 동일 키·순서 | {len(cats)} | — | `/categories/0` |")
    A(f"| `/categories/*/id` | string | {len(cats)} | {cats[0]['id']} | `/categories/0/id` |")
    A(f"| `/categories/*/name` | string · `/` 포함 변형 있음 | {len(cats)} | {cell(cats[2]['name'])} | `/categories/2/name` |")
    for f in ["mandatory_disclosures", "contraindications", "emergency_signs"]:
        lens = [len(c[f]) for c in cats]
        tot = sum(lens)
        A(f"| `/categories/*/{f}` | array of string · 길이 {min(lens)}~{max(lens)} · 빈 배열 0 | {len(cats)} | — | `/categories/0/{f}` |")
        ex = cats[0][f][0]
        A(f"| `/categories/*/{f}/*` | string · 빈 문자열 0 | {tot} | {cell(ex)} | `/categories/0/{f}/0` |")
    multi = [(i, j) for i, c in enumerate(cats) for f in ["mandatory_disclosures", "contraindications", "emergency_signs"] for j, v in enumerate(c[f]) if len(re.findall(r"[.](?=\s|$)", v)) >= 2 or re.search(r"[.]\s", v)]
    longest = max(((i, j, v) for i, c in enumerate(cats) for j, v in enumerate(c["mandatory_disclosures"])), key=lambda x: len(x[2]))
    A(f"| `/categories/*/{{mandatory_disclosures,contraindications,emergency_signs}}/*` (변형: 여러 문장) | string · 문장 여러 개(마침표+공백 경계) | {len(multi)} | {cell(longest[2][:60])}… | `/categories/{longest[0]}/mandatory_disclosures/{longest[1]}` |")
    A("")
    A("선택적 필드·null·숫자·불리언·빈 컨테이너·빈 문자열은 없다(source-map.json counts 와 verify 로 확인).")
    A("")
    A("## 구획 목차")
    A("")
    A("| 구획 | 범위 | 소유 노드 | 말단 | 읽기 상태 |")
    A("|---|---|---|---|---|")
    for s in sections:
        A(f"| [{s['id']}](#{s['id'].lower()}) | {cell(s['title'])} | {len(s['owned'])} | {s['leaf_count']} | {s['read_status']} |")
    A("")
    for s in sections:
        A(f"## {s['id']}")
        A("")
        A(f"**{s['title']}** · 읽기: {s['read_status']} ({s['read_method']})")
        if s["context"]:
            A(f"· 함께 읽은 상위 문맥: {', '.join('`'+c+'`' for c in s['context'])}")
        A("")
        A("| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |")
        A("|---|---|---|---|")
        for r in nodes:
            if r["section"] != s["id"]:
                continue
            col = r["key"] if r["key"] is not None else (nodes_parent_key(nodes, r) + f"[{r['index']}]") if r["index"] is not None else "(루트)"
            if r["leaf"]:
                val = cell(r["value"])
                typ = r["type"]
            else:
                val = "—"
                typ = f"{r['type']} · 길이 {r['length']}"
            A(f"| `{col}` | `{r['pointer'] or '(루트)'}` | {typ} | {val} |")
        A("")
        o = obs["sections"][s["id"]]
        A("**잠정 관찰** (원문 아님 · 근거 위치 병기 · 확정 아님)")
        A("")
        if o["observations"]:
            A("| # | 근거 Pointer | 원문 인용 | 관찰 | 상태 |")
            A("|---|---|---|---|---|")
            for k, ob in enumerate(o["observations"], 1):
                A(f"| {s['id']}-{k} | `{ob['pointer']}` | {cell(ob['quote'])} | {cell(ob['note'])} | {ob['status']} |")
        else:
            A("관찰 없음(관찰이 없다고 의미가 없다는 뜻은 아니다).")
        A("")
    with open(out("review.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def nodes_parent_key(nodes, r):
    par = next(n for n in nodes if n["pointer"] == r["parent"])
    return par["key"] or ""


if __name__ == "__main__":
    build()
