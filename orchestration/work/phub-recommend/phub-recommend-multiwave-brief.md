# [researcher] 2단계 다파장 4 — KTP 보조 하위(사용자 10-30 ⑤)
(앞 작업 `phub-recommend-gold-prep-brief.md` 이어서 · `step2-families.json` multi_wavelength.seen)
- 노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코: 원천에 532nm 낱말이 있는데 KTP 하위 없음 → KTP 보조 하위 추가(엑셀V 와 같은 규칙 · 원천 파장 낱말 근거) — 규칙을 「보조 하위가 이미 있어도 원천 파장 낱말이 가리키는 하위가 빠졌으면 더함」으로 넓혀 전수
- 2 → 5 → 7 → 8 → semantic-build · quality-eval(목표 6/6 유지 · 남은 틀림 4 그대로인지) · open 0 · cmp · 고정 시험 · 스킬 9종 · 페이지 재생성
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_39f6cf28-b4a6-4dfc-b9e3-373afae49d25 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 다파장 KTP" --body "더한 하위 N / 목표 N/6 / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 다파장 KTP. 상세는 인박스." --enter
```
