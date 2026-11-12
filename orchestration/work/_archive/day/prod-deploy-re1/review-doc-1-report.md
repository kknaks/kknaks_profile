# 리뷰 리포트 — prod-deploy-re1 / doc (2026-11-11)

대상: mediness 워크트리 `prod-deploy-re1-spec` 미커밋 diff(`products/day/20-spec/spec-000-data-model.md` · `40-architecture/deployment.md` · `log.md`) + Delivery CENTURION_DAY#243(본문 · 라벨 · hidden metadata).
대조: 코드 워크트리 `CENTURION_DAY/prod-deploy-re1`(HEAD 7b099e8f + 코디 미커밋 `deploy/config/prod.env`) · GitHub 레포 실물(`gh api` 읽기만) · 코디 실물 확인(브리프 §2).

## 판정: WARN

FAIL 없음. 스펙 개정은 사용자 결정(2026-11-11) 범위 안이고 결정에 없는 정책을 새로 넣지 않았다. 다만 **prod 첫 배포 절차가 레포 실물 · 코디 실물과 세 군데 어긋난다**(KOS IP · `prod` 브랜치 · GitHub Environment `prod`). 이 세 곳은 스펙 PR 전에 고치는 것을 권한다. Delivery #243 은 v1 을 승인하지 말고, 스펙 PR 머지 뒤 v2 로 다시 묶어서 승인하는 게 맞다(W4).

검증 수치
- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning. `products/day/` 에 걸린 항목은 **0**이고, 나머지 WARN 은 모두 다른 제품(selly 등)에 원래 있던 것이라 이번 변경과 무관하다.
- 비밀값 스캔: diff 와 Issue #243 본문 · metadata 에 이메일 · PEM · 키 모양 문자열 **0**. prod.env 값은 출력하지 않고 일치 여부만 불리언으로 확인했다.

## FAIL

없음.

## WARN

### W1. KOS IP 허용: 「확인 안 함」이라고 적혀 있지만 이미 **필요하다고 확인됐다**
- 위치
  - `products/day/40-architecture/deployment.md:252`(미결 「KOS IP 제한」: 「나가는 IP 허용 목록 여부는 확인 안 함 … 막히면 허용 요청 방법은 그때 정함」)
  - `:221`(절차 7: 「등록 뒤 첫 동기화가 되는지(나가는 IP 허용 여부 …)」)
  - Issue #243 「검토할 부분」 4번째 줄과 「아직 결정이 필요한 것」 2번째 줄(metadata `review_surface.3` · `open_questions.1`)
- 근거: 코디 실물 확인(2026-11-11). VM 의 나가는 IP 로 운영 KOS **내부 API** 를 부르면 403 `IPBlocked` 가 돌아온다. 로그인과 open API 는 된다.
- 영향: 절차대로 하면 6(운영 연결 등록)까지 끝낸 뒤 7에서 동기화가 막힌다. Issue A6(「첫 동기화」)은 IP 허용 없이 끝낼 수 없다.
- 고칠 문장
  - `:252` 행:
    `| KOS IP 제한 | **필요(2026-11-11 코디 실측)** — 운영 KOS 내부 API 가 VM 나가는 IP 에서 403 `IPBlocked`(로그인 · open API 는 됨). 브라우저 UA 차단은 별도(system.md 「위험」) | 사용자 — KOS 쪽에 VM 나가는 IP 허용 요청 · prod 첫 배포 절차 6 전 |`
  - 절차 표에 6 앞 단계 추가:
    `| 5-1 | **운영 KOS IP 허용** — KOS 쪽에 VM 나가는 IP 허용 요청(운영 내부 API 가 403 `IPBlocked` — 2026-11-11 실측) | 사용자 | 요청 전 |`
  - 7은 이렇게: 「등록 뒤 첫 동기화가 되는지(IP 허용 반영 확인) · 운영 테넌트 응답 모양(OQ-01-3)」
  - Issue: `open_questions.1` 은 지우고, 「배포 전 확인」에 「운영 KOS IP 허용(사용자 · A6 의 전제)」을 넣는다.

### W2. 절차 4의 「`prod` 브랜치가 없으면」 분기가 실물과 다르다. 브랜치는 이미 있고, 그 브랜치에 워크플로 파일이 없다
- 위치: `deployment.md:218`
- 근거
  - `git ls-remote origin refs/heads/prod` → `8e4fb4b5`(dev 에 포함된 옛 commit 「docs: AGENTS.md …」)
  - `git ls-tree 8e4fb4b5 .github/workflows/` → 비어 있음
  - `migrate-prod.yaml` 은 `workflow_dispatch` 이고 `if: github.ref == 'refs/heads/prod'` 조건이 붙어 있다. 그래서 prod ref 에 이 파일이 없으면 「prod 브랜치에서 실행」을 할 수 없다.
