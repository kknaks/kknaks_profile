---
type: work
id: WORK-005
title: "통합 검증과 배포 — 게이트 1~5 전건 재실행 · PII 0건 · 홈서버/Vercel"
status: todo
product: ontology-demo
work_type: release
platform: "홈서버(docker + NPM) + Vercel"
target_version: "v0.1.0 (내부 공유 데모)"
owner: kknaks
roles:
  pm: "kknaks"
  design: "—"
  fe: "@ontology-fe"
  be: "@ontology-be"
  qa: "coordinator"
  ops: "kknaks"
progress: 0
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/work
  - work-type/release
  - status/todo
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-005-internal-demo-deploy|DEC-005]]"
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
  specs:
    - "[[spec-001-data-layer-contract|SPEC-001]]"
    - "[[spec-002-mcp-tools-contract|SPEC-002]]"
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
    - "[[spec-004-three-screens|SPEC-004]]"
    - "[[spec-005-agent-loop-and-gates|SPEC-005]]"
  works:
    - "[[work-003-agent-loop-and-chat|WORK-003]]"
    - "[[work-004-frontend-three-screens|WORK-004]]"
  releases: []
  related: []
---

# 통합 검증과 배포 — 내부 공유 데모

게이트 5종을 **전건 재실행**하고 PII 노출 0건을 스캔한 뒤, 프론트는 Vercel(기존 profile
배포에 포함) · 백/redis/codex 워커는 홈서버(docker + NPM 서브도메인)로 올린다.
가드는 **공유 비밀번호 하나**다.
**비목표**: 외부 공개 전환 · rate limit·계정 체계 · 수집 자동화 · 알림 발송.

> `work_type: release` 작업이다. 스토어 심사가 아니라 **자체 배포**이므로 템플릿의
> 「심사 체크리스트」는 **배포 전 체크리스트**로, 「제출 기록」은 **배포 기록**으로,
> 「심사 결과」는 **배포 검증 결과**로 읽는다.

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-001~005 의 게이트·AC 를 **통합 재실행**으로 커버(신규 계약 없음)
- Depends on work: WORK-003(BE 완주) · WORK-004(FE 완주)
- Parallel work: 없음 — 마지막 단계다
- Follow-up work: 수집 파이프라인(다음 단계 과제)
- External dependency: 홈서버(docker + Nginx Proxy Manager) · Vercel(기존 profile 배포) ·
  `app/back` compose 의 redis. 비밀번호·API base URL 은 **배포 시 사용자가 직접 주입**한다.

## Work Summary

| Field | Value |
|---|---|
| Type | release |
| Platform | 홈서버(docker + NPM) + Vercel |
| Target Version | v0.1.0 (내부 공유 데모) |
| Owner | @ontology-be + @ontology-fe |
| Status | todo |
| Progress | 0% |
| Next | WORK-003·004 완주 후 Phase 1 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 배포 범위·시점 | todo |
| Design | — | 해당 없음 | todo |
| FE | @ontology-fe | Vercel 편입·env·화면 검증 | todo |
| BE | @ontology-be | 게이트 재실행·compose·NPM | todo |
| QA | coordinator | 게이트 전건·PII 스캔 판정 | todo |
| Ops | kknaks | 홈서버·비밀번호 주입 | todo |

## 출시 대상

| Item | Value |
|---|---|
| Platform / 채널 | 프론트 **Vercel**(기존 profile 배포에 포함) · 백/redis/codex 워커 **홈서버 docker** |
| Version | v0.1.0 (내부 공유) |
| 접근 가드 | 공유 비밀번호 **하나**(env `ONTOLOGY_DEMO_PASSWORD`) — rate limit·계정 없음 |
| 도메인 | NPM 서브도메인(백) · 기존 profile 도메인 경로(프론트) |
| 데이터 | 배포 DB 사본은 **홈서버 볼륨(레포 밖)**. 원천·DB gitignore 유지 |
| 재사용 런북 | 이번 회차에서 절차를 확정하고, 반복이 생기면 `70-runbook/` 으로 승격 |

## 배포 전 체크리스트

누락 시 배포를 진행하지 않는다.

