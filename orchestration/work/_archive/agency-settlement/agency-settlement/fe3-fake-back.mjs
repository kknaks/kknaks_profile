// 스크린샷 전용 가짜 back — SPEC-001 §4.2 0.4.2 꼴(D-18 최종 결제만). 가명 · 에이전시A/B/C · 둥근 금액 · 운영 KOS 0
import http from 'node:http';
import fs from 'node:fs';

const PORT = Number(process.env.PORT || 8892);
const LOG = process.env.LOG || 'requests.log';
const AG_A = '에이전시A(에이전시)', AG_B = '에이전시B(에이전시)', AG_C = '에이전시C(에이전시)';
const T = (md, hm) => `2026-${md}T${hm}:00+09:00`;
const I = (itemType, productName, optionName, amount, status, currency = 'KRW') => ({
  kind: 'item', itemType, productName, productNameFrom: itemType === 'PREPAID_CARD_PRODUCT' ? 'prepaidCard' : itemType === 'ETCETRA_PRODUCT' ? 'etcetera' : 'product',
  optionName, amount, currency, status, at: null });
// 수납 — 실결제 netTotal 은 itemsHere 면 품목 합 · 아니면 주어진 앞 달 결제 취소 합. approved = 그달 APPROVED 행 있음(결제 손님 셈)
const P = (o) => {
  const lines = o.lines ?? [];
  const itemsHere = o.itemsHere ?? true;
  const mixed = o.currency === null;
  const itemsTotal = mixed ? null : itemsHere ? lines.reduce((n, l) => n + l.amount, 0) : 0;
  const netTotal = mixed ? null : itemsHere ? itemsTotal : (o.priorCancel ?? 0);
  return {
    firstApprovedAt: o.paidAt ?? null, itemsHere, visitDate: null, newInLastFetch: false, itemsNowhere: false, currency: 'KRW', itemsMissing: false,
    canceledPayments: 0, refundedItems: 0, approved: true,
    agency: o.visitorFunnelName?.trim().endsWith('(에이전시)') ? o.visitorFunnelName.trim() : null,
    ...o, lines, itemsTotal, netTotal, paymentsNet: mixed ? null : (o.paymentsNet ?? netTotal),
  };
};

