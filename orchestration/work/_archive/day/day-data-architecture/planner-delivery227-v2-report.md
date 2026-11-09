# planner-delivery227-v2 결과 보고 — Delivery #227 로그인 재계약(contract v2)

## 상태: done (human gate 에서 멈춤 · 승인 안 함)

## 수행

- 요청 `delivery/v2-login.json` 을 contract v2 로 다시 썼다(v1 사본 = `delivery/v2-login.v1.json`).
- `start-delivery` 스킬 절차 그대로: 이 워크트리 `tools/harness` `mediness start-delivery --mediness-repo ../.. --code-repo <CENTURION_DAY v2-dev 로컬 clone(8e4fb4b5)> --github-repo MediSolveAIDev/CENTURION_DAY` — `--plan`(`delivery/v2-login.v2.plan.json`) → `--apply`(`delivery/v2-login.v2.apply.json`).
- mediness origin/main = `d93b921013af517570b9c04bd14a0668650f4887`(CLI 요구 — 최신 fetch 값). 워크트리의 미커밋 SPEC-002 변경은 건드리지 않았다.

## Issue 갱신 확인

- [MediSolveAIDev/CENTURION_DAY#227](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/227) — **같은 Issue 갱신**(apply `issue_number: 227` · idempotency `day/v2-login` 를 가진 Issue 는 #227 하나 · 새 Issue 없음). 본문 updatedAt 2026-11-06T01:27Z.
- 메타: `contract_version=2` · `target_specs` = DAY-SPEC-000 · **DAY-SPEC-001** · `missing_target_specs` 둘 다(pending).
- 라벨 그대로: `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`. status `scope-delta-recorded` · `next_action = review-delivery-plan`(human_gate). **승인 receipt 는 보내지 않았다.**
- **plan_digest(v2) = `sha256:7656c2aad09ddffad21b05bd85fdc5264b2aa8cc07e9eb86f07f32b8ad94eb3a`** (v1 `sha256:30c1c98b…` 은 stale). contract_digest `sha256:27b87b9e…6c3f`.
- 주의: GitHub Issue **제목은 CLI 가 바꾸지 않았다**(v1 제목 그대로 · 본문 「목표」 줄은 v2 제목). 제목을 맞추려면 코디가 `gh issue edit` — 나는 하지 않았다.

## 바뀐 계약 항목 (전 → 후)

| 항목 | v1 | v2 |
|---|---|---|
| target_specs | DAY-SPEC-000 | DAY-SPEC-000 · **DAY-SPEC-001** |
| spec_baseline | a6f7460 · pending | d93b921 · pending(PR #909 미머지) |
| 위험 | L3 | L3(유지) |
| 제목(목표) | 로그인 — KOS sign-in 으로 … | 로그인 · 세션 — … (DAY-SPEC-001) |
| scope_delta | 없음 | v1 → v2 사유 11개(아래 Target Delta 변화 요약 + v1 열린 것 2개가 SPEC-001 로 닫힘) |
| Target Delta | 흐름 · 비밀번호 저장 안 함 · external_ref · 브라우저 헤더 · 병원 자동 고르기 (5) | API 4경로 · 흐름(연결 병원 · dev is_demo · 임시 토큰 5분 · 이전 세션 유지) · 세션 전달(day_session 쿠키 httpOnly/Lax/Secure/CSRF + Bearer · 무작위 토큰 + token_hash) · 만료(= KOS 토큰 만료 · KOS 401 → expires_at 당김 · 로그아웃 KOS 안 알림) · 비밀번호/토큰 · 막는 경우(mfa · 비활성 계정/직원) · 오류 매트릭스 11 · 권한(행 없으면 forbidden) · 헤더 + 15초 · **이미 있음 — 재사용(PR #228: kos client · 헤더 · login_session/external_session 모델 · crypto)** (10) |
| Acceptance | A1 ~ A5 | A1 ~ A10 — 단일 병원 로그인 · 여러 병원 + 임시 토큰 · 비밀번호/암호화/token_hash · 오류 11경우 · 만료와 KOS 401 당김 · 로그아웃 · 쿠키 + CSRF · dev is_demo · /me + forbidden · 헤더 + 15초 |
| Non-Goals | 화면 · 시술 현황 · 알림 · prod · 로그인 화면 디자인 · **2단계 인증 — 하지 않음** · permission_key · 본사/관리자 화면 | 화면 · 본사 · 관리자 로그인(1차 밖) · **2단계 인증 「지원」만 제외 — 막고 안내는 Target** · permission_key · 병원 바꾸기 · KOS 로그아웃 알림 · 형식 검사 · **직원 토큰으로 KOS 쓰기(outbox 발송)** · 시술 현황 · 알림 · prod |
| Review Surface | baseline pending · L3 근거 · 「API 계약용 SPEC 필요?」 · 「재로그인 정책」 · 차단 위험 | baseline pending · **v1 승인 stale → 재승인 필요** · L3 근거 · 차단 위험 · CSRF 실패 오류 코드 SPEC-001 에 없음 · 웹이 JSON /api/auth 를 쓰는 것과 AGENTS.md routers/ · routers/api/ 구조 · 재사용 시 시스템 계정 토큰과 섞이지 않게 |
| Execution | 5 phase · fixture/PG/dev 확인 | code surface(auth router · services · session.py · kos client 재사용 + get-user-tenants) · 의존 #225 · #226(PR #228) · 5 phase · 매트릭스 테스트 · predeploy(ENCRYPTION_KEY · HTTPS) · open question = CSRF 코드 |

SPEC-001 에 없는 것은 넣지 않았다. 「재사용」 칸은 PR #228 브랜치 파일(`backend/day/emr/kos/client.py` · `backend/day/models/staff.py` · `backend/common/crypto.py`)과 #226 리포트로 확인했다. `get-user-tenants` 는 #226 client 에 없어 「더한다」로 적었다.

## 다음 (사용자)

1. #227 결과 계약 v2 를 읽고 승인 → receipt `{"decision":"approved","reviewer_type":"human","reviewer":"<사람>","plan_digest":"sha256:7656c2aad09ddffad21b05bd85fdc5264b2aa8cc07e9eb86f07f32b8ad94eb3a"}` 로 같은 request 재실행.
2. PR #909 머지 뒤 같은 key · contract_version 3 · 새 origin/main 으로 baseline ready.
3. Review Surface 의 CSRF 오류 코드 — SPEC-001 개정 여부.
