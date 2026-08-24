# 재개 노트 — kknaks_profile 리뉴얼

**지금**: `app/back/` 이 섰다. 어드민 CRUD 11메뉴 + 시드 전체가 로컬에서 돈다.
**다음**: 공개 API(블로그 페이지 살리기) 또는 수집함(queue — erd §미결 7 부터).

브랜치 `renewal` · 원격 `origin/renewal` 은 `5c0ab54` (**push 안 함**)

> **이 문서의 규칙 — 절마다 수명이 다르다**
>
> | 절 | 수명 |
> |---|---|
> | §1 지금 | **덮어쓴다.** 닫히면 지우고 §6 으로 내린다 |
> | §2 정할 것 상태 | 항목이 닫힐 때만 |
> | §3 문서 지도 | 구조가 바뀔 때만 |
> | §4 열린 것 | 정해지면 지운다 |
> | §5 하지 않기로 한 것 | 추가만 |
> | §6 이력 | append-only, 최신이 위 |
>
> 늘어나는 것은 §6 하나뿐이다. §1 이 길어지면 규칙을 어긴 것이다.

## 1. 지금

- [ ] **공개 API** — 어드민만 섰다. `/api/career`·`/api/projects`·`/api/notes`·
      `/api/contents`·`/api/algorithms`·`/api/activity` 공개 GET 이 없어 블로그
      페이지들이 죽어 있다 (`/`·`/about` 만 산다). 상세 md 렌더(detail_path 읽기)도 여기
- [ ] **수집함** — 케이스 1(자료 캡처)·케이스 6(problem 게이트). `queue` 표(erd §미결 7)를
      먼저 정한다. 어드민 자리(`/admin/capture`·`/admin/approvals`)는 공란으로 서 있음
- [ ] `.agent/` — 규칙·훅·스킬·템플릿. 케이스 2 의 pre-commit, 케이스 4 의 스킬이 여기.
      **코드 계층 규약 문서화도 여기** — 지금은 코드(company·career 슬라이스)가 모범일 뿐
- [ ] mediness 검토 — `visible=false`. 내용 확인 후 켜고, AI 개발자 역할을 나누면
      제품의 역할 재연결
- [!] push 를 아직 안 했다

## 2. CLAUDE.md 「정할 것」 상태

| # | 항목 | 상태 |
|---|---|---|
| 1 | 작업 주체 경계 | 정해짐 — `case_flow.md` 「세 방향」 |
| 2 | 문서 ↔ DB SSOT | 정해짐 — `erd.md` · `database.md` |
| 3 | 자동화 승인 게이트 | 정해짐 — `case_flow.md` 케이스 7 |
| 4 | 코드 규약 | 정해짐(구현으로) — router→service→repo · DTO(내부)/schemas(계약) 분리 · 도메인 예외 · 요청 단위 트랜잭션. **문서화 미작성**(`.agent/` 몫) |
| 5 | 기록의 층 | 정해짐 — 케이스 3 · 6 · 7 |
| 6 | 디렉토리 · 에이전트 규칙 | 디렉토리 ○ · **문서 라우팅 ○** / 훅·스킬 ✗ (`.agent/` 미착수) |

## 3. 문서 지도

`agents.md → para/para.md → 버킷 문서` 로 내려간다. 규칙은 버킷 문서가, 양식은 `templates/` 가 갖는다.

| 문서 | 무엇 |
|---|---|
| `CLAUDE.md` | 왜 리뉴얼하는지. 정할 것 6 |
| `agents.md` | 진입 인덱스 — 루트 · 문서 라우팅 |
| `architecture.md` | 루트 계약 — `para/` · `app/` · `orchestration/` |
| `para/para.md` | 네 버킷의 경계 |
| `para/areas/area.md` | `personal/`·`concept/` — 아홉 영역 · 분류 기준 · 개념 규약 · 맵 366 |
| `para/projects/project.md` | `company/`·`summer-star/` — 단계 00~70 규칙집 · 맵 14 |
| `para/resources/resource.md` | 출처 여덟 — note 하위 · 불변 규약 |
| `erd.md` | **스키마 정본.** mermaid + DDL 14 표 |
| `database.md` | 표면별 컬럼 추출과 그렇게 정한 근거 |
| `case_flow.md` | **동작 정본.** 케이스 7 |
| `orchestration/runbook.md` | 코디네이터 런북 |
| `templates/` | 양식 — `areas/` · `projects/` · `resources/` |
| `_migration/01-concept.md` | concept 366 분류 이력 (중간 산출물) |

