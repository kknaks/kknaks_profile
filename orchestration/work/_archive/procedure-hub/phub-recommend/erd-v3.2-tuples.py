#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3.2 — 분해·실측기. v3.1(erd-v3.1-tuples.py · 동결) 위에 발주서 erd-v3.2-brief.md 6건 + 코디 추가(V3.2-7 · V3.2-8 · V3.2-9 · V3.2-0) 중 분해·실측에 닿는 것을 바꾼다. 독립 실행.
원장 21 = 브론즈 2판 `bronze/phub-ledger/`(HASHES.txt 검증).

v3.1 → v3.2 (실측에 닿는 것):
  V3.2-0 문구 종류 분류(§0 첫 규칙) — 원장 문구를 먼저 「어느 테이블 것인가」로 가른다: 부작용 문구(safety.*)만 문구 사전·단위 생성 · 타임라인 줄 · 응급 징후 줄 · 고지 · 문헌/환자 설명은 자기 테이블에서 부작용 단위를 참조만(adverse_ref).
  V3.2-1 토큰화 — 조사·용언 어미·문법 낱말을 조각에서 떼어 grammar_tokens[] 로 보존(버림 0) · 사전 통째 일치가 먼저(V3-6) · 어간은 사전 값·수식어이거나 원장 독립 토큰(2자 이상)일 때만.
  V3.2-2 표기 변형 — (a) 병기 괄호(한글 ↔ 라틴 · 사전에 안 닿는 라틴 쪽은 gloss) (b) 자모 변형 쌍(편집거리 1 · 같은 자리 · 목록만 · 적용 0) (c) 조사 제거 뒤 재일치(V3.2-1).
  V3.2-3/4/5/6 사전 씨앗 후보 — 원장 전체 어휘(미등록 조각 · 칸(key path) → 종류) · 빈도 ≥2 또는 locator ≥2 · proposed(적용 0) · 부위 닫힌 목록 · 장비 항목 · 줄임말 접두 · 성분.
  V3.2-6 성분 what — 시술 분해 사전에 ingredient_material(성분) — 다른 primary 가 없으면 what=성분, 있으면 ingredient_fragments(보존).
  V3.2-7 부작용 문구 종류 판정 — not_adverse_note(사건 0 + 메모 어휘) · explanatory_sentence(문장) 은 unlinked 로 세지 않는다.
  V3.2-8 R15 속성 상속(item → family → unit · basis · 참조만).
  V3.2-9 post_procedure_timeline(타임라인 10 · 단계 · 줄 435) · R33 has_timeline · R34 timeline_refers · (V3.2-0) emergency_sign 줄 · R35 sign_refers.

실측은 세 번 돈다: ① v3.1(erd-v3.1-tuples.py 그대로) ② v3.2 규칙(씨앗 미적용) ③ 참고 — 씨앗 후보 전부 승인 가정(적용 아님 · 장비 승격 수 등).
입력(같은 폴더): erd-v3.2-dictionaries.json(없으면 erd-v3.1-dictionaries.json) · erd-v3.2.json(없으면 erd_spec_v32) · erd-v3.1-tuples.py · bronze/phub-ledger/ · erd-v3.1-tuples.json
출력: 표준 출력에 §9 표 + erd-v3.2-tuples.json · erd-v3.2-seed-candidates.json/.md(main 실행 때)
실행: python3 erd-v3.2-tuples.py
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "bronze", "phub-ledger")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V31 = load_module("erd_v31_tuples", os.path.join(HERE, "erd-v3.1-tuples.py"))
V3 = V31.V3
V24, V23, V22, V2, V11 = V3.V24, V3.V23, V3.V22, V3.V2, V3.V11
norm, mkid, md_table, with_alias = V3.norm, V3.mkid, V3.md_table, V3.with_alias
locator = V3.locator
_dedupe = V3._dedupe
bronze_check = V3.bronze_check
PRIMARY_KINDS = V3.PRIMARY_KINDS
_AU31 = V31.AdverseUnits31

HANGUL = re.compile(r"[가-힣]")
LATIN = re.compile(r"[A-Za-z]")
DIGIT = re.compile(r"\d")
TOK_SPLIT = re.compile(r"[()\[\]·/,+:;—]")
TOK_STRIP = "*'\"“”‘’.…`~!?"

# 실행 중 규칙(run_all32 가 채운다) — 분해 클래스가 읽는다
CUR = {"tok": None, "flags": None, "ingredient": {}, "vocab": Counter()}
FLAGS_V32 = {"tokenize": True, "gloss": True, "ingredient_what": True, "phrase_kinds": True}
FLAGS_OFF = {"tokenize": False, "gloss": False, "ingredient_what": False, "phrase_kinds": False}


def script_of(s):
    h, l = bool(HANGUL.search(s)), bool(LATIN.search(s))
    if DIGIT.search(s):
        return "N"
    if h and not l:
        return "H"
    if l and not h:
        return "L"
    return "M" if h and l else "N"


def raw_tokens(text):
    t = TOK_SPLIT.sub(" ", str(text))
    return [x.strip(TOK_STRIP) for x in t.split() if x.strip(TOK_STRIP)]


# ---------------------------------------------------------------------------
# 원장 전체 어휘 — 분해하는 문자열 자리 전부(부작용 문구 · 이름 · 조건 · 시술 라벨) · locator
# ---------------------------------------------------------------------------
def _split_code(s):
    m = re.match(r"^(M\d+)(?:[-_ ](.+))?$", s)
    return (m.group(1), m.group(2)) if m else (None, s)


def procedure_label_sites(L):
    """시술 라벨 자리 전부(분류 항목 이름 + §9.2 자유 텍스트 자리) — (slot, file, path, locator, label, hint)."""
    out = []
    tx = L["taxonomy.json"]
    for mi, m in enumerate(tx["modality"]):
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                out.append(("① taxonomy 항목", "taxonomy.json", "modality[].subcategories[].items[].name", locator("taxonomy.json", "modality[].subcategories[].items[].name", f"{m['id']}/{si}/{ii}"), it["name"], m["id"]))
    for i, l in enumerate(L["synergy.json"]["links"]):
        for k in ("from", "to"):
            code, lab = _split_code(l[k])
            out.append(("synergy.links[].from/to (노드 52)", "synergy.json", f"links[].{k}", locator("synergy.json", f"links[].{k}", str(i)), lab, code))
    pp = L["problem-packages.json"]
    for pi, p in enumerate(pp["problems"]):
        for ci, c in enumerate(p["complaints"]):
            for ri, pr in enumerate(c["procedures"]):
                out.append(("problem-packages.procedures[].name (시술 종류 29)", "problem-packages.json", "problems[].complaints[].procedures[].name", locator("problem-packages.json", "problems[].complaints[].procedures[].name", f"{pi}/{ci}/{ri}"), pr["name"], pr["category"]))
                for xi, x in enumerate(pr["products"]):
                    out.append(("problem-packages.procedures[].products[] (제품 34)", "problem-packages.json", "problems[].complaints[].procedures[].products[]", locator("problem-packages.json", "problems[].complaints[].procedures[].products[]", f"{pi}/{ci}/{ri}/{xi}"), x, None))
            for bi, cb in enumerate(c["combos"]):
                for xi, x in enumerate(cb["combo"]):
                    out.append(("problem-packages.combos[].combo[] (멤버 29)", "problem-packages.json", "problems[].complaints[].combos[].combo[]", locator("problem-packages.json", "problems[].complaints[].combos[].combo[]", f"{pi}/{ci}/{bi}/{xi}"), x, None))
    pc = L["procedure-comparison.json"]
    for ci, c in enumerate(pc["comparisons"]):
        for ri, pr in enumerate(c["procedures"]):
            out.append(("procedure-comparison.procedures[].name (39)", "procedure-comparison.json", "comparisons[].procedures[].name", locator("procedure-comparison.json", "comparisons[].procedures[].name", f"{ci}/{ri}"), pr["name"], pr["category"]))
    to = L["treatment-optimization.json"]
    for ci, c in enumerate(to["by_concern"]):
        for si, s in enumerate(c["severity_levels"]):
            for xi, x in enumerate(s["optimal_combo"]):
                out.append(("treatment-optimization.optimal_combo[] (57)", "treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]", locator("treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]", f"{ci}/{si}/{xi}"), x, None))
    for gi, g in enumerate(to["by_age_group"]):
        for k in ("recommended_base", "avoid", "upgrade"):
            for xi, x in enumerate(g.get(k, [])):
                out.append(("treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", "treatment-optimization.json", f"by_age_group[].{k}[]", locator("treatment-optimization.json", f"by_age_group[].{k}[]", f"{gi}/{xi}"), x, None))
    for pi, pl in enumerate(to["annual_plans"]):
        for si, s in enumerate(pl["schedule"]):
            for xi, x in enumerate(s["procedures"]):
                out.append(("treatment-optimization.annual_plans.schedule[].procedures[] (29)", "treatment-optimization.json", "annual_plans[].schedule[].procedures[]", locator("treatment-optimization.json", "annual_plans[].schedule[].procedures[]", f"{pi}/{si}/{xi}"), x, None))
    ts = L["treatment-sequence.json"]
    for si, s in enumerate(ts["sequence_order"]):
        for ci, c in enumerate(s["categories"]):
            code, lab = _split_code(c)
            out.append(("treatment-sequence.sequence_order[].categories[] (19)", "treatment-sequence.json", "sequence_order[].categories[]", locator("treatment-sequence.json", "sequence_order[].categories[]", f"{si}/{ci}"), lab if lab else c, code))
    for i, p in enumerate(ts["incompatible_same_day"]):
        for j, x in enumerate(p["pair"]):
            out.append(("treatment-sequence.incompatible_same_day[].pair[] (14 distinct)", "treatment-sequence.json", "incompatible_same_day[].pair[]", locator("treatment-sequence.json", "incompatible_same_day[].pair[]", f"{i}/{j}"), x, None))
    for i, m in enumerate(ts["minimum_intervals"]):
        for k in ("from", "to"):
            out.append(("treatment-sequence.minimum_intervals from/to (14 distinct)", "treatment-sequence.json", f"minimum_intervals[].{k}", locator("treatment-sequence.json", f"minimum_intervals[].{k}", str(i)), m[k], None))
    for i, c in enumerate(ts["common_combos"]):
        for j, x in enumerate(c["sequence"]):
            out.append(("treatment-sequence.common_combos[].sequence[] (22 distinct)", "treatment-sequence.json", "common_combos[].sequence[]", locator("treatment-sequence.json", "common_combos[].sequence[]", f"{i}/{j}"), x, None))
    for i, t in enumerate(L["post-procedure-timeline.json"]["timelines"]):
        out.append(("post-procedure-timeline.timelines[].name (10)", "post-procedure-timeline.json", "timelines[].name", locator("post-procedure-timeline.json", "timelines[].name", str(i)), t["name"], _split_code(t["category"])[0]))
    mp = L["market-pricing.json"]
    for ci, c in enumerate(mp["categories"]):
        for ii, it in enumerate(c["items"]):
            out.append(("market-pricing.items[].name (122)", "market-pricing.json", "categories[].items[].name", locator("market-pricing.json", "categories[].items[].name", f"{c['id']}/{ii}"), it["name"], c["id"]))
    return out


