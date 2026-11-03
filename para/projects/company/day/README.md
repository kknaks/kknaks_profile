# Product Map — day

규칙: `para/projects/project.md` (`company/` — `sot: external`)

메디솔브 센추리온 제품군의 **DAY CRM**(환자 · 상담 · 접수 · 예약 · 수납) 재구축. mediness 카탈로그 slug `day`, Jira `CENDAY`.
2026-11-02 착수 — 기존 CENTURION_DAY(v0.1.0-rc.14)는 전부 아카이브로 두고 처음부터 다시 짓는다.
웹은 서버 렌더링(Jinja2 + HTMX + 바닐라 JS), 직원 앱은 Flutter — 앱은 기능을 줄여 심사를 빨리 통과하는 것이 목표다.
기획·코드의 원천은 회사 레포에 있고, **여기에는 내 경험(작업 회고)만 쌓인다.**

## 원천 (회사 레포)

| 무엇 | 어디 |
|---|---|
| 코드(v2) | `MediSolveAIDev/CENTURION_DAY` `v2-dev` — 빈 브랜치에서 시작 (로컬 `/Users/kknaks/git/CENTURION_DAY`) |
| 기존 코드(아카이브) | 같은 레포 `stg` = `main` (`11e27b08`, rc.14) — 읽기만 |
| 기획·스펙 | `MediSolveAIDev/mediness` `products/day/` (2026-11-02 기준 아직 없음) |
| KOS API 사용법 (조회만) | `kknaks/ax-clinic-project` `scripts/` · `para/resources/technology/2026-*-kos-*.md` — 공개 API 에 없는 건 HAR(`reference/2026-10-12-cc-prototype/` · `2026-10-23-cc-overall-board/har/`) |
| 참고 | `kknaksss/cc-prototype` — `cc/` · `procedure/` (프로필 `summer-star/cc-prototype/`) |
| 웹 화면 방식의 본 | `MediSolveAIDev/centurion` `main` — `backend/admin/`(Jinja2 + HTMX + 바닐라 JS) · `docs/development/medikit-htmx-design-guide.md` |

`products/nexus/`(더데이랩스 홈페이지·어드민 SI)와 centurion 레포의 `backend/crm`(`company/centurion/`)은 다른 것이다.
centurion `backend/crm` 과의 관계는 아직 정하지 않았다.

## 이 폴더

```text
day/
├── README.md   이 지도
└── log/        작업 회고 — YYYY-MM-DD-<slug>.md (orchestration config `summary_dest` 가 여기를 가리킨다)
```

`showcase.md` 는 아직 없다.

## 오케스트레이션

- 설정 SSOT: `orchestration/config/projects/day.json`
- 워커: researcher · planner · reviewer_doc · designer · backend · frontend · mobile · reviewer (역할: `orchestration/roles/day/` — cc-prototype 에서 가져옴). v2-dev 레포 구조는 레포 루트 `AGENTS.md` 가 정본(2026-11-03). 배포는 DAY 전용 Azure 서버를 할당받을 예정 — infra 워커는 그 뒤에(2026-11-02)
- 진행 중 작업: `orchestration/work/<slug>/_RESUME.md`
