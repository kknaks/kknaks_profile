# Work Index

규칙: `rules/product-doc-pipeline.md`

> 적용 순서 핵심: enforcement(L1~L4 ERROR + 부팅 fail-fast)는 **WORK-007 맨 마지막**에 켠다. 그 전엔 검증기를 report-only로 둬야 라이브 서버가 안 죽는다.

> 마이그레이션 정합: 신규 층(reference/permanent/posts)은 현재 블로그 라우트·loader 키가 **없다** (라우트=about·algorithms·career·contents·notes·projects·print, loader 키=career·projects·notes·contents·daily·algorithms). 마이그레이션 work는 **파일 이동 + 라우트 신설/재배선 + loader 키 추가**를 atomic으로 포함한다 (이동만으로는 블로그에 안 보임).

## 의존 흐름

```
001 빌더+검증기(report) → 002 검증기 정교화(report-only) → 003 지식층 scaffold+규약
  → ┬ 004 projects→products ┐
    ├ 005 notes→reference    ┼→ 007 enforcement ON ✅ → 008 /graph ✅ → 009 로컬그래프 ✅
    └ 006 contents 잔류 확정 ┘  (006=문서정정, 마이그레이션 아님 → 007은 004·005만 의존)
                                  (001~009 done — PLAN-003 그래프 시각화 단계 완료)
  005 reference 배선 ─(미러)→ 010 permanent 층 배선 ✅ (BE-only, lineage 발현 준비 — live permanent 0건이라 아직 latent)
```

승인 파이프라인 트랙 (BL-003):

```
012 bridge 흡수 ─┐
                 ├→ 014 큐 + route 게이트 → 015 유튜브 체인 + Executor
013 concept 층 ─┘
   (012·013 서로 독립 — 병렬 가능하나 **순차 권장**: 012가 프로세스를 하나로 모은 뒤 013 검증을 돌려야 원인 추적이 단순하다)
```

잔디 트랙 (BL-004):

```
016 비동기 실행 ✅ ─→ 017 잔디 커밋 파이프라인
                        P1 형식 SoT (템플릿·agent) ✅
                          → P2 파이프라인 레일 + 더미 collect ─┬→ P4 화면 + 더미 한 바퀴 완주
                             P3 발행부 확장 ───────────────────┘      → P5 진짜 git + 외부연동 + 실운영
                                                     (P2·P3 병렬)
```

- **017**은 016이 세운 제출/수확 분리와 드라이버 **위에 정의만 얹는다.** 게이트·큐·API·admin FE 는 손대지 않는다 — 손대는 곳은 준비부(`prepare`·`flow`·`driver` — auto 스테이지를 여럿 돌리는 레일)와 `apply/`(경로 2개·`upsert`·그래프 밖 산출물·본인작성 보호).
- **Phase 순서를 walking skeleton 으로 뒤집었다.** 제일 무거운 것(bare 클론 321MB·볼륨·토큰·배포)을 앞에 두면 파이프라인이 한 번도 안 돌아 본 채로 인프라 작업을 하게 된다. **깃은 더미로 가져오고 한 바퀴를 먼저 완주**시킨 뒤, 진짜 수집을 마지막에 `collect` 한 곳에서 갈아 끼운다.
- **P5가 가장 무겁고 유일하게 배포가 필요하다** — 마이그레이션 + compose 볼륨 + 서버 최초 클론(~321MB) + 구 잔디 경로 제거가 전부 여기다. **P1~P4 내내 구 잔디 잡이 그대로 돈다.**
- **구 경로 제거는 스케줄러 교체와 같은 커밋이다.** `inputs.py` 의 커밋 조회 함수 둘은 유일한 소비자가 `main_job.py` 인데, `lifespan` 의 `service.scheduler` 임포트만 실패를 삼키는 자리가 없어 먼저 지우면 백엔드 전체가 부팅되지 않는다.
- **012**는 쓰기 소유권을 back으로 모으고 sink 교체 지점을 만든다. 014가 그 sink를 "큐 적재"로 갈아끼운다.
- **013**은 목적지(`permanent/concept/`)를 실재화한다. 목적지가 없으면 route 게이트가 고를 게 없다.
- ~~**013 Phase 1은 report-only 측정**이다.~~ **완료** — 신규 규칙 위반이 **1건**뿐이라 Phase 2(데이터 정리)가 Phase 3와 합쳐졌고, enforce 전환까지 끝났다. lineage 1건 → 4건.
- **014까지만 하면 큐에 쌓이고 발행은 안 된다.** md가 나오려면 015까지 가야 한다.

