
# [reviewer_code] 채용담당자 채팅 BE+FE 산출물 검수 (WORK-023 · WORK-024)

너는 **kknaks-dev `reviewer_code` 워커**다 — **read-only**. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/roles/kknaks-dev/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`
base 브랜치: `origin/main` (변경은 전부 **미커밋 상태** — `git status` + `git diff` + untracked 로 범위를 산정한다)

## 1. SSOT — 판정 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` (**v0.0.4** — API 봉투·에러 detail 형식·합성 slug·url 매핑까지 반영된 최신)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/30-work/work-023-recruiter-chat-backend.md` · `work-024-recruiter-chat-frontend.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/10-decision/decision-027-chat-ai-execution-and-tool-boundary.md` (D1~D6 — 특히 D5 표면 축소·D4 옵트인)

## 2. 검수 축 (각 축에 PASS/WARN/FAIL + 근거 파일:줄)

1. **allowed_paths**: BE 변경이 `app/back/`·`app/mcp/` 안인가, FE 가 `app/front/` 안인가. `para/`·`orchestration/`·`resume/`·`agents.md` 오염 없나
2. **기존 파이프라인 무변경**: `service/ai_service.py`·기존 워커 compose 서비스·`queue=default` 경로에 삭제/수정이 없나
3. **spec 계약**: API 4+1 경로·요청/응답 필드명·에러 `{"detail":"<CODE>"}`·쿠키 속성(httpOnly·Lax·Secure·30일 sliding·해시 저장)·합성 slug 404 동일성·tool 11종 이름·steps/sources shape·폴링 계약(FE)
4. **경계(보안)**: 제출 -c 오버라이드에 shell/web_search/apps off + sandbox=read-only 가 실제로 있나 · turn 토큰 로그 마스킹 · chat-tool 이 chat_exposed 를 매 호출 판정하나 · 남의 세션 대화 404
5. **계층 규약**: router→service→repository, ORM 이 repository 를 넘지 않나, 아래층 HTTP 무지
6. **소비자 멱등**: 같은 이벤트 2회 = 같은 결과인가(재생 초기화·tool_use_id upsert), 실패/timeout 마감 경로
7. **FE**: 폴링 done/failed 중단+cleanup · pending 컴포저 잠금 · mock↔실API 전환 스위치 · 토큰 밖 색 미도입
8. **테스트 실재**: 주장(105+19)이 실제 파일·케이스로 존재하나. 핵심 시나리오(쿠키 발급 시점·409·404 동일성·멱등)가 커버되나

## 3. 산출물 — 이 파일 하나만 쓴다

`/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/work/recruiter-chat/review-code-report.md`

형식: 총평(PASS/WARN/FAIL) → 축별 판정 표 → 위반/우려 목록(파일:줄 + 근거 규칙 + 심각도) → 코디가 물어야 할 질문. 코드를 고치지 말고 테스트도 돌리지 마라(코디가 이미 재현했다 — 105+19 passed).

## 4. 완료 보고 — 문구 변경 금지

- 리포트 작성 후 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch preamble> \
  --dispatch-id <이 태스크의 dispatchId — dispatch preamble> \
  --subject "reviewer_code 완료: <총평>" \
  --body "총평 / 축별 판정 / FAIL·WARN 요지 / 리포트 경로"

orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] reviewer_code 완료 — <총평 한 줄>. 리포트: work/recruiter-chat/review-code-report.md" --enter
```

> ⚠ 핸들은 dispatch preamble 값이 우선이다 — 위 값과 다르면 preamble 이 맞다.
