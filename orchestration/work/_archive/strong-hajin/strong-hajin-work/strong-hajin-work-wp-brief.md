
# [writer] W1 구현 계획 작성 — 문서 WARN 정리 후 WORK-001

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-spec-report.md` 재검수 1차: 기존 위반 해소, 새 WARN R-1~6, W1 독립 WP 가능 판정.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` W1 생성·즉시 배정·회의 후속 승격 관련 절.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md` 신규 생성의 수행자 수락 제거·AX 실행 확인 보존 관련 절.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/templates/projects/30-work/work.md`, `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md`.
- 원 발주·수정 브리프·source-issue-7.md. 기대는 개념: 기존 권한/멱등성/원자성 계약을 보존한다.

## 2. 배경 / 무엇을 바꾸나

리뷰어가 W1 WP는 미결 없이 작성 가능하다고 판정했다. 코디는 WARN으로 W1 계획 작성을 진행한다. 이번에는 R-1~6 문서 정정 후 **WORK-001 업무 생성·타인 즉시 배정** 계획을 작성한다. 코드는 구현하지 않는다. OQ-A 답변은 아직 없다.

## 3. 계약

- W1 계약은 v0.2.0 검수본을 유지한다. W2·문의 정책 미결을 W1 착수 게이트로 끌어오지 않는다.
- 단계 A: R-1~6 정정. D2/N값의 결정 주체는 현재 사용자. 위임전결 값은 PLAN-005에도 없음(리뷰어 고정본 496줄 직접 검증), 값이 정해지기 전에는 추천 없이 사람이 고른다는 계약 유지. 상세의 open→done 전이 추가(행의 시작 버튼과 구분). reply 복수 규칙은 권고/미확정 명시. 기록 추가 API의 누락을 원문 생성·조회 계약에 맞게 보완(현행 구현은 GET뿐, 신규임을 표시). 답변 오류 SoT는 SPEC-002 한 곳. W1 계약이 달라져야 하는 사실을 찾으면 WP를 멈추고 알려라.
- 단계 B: A 자체점검 후 WORK-001 작성. W1 본인 생성/일반 구성원 타인 생성/관리자 배정/회의 후속 생성, 신규 수락용 ActionItem·pending/round 제거, REST·MCP·AX·seed·FE·권한·도메인·영속 표면을 한 slice로 닫는다. AX 사용자 실행 확인과 완료 승인 체계는 유지.
- 신규 요청 권한과 기존 업무 재배정 권한 분리. 일반 구성원에게 관리자 task.assign을 부여하는 우회 금지. 요청자/담당자/행위자/출처/시각과 근거 보존.
- 멱등 키와 payload 충돌·동시 실행·동일 회의 후보 재승격·활성 담당 하나·권한 밖 대상·조직 범위·재시도 영수증 테스트를 설계한다. 기존 AX 키 재조회가 REST 멱등성을 보장하지 않는다는 조사 결과 반영.
- 기존 데이터 전환/호환은 D4 제외. DB reset/실제 데이터 삭제 요구 금지. 새 모델 스키마와 테스트 fixture 검증만 계획한다.
- 승인자 선택의 수동 경로는 기존 확정 계약을 적용. 자동 추천 값 부재를 생성 차단 이유로 쓰지 않는다.
- W2 완료 상태 전환·문의·반복·수신함 본체는 WORK-001 제외(제품 차수 제외가 아니라 다음 실행 단위). 미결과 무관한 W1이 먼저 동작하도록 최소 호환 경계와 후속 소비 계약을 기술한다. #7 전체가 완료됐다고 표시하지 않는다.

## 4. 먼저 읽을 핵심 파일

- BASE-001의 현행 코드 관측·표면 목록. 작업 코드: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`, branch `kknaksss/strong-hajin-work`, base `origin/main`.
- 실제 frontend/backend의 생성/배정/요청/후속승격/판단/권한 경로를 읽고 후보 파일을 열거한다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/config/projects/strong-hajin.json`을 워커에게 읽히지 않는 규칙에 따라 필요한 검증을 여기 제공: BE는 `cd backend && uv run pytest -n auto --dist worksteal`, FE는 `cd frontend && npx tsc --noEmit && npx vitest run && npx vite build`. 이는 **계획에 적을 검증**이며 이번 문서 워커는 실행하지 않는다. 실제 구현 때 DB·환경 격리를 명시하고 integration 요구는 실행 환경 확인을 거쳐야 한다.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`

index/log·코드·리뷰 보고서 수정 금지. SPEC에서 WORK 역참조 금지.

## 6. 구현 단계

1. R-1~6만 정정하고 문서 교차 일관성 자체점검. 필요한 신규 API는 목표 계약임을 표시한다. 모든 정정은 완료 보고에 근거와 함께 나열.
2. W1 WP를 templates/projects/30-work/work.md에서 작성: frontmatter WORK-001/status todo/progress 0, phase 전부 TODO. 코드 작성 완료인 것처럼 표시하지 않는다.
3. Execution은 구현 의존 순서와 BE/FE 분담을 정하고 각 phase에 검증·완료 증거를 둔다. API 계약을 복제하지 말고 spec 절을 참조한다. 내부 입출력·코드 후보·schema invariant·실패/재시도/권한 테스트는 WP가 소유.
4. 기존 작업 브랜치 하나를 계속 사용. 새 워크트리/브랜치/발주 만들지 않는다. 필요한 allowed_paths 밖 변경(예: 코드 docs)은 코디 담당으로 별도 표시한다.
5. WP는 리뷰어 검수 및 사용자 리뷰 전 초안이다. 완료 보고에 범위·검증 계획·실제 차단 미결 유무·후속 W2 경계를 요약한다.

## 7. 범위 제약

코드·회사 레포·index/log·리뷰 보고서 수정, 커밋/push/PR, 테스트 실행·DB reset·배포 금지. OQ-A·D2·N값·자동 추천 값을 임의 확정하지 않는다.

## 8. 검증

문서 양식/links/phase 상태·frontmatter 일관성, W1 전 표면과 인수조건 추적, 원문 권한/멱등/원자성 보존, SPEC→WORK 역참조 0. W1 spec 변경이 없음을 확인 후 WP 작성한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_69d666d1-f133-49e6-94e6-2e6e5e72079e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
