# -*- coding: utf-8 -*-
"""드라이런 3차 전용 — lib.v32.AdverseUnits32 를 감싼다(lib 는 고치지 않는다 · 이 프로세스 안에서만 바꿔 끼운다).
2차 코드(dryrun2/dry2_au.py)를 복사해 3차 규칙(발주서 silver-dryrun3-brief.md N1·N2·N4)만 바꿨다. N3·N5·S 는 run_dryrun3.py.

7차와 같은 것: 묶음(바깥 · 괄호 안) · 멤버(구분자) · 사전 값 통째 일치(span) · 수식어(stopwords 138 · 패턴) · 접속 조사 토막 · 결정(exclude · fold).
  (셈 순서 T3 → T4 → N2 → T1 → N1 → R2(+N4) → R1)
  T3  괄호 안 묶음이 기호·라틴·숫자 위주(형태소 과반) → 사건 후보 아님 · 정확히 절반 = 애매(적용 안 함)       (2차 그대로)
  T4  같은 묶음에서 「--」「—」「:」 뒤 멤버의 토막 → 설명                                                      (2차 그대로)
  N2  문장꼴 = 절이 있을 때만. 어절마다 마지막 어미로 가른다(word_kind):
        CLAUSE  용언 + 연결 어미(EC · 「-게」 뺌)·종결 어미(EF · -ㅁ/-음 뺌)·명사형 「-기」
        ETM     관형형 — 뒤 어절 머리가 의존명사(NNB)이거나 「현상·느낌·증상·경우」(발주서 예) 이거나,
                앞에 격조사(JKS·JKO·JKB) 붙은 어절(그 용언의 논항)이 있으면 절(서술이 이어짐) · 아니면 관형어 하나 = 수식어(R1 후보)
        ADV     「-게」 부사형(「드물게」) — 논항이 앞에 있으면 절, 아니면 수식어(R1 후보)
        N1      용언 어간 + 명사형 -ㅁ/-음(ETN·EF) 로 어절이 끝남 — 명사(사건 이름 후보 · 어절 그대로)
      (a) 토막 안에 사전 사건 NNG · 멤버에 사전 사건 → 2차 T2(a) 와 같음 · (b) 없음 → 「문장꼴 — 사용자」
  T1  핵심어 = 명사(NNG·NNP · 사전 값 SL) + N1 어절(통째) — 수식어(ETM/ADV 관형어·부사어) 어절은 R1 후보(새)로 뗀다
  N1  ANOM(후보 전부 이상 꼴) 어절은 통째 명사 — 1위 분석의 어절 끝이 조사(JC 뺌)·EC·ETM 이면 「조사·연결어미 붙음」 → 애매 그대로
  R2  명사열에서 R2 말(+ N4 임시 부위: 동맥·정맥·안동맥) 뒤에 명사가 더 있으면 부위로 뗀다(2차 그대로)
  R1  명사열 맨 앞·맨 뒤 R1 말(「이상」 뺌)을 뗀다(2차 그대로)
기록: 토막마다 7차 핵심어 → 3차 결과(규칙 · 대상) · 단독 출현.
"""
import re
from collections import Counter, defaultdict

from lib import v32 as V32
from lib.decompose import ADV_MEMBER_SPLIT, ADV_PAREN
from lib.util import norm

import kiwi_t0 as KT

HANGUL = V32.HANGUL
LATIN = V32.LATIN
CUR = V32.CUR
CONTENT_MOD_CLASSES = {"misc", "condition", "connector"}
T4_DELIM = re.compile(r"--|—|:")

TIMELINE_KW = ["일", "주", "개월", "시간", "분", "후", "이내", "지나", "사라지", "호전", "회복", "소실", "완화", "가라앉", "없어지", "줄어들", "감소", "자연", "점차", "며칠", "수일", "수주"]
NOTICE_KW = ["고지", "주의", "금기", "반드시", "상담", "권장", "금지", "피하", "삼가", "알려야", "설명", "동의", "필요", "즉시", "응급"]


