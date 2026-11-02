# [reviewer] WORK002 검수 — 오늘 BE+FE 구현·검증까지 진행

## 1. 역할/SSOT
orchestration/roles/strong-hajin/reviewer/role.md 및 rules/skills/tools/workflow. para/projects/project.md 및 templates/projects/30-work/work.md.
최신 SPEC003 v0.3.1/DEC002/BASE002, WORK002 work-002-task-lifecycle-v2.md, v2-work-plan-report.md. 원문4종+design-change 분석+실제시안 참고. 코드 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 읽기전용. 사용자 BE+FE 개편 오늘 구현완료 목표, E2E 사용자. 시간핑계로 검증 축소 금지, 다만 기존 스펙 검수 반복 말고 WP실행가능성에 집중.

## 2. 작업
WORK002 전체검수: code surface/단일기술안/migration실재/phase작업·검증·증거/Makefile준수/BE FE공유소유/권한/멱등/회귀검증과 A1~C2/U1~15 추적. 실제 코드확인 기반 PASS/WARN/FAIL. WP 전부TODO, 코드수정없음.

## 3. 코디 집중지적
1. 보고의 '없어서 안그림'이 승인된 시안을 무단축소하지 않았는가. 별표는 신규기능이 필요한 사실이지 구현불가 이유가 아님. 미읽음/근무시간 등 미정정책과 단순데이터추가 기술선택 구분. 시안데이터 없는 기능을 임의로 전체제외하거나 inert UI로 대체 금지. SPEC에서 명시유보된 범위와 WP가 임의제외한 범위 구분해 정확히 보고.
2. SPEC done+awaiting_review vs 내부 COMPLETION_SUBMITTED는 외부투영으로 풀 수 있는지. 코드의 내부상태를 외부계약변경 질문으로 자동승격 금지. 두값모두 읽는다는 계획이 '요청done에는 승인행필수'를 깨는지 확인.
3. open→done은 SPEC명시계약이다. A9를 in_progress 경유테스트로 바꾸어 계약위반을 숨기는 계획 금지. 계약대로 전이를 구현/테스트해야 함. 기존W1부채여도 v2직접계약은 검증에서 회피 불가.
4. OQ203/206 답대기, 시간지남 승인아님. 독립범위 계획/구현 진행가능. 사용자답 필요한 좁은 작업을 합의없이 기본값구현으로 덮지 말 것.
5. migration 기존표index를 '사람이' 처리한다는 한줄로 자동검증/재현 누락금지. readonly관측→격리PG/검증가능 DDL 계획과 운영적용 단계 구분. W1미커밋baseline보존.
6. M20~24 기술UX선택이 SPEC에 이미 허용된 것인지 확인. 새계약 필요시 정확한 최소환류 제공, 작업 전체를 질문으로 막지 말 것.

## 4. 결과
막는 결함과 비차단 문구 구분. 각 지적 파일줄+근거+최소수정. 즉시발주 가능한 BE0/1·FE독립 준비범위 판정 제공(단 전체WP 검수 전 코드발주 금지). 같은결함 여러ID로 부풀리지 않음. 구체적인 수정문장 제안으로 다음수정 한회에 닫을 수 있게.

## 5. allowed_paths
orchestration/work/strong-hajin-work/review-v2-work-report.md 하나만. 제품문서/코드/reference/디자인 수정금지.

## 6. 확인하지 않는 것
DB/테스트/빌드/브라우저 실행없음. 기존원문추적 전수반복불필요. 기존코드 관측상태 vs 검증결과 구분.

## 7. 금지
commit/push/PR/stash/reset/checkout/새발주 없음.

## 8. 완료
읽기검수 후 2채널 보고. 현재 코디 handle은 term_9de388d5-58b1-4bbe-8864-5e930def648b 이며 live terminal list ORCA_TAB_ID로 재확인함. 옛 term29f는 stale.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_6c69a3df-4dd6-4b56-ad9b-52133dd8efbc \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
