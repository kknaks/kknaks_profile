# [reviewer] Delivery #226 KOS 연동 — 코드 검수 (L3 · 외부 연동 · credential)

너는 day reviewer 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/`(rules.md 체크리스트 — 2026-11-06 테스트 규칙 줄 포함). **읽기 전용** — 파일 수정 · 커밋 금지. 산출물은 리포트 1개.
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 · #225 커밋됨, #226 은 미커밋(`git status` · `git diff`). AGENTS.md 의 「테스트」 절 추가(DB 쓰는 테스트 나누기 · 2026-11-06)는 코디가 넣은 것 — 같이 본다.

## 읽을 것

- 계약 Issue #226 `gh issue view 226 -R MediSolveAIDev/CENTURION_DAY` (A1 ~ A7 · 하지 않는 것)
- 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-brief.md`(코디 결정 1 ~ 3 · 만들 것) · 구현 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-report.md`(「호출마다 API · 토큰」 · 「비워 둔 칸」 · 「코디가 확인할 것」 1 ~ 6)
- 시스템 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` · SPEC-000 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-000-data-model.md`(01 · 02 · 05 · 06 · §2 · §2.1) · 레포 `AGENTS.md`
- 본: cc-prototype `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/kos/<파일>` · 앞 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-225-report.md`
- KOS 규칙: 프로젝트 설정 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/config/projects/day.json` `repos.reference_kos.notes` · `data_rules`

## 볼 것

1. **계약 A1 ~ A7** — 리포트 주장을 코드 · 테스트로 확인. 「하지 않는 것」 침범(실제 KOS 쓰기 · Vegas · 소켓 · 명동점).
2. **KOS 쓰기 0** — `SUPPORTED_WRITES` 가 비었는지, commands 경로를 부르는 코드가 정말 없는지 grep 전수. 토큰 · 키 · 테넌트 id · 실명이 코드 · 테스트 · fixture · 로그 · 예외 메시지에 새지 않는지.
3. **동기화 정확성** — upsert 의 `ON CONFLICT … WHERE deleted_at IS NULL` · 외부 id 는 `external_ref` 에만 · 사라짐 / 되살림 · 같은 회차 두 번 = 행 그대로 · 병원 경계(다른 병원 행을 건드리지 않음) · transaction 안에서 KOS 를 기다리지 않음 · 잠금(남의 잠금 해제 · 타임아웃 · worker 죽었을 때).
4. **「추정 금지」** — mapper 가 응답에 없는 값을 지어내지 않는지(리포트 「비워 둔 칸」 표와 코드 대조). `is_system_account` 판단 · 직원을 내부 `account/v2` 로 받은 것(cc 와 다름) 판정.
5. **outbox** — 상태 전이 · 재전송 · 실패 뒤 막힘 · seq(유일 제약 없이 advisory lock) 판정.
6. **테스트** — 2026-11-06 규칙: 도메인 규칙이 DB 없이 단위 테스트로 있는지, `infra` 는 DB 가 보장하는 것만인지 · fixture 가 값이 가짜인지 · 조용히 통과하는 자리.
7. 리포트 「코디가 확인할 것」 1 ~ 6 각각 판정.

직접 돌려도 된다: compose `up -d --wait postgres redis` → `scripts/test.sh -q` · `uv run pytest -m "not infra"` · ruff. 포트 11040 · 11042 · 11043 만, 끝나면 `down`. **KOS 를 부르지 마라**(실물은 워커가 1회 함).

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-226-report.md` — 판정(PASS · WARN · FAIL) · 지적마다 파일:줄 + 근거 + 고칠 방향 · 「코디가 확인할 것」 판정표 · 직접 돌린 수치 · 「조용히 통과」 따로. 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
