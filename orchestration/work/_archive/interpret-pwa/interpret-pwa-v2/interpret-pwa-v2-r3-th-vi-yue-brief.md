# [researcher] 새 시술 — 태국어 · 베트남어 · 광둥어(홍콩)

너는 **interpret-pwa researcher 워커**다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/researcher/role.md` (+ rules · skills · tools · workflow). **read-only** — 리포트 1개만. 커밋 금지.

## SSOT
- DEC-001 **D-39 · D-40**(+ 규칙 D-35 · D-38): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 사전(배포본 · read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/seed-2026-10-27.5.json` (157 term × en · ja · zh · zh-Hant · th · vi · yue)
- 앞 조사(방법 · 규칙 선례): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/_archive/interpret-pwa/interpret-pwa-seed-tw/research-tresure-report.md`(대만 3곳 · 표 B = 새 후보) · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/_archive/interpret-pwa/interpret-pwa-seed-tw/research-kr-brands-report.md`
- 추가 후보 시술: 써마지 CPT(Thermage CPT) · 소프웨이브(Sofwave) · 엑시온(Exion) · 덴서티(Density) · 엠페이스(EMFACE) · 클리어앤브릴리언트(Clear+Brilliant) · 쥬베룩(Juvelook) · 스컬트라(Sculptra) · 프로파일로(Profhilo) · 뉴라미스(Neuramis) · 벨로테로 리바이브(Belotero Revive) · 에스테필(AestheFill) · 하이드라페이셜(HydraFacial) · 미라드라이(miraDry) · 울트라셰이프(UltraShape) · 텐서/테슬라포머(TeslaFormer) — 최종 목록은 대만 대조 표 B 를 보고 「사전 범위(피부과 기기 · 주사 · 시술) 안」만 · 수술 · 감량 약 · 가슴 보형물 제외. 목록을 리포트 첫 표로 확정해라(같은 목록을 세 워커가 쓴다 — R1 이 목록 확정 기준: 대만 표 B ∩ 한국 클리닉에서 쓰는 이름)

## 이번 범위
언어: **th(태국) · vi(베트남) · yue(홍콩 · 번체 · 광둥어권)**
- 홍콩은 번체 · 광둥 표기(대만과 다를 수 있다 — 같으면 같다고)

## 방법 (WebSearch · WebFetch · 필요하면 curl 원문 재확인)
- 그 나라 **현지 피부과 · 의원 · 의료미용 플랫폼**의 시술 메뉴 · 가격표 · 칼럼에서 이름을 찾는다(한국 클리닉의 외국어 페이지는 따로 표시 — 현지 출처가 우선)
- 이름마다 URL · 사이트 이름 · 날짜 · 출처 성격(현지 클리닉 / 현지 플랫폼 / 한국 측 외국어 안내). 못 읽은 사이트(차단 · 로그인 · JS)는 목록으로 남긴다
- 현지 허가명이 있으면 그것 · 현지에 없으면 「현지에 없음 — 영문」 · 모호한 말은 표 C · **지어내지 마라**(음역을 만들지 마라)

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-r3-th-vi-yue-report.md` — 표 A(언어 × 새 시술: name · aliases · 출처 수 · URL · 확신) · 표 B(기존 사전 term 중 이 언어 표기가 틀린 것 — 있으면) · 표 C(모호어) · 못 읽은 사이트 · 조사 날짜. 결정하지 않는다.

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: r3-th-vi-yue" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] researcher r3-th-vi-yue 완료 — <한 줄>" --enter`
