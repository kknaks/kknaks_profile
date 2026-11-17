// ComboOption — 시안 `.combo-opt-m` 638–643 · 템플릿 `moveMenuHtml` 1386–1393 · CHECK16 1385 · 방 데이터 819–827
// 폭 200 · 높이 44 · 여백 11 16 · 간격 16 · 14/400 lh1.5 black(글자 칸 flex 1 · 말줄임)
// on = 면 primary/100 · 500 · primary(--text-brand) + check 16(currentColor = primary) · disabled = gray/600(--text-disabled)
const LIST = [
  ["default", "레이저실 3", [14, 400, 21], "black"],
  ["on", "시술실 F", [14, 500, 21], "primary/DEFAULT"],
  ["disabled", "시술실 B", [14, 400, 21], "gray/600"],
];
const variants = LIST.map(([state, str, typo, tk]) => {
  const label = grow(text(str, typo, tk, { name: "label" }));
  const kids = [label];
  if (state === "on") kids.push(icon("check", "primary/DEFAULT"));
  const node = box("HORIZONTAL", { name: "combo-option", w: 200, h: 44, pt: 11, pb: 11, pl: 16, pr: 16, gap: 16, align: "CENTER", bg: state === "on" ? "primary/100" : undefined, children: kids });
  label.textAutoResize = "HEIGHT";
  return { props: { state }, node };
});
makeSet("ComboOption", variants, { perRow: 3, description: "시안 .combo-opt-m(메디킷 ComboBox M 옵션) — 방 옮기기 목록 줄. on = 고른 방(primary/100 면 · 500 · 체크) · disabled = 사람이 있는 방 · 연결된 방." });