def classify_remainder(text):
    """서술 부분 분류 제안(타임라인 / 동의서 고지 / 설명문) — 낱말 목록 일치만(제안 · 자동 적용 안 함)."""
    t = str(text)
    if any(k in t for k in NOTICE_KW):
        return "동의서 고지"
    if re.search(r"\d", t) or any(k in t for k in TIMELINE_KW):
        return "타임라인"
    return "설명문"


class Dry2State:
    def __init__(self, kt, r1=None, r2=None, sites=None, dict_values=None):
        self.kt = kt
        self.r1 = {norm(w) for w in (r1 or [])}
        self.r2 = {norm(w) for w in (r2 or [])}
        self.sites = sites or {}                 # norm(부위 사전 표면) → canonical
        self.dict_values = dict_values or set()  # norm(등록 값) — SL 이 사전 값인지
        self.rec = {}                            # locator → {text, events[]}
        self.seglog = []                         # 토막마다 dict(아래 _log)
        self.t3_parens = []                      # (locator, text, inner, kind, ratio)
        self.solo_strict = Counter()
        self.solo_loose = Counter()
        self.solo_inner = Counter()
        self.solo_inner_texts = defaultdict(list)
        self.seg_contexts = defaultdict(list)


STATE = None


def ws_spans(s):
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", s)]


def member_offsets(gtext):
    """ADV_MEMBER_SPLIT 로 가른 멤버(비지 않은 것) 각각의 시작 글자 위치 — _split_base 의 members 순서와 같다."""
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


N1_FORMS = {"ᆷ", "음", "ㅁ"}
HEAD_NOUNS = {"현상", "느낌", "증상", "경우"}        # 발주서 N2 「~는 현상」「~는 느낌」「~해지는 증상」「~는 경우」
ARG_PARTICLES = {"JKS", "JKO", "JKB"}             # 앞 어절이 이 격조사로 끝나면 그 용언의 논항(절)
PRED_KIND_TAGS = KT.PRED_TAGS | {"VCP"}            # VCP 는 관형형(「일시적인」)·부사형만 — 종결·연결은 2차처럼 용언으로 안 본다


def word_tokens(toks, ws):
    """[(form, tag, a, b, 어절 번호)]"""
    return [(f, tg, a, b, next((wi for wi, x in enumerate(ws) if x[0] <= a < x[1]), -1)) for f, tg, a, b in toks]


def word_kind(ts):
    """어절 하나의 형태소 → (kind, info).
    kind: N1 · N1case(N1 + 격조사 — 이름 아님, 앞 논항) · ETM · ADV · CLAUSE · ARG(명사 + 격조사) · NOUN · OTHER
    info: {'end': 이름으로 쓸 글자 끝(N1) · 'conj': 접속 조사 경계 있음 · 'ending': 마지막 어미}"""
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
    vcp_only = has_pred and not any(t[1] in KT.PRED_TAGS for t in core[:ei])
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


def word_info(kt, text, r1):
    """멤버 문자열 → 어절마다 kind · N2 판정.
    → dict(sent, clause_words, mod_words(R1 목록 밖 수식어 어절), n1(어절 번호 → 이름 글자), kinds{wi: kind}, why{wi: 이유})."""
    text = str(text)
    toks = kt.tokens(text)
    ws = ws_spans(text)
    tw = word_tokens(toks, ws)
    bad = {w for w, _ in kt.anom.get(text, [])}
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
        wn = norm(w.strip("*'\"“”‘’.…`~!?,"))
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
            # 바로 앞 절 경계(다른 CLAUSE·ETM 수식어) 뒤의 논항만 — 멤버 안 앞쪽 아무 어절이나
            head = None
            if k == "ETM" and wi + 1 < len(ws):
                nx = [t for t in byw.get(wi + 1, []) if not t[1].startswith("S")]
                if nx:
                    head = nx[0]
                    # 의존명사 머리는 그 어절의 내용 형태소가 의존명사 하나일 때만(「수」「것」) — 「거상 → 거/NNB+상/XSN」 같은 분석은 의존명사 머리로 보지 않는다
                    if head[1] == "NNB" and any(t[1] in ("NNG", "NNP", "XSN", "XR") or t[1] in KT.PRED_TAGS for t in nx[1:]):
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
    return dict(sent=bool(clause), clause_words=[ws[i][2] for i in clause], mod_words=[ws[i][2] for i in mods], mod_wi=set(mods), n1=n1,
                kinds=kinds, why=why, ws=ws, tw=tw)


