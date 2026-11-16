import json,html
S="/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/f4798840-05cc-4695-94d0-decfad37f126/scratchpad"
g=json.load(open(S+'/gate6-data.json'))
slots=[]
def add(sec,id,title,sub,opts,ev=None,free=None,note=None):
    slots.append({'sec':sec,'id':id,'title':title,'sub':sub,'opts':opts,'ev':ev or [],'free':free,'note':note})
# Q 질문 2
add('Q','Q-prefix','synergy 의 「Mxx-」 접두 34종(171자리)도 떼어 통일할까?','3판에서 18종은 뗐다. 「M1-보톡스」「M2-필러」「M11-포텐자」 등 34종은 이름이 taxonomy 와 같아 그대로 두었다. README 3판 규칙은 「접두 금지」.',[('strip','전부 뗀다(4판에 포함)'),('keep','그대로 둔다(규칙에 예외 명시)')])
add('Q','Q-synonym','글자가 다른 같은 뜻(홍조↔홍반 · 실 촉감↔실 촉지감↔스레드 촉지감 · 눈꺼풀 처짐↔안검하수)을 지금 짝지을까?','기계가 못 잡는 영역. 지금 하면 새 노드 179 목록을 훑으며 적어야 한다.',[('later','나중에(골드에서 눈에 띄는 것부터)'),('now','지금 한다 — 목록 페이지를 따로 만든다')])
# ⑦ 사용자 판단 5 (31쌍은 사용자 승인으로 닫힘 · 아래 요약)
for p in g['dup']:
    ev=[('「%s」 예'%p['a'],p['ex_a']),('「%s」 예'%p['b'],p['ex_b']),('왜 사람이 보나',p.get('hint'))]
    short,long_=(p['a'],p['b']) if len(p['a'])<=len(p['b']) else (p['b'],p['a'])
    add('DUP','DUP|%s|%s'%(p['a'],p['b']),'%s ↔ %s'%(p['a'],p['b']),'규칙 %s'%', '.join(p['rules']),[('same','같은 사건 — 「%s」로, 붙은 말은 속성(정도·조건·경과·부위)으로 분해'%short),('diff','다른 사건 — 둘 다 노드'),('long','긴 쪽 「%s」이 사건 — 짧은 쪽은 조각'%long_)],ev,free='다른 이름으로 접을 때 그 이름')
# 애매 21 + 붙은 사전값 2
for a in g['amb']:
    ev=[('원문 예',a.get('example'))]
    if a.get('partners'): ev.append(('접기 후보','·'.join(a['partners'])))
    add('AMB','AMB|%s'%a['node'],'%s (원장 %s회)'%(a['node'],a.get('n')),a.get('why') or '',[('keep','노드로 둔다'),('other','다른 노드와 같다 → 이름 적기'),('memo','부작용 아님(메모·설명문)')],ev,free='같다고 보는 노드 이름')
for x in g['n3_amb']:
    add('AMB','N3|%s'%x['value'],'사전 값 「%s」 분해?'%x['value'],x['why'],[('split','분해 — 사건 「%s」 + 부위 「%s」'%(x['value'].replace('정맥','').replace('혈관',''),'정맥' if '정맥' in x['value'] else '혈관')),('keep','통째로 둔다')])
# 문장꼴 15
for t in g['t2b']:
    ev=[('7차 핵심어',str(t.get('core7'))),('왜 문장꼴',t.get('why')),('명사',t.get('nouns'))]
    add('T2B','T2B|%s'%t['text'],'「%s」'%t['text'],'제안: %s'%(t.get('suggest') or ''),[('desc','설명문으로 둔다(노드 없음)'),('timeline','타임라인 줄로'),('event','사건 지정 → 이름 적기')],ev,free='사건 이름(사전 값 또는 새 노드)')
# 폐색/색전 3
for x in g['n5']:
    add('N5','N5|%s'%x['locator'],'「%s」'%x['text'],'locator %s · 3차 붙은 사건: %s'%(x['locator'],'·'.join(x['events'])),[('both','두 사건 모두(현재)'),('occl','폐색만'),('emb','색전만')])
# 묶음3 15
for b in g['b3']:
    ev=[(e['file'],e['text']) for e in b['evidence']]
    opts=[(o['key'] or o['label'],o['label']) for o in b['options']]
    add('B3','B3|%s'%b['id'],b['title'],b.get('why') or '',opts,ev,note=('추천 %s'%b['recommended']) if b.get('recommended') else None)
