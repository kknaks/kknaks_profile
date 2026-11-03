# [researcher] 실버 3단계 재검수 v4 지적 수정 — 표준 목록을 기계로 · 치골궁

`review-step3-v4-report.md` §5 「닫으려면」 1~5 를 그대로. 원천 · DEC · step1 · step2 수정 금지.

1. **F-B′ (기계 추출 — 손으로 고르지 않는다)**: TA2 Part 1 영문 이름 줄 → 낱말 → 위치어 · 일반어 목록 제외 → 영문 어간 전부 / KMA 의학용어 조회 결과의 한자어 동의어 칸 전부 → 한글 형태소. **추출 스크립트 + 조회 결과 파일을 `step3-standard-terms/` 에 남긴다**(다시 셀 수 있게 · W-3). 리포트가 든 한자어 18 · 영문 10 이 들어갔는지 확인. 소음은 허용 목록(같은 표면 다른 뜻 — cervix · 요부 · 수부 등)
2. **치골궁(원천 2회)** — 코디 기본값: 문맥이 얼굴 필러라 **원천 오기 후보**. 노드에 붙이지 않고 결정 한 줄로 deferred 「원천 확인(오기 후보)」 + `step3-source-fix.md` 한 줄 + 의료진 질문 1줄(「퍼펙타 · 이브아르 설명의 「치골궁」은 무엇의 오기인가 — 관골궁?」). 행선지를 추정으로 정하지 마라
3. **W-1**: 등 사전 분기에 `node_list_end()` 조건(리포트 값) · fixture 3
4. **W-2**: ‹부위›살 일반 패턴 · 안면부종 → 안전 원장 · 가슴 ?확대(?:술)? D-07 · 손톱으로
5. 알려진 한계 문장 고침(리포트 §3) · fixture 에 리포트 13 + 3 문장
6. open 0 · 결정론 · 셈(예상: 치골궁 +1행 · 안면부종 · 가슴확대 행 갈림 — 다르면 이유)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_fe6fc75e-8ac3-46d0-a4e3-82410870cc67 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 v4 지적 수정" \
  --body "open N / fixture N/N / 표준 목록 기계 추출 N어 / 셈 변화"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 v4 지적 수정. 상세는 인박스." --enter
```
