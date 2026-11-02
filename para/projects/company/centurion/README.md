# Product Map — centurion

규칙: `para/projects/project.md` (`company/` — `sot: external`)

메디솔브 통합 백엔드 `MediSolveAIDev/centurion` 안의 **우리 CRM**(`backend/crm`) 작업. 우리 CRM 은
데이터 허브 + 시술관제를 맡고, 외부 CRM ↔ 우리 CRM ↔ linky · charty · watch 를 잇는다(사용자 2026-10-12).
기획·코드의 원천은 회사 레포에 있고, **여기에는 내 경험(작업 회고)만 쌓인다.**

cc-prototype(금요일 지점 시연용 프로토타입, `summer-star/cc-prototype`)과는 **별개 프로젝트**다.

## 원천 (회사 레포, read-only)

| 무엇 | 어디 |
|---|---|
| 코드 — Python 3.13 · FastAPI · uv, `/auth`·`/linky`·`/common`·`/admin`·`/samples` 를 한 ASGI 프로세스로 | `MediSolveAIDev/centurion` `release/v1.0.0-linky-rc.2` (로컬 `/Users/kknaks/git/centurion`) |
| 우리 CRM 패키지 — 다른 모듈은 `crm.public` 만 import, `crm` → `catalog` 단방향, 1차 연동 업체 KOS | `backend/crm/` · `backend/migrations/crm/` · 관리 화면 `backend/admin/routers/crm.py` |
| 레포 규칙 · 백엔드 안정성 · 테스트 전략 · 새 서비스 편입 | 레포 `AGENTS.md` · `docs/development/` |
| 기획·스펙 | **확인 안 됨** — 회사 레포의 어디가 원천인지 아직 정하지 않았다 |

## 이 폴더

```text
centurion/
├── README.md   이 지도
└── log/        작업 회고 — YYYY-MM-DD-<slug>.md (orchestration config `summary_dest` 가 여기를 가리킨다)
```

`showcase.md` 는 아직 없다.

## 오케스트레이션

- 설정 SSOT: `orchestration/config/projects/centurion.json`
- 워커: researcher · backend · reviewer · reviewer_doc (역할: `orchestration/roles/centurion/`)
- 진행 중 작업: `orchestration/work/<slug>/_RESUME.md`
