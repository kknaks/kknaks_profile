# -*- coding: utf-8 -*-
"""ERD v3.3 부작용 핵심어 — 토큰화 = 형태소 분석기(V3.3-B · kiwipiepy 0.24 · lib/analyzer.py 캐시) · 드라이런 3차(dryrun3/dry3_au.py) 규칙을 lib 로 옮겼다.

AdverseUnits33 은 v3.2 AdverseUnits32 위에서 「사전 사건이 0 인 토막의 핵심어 → 새 사건 노드」(V3.2-0 노드 원칙 · _apply_cores) 만 바꾼다.
  셈 순서 T3 → T4 → N2(T2) → T1 → N1 → R2 → R1 (dryrun3 §0 그대로)
  T3  괄호 안 묶음이 기호·라틴·숫자 위주(형태소 과반) → 사건 후보 아님(explanation 보존) · 정확히 절반 = 애매(적용 안 함 · 기록)
  T4  같은 묶음에서 「--」「—」「:」 뒤 멤버의 토막 → 서술(predicate_marker · explanation 보존)
  N2  문장꼴 = 절이 있을 때만(용언+EC/EF(-게 제외) · ETM/-게 앞 격조사 논항 · ETM 뒤 NNB·현상·느낌·증상·경우)
        (a) 토막에 사전 사건 NNG(조사가 붙어 통째 일치를 놓친 것) → 그 사건(exact) · 나머지 서술 · 멤버에 사전 사건 있으면 토막은 서술
        (b) 없음 → 노드 없음 · 문구는 phrase_dictionary status=sentence(사람 판정 · 게이트 6)
      절 없이 명사 앞 관형어·부사어 하나 = 수식어(R1 · 보존 · parsed.misc · by=analyzer_n2 · R1 목록에 더하지 않는다 — 「R1 후보」 게이트)
  T1  핵심어 = 명사(NNG·NNP · 등록 사전 값 SL) + N1 명사형 어절(통째) · 같은 어절 XSN/XPN 은 명사에 붙인다 · 명사 밖 내용 형태소는 explanation 보존
  N1  용언 어간 + -ㅁ/-음(ETN·EF) 어절 = 명사(어절 그대로 · 뒤 접속 조사·기호만 뗌 · 「따가움감」 꼴 허용) · 후보 전부 이상 꼴(ANOM) 어절은 통째 명사 —
      1위 분석의 어절 끝이 조사(JC 뺌)·EC·ETM 이면 애매(노드 없음 · 사람)
  R2  명사열에서 부위·구조 말(부위 사전 전부 + analyzer_assist 구조 말 목록) 뒤에 명사가 더 있으면 뗀다 — 부위 사전 값이면 그 멤버의 부위 칸(span · basis=analyzer_r2 · 원칙 C),
      사전 밖 구조 말(신경·눈·근육 밖 …)은 side(보존 · 칸 아님)
  R1  명사열 맨 앞·맨 뒤의 R1 말(analyzer_assist 목록 · 「이상」 제외)을 뗀다(parsed.misc · by=analyzer_r1 · 보존)
R3(단독 출현 0 노드 버림)·R4(병기 X(Y) 접기)는 자동 적용하지 않는다 — R3 은 노드의 단독 출현 수로 게이트에 보이고, R4 는 ⑦ paren_pair(strong) 로 올라온다(접기는 fold_approve).
목록(R1 · R2 구조 말)은 ERD 규칙 데이터가 아니라 1차 발주서(silver-dryrun-brief) 목록 — analyzer_assist 로만 쓰고 ERD 질문으로 돌린다.
"""
import re
from collections import Counter, OrderedDict, defaultdict

from . import v32 as V32
from .decompose import ADV_MEMBER_SPLIT, ADV_PAREN, ADV_STRIP
from .util import dedupe, norm

HANGUL = V32.HANGUL
LATIN = V32.LATIN
CUR = V32.CUR

