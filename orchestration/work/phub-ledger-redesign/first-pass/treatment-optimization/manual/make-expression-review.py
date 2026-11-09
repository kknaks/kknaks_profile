#!/usr/bin/env python3
"""자동 후보 오탐·수식 토큰 검토 기록(expression-review.json) 생성기. 직접 대조 결과를 (pointer, pattern, 원문 구절, 몇 번째 출현) 으로 적는다."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, *[".."] * 6, "orchestration/work/phub-recommend/bronze/phub-ledger/treatment-optimization.json")
BC = "/by_concern/{}/severity_levels/{}/{}"
FP = [
    (BC.format(6, 1, "rationale"), "R04-slash-join", "다이오드/Nd", 0, "경계 오류: 장비명 「Nd:YAG」의 콜론에서 끊겨 「다이오드/Nd」만 잡힘. 실제 구절은 「다이오드/Nd:YAG」(수동 구절에 있음)"),
    ("/by_concern/5/concern_en", "R04-slash-join", "Acne / Acne", 0, "경계 오류: 「Acne / Acne Scars」의 뒤 어절이 잘림(수동 구절에 전체 있음)"),
    ("/annual_plans/2/plan_name", "R05-plus-join", "40대+ 안티에이징", 0, "`+` 가 연령 열린 범위(40대 이상)라 「함께」 결합이 아님"),
    (BC.format(6, 2, "optimal_combo/0"), "R05-plus-join", "다이오드+Nd", 0, "경계 오류: 「다이오드+Nd:YAG」의 콜론에서 끊김"),
    (BC.format(6, 2, "rationale"), "R10-sameday", "동시", 0, "「다양한 깊이의 모낭 동시 타겟」 — 한 시술 안의 동시 작용이며 시술 간 같은 날·동시 일정이 아님"),
    ("/by_age_group/2/annual_focus", "R10-sameday", "동시", 0, "「처짐/볼륨 동시 관리」 — 고민 두 개를 함께 관리한다는 뜻, 시술 일정의 동시가 아님"),
    ("/optimization_principles/2", "R11-within-after", "최소", 0, "「최소화」(최소로 줄임)의 일부. 간격 하한 「최소」가 아님"),
    (BC.format(3, 2, "caveats/0"), "R11-within-after", "내", 1, "「화장품 광고 내」 — 공간·범위의 「안」. 기간 「이내」가 아님"),
    (BC.format(2, 0, "level"), "R14-risk", "저하", 0, "「미세 볼륨 저하」 — 고민 상태 서술, 시술 위험·부작용 어휘 아님"),
    (BC.format(3, 0, "level"), "R14-risk", "저하", 0, "「가벼운 피부결 저하」 — 고민 상태 서술"),
    ("/by_age_group/1/primary_concerns/1", "R14-risk", "저하", 0, "「탄력 저하」 — 고민 이름"),
    (BC.format(7, 1, "level"), "R16-limit-only", "만", 0, "「비만」의 일부. 제한 「만」이 아님"),
    ("/combination_rules/2/detail", "R16-limit-only", "만", 0, "「지지하지만」의 양보 어미 「-지만」. 제한 「만」이 아님"),
    (BC.format(3, 2, "caveats/0"), "R17-negation", "미", 1, "「FDA 미용·치료 목적」의 미용(美容). 부정 접두 「미(未)」가 아님(같은 값의 0번째 「미」는 「미승인」으로 정탐)"),
]
UNCOV = []  # (pointer, 원문 구절, occurrence, note) — 수동 구절 밖 수식·부정 토큰의 개별 검토
def main():
    d = json.load(open(SRC, encoding="utf-8"))
    def get(p):
        x = d
        for t in p.split("/")[1:]:
            x = x[int(t)] if isinstance(x, list) else x[t]
        return x
    fps = []
    for ptr, pat, text, occ, note in FP:
        v = get(ptr)
        starts = [m.start() for m in re.finditer(re.escape(text), v)]
        s = starts[occ]
        fps.append({"pointer": ptr, "pattern": pat, "span": [s, s + len(text)], "text": text, "note": note})
    unc = []
    for ptr, text, occ, note in UNCOV:
        v = get(ptr)
        s = [m.start() for m in re.finditer(re.escape(text), v)][occ]
        unc.append({"pointer": ptr, "span": [s, s + len(text)], "text": text, "note": note})
    out = {"note": "자동 정규식 후보 중 직접 대조로 확인한 오탐(출현별)과, 수동 구절에 덮이지 않은 수식·부정 토큰의 개별 검토. 경계만 잘린 R04/R05 후보 전반의 한계는 issues K-03.",
           "auto_false_positives": fps, "uncovered_token_reviews": unc}
    json.dump(out, open(os.path.join(HERE, "expression-review.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("fp", len(fps), "uncovered_reviews", len(unc))
main()
