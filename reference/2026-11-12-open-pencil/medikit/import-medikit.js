// 메디킷(CRM) 토큰 → OpenPencil 0.16.0 (앱 모드)
// 값 출처: medikit.css(키트 :root) + day-override.css(CRM primary blue #1d8bff) + medikit-preset.json(타이포·그림자)
// 실행: bun ~/.bun/bin/openpencil eval --stdin < import-medikit.js   (열려 있는 활성 문서에 넣는다)
//
// 0.16.0 에는 figma.variables · createTextStyle · createEffectStyle 이 없다(공식 문서는 개발판 기준).
//  - 색   → 변수 컬렉션 "medikit" (COLOR)
//  - 타이포 28 · 그림자 3 → 「medikit」 페이지의 컴포넌트 (스타일 대신 인스턴스로 쓴다)
// 다시 돌리면 「medikit」 페이지만 지우고 새로 만든다. 컬렉션은 지우지 않는다 — 이름이 같은 변수는 값이 다를 때만 맞추고, 없으면 만든다
// (지우면 「components」 의 바인딩과 시안 변수 status/* · crm/* 가 끊긴다. 2026-11-12 cc-procedure-map 컴포넌트 판에서 바꿈).
// 린트(2026-11-12): 페이지 배경 흰색 · 모든 레이어 이름 · 글자 12px 이상 · 글자/테두리 색 변수 바인딩. 견본은 컬렉션의 변수 전부(시안 변수 포함).

const COLORS = {
  "primary/DEFAULT": "#1d8bff", "primary/100": "#eff7ff", "primary/300": "#dbecff",
  "primary/500": "#99cbff", "primary/shadow": "rgba(29,139,255,0.3)",
  "red/DEFAULT": "#ff4e51", "red/100": "#ffefef", "red/300": "#ffe1e1", "red/500": "#ffc4c5",
  "red/shadow": "rgba(255,78,81,0.2)",
  "yellow/DEFAULT": "#fd9400", "yellow/100": "#fff7ec", "yellow/300": "#ffe4c0",
  "purple/DEFAULT": "#ac47ff", "purple/100": "#f8f0ff",
  "gray/100": "#fbfbfb", "gray/200": "#f3f3f3", "gray/300": "#e3e3e3", "gray/400": "#d6d6d6",
  "gray/500": "#cfcfcf", "gray/600": "#9f9f9f", "gray/700": "#6e6e6e", "gray/800": "#3e3e3e",
  "black": "#000000", "white": "#ffffff", "overlay": "rgba(0,0,0,0.6)",
  "hover-dark": "#222943",
  "text/DEFAULT": "#3e3e3e", "text/secondary": "#6e6e6e",
};

// [이름, px, weights, lineHeight 배수] — medikit-preset.json fontSize 26단계
const TYPO = [
  ["headline-lg", 40, [600, 500, 400], 1.3], ["headline-md", 32, [600, 500, 400], 1.3],
  ["title-lg", 24, [600, 500, 400], 1.4], ["title-md", 20, [600, 500, 400], 1.4],
  ["title-sm", 18, [600, 500, 400], 1.5], ["heading-md", 16, [600, 500, 400], 1.5],
  ["heading-sm", 14, [500, 400], 1.5], ["body", 14, [600, 500, 400], 1.6],
  ["caption-md", 12, [600, 500, 400], 1.3], ["meta-sm", 10, [500, 400], 1.3],
];

const SHADOWS = {
  "pop-over": { x: 0, y: 0, blur: 4, color: "#CFCFCF", a: 1 },
  "pop-over-more": { x: 0, y: 2, blur: 10, color: "#BDBDBD", a: 0.5 },
  "accordion": { x: 0, y: 0, blur: 3.5, color: "#EBEBEB", a: 1 },
};

const FAMILY = "Pretendard";
const WEIGHT = { 400: "Regular", 500: "Medium", 600: "SemiBold" };

function parse(c) {
  const m = c.match(/rgba?\(([^)]+)\)/);
  if (m) { const [r, g, b, a = 1] = m[1].split(",").map(Number); return { r: r / 255, g: g / 255, b: b / 255, a }; }
  const h = c.replace("#", "");
  return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255, a: 1 };
}
const solid = (c) => { const p = parse(c); return [{ type: "SOLID", color: { r: p.r, g: p.g, b: p.b }, opacity: p.a }]; };

const out = { colors: 0, created: 0, typo: 0, shadows: 0 };
const homePage = figma.currentPage;

// 0) 다시 돌릴 때: 페이지만 정리
for (const p of [...figma.root.children]) if (p.name === "medikit") p.remove();

// 1) 색 변수 — 있으면 두고(값이 다르면 맞춤), 없으면 만든다
let col = figma.getLocalVariableCollections().find((c) => c.name === "medikit");
if (!col) col = figma.createVariableCollection("medikit");
const mode = col.modes[0].modeId;
const have = {};
for (const v of figma.getLocalVariables()) if ((v.collectionId ?? v.variableCollectionId) === col.id) have[v.name] = v;
const sameColor = (a, b) => a && ["r", "g", "b", "a"].every((k) => Math.round((a[k] ?? 1) * 255) === Math.round((b[k] ?? 1) * 255));
for (const [name, val] of Object.entries(COLORS)) {
  const c = parse(val);
  if (have[name]) { if (!sameColor(have[name].valuesByMode?.[mode], c)) figma.setVariableValue(have[name].id, mode, c); }
  else { have[name] = figma.createVariable(name, "COLOR", col.id, c); out.created++; }
}
const vars = {};
for (const v of figma.getLocalVariables()) vars[v.name] = v;