- 정리: 「없으면 만든다」 분기는 타지 않는다. 먼저 fast-forward push 를 해야 한다. `8e4fb4b5` 가 새 SHA 의 조상이므로 `check_promotion` 의 fast-forward 검사(`scripts/deploy/day-deploy.sh:222-223`)는 통과한다.
- 고칠 문장(4): `**migrate-prod** — `prod` 브랜치는 이미 있다(옛 commit · 워크플로 파일 없음 — 2026-11-11 확인). 먼저 `git push origin <sha>:prod`(fast-forward)로 워크플로 파일을 prod 에 올린다 — 그 push 의 deploy-prod 는 DB 가 head 가 아니라 멈춘다(정상). 그 뒤 migrate-prod 를 `prod` 브랜치에서 수동 실행(입력 SHA · 확인 문자열 `migrate day_prod`).`
- 레포 `docs/development/deployment.md:129-131` 도 같은 분기로 적혀 있다. 그쪽 수정은 코드 PR 범위(Issue `code_surface.5`)에 같이 넣으면 된다.

### W3. GitHub Environment `prod` 가 없다. 그런데 준비 표에는 「생김」이라고 적혀 있다
- 위치: `deployment.md:236`(「`dev` · `prod` … **생김(2026-11-09)** — 워크플로 첫 실행 때 자동 생성」). 이번 diff 가 바꾼 줄은 아니지만, 새로 쓴 절차가 이 행을 전제로 한다.
- 근거
  - `gh api repos/MediSolveAIDev/CENTURION_DAY/environments` → `dev` 만 있고 `prod` 는 없다. 나머지는 Vercel Preview/Production 이다.
  - 코디 실물: 레포 권한이 부족해 `prod` 를 못 만들었고, 승인 규칙도 없다.
  - Actions 변수 8개는 레포 단위에 있다(`gh api …/actions/variables`). 그래서 첫 prod 워크플로 실행 때 Environment 가 자동으로 생겨도 변수는 읽힌다.
- 영향(L3 근거와 연결됨): migrate-prod 는 「따로 승인해서 실행」하도록 주석이 달려 있다. 지금 실제로 막아 주는 장치는 확인 문자열 · dev 배포 이력 · dev DB head 검사뿐이고, 사람 승인 단계는 없다.
- 고칠 문장(`:236` 상태 칸): `**dev 만 생김(2026-11-09 · 첫 실행 때 자동)** · **prod 없음** — 레포 권한 부족으로 미리 못 만듦(2026-11-11 코디) · 첫 prod 워크플로 실행 때 자동 생성 예상(그때 확인) · 승인자 규칙 없음 → migrate-prod 의 막는 장치 = 확인 문자열 · dev 배포 이력 · dev DB head 검사뿐. 남음: 배포 브랜치 제한 · 승인 규칙(권한 · plan)`
- 절차 4 아래 메모: 「GitHub Environment `prod` 는 첫 prod 워크플로 실행 때 생긴다(승인 규칙 없음).」

### W4. Delivery #243 v1 의 baseline 이 OQ-01-2 를 닫기 **전** 스펙에 묶여 있는데 `spec-baseline:ready` 로 붙어 있다
- 위치: Issue 라벨 `spec-baseline:ready` · metadata `spec_baseline_revision=7f7319ec…` · `contract.spec_baseline_state=ready`
- 근거: `7f7319ec` 의 SPEC-000 §6 에서 OQ-01-2 는 아직 「prod 배포 때 정한다」로 열려 있다(이번 diff 의 `-` 줄). Target Delta 1 은 개정 ④(미커밋)를 근거로 삼는다. planner 도 Review Surface 1에서 이 점을 인정했다.
- 고칠 것: v1 의 plan_digest 를 승인하지 않는다. 순서는 이렇게 간다.
  1. 스펙 PR 을 머지한다.
  2. 같은 key 를 `contract_version 2` 로, 새 `origin/main` revision 에 다시 묶는다.
  3. 사용자가 v2 의 plan_digest 를 승인한다.

  Issue 본문 「다음 단계」에 「스펙 PR 머지 → v2 재결속 뒤 승인」 한 줄을 더하는 게 좋다.

