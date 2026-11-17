
# [backend] KOS 기기 제한 — UA 표시 · 시스템 자동 해제 · 직원 기기 선택 서비스

너는 **day `backend` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라. §3 계약이 경계다. base = origin/dev `0c401726`.

## 1. SSOT — 먼저 읽을 것

- **스펙(계약 SoT · 미커밋 — 절대경로로 읽어라)**: `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec/products/day/20-spec/spec-001-login-session.md` **개정 ⑨ + 보충**(머리 :42 · :44 · U-1 · U-3 · **U-4 기기 선택** :97- · 화면 라우트 :112- · 흐름 :127- · 화면 글자 :144- · 케이스 매트릭스 :168- · S-7 :234 · **S-8 시스템 계정** :243 · API · 응답 :292-293 · §3 「KOS 동시 로그인 제한」 · 「기기 선택 동안 비밀번호」 · §5 「기기 제한 — 정할 것」) · `spec-003-mobile-app.md` ⑱ · `spec-000-data-model.md`(`KOS_CLIENT_TAG`). 줄 번호는 근처 grep. 「기본값」 꼬리표 값이 계약이다.
- **고정(사용자 2026-11-17 · 스펙 어느 줄과 달라도 우선)**: 앱 JSON 로그인(`POST /api/auth/login`)은 기기 제한이어도 **지금과 똑같이 401 `invalid_credentials`**(새 코드 `kos_signin_limit` 쓰지 않음 · 깔린 앱 화면 그대로 · 서버 로그에만 기기 제한 표시). 스펙 OQ-K17 은 이 값으로 고치는 중(spec-3).
- 결정 · 사실: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/_RESUME.md` §2 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-spec-brief.md` §1(KOS 사실) · 앞 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-0-findings.md` · 초안 패치(참고만 · 그대로 쓰지 말고 스펙에 맞춰) `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-0-draft.patch`.
- 코드 레포 `AGENTS.md`.

기대는 개념: [[external-api-error-classification]] — 같은 401 을 본문 사유로 가른다.

## 2. 배경

KOS 가 계정당 동시 로그인 5개로 막는다. 스펙대로: 공통 판정 · 목록 · 해제 · 재 sign-in / 시스템 계정 UA 환경 표시 + 막혔을 때 같은 UA 가장 오래된 1개 자동 해제 / 직원 웹 기기 선택 단계 / 앱은 지금 그대로. **배포는 나중** — 구현 · 테스트까지.

## 3. 계약 (be ↔ fe — 이 이름 그대로)

- `services/auth.py` `login(...)` 이 기기 제한이면 결과 `status="choose_device"` + `pending_token` · `expires_in_seconds` · `devices: [{id, label, ip_address, signed_in_at}]`(스펙 :292) — 웹 service 결과 dto 로만(JSON 응답 아님).
- `services/auth.py` `choose_device(session, deps, pending_token: str, device_id: str) -> LoginOutcome` — 해제 → sign-in 다시 → 이후 `login` 과 같은 갈래(세션 발급 · `choose_hospital` · 다시 막히면 새 `choose_device`). 토큰 종류 다름 · 만료 · 잘못된 device_id → `SessionExpired`(`session_expired`).
- `label` 만들기(UA → 「macOS Chrome」 등) 는 be(서비스 쪽 함수) · 상대 시각 글자는 fe(화면).
- 앱 `POST /api/auth/login` = 기기 제한이면 401 `invalid_credentials`(위 고정).

## 4. 먼저 읽을 핵심 파일

- `backend/day/emr/kos/client.py`(:39 `WEB_USER_AGENT` · :150 `internal_headers` · :206 `internal_token` · :266 401 재발급) · `staff_client.py`(:60-100) · `services/auth.py`(:82 · :186 · :234 · :263) · pending 보관 · `encrypt_value` 위치 · `routers/api/` auth · `common/config.py` · `deploy/local.env.example` · `deploy/compose*.yaml`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/` 중 `day/emr/` · `day/services/` · `day/dtos/` · `day/errors.py` · `day/routers/api/` · `common/` · `backend/tests/`(웹 화면 테스트 제외)
- `deploy/local.env.example` · `deploy/compose*.yaml`(env 전달만)

## 6. 구현 단계

1. `KOS_CLIENT_TAG` 설정 + UA 조립(세 곳 공용) · 비면 지금과 같음.
2. KOS 공통: `SignInLimitExceeded` 판정 · 목록 · 해제(`kos-client-uri` = `<web>/auth/active-sign-in-limit` — 스펙 사실).
3. 시스템 계정(S-8): `internal_token` 막힘 → 태그 있으면 같은 UA 가장 오래된 1개 해제 → 재시도 1회 · 태그 없으면 정리 없이 실패 + 경고 · 해제 4xx 면 로그만 · 무한 반복 없음.
4. 직원 웹(S-7 · U-4): `login` 의 `choose_device` 결과 · 비밀번호는 스펙 §3 「기기 선택 동안 비밀번호」대로(암호화 · Redis 5분 · 꺼내면 지움 · 종류 표시) · `choose_device` 서비스 · 토큰 종류 구분(W-1 — 병원 고르기 토큰과 섞이면 `session_expired`).
5. 앱 JSON 로그인 = 401 `invalid_credentials`(고정) · 데모 넘김(`services/environments.py`) 영향 없음 확인.
6. 테스트(가짜 KOS): UA 태그 · 시스템 막힘 → 같은 UA 가장 오래된 1개만 · 사람/다른 환경 UA 안 건드림 · 재시도 1회 · 직원 막힘 → choose_device · 비밀번호가 결과 · 로그에 없음 · choose_device 성공/만료/잘못된 id/다시 막힘 · 병원 고르기 토큰과 섞임 · 앱 = invalid_credentials · 틀린 비밀번호 = 기존 그대로.

## 7. 범위 제약 — 하지 말 것

- 웹 라우트(`routers/login.py`) · 템플릿 · static · styles · `app/` 수정 금지(frontend 몫 / 범위 밖). migration 금지.
- KOS 실호출 금지 · 커밋 · push · PR 금지 · 사용자 포트 · 프로세스 · 로컬 스택 금지. 비밀번호 · 이메일 · 토큰을 로그 · 리포트에 쓰지 마라.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- infra 테스트가 있으면: `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q <파일>`(스키마 day_test · 컨테이너 건드리지 마라).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-1-report.md` — 변경 파일 · 계약(설정 이름 · 오류 코드 · 함수) · 테스트 수치 · 앱 영향 판정 · 배포 때 서버 env 에 넣을 값.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
