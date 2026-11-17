// RoomCard — 시안 `.room` 309–310 · 343–356 · 466 · 488 · 499–505 · `.room-title` 313–314 · 340 · 377–382 · 409 · 490 · `.customer` 297–302 · 411 · 536–537 · 506
//            `.memo3`/`.memo-box` 416–417 · 538–541 · 568–569 · `.proc-lists`/`.proc-list` 418–419 · 543–546 · `.list-head` 452 · 546 · `.link-to` 626 · `.held-*` 628–634
//            --glow 672 · --surface-head 668 · --room-height 63
//            템플릿 roomCard3(1199) · heldRoomCard(1367) · emptyRoomCard(1405) · anesChip(1180) · selAll(1194) · linkBar(1366) · 데이터 state(806~ · 시술실 A · c1 · IN_TIME c1)
// 256×448 · r6 · 테두리 없음 · 면 white · 그림자 0 2 4 -2 6%(SHADOW_ROOM) · overflow hidden
// active = 진한 1px(stroke 1 primary · 바깥) + 번짐 4 primary 30% · active-late = red + red 20% + 제목 warn-fill
// selection · going = 아래 호출 칸(절대 위치 · 여백 28 8 8) Button m(1개 호출 solid · 귀가 대기 filled)
// linked = 제목 아래 LinkBar · held = 몸 30% + 몸 가운데 Button filled-gray s 둘(시안은 올렸을 때만 보임) · empty = 면 gray/100 + 제목 줄만
const W = 256, H = 448, TITLE_H = 31, CALL_H = 72; // 호출 칸 = 28 + Button m 36 + 8
const C1 = {
  room: "시술실 A", name: "[TW] CHOU YU WEN", local: "저우위원", sex: "여", age: "만 37세", in: "입실 13:30",
  memo: "**500만원 이상\nOUT TIME : x\n0. 자가세안 O\n- 마취크림\n1. 소프웨이브 200펄스(이마, 눈가, 입가)\n2. 써마지 900샷(이마포함 얼전 + 이중턱)\n3. 리투오 파인 2cc 캐뉼라(눈밑)\n4. 주름 보톡스 제오민(이마, 미간, 눈가, 자갈턱)\n5. 국산 필러 1cc(턱끝)\n6. 수입필러 1cc(입술)\n7. 수입필러 2cc 쥬비덤 (앞볼)\n8. 세라핏 3cc(이중턱) - 금액권 sv",
};
const MOVED_TO = "레이저실 3"; // 데이터 r9 「옮길 수 있는 빈 방(데모)」
const EMPTY_ROOM = "시술실 F";   // 데이터 r10 빈 방

function rect(name, w, h, token) {
  const r = figma.createRectangle();
  r.name = name; r.resize(w, h); fill(r, token);
  return r;
}
// 제목 줄: 손잡이 + (late warn-fill) + 방 이름 [+ 옮긴 방 링크] ··· [마취 Badge]
function titleRow({ title, late, linkTo, badge }) {
  const wrap = [inst("IconButton", { icon: "grip" }, {}, "drag-handle")];
  if (late) { const w = icon("warn-fill"); w.name = "icon/late"; wrap.push(w); }
  wrap.push(text(title, "caption-md-500", "black", { name: "label" }));
  if (linkTo) {
    const a = icon("arrow-right-brand-16"); a.name = "icon/link-to";
    wrap.push(box("HORIZONTAL", { name: "link-to", gap: 4, children: [a, text(linkTo, "caption-md-500", "primary/DEFAULT", { name: "label/link-to" })] }));
  }
  const row = box("HORIZONTAL", {
    name: "room-title", w: W, h: TITLE_H, pt: 5, pb: 5, pl: 10, pr: 10, gap: 6, justify: "SPACE_BETWEEN", bg: "crm/surface-head",
    children: [grow(box("HORIZONTAL", { name: "title-wrap", gap: 4, children: wrap })), badge ? inst("Badge", { kind: "solid", color: "gray" }, {}, "anes-badge") : null],
  });
  return stretch(row);
}
function customer(withIn) {
  const vital = [text(C1.sex, "caption-md-400", "gray/700", { name: "label/sex" }), rect("bar", 1, 10, "gray/300"), text(C1.age, "caption-md-400", "gray/700", { name: "label/age" })];
  if (withIn) vital.push(rect("bar-2", 1, 10, "gray/300"), text(C1.in, "caption-md-400", "gray/700", { name: "label/in" }));
  return stretch(box("VERTICAL", {
    name: "customer", w: W, pt: 8, pl: 8, pr: 8,
    children: [
      box("HORIZONTAL", { name: "name-row", gap: 4, children: [text(C1.name, "body-600", "black", { name: "label/name" }), text(C1.local, "caption-md-500", "gray/800", { name: "label/local" })] }),
      box("HORIZONTAL", { name: "vital", gap: 4, children: vital }),
    ],
  }));
}
// 메모: 왼쪽 선 2 gray/500 · 여백 0 22 0 6 · 10/400 lh1.3 gray/800 · 최대 높이 67(넘치면 잘림) · 다섯 줄 넘으면 크게 보기(maximize) 오른쪽 14 · 아래 12
// 크게 보기 아이콘은 시안에서 메모 칸 오른쪽 여백(22) 위에 절대 위치 — 여기서는 메모 칸 오른쪽 여백 14 + 아이콘 16 으로 같은 자리
function memo(withMore) {
  const textW = W - 8 - 8 - 2 - 6 - 22; // 210 = 메모 칸 240 − 선 2 − 왼쪽 6 − 오른쪽 22(아이콘 있든 없든 같다)
  const t = text(C1.memo, "meta-sm-400", "gray/800", { name: "label/memo", width: textW });
  const line = stretch(rect("memo-line", 2, 67, "gray/500"));
  const mb = grow(box("HORIZONTAL", { name: "memo-box", h: 67, gap: 6, align: "MIN", clip: true, children: [line, t] }));
  return stretch(box("HORIZONTAL", {
    name: "memo", w: W, pt: 12, pb: 12, pl: 8, pr: withMore ? 14 : 8, align: "MAX",
    children: [mb, withMore ? inst("IconButton", { icon: "maximize" }, {}, "memo-more") : null],
  }));
}
// 시술 목록: [선 · (목록 머리 SelectAll + 진행 줄들)] [선 · (완료 줄들 · 위 여백 4)]
const row = (props, texts = {}) => inst("ProcRow", props, texts, "proc-row");
function procLists(selAll, active, done) {
  const kids = [
    stretch(rect("divider", W, 1, "gray/200")),
    stretch(box("VERTICAL", { name: "proc-list", w: W, gap: 4, children: [box("HORIZONTAL", { name: "list-head", pt: 8, pl: 8, pr: 8, gap: 8, children: [inst("SelectAll", { state: selAll }, {}, "select-all")] }), ...active] })),
  ];
  if (done.length) kids.push(stretch(rect("divider-done", W, 1, "gray/200")), stretch(box("VERTICAL", { name: "proc-list-done", w: W, pt: 4, children: done })));
  return stretch(box("VERTICAL", { name: "proc-lists", w: W, children: kids }));
}
const ROW_PROGRESS = () => row({ status: "progress", state: "default" });
const ROW_WAIT = () => row({ status: "wait", state: "default" });
const ROW_DONE = () => row({ status: "done", state: "default" });

