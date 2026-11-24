"""정답표 만들기 — 턴마다 기대(주제 · 꼭 있어야 할 / 있으면 안 되는 진료항목 묶음 · 점 · 답 글 기준)를 규칙으로 풀어
`answers.json`(기계) + `answers.md`(사람)로 쓴다. 값은 매핑 JSON 과 허브 18105 GET 으로만 푼다(지어 넣지 않음).

단위: 진료항목 묶음 = 매핑 `groups[].kos_procedure`(예: 「울쎄라피 프라임」 · 「턱보톡스」). 목록에 그 묶음 진료항목이 하나라도
있으면 「있음」.

규칙(R*) — 정답 칸은 아래 규칙으로만 채운다:
  R1 명시: 손님이 이름을 댄 시술 · 제품(`name`) → 묶음 이름 또는 허브 제품 이름에 그 낱말이 든 묶음.
     「필러」 = 허브 시술 PRC-100 · 「보톡스」 = PRC-001 묶음. 부위가 있으면 R4 로 거르고, 꼭 있음 칸은 그 부위에 바로 매핑된
     묶음 → 없으면 자손 부위 묶음 → 없으면 부위를 품는 얼굴 전체 묶음(한 층만). 「이 묶음만」 칸은 부위 없이 이름 전부.
  R2 고민: 허브 `concern-candidates`(upper=auto · to_procedure=none) 행 가운데 reach 「케이스 직접」 · procedure_case →
     매핑 `hub.case_codes` 로 진료항목 → 묶음(R4 로 거름). ⚑ 사용자 확인 칸.
  R3 효과: 허브 `facets outcome effect:<코드>` 의 procedure_case · procedure 대상 → 진료항목 → 묶음(R4). ⚑ 사용자 확인 칸.
  R4 부위: 진료항목 매핑 부위가 그 부위의 자손(자기 포함)이거나, 얼굴 부위면 「얼굴」(SITE-007) 매핑 + site_scope 얼굴 전체 ·
     어디든(앱 SF2 · SF3 규칙과 같은 정의).
  R5 부위 밖: 지금 주제 부위가 있으면 R4 에 안 드는 묶음은 「있으면 안 됨」.
  R6 몸: 얼굴 주제에 몸 묶음(매핑 부위가 모두 얼굴 밖 · 또는 site_scope 「몸」 뿐)은 「있으면 안 됨」.
  R7 고민 부위(점): 허브 concern-candidates 머리 `sites[]` 의 match 「직접」 부위.
  R8 정보 질문(원리 · 부작용 · 가격 · 「~만 가능해?」 · 밖 시술 물음): 목록은 앞 턴과 같아야 한다(`same_as`).
     밖 · 없는 시술을 물어 목록이 0 이 되는 경우도 앞 목록을 둔다(_RESUME 11-20 「0 이면 앞 목록 + 이유」).
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = Path("/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo")
MAP = A / "data/kos/myeongdong-mapping-20261120-v3.json"
HUB = "http://127.0.0.1:18105/procedure-hub/gold"
FACE_ROOT = "SITE-007"
SCOPE_FACE = ("얼굴 전체", "어디든(부위 무관)", "얼굴 · 몸 가능")  # 앱 detect.py SCOPE_FACE 와 같은 값
PROC_WORD = {"필러": "PRC-100", "보톡스": "PRC-001"}

M = json.loads(MAP.read_text())
SITES = dict(M["sites"]) if isinstance(M["sites"], list) else M["sites"]
ITEM = {i["kos_item_code"]: i for i in M["items"]}
GROUP_OF = {c: g["kos_procedure"] for g in M["groups"] for c in g["items"]}
GROUPS = [g["kos_procedure"] for g in M["groups"]]

# ---------- 허브 GET ----------
_cache: dict = {}


def hub_all(path: str, params: dict, key: str) -> tuple[list, dict]:
    ck = (path, json.dumps(params, sort_keys=True))
    if ck in _cache:
        return _cache[ck]
    rows, head, cur = [], {}, None
    while True:
        q = dict(params, limit=100)
        if cur:
            q["cursor"] = cur
        with urllib.request.urlopen(f"{HUB}{path}?{urllib.parse.urlencode(q)}", timeout=60) as r:
            page = json.loads(r.read())
        if not head:
            head = {k: v for k, v in page.items() if k != key}
        rows += page.get(key) or []
        cur = page.get("next_cursor")
        if not cur:
            break
    _cache[ck] = (rows, head)
    return rows, head


def children(code: str) -> list[str]:
    return [c for c, v in SITES.items() if v.get("parent_code") == code]


def descendants(code: str) -> set[str]:
    out, st = set(), [code]
    while st:
        c = st.pop()
        if c in out:
            continue
        out.add(c)
        st += children(c)
    return out


def ancestors(code: str) -> list[str]:
    out, c = [], SITES.get(code, {}).get("parent_code")
    while c:
        out.append(c)
        c = SITES.get(c, {}).get("parent_code")
    return out


def in_site(code: str, site: str | None) -> bool:
    """R4."""
    if not site:
        return True
    it = ITEM[code]
    sc = set(it["hub"].get("site_codes") or [])
    if sc & descendants(site):
        return True
    face = SITES.get(site, {}).get("region") == "face"
    return bool(face and FACE_ROOT in sc and it.get("site_scope") in SCOPE_FACE)


def direct_site(code: str, site: str) -> bool:
    return bool(set(ITEM[code]["hub"].get("site_codes") or []) & descendants(site))


def groups_of(codes) -> list[str]:
    seen = []
    for c in codes:
        g = GROUP_OF.get(c)
        if g and g not in seen:
            seen.append(g)
    return seen


def named_items(name: str) -> list[str]:
    """R1 진료항목 — 시술 낱말이면 그 시술 · 아니면 묶음 이름 · 진료항목 이름 · 허브 제품 이름에 그 낱말."""
    n = name.replace(" ", "")
    if n in PROC_WORD:
        return [c for c, i in ITEM.items() if PROC_WORD[n] in (i["hub"].get("procedure_codes") or [])]
    return [c for c, i in ITEM.items()
            if n in (i.get("kos_procedure") or "").replace(" ", "")
            or n in (i.get("kos_item_name") or "").replace(" ", "")
            or any(n in (p.get("name") or "").replace(" ", "") for p in i["hub"].get("products") or [])]


def r1_named(name: str, site: str | None) -> list[str]:
    codes = [c for c in named_items(name) if in_site(c, site)]
    if site:  # 그 부위에 바로 매핑된 것 → 자손 부위 → 품는 얼굴 전체 순(하나라도 있으면 그 층만)
        exact = [c for c in codes if site in (ITEM[c]["hub"].get("site_codes") or [])]
        d = [c for c in codes if direct_site(c, site)]
        codes = exact or d or codes
    return groups_of(codes)


def r2_concern(con: str, site: str | None) -> list[str]:
    rows, _ = hub_all("/concern-candidates", {"concern_code": con, "upper": "auto", "to_procedure": "none"}, "groups")
    cases = set()
    for g in rows:
        for r in g.get("rows") or []:
            if r.get("reach") == "케이스 직접" and r.get("candidate_table") == "procedure_case":
                cases.add(r.get("candidate_code"))
    codes = [c for c, i in ITEM.items() if cases & set(i["hub"].get("case_codes") or []) and in_site(c, site)]
    return groups_of(codes)


def r3_effect(eff: str, site: str | None) -> list[str]:
    rows, _ = hub_all("/facets", {"facet": "outcome", "node": f"effect:{eff}"}, "rows")
    cases = {r["target_code"] for r in rows if r.get("target_table") == "procedure_case"}
    procs = {r["target_code"] for r in rows if r.get("target_table") == "procedure"}
    codes = [c for c, i in ITEM.items()
             if (cases & set(i["hub"].get("case_codes") or []) or procs & set(i["hub"].get("procedure_codes") or []))
             and in_site(c, site)]
    return groups_of(codes)


def r7_concern_sites(con: str) -> list[str]:
    _, head = hub_all("/concern-candidates", {"concern_code": con, "upper": "auto", "to_procedure": "none"}, "groups")
    return [s["site_code"] for s in head.get("sites") or [] if s.get("match") in (None, "직접") and s.get("site_code")]


def outside_groups(site: str) -> list[str]:
    """R5 — 그 부위 주제에 있으면 안 되는 묶음(진료항목이 하나도 R4 에 안 듦)."""
    ok = set(groups_of([c for c in ITEM if in_site(c, site)]))
    return [g for g in GROUPS if g not in ok]


def body_groups() -> list[str]:
    """R6 — 몸 묶음: 진료항목 매핑 부위가 모두 얼굴 밖(region ≠ face)이거나 site_scope 가 「몸」 뿐인 묶음
    (0.2 — 겨드랑이제모처럼 「특정 부위」 몸 묶음도 든다 · 검수 P1-2)."""
    out = []
    for g in M["groups"]:
        scopes = {ITEM[c].get("site_scope") for c in g["items"]}
        sites = {x for c in g["items"] for x in ITEM[c]["hub"].get("site_codes") or []}
        if scopes == {"몸"} or (sites and all(SITES.get(x, {}).get("region") != "face" for x in sites)):
            out.append(g["kos_procedure"])
    return out


# ---------- 턴 명세(사람이 쓴 기대 · 규칙 이름만) ----------
S = {"얼굴": "SITE-007", "입꼬리": "SITE-067", "미간": "SITE-015", "눈가": "SITE-019", "팔자": "SITE-046",
     "볼": "SITE-051", "턱": "SITE-072", "턱밑": "SITE-077"}
C = {"볼처짐": "CON-024", "팔자주름": "CON-009", "미간주름": "CON-006", "탄력": "CON-048", "눈가주름": "CON-007", "입꼬리주름": "CON-015",
     "주름": "CON-001", "이중턱": "CON-164", "볼살": "CON-167"}
E = {"타이트닝": "EFF-021"}
LIFT3 = ["소프웨이브", "써마지", "울쎄라"]

# 칸: site(지금 주제 부위 · None = 큰 주제) · must(규칙 목록) · not(규칙) · only(명시 이름 — 이 묶음만) · same_as(턴) ·
#     topic(new · same_as · split · items_same · remember) · said(이 턴에 나온 부위 · 고민 → 점) · ask(답 글이 답할 것) ·
#     crit(이 턴에서 보는 기준 번호) · check(사람 확인 칸 이름)
SPEC = {
    "S01": [
        dict(site="팔자", must=[("concern", "팔자주름", "팔자")], nots=["outside"], said=[("concern", "팔자주름")],
             crit=[1, 4, 7, 10, 11, 13, 22]),
        dict(site="미간", must=[("concern", "미간주름", "미간")], nots=["outside"], said=[("concern", "미간주름")],
             topic={"new": True}, crit=[1, 7, 10, 11, 13, 17, 18, 22]),
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], said=[("site", "얼굴"), ("concern", "탄력")],
             topic={"new": True}, crit=[1, 7, 10, 11, 13, 17, 22]),
        dict(site="얼굴", must=[("named", n, "얼굴") for n in LIFT3], only=LIFT3, topic={"same_as": 3},
             crit=[3, 5, 6, 7, 10, 11, 22]),
        dict(site="얼굴", same_as=4, ask="mechanism", subject="고주파", topic={"same_as": 4}, crit=[1, 6, 8, 9, 10, 11, 15, 22]),
        dict(site="얼굴", same_as=4, ask="overview", subject="고주파", topic={"same_as": 4}, crit=[1, 6, 8, 9, 10, 11, 15, 16, 22]),
    ],
    "S02": [
        dict(site=None, must=[("concern", "탄력", None)], said=[("concern", "탄력")], ask="ask_site", crit=[1, 6, 7, 8, 10, 11, 13, 22],
             check=["S02 T1 부위 없는 「피부 탄력 저하」 — 몸 진료항목(온다 바디 등)도 목록에 두는가"]),
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], said=[("site", "얼굴")],
             topic={"same_as": 1}, crit=[1, 4, 6, 7, 10, 11, 22]),
        dict(site="얼굴", same_as=2, topic={"same_as": 2}, crit=[1, 6, 7, 10, 11, 15, 16, 22]),
    ],
    "S03": [
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], said=[("site", "얼굴"), ("concern", "탄력")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site=("눈가", "입꼬리"), said=[("site", "눈가"), ("site", "입꼬리")],
             topic={"split": ["눈가", "입꼬리"],
                    "topic_must": {"눈가": [("concern", "눈가주름", "눈가")], "입꼬리": [("concern", "입꼬리주름", "입꼬리")]}},
             crit=[7, 10, 11, 17, 18, 22],
             check=["S03 T2 「눈가 · 입꼬리」 둘로 찢은 뒤 지금 주제는 둘 중 아무거나 — 맞는가"]),
        dict(site=("눈가", "입꼬리"), topic={"split": ["눈가", "입꼬리"],
             "remember": {"눈가": "볼뉴머", "입꼬리": "필러"},
             "topic_must": {"눈가": [("named", "볼뉴머", "눈가")], "입꼬리": [("named", "필러", "입꼬리")]},
             "topic_not": {"입꼬리": ["볼뉴머"], "눈가": []}},
             crit=[5, 7, 10, 11, 17, 18, 20, 22]),
        dict(site="입꼬리", must=[("named", "필러", "입꼬리")], not_named=["볼뉴머"], nots=["outside"],
             topic={"remember": {"눈가": "볼뉴머", "입꼬리": "필러"}}, crit=[1, 5, 7, 10, 11, 18, 19, 20, 22]),
    ],
    "S04": [
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], said=[("site", "얼굴"), ("concern", "탄력")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="입꼬리", must=[("concern", "입꼬리주름", "입꼬리")], nots=["outside"], said=[("site", "입꼬리"), ("concern", "입꼬리주름")],
             topic={"new": True}, crit=[1, 4, 7, 10, 11, 17, 18, 22],
             check=["S04 T2 「입꼬리 · 주름」 의 고민 = 입꼬리주름(CON-015) 으로 보는가(「주름」 CON-001 아님)"]),
        dict(site="미간", must=[("concern", "미간주름", "미간")], nots=["outside"], said=[("site", "미간"), ("concern", "미간주름")],
             topic={"new": True}, crit=[1, 7, 10, 11, 17, 18, 22]),
        dict(site="눈가", must=[("named", "써마지", "눈가")], only=["써마지"], nots=["outside"], said=[("site", "눈가")],
             topic={"new": True}, crit=[1, 5, 7, 10, 11, 17, 18, 22]),
        dict(site="입꼬리", must=[("named", "필러", "입꼬리")], not_named=["써마지"], nots=["outside"],
             topic={"same_as": 2, "remember": {"눈가": "써마지", "입꼬리": "필러"}}, crit=[1, 5, 7, 10, 11, 18, 19, 20, 22]),
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], topic={"same_as": 1},
             crit=[1, 7, 10, 11, 21, 22]),
        dict(site=None, ask="remember", remember_words=["써마지"], crit=[8, 10, 11, 15, 20]),
    ],
    "S05": [
        dict(site=None, must=[("named", "써마지", None)], only=["써마지"], crit=[1, 5, 6, 10, 11, 13]),
        dict(dyn="s05t2", site="볼", same_as=1, said=[("site", "볼")], ask="reason", reason_words=["처짐", "처져"],
             topic={"same_as": 1}, crit=[1, 6, 7, 8, 10, 11, 22],
             check=["S05 T2 「볼이 처져서요」(고민 볼처짐 + 부위 볼) — 볼처짐 × 써마지 = 0(허브). 앞 목록 + 까닭(11-20 「0 이면 앞 목록 + 이유」 · 지금 앱)인가 · 부위 볼로 좁힌 목록(아이써마지 뺌 · 지금 정답)인가"]),
        dict(site="볼", must=[("named", "울쎄라", "볼")], only=["울쎄라"], not_named=["써마지"], topic={"same_as": 1, "cond_keep": ["볼"]},
             crit=[1, 2, 5, 7, 10, 11, 22],
             check=["S05 T3 「아니 써마지 말고 울쎄라로」 — 같은 주제 안 고르기 교체(볼 유지 · 지금 정답)인가 · 11-23 「아니 ~ / 그거 말고 = 직전 변화 되돌림」 인가"]),
        dict(site="볼", same_as=2, topic={"same_as": 1}, crit=[2, 7, 10, 11, 22]),
    ],
    "S06": [
        dict(site="얼굴", must=[("effect", "타이트닝", "얼굴")], nots=["body"], said=[("site", "얼굴")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="얼굴", must=[("named", n, "얼굴") for n in LIFT3], only=LIFT3, topic={"same_as": 1},
             crit=[3, 5, 6, 10, 11, 22],
             check=["S06 T2 「그중에서 소프웨이브 · 써마지 · 울쎄라만」 — 소프웨이브 · 울쎄라는 T1 목록(타이트닝 효과 · 허브 outcome)에 없었다. 이름 댄 셋을 다 보이는가(기준 5) · 앞 목록 안에서만 고르는가"]),
        dict(site="얼굴", same_as=1, nots=["body"], topic={"same_as": 1}, crit=[3, 4, 6, 10, 11, 18, 22],
             check=["S06 T3 「다른 시술도 보여줘」 = T1 목록(얼굴 타이트닝 효과는 둠)으로 넓히는가 — 효과까지 비워 얼굴 전체로 넓히는가(11-23 「좁힘 칸 비움」 · 효과는 좁힘 칸)"]),
        dict(site="얼굴", must=[("named", "티타늄리프팅", None), ("named", "포트라", None)], only=["티타늄리프팅", "포트라"],
             topic={"same_as": 1}, crit=[3, 5, 6, 10, 11, 22]),
    ],
    "S07": [
        dict(site=None, must=[("named", "울쎄라", None)], only=["울쎄라"], ask="overview", subject="울쎄라", crit=[1, 5, 6, 8, 9, 10, 11, 13]),
        dict(site=None, same_as=1, ask="mechanism", subject="울쎄라", crit=[1, 6, 8, 9, 10, 11, 16]),
        dict(site=None, same_as=1, ask="adverse", crit=[1, 6, 8, 9, 10, 11, 12, 16]),
        dict(site=None, same_as=1, ask="price", crit=[1, 8, 10, 11, 14]),
    ],
    "S08": [
        dict(site="턱", must=[("named", "보톡스", "턱")], only=["보톡스"], nots=["outside"], said=[("site", "턱")],
             ask="effect_adverse", crit=[1, 5, 6, 7, 8, 10, 11, 12, 22]),
        dict(site="턱", must=[("named", "하이톡스", "턱")], only=["하이톡스"], topic={"same_as": 1}, crit=[1, 5, 7, 10, 11, 22]),
        dict(site="턱", same_as=2, ask="price", crit=[1, 8, 10, 11, 14]),
    ],
    "S09": [
        dict(site="얼굴", must=[("effect", "타이트닝", "얼굴")], nots=["body"], said=[("site", "얼굴")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="얼굴", same_as=1, ask="outside", out_names=["실리프팅", "실 리프팅"], crit=[1, 8, 9, 10, 11, 13],
             check=["S09 T2 · T3 명동점 밖 시술을 물을 때 목록 = 앞 목록 그대로(11-20 「0 이면 앞 목록 + 이유」 · 정보 질문)인가 — 고르기 교체로 0(11-23 「교체로 0 이면 막지 않고 말함」)인가"]),
        dict(site="얼굴", same_as=1, ask="outside", out_names=["인모드"], crit=[1, 8, 9, 10, 11, 13],
             check=["S09 T2 · T3 명동점 밖 시술을 물을 때 목록 = 앞 목록 그대로(11-20 「0 이면 앞 목록 + 이유」 · 정보 질문)인가 — 고르기 교체로 0(11-23 「교체로 0 이면 막지 않고 말함」)인가"]),
        dict(site="얼굴", same_as=1, ask="absent", out_names=["모발이식"], crit=[1, 8, 9, 10, 11, 13]),
    ],
    "S10": [
        dict(site="턱", must=[("named", "보톡스", "턱")], only=["보톡스"], nots=["outside"], said=[("site", "턱")],
             ask="safety", crit=[1, 5, 6, 7, 8, 10, 11, 12, 22]),
        dict(site="턱", same_as=1, topic={"same_as": 1}, crit=[1, 6, 10, 11, 16]),
        dict(site="턱밑", must=[("concern", "이중턱", "턱밑")], nots=["outside"], said=[("concern", "이중턱")],
             topic={"new": True}, crit=[1, 7, 10, 11, 17, 18, 22],
             check=["S10 T3 「턱이 이중턱이라고」 — 턱 보톡스 주제와 다른 새 주제(이중턱 · 턱밑)로 보는가"]),
        dict(site="볼", must=[("concern", "볼살", "볼")], nots=["outside"], said=[("concern", "볼살")], topic={"new": True},
             crit=[1, 7, 10, 11, 17, 18, 22]),
        dict(site="미간", must=[("concern", "미간주름", "미간")], nots=["outside"], said=[("concern", "미간주름")],
             topic={"new": True}, crit=[1, 7, 10, 11, 17, 18, 22]),
        dict(site="미간", same_as=5, ask="other_options", other_than="보톡스", crit=[1, 8, 9, 10, 11, 15]),
    ],
    "S12": [  # 0.3 덮음 보탬(검수 P2-a) — 21 · 19 · 14 · 12
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], said=[("site", "얼굴"), ("concern", "탄력")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="눈가", must=[("concern", "눈가주름", "눈가")], nots=["outside"], said=[("site", "눈가"), ("concern", "눈가주름")],
             topic={"new": True}, crit=[1, 6, 7, 10, 11, 17, 18, 22]),
        dict(site="얼굴", must=[("concern", "탄력", "얼굴")], nots=["body"], topic={"same_as": 1},
             crit=[1, 6, 7, 10, 11, 21, 22]),
        dict(site="눈가", must=[("named", "아이써마지", "눈가")], only=["아이써마지"], nots=["outside"], topic={"same_as": 2},
             crit=[1, 3, 5, 6, 7, 10, 11, 18, 19, 20, 22]),
        dict(site="눈가", same_as=4, ask="price", crit=[1, 6, 8, 10, 11, 14]),
        dict(site="눈가", same_as=4, ask="adverse", subject="써마지", crit=[1, 6, 8, 9, 10, 11, 12, 16]),
    ],
    "S13": [  # 0.3 덮음 보탬 — 21 · 19 · 12 · 14
        dict(site="얼굴", must=[("effect", "타이트닝", "얼굴")], nots=["body"], said=[("site", "얼굴")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="입꼬리", must=[("concern", "입꼬리주름", "입꼬리")], nots=["outside"], said=[("site", "입꼬리"), ("concern", "입꼬리주름")],
             topic={"new": True}, crit=[1, 6, 7, 10, 11, 17, 18, 22]),
        dict(site="얼굴", must=[("effect", "타이트닝", "얼굴")], nots=["body"], topic={"same_as": 1},
             crit=[1, 6, 7, 10, 11, 21, 22]),
        dict(site="입꼬리", same_as=2, topic={"same_as": 2}, crit=[1, 2, 6, 7, 10, 11, 18, 19, 22]),
        dict(site="입꼬리", same_as=4, ask="adverse", subject="필러", crit=[1, 6, 8, 9, 10, 11, 12]),
        dict(site="입꼬리", same_as=4, ask="price", crit=[1, 8, 10, 11, 14]),
    ],
    "S11": [
        dict(site="팔자", must=[("concern", "팔자주름", "팔자")], nots=["outside"], said=[("concern", "팔자주름")],
             crit=[1, 6, 7, 10, 11, 13, 22]),
        dict(site="미간", must=[("concern", "미간주름", "미간")], nots=["outside"], said=[("site", "미간"), ("concern", "미간주름")],
             topic={"new": True, "items_same": {"팔자": 1}}, crit=[1, 7, 10, 11, 17, 18, 22]),
        dict(site="미간", must=[("named", "보톡스", "미간")], only=["보톡스"], nots=["outside"],
             topic={"same_as": 2, "items_same": {"팔자": 1}}, crit=[1, 5, 7, 10, 11, 18, 22],
             check=["S11 T3 「보톡스로 맞고 싶어서」 — 지금 주제(미간)에 붙이는 게 맞는가(팔자 주제는 그대로)"]),
        dict(site="미간", must=[("named", "보톡스", "미간")], only=["보톡스"], nots=["outside"],
             topic={"same_as": 2, "items_same": {"팔자": 1}}, crit=[1, 2, 7, 10, 11, 15, 18, 22]),
        dict(site=None, topic={"items_same": {"팔자": 1}}, crit=[2, 10, 11, 15, 18]),
        dict(site=None, ask="confirm", topic={"items_same": {"팔자": 1}}, crit=[8, 9, 10, 11, 15]),
        dict(site=None, must=[("named", "볼뉴머", None)], ask="overview", subject="볼뉴머", crit=[5, 8, 9, 10, 11]),
    ],
}


# 0.3 — 사용자 결정(11-23 「응 추천대로해」) · 칸 머리 글로 찾는다
DATA_WAIT = ("R2 고민 팔자주름", "R2 고민 입꼬리주름", "R3 효과 타이트닝")
DATA_WAIT_GOLD = "661335b6"  # 데이터 고침 전 gold — 이 gold 일 때만 위 셋을 「데이터 고침 대기」 로 둔다(새 gold = 확정)
DECIDED = {
    "R2 고민": "허브 관계 그대로 확정",
    "R3 효과": "허브 관계 그대로 확정",
    "S02 T1": "몸 진료항목도 둠 + 봇이 부위를 물음(기준 8 「부위 물음」)",
    "S03 T2": "둘 중 아무 주제나 지금 주제가 됨",
    "S04 T2": "입꼬리주름(CON-015)",
    "S05 T2": "앞 목록 + 까닭(11-20) — 목록 = T1 · 답에 「볼처짐으로는 없다」",
    "S05 T3": "교체(볼 유지) — 바꿀 이름 없는 「아니 그거 말고」 만 되돌림",
    "S06 T2": "이름 댄 셋 다(앞 목록 밖이어도)",
    "S06 T3": "첫 목록(효과는 남김 · 시술 · 제품 · 국가 · 뺌만 비움)",
    "S09 T2": "앞 목록 그대로 + 답으로 「없다」",
    "S10 T3": "새 주제(이중턱 · 턱밑)",
    "S11 T3": "지금 주제(미간)에 붙임",
}


def s05_t2_spec(sp: dict) -> dict:
    """S05 T2 「볼이 처져서요」(T1 = 써마지) — 결정 #10 「0 이면 앞 목록 + 까닭」(11-20) 을 허브 데이터로 가른다.
    볼처짐(R2 @볼) ∩ 써마지(R1 @볼) 묶음이 0 이면 앞 목록 + 까닭(지금 칸 그대로) · 0 이 아니면 좁힌 목록(그 교집합 묶음 · 볼 밖 묶음 안 됨)."""
    con = [g for g in r2_concern(C["볼처짐"], S["볼"])]
    thm = r1_named("써마지", S["볼"])
    inter = [g for g in thm if g in con]
    if not inter:
        return dict(sp, dyn_rec={"rule": "0 → 앞 목록 + 까닭", "concern_groups": con, "pick_groups": thm})
    out = {k: v for k, v in sp.items() if k not in ("same_as", "ask", "reason_words", "dyn")}
    out.update(must=[("named", "써마지", "볼")], only=["써마지"], nots=["outside"],
               crit=[c for c in sp["crit"] if c != 8] + [4],
               dyn_rec={"rule": "0 아님 → 좁힌 목록", "intersection": inter, "concern_groups": con, "pick_groups": thm})
    return out


def resolve_rule(r) -> tuple[list[str], bool, str]:
    kind, name, site = r
    sc = S.get(site) if site else None
    if kind == "named":
        return r1_named(name, sc), False, f"R1 명시 「{name}」" + (f" @{site}" if site else "")
    if kind == "concern":
        return r2_concern(C[name], sc), True, f"R2 고민 {name}({C[name]})" + (f" @{site}" if site else "")
    if kind == "effect":
        return r3_effect(E[name], sc), True, f"R3 효과 {name}({E[name]})" + (f" @{site}" if site else "")
    raise ValueError(kind)


def build() -> dict:
    scs = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text())["scenarios"]}
    body = body_groups()
    out = {"version": "0.3.0", "unit": "진료항목 묶음(매핑 groups[].kos_procedure)", "rules": __doc__, "turns": [],
           "check_cells": []}
    checks = {}
    for sid, specs in SPEC.items():
        assert len(specs) == len(scs[sid]["turns"]), sid
        dots: list[str] = []
        for n, sp in enumerate(specs, 1):
            if sp.get("dyn") == "s05t2":  # WP-4 코디 추가 — 결정 #10 「0 이면 앞 목록 + 까닭」 을 데이터로 가름
                sp = s05_t2_spec(sp)
            t = {"sid": sid, "n": n, "q": scs[sid]["turns"][n - 1]["text"], "crit": sp["crit"]}
            if sp.get("dyn_rec"):
                t["dyn"] = sp["dyn_rec"]
            site = sp.get("site")
            sites = [S[x] for x in site] if isinstance(site, tuple) else ([S[site]] if site else [])
            t["topic_sites"] = sites
            t["big"] = site == "얼굴" or site is None
            must, must_why, rule_checks = [], [], []
            for r in sp.get("must", []):
                gs, chk, why = resolve_rule(r)
                must_why.append({"rule": why, "groups": gs, "check": chk})
                must += [g for g in gs if g not in must]
                if chk:
                    key = why
                    checks.setdefault(key, {"cell": why, "groups": gs, "turns": []})["turns"].append(f"{sid} T{n}")
            t["must"] = must
            t["must_why"] = must_why
            nots = []
            if "outside" in sp.get("nots", []) and len(sites) == 1:
                nots += outside_groups(sites[0])
            if "body" in sp.get("nots", []):
                nots += [g for g in body if g not in nots]
            for nm in sp.get("not_named", []):
                nots += [g for g in r1_named(nm, None) if g not in nots and g not in must]
            t["must_not"] = nots
            if sp.get("only"):  # 이 이름만 — 진료항목 단위(같은 묶음 안 제품 좁히기도 본다)
                only, items = [], []
                for nm in sp["only"]:
                    only += [g for g in r1_named(nm, None) if g not in only]
                    items += [c for c in named_items(nm) if c not in items]
                t["only"] = only
                t["only_items"] = items
            if sp.get("same_as"):
                t["same_as"] = sp["same_as"]
            tp = dict(sp.get("topic") or {})
            for k in ("topic_must", "topic_not"):
                if k in tp:
                    res = {}
                    for st, rules in tp[k].items():
                        if k == "topic_must":
                            res[S[st]] = []
                            for r in rules:
                                gs, chk, why = resolve_rule(r)
                                res[S[st]] += [g for g in gs if g not in res[S[st]]]
                                if chk:
                                    checks.setdefault(why, {"cell": why, "groups": gs, "turns": []})["turns"].append(f"{sid} T{n}")
                        else:
                            res[S[st]] = [g for nm in rules for g in r1_named(nm, None)]
                    tp[k] = res
            if "split" in tp:
                tp["split"] = [S[x] for x in tp["split"]]
            if "items_same" in tp:
                tp["items_same"] = {S[k]: v for k, v in tp["items_same"].items()}
            if "cond_keep" in tp:  # 0.3 — 지금 주제 조건에 남아 있어야 할 부위(교체 = 볼 유지 · 사용자 결정 #11)
                tp["cond_keep"] = [S[x] for x in tp["cond_keep"]]
            if "remember" in tp:
                tp["remember"] = {S[k]: v for k, v in tp["remember"].items()}
            t["topic"] = tp
            for kind, nm in sp.get("said", []):
                add = [S[nm]] if kind == "site" else r7_concern_sites(C[nm])
                dots += [x for x in add if x not in dots]
            t["dots"] = list(dots)
            if sp.get("ask"):
                t["ask"] = sp["ask"]
            for k in ("out_names", "remember_words", "other_than", "subject", "reason_words"):
                if k in sp:
                    t[k] = sp[k]
            if sp.get("ask") == "other_options":
                t["other_groups"] = [g for g in r2_concern(C["미간주름"], S["미간"]) if g not in r1_named("보톡스", None)]
            for c in sp.get("check", []):
                checks.setdefault(c, {"cell": c, "groups": None, "turns": []})["turns"].append(f"{sid} T{n}")
            out["turns"].append(t)
    # SPEC-012 0.1.2 C5 — 정답표를 만든 허브 gold(GET /health) · score.py 가 측정 gold 와 견줌
    try:
        with urllib.request.urlopen(f"{HUB}/health", timeout=20) as r:
            b = json.loads(r.read()).get("build") or {}
        out["gold_hash"], out["aux_hash"] = b.get("gold_hash"), b.get("aux_hash")
    except Exception:  # noqa: BLE001
        out["gold_hash"] = None
    # SPEC-012 C5(WP-0 · 11-23) — 데이터 고침(data-gap3) 뒤 gold 면 대기 칸은 그 gold 의 허브 관계로 확정한다
    wait = DATA_WAIT if (out.get("gold_hash") or "").startswith(DATA_WAIT_GOLD) else ()
    out["data_wait_applied"] = bool(wait)
    for c in checks.values():
        key = next((k for k in DECIDED if c["cell"].startswith(k)), None)
        if any(c["cell"].startswith(k) for k in wait):
            c["status"], c["decision"] = "데이터 고침 대기", "허브 관계 그대로 확정 · 허브 새 gold 가 나오면 다시 만든다(data-gap3-task.md)"
        elif key:
            c["status"], c["decision"] = "확정", DECIDED[key]
        else:
            c["status"], c["decision"] = "확인 필요", ""
    out["check_cells"] = list(checks.values())
    out["n_check"] = sum(1 for c in out["check_cells"] if c["status"] == "확인 필요")
    out["n_data_wait"] = sum(1 for c in out["check_cells"] if c["status"] == "데이터 고침 대기")
    # 밖 이름 사전(R9 기준 13): 허브 제품 이름 가운데 명동점 매핑 제품이 아닌 것
    return out


def write_md(ans: dict) -> None:
    L = [f"# 정답표 — 상담 품질 기준선 (v{ans['version']})", "",
         f"허브 gold `{(ans.get('gold_hash') or '?')[:16]}…` · **확인 필요 칸 = {ans['n_check']}** · 데이터 고침 대기 칸 = {ans.get('n_data_wait', 0)}(허브 새 gold 뒤 `build_answers.py` 로 다시 만든다) · 사용자 결정 11-23 반영.", "",
         f"단위 = {ans['unit']} · 규칙 R1 ~ R8 은 `build_answers.py` 머리 주석 · 값은 매핑 JSON · 허브 18105 GET 으로만 풀었다.", "",
         "## 규칙 결과 0 묶음(빈 정답 — 그 턴 목록 판정 1 · 4 · 21 은 na · 확인 필요)", ""]
    zero = [c for c in ans["check_cells"] if c["groups"] == []]
    L += [f"- {c['cell']} → 0 묶음 · 턴 {' · '.join(c['turns'])}" for c in zero] or ["- 없음"]
    L += ["", "## 정답 칸(앞 「확인 필요」 19 칸 → 사용자 결정)", "", "| # | 칸 | 규칙 결과(묶음) | 상태 | 결정 | 쓰는 턴 |", "|---:|---|---|---|---|---|"]
    for i, c in enumerate(ans["check_cells"], 1):
        gs = " · ".join(c["groups"]) if c["groups"] is not None else "(판단)"
        L.append(f"| {i} | {c['cell']} | {gs if gs else '(0)'} | {c.get('status')} | {c.get('decision', '')} | {' · '.join(c['turns'])} |")
    L += ["", "## 턴별 정답", ""]
    cur = None
    for t in ans["turns"]:
        if t["sid"] != cur:
            cur = t["sid"]
            L += ["", f"### {cur}", "", "| 턴 | 손님 말 | 주제 부위 | 꼭 있음 | 있으면 안 됨 | 이 묶음만 | 목록 = 턴 | 주제 | 점(쌓임) | 답 | 기준 |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        sites = " · ".join(SITES[s]["name"] for s in t["topic_sites"]) or "(큰 주제 · 부위 없음)"
        must = " · ".join(t["must"]) or "—"
        nots = f"R5/R6 {len(t['must_not'])} 묶음" if len(t["must_not"]) > 6 else (" · ".join(t["must_not"]) or "—")
        only = " · ".join(t.get("only", [])) or "—"
        tp = json.dumps({k: v for k, v in t["topic"].items() if k not in ("topic_must", "topic_not")}, ensure_ascii=False) if t["topic"] else "—"
        dots = " · ".join(SITES[s]["name"] for s in t["dots"]) or "—"
        L.append(f"| T{t['n']} | {t['q']} | {sites} | {must} | {nots} | {only} | {t.get('same_as', '—')} | {tp} | {dots} | {t.get('ask', '—')} | {','.join(map(str, t['crit']))} |")
    (HERE / "answers.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    ans = build()
    (HERE / "answers.json").write_text(json.dumps(ans, ensure_ascii=False, indent=1))
    write_md(ans)
    print("turns", len(ans["turns"]), "check", ans["n_check"], "data_wait", ans["n_data_wait"])
    for t in ans["turns"]:
        print(t["sid"], t["n"], "must", t["must"][:12], "| not", len(t["must_not"]), "| only", t.get("only"), "| dots", t["dots"])
