import csv, json, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import P, SM, OUT
from convs import CONVS, KMAP
KIND_CODES=("overview","mechanism","indication","outcome","lineup","adverse","recovery","contraindication","avoid","combo","package","same_day","order_interval","offer")  # 앱 clinic_chat/walk/kinds.py KIND_CODES 그대로
def rd(p): return list(csv.DictReader(open(p,encoding='utf-8-sig')))
PRE={"c":("concern","CON-%03d"),"s":("site","SITE-%03d"),"p":("procedure","PRC-%03d"),"m":("modality","M%d"),"d":("product","PRD-%03d")}
def code(x):
    t,f=PRE[x[0]]; return f"{t}:{f%int(x[1:])}"
entry=rd(SM+"/gold/g_entry.csv")
names={}; ents=collections.defaultdict(list)
for x in entry:
    k=f"{x['entity_table']}:{x['entity_code']}"; names.setdefault(k,x['entity_name']); ents[k].append(x)
concern={x['code']:x for x in rd(SM+"/silver/concern.csv")}
kids=collections.Counter(x['parent_code'] for x in concern.values())
cs=collections.defaultdict(list)
for x in rd(SM+"/silver/concern_site.csv"): cs[x['concern_code']].append((x['site_code'],x['id']))
gi=rd(SM+"/gold/g_indication.csv")
rows=collections.Counter(x['asked_concern_code'] for x in gi)
procs=collections.defaultdict(set)
for x in gi:
    if x['procedure_code']: procs[x['asked_concern_code']].add(x['procedure_code'])
GOLD_ROWS={}  # 11-18 SPEC-008 fix1 — 재료 정답 키(rows)의 gold 근거: gid → (gold 표, 행)
for gt in ("g_adverse","g_contraindication","g_outcome","g_pair","g_offer","g_recovery","g_adverse_detail","g_package","g_profile"):
    for x in rd(SM+f"/gold/{gt}.csv"): GOLD_ROWS[x["gid"]]=(gt,x)
def row_basis(gid):
    gt,x=GOLD_ROWS[gid]
    if gt=="g_pair": return f"{gid} {gt} {x['from_name']}({x['from_code']}) → {x['to_name']}({x['to_code']}) · {x['kind']} · 같은 날 {x['same_day'] or '-'}"
    if gt=="g_offer": return f"{gid} {gt} 「{x['offer_name']}」 {x['item_name']}({x['item_code']}) · {x['price_low']}~{x['price_high']}"
    val=x.get("adverse_name") or x.get("condition_name") or x.get("effect_name") or x.get("text") or ""
    return f"{gid} {gt} {x.get('target_name')}({x.get('target_code')}) — {val[:40]}"
def norm(s): return "".join(s.split()).lower()
def groups(s): return [[code(a) for a in g.split("|")] for g in s.split(",") if g] if s else []
def flat(s): return [code(a) for g in s.split(",") if g for a in g.split("|")] if s else []
def basis(text, k):
    n=norm(text); hit=[e for e in ents[k] if e['norm'].lower() in n]
    if hit:
        e=max(hit,key=lambda e:len(e['norm'])); b=f"{k} {names[k]} — g_entry {e['gid']} 「{e['text']}」({e['name_kind']}) 글자 일치"
    else: b=f"{k} {names[k]} — 글자 일치 없음"
    if k.startswith("concern:"):
        c=k.split(":")[1]
        if cs.get(c): b+=" · concern_site "+", ".join(f"{i}→{s}" for s,i in cs[c])
    return b
