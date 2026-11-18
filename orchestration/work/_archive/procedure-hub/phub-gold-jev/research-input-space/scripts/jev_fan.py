"""Jev fan-out 판 — resolve 맞춤 꼴 없이, 허브 resolve 목록 꼴(tables)로 받은 gold 입구 전체에 후보마다 Noul 하나.
usage: jev_fan.py <conversations.jsonl> <now turns.jsonl> <out.jsonl> <alias on|off> <mode one|tables> [conv,…]"""
import asyncio, json, os, sys, time, collections
import clinic_chat.clients.jev_client as jc
jc.JEV_TIMEOUT_S = 90.0  # 앱 기본 10초 — 820 질문 한 요청을 재려고 이 스크립트에서만 늘린다
from clinic_chat.config import load_settings
from clinic_chat.clients.hub_rest import HubRest
from clinic_chat.clients.jev_client import Jev, make_client, noul
from clinic_chat.consult import turn_kind as tk
from paths import RUN, CONV
# usage: jev_fan.py <별칭 on|off> <one|tables> [대화,…] — 출력 runs/fan-<별칭>.jsonl
ALIAS,MODE=sys.argv[1:3]; ONLY=set(sys.argv[3].split(",")) if len(sys.argv)>3 else None
NOW=os.path.join(RUN,"now-rows.jsonl"); OUT=os.path.join(RUN,f"fan-{ALIAS}.jsonl")
CONC=int(os.environ.get("FAN_CONC","2"))
TABLES=["concern","site","modality","procedure","product"]
TASK=("A customer is talking to a skin/aesthetic clinic consultant in Korean. `turns` is the conversation so far (each earlier customer "
      "message and what was identified in it), `object` is what has been identified so far, `question` is the customer's latest message. "
      "A candidate is a TARGET of `question` if the customer is talking about it or referring to it in `question`: named directly, "
      "named with particles in between, in a different word order, shortened, misspelled, by an alias, in the customer's own words, "
      "or referred back to (\"that one\", a follow-up question about it). A broad concern said together with a body site means the "
      "narrower concern of that site when one exists. A candidate whose name merely shares letters with a word in `question` is not a target. "
      "Greetings, agreement, complaints and small talk have no target.")
Q_C='Using `task`: is "{name}" (`candidates[{i}]`, {table}) a target of `question`?'
Q_KIND={"new":"Using `task`: does `question` name a new target (a concern, body site, procedure, modality or product) or answer the consultant's previous question — i.e. bring new information to search for?",
        "talk":"Using `task`: is `question` only a greeting, agreement, complaint or small talk with no target at all?",
        "follow":"Using `task`: does `question` ask a follow-up about a target already in `turns` without naming any new target?"}
def asks_by_conv():
    out={}
    for l in open(NOW,encoding="utf-8"):
        r=json.loads(l)
        if r.get("phase")=="end":
            a=(r.get("consult") or {}).get("ask")
            if a: out[(r["conv_id"].split("-")[0],r["turn"])]=[o.get("name") or "" for o in a.get("options") or []]
    return out
async def entities(hub):
    t0=time.perf_counter()
    ra=await hub.read_all("resolve",{"tables":TABLES})
    ents=collections.OrderedDict()
    for x in ra.items:
        k=(x["entity_table"],x["entity_code"]); e=ents.setdefault(k,{"name":x["entity_name"],"al":[]})
        if x.get("name_kind")!="이름" and x["text"]!=x["entity_name"] and x["text"] not in e["al"]: e["al"].append(x["text"])
    return ents,round((time.perf_counter()-t0)*1000),ra.complete
async def ask(jev,state,cands,kinds):
    st=dict(state); st["candidates"]=[{k:v for k,v in c.items() if k!="key"} for c in cands]
    qs={f"c_{i}":noul(Q_C.replace("{name}",c["name"]).replace("{i}",str(i)).replace("{table}",c["table"])) for i,c in enumerate(cands)}
    if kinds:
        for k,v in Q_KIND.items(): qs[f"tk_{k}"]=noul(v)
    a=await jev.ask(st,qs)
    return a
