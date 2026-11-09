# [reviewer] Delivery #225 데이터 모델 — 코드 검수 (L3 · 첫 schema migration)

너는 day reviewer 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/`. **읽기 전용** — 파일 수정 · 커밋 금지, 산출물은 리포트 1개.
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 는 커밋됨(`git log -1`), #225 는 미커밋 변경(`git status` · `git diff`). 너는 #224 검수를 했다(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-224-report.md`) — 그 W 들이 어떻게 처리됐는지도 본다.

## 읽을 것

- 계약 = Issue #225 `gh issue view 225 -R MediSolveAIDev/CENTURION_DAY` (A1 ~ A5 · 하지 않는 것)
- 정본 = DAY-SPEC-000 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-000-data-model.md` §2 · §3 · §6
- 구현 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-report.md` · 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-brief.md`(§3 코디 결정 1 ~ 6) · 대조 스크립트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-spec-compare.py`
- 레포 `AGENTS.md` · 본 centurion `backend/crm/db.py · models.py` · `backend/common/crypto.py` · linky 모델(enum 선례)

## 볼 것

1. **대조 스크립트를 믿지 마라** — 스크립트가 무엇을 비교하지 않는지(FK 대상 · ON DELETE · UNIQUE 범위 · nullable · 기본값 · 인덱스 · enum 값 목록)를 보고, 그 부분은 SPEC 과 모델을 직접 표본 대조(주제마다 최소 2 테이블 · 05 · 06 은 전부).
2. **리포트 「판단한 곳」** 각각 판정 — §2 우선 deleted_at 3 · 「uuid FK」 대상 추론 · FK 안 건 칸 · 코드 테이블 타입/필수 · 기본값 없음 · 하위 테이블 hospital_id 없음.
3. **migration** — 스키마 이름 없는 리비전이 dev/prod 에 같은 결과인지 · enum 공유 타입 생성/삭제 순서 · 순환 FK · downgrade 가 깨끗한지 · 리비전이 앱 코드를 import 하지 않는지.
4. **env.py autogenerate 수정** — 비교용 사본이 진짜 차이(칸 추가 · 타입 변경 · FK 대상 변경 · enum 값 추가)를 놓치지 않는지 **직접 실험**(스크래치 스키마에서 모델을 일부러 바꿔 `alembic check` 가 잡는지 — 저장소 파일은 되돌려 놓을 것, 남기지 마라).
5. **암호화** — 키 없음/틀림 기동 실패 · `DecryptionError` · `crm_connection.config` 의 어떤 키가 평문인지(`tenant_id`) 와 SPEC 04 · 로그 · repr 에 평문 노출.
6. **테스트** — `day_test` fixture 가 `day_dev` 를 건드리지 않는지 · 제약 테스트가 진짜 DB 위반을 보는지 · skip 이 숨기는 것.
7. 「하지 않는 것」 침범 · SPEC 에 없는 칸/테이블/인덱스 발명.

직접 돌려도 된다(`scripts/test.sh -q`, compose 포트 11040 · 11042 · 11043 만, 끝나면 `down`). 사용자 포트 · 컨테이너 금지.

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-225-report.md` — 판정(PASS · WARN · FAIL) · 지적마다 파일:줄 + 근거(SPEC 절 · Issue · AGENTS.md) + 고칠 방향 · 「판단한 곳」 판정표 · 직접 실험 결과. 「조용히 통과하는 자리」 따로. 완료는 preamble 의 worker_done 절차대로.