def sentence_info(kt, text, r1):
    """2차 호환: (문장꼴?, 절 어절들, [], {어절 번호: kind})."""
    wi_ = word_info(kt, text, r1)
    return wi_["sent"], wi_["clause_words"], [], wi_["kinds"]


def paren_kind(kt, inner, r1):
    toks = kt.tokens(inner)
    content = [t for t in toks if not (t[1].startswith("J") or t[1].startswith("E"))]
    if not content:
        return "empty", 0.0
    s = sum(1 for t in content if t[1] in KT.S_TAGS_T3)
    ratio = s / len(content)
    if ratio > 0.5:
        return "S", ratio
    if ratio == 0.5:
        return "tie", ratio
    if sentence_info(kt, inner, r1)[0]:
        return "sentence", ratio
    return "noun", ratio


NOUNISH = {"NNG", "NNP"}


def noun_units(toks, dict_values, rwords=frozenset(), words=None, n1=None, mods=None, out=None):
    """T1 — 형태소 → 명사 단위 [[글자, 어절 번호]].
    어절 표면이 R1·R2 말과 같으면 그 어절은 통째 한 단위(1차가 토큰 통째로 대던 것과 같은 자리 · 분석기가 「중등도」를 중등+도 로 나눠도).
    명사(NNG·NNP · 사전 값 SL)가 단위를 연다 · 같은 어절 안 XSN(뒤)·XPN(앞)은 그 명사에 붙인다 · XR 은 같은 어절 안 뒤에 XSN·명사가 오면 명사 꼴(「민감성」).
    → (units, dropped[(글자, 품사)], affix[], partial[(어절, 버린 형태소)]) — partial = 명사 단위가 있는 어절 안에서 조사·어미·기호 밖 형태소를 버린 자리(분석 확인 필요)."""
    units, dropped, affix, partial = [], [], [], []
    byw = {}
    for t in toks:
        byw.setdefault(t[4], []).append(t)
    for wi in sorted(byw):
        ts = byw[wi]
        if words is not None and 0 <= wi < len(words):
            wsurf = words[wi].strip("*'\"“”‘’.…`~!?")
            if norm(wsurf) in rwords:
                units.append([wsurf, wi])
                continue
        if n1 and wi in n1:                      # N1 — 명사형 어절은 통째(이름 = 어절 그대로 · 접속 조사·기호 뺌)
            units.append([n1[wi], wi])
            if out is not None:
                out.setdefault("n1_used", []).append(n1[wi])
            continue
        if mods and wi in mods:                  # N2 — 관형어·부사어 하나 = 수식어(R1 후보 · 새)
            if out is not None:
                out.setdefault("mods_removed", []).append(words[wi] if words else "")
            continue
        w_units, w_drop = [], []
        pend = ""
        prev_noun = False
        for i, t in enumerate(ts):
            f, tag = t[0], t[1]
            nxt = ts[i + 1][1] if i + 1 < len(ts) else None
            if tag in NOUNISH or (tag == "SL" and norm(f) in dict_values):
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


