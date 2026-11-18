import csv,json,collections,sys,os
sys.argv=["x"]; os.chdir(os.path.dirname(os.path.abspath(__file__)))
src=open("score.py").read().split("# ───────── 지금 시스템")[0]
g={"__file__":os.path.abspath("score.py")}; exec(src,g)
CONVS,key_of,target_score,prior_ok,prior_add,site_score,pct,med,p90=[g[k] for k in ("CONVS","key_of","target_score","prior_ok","prior_add","site_score","pct","med","p90")]
SM=g["SM"]
fam=collections.defaultdict(set)
for x in csv.DictReader(open(SM+"/gold/g_scope.csv",encoding="utf-8-sig")):
    a=f"{x['subject_table']}:{x['subject_code']}"; b=f"{x['holder_table']}:{x['holder_code']}"
    if a!=b: fam[a].add(b); fam[b].add(a)
par={x["code"]:x["parent_code"] for x in csv.DictReader(open(SM+"/silver/concern.csv",encoding="utf-8-sig"))}
def anc(c):
    out=set()
    while par.get(c): c=par[c]; out.add(c)
    return out
def family(a,b):
    if a.startswith("concern:") and b.startswith("concern:"):
        x,y=a.split(":")[1],b.split(":")[1]; return x in anc(y) or y in anc(x)
    return b in fam[a]
def run(fn,th):
    pk={(r["conv"],r["turn"]):r for r in map(json.loads,open(fn))}
    rows=[]
    for c in CONVS:
        prior=set()
        for t in c["turns"]:
            key=key_of(c,t); r=pk.get((c["conv"],t["n"]))
            if not r: prior_add(key,prior); continue
            picks={i for i,v in r["top"] if v>=th}
            ts=target_score(key,picks,prior_ok(key,prior)); 
            ok_set=set(ts["chosen"])|key["extras"]|prior_ok(key,prior)
            bad2=[b for b in ts["bad"] if not any(family(b,o) for o in ok_set)]
            prior_add(key,prior)
            if key["amb"] or key["na"]: continue
            rows.append((ts,bad2,key))
    n=len(rows); g_=sum(ts["n_groups"] for ts,_,_ in rows); h=sum(ts["hit"] for ts,_,_ in rows); pk_=sum(len(ts["picks"]) for ts,_,_ in rows); bad=sum(len(ts["bad"]) for ts,_,_ in rows); badf=sum(len(b) for _,b,_ in rows)
    return {"th":th,"turns":n,"recall":pct(h,g_),"precision":pct(pk_-bad,pk_),"exact":pct(sum(ts["exact"] for ts,_,_ in rows),n),
            "precision_family_ok":pct(pk_-badf,pk_),"exact_family_ok":pct(sum(1 for ts,b,_ in rows if not ts["missed"] and not b),n),"picks_per_turn":round(pk_/n,2)}
out={}
for th in (0.5,0.6,0.7,0.8):
    out[f"fan-on@{th}"]=run(os.path.join(g["SP"],"fan-on.jsonl"),th); print(out[f"fan-on@{th}"])
out["fan-off@0.7"]=run(os.path.join(g["SP"],"fan-off.jsonl"),0.7); print(out["fan-off@0.7"])
P=g["OUT"]; R=json.load(open(P+"/summary.json")); R["Jev fan-out 문턱별"]=out; json.dump(R,open(P+"/summary.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
