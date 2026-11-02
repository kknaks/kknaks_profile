# [reviewer] 직원 앱 내부 채팅 — 코드 검수 r1 (procedure/back · procedure/app)

너는 **cc-prototype `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` (**read-only** — 미커밋 변경이 검수 대상이다. `git -C /Users/kknaks/orca/workspaces/cc-prototype/internal-chat diff` · `git status`)
base 브랜치: `origin/main`(`dbf0b53`) → 최종 PR 대상 `main`

## 0. SPEC 보충 — 브리프 §0 처분이 SPEC 보다 이긴다

backend · mobile 브리프 §0(review-doc r2 W2-1 ~ W2-6 처분 · DEC D-45)이 SPEC-007 0.2.0 보다 이긴다: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` §0

## 1. SSOT — 대조 기준

1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` 0.2.0 + 위 §0
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` — **WP-REVIEW 행이 검수 목록이다**(전부 본다)
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` D-01 ~ D-45
4. 확정 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design/Ceramique 의료진 앱 — 채팅.dc.html` (헤더는 D-38 이 이김)
5. 문서 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r1.md` · `review-doc-r2.md` 의 「조용히 통과하는 자리」 — 코드에서 실제로 막혔는지 본다

**기대는 개념**: 해당 없음

## 2. 배경

backend(WP-BE1 · BE2 · pytest 500 · ruff 통과)와 mobile(WP-APP1 ~ 3 · analyze 0 · test 184)이 끝났다(코디가 두 수치 다시 돌려 확인). 다음은 코디가 로컬 back + iOS 시뮬레이터 2대로 사용자에게 보인다. **사용자가 시뮬레이터에서 만날 자리**를 특히 모은다.

## 3. 계약

해당 없음 (검수)

## 4. 볼 것

1. WORK-011 WP-REVIEW 행의 항목 전부(async def · 밀리초 · since >= · id 기준 안 읽음 · 배너 층 · 멤버 아닌 404 · 붙기 전 사진 · clientId · 푸시 대상 · 만료(호출 0 회귀) · notification 0 · SSE 받는 연결 · Bearer · 사진첩 0 · 디스크 캐시 0 · 주석 4 · 실명 · 키)
2. SPEC-007 §6 API 14 · §7 SSE 5 · §8 푸시 payload 를 back 구현과 app 소비 **양쪽**에서 필드 이름 · 타입 · 꼴이 맞는지(한쪽만 맞으면 FAIL — 둘이 따로 지었다)
3. §0 W2-1 ~ W2-6 이 코드에 있나
4. 시안 장면 24 → 화면 코드(헤더 = D-38)
5. 기능 독립(procedure 밖 import · 다른 기능 폴더 변경 0) · 기존 기능 회귀(원장 · 상담사 호출 · 띄우기 · 여권 사진 · 알림 목록)
6. 「조용히 통과하는 자리」 · 「사용자가 실물(시뮬레이터 · 실기기)에서 만날 자리」

## 5. allowed_paths — 이 밖은 건드리지 마라

- read-only. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r1.md`

## 6. 단계

1. diff 전체를 읽는다(back · app)
2. §4 를 본다 — 필요하면 `uv run pytest -q -k …` · `flutter test <파일>` 을 읽기 목적으로 돌려도 된다(파일을 만들거나 고치지 않는다)
3. rules.md 리포트 형식 · 지적마다 파일:줄 + 근거(SPEC 절 · D9-nn) · FAIL/WARN
4. §9 두 채널로 보고

## 7. 하지 말 것

- 코드 수정 · 커밋 · push · PR 금지
- 서버 · compose · 시뮬레이터 · 기기 실행 금지(사용자 포트 · 프로세스)
- 취향 지적 · 지금 원천 밖 가상 상황 FAIL 금지

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 기능 독립 위반은 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

- WP-REVIEW 항목별 결과 표 · API 14 / SSE 5 / 푸시 payload 양쪽 대조 수치

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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
