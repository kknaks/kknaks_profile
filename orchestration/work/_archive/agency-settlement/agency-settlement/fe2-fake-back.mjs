// 스크린샷 전용 가짜 back(SPEC-001 §4.2 0.3.1 꼴 · 시안 v2 가짜 값 — 가명 · 에이전시A/B/C · 둥근 금액). 레포 밖 scratchpad · 운영 KOS 0
import http from 'node:http';
import fs from 'node:fs';

const PORT = Number(process.env.PORT || 8891);
const LOG = process.env.LOG || 'requests.log';
const AG_A = '에이전시A(에이전시)', AG_B = '에이전시B(에이전시)', AG_C = '에이전시C(에이전시)';
const T = (md, hm) => `2026-${md}T${hm}:00+09:00`;
const I = (itemType, productName, optionName, amount, status, currency = 'KRW') => ({
  kind: 'item', itemType, productName, productNameFrom: itemType === 'PREPAID_CARD_PRODUCT' ? 'prepaidCard' : itemType === 'ETCETRA_PRODUCT' ? 'etcetera' : 'product',
  optionName, amount, currency, status, at: null });
const X = (kind, amount, at, paymentType) => ({ kind, itemType: null, productName: null, productNameFrom: null, optionName: null, amount, currency: 'KRW',
  status: { payment: 'APPROVED', cancel: 'CANCELED', spent: 'SPENT' }[kind], at, paymentType });
const P = (o) => ({ firstApprovedAt: o.paidAt, itemsHere: true, visitDate: null, agency: o.visitorFunnelName?.trim().endsWith('(에이전시)') ? o.visitorFunnelName.trim() : null,
  newInLastFetch: false, itemsNowhere: false, currency: 'KRW', itemsMissing: false, ...o });

