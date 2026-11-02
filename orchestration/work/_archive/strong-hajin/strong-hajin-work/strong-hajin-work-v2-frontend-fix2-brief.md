# v2 FE 재검수 N-1 최소 정정

## 1. 역할
원 frontend 재사용, 같은 코드 워크트리. review-v2-frontend-report.md 재검수1차 N-1만 수정. 신규 정책/전체 화면 재작성 금지.

## 2. 문제
제안은 BE _is_request_owner가 requester_id/promoted_by_member_id 둘 다 허용하지만 재개는 _requester_of가 requester_id만 허용한다. FE가 viewerIsRequester를 공유하여 승격자에게 서버가 거부하는 재개를 보인다. 미정 OQ206을 기본값으로 확정하지 않고 현재 서버 권한에 맞춰 노출을 좁힌다.

## 3. 수정
일반 요청자와 회의 승격자를 분리해 재개 게이트에 실제 requester_id 판정을 사용한다(제안 게이트는 현재 정정 유지). 본인 업무와 기존 배정의 재개·오늘/캘린더 경로는 보존. 서버 입력/역량 변경 금지. 이 정정은 OQ206 승인자 결정이 아니며 해당 완료 승인 미결을 닫지 않는다. 기존 과거 데이터가 있어도 항상 실패하는 버튼을 내지 않는 것이 목적.

## 4. 테스트
일반 요청자의 재개 유지, system:meeting 요청의 promoted_by에게 제안은 허용하지만 재개는 미노출이라는 회귀. make frontend-test 한 번과 npx tsc --noEmit. 전체 build/verify는 코디. 로그·exit 보존. 재차 전량 반복하지 말고 실패원인/수정을 먼저 한다.

## 5. allowed_paths
frontend/의 해당 게이트와 직접 관련 테스트만. orchestration/work/strong-hajin-work/v2-frontend-fix2-report.md 완료 보고만. BE·SPEC·WORK·다른문서 무수정. 커밋/push/PR 금지.

## 6. 보고
변경 파일/정확한 게이트/테스트 수치/미결 보존을 짧게. 앞선 검수 전체와 보고서 재작성 금지.

## 7. 실행
코드 AGENTS 준수, 브라우저 E2E 실행금지.

## 8. 완료
두채널 보고 후 idle. 새 워커 발주 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_87c176ee-8845-4561-bed6-71414b1ed3e5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
