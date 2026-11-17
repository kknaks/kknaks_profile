// 3-2 호출 수락 — 화면 2
// DIFF: accepted = 기획안 아랫단 「{원장} 수락 완료 HH:MM」 · 윗단 「시작」 · 체크박스 없음(L471 · L518) ↔ 시안 ready 줄 「김도윤 원장 수락」 + 꺼진 체크박스. 문구는 기획안(「김도윤 원장 수락 완료 14:43」), 줄 모양 · 「시작」(xs)은 시안 ProcRow ready. 체크박스는 기획안대로 숨김
// DIFF: accepted 「시작」 크기 = 기획안 style solid/blue/ss ↔ 시안 줄 버튼 xs — 시안 인스턴스 그대로(xs)
// DIFF: reassign = 시안에 「담당 원장 바꾸기」 창 없음 → 시안 Popover(accept) 모양을 떼어 씀. 기획안은 원장 이름을 누르면 바로 반영(L472) → 검색 · 「선택됨」/「전체」 구역 라벨 · 발 버튼 숨김/뺌. 시안 제목 「수락할 원장」은 다른 용도라 쓰지 않고 제목 비움(기획안에 제목 없음)
// DIFF: reassign 원장 3명 = 시안 원장 데이터 · 보조 글 = 시안 doctorStatus 꼴(김도윤 = 시술실 A 시술 중 · 이서연 = 시술실 D 시술 중 · 박하준 = 비어 있음) · 꼬리표 숨김 · 지금 담당 원장 표시는 기획안에 없어 고른 줄(on) 없음

function docAvatarComp32(tone) {
  return findSet("Avatar").children.find((c) => c.name === `kind=doctor, tone=${tone}`);
}
function doctorOpt32(tone, short, full, sub, name) {
  const o = inst("PopOption", { kind: "doctor", state: "default" }, {}, name);
  if (tone !== "0") {
    const av = findIn(o, "avatar");
    try { if (av && av.swapComponent) av.swapComponent(docAvatarComp32(tone)); } catch (e) { /* 안쪽 바꾸기가 막히면 tone 0 그대로 */ }
  }
  setText(o, "label", short, 0);
  setText(o, "label", full, 1);
  setText(o, "label/sub", sub);
  const tag = findIn(o, "label/tag");
  if (tag) tag.visible = false;
  return o;
}

unit("procedure/treatment-line/accepted", (ctx) => {
  const head = inst("SelectAll", { state: "disabled" }, {}, "select-all");
  const headRow = box("HORIZONTAL", { name: "list-head", pl: 6, pr: 8, py: 4, children: [head] });
  const row = inst2("ProcRow", { status: "ready", state: "default" },
    { label: "울쎄라피 프라임 300 shot", "label/doctor": "김도윤 원장", "label/status": "수락 완료 14:43" }, "proc-row");
  hideIn(row, "checkbox");
  ctx.mark(1, findIn(row, "meta"));
  ctx.mark(2, findIn(row, "button"));
  return box("VERTICAL", { name: "design", w: 256, py: 4, bg: "white", children: [headRow, row] });
});

unit("procedure/doctor-list/reassign", (ctx) => {
  const d = detach(inst("Popover", { mode: "accept" }, {}, "popover"), "doctor-reassign");
  const head = d.children.find((n) => n.name === "head");
  setText(head, "label", "");                       // 제목 — 기획안에 없음(비움)
  for (const nm of ["search-row", "foot-line", "foot"]) { const n = d.children.find((x) => x.name === nm); if (n) n.visible = false; }
  const body = d.children.find((n) => n.name === "body");
  body.paddingTop = 6;
  for (const n of [...body.children]) n.remove();   // 구역 라벨 · 시안 줄 빼고 원장 줄만
  const rows = [
    doctorOpt32("0", "도윤", "김도윤 원장", "시술실 A 시술 중", "option/doctor-1"),
    doctorOpt32("1", "서연", "이서연 원장", "시술실 D 시술 중", "option/doctor-2"),
    doctorOpt32("2", "하준", "박하준 원장", "비어 있음", "option/doctor-3"),
  ];
  for (const o of rows) body.appendChild(o);
  ctx.mark(1, body);
  return box("VERTICAL", { name: "design", children: [d] });
});
