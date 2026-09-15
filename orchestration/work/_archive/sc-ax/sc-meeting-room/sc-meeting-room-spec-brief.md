# [planner] 회의록을 「사람 한 벌 · AI 한 벌 · 통합본」으로 다시 잡는다 — 조사

너는 **sc-ax `planner` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/planner/role.md`
  (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: **`/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec`**
(branch `kknaksss/sc-meeting-room-spec`, base `origin/main`)

## 1. 사용자가 말한 것 — 이것이 전제다. 되묻지 마라

> 「회의에 최소 2명이 들어간다 — 회의 만든 사람 / AI. **둘 다 각자 회의록을 적는다.**
>  통합본 때 최종 판정을 내린다. **두 명이 회의록을 써야 정확도가 높아진다.**」

즉 **AI 는 사람 회의록을 거드는 보조가 아니라 별개의 기록자**다. 두 벌이 독립으로 존재하고,
종료 시점에 합쳐서 최종본을 만든다.

## 2. 지금 구조가 그 전제와 어긋난다 — 코디 실측

로컬 DB 와 코드에서 확인한 것:

```
meeting_agendas: id, meeting_id, order_index, title, source, concluded,
                 created_at, updated_at, title_placeholder
```

- **안건 한 벌에 `source` 컬럼이 붙어 있다**(`manual` / `ai`) — 두 벌이 아니라 **한 벌을 둘이 나눠 쓴다**
- AI 배치가 `agenda_id` 를 받아 **기존 안건에 얹는다**. 그래서 사람이 만든 빈 안건
  (`title="안건 1"`, `source=manual`)에 AI 요약이 들어가고, 화면이 번호를 또 붙여
  **「안건 1. 안건 1」** 로 뜬다
- AI 는 `title` 을 **필수로 돌려주는데**(`schemas/ai_batch_output.json` 의 items.required 에 `title` 있음)
  그 제목이 안 쓰인다
- `title_placeholder` 라는 컬럼이 따로 있다 — 원래 「제목은 비우고 자리표시만」이 설계였던 흔적으로 보인다

**이건 표시 버그가 아니라 모델이 전제와 다른 것**이다.

## 3. 할 일 — 조사와 설계안까지. **코드는 건드리지 마라**

`products/sc-ax/` 가 문서 SoT 다(`origin/main` 에 있다). **SPEC-004(회의·미팅노트)** 가 기준이다.

### 조사

1. **SPEC-004 가 지금 무엇이라고 적고 있나** — 회의록의 주인이 하나인가 둘인가. 관련 절을 인용해라
2. **코드가 스펙과 어긋나는가, 스펙 자체가 한 벌 전제인가.** 둘은 다른 문제다
3. **지금 데이터 모델 전수** — `meeting_agendas` · `meeting_lines` · `meeting_todos` ·
   `meeting_ai_sessions` · `meeting_batch_runs` 가 각각 무엇을 담고 누가 쓰나
   (코드 리포는 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room` — **read-only**)
4. **「통합본에서 최종 판정」이 지금 어디까지 있나** — 종료 합성(`meeting.finalize`)이 무엇을 하나

### 설계안

두 벌 + 통합본을 담으려면 무엇이 바뀌어야 하는지. **정답을 하나로 몰지 말고 갈래를 제시해라.**
각 갈래마다 데이터 모델·API·화면이 어떻게 되는지, 무엇을 잃고 얻는지.

**사용자가 답해야 할 질문을 목록으로 뽑아라.** 예를 들면(이게 전부는 아니다):

- 통합 판정을 **누가** 하나 — 사람이 고르나, AI 가 제안하고 사람이 승인하나, 자동인가
- 두 벌이 **충돌**하면(같은 안건을 다르게 적었으면) 어떻게 보여주고 무엇을 남기나
- 통합 뒤 **원본 두 벌이 남나** — 근거로 남겨야 하나
- 회의 **중에** 서로의 회의록이 보이나, 종료 후에만 합쳐지나
- 사람이 안 적으면? AI 만 적으면? **한쪽이 빈 경우**
- 지금 쌓인 데이터를 어떻게 옮기나(마이그레이션)

## 4. 경계

| | |
|---|---|
| **코드 리포를 건드리지 마라** | `ax-workspace` 는 읽기만. 너는 문서 리포에서 일한다 |
| **구현을 설계하지 마라** | 「어느 파일 몇 줄」이 아니라 「무엇이 어떻게 되어야 하나」다 |
| **정하지 마라** | 갈래와 트레이드오프를 놓고, 결정은 사용자가 한다 |
| **없는 것을 지어내지 마라** | SPEC 에 없으면 「없다」고 적어라. 추측으로 채우지 마라 |
| **커밋하지 마라** | 코디가 검증하고 커밋한다 |

## 5. allowed_paths

- `products/sc-ax/`

## 6. 산출물

`products/sc-ax/00-baseline/` 아래에 조사 문서 한 장.
파일명은 그 폴더의 기존 규칙을 따라라(먼저 `ls` 로 확인).

구성:
- **지금 무엇이 있나** (SPEC 인용 + 데이터 모델 + 코드 동작)
- **전제와 어긋나는 지점** — 조목별로, 근거와 함께
- **설계 갈래** — 2~3개, 각각의 모델·API·화면·잃는 것·얻는 것
- **사용자가 답할 질문** — 목록. 각 질문이 어느 갈래를 가르는지 표시

## 7. 보고

- SPEC-004 가 회의록의 주인을 무엇이라 적고 있는지 (인용)
- 코드가 스펙을 어긴 것인지, 스펙이 한 벌 전제인지
- 제시한 갈래 수와 각 한 줄
- 사용자 질문 몇 개
- 조사하다 발견한 것 중 **네가 답 못 한 것**
