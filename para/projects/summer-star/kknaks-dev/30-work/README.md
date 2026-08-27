# Work Index

규칙: `para/projects/project.md`

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
                          → P2 파이프라인 레일 + 더미 collect ✅ ─┬→ P4 화면 + 더미 한 바퀴 완주
                             P3 발행부 확장 ✅ ───────────────────┘      → P5 진짜 git + 외부연동 + 실운영
                                                     (코드 Phase 셋 닫힘 — 남은 것은 화면과 배포)
```

지식층 재편 트랙 (BL-006):

```
013 concept 층 ✅ ─→ 019 디렉토리 이관
                      P1 이동 + 코드 (atomic) ✅ ← 위험 전부가 여기 있었다
                        → P2 문서 정합 ✅ → P3 「양식 원천」 ✅ → P4 배포·부팅 ✅
```

- **P1 이 원자적인 이유가 둘이다.** 파일과 코드가 다른 커밋에 들어가면 그 사이에서 로더가 없는 경로를 보고 **부팅이 막히고**(DEC-018 D9), 되돌릴 때도 한 커밋이라야 원상태가 된다. WORK-004 가 `projects → products/showcase` 를 같은 이유로 atomic 하게 했다.
- **문서를 코드보다 뒤에 둔다** — 반대면 문서가 아직 없는 경로를 가리키는 구간이 생긴다.
- **마이그레이션 0건이다.** 지식층은 파일 SoT 라 DB 를 안 건드린다.

제품 레지스트리 트랙 (BL-005):

```
017 잔디 파이프라인 ✅ ─→ 018 제품 레지스트리
                            P1 형식 SoT + 제품 트리 정리 (코드 0)
                              → P2 컬럼 + repository 계층 신설
                                → P3 service + API (스캐폴드·검증·발견)
                                  → P4 화면 → P5 배포 + 실운영 관측
