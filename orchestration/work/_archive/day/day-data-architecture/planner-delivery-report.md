# day 백엔드 Delivery 시작 + PR #909 보정 — 결과 보고

## 상태: done (human gate 에서 멈춤)

## A. PR #909 보정

워크트리 `mediness-mediness/day-data-architecture-spec` · `products/day/` 만. 커밋 · push 안 함(코디가 함).

| 파일:줄 | 고친 것 |
|---|---|
| `products/day/20-spec/spec-000-data-model.md:86` | §2 공통 규칙 「DB」 행 — 원천 README 를 다시 생성기로 옮김: 「`day` 스키마」 → **스키마 이름은 env(`DB_SCHEMA` — dev `day_dev` / prod `day_prod`)** (2026-11-05). 재생성 diff 는 이 1줄뿐 |
| `products/day/40-architecture/system.md:32` | 토폴로지 DB 노드 「day 스키마」 → 「DB 1개 · 스키마 DB_SCHEMA」 |
| 같은 파일 :54 | DB 줄 → 「스키마 이름은 env `DB_SCHEMA`」 |
| 같은 파일 :65 | 런타임 표 PostgreSQL 행 → 1대 · DB 1개 · `DB_SCHEMA` · 새 DB 권한 없음 |
| 같은 파일 「DB · 환경 분리」 새 절(:69-76) | system 원천 결정 7 · 8 — DB 1개 · 스키마로 env 분리 · `MetaData(schema)` · `version_table_schema` · `search_path` · 스키마별 DB 계정 · dev 먼저 → prod 같은 migration · 지금은 dev 만(로컬 compose 도 같은 방식) |
| 같은 파일 「서버」 표 | 요청할 것 — 관리형 PostgreSQL(1대 · DB 1개 — 확정 2026-11-05) |
| 같은 파일 「로그인」(:178) | sign-in 은 내부 API 라 브라우저 헤더 필요 → 위험 절 링크 |
| 같은 파일 「외부 통합」 KOS 행(:201) | 내부 API 브라우저 헤더 필수 |
| 같은 파일 :206 「위험 — KOS 내부 API 차단」 새 절 | 2026-11-03 18:23 KST 부터 비브라우저 UA 403 · cc-prototype 헤더(User-Agent · Origin · `kos-client-uri`)로 해결 · DAY 로그인 · 일정 · 쓰기 전부 해당 · 공식 API 이전 후보 |
| `products/day/40-architecture/code-structure.md:50` | 「테이블은 `day` 스키마」 → env `DB_SCHEMA` 스키마 + system.md 링크 |
| `products/day/log.md:17` | 2026-11-05 `spec-change, arch-change` · DAY-SPEC-000 · #909 한 줄 |

`grep "day 스키마"` → products/day 0건.

lint: `python3 scripts/lint-pipeline.py --strict` → **0 error, 263 warning** · products/day ERROR 0 · WARN 0(263 은 타 제품 기존 — 무관).

## B. Delivery Issue 4개 (MediSolveAIDev/CENTURION_DAY)

절차: `start-delivery` Skill · `rules/delivery-workflow.md` · harness README · `references/requests.md` 그대로. CLI = 이 워크트리 `tools/harness` 의 `mediness start-delivery --mediness-repo . --code-repo <CENTURION_DAY v2-dev 임시 로컬 clone> --github-repo MediSolveAIDev/CENTURION_DAY`, `--plan` 으로 4개 검증 뒤 `--apply`. 기준 Mediness `origin/main` = `a6f7460720fcc6c2130421840733f82edcdb5c09`, 코드 = `v2-dev` `8e4fb4b5`(AGENTS.md · CLAUDE.md 만 있음).

