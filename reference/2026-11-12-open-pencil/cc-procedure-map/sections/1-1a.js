// 1-1a — 시술 현황 화면 · 관리실 칸 · 고객 카드(카드 상태 · 오더 메모). 화면 9개.
// DIFF: 레일 바탕 = 시안 --secondary #000a14 → 변수 없음 → black. 판 바탕 --surface-board #e3e3e5 → gray/300
// DIFF: 레일 아이콘(rail-*.svg) · 병원 이름 꺾쇠(hd-chevron-down-12)는 Icon 세트에 없음 → 글자만
// DIFF: 레일 고른 칸 = 시안 crmRail("예약") 그대로 「예약」
// DIFF: 페이지 머리 오른쪽 [필터] · 「의사별 · 4층 · 미사용」 = 결정(화면을 보고 2026-11-06)대로 뺌. 기획안 「관리실 기록」(시안에 없음)은 Button outlined-gray ss 로 넣음
// DIFF: 판 = 시안 state.rooms 순서. 빈 방(레이저실 3 · 시술실 F)은 결정 U6 대로 안 그림(기획안 정책 3 「사용을 켠 관리실마다 칸」과 다름) — 둘째 줄부터 슬롯 밖이라 잘림
// DIFF: 판 카드 = 시안 RoomCard 모양(마취 배지 = 방 머리 오른쪽 · 시안 「마취 완료 n분」/「마취 +mm:ss」) ↔ 기획안 「마취 시작 · 마취중 mm:ss · 마취 종료」 · 카드 상태 배지
// DIFF: 판 카드 고객 줄 = 결정대로 「입실 HH:MM」을 뺌. 국적은 시안 데이터에 값이 없어(flag 만) 판 카드에선 비움 — 고객 카드 화면은 「{국적}」(형식 미정 SPEC-000 OQ-02-1)
// DIFF: 시안 판 카드 시술 줄 = state.orders 그대로(대기 줄에 담당 원장 표시 없음 — ProcRow wait 에 원장 자리 없음)
// DIFF: 인박스 = 시안 사이드바(현황 · 호출 · 시술 완료 탭 / 확인 필요 · 시작 가능 · 시술 대기) ↔ 기획안 「확인 필요」 영역. 확인 필요 카드는 레이저실 2(호출 6분)만 — 레이저실 1(마취 +23:00 초과)은 세트에 빨간 배지 now 카드가 없어 뺌
// DIFF: 관리실 칸 = 기획안 「침대마다 칸」을 기획안 예시 「A-룸2 (1/2)」 형식으로 두 칸(「(2/2)」는 그 형식을 이어 씀)
// DIFF: 점유 중 = 시안 held 카드(방 머리 「→ 옮긴 방」 + 몸 30% + 「연결 풀기 · 돌아오기」) ↔ 기획안 「점유 중 · {고객 이름}」 — 방 머리 링크 글을 기획안 문구로, 화살표는 숨김, 시안 버튼 둘은 그대로 둠
// DIFF: 고객 카드 = 시안 RoomCard(selection)를 떼어 기획안 요소 더함 — 카드 상태 배지는 시안 마취 배지 자리(방 머리 오른쪽), 마취는 고객 정보 아래 줄로 내림
// DIFF: 고객 카드 고객 정보 = 시안 성별 · 나이 + 결정 「국적」 + 기획안 「담당 상담실장」 · 「통역 필요 중국어」(보라 배지는 세트에 없어 custom)
// DIFF: 오더 메모 = 시안 글 덩어리(memo-box) ↔ 기획안 칸별 칩 7종 → 기획안대로 Badge solid gray 칩
// DIFF: 시안 「n개 호출」 한 버튼(결정 U2 팝오버) ↔ 기획안 「전체 호출 · n개」 · 「지정 호출 · n개」 두 버튼 → 기획안. 지정 호출 = outlined-blue 가 세트에 없어 Button filled m
// DIFF: 「귀가 대기」 버튼 = 시안 filled m(기획안 solid/blue/s). 호출 버튼과 같은 카드에 동시에 안 보여서 카드 아래 따로 둔 칸(call-area-going)
// DIFF: 카드 상태 「귀가 대기 HH:MM」 = 시안 귀가 대기 배지(going-wait 초록) — 기획안 style warning(노랑)과 다름. 시각 14:42 = 시안 HISTORY(13:30-14:42)
// DIFF: 귀가 대기 카드 = 기획안 5-1 「카드는 같은 관리실에 그대로」(시안 U8 은 판에서 빠지고 시술 완료 탭)
{
  const s11Bar = (name, w, h, token) => { const r = figma.createRectangle(); r.name = name; r.resize(w, h); fill(r, token); return r; };
  const s11Row = ([status, state, t]) => inst2("ProcRow", { status, state }, t, "proc-row");
  const s11Badge = (color, label, name = "badge") => inst2("Badge", { kind: "solid", color }, { label }, name);
  // 이름이 긴 시술 줄 — 이름 글자 폭을 고정해 줄바꿈(인스턴스에서 안 되면 그대로 · 카드가 자른다)
  const s11Wrap = (row, w) => { const t = findIn(row, "label"); try { t.textAutoResize = "HEIGHT"; t.resize(w, t.height); } catch (e) { /* 그대로 */ } return row; };

  // 시안 데이터(state.customers · state.orders · state.calls · IN_TIME) — 시술 줄 = [status, state, 글자]
  const CU = {
    c1: { name: "[TW] CHOU YU WEN", local: "저우위원", sex: "여", age: "만 37세" },
    c2: { name: "[JP] HIROSE YUURI", local: "히로세 유우리", sex: "여", age: "만 37세" },
    c3: { name: "[TW] LIN MEI", local: "린메이", sex: "여", age: "만 29세" },
    c4: { name: "[JP] SUZUKI ICHIRO", local: "스즈키 이치로", sex: "남", age: "만 42세" },
    c5: { name: "[TW] CHEN YI TING", local: "천이팅", sex: "여", age: "만 31세" },
    c6: { name: "[JP] SATO YUKI", local: "사토 유키", sex: "여", age: "만 26세" },
    c7: { name: "[TW] HUANG WEI", local: "황웨이", sex: "남", age: "만 35세" },
    c8: { name: "[JP] KIMURA AOI", local: "기무라 아오이", sex: "여", age: "만 33세" },
  };
  const W_ = (label) => ["wait", "default", { label, "label/status": "준비중" }];
  const P_ = (label, doctor, time) => ["progress", "default", { label, "label/doctor": doctor, "label/time": time }];
  const C_ = (label, doctor, time, late) => ["called", late ? "late" : "default", { label, "label/doctor": doctor, "label/time": time }];
  const A_ = (label, doctor) => ["ready", "default", { label, "label/doctor": doctor }];
  const D_ = (label, time) => ["done", "default", { label, "label/time": time }];
  const ROOMS = [
    { title: "시술실 A", cu: "c1", badge: ["gray", "마취 완료 21분"], memo: "**500만원 이상\nOUT TIME : x\n0. 자가세안 O\n- 마취크림\n1. 소프웨이브 200펄스(이마, 눈가, 입가)\n2. 써마지 900샷(이마포함 얼전 + 이중턱)\n3. 리투오 파인 2cc 캐뉼라(눈밑)\n4. 주름 보톡스 제오민(이마, 미간, 눈가, 자갈턱)\n5. 국산 필러 1cc(턱끝)\n6. 수입필러 1cc(입술)\n7. 수입필러 2cc 쥬비덤 (앞볼)\n8. 세라핏 3cc(이중턱) - 금액권 sv",
      active: [P_("써마지 900샷", "김도윤 원장", "8분"), W_("리투오 파인 2cc"), W_("주름 보톡스 제오민"), W_("국산 필러 1cc"), W_("수입필러 1cc"), W_("수입필러 2cc 쥬비덤"), W_("세라핏 3cc")], done: [D_("소프웨이브 200펄스", "28분")], selAll: "default" },
    { title: "시술실 B", cu: "c2", badge: ["primary", "마취 +12:00"], memo: "OUT TIME : 16:00\n0. 자가세안 X\n- 마취크림 40분\n1. 울쎄라피 프라임 300샷(볼, 턱선)\n2. 리쥬란 힐러 2cc(얼굴 전체)\n3. 보톡스 이마 - 김도윤 원장님 지정",
      active: [A_("울쎄라피 프라임 300 shot", "김도윤 원장"), W_("리쥬란 힐러"), W_("보톡스 이마")], done: [], selAll: "default" },
    { title: "시술실 C", cu: "c3", badge: null, memo: "첫 방문 · 통증 예민\n0. 자가세안 O\n1. 쥬베룩 2cc(앞볼)\n2. 레이저토닝 1회",
      active: [C_("쥬베룩", "전체", "2분"), W_("레이저토닝")], done: [], selAll: "default" },
    { title: "시술실 D", cu: "c4", badge: ["gray", "마취 완료 20분"], memo: "OUT TIME : x\n1. 슈링크 유니버스 300샷(하안면)\n2. 아쿠아필\n3. 레이저토닝 - 10회 패키지 4회차",
      active: [P_("슈링크 유니버스 300 shot", "이서연 원장", "14분"), W_("레이저토닝")], done: [D_("아쿠아필", "22분")], selAll: "default" },
    { title: "시술실 E", cu: "c5", base: "going", badge: ["gray", "마취 완료 22분"], memo: "0. 자가세안 O\n1. 리쥬란 힐러 2cc(눈밑 제외)\n2. 보톡스 사각턱 50u\n3. 모델링팩 - 10월 이벤트(진정팩)",
      active: [], done: [D_("리쥬란 힐러", "27분"), D_("보톡스 사각턱", "16분"), D_("모델링팩", "10분")], selAll: "disabled" },
    { title: "레이저실 1", cu: "c6", badge: ["red", "마취 +23:00"], memo: "토닝 10회 패키지 4회차\n1. 레이저토닝\n2. 아쿠아필",
      active: [W_("레이저토닝"), W_("아쿠아필")], done: [], selAll: "default" },
    { title: "레이저실 2", cu: "c7", badge: null, memo: "원장님 상담 먼저 · 시술 범위 바뀔 수 있음\n1. 울쎄라피 프라임 300샷(턱선)\n2. 써마지 FLX 300샷(눈가 제외)\n3. 보톡스 이마",
      active: [C_("울쎄라피 프라임 300 shot", "이서연 원장", "6분", true), C_("써마지 FLX 300shot", "이서연 원장", "6분", true), C_("보톡스 이마", "박하준 원장", "2분")], done: [], selAll: "disabled" },
    { title: "VIP실", cu: "c8", badge: ["gray", "마취 완료 19분"], memo: "**300만원 이상 · 보호자 동반\nOUT TIME : 17:30\n0. 자가세안 O\n- 마취크림\n1. 써마지 FLX 300샷(하안면, 턱끝 피하기)\n2. 쥬베룩 볼·팔자 각 1cc\n3. 리쥬란 힐러(눈밑 제외)\n4. 모델링팩 - 마지막에",
      active: [P_("써마지 FLX 300shot", "이서연 원장", "11분"), C_("쥬베룩", "박하준 원장", "3분"), W_("리쥬란 힐러"), W_("모델링팩")], done: [], selAll: "default" },
  ];

  // RoomCard 를 떼어 방 · 고객 · 메모 · 시술 줄을 시안 데이터로 바꾼다
  // o: { base, cname, title, badge(노드|null), cu, keepIn, memo, active, done, selAll }
  const s11Card = (o) => {
    const c = detach(inst("RoomCard", { state: o.base || "default" }, {}, "room-card"), o.cname || "room-card");
    setText(c, "label", o.title, 0);
    const ab = findIn(c, "anes-badge");
    if (ab) { const p = ab.parent; ab.remove(); if (o.badge) p.appendChild(o.badge); }
    setText(c, "label/name", o.cu.name); setText(c, "label/local", o.cu.local);
    setText(c, "label/sex", o.cu.sex); setText(c, "label/age", o.cu.age);
    if (!o.keepIn) { for (const n of ["label/in", "bar-2"]) { const x = findIn(c, n); if (x) x.remove(); } }
    if (o.memo !== undefined) setText(c, "label/memo", o.memo);
    const list = findIn(c, "proc-list");
    for (const k of [...list.children]) if (k.name !== "list-head") k.remove();
    const lh = findIn(list, "list-head");
    for (const k of [...lh.children]) k.remove();
    lh.appendChild(inst("SelectAll", { state: o.selAll || "default" }, {}, "select-all"));
    for (const r of o.active || []) list.appendChild(Array.isArray(r) ? s11Row(r) : r);
    const dl = findIn(c, "proc-list-done");
    const done = o.done || [];
    if (dl) {
      for (const k of [...dl.children]) k.remove();
      if (done.length) for (const r of done) dl.appendChild(s11Row(r));
      else { const dd = findIn(c, "divider-done"); if (dd) dd.remove(); dl.remove(); }
    } else if (done.length) {
      const lists = findIn(c, "proc-lists");
      lists.appendChild(stretch(s11Bar("divider-done", 256, 1, "gray/200")));
      lists.appendChild(stretch(box("VERTICAL", { name: "proc-list-done", w: 256, pt: 4, children: done.map(s11Row) })));
    }
    return c;
  };
  const s11Room = (r, title) => s11Card({
    base: r.base, title: title || r.title, cu: CU[r.cu], memo: r.memo, active: r.active, done: r.done, selAll: r.selAll,
    badge: r.badge ? s11Badge(r.badge[0], r.badge[1], "anes-badge") : null,
  });

  // 기획안 고객 카드(1-1 화면 구성) — 시안 카드에 국적 · 담당 상담실장 · 통역 · 마취 줄 · 오더 메모 칩
  const s11Plan = (o) => {
    const c = s11Card({ ...o, title: "시술실 A", cu: CU.c1, keepIn: true, cname: "customer-card" });
    const nat = setText(c, "label/in", "{국적}"); nat.name = "label/nationality";
    const vital = findIn(c, "vital");
    vital.appendChild(s11Bar("bar-3", 1, 10, "gray/300"));
    vital.appendChild(text("{상담실장}", "caption-md-400", "gray/700", { name: "label/counselor" }));
    const cust = findIn(c, "customer");
    const interp = custom("badge-interpreter", box("HORIZONTAL", { name: "badge", pt: 3, pb: 3, pl: 6, pr: 6, radius: 6, bg: "purple/100", children: [text("통역 필요 중국어", "badge-11", "purple/DEFAULT", { name: "label", ls: 0.34 })] }));
    cust.appendChild(box("HORIZONTAL", { name: "interp-row", pt: 4, children: [interp] }));
    let anes = null;
    if (o.anes) { anes = inst2("Badge", { kind: "outline", color: "primary" }, { label: "마취 시작" }, "anes-badge"); cust.appendChild(box("HORIZONTAL", { name: "anes-row", pt: 8, children: [anes] })); }
    // 오더 메모: 시안 글 덩어리 숨기고 기획안 칩
    const memo = findIn(c, "memo");
    for (const n of ["memo-box", "memo-more"]) { const x = findIn(memo, n); if (x) x.visible = false; }
    const chips = custom("order-memo", box("HORIZONTAL", { name: "order-memo", gap: 4, children: o.chips.map((t) => s11Badge("gray", t, "memo-chip")) }));
    memo.appendChild(chips);
    return { c, vital, interp, anes, chips };
  };

  // 화면 틀 — 헤더 · 페이지 머리
  const s11Header = (w) => {
    const tabs = box("HORIZONTAL", {
      name: "tabs", gap: 16, align: "MAX",
      children: [
        inst2("Tab", { kind: "header", state: "default" }, { label: "예약 현황" }, "tab"),
        inst2("Tab", { kind: "header", state: "default" }, { label: "원내 현황" }, "tab"),
        inst2("Tab", { kind: "header", state: "active" }, { label: "시술 현황" }, "tab-active"),
      ],
    });
    const search = inst("Search", { size: "ss", state: "default" }, {}, "search");
    const tools = grow(box("HORIZONTAL", { name: "tools", gap: 8, justify: "MAX", children: [search] }));
    const h = custom("header", box("HORIZONTAL", { name: "header", w, h: 44, px: 16, gap: 24, bg: "white", children: [text("세라미크의원 명동점", "caption-md-500", "gray/800", { name: "label/hospital" }), tabs, tools] }));
    return { h, tab: tabs.children[2], search };
  };
  const s11Controls = (w) => {
    const rec = inst2("Button", { kind: "outlined-gray", size: "ss" }, { label: "관리실 기록" }, "button-room-log");
    const right = grow(box("HORIZONTAL", { name: "pc-right", gap: 8, justify: "MAX", children: [rec] }));
    const pc = custom("page-controls", box("HORIZONTAL", {
      name: "page-controls", w, h: 32, pl: 16, pr: 16, pb: 4, gap: 6, bg: "white",
      children: [text("시술 현황", [16, 600, 24], "gray/800", { name: "label/title" }), s11Bar("divider", 1, 12, "gray/300"), text("2026-10-26 (월)", [16, 600, 24], "gray/800", { name: "label/date" }), right],
    }));
    return { pc, rec };
  };

  // ── 1. 시술 현황 화면 ─────────────────────────────
  unit("procedure/board", (ctx) => {
    const RAIL = ["홈", "예약", "고객", "시술", "매출", "설정"];
    const rail = custom("rail", box("VERTICAL", {
      name: "rail", w: 46, h: ctx.h, pt: 20, pb: 16, px: 4, gap: 8, align: "CENTER", bg: "black",
      children: RAIL.map((n) => box("VERTICAL", { name: "rail-item", w: 38, h: 38, radius: 6, justify: "CENTER", align: "CENTER", children: [text(n, "meta-sm-500", "white", { name: "label", opacity: n === "예약" ? 1 : 0.42 })] })),
    }));
    const MW = ctx.w - 46, CH = ctx.h - 44 - 32 - 1, QW = 280, BW = MW - QW - 1;
    const { h: header, tab, search } = s11Header(MW);
    const { pc, rec } = s11Controls(MW);

    // 인박스(시안 renderSide4 · 현황 탭)
    const ibTabs = box("HORIZONTAL", {
      name: "ib-tabs", pt: 8, pb: 8, pl: 16, pr: 12, gap: 24, align: "MAX",
      children: [
        inst2("Tab", { kind: "inbox", state: "active" }, { label: "현황" }, "tab-active"),
        inst2("Tab", { kind: "inbox", state: "default" }, { label: "호출 2" }, "tab"),
        inst2("Tab", { kind: "inbox", state: "default" }, { label: "시술 완료 2" }, "tab"),
      ],
    });
    const lateHead = inst("InboxSectionHead", { icon: "late" }, {}, "ib-head");
    const sec = (name, kids) => box("VERTICAL", { name, gap: 8, children: kids });
    const ibList = box("VERTICAL", {
      name: "ib-list", pt: 8, pb: 8, px: 12, gap: 12,
      children: [
        sec("ib-section-late", [lateHead, inst("InboxCard", { kind: "now-late", state: "active-late" }, {}, "inbox-card")]),
        sec("ib-section-going", [inst("InboxSectionHead", { icon: "going" }, {}, "ib-head"), inst("InboxCard", { kind: "now", state: "default" }, {}, "inbox-card")]),
        sec("ib-section-wait", [inst("InboxSectionHead", { icon: "wait" }, {}, "ib-head")]),
      ],
    });
    const queue = custom("queue", box("VERTICAL", { name: "queue", w: QW, h: CH, bg: "white", clip: true, children: [ibTabs, ibList] }));

    // 판(시안 .rooms — 카드 256 · 간격 8 · 여백 10) 4열
    const cards = ROOMS.map((r) => s11Room(r));
    const rows = [];
    for (let i = 0; i < cards.length; i += 4) rows.push(box("HORIZONTAL", { name: "room-row", gap: 8, align: "MIN", children: cards.slice(i, i + 4) }));
    const board = custom("board", box("VERTICAL", { name: "board", w: BW, h: CH, p: 10, gap: 8, bg: "gray/300", clip: true, children: rows }));

    const content = box("HORIZONTAL", { name: "content", w: MW, h: CH, align: "MIN", children: [queue, s11Bar("divider-queue", 1, CH, "gray/300"), board] });
    const main = box("VERTICAL", { name: "main", w: MW, h: ctx.h, bg: "white", clip: true, children: [header, pc, s11Bar("divider-content", MW, 1, "gray/300"), content] });
    try { main.topLeftRadius = 8; main.bottomLeftRadius = 8; } catch (e) { /* 모서리 따로 못 주면 그대로 */ }

    ctx.mark(1, tab); ctx.mark(2, search); ctx.mark(3, rec); ctx.mark(4, lateHead); ctx.mark(5, board);
    return box("HORIZONTAL", { name: "design", w: ctx.w, h: ctx.h, align: "MIN", bg: "black", children: [rail, main] });
  });

  // ── 「조회 시간 밖」 ─────────────────────────────
  unit("procedure/board/out-of-hours", (ctx) => {
    const { h: header } = s11Header(ctx.w);
    const { pc } = s11Controls(ctx.w);
    const banner = custom("banner-out-of-hours", box("HORIZONTAL", {
      name: "banner", h: 44, px: 16, gap: 8, radius: 6, bg: "white", border: "gray/300",
      children: [text("조회 시간 밖", "heading-sm-500", "gray/700", { name: "label" })],
    }));
    stretch(banner);
    const area = grow(stretch(box("VERTICAL", { name: "board", w: ctx.w, p: 10, bg: "gray/300", children: [banner] })));
    ctx.mark(1, banner);
    return box("VERTICAL", { name: "design", w: ctx.w, h: ctx.h, bg: "white", clip: true, children: [header, pc, s11Bar("divider-content", ctx.w, 1, "gray/300"), area] });
  });

  // ── 관리실 칸(침대마다 칸) ───────────────────────
  unit("procedure/room-slot", (ctx) => {
    const a = s11Room(ROOMS[0], "A-룸2 (1/2)");
    const b = s11Room(ROOMS[1], "A-룸2 (2/2)");
    ctx.mark(1, findIn(a, "label"));
    ctx.mark(2, b);
    return box("HORIZONTAL", { name: "design", w: ctx.w, h: ctx.h, gap: 8, justify: "CENTER", align: "CENTER", bg: "gray/300", children: [a, b] });
  });

  // ── 「점유 중 · {고객 이름}」 칸 ──────────────────
  unit("procedure/room-slot/occupied", (ctx) => {
    const card = inst("RoomCard", { state: "held" }, {}, "room-card");
    const t = setText(card, "label/link-to", "점유 중 · [TW] CHOU YU WEN");
    hideIn(card, "icon/link-to");
    ctx.mark(1, t);
    return box("VERTICAL", { name: "design", w: ctx.w, h: ctx.h, px: 12, py: 11, bg: "gray/300", children: [card] });
  });

  // ── 고객 카드(기획안 요소 12) ────────────────────
  unit("procedure/customer-card", (ctx) => {
    const status = s11Badge("primary", "시술 진행", "status-badge");
    const progress = s11Wrap(s11Row(P_("써마지 FLX 300shot (얼전, 이마포함)", "김도윤 원장", "8분")), 120);
    const { c, vital, interp, anes, chips } = s11Plan({
      base: "selection", badge: status, anes: true, chips: ["200만원결제", "마취크림 30분 희망"], selAll: "checked",
      active: [progress, A_("울쎄라피 프라임 300 shot", "김도윤 원장"), ["wait", "checked", { label: "[이벤트] 아쿠아필 2회", "label/status": "준비중" }]], done: [],
    });
    // 호출 칸: 시안 「1개 호출」 → 기획안 두 버튼
    const call = findIn(c, "room-call");
    for (const k of [...call.children]) k.remove();
    const all = grow(inst2("Button", { kind: "solid", size: "m" }, { label: "전체 호출 · 1개" }, "button-call-all"));
    const pick = grow(inst2("Button", { kind: "filled", size: "m" }, { label: "지정 호출 · 1개" }, "button-call-pick"));
    call.appendChild(all); call.appendChild(pick);
    // 귀가 대기 — 호출 버튼과 같이 안 보이는 상태라 카드 아래 따로
    const going = grow(inst2("Button", { kind: "filled", size: "m" }, { label: "귀가 대기" }, "button-going"));
    const goingArea = custom("call-area-going", box("HORIZONTAL", { name: "call-area-going", w: 256, p: 8, radius: 6, bg: "white", children: [going] }));
    ctx.mark(1, findIn(c, "label")); ctx.mark(2, status); ctx.mark(3, findIn(c, "label/name")); ctx.mark(4, vital);
    ctx.mark(5, interp); ctx.mark(6, chips); ctx.mark(7, anes); ctx.mark(8, progress); ctx.mark(9, findIn(c, "select-all"));
    ctx.mark(10, all); ctx.mark(11, pick); ctx.mark(12, going);
    return box("VERTICAL", { name: "design", w: ctx.w, h: ctx.h, px: 22, py: 12, gap: 8, bg: "gray/300", children: [c, goingArea] });
  });

  // ── 카드 상태 3종 ───────────────────────────────
  const s11Status = (ctx, badge, o) => {
    const { c } = s11Plan({ chips: ["200만원결제", "마취크림 30분 희망"], ...o, badge });
    return box("VERTICAL", { name: "design", w: ctx.w, h: ctx.h, px: 12, py: 11, bg: "gray/300", children: [c] });
  };
  unit("procedure/customer-card/status-waiting", (ctx) => {
    const b = s11Badge("gray", "시술 대기 13:30", "status-badge");
    ctx.mark(1, b);
    return s11Status(ctx, b, { anes: true, selAll: "default", active: [W_("써마지 900샷"), W_("리투오 파인 2cc"), W_("주름 보톡스 제오민")], done: [] });
  });
  unit("procedure/customer-card/status-in-progress", (ctx) => {
    const b = s11Badge("primary", "시술 진행", "status-badge");
    ctx.mark(1, b);
    return s11Status(ctx, b, { anes: true, selAll: "default", active: [P_("써마지 900샷", "김도윤 원장", "8분"), W_("리투오 파인 2cc")], done: [D_("소프웨이브 200펄스", "28분")] });
  });
  unit("procedure/customer-card/status-discharge-wait", (ctx) => {
    const b = s11Badge("going-wait", "귀가 대기 14:42", "status-badge");
    const more = inst("IconButton", { icon: "more" }, {}, "button-more");
    const st = box("HORIZONTAL", { name: "status", gap: 4, children: [b, more] });
    ctx.mark(1, b); ctx.mark(2, more);
    // 기획안: 귀가 대기면 마취 없음 · 오더 메모 · 시술 줄은 그대로
    return s11Status(ctx, st, { anes: false, selAll: "disabled", active: [], done: [D_("소프웨이브 200펄스", "28분")] });
  });

  // ── 오더 메모 7종 ───────────────────────────────
  unit("procedure/customer-card/order-memo", (ctx) => {
    const T = ["자가세안 x", "OUT TIME 16:00", "200만원결제", "지정 김도윤 원장", "마취크림 30분 희망", "특이사항 · {글}", "임플란트 O"];
    const chips = T.map((t) => s11Badge("gray", t, "memo-chip"));
    const lines = [[0, 1], [2, 3], [4, 5], [6]].map((ix) => box("HORIZONTAL", { name: "chip-line", gap: 4, children: ix.map((i) => chips[i]) }));
    chips.forEach((n, i) => ctx.mark(i + 1, n));
    const title = stretch(box("HORIZONTAL", { name: "room-title", w: 256, h: 31, pt: 5, pb: 5, pl: 10, pr: 10, bg: "crm/surface-head", children: [text("시술실 B", "caption-md-500", "black", { name: "label" })] }));
    const cust = box("HORIZONTAL", { name: "name-row", pt: 8, pl: 8, pr: 8, gap: 4, children: [text(CU.c2.name, "body-600", "black", { name: "label/name" }), text(CU.c2.local, "caption-md-500", "gray/800", { name: "label/local" })] });
    const memo = custom("order-memo", box("VERTICAL", { name: "order-memo", pt: 12, pb: 12, pl: 8, pr: 8, gap: 4, children: lines }));
    const card = custom("card-fragment", box("VERTICAL", { name: "room-card", w: 256, radius: 6, bg: "white", clip: true, children: [title, cust, memo] }));
    shadows(card, SHADOW_ROOM);
    return box("VERTICAL", { name: "design", w: ctx.w, h: ctx.h, p: 12, bg: "gray/300", children: [card] });
  });
}
