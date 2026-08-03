---
type: work
id: KDEV-WORK-018
title: "제품 레지스트리 — 조인 컬럼·관리 화면·결정적 스캐폴딩"
status: in_progress
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 20
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-005-product-project-career-link|KDEV-BL-005]]"
  decisions:
    - "[[decision-017-product-registry-and-admin-scaffold|KDEV-DEC-017]]"
  specs:
    - "[[spec-014-product-registry-and-admin|KDEV-SPEC-014]]"
    - "[[spec-011-commit-collection|KDEV-SPEC-011]]"
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works:
    - "[[work-017-grass-commit-pipeline|KDEV-WORK-017]]"
  releases: []
  related:
    - "[[work-011-admin-auth-mvp|KDEV-WORK-011]]"
---

# 제품 레지스트리 — 조인 컬럼·관리 화면·결정적 스캐폴딩

레포와 제품을 잇는 컬럼 하나를 만들고, 관리 화면에서 제품을 등록·연결·발견한다. 등록은 **LLM 없이** 제품 골격과 공개 카드를 만들고 레포를 즉시 클론한다. **백엔드 신규 코드는 `api → service → repository` 3계층으로 짓는다** — 이 발주가 그 규약의 첫 적용이다.

**만들지 않는 것**: 잔디 산출물에 product 추가(후속) · 공개 카드 본문 편집 · `visible` DB 이관 · 제품 문서 삭제 · 레거시 계층 리팩터.

## Meta

- Baseline: [[baseline-005-product-project-career-link|KDEV-BL-005]]
- Covers spec: [[spec-014-product-registry-and-admin|KDEV-SPEC-014]] (전량) + SPEC-011·001 개정분
- Depends on work: [[work-017-grass-commit-pipeline|KDEV-WORK-017]] — `tracked_repos`·`sync_repo`·시드 스크립트가 전제다. 이 발주는 그 위에 컬럼 하나와 관리 표면을 얹는다
- Parallel work: 없음
- Follow-up work: 잔디 산출물에 product 추가 (P2 — 후속 decision)
- External dependency: **P3·P5 에만 있다** — GitHub 토큰(`gh_accounts()`, 이미 `.env` 에 있다) · 신규 레포 4개 클론 디스크 · P5 는 서버 재배포. **P1·P2·P4 는 외부 의존이 없다.**

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | in_progress |
| Progress | 20% (P1 done — 형식 SoT + 트리 정리. 제품 18→12, showcase 13→8, `visible` 6 불변) |
| Branch/PR | `work-018-db` |
| Blocker | 없음 |
| Next | P2 — `product_slug` 컬럼 + `repository/` 계층 신설 + 17행 시드 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | done — DEC-017 D1~D17, OQ 0 |
| Design | kknaks | 등록 폼·표·배너 UX | todo |
| FE | kknaks | 프로젝트 슬롯 화면 | todo |
| BE | kknaks | 컬럼·repository·service·API | todo |
| QA | kknaks | 검증과 완료 판단 | todo |
| Ops | kknaks | 배포·클론·실운영 관측 | todo |

## Scope

포함:

- `templates/product/showcase.md` 신설 (형식 SoT)
- `kknaks-profile` → `kknaks-dev` 통합 · 회사 5개 디렉토리 삭제
- `products/README.md` 목록 1회 정정 · 제품 README 3곳 `Remote: TBD` 정정
- `tracked_repos.product_slug` 컬럼 + 마이그레이션 + 17행 시드
- **`repository/` 계층 신설** (계층 규약 첫 적용)
- 제품 등록 service — 스캐폴드·카드 렌더·사전 검증·채번·커밋/롤백
- 레지스트리 CRU · 수동 재동기화 · 미등록 레포 발견
- admin 프로젝트 슬롯 화면
- 실운영 완주 — 실제 제품 1건 등록 + 잔디에 새 레포가 잡히는지 관측

제외:

- 잔디 산출물에 product 추가 → 후속 decision
- `visible` DB 이관 → DEC-017 D14 기각
- showcase 그래프 노드 승격 → D16 기각
- 공개 카드 본문 편집 · 제품 문서 삭제 → 로컬에서 한다
- **레거시 계층 리팩터** → `queue.py`·`auth.py`·`service/**` 는 손대지 않는다

