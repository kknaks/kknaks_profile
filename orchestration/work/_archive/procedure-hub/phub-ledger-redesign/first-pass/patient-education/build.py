"""patient-education.json 1차 조사 산출물 생성.

레포 루트에서:
  uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/patient-education/build.py

입력: 원본(읽기 전용) + 이 폴더의 segments.json · manual/S*.json · manual/segmentation-review.json
출력(이 폴더만): source-map.json · morphology.json · expressions.json · coverage.json · issues.md · review.md · review-part-S*.md · build-output.txt
생성물은 직접 고치지 않는다. 보완은 manual/ 에 하고 다시 돌린다.
"""
import collections
import sys as _s
_s.dont_write_bytecode = True
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_common import HERE, SRC_REL, Parser, cp_to_byte, read_source, segment_of  # noqa: E402

raw, text, sha = read_source()
parser = Parser(text)
nodes = parser.parse()
c2b = cp_to_byte(text)
by_ptr = {n["pointer"]: n for n in nodes}
segments = json.load(open(os.path.join(HERE, "segments.json"), encoding="utf-8"))["segments"]
seg_ids = [s["segment"] for s in segments]
manual = {}
for f in sorted(glob.glob(os.path.join(HERE, "manual", "S*.json"))):
    m = json.load(open(f, encoding="utf-8"))
    manual[m["segment"]] = m
seg_review = json.load(open(os.path.join(HERE, "manual", "segmentation-review.json"), encoding="utf-8"))
log = []


def out(name, obj):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def b(span):
    return [c2b[span[0]], c2b[span[1]]]


def field_pattern(ptr):
    return re.sub(r"/\d+", "/*", ptr) or "/"


def root_of(seg):
    return next(s["pointer_root"] for s in segments if s["segment"] == seg)


# ---------------------------------------------------------------- source-map
def context_refs(n):
    p = n["pointer"]
    parts = p.split("/")
    refs = []
    if len(parts) >= 3 and parts[1] == "categories":
        base = "/categories/" + parts[2]
        if p not in (base + "/id", base + "/name"):
            refs += [base + "/id", base + "/name"]
        if len(parts) >= 6 and parts[3] == "common_concerns":
            qa = base + "/common_concerns/" + parts[4]
            sib = qa + ("/q" if parts[5] == "a" else "/a")
            refs.append(sib)
    return refs


smap_nodes = []
for n in nodes:
    rec = {
        "order": n["order"],
        "pointer": n["pointer"],
        "parent": n["parent"],
        "key": n["key"],
        "field_pattern": field_pattern(n["pointer"]),
        "type": n["type"],
        "segment": segment_of(n["pointer"]),
        "literal_cp": n["literal_cp"],
        "literal_byte": b(n["literal_cp"]),
        "context_refs": context_refs(n),
    }
    if n["key_cp"] is not None:
        rec["key_literal_cp"] = n["key_cp"]
        rec["key_literal_byte"] = b(n["key_cp"])
    if n["type"] in ("object", "array"):
        rec["child_count"] = n["child_count"]
        rec["empty_container"] = n["child_count"] == 0
    else:
        rec["value"] = n["value"]
        if n["type"] == "string":
            rec["value_cp"] = n["value_cp"]
            rec["value_byte"] = b(n["value_cp"])
            rec["has_escape"] = n["has_escape"]
            rec["decoded_len"] = len(n["value"])
            rec["empty_string"] = n["value"] == ""
    smap_nodes.append(rec)