`_archive/` 는 리뉴얼 이전 레포 전체. **읽기 전용이다.** 이관이 끝났으므로 지울 수 있다 —
지우면 옵시디언 stem 중복도 함께 사라진다.

## 4. 열린 것

`erd.md` §미결 7 과 `case_flow.md` 의 「아직 안 정한 것」이 정본이다. 큰 것만:

- **`queue` 표가 스키마에 없다** — 케이스 1 이 쓰는데 `erd.md` 에 정의가 없다 (§미결 7)
- `app/back/` 계층 규약 — CLAUDE.md 4 번
- `product` 가 어느 표면에 뜨나 — 지금 `/career` 펼침 안에만 있다
- `detail_path` 가 끊기면 — 파일을 옮기거나 지웠을 때 DB 가 모른다
- 개인 프로젝트에 회고가 필요한가 — 잔디잡이 읽을 것이 커밋 메시지뿐이다
- `personal/` 이 갖는 md — SoT 는 DB. 시드 넣고 나서 정한다
- 발행물(이력서·공개 글)의 자리 — `persona-artifacts.md` 의 posts 규정이 갈 곳 없음
- `category` 목록의 소유자 — 옛 `_meta.yaml` 이 없어졌고 DB 는 `varchar(32)` 로 안 막는다

## 5. 하지 않기로 한 것

되돌리려면 근거부터 다시 봐야 한다.

- **`/print`(이력서)** — 사이트 밖에서 관리한다
- **i18n** — 한국어 하나만. 영문 표면이 필요해지면 그때 번역 축을 얹는다
- **`areas/concept/` 공개** — 내가 쓰려고 쌓는 것이지 보여주려고 쌓는 것이 아니다
- **개인 프로젝트 오케스트레이션** — 당분간 단일 에이전트. 회사 일에서 먼저 검증한다
- **`book`·`session` 캡처 로직** — v1 은 버튼만
- **알고리즘의 개념 축적** — 매일 자동으로 도는 것이라 잡음이 쌓인다
- **`context/` 11 건 이관** — 라우팅·기준은 새 문서가 대체했고 사람·현황은 DB 원장.
  작업 종류 표 하나만 `project.md` 3.1 로 흡수했다
- **source 의 유튜브 노트 4건** — content(C-0NN)가 유튜브 출처층. 같은 영상을 두 층에 안 둔다
- **md frontmatter 의 파이프라인 상태** — `status`·`enriched_at` 류는 DB(`queue`)가 갖는다

## 6. 이력

- `2026-08-24` **`app/back/` 구축** — FastAPI·SQLAlchemy 2.0 async·uv·alembic·compose(postgres).
  계층: router→service→repo, dto(내부)/schemas(front 계약, camelCase alias), 도메인 예외,
  get_db 가 요청 단위 commit. 인증은 레거시 쿠키 JWT 계약 그대로. 표 12개 모델+어드민
  CRUD 11메뉴(수집함 2는 공란) + 시드(profile·site_config 8키·company 3·career 3·
  product 1·education 2·content 25·algorithm 94·note 144). **erd 개정 2건** —
  ① profile 은 신원·연락·스택만, 문구는 전부 site_config(jsonb value)로 ② product 를
  company→career 종속으로(재직기간 파생은 경계 판정 불가라 폐기). 어드민 모바일(햄버거),
  케이스 2 디렉토리 게이트·역할/회사 삭제 가드·today 단일 강제 구현
- `2026-08-24` **`_archive/` → `para/` 이관 완료** — concept 366(아홉 영역, 워커 10 분류)
  · products 486(13 제품 통째) · note 144(8 폴더) · youtube 25(C-026 신규, 상태 5종 제거,
  개념 up: 14건 C-0NN 재지정) · algorithms 94 · context 는 표 하나만 흡수하고 종결.
  버킷 문서 3종(`area`·`project`·`resource`) + `para`·`agents` 재작성, `templates/` 26종,
  회사 showcase 3건(P-17~19), worker-brief §1 개념 자리, erd §미결 7(queue) 추가
- `2026-08-24` 프론트 이관(54 파일·tsc 0) · `case_flow.md` 케이스 7 · `career` 재설계
  (`company`·`problem` 신설) · `site_config` 신설
- `2026-08-23` `erd.md` 스키마 정본 · `profile` 루트 · 상세는 `detail_path` 로 md
- `2026-08-23` `para/` 네 버킷 · `areas/concept` 아홉 영역 · `projects`·`archive` 를
  `company`/`summer-star` 로 가름
- `2026-08-23` 루트 3 분할 · `orchestration/` 골격(orca_settings 이식)
- `2026-08-21` 리뉴얼 시작 — 이전 전부 `_archive/` 로
