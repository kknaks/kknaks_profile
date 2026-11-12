# prod-deploy-re1 — 스펙 개정 · Delivery 발행 결과

## 상태: done (승인 대기 — receipt 적용 안 함)

| 항목 | 값 |
|---|---|
| Issue | **#243** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/243 (OPEN) |
| 제목 | DAY prod 첫 배포 준비 — 운영 연결 등록 진입점(is_demo=false · prod api 컨테이너 안) · prod 설정 계약 시험 (DAY-SPEC-000 OQ-01-2) |
| idempotency key | `day/prod-first-deploy-live-connection` · contract_version 1 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` |
| risk_level | **L3** — 운영 DB 에 실제 병원 KOS 접속값(암호화)을 쓰는 길을 새로 만들고, 그 연결로 prod 가 실제 병원 KOS 동기화 · 쓰기를 시작함. migration · 공개 API 변경 없음 |
| contract_digest | `sha256:597fbb8115e3b93f4138eea0f5eecf94f86d313630e1c789da84f65821c95473` |
| plan_digest | `sha256:be8dd2505d7534c1eb8c0e968079012c79ad4f0d4c8749df1ce89df3d3e3dbc8` |
| baseline | `ready` · mediness `origin/main` `7f7319ec299c7ef4b904a6e66476c9d0e4997069`(그 시점 SPEC-000 이 이미 stable). **주의**: 개정 ④(OQ-01-2 닫음)는 아직 이 워크트리에만 있음(미커밋) — Review Surface 에 적었고, 스펙 PR 머지 뒤 같은 key · version 2 로 다시 묶을지는 코디 판단 |
| next_action | `review-delivery-plan` · human_gate true — 사용자가 plan_digest 를 승인해야 함(receipt 는 적용하지 않음) |
| task_projection | blocked(`delivery-plan-review-required`) · `partial: true` |

## 스펙 변경 (products/day 만)

- `20-spec/spec-000-data-model.md`
  - :31 머리말에 개정 ④ 메모 추가
  - :189 `is_demo` — 「데모 시드는 true · 운영 연결 등록은 false」
  - :205 `room_assign_etc_task_id` — prod 값은 운영 연결 등록 때 같은 연결 설정 값으로 넣음
  - :238 「환경」 — 운영 연결을 넣는 방법 = 운영 등록 진입점(OQ-01-2 닫음)
  - :1383-1384 **OQ-01-2 닫음** — 운영용 등록 진입점을 따로 둠 · `is_demo=false` · `backend` 안 모듈(`python -m`, 이미지에 `scripts/` 가 없어서) · prod api 컨테이너 안에서 1회 · 값은 env/표준입력에서만(레포 밖) · 브랜드 `ceramique` · 실제 병원 1곳(이름은 적지 않음 — 등록 때 사용자 값) · 데모 계정과 전체 권한 계정은 `prod.env` 에 둠
  - 상태 `stable`, 칸 · migration 변경 없음
- `40-architecture/deployment.md`
  - :21 2026-11-11 prod 첫 배포 준비 메모
  - :166-173 env 표 prod 칸을 「아직」에서 「채움/넣음」으로(공개 주소 · 데모 넘김 = dev 주소 · 허용 앱 `day.medisolveai` · blob/`prod` · Key ID 와 Team ID 함께 · APNs/Soniox prod Key Vault). 값은 prod.env 에서 모양만 확인했고 비밀값은 안 적음
  - :209-225 새 절 「prod 첫 배포 절차」 — Key Vault 8 → prod.env → 코드 PR · dev 배포 → migrate-prod → deploy-prod → 운영 연결 등록 → 운영 KOS 확인(IP 허용 여부 · OQ-01-3). 레포 `docs/development/deployment.md` 와 워크플로 사실 그대로
  - :233 Key Vault 행 — 남은 prod 6 → prod 8 넣음(브리프 사실)
  - :252-253 미결 — KOS IP 행에 확인 시점 추가(허용 요청 방법은 「그때 정함」으로 열어 둠) · 「prod 스키마의 실제 병원 연결」 행 닫음
- `log.md` :17 — `decision-add, spec-change, arch-change` 한 줄

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning, 그중 `products/day/` 는 **0**(나머지는 다른 제품에 원래 있던 WARN — 무관)

## 미결 · 주의점

1. **브리프의 함수 이름 정정**: 브리프의 `services/crm_connections.py seed_demo_kos_connection` 은 실제로는 `day/public.py seed_demo_kos_connection` → `services/crm_connections.py ensure_demo_connection` 이다. Issue 에는 실제 이름으로 적음.
2. 열어 둔 것(Issue open_questions/Review Surface): 같은 브랜드/병원 이름의 데모 연결이 이미 있을 때 덮을지 거절할지 · 진입점 모듈 이름과 env 이름 · 운영 KOS 나가는 IP 허용 필요 여부.
3. A4(prod 계약 시험)는 코디의 미커밋 `deploy/config/prod.env` 가 같은 코드 PR 에 들어가야 의미가 있음 — Execution dependencies 에 적음.
4. 병원 실제 이름은 브리프에 없어 적지 않음.
5. 하네스 실행 때 `tools/harness/.venv` 가 생김(gitignore 대상이라 git status 깨끗함).

## 파일

- request · 결과: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v1.request.json` · `prod.v1.plan.json` · `prod.v1.apply.json`
- 코드 워크트리 수정 0 · 커밋 · push · PR 0

