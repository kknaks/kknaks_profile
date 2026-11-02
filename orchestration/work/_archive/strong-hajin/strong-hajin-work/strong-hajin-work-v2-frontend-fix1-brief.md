# v2 FE 검수 정정 1차

## 1. 역할과 입력
원 frontend 워커 재사용. 이전 WORK002 구현의 후속이며 동일 코드 워크트리에서 작업한다. SPEC003·WORK002·review-v2-frontend-report.md를 읽는다. BE는 독립 구현 중이므로 backend/ 수정 금지. W1 미커밋분 보존.

## 2. 필수 수정
F-1: 제안 버튼은 요청자만 보인다. 수락 전 요청 업무의 직접취소도 서버 명령 권한과 맞춘다. origin.actor와 실제 BE 요청자/promoted_by 판정을 대조하고 단순 assignee 여부로 요청자를 추정하지 않는다. 요청자·담당자·제3자·본인/관리 배정 경로의 버튼 회귀를 추가한다. 요청자 자신의 정상 기능은 보존한다.

## 3. 함께 닫을 WARN
W-1: TaskChild에서 죽은 보수 분기를 정리하고 주석을 실제 의미에 맞춘다. 서버 derived.approval/blocking_children가 원장이고 누락 값에서 요청 업무를 발명하지 않는다.
W-3: include_removed 조회 실패 때 사용자에게 숨긴 목록을 읽지 못했음을 알린다. 성공한 일반 목록을 빈 목록으로 버리지 않는다. 실제 첫 실패에서 경고가 나야 하며 일반 목록까지 실패했을 때만 경고하는 형태는 안 된다.
W-5: 보고의 회차별 수치를 원본 로그대로 정정한다. 로그가 없는 681 통과는 검증 근거에서 제외. 82/82는 착수 시점임을 명시.

## 4. Phase7-A 원래 범위
WORK에 첨부 DropZone이 명시돼 있다. 계약 없음이라는 이유만으로 완료에서 빼지 않는다. 기존 생성 응답의 task/request id와 기존 자료 업로드/연결 API를 이용해 파일 선택 → 생성 → 자료 연결의 두 단계로 구현 가능한지 실물 확인 후 구현한다. 새 서버 API/새 권한을 만들지 않는다. 생성 성공 후 업로드 실패가 업무 재생성으로 이어지지 않도록 생성 결과를 보존하고 재시도 또는 상세로 이동하는 경로를 제공한다. 기존 본인/관리 배정/요청/회의 승격 경로를 보존. 실제 기존 API로 연결 불가능한 갈래가 있으면 구체적인 응답·권한·경로 근거를 즉시 코디에 묻고 다른 수정은 계속한다.
Composer의 200자 하드캡은 SPEC003이 기존 본문 계약을 보존하므로 새로 강제하지 않는다. 현재 카운터는 유지하고 코디가 WORK에 이 해석을 명시한다. 파일 첨부 원래 범위를 임의 유예하거나 Phase7-A를 전부 완료라고 적지 않는다.

## 5. 허용 파일
코드 frontend/ 및 본인 v2-frontend-implementation-report.md의 정정 절, 신규 v2-frontend-fix1-report.md만. 제품 스펙·WORK·index·BE·DB 수정 금지. 커밋/push/PR 금지.

## 6. 검증
AGENTS 준수 make frontend-test 및 frontend에서 npx tsc --noEmit. 필수 F-1 권한 및 W-3 실패 경로, 첨부 정상·생성 후 업로드 실패/재시도 중 중복 생성 없음 회귀. 로그와 실제 exit 저장. 불필요한 전량 반복 금지. 빌드·전체 verify는 최종 코디가 실행한다. 브라우저 E2E 사용자 몫.

## 7. 보고
지적별 수정·검증·남은 범위, 첨부 단계의 실패 처리와 보존된 API 계약을 간결히 남긴다. 현재 BE 미완료를 FE 회귀로 섞지 않는다.

## 8. 완료
두 채널 보고 후 idle. 원문 전수 추적이나 전체 FE 재작성 금지.

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
