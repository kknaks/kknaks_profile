import { expect, test, type Page } from '@playwright/test';

// 같은 브라우저(컨텍스트)의 탭 두 개 — BroadcastChannel 은 같은 출처 같은 컨텍스트에서만 닿는다
const SEC = 1000; // AC: 「1초 안에」

async function openBoth(context: import('@playwright/test').BrowserContext) {
  const tablet = await context.newPage();
  await tablet.setViewportSize({ width: 1180, height: 820 });
  await tablet.goto('/tablet');
  await tablet.evaluate(() => localStorage.clear());
  await tablet.reload();
  await expect(tablet.getByTestId('tablet-root')).toBeVisible();
  const screen = await context.newPage();
  await screen.setViewportSize({ width: 1920, height: 1080 });
  await screen.goto('/screen');
  await expect(screen.getByTestId('screen-root')).toBeVisible();
  await expect(screen.getByTestId('screen-link')).toHaveAttribute('data-on', 'true', { timeout: 5 * SEC });
  return { tablet, screen };
}

const addProc = (tablet: Page, name: string) => tablet.locator(`[data-testid=procedure-row][data-name="${name}"]`).first().click();
const cartRow = (tablet: Page, name: string) => tablet.locator(`[data-testid=cart-row][data-name="${name}"]`);
const planRow = (screen: Page, name: string) => screen.locator(`[data-testid=plan-row][data-name="${name}"]`);

test('AC-5·6·7·14 — 카트·항목 할인·무료·전체 할인·체크 해제·삭제가 1초 안에 큰 화면에', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('view-all').click();
  await expect(tablet.getByTestId('procedure-row')).toHaveCount(48);

  // AC-5
  await addProc(tablet, '눈가 보톡스');
  await expect(planRow(screen, '눈가 보톡스')).toBeVisible({ timeout: SEC });
  await expect(planRow(screen, '눈가 보톡스').getByTestId('plan-row-price')).toHaveAttribute('data-value', '120000', { timeout: SEC });

  // AC-14 카트
  await addProc(tablet, '리쥬란 HB 1회');
  await addProc(tablet, '울쎄라 하안면');
  await cartRow(tablet, '리쥬란 HB 1회').getByTestId('item-free').click();
  await cartRow(tablet, '울쎄라 하안면').getByTestId('item-discount').selectOption('10');
  await expect(screen.getByTestId('plan-total')).toHaveAttribute('data-value', '2100000', { timeout: SEC });
  await expect(screen.getByTestId('plan-total-vat')).toHaveAttribute('data-value', '2310000', { timeout: SEC });
  await expect(tablet.getByTestId('tablet-total')).toHaveText('2,100,000원');
  await expect(tablet.getByTestId('tablet-total-vat')).toHaveText('2,310,000원');

  // AC-7 전체 10% → round(totalVat × 0.9)
  await tablet.getByTestId('rate-10').click();
  await expect(screen.getByTestId('plan-final')).toHaveAttribute('data-value', '2079000', { timeout: SEC });
  await expect(tablet.getByTestId('tablet-final')).toHaveText('2,079,000원');
  await expect(screen.getByTestId('plan-final')).toHaveText('2,079,000', { timeout: 2 * SEC }); // 트윈 300ms 끝난 뒤 글자도 같다
  // 협찬 100% → 0원
  await tablet.getByTestId('rate-100').click();
  await expect(screen.getByTestId('plan-final')).toHaveAttribute('data-value', '0', { timeout: SEC });
  await tablet.getByTestId('rate-100').click();

  // AC-6 항목 할인 20%
  await cartRow(tablet, '울쎄라 하안면').getByTestId('item-discount').selectOption('20');
  await expect(planRow(screen, '울쎄라 하안면').getByTestId('plan-row-price')).toHaveAttribute('data-value', '1760000', { timeout: SEC });
  // 체크 해제 → 큰 화면에서 행이 빠지고 합계가 준다
  await cartRow(tablet, '눈가 보톡스').click();
  await expect(planRow(screen, '눈가 보톡스')).toHaveCount(0, { timeout: SEC });
  await expect(screen.getByTestId('plan-total')).toHaveAttribute('data-value', '1760000', { timeout: SEC });
  // 삭제
  await cartRow(tablet, '울쎄라 하안면').getByTestId('item-remove').click();
  await expect(planRow(screen, '울쎄라 하안면')).toHaveCount(0, { timeout: SEC });
  // 무료 해제 → 금액 복귀
  await cartRow(tablet, '리쥬란 HB 1회').getByTestId('item-free').click();
  await expect(planRow(screen, '리쥬란 HB 1회').getByTestId('plan-row-price')).toHaveAttribute('data-value', '200000', { timeout: SEC });
});

