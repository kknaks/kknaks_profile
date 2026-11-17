# [frontend] fe-5 — 버그: 수락(시작 전) 줄에서 원장 변경이 안 됨

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-fe-brief.md`(역할 · 검증 · 완료 보고). 앞 판 `fe-2-report.md` · `fe-4-report.md`(같은 폴더 — 시술명 영역 전체를 차트 여는 곳으로 바꿈). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(혼자 · 미커밋 위). 커밋 금지.

## 증상 (사용자 2026-11-17 로컬)
- 판 카드 시술 줄 — **수락(시작 전) 줄**의 원장 이름(「{원장} 수락 완료 HH:MM」)으로 **원장 변경이 안 된다.** **진행중 줄은 된다.**
- 스펙: 원장 변경 = 수락 · 진행중(SPEC-002 규칙 27 · U-3) · 서버 `board_rules.py:291` `doctor_change_block` 도 둘 다 허용.

## 할 일
1. 원인을 찾는다 — 템플릿(`board_parts.html` :83 `doctor_pop` · :134 원장 변경 창 · `ui.html` `_proc_doctor` · 수락 줄 메타) · 스냅샷 값(수락 줄의 `t.doctor` 가 비어 「원장」 글자가 호출 대상으로 대신 채워지는지 — `board_rules.py:163` `task_doctor` · 스냅샷 조립) · `day.js`(차트 영역 `innerOwn` 가드 :853 · 팝오버/창 열기 · 수락 줄에만 있는 속성)로 수락 줄과 진행중 줄을 같은 데이터로 렌더해 비교한다(TestClient + 가짜 스냅샷 또는 기존 테스트 픽스처).
2. dev(`origin/dev` `0c401726` — 오늘 차트 영역 변경 전)에서도 같은지 확인 — 회귀인지 원래 버그인지 리포트에.
3. 고친다(allowed_paths: `backend/day/templates/` · `backend/day/static/day.js` · `backend/day/styles/` · `backend/day/static/day.css`(빌드) · `backend/tests/day/web/` — 원인이 서비스 · 스냅샷이면 고치지 말고 리포트에 「backend 몫」 + 정확한 자리).
4. 테스트: 수락 줄 원장 이름 = 원장 변경 버튼 + 창 존재 · 차트 영역이 가로채지 않음.

검증: 화면 pytest · CSS 빌드(바꿨으면) · node --check · 인라인/style= 0. 리포트 `…/kos-signin-limit/fe-5-report.md`. 완료 보고는 preamble 의 worker_done.
