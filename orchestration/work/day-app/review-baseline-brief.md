# [reviewer_doc] DAY 앱 stable 기준선 최종 독립 검수

너는 day reviewer_doc, read-only다. 앞 대화 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer_doc/`의 role.md·rules.md·skills.md·tools.md·workflow.md, mediness AGENTS.md를 읽는다.

## 1. 대상
`/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec` branch kknaksss/day-app-spec. 현재 로컬 다섯 문서는 SPEC/WP의 이전 독립리뷰 PASS 산출물이다. origin/main exact 3f57c1af09afa7ce185cd754244c714bf1ec11e5는 기존 b4cd1a00 이후 planning 원문 추가만 있다. 코드 구현은 미착수.

## 2. 근거
profile `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/`의 review-policy-report.md, review-wp2-report.md, planner-baseline-report.md, baseline-brief.md, delivery-request.json, delivery-plan-approval.json을 읽는다. Issue #235 https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235 사용자 2026-11-09 “응 진행하자 !” 결과계약 승인. start-delivery/문서파이프라인 규칙과 target SPEC001/003 전문을 대조.

## 3. 검수
SPEC001/003 stable 상태·인덱스 정합, coverage GitHub Issue 연결, 배포문서 정합을 확인한다. 기존 PASS 이후 승인 결과계약이 바뀌었는지 git diff 및 보고서로 확인. 통역=고객정보 보기권한, 푸시=기존 호출대상, 간호사 대리수락, prod 로그인에서 demo dev 넘김 fail-closed, 60/75초·/me 후 원자저장·allowlist·redirect금지 유지. D1 로그인 변경만 backend 승인 예외, D2/D3 전체서버는 범위밖·앱 더블검증만, 방이동/차트작성은 옆세션. 미정 문구 창작금지. OQ-A1/A9/A11 보류 유지.

## 4. 우선순위
최신 main에 추가된 planning은 과거 원문 snapshot이다. 최신 사용자 직접 결정과 다른 경우 최신 직접 결정이 우선임을 보고하되 이미 승인한 결정을 다시 미정으로 만들지 않는다. 승인 범위에 없는 새 의미 충돌만 구체 근거로 FAIL한다. 없는 기능/검증을 완료라고 선언하는 부분이 없는지 본다.

## 5. 권한
모든 레포 read-only. profile 작업폴더 review-baseline-report.md 보고서 하나만 생성한다. 코드/스펙/원장 수정·커밋/push/PR/GitHub write 금지.

## 6. 검증
lint --strict (DAY ERROR0, 기존 외부 warnings 구분), git diff --check. 상태 이외 결과계약 의미 변화 0인지 판정. 보고서 PASS/WARN/FAIL 및 차단 여부·실제 명령·근거를 쓴다.

## 7. 완료
리뷰판정과 남은 위험을 보고한다. stable main 도달·서버통합·코드완료로 오인하지 않는다. 코디가 커밋/rebase/PR을 준비한다.

## 8. 통신
live preamble id와 핸들 우선, worker_done --outcome succeeded/failed 필수. 아래 legacy §9는 보존하되 preamble을 따른다.

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
