// 4-2 시술 차트 — 화면 9개(procedure/chart · order-memo · doctor-chart · nursing-chart · author-picker · apply-all-confirm · discard-confirm · conflict-notice · past-visits)
// 출처: 기획안 L570-631 · 시안 chartModalHtml 1272-1292 · .cm-* 582-613 · .combo 682 · 데이터 c1/o1/o2 808·833-834 · NURSE_NAME 1459
//
// DIFF: 시안 차트 모달 = 「간호 관리 차트 / 의사 차트」 탭 + 시술마다 글 칸 하나 ↔ 기획안 = 시술 줄마다 「의사 차트」 · 「간호관리차트」 두 칸 → 기획안(탭 없음 · 줄마다 두 패널 나란히)
// DIFF: 시안 모달 폭 410 ↔ 기획안 영역이 많아 560 으로 넓힘(모양 r14 · 머리 18/500 · 섹션 여백 12 16 · Textarea · Button 은 시안)
// DIFF: 시안 발 「Ctrl + Enter」 + 「저장」 ↔ 기획안 「고객 차트」 · 「닫기」 · 「저장」 → 기획안(「Ctrl + Enter」 뺌)
// DIFF: 시안 글 칸 placeholder 「내용을 입력해 주세요」 ↔ 기획안 「차트 칸」 표 L605-606 예시 글 → 기획안
// DIFF: 시안 섹션 메타(연필 · 쓴 사람 · 시각 수정|작성) ↔ 기획안 화면 구성에 없음(저장 기록은 정책 12) → 뺌
// DIFF: 시안 제목 「CHOU YU WEN 저우위원」(이름 + 현지 이름) = 기획안 「한국어 발음」 자리로 보고 그대로 · 차트 번호 · 「주의 · 불만」은 제목 아래 줄(custom/customer-info)
// DIFF: 확인 창 시안 본문 「쓴 내용은 사라져요.」 + 「취소」/「닫기」 ↔ 기획안 「계속 쓰기」 · 「버리고 닫기」(본문 문구 없음) → 기획안(본문 숨김)
// DIFF: 「닫기」 기획안 스타일 outlined/gray/l ↔ 세트에 outlined-gray l 없음 → Button outlined-gray m-dialog(36 높이 · 「저장」 l 44 와 높이 다름)
// DIFF: 텍스트 버튼(「고객 차트」 · 「작성자 추가」 · 「칸 지우기」 · 「오더 메모 접기」) 세트에 없음 → custom/text-button(시안 .link-to 모양: 여백 2 4 · r4 · 500)
// DIFF: 담당자 고르기 = 세트에 콤보 박스 없음 → custom/select(시안 .combo 36 · 여백 0 16 · 테두리 gray/300 · r6 · chevron) · 값 비움(목록 원천 미정)
// DIFF: 「다른 직원이 먼저 저장한 줄은 저장하지 않았습니다」 배너 세트 없음 → custom/conflict-banner(yellow/100 면 · yellow/300 선 · warn-fill)
// DIFF: 작성자 목록 = Popover/MoreMenu 대신 custom/author-picker(시안 .more-pop.is-combo 모양 · ComboOption 인스턴스 · 발 버튼 없음 — 이름을 고르면 바로 칸이 생김)

const W_MODAL = 560;
const IW = W_MODAL - 32; // 섹션 여백 16 양쪽
const PW = (IW - 8) / 2; // 줄마다 두 패널 나란히(260)
const TA_H = 80;
const CUSTOMER_TITLE = "CHOU YU WEN 저우위원";
const ORDER_MEMO = "**500만원 이상\nOUT TIME : x"; // 시안 RoomCard label/memo
const PH_DOCTOR = "샷 수 · 레벨 · 제품 · 용량 / 고객 반응 / 설명한 내용"; // 기획안 L605
const PH_NURSE = "한 일(세안 · 마취크림 30분) / 고객 반응 · 설명한 내용"; // 기획안 L606
const NURSE = "정하늘 간호사"; // 시안 NURSE_NAME(가짜 이름)
const PROCS = [
  ["소프웨이브 200펄스", "시술실 A", "김도윤 원장"],
  ["써마지 900샷", "시술실 A", "김도윤 원장"],
];

