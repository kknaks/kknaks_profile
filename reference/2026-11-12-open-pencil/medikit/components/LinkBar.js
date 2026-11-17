// LinkBar — 시안 `.link-bar` 620–624 · 템플릿 linkBar(1366) · 데이터 state.rooms(시술실 A)
// 옮겨 간 방 카드의 제목 아래 띠: 「원래 방」 + [연결 풀기] [돌아가기]
// 폭 256 · 여백 1 8 · 간격 6 · 면 --st-reception = primary · link-2-white-16 · 방 이름 12/500 lh1.3 white(flex 1)
// 버튼(.link-bar button 623 — Button 세트에 없는 모양이라 여기서 그림): 여백 2 4 · r4 · 면 primary · 12/500 lh1.3 white
const barBtn = (str, role) => box("HORIZONTAL", {
  name: `button-${role}`, pt: 2, pb: 2, pl: 4, pr: 4, radius: 4, bg: "primary/DEFAULT",
  children: [text(str, "caption-md-500", "white", { name: `label/${role}` })],
});
const roomName = grow(text("시술실 A", "caption-md-500", "white", { name: "label" }));
roomName.textAutoResize = "HEIGHT";
const linkIcon = icon("link-2-white-16");
linkIcon.name = "icon/link";
const bar = box("HORIZONTAL", {
  name: "link-bar", w: 256, pt: 1, pb: 1, pl: 8, pr: 8, gap: 6, bg: "primary/DEFAULT",
  children: [linkIcon, roomName, barBtn("연결 풀기", "release"), barBtn("돌아가기", "return")],
});
makeSet("LinkBar", [{ props: { state: "default" }, node: bar }], { description: "시안 .link-bar — 방을 옮긴 고객 카드 제목 아래. label = 원래 방 이름, label/release 「연결 풀기」 · label/return 「돌아가기」(작은 버튼은 이 띠 전용)." });
