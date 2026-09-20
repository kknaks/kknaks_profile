# [reviewer] W1 마지막 R1~4 최소 확인

## 1. SSOT
기존 코드 리뷰 브리프와 review-code-report.md 재검수1차. backend-review-fix2-report.md(완료 메시지 보존).
## 2. 목적
R1~4만 확인. 기존 PASS 재개방/전체 재조사 없음.
## 3. 항목
R1 README/domain-model 요청422·403·404 vs 배정422·404 문장 정합. R2 승격 actor/history 단언. R3 active없는 순간 열람 경계 테스트와 fallback 분기 자체를 가르지 못하는 한계 명시. R4 pending 주석·넓은 단언 정정.
## 4. 범위
README/domain-model 및 test_task_actor/test_meeting_finalize/test_task_creation_contract의 마지막 수정. 제품 코드 무변경 확인.
## 5. allowed_paths
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md 재검수2차 절만 추가.
## 6. 결과
짧은 항목별 판정과 최종 PASS/WARN/FAIL. 새 실제 회귀만 추가.
## 7. 제약
코드/문서 수정 금지. 테스트/빌드/DB/E2E 미실행. 커밋/stash 금지.
## 8. 검증 상태
코디 BE1297+scale13+release1(병렬4), PG65 통과. Node25 FE localStorage 실패 후 Node20.20에서 FE645/assets/build exit0. 단계별 통과이며 단일 make verify green 아님. 마지막 제품 코드 변경없고 scoped84 exit0 보고. E2E 사용자 담당.

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
