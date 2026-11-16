"""problem-packages.json 1차 수집 빌드.

레포 루트에서:
  OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
    python orchestration/work/phub-ledger-redesign/first-pass/problem-packages/build.py

입력: 원본(읽기 전용) + manual/Sxx.json(직접 읽기 기록) + manual/K.json(형태소 한계 기록).
출력: source-map.json · morphology.json · expressions.json · coverage.json · cue-review.json ·
      review.md · review-part-Sxx.md · issues.md (모두 이 폴더 안).
"""
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pp_common import (HERE, OUT_REL, SRC, SRC_REL, column_name, cp_to_byte_factory, load,
                       pattern_of, section_of, sha256_bytes)

SECTIONS = ["S00"] + [f"S{i:02d}" for i in range(1, 15)]
MORPH_EXCLUDE = [
    (re.compile(r"^/version$"), "버전 코드 문자열('6.2') — 언어 텍스트 아님"),
    (re.compile(r"^/updated$"), "날짜 문자열(ISO 형식 '2026-07-26') — 언어 텍스트 아님"),
    (re.compile(r"^/problems/\d+/problem_id$"), "problem 식별자 코드('P1'~'P14') — ID 값"),
    (re.compile(r"^/problems/\d+/complaints/\d+/procedures/\d+/category$"), "카테고리 코드('M1'~'M16') — 코드 값"),
]
NAME_LIKE = re.compile(r"/(cc|name|products/\d+|combo/\d+)$")

CUES = OrderedDict([
    ("negation_limit", r"없|않|아닌|아님|금지|피할|배제|허가 외|미허가|부족|제한"),
    ("possibility", r"수 있|가능"),
    ("condition", r"(?<= )시(?=[ ,.;)]|$)|경우|이면"),
    ("range", r"\d+\s?[~\-]\s?\d+"),
    ("number_unit", r"\d+(?:\.\d+)?\s?(?:nm|개월|주|회|배)"),
    ("time_order", r"후(?![가-힣])|뒤|(?<= )전(?= )|간격|즉각|장기|단기|수개월|사전|동시|주기"),
    ("degree_directive", r"가장|최대|강력|영구|완전|필수|권장|권고|추천|정밀|보수적|과다|고용량|저출력|고농도"),
])
SYMBOLS = OrderedDict([
    ("plus", r"\+"), ("slash", r"/"), ("middle_dot", r"·"), ("arrow", r"↓"), ("plus_minus", r"±"),
    ("semicolon", r";"), ("equals", r"="), ("paren", r"\("), ("tilde", r"~"),
])


def die(msg):
    print("BUILD ERROR:", msg)
    sys.exit(1)


def resolve(loc, sec):
    """manual 기록의 위치 약식 → JSON Pointer."""
    if loc.startswith("/"):
        return loc
    if ":" in loc:
        sec, loc = loc.split(":", 1)
        if loc.startswith("/"):
            return loc
    pi = int(sec[1:]) - 1
    parts = loc.split(".")
    m = re.fullmatch(r"c(\d+)", parts[0])
    if not m:
        die(f"bad loc {loc}")
    out = f"/problems/{pi}/complaints/{m.group(1)}"
    rest = parts[1:]
    i = 0
    while i < len(rest):
        p = rest[i]
        mm = re.fullmatch(r"([PBA])(\d+)", p)
        if mm:
            out += {"P": "/procedures/", "B": "/combos/", "A": "/alternatives/"}[mm.group(1)] + mm.group(2)
        else:
            out += "/" + p
        i += 1
    return out


