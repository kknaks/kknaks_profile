
# [backend] WORK-001 데이터 기반 — DB·마스킹 뷰·브론즈~온톨로지 적재 (게이트 1·2)

너는 **ontology-demo `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/ontology-demo/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation`
base 브랜치: `origin/ontology-demo` → 최종 PR 대상 `ontology-demo` (PR 은 코디네이터가 올린다)

이 워크트리는 backend 워커 단독이다.

## 1. SSOT — 먼저 읽을 것

**spec·work 문서는 네 base 에 아직 없다** (문서 PR 미머지) — 아래 절대경로(read-only)로 읽어라. 복사·수정 금지:

- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/30-work/work-001-data-foundation.md` ← **이번 작업의 SoT.** P1~P5 phase·완료 증거가 전부 여기 있다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/20-spec/spec-001-data-layer-contract.md` ← 데이터 계약(테이블 목록·enum·마스킹 뷰·표기·대조값·AC). **여기 없는 건 발명하지 마라.**

변환 규칙·게이트 명세의 SoT 는 기록이다 (네 워크트리 안, read-only):

- `para/resources/note/ontology/2026-09-01-ontology-02-research.md`(브론즈 실사·행수) · `-03-glossary.md`(글로서리·PII 반입) · `-04-silver.md`(실버 변환 규칙·게이트) · `-05-kpi.md`(골드 계산식·게이트·대조값)

**기대는 개념**:

- `para/areas/concept/db/medallion-architecture.md` — 계층 책임 분리(브론즈 원형 보존·상위는 바로 아래만)를 이대로.
- `para/areas/concept/db/pii-masking.md` — 마스킹 뷰 단일 경계·전처리 순서(마스킹이 파싱·채점보다 앞)를 이대로.

## 2. 배경 / 무엇을 바꾸나

기존 산출물은 파일(CSV) 기반이다 — `reference/ontology_demo/scripts/` 의 빌드 스크립트가 원천 파일을 읽어 CSV 를 낸다. 이번 작업은 그 파이프라인을 **SQLite 한 DB** 로 이식한다: 브론즈(원형) 적재부터 실버·골드 빌드, 온톨로지(nodes/edges) 적재까지. **변환 규칙·게이트는 이식이지 재설계가 아니다** — 기존 스크립트의 로직을 그대로 옮기고 입출력만 파일→DB 로 바꾼다. LLM 리뷰 재채점 금지(기존 `_scoring/` 산출물 사용).

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

- 테이블·뷰 이름, enum, 마스킹 표기(`김○○`/`010-****-1234`/`1990-**-**`), 월 View(`gold_kpi_monthly`)는 SPEC-001 §4 그대로 — 후속 WORK-002(도구·API)가 이 이름으로 소비한다.
- DB 파일 경로·원천 경로는 `config.py` 의 env(`ONTOLOGY_DATA_DIR` 등) 경유 — 하드코딩 금지.
- 데이터 경계: **원천** = `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/` (절대경로 read-only — PII 포함·gitignore 라 네 base 에 없다. 복사·커밋 금지). **산출 DB** = 네 워크트리 로컬(`ONTOLOGY_DATA_DIR` 로 지정한 경로 하위) — 커밋 금지(gitignore 확인).

## 4. 먼저 읽을 핵심 파일

- `app/ontology-agent/config.py` — env 설정 패턴. 필요한 키는 여기에 더한다
- `app/ontology-agent/build/` — 빌드 모듈이 들어갈 자리(빈 뼈대)
- `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/scripts/` — 이식 원본(build_reservations·build_catalog·reviews_*·build_gold) (read-only)
- `app/back/config.py` — pydantic-settings 모범 (참조만)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/ontology-agent/`

## 6. 구현 단계 — work 문서의 phase 를 그대로 탄다 (P1→P5 순서, phase 단위 보고)

1. **P1** DB 부트스트랩 + 브론즈 스키마 (SPEC-001 §4 브론즈 16테이블)
2. **P2** `load_bronze` — 원천 → 브론즈 원형 적재. **게이트 1: 행수 대사 전 테이블 오차 0** (vegas 78,216 · 리뷰 1,962(csv 파서 기준) · nexus 테이블별 원본 일치)
3. **P3** 마스킹 뷰 `v_*` (SPEC-001 마스킹 표기·`authorName` 포함)
4. **P4** 실버·골드 빌드 이식 + `gold_kpi_monthly` 신설. **게이트 2: 재현 대조값 일치** (매출 2,615,555,218 · 결제 내원 5,428 · 신환 3,447 · 내원 47,537 · 일별 235행). monthly·retention 행수는 실측해 보고에 등재
5. **P5** 온톨로지 nodes/edges 적재 — **고아 0** (edges 의 cause/effect 전건이 nodes 에 존재)

각 phase 완료 시 게이트를 pytest 로 감싼 테스트가 함께 남아야 한다(역할 workflow.md §4).
phase 를 마칠 때마다 §9 (2) 채널로 `[진행] P<n> 완료 — <게이트 수치>` 를 보내라. 전체 완료 시에만 §9 두 명령을 모두 실행한다.

## 7. 범위 제약 — 하지 말 것

- 도구(MCP)·API·화면 — WORK-002~004 몫. 만들지 마라.
- 변환 규칙·게이트 기준 재해석·완화 금지 — 어긋나면(예: 대조값 불일치) 코드로 맞추지 말고 즉시 질문 채널로 보고. **문서가 먼저다.**
- 원천 데이터 복사·커밋 금지 · 산출 DB 커밋 금지 · PII 를 로그·테스트 픽스처에 쓰지 마라.
- git commit·push·PR 금지.

## 8. 검증

```
cd app/ontology-agent && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-001 데이터 기반" \
  --body "변경 파일 목록 / phase 별 게이트 수치(1·2 + monthly·retention 실측) / 테스트 결과 / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] backend 완료 — WORK-001 P1~P5 + 게이트 1·2 수치. 상세는 인박스." --enter

# 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[질문] backend: <질문>" --enter
```