function spacer() {
  const s = box("HORIZONTAL", { name: "spacer", h: 1 });
  s.layoutGrow = 1;
  return s;
}
function hline(name, w) {
  const r = figma.createRectangle();
  r.name = name; r.resize(w, 1); fill(r, "gray/200");
  return r;
}
// 텍스트 버튼: s = 14/500 · ss = 12/500 · blue = primary · gray = gray/700
function textBtn(str, size, tone) {
  const t = text(str, size === "s" ? [14, 500, 18] : [12, 500, 16], tone === "blue" ? "primary/DEFAULT" : "gray/700", { name: "label" });
  return custom("text-button", box("HORIZONTAL", { name: "text-button", pt: 2, pb: 2, pl: 4, pr: 4, radius: 4, children: [t] }));
}
// 콤보(시안 .combo) — 값 비움
function select() {
  const val = box("HORIZONTAL", { name: "value-empty", h: 21 });
  val.layoutGrow = 1;
  return custom("select", box("HORIZONTAL", { name: "select", h: 36, pl: 16, pr: 16, gap: 16, radius: 6, bg: "white", border: "gray/300", children: [val, icon("chevron-down-20c", "gray/600")] }));
}
// 표: cols = [[머리 글, 폭 비율]] · rows = [[칸 글 | null]]
function table(name, W, cols, rows) {
  const ws = cols.map((c) => Math.floor(W * c[1]));
  const row = (cells, head) => box("HORIZONTAL", {
    name: head ? "row-head" : "row", h: 26, bg: head ? "crm/surface-head" : undefined,
    children: cells.map((v, i) => box("HORIZONTAL", {
      name: `cell-${i + 1}`, w: ws[i], h: 26, pl: 8, pr: 8,
      children: v === null || v === undefined ? [] : [text(v, head ? "caption-md-500" : "caption-md-400", head ? "gray/700" : "black", { name: "label" })],
    })),
  });
  const kids = [row(cols.map((c) => c[0]), true)];
  for (const r of rows) { kids.push(hline("row-line", W)); kids.push(row(r, false)); }
  return custom(name, box("VERTICAL", { name, w: W, radius: 6, border: "gray/200", clip: true, children: kids }));
}
function section(name, W, children, gap = 8) {
  return box("VERTICAL", { name, w: W, pt: 12, pb: 12, pl: 16, pr: 16, gap, children });
}
function textarea(w, placeholder) {
  const ta = inst2("Textarea", { state: "default" }, { label: placeholder }, "textarea");
  ta.resize(w, TA_H);
  return ta;
}

