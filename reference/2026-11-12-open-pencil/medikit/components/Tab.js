// Tab — header = .tab 102–104 · inbox = .ib-tab 170–172 · 150(::after 아래 -1 · 2) · modal = .cm-tabs .ib-tab 588–590. 고른 색 = body.crm --text-brand(= primary) 669–670
// 밑줄 = 사각형 `underline`(오토레이아웃 밖 절대 위치 · 좌우 꽉 · 시안 bottom 값)
const KIND = {
  header: { label: "시술 현황", typo: [14, 500, 21], on: [14, 500, 21], pb: 4, ul: 3, bottom: 0 },
  inbox: { label: "현황", typo: [14, 400, 21], on: [14, 600, 21], pb: 4, ul: 2, bottom: -1 },
  modal: { label: "간호 관리 차트", typo: [16, 400, 24], on: [16, 500, 24], pb: 8, ul: 3, bottom: 0 },
};
const variants = [];
for (const kind of ["header", "inbox", "modal"]) for (const state of ["default", "active"]) {
  const k = KIND[kind], on = state === "active";
  const node = box("VERTICAL", { name: "tab", pb: k.pb, children: [text(k.label, on ? k.on : k.typo, on ? "primary/DEFAULT" : "gray/600", { name: "label" })] });
  if (on) {
    const u = figma.createRectangle();
    u.name = "underline";
    node.appendChild(u);
    u.layoutPositioning = "ABSOLUTE";
    u.resize(node.width, k.ul);
    u.x = 0; u.y = node.height - k.ul - k.bottom;
    u.cornerRadius = 3;
    u.constraints = { horizontal: "STRETCH", vertical: "MAX" };
    fill(u, "primary/DEFAULT");
  }
  variants.push({ props: { kind, state }, node });
}
makeSet("Tab", variants, { perRow: 6, description: "탭 — header(.tab 102) · inbox(.ib-tab 170) · modal(.cm-tabs .ib-tab 588). active = primary + 밑줄(header 3 · inbox 2 아래 -1 · modal 3, 모서리 3)" });
