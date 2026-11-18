"""채점 — 지금 시스템(층 가르기) · 후보 뽑기 시안(소넷/하이쿠 · Jev 붙인 판)."""
import csv, json, os, sys, collections, statistics as S
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import SM, OUT, RUN as SP
WOUT=os.environ.get("INPUT_SPACE_OUT") or OUT  # 0.4(WORK-017 B-6 · 검수 R-3) — 쓰는 자리만 바꾼다(표 · 실행 기록 읽기는 그대로)
os.makedirs(WOUT,exist_ok=True)
def rd(p): return list(csv.DictReader(open(p,encoding="utf-8-sig")))
FIVE={"concern","site","modality","procedure","product"}
CS=collections.defaultdict(set)
for x in rd(SM+"/silver/concern_site.csv"): CS[x["concern_code"]].add(x["site_code"])
SITE_NAME={}
for x in rd(SM+"/gold/g_entry.csv"):
    if x["entity_table"]=="site": SITE_NAME.setdefault(x["text"],x["entity_code"])
GI=rd(SM+"/gold/g_indication.csv")
ROWS=collections.Counter(x["asked_concern_code"] for x in GI)
CONVS=[json.loads(l) for l in open(OUT+"/conversations.jsonl",encoding="utf-8")]
def load_now(path):
    out={}
    for l in open(path,encoding="utf-8"):
        r=json.loads(l)
        if r.get("phase")=="end": out[(r["conv_id"].split("-")[0],r["turn"])]=r
    return out
NOW=load_now(os.path.join(SP,os.environ.get("INPUT_SPACE_NOW","now-rows.jsonl")))
def key_of(c,t):
    """정답 키(되물음 답은 지금 시스템 실행의 앞 턴 ask 로 푼다) → dict 또는 None(채점 밖)."""
    k=t["key"]; groups=[[f"{a['table']}:{a['code']}" for a in g] for g in k["targets"]]
    na=None
    if k["ask_option"]:
        prev=NOW.get((c["conv"],t["n"]-1)); a=((prev or {}).get("consult") or {}).get("ask") or {}
        opts=a.get("options") or []
        if len(opts)>=k["ask_option"]:
            o=opts[k["ask_option"]-1]; groups=[[f"{o['table']}:{o['code']}"]]
        else: na="앞 턴에 앱이 되묻지 않았다(선택지 %d 개)"%len(opts)
    if k.get("ref") and not key_of.picker:  # 가리키는 말 — 앱 전체 실행에서는 앱이 실제로 보여 준 리스트가 표의 것과 같을 때만 채점
        prev_t=next((x for x in c["turns"] if x["n"]==t["n"]-1),None); want=[x["code"] for x in ((prev_t or {}).get("shown") or {}).get("list") or []]
        prow=NOW.get((c["conv"],t["n"]-1)) or {}
        got=[p["procedure_code"] for cc in (prow.get("list") or {}).get("concerns") or [] for m in [*(cc.get("modalities") or []),*(cc.get("descended") or [])] for p in m.get("procedures") or [] if p.get("procedure_code")]
        if k["ref"]["to"]=="list" and want and got[:len(want)]!=want: na=na or "앱이 보여 준 리스트가 표에 적어 둔 것과 다르다"
    return {"kinds":k.get("kinds"),"kinds_ok":k.get("kinds_ok") or [],"groups":groups,"extras":set() if "extras" in STRICT else set(k["extras_ok"]),"kind":k["kind"],"site_ok":set(x.split(":")[1] for x in k["site_filter"]),
            "site_req":k["site_required"],"withdraw":k["withdraw"],"na":na,"amb":t["ambiguous"],"material":k.get("material")}
STRICT=set(x for x in os.environ.get("INPUT_SPACE_STRICT","").split(",") if x)
# 0.4(검수 M-1) — 답 LLM 을 실제로 부른 대화의 둘째 턴부터는 키가 표의 가짜 앞 답 기준이라 D-14 분모에서 따로 묶는다(키는 안 고침 ·
# 사람 검수 E8-5 몫). 기본 = 표에서 `ref.to = answer` 턴이 든 대화(run_now --real-answer 와 같은 다섯) · 0.4 줄에만
REAL_ANSWER=set(x for x in os.environ.get("INPUT_SPACE_REAL_ANSWER","").split(",") if x) or {
    c["conv"] for c in CONVS if any((t["key"].get("ref") or {}).get("to")=="answer" for t in c["turns"])}  # prior = 앞 대상 다시 듦을 안 받음 · extras = extras_ok 를 끔(검수 R-3)
def kinds_score(key,got):
    """정보 종류(D-11) — 기대 종류를 전부 냈고, 낸 것이 기대 ∪ 함께 받는 종류 안이면 통과. 키가 없으면 None."""
    if not key.get("kinds"): return None
    if got is None: return None
    got=set(got); return set(key["kinds"])<=got and got<=set(key["kinds"])|set(key["kinds_ok"])
