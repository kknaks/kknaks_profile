// MoreMenu — 시안 `.more-pop` 208 · `.more-pop.is-combo` 636 · `.combo-scroll` 637 · `.combo-foot` 645–649 · 템플릿 `renderMorePop` 1234–1246 · `moveMenuHtml` 1386–1393
// 겉 = .pop(면 white · 그림자 0 0 4 #cfcfcf)
// menu  = More Menu Panel: 폭 200 · 여백 6 · r12 · MenuRow 「시작 취소」(진행중 시술 · 3차 v2 부터 이 한 줄)
// combo = ComboBox M 펼친 목록: 폭 200 · 여백 0 · r8 · ComboOption(고를 수 있는 방 먼저 → 꺼진 방) + 발(위 선 1 gray/200 · 여백 8 · Button m solid 꽉)
//         샘플 = 시술실 A 에서 옮길 때(목록에서 제 방 빠짐) · 시술실 F 를 고른 상태(발이 올라온 상태)
const menu = box("VERTICAL", { name: "more-menu", w: 200, p: 6, radius: 12, bg: "white", children: [inst("MenuRow", { state: "default" }, { label: "시작 취소" }, "menu-row")] });
shadows(menu, SHADOW_POPOVER);

const ROOMS = [["default", "레이저실 3"], ["on", "시술실 F"], ["disabled", "시술실 B"], ["disabled", "시술실 C"]];
const list = box("VERTICAL", { name: "combo-list", children: ROOMS.map(([state, str], i) => inst("ComboOption", { state }, { label: str }, `option-${i + 1}`)) });
list.layoutAlign = "STRETCH";
const line = figma.createRectangle();
line.name = "foot-line"; line.resize(200, 1); fill(line, "gray/200"); line.layoutAlign = "STRETCH";
const go = inst("Button", { kind: "solid", size: "m", state: "default" }, { label: "방 옮기기" }, "move");
const foot = box("VERTICAL", { name: "foot", p: 8, children: [go] });
foot.layoutAlign = "STRETCH";
go.layoutAlign = "STRETCH";
const combo = box("VERTICAL", { name: "more-menu", w: 200, radius: 8, bg: "white", clip: true, children: [list, line, foot] });
shadows(combo, SHADOW_POPOVER);

makeSet("MoreMenu", [{ props: { kind: "menu" }, node: menu }, { props: { kind: "combo" }, node: combo }], {
  perRow: 2,
  description: "시안 .more-pop — menu = 더보기(MenuRow · 진행중 「시작 취소」 / 완료 「완료 취소」) · combo = 방 옮기기(ComboOption 목록 최대 높이 220 · 고르면 발 [방 옮기기] · 원래 방이면 「돌아가기」).",
});
