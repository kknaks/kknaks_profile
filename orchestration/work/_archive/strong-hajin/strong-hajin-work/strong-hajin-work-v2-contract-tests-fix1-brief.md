# 신규 계약 테스트 최종 증거 정정

## 1. 역할
기존 contract-tests 워커 재사용. 원래 코드 워크트리에서 본인 소유 두 테스트 파일과 v2-contract-tests-report.md만 수정한다. 제품 코드·기존 테스트·PG는 무수정.

## 2. 입력
원래 SPEC003/WORK002와 본인 보고서. 새로운 범위를 만들지 않는다.

## 3. 필수 정정
A5 테스트 :437/:443의 status_code != 200 두 자리는 권한 거부를 증명하지 않는다. 실제 권한 계약과 HTTP 매핑을 확인해 정확한 거부 코드로 단언한다. 500/다른 성공도 통과하는 넓은 단언을 남기지 않는다. 같은 테스트의 state/assignee 불변 보존.

## 4. 보고서 판독 정정
숨은 하위를 제품 경로로 만들 수 없다는 일반화는 V21만으로 성립하지 않는다. V21은 요청자/승격자만 확장하고 CC·다른 독립 읽기에는 자동 하위 확장이 없다. 실제 완료 가능한 상위 담당/승인 주체에 숨은 직속 하위가 생길 수 있는지 관련 기존 테스트/코드를 제한적으로 확인한다. 재현 가능하면 API 또는 정확한 권한 fixture로 숨은 이름/id/건수 없이 409 및 혼합 경우 visible만 노출 회귀를 넣는다. 진짜 도달 불가면 그 좁은 전제와 근거를 적고 상위를 읽으면 무조건 하위도 읽는다는 문장은 제거한다. 제품 결함이면 원BE/코디에 전달. 순환관계 방어 테스트를 억지 API로 만들지는 않는다.

## 5. 경계
reason 직접취소 계약 모순은 원BE·코디 확인 중, 이 발주에서는 정하지 않는다. OQ203/206 현행 그대로. PG는 term_2e64fd06-507c-460d-accd-2c91b8863dd8 소유로 보고서 갱신.

## 6. 검증
make test-contract의 PYTEST_ADDOPTS -k 로 변경 테스트만 검증. 전체 재실행 금지. 실제 make rc/full log 보존. 마지막 31 pass 기존 증거를 새 검증 수치와 구별한다.

## 7. 산출물
기존 두 테스트 파일만 필요 최소 수정, v2-contract-tests-report.md에 정정 부록. 허용 범위 이탈·제품/DB 수정·새 워커 발주·커밋/push 금지.

## 8. 완료
두 채널 보고 후 idle. 근거 없는 테스트 확장이나 반복 검수 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_84ab1149-5aef-4981-aa60-2c48e3be004c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "contract-tests 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] contract-tests 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] contract-tests: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
