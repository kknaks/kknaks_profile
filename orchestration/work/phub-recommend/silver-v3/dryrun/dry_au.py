# -*- coding: utf-8 -*-
"""드라이런 전용 — lib.v32.AdverseUnits32 를 감싼다(lib 는 고치지 않는다 · 이 프로세스 안에서만 run_adverse32 가 이 클래스를 쓰게 바꿔 끼운다).

규칙(사용자 승인 2026-11-05 · silver-dryrun-brief.md):
  R2 구조·부위 말 → 부위 칸: 사전 사건이 없는 토막(노드 핵심어가 서는 곳)에서 R2 말 뒤에 핵심어 토큰(미등록·대체 핵심어)이 더 있으면 그 말을 떼어 부위로(드라이런 임시 site · 단위 칸에는 넣지 않고 기록만).
  R1 정도·경과·빈도 수식어 → R15 속성: 핵심어 토큰열의 맨 앞·맨 뒤에 있는 R1 말을 뗀다(핵심어가 하나 이상 남을 때만).
  둘 다 꺼 두면 _apply_cores 는 lib 원본과 같은 결과(드라이런이 0 단계에서 7차 노드 260 과 대조한다).
기록: REC(자리마다 사건 칸 · 토막 내용) · R1/R2 뗀 기록 · 애매 기록 · 단독 출현(엄격/느슨).
"""
from collections import Counter, defaultdict

from lib import v32 as V32
from lib.util import norm

HANGUL = V32.HANGUL
LATIN = V32.LATIN
CUR = V32.CUR
CONTENT_MOD_CLASSES = {"misc", "condition", "connector"}   # 엄격 단독: 이 부류 수식어는 내용으로 남긴다(R1 의 정도·경과·빈도 부류가 아님)


class DryState:
    def __init__(self, r1=None, r2=None):
        self.r1 = {norm(w) for w in (r1 or [])}
        self.r2 = {norm(w) for w in (r2 or [])}
        self.rec = {}                     # locator → {text, events[]}
        self.r1_hits = []                 # (word, edge, core_before, core_after, locator, text)
        self.r2_hits = []                 # (word, core_before, core_after, locator, text)
        self.r1_middle = []               # (word, core, locator, text)
        self.r2_before_pred = []          # (word, core, predicates, locator, text)
        self.r2_alone = []                # (word, core, locator, text)
        self.solo_strict = Counter()      # norm(core) → 토막 자리 수
        self.solo_loose = Counter()
        self.solo_inner = Counter()        # 단독 자리 중 괄호 안 묶음
        self.solo_inner_texts = defaultdict(list)
        self.solo_strict_locs = defaultdict(list)
        self.seg_contexts = defaultdict(list)   # norm(core) → [(locator, 토막 내용 strict)]


STATE = DryState()


def _match(tok, words, tk):
    """tok 이 words(정규화) 의 말이면 그 말 — 통째 일치 또는 조사·어미를 뗀 어간 일치."""
    n = norm(tok)
    if n in words:
        return n
    if tk is not None:
        st = tk.strip(tok, lambda s: norm(s) in words)
        if st and norm(st[0]) in words:
            return norm(st[0])
    return None


