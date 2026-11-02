# [backend] interpret-pwa 대만어 사전 2차(D-38) — 시드만

너는 **interpret-pwa backend 워커**다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/backend/role.md` (+ rules · skills · tools · workflow)
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-seed-tw` (base origin/main fe8475e) · 커밋 · push 금지 · `.env` 없음(실물 호출은 키가 있으면 — 아래)

## SSOT
- DEC-001 **D-38**(+ D-33 · D-35 · D-37): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 조사 리포트(근거 · URL): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-seed-tw/research-tresure-report.md`(대만 클리닉 3곳 전수 · 표 A/B/C · §0 · §6) · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-seed-tw/research-kr-brands-report.md`(한국 톡신 대만 허가명) · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/_archive/interpret-pwa/interpret-pwa-poc/research-tw-names-report.md`(1차 · 찾지 못한 80)
- 시드: `back/seed/glossary.json` (version 2026-10-27.4) · 스키마 SPEC-001 §4.2

## 할 일 (back/seed/glossary.json · 관련 시험만)
1. 톡신: ph-031 레티보 · ph-042 보툴렉스 → zh-Hant name `保提拉` (alias Letybo · 白毒 · 輕齡肉毒 · 精品肉毒 · 樂提保) · ph-041 메디톡신 → `優力柔` (alias Neuronox · 粉毒 · 奇蹟肉毒 — 妙盾 제외) · ph-027 나보타 → `娜柏塔` (alias NABOTA · 彩虹肉毒 · 綠毒) · reviewed true(출처 2+) · source web-research 2026-10-27 · note URL
2. **대만에 없는 한국 전용 제품 = zh-Hant name 을 영문 브랜드명**(en entry 의 name 과 같은 값) — 1차 리포트 §4 「한국 전용 브랜드」 묶음 + 리즈톡스 · 코어톡스 · 신펄 · 더채움 · 엘라비에 · 리젠ACR 등. 기존 초안은 aliases 로 내리되 **s2twp 오변환(匯入 · 專案 · 裝置 · 鐳射)은 버린다** · reviewed false · note 「대만 클리닉 3곳에 중문명 없음」. 뉴럭스(ph-028)는 Neuronox 와 같은지 불명 — 건드리지 마라. 리쥬란이 사전에 있으면 zh-Hant alias 에 `麗珠蘭` 만(reviewed 그대로)
3. 대륙식 · 오변환 고침(name 교체 · 옛 표기는 alias 로 — 단 匯入 · 專案 · 裝置 오변환은 alias 에도 두지 않는다): ph-026 下頜線 → 下顎線 · ph-093 超聲波 → 超音波 · ph-096 離子匯入 → 離子導入 · ph-116 無細胞同種真皮 → 異體真皮 · ph-059 脂肪細胞破壞 → 去氧膽酸(alias 倍克脂) · ph-092 · ph-097 · ph-127 · ph-142 의 匯入/專案/裝置 → 導入/項目/設備(대만 표기 — 리포트에 더 맞는 말이 있으면 그것) · 1차 「찾지 못한 80」 중 남은 초안 전부를 **s2tw**(글자만)로 다시 만든 값으로 교체(DISPLAY_REPLACE 激光→雷射 포함 — to_display(zh-Hant) 재사용)
4. ph-126 슈링크유니버스 → name `海芙音波媚必提` (alias 海芙音波 · 媚必提 · Ultraformer MPT · Shurink Universe …) · ph-130 써마지FLX alias 에 `第四代電波拉皮` 추가(출처 museedunuage.com/鳳凰電波-thermage/) · ph-135 포텐자 alias 에 `無限電波`(출처 1)
5. **모호어 제거**: ph-121 울쎄라 zh-Hant aliases 에서 `音波拉提` 삭제(ph-131 HIFU name 으로만) · 리포트 표 C 의 말이 시드 어디에 alias 로 들어 있으면 지운다(鳳凰 단독 · 黃金微針 · 水光 류 통칭 · 素顏針/素妍針 혼동 · 熊貓 · 光纖) — 지운 목록을 리포트에
6. version 올리기(.5) · 시드 검사 · 시험(톡신 3 · 영문 브랜드 · 대륙식 0 · 匯入/專案/裝置/鐳射 zh-Hant 0 · 音波拉提 울쎄라 0) · ruff · pytest 전체
7. 실물(선택): 키가 있으면(`/Users/kknaks/git/toy_pr2/interpret-pwa/.env` 를 읽기만 — 값 출력 금지 · 복사 금지) zh-Hant 로 「我想打保提拉」「彩虹肉毒」→ 보툴렉스 · 나보타 1회. 없으면 pending
8. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-seed-tw/seed-tw-be-report.md` — 바꾼 term 목록(전 · 후) · 지운 alias · 시험 수치

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: 대만어 사전 2차" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] backend 대만어 사전 2차 완료 — <한 줄>" --enter`
