# -*- coding: utf-8 -*-
"""드라이런 2차 — T0(사전 값 통째 등록) · Kiwi 분석 도우미.

T0: 7차 실버가 실제로 쓰는 사전(ERD v3.2 사전 49 중 phrase_dictionary 를 뺀 48 · 승인 결정 반영 — 사건 43 = 40 + 3)의
canonical · synonym 전부를 Kiwi 사용자 단어(NNG)로 등록한다. adverse_event_type 의 origin=ledger 262 는 7차 실버 사전에
이미 없다(다시 세는 대상 노드라 등록하지 않는다). phrase_dictionary(원장 문구 558)는 분석 대상 문구 자체라 등록하지 않는다.
.venv-kiwi 인터프리터로만 돈다.
"""
import re
import unicodedata
from collections import OrderedDict

from kiwipiepy import Kiwi

from lib.util import norm

PRED_TAGS = {"VV", "VA", "VX", "XSV", "XSA"}          # 용언(·용언 파생 접미) — 문장꼴 판정의 앞 말
T2_END_TAGS = {"EC", "ETM", "ETN"}                    # 발주서 T2 어미
NOUN_TAGS = {"NNG", "NNP"}
S_TAGS_T3 = {"SL", "SN", "SW", "SP", "SS", "SSO", "SSC", "SE", "SO", "SB", "SH"}


TOP_N = 10
OPEN_WORD_TAGS = {"MM", "IC", "NR", "NP", "MAJ"}          # 어절 하나로 서는 품사(관형사·감탄사·수사·대명사·접속부사)


def anomalies(text, toks):
    """어절(공백 토큰) 안 이상 꼴 — 한국어 띄어쓰기상 한 어절 안에 올 수 없는 형태소 배열(분석기 오분석 신호).
    A1 관형사·감탄사·수사·대명사·접속부사가 다른 내용 형태소와 한 어절 · A2 명사·어근 바로 뒤 VV/VA/VX(파생 접미 XSV/XSA 없이)
    A3 조사 뒤 어미 · Z_ 꼴 · A4 EC/ETM/EF 뒤에 같은 어절 안 내용 형태소 · A5 받침 자모로 시작하는 두 글자 이상 어미(「ᆫ감」) · A6 조사 뒤 같은 어절 안 내용 형태소 · A7 일반 부사(MAG)가 명사와 한 어절."""
    out = []
    words = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", text)]
    for a, b, w in words:
        ts = [t for t in toks if a <= t[2] < b]
        content = [t for t in ts if not (t[1].startswith("J") or t[1].startswith("E") or t[1].startswith("S"))]
        for i, t in enumerate(ts):
            tg = t[1]
            nxt = ts[i + 1] if i + 1 < len(ts) else None
            if tg in OPEN_WORD_TAGS and len(content) > 1:
                out.append((w, f"A1 {t[0]}/{tg}"))
            if tg == "MAG" and any(x[1] in ("NNG", "NNP", "XSN") for x in ts if x is not t):
                out.append((w, f"A7 {t[0]}/{tg}+명사"))
            if tg in ("NNG", "NNP", "XR") and nxt and nxt[1] in ("VV", "VA", "VX"):
                out.append((w, f"A2 {t[0]}/{tg}+{nxt[0]}/{nxt[1]}"))
            if tg.startswith("Z"):
                out.append((w, f"A3 {t[0]}/{tg}"))
            if tg.startswith("J") and nxt and nxt[1].startswith("E"):
                out.append((w, f"A3 {t[0]}/{tg}+{nxt[0]}/{nxt[1]}"))
            if tg in ("EC", "ETM", "EF") and any(not (x[1].startswith("J") or x[1].startswith("E") or x[1].startswith("S") or x[1] in PRED_TAGS or x[1] in ("VCP", "VCN", "EP")) for x in ts[i + 1:]):
                out.append((w, f"A4 {t[0]}/{tg}+…"))
            if tg.startswith("E") and len(t[0]) > 1 and "\u11a8" <= t[0][0] <= "\u11ff":
                out.append((w, f"A5 {t[0]}/{tg}"))
            if tg.startswith("J") and any(not (x[1].startswith("J") or x[1].startswith("E") or x[1].startswith("S")) for x in ts[i + 1:]):
                out.append((w, f"A6 {t[0]}/{tg}+…"))
    return out