// ── 영역 ───────────────────────────────
function customerInfo(W) {
  const bar = figma.createRectangle();
  bar.name = "info-bar"; bar.resize(1, 10); fill(bar, "gray/300");
  return custom("customer-info", box("HORIZONTAL", {
    name: "customer-info", w: W, pl: 16, pr: 16, pb: 8, gap: 8,
    children: [
      text("{차트 번호}", "caption-md-400", "gray/700", { name: "label/chart-no" }),
      bar,
      text("주의 · 불만", "caption-md-500", "red/DEFAULT", { name: "label/caution-title" }),
      text("{주의 · 불만}", "caption-md-400", "black", { name: "label/caution" }),
    ],
  }));
}
function orderMemo(W) {
  const iw = W - 32;
  const title = text("오더 메모", [14, 500, 21], "black", { name: "label/title" });
  const time = box("HORIZONTAL", {
    name: "edited-at", gap: 4,
    children: [text("마지막 고친 시각", "caption-md-400", "gray/700", { name: "label" }), text("HH:MM", "caption-md-400", "gray/700", { name: "label/time" })],
  });
  const fold = textBtn("오더 메모 접기", "ss", "gray");
  const head = box("HORIZONTAL", { name: "order-memo-head", w: iw, gap: 8, children: [title, time, spacer(), fold] });
  const body = box("VERTICAL", { name: "order-memo-body", w: iw, p: 10, radius: 8, bg: "gray/100", children: [text(ORDER_MEMO, "caption-md-400-lh18", "black", { name: "label/memo", width: iw - 20 })] });
  const node = custom("order-memo", section("order-memo", W, [head, body]));
  return { node, title, time, fold };
}
function procTable(W) {
  const t = table("proc-table", W - 32, [["시술 이름", 0.44], ["진행한 관리실", 0.28], ["담당 원장", 0.28]], PROCS);
  return { node: section("proc-lines", W, [t]), table: t };
}
function anesRoom(W) {
  const half = (W - 32 - 8) / 2;
  const anes = table("anesthesia-table", half, [["마취 회차", 0.3], ["시작 시각", 0.35], ["전체 시간", 0.35]], [["1", "HH:MM", "21분"]]);
  const rooms = table("room-log-table", half, [["관리실", 0.34], ["들어온 시각", 0.33], ["나간 시각", 0.33]], [["시술실 A", "13:30", null]]);
  const row = box("HORIZONTAL", { name: "anesthesia-room-log", gap: 8, align: "MIN", children: [anes, rooms] });
  return { node: section("anesthesia-room", W, [row]), row };
}
function doctorPanel(pw) {
  const iw = pw - 24;
  const title = text("의사 차트", [14, 500, 21], "black", { name: "label/title" });
  const apply = inst2("Button", { kind: "outlined-gray", size: "ss", state: "default" }, { label: "전체 시술에 내용 적용" }, "apply-all");
  const head = box("HORIZONTAL", { name: "doctor-chart-head", w: iw, gap: 8, children: [title, spacer(), apply] });
  const sel = select();
  sel.layoutGrow = 1;
  const who = box("HORIZONTAL", { name: "assignee", w: iw, gap: 8, children: [text("담당자", "caption-md-400", "gray/700", { name: "label/assignee" }), sel] });
  const ta = textarea(iw, PH_DOCTOR);
  const node = custom("doctor-chart", box("VERTICAL", { name: "doctor-chart", w: pw, p: 12, gap: 8, radius: 8, bg: "white", border: "gray/200", children: [head, who, ta] }));
  return { node, title, sel, ta, apply };
}
function nursingPanel(pw, withStaff) {
  const iw = pw - 24;
  const title = text("간호관리차트", [14, 500, 21], "black", { name: "label/title" });
  const add = textBtn("작성자 추가", "s", "blue");
  const head = box("HORIZONTAL", { name: "nursing-chart-head", w: iw, h: 28, gap: 8, children: [title, spacer(), add] });
  const kids = [head];
  const r = { title, add };
  if (withStaff) {
    r.staff = text(NURSE, "caption-md-500", "black", { name: "label/staff" });
    r.clear = textBtn("칸 지우기", "ss", "gray");
    const nameRow = box("HORIZONTAL", { name: "staff-head", w: iw, h: 24, gap: 8, children: [r.staff, spacer(), r.clear] });
    r.ta = textarea(iw, PH_NURSE);
    r.apply = inst2("Button", { kind: "outlined-gray", size: "ss", state: "default" }, { label: "전체 시술에 내용 적용" }, "apply-all");
    const act = box("HORIZONTAL", { name: "staff-actions", w: iw, justify: "MAX", children: [r.apply] });
    kids.push(box("VERTICAL", { name: "staff-entry", w: iw, gap: 4, children: [nameRow, r.ta, act] }));
  }
  r.node = custom("nursing-chart", box("VERTICAL", { name: "nursing-chart", w: pw, p: 12, gap: 8, radius: 8, bg: "white", border: "gray/200", children: kids }));
  return r;
}
function pastVisits(W) {
  const iw = W - 32;
  const title = text("지난 방문 기록", [14, 500, 21], "black", { name: "label/title" });
  const cc = table("past-visits-cc", iw, [["날짜", 0.18], ["시술", 0.3], ["의사 차트", 0.26], ["간호관리차트", 0.26]], [["{날짜}", "{시술}", "{의사 차트}", "{간호관리차트}"]]);
  const kos = table("past-visits-kos", iw, [["날짜", 0.18], ["시술", 0.52], ["원장", 0.3]], [["{날짜}", "{시술}", "{원장}"]]);
  const node = custom("past-visits", section("past-visits", W, [title, cc, kos]));
  return { node, cc, kos };
}
function framed(W, children, name) {
  return box("VERTICAL", { name, w: W, radius: 14, bg: "white", border: "gray/200", clip: true, children });
}