## Code Surface

- Repo / module: `app/back` (주) · `app/front` (화면) · 루트(`templates/`·`products/`)

| 경로 후보 | 설명 |
|---|---|
| `templates/product/showcase.md` (신규) | 카드 형식 SoT — P1 |
| `products/kknaks-dev/showcase.md` | `kknaks-profile` 에서 이동 — P1 |
| `products/README.md` | 제품 목록 정정 — P1 |
| `alembic/versions/0009_*.py` (신규) | `product_slug` 컬럼 — P2 |
| `core/models.py` | `TrackedRepo` 컬럼 1줄 — P2 |
| **`repository/__init__.py` · `repository/tracked_repos.py`** (신규) | **DB 접근 전담 계층 신설** — P2 |
| `app/scripts/seed_repo_registry.py` | 시드에 `product_slug` + 신규 4행 — P2 |
| **`service/products/dto.py`** (신규) | **도메인 DTO (pydantic)** — api↔service↔repository 경계 — P2 |
| `service/products/registry.py` (신규) | 등록 오케스트레이션 · CRU — P3 |
| `service/products/scaffold.py` (신규) | 골격 복사 **화이트리스트** · 카드 렌더 · 채번 — P3 |
| `service/products/validate.py` (신규) | 사전 검증 7종 · 도메인 예외 — P3 |
| `service/products/discover.py` (신규) | 미등록 레포 발견 — P3 |
| `utils/slug.py` (신규) | 레포/제품 slug 파싱·정규화 (순수) — P3 |
| **`api/schemas/products.py`** (신규) | **요청·응답 모델 (pydantic)** — HTTP 표면 — P3 |
| `api/routers/products.py` (신규) | 엔드포인트 6 · 예외→HTTP 매핑 — P3 |
| `main.py` | `include_router` 1줄 — P3 |
| `app/front/app/admin/(panel)/projects/page.tsx` (신규) | 화면 — P4 |
| `app/front/components/admin/product-registry.tsx` (신규) | 표·폼·배너 — P4 |
| `app/front/components/admin/sidebar.tsx` | `ready: true` 1줄 — P4 |
| `app/front/lib/api.ts` | 클라이언트 함수 — P4 |
| `tests/` | 계층 경계 · 스캐폴드 화이트리스트 · 검증 7종 · 마이그레이션 드리프트 |

- Domain / schema note: **마이그레이션 1건**(컬럼 추가, P2). 기존 테이블 구조 변경 없음. `tracked_repos` 외 다른 테이블은 무변경.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `tracked_repos.product_slug` | 레포 → 제품 디렉토리 조인. nullable |

- 상태 / invariant: `product_slug` 는 **CHECK 를 걸지 않는다**(DEC-017 D7). `detail` 처럼 `type` 에 묶지도 않는다 — company·studio 둘 다 가질 수 있다. 실재 여부는 응답 시점에 판정해 화면이 경고한다.
- Migration 필요 여부: **필요** — 컬럼 1개 추가. 기존 13행은 `NULL` 로 시작하고 시드가 채운다.
- SPEC 환류: 없음 — SPEC-014 가 이미 계약을 담고 있다.

### 왜 CHECK 를 안 거는지

`daily.py:151` 이 같은 판단의 근거를 남겨 뒀다 — *"DB 계층이 레포 파일시스템을 알게 되고, 나중에 career 파일 이름이 바뀌면…"*. `detail` 오타를 CHECK 가 아니라 `missing_career()` 가 승인 화면까지 들고 가는 방식이 이미 서 있다. `product_slug` 도 같은 형태를 따른다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| P2 시드 | P1 의 정리된 제품 목록 | `kknaks-profile` 통합·회사 5개 삭제 **후의** 상태가 매핑 기준이다 |
| P3 스캐폴드 | P1 의 `templates/product/showcase.md` | 형식 SoT 를 읽어 카드를 만든다 |
| P3 전부 | P2 의 `repository/tracked_repos.py` | service 는 DB 를 직접 만지지 않는다 |
| P4 화면 | P3 의 엔드포인트 6 | — |
| P5 완주 | P3+P4 | 등록이 실제로 커밋·push 되고 클론이 붙어야 관측이 된다 |
| 후속(잔디 product) | P2 의 `product_slug` | `product_map` 을 만들 재료 |