## Work 목록

| ID | Title | 담당 | Status | Covers Spec | Depends | File |
|---|---|---|---|---|---|---|
| WORK-001 | 그래프 빌더 수술 + 검증기(report-only) | BE | done | SPEC-002·004 | — | `work-001-graph-builder-validator.md` |
| WORK-002 | 검증기 정교화 (code-fence 스킵·navigational 제외·orphan 범위, report-only) | BE | done | SPEC-002·004 | 001 | `work-002-validator-refinement.md` |
| WORK-003 | 지식층 scaffold + 작성 규약(분류·정제·up·archive + agent.md) | BE/문서 | done | SPEC-001·003 | 002 | `work-003-knowledge-layer-scaffold.md` |
| WORK-004 | projects → products/showcase 재편 (+`/projects` 라우트가 `products/*/showcase.md`를 읽도록 재배선 + loader가 products showcase 노출 + inputs.py) | BE+FE | done | SPEC-001 | 003 | `work-004-migrate-projects.md` |
| WORK-005 | notes → reference 재편 (+ reference 라우트·loader 키 신설/재정의 — `/notes` 유지 vs `/reference` 네이밍은 발주 직전 admin 결정) | BE+FE | done | SPEC-001 | 003 | `work-005-migrate-notes.md` |
| WORK-006 | contents 잔류 확정(마이그레이션 철회)+문서정정 (DEC-008 신설·DEC-002 amend·SPEC-001 정정, 코드 0, /posts 배선 연기) | 문서 | done | SPEC-001 | 003 | `work-006-migrate-contents.md` |
| WORK-007 | enforcement ON (L1~L4 ERROR fail-fast + pre-commit + kill-switch GRAPH_ENFORCE) — 단일 지점 load_persona, boot propagate/reload catch, 메커니즘 4종 실증 | BE | done | SPEC-004 | 004·005 | `work-007-enforce-validation.md` |
| WORK-008 | 전역 그래프 /graph (_graph.json API + force-directed) | BE+FE | done | SPEC-005 | 007 | `work-008-global-graph.md` |
| WORK-009 | 노트별 로컬 그래프 (이웃+백링크) | FE | done | SPEC-005 | 008 | `work-009-local-graph.md` |
| WORK-010 | permanent 층 그래프 배선 — 영구노트를 _graph 에 연결 (BE-only, WORK-005 미러) | BE | done | SPEC-001·003 | 005 | `work-010-wire-permanent.md` |
| WORK-011 | 관리자 인증 MVP — DB 토대(Postgres·async SQLAlchemy·Alembic) + 쿠키 JWT 로그인 + admin 목 | BE+FE | done | SPEC-006 | — | `work-011-admin-auth-mvp.md` |
| WORK-012 | Slack bridge를 back에 흡수 + 쓰기 소유권 정리 (sink DI 리팩터·lifespan 흡수·compose 정리·OKK-SPEC-011 §4 개정) | BE | **done** | SPEC-007(선행분) | — | `work-012-slack-bridge-absorb.md` |
| WORK-013 | concept 층 도입 — 4층 재편·검증 재정의·규칙/템플릿 (report-only 선행 → enforce) | BE+문서 | **done** | SPEC-001·002·003·004 | — | `work-013-concept-layer.md` |
| WORK-014 | 승인 큐 + route 게이트 MVP (스키마·접수·자동준비·게이트 공통계약·admin 큐 화면) | BE+FE | done | SPEC-007·008(route)·009 | 012·013 | `work-014-queue-and-route-gate.md` |
| WORK-016 | 비동기 실행 + 진행 표시 UI (제출/수확 분리·완료 대기·진행 표시) | BE+FE | done | SPEC-008·009 | 015 | `work-016-async-execution-and-progress-ui.md` |
| WORK-015 | 유튜브 체인 완성 + Apply Executor (source_note·concept·derived + 원자적 발행) | BE+FE | doing 80% (BE·FE 전부 done, 실전 e2e 만 남음) | SPEC-008·010·004 | 014 | `work-015-youtube-chain-and-executor.md` |
| WORK-017 | 잔디 커밋 파이프라인 — 형식 SoT·준비부 일반화·더미 collect·발행부·화면·진짜 git 수집 (5 phase) | BE+FE+Ops | in_progress 25% (P1 done · P2 진행 중) | SPEC-011·012·013·010 | 016 | `work-017-grass-commit-pipeline.md` |

