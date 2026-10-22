import { expect, test, type Page } from '@playwright/test';
import sharp from 'sharp';

const FILTERS = ['natural', 'fineWrinkle', 'deepWrinkle', 'pore', 'redness', 'pigment', 'porphyrin'] as const;

async function openScreen(page: Page) {
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto('/screen');
  await expect(page.getByTestId('face-viewer')).toHaveAttribute('data-ready', 'true', { timeout: 60_000 });
}

/** 큰 화면 필터 칩은 태블릿에 요청만 보내므로, 단독 시험에선 태블릿 탭을 같이 띄운다 */
async function openPair(page: Page) {
  const tablet = await page.context().newPage();
  await tablet.goto('/tablet');
  await tablet.evaluate(() => localStorage.clear());
  await tablet.reload();
  await openScreen(page);
  return tablet;
}

const az = (p: Page) => p.evaluate(() => window.__faceViewer!.azimuthDeg());

/** WebGL 캔버스 픽셀만(위에 떠 있는 A2 카드·필터 바는 빼고) — preserveDrawingBuffer 로 읽는다 */
async function canvasRaw(page: Page) {
  const url = await page.locator('[data-testid=face-viewer] canvas').evaluate((c: HTMLCanvasElement) => c.toDataURL('image/png'));
  return sharp(Buffer.from(url.split(',')[1], 'base64')).removeAlpha().raw().toBuffer({ resolveWithObject: true });
}

type Raw = Awaited<ReturnType<typeof canvasRaw>>;

function diffRatio(a: Raw, b: Raw) {
  const ch = a.info.channels;
  const px = a.info.width * a.info.height;
  let changed = 0;
  for (let i = 0; i < px; i++) {
    let d = 0;
    for (let c = 0; c < 3; c++) d = Math.max(d, Math.abs(a.data[i * ch + c] - b.data[i * ch + c]));
    if (d > 12) changed++;
  }
  return changed / px;
}

test('AC-19 — 첫 진입은 정면(+z), 거울 반전 없음', async ({ page }) => {
  await openScreen(page);
  expect(Math.abs(await az(page))).toBeLessThan(1);
  expect(Math.abs((await page.evaluate(() => window.__faceViewer!.polarDeg())) - 90)).toBeLessThan(1);
  // 고객의 오른쪽(x 음수)이 화면 왼쪽(NDC x < 0) — 마주 보는 시점
  const [xr] = await page.evaluate(() => window.__faceViewer!.project(-0.05, 0, 0.05));
  const [xl] = await page.evaluate(() => window.__faceViewer!.project(0.05, 0, 0.05));
  expect(xr).toBeLessThan(0);
  expect(xl).toBeGreaterThan(0);
  await expect(page.getByTestId('face-viewer')).toHaveAttribute('data-applied', 'natural');
});

test('AC-20 — 필터 7개가 각각 다른 그림', async ({ page }) => {
  await openPair(page);
  const shots: Record<string, Raw> = {};
  for (const f of FILTERS) {
    await page.getByTestId(`filter-${f}`).click();
    await expect(page.getByTestId('face-viewer')).toHaveAttribute('data-applied', f, { timeout: 15_000 });
    await page.waitForTimeout(700); // 페이드 250ms
    shots[f] = await canvasRaw(page);
  }
  const rows: string[] = [];
  for (let i = 0; i < FILTERS.length; i++) {
    for (let j = i + 1; j < FILTERS.length; j++) {
      const r = diffRatio(shots[FILTERS[i]], shots[FILTERS[j]]);
      rows.push(`${FILTERS[i]}↔${FILTERS[j]} ${(r * 100).toFixed(2)}%`);
      expect(r, `${FILTERS[i]}↔${FILTERS[j]}`).toBeGreaterThan(0.01);
    }
  }
  console.log(rows.join('\n'));
});

test('AC-22 — 좌우 ±75° 까지만 · 더블클릭·[정면으로] 로 정면 복귀', async ({ page }) => {
  const tablet = await openPair(page);
  const box = (await page.locator('[data-testid=face-viewer] canvas').boundingBox())!;
  const cx = box.x + box.width / 2;
  const cy = box.y + box.height / 2;
  for (const dir of [1, -1]) {
    await page.mouse.move(cx, cy);
    await page.mouse.down();
    for (let k = 1; k <= 20; k++) await page.mouse.move(cx + dir * k * 60, cy, { steps: 2 });
    await page.mouse.up();
    await page.waitForTimeout(1200); // damping
    const a = await az(page);
    expect(Math.abs(a)).toBeGreaterThan(70);
    expect(Math.abs(a)).toBeLessThanOrEqual(75.01);
    // 위아래도 60–120° 안
    const polar = await page.evaluate(() => window.__faceViewer!.polarDeg());
    expect(polar).toBeGreaterThanOrEqual(59.99);
    expect(polar).toBeLessThanOrEqual(120.01);
  }
  await page.locator('[data-testid=face-viewer] canvas').dblclick();
  await expect.poll(() => az(page).then(Math.abs), { timeout: 3000 }).toBeLessThan(1);

  // 태블릿 [정면으로]
  await page.mouse.move(cx, cy);
  await page.mouse.down();
  await page.mouse.move(cx + 400, cy, { steps: 10 });
  await page.mouse.up();
  await page.waitForTimeout(800);
  expect(Math.abs(await az(page))).toBeGreaterThan(10);
  await tablet.getByTestId('camera-reset').click();
  await expect.poll(() => az(page).then(Math.abs), { timeout: 3000 }).toBeLessThan(1);
});

test('AC-23 — public/m3d 가 없으면 안내 문구, 페이지는 산다', async ({ page }) => {
  await page.route('**/m3d/**', (r) => r.fulfill({ status: 404, body: 'not found' }));
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto('/screen');
  await expect(page.getByTestId('viewer-missing')).toContainText('npm run prepare:assets');
  await expect(page.getByTestId('screen-plan')).toBeVisible();
  await expect(page.getByTestId('report-missing').first()).toContainText('prepare:assets');
  expect(errors).toEqual([]);
});