| # | Issue | idempotency key | 위험 | 근거 |
|---|---|---|---|---|
| 1 | [#224 백엔드 뼈대](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/224) | `day/v2-backend-skeleton` | **L2** | 새 골격 · 설정 · 헬스체크 경로 · task 자리 — CENTURION_DAY AGENTS.md 상 외부 계약(API 경로 · task name)이 처음 생겨 독립 검토 가치. 데이터 migration · 외부 write · 배포 없음 → L3 아님 |
| 2 | [#225 데이터 모델](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/225) | `day/v2-data-model` | **L3** | 첫 schema migration(delivery-workflow: migration = L3), 이후 전부의 기반 |
| 3 | [#226 KOS 연동 기반](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/226) | `day/v2-kos-sync` | **L3** | 외부 시스템 연동 · credential(데모 지점 키) 사용 · external_outbox 외부 write 경로 |
| 4 | [#227 로그인](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/227) | `day/v2-login` | **L3** | 인증 · 쿠키 계약(AGENTS.md 외부 계약) · 직원 KOS 토큰 저장 · 외부 sign-in 호출 |

각 Issue: target `DAY-SPEC-000` · Target Delta · Acceptance(A1~) · Non-Goals(공통: 화면 · 시술 현황 동작 · 알림/채팅 · prod 배포 + 각자) · Review Surface(위험 근거 포함) · Execution(code surface · phases · verification · rollback — preflight 근거만) · 의존(2→1, 3→2, 4→2·3 — execution.dependencies). KOS 키 · 토큰 · 테넌트 id · 실명 없음.

### 현재 상태 (4개 모두 같음)

- 라벨: `spec-baseline:pending` · `delivery-plan:review` · `execution-plan:ready`
- `next_action`: **`review-delivery-plan`** (skill `start-delivery`, when `human-approved`, human_gate true) — 여기서 멈춤. 구현 · Code PR 없음.
- Task projection: `blocked — delivery-plan-review-required`(승인 전이라 정상).
- plan_digest(승인 receipt 에 쓰는 값):
  - #224 `sha256:4210536e42bf65aafacf24c503d28fa8e8d01f0f3e4e5bcb2f33cc526514267c`
  - #225 `sha256:75620f99e6e8b843d23a302ca8d03a511bb8c44c0fdae2e77c58c91fa9150297`
  - #226 `sha256:afde60cd5c4e2c92f0cf7b132a04f48c3c70507b85dbab9a1e67e355eaa9bd95`
  - #227 `sha256:30c1c98b5cbef0f33adacabba2558bdf8696683378222fde759b3ca7edb6b3b7`

### 다음 순서

1. **사용자(담당자 1인)가 각 Issue 의 결과 계약을 읽고 승인** → receipt `{"decision":"approved","reviewer_type":"human","reviewer":"<사람>","plan_digest":"<위 값>"}` 로 같은 request 를 `--plan-approval-receipt` 와 함께 재실행 → `delivery-plan:approved`.
2. PR #909 머지 뒤 같은 key · `contract_version` 2 · 새 `origin/main` revision 으로 재실행 → `spec-baseline:ready`(결과 계약 의미가 같으면 재승인 없음). 이 순서는 1 과 바뀌어도 된다. 둘 다 끝나면 `implement-and-open-code-pr`.
3. 구현은 의존 순서(#224 → #225 → #226 → #227).

request JSON 4개는 재실행용으로 scratchpad 에 있다: `…/scratchpad/delivery/v2-*.json`(코디가 쓰려면 kknaks_profile work 폴더로 옮기는 것을 권장).

## 사용자에게 받을 결정

1. **4개 결과 계약 승인**(위 1). 특히 위험 등급 L2 / L3 / L3 / L3 이 맞는지.
2. #224 — CENTURION_DAY `AGENTS.md`(v2-dev)가 아직 `schema="day"` · 「테이블은 `day` 스키마」다. DB_SCHEMA 결정에 맞게 이 Delivery 에서 함께 고칠지.
3. #225 — `visit_requested_procedure` · `consultation_procedure` 의 `product_option_id` 가 SPEC 상 FK 인데 1차에 `product_option` 테이블이 없다: 1차는 FK 없이 칸만 둘지. 열린 enum(gender · display_request.kind · id_photo.doc_type 등) 처리. 07(칸 검토 전 · ESC-001 법적 검토 미회신) 테이블을 그대로 만들지.
4. #226 — external_outbox 를 이번에 실제 KOS(데모)로 발송해 볼지, 기반만 두고 첫 실제 쓰기를 시술 현황으로 미룰지. 공식 API 이전 범위.
5. #227 — 로그인 API 경로 · 쿠키 · 오류 계약이 처음 생기는데 SPEC-000 은 데이터 계약뿐 — 로그인 API 용 SPEC 을 따로 둘지. 재로그인 정책.
6. Python 3.13 · uv(발주 지정)가 centurion 고정 버전과 다르면 그대로 갈지.

## 주의

- CENTURION_DAY 기본 checkout(`/Users/kknaks/git/CENTURION_DAY`)은 `stg` 라 건드리지 않고, `v2-dev` 를 scratchpad 로 로컬 clone 해 `--code-repo` 로 썼다(원본 repo 변경 없음).
- CLI 가 CENTURION_DAY 에 라벨(`spec-baseline:pending` 등)을 새로 만들었을 수 있다(harness 동작).
- harness README 「알려진 제약」(#749): 대장이 제품 레포 · 문서 PR 이 mediness 라 나중 `spec-sync --apply` 가 문서 PR 을 못 찾는다 — closeout 때 코디 처리 필요.
- `30-work.md` Delivery dashboard(marker 안)는 손대지 않았다 — `dashboard-sync` 는 spec-sync 단계 몫.
