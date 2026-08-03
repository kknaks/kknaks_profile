# kknaks-dev

## 목적

`kknaks.dev`와 이 레포 자체를 제품으로 운영하기 위한 SSOT다.

규칙: `rules/product-doc-pipeline.md`

## 현재 상태

| Area | Status | Next |
|---|---|---|
| 지식그래프 (BL-001) | WORK-001~010 done + **WORK-013으로 4층 재편 완료** (`permanent/concept/` 실재화, lineage 1→4) | — |
| 앱 DB화 + 관리자 인증 (BL-002) | BL-002·DEC-009 accepted, SPEC-006 implemented, WORK-011 done (async) | 후속 — admin 실제 관리 기능 spec |
| inbox 승인 파이프라인 + concept 층 (BL-003) | BL-003·DEC-010~013 accepted · spec 9건 · 40-arch · **WORK-012·013 done** · **WORK-014 done** · WORK-015 P1~P4(게이트 3종·재오픈·Executor) done | WORK-015 P5 실전 e2e (**배포 필요**) |
| 커밋 잔디 파이프라인 (BL-004) | BL-004 accepted · DEC-014~016 · SPEC-011~013 · **WORK-017 done (2026-08-03)** — 서버 하루치 실 push 완주 | 후속 — `algorithms`·`content_enrich` 게이트 편입 (새 baseline) |
| 제품·프로젝트·커리어 연동 (BL-005) | **BL-005 (raw) · DEC-017 (proposed, D1~D17, OQ 0) · SPEC-014 (draft) · 40-arch 계층 규약 · WORK-018 발주 (todo, 5 phase)** — 2026-08-03 | **P1 착수** — 형식 SoT + 제품 트리 정리 (코드 0줄) |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |

## 최근 로그

