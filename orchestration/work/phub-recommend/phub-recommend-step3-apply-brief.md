# [researcher] 실버 3단계(부위) 반영 — step3-research 결정대로 부위 원장

앞 판 조사(`step3-research.json` · `.md`)를 네가 했다. 결정 `_RESUME.md` §2 10-28 「3단계 부위 조사 반영」 행(사용자 「추천으로 가자」). 2단계 반영 방식(`step2-apply.py` — 결정론 · 고정 입력 · 판 사본)을 참고하되, **2단계의 한계(고정 assert · 이름별 dict 라 새 행마다 손으로 고침)를 되풀이하지 마라** — 결정은 데이터 파일(`step3-decisions.json`)로 빼고 스크립트는 그것을 읽는다. 셈 검사는 결정 파일에서 계산한 값과 대조.

## 반영
- B1~B12 · U1 · U2 전부 step3-research 추천대로(사용자). 노드 43 + 새 10 = **53**
- 산출:
  - `step3-decisions.json`(결정 데이터 — 묶음 · 노드 추가 · 문자열 행선지)
  - `step3-apply.py`(입력: step3-decisions.json · step3-research.json · DEC-002 트리 · stg 원천 → 같은 입력 같은 출력)
  - `step3-sites.json` · `.md`: `nodes[]` 53(id · 이름 · 상위 · 동의어[] · 해부학 이름 후보{en, ko, 근거, 수준} · 위험 부위 대응 · 원천 근거 · 근거 약 표시) · `strings[]` 500(행선지) · `deferred[]`(부위 아님 173 → 단계) · `open[]` · `doctor_questions[]`(근거 약 20 + 위험 부위 확인 + 해부학 이름)
  - `step3-source-fix.md`(B11 DEC-002 근거 표 정정 3 · B12 원천 수정 후보 2) — DEC-002.md 는 직접 고치지 마라(목록만)
- **끝 조건: open[] = 0.** md 맨 위 셈(노드 · 문자열 행선지 · 근거 약 · 질문 수)
- step1 · step2 산출 · DEC 문서 · 원천 수정 금지 · 결정에 없는 변경 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_16898dfd-67ba-45ea-81ba-e60d37fd48e4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 반영" \
  --body "노드 N / 문자열 행선지 셈 / open N / 의료진 질문 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 반영. 상세는 인박스." --enter
```