leaf_ptrs = [n["pointer"] for n in nodes if n["type"] not in ("object", "array") or n["child_count"] == 0]
out("source-map.json", {
    "source": SRC_REL,
    "source_sha256": sha,
    "source_bytes": len(raw),
    "source_codepoints": len(text),
    "encoding": "UTF-8 (BOM 없음)",
    "parse": {
        "parser": "pe_common.Parser — 직접 문자 단위 파싱(중복 키 감지·위치 기록)",
        "duplicate_keys": parser.duplicates,
        "strings_with_escape": sum(1 for n in nodes if n.get("has_escape")),
        "newlines_in_file": text.count("\n"),
    },
    "span_units": {
        "literal_cp": "원문 파일 문자열(디코딩된 UTF-8)의 코드포인트 [start,end) — JSON 리터럴 전체(문자열은 따옴표 포함)",
        "value_cp": "문자열 값의 따옴표 안쪽 원문 코드포인트 [start,end). 이스케이프 0 이므로 디코딩 값과 길이·내용이 같다",
        "*_byte": "원문 파일 UTF-8 바이트 [start,end)",
        "key_literal_cp": "객체 키 리터럴(따옴표 포함) 코드포인트 [start,end)",
    },
    "counts": {
        "nodes": len(nodes),
        "objects": sum(1 for n in nodes if n["type"] == "object"),
        "arrays": sum(1 for n in nodes if n["type"] == "array"),
        "strings": sum(1 for n in nodes if n["type"] == "string"),
        "numbers": sum(1 for n in nodes if n["type"] == "number"),
        "booleans": sum(1 for n in nodes if n["type"] == "boolean"),
        "nulls": sum(1 for n in nodes if n["type"] == "null"),
        "empty_containers": sum(1 for n in nodes if n["type"] in ("object", "array") and n["child_count"] == 0),
        "empty_strings": sum(1 for n in nodes if n.get("value") == ""),
        "leaf_pointers": len(leaf_ptrs),
        "object_keys": sum(1 for n in nodes if n["key_cp"] is not None),
    },
    "nodes": smap_nodes,
})

# ---------------------------------------------------------------- morphology
EXCLUDE = [
    (r"^/version$", "version_code", "버전 식별자. 언어 텍스트 아님"),
    (r"^/updated$", "date", "ISO 날짜. 언어 텍스트 아님"),
    (r"^/categories/\d+/id$", "category_code", "카테고리 코드(M1~M17). 식별자"),
]
from kiwipiepy import Kiwi, __version__ as KIWI_VER  # noqa: E402

kiwi = Kiwi(num_workers=1, model_type="cong")
TOK_OPTS = dict(normalize_coda=False, z_coda=True, split_complex=False, compatible_jamo=False, saisiot=None)

applied, excluded = [], []
for n in nodes:
    if n["type"] != "string":
        continue
    reason = next(((k, r) for pat, k, r in EXCLUDE if re.match(pat, n["pointer"])), None)
    if reason:
        excluded.append({"pointer": n["pointer"], "kind": reason[0], "reason": reason[1], "value": n["value"]})
        continue
    toks = kiwi.tokenize(n["value"], **TOK_OPTS)
    trecs = []
    for i, t in enumerate(toks):
        s, e = t.start, t.start + t.len
        trecs.append({
            "i": i, "form": t.form, "tag": t.tag, "lemma": t.lemma, "start": s, "end": e,
            "surface": n["value"][s:e], "file_cp": [n["value_cp"][0] + s, n["value_cp"][0] + e],
        })
    applied.append({"pointer": n["pointer"], "segment": segment_of(n["pointer"]), "value": n["value"], "tokens": trecs})

# 필드명(키): 영문 snake_case 식별자 — 형태소 제외. 출현 위치는 source-map key_literal_cp.
key_names = collections.OrderedDict()
for n in nodes:
    if n["key_cp"] is not None:
        key_names.setdefault(n["key"], []).append(n["pointer"])