def kinds_has(key,got):
    """기대 종류를 전부 냈나(더 낸 것은 안 봄 — 앱의 「읽은 종류」 는 기본 묶음이 섞여 있어 이 값으로 본다)."""
    if not key.get("kinds") or got is None: return None
    return set(key["kinds"])<=set(got)
def prior_ok(key,prior):
    """앞 턴에 정답이었던 대상을 이번 턴에 다시 든 것은 군더더기로 안 센다(순수 잡담 턴 · 이번에 거둔 것은 빼고)."""
    if key["kind"]==["talk"] or "prior" in STRICT: return set()
    return set(prior)-{a for g in key["withdraw"] for a in g}
def prior_add(key,prior):
    for g in key["groups"]: prior.update(g)
    prior.update(key["extras"])
    for g in key["withdraw"]: prior.difference_update(g)
key_of.picker=False
def target_score(key,picks,prior=()):
    """picks = {"table:code"}(다섯 표만 센다) → hit 묶음 · 군더더기 · chosen."""
    picks={p for p in picks if p.split(":")[0] in FIVE}
    members={a for g in key["groups"] for a in g}
    hit=[any(a in picks for a in g) for g in key["groups"]]
    wd={a for g in key["withdraw"] for a in g}
    own={f"site:{x}" for p in picks if p.startswith("concern:") and (p in members or p in key["extras"] or p in prior) for x in CS.get(p.split(":")[1],())}
    bad=sorted(p for p in picks if p not in members and p not in key["extras"] and p not in prior and p not in own)
    bad_wd=sorted(p for p in picks if p in wd)
    return {"n_groups":len(hit),"hit":sum(hit),"missed":[g for g,h in zip(key["groups"],hit) if not h],"picks":sorted(picks),
            "bad":sorted(set(bad)|set(bad_wd)),"exact":all(hit) and not bad and not bad_wd,
            "chosen":sorted(p for p in picks if p in members)}
def site_score(key,sites,chosen):
    allowed=set(key["site_ok"])|{e.split(":")[1] for e in key["extras"] if e.startswith("site:")}
    for p in chosen:
        if p.startswith("concern:"): allowed|=CS.get(p.split(":")[1],set())
    stale=sorted(set(sites)-allowed)
    via=any(p.startswith("concern:") and CS.get(p.split(":")[1],set())&key["site_ok"] for p in chosen)
    missing=bool(key["site_req"] and not (set(sites)&key["site_ok"]) and not via)
    applies=bool(key["site_ok"]) or any(a.split(":")[0] in ("concern","site") for g in key["groups"] for a in g)
    return {"ok":(not stale and not missing) if applies else None,"stale":stale,"missing":missing}
def pct(a,b): return round(100*a/b,1) if b else None
def med(xs): return round(S.median(xs)) if xs else None
def p90(xs):
    xs=sorted(xs); return round(xs[min(len(xs)-1,int(0.9*len(xs)))]) if xs else None

