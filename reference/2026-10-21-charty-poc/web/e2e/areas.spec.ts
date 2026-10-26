import { expect, test, type BrowserContext, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import path from 'node:path';

// 부위 카드 · 지시선 · 모달(SPEC charty-consult-recommend §8 R-n)
const SEC = 1000;
const SCREENS = path.resolve(__dirname, '../../../../orchestration/work/charty-consult-recommend/screens');
const AREA_KEYS = ['forehead', 'eye', 'nasolabial', 'sebum', 'cheek', 'poreTexture'] as const;

async function openBoth(context: BrowserContext) {
  const tablet = await context.newPage();
  await tablet.setViewportSize({ width: 1180, height: 820 });
  await tablet.goto('/tablet');
  await tablet.evaluate(() => localStorage.clear());
  await tablet.reload();
  await expect(tablet.getByTestId('tablet-root')).toBeVisible();
  const screen = await context.newPage();
  await screen.setViewportSize({ width: 1920, height: 1080 });
  await screen.goto('/screen');
  await expect(screen.getByTestId('screen-link')).toHaveAttribute('data-on', 'true', { timeout: 5 * SEC });
  await expect(screen.getByTestId('area-score-eye')).toHaveAttribute('data-value', /\d/, { timeout: 10 * SEC });
  return { tablet, screen };
}

const card = (p: Page, k: string) => p.getByTestId(`area-card-${k}`);
/** 카드 안 내용(설명 · [자세히])이 카드 밖으로 잘리지 않고, 시술 탭이 한 줄(줄바꿈 X)인가 */
async function expectCardFits(p: Page, k: string) {
  const c = (await card(p, k).boundingBox())!;
  for (const id of [`area-desc-${k}`, `area-tabs-${k}`]) {
    const b = (await card(p, k).getByTestId(id).boundingBox())!;
    expect(b.y + b.height, `${k} ${id} 잘림`).toBeLessThanOrEqual(c.y + c.height - 1);
  }
  const tops = await card(p, k).getByTestId('area-tab').evaluateAll((els) => els.map((e) => Math.round(e.getBoundingClientRect().top)));
  expect(new Set(tops).size, `${k} 탭 줄바꿈`).toBe(1);
}
async function expectStrong(p: Page, strong: string[]) {
  for (const k of AREA_KEYS) await expect(card(p, k)).toHaveAttribute('data-state', strong.includes(k) ? 'strong' : 'dim', { timeout: SEC });
}

test('R-7 — 카드 6장이 뷰어 패널 안 좌3 · 우3 순서 · 오른쪽 열 그대로 · focus-card 없음', async ({ context }) => {
  const { screen } = await openBoth(context);
  const left = await screen.getByTestId('area-col-left').locator('[data-testid^=area-card-]').evaluateAll((els) => els.map((e) => e.getAttribute('data-testid')));
  const right = await screen.getByTestId('area-col-right').locator('[data-testid^=area-card-]').evaluateAll((els) => els.map((e) => e.getAttribute('data-testid')));
  expect(left).toEqual(['area-card-forehead', 'area-card-eye', 'area-card-nasolabial']);
  expect(right).toEqual(['area-card-sebum', 'area-card-cheek', 'area-card-poreTexture']);
  const viewer = screen.getByTestId('screen-viewer');
  await expect(viewer.locator('[data-testid^=area-card-]')).toHaveCount(6);
  for (const id of ['screen-overview', 'screen-items', 'screen-plan', 'score-bars']) await expect(screen.getByTestId(id)).toBeVisible();
  await expect(screen.getByTestId('focus-card')).toHaveCount(0);
  await expect(screen.getByTestId('viewer-legend')).toContainText('목업 · 의학적 근거 아님');
  // 카드는 뷰어 패널 안
  const vb = (await viewer.boundingBox())!;
  for (const k of AREA_KEYS) {
    const c = (await card(screen, k).boundingBox())!;
    expect(c.x >= vb.x && c.x + c.width <= vb.x + vb.width && c.y >= vb.y && c.y + c.height <= vb.y + vb.height, `${k} 패널 밖`).toBe(true);
  }
  // 내용이 카드 밖으로 잘리지 않고 탭은 한 줄(W-12 → 2루프 U-1)
  for (const k of AREA_KEYS) await expectCardFits(screen, k);
});

test('W-4 — 측정 데이터 없음: 카드엔 짧은 문구 · 긴 안내는 오른쪽 열 · 잘림 0 · 확대 사진 자리표시', async ({ page }) => {
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.route('**/m3d/**', (r) => r.fulfill({ status: 404, body: 'not found' }));
  await page.goto('/screen');
  await expect(page.getByTestId('area-report-missing')).toHaveCount(6);
  await expect(page.getByTestId('area-report-missing').first()).toHaveText('측정 데이터 없음');
  await expect(page.getByTestId('report-missing').first()).toContainText('prepare:assets');
  for (const k of AREA_KEYS) {
    await expect(card(page, k)).toHaveAttribute('data-state', 'dim');
    await expectCardFits(page, k);
    await expect(page.getByTestId(`area-crop-${k}`)).toHaveAttribute('data-bg', '');
  }
});

test('R-8 — 자연광: strong 4 · dim 2 · 대표 점수 · 피지 「점수 없음」 「5,470개」', async ({ context }) => {
  const { screen } = await openBoth(context);
  await expectStrong(screen, ['eye', 'nasolabial', 'cheek', 'poreTexture']);
  const want: Record<string, string> = { eye: '61.4', nasolabial: '80.7', cheek: '67', poreTexture: '68.8', forehead: '88.3', sebum: '' };
  for (const [k, v] of Object.entries(want)) {
    await expect(screen.getByTestId(`area-score-${k}`)).toHaveAttribute('data-value', v);
    await expect(card(screen, k).locator('h3')).not.toBeEmpty();
    await expect(card(screen, k).locator('[data-grade]').first()).toBeVisible();
  }
  await expect(card(screen, 'sebum')).toContainText('점수 없음');
  await expect(card(screen, 'sebum')).toContainText('5,470개');
});

test('R-9 — 태블릿 「모공」 → 모공/피부결만 strong · 화면 「피지 세균」 → 6장 dim, 피지만 match', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('filter-pore').click();
  await expectStrong(screen, ['poreTexture']);
  await screen.getByTestId('filter-porphyrin').click();
  await expectStrong(screen, []);
  for (const k of AREA_KEYS) await expect(card(screen, k)).toHaveAttribute('data-match', k === 'sebum' ? 'true' : 'false');
});

