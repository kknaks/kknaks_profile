// Uses an already installed offline Chromium over CDP pipes; no server/port/package.
import {spawn} from 'node:child_process';import {readFile,writeFile,rm,mkdir} from 'node:fs/promises';import {fileURLToPath,pathToFileURL} from 'node:url';import path from 'node:path';
const out=path.dirname(fileURLToPath(import.meta.url));const profile=path.join(out,'.browser-profile');await mkdir(profile,{recursive:true});
const exe='/Users/kknaks/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const proc=spawn(exe,['--headless','--remote-debugging-pipe','--disable-gpu','--no-first-run','--disable-background-networking','--disable-component-update','--disable-sync','--disable-default-apps','--no-proxy-server','--host-resolver-rules=MAP * ~NOTFOUND','--user-data-dir='+profile],{stdio:['ignore','ignore','pipe','pipe','pipe']});
let next=0,buf='',pending=new Map(),events=[],errors=[];proc.stderr.on('data',()=>{});proc.stdio[4].on('data',b=>{buf+=b.toString();let pos;while((pos=buf.indexOf('\0'))>=0){let s=buf.slice(0,pos);buf=buf.slice(pos+1);if(!s)continue;let m=JSON.parse(s);if(m.id&&pending.has(m.id)){let p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result)}else events.push(m)}});
const call=(method,params={},sessionId)=>new Promise((resolve,reject)=>{let id=++next,timer=setTimeout(()=>{pending.delete(id);reject(new Error('timeout '+method))},45000);pending.set(id,{resolve,reject,timer});proc.stdio[3].write(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})})+'\0')});
let sid,checks=[];const ck=(name,pass,detail={})=>checks.push({check:name,pass,...detail});
try{
 const target=await call('Target.createTarget',{url:'about:blank'});sid=(await call('Target.attachToTarget',{targetId:target.targetId,flatten:true})).sessionId;
 await call('Page.enable',{},sid);await call('Runtime.enable',{},sid);await call('Network.enable',{},sid);await call('Network.setBlockedURLs',{urls:['http://*','https://*','ws://*','wss://*']},sid);
 await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false},sid);
 await call('Page.navigate',{url:pathToFileURL(path.join(out,'index.html')).href},sid);
 async function evaluate(expression){let r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true},sid);if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 for(let i=0;i<30;i++){if(await evaluate("document.readyState==='complete' && typeof renderCounts!=='undefined'"))break;await new Promise(r=>setTimeout(r,300))}
 let initial=await evaluate("({counts:renderCounts,types:document.querySelectorAll('#types>article').length,nodes:document.querySelectorAll('#nodes>article').length,edges:document.querySelectorAll('#edges>article').length,cases:document.querySelectorAll('#cases>article').length,ids:[...document.querySelectorAll('[id]')].map(x=>x.id),anchors:[...document.querySelectorAll('a[href^=\"#\"]')].map(x=>x.getAttribute('href').slice(1)),body:document.body.scrollWidth,viewport:innerWidth})");
 ck('html_design_type_node_edge_case_counts',initial.types===25&&initial.nodes===13&&initial.edges===33&&initial.cases===42,initial.counts);ck('dynamic_ids_unique',initial.ids.length===new Set(initial.ids).size);ck('all_dynamic_anchor_targets',initial.anchors.every(x=>initial.ids.includes(x)));ck('desktop_no_body_overflow',initial.body<=initial.viewport,{width:initial.body,viewport:initial.viewport});
 ck('case_search',await evaluate("$('search').value='NOTE-LINK-111';$('search').dispatchEvent(new Event('input'));renderCounts.cases===1 && !!document.getElementById('case-NOTE-LINK-111')"));
 ck('edge_filter',await evaluate("$('reset').click();$('type').value='product';$('type').dispatchEvent(new Event('change'));[...document.querySelectorAll('#types>article')].length===1 && document.querySelector('#types>article').id==='type-product' && renderCounts.edges>0 && renderCounts.edges<33"));
 ck('current_only_filter',await evaluate("$('reset').click();$('mode').value='current';$('mode').dispatchEvent(new Event('change'));renderCounts.types===0 && renderCounts.current===284 && renderCounts.migration===4400"));
 ck('unknown_query_empty',await evaluate("$('reset').click();$('search').value='zz-no-match-721';$('search').dispatchEvent(new Event('input'));renderCounts.types===0 && renderCounts.cases===0 && $('types').textContent.includes('없습니다')"));
 await evaluate("$('reset').click()");
 await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true},sid);
 ck('mobile_no_body_overflow',await evaluate('document.body.scrollWidth<=innerWidth'));
 ck('mobile_tables_scrollable',await evaluate("[...document.querySelectorAll('.scroll')].some(x=>x.scrollWidth>x.clientWidth)"));
 await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false},sid);
 await evaluate('window.scrollTo(0,0)');const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},sid);await writeFile(path.join(out,'.preview.png'),Buffer.from(shot.data,'base64'));
 errors=events.filter(e=>e.method==='Runtime.exceptionThrown');ck('no_browser_js_errors',errors.length===0,{errors});ck('no_remote_requests',events.filter(e=>e.method==='Network.requestWillBeSent').every(e=>!/^https?:/.test(e.params.request.url)));
}catch(e){ck('browser_run',false,{error:String(e)})}finally{await call('Browser.close').catch(()=>{});proc.kill();await new Promise(r=>setTimeout(r,200));await rm(profile,{recursive:true,force:true})}
const result={engine:'existing Chromium headless shell 1248 / CDP pipe / file:// / HTTP blocked',passed:checks.filter(c=>c.pass).length,failed:checks.filter(c=>!c.pass).length,checks};
let combined={};try{combined=JSON.parse(await readFile(path.join(out,'validation.json'),'utf8'))}catch{};combined.browser=result;await writeFile(path.join(out,'validation.json'),JSON.stringify(combined,null,2)+'\n');console.log(JSON.stringify(result));if(result.failed)process.exitCode=1;
