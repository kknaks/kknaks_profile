# delivery-1 결과 보고 — 상태: done (Issue 2개 발행 · 승인 대기 — receipt 는 만들지 않음 · 사용자 몫)

## 최종 (3차 — 코디 답 ㉮ · 사용자 지시 2026-11-25 「우회해서 만들 수 있잖아」)

| request | Issue | status | baseline | labels | next_action | plan_digest | contract_digest |
|---|---|---|---|---|---|---|---|
| WP-1 BE · KOS 호출 → DAY 원장 호출 (`day/day-kos-call-notify-be` · L2 · SPEC-002 · 005) | [CENTURION_DAY#283](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/283) | created | origin/main `b152d463` · ready | delivery-plan:review · execution-plan:ready · spec-baseline:ready | review-delivery-plan(human gate) | `sha256:61ce7c7084c3cb6f086267e0293161191f0143df3e8d1fe216c699915992c547` | `sha256:cd26c78fa4128fb471cddaf1552a3d1287b79c1fe6ef4c790522b448a4a3e32b` |
| WP-2 웹 · 예약 / 고객 화면 열림 설정 (`day/day-kos-call-notify-web` · L2 · SPEC-006 · 007) | [CENTURION_DAY#284](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/284) | created | origin/main `b152d463` · ready | (같음) | review-delivery-plan(human gate) | `sha256:b5be6ea1aae0343de22acc16469fdf8e1988cfc7ea76d40cbe053a5a89f71f55` | `sha256:99ab21646e14471f614672124bf2a94725c0929e3375e8c6d3c7e600c1a468f5` |

- 계약 원천 문장을 두 Issue 의 **target_delta 첫 줄(본문 머리)** 과 **review_surface 첫 줄**에 넣었다: 「계약 원천 = mediness PR #965 브랜치 kknaksss/day-kos-call-notify-spec a498d34b(+ 이번 커밋) · main 판 SPEC-002 · 005 · 006 · 007 은 개정 전 · #965 머지 뒤 같은 idempotency key · contract_version 2 · 새 main SHA 로 재결속」.
- 승인 receipt 형식(사용자 몫 · 적용 안 함): `{"decision":"approved","reviewer_type":"human","reviewer":"<사람>","plan_digest":"<위 값>"}` → 같은 request 로 `--apply --plan-approval-receipt <파일>`.
- 결과 `partial: true` · `task_projection: blocked` — Mediness Task(MCP) 연결을 하지 않아서(best-effort · Issue 를 되돌리지 않음).
- 커밋 `9656c6c2` 을 PR #965 에 push(PR head = `9656c6c2816a7a8b4fa517b477523f7839891a4c` 확인 · 머지 안 함): `30-work.md` Spec Coverage — SPEC-002 · 005 행에 #283 · SPEC-006 · 007 행에 #284 · `log.md` wp-add 한 줄. lint `--strict` = 0 error · products/day 0 줄(263 WARN 타 제품 — 무관).
- 파일: `delivery/wp1-be-request-v1.json` · `wp2-web-request-v1.json`(baseline b152d463 로 고침) · `*-plan-v1.json` · `*-apply-v1.json` · `*.err`.
- WP 표 · BE ↔ FE 계약은 아래 1차 기록 그대로(바뀐 것 = baseline · 계약 원천 문장).

---

(아래는 막혔던 1차 · 2차 기록 — 그대로 둠)

## 막힌 것 — baseline (우회하지 않음)

| 시도 | 명령 | 결과 |
|---|---|---|
| ① 지시대로 baseline = `a498d34b32da…`(PR #965 head) | `mediness start-delivery --plan`(WP-1 · WP-2 둘 다) | **exit 2** `{"error": "requested SPEC baseline is not the fetched latest origin/main revision", "status": "conflict"}` — 원문 `delivery/wp1-be-plan-v1.json` · `wp2-web-plan-v1.json` |
| ② 확인만(쓰기 없음) baseline = latest origin/main `b152d463…` | 같은 `--plan`(scratchpad 사본 · 저장 안 함) | `status: planned` · **`spec_baseline_state: ready`** · `next_action: review-delivery-plan`(human gate) |

- CLI 규칙(`tools/harness/references/requests.md`): `spec_baseline_revision` = command 가 fetch 한 `origin/main` 이어야 한다 → PR 브랜치 head 는 쓸 수 없다.
- ② 는 막히지 않지만 **의미가 틀리다**: origin/main(b152d463) 의 DAY-SPEC-002 · 005 · 006 · 007 은 이미 `stable` 이라 CLI 가 `ready` 로 본다. 그러나 이 Delivery 의 계약(SPEC-002 개정 ㉚ 규칙 40 · SPEC-005 「KOS 에서 건 호출」 · SPEC-006 개정 ⑭ · 007 개정)은 main 에 없고 #965 에만 있다. `pending` 이 나오지 않으므로 「pending baseline 으로 최초 발행」은 이 CLI 로 만들 수 없다. main 으로 apply 하면 옛 계약에 `ready` 로 결속된다 → 사람 판단.
- `--apply`(GitHub Issue 생성)는 하지 않았다. 승인 receipt 도 만들지 않았다.

### 고를 것 (코디 · 사용자)
- **ⓐ (권장)** #965 를 먼저 머지(사용자) → 새 origin/main 으로 같은 요청을 `--plan` → `--apply` → `spec-baseline:ready` · L2 라 `review-delivery-plan`(사용자 승인 receipt) 뒤 구현. 요청 json 은 baseline 한 줄만 바꾸면 된다(review_surface 의 「pending」 문장도 같이 고침).
- ⓑ main `b152d463` 로 지금 apply — CLI 상 `ready` 지만 main 의 SPEC 본문이 이 계약과 다르다는 것을 review_surface 에 밝히고 사람이 받아들임. 권장하지 않음(하네스 「SPEC authority = main exact revision」과 어긋남).

## WP 표 (Delivery 두 판 · 병렬)

| WP | idempotency key | 위험 | target SPEC | 범위 | 완료 조건 | migration | 되돌리기 |
|---|---|---|---|---|---|---|---|
| WP-1 BE · KOS 호출 → DAY 원장 호출 | `day/day-kos-call-notify-be` | L2 | DAY-SPEC-002 · 005 | 규칙 40 ① ~ ⑨ — `_apply_tasks` 판정 · 방문 잠금 뒤 이전 `doctor_called_at` · `status` · 묶음(같은 kind · 원장 집합 · 가장 이른 시각과 허용 오차) · 메아리 창(op pending · sent · confirmed · 2xx 뒤 failed / last_error BLOCKED · 토큰 없음만 보내기 전) · 늦은 관측 · 사슬 · KOS 수락 전이 · 시스템 계정 · 두 경로 커밋 뒤 `after_call` · `_recipients` called_doctor(kind one 규칙 40 만) · 시험 | A1 ~ A9 pytest · ruff · 아키텍처 + **A10 로컬 KOS DEMO 실물 1회**(지정 · 전체 · 여러 작업 동시 → DB 알림 행 · 웹 OS 알림 · iPad 시뮬레이터) · 이 실물로 OQ-99 · OQ-106 닫음 | 없음 | Code PR revert |
| WP-2 웹 · 예약 / 고객 화면 열림 설정 | `day/day-kos-call-notify-web` | L2 | DAY-SPEC-006 · 007 | `DAY_WEB_RESERVATION_CUSTOMER_ENABLED`(common/config bool 기본 False · dev.env true · prod.env 줄 없음 · local.env.example true) · 메뉴 숨김(`menu.py`) · 라우터 가드(`/reservations*` · `/customers*` — 303 /board · HTMX HX-Redirect · SSE 연결 안 함 · 권한보다 먼저) · APP_ENV 분기 없음 · 새 글자 없음 | A1 ~ A4 · A6 pytest/파일 검사 + **A5 설정 켬 · 끔 두 번 화면 확인** | 없음 | Code PR revert 또는 env true + 재배포 |

요청 원본: `delivery/wp1-be-request-v1.json` · `delivery/wp2-web-request-v1.json`(execution = code_surface · phases · verification · predeploy · rollback 다 채움 — L2 준비).

## BE ↔ FE 계약 (겹치는 곳)
- 두 WP 는 **코드 면이 겹치지 않는다** — WP-1 = `emr/` 동기화 · `services/notifications.py` · 테스트 / WP-2 = `common/config.py` · `menu.py` · 웹 라우터 4개 · `deploy/config` · 테스트. 같은 파일 수정 없음.
- 서로 주고받는 API · 칸 없음. WP-1 의 결과(알림 행 · 판 「호출」)는 기존 웹 OS 알림 · 앱 경로로 그대로 보이고, WP-2 가 막는 경로(`/reservations` · `/customers`)는 판 · 알림이 쓰지 않는다(SPEC-006 §3 「그대로」 줄 · 검수 r1 확인).
- 병렬 가능 · 머지 순서 무관. 둘 다 dev 배포 뒤 dev → prod ff 에 같이 실림.

## baseline
- SPEC PR MediSolveAIDev/mediness#965 head `a498d34b32da77937824dd9a695573ff9bf73941`(origin/main `b152d46325423848fb6682a4c18d3269748d6cb1` 위 · 검수 r3 PASS · 미머지).
- 코드 `origin/dev` `55e60aa4d6f3be048bc7e933ee5dbd5f74456bfc`(미커밋 없음).

## 하지 않은 것
- `--apply` · GitHub Issue 생성 · 승인 receipt.
- `30-work.md` Spec Coverage · `log.md` · 커밋 · push — Issue 번호가 없어 행을 쓸 수 없어 멈춤(ⓐ/ⓑ 결정 뒤 같이 함).

## 2차 — 코디 답(선례 day-reservation2 방식) 뒤 확인 (2026-11-25)

- 코디 지시: baseline = origin/main `b152d463` + `spec-baseline:pending` · review_surface 에 SPEC 원천 = PR #965 브랜치.
- **pending 을 만들 수 없다 — CLI 판정 근거(코드)**: `tools/harness/src/mediness_harness/surfaces.py:99-123` — baseline revision 의 `spec-*.md` frontmatter 를 읽어 `status == "stable"` 인 id 를 모으고, `missing = [target ∉ stable]` 이 있을 때만 `"pending"`, 아니면 `"ready"`. request 에 pending 을 선언하는 칸은 없다.
- 선례(#275 ~ #278)는 target DAY-SPEC-007 이 그때 main(`c43633be`)에 없어서 pending 이 나왔다. 이번 target 은 main `b152d463` 에 모두 `status: stable`(DAY-SPEC-002 · 005 · 006 · 007 — 아래 확인) → 같은 방식으로 내면 **`spec-baseline:ready`**(위 ② plan 결과 그대로).
- 그래서 apply 하지 않았다(pending 이 아니라 ready 로 옛 계약에 결속되므로). 30-work · log · 커밋 · push 도 하지 않았다.
- 사람이 고를 수 있는 길(내가 고르지 않음):
  - ㉮ ready 를 받아들이고 apply — review_surface 에 「main 의 target SPEC 은 개정 전 판 · 계약 원천 = #965 a498d34b · #965 머지 뒤 contract_version 2 · 새 main 으로 재결속」을 적는다(라벨은 `spec-baseline:ready` 로 찍힘 — 선례와 다름).
  - ㉯ target 에 main 에 아직 stable 이 아닌 SPEC 을 넣어 pending 을 만든다 — 그런 SPEC 이 없어 새로 지어야 함(창작 금지 · 권장 안 함).
  - ㉰ 하네스 쪽에 「같은 SPEC 의 미머지 개정」 pending 을 표현할 길을 더함(하네스 변경 — 이 발주 범위 밖).