test('R-10 — 태블릿 「피부결」 항목 → 모공/피부결만 strong, 화면 「붉은기」 → 볼/코만 strong', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('tab-analysis').click();
  await tablet.getByTestId('analysis-item-dermatoglyph').click();
  await expectStrong(screen, ['poreTexture']);
  await screen.getByTestId('filter-redness').click();
  await expectStrong(screen, ['cheek']);
});

test('R-11 — 화면 ① 새로고침 뒤 같은 필터 · 카드 상태 · 태블릿 카트 유지', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('view-all').click();
  await tablet.locator('[data-testid=procedure-row][data-name="눈가 보톡스"]').first().click();
  await tablet.getByTestId('filter-deepWrinkle').click();
  await expectStrong(screen, ['eye', 'nasolabial']);
  await screen.reload();
  await expect(screen.getByTestId('filter-deepWrinkle')).toHaveAttribute('data-active', 'true', { timeout: SEC });
  await expectStrong(screen, ['eye', 'nasolabial']);
  await tablet.reload();
  await expect(tablet.locator('[data-testid=cart-row][data-name="눈가 보톡스"]')).toBeVisible();
});

test('스크린샷 — 자연광 · 모공 필터', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await expect(screen.getByTestId('face-viewer')).toHaveAttribute('data-ready', 'true', { timeout: 60_000 });
  await screen.waitForTimeout(800);
  await screen.screenshot({ path: path.join(SCREENS, 'loop3-natural.png') });
  await tablet.getByTestId('filter-pore').click();
  await expect(screen.getByTestId('face-viewer')).toHaveAttribute('data-applied', 'pore', { timeout: 15_000 });
  await screen.waitForTimeout(800);
  await screen.screenshot({ path: path.join(SCREENS, 'loop2-filter-pore.png') });
});

