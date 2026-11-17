// 시술현황 맵 — 화면 → 화면 화살표(마지막에 한 번). run-map.sh 가 앞에 붙인다:
//   const DATA = { edges };  + ../medikit/components/_icons.js + _lib.js(TARGET_PAGE="components")
// 화살표 = 페이지 맨 위 프레임 `edge/<from>→<to>`(같은 쌍이 둘 이상이면 `#2` …) 안에 선(vector) + 화살촉 + 트리거 라벨.
// 끝점 = 각 화면 프레임 `screen/<id>` 안 디자인(첫 자식)의 바깥 상자. 고아(끝 화면이 맵에 없음) = 오류로 센다.
// 종류(kind): nav 이동(파랑 실선) · contains 포함(회색 점선) · event 바깥 사건(보라 점선) · ref 참조(회색 점선 · 범위 밖)
const MAP_NAME = "시술현황 맵";
const MAP = figma.root.children.find((p) => p.name === MAP_NAME);
if (!MAP) throw new Error("「시술현황 맵」 페이지가 없다 — 섹션부터 그려라");
const STYLE = {
  nav: { color: "primary/DEFAULT", w: 2, dash: null, tag: "" },
  contains: { color: "gray/600", w: 1.5, dash: [8, 6], tag: "포함 · " },
  event: { color: "purple/DEFAULT", w: 1.5, dash: [3, 5], tag: "사건 · " },
  ref: { color: "gray/500", w: 1.5, dash: [8, 6], tag: "참조 · " },
};
const R = { edges: 0, orphans: [], stray: 0 };
const before = new Map(figma.root.children.map((p) => [p.id, new Set(p.children.map((c) => c.id))]));

for (const n of [...MAP.children]) if (n.name.startsWith("edge/")) n.remove();

const boxes = new Map();
MAP.findAll((n) => n.name.startsWith("screen/")).forEach((f) => {
  const d = f.children.find((c) => !c.name.startsWith("marker/")) || f;
  const b = d.absoluteBoundingBox;
  const id = f.name.slice(7);
  const nt = MAP.findOne((n) => n.name === `notes/${id}`);
  const nb = nt ? nt.absoluteBoundingBox : b;
  // ux · uw = 화면 + 메모 칸(유닛) 가로 범위 — 옆으로 가는 화살표는 메모 칸 바깥에서 나간다
  boxes.set(id, { x: b.x, y: b.y, w: b.width, h: b.height, ux: b.x, uw: Math.max(b.x + b.width, nb.x + nb.width) - b.x });
});

