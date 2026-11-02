import { expect, test } from '@playwright/test';

test('라우트 3개가 200', async ({ request }) => {
  for (const p of ['/', '/screen', '/tablet']) {
    const res = await request.get(p);
    expect(res.status(), p).toBe(200);
  }
});

test('메디킷 solid blue 버튼이 차티 primary #6f21ff', async ({ page }) => {
  await page.goto('/');
  const bg = await page.getByTestId('open-screen').evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe('rgb(111, 33, 255)');
});

test('창 크기가 바뀌어도 1920×1080 캔버스 비율 유지', async ({ page }) => {
  for (const [w, h] of [
    [1280, 720],
    [1000, 900],
    [1920, 1080],
  ]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('/screen');
    const box = await page.getByTestId('stage-canvas').boundingBox();
    expect(box).not.toBeNull();
    expect(Math.abs(box!.width / box!.height - 1920 / 1080)).toBeLessThan(0.01);
    expect(box!.width).toBeLessThanOrEqual(w + 1);
    expect(box!.height).toBeLessThanOrEqual(h + 1);
  }
});
