# [researcher] 실버 5단계 — F1 규칙을 기법이 갈리는 계열 전부에 · 단위 시술 없는 추천 제품 3

앞 판(`phub-recommend-step5-fix2-brief.md`)에서 네가 「범위 밖」으로 적은 것을 닫는다. 결정은 이미 있다(_RESUME §2 10-29 「5단계 검수 FAIL 1 · WARN 2 처리」 · 「5단계 원칙」): **F1 = 기법이 갈리는 계열은 근거로 거른다 · 계열 기법이 하나면 계열 기본이 근거** · **클리닉에서 쓰는 장비 → 시술은 전부 단위 시술**.

1. **F1 을 M4 · M5 · M15 · M17 · N4 에도**(4단계 family_defaults 에 also 가 있는 계열 전부). 근거 = 2단계 하위 계열(M15 화학 박피 → K09 · 기계적 박리 · 클렌징 → K11 · 흡수 보조 기기 → K10 · 외용제 → K09 등 — 매핑은 4단계 정본 근거로) · 1단계 제품 종류(약제 vs 기기 — M4 주입 기기 K01c ↔ 약제 K01a) · 4단계 hint. 근거 없으면 상속 안 함. 코디 실측(고치기 전): M15 필링 제품 → K08 · K10 · K11 후보 · 하이드라페이셜 → K08 · K09 · M4 리쥬란 → K01c · 큐어젯 → K01a — 이것들이 빠지는지 확인
2. **단위 시술 없는 추천 제품 3**: 브이빔 · 브이빔 퍼펙타 = **M8 PDL × 얼굴 전체 × K04** 키 신설(부위 기본값 표시 · 목적 혈관은 7단계 넘김) · ASCE+엑소좀 = **M5 엑소좀 × 얼굴 전체 × K09 도포** 키(원천에 이미 있으면 그 키에 잇기 · U5 가드). 진단 장비(3D 메타뷰 · 마크뷰)는 계열 밖 그대로
3. 다시 셈: **추천 가능 제품 중 이어지는 단위 시술 0 = 진단 장비만**인지 md 맨 위에 · open 0 · 결정론 · 고정 시험(케이스 추가)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_90209fd9-0fef-4040-9ad0-2e8021e34785 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 F1 확장 · 제품 3" \
  --body "상속 전후 / 키 N / 단위 시술 없는 추천 제품 N / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 F1 확장 · 제품 3. 상세는 인박스." --enter
```
