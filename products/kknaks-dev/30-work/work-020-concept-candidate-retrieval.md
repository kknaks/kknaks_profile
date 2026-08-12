---
type: work
id: KDEV-WORK-020
title: "개념 후보 좁히기 — alias seed + 그래프 1홉"
status: todo
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: —
progress: 0
created_at: 2026-08-12
updated_at: 2026-08-12
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-007-update-lines-by-case|KDEV-BL-007]]"
  decisions:
    - "[[decision-023-concept-candidate-retrieval|KDEV-DEC-023]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# 개념 후보 좁히기 — alias seed + 그래프 1홉

`concept` 게이트가 개념 전량(363건 · 32k 토큰)을 프롬프트에 싣는 것을 멈추고, alias 사전으로 찾은 seed 와 그 1홉 이웃만 넘긴다.

**만들지 않는 것**: 임베딩 검색, 그래프의 화면 노출, 개념 병합·정리.

## Meta

- Baseline: [[baseline-007-update-lines-by-case|KDEV-BL-007]]
- Covers spec: [[spec-008-gate-chain|KDEV-SPEC-008]] (concept 게이트 입력 계약)
- Depends on work: 없음
- Parallel work: 없음
- Follow-up work: 좁히기가 부족하면 임베딩(DEC-023 옵션 C) — 지금은 열지 않는다
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker |  |
| Next | P1 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | done |
| Design | — | 화면 없음 | — |
| FE | — | 프론트 변경 없음 | — |
| BE | kknaks | 인덱스·좁히기·스테이지 배선 | todo |
| QA | kknaks | 좁힘 비율 실측과 회귀 | todo |
| Ops | — | 배포 절차 변경 없음 | — |

## Scope

포함:

- `ConceptIndex` 에 **이웃**을 싣는다 (`up:` + 본문 `[[]]`)
- 텍스트 하나에서 **seed** 를 결정적으로 뽑는다 (alias 정확 매칭)
- 1홉 확장 + 폴백 규칙(seed 0 → 전량, 60% 초과 → 전량)
- `concept`·`daily` 두 스테이지 배선
- `path` 필드 제거 (DEC-023 D5)

제외:

- 임베딩·벡터 저장 (DEC-023 옵션 C, 보류)
- `_graph` 를 HTTP 로 내보내기 — 사람이 보는 시각화는 다른 일이다
- seed 를 수집 원문까지 넓히는 것 (DEC-023 OQ-1 — 요약으로 시작한다)

## Code Surface

- Repo / module: `app/back` (백엔드 전용)

| 경로 후보 | 설명 |
|---|---|
| `service/pipeline/concept_index.py` | **주 변경.** 이웃 저장 · seed 추출 · 좁히기 · `path` 제거 |
| `service/pipeline/stages/concept.py` | `existing_concepts` 를 좁힌 것으로 (281·293행) |
| `service/pipeline/stages/daily.py` | 〃 (459행). seed 는 커밋 조사 결과에서 |
| `core/wikilinks.py` | `extract_wikilinks` 재사용 — 본문 `[[]]` 파싱 |
| `core/graph.py` | `build_alias_index`·`_resolve` 의 별칭 해석 규약 참고 |
| `tests/test_concept_index.py` | 기존 테스트 + 좁히기 케이스 |

- Domain / schema note: **DB 변경 없음.** 인덱스는 요청 시 파일에서 만든다(지금과 같다).

## Domain / Schema

해당 없음 — 저장하는 것이 없다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| `stages/concept.py` | `ConceptIndex.narrowed_payload(seed_text)` | 프롬프트에 실을 개념 목록 |
| `stages/daily.py` | 〃 | 잔디도 같은 함수를 쓴다 (DEC-023 D6) |

## Internal Interface Contract

```python
# 이웃 — 별칭 해석까지 끝난 stem 집합
ConceptIndex.neighbors(stem: str) -> set[str]

# seed — 텍스트에서 정확 매칭으로 찾은 개념 stem 들
ConceptIndex.seeds(text: str) -> set[str]

# 좁힌 목록 — 폴백 규칙을 여기서 적용한다
ConceptIndex.narrowed_payload(text: str) -> tuple[list[dict], dict]
#   반환 둘째는 왜 그렇게 됐는지: {"mode": "narrowed"|"all", "seeds": n, "picked": n, "total": n}
```

**둘째 반환값이 있는 이유**: 좁히기는 조용히 실패하면 알 방법이 없다. seed 0 으로 매번 전량이 나가고 있어도 응답은 똑같다 — 그래서 판단 근거를 로그와 준비 payload 에 남긴다.

## Execution

### Phase 1 — 인덱스에 이웃을 싣는다

- **Status**: TODO
- **설명**: 좁히기의 재료를 만든다. `build_index` 가 이미 `frontmatter.load` 로 파일을 여니 **본문도 이미 손에 있다** — 지금은 버리고 있을 뿐이라 추가 I/O 가 없다.
- **작업**:
  - [ ] `ConceptEntry` 에 `up: tuple[str, ...]` 과 `links: tuple[str, ...]`(본문 `[[]]`) 추가
  - [ ] `build_index` 에서 `post.content` 를 `extract_wikilinks` 로 파싱해 채운다
  - [ ] `ConceptIndex.neighbors(stem)` — `up` + `links` 를 **별칭 해석 후** stem 으로 정규화, 양방향(들어오는 링크도 이웃이다)
  - [ ] `as_prompt_payload` 에서 `path` 제거 (DEC-023 D5)
