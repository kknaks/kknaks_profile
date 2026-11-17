// ChartModal — 시안 `.cm-box` 582–607 · 템플릿 `chartModalHtml` 1272–1292 · `openChart` 1268 · 제목 1609(이름에서 [국가] 떼고 + 현지 이름)
// 폭 410 · r14 · 면 white · 그림자 SHADOW_FLOAT · 최대 높이 min(640, 100dvh − 48)
// 머리 여백 14 · 간격 10 · 위 정렬 · 제목 18/500 lh1.5 black(꽉 · 말줄임) + IconButton close-24
// 탭 줄 여백 8 16 · 간격 16 · Tab modal / 섹션 여백 12 16 · 간격 4: 머리(간격 4) = 시술 이름 14/400 lh1.5 + 메타(pencil-12 · 쓴 사람 · 막대 1×10 gray/300 · 「시각 수정|작성」 12 lh1.3 gray/700, 간격 4) + Textarea
// 발 여백 8 16 · 간격 8 · 오른쪽: 「Ctrl + Enter」 14 lh1.6 gray/700 + Button l solid 「저장」
// 샘플 = c1 [TW] CHOU YU WEN(저우위원) 시술 o1 · o2 · 간호사 NURSE_NAME 1459
function section(name, meta) {
  const headKids = [grow(text(name, [14, 400, 21], "black", { name: "label/procedure" }))];
  if (meta) {
    const bar = figma.createRectangle();
    bar.name = "meta-bar"; bar.resize(1, 10); fill(bar, "gray/300");
    headKids.push(box("HORIZONTAL", {
      name: "meta", gap: 4,
      children: [icon("pencil-12"), text(meta[0], "caption-md-400", "gray/700", { name: "label/by" }), bar, text(meta[1], "caption-md-400", "gray/700", { name: "label/time" })],
    }));
  }
  const head = box("HORIZONTAL", { name: "section-head", gap: 4, children: headKids });
  head.layoutAlign = "STRETCH";
  headKids[0].textAutoResize = "HEIGHT";
  const ta = inst("Textarea", { state: "default" }, {}, "textarea");
  ta.layoutAlign = "STRETCH";
  const sec = box("VERTICAL", { name: "proc-section", pt: 12, pb: 12, pl: 16, pr: 16, gap: 4, children: [head, ta] });
  sec.layoutAlign = "STRETCH";
  return sec;
}
const title = grow(text("CHOU YU WEN 저우위원", "title-sm-500", "black", { name: "label" }));
const head = box("HORIZONTAL", { name: "head", p: 14, gap: 10, align: "MIN", children: [title, inst("IconButton", { icon: "close-24" }, {}, "close")] });
head.layoutAlign = "STRETCH";
title.textAutoResize = "HEIGHT";
const tabs = box("HORIZONTAL", {
  name: "tabs", pt: 8, pb: 8, pl: 16, pr: 16, gap: 16, align: "MIN",
  children: [inst("Tab", { kind: "modal", state: "active" }, { label: "간호 관리 차트" }, "tab/nurse"), inst("Tab", { kind: "modal", state: "default" }, { label: "의사 차트" }, "tab/doctor")],
});
const body = box("VERTICAL", { name: "body", children: [section("소프웨이브 200펄스", ["정하늘 간호사", "14:36 수정"]), section("써마지 900샷", null)] });
body.layoutAlign = "STRETCH";
const foot = box("HORIZONTAL", {
  name: "foot", pt: 8, pb: 8, pl: 16, pr: 16, gap: 8, justify: "MAX",
  children: [text("Ctrl + Enter", "body-400", "gray/700", { name: "shortcut" }), inst("Button", { kind: "solid", size: "l", state: "default" }, { label: "저장" }, "save")],
});
foot.layoutAlign = "STRETCH";
const modal = box("VERTICAL", { name: "chart-modal", w: 410, radius: 14, bg: "white", clip: true, children: [head, tabs, body, foot] });
shadows(modal, SHADOW_FLOAT);
makeSet("ChartModal", [{ props: { state: "default" }, node: modal }], { description: "시안 .cm-box — 시술 차트 창(간호 관리 차트 / 의사 차트). 섹션 = 고객의 시술마다 · 메타 = 마지막으로 쓴 사람 · 시각(없으면 비움). 저장 = Ctrl + Enter." });
