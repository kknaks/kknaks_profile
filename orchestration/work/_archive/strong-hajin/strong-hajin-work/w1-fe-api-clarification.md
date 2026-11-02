# W1 FE 가시 계약 확인 — 2026-09-16

근거: WORK-001 Scope의 기존 경로 유지·입력 확장, Phase1 기존 필드 의미 유지, Phase3 기존 후보 함수 재사용, Internal Interface 경로별 권한 보존. SPEC §4는 목표 계약이며 W1에서 그 전체 shape를 전환하지 않는다. 아래는 이번 slice의 구현 기준이며 target 계약 삭제가 아니다.

1. 일반 구성원 타인 생성은 POST /api/tasks + assignee_id. 본인/생략은 self. REST Idempotency-Key 필수.
2. W1 후보는 기존 GET /api/work-request-assignee-candidates를 유지한다. /api/task-recipient-candidates 이름 전환은 이번에 하지 않는다. 후보 판정에서는 work_request.decide 필터만 제거하고 재직/로그인·본인 제외·조직 범위와 행위자 work_request.create 검사를 보존한다.
3. W1 생성은 기존 title/description 및 기존 일정 필드를 유지하고 assignee_id를 확장한다. content로 일괄 개명/응답 전면 전환은 이번에 하지 않는다. content 목표 계약을 W2 확정 사항이라고 단정하지 말고 후속 전체 API 정렬 사항으로 기록한다.
4. 관리자 기존 /api/tasks/assign 경로와 task-assignment-candidates를 유지한다. 생성 창은 envelope에서 허용한 경로의 후보만 합친다. self 우선, 배정 권한+배정 후보에 있는 대상은 기존 assign 경로, 나머지 work_request.create+수신 후보 대상은 tasks+assignee_id. 같은 후보 중복 제거. 서버에서 각 경로 권한/대상 범위를 반드시 재검사한다. API 실패시 다른 경로로 자동 재시도하지 않는다.
5. 두 목록에 동시에 속한 대상의 managed 우선은 기존 관리자 생성 경로 유지 목적이다. 요청 출처/완료 승인 의미가 다르므로 테스트에 overlap을 명시하고 기존 관리자 동작을 보존한다. 한 제출 의도에서 경로를 고정하여 재시도 중 endpoint가 바뀌지 않게 한다.
6. BE와 FE 모두 이 계약을 사용한다. 실제 코드와 충돌이 발견되면 구체적인 근거를 코디에게 보고하고 해당 부분만 보류한다. E2E는 사용자 담당, 자동 계약/컴포넌트 검증은 워커/코디 담당.
