// code r2 F-1 확인 — [전체 다시 받기] · [새 결제 받기] 뒤 달 이동 · 뒤로 · 앞으로 · 탭에서 refresh 가 다시 나가지 않는지(가짜 back 8891 · front 3891)
import fs from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-agency-settlement-agency-settlement/caf95cf3-5253-478e-97ea-447abe5563d3/scratchpad/');
const { chromium } = require('playwright-core');
const FRONT = 'http://localhost:3891', BACK = 'http://127.0.0.1:8891', LOG = process.env.LOG, OUT = process.env.OUT;
const b = await chromium.launch({ executablePath: process.env.HOME + '/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
const p = await ctx.newPage();
await ctx.route(/:8800\//, (r) => { console.log('BLOCKED 8800', r.request().url()); return r.abort(); });
const wait = (ms = 1800) => p.waitForTimeout(ms);
const mark = () => fs.writeFileSync(LOG, '');
const took = (label) => {
  const reqs = fs.readFileSync(LOG, 'utf8').split('\n').filter((l) => l.startsWith('GET /api/sales?')).map((l) => decodeURIComponent(l.slice(4)));
  const withRefresh = reqs.filter((r) => r.includes('refresh='));
  console.log(`${label.padEnd(44)} 요청 ${reqs.length} · refresh 붙은 것 ${withRefresh.length}${withRefresh.length ? ' → ' + [...new Set(withRefresh)].join(' | ') : ''}`);
  return withRefresh;
};
const step = async (label, fn, ms) => { mark(); await fn(); await wait(ms); return took(label); };
const go = (path) => p.goto(FRONT + path, { waitUntil: 'networkidle' });
const confirmFull = async () => { await p.click('[data-testid=full-refresh]'); await wait(400); await p.getByRole('button', { name: '다시 받기', exact: true }).click(); };
let bad = 0;
const expect0 = (r) => { bad += r.length; };

await fetch(BACK + '/__reset');
console.log('— A. 10월(이번 달) [전체 다시 받기] 뒤');
await step('열기 /?month=2026-10', () => go('/?month=2026-10'));
const a = await step('[전체 다시 받기] → 확인', confirmFull, 2500);
if (!a.every((r) => r.includes('month=2026-10&refresh=full'))) bad++;
expect0(await step('‹ (9월 · 확정 달)', () => p.getByRole('button', { name: '이전 달' }).click()));
expect0(await step('› (10월)', () => p.getByRole('button', { name: '다음 달' }).click()));
expect0(await step('브라우저 뒤로 (9월)', () => p.goBack()));
expect0(await step('브라우저 앞으로 (10월)', () => p.goForward()));
expect0(await step('메뉴 에이전트별 (10월)', () => p.getByRole('link', { name: '에이전트별 조회' }).click()));

console.log('— B. 9월(확정) [전체 다시 받기] 뒤');
await step('열기 /?month=2026-09', () => go('/?month=2026-09'));
await step('[전체 다시 받기] → 확인', confirmFull, 2500);
expect0(await step('‹ (8월 · 확정 달)', () => p.getByRole('button', { name: '이전 달' }).click()));
expect0(await step('› (9월 · 확정 달)', () => p.getByRole('button', { name: '다음 달' }).click()));
expect0(await step('브라우저 뒤로 (8월)', () => p.goBack()));
expect0(await step('브라우저 뒤로 (9월)', () => p.goBack()));

console.log('— C. 에이전트별 10월 [전체 다시 받기] 뒤 탭 · 달');
await step('열기 /agency?month=2026-10', () => go('/agency?month=2026-10'));
await step('[전체 다시 받기] → 확인', confirmFull, 2500);
expect0(await step('탭 에이전시A', () => p.getByRole('tab', { name: /에이전시A/ }).click()));
expect0(await step('‹ (9월)', () => p.getByRole('button', { name: '이전 달' }).click()));
expect0(await step('브라우저 뒤로 (10월 · A)', () => p.goBack()));

console.log('— D. 10월 [새 결제 받기] 뒤');
await fetch(BACK + '/__reset');
await step('열기 /?month=2026-10', () => go('/?month=2026-10'));
await step('[새 결제 받기]', () => p.click('[data-testid=pull-new]'), 2500);
expect0(await step('‹ (9월)', () => p.getByRole('button', { name: '이전 달' }).click()));
expect0(await step('브라우저 뒤로 (10월)', () => p.goBack()));
expect0(await step('[다시 시도] 없음 · 새로고침 (10월)', () => p.reload()));

console.log(`\n결과: 확인 없이 나간 refresh = ${bad}`);
// 폭 1600 — 1440 · 1920 스크린샷
await fetch(BACK + '/__reset');
for (const w of [1440, 1920]) {
  await p.setViewportSize({ width: w, height: 1000 });
  await go('/?month=2026-10'); await wait(1500);
  await p.screenshot({ path: `${OUT}/width-${w}-monthly.png`, fullPage: false });
  const box = await p.locator('main > div').first().boundingBox();
  console.log(`폭 ${w}: 본문 x=${Math.round(box.x)} w=${Math.round(box.width)}`);
  await go('/agency?month=2026-10'); await wait(1500);
  await p.screenshot({ path: `${OUT}/width-${w}-agency-all.png`, fullPage: false });
}
await b.close();