## Internal Interface Contract

**계층 계약은 `40-architecture/system/README.md` 「백엔드 계층 규약」이 SoT 다.** 여기서 다시 적지 않는다.

이 발주에서 새로 고정하는 것은 **스캐폴드 화이트리스트** 하나다.

```text
복사한다        templates/product/README.md              → products/{slug}/README.md
                templates/product/log.md                 → products/{slug}/log.md
                templates/product/00-baseline/README.md  → products/{slug}/00-baseline/README.md
                templates/product/10-decision/README.md  → products/{slug}/10-decision/README.md
                templates/product/20-spec/README.md      → products/{slug}/20-spec/README.md
                templates/product/30-work/README.md      → products/{slug}/30-work/README.md

복사하지 않는다  baseline.md · decision.md · spec.md · work.md · work-release.md
                release.md · runbook.md · domain.md          ← frontmatter 를 가진 예시 문서 8개
                40-architecture/** · 60-release/** · 70-runbook/**   ← optional
```

**이 목록은 코드 상수이고 테스트가 고정한다.** 템플릿에 새 예시 문서가 추가될 때 복사 목록이 조용히 어긋나는 것이 이 발주의 가장 조용한 실패 모드다.

### 계층과 DTO 배치

규약 자체는 `40-architecture/system/README.md` 가 SoT 다. 이 발주에서 **어느 파일이 어느 계층인지**만 고정한다.

```text
api/schemas/products.py     요청·응답 (pydantic)      ← HTTP 표면
api/routers/products.py     엔드포인트 · 예외→HTTP     ← select() 없음
        ↕  도메인 DTO
service/products/dto.py     도메인 DTO (pydantic)
service/products/*.py       규칙 · 오케스트레이션       ← HTTPException 없음, select() 없음
        ↕  도메인 DTO
repository/tracked_repos.py DB 접근                    ← ORM 이 여기서 끝난다
        ↕  ORM
core/models.py              TrackedRepo
```

**`sync_all` 이 ORM 을 밖으로 흘리던 것을 이번에 끊는다.** 지금 `enabled_repos()` 가 `list[TrackedRepo]` 를 돌려주고 `sync_all` 이 그 객체의 `last_fetched_at`·`last_error` 를 직접 대입한다. P2 에서 **repository 가 DTO 를 돌려주고, 상태 기록은 repository 메서드로** 바꾼다.

| 종전 | 이후 |
|---|---|
| `enabled_repos(db) -> list[TrackedRepo]` | `repository.list_enabled(db) -> list[TrackedRepoDTO]` |
| `repo.last_fetched_at = now` (ORM 직접 대입) | `repository.mark_synced(db, id, at)` |
| `repo.last_error = f"{code}: {msg}"` | `repository.mark_failed(db, id, code, msg)` |

**잔디 경로가 이 변경을 지난다.** `collect_git.py:91-101` 이 유일한 소비자이므로 회귀면이 좁지만, P2 검증에 회귀 항목을 둔 이유가 이것이다.

## Execution

> **P1 이 맨 앞인 이유가 둘이다.** ① 스캐폴드가 읽을 카드 양식이 없으면 P3 가 형식을 지어내게 되고, 그 순간 SoT 가 둘이 된다(WORK-017 P1 이 같은 이유로 맨 앞이었다). ② 시드 매핑은 **정리된 뒤의** 제품 목록을 기준으로 해야 한다 — `kknaks-profile` 이 남아 있으면 `kknaks/kknaks_profile` 을 어디로 보낼지 코드가 정할 수 없다.
>
> **P1 은 코드가 한 줄도 없다.** 문서와 파일 이동뿐이라 되돌리기 쉽고, 그러면서 P2~P5 의 전제를 전부 만든다.

### Phase 1 — 형식 SoT + 제품 트리 정리 (문서·파일)

