# [reviewer] SPEC-005 검수 — 계약이 결정과 코드 둘 다에 맞는가

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더의 다른 `.md` 전부)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (1000줄) ← **검수 대상**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` ← 결정 27건(D-01~D-27). **계약의 상위 근거**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md` ← 사실·어긋남 ①~⑤
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` ← 근거 출처

작업 워크트리: **`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`** (코디 워크트리에 직접 탄다)
코드는 **read-only 로 이 경로를 본다**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
⚠ 코디네이터가 같은 워크트리에 있다. **리포트 파일 하나 밖은 아무것도 건드리지 마라.**

## 1. 판정 규칙

- **FAIL** — 계약과 다른 것이 서 있다 (결정과 어긋남 · 코드 사실과 어긋남 · 내부 모순)
- **WARN** — 물어야 할 만큼 모호하다 (구현자가 둘로 읽을 수 있다)
- **PASS** — 근거를 대어 통과

**각 지적에 `파일:줄` + 근거를 반드시 단다. 근거 없는 지적은 쓰지 마라.**
**「조용히 통과하는 자리」를 따로 본다** — 결정 번호만 달려 있고 내용이 그 결정과 다른 조문,
표에는 있는데 본문이 안 받는 항목, 「세었다」고 적었지만 실제로 안 센 것.

## 2. 반드시 확인할 것

1. **결정 27건 전수 대조** — §6 추적표가 맞나. **번호만 맞는 게 아니라 내용이 그 결정과 같은가.**
   특히 D-20~D-25 구간: 작성자가 「발주서 번호가 DEC-004 본문과 한 칸 어긋나 DEC-004 를 따랐다」고
   보고했다. **DEC-004 본문 번호가 맞는지 직접 확인하라**
2. **저장 구조 누수 0건인가** — 컬럼·인덱스·FK·마이그레이션 서술이 있으면 FAIL
   (`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/README.md` § Data / Domain Boundary 가 기준)
3. **「새 라우트 0건·새 오류코드 0건」 주장이 사실인가** — 코드 레포에서 **직접 grep** 해서
   스펙이 쓰는 경로·오류 이름이 **실재하는지** 확인하라. 없는 이름을 쓰면 FAIL
4. **자동 초대 표면 「붙는 3 / 뺀 6 / 떼는 3」 이 맞나** — `task.assign` 이 지나는 자리를
   **네가 직접 grep 으로 세어** 대조하라. 빠진 표면이 있으면 FAIL
5. **인수조건이 관측 가능한가** — 「올바르게 동작한다」 같은 문장은 WARN.
   핵심 넷(손자 행 · 접어도 안 사라지는 의존선 · 프로젝트 밖 사람 초대와 거절 시 해제 · 이동 시 손자 추종)이 들어 있나
6. **기존 스펙과 충돌 없나** — SPEC-001(선행·기한) · SPEC-003(상태·상위/하위·중심 업무) ·
   SPEC-004(어휘 정본). **특히 상태 어휘와 깊이 정책**
7. **시안 기하와 어긋난 값이 없나** — 레일 폭 380/342 · 행 40 · 하루 34 · 라벨 200 · 바 3종.
   변경된 값(들여쓰기 12px·최대 5단)은 **결정 D-18 이 근거로 달려 있는가**

## 3. 이번에 **범위 밖**인 것 — 지적하지 마라

- **Phase·일정·구현 순서** (WORK-005 몫)
- **첨부(material) 관련 계약·테스트** — 이번 루프에서 의도적으로 제외했다
- **Phase 0(`material_*` 병렬 격리)** — 내일 사용자가 검수하며 진행한다
- 문서의 말투·표 서식 취향

## 4. allowed_paths

- **read-only.** 문서·코드 **어느 것도 고치지 마라.** 커밋·push 금지. 테스트·서버 실행 금지
- **쓰는 파일은 정확히 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-spec-005-report.md`

## 5. 리포트 형식

머리에 **판정 한 줄**(FAIL n건 · WARN n건 · PASS) → 지적마다
`[FAIL-1] 제목 / 무엇이 / 근거 파일:줄 / 무엇과 어긋나나(결정 번호 또는 코드) / 어떻게 고치면 되나 한 줄`
→ 마지막에 **§2 의 7개 확인 항목 각각에 결과**를 남긴다(확인했다는 증거로).

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_455fc57d-ccc8-44c8-8d18-40996ad6d6c2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer 완료: SPEC-005 검수" \
  --body "판정(FAIL n·WARN n) / 가장 큰 지적 3개 / §2 항목 7개 결과 / git status / 주의점"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — SPEC-005 검수. 상세는 인박스." --enter
```