// ── 3D 앵커 · 지시선(R-12 ~ R-16). 좌표 = 뷰어 패널 기준 설계 px. C 구역 = 두 카드 열 사이 x 256–784 · y 0–848(범례 줄 위)
const FACE = { x0: 256, x1: 784, y0: 0, y1: 848 };
type Anchor = { key: string; x: number; y: number; visible: boolean; opacity: number; occlusion: number };
const anchors = (p: Page) => p.evaluate(() => window.__faceViewer!.anchors!()) as Promise<Anchor[]>;
const az = (p: Page) => p.evaluate(() => window.__faceViewer!.azimuthDeg());

async function openViewer(context: BrowserContext) {
  const both = await openBoth(context);
  await expect(both.screen.getByTestId('face-viewer')).toHaveAttribute('data-ready', 'true', { timeout: 60_000 });
  await expect(both.screen.getByTestId('leader-lines')).toHaveCount(1, { timeout: 10 * SEC });
  await expect.poll(async () => (await anchors(both.screen)).filter((a) => a.occlusion > 0.99).length, { timeout: 5 * SEC }).toBe(6);
  return both;
}

async function drag(p: Page, dx: number) {
  const box = (await p.locator('[data-testid=face-viewer] canvas').boundingBox())!;
  const cx = box.x + box.width / 2;
  const cy = box.y + box.height / 2;
  await p.mouse.move(cx, cy);
  await p.mouse.down();
  const n = Math.max(1, Math.round(Math.abs(dx) / 40));
  for (let k = 1; k <= n; k++) await p.mouse.move(cx + (dx * k) / n, cy, { steps: 2 });
  await p.mouse.up();
  await p.waitForTimeout(300);
}

/** damping 이 멎을 때까지 */
async function settle(p: Page) {
  let prev = NaN;
  await expect
    .poll(async () => { const now = await az(p); const still = Math.abs(now - prev) < 0.01; prev = now; return still; }, { timeout: 10 * SEC, intervals: [250] })
    .toBe(true);
}
/** 작은 드래그를 반복해 방위각이 deg 를 넘을 때까지(매번 멎은 뒤 잰다) */
async function rotateTo(p: Page, deg: number) {
  for (let i = 0; i < 40 && Math.abs(await az(p)) < deg; i++) {
    await drag(p, 12);
    await settle(p);
  }
}

function polyline(attr: string | null): [number, number][] {
  return (attr ?? '').trim().split(/\s+/).map((s) => s.split(',').map(Number) as [number, number]);
}
function cross(a: [number, number], b: [number, number], c: [number, number], d: [number, number]) {
  const o = (p: [number, number], q: [number, number], r: [number, number]) => Math.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]));
  return o(a, b, c) * o(a, b, d) < 0 && o(c, d, a) * o(c, d, b) < 0;
}

test('R-12 — 정면: 점 6개 visible · C 구역 안 · 지시선 교차 0', async ({ context }) => {
  const { screen } = await openViewer(context);
  for (const a of await anchors(screen)) {
    expect(a.visible, a.key).toBe(true);
    expect(a.x > FACE.x0 && a.x < FACE.x1 && a.y > FACE.y0 && a.y < FACE.y1, `${a.key} (${a.x}, ${a.y})`).toBe(true);
    await expect(screen.getByTestId(`leader-${a.key}`)).toHaveAttribute('data-visible', 'true');
  }
  const lines = await Promise.all(AREA_KEYS.map(async (k) => polyline(await screen.getByTestId(`leader-${k}`).locator('polyline').getAttribute('points'))));
  const crossings: string[] = [];
  for (let i = 0; i < lines.length; i++)
    for (let j = i + 1; j < lines.length; j++)
      for (let s = 0; s < 2; s++) for (let t = 0; t < 2; t++) if (cross(lines[i][s], lines[i][s + 1], lines[j][t], lines[j][t + 1])) crossings.push(`${AREA_KEYS[i]}×${AREA_KEYS[j]}`);
  expect(crossings).toEqual([]);
  await screen.locator('[data-testid=screen-viewer]').screenshot({ path: path.join(SCREENS, 'anchors-front.png') });
});