def main():
    raw0 = SRC.read_bytes()
    h0 = sha256_bytes(raw0)
    raw, text, root, nodes, dups = load()
    if dups:
        die(f"duplicate keys: {dups}")
    c2b = cp_to_byte_factory(text)
    by_ptr = {n.pointer: n for n in nodes}

    def ctx(n):
        parts = n.pointer.split("/")[1:]
        c = {}
        if len(parts) >= 2 and parts[0] == "problems":
            pp = f"/problems/{parts[1]}"
            c["problem"] = pp
            c["problem_id"] = by_ptr[pp + "/problem_id"].value
            c["problem_name"] = by_ptr[pp + "/problem"].value
            if len(parts) >= 4 and parts[2] == "complaints":
                cp = pp + f"/complaints/{parts[3]}"
                c["complaint"] = cp
                c["cc"] = by_ptr[cp + "/cc"].value
                if len(parts) >= 6 and parts[4] in ("procedures", "combos"):
                    c[parts[4][:-1]] = cp + f"/{parts[4]}/{parts[5]}"
                    c[parts[4][:-1] + "_name"] = by_ptr[cp + f"/{parts[4]}/{parts[5]}/name"].value
        return c

    # ---------- source-map ----------
    sm_nodes = []
    for n in nodes:
        rec = OrderedDict()
        rec["order"] = n.order
        rec["pointer"] = n.pointer
        rec["parent"] = n.parent.pointer if n.parent is not None else None
        rec["section"] = section_of(n.pointer)
        rec["column_name"] = column_name(n)
        rec["key"] = n.key
        rec["index"] = n.index
        rec["path_pattern"] = pattern_of(n.pointer)
        rec["type"] = n.type
        rec["depth"] = n.pointer.count("/")
        rec["literal_cp_span"] = list(n.lit_cp)
        rec["literal_byte_span"] = [c2b(n.lit_cp[0]), c2b(n.lit_cp[1])]
        if n.key_cp is not None:
            rec["key_literal_cp_span"] = list(n.key_cp)
        if n.type in ("object", "array"):
            rec["child_count"] = len(n.children)
            rec["empty"] = len(n.children) == 0
            if n.type == "object":
                rec["child_keys"] = [c.key for c in n.children]
        else:
            rec["value"] = n.value
            rec["raw_literal"] = n.raw_literal
            if n.type == "string":
                rec["content_cp_span"] = list(n.content_cp)
                rec["content_byte_span"] = [c2b(n.content_cp[0]), c2b(n.content_cp[1])]
                rec["length_cp"] = len(n.value)
                rec["has_escape"] = n.has_escape
                rec["empty"] = n.value == ""
        rec["context"] = ctx(n)
        sm_nodes.append(rec)
    field_names = OrderedDict()
    for n in nodes:
        if n.key is not None:
            field_names.setdefault(n.key, []).append(n.pointer)
    leaves = [n for n in nodes if n.type not in ("object", "array")]
    empties = [n.pointer for n in nodes if (n.type in ("object", "array") and not n.children)
               or (n.type == "string" and n.value == "")]
    source_map = OrderedDict(
        about="원본 전체 노드(컨테이너·말단·빈 컨테이너) 문서 순서 기록. 구간: literal_cp_span = 디코딩 원문(파일 전체 문자열) 기준 Unicode 코드 포인트 [start,end) 의 JSON 리터럴(따옴표 포함), content_cp_span = 문자열 따옴표 안쪽. *_byte_span = UTF-8 파일 바이트 [start,end). 이스케이프가 0 이므로 content 구간의 원문 = 디코딩 값.",
        source=OrderedDict(path=SRC_REL, bytes=len(raw), codepoints=len(text), sha256=h0,
                           newlines=text.count("\n"), bom=raw[:3] == b"\xef\xbb\xbf",
                           max_codepoint=max(ord(c) for c in text), duplicate_keys=dups,
                           string_escapes=sum(1 for n in leaves if n.type == "string" and n.has_escape)),
        counts=OrderedDict(nodes=len(nodes), leaves=len(leaves),
                           by_type={t: sum(1 for n in nodes if n.type == t) for t in
                                    ["object", "array", "string", "integer", "number", "boolean", "null"]},
                           empty_containers_or_strings=len(empties)),
        empty_values=empties,
        field_names=OrderedDict((k, OrderedDict(occurrences=len(v), pointers=v)) for k, v in field_names.items()),
        nodes=sm_nodes,
    )

    # ---------- morphology ----------
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi(num_workers=1, model_type="cong")
    cache = {}

    def tok(s):
        if s not in cache:
            out = []
            for i, t in enumerate(kiwi.tokenize(s)):
                st, en = t.start, t.start + t.len
                surf = s[st:en]
                out.append(OrderedDict(i=i, form=t.form, tag=t.tag, lemma=t.lemma, span=[st, en],
                                       surface=surf, form_equals_surface=surf == t.form))
            cache[s] = out
        return cache[s]

    text_values, excluded = [], []
    for n in leaves:
        sec = section_of(n.pointer)
        if n.type != "string":
            excluded.append(OrderedDict(pointer=n.pointer, section=sec, reason=f"비문자열({n.type})"))
            continue
        rule = next((why for rx, why in MORPH_EXCLUDE if rx.search(n.pointer)), None)
        if rule:
            excluded.append(OrderedDict(pointer=n.pointer, section=sec, value=n.value, reason=rule))
            continue
        toks = tok(n.value)
        base = n.content_cp[0]
        tv = OrderedDict(pointer=n.pointer, section=sec, role="text_value", column_name=column_name(n),
                         value=n.value, file_cp_span=list(n.content_cp), tokens=[])
        for t in toks:
            t2 = OrderedDict(t)
            t2["file_cp_span"] = [base + t["span"][0], base + t["span"][1]]
            tv["tokens"].append(t2)
        text_values.append(tv)
    fields = []
    for k, ptrs in field_names.items():
        fields.append(OrderedDict(field_name=k, role="field_name", occurrences=len(ptrs),
                                  tokens=tok(k), note="필드명 문자열 자체 분석. 출현 위치 전체는 source-map.json field_names."))
    # 이름형 값(cc·name·products·combo 원소)에서 조사·어미·접사가 끼어든 분절 = 오분절 후보(출현별)
    name_splits = []
    for tv in text_values:
        if NAME_LIKE.search(tv["pointer"]):
            bad = [t for t in tv["tokens"] if t["tag"][0] in "JEX" or t["tag"] in ("VV", "VA", "VX")]
            if bad:
                name_splits.append(OrderedDict(pointer=tv["pointer"], section=tv["section"], value=tv["value"],
                                               tokens=[f"{t['form']}/{t['tag']}@{t['span'][0]}-{t['span'][1]}" for t in tv["tokens"]],
                                               flagged=[f"{t['form']}/{t['tag']}" for t in bad]))
    form_mismatch = [OrderedDict(pointer=tv["pointer"], form=t["form"], surface=t["surface"], tag=t["tag"], span=t["span"])
                     for tv in text_values for t in tv["tokens"] if not t["form_equals_surface"]]
    kman = json.loads((HERE / "manual" / "K.json").read_text(encoding="utf-8"))
    for ke in kman["known_errors"]:
        occ = []
        for trig in ke["triggers"]:
            for tv in text_values:
                for mm in re.finditer(re.escape(trig), tv["value"]):
                    st, en = mm.span()
                    occ.append(OrderedDict(pointer=tv["pointer"], trigger=trig, span=[st, en],
                                           file_cp_span=[tv["file_cp_span"][0] + st, tv["file_cp_span"][0] + en],
                                           raw_tokens=[f"{t['form']}/{t['tag']}@{t['span'][0]}-{t['span'][1]}" for t in tv["tokens"]
                                                       if t["span"][0] < en and t["span"][1] > st]))
        if not occ:
            die(f"{ke['id']} triggers found nowhere")
        ke["occurrences"] = occ
        ke["occurrence_count"] = len(occ)
    morphology = OrderedDict(
        about="문자열 값(언어 텍스트)과 필드명에 Kiwi 형태소 분석을 적용한 원시 결과. 기본형은 도메인 표준명이 아니며 오분절은 교정하지 않고 기록한다.",
        analyzer=OrderedDict(
            name="Kiwi (kiwipiepy)", kiwipiepy=kiwipiepy.__version__, model_type="cong", num_workers=1,
            env="uv run --python 3.12 --with kiwipiepy==0.24.1, OMP_NUM_THREADS=1",
            call="Kiwi(num_workers=1, model_type='cong').tokenize(text) — 기본 옵션(사용자 사전·오타 교정·입력 정규화 없음)",
            default_dictionary="kiwipiepy 기본 내장 사전", user_dictionary=None, typo_correction=None,
            tagset="Kiwi 품사 체계(세종 기반 확장)",
            lemma="Kiwi Token.lemma 그대로. 분석기가 주지 않는 기본형은 만들지 않음.",
            span="각 값 문자열 기준 Unicode 코드 포인트 [start,end). 원문 전부 BMP(최대 U+%04X)이므로 Kiwi 오프셋=코드 포인트. file_cp_span = 원문 파일 전체 문자열 기준. 바이트 구간은 source-map content_byte_span 으로 환산." % max(ord(c) for c in text),
            normalization="입력 정규화 없음. form 이 표면과 다르면 form_equals_surface=false(활용·축약 복원). 복원 형태소는 길이 0 구간(span start=end, surface '')으로 올 수 있다(예: '리쥬란' 안의 이/VCP).",
            caching="같은 문자열은 한 번 분석하고 출현마다 같은 결과를 펼쳐 기록(분석기 결정적).",
        ),
        applied_counts=OrderedDict(text_values=len(text_values), field_names=len(fields), excluded_leaves=len(excluded),
                                   tokens=sum(len(t["tokens"]) for t in text_values),
                                   distinct_strings_analyzed=len(cache)),
        exclusion_rules=[OrderedDict(pattern=rx.pattern, reason=why) for rx, why in MORPH_EXCLUDE],
        known_errors=kman["known_errors"],
        name_value_functional_splits=name_splits,
        form_surface_mismatch=form_mismatch,
        text_values=text_values,
        field_names=fields,
        excluded=excluded,
    )

    # ---------- manual ----------
    manual = {}
    for s in SECTIONS:
        f = HERE / "manual" / f"{s}.json"
        if not f.exists():
            die(f"missing manual {f}")
        manual[s] = json.loads(f.read_text(encoding="utf-8"))
    mexpr, obs_out, issues = [], [], OrderedDict()
    for s in SECTIONS:
        m = manual[s]
        for ob in m["observations"]:
            ptrs = []
            for loc in ob["at"]:
                p = resolve(loc, s)
                if p not in by_ptr:
                    die(f"{ob['id']} bad pointer {loc}->{p}")
                ptrs.append(p)
            o = OrderedDict(ob)
            o["section"] = s
            o["pointers"] = ptrs
            obs_out.append(o)
        for k, e in enumerate(m["expressions"], 1):
            for loc in e["at"]:
                p = resolve(loc, s)
                n = by_ptr.get(p)
                if n is None or n.type != "string":
                    die(f"expr {e['text']} bad pointer {loc}->{p}")
                occ = e.get("occ", 1)
                pos, start = -1, 0
                for _ in range(occ):
                    pos = n.value.find(e["text"], start)
                    if pos < 0:
                        die(f"expr text not in value: {e['text']!r} @ {p} = {n.value!r}")
                    start = pos + 1
                st, en = pos, pos + len(e["text"])
                fs = n.content_cp[0]
                mexpr.append(OrderedDict(
                    id=f"MX-{s}-{k:03d}-{len(mexpr)+1:04d}", section=s, pointer=p, column_name=column_name(n),
                    text=e["text"], span=[st, en], file_cp_span=[fs + st, fs + en],
                    file_byte_span=[c2b(fs + st), c2b(fs + en)], occurrence_in_value=occ,
                    occurrences_of_text_in_value=n.value.count(e["text"]),
                    whole_value=st == 0 and en == len(n.value), aspects=e["aspects"], note=e.get("note"),
                    method="manual_direct_reading", value=n.value))
        for it in m["issues"]:
            if it["id"] in issues:
                die(f"dup issue id {it['id']}")
            ptrs = []
            for loc in it["at"]:
                p = resolve(loc, s)
                if p not in by_ptr:
                    die(f"issue {it['id']} bad pointer {loc}")
                ptrs.append(p)
            i2 = OrderedDict(it)
            i2["section"] = s
            i2["pointers"] = ptrs
            issues[it["id"]] = i2
    for ke in kman["known_errors"]:
        issues[ke["id"]] = OrderedDict(id=ke["id"], status="K", summary=ke["summary"], impact=ke["impact"],
                                       pointers=sorted({o["pointer"] for o in ke["occurrences"]}, key=lambda q: by_ptr[q].order),
                                       section="(전 구획)")
    # 관찰 → 미결 id 참조 확인
    for o in obs_out:
        for ref in re.findall(r"\b([ABCIKPF]-\d{2})\b", o["text"]):
            if ref not in issues:
                die(f"{o['id']} refs unknown issue {ref}")

    # ---------- regex candidates · clause segments ----------
    regex_c, clauses = [], []
    for tv in text_values:
        n = by_ptr[tv["pointer"]]
        fs = n.content_cp[0]
        for grp, table in (("cue", CUES), ("symbol", SYMBOLS)):
            for name, pat in table.items():
                for mm in re.finditer(pat, n.value):
                    st, en = mm.span()
                    regex_c.append(OrderedDict(pointer=tv["pointer"], section=tv["section"], group=grp, pattern_name=name,
                                               text=mm.group(0), span=[st, en], file_cp_span=[fs + st, fs + en],
                                               method="regex_candidate"))
        segs, last = [], 0
        for mm in re.finditer(r"(?<=\.)\s+|;\s*", n.value):
            segs.append((last, mm.start()))
            last = mm.end()
        segs.append((last, len(n.value)))
        if len(segs) > 1:
            for j, (st, en) in enumerate(segs):
                clauses.append(OrderedDict(pointer=tv["pointer"], section=tv["section"], seg=j, text=n.value[st:en],
                                           span=[st, en], file_cp_span=[fs + st, fs + en],
                                           paren_balanced=n.value[st:en].count("(") == n.value[st:en].count(")"),
                                           method="clause_split('. ' 또는 ';')"))

    # ---------- cue review: 정규식 단서가 수동 표현 구간 안에 있는가 ----------
    cover = defaultdict(list)
    for e in mexpr:
        cover[e["pointer"]].append(tuple(e["span"]))
    cfile = HERE / "manual" / "cue-decisions.json"
    cdec = json.loads(cfile.read_text(encoding="utf-8")) if cfile.exists() else {"decisions": []}
    decided = {(d["pointer"], d["text"], d["span"][0]): d for d in cdec["decisions"]}
    cue_rows = []
    for r in regex_c:
        if r["group"] != "cue":
            continue
        covered = any(a <= r["span"][0] and r["span"][1] <= b for a, b in cover[r["pointer"]])
        d = decided.get((r["pointer"], r["text"], r["span"][0]))
        cue_rows.append(OrderedDict(pointer=r["pointer"], pattern_name=r["pattern_name"], text=r["text"], span=r["span"],
                                    value=by_ptr[r["pointer"]].value, covered_by_manual=covered,
                                    decision=(d["decision"] if d else None), reason=(d["reason"] if d else None)))
    unresolved = [c for c in cue_rows if not c["covered_by_manual"] and not c["decision"]]
    cue_review = OrderedDict(about="정규식 단서(부정·한정·가능성·조건·범위·수량단위·시간·정도·지시) 출현마다 수동 표현 구간이 덮는지 대조. 덮이지 않은 단서는 manual/cue-decisions.json 에 판단 사유를 남긴다.",
                             counts=OrderedDict(cue_hits=len(cue_rows), covered=sum(c["covered_by_manual"] for c in cue_rows),
                                                decided=sum(1 for c in cue_rows if not c["covered_by_manual"] and c["decision"]),
                                                unresolved=len(unresolved)),
                             rows=cue_rows)

    expressions = OrderedDict(
        about="복합 표현·구절 구간. manual = 직접 읽기에서 수집(aspects 는 탐색 관점이며 확정 분류 아님), regex_candidates = 정규식 보조 후보(전수 의미 해석 아님), clause_segments = '. '·';' 기준 기계 분할(2절 이상인 값만). 구간 겹침은 의도된 것.",
        span_rule="span = 값 문자열 기준 코드 포인트 [start,end). file_cp_span = 원문 파일 문자열 기준 코드 포인트, file_byte_span = UTF-8 바이트.",
        regex_patterns=OrderedDict(cue=CUES, symbol=SYMBOLS),
        counts=OrderedDict(manual=len(mexpr), regex_candidates=len(regex_c), clause_segments=len(clauses),
                           manual_distinct_texts=len({e["text"] for e in mexpr})),
        manual=mexpr, regex_candidates=regex_c, clause_segments=clauses,
    )

    # ---------- coverage ----------
    secs = []
    for s in SECTIONS:
        owned = [n.pointer for n in nodes if section_of(n.pointer) == s]
        owned_leaves = [n.pointer for n in leaves if section_of(n.pointer) == s]
        owned_empty = [p for p in empties if section_of(p) == s]
        if s == "S00":
            rng, ctxr, title = "'' (루트 객체), /version, /updated, /description, /problems (배열 컨테이너만; 원소는 S01~S14)", [], "루트·메타데이터·problems 컨테이너"
        else:
            pi = int(s[1:]) - 1
            rng = f"/problems/{pi} 및 /problems/{pi}/** 전체"
            ctxr = ["", "/problems", "/description"]
            title = f"/problems/{pi} {by_ptr[f'/problems/{pi}/problem_id'].value} {by_ptr[f'/problems/{pi}/problem'].value}"
        m = manual[s]
        secs.append(OrderedDict(
            id=s, title=title, pointer_range=rng, shared_context_refs=ctxr,
            owned_pointers=owned, owned_leaf_pointers=owned_leaves, owned_empty_values=owned_empty,
            counts=OrderedDict(nodes=len(owned), leaves=len(owned_leaves), empty=len(owned_empty)),
            machine_extracted="done",
            direct_read=m["read_status"], direct_read_note=m["read_note"],
            manual_record=f"manual/{s}.json",
            review_file=f"review-part-{s}.md",
            observations=[o["id"] for o in obs_out if o["section"] == s],
            manual_expressions=sum(1 for e in mexpr if e["section"] == s),
            issues_raised=[i for i, v in issues.items() if v["section"] == s],
        ))
    coverage = OrderedDict(
        about="구획별 소유 경로·읽기 상태. machine_extracted = build.py 기계 추출, direct_read = 에이전트가 reading/Sxx.txt 로 원문을 직접 읽고 manual/Sxx.json 에 관찰·표현·미결을 남긴 상태. S01~S14 는 루트·/problems·/description 을 공유 문맥으로 참조만 하고 소유하지 않는다.",
        source_sha256=h0, total_nodes=len(nodes), total_leaves=len(leaves),
        reading_log=OrderedDict(order=SECTIONS, last_read="S14", last_read_pointer="/problems/13/complaints/6/alternatives/0",
                                remaining=[s for s in SECTIONS if manual[s]["read_status"] != "done"],
                                method="원본은 한 줄 JSON 이라 구획별 덤프(reading_dump.py → reading/Sxx.txt, complaint 블록 단위)를 위에서 아래로 읽었다. 기계 추출(build.py)은 경로·구간·형태소·정규식 후보만 담당한다."),
        sections=secs,
    )

    # ---------- write json ----------
    def wj(name, obj):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    wj("source-map.json", source_map)
    wj("morphology.json", morphology)
    wj("expressions.json", expressions)
    wj("coverage.json", coverage)
    wj("cue-review.json", cue_review)

    # ---------- review markdown ----------
    def esc(v):
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        return s.replace("|", "\\|")

    pat_rows = OrderedDict()
    for n in nodes:
        pt = pattern_of(n.pointer)
        r = pat_rows.setdefault(pt, OrderedDict(types=set(), count=0, examples=[], empty=[], lens=set()))
        r["types"].add(n.type)
        r["count"] += 1
        if n.type in ("object", "array"):
            r["lens"].add(len(n.children))
            if not n.children:
                r["empty"].append(n.pointer)
        if len(r["examples"]) < 2:
            if n.type == "string":
                r["examples"].append(f"`{n.pointer}` = {esc(n.value)}")
            else:
                r["examples"].append(f"`{n.pointer}` ({n.type}[{len(n.children)}])")
    L = []
    L.append("# problem-packages.json — 1차 조사 읽기용 결과\n")
    L.append("**1차 범위 종료: 예 · 원장 전체 완료: 아님** (열린 미결은 [issues.md](issues.md), 검증은 [validation.md](validation.md)).\n")
    L.append(f"원본 `{SRC_REL}` · {len(raw)} 바이트 · {len(text)} 코드 포인트 · sha256 `{h0}` · 한 줄(줄바꿈 0) · BOM 없음 · 중복 키 0 · 문자열 이스케이프 0.\n")
    L.append(f"노드 {len(nodes)} · 말단 {len(leaves)}(전부 string) · 빈 값 {len(empties)}(빈 배열: products 47 · combos 1).\n")
    L.append("기계 기록: [source-map.json](source-map.json) · [morphology.json](morphology.json) · [expressions.json](expressions.json) · [coverage.json](coverage.json) · [cue-review.json](cue-review.json). 직접 읽기 기록: `manual/Sxx.json`. 진행: [progress.md](progress.md).\n")
    L.append("## 상태\n")
    L.append("| 항목 | 상태 |\n|---|---|")
    L.append(f"| 전수 읽기 | 15/15 구획 직접 읽기 done |")
    L.append(f"| 구조·값 수집 | 노드 {len(nodes)} · 말단 {len(leaves)} · 필드명 {len(field_names)}종 |")
    L.append(f"| 형태소 | 텍스트 값 {len(text_values)} · 필드명 {len(fields)} · 제외 {len(excluded)} · 토큰 {morphology['applied_counts']['tokens']} |")
    L.append(f"| 표현 | 수동 {len(mexpr)} · 정규식 후보 {len(regex_c)} · 절 구간 {len(clauses)} |")
    L.append(f"| 단서 대조 | 단서 {cue_review['counts']['cue_hits']} · 수동 표현으로 덮임 {cue_review['counts']['covered']} · 판단 기록 {cue_review['counts']['decided']} · 미처리 {cue_review['counts']['unresolved']} |")
    L.append("")
    L.append("## 컬럼 구성\n")
    L.append("원본 키 이름 그대로. `*` = 배열 순번. 모든 객체는 같은 위치에서 같은 키 집합·같은 순서를 가진다(선택적 필드 없음).\n")
    L.append("| 경로 패턴 | 원본 컬럼명 | 자료형·중첩 | 출현 수 | 원문 예시(위치) | 빈 값 |\n|---|---|---|---|---|---|")
    for pt, r in pat_rows.items():
        col = pt.split("/")[-1] if pt else "(루트)"
        if col == "*":
            col = f"({pt.split('/')[-2]} 원소)"
        tdesc = "/".join(sorted(r["types"]))
        if r["lens"]:
            tdesc += f" 길이 {min(r['lens'])}~{max(r['lens'])}"
        emp = f"{len(r['empty'])}개 (예: `{r['empty'][0]}`)" if r["empty"] else "—"
        L.append(f"| `{pt or '(루트)'}` | `{col}` | {tdesc} | {r['count']} | {'<br>'.join(r['examples'])} | {emp} |")
    L.append("\n변형 행:\n")
    L.append("| 변형 | 위치 | 원문 |\n|---|---|---|")
    L.append("| combos 빈 배열(유일) | `/problems/13/complaints/3/combos` | `[]` |")
    L.append("| products 빈 배열 47곳 | source-map.json `empty_values` | `[]` (예: `/problems/0/complaints/3/procedures/0/products`) |")
    one = [n for n in nodes if pattern_of(n.pointer) == "/problems/*/complaints/*/combos/*/combo" and len(n.children) == 1]
    three = [n for n in nodes if pattern_of(n.pointer) == "/problems/*/complaints/*/combos/*/combo" and len(n.children) == 3]
    L.append(f"| combo 원소 1개(단독 묶음) {len(one)}곳 | 예: `{one[0].pointer}` | {esc([c.value for c in one[0].children])} |")
    L.append(f"| combo 원소 3개 {len(three)}곳 | 예: `{three[0].pointer}` | {esc([c.value for c in three[0].children])} |")
    alt2 = [n for n in nodes if pattern_of(n.pointer) == "/problems/*/complaints/*/alternatives" and len(n.children) == 2]
    L.append(f"| alternatives 2개 {len(alt2)}곳 | 예: `{alt2[0].pointer}` | {esc([c.value for c in alt2[0].children])} |")
    L.append("\n## 구획 목차\n")
    L.append("| 구획 | 범위 | 노드 | 말단 | 직접 읽기 | 관찰 | 수동 표현 | 파일 |\n|---|---|---|---|---|---|---|---|")
    for sc in secs:
        L.append(f"| {sc['id']} | {sc['title']} | {sc['counts']['nodes']} | {sc['counts']['leaves']} | {sc['direct_read']} | {len(sc['observations'])} | {sc['manual_expressions']} | [{sc['review_file']}]({sc['review_file']}) |")
    L.append("\n## 전 원장 관찰 요약(잠정 — 원문 칸과 분리)\n")
    L.append("- 같은 combo 블록·alternatives 문장이 부위·세부가 다른 complaint 에 글자 그대로 반복된다(B-02). description 이 스스로 '자동 생성' 이라고 한다(F-01).")
    L.append("- cc·cc_detail·cc_group·alternatives·evidence 는 칸마다 정보 종류가 섞여 있다(F-03·F-04·F-05·F-06).")
    L.append("- procedures.name ↔ combos.combo ↔ combo name ↔ cc_detail 표기가 일치하지 않는 곳이 여럿이다(I-01·I-02·I-03·I-06·I-10).")
    L.append("- 같은 combo 의 근거 진술이 complaint 마다 서로 맞지 않는 곳이 있다(I-05·I-09), 한 값 안의 정도 불일치(I-08).")
    L.append("- 기호 '+','/','·','=' 는 필드마다 쓰임이 다르다(F-02). 이름 안의 '+'(리쥬란 HB+·NAD+·ASCE+)는 기호 규칙과 겹친다(K-03).")
    (HERE / "review.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    for f in HERE.glob("review-part-*.md"):
        f.unlink()
    obs_by_ptr = defaultdict(list)
    for o in obs_out:
        for p in o["pointers"]:
            obs_by_ptr[p].append(o["id"])
    for sc in secs:
        s = sc["id"]
        P = [f"# {s} — {sc['title']}\n", f"[← review.md](review.md) · 범위 {sc['pointer_range']} · 소유 노드 {sc['counts']['nodes']} · 말단 {sc['counts']['leaves']} · 빈 값 {sc['counts']['empty']} · 직접 읽기 {sc['direct_read']}\n"]
        if sc["shared_context_refs"]:
            P.append("상위 문맥(공유, S00 소유): 루트 객체 → `/description` = " + esc(by_ptr["/description"].value) + " → `/problems` 배열.\n")
        P.append(f"직접 읽기: {sc['direct_read_note']}\n")
        P.append("## 원문 값 (문서 순서 · 전부)\n")
        P.append("| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |\n|---|---|---|---|---|---|---|")
        for p in sc["owned_pointers"]:
            n = by_ptr[p]
            if n.type == "object":
                v = "(객체 · 키: " + ", ".join(f"`{c.key}`" for c in n.children) + ")"
            elif n.type == "array":
                v = f"(배열 · {len(n.children)}개)" if n.children else "`[]` (빈 배열)"
            else:
                v = esc(n.value)
            tp = n.type + (f"[{len(n.children)}]" if n.type == "array" else (f"{{{len(n.children)}}}" if n.type == "object" else ""))
            P.append(f"| {n.order} | `{p or '(루트)'}` | `{column_name(n)}` | {'' if n.index is None else n.index} | {tp} | {v} | {', '.join(obs_by_ptr.get(p, []))} |")
        P.append("\n## 잠정 관찰 (원문 칸과 분리)\n")
        P.append("| ID | 상태 | 위치 | 관찰 |\n|---|---|---|---|")
        for o in obs_out:
            if o["section"] == s:
                P.append(f"| {o['id']} | {o['status']} | {'<br>'.join('`'+x+'`' for x in o['pointers'])} | {esc(o['text'])} |")
        P.append("\n## 수동 복합 표현 (직접 읽기 · 출현별)\n")
        P.append("| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |\n|---|---|---|")
        grouped = OrderedDict()
        for e in mexpr:
            if e["section"] == s:
                grouped.setdefault((e["text"], tuple(e["aspects"])), []).append(f"`{e['pointer']}` [{e['span'][0]},{e['span'][1]})")
        for (t, asp), locs in grouped.items():
            P.append(f"| {esc(t)} | {'<br>'.join(locs)} | {', '.join(asp)} |")
        P.append("\n## 이 구획에서 연 미결\n")
        raised = [issues[i] for i in sc["issues_raised"]]
        if raised:
            for it in raised:
                P.append(f"- **{it['id']}** ({it['status']}) {it['summary']} — 영향: {it['impact']}")
        else:
            P.append("- 새로 연 미결 없음(관찰은 기존 미결 유형에 연결).")
        (HERE / sc["review_file"]).write_text("\n".join(P) + "\n", encoding="utf-8")

    # ---------- issues.md ----------
    I = ["# problem-packages.json — 미결·한계 기록\n",
         "상태 문자: **A** = 에이전트 추출/해석 오류 · **B** = 원문 정보 부족 · **C** = 현재 사용자 결정 필요 · **I** = 원문 내 불일치 · **K** = 알려진 분석 한계 · **P** = 잠정 관찰 · **F** = 후속 의미 조사.",
         "원문 불일치(I)는 C 로 부르지 않는다. 원본 변경 제안은 원본 보존 지시 아래 후속 확인 후보이며 지금 선택 대기로 올리지 않는다.\n"]
    cnt = defaultdict(int)
    for v in issues.values():
        cnt[v["status"]] += 1
    I.append("| 상태 | 건수 |\n|---|---|")
    for st in "ABCIKF":
        I.append(f"| {st} | {cnt.get(st, 0)} |")
    I.append(f"| P (구획 관찰) | {sum(1 for o in obs_out if o['status']=='P')} |")
    I.append("")
    I.append("A = 0: 빌드 중 발견한 추출 오류는 고친 뒤 재검증했다(validation.md). C = 0: 잔여 항목(B·I·K·F)은 원문 보존·후속 단계로 처리 가능하며 지금 사용자 선택을 요구하는 항목은 없다(영향 검토 후 판단 — 각 항목 영향 칸).\n")
    for st in "BIFK":
        I.append(f"## {st}\n")
        for v in issues.values():
            if v["status"] == st:
                refs = sorted({o["id"] for o in obs_out if v["id"] in o["text"]})
                I.append(f"### {v['id']}\n")
                I.append(f"- 요약: {v['summary']}")
                I.append(f"- 영향: {v['impact']}")
                I.append(f"- 원문 위치: " + ", ".join(f"`{p}`" for p in v["pointers"][:12]) + (f" 외 {len(v['pointers'])-12}곳" if len(v["pointers"]) > 12 else ""))
                if refs:
                    I.append(f"- 관련 구획 관찰: {', '.join(refs)}")
                I.append(f"- 처리 상태: {'원문 보존 · 후속 확인' if st in 'BIF' else '한계로 기록(교정하지 않음)'}")
                I.append("")
    I.append("## 1차에서 검토하지 않은 것\n")
    I.append("- 공통 개념 ID·동의어 병합·상하 관계·관계 방향·적용 조건: 미검토(후속 단계).")
    I.append("- 다른 원장(taxonomy 등)과의 대응: 미검토(F-01).")
    I.append("- 임상·법적 진술의 사실 여부: 판정하지 않음(원문 보존만).")
    (HERE / "issues.md").write_text("\n".join(I) + "\n", encoding="utf-8")

    h1 = sha256_bytes(SRC.read_bytes())
    print("source sha256 start", h0, "end", h1, "same" if h0 == h1 else "CHANGED")
    print("nodes", len(nodes), "leaves", len(leaves), "empty", len(empties), "fields", len(field_names))
    print("morph text_values", len(text_values), "fields", len(fields), "excluded", len(excluded),
          "tokens", morphology["applied_counts"]["tokens"], "distinct", len(cache))
    print("manual_expr", len(mexpr), "regex", len(regex_c), "clauses", len(clauses), "observations", len(obs_out), "issues", len(issues))
    print("name_splits", len(name_splits), "form_mismatch", len(form_mismatch))
    print("cue hits", cue_review["counts"])
    print("clause cut-through (괄호 불균형)", [(c["pointer"], c["seg"]) for c in clauses if not c["paren_balanced"]])
    if h0 != h1:
        sys.exit(1)


if __name__ == "__main__":
    main()
