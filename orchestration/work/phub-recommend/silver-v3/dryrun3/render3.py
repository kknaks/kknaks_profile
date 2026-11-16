# -*- coding: utf-8 -*-
"""out-dryrun3/report.md — dryrun3.json(센 값) · verify-7차.json 을 그대로 옮긴다. 여기서 새로 세는 수는 표의 행 수·합계뿐이다."""
from collections import Counter

BNAME = {"ledger-nodes": "새 사건 노드", "dup-strong": "⑦ strong", "seeds": "씨앗", "batch3": "묶음3 미결"}
COLS3 = [("T1", "T1"), ("N1", "N1"), ("N2(a)", "T2a"), ("N2(b)", "T2b_user"), ("T3", "T3"), ("T4", "T4"), ("R2", "R2"), ("N3", "N3"), ("R1", "R1"), ("R3", "R3"), ("R4", "R4"), ("S", "S")]


def esc(x):
    if isinstance(x, (list, tuple)):
        x = ", ".join(str(y) for y in x)
    if x is True:
        x = "예"
    if x is False:
        x = "—"
    return str(x if x not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def why_final(r):
    if r["ambiguous"]:
        return "애매 — " + " / ".join(r["ambiguous"])
    p = []
    nm = r["node"].split()
    if not r["in_7th"]:
        p.append("3차가 세운 이름(7차 「" + ", ".join(r["from7"]) + "」 에서)")
    if r["n1"]:
        p.append("N1 명사형(-ㅁ/-음) 이름")
    if r["sole"]:
        p.append(f"R3 후보(단독 0)지만 「{r['sole']}」의 유일한 사건 칸")
    elif len(nm) > 1:
        p.append("명사 여럿 · 앞뒤 「" + nm[0] + "」·「" + nm[-1] + "」 은 R1·R2·N4 목록 밖")
    else:
        p.append(f"말 하나 · R1·R2 말 없음 · 단독 출현 {r['solo_strict']}")
    p.append("사전 사건과 같은 꼴 아님(N3 동치 밖)")
    return " · ".join(p) + " → 부작용 여부·종류는 사람"


def write(res, verify, path):
    T, T1, T2 = res["table"], res["table_1st"], res["table_2nd"]
    L = []
    a = L.append
    nd = res["nodes"]
    fr = res["final_rows"]
    a("# 드라이런 3차 — 2차 규칙 구멍 메우기 + 기존 사전 사건에도 R2 (2026-11-06)")
    a("")
    a(f"발주서 `../../silver-dryrun3-brief.md` · 코드 `silver-v3/dryrun3/`(run_dryrun3.py · dry3_au.py · kiwi_t0.py · common3.py · render3.py — 2차 `dryrun2/` 를 복사해 고침 · `dryrun2/` 는 안 건드림) · 센 값 원본 `out-dryrun3/dryrun3.json` · 인터프리터 `silver-v3/.venv-kiwi/bin/python`(kiwipiepy {res['kiwi']['version']}).")
    a("**결정이 아니라 드라이런이다.** 이 문서의 수는 전부 코드가 센 값이다(추정이라 적은 곳 1 곳 — §8 빌더 메모). 사전 값은 바꾸지 않았다(N3·N4 는 드라이런 전용 동치표·임시 값). 7차 산출물(`out/` · `decisions/` · `baseline/` · lib · ERD · 브론즈)·1차(`dryrun/`)·2차(`dryrun2/`) 코드는 읽기만 했다.")
    a("")
    a("## 0. 3차 규칙을 기계로 옮긴 방식(2차와 다른 곳만 · 나머지는 2차 report §0 그대로)")
    a("")
    a("- **판정 순서** T3 → T4 → N2 → T1 → N1 → R2(+N4) → N3 → R1 → R3 → R4 → S · 겹치면 먼저 적용된 규칙에 센다(1·2차와 같은 관례). 7차 노드 하나의 자리들 중 7차 이름이 하나라도 그대로 서면 「남음」.")
    a("- **어절 종류(word_kind)** — 어절마다 마지막 어미로 가른다(뒤 기호·접속 조사 JC 는 떼고 봄). `N1` = 용언 어간 + -ㅁ/-음(ETN·EF)로 끝남(뒤에 명사·접미 「감」만 허용 — 「따가움감」) · `ETM` 관형형 · `ADV` 「-게」 부사형 · `CLAUSE` = 용언 + 연결 어미(EC · 「-게」 뺌)·종결 어미(EF · -ㅁ/-음 뺌)·「-기」 · `ARG` = 격조사(JKS·JKO·JKB)로 끝나는 어절(N1+격조사 「막힘으로」 포함). 어절 안 보조 용언 연결(「붉어짐 = 붉/VA+어/EC+지/VX+ᆷ」·「어색해지는」)은 마지막 어미로만 본다. VCP(「일시적인」)는 관형형·부사형일 때만 용언으로 본다(2차처럼 종결·연결은 용언 아님).")
    a("- **N2 문장꼴 = 절이 있을 때만** — 멤버에 `CLAUSE` 어절이 있거나, `ETM`·`ADV` 어절 앞에 `ARG` 어절(그 용언의 논항)이 있거나, `ETM` 의 뒤 어절 머리가 의존명사(NNB · 그 어절 내용이 의존명사 하나일 때만 — 「거상 → 거/NNB+상/XSN」은 아님) 또는 「현상·느낌·증상·경우」(발주서 예 그대로 · 넓히지 않음)일 때. 나머지 `ETM`·`ADV` 어절은 **관형어·부사어 하나 = 수식어** → R1 목록에 없으면 「R1 후보(새)」로 떼고 따로 셈(§3.4). 여러 수식어가 겹쳐도(「일시적인 가벼운 따가움」) 절이 없으면 수식어. R1 목록 말(「심한」「경미한」…)은 2차처럼 판정에서 뺀다. 2차와 같게 **멤버 단위**로 읽는다 — 「시술 중 당기는 느낌과 냉감」은 멤버에 절(당기는 느낌)이 있어 「냉감」 토막도 (b).")
    a("- **N1** — `N1` 어절은 명사(T1 통과) · 이름 = 어절 그대로(뒤 접속 조사·기호만 뗌 — 「따가움이나」→「따가움」 · 7차 접속 조사 토막 경계와 같은 자리). 분석기 후보 10 개가 전부 이상 꼴인 어절(2차 ANOM)은 통째 명사 — 단 1위 분석의 어절 끝이 조사(JC 뺌)·EC·ETM 이면 「조사·연결어미 붙음」으로 보고 애매 그대로. 이름 하나로 다시 분석했을 때 `N1` 어절 안 어미는 조사·어미 검사에서 뺀다(2차가 「눈부심」을 뺀 자리). N1 어절이 아닌데 용언이 든 어절(「막힘으로」 같은 N1+격조사가 절 없는 멤버에 있을 때)은 적용 안 하고 애매(`T1-pred`).")
    a("- **N4** — R2 목록에 동맥 · 정맥 · 안동맥(parent 동맥) 을 더했다(혈관은 이미 R2·site layer). 드라이런 전용 임시 값(사전 추가 아님).")
    a("- **N3** — 사전 사건 43(40 + 승인 3)의 canonical(과 동의어)을 「부위 말(R2·N4·site 사전) + 명사」로 띄어 쓴 꼴만 분해(사건 = 뒤 말 · 부위 = 앞 말). 띄어쓰기 없이 붙은 값은 뒤 말이 사건 말인지 애매 → 분해 안 함(애매 — 사용자). 분해한 사건 말과 이름이 같은 새 노드는 그 사전 사건과 한 묶음(N3)으로 센다. 사전 값 자체 변경은 제안 표(§2 (라))로만.")
    a("- **N5** — 폐색 ≠ 색전: 접는 규칙 없음(코드에 둘을 잇는 동치 0 · 확인 §2 (마)). R1 은 「이상」 뺀 채 그대로.")
    a("- **S** — 게이트 23 쌍(접미 감·증·형성 · 두 끝이 3차에도 노드·사전일 때) + 2차에 못 쓴 쌍 중 N1 로 돌아온 쌍 + 규칙 뒤 ⑦ 에서 한쪽이 N1 노드인 새 접미 쌍(센 값 0). 자모 쌍은 같다고 보지 않는다.")
    a("")

    # ---------------- 1
    a("## 1. 묶음 × 규칙 — 1차 · 2차 · 3차 나란히")
    a("")
    head = ["묶음", "자리", "1차 남음(애매)", "2차 남음(애매)"] + [c for c, _ in COLS3] + ["닫힘 계", "문장꼴(b)→사용자", "애매→사용자(노드 아님)", "**3차 남음**", "남음 중 애매"]
    rows = []
    tot = Counter()
    for b in ("ledger-nodes", "dup-strong", "seeds", "batch3"):
        t, t1, t2 = T[b], T1[b], T2[b]
        rows.append([BNAME[b], t["slots"], f"{t1['remaining']}({t1['ambiguous']})", f"{t2['remaining']}({t2['remaining_ambiguous']})"] + [t.get(k, 0) for _, k in COLS3]
                    + [t["closed"], t["T2b_user"], t["amb_nonnode_user"], f"**{t['remaining']}**", t["remaining_ambiguous"]])
        for _, k in COLS3:
            tot[k] += t.get(k, 0)
        for k in ("slots", "closed", "T2b_user", "amb_nonnode_user", "remaining", "remaining_ambiguous"):
            tot[k] += t[k]
        tot["r1"] += t1["remaining"]
        tot["a1"] += t1["ambiguous"]
        tot["r2"] += t2["remaining"]
        tot["a2"] += t2["remaining_ambiguous"]
    rows.append(["**합계**", tot["slots"], f"{tot['r1']}({tot['a1']})", f"{tot['r2']}({tot['a2']})"] + [tot[k] for _, k in COLS3] + [tot["closed"], tot["T2b_user"], tot["amb_nonnode_user"], f"**{tot['remaining']}**", tot["remaining_ambiguous"]])
    a(tbl(head, rows))
    a("")
    a("- 「N2(b)」 열은 닫힘이 아니다 — 「문장꼴(b)→사용자」 열과 같은 수(노드가 아니게 되어 사람이 볼 자리). 「닫힘 계」에 안 들어간다. 「excluded」(7차 결정 exclude) 열은 0 이라 뺐다.")
    a(f"- **N3 열 0 의 뜻**: 「동맥 폐색」은 먼저 R2(동맥 → 부위)로 이름이 「폐색」이 되어 R2 에 센다(먼저 적용된 규칙). 그 「폐색」이 N3 으로 사전 「혈관 폐색」의 사건과 한 묶음이 된다 — 그래서 3차 남는 새 노드 목록에 「폐색」은 없다(§2 (라)). 7차 이름이 곧바로 N3 으로 닫힌 자리는 0.")
    a("- 1차·2차 열은 그때 규칙 순서(1차 R2→R1→R3→R4→S · 2차 T3→T4→T2→T1→R2→R1→…)라 3차 규칙 열과 열끼리 비교하지 않는다 — 비교는 「남음」으로.")
    a("")
    t = T["ledger-nodes"]
    a(f"**새 사건 노드 260 → 3차 남는 7차 자리 {t['remaining']}**(2차 146 · 1차 206) · 그중 애매 {t['remaining_ambiguous']} · 노드 아님으로 사람이 볼 자리 = 문장꼴(b) {t['T2b_user']} + 애매 {t['amb_nonnode_user']}.")
    a(f"**3차가 새로 세운 이름 {sum(1 for r in fr if not r['in_7th'])}**(7차 260 에 없던 이름) → **남는 새 사건 노드 묶음 {nd['final_node_groups']}**(2차 {res['second']['final_node_groups']} · 1차 {res['first_nodes']['node_groups_after_R4S']}) → 사건 노드 = 사전 43 + {nd['final_node_groups']} = **{43 + nd['final_node_groups']}**.")
    sr = res["strong_recalc"]
    a(f"**⑦ strong**: 96 자리 중 남음 {T['dup-strong']['remaining']}(애매 {T['dup-strong']['remaining_ambiguous']}) · 규칙 뒤 재계산 strong 쌍 {sr['strong_after_rules']}(2차 {res['second']['strong_after_rules']} · 1차 {res['first_strong_recalc']}) · 그중 96 자리 밖 새 쌍 {sr['of_which_new']}.")
    a("")
    a(f"분해 수: 7차 노드 260 → T·N·R2·R1 뒤 {nd['nodes_after_T_R2_R1']} → R3 버림 {nd['r3_dropped']} → {nd['alive_after_R3']} → N3·R4·S 묶음 {nd['final_node_groups']}. 토막 기록 {res['seglog_n']} 의 결과 종류: " + ", ".join(f"{k} {v}" for k, v in sorted(res["seglog_kinds"].items(), key=lambda kv: -kv[1])) + ".")
    a("")

    # ---------------- 2
    a("## 2. 사람이 볼 최종 목록")
    a("")
    pc = res["particle_check"]
    a(f"**조사·어미 검사**: 남는 새 노드 {pc['checked']} 개 이름을 하나씩 Kiwi 로 다시 분석 — 조사(J*)·어미(E*) 형태소(N1 명사형 어절 안 -ㅁ/-음 제외) = **{len(pc['fail'])}**. N1 명사형 어절을 가진 이름 {sum(1 for x in pc['rows'] if x['n1_nominal_endings'])} 개(그 어절 안 어미는 N1 이 명사로 정한 것).")
    a("")
    amb_fr = [r for r in fr if r["ambiguous"]]
    a(f"### (가) 남는 새 사건 노드 전부 — {len(fr)} 행 (그중 애매 표시 {len(amb_fr)} · 3차가 새로 세운 이름 {sum(1 for r in fr if not r['in_7th'])} · N1 명사형 이름 {sum(1 for r in fr if r['n1'])})")
    a("")
    a("원장 횟수 = 이 이름이 선 원장 자리 수(접힌 이름 포함 묶음 합은 괄호). 접기 후보 = 규칙 뒤 ⑦ strong 상대 · 이 노드로 접힌 이름(R4·S).")
    a("")
    rows = []
    for i, r in enumerate(fr, 1):
        fold = []
        if r["folded_in"]:
            fold.append("접힘: " + ", ".join(r["folded_in"]))
        if r["partners"]:
            fold.append("⑦: " + ", ".join(r["partners"]))
        rows.append([i, r["node"], f"{r['n']}" + (f"({r['n_group']})" if r["n_group"] != r["n"] else ""), r["example"], "; ".join(fold) or "—", why_final(r)])
    a(tbl(["#", "노드", "원장 횟수", "원문 예", "접기 후보", "왜 남나"], rows))
    a("")
    rem_dup = [r for r in res["dup_rows"] if not r["rule"] and not r["bucket"]]
    a(f"### (나) ⑦ strong 남는 쌍 — 규칙 뒤 재계산 {len(sr['all_pairs'])} 쌍 (96 자리 중 남은 자리 {len(rem_dup)} · 애매 {sum(1 for r in rem_dup if r['ambiguous'])})")
    a("")
    slot_by_pair = {}
    for r in rem_dup:
        slot_by_pair.setdefault(tuple(sorted(r["now"])), []).append(r)
    rows = []
    for i, p in enumerate(sr["all_pairs"], 1):
        k = tuple(sorted((p["a"], p["b"])))
        sl = slot_by_pair.get(k, [])
        rows.append([i, p["a"], p["b"], "/".join(p["rules"]), ", ".join(f"{r['a']}↔{r['b']}" for r in sl) or "96 밖 새 쌍", " / ".join(x for r in sl for x in r["ambiguous"]) or "—"])
    a(tbl(["#", "노드", "상대", "규칙", "96 자리(7차 쌍)", "애매"], rows))
    a("")
    left = [r for r in rem_dup if tuple(sorted(r["now"])) not in {tuple(sorted((p["a"], p["b"]))) for p in sr["all_pairs"]}]
    a(f"96 자리 중 남았지만 재계산 strong 표에 같은 이름 쌍이 없는 자리 {len(left)}: " + ("; ".join(f"{r['a']}↔{r['b']} → 지금 {r['now'][0]}↔{r['now'][1]}" + (f" ({' / '.join(r['ambiguous'])})" if r["ambiguous"] else "") for r in left) or "없음"))
    a("")
    # (다)
    t2b = res["t2b_texts"]
    amb_slots = [r for r in res["node_rows"] if r["bucket"] == "AMB"]
    t2b_slots = [r for r in res["node_rows"] if r["bucket"] == "T2b"]
    n3_amb = [r for r in res["n3_table"] if r["judgement"] == "glued"]
    n_da = len(t2b) + len(amb_slots) + len(amb_fr) + len(n3_amb)
    a(f"### (다) 문장꼴(b) · 애매 전부 — {n_da} 행 (문장꼴(b) 문구 {len(t2b)} · 애매 노드 아님 {len(amb_slots)} · 남은 노드의 애매 {len(amb_fr)} · N3 애매 사전 값 {len(n3_amb)})")
    a("")
    a(f"**(다-1) 문장꼴(b) 문구 {len(t2b)}**(7차 자리로는 {len(t2b_slots)} — 「" + "」「".join(r["node"] for r in t2b_slots) + "」) — 절이 있고 멤버에 사전 사건이 없다. 노드 아님 · 사람이 사건을 정한다.")
    a("")
    rows = [[i, x["text"], len(x["locators"]), ", ".join(x["core7"]), "; ".join(x["clause_why"]), ", ".join(x["nouns"]), x["class"]] for i, x in enumerate(t2b, 1)]
    a(tbl(["#", "원문", "자리", "7차 핵심어", "왜 문장꼴(절)", "명사", "서술 분류 제안"], rows))
    a("")
    a(f"**(다-2) 애매 — 노드 아님 {len(amb_slots)}**")
    a("")
    a(tbl(["#", "7차 노드", "원장 횟수", "원문 예", "왜"], [[i, r["node"], r["n"], r.get("example"), " / ".join(r["ambiguous"])] for i, r in enumerate(amb_slots, 1)]))
    a("")
    a(f"**(다-3) 남은 노드 중 애매 표시 {len(amb_fr)}**(노드로 둠 · (가)에도 있음)")
    a("")
    a(tbl(["#", "노드", "원장 횟수", "원문 예", "왜 애매"], [[i, r["node"], r["n"], r["example"], " / ".join(r["ambiguous"])] for i, r in enumerate(amb_fr, 1)]))
    a("")
    a(f"**(다-4) N3 애매 — 띄어쓰기 없이 부위 말로 시작하는 사전 값 {len(n3_amb)}**(분해 안 함)")
    a("")
    a(tbl(["#", "사전 값", "부위 말", "나머지", "왜"], [[i, r["value"], r["site"], r["event"], r["why"]] for i, r in enumerate(n3_amb, 1)]))
    a("")
    # (라)
    a(f"### (라) N3 — 기존 사전 사건과 같은 사건으로 모이는 새 노드 {len(res['n3_merge'])} 행")
    a("")
    a(tbl(["#", "새 노드(3차 이름)", "원장 횟수", "7차 이름", "모이는 사전 사건", "동치(분해)"], [[i, x["node"], x["n"], ", ".join(x["from7"]), x["dict"], f"「{x['dict']}」 = (사건 {x['node']}, 부위 " + next((r["site"] for r in res["n3_table"] if r["value"] == x["dict"]), "?") + ")"] for i, x in enumerate(res["n3_merge"], 1)]))
    a("")
    a("제안(결정 아님 · 사전은 안 바꿈): `canonical_rename` adverse_event_type 「혈관 폐색」→「폐색」 + 「혈관 폐색」 자리는 부위 「혈관」 — 가능한지는 §8. N4 임시 부위 동맥·정맥·안동맥(parent 동맥)은 `dictionary_add`(site) 제안.")
    a("")
    # (마)
    n5 = res["n5_rows"]
    r30 = res["r30_rows"]
    a(f"### (마) 사용자 확인 — {len(n5) + len(r30)} 행 (폐색·색전 한 문구 {len(n5)} · R30 leads_to 후보 {len(r30)})")
    a("")
    a(f"N5: 폐색 ≠ 색전 — 3차 묶음에서 「폐색」/「혈관 폐색」 과 「색전」 이 한 묶음인 자리 **{len(res['n5_fold_check'])}**(접지 않음). `/` 는 대안(또는) — 「혈관폐색/색전」은 두 사건 모두에 붙는다(7차 멤버 구분자 그대로).")
    a("")
    a(tbl(["#", "원문", "붙은 사건(3차)", "「/」 대안 꼴", "locator"], [[i, x["text"], ", ".join(x["events"]), x["slash"], x["locator"]] for i, x in enumerate(n5, 1)]))
    a("")
    a("R30 leads_to 후보(제안 · 원장 한 문구 안에 두 사건 말이 같이 나온 자리 · 「막힘」은 「폐색」 쪽 말로 셌으나 같은 사건이라 놓지 않음 — 노드 「막힘」 은 따로 남음):")
    a("")
    a(tbl(["#", "원문", "후보", "인과 표지(인한·의한·일으킬…)", "붙은 사건(3차)", "locator"], [[i, x["text"], ", ".join(x["candidates"]), x["causal_marker"], ", ".join(x["events"]) or "— (부작용 문구 자리 아님)", x["locator"]] for i, x in enumerate(r30, 1)]))
    a("")

    # ---------------- 3
    a("## 3. 규칙이 만든 변경 전수")
    a("")
    nb = res["n1_back"]
    via = [x for x in nb if x["via_n1"]]
    a(f"### 3.1 N1 — 2차에 노드가 아니던(문장꼴·애매) 7차 자리 중 3차에 노드로 돌아온 것 {len(nb)} (N1 로 {len(via)} · N2 로 절이 아니게 되어 {len(nb) - len(via)})")
    a("")
    a(tbl(["#", "7차 노드", "원장 횟수", "2차", "3차", "3차 이름", "N1", "원문 예"], [[i, x["node7"], x["n"], x["cat2"], x["cat3"] + (f"({x['rule3']})" if x["rule3"] else ""), x["to3"] or x["node7"], x["via_n1"], x["example"]] for i, x in enumerate(nb, 1)]))
    a("")
    a(f"- N1 이름이 든 3차 노드(이름 기준) {len(res['n1_keys'])}: " + ", ".join(res["n1_keys"]))
    a(f"- 접속 조사 경계에서 뗀 N1 멤버 {len(res['n1_conj'])}: " + "; ".join(f"「{m}」→{', '.join(n)}" for m, n in res["n1_conj"]))
    a(f"- ANOM 어절을 통째 명사로 받은 것 {len(res['n1_anom_whole'])}: " + "; ".join(f"「{m}」→「{n}」" for m, n in res["n1_anom_whole"]) + f" · 조사·연결어미가 붙어 애매로 둔 ANOM {res['seglog_kinds'].get('ANOM', 0)} · 용언 어절이라 애매로 둔 자리(T1-pred) {res['seglog_kinds'].get('T1-pred', 0)}")
    a("")
    nr = res["n2_rejudge"]
    c = Counter(x["n2"] for x in nr)
    cn = Counter(x["n2"] for x in nr if x["status7"] in ("note", "sentence"))
    a(f"### 3.2 N2 — 2차 문장꼴 79 문구 다시 판정: 수식어 {c.get('수식어', 0)} · (a) {c.get('(a)', 0)} · (b) {c.get('(b)', 0)} · N1 명사형(절·수식어 없음) {c.get('N1 명사형(절·수식어 없음)', 0)}")
    a("")
    a(f"79 중 7차가 note·sentence 로 둔 {sum(cn.values())} 문구(분해·단위 없음 — 판정만): " + ", ".join(f"{k} {v}" for k, v in cn.items()) + ". 문구 안 멤버 중 하나라도 절이면 (a)/(b)(사전 사건 있음/없음).")
    a("")
    a(tbl(["#", "원문", "7차", "2차", "3차 N2", "절(왜)", "수식어(R1)", "N1 명사형", "사전 사건", "선 노드", "locator"],
          [[i, x["text"], x["status7"], x["t2_2nd"], x["n2"], "; ".join(x["clause_why"]), ", ".join(x["mods"]), ", ".join(x["n1"]), ", ".join(x["dict_events"]), ", ".join(x["nodes"]), x["locator"]] for i, x in enumerate(nr, 1)]))
    a("")
    a("### 3.3 N3 — 사전 사건 43 canonical 전수(+ 부위 꼴 동의어) 분해 표")
    a("")
    n3 = res["n3_table"]
    cc = Counter((r["role"], r["judgement"]) for r in n3)
    a(f"canonical 43: 분해 {cc.get(('canonical', 'split'), 0)} · 붙은 꼴 애매 {cc.get(('canonical', 'glued'), 0)} · 분해 안 함 {cc.get(('canonical', 'no'), 0)} · 동의어 중 부위 꼴(분해 가능) {cc.get(('synonym', 'split'), 0)}(이미 그 사건 canonical 로 감 — 동치표만 일치 확인).")
    a("")
    a(tbl(["#", "canonical", "값", "역할", "판정", "사건", "부위", "왜", "승인 3"], [[i, r["canonical"], r["value"], r["role"], {"split": "분해", "glued": "애매(붙은 꼴)", "no": "분해 안 함"}[r["judgement"]], r["event"], r["site"], r["why"], r["approved_decision"]] for i, r in enumerate(n3, 1)]))
    a("")
    r1n = res["r1_new"]
    r1n_new = [x for x in r1n if not x["in_7th_modifiers"]]
    a(f"### 3.4 R1 후보(새) — N2 가 관형어·부사어 하나(수식어)로 본 말 {len(r1n)} 중 R1 목록(1차 R1 = 발주서 목록 ∪ 7차 수식어 138)에 없는 새 후보 {len(r1n_new)} (노드 이름에서 실제로 뗀 자리 합 {res['r1_new_applied_total']})")
    a("")
    a("부작용 문구 자리(2,285)·complications 이름의 절 없는 멤버에서 센 출현 · 「7차 수식어」 예 = 7차 stopwords(수식어 138 등)에 이미 있어 7차가 이미 떼던 말(R1 목록 안 · 새 후보 아님 · 이번에 이름이 바뀌지 않음).")
    a("")
    a(tbl(["#", "말", "출현", "노드 이름에서 뗀 자리", "7차 수식어", "원문 예", "비고"], [[i, x["word"], x["phrase_occ"], x["applied_in_node_names"], x["in_7th_modifiers"], x["example"], x.get("note")] for i, x in enumerate(r1n, 1)]))
    a("")
    a("### 3.5 N4 — 임시 부위 값")
    a("")
    a(tbl(["임시 값", "parent", "부위로 떨어진 자리"], [[w, p, sum(n for s, h, n in res["n4_count"] if s == w)] for w, p in res["n4_sites"]]))
    a("")
    a(tbl(["#", "부위", "어떻게", "멤버", "뒤 말", "붙은 사건", "locator"], [[i, r["site"], r["how"], r["member"], r["rest"], ", ".join(r["events"]), r["locator"]] for i, r in enumerate(res["n4_rows"], 1)]))
    a("")
    a("「혈관계 합병증(안동맥 역행성 색전)」 → 괄호 안 사건 「색전」(사전) · 부위 「안동맥」(N4) · 수식 「역행성」(R1 후보 · §3.4). 괄호 앞 「혈관계 합병증」 은 노드로 남는다(「혈관계」= 혈관/NNG+계/XSN 이라 R2 말 「혈관」과 다름 · ⑦ 상대 「합병증」).")
    a("")
    sp = res["s_pairs"]
    a(f"### 3.6 S 로 접힌 쌍 — 게이트 23 중 {len(sp)} + N1 로 돌아온 쌍 {len(res['s_back_n1'])}(23 안) + 규칙 뒤 새 접미 쌍(N1 노드 한쪽) {len(res['s_new_n1'])}")
    a("")
    back = {(x["a"], x["b"]) for x in res["s_back_n1"]}
    a(tbl(["#", "쌍", "규칙", "N1 로 돌아옴"], [[i, f"{x['a']} ↔ {x['b']}", "/".join(x["rules"]), (x["a"], x["b"]) in back] for i, x in enumerate(sp, 1)]))
    a("")
    a(f"S 적용 못 한 게이트 쌍 {len(res['s_ambiguous'])}" + (": " + "; ".join(f"{x['a']}↔{x['b']}" for x in res["s_ambiguous"]) if res["s_ambiguous"] else "") + f" · 규칙 뒤 접미 쌍 중 N1 노드가 아닌 새 쌍 {len(res['s_new_other'])}(S 를 넓히지 않음 — 있으면 ⑦ 에 남김).")
    a(f"R4 병기 쌍 {len(res['r4_pairs'])}: " + "; ".join(f"「{x['a']}」=「{x['b']}」" for x in res["r4_pairs"]) + f" · R4 애매 {len(res['r4_ambiguous'])}: " + "; ".join(f"「{x['a']}」=「{x['b']}」({x['kind']})" for x in res["r4_ambiguous"]))
    a(f"R3 버린 토막 {len(res['r3_dropped'])}" + (": " + ", ".join(x["node"] for x in res["r3_dropped"]) if res["r3_dropped"] else ""))
    a("")

    # ---------------- 4
    ds = res["dest_2nd"]
    a(f"## 4. 2차 남음 146 + 문장꼴 30 + 애매 18 → 3차 행선지 전수 {len(ds)} (「이유 없음」 {len(res['dest_no_reason'])})")
    a("")
    cnt = Counter((x["cat2"], x["dest3"]) for x in ds)
    a(tbl(["2차", "3차", "자리"], [[k[0], k[1], v] for k, v in sorted(cnt.items())]))
    a("")
    moved = [x for x in ds if x["dest3"] != "남음" or x["cat2"] != "2차 남음"]
    stay = [x for x in ds if x["dest3"] == "남음" and x["cat2"] == "2차 남음"]
    a(f"2차 남음이 3차에도 남은 {len(stay)} 은 (가) 목록에 같은 이름으로 있다(행 생략 · 이름: " + ", ".join(x["node"] for x in stay) + ").")
    a("")
    a(f"그 밖 {len(moved)} 행:")
    a("")
    a(tbl(["#", "7차 노드", "원장 횟수", "2차", "3차", "왜(어디로)"], [[i, x["node"], x["n"], x["cat2"], x["dest3"], x["why"]] for i, x in enumerate(moved, 1)]))
    a("")

    # ---------------- 5
    a("## 5. 사건 노드 수 · ⑦ strong 재계산")
    a("")
    a(tbl(["", "1차", "2차", "3차"], [
        ["사전 사건", 40, 43, 43],
        ["남는 새 사건 노드(묶음)", res["first_nodes"]["node_groups_after_R4S"], res["second"]["final_node_groups"], nd["final_node_groups"]],
        ["사건 노드 합", 40 + res["first_nodes"]["node_groups_after_R4S"], 43 + res["second"]["final_node_groups"], 43 + nd["final_node_groups"]],
        ["⑦ strong(규칙 뒤 재계산 쌍)", res["first_strong_recalc"], res["second"]["strong_after_rules"], sr["strong_after_rules"]],
        ["⑦ 96 자리 남음", T1["dup-strong"]["remaining"], T2["dup-strong"]["remaining"], T["dup-strong"]["remaining"]],
    ]))
    a("")
    a("1차 「사전 사건 40」은 1차 report 기준(승인 3 전). 3차 새 strong 쌍(96 밖): " + ("; ".join(f"{p['a']} ↔ {p['b']}({'/'.join(p['rules'])})" for p in sr["new_pairs"]) or "없음") + ".")
    a("")

    # ---------------- 6
    ph = res["phrases"]
    a("## 6. 부작용 문구 2,285 중 사건 칸이 비는 수")
    a("")
    a("문구 판정(7차 judge_phrase · new/exact 는 「원장 노드 사건이 있나」): " + ", ".join(f"{k} {v}" for k, v in ph["by_status"].items()) + ".")
    a("")
    a(f"- exact·new 문구 중 사건 칸이 빈 문구(문장꼴(b) · 애매 제외): **{len(ph['empty_event_cell'])}**")
    a(f"- 따로: 문장꼴(b) 때문에 빈 문구 **{len(ph['empty_t2b'])}**(2차 {res['second']['empty_t2b']}) · 애매 — 사용자(노드 아님) 때문에 빈 문구 **{len(ph['empty_amb_user'])}**(2차 {res['second']['empty_amb']}) · complications 이름 중 빈 것 {len(ph['names_empty'])}")
    a("")
    a(tbl(["locator", "원문", "토막 결과"], [[x[0], x[1], ", ".join(x[2])] for x in ph["empty_t2b"] + ph["empty_amb_user"]]))
    a("")

    # ---------------- 7
    a("## 7. 7차 불변 확인")
    a("")
    if verify:
        a(f"명령(`silver-v3/` · 시스템 `{verify['python3']}`): `{verify['cmd']}` → exit {verify['returncode']}")
        a("")
        a(f"- determinism key: out = `{verify['key_out']}` · baseline/manifest-7차.json = `{verify['key_baseline']}` → **{'같음' if verify['key_out'] == verify['key_baseline'] else '다름'}**")
        same = verify["out_hash_before"] == res["out_hash_after_analysis"] == verify["out_hash_after_build"]
        a(f"- out/ 트리 해시: 드라이런 전 `{verify['out_hash_before']}` · 분석 뒤 `{res['out_hash_after_analysis']}` · 빌드 뒤 `{verify['out_hash_after_build']}` → **{'전부 같음' if same else '다름'}**")
        a("")
        a("```")
        a(verify["stdout"].rstrip())
        a("--- stderr ---")
        a(verify["stderr"].rstrip())
        a("```")
    else:
        a("(아직 --verify 로 돌리지 않음)")
    a("")

    # ---------------- 8
    a("## 8. 빌더 반영 설계 메모(사실만 · 판단은 사용자)")
    a("")
    for line in res["builder_memo"]:
        a(line)
    a("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
