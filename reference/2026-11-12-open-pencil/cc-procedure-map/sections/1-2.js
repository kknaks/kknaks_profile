// 1-2 — 고객 검색(3 화면)
// DIFF: 헤더 틀은 세트에 없음 → custom/header(시안 .header 44 · 좌우 16 · 간격 24 · 오른쪽 tools 끝 정렬). 탭 = Tab header, 검색 칸 = Search ss(시안 헤더 고객 검색 200×28)
// DIFF: 시안에는 헤더 검색 결과 목록이 없음 → custom/search-results(시안 팝 스타일: 흰 면 · 테두리 gray/300 · r8 · SHADOW_POPOVER · 폭 360, 검색 칸 아래 오른쪽 정렬). 행 = 기획안 L196 고객 이름 · 국적 · 최근 방문일 · 관리실 · 시술 이름(구분은 시안 고객 줄 세로 막대)
// 샘플: 검색어 · 1행 = 기획안 예시(「유이」 → 「타나카 유이」 · 「일본」 · 「오늘」 · 시술 이름 예시 「써마지 FLX 300shot」 · 「아쿠아필 2회」 + 「외 1건」), 관리실 = 시안 방 「시술실 B」
//       2행 = 동명이인(기획안 정책 5) — 날짜 = 시안 페이지 날짜 「2026-10-26」 · 관리실 · 시술 = 시안 데이터 레이저실 1 · 레이저토닝
// 「검색 결과 없음」 화면의 검색어는 샘플이 없어 자리표시 「{검색어}」

function s12_bar(name) {
  const r = figma.createRectangle();
  r.name = name; r.resize(1, 10); fill(r, "gray/300");
  return r;
}
function s12_header(query) {
  const search = inst("Search", { size: "ss", state: "focus" }, {}, "search");
  const q = setText(search, "label", query);
  fill(q, "black");
  const tools = box("HORIZONTAL", { name: "tools", gap: 8, justify: "MAX", children: [search] });
  const head = box("HORIZONTAL", {
    name: "header", w: 520, h: 44, px: 16, gap: 24, bg: "white",
    children: [inst("Tab", { kind: "header", state: "active" }, {}, "tab"), tools],
  });
  grow(tools);
  return { head: custom("header", head), search };
}
function s12_panel(name, children) {
  const p = box("VERTICAL", { name, w: 360, py: 4, radius: 8, bg: "white", border: "gray/300", children });
  shadows(p, SHADOW_POPOVER);
  for (const c of p.children) stretch(c);
  const wrap = box("HORIZONTAL", { name: "panel-row", w: 520, pr: 16, justify: "MAX", children: [custom(name, p)] });
  return { panel: p, wrap };
}
// 결과 한 행: [이름 · 국적] / [최근 방문일 | 관리실 | 시술 이름 (외 n건)]
function s12_row(d, idx) {
  const procs = [text(d.procs, "caption-md-400", "gray/700", { name: "label/procedures" })];
  let more = null;
  if (d.more) { more = text(d.more, "caption-md-400", "gray/600", { name: "label/more" }); procs.push(more); }
  const row = box("VERTICAL", {
    name: `result-row-${idx}`, px: 12, py: 8, gap: 2,
    children: [
      box("HORIZONTAL", { name: "name-line", gap: 6, children: [text(d.name, "body-500", "black", { name: "label/name" }), text(d.nation, "caption-md-400", "gray/700", { name: "label/nationality" })] }),
      box("HORIZONTAL", {
        name: "visit-line", gap: 4,
        children: [
          text(d.visit, "caption-md-400", "gray/700", { name: "label/visit" }), s12_bar("bar"),
          text(d.room, "caption-md-400", "gray/700", { name: "label/room" }), s12_bar("bar-2"),
          box("HORIZONTAL", { name: "procedures", gap: 4, children: procs }),
        ],
      }),
    ],
  });
  return { row, more };
}

unit("procedure/search", (ctx) => {
  const { head, search } = s12_header("유이");
  ctx.mark(1, search);
  return box("VERTICAL", { name: "header-slice", w: 520, children: [head] });
});

unit("procedure/search/results", (ctx) => {
  const { head } = s12_header("유이");
  const r1 = s12_row({ name: "타나카 유이", nation: "일본", visit: "오늘", room: "시술실 B", procs: "써마지 FLX 300shot, 아쿠아필 2회", more: "외 1건" }, 1);
  const div = figma.createRectangle();
  div.name = "divider"; div.resize(360, 1); fill(div, "gray/200");
  const r2 = s12_row({ name: "타나카 유이", nation: "일본", visit: "2026-10-26", room: "레이저실 1", procs: "레이저토닝" }, 2);
  const { wrap } = s12_panel("search-results", [r1.row, div, r2.row]);
  ctx.mark(1, r1.row);
  ctx.mark(2, r1.more);
  return box("VERTICAL", { name: "header-with-results", w: 520, gap: 4, children: [head, wrap] });
});

unit("procedure/search/empty", (ctx) => {
  const { head } = s12_header("{검색어}");
  const msg = text("검색 결과 없음", "body-400", "gray/600", { name: "label", align: "CENTER" });
  const body = box("HORIZONTAL", { name: "empty", py: 16, justify: "CENTER", children: [msg] });
  const { wrap } = s12_panel("search-results-empty", [body]);
  ctx.mark(1, msg);
  return box("VERTICAL", { name: "header-with-empty", w: 520, gap: 4, children: [head, wrap] });
});
