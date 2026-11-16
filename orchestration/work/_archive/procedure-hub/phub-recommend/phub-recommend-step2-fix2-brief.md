# [researcher] 실버 2단계 마지막 수정 — 재검수 v2 WARN 3

`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-v2-report.md` W-1~W-3 와 `_RESUME.md` §2 10-28 「2단계 재검수 v2 PASS 뒤 WARN 3 처리」 행(사용자 결정)대로 `step2-apply.py` 를 고치고 재실행. step1-products.json 수정 금지 · 결정에 없는 변경 · 추정 금지.

1. **M8 하위 = 광원 매질 한 축.** 하위 칸에서 「피코초」 「프락셔널」 등 방식 칸을 없앤다. 그 행들은 원천 설명 · 허가 품목 · 모델명에 적힌 매질로(Nd:YAG 피코 → 엔디야그 레이저 · 프락셔널 CO2 → 탄산가스 레이저 …). 매질이 안 적혀 있으면 null + open(사유). 방식(피코초 · 프락셔널 · 롱펄스 · Q스위치 등)은 행에 `technique_hint`(적힌 말 그대로) + families[M8].deferred 에 「방식 → 4단계 기법」
2. **광원 2종 장비**(허가 item · 모델명 · 원천 설명 중 어디든 매질 2종): null + open — 스플렌더 X 포함, 같은 기준으로 전수. 젠틀맥스 프로 플러스는 「듀얼 파장」 사유로 open
3. **M7**: 「기타흡수성봉합사」 「폴리디옥사논봉합사」 「안면조직고정용실」 등 품목명은 synonyms 에서 빼고 name_basis 에만
4. md 맨 위 셈 · open 수 · 바뀐 행 목록(이번 수정분 따로) 갱신

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 마지막 수정" \
  --body "M8 하위 매질 재배치 N행 · null/open N / 광원 2종 N / M7 동의어 정리"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 마지막 수정. 상세는 인박스." --enter
```
