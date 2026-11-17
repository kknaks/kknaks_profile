// Checkbox — 시안 .checkbox 138 · .is-checked 145 · .is-mixed 212–213 · .is-off 552 · procRow3(1139–1141)
// 16×16 · r4 · 테두리 1 gray/300 · 면 white. checked/mixed = primary 면·테두리. checked = check-white 12 (padding box 기준 left1 top1 → 2,2)
// mixed = 흰 막대(left3 right3 top6.5 h1.5 r1 · padding box 기준 → x4 y7.5 · 8×1.5). off = 면 gray/200 · 테두리 gray/300
function checkbox(state) {
  const f = figma.createFrame();
  f.name = "checkbox";
  f.resize(16, 16);
  f.cornerRadius = 4;
  f.clipsContent = false;
  const on = state === "checked" || state === "mixed";
  fill(f, on ? "primary/DEFAULT" : state === "off" ? "gray/200" : "white");
  stroke(f, on ? "primary/DEFAULT" : "gray/300", 1);
  if (state === "checked") {
    const ic = icon("check-white");
    ic.name = "icon/check";
    f.appendChild(ic); ic.x = 2; ic.y = 2;
  }
  if (state === "mixed") {
    const bar = figma.createRectangle();
    bar.name = "mixed-bar";
    bar.resize(8, 1.5);
    bar.cornerRadius = 1;
    fill(bar, "white");
    f.appendChild(bar); bar.x = 4; bar.y = 7.5;
  }
  return f;
}
const variants = ["default", "checked", "mixed", "off"].map((state) => ({ props: { state }, node: checkbox(state) }));
makeSet("Checkbox", variants, { perRow: 4, description: "시안 .checkbox — default · checked(is-checked) · mixed(is-mixed) · off(is-off · 준비중이 아닌 줄)" });
