// PopOption — 시안 `.pop-opt` 234–244 · 템플릿 `recallPopHtml` 1066–1088 · `doctorStatus` 895 · 원장 데이터 871
// 폭 224(.pop 240 − .pop-body 여백 8×2) · 높이 32 · 여백 0 6 · 간격 6 · r6 · Avatar 24
// 이름 b 12/500 black · 보조 .pop-sub 10/400 gray/700(--text-tertiary · 말줄임) · 꼬리표 em 10/500 primary(margin-left auto → 보조가 남는 폭을 먹는다)
// on = 면 primary/100 · 이름 primary. 줄높이 = normal(Pretendard ≈ ×1.193 반올림: 12→14 · 10→12, Notify 와 같은 셈)
// 보조 글자 = doctorStatus 꼴(「<방> 시술 중」 · 「<방> 시작 대기」 · 「비어 있음」) · 꼬리표 = 「처음 호출」(recall) · 「호출」(accept)
const LIST = [
  { kind: "doctor", state: "default", tone: "0", name: "김도윤 원장", sub: "레이저실 1 시술 중", tag: null },
  { kind: "doctor", state: "on", tone: "1", name: "이서연 원장", sub: "시술실 D 시술 중", tag: "처음 호출" },
  { kind: "all", state: "default", tone: null, name: "전체 호출", sub: null, tag: null },
];
const variants = LIST.map((o) => {
  const on = o.state === "on";
  const kids = [
    o.kind === "all" ? inst("Avatar", { kind: "none" }, {}, "avatar") : inst("Avatar", { kind: "doctor", tone: o.tone }, {}, "avatar"),
    text(o.name, [12, 500, 14], on ? "primary/DEFAULT" : "black", { name: "label" }),
  ];
  let sub = null;
  if (o.sub) { sub = grow(text(o.sub, [10, 400, 12], "gray/700", { name: "label/sub" })); kids.push(sub); }
  if (o.tag) kids.push(text(o.tag, [10, 500, 12], "primary/DEFAULT", { name: "label/tag" }));
  const node = box("HORIZONTAL", { name: "pop-option", w: 224, h: 32, px: 6, gap: 6, radius: 6, align: "CENTER", bg: on ? "primary/100" : undefined, children: kids });
  if (sub) sub.textAutoResize = "HEIGHT";
  return { props: { kind: o.kind, state: o.state }, node };
});
makeSet("PopOption", variants, { perRow: 3, description: "시안 .pop-opt — 재호출 · 수락할 원장 창의 원장 줄. 보조 = doctorStatus(「<방> 시술 중」 등) · 꼬리표 = 「처음 호출」/「호출」. on = 고른 줄(primary/100 면 · 이름 primary). all = 전체 호출(사람 아이콘)." });