test('AC-8·9 — 필터 양방향 · 피부 분석 항목 강조', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('filter-pore').click();
  await expect(screen.getByTestId('filter-pore')).toHaveAttribute('data-active', 'true', { timeout: SEC });
  await expect(screen.getByTestId('bar-pore')).toHaveAttribute('data-highlight', 'true', { timeout: SEC });

  await screen.getByTestId('filter-redness').click();
  await expect(tablet.getByTestId('filter-redness')).toHaveAttribute('data-active', 'true', { timeout: SEC });
  await expect(screen.getByTestId('filter-redness')).toHaveAttribute('data-active', 'true', { timeout: SEC });

  await tablet.getByTestId('analysis-item-fineWrinkle').click();
  await expect(screen.getByTestId('bar-fineWrinkle')).toHaveAttribute('data-highlight', 'true', { timeout: SEC });
  await expect(screen.getByTestId('filter-fineWrinkle')).toHaveAttribute('data-active', 'true', { timeout: SEC });
  await expect(screen.getByTestId('focus-card')).toHaveAttribute('data-filter', 'fineWrinkle');
  await expect(screen.getByTestId('region-map')).toBeVisible();
  // 다시 누르면 해제(필터는 그대로)
  await tablet.getByTestId('analysis-item-fineWrinkle').click();
  await expect(tablet.getByTestId('analysis-item-fineWrinkle')).toHaveAttribute('data-focus', 'false');
});

test('AC-10 — 새로고침해도 같은 상태', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('view-all').click();
  await addProc(tablet, '눈가 보톡스');
  await tablet.getByTestId('rate-15').click();
  await tablet.getByTestId('filter-pigment').click();
  await expect(planRow(screen, '눈가 보톡스')).toBeVisible({ timeout: SEC });

  await screen.reload();
  await expect(planRow(screen, '눈가 보톡스')).toBeVisible({ timeout: SEC });
  await expect(screen.getByTestId('plan-discount')).toContainText('15%', { timeout: SEC });
  await expect(screen.getByTestId('filter-pigment')).toHaveAttribute('data-active', 'true', { timeout: SEC });

  await tablet.reload();
  await expect(cartRow(tablet, '눈가 보톡스')).toBeVisible();
  await expect(tablet.getByTestId('filter-pigment')).toHaveAttribute('data-active', 'true');
  await expect(planRow(screen, '눈가 보톡스')).toBeVisible();
});

test('AC-11 — 큰 화면을 닫으면 5초 안에 「큰 화면 없음」, 다시 열면 「연결됨」', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await expect(tablet.getByTestId('tablet-screen-link')).toHaveAttribute('data-on', 'true', { timeout: 5 * SEC });
  await screen.close();
  await expect(tablet.getByTestId('tablet-screen-link')).toHaveAttribute('data-on', 'false', { timeout: 5 * SEC });
  await expect(tablet.getByTestId('tablet-screen-link')).toContainText('큰 화면 없음');
  const again = await context.newPage();
  await again.goto('/screen');
  await expect(tablet.getByTestId('tablet-screen-link')).toHaveAttribute('data-on', 'true', { timeout: 5 * SEC });
  await expect(tablet.getByTestId('tablet-screen-link')).toContainText('큰 화면 연결됨');
});

