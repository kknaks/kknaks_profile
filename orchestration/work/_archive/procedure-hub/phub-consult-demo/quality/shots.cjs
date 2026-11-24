// 품질 기준선 대표 화면 3 장 — 새 브라우저 프로필(새 context)로 대화 마지막 화면을 찍는다.
// 실행: PW_PATH=<playwright 모듈 경로> node shots.cjs <base> <out_dir> <이름>=<대화 id> [<이름>=<대화 id> …]
const pw = require(process.env.PW_PATH);
(async () => {
  const [base, out, ...pairs] = process.argv.slice(2);
  const browser = await pw.chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  for (const p of pairs) {
    const [name, id] = p.split('=');
    await page.goto(`${base}/c/${id}`, { waitUntil: 'load' });
    await page.waitForTimeout(3000);
    await page.screenshot({ path: `${out}/quality-base-${name}.png`, fullPage: false });
  }
  console.log(JSON.stringify({ errors }));
  await browser.close();
})();
