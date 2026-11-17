// 시술현황 맵 공통 도구 — OpenPencil 0.16.0 headless(`eval medikit.fig -w --stdin`).
// 실행 순서(run-section.sh 가 한 eval 로 붙인다):
//   const DATA = { section, screens, notes };   ← layout.json 섹션 하나 + 그 섹션 화면 · 메모
//   ../medikit/components/_icons.js + _lib.js   ← TARGET_PAGE="components" (inst() 는 「components」 세트를 찾는다)
//   _maplib.js(이 파일) → sections/<절>.js → JSON.stringify(mapDone())
//
// 섹션 스크립트가 쓰는 것:
//   unit(screenId, (ctx) => 디자인노드)   화면 하나 = 캡션 + 화면 프레임 `screen/<id>`(layout 슬롯) + 마커 + 메모 카드
//     ctx.mark(no, node)                   screens.json elements[no] 가 가리키는 노드(마커 ①②③ 자리)
//     ctx.w · ctx.h                        화면 슬롯 크기(디자인은 이 안에 들어가야 한다)
//   inst2(set, props, texts, name)          inst() + 같은 이름 글자 자리 여럿: texts = { label: ["시술실 A", null, "마취 시작"] }(null = 그대로)
//   setText(node, name, value, nth=0) · hideIn(node, name, nth=0) · findIn(node, name, nth=0)
//   custom(name, node)                      세트에 없는 요소 → 이름 `custom/<name>` + 리포트 목록
//   detach(instance, name)                  합성 인스턴스를 떼어 고칠 때(안쪽 인스턴스는 남음) → `custom/<name>`
//   그 밖 _lib.js 의 box · text · icon · fill · stroke · grow · stretch · shadows · COLORS · TYPO 그대로
//
// ⚠ 만든 노드는 전부 디자인 트리 안에 넣는다. 다른 페이지에 남은 새 노드는 mapDone() 이 지우고 오류로 센다.

const MAP_NAME = "시술현황 맵";
const NOTE_KIND = { policy: "정책", memo: "기획 메모", "open-question": "기획 담당자 확인 필요" };
const MARK_TOKEN = "purple/DEFAULT"; // 맵 주석 색(세트 테두리와 같은 보라) — 제품 색(primary · red)과 겹치지 않게
const SOURCE_DOC = "cc-기획안-시술현황";

const MAP = (() => {
  let p = figma.root.children.find((x) => x.name === MAP_NAME);
  if (!p) { p = figma.createPage(); p.name = MAP_NAME; }
  p.backgrounds = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: 1 }];
  return p;
})();
try { figma.currentPage = MAP; } catch (e) { /* headless 에 없으면 그대로 — 아래 정리가 막는다 */ }
const _BEFORE = new Map(figma.root.children.map((p) => [p.id, new Set(p.children.map((c) => c.id))]));
const RESULT = { section: DATA.section.key, screens: [], markers: 0, missingMarkers: [], notes: 0, instances: 0, custom: [], overflow: [], stray: 0 };

// text() 다시 정의 — headless 0.16.0 은 글자를 넣은 뒤 폭을 주면 높이가 한 줄로 남는다(줄바꿈 안 됨).
// 폭이 있으면 폭 → HEIGHT → 글자 순서로 넣는다(2026-11-12 실측). 그 밖은 _lib.js text() 와 같다.
text = function (str, typo, color = "black", o = {}) {
  const [px, w, lh] = Array.isArray(typo) ? typo : TYPO[typo];
  if (px === undefined) throw new Error(`타이포 없음: ${typo}`);
  const t = figma.createText();
  t.fontName = { family: FAMILY, style: WEIGHT[w] };
  t.fontSize = px;
  t.lineHeight = { unit: "PIXELS", value: lh };
  if (o.ls) t.letterSpacing = { unit: "PIXELS", value: o.ls };
  if (o.width) { t.resize(Math.round(o.width), lh); t.textAutoResize = "HEIGHT"; } else t.textAutoResize = "WIDTH_AND_HEIGHT";
  t.characters = String(str);
  fill(t, color, o.opacity ?? 1);
  if (o.align) t.textAlignHorizontal = o.align;
  t.name = o.name || "label";
  return t;
};