# ───────── 지금 시스템 ─────────
def now_turn(c,t,cum):
    r=NOW.get((c["conv"],t["n"])); key=key_of(c,t)
    cons=r.get("consult") or {}; tr=r.get("trace") or {}
    v04=cons.get("understand") is not None; und=cons.get("understand") or {}; acc_=und.get("accepted") or {}
    tf=tr.get("front") or {}; ep=tr.get("entry_pick") or {}
    scored={x["id"]:x for x in tf.get("targets") or []}
    epc={x["id"]:x for x in ep.get("per_candidate") or []}
    targets={f"{x['table']}:{x['code']}":x for x in r.get("targets") or []}
    after=cons.get("after") or {}
    kind=(cons.get("turn_kind") or {}).get("kind")
    focus=after.get("focus")
    fs=[x for x in after.get("sites") or [] if x.get("state") in ("said","confirmed") and (x.get("source") or {}).get("pair_concern") in (None,focus)]
    filt=sorted({x["code"] for x in fs})
    if v04: filt=sorted(set((cons.get("site_filter") or {}).get("sites") or []))  # 0.4 — 조회에 실제로 건 거르개
    wd_now={f"{x['table']}:{x['code']}" for slot in ("concerns","sites","subjects") for x in after.get(slot) or [] if x.get("state")=="withdrawn"}
    if v04: wd_now|=set(acc_.get("withdraw") or [])
    ts=target_score(key,set(targets)-wd_now,prior_ok(key,cum["prior"])); prior_add(key,cum["prior"]); ss=site_score(key,filt,ts["chosen"])
    lst=r.get("list") or {}
    procs=sorted({p["procedure_code"] for cc in lst.get("concerns") or [] for m in [*(cc.get("modalities") or []),*(cc.get("descended") or [])] for p in m.get("procedures") or [] if p.get("procedure_code")})
    list_site=[cc.get("site") for cc in lst.get("concerns") or [] if cc.get("site")]
    st=r.get("sites"); dots=sorted({d["site_code"] for d in (st or {}).get("dots") or []}|{d["site_code"] for d in (st or {}).get("labels") or []}) if st is not None else None
    if dots is not None: cum["dots"]=dots
    # 객체 반영
    in_obj=set()
    for slot in ("concerns","sites","subjects"):
        for x in after.get(slot) or []:
            if x.get("state") in ("said","confirmed"): in_obj.add(f"{x['table']}:{x['code']}")
    wd_obj={f"{x['table']}:{x['code']}" for slot in ("concerns","sites","subjects") for x in after.get(slot) or [] if x.get("state")=="withdrawn"}
    obj_missing=[p for p in ts["chosen"] if p not in in_obj]
    chosen_con=[p.split(":")[1] for p in ts["chosen"] if p.startswith("concern:")]
    focus_bad=bool(chosen_con and focus not in chosen_con)
    wd_missed=[g for g in key["withdraw"] if not any(a in wd_obj or a not in in_obj for a in g)]
    # 점 — 말한 고민(고른 것)의 직접 부위 누적
    for cc in chosen_con: cum["exp"]|=CS.get(cc,set()); cum["con"].add(cc)
    for g in key["withdraw"]:
        pass
    exp=sorted(cum["exp"]); got=cum.get("dots") or []
    dots_extra=sorted(set(got)-set(exp)); dots_miss=sorted(set(exp)-set(got))
    checks={"target":ts["exact"],"kind":kind in key["kind"],"site":ss["ok"],"obj":not obj_missing and not focus_bad and not wd_missed,
            "dots":(not dots_extra and not dots_miss) if (chosen_con and cum["all_hit"]) else None,
            "list":None}
    checks["options"]=None; linked=[]
    site_only=[p.split(":")[1] for p in ts["chosen"] if p.startswith("site:")]
    if site_only and not chosen_con and not focus and ts["exact"] and "부위만" in t["tags"]["intent"]:
        linked=[c_ for c_,ss_ in CS.items() if set(site_only)&ss_]
        if linked: checks["options"]=bool((cons.get("ask") or {}).get("options"))
    if chosen_con and r.get("list") is not None and focus in chosen_con:
        checks["list"]=bool(procs)
    kgot=(acc_.get("kinds") if acc_ else ([] if und.get("error") else None)) if v04 else r.get("kinds")
    checks["kinds"]=kinds_score(key,kgot); checks["kinds_has"]=kinds_has(key,kgot)
    # 0.4 E8-6b — 재료 · 깊이(key.material 이 있는 턴만)
    for ln in (r.get("material") or {}).get("new_lines") or []:
        if ln.get("gid"): cum.setdefault("lines",{})[ln["n"]]=ln["gid"]
    checks["mat_rows"]=checks["mat_b"]=checks["mat_c"]=None; mat_got=None
    km=key.get("material")
    if v04 and km is not None:
        mat_got={x["gid"] for x in (r.get("material") or {}).get("new_lines") or [] if x.get("gid")}|{cum.get("lines",{}).get(n) for n in (r.get("material") or {}).get("seen_lines") or []}
        mat_got.discard(None)
        checks["mat_rows"]=all(any(g in mat_got for g in grp) for grp in km.get("rows") or [])
        dec=((r.get("depth") or {}).get("decisions")) or {}
        gate={k_ for k_,v_ in dec.items() if v_=="gate_forced"}
        checks["mat_b"]=gate<=set(km.get("depth") or [])
        checks["mat_c"]=all(dec.get(n_)=="gate_forced" for n_ in km.get("depth") or [] if n_ in dec)
    checks["site_effect"]=None
    if key["site_req"] and ts["exact"] and list_site:
        checks["site_effect"]=not (list_site[0].get("applied")=="prefer" and not list_site[0].get("prefer_rows"))
    # 층
    layer=None; why=""
    def cand_layer(group):
        ids=[a for a in group if a in scored or a in epc]
        if not ids: return "후보","정답이 후보에 없음(resolve · 든 후보 · 입구 고르기 어디에도)"
        for a in ids:
            x=scored.get(a) or epc.get(a)
            if x.get("decision")=="overlap": return "앱 규칙",f"겹침 규칙이 뺌({a} noul {x.get('noul')})"
            if (x.get("noul") or 0)>=0.7 and x.get("decision") in ("dropped",): return "앱 규칙",f"noul {x.get('noul')} 인데 규칙이 뺌({a})"
        a=ids[0]; x=scored.get(a) or epc.get(a)
        return "Jev",f"후보에 있는데 점수로 떨어짐({a} noul {x.get('noul')} · {x.get('decision')})"
    def extra_layer(p):
        x=scored.get(p) or epc.get(p) or {}; by=targets.get(p,{}).get("by")
        if by in ("named","uncertain_kept"): return "앱 규칙",f"점수 {x.get('noul')} 인데 규칙(TG{'3' if by=='named' else '2'})으로 대상({p})"
        return "Jev",f"엉뚱한 것을 yes({p} noul {x.get('noul')} · {by})"
    if not checks["target"]:
        if ts["missed"]:
            if kind=="talk" and "talk" not in key["kind"]: layer,why="Jev","턴 종류를 talk 로 판정 → 걷기를 버림"
            else: layer,why=cand_layer(ts["missed"][0])
        else: layer,why=extra_layer(ts["bad"][0])
    elif not checks["kind"]:
        rule=(cons.get("turn_kind") or {}).get("rule"); nl=(cons.get("turn_kind") or {}).get("nouls") or {}
        order=rule=="TK5-1" and any((nl.get(k_) or 0)>=0.7 and (nl.get(k_) or 0)>(nl.get("new") or 0) for k_ in key["kind"])
        layer,why=("앱 규칙" if rule in ("TK2","TT6","off") or order else "Jev"),("TK5 순서(new 먼저) — " if order else "")+f"턴 종류 {kind}(기대 {'/'.join(key['kind'])} · {rule} · {(cons.get('turn_kind') or {}).get('nouls')})"
    elif checks["site"] is False:
        if ss["stale"]: layer,why="앱 규칙",f"앞 턴 부위가 거르개에 남음({','.join(ss['stale'])})"
        else:
            ids=[f"site:{s}" for s in key["site_ok"]]
            if not any(i in scored or i in epc for i in ids): layer,why="후보","이번 턴 부위가 후보에 없음"
            else: layer,why="앱 규칙","이번 턴 부위가 거르개에 안 실림"
    elif not checks["obj"]:
        if wd_missed:
            items={f"{x['table']}:{x['code']}":x for x in cons.get("retract") or []}
            a=next((a for g in wd_missed for a in g if a in items),None)
            layer,why=("Jev",f"거둠 noul {items[a]['noul']}({a})") if a else ("앱 규칙","거둘 항목이 객체에 없어 묻지 않음")
        elif obj_missing:
            bys={targets.get(p_,{}).get("by") for p_ in obj_missing}
            if bys<={"uncertain_kept"}: layer,why="Jev",f"이름을 말했는데 점수가 사이 값 → 추정(guess)으로만 듦({','.join(obj_missing)})"
            elif "noul" in bys: layer,why="앱 규칙",f"입구 고르기로 확정한 대상이 객체에 안 듦({','.join(obj_missing)})"
            else: layer,why="앱 규칙",f"대상인데 객체에 안 듦({','.join(obj_missing)} · {bys})"
        else: layer,why="앱 규칙",f"focus {focus} ≠ 이번 턴 고민 {','.join(chosen_con)}"
    elif checks["dots"] is False:
        layer,why="앱 규칙",("말하지 않은 부위에 점("+",".join(dots_extra)+")" if dots_extra else "말한 고민 부위 점 빠짐("+",".join(dots_miss)+")")
    elif checks["options"] is False:
        qt=[q.get("total") for q in cons.get("queries") or [] if q.get("rule")=="QY7"]
        if qt and not any(qt): layer,why="데이터","부위만 말함 → 되물을 고민 선택지 0 — facets(site, indication) total 0(concern_site 에는 묶인 고민 있음: "+",".join(sorted(linked))+")"
        else: layer,why="앱 규칙",f"부위만 말함 → 조회는 {qt} 행인데 되묻지 않음(ask_why {cons.get('ask_why')})"
    elif checks["site_effect"] is False:
        layer,why="데이터",f"부위 거르개가 0 행에 걸림 → 우선 표시로 풀림({list_site[0].get('name')}) — 말한 부위가 그 고민의 행 · concern_site 에 닿지 않음"
    elif checks["list"] is False:
        z=[cc for cc in chosen_con if not ROWS.get(cc)]
        layer,why=("데이터",f"고민 행 0({','.join(z)})") if z else ("데이터","행은 있는데 시술로 안 닿음")
    # 데이터 층 — 부위 글자 ≠ 고민 부위(거르개가 우선 표시로 풀림)
    data_note=[]
    for s in list_site:
        if s.get("applied")=="prefer" and key["site_ok"]: data_note.append(f"부위 거르개가 우선 표시로 풀림({s.get('name')} · prefer_rows {s.get('prefer_rows')})")
    for cc in chosen_con:
        if not ROWS.get(cc): data_note.append(f"{cc} g_indication 행 0")
    if not checks["target"]: cum["all_hit"]=cum["all_hit"] and not [g for g in ts["missed"] if any(a.startswith("concern:") for a in g)]
    layer04=None
    if v04 and layer:  # 0.4 층(이해 호출 · 검증 · 객체 · 조회 · 데이터) — checks 로만 가른다
        dropped={f"{x.get('table')}:{x.get('code')}" for x in und.get("dropped") or []}
        if und.get("error"): layer04="이해 호출(오류 "+str(und["error"].get("kind"))+")"
        elif not checks["target"]: layer04="검증" if any(a in dropped for g in ts["missed"] for a in g) else "이해 호출"
        elif not checks["kind"]: layer04="검증" if (cons.get("turn_kind") or {}).get("from") not in (None,"understand") else "이해 호출"
        elif checks["site"] is False: layer04="객체(부위 잇기)" if (cons.get("site_filter") or {}).get("carried") else "이해 호출"
        elif not checks["obj"]: layer04="객체"
        elif layer=="데이터": layer04="데이터"
        else: layer04="조회"
    return {"conv":c["conv"],"turn":t["n"],"text":t["text"],"intent":t["tags"]["intent"],"form":t["tags"]["form"],"data":t["tags"]["data"],
            "ambiguous":bool(key["amb"]),"na":key["na"],"answer_ref":bool(v04 and c["conv"] in REAL_ANSWER and t["n"]>=2),
            "resolve":[x["id"] for x in (tr.get("entry") or {}).get("resolve_candidates") or []],
            "jev":[[x["id"],x.get("noul"),x.get("decision")] for x in tf.get("targets") or []],
            "entry_pick":({"result":ep.get("result"),"requests":ep.get("requests"),"yes":[x["id"] for x in ep.get("per_candidate") or [] if x["decision"]=="confirmed"]} if ep and not ep.get("skipped") else None),
            "targets":[[k,v.get("by")] for k,v in targets.items()],"kinds":r.get("kinds"),"turn_kind":kind,"turn_kind_nouls":(cons.get("turn_kind") or {}).get("nouls"),
            "diff":[[d["op"],d["slot"],d.get("code"),d.get("to")] for d in cons.get("diff") or []],
            "queries":[[q["rule"],q["tool"],q["request"],q.get("total")] for q in cons.get("queries") or []],"ask":({"slot":cons["ask"]["slot"],"options":[o.get("code") for o in cons["ask"].get("options") or []]} if cons.get("ask") else None),"ask_why":cons.get("ask_why"),"site_filter":filt,"focus":focus,
            "list_procedures":procs,"list_site":list_site,"dots":dots,"dots_now":got,"dots_expected":exp,
            "end_state":r.get("end_state"),"ms":(r.get("timing") or {}).get("total_ms"),"jev_ms":((r.get("timing") or {}).get("parts") or {}).get("jev_ms"),
            "jev_requests":cons.get("jev_requests"),
            "score":{"groups":ts["n_groups"],"hit":ts["hit"],"picks":len(ts["picks"]),"bad":ts["bad"],"missed":ts["missed"]},
            "checks":checks,"layer":layer,"why":why,"data_note":data_note,
            **({"v04":{"layer":layer04,"understand_ms":und.get("ms"),"api_ms":und.get("api_ms"),"thinking":(und.get("usage") or {}).get("thinking_tokens"),
                       "error":und.get("error"),"dropped":und.get("dropped"),"accepted":acc_,"site_filter":cons.get("site_filter"),
                       "turn_kind_from":(cons.get("turn_kind") or {}).get("from"),"material_got":sorted(mat_got) if mat_got is not None else None,
                       "depth":r.get("depth"),"ft5":r.get("tokens_over")}} if v04 else {})}