# 알려진 오분절(출현별) — manual/segmentation-review.json 을 원시 토큰과 대조
app_by_ptr = {a["pointer"]: a for a in applied}
known = []
for r in seg_review["occurrences"]:
    a = app_by_ptr[r["pointer"]]
    v = a["value"]
    occ = [m.start() for m in re.finditer(re.escape(r["surface"]), v)]
    k = r.get("occurrence", 1)
    if len(occ) < k:
        raise SystemExit("segmentation-review surface not found: %r @ %s" % (r["surface"], r["pointer"]))
    s = occ[k - 1]
    e = s + len(r["surface"])
    raw_toks = [t for t in a["tokens"] if t["start"] < e and t["end"] > s or (t["start"] == t["end"] == s)]
    known.append(dict(r, span=[s, e], file_cp=[by_ptr[r["pointer"]]["value_cp"][0] + s, by_ptr[r["pointer"]]["value_cp"][0] + e],
                      raw_tokens=["%s/%s" % (t["form"], t["tag"]) for t in raw_toks]))

out("morphology.json", {
    "source_sha256": sha,
    "analyzer": {
        "name": "kiwipiepy", "version": KIWI_VER, "model_type": "cong", "num_workers": 1,
        "user_dictionary": None, "builtin_dictionary": "kiwipiepy_model 기본(설치 패키지 내장)",
        "tokenize_options": TOK_OPTS, "split_sents": False,
        "tagset": "Kiwi 품사 태그(세종 기반 + SL/SN/SH/W_SERIAL 등)",
        "lemma": "Kiwi Token.lemma 를 그대로 기록. 도구가 준 값 외 기본형을 만들지 않았다",
        "offsets": "start/end = 분석에 넣은 디코딩 값의 코드포인트 [start,end). file_cp = value_cp 시작 + start (이스케이프 0)",
        "surface": "원문 value[start:end]. form 과 다를 수 있다(길이 0 토큰·ᆫ 어미 등)",
        "stopwords": "제거 없음 — 조사·어미·부사·부정 표현 보존",
        "invocation": "uv run --python 3.12 --with kiwipiepy==0.24.1",
    },
    "policy": {
        "values_excluded": [{"pattern": p, "kind": k, "reason": r} for p, k, r in EXCLUDE],
        "field_names": "필드명은 영문 snake_case 식별자(id·name·patient_name·simple_explanation·how_it_works·duration_simple·pain_level·downtime·common_concerns·q·a·version·updated·categories). 한국어 분석기 적용 부적합 — 제외. 출현 위치는 source-map.json key_literal_cp",
        "languages": "모든 텍스트 값은 한국어 문장에 라틴 약어·제품 표기(PRP·RF·SMAS·PIH·AHA 등)·수치가 섞인 형태. 별도 언어별 필드 없음. 라틴 약어는 Kiwi 가 SL 로 남기며 영어 형태소 분석은 하지 않았다",
    },
    "counts": {
        "string_values": sum(1 for n in nodes if n["type"] == "string"),
        "applied_values": len(applied), "excluded_values": len(excluded),
        "tokens": sum(len(a["tokens"]) for a in applied),
        "field_names_excluded": len(key_names), "field_name_occurrences": sum(len(v) for v in key_names.values()),
        "known_missegmentation_occurrences": len(known),
    },
    "excluded": excluded,
    "field_names": [{"key": k, "occurrences": len(v), "first_pointer": v[0], "status": "excluded", "reason": "영문 식별자"} for k, v in key_names.items()],
    "known_missegmentation": known,
    "known_missegmentation_note": seg_review["note"],
    "values": applied,
})

# ---------------------------------------------------------------- expressions
expr = []
eid = 0
for seg in seg_ids:
    m = manual.get(seg)
    if not m:
        continue
    root = root_of(seg)
    for rel, items in m["expressions"].items():
        ptr = root + rel
        n = by_ptr[ptr]
        v = n["value"]
        for it in items:
            sub, facets, note = it[0], it[1], it[2]
            k = it[3] if len(it) > 3 else 1
            occ = [mm.start() for mm in re.finditer(re.escape(sub), v)]
            if len(occ) < k:
                raise SystemExit("manual expression not found: %r @ %s" % (sub, ptr))
            s = occ[k - 1]
            e = s + len(sub)
            eid += 1
            expr.append({
                "id": "E%04d" % eid, "segment": seg, "pointer": ptr, "field": n["key"], "text": sub,
                "span_in_value": [s, e], "file_cp": [n["value_cp"][0] + s, n["value_cp"][0] + e],
                "file_byte": b([n["value_cp"][0] + s, n["value_cp"][0] + e]),
                "facets": facets.split(","), "note": note, "source": "manual", "occurrence_in_value": k,
                "occurrences_of_text_in_value": len(occ),
            })