const OCT = [
  P({ purchaseId: '6a1f00000000a1b2c3', paidAt: T('10-02', '11:20'), visitorId: 'v01', visitorName: '홍길동', visitDate: '2026-10-02', visitorFunnelName: AG_A, paymentTypes: ['CARD'], approvedTotal: 3300000, itemsTotal: 3300000, lines: [
    I('PRODUCT_OPTION', '[10월 이벤트] 울쎄라피프라임300샷+써마지600샷', '1회', 3300000, 'ACCEPTED'),
    I('PRODUCT_OPTION', '울쎄라피프라임 300샷', '구성품', 0, 'ACCEPTED'),
    I('PRODUCT_OPTION', '써마지 FLX 600샷', '구성품', 0, 'ACCEPTED')] }),
  P({ purchaseId: '6a1f00000000d4e5f6', paidAt: T('10-03', '15:05'), visitorId: 'v02', visitorName: '김철수', visitDate: '2026-10-03', visitorFunnelName: '네이버 검색', paymentTypes: ['CARD', 'CASH'], approvedTotal: 1030000, itemsTotal: 1030000, lines: [
    I('PRODUCT_OPTION', '[첫방문] 써마지 FLX', '300샷', 1000000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '마취 크림', null, 30000, 'PAID')] }),
  P({ purchaseId: '6a1f00000000778899', paidAt: T('10-05', '14:00'), firstApprovedAt: T('09-15', '10:30'), itemsHere: false, visitorId: 'v03', visitorName: '이영희', visitorFunnelName: AG_B, paymentTypes: ['CARD'], approvedTotal: 500000, itemsTotal: 0, lines: [
    X('payment', 500000, T('10-05', '14:00'), 'CARD')] }),
  P({ purchaseId: '6a1f00000000aabbcc', paidAt: T('10-08', '09:10'), visitorId: 'v04', visitorName: '박가명', visitDate: '2026-10-08', visitorFunnelName: AG_A, paymentTypes: ['PREPAID_CARD'], approvedTotal: 800000, itemsTotal: 1200000, lines: [
    I('PRODUCT_OPTION', '[오픈] 울써마지 300샷', '1회', 800000, 'ACCEPTED'),
    I('PRODUCT_OPTION', '리쥬란 힐러 2cc', '1회', 400000, 'REFUNDED'),
    X('cancel', -400000, T('10-12', '16:05'), 'CARD')] }),
  P({ purchaseId: '6a1f00000000ddeeff', paidAt: T('10-11', '17:45'), visitorId: 'v05', visitorName: '정예시', visitDate: '2026-10-11', visitorFunnelName: '지인 소개', paymentTypes: ['CARD'], currency: null, approvedTotal: null, itemsTotal: null, lines: [
    I('PRODUCT_OPTION', '[오픈] 울써마지 300샷', '1회', 200000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '해외 결제 상품', null, 100, 'ACCEPTED', 'USD')] }),
  P({ purchaseId: '6a1f00000000123abc', paidAt: T('10-14', '12:00'), visitorId: 'v06', visitorName: null, visitorFunnelName: AG_C, paymentTypes: ['CASH'], approvedTotal: 1000000, itemsTotal: 0, itemsMissing: true, lines: [] }),
  P({ purchaseId: '6a1f00000000456def', paidAt: null, firstApprovedAt: null, itemsHere: false, visitorId: 'v07', visitorName: '강샘플', visitDate: '2026-09-20', visitorFunnelName: AG_A, paymentTypes: [], approvedTotal: 0, itemsTotal: 0, lines: [
    X('spent', -50000, null, 'CASH'),
    X('cancel', -300000, T('10-02', '10:00'), 'CARD')] }),
  P({ purchaseId: '6a1f00000000789fed', paidAt: T('10-20', '13:30'), visitorId: 'v08', visitorName: '오가나', visitDate: '2026-10-20', visitorFunnelName: AG_A, paymentTypes: ['EASY_PAY'], approvedTotal: 500000, itemsTotal: 500000, lines: [
    I('PREPAID_CARD_PRODUCT', '선불카드 50만원권', null, 500000, 'PARTIALLY_REFUNDED')] }),
  P({ purchaseId: '6a1f00000000654321', paidAt: null, firstApprovedAt: null, itemsHere: false, visitorId: 'v09', visitorName: '한다라', visitDate: '2026-10-21', visitorFunnelName: null, paymentTypes: ['CARD'], approvedTotal: 1000000, itemsTotal: 0, lines: [
    X('payment', 1000000, null, 'CARD')] }),
  P({ purchaseId: '6a1f00000000cba987', paidAt: T('10-24', '16:40'), visitorId: 'v10', visitorName: '윤테스트', visitDate: '2026-10-24', visitorFunnelName: AG_B, paymentTypes: ['CARD'], approvedTotal: 2200000, itemsTotal: 2200000, lines: [
    I('PRODUCT_OPTION', '[10월 이벤트] 울쎄라피프라임300샷+써마지600샷', '1회', 2000000, 'PAID'),
    I('PRODUCT_OPTION', '울쎄라피프라임 300샷', '구성품', 0, 'PAID'),
    I('PRODUCT_OPTION', '써마지 FLX 600샷', '구성품', 0, 'PAID'),
    I('ETCETRA_PRODUCT', '진정 관리', null, 200000, 'PAID')] }),
];
const OCT_NEW = [
  P({ purchaseId: '6a1f00000000e1f2a3', paidAt: T('10-29', '14:40'), visitorId: 'v11', visitorName: '노샘플', visitDate: '2026-10-29', visitorFunnelName: AG_C, paymentTypes: ['CARD'], approvedTotal: 700000, itemsTotal: 700000, lines: [
    I('PRODUCT_OPTION', '리쥬란 힐러 2cc', '1회', 700000, 'ACCEPTED')] }),
  P({ purchaseId: '6a1f00000000b4c5d6', paidAt: T('10-29', '15:05'), visitorId: 'v12', visitorName: '류가짜', visitDate: '2026-10-29', visitorFunnelName: '네이버 검색', paymentTypes: ['CASH'], approvedTotal: 120000, itemsTotal: 120000, lines: [
    I('ETCETRA_PRODUCT', '진정 관리', null, 120000, 'PAID')] }),
];
const SEP = [
  P({ purchaseId: '6a1e000000000a1b2c', paidAt: T('09-03', '10:30'), visitorId: 'v21', visitorName: '최가상', visitDate: '2026-09-03', visitorFunnelName: AG_A, paymentTypes: ['CARD'], approvedTotal: 1500000, itemsTotal: 1500000, lines: [
    I('PRODUCT_OPTION', '[9월 이벤트] 슈링크 유니버스 300샷', '1회', 1500000, 'ACCEPTED')] }),
  P({ purchaseId: '6a1e000000003d4e5f', paidAt: T('09-07', '16:10'), visitorId: 'v22', visitorName: '문예제', visitDate: '2026-09-07', visitorFunnelName: AG_B, paymentTypes: ['CASH'], approvedTotal: 600000, itemsTotal: 600000, lines: [
    I('PRODUCT_OPTION', '리쥬란 힐러 2cc', '1회', 600000, 'PAID')] }),
  P({ purchaseId: '6a1e000000006a7b8c', paidAt: T('09-20', '15:40'), visitorId: 'v07', visitorName: '강샘플', visitDate: '2026-09-20', visitorFunnelName: AG_A, paymentTypes: ['CARD', 'CASH'], approvedTotal: 350000, itemsTotal: 350000, lines: [
    I('PRODUCT_OPTION', '아쿠아필', '1회', 300000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '진정 관리', null, 50000, 'PAID')] }),
  P({ purchaseId: '6a1e000000009d0e1f', paidAt: T('09-22', '13:15'), visitorId: 'v24', visitorName: '서임시', visitDate: '2026-09-22', visitorFunnelName: '인스타그램', paymentTypes: ['CARD'], approvedTotal: 900000, itemsTotal: 900000, lines: [
    I('PRODUCT_OPTION', '[첫방문] 써마지 FLX', '300샷', 900000, 'ACCEPTED')] }),
  P({ purchaseId: '6a1e000000002a3b4c', paidAt: T('09-27', '18:00'), visitorId: 'v25', visitorName: '백더미', visitDate: '2026-09-27', visitorFunnelName: AG_A, paymentTypes: ['EASY_PAY'], approvedTotal: 2000000, itemsTotal: 2000000, lines: [
    I('PREPAID_CARD_PRODUCT', '선불카드 200만원권', null, 2000000, 'PAID')] }),
];