test('R-13 — 약 30° 돌리면 점이 피부에 붙어 이동 · SVG 점 = 투영', async ({ context }) => {
  const { screen } = await openViewer(context);
  const before = await anchors(screen);
  await rotateTo(screen, 28);
  const a = Math.abs(await az(screen));
  expect(a).toBeGreaterThan(20);
  expect(a).toBeLessThan(36);
  const after = await anchors(screen);
  const [W, H] = await screen.evaluate(() => window.__faceViewer!.canvasSize!());
  for (const x of after.filter((q) => q.visible)) {
    const b = before.find((q) => q.key === x.key)!;
    expect(Math.hypot(x.x - b.x, x.y - b.y), `${x.key} 이동`).toBeGreaterThan(10);
    // 같은 틱에서 SVG 점과 투영을 함께 읽는다
    const { nx, ny, cx, cy } = await screen.evaluate((k) => {
      const p = window.__faceViewer!.anchor3d!(k as never);
      const [nx, ny] = window.__faceViewer!.project(p[0], p[1], p[2]);
      const dot = document.querySelector(`[data-testid=leader-dot-${k}]`)!;
      return { nx, ny, cx: Number(dot.getAttribute('cx')), cy: Number(dot.getAttribute('cy')) };
    }, x.key);
    expect(Math.abs(cx - (((nx + 1) / 2) * W + FACE.x0)), `${x.key} cx`).toBeLessThan(1);
    expect(Math.abs(cy - ((1 - ny) / 2) * H), `${x.key} cy`).toBeLessThan(1);
  }
  console.log(`azimuth ${a.toFixed(1)}° · visible ${after.filter((q) => q.visible).map((q) => q.key).join(',')}`);
  await screen.screenshot({ path: path.join(SCREENS, 'rotate-30.png') });
});

test('R-14 — 좌우 끝(±75°)에서 먼 쪽 볼 점이 숨고 카드는 그대로 · 더블클릭 정면 복귀 3초 안에 6개 visible', async ({ context }) => {
  const { screen } = await openViewer(context);
  const SIDES = { left: ['eye', 'nasolabial'], right: ['cheek', 'poreTexture'] };
  // 드래그 방향마다 먼 쪽 볼을 고정한다(W-1): 오른쪽으로 끌면 −75°(얼굴이 화면 오른쪽으로 돌아 R2·R3 이 멀어짐), 왼쪽으로 끌면 +75°(L2·L3)
  for (const [dx, far, sign] of [[1300, SIDES.right, -1], [-1300, SIDES.left, 1]] as const) {
    await drag(screen, dx);
    expect((await az(screen)) * sign).toBeGreaterThan(70);
    await screen.waitForTimeout(500);
    const list = await anchors(screen);
    const hidden = list.filter((q) => !q.visible).map((q) => q.key);
    expect(hidden.filter((k) => (far as readonly string[]).includes(k)).length, `az ${await az(screen)} hidden ${hidden}`).toBeGreaterThanOrEqual(1);
    for (const k of hidden) {
      expect(list.find((q) => q.key === k)!.opacity).toBeLessThan(0.05);
      await expect(screen.getByTestId(`leader-${k}`)).toHaveAttribute('data-visible', 'false');
    }
    for (const k of AREA_KEYS) await expect(card(screen, k)).toBeVisible();
    console.log(`az ${(await az(screen)).toFixed(1)} hidden ${hidden.join(',')}`);
  }
  await screen.locator('[data-testid=face-viewer] canvas').dblclick();
  await expect.poll(async () => (await anchors(screen)).filter((q) => q.visible).length, { timeout: 3 * SEC }).toBe(6);
});