test('AC-12 — 가격 표시 끄면 금액·합계가 사라지고 시술명은 남는다 · 빈 카트 문구', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await expect(screen.getByTestId('plan-empty')).toBeVisible();
  await tablet.getByTestId('view-all').click();
  await addProc(tablet, '눈가 보톡스');
  await expect(screen.getByTestId('plan-totals')).toBeVisible({ timeout: SEC });
  await tablet.getByTestId('toggle-price').click();
  await expect(screen.getByTestId('plan-totals')).toHaveCount(0, { timeout: SEC });
  await expect(screen.getByTestId('plan-row-price')).toHaveCount(0);
  await expect(planRow(screen, '눈가 보톡스')).toBeVisible();
  await expect(screen.getByTestId('plan-price-hidden')).toBeVisible();
});

test('AC-18 — 가격 목록 48건 · 「추천」은 규칙 행만 · 재방문이면 첫방문이벤트 없음', async ({ context }) => {
  const { tablet } = await openBoth(context);
  await expect(tablet.getByTestId('view-recommend')).toHaveText(/추천 \d+/);
  const recRows = await tablet.getByTestId('procedure-row').evaluateAll((els) => els.map((e) => e.getAttribute('data-name')));
  expect(recRows).toContain('눈가 보톡스');
  expect(recRows).toContain('엑셀V 1회');
  expect(recRows).not.toContain('겨드랑이 제모');
  expect(recRows).not.toContain('사각턱 보톡스');
  await expect(tablet.getByTestId('recommend-count')).toHaveText('6');
  await tablet.getByTestId('view-all').click();
  await expect(tablet.getByTestId('procedure-row')).toHaveCount(48);

  await tablet.getByTestId('consult-type-trigger').click();
  await tablet.getByRole('option', { name: '재방문' }).click();
  await expect(tablet.locator('[data-testid=procedure-row][data-price-type="첫방문이벤트"]')).toHaveCount(0);
  await expect(tablet.getByTestId('ptype-chip-첫방문이벤트')).toHaveCount(0);
  // 데모 가격표에 첫방문이벤트 행이 0건이라 재방문 전후 48건 그대로(데이터상 0건 — 규칙은 단위 테스트로 확인)
  await expect(tablet.getByTestId('procedure-row')).toHaveCount(48);
});

test('AC-15·16·17 — 한자·−1 없음 · 좌/우 ⓘ 는 태블릿만 · 금지어 없음', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await expect(screen.getByTestId('score-bars')).toBeVisible();
  const han = /[一-鿿]/;
  for (const f of ['natural', 'fineWrinkle', 'deepWrinkle', 'pore', 'redness', 'pigment', 'porphyrin']) {
    await screen.getByTestId(`filter-${f}`).click();
    await expect(screen.getByTestId(`filter-${f}`)).toHaveAttribute('data-active', 'true', { timeout: SEC });
    const text = await screen.locator('body').innerText();
    expect(text).not.toMatch(han);
    expect(text).not.toMatch(/(^|[^0-9])[-−]1(?![0-9])/);
    expect(text).not.toMatch(/진단|질환|치료|환자/);
    expect(text).not.toMatch(/좌\/우|좌 |우 |왼쪽|오른쪽/);
  }
  for (const t of ['analysis', 'checklist', 'chart', 'raw']) {
    await tablet.getByTestId(`tab-${t}`).click();
    const text = await tablet.locator('body').innerText();
    expect(text).not.toMatch(han);
    expect(text).not.toMatch(/(^|[^0-9])[-−]1(?![0-9])/);
  }
  await tablet.getByTestId('tab-analysis').click();
  await expect(tablet.getByTestId('analysis-item-deepWrinkle')).toContainText('좌/우');
  await expect(tablet.getByTestId('side-note')).toHaveCount(2); // 측정치는 항목당 2개까지(SPEC §3-3)
});

