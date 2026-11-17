// 시술현황 시안 → OpenPencil 0.16.0 공통 도구. 실행 = _icons.js + _lib.js + <Name>.js 를 한 eval 로(run-one.sh · run-all.sh).
// 값 출처: 시안 `reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`(3차 v11) <style> + 변수 컬렉션 medikit.
// 색은 전부 변수 컬렉션 `medikit` 에 바인딩한다(COLORS 값은 바인딩 전 초기값 · 변수가 없으면 STATS.unbound 에 남는다).
//
// 대상 페이지: globalThis.TARGET_PAGE(기본 「components」). 시험은 run-one.sh --page draft/<그룹>.
// ⚠ figma.currentPage 에 기대지 않는다(병렬 eval 이 await 사이에 바꿀 수 있음) — 만든 노드는 반드시 명시적으로 appendChild.

const TARGET = globalThis.TARGET_PAGE || "components";

const COLORS = {
  // medikit 기존 29개 중 쓰는 것(값 변경 금지 — import-medikit.js 와 같다)
  "primary/DEFAULT": "#1d8bff", "primary/100": "#eff7ff", "primary/300": "#dbecff", "primary/500": "#99cbff",
  "red/DEFAULT": "#ff4e51", "red/100": "#ffefef", "red/300": "#ffe1e1", "red/500": "#ffc4c5",
  "yellow/DEFAULT": "#fd9400", "yellow/100": "#fff7ec", "yellow/300": "#ffe4c0",
  "purple/DEFAULT": "#ac47ff", "purple/100": "#f8f0ff",
  "gray/100": "#fbfbfb", "gray/200": "#f3f3f3", "gray/300": "#e3e3e3", "gray/400": "#d6d6d6",
  "gray/500": "#cfcfcf", "gray/600": "#9f9f9f", "gray/700": "#6e6e6e", "gray/800": "#3e3e3e",
  "black": "#000000", "white": "#ffffff", "hover-dark": "#222943",
  // 시안에만 있는 색 — _vars.js 가 컬렉션 medikit 에 추가한다(NEW_VARS 와 같은 값)
  "status/consult-wait": "#6c34cb", "status/consult-wait-100": "#f5f1fb", "status/consult-wait-300": "#e7dff7", "status/consult-wait-500": "#bda4e8",
  "status/consult": "#de4694", "status/consult-100": "#fdf2f8", "status/consult-300": "#fae1ee", "status/consult-500": "#f0accf",
  "status/proc-wait": "#4dbec1", "status/proc-wait-100": "#f3fafb", "status/proc-wait-300": "#e3f5f5", "status/proc-wait-500": "#afe2e3",
  "status/proc": "#f6ae53", "status/proc-100": "#fef9f3", "status/proc-300": "#fef2e3", "status/proc-500": "#fbdbb2",
  "status/going-wait": "#6ac13b", "status/going-wait-100": "#f5fbf1", "status/going-wait-300": "#e7f5e0", "status/going-wait-500": "#bce3a7",
  "status/gone": "#8c8c8c", "status/gone-100": "#f7f7f7", "status/gone-300": "#ededed", "status/gone-500": "#cbcbcb",
  // Badge solid 면 = 글자색 8% 를 흰 바탕에 합성한 불투명 단색(린트가 칠 불투명도를 무시해 1.00:1 거짓 대비를 내서 — 코디 2026-11-12)
  "status/badge-primary-8": "#edf6ff", "status/badge-red-8": "#fff1f1", "status/badge-gray-8": "#f4f4f5", "status/going-wait-8": "#f3faef",
  "crm/surface-head": "#f7f7f8",          // body.crm --surface-head (방 제목 줄 · 카드 머리)
  "crm/badge-gray": "#70737c",            // body.crm .cbadge.solid.gray 면 rgba(112,115,124,0.08) 의 색
  "crm/doctor-blue-border": "#e3f0ff",    // .avatar.doctor 테두리(tone-0)
  "crm/doctor-purple-border": "#eedcff",  // tone-1 테두리
  "crm/doctor-green": "#5aa832", "crm/doctor-green-100": "#eef8e7", "crm/doctor-green-border": "#dcf0cd", // tone-2
};
// 아이콘 SVG 안 색 → 변수
const HEX2TOKEN = { "1d8bff": "primary/DEFAULT", "9f9f9f": "gray/600", "6e6e6e": "gray/700", "ff4e51": "red/DEFAULT", "ffffff": "white", "e3e3e3": "gray/300", "cfcfcf": "gray/500", "000000": "black" };