- **검증**:
  - [ ] `path` 제거로 payload 문자 수가 줄어든 것을 측정해 기록
  - [ ] `neighbors` 가 별칭으로 걸린 링크도 stem 으로 돌려주는지 (`[[STT]]` → `speech-to-text`)
  - [ ] 없는 대상(dead link)은 이웃에 안 들어가는지
  - [ ] 기존 테스트 전부 통과 — `match`·`match_any` 계약은 안 바뀐다
- **완료 증거**: 미작성

### Phase 2 — seed 추출

- **Status**: TODO
- **설명**: 텍스트에서 진입점을 찾는다. **AI 에 맡기지 않는다** — 이름이 사전에 있느냐는 사실 판단이다.
- **작업**:
  - [ ] `ConceptIndex.seeds(text)` — 등록된 이름·별칭이 텍스트에 나타나는지 본다
  - [ ] 정규화는 기존 `normalize` 를 쓴다(공백·하이픈·밑줄만). **부분 일치를 넣지 않는다**
  - [ ] 짧은 별칭의 오탐을 막는다 — 한 글자·두 글자 별칭이 우연히 걸리는 경우
- **검증**:
  - [ ] 자료 하나(요약문)를 넣어 seed 가 사람이 보기에 맞는지 육안 확인 3건
  - [ ] 오탐 케이스 테스트 — 짧은 별칭이 다른 단어 안에서 걸리지 않는다
  - [ ] seed 가 0인 텍스트(무관한 문장)에서 빈 집합
- **완료 증거**: 미작성

### Phase 3 — 좁히기와 폴백

- **Status**: TODO
- **설명**: 1홉 확장과 「의심스러우면 안 자른다」 규칙. **DEC-023 D2·D3·D4 가 여기서 코드가 된다.**
- **작업**:
  - [ ] `narrowed_payload(text)` — seed → 1홉 → payload
  - [ ] seed 0 이면 전량 (D3)
  - [ ] 결과가 전량의 60% 초과면 전량 (D4)
  - [ ] 두 폴백이 발동하면 `mode: "all"` 과 사유를 남긴다
  - [ ] **홉은 1 고정.** 파라미터로 열지 않는다 — 2홉은 99% 라 열어 두면 언젠가 켜진다
- **검증**:
  - [ ] seed 5건 → 결과가 전량보다 유의하게 작다
  - [ ] seed 0 → 전량, `mode == "all"`
  - [ ] 60% 경계 양쪽 테스트
  - [ ] 좁힌 목록에 **seed 자신이 반드시 들어간다**
- **완료 증거**: 미작성

### Phase 4 — 스테이지 배선

- **Status**: TODO
- **설명**: 두 스테이지가 같은 함수를 쓴다. 한쪽만 바꾸면 규칙이 두 벌이 되고 잔디만 계속 전량을 받는다(DEC-023 D6).
- **작업**:
  - [ ] `stages/concept.py` — seed 텍스트는 `summarize` 산출(요약·제목·태그)
  - [ ] `stages/daily.py` — seed 텍스트는 그날 커밋 조사 결과(레포별 정리·영역)
  - [ ] 두 곳의 준비 payload 에 좁히기 판단 근거를 싣는다 — 승인 화면이 「왜 이 개념들만 보였나」를 답할 수 있어야 한다
- **검증**:
  - [ ] 게이트 프롬프트 스냅샷 테스트 — 전량이 아니라 좁힌 목록이 실린다
  - [ ] 잔디 게이트도 같은 경로를 탄다
  - [ ] 전체 스위트 통과
- **완료 증거**: 미작성

### Phase 5 — 실측

- **Status**: TODO
- **설명**: 계획한 효과가 실제로 나는지 본다. **DEC-023 이 「363 → 110 안팎, 약 1/3」로 예측했고, 그 예측이 맞는지가 이 work 의 완료 조건이다.**
- **작업**:
  - [ ] 실제 자료 5건(유튜브·블로그·공부 노트 섞어)으로 seed 수·좁힌 수·토큰 수를 잰다
  - [ ] 결과를 이 문서 완료 증거에 표로 남긴다
  - [ ] 좁힘이 예측보다 나쁘면 **사유를 적는다.** 수치를 맞추려고 규칙을 비틀지 않는다
- **검증**:
  - [ ] 5건 중 seed 0 으로 떨어진 건수와 그 자료의 성격
  - [ ] 좁힌 목록에서 **빠졌지만 있어야 했던 개념**이 있는지 육안 확인 — 이것이 이 설계의 유일한 실패 모드다
- **완료 증거**: 미작성

## Rollback

코드 변경만이고 DB·파일 산출이 없다. `narrowed_payload` 를 `as_prompt_payload` 로 되돌리면 종전 동작이다 — 커밋 revert 하나로 끝난다.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 짧은 별칭(1~2자)의 오탐을 길이로 막을지 문맥으로 막을지 | kknaks | P2 에서 실제 별칭 분포를 보고 정한다 |
