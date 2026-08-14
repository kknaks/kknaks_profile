---
type: work
id: KDEV-WORK-021
title: "노트 출력 계약에서 JSON 을 뺀다 — 구분자 레코드"
status: in_progress
product: kknaks-dev
work_type: refactor
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: —
progress: 80
created_at: 2026-08-13
updated_at: 2026-08-13
tags:
  - product/kknaks-dev
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# 노트 출력 계약에서 JSON 을 뺀다 — 구분자 레코드

노트를 만드는 게이트 넷(`source_note`·`concept`·`derived`·`post`)이 markdown 전문을 JSON 문자열 값에 넣는 것을 멈추고, **이스케이프가 필요 없는 구분자 레코드**로 낸다.

**만들지 않는 것**: 잔디(`daily`) 게이트 이관, route 출력 형식 변경, 발행부(`apply`) 계약 변경.

## Meta

- Baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]
- Covers spec: [[spec-008-gate-chain|KDEV-SPEC-008]] (§4 「노트 출력 형식 — 구분자 레코드」)
- Depends on work: 없음
- Parallel work: [[work-022-stage-session-inheritance|KDEV-WORK-022]] — 같은 파일을 만지지만 자리가 다르다(이쪽은 출력 파싱, 저쪽은 세션·payload)
- Follow-up work: 잔디 게이트 이관 (SPEC-008 §7 OPEN)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner | kknaks |
| Status | in_progress |
| Progress | 80% |
| Branch/PR |  |
| Blocker |  |
| Next | P5 — 배포 후 실전 1건 무재시도 완주 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 형식 확정 | done |
| Design | — | 화면 없음 | — |
| FE | — | 프론트 변경 없음 — 승인 화면이 보는 payload 모양은 그대로다 | — |
| BE | kknaks | 파서·프롬프트·스테이지 배선 | done |
| QA | kknaks | 회귀 + 실전 1건 무재시도 완주 | 회귀 done · 실전 대기 |
| Ops | — | 배포 절차 변경 없음 | — |

## Scope

포함:

- `stages/common.py` 에 구분자 레코드 파서 신설 — 관용 규칙 포함
- `OUTPUT_CONTRACT`·`OUTPUT_CONTRACT_LIST` 교체, `OUTPUT_CONTRACT_ONE` 신설
- 스테이지 넷 배선: `source_note`·`post`(단일) · `concept`(0..N) · `derived`(단일 · 필드 다수)
- `parse_json_output` 제거 — 남기면 새 형식과 두 벌이 된다
- 실전 자료 1건 무재시도 완주 확인

제외:

- 잔디(`daily`) 게이트 — 산출물이 넷으로 중첩돼 레코드 하나로 안 떨어진다. 형태를 먼저 정한다
- `route` — 본문이 없어 이스케이프가 문제 되는 자리가 아니다
- `extract_json_object` — route·daily 가 계속 쓴다. 그대로 둔다
- 승인 payload 계약 (`filename_stem`·`content`·`target_path`) — **바꾸지 않는다.** 바꾸면 화면과 발행부가 같이 움직여야 한다

## Code Surface

- Repo / module: `app/back` (백엔드 전용)

| 경로 후보 | 설명 |
|---|---|
| `service/pipeline/stages/common.py` | **주 변경.** 레코드 파서 · 출력 계약 문구 · `parse_note_output` |
| `service/pipeline/stages/source_note.py` | 44행 — 계약 문구만 갈아 끼운다 |
| `service/pipeline/stages/post.py` | 110행 — 〃 |
| `service/pipeline/stages/concept.py` | 274·293행 — `RESULT_SHAPE` 와 `parse` |
| `service/pipeline/stages/derived.py` | 170·179행 — `RESULT_SHAPE` 와 `parse`. 헤더 키가 여럿이다 |
| `tests/test_pipeline_concept.py` · `test_pipeline_derived.py` | 기존 테스트가 JSON 원문을 만든다 — 같이 옮긴다 |
| `tests/test_pipeline_notes.py` | **신설.** 파서 자체의 관용·거부 경계 |

- Domain / schema note: **DB 변경 없음.** 바뀌는 것은 AI 와 백엔드 사이의 wire 형식뿐이고, `GateRevision.payload` 에 저장되는 모양은 그대로다.

## Domain / Schema

해당 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 스테이지 넷 | `parse_records(raw, keys=...)` | 레코드 목록 |
| `source_note`·`post` | `parse_note_output(raw)` | `(stem, content)` — **시그니처 유지** |
| 승인 화면 · 발행부 | `revision.payload` | **바뀌지 않는다** |

## Internal Interface Contract

