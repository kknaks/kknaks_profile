// 2-1 관리실 이동 — 화면 4
// DIFF: menu = 기획안 「점유 이동」 · 「다른 관리실로 이동」 · 「원래 관리실로 복귀」(L297 · L301 · L326) ↔ 시안은 방 이름을 누르면 바로 방 고르기 콤보(moveMenuHtml) · 「연결」 개념(연결 풀기 · 돌아오기). 문구 · 요소는 기획안, 모양은 시안 MoreMenu menu(MenuRow) — 떼어 MenuRow 3줄. 「원래 관리실로 복귀」는 점유 이동 중일 때만 뜨지만 맵에서는 세 줄 다 보인다
// DIFF: list = 기획안은 빈 관리실을 고르면 바로 옮긴다(L327) ↔ 시안은 고른 뒤 아래 「방 옮기기」 버튼(+ 고른 줄 on 체크) — 기획안대로 발(foot-line · foot) 숨김, 줄은 모두 ComboOption default. 시안의 꺼진 방(disabled) 줄도 기획안 목록에 없어 뺐다
// DIFF: list · list-empty 머리 「점유 이동」 = 기획안 「관리실 이동 목록 | 「점유 이동」이나 「다른 관리실로 이동」 · 새로 배정할 빈 관리실」(L327) — 시안 콤보에는 머리가 없어 Popover 구역 라벨(10/500 gray/600) 모양으로 더함
// DIFF: list 방 이름 = 시안 빈 방 「레이저실 3」 · 「시술실 F」 + 기획안 예시 「A-룸2 (1/2)」(침대 둘 이상만 n/m)
// DIFF: list-empty 「빈 관리실 없음」 = 시안에 없음 — ComboOption 줄 자리(높이 44 · 여백 11 16 · 14/400)에 꺼진 글자색 gray/600
// DIFF: toast/room-full = 시안 Notify(primary 글자 · 체크 아이콘) 그대로 — 기획안은 오류 알림(style error)인데 세트에 오류 모양이 없어 체크 아이콘 · primary 색이 남는다

function roomMoveLabel(str) {
  const h = box("HORIZONTAL", { name: "list-label", pt: 8, pb: 4, pl: 16, pr: 16, children: [text(str, "meta-sm-500", "gray/600", { name: "heading" })] });
  return h;
}
function roomMoveCombo(name) {
  const c = detach(inst("MoreMenu", { kind: "combo" }, {}, "more-menu"), name);
  for (const nm of ["foot-line", "foot"]) { const n = c.children.find((x) => x.name === nm); if (n) n.visible = false; }
  const list = c.children.find((x) => x.name === "combo-list");
  for (const n of [...list.children]) n.remove();
  const head = roomMoveLabel("점유 이동");
  c.insertChild(0, head);
  head.layoutAlign = "STRETCH";
  return { c, list };
}

unit("procedure/room-move/menu", (ctx) => {
  const m = detach(inst("MoreMenu", { kind: "menu" }, {}, "more-menu"), "room-move-menu");
  const hold = findIn(m, "menu-row");
  hold.name = "menu-row/hold";
  setText(hold, "label", "점유 이동");
  const move = inst2("MenuRow", { state: "default" }, { label: "다른 관리실로 이동" }, "menu-row/move");
  const back = inst2("MenuRow", { state: "default" }, { label: "원래 관리실로 복귀" }, "menu-row/return");
  m.appendChild(move);
  m.appendChild(back);
  ctx.mark(1, hold);
  ctx.mark(2, move);
  ctx.mark(3, back);
  return box("VERTICAL", { name: "design", children: [m] });
});

unit("procedure/room-move/list", (ctx) => {
  const { c, list } = roomMoveCombo("room-move-list");
  const rooms = ["레이저실 3", "시술실 F", "A-룸2 (1/2)"];
  const opts = rooms.map((r, i) => inst2("ComboOption", { state: "default" }, { label: r }, `option-${i + 1}`));
  for (const o of opts) list.appendChild(o);
  ctx.mark(1, list);
  ctx.mark(2, opts[2]);
  return box("VERTICAL", { name: "design", children: [c] });
});

unit("procedure/room-move/list-empty", (ctx) => {
  const { c, list } = roomMoveCombo("room-move-list-empty");
  const empty = box("HORIZONTAL", {
    name: "empty-row", w: 200, h: 44, pt: 11, pb: 11, pl: 16, pr: 16, align: "CENTER",
    children: [text("빈 관리실 없음", [14, 400, 21], "gray/600", { name: "label" })],
  });
  list.appendChild(empty);
  empty.layoutAlign = "STRETCH";
  ctx.mark(1, empty);
  return box("VERTICAL", { name: "design", children: [c] });
});

unit("procedure/toast/room-full", (ctx) => {
  const t = inst2("Notify", { state: "default" }, { label: "그 관리실에 자리가 없습니다" }, "notify");
  ctx.mark(1, t);
  return box("VERTICAL", { name: "design", children: [t] });
});
