# [researcher] 실버 7단계 — 남은 사람 질문 13 닫기 (사용자 결정 10-29)

(앞 작업 `phub-recommend-step7-regate-brief.md` 이어서 · 같은 파일들)

사용자 「응 그렇게 가자」 — 13행 전부 아래대로. 결정 파일 `rules`/사전에 **규칙·사전 항목으로** 넣고(행마다 결정 표 금지) apply 재실행:

| 원천 낱말 | 값 |
|---|---|
| 코성형 · 코 라인 | P1-1 코(쁘띠시술) — 근거 taxonomy P1-1 items 코필러 · 코실리프팅 |
| 다크서클 · 눈밑꺼짐(꺼짐) | P1-5 눈가 + 목적 볼륨 회복 — 근거 P1-5 「다크서클필러」 detail 「눈밑꺼짐」 |
| 모발 | P13 두피/탈모(동의어 사전) |
| Hair · 모발/체모 | P10 제모 + P13 두피/탈모(묶음 규칙) |
| 잇몸미소(잇몸 노출 미소) | 새 고민 항목 「잇몸미소」 @잇몸 — 자갈턱(J8)과 같은 방식 id · 단위 시술 U5-013 잇몸 보톡스로 엣지 |
| 항산화 · 피로회복 · 면역 · 영양보충 | 목적 노드만 · 고민 대응 없음(J9 규칙으로 닫음 · 사람 질문 아님) |

끝 조건: 사람 질문 0 · open 0 · 결정론(cmp) · 고정 시험(새 사전 항목 · 잇몸미소 빼면 open) · concern-check errors 0 · md 셈 파일에서. 키 지우지 말 것(8단계가 읽음). 원천 · DEC 수정 금지.

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_42ed7a4c-9c30-4237-9495-98508794e597 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 실버 7단계 질문 13 닫기" --body "사람 질문 N / 잇몸미소 엣지 N / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 실버 7단계 질문 13 닫기. 상세는 인박스." --enter
```