// 타이포 [px, weight, lineHeight(px)] — medikit-preset.json 단계(줄높이 = px × 배수 반올림) + 시안에만 있는 값(아래 주석)
const TYPO = {
  "title-sm-600": [18, 600, 27], "title-sm-500": [18, 500, 27],
  "heading-md-600": [16, 600, 24], "heading-md-500": [16, 500, 24], "heading-md-400": [16, 400, 24],
  "heading-sm-600": [14, 600, 21], "heading-sm-500": [14, 500, 21], "heading-sm-400": [14, 400, 21],
  "body-600": [14, 600, 22], "body-500": [14, 500, 22], "body-400": [14, 400, 22],
  "caption-md-600": [12, 600, 16], "caption-md-500": [12, 500, 16], "caption-md-400": [12, 400, 16],
  "caption-md-400-lh18": [12, 400, 18],   // .memo-box 12/1.5 (시안 · 키트 단계 아님)
  "meta-sm-500": [10, 500, 13], "meta-sm-400": [10, 400, 13],
  "badge-11": [11, 500, 14],              // .cbadge 11/500 · line-height 1.273 · letter-spacing 0.34 (시안 · 키트 단계 아님)
  "notify-13": [13, 500, 16],             // .notify 13/500 line-height normal (시안 · 키트 단계 아님)
};
const WEIGHT = { 400: "Regular", 500: "Medium", 600: "SemiBold" };
const FAMILY = "Pretendard";
for (const w of [400, 500, 600]) await figma.loadFontAsync({ family: FAMILY, style: WEIGHT[w] });

const VARS = {};
for (const v of figma.getLocalVariables()) VARS[v.name] = v;
const STATS = { bound: 0, unbound: [] };

function page(name) {
  let p = figma.root.children.find((x) => x.name === name);
  if (!p) { p = figma.createPage(); p.name = name; p.backgrounds = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: 1 }]; }
  return p;
}
const PG = page(TARGET);

function rgb(hex) { const h = hex.replace("#", ""); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; }
// 칠 하나 = 변수 하나. opacity 는 칠 불투명도(시안 rgba · color-mix · currentColor 43% 같은 것)
function paint(node, field, token, opacity = 1) {
  if (!COLORS[token]) throw new Error(`색 토큰 없음: ${token}`);
  node[field] = [{ type: "SOLID", color: rgb(COLORS[token]), opacity }];
  const v = VARS[token];
  if (v) { figma.bindVariable(node.id, `${field}/0/color`, v.id); STATS.bound++; } else STATS.unbound.push(token);
}
const fill = (n, t, a = 1) => paint(n, "fills", t, a);
function stroke(n, t, w = 1, a = 1) { paint(n, "strokes", t, a); n.strokeWeight = w; n.strokeAlign = "INSIDE"; }