## 수정 1 — review-doc-1 W1 ~ W6 · 코디 결정 (a) ~ (f) 반영 (2026-11-11)

### 스펙 (products/day · 미커밋)

| 항목 | 위치 | 반영 |
|---|---|---|
| W1 KOS IP | deployment.md :254(미결 「KOS IP 제한」 = **필요** · 403 `IPBlocked` 실측 · 사용자 허용 요청 · 절차 6 전) · :220 새 절차 **5-1 운영 KOS IP 허용** · :222 절차 7 = 「IP 허용 반영 확인」 | 리포트 문장 그대로 |
| W2 prod 브랜치 | deployment.md :218 절차 4 = prod 브랜치 있음(워크플로 파일 없음) → 먼저 fast-forward push → migrate-prod | 리포트 문장 그대로. 레포 `docs/development/deployment.md` 쪽은 v2 code_surface 에 넣음 |
| W3 Environment prod | deployment.md :238 준비 표 = dev 만 생김 · prod 없음 · 승인 규칙 없음 → 막는 장치 셋뿐 · 절차 아래 메모 :224 | 리포트 문장 그대로 |
| W6 DAY_ADMIN_EMAILS | deployment.md :162 prod 칸 = **채움**(값은 안 적음) | 리포트 문장 그대로 |
| (a) 거절 | spec-000 :1384 · :31 — 같은 브랜드 코드 · 병원 이름에 `is_demo` 가 다른 연결이 이미 있으면 거절(0 아닌 종료 · 쓰기 0 · 비밀값 없는 메시지 · 데모 시드처럼 덮지 않음). 같은 값으로 다시 돌리면 행이 늘지 않음(A1 그대로) | 해석: 「데모든 운영이든 is_demo 가 다르면」 = 기존 연결의 is_demo 가 이번 값(false)과 다르면 거절, 이미 같은 운영 연결이면 재실행 = 행 그대로 |
| (b) 실행 주체 | spec-000 :1384 · :31 「코디가 1회」 · deployment.md 절차 6 「누가」 = 코디 | — |
| (c) 가드 없음 | spec-000 :1384 「dev · APP_ENV 가드는 두지 않는다(사용자 2026-11-09)」 · deployment.md 절차 6 「**prod api 컨테이너에서만 실행**」(dev 에서 돌리면 day_dev 에 실제 병원 접속값 · 코드 가드 없음) | — |
| (d) env 접두 | spec-000 :1384 「`DAY_SEED_*` 재사용 안 함 · 이름은 구현 때」 | — |
| (e) log 종류 | log.md :17 = `spec-change, arch-change` · 요약에 수정 1 내용 추가 | — |
| (f) Soniox | deployment.md :170 「한 줄 더함(구현 때)」 → 「`day_vm.py` `OPTIONAL_SECRETS` 에 있음」 | — |

### Delivery #243

