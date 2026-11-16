# [reviewer] charty 1차 외부 연동 API 코드 검수 r1 (SPEC-008 0.4.3)

너는 **cc-prototype `reviewer` 워커**다. **너는 이 작업의 앞 맥락이 하나도 없다** — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-charty1` (브랜치 `kknaksss/ext-api-charty1` · **커밋 안 된 변경**이 검수 대상 — `git diff` · `git status` 의 새 파일)
base 브랜치: `origin/main`(`0a58aba`) → 최종 PR 대상 `main`
backend 워커가 같은 워크트리에 있으나 끝났고 쉬는 중이다. **파일을 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` (0.4.3) ← 계약의 SoT. 0.4.0 ~ 0.4.3 절 · §9 T48 ~ T73 · 부록 F · G
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` (D-01 ~ D-44) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/30-work/work-014-ext-api-charty1.md` — 「계약 고정점」 · WP-REVIEW 행(검수 항목) · 「주의」
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/kos0-report.md` — 데모 실물 모양(이력 · 휴무 · 선불카드 · 내부 시술권)
- backend 완료 보고 요지: 전체 `uv run pytest -q` 746 passed(기준선 647) · ruff 통과. 워커가 남긴 미결 6개 → 아래 §6 4

**기대는 개념**:

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/areas/concept/back/minimal-api-surface.md` — 외부 경로는 계약의 칸만 · 경로 고정 시험은 넓힐 뿐 지우지 않는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/areas/concept/back/api-documentation.md` — Swagger `summary` · `description`

## 2. 배경

`procedure/back` 에 외부 연동 API 를 더했다: lookup 고침 + 새 일곱(board · 예약 상세 · 언어 · 오더 메모 · 상담 메모 · 병원 · 직원). 외부 KOS(병원 관리 SaaS) 를 부르고 CC 사본 · `event_log` 를 쓴다. 기존 외부 여섯 경로 계약과 직원 API 동작은 그대로여야 한다.

## 3. 계약

SPEC-008 0.4.3 · WORK-014 「계약 고정점」 그대로. 프론트 없음.

## 4. 먼저 읽을 핵심 파일 (`procedure/back/` 아래 · 변경분)

- `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py` · `app/openapi_docs.py`
- `app/repository/db.py`(`consult_wait_first`) · `app/repository/repo.py`(`immediate()` · `set_visit_order_memo` · `consult_waits` · `put_consult_wait`)
- `app/domain/reservation_rules.py`(`is_after` · `consultation_passed`) · `app/service/reservations.py`(손댄 곳 셋: `_flow` · `_detail_reads` · `personal`)
- 시험: `tests/fake_kos.py` · 새 `tests/test_ext_{lookup2,detail,write,board,clinic}.py` · 고친 `tests/test_ext_{lookup,history,auth,docs}.py` · `tests/test_openapi_docs.py` · `tests/test_order.py`
- 비교 원본: `git show origin/main:procedure/back/<파일>`

## 5. allowed_paths — 이 밖은 건드리지 마라

- read-only. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-code-r1.md`

## 6. 할 일

1. **WORK-014 WP-REVIEW 행의 항목 전부**를 코드로 확인한다(SPEC 절 ↔ 코드 · 부록 F D-01 ~ D-44 반영 · 기존 여섯 계약 무변경 · 직원 API 무변경 · KOS 먼저 · 경로별 KOS 호출 수 §6.9 · `ext_call` 에 직원 id · 고객 · 예약 id 0 · 이력 규칙 · 시도 예약 · 요청당 10 · 과거 시술 · 예약 내역 본문 모델 무변경 · 헤더 다섯 경로만 · 실명 · 키 grep).
2. **시험이 계약을 실제로 고정하는지** 본다 — 시험이 초록이어도 단언이 약해 계약이 깨질 수 있는 자리(가짜 응답이 KOS0 실물 모양과 다른 곳 포함). 기존 시험에서 **지우거나 약하게 바꾼 단언**이 있는지 `git diff tests/` 로 전수 확인한다.
3. 시도 예약: `BEGIN IMMEDIATE` 트랜잭션 안에 `await` 가 없는지 · KOS 호출 전에 커밋하는지 · 요청 트랜잭션과 엉키지 않는지 · 예외 때 행이 잠긴 채 남지 않는지.
4. backend 미결 6개 판정(맞음 · 고칠 것 · 사용자 몫): ① customerId 갈래 KOS 고객 없음 = 404 또는 400+errorProperties NotFound 둘 다 `customer_not_found` ② 처음 봄(ⓐ) 때 이미 귀가면 `final_tried` 안 세움 → 다음 board 에서 ⓒ 1번 더 ③ `clinic_not_found` message 문구 「없는 병원이에요」(SPEC 에 문구 없음 — 기존 오류 message 관례와 맞는지) ④ 상세 `customer.customerId` 사본 없으면 null · 선불카드 객체 안쪽만 null ⑤ KOS0 인증 호출 ⑥ 실물 쓰기는 E2E 몫.
5. 필요하면 `uv run pytest -q <파일>` 로 시험을 돌려 봐도 된다(전체는 코디가 이미 돌렸다 — 746 passed). **사용자 포트 · 프로세스 · KOS 호출 금지.**

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · push 금지. KOS 호출 금지(실물은 코디의 E2E 몫)
- 결정하지 않는다 — 사용자 · 코디 몫 질문은 모은다
- 리포트는 public 레포 규칙: 키 · KOS id · 실명 · 실제 이메일 · 전화 0

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 기능 독립 위반은 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

- 리포트 맨 위에 판정 한 줄 · FAIL / WARN / 질문 수. WP-REVIEW 항목별 표(항목 → 판정 → 근거 파일:줄).
- 기존에 이미 깨져 있던 무관한 문제는 "무관"으로 분리한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aad33590-4323-443d-9c17-3541475ee5f5 --from term_a1d4dd8c-fb2e-484e-977f-a305b43f844e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
