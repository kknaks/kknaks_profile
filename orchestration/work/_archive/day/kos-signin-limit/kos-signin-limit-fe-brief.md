
# [frontend] KOS 기기 제한 — 웹 기기 선택 단계(U-4)

너는 **day `frontend` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리에서 동시에 작업한다** — 서로의 파일을 건드리지 마라. §3 계약이 경계다. base = origin/dev `0c401726`.

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

- `backend/day/routers/login.py`(`POST /login` · `POST /login/hospital` · 오류 조각) · 웹 로그인 템플릿(병원 고르기 조각 — 같은 틀로) · `backend/day/static/` · `backend/day/styles/` · 화면 글자 근거 표 `backend/tests/architecture/test_screen_copy.py` · 웹 화면 테스트 `backend/tests/day/web/`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/login.py` · `backend/day/templates/`(로그인 관련) · `backend/day/static/` · `backend/day/styles/` · `backend/tests/day/web/` · `backend/tests/architecture/test_screen_copy.py`(근거 표 추가만)

## 6. 구현 단계

1. `POST /login` 이 `choose_device` 결과면 **기기 선택 조각**(U-4 · 로그인 카드 자리 · 병원 고르기와 같은 틀 · DS 컴포넌트) — 글자는 스펙 「화면 글자」 표 그대로: 제목 「이미 로그인 중인 기기가 있습니다」 · 안내 두 줄 · 라디오 카드(1줄 `label · ip_address` · 2줄 상대 시각 「n분 전」 · 「방금 전」) · 처음 선택 첫 항목 · 버튼 「계속하기」 · **「처음으로」 없음**.
2. `POST /login/device`(폼 `pending_token` 숨은 칸 · `device_id` 라디오) → `auth.choose_device` → `POST /login` 과 같은 갈래(이동 · 병원 고르기 조각 · 새 기기 선택 조각 · 오류). CSRF 없음(스펙).
3. 비밀번호 · 이메일은 조각 · 숨은 칸 · URL 어디에도 없음(grep 테스트).
4. 화면 테스트 · 글자 근거 표.

## 7. 범위 제약 — 하지 말 것

- 서비스 · emr · dto · api 라우터 수정 금지(backend 몫 — §3 이름 그대로 부른다 · 아직 없으면 가짜로 테스트하고 리포트에). 글자 발명 금지 · 손 CSS 0 · 인라인 스크립트 0. 커밋 · 사용자 포트 · 로컬 스택 금지.

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/fe-1-report.md` — 변경 파일 · §3 계약 준수 · 테스트 수치 · 상대 몫 · E2E 에서 만날 자리.
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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
