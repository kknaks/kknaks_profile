# [reviewer_doc] batch-01 원장 5개 1차 결과 묶음 검토

너는 독립 Opus 검토 워커다. 추가 에이전트 실행 금지. 최신 라이브 dispatch preamble이 보고 명령·ID의 정본이다. §9 고정 양식보다 최신 preamble의 outcome·정확한 인자 요구를 우선한다.

## 1. SSOT — 먼저 읽을 것

- AGENTS.md
- orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md (수정된 종료 기준)
- orchestration/work/phub-ledger-redesign/_RESUME.md
- orchestration/work/phub-ledger-redesign/batch-01-dispatches.json

## 2. 배경

사용자는 샘플 이후 1차 범위에서 더 반복하지 않고 다음 원장으로 넘어가기로 했다. 컬럼명·자료형·원문·잠정 관찰은 분리하며, 알려진 형태소 오류는 위치·영향·한계를 기록해 후속으로 남긴다. 5개 조사 워커가 결과를 제출했고 코디가 각 verify.py를 직접 재실행해 오류 0을 확인했다. 이는 자동 검증 결과일 뿐 읽기 검토나 최종 의미 정답을 보장하지 않는다. 너는 같은 원장의 의미 조사·임상 사실 검증·변환을 새로 수행하는 것이 아니라 1차 수집 계약 충족 여부를 검토한다.

## 3. 계약

대상 원장은 products, procedure-comparison, complications, treatment-sequence, synergy 각 JSON 전체다. 원본은 orchestration/work/phub-recommend/bronze/phub-ledger/, 결과는 orchestration/work/phub-ledger-redesign/first-pass/<원장명>/ 이다.

각 원본의 모든 구획·내부 값을 읽고 review.md 원문 대응과 잠정 관찰을 대조한다. 원문 누락·변형, 빠진 필드/중첩 구조, 잘못된 Pointer·문자구간, 출력 형식, 자료형 변형/빈 값, 명시하지 않은 추출 실패를 확인한다. 보고서가 실제 수집 수준 이상으로 완료를 주장하는지 검토한다. 5개 verify.py를 읽기 전용으로 재실행한다.

형태소 결과는 전부 정답으로 고치는 대상이 아니다. 알려진 오류가 위치·영향·한계와 함께 기록됐는지, 자동 후보를 확정 의미로 썼는지 확인한다. 새 미표시 오분절을 찾으면 알려진 한계/후속에 정확히 기록하면 되고 그것만으로 1차 종료를 막지 않는다. 추출 누락·원문 변형·실제 위치 오류는 수정 필요로 분리한다. 후보 전체의 최종 의미 판정이나 전체 품사 정답을 요구하지 않는다.

미결은 원문 부족·에이전트 추출/해석 과제·후속 의미 조사·사용자 결정 필요를 의미 기준으로 대조한다. 로컬 문서의 A/B/C 글자가 원장마다 다르므로 같은 글자를 단순 합산하지 않는다. 원문 부족으로 위장한 에이전트 해석이나 사용자에게 지금 불필요하게 넘긴 항목을 찾되 미결을 억지로 닫지 않는다.

synergy U1(/links/54 방향)·U2(Mxx- 접두 171출현)는 원본 수정 제안이다. 사용자는 원본 보존을 이미 지시했다. 현재 조사에는 원본 수정이 필요하지 않으므로 '현재 사용자 선택 대기'가 아닌 후속 의미/변환 검토 후보로 정리할 수 있는지 판단하라. 이 판단은 삭제·수정 승인이나 관계 방향 확정이 아니다. 관찰·영향은 유지한다.

## 4. 읽을 핵심 파일

5개 원본과 각 결과의 review.md·issues.md·validation.md·source-map.json·morphology.json·expressions.json·verify.py. 구조화 결과가 큰 경우 모든 값을 원문과 읽기용 문서로 대조하고, 전수/표본/자동 검토 범위를 정확히 밝힌다. 이전 완료 주장을 근거로 삼지 않는다. 이번 5개 외 원장은 조사하지 않는다.

## 5. allowed_paths

신규 `orchestration/work/phub-ledger-redesign/batch-01-review.md` 한 개만 생성한다. 원본·조사 결과·공통 스킬·재개 노트·발주 기록은 읽기 전용. 추가 코드·캐시·임시 산출물을 공유 트리에 만들지 않는다.

## 6. 검토 단계

1. 대상 5개 전체를 구획별 읽고 수집 결과와 대조한다.
2. verify.py를 각각 실행하고 확인 범위를 기록한다.
3. 원장별 1차 PASS/WARN/FAIL과 근거·수정 필요·알려진 한계·열린 후속을 구분한다.
4. 미결 분류와 현재 사용자 선택 필요 여부를 근거로 확인한다. 원장 간 차이는 후속 비교 후보로만 기록하며 통합 의미를 확정하지 않는다.
5. 단일 보고서에 원장별 결과 경로와 실제 컬럼 표 위치, 종료 가능 여부, 실제 추출 오류를 고칠 정확한 경로/Pointer, 분류 보완 권고를 담는다.

## 7. 제약

원본·기존 파일 수정/삭제·추가 워커·외부 임상/법률 조사·의미 모델 설계·다음 묶음 발주·커밋·push·PR 금지. 같은 원장을 반복 조사해 완벽한 의미 해석을 얻으려 하지 않는다.

## 8. 완료 기준

5개 모두를 검토해 각각 1차 수집 종료 가능 여부와 근거를 보고한다. 알려진 분석 한계만 남으면 이를 기록한 WARN/PASS로 구분하고 불필요한 재작업을 만들지 않는다. 실제 누락·변형·잘못된 위치가 있으면 해당 수정만 요청한다. 원장 전체 미완료와 구분한다. 3문장 요약과 단일 리포트 경로만 코디에 보낸다.

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
