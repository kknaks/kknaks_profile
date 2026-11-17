// 6-1 관리실 기록 — 화면 4: room-log(창) · date-calendar(달력) · room-select(관리실 고르기) · room-group(관리실 묶음)
// 시안에 이 창은 없다. 틀 = 차트 모달(.cm-box 582 · r14 · 그림자 SHADOW_FLOAT) · 묶음 = 「시술 완료」 탭(renderDoneTab · doneRoomCard 1433–1457 · 방별 묶음 머리 InboxSectionHead)
// 샘플 = 시안 데이터(데모 시계 14:45 · DEMO_NOW_MIN 1017)
//   시술실 A: c1 저우위원 입실 13:30(IN_TIME) 체류 중 · o1 소프웨이브 200펄스 14:05–14:33 김도윤 원장 · 간호 차트 정하늘 간호사(1475) · o2 써마지 900샷 14:37 진행 중 김도윤 원장
//             HISTORY r1 다나카 미카 11:20–13:05(울쎄라피 · 간호 차트 정하늘 간호사 1478 · 리쥬란) · 왕이 09:30–11:10(써마지 FLX 600샷 · 모델링팩 원장 없음)
//   시술실 B: c2 히로세 유우리 입실 13:40 체류 중 · 시술 줄 모두 시작 전(o4 ready · o5 · o6 wait) → 「시작한 시술 없음」 · HISTORY r2 이토 켄타 10:10–11:40
//   묶음 안 고객 순서 = 기획안 6-1 정책 1(진행 중 시술 있는 고객 → 마지막 종료 시각 늦은 순) · 시술 줄 = 시작 시각 순
// DIFF: 시안 「시술 완료」 탭 = 귀가 대기로 나온 고객 카드(입실-귀가 · 귀가 배지 · 차트 아이콘) ↔ 기획안 관리실 기록 = 체류 구간(들어온 · 나간 시각 / 「체류 중」) + 시술 줄 2줄(시술 · 시작 · 종료 / 원장 · 간호관리 담당자) → 요소 · 문구는 기획안, 카드 모양(테두리 · 머리 면)은 시안
// DIFF: 결정 「입실 HH:MM 빼고 국적」 → 고객 줄에 국적. 시안 데이터에 국적 값이 없고 형식은 SPEC-000 OQ-02-1 미정 · 변환 금지(결정) → 자리표시 「{국적}」(리드 수정: 처음 판의 「대만」 · 「일본」은 [TW] · [JP] 를 바꾼 추정이라 뺌)
// DIFF: 「이전 날」 · 「다음 날」 = 시안 date-nav 꺾쇠(pc-chevron-left/right-20)인데 아이콘 세트에 없음 → 기획안 문구 글자 버튼(Button outlined-gray m-dialog). 「다음 날」 비활성 = 면 gray/200(.btn:disabled)
// DIFF: 「닫기」 기획안 style outlined/gray/l ↔ Button 세트에 outlined-gray l 없음 → outlined-gray m-dialog. 창 오른쪽 위 X(차트 모달 close-24)는 기획안에 없어 뺐다
// DIFF: room-group = 「묶음 하나 확대」 힌트지만 「시작한 시술 없음」 샘플(c2)은 시술실 B, 「진행 중」(o2)은 시술실 A 에만 있어 두 묶음을 나란히 둔다
// 비움: 창 제목(기획안에 창 제목 문구 없음 — 머리 줄에 날짜 · 관리실 고르기만)

const RL_DATE = "2026-10-26 (월)";
const RL_ROOMS = ["시술실 A", "시술실 B", "시술실 C", "시술실 D", "시술실 E", "레이저실 1", "레이저실 2", "레이저실 3", "시술실 F", "VIP실"]; // 시안 state.rooms 순서(= 관리실 등록 순서)
// [이름(한국어 발음), 국적, 들어온, 나간(null = 체류 중), [[시술, 시작, 종료(null = 진행 중), 원장, 간호관리 담당자]]]
const RL_GROUPS = [
  ["시술실 A", [
    ["저우위원", "{국적}", "13:30", null, [["소프웨이브 200펄스", "14:05", "14:33", "김도윤 원장", "정하늘 간호사"], ["써마지 900샷", "14:37", null, "김도윤 원장", null]]],
    ["다나카 미카", "{국적}", "11:20", "13:05", [["울쎄라피 프라임 300샷", "11:52", "12:30", "김도윤 원장", "정하늘 간호사"], ["리쥬란 힐러 2cc", "12:34", "12:58", "김도윤 원장", null]]],
    ["왕이", "{국적}", "09:30", "11:10", [["써마지 FLX 600샷", "10:02", "10:48", "김도윤 원장", null], ["모델링팩", "10:50", "11:05", null, null]]],
  ]],
  ["시술실 B", [
    ["히로세 유우리", "{국적}", "13:40", null, []],
    ["이토 켄타", "{국적}", "10:10", "11:40", [["슈링크 유니버스 300샷", "10:40", "11:12", "이서연 원장", null], ["보톡스 사각턱 50u", "11:15", "11:28", "이서연 원장", null]]],
  ]],
];