bad=[]; n_turn=0
with open(OUT+"/conversations.jsonl","w",encoding="utf-8") as f:
    for cid,title,turns in CONVS:
        out=[]
        for i,t in enumerate(turns,1):
            tg=groups(t["t"]); ex=flat(t["ex"]); st=flat(t["site"]); wd=groups(t["w"])
            for k in [a for g in tg for a in g]+ex+st+[a for g in wd for a in g]:
                if k not in names: bad.append((cid,i,k))
            first=[g[0] for g in tg if g[0].startswith("concern:")]
            data=[]
            for k in first:
                c=k.split(":")[1]
                data+=["부위있음" if cs.get(c) else "부위없음","하위있음" if kids.get(c) else "하위없음",
                       "행0" if not rows.get(c) else ("시술닿음" if procs.get(c) else "시술안닿음")]
            b=[basis(t["text"],a) for g in tg for a in g[:1]]
            if t["ask"]: b.append(f"앞 턴에 앱이 준 되물음의 {t['ask']} 번째 선택지 — 실행 때 장부의 ask.options 로 정한다")
            if not tg and not t["ask"] and not wd: b.append("기대 대상 없음")
            if t["note"]: b.append(t["note"])
            kinds,kok=t.get("kinds"),t.get("kok") or ""
            if kinds is None and (cid,i) in KMAP:
                kinds,kok=KMAP[(cid,i)]; b.append("정보 종류 — 이번 말이 묻는 것을 앱 종류 표(walk/kinds.py)의 영어 이름과 견줘 정함")
            elif kinds: b.append("정보 종류 — 이번 말이 묻는 것을 앱 종류 표(walk/kinds.py)의 영어 이름과 견줘 정함")
            kl=[x for x in (kinds or "").split(",") if x]; okl=[x for x in kok.split(",") if x]
            for x in kl+okl:
                if x not in KIND_CODES: bad.append((cid,i,"kind:"+x))
            shown=None
            if t.get("a") or t.get("lst"):
                ls=[code(x) for x in (t.get("lst") or "").split(",") if x]
                for k in ls:
                    if k not in names: bad.append((cid,i,k))
                shown={"answer_summary":t.get("a"),"list":[{"table":k.split(":")[0],"code":k.split(":")[1],"name":names.get(k)} for k in ls]}
            if t.get("ref"): b.append(f"가리키는 것 — 앞 턴 shown 의 {'리스트' if t['ref']['to']=='list' else '답 요약'}: {t['ref']['how']}")
            out.append({"n":i,"text":t["text"],"tags":{"intent":t["intent"].split(","),"form":t["form"],"data":sorted(set(data))},
                        "key":{"targets":[[{"table":a.split(":")[0],"code":a.split(":")[1],"name":names.get(a)} for a in g] for g in tg],
                               "extras_ok":ex,"kind":t["k"].split("|"),"site_filter":st,"site_required":t["sr"],
                               "dots":"말한 고민(묶음에서 고른 것)의 concern_site 직접 부위 — 채점 때 gold 로 셈",
                               "withdraw":[[a for a in g] for g in wd],"ask_option":t["ask"]},
                        "ambiguous":t["amb"],"basis":b})
            if kl: out[-1]["key"]["kinds"]=kl; out[-1]["key"]["kinds_ok"]=okl
            if t.get("ref"): out[-1]["key"]["ref"]=t["ref"]
            if t.get("rows"):  # 재료 정답 키(E8-6b) — rows = 꼭 있어야 하는 행 · depth = 깊이 읽기 대상(그 밖의 깊이 후보는 listed_only)
                rg=[[a for a in g.split("|")] for g in t["rows"].split(",") if g]
                for g in rg:
                    for a in g:
                        if a not in GOLD_ROWS: bad.append((cid,i,"row:"+a))
                dp=flat(t.get("depth") or "")
                for k in dp:
                    if k not in names: bad.append((cid,i,k))
                out[-1]["key"]["material"]={"rows":rg,"depth":dp}
                out[-1]["basis"]+=["재료 — "+row_basis(a) for g in rg for a in g if a in GOLD_ROWS]
                out[-1]["basis"].append("깊이 — "+(", ".join(f"{k} {names.get(k)}" for k in dp) if dp else "깊이 읽기 0(상대 · 상품의 시술은 이번 턴 대상이 아니다)"))
            if shown: out[-1]["shown"]=shown
            n_turn+=1
        f.write(json.dumps({"conv":cid,"title":title,"turns":out},ensure_ascii=False)+"\n")
print("convs",len(CONVS),"turns",n_turn,"bad",bad)
ic=collections.Counter(); fc=collections.Counter(); dc=collections.Counter(); amb=0
for l in open(OUT+"/conversations.jsonl",encoding="utf-8"):
    for t in json.loads(l)["turns"]:
        ic.update(t["tags"]["intent"]); fc[t["tags"]["form"]]+=1; dc.update(t["tags"]["data"]); amb+=bool(t["ambiguous"])
print(ic); print(fc); print(dc); print("amb",amb)
