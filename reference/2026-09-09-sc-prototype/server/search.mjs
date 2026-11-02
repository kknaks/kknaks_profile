import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { load } from 'cheerio';

const exec = promisify(execFile);
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
export const searchUrl = keyword => `https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=${encodeURIComponent(keyword)}`;

export function normalizeDomain(value) {
  const raw = String(value || '').trim();
  let url;
  try { url = new URL(raw.includes('://') ? raw : `https://${raw}`); } catch { throw new Error('타겟 사이트 주소를 입력해 주세요.'); }
  const host = url.hostname.toLowerCase().replace(/^www\./, '');
  if (!['http:', 'https:'].includes(url.protocol) || !host.includes('.') || url.username || url.password) throw new Error('올바른 사이트 도메인을 입력해 주세요.');
  if (['ader.naver.com', 'adcr.naver.com'].includes(host)) throw new Error('광고 추적 링크 대신 표시 도메인(예: daybeauclinic13.com)을 입력해 주세요.');
  return host;
}

const clean = value => value.replace(/\s+/g, ' ').trim();
export function parseSearch(html, domain) {
  const $ = load(html);
  if (!$('title').text().includes('네이버 검색') || !$('#content').length) throw new Error('정상 검색 페이지를 받지 못했습니다. 잠시 후 다시 조회해 주세요.');
  const section = $('#power_link_body');
  if (!section.length) {
    // Do not report an unrecognised layout as a confident absence.
    throw new Error('파워링크 영역을 확인할 수 없습니다. 광고 미제공 또는 검색 구조 변경일 수 있습니다.');
  }
  const items = section.find('ul.lst_type').first().children('li.lst');
  if (!items.length) throw new Error('광고 목록을 읽지 못했습니다. 네이버에서 직접 확인해 주세요.');
  const ads = items.map((i, el) => {
    const item = $(el), titleLink = item.find('a.lnk_head').first();
    const handler = titleLink.attr('onclick') || '';
    const destination = handler.match(/urlencode\(["'](https?:\/\/[^"']+)["']\)/)?.[1];
    const displayUrl = clean(item.find('.lnk_url').first().text());
    let host = '';
    try { host = normalizeDomain(destination || displayUrl); } catch { /* preserve unknown rows for rank */ }
    return { rank: i + 1, title: clean(item.find('.lnk_tit').first().text()), domain: host, displayUrl, description: clean(item.find('.link_desc').first().text()) };
  }).get();
  if (ads.some(ad => !ad.title || !ad.domain)) throw new Error('일부 광고 정보를 읽지 못해 정확한 순위를 계산할 수 없습니다.');
  const matches = ads.filter(ad => ad.domain === domain);
  return { status: matches.length ? 'found' : 'not_found', rank: matches[0]?.rank ?? null, matches, totalAds: ads.length, ads };
}

export async function checkKeyword(keyword, domain) {
  const url = searchUrl(keyword);
  const base = { keyword, domain, searchUrl: url, checkedAt: new Date().toISOString(), scope: 'PC 통합검색 · 첫 파워링크' };
  try {
    const { stdout } = await exec('curl', ['--silent', '--show-error', '--compressed', '--max-time', '25', '--max-filesize', '8388608', '--user-agent', UA, '--write-out', '\n%{http_code}', url], { maxBuffer: 10 * 1024 * 1024, timeout: 28000 });
    const split = stdout.lastIndexOf('\n'), status = stdout.slice(split + 1).trim();
    if (status !== '200') throw new Error(`네이버 응답 HTTP ${status}. 잠시 후 다시 조회해 주세요.`);
    return { ...base, ...parseSearch(stdout.slice(0, split), domain) };
  } catch (error) {
    return { ...base, status: 'error', rank: null, totalAds: null, matches: [], ads: [], message: error.killed || error.code ? '검색 요청이 실패했거나 시간이 초과되었습니다. 다시 조회해 주세요.' : error.message };
  }
}