const pairCount = new Map();
const r1 = (v) => Math.round(v * 10) / 10;
for (const e of DATA.edges) {
  const A = boxes.get(e.from), B = boxes.get(e.to);
  if (!A || !B) { R.orphans.push(`${e.from}→${e.to}`); continue; }
  const key = `${e.from}→${e.to}`;
  const i = (pairCount.get(key) || 0); pairCount.set(key, i + 1);
  const off = i * 28;
  const st = STYLE[e.kind || "nav"];
  let P0, P1, P2, P3;
  if (e.from === e.to) {           // 자기 자신(재호출): 위쪽 고리
    P0 = [A.x + A.w - 24, A.y]; P3 = [A.x + A.w - 96, A.y];
    P1 = [P0[0], A.y - 90]; P2 = [P3[0], A.y - 90];
  } else if (B.x >= A.ux + A.uw) {   // 오른쪽(메모 칸 바깥에서)
    P0 = [A.ux + A.uw, A.y + Math.min(A.h / 2, 60) + off]; P3 = [B.x, B.y + Math.min(B.h / 2, 60) + off];
    const dx = Math.max(60, (P3[0] - P0[0]) / 2); P1 = [P0[0] + dx, P0[1]]; P2 = [P3[0] - dx, P3[1]];
  } else if (B.ux + B.uw <= A.x) {   // 왼쪽(대상 메모 칸 바깥으로)
    P0 = [A.x, A.y + Math.min(A.h / 2, 60) + off]; P3 = [B.ux + B.uw, B.y + Math.min(B.h / 2, 60) + off];
    const dx = Math.max(60, (P0[0] - P3[0]) / 2); P1 = [P0[0] - dx, P0[1]]; P2 = [P3[0] + dx, P3[1]];
  } else if (B.y >= A.y) {         // 아래
    P0 = [A.x + A.w / 2 + off, A.y + A.h]; P3 = [B.x + B.w / 2 + off, B.y];
    const dy = Math.max(60, (P3[1] - P0[1]) / 2); P1 = [P0[0], P0[1] + dy]; P2 = [P3[0], P3[1] - dy];
  } else {                         // 위
    P0 = [A.x + A.w / 2 + off, A.y]; P3 = [B.x + B.w / 2 + off, B.y + B.h];
    const dy = Math.max(60, (P0[1] - P3[1]) / 2); P1 = [P0[0], P0[1] - dy]; P2 = [P3[0], P3[1] + dy];
  }
  // 화살촉(끝점 P3 · 접선 P2→P3)
  const ang = Math.atan2(P3[1] - P2[1], P3[0] - P2[0]), L = 12, Wd = 6;
  const back = [P3[0] - L * Math.cos(ang), P3[1] - L * Math.sin(ang)];
  const H1 = [back[0] + Wd * Math.sin(ang), back[1] - Wd * Math.cos(ang)], H2 = [back[0] - Wd * Math.sin(ang), back[1] + Wd * Math.cos(ang)];
  const pts = [P0, P1, P2, P3, H1, H2];
  const minX = Math.min(...pts.map((p) => p[0])) - 4, minY = Math.min(...pts.map((p) => p[1])) - 4;
  const maxX = Math.max(...pts.map((p) => p[0])) + 4, maxY = Math.max(...pts.map((p) => p[1])) + 4;
  const loc = (p) => `${r1(p[0] - minX)} ${r1(p[1] - minY)}`;

  const f = figma.createFrame();
  MAP.appendChild(f);
  f.name = `edge/${key}${i ? `#${i + 1}` : ""}`;
  f.x = Math.round(minX); f.y = Math.round(minY); f.resize(Math.max(1, Math.round(maxX - minX)), Math.max(1, Math.round(maxY - minY)));
  f.fills = []; f.clipsContent = false;

  const line = figma.createVector();
  f.appendChild(line);
  line.name = "edge-path";
  line.vectorPaths = [{ windingRule: "NONE", data: `M ${loc(P0)} C ${loc(P1)} ${loc(P2)} ${loc(back)}` }];
  line.fills = [];
  stroke(line, st.color, st.w); line.strokeAlign = "CENTER";
  if (st.dash) line.dashPattern = st.dash;
  line.x = 0; line.y = 0;

  const head = figma.createVector();
  f.appendChild(head);
  head.name = "arrow-head";
  head.vectorPaths = [{ windingRule: "NONZERO", data: `M ${loc(P3)} L ${loc(H1)} L ${loc(H2)} Z` }];
  fill(head, st.color);
  head.x = 0; head.y = 0;

  // 라벨 = 곡선 가운데(t=0.5)
  const mid = [0, 1].map((k) => (P0[k] + 3 * P1[k] + 3 * P2[k] + P3[k]) / 8);
  const trig = String(e.triggerLabel || e.trigger);
  const lab = box("HORIZONTAL", {
    name: "label", px: 6, py: 2, gap: 6, radius: 4, bg: "white", border: st.color,
    children: [
      text(`${st.tag}${trig}`, "caption-md-500", st.color === "gray/500" ? "gray/700" : st.color, { name: "label/trigger" }),
      text(e.source, "caption-md-400", "gray/700", { name: "label/source" }),
    ],
  });
  f.appendChild(lab);
  lab.x = Math.round(mid[0] - minX - lab.width / 2); lab.y = Math.round(mid[1] - minY - lab.height / 2 - (e.from === e.to ? 30 : 0));
  R.edges++;
}
for (const p of figma.root.children) {
  if (p === MAP) continue;
  const b = before.get(p.id) || new Set();
  for (const c of [...p.children]) if (!b.has(c.id)) { c.remove(); R.stray++; }
}
R.unbound = STATS.unbound.length;
JSON.stringify(R);