const OCT = [
  P({ purchaseId: '6a1f00000000a1b2c3', paidAt: T('10-02', '11:20'), visitorId: 'v01', visitorName: '홍길동', visitDate: '2026-10-02', visitorFunnelName: AG_A, paymentTypes: ['CARD'], lines: [
    I('PRODUCT_OPTION', '[10월 이벤트] 울쎄라피프라임300샷+써마지600샷', '1회', 3300000, 'ACCEPTED'),
    I('PRODUCT_OPTION', '울쎄라피프라임 300샷', '구성품', 0, 'ACCEPTED'),
    I('PRODUCT_OPTION', '써마지 FLX 600샷', '구성품', 0, 'ACCEPTED')] }),
  // 0원 줄이 ② 차례 맨 앞 → 첫 유료 줄 바로 아래로(§3.3)
  P({ purchaseId: '6a1f00000000d4e5f6', paidAt: T('10-03', '15:05'), visitorId: 'v02', visitorName: '김철수', visitDate: '2026-10-03', visitorFunnelName: '네이버 검색', paymentTypes: ['CARD', 'CASH'], lines: [
    I('ETCETRA_PRODUCT', '사은품 마스크팩', null, 0, 'PAID'),
    I('PRODUCT_OPTION', '[첫방문] 써마지 FLX', '300샷', 1000000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '마취 크림', null, 30000, 'PAID')] }),
  // 분할 결제 나머지만 이 달 → 숨김
  P({ purchaseId: '6a1f00000000778899', paidAt: T('10-05', '14:00'), itemsHere: false, visitorId: 'v03', visitorName: '이영희', visitorFunnelName: AG_B, paymentTypes: ['CARD'], hidden: true }),
  // 재결제 — 800,000 승인 → 전액 취소 → 600,000 재승인 · 품목 600,000(실결제 600,000 · 취소 1)
  P({ purchaseId: '6a1f00000000aabbcc', paidAt: T('10-08', '09:40'), visitorId: 'v04', visitorName: '박가명', visitDate: '2026-10-08', visitorFunnelName: AG_A, paymentTypes: ['CARD'], canceledPayments: 1, paymentsNet: 600000, lines: [
    I('PRODUCT_OPTION', '[오픈] 울써마지 300샷', '1회', 600000, 'ACCEPTED')] }),
  P({ purchaseId: '6a1f00000000ddeeff', paidAt: T('10-11', '17:45'), visitorId: 'v05', visitorName: '정예시', visitDate: '2026-10-11', visitorFunnelName: '지인 소개', paymentTypes: ['CARD'], currency: null, lines: [
    I('PRODUCT_OPTION', '[오픈] 울써마지 300샷', '1회', 200000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '해외 결제 상품', null, 100, 'ACCEPTED', 'USD')] }),
  P({ purchaseId: '6a1f00000000123abc', paidAt: T('10-14', '12:00'), visitorId: 'v06', visitorName: null, visitorFunnelName: AG_C, paymentTypes: ['CASH'], itemsMissing: true, paymentsNet: 1000000 }),
  // 앞 달 결제 취소 — 9월 품목 · 10월 취소 −300,000(반영 안 됨) · 반환 −50,000(반영됨 → reflectedCancels)
  P({ purchaseId: '6a1e000000006a7b8c', paidAt: null, firstApprovedAt: T('09-20', '15:40'), itemsHere: false, visitorId: 'v07', visitorName: '강샘플', visitDate: '2026-09-20', visitorFunnelName: AG_A, paymentTypes: [], approved: false, canceledPayments: 2, priorCancel: -300000, paymentsNet: -350000 }),
  // 부분 환불 — 선불카드 50만원권 → 20만원 반환 · 남은 300,000
  P({ purchaseId: '6a1f00000000789fed', paidAt: T('10-20', '13:30'), visitorId: 'v08', visitorName: '오가나', visitDate: '2026-10-20', visitorFunnelName: AG_A, paymentTypes: ['EASY_PAY'], canceledPayments: 1, paymentsNet: 300000, lines: [
    I('PREPAID_CARD_PRODUCT', '선불카드 50만원권', null, 300000, 'PARTIALLY_REFUNDED')] }),
  P({ purchaseId: '6a1f00000000654321', paidAt: null, itemsHere: false, visitorId: 'v09', visitorName: '한다라', visitDate: '2026-10-21', visitorFunnelName: null, paymentTypes: ['CARD'], hidden: true }),
  // 품목 하나 전액 환불(줄 없음 · 환불 1) + 그 결제 취소 1
  P({ purchaseId: '6a1f00000000cba987', paidAt: T('10-24', '16:40'), visitorId: 'v10', visitorName: '윤테스트', visitDate: '2026-10-24', visitorFunnelName: AG_B, paymentTypes: ['CARD'], canceledPayments: 1, refundedItems: 1, paymentsNet: 2000000, lines: [
    I('PRODUCT_OPTION', '[10월 이벤트] 울쎄라피프라임300샷+써마지600샷', '1회', 2000000, 'PAID'),
    I('PRODUCT_OPTION', '울쎄라피프라임 300샷', '구성품', 0, 'PAID'),
    I('PRODUCT_OPTION', '써마지 FLX 600샷', '구성품', 0, 'PAID')] }),
  // 품목이 어느 달에도 없음 · 실결제 0 · 줄 0 → 숨기지 않는다(NOTE-6)
  P({ purchaseId: '6a1f00000000ab12cd', paidAt: T('10-25', '10:00'), itemsHere: false, itemsNowhere: true, visitorId: 'v15', visitorName: '도가명', visitorFunnelName: '네이버 검색', paymentTypes: ['CARD'] }),
  // 결제 순액 ≠ 품목 합 → ⚠
  P({ purchaseId: '6a1f00000000f0e1d2', paidAt: T('10-26', '11:10'), visitorId: 'v14', visitorName: '최모의', visitDate: '2026-10-26', visitorFunnelName: '네이버 검색', paymentTypes: ['CARD'], paymentsNet: 800000, lines: [
    I('PRODUCT_OPTION', '리쥬란 힐러 4cc', '2회', 1200000, 'ACCEPTED')] }),
];
const SEP = [
  P({ purchaseId: '6a1e000000000a1b2c', paidAt: T('09-03', '10:30'), visitorId: 'v21', visitorName: '최가상', visitDate: '2026-09-03', visitorFunnelName: AG_A, paymentTypes: ['CARD'], lines: [
    I('PRODUCT_OPTION', '[9월 이벤트] 슈링크 유니버스 300샷', '1회', 1500000, 'ACCEPTED')] }),
  // 에이전시B 의 9월 수납은 전액 환불 하나 → 숨김 → B 탭 빈 탭 문구
  P({ purchaseId: '6a1e000000003d4e5f', paidAt: T('09-07', '16:10'), visitorId: 'v22', visitorName: '문예제', visitDate: '2026-09-07', visitorFunnelName: AG_B, paymentTypes: [], canceledPayments: 1, refundedItems: 1, hidden: true }),
  P({ purchaseId: '6a1e000000006a7b8c', paidAt: T('09-20', '15:40'), visitorId: 'v07', visitorName: '강샘플', visitDate: '2026-09-20', visitorFunnelName: AG_A, paymentTypes: ['CARD', 'CASH'], lines: [
    I('PRODUCT_OPTION', '아쿠아필', '1회', 300000, 'ACCEPTED'),
    I('ETCETRA_PRODUCT', '진정 관리', null, 0, 'PAID')] }),
  P({ purchaseId: '6a1e000000009d0e1f', paidAt: T('09-22', '13:15'), visitorId: 'v24', visitorName: '서임시', visitDate: '2026-09-22', visitorFunnelName: '인스타그램', paymentTypes: ['CARD'], lines: [
    I('PRODUCT_OPTION', '[첫방문] 써마지 FLX', '300샷', 900000, 'ACCEPTED')] }),
];

