# [reviewer] 식약처 MCP 코드 검수 — 공유 전 마지막 게이트

너는 **procedure-hub 검수 워커**다(read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (리포트 1개 외 수정 금지)

## 1. 기준 · 대상

- 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` 전체(`git status` 로 untracked 포함 범위 산정)
- 기준: `orchestration/work/phub-recommend/SPEC-002-mfds-mcp.md`(v0.2.0) · 구현 브리프 `phub-recommend-tool-brief.md` §3(의약품 Service08 · 공유용 폴더 요건) · 코디 추가 지시(DUR 실제 동작) · `NOTES.md`(실호출 정본) · `review-spec-002-003-report.md` W-13
- 구현 워커 완료 보고는 코디가 아래 §3 에 붙인다

## 2. 볼 것

1. **키 누출 — 최우선.** 코드 · 테스트 · README · 로그 · 예외 메시지 · 캐시 파일 이름 · git 추적 파일 어디에도 키 값이나 serviceKey 가 남지 않나(`.env` 의 실제 값 문자열로 폴더 전체 grep — 값을 리포트에 쓰지 않는다). `.gitignore` 가 .env · cache · .venv 를 막나
2. SPEC 대조 — tool 이름 · 입력 · 출력 · 대소문자 파라미터 · 서비스 버전(의약품 08) · 취소 걸러내기 · 에러 구분 · 캐시 · 일일 상한
3. **받는 사람 기준** — 폴더 하나만 복사해 README 대로 하면 돌아가나. 절대경로 · 이 프로젝트 의존 · 빠진 파일(uv.lock 등) · README 의 설치/설정/예시가 실제 명령과 맞나
4. 테스트가 실호출 없이 도나 · smoke 스크립트가 무엇을 확인하나
5. 사용자가 실물에서 만날 자리

## 3. 구현 워커 보고

tool_dev 완료 보고 요약(10-27): tool 7(device_search · device_detail · device_company · drug_search · drug_detail · dur_check(kind 9 → 오퍼레이션 9) · status). pytest 25 passed(실호출 0) · ruff 통과 · smoke 실호출 8회 OK · stdio e2e(tools/list 7 + 3 호출) · 가짜 키 · 실키 grep 0(stdout · stderr · cache · 폴더). SPEC 과 다른 점(판정 대상): ① 의약품 07→08 ② DUR not_available_yet 제거 · 실조회 ③ drug_search 의 ingredient 입력 뺌(필터 0건) ④ drug_detail 은 item_seq 만 ⑤ include_ingredients 입력 추가(Mcpn) ⑥ ruff line-length 140. 미결: 틀린 키도 SERVICE_KEY_IS_NOT_REGISTERED 로 와서 미등록과 구분 불가

## 4. 산출물 · 판정

- 생성: `orchestration/work/phub-recommend/review-mcp-report.md` 1개. 맨 위 PASS/WARN/FAIL. FAIL = 키 누출 · 받는 사람이 못 돌림 · SPEC 위반으로 틀린 결과
- 코드 실행 금지(read-only) — 단 `uv run pytest` 는 실호출 없는 테스트라 1회 허용

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: MCP <판정>" \
  --body "FAIL / WARN / 키 grep 결과 / pytest 결과"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer 완료 — MCP <판정>. 상세는 인박스." --enter
```
