"""소넷 후보 → Jev 점수(앱의 맨 앞 판단 요청 꼴 ask_front 그대로 · 후보만 소넷이 뽑은 것)."""
import asyncio, json, sys, time, os, collections
from clinic_chat.config import load_settings
from clinic_chat.columns.base import Deps
from clinic_chat.consult import prompt as prompt_mod
from clinic_chat.walk.jev_requests import ask_front, base_state
from clinic_chat.walk.kinds import KINDS
from paths import SM, RUN
PICK=os.path.join(RUN,sys.argv[1]) if not os.path.isabs(sys.argv[1]) else sys.argv[1]
async def main():
    s=load_settings(); d=Deps.from_settings(s); p=prompt_mod.load(s.chat_prompt_path())
    catalog=[{"code":k.code,"name":k.name} for k in KINDS]
    rows=[json.loads(l) for l in open(PICK,encoding="utf-8")]
    by=collections.defaultdict(list)
    for r in rows: by[r["conv"]].append(r)
    names={}
    import csv
    for x in csv.DictReader(open(SM+"/gold/g_entry.csv",encoding="utf-8-sig")):
        names.setdefault((x["entity_table"],x["entity_code"]),x["entity_name"])
    for conv,rs in by.items():
        rs.sort(key=lambda r:r["turn"]); seen={}; qs=[]
        for r in rs:
            if "jev" not in r:
                cands=[]
                for a,b in r["picks"]:
                    it={"id":f"{a}:{b}","name":names.get((a,b),""),"table":a,"matched":None,"rows":{}}
                    if (a,b) in seen: it["carried_from"]=seen[(a,b)]
                    cands.append(it)
                r["jev"]={}; r["jev_ms"]=0
                if cands:
                    t0=time.perf_counter()
                    try:
                        tn,_,_,_,_=await ask_front(d.jev, base_state(r["text"],None,prev_questions=qs[-3:] or None), cands, catalog, p.jev_front, s.jev_batch_size)
                        r["jev"]={c["id"]:v for c,v in zip(cands,tn)}
                    except Exception as e: r["jev_error"]=type(e).__name__
                    r["jev_ms"]=round((time.perf_counter()-t0)*1000)
            for a,b in r["picks"]: seen[(a,b)]=r["turn"]
            qs.append(r["text"])
        print(conv,flush=True)
    with open(PICK,"w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
asyncio.run(main())
