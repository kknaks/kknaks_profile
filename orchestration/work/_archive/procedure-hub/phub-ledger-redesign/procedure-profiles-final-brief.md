# 최종 기록 보완 — 재검토 W1·W2만

이번 발주는 아래 최초 보정 브리프보다 이 절이 우선한다. 조사 범위를 확대하거나 다음 원장을 시작하지 않는다.

`procedure-profiles-rereview-report.md`의 W1·W2와 종료 조건을 읽는다. 재검토는 F1~F7 반영과 기계 검증을 확인했고, W1 두 출현을 표시 또는 알려진 범위 밖 사례로 기록하면 1차 수집 범위를 종료할 수 있다고 판정했다.

허용 작업은 다음에 한정한다.
1. issues.md A1에 W1 두 출현을 **범위 밖 알려진 오분절**로 정확히 기록한다. `/profiles/13/aftercare/0` 발적 [6,8), `/profiles/2/practicalNotes/2` 수화 [66,68). 원시 토큰·문맥·원문 구간을 직접 확인해 적고 후속 거짓 부위/용어 후보 위험을 명시한다. 지금 분석 토큰이나 JSON을 재생성하지 않는다. 이 경로는 재검토자가 허용한 W1(b)다.
2. validation.md와 review.md에 위 두 사례 기록 위치를 연결하고, 원시 형태소 출력에 알려진 오류가 남고 지정 품사·서명 밖 정확성을 보장하지 않는다는 한계를 명확히 한다. W2 근거 토큰 46건은 verify가 미판정 토큰을 correct로 간주하는 구현이라는 점, 재검토자가 46건을 문맥 대조한 결과 현재 추가 오태깅은 없었다는 보고를 구분한다.
3. verify.py를 재실행하고 원본 해시 불변을 확인한다. 신규 `procedure-profiles-final-note.md`에 W1(b)·W2 처리의 실제 경로·구간·검증 명령·결과를 짧게 기록한다.
4. _RESUME의 현재 상태·다음·발주·산출물·이력을 갱신한다. 1차 수집 범위의 조건부 종료 요건을 기록으로 충족했으며 코디 확인 전이라는 상태로 둔다. 원장 전체 미완료(B10묶음·잠정2·보류2·후속9), 의미 조사·정규화 미실행을 유지한다. 전 C1·C2는 사용자 결정이 아니라 후속 보류다. 재검토 판정이 WARN이었다는 사실은 지우지 않는다.

수정 허용 파일: first-pass/procedure-profiles/issues.md, validation.md, review.md, _RESUME.md. 신규 최종 메모 한 개. JSON·코드·스킬·기존 리포트·원본·이전 폴더는 수정 금지. 추가 워커 금지. 원장 전체 완료 또는 모든 토큰 정확성 보장이라고 쓰지 않는다. 결과는 최종 메모 경로와 짧은 요약만 보고한다. 라이브 preamble ID로 정확히 한 번 완료 보고한다.

---

# 후속 발주 — procedure-profiles 1차 결과 보정

이 문서가 이번 발주의 계약이다. 아래 최초 브리프는 배경이며 서로 다르면 이 후속 절이 우선한다. 새 원장을 조사하지 않는다.

먼저 `orchestration/work/phub-ledger-redesign/procedure-profiles-review-report.md` 전체를 읽고 F1~F7을 원본과 대조하라. 현재 너에게 발주된 task/dispatch는 라이브 preamble 기준이다. 이전 ID로 보고하지 않는다.

## 보정 범위

1. F1: 의미를 바꾸는 오태깅의 출현을 모든 값에서 다시 확인하고 미표시 출현을 추가한다. 원시 Kiwi 토큰은 유지한다. 규칙이 한번 이상 쓰였다는 검사에 더해, 확인된 문제 토큰의 출현과 검토 표시가 대응하는지 검증한다.
2. F2: 오태깅으로 만들어진 표현 후보에 출현별 오탐·근거 표시를 붙인다. 단어 자체의 다른 문맥까지 일괄 오탐 처리하지 않는다. 원래 후보는 보존한다. 파생 후보 판정의 연결과 검증 근거를 남긴다.
3. F3: 표시한 오류와 교정한 분석을 혼동하지 않게 상태를 정리한다. 행위·대상 구절의 후속 분해는 후속 목록으로 명확히 남기고 1차 수집 전체에서 의미가 없거나 해결됐다고 하지 않는다.
4. F4: phaseOrder 반대 근거를 추가하고 일관된 방향을 추정하지 않는다.
5. F5~F7: B·C를 원문과 스킬 기준으로 재분류한다. 잠정 해석은 잠정으로 남기고 임상 사실을 추가하지 않는다. 현재 사용자 결정이 불필요한 이유와 처리 단계·영향을 기록한다. 사용자 결정을 받은 것으로 표시하지 않는다.
6. 검토 보고서에도 집계 혼선이 있다: B10은 모호한 1건이 남는다고 하면서 마지막에는 B 8묶음이라 했다. 항목별 현재 상태를 실제로 대조해 열린 묶음 수를 새로 계산하라. 리뷰어 수치를 그대로 복사하지 않는다. review.md의 scalar string 필드 수 표기도 실제 키·자료형과 다시 대조한다.
7. build/verify와 원문 해시 검증을 수행하고 문서·구조화 결과·집계를 일치시킨다. 재개 노트에는 보정과 재검토 대기 상태만 기록한다. 독립 재검토가 아직 없으면 그 사실을 명시한다.

