// Badge — 시안 `.cbadge` 176–182 · 200–205 · `body.crm .cbadge.solid.gray` 665 · `.cbadge.going-wait` 556 · 템플릿 `cbadge()` 949 · `anesChip` 1184–1187 · `doneRoomCard` 1438
// 여백 3 6 · r6 · 11/500 lh1.273(14) · 자간 0.34 · solid 면 = 글자색 8% 의 흰 바탕 합성 단색(status/*-8) · outline = 면 없음 + 테두리 1 글자색 43%
const BADGE = [
  { kind: "solid", color: "primary", label: "마취 +12:00", fg: "primary/DEFAULT", bg: "status/badge-primary-8" },
  { kind: "solid", color: "red", label: "마취 +23:00", fg: "red/DEFAULT", bg: "status/badge-red-8" },
  { kind: "solid", color: "gray", label: "마취 완료 21분", fg: "gray/700", bg: "status/badge-gray-8" },
  { kind: "outline", color: "primary", label: "마취 시작", fg: "primary/DEFAULT" },
  { kind: "solid", color: "going-wait", label: "귀가 대기", fg: "status/going-wait", bg: "status/going-wait-8" },
];
const badgeVariants = BADGE.map((b) => {
  const o = { name: "badge", pt: 3, pb: 3, pl: 6, pr: 6, radius: 6 };
  if (b.bg) { o.bg = b.bg; }  // 8% 를 흰 바탕에 합성한 불투명 단색 변수(코디 2026-11-12)
  else { o.border = b.fg; o.borderA = 0.43; }
  const n = box("HORIZONTAL", { ...o, children: [text(b.label, "badge-11", b.fg, { ls: 0.34 })] });
  return { props: { kind: b.kind, color: b.color }, node: n };
});
makeSet("Badge", badgeVariants, { perRow: 5, description: "시안 .cbadge — 마취 시간 · 마취 시작 · 귀가 대기 꼬리표. solid 면 = 글자색 8% 합성 단색, outline 테두리 = 글자색 43%." });