| # | 항목 | 충족 | 근거/비고 |
|---|------|------|-----------|
| 1 | 게이트 1(브론즈 대사) 재실행 통과 | [ ] | SPEC-001 AC-1 |
| 2 | 게이트 2(빌드 재현) 재실행 통과 | [ ] | SPEC-001 AC-2 |
| 3 | **게이트 3(PII 마스킹) — 화면·API·에이전트 응답 원값 0건** | [ ] | SPEC-005 G3 |
| 4 | 게이트 4(회귀 3본) 재실행 통과 | [ ] | SPEC-005 G4 |
| 5 | 게이트 5(근거 무결성 ①②③) 통과 | [ ] | SPEC-005 G5 |
| 6 | 비밀번호가 레포·문서·응답·로그 어디에도 없음 | [ ] | DEC-005 · SPEC-003 AC-2 |
| 7 | 「실시간」 계열 카피 0건 · 기준일 배지 전 화면 | [ ] | DEC-005 D4 |
| 8 | 기존 포트폴리오 표면 무변경(`globals.css`·루트 레이아웃·`/chat`) | [ ] | SPEC-004 AC-2·AC-3 |
| 9 | 기존 `app/back` 워커·큐(`default`·`chat`) 계약 무변경 | [ ] | diff 확인 |

## Execution

### Phase 1 — 게이트 전건 재실행과 PII 스캔

- **Status**: TODO
- **설명**: 각 WP 가 자기 게이트를 통과했더라도, **합쳐 놓은 상태에서 다시** 돌려야
  배포 가능 여부를 말할 수 있다.
- **작업**:
  - [ ] 게이트 1·2 재실행 — WORK-001 이 낸 CLI 를 그대로 부른다
  - [ ] 게이트 4 재실행 — WORK-003 의 회귀 3본
  - [ ] 게이트 5 ①②③ — 답변 수치 재조회 · `used_edges` ⊆ 확정 ·
        **하이라이트 = `used_edges`**(검증 대상 화면 = **모니터링 그래프 단일**)
  - [ ] **게이트 3 PII 스캔** — 화면(3페이지)·API 응답·도구 응답·에이전트 답변·드릴다운·
        로그를 훑어 실명·전화·생년월일 원값 검출 0건
- **검증**:
  - [ ] 게이트 5종이 **한 번의 실행으로** 전건 판정된다
  - [ ] 스캔 대상 표면 목록이 빠짐없이 열거돼 있다(화면·API·도구·답변·로그)
- **완료 증거**: 미작성 — 게이트 5종 판정표(수치 포함: 브론즈 대사 오차 0 · 매출
  2,615,555,218 · 결제 내원 5,428 · 신환 3,447 · 내원 47,537 · 일별 235 · 회귀 3본 통과) +
  **PII 원값 검출 0건** 스캔 리포트 + 게이트 5-③ 집합 일치 캡처

### Phase 2 — 회귀 자동화

- **Status**: TODO
- **설명**: 한 번 통과한 것이 다음에도 통과하는지를 사람이 기억하지 않게 만든다.
- **작업**:
  - [ ] 게이트 1~5 + PII 스캔을 **명령 하나**로 묶는다(로컬 재현 가능)
  - [ ] 판정은 단언으로 — 수치는 정확 일치, 서술은 키워드 포함
  - [ ] 실패 시 어느 게이트가 왜 깨졌는지 코드·기대·실측을 출력
  - [ ] 자동 실행 경로 등록(가능한 범위에서 — 데모라 무겁게 만들지 않는다)
- **검증**:
  - [ ] 일부러 데이터를 흔들면 해당 게이트만 정확히 실패한다
  - [ ] 반복 실행이 같은 결과를 낸다
- **완료 증거**: 미작성 — 통합 실행 로그 1회분 + 고의 실패 주입 시 실패 게이트 지목 로그

### Phase 3 — 배포 구성

- **Status**: TODO
- **설명**: 상주 프로세스(redis·codex 워커)는 Vercel 에 올릴 수 없다. 백은 홈서버로 간다.
- **작업**:
  - [ ] 홈서버 compose — 백(API) · redis · codex 워커(`queue=ontology`).
        **기존 서비스 정의 무변경**
  - [ ] NPM 서브도메인 + 인증서 · 백 내부 포트만 노출
  - [ ] 배포 DB 사본을 **홈서버 볼륨(레포 밖)**에 배치. 원천 데이터는 올리지 않는다
  - [ ] Vercel — 데모 라우트 그룹이 기존 profile 배포에 포함되도록 · 백 API base URL env
  - [ ] 비밀번호 주입 절차 문서화 — env 이름만 적고 **값은 어디에도 적지 않는다**
- **검증**:
  - [ ] 백 컨테이너가 DB 볼륨을 읽고 게이트 1·2 를 재실행할 수 있다
  - [ ] 프론트에서 백 API 가 도메인 경유로 닿는다(CORS·쿠키 포함)
  - [ ] 기존 profile 사이트·기존 워커가 영향받지 않는다
