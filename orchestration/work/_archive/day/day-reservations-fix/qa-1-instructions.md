# [qa] 웹 화면 검수 — 예약 현황판 F1 ~ F6 · 6개월 경과 (Playwright)

너는 **day `qa` 워커**다. 먼저 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/qa/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`).

대상: **로컬 스택 `http://127.0.0.1:11340`**(코디가 띄움 · 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` 미커밋 코드 · KOS DEMO 지점 연결). **스택 시작 · 멈춤 · 코드 · 문서 수정 금지.** 다른 스택(11040 · 11240) 금지. 로그인 = `deploy/local.env` 의 데모 지점 계정(값 출력 금지 · 옮기지 마라). 로컬 DB 는 SELECT 만(포트 11342 · 스키마 `day_dev`).

⚠ 같은 스택에서 **backend 워커가 e2e-1(서버 · DB 시험)** 을 하고 있다. 그가 DEMO 오늘 17:00 · 17:30 리프팅 예약 두 건(고객 `b26e24e0` · `1b9a7c0c`)을 만든다 — 그 두 방문을 써라. 다른 방문 · 다른 사람 예약은 손대지 마라. **예약 만들기 · 옮기기 · 취소처럼 KOS 에 쓰는 동작은 하지 마라**([+] 은 등록 창이 열리는 데까지만). 태블릿 보내기 · 링크 복사 · 링크 열기는 DAY 안 동작이라 해도 된다.

## 기준
- SPEC(mediness#971): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec/products/day/20-spec/spec-006-reservation-board.md`(개정 ⑯ · Rule 15 ⓐ ~ ⓚ) · `spec-007-reservation-detail.md`(고침 8 · 규칙 2 · 7 · 9)
- Issue #301 완료 조건: `gh issue view 301 -R MediSolveAIDev/CENTURION_DAY`
- 사용자 피드백 원문 · 스크린샷: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §1 F1 ~ F6 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/f1-kos-add-slot.png` · `f3-kos-survey-menu.png` · `f5-day-device-card.png`(이 카드가 **없어져야** 함)

## 시나리오 (각 PASS / FAIL · 스크린샷)
1. **F2 배치**: 60분 예약 = 1시간 행 하나 높이 · 17:00 · 17:30 두 카드가 겹치면 옆 자리 · 30분 카드면 반 · 시간 글자 = 1시간 행 · 바탕 선 = 행 경계만.
2. **F1 [+]**: 카드 오른쪽 여백(카드 반 폭)에 호버 → 점선 [+] · 툴팁 「그룹 | 시작 ~ 끝」 · 누르면 그 그룹 · 시각으로 등록 창(**저장 누르지 마라** · 닫기).
3. **F3 [문진 QR]**: 버튼이 비활성처럼 보이지 않음 · 누르면 팝오버 **하나**(위 「링크 복사하기」 · 「링크 열기」 / 아래 기기 줄) · 두 단계 메뉴 없음.
4. **F5 기기 줄**: `기기명 [점] 상태` · 초록 = 연결 · 빨강 = 미연결 · 미연결도 누를 수 있음 · 모달 안 별도 기기 카드 없음. [여권 스캔] = 같은 기기 팝오버.
5. **F6 태블릿 보내기**: 태블릿(기기) 화면을 다른 Playwright 페이지로 열어 두고(DAY 의 기기 표시 화면 · 경로는 코드/SPEC 에서 찾아라) 웹 [문진 QR] → 기기 줄 누름 → **QR 이 사라지지 않고** 기기 화면에 문진이 뜸 · 웹 진행 칸 상태.
6. **링크**: 「링크 열기」 = 새 탭에 문진 링크 · 「링크 복사하기」 = 클립보드(Chromium 권한 허용) · 두 번 눌러도 같은 링크 · (가능하면) 링크로 문진 화면까지만 열고 **제출은 하지 마라**(backend 가 제출 시험을 한다).
7. **D45**: 팝오버 연 채로 SSE 다시 그리기(다른 페이지에서 상태 바꾸기 또는 동기화 10초 기다림) → 팝오버 안 닫힘.
8. **6개월 경과**: 해당 고객이 있으면 「초진 문진」 줄 「6개월 경과」 · 없으면 DB SELECT 로 근거만 · 「데이터 없음」.
9. 콘솔 오류 · 네트워크 4xx/5xx 0(있으면 그대로).

## 산출물
- 스크린샷: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-1/` (시나리오 번호 이름)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-1-report.md` — 맨 위 표(시나리오 × PASS/FAIL · 스크린샷 · 비고) · FAIL 은 재현 절차 + (보이면) 원인 file:line · 사용자 피드백 F1 ~ F6 각각 「고쳐졌나」 한 줄

## 하지 말 것
코드 · 문서 수정 · 커밋 · KOS 쓰기 동작 · 스택 건드리기 · 비밀값 · PII 출력(id 앞 8자).

## 완료 보고 — 문구 변경 금지
⚠ 핸들은 dispatch preamble 값을 믿어라.
```bash
orca orchestration send --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "qa 완료: <한 줄>" --body "<요약>"
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[worker_done] qa 완료 — <한 줄>. 상세는 인박스." --enter
```