# 보조 정규식 후보 — 실제 패턴 일치분뿐이다. 의미 판정 아님.
REGEX = [
    ("num_range", r"\d+(?:\.\d+)?\s*[-~]\s*\d+(?:\.\d+)?\s*(?:개월|주|일|년|시간|회|%|mm|ml)?"),
    ("num_unit", r"\d+(?:\.\d+)?\s*(?:개월|주|일|년|시간|회|%|mm|ml|분)"),
    ("approx", r"약 |대략|정도|거의|수 ?시간|수 ?주|수 ?분|수 ?개월|수회|며칠|몇 주"),
    ("frequency", r"드물|드뭅|흔합|보통|일반적으로|자주|정기적"),
    ("negation", r"않|없|아니|아닙|못|말고|마세요|미허가|비수술|입증되지"),
    ("possibility", r"수 있|가능|어렵|단정할 수"),
    ("condition", r"(?:하|되|맞으|있으|지나|빠지|찌|녹으)면|경우|따라|시 |필요 시|하에|더라도"),
    ("time_rel", r"후|직후|당일|전 |중 |동안|이후|즉시|바로|당장|즉각"),
    ("instruction", r"하세요|주세요|마세요|해야 합니다|필요합니다|중요합니다|중요해요|삼가|자제|반드시|절대|바랍니다|상의|상담"),
    ("degree", r"약간|가벼운|가볍게|심한|과도하게|세게|강한|극히|매우|훨씬|크게|미세한|자잘한|아주|고도로|충분히|철저히"),
    ("depth_thick", r"깊|얕|얇|가는 바늘|두께"),
    ("manner_speed", r"서서히|점진적|빠르게|금방|자연스럽게|부드럽게|천천히"),
    ("comparison", r"보다|만큼|처럼|비슷|더 |오히려|상대적"),
    ("evidence", r"연구|입증|근거|보고|임상"),
]
manual_by_ptr = collections.defaultdict(list)
for x in expr:
    manual_by_ptr[x["pointer"]].append(x)
cands = []
cid = 0
for a in applied:
    ptr = a["pointer"]
    v = a["value"]
    n = by_ptr[ptr]
    for kind, pat in REGEX:
        for mm in re.finditer(pat, v):
            s, e = mm.start(), mm.end()
            cov = [x["id"] for x in manual_by_ptr[ptr] if x["span_in_value"][0] <= s and e <= x["span_in_value"][1] and "sentence" not in x["facets"]]
            cov_sent = [x["id"] for x in manual_by_ptr[ptr] if x["span_in_value"][0] <= s and e <= x["span_in_value"][1]]
            cid += 1
            cands.append({
                "id": "R%04d" % cid, "kind": kind, "pointer": ptr, "match": v[s:e], "span_in_value": [s, e],
                "file_cp": [n["value_cp"][0] + s, n["value_cp"][0] + e],
                "covered_by_manual_phrase": cov, "covered_by_manual_any": cov_sent,
            })
uncov_phrase = [c for c in cands if not c["covered_by_manual_phrase"]]
uncov_any = [c for c in cands if not c["covered_by_manual_any"]]
regex_review = json.load(open(os.path.join(HERE, "manual", "regex-review.json"), encoding="utf-8"))
rr_map = {(r["pointer"], r["match"], r["span_in_value"][0]): r for r in regex_review["items"]}
for c in uncov_phrase:
    r = rr_map.get((c["pointer"], c["match"], c["span_in_value"][0]))
    c["review"] = r["verdict"] if r else None
    c["review_note"] = r["note"] if r else None

