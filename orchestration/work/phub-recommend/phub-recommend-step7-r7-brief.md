# [researcher] 7단계 — R24 좁힘에 레시피 설명 문장 포함(남은 확인 필요 1 닫기 · 사용자 10-30)

(앞 작업 `phub-recommend-step7-sweepfix-brief.md` 이어서)
- 사용자 확인: RC-RE-R7 「레이저 토닝 + 재생」의 「재생」 = 목적, 그 자리 시술 M5 = 원천 patientExplanation 「PRP 성장인자」 · analogy 「PRP = 새 도화지」 → **U5-020 얼굴 전체 PRP**(시술 가능 부위가 얼굴 전체 — 사용자)
- 규칙으로: R24 좁힘 원천 칸에 combo-recipes `patientExplanation` · `analogy` 추가(결정 파일 문장) · 같은 성격 전수(다른 레시피에도 이 칸으로 좁혀지는 것) · 조합에 목적 「재생」 연결 확인
- 5 → 7 → 8 재실행 · open 0 · cmp · 고정 시험 1 · concern-check errors 0 · `review-step7-sweep-recount.py` 확인 필요 0 · semantic-build · silver-graph-build 재생성

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_9a547119-8de5-4e0e-a03c-09c2a71b1854 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 7단계 R7 재생 PRP" --body "확인 필요 N / 좁혀진 조합 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 7단계 R7 재생 PRP. 상세는 인박스." --enter
```
