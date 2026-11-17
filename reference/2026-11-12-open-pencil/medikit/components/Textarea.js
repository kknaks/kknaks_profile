// Textarea — 시안 .cm-ta 598–600(메디킷 Textarea) · 차트 모달 안 폭 378
// 최소 높이 90 · 여백 16 · 테두리 1 gray/300 · r8 · 면 white · 14/400 lh1.6 · placeholder gray/600 · focus 테두리 primary
const variants = ["default", "focus"].map((state) => {
  const label = stretch(text("내용을 입력해 주세요", "body-400", "gray/600", { name: "label" }));
  const f = box("VERTICAL", {
    name: "textarea", w: 378, h: 90, p: 16, radius: 8,
    bg: "white", border: state === "focus" ? "primary/DEFAULT" : "gray/300",
    children: [label],
  });
  label.textAutoResize = "HEIGHT";
  return { props: { state }, node: f };
});
makeSet("Textarea", variants, { perRow: 2, description: "시안 .cm-ta — 높이 90 에서 시작(최대 150 · 넘으면 칸 안 스크롤). focus = 테두리 primary" });
