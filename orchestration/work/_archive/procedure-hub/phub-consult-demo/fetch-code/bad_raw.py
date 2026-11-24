"""JSON 깨짐 턴 다시 불러 원문 보기(같은 앱 프롬프트) — replay54 의 표본 · 밖 모음에서 conv:turn 만."""
import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import replay54 as R

async def main(keys):
    from clinic_chat.clients.hub_rest import HubRest
    from clinic_chat.config import load_settings
    from clinic_chat.consult import entry_list as el_mod, understand as und
    md = R.common.md_sets()
    ts = [t for t in R.M.load_turns(md) + R.run4.outside_turns(md) if f"{t['conv'][:4]}:{t['turn']}" in keys]
    s = load_settings(); hub = HubRest(s.hub_rest_url, page_limit=s.hub_page_limit)
    el = await el_mod.load(hub, aliases=s.chat_pick_aliases == "on", cache=False)
    system = und.system_text(R.APP_PICK, el)
    for t in ts:
        prev = t["prev"]; obj = ((prev[-1].get("consult") or {}).get("after") or {}) if prev else {}
        msg = und.turn_message(prev, obj, t["row"]["question"], R.APP_PICK, s, el, topics=R.M_brief(prev, s))
        for i in range(int(sys.argv[2]) if len(sys.argv) > 2 else 1):
            raw = await und.call(s, system, msg)
            print("====", t["conv"][:4], t["turn"], i, repr(raw.output_raw))
asyncio.run(main(sys.argv[1].split(",")))