# analyzer_assist 목록(ERD 규칙 데이터 아님 · 1차 발주서 silver-dryrun-brief 목록 · dryrun3/common3.py 그대로 · R1 은 「이상」 제외)
ASSIST_R1 = ["장기간", "장기적", "임시", "일시", "일시적", "지속", "지속적", "영구", "영구적", "중등도", "중증", "심한", "경미", "경미한", "과도", "과도한", "불규칙",
             "미세", "미세한", "약간", "약간의", "광범위", "광범위한", "초기", "드문", "높음", "증가", "덜"]
ASSIST_R2 = ["신경", "하악변연신경", "안면신경", "감각신경", "눈", "안구", "결막", "눈썹", "눈꺼풀", "표정근", "근육", "두피", "피부", "진피", "혈관", "전신", "표면", "주사 부위", "시술 부위"]
PRED_TAGS = {"VV", "VA", "VX", "XSV", "XSA"}
PRED_KIND_TAGS = PRED_TAGS | {"VCP"}
NOUN_TAGS = {"NNG", "NNP"}
S_TAGS_T3 = {"SL", "SN", "SW", "SP", "SS", "SSO", "SSC", "SE", "SO", "SB", "SH"}
N1_FORMS = {"ᆷ", "음", "ㅁ"}
HEAD_NOUNS = {"현상", "느낌", "증상", "경우"}
ARG_PARTICLES = {"JKS", "JKO", "JKB"}
T4_DELIM = re.compile(r"--|—|:")
CONTENT_MOD_CLASSES = {"misc", "condition", "connector"}
TIMELINE_KW = ["일", "주", "개월", "시간", "분", "후", "이내", "지나", "사라지", "호전", "회복", "소실", "완화", "가라앉", "없어지", "줄어들", "감소", "자연", "점차", "며칠", "수일", "수주"]
NOTICE_KW = ["고지", "주의", "금기", "반드시", "상담", "권장", "금지", "피하", "삼가", "알려야", "설명", "동의", "필요", "즉시", "응급"]
STRIP = ADV_STRIP + ","
GONE_SENTENCE = ("T2b",)
GONE_AMBIG = ("ANOM", "T1-pred", "T1-none", "T1-partial")
GONE_EXPLAIN = ("T3", "T4", "T2a-rest")


def classify_remainder(text):
    """서술 부분의 행선지 힌트(타임라인 / 동의서 고지 / 설명문) — 낱말 목록 일치만 · 추천 아님(게이트 힌트)."""
    t = str(text)
    if any(k in t for k in NOTICE_KW):
        return "동의서 고지"
    if re.search(r"\d", t) or any(k in t for k in TIMELINE_KW):
        return "타임라인"
    return "설명문"


def ws_spans(s):
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", s)]


def member_offsets(gtext):
    """ADV_MEMBER_SPLIT 로 가른 멤버(비지 않은 것)의 시작 글자 위치 — _split_base 의 members 순서와 같다."""
    out, pos = [], 0
    for m in ADV_MEMBER_SPLIT.finditer(gtext):
        part = gtext[pos:m.start()]
        if part.strip():
            out.append(pos + (len(part) - len(part.lstrip())))
        pos = m.end()
    part = gtext[pos:]
    if part.strip():
        out.append(pos + (len(part) - len(part.lstrip())))
    return out


def analyzer_texts(text):
    """한 문구에서 분석기가 보게 될 문자열 전부(멤버 · 괄호 안 묶음) — 캐시 미리 채우기(Analyzer.ensure)."""
    text = str(text)
    parens = ADV_PAREN.findall(text)
    outer = ADV_PAREN.sub(" ", text)
    out = []
    for g in [outer] + parens:
        out.append(g)
        for part in ADV_MEMBER_SPLIT.split(g):
            part = part.strip()
            if part:
                out.append(part)
    return [x for x in out if x.strip()]


def word_tokens(toks, ws):
    return [(f, tg, a, b, next((wi for wi, x in enumerate(ws) if x[0] <= a < x[1]), -1)) for f, tg, a, b in toks]


