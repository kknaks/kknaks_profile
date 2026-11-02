# [reviewer] SPEC003 v0.3.0 재검수2차 — 정정과 신규 UX 계약

## 1. 역할/SSOT
orchestration/roles/strong-hajin/reviewer/ 의 role/rules/skills/tools/workflow 읽기. 문서 workspace 현재 strong_hajin, 코드 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 읽기전용.
reference/2026-09-10-sc-meeting/ 원문4종 + design-change-2026-09-17 분석4문서 + 코드 .design-sync/screens/ 실물. 분석보고는 과거스냅샷 기준, 최신 SPEC과 비교 필요.
최신 사용자 승인: 프론트도 이번 작업에 포함, BE+FE통합 WORK002/구현. E2E 사용자 유지.

## 2. 대상
BASE002/DEC002/SPEC003 v0.3.0 및 SPEC001/002 상단안내. 수정발주 strong-hajin-work-v2-spec-fix2-brief.md / 작성보고 v2-spec-fix2-report.md. 판정원장 review-v2-spec-report.md 재검수1차 RF1~2/RW1~6, 디자인 분석부기.

## 3. 정정 확인
RF1 요청자 조작과 완료확인 주체분리, 승인가능사람0 기본값 폐기, OQ206 완료확인만 미정. RF2 정상 기존done 승인사실 매핑/실행DB 예외관측 분리, OQ205 질문폐기. RW1/2 기존 Task투영 응답 유지, 결과상태와 입출력 동일성 구분. RW3 인용문구로 지목. RW4 completion-report/submit_completion과 승인 실제동작 관측정정, 기존 API호환. RW5 상태도, RW6 질문담당정리.
기존 초판 전수검수는 반복하지 않고 수정으로 깨진 곳만 확인. OQ203/206은 사용자에게 이미 질문했고 답대기, 다시질문 늘리지 말 것. 미정을 미정으로 남긴 것이 자체 FAIL은 아니다.

## 4. 신규 UX 계약 검수
SPEC003 §2 UX/§6 U1~15 및 DEC 범위변경이 최신 사용자승인과 맞는가. 프론트 제외 옛지시가 현행문장에 남지 않는가. 시안의 탭/표/모달/레일을 현재코드에 맞춰 임의 축소하거나 구현불가 단추로 남기지 않는가. v2 상하위/수락/승인/재배정/취소재개와 UI명령이 일치하는가. 시안빈곳=정책부정으로 오해 금지.
M20~24를 무작정 범위밖으로 미뤄 승인된 FE개편을 빠뜨리지 않았는지 확인: 기존데이터로 구현할 수 있는 것은 관측/기술선택으로 닫고, 새 서비스 전체를 사용자 확인없이 추가하지 않음. 미정의 화면 조각/사용자 영향/후속조사 책임 구체성 검수. 원문이 답한 StateSwitch 제외·상태매핑·탭축 구분 등에 질문 신설 금지. 결과 UI와 BE계약을 함께 확인하고 코드경로는 BASE, 구현단계는 WORK 경계 준수.

## 5. allowed_paths
orchestration/work/strong-hajin-work/review-v2-spec-report.md 에 재검수2차 절만 추가. 기존본문 보존, 모든제품문서/코드/디자인/reference read-only. 해시 고정.

## 6. 결과
PASS/WARN/FAIL + 지적별 근거/최소정정. WORK002 즉시 작성가능 범위, 의존미결 명시. 전체무한재조사 금지. W10 index/log는 코디소유이므로 writer FAIL 아님.

## 7. 금지
코드/문서정정/테스트/빌드/DB/브라우저E2E/커밋/push/PR/stash/reset/checkout 금지.

## 8. 검증
읽기대조만, 실행검증0. 완료1회 후 idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --from term_4994ba2f-dd6a-4714-af58-632b3fdbb89a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