```python
MARKER = "---8<---"          # 뒤에 note | content | end | none 이 붙는다

@dataclass(frozen=True)
class Record:
    header: dict[str, list[str]]   # key -> 나온 순서대로의 값들
    body: str                      # 손대지 않은 본문
    def one(self, key: str) -> str        # 없거나 비면 ""
    def many(self, key: str) -> list[str] # 반복 줄 + 쉼표 분해

def parse_records(raw: str, *, keys: frozenset[str]) -> list[Record]
def parse_note_output(raw: str) -> tuple[str, str]    # 단일 레코드 — 종전 시그니처
```

**`keys` 를 받는 이유**: 머리말을 어디서 자를지 판단하려면 「이것이 헤더인가 산문인가」를 알아야 한다. 아는 키가 나오는 줄부터가 헤더다. 이 인자가 없으면 `참고:` 로 시작하는 설명 문장이 헤더로 읽힌다.

## Execution

### Phase 1 — 레코드 파서

- **Status**: DONE
- **설명**: 형식의 전부가 여기 있다. 관용의 범위도 여기서 정해진다.
- **작업**:
  - [x] 마커 정규식 — `---8<---` + 선택적 역할(`note`·`content`·`end`·`none`), 앞뒤 공백 허용
  - [x] 헤더 파싱 — `key: value`, 같은 키 반복이면 목록, 모르는 키는 버린다
  - [x] 본문 — content 마커 다음 줄부터 다음 마커/EOF 까지 **원문 그대로**, 앞뒤 빈 줄만 다듬는다
  - [x] 관용 ①: 출력 전체를 감싼 코드펜스를 벗긴다
  - [x] 관용 ②: 첫 마커 또는 아는 헤더 키 앞의 산문을 버린다
  - [x] 관용 ③: `---8<--- end` 뒤를 버린다
  - [x] 거부: 마커 없음 · 본문 빔 → `GateError("INVALID_NOTE_OUTPUT", ...)`, 메시지에 **무엇을 봤는지** 담는다
  - [x] `---8<--- none` → 빈 목록 (`concept` 0건)
- **검증**:
  - [x] 본문에 `"` · `\` · 줄바꿈 · ` ``` ` 코드펜스 · frontmatter `---` 가 들어간 노트가 **한 글자도 안 변하고** 돌아온다
  - [x] 머리말·꼬리말·코드펜스 각각을 붙인 출력이 통과한다
  - [x] **가드를 깨뜨려 본다** — 마커를 지운 출력, 필수 키를 지운 출력, 본문이 빈 출력이 각각 실패하는지 확인하고 원복해 통과하는지도 확인한다
  - [x] 본문 안에 `---8<---` 가 들어간 경우의 동작을 테스트로 고정한다
- **완료 증거**: `parse_records(raw, *, keys)` + `Record`. `tests/test_pipeline_notes.py` 20건.

  **`keys` 인자가 이 파서의 핵심 판단이다.** 머리말을 어디서 자를지는 「이 줄이 헤더인가 산문인가」로 갈리는데, 그 판정을 **아는 키인지**로만 한다. 없으면 `참고:` 로 시작하는 설명 문장이 헤더로 읽힌다.

  **본문 안의 역할 없는 마커는 글자로 읽기로 했다** — 계획서에는 「레코드가 갈린다」고 적었는데, 만들면서 뒤집었다. 구조로 읽으면 노트가 **소리 없이 잘리고**, 글자로 읽으면 형식이 조금 이상한 노트가 승인 화면에 올라간다. 사람이 볼 수 있는 쪽이 낫다. `note`·`end` 는 구조로 남는다.

### Phase 2 — 단일 노트 스테이지 (`source_note` · `post`)

- **Status**: DONE
- **설명**: 가장 단순한 형태. 헤더 키가 `filename_stem` 하나다.
- **작업**:
  - [x] `OUTPUT_CONTRACT` 를 구분자 형식으로 교체 — 「JSON 이 아니다」를 명시한다
  - [x] `parse_note_output` 내부를 레코드 파서로 갈아 끼운다. **시그니처는 그대로**
  - [x] 레코드가 2건 이상이면 실패시킨다 — 단일 노트 스테이지다
- **검증**:
  - [x] 기존 `check_note`·`check_post` 검증이 그대로 걸린다(stem 규약 · 필수 필드 · id 불일치)
  - [x] 경로·확장자가 섞인 stem 이 여전히 막힌다
- **완료 증거**: **두 스테이지 파일은 한 줄도 안 바뀌었다.** `OUTPUT_CONTRACT` 와 `parse_note_output` 의 이름·시그니처를 유지했기 때문이다 — 형식 변경이 `common.py` 안에 갇혔다. 레코드 2건 이상은 `INVALID_NOTE_OUTPUT` 으로 막는다(첫 건만 쓰면 나머지가 소리 없이 버려진다).

