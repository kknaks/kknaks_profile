"""지금 시스템 실행 — 앱 코드를 부르기만 한다(답 LLM 은 빈 답을 내는 가짜)."""
import asyncio, json, sys, time, os
from clinic_chat.config import load_settings
from clinic_chat.consult import prompt as prompt_mod
from clinic_chat.consult.ledger import Ledger, state_at_start
from clinic_chat.consult.render import Render
from clinic_chat.consult.turn import Ctx, run_turn
from clinic_chat.llm.chat import new_chat_result

from paths import RUN as SP, CONV
# usage: run_now.py <실행 이름> [대화,대화…] [--real-answer C56,C57,…] — 장부는 runs/<실행 이름>/turns.jsonl
# --real-answer: 그 대화들은 빈 답 가짜 대신 앱의 답 LLM(구독 CLI · 소넷 · --resume)을 실제로 부른다(SPEC-008 §8-1 · 11-18)
argv=list(sys.argv[1:]); real=set()
if "--real-answer" in argv:
    i=argv.index("--real-answer"); real=set(argv[i+1].split(",")); del argv[i:i+2]
RUN=argv[0]; only=set(argv[1].split(",")) if len(argv)>1 else None

class Fake:
    kind="fake"
    async def turn(self, conv, user_message, prompt, history):
        res=new_chat_result(); conv.state="open"; res["session_state"]="open"
        res["llm"].update({"kind":"fake","session_id":conv.session_id}); res["timing"]={"ttft_ms":0.0,"total_ms":0.0}
        return res

async def main():
    s=load_settings(chat_state="on", chat_dir=os.path.join(SP,RUN), chat_debug_panel="off")
    p0=prompt_mod.load(s.chat_prompt_path())
    ctx=Ctx(s, Ledger(s.chat_dir_path()), Render(p0.steps, panel=False, slots=p0.slots), Fake())
    fake=ctx.llm; live=None
    if real:
        from clinic_chat.llm.chat_cli import ChatCli, ChatCliSpec
        live=ChatCli(ChatCliSpec.from_settings(s))
    done=set()
    wall=os.path.join(SP,RUN,"wall.jsonl")
    if os.path.exists(wall):
        done={json.loads(l)["conv"] for l in open(wall) if json.loads(l).get("end")}
    for line in open(CONV,encoding="utf-8"):
        c=json.loads(line)
        if (only and c["conv"] not in only) or c["conv"] in done: continue
        ctx.llm=live if c["conv"] in real else fake
        conv=ctx.ledger.new_conv(None, f"{c['conv']}-{RUN}")
        conv.prompt=prompt_mod.keep(s.chat_prompt_path(), s.chat_dir_path()); conv.prompt_sha=conv.prompt.sha256
        for t in c["turns"]:
            q=t["text"]; t0=time.perf_counter()
            n=ctx.ledger.start(conv, q, state_at_start(conv, s.chat_state))["turn"]
            err=None
            try:
                await run_turn(ctx, conv, n, q, lambda *_: None, clicked_at=t0)
            except Exception as e:
                err=f"{type(e).__name__}: {e}"[:300]
                if conv.running==n:
                    ctx.ledger.end(conv, {"turn":n,"question":q,"session_state":conv.chat.state,"error":{"kind":"internal","detail":err},"llm":{"answered":False}})
            with open(wall,"a") as f: f.write(json.dumps({"conv":c["conv"],"turn":n,"ms":round((time.perf_counter()-t0)*1000,1),"err":err})+"\n")
            print(c["conv"], n, round((time.perf_counter()-t0)*1000), err or "", flush=True)
        with open(wall,"a") as f: f.write(json.dumps({"conv":c["conv"],"end":True})+"\n")

asyncio.run(main())
