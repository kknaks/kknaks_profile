// IconButton — .icon-btn 315(gray/500) · .proc-more 439(gray/600) · .pop-close 228(x gray/700) · .cm-close 585(24×24 · x-24) · .memo-more 541 · 569(면 white · maximize-2)
const LIST = [
  ["grip", "grip", "gray/500", 16, null],
  ["more", "more", "gray/600", 16, null],
  ["close", "x", "gray/700", 16, null],
  ["close-24", "x-24", "gray/600", 24, null],   // SVG 색 #9f9f9f 그대로
  ["maximize", "maximize-2", "gray/600", 16, "white"], // SVG 색 #9f9f9f 그대로
];
const variants = LIST.map(([key, ic, tk, size, bg]) => {
  const node = box("HORIZONTAL", { name: "icon-button", w: size, h: size, radius: 4, justify: "CENTER", align: "CENTER", bg, children: [icon(ic, tk)] });
  return { props: { icon: key }, node };
});
makeSet("IconButton", variants, { perRow: 5, description: "아이콘 버튼 — 16×16 r4(close-24 = 24×24). 시안 .icon-btn 315 · .proc-more 439 · .pop-close 228 · .cm-close 585 · .memo-more 541 · 569" });
