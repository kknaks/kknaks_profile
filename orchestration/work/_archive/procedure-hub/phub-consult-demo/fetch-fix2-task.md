# [code] 고침 2 — 내부 note · 목록 속사정을 손님에게 말하지 않기 (자동 · 검수 FAIL 처리 · 11-23)

앞 발주 `fetch-fix1-task.md` 규칙 · 사용자 결정 그대로(아는 것만 · 지어내지 않음 · 모르면 돌려서 · **모름 · 앱 사정을 손님에게 말하지 않음**). 검수 `$W/review-fetch-fix1.md`(FAIL · P1 1 · P2 3). `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`

## 할 일(셋 다)
1. **P1-1 kos R3**: note 는 데이터 작업 메모(「구성1 확인 필요 · KOS 기기 칸 「해당 없음」」)다 — 답에 **읽어 주지 않는다 · 바꿔 쓰지도 않는다**. status 가 매핑됨이 아닌 진료항목은 「자세한 구성은 상담 때 확인해 드릴게요」 꼴로 돌려 말한다(이름 · 가격은 블록 값 그대로 말해도 됨). note 가 답 재료로 가는 자리(블록 줄 · 규칙)를 grep 전수 — 모델이 안 보게 빼거나 「말하지 않는 메모」 표지로.
2. **P2-2 kos R8 · R13**: 「조건 때문에 목록이 비어 있어요」 · 「좁혀 본 조건 때문에」 · 「지금은 ~만으로 명동점 목록을 보고 있어요」 같은 목록 · 거르기 속사정 문장 막기. 병원 사실(「명동점에는 X 진료항목이 없어요 — 대신 …」)은 말해도 된다.
3. **P2-3**: `close.py` docstring 옛 글 정리.
4. 실물: 빈 포트에서 73bd · 검수 E3 · E4 다시 + 장부 답 grep(「확인 필요:」 · 「구성1」 · 「KOS」 · 「기기 칸」 · 「조건 때문」 · 「좁혀」 · 「목록을 보고」 · 앞 고침 1 꼴) 전 → 후 = 0 · 지어냄 0.

## 산출 · 보고
`$W/fetch-fix2-report.md`(바뀐 파일:줄 · grep 표 · 실물 답 앞 2 줄 · 시험).
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 고침 2" --body "note · 속사정 문장 전 → 후 / 지어냄 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 고침 2 완료 — <한 줄>. 상세는 인박스." --enter
```
