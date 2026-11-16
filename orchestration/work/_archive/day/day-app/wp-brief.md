
# [planner] DAY iOS 직원 앱 최종 SPEC 작성 — 시술현황·대리 수락·통역 사전·데모 환경 연결

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 대화 맥락이 없다. 이 브리프가 최종 사용자 결정이다. 다른 day-procedure-board-2 세션은 별도 워크트리에서 방 이동·차트·시작 취소 정리를 한다. 그 워크트리와 산출물을 수정하지 마라. 현재 태스크는 SPEC만. WP·코드·PR은 작성하지 않는다.

## 1. 먼저 읽을 것

- mediness AGENTS.md → context/manifest.yaml·index.md·current-state.md · rules/delivery-workflow.md · .agents/skills/start-delivery/SKILL.md · tools/harness/references/requests.md
- 이 태스크의 mediness origin/main은 fetch 완료: b4cd1a004cd99c8e57761ad8cccd434d5e237b38. 이 exact ref의 products/day/README.md·20-spec.md·SPEC-001 전문·실제 인접 SPEC-002와 SPEC-000 직원/기기 절을 git show로 읽는다. main에는 SPEC-003이 아직 없다.
- 로컬 리뷰된 초안 products/day/20-spec/spec-003-mobile-app.md 및 spec-001 변경·40-architecture/mobile-deployment.md. 로컬 초안은 제안 기준이며 origin/main의 Stable SPEC인 척 쓰지 않는다.
- profile orchestration/work/day-app/_RESUME.md · review-policy-report.md · planner-policy-report.md · planner-spec-fix2-report.md · research-prototype-board.md
- 코드 워크트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app (origin/dev = 91728737), AGENTS.md·backend/day/routers/api/{auth,board}.py·schemas/auth.py·session.py·services/auth.py. 읽기 전용.
- 옆 작업 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md 읽기 전용.

## 2. 이번 목표

사용자가 “이제 WP 만들어야지 GitHub 이슈로 만들거지?”라고 했다. WP는 신규 repo WP 파일이 아니라 CENTURION_DAY의 GitHub Delivery Issue 하나다. 지금은 발행할 request JSON을 작성하는 단계다. 코디가 독립 리뷰 뒤 mediness CLI로 --plan → --apply해 이슈를 만든다. worker는 GitHub에 쓰지 않는다.

## 3. 결과 계약

- idempotency_key: day/day-app, product_id: day, document_root: products/day, contract_version:1, target_specs: [DAY-SPEC-003, DAY-SPEC-001], spec_baseline_revision: b4cd1a004cd99c8e57761ad8cccd434d5e237b38.
- risk_level L3: 앱 신규 구축 + 서버 로그인 공개 계약 변경 + 환경 간 인증 전달. 과장해서 실제 운영 조작을 한다는 뜻은 아니다. 코드·배포는 아직 시작하지 않는다. L3 사람 계약 승인 gate는 CLI 결과대로 남긴다. 승인 receipt를 만들거나 사용자인 척 하지 않는다.
- main에 SPEC-003이 없으므로 spec-baseline pending이어야 한다. local draft를 Stable SPEC으로 결속하거나 target id를 main의 다른 ID로 바꿔 gate를 우회하지 않는다.
- 범위: Flutter app/ iOS 폰·아이패드 최초 구성, DAY 브랜드·로그인·병원선택·권한·시술현황·룸상세·현재 API의 마취·호출/재호출·본인/간호사 대리 수락·시작종료/취소·귀가대기·SSE, 사용자 기준 APNs 토큰 연결과 통역/7언어사전 소비 클라이언트. 사용자 승인 예외 D-1 로그인 환경연결: 고정 진입점에서 데모 계정 dev 인증, API주소+세션 묶음, 일반계정 prod, dev장애 prod우회금지. 코드PR은 하나→dev, 사용자가 말하기 전 머지금지.
- 통역은 해당 고객정보 보는 사람 모두. 푸시는 호출 대상 그대로(모든의사→병원 원장목록 전체/지정→그원장), 관리자 별도추가/호출자자동제외없음. 간호사 대리수락과 수신자 별개. 향후 코디→상담사 호출은 이번범위 밖.
- D-2 기기등록/APNs 발송 서버 전체, D-3 통역 WS/사전 서버 전체 구현은 이 작업에 승인되지 않음. 앱 소비 계약과 테스트더블 준비를 실제서버통합 완료로 쓰지 않는다. 서버 담당 미배정/사용자 준비 항목 정확히 명시. Apple 등록·서명·TestFlight·APNs/Soniox키·서버env는 사용자, 코드착수조건 아님/실물검증조건.
- 방이동·차트작성·시작취소KOS쓰기·seed스크립트는 옆세션 SPEC/머지 이후 소비. 원본프로토는 읽기만. backend는 D-1 로그인 변경·관련테스트 외 손대지 않는다. AGENTS의 서버주소규칙 정합수정만 코드단계 범위로 포함.
- 미결 OQ-A1/A9/A11·문구는 SPEC에 적힌 보류/원천그대로. 기능 임의 추가/번역/화면문구창작금지. 새로운 미결을 생성해 기존결정을 다시묻지 않는다.

## 4. 산출물

request reference 및 delivery-request.schema.json shape에 맞는 JSON 1개. target_delta·acceptance·non_goals·review_surface·execution(code_surface/dependencies/phases/verification/predeploy/rollback/open_questions)를 한국어로 쓴다. 기술근거가 있는 순서만. Acceptance에는 SPEC-003 A1~24/A14b/A16b와 핵심연결을 명시하고 더블검증/실물검증을 구분한다. iOS unsigned build·analyze·test, D1 auth pytest/ruff, 폰/아이패드검수, allowed_paths검사, 비밀미포함을 담는다. 실제서버키가 없어도 앱코드검증은 진행가능.

별도 사람이 읽는 WP 본문 파일을 원장으로 만들지 않는다. JSON은 CLI 입력일 뿐, canonical ledger는 생성될 GitHub 이슈다. 보고서에 검증결과·범위/의존성만 간결히 남긴다.

## 5. allowed_paths

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/delivery-request.json
- 같은 폴더 planner-wp-report.md
그 밖 모든 파일 읽기전용. products/day/30-work.md, 30-work/, SPEC, 코드 수정 금지.

## 6. 검증

JSON 파싱·스키마검증, baseline SHA·target ID·Acceptance와 NonGoals가 충돌하지 않는지 대조. CLI apply·Issue/PR 생성·커밋·push·배포·MCP Task draft 금지. 보고 후 코디가 WP 독립리뷰를 발주한다.

## 7. 이번 단계 금지

코드구현/서버·기기 조작/실자격증명 읽기/승인receipt 생성 금지. 이미 리뷰한 SPEC을 재작성하지 않는다.

## 8. 완료

request JSON과 보고서만 남기고 새 preamble id의 worker_done으로 완료한다. GitHub 이슈는 아직 생성하지 않았다고 명시.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_6acba11d-0262-431b-aea2-37a4e7366b4b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
