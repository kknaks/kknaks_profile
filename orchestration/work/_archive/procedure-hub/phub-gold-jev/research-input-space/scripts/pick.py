"""후보 뽑기 시안 — claude -p (앱 chat_args 와 같은 격리 인자 · 세션은 남기지 않음) 로 턴마다 한 번.
usage: pick.py <conversations.jsonl> <now turns.jsonl> <out.jsonl> <model> <alias on|off> [conv,conv…]"""
import asyncio, csv, json, os, sys, time, collections
from clinic_chat.llm.cli import DISALLOWED_TOOLS
from clinic_chat.llm.cli_process import child_env
import tempfile
from paths import SM, RUN, CONV
# usage: pick.py <모델 sonnet|haiku> <별칭 on|off> [대화,대화…] — 출력 runs/pick-<모델>-<별칭>.jsonl · 되물음 선택지는 runs/now-rows.jsonl
MODEL,ALIAS=sys.argv[1:3]; ONLY=set(sys.argv[3].split(",")) if len(sys.argv)>3 else None
NOW=os.path.join(RUN,"now-rows.jsonl"); OUT=os.path.join(RUN,f"pick-{MODEL}-{ALIAS}.jsonl")
CONC=int(os.environ.get("PICK_CONC","4"))
TABLES=[("concern","고민"),("site","부위"),("modality","계열"),("procedure","시술"),("product","제품")]
def gold_list(alias):
    ents=collections.OrderedDict()
    for x in csv.DictReader(open(SM+"/gold/g_entry.csv",encoding="utf-8-sig")):
        k=(x["entity_table"],x["entity_code"]); e=ents.setdefault(k,{"name":x["entity_name"],"al":[]})
        if x["name_kind"]!="이름" and x["text"]!=x["entity_name"] and x["text"] not in e["al"]: e["al"].append(x["text"])
    out=[]; valid={}
    for t,label in TABLES:
        out.append(f"## {label} (table = {t})")
        for (tt,c),e in ents.items():
            if tt!=t: continue
            valid[(t,c)]=e["name"]
            out.append(f"{c} {e['name']}"+(f" (= {', '.join(e['al'])})" if alias and e["al"] else ""))
    return "\n".join(out), valid
LIST,VALID=gold_list(ALIAS=="on")
SYSTEM=f"""너는 피부 · 미용 상담 앱의 「후보 뽑기」 단계다. 손님의 이번 말이 가리키는 대상을 아래 목록에서 골라 JSON 한 줄로만 답한다. 설명 · 코드 울타리 · 다른 글을 쓰지 않는다.

출력 꼴: {{"targets":[{{"table":"concern","code":"CON-000"}}],"kind":"new","sites":["SITE-000"],"withdraw":[]}}

규칙
1. targets = 이번 말이 말하거나 가리키는 대상. 목록에 있는 (table, code) 만 쓴다. 목록에 없으면 넣지 않는다 — 코드를 지어내지 않는다.
2. 대화 맥락으로 읽는다. 조사가 끼거나(턱에 살) 어순이 바뀌거나(볼이 꺼졌어요) 줄이거나 오타가 있거나 자기 말로 바꿔 말해도 같은 대상이다.
3. 넓은 고민과 부위를 함께 말했고 그 부위의 더 좁은 고민이 목록에 있으면 좁은 고민을 고른다(이마에 주름 → 이마주름).
4. 같은 이름이 여러 표에 있으면 가장 넓은 것 하나만 고른다(계열 > 시술 > 제품).
5. 글자만 같고 뜻이 다른 것은 고르지 않는다(「주사 맞기 무섭다」 의 주사는 고민 「주사」 가 아니다).
6. kind — new: 대상(고민 · 부위 · 시술 · 계열 · 제품)을 새로 말했거나 앞 되물음에 답했다 · follow: 대상을 새로 말하지 않고 앞 대상에 대해 이어 묻는다(「그거 아파요?」 「얼마나 가요?」) — targets 에 그 앞 대상을 넣는다 · talk: 대상 없는 인사 · 맞장구 · 불만 · 혼잣말 — targets 는 [].
7. sites = 이번 말에 나온 부위의 코드만(고민 이름 안의 부위 포함). 앞 턴의 부위를 끌고 오지 않는다. 없으면 [].
8. withdraw = 손님이 빼 달라고 한 대상(「그건 말고」 「필러는 됐어요」)의 "table:code". 그 대상은 targets 에 넣지 않는다. 없으면 [].
9. 앞 턴에 상담사가 선택지를 물었고 이번 말이 그 답(「두 번째요」 · 이름)이면 그 선택지를 targets 에 넣는다.

# 목록
{LIST}
"""
def asks_by_conv():
    """지금 시스템 실행 장부 → (conv, turn) 에 준 되물음 선택지."""
    out={}
    if not os.path.exists(NOW): return out
    for l in open(NOW,encoding="utf-8"):
        r=json.loads(l)
        if r.get("phase")=="end":
            a=(r.get("consult") or {}).get("ask")
            if a: out[(r["conv_id"].split("-")[0],r["turn"])]=[(o["table"],o["code"],o.get("name") or "") for o in a.get("options") or []]
    return out
ASKS=asks_by_conv()
def args(): return ["claude","-p","--model",MODEL,"--effort","low","--max-turns","1","--system-prompt",SYSTEM,
        "--setting-sources","","--tools","","--disallowedTools",DISALLOWED_TOOLS,"--disable-slash-commands",
        "--strict-mcp-config","--no-session-persistence","--permission-mode","bypassPermissions","--output-format","json"]
