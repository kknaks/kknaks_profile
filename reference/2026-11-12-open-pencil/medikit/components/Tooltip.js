// Tooltip — 시안 `.ftip` 576 · `.ftip::before` 652 · `[data-tip]` 186–195 · 문구 1214 `data-ftip="방 옮기기"`
// 여백 5 8 · r6 · 최소 폭 36 · 면 hover-dark 70% · 글자 white 12/500 · 꼬리 14×6 위 가운데(clip-path 삼각형, 면 inherit)
const tail = figma.createVector();
tail.vectorPaths = [{ windingRule: "NONZERO", data: "M 7 0 L 14 6 L 0 6 Z" }];
tail.resize(14, 6);
tail.name = "tail";
tail.strokes = [];
fill(tail, "hover-dark", 0.7);
const tipBody = box("HORIZONTAL", { name: "body", pt: 5, pb: 5, pl: 8, pr: 8, radius: 6, justify: "CENTER", bg: "hover-dark", bgA: 0.7, children: [text("방 옮기기", "caption-md-500", "white", { align: "CENTER" })] });
tipBody.minWidth = 36;
const tip = box("VERTICAL", { name: "tooltip", align: "CENTER", children: [tail, tipBody] });
makeSet("Tooltip", [{ props: { state: "default" }, node: tip }], { description: "시안 .ftip · [data-tip] — 아이콘 버튼 아래에 뜨는 안내. 꼬리는 위 가운데." });
