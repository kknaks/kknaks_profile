# [reviewer] fix 서버 검수 3 — WP-BE-4 파일 저장소(관리 ID · 컨테이너로 환경 분리)

너는 **day `reviewer` 워커**(같은 터미널)다. 작성자가 아니다. read-only.

- **계약의 SoT**(미커밋 스펙 9판): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/40-architecture/deployment.md` 「파일 저장소(Blob) — 구조 · 인증 · 규칙」 절 · env 표 / `20-spec/spec-004-internal-chat.md` 개정 ⑤ + 정정 3 — §3 첨부 「저장소」 · 「키」 · 「저장소 꺼짐」 · 「저장소 접근 실패」 · 오류 표 · 케이스 매트릭스 · C-A26 · C-A27
- 정정 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-storage-2.md` · `correction-storage-3.md`(3 이 2 의 「환경 폴더」를 뒤집었다 — **최종 = 환경은 컨테이너 · 키 `chat/{병원 id}/…`**) · 작업 계획 `…/work/fix/wp-plan.md` 「WP-BE-4」 · 문서 리뷰 `…/work/fix/review-doc-3-report.md`(W1 ~ W7)
- 작성자 브리프 · 리포트: `…/work/fix/fix-be-code-3-brief.md` · `be-4-report.md`
- 저장소 사실(인프라 안내문): 사용자 로컬 `~/.config/day/blob-guide-2026-11-11.md` — ⚠ 그 안의 값(계정 이름 · 주소 등)을 리포트에 옮기지 않는다. `deploy/config/dev.env` 의 저장소 주소 값도 옮기지 않는다.

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 `app/` 밖 — 네 앞 서버 검수(2) 뒤에 바뀐 것.

## 볼 것

1. **연결 문자열이 정말 없어졌나** — `from_connection_string` · `chat_blob` · `CHAT_BLOB` · `chat-blob` 를 네가 직접 grep. 남은 자리가 「금지 목록 · 안 읽음 설명 · 금지 단언」뿐인지. 없앤 키 이름이 Git 일반 설정에 들어오면 계속 거절되는지 · Key Vault 에 옛 비밀이 남아 있거나 없어도 배포가 그대로인지(`day_vm.py` 코드로).
2. **관리 ID 만** — `ManagedIdentityCredential` 하나 · 다른 자격으로 넘어가는 길(환경 변수 자격 · CLI · 체인)이 없는지 · 토큰 받기 전체 상한 30초가 `get_token` · `get_token_info` 둘 다 걸리는지 · 상한을 넘겼을 때 걸려 있던 요청이 정리되는지 · 토큰 캐시 · 동시 요청.
3. **클라이언트 수명** — 처음 쓸 때 만들고 재사용 · (주소, 컨테이너)마다 한 벌 · lifespan 종료 때 닫기 · 닫은 뒤 다시 쓰는 길 · 시험 사이 누수 · 기동 때 저장소 · IMDS 에 닿지 않는지 · worker · scheduler 프로세스에서 어떻게 되는지.
4. **키 · 경로** — 최종 규칙 `chat/{병원 id}/{32 hex}.{jpg|mp4}` · 환경 접두 · 환경 `check_key` 가 **완전히** 걷혔는지(중간에 넣었다 뺀 코드 · 주석 · 시험 잔재 grep — `APP_ENV` · `app_env` 가 저장소 코드에 남았는지) · 모양 밖 키가 열기 · 전달 · 지우기에서 500 이 아니라 스펙의 길로 가는지 · 다른 병원의 키를 여는 길이 없는지(키 모양이 아니라 DB 행 · 방 경계로 막는지).
5. **실패 동작** — 토큰 실패 · 403 · `ContainerNotFound` · 연결 실패 · 시간 초과 → 503 `photo_disabled` · `BlobNotFound` → 404(열기) · 크기 초과 413 은 그대로 · 쓰다 실패하면 반쯤 올라간 파일 지우기 시도 · **본문 스트림 도중 실패 = 끊김 + 로그**(이미 머리를 보낸 뒤 예외가 500 으로 바뀌지 않는지) · 로그에 키 전체 · 주소 · 토큰이 실리지 않는지. 앱 실제 코드(`app/lib/chat/`)에서 409 와 503 이 스펙이 말한 대로 갈리는지.
6. **컨테이너 이름은 설정에서만** — 코드 · 시험에 `daydev` · `dayprod` · `files` 가 박혀 있지 않은지(설정 파일 `dev.env` 제외).
7. **배포 설정** — `dev.env` 세 칸(스위치 · 주소 · 컨테이너) · `prod.env` 값 없음(칸 · 주석만) · compose · 예시 env · `day_vm.py materialize --dry-run` 통과 주장 · 설정 계약 시험이 값(주소)을 실패 메시지에 싣지 않는지.
8. **의존성** — `azure-identity` 범위 · `uv.lock` 이 `azure-identity` · `msal` · `msal-extensions` 셋 추가 말고 기존 패키지를 올리지 않았는지(네가 직접 lock diff).
9. **시험이 조용히 통과하는 자리** — 가짜 자격 · 가짜 전송이 SDK 예외 모양 그대로인지 · 관리 ID 경로는 실물에서만 확인된다는 점이 보고에 분명한지 · 작성자가 적은 「배포 뒤 코디가 컨테이너에서 돌릴 실물 확인 명령」이 실제로 스펙 C-A27 ⓐⓑⓒ 를 가르는지(읽고 판정 — 돌리지 않는다).
10. 범위(`app/` · 통역 · migration · 워크플로 무변경) · 앞 판 코드(읽음 표시 · 통역 · 접근 로그 필터)를 건드려 깨뜨린 것이 없는지.

## 돌려 볼 것(각 1회)

```
cd backend && uv run pytest -q -m "not infra"
cd backend && uv run ruff check . ../scripts
```

infra 는 돌리지 않는다. **실제 저장소 · Azure · IMDS 호출 금지.**

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-be-3-report.md` — 판정 **FAIL / WARN / PASS** · 지적마다 `파일:줄` + 근거(스펙 절 · 정정 문서) + 고칠 방향 · 조용히 통과하는 자리 · 수치. 값 없음.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: <판정 · 한 줄>" --body "판정 / FAIL·WARN 목록(파일:줄) / 수치"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```
