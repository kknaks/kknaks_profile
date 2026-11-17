
# [planner] KOS 로그인 기기 5대 제한 — SPEC 개정 · Delivery 발행

너는 **day `planner` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 (2026-11-17 · 이 표가 정본)

| # | 결정 |
|---|---|
| K-1 공통 | KOS sign-in 이 401 `SignInLimitExceeded` 면 활성 로그인 목록 → 하나(또는 여럿) 해제 → sign-in 다시. 틀린 비밀번호(같은 401 `InvalidRequestException`)와 본문 `message` 로 가른다 |
| K-2 시스템 계정 | KOS 요청 User-Agent 끝에 환경 표시 ` (local)` / ` (dev)` / ` (prod)` — 새 설정 `KOS_CLIENT_TAG`(`APP_ENV` 쓰지 않음 — 로컬도 `APP_ENV=dev`). **막혔을 때만**(매번 아님 — 사용자 「하루 한두 번 · 매번 삭제는 부담」) UA 가 정확히 같은(=같은 환경) 이전 세션을 자동 해제 후 재시도 1회. 표시가 비면 자동 정리 안 함(사람 세션 보호) |
| K-3 직원 | 막히면 **기기 선택 단계** — KOS 웹 화면과 같은 구성: 제목 「이미 로그인 중인 기기가 있습니다」 · 안내 「최대 5개 기기에서만 동시 로그인이 가능합니다.」 / 「아래 목록 중 로그아웃 시킬 기기를 선택해주세요.」 · 라디오 카드 하나 선택(「{OS} {브라우저} · {IP}」 + 상대 시각 「n분 전」 · 「방금 전」) · 버튼 「계속하기」. 고른 세션 해제 → sign-in 다시 → 이후 기존 흐름(병원 고르기 등). 화면은 DAY 디자인 시스템으로(기존 병원 고르기 단계와 같은 틀) |
| K-4 | **로그아웃 때 KOS 해제는 하지 않는다**(사용자 — 다시 로그인할 때 고르면 됨) |
| K-5 | 웹 · 앱 로그인 API 모두. 앱 코드는 이번에 안 고침(심사 중) — 깔린 앱이 새 단계를 받으면 어떻게 되는지 적고, 앱 화면은 다음 스펙 |
| K-6 | 순서 = **스펙 → 검수 → 코드 구현까지**. 배포는 나중(사용자) |

### KOS 사실 (코디 2026-11-17 실물 · 시스템 계정)
- 막힘: sign-in 401 `{"message":"SignInLimitExceeded","className":"InvalidRequestException","errorProperties":[{"key":"user","reason":10}]}` · `maxSignInCount` 5
- 목록 `POST common/user/v1/queries/get-active-sign-ins` 본문 `{email, password}` → `data[{id, userAgent, ipAddress, signedInDateTimeUtc}]` · 해제 `POST common/user/v1/commands/revoke-active-sign-in` 본문 `{email, password, signInId}` → `{}` (sign-in 경로 `common/v1/user/…` 와 순서 다름)
- UA 끝 표시를 붙여도 sign-in · 내부 API 200 · 목록 `userAgent` 에 그대로 · 같은 IP+UA 재로그인해도 앞 세션 안 지워짐 · dev · prod 는 같은 IP
- 목록 · 해제는 **비밀번호가 필요** → 직원 선택 단계 동안 비밀번호를 서버에 임시로 들고 있어야 한다. 지금 병원 고르기 임시 토큰이 Redis · 5분 · 한 번 쓰면 지움(SPEC-001 :121) — 같은 틀을 쓰되 비밀번호 보관 방식(암호화 · 보관 범위)은 「정할 것」 후보와 기본값으로.
- 근거 HAR(레포 밖): `~/Downloads/기기로그인.har` · 화면 캡처 `~/.config/day/reference/kos-device-limit-2026-11-17.png`(IP 가 찍혀 있어 레포에 넣지 말 것 — 글자만 옮겨라)

### 문서 · 코드
- 스펙: `products/day/20-spec/spec-001-login-session.md`(주 — U-1 · U-2 · 웹 화면 · 화면 글자 · 케이스 매트릭스 · API) · `spec-003-mobile-app.md`(앱 영향 사실만) · `spec-000-data-model.md`(필요하면) · `20-spec.md` · `log.md`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(dev `0c401726`) — `backend/day/emr/kos/client.py`(:39 `WEB_USER_AGENT` · :206 `internal_token` · :266 401 재발급) · `staff_client.py`(:60-100 sign_in · :88-90 400/401 → 자격 틀림) · `services/auth.py`(:186 login · :263 `_sign_in` · pending) · `routers/login.py` · `routers/api/` auth · 웹 로그인 템플릿 · 앱 로그인 코드(`app/`)
- 앞 백엔드 워커 조사(스펙 먼저로 중단): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-0-findings.md` · 반쯤 짠 초안 패치(참고만 · 코드엔 없음) `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-0-draft.patch`
- Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`

기대는 개념: 해당 없음.

## 2. 배경

KOS 가 계정당 동시 로그인 5개로 막기 시작했다. DAY 는 로그인마다 KOS 세션을 하나 만들고 지우지 않으며, 막히면 직원에게 「비밀번호가 맞지 않습니다」를 보여 준다. 시스템 계정(동기화)도 같은 제한에 걸린다. 위 결정 표대로 스펙을 먼저 닫고, 검수 뒤 코드로 간다.

## 3. 계약

결정 표가 계약의 뼈대다. 새 API 단계(웹 조각 · 앱 응답 모양 · 오류 코드 · 만료)를 코드 사실(병원 고르기 단계)에 맞춰 적고, 이름이 새로 필요하면 제안으로 적되 「정할 것」에 올린다.

## 4. 먼저 읽을 핵심 파일

위 §1 문서 · 코드.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. SPEC-001 개정 — K-1 ~ K-5 를 U-1 · 새 U(기기 선택) · 웹 화면 라우트 · 흐름 · 화면 글자(위 KOS 문구만) · 케이스 매트릭스(새 코드 · 만료 · 잘못된 선택 · 재차 막힘) · API · 보안(비밀번호 임시 보관) · 시스템 계정(K-2 — 연결 sign-in 절 또는 SPEC-000 해당 절)에 반영. 화면 글자는 결정 표에 있는 것만 — 짓지 마라.
2. SPEC-003 — 앱 코드 무수정 사실 · 깔린 앱이 새 단계를 받으면 어떻게 보이는지(코드 사실) · 앱 화면은 다음.
3. 열린 것은 「정할 것」(OQ)으로 — 코드 착수를 막는 것은 기본값 후보와 함께 따로 표로.
4. Delivery Issue 발행(`mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`) · 승인 receipt 는 적용하지 마라(사용자 몫).

## 7. 범위 제약 — 하지 말 것

- 코드 수정 · 커밋 · push · PR 금지. 기획안 수정 금지. 비밀번호 · 이메일 · IP 를 문서에 넣지 마라(서버 IP 도 — profile · 스펙 공개 범위 주의).
- 앱 화면 · 로그아웃 해제는 범위 밖.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/spec-report.md` — 변경 파일:줄 · 결정 표 반영 위치 · 착수 막는 OQ 표 · Issue 번호 · digest.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
