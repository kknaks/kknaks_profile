# -*- coding: utf-8 -*-
"""부작용 수식어 수집 · 표준 점수 초안(modifier-scale-brief.md · 2026-11-06 · 읽기 전용 조사).

입력(읽기만): silver-v3/out/(8차 산출) · silver-v3/lib(8차 빌더 — 문구 자리별 parsed 를 다시 얻으려고 import 만) ·
             bronze/phub-ledger/(원장 3판) · erd-v3.3.json(수식어 138 · course 사전) · silver-v3/out/gate/batch6.json(R1 후보 20).
산출(쓰기): modifier-scale/modifier-inventory.json · modifier-scale/modifier-scale-draft.md

왜 빌더를 다시 부르나: out/dictionaries.json 의 문구 사전 항목 parsed 는 그 항목의 **첫 원문**(raw_variants[0])에서만 나온다
(같은 정규화형으로 묶인 다른 원문 — 「경미한 불편감」 — 의 수식어는 항목에 없다). 2,285 자리마다 수식어를 세려면 자리마다 parsed 가 필요해서
8차 빌더(pipeline.run)를 그대로 돌리며 AdverseUnits31.evaluate 를 감싸 자리별 결과를 받아 둔다. silver-v3/ 에는 아무것도 쓰지 않는다
(분석기 캐시는 임시 폴더 복사본 · 바이트코드 끔 · out 인자는 쓰이지 않음). 재현 검사: 항목 543 의 첫 원문 parsed 가 out 과 전부 같아야 한다.

실행: python3 modifier-scale/collect.py   (작업 폴더 phub-recommend 어디서든)
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, OrderedDict, defaultdict

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
SV = os.path.join(W, "silver-v3")
OUT = os.path.join(SV, "out")
LEDGER = os.path.join(W, "bronze", "phub-ledger")
sys.path.insert(0, SV)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- 1. 빌더 재실행 + 자리별 캡처
def capture():
    from lib import pipeline, v32 as V32, adverse31 as A31
    from lib.adverse33 import analyzer_texts, word_info
    tmp = tempfile.mkdtemp(prefix="modscale-")
    cache = os.path.join(tmp, "kiwi-cache.json")
    shutil.copy(os.path.join(SV, "cache", "kiwi-cache.json"), cache)
    runs = []
    orig_run = V32.run_v32

    def run_wrap(*a, **k):
        runs.append({"analyzer": k.get("analyzer") is not None, "rows": {}})
        return orig_run(*a, **k)

    V32.run_v32 = run_wrap
    pipeline.V32.run_v32 = run_wrap
    orig_ev = A31.AdverseUnits31.evaluate

    def ser(groups):
        out = []
        for g in groups:
            mem = []
            for m in g["members"]:
                spans = []
                for s in m.get("spans", []):
                    spans.append([s.get("kind"), s.get("canonical"), s.get("text")] if isinstance(s, dict) else list(s))
                mem.append({"text": m.get("text"), "spans": spans,
                            "modifiers": [{"text": md.get("text"), "class": md.get("class"), "by": md.get("by")} for md in m.get("modifiers", [])]})
            out.append({"where": g.get("where"), "members": mem})
        return out

    def ev_wrap(self, text, src):
        cls_split = type(self).split
        cap = {}

        def sp(t_, *a, **k):
            g = cls_split(self, t_, *a, **k)
            cap.setdefault("g", g)
            return g
        self.split = sp
        try:
            row = orig_ev(self, text, src)
        finally:
            del self.split
        if runs and src.get("locator") and src.get("kind") == "safety_phrase":
            runs[-1]["rows"][src["locator"]] = {"text": text, "parsed": row["parsed"], "groups": ser(cap.get("g") or []),
                                                "candidates": [{"event": c["event"], "courses": c["courses"], "members": c["members"]} for c in row["candidates"]]}
        return row

    A31.AdverseUnits31.evaluate = ev_wrap
    ns = argparse.Namespace(bronze=LEDGER, step1=os.path.join(W, "step1-products.json"), erd=os.path.join(W, "erd-v3.3.json"), dict=os.path.join(W, "erd-v3.3-dictionaries.json"),
                            colmap=os.path.join(W, "erd-v3.3-column-map.md"), tuples=os.path.join(W, "erd-v3.3-tuples.json"), tuples_prev=os.path.join(W, "erd-v3.2-tuples.json"),
                            kiwi_cache=cache, kiwi_python=os.path.join(SV, ".venv-kiwi", "bin", "python"), decisions=os.path.join(SV, "decisions"), out=os.path.join(tmp, "out-unused"))
    S = pipeline.run(ns)
    A31.AdverseUnits31.evaluate = orig_ev
    final = [r for r in runs if r["analyzer"]][-1]["rows"]
    # 분석기 관형어·부사어(게이트 6 R1 후보와 같은 셈 — word_info · 단 R1 목록 걸름 없이 r1=∅)
    AT = S.ctx["AU"].A["AT"]
    an = AT.an
    for lc, r in final.items():
        mods = []
        for part in analyzer_texts(r["text"])[1:]:
            try:
                wi = word_info(an, part, frozenset())
            except Exception:  # noqa: BLE001
                continue
            if wi["sent"]:
                continue
            mods.extend(wi["mod_words"])
        r["analyzer_mod_words"] = mods
    # 게이트 6 R1 후보 셈과 같은 텍스트 집합(complication_name 포함) — R1 후보 표 대조용
    from lib.v32 import CUR
    comp_mods = defaultdict(list)
    for ax, kind, f, p, lc, text, mod in (CUR.get("texts") or []):
        if ax != "adverse" or kind != "complication_name":
            continue
        for part in analyzer_texts(text)[1:]:
            try:
                wi = word_info(an, part, frozenset())
            except Exception:  # noqa: BLE001
                continue
            if not wi["sent"]:
                for w in wi["mod_words"]:
                    comp_mods[strip(w)].append((lc, text))
    shutil.rmtree(tmp, ignore_errors=True)
    return final, comp_mods


STRIP_CHARS = "*'\"“”‘’.…`~!?,()[]{}:;·"


def strip(w):
    return str(w).strip(STRIP_CHARS).strip()


def norm(s):
    return re.sub(r"\s+", "", str(s)).lower()


# ---------------------------------------------------------------- 2. 눈금(원장 근거) — 값은 전부 원장에서 읽는다
AX = ["빈도", "정도", "시점", "경과", "조건", "양상", "기타"]
ST_DIRECT = "원장 같은 말"          # 원장 눈금 이름·원장 말이 그대로
ST_DRAFT = "초안(뜻) — 사용자 확인"   # 원장 눈금에 뜻으로 맞춤(원장이 말-눈금 연결을 적지 않음)
ST_AMB = "애매 — 사용자"
ST_BOUND = "경계 미정 — 사용자"
ST_NOM = "눈금 없음(이름 축)"         # 조건·양상·기타 — 서열 점수를 주지 않는다
ST_INT = "강조어 — 단독 점수 없음"
ST_LABEL = "축 이름말 — 단계 없음"

DEGREE = [("경미", "mild", 1), ("중등도", "moderate", 2), ("중증", "severe", 3), ("위급", "critical", 4)]
FREQ = [("매우 흔함", 5), ("흔함", 4), ("(uncommon 칸)", None), ("드묾", 2), ("극히 드묾", 1)]
TIMING = [("시술 중", 1, r"(시술|주입|도포|천자|주사)\s*(중|시)"), ("즉시·직후", 2, r"즉시|직후|당일"), ("수시간", 3, r"수\s*시간|\d+\s*시간"),
          ("수일", 4, r"수\s*일|\d+\s*일"), ("수주", 5, r"수\s*주|\d+\s*주"), ("수개월", 6, r"수\s*개월|\d+\s*개월"), ("수년", 7, r"수\s*년|\d+\s*년")]
UNIT_STAGE = {"시간": "수시간", "일": "수일", "주": "수주", "개월": "수개월", "년": "수년"}
TIMING_SCORE = {n: sc for n, sc, _ in TIMING}
FREQ_SCORE = dict(FREQ)
DEG_SCORE = {k: sc for k, _, sc in DEGREE}


def E(axis, stage=None, score=None, status=ST_NOM, basis=""):
    return OrderedDict([("axis", axis), ("stage", stage), ("score", score), ("status", status), ("basis", basis)])


B_SEV = "complications.json severity_levels"
B_FREQ = "complications.json incidence 문구의 빈도 말"
B_COURSE = "course 사전(DIC · 동의어)"
B_ONSET = "complications.json onset 문구의 시점 말"

# 말 → 축 매핑(이 표가 초안의 판단 전부 · 표 밖의 말은 아래 기본 규칙). 근거는 원장 문장/칸 · 「뜻」은 원장이 말-눈금 연결을 적지 않은 자리.
CLS = {
    # --- 정도(severity_levels 4단)
    "경미한": [E("정도", "경미", 1, ST_DIRECT, B_SEV + ".mild 「경미 — 자연 소실, 경과 관찰」 — 등급 이름과 같은 말")],
    "경미": [E("정도", "경미", 1, ST_DIRECT, B_SEV + ".mild — 등급 이름과 같은 말")],
    "중등도": [E("정도", "중등도", 2, ST_DIRECT, B_SEV + ".moderate 「중등도 — 치료 필요, 클리닉 방문」 — 등급 이름과 같은 말")],
    "중증": [E("정도", "중증", 3, ST_DIRECT, B_SEV + ".severe 「중증 — 즉시 치료, 후유증 가능」 — 등급 이름과 같은 말")],
    "가벼운": [E("정도", "경미", 1, ST_DRAFT, B_SEV + ".mild — 뜻(가벼운 ≈ 경미) · 원장이 이 말을 등급에 잇지 않음")],
    "약간의": [E("정도", "경미", 1, ST_DRAFT, B_SEV + ".mild — 뜻(약간 ≈ 경미)")],
    "약간": [E("정도", "경미", 1, ST_DRAFT, B_SEV + ".mild — 뜻(약간 ≈ 경미)")],
    "미약한": [E("정도", "경미", 1, ST_DRAFT, B_SEV + ".mild — 뜻(미약 ≈ 경미)")],
    "미미": [E("정도", "경미", 1, ST_DRAFT, B_SEV + ".mild — 뜻")],
    "덜": [E("정도", None, None, ST_AMB, "비교(덜 ~) — 기준이 문구 밖")],
    "최소": [E("정도", "경미?", None, ST_AMB, "「최소 부종 · 최소 부작용 · 최소 반응성」 — 경미인지 「거의 없음」(빈도)인지 원장이 가르지 않음"), E("빈도", None, None, ST_AMB, "")],
    "미세한": [E("정도", "경미?", None, ST_AMB, "「미세한 부종」은 정도 · 「미세한 출혈점 · 딱지」는 크기(양상) — 한 말이 두 뜻"), E("양상", "크기", None, ST_NOM, "크기(작음)")],
    "미세": [E("양상", "크기", None, ST_NOM, "「미세 결절 · 미세출혈 · 미세 각질」 — 크기"), E("정도", "경미?", None, ST_AMB, "ERD 수식어 목록 class degree — 정도로 쓴 자리 확인 필요")],
    "심한": [E("정도", "중등도~위급?", None, ST_AMB, B_SEV + " — 「심한」을 moderate/severe/critical 중 어디에 둘지 원장 정의(관리 수준)로는 못 가름")],
    "심하게": [E("정도", "중등도~위급?", None, ST_AMB, "「심한」과 같음")],
    "심각한": [E("정도", "중증~위급?", None, ST_AMB, B_SEV + " — 「심각한 전신 알레르기 반응」(아나필락시스 · complications 9/9 critical) 한 자리뿐")],
    "강한": [E("정도", None, None, ST_AMB, "「강한 근육 수축감」 — 감각 세기 · 관리 수준 정의(4단)와 잇는 원장 말 없음")],
    "과도한": [E("정도", None, None, ST_AMB, "사건 앞(「과도한 부종 · 과도한 이물반응」)은 정도 · 원장 4단 어디인지 없음"), E("조건", "시술 조건", None, ST_NOM, "「과도한 에너지 · 과도한 열 작용 시」 — 원인 조건")],
    "과도": [E("정도", None, None, ST_AMB, "「표정근 과도 이완」 — 정도"), E("조건", "시술 조건", None, ST_NOM, "")],
    "과다": [E("조건", "시술 조건", None, ST_NOM, "「과다 주입 시 · 과다 에너지」"), E("정도", None, None, ST_AMB, "「색소침착 과다」 — 사건 이름의 일부(과색소)일 수도")],
    "과한": [E("조건", "시술 조건", None, ST_NOM, "「과한 ~」 설명문")],
    "광범위": [E("양상", "범위", None, ST_NOM, "범위(넓게)"), E("정도", None, None, ST_AMB, "ERD class degree — 범위를 정도로 셀지 사용자")],
    "광범위한": [E("양상", "범위", None, ST_NOM, "「광범위한 근육 마비」"), E("정도", None, None, ST_AMB, "")],
    "치명적": [E("정도", "위급?", None, ST_AMB, B_SEV + ".critical 「응급 대응, 비가역적 손상 가능」 — 「치명적」과 같은 말인지 원장이 적지 않음")],
    "현저히": [E("정도", None, None, ST_INT, "강조어(현저히 낮음)")],
    "매우": [E("정도", None, None, ST_INT, "ERD class degree · 실제 자리는 「매우 드물음 · 매우 안전한 · 매우 작음 · 매우 낮은」 — 뒤 말의 강조"), E("빈도", None, None, ST_INT, "「매우 드묾」 표현 쪽에서 셈")],
    "극히": [E("빈도", None, None, ST_INT, "ERD class degree · 실제 자리는 전부 「극히 드묾/드물게/드문」 — 표현 「극히 드묾」 쪽에서 셈")],
    "깊은": [E("조건", "시술 조건", None, ST_NOM, "「깊은 필링 · 깊은 모노폴라」"), E("양상", "피부톤", None, ST_NOM, "「깊은 피부톤」 — 사람 조건(피부형)에 가까움")],
    "얕은": [E("양상", "깊이", None, ST_NOM, "「얕은 결절」 — 위치 깊이")],
    "낮은": [E("빈도", None, None, ST_AMB, "「낮은 발생률 · 매우 낮은」 — 단계 이름 아님(수치 함께 적힌 자리는 수치로)"), E("조건", "피부톤", None, ST_NOM, "「낮은 피부톤」")],
    "높은": [E("조건", "시술 조건", None, ST_NOM, "「너무 높은 에너지 · 높은 에너지」 — R1 후보")],
    "낮음": [E("빈도", None, None, ST_AMB, "「PIH 낮음」 류 — 단계 이름 아님")],
    "높음": [E("빈도", None, None, ST_AMB, "「50% 발생률로 높음」 — 수치와 함께")],
    "작음": [E("빈도", None, None, ST_AMB, "「위험이 매우 작음」 — 비교 서술")],
    "최저": [E("빈도", None, None, ST_AMB, "「QS 제품 중 최저 수준」 — 비교 서술")],
    "부적절한": [E("조건", "시술 조건", None, ST_NOM, "「부적절한 에너지 설정 시 · 부적절한 쿨링 시」 — 원인 조건")],
    "부적절": [E("조건", "시술 조건", None, ST_NOM, "")],
    "부정확한": [E("조건", "시술 조건", None, ST_NOM, "「부정확한 시술 시」 — R1 후보")],
    "부당한": [E("기타", None, None, ST_NOM, "「부당한 거상(코그 이탈)」 — 사건 이름 일부 · R1 후보")],
    "비정상적": [E("기타", None, None, ST_NOM, "")],
    "비슷한": [E("기타", "비교", None, ST_NOM, "「운동 후와 비슷한 · 감기 비슷한」 — 비교")],
    "정도": [E("기타", "어림", None, ST_NOM, "「1~2일 정도」 어림말 · 「재생 정도」 명사")],
    "예상보다": [E("기타", "비교", None, ST_NOM, "")],
    "완전": [E("정도", None, None, ST_AMB, "")],
    "급격한": [E("시점", None, None, ST_AMB, "속도 — 시점 단계 아님")],
    "고농도": [E("조건", "시술 조건", None, ST_NOM, "")], "장시간": [E("조건", "시술 조건", None, ST_NOM, "「고농도/장시간」 — 노출 조건")],
    "고용량": [E("조건", "시술 조건", None, ST_NOM, "")], "과량": [E("조건", "시술 조건", None, ST_NOM, "")], "극소량": [E("조건", "시술 조건", None, ST_NOM, "")],
    "너무": [E("기타", None, None, ST_INT, "「너무 높은 에너지」 — 조건 강조")],
    "과하게": [E("기타", None, None, ST_NOM, "설명문 서술")],
    # --- 빈도(낱말)
    "드물게": [E("빈도", "드묾", 2, ST_DIRECT, B_FREQ + " 「드묾」(complications 7/6 · 9/9) — 같은 말의 활용")],
    "드묾": [E("빈도", "드묾", 2, ST_DIRECT, B_FREQ + " 「드묾」")],
    "드물음": [E("빈도", "드묾", 2, ST_DIRECT, B_FREQ + " 「드묾」 — 표기 변형")],
    "드문": [E("빈도", "드묾", 2, ST_DIRECT, B_FREQ + " 「드묾」 — 활용")],
    "드물지만": [E("빈도", "드묾", 2, ST_DIRECT, B_FREQ + " 「드물지만」(complications 2/3 · 9/10)")],
    "희귀": [E("빈도", "드묾", 2, ST_DRAFT, "뜻(희귀 ≈ 드묾) — 원장 incidence 에 「희귀」 없음")],
    "극드문": [E("빈도", "극히 드묾", 1, ST_DRAFT, B_FREQ + " 「극히 드묾」 — 줄임꼴")],
    "흔함": [E("빈도", "흔함", 4, ST_DIRECT, B_FREQ + " 「흔함」")],
    "필발": [E("빈도", "매우 흔함", 5, ST_DIRECT, B_FREQ + " 「매우 흔함 (턱밑 임상 ~87%, 거의 필발)」(complications 9/0) — 원장이 같은 칸에 함께 씀")],
    "거의": [E("빈도", None, None, ST_INT, "「거의 필발」(매우 흔함) · 「거의 없음」(드묾 쪽) — 뒤 말이 정함 · 표현 쪽에서 셈")],
    "대부분": [E("경과", None, None, ST_AMB, "phrase 자리는 전부 「대부분 호전 · 대부분 회복됨 · 대부분 수 시간 내 사라짐」 — 회복 비율(경과) · 발생 빈도 아님"),
             E("빈도", "매우 흔함?", None, ST_AMB, B_FREQ + " — complications 에서는 「대부분 (일시적)」이 incidence 칸에 있음(발생 쪽)")],
    "주로": [E("양상", "유형 비율", None, ST_NOM, "「주로 cystic형, 드물게 sclerosing」 — 유형 분포 · 사건 발생 빈도 아님")],
    "발생률": [E("빈도", None, None, ST_LABEL, "")], "발생빈도": [E("빈도", None, None, ST_LABEL, "")],
    # --- 시점
    "직후": [E("시점", "즉시·직후", 2, ST_DIRECT, B_ONSET + " 「직후」(예 「시술 직후~수 시간」)")],
    "즉시": [E("시점", "즉시·직후", 2, ST_DIRECT, B_ONSET + " 「즉시」")],
    "즉각적": [E("시점", "즉시·직후", 2, ST_DRAFT, B_ONSET + " 「즉시」 — 뜻")],
    "수일": [E("시점", "수일", 4, ST_DIRECT, B_ONSET + " 「수일」")],
    "수시간": [E("시점", "수시간", 3, ST_DIRECT, B_ONSET + " 「수시간」")],
    "중": [E("시점", "시술 중", 1, ST_DIRECT, B_ONSET + " 「시술 중」 — 「시술 중 약간의 불편감」"), E("조건", "때", None, ST_NOM, "ERD class condition(「~ 중」)")],
    "시": [E("조건", "때", None, ST_NOM, "「~ 시」(「부적절한 설정 시」) — 원인 조건 · 「시술 시」는 시점 1 과 겹침")],
    "후": [E("시점", None, None, ST_AMB, "「시술 후」 — 구간을 말하지 않음(직후~수개월 어디든) · 원장 onset 에 「시술 후 수일~1개월」처럼 뒤 말이 단계")],
    "초기": [E("시점", None, None, ST_AMB, "「초기 부종 · 초기 과교정 · 초기 사용시」 — 원장 onset 「주입 초기」(9/7)는 시술 중 · 여기는 시술 뒤 초기라 단계 미정")],
    "내": [E("기타", "기간 표지", None, ST_NOM, "「1~2일 내 호전 · 24시간 내 소실」 — 앞 수치의 기간 표지")],
    "시간": [E("기타", None, None, ST_NOM, "「시간 지나면 · 수 시간 내」 — 서술 일부(수 시간은 기간)")],
    "만성": [E("경과", "지속?", None, ST_AMB, B_COURSE + " — 「만성」은 경과 사전에 없음(지속/영구 어느 쪽인지 · dictionary_add 는 사용자)")],
    "원래": [E("기타", None, None, ST_NOM, "「원래 위치에서 이동」 — 위치 서술 · 시점 아님")],
    "아직": [E("기타", None, None, ST_NOM, "「연구가 아직 충분하지 않음」 — 설명문")],
    "호전": [E("경과", "일시?", None, ST_AMB, B_COURSE + " — 「~ 내 호전」은 일시를 함의하나 원장 경과 칸이 아님(경과 동의어 아님)")],
    "소실": [E("경과", "일시?", None, ST_AMB, B_COURSE + " — 「24시간 내 소실 · 수개월 내 소실」")],
    "회복": [E("경과", "일시?", None, ST_AMB, "")], "사라짐": [E("경과", "일시?", None, ST_AMB, "")], "지나면": [E("기타", None, None, ST_NOM, "")],
    "일시적인": [E("경과", "일시", None, ST_AMB, B_COURSE + " 「일시 ← 일시적」 — ERD v3.3 §수식어: 「일시적인」은 경과 동의어가 아니라 시간 수식어(동의어 추가는 dictionary_add)")],
    "일시적으로": [E("경과", "일시", None, ST_AMB, "같음")],
    "임시적": [E("경과", "일시?", None, ST_AMB, B_COURSE + " — 「임시적 색소침착」 · 경과 동의어 아님")],
    "임시": [E("경과", "일시?", None, ST_AMB, "「임시 색소탈실」 · analyzer R1 목록")],
    "장기적": [E("경과", "지속?", None, ST_AMB, "「장기적 색소이상」 · 경과 동의어 아님")],
    "장기간": [E("경과", "지속?", None, ST_AMB, "「장기간 홍조」 · 경과 동의어 아님")],
    "지속적인": [E("경과", "지속", None, ST_AMB, B_COURSE + " 「지속 ← 지속적」 — 「지속적인」 꼴은 동의어에 없음 · R1 후보")],
    "연장된": [E("경과", "지속?", None, ST_AMB, "「연장된 부종(1주)」 · R1 후보")],
    "20년간": [E("기타", None, None, ST_NOM, "「20년간 치명적 부작용 보고 없음」 — 보고 기간 · 사건 시점 아님")],
    # --- 조건(이름 축)
    **{w: [E("조건", "때·원인", None, ST_NOM, "ERD class condition")] for w in ["시술", "반복", "주입", "주사", "사용", "투여", "도포", "치료", "설정", "에너지", "노출", "누르면", "경우", "따라", "관리가", "저온", "극저온"]},
    "특히": [E("조건", "강조", None, ST_NOM, "「특히 ~ 피부에서」 — 조건 강조")],
    "민감성": [E("조건", "사람 조건", None, ST_NOM, "「민감성 피부의 과도한 자극반응」")],
    "어두운": [E("조건", "사람 조건", None, ST_NOM, "「특히 어두운 피부」 — 피부형 · R1 후보")],
    # --- 양상
    "국소": [E("양상", "범위", None, ST_NOM, "「국소 발적 · 국소 홍반」")],
    "전신": [E("양상", "범위", None, ST_NOM, "「전신 알레르기 반응」 — 범위(부위 칸이 아닌 구조 말로 남음)")],
    "확산": [E("양상", "범위", None, ST_NOM, "")],
    "따뜻한": [E("양상", "감각", None, ST_NOM, "「따뜻한 감각」 — R1 후보")],
    "따가운": [E("양상", "감각", None, ST_NOM, "「따가운 감각」 — R1 후보")],
    "묘한": [E("양상", "감각", None, ST_NOM, "「묘한 따끔거림」 — R1 후보")],
    "불균일한": [E("양상", "모양", None, ST_NOM, "「불균일한 생착」 — R1 후보")],
    "불규칙한": [E("양상", "모양·주기", None, ST_NOM, "「불규칙한 출혈」 — R1 후보")],
    "만져지는": [E("양상", "촉감", None, ST_NOM, "「만져지는 결절」 — R1 후보")],
    "비후성": [E("양상", "형태", None, ST_NOM, "「비후성 반흔」")],
    "표면": [E("양상", "깊이", None, ST_NOM, "「피부 표면이 울퉁불퉁」")],
    # --- 기타(관형어지만 사건 수식 아님 · R1 후보)
    "안전한": [E("기타", None, None, ST_NOM, "「매우 안전한 시술」 — 시술 수식 · 사건 수식 아님 · R1 후보")],
    "불만족스러운": [E("기타", None, None, ST_NOM, "「불만족스러운 결과」 — 사건 이름 일부 · R1 후보")],
    "주입된": [E("기타", None, None, ST_NOM, "「주입된 지방의 ~」 — 물질 수식 · R1 후보")],
    "제한된": [E("기타", None, None, ST_NOM, "「제한된 가동범위」 — 사건 이름 일부 · R1 후보")],
    "씹는": [E("기타", None, None, ST_NOM, "「씹는 힘 감소」 — 사건 이름 일부 · R1 후보")],
}
SIDE_NOTE = "부위·구조·사건 말(분해 뒤 남은 명사) — 수식어 아님"
MISC_NOTE = "문법·서술·사건 말 일부(ERD class misc)"
# 설명문·서술 칸(explanation · predicate)에서 수식 말로 집는 낱말(그 밖의 명사·용어는 집지 않는다 — 이 목록이 판단의 전부)
EXTRA_PICK = {"필발", "희귀", "흔함", "극드문", "치명적", "현저히", "낮음", "높음", "작음", "최저", "중증", "심각한", "높은", "과한", "너무", "덜", "극소량", "과량",
              "고농도", "장시간", "고용량", "심하게", "과하게", "연장된", "만져지는", "불만족스러운", "어두운", "부정확한", "부당한", "안전한", "따가운", "씹는", "확산", "사라짐",
              "회복", "지나면", "부적절", "부적절한"}

# 빈도 표현(낱말 둘 이상) — 원문에서 찾는다
FREQ_EXPR = [
    ("극히 드묾", r"극히\s*드(?:물|묾|문)", "극히 드묾", 1, ST_DIRECT, B_FREQ + " 「극히 드묾 (<0.01%)」(complications 7/1)"),
    ("매우 드묾", r"매우\s*드(?:물|묾|문)", "극히 드묾?", None, ST_AMB, "「매우 드물음 · 매우 드문」 — 원장 incidence 에 「매우 드묾」 없음 · 극히 드묾과 같은지 원장이 말하지 않음"),
    ("매우 흔함", r"매우\s*흔", "매우 흔함", 5, ST_DIRECT, B_FREQ + " 「매우 흔함」"),
    ("거의 필발", r"거의\s*필발", "매우 흔함", 5, ST_DIRECT, B_FREQ + " 「매우 흔함 (… 거의 필발)」(9/0)"),
    ("거의 없음", r"거의\s*없", "극히 드묾?", None, ST_AMB, "「알레르기·거부반응이 거의 없음」 — 단계 이름 아님"),
    ("낮은 발생률", r"낮은\s*발생률|낮음", None, None, ST_AMB, "「1% 미만의 낮은 발생률 · ~10% 가능의 매우 낮은 발생률」 — 같은 말이 1% 미만과 ~10% 에 함께 쓰임"),
    ("N% 미만·이하·이내", r"\d+(?:\.\d+)?\s*%\s*(?:미만|이하|이내)", None, None, ST_BOUND, "수치 상한 — 단계 경계가 정해지면 기계 매핑"),
]

# ---------------------------------------------------------------- 3. 원장 눈금 근거 셈
def ledger_basis():
    L = {f: load(os.path.join(LEDGER, f)) for f in ["complications.json", "pih-risk.json", "patient-education.json", "consent-checklist.json"]}
    comp = L["complications.json"]
    rows = []
    for i, cat in enumerate(comp["categories"]):
        for j, c in enumerate(cat["complications"]):
            rows.append({"loc": f"{i}/{j}", "name": c.get("name"), "severity": c.get("severity"), "incidence": c.get("incidence"), "onset": c.get("onset"), "duration": c.get("duration")})
    # 빈도 말 ↔ 수치 짝: complications incidence 한 칸에 빈도 말과 %가 함께 있는 자리 (+ patient-education common_concerns 답 · consent 고지)
    FW = [("매우 흔함", r"매우\s*흔"), ("흔함", r"(?<!매우 )(?<!가장 )(?<!이보다 )흔(?:함|한|히)"), ("가장 흔한", r"가장\s*흔한"), ("극히 드묾", r"극히\s*드(?:물|묾|문)"), ("드묾", r"(?<!극히 )드(?:물|묾|문)"),
          ("대부분·거의 전례", r"대부분|거의\s*(?:전례|모든|보편|필발)|사실상\s*전|거의\s*전례")]
    NUM = re.compile(r"[<>~]?\s*\d+(?:\.\d+)?(?:\s*[-~]\s*\d+(?:\.\d+)?)?\s*%|수\s*%")
    pairs = []
    texts = [("complications.json:categories[].complications[].incidence@" + r["loc"], r["incidence"]) for r in rows if r["incidence"]]
    for i, cat in enumerate(L["patient-education.json"].get("categories") or []):
        for j, cc in enumerate(cat.get("common_concerns") or []):
            texts.append((f"patient-education.json:categories[].common_concerns[].a@{i}/{j}", cc.get("a")))
    for i, cat in enumerate(L["consent-checklist.json"].get("categories") or []):
        for j, t in enumerate(cat.get("mandatory_disclosures") or []):
            texts.append((f"consent-checklist.json:categories[].mandatory_disclosures[]@{i}/{j}", t))
    for loc_, t in texts:
        if not isinstance(t, str):
            continue
        words = [lab for lab, rx in FW if re.search(rx, t)]
        nums = [m.group(0).replace(" ", "") for m in NUM.finditer(t)]
        if words and nums:
            pairs.append({"locator": loc_, "words": words, "numbers": nums, "text": t[:140]})
    # 빈도 말만 있는 incidence 칸(수치 없음)
    verbal_only = Counter()
    for r in rows:
        t = r["incidence"] or ""
        if not NUM.search(t):
            for lab, rx in FW:
                if re.search(rx, t):
                    verbal_only[lab] += 1
    numeric_only = sum(1 for r in rows if r["incidence"] and NUM.search(r["incidence"]) and not any(re.search(rx, r["incidence"]) for _, rx in FW))
    # 시점 말 셈(complications onset 65)
    onset_counts = Counter()
    for r in rows:
        for name, sc, rx in TIMING:
            if r["onset"] and re.search(rx, r["onset"]):
                onset_counts[name] += 1
    sev_counts = Counter(r["severity"] for r in rows)
    return {"complications": rows, "severity_levels": comp["severity_levels"], "severity_counts": dict(sev_counts),
            "pih_risk_levels": L["pih-risk.json"].get("risk_levels"), "freq_number_pairs": pairs, "freq_verbal_only": dict(verbal_only), "incidence_numeric_only": numeric_only,
            "onset_counts": dict(onset_counts)}


def pih_band(pct, levels):
    """참고만 — pih-risk risk_levels 수치 띠(원장의 유일한 수치 눈금 · PIH 전용)."""
    out = []
    for k, v in levels.items():
        m = re.match(r"\s*<\s*([\d.]+)%", v)
        if m and pct < float(m.group(1)):
            out.append(k)
            continue
        m = re.match(r"\s*>\s*([\d.]+)%", v)
        if m and pct > float(m.group(1)):
            out.append(k)
            continue
        m = re.match(r"\s*([\d.]+)-([\d.]+)%", v)
        if m and float(m.group(1)) <= pct <= float(m.group(2)):
            out.append(k)
    return out


# ---------------------------------------------------------------- 4. 수집
def path_freq(locator):
    m = re.search(r"safety\.(\w+)\[\]", locator)
    k = m.group(1) if m else None
    return {"common_adverse_effects": "common", "common_side_effects": "common", "serious_adverse_effects": "serious"}.get(k, k)


def next_token_event(text, word, event_spans):
    """원문에서 word 바로 뒤 어절이 사건 말로 시작하면 그 사건(정준값)."""
    i = text.find(word)
    if i < 0:
        return None
    rest = text[i + len(word):].lstrip()
    tok = re.split(r"[\s,·/()]", rest, maxsplit=1)[0] if rest else ""
    for ev_text, canon in sorted(event_spans, key=lambda x: -len(x[0])):
        if ev_text and (tok.startswith(ev_text) or rest.startswith(ev_text)):
            return canon
    return None


def collect(final, entries):
    occs = []
    for e in entries:
        for lc, llc in zip(e["locators"], e["ledger_locators"]):
            r = final[lc]
            ev_spans = [(s[2], s[1]) for g in r["groups"] for m in g["members"] for s in m["spans"] if s[0] == "event"]
            cand_events = [c["event"] for c in r["candidates"]] or [s[1] for s in ev_spans]
            hits = []
            fields_of = defaultdict(set)
            for k, v in r["parsed"].items():
                if isinstance(v, list):
                    for x in v:
                        if isinstance(x, str):
                            fields_of[strip(x)].add(k)

            def add(word, source, cls=None, by=None, canonical=None, member=None):
                w = strip(word)
                if not w:
                    return
                m_ev = [s[1] for s in (member or {}).get("spans", []) if s[0] == "event"] if member else []
                direct = next_token_event(member["text"] if member else r["text"], w, [(s[2], s[1]) for s in member["spans"] if s[0] == "event"] if member else ev_spans)
                if direct:
                    evs, att = [direct], "바로 뒤 사건"
                elif m_ev:
                    evs, att = m_ev, "같은 멤버"
                else:
                    evs, att = cand_events, "문구 전체"
                hits.append(OrderedDict([("word", w), ("source", source), ("class", cls), ("by", by), ("canonical", canonical), ("events", evs), ("attach", att),
                                         ("fields_now", sorted(fields_of.get(w, set())))]))
            for g in r["groups"]:
                for m in g["members"]:
                    for md in m["modifiers"]:
                        add(md["text"], "parsed." + md["class"], md["class"], md["by"], None, m)
                    for s in m["spans"]:
                        if s[0] == "course":
                            add(s[2], "parsed.courses", "course", "dict", s[1], m)
                        elif s[0] == "qualifier":
                            add(s[2], "parsed.qualifiers", "qualifier", "dict", s[1], m)
            for w in r["parsed"].get("side") or []:
                add(w, "parsed.side")
            for w in r.get("analyzer_mod_words") or []:
                add(w, "analyzer_mod")
            for f in ("explanation", "predicate"):
                for w in r["parsed"].get(f) or []:
                    if strip(w) in EXTRA_PICK:
                        add(w, "parsed." + f)
            exprs = []
            for lab, rx, stage, score, st, basis in FREQ_EXPR:
                for mm in re.finditer(rx, r["text"]):
                    exprs.append(lab)
            for lab in dedupe_list(exprs):
                hits.append(OrderedDict([("word", lab + "(표현)"), ("source", "text_expr"), ("class", "frequency_expr"), ("by", "regex"), ("canonical", None), ("events", cand_events), ("attach", "문구 전체"), ("fields_now", [])]))
            occs.append(OrderedDict([("locator", lc), ("ledger_locator", llc), ("phrase_id", e["id"]), ("status", e["status"]), ("frequency_key", path_freq(lc)), ("text", r["text"]),
                                     ("events", cand_events), ("hits", hits)]))
    return occs


def dedupe_list(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


# ---------------------------------------------------------------- 5. 말 → 축
R15_ATTR = {"degree": "degree_text", "timing": "timing_text", "incidence": "incidence_text", "condition": "condition_text", "course": "course", "qualifier": "끝 단위 qualifier 칸(엣지 아님)"}


def classify(word, info, stop_cls, course_syn, basis):
    if word in CLS:
        return [OrderedDict(x) for x in CLS[word]]
    w0 = word.replace("(표현)", "")
    for lab, rx, stage, score, st, b in FREQ_EXPR:
        if word == lab + "(표현)":
            return [E("빈도", stage, score, st, b)]
    if "course" in info["classes"]:
        canon = info["canonicals"][0]
        return [E("경과", canon, None, ST_DIRECT, B_COURSE + f" 「{canon}」 ← 「{w0}」 (경과는 이름 축 · 서열 점수는 사용자)")]
    if "qualifier" in info["classes"]:
        return [E("기타", "물질·기전", None, ST_NOM, "adverse_qualifier 사전(튜플 칸) — 눈금 아님")]
    mp = re.fullmatch(r"(\d+(?:\.\d+)?)(?:[-~](\d+(?:\.\d+)?))?%", w0)
    if mp:
        bands = dedupe_list(b for x in mp.groups() if x for b in pih_band(float(x), basis["pih_risk_levels"]))
        return [E("빈도", "수치 " + w0, None, ST_BOUND, f"원장 수치 · 단계 경계 없음 · 참고: pih-risk risk_levels 띠 = {'~'.join(bands) or '—'}(PIH 전용)")]
    m = re.fullmatch(r"\d+(?:[-~]\d+)?(시간|일|주|개월|년)(?:간|째|내|이내|이상|후|이후|정도|후에)?", w0)
    if m:
        st = UNIT_STAGE[m.group(1)]
        return [E("시점", st, TIMING_SCORE[st], ST_DRAFT, B_ONSET + f" 「{st}」 — 수치의 단위로 단계 · 시점(발현)인지 기간(지속)인지 문구가 가르지 않음")]
    if re.fullmatch(r"\d+(?:\.\d+)?(mL|ml|cc|mm|cm|도|U|단위).*", w0):
        return [E("조건", "용량·치수", None, ST_NOM, "ERD 패턴 condition")]
    if stop_cls.get(w0) == "condition":
        return [E("조건", "때·원인", None, ST_NOM, "ERD class condition")]
    if stop_cls.get(w0) in ("misc", "connector"):
        return [E("기타", None, None, ST_NOM, MISC_NOTE)]
    if info["sources"].keys() <= {"parsed.side"}:
        return [E("기타", None, None, ST_NOM, SIDE_NOTE)]
    return [E("기타", None, None, ST_AMB, "분류 표 밖 — 사용자")]


# ---------------------------------------------------------------- 6. R15 엣지 영향(참고 · 적용 아님)
def edge_impact(occs, inv, basis):
    rows = [json.loads(l) for l in open(os.path.join(OUT, "relations", "R15.jsonl"), encoding="utf-8")]
    adv = {}
    for l in open(os.path.join(OUT, "entities", "adverse_effect.jsonl"), encoding="utf-8"):
        a = json.loads(l)
        adv[a["id"]] = (a["attrs"].get("event") or [{}])[0].get("value")
    mods = {}
    for l in open(os.path.join(OUT, "entities", "modality.jsonl"), encoding="utf-8"):
        m = json.loads(l)
        mods[m["id"]] = (m["attrs"].get("code") or [{}])[0].get("value")
    by_ll = {o["ledger_locator"]: o for o in occs}
    by_l = {o["locator"]: o for o in occs}
    comp = {r["loc"]: r for r in basis["complications"]}
    fam = {}
    for r in rows:
        if r["from"]["type"] == "modality":
            fam[f"R15:{mods.get(r['from']['id'])}→{r['to']['id']}"] = r

    def val(r, k):
        a = r["attrs"].get(k)
        return a.get("value") if isinstance(a, dict) else None

    def inh_sev(r, depth=0):
        if val(r, "severity"):
            v = val(r, "severity")
            return v[0] if isinstance(v, list) else v
        for i in val(r, "inheritance") or []:
            if i["attr"] != "severity" or not i.get("ref"):
                continue
            ref = i["ref"]
            if ref.startswith("complications.json"):
                return comp.get(ref.split("@")[1], {}).get("severity")
            if ref.startswith("R15:") and depth < 3 and ref in fam:
                return inh_sev(fam[ref], depth + 1)
        return None

    def stage_of(word, axis):
        for x in inv[word]["axes"]:
            if x["axis"] == axis and x["score"] is not None and x["status"] in (ST_DIRECT, ST_DRAFT):
                return x["stage"], x["score"], x["status"]
        return None

    FREQ_CLASS = {"common": ("흔함", 4, ST_DRAFT)}
    res = Counter()
    deg_cooc = defaultdict(Counter)
    freq_src = Counter()
    deg_src = Counter()
    unmatched_event = 0
    for r in rows:
        ev = adv.get(r["to"]["id"])
        sp = val(r, "source_phrases") or []
        occ_here = []
        for l in (r["attrs"].get("source_phrases") or {}).get("derived_from") or []:
            o = by_ll.get(l) or by_l.get(l)
            if o and o["phrase_id"] in sp and o not in occ_here:
                occ_here.append(o)
        hits = [h for o in occ_here for h in o["hits"] if ev in h["events"]]
        if occ_here and not any(ev in o["events"] for o in occ_here):
            unmatched_event += 1
        f_st, d_st = set(), set()
        f_from, d_from = set(), set()
        fc = val(r, "frequency_class")
        fcs = fc if isinstance(fc, list) else ([fc] if fc else [])
        for k in fcs:
            if k in FREQ_CLASS:
                f_st.add(FREQ_CLASS[k][0])
                f_from.add("frequency_class=common")
        if "uncommon" in fcs:
            res["freq_class_uncommon(위치 애매)"] += 1
        for h in hits:
            s = stage_of(h["word"], "빈도")
            if s:
                f_st.add(s[0])
                f_from.add("문구 빈도 말")
            s = stage_of(h["word"], "정도")
            if s:
                d_st.add(s[0])
                d_from.add("문구 정도 말")
                deg_cooc[h["word"]][inh_sev(r) or "없음"] += 1
            for x in inv[h["word"]]["axes"]:
                if x["axis"] == "정도" and x["status"] == ST_AMB:
                    deg_cooc[h["word"]][inh_sev(r) or "없음"] += 1
        inc = val(r, "incidence")
        if isinstance(inc, str):
            for lab, rx, stage, score, st, b in FREQ_EXPR:
                if score and re.search(rx, inc):
                    f_st.add(stage)
                    f_from.add("complications incidence 말")
            for w in ("드묾", "드물지만", "흔함"):
                if w in inc and not re.search(r"(극히|매우)\s*" + w[:2], inc):
                    f_st.add(CLS[w][0]["stage"])
                    f_from.add("complications incidence 말")
            if not f_from & {"complications incidence 말"} and re.search(r"\d\s*%", inc):
                res["incidence_numeric_only(경계 미정)"] += 1
        if val(r, "severity"):
            d_st.add("원장 severity")
            d_from.add("complications severity(이미 값)")
        if f_st:
            res["freq_any"] += 1
            if f_from - {"frequency_class=common"}:
                res["freq_any_without_common_class"] += 1
            for s_ in f_from:
                freq_src[s_] += 1
            if len(f_st) > 1:
                res["freq_conflict"] += 1
        if d_st:
            res["deg_any"] += 1
            for s_ in d_from:
                deg_src[s_] += 1
            if "원장 severity" not in d_st:
                res["deg_new_from_phrase"] += 1
        if inh_sev(r) and not val(r, "severity"):
            res["deg_inherited_ref(상속 참조 · 이미 있음)"] += 1
    res["edges"] = len(rows)
    res["edges_with_phrase"] = sum(1 for r in rows if val(r, "source_phrases"))
    res["phrase_edges_event_not_in_occurrence"] = unmatched_event
    return dict(res), dict(freq_src), dict(deg_src), {w: dict(c) for w, c in deg_cooc.items()}


# ---------------------------------------------------------------- 7. 본체
def main():
    final, comp_mods = capture()
    dicts = {d["name"]: d for d in load(os.path.join(OUT, "dictionaries.json"))["dictionaries"]}
    entries = dicts["phrase_dictionary"]["entries"]
    # 재현 검사 — 항목 첫 원문 parsed 가 out 과 같은가
    F = ["degree", "incidence", "timing", "condition", "misc", "side", "connector", "predicate", "explanation", "grammar"]
    repro_ok = 0
    for e in entries:
        first = next(l for l in e["locators"] if final[l]["text"] == e["raw_variants"][0])
        if all(final[first]["parsed"].get(f, []) == e["parsed"].get(f, []) for f in F):
            repro_ok += 1
    assert repro_ok == len(entries), f"재현 실패 {repro_ok}/{len(entries)}"
    assert sum(len(e["locators"]) for e in entries) == len(final) == 2285
    erd = load(os.path.join(W, "erd-v3.3.json"))
    stop = erd["tuple_rules"]["adverse"]["adverse_stopwords"]
    stop_cls = {w["word"]: w["class"] for w in stop["words"]}
    course_syn = {}
    for e in dicts["course"]["entries"]:
        course_syn[e["canonical"]] = e["canonical"]
        for s in e["synonyms"]:
            course_syn[s["value"]] = e["canonical"]
    basis = ledger_basis()
    occs = collect(final, entries)
    # R1 후보 20(게이트 6)
    b6 = load(os.path.join(OUT, "gate", "batch6.json"))
    r1 = [x for x in b6 if x["id"] == "r1-candidates"][0]["subitems"]
    r1_words = {s["word"]: {"gate_id": s["id"], "gate_n": s["n"], "gate_locators": len(s["locators"]), "gate_example": s["evidence"][0]["text"] if s.get("evidence") else None} for s in r1}
    slots = load(os.path.join(OUT, "gate", "batch6-page-slots.json"))
    r1_slots = [s for s in slots["slots"] if "R1" in json.dumps(s, ensure_ascii=False)[:400]] if isinstance(slots.get("slots"), list) else []
    # 말별 모음
    inv = OrderedDict()
    for o in occs:
        seen = set()
        for h in o["hits"]:
            w = h["word"]
            d = inv.setdefault(w, {"locs": set(), "sources": Counter(), "classes": set(), "by": Counter(), "canonicals": [], "examples": [], "events": Counter(), "attach": Counter(),
                                   "fields_now": Counter(), "freq_keys": Counter(), "statuses": Counter()})
            d["sources"][h["source"]] += 1
            if h["class"]:
                d["classes"].add(h["class"])
            if h["by"]:
                d["by"][h["by"]] += 1
            if h["canonical"] and h["canonical"] not in d["canonicals"]:
                d["canonicals"].append(h["canonical"])
            for f in h["fields_now"]:
                d["fields_now"][f] += 1
            if w in seen:
                continue
            seen.add(w)
            d["locs"].add(o["locator"])
            d["attach"][h["attach"]] += 1
            for ev in dedupe_list(h["events"]):
                d["events"][ev] += 1
            d["freq_keys"][o["frequency_key"]] += 1
            d["statuses"][o["status"]] += 1
            if o["text"] not in d["examples"] and len(d["examples"]) < 3:
                d["examples"].append(o["text"])
    words = OrderedDict()
    for w, d in sorted(inv.items(), key=lambda kv: (-len(kv[1]["locs"]), kv[0])):
        info = {"classes": d["classes"], "canonicals": d["canonicals"], "sources": d["sources"]}
        axes = classify(w, info, stop_cls, course_syn, basis)
        r15 = sorted({R15_ATTR.get(c, "R15 속성 없음(문구 parsed 보존만)") for c in d["classes"]} or {"R15 속성 없음(문구 parsed 보존만)"})
        words[w] = OrderedDict([("word", w), ("n_slots", len(d["locs"])), ("axes", axes), ("examples", d["examples"]), ("top_events", d["events"].most_common(3)),
                                ("sources", dict(d["sources"])), ("by", dict(d["by"])), ("fields_now", dict(d["fields_now"])), ("r15_attr_now", r15),
                                ("erd_stopword_class", stop_cls.get(w)), ("course_dict", course_syn.get(w)), ("analyzer_assist_r1", w in ASSIST_R1()),
                                ("r1_candidate", r1_words.get(w)), ("attach", dict(d["attach"])), ("frequency_keys", dict(d["freq_keys"])), ("phrase_status", dict(d["statuses"]))])
    # R1 후보 20 이 인벤토리에 다 있는가
    r1_missing = [w for w in r1_words if w not in words]
    for w in r1_missing:
        words[w] = OrderedDict([("word", w), ("n_slots", 0), ("axes", classify(w, {"classes": set(), "canonicals": [], "sources": {}}, stop_cls, course_syn, basis)), ("examples", [x[1] for x in comp_mods.get(w, [])][:3]),
                                ("top_events", []), ("sources", {"complication_name(analyzer_mod)": len(comp_mods.get(w, []))}), ("r1_candidate", r1_words[w])])
    impact, freq_src, deg_src, deg_cooc = edge_impact(occs, words, basis)
    # 축별 셈
    per_axis = Counter()
    per_axis_status = defaultdict(Counter)
    amb_words = []
    for w, x in words.items():
        for a in dedupe_list([e["axis"] for e in x["axes"]]):
            per_axis[a] += 1
        for e in x["axes"]:
            per_axis_status[e["axis"]][e["status"]] += 1
        if any(e["status"] in (ST_AMB, ST_BOUND) for e in x["axes"]):
            amb_words.append(w)
    out = OrderedDict([
        ("brief", "modifier-scale-brief.md"), ("generated_by", "modifier-scale/collect.py"),
        ("inputs", {"silver_out": "silver-v3/out (8차)", "ledger": "bronze/phub-ledger (3판)", "erd": "erd-v3.3.json", "gate": "silver-v3/out/gate/batch6.json r1-candidates"}),
        ("repro_check", {"phrase_entries": len(entries), "first_variant_parsed_equal": repro_ok, "occurrences": len(final)}),
        ("method", "8차 빌더를 다시 돌려 문구 자리(2,285)마다 parsed·멤버 수식어·경과/물질 span 을 받고, 분석기 관형어·부사어(word_info · R1 목록 걸름 없이)와 설명문·서술 칸의 EXTRA_PICK 낱말, 빈도 표현 정규식을 더했다. 같은 자리에서 같은 말은 한 번만 센다."),
        ("scales", OrderedDict([
            ("degree", [OrderedDict([("stage", k), ("key", key), ("score", sc), ("ledger_definition", basis["severity_levels"][key]), ("complications_rows", basis["severity_counts"].get(key, 0))]) for k, key, sc in DEGREE]),
            ("frequency", [OrderedDict([("stage", k), ("score", sc)]) for k, sc in FREQ]),
            ("frequency_number_pairs", basis["freq_number_pairs"]), ("frequency_verbal_only_incidence", basis["freq_verbal_only"]), ("incidence_numeric_only_rows", basis["incidence_numeric_only"]),
            ("pih_risk_levels_reference", basis["pih_risk_levels"]),
            ("timing", [OrderedDict([("stage", n), ("score", sc), ("onset_rows", basis["onset_counts"].get(n, 0))]) for n, sc, _ in TIMING]),
            ("course", {c: [s["value"] for s in e["synonyms"]] for c, e in ((e["canonical"], e) for e in dicts["course"]["entries"])}),
        ])),
        ("counts", OrderedDict([("words", len(words)), ("words_per_axis", dict(per_axis)), ("status_per_axis", {a: dict(c) for a, c in per_axis_status.items()}), ("ambiguous_words", len(amb_words)),
                                ("r1_candidates", len(r1_words)), ("r1_missing_in_phrase_slots", r1_missing)])),
        ("r15_impact_reference", OrderedDict([("counts", impact), ("frequency_sources", freq_src), ("degree_sources", deg_src), ("degree_word_vs_inherited_severity", deg_cooc)])),
        ("ambiguous", amb_words),
        ("words", list(words.values())),
    ])
    with open(os.path.join(HERE, "modifier-inventory.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=list)
    write_md(out, words, basis, r1_words)
    print(json.dumps(out["counts"], ensure_ascii=False))
    print(json.dumps(out["r15_impact_reference"]["counts"], ensure_ascii=False))


def ASSIST_R1():
    from lib.adverse33 import ASSIST_R1 as A
    return set(A)


# ---------------------------------------------------------------- 8. 검토용 md
def cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        out.append("| " + " | ".join(cell(c) for c in r) + " |")
    return "\n".join(out)


def write_md(out, words, basis, r1_words):
    c = out["counts"]
    imp = out["r15_impact_reference"]
    L = []
    L.append("# 부작용 수식어 — 수집 · 축 분류 · 표준 점수 초안 (2026-11-06 · 검토용 · 적용 아님)")
    L.append("")
    L.append("발주 `modifier-scale-brief.md`. 생성 `modifier-scale/collect.py`(모든 수는 코드가 셈) · 전수 `modifier-scale/modifier-inventory.json`. "
             "이 문서는 **초안**이다 — 사용자가 고친 뒤 ERD v3.3 구조(H)·결정 레코드로 9차에 들어간다. 지어낸 눈금·수치는 없다: 원장이 경계를 안 주는 곳은 「경계 미정 — 사용자」, 말-단계 연결이 원장에 없는 곳은 「애매 — 사용자」 또는 「초안(뜻)」으로 둔다.")
    L.append("")
    L.append("## 0. 요약")
    L.append("")
    L.append(f"- 문구 자리 {out['repro_check']['occurrences']} 전부(문구 사전 항목 {out['repro_check']['phrase_entries']}) · 8차 빌더 재실행 재현 검사 {out['repro_check']['first_variant_parsed_equal']}/{out['repro_check']['phrase_entries']} 일치")
    L.append(f"- 모은 말 {c['words']}(빈도 표현 묶음 포함) · 애매·경계 미정이 하나라도 있는 말 {c['ambiguous_words']} · R1 후보 {c['r1_candidates']}(문구 자리에 없는 것 {len(c['r1_missing_in_phrase_slots'])})")
    L.append("- 축별 말 수(한 말이 두 축이면 둘 다 셈): " + " · ".join(f"{a} {c['words_per_axis'].get(a, 0)}" for a in AX))
    oth = Counter()
    for w, x in words.items():
        if [e["axis"] for e in x["axes"]] == ["기타"]:
            b = x["axes"][0]["basis"]
            oth["부위·구조 명사(side)" if b == SIDE_NOTE else "문법·서술(ERD misc)" if b == MISC_NOTE else "물질·기전(qualifier)" if b.startswith("adverse_qualifier") else "그 밖"] += 1
    L.append("- 기타만 있는 말 내역: " + " · ".join(f"{k} {v}" for k, v in oth.most_common()) + " — 대부분 수식어가 아니라 분해 뒤 남은 명사·문법 말이다(참고로 함께 실었다)")
    L.append(f"- R15 엣지 영향(참고): 빈도 값이 생기는 엣지 {imp['counts'].get('freq_any', 0)} / {imp['counts']['edges']} · 정도 값 {imp['counts'].get('deg_any', 0)}(그중 complications severity 가 이미 있는 {imp['degree_sources'].get('complications severity(이미 값)', 0)} · 문구 정도 말로 새로 {imp['counts'].get('deg_new_from_phrase', 0)})")
    L.append("")
    L.append("## 1. 어떻게 모았나")
    L.append("")
    L.append("- **자리별 parsed**: `out/dictionaries.json` 문구 사전 항목의 parsed 는 그 항목 **첫 원문**에서만 나온다(같은 정규화형의 다른 원문 — 「경미한 불편감」 — 의 수식어는 항목에 안 보인다). 그래서 8차 빌더(`pipeline.run`)를 그대로 다시 돌려 `AdverseUnits31.evaluate` 를 감싸 2,285 자리마다 멤버·수식어·span 을 받았다. silver-v3/ 에는 쓰지 않는다(분석기 캐시는 임시 복사본).")
    L.append("- **출처(source)**: `parsed.<class>`(멤버 수식어 — ERD 수식어 138 단어·패턴 · analyzer_r1 · analyzer_n2) · `parsed.courses`(경과 span) · `parsed.qualifiers`(물질·기전 span) · `parsed.side` · `analyzer_mod`(분석기 관형어·부사어 하나 — 게이트 6 R1 후보와 같은 셈, R1 목록 걸름 없이) · `parsed.explanation/predicate` 중 EXTRA_PICK 낱말(collect.py 목록) · `text_expr`(빈도 표현 정규식 — 「극히 드묾」「매우 드묾」「거의 필발」「거의 없음」「낮은 발생률」「N% 미만·이하·이내」).")
    L.append("- **붙은 사건**: 말 바로 뒤 어절이 사건 말이면 그 사건 · 아니면 같은 멤버의 사건 · 없으면 문구 전체 사건. 「지금 들어간 칸」= 그 자리 parsed 의 어느 키에 들었나 · R15 속성(degree_text · timing_text · incidence_text · condition_text · course).")
    L.append("- **같은 자리에서 같은 말은 한 번**만 센다(자리 수 = 원장 자리 수).")
    L.append("")
    L.append("## 2. 눈금 초안")
    L.append("")
    L.append("### 2.1 정도 — complications `severity_levels` 4단")
    L.append("")
    deg_rows = []
    for s in out["scales"]["degree"]:
        mapped = [w for w, x in words.items() if any(e["axis"] == "정도" and e["stage"] == s["stage"] and e["status"] in (ST_DIRECT, ST_DRAFT) for e in x["axes"])]
        deg_rows.append((s["score"], s["stage"], s["key"], s["ledger_definition"], s["complications_rows"], ", ".join(f"{w}({words[w]['n_slots']}{'·뜻' if any(e['status'] == ST_DRAFT for e in words[w]['axes']) else ''})" for w in mapped) or "—"))
    L.append(table(["점수", "단계", "원장 키", "원장 정의(글자 그대로)", "complications 행", "맞춘 말(자리 · 뜻=초안)"], deg_rows))
    L.append("")
    amb_deg = [w for w, x in words.items() if any(e["axis"] == "정도" and e["status"] == ST_AMB for e in x["axes"])]
    L.append("정도 축 「애매 — 사용자」: " + ", ".join(f"{w}({words[w]['n_slots']})" for w in amb_deg) + " — 원장 4단 정의는 **관리 수준**(자연 소실 / 치료 필요 / 즉시 치료 / 응급)이라 「심한 · 강한 · 과도한」 같은 세기 말을 어느 단에 둘지 원장이 말하지 않는다. 참고로 그 말이 붙은 엣지가 상속받은 원장 severity 분포:")
    L.append("")
    co = imp["degree_word_vs_inherited_severity"]
    L.append(table(["말", "엣지가 상속한 severity 분포(참고 · 근거 아님)"], [(w, ", ".join(f"{k} {v}" for k, v in sorted(co[w].items(), key=lambda kv: -kv[1]))) for w in sorted(co, key=lambda w: -sum(co[w].values()))]))
    L.append("")
    L.append("### 2.2 빈도 — 원장 말 순서 · 경계는 원장이 안 준다")
    L.append("")
    fr = []
    for s in out["scales"]["frequency"]:
        mapped = [w for w, x in words.items() if any(e["axis"] == "빈도" and e["stage"] == s["stage"] and e["status"] in (ST_DIRECT, ST_DRAFT) for e in x["axes"])]
        fr.append((s["score"] if s["score"] is not None else "애매 — 사용자", s["stage"], ", ".join(f"{w}({words[w]['n_slots']})" for w in mapped) or ("taxonomy·extracted safety 칸 `uncommon` — 흔함 아래인 것은 말 뜻, 드묾과의 위아래는 원장이 말하지 않음" if s["score"] is None else "—")))
    L.append(table(["점수", "단계", "맞춘 말(자리)"], fr))
    L.append("")
    L.append("- **단계 이름의 출처**: complications incidence 칸의 빈도 말(매우 흔함 · 흔함 · 드묾 · 극히 드묾) — 원장 incidence 65 칸 중 수치 없이 말만 있는 칸: " + ", ".join(f"{k} {v}" for k, v in out["scales"]["frequency_verbal_only_incidence"].items()) + f" · 수치만 있는 칸 {out['scales']['incidence_numeric_only_rows']}.")
    L.append("- **safety 칸**: `common` → 흔함(4)은 칸 이름 뜻(초안) · `uncommon` → 위 표의 빈 자리(애매) · `serious` 는 **빈도가 아니라 중대성 칸**이라 빈도 값을 주지 않는다(애매 — 정도 축으로 볼지 사용자) · `long_term` 은 경과 쪽.")
    L.append("- **원장이 빈도 말과 수치를 한 칸에 함께 쓴 자리**(코드가 찾음 · 경계 근거 후보):")
    L.append("")
    L.append(table(["원장 자리", "빈도 말", "수치(같은 칸 · 짝인지는 원문 확인)", "원문"], [(p["locator"], ", ".join(p["words"]), ", ".join(p["numbers"]), p["text"]) for p in out["scales"]["frequency_number_pairs"]]))
    L.append("")
    L.append("  → 「흔함」이 `수%`(9/7)부터 `~72%`(9/2)까지 걸쳐 있다. 원장 안에서 흔함/드묾을 가르는 **한 경계값이 나오지 않는다** — 빈도 단계 경계는 **「경계 미정 — 사용자」**. "
             "원장의 유일한 수치 띠는 pih-risk.json `risk_levels`(" + ", ".join(f"{k} {v}" for k, v in out["scales"]["pih_risk_levels_reference"].items()) + ")인데 **PIH 위험도 전용**이다 — 이 띠를 부작용 전체 빈도 경계로 쓸지는 사용자 결정(지금 표의 % 말에는 「참고」로만 적었다).")
    L.append("")
    L.append("### 2.3 시점 — 원장 onset 말 그대로 · 점수 = 시간 순서")
    L.append("")
    tm = []
    for s in out["scales"]["timing"]:
        mapped = [w for w, x in words.items() if any(e["axis"] == "시점" and e["stage"] == s["stage"] and e["status"] in (ST_DIRECT, ST_DRAFT) for e in x["axes"])]
        tm.append((s["score"], s["stage"], s["onset_rows"], ", ".join(f"{w}({words[w]['n_slots']})" for w in mapped) or "—"))
    L.append(table(["점수", "단계", "complications onset 65 칸 중 그 말이 있는 칸", "맞춘 말(자리)"], tm))
    L.append("")
    L.append("- 「지연」은 시점이 아니라 경과 사전 값(§2.4). 수치(「1-2주」「24-72시간」)는 단위로 단계를 주되 **발현 시점인지 지속 기간인지 문구가 가르지 않는다**(초안). 「후」「초기」는 구간을 말하지 않아 애매.")
    L.append("")
    L.append("### 2.4 경과 — course 사전 그대로(매핑만 · 새 값 없음)")
    L.append("")
    crs = []
    for canon, syns in out["scales"]["course"].items():
        direct = [w for w, x in words.items() if any(e["axis"] == "경과" and e["stage"] == canon and e["status"] == ST_DIRECT for e in x["axes"])]
        cand = [w for w, x in words.items() if any(e["axis"] == "경과" and (e["stage"] or "").rstrip("?") == canon and e["status"] == ST_AMB for e in x["axes"])]
        crs.append((canon, ", ".join(syns) or "—", ", ".join(f"{w}({words[w]['n_slots']})" for w in direct) or "—", ", ".join(f"{w}({words[w]['n_slots']})" for w in cand) or "—"))
    L.append(table(["경과 값", "사전 동의어", "지금 경과로 읽힌 말(자리)", "경과 후보 — 사전 밖(dictionary_add 는 사용자)"], crs))
    L.append("")
    L.append("- 경과는 **이름 축**이다 — 서열 점수를 주지 않았다(일시 < 지속 < 영구 같은 순서는 원장이 적지 않음 · 매기려면 사용자).")
    L.append("")
    L.append("## 3. 축별 표(말 전수)")
    L.append("")
    for a in AX:
        rows = []
        for w, x in words.items():
            es = [e for e in x["axes"] if e["axis"] == a]
            if not es:
                continue
            e = es[0]
            rows.append((("★" if x.get("r1_candidate") else "") + w, x["n_slots"], e["stage"] or "—", e["score"] if e["score"] is not None else "—", e["status"], e["basis"],
                         " / ".join(x.get("examples") or [])[:120], ", ".join(f"{k} {v}" for k, v in x.get("top_events") or []),
                         ", ".join(f"{k} {v}" for k, v in (x.get("sources") or {}).items()), ", ".join(x.get("r15_attr_now") or [])))
        L.append(f"### 3.{AX.index(a) + 1} {a} — {len(rows)} 말")
        L.append("")
        L.append(table(["말(★=R1 후보)", "자리", "단계", "점수", "상태", "근거", "원문 예(최대 3)", "붙은 사건 상위 3", "출처 칸(자리)", "지금 R15 속성"], rows))
        L.append("")
    L.append("## 4. 애매 · 경계 미정 목록 — 사용자")
    L.append("")
    ar = []
    for w in out["ambiguous"]:
        x = words[w]
        for e in x["axes"]:
            if e["status"] in (ST_AMB, ST_BOUND):
                ar.append((w, x["n_slots"], e["axis"], e["stage"] or "—", e["status"], e["basis"]))
    L.append(f"말 {len(out['ambiguous'])} · 줄 {len(ar)}(한 말이 두 축이면 두 줄).")
    L.append("")
    L.append(table(["말", "자리", "축", "후보 단계", "상태", "왜"], ar))
    L.append("")
    L.append("## 5. R1 후보 20(게이트 6 `r1-candidates`)")
    L.append("")
    rr = []
    for w, g in r1_words.items():
        x = words[w]
        e = x["axes"][0]
        rr.append((w, g["gate_n"], x["n_slots"], " · ".join(f"{q['axis']}:{q['stage'] or '—'}" for q in x["axes"]), e["status"], g["gate_example"]))
    L.append("게이트 출현 수(complication 이름 포함 · 분석기 토막마다)와 이 조사의 문구 자리 수(자리당 1)는 세는 단위가 다르다. 게이트 결정(R1 목록 추가 여부)은 그대로 열려 있다 — 아래는 **축 분류만**.")
    L.append("")
    L.append(table(["말", "게이트 출현", "문구 자리", "축:단계", "상태", "게이트 원문 예"], rr))
    L.append("")
    L.append("## 6. R15 엣지 영향 수(참고 · 결정 전 · 적용 아님)")
    L.append("")
    ic = imp["counts"]
    L.append(table(["항목", "엣지 수"], [
        ("R15 엣지 전체", ic["edges"]), ("문구 유래(source_phrases 있음)", ic["edges_with_phrase"]),
        ("빈도 단계 값이 생김(초안 · 원장 같은 말+초안(뜻)만 · 애매 제외)", ic.get("freq_any", 0)),
        ("  ↳ 출처: " + ", ".join(f"{k} {v}" for k, v in imp["frequency_sources"].items()), ""),
        ("  ↳ common 칸을 빼고도 값이 생기는 엣지(문구 빈도 말 · complications incidence 말)", ic.get("freq_any_without_common_class", 0)),
        ("  ↳ 단계가 둘 이상 겹침(예: common 칸 + 「드물게」)", ic.get("freq_conflict", 0)),
        ("frequency_class=uncommon(자리 애매 — 값 안 줌)", ic.get("freq_class_uncommon(위치 애매)", 0)),
        ("complications incidence 가 수치만(경계 미정 — 값 안 줌)", ic.get("incidence_numeric_only(경계 미정)", 0)),
        ("정도 단계 값이 있음", ic.get("deg_any", 0)),
        ("  ↳ 출처: " + ", ".join(f"{k} {v}" for k, v in imp["degree_sources"].items()), ""),
        ("  ↳ complications severity 없이 문구 정도 말로만 새로", ic.get("deg_new_from_phrase", 0)),
        ("(별도) severity 를 계열 엣지에서 상속 참조만 하는 엣지", ic.get("deg_inherited_ref(상속 참조 · 이미 있음)", 0)),
        ("문구 자리 사건과 엣지 끝 사건이 안 맞은 엣지(셈 누락 점검)", ic.get("phrase_edges_event_not_in_occurrence", 0)),
    ]))
    L.append("")
    L.append("- 빈도 셈은 `common` 칸 → 흔함(초안)을 넣은 수다. `common` 을 빼면 문구 빈도 말·complications incidence 말만 남는다(출처 줄 참고).")
    L.append("- 정도 셈의 「문구 정도 말」은 경미 쪽(경미한 · 가벼운 · 약간의 …)뿐이다 — 「심한 · 과도한」 류는 애매라 값을 주지 않았다.")
    L.append("")
    L.append("## 7. 모으지 않은 것 · 한계")
    L.append("")
    L.append("- 설명문·서술 칸(parsed.explanation · predicate)의 명사·용어(「1회용 · 팁 · 위생」 류)는 수식 말이 아니라 모으지 않았다 — 집은 낱말은 collect.py `EXTRA_PICK` 이 전부다.")
    L.append("- 「붙은 사건」은 바로 뒤 어절 규칙이라 「과도한 에너지로 인한 진피 손상」처럼 수식 대상이 사건이 아닌 자리는 「같은 멤버/문구 전체」 사건으로 잡힌다(축 분류는 원문 예를 보고 두 축으로 적었다).")
    L.append("- complications 이름 65(계열 R15)의 수식 말은 이름 분해 쪽 경과·정도로 이미 들어가 있어 여기서는 R1 후보 대조에만 썼다.")
    with open(os.path.join(HERE, "modifier-scale-draft.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
