"""게이트 6 사람 결정 페이지 — 8차 게이트(out/gate/batch6.json) 기준 71자리.

브리프: ../gate6-page-brief.md (2026-11-06).
화면 꼴·db 저장(answers/<docId> · docId = encodeURIComponent(id) 의 % → _)·내보내기 상자·스크립트 구조는
dryrun3/_ref_gen_gate6_dryrun3.py 그대로. 데이터만 8차.

입력: out/gate/batch6.json · ../decisions-batch6b-dup-classification.json · dryrun3/_ref_silver-gate-6.html(⑦ 힌트·Q-synonym 문구)
      · out/entities/adverse_effect.jsonl(R1 후보가 붙어 있던 사건 노드) · ../bronze/phub-ledger(3판 · Q-timeline-co2 근거)
산출: out/gate/batch6-page.html · out/gate/batch6-page-slots.json
실행: python3 -m lib.gate6page   (silver-v3 에서)
"""
import json, os, re, html
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # silver-v3
WORK = os.path.dirname(HERE)
GATE = os.path.join(HERE, "out", "gate", "batch6.json")
CLS = os.path.join(WORK, "decisions-batch6b-dup-classification.json")
REF = os.path.join(HERE, "dryrun3", "_ref_silver-gate-6.html")
AE = os.path.join(HERE, "out", "entities", "adverse_effect.jsonl")
BRONZE = os.path.join(WORK, "bronze", "phub-ledger")
OUT_HTML = os.path.join(HERE, "out", "gate", "batch6-page.html")
OUT_SLOTS = os.path.join(HERE, "out", "gate", "batch6-page-slots.json")
BUILDER_BUG = frozenset(("처짐", "밑 처짐"))  # 분석기가 「턱밑」을 쪼갠 빌더 버그 — 9차에서 고침 · 자리로 안 올림

G = {b["id"]: b for b in json.load(open(GATE, encoding="utf-8"))}
C = json.load(open(CLS, encoding="utf-8"))
CLS_BY = {frozenset((p["a"], p["b"])): p for p in C["pairs"]}

# 이전 페이지 자리(⑦ 힌트 · Q-synonym 문구를 그대로 가져온다)
_m = re.search(r'<script type="application/json" id="slots">(.*?)</script>', open(REF, encoding="utf-8").read(), re.S)
REF_SLOTS = {x["id"]: x for x in json.loads(_m.group(1).replace("<\\/", "</"))}

slots = []


def add(sec, id, title, sub, opts, ev=None, free=None, note=None):
    slots.append({"sec": sec, "id": id, "title": title, "sub": sub, "opts": opts, "ev": [e for e in (ev or []) if e[1]], "free": free, "note": note})


def texts_by_note(ev, key):
    out = []
    for e in ev:
        if key in (e.get("note") or "") and e["text"] not in out:
            out.append(e["text"])
    return out


def rec_note(s):
    if s.get("recommended"):
        lab = next((o["label"] for o in s["options"] if o.get("key") == s["recommended"]), s["recommended"])
        return f"추천 {lab} — {s.get('recommend_reason') or ''}".rstrip(" —")
    return None


# ---------------------------------------------------------------- 질문 2
syn = REF_SLOTS["Q-synonym"]
n_new = len(G["ledger-nodes"]["subitems"])
add("Q", "Q-synonym", syn["title"], syn["sub"].replace("새 노드 179", f"새 노드 {n_new}"), [tuple(o) for o in syn["opts"]])


