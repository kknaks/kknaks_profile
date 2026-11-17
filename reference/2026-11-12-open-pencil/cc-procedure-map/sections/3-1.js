// 3-1 의사 호출 — 화면 2
// DIFF: calling = 기획안 호출 중 줄 아랫단 「호출 중 n분」 / 「{원장} 호출 중 n분」 · 윗단 「시작」 · 「재호출」(L402 · L517) ↔ 시안 called 줄 「전체 호출」 + 시계 칸 「2분」 · 버튼 「수락」. 문구 · 버튼은 기획안, 줄 모양은 시안 ProcRow called(5분 넘은 줄 = late 빨강) — 떼어 시계 칸 숨기고 「수락」을 「시작」 · 「재호출」로 바꿈
// DIFF: calling 버튼 크기 = 기획안 style ss(solid/blue/ss · outlined/gray/ss) — 시안 줄 버튼은 xs(24). 「재호출」 outlined-gray 는 세트에 ss 만 있어 둘 다 ss
// DIFF: calling 조각 폭 280(시안 줄 256) — 「써마지 FLX 300shot」 · 「이서연 원장 호출 중 6분」이 버튼 둘 옆에 들어가게 슬롯 폭으로
// DIFF: calling 샘플 = 시안 호출 k5(시술실 C 쥬베룩 · 전체 · 2분) · k1(레이저실 2 써마지 FLX 300shot · 이서연 원장 지정 · 6분)
// DIFF: designate-call = 결정 U2 는 팝오버에서 「모든 의사」 | 원장 한 명 ↔ 기획안은 「전체 호출 · n개」를 따로 두고 「지정 호출」 원장 목록은 원장만(L389 · L418) — 기획안을 따라 「모든 의사」(전체 호출) 줄 없음(Popover accept 모양)
// DIFF: designate-call 머리 = 결정 「화면 참고 — 의사 호출 창」 「의사 호출」. 결정의 「방 · 고객 이름」 보조 머리 · 오른쪽 「선택됨 / 호출할 시술 · N개」 칸 · 「추천」 묶음은 그리지 않음(시안 Popover 한 칸 모양 — 「선택됨」 · 「전체」 구역 라벨은 시안 그대로)
// DIFF: designate-call 지정 원장(이서연 원장 · 시안 k1) 맨 위 골라진 채(PopOption on) — 기획안 L418. 시안 꼬리표(「처음 호출」 · 「호출」)는 기획안에 없어 숨김. 보조 글 = 시안 doctorStatus 꼴(김도윤 = 시술실 A 시술 중 · 이서연 = 시술실 D 시술 중 · 박하준 = 비어 있음)
// DIFF: designate-call 기획안은 라디오 + 「호출」 ↔ 시안 줄 고르기(PopOption on) + 발 버튼 — 시안 모양. 고른 상태라 「호출」은 켜진 모양

function docAvatarComp31(tone) {
  return findSet("Avatar").children.find((c) => c.name === `kind=doctor, tone=${tone}`);
}
// 원장 줄 하나. on = 고른 줄(세트 on 은 tone 1, default 는 tone 0 — 다르면 아바타만 바꿈)
function doctorOpt31(tone, short, full, sub, on, name) {
  const o = inst("PopOption", { kind: "doctor", state: on ? "on" : "default" }, {}, name);
  const builtin = on ? "1" : "0";
  if (tone !== builtin) {
    const av = findIn(o, "avatar");
    try { if (av && av.swapComponent) av.swapComponent(docAvatarComp31(tone)); } catch (e) { /* 안쪽 바꾸기가 막히면 세트 tone 그대로 */ }
  }
  setText(o, "label", short, 0);
  setText(o, "label", full, 1);
  setText(o, "label/sub", sub);
  const tag = findIn(o, "label/tag");
  if (tag) tag.visible = false;
  return o;
}

function callingRow31(props, name, proc, doctor, status) {
  const r = detach(inst("ProcRow", props, {}, "proc-row"), name);
  r.resize(280, r.height);
  setText(findIn(r, "name-meta"), "label", proc);
  if (doctor) setText(r, "label/doctor", doctor); else hideIn(r, "label/doctor");
  setText(r, "label/status", status);
  hideIn(r, "proc-time");
  const old = r.children.find((n) => n.name === "button");
  if (old) old.remove();
  const start = inst2("Button", { kind: "solid", size: "ss" }, { label: "시작" }, "button-start");
  const recall = inst2("Button", { kind: "outlined-gray", size: "ss" }, { label: "재호출" }, "button-recall");
  r.appendChild(box("HORIZONTAL", { name: "actions", gap: 4, children: [start, recall] }));
  return { r, start, recall };
}

unit("procedure/treatment-line/calling", (ctx) => {
  const head = inst("SelectAll", { state: "disabled" }, {}, "select-all");
  const headRow = box("HORIZONTAL", { name: "list-head", pl: 6, pr: 8, py: 4, children: [head] });
  const all = callingRow31({ status: "called", state: "default" }, "proc-row-calling-all", "쥬베룩", null, "호출 중 2분");
  const pick = callingRow31({ status: "called", state: "late" }, "proc-row-calling-designate", "써마지 FLX 300shot", "이서연 원장", "호출 중 6분");
  ctx.mark(1, findIn(all.r, "checkbox"));
  ctx.mark(2, all.start);
  ctx.mark(3, all.recall);
  ctx.mark(4, findIn(all.r, "label/status"));
  ctx.mark(5, findIn(pick.r, "meta"));
  return box("VERTICAL", { name: "design", w: 280, py: 4, gap: 4, bg: "white", children: [headRow, all.r, pick.r] });
});

unit("procedure/doctor-list/designate-call", (ctx) => {
  const d = detach(inst("Popover", { mode: "accept" }, {}, "popover"), "doctor-designate-call");
  const head = d.children.find((n) => n.name === "head");
  setText(head, "label", "의사 호출");
  const body = d.children.find((n) => n.name === "body");
  for (const n of [...body.children]) if (n.name !== "section-label") n.remove();
  // 선택됨: 지정 원장 · 전체: 지정 원장 맨 위(골라진 채) → 나머지 원장(시안 원장 순서)
  body.insertChild(1, doctorOpt31("1", "서연", "이서연 원장", "시술실 D 시술 중", true, "option/selected"));
  const rows = [
    doctorOpt31("1", "서연", "이서연 원장", "시술실 D 시술 중", true, "option/doctor-designated"),
    doctorOpt31("0", "도윤", "김도윤 원장", "시술실 A 시술 중", false, "option/doctor-1"),
    doctorOpt31("2", "하준", "박하준 원장", "비어 있음", false, "option/doctor-2"),
  ];
  for (const o of rows) body.appendChild(o);
  const foot = d.children.find((n) => n.name === "foot");
  const send = findIn(foot, "send");
  setText(send, "label", "호출");
  ctx.mark(1, rows[0]);
  ctx.mark(2, send);
  return box("VERTICAL", { name: "design", children: [d] });
});