// text(글자, 타이포 키 또는 [px, weight, lhPx], 색 토큰, { name, width, align, ls, opacity })
// 바뀌는 글자 자리는 name 을 「label」(여러 개면 label/<역할>)로 둔다
function text(str, typo, color = "black", o = {}) {
  const [px, w, lh] = Array.isArray(typo) ? typo : TYPO[typo];
  if (px === undefined) throw new Error(`타이포 없음: ${typo}`);
  const t = figma.createText();
  t.fontName = { family: FAMILY, style: WEIGHT[w] };
  t.textAutoResize = "WIDTH_AND_HEIGHT";
  t.fontSize = px;
  t.lineHeight = { unit: "PIXELS", value: lh };
  if (o.ls) t.letterSpacing = { unit: "PIXELS", value: o.ls };
  t.characters = String(str);
  fill(t, color, o.opacity ?? 1);
  if (o.width) { t.textAutoResize = "HEIGHT"; t.resize(Math.round(o.width), t.height); }
  if (o.align) t.textAlignHorizontal = o.align;
  t.name = o.name || "label";
  return t;
}
// 오토레이아웃 프레임. o: name w h p px py pt pb pl pr gap align justify radius bg bgA border borderW borderA children clip
function box(dir = "VERTICAL", o = {}) {
  const f = figma.createFrame();
  f.name = o.name || "container";
  f.layoutMode = dir;
  if (o.w || o.h) f.resize(o.w || 10, o.h || 10);
  f.primaryAxisSizingMode = (dir === "HORIZONTAL" ? !!o.w : !!o.h) ? "FIXED" : "AUTO";
  f.counterAxisSizingMode = (dir === "HORIZONTAL" ? !!o.h : !!o.w) ? "FIXED" : "AUTO";
  const p = o.p ?? 0;
  f.paddingLeft = o.pl ?? o.px ?? p; f.paddingRight = o.pr ?? o.px ?? p;
  f.paddingTop = o.pt ?? o.py ?? p; f.paddingBottom = o.pb ?? o.py ?? p;
  f.itemSpacing = o.gap ?? 0;
  f.counterAxisAlignItems = o.align || (dir === "HORIZONTAL" ? "CENTER" : "MIN");
  f.primaryAxisAlignItems = o.justify || "MIN";
  if (o.radius) f.cornerRadius = o.radius;
  if (o.bg) fill(f, o.bg, o.bgA ?? 1); else f.fills = [];
  if (o.border) stroke(f, o.border, o.borderW || 1, o.borderA ?? 1);
  f.clipsContent = !!o.clip;
  for (const c of o.children || []) if (c) f.appendChild(c);
  return f;
}
// 자식 하나를 부모 폭에 맞춰 늘림(오토레이아웃 안에서)
function grow(n) { n.layoutGrow = 1; return n; }
function stretch(n) { n.layoutAlign = "STRETCH"; return n; }
// 그림자들: [[hex, alpha, x, y, blur, spread]] — 효과 색은 0.16.0 에서 변수 바인딩 대상이 아니라 값으로 둔다(리포트 기재)
function shadows(f, list) {
  f.effects = list.map(([hex, a, x, y, blur, spread = 0]) => ({ type: "DROP_SHADOW", color: { ...rgb(hex), a }, offset: { x, y }, radius: blur, spread, visible: true, blendMode: "NORMAL" }));
}
const SHADOW_CARD = [["#000000", 0.06, 0, 2, 4, 0]];          // --shadow-card
const SHADOW_ROOM = [["#000000", 0.06, 0, 2, 4, -2]];         // body.crm .room --shadow-card
const SHADOW_POPOVER = [["#cfcfcf", 1, 0, 0, 4, 0]];          // .pop · .more-pop(메디킷 pop-over)
const SHADOW_FLOAT = [["#000000", 0.08, 0, 2, 6, 0], ["#000000", 0.14, 0, 10, 28, 0]]; // .cm-box · .cm-confirm

// 아이콘: 시안 SVG 그대로 → 프레임 `icon/<이름>`, 칠 · 선은 변수 바인딩. token 을 주면 모든 색을 그 토큰으로(currentColor 자리)
function icon(name, token) {
  const svg = ICON_SVG[name];
  if (!svg) throw new Error(`아이콘 없음: ${name}`);
  const n = figma.createNodeFromSvg(svg);
  n.name = `icon/${name}`;
  n.fills = [];
  n.clipsContent = false;
  let i = 0;
  const walk = (x) => {
    if (x !== n) x.name = x.type === "VECTOR" ? `shape${i++ ? "-" + i : ""}` : (x.type === "ELLIPSE" ? `dot${i++ ? "-" + i : ""}` : `part${i++ ? "-" + i : ""}`);
    for (const field of ["fills", "strokes"]) {
      if (x === n && field === "fills") continue;
      const ps = x[field];
      if (!Array.isArray(ps) || !ps.length || ps[0].type !== "SOLID") continue;
      const c = ps[0].color;
      const hex = [c.r, c.g, c.b].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
      const tk = token || HEX2TOKEN[hex];
      if (!tk) { STATS.unbound.push(`icon ${name} #${hex}`); continue; }
      x[field] = ps.map((p, k) => (k ? p : { ...p, color: { ...rgb(COLORS[tk]), a: 1 } }));
      const v = VARS[tk];
      if (v) { figma.bindVariable(x.id, `${field}/0/color`, v.id); STATS.bound++; } else STATS.unbound.push(tk);
    }
    if ("children" in x) for (const k of x.children) walk(k);
  };
  walk(n);
  return n;
}

