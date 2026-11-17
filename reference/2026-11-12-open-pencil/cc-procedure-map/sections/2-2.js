// 2-2 마취 — 화면 2
// DIFF: 시안 마취 = 방 머리 오른쪽 배지 하나(「마취 시작」 → 「마취 +00:00」(누르면 끝) → 「마취 완료 00분」) ↔ 기획안 「마취 시작」 · 「마취중 mm:ss」 · 「마취 종료」(L365–366). 문구 · 요소는 기획안, 모양은 시안 Badge(outline primary · solid primary). 「마취 종료」는 시안에 따로 없어 Button outlined-gray ss 로 배지 옆에 더함(기획안 style outlined/gray/ss)
// DIFF: 기획안 「마취 시작」 style = outlined/blue/ss 버튼 ↔ 시안 Badge outline primary — 시안 배지 모양을 따름
// DIFF: running 제목 줄 높이 = 시안 31 고정 → 「마취 종료」 버튼(ss 28)이 들어가게 높이 맞춤(약 38)
// DIFF: 시안 「마취 완료 21분」(끝난 회차 배지)은 기획안에 없음 — 기획안은 「마취 종료」 뒤 「마취 시작」으로 돌아간다(L364) → 그리지 않음
// DIFF: 고객 줄 「입실 13:30」 = 결정 「입실을 빼고 국적」 — 국적 샘플 값이 시안에 없어 칸을 그리지 않음(결정: 값 없으면 칸 안 그림)
// 조각 = RoomCard default 를 떼어 제목 줄 + 고객 줄만 남김(메모 · 시술 목록 숨김)

function anesCardFragment(name) {
  const d = detach(inst("RoomCard", { state: "default" }, {}, "room-card"), name);
  const body = findIn(d, "room-body");
  body.layoutGrow = 0;
  for (const nm of ["memo", "proc-lists"]) findIn(body, nm).remove();   // 떼어 낸 프레임이라 지운다(숨기면 높이 448 이 남는다 · 리드 실행 확인)
  findIn(d, "label/in").remove();
  findIn(d, "bar-2").remove();
  body.primaryAxisSizingMode = "AUTO";
  d.primaryAxisSizingMode = "AUTO";
  const title = findIn(d, "room-title");
  const old = findIn(title, "anes-badge");
  if (old) old.remove();
  return { d, title };
}
// 고정 높이가 남으면 제목 줄 + 몸 높이로 맞춘다
function fitCard(d) { const h = d.children.reduce((a, c) => a + c.height, 0); d.resize(d.width, Math.ceil(h)); return d; }

unit("procedure/customer-card/anesthesia-idle", (ctx) => {
  const { d, title } = anesCardFragment("room-card-anesthesia-idle");
  const badge = inst2("Badge", { kind: "outline", color: "primary" }, { label: "마취 시작" }, "anes-badge");
  title.appendChild(badge);
  ctx.mark(1, badge);
  return box("VERTICAL", { name: "design", children: [fitCard(d)] });
});

unit("procedure/customer-card/anesthesia-running", (ctx) => {
  const { d, title } = anesCardFragment("room-card-anesthesia-running");
  title.counterAxisSizingMode = "AUTO";
  const badge = inst2("Badge", { kind: "solid", color: "primary" }, { label: "마취중 12:00" }, "anes-badge");
  const end = inst2("Button", { kind: "outlined-gray", size: "ss" }, { label: "마취 종료" }, "anes-end");
  title.appendChild(box("HORIZONTAL", { name: "anes", gap: 4, children: [badge, end] }));
  ctx.mark(1, badge);
  ctx.mark(2, end);
  return box("VERTICAL", { name: "design", children: [fitCard(d)] });
});
