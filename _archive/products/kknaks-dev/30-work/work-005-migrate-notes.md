---
type: work
id: KDEV-WORK-005
title: "notes → reference 재편 + 재타이핑(type reference) + loader 재배선"
status: done
product: kknaks-dev
work_type: migration
owner: "profile-be"
roles:
  pm: ""
  design: ""
  fe: ""
  be: "profile-be"
  qa: ""
  ops: ""
progress: 100
created_at: 2026-06-30
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions: []
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works:
    - "[[work-004-migrate-projects|KDEV-WORK-004]]"
  releases: []
  related: []
---

# notes → reference 재편 + 재타이핑(type reference) + loader 재배선

`persona/notes/` 157개(13 클러스터)를 루트 `reference/`로 이동하고(D-006), 노드 타입을 `note`→`reference`로 재타이핑한다(D-010). **블로그 라우트 `/notes` 유지**(admin 결정 2026-06-30), dict 키 `notes` 보존 → /api/notes·graph·edges·FE 무변경. 데이터 이동·코드는 **하나의 atomic 커밋**.

> 비목표: contents 이동(WORK-006), enforcement(WORK-007), 시각화(WORK-008/009). **데이터 정제(Day01 중복 stem·" copy" 파일·평문 `links:`→본문 `[[]]` 정규화)는 이 work 제외 → 후속 별도 정제 work**(§Open Issue, 현재 hidden·enforcement safe).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-001-directory-structure|KDEV-SPEC-001]] (notes→reference 재편 + dir↔type 정합)
- Depends on work: [[work-004-migrate-projects|KDEV-WORK-004]]
- Follow-up work: WORK-006(contents→reference/posts), 데이터 정제 work(stem 충돌·평문 links)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | migration |
| Owner | profile-be (코드) + product-curator는 해당 없음 — placement도 persona/reference(planner/be 영역, products 아님) |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · 커밋 `a563fa9` (atomic) |
| Blocker | - |
| Next | WORK-006 contents→reference/posts |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| 배치 | profile-be | `git mv persona/notes/* → reference/` (클러스터 폴더 유지, 순수 이동·frontmatter 무편집) | done |
| BE | profile-be | auto-enrich 재배선(boot-critical) + loader scan + REQUIRED_FIELDS[reference] + map/job/test | done |
| QA | admin | boot 성공 + pytest + 새 L5 게이트 측정 + /api/notes 무회귀 → atomic 커밋 | done |

> WORK-004와 달리 **placement도 profile-be가 수행**(reference/는 products/가 아니라 루트 — curator 영역 아님, 순수 git mv+코드라 BE 일괄이 자연스럽다). 단일 워커(profile-be) 한 task. 커밋은 admin.

## 핵심 설계 (3가지 못)

1. **재타이핑은 파일 편집 없이 auto-enrich로**: notes는 frontmatter에 type/id/group이 **없고** `_auto_enrich_note`가 경로에서 주입한다. 157개 파일을 안 건드리고, auto-enrich가 `reference/` 경로 파일에 `type=reference`를 주입하게 바꾼다.
2. **클러스터 유지**: `reference/{cluster}/{note}.md` 구조 보존(13 클러스터). `/notes` 그래프 뷰가 클러스터로 렌더 → 평탄화 금지. group 검증은 `persona/_meta.yaml`의 `notes.clusters` 그대로(키 이름 유지, 선례).
3. **dict 키 `notes` 보존**: API/FE/wikilinks 코어 무변경(WORK-004 키 보존 트릭 동형).

## Code Surface

| 경로:라인 | 동작 | 위험 |
|---|---|---|
| `persona/notes/*` (157, 13 클러스터) | git mv → `reference/{cluster}/...` (frontmatter 무편집) | — |
| `persona_loader.py:37-49` `_auto_enrich_note` | **boot-critical**: `relative_to(persona_dir)` → reference는 persona_dir **밖**이라 ValueError로 enrich 누락 → `validate_persona`가 **RAISE → boot fail**. enrich 기준 디렉토리를 reference 루트로 재배선 + `"notes"` 가드 교체 + type 기본값 `reference` | ★최상 |
| `persona_loader.py:113` notes scan | `persona_dir / "notes"` → `persona_dir.parent / "reference"`. 클러스터 하위만 로드(top-level `reference/README.md` navigational 제외) | 중 |
| `persona_loader.py:64` `REQUIRED_FIELDS` | `"reference"` 항목 추가(note 미러: type/id/title/date/group). | 중 |
| `persona_loader.py:264` `_check_required(n, "note", ...)` | 라벨 `"note"` → `"reference"` | 중 |
| `persona_loader.py:189-198` `_build_graph_nodes` | notes 노드 type이 `reference`로 자동 전환(코드 변경 최소), 라벨 `"persona/notes"`→`"reference"` 정합 | 저 |
| `app/scripts/build_persona_map.py` | notes scan 경로 + `_section_notes`/graph/backlinks 경로(`[[notes/...]]`→`[[reference/...]]`) | 중 |
| `app/back/service/jobs/main_job.py:76` | `read_changed_files_today("persona/notes/")` → `"reference/"` (안 고치면 daily 잔디에서 reference 변경 silent drop) | 중 |
| `app/back/tests/test_loader.py` | `tmp_path/"notes"` 스캐폴드 → reference 레이아웃(WORK-004처럼 tmp 격리 주의: reference=persona_dir.parent라 unique repo layout 필요) | 중 |

