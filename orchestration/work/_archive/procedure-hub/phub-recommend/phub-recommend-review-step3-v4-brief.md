# [reviewer] 실버 3단계 재검수 v4 — v3 지적 수정 · 끝 조건 open 0

너는 맥락이 없다(앞 검수 터미널이 죽음). read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.
- 먼저 읽을 것: `orchestration/work/phub-recommend/review-step3-report.md` · `-v2` · `-v3`(앞 검수 3판 — 방법 · 시험 문장 · 기준) · 결정 `_RESUME.md` §2 10-28 3단계 행 · 지시 `phub-recommend-step3-fix3-brief.md`
- 대상: `step3-lexicon.json` · `step3-decisions.json` · `step3-apply.py` · `step3-fixture-test.py` · `step3-boundary-test.py` · `step3-fixtures/` · `step3-sites.json` · `.md`
- 볼 것: v3 F-A · F-B · W-C 닫힘 · **F-A 는 워커가 리포트 값(뒤 막기 기) 대신 「뒤 글자를 정해 두는 꼴」로 바꿨다**(볼+한 글자 11,152/11,172 가 볼로 가서) — 그 판단이 맞는지 · **W-C 「입술 등 점막」 1회를 residual_reviewed 로 닫음** — 맞는지 · 표준 목록 출처(TA2 · KMA 의학용어 6.1판 — 해부학회 용어집 대용) 실재 · 새로 드러난 4행(supraorbital · supratrochlear · tragus · submandibular salivary gland) · 「mandibular 조각이 하악으로 잘못 간 결정 1행 삭제」 · ‹부위›라인 3행 · 셈 519→525 · 3,616→3,627 · fixture 88 · boundary 시험 · **네가 fixture 밖 새 문장 20개 이상 만들어 사본 시험**(앞 판들과 겹치지 않게) · 「알려진 한계」 절이 정직한지 · open 0 · 결정론 · 회귀
- 판정 기준(v3 리포트 합의): 표준 목록 안의 부위 낱말이 open/행으로 나오면 PASS 대상. 표준 목록 밖 신조어 · 같은 표면 다른 뜻은 「알려진 한계」에 적혀 있으면 FAIL 아님
- 산출 `orchestration/work/phub-recommend/review-step3-v4-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_8312a270-deaa-40fd-9e56-eb1fcd3be479 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 3단계 재검수 v4 <판정>" \
  --body "open N / FAIL N / WARN N / v3 지적 닫힘 N/3"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 3단계 재검수 v4 <판정>. 상세는 인박스." --enter
```
