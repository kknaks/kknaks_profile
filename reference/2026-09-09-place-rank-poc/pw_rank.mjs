import { chromium } from 'playwright';
import fs from 'fs';
const QUERY = process.argv[2] || '강남역성형외과';
const TARGET = process.argv[3] || '무이성형외과';
const MAX_PAGES = 10;
const url = `https://map.naver.com/p/search/${encodeURIComponent(QUERY)}?searchType=place`;
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ locale: 'ko-KR', viewport: { width: 1400, height: 900 },
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36' });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
// wait for searchIframe frame to exist and have content
const getSF = () => page.frames().find(f => f.name() === 'searchIframe' && f.url().includes('pcmap'));
let sf = null;
for (let i = 0; i < 60; i++) { sf = getSF(); if (sf) { const n = await sf.$$eval('li', e => e.length).catch(() => 0); if (n > 0) break; } await page.waitForTimeout(500); }
if (!sf) throw new Error('searchIframe not found');
await page.waitForTimeout(1500); sf = getSF();

async function scrollAll() {
  sf = getSF();
  let prev = -1;
  for (let i = 0; i < 20; i++) {
    const n = await sf.$$eval('li', els => els.length);
    if (n === prev) break; prev = n;
    await sf.evaluate(() => {
      const li = document.querySelector('li'); let el = li;
      while (el && el !== document.body) { const s = getComputedStyle(el); if (/(auto|scroll)/.test(s.overflowY) && el.scrollHeight > el.clientHeight) break; el = el.parentElement; }
      (el || document.scrollingElement).scrollTop = (el || document.scrollingElement).scrollHeight;
    });
    await page.waitForTimeout(1000);
  }
}
async function readItems() {
  sf = getSF();
  return sf.$$eval('li', els => els.map(li => {
    const t = li.innerText.replace(/\s+/g, ' ');
    const spans = [...li.querySelectorAll('span')].map(e => e.textContent.trim()).filter(Boolean);
    const name = spans.find(t => t.length < 40 && /(의원|병원|클리닉|외과)$/.test(t)) || spans.find(t => /성형외과/.test(t) && t.length < 40) || null;
    const hrefs = [...li.querySelectorAll('a')].map(a => a.getAttribute('href') || '');
    const id = hrefs.map(h => h.match(/\/(\d{6,})(?:[/?#]|$)/)?.[1]).find(Boolean) || null;
    return { name, id, ad: /광고/.test(t), reviews: (t.match(/리뷰 ([\d,]+)/) || [])[1] || null, addr: (t.match(/(서울 [가-힣]+구 [가-힣\d]+동)/) || [])[1] || null };
  }).filter(x => x.name && x.name.length > 1 && /의원|병원|외과|클리닉/.test(x.name)));
}
async function debugNames() {
  sf = getSF();
  const v = await sf.$$eval('li', els => els.slice(0,5).map(li => li.innerText.replace(/\s+/g,' ').slice(0,80)));
  console.error('sample:', v);
}

const all = []; const seen = new Set();
for (let p = 1; p <= MAX_PAGES; p++) {
  await scrollAll();
  const items = await readItems();
  let added = 0;
  for (const it of items) { const k = it.id || it.name; if (seen.has(k)) continue; seen.add(k); all.push({ ...it, page: p }); added++; }
  console.error(`page ${p}: ${items.length} li, +${added} new (total ${all.length})`);
  if (added === 0) break;
  // next page: pagination anchors at bottom, the one whose text is p+1
  const clicked = await sf.evaluate(next => {
    const cands = [...document.querySelectorAll('a, button')].filter(e => e.textContent.trim() === String(next));
    const el = cands.at(-1); if (!el) return false; el.click(); return true;
  }, p + 1);
  if (!clicked) break;
  await page.waitForTimeout(2500);
  await sf.waitForSelector('li', { timeout: 20000 }).catch(() => {});
}
let organic = 0; const rows = all.map((x, i) => { if (!x.ad) organic++; return { rank: i + 1, organicRank: x.ad ? null : organic, ...x }; });
const hit = rows.filter(r => r.name.replace(/\s/g, '').includes(TARGET.replace(/\s/g, '')));
fs.writeFileSync('rank_result.json', JSON.stringify({ query: QUERY, target: TARGET, total: rows.length, ads: rows.filter(r => r.ad).length, hit, rows }, null, 2));
console.log(`query="${QUERY}" target="${TARGET}" | collected ${rows.length} (ads ${rows.filter(r => r.ad).length})`);
if (hit.length) hit.forEach(h => console.log(`FOUND: 전체 ${h.rank}위 / 광고제외 ${h.organicRank ?? '(광고)'}위 / page ${h.page} / ${h.name} / ${h.addr} / 리뷰 ${h.reviews} / id ${h.id}`));
else console.log('NOT FOUND in collected list');
console.log('--- top 15 ---');
rows.slice(0, 15).forEach(r => console.log(`${String(r.rank).padStart(2)} ${r.ad ? 'AD ' : '   '} org=${r.organicRank ?? '-'} ${r.name} | ${r.addr} | 리뷰 ${r.reviews ?? '-'}`));
await browser.close();
