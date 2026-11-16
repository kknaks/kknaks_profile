# [reviewer_doc] batch-03 독립 검토 — others

Opus 검토 워커. 다른 검토 워커와 공유 트리지만 쓰기는 아래 보고서 하나만 허용된다. 추가 워커 금지. §9보다 라이브 preamble의 정확한 보고 인자·ID·outcome 요구가 우선한다.

## 1. SSOT

AGENTS.md, orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md, _RESUME.md, batch-03-dispatches.json(작업 디렉토리 orchestration/work/phub-ledger-redesign/ 기준). 원본은 orchestration/work/phub-recommend/bronze/phub-ledger/, 새 조사 결과는 작업 디렉토리 first-pass/<원장명>/.

## 2. 대상과 목적

이번 검토 대상: literature-evidence, problem-packages, problem-combos, pih-risk. 이 원장들만 검토한다. 1차 수집 계약 충족 여부를 확인하며 최종 의미 조사·정규화·임상/법적 사실 검증을 하지 않는다. 사용자는 알려진 분석 오류와 후속 의미 과제를 기록하고 다음 원장으로 넘어가기로 했다. 동일 원장을 재조사하며 모든 형태소 정답을 얻으려 하지 않는다.

## 3. 검토 계약

각 대상의 원본과 source-map·coverage·morphology·expressions·review.md/분할문서·issues·validation·verify.py를 대조한다. 코디가 각 verify.py를 실제 재실행해 failure0·원본 해시 불변을 확인한 상태이지만 그 주장을 최종 근거로 쓰지 말고 검사 범위와 출력·원문을 직접 확인한다.

- 기계 대조는 전체 경로 집합·자료형·모든 값·빈컨테이너·구획 소유 합집합·Pointer·문자구간·바이트구간·중복·이스케이프·분할문서 원문 대응·형태소 적용/제외·구간을 확인한다. 기존 verify.py를 읽기 전용으로 실행한다. 큰 출력은 요약만 메인에 보낸다.
- 독립 읽기는 원문 인용·잠정 관찰·수식·조건·부정·가능성·범위 보존과 알려진 분석 오류의 영향 기록을 확인한다. 자동/표본/전수 범위를 명확히 구분한다. 단서 정규식·토큰 수를 전수 의미 조사로 제시하지 않는다.
- 정확한 실제 추출 누락/변형/위치 오류는 종료 차단 수정과 근거 Pointer로 제시한다. 알려진 품사 오류나 의미 미결은 위치·영향이 기록됐으면 비차단 한계로 남긴다. 새 발견도 한계로 기록할 수 있다. 원문 부족을 에이전트 해석 과제와 혼동했는지 확인하되 미결을 닫지 않는다.
- C는 현재 사용자 결정이다. 원문 내 불일치 I와 구분한다. 원본 보존 지시는 이미 있으므로 원본 수정 여부를 다시 고르게 하지 않는다. 지금 필요한 사용자 선택이 없다면 잔여 항목 상태·영향 검토 근거와 함께0이라고 보고한다.

literature-evidence의 영어/중국어/일본어·서지는 원문 수집과 형태소 제외를 구분해서 검토한다. 제외 사유·영향이 명시됐는지, 제외를 의미 없다고 처리하거나 전언어 형태소 분석 완료라고 과장했는지 확인한다. 언어별 극성·조건 차이라는 관찰은 원문 근거가 있는 잠정/불일치 기록인지 본다. 문제 조합·패키지는 원문 내 이름/코드/가격/기호 불일치와 후속 개념 연결을 구분한다. pih-risk는 원래 워커의 최종 결과이며 재시작 대상이 아니었다. 이 워커가 pkill -f cat을 보고한 운영 사고가 있으므로 현재 산출물의 완전 파싱·값/구간 대응을 확인하되 다른 프로세스 피해가 없었다고 추정하지 않는다. 사고 자체로 기계적으로 정상인 데이터를 실패로 만들거나 사용자 선택을 억지로 만들지 않는다.

## 4. 보고서

원장별 PASS/WARN/FAIL, 1차 종료 가능 여부, 반드시 고칠 추출 오류, 비차단 한계·분류 보완, 미결 처리 상태, 직접 읽은 범위·검증 명령·실제 결과, 결과/컬럼표 접근 경로를 한 보고서에 담는다. 원장 전체 완료와 구분한다.

## 5. allowed_paths

새 `orchestration/work/phub-ledger-redesign/batch-03-review-others.md` 한 개만 생성. 원본·결과·다른 리뷰·스킬·재개 노트·발주 기록은 읽기 전용. 독립 검사 스크립트가 필요하면 scratchpad에만 두고 공유 트리에 생성하지 않는다.

## 6. 순서

계약·범위 확인 → 기계 전수 대조 → 공개한 범위의 독립 읽기 검토 → 미결 분류 검토 → 보고서 작성. 넓은 taxonomy 검토와 나머지4개 검토가 독립이므로 다른 워커 결과를 기다리거나 편집하지 않는다.

## 7. 제약

원본·조사 결과 수정/삭제·전체 rebuild·다른원장 조사·추가워커·외부 임상조사·커밋·push·PR 금지. pkill/killall 같은 프로세스명 패턴 종료 금지, 본인이 시작한 정확 PID/세션만 제어한다. 작업 범위밖 파일 생성 금지.

## 8. 완료

대상 원장별 실제1차 계약 충족을 판정하고 근거를 남긴다. 기계 pass를 의미 정답으로 주장하지 않는다. 코디에게3문장 요약과 보고서 경로만 전송하고 idle한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --from term_8c2999f2-0bca-4945-9d09-c5212852bdaa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