function rlBar() {
  const b = figma.createRectangle();
  b.name = "divider"; b.resize(1, 10); fill(b, "gray/300");
  return b;
}
// 시술 줄: 1줄 = 시술 이름 · 시작 – 종료(진행 중 배지) / 2줄 = 담당 원장 · 간호관리 담당자(둘 다 없으면 줄 없음)
function rlProcRow(p, m) {
  const [name, start, end, doctor, nurse] = p;
  const label = grow(text(name, "caption-md-500", "black", { name: "label/procedure" }));
  const time = box("HORIZONTAL", {
    name: "proc-time", gap: 4,
    children: [text(end ? `${start} – ${end}` : `${start} –`, "caption-md-400", "gray/700", { name: "label/time" }),
      end ? null : inst2("Badge", { kind: "solid", color: "primary" }, { label: "진행 중" }, "badge/progress")],
  });
  const line1 = box("HORIZONTAL", { name: "proc-line", gap: 8, children: [label, time] });
  stretch(line1); label.textAutoResize = "HEIGHT";
  const who = [doctor, nurse].filter(Boolean).join(" · ");
  const line2 = who ? text(who, "caption-md-400", "gray/700", { name: "label/staff" }) : null;
  const row = box("VERTICAL", { name: "proc-row", gap: 2, children: [line1, line2] });
  stretch(row);
  if (m) {
    if (!m.proc) m.proc = line1;
    if (line2 && !m.staff) m.staff = line2;
    if (!end && !m.progress) m.progress = findIn(time, "badge/progress");
  }
  return row;
}
// 고객 한 명 = 카드(시안 .crm-card: r6 · 테두리 gray/300 · 머리 crm/surface-head)
function rlCustomer(c, m) {
  const [name, nation, inAt, outAt, procs] = c;
  const nameBtn = text(name, "caption-md-600", "black", { name: "button/customer" }); // 고객 이름 = 누르면 그날 시술 차트(text/black/s)
  const meta = box("HORIZONTAL", {
    name: "customer-meta", gap: 4,
    children: [text(nation, "caption-md-400", "gray/700", { name: "label/nation" }), rlBar(),
      text(outAt ? `${inAt} – ${outAt}` : `${inAt} –`, "caption-md-400", "gray/700", { name: "label/stay" })],
  });
  const stay = outAt ? null : inst2("Badge", { kind: "solid", color: "primary" }, { label: "체류 중" }, "badge/stay");
  const head = box("HORIZONTAL", { name: "customer-head", pt: 6, pb: 6, pl: 8, pr: 8, gap: 6, bg: "crm/surface-head", children: [nameBtn, meta, stay] });
  stretch(head);
  const rows = procs.length
    ? procs.map((p) => rlProcRow(p, m))
    : [inst2("Badge", { kind: "solid", color: "gray" }, { label: "시작한 시술 없음" }, "badge/no-procedure")];
  const body = box("VERTICAL", { name: "customer-body", p: 8, gap: 6, children: rows });
  stretch(body);
  const card = box("VERTICAL", { name: "customer", p: 1, radius: 6, bg: "white", border: "gray/300", clip: true, children: [head, body] });
  stretch(card);
  shadows(card, SHADOW_CARD);
  if (m) {
    if (!m.name) m.name = nameBtn;
    if (!m.meta) m.meta = meta;
    if (stay && !m.stay) m.stay = stay;
    if (!procs.length && !m.none) m.none = rows[0];
  }
  return card;
}
// 관리실 묶음 = 묶음 머리(InboxSectionHead none · 접기 꺾쇠 숨김 — 기획안에 접기 없음) + 고객 카드
function rlGroup([room, customers], m, w) {
  const h = inst2("InboxSectionHead", { icon: "none" }, { label: room }, "group-head");
  hideIn(h, "icon/chevron");
  const g = box("VERTICAL", { name: "room-group", w, gap: 8, children: [h, ...customers.map((c) => rlCustomer(c, m))] });
  stretch(h);
  if (m && !m.title) m.title = findIn(h, "label");
  return g;
}

