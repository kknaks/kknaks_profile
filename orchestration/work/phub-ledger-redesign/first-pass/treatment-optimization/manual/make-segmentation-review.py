#!/usr/bin/env python3
"""알려진 오분절 출현 기록(segmentation-review.json) 생성기.

토큰 전수 열람에서 찾은 오분절을 규칙(값 Pointer · 원문 구절 · 기대 원시 토큰)으로 적고,
morphology.json 에서 출현 구간을 찾아 원시 토큰이 기대와 같은지 확인한 뒤 출현별로 기록한다.
pointer="*" 는 분석 적용된 모든 값에서 그 구절의 모든 출현을 찾는다(모든 출현이 기대 토큰과 같아야 통과).
실행(이 폴더에서, build.py 1회 실행 뒤): python3 manual/make-segmentation-review.py → 다시 build.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

BC = "/by_concern/{}/severity_levels/{}/{}"
RULES = [
    # (pointer, 원문 구절, occurrence 또는 None(전부), 기대 원시 토큰, 유형, 영향)
    ("/optimization_principles/0", "우선", 0, ["우선/MAG"], "POS_SHIFT", "「안전성 우선」의 우선(우선순위)이 부사(MAG)로 태깅 — 명사 결합 정보가 약해진다"),
    ("/combination_rules/5/detail", "우선", 0, ["우선/MAG"], "POS_SHIFT", "「필러 위치 안정화 우선」의 우선이 부사 — 목적·우선순위 서술이 부사로 읽힌다"),
    ("*", "중등도", None, ["중등/NNG", "도/JX"], "SPLIT_TERM", "단계명 「중등도」가 「중등」+보조사 「도」로 갈려 정도 단계어가 사라지고 「도(또한)」로 오인될 수 있다"),
    (BC.format(0, 1, "expected_sessions"), "필러", 0, ["필/NNP", "러/EC"], "SPLIT_TERM", "시술명 「필러」가 「필」+어미 「러」로 분해 — 시술 토큰 소실"),
    (BC.format(0, 2, "expected_sessions"), "필러", 0, ["필/NNP", "러/EC"], "SPLIT_TERM", "시술명 「필러」 분해"),
    (BC.format(1, 2, "expected_sessions"), "필러", 0, ["필/NNP", "러/EC"], "SPLIT_TERM", "시술명 「필러」 분해"),
    (BC.format(5, 2, "expected_sessions"), "필러", 0, ["필/NNP", "러/EC"], "SPLIT_TERM", "시술명 「필러」 분해"),
    ("/by_age_group/2/maintenance", "필러", 0, ["필/NNG", "러/EC"], "SPLIT_TERM", "시술명 「필러」 분해 — 유지 빈도 「필러 6개월+」의 대상 소실"),
    ("/by_age_group/3/maintenance", "필러", 0, ["필/NNG", "러/EC"], "SPLIT_TERM", "시술명 「필러」 분해 — 유지 빈도 대상 소실"),
    ("/combination_rules/0/evidence", "필러", 0, ["필/NNG", "러/EC"], "SPLIT_TERM", "문헌 서술 「HA 필러 열분해」의 필러 분해"),
    (BC.format(0, 2, "sequence"), "필러", 0, ["피/VV", "ᆯ러/EC"], "SPLIT_TERM", "「2주 후 필러」의 필러가 동사 「피다」+어미로 분석 — 순서 단계의 시술 소실"),
    (BC.format(1, 1, "rationale"), "슬림", 0, ["슬/MAG", "림/NNG"], "SPLIT_TERM", "「턱선 슬림」이 부사 「슬」+「림」 — 거짓 부사 생성, 효과어 소실"),
    (BC.format(1, 1, "rationale"), "바이오스티뮬로", 0, ["바이오스티뮬로/NNG"], "PARTICLE_ABSORB", "조사 「로」가 명사에 흡수 — 다른 출현(바이오스티뮬/NNG 로/JKB)과 표면형이 달라 같은 대상 집계에서 빠진다"),
    (BC.format(1, 2, "rationale"), "거상", 0, ["거/NNB", "상/NNG"], "SPLIT_TERM", "「물리적 거상」(들어 올림)이 의존명사 「거」+「상」 — 효과어 소실"),
    (BC.format(1, 2, "rationale"), "실리프팅", 0, ["실/NNG", "리프팅/NNG"], "INCONSISTENT", "다른 출현은 실리프팅/NNP 한 토큰 — 같은 시술이 분석마다 다르게 잘림"),
    ("/by_age_group/3/recommended_base/4", "실리프팅", 0, ["실/NNG", "리프팅/NNG"], "INCONSISTENT", "같은 시술의 분절 불일치"),
    (BC.format(1, 2, "contraindicated_combos/0"), "비가교", 0, ["비가교/NNP"], "NEG_HIDDEN", "부정 접두 「비(非)」가 고유명사 안에 묻힘 — 「가교 HA」와의 대비가 토큰에서 드러나지 않는다"),
    ("/combination_rules/7/rule", "비가교", 0, ["비가교/NNP"], "NEG_HIDDEN", "부정 접두 「비」 숨김"),
    ("/combination_rules/7/detail", "비가교", 0, ["비가교/NNP"], "NEG_HIDDEN", "부정 접두 「비」 숨김"),
    (BC.format(2, 2, "rationale"), "지방이식", 0, ["지방/NNG", "이/JKS", "식/NNB"], "SPLIT_TERM", "「지방이식」의 이식이 주격조사 「이」+「식」 — 시술명 소실, 거짓 주어 표지"),
    (BC.format(3, 1, "rationale"), "스킨부스터", 0, ["스킨/NNG", "부스/NNG", "터/NNG"], "SPLIT_TERM", "시술 계열명 3토큰 분해"),
    (BC.format(3, 2, "rationale"), "스킨부스터", 0, ["스킨/NNG", "부스/NNG", "터/NNG"], "SPLIT_TERM", "시술 계열명 3토큰 분해"),
    ("*", "CO2", None, ["CO/SL", "2/SN"], "FALSE_NUM", "장비명 「CO2」의 2가 숫자(SN)로 분리 — 수량·회차로 오인될 수 있다"),
    (BC.format(3, 2, "caveats/1"), "엑소좀", 0, ["엑소/NNP", "좀/MAG"], "FALSE_MODIFIER", "「엑소좀」이 「엑소」+정도부사 「좀(조금)」 — 거짓 정도 수식 생성, 대상명 소실"),
    (BC.format(3, 2, "caveats/1"), "유의", 0, ["유/NNG", "의/JKG"], "SPLIT_TERM", "「유의 개선」(통계적 유의)이 「유」+관형격조사 — 근거 강도 표현 소실"),
    (BC.format(4, 1, "optimal_combo/1"), "경구", 0, ["경/NNG", "구/NNG"], "SPLIT_TERM", "투여 경로 「경구」 분해"),
    (BC.format(4, 1, "optimal_combo/1"), "국소", 0, ["국/NNG", "소/NNG"], "SPLIT_TERM", "투여 경로 「국소」 분해"),
    (BC.format(4, 2, "sequence"), "국소", 0, ["국/NNG", "소/NNG"], "SPLIT_TERM", "투여 경로 「국소」 분해"),
    (BC.format(4, 1, "optimal_combo/3"), "병용", 0, ["병/NNG", "용/XSN"], "SPLIT_TERM", "「병용 보조」의 병용(함께 씀)이 「병」+접미사 — 병용 조건 소실"),
    (BC.format(4, 1, "sequence"), "선행", 0, ["선/NNG", "행/NNG"], "SPLIT_TERM", "「광차단 선행」의 선행(먼저 함) 분해 — 선행 조건 소실"),
    (BC.format(4, 1, "sequence"), "미백", 0, ["미/NNP", "백/NR"], "FALSE_NUM", "「스킨부스터(미백)」의 미백이 「미」+수사 「백(100)」 — 거짓 수량 생성"),
    (BC.format(5, 0, "sequence"), "필링", 0, ["필/NNG", "링/NNG"], "SPLIT_TERM", "시술명 「필링」 분해"),
    ("/annual_plans/1/schedule/11/procedures/1", "필링", 0, ["필/NNG", "링/NNG"], "SPLIT_TERM", "시술명 「필링」 분해"),
    (BC.format(5, 1, "sequence"), "서브시전", 0, ["서브/NNG", "시전/NNG"], "SPLIT_TERM", "시술명 「서브시전」 분해(다른 출현은 한 토큰)"),
    (BC.format(5, 1, "expected_sessions"), "서브시전", 0, ["서브시/NNP", "전/MM"], "SPLIT_TERM", "「서브시전」이 「서브시」+관형사 「전」 — 시술명 소실, 거짓 관형사"),
    (BC.format(5, 2, "expected_sessions"), "서브시전", 0, ["서브시/NNP", "전/MM"], "SPLIT_TERM", "같음"),
    (BC.format(5, 1, "sequence"), "박리", 0, ["박/NNG", "리/XSN"], "SPLIT_TERM", "「흉터 박리」의 박리 분해"),
    (BC.format(5, 1, "rationale"), "박리", 0, ["박/NNG", "리/XSN"], "SPLIT_TERM", "「섬유화 박리」의 박리 분해"),
    (BC.format(5, 1, "sequence"), "동시", 0, ["동/MM", "시/NNB"], "SPLIT_TERM", "「PRP 동시 도포」의 동시가 관형사 「동」+의존명사 「시」 — 동시 시점 표현이 토큰에서 사라진다"),
    (BC.format(5, 2, "level"), "박스카", 0, ["박스/NNG", "카/NNG"], "SPLIT_TERM", "흉터 유형 「박스카」 분해"),
    (BC.format(5, 2, "level"), "아이스픽", 0, ["아이스/NNG", "픽/MAG"], "FALSE_MODIFIER", "흉터 유형 「아이스픽」이 「아이스」+부사 「픽」 — 거짓 부사"),
    (BC.format(5, 2, "sequence"), "남은", 0, ["남/NNG", "은/JX"], "POS_SHIFT", "「필러(남은 함몰)」의 남은(남다+관형형)이 명사 「남」+보조사 — 잔여 조건이 사라진다"),
    (BC.format(6, 1, "rationale"), "Nd:YAG", 0, ["Nd/SL", ":/SP", "YAG/SL"], "ID_SPLIT", "장비명 「Nd:YAG」의 콜론이 구두점(SP)으로 분리 — 라벨 구분자(「밝은 피부:」)와 구별되지 않는다"),
    (BC.format(6, 2, "optimal_combo/0"), "Nd:YAG", 0, ["Nd/SL", ":/SP", "YAG/SL"], "ID_SPLIT", "같음"),
    ("/by_age_group/0/avoid/0", "중요", 0, ["중/NNB", "요/NNG"], "SPLIT_TERM", "「자연스러운 노화 중요」의 중요가 「중」+「요」 — 회피 사유의 판단어 소실"),
    ("/by_age_group/2/primary_concerns/1", "처짐", 0, ["처지/VV", "ᆷ/EF"], "POS_SHIFT", "단독 명사 「처짐」의 ㅁ이 종결어미(EF)로 — 다른 출현(ETN 명사형)과 다름"),
    ("/by_age_group/3/primary_concerns/0", "처짐", 0, ["처지/VV", "ᆷ/EF"], "POS_SHIFT", "같음"),
    ("/by_age_group/3/note", "비수술", 0, ["비수/NNG", "술/NNG"], "NEG_HIDDEN", "「비수술 조합」이 「비수(秘手)」+「술」 — 부정 접두 「비」 소실로 수술/비수술 대비가 사라진다"),
    ("/by_age_group/3/recommended_base/0", "울쎄라급", 0, ["울쎄라급/NNP"], "PARTICLE_ABSORB", "등급 접미 「급」이 고유명사에 흡수 — 근사(수준) 표현이 토큰에서 드러나지 않는다"),
    ("/combination_rules/0/rule", "열시술", 0, ["열/NR", "시/NNB", "술/NNG"], "FALSE_NUM", "「열시술」(열을 쓰는 시술)이 수사 「열(10)」+의존명사 「시(時)」+「술」 — 거짓 수량·시각 생성"),
    ("/combination_rules/0/detail", "열시술", 0, ["열/NR", "시/NNB", "술/NNG"], "FALSE_NUM", "같음 — 거짓 「10시」"),
    ("/combination_rules/0/detail", "열시술", 1, ["열/NR", "시/NNB", "술/NNG"], "FALSE_NUM", "같음"),
    ("/combination_rules/2/rule", "수화", 0, ["수/NNG", "화/XSN"], "SPLIT_TERM", "「수화」(물을 머금게 함) 분해"),
    ("/combination_rules/2/detail", "수화", 0, ["수/NNB", "화/XSN"], "SPLIT_TERM", "「충분한 수화」의 수화가 의존명사 「수」+접미사 — 「~할 수」 표지로 오인될 수 있다"),
    ("/combination_rules/2/detail", "결절", 0, ["결/NNG", "절/NNG"], "INCONSISTENT", "「결절 예방」의 결절 분해(같은 값의 「결절률」은 결절/NNG)"),
    ("/combination_rules/2/detail", "깊이", 0, ["깊이/MAG"], "POS_SHIFT", "「정확한 주입 깊이」의 명사 깊이가 부사(깊게)로 — 깊이 조건이 수식어로 바뀐다"),
    ("/combination_rules/2/evidence", "비마사지군", 0, ["비마사지군/NNG"], "NEG_HIDDEN", "부정 접두 「비」가 한 명사에 묻힘 — 대조군 표지 숨김"),
    ("/combination_rules/4/detail", "반동", 0, ["반/NNG", "동/NNG"], "INCONSISTENT", "「반동 색소침착」의 반동 분해(다른 출현은 반동/NNG)"),
    ("/annual_plans/1/schedule/0/procedures/0", "이마", 0, ["이/MM", "마/NNG"], "SPLIT_TERM", "부위 「이마」가 관형사 「이(this)」+「마」 — 부위 소실"),
]


def main():
    morph = json.load(open(os.path.join(OUT, "morphology.json"), encoding="utf-8"))
    vals = {a["pointer"]: a["value"] for a in morph["applied_values"]}
    toks = {}
    for t in morph["tokens"]:
        toks.setdefault(t["value_pointer"], []).append(t)
    entries = []
    for ptr, text, occ, expect, kind, impact in RULES:
        targets = [ptr] if ptr != "*" else [p for p in vals if text in vals[p]]
        assert targets, ("no target", ptr, text)
        for p in targets:
            starts = [m.start() for m in re.finditer(re.escape(text), vals[p])]
            assert starts, ("text not in value", p, text)
            use = starts if occ is None else [starts[occ]]
            for s in use:
                e = s + len(text)
                raw = [f"{t['form']}/{t['tag']}" for t in toks[p] if t["start"] < e and t["end"] > s]
                assert raw == expect, ("token mismatch", p, text, s, raw, expect)
                entries.append({"pointer": p, "span": [s, e], "text": text, "raw_tokens": raw, "kind": kind,
                                "impact": impact, "status": "K-기록됨(교정 안 함)"})
    out = {
        "note": "Kiwi 0.24.1(cong) 기본 사전 원시 출력의 알려진 오분절·오태깅 출현별 기록. 토큰 전수 열람(SEG-00~13)에서 직접 찾았다. 교정하지 않았고 morphology.json 의 원시 토큰은 그대로다. 이 목록 밖의 원시 출력 정확성을 보장하지 않는다.",
        "kinds": {"SPLIT_TERM": "전문어·시술명·일반어 분해", "FALSE_NUM": "숫자·수량으로 오인", "FALSE_MODIFIER": "거짓 부사·수식어 생성",
                  "NEG_HIDDEN": "부정 접두가 묻히거나 사라짐", "POS_SHIFT": "품사가 바뀌어 기능이 달라짐", "PARTICLE_ABSORB": "조사·접미가 명사에 흡수",
                  "INCONSISTENT": "같은 표기의 분절 불일치", "ID_SPLIT": "식별자·장비명 내부 기호 분리"},
        "entries": entries,
    }
    with open(os.path.join(HERE, "segmentation-review.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("entries", len(entries))


if __name__ == "__main__":
    main()
