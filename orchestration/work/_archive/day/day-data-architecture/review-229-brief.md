# [reviewer] Delivery #229 웹 기반 + 웹 로그인 — 코드 검수

너는 #226 · #227 을 검수한 day reviewer 다. **읽기 전용** · KOS 호출 금지. **compose 는 지금 사용자가 브라우저로 보고 있다(11040) — 내리거나 재시작하지 마라.** 테스트는 `uv run pytest -m "not infra"` 만 돌려라(infra 는 frontend 리포트 수치 사용).
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 ~ #227 커밋됨, #229 + 웹 로그인 미커밋.
읽을 것: 계약 Issue #229(v2) · #232(v3 — 로그인 화면) · 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-brief.md` + 코디 우선순위 변경(로그인 먼저) · 구현 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-report.md`(「코디가 확인할 것」 8건 판정) · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-229-shots/` · SPEC-001 화면 절 · SPEC-002 화면 구성 · 레포 AGENTS.md 「웹 화면」 · centurion admin 본.
볼 것: 손 CSS 0 · 인라인 스크립트 · `hx-on` 0(grep 전수) · 토큰 확장이 DAY 토큰 파일에만 · 매크로 ↔ E 번호 대응표 · CSRF(hx-headers · form · 로그인 전 미적용) · 로그인 화면이 SPEC-001 화면 절(문구 13줄 · 숨은 폼 칸 · 이메일 유지) · 쿠키 심기가 웹 라우트 · JSON client 기본값 · /dev/kit 노출 범위(dev 만? 로그인 없이 열림 — 판정) · **템플릿 · 견본에 실제 병원 이름 · 실명 같은 실데이터가 하드코딩됐나**(스크린샷 머리에 실제 지점 이름이 보인다 — 어디서 오는지 확인) · 「조용히 통과」.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-229-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