def ledger_texts(L):
    """원장 전수 — 분해하는 문자열 자리 전부: (axis, kind, file, path, locator, text, modality)."""
    out = []
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            out.append(("adverse", "complication_name", "complications.json", "categories[].complications[].name", locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}"), c["name"], cat["id"]))
    for kind, text, src in V31.adverse_phrases31(L):
        out.append(("adverse", kind, src["file"], src["path"], src["locator"], text, src.get("modality")))
    for f, p, rec, x, code, lvl in V31.condition_occurrences(L):
        out.append(("condition", "condition_name", f, p, locator(f, p, rec), x, code))
    for slot, f, p, loc, lab, hint in procedure_label_sites(L):
        if lab is None:
            continue
        out.append(("procedure", slot, f, p, loc, lab, hint))
    return out


def build_vocab(texts):
    v = Counter()
    locs = defaultdict(list)
    for ax, kind, f, p, loc, text, mod in texts:
        for t in raw_tokens(text):
            k = norm(t)
            v[k] += 1
            if len(locs[k]) < 12 and loc not in locs[k]:
                locs[k].append(loc)
    return v, locs


# ---------------------------------------------------------------------------
# V3.2-1 토큰화기
# ---------------------------------------------------------------------------
class Tokenizer:
    def __init__(self, tok_rules, vocab):
        self.particles = sorted({norm(p) for p in tok_rules["particles"]}, key=lambda x: -len(x))
        self.endings = sorted({norm(p) for p in tok_rules["verb_endings"]}, key=lambda x: -len(x))
        self.grammar = {norm(w): w for w in tok_rules["grammar_words"]}
        self.min_len = tok_rules.get("stem_min_len", 2)
        self.relaxed = sorted({norm(p) for p in tok_rules.get("relaxed_suffixes", [])}, key=lambda x: -len(x))
        self.vocab = vocab
        self.hits = Counter()          # 접미·낱말 → 횟수
        self.hit_locs = defaultdict(list)
        self.log = []                  # (axis, 원 토큰, 결과 종류, 어간/값, 접미)
        self.seen = set()

    def note(self, key, loc):
        if not loc or (key, loc) in self.seen:
            return
        self.seen.add((key, loc))
        self.hits[key] += 1
        if len(self.hit_locs[key]) < 12:
            self.hit_locs[key].append(loc)

    def is_grammar(self, tok):
        return norm(tok) in self.grammar

    def attested(self, stem):
        n = norm(stem)
        return len(n) >= self.min_len and self.vocab.get(n, 0) > 0

    def strip(self, tok, known):
        """tok = 어간 + 조사|용언 어미 · 어간이 known(사전·수식어·문법) 또는 원장 독립 토큰(2자 이상)일 때만 → (어간 원문, 접미, 접미 종류). 없으면 None. 가장 긴 접미부터."""
        nt = norm(tok)
        cands = [(e, "particle") for e in self.particles] + [(e, "ending") for e in self.endings]
        cands.sort(key=lambda x: -len(x[0]))
        for suf, kind in cands:
            if len(nt) > len(suf) and nt.endswith(suf):
                stem_n = nt[: -len(suf)]
                # 원문 어간(대소문자 보존) — 끝에서 접미 길이만큼 자른다(정규화가 길이를 바꾸지 않는 경우만)
                stem = tok[: len(tok) - len(suf)] if norm(tok[: len(tok) - len(suf)]) == stem_n else stem_n
                if known(stem) or self.is_grammar(stem) or self.attested(stem):
                    return stem, tok[len(stem):], kind
        # 검토 S-4: 어간이 원장 독립 토큰이 아니어도 한글 2자 이상이면 떼는 접미(조사 일부 · 「~시」) — grammar 로 보존
        for suf in self.relaxed:
            if len(nt) > len(suf) and nt.endswith(suf):
                stem_n = nt[: -len(suf)]
                if len(stem_n) >= 2 and re.fullmatch(r"[가-힣]+", stem_n):
                    stem = tok[: len(tok) - len(suf)] if norm(tok[: len(tok) - len(suf)]) == stem_n else stem_n
                    return stem, tok[len(stem):], "particle"
        return None


# ---------------------------------------------------------------------------
# V3.2-2(a) 병기 괄호 — 괄호 앞 마지막 토큰 ↔ 괄호 안(멤버 하나 · 숫자 없음 · 한글만 ↔ 라틴만)
# ---------------------------------------------------------------------------
def gloss_pairs(text, paren_re):
    """[(k, 앞 토큰, 괄호 안)] — k = 괄호 순번(분해의 inner 묶음 순서와 같다)."""
    out = []
    for k, m in enumerate(paren_re.finditer(str(text))):
        inner = m.group(1).strip()
        before = str(text)[: m.start()].rstrip()
        if not before or not inner:
            continue
        prev = re.split(r"[\s·/,+]", before)[-1].strip(TOK_STRIP)
        if not prev or re.search(r"[·/,+;:]|\s및\s|\s또는\s", inner):
            continue
        a, b = script_of(prev), script_of(inner)
        if {a, b} == {"H", "L"}:
            out.append((k, prev, inner))
    return out


def _apply_gloss(groups, text, paren_re, loc, sink, axis):
    """groups(outer + inner 순) 위에 병기 규칙: 사전에 닿지 않은 라틴 쪽을 gloss 로 옮긴다(보존). 쌍은 sink 에 전부(후보 목록)."""
    pairs = gloss_pairs(text, paren_re)
    if not pairs:
        return groups
    outer = groups[0]
    inners = groups[1:]
    for k, prev, inner in pairs:
        rec = {"axis": axis, "locator": loc, "text": text, "before": prev, "inner": inner}
        if loc and rec not in sink:
            sink.append(rec)
        if k >= len(inners):
            continue
        ig = inners[k]
        if len(ig["members"]) != 1:
            continue
        im = ig["members"][0]
        un_in = [u if isinstance(u, str) else u["text"] for u in im["untouched"]]
        # (i) 앞 토큰이 사전에 닿았고(바깥 미등록에 없음) 괄호 안이 전부 미등록·라틴만 → 괄호 안 = gloss
        out_un = [u if isinstance(u, str) else u["text"] for m in outer["members"] for u in m["untouched"]]
        if script_of(inner) == "L" and not im["spans"] and un_in and norm(prev) not in {norm(x) for x in out_un}:
            im.setdefault("gloss", []).extend(un_in)
            im["untouched"] = []
            continue
        # (ii) 앞 토큰이 미등록 라틴 · 괄호 안이 전부 사전에 닿음(한글) → 앞 토큰 = gloss
        if script_of(prev) == "L" and im["spans"] and not im["untouched"]:
            for m in outer["members"]:
                for u in list(m["untouched"]):
                    ut = u if isinstance(u, str) else u["text"]
                    if norm(ut) == norm(prev):
                        m["untouched"].remove(u)
                        m.setdefault("gloss", []).append(ut)
                        break
                else:
                    continue
                break
    return groups


# ---------------------------------------------------------------------------
# 부작용 축 — AdverseUnits31 + 토큰화 · 병기
# ---------------------------------------------------------------------------
class AdverseUnits32(V31.AdverseUnits31):
    def __init__(self, ids, rules):
        super().__init__(ids, rules)
        self.gloss_sink = []
        self.mode = None          # None | create | refer (V3.2-0)
        self.ctx = None
        self.ledger = OrderedDict()
        self.base_event_surface = dict(ids.event_surface)
        self.fallback = {norm(w) for w in (CUR.get("fallback_core") or [])}

    def _known(self, s):
        n = norm(s)
        return n in self.lookup or n in self.stop or any(rx.match(unicodedata.normalize("NFKC", s)) for _, rx, _ in self.patterns)

    def _span_at(self, toks, i):
        for j in range(min(len(toks), i + self.maxlen), i, -1):
            key = norm("".join(toks[i:j]))
            if key in self.lookup:
                return (self.lookup[key], " ".join(toks[i:j]), j, None)
        return None

    def _span_at_stripped(self, toks, i, tk):
        for j in range(min(len(toks), i + self.maxlen), i, -1):
            st = tk.strip(toks[j - 1], self._known)
            if not st:
                continue
            key = norm("".join(toks[i:j - 1] + [st[0]]))
            if key in self.lookup:
                return (self.lookup[key], " ".join(toks[i:j - 1] + [st[0]]), j, st)
        return None

    def split(self, text, loc=None):
        flags = CUR["flags"] or FLAGS_OFF
        self._loc = loc
        groups = self._split_base(text, loc)
        if flags["phrase_kinds"]:
            groups = self._explanations(groups)
            if self.mode:
                groups = self._apply_cores(groups, text, loc)
        return groups

    @staticmethod
    def _has_event(g):
        return any(s["kind"] == "event" for m in g["members"] for s in m["spans"])

    def _explanations(self, groups):
        """V3.2-0/7: 사건 조각이 없는 괄호 안 묶음의 미등록 토큰은 설명(explanation · 보존)이지 조각이 아니다.
        V3.2-1(검토 S-4): 용언 꼴(관형형·연결형 어미로 끝나는 미등록 토큰)은 predicate(보존) — 핵심어에는 다른 조각이 없을 때만."""
        pe = sorted({norm(x) for x in (CUR["kinds"].get("predicate_endings") or [])}, key=lambda x: -len(x))
        tk = CUR.get("tok")
        for g in groups:
            for m in g["members"]:
                keep = []
                for u in m["untouched"]:
                    nu = norm(u)
                    hit = next((e for e in pe if len(nu) > len(e) and nu.endswith(e) and HANGUL.search(nu)), None)
                    if hit:
                        m.setdefault("predicate", []).append(u)
                        if tk:
                            tk.note(f"predicate:{hit}", self._loc)
                    else:
                        keep.append(u)
                m["untouched"] = keep
        for g in groups[1:]:
            if not self._has_event(g):
                for m in g["members"]:
                    if m["untouched"]:
                        m.setdefault("explanation", []).extend(m["untouched"])
                        m["untouched"] = []
        return groups

    def _pieces(self, m, text):
        """멤버의 조각을 원문 순서로 — (위치, 종류, 글자): ev(사전·노드 사건) · u(미등록) · fb(대체 핵심어 수식어) · pr(용언 꼴 · predicate) · 접속 조사(와·과·이나 …)가 붙은 토큰 끝은 경계(bd)."""
        txt = m["text"]
        out, pos = [], 0
        for s_ in m["spans"]:
            if s_["kind"] == "event":
                i = txt.find(s_["text"].split()[0]) if s_["text"] else -1
                out.append((i if i >= 0 else 10 ** 6, "ev", s_))
        for u in m["untouched"]:
            i = txt.find(u, pos)
            out.append((i if i >= 0 else 10 ** 6, "u", u))
            if i >= 0:
                pos = i + len(u)
        for md in m.get("modifiers", []):
            if norm(md["text"]) in self.fallback:
                out.append((txt.find(md["text"]), "fb", md["text"]))
        for x in m.get("predicate", []):
            out.append((txt.find(x), "pr", x))
        conj = {norm(c) for c in (CUR["kinds"].get("conj_particles") or [])}
        for g_ in m.get("grammar", []):
            if g_["kind"] == "particle" and norm(g_["text"]) in conj:
                i = txt.find(g_["of"])
                if i >= 0:
                    out.append((i + len(g_["of"]) - 0.5, "bd", g_["text"]))
        out.sort(key=lambda x: x[0])
        return out

    def _segments(self, m, text):
        segs, cur = [], []
        for x in self._pieces(m, text):
            if x[1] == "bd":
                segs.append(cur)
                cur = []
            else:
                cur.append(x)
        segs.append(cur)
        return [sg for sg in segs if sg]

    def _register_core(self, core, m, text, loc):
        key = norm(core)
        if key in self.base_event_surface:
            return self.base_event_surface[key], "dictionary"
        if key in self.ledger:
            canon, origin = self.ledger[key]["canonical"], "ledger"
        elif self.mode == "create":
            canon, origin = core, "ledger"
            eid = mkid("DIC", f"adverse_event_type|{core}")
            self.ledger[key] = {"canonical": core, "id": eid, "locators": [], "contexts": [], "core_tokens": core.split()}
            self.ids.event[key] = {"id": eid, "label": core, "category": None}
        else:
            return None, None
        if self.mode == "create" and loc and loc not in self.ledger[key]["locators"]:
            self.ledger[key]["locators"].append(loc)
            self.ledger[key]["contexts"].append(dict(self.ctx or {}, locator=loc, text=text))
        return canon, origin

    def _apply_cores(self, groups, text, loc):
        """V3.2-0 노드 원칙(검토 S-1 반영 · 시술 축과 대칭): 멤버를 접속 조사(와·과·이나 …)로 토막 내고, 토막마다
        사전 사건이 닿으면 그 사건에 exact 로 붙이고 옆의 미등록 토큰은 side(보존 · 노드 후보 목록) · 사전 사건이 0 인 토막만
        핵심어(미등록 토큰 + 대체 핵심어 · 비면 용언 꼴)를 새 사건 노드로 — mode=create 면 세우고 refer 면 이미 있는 것만."""
        has_h = bool(HANGUL.search(str(text)))
        excl = {norm(w) for w in (CUR["kinds"].get("core_exclude") or [])}
        for gi, g in enumerate(groups):
            if gi > 0 and not self._has_event(g):
                continue
            for m in g["members"]:
                moved = [u for u in m["untouched"] if (has_h and script_of(u) == "L") or norm(u) in excl or not (HANGUL.search(u) or LATIN.search(u))]
                if moved:
                    m.setdefault("explanation", []).extend(moved)
                    m["untouched"] = [u for u in m["untouched"] if u not in moved]
                if not m["untouched"] and (any(s_["kind"] == "event" for s_ in m["spans"]) or gi > 0):
                    continue
                if not m["untouched"] and not any(p[1] in ("fb", "pr") for p in self._pieces(m, text)):
                    continue
                new_spans, side, cores, left = [], [], [], []
                for sg in self._segments(m, text):
                    evs = [x for x in sg if x[1] == "ev"]
                    us = [x[2] for x in sg if x[1] == "u"]
                    if evs:
                        side += us
                        continue
                    toks = [x[2] for x in sg if x[1] in ("u", "fb")] or ([x[2] for x in sg if x[1] == "pr"] if gi == 0 else [])
                    if not toks or (not us and gi > 0):
                        continue
                    core = " ".join(toks)
                    canon, origin = self._register_core(core, m, text, loc)
                    if canon is None:
                        left += us
                        continue
                    cores.append(core)
                    new_spans.append({"kind": "event", "canonical": canon, "text": core, "basis": "ledger_core" if origin == "ledger" else "core_exact"})
                if side:
                    m["side"] = list(side)
                if cores:
                    m["core_tokens"] = cores
                m["spans"] = list(m["spans"]) + new_spans
                m["untouched"] = left + ([] if self.mode == "create" else [])
                if self.mode == "refer" and side:
                    m["untouched"] = left + side
        return groups

    def _split_base(self, text, loc=None):
        flags = CUR["flags"] or FLAGS_OFF
        tk = CUR["tok"] if flags["tokenize"] else None
        if not flags["tokenize"] and not flags["gloss"]:
            return super().split(text, loc)
        parens = V2.ADV_PAREN.findall(text)
        outer = V2.ADV_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in V2.ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part:
                    continue
                toks = [t.strip(V2.ADV_STRIP) for t in part.split()]
                toks = [t for t in toks if t]
                spans, untouched, mods, gram = [], [], [], []
                i = 0
                while i < len(toks):
                    found = self._span_at(toks, i)
                    if not found and tk:
                        found = self._span_at_stripped(toks, i, tk)
                    if found:
                        spans.append({"kind": found[0][0], "canonical": found[0][1], "text": found[1]})
                        if found[3]:
                            gram.append({"text": found[3][1], "kind": found[3][2], "of": toks[found[2] - 1]})
                            tk.note(f"{found[3][2]}:{norm(found[3][1])}", loc)
                            tk.log.append(("adverse", toks[found[2] - 1], "span", found[1], found[3][1]))
                        i = found[2]
                        continue
                    tok = toks[i]
                    nt = norm(tok)
                    hit = None
                    for k in range(1, len(nt)):
                        if nt[:k] in self.ids.qualifier_surface and nt[k:] in self.ids.event_surface:
                            hit = (nt[:k], nt[k:])
                            break
                    if hit:
                        spans.append({"kind": "qualifier", "canonical": self.ids.qualifier_surface[hit[0]], "text": tok, "basis": "prefix_split"})
                        spans.append({"kind": "event", "canonical": self.ids.event_surface[hit[1]], "text": tok})
                        self.prefix_splits.append((tok, self.ids.qualifier_surface[hit[0]], self.ids.event_surface[hit[1]]))
                        i += 1
                        continue
                    cls, how, key_ = self._classify_token(tok)
                    if cls:
                        mods.append({"text": tok, "class": cls, "by": how, "key": key_})
                        tgt_hits, tgt_locs = (self.stop_hits, self.stop_locs) if how == "word" else (self.pat_hits, self.pat_locs)
                        tgt_hits[key_] += 1
                        if loc and len(tgt_locs[key_]) < 12 and loc not in tgt_locs[key_]:
                            tgt_locs[key_].append(loc)
                        i += 1
                        continue
                    if tk and tk.is_grammar(tok):
                        gram.append({"text": tok, "kind": "word", "of": tok})
                        tk.note(f"word:{nt}", loc)
                        tk.log.append(("adverse", tok, "grammar", tok, ""))
                        i += 1
                        continue
                    st = tk.strip(tok, self._known) if tk else None
                    if st:
                        stem, suf, sk = st
                        gram.append({"text": suf, "kind": sk, "of": tok})
                        tk.note(f"{sk}:{norm(suf)}", loc)
                        ns = norm(stem)
                        if ns in self.lookup:
                            spans.append({"kind": self.lookup[ns][0], "canonical": self.lookup[ns][1], "text": stem})
                            tk.log.append(("adverse", tok, "span", stem, suf))
                        else:
                            c2, how2, key2 = self._classify_token(stem)
                            if c2:
                                mods.append({"text": stem, "class": c2, "by": how2, "key": key2})
                                tk.log.append(("adverse", tok, "modifier", stem, suf))
                            elif tk.is_grammar(stem):
                                gram.append({"text": stem, "kind": "word", "of": tok})
                                tk.log.append(("adverse", tok, "grammar", stem, suf))
                            else:
                                untouched.append(stem)
                                tk.log.append(("adverse", tok, "stem", stem, suf))
                        i += 1
                        continue
                    untouched.append(tok)
                    i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched, "modifiers": mods, "where": where, "grammar": gram})
            groups.append({"where": where, "members": members})
        if flags["gloss"]:
            groups = _apply_gloss(groups, text, V2.ADV_PAREN, loc, self.gloss_sink, "adverse")
        return groups

    @staticmethod
    def _classes(groups):
        out = _AU31._classes(groups)
        for g in groups:
            for m in g["members"]:
                for x in m.get("grammar", []):
                    out.append({"token": x["text"], "class": "grammar"})
                for x in m.get("gloss", []):
                    out.append({"token": x, "class": "gloss"})
                for x in m.get("explanation", []):
                    out.append({"token": x, "class": "explanation"})
                for x in m.get("side", []):
                    out.append({"token": x, "class": "side"})
                for x in m.get("predicate", []):
                    out.append({"token": x, "class": "predicate"})
        return out

    def _parsed(self, groups):
        p = super()._parsed(groups)
        p["grammar"] = [x["text"] for g in groups for m in g["members"] for x in m.get("grammar", [])]
        p["gloss"] = [x for g in groups for m in g["members"] for x in m.get("gloss", [])]
        p["explanation"] = _dedupe(p.get("explanation", []) + [x for g in groups for m in g["members"] for x in m.get("explanation", [])])
        p["core_tokens"] = [x for g in groups for m in g["members"] for x in m.get("core_tokens", [])]
        p["side"] = [x for g in groups for m in g["members"] for x in m.get("side", [])]
        p["predicate"] = [x for g in groups for m in g["members"] for x in m.get("predicate", [])]
        return p


# ---------------------------------------------------------------------------
# 시술 축 — V3Resolver + 토큰화 · 병기 · 성분(V3.2-6)
# ---------------------------------------------------------------------------
INGREDIENT_DICT = "ingredient_material"