- **Status**: DONE
- **설명**: 카드 양식을 만들고, 제품 트리의 어긋남 셋을 정리한다. 코드 변경이 없어 배포도 마이그레이션도 필요 없다.
- **작업**:
  - [x] `templates/product/showcase.md` 신설 — 로더 필수 7 필드 · 표시 필드 · **PDF 전용 블록은 "필요할 때 추가" 로 표시** · 본문 필수 3섹션 + 선택 4섹션 · `links.repo` 는 표시 전용이고 추적은 레지스트리 소유(DEC-014 D1)
  - [x] `products/kknaks-profile/showcase.md` → `products/kknaks-dev/showcase.md` (git mv) · 빈 디렉토리 삭제
  - [x] 회사 5개 디렉토리 삭제 — `centurion-charty`·`centurion-mso`·`linky`·`mediness`·`nexus`
  - [x] `products/README.md` 제품 목록 정정 — 정리 후 13개 기준
  - [x] 제품 README 3곳 `Remote: TBD` → 실제 값 (`ax-knowledge-graph`=`kknaks/ax-graph` · `mini-game`=`kknaks/lunch_game` · `mac-remote`=`kknaks/mac-remote`)
  - [x] `agent.md` 「별도 계열」에 showcase 템플릿 등록 (daily·career 와 같은 형태)
- **검증**:
  - [x] `product_doc_pipeline.py --strict` 통과 — **빈 디렉토리가 남지 않았다**
  - [x] 부팅 그래프 검증 ERROR 0
  - [x] `/api/projects` 모집단 13 → 8, **`visible:true` 6개는 그대로** (화면 무변경)
  - [x] `/api/print` 포트폴리오 PDF 대상이 안 줄었다 (`visible` 기준이라 동일)
  - [x] `id: P-02` 가 유지된다 (경로만 바뀌었다)
  - [x] `products/kknaks-profile` 참조가 레포에 0건
- **완료 증거**:
  - `templates/product/showcase.md` 신설. **같은 디렉토리의 다른 템플릿과 형태가 다르다** — `baseline.md` 등은 손으로 복사하는 골격이지만 showcase 는 등록 화면이 입력값으로 **렌더**하므로, `templates/persona/daily.md`·`career.md` 와 같은 **형식 SoT 문서**로 썼다. 머리에 "이 파일은 복사 대상이 아니다" 를 못박아 D3 화이트리스트와 어긋나지 않게 했다.
  - **템플릿에 담은 것 넷.** ① `id: P-NN` 채번이 코드 소유이고 **결번을 재사용하지 않는** 이유(자산 경로 `/assets/projects/P-NN/` 가 그 번호를 쓴다 — 재사용하면 과거 이미지가 새 프로젝트에 붙는다) ② **`category` 는 이 템플릿이 아니라 `persona/_meta.yaml` 이 소유한다**는 것과 어겼을 때의 결과(파일 하나가 아니라 persona 로드 전체 실패 → 사이트가 옛 데이터 서빙) ③ `links.repo` 는 표시 전용이고 추적은 레지스트리 소유(DEC-014 D1) ④ PDF 케이스 스터디 블록은 **새 카드에 넣지 않는다** — 빈 필드를 미리 깔면 "채워야 할 것" 과 "안 쓰기로 한 것" 이 구분되지 않는다.
  - 제품 트리 정리 실측: **18개 → 12개**, showcase **13 → 8**. `git mv` 로 `P-02` 가 `products/kknaks-dev/showcase.md` 로 이동했고 회사 5개는 디렉토리째 제거했다(`showcase.md` 하나뿐이라 파일만 지우면 빈 디렉토리가 검증 에러가 된다).
  - **로더 실측으로 무영향 확인**: `projects` 8건 로드 · `visible` **6건 그대로**(`P-02`·`P-03`·`P-04`·`P-05`·`P-06`·`P-10`) · `P-02` 경로가 `kknaks-dev/showcase.md` 로 바뀐 것 확인 · 그래프 **nodes 284 / ERROR 0 / WARN 0** · 빈 디렉토리 0. `visible` 이 안 줄었으므로 `/api/projects` 와 포트폴리오 PDF 양쪽에 **화면 변화가 없다.**
  - `products/kknaks-profile` 경로를 가리키는 살아 있는 참조 0건. 남은 문자열은 WORK-004 의 과거 기록과 무관한 User-Agent 뿐이다.
  - `products/README.md` 를 **9행 → 12행**으로 맞추고, 갱신 주체(D15)와 **회사 제품이 여기 없는 이유**(D9 — 회사 레포는 문서 트리도 카드도 없이 레지스트리에만 산다)를 명시했다.
  - `agent.md` 「별도 계열」이 셋 → **넷**. 카드가 제품 문서와 같은 폴더에 있으면서 **성격이 반대**라는 것(내부 결정 vs 공개 한 장)과, 그래서 그래프 노드가 아니라는 것을 적었다.
  - 스캐폴드가 읽을 양식과 시드가 기준 삼을 목록이 둘 다 확정됐다 — **P2 의 전제가 닫혔다.**

