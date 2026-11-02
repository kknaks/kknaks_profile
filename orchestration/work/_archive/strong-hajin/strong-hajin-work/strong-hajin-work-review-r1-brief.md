
# [reviewer] 업무 스펙 수정본 재검수 — V-1~8 및 WARN 해소 확인

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이번은 planner 리뷰다. 코드 워크트리에서 실행하되 실제 검수 대상은 아래 코디 문서 4건이다. 모두 read-only, 보고서 1개만 작성한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-write-brief.md` — 원 발주와 allowed_paths.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/source-issue-7.md` — 원문 계약. 우선순위·D4 제외·미결 유지·기존 요구 임의 후순위 금지 확인.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md`와 `templates/projects/` 해당 양식.
- 기대는 개념: 해당 없음. 명시된 계약과 실제 근거로 판정.

## 2. 배경 / 무엇을 바꾸나

1차 수정 재검수다. writer는 V-1~8 및 WARN 9건을 모두 해소했다고 보고했다. 같은 네 문서 v0.2.0을 실제 확인하고 이전 보고서에 재검수 절을 추가한다. 코디가 index/log 옛 ID를 갱신했다.

## 3. 계약

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-write-fix1-brief.md` 수정 지시를 확인한다.
- 기존 위반 해소 여부와 수정으로 새로 생긴 계약 모순을 본다. 양식 준수만으로 PASS 처리하지 않는다.
- OQ-A는 사용자에게 질문했고 아직 답변이 없다. 답이 없는 것을 결정으로 취급하지 않는다.
- D2는 복수 문의 해소·취소 규칙만 미결이며 문의 기능 전체를 미루지 않는다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`
- 코디 소유 README/index/log는 ID와 링크 정합만 확인.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-spec-report.md` 한 파일. 기존 리뷰는 보존하고 `재검수 (1차)` 절을 추가한다.

## 6. 구현 단계

1. V-1~8, WARN 9건별 PASS/잔여를 구체적 파일:줄로 작성한다. 원문과 코드 근거는 필요 부분을 다시 확인한다.
2. 새 API/문의/판정변경/목록 상태/AX 확인 표면 경계가 실제로 원문에 기반하는지, 불명확한 구현 선택을 확정으로 쓴 곳이 없는지 본다.
3. OQ-A 기본값 '취소만'이 원문과 실제 표 의미로 뒷받침되는지, D2가 회사 결정 대기로 잘못 묶였는지 확인한다. 개인 프로젝트이므로 결정 주체는 현재 사용자다. 원문의 미결 상태는 출처 사실이지 회사 승인을 기다릴 이유가 아니다.
4. PLAN-005 위임전결 값의 조사 여부/구체적 잔여를 확인한다. 미조사와 실제 값 부재를 구분하고, 이를 W1까지 막는 게이트로 쓰지 않는다.
5. W1 생성·즉시 배정·회의 후속 승격의 WP는 OQ-A/D2와 독립해서 작성 가능한지 판정하고, 다음 WP가 안전하게 다룰 범위와 미결 영향 단계를 명시한다.

## 7. 범위 제약

문서/코드 수정·커밋·push·PR·DB 작업 금지. 범위 밖 기존 부채로 FAIL 주지 않는다. 새 제품 결정을 만들지 않는다.

## 8. 검증

planner 리뷰. 역할문서의 scripts/lint-pipeline.py는 이 레포에 없으므로 실행 불가를 명시하고 현재 project.md 및 양식 대조로 검증한다. 코드 테스트는 실행하지 않는다. 최종 PASS/WARN/FAIL과 OQ 분류, 못 확인한 것은 그대로 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_22586d00-1fe8-4a69-9b8f-83f5b9d8dfb1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
