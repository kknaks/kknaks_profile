// Notify — 시안 `.notify` 287–289 · `crmNotify` 739–751 · 문구 1330 「저장되었어요」
// 알약 r100 · 여백 14 16 · 간격 8 · 면 white · 그림자 0 1 6 rgba(29,139,255,.3) · 13/500 primary · 아이콘 18(primary 원 + 흰 체크)
const note = box("HORIZONTAL", { name: "notify", pt: 14, pb: 14, pl: 16, pr: 16, gap: 8, radius: 100, bg: "white", children: [icon("notify-check"), text("저장되었어요", "notify-13", "primary/DEFAULT")] });
shadows(note, [["#1d8bff", 0.3, 0, 1, 6, 0]]);
makeSet("Notify", [{ props: { state: "default" }, node: note }], { description: "시안 .notify(메디킷 Notify) — 저장 등 완료 알림. 화면 위 가운데에 2초." });
