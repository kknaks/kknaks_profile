# [backend] fix 코드 2 — WP-BE-3 읽음 표시 서버

너는 **day `backend` 워커**(WP-BE-1 · BE-2 · 수정 1 을 한 같은 터미널)다.

- **작업 계획**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` — 「WP-BE-3 읽음 표시 서버」 · §3 「읽음 계약 표」 · §4 순서
- **계약의 SoT**(미커밋 스펙): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-004-internal-chat.md` 개정 ④ — §3 `Member`(`lastReadSeq` · `fromSeq`) · 규칙 「읽음」 「읽음 표시 계약」 · 실시간 표 `chat_member_read` · 케이스 매트릭스 · C-A11 · C-A24 · OQ-C17 / `spec-000-data-model.md` 07 `chat_member`
- 사용자 원천: `…/work/fix/e2e-feedback.md` 10번 · Delivery CENTURION_DAY#241 v2(승인됨)
- 스펙에 없는 것은 발명하지 마라. **문서 리뷰어가 이 스펙 4판을 지금 검수 중이다** — 계약이 바뀌면 코디가 정정을 보낸다. 스펙이 모호하거나 코드와 안 맞는 곳을 보면 짐작으로 메우지 말고 물어라.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(브랜치 이름이 **`kknaksss/fix-app-re1`** 로 바뀌었다 · 앞 판 변경 미커밋 그대로 그 위에). ⚠ mobile 워커가 같은 워크트리의 `app/` 에서 동시에 일한다 — `app/` 은 읽기만. `git stash` · `checkout -- .` · `clean` 금지.

## 할 것

`wp-plan.md` 「WP-BE-3」 그대로.

- `Room` 이 나오는 **모든** 응답 · 이벤트의 `members[]` 에 `lastReadSeq` · `fromSeq` — `Room` 을 만드는 자리를 grep 으로 전부 세어(한 함수를 지나는지) 보고에 표로.
- `chat_member_read {roomId, accountId, lastReadSeq}` — 읽음 #15 가 **실제로 올렸을 때만** · 커밋 뒤 · 스펙이 정한 받는 사람에게만. 읽은 본인에게 가는 기존 `chat_read` 는 그대로.
- migration 없음(칸이 이미 있다). 필요해 보이면 멈추고 물어라.
- 목록 안 읽음 수 · 탭 배지 · 푸시 · #15 응답은 바꾸지 않는다.

## 범위 제약

allowed_paths: `backend/`(채팅 쪽 — 계획이 센 파일) · `backend/tests/`. 금지: `app/` · 통역 코드 · 배포 설정 · 의존성 · 배포 · 서버 · Soniox · KOS 호출 · 커밋 · push.
사용자 로컬 스택(`day-local-*` · 11040 · 11042 · 11043) 금지 — infra 시험은 앞 판처럼 **격리 스택**(다른 프로젝트 이름 · 다른 포트 · 끝나면 `down -v`).

## 검증

고친 테스트 파일만 `uv run pytest -q`(infra 는 격리 스택 `scripts/test.sh -q <파일들>`) · `uv run ruff check` · 마지막에 `uv run pytest -q -m "not infra"` 1회 + 격리 스택 `scripts/test.sh -q` 1회.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-3-report.md` — 변경 파일 / `Room` 만드는 자리 전수 표 / 수용 항목 ↔ 시험 / §3 읽음 계약 표와 구현 필드 대조 / 수치 / 스펙과 다른 곳 · 물을 것 / pending.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_d8e9c610-96b4-482a-9972-365ca65c1084 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 수 / 시험 수치 / 스펙과 다른 곳 / pending"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] backend: <질문>" --enter`