class V32Resolver(V3.V3Resolver):
    def classify3(self, frag, family, where):
        c = super().classify3(frag, family, where)
        flags = CUR["flags"] or FLAGS_OFF
        if c is None and flags["ingredient_what"]:
            t = norm(frag)
            if t in CUR["ingredient"]:
                e = CUR["ingredient"][t]
                return {"kind": "ingredient", "text": frag.strip(), "canonical": e["canonical"], "dict_id": e["id"]}
        return c

    def _known(self, s, family, where):
        c = self.classify3(s, family, where)
        return (c is not None and c["kind"] != "ambiguous") or self.is_stop(s)

    def decompose(self, label, family, exclude=None):
        flags = CUR["flags"] or FLAGS_OFF
        if not flags["tokenize"] and not flags["gloss"] and not flags["ingredient_what"]:
            return super().decompose(label, family, exclude)
        tk = CUR["tok"] if flags["tokenize"] else None
        self.exclude = exclude
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members, sep = [], None
            for piece in V3.SEP_RE.split(g):
                if piece in ("+", "/", "&", ","):
                    sep = piece
                    continue
                part = piece.strip(" ·")
                if not part:
                    continue
                spans, untouched, stops, gram = [], [], [], []
                c = self.classify3(part, family, where)
                if c and c["kind"] != "ambiguous":
                    spans.append(c)
                else:
                    toks = part.split()
                    i = 0
                    while i < len(toks):
                        found = None
                        for j in range(len(toks), i, -1):
                            h = self.classify3(" ".join(toks[i:j]), family, where)
                            if h and h["kind"] != "ambiguous":
                                found = (h, j, None)
                                break
                        if not found and tk:
                            for j in range(len(toks), i, -1):
                                st = tk.strip(toks[j - 1], lambda s: self._known(s, family, where))
                                if not st:
                                    continue
                                h = self.classify3(" ".join(toks[i:j - 1] + [st[0]]), family, where)
                                if h and h["kind"] != "ambiguous":
                                    found = (h, j, st)
                                    break
                        if found:
                            spans.append(found[0])
                            if found[2]:
                                gram.append({"text": found[2][1], "kind": found[2][2], "of": toks[found[1] - 1]})
                                tk.note(f"{found[2][2]}:{norm(found[2][1])}", "label:" + str(label))
                                tk.log.append(("procedure", toks[found[1] - 1], "span", found[2][0], found[2][1]))
                            i = found[1]
                            continue
                        tok = toks[i]
                        if self.is_stop(tok):
                            stops.append(tok)
                        elif tk and tk.is_grammar(tok):
                            gram.append({"text": tok, "kind": "word", "of": tok})
                            tk.note(f"word:{norm(tok)}", "label:" + str(label))
                            tk.log.append(("procedure", tok, "grammar", tok, ""))
                        else:
                            st = tk.strip(tok, lambda s: self._known(s, family, where)) if tk else None
                            if st:
                                stem, suf, sk = st
                                gram.append({"text": suf, "kind": sk, "of": tok})
                                tk.note(f"{sk}:{norm(suf)}", "label:" + str(label))
                                if self.is_stop(stem):
                                    stops.append(stem)
                                    tk.log.append(("procedure", tok, "modifier", stem, suf))
                                elif tk.is_grammar(stem):
                                    gram.append({"text": stem, "kind": "word", "of": tok})
                                    tk.log.append(("procedure", tok, "grammar", stem, suf))
                                else:
                                    amb = self.classify(stem, family)
                                    untouched.append({"text": stem, "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                                    tk.log.append(("procedure", tok, "stem", stem, suf))
                            else:
                                amb = self.classify(tok, family)
                                untouched.append({"text": tok, "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                        i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched, "stopwords": stops, "sep": sep, "grammar": gram})
                sep = None
            groups.append({"where": where, "members": members})
        self.exclude = None
        if flags["gloss"]:
            groups = _apply_gloss(groups, label, self.paren_re, "label:" + str(label), CUR["gloss_sink"], "procedure")
        return groups


class ProcedureTuples32(V31.ProcedureTuples31):
    """v3.1 위에 V3.2-1/2(분해기 V32Resolver) · V3.2-6(성분 what)."""

    def __init__(self, lex, rules, ids, L):
        super().__init__(lex, rules, ids, L)
        self.R = V32Resolver(lex, rules, ids)
        self.ingredient_what = []

    def _annotate(self, groups, base):
        base = super()._annotate(groups, base)
        mems = [m for g in groups for m in g["members"]]
        base["grammar_tokens"] = [x["text"] for m in mems for x in m.get("grammar", [])]
        base["gloss"] = [x for m in mems for x in m.get("gloss", [])]
        base["ingredient_fragments"] = [s["canonical"] for m in mems for s in m.get("ingredients", [])]
        return base

    def assemble22(self, groups, family, for_item, anchor, label_text=None):
        flags = CUR["flags"] or FLAGS_OFF
        ings = [s for g in groups for m in g["members"] for s in m["spans"] if s["kind"] == "ingredient"]
        if not ings or not flags["ingredient_what"]:
            return super().assemble22(groups, family, for_item, anchor, label_text)
        # 성분 조각은 primary 판단에서 빼고(멤버 ingredients 에 보존) 나머지로 조립 → primary 가 없으면 what = 성분
        g2 = []
        for g in groups:
            ms = []
            for m in g["members"]:
                m2 = dict(m, spans=[s for s in m["spans"] if s["kind"] != "ingredient"], ingredients=[s for s in m["spans"] if s["kind"] == "ingredient"])
                if m2["spans"] or m2["untouched"] or m2.get("stopwords") or m2["ingredients"] or m2.get("grammar") or m2.get("gloss"):
                    ms.append(m2)
            g2.append(dict(g, members=ms))
        a = super().assemble22(g2, family, for_item, anchor, label_text)
        if a.get("untouched"):
            return a
        if a["kind"] == "hint_only" or (a["kind"] == "self" and a.get("reason") == "no_primary"):
            distinct = _dedupe(s["canonical"] for s in ings)
            if len(distinct) >= 2:
                return dict(a, kind="ambiguous", reason="multi_primary", status="ambiguous", detail=[f"ingredient:{x}" for x in distinct])
            f = a["fragments"]
            if len(f["sites"]) >= 2:
                return dict(a, kind="ambiguous", reason="multi_site", status="ambiguous", detail=list(f["sites"]))
            if len(f["techniques"]) >= 2:
                return dict(a, kind="ambiguous", reason="multi_technique", status="ambiguous", detail=list(f["techniques"]))
            e = CUR["ingredient"][norm(ings[0]["canonical"])]
            what = {"id": e["id"], "label": e["canonical"], "family": family}
            site = self.ids.site[norm(f["sites"][0])] if f["sites"] else None
            tech = f["techniques"][0] if f["techniques"] else None
            self.ingredient_what.append({"label": label_text, "family": family, "ingredient": e["canonical"], "for_item": for_item})
            a = dict(a, kind="tuple", what_kind="ingredient", what=what, what_basis=f"ingredient:{e['canonical']}", site=site, technique=tech, anchor=anchor, extra_primaries=[], extra_sites=[], via_item=None)
        a["fragments"] = dict(a["fragments"], ingredients=_dedupe(s["canonical"] for s in ings))
        return a


# ---------------------------------------------------------------------------
# 조건 축 — ConditionTuples + 토큰화 · 병기
# ---------------------------------------------------------------------------
class ConditionTuples32(V31.ConditionTuples):
    def split(self, text, loc=None):
        flags = CUR["flags"] or FLAGS_OFF
        if not flags["tokenize"] and not flags["gloss"]:
            return super().split(text, loc)
        tk = CUR["tok"] if flags["tokenize"] else None
        known = lambda s: norm(s) in self.surface or norm(s) in self.markers  # noqa
        parens = V31.COND_PAREN.findall(text)
        outer = V31.COND_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in V31.COND_SPLIT.split(g):
                toks = [t.strip(V31.COND_STRIP) for t in part.split()]
                toks = [t for t in toks if t]
                if not toks:
                    continue
                spans, untouched, marks, gram = [], [], [], []
                i = 0
                while i < len(toks):
                    found = None
                    for j in range(min(len(toks), i + self.maxlen), i, -1):
                        key = norm("".join(toks[i:j]))
                        if key in self.surface:
                            found = (self.surface[key], " ".join(toks[i:j]), j, None)
                            break
                    if not found and tk:
                        for j in range(min(len(toks), i + self.maxlen), i, -1):
                            st = tk.strip(toks[j - 1], known)
                            if not st:
                                continue
                            key = norm("".join(toks[i:j - 1] + [st[0]]))
                            if key in self.surface:
                                found = (self.surface[key], " ".join(toks[i:j - 1] + [st[0]]), j, st)
                                break
                    if found:
                        spans.append({"canonical": found[0], "text": found[1]})
                        if found[3]:
                            gram.append({"text": found[3][1], "kind": found[3][2], "of": toks[found[2] - 1]})
                            tk.note(f"{found[3][2]}:{norm(found[3][1])}", loc)
                            tk.log.append(("condition", toks[found[2] - 1], "span", found[3][0], found[3][1]))
                        i = found[2]
                        continue
                    tok = toks[i]
                    if norm(tok) in self.markers:
                        marks.append(tok)
                        self.marker_hits[self.markers[norm(tok)]] += 1
                        if loc and len(self.marker_locs[self.markers[norm(tok)]]) < 12:
                            self.marker_locs[self.markers[norm(tok)]].append(loc)
                    elif tk and tk.is_grammar(tok):
                        gram.append({"text": tok, "kind": "word", "of": tok})
                        tk.note(f"word:{norm(tok)}", loc)
                        tk.log.append(("condition", tok, "grammar", tok, ""))
                    else:
                        st = tk.strip(tok, known) if tk else None
                        if st:
                            stem, suf, sk = st
                            gram.append({"text": suf, "kind": sk, "of": tok})
                            tk.note(f"{sk}:{norm(suf)}", loc)
                            if norm(stem) in self.surface:
                                spans.append({"canonical": self.surface[norm(stem)], "text": stem})
                                tk.log.append(("condition", tok, "span", stem, suf))
                            elif norm(stem) in self.markers:
                                marks.append(stem)
                                tk.log.append(("condition", tok, "modifier", stem, suf))
                            elif tk.is_grammar(stem):
                                gram.append({"text": stem, "kind": "word", "of": tok})
                                tk.log.append(("condition", tok, "grammar", stem, suf))
                            else:
                                untouched.append(stem)
                                tk.log.append(("condition", tok, "stem", stem, suf))
                        else:
                            untouched.append(tok)
                    i += 1
                members.append({"text": part.strip(), "spans": spans, "untouched": untouched, "markers": marks, "where": where, "grammar": gram})
            groups.append({"where": where, "members": members})
        if flags["gloss"]:
            groups = _apply_gloss(groups, text, V31.COND_PAREN, loc, CUR["gloss_sink"], "condition")
        return groups


# ---------------------------------------------------------------------------
# V3.2-7 부작용 문구 종류 판정(메모 · 설명문) — 바탕 분해(사전 그대로)로 판정한다
# ---------------------------------------------------------------------------
def _outer_tokens(text):
    return raw_tokens(V2.ADV_PAREN.sub(" ", str(text)))


def judge_phrase(text, groups0, kr, tk):
    """exact | note | sentence | new — exact 가 먼저(사건이 있고 미등록 0), 그 다음 메모, 그 다음 설명문, 나머지는 새 노드."""
    has_ev = any(s["kind"] == "event" for g in groups0 for m in g["members"] for s in m["spans"])
    excl = {norm(w) for w in kr.get("core_exclude") or []}
    has_h = bool(HANGUL.search(str(text)))
    unt = [u for g in groups0 for m in g["members"] for u in m["untouched"] if not ((has_h and script_of(u) == "L") or norm(u) in excl or not (HANGUL.search(u) or LATIN.search(u)))]
    if has_ev and not unt:
        return "exact", {}
    toks = _outer_tokens(text)
    note_words = {norm(w) for w in kr["note_words"]}
    hits = []
    for t in toks:
        nt = norm(t)
        if nt in note_words:
            hits.append(t)
            continue
        st = tk.strip(t, lambda s: norm(s) in note_words) if tk else None
        if st and norm(st[0]) in note_words:
            hits.append(t)
    if not has_ev and hits:
        return "note", {"note_words": hits}
    gram = [x for m in groups0[0]["members"] for x in m.get("grammar", [])]
    letters = re.findall(r"[A-Za-z가-힣]", " ".join(toks))
    latin = sum(1 for c in letters if LATIN.match(c)) / max(1, len(letters))
    mtoks = max([len(raw_tokens(m["text"])) for m in groups0[0]["members"]] or [0])
    why = []
    if mtoks >= kr["sentence_min_tokens"]:
        why.append(f"tokens≥{kr['sentence_min_tokens']}")
    if len(gram) >= kr["sentence_min_grammar"]:
        why.append(f"grammar≥{kr['sentence_min_grammar']}")
    if latin >= kr["sentence_latin_ratio"]:
        why.append(f"latin≥{kr['sentence_latin_ratio']}")
    if why:
        return "sentence", {"why": why, "member_tokens": mtoks, "tokens": len(toks), "grammar": len(gram), "latin": round(latin, 2)}
    if not has_ev and not unt:
        fb = {norm(w) for w in kr["fallback_core"]}
        if not any(norm(md["text"]) in fb for m in groups0[0]["members"] for md in m.get("modifiers", [])):
            return "note", {"note_words": [], "why": "사건 0 · 핵심어 0"}
    return "new", {}


def _unused():
    return None


# ---------------------------------------------------------------------------
# ⑦ duplicate_candidate — 원장 사건 노드 ↔ 사전 사건(정준값·동의어) · 표기 규칙만(유사도 점수 없음)
# ---------------------------------------------------------------------------
CHO = 0x1100


def jamo(s):
    out = []
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3:
            o -= 0xAC00
            out += [chr(0x1100 + o // 588), chr(0x1161 + (o % 588) // 28)] + ([chr(0x11A7 + o % 28)] if o % 28 else [])
        else:
            out.append(ch.lower())
    return out


def jamo_sub1(a, b):
    """같은 자리 하나만 다른가(자모 편집거리 1 · 치환만 · 길이 같음)."""
    ja, jb = jamo(a), jamo(b)
    if len(ja) != len(jb) or ja == jb:
        return False
    return sum(1 for x, y in zip(ja, jb) if x != y) == 1


STRONG_SUFFIX = ("감", "증", "형성", "감각")


def dup_rules(a, b, rules, a_words=None, b_words=None):
    """a, b = 정규화형 · a_words/b_words = 공백 낱말(정규화). → [(규칙, 등급)] — strong 만 기본 게이트, weak 는 표시만(검토 S-2)."""
    hit = []
    if a == b:
        return hit
    lo, sh = (a, b) if len(a) >= len(b) else (b, a)
    lw = (a_words if lo == a else b_words) or []
    if any(lo == sh + x for x in STRONG_SUFFIX):
        hit.append(("suffix_" + lo[len(sh):], "strong"))
    elif sh in lw and len(sh) >= 2:
        hit.append(("word_contains", "strong"))
    elif len(sh) >= 2 and sh in lo:
        hit.append(("substring", "weak"))
    if jamo_sub1(a, b):
        hit.append(("jamo1", "strong"))
    pre = os.path.commonprefix([a, b])
    if not hit and len(pre) >= rules["dup_prefix_min"]:
        hit.append((f"prefix{len(pre)}", "weak"))
    if not hit and a[:1] == b[:1] and len(a) <= 2 and len(b) <= 2:
        hit.append(("first_syllable", "weak"))
    return hit


def duplicate_pairs(new_nodes, existing, rules, paren_pairs=()):
    """노드끼리(검토 S-2): 원장 노드 ↔ 사전 사건(정준값·동의어) · 원장 노드 ↔ 원장 노드 · 원장 병기 「X(Y)」 쌍. 문구 ↔ 노드 는 ⑦ 이 아니다.
    → [{new, existing, existing_kind, rules, grade}] · grade = strong(기본 게이트) | weak(표시만)."""
    out = []
    words = {k: [norm(w) for w in rec["canonical"].split()] for k, rec in new_nodes.items()}
    items = list(new_nodes.items())
    pp = {tuple(sorted(x)) for x in paren_pairs}
    for k, rec in items:
        seen = set()
        for s_, canon in existing.items():
            h = dup_rules(k, s_, rules, words[k], [s_])
            if (k, s_) in pp or (s_, k) in pp:
                h = [("paren_pair", "strong")] + h
            if h and canon not in seen:
                seen.add(canon)
                out.append({"new": rec["canonical"], "new_id": rec["id"], "existing": canon, "existing_kind": "dictionary", "surface": s_, "rules": [r for r, g in h], "grade": "strong" if any(g == "strong" for r, g in h) else "weak", "n_locators": len(rec["locators"]),
                            "stable_key": f"duplicate_candidate|adverse_event_type|{rec['canonical']}|{canon}"})
    for i, (k, rec) in enumerate(items):
        for k2, rec2 in items[i + 1:]:
            h = dup_rules(k, k2, rules, words[k], words[k2])
            if tuple(sorted((k, k2))) in pp:
                h = [("paren_pair", "strong")] + h
            if h:
                out.append({"new": rec["canonical"], "new_id": rec["id"], "existing": rec2["canonical"], "existing_kind": "ledger", "surface": k2, "rules": [r for r, g in h], "grade": "strong" if any(g == "strong" for r, g in h) else "weak",
                            "n_locators": len(rec["locators"]) + len(rec2["locators"]), "stable_key": f"duplicate_candidate|adverse_event_type|{rec['canonical']}|{rec2['canonical']}"})
    out.sort(key=lambda x: (x["grade"] != "strong", -x["n_locators"], x["new"], x["existing"]))
    return out


def paren_node_pairs(texts, keys):
    """원장 병기 「X (Y)」 — 괄호 앞 전체와 괄호 안 전체가 둘 다 사건(사전·원장 노드) 정규화형이면 쌍."""
    out = set()
    for ax, kind, f, p, loc, text, mod in texts:
        m = re.fullmatch(r"\s*([^()]+?)\s*\(([^()]+)\)\s*", str(text))
        if m and ax == "adverse":
            a, b = norm(m.group(1)), norm(m.group(2))
            if a in keys and b in keys and a != b:
                out.add((a, b))
    return out


# ---------------------------------------------------------------------------
# 부작용 축 실행 v3.2 — V3.2-0(종류 분류 · 노드 원칙) · V3.2-7 · V3.2-8 · V3.2-9
# ---------------------------------------------------------------------------
INHERIT_ATTRS = ["severity", "incidence", "onset", "duration", "mechanism", "management", "prevention", "risk_factors"]


def _comp_attr_locs(L):
    out = {}
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            d = {}
            for a in INHERIT_ATTRS:
                v = c.get(a)
                if v not in (None, "", [], {}):
                    d[a] = locator("complications.json", f"categories[].complications[].{a}", f"{cat['id']}/{i}")
            out[f"{cat['id']}/{i}"] = d
    return out


def run_adverse32(ids, rules, L, v31tup=None):
    rules = rules["adverse"] if "adverse" in rules else rules
    kr = CUR["kinds"]
    tk = CUR["tok"]
    AT = AdverseUnits32(ids, rules)
    base_surface = dict(ids.event_surface)
    comp_attrs = _comp_attr_locs(L)
    # ---- ① complications 65 이름 → 단위(create · raw_name 없음 — 핵심어 노드)
    comp_rows, name_edges = [], OrderedDict()
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            src = {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc}
            AT.mode, AT.ctx = None, None
            ev0 = AT.evaluate(c["name"], dict(src))
            AT.mode, AT.ctx = "create", {"kind": "complication_name", "modality": cat["id"], "severity": c.get("severity"), "frequency_class": None}
            ev = AT.evaluate(c["name"], dict(src))
            ids_ = []
            for uc in ev["unit_candidates"]:
                ids_.append(AT.register_unit(uc, src))
            if not ids_:
                tid = AT.register_raw(c["name"], [], ev["unregistered"], {"extra_sites": ev["extra_sites"], "extra_courses": ev["extra_courses"], "extra_qualifiers": ev["extra_qualifiers"]}, src, loc)
                ids_ = [tid]
            st = "new" if any(sp[0] == "event" and norm(sp[1]) in AT.ledger for sp in ev["spans"]) else ("exact" if ev["event_fragments"] else "raw")
            comp_rows.append(dict(ev, text=c["name"], locator=loc, modality=cat["id"], record=i, severity=c.get("severity"), unit_ids=_dedupe(ids_), status32=st, base_unregistered=ev0["unregistered"]))
            for uid in _dedupe(ids_):
                k = (("modality", cat["id"]), uid)
                e = name_edges.setdefault(k, {"from": ("modality", cat["id"]), "unit": uid, "courses": [], "names": [], "attrs": {}})
                e["courses"] = _dedupe(e["courses"] + [co for cc in ev["candidates"] if AT.units.get((cc["event_id"], cc["site_id"], cc["qualifier_id"])) == uid for co in cc["courses"]])
                e["names"].append(loc)
                for a, al in comp_attrs[f"{cat['id']}/{i}"].items():
                    e["attrs"].setdefault(a, []).append(al)
    # ---- ② 부작용 문구(safety.*) → 판정(V3.2-7) → exact/new 는 문구 사전 · 단위 · R15
    entries, memo = OrderedDict(), OrderedDict()
    occ = V31.adverse_phrases31(L)
    safety = [(k, t, s) for k, t, s in occ if k == "safety_phrase"]
    phrase_rows = []
    for kind, text, src in safety:
        src = dict(src, kind=kind)
        AT.mode, AT.ctx = None, None
        g0 = AT.split(text, None)
        verdict, why = judge_phrase(text, g0, kr, tk)
        if verdict in ("note", "sentence"):
            ev0 = AT.evaluate(text, src)
            key = ev0["normalized"] or norm(text)
            e = memo.setdefault(key, OrderedDict([("id", mkid("PHR", key)), ("normalized", key), ("status", verdict), ("raw_variants", []), ("locators", []), ("contexts", []), ("why", why), ("parsed", ev0["parsed"]), ("events_seen", ev0["event_fragments"]), ("unregistered", ev0["unregistered"]), ("status_mismatch", 0)]))
            if e["status"] != verdict:
                e["status_mismatch"] += 1
            if text not in e["raw_variants"]:
                e["raw_variants"].append(text)
            e["locators"].append(src["locator"])
            e["contexts"].append({"locator": src["locator"], "from": V31._from_end(src), "modality": src.get("modality"), "frequency_class": (src.get("context") or {}).get("frequency_class")})
            phrase_rows.append({"locator": src["locator"], "text": text, "status": verdict, "phrase_id": e["id"], "from": V31._from_end(src)})
            continue
        ctx = src.get("context") or {}
        AT.mode, AT.ctx = "create", {"kind": "safety_phrase", "modality": src.get("modality"), "frequency_class": ctx.get("frequency_class"), "item": ctx.get("item_name"), "product": ctx.get("product_name")}
        ev = AT.evaluate(text, src)
        key = ev["normalized"] or norm(text)
        status = "new" if any(sp[0] == "event" and norm(sp[1]) in AT.ledger for sp in ev["spans"]) else "exact"
        e = entries.get(key)
        if e is None:
            e = OrderedDict([("id", mkid("PHR", key)), ("normalized", key), ("raw_variants", []), ("kinds", ["safety_phrase"]), ("langs", ["ko"]), ("locators", []), ("modality_codes", []), ("contexts", []), ("status", status),
                             ("units", []), ("created_units", []), ("candidates", ev["candidates"]), ("parsed", dict(ev["parsed"], events=ev["event_fragments"], sites=_dedupe(c["site"] for c in ev["candidates"] if c["site"]), relative_sites=ev["relative_sites"], courses=ev["courses"], qualifiers=ev["qualifiers"], phrase_shape=ev["phrase_shape"])),
                             ("unregistered", ev["unregistered"]), ("extra_sites", ev["extra_sites"]), ("extra_courses", ev["extra_courses"]), ("extra_qualifiers", ev["extra_qualifiers"]), ("fragment_classes", ev["fragment_classes"]), ("spans", ev["spans"]),
                             ("_uc", ev["unit_candidates"]), ("status_mismatch", 0), ("ledger_events", _dedupe(s[1] for s in ev["spans"] if s[0] == "event" and norm(s[1]) in AT.ledger))])
            entries[key] = e
        elif e["status"] != status:
            e["status_mismatch"] += 1
        for k_ in ("side", "predicate", "grammar"):
            for x_ in ev["parsed"].get(k_, []):
                if x_ not in e["parsed"].setdefault(k_, []):
                    e["parsed"][k_].append(x_)
        if text not in e["raw_variants"]:
            e["raw_variants"].append(text)
        e["locators"].append(src["locator"])
        if src.get("modality") and src["modality"] not in e["modality_codes"]:
            e["modality_codes"].append(src["modality"])
        e["contexts"].append({"locator": src["locator"], "kind": kind, "from": V31._from_end(src), "modality": src.get("modality"), "frequency_class": ctx.get("frequency_class")})
        phrase_rows.append({"locator": src["locator"], "text": text, "status": status, "phrase_id": e["id"], "from": V31._from_end(src)})
    units_names_only = len(AT.tuples)
    for e in entries.values():
        src0 = {"origin": "safety_phrase", "locator": e["locators"][0], "phrase_id": e["id"], "kind": "safety_phrase"}
        ids_ = []
        for c in e["_uc"]:
            existed = AT.unit_key(c) in AT.units
            tid = AT.register_unit(c, src0)
            ids_.append(tid)
            if not existed:
                e["created_units"].append(tid)
                AT.created[tid] = e["id"]
                AT.tuples[tid]["created_by_phrase"] = e["id"]
        e["units"] = _dedupe(ids_)
        for c in e["candidates"]:
            c["exists"] = True
            c["unit_id"] = AT.units.get((c["event_id"], c["site_id"], c["qualifier_id"]))
        e.pop("_uc", None)
    phrase_edges = OrderedDict()
    for e in entries.values():
        for ctx in e["contexts"]:
            for uid in e["units"]:
                k = (ctx["from"], uid)
                pe = phrase_edges.setdefault(k, {"from": ctx["from"], "unit": uid, "source_phrases": [], "courses": [], "frequency_class": [], "created_by_phrase": uid in AT.created})
                if e["id"] not in pe["source_phrases"]:
                    pe["source_phrases"].append(e["id"])
                pe["courses"] = _dedupe(pe["courses"] + [co for c in e["candidates"] if c.get("unit_id") == uid for co in c["courses"]])
                if ctx["frequency_class"] and ctx["frequency_class"] not in pe["frequency_class"]:
                    pe["frequency_class"].append(ctx["frequency_class"])
    # ---- ③ 다른 테이블 — 참조만(refer · 단위를 세우지 않는다)
    AT.mode, AT.ctx = "refer", None

    def refer(text, src):
        ev = AT.evaluate(text, src)
        refs = _dedupe(AT.units.get((c["event_id"], c["site_id"], c["qualifier_id"])) for c in ev["candidates"] if (c["event_id"], c["site_id"], c["qualifier_id"]) in AT.units)
        missing = [c["event"] for c in ev["candidates"] if (c["event_id"], c["site_id"], c["qualifier_id"]) not in AT.units]
        st = ("ref" if refs and not missing and not ev["unregistered"] else "ref_partial") if refs else "none"
        return {"adverse_ref": refs, "ref_status": st, "missing": missing, "unregistered": ev["unregistered"], "parsed": dict(ev["parsed"], events=ev["event_fragments"], courses=ev["courses"]), "candidates": [(c["event"], c["site"], c["qualifier"]) for c in ev["candidates"]]}

    timelines = []
    for ti, tl in enumerate(L["post-procedure-timeline.json"]["timelines"]):
        code = tl["category"].split("-")[0]
        T = {"id": mkid("TML", tl["id"]), "ledger_id": tl["id"], "name": tl["name"], "category": tl["category"], "modality": code, "locator": locator("post-procedure-timeline.json", "timelines[].name", str(ti)), "phases": []}
        for pi, ph in enumerate(tl["phases"]):
            P = {"order": pi, "period": ph["period"], "label": ph["label"], "locator": locator("post-procedure-timeline.json", "timelines[].phases[].period", f"{ti}/{pi}"), "lines": []}
            for lvl in ("normal", "abnormal", "caution", "emergency"):
                for li, x in enumerate(ph.get(lvl) or []):
                    loc = locator("post-procedure-timeline.json", f"timelines[].phases[].{lvl}[]", f"{code}/{sum(1 for _ in [])}")
                    loc = locator("post-procedure-timeline.json", f"timelines[].phases[].{lvl}[]", f"{ti}/{pi}/{li}")
                    r = refer(x, {"locator": loc, "origin": f"timeline.{lvl}"})
                    if lvl == "normal" and not r["adverse_ref"]:
                        r["ref_status"] = "normal_memo"
                    P["lines"].append(dict(r, reaction_level=lvl, text=x, locator=loc))
            T["phases"].append(P)
        timelines.append(T)
    signs = OrderedDict()
    for cat in L["consent-checklist.json"]["categories"]:
        for i, x in enumerate(cat.get("emergency_signs") or []):
            loc = locator("consent-checklist.json", "categories[].emergency_signs[]", f"{cat['id']}/{i}")
            k = norm(x)
            s = signs.get(k)
            if s is None:
                s = dict(refer(x, {"locator": loc, "origin": "consent.emergency"}), id=mkid("SGN", k), text=x, modality_codes=[], locators=[])
                signs[k] = s
            s["modality_codes"].append(cat["id"])
            s["locators"].append(loc)
    disclosures = []
    for cat in L["consent-checklist.json"]["categories"]:
        for i, x in enumerate(cat.get("mandatory_disclosures") or []):
            loc = locator("consent-checklist.json", "categories[].mandatory_disclosures[]", f"{cat['id']}/{i}")
            disclosures.append(dict(refer(x, {"locator": loc, "origin": "consent.disclosure"}), rule_id=mkid("RUL", f"disclosure|{x}"), text=x, modality=cat["id"], locator=loc))
    literature = []
    for code, cat in L["literature-evidence.json"]["categories"].items():
        for i, ae in enumerate(cat.get("adverse_effects") or []):
            loc = locator("literature-evidence.json", "categories.{code}.adverse_effects[].statement", f"{code}/{i}")
            r1 = refer(ae["statement"], {"locator": loc, "origin": "literature"})
            r2 = refer(ae["patient_ko"], {"locator": loc.replace(".statement@", ".patient_ko@"), "origin": "literature.patient_ko"}) if ae.get("patient_ko") else {"adverse_ref": [], "ref_status": "none"}
            refs = _dedupe(r1["adverse_ref"] + r2["adverse_ref"])
            literature.append({"id": mkid("EVS", f"{code}|adverse_effects|{ae['statement']}"), "modality": code, "locator": loc, "statement": ae["statement"], "patient_ko": ae.get("patient_ko"), "adverse_ref": refs,
                               "ref_status": "ref" if refs and "ref" in (r1["ref_status"], r2["ref_status"]) else ("ref_partial" if refs else "none"), "statement_ref": r1["ref_status"], "patient_ko_ref": r2["ref_status"],
                               "translations": [{"lang": lg, "locator": loc.replace(".statement@", f".patient_{lg}@")} for lg in ("en", "zh", "ja") if ae.get(f"patient_{lg}")]})
    # ---- R15 · R34 · R35
    all_edges = OrderedDict()
    for k, e in name_edges.items():
        all_edges[k] = dict(e, source_phrases=[], frequency_class=[], timeline_refs=[], emergency_sign_refs=[], layer="family")
    for k, e in phrase_edges.items():
        if k in all_edges:
            all_edges[k]["source_phrases"] = e["source_phrases"]
            all_edges[k]["courses"] = _dedupe(all_edges[k]["courses"] + e["courses"])
            all_edges[k]["frequency_class"] = e["frequency_class"]
        else:
            all_edges[k] = dict(e, names=[], attrs={}, timeline_refs=[], emergency_sign_refs=[], layer="item" if k[0][0] in ("procedure(item)", "product") else "family")
    r34 = []
    for T in timelines:
        for P in T["phases"]:
            for ln in P["lines"]:
                for uid in ln["adverse_ref"]:
                    r34.append({"timeline": T["id"], "line_locator": ln["locator"], "unit": uid, "reaction_level": ln["reaction_level"], "period": P["period"], "phase_label": P["label"]})
                    k = (("modality", T["modality"]), uid)
                    e = all_edges.get(k)
                    if e is None:
                        e = all_edges[k] = {"from": ("modality", T["modality"]), "unit": uid, "courses": [], "names": [], "attrs": {}, "source_phrases": [], "frequency_class": [], "timeline_refs": [], "emergency_sign_refs": [], "layer": "family", "created_by_phrase": False}
                    e["timeline_refs"].append(ln["locator"])
    r35 = []
    for s in signs.values():
        for uid in s["adverse_ref"]:
            r35.append({"sign": s["id"], "unit": uid})
            for code in s["modality_codes"]:
                k = (("modality", code), uid)
                e = all_edges.get(k)
                if e is None:
                    e = all_edges[k] = {"from": ("modality", code), "unit": uid, "courses": [], "names": [], "attrs": {}, "source_phrases": [], "frequency_class": [], "timeline_refs": [], "emergency_sign_refs": [], "layer": "family", "created_by_phrase": False}
                e["emergency_sign_refs"].append(s["id"])
    # ---- V3.2-8 단위 일반값(참조) · 상속
    A = AT.tuples
    for t in A.values():
        t["general_description"] = []
        t["general_management"] = []
    for lit in literature:
        for uid in lit["adverse_ref"]:
            A[uid]["general_description"].append({"ref": lit["id"], "locator": lit["locator"]})
    for k, e in name_edges.items():
        for al in e["attrs"].get("management", []):
            A[e["unit"]]["general_management"].append({"ref": f"R15:{k[0][1]}→{e['unit']}", "locator": al})
    fam_edge = {(k[0][1], k[1]): e for k, e in all_edges.items() if k[0][0] == "modality"}
    inherit_rows = []
    for k, e in all_edges.items():
        fk = k[0][0]
        fam = str(k[0][1]).split("/")[0] if fk in ("procedure(item)", "product") else (k[0][1] if fk == "modality" else None)
        inh = []
        for a in INHERIT_ATTRS:
            if e.get("attrs", {}).get(a):
                inh.append({"attr": a, "basis": "item" if fk != "modality" else "family", "ref": e["attrs"][a][0]})
                continue
            fe = fam_edge.get((fam, e["unit"])) if fk != "modality" else None
            if fe is not None and fe.get("attrs", {}).get(a):
                inh.append({"attr": a, "basis": "family", "ref": f"R15:{fam}→{e['unit']}", "ref_locator": fe["attrs"][a][0]})
                continue
            gen = A[e["unit"]]["general_management"] if a == "management" else []
            if gen:
                inh.append({"attr": a, "basis": "unit", "ref": f"{e['unit']}.general_management", "ref_locator": gen[0]["locator"]})
                continue
            inh.append({"attr": a, "basis": "none", "ref": None})
        e["inheritance"] = inh
        inherit_rows.append((fk, e["unit"], inh))
    # ---- ⑦ 원장 사건 노드 ↔ 사전 사건
    keys = set(base_surface) | set(AT.ledger)
    dup = duplicate_pairs(AT.ledger, base_surface, kr, paren_node_pairs(CUR["texts"], keys))
    # ---- 집계
    ledger_nodes = [dict(rec, key=k, n_locators=len(rec["locators"]), has_description=bool(rec["contexts"]), dup_candidates=[d["existing"] for d in dup if d["new_id"] == rec["id"] and d["grade"] == "strong"]) for k, rec in AT.ledger.items()]
    occ_status = Counter(r["status"] for r in phrase_rows)
    by_event_top = Counter()
    for t in A.values():
        if t["event_kind"] == "dict":
            by_event_top[t["event"]] += 0
    item_edges = [(k, e) for k, e in all_edges.items() if k[0][0] in ("procedure(item)", "product")]
    ev_of = {t["id"]: t["event"] for t in A.values()}
    inh_by_event = OrderedDict()
    for k, e in item_edges:
        ev = ev_of[e["unit"]]
        d = inh_by_event.setdefault(ev, {"item_edges": 0, "attrs": {a: Counter() for a in INHERIT_ATTRS}})
        d["item_edges"] += 1
        for x in e["inheritance"]:
            d["attrs"][x["attr"]][x["basis"]] += 1
    inh_by_event = OrderedDict(sorted(inh_by_event.items(), key=lambda kv: -kv[1]["item_edges"]))
    tl_lines = [ln for T in timelines for P in T["phases"] for ln in P["lines"]]
    summary = OrderedDict([
        ("complications_names", len(comp_rows)), ("complications_by_status", dict(Counter(r["status32"] for r in comp_rows))), ("complications_distinct_units", len(_dedupe(x for r in comp_rows for x in r["unit_ids"]))),
        ("complications_raw_name", sum(1 for r in comp_rows if r["status32"] == "raw")),
        ("safety_occurrences", len(phrase_rows)), ("safety_by_status", dict(occ_status)), ("safety_entries", len(entries)), ("safety_entries_by_status", dict(Counter(e["status"] for e in entries.values()))),
        ("memo_entries", len(memo)), ("memo_entries_by_status", dict(Counter(e["status"] for e in memo.values()))), ("entries_status_mismatch", sum(e["status_mismatch"] for e in list(entries.values()) + list(memo.values()))),
        ("adverse_unattached", sum(1 for r in phrase_rows if r["status"] in ("exact", "new") and not entries[next(k for k, e in entries.items() if e["id"] == r["phrase_id"])]["units"])),
        ("ledger_events", len(AT.ledger)), ("ledger_events_without_locator", sum(1 for n in ledger_nodes if not n["locators"])), ("ledger_events_without_description", sum(1 for n in ledger_nodes if not n["contexts"])),
        ("dup_pairs", len(dup)), ("dup_pairs_strong", sum(1 for d in dup if d["grade"] == "strong")), ("dup_pairs_weak", sum(1 for d in dup if d["grade"] == "weak")), ("dup_pairs_node_node", sum(1 for d in dup if d["existing_kind"] == "ledger")), ("dup_ledger_events", len({d["new"] for d in dup} | {d["existing"] for d in dup if d["existing_kind"] == "ledger"})), ("dup_by_rule", dict(Counter(r_ for d in dup for r_ in d["rules"]))),
        ("units_total", len(A)), ("units_from_names_only", units_names_only), ("units_by_event_kind", dict(Counter(t["event_kind"] for t in A.values()))), ("units_with_ledger_event", sum(1 for t in A.values() if norm(t["event"]) in AT.ledger)),
        ("units_created_by_phrases", len(AT.created)), ("edges_total", len(all_edges)), ("edges_by_from_kind", dict(Counter(k[0][0] for k in all_edges))), ("edges_with_course", sum(1 for e in all_edges.values() if e["courses"])),
        ("edges_from_names", len(name_edges)), ("edges_from_safety", len(phrase_edges)), ("edges_with_timeline_refs", sum(1 for e in all_edges.values() if e["timeline_refs"])), ("edges_with_sign_refs", sum(1 for e in all_edges.values() if e["emergency_sign_refs"])),
        ("timelines", len(timelines)), ("timeline_phases", sum(len(T["phases"]) for T in timelines)), ("timeline_lines", len(tl_lines)), ("timeline_lines_by_status", dict(Counter(ln["ref_status"] for ln in tl_lines))),
        ("timeline_lines_by_level_status", {lv: dict(Counter(ln["ref_status"] for ln in tl_lines if ln["reaction_level"] == lv)) for lv in ("normal", "abnormal", "caution", "emergency")}), ("r34", len(r34)),
        ("emergency_sign_rows", sum(len(s["locators"]) for s in signs.values())), ("emergency_signs", len(signs)), ("emergency_signs_by_status", dict(Counter(s["ref_status"] for s in signs.values()))), ("r35", len(r35)),
        ("disclosures", len(disclosures)), ("disclosures_by_status", dict(Counter(d["ref_status"] for d in disclosures))),
        ("literature", len(literature)), ("literature_by_status", dict(Counter(x["ref_status"] for x in literature))), ("units_with_general_description", sum(1 for t in A.values() if t["general_description"])), ("units_with_general_management", sum(1 for t in A.values() if t["general_management"])),
        ("inheritance_item_edges", len(item_edges)), ("inheritance_by_basis", {a: dict(Counter(x["basis"] for k, e in item_edges for x in e["inheritance"] if x["attr"] == a)) for a in INHERIT_ATTRS}),
        ("inheritance_missing_basis", sum(1 for k, e in all_edges.items() for x in e["inheritance"] if not x.get("basis"))), ("inheritance_copied_values", sum(1 for k, e in all_edges.items() for x in e["inheritance"] if "value" in x)),
        ("inheritance_by_event", {ev: {"item_edges": d["item_edges"], "attrs": {a: dict(c) for a, c in d["attrs"].items()}} for ev, d in list(inh_by_event.items())[:12]}),
        ("unregistered_reference_tables", dict(Counter(u for ln in tl_lines for u in ln["unregistered"]).most_common(40))),
    ])
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("phrase_dictionary", list(entries.values())), ("memo_phrases", list(memo.values())), ("phrase_rows", phrase_rows),
                        ("ledger_events", ledger_nodes), ("duplicate_pairs", dup), ("timelines", timelines), ("emergency_signs", list(signs.values())), ("disclosures", disclosures), ("literature", literature),
                        ("edges", [dict(e, from_=list(e["from"]), **{"from": list(e["from"])}) for e in all_edges.values()]), ("r34", r34), ("r35", r35), ("gloss_pairs", AT.gloss_sink)])


# ---------------------------------------------------------------------------
# V3.2-5 장비 항목 → 제품(origin=taxonomy) — 자동 등록(열린 사전 · 원장 칸이 종류를 선언)
# ---------------------------------------------------------------------------
def equipment_items(L, dic_json, er):
    D = {d["name"]: d for d in dic_json["dictionaries"]}
    known = {}
    for dn in ("modality", "modality_subcategory_label", "product_name", "technique"):
        for e in D[dn]["entries"]:
            known.setdefault(norm(e["canonical"]), f"{dn}:{e['canonical']}")
            for s in e.get("synonyms", []):
                known.setdefault(norm(s["value"]), f"{dn}:{e['canonical']}")
    extra = {sid for sid, _ in er["extra_subcats"]}
    out = []
    for m in L["taxonomy.json"]["modality"]:
        for si, sc in enumerate(m["subcategories"]):
            fam_ok = m["id"] in er["families"] or sc["id"] in extra
            if not fam_ok:
                continue
            sub_excl = any(w in (sc.get("label") or "") for w in er["exclude_subcat_words"])
            for ii, it in enumerate(sc["items"]):
                loc = locator("taxonomy.json", "modality[].subcategories[].items[].name", f"{m['id']}/{si}/{ii}")
                why = None
                if sub_excl:
                    why = "subcategory:" + sc["label"]
                elif any(w in it["name"] for w in er["exclude_name_words"]):
                    why = "name_word:" + next(w for w in er["exclude_name_words"] if w in it["name"])
                elif norm(it["name"]) in known:
                    why = "already:" + known[norm(it["name"])]
                out.append({"family": m["id"], "subcategory": sc["id"], "subcategory_label": sc["label"], "name": it["name"], "locator": loc, "excluded": why, "register": why is None})
    return out


def add_equipment_products(dic_json, items):
    dj = copy.deepcopy(dic_json)
    D = {d["name"]: d for d in dj["dictionaries"]}
    pn = D["product_name"]
    seen = {}
    for it in items:
        if not it["register"]:
            continue
        k = norm(it["name"])
        if k in seen:
            e = seen[k]
            if it["family"] not in str(e["code"]).split("|"):
                e["code"] = f"{e['code']}|{it['family']}"
            e["sources"].append({"file": "taxonomy.json", "path": "modality[].subcategories[].items[].name", "n": 1, "kind": "value", "locator": it["locator"]})
            continue
        e = {"id": mkid("DIC", f"product_name|{it['name']}"), "canonical": it["name"], "sources": [{"file": "taxonomy.json", "path": "modality[].subcategories[].items[].name", "n": 1, "kind": "value", "locator": it["locator"]}], "synonyms": [], "definition": None,
             "code": it["family"], "origin": "taxonomy", "status": "unreviewed", "license_status": "미확인", "kind_note": "장비(V3.2-5)"}
        pn["entries"].append(e)
        seen[k] = e
    return dj, list(seen.values())


# ---------------------------------------------------------------------------
# 규칙 데이터 · 전체 실행
# ---------------------------------------------------------------------------
def rule_data():
    """erd-v3.2.json(있으면) → 아니면 명세 데이터."""
    sys.path.insert(0, HERE)
    import erd_spec_v32 as D  # noqa
    tok = {"particles": D.PARTICLES, "verb_endings": D.VERB_ENDINGS, "grammar_words": D.GRAMMAR_WORDS, "stem_min_len": D.STEM_MIN_LEN, "relaxed_suffixes": D.RELAXED_SUFFIXES}
    kinds = {"conj_particles": D.CONJ_PARTICLES, "predicate_endings": D.PREDICATE_ENDINGS, "core_exclude": D.CORE_EXCLUDE, "note_words": D.NOTE_WORDS, "sentence_min_tokens": D.SENTENCE_MIN_TOKENS, "sentence_min_grammar": D.SENTENCE_MIN_GRAMMAR, "sentence_latin_ratio": D.SENTENCE_LATIN_RATIO, "fallback_core": D.FALLBACK_CORE, "dup_prefix_min": D.DUP_PREFIX_MIN}
    equip = {"families": D.EQUIP_FAMILIES, "extra_subcats": D.EQUIP_EXTRA_SUBCATS, "exclude_subcat_words": D.EQUIP_EXCLUDE_SUBCAT_WORDS, "exclude_name_words": D.EQUIP_EXCLUDE_NAME_WORDS, "abbrev_min_len": D.ABBREV_MIN_LEN}
    p = os.path.join(HERE, "erd-v3.2.json")
    if os.path.exists(p):
        j = json.load(open(p, encoding="utf-8"))
        tok = j["resolve_rules"].get("tokenize", tok)
        kinds = j["tuple_rules"].get("phrase_kinds", kinds)
        equip = j["tuple_rules"].get("equipment", equip)
    return tok, kinds, equip, D


def base_dictionary(dic_json):
    """v3.2 사전 파일에 실린 파생 항목(origin ledger · taxonomy)을 뺀 ERD 사전 — 분해의 바탕."""
    dj = copy.deepcopy(dic_json)
    for d in dj["dictionaries"]:
        d["entries"] = [e for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
    dj["dictionaries"] = [d for d in dj["dictionaries"] if d["name"] != "phrase_dictionary"]
    return dj


def run_all32(dic_json, rules, L, resolve_rules, v31tup=None, flags=None, equipment=True):
    flags = dict(FLAGS_V32 if flags is None else flags)
    tokr, kinds, equip, D = rule_data()
    texts = ledger_texts(L)
    vocab, vlocs = build_vocab(texts)
    tok = Tokenizer(tokr, vocab)
    Dn = {d["name"]: d for d in dic_json["dictionaries"]}
    ing = {}
    for e in Dn[INGREDIENT_DICT]["entries"]:
        ing[norm(e["canonical"])] = e
        for s in e.get("synonyms", []):
            ing[norm(s["value"])] = e
    eq_items = equipment_items(L, dic_json, equip)
    dj, eq_products = (add_equipment_products(dic_json, eq_items) if (equipment and flags["phrase_kinds"]) else (dic_json, []))
    CUR.update(texts=texts, tok=tok, flags=flags, ingredient=ing, gloss_sink=[], kinds=kinds, fallback_core=kinds["fallback_core"], vocab=vocab, equip=equip, adv_stop=rules["adverse"]["adverse_stopwords"]["words"])
    saved = {k: getattr(V31, k) for k in ("ProcedureTuples31", "ConditionTuples", "run_adverse31")}
    saved_dwk = V22.DICT_WHAT_KINDS
    try:
        V31.ProcedureTuples31 = ProcedureTuples32
        V31.ConditionTuples = ConditionTuples32
        if flags["phrase_kinds"]:
            V31.run_adverse31 = lambda ids, r, L_, v3tup=None: run_adverse32(ids, r, L_, v31tup)
        if flags["ingredient_what"]:
            V22.DICT_WHAT_KINDS = tuple(saved_dwk) + ("ingredient",)
        R = V31.run_all(dj, rules, L, resolve_rules, v31tup)
    finally:
        for k, v in saved.items():
            setattr(V31, k, v)
        V22.DICT_WHAT_KINDS = saved_dwk
    R["erd_version"] = "v3.2"
    R["flags"] = flags
    R["tokenizer"] = {"hits": dict(tok.hits), "locators": {k: v for k, v in tok.hit_locs.items()}, "log": tok.log}
    R["gloss_pairs_other"] = list(CUR["gloss_sink"])
    R["equipment"] = {"items": eq_items, "products": eq_products}
    R["vocab_size"] = len(vocab)
    R["_vocab"] = (vocab, vlocs, texts)
    return R


# ---------------------------------------------------------------------------
# V3.2-2(b) 자모 변형 쌍 — 원장 전체 어휘 · 같은 자리 하나 치환 · 목록(적용 0)
# ---------------------------------------------------------------------------
def variant_pairs(vocab, vlocs, surfaces, skip):
    """vocab {norm: n} · surfaces {norm: 'dict:canonical'} · skip = 문법·수식어 norm."""
    words = [w for w in vocab if not DIGIT.search(w) and w not in skip and ((HANGUL.search(w) and len(w) >= 2) or (not HANGUL.search(w) and LATIN.search(w) and len(w) >= 4))]
    words += [w for w in surfaces if w not in vocab and not DIGIT.search(w) and ((HANGUL.search(w) and len(w) >= 2) or (LATIN.search(w) and len(w) >= 4))]
    buckets = defaultdict(list)
    for w in set(words):
        buckets[len(jamo(w))].append(w)
    out = []
    for n, ws in buckets.items():
        ws.sort()
        J = {w: jamo(w) for w in ws}
        for i, a in enumerate(ws):
            ja = J[a]
            for b in ws[i + 1:]:
                jb = J[b]
                d = 0
                for x, y in zip(ja, jb):
                    if x != y:
                        d += 1
                        if d > 1:
                            break
                if d == 1:
                    out.append({"a": a, "b": b, "a_dict": surfaces.get(a), "b_dict": surfaces.get(b), "a_n": vocab.get(a, 0), "b_n": vocab.get(b, 0), "a_locators": vlocs.get(a, [])[:12], "b_locators": vlocs.get(b, [])[:12],
                                "status": "proposed", "applied": False})
    out.sort(key=lambda x: (-(x["a_n"] + x["b_n"]), x["a"]))
    return out


def all_surfaces(dic_json):
    out = {}
    for d in dic_json["dictionaries"]:
        if d["name"] in ("phrase_dictionary", "catalog_item_name"):
            continue
        for e in d["entries"]:
            out.setdefault(norm(e["canonical"]), f"{d['name']}:{e['canonical']}")
            for s in e.get("synonyms", []):
                out.setdefault(norm(s["value"]), f"{d['name']}:{e['canonical']}")
    return out


# ---------------------------------------------------------------------------
# V3.2-3/4/6 씨앗 후보 — 닫힌 목록(부위·경과·물질·상대 부위) · 문맥 추정(성분 · 시술 조각) · 줄임말 접두(제품)
# ---------------------------------------------------------------------------
def token_locators(texts, value, tk=None):
    """value(공백 토큰 열)가 문자열 자리의 토큰 열에 연속으로 나오는 자리 전부(조사·어미는 떼고 본다)."""
    vt = [norm(x) for x in str(value).split()]
    out = []
    for ax, kind, f, p, loc, text, mod in texts:
        toks = [norm(t) for t in raw_tokens(text)]
        if tk:
            toks2 = []
            for t in raw_tokens(text):
                st = tk.strip(t, lambda s: False)
                toks2.append(norm(st[0]) if st else norm(t))
        else:
            toks2 = toks
        n = len(vt)
        hit = any(toks[i:i + n] == vt or toks2[i:i + n] == vt for i in range(len(toks) - n + 1)) or (n > 1 and any(t == "".join(vt) for t in toks))
        if hit:
            out.append({"locator": loc, "axis": ax, "path": f"{f}:{p}", "text": text})
    return out


def seed_candidates(R, dic_json, L, D):
    vocab, vlocs, texts = R["_vocab"]
    tk = CUR["tok"]
    Dn = {d["name"]: d for d in dic_json["dictionaries"]}
    site_existing = {norm(e["canonical"]): e for e in Dn["site"]["entries"]}
    rel_existing = {norm(e["canonical"]): e for e in Dn["relative_site"]["entries"]}
    out = OrderedDict()
    homo = {norm(w) for w in CUR["tok"].grammar} | {norm(w["word"]) for w in (CUR.get("adv_stop") or [])}
    # ---- 부위(닫힌 목록 · V3.2-4)
    rows = []
    for val, kind, parent, syns in D.SITE_CLOSED:
        ex = (site_existing.get(norm(val)) or rel_existing.get(norm(val)))
        locs = token_locators(texts, val, tk)
        syn_rows = []
        for sv in syns:
            sl = token_locators(texts, sv, tk)
            syn_rows.append({"value": sv, "n": len(sl), "locators": [x["locator"] for x in sl], "status": "proposed" if sl else "원장에 없음"})
        rows.append({"value": val, "kind": kind, "parent": parent, "existing": bool(ex), "existing_kind": (ex or {}).get("kind") if ex else None, "n": len(locs), "locators": [x["locator"] for x in locs],
                     "paths": dict(Counter(x["path"] for x in locs)), "synonyms": syn_rows, "closed": True,
                     "homograph": norm(val) in homo,
                     "status": ("기존 값(parent 제안)" if ex else ("동형어 — 확인 필요(수식어·문법 낱말과 같은 꼴 · 자리 수는 상한)" if norm(val) in homo and locs else ("proposed" if (locs or any(x["n"] for x in syn_rows)) else "원장에 없음")))})
    out["site"] = {"dictionary": "site", "closed": True, "why_closed": "부위 kind(anatomical·region·layer·relative)와 계층(parent)은 임상 해석이라 원장 어휘가 바로 값이 되지 않는다 — 목록은 발주서 V3.2-4 로 닫고 승인으로만 연다", "rows": rows}
    # ---- 시술 조각(미등록) 전부 — 자리별 locator
    frag = defaultdict(lambda: {"n": 0, "locators": [], "paths": Counter(), "labels": []})
    site_sites = {x[2]: (x[0], x[3]) for x in []}
    loc_by_label = defaultdict(list)
    for slot, f, p, loc, lab, hint in procedure_label_sites(L):
        if lab is not None:
            loc_by_label[(str(lab), hint)].append((loc, f"{f}:{p}"))
            loc_by_label[(str(lab), None)].append((loc, f"{f}:{p}"))
    prow = []
    for r in R["procedure"]["catalog"]:
        prow.append((r["name"], r["family"], r.get("unregistered") or []))
    for slot, rows_ in R["procedure"]["references"].items():
        for r in rows_:
            prow.append((r["label"], r.get("hint"), r.get("unregistered") or []))
    for r in R["procedure"]["market_pricing"]:
        prow.append((r["label"], r.get("hint"), r.get("unregistered") or []))
    for lab, hint, unr in prow:
        locs = loc_by_label.get((str(lab), hint)) or loc_by_label.get((str(lab), None)) or []
        for u in _dedupe(unr):
            fr = frag[u]
            for loc, pth in locs:
                if loc not in fr["locators"]:
                    fr["locators"].append(loc)
                    fr["paths"][pth] += 1
            fr["n"] += max(1, len(locs))
            if str(lab) not in fr["labels"]:
                fr["labels"].append(str(lab))
    site_vals = {norm(v): v for v, k, pa, sy in D.SITE_CLOSED} | {norm(s): v for v, k, pa, sy in D.SITE_CLOSED for s in sy}
    ctxw = {norm(w) for w in D.INGREDIENT_CONTEXT_WORDS}
    named = {norm(w): w for w in D.INGREDIENT_NAMED}
    ing_rows, term_rows, site_frag = [], [], []
    ing_have = {norm(e["canonical"]) for e in Dn["ingredient_material"]["entries"]}
    ptype = {norm(e["canonical"]): e["canonical"] for e in Dn["product_type"]["entries"]}
    for u, fr in sorted(frag.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
        nu = norm(u)
        base = {"value": u, "n": fr["n"], "locators": fr["locators"], "paths": dict(fr["paths"]), "labels": fr["labels"][:12], "seed": fr["n"] >= 2 or len(fr["locators"]) >= 2}
        if nu in site_vals:
            site_frag.append(dict(base, site=site_vals[nu], status="proposed" if base["seed"] else "빈도 1(후보 아님)"))
            continue
        ctx = []
        for lab in fr["labels"]:
            tt = [norm(t) for t in raw_tokens(lab)]
            for i_, t_ in enumerate(tt):
                if t_ == nu and ((i_ + 1 < len(tt) and tt[i_ + 1] in ctxw) or (i_ > 0 and tt[i_ - 1] in ctxw)):
                    ctx.append(lab)
                    break
        if nu in named or ctx:
            if nu not in ing_have:
                ing_rows.append(dict(base, basis=("발주서 명시(필링 산·성분)" if nu in named else "문맥(바로 옆 토큰 " + "·".join(sorted({t for lab in ctx for t in raw_tokens(lab) if norm(t) in ctxw})) + ")"), context_labels=ctx[:8], status="proposed" if base["seed"] else "빈도 1(후보 아님)"))
            continue
        term_rows.append(dict(base, recommend=("product_type 값 「" + ptype[nu] + "」 — 계열·하위분류 동의어 후보") if nu in ptype else "시술 조각(사전 선택: modality·modality_subcategory_label·technique 동의어)", status="proposed" if base["seed"] else "빈도 1(후보 아님)"))
    # 발주서 명시 성분 중 조각에 안 나온 것 — 어휘 locator 로
    for w in D.INGREDIENT_NAMED:
        if norm(w) in ing_have or any(norm(r["value"]) == norm(w) for r in ing_rows):
            continue
        locs = token_locators(texts, w, tk)
        basis_ = "발주서 명시(어휘 전수)"
        if not locs:
            nw = norm(w)
            locs = [{"locator": loc, "axis": ax, "path": f"{f}:{p_}", "text": text} for ax, kind, f, p_, loc, text, mod in texts if any(norm(t).startswith(nw) and norm(t)[len(nw):] in ctxw for t in raw_tokens(text))]
            basis_ = "발주서 명시(합성 토큰 「값+필링/필」)" if locs else basis_
        ing_rows.append({"value": w, "n": len(locs), "locators": [x["locator"] for x in locs], "paths": dict(Counter(x["path"] for x in locs)), "labels": [], "seed": len(locs) >= 2, "basis": basis_, "context_labels": [],
                         "status": "proposed" if len(locs) >= 2 else ("빈도 1(후보 아님)" if locs else "원장에 없음")})
    tox = [(w, vocab[w]) for w in vocab if re.match(r"^\d+(?:u|유닛|단위)$", w)]
    out["ingredient_material"] = {"toxin_units": {"tokens": tox, "note": "톡신 단위(U·유닛·단위)는 성분이 아니라 규격 — §1.3 규격 정규식·unit 사전이 받는다(성분 씨앗 대상 아님)"}, "dictionary": "ingredient_material", "closed": False, "why_not_auto": "성분은 열린 사전이지만 원장이 「성분」이라고 칸으로 선언한 곳은 products.json ingredient/material 뿐(이미 사전 10) — 그 밖은 라벨에서 바로 옆 토큰(필링·필러·실)으로 추정한 것이라(「아이 필러」의 아이) 자동으로 세우지 않고 승인 묶음으로 둔다", "rows": ing_rows}
    out["site_fragments"] = {"dictionary": "site", "closed": True, "note": "시술 라벨의 미등록 조각 중 부위 닫힌 목록(값·동의어)에 닿는 것 — 승인되면 그 값으로", "rows": site_frag}
    out["procedure_term"] = {"dictionary": "(선택)", "closed": None, "note": "시술 라벨의 남은 미등록 조각 — 어느 사전 동의어인지는 사람이 고른다(종류 추정 규칙 밖)", "rows": term_rows}
    # ---- 줄임말·옛 이름(접두 규칙 · V3.2-5) — 제품 이름 ↔ 미등록 조각 · 자동 장비 제품 ↔ 기존 제품
    prods = {}
    for e in Dn["product_name"]["entries"]:
        prods.setdefault(norm(e["canonical"]), (e["canonical"], e.get("origin") or "ledger_product"))
        for s in e.get("synonyms", []):
            prods.setdefault(norm(s["value"]), (e["canonical"], e.get("origin") or "ledger_product"))
    eqp = {norm(p["canonical"]): (p["canonical"], "taxonomy") for p in R["equipment"]["products"]}
    allp = dict(prods)
    allp.update(eqp)
    ab = []
    mn = CUR["equip"]["abbrev_min_len"]
    for u, fr in frag.items():
        nu = norm(u)
        if len(nu) < mn:
            continue
        for pk, (canon, origin) in allp.items():
            if pk != nu and min(len(pk), len(nu)) >= mn and (pk.startswith(nu) or nu.startswith(pk)):
                ab.append({"fragment": u, "product": canon, "product_origin": origin, "rule": "정식명이 줄임말을 접두로 포함" if pk.startswith(nu) else "조각이 제품명을 접두로 포함", "n": fr["n"], "locators": fr["locators"], "status": "proposed"})
    for pk, (canon, origin) in eqp.items():
        for qk, (c2, o2) in prods.items():
            if pk != qk and min(len(pk), len(qk)) >= mn and (pk.startswith(qk) or qk.startswith(pk)):
                ab.append({"fragment": canon, "product": c2, "product_origin": o2, "rule": "자동 장비 제품 ↔ 기존 제품(접두) — ⑦ duplicate_candidate", "n": 1, "locators": [s_["locator"] for x in R["equipment"]["products"] if x["canonical"] == canon for s_ in x["sources"]][:3], "status": "⑦"})
    seen_ab, ab2 = set(), []
    for x in ab:
        if (x["fragment"], x["product"]) not in seen_ab:
            seen_ab.add((x["fragment"], x["product"]))
            ab2.append(x)
    ab = ab2
    ab.sort(key=lambda x: (-x["n"], x["fragment"]))
    out["product_abbrev"] = {"dictionary": "product_name", "closed": False, "note": "줄임말·옛 이름 — 승인 묶음(자동 아님 · V3.2-5)", "rows": ab}
    return out


# ---------------------------------------------------------------------------
# 회귀(규칙 끔 = v3.1) · 사라진 조각 · 참고 실행(씨앗 승인 가정) · R33
# ---------------------------------------------------------------------------
def _canon_json(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, default=str)


def regression_v31(dic_json, rules, L, rrules, v31tup):
    """v3.2 분해 클래스에 규칙을 전부 끄고(FLAGS_OFF) v3.1 실행기를 돌리면 erd-v3.1-tuples.json 요약과 같아야 한다."""
    CUR.update(flags=dict(FLAGS_OFF), tok=None, gloss_sink=[], ingredient={})
    e31 = json.load(open(os.path.join(HERE, "erd-v3.1.json"), encoding="utf-8"))
    rules, rrules = e31["tuple_rules"], e31["resolve_rules"]   # v3.1 규칙 데이터 그대로
    saved = {k: getattr(V31, k) for k in ("ProcedureTuples31", "ConditionTuples", "AdverseUnits31")}
    try:
        V31.ProcedureTuples31, V31.ConditionTuples, V31.AdverseUnits31 = ProcedureTuples32, ConditionTuples32, AdverseUnits32
        R = V31.run_all(dic_json, rules, L, rrules, json.load(open(os.path.join(HERE, "erd-v3-tuples.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "erd-v3-tuples.json")) else None)
    finally:
        for k, v in saved.items():
            setattr(V31, k, v)
    out = {}
    for ax in ("procedure", "adverse", "condition"):
        a = json.loads(_canon_json(R[ax]["summary"]))
        b = v31tup[ax]["summary"]
        diff = sorted(k for k in set(a) | set(b) if _canon_json(a.get(k)) != _canon_json(b.get(k)))
        out[ax] = {"keys": len(b), "same": not diff, "diff_keys": diff[:20]}
    return out, R


def unregistered_sets(R31):
    adv = set(f for f, n in R31["adverse"]["summary"]["unregistered_all"])
    proc = set()
    for r in R31["procedure"]["catalog"]:
        proc |= set(r.get("unregistered") or [])
    for slot, rows in R31["procedure"]["references"].items():
        for r in rows:
            proc |= set(r.get("unregistered") or [])
    for r in R31["procedure"]["market_pricing"]:
        proc |= set(r.get("unregistered") or [])
    cond = {u for r in R31["condition"]["phrases"] for u in r["unregistered_fragments"]}
    return {"adverse": adv, "procedure": proc, "condition": cond}


def disappeared(tok_log, sets31):
    """토큰화(V3.2-1)가 바꾼 원 토큰 중 v3.1 에서 미등록 조각이던 것 — 축별 · 결과별 distinct."""
    out = OrderedDict()
    for ax in ("adverse", "procedure", "condition"):
        by = defaultdict(set)
        for a, tok, kind, val, suf in tok_log:
            if a == ax and tok in sets31[ax]:
                by[kind].add(tok)
        allx = set().union(*by.values()) if by else set()
        out[ax] = {"distinct": len(allx), "by_outcome": {k: len(v) for k, v in by.items()}, "examples": sorted(allx)[:60]}
    return out


def projection_dictionary(dic_json, seeds, pairs):
    """참고 실행용 — 부위·성분 씨앗 후보(proposed)를 승인했다고 가정한 사전(적용 아님 · 파일에 쓰지 않는다 · 변형 쌍은 목록 승인이라 넣지 않는다)."""
    dj = copy.deepcopy(dic_json)
    Dn = {d["name"]: d for d in dj["dictionaries"]}
    added = Counter()

    def add(dn, canon, syns, extra=None):
        d = Dn[dn]
        e = next((x for x in d["entries"] if norm(x["canonical"]) == norm(canon)), None)
        if e is None:
            e = dict({"id": mkid("DIC", f"{dn}|{canon}"), "canonical": canon, "sources": [], "synonyms": [], "definition": None}, **(extra or {}))
            d["entries"].append(e)
            added[dn + ":value"] += 1
        have = {norm(e["canonical"])} | {norm(s["value"]) for s in e["synonyms"]}
        for sv in syns:
            if norm(sv) not in have:
                e["synonyms"].append({"value": sv, "link": "projection", "sources": []})
                have.add(norm(sv))
                added[dn + ":synonym"] += 1
    for r in seeds["site"]["rows"]:
        if r["kind"] == "relative":
            continue
        syns = [x["value"] for x in r["synonyms"] if x["n"]]
        if r["existing"] or r["n"] or syns:
            add("site", r["value"], syns, {"kind": r["kind"]})
    for r in seeds["ingredient_material"]["rows"]:
        if r["status"] == "proposed":
            add("ingredient_material", r["value"], [])
    return dj, dict(added)


def r33_rows(R):
    rows = R["procedure"]["references"].get("post-procedure-timeline.timelines[].name (10)", [])
    by = {(str(r["label"]), r.get("hint")): r for r in rows}
    out = []
    for T in R["adverse"].get("timelines", []):
        r = by.get((T["name"], T["category"].split("-")[0])) or next((x for x in rows if str(x["label"]) == T["name"]), None)
        end = None
        if r:
            ids_ = V3.tids_of(r) if r.get("result") in ("tuple", "multi_tuple", "combo_ref") else []
            end = {"kind": "procedure", "ids": ids_} if ids_ else {"kind": "modality", "ids": [mkid("MOD", T["modality"])]}
        out.append({"timeline": T["id"], "name": T["name"], "category": T["category"], "end": end, "result": r.get("result") if r else None})
    return out


def run_everything(dic, rules, L, rrules, v31tup):
    base = base_dictionary(dic)
    reg, Roff = regression_v31(base, rules, L, rrules, v31tup)
    R31 = V31.run_all(base, rules, L, rrules, json.load(open(os.path.join(HERE, "erd-v3-tuples.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "erd-v3-tuples.json")) else None)
    sets31 = unregistered_sets(R31)
    R = run_all32(base, rules, L, rrules, v31tup)
    tokr, kinds, equip, D = rule_data()
    vocab, vlocs, texts = R["_vocab"]
    skip = {norm(w) for w in tokr["grammar_words"]} | {norm(w["word"]) for w in rules["adverse"]["adverse_stopwords"]["words"]}
    surf = all_surfaces(base)
    sv, sl = Counter(), defaultdict(list)
    for w, n in vocab.items():
        st = CUR["tok"].strip(w, lambda x: False)
        k = norm(st[0]) if st else w
        sv[k] += n
        for l_ in vlocs.get(w, []):
            if len(sl[k]) < 12 and l_ not in sl[k]:
                sl[k].append(l_)
    pairs = variant_pairs(sv, sl, surf, skip)
    seeds = seed_candidates(R, base, L, D)
    R["r33"] = r33_rows(R)
    gone = disappeared(R["tokenizer"]["log"], sets31)
    # 참고 실행(씨앗 승인 가정 · 적용 아님)
    pdic, added = projection_dictionary(base, seeds, pairs)
    tok_saved = dict(CUR)
    RP = run_all32(pdic, rules, L, rrules, v31tup)
    CUR.clear()
    CUR.update(tok_saved)
    R["v32"] = OrderedDict([("regression_v31", reg), ("disappeared_by_tokenizer", gone), ("variant_pairs", pairs), ("seeds", seeds), ("projection", {"added": added, "R": _metrics(RP)}),
                            ("before", _metrics31(v31tup, R31)), ("after", _metrics(R)), ("tokenizer_words", _tok_table(tokr, R["tokenizer"])), ("kinds_rules", kinds), ("equipment_rules", {k: v for k, v in equip.items()})])
    return R


def _tok_table(tokr, T):
    rows = []
    for kind, ws in (("particle", tokr["particles"]), ("ending", tokr["verb_endings"]), ("word", tokr["grammar_words"]), ("relaxed", tokr.get("relaxed_suffixes", [])), ("predicate", CUR["kinds"].get("predicate_endings", []))):
        for w in ws:
            k = f"{'particle' if kind == 'relaxed' else kind}:{norm(w)}"
            rows.append({"word": w, "kind": kind, "hits": T["hits"].get(k, 0), "locators": T["locators"].get(k, [])[:12]})
    return rows


def _metrics31(v31tup, R31):
    p, a, c = v31tup["procedure"]["summary"], v31tup["adverse"]["summary"], v31tup["condition"]["summary"]
    return OrderedDict([("adverse_unregistered_distinct", a["unregistered_distinct"]), ("adverse_unregistered_total", a["unregistered_total"]), ("phrase_entries", a["phrase_entries"]), ("phrase_entries_by_status", a["phrase_entries_by_status"]),
                        ("phrase_occurrences_by_status", a["phrase_occurrences_by_status"]), ("units", a["tuples_total"]), ("raw_name_units", a["tuples_raw_name"]),
                        ("ref_unresolved", p["reference_total"]["unresolved"]), ("market_unresolved", p["market_pricing"]["unresolved"]), ("unresolved_9", p["reference_total"]["unresolved"] + p["market_pricing"]["unresolved"]),
                        ("catalog_self", p["catalog_self_items"]), ("catalog_by_what_kind", p["catalog_by_what_kind"]), ("procedure_unregistered_distinct", p["unregistered_distinct"]), ("procedure_unregistered_total", p["unregistered_total"]),
                        ("condition_units", c["units_total"]), ("condition_raw", c["units_raw"]), ("condition_unregistered_distinct", c["unregistered_distinct"]), ("condition_unregistered_total", c["unregistered_total"])])


def _metrics(R):
    p, a, c = R["procedure"]["summary"], R["adverse"]["summary"], R["condition"]["summary"]
    ref_unreg = Counter()
    for T in R["adverse"]["timelines"]:
        for P in T["phases"]:
            for ln in P["lines"]:
                ref_unreg.update(ln["unregistered"])
    for x in R["adverse"]["emergency_signs"] + R["adverse"]["disclosures"]:
        ref_unreg.update(x["unregistered"])
    return OrderedDict([("adverse_kind_unregistered", sum(len(e["unregistered"]) for e in R["adverse"]["phrase_dictionary"])), ("reference_tables_unregistered_distinct", len(ref_unreg)), ("reference_tables_unregistered_total", sum(ref_unreg.values())),
                        ("safety_entries_by_status", a["safety_entries_by_status"]), ("memo_entries_by_status", a["memo_entries_by_status"]), ("safety_by_status", a["safety_by_status"]), ("units", a["units_total"]), ("ledger_events", a["ledger_events"]), ("raw_name_units", a["complications_raw_name"]),
                        ("ref_unresolved", p["reference_total"]["unresolved"]), ("market_unresolved", p["market_pricing"]["unresolved"]), ("unresolved_9", p["reference_total"]["unresolved"] + p["market_pricing"]["unresolved"]),
                        ("catalog_self", p["catalog_self_items"]), ("catalog_by_what_kind", p["catalog_by_what_kind"]), ("procedure_unregistered_distinct", p["unregistered_distinct"]), ("procedure_unregistered_total", p["unregistered_total"]),
                        ("condition_units", c["units_total"]), ("condition_raw", c["units_raw"]), ("condition_unregistered_distinct", c["unregistered_distinct"]), ("condition_unregistered_total", c["unregistered_total"]),
                        ("equipment_products", len(R["equipment"]["products"])), ("ingredient_what", len([1 for r in R["procedure"]["catalog"] if r.get("what_kind") == "ingredient"]))])


# ---------------------------------------------------------------------------
# 표
# ---------------------------------------------------------------------------
def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


def _locs(xs, n=6):
    xs = list(xs or [])
    return " · ".join(f"`{x}`" for x in xs[:n]) + (f" …(+{len(xs) - n})" if len(xs) > n else "") if xs else "—"


def kinds_md(R):
    a = R["adverse"]["summary"]
    m = R["v32"]["after"]
    o = []
    A = o.append
    A("#### 9.9 원장 문구 종류별 표 (V3.2-0 · §0 첫 규칙) — 종류마다 자기 테이블 · 부작용 단위에는 부작용 문구만")
    A("")
    tl = a["timeline_lines_by_status"]
    es = a["emergency_signs_by_status"]
    ds = a["disclosures_by_status"]
    ls = a["literature_by_status"]
    sb = a["safety_by_status"]
    cs = R["condition"]["summary"]
    A(md_table(["문구 종류", "원장 자리", "자리 수", "자기 테이블 · 행", "부작용과의 관계", "참조·연결 성공", "참조 없음 / 메모", "진짜 unlinked"], [
        ("부작용 이름", "complications.json name", a["complications_names"], f"부작용 단위 · 이름 유래 {a['complications_distinct_units']}", "붙임(단위 생성·연결)", f"exact {a['complications_by_status'].get('exact', 0)} · new {a['complications_by_status'].get('new', 0)}", f"raw_name {a['complications_raw_name']}", 0),
        ("부작용 문구", "safety.common/uncommon/serious/emergency/long_term/…(taxonomy·extracted·제품)", a["safety_occurrences"], f"문구 사전 {a['safety_entries']}(exact {a['safety_entries_by_status'].get('exact', 0)} · new {a['safety_entries_by_status'].get('new', 0)}) + 메모 {a['memo_entries']}", "붙임 · 없으면 새 사건 노드",
         f"exact {sb.get('exact', 0)} · new {sb.get('new', 0)}", f"메모 {sb.get('note', 0)} · 설명문 {sb.get('sentence', 0)}", a["adverse_unattached"]),
        ("시술 후 경과", "post-procedure-timeline phases[].normal/abnormal/caution/emergency", a["timeline_lines"], f"post_procedure_timeline {a['timelines']} · 단계 {a['timeline_phases']} · 줄 {a['timeline_lines']}", "줄이 참조(R34)", f"ref {tl.get('ref', 0)} · 부분 {tl.get('ref_partial', 0)}", f"없음 {tl.get('none', 0)} · 정상 메모 {tl.get('normal_memo', 0)}", "— (참조 테이블)"),
        ("응급 징후", "consent-checklist emergency_signs[]", a["emergency_sign_rows"], f"emergency_sign {a['emergency_signs']}", "참조(R35)", f"ref {es.get('ref', 0)} · 부분 {es.get('ref_partial', 0)}", f"없음 {es.get('none', 0)}", "— (참조 테이블)"),
        ("필수 고지", "consent-checklist mandatory_disclosures[]", a["disclosures"], f"clinical_rule(disclosure) {len({d['rule_id'] for d in R['adverse']['disclosures']})}", "참조(adverse_ref)", f"ref {ds.get('ref', 0)} · 부분 {ds.get('ref_partial', 0)}", f"없음 {ds.get('none', 0)}", "— (참조 테이블)"),
        ("금기(조건)", "consent·extracted·taxonomy contraindications · pre-procedure label", cs["occurrences"], f"person_condition 단위 {cs['units_total']}(사전 {cs['units_dict']} · raw {cs['units_raw']})", "엣지(R16·R18) · 부작용 참조 없음", f"사전 단위 문장 {cs['phrases_by_match'].get('exact', 0)}", f"raw {cs['phrases_by_match'].get('raw', 0)}", "— (조건 축)"),
        ("문헌·환자 설명", "literature adverse_effects statement·patient_*", a["literature"], f"evidence_statement(kind=adverse_effects) {a['literature']} · 번역은 부록", "참조(adverse_ref) · 단위 general_description", f"ref {ls.get('ref', 0)} · 부분 {ls.get('ref_partial', 0)}", f"없음 {ls.get('none', 0)}", "— (설명 부록)"),
    ]))
    A("")
    A("「unlinked」는 부작용 문구 종류에서만 센다 — 부작용 축은 v3.2 에서 「사전에 없으면 원장 핵심어로 새 사건 노드」이므로 그 값은 0 이다(검산). 다른 종류는 자기 테이블의 참조 성공/없음으로 센다.")
    A("")
    return "\n".join(o)


def before_after_md(R):
    b, a, p = R["v32"]["before"], R["v32"]["after"], R["v32"]["projection"]["R"]
    s = R["adverse"]["summary"]
    o = []
    A = o.append
    A("#### 9.10 규칙 적용 전후 (v3.1 → v3.2 규칙 · 참고: 씨앗 후보 승인 가정 — 적용 아님)")
    A("")
    A(md_table(["지표", "v3.1(erd-v3.1-tuples.json)", "v3.2 규칙(씨앗 미적용 · 장비 자동 등록 · 원장 사건 노드)", "참고: 부위·성분 씨앗 승인 가정"], [
        ("부작용 미등록 조각 distinct / 총", f"{b['adverse_unregistered_distinct']} / {b['adverse_unregistered_total']}(문구 전 종류)", f"부작용 문구 종류 {a['adverse_kind_unregistered']} · 참조 테이블(타임라인·응급·고지) {a['reference_tables_unregistered_distinct']} / {a['reference_tables_unregistered_total']}", f"{p['adverse_kind_unregistered']} · {p['reference_tables_unregistered_distinct']} / {p['reference_tables_unregistered_total']}"),
        ("문구 사전 항목", f"{b['phrase_entries']} · {_kv(b['phrase_entries_by_status'])}", f"부작용 문구만 {sum(a['safety_entries_by_status'].values())} · {_kv(a['safety_entries_by_status'])} · unlinked 0 + 메모 {_kv(a['memo_entries_by_status'])}", f"{_kv(p['safety_entries_by_status'])}"),
        ("문구 자리 status", _kv(b["phrase_occurrences_by_status"]), f"부작용 문구 {_kv(a['safety_by_status'])}", _kv(p["safety_by_status"])),
        ("부작용 단위 · raw_name", f"{b['units']} · raw {b['raw_name_units']}", f"{a['units']} · raw {a['raw_name_units']} · 원장 사건 노드 {a['ledger_events']}", f"{p['units']} · 노드 {p['ledger_events']}"),
        ("시술 미해결 ⑨(참조 + 시장가)", f"{b['unresolved_9']}({b['ref_unresolved']} + {b['market_unresolved']})", f"{a['unresolved_9']}({a['ref_unresolved']} + {a['market_unresolved']})", f"{p['unresolved_9']}({p['ref_unresolved']} + {p['market_unresolved']})"),
        ("항목 자신이 시술(catalog_item)", f"{b['catalog_self']} · {_kv(b['catalog_by_what_kind'])}", f"{a['catalog_self']} · {_kv(a['catalog_by_what_kind'])}", f"{p['catalog_self']} · {_kv(p['catalog_by_what_kind'])}"),
        ("시술 미등록 조각 distinct / 총", f"{b['procedure_unregistered_distinct']} / {b['procedure_unregistered_total']}", f"{a['procedure_unregistered_distinct']} / {a['procedure_unregistered_total']}", f"{p['procedure_unregistered_distinct']} / {p['procedure_unregistered_total']}"),
        ("조건 단위 · raw · 미등록 distinct / 총", f"{b['condition_units']} · {b['condition_raw']} · {b['condition_unregistered_distinct']} / {b['condition_unregistered_total']}", f"{a['condition_units']} · {a['condition_raw']} · {a['condition_unregistered_distinct']} / {a['condition_unregistered_total']}", f"{p['condition_units']} · {p['condition_raw']} · {p['condition_unregistered_distinct']} / {p['condition_unregistered_total']}"),
        ("장비 제품 자동 등록 · 성분 what", "—", f"{a['equipment_products']} · {a['ingredient_what']}", f"{p['equipment_products']} · {p['ingredient_what']}"),
    ]))
    A("")
    pa = R["v32"]["projection"]["added"]
    A(f"- 참고 실행이 더한 값(파일에 쓰지 않음): {_kv(pa)}. 변형 쌍은 목록 승인이라 참고 실행에도 넣지 않았다.")
    A(f"- 장비 승격(V3.2-5): 항목 자신 {b['catalog_self']} → {a['catalog_self']} — 제품으로 승격 {a['catalog_by_what_kind'].get('product', 0) - b['catalog_by_what_kind'].get('product', 0)} · 성분 what {a['catalog_by_what_kind'].get('ingredient', 0)}.")
    A(f"- unlinked 분리 전후(V3.2-7 · 코디 요청): v3.1 unlinked 자리 {b['phrase_occurrences_by_status'].get('unlinked', 0)}(전 종류) → 종류 분리 뒤 부작용 문구 종류 안 사전 밖 자리 {s['safety_by_status'].get('new', 0) + s['safety_by_status'].get('note', 0) + s['safety_by_status'].get('sentence', 0)} → 메모 {s['safety_by_status'].get('note', 0)} · 설명문 {s['safety_by_status'].get('sentence', 0)} 분리 → 새 노드 {s['safety_by_status'].get('new', 0)} → **unlinked 0**.")
    A("")
    rg = R["v32"]["regression_v31"]
    A(f"- 회귀: v3.2 분해 클래스에서 규칙을 전부 끄면 erd-v3.1-tuples.json 요약과 같다 — 시술 {rg['procedure']['keys']} 키 {rg['procedure']['same']} · 부작용 {rg['adverse']['keys']} 키 {rg['adverse']['same']} · 조건 {rg['condition']['keys']} 키 {rg['condition']['same']}.")
    A("")
    return "\n".join(o)


def tokenizer_md(R):
    o = []
    A = o.append
    V = R["v32"]
    A("#### 9.11 토큰화(V3.2-1) — 조사 · 용언 어미 · 문법 낱말 · 적중 · locator · 사라진 조각")
    A("")
    rows = V["tokenizer_words"]
    A(f"- 목록 {len(rows)}(조사 {sum(1 for r in rows if r['kind'] == 'particle')} · 어미 {sum(1 for r in rows if r['kind'] == 'ending')} · 문법 낱말 {sum(1 for r in rows if r['kind'] == 'word')}) · 적중 합 {sum(r['hits'] for r in rows)} · locator 없는 원소 {sum(1 for r in rows if not r['locators'])}.")
    A("")
    A(md_table(["원소", "종류", "적중(자리)", "locator(최대 4)"], [(r["word"], r["kind"], r["hits"], _locs(r["locators"], 4)) for r in rows]))
    A("")
    g = V["disappeared_by_tokenizer"]
    for ax, d in g.items():
        A(f"- **{ax}** v3.1 미등록 조각 중 토큰화로 사라진 것 distinct **{d['distinct']}**(결과별 {_kv(d['by_outcome'])} — span = 사전 값에 닿음 · modifier = 수식어 · grammar = 문법 낱말 · stem = 어간 조각으로 합쳐짐): " + ", ".join(d["examples"][:40]))
    A("")
    lg = Counter((x[1], x[2], x[3], x[4]) for x in R["tokenizer"]["log"])
    A("변환 표본(상위 60 · 원 토큰 → 결과 · 어간 · 뗀 접미): " + " · ".join(f"{t}→{k}:{v}+{s}×{n}" for (t, k, v, s), n in lg.most_common(60)))
    A("")
    return "\n".join(o)


def variants_md(R):
    o = []
    A = o.append
    V = R["v32"]
    gl = R["adverse"]["gloss_pairs"] + R.get("gloss_pairs_other", [])
    A("#### 9.12 표기 변형(V3.2-2) — 병기 괄호 · 자모 변형 쌍(목록 승인 · 적용 0)")
    A("")
    A(f"- (a) 병기 괄호 쌍 {len(gl)}(축별 {_kv(Counter(x['axis'] for x in gl))} · distinct {len({(x['before'], x['inner']) for x in gl})}) — 사전에 닿은 쪽 + 라틴 문자 쪽이면 라틴 쪽이 gloss(보존), 아니면 둘 다 그대로(쌍은 후보). 표본: " + " · ".join(f"{a}({b})" for a, b in sorted({(x['before'], x['inner']) for x in gl})[:60]))
    A(f"- (b) 자모 변형 쌍 **{len(V['variant_pairs'])}**(원장 전체 어휘 · 어간 기준 · 같은 자리 자모 하나 치환 · 한글 2자 이상·라틴 4자 이상 · 숫자·문법 낱말·수식어 제외) — 전부 status=proposed · applied=false. 한쪽이 사전 값 {sum(1 for p in V['variant_pairs'] if bool(p['a_dict']) != bool(p['b_dict']))} · 둘 다 사전 값 {sum(1 for p in V['variant_pairs'] if p['a_dict'] and p['b_dict'])} · 둘 다 사전 밖 {sum(1 for p in V['variant_pairs'] if not p['a_dict'] and not p['b_dict'])}. 승인되면 사전 동의어(dictionary_add) — 쌍 전부는 `erd-v3.2-seed-candidates.json` variant_pairs.")
    A("")
    A(md_table(["#", "a", "b", "a 사전", "b 사전", "a 횟수", "b 횟수", "locator(a · 최대 2 / b · 최대 2)"], [(i + 1, p["a"], p["b"], p["a_dict"] or "—", p["b_dict"] or "—", p["a_n"], p["b_n"], _locs(p["a_locators"], 2) + " / " + _locs(p["b_locators"], 2)) for i, p in enumerate(V["variant_pairs"][:50])]))
    A("")
    A("- (c) 조사 제거 뒤 재일치 = §9.11(어간이 사전 값이면 span).")
    A("")
    return "\n".join(o)


def nodes_md(R):
    o = []
    A = o.append
    ad = R["adverse"]
    s = ad["summary"]
    ps = R["procedure"]["summary"]
    A("#### 9.13 부작용 축 노드 원칙(V3.2-0 교체) — 원장 사건 노드 · ⑦ 후보 · exact/new 분포 · 시술 축과 대칭")
    A("")
    sb = s["safety_by_status"]
    A(f"- 원장 사건 노드(origin=ledger · status=unreviewed) **{s['ledger_events']}** — locator 없는 노드 {s['ledger_events_without_locator']} · 설명(원장 문맥) 없는 노드 {s['ledger_events_without_description']}. 이 노드를 쓰는 단위 {s['units_with_ledger_event']} / 단위 {s['units_total']}.")
    A(f"- 부작용 문구 {s['safety_occurrences']} 자리: exact **{sb.get('exact', 0)}** · new **{sb.get('new', 0)}** (그중 ⑦ 후보가 있는 노드를 가리키는 자리 {sum(1 for r in ad['phrase_rows'] if r['status'] == 'new' and any(norm(e) in {norm(d['new']) for d in ad['duplicate_pairs']} for e in next((x['ledger_events'] for x in ad['phrase_dictionary'] if x['id'] == r['phrase_id']), [])))}) · 메모 {sb.get('note', 0)} · 설명문 {sb.get('sentence', 0)} · 어느 노드에도 안 붙은 부작용 문구 **{s['adverse_unattached']}**. complications 이름 65: {_kv(s['complications_by_status'])} · raw_name {s['complications_raw_name']}.")
    A(f"- ⑦ duplicate_candidate(노드끼리 · 검토 S-2) 쌍 **{s['dup_pairs']}** = strong **{s['dup_pairs_strong']}**(기본 게이트) + weak {s['dup_pairs_weak']}(표시만) · 원장 노드 ↔ 원장 노드 {s['dup_pairs_node_node']} · 관련 노드 {s['dup_ledger_events']} · 규칙별 {_kv(s['dup_by_rule'])}. 점수·유사도 없음 · 접기는 fold_approve.")
    A(f"- 사전 사건 옆 미등록 토큰(side · 노드 후보 · 단위 칸 아님): 문구 항목 {sum(1 for e in ad['phrase_dictionary'] if e['parsed'].get('side'))} · distinct {len({x for e in ad['phrase_dictionary'] for x in e['parsed'].get('side', [])})}.")
    A(f"- 시술 축 대칭: 분류 항목 자신(catalog_item) v3.1 477 → v3.2 **{ps['catalog_self_items']}**(장비 승격 뒤) · 실버 6차(결정 뒤) 355 ↔ 부작용 원장 사건 노드 {s['ledger_events']} — 둘 다 「사전에 없으면 원장 이름이 그 자신의 노드」이고 ⑦ 로 접는다.")
    A("")
    A("원장 사건 노드 상위 50(locator 수 순 · 전부 JSON adverse.ledger_events):")
    A("")
    ln = sorted(ad["ledger_events"], key=lambda x: (-x["n_locators"], x["canonical"]))
    A(md_table(["#", "노드", "id", "자리 수", "⑦ 후보", "문맥(첫 자리 · 계열 · 빈도 등급)", "locator(최대 3)"], [(i + 1, n["canonical"], n["id"], n["n_locators"], ", ".join(n["dup_candidates"]) or "—", f"{n['contexts'][0].get('kind')} · {n['contexts'][0].get('modality')} · {n['contexts'][0].get('frequency_class') or n['contexts'][0].get('severity') or '—'} · 「{str(n['contexts'][0]['text'])[:40]}」", _locs(n["locators"], 3)) for i, n in enumerate(ln[:50])]))
    A("")
    A("⑦ 후보 쌍 상위 50(strong 먼저):")
    A("")
    A(md_table(["#", "노드", "상대(사전 · 원장 노드)", "상대 종류", "규칙", "등급", "자리 수"], [(i + 1, d["new"], d["existing"], d["existing_kind"], ", ".join(d["rules"]), d["grade"], d["n_locators"]) for i, d in enumerate(ad["duplicate_pairs"][:50])]))
    A("")
    A("메모·설명문(V3.2-7 · unlinked 로 세지 않음 · 원문·locator 보존) 전부:")
    A("")
    A(md_table(["#", "판정", "근거", "원문(표면형 첫째)", "자리 수"], [(i + 1, m["status"], _kv(m["why"]) if isinstance(m["why"], dict) else str(m["why"]), m["raw_variants"][0][:100], len(m["locators"])) for i, m in enumerate(ad["memo_phrases"])]))
    A("")
    return "\n".join(o)


def tables_md(R):
    o = []
    A = o.append
    ad = R["adverse"]
    s = ad["summary"]
    A("#### 9.14 post_procedure_timeline(V3.2-9) · emergency_sign · 고지 · 문헌 — 참조 실측")
    A("")
    A(f"- 타임라인 {s['timelines']} · 단계 {s['timeline_phases']} · 줄 {s['timeline_lines']} — 줄 상태 {_kv(s['timeline_lines_by_status'])} · 반응 등급별 " + " · ".join(f"{k}: {_kv(v)}" for k, v in s["timeline_lines_by_level_status"].items()) + f" · R34 timeline_refers {s['r34']} · R15 에 타임라인 참조가 붙은 엣지 {s['edges_with_timeline_refs']}.")
    A(f"- R33 has_timeline: " + " · ".join(f"{x['name']}→{(x['end'] or {}).get('kind')}" for x in R.get("r33", [])))
    A(f"- 응급 징후 자리 {s['emergency_sign_rows']} → emergency_sign {s['emergency_signs']} · {_kv(s['emergency_signs_by_status'])} · R35 {s['r35']} · R15 에 응급 참조가 붙은 엣지 {s['edges_with_sign_refs']}.")
    A(f"- 필수 고지 {s['disclosures']} · {_kv(s['disclosures_by_status'])} (clinical_rule.adverse_ref — 단위를 세우지 않는다).")
    A(f"- 문헌 adverse_effects {s['literature']} · {_kv(s['literature_by_status'])} · general_description 이 있는 단위 {s['units_with_general_description']}.")
    A("")
    A(md_table(["타임라인", "계열", "단계", "줄", "ref", "부분", "없음", "정상 메모"], [(T["name"], T["category"], len(T["phases"]), sum(len(P["lines"]) for P in T["phases"]), *[sum(1 for P in T["phases"] for l_ in P["lines"] if l_["ref_status"] == k) for k in ("ref", "ref_partial", "none", "normal_memo")]) for T in ad["timelines"]]))
    A("")
    A("참조 테이블에서 남은 미등록 조각 상위(타임라인): " + ", ".join(f"{k}×{v}" for k, v in s["unregistered_reference_tables"].items()))
    A("")
    return "\n".join(o)


def inherit_md(R):
    s = R["adverse"]["summary"]
    o = []
    A = o.append
    A("#### 9.15 R15 속성 상속(V3.2-8) — 항목/제품 엣지 → 계열 엣지 → 단위 일반값 (참조만)")
    A("")
    A(f"- 항목·제품 출발 R15 {s['inheritance_item_edges']} · 단위 general_management 있는 단위 {s['units_with_general_management']} · general_description {s['units_with_general_description']} · basis 없는 상속 값 **{s['inheritance_missing_basis']}** · 값이 복사된 상속 **{s['inheritance_copied_values']}**.")
    A("")
    A(md_table(["속성", "item", "family", "unit", "none"], [(a, *[d.get(k, 0) for k in ("item", "family", "unit", "none")]) for a, d in s["inheritance_by_basis"].items()]))
    A("")
    A(md_table(["사건(상위)", "항목 엣지", "severity f/n", "incidence f/n", "management f/u/n", "prevention f/n"], [(ev, d["item_edges"], f"{d['attrs']['severity'].get('family', 0)}/{d['attrs']['severity'].get('none', 0)}", f"{d['attrs']['incidence'].get('family', 0)}/{d['attrs']['incidence'].get('none', 0)}", f"{d['attrs']['management'].get('family', 0)}/{d['attrs']['management'].get('unit', 0)}/{d['attrs']['management'].get('none', 0)}", f"{d['attrs']['prevention'].get('family', 0)}/{d['attrs']['prevention'].get('none', 0)}") for ev, d in s["inheritance_by_event"].items()]))
    A("")
    return "\n".join(o)


def equipment_md(R):
    o = []
    A = o.append
    eq = R["equipment"]
    A("#### 9.16 장비 = 제품 자동 등록(V3.2-5) · 성분 what(V3.2-6)")
    A("")
    ex = Counter((x["excluded"] or "register").split(":")[0] for x in eq["items"])
    A(f"- 장비 계열·하위분류 항목 {len(eq['items'])} → 등록 {sum(1 for x in eq['items'] if x['register'])}(제품 {len(eq['products'])} · 같은 이름 합침) · 제외 {_kv({k: v for k, v in ex.items() if k != 'register'})}. license_status=미확인 · origin=taxonomy · status=unreviewed.")
    A("- 제외 항목: " + " · ".join(f"{x['name']}({x['excluded']})" for x in eq["items"] if not x["register"]))
    iw = [r for r in R["procedure"]["catalog"] if r.get("what_kind") == "ingredient"]
    A(f"- 성분 what(분류 항목): {len(iw)} — " + " · ".join(f"{r['name']}[{r['family']}]" for r in iw))
    A("")
    return "\n".join(o)


def seeds_md(R, full=False):
    o = []
    A = o.append
    S = R["v32"]["seeds"]
    A("#### 9.17 사전 씨앗 후보(V3.2-3/4/6) — 적용 0 · 승인 묶음 · 사전별")
    A("")
    A(md_table(["묶음", "사전", "닫힌 목록", "행", "proposed", "그 밖"], [(k, v["dictionary"], v.get("closed"), len(v["rows"]), sum(1 for r in v["rows"] if r.get("status") == "proposed"), _kv(Counter(r.get("status") for r in v["rows"] if r.get("status") != "proposed"))) for k, v in S.items()]))
    A("")
    lim = None if full else 50
    for k, v in S.items():
        A(f"##### {k} — {v['dictionary']} ({'닫힘' if v.get('closed') else '열림/선택'})")
        A("")
        if v.get("why_closed"):
            A(f"- 닫힌 까닭: {v['why_closed']}")
        if v.get("why_not_auto"):
            A(f"- 자동이 아닌 까닭: {v['why_not_auto']}")
        if v.get("note"):
            A(f"- {v['note']}")
        if v.get("toxin_units"):
            A(f"- {v['toxin_units']['note']} — 원장 토큰 {len(v['toxin_units']['tokens'])}: " + ", ".join(f"{a}×{b}" for a, b in v["toxin_units"]["tokens"][:20]))
        A("")
        rows = v["rows"][:lim] if lim else v["rows"]
        if k == "site":
            A(md_table(["값", "kind", "parent", "기존", "자리", "상태", "동의어 후보(자리)", "locator"], [(r["value"], r["kind"], r["parent"] or "—", "○" if r["existing"] else "", r["n"], r["status"], ", ".join(f"{x['value']}({x['n']})" for x in r["synonyms"]) or "—", _locs(r["locators"], 999 if full else 4)) for r in rows]))
        elif k == "product_abbrev":
            A(md_table(["조각/제품", "제품", "origin", "규칙", "자리", "상태", "locator"], [(r["fragment"], r["product"], r["product_origin"], r["rule"], r["n"], r["status"], _locs(r["locators"], 999 if full else 4)) for r in rows]))
        else:
            A(md_table(["값", "자리", "상태", "근거·추천", "자리 경로", "locator"], [(r["value"], r["n"], r.get("status", "—"), r.get("basis") or r.get("recommend") or r.get("site") or "—", _kv(r.get("paths")), _locs(r["locators"], 999 if full else 4)) for r in rows]))
        A("")
    return "\n".join(o)


def v32_md(R):
    return "\n".join([kinds_md(R), before_after_md(R), tokenizer_md(R), variants_md(R), nodes_md(R), tables_md(R), inherit_md(R), equipment_md(R), seeds_md(R)])


def seed_files(R, out_dir=HERE):
    S = R["v32"]["seeds"]
    j = OrderedDict([("erd_version", "v3.2"), ("status", "proposed — 사용자 승인 전(적용 0)"), ("note", "사전 단위로 승인한다. 부작용 사건과 장비 제품은 원장 칸이 종류를 선언하므로 자동 생성(승인 불필요 · ⑦ 로 접기) — 여기 있는 것은 닫힌 목록(부위·경과·물질·상대 부위)과 문맥 추정(성분 · 시술 조각)·줄임말 접두 후보."),
                     ("seeds", S), ("variant_pairs", R["v32"]["variant_pairs"]), ("gloss_pairs", R["adverse"]["gloss_pairs"] + R.get("gloss_pairs_other", [])),
                     ("auto_created", {"ledger_events": len(R["adverse"]["ledger_events"]), "equipment_products": len(R["equipment"]["products"]), "duplicate_pairs": R["adverse"]["duplicate_pairs"]})])
    json.dump(j, open(os.path.join(out_dir, "erd-v3.2-seed-candidates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# ERD v3.2 사전 씨앗 후보 묶음 — 사용자 승인용 (status=proposed · 적용 0)", "",
          "작성 2026-11-05 · 생성 `erd-v3.2-tuples.py` · 원장 = 브론즈 2판. 사전 단위로 승인한다(승인된 값은 결정 dictionary_add). 부작용 사건·장비 제품은 v3.2 원칙(원장이 쓴 말이 곧 씨앗)으로 자동 생성되어 여기서 승인할 것이 아니다 — ⑦ duplicate_candidate 로 접기만 고른다(§ 끝).", "",
          seeds_md(R, full=True), "", "## 자모 변형 쌍(V3.2-2b) 전부 — 목록 승인", "",
          md_table(["#", "a", "b", "a 사전", "b 사전", "a 횟수", "b 횟수", "locator a / b"], [(i + 1, p["a"], p["b"], p["a_dict"] or "—", p["b_dict"] or "—", p["a_n"], p["b_n"], _locs(p["a_locators"], 3) + " / " + _locs(p["b_locators"], 3)) for i, p in enumerate(R["v32"]["variant_pairs"])]), "",
          "## 자동 생성(승인 불필요) — 원장 사건 노드 ⑦ 후보 전부(노드끼리 · strong = 기본 게이트 · weak = 표시만)", "",
          md_table(["#", "노드", "상대", "상대 종류", "규칙", "등급", "자리"], [(i + 1, d["new"], d["existing"], d["existing_kind"], ", ".join(d["rules"]), d["grade"], d["n_locators"]) for i, d in enumerate(R["adverse"]["duplicate_pairs"])]), ""]
    open(os.path.join(out_dir, "erd-v3.2-seed-candidates.md"), "w", encoding="utf-8").write("\n".join(md))


def slim(R):
    X = OrderedDict((k, v) for k, v in R.items() if k != "_vocab")
    X["tokenizer"] = {"hits": R["tokenizer"]["hits"], "locators": R["tokenizer"]["locators"], "log_counts": [list(k) + [n] for k, n in Counter(tuple(x) for x in R["tokenizer"]["log"]).most_common()]}
    return X


def load_all32():
    dic = None
    p = os.path.join(HERE, "erd-v3.2-dictionaries.json")
    dic = json.load(open(p if os.path.exists(p) else os.path.join(HERE, "erd-v3.1-dictionaries.json"), encoding="utf-8"))
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    e = os.path.join(HERE, "erd-v3.2.json")
    erd = json.load(open(e if os.path.exists(e) else os.path.join(HERE, "erd-v3.1.json"), encoding="utf-8"))
    v31 = json.load(open(os.path.join(HERE, "erd-v3.1-tuples.json"), encoding="utf-8"))
    return dic, erd["tuple_rules"], erd["resolve_rules"], L, v31


def main():
    dic, rules, rrules, L, v31 = load_all32()
    bc = bronze_check(LEDGER)
    assert bc["hashes_file"] and not bc["mismatch"], f"브론즈 2판 해시 불일치 {bc}"
    R = run_everything(dic, rules, L, rrules, v31)
    print(v32_md(R))
    json.dump(slim(R), open(os.path.join(HERE, "erd-v3.2-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    seed_files(R)
    print("\n→ erd-v3.2-tuples.json · erd-v3.2-seed-candidates.json/.md")


if __name__ == "__main__":
    main()
