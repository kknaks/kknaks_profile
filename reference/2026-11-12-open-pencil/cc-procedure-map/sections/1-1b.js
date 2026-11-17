// 1-1b — 시술 줄 상태 · 고객 카드 변경 표시 · 원장 호출 칸 · 변경 이력(7 화면)
// DIFF: waiting — 시안 대기 줄 = 체크박스 + 「준비중」(버튼 없음) ↔ 기획안 L516 「대기」 글자 없이 체크박스 · 「시작」 · 결정 U1(담당의가 있으면 호출 없이 [시작]) → 기획안 · 결정대로 「준비중」 숨기고 「시작」(Button xs solid)
// DIFF: waiting — 「[이벤트]」 배지는 시안에 없음 → Badge solid primary 인스턴스에 기획안 글자
// DIFF: not-proceeding — 시안에 「시술 미진행」 줄 없음 → ProcRow called 를 떼어(체크박스 off = 비활성) 원장 · 시간 · 버튼 숨기고 아랫단에 「시술 미진행」, 글자 gray/600
// DIFF: done — 완료 표시는 시안 st-done-gray 아이콘(기획안 L505 「체크된 체크박스」) → 모양은 시안. 시안 시간 칸 「28분」 ↔ 기획안 「{원장} · n분」 → 「김도윤 원장 · 28분」. 시안 완료 줄에 「⋯」 없음 → IconButton more 더함
// DIFF: line-changed — 「변경」 · 「변경 n건」은 시안에 없음. 세트에 노랑(warning) Badge · filled yellow Button 이 없어 Badge solid · Button xs 를 떼어 yellow/100 면 + yellow 글자로
// DIFF: new-lines — 시안에 「새 시술 줄」 구분 없음 → 완료 줄 아래 구분선 + ProcRow wait 를 떼어 「준비중」 숨기고 「시작」. 줄 이름 = 기획안 예시 「아쿠아필 2회」
// DIFF: call-bar — 시안 「n개 호출」 한 버튼 + 고르기 팝오버(결정 U2) ↔ 기획안 3-1 「전체 호출 · n개」 · 「지정 호출 · n개」 + 「지정 원장 · {원장}」 → 기획안 문구 · 버튼 둘. n = 시안 selection 카드에 체크된 줄 수 1(브리프 예시 2개 → 카드 체크 수와 맞춰 1개)
// DIFF: call-bar — 「지정 호출」 outlined/blue/s 는 세트에 없음 → Button solid s 를 떼어 흰 면 + primary 테두리 · 글자
// DIFF: RoomCard 고객 줄 「입실 13:30」 → 결정 「입실을 빼고 국적」. 국적 형식(코드/이름)은 SPEC-000 OQ-02-1 열림 → 자리표시 「{국적}」
// change-history — 기획안에 화면 정의 없음(확인 안 됨) → 빈 자리 프레임(custom/placeholder · 점선 red) + 「변경 이력」만

function b1_rule(name) {
  const r = figma.createRectangle();
  r.name = name; r.resize(256, 1); fill(r, "gray/200");
  return stretch(r);
}
function b1_listHead(state = "default") {
  return box("HORIZONTAL", { name: "list-head", pt: 8, pl: 8, pr: 8, gap: 8, children: [inst("SelectAll", { state }, {}, "select-all")] });
}
function b1_slice(children) {
  const f = box("VERTICAL", { name: "proc-list-slice", w: 256, pb: 4, gap: 4, radius: 6, bg: "white", clip: true, children });
  shadows(f, SHADOW_ROOM);
  for (const c of f.children) if (c.type !== "TEXT") stretch(c);
  return f;
}
// 결정: 「입실 HH:MM」 → 국적(형식 미정 → 자리표시)
function b1_nat(card) { setText(card, "label/in", "{국적}"); }
// 이름 줄에 배지 붙이기: name-meta = [이름, meta] → [name-line(이름 + 배지), meta]
function b1_nameWithBadge(rowFrame, badge, nameGrow) {
  const meta = findIn(rowFrame, "name-meta");
  const nameT = meta.children.find((c) => c.type === "TEXT" && c.name === "label");
  const m = findIn(meta, "meta");
  const line = box("HORIZONTAL", { name: "name-line", gap: 4, children: badge.first ? [badge.node, nameT] : [nameT, badge.node] });
  meta.appendChild(line);
  stretch(line);
  if (m) meta.appendChild(m);
  if (nameGrow) { grow(nameT); nameT.textAutoResize = "HEIGHT"; }
  return { line, nameT };
}

unit("procedure/treatment-line/waiting", (ctx) => {
  const row = detach(inst("ProcRow", { status: "wait", state: "default" }, {}, "proc-row"), "proc-row-waiting");
  setText(row, "label", "써마지 FLX 300shot (얼전, 이마포함)");
  const ev = inst2("Badge", { kind: "solid", color: "primary" }, { label: "[이벤트]" }, "badge-event");
  const { nameT } = b1_nameWithBadge(row, { node: ev, first: true }, true);
  hideIn(row, "meta");
  const start = inst2("Button", { kind: "solid", size: "xs", state: "default" }, { label: "시작" }, "button-start");
  row.appendChild(start);
  ctx.mark(1, findIn(row, "checkbox"));
  ctx.mark(2, ev);
  ctx.mark(3, nameT);
  ctx.mark(4, start);
  return b1_slice([b1_listHead("default"), row]);
});

