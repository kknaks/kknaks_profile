# -*- coding: utf-8 -*-
"""ERD v3.2 분해 — 참조 구현 `erd-v3.2-tuples.py` 의 분해·실측 부분(V3.2-0~9)을 lib 클래스(decompose · adverse31) 위로 옮겼다.
같은 입력(사전 · tuple_rules · resolve_rules · 원장)에 같은 단위 · 같은 id · 같은 등록 순서 · 같은 요약(check ③ 이 erd-v3.2-tuples.json 과 대조).

V3.2-0 문구 종류 분류(부작용 문구만 단위 · 타임라인/응급/고지/문헌은 refer) · V3.2-0 노드 원칙(토막 · 사전 사건 exact · side · 핵심어 새 노드)
V3.2-1 토큰화(조사·어미·문법 낱말 → grammar 보존) · V3.2-2 병기 괄호(gloss) · V3.2-5 장비 → 제품(origin=taxonomy) · V3.2-6 성분 what
V3.2-7 메모·설명문 판정 · V3.2-8 R15 상속(item → family → unit · basis · 참조) · V3.2-9 타임라인 · 응급 징후 · ⑦ duplicate_candidate(노드끼리 · strong/weak)

실행 중 규칙은 모듈 CUR(참조 구현과 같은 자리)에 둔다 — setup() 이 채우고 run_v32() 가 돈다. 빌드는 한 프로세스에서 순서대로 돌아 결정론이다.
"""
import copy
import os
import re
import unicodedata
from collections import Counter, OrderedDict, defaultdict

from . import decompose as DCMP
from .adverse31 import AdverseUnits31, ConditionTuples, COND_PAREN, COND_SPLIT, COND_STRIP, adverse_phrases31, condition_occurrences, _from_end, run_condition
from .decompose import ADV_MEMBER_SPLIT, ADV_PAREN, ADV_STRIP, SEP_RE, ProcedureTuples, Resolver, locator, run_procedure, tids_of
from .util import dedupe as _dedupe, mkid, norm

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
    for kind, text, src in adverse_phrases31(L):
        out.append(("adverse", kind, src["file"], src["path"], src["locator"], text, src.get("modality")))
    for f, p, rec, x, code, lvl in condition_occurrences(L):
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
class AdverseUnits32(AdverseUnits31):
    def __init__(self, ids, rules):
        super().__init__(ids, rules)
        self.gloss_sink = []
        self.mode = None          # None | create | refer (V3.2-0)
        self.ctx = None
        self.ledger = OrderedDict()
        self.base_event_surface = dict(ids.event_surface)
        self.fallback = {norm(w) for w in (CUR.get("fallback_core") or [])}
        self.excluded_hits = OrderedDict()   # 실버 결정 exclude(dictionary_value · 원장 사건 노드 = 부작용 아님) — locator → 뺀 핵심어
        self.fold_hits = OrderedDict()       # 실버 결정 fold_approve(사전 값 쌍) — 원장 노드 핵심어 → [(locator, 접힌 곳)]

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
        # 실버 결정(V3.2-0 · 원장 사건 노드): exclude(부작용 아님) → 노드를 세우지 않는다 · fold_approve(사전 값 쌍) → 접힌 곳(기존 사건 또는 다른 노드)
        if key in (CUR.get("not_adverse") or {}):
            if loc is not None:
                self.excluded_hits.setdefault(loc, [])
                if core not in self.excluded_hits[loc]:
                    self.excluded_hits[loc].append(core)
            return None, "excluded"
        folds = CUR.get("node_folds") or {}
        if key in folds:
            seen, tgt = {key}, folds[key]
            while norm(tgt) in folds and norm(tgt) not in seen:
                seen.add(norm(tgt))
                tgt = folds[norm(tgt)]
            if loc is not None:
                self.fold_hits.setdefault(core, [])
                if (loc, tgt) not in self.fold_hits[core]:
                    self.fold_hits[core].append((loc, tgt))
            if norm(tgt) in self.base_event_surface:
                return self.base_event_surface[norm(tgt)], "dictionary"
            core, key = tgt, norm(tgt)
        if key in self.ledger:
            canon, origin = self.ledger[key]["canonical"], "ledger"
        elif self.mode == "create":
            canon, origin = core, "ledger"
            eid = mkid("DIC", f"adverse_event_type|{core}")
            self.ledger[key] = {"canonical": core, "id": eid, "locators": [], "contexts": [], "core_tokens": core.split()}
            self.ids.event[key] = {"id": eid, "label": core} if CUR.get("is33") else {"id": eid, "label": core, "category": None}   # v3.3(V3.3-E): category 없음
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
                    if canon is None and origin == "excluded":
                        m.setdefault("explanation", []).extend(us)
                        m.setdefault("excluded_core", []).append(core)
                        continue
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
        parens = ADV_PAREN.findall(text)
        outer = ADV_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part:
                    continue
                toks = [t.strip(ADV_STRIP) for t in part.split()]
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
            groups = _apply_gloss(groups, text, ADV_PAREN, loc, self.gloss_sink, "adverse")
        return groups

    @staticmethod
    def _classes(groups):
        out = AdverseUnits31._classes(groups)
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


