# planner — ① 앱 계약 판 (코디 · 2026-10-27) · 같은 터미널 이어서

사용자가 `workflow-app.md` 정할 것 **AP-1 ~ AP-45 기본값 전부 승인**(「응 그렇게 가자」 · `_RESUME` §2 10-27 줄). 이제 계약 문서를 쓴다. 역할 · 금지 · 완료 보고는 앞 브리프 `app-workflow-brief.md` 그대로(보고서만 아래).

## 쓸 문서 (allowed_paths)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-27-cc-app/workflow-app.md` — AP 줄을 「정해짐(10-27 사용자 · 기본값 승인)」으로 · 정할 것 표는 닫힌 표로
- `para/projects/summer-star/cc-prototype/10-decision/decision-007-app-v2.md`(새) — 앱 결정 D-xx(10-26 · 10-27 앱 줄 + AP 45)
- `para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` **0.3.2 → 0.4.0** — 앱 = 4탭(예약 · 내원 · 시술 현황 · 설정) · 새 틀(탭바 · 레일 · 공통 헤더) · 상태 = 웹 2계층 · 예약 · 내원 쓰기(웹 API 재사용) · 상담사 계정 · 상담사 호출 푸시 · 알림 둘 · 띄우기 요청 · QR 문진 · 여권 스캔 · 사진 저장 · 웹 따라잡기(§10.1 닫기). back 새 API · 표(`device` 이름 · 띄우기 요청 · `push_log.kind` · 문진 이력 · 사진)는 §7 · §3 에 · 법적 검토 주석 자리
- `30-work/work-009-app-v2.md`(새) — WP 나눔(back · app · infra(사진 볼륨) · WP-KOS 미확인 4건 데모 확인 게이트) · 대상 파일 · 완료 조건 · 검증 · E2E(**실기기 iOS** — 사용자 표면)
- README 2 · log.md · SPEC-003 · SPEC-005 frontmatter links 한 줄
- 보고 `orchestration/work/overall-board/app-spec-report.md`

## 검증
- AP 45 · 앱 결정 줄 → DEC · SPEC 절 대조(빠짐 0) · KOS 표 25 → SPEC §8(미확인 4 = WP-KOS 게이트) · 실명 · id · 토큰 grep 0
- 끝나면 같은 두 명령(subject 「planner 완료: 앱 계약 …」)
