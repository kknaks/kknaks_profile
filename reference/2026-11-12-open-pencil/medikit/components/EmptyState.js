// EmptyState — 메디킷 EmptyState. 시안 `.dn-empty` 524–527 · 템플릿 renderDoneTab 1447
// 바탕 · 테두리 없음 · 세로 가운데 · 간격 20 · 최소 높이 380 · 제목 18/600 lh1.5 black → Button m-dialog outlined-gray(.dn-empty .btn 36 · 0 12 · r6 · 14)
// 폭 256 = 인박스 카드 폭
const empty = box("VERTICAL", {
  name: "empty-state", w: 256, h: 380, gap: 20, align: "CENTER", justify: "CENTER",
  children: [
    text("조건에 맞는 고객이 없어요", "title-sm-600", "black", { name: "label", align: "CENTER" }),
    inst("Button", { kind: "outlined-gray", size: "m-dialog", state: "default" }, { label: "조건 지우기" }, "button"),
  ],
});
makeSet("EmptyState", [{ props: { state: "default" }, node: empty }], { description: "메디킷 EmptyState — 시술 완료 탭에서 찾는 이름이 없을 때. 최소 높이 380 가운데 · 제목 title/sm/600 → 20 → Outlined Gray M(조건 지우기). 시안 .dn-empty 525" });
