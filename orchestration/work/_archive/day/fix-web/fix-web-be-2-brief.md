# [backend] E3 — 판 스냅샷 cards[].counselors

너는 **day backend 워커**다(1차와 같은 규칙 · 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web` · 1차 변경 위에 이어서). ⚠ frontend 워커가 동시에 템플릿 · static · styles · kit 라우터 · 화면 테스트를 고친다 — 그쪽 파일 금지.

## 1. SSOT

### 사용자 결정 — E2E 1회차 수정(2026-11-12 · 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` 「E2E 피드백」 E1~E4 + 보충 · 조사 `research-2-report.md`(같은 폴더).

- **E1** 방 카드 오더 메모 펼침 아이콘(`.day-memo__more`) → **파란 글자 「펼치기」 / 「접기」**, 메모 **제목 줄 오른쪽 끝**.
- **E2** 오더 메모 글자 12px → **14px**(접힌 높이 `--day-memo-max-h` 를 14px 기준 5줄로 다시 계산).
- **E4** 오더 메모에 제목 줄: **「오더 메모」 + 상담사 이름 배지(작은 글씨 · 여러 명이면 여러 개)** … 오른쪽 끝 「펼치기/접기」. 그 아래 메모 내용. **구분선 없음.**
- **E3** 상담사 = **그 방문의 상담(`consultation`, 삭제 안 됨) 전부의 `counselor_id` 직원 이름** · 중복 제거 · 상담 시작 순. **migration 없음 · 동기화 변경 없음**(KOS 는 상담 하나에 상담사 여러 명 저장 안 됨 — 사용자). 희망 상담사(`requested_counselor_id`) 안 씀 · 상담사 없으면 제목 「오더 메모」만 · 메모가 없으면 지금처럼 메모 칸 자체 없음 · 비활성 직원도 이름 표시 · 상담 의사 범위 밖 · **앱 변경 0**(앱 방 상세 배지 안 넣음).

**계약(backend → frontend · 스펙)**: 스냅샷 `cards[]` 에 `counselors: [{"staffId": str, "name": str}]` (없으면 `[]`) — `orderMemo` 옆. 앱은 모르는 키를 무시(research-2 §5 `board.dart:210-224`).

## 2. 할 일

1. `queries/board.py` — 판 대상 방문들의 상담(삭제 안 됨 · counselor_id 있음) 상담사 id 를 방문별로 읽기(한 번의 쿼리 · 방문 수와 무관한 쿼리 수 · 직원 이름은 이미 읽는 staff 사용 · 비활성 포함 · 지운 직원 제외 규칙은 지금 판 규칙 따름). 순서 = 상담 시작 시각(같으면 생성 순 · id) · 중복 제거.
2. `dtos/board.py` `BVisit` 에 칸 · `board_rules.py` 스냅샷 `cards[]` 에 `counselors: [{staffId, name}]`(:814 orderMemo 옆).
3. 테스트: 쿼리 수 고정(test_board_queries.py `one == 15` 등) 갱신 · 여러 상담 → 여러 명 · 중복 제거 · 순서 · 삭제된 상담 제외 · 없으면 [] 단언(test_board_rules / test_board_api — 실제 DB infra 1건 이상).
4. 동기화(emr/) · 모델 · migration 손대지 마라.

## 3. 검증 · 리포트

- `uv run pytest -q` 고친 테스트 파일 · `ruff check` 1회. infra 는 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q <파일>` (로컬 compose · 테스트 스키마).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/be-2-report.md`. 완료 보고는 1차와 같은 두 명령.