now_rows=[]
for c in CONVS:
    cum={"exp":set(),"con":set(),"all_hit":True,"prior":set()}
    for t in c["turns"]:
        if (c["conv"],t["n"]) in NOW: now_rows.append(now_turn(c,t,cum))
with open(WOUT+"/now-turns.jsonl","w",encoding="utf-8") as f:
    for r in now_rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")

# ───────── 후보 뽑기 시안 ─────────
def load_pick(path):
    out={}
    if os.path.exists(path):
        for l in open(path,encoding="utf-8"):
            r=json.loads(l); out[(r["conv"],r["turn"])]=r
    return out
def pick_rows(pk,mode="raw"):
    rows=[]; key_of.picker=True
    for c in CONVS:
        prior=set()
        for t in c["turns"]:
            r=pk.get((c["conv"],t["n"]))
            key=key_of(c,t)
            if not r:
                prior_add(key,prior); continue
            picks={f"{a}:{b}" for a,b in r["picks"]}|{f"site:{x}" for x in r["sites"]}
            if mode=="jev": picks={p for p in picks if (r.get("jev") or {}).get(p,0)>=0.7}
            ts=target_score(key,picks,prior_ok(key,prior)); prior_add(key,prior); ss=site_score(key,r["sites"],ts["chosen"])
            wd_ok=all(any(a in r["withdraw"] for a in g) for g in key["withdraw"])
            rows.append({"conv":c["conv"],"turn":t["n"],"text":t["text"],"intent":t["tags"]["intent"],"form":t["tags"]["form"],
                         "ambiguous":bool(key["amb"]),"na":key["na"],"has_wd":bool(key["withdraw"]),"picks":ts["picks"],"kind":r["kind"],"sites":r["sites"],"withdraw":r["withdraw"],
                         "invented":len(r["invented"])+len(r.get("bad_sites") or []),"error":r["error"],
                         "ms":(r["ms"] or 0)+(r.get("jev_ms") or 0 if mode=="jev" else 0),"usage":r["usage"],
                         "score":{"groups":ts["n_groups"],"hit":ts["hit"],"picks":len(ts["picks"]),"bad":ts["bad"],"missed":ts["missed"]},
                         "checks":{"target":ts["exact"],"kind":r["kind"] in key["kind"],"site":ss["ok"],"withdraw":wd_ok,"kinds":kinds_score(key,r.get("kinds")),"kinds_has":kinds_has(key,r.get("kinds"))}})
    return rows