// 2) 「medikit」 페이지 (흰 배경)
const page = figma.createPage();
page.name = "medikit";
page.backgrounds = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: 1 }];
for (const w of [400, 500, 600]) await figma.loadFontAsync({ family: FAMILY, style: WEIGHT[w] });

// 글자·선 색은 변수로(값 = 변수 값)
function bindPaint(node, field, varName) {
  const v = vars[varName];
  node[field] = solid(COLORS[varName] || "#3e3e3e");
  if (v) figma.bindVariable(node.id, `${field}/0/color`, v.id);
}
function label(text, x, y, name, size = 12, w = 400, color = "gray/700") {
  const t = figma.createText();
  t.fontName = { family: FAMILY, style: WEIGHT[w] };
  t.characters = text; t.fontSize = size;
  t.lineHeight = { unit: "PIXELS", value: Math.round(size * 1.3) };
  bindPaint(t, "fills", color);
  t.name = name;
  t.x = x; t.y = y; page.appendChild(t);
  return t;
}
const hexOf = (c) => "#" + [c.r, c.g, c.b].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("") + ((c.a ?? 1) < 1 ? ` · ${Math.round(c.a * 100)}%` : "");

// 2-1) 색 견본 — 컬렉션의 변수 전부(키트 29 + 시안 status/* · crm/*)
const colorVars = figma.getLocalVariables().filter((v) => (v.collectionId ?? v.variableCollectionId) === col.id).filter((v) => v.resolvedType === "COLOR" || !v.resolvedType);
label("Colors · 변수 컬렉션 medikit", 0, 0, "title/colors", 20, 600, "gray/800");
colorVars.forEach((v, i) => {
  const x = (i % 8) * 140, y = 40 + Math.floor(i / 8) * 116;
  const val = v.valuesByMode[mode];
  const r = figma.createRectangle();
  r.name = `swatch/${v.name}`; r.resize(120, 64); r.x = x; r.y = y; r.cornerRadius = 8;
  r.fills = [{ type: "SOLID", color: { r: val.r, g: val.g, b: val.b }, opacity: val.a ?? 1 }];
  page.appendChild(r);
  figma.bindVariable(r.id, "fills/0/color", v.id);
  bindPaint(r, "strokes", "gray/300"); r.strokeWeight = 1;
  label(v.name, x, y + 70, `name/${v.name}`, 12, 500, "gray/800");
  label(hexOf(val), x, y + 88, `value/${v.name}`, 12, 400, "gray/700");
  out.colors++;
});

// 2-2) 타이포 컴포넌트(키트 값 그대로 — meta-sm 10px 은 키트 단계라 린트 min-text-size 경고가 남는다)
let ty = 40 + Math.ceil(colorVars.length / 8) * 116 + 40;
label("Typography · 컴포넌트 typo/<이름>-<굵기>", 0, ty, "title/typography", 20, 600, "gray/800"); ty += 44;
for (const [name, px, weights, lh] of TYPO) {
  let tx = 0;
  for (const w of weights) {
    const t = figma.createText();
    t.fontName = { family: FAMILY, style: WEIGHT[w] };
    t.characters = `${name}-${w} 시술현황 ${px}`;
    t.fontSize = px;
    t.lineHeight = { unit: "PERCENT", value: lh * 100 };
    t.letterSpacing = { unit: "PIXELS", value: 0 };
    bindPaint(t, "fills", "gray/800");
    page.appendChild(t);
    const comp = figma.createComponentFromNode(t);
    comp.name = `typo/${name}-${w}`;
    comp.fills = [];  // 컴포넌트 기본 흰 면(하드코딩) 제거
    t.name = "sample";
    comp.x = Math.round(tx); comp.y = ty;
    tx += Math.ceil(Math.max(comp.width, 200)) + 40;
    out.typo++;
  }
  ty += Math.ceil(px * lh) + 24;
}

// 2-3) 그림자 컴포넌트(효과 스타일이 0.16.0 에 없어 effect-style-required 정보가 남는다)
ty += 20;
label("Shadow · 컴포넌트 shadow/<이름>", 0, ty, "title/shadow", 20, 600, "gray/800"); ty += 44;
Object.entries(SHADOWS).forEach(([name, sh], i) => {
  const f = figma.createFrame();
  f.resize(200, 100); f.cornerRadius = 8;
  bindPaint(f, "fills", "white");
  const c = parse(sh.color);
  f.effects = [{ type: "DROP_SHADOW", color: { r: c.r, g: c.g, b: c.b, a: sh.a }, offset: { x: sh.x, y: sh.y }, radius: sh.blur, spread: 0, visible: true, blendMode: "NORMAL" }];
  page.appendChild(f);
  const comp = figma.createComponentFromNode(f);
  comp.name = `shadow/${name}`;
  comp.x = i * 240; comp.y = ty;
  label(name, i * 240, ty + 112, `name/shadow/${name}`, 12, 500, "gray/800");
  out.shadows++;
});

figma.currentPage = homePage;
out;
