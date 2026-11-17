// InboxSectionHead — 인박스 묶음 머리(접기 버튼). 시안 `.ib-head` 261–264 → `body.crm .ib-head` 709 · 템플릿 renderSide4 984–989 · renderCallsTab 1054–1057
// 폭 256(인박스 카드 폭) · 최소 22 · 간격 5 · 아이콘 16 + 제목 14/500 lh1.6 gray/800(--text-secondary · flex 1) + chevron-down-20c 20
// none = 호출 탭 머리(아이콘 없음 · 「제목 개수」)
const HEADS = [
  ["late", "warn-fill", "확인 필요"],
  ["going", "circle-check-brand", "시작 가능"],
  ["wait", "circle-minus", "시술 대기"],
  ["none", null, "수락 대기 2"],
];
const variants = HEADS.map(([key, ic, title]) => {
  const label = text(title, "body-500", "gray/800", { name: "label" });
  const chev = icon("chevron-down-20c");
  chev.name = "icon/chevron";
  const head = box("HORIZONTAL", { name: "ib-head", w: 256, gap: 5, children: [ic ? icon(ic) : null, label, chev] });
  grow(label); label.textAutoResize = "HEIGHT";
  return { props: { icon: key }, node: head };
});
makeSet("InboxSectionHead", variants, { perRow: 2, description: "인박스 묶음 머리 — late 확인 필요 · going 시작 가능 · wait 시술 대기(현황 탭) · none 호출 탭(「수락 대기 N」). 오른쪽 chevron(접히면 -90° 회전). 시안 .ib-head 261 · 709" });
