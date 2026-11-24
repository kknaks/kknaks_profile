// SPEC-011 화면 확인 — 새 브라우저 프로필(새 context)로 재생 마지막 화면 · 모달 · 스피너를 찍는다.
// 실행: node shots.cjs <base> <out_dir> <conv_03b8> <conv_ecc6> <conv_73bd>
const pw = require(process.env.PW_PATH);
(async () => {
  const [base, out, c1, c2, c3] = process.argv.slice(2);
  const browser = await pw.chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  for (const [tag, id] of [['03b8', c1], ['ecc6', c2], ['73bd', c3]]) {
    await page.goto(`${base}/c/${id}`, { waitUntil: 'load' });
    await page.waitForTimeout(3000);
    await page.screenshot({ path: `${out}/fetchplan-${tag}-final.png`, fullPage: false });
  }
  // 모달 — 마지막 대화 목록의 첫 「설명」 단추
  if (!(await page.locator('[data-cs-explain]:visible').count())) { const h = page.locator('.cs-topic__head').first(); if (await h.count()) { await h.click(); await page.waitForTimeout(800); } }
  const btn = page.locator('[data-cs-explain]:visible').first();
  if (await btn.count()) {
    await btn.click();
    await page.waitForTimeout(2500);
    await page.screenshot({ path: `${out}/fetchplan-73bd-modal.png`, fullPage: false });
    await page.keyboard.press('Escape');
  } else {
    errors.push('no explain button');
  }
  if (process.env.SKIP_SPIN) { console.log(JSON.stringify({ errors })); await browser.close(); return; }
  // 스피너 — 새 대화 첫 턴
  await page.goto(`${base}/`, { waitUntil: 'load' }); await page.waitForTimeout(2000);
  await page.fill('.cs-form__input', '눈가 주름이 고민이야');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}/fetchplan-spinner.png`, fullPage: false });
  await page.waitForTimeout(90000);
  await page.screenshot({ path: `${out}/fetchplan-spinner-done.png`, fullPage: false });
  console.log(JSON.stringify({ errors, url: page.url() }));
  await browser.close();
})();