# 문장 단위 보존: 모든 적용 값은 manual 「sentence」 또는 값 전체 구절로 덮여야 한다 → verify 가 검사
out("expressions.json", {
    "source_sha256": sha,
    "method": {
        "manual_reading": "구획별 원문 직접 읽기로 기록(manual/S*.json). facets 는 탐색 관점이며 확정 분류가 아니다",
        "regex": "보조 정규식 후보(REGEX). 실제 패턴 일치분뿐이며 패턴 밖 표현은 이 목록에 없다 — 패턴 밖 형용사·부사·회피/권고·깊이/두께·속도·근사·「후/시」 조건은 직접 읽기 기록(manual)에서 수집",
        "regex_review": "수동 구절(문장 제외)로 덮이지 않은 후보는 manual/regex-review.json 에서 판정(added_elsewhere/false_positive/covered_by_sentence_only 등)",
        "span": "span_in_value = 디코딩 값의 코드포인트 [start,end). file_cp/file_byte = 원문 파일 위치",
        "overlap": "표현 간 겹침은 의도(문장·구절·내부 수식어를 함께 보존). 같은 (pointer, span) 중복은 verify 가 오류로 검사",
    },
    "facet_vocabulary": {
        "sentence": "문장(또는 문장 단위 값) 전체", "name": "시술·제품·카테고리명처럼 보이는 표현", "alternative": "「/」「또는」 등으로 묶인 대안·병기",
        "concern": "고민·증상 표현", "site": "부위·층·장소성 신체 위치", "depth": "깊이·층 수식", "thickness": "두께 수식",
        "substance": "물질·성분·약물", "device": "기구·장비·바늘·실", "device_param": "에너지 종류·파장·온도 등 작용 수단",
        "route": "투여·적용 방식(주사·도포 등)", "mechanism": "작용 설명", "effect": "기대 효과·결과", "adverse": "부작용·위험 사건",
        "emergency": "응급 관련 표현", "contraindication": "금기·시술 대상 아님", "target": "대상 집단(환자 조건)", "actor": "시술·판단 주체(의사·병원)",
        "place": "장소(병원·집·클리닉·국내)", "time": "시간·기간·시점(후/시/직후/당일)", "quantity": "수치·단위", "range": "범위",
        "approx": "근사(약·대략·정도·수 N)", "frequency": "빈도·횟수·주기", "degree": "정도 수식", "manner": "방식·속도",
        "course": "경과·지속·소실 특성", "condition": "조건·적용 범위", "scope": "한정(~만·일부·~에만)", "negation": "부정",
        "possibility": "가능성·단정 회피", "hedge": "완곡·추정 서술", "comparison": "비교", "instruction": "행동 지시·권고",
        "avoid": "회피·금지 지시", "management": "관리·교정·조치", "rationale": "이유·근거 설명", "cause": "원인 관계 표현",
        "evidence": "연구·근거·보고 언급", "regulatory": "허가·규제 서술", "reference": "다른 항목·카테고리 참조", "paraphrase": "괄호 풀이·병기",
        "relation": "관계 서술", "combination": "병용·함께 받기", "sequence": "순서·단계", "sensory": "감각·통증 표현", "contrast": "단서·예외 도입(다만·~지만 등)",
    },
    "counts": {
        "manual_expressions": len(expr), "regex_candidates": len(cands),
        "regex_uncovered_by_manual_phrase": len(uncov_phrase), "regex_uncovered_by_any_manual": len(uncov_any),
    },
    "expressions": expr,
    "regex_candidates": cands,
})

# ---------------------------------------------------------------- coverage
cov_segments = []
for s in segments:
    seg = s["segment"]
    m = manual.get(seg, {})
    owned = [n["pointer"] for n in nodes if segment_of(n["pointer"]) == seg]
    cov_segments.append(dict(
        s,
        machine_extracted=True,
        direct_read=m.get("read_status", "planned"),
        last_read_pointer=m.get("last_read_pointer"),
        manual_record="manual/%s.json" % seg if m else None,
        review_file="review-part-%s.md" % seg,
        owned_pointers=owned,
        owned_leaf_pointers=[p for p in owned if p in set(leaf_ptrs)],
        expressions=sum(1 for x in expr if x["segment"] == seg),
        observations=len(m.get("observations", [])),
    ))
