// ConfirmDialog — 시안 `.cm-confirm > div` 610 · h3 611 · p 612 · .cm-foot 613 · 템플릿 `chartModalHtml` 1290–1291 · `renderConfirm` 1396–1402
// 폭 280 · 여백 20 · r14 · 면 white · 그림자 SHADOW_FLOAT
// 제목 16/500 lh1.5 black · 본문 14/400 lh1.6 gray/700(위 4) · 발 위 20 · 간격 8 · 오른쪽: Button m-dialog outlined-gray 「취소」 + solid 「닫기」
const titleT = text("저장하지 않고 닫을까요?", "heading-md-500", "black", { name: "label" });
const bodyT = text("쓴 내용은 사라져요.", "body-400", "gray/700", { name: "label/body" });
const bodyRow = box("VERTICAL", { name: "body", pt: 4, children: [bodyT] });
const foot = box("HORIZONTAL", {
  name: "foot", pt: 20, gap: 8, justify: "MAX",
  children: [inst("Button", { kind: "outlined-gray", size: "m-dialog" }, { label: "취소" }, "cancel"), inst("Button", { kind: "solid", size: "m-dialog" }, { label: "닫기" }, "confirm")],
});
const dlg = box("VERTICAL", { name: "confirm-dialog", w: 280, p: 20, radius: 14, bg: "white", children: [titleT, bodyRow, foot] });
for (const n of [titleT, bodyRow, foot, bodyT]) n.layoutAlign = "STRETCH";
titleT.textAutoResize = "HEIGHT"; bodyT.textAutoResize = "HEIGHT";
shadows(dlg, SHADOW_FLOAT);
makeSet("ConfirmDialog", [{ props: { state: "default" }, node: dlg }], { description: "시안 .cm-confirm — 확인 창. 차트를 저장 않고 닫을 때 · 진행중 시술이 있는 방 옮기기 · 연결 풀기(renderConfirm: 제목 · 본문(없을 수 있음) · 「취소」 + 확인 문구)." });