### W5. Issue Non-Goal 「계정 이메일을 레포에 두지 않는다」가 의존성 「prod.env 를 같은 코드 PR 에 넣는다」와 부딪친다
- 위치: Issue 「이번에 하지 않는 것」 6번째 줄(`non_goals.5`), 「의존성」 2번째 줄(`dependencies.1`)
- 근거: 코디의 미커밋 `deploy/config/prod.env` 에서 `DAY_DEMO_LOGIN_EMAILS` 와 `DAY_ADMIN_EMAILS` 값이 비어 있지 않고 `@` 를 포함한다(각 1개 · 값은 출력하지 않음). 이 파일은 코드 PR 로 레포(비공개)에 들어간다. dev.env 에 이미 같은 선례가 있다. SPEC-000 `:1384` 는 이 값들을 「`prod.env` … 값은 이 문서에 안 적음」으로 적었고, 이것은 맞다.
- 고칠 문장(`non_goals.5`): `운영 연결 값(KOS open API 키 · 테넌트 · 시스템 계정 이메일 · 비밀번호 · 「방 배정」 id)을 레포 · 문서 · Issue 에 두기 — 서버 일반 설정 prod.env 의 데모 · 전체 권한 계정(비공개 레포 · 기존 dev.env 와 같은 방식)은 예외`

### W6. env 표의 `DAY_ADMIN_EMAILS` prod 칸만 「채움」으로 바뀌지 않았다
- 위치: `deployment.md:162`(prod 칸 「비움 또는 실제 관리자」 그대로)
- 근거: `git show HEAD:deploy/config/prod.env` 에서는 `DAY_ADMIN_EMAILS` 가 EMPTY 였고, 지금 워크트리에서는 SET 이다. 리포트와 log 에는 「env 표 prod 칸 채움 사실 반영」이라고 적혀 있지만 이 행은 빠졌다.
- 고칠 문장(prod 칸): `**채움**(2026-11-11 · `prod.env` · 값은 안 적음)`

## Delivery #243: 확인 결과

- **Target Delta**: 브리프의 두 건(운영 등록 진입점, prod 설정 계약 시험)과 스펙 개정, 이렇게 세 항목이다. 범위가 넘치거나 빠진 곳은 없다. 함수 이름 정정(`day.public.seed_demo_kos_connection` → `services/crm_connections.ensure_demo_connection`)은 코드와 같다(`backend/day/services/crm_connections.py:85` · `backend/day/public.py:37`).
- **Non-Goals**: migration · 공개 API · 웹 · 앱 · prod 배포 실행 · CRM 설정 화면 · Vegas · OQ-01-3 이 들어 있고 적절하다. 다만 5번은 W5 를 볼 것.
- **Acceptance**
  - A1~A5 는 구현 워커가 시험 · 명령으로 확인할 수 있다.
  - A4 의 「여섯 조건」은 Target Delta 2 의 여섯 항목과 수가 맞는다. prod.env 로 실제 맞는지도 확인했다(허용 앱 = `day.medisolveai` · 공개 주소 = prod · 데모 넘김 = dev 공개 주소 · `blob` · 컨테이너 `prod` · Key ID 와 Team ID 둘 다 SET → 모두 True).
  - A6 은 Delivery 밖이라고 적혀 있어 괜찮다. 다만 KOS IP 허용이 전제다(W1).
- **risk L3**: 근거가 타당하다. 운영 DB 에 실제 병원 접속값을 쓰는 새 길이 생기고, 데모 · 운영 동작을 가르지 않으니(`spec-000:235-237`) 즉시 실 KOS 동기화 · 쓰기로 이어진다. 여기에 W3 의 「prod 승인 규칙 없음」을 L3 근거 옆에 적어 두길 권한다.
- **열어 둔 질문 세 개 중 기본값으로 닫을 수 있는 것**
  1. **데모 연결 이름이 겹칠 때** → 기본값 **거절**로 닫을 수 있다. 0 이 아닌 종료 · 쓰기 0 · 메시지에 비밀값 없음.
     - 근거: SPEC-000 `:235-236` 「prod 스키마에는 실제 병원 연결만」. prod 에서 `is_demo=true` 연결을 만났다면 잘못된 스키마나 잘못된 값이라는 신호다.
     - 반대 방향 위험도 있다. `ensure_demo_connection`(`crm_connections.py:131-138`)은 같은 브랜드 코드 · 병원 이름의 기존 연결을 찾으면 `is_demo=True` 로 덮는다. 운영 진입점이 이 함수를 인자만 바꿔 재사용하면 같은 덮기 동작을 물려받는다. 거절을 A1~A2 옆 시험으로 박는 걸 권한다.
  2. **모듈 이름 · env 이름** → 사용자가 판단할 일이 아니다. 구현 워커가 정해 PR 에 적으면 된다. 참고로 데모 시드는 `DAY_SEED_*`(`scripts/seed_demo_connection.py:23-34`)를 쓰고, deployment.md 는 「`DAY_SEED_*` 는 배포 env 에 넣지 않는다」고 한다. 그래서 운영 진입점은 `DAY_SEED_*` 를 재사용하지 말고 다른 접두를 쓰는 편이 혼동이 적다(제안).
  3. **KOS IP 허용 필요 여부** → **닫힘**(필요 · W1).
