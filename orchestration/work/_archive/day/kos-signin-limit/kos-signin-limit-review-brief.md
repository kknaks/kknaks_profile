
# [reviewer] KOS 기기 제한 코드 검수 (read-only)

너는 **day `reviewer` 워커**다. 너는 앞 맥락이 없다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

be · fe 는 끝났다. 파일을 고치지 마라 — 리포트 1개만.

## 1. SSOT — 먼저 읽을 것

- 스펙(미커밋): `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec/products/day/20-spec/spec-001-login-session.md` 개정 ⑨ + 보충 ① ~ ④ · `spec-003-mobile-app.md` ⑱ · `spec-000-data-model.md`. 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/_RESUME.md` §2.
- 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-be-brief.md` · `kos-signin-limit-fe-brief.md` · 결과 `be-1-report.md` · `fe-1-report.md`.
- 리뷰 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit` 미커밋 diff 전체 · base dev `0c401726`. `AGENTS.md`.

기대는 개념: [[external-api-error-classification]].

## 2. 배경

KOS 동시 로그인 5개 제한 처리. 다음은 사용자 로컬 확인 → 배포(나중).

## 3. 계약

be ↔ fe: `PendingDeviceChoice` · `DeviceChoice` · `auth.choose_device` · `auth.login(device_choice=...)`(be-1 리포트).

## 4. 먼저 읽을 핵심 파일

diff 전체.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 검토 항목

1. **보안** — 비밀번호 · 이메일 · KOS 토큰이 응답 · 화면 · 숨은 칸 · URL · 로그 · DB · 예외 메시지 · repr 에 새는 곳 0(grep + 경로 추적) · 임시 값 암호화 · 5분 · 꺼내면 지움 · 종류 구분(병원 고르기와 섞이면 session_expired).
2. **시스템 계정 자동 해제** — 막혔을 때만 · 같은 UA 정확히 같음 · 가장 오래된 1개 · 재시도 1회 · 태그 없으면 정리 안 함 · 해제 4xx · 다른 환경 · 사람 세션 안 건드림 · 동시 실행(병원별 어댑터 여럿)에서 서로 끊는 왕복 위험.
3. **판정** — `SignInLimitExceeded` vs 틀린 비밀번호(같은 401) · 본문 모양이 다르면.
4. **앱** — `/api/auth/login` 이 기기 제한이어도 지금과 같은 401 `invalid_credentials` · 데모 넘김(`services/environments.py`) 영향 · 앱 응답 모양 변화 0.
5. **웹** — U-4 글자 스펙 그대로 · 「처음으로」 없음 · `/login/device` 갈래 · CSRF.
6. **UA 표시** — 세 곳 공용 · 비면 지금과 같음 · env 전달(compose).
7. 테스트가 위를 실제로 단언하나 · `pytest -m "not infra"` 1회 직접. 「조용히 통과하는 자리」 · 사용자가 로컬에서 만날 자리.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 금지 · Docker · 로컬 스택 · KOS 실호출 금지.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/review-code-1-report.md`.

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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
