# [planner] spec-4 — 마감 전 스펙 맞추기 (작은 판)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-spec-brief.md`(역할 · allowed_paths `products/day/` · 검증)를 따른다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec`(미커밋 위에). 커밋 금지. **20시 배포 전이라 빨리.**

같은 작업에서 사용자가 로컬 확인 중 정한 화면 변경 3건(코드 반영 끝 — `fe-2-report.md` · `fe-3-report.md` · `fe-4-report.md` 같은 폴더)을 **SPEC-002(`spec-002-procedure-board.md`)** 에 반영한다(다음 개정 번호 · 사용자 2026-11-17):
1. 차트 여는 곳 = **시술명 영역 전체**(1줄 시술 이름 + 2줄 상태 줄 · 빈 자리 포함) — 체크박스 · 줄 버튼 · ⋮ · 「원장 변경」 원장 이름 버튼은 제외. 판 줄 · 「시술 완료」 탭 줄 모두(개정 ㉒ E6 「시술 이름 글자만」을 넓힘 — 옛 문장 취소선 + 사유).
2. 차트 영역 호버 · 포커스 = **배경 · 테두리 없음 · 툴팁 「차트 작성」만**.
3. 정렬 탭 글자 확정 = **「시술대기 순」 · 「방별 순」**(OQ-59 ⓐ 임시 이름 닫음).
그리고 SPEC-001 개정 ⑨ 에 배포 메모 한 줄: 서버 env `KOS_CLIENT_TAG` = dev 서버 `dev` · prod 서버 `prod` · 로컬 `local`.

lint --strict products/day ERROR 0. 리포트 `…/kos-signin-limit/spec-4-report.md`(짧게). 완료 보고는 preamble 의 worker_done.
