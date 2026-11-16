# [researcher] 실버 3단계 검수 FAIL 수정 — review-step3-report 전부

`review-step3-report.md`(FAIL 5 · WARN 7 · open 12)를 읽고 리포트 「고칠 값」대로 고친다. 리포트 끝 「다시 돌릴 때 순서」를 따른다. 원천 · DEC · step1 · step2 수정 금지 · 추정 금지.

## 코디 기본값(리포트가 코디에게 맡긴 것)
- **F1 대소문자**: 영문 패턴은 대소문자 무시. 단 `citations[].title`(논문 제목)은 셈 밖(원천 내용이 아니라 서지). `#skip:ALA` 는 대소문자 구분으로 앞에. `problem[].category_en` 은 이름 칸(`method.name_fields`)에 넣는다. F1 표 50회 전부 행으로
- **F2**: 근거 약 7행 추가(리포트 값 그대로) · 질문 추가
- **F3**: (a) handoff 기준으로 분기 · (b) 10행 리포트 고칠 값대로 · 어깨라인은 그대로
- **F4**: 상악골 · 위턱뼈 → 볼(묶음) + 질문 문구 교체
- **F5**: 4줄 리포트대로
- **W1 · W2 받는다 — 갱신 구조가 이번 작업의 목적이다(스킬로 이어짐)**: 행선지(site · kind · other_parts/stage) · 노드 속성 · lexicon 을 결정 쪽 파일(`step3-decisions.json` 또는 `step3-lexicon.json`)로 옮기고, rows 는 스크립트가 원천에서 만든다. 조사 판은 근거로만 읽는다. 가드: 순서 없는 집합 + 등장 수 비교 · **사전에 잡혔는데 결정에 없는 문자열 = open[]**(결정 파일에 행선지 더하면 닫힘) · 사전 밖 부위 형태소 잔여 검사(허용 목록 대조, 잔여 = open) · 원천 경로는 결정 파일 `source` 키
- **W3 · W4 · W5 · W7**: 리포트대로(W5 는 「약」 노드마다 질문 1줄) · **W6**: kind 「여러 부위(나열)」
- **아직 사용자 미정(바꾸지 마라)**: deferred 의 「위험 부위 속성(ANATOMY_HAZARD)」 · 「안전 원장(합병증)」 · 「사후관리 문구」 행선지 이름은 지금대로 둔다

## 끝 조건 · 산출
open[] = 0(새 가드 기준) · 결정론 · md 맨 위 셈 · 바뀐 행 목록 · 근거 약 · 질문 수. 산출 파일은 앞 판과 같은 이름(+ 결정 쪽 새 파일이 생기면 그것).

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_16898dfd-67ba-45ea-81ba-e60d37fd48e4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 검수 수정" \
  --body "문자열 N(회) / open N / 근거 약 N / 질문 N / 구조 변경 요약"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 검수 수정. 상세는 인박스." --enter
```
