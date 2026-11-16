# [researcher] 실버 2단계 검수 FAIL 수정 — review-step2-report 지적

앞 판 반영(`step2-apply.py` → `step2-families.json` · `.md`)을 네가 했다. 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-report.md` 를 읽고 아래대로 고쳐라. 고치는 것은 `step2-apply.py` 다(산출은 재실행으로 — 결정론 유지). step1-products.json 수정 금지.

## 고칠 것 (코디 기본값 — 사용자 결정 「추천대로」 범위)
1. **F1 이름**
   - M2: 식약처 「성형용 필러」 안전정보 페이지 원문을 **다시 열어** 제목 · URL 을 확인한다. 확인되면 `name` = 「성형용 필러」 · `name_status` = 「국내 공식 출처」 · 「필러」는 동의어. 확인 안 되면 「필러」 유지 + `name_status` = 「출처 있음 · 원문 재확인 실패」(사유)
   - M7: 「안면조직고정용실」은 식약처 품목명이지만 M7 12행 중 3행만 해당(PDO 실 = 폴리디옥사논봉합사 등) → 계열 이름으로 쓰지 않는다. `name` = 「실리프팅」 유지 · `name_status` = 「국내 품목명 있음 · 계열 일부만 해당(3/12행) — 공식 일반명 아님」 · 품목명들은 동의어
   - 나머지 계열은 지금대로(「공식 출처 미확인」)
2. **F2 M8 하위**: 리포트 F2 표 9행을 표대로 채운다(피코초 5 · IPL 4)
3. **W1 M8 하위 null 41행**: D18 「광원/방식(M8) → 하위 계열」 규칙대로 **원천 설명 · 허가 품목에 광원이 적힌 행은 광원 하위**(Nd:YAG · 알렉산드라이트 · 다이오드 · Er:YAG · CO2 · Q스위치/롱펄스 등 — 적힌 말 그대로, 새 이름 짓지 마라)로. 근거가 약한 행(리포트가 든 아이콘 · 피콜로 프리미엄 포함)은 null 로 두고 **open[] 에 type `sub_family` + 사유**. M7 null 과 같은 기준으로
4. **W3 M17**: 정의를 받치는 리뷰 문헌 1건 이상 추가(PMID ESummary 확인) · 28296617 은 「부작용 근거」로 표시
5. **W4 · W2**: 셀리뉴 step1 detail 오류는 `step2-families.json` 의 `source_fix_candidates[]`(새 칸)에 기록 · 소노퀸은 `research_errata` 에 「D03 대상 행 · 조사 정정」 표시
6. md 맨 위 셈 · open 수 갱신

결정에 없는 변경 금지 · 추정 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 검수 수정" \
  --body "F1 M2 원문 확인 결과 / M8 하위 채움 N · open N / M17 추가 PMID"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 검수 수정. 상세는 인박스." --enter
```
