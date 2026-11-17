// 1-3 — 「확인 필요」(4 화면)
// DIFF: confirm-flag — 시안은 늦은 카드를 제목 줄 warn-fill 아이콘 + 빨간 테두리(RoomCard active-late)로만 보임 ↔ 기획안 L262 「확인할 일」 글자 → 모양은 시안 active-late 그대로 + 고객 줄 아래 Badge solid red 셋(「대기 6분째」 · 「호출 6분째」 · 「시술 변경 1건」 · n = 브리프 샘플 6 · 1). 세 상황이 한 카드에 같이 든 그림은 요소를 다 보이려는 것
// DIFF: confirm-needed — 시안 인박스 사이드바(탭 현황 · 호출 · 시술 완료 / 묶음 확인 필요 · 시작 가능 · 시술 대기) ↔ 기획안 「확인 필요」 영역 → 「확인 필요」 묶음만(탭 · 다른 묶음 생략). 카드 = 시안 확인 필요 두 장(레이저실 1 마취 +23:00 · 레이저실 2 호출 +06:00, 늦은 순)
// DIFF: confirm-needed — 시안 InboxCard now-late 는 세트에 active-late(고른 상태)만 있음 → 떼어 테두리 gray/300 · 그림자 SHADOW_CARD(고르지 않은 모양)
// DIFF: 결정 U12 = 확인 필요 기준은 「마취 20분 초과 · 호출 5분 무응답」만 ↔ 기획안 「확인할 상황」 6종(마취 초과 40분 · 수락 뒤 미시작 · 시술 변경 · 귀가 대기 전 …) → confirm-needed 는 시안 · U12 의 두 장, confirm-needed/card 는 기획안 카드 버튼 4종(브리프 지시)
// DIFF: confirm-needed/card — 시안 확인 필요 카드는 원장 줄 「호출 +06:00」 + 「재호출」 하나 ↔ 기획안 버튼 4종 · 「확인할 일」 글자 → 원장 줄 숨기고 확인할 일 글자 줄(red 12/400) + 버튼 글자만 바꿈. 버튼 모양은 시안 outlined-gray ss(기획안 스타일 outlined/blue 는 세트에 없음)
// DIFF: confirm-needed/card — 「수락 뒤 미시작」 n 은 시안 샘플(수락 2분 전)이 기준 5분 미만이라 기준 분 「5분째」, 「시술 변경 1건」은 line-changed 화면과 같은 시술실 A
// DIFF: toast/alert — Notify 아이콘은 성공 체크(notify-check · primary 글자)라 「확인 필요」 알림 뜻과 다름 → 세트 그대로 두고 글자만 기획안 형식 「{관리실} {이름} {확인할 일}」 → 「레이저실 2 황웨이 호출 6분째」(시안 늦은 호출 = 레이저실 2 c7)
// DIFF: RoomCard 고객 줄 「입실 13:30」 → 결정 「입실을 빼고 국적」. 국적 형식(코드/이름)은 SPEC-000 OQ-02-1 열림 → 자리표시 「{국적}」

// InboxCard 떼어 고르지 않은 모양으로
function s13_plain(card) {
  stroke(card, "gray/300", 1);
  shadows(card, SHADOW_CARD);
  return card;
}
// 원장 줄 숨기고 확인할 일 글자 줄 더하기
function s13_confirmLine(card, str) {
  hideIn(card, "doctor-line");
  const t = text(str, "caption-md-400", "red/DEFAULT", { name: "label/confirm" });
  const line = box("HORIZONTAL", { name: "confirm-line", p: 2, gap: 4, children: [t] });
  findIn(card, "card-body").appendChild(line);
  return line;
}

unit("procedure/customer-card/confirm-flag", (ctx) => {
  const card = detach(inst("RoomCard", { state: "active-late" }, {}, "room-card"), "room-card-confirm-flag");
  setText(card, "label/in", "{국적}");
  const b1 = inst2("Badge", { kind: "solid", color: "red" }, { label: "대기 6분째" }, "confirm-flag");
  const b2 = inst2("Badge", { kind: "solid", color: "red" }, { label: "호출 6분째" }, "confirm-flag-2");
  const b3 = inst2("Badge", { kind: "solid", color: "red" }, { label: "시술 변경 1건" }, "confirm-flag-3");
  const flags = box("HORIZONTAL", { name: "confirm-flags", pt: 4, gap: 4, children: [b1, b2, b3] });
  findIn(card, "customer").appendChild(flags);
  ctx.mark(1, b1);
  ctx.mark(2, b2);
  ctx.mark(3, b3);
  return card;
});