class V32Resolver(Resolver):
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
            for piece in SEP_RE.split(g):
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


class ProcedureTuples32(ProcedureTuples):
    """v3.1 위에 V3.2-1/2(분해기 V32Resolver) · V3.2-6(성분 what)."""

    def __init__(self, lex, rules, ids, L, scoped=None):
        super().__init__(lex, rules, ids, L, scoped)
        self.R = V32Resolver(lex, rules, ids)
        self.ingredient_what = []

    def _annotate(self, groups, base):
        base = super()._annotate(groups, base)
        mems = [m for g in groups for m in g["members"]]
        base["grammar_tokens"] = [x["text"] for m in mems for x in m.get("grammar", [])]
        base["gloss"] = [x for m in mems for x in m.get("gloss", [])]
        base["ingredient_fragments"] = [s["canonical"] for m in mems for s in m.get("ingredients", [])] or list((base.get("fragments") or {}).get("ingredients") or [])   # 실버: primary 가 있는 라벨의 성분 조각(assemble22 가 fragments.ingredients 로 남긴 것) 보존
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
class ConditionTuples32(ConditionTuples):
    def split(self, text, loc=None):
        flags = CUR["flags"] or FLAGS_OFF
        if not flags["tokenize"] and not flags["gloss"]:
            return super().split(text, loc)
        tk = CUR["tok"] if flags["tokenize"] else None
        known = lambda s: norm(s) in self.surface or norm(s) in self.markers  # noqa
        parens = COND_PAREN.findall(text)
        outer = COND_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in COND_SPLIT.split(g):
                toks = [t.strip(COND_STRIP) for t in part.split()]
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
            groups = _apply_gloss(groups, text, COND_PAREN, loc, CUR["gloss_sink"], "condition")
        return groups


# ---------------------------------------------------------------------------
# V3.2-7 부작용 문구 종류 판정(메모 · 설명문) — 바탕 분해(사전 그대로)로 판정한다
# ---------------------------------------------------------------------------
def _outer_tokens(text):
    return raw_tokens(ADV_PAREN.sub(" ", str(text)))


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


def _analyzer_prepass(L):
    """v3.3: 부작용 축에서 분석기가 보게 될 문자열 전부를 미리 캐시에 채운다(이름 · 부작용 문구 · 타임라인 줄 · 응급 징후 · 고지 · 문헌 statement·patient_ko)."""
    from .adverse33 import analyzer_texts
    texts = []
    for cat in L["complications.json"]["categories"]:
        for c in cat["complications"]:
            texts.append(c["name"])
    for kind, text, src in adverse_phrases31(L):
        texts.append(text)
    for tl in L["post-procedure-timeline.json"]["timelines"]:
        for ph in tl["phases"]:
            for lvl in ("normal", "abnormal", "caution", "emergency"):
                texts += list(ph.get(lvl) or [])
    for cat in L["consent-checklist.json"]["categories"]:
        texts += list(cat.get("emergency_signs") or []) + list(cat.get("mandatory_disclosures") or [])
    for code, cat in L["literature-evidence.json"]["categories"].items():
        for ae in cat.get("adverse_effects") or []:
            texts.append(ae["statement"])
            if ae.get("patient_ko"):
                texts.append(ae["patient_ko"])
    subs = []
    for t in texts:
        subs += analyzer_texts(t)
    return CUR["analyzer"].ensure(subs)


