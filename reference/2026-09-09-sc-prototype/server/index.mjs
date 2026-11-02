import express from 'express';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { checkKeyword, normalizeDomain } from './search.mjs';
import { checkPlace, closePlaceBrowser } from './place.mjs';
import { checkBlog } from './blog.mjs';
import { makeWorkbook } from './workbook.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const app = express();
app.use(express.json({ limit: '7mb' }));
app.get('/api/health', (_, res) => res.json({ ok: true }));
let busy = false;
let nextAllowed = 0;
app.post('/api/check', async (req, res) => {
  let domain;
  const keyword = req.body.keyword;
  try {
    if (typeof keyword !== 'string' || !keyword.trim() || keyword.length > 100) throw new Error('키워드는 1~100자로 입력해 주세요.');
    domain = normalizeDomain(req.body.domain);
  } catch (error) { return res.status(400).json({ message: error.message }); }
  if (busy || Date.now() < nextAllowed) return res.status(429).json({ message: '다른 조회가 진행 중입니다. 잠시 후 다시 조회해 주세요.' });
  busy = true;
  try { res.json(await checkKeyword(keyword.trim(), domain)); }
  finally { busy = false; nextAllowed = Date.now() + 700; }
});
app.post('/api/blog/check', async (req, res) => {
  if (busy || Date.now() < nextAllowed) return res.status(429).json({ message: '다른 조회가 진행 중입니다. 잠시 후 다시 조회해 주세요.' });
  busy = true;
  try { res.json(await checkBlog(req.body.keyword, req.body)); }
  finally { busy = false; nextAllowed = Date.now() + 700; }
});
app.post('/api/place/check', async (req, res) => {
  const { keyword, target } = req.body;
  if (typeof keyword !== 'string' || !keyword.trim() || keyword.length > 100 || typeof target !== 'string' || !target.trim() || target.length > 50) return res.status(400).json({ message: '키워드는 1~100자, 병원명은 1~50자로 입력해 주세요.' });
  if (busy || Date.now() < nextAllowed) return res.status(429).json({ message: '다른 조회가 진행 중입니다. 잠시 후 다시 조회해 주세요.' });
  busy = true;
  try { res.json(await checkPlace(keyword.trim(), target.trim())); }
  finally { busy = false; nextAllowed = Date.now() + 2000; }
});
process.on('SIGTERM', async () => { await closePlaceBrowser(); process.exit(0); });
process.on('SIGINT', async () => { await closePlaceBrowser(); process.exit(0); });
app.post('/api/export', async (req, res) => {
  const rows = req.body.rows;
  if (!Array.isArray(rows) || !rows.length || rows.length > 50 || rows.some(row => !row || typeof row.keyword !== 'string')) return res.status(400).json({ message: '저장할 결과는 1~50개여야 합니다.' });
  try {
    const buffer = await makeWorkbook(rows, { place: req.body.mode === 'place', blog: req.body.mode === 'blog' });
    res.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    res.set('Content-Disposition', 'attachment; filename="naver-keyword-ranks.xlsx"');
    res.send(Buffer.from(buffer));
  } catch { res.status(400).json({ message: '엑셀을 만들지 못했습니다. 결과를 다시 조회해 주세요.' }); }
});
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(root, 'dist')));
  app.get('*', (_, res) => res.sendFile(path.join(root, 'dist/index.html')));
}
app.listen(Number(process.env.PORT || 18000), '127.0.0.1', () => console.log(`SCAX API: http://localhost:${process.env.PORT || 18000}`)).on('error', error => { console.error(`백엔드 실행 실패: ${error.message}`); process.exit(1); });
