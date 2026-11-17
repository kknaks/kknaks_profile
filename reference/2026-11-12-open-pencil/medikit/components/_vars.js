// 실측(2026-11-12): 직렬 실행이면 1초. 병렬 eval 중엔 100초 넘게 걸리고 앱 eval 이 고장 났다 — eval 은 한 번에 하나만.
// 시안에만 있는 색을 컬렉션 medikit 에 추가(있으면 값만 맞춤 · 기존 29개는 건드리지 않음). _lib.js 보다 먼저, 단독으로 실행.
// 출처: 시안 :root --st-*(고객 상태색 · 접수 = primary 라 뺌) · body.crm --surface-head · .cbadge.solid.gray · .avatar.doctor.tone-*
const NEW_VARS = {
  "status/consult-wait": "#6c34cb", "status/consult-wait-100": "#f5f1fb", "status/consult-wait-300": "#e7dff7", "status/consult-wait-500": "#bda4e8",
  "status/consult": "#de4694", "status/consult-100": "#fdf2f8", "status/consult-300": "#fae1ee", "status/consult-500": "#f0accf",
  "status/proc-wait": "#4dbec1", "status/proc-wait-100": "#f3fafb", "status/proc-wait-300": "#e3f5f5", "status/proc-wait-500": "#afe2e3",
  "status/proc": "#f6ae53", "status/proc-100": "#fef9f3", "status/proc-300": "#fef2e3", "status/proc-500": "#fbdbb2",
  "status/going-wait": "#6ac13b", "status/going-wait-100": "#f5fbf1", "status/going-wait-300": "#e7f5e0", "status/going-wait-500": "#bce3a7",
  "status/gone": "#8c8c8c", "status/gone-100": "#f7f7f7", "status/gone-300": "#ededed", "status/gone-500": "#cbcbcb",
  // Badge solid 면 = 글자색 8% 를 흰 바탕에 합성한 불투명 단색(린트가 칠 불투명도를 무시해 1.00:1 거짓 대비를 내서 — 코디 2026-11-12)
  "status/badge-primary-8": "#edf6ff", "status/badge-red-8": "#fff1f1", "status/badge-gray-8": "#f4f4f5", "status/going-wait-8": "#f3faef",
  "crm/surface-head": "#f7f7f8", "crm/badge-gray": "#70737c",
  "crm/doctor-blue-border": "#e3f0ff", "crm/doctor-purple-border": "#eedcff",
  "crm/doctor-green": "#5aa832", "crm/doctor-green-100": "#eef8e7", "crm/doctor-green-border": "#dcf0cd",
};
const col = figma.getLocalVariableCollections().find((c) => c.name === "medikit");
if (!col) throw new Error("컬렉션 medikit 없음 — import-medikit.js 먼저");
const have = {}; for (const v of figma.getLocalVariables()) have[v.name] = v;
const toC = (h) => ({ r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255, a: 1 });
const out = { created: 0, kept: 0 };
for (const [name, hex] of Object.entries(NEW_VARS)) {
  if (have[name]) {
    const cur = have[name].valuesByMode?.[col.modes[0].modeId];
    const same = cur && ["r", "g", "b"].every((k) => Math.round(cur[k] * 255) === Math.round(toC(hex)[k] * 255));
    if (!same) figma.setVariableValue(have[name].id, col.modes[0].modeId, toC(hex));
    out.kept++;
  }
  else { figma.createVariable(name, "COLOR", col.id, toC(hex)); out.created++; }
}
out.total = figma.getLocalVariables().length;
out;
