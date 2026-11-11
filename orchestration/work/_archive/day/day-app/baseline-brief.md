# [planner] DAY 앱 승인된 SPEC 기준선 확정

너는 day planner다. 앞 맥락이 없다고 보고 이 한 장으로 진행한다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/`의 role.md·rules.md·skills.md·tools.md·workflow.md와 mediness AGENTS.md를 먼저 읽는다.

## 1. 대상·현재 상태
작업 트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`, 브랜치 kknaksss/day-app-spec. 현재 HEAD b4cd1a004cd99c8e57761ad8cccd434d5e237b38. origin/main은 3f57c1af09afa7ce185cd754244c714bf1ec11e5로 fetch됨. 그 사이 변경은 planning 원문 추가뿐이고 현재 수정 5파일과 교집합 없음. git 작업은 코디 몫: commit/rebase/push/PR 금지.

## 2. 근거
profile 작업폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/`의 review-policy-report.md(PASS), review-wp2-report.md(PASS), delivery-request.json, _RESUME.md를 읽는다. mediness rules/delivery-workflow.md, .agents/skills/start-delivery/SKILL.md 및 target SPEC001·003 전문/20-spec 인덱스/30-work coverage/배포문서를 읽는다. 최신 origin/main의 README·20-spec·인접 SPEC000/002도 읽되 수정금지.

## 3. 사용자 승인
사용자는 GitHub Delivery #235 결과계약에 2026-11-09 “응 진행하자 !”로 명시 승인했다. 코드 PR 하나→dev, merge 별도 사용자 지시라는 경계 유지. L3 승인 digest sha256:c4f70ae3f97540fbe9b54c2b9d8698395e58cd9a509e393308a52d59cca5c75e. 현재 계약 의미를 바꾸지 말고 이미 독립리뷰 PASS인 SPEC001/003을 stable baseline으로 만들기 위한 최소 문서 변경만 한다.

## 4. 변경
SPEC001/003 frontmatter status stable 및 인덱스에 대응 상태 동기화. 30-work의 SPEC003 coverage가 아직 WP 미발주라고 하는 오래된 표현을 GitHub Delivery Issue https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235 기준으로 바로잡는다. 기존 coverage 형식과 CLI 원칙에 맞게 하고 별도 WP 파일·원장 생성금지. 타 SPEC 상태를 건드리지 않는다. 앱 동작/권한/라우팅/푸시/통역/보류/OQ 등 승인된 내용 변경금지. 표/링크/lint 오류만 고친다. 최신 planning 원문이 승인된 결정과 의미 충돌한다고 판단되면 임의 변경하지 말고 근거를 보고한다.

## 5. 권한·범위
수정 가능: mediness products/day/20-spec.md, 20-spec/spec-001-login-session.md, 20-spec/spec-003-mobile-app.md, 30-work.md, 40-architecture/mobile-deployment.md. 기존 로컬 미커밋 변경은 앞 단계의 승인된 산출물이므로 보존한다. profile에는 작업폴더 planner-baseline-report.md 보고서 하나만 쓴다. 다른 워크트리/옆세션/코드/실서버/환경비밀파일 수정·조작 금지.

## 6. 검증
mediness CLI lint --strict를 레포 규칙대로 실행(전역 warning은 분리, DAY ERROR 0), git diff --check, 두 SPEC stable·인덱스 상태·issue coverage 정합을 확인. 승인 결과계약이 바뀌지 않았다는 비교 근거를 보고. 기존 다섯파일을 통째로 재작성하지 않는다.

## 7. 완료
변경파일, 실제 검증명령·수치, 상태 변경 이외의 의미 변화 여부를 planner-baseline-report.md에 남긴다. 코디가 독립 리뷰 후 commit/rebase/push/PR 준비. 실제 main baseline ready나 구현착수를 선언하지 않는다.

## 8. 보고 주의
live preamble task/dispatch/코디 핸들이 §9 예시보다 우선. worker_done은 --outcome succeeded/failed를 반드시 포함한다. 아래 legacy 완료 블록은 보존하지만 live preamble의 정확한 보고 규약을 적용한다.

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
