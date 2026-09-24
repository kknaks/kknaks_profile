# WORK-005 정정 — 옛 뜻 D-31 여섯 자리 (코디 지시 범위의 구멍이었다)

**고칠 파일 하나**: `para/projects/summer-star/strong-hajin/30-work/work-005-projects.md`
그 밖은 건드리지 마라. **코드 read-only.** 커밋·push 금지.

## 배경

**D-31**(생성 버튼의 게이트는 `PROJECT_MANAGE`)이 **사용자 지시로 뒤집혀 D-39 가 됐다**
(「**추가는 모든 사람이 할 수 있다고**」). DEC-004 와 SPEC-005 는 **이미 정정됐다** —
`~~D-31~~ → D-39`, 「버튼은 뜨고, 거절은 모달이 말한다」.

**그런데 코디가 그 판의 범위를 「파일 둘」로 못 박아서 WORK-005 가 빠졌다.** 그 판의 워커가
**여섯 자리를 세어 남겨 뒀다.**

## 고칠 자리 — 앞 판 워커가 센 여섯

| 줄 | 지금 뭐라 적혀 있나 |
|---|---|
| `:272` | **F9 행** — 「넘길 것은 **둘** — `project.manage`(생성 버튼 게이트)…」 |
| `:499` | (같은 계열 서술) |
| `:1259` | **근거 결정이 `D-31`** 로 달려 있다 |
| `:1268` | 「**세션 값 둘**」 |
| `:1350` | **L-17 의 옛 인수조건** — 「헤더 등록 노드가 `null`」 |
| `:1557` | (같은 계열 서술) |

⚠ **`:272`(F9)와 `:1350`(L-17)은 FE 가 이미 코드에서 걷어낸 것과 어긋난다**
(`loop2-final-fix-report.md` §A-2 — `canCreateProjects` 배선을 없앴다). **문서가 코드보다 낡았다.**

## 어떻게

- **SPEC-005·DEC-004 가 쓴 것과 «같은 서식»**으로 — `~~D-31~~` 취소선 + 「2026-09-22 정정 — D-39」
- **`:1350` L-17 은 삭제하지 말고 «뒤집어»** 써라. SPEC-005 의 L-17 이 이미 그렇게 돼 있으니
  **그 문장과 일치**시켜라(SPEC 이 계약의 정본이다)
- **`:272` F9** — 넘기는 세션 값이 **둘에서 하나로** 줄었다(`task.self_manage` 만).
  ⚠ **상태 드롭다운 게이트는 안 움직인다** — 그 사실을 같은 줄에 적어 둘이 안 섞이게 하라
- **인수조건 배정·부담 수치가 틀어졌으면** 같이 맞춰라

## 검증

- `grep -n 'D-31' work-005-projects.md | grep -v '~~' | grep -v '뒤집' | grep -v '정정'` → **0건**
- 옛 계약 문장(「자격을 가졌는가」·「헤더 등록 노드가 null」·「세션 값 둘」)이
  **살아 있는 자리 0건** — 취소선 안의 보존 기록만 남아야 한다
- **`task.self_manage` 서술이 안 흔들렸다**
- WORK 의 L-17 문장이 **SPEC-005 의 L-17 과 일치**한다
- `git status --porcelain` 이 **그 파일 하나만** 바뀐 것을 보인다

## 역할·맥락

너는 **strong-hajin `architect` 워커**다. 먼저 읽어라:
- `.../roles/strong-hajin/planner/role.md` (+ 같은 폴더 `.md`. ⚠ lint 스크립트 없음 — 건너뛰어라)
- `decision-004-projects.md` 의 **D-39** 와 **~~D-31~~ 뒤집음 블록**(서식의 본보기)
- `spec-005-projects.md` 의 **L-17**(문장을 여기에 맞춘다) · §2.10
- `loop2-final-fix-report.md` §A-2(FE 가 코드에서 무엇을 걷어냈는지)

워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` (코디가 함께 있다).

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_5403e9f8-4c0b-4785-a418-ca34d00b5da0 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "architect 완료: WORK-005 D-31 정정" \
  --body "고친 자리 여섯 / grep 잔재 수치 / L-17 이 SPEC 과 일치하나 / task.self_manage 무변경 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] architect 완료 — WORK-005 D-31 정정. 상세는 인박스." --enter
```
