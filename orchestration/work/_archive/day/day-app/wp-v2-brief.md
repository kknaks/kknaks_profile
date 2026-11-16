# [planner] DAY 앱 WP v2 — 기존 Delivery #235 갱신 입력 작성

너는 DAY planner. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/ 문서 및 mediness AGENTS.md 라우팅을 따른다. 앞 맥락은 이 브리프로 복원한다. 하위워커/내부서브에이전트 금지.
작업트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec, HEAD1551fa22dfe23f36d6c3ebe443337225fc6277f1, 기존 SPEC PR921 OPEN. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD0b776e90, PR237 OPEN→dev. 기존 앱/D1 구현은 완료·리뷰PASS이나 최신UI는 미반영.

## 1. 먼저 읽을 것
- mediness AGENTS.md→context 및 rules/delivery-workflow.md, .agents/skills/start-delivery/SKILL.md, tools/harness/references/requests.md, 실제 request schema.
- profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/_RESUME.md, ui-spec-brief.md, planner-ui-spec-report.md, planner-ui-spec-fix-report.md, review-ui-spec2-report.md.
- products/day/SPEC003 전문 exact HEAD1551fa22(사용자교정13항목) 및 SPEC001/002, README/20-spec. fetch완료 latest origin/main exact3f57c1af09afa7ce185cd754244c714bf1ec11e5의 README/20-spec/target SPEC git show. main에SPEC003없음·SPEC001stable없음은 pending그대로.
- 같은 profile작업폴더 delivery-request.json(v1 입력), delivery235-current.json(현재 GitHub #235 스냅샷), delivery-approved-result.json, mobile-fix1-report.md 등 기존구현증거.
- 옆세션 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md 및 /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md read-only. 옆코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2 HEADa1c90b9dc63271dc06023ec0a530c53a216a296c는 미머지·코드실물 확인용이며스펙권한아님.

## 2. 사용자 최신지시·범위
「백엔드 수정 거의 끝나서 wp 작업 해도 될거 같아」. 이번은 기존 #235 WP 결과계약+실행계획 갱신·독립리뷰까지만. 코드구현/스펙수정/머지 안함. 기존승인은v1이고UI수정으로계약의미가바뀌므로version2·scope_delta, 승인receipt복제/대행금지. CLI plan/apply는코디몫. GitHub WP이슈하나·코드PR하나를유지, 신규이슈/WP문서없음.

## 3. WP v2 계약
- idempotency_key day/day-app, product_id day, document_root products/day, contract_version2, target_specs 기존DAY-SPEC-003/DAY-SPEC-001 유지. risk L3는 원래D1환경인증전체계약을보존하는누적Delivery이기때문에유지. spec_baseline_revision latestmain3f57c1af…이며pending, 로컬1551fa22를mainready로위장금지. 정확한fullSHA로작성.
- 결과는 최초구현재발주가아니라 기존코드유지+사용자확정UI교정13항목. SPEC003 A25~36/U계약, A2원장즉시/간호대리, 4메뉴/알림아이콘·설정계정, 4필터, 4행카드, 마취한줄, 목록수락, 상세/시술카드/완료하단회색/세로더보기, 상세→호출시트체크+원장, 전체완료귀가강조, 원형통역드로어/칩, TW언어매핑, 성공토스트2.6초·되돌리기없음을누락없이Acceptance에매핑.
- 이전 A1~13+환경/로그인/세션보안/SSE/푸시·통역클라이언트/D1 완료근거는보존. 과거통과155앱/47native/663서버수치는옛exacthead검증이라는실행기록, 새UI완료로체크하지말것. D1기능을새로고치는task를재발주하지않고완료된기존기반/회귀대상으로표시.
- **이번 후속 구현 변경 경로는app/만**. 기존PR의D1 backend변경은누적diff에남되새backend/웹/배포설정수정승인으로쓰지않음. app기반회귀검사+필요한스크린샷시각검수 포함, 원본프로토read-only.
- D2APNs/기기등록/D3통역사전서버/D5알림API 구현은아직범위밖. 종은보여도계약없이는가짜배지/경로/목록만들지않음. 설정은계정·로그아웃만, 채팅상세는후속, 예약문구곧출시예정. Apple/서명/TestFlight키/env사용자.
- 코드PR237→dev그대로, 모든머지사용자마지막명시지시때만. 문서선머지게이트를다시만들지않음(사용자가11/09직접폐기). baselinepending정직유지. 코드착수는이번사용자범위아님.

## 4. 옆세션과의 호환 — 반드시 구분
새옆SPEC002/코드는앱003의옛업무전제와다름: 재호출항상called줄·취소확인모달·확인필요추가이유·반복마취·원장변경등. 정확한원천/줄/sha와계약차이를조사해review_surface+dependencies에표시. 원장변경푸시/방이동/차트를이번앱범위에자동추가하지않음. **충돌을판단/덮어쓰기/코드적용하지말고** 「UI작업계획은작성, 해당업무동작구현전최신병합SPEC002와003대조·스펙정합필요」라는구체dependency/phase로둠. 기존SPEC003 A22를슬쩍always로바꾸거나확인모달없음과있음을동시에Acceptance로약속하지않음. 이번은WP작성목표라호환검토는남겨도된다. 다른세션진행상태/머지완료를추측하지않음.

## 5. 산출물·allowed_paths
profile작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ 안 delivery-request-v2.json, planner-wp-v2-report.md 두개만생성. JSON은CLI입력·보고서는발주결과, 별도WP원장아님. 스펙/30-work/코드/다른세션읽기전용. GitHub/CLIapply/승인receipt/커밋/push금지.

## 6. 검증
JSON파싱+실제schema검증(필요시CLIplan은읽기전용이지만코디가하므로worker는안함). scope_delta참조형식확인. 원문13항목+기존Acceptance회귀/NonGoals충돌0, 코드·문구·번역·API발명없음. 검증결과와호환차이·완료기반/남은단계를한국어로간결보고.

## 7. 남은미정
SPEC003OQ-A8/A21/A27/A28등은기본값·후속확인점그대로. 새확인질문이나승인단계를임의추가하지않음. 다른원장지정호출본인수락은현서버성공사실을보존, 새차단정책없음.

## 8. 완료
live preamble의Task/Dispatch/핸들/outcome우선. 마지막메일확인후worker_done한번·idle. 코디가독립리뷰후기존235에apply한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
