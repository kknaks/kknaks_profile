# [reviewer] W1 통합 코드 재검수 1차

역할/워크트리/기존 SSOT/읽기 전용 규칙은 앞 strong-hajin-work-review-code-brief.md와 동일.

## 1. SSOT
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md F-1·W-1~7 및 backend-review-fix1-report.md, frontend-f1-fix.diff. BE/FE review-fix1 브리프.

## 2. 목적
마지막 지적의 해소와 수정이 만든 회귀만 좁게 검수. 이미 PASS 항목 재개방 금지.

## 3. 확인
F-1: FE horizontal start_date 미노출/미전송/지문·validation 분리, self/managed 유지 + BE 3필드 422/no effect.
W-1: horizontal AX 계보가 실제 Task까지 전달되고 replay에서 소실/중복 없음.
W-2: 신규 caller·회의 승격자·legacy 수락자 각각 실제 actor/history. 열람 권한 회귀.
W-3~6: README 권한·AX 현행 경로·회의 실제 route/잠금·evidence vs 업무 자료 경계.
W-7: 정확한 4xx 단언/키 누락 모든 표면/낡은 주석·불필요 호출 정정.

## 4. 특히
source refs 중 일부만 보존되거나 actor를 requester로 일괄 치환한 곳 없는지 확인. 자료 worker/lease 제품 코드는 원복됐고 이번 변경에는 없다는 보고를 diff로 확인.

## 5. allowed_paths
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md에 재검수 1차 절 추가만. 코드/테스트/문서 무수정.

## 6. 결과
항목별 해소/잔여, PASS/WARN/FAIL. 기존 부채와 새로운 회귀 구분.

## 7. 제약
테스트/빌드/DB/E2E 실행 금지. 커밋/push/PR·stash 금지. 테스트 수치만 보고 PASS 하지 않는다.

## 8. 실행 검증 상태
코디 make verify 앞 실행은 1289 passed/자료 worker2 실패. 부하에서 3초 lease 전제를 충족 못한 원인 보고 수령. 코디는 테스트/단언 변경 없이 xdist 자동 worker 수 4개로 제한한 make verify와 격리 PG 최종 검증 예정. E2E는 사용자 담당.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --from term_fd9e957e-c7d0-4e8e-a59c-c14c600da674 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