unit("procedure/confirm-needed", (ctx) => {
  const head = inst("InboxSectionHead", { icon: "late" }, {}, "ib-head");
  // 레이저실 1 · c6 사토 유키 · 마취 +23:00(20분 초과 → red) · 호출 없음
  const anes = s13_plain(detach(inst("InboxCard", { kind: "now", state: "default" }, {}, "inbox-card"), "inbox-card-anes-late"));
  setText(anes, "label", "레이저실 1");
  hideIn(anes, "badge");
  findIn(anes, "card-head").appendChild(inst2("Badge", { kind: "solid", color: "red" }, { label: "마취 +23:00" }, "badge-anes"));
  setText(anes, "label/customer", "[JP] SATO YUKI");
  setText(anes, "label/local", "사토 유키");
  hideIn(anes, "doctor-line");
  // 레이저실 2 · c7 황웨이 · 이서연 원장 호출 +06:00 · 재호출
  const call = s13_plain(detach(inst("InboxCard", { kind: "now-late", state: "active-late" }, {}, "inbox-card"), "inbox-card-call-late"));
  const cards = box("VERTICAL", { name: "ib-cards", pt: 8, gap: 8, children: [anes, call] });
  for (const c of cards.children) stretch(c);
  ctx.mark(1, head);
  ctx.mark(2, cards);
  return box("VERTICAL", { name: "ib-list", w: 280, px: 12, py: 8, bg: "white", children: [head, cards] });
});

unit("procedure/confirm-needed/card", (ctx) => {
  const D = [
    { name: "confirm-card-recall", room: "레이저실 2", cust: "[TW] HUANG WEI", local: "황웨이", what: "호출 6분째", btn: "재호출" },
    { name: "confirm-card-renotify", room: "시술실 B", cust: "[JP] HIROSE YUURI", local: "히로세 유우리", what: "김도윤 원장 수락 5분째", btn: "다시 알림" },
    { name: "confirm-card-going", room: "시술실 E", cust: "[TW] CHEN YI TING", local: "천이팅", what: "귀가 대기 전", btn: "귀가 대기" },
    { name: "confirm-card-change", room: "시술실 A", cust: "[TW] CHOU YU WEN", local: "저우위원", what: "시술 변경 1건", btn: "변경 확인" },
  ];
  const head = inst("InboxSectionHead", { icon: "late" }, {}, "ib-head");
  const built = D.map((d) => {
    const card = s13_plain(detach(inst("InboxCard", { kind: "now-late", state: "active-late" }, {}, "inbox-card"), d.name));
    setText(card, "label", d.room);
    setText(card, "label/customer", d.cust);
    setText(card, "label/local", d.local);
    const line = s13_confirmLine(card, d.what);
    const btn = findIn(card, "button");
    setText(btn, "label", d.btn);
    return { card, line, btn };
  });
  const cards = box("VERTICAL", { name: "ib-cards", pt: 8, gap: 8, children: built.map((b) => b.card) });
  for (const c of cards.children) stretch(c);
  ctx.mark(1, findIn(built[0].card, "card-head"));
  ctx.mark(2, built[0].line);
  built.forEach((b, i) => ctx.mark(3 + i, b.btn));
  return box("VERTICAL", { name: "ib-list", w: 280, px: 12, py: 8, bg: "white", children: [head, cards] });
});

unit("procedure/toast/alert", (ctx) => {
  const n = inst2("Notify", { state: "default" }, { label: "레이저실 2 황웨이 호출 6분째" }, "notify");
  ctx.mark(1, n);
  return box("HORIZONTAL", { name: "toast-area", w: ctx.w, h: ctx.h, justify: "CENTER", align: "CENTER", children: [n] });
});
