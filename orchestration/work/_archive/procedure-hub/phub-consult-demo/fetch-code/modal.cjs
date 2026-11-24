const pw = require(process.env.PW_PATH);
(async () => {
  const b = await pw.chromium.launch(); const p = await (await b.newContext({viewport:{width:1440,height:1000}})).newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0,200)));
  await p.goto(process.argv[2], {waitUntil:'load'}); await p.waitForTimeout(3000);
  console.log('explain buttons', await p.locator('[data-cs-explain]').count());
  await p.locator('[data-cs-explain]').first().click(); await p.waitForTimeout(3000);
  await p.screenshot({path: process.argv[3]});
  console.log('dialog', await p.locator('dialog[open], [role=dialog]').count(), 'errors', JSON.stringify(errs));
  await b.close();
})();
