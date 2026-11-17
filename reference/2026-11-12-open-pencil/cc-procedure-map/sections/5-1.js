// 5-1 귀가 대기 — 화면 1
// DIFF: 시안은 귀가 대기 카드가 판에서 빠지고(결정 U8) 카드 더보기 메뉴가 없음 → 기획안 L656 「⋯」 더보기 「귀가 대기 취소」를 시안 MoreMenu menu 모양으로

unit("procedure/customer-card/more-menu", (ctx) => {
  const m = inst2("MoreMenu", { kind: "menu" }, { label: "귀가 대기 취소" }, "more-menu/going-wait");
  ctx.mark(1, findIn(m, "menu-row"));
  return box("VERTICAL", { name: "design", children: [m] });
});