def run_adverse32(ids, rules, L, v31tup=None):
    rules = rules["adverse"] if "adverse" in rules else rules
    kr = CUR["kinds"]
    tk = CUR["tok"]
    if CUR.get("is33") and CUR.get("analyzer") is not None:
        from .adverse33 import AdverseUnits33
        CUR["analyzer_prefilled"] = _analyzer_prepass(L)
        AT = AdverseUnits33(ids, rules)
    else:
        AT = AdverseUnits32(ids, rules)
    base_surface = dict(ids.event_surface)
    comp_attrs = _comp_attr_locs(L)
    # ---- ① complications 65 이름 → 단위(create · raw_name 없음 — 핵심어 노드)
    comp_rows, name_edges = [], OrderedDict()
    for ci, cat in enumerate(L["complications.json"]["categories"]):
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            src = {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc, "rec": (ci, i)}
            AT.mode, AT.ctx = None, None
            ev0 = AT.evaluate(c["name"], dict(src))
            AT.mode, AT.ctx = "create", {"kind": "complication_name", "modality": cat["id"], "severity": c.get("severity"), "frequency_class": None}
            ev = AT.evaluate(c["name"], dict(src))
            ids_ = []
            for uc in ev["unit_candidates"]:
                ids_.append(AT.register_unit(uc, src))
            excluded_cores = list(AT.excluded_hits.get(loc, []))
            if not ids_ and not excluded_cores:
                tid = AT.register_raw(c["name"], [], ev["unregistered"], {"extra_sites": ev["extra_sites"], "extra_courses": ev["extra_courses"], "extra_qualifiers": ev["extra_qualifiers"]}, src, loc)
                ids_ = [tid]
            # 결정(exclude · 부작용 아님)이 이 이름의 사건 노드를 전부 뺐으면 단위 없음(note · 메모)
            st = "note" if (not ids_ and excluded_cores) else ("new" if any(sp[0] == "event" and norm(sp[1]) in AT.ledger for sp in ev["spans"]) else ("exact" if ev["event_fragments"] else "raw"))
            for cc in ev["candidates"]:   # 실버: 등록 뒤 단위 id(결정 · R15 경과 지도가 읽는다)
                cc["unit_id"] = AT.units.get((cc["event_id"], cc["site_id"], cc["qualifier_id"]))
                cc["exists"] = cc["unit_id"] is not None
            comp_rows.append(dict(ev, text=c["name"], locator=loc, modality=cat["id"], record=i, severity=c.get("severity"), unit_ids=_dedupe(ids_), status32=st, base_unregistered=ev0["unregistered"],
                                  rec=(ci, i), event_kind=("ledger" if st == "new" else "dict") if ids_ else None, excluded_cores=excluded_cores))
            for uid in _dedupe(ids_):
                k = (("modality", cat["id"]), uid)
                e = name_edges.setdefault(k, {"from": ("modality", cat["id"]), "unit": uid, "courses": [], "names": [], "attrs": {}})
                e["courses"] = _dedupe(e["courses"] + [co for cc in ev["candidates"] if AT.units.get((cc["event_id"], cc["site_id"], cc["qualifier_id"])) == uid for co in cc["courses"]])
                e["names"].append(loc)
                for a, al in comp_attrs[f"{cat['id']}/{i}"].items():
                    e["attrs"].setdefault(a, []).append(al)
    # ---- ② 부작용 문구(safety.*) → 판정(V3.2-7) → exact/new 는 문구 사전 · 단위 · R15
    entries, memo = OrderedDict(), OrderedDict()
    occ = adverse_phrases31(L)
    safety = [(k, t, s) for k, t, s in occ if k == "safety_phrase"]
    phrase_rows = []
    for kind, text, src in safety:
        src = dict(src, kind=kind)
        AT.mode, AT.ctx = None, None
        g0 = AT.split(text, None)
        verdict, why = judge_phrase(text, g0, kr, tk)
        ev = ev_an = None
        if verdict not in ("note", "sentence"):
            ctx = src.get("context") or {}
            AT.mode, AT.ctx = "create", {"kind": "safety_phrase", "modality": src.get("modality"), "frequency_class": ctx.get("frequency_class"), "item": ctx.get("item_name"), "product": ctx.get("product_name")}
            ev = AT.evaluate(text, src)
            if not ev["candidates"] and AT.excluded_hits.get(src["locator"]):
                # 실버 결정 exclude(원장 사건 노드 = 부작용 아님)가 이 문구의 사건을 전부 뺐다 → 메모(note)
                verdict, why, ev = "note", {"note_words": [], "excluded_node": list(AT.excluded_hits[src["locator"]])}, None
                AT.mode, AT.ctx = None, None
            elif not ev["candidates"] and hasattr(AT, "gone_kinds") and AT.gone_kinds(src["locator"]):
                # v3.3(V3.3-B): 분석기가 토막을 문장꼴(b)·애매·서술로 보아 사건이 하나도 남지 않았다 → 노드 없이 status=sentence(사람 판정 · 게이트 6) · 원문·토막 기록 보존
                gk = AT.gone_kinds(src["locator"])
                verdict, why = "sentence", {"why": ["analyzer"], "analyzer_kinds": gk, "analyzer": "sentence_b" if any(k == "T2b" for k in gk) else ("ambiguous" if any(k in ("ANOM", "T1-pred", "T1-none", "T1-partial") for k in gk) else "predicate")}
                ev_an = ev
                ev = None
                AT.mode, AT.ctx = None, None
        if verdict in ("note", "sentence"):
            ev0 = ev_an if (ev is None and verdict == "sentence" and "analyzer" in why) else AT.evaluate(text, src)
            key = ev0["normalized"] or norm(text)
            e = memo.setdefault(key, OrderedDict([("id", mkid("PHR", key)), ("normalized", key), ("status", verdict), ("raw_variants", []), ("locators", []), ("contexts", []), ("why", why), ("parsed", ev0["parsed"]), ("events_seen", ev0["event_fragments"]), ("unregistered", ev0["unregistered"]), ("status_mismatch", 0)]))
            if e["status"] != verdict:
                e["status_mismatch"] += 1
            if text not in e["raw_variants"]:
                e["raw_variants"].append(text)
            e["locators"].append(src["locator"])
            e["contexts"].append({"locator": src["locator"], "from": _from_end(src), "modality": src.get("modality"), "frequency_class": (src.get("context") or {}).get("frequency_class"),
                                  "kind": kind, "file": src["file"], "path": src["path"], "rec": src.get("rec"), "item": src.get("item"), "product": src.get("product"), "context": src.get("context") or {}, "text": text})
            phrase_rows.append({"locator": src["locator"], "text": text, "status": verdict, "phrase_id": e["id"], "from": _from_end(src), "file": src["file"], "path": src["path"], "rec": src.get("rec")})
            continue
        ctx = src.get("context") or {}
        key = ev["normalized"] or norm(text)
        status = "new" if any(sp[0] == "event" and norm(sp[1]) in AT.ledger for sp in ev["spans"]) else "exact"
        e = entries.get(key)
        if e is None:
            e = OrderedDict([("id", mkid("PHR", key)), ("normalized", key), ("raw_variants", []), ("kinds", ["safety_phrase"]), ("langs", ["ko"]), ("locators", []), ("modality_codes", []), ("contexts", []), ("status", status),
                             ("units", []), ("created_units", []), ("candidates", ev["candidates"]), ("parsed", dict(ev["parsed"], events=ev["event_fragments"], sites=_dedupe(c["site"] for c in ev["candidates"] if c["site"]), relative_sites=ev["relative_sites"], courses=ev["courses"], qualifiers=ev["qualifiers"], phrase_shape=ev["phrase_shape"])),
                             ("unregistered", ev["unregistered"]), ("extra_sites", ev["extra_sites"]), ("extra_courses", ev["extra_courses"]), ("extra_qualifiers", ev["extra_qualifiers"]), ("fragment_classes", ev["fragment_classes"]), ("spans", ev["spans"]),
                             ("_uc", ev["unit_candidates"]), ("status_mismatch", 0), ("ledger_events", _dedupe(s[1] for s in ev["spans"] if s[0] == "event" and norm(s[1]) in AT.ledger)),
                             ("reasons", []), ("translations", []), ("citations", []), ("accuracy", [])])
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
        e["contexts"].append({"locator": src["locator"], "kind": kind, "from": _from_end(src), "modality": src.get("modality"), "frequency_class": ctx.get("frequency_class"),
                              "file": src["file"], "path": src["path"], "rec": src.get("rec"), "item": src.get("item"), "product": src.get("product"), "context": ctx, "text": text})
        phrase_rows.append({"locator": src["locator"], "text": text, "status": status, "phrase_id": e["id"], "from": _from_end(src), "file": src["file"], "path": src["path"], "rec": src.get("rec")})
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
    erd_tl = {(src["path"], tuple(src["rec"])): src["locator"] for kind_, _, src in DCMP.adverse_phrases(L) if kind_ == "symptom_phrase"}   # 옛 판(v3·v3.1) ERD 꼴 줄 locator(결정 target)
    for ti, tl in enumerate(L["post-procedure-timeline.json"]["timelines"]):
        code = tl["category"].split("-")[0]
        T = {"id": mkid("TML", tl["id"]), "ledger_id": tl["id"], "name": tl["name"], "category": tl["category"], "modality": code, "locator": locator("post-procedure-timeline.json", "timelines[].name", str(ti)), "phases": []}
        for pi, ph in enumerate(tl["phases"]):
            P = {"order": pi, "period": ph["period"], "label": ph["label"], "locator": locator("post-procedure-timeline.json", "timelines[].phases[].period", f"{ti}/{pi}"), "lines": []}
            for lvl in ("normal", "abnormal", "caution", "emergency"):
                for li, x in enumerate(ph.get(lvl) or []):
                    loc = locator("post-procedure-timeline.json", f"timelines[].phases[].{lvl}[]", f"{ti}/{pi}/{li}")
                    r = refer(x, {"locator": loc, "origin": f"timeline.{lvl}"})
                    if lvl == "normal" and not r["adverse_ref"]:
                        r["ref_status"] = "normal_memo"
                    P["lines"].append(dict(r, reaction_level=lvl, text=x, locator=loc, rec=(ti, pi, li), path=f"timelines[].phases[].{lvl}[]", erd_locator=erd_tl.get((f"timelines[].phases[].{lvl}[]", (ti, pi, li)))))
            T["phases"].append(P)
        timelines.append(T)
    signs = OrderedDict()
    for ci_, cat in enumerate(L["consent-checklist.json"]["categories"]):
        for i, x in enumerate(cat.get("emergency_signs") or []):
            loc = locator("consent-checklist.json", "categories[].emergency_signs[]", f"{cat['id']}/{i}")
            k = norm(x)
            s = signs.get(k)
            if s is None:
                s = dict(refer(x, {"locator": loc, "origin": "consent.emergency"}), id=mkid("SGN", k), text=x, modality_codes=[], locators=[], recs=[])
                signs[k] = s
            s["modality_codes"].append(cat["id"])
            s["locators"].append(loc)
            s["recs"].append((ci_, i))
    disclosures = []
    for ci_, cat in enumerate(L["consent-checklist.json"]["categories"]):
        for i, x in enumerate(cat.get("mandatory_disclosures") or []):
            loc = locator("consent-checklist.json", "categories[].mandatory_disclosures[]", f"{cat['id']}/{i}")
            disclosures.append(dict(refer(x, {"locator": loc, "origin": "consent.disclosure"}), rule_id=mkid("RUL", f"disclosure|{x}"), text=x, modality=cat["id"], locator=loc, rec=(ci_, i)))
    literature = []
    for code, cat in L["literature-evidence.json"]["categories"].items():
        for i, ae in enumerate(cat.get("adverse_effects") or []):
            loc = locator("literature-evidence.json", "categories.{code}.adverse_effects[].statement", f"{code}/{i}")
            r1 = refer(ae["statement"], {"locator": loc, "origin": "literature"})
            r2 = refer(ae["patient_ko"], {"locator": loc.replace(".statement@", ".patient_ko@"), "origin": "literature.patient_ko"}) if ae.get("patient_ko") else {"adverse_ref": [], "ref_status": "none"}
            refs = _dedupe(r1["adverse_ref"] + r2["adverse_ref"])
            literature.append({"id": mkid("EVS", f"{code}|adverse_effects|{ae['statement']}"), "modality": code, "locator": loc, "statement": ae["statement"], "patient_ko": ae.get("patient_ko"), "adverse_ref": refs,
                               "ref_status": "ref" if refs and "ref" in (r1["ref_status"], r2["ref_status"]) else ("ref_partial" if refs else "none"), "statement_ref": r1["ref_status"], "patient_ko_ref": r2["ref_status"],
                               "translations": [{"lang": lg, "locator": loc.replace(".statement@", f".patient_{lg}@")} for lg in ("en", "zh", "ja") if ae.get(f"patient_{lg}")],
                               "rec": (code, i), "parsed": r1.get("parsed"), "patient_ko_parsed": r2.get("parsed")})
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
    analyzer_stats = None
    if hasattr(AT, "seglog"):
        analyzer_stats = OrderedDict([("segments", len(AT.seglog)), ("segment_kinds", dict(Counter(r["kind"] for r in AT.seglog))), ("rules", dict(Counter(x for r in AT.seglog for x in r["rules"]))),
                                      ("r1_new", dict(AT.r1_new)), ("r2_struct_side", dict(AT.r2_struct)), ("n1_names", len(AT.n1_names)), ("solo_strict_zero_nodes", sum(1 for k in AT.ledger if AT.solo_strict.get(k, 0) == 0)),
                                      ("paren_kinds", dict(Counter(x["kind"] for x in AT.t3_parens))), ("prefilled", CUR.get("analyzer_prefilled"))])
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
    if analyzer_stats is not None:
        summary["_analyzer"] = analyzer_stats   # v3.3 — `_` 접두: ③ ERD 실측 대조(분석기 없는 목록 규칙)의 요약 키 밖
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("phrase_dictionary", list(entries.values())), ("memo_phrases", list(memo.values())), ("phrase_rows", phrase_rows),
                        ("ledger_events", ledger_nodes), ("duplicate_pairs", dup), ("timelines", timelines), ("emergency_signs", list(signs.values())), ("disclosures", disclosures), ("literature", literature),
                        ("edges", [dict(e, from_=list(e["from"]), **{"from": list(e["from"])}) for e in all_edges.values()]), ("r34", r34), ("r35", r35), ("gloss_pairs", AT.gloss_sink),
                        # 실버(lib) 부록 — 결정·관계·provenance 가 읽는다(요약 대조 밖)
                        ("AT", AT), ("phrase_occurrences", phrase_rows), ("fold_hits", AT.fold_hits), ("excluded_hits", AT.excluded_hits), ("base_surface", base_surface)])


