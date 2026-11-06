// WP-FE3 스크린샷 — 가짜 back 8892 · front 복사본 dev 3892(localhost). 8800 요청은 막는다
import { createRequire } from 'node:module';
const require = createRequire('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-agency-settlement-agency-settlement/caf95cf3-5253-478e-97ea-447abe5563d3/scratchpad/');
const { chromium } = require('playwright-core');
const FRONT = 'http://localhost:3892', OUT = process.env.OUT;
const b = await chromium.launch({ executablePath: process.env.HOME + '/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
const ctx = await b.newContext({ viewport: { width: 1600, height: 1000 } });
const p = await ctx.newPage();
const errors = [];
p.on('pageerror', (e) => errors.push(String(e)));
p.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await ctx.route(/:8800\//, (r) => { errors.push('BLOCKED 8800'); return r.abort(); });
const go = async (path) => { await p.goto(FRONT + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200); };
const t = async (sel) => (await p.locator(sel).first().innerText().catch(() => '(없음)')).replace(/\s+/g, ' ').trim();
const group = async (id, name) => {
  const g = p.locator(`[data-purchase="${id}"]`);
  await g.screenshot({ path: `${OUT}/${name}.png` });
  console.log(`${name}: ${(await g.innerText()).replace(/\s+/g, ' ')}`);
};

await go('/?month=2026-10');
await p.screenshot({ path: `${OUT}/monthly.png`, fullPage: true });
console.log('monthly summary:', await t('[data-testid=summary]'));
console.log('monthly groups:', await p.locator('[data-purchase]').count(), '| 결제·취소 줄:', await p.locator('[data-kind]:not([data-kind=item])').count(), '| 환불 배지:', await p.getByText('환불', { exact: true }).count(), '| 미수납:', await p.getByText('미수납').count());
await group('aabbcc', 'repayment');
await group('789fed', 'partial-refund');
await group('6a7b8c', 'prior-cancel');
await group('d4e5f6', 'zero-order');
await group('f0e1d2', 'mismatch');
await group('cba987', 'refunded-item');
await group('ddeeff', 'mixed-currency');

await go('/agency?month=2026-10');
await p.screenshot({ path: `${OUT}/agency-all.png`, fullPage: true });
console.log('agency-all summary:', await t('[data-testid=summary]'));
console.log('agency-all tabs:', await t('[role=tablist]'));
await go('/agency?month=2026-10&agency=' + encodeURIComponent('에이전시A(에이전시)'));
await p.screenshot({ path: `${OUT}/agency-one.png`, fullPage: true });
console.log('agency-one summary:', await t('[data-testid=summary]'));
await go('/?month=2026-09');
await p.screenshot({ path: `${OUT}/monthly-closed.png`, fullPage: true });
console.log('sep summary:', await t('[data-testid=summary]'));
await go('/agency?month=2026-09&agency=' + encodeURIComponent('에이전시B(에이전시)'));
await p.screenshot({ path: `${OUT}/agency-hidden-only.png`, fullPage: true });
console.log('sep B url:', decodeURIComponent(p.url().replace(FRONT, '')), '| empty:', await t('[data-state=empty]'));
console.log('errors:', JSON.stringify(errors));
await b.close();
