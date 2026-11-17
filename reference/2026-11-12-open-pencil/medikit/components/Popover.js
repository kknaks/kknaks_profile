// Popover — 시안 `.pop` 219–245 · 템플릿 `recallPopHtml` 1066–1088 · 호출 1630(accept) · 1634(recall)
// 폭 240 · r8 · 면 white · 그림자 0 0 4 #cfcfcf(SHADOW_POPOVER) · 최대 높이 380
// 머리 여백 10 12 · 양끝 정렬 · 아래 선 1 gray/200 · 제목 14/600 lh1.5 · 닫기 = IconButton close
// 검색 여백 8 8 0 · Search m-left / 몸 여백 0 8 6 · 라벨 10/500 lh1.3 gray/600 여백 8 4 4 · PopOption 들 / 발 여백 8 · 위 선 1 gray/200 · Button s solid 꽉
// 줄: 선택됨 = 고른 원장(on) · 전체 = (recall 만) 전체 호출 + 원장 순서대로(고른 원장은 전체에서도 on · 꼬리표 그대로). 원장 2줄만 넣는다
function divider(name) {
  const r = figma.createRectangle();
  r.name = name; r.resize(240, 1);
  fill(r, "gray/200");
  r.layoutAlign = "STRETCH";
  return r;
}
function sectionLabel(str) {
  return box("HORIZONTAL", { name: "section-label", pt: 8, pb: 4, pl: 4, pr: 4, children: [text(str, "meta-sm-500", "gray/600", { name: "heading" })] });
}
const MODE = {
  recall: { title: "재호출", tag: "처음 호출", all: true, send: "재호출" },
  accept: { title: "수락할 원장", tag: "호출", all: false, send: "수락" },
};
const variants = ["recall", "accept"].map((mode) => {
  const m = MODE[mode];
  const picked = (nm) => inst("PopOption", { kind: "doctor", state: "on" }, { "label/tag": m.tag }, nm);
  const head = box("HORIZONTAL", {
    name: "head", pt: 10, pb: 10, pl: 12, pr: 12, justify: "SPACE_BETWEEN",
    children: [text(m.title, "heading-sm-600", "black", { name: "label" }), inst("IconButton", { icon: "close" }, {}, "close")],
  });
  head.layoutAlign = "STRETCH";
  const search = box("VERTICAL", { name: "search-row", pt: 8, pl: 8, pr: 8, children: [inst("Search", { size: "m-left", state: "default" }, {}, "search")] });
  const rows = [sectionLabel("선택됨"), picked("option/selected"), sectionLabel("전체")];
  if (m.all) rows.push(inst("PopOption", { kind: "all", state: "default" }, {}, "option/all"));
  rows.push(inst("PopOption", { kind: "doctor", state: "default" }, {}, "option/doctor"));
  rows.push(picked("option/doctor-selected"));
  const body = box("VERTICAL", { name: "body", pl: 8, pr: 8, pb: 6, children: rows });
  const btn = inst("Button", { kind: "solid", size: "s", state: "default" }, { label: m.send }, "send");
  const foot = box("VERTICAL", { name: "foot", p: 8, children: [btn] });
  foot.layoutAlign = "STRETCH";
  btn.layoutAlign = "STRETCH";
  const node = box("VERTICAL", { name: "popover", w: 240, radius: 8, bg: "white", clip: true, children: [head, divider("head-line"), search, body, divider("foot-line"), foot] });
  shadows(node, SHADOW_POPOVER);
  return { props: { mode }, node };
});
makeSet("Popover", variants, { perRow: 2, description: "시안 .pop — recall = 재호출(전체 호출 줄 있음 · 꼬리표 「처음 호출」 · 발 「재호출」) · accept = 수락할 원장(전체 호출 줄 없음 · 꼬리표 「호출」 · 발 「수락」). 최대 높이 380 · 넘으면 몸 스크롤." });
