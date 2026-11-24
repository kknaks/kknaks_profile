# [spec] SPEC-010 고침 9 — r6 FAIL 반영 → 0.2.6 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 재검수 `$W/review-spec-010-r6.md` 의 **P1 3 · P2 7 전부**를 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.2.6(변경 기록 한 줄씩). 문서 1 개만 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0.

## 코디 판단
- **P1-2(조건 없는 되돌림 표지 오판): (가)** — TP3 2 의 「조건이 비었으면 모든 앞 주제」 규칙을 지운다. 조건 없는 되돌림은 **머리 누름 · 이해 호출 return(TP14 `to`)** 으로만. TP14 에 「규칙 continue · LLM return + 유효 `to` → return」 예외 한 줄. 「다시 설명해 주세요」 · 「처음이라 무서워요」 · 「눈매 또렷하게」 를 T 줄(주제 안 바뀜)로. 근거: 이해 호출이 주제 판단을 하기로 했으니(사용자 11-20) 낱말 표지로 넓게 잡을 까닭이 없다.
- P1-1 · P1-3 · P2 1 ~ 7: 검수 「고칠 방향」 그대로(P2-4 의 「이번 턴 조건」 정의는 **follow 로 채운 대상을 뺀 이해 결과**로 정함).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.6" --body "r6 반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 9 완료 — <한 줄>. 상세는 인박스." --enter
```