CWD=os.path.join(tempfile.gettempdir(),"input-space-pick-cwd"); os.makedirs(CWD,exist_ok=True)  # 레포 밖
async def call(msg):
    t0=time.perf_counter()
    p=await asyncio.create_subprocess_exec(*args(),stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,
                                           stderr=asyncio.subprocess.PIPE,cwd=CWD,env=child_env())
    try: so,se=await asyncio.wait_for(p.communicate(msg.encode()),120)
    except asyncio.TimeoutError:
        p.kill(); return {"error":"timeout","ms":round((time.perf_counter()-t0)*1000)}
    ms=round((time.perf_counter()-t0)*1000)
    try: d=json.loads(so.decode())
    except Exception: return {"error":"parse_cli","ms":ms,"raw":so.decode()[:300],"stderr":se.decode()[-300:]}
    if isinstance(d,list): d=next((x for x in reversed(d) if x.get("type")=="result"),{})
    return {"ms":ms,"api_ms":d.get("duration_api_ms"),"text":d.get("result") or "","usage":d.get("usage") or {},
            "models":list((d.get("modelUsage") or {}).keys()),"error":None if not d.get("is_error") else str(d.get("result"))[:200]}
def parse(text):
    i,j=text.find("{"),text.rfind("}")
    try: d=json.loads(text[i:j+1])
    except Exception: return None
    return d if isinstance(d,dict) else None
def name(t,c): return VALID.get((t,c),"")
async def run_conv(c,sem,f):
    hist=[]; obj=collections.OrderedDict(); sites_said=[]
    for t in c["turns"]:
        lines=[]
        if hist:
            lines.append("# 대화 지금까지")
            for h in hist:
                lines.append(f"{h['n']}. 손님: {h['text']}")
                lines.append("   → 고른 대상: "+(", ".join(f"{name(a,b)}({a}:{b})" for a,b in h["picks"]) or "없음")+f" · {h['kind']}")
                if h.get("shown"):  # 11-18 보강(D-8) — 표에 적어 둔 앞 답 요약 · 보여 준 리스트
                    if h["shown"].get("answer_summary"): lines.append("   상담사 답 요약: "+h["shown"]["answer_summary"])
                    if h["shown"].get("list"): lines.append("   보여 준 리스트: "+" / ".join(f"{i}) {x['name']}({x['table']}:{x['code']})" for i,x in enumerate(h["shown"]["list"],1)))
                if h.get("ask"): lines.append("   상담사가 물은 선택지: "+" / ".join(f"{i}) {nm}({a}:{b})" for i,(a,b,nm) in enumerate(h["ask"],1)))
        lines.append("# 지금 객체")
        lines.append("대상: "+(", ".join(f"{name(a,b)}({a}:{b})" for (a,b),st in obj.items() if st=="on") or "없음"))
        lines.append("거둔 것: "+(", ".join(f"{name(a,b)}({a}:{b})" for (a,b),st in obj.items() if st=="off") or "없음"))
        lines.append(f"# 이번 말\n{t['text']}")
        msg="\n".join(lines)
        async with sem: r=await call(msg)
        d=parse(r.get("text") or "") or {}
        raw=[(x.get("table"),x.get("code")) for x in d.get("targets") or [] if isinstance(x,dict)]
        picks=[x for x in raw if x in VALID]
        sites=[s for s in d.get("sites") or [] if ("site",s) in VALID]
        wd=[w for w in d.get("withdraw") or [] if isinstance(w,str) and tuple(w.split(":",1)) in VALID]
        rec={"conv":c["conv"],"turn":t["n"],"text":t["text"],"model":MODEL,"alias":ALIAS,"ms":r.get("ms"),"api_ms":r.get("api_ms"),
             "usage":r.get("usage"),"models":r.get("models"),"error":r.get("error") or (None if d else "parse_json"),
             "raw_text":(r.get("text") or "")[:600],"picks":picks,"invented":[x for x in raw if x not in VALID],
             "bad_sites":[s for s in d.get("sites") or [] if ("site",s) not in VALID],
             "kind":d.get("kind"),"sites":sites,"withdraw":wd,"msg_chars":len(msg)}
        f.write(json.dumps(rec,ensure_ascii=False)+"\n"); f.flush()
        for x in picks: obj[x]="on"
        for w in wd: obj[tuple(w.split(":",1))]="off"
        hist.append({"n":t["n"],"text":t["text"],"picks":picks,"kind":d.get("kind"),"ask":ASKS.get((c["conv"],t["n"])),"shown":t.get("shown")})
        print(c["conv"],t["n"],r.get("ms"),rec["error"] or "",flush=True)
async def main():
    done=set()
    if os.path.exists(OUT):
        got=collections.Counter(json.loads(l)["conv"] for l in open(OUT))
    else: got={}
    convs=[json.loads(l) for l in open(CONV,encoding="utf-8")]
    convs=[c for c in convs if (not ONLY or c["conv"] in ONLY) and got.get(c["conv"],0)<len(c["turns"])]
    sem=asyncio.Semaphore(CONC)
    with open(OUT,"a",encoding="utf-8") as f:
        await asyncio.gather(*(run_conv(c,sem,f) for c in convs))
print("system chars",len(SYSTEM),"entities",len(VALID),flush=True)
if os.environ.get("PICK_DRY"): sys.exit()
asyncio.run(main())
