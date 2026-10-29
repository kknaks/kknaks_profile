// 시안 v2 장면 이름 그대로 스크린샷(가짜 back 8891 · front 3891). 운영 back 8800 · front 3800 은 건드리지 않는다
import { createRequire } from 'node:module';
const require = createRequire('/private/tmp/claude-501/-Users-kknaks-orca-workspaces-agency-settlement-agency-settlement/caf95cf3-5253-478e-97ea-447abe5563d3/scratchpad/');
const { chromium } = require('playwright-core');

const FRONT = process.env.FRONT || 'http://127.0.0.1:3891';
const BACK = 'http://127.0.0.1:8891';
const OUT = process.env.OUT;
const ONLY = process.argv.slice(2);
const b = await chromium.launch({ executablePath: process.env.HOME + '/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
const p = await ctx.newPage();
const errors = [];
p.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
p.on('pageerror', (e) => errors.push(String(e)));
// 안전장치 — 8800(운영 back)으로 나가는 요청은 막는다
await ctx.route(/:8800\//, (r) => { errors.push('BLOCKED 8800 ' + r.request().url()); return r.abort(); });

const reset = () => fetch(BACK + '/__reset');
const go = async (path, wait = 1500) => { await p.goto(FRONT + path, { waitUntil: 'networkidle' }).catch(() => {}); await p.waitForTimeout(wait); };
const shot = async (name) => { await p.screenshot({ path: `${OUT}/${name}.png`, fullPage: true }); console.log('shot', name, '→', decodeURIComponent(p.url().replace(FRONT, ''))); };
const text = async (sel) => (await p.locator(sel).first().textContent().catch(() => null))?.replace(/\s+/g, ' ').trim();
const want = (n) => ONLY.length === 0 || ONLY.includes(n);

if (want('monthly')) { await reset(); await go('/?month=2026-10'); await shot('monthly'); console.log('  summary:', await text('[data-testid=summary]')); }
if (want('monthly-current')) {
  await reset(); await go('/?month=2026-10');
  await p.click('[data-testid=pull-new]'); await p.waitForTimeout(250); await shot('monthly-current-pulling');
  console.log('  button while pulling:', await text('[data-testid=pull-new]'), '| table still shown:', await p.locator('[data-testid=sales-table]').count());
  await p.waitForTimeout(1500); await shot('monthly-current');
  console.log('  fetched:', await text('[data-testid=fetched-at]'), '| 새로 받음 badges:', await p.getByText('새로 받음', { exact: true }).count());
  await p.click('[data-testid=pull-new]'); await p.waitForTimeout(1800); await shot('monthly-current-none');
  console.log('  none note:', await p.getByText(/새 결제 없음/).count());
}
if (want('monthly-closed')) {
  await reset(); await go('/?month=2026-09'); await shot('monthly-closed');
  console.log('  pull-new buttons:', await p.locator('[data-testid=pull-new]').count(), '| 확정:', await p.getByText('✓ 확정 · 저장됨').count());
  await p.click('[data-testid=full-refresh]'); await p.waitForTimeout(500); await shot('monthly-closed-confirm');
  await p.getByRole('button', { name: '다시 받기', exact: true }).click(); await p.waitForTimeout(250); await shot('monthly-closed-full-loading');
  await p.waitForTimeout(1500); await shot('monthly-closed-full-done'); console.log('  fetched after full:', await text('[data-testid=fetched-at]'));
}
if (want('monthly-loading')) { await go('/?month=2026-07', 2000); await shot('monthly-loading'); console.log('  export disabled:', await p.locator('[data-testid=export]').isDisabled()); }
if (want('monthly-empty')) { await go('/?month=2026-08'); await shot('monthly-empty'); console.log('  export disabled:', await p.locator('[data-testid=export]').isDisabled()); }
if (want('monthly-error')) { await go('/?month=2026-06'); await shot('monthly-error'); console.log('  export disabled:', await p.locator('[data-testid=export]').isDisabled()); }
if (want('monthly-bad-month')) { await go('/?month=2026-13'); await shot('monthly-bad-month'); }
if (want('monthly-config')) { await go('/?month=2026-10'); await shot('monthly-config'); }
if (want('agency-all')) { await reset(); await go('/agency?month=2026-10'); await shot('agency-all'); console.log('  summary:', await text('[data-testid=summary]')); }
if (want('agency-one')) {
  await go('/agency?month=2026-10&agency=' + encodeURIComponent('에이전시B(에이전시)')); await shot('agency-one'); console.log('  summary:', await text('[data-testid=summary]'));
  const dl = p.waitForEvent('download', { timeout: 5000 }).catch(() => null);
  await p.click('[data-testid=export]'); const d = await dl; console.log('  download name:', d ? d.suggestedFilename() : null);
}
if (want('agency')) { await go('/agency?month=2026-10&agency=' + encodeURIComponent('에이전시A(에이전시)')); await shot('agency'); console.log('  summary:', await text('[data-testid=summary]')); }
if (want('agency-empty')) { await go('/agency?month=2026-08'); await shot('agency-empty'); }
if (want('agency-unknown')) { await go('/agency?month=2026-10&agency=' + encodeURIComponent('에이전시Z(에이전시)'), 2000); await shot('agency-unknown'); }
if (want('agency-closed')) { await go('/agency?month=2026-09'); await shot('agency-closed'); }
if (want('export-monthly')) {
  await reset(); await go('/?month=2026-10');
  const dl = p.waitForEvent('download', { timeout: 5000 }).catch(() => null);
  await p.click('[data-testid=export]'); const d = await dl; console.log('  download name:', d ? d.suggestedFilename() : null);
  await go('/agency?month=2026-10');
  const dl2 = p.waitForEvent('download', { timeout: 5000 }).catch(() => null);
  await p.click('[data-testid=export]'); const d2 = await dl2; console.log('  download name:', d2 ? d2.suggestedFilename() : null);
}
if (want('nav')) {
  await reset(); await go('/?month=2026-09');
  await p.getByRole('link', { name: '에이전트별 조회' }).click(); await p.waitForTimeout(1500);
  console.log('  nav → ', decodeURIComponent(p.url().replace(FRONT, '')));
  await p.getByRole('tab', { name: /에이전시A/ }).click(); await p.waitForTimeout(1500);
  console.log('  tab → ', decodeURIComponent(p.url().replace(FRONT, '')));
  await p.getByRole('button', { name: '이전 달' }).click(); await p.waitForTimeout(1500);
  console.log('  ‹ → ', decodeURIComponent(p.url().replace(FRONT, '')));
}
console.log('errors:', JSON.stringify(errors));
await b.close();
