// CardRow — 인박스 카드 안 시술 줄. 폭 238 = 카드 256 − 테두리 1×2 − .card-body 여백 8×2
// proc-link = 시술 완료 카드 `.chart-card .card-row.is-link` 560 · `.row-name::before` 563 · `.ch-icons` 564 · 템플릿 doneRoomCard 1435 · chartIcons 1468
//   여백 4 6 · 간격 6 · r6 · 면 없음(hover 만 bg-subtle) · 점 3×3 + 이름 12/400 lh1.3 black(flex 1) + 차트 아이콘 16 두 개(간격 4)
// call-proc = 호출 탭 카드 `.cl-proc` 399 → `body.crm .crm-card .card-list .cl-proc` 678–679 · 템플릿 renderCallsTab 1050
//   여백 2 · 간격 6 · 가운데 맞춤 · 점 3×3(currentColor = black) + 이름 12/400 lh1.3 black
function dot() {
  const d = figma.createEllipse();
  d.name = "dot";
  d.resize(3, 3);
  fill(d, "black");
  return d;
}
function cardRow(kind) {
  const label = text(kind === "proc-link" ? "리쥬란 힐러 2cc" : "울쎄라피 프라임 300 shot", "caption-md-400", "black", { name: "label" });
  const children = [dot(), label];
  if (kind === "proc-link") children.push(box("HORIZONTAL", { name: "chart-icons", gap: 4, children: [icon("chart-nurse-on"), icon("chart-doctor-off")] }));
  const o = kind === "proc-link"
    ? { name: "card-row", w: 238, pt: 4, pb: 4, pl: 6, pr: 6, gap: 6, radius: 6 }
    : { name: "card-row", w: 238, p: 2, gap: 6 };
  const row = box("HORIZONTAL", { ...o, children });
  grow(label); label.textAutoResize = "HEIGHT";
  return row;
}
const variants = ["proc-link", "call-proc"].map((kind) => ({ props: { kind }, node: cardRow(kind) }));
makeSet("CardRow", variants, { perRow: 2, description: "인박스 카드 안 시술 줄 — proc-link(시술 완료 카드 · 누르면 차트 · 간호/의사 차트 아이콘 on/off) · call-proc(호출 탭 카드 시술 목록). 폭 238(카드 안에서는 늘려 씀). 시안 .card-row.is-link 560 · .cl-proc 399 · 678" });
