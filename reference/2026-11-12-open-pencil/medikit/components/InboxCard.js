// InboxCard — 인박스 카드(현황 · 호출 · 시술 완료 탭). 시안 `.inbox-card` 268 → `body.crm .crm-card` 692(여백 0 · 간격 0) · `.card-head` 693–694 · `.card-body` 695
//   `.ib-line` 279 → 696–698 · `.ib-call` 530–531 · `.ib-doc .ok` 375 · 669 · `.ib-actions` 371 → 533(0 8 8 · margin-top -4) · `.card-list` 699 · chart-card 557–559 · `.dn-time` 519
//   active 492 · 501–502 · 672–673(테두리 1 + 바깥 3 번짐 primary 30% / red 20% · 그 위에 --shadow-card)
//   템플릿 a1Rows 951–961 · inboxCard 962–981 · renderCallsTab 1037–1053 · doneRoomCard 1433–1441 · 데이터 state 806–877 · IN_TIME 947
// 폭 256 · r6 · 테두리 1 gray/300(border-box → 안쪽 여백 1) · 면 white · 넘침 자름 · 그림자 0 2 4 6%
// 글자 자리: label = 방 이름(머리 첫 글자 · 머리 Badge 보다 앞이라 inst() 에서 먼저 잡힌다) · label/time(done-chart 머리) · label/customer · label/local · label/doctor · label/call
const RING = { primary: ["#1d8bff", 0.3, 0, 0, 0, 3], red: ["#ff4e51", 0.2, 0, 0, 0, 3] };

// 고객 줄: (user-round-12 · 검정) 이름 12/400 + 한글 12/500 gray/700. done-chart 는 아이콘 없이 이름 12/500
function customerLine(name, local, done) {
  return box("HORIZONTAL", {
    name: "customer-line", p: 2, gap: 4,
    children: [
      done ? null : icon("user-round-12", "black"),
      text(name, done ? "caption-md-500" : "caption-md-400", "black", { name: "label/customer" }),
      text(local, "caption-md-500", "gray/700", { name: "label/local" }),
    ],
  });
}
// 원장 줄: stethoscope(검정) + 원장 이름 + 상태(호출 +mm:ss gray/700 · 늦으면 red · 수락 primary)
function doctorLine(doctor, status, tone) {
  return box("HORIZONTAL", {
    name: "doctor-line", p: 2, gap: 4,
    children: [
      icon("stethoscope", "black"),
      text(doctor, "caption-md-400", "black", { name: "label/doctor" }),
      text(status, "caption-md-400", tone, { name: "label/call" }),
    ],
  });
}
function cardList(rows, gap) {
  const list = box("VERTICAL", { name: "card-list", gap, children: rows.map(([kind, label]) => inst("CardRow", { kind }, { label }, "card-row")) });
  for (const r of list.children) stretch(r);
  return list;
}
// d: { room | time, badge:[props,label], customer, local, done, procs:[[kind,label]], listGap, doctor:[name,status,tone], button:[props,label], bodyGap }
function card(d, state) {
  const headLabel = d.time
    ? text(d.time, "caption-md-400", "gray/700", { name: "label/time" })
    : text(d.room, "caption-md-500", "black", { name: "label" });
  const head = box("HORIZONTAL", {
    name: "card-head", pt: 4, pb: 4, pl: 8, pr: 8, gap: 4, bg: "crm/surface-head",
    children: [headLabel, d.badge ? inst("Badge", d.badge[0], { label: d.badge[1] }, "badge") : null],
  });
  grow(headLabel); headLabel.textAutoResize = "HEIGHT";
  const body = box("VERTICAL", {
    name: "card-body", pt: 8, pl: 8, pr: 8, pb: d.button ? 4 : 8, gap: d.bodyGap ?? 4,
    children: [
      customerLine(d.customer, d.local, d.done),
      d.procs ? cardList(d.procs, d.listGap ?? 2) : null,
      d.doctor ? doctorLine(...d.doctor) : null,
    ],
  });
  const actions = d.button
    ? box("HORIZONTAL", { name: "card-actions", pl: 8, pr: 8, pb: 8, gap: 8, children: [inst("Button", d.button[0], { label: d.button[1] }, "button")] })
    : null;
  const border = state === "active" ? "primary/DEFAULT" : state === "active-late" ? "red/DEFAULT" : "gray/300";
  const root = box("VERTICAL", { name: "inbox-card", w: 256, p: 1, radius: 6, bg: "white", border, clip: true, children: [head, body, actions] });
  for (const c of root.children) stretch(c);
  shadows(root, state === "active" ? [RING.primary, ...SHADOW_CARD] : state === "active-late" ? [RING.red, ...SHADOW_CARD] : SHADOW_CARD);
  return root;
}

