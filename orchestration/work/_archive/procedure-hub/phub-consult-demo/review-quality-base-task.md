# [reviewer · 읽기만] 품질 기준선 검수 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 앱 · 허브 · 데이터 · 프롬프트 · `quality/` 안 파일 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만) · 키 값 출력 0 · **LLM 호출 0**(앱 다시 안 돌림 — 저장된 결과로만).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`35b56e5`) · 대상 `$W/quality/`(`QUALITY.md` · `scenarios.json` · `answers.md/json` · `build_answers.py` · `run.py` · `score.py` · `base-report.md` · `out/base-20261123-1714/`) · 발주서(기준) `$W/quality-base-task.md` · 정해진 것 `$W/_RESUME.md` §2.

## 볼 것
1. **판정이 너그럽지 않은가** — 기준 22 개 각각 `score.py` 판정 규칙이 기준 뜻을 실제로 재나. 특히 10 · 11(156/156) · 9 · 14 · 18 · 19 · 20(100%)이 「낱말이 없다 = 통과」 같이 비어 있어 통과한 건 아닌가. 표본 5 턴 이상을 `screens/` · `turns.jsonl` 원본으로 직접 다시 판정해 맞대라.
2. **정답 규칙 R1 ~ R8** — 매핑 JSON · 허브 값으로만 만들었나(지은 진료항목 0). 「확인 필요」 로 올리지 않고 규칙으로 정한 칸 중 사람 판단이 필요한 게 숨어 있나. `_RESUME` §2 결정(주제 찢기 · 좁히기 + 넓히기 + 되돌리기 · 점은 늘 다 뜨고 지금 주제만 강조 · 「0 이면」 처리)과 어긋난 정답 칸.
3. **수치 재현** — `score.py out/base-20261123-1714` 를 다시 돌려 §1 표 · 흔들림 3 턴 · 비용 $5.73 이 같은가.
4. **구멍 표 H1 ~ H10** — 까닭 · `파일:줄` 이 코드와 맞나(직접 열어 확인). 빠진 구멍(실패 표에 있는데 구멍 표에 없는 것).
5. **시나리오 덮음** — 발주서 「반드시 포함」 꼴이 다 있나 · 기준 22 개 모두 판정하는 턴이 있나(21 은 3 판정뿐 · 15 는 사람만).

## 산출
`$W/review-quality-base.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 실측 · 고칠 방향) · 다시 판정 표본 표 · 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: 품질 기준선" --body "판정 / P0 · P1 · P2 수 / 너그러운 판정 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 품질 기준선 완료 — <한 줄>. 상세는 인박스." --enter
```