```

- **018 은 017 의 `tracked_repos`·`sync_repo`·시드 스크립트 위에 컬럼 하나와 관리 표면을 얹는다.** 잔디 파이프라인 코드는 손대지 않는다.
- **P1 이 코드 0줄인데 맨 앞이다.** 스캐폴드가 읽을 카드 양식이 없으면 P3 가 형식을 지어내 SoT 가 둘이 되고(017 P1 과 같은 이유), 시드 매핑은 `kknaks-profile` 통합 **뒤의** 제품 목록을 기준으로 해야 한다.
- **P2 가 `repository/` 계층의 첫 입주자다.** 레거시 일괄 리팩터는 하지 않는다 — 규약과 경계는 `40-architecture/system/README.md`.
- **완료 판정이 화면이 아니라 잔디다.** P5 에서 신규 레포 커밋이 그날 `counts` 에 잡혀야 이 발주가 푼 문제(한 달 57건 누락)가 닫힌다.

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
| WORK-017 | 잔디 커밋 파이프라인 — 형식 SoT·준비부 일반화·더미 collect·발행부·화면·진짜 git 수집 (5 phase) | BE+FE+Ops | **done (2026-08-03)** — 서버 하루치 실 push 완주(`a8c44b4`). 로컬 e2e 가 결함 10건을 꺼내 9건 수정, 818 passed | SPEC-011·012·013·010 | 016 | `work-017-grass-commit-pipeline.md` |
| WORK-019 | 지식층 디렉토리 이관 — `resources/{source,concept,synthesis}/` · `archive/` 최상위 · 「양식 원천」 명칭 전환 (4 phase) | BE+문서+Ops | **done (2026-08-03)** — 이동 전후 그래프 동일(`nodes 287·ERROR 0`), 서버 실측도 같다. 잠복 버그 1건 발견·수정. 887 passed | SPEC-001·005 | 013 | `work-019-resources-layout-migration.md` |
| WORK-018 | 제품 레지스트리 — 형식 SoT+트리 정리 · `product_slug` 컬럼 + **`repository/` 계층 신설** · 결정적 스캐폴딩 · 미등록 발견 · 관리 화면 (5 phase) | BE+FE+Ops | **done (2026-08-03)** — 배포·시드 17행·클론 295MB 완주. 로컬 e2e 가 결함 4건을 꺼냈고 **서버에서 "한 달 57건 누락" 이 재현됐다**. 887 passed | SPEC-014·011·001 | 017 | `work-018-product-registry-admin.md` |
| WORK-020 | 개념 후보 좁히기 — alias seed + 그래프 1홉 (`concept`·`daily` 게이트 입력에서 전량 투입 제거, 5 phase) | BE | **done (2026-08-12)** — payload 70,554 → 11,359자(84% 감소), 회수율 87%. 문서 행이 `todo` 로 남아 있던 것을 2026-08-13 에 바로잡았다 | SPEC-008 | — | `work-020-concept-candidate-retrieval.md` |
| WORK-021 | 노트 출력 계약에서 JSON 을 뺀다 — 구분자 레코드 (`source_note`·`concept`·`derived`·`post`, 6 phase) | BE | **in_progress 90%** — P1~P4·P6 done. **실전(#3881)에서 다섯 스테이지 전부 1차 통과·재시도 0** — 이 발주가 풀려던 문제는 닫혔다. 발행은 다른 사유(`type` 누락·dead link)로 거부됐고 하나는 P6 로 닫았다(OQ-3) | SPEC-008 | — | `work-021-note-output-delimiter.md` |
| WORK-022 | 스테이지 사이 세션 이어받기 — 앞 게이트 승계 · `cancelled` 제외 · 실패 세션 보존 · 원문 재전송 제거 · **죽은 세션 복구** (6 phase) | BE | **in_progress 85%** — P1~P4·P6 done. 실전(#3881)에서 게이트 넷이 한 세션임을 확인했고, **배포가 세션을 죽여 항목이 멎는 구멍**을 P6 로 닫았다. P5 재측정만 남았다 | SPEC-009 | — | `work-022-stage-session-inheritance.md` |

## Status Board

| Track | 진행 | Next |
|---|---|---|
| 지식그래프 (BL-001) | WORK-001~010 done | — |
| 앱 DB화 (BL-002) | WORK-011 done | admin 실제 관리 기능 → **WORK-018 이 첫 사례** |
| 제품 레지스트리 (BL-005) | **018 done (2026-08-03)** — P1~P5 완주. `repository/` 계층 신설이 규약의 첫 적용 | 관측 3건(시드 자동화·서버 실 등록·잔디)만 Open Issue |
| PARA 정렬 (BL-006) | **019 done (2026-08-03)** — `resources/` 이관 완주. P·R·Archive 가 폴더로 섰다 | 후속 — `persona/` A 판정 (DEC-018 OQ-1) |
| 승인 파이프라인 (BL-003) | **012·013 done** · 014~015 todo | **014 착수** (큐 + route 게이트) → 015 |
| 잔디 파이프라인 (BL-004) | **017 in_progress 50%** — P1 형식 SoT done · **P2 done**(레일·더미 `collect`·`investigate`·`daily` 게이트 작성·실배선 + 접수 진입점 `daily:{date}` 합성 키·백필·`auto:false`/미래 날짜 차단) · **P3 done**(발행 허용 2경로·`upsert`·그래프 검증 제외·보호 검증 둘, `publish_atomic` 은 자동 달성). **737 passed** | P4 — 게이트 화면 + 더미 한 바퀴 완주(dry-run). 착수 전 Open Issue 「활동 0 차단 위치」 결정. ⚠ **이 갱신 직후 `8c2aa7a`(P4 승인 화면)가 들어왔다 — 아직 문서에 미반영** |

## Spec Coverage

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 디렉토리 (v0.0.6) · SPEC-005 (v0.0.4) | WORK-**019** | **done (2026-08-03)** — 레이아웃이 실제와 일치한다. 이동 전후 그래프 동일, 서버 배포 후 실측도 같다(`nodes 287 · ERROR 0 · WARN 0`) |
| SPEC-014 제품 레지스트리 | WORK-**018** | **done (2026-08-03)** — 수용조건 14 중 11 검증, 3은 관측 대기(Open Issue). 원 계획: P1 형식 SoT(`templates/product/showcase.md`) + 제품 트리 정리(`kknaks-profile`→`kknaks-dev` 통합·회사 5개 삭제·README 정정) / P2 `product_slug` 컬럼 + **`repository/` 계층 신설**(계층 규약 첫 적용) + 17행 시드 / P3 service+API(스캐폴드 화이트리스트·사전 검증 7종·커밋 1개+롤백·미등록 발견) / P4 화면 / P5 배포+실운영. **관측 대상이 화면이 아니라 잔디다** — 신규 레포 커밋이 그날 `counts` 에 잡혀야 "한 달 57건 누락" 이 닫힌다 |
| SPEC-001 디렉토리 | WORK-003·004·005·006·010·**013** | 003~010 done / **013 — 4층 매핑 + `permanent/concept/` 실재화 done** |
| SPEC-002 스키마 | WORK-001·002·**013** | 001·002 done / **013 — `layer` 도출·type enum 재편·rank 반전 done** |
| SPEC-003 워크플로 | WORK-003·010·**013** (+강제: 001·007) | 003·007·010 done / **013 — 4층 생명주기 규칙 문서화(`rules/knowledge-note-pipeline.md`) done** |
| SPEC-004 검증 | WORK-001·002·007·**013**·015 | 001·002·007 done / **013 — 층별 orphan·L2 필수필드·L4 반전 enforce done** / 015 발행 전 검증 todo |
| SPEC-005 시각화 | WORK-008·009 | 008 전역 done / 009 로컬 done (시각화 완료) |
| SPEC-006 관리자 인증 | WORK-011 | 011 done (DB 토대+async+로그인+admin 목 e2e 검증 — 앱 DB화 첫 트랙, 그래프 work와 독립) |
| SPEC-007 승인 큐 | WORK-012·014 | **둘 다 done** — 접수·준비·재시도·삭제·큐 화면까지 구현. 발행 재시도만 WORK-015 |
| SPEC-008 게이트 체인 | WORK-014·015·**017**·020·**021** | **021 todo — 노트 출력 형식**(v0.0.7 개정: 구분자 레코드. markdown 전문을 JSON 문자열 값에 넣지 않는다) / 020 done — concept 게이트 입력 좁히기 / 014 route BE done / 015 나머지 스테이지 todo / **017 P2 — `daily_commit` 정의 등록 + 준비부 일반화 done**(auto 스테이지 N개를 정의 순서로 돌려 `daily` 게이트까지). route 없는 체인(`enabled_stages` 일반화)은 **범위 밖으로 뺐다** — 게이트 1개인 잔디에는 필요가 없고 판정 기준도 payload 유무가 아니라 정의의 route 유무여야 한다 (017 Open Issue). ✅ `daily_commit` 정의 표가 **SPEC-008 v0.0.3** 에서 `compose` auto 를 걷고 `daily` 게이트로 정정됐다 — 두 spec 의 모순 해소 |
| SPEC-009 게이트 피드백 | WORK-014·**022** | 014 P3 에서 공통 계약 구현 done / **022 P1~P4·P6 done**(v0.0.4: 앞 게이트 승계 S-6 · `cancelled` 제외 S-7 · 형식 실패 세션 보존 S-8 · 원문 재전송 제거 · **죽은 세션 자동 복구 S-9**). P5 재측정만 남았다 |
| SPEC-010 Apply Executor | WORK-015·**017** | 015 구현 done (검증 6종·원자 커밋·전량 롤백·재시도) / **017 P3 done — 개정분 전량 반영**: `upsert`(존재·stale 검사 둘 다 면제 — daily 는 첫 회 생성과 덮어쓰기가 둘 다 정상이라 존재 여부가 판단 근거가 못 된다) · 그래프 밖 산출물(`OUTSIDE_GRAPH` — `up:` 이 없는 문서를 얹으면 고아 규칙에 걸리므로 **빼는 것이 사실의 반영**) · 본인작성 보호(`USER_AUTHORED_DAILY` 접수·발행 이중) · `PROTECTED_FIELD`. `publish_atomic` 전환은 **별도 작업 없이 자동 달성**(`apply_item` 이 파이프라인을 가리지 않는다) |
| SPEC-011 커밋 조사 | WORK-**017** | **P2 더미 `collect` done — §4 계약 7키 전량 + 시나리오 7종**(교체 비용을 `collect` 한 곳에 가둔다. 지어내는 것은 `commits[]` 뿐이고 영역 분해·`counts`·career 귀속은 진짜 코드) / P5 todo — 레지스트리·bare 클론·로컬 git 수집 |
| SPEC-012 잔디 산출물 | WORK-**017** | **P1 템플릿 SoT done**(`templates/persona/daily.md`·`career.md` + `agent.md` 등록) / **P2 `daily` 게이트 작성 done — 그 SoT 를 코드가 실제로 싣는다**(프롬프트 복사 아님을 마커 테스트가 검증, `counts` 는 코드 주입, career 는 전문 교체). 싣는 주체가 `compose`(auto)에서 게이트로 바뀌었을 뿐 **형식 계약 자체는 무변경** / **P3 발행 done** — frontmatter 는 **시스템이 조립한다**(daily 의 `type`·`date`·`auto`·`counts` 는 AI 것이 아니고, career 는 기존 frontmatter 를 그대로 이고 본문만 바꿔 **사람 전용 필드를 건드릴 방법 자체를 없앤다** — 검증 전에 구조로 막는다). 「형식 SoT」 표의 **읽는 쪽**을 `daily` 게이트로 갱신(2026-08-01, 계약 아닌 소비자 이름표라 version 유지). ⚠ **잔디 concept 만 형식 SoT 를 읽지 않는다** — `stages/daily.py` 가 `templates/knowledge/concept.md` 를 싣지 않는다(유튜브 `concept` 게이트는 읽는다). 017 Open Issue |
| SPEC-013 잔디 게이트 | WORK-**017** | **v0.0.2 개정 — 작성 주체를 게이트로 모았다**(`compose` auto 제거, 근거는 재생성 S-3). **P2 done** — auto 둘 + `daily` 게이트 작성 + 실배선 + 접수 진입점(`daily:{date}` 합성 키로 **기존 중복 판정을 날짜 축에서 그대로 돌린다** — 컬럼·인덱스 무증설, `uq_queue_items_pending_url` 이 마이그레이션 없이 하루 한 항목을 강제, 재접수는 S-7 3항대로 `duplicate_published`) · 백필 · `auto:false`·미래 날짜 접수 전 차단 / **P3 발행 done** / P4 화면 + 더미 한 바퀴 완주 todo / P5 실발행 todo. ✅ 부분 실패 **결과 귀속**이 §4 Data Contract 로 들어가 017 Open Issue 해소. ⚠ **활동 0 차단이 스펙과 다른 자리에 있다** — §4 Flow·State 는 "활동 0이면 항목 없음" 인데 코드는 `collect` 의 `NO_ACTIVITY` 로 접수 **후** 막아 항목 행이 남는다(조사를 두 번 하지 않으려는 판단). 017 Open Issue — P4 착수 전 결정 |

> SPEC-001·002·003·004는 DEC-010 반영으로 **개정**됐다(4층·concept·층별 검증). WORK-013이 그 개정분을 코드에 반영한다 — 기존 WORK-001~010이 구현한 것과 별개 커버리지다.
