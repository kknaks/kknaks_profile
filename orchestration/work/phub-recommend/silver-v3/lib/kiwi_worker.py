# -*- coding: utf-8 -*-
"""형태소 분석기 워커(V3.3-B) — `.venv-kiwi/bin/python lib/kiwi_worker.py` 로만 돈다(kiwipiepy 는 그 venv 에만 있다).

stdin  JSON {"registered": [사전 표면형 …], "texts": [문구 …], "top_n": 10}
stdout JSON {"version": kiwipiepy 판, "results": {문구: {"tokens": [[form, tag, start, end] …], "rank": 고른 후보 순위|null, "anom": [[어절, 이유] …]}}, "failed": [[값, 오류] …]}

규칙(드라이런 2차·3차 kiwi_t0.py 그대로): 사전 값 전부를 사용자 단어(NNG · 0.0)로 등록 → 후보 top_n 중 「어절 안 이상 꼴」(anomalies) 이 없는 가장 높은 점수의 분석을 고른다 ·
이상 꼴 없는 후보가 없으면 1위 분석 + anom 기록. 빌더(lib/analyzer.py)는 결과를 캐시(판 + 등록 사전 해시 + 문구)에 보존해 재실행이 venv 없이 같다.
"""
import json
import re
import sys

PRED_TAGS = {"VV", "VA", "VX", "XSV", "XSA"}
OPEN_WORD_TAGS = {"MM", "IC", "NR", "NP", "MAJ"}          # 어절 하나로 서는 품사(관형사·감탄사·수사·대명사·접속부사)


def base_tag(t):
    return t.split("-")[0]


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
                out.append([w, f"A1 {t[0]}/{tg}"])
            if tg == "MAG" and any(x[1] in ("NNG", "NNP", "XSN") for x in ts if x is not t):
                out.append([w, f"A7 {t[0]}/{tg}+명사"])
            if tg in ("NNG", "NNP", "XR") and nxt and nxt[1] in ("VV", "VA", "VX"):
                out.append([w, f"A2 {t[0]}/{tg}+{nxt[0]}/{nxt[1]}"])
            if tg.startswith("Z"):
                out.append([w, f"A3 {t[0]}/{tg}"])
            if tg.startswith("J") and nxt and nxt[1].startswith("E"):
                out.append([w, f"A3 {t[0]}/{tg}+{nxt[0]}/{nxt[1]}"])
            if tg in ("EC", "ETM", "EF") and any(not (x[1].startswith("J") or x[1].startswith("E") or x[1].startswith("S") or x[1] in PRED_TAGS or x[1] in ("VCP", "VCN", "EP")) for x in ts[i + 1:]):
                out.append([w, f"A4 {t[0]}/{tg}+…"])
            if tg.startswith("E") and len(t[0]) > 1 and "ᆨ" <= t[0][0] <= "ᇿ":
                out.append([w, f"A5 {t[0]}/{tg}"])
            if tg.startswith("J") and any(not (x[1].startswith("J") or x[1].startswith("E") or x[1].startswith("S")) for x in ts[i + 1:]):
                out.append([w, f"A6 {t[0]}/{tg}+…"])
    return out


def main():
    import kiwipiepy
    from kiwipiepy import Kiwi
    req = json.load(sys.stdin)
    top_n = int(req.get("top_n") or 10)
    kiwi = Kiwi()
    failed = []
    for v in req.get("registered") or []:
        try:
            kiwi.add_user_word(v, "NNG", 0.0)
        except Exception as ex:  # noqa: BLE001
            failed.append([v, str(ex)])
    results = {}
    for text in req.get("texts") or []:
        if not str(text).strip():
            results[text] = {"tokens": [], "rank": None, "anom": []}
            continue
        cands = kiwi.analyze(text, top_n=top_n)
        chosen, rank = None, None
        for i, (toks, score) in enumerate(cands):
            tt = [[t.form, base_tag(t.tag), t.start, t.start + t.len] for t in toks]
            if not anomalies(text, tt):
                chosen, rank = tt, i
                break
        anom = []
        if chosen is None:
            chosen = [[t.form, base_tag(t.tag), t.start, t.start + t.len] for t in cands[0][0]]
            anom = anomalies(text, chosen)
        results[text] = {"tokens": chosen, "rank": rank, "anom": anom}
    json.dump({"version": kiwipiepy.__version__, "top_n": top_n, "results": results, "failed": failed}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