test('R-15 — 매니페스트 mesh.bytes 가 다르면 지시선 0 · 카드·3D 정상', async ({ context }) => {
  const tablet = await context.newPage();
  await tablet.goto('/tablet');
  const screen = await context.newPage();
  await screen.setViewportSize({ width: 1920, height: 1080 });
  await screen.route('**/m3d/manifest.json', async (route) => {
    const res = await route.fetch();
    const body = await res.json();
    body.mesh.bytes += 1;
    await route.fulfill({ response: res, json: body });
  });
  const warns: string[] = [];
  screen.on('console', (m) => m.type() === 'warning' && m.text().includes('[anchors]') && warns.push(m.text()));
  await screen.goto('/screen');
  await expect(screen.getByTestId('face-viewer')).toHaveAttribute('data-ready', 'true', { timeout: 60_000 });
  await screen.waitForTimeout(1000);
  await expect(screen.getByTestId('leader-lines')).toHaveCount(0);
  await expect(screen.locator('[data-testid^=area-card-]')).toHaveCount(6);
  expect(warns.length).toBe(1);
});

test('R-16 — dim 카드 점·선 opacity 0.45–0.55 + 점선, strong 은 0.9 이상 · 프레임 비용(W-6)', async ({ context }) => {
  const { screen } = await openViewer(context);
  const list = await anchors(screen);
  for (const k of AREA_KEYS) {
    const state = await card(screen, k).getAttribute('data-state');
    const a = list.find((q) => q.key === k)!;
    // 흐린 선 0.5 + 점선(2루프 W-5)
    if (state === 'dim') {
      expect(a.opacity, k).toBeGreaterThanOrEqual(0.45);
      expect(a.opacity, k).toBeLessThanOrEqual(0.55);
      await expect(screen.getByTestId(`leader-${k}`).locator('polyline')).toHaveAttribute('stroke-dasharray', '6 4');
    }
    else expect(a.opacity, k).toBeGreaterThanOrEqual(0.9);
    expect(Number(await screen.getByTestId(`leader-${k}`).getAttribute('opacity'))).toBeCloseTo(a.opacity, 2);
  }
  await drag(screen, 300);
  const ms = await screen.evaluate(() => window.__faceViewer!.anchorMs!());
  console.log(`AnchorProjector useFrame 평균 ${ms.toFixed(3)}ms`);
  expect(ms).toBeLessThan(2);
});

// ── 시술명 모달(R-17 ~ R-21)
const tab = (p: Page, area: string, name: string) => card(p, area).locator(`[data-testid=area-tab][data-name="${name}"]`);
/** 탭을 골라 [자세히] — 모달을 연다 */
async function openProc(p: Page, area: string, name: string) {
  await tab(p, area, name).click();
  await card(p, area).getByTestId('area-detail').click();
}
const modal = (p: Page) => p.getByTestId('procedure-modal');
const sec = (p: Page, k: string) => modal(p).getByTestId(`modal-sec-${k}`);

test('R-17 — 눈가/눈밑 보톡스 모달 · 상향 표기 · 시술 시간 · 태블릿 변화 없음', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  const tabletText = async () => (await tablet.locator('body').innerText()).replace(/\d{1,2}:\d{2}/g, ''); // 시계는 뺀다
  await expect(tablet.getByTestId('tablet-screen-link')).toHaveAttribute('data-on', 'true', { timeout: 5 * SEC }); // 연결 표시가 켜진 뒤를 기준으로
  const before = await tabletText();
  await openProc(screen, 'eye', '보톡스');
  await expect(modal(screen)).toHaveAttribute('data-hub', 'M1-3-1');
  for (const [k, title] of [['mechanism', '어떻게 작용하나요'], ['safety', '알아 둘 반응'], ['contraindications', '받으면 안 되는 경우'], ['onset', '효과는 언제부터 · 얼마나'], ['procedure', '시술 시간 · 마취']])
    await expect(sec(screen, k)).toContainText(title);
  await expect(sec(screen, 'contraindications')).toContainText('보톡스 전체 기준');
  await expect(sec(screen, 'procedure')).toContainText('10–15분');
  await expect(sec(screen, 'procedure')).toContainText('마취 없음');
  await expect(sec(screen, 'procedure')).toContainText('보톡스 전체 기준');
  await screen.waitForTimeout(500);
  expect(await tabletText()).toBe(before);
});

