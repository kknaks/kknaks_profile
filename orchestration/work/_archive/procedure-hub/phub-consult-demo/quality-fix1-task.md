# [spec · 고침 1] 품질 기준선 채점 고침 — 검수 FAIL 반영 (사용자 승인 11-23 「쭉 진행해」 범위 · 기준선 단계 안)

너는 스펙 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **고칠 것 = `$W/quality/` 안 `score.py` · `build_answers.py` · `answers.*` · `QUALITY.md` · `base-report.md` 뿐** · **앱 다시 안 돌림 · LLM 호출 0**(저장된 `out/base-20261123-1714/` 로 다시 채점만) · 앱 · 허브 · 데이터 · 프롬프트 수정 0 · 커밋 0 · 서브에이전트 0 · 18222 · 18105 손대지 마라(허브 GET 만) · 키 값 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-quality-base.md`(FAIL · P1 4 · P2 8) · 앞 발주 `$W/quality-base-task.md` · 정해진 것 `$W/_RESUME.md` §2.

## 할 일
1. **P1-1 ~ P1-4 · P2-1 ~ P2-8 전부** 검수 「고칠 방향」 대로. 특히:
   - 기준 11 금지 말 넓히기(「확인이 필요」 · 값 문장 · 목록 사정 문장) · 구멍 H11(`prompts/consult.json:193` 같은 날 대본).
   - 기준 18 부위 둘 주제 · 얼굴 주제(R6 몸 묶음) 판정.
   - 기준 8 · 10 · 13 돌려 막기(「어려」 · 「상담」 빼기 · 「드리기 어려」 · 시술 · 계열 이름 사전).
   - S05 T2 · S05 T3 · 빈 정답(must 0) 칸을 「확인 필요」로 올림 — **확인 필요 칸 수를 새로 셈**(사람 몫 50 안쪽).
   - 기준 14 진료항목 ↔ 옵션 값 짝 · 빠뜨림.
   - `same_as` 판정이 틀린 앞 턴을 물려받으면 na/따라 fail.
   - 구멍 표 H9 · H10 자리 고침 · 빠진 구멍(P2-4 ①~⑤) 더함 · 줄 번호(P2-8).
   - 기준 21 · 14 판정이 얇은 것은 **리포트 한계에 적기만**(이번엔 앱 다시 안 돌림 — 시나리오 추가는 다음 단계 측정 때).
2. 너그러움 전수: 검수가 본 것 말고도 22 기준 판정 규칙을 하나씩 다시 읽고 「낱말 없음 = 통과」 꼴이 남았는지 스스로 찾아 고친다(찾은 목록을 리포트에).
3. 다시 채점 → `base-report.md` 판 올림(0.2) · 머리 표 · 기준 22 표 · 구멍 표 · 바뀐 수치 전 → 후 표.

## 검증
`git -C $A status --short` 0 줄(`A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`) · 18222 · 18105 그대로 · LLM 호출 0 · 수치는 스크립트 출력에서.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: 품질 기준선 고침 1" --body "확정 통과 전 → 후 / 확인 필요 칸 수 / 새 구멍 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 품질 기준선 고침 1 완료 — <한 줄>. 상세는 인박스." --enter
```
