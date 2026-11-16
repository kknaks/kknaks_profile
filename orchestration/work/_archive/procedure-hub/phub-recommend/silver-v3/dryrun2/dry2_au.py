# -*- coding: utf-8 -*-
"""드라이런 2차 전용 — lib.v32.AdverseUnits32 를 감싼다(lib 는 고치지 않는다 · 이 프로세스 안에서만 바꿔 끼운다).

7차와 같은 것: 묶음(바깥 · 괄호 안) · 멤버(구분자) · 사전 값 통째 일치(span) · 수식어(stopwords 138 · 패턴) · 접속 조사 토막 · 결정(exclude · fold).
2차에서 바꾼 것: 사전 사건이 없는 토막(노드 핵심어가 서는 곳)의 핵심어를 Kiwi 형태소로 다시 뽑는다(발주서 silver-dryrun2-brief.md T0~T4 · R1·R2).
  (셈 순서 T3 → T4 → T2 → T1 → R2 → R1)
  T3  괄호 안 묶음이 기호·라틴·숫자(SL·SN·SW·SP …) 위주(형태소 과반) → 사건 후보 아님(R15 속성/문헌 후보) · 정확히 절반 = 애매(적용 안 함)
  T4  같은 묶음에서 「--」「—」「:」 뒤 멤버의 토막 → 설명(사건 후보 아님)
  T2  멤버에 용언(VV·VA·VX·XSV·XSA)+어미(EC·ETM·ETN)가 있으면 문장꼴(R1 목록의 관형형 「심한·경미한 …」 낱말은 판정에서 뺀다 — R1 수식어)
        (a) 토막 안에 사전 사건 NNG 가 있으면 그 사건 · 멤버에 사전 사건이 있으면 사건 없는 토막은 서술(분류는 제안만)
        (b) 멤버에 사전 사건이 없으면 「문장꼴 — 사용자」(노드 후보 아님)
  T1  핵심어 = 명사(NNG·NNP · SL 은 사전 값일 때만)만. 명사에 붙은 XSN(뒤)·XPN(앞)은 그 명사의 일부로 둔다(접사 단독은 핵심어 아님).
      명사가 하나도 없으면 노드가 서지 않는다 — 용언+(-ㅁ/-음, Kiwi EF) 한 낱말(「따가움」)·부사(「울퉁불퉁」)처럼 T2 어미 목록 밖이면 애매 — 사용자.
  R2  명사열에서 R2 말(형태소를 이어 붙인 꼴 포함 · 띄어쓰기 없이 붙은 말에도) 뒤에 명사가 더 있으면 그 말을 부위로 뗀다.
  R1  명사열 맨 앞·맨 뒤 R1 말(「이상」 뺌)을 뗀다(명사가 하나 이상 남을 때만).
기록: 토막마다 7차 핵심어 → 2차 결과(규칙 · 대상) · T 표 · 단독 출현.
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


def is_pred_end(toks, i):
    """toks[i] 가 용언 형태소이고 뒤로 이어지는 어미(선어말 EP 건너뜀) 중 T2 어미가 있나 → 'T2' · EF 만 → 'EF' · 없음 → None."""
    if toks[i][1] not in KT.PRED_TAGS:
        return None
    j = i + 1
    while j < len(toks) and (toks[j][1] in KT.PRED_TAGS or toks[j][1] == "EP" or toks[j][1].startswith("E")):
        if toks[j][1] in KT.T2_END_TAGS:
            return "T2"
        if toks[j][1] == "EF":
            return "EF"
        j += 1
    return None


def sentence_info(kt, text, r1):
    """멤버 문자열 → (문장꼴?, T2 용언 낱말들, EF 꼴 낱말들, {어절 번호: 'T2'|'EF'}). R1 목록 낱말(관형형 수식어)·분석기 이상 어절은 뺀다."""
    toks = kt.tokens(text)
    ws = ws_spans(text)
    bad = {w for w, _ in kt.anom.get(str(text), [])}
    sent_words, ef_words, per = [], [], {}
    for i, t in enumerate(toks):
        k = is_pred_end(toks, i)
        if not k:
            continue
        wi = next((j for j, x in enumerate(ws) if x[0] <= t[2] < x[1]), -1)
        w = ws[wi][2] if wi >= 0 else t[0]
        if norm(w.strip("*'\"“”‘’.…`~!?")) in r1 or w in bad:
            continue
        if k == "T2":
            if per.get(wi) != "T2":
                sent_words.append(w)
            if per.get(wi) == "EF":
                ef_words.remove(w)
            per[wi] = "T2"
        elif wi not in per:
            per[wi] = "EF"
            ef_words.append(w)
    return bool(sent_words), sent_words, ef_words, per


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


def noun_units(toks, dict_values, rwords=frozenset(), words=None):
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
                sent, sent_words, ef_words, pred_w = sentence_info(kt, txt, STATE.r1)
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
                           "sentence_words": sent_words, "ef_words": ef_words, "site": [], "dropped": [], "r1": [], "r2": [], "affix": [], "amb": [], "remainder_class": None, "paren_kind": pk, "paren_ratio": pratio}
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
                                units, dropped, affix, partial = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws])
                                rec["nouns"] = [u[0] for u in units]
                                rec["remainder_class"] = classify_remainder(txt)
                        seg_words = [ws[w][2] for w in sorted(wis)]
                        seg_bad = [w for w in seg_words if w in bad_words]
                        seg_ef = [ws[w][2] for w in sorted(wis) if pred_w.get(w) == "EF"]
                        if outcome is None and seg_bad:
                            rec["rules"].append("T1")
                            outcome = ("gone", "ANOM")
                            rec["amb"].append(f"분석기: 어절 {', '.join('「' + w + '」' for w in seg_bad)} 의 후보 {KT.TOP_N} 개가 전부 어절 안 이상 꼴({'; '.join(r for w, r in kt.anom.get(txt, []) if w in seg_bad)}) — T1 적용 불가")
                        if outcome is None and seg_ef:
                            units, dropped, affix, partial = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws])
                            rec["rules"].append("T1")
                            rec["nouns"] = [u[0] for u in units]
                            outcome = ("gone", "T1-EF")
                            rec["amb"].append(f"T1·T2: 용언+-ㅁ/-음 꼴 「{' '.join(seg_ef)}」 — Kiwi 가 EF(종결 어미)로 봄 · 명사(T1) 아님 · T2 어미 목록(EC·ETM·ETN) 밖 — 명사형 사건 이름인지 애매")
                        if outcome is None:
                            # ---- T1
                            units, dropped, affix, partial = noun_units(toks, STATE.dict_values, STATE.r1 | STATE.r2, [w[2] for w in ws])
                            rec["dropped"], rec["affix"], rec["partial"] = dropped, affix, partial
                            core_t1 = join_units(units)
                            if not units:
                                rec["rules"].append("T1")
                                outcome = ("gone", "T1-none")
                                rec["amb"].append(f"T1: 명사 없음({', '.join(f'{f}/{t}' for f, t in dropped) or '형태소 없음'}) — 사건 이름인지 애매")
                            else:
                                if norm(core_t1) != norm(core7):
                                    rec["rules"].append("T1")
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
                                if h1:
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
