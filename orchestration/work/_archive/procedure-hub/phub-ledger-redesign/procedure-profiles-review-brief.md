
# [reviewer_doc] procedure-profiles.json 1차 결과 독립 검토

너는 **procedure-hub `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 트리다. 원 작성 워커의 조사 턴은 종료됐다. 너는 독립 검토만 하며 추가 워커를 띄우지 않는다. 원장·기존 작업은 수정·삭제 금지.

## 실행 권한과 보고 프로토콜

사용자는 실제 작업을 워커에게 발주하도록 명시했다. 아래 §9는 저장소 고정 양식이다. 최신 라이브 dispatch preamble의 명령·인자·outcome 요구가 우선하며 worker_done는 정확히 한 번 보낸다. 필요한 --outcome succeeded/failed를 반드시 넣는다. 코디에게 장문 원문을 보내지 말고 실제 파일 경로와 요약만 전달한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/_RESUME.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 별도 개념 노트 해당 없음. 선행 온톨로지를 가정하지 않는다.

## 2. 검토 목적

별도 작성자가 만든 1차 조사 산출물을 원본과 스킬에 대조하는 독립 읽기 검토다. 기존 작성자의 통독·통과 주장과 분류를 전제하지 않는다. 메인에서는 verify.py 재실행 결과 failure_count=0을 확인했으나 의미 해석·미결 분류 승인과는 별개다.

## 3. 검토 계약

원장 하나의 1차 수집 범위를 검토한다. 임상 사실 검증·온톨로지 확정은 하지 않는다. 모든 17개 항목과 필드를 직접 읽고 누락·부적절한 추출·형태소 문제의 처리·본문 진술·미결 분류를 대조한다. 단순 토큰·정규식 결과를 전수 의미 조사로 포장했는지, A 오류를 표시만 하고 해결했다고 했는지, 원문 부족과 해석 과제를 혼동했는지, C 사용자 선택이 실제 필요한지 판단한다.

## 4. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/procedure-profiles-research-brief.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json`
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles` 안 산출물. review.md·issues.md·validation.md와 구조화 기록·build.py·verify.py를 필요에 맞게 대조한다.

## 5. allowed_paths

새 파일 `orchestration/work/phub-ledger-redesign/procedure-profiles-review-report.md` 하나만 생성한다. 나머지는 읽기 전용이다. _RESUME·조사 결과를 수정하지 않는다.

## 6. 검토 절차

1. 원본·스킬·산출물을 대조하고 기계 검증을 실행한다. 모든 원문 항목을 검토한다.
2. 각 지적은 위치·원문·문제·영향·필요 수정과 근거를 남긴다.
3. 사용자 결정 2건 각각 지금 필요한지, 에이전트 판단인지, 후속 보류 가능한지 검토한다. 다른 미결도 B로 보내기 전 에이전트 해석으로 해결할 수 있는지 구분한다.
4. PASS/WARN/FAIL 판정, 1차 범위 충족 여부, 남은 문제·사용자에게 보여줄 사항을 리포트로 작성한다. 미결을 억지로 닫지 않는다.
5. 짧은 요약·판정·리포트 경로만 코디에게 보고한다.

## 7. 제약

- 결과 수정·삭제, 다른 원장 조사, 추가 에이전트 실행, 외부 임상/법률 조사, 커밋·push·PR 금지.
- 1차 결과를 정규화 완료나 최종 의미 조사 완료라고 판정하지 않는다.
- 실행 전 원문을 읽었는지 입증할 수 없는 주장으로 검토를 대신하지 않는다.

## 8. 검증

`python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/verify.py` 및 원본 대비 읽기 검토. 자동 검증과 읽기 검토 판정을 분리한다. 기존 파일은 바꾸지 않는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --from 라이브-preamble의-워커-handle \
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
