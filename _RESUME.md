# 재개 노트 — kknaks_profile 리뉴얼

**지금**: `app/back/` 이 섰다. 어드민 CRUD 11메뉴 + 시드 + **공개 API 여섯 전부**가 로컬에서 돈다.
**다음**: 두 갈래 병행 — ① 백그라운드: 잔디(commit 수집)·인박스(유튜브/블로그 캡처,
queue — erd §미결 7 부터) ② 메인: 문서·DB 상세 내용 채우기(이력서 원료 —
problem 0건·career description 공백. 페이지 하나씩).

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

- [ ] **상세 내용 채우기(다음)** — 표면·수집은 다 섰고 알맹이가 비었다. `problem` 0건,
      career `description` 공백 다수, education `detail_path` 공백 2건. 이력서 원료가
      되게 `/career` 부터 한 역할씩 인터뷰로 채운다(메인 세션). 원료는
      `para/projects/company/*/log/` SUMMARY 들
- [ ] **과거 커밋 복구** — 잔디 수집이 `git_token` 의 (account,email) 로 「내 커밋」을
      거른다. 2026-08-03 신원 통일 이전 커밋은 옛 이메일이라 잘렸다(mac-remote 129→17
      등). 옛 이메일들을 신원 집합에 더하는 방식 — 이메일 확보 후 발주
- [ ] `.agent/` — 규칙·훅·스킬·템플릿. 케이스 2 pre-commit, 케이스 4 스킬. **코드 계층
      규약 문서화도 여기** — 지금은 코드가 모범일 뿐
- [ ] mediness 검토 — `visible=false`. 내용 확인 후 켜고, AI 개발자 역할 재연결
- [ ] **prod 배포** — push 켜기(`JOB_GIT_PUSH_DRY_RUN=0`)·홈서버(profile-api)·워커
      systemd·`.env` 경로 서버 기준(`AI_CWD`·`AI_SCHEMA_DIR`·`LEDGER_PATH`). 배포하는 날
- [!] push 를 아직 안 했다 (로컬 커밋만, `origin/renewal` 은 `5c0ab54`)

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

`erd.md` §미결 과 `case_flow.md` 의 「아직 안 정한 것」이 정본이다. 큰 것만:

- `app/back/` 계층 규약 — CLAUDE.md 4 번
- `product` 가 어느 표면에 뜨나 — 지금 `/career` 펼침 안에만 있다
- `detail_path` 가 끊기면 — 파일을 옮기거나 지웠을 때 DB 가 모른다
- `personal/` 이 갖는 md — SoT 는 DB. 시드 넣고 나서 정한다
- 발행물(이력서·공개 글)의 자리 — `persona-artifacts.md` 의 posts 규정이 갈 곳 없음
- `category` 목록의 소유자 — 옛 `_meta.yaml` 이 없어졌고 DB 는 `varchar(32)` 로 안 막는다
- **codex stem 채번을 못 믿는다** — 서버가 max+1 로 강제 중(youtube). 근본은 프롬프트가
  원장을 못 읽던 것(해결)이나, 강제 레이어는 남겨 둔다

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

- `2026-08-26` **인박스 크롤링 완결 — 네 종류가 다 선다** — docs·article·blog 를
  레거시 `web.py` 3단계로: 정적(httpx+trafilatura) → JS 마커·본문 500자 미만이면
  playwright chromium 동적 렌더 → 실패(단계·사유 코드). **페이월·봇 차단(Cloudflare
  403)은 우회 없이 즉시 failed**(wikidocs 실측). Dockerfile 에 chromium. E2E:
  GeekNews blog 착지 성공. **케이스 1 개정 — 문서 게이트 제거**: 서버 검증(양식 절 ·
  실행 실패 흔적 · 채번 강제) 통과 시 **자동 착지**, 승인은 concept 하나. 실측 버그
  둘 잡음 — ① 컨테이너 안 codex sandbox(bwrap) 초기화 실패로 셸 전부 죽어 실패문이
  초안으로 나옴 → `sandbox=danger-full-access`(격리는 컨테이너+ro 마운트가 맡음),
  resume 호출은 `--sandbox` 를 거부해 `-c sandbox_mode` config 로 ② **dry-run 재정의**:
  「커밋·푸시 둘 다 안 함」(md 파일만, `commit_ref="dry-run"` 마커). published_on 은
  착지일 KST 강제(영상 게시일 아님 — 목록 정렬). 인박스·승인 대기 한 화면(행 펼침)
- `2026-08-25` **잔디 완결 — 수집·AI 요약·`/about`** — repo 어드민(제품/프로젝트 폼
  안 레포 섹션 + GitHub 불러오기 모달, owner 는 `product→career→company` 로 스코프)
  · `git_token`(Fernet 암호화, 키는 `.env GIT_TOKEN_KEY`, 회사 연결·활성 토글) ·
  GitHub 수집기(**내 신원 필터**=git_token (account,email) · **전 브랜치** · 매일 KST
  08:00 · 레포별 격리) · **커밋 AI 요약 → `daily` 표**(날짜당 codex 1호출, 최근 7일 창
  자동, `scripts/backfill_daily.py` 로 과거 하나씩, 실패는 daily.error) · 어드민 커밋
  히스토리(월 스트립 잔디·동적 레포 칩·데일리 카드). 회사 커밋은 사내 정보 추상화.
  **워커 컨테이너화**(compose worker, codex 는 이미지에 안 굽고 리눅스 CLI 번들 런타임
  마운트 — mediness action-runtime-review 패턴). **erd 4표 신설**: `queue`·`gate`·
  `git_token`·`daily` + `repo.git_token_id`·`commit.summarized_at`·`company.github_org`.
  §미결 7 해소. back 도커화(48000, `docker-compose.local.yml`)
