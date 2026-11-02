import test from 'node:test';
import assert from 'node:assert/strict';
import ExcelJS from 'exceljs';
import { parsePlaceList, PLACE_SCOPE } from '../server/place.mjs';
import { makeWorkbook } from '../server/workbook.mjs';
const item = (name, ad = false, page = 1) => ({ name, ad, page });
test('광고 사이 타겟의 전체·일반 순위와 페이지', () => {
  const r = parsePlaceList([item('가병원',true), item('나병원'), item('다병원',true), item('무이성형외과의원',false,2)], '무이성형외과');
  assert.equal(r.rank,4); assert.equal(r.organicRank,2); assert.equal(r.page,2); assert.equal(r.totalAds,2);
});
test('부분 일치·공백 차이·동명 다건 보존', () => {
  const r = parsePlaceList([item('무 이 성형외과의원'),item('무이성형외과 강남의원')], '무이 성형외과');
  assert.equal(r.matches.length,2); assert.equal(r.rank,1);
});
test('광고와 일반 결과에 모두 있으면 첫 일반 매칭의 순위를 표시', () => {
  const r = parsePlaceList([item('무이성형외과의원',true),item('다른병원'),item('무이성형외과의원')], '무이성형외과');
  assert.equal(r.rank,1); assert.equal(r.organicRank,2); assert.equal(r.matches.length,2); assert.equal(r.rows[0].organicRank,null);
});
test('광고만 매칭되면 광고 제외 순위 없음', () => assert.equal(parsePlaceList([item('무이성형외과의원',true)],'무이').organicRank,null));
test('미노출과 읽기 실패 구분', () => {
  assert.equal(parsePlaceList([item('다른병원')],'무이').status,'not_found');
  assert.throws(() => parsePlaceList([],'무이'));
  assert.throws(() => parsePlaceList([{spans:['이미지 수 6']}],'무이'));
});
test('두 span 상호: 전체 title 우선, 진료과 단독 선택 방지', () => {
  const r = parsePlaceList([{title:'비티성형외과의원 강남성형외과',spans:['의191210','이미지 수 6','성형외과','비티성형외과의원','강남성형외과']}], '비티성형외과');
  assert.equal(r.status,'found'); assert.equal(r.rows[0].name,'비티성형외과의원 강남성형외과');
  assert.equal(parsePlaceList([{spans:['이미지 수 6','비티','성형외과의원']}],'비티성형외과').status,'found');
});
test('플레이스 xlsx 한글 13열·숫자·한국시각·수식 텍스트', async () => {
  const r = parsePlaceList([item('무이성형외과의원')],'무이');
  const b = await makeWorkbook([{...r,keyword:'=1+1',target:'무이',scope:PLACE_SCOPE,checkedAt:'2026-09-09T01:00:00Z'}],{place:true});
  const wb=new ExcelJS.Workbook();await wb.xlsx.load(b);const s=wb.worksheets[0];
  assert.equal(s.columnCount,13);assert.equal(s.getCell('D1').value,'광고 제외 순위');assert.equal(s.getCell('D2').value,1);
  assert.equal(s.getCell('A2').type,ExcelJS.ValueType.String);assert.equal(s.getCell('J2').value,'2026-09-09 10:00:00');assert.match(s.getCell('K2').value,/위치 고정 없음/);
});
test('진료과 전문의 수는 병원명이 아니다', () => {
  assert.throws(() => parsePlaceList([{spans:['성형외과','성형외과 1명','이미지 수 6']}],'무이'));
});
test('이전 페이지 전체와 2페이지 상호의 누적 순위', () => {
  const r = parsePlaceList([item('이전광고병원',true,1),item('이전일반병원',false,1),item('아이그램성형외과의원',false,2),item('무이성형외과의원',false,2),item('윌비성형외과의원',false,2)],'무이성형외과');
  assert.equal(r.rank,4);assert.equal(r.organicRank,3);assert.equal(r.page,2);assert.equal(r.total,5);
});