test('R-18 — V빔 모달: 경로 · 원리 = M8-4-1 mechanism · 받으면 안 되는 경우 레이저 전체 기준', async ({ context }) => {
  const { screen } = await openBoth(context);
  await openProc(screen, 'cheek', 'V빔');
  await expect(modal(screen).getByTestId('modal-path')).toHaveText('레이저 › 혈관 › 브이빔');
  const snap = JSON.parse(readFileSync(path.resolve(__dirname, '../src/data/hub/hub-snapshot.json'), 'utf8'));
  const mech = snap.nodes['M8-4-1'].extracted.mechanism as string;
  await expect(sec(screen, 'mechanism').locator('p')).toHaveText(mech);
  await expect(sec(screen, 'mechanism')).toHaveAttribute('data-source', 'M8-4-1');
  await expect(sec(screen, 'contraindications')).toContainText('레이저 전체 기준');
  await expect(modal(screen).getByTestId('modal-more')).toBeVisible(); // 넘치면 아래 안내(W-6)
  await screen.screenshot({ path: path.join(SCREENS, 'loop2-modal.png') });
});

test('R-19 — 프락셔널레이저 모달: 경로 「레이저 › 프락셔널」 · 모든 섹션 레이저 전체 기준', async ({ context }) => {
  const { screen } = await openBoth(context);
  await openProc(screen, 'poreTexture', '프락셔널레이저');
  await expect(modal(screen).getByTestId('modal-path')).toHaveText('레이저 › 프락셔널');
  const secs = modal(screen).locator('[data-testid^=modal-sec-]');
  const n = await secs.count();
  expect(n).toBeGreaterThan(4);
  for (let i = 0; i < n; i++) await expect(secs.nth(i)).toContainText('레이저 전체 기준');
  await screen.screenshot({ path: path.join(SCREENS, 'loop2-modal-fractional.png') });
});

test('R-20 — ✕ · 바탕 · Esc 로 닫힘 · 열린 채 태블릿 필터 변경 → 모달 유지 · 뒤 카드만 바뀜 · 출처 줄', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await openProc(screen, 'eye', '필러');
  await expect(modal(screen).getByTestId('modal-source')).toContainText(/Procedure Hub\(stg\) · \d{4}-\d{2}-\d{2} 받음 · 목업 · 의학적 근거 아님/);
  await screen.getByTestId('procedure-modal-close').click();
  await expect(modal(screen)).toHaveCount(0);

  await openProc(screen, 'eye', '필러');
  await screen.getByTestId('procedure-modal-backdrop').click({ position: { x: 20, y: 20 } });
  await expect(modal(screen)).toHaveCount(0);

  await openProc(screen, 'eye', '필러');
  await screen.keyboard.press('Escape');
  await expect(modal(screen)).toHaveCount(0);

  await openProc(screen, 'eye', '필러');
  await tablet.getByTestId('filter-pore').click();
  await expect(card(screen, 'poreTexture')).toHaveAttribute('data-state', 'strong', { timeout: SEC });
  await expect(card(screen, 'eye')).toHaveAttribute('data-state', 'dim');
  await expect(modal(screen)).toBeVisible();
  await expect(modal(screen)).toHaveAttribute('data-hub', 'M2');
});

test('R-21 — 모달은 네트워크 요청 0(procedure-hub) · 탭 19개 모두 열림 · 한자 0', async ({ context }) => {
  const { screen } = await openBoth(context);
  const hubReqs: string[] = [];
  screen.on('request', (r) => r.url().includes('procedure-hub') && hubReqs.push(r.url()));
  const tabs = await screen.getByTestId('area-tab').all();
  expect(tabs.length).toBe(19);
  const ids = new Set<string>();
  for (const c of tabs) {
    const hub = (await c.getAttribute('data-hub'))!;
    ids.add(hub);
    await c.click();
    // 그 탭이 든 카드의 [자세히](보톡스·필러·아그네스는 두 카드에 있다)
    await c.locator('xpath=ancestor::*[starts-with(@data-testid,"area-card-")][1]').getByTestId('area-detail').click();
    await expect(modal(screen)).toHaveAttribute('data-hub', hub);
    expect(await modal(screen).locator('[data-testid^=modal-sec-]').count(), hub).toBeGreaterThan(3);
    expect(await modal(screen).innerText()).not.toMatch(/[一-鿿]/);
    await screen.keyboard.press('Escape');
    await expect(modal(screen)).toHaveCount(0);
  }
  expect(ids.size).toBe(16);
  expect(hubReqs).toEqual([]);
});

