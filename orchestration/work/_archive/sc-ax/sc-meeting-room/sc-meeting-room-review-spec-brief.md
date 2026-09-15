# [reviewer_spec] SPEC-004 v0.5.0 개정 리뷰

너는 **sc-ax `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/reviewer/role.md`
  (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec`

## 1. 무엇을 리뷰하나

`git status` 의 변경 3건 + 미추적 1건이 대상이다:

```
M products/sc-ax/20-spec/spec-004-meeting-note.md   ← 본체 (v0.4.11 → v0.5.0)
M products/sc-ax/20-spec.md                          ← 제공범위 요약
M products/sc-ax/log.md
?? products/sc-ax/00-baseline/_working/meeting-two-copies-investigation.md   ← 근거 조사
```

**너는 read-only 다.** 문서를 고치지 마라. 산출물은 리뷰 리포트 **한 장**뿐이다.

## 2. 사용자 결정 — 이 기준으로 판정해라

> 회의에 최소 2명 — 사람 / AI. **둘 다 각자 회의록을 적는다.** 통합본 때 최종 판정.
> **두 명이 써야 정확도가 높아진다.**
> 이어서: **「일단 AI 가 최종을 만들라고. 그다음에 논의해보자」**

코디가 준 결정 다섯(개정 브리프 `sc-meeting-room-spec-2-brief.md` §1):

| # | |
|---|---|
| D-1 | 뼈대도 두 벌 — `agendas` 에 벌 축. 사람·AI 가 **각자 자기 안건 목록** |
| D-2 | **최종본은 AI 가 짓는다.** 사람이 고르거나 판정하지 않는다 (다만 **고칠 수는 있다** — 그 경계가 적혀야 한다) |
| D-3 | **충돌 판정은 범위 밖.** `OQ-308` 을 열어 둔다 |
| D-4 | 원본 두 벌은 최종본 뒤에도 남는다 |
| D-5 | 「안건 1. 안건 1」은 별건. 한 줄로만 |

## 3. 특히 볼 것

1. **D-2 의 경계가 분명한가** — 「AI 가 짓는다」와 「사람이 고칠 수 있다」가 어디서 갈리는지.
   모호하면 구현이 갈린다
2. **뒤집은 결정이 제대로 기록됐나** — 원래 `D1`·`D42` 가 「뼈대 한 벌 · 판정 없음」이었다.
   신설 `§0.1` 이 그것을 지우지 않고 **왜 뒤집었는지**까지 남겼는가
3. **범위가 안 샜나** — `D-3` 을 어기고 충돌 판정·`merge_conflicts` 가 들어오지 않았는지
4. **세 벌 사이의 규칙이 빠짐없나** — 누가 어느 벌에 쓰나 · 벌 사이를 참조할 수 있나 ·
   한쪽이 비면 어떻게 되나 · 계보(`merged_from`·`from_lines`)를 언제 남기나
5. **미결 처리가 정직한가** — `OQ-312` 를 「종결」했다는데 정말 닫혔나, 아니면 `OQ-318` 로
   이름만 옮긴 것인가. 새 미결 셋(`OQ-318`·`319`·`320`)이 **결정을 미룬 것인지 진짜 미결인지**
6. **문서 간 정합** — 본체 · `20-spec.md` 요약 · `log.md` 가 서로 어긋나지 않는가.
   기획 정본(`PLAN-004`)과 부딪히는 자리가 있으면 그것
7. **구현 가능한가** — 조사 문서가 짚은 코드 현실(`replace_track` 결합 · `application.py:778` 필터 ·
   배치 출력 스키마)과 개정본이 맞물리는가. **코드는 읽기만 해라**
   (`/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room` — read-only)

## 4. 판정

각 지적에 **파일:줄 + 근거**를 달아라. 근거 없는 지적은 쓰지 마라.

- **FAIL** — 이대로 구현하면 사용자 결정과 다른 것이 나온다
- **WARN** — 구현자가 물어야 할 만큼 모호하다
- **PASS**

## 5. 검증

```
python3 scripts/lint-pipeline.py --strict
```

→ `products/sc-ax/` 범위 ERROR 0 확인. 타 제품 기존 WARN/ERROR 는 「무관」으로 분리 보고.
**리뷰는 read-only — 문서를 고치지 않는다.**

## 6. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/review-spec-004-v050-report.md`

구성: 판정(PASS/WARN/FAIL) · 지적 목록(파일:줄 + 근거 + 무엇이 문제인가) ·
**구현자가 물을 수밖에 없는 자리** · lint 결과

## 7. 보고

- 판정과 지적 건수(FAIL/WARN 별)
- **가장 위험한 지적 하나**와 그 이유
- `OQ-312` 가 정말 닫혔는지에 대한 네 판정
- lint 결과
