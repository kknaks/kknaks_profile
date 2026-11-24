"""채점 — `answers.json` 기준으로 run.py 결과(`out/<tag>/turns.jsonl`)를 기준 22 개로 판정한다.

실행: python3 score.py out/base-<시각>   → 그 폴더에 score.json · score.md(표) · human.md(사람 판정 표)
판정 값: pass · fail · na(이 턴에 볼 것 없음) · human(사람 판정 — human.md) · pending 표지(「확인 필요」 칸에 기대는 판정 — 따로 셈)

채점 0.4(재검수 r3 P2-2 · P2-5 · P2-6 · 2026-11-23): 기준 13 밖 이름에 매핑 밖 패키지(kind 메뉴) · `ask_site` = 부위를 묻는
물음 문장(부위 · 어디 · 어느 쪽 또는 부위 이름 둘) · `no_here` 부정에 「다루지 않」 · 하위 칸 23(안 물은 안전 먼저 꺼냄 — 합계 밖).

채점 0.6(검수 r4 P2-2 · P2-3 · P2-4 · 2026-11-24): 기준 11 에 값 · 자료 사정 바꿔 말한 꼴(「…이 같이 · 함께 있」 · 「엇갈려」 ·
「자료상 · 자료로 · 자료에」) · 기준 14 값마다 가장 가까운 앞 이름(진료항목 · 옵션 이름)과 짝 · 하위 칸 24(안 물은 같은 날 줄 — 합계 밖).
채점 0.5(코디 ④ · 2026-11-24): 기준 11 의 「확인(이) 필요」 는 자료 · 메모 · 목록 사정 문장(같은 문장에 자료 · 구성 · 목록 · 가격 …)일
때만 실패로 친다(손님 쪽 금기 · 복용 확인 안내는 내부 사정 아님). 다른 금지말은 그대로. 0.4 판은 바꾼 판정 수를 리포트에 적는다.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = Path("/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo")
W = HERE.parent
M = json.loads((A / "data/kos/myeongdong-mapping-20261120-v3.json").read_text())
SITES = dict(M["sites"]) if isinstance(M["sites"], list) else M["sites"]
ITEM = {i["kos_item_code"]: i for i in M["items"]}
GROUP_OF = {c: g["kos_procedure"] for g in M["groups"] for c in g["items"]}
PRICE_SONNET = {"input": 2.0, "cache_creation": 2.5, "cache_read": 0.10, "output": 10.0}  # $/MTok(발주서 값)
CRIT = list(range(1, 23))  # 22 기준(합계 · 전 → 후 비교는 이것만)
SUB = [23, 24]  # 0.4(재검수 r3 P2-6) — 기준 8 · 16 하위 판정 칸(합계와 따로 센다)
ALL = CRIT + SUB
CRIT_NAME = {
    1: "의도 → 맞는 진료항목", 2: "말 바꾸면 원래로", 3: "좁히기 · 넓히기", 4: "부위만 말할 때 거름", 5: "직접 말한 시술 안 빠짐",
    6: "실행마다 같은 목록", 7: "얼굴 점 = 목록", 8: "물은 것에 답", 9: "지어내지 않음", 10: "모르면 돌려 말함",
    11: "메모 · 내부 사정 안 읽음", 12: "안전 안 빠뜨림", 13: "명동점 기준", 14: "가격 · 회차 = 매핑 값",
    15: "앞 말과 안 어긋남", 16: "되풀이 안 함", 17: "큰 주제 → 부위 나눔", 18: "나눈 주제 안 섞임", 19: "부위 사이 오감",
    20: "부위마다 고른 것 기억", 21: "큰 주제로 오면 전체", 22: "주제 표시 = 점",
    23: "(8 · 16 하위) 안 물은 안전 먼저 안 꺼냄",
    24: "(8 · 16 하위) 안 물은 같은 날 줄 안 꺼냄",
}
SAMEDAY_ASK = ("same_day", "combo")  # 0.6 — 정답표 ask 가운데 같은 날 · 같이 받기를 물은 턴(지금 시나리오에는 없음)
RX_SAMEDAY = re.compile(r"같은\s?날[^.?!\n]{0,40}")
SAFE_ASK = ("adverse", "effect_adverse", "safety")  # 정답표 ask 가운데 안전을 물은 턴
# 0.4(r3 P2-6) — 안전 내용 문장: 증상 낱말과 「생길 수 있음 · 일시적 · 부작용」 꼴이 한 문장에 · 또는 금기 · 피할 사람. 물음 문장은 안 침
_SYM = r"(붓기|부기|부종|멍|통증|홍조|홍반|열감|화상|따끔|저림|두통|염증|결절|괴사|붉어)"
_MK = r"(수\s?있|일시적|부작용|생기|생길|나타|드물|지속)"
RX_SAFETY_FIRST = re.compile(rf"{_SYM}[^.\n]*{_MK}|{_MK}[^.\n]*{_SYM}|금기|임신|수유|피해야|받으시면\s?안")
HUMAN = {9, 15}  # 기계 대리 판정 + 사람 판정 표


# ---------- 사전 ----------
def price_set() -> set[int]:
    out = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if isinstance(x, (int, float)) and ("price" in k or "amount" in k) and x:
                    out.add(int(x))
                else:
                    walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(M.get("products"))
    walk([i.get("options") for i in M["items"]])
    return out


PRICES = price_set()


def mapping_words() -> set[str]:
    w = set()
    for i in M["items"]:
        for x in (i.get("kos_item_name"), i.get("kos_procedure"), i.get("kos_machine"), i.get("kos_medicine")):
            if x:
                w.add(x.replace(" ", ""))
        for p in i["hub"].get("products") or []:
            w.add((p.get("name") or "").replace(" ", ""))
    return w


COMMON = {"시크릿", "아이콘", "미라클", "리저브", "인피니", "고우리", "더채움", "제니스"}  # 보통 말로도 쓰는 낱말 — 밖 이름 판정에서 뺌


def out_lexicon() -> list[str]:
    """허브 제품 이름 가운데 명동점 매핑 낱말 어디에도 들지 않는 것(3 자 이상) + 시술 · 계열 이름(0.2) — 기준 13."""
    mw = mapping_words()
    out = []
    with (W / "silver-model/silver/product.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            n = (r.get("name_ko") or "").replace(" ", "")
            if len(n) >= 3 and n not in COMMON and not any(n in x for x in mw):
                out.append(n)
    # 0.2(검수 P1-3) — 허브 시술 · 계열 이름 가운데 명동점 매핑 시술(hub.procedure_codes) · 그 계열에 없는 것
    pin = {p for i in M["items"] for p in i["hub"].get("procedure_codes") or []}
    with (W / "silver-model/silver/procedure.csv").open(encoding="utf-8-sig") as f:
        procs = list(csv.DictReader(f))
    min_ = {r["modality_code"] for r in procs if r["code"] in pin}
    with (W / "silver-model/silver/modality.csv").open(encoding="utf-8-sig") as f:
        mods = list(csv.DictReader(f))
    names = [r["name_ko"] for r in procs if r["code"] not in pin] + [r["name_ko"] for r in mods if r["code"] not in min_]
    for nm in names:
        for part in (nm or "").split("/"):
            n = part.replace(" ", "")
            if len(n) >= 2 and n not in COMMON and not any(n in x for x in mw):
                out.append(n)
    out += out_packages(mw)
    return sorted(set(out), key=len, reverse=True)


PACKAGE_MENU = "메뉴"  # silver package.kind 값 — 이름 붙은 메뉴(DNA리셋프로그램 · V라인주사). 그 밖 kind 는 「보톡스 + 필러」 같은 조합 설명


def out_packages(mw: set[str] | None = None) -> list[str]:
    """0.4(재검수 r3 P2-2) — 매핑(v3 — 패키지 칸 없음)에 없는 허브 패키지 이름 가운데 kind 「메뉴」(이름 붙은 상품) · 3 자 이상 ·
    매핑 낱말에 들지 않는 것 — 기준 13 밖 이름."""
    mw = mapping_words() if mw is None else mw
    out = []
    with (W / "silver-model/silver/package.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            n = (r.get("name") or "").replace(" ", "")
            if r.get("kind") == PACKAGE_MENU and len(n) >= 3 and n not in COMMON and not any(n in x for x in mw):
                out.append(n)
    return out


OUT_LEX = out_lexicon()

# ---------- 말 규칙 ----------
RX_BAN10 = re.compile(r"(정보|자료|내용|설명)[가는이은도]?\s*(따로\s*)?(없|부족)|나와\s?있지\s?않|드리기\s?어려|"
                      r"모르겠|새로\s?가져온|확인되지\s?않|파악(이|하기)?\s?어렵|개요[^.\n]{0,8}(모르|없)")
RX_BAN11 = re.compile(r"값이\s?(같이|둘\s?다|따로)|(안내|값|설명|내용|정보)[가이도]?\s?(같이|함께)\s?(있|나와|적혀)|엇갈|자료\s?(상|로|에)|적혀\s?있|목록에[^.\n]{0,20}없|설명도\s?있고[^.\n]*설명도\s?있|한도|KOS|매핑|허브|구성\s?\d|장부|프롬프트|시스템|내부|목록(을|은)?\s?(고른|골라|뽑)|"
                      r"\b(CAS|PRC|SITE|CON|PRD|EFF|GIN|GEN)-\d{2,}|gid")
# 0.5(코디 ④ · 2026-11-24) — 「확인(이) 필요」 는 자료 · 메모 · 목록 사정 문장일 때만 친다. 손님 쪽 금기 · 복용 확인 안내
# (「…에 해당하면 먼저 확인이 필요해요」 꼴 의학 안내)는 내부 사정이 아니다. 같은 문장에 사정 낱말이 있어야 실패.
RX_CHECK11 = re.compile(r"확인(이)?\s?필요")
RX_SIT11 = re.compile(r"같은\s?날|따로|물으시면|자료|정보|내용|구성|목록|데이터|원문|메모|칸|표기|등록|항목|가격|값|금액|옵션|상품|샷\s?수|회차|용량")


def ban11_check(answer: str):
    """0.5 — 문장마다 「확인 필요」 + 사정 낱말이 함께 있으면 그 「확인 필요」 를 돌려준다(없으면 None)."""
    for sent in re.split(r"(?<=[.?!])\s+|\n+|(?<=요)\s+", answer or ""):
        m = RX_CHECK11.search(sent)
        if m and RX_SIT11.search(sent):
            return m
    return None


KW = {
    "mechanism": r"원리|에너지|열|초음파|고주파|전달|자극|작용",
    "adverse": r"붓기|부기|부종|멍|통증|홍조|홍반|열감|화상|따끔|붉|저림|감각|비대칭|두통|처짐|뻐근|씹|건조|염증|결절|괴사",  # 「부작용」 낱말만으로는 안 됨
    "effect": r"효과|개선|줄여|완화|얇|슬림|각진",
    "price": r"\d[\d,]*\s*원|\d+\s*만\s*\d*\s*천?\s*원",
    "outside": r"명동점",
    "neg": r"없|안\s?해|안\s?하|하지\s?않|진행하지\s?않|않아요|다루지\s?않|취급하지\s?않",  # 0.4(r3 P2-5) 「다루지 않」 더함 · 0.2 — 「어렵 · 어려 · 드리지」 뺌(돌려 막기는 답 아님)
    # 0.2 — 「상담」 · 「주의」 · 「괜찮」 · 「안전」 · 「부작용」 같은 빈 낱말 뺌(「주의할 점은 상담 때 확인」 = 돌려 막기) ·
    # 실제 안전 내용(부작용 증상 · 금기 · 피할 것)이 있어야 함
    "safety": r"붓기|부기|부종|멍|통증|홍조|홍반|열감|화상|따끔|저림|비대칭|두통|뻐근|씹|염증|금기|피해야|임신|수유|근육\s?약|사우나|음주",
}


def money(ans: str) -> list[int]:
    out = []
    for m in re.finditer(r"(\d{1,3}(?:,\d{3})+|\d+)\s*원", ans or ""):
        out.append(int(m.group(1).replace(",", "")))
    for m in re.finditer(r"(\d+)\s*만\s*(?:(\d+)\s*천)?\s*원", ans or ""):
        out.append(int(m.group(1)) * 10000 + (int(m.group(2)) * 1000 if m.group(2) else 0))
    for m in re.finditer(r"(\d+)\s*만\s*(\d{1,4})\s*원", ans or ""):
        out.append(int(m.group(1)) * 10000 + int(m.group(2)))
    return [x for x in out if x >= 1000]


def sentences(ans: str) -> list[str]:
    xs = re.split(r"(?<=[.?!요다])\s+|\n+", ans or "")
    return [re.sub(r"[\s.,!?·\-*()]", "", x) for x in xs if len(re.sub(r"\s", "", x)) >= 12]


def groups(codes) -> list[str]:
    out = []
    for c in codes or []:
        g = GROUP_OF.get(c)
        if g and g not in out:
            out.append(g)
    return out


def anc(s: str) -> list[str]:
    out, c = [], SITES.get(s, {}).get("parent_code")
    while c:
        out.append(c)
        c = SITES.get(c, {}).get("parent_code")
    return out


def face(s: str) -> bool:
    return SITES.get(s, {}).get("region") == "face"


# ---------- 판정 ----------
def verdict(ok: bool | None, why: str = "", pending: bool = False) -> dict:
    return {"v": "na" if ok is None else ("pass" if ok else "fail"), "why": why, "pending": pending}


def judge(t: dict, rec: dict, conv: dict[int, dict], ans: dict) -> dict[int, dict]:
    """한 턴(한 실행) — 기준 번호 → 판정."""
    L = rec.get("ledger") or {}
    scr = rec.get("screen") or {}
    G = groups(scr.get("cards"))
    items = set(scr.get("cards") or [])
    answer = L.get("answer") or ""
    cs = L.get("consult") or {}
    topics = cs.get("topics") or []
    active = cs.get("active_topic")
    # 0.3 — 사용자 결정으로 확정된 칸은 확정으로 센다 · 「데이터 고침 대기」 · 「확인 필요」 칸만 따로
    open_cells = {c["cell"] for c in ans["check_cells"] if c.get("status", "확인 필요") != "확정"}
    pend_must = any(w["check"] and w["rule"] in open_cells for w in t.get("must_why", []))
    pend_turn = any(f"{t['sid']} T{t['n']}" in c["turns"] and c["groups"] is None and c["cell"] in open_cells
                    for c in ans["check_cells"])
    out: dict[int, dict] = {}
    crit = set(t["crit"])

    def prevG(k):
        r = conv.get(k)
        return groups((r or {}).get("screen", {}).get("cards")) if r else None

    def prev_active(k):
        r = conv.get(k)
        return ((r or {}).get("ledger") or {}).get("consult", {}).get("active_topic") if r else None

    if L.get("error") or rec.get("event") != "done":
        return {c: verdict(False, f"턴 오류 {rec.get('event')} {L.get('error')}") for c in crit}

    if not answer.strip():  # 0.2 — 빈 답은 답 글 기준 모두 fail(낱말 없음 = 통과 막기)
        for c in crit & {8, 9, 10, 11, 12, 13, 14, 16}:
            out[c] = verdict(False, "답 없음")
    empty_must = any(w["check"] and not w["groups"] for w in t.get("must_why", []))  # 빈 정답(데이터 고침 대기)
    must, nots = t.get("must", []), t.get("must_not", [])
    miss = [g for g in must if g not in G]
    bad = [g for g in nots if g in G]
    if 1 in crit:
        if t.get("same_as") and not must:
            pg = prevG(t["same_as"])
            same = set(pg or []) == set(G)
            out[1] = verdict(same, f"목록 ≠ T{t['same_as']} — 지금 {len(G)} 묶음 / 그때 {len(pg or [])}" if not same else "", pend_must)
        elif must or nots:
            out[1] = verdict(not miss and not bad, f"빠짐 {miss} · 섞임 {bad[:5]}" if (miss or bad) else "", pend_must or pend_turn)
    if 2 in crit:
        if t.get("same_as"):
            pg = prevG(t["same_as"])
            same = set(pg or []) == set(G)
            out[2] = verdict(same, f"T{t['same_as']} 로 안 돌아감 — 지금 {G[:6]} / 그때 {(pg or [])[:6]}" if not same else "")
        elif t["topic"].get("items_same"):
            pass  # 18 에서 본다
        else:
            nn = [g for g in nots if g in G]
            out[2] = verdict(not miss and not nn, f"빠짐 {miss} · 남음 {nn[:5]}" if (miss or nn) else "")
        if t["topic"].get("items_same") and 2 not in out:
            out[2] = topic_items_same(t, topics, conv)
    if 2 in crit and t["topic"].get("cond_keep"):  # 0.3 — 교체 뒤에도 지금 주제 조건에 부위가 남았나
        cur_t = next((x for x in topics if x.get("id") == active), {})
        have = {v.get("code") for v in ((cur_t.get("conditions") or {}).get("site") or [])}
        lost = [SITES[x]["name"] for x in t["topic"]["cond_keep"] if x not in have]
        if lost:
            out[2] = verdict(False, f"조건에서 부위 {lost} 가 빠짐(되돌림이 앞 턴 부위까지 지움)")
    if 3 in crit:
        if t.get("only_items"):
            extra = sorted(items - set(t["only_items"]))
            out[3] = verdict(not extra and not miss, f"좁힘 밖 {groups(extra)[:6]} · 빠짐 {miss}" if (extra or miss) else "")
        elif t.get("same_as"):
            pg = prevG(t["same_as"])
            same = set(pg or []) == set(G)
            out[3] = verdict(same, f"넓히기 ≠ T{t['same_as']} — 지금 {len(G)} 묶음 / 그때 {len(pg or [])}" if not same else "")
    if 4 in crit:
        out[4] = verdict(not miss and not bad, f"빠짐 {miss} · 부위 밖 {bad[:5]}" if (miss or bad) else "", pend_must)
    if 5 in crit:
        named = [g for w in t.get("must_why", []) if w["rule"].startswith("R1") for g in w["groups"]]
        tm = t["topic"].get("topic_must") or {}
        if named:
            m5 = [g for g in named if g not in G]
            out[5] = verdict(not m5, f"빠짐 {m5}" if m5 else "")
        elif tm and t["topic"].get("remember"):
            m5 = []
            for s, gs in tm.items():
                tp = topic_with(topics, s)
                tg = groups((tp or {}).get("items"))
                m5 += [f"{SITES[s]['name']}:{g}" for g in gs if g not in tg]
            out[5] = verdict(not m5, f"빠짐 {m5}" if m5 else "")
    if 7 in crit:
        shown = [d["site"] for d in scr.get("dots") or []]
        exp = [s for s in t.get("dots") or [] if face(s)]
        lack = [SITES[s]["name"] for s in exp if s not in shown]
        stray = [SITES.get(s, {}).get("name", s) for s in dict.fromkeys(shown) if s not in exp]
        out[7] = verdict(not lack and not stray, f"점 빠짐 {lack} · 군점 {stray}" if (lack or stray) else "")
    if 8 in crit and 8 not in out:
        out[8] = answer_kind(t, answer, L)
    if 9 in crit:
        pr = [x for x in money(answer) if x not in PRICES]
        absent = t.get("ask") == "absent" and bool(re.search(KW["price"], answer))
        out[9] = verdict(not pr and not absent, f"매핑에 없는 값 {pr[:3]}" if pr else ("없는 시술에 값" if absent else ""))
        out[9]["human"] = True
    if 10 in crit:
        m = RX_BAN10.search(answer)
        out[10] = verdict(not m, f"「{m.group(0)}」" if m else "")
    if 11 in crit:
        m = RX_BAN11.search(answer) or ban11_check(answer)
        out[11] = verdict(not m, f"「{m.group(0)}」" if m else "")
    if 12 in crit:
        kinds = set(L.get("kinds") or [])
        a = bool(re.search(KW["adverse"], strip_deflect(answer)))
        k = bool(kinds & {"adverse", "contraindication", "recovery", "avoid"})
        out[12] = verdict(a and k, ("" if a else "답에 부작용 말 없음 ") + ("" if k else f"종류 {sorted(kinds)} 에 안전 없음"))
    if 13 in crit:
        out[13] = branch_check(t, answer)
    if 14 in crit:
        out[14] = price_check(t, answer, scr.get("cards") or [])
    if 15 in crit:
        out[15] = {"v": "human", "why": "", "pending": False, "human": True}
    if 16 in crit:
        mine = sentences(answer)
        before = {s for k, r in conv.items() if k < t["n"] for s in sentences(((r or {}).get("ledger") or {}).get("answer") or "")}
        rep = [s for s in mine if s in before]
        ratio = len(rep) / len(mine) if mine else 0
        out[16] = verdict(ratio <= 0.34, f"앞 답과 같은 문장 {len(rep)}/{len(mine)}" if ratio > 0.34 else "")
    if 17 in crit:
        out[17] = split_check(t, topics, active, conv)
    if 18 in crit:
        out[18] = mix_check(t, topics, conv)
    if 19 in crit:
        k = t["topic"].get("same_as")
        if k is not None:
            out[19] = verdict(prev_active(k) == active, f"주제 {active} ≠ T{k} 주제 {prev_active(k)}" if prev_active(k) != active else "")
        else:  # 앞에서 연 그 부위 주제로 돌아왔나(그 부위를 가진 앞 턴 주제 id)
            s0 = (t.get("topic_sites") or [None])[0]
            prev_ids = {x.get("id") for k2, r2 in conv.items() if k2 < t["n"]
                        for x in ((r2 or {}).get("ledger") or {}).get("consult", {}).get("topics") or [] if s0 in (x.get("sites") or [])}
            out[19] = verdict(active in prev_ids, f"주제 {active} 가 앞 턴의 {SITES.get(s0, {}).get('name')} 주제 {sorted(prev_ids)} 아님" if active not in prev_ids else "")
    if 20 in crit:
        out[20] = remember_check(t, topics, answer)
    if 21 in crit:
        k = t["topic"].get("same_as")
        same = prev_active(k) == active
        tp = next((x for x in topics if x.get("id") == active), {})
        only_site = tp.get("sites") and all(s != "SITE-007" for s in tp.get("sites"))
        out[21] = verdict(same and not miss and not only_site,
                          ("" if same else f"주제 {active} ≠ T{k} {prev_active(k)} ") + (f"빠짐 {len(miss)} 묶음 " if miss else "")
                          + ("부위 목록만 " if only_site else ""), pend_must)
    if 22 in crit:
        out[22] = display_check(t, scr, topics, active)
    if answer.strip() and 12 not in crit and t.get("ask") not in SAFE_ASK:  # 0.4 — 안전을 안 물은 턴 전부
        hit = next((m.group(0) for x in re.split(r"(?<=[.?!])\s+|\n+", strip_deflect(answer)) if "?" not in x
                    for m in [RX_SAFETY_FIRST.search(x)] if m), None)
        out[23] = verdict(not hit, f"묻지 않은 안전을 먼저 꺼냄 「{hit[:30]}」" if hit else "")
    if answer.strip() and t.get("ask") not in SAMEDAY_ASK:  # 0.6(검수 r4 P2-4) — 같은 날 · 같이 받기를 안 물은 턴 전부
        hit = next((m.group(0) for x in re.split(r"(?<=[.?!])\s+|\n+", answer) if "?" not in x
                    for m in [RX_SAMEDAY.search(x)] if m), None)
        out[24] = verdict(not hit, f"묻지 않은 같은 날 줄 「{hit[:30]}」" if hit else "")
    if empty_must:  # 0.2(검수 P2-2) — 꼭 있음 규칙이 0 묶음이면 목록 판정은 하지 않음(빈 정답 · 확인 필요)
        for c in (1, 4, 21):
            if c in out:
                out[c] = {"v": "na", "why": "빈 정답(규칙 결과 0 묶음 · 확인 필요)", "pending": True, "empty": True}
    for c in (2, 3):  # 0.2 — 볼 것이 없던 판정은 na(낱말 없음 = 통과 막기)
        if c in out and out[c]["v"] == "pass" and not (t.get("same_as") or t.get("only_items") or must
                                                       or nots or t["topic"].get("items_same")):
            out[c] = verdict(None, "볼 것 없음")
    k = t.get("same_as")
    if k and conv.get(k) is not None:  # 0.2(검수 P2-5) — 기대 턴이 틀렸으면 따라 fail · 확인 필요면 따라 확인 필요
        pv = conv[k].get("_v") or {}
        badk = [c for c in (1, 2, 3, 4) if (pv.get(c) or {}).get("v") == "fail"]
        pendk = any((pv.get(c) or {}).get("pending") for c in (1, 2, 3, 4))
        for c in (1, 2, 3):
            if c in out and out[c]["v"] == "pass":
                if badk and not any((pv.get(c2) or {}).get("pending") for c2 in badk):
                    out[c] = verdict(False, f"기대 턴 T{k} 가 틀림(기준 {badk}) — 따라 fail")
                elif badk or pendk:  # 0.3(검수 P2-b) — 기대 턴이 ⚑ 면 「따라 확인 필요」(na⚑)
                    out[c] = {"v": "na", "why": f"기대 턴 T{k} 가 확인 필요 · 데이터 대기 칸 — 따라 확인 필요", "pending": True}
    if pend_turn:  # 턴 칸이 「확인 필요」 면 목록 · 주제 판정은 따로 센다(답 글 판정은 그대로)
        for c in (1, 2, 3, 4, 5, 7, 17, 18, 19, 20, 21, 22):
            if c in out:
                out[c]["pending"] = True
    return out


def topic_with(topics, site):
    for tp in topics:
        if site in (tp.get("sites") or []):
            return tp
    return None


def topic_items_same(t, topics, conv):
    bad = []
    for s, k in (t["topic"].get("items_same") or {}).items():
        now = topic_with(topics, s)
        then = topic_with(((conv.get(k) or {}).get("ledger") or {}).get("consult", {}).get("topics") or [], s)
        if not now or not then or set(now.get("items") or []) != set(then.get("items") or []):
            bad.append(f"{SITES[s]['name']} 주제 진료항목이 T{k} 와 다름" if now and then else f"{SITES[s]['name']} 주제 없음")
    return verdict(not bad, " · ".join(bad))


RX_DEFLECT = re.compile(r"(상담|원장|내원)[^.\n]{0,30}(확인|여쭤|문의)")


def strip_deflect(ans: str) -> str:
    """0.2 — 「~ 는 상담 때 원장님과 확인해 주세요」 문장은 답 내용에서 뺀다(돌려 막기 문장 속 낱말로 통과 막기)."""
    return "\n".join(x for x in re.split(r"(?<=[.?!])\s+|\n+", ans or "") if not RX_DEFLECT.search(x))


BODY_WORDS = ("몸", "전신", "바디")  # 0.4 — 부위 갈래 이름(매핑 부위 표에 없는 큰 갈래)


def site_names_in(sent: str) -> set[str]:
    flat = sent.replace(" ", "")
    names = {(v.get("name") if isinstance(v, dict) else str(v)) for v in SITES.values()} | set(BODY_WORDS)
    # 한 글자 부위 이름(눈 · 코 · 등 …)은 다른 낱말 속에 끼므로 갈래 이름(몸)만 한 글자로 받는다
    return {n for n in names if n and (len(n) >= 2 or n in BODY_WORDS) and n.replace(" ", "") in flat}


def answer_kind(t, ans, L):
    ans = strip_deflect(ans)
    ask = t.get("ask")
    if not ask:
        return verdict(None)
    if ask == "confirm":
        return {"v": "human", "why": "", "pending": False, "human": True}
    if ask == "remember":
        lack = [w for w in t.get("remember_words", []) if w not in ans]
        return verdict(not lack, f"답에 {lack} 없음" if lack else "")
    subj = t.get("subject")
    if subj and subj not in ans.replace(" ", ""):
        return verdict(False, f"물은 대상 「{subj}」 이 답에 없음")
    if ask == "ask_site":  # 0.3 — 부위를 되묻는다(S02 T1 사용자 결정)
        # 0.4(재검수 r3 P2-5) — 기준 뜻 = 어느 부위인지 묻는 물음 문장. 「부위 · 어디 · 어느 쪽」 이 든 물음 문장, 또는 부위 이름(매핑
        # 부위 + 몸 · 전신)을 둘 이상 들어 고르게 하는 물음 문장(「얼굴이세요, 아니면 전신이세요?」). 물음 부호 없는 문장은 안 침.
        ok = any(("?" in x) and (bool(re.search(r"부위|어디|어느\s?쪽", x)) or len(site_names_in(x)) >= 2)
                 for x in re.split(r"(?<=[.?!])\s+|\n+", ans))
        return verdict(ok, "부위를 묻지 않음" if not ok else "")
    if ask == "reason":  # 0.3 — 앞 목록 + 까닭(S05 T2)
        rw = "|".join(t.get("reason_words") or ["없"])
        ok = bool(re.search(rf"({rw})[^.\n]*없|없[^.\n]*({rw})", ans))
        return verdict(ok, "0 인 까닭을 말하지 않음" if not ok else "")
    if ask == "overview":
        return verdict(len(ans) >= 80, "답이 짧음" if len(ans) < 80 else "")
    if ask == "effect_adverse":
        a, e = re.search(KW["adverse"], ans), re.search(KW["effect"], ans)
        return verdict(bool(a and e), ("" if e else "효과 없음 ") + ("" if a else "부작용 없음"))
    if ask in ("outside", "absent"):
        ok = no_here(ans)
        return verdict(ok, "명동점에 없다는 말 없음(돌려 막기 · 되물음 포함)" if not ok else "")
    if ask == "other_options":
        names = [g for g in t.get("other_groups", [])]
        words = {w for g in names for w in re.findall(r"필러|볼뉴머|소프웨이브|울쎄라|슈링크|리프팅", g)} or set(names)
        hit = [w for w in words if w in ans]
        return verdict(bool(hit), f"보톡스 밖 선택지 말 없음(기대 {sorted(words)})" if not hit else "")
    rx = KW.get(ask)
    return verdict(bool(rx and re.search(rx, ans)), f"「{ask}」 말 없음" if not (rx and re.search(rx, ans)) else "")


def item_prices(code: str) -> set[int]:
    out = set()

    def add(o):
        for k2 in ("price_amount", "event_price"):
            if isinstance(o.get(k2), (int, float)) and o.get(k2):
                out.add(int(o[k2]))
        for a in o.get("additional_prices") or []:
            for v in (a.values() if isinstance(a, dict) else [a]):
                if isinstance(v, (int, float)) and v:
                    out.add(int(v))
    for o in ITEM.get(code, {}).get("options") or []:
        add(o)
    for pr in M.get("products") or []:
        for o in pr.get("options") or []:
            if code in (o.get("covers") or []):
                add(o)
    return out


def _name_index() -> list[tuple[str, set[str]]]:
    """0.6 — 이름(공백 지움) → 진료항목: 진료항목 이름 · 그 진료항목 옵션 이름 · 그 진료항목을 덮는 상품 옵션 이름(긴 이름 먼저)."""
    idx: dict[str, set[str]] = {}
    for c, i in ITEM.items():
        for nm in [i.get("kos_item_name")] + [o.get("option_title") for o in i.get("options") or []]:
            k = (nm or "").replace(" ", "")
            if len(k) >= 3:
                idx.setdefault(k, set()).add(c)
    for pr in M.get("products") or []:
        for o in pr.get("options") or []:
            k = (o.get("title") or "").replace(" ", "")
            if len(k) >= 3 and o.get("covers"):
                idx.setdefault(k, set()).update(x for x in o["covers"] if x in ITEM)
    return sorted(idx.items(), key=lambda x: -len(x[0]))


NAME_IDX = _name_index()


def nearest_items(sent: str) -> dict[int, set[str] | None]:
    """0.6 — 문장 안 값마다 그 값 앞 가장 가까운 이름의 진료항목(긴 이름이 겹친 짧은 이름을 이김). 앞 이름이 없으면 None."""
    flat = sent.replace(" ", "")
    spans: list[tuple[int, int, set[str]]] = []
    for k, codes in NAME_IDX:
        i = flat.find(k)
        while i >= 0:
            if not any(a <= i < b for a, b, _ in spans):
                spans.append((i, i + len(k), codes))
            i = flat.find(k, i + 1)
    out: dict[int, set[str] | None] = {}
    for v in money(sent):
        pos = [m.start() for m in re.finditer(r"(\d{1,3}(?:,\d{3})+|\d+)\s*만?\s*\d*\s*원", flat)]
        best = None
        for p in pos:
            if v not in money(flat[p:p + 20]):
                continue
            before = [sp for sp in spans if sp[1] <= p]
            best = max(before, key=lambda sp: sp[1])[2] if before else None
            break
        out[v] = best
    return out


def price_check(t, ans, cards):
    """0.2(검수 P2-1) — 금액은 그 문장에 나온 진료항목(없으면 화면 진료항목)의 옵션 값과 짝이 맞아야 하고,
    가격을 물으면 화면 묶음마다 값 하나는 있어야 한다(빠뜨림)."""
    ms = money(ans)
    if t.get("ask") == "price" and not ms:
        return verdict(False, "가격을 묻는데 값 없음")
    if not ms:
        return verdict(None)
    card_set = set(cards)
    bad = []
    for sent in re.split(r"(?<=[.?!])\s+|\n+", ans):
        vals = money(sent)
        if not vals:
            continue
        flat = sent.replace(" ", "")
        near = nearest_items(sent)  # 0.6(검수 r4 P2-3) — 값마다 같은 문장 안 가장 가까운 앞 이름(진료항목 · 옵션 이름)과 짝
        if near and all(n is not None for n in near.values()):
            for v, codes in near.items():
                cg = {GROUP_OF.get(c) for c in codes}
                pool_v = set().union(*[item_prices(c) for c in list(codes) + [c for c in card_set if GROUP_OF.get(c) in cg]])
                if v not in pool_v:
                    bad.append(v)
            continue
        hit = [c for c, i in ITEM.items() if (i.get("kos_item_name") or "").replace(" ", "") and (i["kos_item_name"].replace(" ", "") in flat)]
        if not hit:
            hit = [c for c, i in ITEM.items() if (i.get("kos_procedure") or "").replace(" ", "") in flat and c in card_set]
        hg = {GROUP_OF.get(c) for c in hit}
        hit = hit + [c for c in card_set if GROUP_OF.get(c) in hg]  # 이름이 맞은 진료항목의 같은 묶음(회차 · 추가 옵션)까지
        pool = set().union(*[item_prices(c) for c in hit]) if hit else set().union(*[item_prices(c) for c in card_set] or [set()])
        if not pool:  # 0.3(검수 P2-c) — 전체 가격 묶음으로 돌아가지 않음
            bad += [v for v in vals]
            continue
        bad += [v for v in vals if v not in pool]
    miss = []
    if t.get("ask") == "price":
        # 0.3(검수 P2-c · P2-d) — 빠뜨림 대상 = 주제 부위에 바로 매핑된 묶음(부위 없으면 화면 묶음 전부) ·
        # 그 묶음 값은 그 묶음 · 진료항목 이름이 든 문장 안에 있어야
        tsites = set(t.get("topic_sites") or []) - {"SITE-007"}
        target = [g for g in groups(cards)
                  if not tsites or any(tsites & set(ITEM[c]["hub"].get("site_codes") or []) for c in cards if GROUP_OF.get(c) == g)]
        sents = re.split(r"(?<=[.?!])\s+|\n+", ans)
        for g in target:
            gcodes = [c for c in cards if GROUP_OF.get(c) == g]
            gp = set().union(*[item_prices(c) for c in gcodes] or [set()])
            names = {g.replace(" ", "")} | {(ITEM[c].get("kos_item_name") or "").replace(" ", "") for c in gcodes}
            near = set()
            for x in sents:
                fx = x.replace(" ", "")
                if any(nm and nm in fx for nm in names):
                    near |= set(money(x))
            if gp and not (gp & near):
                miss.append(g)
    return verdict(not bad and not miss, (f"짝 안 맞는 값 {bad[:4]} " if bad else "") + (f"값 빠뜨림 {miss[:4]}" if miss else ""))


def no_here(ans: str) -> bool:
    """0.2 — 「명동점」 과 없다는 말이 한 문장에(돌려 막기 「안내해 드리기 어려워요」 · 되물음은 아님)."""
    for sent in re.split(r"(?<=[.?!])\s+|\n+", ans or ""):
        if re.search(KW["outside"], sent) and re.search(KW["neg"], sent):
            return True
    return False


def branch_check(t, ans):
    flat = ans.replace(" ", "")
    if t.get("ask") in ("outside", "absent"):
        ok = no_here(ans)
        return verdict(ok, "" if ok else "밖 시술을 있는 것처럼 말함(없다는 말 없음)")
    hits = [w for w in OUT_LEX if w in flat]
    return verdict(not hits, f"밖 이름 {hits[:4]}" if hits else "")


def split_check(t, topics, active, conv):
    tp = t["topic"]
    if tp.get("split"):
        own = {s: [x.get("id") for x in topics if s in (x.get("sites") or [])] for s in tp["split"]}
        lack = [SITES[s]["name"] for s, ids in own.items() if not ids]
        both = [x.get("id") for x in topics if all(s in (x.get("sites") or []) for s in tp["split"])]
        return verdict(not lack and not both, (f"주제 없음 {lack} " if lack else "") + (f"한 주제에 같이 {both}" if both else ""))
    if tp.get("new"):
        prev = conv.get(t["n"] - 1)
        ids = {x.get("id") for x in ((prev or {}).get("ledger") or {}).get("consult", {}).get("topics") or []}
        cur = next((x for x in topics if x.get("id") == active), {})
        exp = set(t.get("topic_sites") or [])
        site_ok = not exp or bool(exp & set(cur.get("sites") or []))
        return verdict(active not in ids and site_ok,
                       ("" if active not in ids else f"새 주제 아님({active})") + ("" if site_ok else f" 주제 부위 {cur.get('sites')}"))
    return verdict(None)


def mix_check(t, topics, conv):
    """18 — 부위가 하나뿐인 얼굴 주제마다 그 부위 밖 묶음이 섞였나 + items_same + topic_not."""
    from build_answers import body_groups, outside_groups  # noqa: PLC0415
    bad = []
    body = set(body_groups())
    for tp in topics:
        ss = [s for s in tp.get("sites") or [] if face(s) and s != "SITE-007"]
        ss = [s for s in ss if not any(a in ss for a in anc(s))]  # 부모 · 자식(턱 · 턱밑)은 한 부위로
        if len(ss) >= 2:  # 0.2(검수 P1-2) — 한 주제에 부위 둘 = 섞임
            bad.append(f"{tp.get('id')} 에 부위 {len(ss)} 개({' · '.join(SITES[x]['name'] for x in ss)})")
        if "SITE-007" in (tp.get("sites") or []) and not ss:  # 얼굴(큰) 주제 = 몸 묶음(R6) 0
            mb = [g for g in groups(tp.get("items")) if g in body]
            if mb:
                bad.append(f"{tp.get('id')}(얼굴) 에 몸 묶음 {len(mb)} 개 {mb[:3]}")
        if len(ss) == 1:
            mix = [g for g in groups(tp.get("items")) if g in set(outside_groups(ss[0]))]
            if mix:
                bad.append(f"{tp.get('id')}({SITES[ss[0]]['name']}) 에 {mix[:3]}")
    for s, gs in (t["topic"].get("topic_not") or {}).items():
        tp = topic_with(topics, s)
        mix = [g for g in groups((tp or {}).get("items")) if g in gs]
        if mix:
            bad.append(f"{SITES[s]['name']} 주제에 {mix}")
    if t["topic"].get("items_same"):
        v = topic_items_same(t, topics, conv)
        if v["v"] == "fail":
            bad.append(v["why"])
    return verdict(not bad, " · ".join(bad))


def remember_check(t, topics, ans):
    rem = t["topic"].get("remember")
    if not rem and t.get("remember_words"):
        lack = [w for w in t["remember_words"] if w not in ans]
        return verdict(not lack, f"답에 {lack} 없음" if lack else "")
    bad = []
    for s, word in (rem or {}).items():
        tp = topic_with(topics, s)
        conds = (tp or {}).get("conditions") or {}
        names = " ".join(v.get("name") or "" for k in ("procedure", "product") for v in conds.get(k) or [])
        if not tp:
            bad.append(f"{SITES[s]['name']} 주제 없음")
        elif word not in names:
            bad.append(f"{SITES[s]['name']} 주제 조건 「{names or '없음'}」 에 {word} 없음")
    return verdict(not bad, " · ".join(bad))


def display_check(t, scr, topics, active):
    bad = []
    if scr.get("current_topic") and scr.get("current_topic") != active:
        bad.append(f"화면 지금 주제 {scr.get('current_topic')} ≠ 장부 {active}")
    cur = next((x for x in topics if x.get("id") == active), {})
    cur_face = {s for s in cur.get("sites") or [] if face(s)}
    all_face = {s for x in topics for s in x.get("sites") or [] if face(s)}
    dots = scr.get("dots") or []
    lit = {d["site"] for d in dots if not d["other"]}
    shown = {d["site"] for d in dots}
    if lit != cur_face:
        bad.append(f"강조 점 {sorted(SITES.get(s, {}).get('name', s) for s in lit)} ≠ 지금 주제 부위 {sorted(SITES[s]['name'] for s in cur_face)}")
    if shown != all_face:
        bad.append(f"뜬 점 {len(shown)} ≠ 전체 주제 부위 {len(all_face)}")
    if t.get("topic_sites") == ["SITE-007"] and cur.get("sites") and "SITE-007" not in cur.get("sites"):
        bad.append(f"큰 주제(얼굴) 기대 · 지금 주제 부위 {cur.get('sites')}")  # 0.2 — 큰 주제 표시도 본다
    exp = [s for s in t.get("topic_sites") or [] if s != "SITE-007"]
    if exp and not isinstance(exp, str):
        if len(exp) == 1 and exp[0] not in (cur.get("sites") or []):
            bad.append(f"지금 주제 부위 {cur.get('sites')} ≠ 기대 {SITES[exp[0]]['name']}")
    return verdict(not bad, " · ".join(bad))


# ---------- 모으기 ----------
def cost_of(tok: dict | None) -> float:
    s = 0.0
    for c in (tok or {}).get("calls") or []:
        for k, p in PRICE_SONNET.items():
            s += (c.get(k) or 0) * p / 1e6
    return s


def gold_of(d: Path) -> str | None:
    """결과 폴더의 측정 gold — meta.json gold_hash(0.3 이후 run.py) · 없으면 None(옛 측정)."""
    try:
        return json.loads((d / "meta.json").read_text()).get("gold_hash")
    except Exception:  # noqa: BLE001
        return None


def main() -> None:
    d = Path(sys.argv[1])
    # SPEC-012 C1 · C2 — `--before <폴더>` 를 주면 전 · 후 gold_hash 가 같을 때만 채점(다르면 멈춤)
    if "--before" in sys.argv:
        b = Path(sys.argv[sys.argv.index("--before") + 1])
        gb, ga = gold_of(b), gold_of(d)
        if not gb or not ga or gb != ga:
            raise SystemExit(f"전 · 후 gold_hash 가 다르거나 없다(전 {gb} · 후 {ga}) — 같은 gold 위에서 다시 재라")
    sys.path.insert(0, str(HERE))
    af = Path(sys.argv[sys.argv.index("--answers") + 1]) if "--answers" in sys.argv else HERE / "answers.json"
    ans = json.loads(af.read_text())  # 0.6 — 정답표 파일을 고를 수 있음(옛 gold 정답표로 옛 측정을 같은 규칙 채점)
    # SPEC-012 0.1.2 C5 — 정답표 gold ≠ 측정 gold 면 멈춤(둘 다 기록돼 있을 때 · 옛 측정은 meta gold 없음 → 경고만)
    ga, gm = ans.get("gold_hash"), gold_of(d)
    if gm and not ga:  # SPEC-012 r3 P2-2 — 새 측정(meta gold 있음)이면 정답표 gold 도 필수
        raise SystemExit("정답표에 gold 기록이 없다 — 측정과 같은 gold 로 build_answers.py 를 다시 돌려라")
    cross = "--cross-gold" in sys.argv  # 0.6 — 옛 gold 측정 × 새 gold 정답(WP-0 §2 ② 꼴) · 결과에 적는다
    if ga and gm and ga != gm and not cross:
        raise SystemExit(f"정답표 gold {ga[:16]} ≠ 측정 gold {gm[:16]} — 같은 gold 로 build_answers.py 를 다시 돌려라")
    if not gm:
        print(f"경고: 측정 gold 기록 없음(옛 측정) — 정답표 gold {str(ga)[:16]}", flush=True)
    key = {(t["sid"], t["n"]): t for t in ans["turns"]}
    recs = [json.loads(x) for x in (d / "turns.jsonl").read_text().splitlines()]
    by_conv = collections.defaultdict(dict)
    for r in recs:
        by_conv[(r["run"], r["sid"])][r["n"]] = r
    rows = []
    for r in sorted(recs, key=lambda x: (x["run"], x["sid"], x["n"])):
        t = key[(r["sid"], r["n"])]
        v = judge(t, r, by_conv[(r["run"], r["sid"])], ans)
        r["_v"] = v
        rows.append({"run": r["run"], "sid": r["sid"], "n": r["n"], "q": r["q"], "v": v,
                     "groups": groups(r["screen"].get("cards")), "items": r["screen"].get("cards"),
                     "answer": ((r.get("ledger") or {}).get("answer") or ""), "cost": cost_of((r.get("ledger") or {}).get("tokens")),
                     "tokens": ((r.get("ledger") or {}).get("tokens") or {}).get("sum"),
                     "calls": ((r.get("ledger") or {}).get("tokens") or {}).get("calls"),
                     "understand": ((r.get("ledger") or {}).get("understand") or {}).get("parsed"),
                     "active": ((r.get("ledger") or {}).get("consult") or {}).get("active_topic")})
    # 6 — 실행 3 번 사이
    shake = []
    turns = sorted({(x["sid"], x["n"]) for x in rows})
    for sid, n in turns:
        rs = sorted([x for x in rows if x["sid"] == sid and x["n"] == n], key=lambda x: x["run"])
        sets = [frozenset(x["items"] or []) for x in rs]
        gsets = [frozenset(x["groups"]) for x in rs]
        same = len(set(sets)) == 1
        diff_fields = understand_diff([x["understand"] for x in rs])
        shake.append({"sid": sid, "n": n, "q": rs[0]["q"], "same_items": same, "same_groups": len(set(gsets)) == 1,
                      "n_items": [len(s) for s in sets], "n_groups": [len(s) for s in gsets], "u_diff": diff_fields,
                      "only_in": {f"r{x['run']}": sorted(set(x["groups"]) - set.intersection(*[set(y["groups"]) for y in rs]))[:6] for x in rs},
                      "verdict_flip": sorted({c for x in rs for c, vv in x["v"].items()
                                              if len({y["v"].get(c, {}).get("v") for y in rs}) > 1})})
        if True:  # 기준 6 은 모든 턴에서 본다(같은 말 · 같은 앞 대화)
            for x in rs:
                x["v"][6] = verdict(same, "" if same else f"실행마다 진료항목 수 {[len(s) for s in sets]}")
    # 기준별
    per = {}
    for c in ALL:
        vs = [x["v"][c] for x in rows if c in x["v"]]
        fixed = [v for v in vs if not v.get("pending") and v["v"] in ("pass", "fail")]
        pend = [v for v in vs if v.get("pending") and v["v"] in ("pass", "fail")]
        per[c] = {"name": CRIT_NAME[c], "n": len(fixed), "pass": sum(v["v"] == "pass" for v in fixed),
                  "pend_n": len(pend), "pend_pass": sum(v["v"] == "pass" for v in pend),
                  "human": sum(v["v"] == "human" for v in vs) + sum(1 for v in vs if v.get("human") and v["v"] != "human"),
                  "empty": sum(1 for v in vs if v.get("empty"))}
    per_sc = collections.defaultdict(lambda: [0, 0])
    for x in rows:
        for c, v in x["v"].items():
            if c in CRIT and v["v"] in ("pass", "fail"):
                per_sc[x["sid"]][0] += v["v"] == "pass"
                per_sc[x["sid"]][1] += 1
    per_run = collections.defaultdict(lambda: [0, 0])
    for x in rows:
        for c, v in x["v"].items():
            if c in CRIT and v["v"] in ("pass", "fail"):
                per_run[x["run"]][0] += v["v"] == "pass"
                per_run[x["run"]][1] += 1
    res = {"dir": str(d), "gold_hash": gold_of(d), "answers_gold": ans.get("gold_hash"), "answers_file": af.name, "cross_gold": cross, "score_version": "0.6", "answers_version": ans.get("version"), "per_crit": per, "per_scenario": per_sc, "per_run": per_run, "shake": shake,
           "cost_total": round(sum(x["cost"] for x in rows), 4), "turns": len(rows),
           "cost_per_turn": round(sum(x["cost"] for x in rows) / max(1, len(rows)), 4),
           "rows": [{k: v for k, v in x.items() if k not in ("items",)} for x in rows]}
    (d / "score.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=list))
    write_md(d, res, key)
    write_human(d, rows, key)
    for c in ALL:
        p = per[c]
        print(c, p["name"], f"{p['pass']}/{p['n']}", f"pend {p['pend_pass']}/{p['pend_n']}", f"human {p['human']}")
    main_ = [per[c] for c in CRIT]
    print("total fixed", sum(p["pass"] for p in main_), sum(p["n"] for p in main_),
          "pend", sum(p["pend_pass"] for p in main_), sum(p["pend_n"] for p in main_),
          "empty", sum(p["empty"] for p in main_))
    print("sub", {c: f"{per[c]['pass']}/{per[c]['n']}" for c in SUB})
    print("cost", res["cost_total"], "per turn", res["cost_per_turn"])


def understand_diff(us: list[dict | None]) -> list[str]:
    keys = set()
    for u in us:
        keys |= set((u or {}).keys())
    out = []
    for k in sorted(keys):
        vals = {json.dumps((u or {}).get(k), sort_keys=True, ensure_ascii=False) for u in us}
        if len(vals) > 1:
            out.append(k)
    return out


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "—"


def write_md(d: Path, res: dict, key: dict) -> None:
    L = ["# 채점 표", "", ("측정 gold `" + res["gold_hash"][:16] + "…`" if res.get("gold_hash") else "측정 gold (meta 에 기록 없음 — run.py 0.3 전 측정)") + f" · 정답표 v{res.get('answers_version')}", "",
         f"결과 폴더 `{d.name}` · 턴 {res['turns']} · 돌린 비용 ${res['cost_total']:.2f} · 턴당 ${res['cost_per_turn']:.3f}", "",
         "| # | 기준 | 확정 통과 | 확인 필요 칸에 걸린 판정 | 빈 정답(na) | 사람 판정 |", "|---:|---|---:|---:|---:|---:|"]
    for c in ALL:
        p = res["per_crit"][c]
        nm = p["name"] + (" (기계 대리 — 가격 · 없는 시술 값만)" if c == 9 else "")
        L.append(f"| {c} | {nm} | {pct(p['pass'], p['n'])} | {pct(p['pend_pass'], p['pend_n'])} | {p.get('empty') or '—'} | {p['human'] or '—'} |")
    L += ["", "## 실패(턴 × 실행)", "", "| 시나리오 | 턴 | 실행 | 기준 | 까닭 |", "|---|---:|---:|---:|---|"]
    for x in res["rows"]:
        for c, v in sorted(x["v"].items()):
            if v["v"] == "fail":
                L.append(f"| {x['sid']} | T{x['n']} | r{x['run']} | {c}{'⚑' if v.get('pending') else ''} | {v['why'][:160]} |")
    (d / "score.md").write_text("\n".join(L) + "\n")


def write_human(d: Path, rows: list[dict], key: dict) -> None:
    L = ["# 사람 판정 표 — 기준 8(확인) · 9 · 15", "", "실행 1(r1) 답만 싣는다. 칸에 ○ / × 를 적는다.", ""]
    for x in sorted(rows, key=lambda y: (y["sid"], y["n"])):
        if x["run"] != 1:
            continue
        t = key[(x["sid"], x["n"])]
        hs = [c for c in (9, 15) if c in t["crit"]] + ([8] if t.get("ask") == "confirm" else [])
        if not hs:
            continue
        L += [f"### {x['sid']} T{x['n']} — 「{x['q']}」 · 볼 기준 {hs}", "", "> " + x["answer"].replace("\n", "\n> "), "",
              "| 기준 | ○ / × | 메모 |", "|---|---|---|"] + [f"| {c} {CRIT_NAME[c]} | | |" for c in hs] + [""]
    (d / "human.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