// ── 2루프(U-1 ~ U-4)
test('U-1 — 첫 탭 기본 · 탭 클릭은 설명만 교체(모달 X) · [자세히] → 모달 · 흐린 카드에서도 동작', async ({ context }) => {
  const { screen } = await openBoth(context);
  const desc = screen.getByTestId('area-desc-cheek');
  await expect(desc).toHaveAttribute('data-hub', 'M8-4-1'); // 첫 탭 V빔
  await expect(tab(screen, 'cheek', 'V빔')).toHaveAttribute('data-selected', 'true');
  const before = await desc.getByTestId('area-summary').innerText();
  await tab(screen, 'cheek', '피코토닝').click();
  await expect(desc).toHaveAttribute('data-hub', 'M8-1-2');
  await expect(tab(screen, 'cheek', '피코토닝')).toHaveAttribute('data-selected', 'true');
  await expect(tab(screen, 'cheek', 'V빔')).toHaveAttribute('data-selected', 'false');
  expect(await desc.getByTestId('area-summary').innerText()).not.toBe(before);
  await expect(desc).toContainText('피코토닝');
  await expect(modal(screen)).toHaveCount(0);
  await desc.getByTestId('area-detail').click();
  await expect(modal(screen)).toHaveAttribute('data-hub', 'M8-1-2');
  await screen.keyboard.press('Escape');
  // 흐린 카드(이마 — 추천 불필요)에서도 탭 · [자세히]
  await screen.getByTestId('filter-natural').click();
  await expect(card(screen, 'forehead')).toHaveAttribute('data-state', 'dim');
  await card(screen, 'forehead').getByTestId('area-detail').click();
  await expect(modal(screen)).toHaveAttribute('data-hub', 'M1-3-1');
  // 상향 대체 설명엔 「◯◯ 전체 기준」 — 프락셔널(M8-2)
  await screen.keyboard.press('Escape');
  await tab(screen, 'poreTexture', '프락셔널레이저').click();
  await expect(screen.getByTestId('area-desc-poreTexture').getByTestId('area-summary-inherited')).toHaveText('레이저 전체 기준');
  await expect(screen.getByTestId('area-desc-poreTexture').getByTestId('area-summary')).toHaveAttribute('data-source', 'M8');
  // 「Hub 원문」 문구는 3루프 V-1 로 뺐다 — 출처는 모달 아래 출처 줄에만
  await expect(screen.getByTestId('area-summary-source')).toHaveCount(0);
});

test('U-2 — 카드 클릭 = 그 카드만 strong · 재클릭 해제 · 필터 누르면 해제 · 태블릿 필터로도 해제 · 3D 필터 그대로', async ({ context }) => {
  const { tablet, screen } = await openViewer(context);
  await card(screen, 'forehead').click({ position: { x: 120, y: 240 } }); // 빈 곳
  await expectStrong(screen, ['forehead']);
  await expect(card(screen, 'forehead')).toHaveAttribute('data-selected', 'true');
  await expect(screen.getByTestId('filter-natural')).toHaveAttribute('data-active', 'true');
  await expect.poll(async () => (await anchors(screen)).find((a) => a.key === 'forehead')?.opacity ?? 0, { timeout: 5 * SEC }).toBeGreaterThan(0.9);
  await screen.screenshot({ path: path.join(SCREENS, 'loop2-card-selected.png') });
  // 다른 카드로 옮기기 → 재클릭 해제
  await card(screen, 'cheek').click({ position: { x: 120, y: 240 } });
  await expectStrong(screen, ['cheek']);
  await card(screen, 'cheek').click({ position: { x: 120, y: 240 } });
  await expectStrong(screen, ['eye', 'nasolabial', 'cheek', 'poreTexture']);
  // 탭 클릭도 그 카드를 고른다(해제하지 않음)
  await tab(screen, 'sebum', 'PDT').click();
  await expectStrong(screen, ['sebum']);
  await tab(screen, 'sebum', 'PDT').click();
  await expectStrong(screen, ['sebum']);
  // 화면 필터 → 해제
  await screen.getByTestId('filter-pore').click();
  await expectStrong(screen, ['poreTexture']);
  await expect(card(screen, 'sebum')).toHaveAttribute('data-selected', 'false');
  // 태블릿 필터 → 해제
  await card(screen, 'eye').click({ position: { x: 120, y: 240 } });
  await expectStrong(screen, ['eye']);
  await tablet.getByTestId('filter-redness').click();
  await expectStrong(screen, ['cheek']);
});

