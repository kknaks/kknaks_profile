
# [frontend] 어드민 「채팅」 탭 + /admin/chats — 위젯 3종·목록·상세 (KDEV-WORK-025 P2)

너는 **kknaks-dev `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/roles/kknaks-dev/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/admin-chat-insights`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ BE 워커가 같은 워크트리의 `app/back/` 에서 병렬 작업 중 — 읽기만 하고 수정 금지. BE API 미완이어도 계약대로 mock 으로 개발.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` ← 계약의 SoT (§2 U-8 화면 계약 · §4 admin 응답 계약)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/30-work/work-025-admin-chat-insights.md` ← 빌드 계획 (Phase 2 가 네 몫)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/21-html/admin-chat-mockup.html` ← **시각 정본.** 브라우저로 열어 직접 눌러 보라 — 위젯 3종·목록·상세 전환·차트 hover 까지 마크업·CSS 값을 그대로 가져온다

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음 (시안과 spec 이 기준의 전부)

## 2. 배경 / 무엇을 바꾸나

어제 배포된 채용담당자 채팅의 대화 데이터를 owner 가 어드민에서 열람·인사이트로 본다. 어드민 사이드바에 「채팅」 탭을 추가하고 `/admin/chats` 를 시안 그대로 만든다. 대화 상세는 방문자 스레드 렌더(components/chat/ — 어제 WORK-024 산출물)를 재사용한다 — 읽기 전용.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

spec §4 「어드민 chat API 응답 계약」 그대로 소비. BE 병렬 개발 중 — 어제 lib/chat-mock 패턴처럼 fixture mock 스위치를 두고 개발, 통합은 코디 검증.

## 4. 먼저 읽을 핵심 파일

- `app/front/app/admin/(panel)/` — 기존 admin 페이지·사이드바(탭 추가 자리)·페이지네이션 관례
- `app/front/components/chat/chat-thread.tsx`·`tool-steps.tsx`·`source-cards.tsx` — 상세 렌더 재사용
- `app/front/lib/api.ts` — authFetch(admin API 호출 관례)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/`

## 6. 구현 단계

1. 사이드바 「채팅」 탭 + `/admin/chats` 라우트
2. 위젯 3종 — 시안 이식: 최근 질문 피드(클릭→상세) · 일별 30일 CSS 바 차트(hover 툴팁·요약 3수치·차트 라이브러리 금지) · 근거 문서 Top 5(태그+막대)
3. 대화 목록 테이블(페이지네이션) → 행 클릭 시 읽기 전용 상세(스레드 렌더 재사용 — 폴링·컴포저 없이 정적 렌더)
4. 헤더 총계 줄(totals)

## 7. 범위 제약 — 하지 말 것

- `app/back/`·`para/`·`orchestration/` 수정 금지 · 새 색/폰트/차트 라이브러리 금지(globals.css 토큰만) · 방문자 /chat 화면 회귀 금지(components/chat 수정은 최소·재사용 위주) · 대화 개입 기능(답장·삭제) 만들지 마라

## 8. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러). 전체 빌드 금지 — 사용자 방침. 검증은 1회만
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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
