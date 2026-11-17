// Icon — 시안 내장 아이콘 26(_icons.js ICON_SVG 키 전부) 카탈로그. 색 = SVG 원래 색 → medikit 변수(HEX2TOKEN).
// 근거: 시안 1·8행 자산 표 · 788행 ICON · CHECK16 · crmNotify
// variant name = icon/<키>. 단 린트 touch-target-size 가 이름의 link · input 낱말을 조작 요소로 오인해서(16×16 경고),
// 두 개만 낱말을 피한 별칭으로 둔다(코디 2026-11-12 ③): link-2-white-16 → chain-white-16 · input-delete → clear-20. SVG 키는 그대로.
const ALIAS = { "link-2-white-16": "chain-white-16", "input-delete": "clear-20" };
const variants = Object.keys(ICON_SVG).map((name) => ({ props: { name: `icon/${ALIAS[name] || name}` }, node: icon(name) }));
for (const v of variants) if (ALIAS[v.node.name.slice(5)]) v.node.name = `icon/${ALIAS[v.node.name.slice(5)]}`;
makeSet("Icon", variants, { perRow: 13, description: "시안 내장 아이콘(SVG 그대로 · 색은 변수). 카탈로그용 — 화면 컴포넌트 안에서는 icon() 프레임으로 들어간다. 별칭: chain-white-16 = link-2-white-16 · clear-20 = input-delete." });