unit("procedure/treatment-line/not-proceeding", (ctx) => {
  const row = detach(inst("ProcRow", { status: "called", state: "default" }, {}, "proc-row"), "proc-row-not-proceeding");
  hideIn(row, "label/doctor");
  hideIn(row, "proc-time");
  hideIn(row, "button");
  const st = setText(row, "label/status", "시술 미진행");
  fill(st, "gray/600");
  fill(findIn(row, "label"), "gray/600");
  ctx.mark(1, row);
  return b1_slice([b1_listHead("disabled"), row]);
});

unit("procedure/treatment-line/done", (ctx) => {
  const prog = inst("ProcRow", { status: "progress", state: "default" }, {}, "proc-row");
  const row = detach(inst("ProcRow", { status: "done", state: "default" }, {}, "proc-row"), "proc-row-done");
  const t = setText(row, "label/time", "김도윤 원장 · 28분");
  const more = inst("IconButton", { icon: "more" }, {}, "more");
  row.appendChild(more);
  ctx.mark(1, findIn(row, "icon/status"));
  ctx.mark(2, t);
  ctx.mark(3, more);
  return b1_slice([b1_listHead("disabled"), prog, b1_rule("divider-done"), row]);
});

unit("procedure/customer-card/line-changed", (ctx) => {
  const card = detach(inst("RoomCard", { state: "default" }, {}, "room-card"), "room-card-line-changed");
  b1_nat(card);
  // 진행 중 줄(써마지 900샷)에 「변경」
  const row = detach(findIn(card, "proc-row", 0), "proc-row-changed");
  const chip = detach(inst2("Badge", { kind: "solid", color: "primary" }, { label: "변경" }, "badge"), "badge-warning");
  fill(chip, "yellow/100");
  fill(findIn(chip, "label"), "yellow/DEFAULT");
  b1_nameWithBadge(row, { node: chip, first: false }, false);
  // 카드 머리 「변경 1건」
  const cnt = detach(inst2("Button", { kind: "solid", size: "xs", state: "default" }, { label: "변경 1건" }, "button"), "button-change-count");
  fill(cnt, "yellow/100");
  fill(findIn(cnt, "label"), "yellow/DEFAULT");
  findIn(card, "title-wrap").appendChild(cnt);
  ctx.mark(1, chip);
  ctx.mark(2, cnt);
  return card;
});

unit("procedure/customer-card/new-lines", (ctx) => {
  const card = detach(inst("RoomCard", { state: "default" }, {}, "room-card"), "room-card-new-lines");
  b1_nat(card);
  const row = detach(inst("ProcRow", { status: "wait", state: "default" }, {}, "proc-row"), "proc-row-new");
  setText(row, "label", "아쿠아필 2회");
  hideIn(row, "meta");
  const start = inst2("Button", { kind: "solid", size: "xs", state: "default" }, { label: "시작" }, "button-start");
  row.appendChild(start);
  const div = b1_rule("divider-new");
  const lists = findIn(card, "proc-lists");
  lists.appendChild(div);
  const list = box("VERTICAL", { name: "proc-list-new", w: 256, pt: 4, children: [row] });
  lists.appendChild(list);
  stretch(list);
  ctx.mark(1, div);
  ctx.mark(2, start);
  return card;
});

unit("procedure/customer-card/call-bar", (ctx) => {
  const card = detach(inst("RoomCard", { state: "selection" }, {}, "room-card"), "room-card-call-bar");
  b1_nat(card);
  const call = findIn(card, "room-call");
  for (const c of call.children) c.visible = false; // 시안 「1개 호출」 한 버튼
  const doc = inst2("Badge", { kind: "solid", color: "primary" }, { label: "지정 원장 · 김도윤 원장" }, "badge-pick-doctor");
  const all = inst2("Button", { kind: "solid", size: "s", state: "default" }, { label: "전체 호출 · 1개" }, "button-call-all");
  const pick = detach(inst2("Button", { kind: "solid", size: "s", state: "default" }, { label: "지정 호출 · 1개" }, "button"), "button-outlined-blue");
  fill(pick, "white");
  stroke(pick, "primary/DEFAULT", 1);
  fill(findIn(pick, "label"), "primary/DEFAULT");
  const btns = box("HORIZONTAL", { name: "call-buttons", gap: 6, children: [all, pick] });
  grow(all); grow(pick);
  const inner = box("VERTICAL", { name: "call-bar", gap: 6, children: [doc, btns] });
  call.appendChild(inner);
  grow(inner); stretch(btns);
  call.resize(256, 95);
  call.y = 448 - 95;
  ctx.mark(1, findIn(card, "select-all"));
  ctx.mark(2, doc);
  ctx.mark(3, all);
  ctx.mark(4, pick);
  return card;
});

unit("procedure/chart/change-history", (ctx) => {
  const f = box("VERTICAL", {
    name: "placeholder", w: ctx.w, h: ctx.h, radius: 8, bg: "white", border: "red/DEFAULT",
    justify: "CENTER", align: "CENTER",
    children: [text("변경 이력", "heading-sm-500", "gray/700", { name: "label" })],
  });
  f.dashPattern = [4, 4];
  return custom("placeholder", f);
});