out("coverage.json", {
    "source_sha256": sha,
    "rule": "pe_common.segment_of — /categories/<i> 하위 전부는 S(i+1), 그 밖(루트·/version·/updated·/categories 배열 노드)은 S00. 공동 참조 문맥(context_refs)은 소유가 아니다",
    "machine_vs_direct": "machine_extracted=build 가 구조·값·형태소를 추출함 · direct_read=manual 기록의 읽기 상태(사람이 원문을 직접 읽었는지)",
    "all_node_pointers": [n["pointer"] for n in nodes],
    "all_leaf_pointers": leaf_ptrs,
    "segments": cov_segments,
})

# ---------------------------------------------------------------- issues.md
ST = {"A": "에이전트 추출/해석 오류", "B": "원문 정보 부족", "C": "사용자 결정 필요", "K": "알려진 분석 한계",
      "P": "잠정 관찰", "F": "후속 의미 조사", "I": "원문 내 불일치·표기 이상"}
obs_all = []
for seg in seg_ids:
    m = manual.get(seg)
    if not m:
        continue
    for i, (rel, st, txt) in enumerate(m["observations"], 1):
        obs_all.append({"id": "%s-O%d" % (seg, i), "segment": seg, "pointer": root_of(seg) + rel, "status": st, "text": txt})
issues_head = open(os.path.join(HERE, "manual", "issues-head.md"), encoding="utf-8").read()
L = [issues_head.rstrip(), "", "## 상태별 집계 (manual 관찰 + 오분절 기록에서 생성)", "", "| 상태 | 뜻 | 건수 |", "|---|---|---|"]
cnt = collections.Counter(o["status"] for o in obs_all)
for k in "ABCIKPF":
    extra = len(known) if k == "K" else 0
    L.append("| %s | %s | %d%s |" % (k, ST[k], cnt.get(k, 0) + extra, " (관찰 %d + 오분절 출현 %d)" % (cnt.get(k, 0), len(known)) if k == "K" else ""))
L += ["", "## 관찰·미결 전체 목록 (구획 순)", "", "| ID | 상태 | Pointer | 내용 |", "|---|---|---|---|"]
for o in obs_all:
    L.append("| %s | %s | `%s` | %s |" % (o["id"], o["status"], o["pointer"], o["text"].replace("|", "\\|")))
L += ["", "## K — 알려진 형태소 오분절 (출현별, 교정하지 않음)", "", "| # | Pointer | 원문 표면 | 값 내 구간 | 원시 토큰 | 영향 |", "|---|---|---|---|---|---|"]
for i, k in enumerate(known, 1):
    L.append("| K%d | `%s` | %s | [%d,%d) | %s | %s |" % (i, k["pointer"], k["surface"], k["span"][0], k["span"][1], " ".join(k["raw_tokens"]), k["impact"]))
L += ["", "## 보조 정규식 후보 중 수동 구절로 덮이지 않은 것", "",
      "정규식 후보 %d건 중 문장 아닌 수동 구절에 포함되지 않은 것 %d건(문장 기록까지 포함하면 미포함 %d건). 판정은 manual/regex-review.json." % (len(cands), len(uncov_phrase), len(uncov_any)), "",
      "| ID | 종류 | Pointer | 일치 | 판정 | 메모 |", "|---|---|---|---|---|---|"]
for c in uncov_phrase:
    L.append("| %s | %s | `%s` | %s | %s | %s |" % (c["id"], c["kind"], c["pointer"], c["match"], c["review"], c["review_note"] or ""))