class DryAdverseUnits(V32.AdverseUnits32):

    def evaluate(self, text, src):
        row = super().evaluate(text, src)
        loc = src.get("locator")
        if self.mode == "create" and loc:
            STATE.rec[loc] = {"text": text, "events": [c["event"] for c in row["candidates"]]}
        return row

    def _rec(self, lst, item):
        if self.mode == "create":
            lst.append(item)

    def _seg_ranges(self, m, text):
        """_segments 와 같은 토막 · 각 토막의 글자 범위(수식어 자리 배정용)."""
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
        has_h = bool(HANGUL.search(str(text)))
        excl = {norm(w) for w in (CUR["kinds"].get("core_exclude") or [])}
        tk = CUR.get("tok")
        for gi, g in enumerate(groups):
            if gi > 0 and not self._has_event(g):
                continue
            for m in g["members"]:
                moved = [u for u in m["untouched"] if (has_h and V32.script_of(u) == "L") or norm(u) in excl or not (HANGUL.search(u) or LATIN.search(u))]
                if moved:
                    m.setdefault("explanation", []).extend(moved)
                    m["untouched"] = [u for u in m["untouched"] if u not in moved]
                if not m["untouched"] and (any(s_["kind"] == "event" for s_ in m["spans"]) or gi > 0):
                    continue
                if not m["untouched"] and not any(p[1] in ("fb", "pr") for p in self._pieces(m, text)):
                    continue
                txt = m["text"]
                mods_pos = [(txt.find(md["text"]), md) for md in m.get("modifiers", []) if norm(md["text"]) not in self.fallback]
                new_spans, side, cores, left = [], [], [], []
                for sg, s0, s1 in self._seg_ranges(m, text):
                    evs = [x for x in sg if x[1] == "ev"]
                    us = [x[2] for x in sg if x[1] == "u"]
                    if evs:
                        side += us
                        continue
                    seq = [x for x in sg if x[1] in ("u", "fb")]
                    prs = [x for x in sg if x[1] == "pr"]
                    seq0 = " ".join(x[2] for x in seq)
                    stripped = set()
                    # ---- R2(앞 붙은 구조·부위 말 → 부위)
                    if STATE.r2 and seq:
                        keep = []
                        for i, x in enumerate(seq):
                            w = _match(x[2], STATE.r2, tk)
                            rest = seq[i + 1:]
                            if w and rest:
                                self._rec(STATE.r2_hits, (w, seq0, None, loc, text))
                                stripped.add(id(x))
                                continue
                            keep.append(x)
                        seq = keep
                        if seq:
                            w = _match(seq[-1][2], STATE.r2, tk)
                            if w:
                                after_pr = [p[2] for p in prs if p[0] > seq[-1][0]]
                                core_ = " ".join(x[2] for x in seq)
                                if after_pr:
                                    self._rec(STATE.r2_before_pred, (w, core_, after_pr, loc, text))
                                elif len(seq) == 1:
                                    self._rec(STATE.r2_alone, (w, core_, loc, text))
                    # ---- R1(앞뒤 수식어 → R15 속성)
                    if STATE.r1 and seq:
                        before = " ".join(x[2] for x in seq)
                        changed = True
                        while changed and len(seq) > 1:
                            changed = False
                            w = _match(seq[0][2], STATE.r1, tk)
                            if w:
                                self._rec(STATE.r1_hits, (w, "front", before, None, loc, text))
                                stripped.add(id(seq[0]))
                                seq = seq[1:]
                                changed = True
                                continue
                            w = _match(seq[-1][2], STATE.r1, tk)
                            if w and len(seq) > 1:
                                self._rec(STATE.r1_hits, (w, "back", before, None, loc, text))
                                stripped.add(id(seq[-1]))
                                seq = seq[:-1]
                                changed = True
                        for x in seq[1:-1]:
                            w = _match(x[2], STATE.r1, tk)
                            if w:
                                self._rec(STATE.r1_middle, (w, " ".join(y[2] for y in seq), loc, text))
                    toks = [x[2] for x in seq] or ([x[2] for x in prs] if gi == 0 else [])
                    if not toks or (not us and gi > 0):
                        continue
                    core = " ".join(toks)
                    # 뗀 기록에 결과 핵심어를 채운다
                    for lst in ((STATE.r2_hits, STATE.r1_hits) if self.mode == "create" else ()):
                        for k in range(len(lst) - 1, -1, -1):
                            r = lst[k]
                            if r[-2] != loc or r[-1] != text:
                                break
                            if lst is STATE.r2_hits and r[2] is None:
                                lst[k] = (r[0], r[1], core, r[3], r[4])
                            elif lst is STATE.r1_hits and r[3] is None:
                                lst[k] = (r[0], r[1], r[2], core, r[4], r[5])
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
                    # ---- 단독 출현(이 토막의 내용이 핵심어 하나뿐인가) — create 일 때만 센다
                    if self.mode == "create" and loc:
                        other_strict = [p[2] for p in prs if seq] + [md["text"] for pos, md in mods_pos if s0 <= pos < s1 and md["class"] in CONTENT_MOD_CLASSES and norm(md["text"]) not in STATE.r1]
                        other_loose = [p[2] for p in prs if seq]
                        k = norm(canon)
                        if not other_strict:
                            STATE.solo_strict[k] += 1
                            if gi > 0:
                                STATE.solo_inner[k] += 1
                                STATE.solo_inner_texts[k].append(text)
                            if len(STATE.solo_strict_locs[k]) < 5:
                                STATE.solo_strict_locs[k].append(loc)
                        if not other_loose:
                            STATE.solo_loose[k] += 1
                        STATE.seg_contexts[k].append((loc, [core] + other_strict))
                if side:
                    m["side"] = list(side)
                if cores:
                    m["core_tokens"] = cores
                m["spans"] = list(m["spans"]) + new_spans
                m["untouched"] = left
                if self.mode == "refer" and side:
                    m["untouched"] = left + side
        return groups
