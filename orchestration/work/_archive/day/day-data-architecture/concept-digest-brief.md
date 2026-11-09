# [planner · 개념 소화] day-data-architecture 회고 §2 → para/areas/concept

너는 문서 워커다. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/day`(profile · 브랜치 kknaksss/day) · **커밋 금지**. 다른 파일 건드리지 마라.
읽을 것: 회고 `para/projects/company/day/log/2026-11-09-day-data-architecture.md` §2(8항목) · 규약 `para/areas/area.md` §3.1 ~ §3.4(**§3.3 규약 그대로** — 먼저 찾기 · aliases grep · 있으면 보강 · 없을 때만 새로 · up: 필수 · 영문 kebab stem · stem 바꾸지 않기 · 새것은 3.4 맵 한 줄) · 양식 `templates/areas/concept.md` · 앞 마감의 본보기 `git show d4cde160 --stat` 와 그 개념 diff.
할 일:
1. §2 각 항목을 개념 단위로 쪼개 기존 노트를 찾는다(코디 1차 후보: `cs/polling` · `back/webhook` · `db/unique-key` · `infra/ci-cd` · `infra/reverse-proxy` · `cs/layered-architecture` · `infra/web-application-deployment` · `infra/dev-prod-parity` — **후보일 뿐 · 직접 grep 으로 확정**). 있으면 보강(up: 에 회고 링크 · 본문에 이번 사례 녹이기), 없으면 새로(예: transactional outbox · partial unique index · 서버 렌더 HTMX/SSE · OIDC 배포 · managed identity + 비밀 보관 · asyncpg TLS 같은 「막혔다 푼 것」은 기존 노트 안 절로 갈지 새 노트로 갈지 판단).
2. 회고 §2 각 항목 끝에 `[[stem]]` 역링크.
3. 사내 정보 최소: 사람 이름 · 지점 이름 · IP · 계정 ID · KOS 주소 · 키 넣지 마라(제품 이름 DAY · KOS 는 됨).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/_archive/day/day-data-architecture/concept-digest-report.md` — 항목 → (보강 | 새로) stem 표 · 맵 추가 줄. 완료는 preamble 의 worker_done 절차대로(둘 다).