open(os.path.join(HERE, "issues.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
out("observations.json", {"source_sha256": sha, "status_legend": ST, "observations": obs_all})

# ---------------------------------------------------------------- review
def md(v):
    return json.dumps(v, ensure_ascii=False).replace("|", "\\|")


expr_ids_by_ptr = collections.defaultdict(list)
for x in expr:
    expr_ids_by_ptr[x["pointer"]].append(x["id"])
tok_by_ptr = {a["pointer"]: a for a in applied}
excl_ptr = {e["pointer"]: e for e in excluded}

for s in cov_segments:
    seg = s["segment"]
    m = manual.get(seg, {})
    P = ["# %s — %s" % (seg, s["label"]), "", "[← review.md 목차](./review.md)", "",
         "- 읽기 상태: **%s** · 마지막 읽은 Pointer `%s`" % ({"direct_read": "직접 읽음", "planned": "미독"}.get(s["direct_read"], s["direct_read"]), s["last_read_pointer"]),
         "- 소유 노드 %d · 소유 말단 %d · 공동 참조 문맥(소유 아님): %s" % (len(s["owned_pointers"]), len(s["owned_leaf_pointers"]), ", ".join("`%s`" % c for c in s["context_refs"]) or "없음"),
         "- 수동 기록 `%s` · 구조화 기록: source-map.json · morphology.json · expressions.json" % s["manual_record"], "",
         "## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)", "",
         "원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.", "",
         "| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |", "|---|---|---|---|---|---|---|"]
    for p in s["owned_pointers"]:
        n = by_ptr[p]
        if n["type"] in ("object", "array"):
            val = "(%s, 자식 %d)" % (n["type"], n["child_count"])
            span = n["literal_cp"]
            mo = ""
        else:
            val = md(n["value"])
            span = n.get("value_cp", n["literal_cp"])
            mo = ("제외(%s)" % excl_ptr[p]["kind"]) if p in excl_ptr else ("%d토큰" % len(tok_by_ptr[p]["tokens"]) if p in tok_by_ptr else "")
        key = "(루트)" if n["key"] is None else ("[%d]" % n["key"] if isinstance(n["key"], int) else n["key"])
        P.append("| `%s` | %s | %s | %s | %d–%d | %s | %s |" % (p or "/", key, n["type"], val, span[0], span[1], mo, ", ".join(expr_ids_by_ptr.get(p, []))))
    P += ["", "## 2. 잠정 관찰·미결 (원문과 분리)", "", "| ID | 상태 | Pointer | 관찰 |", "|---|---|---|---|"]
    for o in obs_all:
        if o["segment"] == seg:
            P.append("| %s | %s | `%s` | %s |" % (o["id"], o["status"], o["pointer"], o["text"].replace("|", "\\|")))
    P += ["", "## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)", "", "| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |", "|---|---|---|---|---|---|"]
    for x in expr:
        if x["segment"] == seg:
            P.append("| %s | `%s` | %s | %d–%d | %s | %s |" % (x["id"], x["pointer"], x["text"].replace("|", "\\|"), x["span_in_value"][0], x["span_in_value"][1], ",".join(x["facets"]), x["note"].replace("|", "\\|")))
    P += ["", "## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)", ""]
    for p in s["owned_pointers"]:
        if p in tok_by_ptr:
            P.append("- `%s`: %s" % (p, " ".join("%s/%s" % (t["form"], t["tag"]) for t in tok_by_ptr[p]["tokens"])))
    ks = [k for k in known if segment_of(k["pointer"]) == seg]
    if ks:
        P += ["", "알려진 오분절(출현별, 교정 안 함):", ""]
        for k in ks:
            P.append("- `%s` 「%s」 [%d,%d) → %s — %s" % (k["pointer"], k["surface"], k["span"][0], k["span"][1], " ".join(k["raw_tokens"]), k["impact"]))
    open(os.path.join(HERE, "review-part-%s.md" % seg), "w", encoding="utf-8").write("\n".join(P) + "\n")

# 컬럼 구성 표
pat_rows = collections.OrderedDict()
for n in nodes:
    fp = field_pattern(n["pointer"])
    r = pat_rows.setdefault(fp, {"types": collections.Counter(), "count": 0, "first": n["pointer"], "example": None, "empty": 0, "child": collections.Counter(), "lens": []})
    r["types"][n["type"]] += 1
    r["count"] += 1
    if n["type"] in ("object", "array"):
        r["child"][n["child_count"]] += 1
        if n["child_count"] == 0:
            r["empty"] += 1
    else:
        if r["example"] is None:
            r["example"] = (n["pointer"], n["value"])
        if n["value"] == "":
            r["empty"] += 1
        if n["type"] == "string":
            r["lens"].append(len(n["value"]))
parent_count = {"/": 1, "/categories/*": 17, "/categories/*/common_concerns/*": 51}
head = open(os.path.join(HERE, "manual", "review-head.md"), encoding="utf-8").read()
R = [head.rstrip(), "", "## 컬럼 구성 표 (원본 컬럼명/경로 패턴 · 자료형 · 중첩 · 원문 예시와 위치)", "",
     "`*` 는 배열 인덱스. 출현 수는 원문 실측. 선택적 필드 여부는 상위 객체 수와 출현 수 비교로 판정.", "",
     "| 경로 패턴 | 원본 컬럼명 | 자료형 | 중첩 구조 | 출현 | 선택적? | 빈 값 | 길이(코드포인트) 최소–최대 | 원문 예시 | 예시 위치 |", "|---|---|---|---|---|---|---|---|---|---|"]
for fp, r in pat_rows.items():
    key = fp.rsplit("/", 1)[-1] or "(루트)"
    t = ", ".join("%s" % k for k in r["types"])
    nest = ("자식 수 %s" % ", ".join("%d(×%d)" % (k, v) for k, v in sorted(r["child"].items()))) if r["child"] else "말단"
    parent = fp.rsplit("/", 1)[0] or "/"
    opt = "아니오(모든 상위 객체에 있음)" if fp == "/" or parent_count.get(parent, None) in (None, r["count"]) else "예"
    ex = md(r["example"][1]) if r["example"] else "(컨테이너)"
    if r["example"] and len(ex) > 70:
        ex = ex[:70] + "…(전체는 review-part)"
    R.append("| `%s` | %s | %s | %s | %d | %s | %d | %s | %s | `%s` |" % (fp, key, t, nest, r["count"], opt, r["empty"],
             ("%d–%d" % (min(r["lens"]), max(r["lens"]))) if r["lens"] else "", ex, r["example"][0] if r["example"] else r["first"] or "/"))
R += ["", "## 구획 목차 (모든 값은 review-part-*.md 에 원본 컬럼명 그대로)", "",
      "| 구획 | 범위 | 소유 노드 | 소유 말단 | 직접 읽기 | 표현 | 관찰 | 파일 |", "|---|---|---|---|---|---|---|---|"]
for s in cov_segments:
    R.append("| %s | %s | %d | %d | %s | %d | %d | [review-part-%s.md](./review-part-%s.md) |" % (s["segment"], s["label"], len(s["owned_pointers"]), len(s["owned_leaf_pointers"]), s["direct_read"], s["expressions"], s["observations"], s["segment"], s["segment"]))
open(os.path.join(HERE, "review.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")

log += ["sha256 %s" % sha, "nodes %d leaf %d strings %d" % (len(nodes), len(leaf_ptrs), sum(1 for n in nodes if n["type"] == "string")),
        "morph applied %d excluded %d tokens %d known_missegmentation %d" % (len(applied), len(excluded), sum(len(a["tokens"]) for a in applied), len(known)),
        "manual expressions %d regex %d uncovered_phrase %d uncovered_any %d unreviewed %d" % (len(expr), len(cands), len(uncov_phrase), len(uncov_any), sum(1 for c in uncov_phrase if not c["review"])),
        "segments direct_read %d/%d" % (sum(1 for s in cov_segments if s["direct_read"] == "direct_read"), len(cov_segments))]
open(os.path.join(HERE, "build-output.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
print("\n".join(log))