- `2026-08-25` **`GET /api/algorithms` + `/algorithms` 완결 — 공개 API 여섯이 다 섰다** —
  **slug 결정: detail_path 파일명 stem 소문자(`a-001-two-sum`)**, frontmatter `id`(A-001)가
  아니다. DB 94행 UPDATE + 시드의 slug 파생도 stem 소문자로 동기(재실행이 안 되돌린다).
  목록은 visible=true 만 service 가 거르고(erd §미결 3) totalCount + today 한 건을 meta 로
  (그 한 건이 visible=false 면 null — 숨긴 문제를 meta 로 안 드러낸다). 상세의 단계 구조
  (problem·clarifying·approach·logic·trace·solution)는 md `## Data` fenced yaml 에서 파싱
  (pyyaml 의존성 추가) — 원장의 {ko,en} 이중 축은 ko 로 접는다(표면은 한국어 하나).
  yaml 이 없거나 깨지면 500 대신 단계별 빈 구조 — 컴포넌트의 빈 상태 문구가 받는다.
  이웃(newer/older)은 published_on DESC NULLS LAST, id DESC 정렬의 이웃(repo
  list_published 소유, 어드민 정렬과 달리 today 를 앞세우지 않는다). 원장 94건 yaml
  편차 0. 프론트 무수정
- `2026-08-25` **`GET /api/contents` + `/contents` 완결** — 목록(visible 필터·`?limit=`·
  totalCount)과 상세(body + newer/older). 이웃 기준 정렬은 `published_on DESC NULLS
  LAST, id DESC`(repo list_visible 이 소유). 끊긴 detail_path 는 계약(body: string)에
  맞춰 빈 문자열. subtitle·intro 는 안 내림(프론트 기본문구). 프론트 무수정.
  notes 와 병렬 작업 — main.py 충돌 없이 합류
- `2026-08-25` **`GET /api/notes` + `/notes` 탐색기 레이아웃** — 목록은 visible=true 만
  service 가 거르고(erd §미결 3) `?limit=`(기본 50)·totalCount. 상세(`/{slug}`)는
  body(read_detail — frontmatter 는 서빙에서 뗀다)+newer/older(published_on 정렬의
  파생 이웃). **`folder` 파생 필드 결정** — detail_path 의 note/ 이하 첫 디렉토리명,
  컬럼이 아니라 경로의 파생(분류 SoT 는 원장 디렉토리 8폴더). 프론트는 목록형을
  탐색기형으로 교체 — 왼쪽 디렉토리 트리(폴더+노트 수), 오른쪽 md 뷰. `/notes` 와
  `/notes/[slug]` 가 NotesExplorer 하나를 공유, 트리 클릭은 클라이언트 fetch +
  history.replaceState(펼침 상태 유지), 직접 URL 진입은 서버가 채운다.
  notes-list.tsx 삭제
- `2026-08-25` **showcase.md 는 본문만 — frontmatter 제거 9건** — 메타 SoT 가 DB 로
  갔으므로 md 의 frontmatter({ko,en}·P-NN·visible)는 낡은 둘째 원천이었다. 서빙
  (`read_detail`)도 frontmatter 를 떼고 내려준다 — note 등 frontmatter 를 유지하는
  원장의 body 누출 방지. `templates/projects/showcase.md` 양식 재작성(DB 소유 표·
  assets 규약·i18n/PDF 블록 제거)
- `2026-08-25` **자산 규약 — 이미지는 원장 옆 `assets/`** — para/projects/summer-star/
  `<slug>/assets/cover.png`. DB thumbnail 은 para 상대경로, 서빙은 `GET /api/assets/{path}`
  (para 하위·이미지 확장자만, 경로 탈출 차단). showcase.md 본문의 상대참조 이미지도
  같은 라우터로 풀린다(프론트 urlTransform). 프론트 public 의 프로젝트 커버 복사본
  제거 — 원천 하나. 커버 6장(P-02~P-10) `_archive` 에서 끌어올림
- `2026-08-25` **`GET /api/projects` + `/projects` 완결** — visible=true 만 service 가
  거르고(erd §미결 3), 메타는 totalCount + category GROUP BY 파생(count 내림차순, NULL
  제외). 상세는 별도 API 없이 목록 각 항목에 detail_path md 전문을 body 로 싣는다 —
  항목이 적어서. md 읽기는 `core/detail.py` 공용 헬퍼로 추출(education 읽기도 교체).
  프론트 무수정
- `2026-08-25` **`GET /api/career` + `/career` 완결** — career(회사 조인: org·location·
  orgDescription)+education 합류, 역할 펼침 = description(컬럼, md 원장 없음)+product
  카드(visible 필터)+problem 목록. 좌측 메타의 연차·focus 는 profile 재사용(원천 하나).
  education body 는 detail_path md 읽기(첫 구현). 프론트: types 에 CareerProduct/
  CareerProblem 추가, 타임라인 펼침에 두 섹션. **erd §미결 2(커밋만 센다)·3(visible 은
  공개 API 가 거른다) 확정.** problem 은 시드가 없어 어드민에서 넣어야 뜬다
- `2026-08-24` **`repo`·`commit` 표 + `GET /api/activity`** — erd 14표가 모델로 다 섰다.
  잔디는 commit 을 `authored_at::date` 로 묶은 파생(counts 는 erd §미결 2 대로 commit 만).
  날짜는 `YYYY.MM.DD` 점 구분 — ContribGrass 가 문자열 키로 비교해서다. 프론트 무수정.
  `/about` 완결 — 커밋 수집(케이스 6·7)이 서기 전까지 빈 격자가 내려간다
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
