# planner — Delivery Issue v1 발행 (start-delivery) · 테이블 보충

너는 이 지시서의 맥락을 파일로만 받는다. 원 브리프 `day-cc-mig-spec-brief.md`(같은 폴더)의 금지(비밀값 · 이메일 · 테넌트 출력 금지 · 파일 커밋 · push 금지)와 §9 완료 보고 두 명령(subject 「planner 완료: delivery v1 <이슈 번호>」)은 그대로다.

## 읽을 것

- 절차: mediness `.claude/skills/start-delivery/SKILL.md` · `tools/harness/references/requests.md` · `rules/delivery-workflow.md`
- **앞 사례(같은 제품 · 같은 CLI 실행 방식 — 그대로 따라 하라)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/delivery-start-instructions.md` 와 그 `delivery/` 폴더(`cerd.v1.request.json` · `plan` · `apply` · `approval-receipt` · `approve.*`)
- 결과 계약 원천: mediness **PR #954**(미머지 — 브랜치 `kknaksss/day-cc-mig-spec` · 커밋 1944f922 · SPEC-000 §4A) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2 · 검수 `review-spec-000-4a-report.md`

## 워크트리 — 파일 수정 금지 · CLI 실행만

- mediness(detached): `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-delivery` = origin/main `ccede2866d006607509c5e34bdad33079fa9dffd`
- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-cc-mig` = origin/dev `844eace4`(방금 fetch 한 최신 · 브랜치 `kknaksss/day-cc-mig`)
- GitHub repo: `MediSolveAIDev/CENTURION_DAY`
- 요청 · 결과 json 위치: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/delivery/` (파일 이름 앞붙이 `dcm.`)

## v1 request

- `idempotency_key`: `day/day-cc-mig-tables-2026-11-20`
- 제목: KOS 키 전부 담는 테이블 보충(마이그레이션) + 동기화 매퍼 채우기 + 기존 행 업데이트
- `risk_level`: **L3** — schema 마이그레이션 · prod 서비스 중
- `target_specs`: `DAY-SPEC-000`
- baseline: SPEC-000 §4A 는 #954(미머지). customer-erd 때처럼 Skill 규칙대로 판단 — 정답이 모호하면 `spec-baseline:pending` 으로 시작해 #954 머지 뒤 재결속. 판단과 이유를 보고에.

### target_delta

| ID | 내용 |
|---|---|
| D-1 | 마이그레이션 0012 — SPEC-000 §4A 새 표 12 + 기존 표(prod 9 · dev 15) nullable 칸 · 새 DAY enum 타입 · `external_ref.entity_type` 새 값(hospital). **지금 표 · 칸 이름 · 타입 변경 0(더하기만)** · 새 표 `deleted_at` · 유일 제약은 살아 있는 행만. 0011 head 에 이어짐 |
| D-2 | 모델 + 매퍼 — §4A 의 「동기화로 채움」 칸 전부를 이미 도는 회차(일정 10초 · 기준 정보 1시간 · 판매 · 메뉴)의 응답에서 채운다. 상태 · 종류 = DAY enum · **목록 밖 KOS 값 = 행 유지 · 그 칸 null + 동기화 경고(KOS 원래 문자열 남김)** · CARD 매핑 · `created_at` ← KOS 생성 시각 · 금액마다 통화 |
| D-3 | 병원 — 기준 정보 회차에 `get-hospital` · `get-default-operation-timetable` · `get-default-days-off` · 예약 그룹 휴무 · 예약 규칙 조회를 더해 `hospital` 칸 · 새 표를 채운다. KOS `hospitalId` → `external_ref` |
| D-4 | 고객 미동기화 칸 — §4A(OQ-4A-14) 대로. 원천 회차는 SPEC 기본값을 따른다 |
| D-5 | **기존 행 업데이트** — 이미 들어 있는 행의 새 칸을 채우는 수동 실행 경로(기존 `runtime/backfill.py` 의 `--dry-run` · `--resume` · KOS 1초 1회를 재사용하거나 넓힌다). **로컬: 드라이런 → 실제 업데이트. dev 배포: 실제 업데이트**(사용자 2026-11-20) |

### acceptance

- A1: alembic 0012 upgrade → downgrade → upgrade 왕복 성공(로컬 compose DB) · 0011 에 이어짐
- A2: 기존 표 칸 · 타입 변경 0(모델 diff)
- A3: DEMO 테넌트 로컬 실물 — 동기화 한 회차 뒤 새 칸 · 새 표가 채워진다(병원 · 운영 시간 · 고객 칸 · 구매 · 일정)
- A4: 목록 밖 enum 값 시험 — 행은 저장 · 칸 null · 경고 1줄
- A5: 기존 업데이트 경로 — 로컬 드라이런(건수만 · DB 쓰기 0) → 실제 실행(새 칸 채워짐) 둘 다 실물
- A6: 시술현황 판 기존 테스트 통과 · 화면 동작 변경 0
- A7: 동기화 코드에 물리 DELETE 0 · 새 테스트 통과

### non_goals

- ext API(2단계) · 화면 · 수납 · 문진 · 타이머 · 리액션 · 예약 칸/점유 표
- DAY → KOS 쓰기
- prod 배포(dev 배포까지 — dev 실제 업데이트는 코디가 서버에서)

### review_surface

- L3 schema 추가 · prod 무중단(더하기만)
- enum 목록 밖 값 처리 · 값 미관찰 enum 칸(늘 null)
- 업데이트 경로의 KOS 호출량 · 자기 세션만 해제

### execution

`code_surface` 는 코드 워크트리에서 실제로 확인한 경로만. 출발점: `backend/day/models/` · `backend/migrations/versions/` · `backend/day/emr/` · `backend/day/services/emr_*.py` · `backend/day/tasks/emr.py` · `backend/runtime/backfill.py` · `backend/tests/`

phases: 1. DB(마이그레이션 · 모델) 2. 매퍼 · 동기화(병원 포함) 3. 기존 행 업데이트 경로 4. 로컬 실물(드라이런 → 실제)

verification: pytest 해당 파일 · migrations 왕복 · DEMO 로컬 실물

## 끝나면

이슈 번호 · URL · baseline 판단 · json 경로를 §9 두 명령으로 보고.