const RANGE = { '2026-10': ['2026-09-30T15:00:00Z', '2026-10-31T14:59:59Z'], '2026-09': ['2026-08-31T15:00:00Z', '2026-09-30T14:59:59Z'], '2026-08': ['2026-07-31T15:00:00Z', '2026-08-31T14:59:59Z'] };
let st;
const reset = () => {
  st = {
    '2026-10': { state: 'current', purchases: OCT, fetchedAt: '2026-10-29T14:03:12+09:00', full: '2026-10-29T09:00:05+09:00', pulls: 0 },
    '2026-09': { state: 'closed', purchases: SEP, fetchedAt: '2026-10-29T13:58:02+09:00', full: '2026-10-29T13:58:02+09:00', closedAt: '2026-10-29T13:58:30+09:00' },
    '2026-08': { state: 'closed', purchases: [], fetchedAt: '2026-10-29T13:57:40+09:00', full: '2026-10-29T13:57:40+09:00', closedAt: '2026-10-29T13:57:41+09:00' },
  };
};
reset();

function summarize(ps) {
  const people = new Set(ps.map((p) => p.visitorId ?? p.purchaseId));
  const paying = new Set(ps.filter((p) => p.paymentTypes.length > 0).map((p) => p.visitorId ?? p.purchaseId));
  return { customers: people.size, payingCustomers: paying.size, purchases: ps.length };
}
function respond(month, s, fetch) {
  const ps = s.purchases;
  const lines = ps.flatMap((p) => p.lines);
  const n = (ks) => lines.filter((l) => ks.includes(l.kind)).length;
  const ag = ps.filter((p) => p.agency);
  const names = [...new Set(ag.map((p) => p.agency))].sort();
  return {
    month, rangeUtc: { from: RANGE[month][0], to: RANGE[month][1] }, fetchedAt: s.fetchedAt, cached: fetch.mode === 'none',
    store: { state: s.state, fetchedAt: s.fetchedAt, fullFetchedAt: s.full, closedAt: s.closedAt ?? null },
    fetch: { fromUtc: fetch.mode === 'none' ? null : RANGE[month][0], kosCalls: 0, newTransactions: 0, duplicateTransactions: 0, missingTransactions: 0, newPurchases: 0, ...fetch },
    counts: { purchases: ps.length, itemLines: n(['item']), paymentLines: n(['payment']), reversalLines: n(['cancel', 'spent']), transactions: lines.length + 3,
      ignoredTransactions: month === '2026-10' ? 1 : 0, itemsMissing: ps.filter((p) => p.itemsMissing).length, visitorMissing: ps.filter((p) => !p.visitorName).length,
      itemsElsewhere: ps.filter((p) => !p.itemsHere).length, firstApprovalCanceled: 0, firstApprovedUnknown: 0, unmatchedTransactions: 2, atOutsideMonth: 0, itemsPinnedElsewhere: 0, itemsNowhere: 0 },
    agencyTotal: summarize(ag),
    agencies: names.map((name) => ({ name, ...summarize(ag.filter((p) => p.agency === name)) })),
    purchases: ps,
  };
}

