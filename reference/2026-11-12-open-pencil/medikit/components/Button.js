// Button — 시안 .btn 150 · .btn-m 155 · .btn-solid/.btn-filled/.btn-outlined-gray 156–162 · .btn-outlined-black 129 · .btn-filled-gray 674
// 크기: l = .cm-box > .cm-foot .btn 607 · m = .btn-m 155 · m-dialog = .cm-foot .btn 606 · .dn-empty .btn 527 · s = .pop-foot .btn 245 · .held-actions .btn 634
//       ss = .btn 150 · xs = .proc3 .btn 430. disabled = .btn:disabled 169. 높이 고정 · 가로는 글자에 맞춤.
// 줄높이: .btn 1.3(held-actions 만 1.5)
const SIZE = {
  l: { h: 44, px: 16, py: 0, r: 8, typo: [16, 500, 21] },
  m: { h: 36, px: 16, py: 0, r: 8, typo: [14, 500, 18] },
  "m-dialog": { h: 36, px: 12, py: 0, r: 6, typo: [14, 500, 18] },
  s: { h: 33, px: 12, py: 0, r: 6, typo: [14, 500, 18] },
  ss: { h: 28, px: 8, py: 6, r: 4, typo: [12, 500, 16] },
  xs: { h: 24, px: 8, py: 4, r: 4, typo: [12, 500, 16] },
};
const KIND = {
  solid: { bg: "primary/DEFAULT", fg: "white" },
  filled: { bg: "primary/100", fg: "primary/DEFAULT" },
  "filled-gray": { bg: "gray/200", fg: "gray/700" },
  "outlined-gray": { bg: "white", fg: "gray/600", border: "gray/300" },
  "outlined-black": { bg: "white", fg: "black", border: "gray/500" },
};
const DISABLED = { bg: "gray/200", fg: "gray/600" };
// [kind, size, state, 문구, 줄높이 덮어쓰기]
const LIST = [
  ["solid", "l", "default", "저장"],
  ["solid", "m", "default", "2개 호출"],
  ["filled", "m", "default", "귀가 대기"],
  ["solid", "m-dialog", "default", "닫기"],
  ["outlined-gray", "m-dialog", "default", "취소"],
  ["solid", "s", "default", "재호출"],
  ["solid", "s", "disabled", "재호출"],
  ["filled-gray", "s", "default", "연결 풀기", 21], // .held-actions .btn line-height 1.5
  ["solid", "ss", "default", "수락"],
  ["outlined-gray", "ss", "default", "재호출"],
  ["solid", "xs", "default", "시작"],
  ["outlined-black", "xs", "default", "종료"],
];
const variants = LIST.map(([kind, size, state, str, lh]) => {
  const s = SIZE[size];
  const k = state === "disabled" ? { ...KIND[kind], ...DISABLED } : KIND[kind];
  const typo = lh ? [s.typo[0], s.typo[1], lh] : s.typo;
  const node = box("HORIZONTAL", {
    name: "button", h: s.h, px: s.px, py: s.py, radius: s.r, justify: "CENTER", align: "CENTER",
    bg: k.bg, border: k.border,
    children: [text(str, typo, k.fg, { name: "label" })],
  });
  return { props: { kind, size, state }, node };
});
makeSet("Button", variants, { perRow: 6, description: "메디킷 Button — 시안에 나오는 조합만. 높이 고정 · 가로는 글자에 맞춤. 시안 .btn 150 · 129 · 674 · .proc3 .btn 430 · .pop-foot .btn 245 · .held-actions .btn 634 · .cm-foot .btn 606–607 · .dn-empty .btn 527" });
