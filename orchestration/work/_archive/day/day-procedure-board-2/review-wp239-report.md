# 리뷰 리포트 — day-procedure-board-2 / doc(WP) — Delivery CENTURION_DAY#239 (2026-11-10)

대상: `gh issue view 239 --repo MediSolveAIDev/CENTURION_DAY`(본문 · 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`). 읽기만 했다(Issue 수정 없음).
기준: 스펙 워크트리 커밋 4490876e(SPEC-002 개정 ⑯ · SPEC-000) · `_RESUME.md` §2 2026-11-10 차트 · 방 이동 · 결정 (가) · 「방 배정」 id · ⑯ 리뷰 · 재리뷰 답(:70 ~ :74) · `research-har-room-chart-report.md`.
코드 대조: CENTURION_DAY 워크트리(HEAD caa72435 + 미커밋 F9 4파일).

## 판정: WARN (FAIL 0)

Target ① ~ ⑦ 이 개정 ⑯ 을 빠짐없이 덮는다. 스펙 밖 계약도 없다. Acceptance 는 테스트 · 화면 · 데모 실물로 나뉘었고, Non-Goals 는 「이번에 안 하는 것」 표 · OQ 와 같다. 고칠 것은 Execution 쪽이다. 수정 후보에 빠진 파일(W1), #236 의 「누른 카드만 갱신」 계약과의 접점(W2), migration 「forward-only」와 레포 downgrade 테스트(W3), 같은 PR 에 쌓을 때 #236 증거 순서(W4) 네 가지다. 승인 전에 Issue 에 한두 줄씩 더하면 된다.

## 1. Target Delta ↔ 개정 ⑯ (PASS)

| 스펙 ⑯ | Issue |
|---|---|
| 「방 배정」 = 설정 id(규칙 3) · 기타 작업 보임 · 기타 작업도 [종료]해야 [귀가 대기](재리뷰 답 ①) · 설정 비면 OQ-49 기본값 | ① |
| SPEC-000 05 `is_room_assign` · `started_room_id` · `visit_task_chart_log` · 01 `room_assign_etc_task_id` | ② |
| U-14 차트(탭 · 표 · 첫 탭 · 담당자 처음 값 3단계 · 목록 · DAY 에만 · 집도의 처음 값 · 필수) | ③ |
| 자동 저장 · 「최근 저장 : HH:MM」(창 열 때부터) · 작성자 · 「KOS」 · 이력 · outbox 순서 · 결정 (가)(시술 전 = 이력만 · [수락] 때 한 번 검증 · 호출 없는 [시작]) · 동시성 4갈래 · 시술 전 글 뒤 KOS 수정이면 안 보냄(재리뷰 답 ③) | ④ |
| U-15 방 이동(팝오버 · 「점유 이동」 · 「이동」 · 점유 한 번 · 「방 배정」 만드는 중도 `room_held` · 띠 · [복귀하기] 확인 창 없이 + 토스트 · 계산 점유) | ⑤ |
| 규칙 30 · 33 · U-12 원래 방 묶음 · 스냅샷 `holdRoom` · `canMoveRoom` · `canReturnRoom` · `rooms` · `doneTab.homeRoom` · 차트 JSON | ⑥ |
| 데모 설정 값(DB 데이터만) | ⑦(env · 일회성 · 하드코딩 없음 — 스펙 「설정 화면 없음 · DB 데이터로만」과 맞음) |

- 스펙 밖 계약: 없음. 라우트 · 오류 코드 · `event_log` 이름은 「제안」 표기 그대로다. 「검토할 부분」이 구현이 바꾸면 spec-sync 라고 적었다.
- OQ-40 · 42 · 50 은 닫힌 상태로 반영됐고, 열린 OQ 목록(37 · 38 · 39 · 41 · 43 ~ 49)도 스펙과 같다.

## 2. Acceptance (PASS · 낮은 지적 1)

- A1 ~ A8 은 항목마다 어떤 테스트(rules · API · infra · web · column snapshot) · 스크린샷으로 볼지 적혀 있어 검증할 수 있다. A10 은 문구 · pytest · test.sh · ruff 다.
- A9 데모 실물 10항목 ↔ 스펙 확인 안 됨 묶음:
  - OQ-38: 진행 중 작업 이동(⑤) · `roomAssignedDateTimeUtc`(①) · `sequences` 여러 개(⑥) · `add-flow-tasks` → 다음 조회 가려내기(④) — **모두 있음**.
  - OQ-39: 담당자 빈 작업 메모(⑩) — 있음. 「KOS 가 남기는 작성자 · 이력」은 KOS 조회가 작성자를 돌려주지 않아(HAR 리포트 1-4) 데모로도 확인할 길이 마땅치 않다 → OQ-39 에 그대로 남는 것으로 충분하다. 메모 `sequences` 여러 개는 일괄 적용(Non-Goal) 전제라 빠진 것이 맞다.
  - 그 밖 ②③⑦⑧⑨ 는 새 쓰기 경로의 실물 확인이라 더한 것이 맞다. 결과표(2xx · 다음 조회 값 · outbox 상태)를 Issue 에 남기고 spec-sync 로 KOS 쓰기 표 · OQ-38 · 39 를 갱신한다는 흐름도 맞다.
- (낮음) A9 ⑨ 「KOS 웹 메모 수정 → DAY 반영」은 사람이 KOS 웹에서 고쳐야 한다. 「사용자 허락 뒤」(의존성)에 「사용자 · 코디가 KOS 웹에서 수정」 한 줄을 더하면 누가 할지가 분명하다.

## 3. Non-Goals (PASS)

- 일괄 적용 · 작성자 여러 명(작성자 추가 · 칸 지우기) · 지난 방문 · 침대 수 · 「(n/m)」 · 관리실 기록 창 · 날짜 이동 · 체류 구간 · 토스트 글자(OQ-41 · 48) · 차트 이력 보기 · 보존 운영(OQ-44) · OQ-37 · 설정 화면 · prod 설정 값 · Flutter — 스펙 「기획안 중 이번에 안 하는 것」 표 · OQ 와 모두 같다. 빠진 것 · 더한 것 없음.

## 4. Execution

### W1. 수정 후보에 빠진 파일 — 판 묶음 조회 · 동기화 본체 · 정규화 칸
- **`backend/day/queries/board.py`**(`load_world`)가 빠졌다. 차트 이력(작성자 · 마지막 저장 · `baseLogId`) · `is_room_assign` · `started_room_id` · 원래 방 · 차트 담당자 목록을 판 · 스냅샷 · 차트 JSON 에 실으려면 여기를 고친다(#236 의 `doctor_changed_at` · `starting` 도 여기서 읽었다).
- **`backend/day/emr/sync.py`** 가 빠졌다. 반영 대기 칸을 지키는 guard(`guard_of` · `EXPECT_TASK_FIELDS` :1171 · `TASK_COLUMNS` :1180)와 작업 칸 반영이 여기 있다. 차트 글 guard · KOS 수정 → 이력(`source kos`) · `is_room_assign` 저장은 이 파일 몫이다. Issue 는 `services/emr_sync.py`(조회 주기 · 신호)만 적었다.
- **`backend/day/emr/normalized.py`**(NTask 에 `etceteraTaskId` 칸 — 지금 매퍼는 `etceteraConfiguration.name` 만 읽음 · `mapper.py:500`) · **`backend/day/emr/base.py`**(`WriteKind` 에 새 op 종류)도 빠졌다.
- 견본 판 `routers/kit_board.py`(sample world — 기타 작업 · 점유 · 차트 견본)도 #236 때처럼 같이 고칠 자리다.
- 빠져도 워커가 찾겠지만, 계약 문서의 「수정 후보」가 리뷰 · review-delivery 의 대조 기준이 되므로 더하기를 권한다.

### W2. #236 v3 의 「누른 카드만 갱신(version · OOB)」 계약과 새 조작의 응답 모양이 적혀 있지 않다
- #236 v3 ⑲(Acceptance A13): 웹 조작 응답 = 누른 카드 조각 + OOB(인박스 · 호출 탭 · 탭 숫자 · 원장 상태) + version. #239 의 방 이동 · 복귀 · 차트 저장도 웹 조작이다.
  - 방 이동 · 복귀는 그 카드(파란 띠 · 방 이름)와 인박스를 바꾸므로 같은 `_after` 모양을 따라야 한다.
  - 차트 저장은 스펙상 「그 줄 조각」(모달 안)이다. 집도의가 바뀌면(수락 · 진행중 → 규칙 27 전부) 판 카드 원장 글자 · 원장 상태도 바뀐다.
- Target ⑤ · ④ 와 Execution 에 이 접점이 없다 → 「방 이동 · 복귀 응답 = #236 ⑲ 조작 응답(누른 카드 + OOB + version) · 차트 저장 = 그 줄 조각 + 집도의가 바뀌면 그 카드 · 원장 상태 OOB」 한 줄을 Target 이나 Execution 에 더할 것. 안 그러면 판 카드가 다음 신호까지 옛 방에 남거나, 판 전체 다시 그리기(F8 이전)로 돌아갈 수 있다.

### W3. 「migration forward-only」와 레포의 downgrade 테스트
- 「문제가 생겼을 때 되돌리는 방법」: 「migration forward-only — 칸 · 테이블을 지우는 새 revision 대신 그대로 두고 코드만 되돌림(차트 이력은 지우지 않음)」.
- 레포 `backend/tests/migrations/test_alembic.py:89` `test_downgrade_base_는_version_을_비우고_다시_upgrade_된다` 는 모든 revision 의 `downgrade()` 가 돌아야 통과한다(#236 의 0006 도 `downgrade()` 가 인덱스를 지움). 그래서 새 revision 의 `downgrade()` 는 `visit_task_chart_log` 를 지우는 코드가 된다.
- 운영 되돌리기 정책(downgrade 를 돌리지 않음 · 차트 이력 보존)과 테스트 요구(downgrade 함수 있음)는 함께 갈 수 있다. 다만 「forward-only」만 적으면 워커가 `downgrade()` 를 비우거나 막아 테스트를 깨뜨릴 수 있다. 「downgrade() 는 테스트용으로 두되 운영에서는 돌리지 않는다(의료 기록)」로 적기를 권한다.

### W4. 같은 코드 PR #238 에 쌓을 때 #236 의 review-delivery 증거 시점
- 의존성: 「같은 브랜치 · 커밋 caa72435 위(+ 미커밋 F9 — #236 쪽 마무리) · 같은 코드 PR #238」. 순서상 #236 v3 위에 쌓이는 것은 맞다(HEAD caa72435 = #236 v3 커밋 · F9 미커밋 4파일 확인).
- review-delivery 는 「exact PR head」 대조다. #239 커밋이 #236 의 review-delivery 전에 PR #238 에 들어가면, #236 의 증거가 #239 변경까지 섞인 head 에 묶인다. 또 ① 「방 배정」 판정 교체는 #236 이 만든 규칙(전부 완료 · 확인 필요 「귀가 대기 전」 · 체크 대상)의 결과를 바꾼다. 그래서 #236 Acceptance 를 그 head 에서 다시 보면 기대가 달라진다.
- → 「F9 를 #236 쪽으로 커밋하고 #236 review-delivery 를 그 head 에서 먼저 끝낸 뒤 #239 커밋을 쌓는다」 같은 순서 한 줄(또는 #236 · #239 를 한 번에 review-delivery 한다는 명시)을 의존성에 더할 것.

### 그 밖 (PASS)
- phase 순서(데이터 → 차트 → 방 이동 → 화면 → 검증 · 데모 실물)는 의존 관계와 맞다. 「방 배정」 판정 교체를 1단계에 둔 것도 맞다 — 2 · 3단계가 이 판정에 기댄다.
- 데모 실물(A9)이 dev 배포 · 사용자 허락 뒤다. prod 배포 없음 · prod 설정 값 = 배포 때(OQ-49 배포 체크)도 맞다.
- 「기존 테스트 중 「방 붙은 기타 작업 = 방 배정」 단언은 새 판정으로 고친다」 — #236 테스트 영향을 짚었다.

## 5. #236 과 겹침 (WARN — W2 · W4)

- 같은 파일(`board_rules.py` · `board.py` · `routers/board.py` · 템플릿 · `day.js`) · 같은 규칙(규칙 2 · 3 · 17 · 27 · 18 카드 순서)을 만진다. 순서상 #236 v3 커밋 위에 쌓인다.
- 부딪히는 자리:
  - ① 「방 배정」 판정 교체 → #236 의 전부 완료 · 체크 · 확인 필요 결과가 바뀐다(W4).
  - 차트 집도의 변경이 #236 의 규칙 27(원장 변경) 서비스를 재사용한다 — Issue 「규칙 27 재사용」 명시 · PASS.
  - 조작 응답 모양(#236 ⑲ — W2).
  - 카드 순서(#236 ⑰): 방 이동이 자리를 바꾸지 않는다고 ⑤ 에 명시 · PASS.

## 6. 위험 L3 근거 (PASS)
- 새 KOS 외부 쓰기(add-flow-tasks · change-tasks-room 다중 · cancel-flow-tasks 복귀 · change-tasks-doctors 차트 · memo 2종) · migration(새 테이블 · 칸) · 확인 안 된 KOS 동작(OQ-38 · 39)을 데모 실물로 확인 · 의료 기록(차트 이력 보존) · [귀가 대기] 조건 변화. L3 로 둘 근거로 충분하다.

## 참고 (낮음)
- 「기술 추적 정보」 기준 commit `9692e1fb`(main · 다른 제품 커밋)의 SPEC 링크에는 개정 ⑯ 이 아직 없다. 「검토할 부분」이 「⑯ 은 PR #920(4490876e)에만 · spec-baseline:pending · 머지 뒤 재결속」이라 밝혀 #236 과 같은 처리다 — 리뷰어가 링크만 열면 옛 스펙을 본다는 점만 기억할 것.

## 사용자 · 코디 확인

| # | 무엇 | 근거 |
|---|---|---|
| ① | #236 review-delivery 를 #239 커밋 전에 끝낼지 · 둘을 한 번에 볼지(W4) | 의존성 · start-delivery exact head |
| ② | 방 이동 · 복귀 · 차트 저장의 웹 응답 = #236 ⑲ 모양으로(W2) — Issue 에 한 줄 | #236 v3 A13 |