- 2026-08-03 **KDEV-WORK-018 발주 (todo)** — 제품 레지스트리, 5 phase. **P1 형식 SoT + 제품 트리 정리(코드 0줄)** — `templates/product/showcase.md` 신설 · `kknaks-profile`→`kknaks-dev` 통합 · 회사 5개 삭제 · `products/README.md` 정정 · Remote `TBD` 3곳 정정. **맨 앞인 이유 둘**: 스캐폴드가 읽을 양식이 없으면 P3 가 형식을 지어내 SoT 가 둘이 되고(017 P1 과 같은 이유), 시드 매핑은 **통합 뒤의** 목록을 기준으로 해야 한다(`kknaks-profile` 이 남아 있으면 `kknaks/kknaks_profile` 을 어디로 보낼지 코드가 정할 수 없다) / **P2 컬럼 + `repository/` 계층 신설**(계층 규약 첫 입주자. 이 도메인은 이번에 만지므로 `repo_registry`·`repos` 의 기존 `select()` 도 함께 이동 — 규약 ②) + 17행 시드 / **P3 service+API** — 3-A 등록·스캐폴딩(화이트리스트 6 파일·사전 검증 7종·커밋 1개+push 실패 롤백·`P-NN` 채번), 3-B CRU·재동기화·미등록 발견 / **P4 화면** / **P5 배포+실운영**. **완료 판정이 화면이 아니라 잔디다** — 신규 레포 커밋이 그날 `counts` 에 잡혀야 "한 달 57건 누락" 이 닫힌다. 롤백 설계: 컬럼이 nullable 이라 **P2 만 남기고 P3 이후를 되돌려도 안전**(아무도 안 읽는다), 반대로 P1 만 되돌리면 P2 시드가 깨진다. Open Issue 4 — 화이트리스트 장기 유지(템플릿에 파일이 늘면 조용히 어긋난다) · 미등록 발견의 회사 조직 범위 · `gcs_demo` 계정(`kknaksss`) 토큰 · **P1 의 회사 5개 삭제가 유일하게 되돌리기 번거로운 항목**.
- 2026-08-03 **KDEV-SPEC-014 작성 (draft) + 40-architecture 「백엔드 계층 규약」 신설** — SPEC-014 는 제품 레지스트리의 **외부 계약**(등록 흐름·검증 사유코드 7종·Case Matrix·상태·수용조건 14). **계층 구조는 SPEC 에 넣지 않았다** — 템플릿이 *"repository/service 구조는 두지 않는다"* 로 막고 있고, 계층은 *"여러 작업이 공유하는 장기 구조"* 라 `40-architecture/system/` 이 제자리다. 규약: **api → service → repository**, 공용 순수함수는 `utils`, 횡단은 `core`. 계층별 금지 4종(api 의 `select()`·service 의 `HTTPException`·repository 의 도메인규칙/외부I/O·utils 의 의존). 예외는 도메인 예외로 올리고 라우터가 매핑 — **선례가 이미 있다**(`GateError` → `queue.py:414 _gate_error()`). 현행 실측: **`repository` 계층이 없고** `queue.py` 690줄이 `select()` 를 8회 직접 호출, service 9개 파일도 직접 호출, `utils/` 는 파일 하나. **적용은 신규만** — 레거시 일괄 리팩터를 하지 않는다(WORK-017 이 구 경로 제거를 P5 한 곳에 가둔 것과 같은 이유. `queue.py` 는 승인 파이프라인 전체가 지나는 길목이다). 새 코드가 `queue.py` 의 직접 쿼리를 패턴으로 복사하지 않게 명시.
- 2026-08-03 **KDEV-DEC-017 D17 추가** — **미등록 레포 발견.** D12 만으로는 재발을 못 막는다(오늘 4개를 채울 뿐 다음 달에 또 샌다). 근본 원인은 레지스트리가 `showcase.md` 에서 시드돼 **사각지대를 그대로 물려받았고** 이후 발견 장치가 없다는 것 — 모듈에 `seed_from_showcase`(1회)와 `enabled_repos`(조회)뿐이다. 실패가 침묵한다: 레포를 파도·커밋을 쌓아도·09:05 이 돌아도 알림이 없고 **잡은 성공으로 끝난다**(WORK-017 결함 ④와 같은 종류). GitHub 계정·조직 레포 목록 → 레지스트리 diff → 화면 배너, fork·아카이브·타인 레포는 거른다(소음이 되면 아무도 안 본다). **자동 등록하지 않는다** — 막지 않고 알린다(D7 원칙, `missing_career()` 형태). 스케줄 잡으로 만들지 않는다 — 배너는 볼 사람이 화면에 있을 때만 의미가 있다.
- 2026-08-03 **KDEV-DEC-017 작성 (proposed)** — 제품 레지스트리 조인 + 관리자 제품 등록. BL-005 P1 을 결정으로 내렸다. D1 조인은 **`tracked_repos.product_slug` 컬럼 하나**(`project_detail` 테이블·showcase 필드·경로 저장 전부 기각 — 본문이 파일에 남으면 DB 가 담을 것이 조인뿐) · D2 **`kknaks-profile` → `kknaks-dev` 통합**(D5 가 showcase 를 제품 폴더 안에서 만드니 두 폴더가 영구 예외가 된다. 경로 참조 0건 확인) · D3 **스캐폴드 6 파일** — 템플릿 통째 복사는 **부팅을 막는다**(샘플 문서 8개가 `type` 을 갖고 있어 `products/` 아래 들어가면 그래프 노드가 되고, 제품 둘이면 stem `baseline` 중복 → L2 ERROR → WORK-007 enforce 가 raise) · D4 **LLM 미사용**(전 단계가 복사·치환·검증, 백그라운드는 클론 하나. `category` 는 `_meta.yaml` 7종 드롭다운 — 벗어난 값 하나가 persona 로드 전체를 실패시켜 사이트가 옛 데이터를 서빙한다) · D5 `templates/product/showcase.md` 신설이 형식 SoT · D6 `P-NN` 코드 채번(max+1, 결번 재사용 안 함) · D7 **DB CHECK 로 파일 존재를 강제하지 않는다**(`daily.py:151` 근거) — 쓰기 전 검증 + 화면 표시 · D8 커밋 1개 + push 실패 시 롤백(`commit_and_push_with_retry` 는 롤백이 없다) · D9 **company 는 파일을 만들지 않는다** → 회사 5개 디렉토리 삭제(`showcase.md` 하나뿐·전부 `visible:false`, 모집단 13→8 이나 화면 변화 없음) · D10 CRU(D = `enabled=false`) · D11 슬롯은 「프로젝트」. **파일 쓰기가 발행부 독점이 아니라는 점을 확인**했다 — `ALLOWED_PREFIXES` 는 게이트 경로만 검사하고 잡 셋이 이미 직접 쓴다. **OQ 5건을 같은 날 전부 해소** — D12 레포 4개 전부 편입(로컬 클론 `origin` 실측: 넷 다 원격 실재, README `TBD` 가 낡았다. **한 달 57건이 잔디에서 빠지고 있었다** — `ax-graph` 48건) · D13 showcase 형식은 **하나**(케이스 스터디 필드 보유 8 = studio 8, 스텁 5 = company 5 → D9 이 company 를 없애 저절로 단일화) · D14 `visible` 파일 유지 · D15 `products/README.md` 는 스캐폴드가 행 추가 · D16 showcase 노드 승격 기각.
- 2026-08-03 **KDEV-BL-005 작성 (raw)** — 제품·프로젝트·커리어 연동 + 레지스트리 관리 화면. 원 발주(파일 데이터 DB화 검토)의 답으로 **판정표 8건**을 실었고, 대화 중 설계가 두 번 뒤집혔다: ① showcase 본문 DB화 폐기(로컬 md 작업 유지) → **DB 가 가질 것은 조인뿐** ② 낡음의 해법이 "관리 화면 편집" 이 아니라 **"잔디 잡 확장"**(career 는 이미 자동 갱신되는데 product 만 경로가 없다). 실측 — 제품 18 vs showcase 13, **파이프라인만 있는 5개가 사이트에 뜰 방법이 없다**(최근 작업 전부가 거기 있다), showcase 13개 **34일째 무수정**(전부 WORK-004 마이그레이션 커밋), `org=company` 5개는 전부 `visible:false`+`(TBD)`, `kknaks-dev`/`kknaks-profile` 이 **같은 제품인데 두 폴더**, 조인 키가 폴더명뿐. 판단 축 둘 무력화 — 부팅 641 md 중 **428이 `products/**`**(persona DB화로 31%만 준다), 봇 identity 가 개인 계정이라 **DB화가 잔디 커밋을 줄인다**. P1 = `product_slug` 컬럼 + 레지스트리 CRU + **깃 연동**(등록 오타가 다음 날 09:05 까지 숨는다 — `sync_repo` 호출부가 `collect_git.py:92` 하나뿐), P2 = 잔디 산출물에 product 추가. 미결 8건.
- 2026-07-31 **KDEV-WORK-017 발주 (todo)** — 잔디 커밋 파이프라인 5 phase. P1 레지스트리+bare 클론+collect(마이그레이션·compose 볼륨·서버 최초 클론 321MB — 가장 무겁고 배포 필요) · P2 형식 SoT 템플릿(P1과 병렬) · P3 `daily_commit` 파이프라인+chain 일반화 · P4 apply 확장 6종(P3과 병렬) · P5 화면+실운영 완주. WORK-016 의 제출/수확 분리 위에 정의만 얹는다 — 게이트·큐·API·admin FE 무변경.
- 2026-07-31 **KDEV-SPEC-011·012·013 신규 (draft) + SPEC-001·003·008·010 개정** — 011 커밋 조사(레지스트리·bare 클론·수집 규칙·drift 알림) · 012 산출물 계약(daily·career·concept, career 갱신 규율·형식 SoT) · 013 잔디 게이트(`daily_commit` 정의·fan-out 배치·발행 검증 확장). 개정: SPEC-001 에 daily·career 자동갱신 주체 + 자동갱신 경로표, SPEC-003 에 커밋 유입 경로, SPEC-008 에 잔디 정의·route 없는 체인·fan-out 규칙(공통코어 가정 정정), SPEC-010 에 `upsert`·그래프 밖 산출물·본인작성 보호·사람 전용 필드.
- 2026-07-31 **DEC-014 OQ 실측 해소** — `mediness` bare 129M → 13개 합 ~321MB(bare full 확정). **identity 3종 발견 — `kknaks@medisolveai.com` 만 걸었으면 `kknaks_profile` 커밋 절반 유실**, D5 를 `--author=kknaks` 단일 패턴 + drift 감지로 개정. `--all` 추가분 +17.3%(본인 +7.9%) · tree-hash 중복 163건으로 D3·D6 근거 확보. 미결 13→3, 전부 spec 무관.
- 2026-07-31 **KDEV-DEC-014·015·016 작성 (proposed)** — BL-004 미결 10건 전부 해소. 014 레지스트리 DB화 + bare full clone(`--all --numstat`, email 다중 author, tree-hash dedupe, diff 상한 32KB/8KB/30건, 회사 레포도 diff 전부 포함) · 015 목적지 3개 + `templates/persona/daily.md`·`career.md` 신규 + `## 담당 영역` 신설 + daily body 500→1200자 · 016 `daily_commit` 파이프라인 + fan-out 을 게이트 밖 auto 로 + `chain.enabled_stages` 일반화 + `apply/` 확장 6종(`upsert` 액션·graph_check 제외·`auto:false` 검증) + `publish_atomic` 전환. DEC-011 보류(커밋 파이프라인 정의) 해소.
- 2026-07-30 **KDEV-BL-004 작성 (raw)** — 커밋 잔디 파이프라인. 잔디 잡이 BL-003 auto-commit 경로 4개 중 유일하게 게이트 미적용. 커밋 입력이 `{repo, msg}` 뿐(diff·stat·브랜치 없음)이라 서술 품질 병목이 형식이 아니라 입력, 로컬 bare 클론 + `--numstat` 으로 전환. daily body 는 미노출·career body 는 렌더된다는 비대칭이 목적지를 갈랐다 — daily·career·concept 3개, `persona/areas/` 와 work·showcase 는 폐기. 미결 10건.
- 2026-07-28 **WORK-013 done** — concept 층 도입. 4층 재편(`layer` 도출·rank 반전·층별 orphan), `permanent/concept/` 실재화, `rules/knowledge-note-pipeline.md` + `templates/knowledge/`, enforce 전환. 신규 규칙 위반 1건뿐이었고 lineage 1→4건. 344 passed.
- 2026-07-27 **WORK-012 done** — Slack bridge를 back lifespan으로 흡수. sink DI 리팩터(WORK-014 교체 지점), 컨테이너 5→4개, deploy.yml의 죽은 profile 참조 제거. 309 passed. 운영 e2e는 배포 대기.
- 2026-07-27 DEC-010~013 accepted 승격 + WORK-012~015 발주 (bridge 흡수 · concept 층 · 큐+route · 유튜브 완주). 012·013 병렬 → 014 → 015.
- 2026-07-27 40-architecture 작성 (database·system·deploy) — SoT 경계 · ERD 9테이블 · 쓰기 소유권 경계 · 배포 환경. 종전 전부 빈 템플릿이었음.
- 2026-07-27 KDEV-SPEC-003 개정 v0.0.2 + DEC-005 개정 노트 — 4층 생명주기, 정제 주체를 AI 초안 + 사람 승인으로 전환(DEC-005의 기각 근거는 승인 게이트가 흡수), `inbox/`는 대기열이 아니라 목적지.
- 2026-07-27 KDEV-SPEC-007~010 신규 (draft) — 승인 큐 · 게이트 체인 · 피드백/재생성 · Apply Executor.
- 2026-07-27 KDEV-SPEC-005 개정 v0.0.3 + DEC-007 superseded — force-graph 폐기 → 트리 문서 렌더러, 연결 패널(상류/인용/백링크), 공개 프론트는 게시분만.
- 2026-07-27 KDEV-SPEC-004 개정 v0.0.5 — L5 층별 재정의(source orphan=미소화 큐), L2 type별 필수 필드, L4 방향 반전, 발행 전 검증 지점 신설.
- 2026-07-27 KDEV-SPEC-002 개정 v0.0.3 — `layer` 도출(frontmatter 미기재), type enum 재편(`note` 제거·`concept` 추가), rank 방향 반전, concept `aliases`/`up:` 필수. 미해소 OPEN 2건(products 노드 포함·lineage 0건) 해소.
- 2026-07-27 KDEV-SPEC-001 개정 v0.0.4 — 4층 매핑 + `permanent/concept/` 신설, concept 규약(aliases·up: 필수·SoT 위임·개념 성장), 층간 참조 방향.
- 2026-07-27 KDEV-DEC-013 작성 (proposed) — Slack bridge를 back lifespan으로 흡수. 쓰기 소유권 back 단독, `app/slack_bridge/` 제거, OKK-SPEC-011 §4 개정.
- 2026-07-27 KDEV-DEC-012 작성 (proposed) — 저장·발행 경계. draft=DB/확정=md, AI는 발행 계획만·Executor가 실행, 승인 1회=커밋 1개(원자적), 수정은 전문교체+diff, 실패 시 전량 롤백.
- 2026-07-27 KDEV-DEC-011 작성 (proposed) — 승인 게이트 체인. DB 큐 / `inbox/` 보류함 분리, 파이프라인 정의가 데이터(공통코어+파생슬롯), 유튜브 체인 확정, 역방향은 route 재오픈 하나, 마지막 게이트 승인이 발행 트리거.
- 2026-07-27 KDEV-DEC-010 작성 (proposed) — 지식 그래프 4층 재설계(source/concept/synthesis/execution). `permanent/concept/` 신설, `up:` 생성 의무화, 층별 orphan 재정의, force-graph 폐기→트리 렌더러.
- 2026-07-27 KDEV-BL-003 작성 — inbox 승인 게이트 파이프라인 + 원자 개념(concept) 층. auto-commit 4경로 진단, ax 패턴 각색 방향 후보 정리.
- 2026-07-27 WORK-011 done — 관리자 인증 MVP 구현+e2e(Postgres·Alembic·async SQLAlchemy·쿠키 JWT·톱니→admin 목). DEC-009 v2로 DB 접근 async 전환.
- 2026-07-27 KDEV-BL-002 + DEC-009 + SPEC-006 작성 — 애플리케이션 DB화 시작(첫 테이블 users) + 관리자 인증(쿠키 JWT, .env 시드). 지식그래프는 md SoT 유지 공존.
- 2026-06-29 30-work WORK-001~009 정의 (적용 9단계, enforcement는 007 맨끝). SPEC-003 정제흐름 보강.
- 2026-06-29 KDEV-SPEC-001~005 작성 (디렉토리·스키마·워크플로·검증·시각화). medi_docs 폐기(73파일).
- 2026-06-29 KDEV-DEC-001~007 작성 (단일루트·파이프라인·노드/식별자·엣지·워크플로·검증·시각화).
- 2026-06-29 KDEV-BL-001 (레포 지식그래프化) baseline 작성. 설계 SSOT: PLAN-003.