### Phase 2 — 스키마 + repository 계층 (BE)

- **Status**: TODO
- **설명**: 컬럼 하나를 추가하고, **`repository/` 계층을 신설한다.** 이 발주에서 계층 규약이 실제로 서는 지점이라 첫 입주자가 본이 된다.
- **작업**:
  - [ ] `alembic/versions/0009_*.py` — `tracked_repos.product_slug` nullable 추가
  - [ ] `core/models.py` — `TrackedRepo` 컬럼
  - [ ] **`service/products/dto.py`** — 도메인 DTO(pydantic). `TrackedRepoDTO` 가 계층을 넘는 유일한 형태
  - [ ] **`repository/` 신설** — `tracked_repos.py` 에 조회·생성·수정·클론상태 갱신. `select()` 가 사는 유일한 자리이고 **ORM → DTO 변환을 여기서 끝낸다**
  - [ ] `service/jobs/repo_registry.py`·`repos.py` 의 **기존 `select()` 를 repository 로 옮긴다** — 이 도메인은 이번에 만지므로 규약 ②에 해당한다
  - [ ] `sync_all` 의 **ORM 직접 대입을 `mark_synced`/`mark_failed` 로 교체** — ORM 이 계층 밖으로 새던 자리다
  - [ ] `app/scripts/seed_repo_registry.py` — 기존 13행에 `product_slug` 매핑 + **신규 4행 추가**(`ax-graph`·`gcs_demo`·`lunch_game`·`mac-remote`, 전부 studio·personal)
- **검증**:
  - [ ] `alembic check` 드리프트 없음 (`test_models_and_migrations_agree`)
  - [ ] 시드 후 17행, `product_slug` 가 전부 실재 디렉토리를 가리킨다
  - [ ] `kknaks/kknaks_profile` → `kknaks-dev` (P1 통합 결과)
  - [ ] **잔디 경로 회귀 없음** — `collect_git` 가 17개를 조사하고 `career_map` 이 종전과 같다
  - [ ] `repository` 밖에서 `TrackedRepo` 를 `select()` 하는 코드가 없다 (테스트로 고정)
  - [ ] **`repository` 밖으로 ORM 객체가 나가지 않는다** — 반환 타입이 전부 DTO 다
- **완료 증거**: 미작성

### Phase 3 — service + API (BE)

- **Status**: TODO
- **설명**: 등록·CRU·발견을 만든다. **LLM 을 호출하지 않는다** — 전부 복사·치환·검증이고 비동기로 도는 것은 클론뿐이다.

#### 3-A. 등록과 스캐폴딩

- **작업**:
  - [ ] `utils/slug.py` — 레포/제품 slug 파싱·정규화 (순수 함수, 도메인·DB 무지)
  - [ ] `service/products/validate.py` — 사전 검증 7종 + 도메인 예외. **분류는 `_meta.yaml` 목록과 대조**
  - [ ] `service/products/scaffold.py` — **화이트리스트 6 파일** 복사 · 카드 렌더 · `P-NN` 채번(max+1)
  - [ ] `service/products/registry.py` — 등록 오케스트레이션. studio/company 분기, 커밋 1개, **push 실패 시 커밋 롤백**
  - [ ] `products/README.md` 행 자동 추가 (같은 커밋)
  - [ ] 클론은 `BackgroundTasks` 로 예약하고 **즉시 응답**
