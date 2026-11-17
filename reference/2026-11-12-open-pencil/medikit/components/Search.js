// Search — 시안 .search 110–120 · .header .search 107–108 · .pop-search .search 231 · .dn-search 520 · 마크업 726 · 1085 · 1446
// 공통: 테두리 1 gray/300 · 면 white · 글자 14/400 lh1.5 · placeholder gray/600(--text-placeholder) · 아이콘 search 16 · focus = 테두리 primary(115)
// ss  = 헤더: 200×28 · 여백 0 16 · 간격 16 · r4 · 아이콘 오른쪽 · 「고객 검색」(726)
// m   = 시술 완료 탭: 200×36 · 여백 7 16 · 간격 16 · r8 · 아이콘 오른쪽 · 「고객 이름」(1446)
// m-left = 팝오버: 224×36(240 − 여백 8×2) · 여백 7 12 · 간격 8 · r8 · 아이콘 왼쪽 · 「검색」(1085)
const SIZE = {
  ss: { w: 200, h: 28, py: 0, px: 16, gap: 16, radius: 4, left: false, ph: "고객 검색" },
  m: { w: 200, h: 36, py: 7, px: 16, gap: 16, radius: 8, left: false, ph: "고객 이름" },
  "m-left": { w: 224, h: 36, py: 7, px: 12, gap: 8, radius: 8, left: true, ph: "검색" },
};
const variants = [];
for (const size of ["ss", "m", "m-left"]) for (const state of ["default", "focus"]) {
  const s = SIZE[size];
  const label = grow(text(s.ph, "heading-sm-400", "gray/600", { name: "label" }));
  const ic = icon("search");
  const f = box("HORIZONTAL", {
    name: "search", w: s.w, h: s.h, px: s.px, py: s.py, gap: s.gap, radius: s.radius,
    bg: "white", border: state === "focus" ? "primary/DEFAULT" : "gray/300",
    children: s.left ? [ic, label] : [label, ic],
  });
  label.textAutoResize = "HEIGHT";
  variants.push({ props: { size, state }, node: f });
}
makeSet("Search", variants, { perRow: 2, description: "시안 .search — ss 헤더 28 · m 36(시술 완료 탭) · m-left 팝오버(아이콘 왼쪽). focus = 테두리 primary" });