const H = { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': 'Content-Disposition', 'Cache-Control': 'no-store' };
const err = (res, status, code, message) => { res.writeHead(status, H); res.end(JSON.stringify({ error: { code, message } })); };

http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  fs.appendFileSync(LOG, `${req.method} ${u.pathname}${u.search}\n`);
  if (u.pathname === '/__reset') { reset(); res.writeHead(200, H); return res.end('{}'); }
  const month = u.searchParams.get('month') ?? '2026-10';
  if (u.pathname === '/api/sales.xlsx') {
    if (!st[month]) return err(res, 409, 'not_fetched', '이 달은 아직 받지 않았어요 — 화면에서 먼저 받아 주세요');
    const view = u.searchParams.get('view') ?? 'monthly';
    const agency = u.searchParams.get('agency');
    const name = `매출_${month}_${view === 'monthly' ? '월별' : agency ? agency.replace(/\(에이전시\)$/, '') : '에이전시전체'}.xlsx`;
    res.writeHead(200, { ...H, 'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Content-Disposition': `attachment; filename*=UTF-8''${encodeURIComponent(name)}` });
    return res.end('PK fake');
  }
  if (u.pathname !== '/api/sales') return err(res, 404, 'not_found', '없음');
  if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(month) || month > '2026-10') return err(res, 400, 'bad_month', '조회할 달이 올바르지 않아요');
  if (month === '2026-07') return setTimeout(() => err(res, 502, 'kos_unavailable', 'KOS 에 연결하지 못했어요'), 120000); // 불러오는 중 장면
  if (month === '2026-06') return err(res, 502, 'kos_unavailable', 'KOS 에 연결하지 못했어요');
  const s = st[month];
  if (!s) return err(res, 502, 'kos_unavailable', 'KOS 에 연결하지 못했어요');
  const refresh = u.searchParams.get('refresh');
  if (refresh && refresh !== 'new' && refresh !== 'full') return err(res, 400, 'bad_refresh', '다시 받기 방식이 올바르지 않아요');
  let fetch = { mode: 'none' };
  if (refresh === 'full') {
    s.purchases = s.purchases.map((p) => ({ ...p, newInLastFetch: false }));
    s.fetchedAt = s.full = '2026-10-29T15:22:04+09:00';
    fetch = { mode: 'full', kosCalls: 14 };
  } else if (refresh === 'new' && s.state === 'current') {
    s.pulls++;
    if (s.pulls === 1) {
      s.purchases = [...OCT, ...OCT_NEW.map((p) => ({ ...p, newInLastFetch: true }))];
      s.fetchedAt = '2026-10-29T15:20:31+09:00';
      fetch = { mode: 'incremental', kosCalls: 6, newTransactions: 2, duplicateTransactions: 14, newPurchases: 2 };
    } else {
      s.purchases = s.purchases.map((p) => ({ ...p, newInLastFetch: false }));
      s.fetchedAt = '2026-10-29T15:31:08+09:00';
      fetch = { mode: 'incremental', kosCalls: 2, newTransactions: 0, duplicateTransactions: 16 };
    }
  }
  const delay = refresh ? 900 : 0;
  setTimeout(() => { res.writeHead(200, H); res.end(JSON.stringify(respond(month, s, fetch))); }, delay);
}).listen(PORT, '127.0.0.1', () => console.log('fake back', PORT));
