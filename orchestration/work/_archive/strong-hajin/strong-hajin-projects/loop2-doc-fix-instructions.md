# 루프2 문서 수정 — 검수 FAIL 6 · WARN 4

**읽을 것**: `orchestration/work/strong-hajin-projects/review-loop2-doc-report.md` (검수 전문)
**고칠 파일 셋**: `decision-004-projects.md` · `spec-005-projects.md` · `work-005-projects.md`
그 밖은 건드리지 마라. 커밋·push 금지.

검수 판정: **계약 자체는 백로그 11건과 어긋나지 않는다.** 인수조건 48줄 전수 배정도 검수자가 다시 세어 맞다.
**FAIL 은 사실 오류·잔재·빠진 규칙에서 났다.** 지적대로 고쳐라. 아래 둘만 코디가 방향을 덧붙인다.

## FAIL-1 — `external_key` 는 **받는다**. 코디가 코드로 확인했다

**조사 리포트(`loop2-survey-report.md` Q4)가 「API 가 안 받는다」고 적은 것이 틀렸다.**
코디 실측:

```python
# modules/work/project_commands.py — ProjectCreateInput
model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
name: str = Field(min_length=1, max_length=300)
description: str | None
starts_on: date | None
ends_on: date | None
external_key: str | None = Field(default=None, max_length=200, title="외부 식별자")   # ← 있다
```
그리고 라우트가 그대로 넘긴다 — `entrypoints/http.py:1389-1400` 의 `external_key=request.external_key`.

**고칠 것**
- SPEC §2.10(프로젝트 만들기)·§4 의 「`external_key` 는 API 가 안 받는다」를 **지우고**
  **다섯 칸**으로 고쳐라: `name`(필수 1~300) · `description` · `starts_on` · `ends_on` ·
  **`external_key`(선택, 최대 200, unique)**
- ⚠ **그런데 화면이 그 칸을 «보여줄» 것인가는 별 문제다.** `external_key` 는 **데이터셋 import 의
  외부 식별자**이고 사람이 손으로 채울 값이 아니다(중복이면 DB unique 제약에 걸린다).
  → **계약은 「받는다」로 바로잡고, 화면은 「그 칸을 내지 않는다」로 적어라.** 그 둘이 다른 층이라는
  것을 한 줄로 명시하고, **미결로 올려라**(사용자가 원하면 나중에 노출한다)
- `extra="forbid"` 이므로 **모르는 필드는 422** 라는 서술은 맞다 — 그대로 둔다

## FAIL-4·FAIL-5 — 「업무 화면 로직 그대로」의 범위를 코디가 확정한다

검수 지적: 물려받을 규칙이 **셋인데 둘만 적혔다**(막힘 사유 모달 누락), 그리고 게이트가
`access=="owner"` **하나로** 적혔는데 선례 게이트는 **둘**이다.

**코디 결정: 「업무 화면 로직 그대로」는 «그 화면이 상태를 바꿀 때 지나는 모든 관문»을 뜻한다.**
드롭다운만 옮기고 관문을 빼면 **서버가 거절하는 전이를 화면이 보내는** 상태가 된다.
그러니 **선례(`MyWorkPage.tsx:1383-1416` 및 그 주변)가 가진 규칙을 전수로 옮겨 적어라** —
검수가 든 셋(요청 업무의 완료 → 완료 보고 모달 · **막힘 → 사유 입력** · 게이트 둘)을 포함해,
**그 자리가 실제로 거치는 것을 네가 코드에서 세어** SPEC 에 적는다. 빠진 것이 또 있으면 그것도 적어라.

## FAIL-6 — `App.tsx` 를 파일 목록에 넣어라

게이트가 읽을 값이 화면에 오지 않는다는 지적이다. **`App.tsx` 가 2루프 `Code Surface` 목록에 없다.**
- WORK 의 `Code Surface` 에 `App.tsx` 를 넣고 **무엇을 위해 만지는지**(게이트 값 전달 ·
  빈 상태에서도 헤더가 서게 하는 것) 적어라
- **빈 상태(프로젝트 0개)에서도 생성 버튼이 선다**는 계약이 실현 가능하려면
  `noProjects` 갈래(`ProjectPage.tsx:230-235·292-298`)도 함께 바뀐다 — 그 자리도 목록에

## FAIL-2 · FAIL-3 — 잔재 제거

- **뒤집힌 ~~D-12~~ 가 일곱 자리에 옛 뜻으로 남았다.** 검수 리포트가 그 일곱을 적어 뒀다.
  **전부 갱신하라** — 한 곳이라도 옛 뜻으로 남으면 다음 사람이 그것을 근거로 쓴다
- **「결정 27건」이 세 자리에 남아 38건과 충돌한다.** 세 문서에서 개수 서술을 찾아 **전부** 고쳐라

## WARN 넷 — 전부 닫는다

1. 미결 개수가 2 와 3 사이에서 흔들린다 → **한 수로** 맞춰라
2. **상위 인덱스·상태표가 1루프 사실에 멈춰 있다** (`20-spec/README.md` · `30-work/README.md` ·
   제품 `README.md` · `log.md`) → ⚠ **이것은 코디 몫이다. 너는 건드리지 마라.**
   대신 **무엇이 낡았는지 목록만** 보고에 적어라
3. 줄 수·묶음 수의 낡은 수치 셋 → 실측으로 고쳐라
4. **D-31 게이트의 관측 가능성** — L-17 로 증명하기 어렵다는 지적.
   **관측 가능한 문장으로 다시 쓰거나**, 「오늘의 역할 표로는 그 사람이 존재하지 않는다」처럼
   1루프에서 쓴 방식(테스트가 아니라 **코드 자리로 관측**)을 따르라

## 하지 말 것

- **새 결정을 만들지 마라** — 필요하면 §7 / Open Issues
- 색인·`log.md` 금지(WARN-2 는 코디 몫) · 1루프 Phase·기존 76줄 인수조건 재배열 금지
- 커밋·push 금지. 지정 세 파일 밖 변경 0건

## 검증

- FAIL 6 · WARN 4 각각 **어떻게 닫혔는지** 보고에 한 줄씩 (WARN-2 는 「코디 몫 — 목록만」)
- `external_key` 서술이 **계약(받는다)과 화면(안 낸다)으로 갈려** 있고 미결이 올라갔다
- **D-12 잔재 0건** · **「27건」 잔재 0건** — grep 으로 확인해 수치를 보고에 적어라
- 상태 변경이 지나는 관문이 **전수로** 적혔다
- `git status --porcelain` 이 **세 파일만** 바뀐 것을 보인다

## 역할·맥락

너는 **strong-hajin `architect` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `.md`)
- `review-loop2-doc-report.md`(검수 전문) · `loop2-backlog.md`(사용자 지시 정본) · 고칠 세 파일

워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` (코디가 함께 있다).
코드 read-only: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_94262426-6694-43a2-b6e8-4b0ad91e4bab \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "architect 완료: 루프2 문서 수정" \
  --body "FAIL 6·WARN 4 각각 어떻게 닫았나 / D-12·27건 잔재 grep 수치 / 상태 관문 전수 / 코디가 고칠 색인 목록 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] architect 완료 — 루프2 문서 수정. 상세는 인박스." --enter
```
