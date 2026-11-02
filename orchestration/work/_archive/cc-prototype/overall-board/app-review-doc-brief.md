# [reviewer_doc] 앱 계약 검수 — SPEC-004 0.4.0 · DEC-007 · WORK-009

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` — **read-only** · 리포트 1개.

## 기준
- 결정 정본 = `orchestration/work/overall-board/_RESUME.md` §2 **10-26 · 10-27 앱 줄 전부**(앱 범위 · 앱도 쓴다 · 상담사 · 문진 언어 · 스캐너 여권만 · 마스킹 · 사진 · 법적 검토 주석 · iOS 만 · 시안에서 뺌 · 수납 · 처방전 웹만 · 알림 둘 · 새 틀 · 상태 = 웹 2계층 · AP 45 승인)
- 흐름 = `reference/2026-10-27-cc-app/workflow-app.md`(r2 · AP 정해짐) · KOS 근거 `orchestration/work/overall-board/app-kos-report.md` 외 workflow 머리말 리포트
- 웹 규칙(앱이 따름) = `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` 0.4.0 · `spec-003-procedure-board.md` 0.6.0
- 앱 시안(로컬 · 실명 옮기지 마라) `reference/2026-10-23-cc-overall-board/design/` · 분석 `design-refresh-report.md` — 웹과 다르면 웹이 이김
- 코드 현실(읽기만) `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`(back · app)

## 대상 (planner 보고 `orchestration/work/overall-board/app-spec-report.md`)
- `para/projects/summer-star/cc-prototype/10-decision/decision-007-app-v2.md`(새) · `20-spec/spec-004-procedure-app.md` 0.4.0 · `30-work/work-009-app-v2.md`(새) · README · log · links

## 볼 것 (지적마다 `파일:줄` · 근거 · FAIL/WARN/PASS)
1. 결정 줄 · AP 45 → DEC · SPEC 반영 전수(빠짐 · 다르게 = FAIL)
2. **웹 규칙과 같은가**: 앱의 예약 · 내원 쓰기가 웹 API · 규칙(SPEC-005)을 그대로 쓰나 · 상태 이름 · 색 = 웹 2계층 · 뺀 것(수납 · 처방전 버튼 · 알림 다섯 · 리포트 QR · 공지 · 등록 · 드래그)이 정말 빠졌나
3. KOS 표 25 ↔ 리포트 · 미확인 4 가 WP-KOS 게이트로 다 덮이나 · 지어낸 KOS 동작
4. 계약 완결성: back 새 HTTP 14(경로 49) · 표(`device` · `notification` · `display_request` · `questionnaire_history` · `id_photo`) · SSE · 푸시 payload — BE ↔ 앱이 SPEC 만 보고 따로 짤 수 있나 · 기존 원장 호출 푸시 · 시술 현황 회귀
5. 개인정보 · 보안: 사진 저장 · 열람 · 주민번호 안 넣음 · 법적 검토 주석 자리 · 문진 잠금 · 잠금 화면 푸시 글자
6. WORK-009: WP 순서 · 게이트 · 대상 파일 · 완료 조건 · 실기기 E2E 가 사용자 표면인가
7. public(실명 · KOS id · 키 · 토큰 0)

산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-review-doc-r1.md`. 결정을 대신 내리지 마라 — 「사용자 결정 필요」로 모은다.

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_ec508ae4-5ff6-44e8-889b-d955a95e5693 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_doc 완료: <한 줄>" --body "보고서 경로 / 요약 / 검증 수치 / FAIL·WARN · 정할 것 · 흔적"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] reviewer_doc: <질문>" --enter`

## 추가 (재발주 · 2026-10-27)
- 앞 터미널이 보고 없이 사라져 다시 띄운다. **WP-KOS 게이트 결과가 나왔다**: `orchestration/work/overall-board/app-wp-kos-report.md`(K1 ~ K3 받음 · K4 = 사진은 `get-visitor-images` 에 보임 — SPEC §8.0 #23 경로 이름 틀림 · 분류 안 보냄 · scheduleId · path 안 보냄). SPEC 이 이 결과와 다른 곳도 지적에 넣어라
