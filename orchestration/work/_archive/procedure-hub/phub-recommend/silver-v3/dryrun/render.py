# -*- coding: utf-8 -*-
"""out-dryrun/report.md — dryrun.json(센 값) · verify-7차.json 을 그대로 옮긴다. 여기서 새로 세는 수는 없다(합계·차만)."""

RULES = ("R2", "R1", "R3", "R4", "S")
BNAME = {"ledger-nodes": "새 사건 노드", "dup-strong": "⑦ strong", "seeds": "씨앗", "batch3": "묶음3 미결"}
R3_EXAMPLES = ["손상", "반응", "자극", "표정", "감각", "알레르기", "약화", "마비", "염증", "합병증", "최소", "실의", "CO2", "눈썹", "주름"]


def esc(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def node_reason(r):
    if r["ambiguous"]:
        return "애매 — " + " / ".join(r["ambiguous"])
    p = []
    if r["n_after"] != r["n"]:
        p.append(f"다른 노드가 규칙으로 합류(원장 자리 {r['n']}→{r['n_after']})")
    if r["sole"]:
        p.append(f"R3 후보(단독 0)지만 「{r['sole']}」의 유일한 사건 칸 → R3 단서로 유지")
    elif r["edge_words"]:
        p.append("앞뒤 말 " + "·".join(f"「{w}」" for w in r["edge_words"]) + " 은 R1·R2 목록 밖")
    else:
        p.append(f"한 낱말 · R1·R2 말 없음 · 단독 출현 {r['solo_strict']}")
    if r.get("group"):
        p.append("R4·S 로 " + ", ".join(f"「{x}」" for x in r["group"]) + " 이 이 노드에 접힘(남는 이름 표시용)")
    p.append(("⑦ strong 남음: " + ", ".join(r["partners"])) if r["partners"] else ("" if r.get("group") else "병기(R4)·접미(S) 쌍 없음"))
    p = [x for x in p if x]
    return " · ".join(p) + " → 부작용 여부·종류는 사람"


def dup_reason(r):
    rules = set(r["rules"])
    if r["ambiguous"]:
        base = "애매 — " + " / ".join(r["ambiguous"])
    elif "jamo1" in rules:
        base = "자모 1 치환 — 가정 S 밖(자모는 같다고 놓지 않음)"
    elif "word_contains" in rules:
        base = "낱말 포함(word_contains) — R1~R4·S 어디에도 안 듦 · 같은지는 사람"
    else:
        base = "규칙 " + "/".join(r["rules"]) + " — R1~R4·S 밖"
    now = tuple(r["now"]) if r["now"] else None
    if now and (now[0] != r["a"] or now[1] != r["b"]):
        base += f" (규칙 뒤 「{now[0]}」↔「{now[1]}」)"
    if not r.get("in_recalc"):
        base += " · 규칙 뒤 재계산에선 strong 아님"
    return base


def write(res, verify, path):
    T = res["table"]
    L = []
    a = L.append
    a("# 드라이런 — 묶음5 432 자리를 규칙 R1~R4·S 로 세기 (2026-11-05)")
    a("")
    a("발주서 `../../silver-dryrun-brief.md` · 코드 `silver-v3/dryrun/`(run_dryrun.py · dry_au.py · render.py) · 센 값 원본 `out-dryrun/dryrun.json`. **결정이 아니라 드라이런이다.** 이 문서의 수는 전부 코드가 센 값이다(추정 0).")
    a("7차 산출물(`out/` · `decisions/` · `baseline/` · lib · ERD · 브론즈)은 읽기만 했다 — 드라이런은 한 프로세스 안에서 `lib.v32.AdverseUnits32` 를 감싼 클래스로 바꿔 끼워 분해를 다시 돌렸다(§6 에 7차 불변 확인).")
    a("")
    # -------------------------------------------------------------- 규칙 구현
    a("## 0. 규칙을 기계로 옮긴 방식(센 값이 이 정의를 따른다)")
    a("")
    a("- 0 단계(규칙 없음)로 감싼 클래스를 돌려 7차 노드 260 · ⑦ strong 96 과 이름·쌍이 같음을 먼저 확인했다(assert).")
    a("- **R2** — 사전 사건이 없는 토막(노드 핵심어가 서는 곳)에서 R2 말 바로 뒤에 핵심어 토큰이 더 있으면 그 말을 부위로 뗀다(조사 붙은 꼴 「눈이」도 같은 말). 뒤에 용언 꼴(무거운·건조해지는)만 있으면 「사건 앞」인지 애매 → 적용 안 함·애매. 단독(「경미한 결막」)은 「사건 앞」이 아니라 적용 안 함. 뗀 부위는 단위 칸에 넣지 않고 기록만(드라이런 임시 값).")
    a("- **R1** — 핵심어 토큰열의 맨 앞·맨 뒤 R1 말을 뗀다(핵심어가 하나 이상 남을 때만). 목록은 발주서 문장의 말과 괄호 꼴(일시/일시적 …) 그대로 — 「…」을 넓히지 않았다. 사전 사건 토막(「감각 이상」은 사전 값)은 건드리지 않는다.")
    a("- **R1·R2 공통** — 띄어쓰기 없이 붙은 꼴(「피부위축」「색소이상」「미세출혈」)은 「앞뒤 말」인지 애매 → 적용 안 함·애매(R2 는 2 글자 이상 말만 검사 · 「눈부심」 같은 1 글자 「눈」+ 꼴은 검사하지 않음).")
    a("- **R3** — R1·R2 뒤 분해에서 노드 W 의 **단독 출현** = W 가 핵심어인 토막에서 W 말고 남는 내용(용언 꼴 · 정도·경과·빈도가 아닌 기존 수식어 — 증상·현상·느낌·부작용·노출 …)이 없는 자리 수. 단독 0 이고, W 가 사건인 모든 자리에 다른 사건이 있을 때만 버린다(「아무 문구의 사건 칸을 차지하지 않는 토막」). W 가 어느 자리의 유일한 사건이면 유지. 기존 수식어 138 전부를 빼면 단독이 되는 노드(엄격 0 · 느슨 >0)는 기준이 애매 → 적용 안 함·애매.")
    a("- **R4** — 원장 문자열(부작용 축 전부 · 타임라인 포함)에서 멤버(· / , + : ; — 및 또는 -- 로 가른 토막) 안의 「X (Y)」: X = 토막 처음부터 괄호까지 전부, Y = 괄호 안(구분자 없음). 둘 다 사건 키(사전 사건·규칙 뒤 노드)면 같은 사건. 7차에선 쌍이던 것이 R1/R2 로 한쪽이 바뀌었거나, X·Y 에서 R1/R2 말을 떼야만 쌍이 되면 애매.")
    a("- **S** — 7차 ⑦ strong 중 규칙 suffix_감·suffix_증·suffix_형성 23 쌍을 같다고 놓는다(두 끝이 규칙 뒤에도 그대로일 때). jamo1 3 쌍은 같다고 놓지 않는다. 규칙 뒤 새로 생긴 접미 꼴 쌍이 있으면 23 쌍 밖이라 애매(이번엔 0).")
    a("- 접기 묶음(R4→S)의 이름: 사전 사건이 있으면 사전 값, 노드끼리면 원장 자리가 많은 쪽을 표시용으로 남겼다(이름은 사용자 몫 · 자리 수에는 영향 없음).")
    a("- 자리 판정 순서 R2→R1→R3→R4→S · 겹치면 먼저 적용된 규칙에 센다. ⑦ 쌍은 (a) 두 끝이 한 노드가 됨 (b) 한쪽이 사라짐 (c) 바뀐 쌍이 더는 strong 이 아님 (d) 다른 자리와 같은 쌍이 됨(중복 — 그 쌍을 만든 규칙에 셈)이면 닫힘.")
    a("")
    # -------------------------------------------------------------- §1
    a("## 1. 자리 수 — 묶음 × 규칙")
    a("")
    rows = []
    tot = {k: 0 for k in ("slots",) + RULES + ("remaining", "ambiguous")}
    for b, t in T.items():
        rows.append([BNAME[b], t["slots"]] + [t[r] for r in RULES] + [sum(t[r] for r in RULES), t["remaining"], t["ambiguous"]])
        for k in tot:
            tot[k] += t[k]
    rows.append(["**합계**", tot["slots"]] + [tot[r] for r in RULES] + [sum(tot[r] for r in RULES), tot["remaining"], tot["ambiguous"]])
    a(tbl(["묶음", "자리", "R2", "R1", "R3", "R4", "S", "닫힘 계", "남음", "남음 중 애매 — 사용자"], rows))
    a("")
    nn = res["nodes"]["new_node_names"]
    ns = res["strong_recalc"]["new_pairs"]
    a(f"**규칙이 새로 만든 자리**(432 밖): 새 노드 이름 {len(nn)}(§2.2) · 새 ⑦ strong 쌍 {len(ns)}(§2.4). "
      f"→ 규칙 적용 뒤 사람이 볼 자리 = 남은 {tot['remaining']} + 새 노드 {len(nn)} + 새 쌍 {len(ns)} = **{tot['remaining'] + len(nn) + len(ns)}** "
      f"(그중 애매 — 사용자 = 남은 자리 {tot['ambiguous']} + 새 노드 {sum(1 for x in nn if x['ambiguous'])} + 새 쌍 {sum(1 for x in ns if x['ambiguous'])}).")
    a("")
    a("씨앗 61 · 묶음3 미결 15 는 규칙 R1~R4·S 의 대상(사건 노드 이름 · ⑦ 쌍)이 아니라 0 이다. 씨앗 부위 「눈꺼풀」「두피」는 R2 말과 같은 값이지만 R2 의 부위는 드라이런 임시 값이고 실제 사전 추가는 승인(dictionary_add) 몫이라 그 자리를 닫지 않았다.")
    a("")
    # -------------------------------------------------------------- §2
    a("## 2. 남는 자리 전부")
    a("")
    rem_nodes = [r for r in res["node_rows"] if not r["rule"]]
    a(f"### 2.1 새 사건 노드 — 남음 {len(rem_nodes)} (원장 횟수 = 7차 → 규칙 뒤)")
    a("")
    a(tbl(["#", "노드", "원장 횟수", "왜 규칙으로 안 닫히나"], [[i + 1, (r["name_after"] or r["node"]) + (f" (7차 「{r['node']}」)" if r["name_after"] and r["name_after"] != r["node"] else ""), f"{r['n']} → {r['n_after']}", node_reason(r)] for i, r in enumerate(rem_nodes)]))
    a("")
    a(f"### 2.2 규칙이 새로 세운 노드 이름 {len(nn)} (260 에 없던 이름)")
    a("")
    a(tbl(["노드", "원장 횟수", "어디서", "단독 출현", "⑦ strong", "애매"], [[x["node"], x["n"], ", ".join(x["from"]), x["solo_strict"], ", ".join(x["partners"]) or "—", " / ".join(x["ambiguous"]) or "—"] for x in nn]))
    a("")
    rem_dup = [r for r in res["dup_rows"] if not r["rule"]]
    a(f"### 2.3 ⑦ strong — 남음 {len(rem_dup)}")
    a("")
    a(tbl(["#", "쌍", "규칙", "왜 규칙으로 안 닫히나"], [[i + 1, f"{r['a']} ↔ {r['b']}" + (" (사전)" if r["b_kind"] == "dictionary" else ""), "/".join(r["rules"]), dup_reason(r)] for i, r in enumerate(rem_dup)]))
    a("")
    a(f"### 2.4 규칙 뒤 새로 생긴 ⑦ strong {len(ns)}")
    a("")
    a(tbl(["쌍", "규칙", "애매"], [[f"{x['a']} ↔ {x['b']}", "/".join(x["rules"]), " / ".join(x["ambiguous"]) or "—"] for x in ns]))
    a("")
    a(f"### 2.5 씨앗 {len(res['seed_slots'])} · 묶음3 미결 {len(res['b3_slots'])} — 전부 남음(규칙 대상 아님)")
    a("")
    a(tbl(["묶음", "자리", "항목", "왜"], [[g, sid, title, "사전 씨앗 승인 — R1~R4·S 는 사건 노드·⑦ 규칙이라 닫지 않음"] for g, sid, title in res["seed_slots"]] +
          [[g, sid, title, "묶음 3 미결(이름·기법·부위 동의어·수식 단위·기록) — 규칙 밖"] for g, sid, title in res["b3_slots"]]))
    a("")
    # -------------------------------------------------------------- §3
    a("## 3. 규칙이 만든 변경 전수")
    a("")
    a("### 3.1 R1 수식어 — 발주서 목록(괄호 꼴 포함) · 원장 전수에서 사건 핵심어 앞뒤에 붙은 횟수")
    a("")
    a("「138」 = 기존 stopwords 138 의 부류(없으면 —) · 「경과 사전」 = course 사전 값·동의어 · 「사건 앞뒤」 = 부작용 축 원장 문자열 전부에서 그 말 바로 앞·뒤 토큰이 사건(사전 사건 표면 · 7차/규칙 뒤 노드 낱말)인 횟수 · 「뗀 횟수」 = 드라이런이 노드 이름에서 뗀 자리 수(이름·safety 문구). R1 목록 = 이 표 ∪ 138.")
    a("")
    a(tbl(["말", "138", "경과 사전", "새로 추가", "사건 앞뒤", "원장 토큰 수", "뗀 횟수", "뗀 이름(R2 뒤)"],
          [[t["word"], t["in_138"] or "—", "○" if t["course_dict"] else "—", "○" if not t["in_138"] and not t["course_dict"] else "—", t["adjacent_to_event"], t["token_total"], t["stripped_in_dryrun"], ", ".join(t["from_names"]) or "—"] for t in res["r1_table"]]))
    a("")
    ew = res["edge_words_outside_rules"]
    a(f"참고(적용 안 함) — 남은 여러 낱말 노드의 앞뒤 말 중 R1·R2 목록 밖 {len(ew)} 말: " + " · ".join(f"{x['word']}({len(x['nodes'])})" for x in ew) + ". 정도·경과·빈도인지는 사람이 본다(규칙을 넓히지 않음).")
    a("")
    a("### 3.2 R2 구조·부위 말 — 임시 site 값")
    a("")
    a(tbl(["말", "기존 사전", "드라이런 임시 값", "뗀 횟수", "바뀐 이름(앞 → 뒤)"],
          [[t["word"], t["existing_dict"] or "없음", t["temp_site"] or "— (기존 값)", t["stripped_in_dryrun"], ", ".join(f"{x[0]}→{x[1]}" for x in t["names"]) or "—"] for t in res["r2_table"]]))
    a("")
    a("「신경 손상」→(손상, 신경[임시]) 과 「혈관 손상」→(손상, 혈관[사전]) 은 둘 다 사건 칸 「손상」 — 같은 꼴(사건 노드 「손상」 원장 자리 7차 3 → 규칙 뒤 " + str(next((r["n_after"] for r in res["node_rows"] if r["node"] == "손상"), "?")) + "). 「신경손상」처럼 붙여 쓴 자리는 애매로 남았다(§2.1).")
    a("")
    a("R2 를 적용하지 않은 자리: " + (" · ".join(f"「{t}」({w} 뒤 용언 {'/'.join(p)})" for w, c, p, t in dict(((x[3], x) for x in res["r2_before_pred"])).values()) or "없음") +
      " — 애매 · " + (" · ".join(f"「{t}」({w} 단독)" for w, c, t in dict(((x[2], x) for x in res["r2_alone"])).values()) or "없음") + " — 사건 앞 아님.")
    a("")
    a(f"### 3.3 R3 버린 토막 {len(res['r3_dropped'])}")
    a("")
    a(tbl(["말", "단독(엄격/느슨)", "어느 문구의 조각", "그 문구에 남는 사건"], [[x["node"], f"{x['solo_strict']}/{x['solo_loose']}", " / ".join(sorted({o[1] for o in x["occurrences"]})), ", ".join(sorted({e for o in x["occurrences"] for e in o[2]}))] for x in res["r3_dropped"]]))
    a("")
    a(f"R3 후보(엄격 단독 0)인데 어느 문구의 유일한 사건 칸이라 유지 {len(res['r3_sole_kept'])}: " + " · ".join(f"{x['node']}(「{x['text']}」)" for x in res["r3_sole_kept"]))
    a("")
    a(f"R3 애매(엄격 0 · 기존 수식어 138 을 다 빼면 단독) {len(res['r3_ambiguous'])}: " + " · ".join(f"{x['node']}(" + " / ".join("+".join(c[1]) for c in x["contexts"][:1]) + ")" for x in res["r3_ambiguous"]))
    a("")
    a(f"R3 애매(단독 자리가 전부 괄호 안 · 모든 자리에 다른 사건) {len(res['r3_ambiguous_paren'])}: " + (" · ".join(f"{x['node']}(" + " / ".join(f"「{t}」" for t in x["texts"]) + ")" for x in res["r3_ambiguous_paren"]) or "없음"))
    a("")
    alive = {r["node"]: r for r in res["node_rows"]}
    ex = []
    for w in R3_EXAMPLES:
        r = alive.get(w)
        if r is None:
            ex.append(f"{w}(7차 노드 아님)")
        elif r["rule"]:
            ex.append(f"{w}({r['rule']})")
        else:
            ex.append(f"{w}(남음 · 단독 {r['solo_strict']})")
    a("발주서 R3 예시 말이 이번 판정에서 어떻게 됐나: " + " · ".join(ex) + ".")
    a("")
    a(f"### 3.4 R4 병기 쌍 {len(res['r4_pairs'])} · 애매 {len(res['r4_ambiguous'])}")
    a("")
    a(tbl(["쌍", "원문", "판정"], [[f"{x['a']} = {x['b']}", " / ".join(x["texts"]), "같은 사건(적용)"] for x in res["r4_pairs"]] +
          [[f"{x['a']} ? {x['b']}", " / ".join(x["texts"]), "애매 — " + ("R1/R2 말을 떼야만 쌍(괄호 앞 범위)" if x["kind"] == "stripped" else "7차 쌍의 한쪽이 R2 로 (사건, 부위)") + " · 적용 안 함"] for x in res["r4_ambiguous"]]))
    a("")
    a(f"### 3.5 S 로 접힌 쌍 {len(res['s_pairs'])}" + (f" · 애매 {len(res['s_ambiguous'])}" if res["s_ambiguous"] else ""))
    a("")
    a(tbl(["쌍", "규칙", "남긴 이름"], [[f"{x['a']} ↔ {x['b']}" + (" (사전)" if x["b_kind"] == "dictionary" else ""), "/".join(x["rules"]), x["kept"]] for x in res["s_pairs"]]))
    a("")
    a("접기 묶음(R4·S · 둘 이상): " + " · ".join("{" + ", ".join(g["members"]) + "} → " + (g["dict"][0] + "(사전)" if g["dict"] else g["kept"] + "(표시용)") for g in res["groups"]))
    a("")
    # -------------------------------------------------------------- §4
    N = res["nodes"]
    S = res["strong_recalc"]
    a("## 4. 규칙 적용 뒤 사건 노드 수 · ⑦ strong 재계산")
    a("")
    extra = sorted(set(N["dict_events_names"]) - set(N["erd_base_events"]))
    a(tbl(["항목", "수"], [
        ["사건 사전(7차 · ERD 40 + approved 결정 " + "·".join(extra) + ")", N["dict_events"]],
        ["원장 사건 노드 7차", N["nodes_7th"]],
        ["R2 뒤 노드", N["nodes_after_R2"]],
        ["R2+R1 뒤 노드", N["nodes_after_R2R1"]],
        ["R3 버림", N["r3_dropped"]],
        ["R3 뒤 노드", N["alive_after_R3"]],
        ["R4·S 접기 뒤 노드(= 남은 7차 노드 " + str(sum(1 for r in res['node_rows'] if not r['rule'])) + " + 새 이름 " + str(len(nn)) + ")", N["node_groups_after_R4S"]],
        ["**사건 노드 계(사전 " + str(N["dict_events"]) + " + 노드 " + str(N["node_groups_after_R4S"]) + ")** · ERD 40 기준이면 40 + " + str(N["node_groups_after_R4S"]) + " = " + str(40 + N["node_groups_after_R4S"]), N["dict_events"] + N["node_groups_after_R4S"]],
        ["⑦ strong 7차", N["strong_7th"]],
        ["⑦ strong 규칙 뒤 재계산(R3 버린 노드 빼고 · R4·S 같은 묶음 빼고 · 묶음 단위 중복 제거)", S["strong_after_rules"]],
        ["  그중 남은 432 자리에서 온 쌍", S["remaining_slots_in_recalc"]],
        ["  그중 새로 생긴 쌍", S["of_which_new"]],
        ["남은 ⑦ 자리 중 재계산에선 strong 이 아닌 것", len(S["remaining_slots_not_in_recalc"])],
        ["⑦ weak 규칙 뒤(게이트 밖 · 7차 " + str(N["weak_7th"]) + ")", S["weak_after_rules"]],
    ]))
    a("")
    if S["remaining_slots_not_in_recalc"]:
        a("재계산에선 strong 이 아닌 남은 ⑦ 자리: " + " · ".join(f"{x['a']}↔{x['b']}(규칙 뒤 {x['now'][0]}↔{x['now'][1]})" for x in S["remaining_slots_not_in_recalc"]) + " — 둘 다 애매라 닫지 않고 남겼다.")
        a("")
    # -------------------------------------------------------------- §5
    P = res["phrases"]
    a("## 5. 부작용 문구 2,285 — 사건 칸이 비는 문구")
    a("")
    a(tbl(["", "7차", "규칙 뒤"], [[k, P["by_status_7th"].get(k, 0), P["by_status_after"].get(k, 0)] for k in ("exact", "new", "note", "sentence")] + [["계", sum(P["by_status_7th"].values()), P["occurrences"]]]))
    a("")
    a(f"exact·new 문구 중 규칙 뒤(R3 버림 반영) 사건 칸이 빈 자리 = **{len(P['empty_event_cell'])}** · complications 이름 중 빈 자리 = **{len(P['names_empty_event_cell'])}**. "
      "메모(note)·설명문(sentence) 41 은 7차 판정 그대로(사건 칸이 없는 종류 — 규칙이 바꾸지 않음).")
    if P["empty_event_cell"]:
        a("")
        a(tbl(["locator", "문구"], P["empty_event_cell"]))
    a("")
    # -------------------------------------------------------------- §6
    a("## 6. 7차 불변 확인")
    a("")
    if not verify:
        a("(아직 안 돌림 — `python3 dryrun/run_dryrun.py --verify`)")
    else:
        same = verify["key_out"] == verify["key_baseline"]
        a(f"명령 `{verify['cmd']}`(silver-v3) · 종료 코드 {verify['returncode']}")
        a("")
        a(f"- determinism key — out/manifest.json `{verify['key_out']}` · baseline/manifest-7차.json `{verify['key_baseline']}` → **{'같음' if same else '다름'}**")
        a(f"- out/ 트리 해시(파일 경로+내용) — 드라이런 시작 전 `{verify['out_hash_before']}` · 빌드 뒤 `{verify['out_hash_after_build']}` → **{'같음' if verify['out_hash_before'] == verify['out_hash_after_build'] else '다름'}**")
        a(f"- 드라이런 분석 직후(빌드 전) out/ 해시 `{res['out_hash_after_analysis']}` → 시작 전과 {'같음' if res['out_hash_after_analysis'] == res['out_hash_before'] else '다름'}")
        a("")
        a("출력 그대로:")
        a("")
        a("```")
        a(verify["stdout"].rstrip())
        if verify["stderr"].strip():
            a("--- stderr ---")
            a(verify["stderr"].rstrip())
        a("```")
    a("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
