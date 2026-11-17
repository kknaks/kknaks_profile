// Avatar — 시안 `.avatar` 328–331 · `body.crm .avatar.doctor` 473–475 · 템플릿 `docAvatar` 888 · `initials()` 886 · 원장 데이터 871
// 24×24 · r12 · doctor 10/500 lh1.3(13) · 테두리 1(box-sizing border-box = 안쪽) · none = 면 gray/300 + 테두리 gray/200 + `user` 16
const initials = (doctor) => doctor.replace(/ .*$/, "").slice(1, 3);
const TONES = [
  { tone: "0", name: "김도윤 원장", bg: "primary/100", fg: "primary/DEFAULT", bd: "crm/doctor-blue-border" },
  { tone: "1", name: "이서연 원장", bg: "purple/100", fg: "purple/DEFAULT", bd: "crm/doctor-purple-border" },
  { tone: "2", name: "박하준 원장", bg: "crm/doctor-green-100", fg: "crm/doctor-green", bd: "crm/doctor-green-border" },
];
const avatarVariants = TONES.map((t) => ({
  props: { kind: "doctor", tone: t.tone },
  node: box("HORIZONTAL", { name: "avatar", w: 24, h: 24, radius: 12, justify: "CENTER", bg: t.bg, border: t.bd, children: [text(initials(t.name), "meta-sm-500", t.fg)] }),
}));
avatarVariants.push({
  props: { kind: "none", tone: "none" },
  node: box("HORIZONTAL", { name: "avatar", w: 24, h: 24, radius: 12, justify: "CENTER", bg: "gray/300", border: "gray/200", children: [icon("user")] }),
});
makeSet("Avatar", avatarVariants, { perRow: 4, description: "시안 .avatar — 원장 이니셜(이름 첫 단어의 2~3번째 글자) · 원장 순서 % 3 = tone. none = 사람 아이콘." });
