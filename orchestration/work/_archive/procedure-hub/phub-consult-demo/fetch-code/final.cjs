// 재생 마지막 화면 — 페이지마다 새 브라우저(새 프로필) · 'load' + 3 초 · 보이는 창만(fullPage 는 고정 배치에서 빈 화면으로 찍힘).
// 실행: PW_PATH=<playwright> node final.cjs <url> <out.png>
const pw = require(process.env.PW_PATH);
(async () => {
  const b = await pw.chromium.launch(); const p = await (await b.newContext({viewport:{width:1440,height:1000}})).newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0,200)));
  await p.goto(process.argv[2], {waitUntil:'load'}); await p.waitForTimeout(3000);
  console.log('bubbles', await p.locator('.cs-bubble').count(), 'errors', JSON.stringify(errs));
  await p.screenshot({path: process.argv[3]});
  await b.close();
})();
