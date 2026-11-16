
# [reviewer_doc] DAY 앱 SPEC 독립 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner가 쓴 SPEC 단계 산출물만 검수한다. planner 완료 후 실행되는 태스크다. 너는 앞 대화 맥락이 없으며 원천은 아래 최종 발주 브리프다. WP·코드 작성 금지. 모든 소스는 읽기 전용이다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/day-app-spec-brief.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/planner-spec-report.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/research-prototype-board.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `해당 없음` — 기존 DAY 계약이 정본. 사용자 발주와 모순되는 정책이나 임의 문구가 없는지 검수.

## 2. 배경 / 무엇을 바꾸나

사용자 승인 순서는 SPEC → 리뷰 → WP → 리뷰 → 코드 → 리뷰다. 이번 태스크는 최종 앱 SPEC의 첫 독립 리뷰. iOS 우선·DAY 로그인/컬러/권한·간호사 대리 수락·통역 매핑 사전·사용자 기준 푸시 연결·데모 로그인 시 dev 환경 연결을 누락 없이 검수한다. Apple 등록·서명·TestFlight·실서버 설정은 사용자가 한다. SPEC-003 신규 및 SPEC-001 로그인 변경을 중심으로 관련 문서 diff를 대조한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

planner 최종 브리프 §3이 사용자 결정을 담은 계약이다. 현재 dev와 새 계약의 차이는 명시돼야 한다. 미구현 API를 기존 사실로 단정하지 않는다. SPEC-002의 기존 JSON/SSE 계약은 존재한다(조사 보고서 부재 주장 정정). 새로운 통역/푸시 서버 구현까지 사용자 승인 없이 범위를 넓히면 안 된다. 데모 환경 연결용 백엔드 로그인 변경은 명시적 예외로 허용됐다. 방 이동/차트/시작취소 KOS는 옆 세션 담당.

## 4. 먼저 읽을 핵심 파일

- `products/day/20-spec/spec-003-mobile-app.md · 20-spec/spec-001-login-session.md · 20-spec.md · 10-decision.md · 40-architecture/mobile-deployment.md · /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/AGENTS.md·backend/day/routers/api/auth.py·board.py·schemas/auth.py·session.py · profile para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md §4` — git diff 기준 정확한 파일을 검수하고 실제 현재 계약과 구분한다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-spec-report.md 한 파일만 작성. 다른 모든 파일 읽기 전용.

## 6. 구현 단계

1. 역할과 mediness AGENTS.md를 읽고 git diff·새 파일을 확인한다. 최종 planner 발주 브리프와 실제 산출물을 항목별로 대조한다.
2. 데모 환경 연결: 인증 우회 없음·서버 데모 계정 판별·기존 서버 env 분리 유지·dev 실패 시 prod로 자동 우회 금지·pending 병원선택부터 token/API 대상 묶음 저장·재시작·만료·로그아웃·HTTP/SSE/WS/푸시까지 같은 환경·토큰을 임의 주소로 보내지 않음. API 응답 필드·분기·오류·인수조건이 구현 가능한지 확인한다.
3. DAY 권한 표와 can* 서버 판정·UUID·본인/간호사 대리 수락·재호출·귀가 대기 제거·시작 취소 유지·KOS 쓰기 담당 경계·프로토와 다른 곳을 검수한다. 앱 화면 문구/테마/폰·아이패드 배치의 원천이 명확한지 확인한다.
4. 통역 사전은 기존 170용어/7언어의 양방향 현지명/별칭 규칙을 소비하며 앱에 임의 번역/사전관리 화면을 추가하지 않는지 확인한다. 푸시 토큰은 로그인 유저와 자동 연결하며 별도 기기등록 화면이 없는지 확인한다. 서버 API 미구현과 사용자 담당 설정을 기능 제외/구현 완료와 혼동하면 지적한다.
5. 새로운 정책이나 미확정 API를 현재 사실처럼 쓰는 곳, 확인 불가능한 AC, 기존 로그인/병원선택 회귀, 허용 경로 이탈을 본다. WP를 SPEC보다 먼저 썼으면 FAIL.
6. python3 scripts/lint-pipeline.py --strict 1회. DAY 오류와 타제품 부채를 분리. 지정 보고서에 판정 PASS/WARN/FAIL, 각 지적의 파일:줄+결정/계약 근거, 수정 제안, 직원이 실물에서 만날 자리를 쓴다. 코드를 고치거나 문서를 직접 수정하지 않는다.

## 7. 범위 제약 — 하지 말 것

- read-only. 지정 리뷰 리포트 밖 수정·커밋·push·PR 금지. 서버·DB·시뮬레이터·기기·외부 API 조작 금지. 대화에 없던 제품 결정을 새로 요구하지 않는다.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_bfb1afc9-97a0-4d5b-bcab-aa5b6b982f00 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
