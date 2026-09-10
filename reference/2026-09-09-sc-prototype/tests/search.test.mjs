import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeDomain, parseSearch } from '../server/search.mjs';
import { makeWorkbook } from '../server/workbook.mjs';
import ExcelJS from 'exceljs';

const ad = (domain, title = '병원', extra = '') => `<li class="lst"><a class="lnk_head" href="https://ader.naver.com/random" onclick='return goOtherCR(this,"a=pwl_nop.tit&r=1&d="+urlencode("https://www.${domain}/")+"&u=")'><span class="lnk_tit">${title}</span></a><a class="lnk_url">${domain}</a>${extra}</li>`;
const page = body => `<title>키워드 : 네이버 검색</title><div id="content"><div id="power_link_body"><ul class="lst_type">${body}</ul></div></div>`;
test('count advertiser rows, not multiple links or nested sitelinks; normalise www', () => {
  const html = page(ad('first.kr', '다른 병원', '<ul><li class="item"><a>예약</a></li></ul>') + ad('daybeauclinic13.com', '데이뷰<strong>의원</strong>') + ad('last.kr'));
  const result = parseSearch(html, normalizeDomain('https://www.daybeauclinic13.com/some/path'));
  assert.equal(result.rank, 2); assert.equal(result.totalAds, 3); assert.equal(result.matches[0].title, '데이뷰의원');
});
test('domain matching rejects lookalikes and does not match mentions in title', () => {
  const r = parseSearch(page(ad('daybeauclinic13.com.evil.kr') + ad('other.kr', 'daybeauclinic13.com')), 'daybeauclinic13.com');
  assert.equal(r.status, 'not_found'); assert.equal(r.rank, null);
});
test('blocked pages and missing or changed layouts are errors, not absence', () => {
  for (const html of ['<title>접근 제한</title>', '<title>네이버 검색</title><div id="content"></div>', page('<li>unexpected</li>'), page('<li class="lst"><span>unknown ad</span></li>')]) assert.throws(() => parseSearch(html, 'daybeauclinic13.com'));
});
test('tracking URLs are rejected without resolving or clicking', () => assert.throws(() => normalizeDomain('https://ader.naver.com/v1/abc')));
test('duplicate advertiser creatives preserve positions and all matches', () => {
  const r = parseSearch(page(ad('target.kr') + ad('other.kr') + ad('target.kr')), 'target.kr');
  assert.equal(r.rank, 1); assert.deepEqual(r.matches.map(a => a.rank), [1, 3]);
});
test('xlsx preserves numeric rank, Korean labels, null absence and formula-like strings as text', async () => {
  const buffer = await makeWorkbook([
    { keyword: '=1+1', status: 'found', rank: 3, totalAds: 10, domain: 'target.kr', checkedAt: '2026-09-09T01:00:00Z' },
    { keyword: '인천필러', status: 'not_found', rank: null, totalAds: 10 },
    { keyword: '구월동필러', status: 'error', rank: null, message: 'HTTP 403' },
  ]);
  const wb = new ExcelJS.Workbook(); await wb.xlsx.load(buffer);
  const s = wb.getWorksheet('키워드 순위');
  assert.equal(s.getCell('A2').value, '=1+1'); assert.equal(s.getCell('A2').type, ExcelJS.ValueType.String);
  assert.equal(s.getCell('C2').value, 3); assert.equal(s.getCell('C3').value, null);
  assert.equal(s.getCell('B3').value, '미노출'); assert.equal(s.getCell('B4').value, '조회 실패');
  assert.equal(s.getCell('G2').value, '2026-09-09 10:00:00');
});
