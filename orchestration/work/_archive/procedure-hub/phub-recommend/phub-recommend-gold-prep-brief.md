# [researcher] 골드 전 정리 — 남은 문항 2묶음 + 골드 빈틈 2 (사용자 10-30)

(앞 작업 `phub-recommend-quality-fix-brief.md` 이어서 · `quality-report.md` §0-3 · 골드 조사 `gold-research.md` 큰 발견 ② ③)

사용자 「응 그렇게 발주해줘」 — 아래 4개 · 규칙으로 · 행별 결정 금지:
1. **측정 계열 대응(Q020 · Q025)**: `quality-eval.py` 의 계열 옮김 표를 손 표가 아니라 5 · 7단계 결정 파일(계열 옮김 · fam_kw · 원장 행선지)에서 읽게. 문항 · 정답 · 채점 식 그대로(문항 파일 바이트 같음 확인)
2. **2단계 엑셀V 하위(Q018 · Q019)**: 엑셀V(원천 「532+1064nm」) 하위 = 엔디야그(주) + KTP(보조) — 2단계 결정 → step2 재실행 → 같은 성격 전수(다파장 장비인데 하위 하나만 잡힌 것 · 원천 파장 낱말 근거로만) → 5 → 7 → 8 재실행. 사용자 판단 ③(엑셀V 동의어 U5-138)과 맞물리는지
3. **골드 빈틈 ① 부작용 덮어쓰기 값**: 시맨틱 U2 「제품 · 단위 시술 값이 계열 부작용을 덮어씀」의 값이 실버에 키만 있음 → 브론즈 extracted safety(common 등) 값을 5단계 단위 시술 · 1단계 연결 제품 쪽 칸에 원문 그대로(붙는 수준 · 근거) — 5단계 결정 → 재실행
4. **골드 빈틈 ② 추천 조합 구성 119**: 7단계 combos 구성 셈에서 비교 members · upgrade 119 가 빠짐 → 7단계 · 시맨틱 combo_component 셈에 포함(구성 칸 이름 그대로)

## 끝
- 2 → 5 → 7 → 8 → semantic-build · open 0 · cmp · 고정 시험(항목마다 1) · 스킬 9종 errors 0
- `quality-eval.py` 다시 → 목표 6/6 유지(CC 슬롯 · CC 없음 두 값) · 남은 틀림은 Q106 · Q108~Q110(골드 판단 몫)만인지
- `silver-graph-build.py` · `silver-questions-build.py` 재생성(코디 게시)
- 원천 · DEC 수정 금지 · 가상 문장 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_39f6cf28-b4a6-4dfc-b9e3-373afae49d25 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 골드 전 정리" --body "남은 틀림 N(목록) / 다파장 하위 N / 부작용 덮어쓰기 값 N / 조합 구성 N / 목표 N/6 / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 골드 전 정리. 상세는 인박스." --enter
```
