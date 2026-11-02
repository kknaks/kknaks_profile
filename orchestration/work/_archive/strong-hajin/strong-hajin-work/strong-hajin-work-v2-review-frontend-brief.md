# v2 FE 완료분 검수 — BE 구현·테스트 병행

## 1. 역할
기존 리뷰어 재사용 허용. 제품 코드/문서 read-only, 리포트만 쓴다. 코드 워크트리와 SPEC/WORK 경로는 WORK002에 명시된 기존 것을 그대로 쓴다. WORK002·SPEC003·보존된 SPEC001/002가 계약. W1 미커밋 기준은 v2-code-baseline/manifest.json·working-files.zip·tracked.patch. HEAD 차이 전체를 v2 변경이라고 오인하지 말고 baseline↔현재를 비교한다.

## 2. 입력과 범위
v2-frontend-implementation-report.md와 실제 frontend diff/테스트 로그를 검수한다. BE는 현재 수정/테스트중이며 완료되지 않았다. BE 미완료 자체는 이번 FE리포트 결함이 아니다. API 소비는 현재 http.py·typed responses와 대조하되 BE가 수정중인 차이는 코디에게 연결과제로 분리한다. 본문 WORK/SPEC 변경은 금지.

## 3. 중점
FE Phase7 A~E 전량과 UX U1~15, 시안/기존기능 보존, 요청/하위요청/담당교체/수락거절/철회/완료보고/보완/승인/합의취소/조건변경/재개/목록숨김. 앞선 코디지적의 실물수정 확인: isChildSettled에서 derived존재를 요청판정으로 오용한 것, proposal mutation봉투 타입, terms_change payload실제입력, include_removed/list_entry_hidden 새로고침 토글, 외부done으로 명령추론 금지, 비공개하위 409 일반문구 정상처리. 서버의 권한봉투를 소비하는지 특히 확인.
현재 BE shape는 모두 코드에 있음. 본인생성/발송만 키필수, 새명령 expected_version 필수(DELETE list-entry는 상태축 아닌목록정리로 입력없음).

## 4. FE 검수
실제 시안 MyWork.html+bundle과 WORK Phase7의 3탭/표/칩/모달/레일/상세 명령 전부. 사용자E2E인수와 자동타입/API매핑 구분. 가짜 데이터/없는 endpoint/버튼노출 후항상실패/권한 FE추정/기존생성경로소실/고정null로 필요한값 숨기기 검사. viewModels의 optional/string확장이 BE불일치를 감추는지. SPEC에서 명시한 후속범위는 새요구로 확장하지 않는다. 브라우저 실행금지.

## 5. allowed_paths
orchestration/work/strong-hajin-work/review-v2-frontend-report.md 하나만. 다른 코드/문서/DB/사용자프로세스 수정금지. 새 worker발주 금지.

추가 코디 확인거리: 완료보고의 DropZone 미반영/Composer 200자 눈금 처분이 WORK Phase7A 및 기존첨부계약과 일치하는지. isChildSettled가 단지 derived존재 추론만 없애고 요청판정을 새방식으로 잘못추측하지 않는지. 보고의 baseline82/82는 착수시 검증인지 완료현재대조인지 구분(지금은 BE/FE가 변경했으므로 같을 수 없다).

## 6. 결과
PASS/WARN/FAIL, 각 지적 파일:줄·재현가능조건·계약근거·최소수정과 담당 BE/FE. 기존부채와 v2직접위반 분리. 테스트 로그의 수치는 실제 열어 확인하고 아직 코디 make verify가 안돌았으면 그대로 명시한다. 이번 FE 검수로 BE/전체v2 완료를 주장하지 않는다. 없는 증거는 통과 아님. 비차단 지적을 착수차단으로 부풀리지 않는다. 단 계약누락은 작아보여도 축소하지 않는다.

## 7. 실행
read-only 검수. 기존 테스트 로그/코드 확인, 직접 테스트·DB·빌드·브라우저 실행 없음(코디통합검증과 중복방지). 의심은 관련테스트 위치와 재현방법으로 보고.

## 8. 완료
2채널 완료 후 idle. 원문추적 전수조사 재시작 불필요, 검증대상은 현재 FE 구현 diff다. 코디는 BE완료 후 BE+통합 검수를 따로 발주하며 이번에 본 FE전체를 다시 조사하지 않는다. 커밋 push PR 금지.

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