## Status Board

| Track | 진행 | Next |
|---|---|---|
| 지식그래프 (BL-001) | WORK-001~010 done | — |
| 앱 DB화 (BL-002) | WORK-011 done | admin 실제 관리 기능 |
| 승인 파이프라인 (BL-003) | **012·013 done** · 014~015 todo | **014 착수** (큐 + route 게이트) → 015 |
| 잔디 파이프라인 (BL-004) | **017 in_progress 25%** — P1 형식 SoT done · P2 레일 진행 중 | P2 잔여 — auto 루프·이름별 등록·수집 전제 해제·fan-out 저장·더미 collect·`investigate`·`compose`·합성 키 |

## Spec Coverage

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 디렉토리 | WORK-003·004·005·006·010·**013** | 003~010 done / **013 — 4층 매핑 + `permanent/concept/` 실재화 done** |
| SPEC-002 스키마 | WORK-001·002·**013** | 001·002 done / **013 — `layer` 도출·type enum 재편·rank 반전 done** |
| SPEC-003 워크플로 | WORK-003·010·**013** (+강제: 001·007) | 003·007·010 done / **013 — 4층 생명주기 규칙 문서화(`rules/knowledge-note-pipeline.md`) done** |
| SPEC-004 검증 | WORK-001·002·007·**013**·015 | 001·002·007 done / **013 — 층별 orphan·L2 필수필드·L4 반전 enforce done** / 015 발행 전 검증 todo |
| SPEC-005 시각화 | WORK-008·009 | 008 전역 done / 009 로컬 done (시각화 완료) |
| SPEC-006 관리자 인증 | WORK-011 | 011 done (DB 토대+async+로그인+admin 목 e2e 검증 — 앱 DB화 첫 트랙, 그래프 work와 독립) |
| SPEC-007 승인 큐 | WORK-012·014 | **둘 다 done** — 접수·준비·재시도·삭제·큐 화면까지 구현. 발행 재시도만 WORK-015 |
| SPEC-008 게이트 체인 | WORK-014·015·**017** | 014 route BE done / 015 나머지 스테이지 todo / **017 P2 — `daily_commit` 정의 등록 done, 준비부 일반화 진행 중.** route 없는 체인(`enabled_stages` 일반화)은 **범위 밖으로 뺐다** — 게이트 1개인 잔디에는 필요가 없고 판정 기준도 payload 유무가 아니라 정의의 route 유무여야 한다 (017 Open Issue) |
| SPEC-009 게이트 피드백 | WORK-014 | 014 P3 에서 공통 계약 구현 done |
| SPEC-010 Apply Executor | WORK-015·**017** | 015 구현 done (검증 6종·원자 커밋·전량 롤백·재시도) / **017 P3 — `upsert`·그래프 밖 산출물·본인작성 보호 todo** |
| SPEC-011 커밋 조사 | WORK-**017** | **P2 더미가 §4 계약 전량을 먼저 낸다**(교체 비용을 `collect` 한 곳에 가둔다) / P5 todo — 레지스트리·bare 클론·로컬 git 수집 |
| SPEC-012 잔디 산출물 | WORK-**017** | **P1 템플릿 SoT done**(`templates/persona/daily.md`·`career.md` + `agent.md` 등록) / P2 todo — daily·career·concept 초안(`compose`) |
| SPEC-013 잔디 게이트 | WORK-**017** | **P2 정의 등록 done, 스테이지 todo** / P3 발행 todo / P4 화면 + 더미 한 바퀴 완주 todo / P5 실발행 todo |

> SPEC-001·002·003·004는 DEC-010 반영으로 **개정**됐다(4층·concept·층별 검증). WORK-013이 그 개정분을 코드에 반영한다 — 기존 WORK-001~010이 구현한 것과 별개 커버리지다.