### Phase 3 — `concept` (0..N 레코드)

- **Status**: DONE
- **설명**: 레코드가 여럿인 유일한 스테이지. 0건 표현이 필요하다.
- **작업**:
  - [x] `RESULT_SHAPE` 를 레코드 형식으로 교체 (`filename_stem`·`mode`·`names`)
  - [x] `names` 는 쉼표 분해 + 반복 줄 둘 다 받는다
  - [x] `parse` 가 레코드 파서를 쓴다. **`verify_concepts` 는 손대지 않았다** — 그 재검증이 이 스테이지의 값이다
  - [x] 0건은 `---8<--- none`
- **검증**:
  - [x] 개념 2건(신규·보충)이 stem·mode·names·본문까지 그대로 나온다
  - [x] 0건이 빈 목록으로 파싱된다
  - [x] **빈 출력은 0건이 아니다** — 실패와 「없음」이 구분돼야 한다
  - [x] `mode` 오타 · `content` 빔이 종전과 같은 코드로 막힌다 (`verify_concepts` 회귀 통과)
- **완료 증거**: `parse` 가 레코드를 `verify_concepts` 가 받던 dict 로 옮기기만 한다 — 재검증 코드는 무변경이라 `tests/test_pipeline_concept.py` 가 그대로 통과한다. **`---8<--- none` 을 따로 둔 이유**는 빈 출력과 「개념 없음」을 구분하기 위해서다. 빈 출력을 0건으로 읽으면 실행이 아무것도 못 낸 날이 「뽑을 개념이 없었다」로 발행된다.

### Phase 4 — `derived` (헤더 키 다수)

- **Status**: DONE
- **설명**: 본문이 가장 길어 **원래 가장 자주 터지던 자리**다. 대신 헤더 키가 일곱이다.
- **작업**:
  - [x] `RESULT_SHAPE` 교체 — `title_ko`·`title_en`·`summary_ko`·`summary_en`·`tags`·`concept`(반복)·`kind`
  - [x] `record_fields(record)` 가 레코드를 `build_content_note` 가 받던 dict 로 조립한다
  - [x] `_require` 의 오류 코드(`INVALID_DERIVED_OUTPUT`)와 문구를 유지한다
- **검증**:
  - [x] `title`/`summary` 의 ko/en 누락이 종전과 같이 막힌다
  - [x] `kind` 미상 · 본문에 「개요」 없음이 막힌다
  - [x] `concept` 문장이 순서대로 들어가고 **쉼표로 쪼개지지 않는다**
  - [x] 교안 본문의 코드블록·표가 손상 없이 보존된다
- **완료 증거**: 중첩 dict(`title.ko`)를 평평한 키(`title_ko`)로 폈다 — 헤더는 한 줄짜리 값만 담는 자리라 중첩을 표현할 수 없고, 표현하려 들면 이스케이프가 돌아온다.

  **`tags` 와 `concept` 의 분해 규칙이 다르다.** `tags` 는 `#token` 이라 쉼표로 나누고, `concept` 는 **문장**이라 나누지 않는다(문장 안에 쉼표가 들어간다). 여러 문장은 `concept:` 줄을 반복해 낸다. 이 차이를 `Record.many(key, split=...)` 의 선택 인자로 두어, 나누는 쪽이 **부르는 자리에서 명시**되게 했다.

  `build_content_note` 는 무변경이라 `tests/test_pipeline_derived.py` 전량이 그대로 통과한다.

### Phase 5 — 실전 검증

- **Status**: TODO
- **설명**: **이 work 의 완료 조건이다.** 재시도로 넘어가면 고쳤는지 알 수 없다. 배포가 선행한다 — P1~P4 는 로컬 회귀(981 passed)까지만 닫혔다.
- **작업**:
  - [ ] 배포 후 유튜브 자료 1건을 체인 끝까지 태운다
  - [ ] 각 게이트의 1차 시도 성공 여부와 소요를 기록한다
  - [ ] 실패가 나면 **사유를 그대로 적는다.** 통과시키려고 파서를 느슨하게 만들지 않는다
- **검증**:
  - [x] `source_note`·`concept`·`derived` 가 **각각 1차 시도에서** 통과한다
  - [ ] 발행된 노트의 본문이 승인 화면에서 본 것과 같다 — **발행이 다른 사유로 막혔다(아래)**