unit("procedure/room-log", (ctx) => {
  const prev = inst2("Button", { kind: "outlined-gray", size: "m-dialog" }, { label: "이전 날" }, "button/prev-day");
  const date = inst2("Button", { kind: "outlined-gray", size: "m-dialog" }, { label: RL_DATE }, "button/date");
  const next = inst2("Button", { kind: "outlined-gray", size: "m-dialog" }, { label: "다음 날" }, "button/next-day");
  fill(next, "gray/200"); stroke(next, "gray/200"); // 오늘이면 비활성(.btn:disabled)
  const nav = box("HORIZONTAL", { name: "date-nav", gap: 4, children: [prev, date, next] });
  const selLabel = grow(text("모든 관리실", "body-400", "black", { name: "label" }));
  const chev = icon("chevron-down-20c"); chev.name = "icon/chevron";
  const sel = custom("room-select-trigger", box("HORIZONTAL", { w: 160, h: 36, pl: 12, pr: 8, gap: 4, radius: 6, bg: "white", border: "gray/300", children: [selLabel, chev] }));
  selLabel.textAutoResize = "HEIGHT";
  const head = box("HORIZONTAL", { name: "head", p: 14, gap: 8, children: [nav, sel] });
  stretch(head);

  const m = {};
  const groups = RL_GROUPS.map((g) => rlGroup(g, m, 568));
  const body = box("VERTICAL", { name: "body", h: 664, pt: 4, pb: 16, pl: 16, pr: 16, gap: 16, clip: true, children: groups });
  stretch(body);
  const close = inst2("Button", { kind: "outlined-gray", size: "m-dialog" }, { label: "닫기" }, "button/close");
  const foot = box("HORIZONTAL", { name: "foot", pt: 8, pb: 8, pl: 16, pr: 16, justify: "MAX", children: [close] });
  stretch(foot);
  const modal = custom("room-log-modal", box("VERTICAL", { w: 600, h: 780, radius: 14, bg: "white", clip: true, children: [head, body, foot] }));
  shadows(modal, SHADOW_FLOAT);

  ctx.mark(1, date); ctx.mark(2, prev); ctx.mark(3, next); ctx.mark(4, sel); ctx.mark(5, groups[0]); ctx.mark(6, close);
  return modal;
});

unit("procedure/room-log/date-calendar", (ctx) => {
  // 세트 · 시안에 달력 없음 → 7열 날짜 격자. 2026년 10월(10-01 = 목) · 26일(오늘 · 고른 날) = primary
  const CELL_W = 40, CELL_H = 36;
  const cell = (str, o = {}) => {
    const kids = [];
    if (str && o.on) kids.push(box("HORIZONTAL", { name: "selected", w: 32, h: 32, radius: 16, bg: "primary/DEFAULT", justify: "CENTER", align: "CENTER", children: [text(str, "body-600", "white", { name: "label" })] }));
    else if (str) kids.push(text(str, o.typo || "body-400", o.color || "black", { name: "label" }));
    return box("HORIZONTAL", { name: str ? `day/${str}` : "day/blank", w: CELL_W, h: CELL_H, justify: "CENTER", align: "CENTER", children: kids });
  };
  const week = box("HORIZONTAL", { name: "weekdays", children: ["일", "월", "화", "수", "목", "금", "토"].map((d) => cell(d, { typo: "caption-md-500", color: "gray/700" })) });
  const rows = [];
  let sel = null;
  let day = 1 - 4; // 첫 줄 앞 칸 4개(일~수) 비움
  for (let r = 0; r < 5; r++) {
    const kids = [];
    for (let c = 0; c < 7; c++, day++) {
      const n = day >= 1 && day <= 31 ? String(day) : "";
      const k = cell(n, { on: day === 26 });
      if (day === 26) sel = k;
      kids.push(k);
    }
    rows.push(box("HORIZONTAL", { name: `week-${r + 1}`, children: kids }));
  }
  const title = text("2026년 10월", "heading-md-600", "black", { name: "label/month" });
  const cal = custom("calendar", box("VERTICAL", { w: 312, p: 16, gap: 8, radius: 12, bg: "white", children: [title, week, box("VERTICAL", { name: "days", children: rows })] }));
  shadows(cal, SHADOW_POPOVER);
  ctx.mark(1, sel);
  return cal;
});

unit("procedure/room-log/room-select", (ctx) => {
  // 시안 방 옮기기 목록(MoreMenu combo · ComboOption) 모양. 「모든 관리실」 = 처음 값(on) · 아래 관리실 이름(등록 순서) · 목록은 칸 안 스크롤
  const all = inst2("ComboOption", { state: "on" }, { label: "모든 관리실" }, "option/all");
  const opts = RL_ROOMS.map((r, i) => inst2("ComboOption", { state: "default" }, { label: r }, `option-${i + 1}`));
  const list = custom("room-select-list", box("VERTICAL", { w: 200, h: 320, radius: 8, bg: "white", clip: true, children: [all, ...opts] }));
  shadows(list, SHADOW_POPOVER);
  ctx.mark(1, all); ctx.mark(2, opts[0]);
  return list;
});

unit("procedure/room-log/room-group", (ctx) => {
  const m = {};
  const a = rlGroup(RL_GROUPS[0], m, 272);
  const b = rlGroup(RL_GROUPS[1], m, 272);
  const panel = box("HORIZONTAL", { name: "room-groups", w: 560, gap: 16, align: "MIN", children: [a, b] });
  ctx.mark(1, m.title); ctx.mark(2, m.name); ctx.mark(3, m.meta); ctx.mark(4, m.stay); ctx.mark(5, m.none);
  ctx.mark(6, m.proc); ctx.mark(7, m.staff); ctx.mark(8, m.progress);
  return panel;
});
