import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { load } from 'cheerio';
import sharp from 'sharp';
import { blogBatches } from './blog-browser.mjs';
const exec = promisify(execFile);
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
export const blogUrl = keyword => `https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_hty.top&query=${encodeURIComponent(keyword)}`;
const clean = value => String(value || '').replace(/새 창 열림/g, '').replace(/\s+/g, ' ').trim();
const compact = value => clean(value).replace(/\s/g, '').toLowerCase();
export function parseBlogList(html) {
  const $ = load(html);
  if (!$('title').text().includes('블로그검색')) throw new Error('정상 블로그 검색 페이지를 받지 못했습니다.');
  const cards = $('[data-template-id="ugcItem"]');
  if (!cards.length) throw new Error('블로그 결과 목록을 읽지 못했습니다. 검색 결과가 없거나 구조가 바뀌었을 수 있습니다.');
  return cards.map((i, el) => {
    const card = $(el);
    const link = card.find('a').filter((_, a) => $(a).find('[class*="text-type-headline"]').length > 0).first();
    const title = clean(link.find('[class*="text-type-headline"]').first().text());
    const url = link.attr('href');
    if (!title || !/^https?:\/\//.test(url || '')) throw new Error('일부 글의 제목을 읽지 못해 순위를 계산할 수 없습니다.');
    const snippets = card.find('a').filter((_, a) => $(a).attr('href') === url && $(a).find('[class*="text-type-body1"]').length).first();
    const thumbnailUrls = [...new Set(card.find('a').filter((_, a) => $(a).attr('href') === url).find('img').map((_, img) => $(img).attr('src') || $(img).attr('data-src')).get().filter(Boolean))];
    const blogger = card.find('a').filter((_, a) => /blog\.naver\.com\/[^/?]+\/?$/.test($(a).attr('href') || '')).map((_, a) => clean($(a).text())).get().find(Boolean) || '';
    return { rank: i + 1, title, url, snippet: clean(snippets.find('[class*="text-type-body1"]').first().text()), blogger, thumbnailUrls };
  }).get();
}
export function matchBlogKeyword(rows, target) {
  if (!compact(target)) throw new Error('타겟 키워드를 입력해 주세요.');
  const matches = rows.filter(row => compact(`${row.title} ${row.snippet}`).includes(compact(target)));
  return { status: matches.length ? 'found' : 'not_found', rank: matches[0]?.rank ?? null, matches, total: rows.length };
}
// 63 low-frequency DCT bits (DC excluded). Compare visual identity, not semantics.
export async function imageHash(buffer) {
  const pixels = await sharp(buffer, { limitInputPixels: 25000000 }).rotate().flatten({ background: '#fff' }).resize(32, 32, { fit: 'fill' }).greyscale().raw().toBuffer();
  const coefficients = [];
  for (let u = 0; u < 8; u++) for (let v = 0; v < 8; v++) {
    if (u === 0 && v === 0) continue;
    let sum = 0;
    for (let x = 0; x < 32; x++) for (let y = 0; y < 32; y++) sum += pixels[y * 32 + x] * Math.cos((2 * x + 1) * u * Math.PI / 64) * Math.cos((2 * y + 1) * v * Math.PI / 64);
    coefficients.push(sum);
  }
  const median = [...coefficients].sort((a,b) => a-b)[31];
  return coefficients.map(value => value > median ? '1' : '0').join('');
}
export const hashDistance = (a, b) => [...a].reduce((n, bit, i) => n + Number(bit !== b[i]), 0);
export async function mapConcurrent(items, limit, fn) {
  const results = new Array(items.length); let index = 0;
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (index < items.length) { const i = index++; results[i] = await fn(items[i], i); }
  }));
  return results;
}
async function curl(url, { binary = false, seconds = 20 } = {}) {
  const { stdout } = await exec('curl', ['--silent','--show-error','--fail','--compressed','--max-time',String(seconds),'--max-filesize','6291456','--user-agent',UA,url], { encoding: binary ? 'buffer' : 'utf8', maxBuffer: 7 * 1024 * 1024, timeout: (seconds + 2) * 1000 });
  return stdout;
}
export function decodeTargetImage(data) {
  if (typeof data !== 'string' || !/^data:image\/(png|jpeg|webp);base64,/.test(data)) throw new Error('PNG, JPG, WebP 이미지를 선택해 주세요.');
  const buffer = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64');
  if (!buffer.length || buffer.length > 4 * 1024 * 1024) throw new Error('이미지는 4MB 이하로 선택해 주세요.');
  return buffer;
}
function imageUrl(source) {
  const url = new URL(source);
  if (url.protocol !== 'https:' || url.hostname !== 'search.pstatic.net' || !['/common/', '/sunny/'].includes(url.pathname)) throw new Error('지원하지 않는 검색 썸네일 주소입니다.');
  // Download the exact thumbnail URL supplied by the search result.
  return url.href;
}
export async function checkBlog(keyword, { targetType = 'keyword', target = '', imageData, imageName = '' } = {}) {
  const started = Date.now();
  const base = { keyword, target: targetType === 'image' ? imageName || '업로드 이미지' : target, targetType, searchUrl: blogUrl(keyword), scope: `PC 네이버 블로그 탭 · 초기 목록 + 최대 3회 스크롤 · ${targetType === 'image' ? '검색 썸네일 pHash(거리 6 이하)' : '제목·요약 키워드 일치'}` };
  try {
    if (typeof keyword !== 'string' || !keyword.trim() || keyword.length > 100) throw new Error('검색 키워드는 1~100자로 입력해 주세요.');
    if (!['keyword', 'image'].includes(targetType)) throw new Error('타겟 종류를 확인해 주세요.');
    if (targetType === 'keyword' && (typeof target !== 'string' || !target.trim() || target.length > 100)) throw new Error('타겟 키워드는 1~100자로 입력해 주세요.');
    const targetBuffer = targetType === 'image' ? decodeTargetImage(imageData) : null;
    const targetHashes = targetBuffer ? await Promise.all([imageHash(targetBuffer), imageHash(await sharp(targetBuffer).rotate().resize(250,208,{fit:'cover'}).toBuffer())]) : [];
    let result, lastScrolls = 0;
    const byUrl = new Map();
    for await (const batch of blogBatches(blogUrl(keyword))) {
    lastScrolls = batch.scrolls;
    const rows = parseBlogList(batch.html);
    console.info('[blog]', JSON.stringify({ keyword, stage: 'batch', scrolls: batch.scrolls, total: rows.length }));
    if (targetType === 'keyword') result = matchBlogKeyword(rows, target);
    else {
      const allUrls = [...new Set(rows.flatMap(row => row.thumbnailUrls))];
      const urls = allUrls.filter(url => !byUrl.has(url));
      if (!allUrls.length) throw new Error('비교할 검색 썸네일을 읽지 못했습니다.');
      console.info('[blog]', JSON.stringify({ keyword, stage: 'images-start', images: urls.length, concurrency: 8 }));
      const checks = await mapConcurrent(urls, 8, async url => {
        try { const hash = await imageHash(await curl(imageUrl(url), { binary: true, seconds: 8 })); return { url, distance: Math.min(...targetHashes.map(targetHash => hashDistance(targetHash, hash))) }; }
        catch { return { url, error: true }; }
      });
      for (const check of checks) byUrl.set(check.url, check);
      const matches = rows.flatMap(row => {
        const best = row.thumbnailUrls.map(url => byUrl.get(url)).filter(check => !check.error).sort((a,b) => a.distance - b.distance)[0];
        return best && best.distance <= 6 ? [{ ...row, imageUrl: best.url, hashDistance: best.distance }] : [];
      });
      const rank = matches[0]?.rank ?? null;
      const failedBefore = rows.some(row => (rank === null || row.rank < rank) && row.thumbnailUrls.some(url => byUrl.get(url).error));
      if (failedBefore) throw new Error('일부 썸네일을 읽지 못해 첫 노출 순위를 확정할 수 없습니다. 다시 조회해 주세요.');
      result = { status: matches.length ? 'found' : 'not_found', rank, matches, total: rows.length, comparedImages: byUrl.size };
    }
    if (result.status === 'found') break;
    }
    if (!result) throw new Error('블로그 결과를 읽지 못했습니다.');
    console.info('[blog]', JSON.stringify({ keyword, stage: 'complete', elapsedMs: Date.now() - started, rank: result.rank, total: result.total, scrolls: lastScrolls }));
    return { ...base, ...result, scrolls: lastScrolls, checkedAt: new Date().toISOString(), message: result.status === 'not_found' ? '이번 블로그 탭 초기 목록 + 최대 3회 스크롤에서 찾지 못했습니다.' : '' };
  } catch (error) {
    console.info('[blog]', JSON.stringify({ keyword, stage: 'error', elapsedMs: Date.now() - started, message: error.message.slice(0,200) }));
    return { ...base, status: 'error', rank: null, matches: [], total: null, checkedAt: new Date().toISOString(), message: /[가-힣]/.test(error.message) && !error.code ? error.message : '블로그 조회 또는 이미지 처리가 실패했습니다. 잠시 후 다시 확인해 주세요.' };
  }
}
