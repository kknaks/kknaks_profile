# [backend] #226 검수 WARN 반영(fix1) — W1 · W2 · W3 · W4 · W5 · W6 + 병원 경계 테스트

너는 day backend 워커다. 같은 워크트리 · #226 미커밋 변경 그대로 이어서. 앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-brief.md` 규칙 그대로(KOS 쓰기 금지 · 비밀값 금지 · 커밋 금지 · 포트 11040 · 11042 · 11043).
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-226-report.md` W1 ~ W6 · 「조용히 통과하는 자리」 · 레포 `AGENTS.md` 「테스트」(2026-11-06 — DB 쓰는 테스트 나누기).

## 고칠 것 (리뷰어 권장 방향 — 코디 결정)

1. **W1** — 기준 정보에서 매핑 실패로 뺀 행을 사라짐으로 처리하지 않는다: 종류별 「응답에 있었던 외부 id(매핑 실패 포함)」를 싣고 `seen` 에 합친다(일정의 `skipped_external_ids` 방식). 응답이 비거나 그 종류가 전부 실패하면 그 종류는 사라짐 표시를 하지 않는다. 테스트: DB 없이 1(후보 계산) + infra 1.
2. **W2** — outbox 전이 판단을 순수 함수로 빼서(예: `decide_after_send` · `decide_on_poll`) 상태 전이 테스트를 **DB 없이** 옮긴다. infra 는 DB 가 보장하는 것만(조건부 UPDATE 경합 · seq 동시 적재 · 막힘 UPDATE). `today_window` · 주기 테스트처럼 DB 가 필요 없는데 모듈 `pytestmark` 로 `infra` 가 된 것은 infra 아닌 파일로.
3. **W3** — 잠금 TTL 을 일마다 따로(일정 · 쓰기 큐 ≈ 60초 · 기준 정보 ≈ 300초, 설정값) · 회차 본문을 `asyncio.timeout(ttl - 여유)` 로 감싼다. 테스트 DB 없이.
4. **W4** — 두 세션 동시 `enqueue` → seq {1,2} infra 테스트 1개(advisory lock 을 지우면 실패해야 한다 — 직접 확인). 유일 제약 migration 은 하지 않는다(첫 실제 쓰기 Delivery).
5. **W5** — 로그에서 테넌트 id(일부 포함)를 뺀다 — `hospital_id` 로.
6. **W6** — mapper 의 대체 칸 이름 중 데모 응답 · fixture 에서 확인되지 않은 것(`funnelCategoryId` · `phoneNumber` 등)은 지운다. 확인된 것(`role.id`)은 출처 주석.
7. **병원 경계** — 두 병원에 같은 외부 id 를 넣고 A 에서 사라짐 처리 → B 그대로인지 infra 1개.

## 하지 말 것

W7(outbox 중복 발송 · SENT 정체 · 빈 expect) · W8(공용 계정) — 다음 Delivery / 사용자 결정. 손대지 마라. 모델 · migration 변경 금지.

## 검증 · 보고

`uv run pytest -m "not infra"`(수치) · compose `up -d --wait postgres redis` → `scripts/test.sh -q`(수치) · ruff 각 1회. KOS 실물 호출은 하지 않는다(로직 변경은 테스트로).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-fix1-report.md` — W 별 고친 곳(파일:줄) · 테스트 이동 전후 수(infra / not infra). 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
