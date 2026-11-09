# 작업 요약 — day-data-architecture (day)

기간: `2026-11-03` ~ `2026-11-09`
결과: 머지 · dev 배포까지 — 코드 PR #228 → `dev`(91728737) · 스펙 PR #909 → `main`(b4cd1a00) · https://day-dev.medisolveai.com 가동(데모 지점 KOS 동기화). prod 는 다음 작업.

## 1. 무엇을 했나

회사 CRM DAY 를 옛 v0.1 코드(rc.14) 위가 아니라 빈 브랜치에서 다시 지었다. 데스크는 KOS 를 그대로 쓰고
시술실 · 의국만 DAY 를 쓰는 1차 범위로, 데이터 모델(51 테이블) → KOS 폴링 · outbox 쓰기 → 로그인(KOS 직원
sign-in) → 웹 기반(Jinja2 + HTMX + medikit) → 시술 현황 화면 → 서버 배포를 스펙 → Delivery → 코드 순서로
단계마다 리뷰를 붙여 쌓았다. 끝에 레포 브랜치를 `dev` · `prod` · `archive` 로 정리하고, Azure VM 한 대에
GitHub Actions · ACR · Key Vault 로 첫 dev 배포를 올렸다.

## 2. 적용한 기술·개념

- **외부 CRM 폴링 + outbox 쓰기(KOS)** — DAY 가 KOS 를 10초 회차로 읽고, DAY 에서 누른 동작은 `external_outbox` 에 쌓아 KOS 로 쓴다 [[external-write-queue]] · [[polling]]
  - 왜 이걸 골랐나: KOS 는 웹훅이 없고, 데스크가 KOS 를 계속 쓰므로 원천은 KOS 다. 직접 쓰기는 실패 시 화면 · KOS 가 어긋나서 큐로 뺐다
  - 무엇이 어려웠나: 같은 행을 두 worker 가 보내는 중복 · SENT 에서 멈춘 행 → 보내기 전 claim · 오래된 SENT 는 실패로. 쓰기 토큰은 시스템 계정이 아니라 **누른 직원의 토큰**(`sender_staff_id`)이어야 KOS 에 「누가」가 남는다. 화면 반응이 느려 즉시 kick(상한 1초)을 더했다
  - 근거: `8c85233a`(#226) · `4c2cebab` · `292d0996` · SPEC-002 ⑥⑦ · 원천 `screen/procedure-board-decisions.md` 「KOS 쓰기」
- **KOS 내부 API 브라우저 헤더** — 내부 API 는 브라우저 UA · Origin · 단계별 `kos-client-uri` 가 없으면 403 [[public-vs-internal-api]]
  - 무엇이 어려웠나: 공개 API 로 안 되는 쓰기는 HAR 에서 경로 · 값 모양만 베꼈다(값은 안 베낌). HAR 로 확인된 쓰기만 열고, cc 근거 쓰기는 데모 연결에서만 연다(`KOS_TRIAL_WRITES_ON_LIVE=false`)
  - 근거: cc-prototype `77173cf` · SPEC-001 개정 · #227
- **부분 유일 인덱스(soft delete)** — 유일은 살아 있는 행만(`WHERE deleted_at IS NULL`) [[unique-key]]
  - 무엇이 어려웠나: upsert 의 `ON CONFLICT` 에 같은 `WHERE` 를 반복해야 인덱스를 찾는다
  - 근거: `b6f23b42`(#225) · SPEC-000 동기화
- **서버 렌더 웹(Jinja2 + HTMX + SSE)** — 웹은 HTML 조각 라우트, JSON `/api/*` 는 앱 전용. CSRF 는 centurion admin 방식 [[server-rendered-fragments]]
  - 왜 이걸 골랐나: 앱(Flutter)과 웹이 같은 JSON 을 쓰려다 화면 상태 · 권한 표시가 서버에 있는 게 단순해서 갈랐다
  - 근거: `9c7376ca`(#229 · #232) · `3cbb2e08` · 원천 `erd/04-staff.md`
- **router → service → repository + DB 없는 단위 테스트** — 기본 실행은 DB 없이(`-m "not infra"` 수 초), 실제 DB · Redis 는 `infra` 표식으로 갈라 전체 실행에서만 [[layered-architecture]] · [[test-tiering]]
  - 근거: `ec2a2681`(#224) · roles backend/reviewer rules 「테스트 나누기」
- **한 VM 두 환경 배포(GitHub OIDC · ACR · run-command · Key Vault)** — `dev` push → 빌드 · 배포 · migration 자동, `prod` 는 fast-forward 로만 → 다시 빌드 안 하고 dev 에서 성공한 같은 digest 만 [[ci-cd]] · [[workload-identity]]
  - 왜 이걸 골랐나: 장기 키 없이(OIDC) · SSH 없이(run-command) · 비밀은 Key Vault. prod 를 merge/squash 로 올리면 커밋이 달라져 「같은 이미지」가 깨진다
  - 무엇이 어려웠나: 같은 concurrency group 대기 실행이 취소됨 → 워크플로별 group + VM flock. 실패 복구가 두 판 전 이미지로 내려가던 것 → 배포 직전 스냅샷만으로
  - 근거: `937dbb68` · `1ccc101b`(#233) · mediness `40-architecture/deployment.md`
- **asyncpg TLS verify-full** — libpq 의 `sslmode=verify-full` 이 asyncpg 에선 안 먹는다 [[database-tls-verification]] · [[dev-prod-parity]]
  - 무엇이 어려웠나: 문서대로 넣으면 TypeError / CA 파일 없음 → `?ssl=verify-full` + `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt` + 시작 때 검사. 터널로 실제 DB 에 앱 코드 경로 그대로 1회 연결해 확인
  - 근거: #233 검수 H1 · `937dbb68`
- **Azure managed identity · Key Vault 방화벽** — VM 은 system identity 로 ACR pull · KV 읽기, Key Vault 는 VM 서브넷만 허용이라 비밀을 넣을 땐 로컬 IP 를 잠깐 열고 바로 닫는다 [[workload-identity]] · [[secret-store]]
  - 근거: `day.json` `infra.azure` · `_RESUME.md` 2026-11-09

## 3. 막혔던 것 / 사고

- 스펙 없이 Delivery 를 먼저 열었다(#224~#227) → 사용자 「스펙도 없는데 wp를 만든거야?」 → SPEC 먼저 닫고 Delivery 재결속. #227 은 SPEC-001 뒤 계약 다시
- 단계 끝에 리뷰를 안 붙임(#226) · 리뷰 PASS 알림을 놓침(#229) → 사용자 지적 → 「단계 done = 같은 턴에 reviewer」 규칙화
- 화면에 시안 · 스펙에 없는 문구를 지어 넣음 → 사용자 질책 → 문구 걷기(`8f26612f`) + frontend · designer rules 「지어 넣지 않는다」 + 화면 검수 항목
- 견본 페이지에 실제 지점 이름이 박힘(#229 F1) → 검수가 잡음 → 제거 + 레포 실명 금지 테스트
- 「방 있는 시술만 판에」를 「간호사가 방 배정」으로 잘못 연결 → 방 배정은 데스크(코디)가 KOS 에서 — 지금 규칙 유지
- cc 의 쓰기 토큰을 「누른 사람」으로 잘못 전제 → cc 는 시스템 계정이었음 → DAY 는 누른 사람 토큰으로(`sender_staff_id` · migration 0005) 결정
- 배포 문서대로면 DB 연결 실패(asyncpg verify-full) → 코드 검수 H1 → 실제 DB 로 확인하고 고침
- 코디가 설계(ACR)를 두고 수동 · SSH 배포를 다시 제안 → 사용자 「설계에 ACR 쓰는데 왜 수동」 → 설계대로 구현
- KOS 주소를 레포 env 에 둠 → 사용자 「kos 꺼는 env 에 노출하면 안 돼」 → Key Vault 로(이미 커밋된 기록은 그대로 — 사용자)
- DB 관리자 env 파일이 profile 레포 안에 gitignore 없이 놓임 → 바로 무시 목록 · 600 · 이후 `~/.pgpass` 로 옮기고 원본 삭제
- 코디가 영어로 답함(여러 번) → 사용자 질책 → 메모리 「답은 언제나 한국어」

## 4. 결정

`_RESUME.md` §2 표가 정본(2026-11-03 ~ 11-06) — 그 뒤 굵은 것만 더한다.

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-05 | 코드 PR 은 #228 하나 — 화면까지 다 만들 때까지 · 구현 먼저 머지는 나중 | 사용자 |
| 2026-11-06 | 웹 = 화면 라우트 HTML 조각 · JSON 은 앱 전용 · CSRF centurion admin 방식 | 사용자(원천 04-staff) |
| 2026-11-06 | 시술 현황 U1 ~ U12 · 다시 호출 = cc D-25~27(마지막 호출이 유효 · 이전 수락 무효) | 사용자(원천 procedure-board-decisions) |
| 2026-11-06 | 쓰기 = 누른 직원 토큰 · 바로 보내기(상한 1초) | 사용자 · 코디 OQ-21 |
| 2026-11-08 | 기본 권한 표(직무별 board 보기 · 수정 · 수락 — 수락은 간호사 · 원장) · 전체 권한 = env `DAY_ADMIN_EMAILS` | 사용자 |
| 2026-11-08 | 브랜치 정리: `dev`(v2 · 기본) · `prod` · `archive`(옛 코드) + 옛 브랜치 끝 태그 19 | 사용자 |
| 2026-11-08 | 배포: Caddy · dev/prod 한 VM · PG 한 대(스키마 둘) · 도메인 day-dev / day · 나머지 조사 추천 | 사용자 |
| 2026-11-09 | 앱 계정 = 스키마 주인 · migration 도 앱 계정 · NSG 80/443 공개 · KOS 주소 = Key Vault · 첫 배포는 dev(데모 테넌트)만 | 사용자 |
| ~~2026-11-05~~ | ~~Delivery 를 SPEC 머지 전에 연다~~ → 11-05 SPEC 먼저 | 사용자 지적 |

## 5. 날짜별 로그

- `2026-11-03` 테이블 설계 01~07 확정 · `products/day` 스캐폴드 · SPEC-000 · PR #909
- `2026-11-05` 40-architecture · SPEC-001 로그인 · Delivery #224~#227 · #224 뼈대 · #225 데이터 모델(51 테이블)
- `2026-11-06` #226 KOS 연동 · #227 로그인 · #229 웹 기반 · #232 로그인 화면 · SPEC-002 · #230/#231 시술 현황 · 화면 피드백 F1~F19 · 데모 지점 실물 KOS 쓰기 확인
- `2026-11-08` 기본 권한 표 · 문구 걷기 · 모바일 배포 문서 · 서버 배포 결정 · CENTURION_DAY 브랜치 정리 · deployment.md · #233 계약
- `2026-11-09` VM · DB 받음 · 스키마 · 계정 · docker · Azure 권한 · DNS · #233 배포 구현 · KOS 주소 Key Vault · #228 → dev 머지 · **첫 dev 배포** · #909 → main 머지

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/909 (squash `b4cd1a00`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/228 (squash `91728737` → `dev`) · Delivery #224~#233 닫음

- `kknaksss/day-data-architecture-spec` → `main`
  - `60c020dd` Merge branch 'main' into kknaksss/day-data-architecture-spec
  - `bf8ef79f` docs(day): 첫 dev 배포 완료 반영 — 상태 · 준비 표 · 미결
  - `8dc78d98` docs(day): deployment.md — KOS 주소 = Key Vault · 환경당 비밀 6 · dev 먼저
  - `b46351a8` docs(day): deployment.md — #233 구현 · 실제 Azure 에 맞춤(ssl · OIDC environment · KV 비밀 · 권한 · NSG · DNS 준비됨)
  - `05c6b731` docs(day): deployment.md — 받은 서버 · DB 반영 · 스키마 생성 권한 닫음(앱 계정 = 스키마 주인)
  - `48132fae` docs(day): 40-architecture/deployment.md — dev · prod 한 VM 배포 구조(Caddy · ACR · Key Vault · 브랜치 dev/prod · prod fast-forward · 롤백 · migration 순서)
  - `f7a1ba4e` docs(day): 모바일 배포 구조 검수 보정 및 변경 이력
  - `2ac50899` docs(day): 40-architecture 모바일 배포 구조(초안) — iOS · Android 빌드 · 서명 · 비공개 배포
  - `42dd8a08` docs(day): SPEC-001 · SPEC-002 ⑪ — 화면 문구 근거(병원 선택 · 처음으로 · 로그인 브랜드 · 오류 토스트 16+1)
  - `95185ea5` docs(day): SPEC-002 ⑩ 권한 이름 표 · SPEC-001 시드 문장 범위(전체 권한 계정만)
  - `79d6cb82` docs(day): SPEC-002 ⑨ — 시술 현황 1차 기본 권한 표(사용자 2026-11-08)
  - `c55b5082` docs(day): SPEC-002 ⑧ — 의사 호출 · 재호출 · 수락 창 = 버튼 아래 팝오버(사용자 F1)
  - `bad75654` docs(day): SPEC-002 개정 ⑥⑦ — 화면 확인 피드백(다시 호출 cc D-25~27 · 줄 순서 · 귀가 대기 판에서 빠짐 · 필터/보기 뺌 · 국적 · 누른 사람 토큰 · 귀가 대기/취소 KOS 쓰기) · SPEC-000 external_outbox.sender_staff_id
  - `ec973c11` docs(day): SPEC-001 전체 권한 계정(env DAY_ADMIN_EMAILS) — 사용자 2026-11-06
  - `af8fd568` docs(day): SPEC-001 웹 화면 절(화면 라우트 · 문구 13줄 · 숨은 폼 칸) · SPEC-002 W6(HAR 미확인 쓰기 닫음)
  - `c908ed1f` docs(day): DAY-SPEC-002 시술 현황(1차 · 웹) + SPEC-001 개정(CSRF · 빈 입력 · kos-client-uri) + SPEC-000 동기화
  - `f835531f` docs(day): SPEC-000 동기화 — 유일은 살아 있는 행만 · direct_key 병원별 · #225 구현이 정한 FK 대상 · 코드 테이블 타입
  - `e3ee7e99` docs(day): DAY-SPEC-001 로그인 · 세션 + SPEC-000 login_session.token_hash
  - `a9adf55a` docs(day): DB 스키마 = env(DB_SCHEMA day_dev / day_prod) · KOS 내부 API 브라우저 헤더 위험
  - `7af03178` docs(day): 40-architecture — 시스템 런타임(api · worker · scheduler · Redis · interval 폴링) · 코드 구조 요약
  - `53a93afb` docs(day): log PR 칸 #909
  - `52c50013` docs(day): DAY 제품 스캐폴드 + DAY-SPEC-000 데이터 모델 · 40-architecture
- `kknaksss/day-data-architecture` → `dev`
  - `fdc2345f` chore(deploy): dev 관리자 이메일(로컬과 같은 값)
  - `1ccc101b` feat(deploy): KOS 주소를 레포 env 에서 빼고 Key Vault 로 (#233)
  - `937dbb68` feat(deploy): DAY 서버 배포 — dev · prod 한 VM (#233)
  - `8f26612f` fix: 시술 현황 · 로그인 화면 — 지어 넣은 문구 걷기 · 시안 글자로 (#231 · #232)
  - `34ac05b9` feat: 시술 현황 1차 기본 권한 — 직무별 board 보기 · 수정 · 수락 채우기 (#230)
  - `e5912d2b` feat: 시술 현황 화면 — 호출 뒤 선택 해제 · 종료 뒤 더보기 가드 · 카드 D&D (#231)
  - `292d0996` fix: 시술 현황 피드백 검수 반영 — 바로 보내기 상한 · 다시 호출 확인 · day.js 판 해시 (#230 · #231)
  - `4c2cebab` feat: DAY v2 시술 현황 — 사용자 화면 피드백 반영 (#230 · #231)
  - `3cbb2e08` feat: DAY v2 시술 현황 1차 — 백엔드 · 화면 (#230 · #231)
  - `9c7376ca` feat: DAY v2 웹 기반 — medikit HTMX 컴포넌트 · 웹 로그인 화면 (#229 · #232)
  - `fb2508e4` feat: DAY v2 로그인 · 세션 — KOS 직원 sign-in · 쿠키/Bearer · CSRF (#227)
  - `8c85233a` feat: DAY v2 KOS 연동 — 폴링 · external_ref · outbox 기반 (#226)
  - `b6f23b42` feat: DAY v2 데이터 모델 — 1차 51 테이블 · 첫 migration (#225)
  - `ec2a2681` feat: DAY v2 백엔드 뼈대 — api · worker · scheduler · DB_SCHEMA · 경계 테스트 (#224)
- 리포트: `review-*-report.md`(단계별 검수) · `researcher-deploy-report.md` · `board-feedback.md`(F1~F21)

## 7. 잔여

- **prod 배포**: Key Vault prod 비밀 6 · `prod` fast-forward · prod migration 승인 · 운영 KOS 나가는 IP 확인 · `KOS_TRIAL_WRITES_ON_LIVE` 는 false 로 시작
- GitHub Environments `dev`/`prod` 배포 브랜치 제한 걸기(관리자 — 사용자)
- dev 화면 눈 확인(사용자) · 실측 메모리로 compose 상한 다시
- 시작 취소(`PROCEDURE_WAITING`) KOS 쓰기 실물 미확인
- 다음 스펙: 방 옮기기 · 차트 작성(HAR 뒤)
- F20 의사 계정 수락 = 본인(앱 · 기기 구분 정할 때) · QA 역할(Playwright) 다듬기
- 정본 클론 `~/git/CENTURION_DAY` = `dev` · `deploy/local.env` 여기 · `day-local` 은 내려 둠(볼륨 남음)

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/day-data-architecture/README|day-data-architecture]]
<!-- work-links:end -->