async def main():
    s=load_settings(); hub=HubRest(s.hub_rest_url,page_limit=s.hub_page_limit); jev=Jev(make_client(s))
    ents,list_ms,complete=await entities(hub)
    print("entities",len(ents),"list_ms",list_ms,"complete",complete,flush=True)
    cands=[{"key":k,"id":f"{k[0]}:{k[1]}","name":e["name"],"table":k[0],**({"aliases":e["al"]} if ALIAS=="on" and e["al"] else {})} for k,e in ents.items()]
    names={c["id"]:c["name"] for c in cands}
    ASKS=asks_by_conv()
    got=collections.Counter(json.loads(l)["conv"] for l in open(OUT)) if os.path.exists(OUT) else {}
    convs=[json.loads(l) for l in open(CONV,encoding="utf-8")]
    convs=[c for c in convs if (not ONLY or c["conv"] in ONLY) and got.get(c["conv"],0)<len(c["turns"])]
    sem=asyncio.Semaphore(CONC); f=open(OUT,"a",encoding="utf-8")
    async def run_conv(c):
        hist=[]; obj=collections.OrderedDict()
        for t in c["turns"]:
            state={"task":TASK,"turns":hist,"object":{"identified":[names[i] for i,v in obj.items() if v]},"question":t["text"]}
            rec={"conv":c["conv"],"turn":t["n"],"text":t["text"],"alias":ALIAS,"mode":MODE}
            async with sem:
                t0=time.perf_counter()
                try:
                    if MODE=="one":
                        ans=[await ask(jev,state,cands,True)]; parts=[cands]
                    else:
                        parts=[[c_ for c_ in cands if c_["table"]==tb] for tb in TABLES]
                        ans=await asyncio.gather(*(ask(jev,state,p,i==0) for i,p in enumerate(parts)))
                    rec["error"]=None
                except Exception as e:
                    ans=[]; parts=[]; rec["error"]=f"{type(e).__name__}: {str(e)[:300]}"
                rec["ms"]=round((time.perf_counter()-t0)*1000)
            scores={}; kn={}
            for a,p in zip(ans,parts):
                for i,c_ in enumerate(p): scores[c_["id"]]=a.nouls[f"c_{i}"]
                for k in Q_KIND:
                    if f"tk_{k}" in a.nouls: kn[k]=a.nouls[f"tk_{k}"]
            yes=[i for i,v in scores.items() if v>=s.jev_noul_yes_at]
            rec.update({"requests":len(ans),"req_ms":[a.ms for a in ans],"usage":[a.usage for a in ans],"models":sorted({a.model or "" for a in ans}),
                        "picks":[i.split(":",1) for i in yes if not i.startswith("site:")],"sites":[i.split(":")[1] for i in yes if i.startswith("site:")],
                        "kind":tk.judge(kn,s.jev_noul_yes_at)[0] if kn else None,"kind_nouls":kn,"withdraw":[],"invented":[],"bad_sites":[],
                        "top":sorted(((i,round(v,3)) for i,v in scores.items() if v>=0.2),key=lambda x:-x[1])[:40],"n_yes":len(yes),"n_between":sum(1 for v in scores.values() if 0.3<v<0.7)})
            f.write(json.dumps(rec,ensure_ascii=False)+"\n"); f.flush()
            for i in yes: obj[i]=True
            h={"n":t["n"],"customer":t["text"],"identified":[names[i] for i in yes]}
            if ASKS.get((c["conv"],t["n"])): h["consultant_asked_options"]=ASKS[(c["conv"],t["n"])]
            hist.append(h)
            print(c["conv"],t["n"],rec["ms"],rec["n_yes"],rec["error"] or "",flush=True)
    await asyncio.gather(*(run_conv(c) for c in convs))
asyncio.run(main())
