# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-09-03 | 문서 파이프라인 재시작 — 프로젝트 세팅 커밋(config·roles·디자인 패키지), 문서 워커 workspace=coordinator 전환 | [README](README.md) |
| 2026-09-03 | 디자인 프론트 구조 분석 완료(designer) — P-01~72 · F-1~13 · C-01~49 · S-01~34 · Q-01~42. 총계 Page 24 · 오버레이 27 · 신규 컴포넌트 ~43 · 공용 34 | [리포트](../../../../orchestration/work/docs-v1/docs-v1-design-report.md) |
| 2026-09-03 | **사용자 확정 4건**: ① 홈화면.dc.html 패키지 제외(홈·채팅은 나중, Q-27) ② 자료함 정본 = 문서함.dc.html 확정안, 탐색안 화면 10개 폐기(Q-26) ③ 메시지함 v1 범위 보류(Q-35 open) ④ 문서화 순서 = 내 업무부터 → **인증·설정부터로 번복**(업무가 설정의 유형·프로젝트를 참조) | — |
| 2026-09-03 | docs-v1 전체 계획 합의(Phase 1 영역 6건 BASE+DEC → 2 SPEC → 3 코드). 문서는 발주 없이 **논의→코디 직접 작성→리뷰**, 워커는 분석·코드만 | [_RESUME](../../../../orchestration/work/docs-v1/_RESUME.md) |
| 2026-09-03 | **BASE-001+DEC-001(인증·설정) 작성** — 로그인(아이디+비번, 8자 문자·숫자·특수, JWT 쿠키 access 1h/refresh 7d), 계정=DB 시드(가입·찾기 없음), 유형(종류 미팅\|업무+이름+색, 기본 3종 잠금)·프로젝트(이름+색), slug 없음(자동 키), 소프트 딜리트, 목 UI 4종(소셜·목소리·연동·계정삭제=v2). OQ 6건 | [BASE-001](00-baseline/baseline-001-auth-settings.md) · [DEC-001](10-decision/decision-001-auth-settings.md) |