// ── 세트 · 인스턴스 ─────────────────────────────────
const vname = (props) => Object.entries(props).map(([k, v]) => `${k}=${v}`).join(", ");
const vparse = (name) => Object.fromEntries(name.split(",").map((s) => s.trim().split("=")));
function findSet(setName) {
  const s = PG.findOne ? PG.findOne((n) => n.type === "COMPONENT_SET" && n.name === setName) : null;
  if (!s) throw new Error(`세트 없음(먼저 렌더): ${setName} @ ${TARGET}`);
  return s;
}
// 세트의 variant 인스턴스. props 는 일부만 줘도 된다(첫 일치). texts = { label: "…", "label/time": "…" }
function inst(setName, props = {}, texts = {}, name) {
  const set = findSet(setName);
  const comp = set.children.find((c) => { const p = vparse(c.name); return Object.entries(props).every(([k, v]) => p[k] === String(v)); });
  if (!comp) throw new Error(`variant 없음: ${setName} ${vname(props)}`);
  const i = comp.createInstance();
  i.name = name || setName.replace(/^./, (c) => c.toLowerCase());
  for (const [k, v] of Object.entries(texts)) { const t = i.findOne((n) => n.type === "TEXT" && n.name === k); if (!t) throw new Error(`글자 자리 없음: ${setName}.${k}`); t.characters = String(v); }
  return i;
}
// variants: [{ props, node }] → 세트. 대상 페이지에 섹션(프레임 `section/<이름>` = 이름표 + 세트)으로 쌓는다. 다시 돌리면 그 섹션만 갈아 끼운다
function makeSet(setName, variants, o = {}) {
  for (const x of [...PG.children]) if (x.name === `section/${setName}`) x.remove();
  let y = 0;
  for (const x of PG.children) y = Math.max(y, x.y + x.height);
  y = y ? Math.ceil(y) + 80 : 0;
  const sec = box("VERTICAL", { name: `section/${setName}`, gap: 16 });
  PG.appendChild(sec);
  sec.x = 0; sec.y = y;
  sec.appendChild(text(setName, "title-sm-600", "black", { name: "title" }));
  if (o.note) sec.appendChild(text(o.note, "caption-md-400", "gray/700", { name: "note" }));
  const comps = variants.map(({ props, node }) => { sec.appendChild(node); const c = figma.createComponentFromNode(node); c.name = vname(props); return c; });
  const set = figma.combineAsVariants(comps, sec);
  set.name = setName;
  if (o.description) set.description = o.description;
  const perRow = o.perRow || 6, gap = 24;
  let cx = gap, cy = gap, rowH = 0, maxW = 0;
  comps.forEach((c, i) => {
    if (i && i % perRow === 0) { cx = gap; cy += rowH + gap; rowH = 0; }
    c.x = cx; c.y = cy; cx += Math.ceil(c.width) + gap; rowH = Math.max(rowH, Math.ceil(c.height)); maxW = Math.max(maxW, cx);
  });
  set.resize(Math.max(maxW, 200), cy + rowH + gap);
  fill(set, o.setBg || "white");
  stroke(set, "purple/DEFAULT", 1); set.dashPattern = [4, 4]; set.cornerRadius = 8;
  return { set: setName, variants: comps.length, unbound: STATS.unbound.length };
}
