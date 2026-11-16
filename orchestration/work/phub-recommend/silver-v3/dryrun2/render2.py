# -*- coding: utf-8 -*-
"""out-dryrun2/report.md — dryrun2.json(센 값) · verify-7차.json 을 그대로 옮긴다. 여기서 새로 세는 수는 없다(합계·차만)."""
from collections import Counter

BNAME = {"ledger-nodes": "새 사건 노드", "dup-strong": "⑦ strong", "seeds": "씨앗", "batch3": "묶음3 미결"}
COLS = ["T1", "T2a", "T3", "T4", "R2", "R1", "R3", "R4", "S"]


def esc(x):
    if isinstance(x, (list, tuple)):
        x = ", ".join(str(y) for y in x)
    return str(x if x is not None else "—").replace("|", "\\|").replace("\n", " ")


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
        p.append(f"원장 자리 {r['n']}→{r['n_after']}(규칙으로 다른 자리가 합류하거나 일부 자리가 문장꼴·서술로 빠짐)")
    toks = r["node"].split()
    if r["sole"]:
        p.append(f"R3 후보(단독 0)지만 「{r['sole']}」의 유일한 사건 칸 → 유지")
    elif len((r["name_after"] or r["node"]).split()) > 1:
        nm = (r["name_after"] or r["node"]).split()
        p.append("명사 여럿 · 앞뒤 명사 " + "·".join(f"「{w}」" for w in sorted({nm[0], nm[-1]})) + " 은 R1·R2 목록 밖")
    else:
        p.append(f"명사 하나 · R1·R2 말 없음 · 단독 출현 {r['solo_strict']}")
    if r.get("group"):
        p.append("R4·S 로 " + ", ".join(f"「{x}」" for x in r["group"]) + " 이 이 노드에 접힘(남는 이름 표시용)")
    p.append(("⑦ strong 남음: " + ", ".join(r["partners"])) if r["partners"] else ("" if r.get("group") else "병기(R4)·접미(S) 쌍 없음"))
    return " · ".join(x for x in p if x) + " → 부작용 여부·종류는 사람"