// 샘플 = 시안 데이터
// 현황 · 시작 가능: 시술실 B(c2 · 마취 +12:00 · 호출 k3 김도윤 원장 수락)
const NOW = { room: "시술실 B", badge: [{ kind: "solid", color: "primary" }, "마취 +12:00"], customer: "[JP] HIROSE YUURI", local: "히로세 유우리", doctor: ["김도윤 원장", "수락", "primary/DEFAULT"] };
// 현황 · 확인 필요: 레이저실 2(c7 · 호출 k1 이서연 원장 6분 무응답 → 재호출)
const NOW_LATE = { room: "레이저실 2", customer: "[TW] HUANG WEI", local: "황웨이", doctor: ["이서연 원장", "호출 +06:00", "red/DEFAULT"], button: [{ kind: "outlined-gray", size: "ss", state: "default" }, "재호출"] };
// 호출 · 수락 대기: 시술실 C(c3 · 전체 호출 k5 · 쥬베룩)
const CALL_WAIT = { room: "시술실 C", customer: "[TW] LIN MEI", local: "린메이", procs: [["call-proc", "쥬베룩"]], doctor: ["전체 의사", "호출 +02:00", "gray/700"], button: [{ kind: "solid", size: "ss", state: "default" }, "수락"] };
// 호출 · 수락함: 시술실 B(c2 · k3 · 울쎄라피 프라임 300 shot · 김도윤 원장 수락)
const CALL_ACC = { room: "시술실 B", customer: "[JP] HIROSE YUURI", local: "히로세 유우리", procs: [["call-proc", "울쎄라피 프라임 300 shot"]], doctor: ["김도윤 원장", "수락", "primary/DEFAULT"] };
// 시술 완료: 입실 13:30(c1 · IN_TIME) – 귀가 대기 14:42 · 시술 줄 = c1 오늘 시술
const DONE = { time: "13:30-14:42", badge: [{ kind: "solid", color: "going-wait" }, "귀가 대기"], customer: "[TW] CHOU YU WEN", local: "저우위원", done: true, bodyGap: 6, listGap: 0, procs: [["proc-link", "소프웨이브 200펄스"], ["proc-link", "써마지 900샷"]] };

const LIST = [
  ["now", "default", NOW],
  ["now", "active", NOW],
  ["now-late", "active-late", NOW_LATE],
  ["call-wait", "default", CALL_WAIT],
  ["call-accepted", "default", CALL_ACC],
  ["done-chart", "default", DONE],
];
const variants = LIST.map(([kind, state, d]) => ({ props: { kind, state }, node: card(d, state) }));
makeSet("InboxCard", variants, { perRow: 3, description: "인박스 카드 — now(현황 · 방 이름 + 시간 Badge · 고객 · 원장 줄) · now-late(확인 필요 · 재호출) · call-wait(호출 탭 · 시술 목록 · 수락) · call-accepted(수락함) · done-chart(시술 완료 · 입실-귀가 시간 + 귀가 Badge · 시술 줄 = 차트). active = 테두리 primary + 바깥 3 번짐 30% / active-late = red + 20%. 시안 .inbox-card 268 · 663 · 692–704" });
