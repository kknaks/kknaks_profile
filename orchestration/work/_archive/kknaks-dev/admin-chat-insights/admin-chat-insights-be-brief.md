
# [backend] 어드민 채팅 API 3종 — 목록·상세·인사이트 (KDEV-WORK-025 P1)

너는 **kknaks-dev `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/roles/kknaks-dev/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/admin-chat-insights`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ FE 워커가 같은 워크트리의 `app/front/` 에서 병렬 작업 중 — 읽기만 하고 수정 금지.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` ← 계약의 SoT (§2 U-8 · §4 「어드민 chat API 응답 계약」 — 필드명 그대로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/30-work/work-025-admin-chat-insights.md` ← 빌드 계획 (Phase 1 이 네 몫)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음 (조회 API — 기존 chat 도메인 관례를 따른다)

## 2. 배경 / 무엇을 바꾸나

채용담당자 채팅(SPEC-017, 어제 배포)의 데이터가 chat_session·conversation·chat_message 에 쌓이고 있다 — owner 가 어드민에서 「누가 뭘 묻는지」를 보고 싶어 한다. DB 무변경, admin 조회 API 3종만 얹는다. 기존 chat 코드(라우터·repo·schemas)가 이 워크트리에 이미 있다 — 그 관례(require_admin·계층 규약·페이지네이션 방식은 기존 admin 라우터 참조) 그대로.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

spec §4 「어드민 chat API 응답 계약」이 전문이다. 요지: 목록 `{items[],total,page,size}`(최신순, page/size 기본 1/20) · 상세는 공개 상세 shape 재사용 + sessionId · 인사이트 `{totals{conversations,questions,last7d}, recentQuestions[20]{question,askedAt,conversationId}, daily[30]{date,count}(빈 날 0), topSources[5]{type,slug,title,count}}`. FE 가 이 계약으로 mock 병행 중 — 필드명 임의 변경 금지.

## 4. 먼저 읽을 핵심 파일

- `app/back/api/chat_router.py` — 기존 chat 라우터·admin 토글(require_admin 관례)
- `app/back/repository/chat_repo.py` — 대화·메시지 조회 관례. 집계도 여기 얹는다
- `app/back/schemas/chat.py` — 상세 응답 스키마 재사용 지점
- 기존 admin 목록 라우터 1개 — 페이지네이션 관례 확인

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/`
- `app/mcp/`

## 6. 구현 단계

1. repo: 목록(최신순·페이지네이션) · 상세(소유 무관) · 집계 쿼리(daily 는 30일 빈 날 0 채움 — 파이썬에서 채워도 된다, topSources 는 assistant 메시지 sources jsonb 전개 → type·slug·title count Top 5, totals 는 대화 수·user 질문 수·최근 7일 질문 수)
2. router+schemas: `GET /api/admin/chat/conversations` · `…/{id}` · `…/insights` — 전부 require_admin
3. 테스트: 정렬·페이지 경계 · 소유 무관 상세 · 집계 정확성(빈 날 0·Top 순서·last7d 경계) · 미인증 거부

## 7. 범위 제약 — 하지 말 것

- `app/front/`·`para/`·`orchestration/` 수정 금지 · 마이그레이션 금지(DB 무변경) · 공개 chat API 계약 변경 금지 · 사전 집계 테이블 만들지 마라(요청 시 계산 — spec 명시)

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