test('fix1 W-3 — 필터를 직접 바꾸면 피부 분석 강조가 풀리고 C·B·A2 가 같은 대상', async ({ context }) => {
  const { tablet, screen } = await openBoth(context);
  await tablet.getByTestId('analysis-item-pore').click();
  await expect(screen.getByTestId('bar-pore')).toHaveAttribute('data-highlight', 'true', { timeout: SEC });
  // 큰 화면에서 붉은기로 바꾼다 → 강조도 붉은기, 모공 강조·태블릿 선택은 풀림
  await screen.getByTestId('filter-redness').click();
  await expect(screen.getByTestId('bar-redness')).toHaveAttribute('data-highlight', 'true', { timeout: SEC });
  await expect(screen.getByTestId('bar-pore')).toHaveAttribute('data-highlight', 'false');
  await expect(screen.getByTestId('cat-inflammation')).toHaveAttribute('data-focus', 'true');
  await expect(screen.getByTestId('focus-card')).toHaveAttribute('data-filter', 'redness');
  await expect(tablet.getByTestId('analysis-item-pore')).toHaveAttribute('data-focus', 'false');
  // 태블릿에서 바꿔도 같다
  await tablet.getByTestId('analysis-item-pore').click();
  await tablet.getByTestId('filter-pigment').click();
  await expect(screen.getByTestId('bar-pigment')).toHaveAttribute('data-highlight', 'true', { timeout: SEC });
  await expect(screen.getByTestId('bar-pore')).toHaveAttribute('data-highlight', 'false');
});

test('fix1 W-1·W-2 — 태블릿 누르는 것은 32px 이상 · 대분류에 등급 배지 · 측정치 2개까지', async ({ context }) => {
  const { tablet } = await openBoth(context);
  await expect(tablet.getByTestId('stage-canvas')).toHaveAttribute('data-scale', '1');
  await tablet.getByTestId('view-all').click();
  await tablet.locator('[data-testid=procedure-row][data-name="눈가 보톡스"]').click();
  await tablet.getByTestId('recommend-chip-M1').click();
  const sel = [
    '[data-testid=item-discount]', '[data-testid=item-free]', '[data-testid=item-remove]', '[data-testid=cart-clear]',
    '[data-testid^=rate-]', '[data-testid^=filter-]', '[data-testid^=recommend-chip-]', '[data-testid^=cat-chip-]',
    '[data-testid^=ptype-chip-]', '[data-testid=view-all]', '[data-testid=view-recommend]', '[data-testid^=tab-]',
    '[data-testid=toggle-price]', '[data-testid=reset-session]', '[data-testid=open-screen-window]', '[data-testid=camera-reset]',
    '[data-testid=consult-type-trigger]', '[data-testid=procedure-row]', '[data-testid=recommend-goto-price]',
  ];
  const small: string[] = [];
  for (const q of sel) {
    for (const h of await tablet.locator(q).evaluateAll((els) => els.map((e) => [e.getAttribute('data-testid'), e.getBoundingClientRect().height] as const))) {
      if (h[1] < 31.5) small.push(`${h[0]}=${h[1]}`);
    }
  }
  await tablet.getByTestId('tab-checklist').click();
  for (const h of await tablet.locator('[data-testid^=check-]').evaluateAll((els) => els.map((e) => e.getBoundingClientRect().height))) if (h < 31.5) small.push(`check=${h}`);
  expect(small).toEqual([]);

  await tablet.getByTestId('tab-analysis').click();
  for (const k of ['inflammation', 'tone', 'texture', 'aging']) await expect(tablet.getByTestId(`analysis-cat-${k}`).locator('[data-grade]')).toHaveCount(1);
  await expect(tablet.getByTestId('analysis-item-pore')).not.toContainText('깊은 모공 비율');
});
