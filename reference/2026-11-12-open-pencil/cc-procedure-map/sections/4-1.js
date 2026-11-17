// 4-1 시술 상태 변경 — 화면 5
// DIFF: in-progress 아랫단 = 기획안 「{원장} · 진행 mm:ss」(→ 「김도윤 원장 · 진행 08:12」) ↔ 시안 「김도윤 원장 진행중」 + 시계 칸 「8분」 — 문구는 기획안, 시계 칸(proc-time)은 숨김. 줄 모양 · 「종료」 · 「⋯」는 시안 ProcRow progress/menu
// DIFF: start-pick = 시안에 「전체 호출 중 시작 → 원장 고르기」 창 없음 → 시안 Popover(accept) 모양을 떼어 씀. 기획안에 제목 · 검색 · 「선택됨」 · 발 버튼 없음(고르면 바로 시작) → 제목 비움 · 검색 · 구역 라벨 · 발 숨김/뺌. 원장 3명(시안 원장 데이터) · 보조 글 = 시안 doctorStatus 꼴
// DIFF: more-menu = 시안은 한 줄 메뉴(진행중 「시작 취소」 / 완료 「완료 취소」 중 하나) — 맵에서는 두 경우를 위아래로 나란히(MoreMenu menu × 2)
// DIFF: cancel-start · cancel-complete = 시안 ConfirmDialog(왼 outlined-gray · 오 solid) 순서대로 왼 「닫기」 · 오 「시작 취소」/「완료 취소」(기획안 L545-547). 본문(label/body)은 기획안에 없어 숨김

unit("procedure/treatment-line/in-progress", (ctx) => {
  const head = inst("SelectAll", { state: "disabled" }, {}, "select-all");
  const headRow = box("HORIZONTAL", { name: "list-head", pl: 6, pr: 8, py: 4, children: [head] });
  const row = inst2("ProcRow", { status: "progress", state: "menu" },
    { label: "써마지 900샷", "label/doctor": "김도윤 원장", "label/status": " · 진행 08:12" }, "proc-row");
  hideIn(row, "proc-time");
  ctx.mark(1, findIn(row, "label/status"));
  ctx.mark(2, findIn(row, "button"));
  ctx.mark(3, findIn(row, "more"));
  ctx.mark(4, findIn(row, "label/doctor"));
  return box("VERTICAL", { name: "design", w: 256, py: 4, bg: "white", children: [headRow, row] });
});

unit("procedure/doctor-list/start-pick", (ctx) => {
  const d = detach(inst("Popover", { mode: "accept" }, {}, "popover"), "doctor-start-pick");
  const head = d.children.find((n) => n.name === "head");
  setText(head, "label", "");                       // 제목 — 기획안에 없음(비움)
  for (const nm of ["search-row", "foot-line", "foot"]) { const n = d.children.find((x) => x.name === nm); if (n) n.visible = false; }
  const body = d.children.find((n) => n.name === "body");
  for (const n of [...body.children]) if (n.name !== "option/doctor") n.remove();   // 「선택됨」 · 「전체」 라벨 · 고른 줄 빼기
  const avatarComp = (tone) => findSet("Avatar").children.find((c) => c.name === `kind=doctor, tone=${tone}`);
  const doctor = (tone, short, full, sub) => {
    const o = inst("PopOption", { kind: "doctor", state: "default" }, {}, `option/doctor-${tone}`);
    const av = findIn(o, "avatar");
    try { if (av && av.swapComponent) av.swapComponent(avatarComp(tone)); } catch (e) { /* 안쪽 바꾸기가 막히면 tone 0 그대로 */ }
    setText(o, "label", short, 0); setText(o, "label", full, 1); setText(o, "label/sub", sub);
    return o;
  };
  body.appendChild(doctor("1", "서연", "이서연 원장", "시술실 D 시술 중"));
  body.appendChild(doctor("2", "하준", "박하준 원장", "비어 있음"));
  ctx.mark(1, body);
  return box("VERTICAL", { name: "design", children: [d] });
});

unit("procedure/treatment-line/more-menu", (ctx) => {
  const a = inst2("MoreMenu", { kind: "menu" }, { label: "시작 취소" }, "more-menu/in-progress");
  const b = inst2("MoreMenu", { kind: "menu" }, { label: "완료 취소" }, "more-menu/done");
  ctx.mark(1, findIn(a, "menu-row"));
  ctx.mark(2, findIn(b, "menu-row"));
  return box("VERTICAL", { name: "design", gap: 12, children: [a, b] });
});

function cancelConfirm(ctx, title, okLabel) {
  const dlg = inst("ConfirmDialog", { state: "default" }, {}, "confirm-dialog");
  setText(dlg, "label", title, 0);
  hideIn(dlg, "body");
  const close = findIn(dlg, "cancel"), ok = findIn(dlg, "confirm");
  setText(close, "label", "닫기");
  setText(ok, "label", okLabel);
  ctx.mark(1, findIn(dlg, "label"));
  ctx.mark(2, close);
  ctx.mark(3, ok);
  return box("VERTICAL", { name: "design", children: [dlg] });
}
unit("procedure/confirm/cancel-start", (ctx) => cancelConfirm(ctx, "써마지 900샷 시작을 취소할까요?", "시작 취소"));
unit("procedure/confirm/cancel-complete", (ctx) => cancelConfirm(ctx, "소프웨이브 200펄스 완료를 취소할까요?", "완료 취소"));
