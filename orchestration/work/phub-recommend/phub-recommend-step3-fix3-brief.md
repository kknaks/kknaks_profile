# [researcher] 실버 3단계 재검수 v3 지적 수정 — 표준 부위 목록으로 한 번에

너는 앞 판 맥락이 없다(앞 워커 터미널이 죽음). 먼저 `step3-sites.md` · `review-step3-report.md` · `-v2` · `-v3` · `phub-recommend-step3-apply-brief.md` · `-fix-brief` · `-fix2-brief` 를 읽고 `step3-apply.py` · `step3-lexicon.json` · `step3-decisions.json` · `step3-fixture-test.py` · `step3-fixtures/` 구조를 파악하라. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`.

`review-step3-v3-report.md` F-A · F-B · W-C 를 리포트 「고칠 값」대로. 원천 · DEC · step1 · step2 수정 금지.

1. **F-A**: 볼 뒤 막기 `기` · 힙에 `볼기(?:부위)?` · **같은 성격 전수**(뒤가 열린 짧은 낱말 볼 · 코 · 목 · 등 · 팔 · 발 · 손 · 배 · 턱 · 눈 · 입 × 「+한 글자」 꼴 시험 → 결과 표)
2. **F-B (덧대기 중단)**: residual 형태소 · 영문 어간을 **표준 부위 목록에서 뽑아** 채운다 — 대한해부학회 해부학용어 부위(regio) · Terminologia Anatomica 2 regiones(영문) + 상담 구어 묶음(리포트 목록). 출처 URL · 날짜를 `residual.note` 에. 영문 어간은 단어 안에서도 찾기(소음은 허용 목록) · 정규화에서 악센트 제거(NFKD)
3. **W-C**: 「등」 허용 앞 조건(앞 낱말이 노드 이름 · 동의어(+과/와)면 허용 안 함) · ‹부위›라인 일반 패턴(W7 규칙과 같게)
4. fixture 에 리포트 37문장 + F-A 전수 시험 문장 + W-C 문장 추가 → 전부 통과
5. **알려진 한계**를 `step3-sites.md` 에 한 절로: 표준 목록 밖 신조어 · 같은 표면 다른 뜻(쇄골 라인 필러) — 사람이 찾는 몫
6. open 0 · 결정론 · 셈(원천 값이 바뀌면 이유)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_fe6fc75e-8ac3-46d0-a4e3-82410870cc67 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 v3 지적 수정" \
  --body "open N / fixture N/N / 표준 목록 출처 / 셈 변화"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 v3 지적 수정. 상세는 인박스." --enter
```
