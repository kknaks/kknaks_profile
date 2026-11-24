# [spec] SPEC-010 고침 6 — WP-0 실측 반영 → 0.2.3 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 실측 `$W/research-v05-facts.md`(스펙과 다른 점 19 · §2 표) · 검수 `$W/review-spec-010-r5.md` P2 3. 이 둘을 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.2.3. 문서 1 개만 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0. 앱 워커가 지금 WP-1(kos_map · 설정)을 하고 있다 — WP-1 계약은 바꾸지 말 것(바꿔야 하면 질문).

## 코디 판단(실측 리포트가 코디에게 넘긴 4)
- **N1:** 실측 「고칠 방향」 그대로 — 0.4 이해 호출 목록(`entry_list.TABLES`)에 `effect`(필수) · `procedure_case`(선택 · 이름 있는 44 코드만) · pick 출력에 `country` · pick 판 `0.5.0-draft` · 회귀 시험 목록을 WP-3 에.
- **N2: 효과를 찾는 키로 쓸 때는 케이스 · 시술 행만 쓴다** — `facets outcome node=effect:` 결과 중 procedure_case → by_case · procedure → by_proc · **modality · package 행은 진료항목 길에서 뺀다**(장부 `items.dropped_reach` 에 표지). 근거 = 고민과 같은 원칙(11-20 「찾는 키는 넓은 위층으로 퍼뜨리지 않는다」 — 보톡스 계열 「눈썹 올리기」 한 행이 보톡스 106 을 끌어오는 것 막음). E15 기대 수를 이 규칙으로 실측해 다시 적는다. 모달 · LLM 의 효과 표시(물려받음 포함)는 그대로.
- **N3:** `effect_code` 빈 경과 줄(onset · peak · duration 만)은 **모달 효과 목록 · 효과 축(AX3)에서 뺀다**. 값은 LLM 블록에는 넣는다(원문). 모달에 경과를 보일 자리는 시안에 없으니 slot 하나(빈칸 시작).
- **N12:** 실측 「고칠 방향」 그대로 — 새 slot 은 템플릿 `data-slot` 빈 자리 · 사용자가 채우면 `slots` 키를 더함.
- 나머지 15 · r5 P2 3: 실측 리포트 「고칠 방향」 그대로.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.3" --body "실측 19 · P2 3 반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 6 완료 — <한 줄>. 상세는 인박스." --enter
```
