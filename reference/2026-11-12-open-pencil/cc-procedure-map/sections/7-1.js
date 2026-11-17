// 7-1 관리실별 상담실장 호출 — 화면 1: consultant-call(고도화 · 1차 범위 밖). 범위 밖 표시는 캡션이 한다
// 기획안 7-1: 「개별 관리실 화면에서만 「상담실장 호출」」 · 흐름 · 화면 구성 · 정책은 다음 스펙 → 버튼 하나만, 관리실 화면 조각(방 카드 제목 줄 · 고객 줄) 위에
// 조각 = 시안 RoomCard 제목 줄(.room-title 313 · 340: 여백 5 10 · 간격 10 · 최소 31 · crm/surface-head · 방 이름 12/500 gray/800) + 고객 줄(c1 저우위원 · 시술실 A)
// DIFF: 시안에 상담실장 호출 없음 · 버튼 자리(제목 줄 오른쪽)는 정해진 것이 아님 — 다음 스펙에서 정한다(기획안 L738)
// DIFF: 기획안 style outlined/gray/s ↔ Button 세트에 outlined-gray s 없음 → outlined-gray ss(28)
unit("procedure/consultant-call", (ctx) => {
  const title = grow(text("시술실 A", "caption-md-500", "gray/800", { name: "label" }));
  const call = inst2("Button", { kind: "outlined-gray", size: "ss" }, { label: "상담실장 호출" }, "button/consultant-call");
  const head = box("HORIZONTAL", { name: "room-title", h: 38, pl: 10, pr: 10, gap: 10, bg: "crm/surface-head", children: [inst("IconButton", { icon: "grip" }, {}, "drag-handle"), title, call] });
  title.textAutoResize = "HEIGHT";
  stretch(head);
  const cust = box("HORIZONTAL", {
    name: "customer-line", pt: 10, pb: 12, pl: 10, pr: 10, gap: 4,
    children: [icon("user-round-12", "black"), text("[TW] CHOU YU WEN", "caption-md-400", "black", { name: "label/name" }), text("저우위원", "caption-md-500", "gray/700", { name: "label/local" })],
  });
  stretch(cust);
  const frag = custom("room-fragment", box("VERTICAL", { w: 256, radius: 6, bg: "white", clip: true, children: [head, cust] }));
  shadows(frag, SHADOW_ROOM);
  ctx.mark(1, call);
  return frag;
});
