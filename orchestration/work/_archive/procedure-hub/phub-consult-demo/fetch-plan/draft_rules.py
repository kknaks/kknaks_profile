"""초안 이해 프롬프트(사본) — 앱 `prompts/consult.json` pick 을 읽어 고친 사본을 만든다(앱 파일은 안 고침).

고친 것: 출력 꼴 줄에 `fetch` 칸 · 규칙 20 ~ 23(가져오기 계획). 회차(`ROUND`)마다 바꾼 문구는 아래 PATCH 에 남긴다.
"""
import copy, json
from pathlib import Path

APP_PROMPT = Path("/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/prompts/consult.json")

OUT_LINE_R4 = ('출력 꼴: {"targets":[{"table":"concern","code":"CON-000","sure":true}],"kind":"new","sites":["SITE-000"],'
               '"withdraw":[],"exclude":[],"pairs":[],"kinds":[],"out":false,"country":null,"topic":{"move":"continue","to":null},'
               '"fetch":{"about":"targets","kinds":[],"layers":"sub","scope":"branch","lineup":"none"}}')
OUT_LINE = ('출력 꼴: {"targets":[{"table":"concern","code":"CON-000","sure":true}],"kind":"new","sites":["SITE-000"],'
            '"withdraw":[],"exclude":[],"pairs":[],"kinds":[],"out":false,"country":null,"topic":{"move":"continue","to":null},'
            '"fetch":{"about":"targets","kinds":[],"layers":"sub","scope":"branch","lineup":"none","site_filter":[]}}')

RULES_R1 = [
    "20. fetch = 다음 단계가 허브에서 **무엇을 · 어디까지** 가져올지. 판단은 여기서 끝내고 다음 단계는 이 값대로만 읽는다.",
    "20-1. about — 이번 말이 대상(고민 · 시술 · 계열 · 케이스 · 제품 · 효과)을 말하거나 그 대상에 대해 물으면 \"targets\". 부위만 말하거나(「얼굴에」 「턱이요」) 짧게 답해 지금 주제를 이어 좁히기만 하면 \"topic\"(지금 주제의 고민 · 시술에 대해 그 부위로 가져옴).",
    "20-2. kinds — 가져올 정보 종류(규칙 11 의 코드). 규칙 11 의 kinds 를 그대로 넣고 더한다: 「전반적으로 설명」 「~에 대해 설명해줘」 · 대상을 처음 묻는 「~가 뭐야」 → overview, mechanism, indication, outcome, lineup. 「원리」 → overview, mechanism. 「효과 · 언제부터 · 얼마나 가」 「~돼?」(효과 확인) → outcome, indication. 「부작용 · 아파?」 → adverse, recovery. 고민만 · 부위만 말하고 묻는 것이 없으면 [](앱 기본 묶음).",
    "20-3. layers — \"self\" 그 대상 자체만 · \"inherit\" 위 계열에서 물려받은 정보까지 · \"sub\" 그 아래 시술 · 케이스 · 제품까지. 계열 · 시술(아래 제품 · 케이스가 있는 것)을 묻거나 「종류 · 뭐가 있어 · 어떤 제품」 이면 \"sub\". 제품 · 케이스 하나를 콕 집어 물으면 \"inherit\". 모르면 \"sub\".",
    "20-4. scope — 기본 \"branch\"(명동점 진료항목에 닿는 것만). 손님이 명동점 목록에 없는 시술 · 제품을 말하거나 「다른 병원」 「명동점 말고」 「일반적으로」 를 물으면 \"all\".",
    "20-5. lineup — 기본 \"none\". 「종류 · 뭐가 있어 · 어떤 제품」 이나 kinds 에 lineup 이 있으면 \"names\"(이름만). 아래 제품 · 케이스끼리 비교 · 차이를 물으면 \"detail\".",
    "20-6. site_filter — 이번 말에 나온 부위 코드(sites 와 같은 값). 없으면 [].",
]
PATCH = {1: RULES_R1}  # 회차 → 규칙 20 묶음(회차 2 부터는 아래에서 덮어씀)

RULES_R2 = list(RULES_R1)
RULES_R2[2] = RULES_R1[2].replace("「부작용 · 아파?」 → adverse, recovery.", "「부작용 · 아파?」 → adverse, recovery. 「몇 샷 · 몇 회 · 용량 · 가격 · 얼마」 → offer(+ outcome).")
RULES_R2[3] = "20-3. layers — 기본 \"sub\"(그 아래 시술 · 케이스 · 제품까지). 제품 · 시술 이름이어도 그 아래 모델 · 용량 · 제품이 있을 수 있으니 \"sub\" 다. \"inherit\"(위 계열에서 물려받은 정보까지)는 케이스 하나를 이름 그대로 콕 집어 그것만 물을 때, \"self\"(그 대상 자체만)는 이미 고른 대상 하나의 한 가지(가격만 · 회복만)를 물을 때만."
RULES_R2[4] = RULES_R1[4] + " 앞 답에서 「명동점에는 없다」 며 보여 준 것을 이어 물어도(「그거 어떤 원리야」) \"all\"."
PATCH[2] = RULES_R2

# 회차 4(0.1.1 — 검수 P2-6 · P2-7 · P2-8 · JC6): site_filter 칸 없앰(sites 를 씀) · 꼴 겹침 · 「그중에서 + 이름 없음」 · 명동점 목록 물음 = branch
RULES_R4 = list(RULES_R2[:6])
RULES_R4[1] = RULES_R2[1] + " 「그중에서 뭐가 좋아」 처럼 이름 없이 앞 답 목록을 좁히면 \"topic\"."
RULES_R4[2] = RULES_R2[2] + " 말이 여러 꼴에 걸리면(「보톡스 맞고 싶은데 효과랑 부작용」) 종류를 모두 합친다."
RULES_R4[4] = RULES_R2[4].replace("(명동점 진료항목에 닿는 것만)", "(명동점 진료항목에 닿는 것은 다 · 밖은 이름만)") + " 「명동점에 뭐 있어」 처럼 명동점 목록만 물으면 \"branch\". 꼴이 여럿이면 \"all\" 이 이긴다."
RULES_R4[5] = RULES_R2[5] + " 꼴이 여럿이면 가장 넓은 값(detail > names > none)."
RULES_R4.append("20-6. layers 는 scope 가 \"all\" 일 때만 쓰인다(명동점에 닿는 하위는 늘 읽힌다). 부위 필터는 sites 를 그대로 쓴다 — fetch 에 따로 쓰지 않는다.")
PATCH[4] = RULES_R4


def build(round_: int) -> dict:
    d = json.loads(APP_PROMPT.read_text())
    p = copy.deepcopy(d["pick"])
    rules = list(p["rules"])
    i = next(k for k, r in enumerate(rules) if r.startswith("출력 꼴:"))
    rules[i] = OUT_LINE_R4 if round_ >= 4 else OUT_LINE
    add = PATCH.get(round_) or PATCH[max(k for k in PATCH if k <= round_)]
    p["rules"] = rules + add
    p["draft_round"] = round_
    return p