test('U-3·U-4 — 시술 사진 자리 · 부위 확대 사진 6개(지금 필터 텍스처를 따라감)', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  for (const k of AREA_KEYS) {
    await expect(screen.getByTestId(`area-photo-${k}`)).toContainText('사진');
    await expect(screen.getByTestId(`area-crop-${k}`)).toHaveAttribute('data-bg', '/m3d/tex/natural.jpg', { timeout: 10 * SEC });
    const bg = await screen.getByTestId(`area-crop-${k}`).evaluate((e) => getComputedStyle(e).backgroundImage);
    expect(bg, k).toContain('natural.jpg');
  }
  await tablet.getByTestId('filter-pore').click();
  for (const k of AREA_KEYS) {
    await expect(screen.getByTestId(`area-crop-${k}`)).toHaveAttribute('data-bg', '/m3d/tex/cool.jpg', { timeout: SEC });
    await expect(screen.getByTestId(`area-crop-${k}`)).toHaveAttribute('data-overlay', '/m3d/overlay/pore.png');
  }
  await tablet.getByTestId('filter-natural').click();
  await expect(screen.getByTestId('area-crop-eye')).toHaveAttribute('data-bg', '/m3d/tex/natural.jpg', { timeout: SEC });
  await screen.waitForTimeout(800);
  const vb = (await screen.getByTestId('screen-viewer').boundingBox())!;
  await screen.screenshot({ path: path.join(SCREENS, 'loop3-crops.png'), clip: { x: vb.x, y: vb.y, width: vb.width, height: vb.height - 96 } });
});

// ── 3루프(V-2 · V-3)
test('V-2·V-3 — [자세히]는 시술 제목 줄 오른쪽 · 부위 사진 ≥ 88px · 흐린 카드에서도 사진은 0.7 이상', async ({ context }) => {
  const { screen } = await openBoth(context);
  for (const k of AREA_KEYS) {
    const desc = screen.getByTestId(`area-desc-${k}`);
    const title = (await desc.locator('p').first().boundingBox())!;
    const btn = (await desc.getByTestId('area-detail').boundingBox())!;
    // 같은 줄: 세로 가운데가 겹치고 버튼이 제목 오른쪽
    expect(Math.abs(btn.y + btn.height / 2 - (title.y + title.height / 2)), `${k} 같은 줄`).toBeLessThan(6);
    expect(btn.x, `${k} 오른쪽`).toBeGreaterThan(title.x);
    const crop = (await screen.getByTestId(`area-crop-${k}`).boundingBox())!;
    expect(crop.width).toBeGreaterThanOrEqual(88);
    await expect(screen.getByTestId(`area-crop-${k}`)).toHaveAttribute('data-radius', /^(2[0-9]{2})$/);
    await expectCardFits(screen, k);
    // 점수 줄이 카드 오른쪽 밖으로 넘치지 않는다(피지 「점수 없음 · 5,470개」)
    const c = (await card(screen, k).boundingBox())!;
    const sc = (await screen.getByTestId(`area-score-${k}`).boundingBox())!;
    expect(sc.x + sc.width, `${k} 점수 넘침`).toBeLessThanOrEqual(c.x + c.width - 1);
  }
  for (const k of ['forehead', 'sebum']) {
    await expect(card(screen, k)).toHaveAttribute('data-state', 'dim');
    const o = await screen.getByTestId(`area-crop-wrap-${k}`).evaluate((e) => Number(getComputedStyle(e).opacity));
    expect(o, k).toBeGreaterThanOrEqual(0.7);
  }
});
