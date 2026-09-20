
# [writer] 업무 스펙 1차 수정 — 리뷰 FAIL 8건과 WARN 9건 해소

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-spec-report.md` — V-1~8와 WARN 9건, OQ별 원문 근거.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/source-issue-7.md` — 확정 요구, 적용 차수, D2 미결, D4 제외.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-write-brief.md` — 원 발주. 아래 정정이 원 브리프의 SPEC 파일:줄 요구보다 우선한다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md`, `templates/projects/` 양식.
- 기대는 개념: 새 기술 선택 근거를 만들면 기존 규약대로 검토하되 불필요한 새 문서 생성 금지.

## 2. 배경 / 무엇을 바꾸나

초안은 검수 FAIL이다. 회사 원문을 읽을 수 없다는 진술은 사실과 다르며, PA 차수·문의 범위·막힘 UI·멱등성·후속업무 경로를 바로잡아야 한다. 동일 writer가 네 문서를 수정한다. 코디가 index/log를 이미 만들었으니 읽되 수정하지 않는다.

## 3. 계약

- 회사 원문은 gh api로 읽을 수 있다. 고정 revision e9bfadbd1db8068a0bbdbaf37b502503de295571의 PLAN-001 및 screens/modules/screen-004-work-management.md를 직접 조회해 대조한다.
- V-1~V-8 전부 해소. 추적 ID 등장만으로 충족 판정하지 말고 계약·차수·인수조건 보존을 확인한다.
- 원문 1차 최소/1차 추가와 이번 구현 slice 순서를 분리. PA-03/04/06 요구를 후속 차수로 강등하지 않는다. 반복·재촉·수신함 상세 조사 잔여는 명시하고 제품 범위를 축소하지 않는다.
- 문의 발송→회신 대기 자동 부착→답변 해소의 확정 계약은 작성. D2 복수 문의 해소/취소 정책만 미결 유지. 코드 부재는 제외 사유가 아니다.
- 목표 상태와 칩은 원문 기준으로 맞춘다. blocked/막힘을 현행 코드 때문에 존치하지 않는다. 신규 흐름에서 일관되게 네 상태, 회신 대기 파생, 외부 대기 상태 메모로 서술.
- 기존 REST 멱등 키 부재를 BASE에 정정. 목표 API는 재전송·동시 생성·중복 활성 담당 안전성을 계약하고 기존 경로 재사용만으로 달성했다고 쓰지 않는다.
- 회의 화면/회의록 재설계는 제외하되 회의 후속업무 승격은 W1 동일 생성/권한/멱등성 계약에 포함한다. 관련 REST/MCP/AX/권한/seed 영향 조사 누락 보완.
- OQ-1(배정 후 거절)과 과거 pending 처리를 분리. 전자는 원문에서 신규 거절 규칙 신설 제외로 해소, 후자는 D4 제외로 사용자 게이트 제거.
- OQ-2/3/4/6/7은 리뷰 원문 근거로 해소. 시간대·부품 매핑은 코드 조사, 위임전결 순서는 PLAN-005 조사. 실제 정책 값 미지정이면 그 값만 미결로 남긴다.
- OQ-5 중 승인자 없는 업무 오완료 복구만 사용자 질문이 나갔다. 답변 전에는 이 부분만 pending. 승인자가 있는 업무의 마지막 판정자 되돌리기는 원문과 PLAN-002 대조해 반영한다. 사용자 답변을 기다리며 다른 수정 중단 금지.
- 최신 회사 SPEC #719/#722/#725 중 업무 계약 관련 변경은 실제 본문 차이를 대조해 보존/충돌 표를 BASE에 기록한다. 무관한 회의 전체 설계는 다루지 않는다.

## 4. 먼저 읽을 핵심 파일

원 브리프의 네 문서와 코드 경로 및 리뷰 리포트 파일:줄. 사용자가 생성 요청한 코드 작업 사본은 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`이며 기준 8973791, 읽기 전용.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`

## 6. 구현 단계

1. 원문을 먼저 읽고 V-1~8을 고친다. SPEC의 내부 코드 경로/명령/구현 지시는 BASE 코드 관측으로 모아 보존하고 SPEC에는 사용자/API 계약만 남긴다. WP는 아직 만들지 않는다.
2. WARN 9건도 수정: ID는 BASE-001/DEC-001/SPEC-001/002로 규약 정렬(파일명 유지); 본문 관계 wikilink 중복 제거; direct 의미 반전 금지; 취소는 완료 탭; 행 액션은 다음 한 걸음; AX 확인 칩 귀속을 근거 없이 승인요청으로 정하지 말고 보존되는 AX 확인 surface와 업무 종류 칩 경계를 정의; 개발주체/제품 축소 해석은 코디 판단임을 표시; 체크리스트 기존 API 보존과 1차 UI 제외 구분; 조직 업무는 원문 팀 관리 경계로 정렬.
3. 미결은 실제 남은 D2·OQ-5 조각 및 근거로 못 닫은 값만. 기술 조사 항목과 사용자 결정 항목을 구분한다.
4. 완료 보고에 V-1~8/WARN 9건별 해소 근거와 변경 파일, 잔여 질문을 적는다.

## 7. 범위 제약

회사 레포·코드·index/log·리뷰 보고서 수정 금지. commit/push/PR 금지. 새 사용자 결정을 발명하지 않는다. 사용자 답변 전 복구 규칙을 기본값으로 굳히지 않는다.

## 8. 검증

네 파일 allowed_paths, 양식, 모든 내부 관계 참조, 실제 요구 추적, 신규/기존 계약 구분 및 API/상태 교차 일관성을 확인한다. 없는 린트 통과 주장 금지. 코드 테스트 실행 금지. 초안 상태 유지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_c9090395-400c-4ac1-a2fd-f34b76f818df \
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