def summarize(rows,keep=None):
    rs=[r for r in rows if not r["ambiguous"] and not r["na"] and not r.get("answer_ref") and (keep is None or (r["conv"],r["turn"]) in keep)]
    g=sum(r["score"]["groups"] for r in rs); h=sum(r["score"]["hit"] for r in rs)
    pk=sum(r["score"]["picks"] for r in rs); bad=sum(len(r["score"]["bad"]) for r in rs)
    ms=[r["ms"] for r in rs if r.get("ms")]
    p3=[r for r in rs if r["checks"]["target"] and r["checks"]["kind"] and r["checks"]["site"] is not False]
    byc=collections.defaultdict(list)
    for r in rs: byc[r["conv"]].append(r in p3)
    kn=[r for r in rs if r["checks"].get("kinds") is not None]
    return {"pass3":len(p3),"pass3_pct":pct(len(p3),len(rs)),"conv_pass3":sum(all(v) for v in byc.values()),"convs":len(byc),
            "kinds":pct(sum(1 for r in kn if r["checks"]["kinds"]),len(kn)),"kinds_has":pct(sum(1 for r in kn if r["checks"].get("kinds_has")),len(kn)),"kinds_n":len(kn),
            "turns":len(rs),"recall":pct(h,g),"precision":pct(pk-bad,pk),"target_exact":pct(sum(r["checks"]["target"] for r in rs),len(rs)),
            "kind":pct(sum(r["checks"]["kind"] for r in rs),len(rs)),"site":pct(sum(1 for r in rs if r["checks"]["site"]),sum(1 for r in rs if r["checks"]["site"] is not None)),"site_n":sum(1 for r in rs if r["checks"]["site"] is not None),
            "ms_median":med(ms),"ms_p90":p90(ms)}