const _inst0 = inst;
inst = function (setName, props, texts, name) { RESULT.instances++; return _inst0(setName, props, texts, name); };

function findIn(node, name, nth = 0) {
  const all = node.findAll((n) => n.name === name);
  return all[nth] || null;
}
function setText(node, name, value, nth = 0) {
  const all = node.findAll((n) => n.type === "TEXT" && n.name === name);
  const t = all[nth];
  if (!t) throw new Error(`글자 자리 없음: ${node.name}.${name}[${nth}]`);
  t.characters = String(value);
  return t;
}
function hideIn(node, name, nth = 0) {
  const n = findIn(node, name, nth);
  if (!n) throw new Error(`노드 없음: ${node.name}.${name}[${nth}]`);
  n.visible = false;
  return n;
}
// inst() + 글자 자리 여럿. texts 값이 배열이면 같은 이름 n 번째에 차례로(null 은 건너뜀)
function inst2(setName, props = {}, texts = {}, name) {
  const i = inst(setName, props, {}, name);
  for (const [k, v] of Object.entries(texts)) {
    if (Array.isArray(v)) v.forEach((x, n) => { if (x !== null && x !== undefined) setText(i, k, x, n); });
    else setText(i, k, v, 0);
  }
  return i;
}
function custom(name, node) {
  node.name = `custom/${name}`;
  if (!RESULT.custom.includes(name)) RESULT.custom.push(name);
  return node;
}

// 합성 세트 인스턴스(RoomCard · InboxCard · Popover · ChartModal …)에 기획안 요소를 더하거나 빼야 할 때:
// 떼어 낸다(detach) → 안쪽 인스턴스(ProcRow · Button · Badge …)는 인스턴스로 남는다. 이름 `custom/<name>` + 리포트 목록
function detach(instance, name) {
  const d = instance.detachInstance();
  RESULT.detached = (RESULT.detached || 0) + 1;
  return custom(name, d);
}

function _section() {
  const s = DATA.section;
  let f = MAP.children.find((n) => n.name === `section/${s.key}`);
  if (!f) {
    f = figma.createFrame();
    MAP.appendChild(f);
    f.name = `section/${s.key}`;
    f.x = s.x; f.y = s.y; f.resize(s.w, s.h);
    fill(f, "gray/100"); stroke(f, "gray/300", 2); f.cornerRadius = 24; f.clipsContent = false;
    const t = text(s.title, [40, 600, 56], "black", { name: "title" });
    f.appendChild(t); t.x = 80; t.y = 48;
  }
  return f;
}
function _rel(node, frame) {
  const a = node.absoluteBoundingBox, b = frame.absoluteBoundingBox;
  return { x: a.x - b.x, y: a.y - b.y, w: a.width, h: a.height };
}
function _marker(label, name) {
  const t = text(label, [11, 600, 14], "white", { name: "label", align: "CENTER" });
  const m = box("HORIZONTAL", { name, w: 20, h: 20, radius: 10, bg: MARK_TOKEN, justify: "CENTER", align: "CENTER", children: [t] });
  return m;
}
function _noteCard(n) {
  const open = n.kind === "open-question";
  const head = [];
  if (n.elementNo !== null && n.elementNo !== undefined) head.push(_marker(String(n.elementNo), "marker-ref"));
  head.push(text(NOTE_KIND[n.kind] || n.kind, "caption-md-600", open ? "red/DEFAULT" : n.kind === "memo" ? "gray/800" : "primary/DEFAULT", { name: "label/kind" }));
  const card = box("VERTICAL", {
    name: `note/${n.id}`, w: DATA_NOTE_W, p: 12, gap: 6, radius: 8, bg: "white",
    border: open ? "red/DEFAULT" : "gray/300", borderW: open ? 2 : 1,
    children: [
      box("HORIZONTAL", { name: "note-head", gap: 6, children: head }),
      text(n.body, "caption-md-400", "black", { name: "label/body", width: DATA_NOTE_W - 24 }),
      text(`${SOURCE_DOC} · ${n.source}`, "caption-md-400", "gray/700", { name: "label/source" }),
    ],
  });
  RESULT.notes++;
  return card;
}
const DATA_NOTE_W = 360;

