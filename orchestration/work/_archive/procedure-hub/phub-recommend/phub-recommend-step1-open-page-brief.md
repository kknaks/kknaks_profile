# [tool_dev] 1단계 「남은 것」 페이지 — 사용자가 한눈에 보고 답하는 곳

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-open.html` 하나(코디가 아티팩트로 게시). 스타일 · 테마 토큰 · 폰트 규칙은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.html` 과 같게. 저장은 window.claude.use('db') 컬렉션 `answers`(항목 id → {choice, note}) · 저장 상태 표시 · U+FFFD 이스케이프 · node 구문 검사 1회.

## 원칙(사용자 요구)
- 「글만 길고 알맹이 없다」 금지 — 항목마다 **한 줄**: 무엇이 · 왜 남았나 · (있으면) 추천. 근거는 접어 둔다
- 쉬운 말. 코드명(D20 등)은 작게 옆에만

## 입력 (전부 읽고 항목을 뽑아라 — 아래 목록은 뼈대, 빠진 것은 파일에서 채워라)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 결정표(오늘 10-27 · 10-28 행 전부) — 이미 정한 것은 넣지 않는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d19.md` · `step1-d20-31.md`(맨 위 「묶음별 추천」 · 「사용자가 판단해야 하는 행」) · `step1-cancel-recheck.md` · `step1-d17-2.md` · `step1-d18.md` · `step1-decisions.json`

## 섹션 (이 순서)
1. **승인만 하면 되는 것(추천 있음)** — 라디오 [추천대로 / 다르게(메모)]
   - D19 처리: 벨라소닉 연결(제인 16-4317) · 벨카이라/카이벨라 미허가(국내 철수) · 이볼브 · 쿨톤 · 더마펜4 · 시너론 아이플러스 미허가 · 미라쥬 · 슬렌더엑스 · 시크릿맥스 · 리포린 확인 불가
   - 8묶음 워커 추천: D25 전부 받기 · D28 유지 · D29(현행 허가 3 둠 · 레티보→보툴렉스 · 8 확인 불가) · D30(채움 · 프락셀 동의어) · D31(오투덤 미용기기 확정 · 메소건 메뉴명 · 벨르업 · 노보젯 확인 불가) · D20 닫힌 5(쥬브아셀 인체조직 · NCTF 국내 허가 못 찾음 · PRX필 · 다복스 · 옥시덤 확인 불가)
   - 규칙으로 정해지는 5: 브이빔 = 라인(Perfecta 18-276 · Prima 21-34) · 하이드라페이셜 = 정상 수입 허가 2건 모두(메디뷰랩 22-213 · 인터엠디 18-215) · 바이리즌 = 라인(HA · PN 품목) · AAPE = 병원용 화장품(허가 대상 아님) · Progen 취하 이력
2. **원천(병원)에 물어볼 것** — 질문 한 줄씩 · 입력칸(받은 답) — 복사 버튼으로 전체 질문 목록 복사
   - 인에이블 · 도프ECM · 아폴로 · 셀피아 · 노보젯 · 피코코어(블루코어 피코어?) · 포토나스타발브 · 센독스 · D22 이름 근거 0 의 10개 · D23 이름 근거 0 의 16개 · D29 확인 불가 8 · 바넥스/바넥스프로 실제 제품 · 힐퓨전프로 · 트리필 프로 · 스킨스탬프 · 미라쥬 수입사 — 파일에서 이름을 정확히
3. **사용자가 확인 중 · 직접 볼 것** — 메모칸
   - 엔진리프팅(현장 명판 — N-Gine?) · BBL 세대 · 국내 허가번호 · 모르페우스8 국내 허가번호(19-352 · 21-205 첨부) · 제네오X 국내 본체 허가 · 구성 · 라라젯 비의료기기 여부(출처) · 타임버스(티엠버스주 — 국문 표기 다름, 같은 제품?) · 취소(이력) 후보: BBL스킨타이트 · E-MAX(elos Plus?)
4. **진행 중(워커)** — 읽기 전용: KPIC MCP 설치 · 검증(리포린 등 의약품 확인용)
5. **답을 다 받은 뒤 할 일** — 읽기 전용 체크리스트: 원장 반영(390행 이름 규칙 · 수출용 허가 빼기 · 취소/취하 이력 · 라인/품목 · 판매사 여러 개 · 원천 수정 목록) · 결정 카드 질문에 제품 이름 · 재검수 → 1단계 끝 → 2단계(바넥스 등 auto- 항목 계열 대조)
- 맨 위: 1단계 상황 한 줄(정해진 묶음 수 / 남은 항목 수 — 섹션별 개수)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 1단계 남은 것 페이지" \
  --body "섹션별 항목 수 / 파일 크기 / 검사 결과"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — 1단계 남은 것 페이지. 상세는 인박스." --enter
```