def word_kind(ts):
    """어절 하나의 형태소 → (kind, info). kind: N1 · N1case · N1part · ETM · ADV · CLAUSE · ARG · NOUN · OTHER."""
    core = list(ts)
    while core and core[-1][1].startswith("S"):
        core.pop()
    conj = False
    if core and core[-1][1] == "JC":
        core.pop()
        conj = True
    if not core:
        return "OTHER", {}
    ei = max((i for i, t in enumerate(core) if t[1].startswith("E")), default=None)
    if ei is None:
        if core[-1][1] in ARG_PARTICLES:
            return "ARG", {}
        return ("NOUN" if any(t[1] in ("NNG", "NNP", "XR", "XSN") for t in core) else "OTHER"), {"conj": conj}
    e = core[ei]
    after = core[ei + 1:]
    has_pred = any(t[1] in PRED_KIND_TAGS for t in core[:ei])
    vcp_only = has_pred and not any(t[1] in PRED_TAGS for t in core[:ei])
    if not has_pred:
        return "OTHER", {"ending": e}
    if e[1] in ("ETN", "EF") and e[0] in N1_FORMS and not vcp_only:
        if not after:
            return "N1", {"end": e[3], "conj": conj, "ending": e}
        if all(t[1] in ("NNG", "XSN") for t in after):          # 「따가움감」 — 명사형 + 감(명사·접미)
            return "N1", {"end": after[-1][3], "conj": conj, "ending": e, "suffix": "".join(t[0] for t in after)}
        if all(t[1].startswith("J") for t in after):
            return ("N1case" if after[-1][1] in ARG_PARTICLES else "N1part"), {"ending": e}
        return "OTHER", {"ending": e}
    if after and all(t[1].startswith("J") for t in after):
        return ("ARG" if after[-1][1] in ARG_PARTICLES else "OTHER"), {"ending": e}
    if after:
        return "OTHER", {"ending": e}
    if e[1] == "ETM":
        return "ETM", {"ending": e}
    if e[1] == "EC" and e[0] == "게":
        return "ADV", {"ending": e}
    if vcp_only:
        return "OTHER", {"ending": e}
    if e[1] in ("EC", "EF", "ETN"):
        return "CLAUSE", {"ending": e}
    return "OTHER", {"ending": e}


def word_info(an, text, r1):
    """멤버 문자열 → 어절마다 kind · N2 판정(sent · clause_words · mod_words · n1 · kinds · why · ws · tw)."""
    text = str(text)
    toks = an.tokens(text)
    ws = ws_spans(text)
    tw = word_tokens(toks, ws)
    bad = {w for w, _ in an.anom(text)}
    byw = defaultdict(list)
    for t in tw:
        byw[t[4]].append(t)
    kinds, infos = {}, {}
    for wi in range(len(ws)):
        kinds[wi], infos[wi] = word_kind(byw.get(wi, []))
    clause, mods, n1, why = [], [], {}, {}
    for wi in range(len(ws)):
        w = ws[wi][2]
        k = kinds[wi]
        wn = norm(w.strip(STRIP))
        if w in bad:
            continue
        if k == "N1":
            n1[wi] = text[ws[wi][0]:infos[wi]["end"]]
            continue
        if k == "CLAUSE":
            clause.append(wi)
            why[wi] = f"{w}: 용언+{infos[wi]['ending'][0]}/{infos[wi]['ending'][1]}"
            continue
        if k in ("ETM", "ADV"):
            if wn in r1:
                continue
            args = [j for j in range(wi) if kinds[j] in ("ARG", "N1case") and ws[j][2] not in bad]
            head = None
            if k == "ETM" and wi + 1 < len(ws):
                nx = [t for t in byw.get(wi + 1, []) if not t[1].startswith("S")]
                if nx:
                    head = nx[0]
                    if head[1] == "NNB" and any(t[1] in ("NNG", "NNP", "XSN", "XR") or t[1] in PRED_TAGS for t in nx[1:]):
                        head = ("", "NNB+")
            if args:
                clause.append(wi)
                why[wi] = f"{w}: 앞 어절 「{ws[args[-1]][2]}」 이 격조사로 끝남(논항)"
            elif head and (head[1] == "NNB" or head[0] in HEAD_NOUNS):
                clause.append(wi)
                why[wi] = f"{w}: 관형형 + {'의존명사' if head[1] == 'NNB' else '「' + head[0] + '」'}"
            else:
                mods.append(wi)
                why[wi] = f"{w}: 관형어·부사어 하나(수식어)"
    return dict(sent=bool(clause), clause_words=[ws[i][2] for i in clause], mod_words=[ws[i][2] for i in mods], mod_wi=set(mods), n1=n1, kinds=kinds, why=why, ws=ws, tw=tw)


