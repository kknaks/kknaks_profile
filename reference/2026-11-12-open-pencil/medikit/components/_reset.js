// 「components」 페이지를 비우고 다시 쓴다(멱등). 페이지 자체는 지우지 않는다 — 앱이 보고 있는 페이지를 지우면
// CLI 의 현재 페이지가 사라진 id 로 남아 eval 이 전부 실패한다(2026-11-12 실측). 다른 페이지는 건드리지 않는다.
let pg = figma.root.children.find((p) => p.name === "components");
if (!pg) { pg = figma.createPage(); pg.name = "components"; }
for (const c of [...pg.children]) c.remove();
pg.backgrounds = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: 1 }];
"reset";