허용 수정: 기존 `first-pass/procedure-profiles/`의 이번 작업 산출물 보정, `_RESUME.md` 상태·산출물·이력. 원본·이전 작업 폴더·reference·스킬·검토 보고서는 수정 금지. 신규 `procedure-profiles-correction-report.md`에 지적별 처리·검증·남은 문제를 간결히 기록한다. 결과 파일은 필요한 보정만 하고 삭제하지 않는다. 코디는 이번 보정에 필요한 기존 신규 산출물 수정을 허용했다.

추가 워커 실행 금지. 완료 보고는 3문장 요약과 보정 리포트 경로만 보낸다. 열린 미결과 후속 의미 조사가 남으므로 원장 완료라고 하지 않는다.

---


# [researcher] procedure-profiles.json 전체 1차 조사

너는 **procedure-hub `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 트리다. 이번 조사 워커는 너 한 명이며 추가 워커를 띄우지 않는다. 원장·기존 작업은 수정·삭제 금지.

## 실행 권한과 보고 프로토콜

사용자는 실제 작업을 워커에게 발주하도록 명시했다. 아래 §9는 저장소 고정 양식이다. 최신 라이브 dispatch preamble의 명령·인자·outcome 요구가 우선하며 worker_done는 정확히 한 번 보낸다. 필요한 --outcome succeeded/failed를 반드시 넣는다. 코디에게 장문 원문을 보내지 말고 실제 파일 경로와 요약만 전달한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/_RESUME.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 별도 개념 노트 해당 없음. 선행 온톨로지를 가정하지 않는다.

## 2. 배경 / 무엇을 바꾸나

사용자는 21개 원장을 하나씩 전수 조사하기로 했고 procedure-profiles.json을 첫 원장으로 승인했다. 1차는 구조·전체 값·원문 문맥·형태소·복합 표현 수집이다. 공통 개념·의미 관계·실버 변환을 확정하는 단계가 아니다. 메인 문맥을 줄이기 위해 실제 조사·작성은 반드시 워커가 수행한다.

너는 앞선 세션의 맥락이 없다. 이전 조사·완료·검증 주장을 사용하지 말고 지정 원본과 스킬을 기준으로 새로 조사한다. 코디가 원문을 읽고 Kiwi 설치 가능성을 확인했지만 조사 결과는 아직 생성하지 않았다. 환경 확인: uv run --python 3.12 --with kiwipiepy==0.24.1 사용 가능, kiwipiepy_model 0.24.0. 모델 cong는 동작, sbg는 패키지에서 파일 누락으로 실패했다. 이는 도구 인계 정보이며 조사 근거가 아니다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

원문 대응과 잠정 의미 관찰을 분리한다. 결과는 first-pass/procedure-profiles/ 안 review.md, source-map.json, morphology.json, expressions.json, issues.md, validation.md에 저장한다. 재현용 스크립트·추가 구조화 기록이 필요하면 같은 결과 폴더 안에만 만든다. 원문 전체 읽기는 토큰 추출·횟수·필드 목록으로 대체할 수 없다. 형용사·부사·조건·부정·가능성 문구를 누락하지 않는다. 자동 처리와 직접 원문 대조 범위를 정확히 보고한다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/AGENTS.md` — 레포 인덱스
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze/phub-ledger/README.md` — 원장 작성 규칙(원문 수정 허가 아님)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json` — 유일한 조사 데이터. 다른 원장을 열지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/` 새 조사 결과
- `orchestration/work/phub-ledger-redesign/_RESUME.md` 현재 상태·산출물·이력 갱신만. 사용자 결정과 이전 이력은 보존

researcher 기본 역할의 단일 리포트 제약 대신 이번 사용자 요청에 따라 위 파일들을 허용한다. 그 밖의 경로는 읽기만 한다.

## 6. 구현 단계

1. 스킬과 재개 노트를 읽고 출력 경로를 확인한다. 없는 결과 디렉토리만 생성한다.
2. 파일 해시·전체 구조·전체 값을 기록하고, 모든 17개 항목 내부를 문맥과 함께 읽는다.
3. 전체 텍스트 형태소 분석과 출현별 원문 구간·복합 표현 수집을 수행한다. 전문어·기호 오분절은 원문과 대조한다.
4. 누락·중복·포인터·구간·해시 검증, 별도 읽기 검토, 미결 분류를 수행한다. 미결은 묶어서 영향과 후속 단계를 기록한다.
5. 원장 전체 완료·정규화 완료로 과장하지 말고 단계별 상태를 남긴다. 재개 노트를 갱신하고 3문장 요약과 실제 경로를 보고한다.

## 7. 범위 제약 — 하지 말 것

- 원본·기존 phub-recommend·reference·다른 원장·전역 설정 수정·삭제 금지. 복구·Git reset/clean/checkout·커밋·push·PR 금지.
- 기존 파일 덮어쓰기·삭제 필요 시 먼저 정확한 경로와 영향을 코디에게 질문한다. 이번 신규 결과의 작업 중 수정은 허용한다.
- 원문의 임상·법적 주장을 사실 승인하거나 외부 정보로 보충하지 않는다. 불확실한 단위·척도·대상은 추측하지 않는다.
- 추가 워커·서브에이전트 실행 금지. 사용자 결정을 혼자 확정하지 않는다.

## 8. 검증

```
원장 해시 시작/끝 비교; 전체 경로·자료형·값 양방향 대조; 중복 키 감지; Pointer 해소; 모든 구간 원문 slice 대조; 형태소 적용/제외 대응; 17개 전항목 원문 재독 및 문맥/표현 손실 검토; 실제 수행 명령·결과를 validation.md에 기록
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --from term_8c2999f2-0bca-4945-9d09-c5212852bdaa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
