# planner — Delivery Issue v1 발행 (start-delivery)

너는 맥락이 없다 — 아래 파일이 전부다. 원 브리프 `customer-erd-spec-brief.md` 의 금지(비밀값 · 이메일 · 테넌트 출력 금지 · 커밋 · push · PR 금지)와 §9 완료 보고 두 명령(이번 dispatch preamble 의 task-id · dispatch-id)은 그대로다.

## 읽을 것

- 절차: mediness `.claude/skills/start-delivery/SKILL.md` · `tools/harness/references/requests.md` · `rules/delivery-workflow.md`
- 앞 사례 — 같은 제품 · 같은 CLI 실행 방식:
  - `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/_archive/day/kos-signin-limit/delivery/ksl.v1.request.json` · `ksl.v1.plan.json` · `ksl.v1.apply.json`
  - `ksl.v2.approval-receipt.json` · `ksl.v2.approve.*`
  - 그 폴더의 `delivery-close-instructions.md` · `kos-signin-limit-spec-brief.md`(start-delivery 실행 줄)
- 결과 계약의 원천:
  - mediness PR #952(SPEC-002 개정 ㉔ · SPEC-000 2026-11-19 칸 수정) — 브랜치 `kknaksss/customer-erd-sync` · 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec`
  - #951(main 머지됨 · SPEC-000 §4 새 테이블)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/_RESUME.md` §2 결정

## 워크트리 — 파일 수정 금지 · CLI 실행만

- mediness(detached): `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-delivery` = origin/main `4585fb59cdfb1203ad6285d53b64edd11363a5f3`
- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd` = origin/dev `bbd9220aebf303eda503ca23c63388ad40fe2eda`(방금 fetch한 최신)
- GitHub repo: `MediSolveAIDev/CENTURION_DAY`
- 요청 · 결과 json 위치: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/delivery/`

## v1 request

- `idempotency_key`: `day/customer-erd-2026-11-19`
- 제목: 메뉴 · 구매 · 시술권 · 선불카드 · 처방 테이블(마이그레이션) + KOS → DAY 동기화
- `risk_level`: **L3** — schema 마이그레이션 · prod 서비스 중이다.
- `target_specs`: `DAY-SPEC-000` · `DAY-SPEC-002`
- baseline:
  - SPEC-002 개정 ㉔ 은 #952(미머지)에 있다. 사용자 결정은 「머지는 코드와 한 번에」다.
  - Skill 규칙대로 판단한다. 지금 main(`4585fb59`) 기준 ready 로 할지, `spec-baseline:pending` 으로 시작해 #952 머지 뒤 v2 로 재결속할지 정한다.
  - 판단과 이유를 리포트에 적는다. 정답이 모호하면 pending 쪽을 쓴다.

### target_delta

| ID | 내용 |
|---|---|
| D-1 | 마이그레이션 0010. SPEC-000 §4 새 테이블 28개와 `visit_task` 빈 값 허용 칸 3개(`treatment_item_id` · `ticket_id` · `machines`)를 만든다. **지금 테이블 · 칸의 이름 · 타입은 바꾸지 않는다(더하기만).** 모든 새 테이블에 `deleted_at` 을 두고, 유일 제약은 살아 있는 행만 대상으로 한다. |
| D-2 | 모델과 매핑을 만든다. KOS 값 → DAY enum 표와 `external_ref.entity_type` 새 값은 SPEC-002 ㉔ 를 따른다. |
| D-3 | 메뉴 동기화. 1시간 기준 정보 회차에 메뉴 목록을 더한다. 원천은 내부 API 이고, 시술 항목 · 기기 · 약물만 공개 API 다. |
| D-4 | 오늘 동기화(10초). 구매는 `purchaseIds` 를 묶어 받는다. 시술권 · 카드는 바뀐 고객만 받는다. 처방 · `visit_task.ticket_id` 는 이미 받는 일정 응답에서 채운다. |
| D-5 | 병원 전체 변경(5분). 공개 통계 3개(거래 · 카드 이벤트 · 구매 항목)는 id 를 모으는 데만 쓰고, 데이터는 내부 원장 API 로 받는다. |
| D-6 | upsert 와 삭제. 삭제는 소프트 딜리트만 쓰고 물리 삭제는 금지다. 지운 구매는 내부 `deleted:true` 로 안다. |

### acceptance

- A1: alembic 0010 upgrade → downgrade → upgrade 왕복이 로컬 compose DB 에서 성공한다. 0009 head 에 이어진다.
- A2: 기존 테이블의 칸 · 타입 변경이 0 이다(모델 diff).
- A3: DEMO 테넌트 실호출로 메뉴 테이블이 채워진다. 건수가 조사 리포트 규모와 맞는다.
- A4: DEMO 오늘 일정의 구매 · 거래 · 시술권 · 카드가 채워지고 `external_ref` 가 연결된다.
- A5: 시술현황 판 기존 테스트가 통과한다. 판 화면 동작은 바뀌지 않는다.
- A6: 동기화 코드에 물리 DELETE 가 0 이다.
- A7: 새 테스트가 통과한다(매핑 · upsert · 사라짐 · 바뀐 고객만).

### non_goals

- 백필(OQ-00-3 · 다른 담당)
- DAY → KOS 쓰기 · 원장 전환
- 화면
- 직원 결제 · 환불 감사 로그
- prod 배포
- 실 명동점 호출

### review_surface

- L3 schema 추가와 prod 무중단(더하기만)
- 내부 API 의존(브라우저 UA)
- enum 매핑: `REFUND`→`revoke`, 5분 회차의 구매 항목 통계
- 기본값 OQ-69~75

### execution

`code_surface` 는 코드 워크트리에서 **실제로 확인한 경로만** 적는다. 이 아래 경로는 출발점일 뿐이다:
- `backend/day/models/`
- `backend/migrations/versions/`
- `backend/day/emr/`(kos client · mapper · normalized · sync)
- `backend/day/tasks/emr.py`
- `backend/tests/`

`phases`:
1. DB(마이그레이션 · 모델)
2. 메뉴 동기화
3. 오늘 동기화
4. 5분 회차

`verification`:
- pytest 해당 파일
- `backend/tests/migrations` 왕복
- DEMO 로컬 실물

`rollback`:
- alembic downgrade 0010
- revert

## 실행

1. 앞 사례와 같은 방식으로 `--plan` → `--apply` 한다. L3 라 `delivery-plan:review` 가 나온다.
2. **승인 receipt** — 사용자(GitHub `kknaksss`)가 2026-11-19 코디 대화에서 「이슈 발행하고 db 만들자」로 이 결과 계약대로 발행 · 구현을 지시했다.
   - 새 `plan_digest` 로 `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"<digest>"}` 를 만든다.
   - `--plan-approval-receipt` 로 plan → apply 를 다시 실행한다.
   - 다음 action 이 `implement-and-open-code-pr` 가 될 때까지 진행한다. execution 이 모자라면 `prepare-execution-projection` 이 나오고, 그때 코드를 읽어 채운다.
3. MCP task projection 이 안 되면 허용된 진단 reason 으로 기록한다(앞 사례 방식).
4. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/delivery-start-report.md` 를 쓴다:
   - Issue 번호 · URL
   - 상태 라벨
   - baseline 판단
   - plan_digest
   - 다음 action
   - 확정된 execution(code_surface · phases)
