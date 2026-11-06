import fs from 'fs';
const P = process.argv[2];
const src = fs.readFileSync(P, 'utf8');
const m = src.match(/<script type="text\/x-dc"[^>]*data-props="([^"]*)">([\s\S]*?)<\/script>/);
const props = JSON.parse(m[1].replace(/&quot;/g, '"').replace(/&amp;/g, '&'));
const tpl = src.slice(src.indexOf('<x-dc>'), src.indexOf('</x-dc>'));
globalThis.DCLogic = class { constructor(){ this.props={}; } setState(p){ this.state={...this.state,...(typeof p==='function'?p(this.state):p)}; } };
const timers=[]; globalThis.setTimeout=(f)=>{timers.push(f);return timers.length;}; globalThis.clearTimeout=()=>{};
const Component = new Function(m[2] + '\nreturn Component;')();
// bindings
const loops = {}; for (const x of tpl.matchAll(/<sc-for list="\{\{ ([\w.]+) \}\}" as="(\w+)"/g)) loops[x[2]] = x[1];
const binds = [...new Set([...tpl.matchAll(/\{\{ ([\w.]+) \}\}/g)].map(x => x[1]))].filter(b => !['true','false'].includes(b));
const get=(o,p)=>p.split('.').reduce((a,k)=>a==null?undefined:a[k],o);
function missing(v){ const out=[]; for (const b of binds){ const [h,...r]=b.split('.'); if (loops[h]){ const list=get(v,loops[h]) ?? (loops[loops[h].split('.')[0]] ? null : undefined); if(list===undefined){out.push(b+' (list '+loops[h]+')');continue;} 
  // nested loop list e.g. g.pays / g.lines: walk
  const lists = resolveList(v, h); for (const it of lists){ const val=r.length?get(it,r.join('.')):it; if(val===undefined) out.push(b);} } else if (get(v,b)===undefined) out.push(b);} return [...new Set(out)]; }
function resolveList(v, as){ const path=loops[as]; const [h,...r]=path.split('.'); if (loops[h]) return resolveList(v,h).flatMap(it=>get(it,r.join('.'))||[]); return get(v,path)||[]; }
const mk=(scene)=>{ const c=new Component(); c.props={scene}; c.componentDidMount(); return c; };
const brief=(c)=>{ const v=c.renderVals(); return { v, line: {
  view:c.state.view, month:v.monthLabel, title:v.title,
  sync: v.sync.cur?'이번달['+v.sync.pullLabel+(v.sync.pullOff?':off':'')+']':v.sync.closed?'확정·저장됨':'-', at: v.sync.at?v.sync.atText:'-', fresh: v.sync.fresh?v.sync.freshText:'', full: v.sync.full?(v.sync.fullOff?'전체다시(off)':'전체다시'):'-',
  tabs: v.isAgency? v.tabs.map(t=>(t.line!=='transparent'?'*':'')+t.name+'('+t.n+')').join(' '):'',
  chips: v.chips.map(c=>c.name+' '+c.value).join(' · '),
  per: v.isAll? v.perAgency.map(a=>a.name+' '+a.people+'/'+a.paid).join(' · '):'',
  st: v.st.on? v.st.title+(v.st.sub?' / '+v.st.sub:''):'',
  groups: v.groups.map(g=>g.at+' '+g.name+(g.flags.length?'['+g.flags.map(f=>f.text).join(',')+']':'')).join(' | '),
  missing: missing(v) } }; };
const res={};
for (const sc of props.scene.options){ const c=mk(sc); const {line}=brief(c); res[sc]=JSON.stringify(line); console.log('== '+sc); console.log(line); }
const uniq=new Set(Object.values(res)); console.log('scenes', props.scene.options.length, 'distinct', uniq.size);
// interactions
console.log('\n== 조작');
let c=mk('monthly'); let v=c.renderVals(); v.sync.pull(); console.log('pull →', brief(c).line.sync, '표 묶음', c.renderVals().groups.length); timers.pop()(); console.log('after →', brief(c).line.sync, brief(c).line.at, brief(c).line.fresh, '묶음', c.renderVals().groups.length);
c.renderVals().prev(); console.log('‹ →', brief(c).line.month, brief(c).line.sync, brief(c).line.at, '묶음', c.renderVals().groups.length);
c.renderVals().sync.fullGo(); console.log('전체 다시 →', brief(c).line.st, brief(c).line.full); timers.pop()(); console.log('after →', brief(c).line.at, '묶음', c.renderVals().groups.length);
c.renderVals().prev(); console.log('‹ →', brief(c).line.month, brief(c).line.st);
c.renderVals().prev(); console.log('‹ →', brief(c).line.month, brief(c).line.sync, brief(c).line.at);
c=mk('monthly'); c.renderVals().navs[1].go(); console.log('헤더 에이전트별 →', brief(c).line.tabs, brief(c).line.per);
c.renderVals().tabs[2].pick(); console.log('탭 B →', brief(c).line.tabs, brief(c).line.chips, brief(c).line.groups);
c.renderVals().perAgency; c=mk('agency-all'); c.renderVals().perAgency[2].pick(); console.log('칩 C →', brief(c).line.chips, brief(c).line.groups);
c=mk('agency-all'); c.renderVals().prev(); console.log('전체 9월 →', brief(c).line.tabs, brief(c).line.per);
c=mk('monthly-error'); console.log('error sync', brief(c).line.sync, brief(c).line.full);
