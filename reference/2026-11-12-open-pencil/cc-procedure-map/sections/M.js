// M CC 모바일 — 화면 3: call-accept(의사 호출 알림 · 「수락」) · toast/taken · toast/canceled
// 시안에 CC 모바일 없음 → 시안 「호출」 탭 카드(renderCallsTab 1034 · InboxCard call-wait)를 모바일 폭 375(custom/mobile-frame)에 놓는다
// 알림 값(기획안 L460) = 관리실 · 한국어 발음 · 시술 · 지정 · 전체 호출. 샘플 = 시안 calls k5(시술실 C · 린메이 · 쥬베룩 · 전체 호출 · 2분) · k4(레이저실 2 · 황웨이 · 보톡스 이마 · 박하준 원장 지정 · 2분)
// DIFF: 시안 원장 줄 「전체 의사」 ↔ 기획안 「전체 호출」 → 기획안 문구. 지정 호출은 시안대로 원장 이름(「지정」 글자는 따로 두지 않음)
// DIFF: 「수락」 기획안 style solid/blue/l ↔ 시안 카드 Button solid ss → 카드를 떼어(detach) Button solid l 꽉 채움으로 바꿈
// DIFF: 토스트 기획안 style error ↔ Notify 세트는 성공(체크 아이콘 · primary 글자) 하나뿐 → 체크 아이콘을 숨기고 글자만. error 모양 변형은 세트에 없음
// 비움: 모바일 화면 제목 · 상단 바(기획안에 문구 없음)

function mFrame(h, kids, o = {}) {
  return custom("mobile-frame", box("VERTICAL", { w: 375, h, p: 16, gap: 12, bg: "gray/100", clip: true, ...o, children: kids }));
}
function mCallCard(room, name, local, proc, doctor, call, cardName) {
  const c = inst2("InboxCard", { kind: "call-wait" }, { label: [room, proc], "label/customer": name, "label/local": local, "label/doctor": doctor, "label/call": call }, cardName);
  const d = detach(c, cardName);
  d.resize(351, d.height);
  const actions = findIn(d, "card-actions");
  for (const k of [...actions.children]) k.remove();
  const accept = inst2("Button", { kind: "solid", size: "l" }, { label: "수락" }, "button/accept");
  actions.appendChild(accept);
  grow(accept);
  d.primaryAxisSizingMode = "AUTO"; // resize 뒤 높이가 l 버튼(44)에 맞게 다시 늘도록
  return { card: d, accept };
}

unit("mobile/call-accept", (ctx) => {
  const a = mCallCard("시술실 C", "[TW] LIN MEI", "린메이", "쥬베룩", "전체 호출", "호출 +02:00", "mobile-call-card");
  const b = mCallCard("레이저실 2", "[TW] HUANG WEI", "황웨이", "보톡스 이마", "박하준 원장", "호출 +02:00", "mobile-call-card");
  ctx.mark(1, a.card); ctx.mark(2, a.accept);
  return mFrame(420, [a.card, b.card], { p: 12, gap: 8 }); // 카드 190 × 2 + 8 + 24 = 412
});

function mToast(ctx, msg) {
  const n = inst2("Notify", { state: "default" }, { label: msg }, "notify");
  hideIn(n, "icon/notify-check");
  ctx.mark(1, n);
  return mFrame(120, [n], { align: "CENTER", justify: "CENTER" });
}
unit("mobile/toast/taken", (ctx) => mToast(ctx, "다른 원장이 먼저 받았습니다"));
unit("mobile/toast/canceled", (ctx) => mToast(ctx, "취소된 호출입니다"));