def _find(obj, target, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _find(v, target, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _find(v, target, f"{path}[{i}]")
    elif obj == target:
        yield path


co2_ev = []
for f, t in [("post-procedure-timeline.json", "프락셔널 CO2 레이저"), ("procedure-comparison.json", "CO2 프랙셔널 레이저"),
             ("treatment-optimization.json", "프락셔널 CO2(피부결)"), ("treatment-sequence.json", "프락셔널 CO2")]:
    d = json.load(open(os.path.join(BRONZE, f), encoding="utf-8"))
    paths = list(_find(d, t))
    assert paths, (f, t)
    for p in paths:
        co2_ev.append((f"{f}{p}", f"「{t}」" + (" — 이 자리를 묻는다" if f.startswith("post-") else " — 4판에서 「CO2프락셔널」로 고친다(사용자 결정)")))
assert sum(1 for k, _ in co2_ev if k.startswith("post-")) == 1 and len(co2_ev) == 5, co2_ev
add("Q", "Q-timeline-co2", "post-procedure-timeline 의 타임라인 이름 「프락셔널 CO2 레이저」(1곳)도 4판에서 「CO2프락셔널 레이저」로 고칠까?",
    "4판에서 시술 라벨 4곳(procedure-comparison 「CO2 프랙셔널 레이저」 · treatment-optimization 「프락셔널 CO2(피부결)」 · treatment-sequence 「프락셔널 CO2」×2)은 사용자 결정으로 「CO2프락셔널」로 고친다. 원장 3판 위치는 아래.",
    [("fix", "고친다"), ("keep", "그대로(타임라인 이름은 설명이라 둔다)")], co2_ev)

# ---------------------------------------------------------------- ⑦ 접기 — user_pending 5
closed, bug, pending = [], [], []
for s in G["dup-strong"]["subitems"]:
    a, b = s["pair"]["node"], s["pair"]["other"]
    k = frozenset((a, b))
    if k == BUILDER_BUG:
        bug.append(s); continue
    p = CLS_BY.get(k)
    assert p, ("분류 파일에 없는 쌍", a, b)
    (pending if p["verdict"] == "user_pending" else closed).append((s, p))
assert len(pending) == 5, len(pending)
for s, p in pending:
    a, b = s["pair"]["node"], s["pair"]["other"]
    ref = REF_SLOTS.get(f"DUP|{a}|{b}") or REF_SLOTS.get(f"DUP|{b}|{a}")
    hint = next((e[1] for e in ref["ev"] if e[0] == "왜 사람이 보나"), None) if ref else None
    ev = [(f"「{a}」 예", " / ".join(texts_by_note(s["evidence"], f"「{a}」 원문 예")[:3])),
          (f"「{b}」 예", " / ".join(texts_by_note(s["evidence"], f"「{b}」 원문 예")[:3])),
          ("원장 자리", s["why"].split(" · 규칙")[0]),
          ("왜 사람이 보나", hint)]
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    add("DUP", f"DUP|{a}|{b}", f"{a} ↔ {b}", "규칙 " + ", ".join(s["pair"]["rules"]) + f" · 게이트 {s['id']}",
        [("same", f"같은 사건 — 「{short}」로, 붙은 말은 속성(정도·조건·경과·부위)으로 분해"), ("diff", "다른 사건 — 둘 다 노드"), ("long", f"긴 쪽 「{long_}」이 사건 — 짧은 쪽은 조각")],
        ev, free="다른 이름으로 접을 때 그 이름", note=rec_note(s))

# ---------------------------------------------------------------- 애매 13
cls_by_node = defaultdict(list)
for p in C["pairs"]:
    cls_by_node[p["a"]].append(p); cls_by_node[p["b"]].append(p)
VERD = {"same_decompose": "같은 사건", "different": "다른 사건", "fragment_not_node": "둘 다 노드 아님", "user_pending": "사용자 판단(이 페이지 ⑦)"}
for s in G["ambiguous"]["subitems"]:
    texts = [e["text"] for e in s["evidence"]]
    if s.get("node"):
        nd = s["node"]
        folds = [o["key"].split(":", 1)[1] for o in s["options"] if (o.get("key") or "").startswith("fold:")]
        rel = " · ".join(f"「{p['a']} ↔ {p['b']}」 {VERD[p['verdict']]}" + (f" → 「{p['keep']}」" if p.get("keep") else "") for p in cls_by_node.get(nd["canonical"], []))
        ev = [("원문 예", " / ".join(dict.fromkeys(texts))), ("게이트 접기 후보", "·".join(folds)), ("⑦ 분류", rel)]
        add("AMB", f"AMB|{nd['canonical']}", f"{nd['canonical']} (원장 {len(nd['locators'])}회)", s["why"].split(" · 애매: ", 1)[-1],
            [("keep", "노드로 둔다"), ("other", "다른 노드와 같다 → 이름 적기"), ("memo", "부작용 아님(메모·설명문)")], ev, free="같다고 보는 노드 이름", note=rec_note(s))
    else:
        amb = " · ".join(a for sg in s["segments"] for a in sg["amb"])
        ev = [("원문", " / ".join(dict.fromkeys(texts))), ("왜 애매", amb or s["why"]), ("locator", " · ".join(s["locators"]))]
        add("AMB", f"AMB|{s['raw_variants'][0]}", f"문구 「{s['raw_variants'][0]}」", s["why"],
            [("keep", "노드로 둔다"), ("other", "다른 노드와 같다 → 이름 적기"), ("memo", "부작용 아님(메모·설명문)")], ev, free="같다고 보는 노드 이름", note=rec_note(s))

# ---------------------------------------------------------------- 문장꼴 11
for s in G["sentence-b"]["subitems"]:
    t = s["raw_variants"][0]
    ev = [("원문", " / ".join(dict.fromkeys(e["text"] for e in s["evidence"]))), ("locator", " · ".join(s["locators"])),
          ("분석기 토막", " · ".join(f"{sg['segment']}({sg['kind']})" for sg in s["segments"])), ("왜 문장꼴", s["why"])]
    add("T2B", f"T2B|{t}", f"「{t}」", "행선지 힌트(추천 아님): " + ("·".join(s["hint"]) or "—"),
        [("desc", "설명문으로 둔다(노드 없음)"), ("timeline", "타임라인 줄로"), ("event", "사건 지정 → 이름 적기")], ev, free="사건 이름(사전 값 또는 새 노드)", note=rec_note(s))

# ---------------------------------------------------------------- 폐색/색전 3
for s in G["occlusion-embolism"]["subitems"]:
    t = s["evidence"][0]["text"]
    add("N5", f"N5|{s['locator']}", f"「{t}」", f"locator {s['locator']} · 지금 사건: {'·'.join(s['events'])} · {s['why']}",
        [("both", "두 사건 모두(현재)"), ("occl", "폐색만"), ("emb", "색전만")], [("게이트", s["recommend_reason"])], note=rec_note(s))

# ---------------------------------------------------------------- R30 2
for s in G["r30-candidates"]["subitems"]:
    ev = [(f"원문 {i+1}" + (" · 인과 표지" if r["causal_marker"] else ""), f"{r['text']}  ({r['locator']})") for i, r in enumerate(s["rows"])]
    eff = next((o["effect"] for o in s["options"] if o.get("key") == "approve"), "")
    ev.append(("연결하면", eff))
    add("R30", f"R30|{s['pair']}", f"{s['pair']} 로 이을까? (leads_to)", f"{s['why']} · {s['recommend_reason']}",
        [("approve", "연결한다(edge_create)"), ("no", "안 한다")], ev, note=rec_note(s))

# ---------------------------------------------------------------- 묶음3 15
for s in G["batch3"]["subitems"]:
    ev = [(e["file"], e["text"]) for e in s["evidence"]]
    add("B3", f"B3|{s['id']}", s["title"], s.get("why") or "", [(o.get("key") or o["label"], o["label"]) for o in s["options"]], ev,
        note=(f"추천 {s['recommended']} — {s['recommend_reason']}" if s.get("recommended") else None))

# ---------------------------------------------------------------- R1 수식어 후보 20
by_loc = defaultdict(set)
for line in open(AE, encoding="utf-8"):
    r = json.loads(line); a = r["attrs"]
    evn = a["event"][0]["value"] if a.get("event") else None
    for e in (a.get("explanations") or [{"value": []}])[0]["value"]:
        if evn:
            by_loc[e["locator"]].add(evn)
for s in G["r1-candidates"]["subitems"]:
    nodes = sorted({n for lc in s["locators"] for n in by_loc.get(lc, ())})
    ev = [("원문 예", s["evidence"][0]["text"]), ("붙어 있던 노드", "·".join(nodes) or "— (같은 자리에 사건 노드 없음)"), ("자리", " · ".join(s["locators"]))]
    add("R1", f"R1|{s['word']}", f"「{s['word']}」 (원장 {s['n']}회)", s["why"],
        [("modifier", "수식어로 둔다(사건에서 떼어 속성으로)"), ("part", "사건 이름의 일부(떼지 않음)")], ev, note=rec_note(s))

# ---------------------------------------------------------------- 세기
secs = [("Q", "원칙 질문"), ("DUP", "⑦ 접기 — 임상 판단 남은 쌍"), ("AMB", "애매 — 분석기가 확신 못 한 노드·문구"), ("T2B", "문장꼴 — 절이 있고 사전 사건이 없는 문구"),
        ("N5", "폐색 / 색전 한 문구"), ("R30", "R30 연결 후보"), ("B3", "묶음 3 미결"), ("R1", "R1 수식어 후보")]
EXPECT = {"Q": 2, "DUP": 5, "AMB": 13, "T2B": 11, "N5": 3, "R30": 2, "B3": 15, "R1": 20}
counts = {s: sum(1 for x in slots if x["sec"] == s) for s, _ in secs}
ids = [x["id"] for x in slots]
assert len(ids) == len(set(ids)), "자리 id 중복"
for s, t in secs:
    print(f"{s:4} {t:28} {counts[s]:3}  (브리프 {EXPECT[s]})")
print("합계", len(slots))
assert counts == EXPECT and len(slots) == 71, counts

# ---------------------------------------------------------------- 닫힌 ⑦ 요약
def verdict_text(p):
    v = p["verdict"]
    if v == "same_decompose":
        return f"같은 사건 → 「{p['keep']}」" + (f" · {p['attr_route']}" if p.get("attr_route") else "")
    return {"different": "다른 사건(둘 다 노드)", "fragment_not_node": "둘 다 노드 아님(조각·설명문)"}[v]

closed.sort(key=lambda sp: sp[1]["n"])
nv = defaultdict(int)
for _, p in closed:
    nv[p["verdict"]] += 1
rows = "".join(f"<tr><td>{html.escape(s['pair']['node'])} ↔ {html.escape(s['pair']['other'])}</td><td>{html.escape(verdict_text(p))}</td></tr>" for s, p in closed)
gate_keys = {frozenset((s["pair"]["node"], s["pair"]["other"])) for s in G["dup-strong"]["subitems"]}
off_gate = [p for p in C["pairs"] if frozenset((p["a"], p["b"])) not in gate_keys]
extra = " ".join(f"분류 #{p['n']} 「{html.escape(p['a'])} ↔ {html.escape(p['b'])}」({html.escape(verdict_text(p))})는 8차 게이트에 쌍으로 없다." for p in off_gate)
bug_txt = "".join(f" 게이트 「{html.escape(s['pair']['node'])} ↔ {html.escape(s['pair']['other'])}」({s['id']})는 분석기가 「턱밑」을 쪼갠 빌더 버그라 자리로 올리지 않는다(9차에서 고침)." for s in bug)
summary_html = (f'<details class="card" style="margin-top:14px"><summary style="cursor:pointer;font-weight:500">⑦ 접기 — 사용자 승인으로 닫힌 {len(closed)}쌍 '
                f'(같은 사건 {nv["same_decompose"]} · 다른 사건 {nv["different"]} · 노드 아님 {nv["fragment_not_node"]}) 펼치기</summary>'
                f'<div style="overflow-x:auto;margin-top:8px"><table style="font-size:13px;border-collapse:collapse;width:100%">{rows}</table></div>'
                f'<p class="sub" style="margin-top:8px">사용자 말: 「{html.escape(C["user_words"])}」({C["decided_at"]}). 결정 파일은 8차 뒤 batch6b. {extra}{bug_txt}</p></details>')
intro = ("8차 게이트(out/gate/batch6.json · ERD v3.3) 뒤 사람이 고를 자리만 남겼다. 새 노드 목록·「Mxx-」 접두 34(원장 꼴 유지 · 사용자 결정 11-06)·승인된 ⑦ 쌍은 자리로 올리지 않는다. "
         "원문은 브론즈 3판 locator. 고른 값은 저장소(answers/&lt;id&gt;)에 바로 저장되고, 저장소가 없으면 아래 내보내기 상자로 복사해 전달한다.")

data = json.dumps(slots, ensure_ascii=False).replace("</", "<\\/")
page = f'''<title>실버 결정 묶음 6</title>
<style>
/* layout: 한 열 · 섹션 머리 고정 · 자리마다 카드 하나 · 상단 진행 바 */
:root{{--bg:#f6f4ef;--fg:#1d1b17;--mute:#6d675c;--line:#d9d3c7;--card:#fffdf8;--acc:#1f5e5a;--acc-fg:#ffffff;--warn:#9a5a12;--ok:#2e6b3a;--chip:#ece7dc;
--f-body:"Noto Sans KR",system-ui,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#17160f;--fg:#ece8df;--mute:#a39c8e;--line:#3a372e;--card:#1f1e16;--acc:#6fc2bb;--acc-fg:#0e1a19;--warn:#e0a35a;--ok:#8fd19b;--chip:#2a2820;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#17160f;--fg:#ece8df;--mute:#a39c8e;--line:#3a372e;--card:#1f1e16;--acc:#6fc2bb;--acc-fg:#0e1a19;--warn:#e0a35a;--ok:#8fd19b;--chip:#2a2820;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 var(--f-body);padding-inline:16px;padding-block:0 48px}}
.wrap{{max-width:860px;margin:0 auto}}
header.top{{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);z-index:5;padding-block:12px 8px;border-bottom:1px solid var(--line)}}
header.top h1{{font-size:20px;margin:0 0 4px;text-wrap:balance}}
.prog{{display:flex;gap:12px;align-items:center;font-size:13px;color:var(--mute);flex-wrap:wrap}}
.bar{{flex:1 1 160px;height:6px;background:var(--chip);border-radius:3px;overflow:hidden;min-width:0}}
.bar>i{{display:block;height:100%;background:var(--acc);width:0}}
.store{{font-family:var(--f-mono);font-size:12px}}
nav.secs{{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}}
nav.secs a{{font-size:12px;padding:3px 9px;border:1px solid var(--line);border-radius:14px;color:var(--fg);text-decoration:none;background:var(--card)}}
h2{{font-size:16px;margin:28px 0 10px;display:flex;gap:10px;align-items:baseline}}
h2 small{{color:var(--mute);font-weight:400;font-size:13px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-bottom:10px}}
.card.done{{border-color:var(--ok)}}
.card h3{{font-size:15px;margin:0 0 4px;text-wrap:balance}}
.sub{{color:var(--mute);font-size:13px;margin:0 0 8px}}
.ev{{font-size:13px;margin:6px 0 10px;padding:8px 10px;background:var(--chip);border-radius:6px;display:grid;grid-template-columns:max-content 1fr;gap:3px 10px}}
.ev b{{font-weight:500;color:var(--mute);white-space:nowrap}}
.ev span{{min-width:0;overflow-wrap:anywhere}}
.opts{{display:flex;flex-wrap:wrap;gap:6px}}
.opts label{{border:1px solid var(--line);border-radius:6px;padding:5px 10px;font-size:14px;cursor:pointer;background:var(--bg)}}
.opts label:has(input:checked){{background:var(--acc);color:var(--acc-fg);border-color:var(--acc)}}
.opts input{{position:absolute;opacity:0;width:0;height:0}}
.opts label:has(input:focus-visible){{outline:2px solid var(--acc);outline-offset:2px}}
.free{{margin-top:8px}} .free input{{width:100%;max-width:420px;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit}}
.note{{font-size:12px;color:var(--warn);margin-top:6px}}
.id{{font-family:var(--f-mono);font-size:11px;color:var(--mute);margin-top:6px;overflow-wrap:anywhere}}
.foot{{margin-top:32px;padding-top:16px;border-top:1px solid var(--line)}}
.foot textarea{{width:100%;min-height:120px;font:12px var(--f-mono);background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px}}
button{{font:inherit;padding:7px 14px;border-radius:6px;border:1px solid var(--acc);background:var(--acc);color:var(--acc-fg);cursor:pointer}}
button.ghost{{background:transparent;color:var(--fg);border-color:var(--line)}}
@media (prefers-reduced-motion:no-preference){{.bar>i{{transition:width .25s}}}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<div class="wrap">
<header class="top">
<h1>실버 결정 묶음 6 — 남은 {len(slots)}자리</h1>
<div class="prog"><span id="cnt">0 / {len(slots)}</span><div class="bar"><i id="barfill"></i></div><span class="store" id="store">저장소 연결 중…</span></div>
<nav class="secs">{''.join(f'<a href="#{s}">{t} {counts[s]}</a>' for s,t in secs)}</nav>
</header>
<p class="sub" style="margin-top:12px">{intro}</p>
{summary_html}
<div id="root"></div>
<div class="foot"><h2>내보내기 <small>저장소가 안 되면 이 JSON 을 복사해 전달</small></h2>
<div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap"><button id="copy">JSON 복사</button><button class="ghost" id="refresh">저장소에서 다시 읽기</button></div>
<textarea id="out" readonly></textarea></div>
</div>
<script type="application/json" id="slots">{data}</script>
<script>
(function(){{
const SLOTS=JSON.parse(document.getElementById('slots').textContent);
const SECS={json.dumps([[s,t] for s,t in secs],ensure_ascii=False)};
const answers={{}};
const docId=id=>encodeURIComponent(id).replace(/%/g,'_');
const root=document.getElementById('root');
function esc(s){{return String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]))}}
function render(){{
  root.innerHTML=SECS.map(([s,t])=>{{
    const items=SLOTS.filter(x=>x.sec===s);
    return `<h2 id="${{s}}">${{esc(t)}} <small>${{items.length}}자리</small></h2>`+items.map(card).join('');
  }}).join('');
  updateCount();
}}
function card(x){{
  const a=answers[x.id]||{{}};
  const ev=x.ev.filter(e=>e[1]).map(e=>`<b>${{esc(e[0])}}</b><span>${{esc(e[1])}}</span>`).join('');
  return `<div class="card ${{a.choice?'done':''}}" data-id="${{esc(x.id)}}">
  <h3>${{esc(x.title)}}</h3>${{x.sub?`<p class="sub">${{esc(x.sub)}}</p>`:''}}
  ${{ev?`<div class="ev">${{ev}}</div>`:''}}
  <div class="opts">${{x.opts.map(o=>`<label><input type="radio" name="r_${{docId(x.id)}}" value="${{esc(o[0])}}" ${{a.choice===o[0]?'checked':''}}>${{esc(o[1])}}</label>`).join('')}}</div>
  ${{x.free?`<div class="free"><input id="f_${{docId(x.id)}}" placeholder="${{esc(x.free)}}" value="${{esc(a.text||'')}}"></div>`:''}}
  ${{x.note?`<div class="note">${{esc(x.note)}}</div>`:''}}
  <div class="id">${{esc(x.id)}}</div></div>`;
}}
function updateCount(){{
  const n=Object.values(answers).filter(a=>a&&a.choice).length;
  document.getElementById('cnt').textContent=n+' / '+SLOTS.length;
  document.getElementById('barfill').style.width=(100*n/SLOTS.length)+'%';
  document.getElementById('out').value=JSON.stringify(answers,null,1);
}}
let db=null;
async function connect(){{
  for(let i=0;i<3;i++){{ try{{ db=await claude.use('db'); if(db) break; }}catch(e){{}} await new Promise(r=>setTimeout(r,800)); }}
  const st=document.getElementById('store');
  if(!db){{ st.textContent='저장소 없음 — 아래 JSON 으로 전달'; return; }}
  st.textContent='저장소 연결됨';
  await load();
}}
async function load(){{
  if(!db) return;
  try{{ const snap=await db.collection('answers').get(); (snap.docs||[]).forEach(d=>{{const v=d.data(); if(v&&v.id) answers[v.id]=v;}}); render(); document.getElementById('store').textContent='저장소 연결됨 · '+Object.keys(answers).length+'건'; }}
  catch(e){{ document.getElementById('store').textContent='저장소 읽기 실패: '+(e.code||e.message||e); }}
}}
async function save(id){{
  const a=answers[id]; if(!db) return;
  try{{ await db.collection('answers').doc(docId(id)).set(a); document.getElementById('store').textContent='저장됨 · '+Object.values(answers).filter(x=>x.choice).length+'건'; }}
  catch(e){{ document.getElementById('store').textContent='저장 실패: '+(e.code||e.message||e); }}
}}
root.addEventListener('change',e=>{{
  const card=e.target.closest('.card'); if(!card) return; const id=card.dataset.id;
  const x=SLOTS.find(s=>s.id===id); const a=answers[id]||(answers[id]={{id,sec:x.sec}});
  if(e.target.type==='radio'){{ a.choice=e.target.value; card.classList.add('done'); }}
  if(e.target.tagName==='INPUT'&&e.target.type==='text'||e.target.id.startsWith('f_')){{ a.text=e.target.value; }}
  a.at=new Date().toISOString(); updateCount(); save(id);
}});
document.getElementById('copy').addEventListener('click',async()=>{{ const t=document.getElementById('out'); try{{await navigator.clipboard.writeText(t.value);}}catch(e){{t.focus();t.select();}} }});
document.getElementById('refresh').addEventListener('click',load);
render(); connect();
}})();
</script>'''

open(OUT_HTML, "w", encoding="utf-8").write(page)
json.dump({"source": "out/gate/batch6.json", "brief": "gate6-page-brief.md", "counts": counts, "total": len(slots), "slots": slots}, open(OUT_SLOTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", OUT_HTML, len(page))
print("written", OUT_SLOTS)