secs=[('Q','원칙 질문',2),('DUP','⑦ 접기 — 임상 판단 남은 쌍',None),('AMB','애매 — 분석기가 확신 못 한 노드·사전 값',None),('T2B','문장꼴 — 절이 있고 사전 사건이 없는 문구',None),('N5','폐색 / 색전 한 문구',None),('B3','묶음 3 미결',None)]
counts={s:sum(1 for x in slots if x['sec']==s) for s,_,_ in secs}
print('slots',len(slots),counts)
data=json.dumps(slots,ensure_ascii=False).replace('</','<\\/')
page=f'''<title>실버 결정 묶음 6</title>
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
<nav class="secs">{''.join(f'<a href="#{s}">{t} {counts[s]}</a>' for s,t,_ in secs)}</nav>
</header>
<p class="sub" style="margin-top:12px">3차 드라이런(형태소 분석기 · 규칙 R1~R4 · N1~N5 · ~감·증·형성 같다) 뒤 사람이 고를 자리만 남겼다. 원문은 브론즈 3판 locator. 고른 값은 저장소(answers/&lt;id&gt;)에 바로 저장되고, 저장소가 없으면 아래 내보내기 상자로 복사해 전달한다.</p>
<details class="card" style="margin-top:14px"><summary style="cursor:pointer;font-weight:500">⑦ 접기 — 사용자 승인으로 닫힌 34쌍 (같은 사건 19 · 다른 사건 5 · 노드 아님 10) 펼치기</summary><div style="overflow-x:auto;margin-top:8px"><table style="font-size:13px;border-collapse:collapse;width:100%"><tr><td>손상 ↔ 깊이 손상</td><td>같은 사건 → 「손상」 · 깊이→정도 · 진피→부위 · 과도한 깊이 설정→조건</td></tr><tr><td>손상 ↔ 표정 손상</td><td>다른 사건(둘 다 노드)</td></tr><tr><td>반응 ↔ 알레르기 반응</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>알레르기 반응 ↔ 알레르기</td><td>같은 사건 → 「알레르기 반응」 · 줄임 표기</td></tr><tr><td>흉터 ↔ 흉터 악화</td><td>같은 사건 → 「흉터」 · 악화→경과</td></tr><tr><td>각질 ↔ 필링 각질</td><td>같은 사건 → 「각질」 · 「필링 후」→조건</td></tr><tr><td>약화 ↔ 근력 약화</td><td>같은 사건 → 「근력 약화」 · 근력/근육→대상</td></tr><tr><td>근육통 ↔ 근육통 유사 감각</td><td>같은 사건 → 「근육통」 · 환자 표현(운동 후와 비슷한 느낌)</td></tr><tr><td>출혈 ↔ 점상 출혈</td><td>같은 사건 → 「출혈」 · 점상→양상</td></tr><tr><td>박피 ↔ 박리</td><td>다른 사건(둘 다 노드)</td></tr><tr><td>자국 ↔ 자극</td><td>다른 사건(둘 다 노드)</td></tr><tr><td>출혈 ↔ 충혈</td><td>다른 사건(둘 다 노드)</td></tr><tr><td>염증 반응 ↔ 염증</td><td>같은 사건 → 「염증」 · 반응은 조각</td></tr><tr><td>메스꺼움 ↔ 미량원소 과잉 메스꺼움</td><td>같은 사건 → 「메스꺼움」 · 「미량원소 과잉 시」→조건</td></tr><tr><td>반응 ↔ 염증 반응</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>자극 ↔ 부위 자극</td><td>같은 사건 → 「자극」 · 「도포 부위」→상대 부위</td></tr><tr><td>처짐 ↔ 턱밑 처짐</td><td>같은 사건 → 「처짐」 · 턱밑→부위</td></tr><tr><td>필링 ↔ 필링 각질</td><td>다른 사건(둘 다 노드)</td></tr><tr><td>약화 ↔ 약화 확산</td><td>같은 사건 → 「근력 약화」 · 확산→양상</td></tr><tr><td>염증 반응 ↔ 이상 염증반응</td><td>같은 사건 → 「염증」 · 이상→정도</td></tr><tr><td>감각 ↔ 근육통 유사 감각</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>감각 ↔ 마늘 냄새 감각</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>감각 변화 ↔ 감각</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>광과민성 ↔ 광과민성 반응</td><td>같은 사건 → 「광과민성」 · 반응은 조각</td></tr><tr><td>반응 ↔ 이물질 반응</td><td>같은 사건 → 「이물반응」 · 사전 「이물반응」 표기 변형</td></tr><tr><td>반응 ↔ 광과민성 반응</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>반응 ↔ 면역 반응</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>알레르기 ↔ 화학적 차단제 알레르기</td><td>같은 사건 → 「알레르기 반응」 · 「화학적 차단제」→조건(물질)</td></tr><tr><td>증식 ↔ 세포 증식 변이</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>최소 반응성 ↔ 최소</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>혈관계 합병증 ↔ 합병증</td><td>둘 다 노드 아님(조각·설명문)</td></tr><tr><td>가려움증 ↔ 소양감</td><td>같은 사건 → 「소양감」 · 한자어/우리말</td></tr><tr><td>저림감 ↔ 감각 이상</td><td>같은 사건 → 「감각 이상」 · 사전 동의어 저림</td></tr><tr><td>압통감 ↔ 통증</td><td>같은 사건 → 「통증」 · 사전 동의어 압통</td></tr></table></div><p class="sub" style="margin-top:8px">사용자 말: 「36쌍 분류는 그렇게 가면 될거 같아」(2026-11-06). 결정 파일은 8차 뒤 batch6b.</p></details>
<div id="root"></div>
<div class="foot"><h2>내보내기 <small>저장소가 안 되면 이 JSON 을 복사해 전달</small></h2>
<div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap"><button id="copy">JSON 복사</button><button class="ghost" id="refresh">저장소에서 다시 읽기</button></div>
<textarea id="out" readonly></textarea></div>
</div>
<script type="application/json" id="slots">{data}</script>
<script>
(function(){{
const SLOTS=JSON.parse(document.getElementById('slots').textContent);
const SECS={json.dumps([[s,t] for s,t,_ in secs],ensure_ascii=False)};
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
open(S+'/silver-gate-6.html','w').write(page)
print('written',len(page))