// 화면 하나 그리기
function unit(screenId, build) {
  const slot = DATA.section.slots.find((s) => s.screenId === screenId);
  if (!slot) throw new Error(`layout 슬롯 없음: ${screenId} @ section ${DATA.section.key}`);
  const scr = DATA.screens.find((s) => s.screenId === screenId);
  if (!scr) throw new Error(`screens.json 에 없음: ${screenId}`);
  const sec = _section();
  for (const n of [...sec.children]) if ([`screen/${screenId}`, `caption/${screenId}`, `notes/${screenId}`].includes(n.name)) n.remove();

  const cap = box("HORIZONTAL", {
    name: `caption/${screenId}`, gap: 10, align: "MAX",
    children: [
      text(`${scr.section} · ${scr.name}`, [18, 600, 26], "black", { name: "label/name" }),
      text(`${screenId} · ${scr.kind} · P = ${SOURCE_DOC} ${scr.source.replace(/^P:/, "")}`, "caption-md-400", "gray/700", { name: "label/meta" }),
    ],
  });
  sec.appendChild(cap); cap.x = slot.caption.x; cap.y = slot.caption.y;

  const fr = figma.createFrame();
  sec.appendChild(fr);
  fr.name = `screen/${screenId}`;
  fr.x = slot.screen.x; fr.y = slot.screen.y; fr.resize(slot.screen.w, slot.screen.h);
  fr.fills = []; fr.clipsContent = false;

  const marks = new Map();
  const ctx = { id: screenId, screen: scr, w: slot.screen.w, h: slot.screen.h, mark: (no, node) => { marks.set(no, node); return node; } };
  const design = build(ctx);
  if (!design) throw new Error(`${screenId}: build() 가 노드를 돌려주지 않았다`);
  fr.appendChild(design); design.x = 0; design.y = 0;
  if (!design.name || /^(Frame|container)( \d+)?$/.test(design.name)) design.name = "design";
  if (design.width > slot.screen.w + 1 || design.height > slot.screen.h + 1)
    RESULT.overflow.push(`${screenId} ${Math.round(design.width)}×${Math.round(design.height)} > 슬롯 ${slot.screen.w}×${slot.screen.h}`);

  // 마커: 가리킨 노드 왼쪽 위 모서리. 같은 자리면 오른쪽으로 비켜 놓는다
  const used = [];
  let k = 0;
  for (const el of scr.elements) {
    const node = marks.get(el.no);
    let x, y;
    if (node) { const r = _rel(node, fr); x = r.x - 10; y = r.y - 10; }
    else { RESULT.missingMarkers.push(`${screenId}#${el.no}`); x = -10 + 24 * k++; y = -34; }
    while (used.some(([ux, uy]) => Math.abs(ux - x) < 20 && Math.abs(uy - y) < 20)) x += 22;
    used.push([x, y]);
    const m = _marker(String(el.no), `marker/${screenId}/${el.no}`);
    fr.appendChild(m); m.x = Math.round(x); m.y = Math.round(y);
    RESULT.markers++;
  }

  const ns = DATA.notes.filter((n) => n.screenId === screenId);
  const col = box("VERTICAL", { name: `notes/${screenId}`, w: DATA_NOTE_W, gap: 8, children: ns.map(_noteCard) });
  sec.appendChild(col); col.x = slot.notes.x; col.y = slot.notes.y;
  if (col.height > slot.notes.h + 1) RESULT.overflow.push(`notes/${screenId} 높이 ${Math.round(col.height)} > ${slot.notes.h}`);

  RESULT.screens.push(screenId);
  return fr;
}

// 끝: 다른 페이지에 새로 생긴 노드(appendChild 빠뜨린 것)를 지우고 센다
function mapDone() {
  for (const p of figma.root.children) {
    if (p === MAP) continue;
    const before = _BEFORE.get(p.id) || new Set();
    for (const c of [...p.children]) if (!before.has(c.id)) { c.remove(); RESULT.stray++; }
  }
  RESULT.unbound = STATS.unbound.length;
  return RESULT;
}