- **검증**:
  - [ ] `studio` 등록이 골격 6 + 카드 + README 행을 **한 커밋**으로 만든다
  - [ ] `company` 등록이 **파일을 하나도 만들지 않는다**
  - [ ] **제품 2개를 연속 등록해도 부팅·그래프 검증이 통과한다** — 예시 문서가 복사되지 않았다는 회귀 테스트
  - [ ] 화이트리스트가 코드 상수이고 테스트가 목록을 고정한다
  - [ ] 검증 실패 시 파일이 하나도 생기지 않는다 (7종 각각)
  - [ ] 허용 목록 밖 분류가 거부된다 — 통과했다면 persona 로드 전체가 죽는다
  - [ ] push 실패 시 로컬 커밋이 남지 않는다
  - [ ] `P-NN` 이 max+1 이고 결번을 재사용하지 않는다

#### 3-B. CRU · 재동기화 · 미등록 발견

- **작업**:
  - [ ] `service/products/discover.py` — 계정·조직 레포 목록 → `owner`·`fork`·`archived` 필터 → 레지스트리 diff
  - [ ] **`api/schemas/products.py`** — 요청·응답 pydantic. **도메인 DTO 와 별개 클래스다**
  - [ ] `api/routers/products.py` — 엔드포인트 6 · 도메인 예외 → HTTP 매핑(`_gate_error` 형태)
  - [ ] 목록 응답의 파생 둘 — 제품 디렉토리 실재 여부 · 카드 노출 값(읽기 전용). **DB 에 저장하지 않는다**
  - [ ] `main.py` 라우터 등록
- **검증**:
  - [ ] 미등록 조회가 fork·아카이브·타인 레포를 거른다
  - [ ] **미등록 조회가 실패해도 목록 API 는 200 이다**
  - [ ] `enabled` 를 껐다 켜도 행·클론이 유지된다
  - [ ] `product_slug` 가 실재하지 않아도 저장되고 응답에 경고가 실린다
  - [ ] 잘못된 레포 등록 시 `last_error` 에 사유 코드가 남는다
  - [ ] **라우터에 `select()` 가 없다** (계층 규약 테스트)
  - [ ] service 가 `HTTPException` 을 던지지 않는다
  - [ ] **응답 모델과 도메인 DTO 가 별개 클래스다** — 라우터가 DTO 를 그대로 반환하지 않는다
- **완료 증거**: 미작성

### Phase 4 — 화면 (FE)

- **Status**: TODO
- **설명**: 프로젝트 슬롯을 연다. 사람이 실제로 눌러 보는 것이 이 Phase 의 완료 조건이다.
- **작업**:
  - [ ] `sidebar.tsx` — 프로젝트 `ready: true`
  - [ ] 미등록 배너 — 0건이면 숨김, 칩 클릭 시 폼 프리필, 조회 실패해도 표는 렌더
  - [ ] 레지스트리 표 — 제품 드롭다운 · 커리어 드롭다운 · `긁기` 토글 · **`노출` 읽기 전용** · 클론 상태 · 재동기화
  - [ ] 새 제품 폼 — `company`/`studio` 분기, 분류 드롭다운, 필드별 오류 표시
  - [ ] 클론 진행 폴링
- **검증**:
  - [ ] `tsc --noEmit` · `next build` 통과
  - [ ] 사람이 등록·수정·토글·재동기화를 눌러 봤다
  - [ ] `⚠ 제품 폴더 없음` 과 `✕ 사유코드` 가 실제로 보인다
  - [ ] `노출` 열이 눌리지 않는다
- **완료 증거**: 미작성

### Phase 5 — 배포 + 실운영 완주 (Ops)

