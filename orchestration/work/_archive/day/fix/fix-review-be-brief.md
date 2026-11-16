# [reviewer] fix 서버 코드 검수 — WP-BE-1(채팅 · 알림) · WP-BE-2(통역)

너는 **day `reviewer` 워커**다. 앞 판(#240 · 앱 검수)의 맥락이 있더라도 아래 파일을 기준으로 한다. 작성자가 아니다 — 독립으로 본다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 문서)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md`(계층 · `day.public` 경계 · 「백엔드 안전 기준」 — timeout · 취소 · 동시성 상한 · 루프 막지 않기 · 로그에 비밀 금지)
- **계약의 SoT**(미커밋 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/`): `20-spec/spec-003-mobile-app.md` §3 「통역 — 앱 · 서버 계약」 · A-14 · A-14b · A-44 ~ A-47 · I-1 ~ I-5 · OQ-A39 ~ A46 / `spec-004-internal-chat.md`(#22 · 규칙 `:349` · 푸시 받는 사람 · C-A20 · C-A21) / `spec-005-notifications.md`(`chat` 종류 · N-A13) / `spec-000-data-model.md` / `40-architecture/deployment.md`
- 작업 계획: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` §2 「WP-BE-1」 「WP-BE-2」 · §3 · §5 · §6 · Delivery CENTURION_DAY#241(L3 · 승인됨)
- 작성자 브리프 · 리포트: `…/work/fix/fix-be-code-brief.md` · `be-1-report.md` · `be-2-report.md`
- 통역 원천(대조용): interpret-pwa `origin/main` `17c26b5` — `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:<path>`(checkout · pull 금지) · 조사 `…/work/fix/research-interpret-report.md`
- 앱 쪽 실제 코드(계약 대조): `app/lib/interpret/` · `app/lib/chat/chat_api.dart` · `app/lib/notify/` — mobile 워커가 **지금 같은 워크트리에서 `app/` 을 고치는 중**이다. `app/` 은 읽기만.

검수 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 **`app/` 밖 미커밋 변경 전부**(`git status --short -- backend scripts deploy docs pyproject.toml uv.lock` · 새 파일 포함).

## 볼 것

1. **통역 — 원천과 무엇이 달라졌나.** 가져온 파일을 원천과 `diff` 해서 「그대로」라는 보고가 참인지 확인하고, 달라진 줄을 전부 표로 낸다(기록기 제거 · 자리 · `session_limit` · 문구 · 인증). 달라진 줄마다 스펙 근거가 있는지.
2. **동시 세션 자리.** 잡는 자리 · 돌려놓는 자리를 코드로 따라가 **모든 종료 경로**(정상 · stop · 오류 프레임 · STT/TTS 열기 실패 · 설정 재시도 중 예외 · ready 뒤 끊김 · 앱이 닫는 프레임 없이 사라짐 · 태스크 취소 · Soniox 연결 중 취소 · accept 뒤 예외)에서 한 번만 반납되는지. 시험이 그 경로를 실제로 타는지(작성자의 「변이 확인」 주장 포함). 프로세스 안 셈이 api worker 1 전제와 맞는지.
3. **인증 · 권한.** accept 전 검사 순서 · DB 세션을 accept 전에 닫는지 · `board` view + 전체 권한 계정 · 로그아웃 · 만료 · 다른 병원 세션. `day.public.run_interpret_session`(인증 없이 세션을 도는 새 공개 함수)이 HTTP 로 닿을 길이 정말 없는지 · 경계를 넓힌 것이 맞는지.
4. **비밀 · 로그.** 오류 `message` · 로그에 키 · env 이름 · 토큰 · 받은 본문 · 발화 원문이 실리는 자리가 없는지 **전부 grep**. 작성자 보고 1(uvicorn 접근 로그에 `?token=` 이 남음 — 원천은 쿼리 지우기 필터가 있었다): 넣어야 하는지 판정하고, 넣는다면 어디에 무엇을(기존 SSE · 다른 경로에도 같은 문제가 있는지 포함).
5. **루프 · 시간 상한 · 자원.** async 경로의 동기 작업(OpenCC · JSON 조립) · Soniox 연결 수립 10초 · drain · 닫기 대기 · 죽은 앱 연결 감지 · 세션당 태스크가 취소 때 전부 정리되는지 · 예외가 삼켜지는 `except` 가 없는지.
6. **기동.** lifespan 시드 적재가 `runtime` → `day.public` 경계를 지키는지 · 깨진 시드 = 기동 실패가 **worker · scheduler 프로세스**에도 걸리는지(걸리면 통역과 무관한 동기화까지 멈춘다 — 스펙은 api 만 말한다) · 시드 파일이 이미지에 들어가는지(`deploy/Dockerfile`).
7. **채팅 · 알림(BE-1).** #22: 그룹만 · 지금 멤버만 · 나간 멤버 · 다른 병원 · 40자 · 빈 값 · 같은 이름 = 이벤트 없음 · 방 행 잠금 · 커밋 뒤 이벤트 · `last_message_at` · 안 읽음 수를 건드리지 않는지. `chat` 알림: 받는 종류 조건 = 채팅 403 판정과 한 곳인지 · 차례 · 저장 없으면 켜짐 · 푸시 받는 사람에서 끈 계정이 빠지는 쿼리(방별 `is_muted` 와의 4조합) · 원장 호출 푸시에 영향이 없는지. migration 없음 주장.
8. **배포 설정.** `day_vm.py` 선택 비밀 한 줄 · 금지 키 검사 · `deploy/config/*.env` 가 **주석만** 바뀌었는지(값 줄 diff 0) · compose 기본값 · `pyproject.toml` 의존성 범위 · `uv.lock` 이 그 둘 말고 다른 것을 바꾸지 않았는지.
9. **시험이 조용히 통과하는 자리.** 가짜 Soniox 가 구현을 그대로 흉내 내 실패할 수 없는 시험 · skip 되는 infra 시험 · 수용 항목마다 시험이 있는지.
10. **범위.** 계획 밖 파일 · `app/` · `.github/` · migration 이 없는지.

## 돌려 볼 것(각 1회)

```
cd backend && uv run pytest -q -m "not infra"
cd backend && uv run ruff check . ../scripts
```

infra 시험(`scripts/test.sh`)은 **돌리지 않는다** — 사용자 로컬 스택(`day-local-*` · 11040 · 11042 · 11043)을 건드리면 안 되고 격리 스택을 네가 띄우지도 않는다. 작성자가 격리 스택에서 1136 passed 라고 보고했다 — 그 수치를 못 믿을 근거가 코드에 보이면 지적한다.

## 하지 말 것

- 파일 수정 금지(리포트 1개만). **Soniox · KOS · 서버 호출 금지** · 배포 · Key Vault 금지. `git stash` · `checkout` 금지.
- 키 · 토큰 값을 리포트에 옮기지 않는다(`deploy/config/dev.env` 의 Key ID · Team ID 포함).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-be-report.md`
— 판정 **FAIL / WARN / PASS** · 지적마다 `파일:줄` + 근거(스펙 절 · AGENTS 줄 · 원천 줄) + 고칠 방향 한 줄 · 「원천 대비 달라진 줄 표」 · 「자리 반납 경로 표」 · 「작성자 5건 판정」 · 「조용히 통과하는 자리」 · 돌린 명령 수치.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] reviewer: <질문>" --enter`
