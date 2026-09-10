import ExcelJS from 'exceljs';
export const labels = { found: '노출', not_found: '미노출', error: '조회 실패', cancelled: '중단', pending: '대기' };
export async function makeWorkbook(rows, { place = false, blog = false } = {}) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = 'SCAX';
  const sheet = workbook.addWorksheet('키워드 순위', { views: [{ state: 'frozen', ySplit: 1 }] });
  sheet.columns = (blog ? [
    ['키워드', 'keyword', 26], ['상태', 'status', 14], ['노출 순위', 'rank', 14], ['확인 글 수', 'total', 14], ['타겟', 'target', 32], ['매칭 글 제목', 'title', 60], ['매칭 글 URL', 'matchedUrl', 55], ['조회 시각 (한국)', 'checkedAt', 26], ['조회 기준', 'scope', 70], ['검색 URL', 'searchUrl', 55], ['안내', 'message', 65],
  ] : place ? [
    ['키워드', 'keyword', 26], ['상태', 'status', 14], ['전체 순위', 'rank', 14], ['광고 제외 순위', 'organicRank', 18], ['페이지', 'page', 12], ['확인 업체 수', 'total', 16], ['광고 수', 'totalAds', 12], ['타겟 병원명', 'target', 26], ['매칭 상호', 'title', 40], ['조회 시각 (한국)', 'checkedAt', 26], ['조회 기준', 'scope', 80], ['검색 URL', 'searchUrl', 55], ['안내', 'message', 65],
  ] : [
    ['키워드', 'keyword', 26], ['상태', 'status', 14], ['노출 순위', 'rank', 14], ['확인 광고 수', 'totalAds', 15],
    ['타겟 도메인', 'domain', 30], ['노출 광고명', 'title', 30], ['조회 시각 (한국)', 'checkedAt', 26],
    ['조회 기준', 'scope', 32], ['검색 URL', 'searchUrl', 55], ['안내', 'message', 65],
  ]).map(([header, key, width]) => ({ header, key, width }));
  for (const row of rows) {
    sheet.addRow({ ...row, matchedUrl: row.matches?.[0]?.url || '', status: labels[row.status] || row.status, title: place ? row.matches?.map(m => m.name).join(' / ') || '' : row.matches?.[0]?.title || '', checkedAt: row.checkedAt ? new Date(row.checkedAt).toLocaleString('sv-SE', { timeZone: 'Asia/Seoul' }) : '', message: row.message || (row.status === 'not_found' ? '이번 응답의 첫 파워링크 광고 목록에 없음' : '') });
  }
  sheet.getRow(1).height = 28;
  sheet.getRow(1).eachCell(cell => { cell.font = { bold: true, color: { argb: 'FFFFFFFF' } }; cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF5467F7' } }; });
  sheet.autoFilter = `A1:${blog ? 'K' : place ? 'M' : 'J'}${Math.max(1, sheet.rowCount)}`;
  sheet.eachRow((row, index) => { if (index > 1) { row.height = 25; row.eachCell(cell => { cell.font = { size: 11 }; cell.alignment = { vertical: 'middle' }; }); } });
  return workbook.xlsx.writeBuffer();
}
