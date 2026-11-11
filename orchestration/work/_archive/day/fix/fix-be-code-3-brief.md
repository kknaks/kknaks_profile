# [backend] fix 코드 3 — WP-BE-4 파일 저장소(관리 ID · 환경 경로)

너는 **day `backend` 워커**(같은 터미널)다.

- **작업 계획**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` — 「WP-BE-4 파일 저장소 — 관리 ID · 환경 경로 (7판)」
- **계약의 SoT**(미커밋 스펙 7판): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/40-architecture/deployment.md` 새 절 「파일 저장소(Blob) — 구조 · 인증 · 규칙」 · env 표 / `20-spec/spec-004-internal-chat.md` 개정 ⑤ — §3 첨부 「저장소」 · 「키」 · 「저장소 꺼짐」 · 「저장소 접근 실패」 · 오류 표 · C-A26 · C-A27 / `spec-000-data-model.md` `file_key`
- 사용자 결정: `…/work/fix/_RESUME.md` §2 · `…/work/fix/correction-storage-1.md` · Delivery CENTURION_DAY#241 v3(승인됨)
- **문서 리뷰어가 이 스펙 7판을 지금 검수 중이다** — 계약이 바뀌면 코디가 정정을 보낸다. 스펙이 모호하거나 코드와 안 맞으면 짐작으로 메우지 말고 물어라.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(`kknaksss/fix-app-re1` · 앞 판 변경 미커밋 그대로 그 위에). `app/` 은 읽기만(스펙 = 앱 변경 없음 — 필요해 보이면 멈추고 물어라). `git stash` · `checkout -- .` · `clean` 금지.

## 할 것

`wp-plan.md` 「WP-BE-4」 그대로.

- 연결 문자열 방식을 **VM 시스템 할당 관리 ID** 로 바꾼다(`DefaultAzureCredential` 을 쓰지 않는다 — 스펙). 설정 = 계정 주소 + 컨테이너(비밀 아님). 없애는 칸 · 선택 비밀 한 줄을 **쓰는 곳 전부**에서 걷어 낸다 — 계획이 센 목록을 믿지 말고 `from_connection_string` · `chat_blob` · `CHAT_BLOB` · `chat-blob` · `new_key` · `check_key` 를 네가 다시 grep 해서 표로.
- 키 = `{APP_ENV}/chat/{병원 id}/{임의 이름}.{확장자}` · `check_key` 규칙 · 로컬 `disk` 는 그대로.
- 실패 동작 = 스펙 표 그대로(기동을 막지 않는다 · 503 · 새 code · 새 글자 없음) · 시간 상한을 명시적으로 넘긴다 · 관리 ID 토큰 받기에도 상한.
- `identity` · `before-after` 를 쓰는 코드는 짓지 않는다(이름만 예약 — 스펙).
- **`deploy/config/dev.env`** 에만 값을 넣는다: 계정 주소 · 컨테이너 이름은 사용자 로컬 `~/.config/day/blob-guide-2026-11-11.md` 에서 **스크립트로 읽어** 넣고(화면 · 리포트 · 로그에 값을 내지 않는다 — 리포트는 PUBLIC 레포에 간다), 채팅 첨부 스위치를 `blob` 으로. **`prod.env` 에는 값을 넣지 않는다**(칸 · 주석만 — prod 는 prod 배포 때 사용자가 정한다).
- 새 의존성은 `azure-identity` 하나(범위 지정). `uv.lock` 이 그것 말고 다른 것을 올리지 않게.

## 하지 말 것

- 저장소 · Key Vault · Azure 설정 변경 · 배포 · 서버 접속 금지. **실제 저장소에 올리기 · 읽기 · 지우기는 이번에 하지 않는다**(로컬 PC 에서는 VM 관리 ID 를 쓸 수 없다 — 실물 확인은 dev 배포 뒤 코디가 dev 컨테이너에서 한다). 사용자 계정 자격으로 로컬에서 붙어 보지도 않는다.
- `app/` · 통역 · migration · 배포 워크플로 변경 금지. 커밋 · push 금지.
- 사용자 로컬 스택(`day-local-*` · 11040 · 11042 · 11043) 금지 — infra 시험은 격리 스택(다른 프로젝트 이름 · 다른 포트 · 끝나면 `down -v`).

## 검증

- 고친 테스트 파일만 `uv run pytest -q`(infra 는 격리 스택 `scripts/test.sh -q <파일들>`) · `uv run ruff check`.
- 관리 ID 경로는 로컬에서 실물로 못 돈다 → **가짜 자격 · 가짜 전송으로** 시험한다: 클라이언트가 계정 주소 · 컨테이너 · 관리 ID 자격으로 만들어지는지 · 경로가 `{환경}/chat/{병원 id}/…` 인지 · 토큰 실패 · 403 · 없음 · 시간 초과가 스펙의 응답으로 가는지 · 기동을 막지 않는지.
- `day_vm.py materialize --environment dev --dry-run` 이 새 `dev.env` 를 통과하는지 · 없앤 선택 비밀이 Key Vault 에 남아 있거나 없어도 배포가 깨지지 않는지(코드로).
- 마지막에 `uv run pytest -q -m "not infra"` 1회 + 격리 스택 `scripts/test.sh -q` 1회.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-4-report.md` — 변경 파일 / 걷어 낸 낱말 grep 전수 표(자리 · 처리) / 수용 항목 ↔ 시험 / 설정 계약 표와 구현 대조(값은 「설정됨」으로) / 실패 동작 표와 구현 대조 / 수치 / **dev 배포 뒤 코디가 컨테이너에서 돌릴 실물 확인 명령**(올리기 → 읽기 → 지우기 · 시험 파일 이름 규칙 · 지운 것 확인 — 값 없이) / 스펙과 다른 곳 · 물을 것 / pending.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_d8e9c610-96b4-482a-9972-365ca65c1084 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: <한 줄>" --body "변경 파일 수 / 시험 수치 / 스펙과 다른 곳 / pending"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] backend: <질문>" --enter`
