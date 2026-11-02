# WORK002 수정1차 한정 재검수

## 1. 역할
기존 리뷰어 세션 재사용 허용. 이전 검수 결과를 활용해 수정된 F1~5/N1~6만 재검수한다. 원문/코드 전수 조사는 반복하지 않는다.

## 2. 입력
WORK002 최신 실물, v2-work-fix1-report.md, 기존 review-v2-work-report.md. Phase0 새 증거 v2-phase0-verification.md와 4개 exit/log, v2-be-phase0-report.md 정정 U6.

## 3. 판정
수정1차의 5 FAIL과 6 WARN 닫힘, 수정이 직접 만든 계약 모순만 검수. 테스트 322/976/645/65 exit0는 지금 코디가 직접 실행한 변경전 기준선이며 반복 불필요. W1 과거로그 재사용 아님. ax_demo 0표/ax_test_w1 업무0행은 실데이터 검사완료 근거가 아님. WORK의 배포 인수조건과 구현착수 조건을 구분하여 로컬 BE/FE 독립구현 가능 여부를 판정한다. OQ203/206 좁은 답의존은 유지. 전체계획 재조사/새 스타일지적 금지. 필요한 수정이 있다면 정확한 최소 문장 제시.

## 4. 산출
기존 review-v2-work-report.md 끝에 재검수1차 절만 추가. 짧은 해소표와 결론. 제품 코드/문서 수정·DB·테스트 실행 없음. 2채널 완료 후 idle.

## 5. allowed_paths
orchestration/work/strong-hajin-work/review-v2-work-report.md 만.

## 6. 금지
커밋 push PR 추가발주 금지.

## 7. 범위
기존 N7 index 코디 소유는 구현차단 아님.

## 8. 완료
새 dispatch의 ID 사용, 이전 ID 재사용 금지.

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
