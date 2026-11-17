// SelectAll — 시안 .sel-all 455 · :disabled 570–571 · selAll()(1196–1197)
// 높이 24 · 여백 0 2 · 간격 6 · r4 · 「전체 선택」 12/400 lh1.3 gray/700. 체크박스 margin-left 1(138) → 왼쪽 여백 3
// disabled = 체크박스 gray/200 면 · gray/300 테두리 = Checkbox off
const CB = { default: "default", mixed: "mixed", checked: "checked", disabled: "off" };
const variants = ["default", "mixed", "checked", "disabled"].map((state) => ({
  props: { state },
  node: box("HORIZONTAL", {
    name: "sel-all", h: 24, pl: 3, pr: 2, gap: 6, radius: 4,
    children: [inst("Checkbox", { state: CB[state] }, {}, "checkbox"), text("전체 선택", "caption-md-400", "gray/700", { name: "label" })],
  }),
}));
makeSet("SelectAll", variants, { perRow: 4, description: "시안 .sel-all — 체크박스 자리는 Checkbox 인스턴스. disabled = 준비중 줄 0(Checkbox off)" });
