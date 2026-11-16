import { chromium } from "playwright-core";
import { readFileSync } from "node:fs";
const [OUT, OLD, mode] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.HOME + "/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell" });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
if (mode === "old") await page.route("**/static/day.js*", (r) => r.fulfill({ contentType: "text/javascript", body: readFileSync(OLD, "utf8") }));
const log = [];
page.on("pageerror", (e) => log.push("PAGEERROR " + e.message));
await page.goto("http://127.0.0.1:11040/login", { waitUntil: "load" });
await page.fill("input[name=email]", process.env.DAY_SEED_KOS_SYSTEM_EMAIL);
await page.fill("input[name=password]", process.env.DAY_SEED_KOS_SYSTEM_PASSWORD);
await Promise.all([page.waitForURL("**/board", { timeout: 30000 }), page.click("button[type=submit]")]);
await page.goto("http://127.0.0.1:11040/dev/kit/board", { waitUntil: "load" });
await page.waitForTimeout(1200);
const visibleCards = () => page.evaluate(() => [...document.querySelectorAll(".day-card--room")].filter((c) => { const r = c.getBoundingClientRect(); return r.height > 0 && r.width > 0; }).length);
const card = page.locator(".day-card--room:has(input[data-day-check]:not(:disabled))").first();
await card.locator("input[data-day-check]:not(:disabled)").first().check();
await page.waitForTimeout(400);
const btn = card.locator(".day-actionbar [data-day-pop^='call-']");
if (process.argv[5] === "f1") {
  // F1 시절 마크업(640 두 칸 · day-modal) + 데모처럼 판에 카드 한 장만 — 그 카드만 남기고 나머지는 숨김
  await page.evaluate((id) => {
    const pop = document.getElementById(id);
    pop.className = "day-pop day-modal day-modal--call";
    pop.removeAttribute("data-day-pop-align");
    pop.hidden = true;
  }, await btn.getAttribute("data-day-pop"));
  await page.evaluate(() => { const keep = document.querySelector(".day-card--room:has(input[data-day-check]:checked)").parentElement;
    document.querySelectorAll("[data-day-sort-item]").forEach((i) => { if (i !== keep) i.remove(); }); });
}
const b = await btn.boundingBox();
log.push(`[${mode}] cards before=${await visibleCards()} btn=(${Math.round(b.x)},${Math.round(b.y)})`);
await btn.click(); await page.waitForTimeout(600);
const st = await page.evaluate(() => {
  const p = document.querySelector(".day-pop:not([hidden])");
  const main = document.getElementById("board-main");
  const r = p?.getBoundingClientRect();
  // 판이 「사라졌나」 — 팝오버가 판 위를 얼마나 덮나 · 판 영역 가운데 점의 맨 위 요소
  const board = document.querySelector("main.day-board").getBoundingClientRect();
  const c = document.querySelector(".day-card--room:has(input[data-day-check]:checked)").getBoundingClientRect();
  const hit = document.elementFromPoint(c.left + c.width / 2, c.top + c.height / 2);
  return { pop: r ? `(${Math.round(r.x)},${Math.round(r.y)}) ${Math.round(r.width)}×${Math.round(r.height)}` : "none",
    count: p?.querySelector("[data-day-pick-count]")?.textContent, open: !!p,
    boardCenterTop: hit ? (hit.closest(".day-pop") ? "팝오버" : hit.closest(".day-card--room") ? "카드" : hit.className || hit.tagName) : null };
});
log.push(`[${mode}] pop=${st.pop} 호출할 시술=${st.count} 고른 카드 자리 맨 위=${st.boardCenterTop} cards=${await visibleCards()}`);
await page.screenshot({ path: `${OUT}/w4-repro-${mode}-js${process.argv[5] ? '-' + process.argv[5] : ''}.png` });
const x = page.locator(".day-pop:not([hidden]) [data-day-pop-close]");
if (await x.count()) { await x.click(); await page.waitForTimeout(300); log.push(`[${mode}] X 누름 → 열림=${await page.locator(".day-pop:not([hidden])").count()}`); }
console.log(log.join("\n"));
await browser.close();
