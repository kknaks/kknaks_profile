# [researcher] 실버 2단계 최종 반영 — open 해결안 반영 + 원장님 문의 3행 분리

결정 `_RESUME.md` §2 10-28 「2단계 open 40 해결안 반영」 행(사용자). 해결안 `step2-open-resolve.json` · `.md`(네가 만든 것). `step2-apply.py` 를 고쳐 재실행(결정론). step1-products.json 수정 금지 · 결정에 없는 변경 금지.

1. **37행 반영**(open-resolve 의 해결 값 그대로): 하위 계열 주 1 + 보조 `also_sub_families` · 계열 주 + 보조 `also_families`(이브타이탄 M9+M10 · 바이리즌 M4+M2 · 트리필 프로 M4) · 새 하위 칸 M4 「무세포동종진피(hADM)」 · M9 「SUPERB 초음파」 · 충돌 6행 `conflict` 기록
2. **근거 약 9행**(실루엣소프트 · 압토스 · 에버라인 · 미라클 · 피코코어 · 트루피코 · 디스커버리 피코 · 아이콘 · 아톰): 값 넣고 `evidence_level: "약"` + `confirm_question`(open-resolve 의 확인할 것). 판정은 open 이 아니다
3. **원장님 문의 3행**(알렉스필 · 더마큐어 · 벨르업): family null 유지 · `pending_director: true` · open[] 에서 빼고 새 칸 `pending_director[]` 로(질문 한 줄 + 정체 확인되면 갈 계열 — 알렉스필 필링 M15 / 레이저면 5단계 시술 이름 · 더마큐어 TS-3 면 M13 · 벨르업 원리 확인 후). `step2-origin-questions.md` 를 「원장님 문의 3」 + 「근거 약 확인 9」 두 절로 다시 쓴다
4. **끝 조건: open[] = 0.** md 맨 위 셈(계열별 · 판정 · evidence 약 · pending_director 3) 갱신 · 이번 반영으로 바뀐 행 목록

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 최종 반영" \
  --body "open N / pending_director 3 / 근거 약 9 / 바뀐 행 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 최종 반영. 상세는 인박스." --enter
```
