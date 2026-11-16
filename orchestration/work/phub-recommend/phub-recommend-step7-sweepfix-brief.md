# [researcher] 실버 7단계 — 전수 눈검 결과 반영(규칙 5 + 판단 3 · 사용자 10-30)

(앞 작업 `phub-recommend-step7-siteup-brief.md` 이어서 · 검수 `review-step7-sweep.md` · `.json`)

사용자 「응 그렇게 해줘」 — 검수 원인 묶음 대로 **규칙으로**(행별 결정 금지 · 결정 파일 rules 에 문장 + 사전):
1. **R23 용도로 좁힘(C1)**: 부위 없는 「후보 전부」는 5단계 units[].purposes 가 고민 · 목적과 맞는 단위 시술만 · 다른 고민 용도(다한증 · 제모 등)가 박힌 단위 시술 빼기 · 못 좁히면 계열만
2. **R24 이름 · 제품으로 좁힘(C2 · C7 · C8)**: 원천 이름 조각 · 제품 칸(「레이저 토닝」 → 토닝 · 「V빔」 · 「PDL(V빔)」 → U5-141 · 「+ PRP」 → PRP) — combo-recipes 경로에도 problem-combos 와 같은 좁힘 · 못 좁히면 계열만
3. **R25 두피 시술은 두피 고민에만(C3)**: 최상위 영역 두피 단위 시술은 두피 영역 고민(P13 계열)에만
4. **R26 흉터 · 튼살(C5 · C6)**: 흉터 → 필러 = 계열만(M2) + 원천 질문 「흉터 필러 단위 시술」 · 튼살(바디) → 얼굴 · 목 단위 시술 빼고 계열만 + 「이 부위 단위 시술 없음」
5. **R27 겹친 엣지 합치기(C4)**: ③ 갈래 목록 복사로 겹친 엣지 → (갈래 × 원천 시술) 하나 · basis 「갈래 X 추천 시술 Y」 · 원천 수정 후보 목록에
- **판단 ①** 목 니들RF 는 여드름 · 모공 · 흉터에서 뺌(얼굴 고민) — 규칙 문장으로(영역 없는 피부 고민의 기본 영역 = 얼굴)
- **판단 ②** 볼륨 회복 · 동안 쁘띠 조합의 필러 8 부위 = 그대로 + 표시 「후보 여럿」
- **판단 ③** 「엑셀V」 동의어 대상에 U5-138(532nm KTP) 추가 — 5단계 결정 → step5 재실행
- 「확인 필요」 36 은 위 규칙 적용 뒤 다시 셈해 남는 것만 보고

## 같이 할 것
- 5 → 7 → 8 재실행 · open 0 · cmp · 고정 시험(각 규칙 · 판단 1건씩) · concern-check · unit-check · relation-check errors 0 · `semantic-build.py` · `silver-graph-build.py` 재생성 · md 셈
- 검수 json 의 이상함 105 가 규칙 뒤 0 인지 스스로 다시 셈(남으면 보고)
- 원천 · DEC 수정 금지 · 키 지우지 말 것

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_9a547119-8de5-4e0e-a03c-09c2a71b1854 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 7단계 전수 눈검 반영" --body "이상함 105 → N · 확인 필요 36 → N / 엣지 N · 조합 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 7단계 전수 눈검 반영. 상세는 인박스." --enter
```
