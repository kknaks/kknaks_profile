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

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |

## 최근 로그

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
