
# [writer] WORK-001 최종 정정 — assigned 출처 상태와 MCP 명시 키

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT

이번 WP 수정본과 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-wp-fix1-brief.md` F-3·F-4. 후속 두 항목만 정정한다.

## 2. 배경

코디가 네 수정 문서와 실제 MCP _mutation_key를 확인했다. 호출 시점 랜덤 키는 외부 클라이언트 재시도의 동일 의도를 알 수 없으므로 필수 안정 키 계약을 만족하지 않는다.

## 3. 확정한 기술 방향

1. 신규 WorkRequest 출처 상태값은 `assigned`, 의미는 **즉시 배정됨**. Task 수행 상태(open/in_progress/done/cancelled)와 다른 출처 상태다. pending/accepted 기존 값의 의미를 바꾸지 않고, 수락/거절/조정 판단 없이 업무와 활성 담당이 생성된 사실만 표현한다. 가짜 사람 accept 감사 로그 금지. 완료 승인 경로는 source_work_request_id로 요청자를 찾도록 보존한다. 상태 enum이 외부 응답에 나오므로 SPEC에도 노출 의미를 명시한다.
2. W1 **MCP 생성 도구는 명시적 idempotency_key 인자를 받는다**. 누락/빈 값 거부. 외부 호출자가 한 생성 의도에서 키를 만들어 재시도마다 유지하고, 다른 생성 의도는 새 키를 사용한다. 호출 시점의 서버 랜덤 fallback 금지. AX 컨텍스트도 논리적 도구 호출의 안정 키를 전달해야 한다.
3. AX_MCP_CAUSATION_ID 하나만으로 키를 만들지 않는다. 하나의 turn에서 같은 종류의 업무를 두 개 만드는 경우도 각 의도마다 다른 키여야 한다. payload는 키 재료가 아니라 충돌 검사용 지문이다. 기존 AX action.id가 있으면 그 action의 재실행 식별로 보존한다. 단순 turn/operation 동일성이 업무 생성 의도의 동일성은 아니다.
4. W1에 해당하는 생성 경로만 고친다. 공용 _mutation_key를 무조건 바꿔 다른 MCP mutation들의 기존 멱등 의미를 손상시키는 계획 금지. 새 W1 key resolver 분리 또는 명시적 범위 제한을 적는다. 조회 및 제안만으로 실제 업무가 생기지 않고 AX 실행 확인 유지.
5. 필수 검증: 명시키 없는 MCP 거부, 동일키/동일payload 재시도1건, 동일키/다른payload 충돌, 같은 turn/같은 operation/다른 명시키 두 생성 성공, response 유실 뒤 호출자 재시도1건, 다른 actor/조직 scope 격리. 기존 비W1 mutation에 회귀 없음.

## 4. 대상

DEC-001 기술 결정·SPEC-001 API/MCP/요청 상태/멱등 인수조건 및 WORK-001 caller 표·Phase4·6·Open Issues. SPEC-002에 영향을 주는 표현만 동기화.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`

## 6. 순서

1. 위 두 항목을 문서에 정정하고 상태값 이름 미결을 닫는다.
2. 'causation ID 없으면 호출 때 새 키'와 '공용 helper 일괄 변경' 표현을 caller 표·phase·계약에서 전부 제거한다.
3. 기존 F-1~6 수정은 보존한다. 문서 version은 수정 사실에 맞춰 갱신. 다른 제품 결정을 새로 만들지 않는다.

## 7. 금지

코드·회사 레포·index/log·config·리뷰 보고서 변경 금지. 테스트/DB/커밋/push/PR 금지. OQ-A·D2 답변 추정 금지.

## 8. 검증

두 기술 결정의 SPEC/DEC/WP 일관성 및 잔존 fallback0 확인. 상태값은 출처 상태와 수행 상태를 혼동하지 않음. 짧은 완료 보고에 변경 파일·줄을 제시한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_403d6b6f-69f4-4925-99a7-f5fa9e7573a8 \
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