# ---------------------------------------------------------------------------
# V3.2-5 장비 항목 → 제품(origin=taxonomy) — 자동 등록(열린 사전 · 원장 칸이 종류를 선언)
# ---------------------------------------------------------------------------
def equipment_items(L, dic_json, er):
    D = {d["name"]: d for d in dic_json["dictionaries"]}
    known = {}
    for dn in ("modality", "modality_subcategory_label", "product_name", "technique"):
        for e in D[dn]["entries"]:
            if e.get("origin") == "taxonomy":
                continue   # 실버: 장비 제품에 동의어를 단 결정(origin=taxonomy)은 「이미 사전 값」이 아니다 — 자동 등록이 그 항목에 합친다
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
    seen = {norm(e["canonical"]): e for e in pn["entries"] if e.get("origin") == "taxonomy"}   # 실버: 결정이 미리 세운 장비 항목(동의어 결정) — 같은 이름이면 합친다
    pre = set(seen)
    for it in items:
        if not it["register"]:
            continue
        k = norm(it["name"])
        if k in seen:
            e = seen[k]
            if k in pre and not any(s_.get("locator") for s_ in e.get("sources", [])):
                e["code"] = it["family"]   # 결정이 세운 항목의 첫 원장 자리 — 계열은 원장 항목에서
            elif it["family"] not in str(e["code"]).split("|"):
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
def rule_data(erd):
    """ERD v3.2 json 의 규칙 데이터(resolve_rules.tokenize · tuple_rules.phrase_kinds · tuple_rules.equipment) — 참조 구현 rule_data 와 같은 값."""
    return erd["resolve_rules"]["tokenize"], erd["tuple_rules"]["phrase_kinds"], erd["tuple_rules"]["equipment"]