def write(res, verify, path):
    T, T1 = res["table"], res["table_1st"]
    L = []
    a = L.append
    nd = res["nodes"]
    a("# 드라이런 2차 — 형태소 분석기(Kiwi)로 부작용 핵심어 다시 뽑기 (2026-11-06)")
    a("")
    a(f"발주서 `../../silver-dryrun2-brief.md` · 코드 `silver-v3/dryrun2/`(run_dryrun2.py · dry2_au.py · kiwi_t0.py · common2.py · render2.py) · 센 값 원본 `out-dryrun2/dryrun2.json` · 인터프리터 `silver-v3/.venv-kiwi/bin/python`(kiwipiepy {res['kiwi']['version']}).")
    a("**결정이 아니라 드라이런이다.** 이 문서의 수는 전부 코드가 센 값이다(추정 0). 7차 산출물(`out/` · `decisions/` · `baseline/` · lib · ERD · 브론즈)과 1차 코드(`dryrun/`)는 읽기만 했다 — 한 프로세스 안에서 `lib.v32.AdverseUnits32` 를 감싼 클래스로 바꿔 끼워 7차 분해를 다시 돌렸다(§8).")
    a("")
    a("## 0. 규칙을 기계로 옮긴 방식(센 값이 이 정의를 따른다)")
    a("")
    a("- **바꾼 곳은 하나**: 7차 분해에서 사전 사건이 없는 토막(노드 핵심어가 서는 곳)의 핵심어 뽑기. 묶음(괄호 밖·안)·멤버(구분자)·사전 값 통째 일치·수식어 138·접속 조사 토막·결정은 7차 그대로. 토막마다 「7차 핵심어 → 2차 결과」를 기록했고(879 토막), 7차 노드 260 의 원장 자리(locator)가 기록과 하나도 어긋나지 않음을 assert 로 확인했다.")
    a(f"- **T0** — 7차 실버가 쓰는 사전 {res['t0']['n_dictionaries_used']} 개(ERD 사전 49 중 `phrase_dictionary` 를 뺀 것 · 승인 결정 반영 · 사건 {res['t0']['event_entries']} = 40 + 3)의 canonical·synonym {res['t0']['value_pairs']} 개(사전×값) → 서로 다른 값 {res['t0']['registered_unique']} 개를 Kiwi 사용자 단어(NNG)로 등록했다(글자 없는 값 {len(res['t0']['skipped_no_letters'])} 개는 등록 안 함 · 실패 {len(res['t0']['failed'])}). `phrase_dictionary`(원장 문구 558)는 분석 대상 문구 자체라 등록하지 않았다(등록하면 문구 하나가 명사 하나가 된다). 사건 사전의 origin=ledger 262 는 7차 실버 사전에 이미 없다(다시 세는 노드).")
    a(f"- **분석 후보 고르기** — Kiwi 분석 후보 {res['kiwi']['top_n']} 개 중 「어절 안 이상 꼴」이 없는 가장 높은 점수의 후보를 쓴다. 이상 꼴 = 한국어 띄어쓰기상 한 어절 안에 올 수 없는 배열(A1 관형사·수사·대명사·감탄사가 다른 내용 형태소와 한 어절 · A2 명사·어근 바로 뒤 VV/VA/VX · A3 조사 뒤 어미·Z_ 꼴 · A4 EC/ETM/EF 뒤 같은 어절의 명사 · A5 받침 자모로 시작하는 두 글자 이상 어미 · A6 조사 뒤 같은 어절의 내용 형태소 · A7 일반 부사가 명사와 한 어절). 1위 후보가 「건조감 → 건조/NNG + 가/VV + ᆷ/EF」「이물감 → 이/MM + 물감」「온감 → 오/NR + 이/VCP + ᆫ감/EF」처럼 ~감 낱말을 동사로 쪼개는 일이 많아서 넣었다. 이상 꼴 없는 후보가 없으면 그 어절은 T1 적용 불가(애매).")
    a("- **T3** — 괄호 안(조사·어미 뺀 형태소)에서 기호·라틴·숫자(SL·SN·SW·SP·SS·SE·SO·SH) 형태소가 과반이면 그 괄호의 토막은 사건 후보 아님(R15 속성/문헌 후보). 정확히 절반 = 「위주」인지 애매 → 적용 안 함. 7차가 괄호 안에서 잡은 사전 사건(예: PIH)은 지우지 않았다(후보가 아니라 사전 일치).")
    a("- **T4** — 같은 묶음 안 첫 「--」「—」「:」 뒤 멤버의 토막은 서술(사건 후보 아님). 그 뒤에 있는 7차 사전 일치는 지우지 않았다(기록만 §4.1).")
    a("- **T2** — 멤버(7차 구분자로 가른 단위)에 용언(VV·VA·VX·XSV·XSA)+어미(EC·ETM·ETN)가 있으면 문장꼴. R1 목록에 있는 관형형 낱말(심한·경미한·과도한·미세한·광범위한·드문 …)은 판정에서 뺐다(R1 이 수식어로 떼는 말). (a) 사건 없는 토막 안에 사전 사건 NNG 가 있으면 그 사전 사건으로 붙이고, 멤버에 사전 사건이 있으면 사건 없는 토막은 서술 · (b) 멤버에 사전 사건이 없으면 「문장꼴 — 사용자」(노드 아님). 서술 분류(타임라인/동의서 고지/설명문)는 낱말 목록 일치로 낸 **제안**이고 적용하지 않았다. 「문구」를 멤버 단위로 읽었다 — 문구 단위로 읽으면 문장꼴 멤버 옆의 명사 멤버까지 서술이 되는데, 그 자리는 적용하지 않고 「T2 범위」 애매로 표시했다.")
    a("- **T1** — 핵심어 = 명사(NNG·NNP · SL 은 등록 사전 값일 때만). 같은 어절 안 XSN(뒤)·XPN(앞)은 그 명사에 붙이고, XR 은 같은 어절 안 뒤에 XSN·명사가 오면 명사 꼴로 본다(「민감성」= 민감/XR+성/XSN · 접사 단독은 핵심어가 아님). 의존명사(NNB)·관형사·부사·수사·숫자·기호·조사·어미·용언은 버린다. 같은 어절이 R1·R2 말과 똑같으면 그 어절은 통째 한 단위(분석기가 「중등도」를 중등/NNG+도/JX 로 나눠도 1차처럼 R1 말로 본다). 이름 = 명사 단위를 같은 어절은 붙여, 다른 어절은 띄워 이은 것.")
    a("  - T1 이 애매해 **적용하지 않은** 자리(노드도 세우지 않고 「애매 — 사용자(노드 아님)」로 셈): ① 용언+-ㅁ/-음 꼴을 Kiwi 가 EF(종결 어미)로 본 토막(「따가움」「눈꺼풀 처짐」 — T2 어미 목록 밖이고 명사도 아님) ② 명사가 하나도 없는 토막 ③ 이상 꼴 없는 후보가 없는 어절 ④ 명사 단위가 있는 어절 안에서 명사 아닌 형태소(NNB 밖)를 버려야 하는 자리(「색소침착과다 → 색소침착/과/이(VCP)/다」) ⑤ 문맥 안에선 명사인데 이름 하나로 다시 분석하면 용언+어미가 되는 이름(「눈부심」).")
    a("- **R2·R1** — 1차 정의 그대로를 명사 단위열에 적용: R2 = 단위(이어 붙인 형태소 포함 · 띄어쓰기 없이 붙은 말도)가 R2 말이고 뒤에 명사가 더 있으면 부위로 뗌 · R1 = 맨 앞·맨 뒤 단위가 R1 말이면 뗌(명사가 하나 이상 남을 때만 · 「이상」 뺌). 사전 사건 NNG 에 R1·R2 밖 명사가 붙은 이름(「색소침착감소」「화학화상」)은 규칙 밖이라 노드로 두고 애매 표시.")
    a("- **R3·R4·S** — 1차 코드와 같은 정의(단독 출현 = 핵심어 말고 남는 내용이 없는 자리 · T1 이 버린 내용 형태소도 「남는 내용」으로 셈). R4 의 괄호 앞·안 키는 원문 그대로 또는 T1 이름. S = 7차 ⑦ strong 중 suffix_감·증·형성 23 쌍(두 끝이 2차 뒤에도 노드·사전일 때만).")
    a("- **자리 판정 순서 T3 → T4 → T2 → T1 → R2 → R1 → R3 → R4 → S** · 겹치면 먼저 적용된 규칙에 센다. 7차 노드 하나가 여러 자리에 서므로, 7차 이름이 2차에 하나라도 그대로 서면 「남음」, 아니면 자리들의 결과 중 「닫힘」(다른 이름·사전 사건·T3·T4·T2(a))이 하나라도 있으면 그중 가장 앞 규칙으로 닫힘, 없으면 T2(b) → 「문장꼴 — 사용자」, 그것도 없으면 「애매 — 사용자(노드 아님)」.")
    a("")
    a("## 1. 자리 수 — 묶음 × 규칙 (1차와 나란히)")
    a("")
    head = ["묶음", "자리"] + COLS + ["닫힘 계", "문장꼴 — 사용자(T2b)", "애매 — 사용자(노드 아님)", "**2차 남음**", "남음 중 애매", "1차 남음(애매)"]
    rows = []
    tot = Counter()
    for b in ("ledger-nodes", "dup-strong", "seeds", "batch3"):
        t, t1 = T[b], T1[b]
        rows.append([BNAME[b], t["slots"]] + [t[c] for c in COLS] + [t["closed"], t["T2b_user"], t["amb_nonnode_user"], f"**{t['remaining']}**", t["remaining_ambiguous"], f"{t1['remaining']}({t1['ambiguous']})"])
        for c in ["slots"] + COLS + ["closed", "T2b_user", "amb_nonnode_user", "remaining", "remaining_ambiguous"]:
            tot[c] += t[c]
        tot["r1"] += t1["remaining"]
        tot["a1"] += t1["ambiguous"]
    rows.append(["**합계**", tot["slots"]] + [tot[c] for c in COLS] + [tot["closed"], tot["T2b_user"], tot["amb_nonnode_user"], f"**{tot['remaining']}**", tot["remaining_ambiguous"], f"{tot['r1']}({tot['a1']})"])
    a(tbl(head, rows))
    a("")
    a(f"T 열 중 T0 는 등록이라 자리를 닫지 않는다(효과는 T1·T2 에 들어 있다). 「excluded」(7차 결정 exclude) 열은 0 이라 뺐다. 1차 표의 R2·R1·R3·R4·S 열(새 노드 {T1['ledger-nodes']['R2']}·{T1['ledger-nodes']['R1']}·{T1['ledger-nodes']['R3']}·{T1['ledger-nodes']['R4']}·{T1['ledger-nodes']['S']})과 2차 열은 순서가 달라(T 가 먼저) 열끼리 직접 비교하지 않는다 — 비교는 「남음」으로.")
    ln = T["ledger-nodes"]
    a("")
    a(f"**새 사건 노드 260 → 2차 뒤 남는 자리 {ln['remaining']}**(1차 {T1['ledger-nodes']['remaining']}) · 그중 애매 {ln['remaining_ambiguous']} · 노드가 아니게 되어 사람이 볼 자리 = 문장꼴 {ln['T2b_user']} + 애매(노드 아님) {ln['amb_nonnode_user']}.")
    a(f"**2차가 새로 세운 노드 이름 {len(nd['new_names'])}**(1차 {res['first_new_names']} · §2.2) → 규칙 적용 뒤 사건 노드 = 사전 {nd['dict_events']} + 새 노드 묶음 **{nd['final_node_groups']}**(1차 {res['first_nodes']['node_groups_after_R4S']}) = {nd['dict_events'] + nd['final_node_groups']}.")
    sr = res["strong_recalc"]
    a(f"**⑦ strong 재계산**: 규칙 뒤 strong {sr['strong_after_rules']} 쌍(1차 {res['first_strong_recalc']}) · 그중 96 자리 밖 새 쌍 {sr['of_which_new']} · 남은 ⑦ 자리 {T['dup-strong']['remaining']} 중 재계산에도 strong 인 것 {sr['remaining_slots_in_recalc']}.")
    a("")
    a("씨앗 61 · 묶음3 미결 15 는 T·R 규칙의 대상(사건 노드 이름 · ⑦ 쌍)이 아니라 0 이다(1차와 같음).")
    a("")
    a(f"분해 수: 7차 노드 {nd['nodes_7th']} → T·R2·R1 뒤 {nd['nodes_after_T_R2_R1']} → R3 버림 {nd['r3_dropped']} → {nd['alive_after_R3']} → R4·S 묶음 {nd['final_node_groups']}. 토막 기록 {res['seglog_n']} 의 결과 종류: " + ", ".join(f"{k} {v}" for k, v in sorted(res["seglog_kinds"].items(), key=lambda x: -x[1])) + ".")
    a("")
    # ---- §2
    a("## 2. 남는 새 노드 전부")
    a("")
    pc = res["particle_check"]
    a(f"**조사·어미 검사**: 남는 새 노드 묶음 {pc['checked']} 개 이름을 하나씩 Kiwi 로 다시 분석해 조사(J*)·어미(E*) 형태소가 나온 이름 = **{len(pc['fail'])}**. (이름은 문맥 분석에서 명사 단위만으로 지었고, 이름 하나로 다시 분석해 어긋난 「{', '.join(x[0] for x in res['t0']['standalone_disagree']) or '없음'}」은 노드로 세우지 않고 애매 — 사용자로 뺐다.)")
    a("")
    rem = [r for r in res["node_rows"] if not r["rule"] and not r["bucket"]]
    a(f"### 2.1 7차 260 중 남는 자리 {len(rem)} (원장 횟수 = 7차 → 2차)")
    a("")
    rows = []
    for i, r in enumerate(rem, 1):
        nm = r["node"] if (r["name_after"] in (None, r["node"])) else f"{r['name_after']} (7차 「{r['node']}」)"
        rows.append([i, nm, f"{r['n']} → {r['n_after']}", r["example"], node_reason(r)])
    a(tbl(["#", "노드", "원장 횟수", "원문 예", "왜 남나"], rows))
    a("")
    a(f"### 2.2 2차가 새로 세운 노드 이름 {len(nd['new_names'])} (260 에 없던 이름)")
    a("")
    a(tbl(["노드", "원장 횟수", "어디서(7차 핵심어)", "⑦ strong", "애매"], [[x["node"], x["n"], x["from"], x["partners"] or "—", x["ambiguous"] or "—"] for x in nd["new_names"]]))
    a("")
    t2b = [r for r in res["node_rows"] if r["bucket"] == "T2b"]
    amb = [r for r in res["node_rows"] if r["bucket"] == "AMB"]
    a(f"### 2.3 노드가 아니게 된 자리 — 문장꼴 — 사용자 {len(t2b)}")
    a("")
    a(tbl(["노드(7차)", "원장 횟수", "원문 예", "자리별 결과"], [[r["node"], r["n"], r["example"], "; ".join(f"{k} ×{v}" for k, v in r["dest"].items())] for r in t2b]))
    a("")
    a(f"### 2.4 노드가 아니게 된 자리 — 애매 — 사용자(노드 아님) {len(amb)}")
    a("")
    a(tbl(["노드(7차)", "원장 횟수", "원문 예", "자리별 결과", "왜 애매"], [[r["node"], r["n"], r["example"], "; ".join(f"{k} ×{v}" for k, v in r["dest"].items()), " / ".join(r["ambiguous"])] for r in amb]))
    a("")
    closed = [r for r in res["node_rows"] if r["rule"]]
    a(f"### 2.5 규칙으로 닫힌 자리 {len(closed)}")
    a("")
    a(tbl(["노드(7차)", "원장 횟수", "규칙", "간 곳", "자리별 결과"], [[r["node"], r["n"], r["rule"], r["to"] or "—", "; ".join(f"{k} ×{v}" for k, v in r["dest"].items())] for r in closed]))
    a("")
    dr = res["dup_rows"]
    drem = [r for r in dr if not r["rule"] and not r["bucket"]]
    a(f"### 2.6 ⑦ strong — 남음 {len(drem)} · 닫힘 {sum(1 for r in dr if r['rule'])} · 한쪽이 노드 아님(사용자) {sum(1 for r in dr if r['bucket'])}")
    a("")
    a(tbl(["쌍(7차)", "규칙(7차)", "2차 결과", "2차 뒤", "애매"], [[f"{r['a']} ↔ {r['b']}", "/".join(r["rules"]), r["rule"] or r["bucket"] or "남음", f"{r['now'][0]} ↔ {r['now'][1]}" if r["now"] else "—", " / ".join(r["ambiguous"]) or "—"] for r in dr]))
    a("")
    a(f"규칙 뒤 새로 생긴 ⑦ strong {sr['of_which_new']}: " + (", ".join(f"{x['a']} ↔ {x['b']}({'/'.join(x['rules'])})" for x in sr["new_pairs"]) or "없음"))
    a("")
    a(f"R4 병기 쌍 {len(res['r4_pairs'])}: " + ", ".join(f"「{x['a']}」=「{x['b']}」" for x in res["r4_pairs"]) + f" · R4 애매 {len(res['r4_ambiguous'])}: " + ", ".join(f"「{x['a']}」=「{x['b']}」({x['kind']})" for x in res["r4_ambiguous"]))
    a(f"S 로 접힌 쌍 {len(res['s_pairs'])} · S 적용 못 함 {len(res['s_ambiguous'])}: " + (", ".join(f"{x['a']} ↔ {x['b']}(2차: {x['a_2nd']})" for x in res["s_ambiguous"]) or "없음"))
    a(f"R3 버린 토막 {len(res['r3_dropped'])}: " + (", ".join(x["node"] for x in res["r3_dropped"]) or "없음"))
    a("")
    # ---- §3
    t2 = res["t2_phrases"]
    a(f"## 3. T2 문장꼴 문구 전수 — 서로 다른 문구 {len(t2)} · 자리 {sum(x['n'] for x in t2)}")
    a("")
    sh = Counter(s for x in t2 for s in x.get("shape", []))
    a(f"(a) 사전 사건 있음 {sum(1 for x in t2 if x['t2'] == '(a)')} · (b) 없음 {sum(1 for x in t2 if x['t2'] == '(b)')} · 7차가 note·sentence 로 둔 문구(분해 안 함 · (a)/(b) 판정 밖) {sum(1 for x in t2 if x['t2'].startswith('—'))} 문구. 문장꼴 멤버 모양: " + ", ".join(f"{k} {v}" for k, v in sh.items()) + " (한 문구에 둘 다 있을 수 있음). 「명사로 끝남」은 「가벼운 출혈」「드물게 신경 손상」처럼 용언이 명사를 꾸미기만 하는 꼴 — 발주서 T2 정의(VV/VA+EC/ETM/ETN)에 그대로 들어 문장꼴로 셌다. 분류는 제안(타임라인: 숫자·시간·호전·사라짐 낱말 / 동의서 고지: 고지·주의·금기·반드시 … / 나머지 설명문).")
    a("")
    a(tbl(["#", "원문", "7차", "자리", "T2", "사전 사건(잡힌 것 포함)", "T2(a) 로 새로 잡음", "부위", "서술(용언 낱말)", "모양", "분류 제안", "locator(첫)"],
          [[i, x["text"], x["status7"], x["n"], x["t2"], x["dict_events"] or "—", x["captured"] or "—", x["site"] or "—", x["predicates"], x.get("shape"), x["class"], x["locators"][0]] for i, x in enumerate(t2, 1)]))
    a("")
    # ---- §4
    t3 = res["t3_parens"]
    a(f"## 4. T3 괄호 수치·약어 전수 — {len(t3)} (기호·라틴·숫자 과반 {sum(1 for x in t3 if x['kind'] == 'S')} · 정확히 절반(애매 · 적용 안 함) {sum(1 for x in t3 if x['kind'] == 'tie')})")
    a("")
    a(tbl(["#", "원문", "떼어낸 괄호 안", "판정", "기호 비율", "괄호 안 사전 사건(지우지 않음)", "자리", "제안 행선지"],
          [[i, x["text"], x["inner"], x["kind"], x["ratio"], x["dict_in_paren"] or "—", x["n"], x["proposal"]] for i, x in enumerate(t3, 1)]))
    a("")
    t4 = res["t4_dict_after"]
    a(f"### 4.1 T4 구분자 뒤에 Kiwi 가 사전 사건 NNG 로 본 말이 있는 자리 {len(t4)} (7차 사전 일치는 지우지 않음 · 기록만)")
    a("")
    a(tbl(["locator", "원문", "구분자 뒤", "사전 사건"], [[x[0], x[1], x[2], x[3]] for x in t4]))
    a("")
    # ---- §5
    fv = res["first_vs_second"]
    a(f"## 5. 1차 남음 {fv['first_remaining']} 중 2차에서 없어진 노드 {len(fv['vanished'])} — 어디로 갔나 (「사라짐 이유 없음」 {len(fv['no_reason'])})")
    a("")
    cc = Counter(v["class"].split("(")[0].split(" →")[0].strip() for v in fv["vanished"])
    a("분류별: " + ", ".join(f"{k} {v}" for k, v in cc.most_common()) + f" · 1차 남음 중 2차에도 남은 것 {len(fv['stayed'])}.")
    a("")
    a(tbl(["#", "노드(7차)", "원장 횟수", "1차 애매", "2차", "어디로", "자리별 결과"], [[i, v["node"], v["n"], "애매" if v["first_ambiguous"] else "—", v["rule2"], v["class"], "; ".join(f"{k} ×{n}" for k, n in v["dest"].items())] for i, v in enumerate(fv["vanished"], 1)]))
    a("")
    fc = fv["first_closed_now_remaining"]
    a(f"반대로 1차에서 닫혔는데 2차에서 남는 자리 {len(fc)}: " + ("; ".join(f"「{x['node']}」(1차 {x['rule1']} → {x['to1']} · 2차: {x['why2'] if isinstance(x['why2'], str) else ' / '.join(x['why2'])})" for x in fc) or "없음"))
    a("")
    # ---- §6
    t0 = res["t0"]
    a("## 6. T0 — 등록 · 분석기가 사전 값을 쪼갠 사례")
    a("")
    a(f"등록: 사전 {t0['n_dictionaries_used']} · (사전, 값) {t0['value_pairs']} · 서로 다른 값 {t0['registered_unique']} 등록 · 글자 없는 값 {len(t0['skipped_no_letters'])} 미등록(" + ", ".join(f"{d}:{v}" for d, v, _ in t0["skipped_no_letters"]) + f") · 실패 {len(t0['failed'])}.")
    a("")
    a(f"- 값 하나만 넣어 분석했을 때 형태소 하나로 안 나오는 값: **{len(t0['split_standalone'])}**")
    ctx = t0["split_in_context"]
    cv = Counter(v for v, _, _ in ctx)
    a(f"- 원장 부작용 축 문자열(3,109) 안에서 등록 값 글자 범위 안쪽에 형태소 경계가 생긴 자리: **{len(ctx)}**(값 {len(cv)}: " + ", ".join(f"「{k}」 {v}" for k, v in cv.most_common()) + ")")
    a("")
    a(tbl(["값", "원문", "그 범위의 형태소"], [[v, t, " ".join(f"{f}/{g}" for f, g in m)] for v, t, m in ctx]))
    a("")
    a(f"- R2 말과 겹치는 등록 값(R2 말로 시작·끝나는 더 긴 값) {len(t0['r2_conflicts'])} 개 — 그중 노드가 서는 토막에서 명사 단위로 나온 것 **{len(t0['r2_conflicts_hit_in_node_segments'])}**(겹침이 노드 셈에 닿은 자리 없음 · R2 우선을 적용할 자리 없음). 목록: " + ", ".join(x["value"] for x in t0["r2_conflicts"]))
    a(f"- R1·R2 말과 똑같은 등록 값 {len(t0['registered_equal_r_words'])}: " + ", ".join(f"{x['value']}({x['as']} · {'/'.join(x['dictionaries'])})" for x in t0["registered_equal_r_words"]) + " — 사전 값이면서 규칙 말이라 등록으로 통째 남고 R1·R2 가 뗀다.")
    a(f"- 문맥과 이름 하나의 분석이 갈린 2차 이름: " + (", ".join(f"「{n}」 → {' '.join(f'{f}/{g}' for f, g in m)}" for n, m in t0["standalone_disagree"]) or "없음"))
    a("")
    # ---- §7
    ph = res["phrases"]
    a(f"## 7. 부작용 문구 {ph['occurrences']:,} 중 사건 칸이 비는 수")
    a("")
    a(f"문구 판정: 7차 " + ", ".join(f"{k} {v}" for k, v in ph["by_status_7th"].items()) + " → 2차 " + ", ".join(f"{k} {v}" for k, v in ph["by_status"].items()) + " (note·sentence 판정은 7차 judge_phrase 그대로 · new/exact 는 「원장 노드 사건이 있나」라 노드가 줄면 exact 로 옮겨 간다). note·sentence 는 7차부터 단위를 세우지 않는 자리라 셈 밖.")
    a("")
    a(f"- exact·new 문구 중 2차 뒤 사건 칸이 빈 문구(문장꼴 (b) · 애매 — 사용자 제외): **{len(ph['empty_event_cell'])}**")
    a(f"- 따로: 문장꼴 (b) 때문에 빈 문구 **{len(ph['empty_t2b'])}** · 애매 — 사용자(노드 아님) 때문에 빈 문구 **{len(ph['empty_amb_user'])}** · complications 이름 65 중 빈 것 {len(ph['names_empty'])}")
    a("")
    if ph["empty_event_cell"]:
        a(tbl(["locator", "원문", "토막 결과"], ph["empty_event_cell"]))
        a("")
    a("<details><summary>문장꼴 (b) 로 빈 문구</summary>\n")
    a(tbl(["locator", "원문", "토막 결과"], ph["empty_t2b"]))
    a("\n</details>\n")
    a("<details><summary>애매 — 사용자(노드 아님)로 빈 문구</summary>\n")
    a(tbl(["locator", "원문", "토막 결과"], ph["empty_amb_user"]))
    a("\n</details>\n")
    # ---- §8
    a("## 8. 7차 불변 확인")
    a("")
    if verify:
        a(f"명령(`silver-v3/` · 시스템 `{verify.get('python3')}`): `{verify['cmd']}` → exit {verify['returncode']}")
        a("")
        a(f"- determinism key: out = `{verify['key_out']}` · baseline/manifest-7차.json = `{verify['key_baseline']}` → **{'같음' if verify['key_out'] == verify['key_baseline'] else '다름'}**")
        a(f"- out/ 트리 해시: 드라이런 전 `{verify['out_hash_before']}` · 분석 뒤 `{res['out_hash_after_analysis']}` · 빌드 뒤 `{verify['out_hash_after_build']}` → **{'전부 같음' if verify['out_hash_before'] == verify['out_hash_after_build'] == res['out_hash_after_analysis'] else '다름'}**")
        a("")
        out = (verify["stdout"] or "").strip().splitlines()
        a("```")
        a("\n".join(out[-40:]))
        if verify.get("stderr", "").strip():
            a("--- stderr ---")
            a("\n".join(verify["stderr"].strip().splitlines()[-20:]))
        a("```")
    else:
        a("(--verify 로 다시 돌리면 채워진다)")
    a("")
    # ---- §9
    a("## 9. ERD 영향 메모(사실만 · 판단은 사용자)")
    a("")
    a("ERD v3.2 는 토큰화를 규칙 문장으로 적어 두었다 — `resolve_rules.tokenize`(V3.2-1 · 검토 S-4): 사전 통째 일치가 먼저, 그다음 수식어·stopword → 문법 낱말(grammar_words) → **조사(particles)·용언 어미(verb_endings) 목록**에서 가장 긴 접미부터 떼되 어간이 사전 값·수식어·문법 낱말이거나 원장 독립 토큰(2자 이상)일 때만, relaxed_suffixes, predicate_endings(-는·-된·-운·-지고·-하게·-하므로·-되며) 꼴은 용언(predicate), 접속 조사(와·과·이나·나·와의)는 토막 경계, 각 목록 원소는 원장 locator 로 센다(§9.11 · locator 0 원소는 검산 FAIL). 이번 드라이런의 T1·T2 는 이 자리를 Kiwi 형태소 품사(J*·E*·XS*·VV/VA …)로 바꿔 판정한다 — 즉 「조사·어미 **목록**에서 뗀다」는 문장이 「형태소 분석기의 품사로 가른다」로 바뀌고, T2(문장꼴 판정 · (a)/(b))·T3(괄호 기호 비율)·T4(구분자 뒤 서술)는 v3.2 에 없는 규칙 문장이며, R1(「이상」 뺌)·R2 를 붙여 쓴 말에도 적용하는 것도 규칙 문장 변경이다. HANDOFF 원칙 8 은 ERD 재개 조건을 「개체·관계·규칙 문장 변경」으로 적었고, 원칙 6 은 「토큰화(조사·어미·~감·관형형)·표기 변형은 목록(출처)이고 떼어낸 조각은 보존」이라 적었다. 사실로 덧붙이면: 이 드라이런은 개체·관계를 바꾸지 않았고, 사전 값도 바꾸지 않았다(Kiwi 사용자 단어 등록은 실행 시점 설정이다). Kiwi 를 쓰면 판정이 분석기 판(kiwipiepy 0.24.1 · 내장 모델)과 후보 고르기 규칙(top_n · 이상 꼴 A1~A7)에 따라 달라진다 — 같은 낱말이 문맥에 따라 다른 품사가 되는 자리(§6 「눈부심」, 「따가움」 EF/ETN)가 이 판에서 실제로 나왔다.")
    a("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