- 무변경(키 "notes" 보존): `api/routers/notes.py`(graph/recent/search/{id}), `core/wikilinks.py`(build_graph/dead_links), `app/front/**`, `main.py`.
- `persona/_meta.yaml` `notes.clusters` **유지**(loader 계속 group 검증).

## 새 검증 게이트 (WORK-003/004와 다름 — 반드시 읽어라)

재타이핑으로 notes가 `KNOWLEDGE_NODE_TYPES`(reference)에 들어가 **L5 orphan 검사 대상으로 전환**된다. persona는 위키링크가 희박(15/299) → **L5가 0에서 다수(미인용 자료노트)로 점프하는 게 정상**(WORK-002 Phase 3가 예고). 이건 회귀 아님.

- **L1 = 0** (dead link 없음 — 진짜 안전 검사. stem 이동했지만 옵시디언/빌더 stem 추적 → inbound `[[note]]` 유지).
- **L2 = 34 불변** (새 중복 stem 없음. Day01 중복은 dict dedup으로 여전히 hidden — L2에 안 더해짐).
- **L3/L4 = 0**.
- **L5 = 156** (측정 확정, admin 독립 재현) — 재타이핑으로 reference 156 노드 전부 orphan(persona 위키링크 희박, WORK-002 Phase 3 예고대로 정상). 회귀 아님, report-only WARN. ⚠ 변동값 — 후속 work로 지식 노드 채워지면 재측정.
- **boot 성공**(validate_persona raise 안 함) = 하드 게이트. ✅ 충족.
- ⚠ **워커는 orphan을 "고치려" 링크 추가 금지** — 연결은 사람 정제(S3-정제), 마이그레이션 스코프 아님. L5는 WORK-007에서도 WARN이라 brick 안 함.

## Execution

### Phase 1 — 배치 (git mv, frontmatter 무편집)
- **Status**: DONE
- `git mv persona/notes/{cluster}` → `reference/{cluster}` (13 클러스터, 157 노트). `persona/notes/` 제거. `reference/README.md`(navigational, WORK-003) 유지. frontmatter 무편집.

### Phase 2 — auto-enrich 재배선 (boot-critical, 독립 검증)
- **Status**: DONE
- `_auto_enrich_note`를 reference 루트 기준으로 재작성(type=reference, id=stem, group=cluster).
- **독립 검증 충족**: ① 앱 boot 성공(validate_persona raise 없음) ② type=reference 156/156 · group 156/156 전수 주입 ③ persona-내부 enrich(career5/contents22/daily59) **무영향** 확인.

### Phase 3 — loader/REQUIRED_FIELDS/map/job 재배선
- **Status**: DONE
- scan 경로, `REQUIRED_FIELDS["reference"]`, `_check_required` 라벨, build_persona_map, main_job git-diff 경로, test fixture 정합. dict 키 `notes` 보존.

### Phase 4 — 검증 + atomic 커밋 (admin)
- **Status**: DONE (커밋 `a563fa9`)
- boot 성공 / pytest **263 passed** / 새 L5 게이트(L1=0·L2=34 불변·L3=0·L4=0·**L5=156**) / `/api/notes/graph` totalCount 156·edges 289·clusters 13 무회귀 / `_map.md` 재빌드(reference 링크). → 단일 atomic 커밋.

## Pre-deploy Check

- [x] report-only 유지(enforcement = WORK-007)
- [x] dict 키 "notes" 보존 → /api/notes·graph·FE 무변경
- [x] persona/notes/ 제거, reference/{cluster}/ 존재
- [x] **boot 성공**(auto-enrich 재배선 후 validate_persona raise 없음)
- [x] L5 새 baseline 측정·기록(L5=156, orphan 강제 해소 안 함)

## Rollback

- 단일 커밋 revert 1회. report-only라 서비스 영향은 loader/enrich 경로뿐.

## Done Criteria

- [x] notes 157개 → reference/{cluster}/ 이동(frontmatter 무편집), type=reference 자동 주입(156/156)
- [x] auto-enrich boot-critical 재배선 + boot 성공 검증
- [x] loader/REQUIRED_FIELDS/map/job/test 정합, pytest green(263 passed)
- [x] 새 L5 게이트 충족(L1=0·L2=34·L5=156), /api/notes 무회귀
- [x] 30-work/README·log 갱신(이 task)

## Open Issues

- **데이터 정제(deferred, 별도 work)**: ① `2024-12-30-Day01` 중복 stem(airflow vs BackendSchool, 현재 dict dedup으로 1개 silent drop — L2 hidden, enforcement safe) ② " copy" 접미 노트 3개 ③ 평문 `links:`→본문 `[[]]` 정규화(D-011). admin 결정 2026-06-30: WORK-005 제외, blast radius 최소화. 후속 정제 work에서 처리.
- L5 새 baseline = **156**(2026-06-30, a563fa9 후 측정). 변동값 — WORK-006 이후 재측정. SPEC-004 §7 참조.

## Related

- Spec: [[spec-001-directory-structure|KDEV-SPEC-001]]
- Work: [[work-004-migrate-projects|KDEV-WORK-004]]