// ── 화면 ───────────────────────────────
unit("procedure/chart", (ctx) => {
  const cm = detach(inst("ChartModal", { state: "default" }, {}, "chart-modal"), "chart-modal");
  findIn(cm, "tabs").remove();
  findIn(cm, "body").remove();
  const foot = findIn(cm, "foot");
  findIn(foot, "shortcut").remove();
  const save = findIn(foot, "save");
  const custBtn = textBtn("고객 차트", "s", "blue");
  const close = inst2("Button", { kind: "outlined-gray", size: "m-dialog", state: "default" }, { label: "닫기" }, "close-modal");
  foot.insertChild(0, custBtn);
  foot.insertChild(1, spacer());
  foot.insertChild(2, close);
  cm.resize(W_MODAL, cm.height);
  cm.primaryAxisSizingMode = "AUTO";
  setText(cm, "label", CUSTOMER_TITLE, 0);

  const info = customerInfo(W_MODAL);
  const memo = orderMemo(W_MODAL);
  const procs = procTable(W_MODAL);
  const anes = anesRoom(W_MODAL);
  // 시술 줄마다 「의사 차트」 · 「간호관리차트」
  const blocks = [];
  const first = {};
  PROCS.forEach(([name], i) => {
    const d = doctorPanel(PW);
    const n = nursingPanel(PW, i === 0);
    if (i === 0) { first.d = d; first.n = n; }
    blocks.push(box("VERTICAL", {
      name: `proc-chart-${i + 1}`, w: IW, gap: 8,
      children: [text(name, [14, 500, 21], "black", { name: "label/procedure" }), box("HORIZONTAL", { name: "charts", w: IW, gap: 8, align: "MIN", children: [d.node, n.node] })],
    }));
  });
  const charts = section("proc-charts", W_MODAL, blocks, 12);
  const past = pastVisits(W_MODAL);
  for (const s of [info, memo.node, procs.node, anes.node, charts, past.node]) cm.insertChild(cm.children.length - 1, s);

  ctx.mark(1, info);
  ctx.mark(2, memo.node);
  ctx.mark(3, procs.table);
  ctx.mark(4, anes.row);
  ctx.mark(5, first.d.node);
  ctx.mark(6, first.n.node);
  ctx.mark(7, past.node);
  ctx.mark(8, custBtn);
  ctx.mark(9, close);
  ctx.mark(10, save);
  return cm;
});

unit("procedure/chart/order-memo", (ctx) => {
  const m = orderMemo(ctx.w);
  ctx.mark(1, m.title);
  ctx.mark(2, m.time);
  ctx.mark(3, m.fold);
  return framed(ctx.w, [m.node], "design");
});