- **Status**: TODO
- **설명**: 이 발주가 실제로 문제를 풀었는지 확인하는 유일한 Phase 다. **관측 대상이 화면이 아니라 잔디다.**
- **작업**:
  - [ ] 배포 — 마이그레이션 `0009` + 시드 재실행(신규 4행)
  - [ ] 서버에서 신규 레포 4개 클론
  - [ ] 화면에서 제품 1건 실제 등록 → origin/main 에 커밋이 나가는 것 확인
  - [ ] 다음 09:05 잔디 관측
- **검증**:
  - [ ] 실 등록 커밋이 `origin/main` 에 있고 `product_doc_pipeline` 이 통과한다
  - [ ] **그날 daily 의 `counts` 에 신규 레포 커밋이 잡힌다** — 이것이 "한 달 57건 누락" 이 닫혔다는 증거다
  - [ ] 배너의 미등록 건수가 등록 후 줄어든다
  - [ ] 기존 잔디·유튜브 파이프라인에 회귀가 없다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 마이그레이션 `0009` 가 **컬럼 추가뿐**이고 기존 13행 데이터를 건드리지 않는다
- [ ] 신규 레포 4개 클론 디스크 여유 (기존 ~290M 위에 추가분)
- [ ] `GH_TOKEN` 계정 권한이 신규 레포 4개를 읽을 수 있다 (`gcs_demo` 는 `kknaksss` 소유 — 계정이 갈린다)
- [ ] admin API 응답에 토큰·경로 절대값이 실리지 않는다 (`_scrub` 경유)
- [ ] 미등록 발견이 **회사 조직 레포를 화면에 노출**하는데, 그것이 의도한 범위인지 확인
- [ ] 스캐폴드가 쓰는 경로가 `products/` 밖으로 나갈 수 없다 (traversal 차단)
- [ ] P1 의 파일 삭제가 `/api/projects`·PDF 에 영향 없음을 배포 전 로컬에서 확인

## Rollback

- **P1** — git revert. 파일 이동·삭제뿐이라 되돌리면 원상태다.
- **P2** — `alembic downgrade` 로 컬럼 제거. 컬럼이 nullable 이라 **기존 잔디 경로는 컬럼이 없어도 돈다**(아무도 안 읽는다).
- **P3** — 라우터를 `main.py` 에서 미등록하면 표면이 사라진다. service·repository 는 호출자가 없으면 무해하다.
- **P4** — `sidebar.tsx` 의 `ready: false` 로 되돌리면 진입점이 닫힌다.
- **P5** — 등록으로 생긴 제품 디렉토리는 git revert. 클론은 볼륨에서 지우면 다음 조사에서 다시 받는다.
- 부분 revert 시 영향: **P2 만 남기고 P3 이후를 되돌려도 안전하다** — 컬럼은 아무도 안 읽는다. 반대로 P1 만 되돌리면 P2 시드 매핑이 깨진다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] SPEC-014 의 수용 조건 14개가 전부 검증됐다.
- [ ] 계층 규약이 신규 코드에 지켜졌다 — 라우터에 `select()` 없음, service 에 `HTTPException` 없음이 테스트로 고정됐다.
- [ ] `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **스캐폴드 화이트리스트의 장기 유지.** 템플릿에 예시 문서가 추가되면 목록이 조용히 어긋난다. 테스트가 목록을 고정하지만, "템플릿에 새 파일이 생겼는데 복사 목록에 없다" 를 감지할지는 P3 에서 판단한다.
- **미등록 발견의 회사 조직 범위.** 조직 레포 전체가 뜨면 본인이 손대지 않은 것까지 배너에 오른다. `owner` 필터만으로 부족하면 "본인 커밋이 있는 것만" 으로 좁힐지 P3 에서 실측 후 정한다.
- **`gcs_demo` 의 계정.** `kknaksss` 소유라 `PERSONAL_OWNERS` 에는 있지만 토큰이 실제로 읽히는지는 P5 클론에서 확인된다.
- **P1 의 회사 5개 삭제가 되돌릴 수 없는 유일한 항목이다.** git 이력에는 남지만, 되살릴 이유가 생기면 `showcase.md` 를 새로 쓰는 편이 빠르다.

## Related

- SPEC: frontmatter `links.specs` 참조
- 계층 규약: `40-architecture/system/README.md` 「백엔드 계층 규약」
