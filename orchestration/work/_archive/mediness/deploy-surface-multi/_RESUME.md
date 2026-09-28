
# 재개 노트 — deploy-surface-multi (mediness)

**지금**: **PR 둘 다 올라갔다 — spec #762 · code #151.** 검수 PASS, 1루프 끝. **사용자 리뷰·머지 대기.**
**다음**: 사용자 리뷰·머지 → `log.md` PR 번호 backfill(`—` → #762) → **사용자 E2E → 2루프**(관찰 6건, WP §Open Issues 에 한 목록).

세팅: `scripts/new-work.sh mediness deploy-surface-multi` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/mediness-app/deploy-surface-multi` (branch `kknaksss/deploy-surface-multi`, base `origin/dev` → PR `dev`). **BE·FE 가 같은 트리를 공유** — `back/` ⟂ `front/` 로만 갈린다

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec` (branch `kknaksss/deploy-surface-multi-spec`, base `origin/mediness` → PR `mediness`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] **사용자 리뷰·머지 대기** — spec #762(커밋 `0dc89a9b`·`a0675ffc`) · code #151(커밋 `0d12fcfc`). 상호 링크됨
- [!] **머지 후 `log.md` PR 번호 backfill** — 현재 `—` → #762. 잊기 쉬운 자리
- [!] **2루프가 남아 있다** — 사용자 E2E 후. 재료는 `work-131` §Open Issues 에 모아 둠(관찰 6건)
- [ ] 머지 후 `archive-work.sh mediness deploy-surface-multi --dry-run` → SUMMARY → 개념 소화
- [x] ~~frontend~~ 완료·통과 (터미널은 사망, 변경은 워크트리에 살아 있음 — **`front/` 건드리면 날아간다**)
- [x] ~~backend Phase 1~5~~ 완료·통과
- [ ] `reviewer_code` 검수 → code PR(base `dev`)
- [!] **머지 후 `log.md` PR 번호 backfill** — spec PR #762 번호로. 현재 `—`. 잊기 쉬운 자리
- [!] **2루프가 남아 있다** — 1루프는 계약대로 세우는 판. 사용자 E2E 뒤 눈으로 보고 고치는 판이 따로 온다(FE 관찰 O-1~O-3)
- [!] **코디handle 이 세 번 바뀌었다.** 현재 `term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1`. **발주마다 `terminal list` 로 재확인** — env·`_RESUME` 둘 다 못 믿는다
- [ ] reviewer_spec 검수 → 사용자 스펙 리뷰
- [ ] (그 뒤) WP 작성 발주 → work-131 예정 · 그 뒤 BE/FE 구현 발주
- [!] **코디handle 이 세션 중 두 번 바뀌었다.** 현재 산 핸들 = `term_6fcc58f6-73d0-4baf-be0d-e066a76cf5d1` (세션 초엔 `term_f2659c81…` 이었다가 재연결로 되돌아옴). **발주할 때마다 `orca terminal list` 로 제목 보고 다시 확인할 것** — env 도 `_RESUME` 도 믿지 마라. 브리프 전부 갱신 완료.

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-22 | 모델 = **별 행**. 유니크 키 `(product_slug, environment, surface_key)` 로 확장 | 사용자 지시. surfaces JSONB 배열·별도 surface 테이블은 검토 후 탈락 |
| 2026-09-22 | 시연계정은 **surface 행마다** — `demo_accounts` shape 불변 | 사용자 지시. 행=surface 라 현행 구조가 그대로 맞음 |
| 2026-09-22 | `surface_key` = **자유 입력** 문자열 (enum 아님) | 사용자 지시. 제품마다 surface 종류가 달라 enum 은 다음 제품에서 또 막힌다 |
| 2026-09-22 | 이번 범위 = **구조까지**. nexus 실데이터 6건은 배포 후 모달 입력 | 사용자 지시. 비번 평문 git 미박제 원칙(SPEC-051 §4 축2)과도 정합 |
| 2026-09-22 | 기존 8개 seed 행은 `surface_key` 기본값 1개로 백필 — 데이터 무손실 | 사용자 지시 |
| 2026-09-22 | 백필 기본값 = `기본`. **sentinel 아님** — `/gm` surface 표기는 값이 아니라 **그룹 행 수 2건 이상**으로 판정 | planner 제안, 코디 승인. 기존 단일 surface 제품 출력 회귀 0 |
| 2026-09-22 | `surface_key` 는 PATCH 로 개명 가능. `product_slug`·`environment` 는 불변 | planner 제안, 코디 승인. 삭제·재생성 강요 시 그 행 시연계정 유실 |
| 2026-09-22 | `surface_key` NOT NULL 이 계약 · 길이 50자 · trim 만 정규화(대소문자 안 접음) · GET surface 필터 미도입 · `/gm` 인자 2토큰 유지 | planner 제안, 코디 승인 |
| 2026-09-22 | OQ-1 은 **규칙 불변, 데이터 현황만 갱신** — 홈페이지가 `nexus` 로 카탈로그 등재되어 규칙상 자동 포함 | planner 판단, 코디 승인. 결정을 다시 연 것이 아님 |
| 2026-09-22 | `21-html` 시안 동기화를 **이번 판에 포함** (기본값 통보, 되묻지 않음) | 시안이 FE 의 SoT 라 구 모델이 남으면 FE 판이 구 모델을 구현한다 |
| 2026-09-22 | 모달 신규 행 surface 입력 = **빈 값 + placeholder**. `기본` 프리필 폐기 | planner 자진 신고. 그룹에 이미 `기본` 행이 있어 프리필이 **항상 409** 를 부른다. 빈값 저장은 400 — 「이름을 지어라」가 맞는 실패 |
| 2026-09-22 | `기본` 은 **백필 값 하나로만** 존재 — 프리필도 sentinel 도 아님 | 위 결정의 따름 |
| 2026-09-22 | 모달 구조 = **평평 카드 + (환경,surface) 정렬**. 스펙의 중첩 와이어프레임을 시안으로 내림 | 확정 시안이 정본. 코디가 2차에 「새 컴포넌트 발명 금지」를 건 결과가 평평이고 그 판단을 유지 |
| 2026-09-22 | 시안에 `demo` 환경 누락·저장행 환경 select 두 건도 시안 쪽으로 정합 | planner 2차 판단, 코디 승인. 실 FE `envChipClass`/`deployEnvLabel` 값 그대로 |
| 2026-09-22 | **환경 표시 정렬 = `prod → stg → dev → demo`**. `ENVS`(select 순서)와 `envOrder`(표시)를 분리 | 검수 W-1. 시안이 dev 먼저라 charty 모달이 뒤집히는 회귀 |
| 2026-09-22 | 시안 say-admin 행의 계정을 **비운다**(`accts:[]` + 「가상 예시」) | 검수 W-2. 지어낸 계정이 사실로 읽힐 위험. `spec-051:476` 사정거리는 안 넓힌다 |
| 2026-09-22 | [기본정보] 블록 요약도 **`/gm` 과 같은 규칙** — 행 1건이면 surface 생략 | 검수 W-3. 「회귀 0」이 한 화면만 예외면 반쪽 |
| 2026-09-22 | `surface_key` 길이 상한 **50자를 계약으로 확정**(「권장」 삭제) | 검수 W-6. 케이스 매트릭스·AC 가 이미 강제 중이라 절반씩이었다 |
| 2026-09-22 | **trim 한 값을 저장한다** — 앱 정규화 값이 곧 DB 유니크가 보는 값 | 검수 W-12. 원문 저장 시 `기본` vs `기본␣` 가 둘 다 통과해 유니크가 샌다 |
| 2026-09-22 | 시연계정 있는 행 **삭제에 확인 단계**를 계약에 넣는다 | 검수 O-4. 행 삭제 = 그 표면 시연계정 전부 소멸인데 방어가 없었다 |
| 2026-09-22 | `30-work.md` Spec Coverage SPEC-051 **`done` → `in_dev`** (derive WARN 은 의도된 신호) | 검수 W-13. 계약이 커버 WP 를 앞질렀다. 같은 파일 SPEC-030 에 동일 선례 |
| 2026-09-22 | frontmatter `version: 0.0.3` **유지 — 조치 없음** | 검수 W-10. mediness 엔 `00-baseline/planning/` 이 없고 최근 SPEC 3건이 0.0.3. 관행을 따른다 |
| 2026-09-22 | ~~다음 판은 WP 파일이 아니라 Delivery Issue~~ → **WP 파일(work-131)로 간다** | 2026-09-22 사용자 지시로 뒤집힘. 규칙(`document-pipeline.md:10`)은 Delivery Issue 이나, **WP 는 같은 PR 에서 스펙과 동시 리뷰되고 Issue 는 안 된다** — 「한번에 리뷰」 요구에 WP 가 맞다. 규칙 예외임을 WP §메타에 명시 |
| 2026-09-22 | WP Phase 5(pytest 회귀)만 **IN_PROGRESS**, 나머지 7개 DONE · frontmatter `in_dev` | 권한 테스트 12건이 환경 탓에 초록을 못 봐 Pre-deploy 이월. WP-129·130 선례. **`done` 은 머지·배포 후** |
| 2026-09-22 | **대시보드 배포 링크는 「결정적으로만」** — 카드는 환경당 1개 유지, `기본` 우선·없으면 surface 오름차순 첫째 | 사용자 지시. `db_source.py:134` 가 2축 dict 라 6행 중 1개만 남고 **어느 게 남는지 비결정적**이었다. 「대표 surface」 신설은 스펙 판으로 남김 |
| 2026-09-22 | migration = **`0139_deployment_surface_key`**(head `0138_task_body_refs`) | BE 실측. WP 의 `0124`/`0125` 는 planner 가 **canonical 피처 브랜치**에서 읽어 stale 이었다. **alembic head 는 워크트리 base 에서 재확인한다** |
| 2026-09-22 | FE 삭제 확인은 시안의 `confirm()` 이 아니라 레포 `useConfirm()` | FE 판단·코디 승인. WKWebView 는 `confirm()` 이 **항상 false** — 시안대로면 데스크톱에서 삭제가 죽는다. 시안이 정본이라는 규칙의 정당한 예외 |
| 2026-09-22 | 확인된 사실: Harness v1 규칙 도입 **2026-08-31(#648)**, 마지막 WP 생성 **2026-09-01** — 이후 3주 신규 0 | 규칙이 실제로 살아 있다는 근거. 예외 판단의 전제 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner(1~4차) | `term_c1552692…` **DEAD** | `task_d475e5d986f0` | `ctx_dde2df90a01c` | `…-spec-brief.md` + 추가지시 3건 | 완료·통과 (터미널 사망) |
| backend | `term_201334b3-620b-4b5d-b969-f4c7e9837a87` | `task_f819aa2897ad` | `ctx_737cb8708035` | `…-be-brief.md` + `be-dashboard-instructions.md` | **전부 완료·통과** |
| reviewer_code | `term_031286fc-0499-4bcf-988f-e4d787c5a1fb` | `task_e22605506fa6` | `ctx_24411b244345` | `…-review-code-brief.md` | 완료 — **PASS**(FAIL 0·WARN 4·관찰 5) |
| code-fix | `term_6caf0195-f54d-4b50-ac72-a2b4c4c57893` | `task_b1b38488f797` | `ctx_ee25a0dfa645` | `code-fix-brief.md` | **완료·통과** |
| frontend | `term_44462bf6…` **DEAD** | `task_06b9d3b7ed53` | `ctx_051d8ce02747` | `…-fe-brief.md` | **완료·통과** |
| planner | `term_3a4cc1ce-2b87-4f61-ae01-b7252cfc2c50` | `task_6d3d6f6ac216` | `ctx_69b48865a491` | 브리프 + 추가지시 4건(`wp-fix` 포함) | **전부 완료·통과** |
| reviewer_spec | `term_855499b4-966c-4283-86f6-d2478f77f501` | `task_cd8d00d50f7e` | `ctx_af8867b6b0f6` | `…-review-spec-brief.md` | 완료 — **WARN**(FAIL 0·경미 14) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- **spec PR: https://github.com/MediSolveAIDev/mediness/pull/762** — 커밋 `0dc89a9b`(5파일 567+/103−) + `a0675ffc`(WP 정정·Phase 상태)
- **code PR: https://github.com/MediSolveAIDev/mediness-app/pull/151** — 커밋 `0d12fcfc`, 24파일 2122+/154−
- `review-code-report.md` (192줄) — **PASS**. WARN 4 중 잠복버그 4건은 PR 안에서 닫음. 관찰 5건은 2루프 이월
- **`flaky-baseline-evidence.md`** — BE 12 failed 판정(환경·무관). 교차 확인 = 무접촉 파일이 같은 사유로 9/11 실패. **재조사 금지**
- 리포트: `planner-report.md` (1~8차) · `review-spec-report.md` (330줄, WARN 판정)
- **확정 산출물 5파일**(미커밋, 워크트리 `deploy-surface-multi-spec`): `spec-051`(+212/−64) · `21-html/Product Management.html`(+126/−32) · **`30-work/work-131-deploy-surface-axis.md`(신규 325줄, doc_no 254)** · `30-work.md`(3표 등재 + Spec Coverage `in_dev`) · `log.md`(1행)
- **최종 검증(코디 직접)**: lint 0 error/263 warning(기준선) · `node --check` 통과 · `doc_no 254` 전역 유일 · `commitDeploys` 6케이스 독립 재현 · AC 16건↔Phase 대응 구멍 0
- **FE 판으로 넘길 관찰(O-1~O-3)**: prod 칩 6회 반복의 시각 위계 · 백필 `기본` 을 운영자가 처음 만나는 순간 안내 · 빈 surface 를 제출 전 인라인으로 알릴지 사후 400 으로 둘지. Delivery Issue 가 받아야 한다
- 변경(미커밋): `spec-051-…md` (+128/−64, 3차로 더 늘어남) · `log.md` (+1) · `21-html/Product Management.html` (+71/−32)
- 커밋: (아직)

## 5. 이력 (최신이 위)

- `2026-09-22` **1루프 종료 — PR 둘 올림(spec #762 · code #151).** reviewer_code PASS, 잠복버그 4건 + FE 테스트 5건을 PR 안에서 닫음.
- `2026-09-22` BE·FE 1루프 완료·코디 검증 통과. BE 가 찾은 대시보드 2축 dict 구멍에 사용자 결정 → BE·planner 추가 판 발주.
- `2026-09-22` **spec PR #762 올림** → BE·FE 구현 병렬 발주. pre-commit lint 0 error 통과, rebase 불필요(0 behind/0 ahead).
- `2026-09-22` **5파일 확정** — WP-131 + log `wp-add` 결합까지 완료. 사용자 리뷰 대기.
- `2026-09-22` lint 264→263 — WP-131 이 Spec Coverage covering 에 들어가 derive 가 `in_dev` 로 일치. **신호가 불일치 WARN(대리물)에서 실제 WP 행(본체)으로 옮겨간 것**이라 옳은 소멸. 되돌리지 않는다.
- `2026-09-22` 수정판 통과(코디 재검증: lint 264·commitDeploys 6케이스 독립 재현·정렬 회귀 해소) → **사용자 지시로 WP 작성 발주**(Delivery Issue 대신, 동시 리뷰 목적).
- `2026-09-22` **코디handle 세 번째 변경** `term_738cfbd7…` → `term_6fcc58f6…`. 브리프 전부 갱신.
- `2026-09-22` reviewer_spec WARN(14건) → 수정판 발주. **코디 오류 1건 정정** — 다음 판을 「WP work-131」이라 했으나 Harness v1 은 `30-work/work-NNN` 을 만들지 않고 Delivery Issue 를 쓴다(`rules/document-pipeline.md:10`). planner 가 WP 를 안 만든 것이 옳았다.
- `2026-09-22` **코디handle 이 또 바뀌었다** — `term_f2659c81…` → `term_738cfbd7…`(세션 초 env 값으로 되돌아감). 리뷰어가 preamble 값으로 보내 살았다. 브리프 전부 갱신. **발주마다 `terminal list` 로 재확인한다.**
- `2026-09-22` planner 3·4차 통과 → reviewer_spec 발주. **코디 오판 1건** — 3차 지시서에서 「시안은 이미 빈 값」이라 판정했으나 템플릿 기본값만 보고 호출부 `surface:'기본'` 을 놓쳤다. planner 가 범위를 지키며 보고해 4차로 정정. 검수 브리프 §2 에 「판 넷은 코디 책임」을 명시.
- `2026-09-22` planner 2차 통과 — 코디 재검증(lint 0 error·JS 문법·유니크 가정 grep 잔존 0). 워커가 **자기 문장의 약점을 자진 신고**(`기본` 프리필이 항상 409) → 3차 발주로 스펙을 시안에 맞춤.
- `2026-09-22` planner 1차 통과 — 코디가 `lint --strict` 직접 1회(0 error), allowed_paths·옛 2축 표현 grep 전수 확인. 워커가 보고한 ②(21-html 구 모델 잔존)를 받아 2차 발주.
- `2026-09-22` planner 발주 — 터미널 생성·브리프 §9 핸들 치환·task-create·dispatch·주입 확인까지 완료.
- `2026-09-22` 코디 세션 시작 — 런북·SPEC-051·코드 현황 조사, 사용자와 모델 결정 4건 확정, planner 브리프 작성. 발주 승인 대기.
- `2026-09-22` `$ORCA_TERMINAL_HANDLE` stale 발견 — `terminal list` 제목으로 산 핸들 확인해 브리프에 반영.

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
