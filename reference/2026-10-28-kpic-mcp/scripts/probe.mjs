// stdio 로 서버를 띄워 MCP tool 을 실호출한다.
//   node scripts/probe.mjs --tools                 tool 목록
//   node scripts/probe.mjs 디스포트 티엠버스         제품명 검색 → 첫 결과 상세
//   node scripts/probe.mjs --ingredient 데옥시콜산   성분 검색 → 첫 제품 상세
//   node scripts/probe.mjs --detail A11AGGGGG7051   상세만
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const c = new Client({ name: 'probe', version: '0' });
await c.connect(new StdioClientTransport({ command: 'node', args: ['dist/index.js'] }));

const call = async (name, args) => {
  const r = await c.callTool({ name, arguments: args });
  if (r.isError) throw new Error(r.content[0].text);
  return JSON.parse(r.content[0].text);
};
const row = (d) =>
  `${d.drug_code} ${d.drug_name} | ${d.list_sunb_name} | ${d.upso_name_kfda} | ${d.drug_class} | ${d.cls_name} | kfda ${d.kfda_code} | boh ${d.boh_code || '-'} ${d.boh_price || ''}`;
const detail = async (code) => {
  const d = (await call('get_drug_detail_by_id', { drugcode: code }))[0];
  console.log(`   └ detail: ${d.drug_name} (${d.drug_enm}) | ${d.list_sunb_name} | ATC ${d.atc_cd} | ${d.boh} | hira ${d.boh_hiracode ?? '-'} | 허가 ${d.item_permit_date}`);
};

const [mode, ...rest] = process.argv.slice(2);
try {
  if (mode === '--tools') {
    console.log(JSON.stringify((await c.listTools()).tools, null, 2));
  } else if (mode === '--detail') {
    for (const code of rest) await detail(code);
  } else if (mode === '--ingredient') {
    for (const q of rest) {
      const groups = await call('search_drugs_by_ingredient', { ingredient: q });
      console.log(`## [성분] ${q} → 성분 ${groups.length}개`);
      for (const g of groups) {
        console.log(` - ${g.ingd_code} ${g.ingd_name} (${g.ingd_ename}) ${g.match_type} · 제품 ${g.drugs.length}건`);
        for (const d of g.drugs.slice(0, 12)) console.log(`   ${row(d)}`);
        if (g.drugs[0]) await detail(g.drugs[0].drug_code);
      }
    }
  } else {
    for (const q of [mode, ...rest].filter(Boolean)) {
      const rows = await call('search_drugs_by_name', { drugname: q });
      console.log(`## ${q} → ${rows.length}건`);
      for (const d of rows.slice(0, 8)) console.log(`   ${row(d)}`);
      if (rows[0]) await detail(rows[0].drug_code);
    }
  }
} catch (e) {
  console.log('ERR', e.message);
}
process.exit(0);