def base_tag(t):
    return t.split("-")[0]


def values_of(dj, skip=("phrase_dictionary",)):
    """[(dictionary, value)] — canonical + synonym 전부(중복 제거 · 원문 그대로)."""
    out = OrderedDict()
    for d in dj["dictionaries"]:
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
                if not v:
                    continue
                out.setdefault((d["name"], v), None)
    return list(out)


class KiwiT0:
    def __init__(self, dj):
        self.kiwi = Kiwi()
        self.values = values_of(dj)
        self.registered = OrderedDict()   # value → [dictionary...]
        self.failed = []                  # (dictionary, value, error)
        self.skipped = []                 # (dictionary, value, why) — 한글·라틴 글자가 없는 값
        for dn, v in self.values:
            if not re.search(r"[가-힣A-Za-z]", v):
                self.skipped.append((dn, v, "글자 없음(숫자·기호만)"))
                continue
            if v in self.registered:
                self.registered[v].append(dn)
                continue
            try:
                ok = self.kiwi.add_user_word(v, "NNG", 0.0)
                self.registered[v] = [dn]
                if not ok:
                    # 이미 같은 꼴·같은 품사가 있으면 False — 등록된 것으로 본다(사전 값 그대로)
                    pass
            except Exception as ex:  # noqa: BLE001
                self.failed.append((dn, v, str(ex)))
        self.cache = {}
        self.anom = {}    # text → [(어절, 이유)] — 이상 꼴 없는 후보가 없던 문자열
        self.rank = {}    # text → 고른 후보 순위(0 = 1위 · None = 없음)

    # ------------------------------------------------------------------
    def tokens(self, text):
        """[(form, tag(기본), start, end)] — Kiwi 형태소(원문 글자 범위). 후보 top_n 중 「어절 안 이상 꼴」(anomalies) 이 없는 가장 높은 점수의 분석.
        이상 꼴이 없는 후보가 없으면 1위 분석 · self.anom[text] 에 이상 어절을 남긴다."""
        text = str(text)
        if text in self.cache:
            return self.cache[text]
        cands = self.kiwi.analyze(text, top_n=TOP_N)
        chosen, rank = None, None
        for i, (toks, score) in enumerate(cands):
            tt = [(t.form, base_tag(t.tag), t.start, t.start + t.len) for t in toks]
            if not anomalies(text, tt):
                chosen, rank = tt, i
                break
        if chosen is None:
            chosen = [(t.form, base_tag(t.tag), t.start, t.start + t.len) for t in cands[0][0]]
            self.anom[text] = anomalies(text, chosen)
        self.rank[text] = rank
        self.cache[text] = chosen
        return chosen

    def split_check(self):
        """T0 등록 뒤에도 값 하나만 넣어 분석했을 때 형태소 하나로 안 나오는 값 [(value, dictionaries, 분석)]."""
        bad = []
        for v, dns in self.registered.items():
            toks = self.tokens(v)
            if len(toks) == 1 and norm(toks[0][0]) == norm(v):
                continue
            bad.append((v, dns, [(f, t) for f, t, _, _ in toks]))
        return bad

    def context_split(self, texts):
        """원장 문자열 안에서 등록 값이 나온 자리(앞 글자가 한글이 아닌 자리)를 Kiwi 가 쪼갰나 — 형태소 경계가 값 글자 범위 안쪽에 하나라도 있으면 쪼갬. [(value, text, 그 범위의 형태소)]."""
        vals = sorted((v for v in self.registered if len(v) >= 2 and re.search(r"[가-힣]", v)), key=len, reverse=True)
        out = []
        for text in texts:
            s = unicodedata.normalize("NFC", str(text))
            toks = None
            for v in vals:
                for m in re.finditer(re.escape(v), s):
                    a, b = m.start(), m.end()
                    if a > 0 and re.match(r"[가-힣]", s[a - 1]):
                        continue
                    if toks is None:
                        toks = self.tokens(s)
                    inside = [x for x in toks if x[3] > a and x[2] < b]
                    if any(a < x[2] < b or a < x[3] < b for x in inside):
                        out.append((v, s, [(x[0], x[1]) for x in inside]))
        return out
