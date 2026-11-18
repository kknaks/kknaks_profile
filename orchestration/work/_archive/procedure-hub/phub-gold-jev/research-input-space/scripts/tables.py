import json,os,collections
import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import OUT as P
R=json.load(open(P+"/summary.json"))
def L(fn): return [json.loads(l) for l in open(P+"/"+fn)] if os.path.exists(P+"/"+fn) else []
now=L("now-turns.jsonl")
print("## counts",json.dumps(R["now"]["counts"],ensure_ascii=False))
print("sample_turns",R.get("sample_turns"))
print("\n### 표1 의도 × 층"); print("| 의도 꼴 | 턴 | 통과 | 후보 | Jev | 앱 규칙 | 데이터 |\n|---|---|---|---|---|---|---|")
for x in R["now"]["layer_by_intent"]: print(f"| {x['tag']} | {x['turns']} | {x['pass']} | {x['후보']} | {x['Jev']} | {x['앱 규칙']} | {x['데이터']} |")
print("\n### 표1b 말 꼴 × 층"); print("| 말 꼴 | 턴 | 통과 | 후보 | Jev | 앱 규칙 | 데이터 |\n|---|---|---|---|---|---|---|")
for x in R["now"]["layer_by_form"]: print(f"| {x['tag']} | {x['turns']} | {x['pass']} | {x['후보']} | {x['Jev']} | {x['앱 규칙']} | {x['데이터']} |")
print("\n### 표1c 데이터 조합 × 층"); print("| 데이터 | 턴 | 통과 | 후보 | Jev | 앱 규칙 | 데이터 |\n|---|---|---|---|---|---|---|")
for x in R["now"]["layer_by_data"]: print(f"| {x['tag']} | {x['turns']} | {x['pass']} | {x['후보']} | {x['Jev']} | {x['앱 규칙']} | {x['데이터']} |")
names=["sonnet+별칭","sonnet+별칭+Jev","sonnet","haiku+별칭","haiku","Jev fan-out+별칭","Jev fan-out"]
def row(label,d):
    return f"| {label} | {d['turns']} | {d['recall']} | {d['precision']} | {d['target_exact']} | {d['kind']} | {d['site']} | {d['ms_median']} | {d['ms_p90']} |"
print("\n### 표2 전수"); print("| 판 | 턴 | 포함률 | 정밀 | 대상 정답 | 턴 종류 | 부위 | ms 중앙 | p90 |\n|---|---|---|---|---|---|---|---|---|")
print(row("지금",R["now"]["all"]))
for n in names:
    if n in R: print(row(n,R[n]["all"]))
print("\n### 표2 표본"); print("| 판 | 턴 | 포함률 | 정밀 | 대상 정답 | 턴 종류 | 부위 | ms 중앙 | p90 |\n|---|---|---|---|---|---|---|---|---|")
if "sample" in R["now"]: print(row("지금",R["now"]["sample"]))
for n in names:
    if n in R: print(row(n,R[n]["sample"]))
for ax,k,nk in (("말 꼴","by_form","by_form_sample"),("의도 꼴","by_intent","by_intent_sample")):
    print(f"\n### 표2 {ax}별(표본) — 대상 정답률 / 포함률")
    tags=list(R["now"][nk]) if nk in R["now"] else []
    cols=["지금"]+[n for n in names if n in R]
    print("| "+ax+" | 턴 | "+" | ".join(cols)+" |\n|---|---|"+"---|"*len(cols))
    for t in tags:
        cells=[]
        for c in cols:
            d=(R["now"][nk] if c=="지금" else R[c][k]).get(t) or {}
            cells.append(f"{d.get('target_exact')} / {d.get('recall')}")
        print(f"| {t} | {R['now'][nk][t]['turns']} | "+" | ".join(cells)+" |")
    print(f"\n### 표2 {ax}별(표본) — 턴 종류 / ms 중앙")
    print("| "+ax+" | "+" | ".join(cols)+" |\n|---|"+"---|"*len(cols))
    for t in tags:
        cells=[]
        for c in cols:
            d=(R["now"][nk] if c=="지금" else R[c][k]).get(t) or {}
            cells.append(f"{d.get('kind')} / {d.get('ms_median')}")
        print(f"| {t} | "+" | ".join(cells)+" |")
for n in names:
    if n in R: print("\n",n,json.dumps({a:R[n].get(a) for a in ("invented","tokens","latency","errors","withdraw","jev_ms_median","n_yes_median","n_between_median")},ensure_ascii=False))
# 후보 층 39 → 소넷이 맞혔나
so={(r["conv"],r["turn"]):r for r in L("pick-sonnet-on-turns.jsonl")}
sj={(r["conv"],r["turn"]):r for r in L("pick-sonnet-on-jev-turns.jsonl")}
for lay in ("후보","Jev","앱 규칙","데이터"):
    ks=[(r["conv"],r["turn"]) for r in now if r["layer"]==lay and not r["ambiguous"] and not r["na"]]
    ok=sum(1 for k in ks if k in so and so[k]["checks"]["target"]); 
    print(f"지금 {lay} 층 실패 {len(ks)} 턴 가운데 소넷+별칭 대상 정답 {ok}"+(f" · +Jev {sum(1 for k in ks if k in sj and sj[k]['checks']['target'])}" if sj else ""))
print("\n## 소넷+별칭 실패 턴")
for r in so.values():
    if r["ambiguous"] or r["na"]: continue
    c=r["checks"]
    if not c["target"] or not c["kind"] or c["site"] is False or not c["withdraw"]:
        print(f"- {r['conv']}-{r['turn']} 「{r['text']}」 picks {r['picks']} kind {r['kind']} wd {r['withdraw']} | missed {r['score']['missed'][:1]} bad {r['score']['bad']} | {[k for k,v in c.items() if v is False]}")
if sj:
    print("\n## +Jev 로 달라진 턴")
    for k,r in sj.items():
        a=so[k]
        if r["ambiguous"] or r["na"]: continue
        if r["checks"]["target"]!=a["checks"]["target"]: print(f"- {k[0]}-{k[1]} 「{r['text']}」 소넷 {a['picks']} → Jev 뒤 {r['picks']} | {'좋아짐' if r['checks']['target'] else '나빠짐'}")
print("\n## 애매 턴 — 소넷이 고른 것")
for r in so.values():
    if r["ambiguous"]: print(f"- {r['conv']}-{r['turn']} 「{r['text']}」 → {r['picks']} · {r['kind']}")