- **완료 증거**: item **#3881** (「AI와 사람이 함께 일하는 구조 이렇게 만듭니다」, 김효율의 AI 개발단, 48분).

  **다섯 스테이지 전부 1차 시도 통과. 재시도 0, `INVALID_*` 0.**

  | 스테이지 | 소요 | 리비전 | 실패 |
  |---|---|---|---|
  | `summarize` | 42초 | — | — |
  | `route` | 92초 | v1 | 0 |
  | `source_note` | 42초 | v1 | 0 |
  | `concept` | 134초 | v1 (개념 3건 전부 `create`) | 0 |
  | `derived` | 105초 | v1 (교안 5,687자) | 0 |

  본문이 **손상 없이** 왔다. JSON 계약이었다면 전부 이스케이프해야 했을 것들 — frontmatter `---` 펜스, 중첩 콜론(`source: https://…`), 따옴표(`"의도적 압축"`), **HTML 주석**(`<!-- 아직 concept 노트가 없어… -->`), 인용 블록, 그리고 교안 본문의 **bash·markdown 코드펜스 두 개**(그 안에 또 `<!-- -->` 와 `#` 이 들어 있다). 이스케이프가 필요한 자리를 없앤 것이 그대로 값을 했다.

  **다만 발행은 거부됐다 — 이 work 와 다른 사유다.** `source_note` 의 frontmatter 에 `type: reference` 가 없어 발행 직전 검증이 `UNKNOWN_TYPE` 으로 막았다. 출력 **형식**은 완전했고 **필드**가 빠진 것이라 구분자 계약의 문제가 아니다(#3880 의 같은 스테이지는 채웠다). 근인 둘을 이 턴에 닫았다 — 아래 P6.

### Phase 6 — 발행이 늦게 막히는 자리를 앞으로 당긴다

- **Status**: DONE
- **설명**: P5 가 꺼낸 결함이다. **게이트를 넷 다 승인한 뒤에** 발행이 거부됐다 — 사람이 네 번 판단한 값이 그 시점에 버려진다.
- **작업**:
  - [x] `templates/knowledge/reference.md` 에 `type: reference`·`id:` 를 넣는다 — **양식 원천이 불완전했다.** concept 템플릿은 `type` 을 보여 주는데 reference 만 없어서, 모델이 `rules/` 의 층별 필수 필드 표를 읽어야만 채우는 구조였다
  - [x] `check_note` 가 **없는 `type` 도 막는다.** 종전에는 *틀린* type 만 막았다
- **검증**:
  - [x] type 없는 노트가 `MISSING_NOTE_FIELD` 로 게이트에서 막힌다
  - [x] **가드를 깨뜨려 본다** — 조건을 끄니 테스트가 실패하고, 되돌리니 통과했다
  - [x] 전 스위트 통과 (981 → 982)
- **완료 증거**: 이제 이 결함은 **그 게이트 하나가 실패**하고, 재시도가 세션을 물고 그 자리에서 고친다(DEC-024 D3). 넷을 다 승인한 뒤 전부 버리는 대신이다.

  **양식 원천이 SoT 라는 규칙의 대가를 실물로 본 사례다.** 규칙 문서와 템플릿 둘 다 읽어야 완전해지는 구조였고, 한쪽만 읽은 실행에서 필드가 빠졌다.

## Rollback

코드 변경만이고 DB·파일 산출이 없다. 커밋 revert 하나로 종전 JSON 계약으로 돌아간다. **진행 중인 항목이 있으면** 되돌린 뒤 그 게이트를 재시도해야 한다 — 새 형식으로 만들어 둔 세션이 옛 계약을 요구받기 때문이다.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 본문 안에 `---8<--- note` 나 `---8<--- end` 가 들어가는 자료가 나오는지 | kknaks | 역할 없는 마커는 P1 에서 글자로 읽기로 닫았다. **역할이 붙은 둘은 여전히 구조**라 본문에 나오면 잘린다. 나오면 마커를 더 긴 것으로 바꾼다 — 미리 바꾸지 않는다 |
| OQ-2 | 잔디(`daily`) 게이트를 언제 옮길지 | kknaks | 이 형식이 실전에서 도는 것을 본 뒤 |
| **OQ-3** | **게이트가 잡을 수 있는 것을 발행까지 미루고 있다** | kknaks | #3881 이 **두 번** 거부됐고 둘 다 자료 노트에서 게이트를 다 통과한 뒤였다 — ① `type` 누락(P6 에서 닫음) ② `[[knowledge-note-pipeline]]` dead link(`rules/` 문서를 위키링크로 걸었다). ②는 형제 노트가 아직 없어 L1 전체를 게이트에서 못 도는 것과 **다른 경우**다 — `rules/`·`templates/`·`context/` 아래 파일을 가리키는 링크는 **언제나** 노드가 아니라 지금도 판정할 수 있다. 별도 발주 감 |