class Dry2AdverseUnits(V32.AdverseUnits32):

    def evaluate(self, text, src):
        row = super().evaluate(text, src)
        loc = src.get("locator")
        if self.mode == "create" and loc:
            STATE.rec[loc] = {"text": text, "events": [c["event"] for c in row["candidates"]]}
        return row

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

    def _canon7(self, core):
        """7차가 이 핵심어로 세웠을 이름(결정 fold 따라가기 · 사전이면 사전 값) — 기록용 키."""
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
        if key in self.ledger:
            return ("node", self.ledger[key]["canonical"])
        return ("node", core)

    def _apply_cores(self, groups, text, loc):
        kt = STATE.kt
        has_h = bool(HANGUL.search(str(text)))
        excl = {norm(w) for w in (CUR["kinds"].get("core_exclude") or [])}
        outer_text = ADV_PAREN.sub(" ", text)
        gtexts = [outer_text] + ADV_PAREN.findall(text)
        create = self.mode == "create" and loc
        for gi, g in enumerate(groups):
            if gi > 0 and not self._has_event(g):
                continue
            gtext = gtexts[gi] if gi < len(gtexts) else ""
            offs = member_offsets(gtext)
            dm = T4_DELIM.search(gtext)
            pk, pratio = (paren_kind(kt, gtext, STATE.r1) if gi > 0 else (None, None))
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
                WI = word_info(kt, txt, STATE.r1)
                sent, sent_words, ef_words, pred_w = WI["sent"], WI["clause_words"], [], WI["kinds"]
                bad_words = {w for w, _ in kt.anom.get(txt, [])}
                mt = kt.tokens(txt)
                ws = ws_spans(txt)
                mt_w = [(f, tg, a, b, next((wi for wi, x in enumerate(ws) if x[0] <= a < x[1]), -1)) for f, tg, a, b in mt]
                member_dict7 = [s_ for s_ in m["spans"] if s_["kind"] == "event"]
                mods_pos = [(txt.find(md["text"]), md) for md in m.get("modifiers", []) if norm(md["text"]) not in self.fallback]
                segs = self._seg_ranges(m, text)
                # 멤버 안 Kiwi 사전 사건 NNG(사건 없는 토막의 어절 안)
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
                    kd = [t for t in toks if t[1] in KT.NOUN_TAGS and norm(t[0]) in self.base_event_surface]
                    seg_info.append((sg, s0, s1, evs, wis, toks, kd))
                member_has_dict = bool(member_dict7) or any(si[6] for si in seg_info)
                new_spans, side, cores, left = [], [], [], []
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
                    k7 = self._canon7(core7)
                    seg_text = " ".join(ws[w][2] for w in sorted(wis))
                    rec = {"loc": loc, "text": text, "gi": gi, "member": txt, "segment": seg_text, "core7": core7, "k7": k7, "rules": [], "kind": None, "target": None,
                           "sentence_words": sent_words, "ef_words": ef_words, "mod_words_member": WI["mod_words"], "clause_why_member": [WI["why"][w] for w in sorted(WI["why"]) if w not in WI["mod_wi"]], "site": [], "dropped": [], "r1": [], "r2": [], "affix": [], "amb": [], "remainder_class": None, "paren_kind": pk, "paren_ratio": pratio}
                    outcome = None    # ('node'|'dict', core) | ('gone', why)
                    # ---- T3
                    if gi > 0 and pk == "S":
                        rec["rules"].append("T3")
                        outcome = ("gone", "T3")
                    # ---- T4
                    elif after_delim:
                        rec["rules"].append("T4")
                        outcome = ("gone", "T4")
                        rec["remainder_class"] = classify_remainder(txt)
                    else:
                        if gi > 0 and pk == "tie":
                            rec["amb"].append(f"T3: 괄호 안 기호·라틴·숫자 형태소가 정확히 절반(「{gtext}」) — 「위주」인지 애매 → 적용 안 함")
                        # ---- T2
                        if sent:
                            if kd:
                                rec["rules"].append("T2a")
                                outcome = ("dict", [t[0] for t in kd])
                                rec["kind"] = "T2a-capture"
                                rest = [ws[w][2] for w in sorted(wis)]
                                rec["remainder_class"] = classify_remainder(" ".join(rest))
                                rec["site"] = [t[0] for t in toks if (norm(t[0]) in STATE.sites or norm(t[0]) in STATE.r2) and t[1] in KT.NOUN_TAGS]
                            elif member_has_dict:
                                rec["rules"].append("T2a")
                                outcome = ("gone", "T2a-rest")
                                rec["remainder_class"] = classify_remainder(seg_text)
                                rec["site"] = [t[0] for t in toks if (norm(t[0]) in STATE.sites or norm(t[0]) in STATE.r2) and t[1] in KT.NOUN_TAGS]
                            else:
                                rec["rules"].append("T2b")
                                outcome = ("gone", "T2b")
                                units, dropped, affix, partial = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws], n1={w: WI["n1"][w] for w in wis if w in WI["n1"]})
                                rec["nouns"] = [u[0] for u in units]
                                rec["remainder_class"] = classify_remainder(txt)
                                rec["clause_why"] = [WI["why"][w] for w in sorted(WI["why"]) if w not in WI["mod_wi"]]
                        seg_bad_wi = [w for w in sorted(wis) if ws[w][2] in bad_words]
                        n1map = {w: WI["n1"][w] for w in sorted(wis) if w in WI["n1"]}
                        modset = {w for w in WI["mod_wi"] if w in wis}
                        anom_att = []
                        for w in seg_bad_wi:
                            # N1: 분석기 후보가 전부 이상 꼴인 어절은 통째 명사 — 단 1위 분석의 어절 끝이 조사(JC 뺌)·EC·ETM 이면 「붙음」 → 애매 그대로
                            core_t = [t for t in mt_w if t[4] == w]
                            while core_t and core_t[-1][1].startswith("S"):
                                core_t.pop()
                            if core_t and core_t[-1][1] == "JC":
                                core_t.pop()
                            last = core_t[-1] if core_t else None
                            if last is None or (last[1].startswith("J") or last[1] in ("EC", "ETM")):
                                anom_att.append(w)
                            else:
                                n1map[w] = txt[ws[w][0]:last[3]].strip("*'\"“”‘’.…`~!?,")
                                rec.setdefault("n1_anom", []).append(n1map[w])
                        pred_odd = [w for w in sorted(wis) if w not in n1map and w not in modset and w not in seg_bad_wi and WI["kinds"].get(w) in ("N1case", "N1part", "OTHER")
                                    and any(t[1] in KT.PRED_TAGS for t in mt_w if t[4] == w) and norm(ws[w][2].strip("*'\"“”‘’.…`~!?,")) not in (STATE.r1 | STATE.r2)]
                        if outcome is None and anom_att:
                            rec["rules"].append("T1")
                            outcome = ("gone", "ANOM")
                            rec["amb"].append(f"분석기: 어절 {', '.join('「' + ws[w][2] + '」' for w in anom_att)} 의 후보 {KT.TOP_N} 개가 전부 어절 안 이상 꼴({'; '.join(r for w_, r in kt.anom.get(txt, []) if w_ in [ws[w][2] for w in anom_att])}) · 1위 분석의 어절 끝이 조사·연결어미 — N1 통째 명사 적용 불가")
                        if outcome is None and pred_odd:
                            rec["rules"].append("T1")
                            outcome = ("gone", "T1-pred")
                            rec["amb"].append(f"T1·N1: 용언 어절 {', '.join('「' + ws[w][2] + '」(' + WI['kinds'][w] + ')' for w in pred_odd)} — 명사형(어절 끝 -ㅁ/-음)도 수식어도 절도 아님(조사가 붙은 명사형 등) — 적용 안 함")
                        if outcome is None:
                            # ---- T1 (+N1 명사형 어절 · N2 수식어 어절)
                            uo = {}
                            units, dropped, affix, partial = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws], n1=n1map, mods=modset, out=uo)
                            keepmods = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws], n1=n1map)[0]   # 수식어 떼기 전(T1·N1 차이만 보려고)
                            rec["dropped"], rec["affix"], rec["partial"] = dropped, affix, partial
                            rec["n1"] = uo.get("n1_used", [])
                            rec["r1_new"] = [x for x in uo.get("mods_removed", [])]
                            core_t1 = join_units(units)
                            if not units:
                                rec["rules"].append("T1")
                                outcome = ("gone", "T1-none")
                                rec["amb"].append(f"T1: 명사 없음({', '.join(f'{f}/{t}' for f, t in dropped) or '형태소 없음'}) — 사건 이름인지 애매")
                            else:
                                mw = {norm(x.strip("*'\"“”‘’.…`~!?,")) for x in rec["r1_new"]}
                                core7_nomod = " ".join(t for t in core7.split() if norm(t) not in mw)
                                if norm(join_units(keepmods)) != norm(core7) and norm(core_t1) != norm(core7_nomod):
                                    rec["rules"].append("N1" if rec["n1"] else "T1")
                                rec["units"] = [u[0] for u in units]
                                if partial:
                                    rec["amb"].append(f"T1: 명사 단위가 있는 어절 안에서 명사 아닌 형태소를 버림({'; '.join(w + ' → ' + ', '.join(f'{f}/{t}' for f, t in d) for w, d in partial)}) — 분석기 판정 확인 필요 · 적용 안 함")
                                    outcome = ("gone", "T1-partial")
                            if outcome is None:
                                u2, h2 = strip_r2(units, STATE.r2)
                                if h2:
                                    rec["rules"].append("R2")
                                    rec["r2"] = h2
                                    rec["site"] = h2
                                elif len(units) == 1 and norm(units[0][0]) in STATE.r2:
                                    rec["r2_alone"] = units[0][0]
                                u1, h1 = strip_r1(u2, STATE.r1)
                                if h1 or rec["r1_new"]:
                                    rec["rules"].append("R1")
                                    rec["r1"] = h1
                                core2 = join_units(u1)
                                if norm(core2) not in self.base_event_surface and any(norm(u[0]) in self.base_event_surface for u in u1) and len(u1) > 1:
                                    rec["amb"].append(f"사전 사건 「{next(u[0] for u in u1 if norm(u[0]) in self.base_event_surface)}」에 R1·R2 밖 명사가 붙음(「{core2}」) — 규칙 밖 → 노드로 둠")
                                outcome = ("node", [core2])
                    rec["kind"] = rec["kind"] or (outcome[0] if outcome[0] != "gone" else outcome[1])
                    # ---- 등록
                    if outcome[0] in ("node", "dict"):
                        rec["target"], rec["target_origin"] = [], []
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
                            rec["target_origin"].append(origin)
                            cores.append(core)
                            new_spans.append({"kind": "event", "canonical": canon, "text": core, "basis": "ledger_core" if origin == "ledger" else "core_exact"})
                            # 단독 출현(1차와 같은 정의 + T1 이 버린 내용 형태소)
                            if create and outcome[0] == "node":
                                other_strict = [p[2] for p in prs] + [f for f, t in rec["dropped"]] + [md["text"] for pos, md in mods_pos if s0 <= pos < s1 and md["class"] in CONTENT_MOD_CLASSES and norm(md["text"]) not in STATE.r1]
                                other_loose = [p[2] for p in prs] + [f for f, t in rec["dropped"]]
                                k = norm(canon)
                                if not other_strict:
                                    STATE.solo_strict[k] += 1
                                    if gi > 0:
                                        STATE.solo_inner[k] += 1
                                        STATE.solo_inner_texts[k].append(text)
                                if not other_loose:
                                    STATE.solo_loose[k] += 1
                                STATE.seg_contexts[k].append((loc, [core] + other_strict))
                    else:
                        m.setdefault("explanation", []).extend(us + [x[2] for x in prs])
                    if create:
                        STATE.seglog.append(rec)
                if side:
                    m["side"] = list(side)
                if cores:
                    m["core_tokens"] = cores
                m["spans"] = list(m["spans"]) + new_spans
                m["untouched"] = left
                if self.mode == "refer" and side:
                    m["untouched"] = left + side
        return groups
