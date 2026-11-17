// ProcRow — 시안 `.proc3` 420–432 · 464 · 547–551 · 566–567 · 572–574 · `.proc-time` 433 · 553–555 · `.meta3` 428–429 · 468–469 · 507 · 516 · 551
//           템플릿 procRow3 · liveTime(1136–1172) · chartIcons(1468) · 데이터 state.orders(806~)
// 폭 256 · 여백 4 8(done 2 8) · 간격 6 · 면 white(menu = primary/100 · 567) · 모서리 0(566)
// 왼쪽: wait = Checkbox(default · checked) · 그 밖 = Checkbox off · done = st-done-gray 16. 체크박스 margin-left 1(138) → 왼쪽 여백 9
// 이름 14/400 lh1.5 black · margin-bottom -2(427 → 세로 간격 -2) / done = lh1.6 gray/700(549 · 취소선 없음) + 차트 아이콘(간격 2 · 574)
// 메타 12/400 lh1.3 간격 2: 원장 gray/700 + 상태(준비중 gray/700 · 호출 primary(551) · 늦은 호출 red(469) · 수락 · 진행중 primary(516))
// 시간 칸 12/400 gray/700 간격 2 + clock3-12(늦음 = red · 554–555) · 버튼 = Button xs(called 수락 · progress 종료 = outlined-black · ready 시작 = solid)
// more = IconButton more — menu 상태에서만 보임(439 · 443: 평소 폭 0)
// is-checked 면 테두리 = body.crm 에서 없음(503) → checked 는 체크박스만 다르다
function procRow(status, state) {
  const late = state === "late";
  const kids = [];
  if (status === "wait") kids.push(inst("Checkbox", { state: state === "checked" ? "checked" : "default" }, {}, "checkbox"));
  else if (status === "done") { const ic = icon("st-done-gray"); ic.name = "icon/status"; kids.push(ic); }
  else kids.push(inst("Checkbox", { state: "off" }, {}, "checkbox"));

  // 시간 칸(called · progress · done)
  const timeOf = (str) => box("HORIZONTAL", {
    name: "proc-time", gap: 2,
    children: [icon("clock3-12", late ? "red/DEFAULT" : undefined), text(str, "caption-md-400", late ? "red/DEFAULT" : "gray/700", { name: "label/time" })],
  });

  if (status === "done") {
    const chart = box("HORIZONTAL", { name: "chart-icons", gap: 2, children: [icon("chart-nurse-on"), icon("chart-doctor-on")] });
    kids.push(grow(box("HORIZONTAL", { name: "proc-name", gap: 6, children: [text("소프웨이브 200펄스", "body-400", "gray/700", { name: "label" }), chart] })));
    kids.push(timeOf("28분"));
  } else {
    const S = {
      wait: { name: "리투오 파인 2cc", who: null, st: "준비중", stc: "gray/700" },
      called: { name: "쥬베룩", who: "전체", st: "호출", stc: late ? "red/DEFAULT" : "primary/DEFAULT", time: late ? "6분" : "2분", btn: ["outlined-black", "수락"] },
      ready: { name: "울쎄라피 프라임 300 shot", who: "김도윤 원장", st: "수락", stc: "primary/DEFAULT", btn: ["solid", "시작"] },
      progress: { name: "써마지 900샷", who: "김도윤 원장", st: "진행중", stc: "primary/DEFAULT", time: "8분", btn: ["outlined-black", "종료"] },
    }[status];
    const meta = box("HORIZONTAL", {
      name: "meta", gap: 2,
      children: [S.who ? text(S.who, "caption-md-400", "gray/700", { name: "label/doctor" }) : null, text(S.st, "caption-md-400", S.stc, { name: "label/status" })],
    });
    const col = grow(box("VERTICAL", { name: "name-meta", gap: -2, justify: "CENTER", children: [text(S.name, "heading-sm-400", "black", { name: "label" }), meta] }));
    kids.push(col);
    if (S.time) kids.push(timeOf(S.time));
    if (S.btn) kids.push(inst("Button", { kind: S.btn[0], size: "xs" }, { label: S.btn[1] }, "button"));
  }
  if (state === "menu") kids.push(inst("IconButton", { icon: "more" }, {}, "more"));

  const done = status === "done";
  return box("HORIZONTAL", {
    name: "proc-row", w: 256, pl: done ? 8 : 9, pr: 8, py: done ? 2 : 4, gap: 6,
    bg: state === "menu" ? "primary/100" : "white",
    children: kids,
  });
}
const LIST = [["wait", "default"], ["wait", "checked"], ["called", "default"], ["called", "late"], ["ready", "default"], ["progress", "default"], ["progress", "menu"], ["done", "default"]];
const variants = LIST.map(([status, state]) => ({ props: { status, state }, node: procRow(status, state) }));
makeSet("ProcRow", variants, { perRow: 4, description: "시안 .proc3(procRow3) — 방 카드 안 시술 한 줄. wait 체크 · called(5분 넘으면 late 빨강) · ready 시작 · progress 종료(menu = 더보기 보임) · done 차트 아이콘 · 시간. 체크박스 · 버튼 · more 는 인스턴스." });
