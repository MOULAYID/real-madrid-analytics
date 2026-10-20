import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const evidence = 'docs/previews';
await fs.mkdir(evidence, { recursive: true });
const browser = await chromium.launch();
const report = { public: [], streamlit: [] };
const viewports = [{ width: 1440, height: 1000 }, { width: 390, height: 844 }];

async function assertNoRawMarkup(page) {
  const text = await page.locator('body').innerText();
  assert(!/<\/?(?:div|span|style)(?:\s|>)/i.test(text), 'Raw HTML leaked into the visible UI');
}

try {
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    const localRequests = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => {
      if (/https?:\/\/(localhost|127\.0\.0\.1):8000\//.test(request.url())) localRequests.push(request.url());
    });
    const response = await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
    assert(response.ok());
    await page.locator('.kpi-card .kpi-value').first().waitFor({ timeout: 30000 });
    await assertNoRawMarkup(page);
    const nav = page.locator('nav.nav-tabs button');
    assert.equal(await nav.count(), 8);
    for (let index = 0; index < 8; index++) {
      await nav.nth(index).click();
      const main = await page.locator('main').innerText();
      assert(main.trim().length > 80, 'Empty public dashboard tab ' + index);
      assert(!/Loading .+Analytics/i.test(main), 'Dashboard stayed in loading state');
    }
    await nav.first().click();
    const original = await page.locator('.kpi-card .kpi-value').first().innerText();
    await page.locator('select').first().selectOption('2014/15');
    await page.waitForFunction(before => document.querySelector('.kpi-card .kpi-value')?.innerText !== before, original);
    await page.locator('select').first().selectOption('2024/25');
    await page.waitForFunction(before => document.querySelector('.kpi-card .kpi-value')?.innerText === before, original);
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Export', exact: true }).click();
    const download = await downloadPromise;
    assert.equal(download.suggestedFilename(), 'financials.csv');
    assert.equal(await download.failure(), null);
    assert.deepEqual(localRequests, [], 'Public UI attempted a request to a visitor local API');
    assert.deepEqual(errors, [], 'Public dashboard JavaScript errors');
    await page.waitForTimeout(1600);
    const layout = await page.evaluate(() => ({ client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }));
    assert(layout.scroll <= layout.client + 1, 'Public page overflows viewport');
    await page.screenshot({ path: evidence + '/public-' + viewport.width + '.png', fullPage: false, animations: 'disabled' });
    report.public.push({ viewport, tabs: 8, seasonSwitch: true, exportCSV: true, localAPIRequests: localRequests.length, layout });
    await page.close();
  }

  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    await page.goto('http://127.0.0.1:8501/', { waitUntil: 'domcontentloaded' });
    await page.locator('.kpi-card').first().waitFor({ timeout: 60000 });
    await page.getByRole('tab', { name: /ESG/ }).waitFor({ timeout: 60000 });
    await page.waitForTimeout(1000);
    assert.equal(await page.locator('[data-testid="stException"]').count(), 0, 'Streamlit raised an exception');
    await assertNoRawMarkup(page);
    const tabs = page.getByRole('tab');
    assert.equal(await tabs.count(), 8);
    for (let index = 0; index < 8; index++) {
      await tabs.nth(index).click();
      await assertNoRawMarkup(page);
      assert.equal(await page.locator('[data-testid="stException"]').count(), 0);
    }
    await tabs.first().click();
    assert.equal(await page.locator('.kpi-card:visible').count(), 8, 'Expected eight executive KPI cards');
    assert.equal(await page.locator('.kpi-card:visible .kpi-tooltip').count(), 8, 'KPI explanations missing');
    const layout = await page.evaluate(() => ({ client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }));
    assert(layout.scroll <= layout.client + 1, 'Streamlit page overflows viewport');
    await page.screenshot({ path: evidence + '/streamlit-' + viewport.width + '.png', fullPage: false, animations: 'disabled' });
    report.streamlit.push({ viewport, tabs: 8, kpiCards: 8, rawMarkup: false, exceptions: 0, layout });
    await page.close();
  }
  await fs.writeFile(evidence + '/report.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally {
  await browser.close();
}