def by_tag(rows,tagkey,keep=None):
    out=collections.OrderedDict()
    tags=sorted({x for r in rows for x in (r[tagkey] if isinstance(r[tagkey],list) else [r[tagkey]])})
    for tg in tags:
        out[tg]=summarize([r for r in rows if tg in (r[tagkey] if isinstance(r[tagkey],list) else [r[tagkey]])],keep)
    return out
res={"now":{"all":summarize(now_rows)}}
runs={"sonnet+별칭":"pick-sonnet-on.jsonl","sonnet":"pick-sonnet-off.jsonl","haiku+별칭":"pick-haiku-on.jsonl","haiku":"pick-haiku-off.jsonl","Jev fan-out+별칭":"fan-on.jsonl","Jev fan-out":"fan-off.jsonl"}
PK={}
for name,fn in runs.items():
    pk=load_pick(os.path.join(SP,fn))
    if pk: PK[name]=pk
sample=None
if PK:
    sample=set.intersection(*[set(v) for v in PK.values()])
    res["sample_turns"]=len(sample)
    res["now"]["sample"]=summarize(now_rows,sample)
for name,pk in PK.items():
    rows=pick_rows(pk); res[name]={"all":summarize(rows),"sample":summarize(rows,sample),"by_form":by_tag(rows,"form",sample),"by_intent":by_tag(rows,"intent",sample)}
    inv=sum(r["invented"] for r in rows); tot=sum(r["score"]["picks"] for r in rows)+inv
    res[name]["invented"]={"n":inv,"of":tot,"pct":pct(inv,tot)}
    res[name]["errors"]=sum(1 for r in rows if r["error"])
    if name.startswith("Jev"):
        raw=list(pk.values())
        res[name]["tokens"]={"input_total_median":med([sum(u_["input_tokens"] for u_ in x["usage"]) for x in raw if x["usage"]]),"output_median":med([sum(u_["output_tokens"] for u_ in x["usage"]) for x in raw if x["usage"]]),"requests_per_turn":med([x["requests"] for x in raw])}
        res[name]["invented"]={"n":0,"of":sum(r["score"]["picks"] for r in rows),"pct":0.0}; res[name]["errors"]=sum(1 for r in rows if r["error"])
        res[name]["n_yes_median"]=med([x["n_yes"] for x in raw]); res[name]["n_between_median"]=med([x["n_between"] for x in raw])
        with open(WOUT+f"/{runs[name][:-6]}-turns.jsonl","w",encoding="utf-8") as f:
            for r in rows: f.write(json.dumps({**{k:v for k,v in r.items() if k!="usage"},"kind_nouls":pk[(r["conv"],r["turn"])]["kind_nouls"],"top":pk[(r["conv"],r["turn"])]["top"],"requests":pk[(r["conv"],r["turn"])]["requests"]},ensure_ascii=False)+"\n")
        continue
    u=[r["usage"] for r in rows if r["usage"]]
    res[name]["tokens"]={"input_total_median":med([x.get("input_tokens",0)+x.get("cache_creation_input_tokens",0)+x.get("cache_read_input_tokens",0) for x in u]),
                        "output_median":med([x.get("output_tokens",0) for x in u]),"output_p90":p90([x.get("output_tokens",0) for x in u]),
                        "cache_read_calls":sum(1 for x in u if x.get("cache_read_input_tokens",0)>0),"calls":len(u),
                        "cache_read_median":med([x.get("cache_read_input_tokens",0) for x in u if x.get("cache_read_input_tokens",0)>0])}
    t1=[r["ms"] for r in rows if r["turn"]==1 and r["ms"]]; t2=[r["ms"] for r in rows if r["turn"]>1 and r["ms"]]
    cold=[r["ms"] for r in rows if r["usage"] and not r["usage"].get("cache_read_input_tokens") and r["ms"]]
    warm=[r["ms"] for r in rows if r["usage"] and r["usage"].get("cache_read_input_tokens") and r["ms"]]
    res[name]["latency"]={"turn1_median":med(t1),"turn2plus_median":med(t2),"cache_miss_median":med(cold),"cache_miss_n":len(cold),"cache_hit_median":med(warm),"cache_hit_n":len(warm)}
    wdt=[r for r in rows if r.get("has_wd")]; res[name]["withdraw"]={"ok":sum(1 for r in wdt if r["checks"]["withdraw"]),"n":len(wdt)}
    with open(WOUT+f"/pick-{runs[name][5:-6]}-turns.jsonl","w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps({k:v for k,v in r.items()},ensure_ascii=False)+"\n")
    if name=="sonnet+별칭" and any("jev" in v for v in pk.values()):
        jr=pick_rows(pk,"jev"); res["sonnet+별칭+Jev"]={"all":summarize(jr),"sample":summarize(jr,sample),"by_form":by_tag(jr,"form",sample),"by_intent":by_tag(jr,"intent",sample)}
        res["sonnet+별칭+Jev"]["jev_ms_median"]=med([v.get("jev_ms") for v in pk.values() if v.get("jev_ms")])
        with open(WOUT+"/pick-sonnet-on-jev-turns.jsonl","w",encoding="utf-8") as f:
            for r in jr: f.write(json.dumps(r,ensure_ascii=False)+"\n")
res["now"]["by_form"]=by_tag(now_rows,"form"); res["now"]["by_intent"]=by_tag(now_rows,"intent")
if sample: res["now"]["by_form_sample"]=by_tag(now_rows,"form",sample); res["now"]["by_intent_sample"]=by_tag(now_rows,"intent",sample)
# 지금 시스템 — 꼴 × 층
scored=[r for r in now_rows if not r["ambiguous"] and not r["na"] and not r.get("answer_ref")]
ar=[r for r in now_rows if r.get("answer_ref") and not r["ambiguous"] and not r["na"]]
if ar:  # 검수 M-1 — 따로 묶은 줄(D-14 분모 밖) · 장부 근거 = 그 대화 앞 턴의 실물 답 앞머리
    def _p3(r): return bool(r["checks"]["target"] and r["checks"]["kind"] and r["checks"]["site"] is not False)
    res["now"]["answer_ref"]={"n":len(ar),"pass8":sum(1 for r in ar if not r["layer"]),"pass3":sum(1 for r in ar if _p3(r)),
        "convs":sorted(REAL_ANSWER),"rule":"답 LLM 실물 대화의 둘째 턴부터(앞 턴 답 ≠ 표의 가짜 앞 답)",
        "turns":[{"conv":r["conv"],"turn":r["turn"],"text":r["text"],"pass8":not r["layer"],"pass3":_p3(r),
                  "first_fail":next((k for k in ("target","kind","site","obj","dots","options","site_effect","list") if r["checks"][k] is False),None),
                  "picked":[x["code"] for x in ((r.get("v04") or {}).get("accepted") or {}).get("targets") or []],
                  "missed":r["score"]["missed"],"bad":r["score"]["bad"],
                  "prev_answer":(NOW.get((r["conv"],r["turn"]-1)) or {}).get("answer","")[:160]} for r in ar]}
res["now"]["counts"]={"turns":len(now_rows),"scored":len(scored),"answer_ref":len(ar),"ambiguous":sum(r["ambiguous"] for r in now_rows),"na":sum(1 for r in now_rows if r["na"] and not r["ambiguous"]),
    "pass":sum(1 for r in scored if not r["layer"]),"pass8_pct":pct(sum(1 for r in scored if not r["layer"]),len(scored)),"fail":sum(1 for r in scored if r["layer"]),
    "layer":dict(collections.Counter(r["layer"] for r in scored if r["layer"])),
    "check_fail":{k:sum(1 for r in scored if r["checks"][k] is False) for k in ("target","kind","site","obj","dots","options","site_effect","list")},
    "check_n":{k:sum(1 for r in scored if r["checks"][k] is not None) for k in ("target","kind","site","obj","dots","options","site_effect","list")},
    "entry_pick_turns":sum(1 for r in now_rows if r["entry_pick"]),"entry_pick_ms_median":med([r["ms"] for r in now_rows if r["entry_pick"]]),
    "ms_median_no_entry_pick":med([r["ms"] for r in now_rows if not r["entry_pick"] and r["ms"]])}
def layer_table(tagkey):
    tags=sorted({x for r in scored for x in (r[tagkey] if isinstance(r[tagkey],list) else [r[tagkey]])})
    out=[]
    for tg in tags:
        rs=[r for r in scored if tg in (r[tagkey] if isinstance(r[tagkey],list) else [r[tagkey]])]
        cnt=collections.Counter(r["layer"] for r in rs if r["layer"])
        out.append({"tag":tg,"turns":len(rs),"pass":sum(1 for r in rs if not r["layer"]),**{k:cnt.get(k,0) for k in ("후보","Jev","앱 규칙","데이터")}})
    return out
res["now"]["layer_by_intent"]=layer_table("intent"); res["now"]["layer_by_form"]=layer_table("form"); res["now"]["layer_by_data"]=layer_table("data")
v4=[r for r in scored if r.get("v04")]
if v4:  # 0.4 E8-6b · 층 · 이해 호출 지연(thinking 있음 / 없음)
    def _k(k_): xs=[r["checks"][k_] for r in v4 if r["checks"].get(k_) is not None]; return {"pass":sum(xs),"n":len(xs),"pct":pct(sum(xs),len(xs))}
    um=[r["v04"]["understand_ms"] for r in v4 if r["v04"]["understand_ms"] and not r["v04"]["error"]]
    th=[r for r in v4 if (r["v04"]["thinking"] or 0)>0]; nth=[r for r in v4 if not (r["v04"]["thinking"] or 0) and not r["v04"]["error"]]
    allv=[r for r in now_rows if r.get("v04")]
    res["now"]["v04"]={"e86b":{"a":_k("mat_rows"),"b":_k("mat_b"),"c":_k("mat_c")},
        "layer":dict(collections.Counter(r["v04"]["layer"] for r in v4 if r["v04"]["layer"])),
        "understand_ms":{"median":med(um),"p90":p90(um),"thinking_calls":len(th),"thinking_tokens_sum":sum(r["v04"]["thinking"] or 0 for r in allv),
                         "thinking_median":med([r["v04"]["understand_ms"] for r in th]),"thinking_p90":p90([r["v04"]["understand_ms"] for r in th]),
                         "no_thinking_median":med([r["v04"]["understand_ms"] for r in nth]),"no_thinking_p90":p90([r["v04"]["understand_ms"] for r in nth])},
        "errors":dict(collections.Counter(str((r["v04"]["error"] or {}).get("kind")) for r in allv if r["v04"]["error"])),
        "dropped_n":sum(len(r["v04"]["dropped"] or []) for r in allv),"invented_n":sum(1 for r in allv for x in r["v04"]["dropped"] or [] if x.get("why")=="not_in_gold"),
        "ft5_turns":sum(1 for r in allv if r["v04"]["ft5"]),"turn_ms":{"median":med([r["ms"] for r in allv if r["ms"]]),"p90":p90([r["ms"] for r in allv if r["ms"]])}}
with open(WOUT+"/fail-by-tag.csv","w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow(["축","꼴","턴","통과","후보","Jev","앱 규칙","데이터"])
    for ax,k in (("의도","layer_by_intent"),("말","layer_by_form"),("데이터","layer_by_data")):
        for x in res["now"][k]: w.writerow([ax,x["tag"],x["turns"],x["pass"],x["후보"],x["Jev"],x["앱 규칙"],x["데이터"]])
json.dump(res,open(WOUT+"/summary.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in res["now"].items() if k in ("all","counts")},ensure_ascii=False,indent=1))
for k in res:
    if k not in ("now","sample_turns"): print(k,json.dumps({a:res[k].get(a) for a in ("all","sample","invented","tokens","latency","errors")},ensure_ascii=False))
