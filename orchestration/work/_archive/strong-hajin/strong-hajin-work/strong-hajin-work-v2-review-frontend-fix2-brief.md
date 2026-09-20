# FE N-1 정정 최소 재검수

## 1. 역할
원reviewer 재사용, 원래 FE 검수 전체를 반복하지 않는다. 같은 코드 워크트리 read-only.

## 2. 입력
v2-frontend-fix2-report.md·strong-hajin-work-v2-frontend-fix2-brief.md·review-v2-frontend-report.md 재검수1차 N-1 및 실제 변경된 게이트만. fix2-* 로그/exit는 v2-frontend-verification/에 보존돼 있다.

## 3. 범위
isRequestRecordRequester가 raw requester_id만 읽어 BE _requester_of와 일치하는지, 제안의 requester/promoted_by 두항은 그대로인지 확인. 일반 요청자·본인·배정·오늘/캘린더 재개 보존, 승격자의 제안은 보존하고 서버가 거부하는 재개만 숨김. 회귀2건·706passed/tsc0 실제로그 대조. OQ206 승인자 미결은 그대로이며 승격 재개 정책을 새로 확정한 것이 아니다.

## 4. 제외
새 디자인/첨부/전체FE 재조사 없음. 앞선 검수의 닫힌항목 재개방 불필요. 제품코드·다른문서·DB·테스트실행 무수정/미실행. BE통합검수는 별도.

## 5. 허용 파일
orchestration/work/strong-hajin-work/review-v2-frontend-report.md에 재검수2차 짧은 절만 append. 커밋/push/PR/새발주 금지.

## 6. 결과
N1 해소여부·증거만. 새 결함을 발견하면 파일/줄/실제조건/최소수정. 최종 build·verify 미실행은 그대로.

## 7. 검증
읽기전용. 전량검수 반복 금지.

## 8. 완료
두채널 보고 후 idle.

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
