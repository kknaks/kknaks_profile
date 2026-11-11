# [planner] DAY-SPEC-000 을 stable 로 — 그리고 Delivery 마감에 무엇이 더 필요한지 계획 확인

너는 day planner 워커(같은 터미널)다.

사용자(2026-11-11): 「아 그럼 스테이블에 올리고 다 닫자」 — DAY-SPEC-000(데이터 모델)을 `stable` 로 올리고 Delivery 를 닫는다. 근거 대화: 코디가 「#241 은 SPEC-000 이 draft 라 baseline 에 묶이지 않아 못 닫는다 · stable 로 올릴지는 사용자 판단」이라고 설명한 데 대한 답이다.

스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` — 코디가 **새 브랜치 `kknaksss/fix-app-re1-spec-stable`(= `origin/main` `1a450bcf` · 깨끗함)** 으로 옮겨 놓았다. 커밋 · push · PR 은 코디가 한다.

## 1. 문서 변경 (이번 발주의 본체)

- `products/day/20-spec/spec-000-data-model.md` 의 `status: draft` → `stable`. 이 레포 규칙(`rules/` · 다른 DAY SPEC 이 stable 로 올라갈 때 한 것 — `git log` 로 SPEC-001 · 003 등의 전례 확인)대로 같이 바뀌어야 하는 것을 **전부** 바꾼다: frontmatter(`last_updated` · 버전 규칙) · 문서 머리의 상태 문장 · `20-spec.md` 목차의 상태 칸 · `log.md` · 그 밖 「SPEC-000 은 draft」라고 적은 자리(다른 SPEC · `40-architecture/` · README — grep).
- 내용은 고치지 않는다. stable 로 올리는 데 **규칙상 막는 것**(열린 OQ 수 · 필수 절 · lint 규칙 등)이 있으면 고치지 말고 그것을 보고한다 — 사용자 지시는 「stable 로 올린다」이지 「내용을 정리한다」가 아니다.
- **DAY-SPEC-002(시술 현황)도 draft 다 — 이번에 건드리지 않는다**(사용자가 말한 것은 SPEC-000 뿐).

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).

## 2. 계획만 확인 (아무것도 적용하지 않는다)

SPEC-000 이 stable 로 main 에 들어갔다고 가정하고, 아래를 `--plan` · 규칙 읽기로만 확인해 보고한다:

- **#241**: 재결속(v6 — request 는 `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery/fix.v6.request.json` 에 보관) → review-delivery → spec-sync → 닫기 까지의 단계와, 각 단계가 요구하는 것. 특히 **수용 항목 중 「사용자 실기기」 · 「TestFlight」 몫(아직 안 함)** 이 `undetermined` 인 채로 닫을 수 있는지 · 닫을 때 사람 결정(receipt)이 어디에 필요한지.
- **2차 Delivery #234 · #235 · #236 · #239**(+ #238 closeout): 각각 지금 상태(라벨 · baseline) · target SPEC · 무엇이 막고 있는지(SPEC-002 draft 인지 등) · 닫으려면 사용자가 무엇을 정해야 하는지. **읽기만 — 라벨 · 본문 · 재결속 금지.**

## 하지 말 것

커밋 · push · PR · Delivery `--apply` · MCP Task 카드 · SPEC-002 변경 · 값 기재 금지.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-stable-report.md` — 1 의 바꾼 자리(문서:줄) · 막는 규칙 유무 · lint / 2 의 #241 단계표 · 2차 Delivery 4건 표 · 사용자가 정할 것.

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "바꾼 자리 / 막는 규칙 / #241 단계 / 2차 Delivery / 사용자 몫"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