def paren_kind(an, inner, r1):
    """T3 — 괄호 안 묶음: S(기호·라틴·숫자 과반) · tie(정확히 절반 · 애매) · sentence · noun · empty."""
    toks = an.tokens(inner)
    content = [t for t in toks if not (t[1].startswith("J") or t[1].startswith("E"))]
    if not content:
        return "empty", 0.0
    s = sum(1 for t in content if t[1] in S_TAGS_T3)
    ratio = s / len(content)
    if ratio > 0.5:
        return "S", ratio
    if ratio == 0.5:
        return "tie", ratio
    if word_info(an, inner, r1)["sent"]:
        return "sentence", ratio
    return "noun", ratio


def noun_units(toks, dict_values, rwords=frozenset(), words=None, n1=None, mods=None, out=None):
    """T1 — 형태소 → 명사 단위 [[글자, 어절 번호]] · (units, dropped[(글자, 품사)], affix[], partial[(어절, 버린 형태소)])."""
    units, dropped, affix, partial = [], [], [], []
    byw = {}
    for t in toks:
        byw.setdefault(t[4], []).append(t)
    for wi in sorted(byw):
        ts = byw[wi]
        if words is not None and 0 <= wi < len(words):
            wsurf = words[wi].strip(ADV_STRIP)
            if norm(wsurf) in rwords:
                units.append([wsurf, wi])
                continue
        if n1 and wi in n1:
            units.append([n1[wi], wi])
            if out is not None:
                out.setdefault("n1_used", []).append(n1[wi])
            continue
        if mods and wi in mods:
            if out is not None:
                out.setdefault("mods_removed", []).append(words[wi] if words else "")
            continue
        w_units, w_drop = [], []
        pend = ""
        prev_noun = False
        for i, t in enumerate(ts):
            f, tag = t[0], t[1]
            nxt = ts[i + 1][1] if i + 1 < len(ts) else None
            if tag in NOUN_TAGS or (tag == "SL" and norm(f) in dict_values):
                w_units.append([pend + f, wi])
                if pend:
                    affix.append(pend + "+" + f)
                pend, prev_noun = "", True
                continue
            if tag == "XR" and nxt in ("XSN", "NNG", "NNP"):
                w_units.append([pend + f, wi])
                pend, prev_noun = "", True
                continue
            if tag == "XSN" and prev_noun:
                w_units[-1][0] += f
                affix.append("+" + f)
                continue
            prev_noun = False
            if tag == "XPN":
                pend += f
                continue
            if pend:
                w_drop.append((pend, "XPN"))
                pend = ""
            if tag.startswith("J") or tag.startswith("E") or tag.startswith("S"):
                continue
            w_drop.append((f, tag))
        if pend:
            w_drop.append((pend, "XPN"))
        units += w_units
        dropped += w_drop
        if w_units and [x for x in w_drop if x[1] != "NNB"]:
            partial.append((words[wi] if words else "", w_drop))
    return units, dropped, affix, partial


def join_units(units):
    out, last = [], None
    for f, wi in units:
        if out and wi == last:
            out[-1] += f
        else:
            out.append(f)
        last = wi
    return " ".join(out)


def strip_r2(units, r2):
    """R2: 위치 i 에서 이어 붙인 형태소(가장 긴 것)가 R2 말이고 그 뒤에 명사가 더 있으면 뗀다. → (남은 단위, 뗀 말들)."""
    keep, hits, i = [], [], 0
    while i < len(units):
        best = None
        for j in range(len(units), i, -1):
            if norm("".join(u[0] for u in units[i:j])) in r2:
                best = j
                break
        if best is not None and best < len(units):
            hits.append("".join(u[0] for u in units[i:best]))
            i = best
            continue
        keep.append(units[i])
        i += 1
    return keep, hits


