# [planner] 40-architecture 추가 — 시스템 런타임 · 코드 구조(백엔드 · 웹 · 앱)

너는 day planner 워커다. 계약은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 그대로다(products/day 밖 금지 · 원천에 없는 것 발명 금지 · 커밋 금지).
같은 워크트리 · 같은 브랜치에서 이어 쓴다 — 지금까지 산출물은 **커밋돼 PR #909 에 올라가 있다**(`git log`). 그 위에 고친다.

## 원천 (2026-11-03 사용자와 정함)

1. **시스템 런타임**: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` — api / worker 분리 · taskiq(worker + scheduler) · Redis(브로커 · 결과 · 화면 알림 · 잠금, RabbitMQ 없음) ·
   10초 폴링 = taskiq `interval` · 병원별 Redis 잠금 · 서버(VM 2코어/4GB + 관리형 PostgreSQL + Blob) · 기본값 표(SSE · Blob · APNs · Key Vault · JSON 로그).
2. **코드 구조**: CENTURION_DAY 레포 `AGENTS.md`(v2-dev) — 읽는 법: `git -C /Users/kknaks/git/CENTURION_DAY show origin/v2-dev:AGENTS.md`
   (저장소 구조 · 계층 규칙 · 외부 CRM 연동(emr) · 웹 화면(Jinja2 + HTMX · centurion admin 방식) · 앱(Flutter) · 백엔드 안전 · 테스트).
   구조의 정본은 그 `AGENTS.md` 다 — mediness 에는 **요약과 링크**만 둔다(복제하지 않는다).

## 할 일

1. `products/day/40-architecture/system.md` — 기존 절(토폴로지 · 원장 · 폴링 · 쓰기 큐 · 로그인 · 환경 · KOS 를 뗄 때 · 외부 통합)은 두고,
   원천 1 을 반영한다: 런타임 구성(api · worker · scheduler · Redis · PostgreSQL · Blob · caddy) · 버튼 하나의 흐름 · 폴링 방식 · 중복 막기 ·
   서버 사양 · 기본값 표. 기존 「토폴로지」 그림이 원천과 다르면 원천으로 맞춘다. 원천의 근거(centurion 대비 · taskiq 버전 확인)는 짧게.
2. **코드 구조** — 원천 2 를 요약한다. 자리: system.md 의 새 절 또는 `40-architecture/` 아래 새 파일 하나(`code-structure.md` 등) 중
   `rules/document-pipeline.md` 의 40-architecture 규칙(「쓰지 않는 것」 — repository 함수 목록 · API 본문 금지)에 맞는 쪽을 골라라.
   담을 것: 레포 · 브랜치 · 최상위 배치(backend/day · runtime · common · migrations · tests · app · deploy) · `backend/day` 안의 층(화면 = admin 방식 /
   업무 = crm · catalog 방식, repository 없음, public.py 만 밖으로 / emr 업체 어댑터) · 웹(Jinja2 + HTMX) · 앱(Flutter · iOS 축소판) · 정본 링크.
3. `40-architecture/README.md` 진입 · 핵심 도메인 표에 새 내용이 있으면 링크. `log.md` 에 한 줄(PR `#909`).
4. lint `--strict` 1회.

하지 말 것: SPEC-000 · 10-decision · 20/30 인덱스는 건드리지 않는다(필요해 보이면 보고). 원천에 없는 기술 선택 · 버전 · 수치를 더하지 않는다.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-arch-report.md`. 완료는 preamble 의 worker_done 절차대로.