- **완료 증거**: 미작성 — compose diff(신규 서비스만) + NPM 라우팅 확인 + 프론트→백
  왕복 1건 성공 로그 + 비밀번호 값 미포함 확인

### Phase 4 — 배포 검증과 마감

- **Status**: TODO
- **설명**: 실제로 눌러 봐야 데모다. 게이트가 배포 환경에서도 성립하는지 확인한다.
- **작업**:
  - [ ] 접속 게이트 통과 → 세 화면 순회(모니터링 → 데이터 → 채팅)
  - [ ] 채팅 1문 완주 — `pending` 진행 표시 → `done` → 칩 클릭 → 모니터링 하이라이트
  - [ ] 브론즈 드릴다운 1건 — 마스킹 표기 확인
  - [ ] 배포 환경에서 게이트 3(PII) 재스캔
  - [ ] 배포 기록·검증 결과 표 갱신, 남은 이슈 목록화
- **검증**:
  - [ ] 「실시간」 카피 0건 · 기준일 배지 전 화면
  - [ ] 첫 응답 지연 실측(180초 timeout 대비 여유 확인)
- **완료 증거**: 미작성 — 세 화면 스크린샷 + 채팅 완주 기록(소요시간 포함) +
  배포 환경 PII 재스캔 0건

## 배포 기록

| 날짜 | Version | 채널 | 결과 | 비고 |
|---|---|---|---|---|
|  | v0.1.0 | 홈서버 + Vercel |  |  |

## 배포 검증 결과

| 날짜 | 상태 | 사유 / 메모 | 후속 조치 |
|---|---|---|---|
|  |  |  |  |

## 출시 정보

| Resulting Release | Action | Notes |
|---|---|---|
| (미정) | create `60-release/release-001-*.md` | 배포 완료 후 생성. `60-release/` 는 아직 없다 — 이번에 처음 생긴다 |

## Pre-deploy Check

- [ ] 기존 서비스 영향 없음 — 포트폴리오 사이트 · `app/back` 워커·큐 무변경
- [ ] credential/env 신규 노출 없음 — 비밀번호·API 키가 레포·로그·응답에 없음
- [ ] 응답·화면에 PII 원값 없음(게이트 3)
- [ ] 원천 데이터·DB 파일이 커밋되지 않았다
- [ ] 링크가 퍼지면 그대로 열린다는 점을 공유 시 함께 알린다(가드는 비밀번호 하나뿐)

## Rollback

- **프론트**: 라우트 그룹 `app/(ontology)` 미배포(디렉토리 삭제 또는 이전 배포로 되돌림).
  포트폴리오 표면은 건드리지 않았으므로 영향 범위가 없다.
- **백**: compose 에서 신규 서비스(백·워커)를 내리고 NPM 라우팅을 제거하면 표면이 사라진다.
  DB 산출물은 **재빌드로 복원** — 파괴적 마이그레이션이 없다.
- 롤백 후에도 기존 profile 배포·기존 워커는 계속 돈다.

## Acceptance Criteria

- [ ] 배포 전 체크리스트 9항목 전건 충족
- [ ] 게이트 1~5 가 **배포 환경에서** 재실행 통과
- [ ] PII 원값 노출 **0건**(화면·API·도구·답변·로그)
- [ ] 세 화면이 공유 링크 + 비밀번호로 열린다

## Done Criteria

- [ ] 모든 Phase 가 `DONE`
- [ ] 배포 기록·검증 결과 표가 최신
- [ ] product `log.md` · `30-work/README.md` 갱신(코디네이터)
- [ ] 배포 완료 시 `60-release/` 릴리즈 노트를 만들고 `links.releases` 에 잇는다

## Open Issues

- 갱신 주기가 일 1회인데 **재빌드를 누가 언제 도는지**는 정해지지 않았다 — 수동 실행으로
  시작하고, 반복이 생기면 `70-runbook/` 승격 또는 다음 단계(수집 파이프라인)로 넘긴다.
- LLM 호출 비용에 상한이 없다(DEC-005 D2 — 가드를 두지 않기로 확정). 사용량이 늘면
  **DEC-005 재검토 사안**이지 워커가 임의로 가드를 넣을 일이 아니다.
- 게이트 5-③ 검증을 자동화할지(E2E) 사람 확인으로 둘지는 Phase 2 에서 판단해 보고한다.

## Related

- SPEC: frontmatter `links.specs` · Work: 선행 WORK-003·004 · Decision: DEC-005