def strip_r1(units, r1):
    hits = []
    while len(units) > 1:
        if norm(units[0][0]) in r1:
            hits.append(("front", units[0][0]))
            units = units[1:]
            continue
        if norm(units[-1][0]) in r1:
            hits.append(("back", units[-1][0]))
            units = units[:-1]
            continue
        break
    return units, hits


class AdverseUnits33(V32.AdverseUnits32):
    """v3.3 — 사전 사건 0 인 토막의 핵심어를 분석기 품사로 가른다(위 규칙). 기록은 self.seglog(토막마다) · self.loc_kinds(locator → 토막 결과 종류)."""

    def __init__(self, ids, rules):
        super().__init__(ids, rules)
        self.an = CUR["analyzer"]
        self.r1 = {norm(w) for w in ASSIST_R1}
        self.sites = dict(ids.site_surface)                       # norm(부위 표면형) → 정준값(부위 사전 전부 · ① 뒤 값 포함)
        self.r2 = {norm(w) for w in ASSIST_R2} | set(self.sites) | set(ids.rsite_surface)
        self.dict_values = set(CUR.get("analyzer_values") or set())
        self.seglog = []                                          # 토막 기록(게이트 6 · 보고)
        self.loc_kinds = defaultdict(list)                        # locator → [토막 결과 종류]
        self.solo_strict = Counter()                              # 노드 핵심어 → 「그 말 하나」로 선 자리 수(R3 신호)
        self.r1_new = Counter()                                   # N2 수식어(R1 목록 밖) → 횟수(R1 후보 게이트)
        self.r1_new_locs = defaultdict(list)
        self.r2_struct = Counter()                                # 사전 밖 구조 말(side 보존)
        self.t3_parens = []
        self.n1_names = set()

    def _canon_now(self, core):
        key = norm(core)
        if key in self.base_event_surface:
            return ("dict", self.base_event_surface[key])
        if key in (CUR.get("not_adverse") or {}):
            return ("excluded", core)
        folds = CUR.get("node_folds") or {}
        if key in folds:
            seen, tgt = {key}, folds[key]
            while norm(tgt) in folds and norm(tgt) not in seen:
                seen.add(norm(tgt))
                tgt = folds[norm(tgt)]
            if norm(tgt) in self.base_event_surface:
                return ("dict", self.base_event_surface[norm(tgt)])
            return ("node", tgt)
        return ("node", core)

    def _seg_ranges(self, m, text):
        segs, cur, start = [], [], -1
        for x in self._pieces(m, text):
            if x[1] == "bd":
                segs.append((cur, start, x[0]))
                cur, start = [], x[0]
            else:
                cur.append(x)
        segs.append((cur, start, 10 ** 7))
        return [s for s in segs if s[0]]

    def _apply_cores(self, groups, text, loc):
        an = self.an
        has_h = bool(HANGUL.search(str(text)))
        excl = {norm(w) for w in (CUR["kinds"].get("core_exclude") or [])}
        outer_text = ADV_PAREN.sub(" ", str(text))
        gtexts = [outer_text] + ADV_PAREN.findall(str(text))
        create = self.mode == "create" and loc
        for gi, g in enumerate(groups):
            if gi > 0 and not self._has_event(g):
                continue
            gtext = gtexts[gi] if gi < len(gtexts) else ""
            offs = member_offsets(gtext)
            dm = T4_DELIM.search(gtext)
            pk, pratio = (paren_kind(an, gtext, self.r1) if gi > 0 and gtext.strip() else (None, None))
            if gi > 0 and create:
                self.t3_parens.append({"locator": loc, "inner": gtext, "kind": pk, "ratio": pratio})
            for mi, m in enumerate(g["members"]):
                moved = [u for u in m["untouched"] if (has_h and V32.script_of(u) == "L") or norm(u) in excl or not (HANGUL.search(u) or LATIN.search(u))]
                if moved:
                    m.setdefault("explanation", []).extend(moved)
                    m["untouched"] = [u for u in m["untouched"] if u not in moved]
                if not m["untouched"] and (any(s_["kind"] == "event" for s_ in m["spans"]) or gi > 0):
                    continue
                if not m["untouched"] and not any(p[1] in ("fb", "pr") for p in self._pieces(m, text)):
                    continue
                txt = m["text"]
                after_delim = bool(dm) and mi < len(offs) and offs[mi] > dm.start()
                WI = word_info(an, txt, self.r1)
                sent, sent_words = WI["sent"], WI["clause_words"]
                bad_words = {w for w, _ in an.anom(txt)}
                mt = an.tokens(txt)
                ws = ws_spans(txt)
                mt_w = word_tokens(mt, ws)
                member_dict7 = [s_ for s_ in m["spans"] if s_["kind"] == "event"]
                mods_pos = [(txt.find(md["text"]), md) for md in m.get("modifiers", []) if norm(md["text"]) not in self.fallback]
                segs = self._seg_ranges(m, text)
                seg_info = []
                for sg, s0, s1 in segs:
                    evs = [x for x in sg if x[1] == "ev"]
                    wis = set()
                    for x in sg:
                        if x[1] in ("u", "fb", "pr") and 0 <= x[0] < 10 ** 6:
                            wi = next((k for k, w in enumerate(ws) if w[0] <= x[0] < w[1]), None)
                            if wi is not None:
                                wis.add(wi)
                    toks = [t for t in mt_w if t[4] in wis]
                    kd = [t for t in toks if t[1] in NOUN_TAGS and norm(t[0]) in self.base_event_surface]
                    seg_info.append((sg, s0, s1, evs, wis, toks, kd))
                member_has_dict = bool(member_dict7) or any(si[6] for si in seg_info)
                new_spans, side, cores, left, m_recs = [], [], [], [], []
                for sg, s0, s1, evs, wis, toks, kd in seg_info:
                    us = [x[2] for x in sg if x[1] == "u"]
                    prs = [x for x in sg if x[1] == "pr"]
                    if evs:
                        side += us
                        continue
                    toks7 = [x[2] for x in sg if x[1] in ("u", "fb")] or ([x[2] for x in prs] if gi == 0 else [])
                    if not toks7 or (not us and gi > 0):
                        continue
                    core7 = " ".join(toks7)
                    seg_text = " ".join(ws[w][2] for w in sorted(wis))
                    rec = OrderedDict([("locator", loc), ("where", g["where"]), ("member", txt), ("segment", seg_text), ("core_list", core7), ("kind", None), ("rules", []), ("target", []), ("site", []), ("r2", []), ("r1", []),
                                       ("r1_new", []), ("n1", []), ("dropped", []), ("amb", []), ("sentence_words", sent_words), ("remainder_hint", None), ("paren_kind", pk)])
                    outcome = None    # ('node'|'dict', [core]) | ('gone', why)
                    if gi > 0 and pk == "S":
                        rec["rules"].append("T3")
                        outcome = ("gone", "T3")
                    elif after_delim:
                        rec["rules"].append("T4")
                        outcome = ("gone", "T4")
                        rec["remainder_hint"] = classify_remainder(txt)
                    else:
                        if gi > 0 and pk == "tie":
                            rec["amb"].append(f"T3: 괄호 안 기호·라틴·숫자 형태소가 정확히 절반(「{gtext}」) — 적용 안 함")
                        if sent:
                            if kd:
                                rec["rules"].append("T2a")
                                outcome = ("dict", dedupe(t[0] for t in kd))
                                rec["kind"] = "T2a-capture"
                                rec["remainder_hint"] = classify_remainder(seg_text)
                            elif member_has_dict:
                                rec["rules"].append("T2a")
                                outcome = ("gone", "T2a-rest")
                                rec["remainder_hint"] = classify_remainder(seg_text)
                            else:
                                rec["rules"].append("T2b")
                                outcome = ("gone", "T2b")
                                units, dropped, affix, partial = noun_units(toks, self.dict_values, self.r1 | self.r2, [w[2] for w in ws], n1={w: WI["n1"][w] for w in wis if w in WI["n1"]})
                                rec["nouns"] = [u[0] for u in units]
                                rec["remainder_hint"] = classify_remainder(txt)
                                rec["clause_why"] = [WI["why"][w] for w in sorted(WI["why"]) if w not in WI["mod_wi"]]
                        seg_bad_wi = [w for w in sorted(wis) if ws[w][2] in bad_words]
                        n1map = {w: WI["n1"][w] for w in sorted(wis) if w in WI["n1"]}
                        modset = {w for w in WI["mod_wi"] if w in wis}
                        anom_att = []
                        for w in seg_bad_wi:
                            core_t = [t for t in mt_w if t[4] == w]
                            while core_t and core_t[-1][1].startswith("S"):
                                core_t.pop()
                            if core_t and core_t[-1][1] == "JC":
                                core_t.pop()
                            last = core_t[-1] if core_t else None
                            if last is None or (last[1].startswith("J") or last[1] in ("EC", "ETM")):
                                anom_att.append(w)
                            else:
                                n1map[w] = txt[ws[w][0]:last[3]].strip(STRIP)
                                rec.setdefault("n1_anom", []).append(n1map[w])
                        pred_odd = [w for w in sorted(wis) if w not in n1map and w not in modset and w not in seg_bad_wi and WI["kinds"].get(w) in ("N1case", "N1part", "OTHER")
                                    and any(t[1] in PRED_TAGS for t in mt_w if t[4] == w) and norm(ws[w][2].strip(STRIP)) not in (self.r1 | self.r2)]
                        if outcome is None and anom_att:
                            rec["rules"].append("T1")
                            outcome = ("gone", "ANOM")
                            rec["amb"].append(f"분석기: 어절 {', '.join('「' + ws[w][2] + '」' for w in anom_att)} 의 후보 전부가 어절 안 이상 꼴 · 1위 분석의 어절 끝이 조사·연결어미 — N1 통째 명사 적용 불가")
                        if outcome is None and pred_odd:
                            rec["rules"].append("T1")
                            outcome = ("gone", "T1-pred")
                            rec["amb"].append(f"T1·N1: 용언 어절 {', '.join('「' + ws[w][2] + '」(' + WI['kinds'][w] + ')' for w in pred_odd)} — 명사형(어절 끝 -ㅁ/-음)도 수식어도 절도 아님 — 적용 안 함")
                        if outcome is None:
                            uo = {}
                            units, dropped, affix, partial = noun_units(toks, self.dict_values, self.r1 | self.r2, [w[2] for w in ws], n1=n1map, mods=modset, out=uo)
                            rec["dropped"] = [list(x) for x in dropped]
                            rec["n1"] = uo.get("n1_used", [])
                            rec["r1_new"] = [x for x in uo.get("mods_removed", [])]
                            if not units:
                                rec["rules"].append("T1")
                                outcome = ("gone", "T1-none")
                                rec["amb"].append(f"T1: 명사 없음({', '.join(f'{f}/{t}' for f, t in dropped) or '형태소 없음'}) — 사건 이름인지 애매")
                            elif partial:
                                rec["rules"].append("T1")
                                outcome = ("gone", "T1-partial")
                                rec["amb"].append(f"T1: 명사 단위가 있는 어절 안에서 명사 아닌 형태소를 버림({'; '.join(w + ' → ' + ', '.join(f'{f}/{t}' for f, t in d) for w, d in partial)}) — 분석기 판정 확인 필요 · 적용 안 함")
                            else:
                                if rec["n1"]:
                                    rec["rules"].append("N1")
                                else:
                                    rec["rules"].append("T1")
                                u2, h2 = strip_r2(units, self.r2)
                                if h2:
                                    rec["rules"].append("R2")
                                    rec["r2"] = h2
                                u1, h1 = strip_r1(u2, self.r1)
                                if h1 or rec["r1_new"]:
                                    rec["rules"].append("R1")
                                    rec["r1"] = [x[1] for x in h1]
                                core2 = join_units(u1)
                                if norm(core2) not in self.base_event_surface and any(norm(u[0]) in self.base_event_surface for u in u1) and len(u1) > 1:
                                    rec["amb"].append(f"사전 사건 「{next(u[0] for u in u1 if norm(u[0]) in self.base_event_surface)}」에 R1·R2 밖 명사가 붙음(「{core2}」) — 규칙 밖 → 노드로 둠")
                                outcome = ("node", [core2])
                    rec["kind"] = rec["kind"] or (outcome[0] if outcome[0] != "gone" else outcome[1])
                    # ---- 등록 · 보존
                    if outcome[0] in ("node", "dict"):
                        for h in rec["r2"]:
                            if norm(h) in self.sites:
                                new_spans.append({"kind": "site", "canonical": self.sites[norm(h)], "text": h, "basis": "analyzer_r2"})
                                rec["site"].append(self.sites[norm(h)])
                            elif norm(h) in self.ids.rsite_surface:
                                new_spans.append({"kind": "relative", "canonical": self.ids.rsite_surface[norm(h)], "text": h, "basis": "analyzer_r2"})
                            else:
                                side.append(h)
                                self.r2_struct[h] += 1
                        for w_ in rec["r1"]:
                            m.setdefault("modifiers", []).append({"text": w_, "class": "misc", "by": "analyzer_r1", "key": w_})
                        for w_ in rec["r1_new"]:
                            m.setdefault("modifiers", []).append({"text": w_, "class": "misc", "by": "analyzer_n2", "key": w_})
                            if create:
                                self.r1_new[w_.strip(STRIP)] += 1
                                if loc not in self.r1_new_locs[w_.strip(STRIP)]:
                                    self.r1_new_locs[w_.strip(STRIP)].append(loc)
                        for f_, t_ in rec["dropped"]:
                            m.setdefault("explanation", []).append(f_)
                        for core in outcome[1]:
                            canon, origin = self._register_core(core, m, text, loc)
                            if canon is None and origin == "excluded":
                                m.setdefault("explanation", []).extend(us)
                                m.setdefault("excluded_core", []).append(core)
                                rec["kind"] = "excluded"
                                continue
                            if canon is None:
                                left += us
                                rec["kind"] = "refer-miss"
                                continue
                            rec["target"].append(canon)
                            cores.append(core)
                            new_spans.append({"kind": "event", "canonical": canon, "text": core, "basis": "ledger_core" if origin == "ledger" else "core_exact"})
                            if create and outcome[0] == "node":
                                if rec["n1"]:
                                    self.n1_names.add(norm(canon))
                                other_strict = [p[2] for p in prs] + [f for f, t in rec["dropped"]] + [md["text"] for pos, md in mods_pos if s0 <= pos < s1 and md["class"] in CONTENT_MOD_CLASSES and norm(md["text"]) not in self.r1]
                                if not other_strict:
                                    self.solo_strict[norm(canon)] += 1
                        if rec["kind"] == "T2a-capture":
                            rest = [ws[w][2] for w in sorted(wis)]
                            m.setdefault("explanation", []).extend(dedupe(x for x in us if x not in rec["target"]))
                    else:
                        m.setdefault("explanation", []).extend(us + [x[2] for x in prs])
                    if create:
                        self.seglog.append(rec)
                        self.loc_kinds[loc].append(rec["kind"])
                    m_recs.append(OrderedDict([("segment", rec["segment"]), ("kind", rec["kind"]), ("rules", rec["rules"]), ("target", rec["target"]), ("r2", rec["r2"]), ("r1", rec["r1"] + rec["r1_new"]), ("amb", rec["amb"])]))
                if side:
                    m["side"] = dedupe(list(m.get("side") or []) + side)
                if cores:
                    m["core_tokens"] = cores
                if m_recs:
                    m["analyzer"] = m_recs
                m["spans"] = list(m["spans"]) + new_spans
                m["untouched"] = left
                if self.mode == "refer" and side:
                    m["untouched"] = left + side
        return groups

    def _parsed(self, groups):
        p = super()._parsed(groups)
        p["analyzer"] = [x for g in groups for m in g["members"] for x in m.get("analyzer", [])]
        return p

    def gone_kinds(self, loc):
        return [k for k in self.loc_kinds.get(loc, []) if k in GONE_SENTENCE + GONE_AMBIG + GONE_EXPLAIN]