const RANGE = { '2026-10': ['2026-09-30T15:00:00Z', '2026-10-31T14:59:59Z'], '2026-09': ['2026-08-31T15:00:00Z', '2026-09-30T14:59:59Z'], '2026-08': ['2026-07-31T15:00:00Z', '2026-08-31T14:59:59Z'] };
const ST = {
  '2026-10': { state: 'current', all: OCT, fetchedAt: '2026-10-29T14:03:12+09:00', full: '2026-10-29T09:00:05+09:00', extra: { reflectedCancels: 1, excludedItems: 1, ignoredTransactions: 1 } },
  '2026-09': { state: 'closed', all: SEP, fetchedAt: '2026-10-29T13:58:02+09:00', full: '2026-10-29T13:58:02+09:00', closedAt: '2026-10-29T13:58:30+09:00', extra: {} },
  '2026-08': { state: 'closed', all: [], fetchedAt: '2026-10-29T13:57:40+09:00', full: '2026-10-29T13:57:40+09:00', closedAt: '2026-10-29T13:57:41+09:00', extra: {} },
};
const sum = (ps) => (ps.some((p) => p.netTotal === null) ? null : ps.reduce((n, p) => n + p.netTotal, 0));
const summarize = (all) => ({
  customers: new Set(all.map((p) => p.visitorId ?? p.purchaseId)).size,
  payingCustomers: new Set(all.filter((p) => p.approved).map((p) => p.visitorId ?? p.purchaseId)).size,
  purchases: all.filter((p) => !p.hidden).length,
  netTotal: sum(all.filter((p) => !p.hidden)),
});
const strip = ({ hidden, approved, priorCancel, ...p }) => (void hidden, void approved, void priorCancel, p);
function respond(month, s) {
  const shown = s.all.filter((p) => !p.hidden);
  const ag = s.all.filter((p) => p.agency);
  const names = [...new Set(ag.map((p) => p.agency))].sort();
  return {
    month, rangeUtc: { from: RANGE[month][0], to: RANGE[month][1] }, fetchedAt: s.fetchedAt, cached: true,
    store: { state: s.state, fetchedAt: s.fetchedAt, fullFetchedAt: s.full, closedAt: s.closedAt ?? null },
    fetch: { mode: 'none', fromUtc: null, kosCalls: 0, newTransactions: 0, duplicateTransactions: 0, missingTransactions: 0, newPurchases: 0 },
    counts: { purchases: shown.length, itemLines: shown.reduce((n, p) => n + p.lines.length, 0),
      canceledPayments: s.all.reduce((n, p) => n + p.canceledPayments, 0), refundedItems: s.all.reduce((n, p) => n + p.refundedItems, 0),
      hiddenPurchases: s.all.length - shown.length, reflectedCancels: 0, excludedItems: 0,
      transactions: 30, ignoredTransactions: 0, itemsMissing: shown.filter((p) => p.itemsMissing).length, visitorMissing: shown.filter((p) => !p.visitorName).length,
      itemsElsewhere: s.all.filter((p) => !p.itemsHere).length, firstApprovalCanceled: 0, firstApprovedUnknown: 0, unmatchedTransactions: 0, atOutsideMonth: 0,
      itemsPinnedElsewhere: 0, itemsNowhere: 0, ...s.extra },
    agencyTotal: summarize(ag),
    agencies: names.map((name) => ({ name, ...summarize(ag.filter((p) => p.agency === name)) })),
    purchases: shown.map(strip),
  };
}

const H = { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': 'Content-Disposition', 'Cache-Control': 'no-store' };
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  fs.appendFileSync(LOG, `${req.method} ${u.pathname}${u.search}\n`);
  const month = u.searchParams.get('month') ?? '2026-10';
  if (u.pathname === '/api/sales' && ST[month]) { res.writeHead(200, H); return res.end(JSON.stringify(respond(month, ST[month]))); }
  res.writeHead(400, H); res.end(JSON.stringify({ error: { code: 'bad_month', message: '조회할 달이 올바르지 않아요' } }));
}).listen(PORT, '127.0.0.1', () => console.log('fake back', PORT));
