// MenuRow — .menu-row 209 · :disabled 215(--text-disabled #9f9f9f · 면 없음). 폭 188 = .more-pop 200 − 여백 6×2(208). 문구 renderMorePop 1244
const variants = [["default", "시작 취소", "black"], ["disabled", "완료 취소", "gray/600"]].map(([state, str, tk]) => ({
  props: { state },
  node: box("HORIZONTAL", { name: "menu-row", w: 188, h: 36, px: 10, gap: 10, radius: 8, align: "CENTER", children: [text(str, [14, 400, 21], tk, { name: "label" })] }),
}));
makeSet("MenuRow", variants, { perRow: 2, description: "More Menu Panel 안 Menu Row — 폭 188 · 높이 36 · 여백 0 10 · r8 · 14/400. 시안 .more-pop 208 · .menu-row 209" });