function card(state) {
  const empty = state === "empty", held = state === "held", linked = state === "linked";
  const late = state === "active-late";
  const root = box("VERTICAL", { name: "room-card", w: W, h: H, radius: 6, bg: empty ? "gray/100" : "white", clip: true });
  shadows(root, SHADOW_ROOM);
  if (state === "active" || late) {
    stroke(root, late ? "red/DEFAULT" : "primary/DEFAULT", 1);
    root.strokeAlign = "OUTSIDE";
    shadows(root, [late ? ["#ff4e51", 0.2, 0, 0, 0, 4] : ["#1d8bff", 0.3, 0, 0, 0, 4], ...SHADOW_ROOM]);
  }
  root.appendChild(titleRow({ title: empty ? EMPTY_ROOM : linked ? MOVED_TO : C1.room, late, linkTo: held ? MOVED_TO : null, badge: !empty && !held }));
  if (empty) return root;
  if (linked) root.appendChild(stretch(inst("LinkBar", { state: "default" }, { label: C1.room }, "moved-from-bar")));

  const body = grow(stretch(box("VERTICAL", { name: "room-body", w: W, clip: true })));
  root.appendChild(body);
  if (held) {
    const fade = stretch(box("VERTICAL", { name: "held-fade", w: W, children: [customer(false), memo(false)] }));
    fade.opacity = 0.3;
    body.appendChild(fade);
    const acts = box("HORIZONTAL", {
      name: "held-actions", w: W, h: H - TITLE_H, gap: 8, justify: "CENTER", align: "CENTER",
      children: [
        inst("Button", { kind: "filled-gray", size: "s" }, { label: "연결 풀기" }, "button-release"),
        inst("Button", { kind: "filled-gray", size: "s" }, { label: "돌아오기" }, "button-return"),
      ],
    });
    body.appendChild(acts);
    acts.layoutPositioning = "ABSOLUTE";
    acts.x = 0; acts.y = 0;
    return root;
  }

  let lists;
  if (state === "selection") lists = procLists("mixed", [ROW_PROGRESS(), row({ status: "wait", state: "checked" }), row({ status: "wait", state: "default" }, { label: "주름 보톡스 제오민" })], [ROW_DONE()]);
  else if (late) lists = procLists("disabled", [ROW_PROGRESS(), row({ status: "called", state: "late" }, { label: "리투오 파인 2cc" })], [ROW_DONE()]);
  else if (state === "going") lists = procLists("disabled", [], [ROW_DONE()]);
  else lists = procLists("default", [ROW_PROGRESS(), ROW_WAIT()], [ROW_DONE()]);
  body.appendChild(customer(true));
  body.appendChild(memo(true));
  body.appendChild(lists);

  if (state === "selection" || state === "going") {
    const btn = state === "going"
      ? inst("Button", { kind: "filled", size: "m" }, { label: "귀가 대기" }, "button")
      : inst("Button", { kind: "solid", size: "m" }, { label: "1개 호출" }, "button");
    const call = box("HORIZONTAL", { name: "room-call", w: W, h: CALL_H, pt: 28, pb: 8, pl: 8, pr: 8, gap: 6, bg: "white", children: [btn] });
    root.appendChild(call);
    grow(btn);
    call.layoutPositioning = "ABSOLUTE";
    call.x = 0; call.y = H - CALL_H;
    call.constraints = { horizontal: "STRETCH", vertical: "MAX" };
  }
  return root;
}
const STATES = ["default", "active", "active-late", "selection", "going", "linked", "held", "empty"];
const variants = STATES.map((state) => ({ props: { state }, node: card(state) }));
makeSet("RoomCard", variants, { perRow: 4, description: "시안 .room(roomCard3 · heldRoomCard · emptyRoomCard) — 시술실 카드 256×448. 제목 줄 · 고객 · 메모 · 시술 목록(ProcRow) · 호출 칸. active = 진한 1px + 번짐 4, linked = LinkBar, held = 옮겨 간 원래 방(몸 30% + 연결 풀기 · 돌아오기), empty = 빈 방. 시술 줄은 견본 3~4줄." });