def base_dictionary(dic_json):
    """v3.2 사전 파일에 실린 파생 항목(origin ledger · taxonomy)을 뺀 ERD 사전 — 분해의 바탕(참조 구현 base_dictionary 와 같다)."""
    dj = copy.deepcopy(dic_json)
    for d in dj["dictionaries"]:
        d["entries"] = [e for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
    dj["dictionaries"] = [d for d in dj["dictionaries"] if d["name"] != "phrase_dictionary"]
    return dj


def setup(L, erd, flags=None, node_folds=None, not_adverse=None, analyzer=None):
    """실행 중 규칙(CUR) — 원장 전체 어휘 · 토큰화기 · 문구 종류 규칙 · 장비 규칙. 실버 결정(원장 사건 노드 접기 · 부작용 아님)은 node_folds · not_adverse.
    v3.3: analyzer(lib.analyzer.Analyzer · 사전 값 등록은 run_v32 가) — None 이면 분석기 없는 목록 규칙(ERD 실측 조건 · check ③)."""
    flags = dict(FLAGS_V32 if flags is None else flags)
    tokr, kinds, equip = rule_data(erd)
    texts = ledger_texts(L)
    vocab, vlocs = build_vocab(texts)
    tok = Tokenizer(tokr, vocab)
    CUR.clear()
    CUR.update(texts=texts, tok=tok, flags=flags, ingredient={}, gloss_sink=[], kinds=kinds, fallback_core=kinds["fallback_core"], vocab=vocab, equip=equip,
               adv_stop=erd["tuple_rules"]["adverse"]["adverse_stopwords"]["words"], node_folds=dict(node_folds or {}), not_adverse=dict(not_adverse or {}),
               is33=erd.get("erd_version") == "v3.3", analyzer=analyzer if erd.get("erd_version") == "v3.3" else None, analyzer_values=set())
    return CUR


def analyzer_surfaces(dic_json, skip=("phrase_dictionary",)):
    """T0(V3.3-B) — 사용자 단어로 등록할 사전 표면형 전부: 정준값 + 동의어(phrase_dictionary 제외 · origin=ledger 노드 제외 · 글자 없는 값 제외) — dryrun3 kiwi_t0.values_of 와 같다."""
    out = OrderedDict()
    for d in dic_json["dictionaries"]:
        if d["name"] in skip:
            continue
        for e in d["entries"]:
            if e.get("origin") == "ledger":
                continue
            vs = [e.get("canonical")] + [s.get("value") if isinstance(s, dict) else s for s in (e.get("synonyms") or [])]
            for v in vs:
                if v is None:
                    continue
                v = str(v).strip()
                if not v or not re.search(r"[가-힣A-Za-z]", v):
                    continue
                out.setdefault(v, None)
    return list(out)


def run_v32(dic_json, erd, L, scoped_decisions=None, bronze_version=2, flags=None, node_folds=None, not_adverse=None, equipment=True, analyzer=None):
    """참조 구현 run_all32 와 같은 순서 — 장비 제품 자동 등록 → 시술(토큰화 · 병기 · 성분 what) → 부작용(V3.2-0/7/8/9) → 조건(토큰화).
    dic_json = 분해의 바탕 사전(파생 항목 없음 · 결정 ① 적용 뒤일 수 있다). 반환 (P, A, C, extra).
    v3.3: analyzer 가 있으면 부작용 핵심어 토큰화를 분석기로(AdverseUnits33 · 사전 값 전부를 사용자 단어로 등록) · 없으면 목록 규칙(ERD 실측 조건)."""
    setup(L, erd, flags, node_folds, not_adverse, analyzer)
    flags = CUR["flags"]
    rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    Dn = {d["name"]: d for d in dic_json["dictionaries"]}
    ing = {}
    for e in Dn[INGREDIENT_DICT]["entries"]:
        ing[norm(e["canonical"])] = e
        for s_ in e.get("synonyms", []):
            ing[norm(s_["value"])] = e
    CUR["ingredient"] = ing
    eq_items = equipment_items(L, dic_json, CUR["equip"])
    dj, eq_products = (add_equipment_products(dic_json, eq_items) if (equipment and flags["phrase_kinds"]) else (dic_json, []))
    if CUR.get("analyzer") is not None:
        vals = analyzer_surfaces(dj)
        CUR["analyzer"].register(vals)
        CUR["analyzer_values"] = {norm(v) for v in vals}
    P = run_procedure(dj, rrules, L, scoped_decisions, prev_tuples=None, bronze_version=bronze_version, pt_cls=ProcedureTuples32)
    A = run_adverse32(P["ids"], rules, L) if flags["phrase_kinds"] else None
    C = run_condition(dj, rules["condition"], L, ct_cls=ConditionTuples32)
    tok = CUR["tok"]
    extra = OrderedDict([("dic", dj), ("equipment", {"items": eq_items, "products": eq_products}), ("tokenizer", {"hits": dict(tok.hits), "locators": {k: v for k, v in tok.hit_locs.items()}, "log": tok.log}),
                         ("gloss_pairs_other", list(CUR["gloss_sink"])), ("vocab_size", len(CUR["vocab"])), ("flags", flags)])
    if A is not None:
        extra["r33"] = r33_rows(P, A)
    if CUR.get("analyzer") is not None:
        extra["analyzer"] = {"registered": len(CUR["analyzer"].registered), "dict_hash": CUR["analyzer"].dict_hash, "kiwi_version": CUR["analyzer"].version}
    return P, A, C, extra


def r33_rows(P, A):
    """R33 has_timeline — 타임라인 이름 참조 행(post-procedure-timeline.timelines[].name)이 튜플로 풀리면 그 튜플 · 아니면 category 계열(참조 구현 r33_rows 와 같다)."""
    rows = P["ref_rows"].get("post-procedure-timeline.timelines[].name (10)", [])
    by = {(str(r["label"]), r.get("hint")): r for r in rows}
    out = []
    for T in A.get("timelines", []):
        r = by.get((T["name"], T["category"].split("-")[0])) or next((x for x in rows if str(x["label"]) == T["name"]), None)
        end = None
        if r:
            ids_ = tids_of(r) if r.get("result") in ("tuple", "multi_tuple", "combo_ref") else []
            end = {"kind": "procedure", "ids": ids_} if ids_ else {"kind": "modality", "ids": [mkid("MOD", T["modality"])]}
        out.append({"timeline": T["id"], "name": T["name"], "category": T["category"], "end": end, "result": r.get("result") if r else None, "ref_id": r.get("ref_id") if r else None})
    return out


def silver_dictionary(dj, A, node_decs=(), v33=False):
    """실버 사전(out/dictionaries.json) — 결정 ① 뒤 사전(장비 제품 origin=taxonomy 포함) + 원장 사건 노드(adverse_event_type origin=ledger · 출처 locator · 설명 문맥 · v3.2: status=unreviewed · category None /
    v3.3: 정식 노드 — status·category 없음(V3.3-E · 사용자 「unreviewed 는 지시 아님」)) + 노드 결정 이력(접힌 노드는 접힐 곳의 동의어 · 뺀 노드는 excluded_ledger_nodes) + 문구 사전 자리(phrase_index · 결정 뒤 내용은 report 가 채운다)."""
    out = copy.deepcopy(dj)
    D = {d["name"]: d for d in out["dictionaries"]}
    E = D["adverse_event_type"]
    have = {norm(e["canonical"]) for e in E["entries"]}
    dup_by = defaultdict(list)
    for d in A["duplicate_pairs"]:
        dup_by[d["new_id"]].append({"existing": d["existing"], "existing_kind": d["existing_kind"], "rules": d["rules"], "grade": d["grade"], "stable_key": d["stable_key"]})
    for n in A["ledger_events"]:
        if norm(n["canonical"]) in have:
            continue
        src = [{"file": "complications.json" if any(l.startswith("complications.json") for l in n["locators"]) else n["locators"][0].split(":", 1)[0], "path": None, "n": len(n["locators"]), "kind": "ledger_core"}]
        if v33:
            E["entries"].append(OrderedDict([("id", n["id"]), ("canonical", n["canonical"]), ("sources", src), ("synonyms", []), ("definition", None), ("origin", "ledger"), ("locators", list(n["locators"])), ("contexts", list(n["contexts"])),
                                             ("core_tokens", n.get("core_tokens")), ("duplicate_candidates", dup_by.get(n["id"], []))]))
            continue
        E["entries"].append(OrderedDict([("id", n["id"]), ("canonical", n["canonical"]), ("sources", src),
                                         ("synonyms", []), ("definition", None), ("category", None), ("origin", "ledger"), ("status", "unreviewed"), ("locators", list(n["locators"])), ("contexts", list(n["contexts"])),
                                         ("core_tokens", n.get("core_tokens")), ("duplicate_candidates", dup_by.get(n["id"], []))]))
    for d in node_decs:
        t, nv = d["target"], d["new_value"]
        if t.get("dictionary") == "adverse_event_type" and d["kind"] == "fold_approve":
            into = t.get("into") or nv.get("keep")
            tgt = next((e for e in E["entries"] if norm(e["canonical"]) == norm(into)), None)
            if tgt is not None and norm(t["canonical"]) not in {norm(s_["value"]) for s_ in tgt.get("synonyms", [])}:
                tgt.setdefault("synonyms", []).append({"value": t["canonical"], "link": "fold_approve", "sources": [{"kind": "decision", "decision_id": d["id"]}]})
        elif d["kind"] == "exclude":
            E.setdefault("excluded_ledger_nodes", []).append({"canonical": t["key"]["canonical"], "decision_id": d["id"]})
    if not any(d["name"] == "phrase_dictionary" for d in out["dictionaries"]):
        out["dictionaries"].append({"name": "phrase_dictionary", "label": "문구 사전(부작용 문구 종류 · v3.2)", "kind": "phrase_index", "closed": None, "entries": [], "note": "v3.2: 부작용 문구 종류만(exact · new · approved) + 메모·설명문(note · sentence)"})
    for x in out["dictionaries"]:
        x["canonical_count"] = len(x["entries"])
        x["synonym_count"] = sum(len(e.get("synonyms", [])) for e in x["entries"])
    return out