unit("procedure/chart/doctor-chart", (ctx) => {
  const d = doctorPanel(IW);
  const sec = section("proc-chart", ctx.w, [text(PROCS[0][0], [14, 500, 21], "black", { name: "label/procedure" }), d.node]);
  ctx.mark(1, d.title);
  ctx.mark(2, d.sel);
  ctx.mark(3, d.ta);
  ctx.mark(4, d.apply);
  return framed(ctx.w, [sec], "design");
});

unit("procedure/chart/nursing-chart", (ctx) => {
  const n = nursingPanel(IW, true);
  const sec = section("proc-chart", ctx.w, [text(PROCS[0][0], [14, 500, 21], "black", { name: "label/procedure" }), n.node]);
  ctx.mark(1, n.title);
  ctx.mark(2, n.add);
  ctx.mark(3, n.staff);
  ctx.mark(4, n.ta);
  ctx.mark(5, n.apply);
  ctx.mark(6, n.clear);
  return framed(ctx.w, [sec], "design");
});

unit("procedure/chart/author-picker", (ctx) => {
  // 이름 목록: 시안 가짜 이름 하나 + 나머지는 자리표시(이름을 지어내지 않음)
  const names = [NURSE, "{직원}", "{직원}", "{직원}", "{직원}"];
  const opts = names.map((s, i) => { const o = inst2("ComboOption", { state: "default" }, { label: s }, `option-${i + 1}`); o.layoutAlign = "STRETCH"; return o; });
  const list = box("VERTICAL", { name: "staff-list", w: 240, children: opts });
  const pop = custom("author-picker", box("VERTICAL", { name: "author-picker", w: 240, radius: 8, bg: "white", clip: true, children: [list] }));
  shadows(pop, SHADOW_POPOVER);
  ctx.mark(1, list);
  return pop;
});

unit("procedure/chart/apply-all-confirm", (ctx) => {
  // 제목 · 버튼 문구 기획안에 없음 → 비움(open-question). 본문 = 적용 수 · 제외 수 자리(기획안 L617)
  const dlg = inst("ConfirmDialog", { state: "default" }, {}, "apply-all-confirm");
  setText(dlg, "label", "", 0);
  setText(dlg, "label/body", "{적용 수} · {제외 수}");
  setText(findIn(dlg, "cancel"), "label", "");
  setText(findIn(dlg, "confirm"), "label", "");
  ctx.mark(1, findIn(dlg, "label/body"));
  return dlg;
});

unit("procedure/chart/discard-confirm", (ctx) => {
  const dlg = inst("ConfirmDialog", { state: "default" }, {}, "discard-confirm");
  setText(dlg, "label", "저장하지 않고 닫을까요?", 0);
  hideIn(dlg, "body"); // 기획안에 본문 문구 없음(시안 「쓴 내용은 사라져요.」)
  const keep = findIn(dlg, "cancel"), discard = findIn(dlg, "confirm");
  setText(keep, "label", "계속 쓰기");
  setText(discard, "label", "버리고 닫기");
  ctx.mark(1, findIn(dlg, "label"));
  ctx.mark(2, keep);
  ctx.mark(3, discard);
  return dlg;
});

unit("procedure/chart/conflict-notice", (ctx) => {
  const band = custom("conflict-banner", box("HORIZONTAL", {
    name: "conflict-banner", w: ctx.w - 32, pt: 12, pb: 12, pl: 16, pr: 16, gap: 8, radius: 8, bg: "yellow/100", border: "yellow/300",
    children: [icon("warn-fill", "yellow/DEFAULT"), text("다른 직원이 먼저 저장한 줄은 저장하지 않았습니다", [14, 500, 21], "black", { name: "label" })],
  }));
  ctx.mark(1, band);
  return framed(ctx.w, [section("chart-top", ctx.w, [band])], "design");
});

unit("procedure/chart/past-visits", (ctx) => {
  const p = pastVisits(ctx.w);
  ctx.mark(1, p.cc);
  ctx.mark(2, p.kos);
  return framed(ctx.w, [p.node], "design");
});
