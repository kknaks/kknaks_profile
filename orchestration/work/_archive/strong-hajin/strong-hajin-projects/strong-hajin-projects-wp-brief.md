# [architect] WORK-005 — 「프로젝트」 화면 실행 계획 (1루프는 코디 자율, Phase 0·E2E 는 2루프)

너는 **strong-hajin `architect` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `.md` 전부)
  (⚠ `skills.md` 의 `scripts/lint-pipeline.py` 는 **이 레포에 없다.** 린트 건너뛰고 수동 검증)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (1000줄) ← **계약의 SoT.** 여기 없는 것을 발명하지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-spec-005-report.md` ← **검수 리포트. 여기 FAIL 이 반영된 뒤의 스펙이 기준이다**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` (결정 D-01~D-27) · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/_RESUME.md` **§0 루프 구조** ← 이번 판의 범위 제약이 거기 있다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` ← 코드 지형(`파일:줄`)

작업 워크트리: **`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`** (코디 워크트리에 직접 탄다)
코드는 read-only 로 본다: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
⚠ 코디네이터가 같은 워크트리에 있다. **지정한 파일 하나 밖은 건드리지 마라.**

## 1. 꼴의 정본

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md` (1022줄) — **절 구성·frontmatter·말투를 그대로 따른다**:
Meta → Work Summary → Role Assignment → Scope → Code Surface → **Domain / Schema** → Dependency →
Internal Interface Contract → Execution(Phase 별) → 검증 계획 → **인수조건 추적** → Pre-deploy Check →
Rollback → Done Criteria → Open Issues → Related

색인 규칙은 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/README.md` (읽기만 — 색인 갱신은 코디 몫).

## 2. 산출물 — 파일 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` (id `WORK-005`, status `todo`)
links: `baselines: BASE-004` · `decisions: DEC-004` · `specs: SPEC-005`

## 3. **이번 판의 루프 구조 — 계획이 이걸 반영해야 한다**

| 루프 | 누가 | 무엇 |
|---|---|---|
| **1루프** | **코디네이터 자율 (오늘)** | BE → FE. 각 Phase 끝나면 **리뷰 + 재수정**까지 |
| **2루프** | **사용자 (내일 오전)** | **Phase 0(`material_*` 병렬 격리)** · **브라우저 E2E** 를 직접 검수하며 |

- **Phase 0 를 WP 에 쓰되 「2루프 · 사용자 동반」으로 표시**하라. 재료는
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md` 다.
  **원인이 아직 규명 안 됐다** — 「다음에 볼 자리」 셋은 가설이다. 조사와 수정을 한 Phase 에 묶어라
- **첨부(material) 관련 테스트는 1루프에서 돌리지 않는다.** 검증 계획이 그것을 **명시적으로 제외**하고,
  제외한 상태에서 **어떻게 초록을 증명하는지**를 적어라 (아래 §5)

## 4. Phase 구성 — 이 뼈대로 쪼개되 근거를 달아라

각 Phase 에 **닫는 SPEC 인수조건 번호**와 **근거 결정(D-NN)** 을 단다.

- **BE-1 — 프로젝트 상세 `tasks[]` 확장 + 상태 투영**
  담당 · 체크리스트 집계 · 하위 집계 · 기한 경과 · **`_external_state()` 적용**(BASE-004 어긋남 ①).
  이것이 FE 전부의 선행이다
- **BE-2 — 소속과 참여의 정합**
  **손자까지 따라가는 프로젝트 이동**(D-19, 어긋남 ③) · **자동 초대**(D-11·D-12) ·
  **자동 해제**(D-13~D-15). 저장 구조 변경은 **`Domain / Schema` 절에 적는다** — 이 문서가 그 자리다
- **FE-1 — 틀과 좌 레일** 3레일 등록(`onRegisterRails`) · 프로젝트 `Select` · 업무 카드 + 선택 상태 · 요약 스트립
- **FE-2 — 간트와 의존선** **깊이 제한 없는 재귀 트리**(D-16) · 들여쓰기 예산(D-18) ·
  **접힌 가지의 의존선을 접힌 부모 바에 붙이기**(D-17). **이 판의 가장 어려운 자리다**
- **FE-3 — 우 레일 · 관리 모달 · 빈 상태**
  **관리 모달의 시안은 없다 — 코디 자율로 정해졌다.** 지금 `ProjectPage.tsx:206-306` 의
  참여자·이력·생성 UI 를 **시안 `handoff/shell/js/work-modal.jsx` 의 어휘**(`Modal`·`Field`·
  `TextField`·`AutoComplete`)로 옮긴다. **새로 발명하지 마라.** 기존 테스트 6개 단언 교체도 여기
- **Phase 0 — `material_*` 병렬 격리 (2루프 · 사용자 동반)** 위 §3 참조

## 5. 검증 계획 — **첨부 제외 상태에서 초록을 증명하는 법**

`make verify` 가 exit 0 를 못 볼 수 있다. 그래서 계획에 **이 절차를 적어라**:

1. **이번 판이 더한 계약 테스트를 직렬로 따로 돌린다** (`-p no:randomly`, `-n0`) → 전부 통과를 보인다
2. **기준선 실패를 분리 보고한다** — 착수 전 기준선을 먼저 재어 두고, 회차마다 들고 나는 파일을 기록.
   `material_*` 계열은 **이번 변경과 무관**함을 그 기록으로 보인다
3. 그 기록이 **내일 Phase 0 의 입력**이다 — 어느 파일이 어느 회차에 흔들렸는지가 원인 규명의 재료다
4. FE 는 `make frontend-test` + `npx tsc --noEmit`. **브라우저 E2E 는 2루프(사용자)**

코드 레포 `AGENTS.md` 의 테스트 규약(Makefile 타겟으로만)을 따른다. 같은 검증을 중복 실행하지 않는다.

## 6. 범위 제약 — 하지 말 것

- **계약을 새로 만들지 마라** — SPEC-005 에 없으면 `## Open Issues` 로 올린다
- **결정을 새로 만들지 마라** — DEC-004 가 SoT
- **첨부(material) 관련 작업·테스트를 1루프 Phase 에 넣지 마라**
- **Phase 0 를 1루프로 끌어오지 마라** — 사용자 몫이다
- 색인(`30-work/README.md`)·`log.md` 를 건드리지 마라. **커밋·push 금지**

## 7. 검증

- Phase 마다 **닫는 인수조건 번호**와 **근거 결정(D-NN)** 이 달려 있다
- SPEC §6 의 인수조건이 **전부 어느 Phase 에든 배정**돼 있다 (「인수조건 추적」 표)
- `Domain / Schema` 절에 **저장 구조 변경이 전부** 적혀 있다 (자동 초대 흔적을 남길 자리 포함)
- 검증 계획이 **첨부 제외**와 **기준선 분리 절차**를 명시한다
- Phase 0 가 **2루프 · 사용자 동반**으로 표시돼 있다
- 소문자 `<…>` 자리표시자 0건. **지정 파일 밖 변경 0건** (`git status --porcelain` 결과를 보고에)

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_f781424f-f880-4ef0-956a-a04b165924d6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "architect 완료: WORK-005" \
  --body "파일·줄 수 / Phase 수와 이름 / 인수조건 배정 누락 여부 / Domain-Schema 변경 항목 / 검증 계획 요지 / git status / 주의점"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] architect 완료 — WORK-005 작성. 상세는 인박스." --enter
```