- **비밀값**: 본문 · metadata 에 키 · 비밀번호 · 계정 이메일 · 병원 실명이 없다. 브랜드 코드 `ceramique` 는 사용자가 정한 값이다.

## 스펙 개정: 사용자 결정과 대조 (PASS)

- `spec-000:31`(개정 ④ 메모) · `:189`(`is_demo` — 운영 등록은 false) · `:205`(「방 배정」 prod 값 = 등록 때 연결 설정) · `:238`(「환경」) · `:1383-1384`(OQ-01-2 닫음)
  - 사용자 결정 다섯 가지와 같다: 운영용 등록 진입점 · `is_demo=false` · prod api 컨테이너 안 · 값은 레포 밖 · `ceramique` · 실제 병원 1곳.
  - 「`backend` 안 모듈(`python -m`)」은 레포 사실에서 따라 나온 것이다(`deploy/Dockerfile` 이 `COPY backend ./backend` 만 하고 `scripts/` 는 없다).
  - 칸 · 타입 · migration 변경이 없고 `status: stable` · `version` 도 그대로다. 문서 파이프라인 규칙에 맞다.
- 열린 것을 닫은 곳은 없다. OQ-01-1 · OQ-01-3 은 열린 채로 남아 있다.
- `deployment.md:223`(첫 배포에는 연결이 없어 `encryption` 확인이 지나간다)은 코드와 같다(`crm_connections.py:158-165` docstring 「연결이 하나도 없으면(첫 배포) 풀 것이 없어 지나간다」).
- 절차 1(Key Vault 필수 6 + 선택 2)은 `scripts/deploy/day_vm.py:35-52`(`SECRETS` 6 · `OPTIONAL_SECRETS` 2)와 같다. 코디 실물(8개 넣음 · `validate_secrets` 통과)과도 같다.
- 절차 5 · 3은 워크플로(`deploy-prod.yaml` check-promotion → require-image → remote deploy → check-public · `migrate-prod.yaml` 확인 문자열 · dev 이력)와 레포 문서 「첫 배포 절차」 2~5와 같다. 4만 W2 가 걸린다.

## 직원이 실물에서 만날 자리

- 운영 연결을 등록한 뒤 KOS IP 허용이 반영되기 전까지 prod 동기화가 403 으로 실패한다. 직원 앱 · 웹의 시술 현황 · 고객이 비어 보인다(W1). 허용 요청을 등록 **전에** 넣어야 첫 화면이 빈 채로 보이지 않는다.

## 참고(기존 부채 · 사소)

- `log.md:17` 종류 `decision-add`: 이번 변경에 ESC 는 없다(`10-decision.md` 무변경). 규칙상 `decision-add` 는 ESC 용이고, day 의 기존 OQ 닫기 행들은 `spec-change` 로 적었다. 제안: `spec-change, arch-change`. lint 는 통과한다.
- `deployment.md:170` Soniox 행의 「배포 스크립트 선택 비밀 목록에 한 줄 더함(구현 때)」는 이미 구현돼 있다(`day_vm.py:51`). 이번 diff 밖의 낡은 문장이다.
- 「사용자가 1회」의 「사용자가」(`spec-000:1384` · 절차 6 「누가」)는 사용자 결정 원문(「prod api 컨테이너 안에서」)에 주어가 없다. 실행 주체를 사용자에게 확인하거나 「사용자 · 코디」로 두는 걸 권한다.
- 같은 진입점을 **dev** api 컨테이너에서 잘못 돌리면 실제 병원 접속값이 `day_dev` 에 들어간다. 그러면 dev 가 실제 병원을 동기화하게 되고, SPEC-000 `:233-235` 「dev 가 실제 병원을 건드리지 않는 근거 = 데이터」가 깨진다. 등록 진입점에 `DB_SCHEMA`/`APP_ENV` 확인 가드를 둘지는 사용자 판단 사항이다(SPEC 의 「코드는 APP_ENV 로 연결을 거르지 않는다」는 동기화 대상 이야기라 등록 가드와는 다르다). 정책이라 리뷰어가 정하지 않는다. Issue 「구현 때 정할 것」에 한 줄 추가를 권한다.
- 값을 `docker exec -e` 로 넘기면 VM 셸 기록에 남는다. 비밀(KOS 비밀번호 · 키)은 표준입력(`docker exec -i`)으로 받는 쪽이 안전하다. 진입점 설계 때 참고.