- **v1 은 승인하지 않음(W4).** Issue 본문은 CLI 가 metadata · digest 와 함께 관리하므로 지금 `gh` 로 직접 고치지 않았다. 「다음 단계: 스펙 PR 머지 → 같은 key contract_version 2 재결속 → 사용자 승인」은 v2 request 의 `review_surface[0]` 에 넣어 v2 apply 때 본문에 들어간다.
- **v2 request 준비만 함(apply 안 함)**: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v2.request.json`
  - `contract_version 2`. `spec_baseline_revision` 은 자리표시라서, 스펙 PR 머지 뒤 fetch 한 `origin/main` 40자 SHA 로 바꿔야 한다. `scope_delta` 에 v1→v2 사유를 적음.
  - W1: predeploy 에 「운영 KOS IP 허용(사용자 · A6 의 전제)」을 넣고 open_questions 를 비움. A6 실행 주체 = 코디, IP 허용 뒤.
  - W5: `non_goals[5]` 를 리포트 문장으로 바꿈(prod.env 데모 · 전체 권한 계정은 예외).
  - (a): Acceptance **A2b** 거절 시험을 더하고 verification 에 거절 시험을 넣음.
  - (c): Non-Goal 「dev · APP_ENV 가드」를 더함.
  - L3 근거에 「GitHub Environment prod 없음 · 승인 규칙 없음」을 더함.
  - 「정한 것」 줄: 거절 · 코디 · 가드 없음 · DAY_SEED_* 재사용 안 함 · 이름은 구현 워커.
  - code_surface 의 레포 docs 에 절차 4 맞춤(W2) 추가.
  - 스키마 확인: 지금 `origin/main`(7f7319ec)으로 임시 `--plan` 만 돌려 통과했다(status planned · contract_version 2 · review-delivery-plan). 쓰기는 없었고 임시 파일은 지움. 실제 plan_digest 는 새 SHA 로 다시 계산된다.

### 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · 263 warning · `products/day/` 0(나머지는 다른 제품에 원래 있던 것 — 무관).

### 남은 것

- 스펙 PR(코디) 머지 → 코디 지시로 v2 apply(SHA 바꿔서) → 사용자가 v2 plan_digest 승인.
- 레포 `docs/development/deployment.md` 절차 4 정정은 코드 PR 몫.

## 수정 2 — review-doc-2 N1 ~ N3 반영 (2026-11-11)

워크트리만 수정했다. 스펙 PR mediness#933 위에 미커밋으로 남아 있다.

- **N1**: 「사용자가 1회」를 「(prod api 컨테이너 안에서만 ·) 코디가 1회」로 바꿈 — deployment.md:255 · log.md:17 · v2 request `target_delta[0]`. 이제 이 문구는 `products/day` 와 v2 request 어디에도 없다.
- **N2**: 「환경별 가드 금지」의 출처를 「사용자 「환경별 가드 금지」(코디 전달 2026-11-11) · 같은 취지 2026-11-09 개정(:41 · 「환경」 :234)」로 고침 — spec-000:1384 · v2 `non_goals[6]`.
- **N3**: 절차 5 를 「4 의 push 로 멈춘 deploy-prod 실행을 다시 실행(Re-run)」으로 바꿈 — deployment.md:219. 레포 docs 쪽 절차 5 는 코드 PR 몫(v2 `code_surface[5]`).
- lint `--strict`: exit 0 · 0 error · `products/day` WARN 0.

## 수정 3 — 코드 리뷰 W2 · 코디 결정 (a) 양방향 거절 (2026-11-11)

- spec-000:1384: 「데모 시드처럼 덮지 않는다」를 사실대로 고침 → **데모 시드도** 같은 브랜드 코드 · 병원 이름의 운영 연결(`is_demo=false`)을 만나면 덮지 않고 멈춘다(양방향 거절 · 실제 병원 접속값을 데모 키로 덮는 사고 방지) · 데모 → 데모 다시 넣기는 그대로. 개정 ④ 메모(:31)와 log.md:17 에도 같은 단서.
- v2 request:
  - A3 에 단서를 붙임: 운영 연결을 만나면 데모 시드도 멈춘다 · 쓰기 0 · 비밀값 없음.
  - A2b 의 「ensure_demo_connection 처럼 덮지 않음」은 이제 맞지 않아 「덮지 않음」으로 고침.
  - scope_delta 에 한 줄 더함. apply 는 하지 않음.
- lint `--strict`: exit 0 · 0 error · `products/day` WARN 0. 워크트리 미커밋 2파일(spec-000 · log.md).

## v2 apply (2026-11-11 · 코디 지시)

- **범위**: 준비해 둔 prod.v2.request.json 그대로(prod 첫 배포 준비만). 웹 디자인 수정(E55 · W1/W2)은 넣지 않았다 — 첫 지시로 잠깐 넣어 본 판은 `--plan` 만 돌리고 버렸다(apply 안 함 · 파일 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v2.request.with-web.discarded.json`).
- **baseline**: 지시 전제(#933 미머지)와 달리 **mediness#933 은 이미 머지됨** — `origin/main` = `7bdde9f2c354555fd7597d8896cc6095d6420bca`(「docs(day): prod 첫 배포 … (#933)」 · 내 워크트리 HEAD 와 products/day 차이 0 · 양방향 거절 포함). CLI 판정 `spec_baseline_state = ready`(pending 아님). Review Surface[0] 에 「#933 이 머지된 커밋 7bdde9f2」 명시 · dependencies[0] 「#933 머지됨 — 결속 끝」 · scope_delta 끝에 같은 한 줄.
- **--plan**: exit 0 · status planned · execution ready · plan_review review-required.
- **--apply**: exit 0 · status `scope-delta-recorded` · core healthy · `partial=true`(task_projection = blocked / `delivery-plan-review-required` — 승인 전이라 정상).
- **Issue #243** https://github.com/MediSolveAIDev/CENTURION_DAY/issues/243 본문 갱신됨(2026-11-11T11:25:13Z) — meta contract_version=2 · Acceptance A2b · A3 양방향 거절 · baseline 7bdde9f2 확인.
- **라벨**: `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready`.
- **contract_digest**: `sha256:ed0cd574b0243c5c47f5254963186824e5934cf74cdf8a690f1052f6131a41f3`
- **plan_digest (v2 · 승인 대상)**: `sha256:3923f54de098a1512dc77de84789af391fe8f1d5c0f7759e4fb9b1467058b094`
- **next_action**: review-delivery-plan · human_gate=true — **승인 receipt 는 적용하지 않음(사용자 몫)**.
- 산출물: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/prod.v2.request.json` · `prod.v2.plan.json` · `prod.v2.apply.json`.

## 수정 — 공개 페이지 /privacy · /support (2026-11-12 · 코디 수정 8)

### 스펙 (products/day · 미커밋 3파일)

- **DAY-SPEC-001 개정 ⑦**(공개 경로 · 인증 예외가 있는 곳 = §2 「화면 라우트」 — 「업무 화면이 세션 없이 열리면 /login」 줄 바로 아래):
  - `GET /privacy` · `GET /support` 는 로그인 없이 연다(세션 검사 · `/login` 이동 없음).
  - 본문 = 60-release §6-1 · §6-2 승인 문안 그대로 · 이 SPEC 은 글자를 정하지 않는다.
  - 앱 설정 「정보」 링크(DAY-SPEC-003 개정 ⑫)가 `/privacy` 를 연다.
  - 머리 개정 노트 ⑦ 한 줄 · `last_updated` 2026-11-12.
- **60-release §7-2 #1** 「지금」 칸 끝에 「**구현 중(fe-3)**(사용자 승인 2026-11-12 · 원천 DAY-SPEC-001 개정 ⑦)」. 이 파일은 그 한 줄만 바뀜(수정 전 사본과 diff 확인).
- **log.md** 2026-11-12 spec-change 한 행(DAY-SPEC-001).
- 새 화면 글자 없음 — 본문은 60-release §6 을 가리키기만 함.

### Delivery #243 — 넣지 않음

- **이유**: #243 은 백엔드 범위(운영 연결 등록 진입점 · prod 설정 계약 시험)다.
  - Non-Goals 2번째 줄이 「공개 API 변경 · 웹 화면 변경 · 웹 버그 수정」을 범위 밖으로 둔다. 공개 페이지는 웹 화면 추가라 이 줄과 충돌한다.
  - Acceptance A1 ~ A6 도 전부 백엔드 · 배포 확인이라 공개 페이지가 걸릴 자리가 없다.
  - 공개 페이지가 막는 것은 prod 배포가 아니라 앱 심사 제출이다(60-release §7-2 #1 「막는 것」 = 심사 제출).
- 그래서 `--plan` / `--apply` 둘 다 돌리지 않았다. #243 은 지금도 v2 · `delivery-plan:review`(2026-11-11T11:25:13Z 이후 변경 없음).
- 공개 페이지 작업을 Delivery 로 묶을지(새 Delivery · 또는 #245 같은 웹 Delivery 에 넣을지)는 코디가 정할 일이다.

### 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · 263 warning · `products/day` 0.

### 코디 확인 필요

- 60-release #1 「담당」 칸은 아직 「서버 코디」다. 실제로는 frontend(fe-3)가 만드니 바꿀지 정해 달라 — 지시에 없어 손대지 않았다.
- 60-release :39 · :40 · :60 · :146 · :147 의 「아직 열리지 않음 / 502」는 지금도 사실이라 그대로 뒀다.
