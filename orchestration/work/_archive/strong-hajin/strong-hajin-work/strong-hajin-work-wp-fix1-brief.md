
# [writer] WORK-001 수정 — 실제 코드·멱등·권한·승인 연속성 정합

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디와 같은 워크트리에서 직렬로 작업한다. 코드 레포는 읽기 전용이다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` F-1~6 / W-1~7.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/source-issue-7.md` 및 기존 BASE/DEC/SPEC/WORK-001.
- 코드 작업 사본 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`의 **AGENTS.md, Makefile, 실제 schema/test 경로**를 먼저 읽는다. 브리프의 과거 직접 pytest 지시는 정정됐고 앞으로 Makefile만 사용.
- para/projects/project.md와 templates/projects 해당 양식.

## 2. 배경

WP FAIL을 수정한다. 이번에 코디가 정한 기술 방향을 문서에 구체화하고 원문과 다른 부분 없이 실행 가능한 계획을 만든다. spec과 WP가 함께 바뀌므로 둘 다 재검수한다. 코드 작업·테스트 실행은 하지 않는다.

## 3. 계약 및 코디 결정

F-1: migration 프레임워크를 새로 도입하지 않는다. 기존 모델 metadata와 reset_demo 전용 스키마 소유를 유지하고, **이 작업 전용으로 만든 빈 격리 테스트 DB**에 목표 스키마를 생성해 DB 수준 활성 담당 유일성을 검증한다. DB 제약 보장을 application 검사로 낮추지 않는다. 기존 DB에 schema_sync가 제약을 추가할 수 있다고 쓰지 않는다. 기존 DB 적용/전환은 이번 실행 범위 밖이며 실제 사용자 데이터 reset 금지. 로컬 사용자 DB로 실행 가능한 것처럼 보고하지 않는다. W1 검증/미리보기 환경은 빈 disposable DB 기준을 명시한다. rollback은 코드/모델 및 일회용 환경 교체 기준, 존재하지 않는 migration downgrade와 데이터 무손실 보장을 발명하지 않는다.

F-2: 검증은 코드 AGENTS.md와 Makefile 타겟. 각 phase 변경 범위에 맞는 make test-unit/test-contract와 관련 검사, 마지막 make verify 및 격리 PostgreSQL make test-postgres·핵심 acceptance journey. 환경 미확인은 required test 자체 면제 아님 — 검증 미완이면 완료 불가. 현재 코디가 config도 정정했다. 전량 4회 반복 제거. 실제 DB 실행은 구현 시 전용 DB URL·격리 확인 후 수행, 이번은 계획만.

F-3: **논리적 생성 명령마다 멱등 키 필수**를 선택한다(리뷰 선택 a). FE는 한 번의 생성 의도에서 키를 만들고 응답 유실/재시도·연타 동안 같은 키 재사용, 새 생성은 새 키. REST 키 누락/빈 값 거부, MCP/AX/회의후속도 같은 의도에 안정적인 키를 보존해서 application에 전달. 내용 해시+시간창으로 의도적인 두 업무를 합치지 않는다. 키 scope는 조직/tenant 경계가 있다면 포함한 행위자+명령 종류, payload 정규화 해시 불일치 충돌. 영수증 반환 전 현재 열람/실행 권한 재검증, 권한 상실 시 존재 은닉. SPEC·DEC·WP·BASE의 '선택', '키 없이 동일 명령 중복0', 호출자 재시도 규칙을 일관되게 고친다. 일반 신규 호출의 키 자동 생성은 매 재시도 새 키가 되지 않도록 명시. 서로 다른 키+동일 내용 두 명령은 독립 생성 허용. 동시 동일 키 1건 및 동시 동일 회의 후보(키가 달라도 후보 identity로 1건) 검증.

F-4: W1은 **신규 수평 요청의 WorkRequest 출처 기록 및 source_work_request_id를 보존하되 수락 대기/판단/회차는 만들지 않는다.** 기존 완료 승인 경로가 출처를 읽는 사실을 반영해 생성 타입별 완료 연속성 테스트를 넣는다. 상세 도메인 상태는 코드 조사로 확정하고 '수락됐다'는 가짜 사람 행위를 기록하지 않는다. **사용자가 지정하는 승인자 기능은 API 수용·FE 노출 모두 W2 완료 경로와 함께 활성화한다.** W1에서 받아서 무시하는 API 금지. 내부 nullable 저장자리 선행 추가는 가능하나 public field가 작동한다고 표시하지 않는다. 최종 제품 SPEC의 승인자 0..1 계약은 유지하고, WP 실행 단계 경계에 W1 제한과 W2 잔여를 명확히 적는다. 'W1만 배포해도 최종 승인자 계약 충족' 표현 제거. 새 수평 요청에서 기존 요청자 승인 흐름이 실제로 이어지는 경로와 테스트를 구체화한다.

F-5: 후보 판정에서 수신자의 work_request.decide 필터 제거. 로그인 가능한 대상/본인 제외/기존 조직 scope 교집합은 유지, 명령과 목록에 같은 판정 적용. 생성 행위자의 work_request.create 등 기존 경로별 역량 검사 유지. 배정·판단 역량 없는 구성원↔구성원 성공 사례 필수. 새 task.assign 부여 금지.

F-6: self는 수신자 대상 추가 검사만 없음. 인증과 기존 task.self_manage 검사 유지. horizontal/managed는 각 경로의 기존 기본 역량 및 scope를 실제 코드로 대조해 보존한다. 세 경로의 인증/역량 없는 principal 거부 테스트. 리뷰 권고만 보고 원래 없던 역량을 다른 경로에 임의 추가하지 않는다.

WARN: 신규 경로의 거절 신설/노출 금지와 과거 endpoint 보존 구분, D4 과거 fixture/읽기 호환 필수검사 제거(기존 코드 무단 삭제 금지로 표현), 새 타인 생성은 권한 검사와 같은 머지 단위로만 공개, operation inventory diff 항목 패치 계획, 동시 승격 검증 추가. W-7 index는 코디가 수정했다.

## 4. 범위

SPEC 변경은 멱등 계약과 신규 거절 인수조건 정합 등 F-3/W-1 범위. W2 복구 OQ-A, 문의 D2, 자동 승인자 값 등 기존 미결은 확정하지 않는다. 새로운 문제를 찾으면 구체적 근거로 보고하고 조용히 제외하지 않는다.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`

## 6. 순서

1. 실제 코드/규칙을 읽고 F-1~6 및 W-1~6에 대한 수정표를 만든 뒤 문서 반영.
2. SPEC/DEC에서 변경 계약과 코디 기술 결정을 명시. WP의 입력·권한·멱등·출처와 완료 호환·schema/검증·rollback을 단일 방향으로 닫는다.
3. 모든 caller/관련 타입의 대응과 검증 매핑, phase 의존/머지 단위 점검. phase는 TODO 유지.
4. 완료 보고에 수정 항목별 파일:줄 및 새 미결 유무를 제공한다. WP/스펙 재검수 후 사용자 리뷰를 거친다.

## 7. 금지

코드·회사문서·index/log·config·리뷰 보고서 수정, 커밋/push/PR, 테스트·DB 실행 금지. 기존 temp.md 및 reference task.md는 사용자 작업이므로 건드리지 않는다.

## 8. 검증

양식, SPEC→WORK 역참조0, 구현 불가능한 중복보장0, 사용되지 않는 승인자 입력 수용0, 새 DB 제약 검증과 기존 DB 전환 제외 정합, 실제 Makefile 명령 사용, 신규 생성의 권한 빠지는 중간 머지0 확인. 테스트 성공을 주장하지 않는다.

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
