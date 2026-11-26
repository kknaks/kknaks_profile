# [planner] spec-sync-2 — SPEC 을 머지된 구현에 맞춘다(마감 전)

너는 day `planner` 워커다. 역할 · 규칙 · 검증 · 완료 보고는 같은 폴더 `day-app-re1-spec-brief.md` 를 따른다(먼저 읽어라). 작업 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`(HEAD `538befe4` = main `ae8cec61` 합친 뒤 · 커밋 · push 금지).

## 배경

WORK-001(앱 차트) · WORK-002(예약현황 탭 · 문진 QR · 여권 스캔 · 태블릿에 보내기) 코드는 CENTURION_DAY dev 에 스쿼시 머지됐다(#295 `8fe0095a` · #296 카메라 문구 `a76496c4`). 스펙 PR #964 를 main 에 머지하기 전에 **SPEC 문장이 구현 · 사용자 결정과 같게** 맞춘다. **구현이 정본** — 새 규칙을 짓지 말고, 구현이 SPEC 과 다른 곳은 SPEC 을 구현대로 고친다(사유 한 줄 + 근거 파일:줄 @ `a76496c4`). 구현이 SPEC 을 어긴 것으로 보이면 고치지 말고 리포트에 「구현 의심」으로.

번호는 merge-dev-2 로 다시 매겨졌다(대응표 = 같은 폴더 `merge-dev-2-report.md` §4 — SPEC-002 ㉚→㉜ · OQ-99/100→119/120 · SPEC-003 ㉑/㉒→㉒/㉓ · U-23~30→U-24~31 · OQ-A63~91→A67~95 · D-7/8→D-8/9 · SPEC-005 OQ-N21/22→N25/26 · SPEC-007 고침 5→6). 아래 원천 리포트들은 **옛 번호**로 적혀 있다 — 대응표로 바꿔 읽어라.

## 맞출 것(전수)

1. **be-2 계약 차이 D1 ~ D17** — `be-2-report.md` §0 표 전부. 행마다 SPEC-000 · 003 · 005 · 006 · 007 의 해당 문장 · 표 · 이름 제안을 구현 이름으로(D1 `crm_status` · `crm_error` · `crm_sent_at` · enum `questionnaire_crm_status` · D3 `customer_not_linked` · D4 `display_closed` · `questionnaire_not_failed` · D10 · D11 · D12 · D13 · D16 · D17 등). 
2. **fix 라운드 변경** — `be-fix-2-report.md` · `app-fix-2-report.md` · `review-code-2-report.md` 에서 계약 · 규칙이 바뀐 곳(F1 문진 1회 제출 = 원자 UPDATE + partial unique `live_unique` · BW2 고객 응답이 KOS 를 안 기다림 등)
3. **migration 이름** — 우리 migration 은 `0030_display_questionnaire_kos`(down `0029_partner_charty`) 가 됐다(`merge-dev-3-report.md`). SPEC-000 등에 0029 로 적힌 곳
4. **「국적 / 통역필요」** — `app-2-report.md` §5 8번: 앱은 웹 템플릿 표시를 따랐다(사용자 기본값). SPEC-003 U-3 문장을 구현대로
5. **WORK-001 W3 · W4 · OQ-119(옛 OQ-99)** — `_RESUME.md` §2 2026-11-25 행 · §「spec-sync 때」 줄: W3 사진 크게 보기 = 새 화면 · W4 저장 띠 자리 = 지금 구현 · OQ-119 baseBody 문자열(GET null ↔ POST "") → 구현대로 닫음
6. **사용자 결정 닫기** — OQ-A79(옛 번호 — 대응표로) iOS 카메라 문구 = 「채팅으로 보낼 사진과 차트에 올릴 시술 전후 사진을 찍고, 고객 여권의 정보면을 읽기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」(사용자 2026-11-26 · #296) · dev 메뉴 「예약 현황」 · 「고객」 다시 열림(dev `65b2de5e` — SPEC 이 막힘을 말하면 맞춤)
7. **`_RESUME.md` §2 의 2026-11-25 · 26 WORK-002 결정 행 전부**를 SPEC 과 한 번 대조 — 빠진 결정이 있으면 반영
8. `30-work.md` 상태 · `log.md` 에 spec-sync 행(날짜 2026-11-26 · 근거 = 이 리포트)

## 하지 말 것

- 새 규칙 · 새 화면 글자 짓기 · main 쪽 문장(#965 · #966 · #967) 고치기 · 코드 건드리기

## 검증 · 보고

lint `--strict` day 범위 0/0 · 번호 참조 끊김 0(merge-dev-2 §4 의 grep 방식). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/spec-sync-2-report.md` — 항목 1 ~ 8 처분표(바꾼 파일:줄 · 근거 코드 파일:줄 · 구현 의심). 완료 = dispatch preamble 의 `worker_done`(`--report-path`) + 직접 주입 `[worker_done] planner 완료: spec-sync-2 — <한 줄>. 상세는 인박스.`
