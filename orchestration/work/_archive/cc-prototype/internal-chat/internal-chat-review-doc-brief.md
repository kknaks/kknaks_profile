# [reviewer_doc] 직원 앱 내부 채팅 — SPEC-007 · WORK-011 문서 검수 r1

너는 **cc-prototype `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅` (코디 워크트리 · **read-only**)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

## 1. SSOT — 대조 기준 (이기는 순)

1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md`: 결정 D-01 ~ D-37 · OQ-901 · 902
2. 확정 시안(화면 정본 · D-35): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design/Ceramique 의료진 앱 — 채팅.dc.html` (장면 24) + `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design-chat-report.md`
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/research-mattermost-report.md` §4 (코드 자리)
4. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` (지금 앱 계약)
5. 지금 구현(읽기만 · canonical · pull/checkout 금지): `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/` HEAD `dbf0b53`

**검수 대상**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` (0.1.0) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` · SPEC-004 바뀐 3줄(`git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 diff`) · planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-report.md`

**기대는 개념**: 해당 없음

## 2. 배경

DEC-009 와 시안을 사용자가 확정했고, planner 가 SPEC-007 · WORK-011 을 썼다. 코드 워커(backend · mobile)는 이 두 문서만 받고 구현한다. 그래서 **워커가 추측으로 메워야 하는 빈칸**을 이 검수에서 찾는다.

## 3. 계약

해당 없음 (검수)

## 4. 볼 것 — 전부

1. **DEC 대조**: D-01 ~ D-37 이 SPEC 절에 맞게 옮겨졌나. 뒤집거나 넓히거나 좁힌 곳은 FAIL
2. **시안 대조**: 장면 24장 → SPEC §10 화면 절. 시안에 있는데 SPEC 에 없는 요소 · 상태 · 문구, 반대로 시안에 없는데 SPEC 이 만든 화면
3. **근거 없는 정책**: DEC · 시안 · 코드 어디에도 근거가 없는데 「기본값」 표시도 OQ 도 없는 규칙
4. **기본값 OQ-903 ~ OQ-931**: 각각이 DEC 와 부딪히지 않나. 사용자에게 물어야 할 무게인 것(제품 동작이 눈에 보이게 갈리는 것)은 따로 「사용자 판단 후보」로 모은다
5. **API · SSE · 표 계약의 완결성**: backend · mobile 이 서로 묻지 않고 구현할 수 있을 만큼 필드 · 타입 · 오류 코드 · 권한 · 정렬 · 페이지가 다 있나. 웹이 깨지지 않는 근거가 코드와 맞나
6. **코드 자리 §12**: `/Users/kknaks/git/toy_pr2/cc-prototype/procedure` 를 직접 grep 해서 줄 번호 · 지금 모양이 맞는지 표본이 아니라 **전부** 확인한다. R§4 · §12 둘 다에 빠진 자리를 찾는다(예: 푸시 받기 · 앞 배너 · 생명주기 · 멀티파트 · 경로 수 · 라우터 · CORS · 시험 픽스처)
7. **WORK-011**: WP 순서 · 병렬 조건 · 대상 파일 · 완료 조건 · 검증 명령이 SPEC 과 맞나. 실기기 E2E 가 사용자 표면(앱)인가. infra 변경 없음 판단의 근거
8. **보안 · 권한**: 남의 방 · 사진 · 삭제 · 나간 사람 열람 · 토큰 · 로그
9. **public**: 실명 · 키 · 토큰 · KOS id · Apple 팀 id grep 0

「조용히 통과하는 자리」(시험은 초록인데 계약이 깨질 수 있는 곳)와 「사용자가 실물에서 만날 자리」를 따로 모은다.

## 5. allowed_paths: 이 밖은 건드리지 마라

- read-only. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r1.md`

## 6. 단계

1. §1 을 다 읽는다(시안 24장 · 코드 자리 전부)
2. §4 1 ~ 9 를 본다
3. rules.md 리포트 형식으로 쓴다. 지적마다 파일:줄 + 근거(D9-nn · DS:Sn · 코드 파일:줄) + FAIL/WARN. 끝에 「사용자 판단 후보」 표
4. §9 두 채널로 보고한다

## 7. 하지 말 것

- 문서 · 코드 수정 금지 · 커밋 · push · PR 금지 · 서버 · 앱 · docker 실행 금지
- 취향 지적 금지 — 근거가 없으면 쓰지 않는다
- 「지금 원천」 밖의 가상 상황으로 FAIL 을 만들지 않는다. 지금 DEC · 시안 · 코드 기준으로만 본다

## 8. 검증

```
SPEC·WORK 를 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 대조 수치: DEC n/37 · 장면 n/24 · §12 코드 자리 n/n 확인
- 리포트 끝에 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short`

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_61179808-14b1-431b-a85f-619d2c232e8e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
