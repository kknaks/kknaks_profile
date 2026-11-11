# [reviewer_doc] fix 스펙 7판 검수 — 파일 저장소(Blob) 구조 · 채팅 첨부 관리 ID 연결

너는 **day `reviewer_doc` 워커**(같은 터미널)다. 작성자가 아니다. read-only.

- 사용자 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/_RESUME.md` §2(저장소 결정 2줄) · `…/work/fix/correction-storage-1.md`(용도 폴더 셋)
- **저장소 사실의 원천(인프라 담당 안내문)**: 사용자 로컬 `~/.config/day/blob-guide-2026-11-11.md` — ⚠ 그 안의 **값(계정 이름 · 주소 · 컨테이너 이름 · 리소스 그룹 · 구독 · VM 이름 · 로그인 계정)을 리포트에 옮기지 않는다.**
- 작성자 브리프 · 리포트: `…/work/fix/fix-spec-7-brief.md` · `spec-7-report.md` · 작업 계획 `…/work/fix/wp-plan.md` 「WP-BE-4」
- 코드(읽기): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `backend/day/services/chat_storage.py` · `chat.py` · `common/config.py` · `scripts/deploy/day_vm.py` · `deploy/` · `app/lib/chat/`(앱이 409 · 5xx 를 어떻게 그리는지)

검수 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` 미커밋 변경 중 **7판분**(`40-architecture/deployment.md` 새 절 「파일 저장소(Blob)」 · env 표 · Key Vault 줄 / SPEC-004 개정 ⑤ / SPEC-000 개정 ③ / `system.md` / `log.md`) + `wp-plan.md` WP-BE-4.

**backend 워커가 이 스펙으로 지금 코드를 짓고 있다.** 계약을 바꿔야 하는 지적이 나오면 리포트 전에 먼저 한 줄:
`orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[긴급] reviewer_doc: <문서:줄 · 무엇이 틀렸나>" --enter`

## 볼 것

1. **사용자 확정과 같은가** — 맨 위 환경(`dev` · `prod`) · 용도 셋(고객 전후 사진 · 고객 신분증(여권) · 내부 채팅 사진). 폴더 **이름**(`identity` · `before-after`) · 병원 id 층 · 로컬 Blob 길 없음 · env 이름 등이 코디/planner 기본값으로 구별돼 있는지.
2. **안내문의 사실과 같은가** — 인증(관리 ID 만 · 키 · 연결 문자열 · SAS · 익명 꺼짐) · 컨테이너 하나 · dev/prod 가 같은 VM · 같은 ID · 권한이 컨테이너 전체(= 폴더 분리는 차단이 아님) · 자동 삭제 · soft delete · 버전 꺼짐 · 서버 경유 전달. 스펙이 안내문에 없는 것을 사실처럼 적은 곳.
3. **값이 새지 않았나** — 스펙 · 계획 · 리포트 · Delivery 본문에 안내문의 값이 **이번에 새로** 들어간 줄이 없는지(`git diff` 의 `+` 줄 기준 — 기존에 있던 Key Vault 이름 줄은 이번 변경이 아니다).
4. **설정 계약** — 더하는 칸 · 없애는 칸이 코드의 쓰는 곳 전부(`config.py` · `day_vm.py` `OPTIONAL_SECRETS` · 금지 키 · compose · 예시 env · 설정 계약 시험 · 문서)와 맞물리는지. 없앤 선택 비밀이 Key Vault 에 남아 있어도 배포가 깨지지 않는지. `DAY_CHAT_STORAGE=blob` 인데 계정 주소 · 컨테이너가 빈 조합의 동작.
5. **경로 규칙** — `{APP_ENV}/chat/{병원 id}/{이름}` 이 코드의 `new_key` · `check_key` · DB `file_key` 칸 · 열기 · 전달 · 지우기와 일관되는지 · 「키의 환경 ≠ 자기 환경이면 404 처럼」이 정당한 dev 데이터 · 시험 · 로컬 `disk` 를 깨뜨리지 않는지 · `APP_ENV` 가 가질 수 있는 값 전부(`local` 등)에서 경로가 어떻게 되는지.
6. **실패 동작** — 토큰 못 받음 · 403 · 컨테이너 없음 · 시간 초과를 503 `photo_disabled` 로 묶은 것이 앱 실제 코드에서 스펙이 말한 대로 보이는지(올리기 · 열기 · 전달 · 동영상 재생 — `app/lib/chat/` 를 직접 본다) · 같은 code 를 409 와 503 에 쓰는 것이 앱 분기를 헷갈리게 하지 않는지 · 「기동을 막지 않는다」가 AGENTS 안전 기준(timeout 명시)과 맞는지 · 관리 ID 토큰 받기에 시간 상한이 있는지.
7. **관리 ID 만** — `DefaultAzureCredential` 을 쓰지 않는다는 결정이 로컬 · 시험 · CI 를 막지 않는지 · 토큰 캐시 · 갱신 · 동시 요청.
8. **예약 폴더** — `identity` · `before-after` 를 「이름만 예약」으로 둔 것이 SPEC-000 의 신분증 사진 칸 · 「법적 검토 필요」 · 데이터 규칙(민감정보 암호화)과 모순 없이 적혔는지 · 구현을 미리 정하지 않았는지.
9. **수용 항목 C-A26 · C-A27 · Delivery A12 ~ A14** 가 통과 · 실패를 가르는지 · 실물 몫 · 조용히 통과하는 자리(가짜 저장소로만 통과 · 관리 ID 경로는 실물에서만).
10. `wp-plan.md` WP-BE-4 의 「고칠 파일」이 코드에서 그 낱말을 쓰는 곳 전부인지 네가 직접 grep · 「앱 변경 없음」이 참인지.
11. 옛 문장(연결 문자열 · 선택 비밀 3 · 「Blob 아직 없음」 등)이 다른 절 · 다른 문서에 남았는지.

## 돌려 볼 것
`python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0)

## 보고
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-doc-3-report.md` — 판정 **FAIL / WARN / PASS** · 지적마다 `문서:줄` + 근거 + 고칠 방향 · 조용히 통과하는 자리 · lint. 값 없음.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_fe17c0ae-13ad-4046-abb8-f9e9280f8932 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer_doc 완료: <판정 · 한 줄>" --body "판정 / FAIL·WARN 목록(문서:줄) / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] reviewer_doc 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```
